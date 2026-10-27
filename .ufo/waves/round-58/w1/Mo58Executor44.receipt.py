#!/usr/bin/env python3
"""Mo58Executor44 — consolidated reproducible receipt for round-58 C1 pointer attacks.

READ-ONLY against the lane. Builds throwaway git fixtures under TMPDIR only.

Run:
  export TMPDIR=/fast/scratch/hyaku/mori-r58/Mo58Executor44
  python3 Mo58Executor44.receipt.py

Emits the exact fixture/rev/verdict table cited in .ufo/waves/round-58/w1/Mo58Executor44.md.
"""
import hashlib
import importlib.util
import io
import json
import os
import re
import subprocess
import sys
import tempfile

LANE_REPO = "/home/vgpnk/Projects/shokunin/mori-shokunin"
FLEET = "/home/vgpnk/Projects/shokunin"
FREEZE = "fe8801120a67c1a6b8899d7d0423839caa09e7d0"
COUNTER_REL = ".ufo/waves/round-58/count-c1.py"

frozen = subprocess.run(["git", "-C", LANE_REPO, "show", f"{FREEZE}:{COUNTER_REL}"],
                        capture_output=True, check=True).stdout
work = open(os.path.join(LANE_REPO, COUNTER_REL), "rb").read()
print(f"freeze rev            : {FREEZE}")
print(f"frozen counter sha256 : {hashlib.sha256(frozen).hexdigest()}")
print(f"worktree  sha256      : {hashlib.sha256(work).hexdigest()}")
print(f"bytes identical       : {frozen == work}")

ROOT = tempfile.mkdtemp(prefix="m58exec44-receipt-")
cp = os.path.join(ROOT, "count-c1-frozen.py")
open(cp, "wb").write(frozen)
spec = importlib.util.spec_from_file_location("c1_frozen", cp)
c1 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c1)

PREAMBLE = """Round 35 (claim C1, calibration). This is the lane's current capabilities register, the
`capabilities` field of the AXES.md SCORECARD contract. It holds one row per capability
that a non-author closure admitted. As the current self-assessment this register supersedes
the `— none yet —` table in the first `## Capabilities` section.

| key | capability | what it can now do | evidence | first-working round |
|---|---|---|---|---|
"""
PADDER = "".join(
    f"| `rounds[{300 + i}].capabilities_added[0]` | pad {i} | Pad. | `tools/mori-vote-bind.py` | 30 |\n"
    for i in range(10))
K0 = "`rounds[832].capabilities_added[0]`"
K1 = "`rounds[832].capabilities_added[1]`"
FILES = {"tools/mori-vote-bind.py": "# vb\n", "tools/mori-driver-liveness.py": "# dl\n",
         ".ufo/waves/round-56/evidence/c2-at-landed.txt": "c2\n",
         ".ufo/waves/round-56/evidence/c1-at-landed.txt": "c1\n"}
mdir = os.path.join(ROOT, "fleet")
os.makedirs(mdir)
rounds = [None] * 833
rounds[832] = {"capabilities_added": ["dual-shape seat-output vote binding (x)",
                                      "strict per-event driver-liveness probe (x)"]}
json.dump({"rounds": rounds}, open(os.path.join(mdir, "MANIFEST.json"), "w"))


def build(name, sc_text):
    d = os.path.join(ROOT, name)
    os.makedirs(d)
    subprocess.run(["git", "-C", d, "init", "-q"], check=True)
    tl = subprocess.run(["git", "-C", d, "rev-parse", "--show-toplevel"],
                        capture_output=True, text=True, check=True).stdout.strip()
    assert tl == d, tl
    for f, c in FILES.items():
        p = os.path.join(d, f)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        open(p, "w").write(c)
    open(os.path.join(d, "SCORECARD.md"), "w").write(sc_text)
    subprocess.run(["git", "-C", d, "add", "-A"], check=True)
    subprocess.run(["git", "-C", d, "-c", "user.name=t", "-c", "user.email=t@t",
                    "commit", "-qm", "f"], check=True)
    rev = subprocess.run(["git", "-C", d, "rev-parse", "HEAD"],
                         capture_output=True, text=True, check=True).stdout.strip()
    return d, rev


