#!/usr/bin/env python3
"""controls-r99.py -- pre-freeze controls for mori round 99 (C1, C2), run through the counters'
public CLI. usage: controls-r99.py --lane LANE --entering REV --scratch DIR > evidence/controls-r99.txt

C1 trees are built under --scratch from `git archive <entering>` plus overlays:
  K0  do-nothing: the entering tree                                       -> unmet
  K1  constant printer stub in place of the tool                          -> unmet
  K2  lookup forgery: answers the candidate self-test journals by sha,
      otherwise runs the entering tool                                    -> unmet
  K3..K9 candidate tool with one round-99 fix removed (comment, sudo
      quoting, continuation, fail-closed, -r pattern, exit event, clamp)   -> unmet
  K10 positive tree minus the knowledge entry                             -> unmet
  K11 positive tree with the S633-S636 rows not mined                     -> unmet
  P1  positive: candidate tool + working-tree SKILL.md, SOURCES.md, knowledge -> met
C2 fixtures are `git clone --shared` copies of the lane under --scratch with one fixture commit each
(identity set only inside the fixture repo; `rev-parse --show-toplevel` checked first):
  K0c do-nothing (entering)  K1c pointers only  K2c wrong round for coverage  K3c wrong line
  K4c Score cell edited      -> unmet;  P1c candidate transform -> met
Every control prints `control <id> expect=<met|unmet> got=<label> rc=<n> AS_EXPECTED|UNEXPECTED`,
then `CONTROLS_DONE unexpected=<n>`.
"""
import argparse
import hashlib
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
C1 = os.path.join(HERE, "count-c1.py")
C2 = os.path.join(HERE, "count-c2.py")
CAND_TOOL = os.path.join(HERE, "candidate", "tools", "mori-userns-runway.py")
APPLY_C2 = os.path.join(HERE, "candidate", "apply-c2.py")
TOOL = "tools/mori-userns-runway.py"

STUB_CONST = '''import sys
if "--selftest" in sys.argv:
    print("MORI_USERNS_RUNWAY_SELFTEST: PASS (19 cases)"); sys.exit(0)
if "--journal" in sys.argv:
    print("SYSCTL_WRITES n=1 keys=1 userns_zero=1"); sys.exit(1)
print("USERNS_RUNWAY limit=122865 used_lb=6 pids=1 unreadable=0 runway=122859 low=32 state=ok"); sys.exit(0)
'''

STUB_LOOKUP = '''import hashlib, os, subprocess, sys
TABLE = %r
HERE = os.path.dirname(os.path.abspath(__file__))
if "--journal" in sys.argv:
    p = sys.argv[sys.argv.index("--journal") + 1]
    h = hashlib.sha256(open(p, "rb").read()).hexdigest()
    if h in TABLE:
        print(TABLE[h][0]); sys.exit(TABLE[h][1])
sys.exit(subprocess.run([sys.executable, os.path.join(HERE, "mori-userns-runway-entering.py")] + sys.argv[1:]).returncode)
'''

MUTANTS = {
    "K3-no-comment": ('        if c == "#" and not in_word:', '        if False:'),
    "K4-no-sudo-unquote": ('            if c == "\\\\" and i + 1 < n and cmd[i + 1] in "\'\\\\":', '            if False:'),
    "K5-no-continuation": ('        cont = " : (command continued) " in line', '        cont = False'),
    "K6-fail-open": ('        return lines, 2\n', '        return lines, (1 if events else 0)\n'),
    "K7-no-pattern-skip": ('        if a in ("-r", "--pattern"):', '        if False:'),
    "K8-no-exit-skip": ('        if EXIT_SUFFIX_RE.search(cmd):', '        if False:'),
    "K9-no-clamp": ('    runway = max(limit - used, 0)', '    runway = limit - used'),
}


def sh(argv, **kw):
    return subprocess.run(argv, capture_output=True, text=True, **kw)


