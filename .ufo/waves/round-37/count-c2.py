#!/usr/bin/env python3
"""Round-37 C2 counter: is the source-drift probe's hardening load-bearing and bound?

Usage:
    count-c2.py <rev> [--repo DIR]

Everything is read from committed bytes at <rev> (`git show <rev>:<path>`), so the
receipt can be re-derived by a closure from the pushed tree alone.

Checks
  tool        tools/mori-source-drift.py exists at <rev> and its --selftest exits 0
              with the two named round-37 arms green:
              `selftest huge_cap PASS`, `selftest redirect_private_refused PASS`.
  cap-kill    a copy with `FETCH_MAX_BYTES = 4 * 1024 * 1024` replaced by `1 << 40`
              must FAIL `selftest huge_cap` (the cap is load-bearing).
  redirect-kill a copy with `if not _public_redirect_target(final):` replaced by
              `if False:` must FAIL `selftest redirect_private_refused` (the policy is
              load-bearing).
  knowledge   corpus/knowledge/source-drift-hardening-r37.md exists, names both arms,
              the hardening commit `8ff9bba`, and cites at least one `S2##` source row
              opened this round.
  capability  SCORECARD.md carries a capabilities row named `source-drift re-fetch probe`
              that points at tools/mori-source-drift.py.
  readme      the `## Coverage map` table carries a row for knowledge/source-drift-r36.md
              and one for knowledge/source-drift-hardening-r37.md.
  live        .ufo/waves/round-37/evidence/drift-live-r37.txt carries the round's live
              summary line (a demonstration, not a freshness verdict).

Exit: 0 met, 1 unmet, 2 counter setup error. Timeouts: the probe is run under a bounded
budget; on expiry the child's process group gets SIGTERM, then SIGKILL after 5 s, and the
check reports `probe_timeout` — never a silent pass.
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
KNOWLEDGE_REL = "corpus/knowledge/source-drift-hardening-r37.md"
SCORECARD_REL = "SCORECARD.md"
README_REL = "corpus/README.md"
LIVE_REL = ".ufo/waves/round-37/evidence/drift-live-r37.txt"
HARDENING_COMMIT = "8ff9bba"
LIVE_SENTENCE = "MORI_SOURCE_DRIFT rows=220 fresh=49 excerpt=0 drifted=9 unavailable=0 no-copy=162"
CAP_ANCHOR = "FETCH_MAX_BYTES = 4 * 1024 * 1024"
CAP_MUTANT = "FETCH_MAX_BYTES = 1 << 40"
REDIRECT_ANCHOR = "if not _public_redirect_target(final):"
REDIRECT_MUTANT = "if False:  # round-37 mutation: policy removed"
PROBE_BUDGET_S = 180
PROBE_GRACE_S = 5

PREDICATE = (
    "P-C2: at revision R, tools/mori-source-drift.py passes its selftest with the named "
    "arms `huge_cap` and `redirect_private_refused`, each of those arms fails in a copy "
    "with its policy removed (4 MiB read cap; post-redirect public-destination policy), "
    "and the committed corpus binds the hardening (knowledge entry citing this round's "
    "source rows and commit 8ff9bba, a SCORECARD capability row, two README coverage-map "
    "rows) with the round's live sweep receipt present."
)


class ProbeTimeout(Exception):
    pass


def run(cmd, cwd=None, timeout=PROBE_BUDGET_S, env=None):
    """Bounded child run: SIGTERM the group, grace, then SIGKILL only that group."""
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
            out, err = proc.communicate(timeout=PROBE_GRACE_S)
        except subprocess.TimeoutExpired:
            try:
                os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
            except OSError:
                pass
            out, err = proc.communicate()
        raise ProbeTimeout("probe exceeded %ds (SIGTERM, then SIGKILL after %ds)"
                           % (timeout, PROBE_GRACE_S))
    return subprocess.CompletedProcess(cmd, proc.returncode, out, err)


def clean_env():
    env = dict(os.environ)
    for key in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_CONFIG_GLOBAL"):
        env.pop(key, None)
    return env


def show(repo, rev, rel):
    """Committed bytes of one path at rev, or None when absent."""
    proc = subprocess.run(["git", "-C", repo, "cat-file", "-e", "%s:%s" % (rev, rel)],
                          capture_output=True)
    if proc.returncode != 0:
        return None
    proc = subprocess.run(["git", "-C", repo, "show", "%s:%s" % (rev, rel)],
                          capture_output=True, text=True, env=clean_env())
    if proc.returncode != 0:
        return None
    return proc.stdout


def selftest(path):
    """Run one probe copy's --selftest; return (exit, lines, output)."""
    try:
        proc = run([sys.executable, path, "--selftest"], cwd=os.path.dirname(path),
                   env=clean_env())
    except ProbeTimeout as exc:
        return None, {}, str(exc)
    lines = {}
    for line in proc.stdout.splitlines():
        m = re.match(r"^selftest (\S+)\s+(PASS|FAIL)\b", line.strip())
        if m:
            lines[m.group(1)] = m.group(2)
    return proc.returncode, lines, proc.stdout + proc.stderr


