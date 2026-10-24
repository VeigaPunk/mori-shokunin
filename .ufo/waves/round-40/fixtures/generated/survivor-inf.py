#!/usr/bin/env python3
"""Round-39 C7 counter v2: fabricated-content discrimination for the drift-corpus
binding (round-38 lesson M18).

Usage:
    count-c7.py <rev> [--repo DIR] [--seed N]
    count-c7.py --print-predicate
    count-c7.py --pin-only [--repo DIR]
    count-c7.py --print-tool <repo-relative path> [--repo DIR]
    count-c7.py <rev> --tool PATH --tool-timeout S --arms selftest [--repo DIR]

Everything scored is read from committed bytes at <rev> (`git show <rev>:<path>`),
so the receipt can be re-derived from the pushed tree alone. The drift-kill
mutation's expected post-state is drawn at run time (seeded); the drawn state is
printed in the receipt, so a probe that hard-codes the expected flip string cannot
know it in advance (r38 M18: the r38 symmetric substring check was gameable).

Checks (P-C7, frozen in ../../contract.md and printed by --print-predicate)
  anchors_v2      every `anchor:` line of the knowledge entry is a unique string of
                  >= 8 characters occurring byte-exactly in tools/mori-source-drift.py
                  at <rev> at a position that is not inside a comment (a line whose
                  stripped form starts with '#' never counts; on any other line the
                  occurrence must start before the first '#' on that line).
  capability_v2   every path the SCORECARD capability row cites resolves at <rev> to
                  a committed file (`git cat-file -t` is `blob`), not a directory.
  live_rows_v2    the live receipt carries one `S### drifted` line per drifted row the
                  summary counts; every named id is a registry row at <rev> and has a
                  committed source copy at <rev> (corpus/evidence/sources-r<N>/
                  <id>.<ext>, highest N).
  named_row_drift as the round-38 counter: the probe's --selftest prints
                  `selftest row_states PASS`.
  drift_kill_v2   the honest and mutated (`return "drifted"` -> `return "<drawn>"`)
                  selftest row_states tables, parsed structurally, are identical
                  except that exactly the rows drifted in the honest table read the
                  drawn state in the mutated table.

Negatives: the three round-38 witnesses (token entry, dangling capability row,
summary-only receipt) plus witness-comment-anchors.md (real anchor strings parked
inside comment lines); each is projected onto the real other bytes and must fail at
least one check.

Exit: 0 met, 1 unmet, 2 counter setup error.
"""
import argparse
import ast
import os
import random
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
EVIDENCE_PREFIX = "corpus/evidence/"
LIVE_REL = ".ufo/waves/round-37/evidence/drift-live-r37.txt"
SCRATCH_ROOT = os.path.join(DEFAULT_REPO, ".ufo", "waves", "round-39", "scratch")
CAPABILITY_KEY = "source-drift re-fetch probe"
DRIFT_MUTANT_FROM = 'return "drifted"'
DRAWN_STATES = ("excerpt", "fresh", "unavailable", "no-copy")
MIN_ANCHORS = 3
MIN_ANCHOR_LEN = 8
MAX_BLOB_BYTES = 8 * 1024 * 1024
GIT_TIMEOUT_S = 120
NAME = 1e400
SELFTEST_BUDGET_S = 120
SELFTEST_GRACE_S = 5
TOOL_TIMEOUT_S = 120
TOOL_GRACE_S = 5

PREDICATE = (
    "P-C7: at revision R, the committed drift-corpus binding passes five content "
    "checks that the round-38 checks could not discriminate — every `anchor:` line "
    "in the knowledge entry is a string of eight or more characters that occurs "
    "byte-exactly in tools/mori-source-drift.py at R at a position that is not "
    "inside a comment; every path the SCORECARD capability row cites resolves at R "
    "to a committed file, not a directory; the live receipt names one drifted row "
    "per drifted row its summary counts and every named id has a committed source "
    "copy at R; and the probe's selftest named-row arm `row_states` is killed by "
    "its own mutation, detected as a structural per-row state difference between "
    "the honest and mutated runs whose expected post-mutation state is drawn at "
    "run time — and the same counter rejects four fabricated witnesses (an entry "
    "carrying tokens with no resolvable anchor, a capability row citing a "
    "nonexistent path, a live receipt with only the summary sentence, a "
    "self-consistent clone whose anchors are parked inside comments) while the "
    "real bytes pass."
)

