#!/usr/bin/env python3
"""Round-38 C4 counter v1: the content half of the drift-corpus binding (r37 M9).

Usage:
    count-c4.py <rev> [--repo DIR]

Everything is read from committed bytes at <rev> (`git show <rev>:<path>`), so the
receipt can be re-derived from the pushed tree alone.

Checks
  anchors         every line of corpus/knowledge/source-drift-content-anchor-r38.md that
                  starts `anchor:` names a code string; each string must occur verbatim
                  in tools/mori-source-drift.py at <rev>. At least three anchor lines.
  capability      the last SCORECARD.md row containing `source-drift re-fetch probe`
                  cites only paths that resolve at <rev> from the repository root.
  live_rows       the live receipt carries one `<S###> drifted` line per drifted row the
                  summary counts, and every named id is a registry row at <rev>.
  named_row_drift the probe's --selftest prints `selftest row_states PASS` (the arm that
                  asserts a named row S103 grades drifted).
  drift_kill      a copy with `return "drifted"` replaced by `return "excerpt"` must FAIL
                  `selftest row_states`, and the failure must name S103.

Negatives: three fabricated token-satisfying witnesses (an entry carrying only the r37
tokens with no `anchor:` line, a capability row citing a nonexistent path, a live
receipt carrying only the summary line) are projected onto the real bytes; each must
fail at least one check.

Exit: 0 met, 1 unmet, 2 counter setup error.
"""
import argparse
import os
import re
import shutil
import signal
import subprocess
import sys
import tempfile

DEFAULT_REPO = "/home/vgpnk/Projects/shokunin/mori-shokunin"
TOOL_REL = "tools/mori-source-drift.py"
ENTRY_REL = "corpus/knowledge/source-drift-content-anchor-r38.md"
SCORECARD_REL = "SCORECARD.md"
SOURCES_REL = "corpus/SOURCES.md"
LIVE_REL = ".ufo/waves/round-37/evidence/drift-live-r37.txt"
SCRATCH_ROOT = os.path.join(DEFAULT_REPO, ".ufo", "waves", "round-38", "scratch")
CAPABILITY_KEY = "source-drift re-fetch probe"
DRIFT_MUTANT_FROM = 'return "drifted"'
DRIFT_MUTANT_TO = 'return "excerpt"'
MIN_ANCHORS = 3
SELFTEST_BUDGET_S = 120
SELFTEST_GRACE_S = 5

PREDICATE = (
    "P-C4: at revision R, the committed drift-corpus binding passes four content checks "
    "that the round-37 token checks cannot discriminate — every `anchor:` line in the "
    "round-38 knowledge entry resolves byte-exactly in tools/mori-source-drift.py at R, "
    "every path the SCORECARD capability row cites resolves at R, the live receipt names "
    "one drifted row by id per drifted row its summary counts, and the probe's selftest "
    "runs the named-row arm `row_states` whose own mutation kills it — and the same "
    "counter rejects three fabricated token-satisfying witnesses (an entry with the "
    "tokens but no resolvable anchor, a capability row citing a nonexistent path, a live "
    "receipt with only the summary sentence), while the real bytes pass."
)

PATH_RE = re.compile(r"^[A-Za-z0-9_.-]+(/[A-Za-z0-9_.<>-]+)+$")
ROW_RE = re.compile(r"^S\d{3} (fresh|excerpt|drifted|unavailable|no-copy)$")
LIVE_ROW_RE = re.compile(r"^(S\d{3}) drifted$")
SUMMARY_RE = re.compile(
    r"^MORI_SOURCE_DRIFT rows=(\d+) fresh=(\d+) excerpt=(\d+) drifted=(\d+) "
    r"unavailable=(\d+) no-copy=(\d+)$")


class ProbeTimeout(Exception):
    pass


def run(cmd, cwd=None, timeout=SELFTEST_BUDGET_S, env=None):
    proc = subprocess.Popen(cmd, cwd=cwd, env=env, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, text=True, start_new_session=True)
    try:
        out, err = proc.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        try:
            os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
        except OSError:
            pass
        try:
            out, err = proc.communicate(timeout=SELFTEST_GRACE_S)
        except subprocess.TimeoutExpired:
            try:
                os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
            except OSError:
                pass
            out, err = proc.communicate()
        raise ProbeTimeout("selftest exceeded %ds" % timeout)
    return subprocess.CompletedProcess(cmd, proc.returncode, out, err)


