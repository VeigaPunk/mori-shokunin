#!/usr/bin/env python3
"""Held-out binding probe: load the r87 gate's binding_problems at <rev> (like noharm-c1) and grade
cases the Mo89R01C1 battery does not contain. Usage: probe.py <repo> <rev> [<rev>...]"""
import importlib.util, json, os, subprocess, sys, tempfile
sys.dont_write_bytecode = True
GATE = ".ufo/waves/round-87/count-c2.py"
B = "tools/mori-record-sweep.py"
P = "--root . --pins .ufo/waves/round-82/record-pins.json"
BODY = "RECORD_SWEEP pending=0 pinned=0 carriers=1 bindings=3 revisions=0"
CASES = [
    # (name, expect, cmd, class)  class: claim = script not executed; prov = executed but body not its output
    ("H01-or-short-circuit", "reject", "true || python3 -I %s %s; printf '%%s\\n' '%s'" % (B, P, BODY), "claim"),
    ("H02-false-and", "reject", "false && python3 -I %s %s; printf '%%s\\n' '%s'" % (B, P, BODY), "claim"),
    ("H03-exit-before", "reject", "printf '%%s\\n' '%s'; exit 0; python3 -I %s %s" % (BODY, B, P), "claim"),
    ("H04-if-false", "reject", "if false; then python3 -I %s %s; fi; printf '%%s\\n' '%s'" % (B, P, BODY), "claim"),
    ("H05-echo-as-data", "reject", "echo python3 -I %s" % B, "claim"),
    ("H06-colon-noop", "reject", ": python3 -I %s %s; printf '%%s\\n' '%s'" % (B, P, BODY), "claim"),
    ("H07-bash-c-echo", "reject", "bash -c 'echo python3 -I %s'" % B, "claim"),
    ("H08-function-def-never-called", "reject", "f() { python3 -I %s %s; }; printf '%%s\\n' '%s'" % (B, P, BODY), "claim"),
    ("H09-heredoc-or-subshell-false", "reject", "(exit 1) && python3 -I %s %s; printf '%%s\\n' '%s'" % (B, P, BODY), "claim"),
    ("H10-dev-null-then-printf", "reject", "python3 -I %s %s >/dev/null; printf '%%s\\n' '%s'" % (B, P, BODY), "prov"),
    ("H11-dotslash-comment", "reject", "printf '%%s\\n' '%s' # ./%s" % (BODY, B), "claim"),
    ("H12-dotslash-selfprint", "reject", "python3 -c \"print('%s')\" ./%s" % (BODY, B), "claim"),
    ("H13-echo-dotslash", "reject", "echo ./%s" % B, "claim"),
    ("M01-env-usr-bin", "met", "/usr/bin/env python3 -I %s %s" % (B, P), "claim"),
    ("M02-timeout", "met", "timeout 600 python3 -I %s %s" % (B, P), "claim"),
    ("M03-command-builtin", "met", "command python3 -I %s %s" % (B, P), "claim"),
    ("M04-O-flag", "met", "python3 -O %s %s" % (B, P), "claim"),
    ("M05-IB-combined", "met", "python3 -IB %s %s" % (B, P), "claim"),
    ("M06-env-i", "met", "env -i PATH=/usr/bin python3 -I %s %s" % (B, P), "claim"),
    ("M07-cd-subshell", "met", "(cd . && python3 -I %s %s)" % (B, P), "claim"),
    ("M08-pipe-tail", "met", "python3 -I %s %s | cat" % (B, P), "claim"),
    ("M09-stderr-redirect", "met", "python3 -I %s %s 2>&1" % (B, P), "claim"),
    ("M10-Wignore-glued", "met", "python3 -Wignore %s %s" % (B, P), "claim"),
]


def gate_at(repo, rev, work):
    out = subprocess.run(["git", "-C", repo, "show", "%s:%s" % (rev, GATE)], capture_output=True, text=True)
    path = os.path.join(work, "g_%s.py" % rev[:12])
    open(path, "w").write(out.stdout)
    spec = importlib.util.spec_from_file_location("g_%s" % rev[:12], path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def bound(g, cmd, repo):
    try:
        return g.binding_problems(cmd, [("0" * 64, B)], True, repo) == []
    except TypeError:
        return g.binding_problems(cmd, [("0" * 64, B)], True) == []


def main():
    repo, revs = sys.argv[1], sys.argv[2:]
    with tempfile.TemporaryDirectory() as w:
        gates = [(r, gate_at(repo, r, w)) for r in revs]
        tally = {r: {"open": 0, "harm": 0} for r in revs}
        for name, exp, cmd, cls in CASES:
            row = []
            for r, g in gates:
                b = bound(g, cmd, repo)
                bad = (exp == "reject" and b) or (exp == "met" and not b)
                if bad:
                    tally[r]["open" if exp == "reject" else "harm"] += 1
                row.append("%s=%s%s" % (r[:8], "bound" if b else "refused", "!" if bad else ""))
            print("HCASE %s expect=%s class=%s %s | %s" % (name, exp, cls, " ".join(row), cmd))
        for r in revs:
            print("HELDOUT rev=%s open=%d harm=%d cases=%d" % (r[:12], tally[r]["open"], tally[r]["harm"], len(CASES)))


main()
