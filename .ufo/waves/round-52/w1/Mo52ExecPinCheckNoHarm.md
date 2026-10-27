# Mo52ExecPinCheckNoHarm — operability no-harm: registry pin re-measure and unlanded check at R52

Seat: executor, mori-shokunin round 52 wave w1. Lane repo `/home/vgpnk/Projects/shokunin/mori-shokunin`
(read-only), measured revision `8524904adb25e44f24d9f25aac7eae909625c18c` (round-52 data), comparison
revision `70e68cdd28c44a95039b9175a947e15664618351` (round-51 landed tip).
Scratch: `/fast/scratch/hyaku/mori-r52/Mo52ExecPinCheckNoHarm/` (created, used, removed at end).
No credential material read; machine id not needed.

## 1. Commands actually run (literal)

All three pin-check runs were executed with cwd `/fast/scratch/hyaku/mori-r52/Mo52ExecPinCheckNoHarm`,
`TMPDIR=/fast/scratch/hyaku/mori-r52/Mo52ExecPinCheckNoHarm/tmp`, and an explicit `--scratch`:

```
python3 /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-pin-check.py \
  --rev 8524904adb25e44f24d9f25aac7eae909625c18c \
  --repo /home/vgpnk/Projects/shokunin/mori-shokunin \
  --scratch /fast/scratch/hyaku/mori-r52/Mo52ExecPinCheckNoHarm/pc
EXIT=0   (91.19 s)

python3 /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-pin-check.py \
  --rev 70e68cdd28c44a95039b9175a947e15664618351 \
  --repo /home/vgpnk/Projects/shokunin/mori-shokunin \
  --baseline-rev 70e68cdd28c44a95039b9175a947e15664618351 \
  --scratch /fast/scratch/hyaku/mori-r52/Mo52ExecPinCheckNoHarm/pc-r51
EXIT=0   (89.34 s)

python3 /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-pin-check.py \
  --rev 8524904adb25e44f24d9f25aac7eae909625c18c \
  --repo /home/vgpnk/Projects/shokunin/mori-shokunin \
  --baseline-rev 70e68cdd28c44a95039b9175a947e15664618351 \
  --scratch /fast/scratch/hyaku/mori-r52/Mo52ExecPinCheckNoHarm/pc-bl
EXIT=0   (90.90 s)

python3 /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-unlanded-check.py \
  --repo /home/vgpnk/Projects/shokunin/mori-shokunin --round 52
EXIT=1
```

`--help` was read first for both tools (`mori-pin-check.py`: `--rev|--root`, `--repo`, `--skill`,
`--min-tally-pins`, `--baseline-rev`, `--timeout`, `--scratch`, `--selftest`;
`mori-unlanded-check.py`: `--repo DIR --round N | --selftest`).
Pins, predicates, counters, controls and kill rules were not touched; no file outside this report was
written in the lane.

## 2. Pin verdict at R52 (the assignment's exact command)

Last line of the first run, verbatim:

```
PIN_CHECK=met tally_pins=36 digest_pins=8 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=8524904adb25e44f24d9f25aac7eae909625c18c baseline=no env=0 stale=0
```

46 pin lines, all `state=match` (36 tally, 8 digest, 2 line-count); strict filter
`grep '^pin ' out | grep -v state=match` → empty. Selected lines (first and last of the run):

```
pin line=166 kind=tally prefix=MORI_SILENCE_CASES_SELFTEST state=match pinned='pass=24 fail=0' observed='pass=24 fail=0' rc=0 cmd='bash tools/mori-silence-cases.sh --selftest'
pin line=938 kind=tally prefix=PIN_CHECK_SELFTEST state=match pinned='pass=125 fail=0' observed='pass=125 fail=0' rc=0 cmd='python3 tools/mori-pin-check.py --selftest'
pin line=1113 kind=tally prefix=C2_SELFTEST state=match pinned='pass=34 fail=0' observed='pass=34 fail=0' rc=0 cmd='python3 .ufo/waves/round-51/count-c2.py --selftest'
```

## 3. Comparison with round 51 — no pin changed state

(a) Registry bytes. `git rev-parse 70e68cdd:SKILL.md` and `git rev-parse 8524904a:SKILL.md` both print
`dcc1fdd07c104a8e20c7e4426079901d80879337`; `git diff 70e68cdd 8524904a -- SKILL.md` is empty. No pin row,
prefix, pinned text or bound command changed between the two revisions.