PATH_RE = re.compile(r"^[A-Za-z0-9_.<>-]+(?:/[A-Za-z0-9_.<>-]+)*\.[A-Za-z0-9]+$")
LIVE_ROW_RE = re.compile(r"^(S\d{3}) drifted$")
SUMMARY_RE = re.compile(
    r"^MORI_SOURCE_DRIFT rows=(\d+) fresh=(\d+) excerpt=(\d+) drifted=(\d+) "
    r"unavailable=(\d+) no-copy=(\d+)$")
COPY_RE = re.compile(r"^corpus/evidence/sources-r(\d+)/(S\d{3})\.[^/]+$")


class ProbeTimeout(Exception):
    pass


class BlobTooLarge(Exception):
    pass


def run(cmd, cwd=None, timeout=NAME, env=None):
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
            try:
                out, err = proc.communicate(timeout=SELFTEST_GRACE_S)
            except subprocess.TimeoutExpired:
                out, err = "", ""
                for stream in (proc.stdout, proc.stderr):
                    try:
                        stream.close()
                    except OSError:
                        pass
        raise ProbeTimeout("child exceeded %ds" % timeout)
    return subprocess.CompletedProcess(cmd, proc.returncode, out, err)


def run_tool(tool, args, timeout=TOOL_TIMEOUT_S):
    """Run the tool under test under the conformance budget (debt (f) trade:
    SIGTERM -> grace -> SIGKILL, disclosed as operator-owned). Raises
    ProbeTimeout when the tool exceeded the budget."""
    proc = subprocess.Popen([sys.executable, tool] + list(args),
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                            start_new_session=True)
    try:
        out, err = proc.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        try:
            os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
        except OSError:
            pass
        try:
            proc.communicate(timeout=TOOL_GRACE_S)
        except subprocess.TimeoutExpired:
            try:
                os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
            except OSError:
                pass
            try:
                proc.communicate(timeout=TOOL_GRACE_S)
            except subprocess.TimeoutExpired:
                for stream in (proc.stdout, proc.stderr):
                    try:
                        stream.close()
                    except OSError:
                        pass
        raise ProbeTimeout("tool exceeded %ds (SIGTERM, then SIGKILL after %ds)"
                           % (timeout, TOOL_GRACE_S))
    if out is None:
        out = ""
    if err is None:
        err = ""
    return subprocess.CompletedProcess([tool] + list(args), proc.returncode, out,
                                       err)


def clean_env():
    env = dict(os.environ)
    for key in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_CONFIG_GLOBAL"):
        env.pop(key, None)
    return env


def git_out(repo, args, timeout=GIT_TIMEOUT_S):
    proc = subprocess.run(["git", "-C", repo] + args, capture_output=True, text=True,
                          timeout=timeout, env=clean_env())
    return proc


def show(repo, rev, rel):
    """Committed bytes of one path at rev, or None when absent."""
    proc = git_out(repo, ["cat-file", "-e", "%s:%s" % (rev, rel)])
    if proc.returncode != 0:
        return None
    size = git_out(repo, ["cat-file", "-s", "%s:%s" % (rev, rel)])
    if size.returncode != 0 or not size.stdout.strip().isdigit():
        return None
    if int(size.stdout.strip()) > MAX_BLOB_BYTES:
        raise BlobTooLarge("%s:%s is %s bytes, cap %d"
                           % (rev, rel, size.stdout.strip(), MAX_BLOB_BYTES))
    proc = git_out(repo, ["show", "%s:%s" % (rev, rel)])
    if proc.returncode != 0:
        return None
    return proc.stdout