def clean_env():
    env = dict(os.environ)
    for key in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_CONFIG_GLOBAL"):
        env.pop(key, None)
    return env


def show(repo, rev, rel):
    """Committed bytes of one path at rev, or None when absent."""
    proc = subprocess.run(["git", "-C", repo, "cat-file", "-e", "%s:%s" % (rev, rel)],
                          capture_output=True, env=clean_env(), timeout=120)
    if proc.returncode != 0:
        return None
    proc = subprocess.run(["git", "-C", repo, "show", "%s:%s" % (rev, rel)],
                          capture_output=True, text=True, env=clean_env(), timeout=120)
    if proc.returncode != 0:
        return None
    return proc.stdout


def resolves(repo, rev, rel):
    proc = subprocess.run(["git", "-C", repo, "cat-file", "-e", "%s:%s" % (rev, rel)],
                          capture_output=True, env=clean_env(), timeout=120)
    return proc.returncode == 0


def anchors_from(entry_text):
    out = []
    for line in (entry_text or "").splitlines():
        line = line.strip()
        if line.startswith("anchor:"):
            out.append(line[len("anchor:"):].strip())
    return out


def capability_row(scorecard_text):
    row = None
    for line in (scorecard_text or "").splitlines():
        if line.startswith("|") and CAPABILITY_KEY in line:
            row = line
    return row


def paths_in(text):
    out = []
    for token in re.findall(r"`([^`\n]+)`", text or ""):
        token = token.strip().rstrip(".,;)")
        if token.startswith("http"):
            continue
        if PATH_RE.match(token):
            out.append(token)
    return out


def registry_ids(sources_text):
    return set(re.findall(r"^\| (S\d{3}) ", sources_text or "", re.M))


def check_anchors(entry_text, tool_text):
    anchors = anchors_from(entry_text)
    missing = [a for a in anchors if a not in (tool_text or "")]
    return (len(anchors) >= MIN_ANCHORS and not missing,
            "anchors=%d missing=%s" % (len(anchors), missing))


def check_capability(scorecard_text):
    row = capability_row(scorecard_text)
    if row is None:
        return False, "row absent"
    paths = paths_in(row)
    return bool(paths), "paths=%s" % paths


def check_live_rows(live_text, ids):
    lines = [l.strip() for l in (live_text or "").splitlines()]
    summary = None
    for line in lines:
        m = SUMMARY_RE.match(line)
        if m:
            summary = m
    named = [LIVE_ROW_RE.match(l).group(1) for l in lines if LIVE_ROW_RE.match(l)]
    if summary is None:
        return False, "summary absent"
    drifted = int(summary.group(4))
    unknown = [sid for sid in named if sid not in ids]
    return (drifted >= 1 and len(named) == drifted and not unknown,
            "named=%d summary_drifted=%d unknown=%s" % (len(named), drifted, unknown))


def selftest_arms(path):
    try:
        proc = run([sys.executable, path, "--selftest"], cwd=os.path.dirname(path),
                   env=clean_env())
    except ProbeTimeout as exc:
        return None, {}, str(exc)
    arms = {}
    for line in proc.stdout.splitlines():
        m = re.match(r"^selftest (\S+)\s+(PASS|FAIL)(?:\s+\((.*)\))?$", line.strip())
        if m:
            arms[m.group(1)] = (m.group(2), m.group(3) or "")
    return proc.returncode, arms, proc.stdout + proc.stderr


