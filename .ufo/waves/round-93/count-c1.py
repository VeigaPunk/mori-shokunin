#!/usr/bin/env python3
"""mori round-93 C1 counter (calibration): the round-92 lesson's self-description is true of the
repo it describes.

Frozen predicate P-C1 (`.ufo/waves/round-93/contract.md` section C1; this docstring, the contract
and the receipt label are the same sentence):

  At revision R `python3 -I .ufo/waves/round-93/count-c1.py R --repo <clone>` prints
  `C1=met trio=98 claim_r92_true=1 files=19 adm_ok=19 adm_fail=0 patched12=12 census=ok rev=<12>`
  and exits 0, where:

  * `trio` = knowledge entries whose first 12 lines carry `source:`, `verified-at:`, `recheck:`
    (>= 98; the round-92 C1 presence rule, QUALITY 194);
  * `claim_r92_true=1` is the round-92 lesson's claim "each verified-at names the admission
    commit of its file", evaluated at R: it holds iff `adm_fail == 0`;
  * for each of the 19 round-92 trio files, the `verified-at:` line at R contains the file's
    admission commit (short hash, >= 7 chars), derived live as
    `git log --diff-filter=A --format=%h <ENTERING> -- <file> | tail -1` (`adm_ok=19`);
  * for each of the 12 entering mismatch files, `git diff -U0 ENTERING R -- <file>` changes
    exactly one `verified-at:` line (`patched12=12`) and nothing else in that file;
  * for each of the other 7 files, the file is byte-identical between ENTERING and R;
  * `sources-census.sh validate --file` on R's corpus/SOURCES.md exits 0.

  Otherwise `C1=unmet ...` with `checks_failed=`; exit 1; exit 2 setup. `--report` prints raw
  values without judgement. Reads git objects only; writes only under TMPDIR-honouring temporary
  directories; no /tmp literal.
"""
import argparse
import os
import re
import subprocess
import sys
import tarfile
import tempfile

ENTERING = "7b3fe9d540c98b8b0390a0f9bbe78de4341092a5"
KNOW = "corpus/knowledge"
SOURCES = "corpus/SOURCES.md"
CENSUS = "/home/vgpnk/Projects/shokunin/scripts/sources-census.sh"
KEYS = ("source:", "verified-at:", "recheck:")
NINETEEN = [
    "audit-r11.md", "counter-semantics-r78.md", "counter-win-r77.md", "drift-pin-r10.md",
    "execution-binding-r89.md", "kernel-v7.3-recheck-r53.md", "lane-silence-r2.md",
    "progressing-weak-r2.md", "rotation-receipt-grammar-r76.md", "rotation-schedule-r74.md",
    "rotation-series-r75.md", "selftest-flake-r9.md", "silence-cutover-r3.md",
    "silence-grading-r2.md", "surfaces-r8.md", "verdict-machine-r4.md", "verdict-machine-r5.md",
    "verdict-machine-r6.md", "workstate-win-r71.md",
]
TWELVE = [
    "counter-semantics-r78.md", "counter-win-r77.md", "drift-pin-r10.md",
    "execution-binding-r89.md", "kernel-v7.3-recheck-r53.md", "lane-silence-r2.md",
    "rotation-receipt-grammar-r76.md", "rotation-schedule-r74.md", "rotation-series-r75.md",
    "selftest-flake-r9.md", "surfaces-r8.md", "workstate-win-r71.md",
]
SEVEN = [f for f in NINETEEN if f not in TWELVE]


def git(repo, *args):
    return subprocess.run(["git", "-C", repo, *args], capture_output=True)


def extract(repo, rev, dest):
    proc = subprocess.Popen(["git", "-C", repo, "archive", rev], stdout=subprocess.PIPE)
    with tarfile.open(fileobj=proc.stdout, mode="r|") as tf:
        tf.extractall(dest)
    return proc.wait() == 0


def head_lines(path, n=12):
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        return fh.read(65536).splitlines()[:n]


def trio_count(root):
    n = 0
    kd = os.path.join(root, KNOW)
    for dirpath, _dn, filenames in os.walk(kd):
        for fn in filenames:
            if fn.endswith(".md") and all(
                    any(ln.startswith(k) for ln in head_lines(os.path.join(dirpath, fn)))
                    for k in KEYS):
                n += 1
    return n