def object_type(repo, rev, rel):
    proc = git_out(repo, ["cat-file", "-t", "%s:%s" % (rev, rel)])
    if proc.returncode != 0:
        return None
    return proc.stdout.strip()


def evidence_tree(repo, rev):
    proc = git_out(repo, ["ls-tree", "-r", "--name-only", rev, EVIDENCE_PREFIX])
    if proc.returncode != 0:
        return []
    return proc.stdout.splitlines()


def copy_paths_at(repo, rev):
    """row id -> committed copy path (highest sources-r<N>), like the probe."""
    best = {}
    for line in evidence_tree(repo, rev):
        m = COPY_RE.match(line.strip())
        if not m:
            continue
        n, sid = int(m.group(1)), m.group(2)
        if sid not in best or n > best[sid][0]:
            best[sid] = (n, line.strip())
    return {sid: rel for sid, (_, rel) in best.items()}


def anchors_from(entry_text):
    out = []
    for line in (entry_text or "").splitlines():
        line = line.strip()
        if line.startswith("anchor:"):
            out.append(line[len("anchor:"):].strip())
    return out


def code_occurrences(haystack, needle):
    """Occurrence offsets of needle in haystack that are not inside a comment.

    Rule (documented in P-C7): a line whose stripped form starts with '#' is a
    comment line and never counts; on any other line, an occurrence counts only
    when it starts before the first '#' on that line.
    """
    offsets = []
    start = 0
    while True:
        idx = haystack.find(needle, start)
        if idx < 0:
            return offsets
        line_start = haystack.rfind("\n", 0, idx) + 1
        line_end = haystack.find("\n", idx)
        if line_end < 0:
            line_end = len(haystack)
        line = haystack[line_start:line_end]
        stripped = line.strip()
        comment_at = line.find("#")
        if not stripped.startswith("#") and (comment_at < 0 or idx < line_start + comment_at):
            offsets.append(idx)
        start = idx + 1


def capability_row(scorecard_text):
    rows = [line for line in (scorecard_text or "").splitlines()
            if line.startswith("|") and CAPABILITY_KEY in line]
    return rows[-1] if len(rows) == 1 else None


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


def check_anchors_v2(entry_text, tool_text):
    anchors = anchors_from(entry_text)
    too_short = [a for a in anchors if len(a) < MIN_ANCHOR_LEN]
    no_code = [a for a in anchors if not code_occurrences(tool_text or "", a)]
    unique = len(set(anchors)) == len(anchors)
    ok = (len(anchors) >= MIN_ANCHORS and not too_short and not no_code and unique)
    return ok, "anchors=%d short=%s not_in_code=%s unique=%s" % (
        len(anchors), too_short, no_code, unique)


def check_capability_v2(repo, rev, scorecard_text):
    row = capability_row(scorecard_text)
    if row is None:
        return False, "row absent"
    paths = paths_in(row)
    bad = []
    for rel in paths:
        if object_type(repo, rev, rel) != "blob":
            bad.append(rel)
    return bool(paths) and not bad, "paths=%s not_file=%s" % (paths, bad)


def check_live_rows_v2(live_text, ids, copies):
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
    unique = len(set(named)) == len(named)
    no_copy = [sid for sid in named if sid not in copies]
    ok = (drifted >= 1 and len(named) == drifted and not unknown and unique
          and not no_copy)
    return ok, "named=%d summary_drifted=%d unknown=%s unique=%s no_copy=%s" % (
        len(named), drifted, unknown, unique, no_copy)


def parse_rowstates(output):
    """The row_states arm verdict from selftest output, or None."""
    for line in (output or "").splitlines():
        m = re.match(r"^selftest row_states (PASS|FAIL)(?:\s+\((.*)\))?$",
                     line.strip())
        if m:
            return m.group(1), m.group(2) or ""
    return None


