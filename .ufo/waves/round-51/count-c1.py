#!/usr/bin/env python3
"""mori round 51, claim C1 (operability) — frozen counter for P-C1.

P-C1. At revision R of the source repo (default: the lane this file sits in), all four arms hold:
  (Every clone below is a fresh `git clone --no-local` of the source repo with branch `master` set to R and
  checked out — the lane's own state when R is its tip.)
  A kill_residue  — in a fresh `git clone --no-local` C0 checked out at R, start
                    `python3 tools/mori-pin-check.py --rev R --repo C0` with TMPDIR=<scratch>/tmpA, wait until the
                    run has started writing (a new untracked/ignored path appears in C0, or <scratch>/tmpA holds
                    >= 100 entries), wait 3 s more, SIGKILL its process group; then
                    `git -C C0 status --porcelain --ignored --untracked-files=all` prints 0 lines.
  B relocated     — in a second fresh clone C1 at R, run inside bubblewrap with the source repo's working tree
                    path hidden (`--tmpfs <lane>`; the run asserts <lane>/SKILL.md is absent):
                    `python3 C1/tools/mori-pin-check.py --rev R --repo C1` with TMPDIR=<scratch>/tmpB -> exit 0 and
                    the last line starts `PIN_CHECK=met`.
  C classified    — R's pin-check run `--root F` over the frozen fixture registry F below prints, for prefixes
                    ENVA_SELFTEST and ENVB_SELFTEST, a `state=mismatch` line ending `class=env`; for STLA_SELFTEST
                    and STLB_SELFTEST a `state=mismatch` line ending `class=stale`; for OKAY_SELFTEST a
                    `state=match` line; and a last line `PIN_CHECK=unmet …` ending ` env=2 stale=2`.
  D selftest      — R's `python3 tools/mori-pin-check.py --selftest` exits 0 and its last line is
                    `PIN_CHECK_SELFTEST pass=N fail=0` with N >= 114 (the entering count; no arm removed).

Output: `C1=met|unmet kill_residue=N relocated=met|unmet reloc_mismatch=N classified=ok|bad
selftest=pass=N,fail=N rev=<full> failed=<arms>`. Exit 0 met, 1 unmet, 2 setup error.
Scratch: `--scratch DIR` (default: a mkdtemp under TMPDIR); refused if inside the source repo; removed on exit
unless `--keep`.
"""
import argparse
import os
import shutil
import signal
import subprocess
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
TOOL = "tools/mori-pin-check.py"
ENTERING_SELFTEST = 114

HDR = ("| name | kind | entry | verdict map | self-test | pinned values | write scope | owner |\n"
       "|---|---|---|---|---|---|---|---|\n")
FIXTURES = {
    # env: no tally line at all — setup error naming a missing absolute path, rc 2
    "enva.py": ("import sys\nif '--selftest' in sys.argv:\n"
                "    print('setup error: No such file or directory: /nonexistent/lane/count.py')\n"
                "    sys.exit(2)\n"),
    # env: the instrument dies before printing its tally (traceback-like), rc 1
    "envb.py": ("import sys\nif '--selftest' in sys.argv:\n"
                "    print('Traceback (most recent call last):')\n"
                "    print('FileNotFoundError: [Errno 2] No such file or directory')\n"
                "    sys.exit(1)\n"),
    # stale: it runs and prints a different tally
    "stla.py": ("import sys\nif '--selftest' in sys.argv:\n"
                "    print('STLA_SELFTEST pass=5 fail=0')\n"),
    # stale: the pinned tally text, but an exit code that contradicts it
    "stlb.py": ("import sys\nif '--selftest' in sys.argv:\n"
                "    print('STLB_SELFTEST pass=2 fail=0')\n    sys.exit(1)\n"),
    "okay.py": ("import sys\nif '--selftest' in sys.argv:\n"
                "    print('OKAY_SELFTEST pass=1 fail=0')\n"),
}
ROWS = [("enva", "ENVA_SELFTEST pass=3 fail=0"), ("envb", "ENVB_SELFTEST pass=4 fail=0"),
        ("stla", "STLA_SELFTEST pass=4 fail=0"), ("stlb", "STLB_SELFTEST pass=2 fail=0"),
        ("okay", "OKAY_SELFTEST pass=1 fail=0")]
WANT = {"ENVA_SELFTEST": "env", "ENVB_SELFTEST": "env", "STLA_SELFTEST": "stale", "STLB_SELFTEST": "stale"}


def sh(argv, **kw):
    return subprocess.run(argv, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, **kw)