(b) Instruments. `git diff --name-only 70e68cdd 8524904a` lists 38 paths: the round-52 contract/counters/
controls/evidence under `.ufo/waves/round-52/`, three round-51 evidence receipts, `SCORECARD.md`,
`SHONEN.md`, `corpus/QUALITY.md`, `corpus/README.md`, `corpus/SOURCES.md`, the five
`corpus/evidence/sources-r52/*`, the new knowledge entry and `corpus/lessons/round-51-verifier-spotcheck.md`.
No `tools/` file and no `.ufo/waves/round-38…51` instrument changed.

(c) Measured baseline. The same command at `70e68cdd` (round-51 landed tip) prints

```
PIN_CHECK=met tally_pins=36 digest_pins=8 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=70e68cdd28c44a95039b9175a947e15664618351 baseline=yes env=0 stale=0
```

(d) Per-pin diff, `diff <(grep '^pin ' r51.out) <(grep '^pin ' r52.out)` — the only differing lines are the
two pins whose command substitutes the measured revision; their state and observed text are identical:

```
< pin line=911 kind=tally prefix=CONFORM_SELFTEST state=match pinned='pass=11 fail=0' observed='pass=11 fail=0' rc=0 cmd='python3 .ufo/waves/round-40/conform.py 70e68cdd28c44a95039b9175a947e15664618351 --selftest'
> pin line=911 kind=tally prefix=CONFORM_SELFTEST state=match pinned='pass=11 fail=0' observed='pass=11 fail=0' rc=0 cmd='python3 .ufo/waves/round-40/conform.py 8524904adb25e44f24d9f25aac7eae909625c18c --selftest'
< pin line=912 kind=tally prefix=MORI_SOURCES_APPENDONLY_SELFTEST state=match pinned='pass=22 fail=0' observed='pass=22 fail=0' rc=0 cmd='python3 tools/mori-sources-appendonly.py 70e68cdd28c44a95039b9175a947e15664618351 --selftest'
> pin line=912 kind=tally prefix=MORI_SOURCES_APPENDONLY_SELFTEST state=match pinned='pass=22 fail=0' observed='pass=22 fail=0' rc=0 cmd='python3 tools/mori-sources-appendonly.py 8524904adb25e44f24d9f25aac7eae909625c18c --selftest'
```

(e) Baseline-keyed run at R52 (`--baseline-rev 70e68cdd…`):

```
PIN_CHECK=met tally_pins=36 digest_pins=8 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=8524904adb25e44f24d9f25aac7eae909625c18c baseline=yes env=0 stale=0
```

`dropped=0` and `rebound=0` at R against round 51: no pin key disappeared and no bound argv moved.

**Answer to the seat question: no pin changed state since round 51. 36 tally pins + 8 digest pins, all
`match`, at both revisions; the verdict is `met`, exit 0, at R52.**

### The cited round-51 receipt line

The seat spec cites `.ufo/waves/round-51/evidence/c1-at-landed.txt` as
`PIN_CHECK=met tally_pins=36 …`. That file (10 lines) contains no such line. Its two relevant lines are:

```
classified: PIN_CHECK=unmet tally_pins=5 digest_pins=0 mismatches=4 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=- baseline=no env=2 stale=2
C1=met kill_residue=0 relocated=met reloc_mismatch=0 classified=ok selftest=pass=125,fail=0 rev=70e68cdd28c44a95039b9175a947e15664618351 failed=-
```

The first is round-51 counter arm C measuring the frozen 5-pin fixture registry (ENVA/ENVB/STLA/STLB/OKAY),
not the lane's `SKILL.md`; the round-51 pin evidence is arm B's `relocated=met` (pin-check exit 0 with the
last line starting `PIN_CHECK=met` under bubblewrap), and no tally count is recorded there. A repo-wide
search for `tally_pins=36` under `.ufo/waves/round-5*/` before my runs returned nothing. The nearest
landed receipts with a count are round 50 (`bae8656e…`, `tally_pins=35 digest_pins=8`, met) and round 47
(`af2250d8…`, `tally_pins=28 digest_pins=5`, met); `git diff bae8656e 70e68cdd -- SKILL.md` (+75/−1) adds the
round-51 counter's tally row (`.ufo/waves/round-51/count-c2.py --selftest`, `C2_SELFTEST pass=34 fail=0`) and
moves `PIN_CHECK_SELFTEST` from `pass=114` to `pass=125`, which accounts for 35 → 36. So the value 36 in the
wave spec is correct but its citation is wrong. My measured round-51 baseline (36, met) matches
that number, so the comparison the seat asked for is not compromised.

## 4. Unlanded check, round 52