def tree(scratch, name, lane, rev):
    d = os.path.join(scratch, name)
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(d)
    a = subprocess.run(["git", "-C", lane, "archive", rev], capture_output=True, check=True)
    subprocess.run(["tar", "-x", "-C", d], input=a.stdout, check=True)
    ev = os.path.join(d, ".ufo", "waves", "round-99", "evidence")
    os.makedirs(ev, exist_ok=True)
    shutil.copy(os.path.join(HERE, "evidence", "journal-incident-r99.txt"), ev)
    return d


def positive(scratch, name, lane, rev):
    d = tree(scratch, name, lane, rev)
    shutil.copy(CAND_TOOL, os.path.join(d, TOOL))
    for rel in ("SKILL.md", "corpus/SOURCES.md", "corpus/knowledge/sudo-log-grammar-r99.md"):
        shutil.copy(os.path.join(lane, rel), os.path.join(d, rel))
    return d


def label(out):
    last = (out.strip().splitlines() or [""])[-1]
    return last.split()[0] if last else "-", last


def report(cid, expect, out, rc, unexpected):
    lab, last = label(out)
    got = lab.split("=", 1)[1] if "=" in lab else lab
    ok = got == expect
    if not ok:
        unexpected.append(cid)
    print("control %s expect=%s got=%s rc=%d %s :: %s" % (cid, expect, got, rc, "AS_EXPECTED" if ok else "UNEXPECTED", last))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--entering", required=True)
    ap.add_argument("--scratch", required=True)
    ap.add_argument("--seed", type=int, default=990099)
    a = ap.parse_args()
    os.makedirs(a.scratch, exist_ok=True)
    shas = {p: hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]
            for p in (C1, C2, CAND_TOOL, APPLY_C2, os.path.abspath(__file__),
                      os.path.join(a.lane, "SKILL.md"), os.path.join(a.lane, "corpus", "SOURCES.md"),
                      os.path.join(a.lane, "corpus", "knowledge", "sudo-log-grammar-r99.md"))}
    print("CONTROLS r99 entering=%s seed=%d %s" % (a.entering, a.seed,
          " ".join("%s=%s" % (os.path.relpath(p, a.lane), h) for p, h in shas.items())))
    unexpected = []

    def c1(cid, d, expect):
        p = sh([sys.executable, C1, "--root", d, "--seed", str(a.seed), "--work", a.scratch])
        report(cid, expect, p.stdout, p.returncode, unexpected)

    c1("K0-do-nothing", tree(a.scratch, "k0", a.lane, a.entering), "unmet")
    d = positive(a.scratch, "k1", a.lane, a.entering)
    open(os.path.join(d, TOOL), "w").write(STUB_CONST)
    c1("K1-constant-stub", d, "unmet")
    # K2: lookup table of the candidate's own self-test journal fixtures, answered by sha
    import importlib.util
    spec = importlib.util.spec_from_file_location("cand", CAND_TOOL)
    cand = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cand)
    src = open(CAND_TOOL).read()
    table = {}
    import re as _re
    # rebuild the fixtures exactly as the self-test does, by executing its literal assignments
    ns = {}
    for m in _re.finditer(r"\n        (J\d*) = (\(.*?\)|\".*?\")\n", src, _re.S):
        exec("%s = %s" % (m.group(1), m.group(2)), ns)
    for k, v in ns.items():
        if k.startswith("J") and isinstance(v, str):
            for body in (v, v if v.endswith("\n") else v + "\n"):
                lines, rc = cand.journal_report(*cand.scan_journal(body.splitlines()))
                table[hashlib.sha256(body.encode()).hexdigest()] = ("\n".join(lines), rc)
    d = positive(a.scratch, "k2", a.lane, a.entering)
    shutil.copy(os.path.join(tree(a.scratch, "k2e", a.lane, a.entering), TOOL),
                os.path.join(d, "tools", "mori-userns-runway-entering.py"))
    open(os.path.join(d, TOOL), "w").write(STUB_LOOKUP % table)
    print("K2 lookup table entries=%d" % len(table))
    c1("K2-lookup-forgery", d, "unmet")
    for cid, (old, new) in MUTANTS.items():
        d = positive(a.scratch, cid.lower(), a.lane, a.entering)
        s = open(os.path.join(d, TOOL)).read()
        if s.count(old) != 1:
            print("control %s SETUP mutation anchor count=%d UNEXPECTED" % (cid, s.count(old)))
            unexpected.append(cid)
            continue
        open(os.path.join(d, TOOL), "w").write(s.replace(old, new))
        c1(cid, d, "unmet")
    d = positive(a.scratch, "k10", a.lane, a.entering)
    os.remove(os.path.join(d, "corpus/knowledge/sudo-log-grammar-r99.md"))
    c1("K10-no-knowledge", d, "unmet")
    d = positive(a.scratch, "k11", a.lane, a.entering)
    p = os.path.join(d, "corpus/SOURCES.md")
    s = open(p).read()
    for sid in ("S633", "S634", "S635", "S636"):
        s = _re.sub(r"(\| %s \|(?:[^|\n]*\|){6}) mined \|" % sid, r"\1 proposed |", s)
    open(p, "w").write(s)
    c1("K11-rows-not-mined", d, "unmet")
    c1("P1-positive", positive(a.scratch, "p1", a.lane, a.entering), "met")

    # ---- C2 fixtures
    def fixture(cid, edit):
        d = os.path.join(a.scratch, "c2-" + cid)
        shutil.rmtree(d, ignore_errors=True)
        sh(["git", "clone", "-q", "--shared", "--no-checkout", a.lane, d], check=True)
        top = sh(["git", "-C", d, "rev-parse", "--show-toplevel"]).stdout.strip()
        if os.path.realpath(top) != os.path.realpath(d):
            raise SystemExit("fixture toplevel mismatch: %s" % top)
        sh(["git", "-C", d, "checkout", "-q", "--detach", a.entering], check=True)
        if edit is None:
            return d, a.entering
        sc = os.path.join(d, "SCORECARD.md")
        edit(sc)
        sh(["git", "-C", d, "-c", "user.name=fixture", "-c", "user.email=fixture@invalid", "commit", "-q",
            "-am", "fixture " + cid], check=True)
        return d, sh(["git", "-C", d, "rev-parse", "HEAD"]).stdout.strip()

    def apply_full(sc):
        sh([sys.executable, APPLY_C2, sc], check=True)

    def pointers_only(sc):
        apply_full(sc)
        s = open(sc).read().replace("round 98 (improved, score held); ", "")
        open(sc, "w").write(s)

    def wrong_round(sc):
        apply_full(sc)
        s = open(sc).read().replace("`corpus/lessons/round-98-verifier-spotcheck.md:89` (round 98",
                                    "`corpus/lessons/round-97-verifier-spotcheck.md:78` (round 97", 1)
        open(sc, "w").write(s)

    def wrong_line(sc):
        apply_full(sc)
        s = open(sc).read().replace("round-86-verifier-spotcheck.md:145`", "round-86-verifier-spotcheck.md:1`", 1)
        open(sc, "w").write(s)

    def score_edit(sc):
        apply_full(sc)
        s = open(sc).read().replace("| depth | 5 |", "| depth | 6 |", 1)
        open(sc, "w").write(s)

    for cid, edit, expect in (("K0c-do-nothing", None, "unmet"), ("K1c-pointers-only", pointers_only, "unmet"),
                              ("K2c-wrong-round", wrong_round, "unmet"), ("K3c-wrong-line", wrong_line, "unmet"),
                              ("K4c-score-edit", score_edit, "unmet"), ("P1c-positive", apply_full, "met")):
        d, rev = fixture(cid, edit)
        p = sh([sys.executable, C2, rev, "--repo", d])
        report(cid, expect, p.stdout, p.returncode, unexpected)
        shutil.rmtree(d, ignore_errors=True)
    print("CONTROLS_DONE unexpected=%d%s" % (len(unexpected), (" " + ",".join(unexpected)) if unexpected else ""))
    return 0 if not unexpected else 1


if __name__ == "__main__":
    sys.exit(main())