def meas(d, rev):
    kl, kf = c1.LANE, c1.FLEET
    c1.LANE, c1.FLEET = d, mdir
    buf = io.StringIO()
    old = sys.stdout
    sys.stdout = buf
    try:
        rc = c1.measure(rev)
    finally:
        sys.stdout = old
        c1.LANE, c1.FLEET = kl, kf
    return rc, buf.getvalue().strip()


def reg(r0, r1):
    return ("## Capabilities\n\n" + PREAMBLE + PADDER
            + f"| {K0} | dual-shape seat-output vote binding | x | {r0} | 56 |\n"
            + f"| {K1} | strict per-event driver-liveness probe | y | {r1} | 56 |\n\n## Saturation\n")


ARMS = [
    ("R01_control_all_resolvable",
     reg("`tools/mori-vote-bind.py`", "`tools/mori-driver-liveness.py`"), []),
    ("R02_missing_under_tools_prefix",
     reg("`tools/no-such-tool.py`", "`tools/mori-driver-liveness.py`"), ["tools/no-such-tool.py"]),
    ("R03_missing_under_corpus_prefix",
     reg("`corpus/no-such.md`", "`tools/mori-driver-liveness.py`"), ["corpus/no-such.md"]),
    ("R04_missing_under_ufo_prefix",
     reg("`.ufo/no-such.txt`", "`tools/mori-driver-liveness.py`"), [".ufo/no-such.txt"]),
    ("R05_missing_under_evidence_prefix",
     reg("`evidence/no-such.txt`", "`tools/mori-driver-liveness.py`"), ["evidence/no-such.txt"]),
    ("R06_missing_under_docs_prefix",
     reg("`docs/no-such.md`", "`tools/mori-driver-liveness.py`"), ["docs/no-such.md"]),
    ("R07_missing_basename_only",
     reg("`no-such-tool.py`", "`tools/mori-driver-liveness.py`"), ["no-such-tool.py"]),
    ("R08_missing_absolute_path",
     reg("`/tools/mori-vote-bind.py`", "`tools/mori-driver-liveness.py`"), ["/tools/mori-vote-bind.py"]),
    ("R09_missing_absolute_host_path",
     reg("`/home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-vote-bind.py`",
         "`tools/mori-driver-liveness.py`"),
     ["/home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-vote-bind.py"]),
    ("R10_pointer_escapes_tree",
     reg("`../MANIFEST.json`", "`tools/mori-driver-liveness.py`"), ["../MANIFEST.json"]),
    ("R11_pointer_to_fleet_root_file",
     reg("`MANIFEST.json`", "`tools/mori-driver-liveness.py`"), ["MANIFEST.json"]),
    ("R12_no_pointer_at_all",
     reg("see the landed artifact", "`tools/mori-driver-liveness.py`"), []),
    ("R13_both_evidence_cells_empty",
     reg("—", "—"), []),
    ("R14_unbackticked_nonexistent_pointer",
     reg("tools/no-such-tool.py", "`tools/mori-driver-liveness.py`"), ["tools/no-such-tool.py"]),
    ("R15_empty_backticks",
     reg("``", "`tools/mori-driver-liveness.py`"), []),
    ("R16_directory_pointer",
     reg("`tools`", "`tools/mori-driver-liveness.py`"), ["tools"]),
    ("R17_subdirectory_pointer",
     reg("`corpus/knowledge`", "`tools/mori-driver-liveness.py`"), ["corpus/knowledge"]),
    ("R18_traversal_up",
     reg("`tools/../tools/mori-vote-bind.py`", "`tools/mori-driver-liveness.py`"),
     ["tools/../tools/mori-vote-bind.py"]),
    ("R19_double_slash",
     reg("`tools//mori-vote-bind.py`", "`tools/mori-driver-liveness.py`"),
     ["tools//mori-vote-bind.py"]),
    ("R20_glob_pointer",
     reg("`tools/*.py`", "`tools/mori-driver-liveness.py`"), ["tools/*.py"]),
    ("R21_trailing_space_pointer",
     reg("`tools/mori-vote-bind.py `", "`tools/mori-driver-liveness.py`"),
     ["tools/mori-vote-bind.py "]),
    ("R22_swapped_pointers",
     reg("`tools/mori-driver-liveness.py`", "`tools/mori-vote-bind.py`"),
     ["tools/mori-driver-liveness.py", "tools/mori-vote-bind.py"]),
    ("R23_key0_twice_key1_absent",
     "## Capabilities\n\n" + PREAMBLE + PADDER
     + f"| {K0} | a | x | `tools/mori-vote-bind.py` | 56 |\n"
     + f"| {K0} | b | y | `tools/mori-driver-liveness.py` | 56 |\n\n## Saturation\n",
     ["tools/mori-vote-bind.py", "tools/mori-driver-liveness.py"]),
    ("R24_emdash_stub_marker_not_matched",
     "## Capabilities\n\n" + PREAMBLE + "| — none yet — | | | |\n" + PADDER
     + f"| {K0} | a | x | `tools/mori-vote-bind.py` | 56 |\n"
     + f"| {K1} | b | y | `tools/mori-driver-liveness.py` | 56 |\n\n## Saturation\n",
     ["tools/mori-vote-bind.py", "tools/mori-driver-liveness.py"]),
    ("R25_hyphen_stub_marker_matched",
     "## Capabilities\n\n" + PREAMBLE + "| -- none yet -- | | | |\n" + PADDER
     + f"| {K0} | a | x | `tools/mori-vote-bind.py` | 56 |\n"
     + f"| {K1} | b | y | `tools/mori-driver-liveness.py` | 56 |\n\n## Saturation\n",
     ["tools/mori-vote-bind.py", "tools/mori-driver-liveness.py"]),
]