def fresh_clone(repo, rev, dest):
    p = sh(["git", "clone", "-q", "--no-local", "--no-checkout", repo, dest], timeout=600)
    if p.returncode != 0:
        raise RuntimeError("clone failed: %s" % p.stdout.decode(errors="replace")[-200:])
    # The clone's `master` is R, checked out (the lane's own state when R is its tip): pinned instruments
    # such as .ufo/waves/round-49/count-c1.py read `master` from the repository they run in.
    p = sh(["git", "-C", dest, "checkout", "-q", "-B", "master", rev], timeout=600)
    if p.returncode != 0:
        raise RuntimeError("checkout failed: %s" % p.stdout.decode(errors="replace")[-200:])


def status_lines(clone):
    p = sh(["git", "-C", clone, "status", "--porcelain", "--ignored", "--untracked-files=all"], timeout=600)
    return [l for l in p.stdout.decode(errors="replace").splitlines() if l.strip()]


def count_entries(d):
    n = 0
    for _, dirs, files in os.walk(d):
        n += len(dirs) + len(files)
        if n >= 100:
            break
    return n


def arm_kill(repo, rev, w):
    c0 = os.path.join(w, "c0")
    fresh_clone(repo, rev, c0)
    if status_lines(c0):
        raise RuntimeError("fresh clone not clean")
    tmp = os.path.join(w, "tmpA")
    os.makedirs(tmp)
    env = dict(os.environ, TMPDIR=tmp)
    proc = subprocess.Popen([sys.executable, os.path.join(c0, TOOL), "--rev", rev, "--repo", c0],
                            cwd=w, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                            start_new_session=True)
    started = False
    t0 = time.time()
    while time.time() - t0 < 180:
        if proc.poll() is not None:
            break
        if status_lines(c0) or count_entries(tmp) >= 100:
            started = True
            break
        time.sleep(0.5)
    if started:
        time.sleep(3)
    try:
        os.killpg(proc.pid, signal.SIGKILL)
    except ProcessLookupError:
        pass
    proc.wait()
    if not started:
        return None, "no_progress"
    left = status_lines(c0)
    return len(left), (left[0][:120] if left else "-")


def arm_relocated(repo, rev, w, lane_hidden):
    c1 = os.path.join(w, "c1")
    fresh_clone(repo, rev, c1)
    tmp = os.path.join(w, "tmpB")
    os.makedirs(tmp)
    probe = ("import os,sys,subprocess\n"
             "if os.path.exists(%r): print('C1_RELOC_SETUP lane visible'); sys.exit(2)\n"
             "sys.exit(subprocess.call([sys.executable, %r, '--rev', %r, '--repo', %r]))\n"
             % (os.path.join(lane_hidden, "SKILL.md"), os.path.join(c1, TOOL), rev, c1))
    argv = ["bwrap", "--bind", "/", "/", "--dev", "/dev", "--proc", "/proc", "--tmpfs", lane_hidden,
            "--chdir", w, "--setenv", "TMPDIR", tmp, "--", sys.executable, "-c", probe]
    p = sh(argv, timeout=3000)
    out = p.stdout.decode(errors="replace").splitlines()
    with open(os.path.join(w, "relocated.out"), "w") as f:
        f.write("\n".join(out) + "\n")
    if any(l.startswith("C1_RELOC_SETUP") for l in out):
        raise RuntimeError("lane path still visible inside bwrap")
    last = out[-1] if out else ""
    mism = sum(1 for l in out if "state=mismatch" in l or "state=no_command" in l)
    return p.returncode == 0 and last.startswith("PIN_CHECK=met"), mism, out


def arm_classified(repo, rev, w):
    tree = os.path.join(w, "tool-at-rev")
    os.makedirs(os.path.join(tree, "tools"))
    p = sh(["git", "-C", repo, "show", "%s:%s" % (rev, TOOL)], timeout=120)
    if p.returncode != 0:
        raise RuntimeError("tool absent at rev")
    tool = os.path.join(tree, TOOL)
    with open(tool, "wb") as f:
        f.write(p.stdout)
    fx = os.path.join(w, "fixture")
    os.makedirs(os.path.join(fx, "tools"))
    for name, src in FIXTURES.items():
        with open(os.path.join(fx, "tools", name), "w") as f:
            f.write(src)
    body = HDR
    for stem, tally in ROWS:
        body += ("| %s | gate | `python3 tools/%s.py` | 0 ok | `python3 tools/%s.py --selftest` → `%s` | none | "
                 "read-only | mori |\n" % (stem, stem, stem, tally))
    with open(os.path.join(fx, "SKILL.md"), "w") as f:
        f.write(body)
    q = sh([sys.executable, tool, "--root", fx, "--timeout", "60"], cwd=w,
           env=dict(os.environ, TMPDIR=os.path.join(w, "tmpC")), timeout=600)
    out = q.stdout.decode(errors="replace").splitlines()
    ok = True
    for prefix, cls in WANT.items():
        lines = [l for l in out if "prefix=%s " % prefix in l]
        ok = ok and len(lines) == 1 and "state=mismatch" in lines[0] and lines[0].endswith("class=" + cls)
    okay = [l for l in out if "prefix=OKAY_SELFTEST " in l]
    ok = ok and len(okay) == 1 and "state=match" in okay[0] and "class=" not in okay[0]
    last = out[-1] if out else ""
    ok = ok and last.startswith("PIN_CHECK=unmet") and last.endswith(" env=2 stale=2")
    return ok, out


