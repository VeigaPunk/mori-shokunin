# Mo52ExecC1Replay — C1 calibration counter, independent replay (mori round 52, wave w1)

Seat: Mo52ExecC1Replay (executor, leaf; no subagent, no labrat probe). Lane `mori-shokunin`
(`/home/vgpnk/Projects/shokunin/mori-shokunin`). Contract: `.ufo/waves/round-52/contract.md`
(freeze `d3a8ea5957b73bddbde750a8c0af2fba8da8b7c2`); entering tip `4f266ef2fdf74d8b046f5b4f5a5c4945f65b966d`;
data `8524904adb25e44f24d9f25aac7eae909625c18c`. Scratch used and removed:
`/fast/scratch/hyaku/mori-r52/Mo52ExecC1Replay/` (every output cited below was copied here first).

Headline: with the counter's `repo` on a quiescent copy of R, **every line of both receipts reproduced
byte-for-byte** (selftest, data-tip verdict, 42 data-tip items, control verdict-counts and 37 control items).
With `repo` on the live lane during the wave, the same data-tip run reads `C1=unmet` while **all 42 items are
`ok` and `mismatches=0`** — the whole difference is other seats' working-tree writes (§3, §4).

No tool was installed or upgraded (operator directive 2026-10-19); nothing was needed, and no pacman transaction
was attempted (host-wide pause). Host access was read-only.

## 1. Setup and preconditions

- `git -C <lane> rev-parse HEAD` → `075436b1346ca659afb8be7a46f0e67e4170aa83`.
- Between the data commit and HEAD only wave machinery changed:
  `git diff --stat 8524904a 075436b1 -- SCORECARD.md SHONEN.md corpus/QUALITY.md corpus/README.md
  .ufo/waves/round-52/evidence/selftests .ufo/waves/round-52/count-c1.py` → empty. The HEAD delta is
  `build-w1-spec-amend.py`, `w1-spec.json`, `w1-dispatch.json`, `w1-validate*`, `w1/swarm-registry.json`,
  `evidence/c1-at-data.txt`, `evidence/c2-at-data.txt`, `evidence/c2-hashes-at-data.txt`. So the measured surface
  is identical at `8524904a` and at HEAD.
- Frozen bytes intact at measurement time: `sha256sum .ufo/waves/round-52/count-c1.py` →
  `e864922790451b4026be784d5344d9a06827b251ed3c81bfe26b1c559ee3c300`, equal to the `count-c1.py` line of
  `evidence/freeze-sha256.txt`; same agreement for `count-c2.py` (`0a9ec2ff…`) and `contract.md` (`b1ea7b83…`).
  No frozen file was edited.
- The counter's pinned fleet revision `FLEET_REV = f0b61b4ad192bcd95d7a76613a626f71285996ed`
  (`count-c1.py:64`) resolves in the fleet repo: `git -C /home/vgpnk/Projects/shokunin cat-file -t f0b61b4a…` →
  `commit`, `git log -1` → "rounds ledger: chousa r52 closure (admitted) — hyaku, non-author". Every run below
  printed `manifest=6209bdb8e400`, the same tag as both receipts.
- `scripts/hyaku/disk-guard.sh status` before the heavy runs: `/fast/scratch/hyaku` 24 % used, 616.3 G free.

## 2. `--selftest`

```
cd /fast/scratch/hyaku/mori-r52/Mo52ExecC1Replay
export TMPDIR=/fast/scratch/hyaku/mori-r52/Mo52ExecC1Replay/tmp
python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-52/count-c1.py --selftest
```
exit **0**, 1.66 s. 42 `PASS …` lines, 0 `FAIL`, verdict `C1_SELFTEST pass=42 fail=0`.
Agreement: `diff -u` of my output against `evidence/selftest-c1.txt` minus its `$ …` and `exit=` lines → empty
(rc 0), same case list in the same order, same verdict. No non-ok line to paste.

## 3. Data tip, live lane — the seat's literal command