```
UNLANDED=dirty round=52 paths=30
unlanded ?? .ufo/waves/round-52/check-history-rows.py
unlanded ?? .ufo/waves/round-52/evidence/m2-history-rows.txt
unlanded ?? .ufo/waves/round-52/w1.ready
unlanded ?? .ufo/waves/round-52/w1.ready.partial
unlanded ?? .ufo/waves/round-52/w1/Mo52ConnSiblings.md
unlanded ?? .ufo/waves/round-52/w1/Mo52CritC1Scope.md
unlanded ?? .ufo/waves/round-52/w1/Mo52CritC2Coverage.md
unlanded ?? .ufo/waves/round-52/w1/Mo52CritC2Prose.md
unlanded ?? .ufo/waves/round-52/w1/Mo52CritC2Voters.md
unlanded ?? .ufo/waves/round-52/w1/Mo52Ent02.md
unlanded ?? .ufo/waves/round-52/w1/Mo52Ent04.md
unlanded ?? .ufo/waves/round-52/w1/Mo52Ent05.md
unlanded ?? .ufo/waves/round-52/w1/Mo52Ent06.md
unlanded ?? .ufo/waves/round-52/w1/Mo52Ent07.md
unlanded ?? .ufo/waves/round-52/w1/Mo52Ent08.md
unlanded ?? .ufo/waves/round-52/w1/Mo52Ent09.md
unlanded ?? .ufo/waves/round-52/w1/Mo52Ent10.md
unlanded ?? .ufo/waves/round-52/w1/Mo52Ent12.md
unlanded ?? .ufo/waves/round-52/w1/Mo52ExecAnchorCheck.md
unlanded ?? .ufo/waves/round-52/w1/Mo52ExecBatchDeviation.md
unlanded ?? .ufo/waves/round-52/w1/Mo52ExecC2Replay.md
unlanded ?? .ufo/waves/round-52/w1/Mo52ExecHostCommit.md
unlanded ?? .ufo/waves/round-52/w1/Mo52ExecLocatorSweep.md
unlanded ?? .ufo/waves/round-52/w1/Mo52ExecProseLines.md
unlanded ?? .ufo/waves/round-52/w1/Mo52MutC2Arm.md
unlanded ?? .ufo/waves/round-52/w1/Mo52MutC2Entry.md
unlanded ?? .ufo/waves/round-52/w1/Mo52RevSourcesRows.md
unlanded ?? .ufo/waves/round-52/w1/Mo52ScribeErratum51.md
unlanded ?? .ufo/waves/round-52/w1/Mo52SentBoundary.md
unlanded ?? corpus/lessons/round-52.md
```

Exit 1. Every listed path is `??` (untracked); `git status --porcelain -uall | grep -vc '^??'` = 0, i.e.
no tracked file is modified, staged or deleted, and the data commit's bytes are what the pin-check measured.
This is the expected mid-wave state (seat reports and wave markers are written before the L1 integrates);
it is not a claim defect, but the same command must read `UNLANDED=clean round=52` in the L1's round-end
receipt, and the file `w1.ready.partial` still present at 21:20 is a superseded dispatch marker
(`w1.ready.dispatched` also exists, 54 files in `w1/` at that time).

## 5. Side effects of my runs

- `--scratch` held only the clone: `pc/`, `pc-r51/`, `pc-bl/` were empty after each exit (the tool removes
  its `git clone --shared` tree), `tmp/` empty. Scratch total 3.2 MB, all my own output captures; removed.
- Lane working tree: two `git status --porcelain=v1 --ignored --untracked-files=all` snapshots taken
  during and after the first run (10,418 then 10,389 entries) differ by 36 removals and 7 additions, all of
  them other seats' paths: 35 removed `.ufo/waves/round-38/scratch/mori-conform-selftest-*` and
  `round-39/scratch/.../counter-*.py` files plus `w1.ready.partial`; added
  `round-39/scratch/mori-conform-selftest-wp9_ix72/counter-{bounded_reads,drain_shape,timeout_state,timeout_value}.py`,
  `w1.ready.dispatched`, `w1/Mo52Ent01.md`, `w1/Mo52ScribeSkill.md`. None of my four commands names any of those paths, and no pinned command
  in the R52 registry contains the lane's absolute path
  (`grep -l "/home/vgpnk/Projects/shokunin/mori-shokunin"` over all 16 pinned instruments and
  `.ufo/waves/round-40/conform.py` → no match), so the churn is concurrent-seat activity, not mine.
  The only lane path I wrote is this report.
- Host: reads only. Disk guard before and after: `/fast/scratch/hyaku` 26 %, 599–600 GB free, no ENOSPC.
  No pacman, no tool installs, no sysctl/cgroup/swap writes, no process kills, no kernel-log message reads.

## 6. Observed in-lane writer (item-8 evidence, detection only)

