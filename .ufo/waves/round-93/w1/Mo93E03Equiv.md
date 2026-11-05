# Mo93E03Equiv — C2 equivalence harness, built and sandbox-proven

Wave w1, round 93 attempt 1, lane `mori-shokunin`. Task: build the C2 equivalence
harness as wave evidence and prove it identical (A=B) and able-to-fail (one-character
`--help` mutation).

## Deliverable

`/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-93/w1/equiv-c2.sh` (4461 bytes, bash, executable).

```
Usage: equiv-c2.sh <rev-A> <rev-B> [scratch-root]
  rev-A rev-B    revisions resolvable in the source repo; the repo is
                 "$EQUIV_REPO" if set, else the caller's cwd
  scratch-root   optional parent for this run's work tree; default is a
                 fresh mkdtemp directory under TMPDIR
Output: "A=<sha>", "B=<sha>", one "<tool>: identical|different" line per tool,
        "OVERALL: identical|different".  Exit: 0 identical, 1 different, 2 setup.
```

Design decisions (reused repository conventions, not new ones):

- The four archived files are the three frozen `count-c2.py` `TOOLS` plus
  `tools/mori-round17-jj-regressions.py`, exactly as the wave spec names them.
- Interpreter convention matches the frozen `count-c2.py` `SELFTESTS` list:
  `bash tools/mori-blind-check.sh …`, `python3 -I tools/<py> …`; `--help` and
  `--selftest` are run with cwd at that side's extracted tree root.
- Per side: `git archive <rev> -- <four paths> | tar -x -C <side>/tree`; tool
  scratch goes to `<side>/tmp`, a *sibling* of the tree, with `TMPDIR` set per
  invocation. This matters: `mori-round17-jj-regressions --selftest` refuses a
  scratch parent that contains the gate source (`--scratch overlaps the gate
  source`, exit 2), so a TMPDIR inside the extracted tree degrades its selftest
  to a setup error; the harness layout exercises the real selftest (rc 0, see
  below).
- Compared artifacts per tool: the archived file itself (`tree/tools/<t>`) and
  the six capture files `<t>.{help,selftest}.{out,err,rc}`. Per-tool verdict
  lines name every differing artifact; overall rc 0 identical / 1 different /
  2 setup.
- Work tree (both side trees, tmp dirs, all artifacts) is removed by an EXIT
  trap; a caller-named scratch-root itself is left in place for the caller.
- No host literals: `grep 'vgpnk|/home/|/fast/|shokunin' equiv-c2.sh` → no
  matches. TMPDIR honoured for all temp layout (`mktemp -d` default when no
  scratch-root argument is passed).

## Environment (frozen-contract scratch, all runs)

```
S=/fast/scratch/hyaku/mori-r93/Mo93E03Equiv
trap 'rm -rf -- $S' EXIT
mkdir -p $S && git clone -q --shared --no-checkout /home/vgpnk/Projects/shokunin/mori-shokunin $S/clone \
  && git -C $S/clone checkout -q -B seat 6d82b8d7ef6d94a5527737f9242cdf04ad018da7 \
  && git -C $S/clone rev-parse --show-toplevel && git -C $S/clone rev-parse --short HEAD
```
Output:
```
/fast/scratch/hyaku/mori-r93/Mo93E03Equiv/clone
6d82b8d7
```
`toplevel` assert prints the fixture dir — guard satisfied before the probe
commit below. Tools are byte-identical between the counting base and the patch
base (`git diff --stat 7b3fe9d5… 6d82b8d7… -- tools` is empty), so either base
is a valid A side for the four tools.

Tooling installed/updated this seat: **none** (bash, git, tar, cmp sufficient;
pacman untouched per the host-wide pause).

## Proof 1 — A=B=7b3fe9d540c98b8b0390a0f9bbe78de4341092a5 → identical, rc 0

Command:
```
TMPDIR=$S EQUIV_REPO=$S/clone bash \
  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-93/w1/equiv-c2.sh \
  7b3fe9d540c98b8b0390a0f9bbe78de4341092a5 \
  7b3fe9d540c98b8b0390a0f9bbe78de4341092a5 $S/proof1
echo "rc=$?"
```
Output (final run):
```
A=7b3fe9d540c98b8b0390a0f9bbe78de4341092a5
B=7b3fe9d540c98b8b0390a0f9bbe78de4341092a5
mori-blind-check.sh: identical
mori-misroot-sweep.py: identical
mori-round17-context-check.py: identical
mori-round17-jj-regressions.py: identical
OVERALL: identical
rc=0
```
Wall time ~11 s per run. No temp-path leakage: every selftest stdout/err is
byte-stable across runs, as the contract's equivalence receipt requires.

Calibration history (both failures were harness bugs, fixed before the proofs
above; recorded because a harness that cannot fail cannot be trusted):

1. First run: `EQUIV_SETUP revision unresolvable: 7b3fe9d5…` (rc 2). Cause: I
   passed `--` to `git rev-parse --verify`, which makes git treat the revision
   as a pathspec. The frozen counter calls `rev-parse --verify -q <rev>^{commit}`
   without `--`; the harness now matches that form. Control: plain
   `git -C $S/clone rev-parse --verify 7b3fe9d5…^{commit}` → rc 0, prints the sha.
2. Second run: every tool reported `different [tools/<t> ]` although
   `git archive` is deterministic (manual double extraction + `cmp` → rc 0).
   Cause: the verdict loop compared `$WORK/<side>/tools/<t>` but extraction
   lands at `$WORK/<side>/tree/tools/<t>`; `cmp -s` failed on a missing file.
   Fixed to compare `tree/tools/$t`.