def coverage_map(text):
    """The `## Coverage map` table body (up to the next heading)."""
    if text is None:
        return ""
    m = re.search(r"^## Coverage map\s*$(.*?)(?=^## |\Z)", text, re.M | re.S)
    return m.group(1) if m else ""


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

    tool_text = show(repo, args.rev, TOOL_REL)
    check("tool_present", tool_text is not None, "path=%s" % TOOL_REL)
    work = tempfile.mkdtemp(prefix="mori-c2-r37-")
    try:
        tool = os.path.join(work, "mori-source-drift.py")
        if tool_text is not None:
            with open(tool, "w", encoding="utf-8") as handle:
                handle.write(tool_text)

            rc, lines, out = selftest(tool)
            check("selftest", rc == 0 and lines.get("huge_cap") == "PASS"
                  and lines.get("redirect_private_refused") == "PASS"
                  and len(lines) >= 6,
                  "exit=%s arms=%s" % (rc, sorted(lines.items())))

            cap = os.path.join(work, "cap-mutant.py")
            with open(cap, "w", encoding="utf-8") as handle:
                handle.write(tool_text.replace(CAP_ANCHOR, CAP_MUTANT))
            cap_rc, cap_lines, _ = selftest(cap)
            check("cap_kill", cap_rc == 1 and cap_lines.get("huge_cap") == "FAIL",
                  "exit=%s huge_cap=%s" % (cap_rc, cap_lines.get("huge_cap")))

            redir = os.path.join(work, "redirect-mutant.py")
            with open(redir, "w", encoding="utf-8") as handle:
                handle.write(tool_text.replace(REDIRECT_ANCHOR, REDIRECT_MUTANT))
            redir_rc, redir_lines, _ = selftest(redir)
            check("redirect_kill",
                  redir_rc == 1 and redir_lines.get("redirect_private_refused") == "FAIL",
                  "exit=%s redirect_private_refused=%s"
                  % (redir_rc, redir_lines.get("redirect_private_refused")))
        else:
            for name in ("selftest", "cap_kill", "redirect_kill"):
                check(name, False, "tool absent")
    finally:
        shutil.rmtree(work, ignore_errors=True)

    knowledge = show(repo, args.rev, KNOWLEDGE_REL)
    rows = re.findall(r"\bS2\d\d\b", knowledge or "")
    check("knowledge", knowledge is not None
          and "huge_cap" in knowledge and "redirect_private_refused" in knowledge
          and HARDENING_COMMIT in knowledge and bool(rows),
          "present=%s rows=%s cited_commit=%s"
          % (knowledge is not None, sorted(set(rows)), HARDENING_COMMIT in (knowledge or "")))

    scorecard = show(repo, args.rev, SCORECARD_REL) or ""
    cap_rows = [line for line in scorecard.splitlines()
                if line.startswith("|") and "source-drift re-fetch probe" in line]
    check("capability", bool(cap_rows) and TOOL_REL in cap_rows[-1],
          "rows=%d names_tool=%s" % (len(cap_rows),
                                     bool(cap_rows) and TOOL_REL in cap_rows[-1]))

    readme = coverage_map(show(repo, args.rev, README_REL))
    check("readme", "knowledge/source-drift-r36.md" in readme
          and "knowledge/source-drift-hardening-r37.md" in readme,
          "r36_row=%s r37_row=%s" % ("knowledge/source-drift-r36.md" in readme,
                                     "knowledge/source-drift-hardening-r37.md" in readme))

    live = show(repo, args.rev, LIVE_REL)
    check("live", live is not None and LIVE_SENTENCE in live,
          "present=%s sentence=%s" % (live is not None,
                                      bool(live) and LIVE_SENTENCE in live))

    for name, ok, detail in checks:
        print("check %-14s %s (%s)" % (name, "PASS" if ok else "FAIL", detail))
    met = all(ok for _, ok, _ in checks)
    print("C2=%s" % ("met" if met else "unmet"))
    return 0 if met else 1


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except Exception as exc:
        print("counter setup error: %s" % exc, file=sys.stderr)
        sys.exit(2)