def parse_got_want(detail):
    """(got, want) row tables from a row_states FAIL detail, or None.

    The probe prints `got=[(...)] want=[(...)]` on failure; both tables are
    parsed structurally so a probe that merely mentions both state strings
    elsewhere cannot satisfy the comparison.
    """
    got_m = re.search(r"got=(\[\(.*?\)\])\s+want=", detail)
    want_m = re.search(r"want=(\[.*\])$", detail)
    if not got_m or not want_m:
        return None
    try:
        got_raw = ast.literal_eval(got_m.group(1))
        want_raw = ast.literal_eval(want_m.group(1))
    except (SyntaxError, ValueError):
        return None
    def table(raw):
        out = {}
        for entry in raw:
            if not (isinstance(entry, (tuple, list)) and len(entry) == 2):
                return None
            out[str(entry[0])] = str(entry[1])
        return out
    got, want = table(got_raw), table(want_raw)
    if got is None or want is None:
        return None
    return got, want


def selftest_arms(path):
    try:
        proc = run([sys.executable, path, "--selftest"], cwd=os.path.dirname(path),
                   timeout=SELFTEST_BUDGET_S, env=clean_env())
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
    parser.add_argument("rev", nargs="?")
    parser.add_argument("--repo", default=DEFAULT_REPO)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--tool")
    parser.add_argument("--tool-timeout", type=int, default=TOOL_TIMEOUT_S)
    parser.add_argument("--arms")
    parser.add_argument("--print-predicate", action="store_true")
    parser.add_argument("--pin-only", action="store_true")
    parser.add_argument("--print-tool")
    args = parser.parse_args(argv)

    if args.print_predicate:
        print(PREDICATE)
        return 0

    repo = os.path.abspath(args.repo)

    if args.pin_only:
        proc = git_out(repo, ["rev-parse", "HEAD"])
        if proc.returncode != 0:
            print("counter setup error: cannot read lane tip", file=sys.stderr)
            return 2
        print("head_at_measurement=%s" % proc.stdout.strip())
        return 0

    if args.print_tool:
        print(os.path.abspath(os.path.join(repo, args.print_tool)))
        return 0

    if args.rev is None:
        print("counter setup error: rev is required", file=sys.stderr)
        return 2


    rev = git_out(repo, ["rev-parse", "--verify", args.rev + "^{commit}"]).stdout.strip()
    if not rev:
        print("counter setup error: cannot resolve %s in %s" % (args.rev, repo),
              file=sys.stderr)
        return 2

    # conformance behavioural arm: the tool under test run under a budget
    if args.arms == "selftest":
        if not args.tool:
            print("counter setup error: --arms selftest requires --tool",
                  file=sys.stderr)
            return 2
        try:
            proc = run_tool(args.tool, ["--selftest"], args.tool_timeout)
        except ProbeTimeout as exc:
            print("tool selftest: tool_timeout (%s)" % exc)
            print("C7=unmet")
            return 1
        arm = parse_rowstates(proc.stdout)
        if proc.returncode == 0 and arm and arm[0] == "PASS":
            print("tool selftest: pass")
            print("C7=met")
            return 0
        print("tool selftest: fail exit=%s row_states=%s" % (proc.returncode, arm))
        print("C7=unmet")
        return 1

    print(PREDICATE)
    checks = []

    def check(name, ok, detail):
        checks.append((name, bool(ok), detail))

    try:
        tool_text = show(repo, rev, TOOL_REL)
        entry_text = show(repo, rev, ENTRY_REL)
        scorecard_text = show(repo, rev, SCORECARD_REL) or ""
        live_text = show(repo, rev, LIVE_REL)
        sources_text = show(repo, rev, SOURCES_REL) or ""
    except BlobTooLarge as exc:
        print("counter setup error: %s" % exc, file=sys.stderr)
        return 2
    ids = registry_ids(sources_text)
    copies = copy_paths_at(repo, rev)

    check("anchors_v2", *check_anchors_v2(entry_text, tool_text))
    check("capability_v2", *check_capability_v2(repo, rev, scorecard_text))
    check("live_rows_v2", *check_live_rows_v2(live_text, ids, copies))

    os.makedirs(SCRATCH_ROOT, exist_ok=True)
    work = tempfile.mkdtemp(prefix="mori-c7-", dir=SCRATCH_ROOT)
    drawn = None
    try:
        if tool_text is not None:
            tool = os.path.join(work, "mori-source-drift.py")
            with open(tool, "w", encoding="utf-8") as handle:
                handle.write(tool_text)
            rc, arms, out = selftest_arms(tool)
            check("named_row_drift", rc == 0 and arms.get("row_states", ("",))[0] == "PASS",
                  "exit=%s row_states=%s" % (rc, arms.get("row_states")))
            rng = random.Random(args.seed)
            drawn = rng.choice(DRAWN_STATES)
            if DRIFT_MUTANT_FROM in tool_text:
                mutant = os.path.join(work, "drift-mutant.py")
                with open(mutant, "w", encoding="utf-8") as handle:
                    handle.write(tool_text.replace(DRIFT_MUTANT_FROM,
                                                   'return "%s"' % drawn))
                kill_rc, kill_arms, kill_out = selftest_arms(mutant)
                state = kill_arms.get("row_states", ("", ""))
                ok = False
                detail = "drawn=%s exit=%s row_states=%s" % (
                    drawn, kill_rc, kill_arms.get("row_states"))
                parsed = parse_got_want(state[1]) if state[0] == "FAIL" else None
                if parsed is not None:
                    got, want = parsed
                    want_drifted = sorted(r for r, s in want.items() if s == "drifted")
                    if (kill_rc == 1 and set(got) == set(want)
                            and want_drifted
                            and all(got[r] == drawn for r in want_drifted)
                            and all(got[r] == want[r] for r in want
                                   if want[r] != "drifted")):
                        ok = True
                    detail += " want_drifted=%s flips_ok=%s" % (
                        want_drifted,
                        parsed is not None and set(got) == set(want))
                check("drift_kill_v2", ok, detail)
            else:
                check("drift_kill_v2", False, "mutation anchor absent")
        else:
            for name in ("named_row_drift", "drift_kill_v2"):
                check(name, False, "tool absent")
    finally:
        shutil.rmtree(work, ignore_errors=True)

    # fabricated witnesses, projected onto the real other bytes
    fixtures = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures")
    try:
        token_entry = open(os.path.join(fixtures, "witness-token-entry.md"),
                           encoding="utf-8").read()
        dangling_row = open(os.path.join(fixtures, "witness-dangling-row.md"),
                           encoding="utf-8").read()
        summary_only_live = open(os.path.join(fixtures,
                                              "witness-summary-only-live.txt"),
                                 encoding="utf-8").read()
        comment_entry = open(os.path.join(fixtures, "witness-comment-anchors.md"),
                             encoding="utf-8").read()
    except OSError as exc:
        print("counter setup error: %s" % exc, file=sys.stderr)
        return 2

    def all_v2(entry, scorecard, live):
        return (check_anchors_v2(entry, tool_text)[0]
                and check_capability_v2(repo, rev, scorecard)[0]
                and check_live_rows_v2(live, ids, copies)[0])

    negatives = [
        ("witness-token-entry",
         all_v2(token_entry, scorecard_text, live_text)),
        ("witness-dangling-row",
         all_v2(entry_text, dangling_row, live_text)),
        ("witness-summary-only-live",
         all_v2(entry_text, scorecard_text, summary_only_live)),
        ("witness-comment-anchors",
         all_v2(comment_entry, scorecard_text, live_text)),
    ]
    rejected = []
    for name, accepted in negatives:
        print("negative %-26s %s" % (name, "ACCEPTED" if accepted else "rejected"))
        rejected.append(not accepted)

    for name, ok, detail in checks:
        print("check %-16s %s (%s)" % (name, "PASS" if ok else "FAIL", detail))
    met = all(ok for _, ok, _ in checks) and all(rejected)
    print("C7=%s" % ("met" if met else "unmet"))
    return 0 if met else 1


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except Exception as exc:  # counter setup error
        print("counter setup error: %s" % exc, file=sys.stderr)
        sys.exit(2)
