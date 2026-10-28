#!/usr/bin/env python3
"""Round 59 C1 counter (calibration) — the active-register checker is landed at
its frozen SHA, resists its frozen hostile fixtures, and binds the two
round-56 register rows to a revision-pinned fleet MANIFEST.

Frozen predicate P-C1 (same sentence in contract.md, this counter and the
receipt label):
  At revision R, tools/mori-register-check.py exists with sha256 equal to PIN;
  `python3 tools/mori-register-check.py --selftest` prints
  `REGCHECK_SELFTEST pass=12 fail=0` and exits 0; executed once per directory
  under .ufo/waves/round-59/fixtures-c1/ (each carrying scorecard.md +
  manifest.json + the paths its rows point at) it exits 1 with reason tokens
  matching that fixture's frozen expect file; executed against R's
  SCORECARD.md and the MANIFEST.json of fleet revision MANIFEST_REV (extracted
  to scratch, evidence paths materialized from R under the scratch root) it
  prints verdict REGISTER_MET and the frozen bound names; and every backticked
  evidence path it reports resolves under R via `git cat-file -e R:path`.

Usage: count-c1.py <rev> [--repo DIR] [--fleet DIR] [--scratch DIR]
       count-c1.py --selftest
Output: `C1=met|unmet selftest=ok|bad fixtures=ok|bad real=ok|bad
  pointers=ok|bad rev=R` (+ ` failed=<reasons>` when unmet).  Exit 0 met,
  1 unmet, 2 setup.
Read-only on both repos: git show / cat-file only; tool and fixture trees are
materialized under --scratch/TMPDIR.  Honors TMPDIR.
"""
import hashlib
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

TOOL = "tools/mori-register-check.py"
FIXDIR = ".ufo/waves/round-59/fixtures-c1"
EXPECT_SELFTEST = "REGCHECK_SELFTEST pass=12 fail=0"
REQUIRE = ["rounds[832].capabilities_added[0]", "rounds[832].capabilities_added[1]"]
BOUND = {
    "rounds[832].capabilities_added[0]":
        "dual-shape seat-output vote binding",
    "rounds[832].capabilities_added[1]":
        "strict per-event driver-liveness probe",
}
MANIFEST_REV = "2807c6ab8a9b04dcf256682bcd722c695fdd6e14"
PIN = "38b733d896f880f5b7ecb464848b80798810ab052fcf0a8afb320918151472b8"  # frozen at freeze commit


def sha256(b):
    return hashlib.sha256(b).hexdigest()


def git(repo, *args):
    p = subprocess.run(["git", "-C", repo] + list(args),
                       capture_output=True, timeout=120)
    return p


def git_show(repo, rev, path):
    p = git(repo, "show", "%s:%s" % (rev, path))
    return p.stdout if p.returncode == 0 else None


def run_tool(tool_path, scratch, scorecard, manifest, root):
    p = subprocess.run(
        ["python3", str(tool_path), "--scorecard", str(scorecard),
         "--manifest", str(manifest), "--root", str(root),
         *[x for r in REQUIRE for x in ("--require", r)]],
        capture_output=True, text=True, timeout=120, cwd=str(scratch))
    try:
        out = json.loads(p.stdout)
    except ValueError:
        out = None
    return p, out


def materialize(repo, rev, paths, root):
    root = Path(root)
    ok = True
    for rel in paths:
        b = git_show(repo, rev, rel)
        if b is None:
            ok = False
            continue
        f = root / rel
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_bytes(b)
    return ok


