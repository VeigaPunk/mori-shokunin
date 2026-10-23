#!/usr/bin/env python3
"""Summary-only fixture — round-37 C1 negative arm (r36 w2/MutC2Deleted limit 3).

Computes honestly (delegates to the lane gate) and prints every line except the
per-id `deleted <id>` lines, whose grammar the contract's C2 tool interface
requires. The round-36 counter compared only the summary line and scored it
`C2=met`; the round-37 counter parses the per-id lines and must reject it.
"""
import subprocess
import sys

LANE_REPO = "/home/vgpnk/Projects/shokunin/mori-shokunin"
HONEST = LANE_REPO + "/tools/mori-sources-appendonly.py"


def main(argv):
    proc = subprocess.run([sys.executable, HONEST] + argv, capture_output=True, text=True)
    kept = [line for line in proc.stdout.splitlines() if not line.startswith("deleted ")]
    sys.stdout.write("\n".join(kept) + ("\n" if kept else ""))
    return proc.returncode


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
