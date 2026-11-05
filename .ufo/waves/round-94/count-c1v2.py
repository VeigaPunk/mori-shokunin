#!/usr/bin/env python3
"""mori round-94 C1 counter v2 (calibration): the round-92 lesson's self-description is true of the
repo it describes, with the admission test bound to a whole token (routed defect R02 of round 93).

Frozen predicate P-C1v2 (`.ufo/waves/round-94/contract.md` section C1; this docstring, the contract
and the receipt label are the same sentence):

  At revision R `python3 -I .ufo/waves/round-94/count-c1v2.py R --repo <clone> [--census PATH]`
  prints `C1=met trio=N files=19 adm_ok=19 adm_fail=0 patched12=12 seven_same=7 census=ok rev=<12>`
  and exits 0, where:

  * `trio` = knowledge entries whose first 12 lines carry `source:`, `verified-at:`, `recheck:` (>= 98);
  * for each of the 19 round-92 trio files, the first whitespace token of the file's `verified-at:`
    value is at least 7 characters and is a prefix of the file's admission commit short hash
    (`git log --diff-filter=A --format=%h <ENTERING> -- <file> | tail -1`), i.e. the token IS the
    admission hash, never a substring of a longer token (`adm_ok=19`);
  * each of the 12 entering-mismatch files changes exactly one `verified-at:` line between ENTERING
    and R, and each of the other 7 is byte-identical (`patched12=12 seven_same=7`);
  * `sources-census.sh validate --file` exits 0 on R's corpus/SOURCES.md.

  The census script is `--census PATH` when given, else `$SHOKUNIN_ROOT/scripts/sources-census.sh`;
  when neither is set the counter exits 2 (`C1_SETUP`) and never falls back to a host path.
  Otherwise `C1=unmet ... checks_failed=<list>`; exit 1. `--report` prints raw values.
  Reads git objects only; writes only under TMPDIR-honouring temporary directories.
"""
import argparse
import os
import subprocess
import sys
import tarfile
import tempfile

ENTERING = "7b3fe9d540c98b8b0390a0f9bbe78de4341092a5"
KNOW = "corpus/knowledge"
SOURCES = "corpus/SOURCES.md"
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


def admission_token_ok(va, ac):
    """The first whitespace token of the verified-at value is >= 7 characters and a prefix of ac."""
    if not va or not ac:
        return False
    value = va.split(":", 1)[1].split()
    if not value:
        return False
    tok = value[0]
    return len(tok) >= 7 and ac.startswith(tok)


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
    return git(repo, "diff", "--quiet", ENTERING, rev, "--", rel).returncode == 0


def census_path(explicit):
    if explicit:
        return explicit
    root = os.environ.get("SHOKUNIN_ROOT")
    if root:
        return os.path.join(root, "scripts", "sources-census.sh")
    return None


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("rev")
    ap.add_argument("--repo", required=True)
    ap.add_argument("--census", default=None)
    ap.add_argument("--report", action="store_true")
    args = ap.parse_args(argv)
    census = census_path(args.census)
    if census is None:
        print("C1_SETUP census path unset: give --census or set SHOKUNIN_ROOT")
        return 2
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
            full = os.path.join(d, kpath)
            va = verified_at(full) if os.path.exists(full) else None
            if admission_token_ok(va, ac):
                adm_ok += 1
            else:
                adm_fail += 1
                details.append("%s ac=%s va=%s" % (rel, ac, (va or "-")[:60]))
        patched = sum(1 for rel in TWELVE
                      if one_verified_at_change(args.repo, rev, os.path.join(KNOW, rel)))
        seven_same = sum(1 for rel in SEVEN
                         if unchanged(args.repo, rev, os.path.join(KNOW, rel)))
        cs = subprocess.run(["bash", census, "validate", "--file", os.path.join(d, SOURCES)],
                            capture_output=True, text=True)
        census_ok = cs.returncode == 0
        if args.report:
            print("C1_REPORT rev=%s trio=%d files=%d adm_ok=%d adm_fail=%d patched12=%d/12 "
                  "seven_same=%d/7 census_rc=%d failures=%s"
                  % (rev[:12], trio, len(NINETEEN), adm_ok, adm_fail, patched, seven_same,
                     cs.returncode, "; ".join(details) if details else "-"))
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
        print("C1=%s trio=%d files=%d adm_ok=%d adm_fail=%d patched12=%d seven_same=%d census=%s%s rev=%s"
              % ("met" if met else "unmet", trio, len(NINETEEN), adm_ok, adm_fail, patched,
                 seven_same, "ok" if census_ok else "rc%d" % cs.returncode,
                 (" checks_failed=" + ",".join(fails)) if fails else "", rev[:12]))
        return 0 if met else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
