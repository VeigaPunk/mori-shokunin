#!/usr/bin/env python3
"""End-to-end: frozen count-c1 helpers (clone_fixture/run_graded/fixture_verdict) with extra
`# cmd:` fixtures, graded by the r87 gate at <rev>; plus a C2 syntax-error kill probe via the frozen
count-c2 grade(). Usage: e2e.py <repo> <rev>"""
import importlib.util, os, subprocess, sys
sys.dont_write_bytecode = True
L = "/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-89/"


def load(n):
    s = importlib.util.spec_from_file_location(n.replace("-", "_"), L + n + ".py")
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


c1, c2 = load("count-c1"), load("count-c2")
repo, rev = sys.argv[1], sys.argv[2]
scratch = os.environ["TMPDIR"]
B, P = c1.BOUND, "--root . --pins " + c1.PIN
BODY = c1.BODY
EXTRA = (
    ("H01or", "true || python3 -I %s %s; printf '%%s\\n' '%s'" % (B, P, BODY), "refused"),
    ("H02falseand", "false && python3 -I %s %s; printf '%%s\\n' '%s'" % (B, P, BODY), "refused"),
    ("H03exit", "printf '%%s\\n' '%s'; exit 0; python3 -I %s %s" % (BODY, B, P), "refused"),
    ("H10devnull", "python3 -I %s %s >/dev/null; printf '%%s\\n' '%s'" % (B, P, BODY), "refused"),
    ("M07subshell", "(cd . && python3 -I %s %s)" % (B, P), "accepted"),
)
c1.FIXTURES = c1.FIXTURES + EXTRA
graded = os.path.join(scratch, "graded-gate.py")
open(graded, "w").write(subprocess.run(["git", "-C", repo, "show", "%s:%s" % (rev, c1.SUBJECT)],
                                       capture_output=True, text=True).stdout)
name = os.path.basename(c1.BASE_RECEIPT)
for kind, cmd, want in EXTRA:
    d, fx = c1.clone_fixture(repo, rev, scratch, kind, c1.BASE_RECEIPT)
    if d is None:
        print("E2E %s build-failed %s" % (kind, fx))
        continue
    rc, out = c1.run_graded(graded, d, fx, scratch, "fx-" + kind)
    line = c1.receipt_line(out, name)
    got = (line.group(2) + " problems=" + line.group(3)) if line else "no-receipt-line"
    print("E2E %s want=%s gate=%s verdict=%s | %s" % (kind, want, got, c1.verdict_line(out)[:60], cmd))
    subprocess.run(["rm", "-rf", d])

# C2: syntax-error kill probe on the r88 count-c1.py at rev — does an uncompilable mutant count?
src = subprocess.run(["git", "-C", repo, "show", "%s:%s" % (rev, c2.C1)], capture_output=True, text=True).stdout
anchor = [m for m in c2.MUTANTS if m[1] == "C1-arms-first"][0]
syn = ((c2.C1, "SYN-arms", anchor[2], anchor[3], anchor[3] + " (("),)
met, tail, lines, extras = c2.grade(lambda p: src, os.path.join(scratch), mutants=syn,
                                    arms_by_file={"count-c1.py": 28})
print("C2SYN", tail, lines, extras)
print("C2SYN killed=%s" % (" killed " in " ".join(lines)))