```
cd /fast/scratch/hyaku/mori-r52/Mo52ExecC1Replay
export TMPDIR=/fast/scratch/hyaku/mori-r52/Mo52ExecC1Replay/tmp
python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-52/count-c1.py \
  8524904adb25e44f24d9f25aac7eae909625c18c --scratch /fast/scratch/hyaku/mori-r52/Mo52ExecC1Replay/c1
```
exit **1**, 69.46 s (run window 21:11:55–21:13:04 local). 42 `item` lines, **all `state=ok`, 0 mismatch,
0 error**, and their sorted set is byte-identical to `evidence/c1-at-data.txt` (`diff` rc 0) — including
`item axis operability … got=ok state=ok`, `item axis depth … got=ok state=ok`,
`item pin python3_tools/mori-pin-check.py_--selftest … got=PIN_CHECK_SELFTEST_pass=125_fail=0 state=ok`,
`item pin python3_tools/mori-unlanded-check.py_--selftest … got=UNLANDED_SELFTEST_pass=17_fail=0 state=ok`,
`item locator SCORECARD.md:1781 expect=pair:5_→_6 got=found state=ok`, and the seven living-pin items
(`QUALITY.md:885` superseded, `909` superseded, `1360` ok, `README.md:607` superseded, `608` superseded, `727` ok,
`728` ok). **No item line is non-ok.**

The verdict line differs from the receipt in exactly two fields:

```
C1=unmet items=42 axes=6 pins=2 boxes=4 living=7 superseded=4 locators=27 mismatches=0 errors=1 hidden=0 lane_writes=7 manifest=6209bdb8e400 rev=8524904adb25e44f24d9f25aac7eae909625c18c failed=errors,lane_writes
```

The seven lines the arm read, verbatim:

```
lane_write !! .ufo/waves/round-52/__pycache__/count-c1.cpython-314.pyc
lane_write ?? .ufo/waves/round-52/w1/Mo52ConnSiblings.md
lane_write ?? .ufo/waves/round-52/w1/Mo52CritC2Coverage.md
lane_write ?? .ufo/waves/round-52/w1/Mo52Ent09.md
lane_write ?? .ufo/waves/round-52/w1/Mo52ExecHostCommit.md
lane_write ?? .ufo/waves/round-52/w1/Mo52ExecProseLines.md
lane_write ?? corpus/lessons/round-52.md
```

Provenance from `ls --time-style=full-iso`, inside my run window:

- the five `w1/*.md` files, mtimes 21:11:43–21:12:37: sibling seats publishing reports into the lane (each file's
  header names its seat, e.g. `Mo52ConnSiblings` "sibling-overlap scan for C2");
- `corpus/lessons/round-52.md`, mtime 21:12:15, untracked, header "L1 MoriR52, attempt 1" — the L1's own draft;
- `__pycache__/count-c1.cpython-314.pyc`, mtime 21:11:55.102. Not mine: CPython writes no bytecode for `__main__`,
  and I ran the counter as a script. Verified in scratch: `python3 m.py` → no `__pycache__`; then
  `python3 -c "import m"` → `m.cpython-314.pyc`. The counter's pinned commands cannot produce it either — `run()`
  passes `PYTHONDONTWRITEBYTECODE="1"` (`count-c1.py:545`). So an importing seat produced it; identity UNVERIFIED.
  The same file set and the same 21:11:55 mtime are recorded independently by `w1/Mo52ExecLocatorSweep.md` §7
  item 5, which disclaims it as its own.

Mechanism: `before = status()` once at setup (`count-c1.py:531`), `lane_writes()` once after all four arms
(`:562`), both `git status --porcelain --ignored --untracked-files=all` on `repo` (`:527`); every line that differs
is counted, and any nonzero value adds 1 to `errors` and appends `lane_writes` to `failed` (`:429–439`). Nothing
ties the delta to the counter's own process, and the receipts' runs used `--repo <clone>`, where the arm watches the
clone.

## 4. Data tip, quiescent clone — receipt reproduced exactly

