# Mo52ExecC1Controls — the three C1 controls replayed independently

Seat: Mo52ExecC1Controls (leaf executor). Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin`.
Lane tip during the run: `075436b1` (round-52 w1 dispatch). Entering tip `4f266ef2fdf74d8b046f5b4f5a5c4945f65b966d`,
freeze `d3a8ea5957b73bddbde750a8c0af2fba8da8b7c2`, data `8524904adb25e44f24d9f25aac7eae909625c18c`.
Read first: `contract.md`, `controls/c1-controls.py`, `controls/c1-data.py`, `count-c1.py` (P-C1 docstring, main,
`superseded`), and the eight frozen `evidence/control-c1-*.txt` receipts.

Assignment: replay `rewrite-in-place`, `repeat-stale-tally`, `witness` and compare every verdict line with the
frozen receipts — without overwriting them.

## Method

The frozen `c1-controls.py` writes its receipts to `<wave>/evidence/` and derives `W`/`LANE`/`FLEET` from its own
`__file__`, so a copy outside the lane cannot run unmodified. Both scripts were copied to
`/fast/scratch/hyaku/mori-r52/Mo52ExecC1Controls/scripts/` (sha256 of the originals:

```
1eb6087fc4e8358c0d136ed29d3b3470fc6b220a4c4e6cd64472bebd5bb14213  .ufo/waves/round-52/controls/c1-controls.py
ff9500a5a2d4bb1e1f372119f2761a3bdd6a98c58af0f025ada77609331ef120  .ufo/waves/round-52/controls/c1-data.py
e864922790451b4026be784d5344d9a06827b251ed3c81bfe26b1c559ee3c300  .ufo/waves/round-52/count-c1.py
```

and `sha256sum -c` of all 26 lines of `evidence/freeze-sha256.txt` against the working tree printed no failure,
so the instrument I replayed is the frozen instrument.)

`c1-data.py` was copied byte-identical (`cmp` → identical) and not edited. In `c1-controls.py` only the four
location constants were set and the receipt directory redirected (this is one edit more than the seat spec's
"only the receipt output directory": the three path constants are consequences of copying the file out of the
lane, and no derivation logic was touched):

```diff
 HERE = os.path.dirname(os.path.abspath(__file__))
-W = os.path.dirname(HERE)
-LANE = os.path.dirname(os.path.dirname(os.path.dirname(W)))
+# Mo52ExecC1Controls replay: the copy lives outside the lane, so the three paths the original derives from
+# __file__ are set explicitly. No other line of the script differs from the frozen original (md5 of the
+# original: 0d1eb2c5b4d80d82c0a5185482bf57a7).
+W = "/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-52"
+LANE = "/home/vgpnk/Projects/shokunin/mori-shokunin"
 FLEET = os.path.dirname(LANE)
+OUTDIR = os.path.join(os.path.dirname(HERE), "receipts")
 E = "4f266ef2fdf74d8b046f5b4f5a5c4945f65b966d"
@@
-        out = os.path.join(W, "evidence", "control-c1-%s.txt" % name)
+        os.makedirs(OUTDIR, exist_ok=True)
+        out = os.path.join(OUTDIR, "control-c1-%s.txt" % name)
```

Command (cwd `/fast/scratch/hyaku/mori-r52/Mo52ExecC1Controls`, `TMPDIR` in the same scratch, wall time 214 s,
whole-run rc 0):

```
$ export TMPDIR=/fast/scratch/hyaku/mori-r52/Mo52ExecC1Controls/tmp
$ cd /fast/scratch/hyaku/mori-r52/Mo52ExecC1Controls
$ python3 scripts/c1-controls.py /fast/scratch/hyaku/mori-r52/Mo52ExecC1Controls/ctl \
    rewrite-in-place repeat-stale-tally witness