Observed per-mode rc inside the harness layout (tree root cwd, TMPDIR sibling
of the tree; each run under the entering revision, TMPDIR=$S/rcprobe variant
corrected to sibling layout for the jj tool):

| tool | --help rc | --selftest rc |
|---|---|---|
| mori-blind-check.sh | 2 (usage to stderr by design) | 0 (`PASS`) |
| mori-misroot-sweep.py | 0 (argparse) | 0 (`MORI_MISROOT_SELFTEST_OK`) |
| mori-round17-context-check.py | 0 (argparse) | 0 (`SELFTEST_OK`) |
| mori-round17-jj-regressions.py | 0 (argparse) | 0 (`SELFTEST ok: guard_…`) |

jj-regressions layout control (both observed, entering revision):

- sibling layout (harness layout): `python3 -I tools/mori-round17-jj-regressions.py --selftest`
  → stdout begins `SELFTEST ok: guard_output_repo_root,guard_output_tools,…`,
  rc **0**.
- TMPDIR inside the extracted tree → stderr
  `mori-round17-jj-regressions: setup: --scratch overlaps the gate source: …/tree/tools/mori-round17-jj-regressions.py`,
  rc **2**. The harness avoids this by construction, so its comparison for this
  tool is a real selftest run, not two identical setup failures.

## Proof 2 — able-to-fail: one-character `--help` mutation → different, rc 1

The seat patch was taken **before** the probe (see Patch below): the probe
commit exists only inside the since-removed scratch clone.

Mutation: one character of the `--selftest` help string at
`tools/mori-misroot-sweep.py:891` in the scratch clone, `sandbox` → `sandbax`
(`o` → `a`). Fixture-commit sequence (toplevel asserted in the same command):

```
[ "$(git -C $S/clone rev-parse --show-toplevel)" = "$S/clone" ] || { echo "TOPLEVEL GUARD FAILED"; exit 9; }
git -C $S/clone add tools/mori-misroot-sweep.py \
  && git -C $S/clone -c user.name=mori-shokunin -c user.email=mori@shokunin.local \
       commit -q -m "fixture able-to-fail probe: one-character --help mutation (seat Mo93E03Equiv)"
```
Probe commit: `dc7909efa54e691d6973aa578ef247c5e7635975`; its full diff (one
line changed, one character within it):
```
diff --git c/tools/mori-misroot-sweep.py w/tools/mori-misroot-sweep.py
index bb951a5e..4fd0c9ee 100755
--- c/tools/mori-misroot-sweep.py
+++ w/tools/mori-misroot-sweep.py
@@ -888,7 +888,7 @@ def _parse_args(argv=None):
     )
     parser.add_argument(
         "--selftest", action="store_true",
-        help="build an isolated sandbox git repo under TMPDIR with the "
+        help="build an isolated sandbax git repo under TMPDIR with the "
         "byte-exact archived MoriR16.Lesson bytes at the root and prove the "
         "no-pathspec sweep finds it by name while the legacy pathspec misses "
         "it; takes no other flags",
```

Harness run (A = patch base; B = HEAD = probe commit):
```
TMPDIR=$S EQUIV_REPO=$S/clone bash \
  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-93/w1/equiv-c2.sh \
  6d82b8d7ef6d94a5527737f9242cdf04ad018da7 HEAD $S/proof2
echo "rc=$?"
```
Output:
```
A=6d82b8d7ef6d94a5527737f9242cdf04ad018da7
B=dc7909efa54e691d6973aa578ef247c5e7635975
mori-blind-check.sh: identical
mori-misroot-sweep.py: different [tree/tools/mori-misroot-sweep.py mori-misroot-sweep.py.help.out ]
mori-round17-context-check.py: identical
mori-round17-jj-regressions.py: identical
OVERALL: different
rc=1
```
Exactly the mutated tool is flagged, on exactly the two artifacts the mutation
touches: the file bytes and the `--help` stdout. The `--selftest` artifacts stay
identical — correct, since a help string is not part of selftest output — which
demonstrates the harness discriminates per artifact instead of collapsing to a
binary blob verdict. The other three tools remain identical.

## Patch

`patches/Mo93E03Equiv.patch` (0 bytes), generated with
`git -C $S/clone diff 6d82b8d7ef6d94a5527737f9242cdf04ad018da7` before the
probe edit. It is honestly empty: this seat changes no source-tree file; its
deliverables are the wave artifacts `w1/equiv-c2.sh` and this note, written
directly into the wave directory per the seat spec.

## Checks run / unrun

Run: proof 1 (A=B entering → identical rc 0); proof 2 (one-char mutation →
different rc 1, correct artifacts named); determinism control (manual double
`git archive` extraction + `cmp`, rc 0); revision-resolution control (plain
`rev-parse --verify`, rc 0); jj selftest layout control (rc 0 sibling vs rc 2
inside-tree, stderr quoted); per-mode rc census (table above); host-literal
grep over the harness (no matches); fixture toplevel assert before the probe
commit; scratch removal (`ls $S` → absent; sibling scratch dirs untouched).

Unrun (out of my seat scope, not executed): `count-c1.py` / `count-c2.py`
re-runs at any landing revision; `sources-census.sh validate`; the C2 repair
itself (owner seats' patches); a harness run against the *landing* revision
pair (the L1 runs that at integration to produce `evidence/equivalence-c2.txt`;
the harness accepts any two revisions, so no change is needed).

The frozen counters (`count-c1.py`, `count-c2.py`, `controls-r93.sh`,
`contract.md`) were read only; never edited.

Report: .ufo/waves/round-93/w1/Mo93E03Equiv.md