`.ufo/waves/round-39/conform.py:53` `LANE = "/home/vgpnk/Projects/shokunin/mori-shokunin"`,
`:54` `SCRATCH_ROOT = os.path.join(LANE, ".ufo", "waves", "round-39", "scratch")`, `:491` `os.makedirs(SCRATCH_ROOT, exist_ok=True)`,
`:492` `work = tempfile.mkdtemp(prefix="mori-conform-selftest-", dir=SCRATCH_ROOT)`; the round-38 file has the
same shape at `:37`/`:38`. Any run of either selftest, from any cwd, writes untracked scratch into the lane.
Live evidence during this wave: `.ufo/waves/round-39/scratch/` held
`mori-conform-selftest-{7fvv2sy5,bjpxq0ox,f0pm0tes}` at 21:18:54–21:19:05 and
`mori-conform-selftest-{4zqojen3,90ok9tm5,p0f7p3jy}` at 21:21:37–21:22:00, while I ran nothing after 21:21.
The pinned registry does not use these two files (the pinned conform is round 40, whose
`SCRATCH_ROOT = tempfile.gettempdir()`), so pin-check is not the writer. Attribution to a specific seat is
UNVERIFIED (no process inspection performed).

## 7. Named limits of this seat's evidence

- Pins measured, not audited: 46 `match` lines prove the pinned instruments print today's pinned text at R,
  not that their arms are good (contract C1 named limit).
- The lane working tree was dirty (30 untracked wave paths) throughout; the pin-check `--rev` mode measured
  committed bytes of R, so the untracked reports did not enter any measurement — but the `--root`-mode
  question ("would the pins pass on the current working tree?") was not asked.
- `/var/tmp/pin-check-*/tree` (four 333 MB exports at 21:18:20–35, replaced by four new names at 21:22) are
  other seats' concurrent `--rev` runs without an explicit `--scratch` (default `$TMPDIR` else `/var/tmp`);
  they rotated between snapshots, so no leak is established here — the documented v5 behaviour (a SIGKILLed
  run leaves its 333 MB tree in scratch) is a risk, not an observation of this seat.
- Two snapshots 4 minutes apart cannot bound lane churn; I did not instrument the lane for write notifications.

## Findings

- **MED — cited round-51 baseline line does not exist.** `.ufo/waves/round-51/evidence/c1-at-landed.txt`
  (rows 7 and 9) holds the arm-C fixture line `classified: PIN_CHECK=unmet tally_pins=5 … env=2 stale=2` and
  `C1=met … relocated=met`, not `PIN_CHECK=met tally_pins=36 …` as the wave spec states. The number is right
  (36 measured at `70e68cdd` in §3c) but not reproducible from the cited receipt; a reader can only rebuild
  the baseline by re-measuring. Concerns the wave spec text, not data.
- **MED — frozen round-38/round-39 `conform.py` write selftest scratch into the lane.**
  `.ufo/waves/round-39/conform.py:53-54,491-492` and `.ufo/waves/round-38/conform.py:37-38` hardcode
  `LANE` and `mkdtemp(dir=SCRATCH_ROOT)` under it; live `round-39/scratch/mori-conform-selftest-*` dirs were
  created/rotated in the lane at 21:18:54–21:22:00 during this wave. This is the round-52 contract item-8
  in-lane-writer class and is a routed item for round 53; the fix must not be an in-place edit of the frozen
  files (closure item 6).
- **LOW — wave work unlanded at measurement time.** `UNLANDED=dirty round=52 paths=30`, exit 1: 28 round-52
  wave paths plus `corpus/lessons/round-52.md` and `.ufo/waves/round-52/check-history-rows.py`
  (`evidence/m2-history-rows.txt`). Expected mid-wave; the L1 round-end receipt must show
  `UNLANDED=clean round=52`.
- **LOW — lane working tree carries 10,389–10,418 ignored+untracked entries**, dominated by pre-existing
  `.ufo/waves/round-38..40/scratch/` selftest residue from earlier rounds; between two snapshots taken during
  this wave, 36 such paths were removed and 7 added by concurrent seats (35 of the removals and 4 of the
  additions were round-38/39 scratch files). Noise for `git status`-based operability tools
  (`mori-unlanded-check.py` excludes only `.scratch/`); not caused by this seat.
- **LOW — four concurrent `--rev` runs exported 333 MB trees into `/var/tmp`** (`pin-check-8elekn17`,
  `-fzczggkj`, `-koenmuev`, `-nxi7_99u` at 21:22, earlier `-0cvi_kq9`, `-2852ne28`, `-_gmeki7b`,
  `-oavelxhu` at 21:18) because the default scratch is `$TMPDIR`/`/var/tmp`; ~1.3 GB transient host usage,
  and a SIGKILLed run leaks one tree. `mori-pin-check.py` docstring v5 documents the leak; seats should pass
  `--scratch` under their own directory (this seat did, so none of those eight are mine).