```
git clone --no-local -q <lane> /fast/scratch/hyaku/mori-r52/Mo52ExecC1Replay/clone-c1
git -C …/clone-c1 rev-parse --show-toplevel   → /fast/scratch/hyaku/mori-r52/Mo52ExecC1Replay/clone-c1
python3 …/count-c1.py 8524904adb25e44f24d9f25aac7eae909625c18c \
  --repo /fast/scratch/hyaku/mori-r52/Mo52ExecC1Replay/clone-c1 \
  --fleet-repo /home/vgpnk/Projects/shokunin --scratch /fast/scratch/hyaku/mori-r52/Mo52ExecC1Replay/c1q
```
exit **0**, 70.70 s:

```
C1=met items=42 axes=6 pins=2 boxes=4 living=7 superseded=4 locators=27 mismatches=0 errors=0 hidden=0 lane_writes=0 manifest=6209bdb8e400 rev=8524904adb25e44f24d9f25aac7eae909625c18c
```

Byte-identical to the receipt's verdict line; the 42 `item` lines are byte-identical to the receipt's too (`diff`
rc 0). The only variable between §3 and §4 is which repo `status()` samples.

## 5. Do-nothing control at the entering tip

```
python3 …/count-c1.py 4f266ef2fdf74d8b046f5b4f5a5c4945f65b966d \
  --scratch /fast/scratch/hyaku/mori-r52/Mo52ExecC1Replay/c0
```
exit **1**, 18.69 s (run window 21:13:22–21:13:41): 37 items, `axes=6 pins=2 boxes=4 living=4 superseded=1
locators=25 mismatches=8` — every count equal to the receipt, and all 37 `item` lines byte-identical (`diff` rc 0).
The eight non-ok items, verbatim:

```
item axis operability expect=round_51_improved got=round=47,evidence_missing:corpus/lessons/round-51-verifier-spotcheck.md state=mismatch
item axis depth expect=round_51_improved got=round=50,evidence_missing:corpus/lessons/round-51-verifier-spotcheck.md state=mismatch
item pin python3_tools/mori-pin-check.py_--selftest expect=(125/125) got=PIN_CHECK_SELFTEST_pass=125_fail=0_receipt_missing state=mismatch
item pin python3_tools/mori-unlanded-check.py_--selftest expect=(17/17) got=UNLANDED_SELFTEST_pass=17_fail=0_receipt_missing state=mismatch
item living corpus/QUALITY.md:909 expect=pass=12_fail=0 got=MORI_SOURCES_APPENDONLY_SELFTEST_pass=22_fail=0_rc=0 state=mismatch
item living corpus/README.md:607 expect=pass=9_fail=0 got=unrunnable state=mismatch
item living corpus/README.md:608 expect=pass=12_fail=0 got=MORI_SOURCES_APPENDONLY_SELFTEST_pass=22_fail=0_rc=0 state=mismatch
item locator SCORECARD.md:1771 expect=pair:5_→_6 got=absent state=mismatch
```

Verdict divergence (everything else identical):

```
receipt: C1=unmet items=37 … mismatches=8 errors=0 hidden=0 lane_writes=0 … failed=mismatch
mine:    C1=unmet items=37 … mismatches=8 errors=1 hidden=0 lane_writes=3 … failed=errors,lane_writes,mismatch
```

The three lane lines, again external:

```
lane_write ?? .ufo/waves/round-39/scratch/mori-conform-selftest-y3fmjwhy/counter-predicate.py
lane_write ?? .ufo/waves/round-52/w1/Mo52Ent05.md
lane_write ?? .ufo/waves/round-52/w1/Mo52Ent07.md
```

`mori-conform-selftest-y3fmjwhy` was one of four such children created in the lane at 21:13:54–21:14:02 and
removed by their owners' `finally`; the `w1/*` files are sibling reports. This control runs no
round-39 conform pin (its living set at `4f266ef2` is `QUALITY.md:885` superseded, `909`, `README.md:607`, `608`),
so none of the three came from it. The receipt read `lane_writes=0` because it was taken with `--repo` on
`clone-do-nothing`.

## 6. Independent checks (not the counter)

1. **Score column vs newest closure.** `corpus/lessons/round-51-verifier-spotcheck.md:130–135` states operability 7,
   depth 5, coverage 6, freshness 5, calibration 5, adjacency 6. The live `## Axes` table (`SCORECARD.md:10–15`)
   holds the same six integers. Agrees.
