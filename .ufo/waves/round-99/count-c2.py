#!/usr/bin/env python3
"""count-c2.py -- mori round 99, claim C2 (calibration), frozen counter.

Predicate P2 (same sentence as .ufo/waves/round-99/contract.md section C2): at revision R, for
each of the six SCORECARD `## Axes` rows the `Evidence pointer` cell carries a located pointer to
the highest admitted mori closure that graded that axis improved or harmed in the fleet
MANIFEST.json pinned at fleet commit FLEET_PIN -- the token
`corpus/lessons/round-<N>-verifier-spotcheck.md:<L>` where line L of that file at R names the axis
and the verdict word, or, when R holds no spot-check file for round N, the token `rounds[<I>]`
with I that closure's index in the pinned MANIFEST -- while every Score cell stays byte-equal to
its entering bytes (ENTERING), every Last-change cell equals its entering bytes or that same text
after one prepended `round <N> (<verdict>, score held); ` clause, and the registered calibration
gate `tools/mori-scorecard-calibration.py` (sha256 equal to its entering bytes) run as
`<gate> R --repo LANE --manifest PINNED --base R` exits 0 printing `C1=met` (every Last-change
cell leads with that same closure round and verdict).

Usage: python3 .ufo/waves/round-99/count-c2.py <rev> [--repo LANE] [--fleet FLEET]
Output: one `axis <name> expect=round_<N> pointer=ok|missing|bad-line` line per axis, then
  C2=met|unmet mismatches=M cells_unchanged=yes|no gate=ok|<detail> mismatched_axes=<list|->
Exit 0 met, 1 unmet, 2 setup (C2_SETUP line: bad git, unreadable pinned MANIFEST).
Read-only: git show / git rev-parse only; the gate runs from a copy written under TMPDIR
(tempfile honours TMPDIR; /tmp is never hardcoded), removed on exit.
"""

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

AXES = ("coverage", "operability", "depth", "freshness", "calibration", "adjacency")
ENTERING = "73308ff6e5c933f53498e9501ef95917b0ef7171"
FLEET_PIN = "4ad377eae8e3eed8f7f32ab5d335feb25dbae94b"
GATE = "tools/mori-scorecard-calibration.py"
GATE_SHA = "662fafde7ba446e13a30bc88c10a61d99f933be72902053b1e1e871fc5835113"
HERE = os.path.dirname(os.path.abspath(__file__))
LANE_DEFAULT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
FLEET_DEFAULT = os.path.normpath(os.path.join(LANE_DEFAULT, ".."))


class Setup(Exception):
    pass


def git(repo, *args, binary=False):
    p = subprocess.run(["git", "-C", repo, *args], capture_output=True)
    if p.returncode != 0:
        raise Setup("git %s failed: %s" % (" ".join(args), p.stderr.decode(errors="replace").strip()))
    return p.stdout if binary else p.stdout.decode()


def git_maybe(repo, *args):
    p = subprocess.run(["git", "-C", repo, *args], capture_output=True)
    return p.stdout.decode(errors="replace") if p.returncode == 0 else None


def axes_rows(text):
    rows, inside = {}, False
    for line in text.splitlines():
        if re.match(r"^##\s+Axes\s*$", line):
            inside = True
            continue
        if inside and line.startswith("## "):
            break
        if inside and line.lstrip().startswith("|"):
            cells = [c.strip() for c in line.split("|")[1:-1]]
            if len(cells) >= 4 and cells[0] in AXES and cells[0] not in rows:
                rows[cells[0]] = {"score": cells[1], "evidence": cells[2], "last": cells[3]}
    return rows


