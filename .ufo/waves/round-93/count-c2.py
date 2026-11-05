#!/usr/bin/env python3
"""mori round-93 C2 counter (operability): no tool under tools/ hardcodes a host home path.

Frozen predicate P-C2 (`.ufo/waves/round-93/contract.md` section C2; this docstring, the contract
and the receipt label are the same sentence):

  At revision R `python3 -I .ufo/waves/round-93/count-c2.py R --repo <clone>` prints
  `C2=met home_literals=0 vgpnk_refs=0 tools=3 selftests=3/3 census=ok rev=<12>` and exits 0,
  where, over the extracted tree at R:
  * `home_literals` counts occurrences of the regex `/home/[a-z_][a-z0-9_-]*/` in every file
    under tools/ (any absolute home-directory path, whichever user name it names);
  * `vgpnk_refs` counts occurrences of the byte sequence `vgpnk` in every file under tools/;
  * the three named tools exist at R (`tools=3`);
  * each tool's declared self-test mode exits 0 at R (`selftests=3/3`);
  * R's corpus/SOURCES.md passes `sources-census.sh validate --file` (no drive-by registry edits).
  Otherwise `C2=unmet ...` with `checks_failed=`; exit 1; exit 2 setup. `--report` prints raw
  values. Reads git objects only; writes only under TMPDIR-honouring temporary directories; no
  /tmp literal.
"""
import argparse
import os
import re
import subprocess
import sys
import tarfile
import tempfile

TOOLS = [
    "tools/mori-blind-check.sh",
    "tools/mori-misroot-sweep.py",
    "tools/mori-round17-context-check.py",
]
SELFTESTS = [
    ["bash", "tools/mori-blind-check.sh", "--selftest"],
    ["python3", "-I", "tools/mori-misroot-sweep.py", "--selftest"],
    ["python3", "-I", "tools/mori-round17-context-check.py", "--selftest"],
]
HOME_RE = re.compile(rb"(?<![>\w])/home/[a-z_][a-z0-9_-]*(?![a-zA-Z0-9_.-])")
CENSUS = "/home/vgpnk/Projects/shokunin/scripts/sources-census.sh"
SOURCES = "corpus/SOURCES.md"


def git(repo, *args):
    return subprocess.run(["git", "-C", repo, *args], capture_output=True)


def extract(repo, rev, dest):
    proc = subprocess.Popen(["git", "-C", repo, "archive", rev], stdout=subprocess.PIPE)
    with tarfile.open(fileobj=proc.stdout, mode="r|") as tf:
        tf.extractall(dest)
    return proc.wait() == 0


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("rev")
    ap.add_argument("--repo", required=True)
    ap.add_argument("--report", action="store_true")
    args = ap.parse_args(argv)
    rv = git(args.repo, "rev-parse", "--verify", "-q", args.rev + "^{commit}")
    if rv.returncode != 0:
        print("C2_SETUP revision unresolvable: %s" % args.rev)
        return 2
    rev = rv.stdout.decode().strip()
    with tempfile.TemporaryDirectory(dir=os.environ.get("TMPDIR")) as d:
        if not extract(args.repo, rev, d):
            print("C2_SETUP cannot extract tree at %s" % rev[:12])
            return 2
        present = sum(1 for t in TOOLS if os.path.exists(os.path.join(d, t)))
        home_lits, vgp = 0, 0
        for dirpath, _dn, filenames in os.walk(os.path.join(d, "tools")):
            for fn in filenames:
                with open(os.path.join(dirpath, fn), "rb") as fh:
                    data = fh.read()
                home_lits += len(HOME_RE.findall(data))
                vgp += data.count(b"vgpnk")
        passed = 0
        for cmd in SELFTESTS:
            if subprocess.run(cmd, capture_output=True, cwd=d).returncode == 0:
                passed += 1
        cs = subprocess.run(["bash", CENSUS, "validate", "--file", os.path.join(d, SOURCES)],
                            capture_output=True, text=True)
        census_ok = cs.returncode == 0
        if args.report:
            print("C2_REPORT rev=%s home_literals=%d vgpnk_refs=%d tools=%d/3 selftests=%d/3 "
                  "census_rc=%d" % (rev[:12], home_lits, vgp, present, passed, cs.returncode))
            return 0
        fails = []
        if home_lits != 0:
            fails.append("home_literals")
        if vgp != 0:
            fails.append("vgpnk_refs")
        if present != len(TOOLS):
            fails.append("tools")
        if passed != len(SELFTESTS):
            fails.append("selftests")
        if not census_ok:
            fails.append("census")
        met = not fails
        print("C2=%s home_literals=%d vgpnk_refs=%d tools=%d selftests=%d/%d census=%s%s rev=%s"
              % ("met" if met else "unmet", home_lits, vgp, present, passed, len(SELFTESTS),
                 "ok" if census_ok else "rc%d" % cs.returncode,
                 (" checks_failed=" + ",".join(fails)) if fails else "", rev[:12]))
        return 0 if met else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
