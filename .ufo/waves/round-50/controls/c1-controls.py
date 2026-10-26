#!/usr/bin/env python3
"""Round 50 C1 controls: build each control as a commit in a throwaway shared clone of the lane, score it
with the frozen count-c1.py, and write one receipt per control under ../evidence/.

Usage: c1-controls.py <entering-rev> --scratch DIR
Every control starts from the entering revision. The clone lives under DIR (git clone --shared); every git
call names -C <clone>; the clone's toplevel is checked before the first commit; the fixture identity is set
on the clone only. Nothing is written in the lane except the receipts.

Controls (expected verdict before data):
  do-nothing              the entering revision itself                                  unmet
  all-latest              every Last change cell set to round 49 (improved), evidence cites round 49  unmet
  pins-deleted            the two SHONEN tally pins removed (commands kept)            unmet (pins_floor)
  pins-updated-no-receipt SHONEN pins set to the observed tallies, no receipts         unmet (receipt_missing)
  axes-only               Axes table fixed from the manifest, SHONEN untouched         unmet
  shonen-only             SHONEN pins fixed with receipts, Axes table untouched        unmet
  box-dropped             SHONEN box 3 deleted                                         unmet (boxes_floor, pins_floor)
  witness                 Axes table fixed and SHONEN pins fixed with receipts         met (feasibility only)
"""
import importlib.util
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
WAVE = os.path.dirname(HERE)
LANE = os.path.dirname(os.path.dirname(os.path.dirname(WAVE)))
FLEET = os.path.dirname(LANE)
COUNTER = os.path.join(WAVE, "count-c1.py")
EVID = os.path.join(WAVE, "evidence")

spec = importlib.util.spec_from_file_location("c1", COUNTER)
c1 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c1)


def g(repo, *args, check=True):
    return subprocess.run(["git", "-C", repo] + list(args), check=check, stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE).stdout.decode()


def axes_fixed(sc, targets):
    out = []
    for line in sc.split("\n"):
        cells = c1.split_cells(line) if re.match(r"^ {0,3}\|", line) else []
        ax = cells[0].strip("* ").lower() if cells else ""
        if len(cells) == 4 and ax in targets:
            n, v = targets[ax]
            spot = "corpus/lessons/round-%d-verifier-spotcheck.md" % n
            ev = cells[2] + "; latest admitted closure grading %s %s: `%s`" % (ax, v, spot)
            if ax == "adjacency":
                ev = cells[2]
            line = "| %s | %s | %s | round %d (%s, score held) |" % (cells[0], cells[1], ev, n, v)
        out.append(line)
    return "\n".join(out)


def all_latest(sc):
    out = []
    for line in sc.split("\n"):
        cells = c1.split_cells(line) if re.match(r"^ {0,3}\|", line) else []
        if len(cells) == 4 and cells[0].strip("* ").lower() in c1.AXES:
            line = "| %s | %s | %s; `corpus/lessons/round-49-verifier-spotcheck.md` | round 49 (improved, score held) |" % (
                cells[0], cells[1], cells[2])
        out.append(line)
    return "\n".join(out)