2. **`N*` per axis.** Fleet MANIFEST at `f0b61b4a`, mori rounds: 48, 49, 50 admitted with calibration `improved`;
   51 admitted with operability `improved` and depth `improved`, the rest `unchanged`. Highest admitted round ≤ 51
   recording an improvement: operability 51, depth 51, calibration 50, coverage 47, freshness 28, adjacency 19 —
   exactly the rounds the six Last-change cells now lead with. Agrees.
3. **Locator repair.** `git diff 4f266ef2 8524904 -- SCORECARD.md` is exactly three changed lines: the operability
   and depth Last-change cells, and the freshness cell's pointer `SCORECARD.md:1771` → `:1781`. `sed -n '1781p'
   SCORECARD.md` is the round-28 measured-outcome row ending "freshness 5 → 6 proposed", so the `5 → 6` the cell
   quotes is on that line.
4. **Living pins.** `corpus/QUALITY.md` gains criteria 141–142 (141 supersedes "112's check cell only" and records
   the stale `pass=12` vs today's 22; 142 states the pointer property with its `Shown able to fail` receipt);
   `corpus/README.md` gains "Round-52 corrections (living pins)" with one-line supersession bullets. The gate those
   bullets quote prints today what they say — `MORI_SOURCES_APPENDONLY_SELFTEST pass=22 fail=0`, observed by my own
   living arm at both revisions — against `pass=12` at `QUALITY.md:909` / `README.md:608`.
5. **SHONEN.** `git diff 4f266ef2 8524904 -- SHONEN.md` → empty; `git show 8524904:SHONEN.md | sed -n '7p'` still
   reads "receipts `.ufo/waves/round-51/evidence/selftests/mori-pin-check.txt`, `.ufo/waves/round-51/evidence/selftests/mori-unlanded-check.txt`".
   What the data commit added is `.ufo/waves/round-52/evidence/selftests/{mori-pin-check,mori-unlanded-check}.txt`
   (absent at the entering tip), holding `PIN_CHECK_SELFTEST pass=125 fail=0` and `UNLANDED_SELFTEST pass=17 fail=0`
   with a literal command line each (`$ cd <lane checkout at d3a8ea5957b7…> && python3 tools/mori-pin-check.py --selftest`).

## 7. Scratch and hygiene

- All work under `/fast/scratch/hyaku/mori-r52/Mo52ExecC1Replay/` (`tmp/`, `c1/`, `c0/`, `c1q/`, `clone-c1/`,
  `pyctest/`), `TMPDIR` set there, one `--no-local` clone with `rev-parse --show-toplevel` asserted equal to the
  clone path. Removed with `rm -rf` at the end of the seat.
- No git/jj mutation anywhere: only `log`, `show`, `diff`, `rev-parse`, `cat-file`, `ls-tree`, `check-ignore`,
  `archive`-via-counter and `clone FROM` the lane. No write to the lane, the fleet root, `~/.local/bin` or any PATH
  directory; my only written path is this report.
- Lane writes I caused: none. The `lane_write` lines reported in §3/§5 are other seats' files and were not created
  by me; my script runs produced no bytecode (§3).
- No credential material, session token or private URL appears in this report; no host fact beyond disk free space
  is reported.

## Findings

1. **MED — `lane_writes` is not isolated from concurrent lane activity, and it flips a correct measurement to
   `C1=unmet`.** `count-c1.py:527,531,562` (baseline and final `git status --porcelain --ignored
   --untracked-files=all` on `repo`, delta counted, `:429–439` adds to `errors`/`failed`). Evidence §3: 42/42 items
   `ok`, `mismatches=0`, yet `errors=1 lane_writes=7 failed=errors,lane_writes` from five sibling reports, the L1's
   untracked `corpus/lessons/round-52.md`, and one imported-module `.pyc`. Consequence: an at-landed reading taken
   while anything else writes the lane (a 68-seat wave writes its reports into `.ufo/waves/round-52/w1/`) fires
   `contract.md` "Kill rule: C1=unmet at the landed tip → C1 not verified" although no arm failed. It reads `met`
   on a quiescent clone (§4) and on the live lane once the wave is committed and the tree is clean; the contract's
   "Named limits" cover only *visibility* of ignored paths, not concurrency. Route: round 53 (scope the arm to paths
   its pinned commands can touch, or freeze "measured with `repo` = a quiescent clone at R" as the instrument's mode
   and record that mode in every receipt). No counter change is proposed as a fix for this round.
2. **MED — the counter's own living arm runs a lane-writing instrument, and the arm cannot see its own transient
   write.** `corpus/README.md:728`'s runnable replacement pins `.ufo/waves/round-39/conform.py <rev> --selftest`;
   that file hardcodes `LANE = "/home/vgpnk/Projects/shokunin/mori-shokunin"` (`.ufo/waves/round-39/conform.py:53`)
   and `SCRATCH_ROOT = os.path.join(LANE, ".ufo","waves","round-39","scratch")` (`:54`), then
   `os.makedirs(SCRATCH_ROOT)` + `tempfile.mkdtemp(…, dir=SCRATCH_ROOT)` (`:491–492`) with `shutil.rmtree(work)`
   only (`:512`). So every run of that pin creates and removes a `mori-conform-selftest-*` directory **inside the
   lane**; the status sample runs after the arms finish (`count-c1.py:562`), so it cannot see the transient child,
   but residue from a killed or timed-out pin persists and makes every later run read `lane_writes>0` — the counter
   could poison its own verdict. Lane evidence: `.ufo/waves/round-39/scratch/` is untracked with `Birth
   2026-10-24 01:26` (pre-existing; this wave did not create the parent) and held 3–4 live
   `mori-conform-selftest-*` children at 21:15:31–21:15:37, removed within seconds; the wave's in-lane-writer
   inventory seat is chartered (`w1-spec.json`) to run exactly these `--selftest` forms from an archive, which still
   writes to the absolute lane path. Whether either of my two runs created a transient child is UNVERIFIED (gone
   before the sample, parent predates the run); the mechanism is verified from source. `count-c1.py`'s own children
   are protected by `PYTHONDONTWRITEBYTECODE="1"` (`:545`); this one is not. Route: round 53.
3. **MED — SHONEN.md's receipt pointer is still the round-51 one, while the arm that closed those two pins reads a
   path the document never names.** `SHONEN.md:7` (byte-identical at `4f266ef2` and `8524904`) names
   `.ufo/waves/round-51/evidence/selftests/…`; the closing evidence is
   `.ufo/waves/round-52/evidence/selftests/{mori-pin-check,mori-unlanded-check}.txt`, which no line of SHONEN.md
   references, and `count-c1.py`'s arm (B) hardcodes the round-52 path. P-C1 as frozen is met; the claim's own
   property ("agrees with … its own pointers") is not established for these two rows, and the asymmetry with arm
   (C) — which does require the supersession text to name the replacement — is unrecorded. Route: round 53; for
   round 52 the L1 may correct the SHONEN data (one appended line naming the round-52 receipts) or this gap stands
   in the closure.
4. **LOW — the two round-52 selftest receipts name the freeze revision, not the measured R, and use a placeholder
   checkout path.** `.ufo/waves/round-52/evidence/selftests/mori-pin-check.txt:1` and
   `…/mori-unlanded-check.txt:1` carry `$ cd <lane checkout at d3a8ea5957b7…> && python3 tools/… --selftest`.
   Arm (B) passes on the observed line alone, so nothing is wrong numerically (my runs read
   `PIN_CHECK_SELFTEST_pass=125_fail=0`, `UNLANDED_SELFTEST_pass=17_fail=0` at R, state=ok), but the receipt does
   not state which revision's bytes produced 125/17.
5. **LOW — the `--scratch` guard is an ancestor test only, and pinned commands inherit the lane as their effective
   write target.** `count-c1.py:505` (`os.path.commonpath([base, repo]) == repo`) rejects only a scratch inside the
   lane; finding 2 shows the practical consequence, since `TMPDIR` is redirected (`:545`) but absolute paths inside
   the pinned instruments are not. Recorded because findings 2 and 5 compound; no fix is proposed for this round.
