#!/usr/bin/env python3
"""mori round-94 controls (frozen with count-c1v2.py and count-c2v2.py; run before any claim data is read).

Usage: python3 -I .ufo/waves/round-94/controls-r94.py <lane-repo> <fleet-root>

Each embedded-hash fixture is one commit in a scratch clone of the lane, made from the entering
base 84b15230, changing exactly one `verified-at:` line of a round-92 trio file so that the file's
8-character admission hash sits INSIDE a longer token. The frozen round-93 counter (v1, read from
the base revision) and the round-94 counter (v2, from the lane tree) both run on each fixture
through their public `main` path (`--repo <clone> <rev>`). The discriminating expectation:

  v1 (frozen, substring test)      reads each embedded fixture `C1=met`   (false pass)
  v2 (token test)                  reads each embedded fixture `C1=unmet checks_failed=admission`
  v2 on the unmodified base        reads `C1=met adm_ok=19`               (the live data still passes)

Prints one `CTRL` line per fixture and one `EMBED_FALSE_PASS` summary; exit 0 iff the expectations
hold, else 1; exit 2 on setup failure. Scratch lives under $HYAKU_SCRATCH/mori-r94 (default
/fast/scratch/hyaku) and is removed on exit. Git writes happen only inside that scratch clone, which
the script checks with `rev-parse --show-toplevel` before committing.
"""
import os
import shutil
import subprocess
import sys
import tempfile

BASE = "84b152308fa6c2f224ad75dff68e525dab9057ac"
ENTERING = "7b3fe9d540c98b8b0390a0f9bbe78de4341092a5"
FIXTURE_FILE = "corpus/knowledge/counter-win-r77.md"
V1_PATH = ".ufo/waves/round-93/count-c1.py"
HERE = os.path.dirname(os.path.abspath(__file__))
V2 = os.path.join(HERE, "count-c1v2.py")
FIXTURES = [
    ("left", lambda ac: "f" + ac + "0"),
    ("right", lambda ac: ac + "9f"),
    ("middle", lambda ac: "a" + ac + "b"),
]


def git(repo, *args, check=True):
    r = subprocess.run(["git", "-C", repo, *args], capture_output=True, text=True)
    if check and r.returncode != 0:
        raise RuntimeError("git %s failed: %s" % (" ".join(args), r.stderr.strip()))
    return r


def verdict(stdout):
    head = stdout.split()[0] if stdout.split() else "NONE"
    return head


def run_counter(counter_src, rev, clone, census, scratch):
    env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "HOME": scratch, "TMPDIR": scratch}
    cmd = ["python3", "-I", counter_src, rev, "--repo", clone]
    if counter_src == V2:
        cmd += ["--census", census]
    r = subprocess.run(cmd, capture_output=True, text=True, env=env)
    return r.returncode, r.stdout.strip()


def admission(clone, rel):
    r = git(clone, "log", "--diff-filter=A", "--format=%h", ENTERING, "--", rel)
    lines = [ln for ln in r.stdout.split() if ln]
    if not lines:
        raise RuntimeError("no admission commit for %s" % rel)
    return lines[-1]


def main(argv):
    if len(argv) != 2:
        print("usage: controls-r94.py <lane-repo> <fleet-root>")
        return 2
    lane, fleet = os.path.abspath(argv[0]), os.path.abspath(argv[1])
    census = os.path.join(fleet, "scripts", "sources-census.sh")
    if not os.path.isfile(census) or not os.path.isfile(V2):
        print("CTRL_SETUP missing census or counter")
        return 2
    scratch_root = os.environ.get("HYAKU_SCRATCH") or "/fast/scratch/hyaku"
    os.makedirs(os.path.join(scratch_root, "mori-r94"), exist_ok=True)
    scratch = tempfile.mkdtemp(prefix="controls-", dir=os.path.join(scratch_root, "mori-r94"))
    try:
        clone = os.path.join(scratch, "clone")
        subprocess.run(["git", "clone", "--shared", "-q", "--no-checkout", lane, clone],
                       check=True, capture_output=True)
        if git(clone, "rev-parse", "--show-toplevel").stdout.strip() != clone:
            print("CTRL_SETUP clone toplevel mismatch")
            return 2
        v1_src = os.path.join(scratch, "count-c1-r93.py")
        v1_bytes = subprocess.run(["git", "-C", lane, "show", "%s:%s" % (BASE, V1_PATH)],
                                  capture_output=True).stdout
        if not v1_bytes:
            print("CTRL_SETUP frozen v1 counter not readable at base")
            return 2
        with open(v1_src, "wb") as fh:
            fh.write(v1_bytes)
        git(clone, "checkout", "-q", "--detach", BASE)

        v1_base_rc, v1_base = run_counter(v1_src, BASE, clone, census, scratch)
        v2_base_rc, v2_base = run_counter(V2, BASE, clone, census, scratch)
        print("CTRL do-nothing v1=%s v2=%s" % (verdict(v1_base), verdict(v2_base)))
        print("CTRL do-nothing v1_line=%s" % v1_base)
        print("CTRL do-nothing v2_line=%s" % v2_base)
        live_ok = v2_base_rc == 0 and verdict(v2_base) == "C1=met" and " adm_ok=19 " in (v2_base + " ")

        original = git(clone, "show", "%s:%s" % (BASE, FIXTURE_FILE)).stdout
        ac = admission(clone, FIXTURE_FILE)
        false_pass_v1, rejected_v2 = 0, 0
        for label, make in FIXTURES:
            git(clone, "checkout", "-q", "--detach", BASE)
            lines = original.splitlines(keepends=True)
            idx = [i for i, ln in enumerate(lines) if ln.startswith("verified-at:")]
            if len(idx) != 1 or ac not in lines[idx[0]]:
                print("CTRL_SETUP fixture line not as expected for %s" % label)
                return 2
            lines[idx[0]] = lines[idx[0]].replace(ac, make(ac), 1)
            with open(os.path.join(clone, FIXTURE_FILE), "w", encoding="utf-8") as fh:
                fh.write("".join(lines))
            git(clone, "add", FIXTURE_FILE)
            git(clone, "-c", "user.name=mori-r94-controls", "-c", "user.email=controls@fixture.invalid",
                "-c", "commit.gpgsign=false", "commit", "-q", "-m", "round-94 control fixture %s" % label)
            rev = git(clone, "rev-parse", "HEAD").stdout.strip()
            _r1, out1 = run_counter(v1_src, rev, clone, census, scratch)
            _r2, out2 = run_counter(V2, rev, clone, census, scratch)
            v1v, v2v = verdict(out1), verdict(out2)
            if v1v == "C1=met":
                false_pass_v1 += 1
            if v2v == "C1=unmet" and "checks_failed=" in out2 and "admission" in out2:
                rejected_v2 += 1
            print("CTRL %s rev=%s v1=%s v2=%s v2_line=%s" % (label, rev[:12], v1v, v2v, out2))

        total = len(FIXTURES)
        v2_false_pass = total - rejected_v2
        print("EMBED_FALSE_PASS v1=%d/%d v2=%d/%d live_v2=%s do_nothing_v1=%s do_nothing_v2=%s"
              % (false_pass_v1, total, v2_false_pass, total, "met" if live_ok else "unmet",
                 verdict(v1_base), verdict(v2_base)))
        expected = (false_pass_v1 == total and rejected_v2 == total and live_ok)
        return 0 if expected else 1
    finally:
        shutil.rmtree(scratch, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
