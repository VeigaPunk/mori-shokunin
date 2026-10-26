#!/usr/bin/env python3
"""Round 52 C1 controls — build each control as a commit in a throwaway clone of the lane at the entering tip,
score it with the frozen counter, write the receipt. Usage: c1-controls.py <scratch-dir> [name...]
Every receipt records the literal command line it ran (routed defect 7 of the round-51 closure); the clone and
the counter scratch live under <scratch-dir> (outside the lane) and are removed at the end.
"""
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
W = os.path.dirname(HERE)
LANE = os.path.dirname(os.path.dirname(os.path.dirname(W)))
FLEET = os.path.dirname(LANE)
E = "4f266ef2fdf74d8b046f5b4f5a5c4945f65b966d"
CONTROLS = {
    "axes-only": "axes,locator",
    "receipts-only": "receipts",
    "living-only": "living",
    "rewrite-in-place": "axes,locator,receipts,rewrite",
    "delete-stale-pins": "axes,locator,receipts,delete",
    "repeat-stale-tally": "axes,locator,receipts,repeat",
    "witness": "axes,locator,receipts,living",
}


def sh(*a, **k):
    return subprocess.run(list(a), check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, **k)


def main(argv):
    base = os.path.abspath(argv[0])
    names = argv[1:] or ["do-nothing"] + list(CONTROLS)
    os.makedirs(base, exist_ok=True)
    for name in names:
        d = os.path.join(base, "clone-" + name)
        shutil.rmtree(d, ignore_errors=True)
        sh("git", "clone", "-q", "--no-local", LANE, d)
        if sh("git", "-C", d, "rev-parse", "--show-toplevel").stdout.decode().strip() != d:
            raise SystemExit("clone toplevel mismatch")
        sh("git", "-C", d, "checkout", "-q", "--detach", E)
        rev = E
        if name != "do-nothing":
            tmp = os.path.join(base, "tmp-" + name)
            os.makedirs(tmp, exist_ok=True)
            sh(sys.executable, os.path.join(HERE, "c1-data.py"), d, CONTROLS[name], env=dict(os.environ, TMPDIR=tmp))
            sh("git", "-C", d, "add", "-A")
            sh("git", "-C", d, "-c", "user.name=mori-control", "-c", "user.email=control@mori.invalid",
               "commit", "-q", "-m", "control " + name)
            rev = sh("git", "-C", d, "rev-parse", "HEAD").stdout.decode().strip()
        scratch = os.path.join(base, "c1-" + name)
        cmd = [sys.executable, os.path.join(W, "count-c1.py"), rev, "--repo", d, "--fleet-repo", FLEET,
               "--scratch", scratch]
        q = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        out = os.path.join(W, "evidence", "control-c1-%s.txt" % name)
        with open(out, "w", encoding="utf-8") as f:
            f.write("# control %s (parts: %s); clone of the lane at %s, control commit %s\n"
                    % (name, CONTROLS.get(name, "-"), E, rev))
            f.write("$ python3 .ufo/waves/round-52/count-c1.py %s --repo %s --fleet-repo %s --scratch %s\n"
                    % (rev, d, FLEET, scratch))
            f.write(q.stdout.decode("utf-8", "replace"))
            f.write("exit=%d\n" % q.returncode)
        last = q.stdout.decode("utf-8", "replace").strip().split("\n")[-1]
        print("%s exit=%d %s" % (name, q.returncode, last))
        shutil.rmtree(d, ignore_errors=True)
        shutil.rmtree(scratch, ignore_errors=True)
        shutil.rmtree(os.path.join(base, "tmp-" + name), ignore_errors=True)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
