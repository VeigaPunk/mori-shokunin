#!/usr/bin/env python3
"""Round 56 C2 counter (operability, capability acquisition) — the dual-shape
seat-output vote binder is landed, runs, and re-binds the round-55 vote arm.

Frozen predicate P-C2 (same sentence in contract.md, this counter and the
receipt label):
  At revision R, tools/mori-vote-bind.py exists with sha256 equal to PIN;
  executed at R it prints `VOTE_BIND_SELFTEST pass=16 fail=0` and exits 0;
  executed as `tally --ledger <ledger> --results <results> --verb RECHECK
  --voter Mo55Rc01 .. Mo55Rc16` over the committed round-55 artifacts
  (corpus/knowledge/kernel-v7.3-recheck-r55.md and
  .ufo/waves/round-55/w1-results.json) at R it prints exactly the line
  `TALLY rows=78 agree=78 double=68 single=10 zero=0 dissent=0 voters=16
  bound_voters=15`; a do-nothing control results file whose every output is
  junk (no vote surface) tallies zero=78; the frozen round-55 C1 counter
  executed at R over the same committed artifacts still prints `voted=0`
  (contrast: the binding shape is the whole difference); and
  corpus/knowledge/vote-binding-r56.md exists at R naming S545 and
  tools/mori-vote-bind.py, with corpus/SOURCES.md at R carrying row S545
  (status mined, opened 2026-10-27, used-by naming the entry).

Usage: count-c2.py <rev> [--repo DIR]   |   count-c2.py --selftest
Output: `C2=met|unmet selftest=ok|bad tally=ok|bad control=ok|bad contrast=voted0|bad entry=ok|bad row=ok|bad rev=R`
  (+ `failed=` list when unmet).  Exit 0 met, 1 unmet, 2 setup.
Read-only over the measured repo (git show / rev-parse); the executed arms
materialize the tools under the caller's TMPDIR (python3 subprocess, no
network).
"""
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile

TOOL = "tools/mori-vote-bind.py"
ENTRY = "corpus/knowledge/vote-binding-r56.md"
LEDGER = "corpus/knowledge/kernel-v7.3-recheck-r55.md"
RESULTS = ".ufo/waves/round-55/w1-results.json"
R55_C1 = ".ufo/waves/round-55/count-c1.py"
VOTERS = ["Mo55Rc%02d" % i for i in range(1, 17)]
EXPECT_SELFTEST = "VOTE_BIND_SELFTEST pass=16 fail=0"
EXPECT_TALLY = ("TALLY rows=78 agree=78 double=68 single=10 zero=0 dissent=0 "
                "voters=16 bound_voters=15")
PIN = "8be1acdbb36cd68deba005e21a4a8679534ab5a5099a787aa9335d288dfa6bca"  # frozen at data commit c419fe6d


def git_show(repo, rev, path):
    p = subprocess.run(["git", "-C", repo, "show", "%s:%s" % (rev, path)],
                       capture_output=True, text=True)
    if p.returncode != 0:
        return None
    return p.stdout


def sha(text):
    return hashlib.sha256(text.encode("utf-8", "surrogateescape")).hexdigest()


def run_in(cwd, args):
    return subprocess.run([sys.executable] + args, capture_output=True, text=True, cwd=cwd)