DECOY = ("## Capabilities\n\n" + PREAMBLE + PADDER
         + f"| {K0} | decoy | x | `tools/mori-vote-bind.py` | 56 |\n"
         + f"| {K1} | decoy | y | `tools/mori-driver-liveness.py` | 56 |\n")
REAL_EMPTY = ("## Capabilities\n\nRound 35 (claim C1, calibration). This is the lane's current capabilities "
              "register, the\n`capabilities` field of the AXES.md SCORECARD contract.\n\n"
              "| key | capability | what it can now do | evidence | first-working round |\n"
              "|---|---|---|---|---|\n" + PADDER + "\n## Saturation\n")
ARMS.append(("R26_decoy_section_wins_over_real_register",
             "# fixture\n\n" + DECOY + "\n" + REAL_EMPTY,
             ["tools/mori-vote-bind.py", "tools/mori-driver-liveness.py"]))

print()
print("=" * 100)
print(f"{'arm':42s} {'git_rc':7s} {'cnt_rc':6s} counter stdout")
print("=" * 100)
rows = []
for name, sc_text, ptrs in ARMS:
    d, rev = build(name, sc_text)
    rc, out = meas(d, rev)
    grcs = []
    for p in ptrs:
        g = subprocess.run(["git", "-C", d, "cat-file", "-e", f"{rev}:{p}"],
                           capture_output=True, text=True)
        grcs.append(g.returncode)
    grc = ",".join(str(x) for x in grcs) if grcs else "-"
    print(f"{name:42s} {grc:7s} {rc:<6d} {out}")
    print(f"{'':42s} fixture={d}")
    print(f"{'':42s} rev={rev}")
    rows.append((name, rc, out, grc, d, rev))

print()
print("=" * 100)
print("REAL-LANE MEASURE AT THE FREEZE REVISION")
kl, kf = c1.LANE, c1.FLEET
c1.LANE, c1.FLEET = LANE_REPO, FLEET
buf = io.StringIO()
old = sys.stdout
sys.stdout = buf
try:
    rc = c1.measure(FREEZE)
finally:
    sys.stdout = old
    c1.LANE, c1.FLEET = kl, kf
real_out = buf.getvalue().strip()
print(f"  rc={rc}  {real_out}")

contract = open(os.path.join(LANE_REPO, ".ufo/waves/round-58/contract.md")).read()
tgt = re.search(r"Frozen target output \(after\): `([^`]+)`", contract).group(1)
print(f"  contract C1 target : {tgt!r}")
print(f"  actual   C1 stdout : {real_out!r}")
print(f"  BYTE-EXACT MATCH   : {real_out == tgt.replace('R', FREEZE)}")
print(f"  contract-only tokens: {[f for f in tgt.split() if f not in real_out.split()]}")
print(f"  actual-only tokens  : {[f for f in real_out.split() if f not in tgt.split()]}")
print(f"ROOT={ROOT}")
