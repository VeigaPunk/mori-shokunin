#!/usr/bin/env python3
"""mori round-94 C2 counter (operability): the round-94 counters carry no host home path, and they run
where HOME points nowhere when the fleet root is passed by environment.

Frozen predicate P-C2 (`.ufo/waves/round-94/contract.md` section C2; this docstring, the contract and
the receipt label are the same sentence):

  At revision R `python3 -I .ufo/waves/round-94/count-c2v2.py R --repo <clone> --root <fleet>` prints
  `C2=met literal_r94=0 files_r94=3 frozen_r93=unchanged env_i=met env_unset=rc2 rev=<12>` and exits 0,
  where, over the extracted tree at R:
  * `literal_r94` counts occurrences of an absolute home-directory path (`/home/<user>`) in every
    `.py` and `.sh` file under `.ufo/waves/round-94/` (must be 0; `files_r94` must be >= 3);
  * `frozen_r93=unchanged` means the three round-93 counter files at R have exactly the blob hashes
    pinned below (the round-93 counters are frozen history, never edited);
  * `env_i=met`: `count-c1v2.py R` run from the extracted tree with `env -i`-style environment
    (`HOME=/nonexistent`, `SHOKUNIN_ROOT=<fleet>`, `TMPDIR` honoured) prints `C1=met` and exits 0;
  * `env_unset=rc2`: the same run without `SHOKUNIN_ROOT` and without `--census` exits 2 (C1_SETUP),
    so the counter fails closed rather than falling back to a host path.
  Otherwise `C2=unmet ... checks_failed=<list>`; exit 1; exit 2 setup. `--report --scan DIR` prints the
  literal count over DIR at R (used for the entering measurement of round 93 counters).
"""
import argparse
import os
import re
import subprocess
import sys
import tarfile
import tempfile

HOST = re.compile(rb"/home/[a-z_][a-z0-9_-]*")
PIN_R93 = {
    ".ufo/waves/round-93/count-c1.py": "45a9d07dc4a1d9be905d847e2e34fa1d9faea2f4",
    ".ufo/waves/round-93/count-c2.py": "7d0a003cf82162b02e9f740f81bfd200f91c6d3c",
    ".ufo/waves/round-93/controls-r93.sh": "be60882e947fc1827af62f69207f9f9a9f5630f1",
}
SCAN = ".ufo/waves/round-94"
COUNTER = ".ufo/waves/round-94/count-c1v2.py"
SUFFIXES = (".py", ".sh")


def git(repo, *args):
    return subprocess.run(["git", "-C", repo, *args], capture_output=True)


def extract(repo, rev, dest):
    proc = subprocess.Popen(["git", "-C", repo, "archive", rev], stdout=subprocess.PIPE)
    with tarfile.open(fileobj=proc.stdout, mode="r|") as tf:
        tf.extractall(dest)
    return proc.wait() == 0


def literal_count(folder):
    total, files = 0, 0
    if not os.path.isdir(folder):
        return 0, 0
    for dirpath, _dn, filenames in os.walk(folder):
        for fn in filenames:
            if fn.endswith(SUFFIXES):
                files += 1
                with open(os.path.join(dirpath, fn), "rb") as fh:
                    total += len(HOST.findall(fh.read()))
    return total, files


def frozen_unchanged(repo, rev):
    for path, want in PIN_R93.items():
        r = git(repo, "rev-parse", "--verify", "-q", "%s:%s" % (rev, path))
        if r.returncode != 0 or r.stdout.decode().strip() != want:
            return False
    return True


def run_c1(tree, repo, rev, env):
    cmd = ["python3", "-I", os.path.join(tree, COUNTER), rev, "--repo", repo]
    return subprocess.run(cmd, capture_output=True, text=True, env=env)


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("rev")
    ap.add_argument("--repo", required=True)
    ap.add_argument("--root", default=None)
    ap.add_argument("--scan", default=None)
    ap.add_argument("--report", action="store_true")
    args = ap.parse_args(argv)
    rv = git(args.repo, "rev-parse", "--verify", "-q", args.rev + "^{commit}")
    if rv.returncode != 0:
        print("C2_SETUP revision unresolvable: %s" % args.rev)
        return 2
    rev = rv.stdout.decode().strip()
    scratch = os.environ.get("TMPDIR") or None
    with tempfile.TemporaryDirectory(dir=scratch) as d:
        if not extract(args.repo, rev, d):
            print("C2_SETUP cannot extract tree at %s" % rev[:12])
            return 2
        if args.report:
            folder = os.path.join(d, args.scan) if args.scan else os.path.join(d, SCAN)
            lits, files = literal_count(folder)
            print("C2_REPORT rev=%s scan=%s literal=%d files=%d" % (rev[:12], args.scan or SCAN, lits, files))
            return 0
        if not args.root:
            print("C2_SETUP --root (fleet root) is required")
            return 2
        lits, files = literal_count(os.path.join(d, SCAN))
        frozen = frozen_unchanged(args.repo, rev)
        base_env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "HOME": "/nonexistent",
                    "SHOKUNIN_ROOT": args.root}
        if scratch:
            base_env["TMPDIR"] = scratch
        ok_run = run_c1(d, args.repo, rev, base_env)
        env_i = ok_run.returncode == 0 and "C1=met" in ok_run.stdout
        unset_env = {k: v for k, v in base_env.items() if k != "SHOKUNIN_ROOT"}
        unset_run = run_c1(d, args.repo, rev, unset_env)
        env_unset_rc2 = unset_run.returncode == 2
        fails = []
        if lits != 0:
            fails.append("literal")
        if files < 3:
            fails.append("files")
        if not frozen:
            fails.append("frozen")
        if not env_i:
            fails.append("env_i")
        if not env_unset_rc2:
            fails.append("env_unset")
        met = not fails
        print("C2=%s literal_r94=%d files_r94=%d frozen_r93=%s env_i=%s env_unset=rc%d%s rev=%s"
              % ("met" if met else "unmet", lits, files, "unchanged" if frozen else "changed",
                 "met" if env_i else "unmet", unset_run.returncode,
                 (" checks_failed=" + ",".join(fails)) if fails else "", rev[:12]))
        return 0 if met else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