def main(argv):
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument("rev")
    parser.add_argument("--repo", default=DEFAULT_REPO)
    args = parser.parse_args(argv)

    print(PREDICATE)
    repo = os.path.abspath(args.repo)
    checks = []

    def check(name, ok, detail):
        checks.append((name, bool(ok), detail))

    rev = subprocess.run(["git", "-C", repo, "rev-parse", "--verify",
                          args.rev + "^{commit}"], capture_output=True, text=True,
                         env=clean_env(), timeout=120).stdout.strip()
    if not rev:
        print("counter setup error: cannot resolve %s in %s" % (args.rev, repo),
              file=sys.stderr)
        return 2

    tool_text = show(repo, rev, TOOL_REL)
    entry_text = show(repo, rev, ENTRY_REL)
    scorecard_text = show(repo, rev, SCORECARD_REL) or ""
    live_text = show(repo, rev, LIVE_REL)
    sources_text = show(repo, rev, SOURCES_REL) or ""
    ids = registry_ids(sources_text)

    real_anchor, real_anchor_detail = check_anchors(entry_text, tool_text)
    real_cap_ok, real_cap_detail = check_capability(scorecard_text)
    cap_paths = paths_in(capability_row(scorecard_text) or "")
    cap_missing = [p for p in cap_paths if not resolves(repo, rev, p)]
    real_cap = real_cap_ok and not cap_missing
    real_live, real_live_detail = check_live_rows(live_text, ids)

    anchors = anchors_from(entry_text)
    rows = [l.strip() for l in (live_text or "").splitlines()]
    named = [LIVE_ROW_RE.match(l).group(1) for l in rows if LIVE_ROW_RE.match(l)]
    del anchors, named

    check("anchors", real_anchor, real_anchor_detail)
    check("capability", real_cap,
          "%s missing=%s" % (real_cap_detail, cap_missing))
    check("live_rows", real_live, real_live_detail)

    os.makedirs(SCRATCH_ROOT, exist_ok=True)
    work = tempfile.mkdtemp(prefix="mori-c4-", dir=SCRATCH_ROOT)
    try:
        arms = {}
        kill_arms = {}
        if tool_text is not None:
            tool = os.path.join(work, "mori-source-drift.py")
            with open(tool, "w", encoding="utf-8") as handle:
                handle.write(tool_text)
            rc, arms, out = selftest_arms(tool)
            check("named_row_drift", rc == 0 and arms.get("row_states", ("",))[0] == "PASS",
                  "exit=%s row_states=%s" % (rc, arms.get("row_states")))
            if DRIFT_MUTANT_FROM in tool_text:
                mutant = os.path.join(work, "drift-mutant.py")
                with open(mutant, "w", encoding="utf-8") as handle:
                    handle.write(tool_text.replace(DRIFT_MUTANT_FROM, DRIFT_MUTANT_TO))
                kill_rc, kill_arms, kill_out = selftest_arms(mutant)
                state = kill_arms.get("row_states", ("", ""))
                check("drift_kill", kill_rc == 1 and state[0] == "FAIL"
                      and "S103" in state[1],
                      "exit=%s row_states=%s" % (kill_rc, state))
            else:
                check("drift_kill", False, "mutation anchor absent")
        else:
            for name in ("named_row_drift", "drift_kill"):
                check(name, False, "tool absent")
    finally:
        shutil.rmtree(work, ignore_errors=True)

    # fabricated token-satisfying witnesses, projected onto the real other bytes
    fixtures = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures")
    try:
        token_entry = open(os.path.join(fixtures, "witness-token-entry.md"),
                           encoding="utf-8").read()
        dangling_row = open(os.path.join(fixtures, "witness-dangling-row.md"),
                            encoding="utf-8").read()
        summary_only_live = open(os.path.join(fixtures,
                                              "witness-summary-only-live.txt"),
                                 encoding="utf-8").read()
    except OSError as exc:
        print("counter setup error: %s" % exc, file=sys.stderr)
        return 2
    negatives = [
        ("witness-token-entry",
         check_anchors(token_entry, tool_text)[0]
         and check_capability(scorecard_text)[0]
         and all(resolves(repo, rev, p)
                 for p in paths_in(capability_row(scorecard_text) or ""))
         and check_live_rows(live_text, ids)[0]),
        ("witness-dangling-row",
         check_anchors(entry_text, tool_text)[0]
         and check_capability(dangling_row)[0]
         and all(resolves(repo, rev, p) for p in paths_in(dangling_row))
         and check_live_rows(live_text, ids)[0]),
        ("witness-summary-only-live",
         check_anchors(entry_text, tool_text)[0]
         and check_capability(scorecard_text)[0]
         and all(resolves(repo, rev, p)
                 for p in paths_in(capability_row(scorecard_text) or ""))
         and check_live_rows(summary_only_live, ids)[0]),
    ]
    rejected = []
    for name, accepted in negatives:
        print("negative %-26s %s" % (name, "ACCEPTED" if accepted else "rejected"))
        rejected.append(not accepted)

    for name, ok, detail in checks:
        print("check %-16s %s (%s)" % (name, "PASS" if ok else "FAIL", detail))
    met = all(ok for _, ok, _ in checks) and all(rejected)
    print("C4=%s" % ("met" if met else "unmet"))
    return 0 if met else 1


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except Exception as exc:  # counter setup error
        print("counter setup error: %s" % exc, file=sys.stderr)
        sys.exit(2)