def measure(repo, fleet, rev, scratch):
    scratch = Path(scratch)
    scratch.mkdir(parents=True, exist_ok=True)
    failed = []
    detail = {}
    tool_b = git_show(repo, rev, TOOL)
    tool_ok = tool_b is not None and sha256(tool_b) == PIN
    if tool_b is None:
        failed.append("tool_absent")
    elif not tool_ok:
        failed.append("tool_sha")

    # materialize tool
    tp = scratch / "tool.py"
    if tool_b is not None:
        tp.write_bytes(tool_b)

    # selftest arm
    st_ok = False
    if tool_b is not None:
        st_dir = scratch / "st"
        p = subprocess.run(["python3", str(tp), "--selftest",
                            "--scratch", str(st_dir)],
                           capture_output=True, text=True, timeout=300,
                           env={**os.environ, "TMPDIR": str(scratch)})
        st_ok = p.returncode == 0 and EXPECT_SELFTEST in p.stdout
    detail["selftest"] = st_ok
    if not st_ok:
        failed.append("selftest")

    # fixture arm: every committed fixture dir must be judged UNMET with its
    # frozen expected reason prefix.
    fix_ok = True
    fix_listing = git(repo, "ls-tree", "--name-only", "%s:%s" % (rev, FIXDIR))
    names = [] if fix_listing.returncode != 0 else [
        n for n in fix_listing.stdout.decode().splitlines() if n]
    dirs = [n for n in names if not n.endswith(".py")]
    if not dirs:
        fix_ok = False
        failed.append("fixtures_absent")
    for name in dirs:
        base = "%s/%s" % (FIXDIR, name)
        exp_b = git_show(repo, rev, base + "/expect.txt")
        sc_b = git_show(repo, rev, base + "/scorecard.md")
        mf_b = git_show(repo, rev, base + "/manifest.json")
        if exp_b is None or sc_b is None or mf_b is None:
            fix_ok = False
            failed.append("fixture:%s:incomplete" % name)
            continue
        expect = exp_b.decode().strip().split(",")
        fdir = scratch / "fx" / name
        fdir.mkdir(parents=True, exist_ok=True)
        (fdir / "scorecard.md").write_bytes(sc_b)
        (fdir / "manifest.json").write_bytes(mf_b)
        file_list = git(repo, "ls-tree", "-r", "--name-only", rev, base + "/")
        for f in (file_list.stdout.decode().splitlines()
                  if file_list.returncode == 0 else []):
            rel = f[len(base) + 1:]
            if rel in ("scorecard.md", "manifest.json", "expect.txt"):
                continue
            materialize(repo, rev, [f], fdir / "_files")
        p, out = run_tool(tp, scratch, fdir / "scorecard.md",
                          fdir / "manifest.json", fdir / "_files")
        reasons = [] if out is None else out.get("reasons", [])
        got = {r.split("=", 1)[0].split(":", 1)[0] + ":" +
               r.split(":", 1)[1].split("=", 1)[0] if ":" in r else r
               for r in reasons}
        matched = all(any(r.startswith(e) for r in reasons) for e in expect)
        verdict_unmet = p.returncode != 0 and (
            out is None or out.get("verdict") != "REGISTER_MET")
        if not (verdict_unmet and matched):
            fix_ok = False
            failed.append("fixture:%s" % name)

    # real arm
    real_ok = False
    ptr_ok = False
    sc = git_show(repo, rev, "SCORECARD.md")
    mf = git_show(fleet, MANIFEST_REV, "MANIFEST.json") if fleet else None
    if sc is None:
        failed.append("scorecard")
    if mf is None:
        failed.append("manifest")
    if tool_b is not None and sc is not None and mf is not None:
        rdir = scratch / "real"
        rdir.mkdir(parents=True, exist_ok=True)
        (rdir / "scorecard.md").write_bytes(sc)
        (rdir / "manifest.json").write_bytes(mf)
        proot = rdir / "_root"
        proot.mkdir(exist_ok=True)
        # first pass learns the pointer list; pointers are checked by the tool
        # under proot AND by git cat-file here.
        p, out = run_tool(tp, scratch, rdir / "scorecard.md",
                          rdir / "manifest.json", proot)
        ptrs = [] if out is None else out.get("pointers", [])
        all_exist = bool(ptrs)
        for rel in ptrs:
            rel2 = rel[2:] if rel.startswith("./") else rel
            if git(repo, "cat-file", "-e", "%s:%s" % (rev, rel2)).returncode != 0:
                all_exist = False
                failed.append("pointer:%s" % rel2)
            else:
                materialize(repo, rev, [rel2], proot)
        p, out = run_tool(tp, scratch, rdir / "scorecard.md",
                          rdir / "manifest.json", proot)
        bmap = {} if out is None else (out.get("bound") or {})
        real_ok = (p.returncode == 0 and out is not None
                   and out.get("verdict") == "REGISTER_MET"
                   and sorted(bmap) == sorted(BOUND)
                   and all(bmap[k].startswith(v) for k, v in BOUND.items()))
        ptr_ok = all_exist
    detail["real"] = real_ok
    detail["pointers"] = ptr_ok
    if not real_ok:
        failed.append("real")
    if not ptr_ok:
        failed.append("pointers")

    met = (tool_ok and st_ok and fix_ok and real_ok and ptr_ok
           and not failed)
    return met, failed, detail


def selftest():
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "c1", os.path.abspath(__file__))
    here = Path(__file__).resolve().parent
    passed = failed = 0

    def chk(name, cond):
        nonlocal passed, failed
        if cond:
            passed += 1
        else:
            failed += 1
            print("FAIL " + name, file=sys.stderr)

    chk("require_two", len(REQUIRE) == 2)
    chk("bound_names", BOUND[REQUIRE[0]].startswith("dual-shape"))
    chk("manifest_rev", len(MANIFEST_REV) == 40)
    chk("pin_set", PIN != "0" * 64)
    chk("fixdir_rel", not FIXDIR.startswith("/"))
    chk("expect_token", EXPECT_SELFTEST.endswith("fail=0"))
    print("C1_SELFTEST pass=%d fail=%d" % (passed, failed))
    return 0 if failed == 0 else 1


def main(argv):
    if "--selftest" in argv:
        return selftest()
    if not argv or argv[0].startswith("-"):
        print(__doc__)
        return 2
    rev = argv[0]
    repo = "/home/vgpnk/Projects/shokunin/mori-shokunin"
    fleet = "/home/vgpnk/Projects/shokunin"
    scratch = None
    i = 1
    while i < len(argv):
        if argv[i] == "--repo":
            repo = argv[i + 1]
        elif argv[i] == "--fleet":
            fleet = argv[i + 1]
        elif argv[i] == "--scratch":
            scratch = argv[i + 1]
        i += 2
    if scratch is None:
        scratch = tempfile.mkdtemp(prefix="mori-r59-c1-",
                                   dir=os.environ.get("TMPDIR") or None)
    met, failed, detail = measure(repo, fleet, rev, scratch)
    line = ("C1=%s selftest=%s fixtures=%s real=%s pointers=%s rev=%s"
            % ("met" if met else "unmet",
               "ok" if detail.get("selftest") else "bad",
               "ok" if "fixtures_absent" not in failed
                   and not any(f.startswith("fixture") for f in failed)
                   else "bad",
               "ok" if detail.get("real") else "bad",
               "ok" if detail.get("pointers") else "bad", rev))
    if not met:
        line += " failed=" + ",".join(failed) if failed else " failed=unknown"
    print(line)
    return 0 if met else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