def admission_commit(repo, rel):
    r = git(repo, "log", "--diff-filter=A", "--format=%h", ENTERING, "--", rel)
    lines = [ln for ln in r.stdout.decode().split() if ln]
    return lines[-1] if lines else None


def verified_at(path):
    for ln in head_lines(path):
        if ln.startswith("verified-at:"):
            return ln
    return None


def one_verified_at_change(repo, rev, rel):
    r = git(repo, "diff", "-U0", "--no-color", ENTERING, rev, "--", rel)
    if r.returncode != 0:
        return False
    removed, added = [], []
    for ln in r.stdout.decode("utf-8", errors="replace").splitlines():
        if ln.startswith(("---", "+++", "@@", "diff ")):
            continue
        if ln.startswith("-"):
            removed.append(ln[1:])
        elif ln.startswith("+"):
            added.append(ln[1:])
    return (len(removed) == 1 and len(added) == 1 and removed[0].startswith("verified-at:")
            and added[0].startswith("verified-at:"))


def unchanged(repo, rev, rel):
    r = git(repo, "diff", "--quiet", ENTERING, rev, "--", rel)
    return r.returncode == 0


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("rev")
    ap.add_argument("--repo", required=True)
    ap.add_argument("--report", action="store_true")
    args = ap.parse_args(argv)
    rv = git(args.repo, "rev-parse", "--verify", "-q", args.rev + "^{commit}")
    if rv.returncode != 0:
        print("C1_SETUP revision unresolvable: %s" % args.rev)
        return 2
    rev = rv.stdout.decode().strip()
    with tempfile.TemporaryDirectory(dir=os.environ.get("TMPDIR")) as d:
        if not extract(args.repo, rev, d):
            print("C1_SETUP cannot extract tree at %s" % rev[:12])
            return 2
        trio = trio_count(d)
        adm_ok, adm_fail, details = 0, 0, []
        for rel in NINETEEN:
            kpath = os.path.join(KNOW, rel)
            ac = admission_commit(args.repo, kpath)
            va = verified_at(os.path.join(d, kpath)) if os.path.exists(os.path.join(d, kpath)) else None
            if ac and va and ac[:7] in va:
                adm_ok += 1
            else:
                adm_fail += 1
                details.append("%s ac=%s va=%s" % (rel, ac, (va or "-")[:60]))
        patched = sum(1 for rel in TWELVE
                      if one_verified_at_change(args.repo, rev, os.path.join(KNOW, rel)))
        seven_same = sum(1 for rel in SEVEN
                         if unchanged(args.repo, rev, os.path.join(KNOW, rel)))
        cs = subprocess.run(["bash", CENSUS, "validate", "--file", os.path.join(d, SOURCES)],
                            capture_output=True, text=True)
        census_ok = cs.returncode == 0
        claim_true = 1 if adm_fail == 0 else 0
        if args.report:
            print("C1_REPORT rev=%s trio=%d claim_r92_true=%d files=%d adm_ok=%d adm_fail=%d "
                  "patched12=%d/12 seven_same=%d/7 census_rc=%d failures=%s"
                  % (rev[:12], trio, claim_true, len(NINETEEN), adm_ok, adm_fail, patched,
                     seven_same, cs.returncode, "; ".join(details) if details else "-"))
            return 0
        fails = []
        if trio < 98:
            fails.append("trio")
        if adm_fail != 0 or adm_ok != len(NINETEEN):
            fails.append("admission")
        if patched != len(TWELVE):
            fails.append("patched12")
        if seven_same != len(SEVEN):
            fails.append("seven_same")
        if not census_ok:
            fails.append("census")
        met = not fails
        print("C1=%s trio=%d claim_r92_true=%d files=%d adm_ok=%d adm_fail=%d patched12=%d "
              "seven_same=%d census=%s%s rev=%s"
              % ("met" if met else "unmet", trio, claim_true, len(NINETEEN), adm_ok, adm_fail,
                 patched, seven_same, "ok" if census_ok else "rc%d" % cs.returncode,
                 (" checks_failed=" + ",".join(fails)) if fails else "", rev[:12]))
        return 0 if met else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