rewrite-in-place exit=1 C1=unmet items=42 axes=6 pins=2 boxes=4 living=4 superseded=1 locators=27 mismatches=3 errors=0 hidden=0 lane_writes=0 manifest=6209bdb8e400 rev=98220db89b865fd73e36f548cd7cfc8aca11492c failed=mismatch
repeat-stale-tally exit=1 C1=unmet items=42 axes=6 pins=2 boxes=4 living=7 superseded=4 locators=27 mismatches=3 errors=0 hidden=0 lane_writes=0 manifest=6209bdb8e400 rev=95d5e46b605a06649023ce9490a3c61139af042a failed=mismatch
witness exit=0 C1=met items=42 axes=6 pins=2 boxes=4 living=7 superseded=4 locators=27 mismatches=0 errors=0 hidden=0 lane_writes=0 manifest=6209bdb8e400 rev=f5b7686ad6653e1d80ec913f42aa26ae8c9ff767
replay-rc=0
```

Each run cloned the lane with `git clone --no-local` into the scratch, asserted `rev-parse --show-toplevel` equals
the clone dir, checked out `4f266ef2`, applied the part list with `c1-data.py`, committed as
`mori-control <control@mori.invalid>`, scored with the frozen `count-c1.py --repo <clone> --fleet-repo
/home/vgpnk/Projects/shokunin --scratch <scratch>`, then removed the clone, the counter scratch and the `TMPDIR`
of that part.

## Verdict comparison

Line-for-line diff of my receipts against `evidence/control-c1-<name>.txt`, excluding only the receipt's own
header and the recorded command line (which carry the clone path and control commit):

| control | L1 receipt (frozen) | my replay | item-line differences |
|---|---|---|---|
| rewrite-in-place | `C1=unmet items=42 … living=4 superseded=1 locators=27 mismatches=3 … failed=mismatch`, exit 1 | identical counts, `mismatches=3`, exit 1 | 0 of 42 |
| repeat-stale-tally | `C1=unmet items=42 … living=7 superseded=4 locators=27 mismatches=3 … failed=mismatch`, exit 1 | identical counts, `mismatches=3`, exit 1 | 0 of 42 |
| witness | `C1=met items=42 … living=7 superseded=4 locators=27 mismatches=0 errors=0 hidden=0 lane_writes=0`, exit 0 | identical counts, `mismatches=0`, exit 0 | 0 of 42 |

`diff` of the item blocks returned exactly one differing line per control, and in every case it is the verdict
line's `rev=` field, which is the new control commit (new clone, new commit timestamp) — not a verdict:

```
43c43
< C1=unmet ... rev=18091f0a78933df0c43d316d44022fe875b02139 failed=mismatch
---
> C1=unmet ... rev=98220db89b865fd73e36f548cd7cfc8aca11492c failed=mismatch
```

`manifest=6209bdb8e400` reproduced in all three, i.e. the fleet MANIFEST bytes at the pinned `--fleet-rev
f0b61b4ad192bcd95d7a76613a626f71285996ed` are unchanged since the freeze, so the axis arm's target set was the
same input in both runs.

The three mismatching items per control are exactly the arm the control isolates, with the same text as the
frozen receipts:

rewrite-in-place (all three are the append-only clause — the stale pins still present at `E`, rewritten):

```
item living corpus/QUALITY.md expect=`python3_tools/mori-sources-appendonly.py_--selftest`_→_`pass=12_fail=0` got=pin_removed_or_rewritten state=mismatch
item living corpus/README.md expect=`--selftest`_→_`pass=9_fail=0` got=pin_removed_or_rewritten state=mismatch
item living corpus/README.md expect=`python3_tools/mori-sources-appendonly.py_--selftest`_→_`pass=12_fail=0` got=pin_removed_or_rewritten state=mismatch
```

repeat-stale-tally (the superseding lines that repeat the stale tally are themselves enumerated and run):

```
item living corpus/QUALITY.md:1354 expect=pass=12_fail=0 got=MORI_SOURCES_APPENDONLY_SELFTEST_pass=22_fail=0_rc=0 state=mismatch
item living corpus/README.md:722 expect=pass=12_fail=0 got=MORI_SOURCES_APPENDONLY_SELFTEST_pass=22_fail=0_rc=0 state=mismatch
item living corpus/README.md:722 expect=pass=9_fail=0 got=unrunnable state=mismatch
```

witness (zero mismatches; the six live items):

```
item living corpus/QUALITY.md:885 expect=CONFORM_SELFTEST_pass=6_fail=0 got=superseded state=ok
item living corpus/QUALITY.md:909 expect=pass=12_fail=0 got=superseded state=ok
item living corpus/QUALITY.md:1360 expect=MORI_SOURCES_APPENDONLY_SELFTEST_pass=22_fail=0 got=MORI_SOURCES_APPENDONLY_SELFTEST_pass=22_fail=0_rc=0 state=ok
item living corpus/README.md:607 expect=pass=9_fail=0 got=superseded state=ok
item living corpus/README.md:608 expect=pass=12_fail=0 got=superseded state=ok
item living corpus/README.md:727 expect=MORI_SOURCES_APPENDONLY_SELFTEST_pass=22_fail=0 got=MORI_SOURCES_APPENDONLY_SELFTEST_pass=22_fail=0_rc=0 state=ok
item living corpus/README.md:728 expect=CONFORM_SELFTEST_pass=9_fail=0 got=CONFORM_SELFTEST_pass=9_fail=0_rc=0 state=ok
```

These agree with the contract's pre-data control table (rows `rewrite-in-place`, `repeat-stale-tally`,
`witness`) on every field except the elided revision.

## Supporting checks

1. Applier determinism. Same input (`git archive 4f266ef2` extracted into a scratch fixture, `rev-parse
   --show-toplevel` asserted equal to the fixture) and same part list, twice, gives the same git tree id:

```
tree rewrite-in-place run=a 5ddb9f90e3b27d8db5ef73cdeeb41a1d7db2fbc7
tree rewrite-in-place run=b 5ddb9f90e3b27d8db5ef73cdeeb41a1d7db2fbc7
tree witness run=a 46e2a3176049404f6a8671d26a645c42393304e9
tree witness run=b 46e2a3176049404f6a8671d26a645c42393304e9
```

   (In these fixtures `HEAD` does not exist, so `c1-data.py`'s receipts part writes `<lane checkout at >` into the
   two selftest files and this tree id is not the control commit's tree id. The check shows the applier contains no
   nondeterminism; it does not reconstruct the L1's tree — see limit 2.)

2. Counter self-test replayed from the scratch (`TMPDIR` in scratch, cwd in scratch, no writes to the lane):
   `C1_SELFTEST pass=42 fail=0`, rc 0 — identical to the frozen `evidence/selftest-c1.txt` tail.

3. No lane writes. `lane_writes=0` in all three runs; `stat` on the eight `evidence/control-c1-*.txt` still shows
   the L1's mtimes (20:55:35 … 21:04:33), and `find` over `controls/`, `SCORECARD.md`, `SHONEN.md`,
   `corpus/QUALITY.md`, `corpus/README.md` with `-newer` than a `git status --porcelain --ignored
   --untracked-files=all` snapshot taken before the replay returned nothing. Only `/fast/scratch/.../receipts/`
   was written.

4. Cross-reference: `evidence/c1-at-data.txt` (landed data `8524904a`) reads `C1=met … mismatches=0 … exit=0`, the
   same tally the witness control reached independently at `E`, so the landed data and the disclosed witness agree.

## Limits of this replay (not fixes)

1. Only the three assigned controls were replayed; `do-nothing`, `axes-only`, `receipts-only`, `living-only`,
   `delete-stale-pins` keep their single-run receipts.
2. Control commits are not preserved: `c1-controls.py` deletes the clone, so a replay can compare counter output
   but not the control commit's tree id against the L1's. Equality is therefore judged on 42 item lines + the
   verdict counts per control, plus applier determinism (check 1) — not on tree identity.
3. Agreement is agreement of an instrument run twice by two seats of the same lane; the counter runs the pinned
   commands unsandboxed in an archive of `R` (P-C1 named limit), and a matching tally still proves only that the
   instrument prints the pin, not that its arms are good.
4. `items=42` counts one entry per enumerated tally token, so one README line carrying two tally pins
   (`README.md:722` in repeat-stale-tally) contributes two items; item counts are therefore not row counts.

## Findings

1. **LOW — replay reproduces the frozen controls exactly; no divergence to report.**
   `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-52/evidence/control-c1-{rewrite-in-place,
   repeat-stale-tally,witness}.txt`: 126 of 126 item lines identical, verdict counts identical, exit codes
   identical (1, 1, 0); the only differing line in each diff is `rev=` (a new control commit). `manifest=` tag
   identical, so no fleet drift entered the axis arm.
2. **LOW — the frozen control builder cannot be run from outside the lane without editing it.**
   `.ufo/waves/round-52/controls/c1-controls.py:12-14` derives `W` and `LANE` by walking up from `__file__`, so an
   independent replay must patch three constants (mine: `W`, `LANE`, `OUTDIR`). Receipts still record their literal
   command line (routed defect 7), but the script's location is an implicit input that no receipt records. Routed
   to round 53 as a builder-ergonomics item; no change proposed to any counter, predicate or kill rule.
3. **LOW — control commits are discarded, so the receipt's `control commit <sha>` cannot be re-derived.**
   `c1-controls.py` (`shutil.rmtree(d, ignore_errors=True)` after the run) leaves the recorded commit id
   unreachable; a later seat can re-run the builder but cannot check the recorded tree. This is the one gap that
   keeps the controls' pre-data readings from being independently reconstructible rather than merely
   reproducible in outcome.
4. **LOW — witness feasibility is confirmed independently of the L1's run.** `witness` reads
   `C1=met … mismatches=0`, exit 0, and the landed data commit reads the same tally
   (`evidence/c1-at-data.txt`), so C1's "met" is not an artefact of one clone or one wall clock.

Scratch `/fast/scratch/hyaku/mori-r52/Mo52ExecC1Controls/` removed after the report was written; no tool was
installed or upgraded for this seat; no file under the lane was written except this report.

Report: .ufo/waves/round-52/w1/Mo52ExecC1Controls.md
