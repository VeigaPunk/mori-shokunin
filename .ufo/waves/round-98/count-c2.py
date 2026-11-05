#!/usr/bin/env python3
"""count-c2.py — mori round 98 C2 counter (calibration).

Predicate P2 (same sentence as .ufo/waves/round-98/contract.md section C2): at revision R, the
lane's registered calibration gate `tools/mori-scorecard-calibration.py`, taken from R with
sha256 equal to its entering bytes, run as `<tool> R --repo LANE --manifest MANIFEST`, exits 0
and prints `C1=met axes=6 mismatches=0 columns_unchanged=yes` — every SCORECARD `## Axes`
Last-change cell leads with the highest admitted mori closure round that graded the axis
improved/harmed, with Score and Evidence cells unchanged.

Usage: python3 count-c2.py <rev> [--repo LANE] [--manifest PATH] [--work SCRATCH]
Label: C2=met (exit 0) / C2=unmet (exit 1); C2_SETUP (exit 2) when the revision or the tool
cannot be read. Standard library only; the tool copy lives under --work (default: a tempfile dir
honouring TMPDIR) and is deleted on exit.
"""

import argparse
import hashlib
import os
import re
import shutil
import subprocess
import sys
import tempfile

TOOL = "tools/mori-scorecard-calibration.py"
TOOL_SHA = "662fafde7ba446e13a30bc88c10a61d99f933be72902053b1e1e871fc5835113"
LANE = "/home/vgpnk/Projects/shokunin/mori-shokunin"
MANIFEST = "/home/vgpnk/Projects/shokunin/MANIFEST.json"


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("rev")
    ap.add_argument("--repo", default=LANE)
    ap.add_argument("--manifest", default=MANIFEST)
    ap.add_argument("--work")
    a = ap.parse_args(argv)
    r = subprocess.run(["git", "-C", a.repo, "rev-parse", "--verify", a.rev + "^{commit}"],
                       capture_output=True, text=True)
    if r.returncode != 0:
        print("C2_SETUP rev unresolvable")
        return 2
    full = r.stdout.strip()
    r = subprocess.run(["git", "-C", a.repo, "show", "%s:%s" % (full, TOOL)], capture_output=True)
    if r.returncode != 0:
        print("C2_SETUP tool absent at rev")
        return 2
    sha = hashlib.sha256(r.stdout).hexdigest()
    work = tempfile.mkdtemp(prefix="count-c2-r98-", dir=a.work)
    try:
        tool_state = "ok" if sha == TOOL_SHA else "changed"
        tp = os.path.join(work, "calib.py")
        with open(tp, "wb") as fh:
            fh.write(r.stdout)
        p = subprocess.run([sys.executable, tp, full, "--repo", a.repo, "--manifest", a.manifest],
                           capture_output=True, text=True, timeout=600)
        lines = [l for l in p.stdout.splitlines() if l.strip()]
        summary = lines[-1] if lines else ""
        per_axis = [l for l in lines if l.startswith("axis ")]
        mism = [l.split()[1] for l in per_axis if "state=ok" not in l]
        m = re.search(r"mismatches=(\d+)", summary)
        cu = re.search(r"columns_unchanged=(\w+)", summary)
        met = (tool_state == "ok" and p.returncode == 0 and summary.startswith("C1=met axes=6 mismatches=0 columns_unchanged=yes"))
        print("C2=%s mismatches=%s columns_unchanged=%s tool=%s tool_rc=%d mismatched_axes=%s rev=%s"
              % ("met" if met else "unmet", m.group(1) if m else "?", cu.group(1) if cu else "?", tool_state,
                 p.returncode, ",".join(mism) or "-", full[:12]))
        return 0 if met else 1
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
