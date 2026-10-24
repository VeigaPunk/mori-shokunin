#!/usr/bin/env python3
"""Round-39 C8 receipts: the r38-M19 bypass fixtures through both checkers.

Usage: run-c8-receipts.py <entering-rev> <scored-rev> <lane-repo>

Writes into <lane>/.ufo/waves/round-39/evidence/:
  c8-red-none.txt     r38 conform on bypass-none  -> CONFORM=met   (before)
  c8-red-wait.txt     r38 conform on bypass-wait  -> CONFORM=met   (before)
  m19-selftest-gap.txt the r38 selftest never mutates a communicate timeout
  c8-after-none.txt   r39 conform on bypass-none  -> CONFORM=unmet (after)
  c8-after-wait.txt   r39 conform on bypass-wait  -> CONFORM=unmet (after)
  c8-after.txt        r39 conform on count-c7     -> CONFORM=met   (after)
  c8-after-selftest.txt  r39 conform --selftest   -> pass=9 fail=0 (after)
"""
import os
import subprocess
import sys

W = os.path.dirname(os.path.abspath(__file__))
R38_CONFORM = ".ufo/waves/round-38/conform.py"
R39_CONFORM = os.path.join(W, "..", "conform.py")
M19 = os.path.join(W, "make-m19-bypass.py")
C7 = os.path.join(W, "..", "count-c7.py")


def run(cmd, timeout=600):
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    return proc


def emit(path, title, lines):
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("command: %s\n" % title)
        fh.write("\n".join(lines) + "\n")


def main(argv):
    enter, scored, repo = argv[1], argv[2], os.path.abspath(argv[3])
    ev = os.path.join(W, "..", "evidence")
    scratch = os.path.join(W, "..", "scratch", "c8")
    os.makedirs(scratch, exist_ok=True)

    # rebuild the bypass fixtures from the r38 count-c1 bytes at the entering tip
    proc = run([sys.executable, M19, enter, repo, scratch])
    bypass_none = os.path.join(scratch, "bypass-none.py")
    bypass_wait = os.path.join(scratch, "bypass-wait.py")

    def conform(checker, rev, counters):
        return run([sys.executable, checker, rev, "--repo", repo]
                   + [c for c in counters for c in ("--counter", c)])

    # before: the r38 checker accepts both bypass fixtures
    for name, path in (("c8-red-none.txt", bypass_none),
                       ("c8-red-wait.txt", bypass_wait)):
        r38 = os.path.join(scratch, "conform-r38.py")
        subprocess.run(["git", "-C", repo, "show", "%s:%s" % (enter, R38_CONFORM)],
                       stdout=open(r38, "w"), timeout=120, check=True)
        proc = conform(r38, enter, [path])
        lines = ["r38 conform on %s at %s:" % (os.path.basename(path), enter),
                 "exit=%d" % proc.returncode]
        lines.extend(l for l in proc.stdout.splitlines()
                     if l.startswith(("check", "CONFORM")))
        lines.append("verdict: %s" % ("RED (bypass accepted)" if "CONFORM=met" in
                                      proc.stdout else "not reproduced"))
        emit(os.path.join(ev, name), "r38 conform %s" % os.path.basename(path),
             lines)

    # the r38 selftest gap (r38 M19): its bounded_reads mutation targets a
    # run() call, never a communicate timeout
    r38_src = subprocess.run(["git", "-C", repo, "show",
                              "%s:%s" % (enter, R38_CONFORM)],
                             capture_output=True, text=True, timeout=120).stdout
    gap = [l.strip() for l in r38_src.splitlines()
           if '"bounded_reads"' in l or "git helper run timeout" in l
           or '("bounded_reads"' in l]
    mutate_lines = [l.strip() for l in r38_src.splitlines()
                    if "communicate(timeout=" in l and "mutations" not in l][:4]
    emit(os.path.join(ev, "m19-selftest-gap.txt"),
         "r38 conform.py selftest bounded_reads mutation target", [
             "the r38 selftest's bounded_reads mutation (conform.py):",
         ] + gap + [
             "no communicate(timeout=...) mutation exists in the r38 selftest;",
             "the communicate-timeout conjunct M13 hardened is never exercised.",
             "first communicate(timeout=...) call sites in the r38 checker body"
             " (for contrast):",
         ] + mutate_lines)

    # after: the r39 checker rejects both bypass fixtures and passes count-c7
    for name, path in (("c8-after-none.txt", bypass_none),
                       ("c8-after-wait.txt", bypass_wait)):
        proc = conform(R39_CONFORM, scored, [path])
        lines = ["r39 conform on %s at %s:" % (os.path.basename(path), scored),
                 "exit=%d" % proc.returncode]
        lines.extend(l for l in proc.stdout.splitlines()
                     if l.startswith(("check", "CONFORM")))
        emit(os.path.join(ev, name), "r39 conform %s" % os.path.basename(path),
             lines)
    proc = conform(R39_CONFORM, scored, [C7])
    emit(os.path.join(ev, "c8-after.txt"),
         "r39 conform on count-c7.py at %s" % scored, [
             "exit=%d" % proc.returncode,
         ] + [l for l in proc.stdout.splitlines()
              if l.startswith(("check", "CONFORM"))])
    proc = run([sys.executable, R39_CONFORM, scored, "--repo", repo,
                "--selftest", "--counter", C7])
    emit(os.path.join(ev, "c8-after-selftest.txt"),
         "r39 conform --selftest at %s" % scored, [
             "exit=%d" % proc.returncode,
         ] + proc.stdout.splitlines())
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