def expectations(manifest):
    exp = {}
    for idx, r in enumerate(manifest.get("rounds", [])):
        if r.get("lane") != "mori" or r.get("type") != "closure":
            continue
        if not (r.get("admitted") is True or str(r.get("admitted")).lower() == "true"):
            continue
        try:
            rnd = int(r.get("lane_round", r.get("round")))
        except (TypeError, ValueError):
            continue
        verdicts = r.get("verdicts") or {}
        for axis in AXES:
            if verdicts.get(axis) in ("improved", "harmed"):
                if axis not in exp or rnd > exp[axis][0]:
                    exp[axis] = (rnd, idx, verdicts[axis])
    return exp


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("rev")
    ap.add_argument("--repo", default=LANE_DEFAULT)
    ap.add_argument("--fleet", default=FLEET_DEFAULT)
    a = ap.parse_args(argv)
    try:
        rev = git(a.repo, "rev-parse", "--verify", a.rev + "^{commit}").strip()
        mbytes = git(a.fleet, "show", "%s:MANIFEST.json" % FLEET_PIN, binary=True)
        manifest = json.loads(mbytes)
        now = axes_rows(git(a.repo, "show", "%s:SCORECARD.md" % rev))
        ent = axes_rows(git(a.repo, "show", "%s:SCORECARD.md" % ENTERING))
        gate_bytes = git(a.repo, "show", "%s:%s" % (rev, GATE), binary=True)
    except (Setup, ValueError) as e:
        print("C2_SETUP %s" % e)
        return 2
    exp = expectations(manifest)
    mism = []
    def last_ok(axis):
        old, new = ent[axis]["last"], now[axis]["last"]
        return new == old or re.fullmatch(r"round \d+ \((?:improved|harmed), score held\); " + re.escape(old), new)

    cells_same = all(axis in now and axis in ent and now[axis]["score"] == ent[axis]["score"]
                     and last_ok(axis) for axis in AXES)
    for axis in AXES:
        state = "missing"
        if axis not in exp or axis not in now:
            state = "no-expectation" if axis not in exp else "no-row"
        else:
            rnd, idx, verdict = exp[axis]
            ev = now[axis]["evidence"]
            path = "corpus/lessons/round-%d-verifier-spotcheck.md" % rnd
            body = git_maybe(a.repo, "show", "%s:%s" % (rev, path))
            if body is None:
                state = "ok" if re.search(r"rounds\[%d\]" % idx, ev) else "missing"
            else:
                lines = body.splitlines()
                hits = re.findall(re.escape(path) + r":(\d+)", ev)
                if hits:
                    state = "bad-line"
                for h in hits:
                    n = int(h)
                    if 1 <= n <= len(lines):
                        low = lines[n - 1].lower()
                        if axis in low and verdict in low:
                            state = "ok"
                            break
        if state != "ok":
            mism.append(axis)
        print("axis %s expect=%s pointer=%s" % (axis, ("round_%d" % exp[axis][0]) if axis in exp else "none", state))
    gate = "skipped"
    if hashlib.sha256(gate_bytes).hexdigest() != GATE_SHA:
        gate = "sha-differs"
    else:
        tmp = tempfile.mkdtemp(prefix="mori-r99-c2-")
        try:
            gp = os.path.join(tmp, "gate.py")
            mp = os.path.join(tmp, "MANIFEST.json")
            with open(gp, "wb") as fh:
                fh.write(gate_bytes)
            with open(mp, "wb") as fh:
                fh.write(mbytes)
            p = subprocess.run([sys.executable, gp, rev, "--repo", a.repo, "--manifest", mp, "--base", rev],
                               capture_output=True, text=True)
            last = (p.stdout.strip().splitlines() or [""])[-1]
            gate = "ok" if p.returncode == 0 and last.startswith("C1=met ") else "rc%d" % p.returncode
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
    met = not mism and cells_same and gate == "ok"
    print("C2=%s mismatches=%d cells_unchanged=%s gate=%s mismatched_axes=%s rev=%s" % (
        "met" if met else "unmet", len(mism), "yes" if cells_same else "no", gate,
        ",".join(mism) or "-", rev[:12]))
    return 0 if met else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