def arm_selftest(repo, rev, w):
    tree = os.path.join(w, "st")
    os.makedirs(tree)
    a = subprocess.Popen(["git", "-C", repo, "archive", "--format=tar", rev], stdout=subprocess.PIPE)
    t = subprocess.run(["tar", "-x", "-C", tree], stdin=a.stdout, timeout=600)
    a.wait()
    if a.returncode != 0 or t.returncode != 0:
        raise RuntimeError("archive failed")
    tmp = os.path.join(w, "tmpD")
    os.makedirs(tmp)
    p = sh([sys.executable, os.path.join(tree, TOOL), "--selftest"], cwd=tree,
           env=dict(os.environ, TMPDIR=tmp), timeout=1800)
    lines = [l for l in p.stdout.decode(errors="replace").splitlines() if l.startswith("PIN_CHECK_SELFTEST ")]
    if not lines:
        return False, "none"
    last = lines[-1]
    try:
        kv = dict(x.split("=") for x in last.split()[1:])
        npass, nfail = int(kv["pass"]), int(kv["fail"])
    except (ValueError, KeyError):
        return False, last
    return p.returncode == 0 and nfail == 0 and npass >= ENTERING_SELFTEST, "pass=%d,fail=%d" % (npass, nfail)


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("rev")
    ap.add_argument("--repo", default=DEFAULT_REPO, help="source repo (default: the lane this file sits in)")
    ap.add_argument("--hide", default=DEFAULT_REPO, help="path hidden inside bwrap (default: the lane)")
    ap.add_argument("--scratch")
    ap.add_argument("--keep", action="store_true")
    a = ap.parse_args(argv)
    repo = os.path.abspath(a.repo)
    p = sh(["git", "-C", repo, "rev-parse", "--verify", a.rev + "^{commit}"], timeout=60)
    if p.returncode != 0:
        print("C1_SETUP unresolvable revision %s" % a.rev)
        return 2
    rev = p.stdout.decode().strip()
    base = os.path.abspath(a.scratch) if a.scratch else tempfile.mkdtemp(prefix="mori-r51-c1-")
    for inside in (repo, os.path.abspath(a.hide)):
        if os.path.commonpath([base, inside]) == inside:
            print("C1_SETUP scratch inside %s" % inside)
            return 2
    os.makedirs(base, exist_ok=True)
    w = tempfile.mkdtemp(prefix="c1-", dir=base)
    try:
        failed = []
        residue, first = arm_kill(repo, rev, w)
        if residue is None or residue != 0:
            failed.append("kill_residue")
        reloc, mism, _ = arm_relocated(repo, rev, w, os.path.abspath(a.hide))
        if not reloc:
            failed.append("relocated")
        cls_ok, cls_out = arm_classified(repo, rev, w)
        if not cls_ok:
            failed.append("classified")
        st_ok, st = arm_selftest(repo, rev, w)
        if not st_ok:
            failed.append("selftest")
        for l in cls_out:
            if "prefix=" in l or l.startswith("PIN_CHECK="):
                print("classified: " + l[:240])
        print("kill_residue_first: %s" % first)
        print("C1=%s kill_residue=%s relocated=%s reloc_mismatch=%d classified=%s selftest=%s rev=%s failed=%s"
              % ("unmet" if failed else "met", "none" if residue is None else residue,
                 "met" if reloc else "unmet", mism, "ok" if cls_ok else "bad", st, rev,
                 ",".join(failed) or "-"))
        return 1 if failed else 0
    except (RuntimeError, OSError, subprocess.SubprocessError) as exc:
        print("C1_SETUP %s" % exc)
        return 2
    finally:
        if not a.keep:
            shutil.rmtree(w, ignore_errors=True)
            if not a.scratch:
                shutil.rmtree(base, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