def evaluate(repo, rev):
    failed = []
    tool_src = git_show(repo, rev, TOOL)
    if tool_src is None:
        return ["tool_absent"]
    if PIN and sha(tool_src) != PIN:
        failed.append("pins")
    ledger = git_show(repo, rev, LEDGER)
    results = git_show(repo, rev, RESULTS)
    if ledger is None or results is None:
        failed.append("r55_artifacts_absent")
        return failed
    cwd = tempfile.mkdtemp(prefix="mori-r56-c2-", dir=os.environ.get("TMPDIR") or None)
    tdir = os.path.join(cwd, "tool")
    os.makedirs(tdir, exist_ok=True)
    tpath = os.path.join(tdir, "mori-vote-bind.py")
    with open(tpath, "w", encoding="utf-8") as f:
        f.write(tool_src)
    lp = os.path.join(cwd, "ledger.md")
    with open(lp, "w", encoding="utf-8") as f:
        f.write(ledger)
    rp = os.path.join(cwd, "results.json")
    with open(rp, "w", encoding="utf-8") as f:
        f.write(results)
    p = run_in(cwd, [tpath, "--selftest"])
    if p.returncode != 0 or EXPECT_SELFTEST not in p.stdout:
        failed.append("selftest")
    args = [tpath, "tally", "--ledger", lp, "--results", rp, "--verb", "RECHECK"]
    for v in VOTERS:
        args += ["--voter", v]
    p = run_in(cwd, args)
    if p.returncode != 0 or EXPECT_TALLY not in p.stdout:
        failed.append("tally")
    # do-nothing control: junk outputs -> no binds
    junk = {"results": [{"name": v, "output": "no votes here, just prose"}
                        for v in VOTERS]}
    jp = os.path.join(cwd, "junk.json")
    with open(jp, "w", encoding="utf-8") as f:
        json.dump(junk, f)
    args = [tpath, "tally", "--ledger", lp, "--results", jp, "--verb", "RECHECK"]
    for v in VOTERS:
        args += ["--voter", v]
    p = run_in(cwd, args)
    if p.returncode != 0 or "zero=78" not in p.stdout or "double=0" not in p.stdout:
        failed.append("control")
    # contrast: the frozen r55 C1 counter still reads voted=0 at R
    r55 = git_show(repo, rev, R55_C1)
    if r55 is None:
        failed.append("contrast_absent")
    else:
        cpath = os.path.join(cwd, "r55-count-c1.py")
        with open(cpath, "w", encoding="utf-8") as f:
            f.write(r55)
        p = run_in(cwd, [cpath, rev, "--repo", repo])
        if p.returncode not in (0, 1) or "voted=0" not in p.stdout:
            failed.append("contrast")
    entry = git_show(repo, rev, ENTRY)
    if entry is None or "S545" not in entry or "mori-vote-bind.py" not in entry:
        failed.append("entry")
    reg = git_show(repo, rev, "corpus/SOURCES.md") or ""
    row = None
    for line in reg.split("\n"):
        if re.match(r"^ {0,3}\|\s*S545\s*\|", line):
            row = line
            break
    if (row is None or "mined" not in row or "2026-10-27" not in row
            or ENTRY not in row):
        failed.append("row")
    return failed


def main():
    if "--selftest" in sys.argv:
        ok = len(VOTERS) == 16 and EXPECT_TALLY.startswith("TALLY rows=78")
        print("C2_COUNTER_SELFTEST pass=%d fail=%d" % (1 if ok else 0, 0 if ok else 1))
        return 0 if ok else 1
    if len(sys.argv) < 2:
        print("usage: count-c2.py <rev> [--repo DIR]", file=sys.stderr)
        return 2
    rev = sys.argv[1]
    repo = "/home/vgpnk/Projects/shokunin/mori-shokunin"
    if "--repo" in sys.argv:
        repo = sys.argv[sys.argv.index("--repo") + 1]
    p = subprocess.run(["git", "-C", repo, "rev-parse", "--verify", rev],
                       capture_output=True, text=True)
    if p.returncode != 0:
        print("C2_SETUP: unresolvable revision %s" % rev, file=sys.stderr)
        return 2
    full = p.stdout.strip()
    failed = evaluate(repo, full)
    ok = not failed
    print("C2=%s selftest=%s tally=%s control=%s contrast=%s entry=%s row=%s rev=%s%s" % (
        "met" if ok else "unmet",
        "bad" if ("selftest" in failed or "pins" in failed) else "ok",
        "bad" if "tally" in failed else "ok",
        "bad" if "control" in failed else "ok",
        "voted0" if "contrast" not in failed else "bad",
        "bad" if "entry" in failed else "ok",
        "bad" if "row" in failed else "ok",
        full,
        "" if ok else " failed=" + ",".join(failed)))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