def main(argv):
    if len(argv) != 3 or argv[1] != "--scratch":
        print("usage: c1-controls.py <entering-rev> --scratch DIR", file=sys.stderr)
        return 2
    entering, scratch = argv[0], os.path.abspath(argv[2])
    os.makedirs(scratch, exist_ok=True)
    d = os.path.join(scratch, "c1-fixture")
    subprocess.run(["rm", "-rf", "--", d], check=True)
    subprocess.run(["git", "clone", "-q", "--shared", "--no-checkout", LANE, d], check=True)
    if os.path.realpath(g(d, "rev-parse", "--show-toplevel").strip()) != os.path.realpath(d):
        print("fixture toplevel mismatch", file=sys.stderr)
        return 2
    g(d, "config", "user.name", "fixture")
    g(d, "config", "user.email", "fixture@invalid")
    base = g(LANE, "rev-parse", entering + "^{commit}").strip()
    manifest = g(FLEET, "show", "%s:MANIFEST.json" % c1.FLEET_REV)
    targets = c1.manifest_targets(manifest)
    sc0 = g(LANE, "show", "%s:SCORECARD.md" % base)
    sh0 = g(LANE, "show", "%s:SHONEN.md" % base)
    obs = {"tools/mori-pin-check.py": None, "tools/mori-unlanded-check.py": None}
    for p in obs:
        tree = os.path.join(scratch, "obs-tree")
        if not os.path.isdir(tree):
            os.makedirs(tree)
            a = subprocess.Popen(["git", "-C", LANE, "archive", base], stdout=subprocess.PIPE)
            subprocess.run(["tar", "-x", "-C", tree], stdin=a.stdout, check=True)
            a.stdout.close()
            a.wait()
        env = dict(os.environ, TMPDIR=scratch, PYTHONDONTWRITEBYTECODE="1")
        out = subprocess.run([sys.executable, p, "--selftest"], cwd=tree, env=env, stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT, timeout=900).stdout.decode()
        obs[p] = c1.TALLY.findall(out)[-1]
    subprocess.run(["rm", "-rf", "--", os.path.join(scratch, "obs-tree")], check=True)
    (pp, pa, pf), (up, ua, uf) = obs["tools/mori-pin-check.py"], obs["tools/mori-unlanded-check.py"]
    sh_upd = sh0.replace("(60/60)", "(%s/%d)" % (pa, int(pa) + int(pf))).replace(
        "(13/13)", "(%s/%d)" % (ua, int(ua) + int(uf)))
    sh_nopin = sh0.replace(" (60/60)", "").replace(" (13/13)", "")
    sh_lines = sh0.split("\n")
    box_idx = [i for i, l in enumerate(sh_lines) if c1.BOX.match(l)]
    sh_drop = "\n".join(l for i, l in enumerate(sh_lines) if i != box_idx[2])
    receipts = {
        c1.RECEIPT_DIR + "mori-pin-check.txt": "%s pass=%s fail=%s\n" % (pp, pa, pf),
        c1.RECEIPT_DIR + "mori-unlanded-check.txt": "%s pass=%s fail=%s\n" % (up, ua, uf),
    }
    controls = [
        ("do-nothing", {}),
        ("all-latest", {"SCORECARD.md": all_latest(sc0)}),
        ("pins-deleted", {"SHONEN.md": sh_nopin}),
        ("pins-updated-no-receipt", {"SHONEN.md": sh_upd}),
        ("axes-only", {"SCORECARD.md": axes_fixed(sc0, targets)}),
        ("shonen-only", dict({"SHONEN.md": sh_upd}, **receipts)),
        ("box-dropped", {"SHONEN.md": sh_drop}),
        ("witness", dict({"SCORECARD.md": axes_fixed(sc0, targets), "SHONEN.md": sh_upd}, **receipts)),
    ]
    rc_all = 0
    for name, edits in controls:
        rev = base
        if edits:
            g(d, "checkout", "-q", "--detach", base)
            for path, body in edits.items():
                full = os.path.join(d, path)
                os.makedirs(os.path.dirname(full), exist_ok=True)
                with open(full, "w") as f:
                    f.write(body)
                g(d, "add", "--", path)
            g(d, "commit", "-q", "-m", "control")
            rev = g(d, "rev-parse", "HEAD").strip()
        repo = d if edits else LANE
        r = subprocess.run([sys.executable, COUNTER, rev, "--repo", repo, "--fleet-repo", FLEET,
                            "--scratch", os.path.join(scratch, "count-" + name)],
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        text = r.stdout.decode()
        with open(os.path.join(EVID, "control-c1-%s.txt" % name), "w") as f:
            f.write("$ count-c1.py <%s> --fleet-repo <fleet>  (control %s, entering %s)\n%sexit=%d\n"
                    % ("entering" if not edits else "fixture commit", name, base, text, r.returncode))
        print("%-24s exit=%d %s" % (name, r.returncode, text.strip().split("\n")[-1]))
        if (name == "witness") != (r.returncode == 0):
            rc_all = 1
    subprocess.run(["rm", "-rf", "--", d], check=True)
    return rc_all


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
