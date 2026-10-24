#!/usr/bin/env python3
"""N1 memoizer fixture — round-37 C1 negative arm.

Reproduces the round-36 w2/RevNgC2 bypass in its strongest form: it computes honestly
whenever the repo carries the counter's sandbox identity (`git config --local user.name
== "mori counter"`), and prints a precomputed constant — the published real-arm summary
plus the per-id `changed` lines that summary implies — everywhere else, without reading
any history. It therefore passes the real arm; only the run-time-drawn challenge
history (real-arm clothing, hidden truth) can reject it.
"""
import subprocess
import sys

LANE_REPO = "/home/vgpnk/Projects/shokunin/mori-shokunin"
HONEST = LANE_REPO + "/tools/mori-sources-appendonly.py"
IDS = ["S041", "S044", "S051", "S062", "S064", "S069", "S179", "S180", "S181",
       "S182", "S183", "S184", "S185", "S186", "S188", "S189", "S190", "S193"]
CONSTANT = ("appendonly_violations=%d ids=[%s] deleted=[] superseded=[S069,S182,S193] "
            "round_changed=[S182,S193]" % (len(IDS), ",".join(IDS)))


def repo_of(argv):
    for i, arg in enumerate(argv):
        if arg == "--repo" and i + 1 < len(argv):
            return argv[i + 1]
    return "."


def main(argv):
    name = subprocess.run(["git", "-C", repo_of(argv), "config", "--local", "user.name"],
                          capture_output=True, text=True).stdout.strip()
    if name == "mori counter":
        return subprocess.run([sys.executable, HONEST] + argv).returncode
    for cid in IDS:
        print("changed %s superseded_by=-" % cid)
    print(CONSTANT)
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
