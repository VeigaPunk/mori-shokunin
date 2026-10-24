# CriticHarmAxes — round 24 wave 2: no harm to held axes

Seat: `MoriR24.CriticHarmAxes` (critic, read-only leaf, no subagent dispatch).
Attacked claim: operability 7, depth 5, freshness 5 and adjacency 6 are held (not harmed) by
`c725aa37aa3c9ec4f34e3c2abc8ca1b616c7c130..a730ecfefbdb5c31b1db13aca2c40eecd5e97abc`
(`contract.md:107`, `SCORECARD.md` round-24 declaration "Held and observed").
Scratch: `/fast/scratch/hyaku/mori-r24-a2/w2/CriticHarmAxes/` (two `--no-hardlinks` clones,
`c725aa37/` and `a730ecfe/`, plus `out/` and `tmp/`). Nothing was pushed; the lane repo, its index
and its jj state were only read.

## Verdict

**Survivor, with one adjacency defect that can be fixed.** I found no broken pointer, no changed
tool, census or pinned baseline, and no rewritten earlier row. Every pre-existing selftest gives
the same result at both commits. One adjacency gap remains: a wave-1 finding was not carried into
the landed bytes (A1 below). It does not move any pointer, but it leaves a shared surface
undisclosed. A2 is a recorded wording risk only.

## Evidence by surface

### 1. Additions only; no earlier row rewritten

- `git diff --numstat c725aa37..a730ecf` gives 57 files, `+12488 -0`, so the range deletes zero
  lines. In plain words: no line that existed at `c725aa37` was changed or removed.
- Outside `.ufo`, there are 7 modified files and 5 added files. 6 of the 7 modified files are pure
  end-of-file appends (`git diff -U0` hunk headers):
  `LOG.md @@ -1764,0`, `PROVINCE.md @@ -232,0`, `SCORECARD.md @@ -1492,0`, `SKILL.md @@ -609,0`,
  `corpus/QUALITY.md @@ -306,0`, `corpus/README.md @@ -443,0`. In each case the old line count
  equals the hunk start (for example, `PROVINCE.md` old=232, new=285).
- `git diff --name-only c725aa37..a730ecf -- .ufo | rg -v '^\.ufo/waves/round-24/'` prints
  nothing, so no earlier round's frozen file, evidence or register changed.
- Two lines were rewritten inside the round, both in `a730ecf` ("S090 wording correction"): the
  S090 row (`corpus/SOURCES.md:96`) and one line of `corpus/knowledge/system-pressure-r24.md`. Both
  were created earlier in this same round (`df4db54`), so this is not a rewrite of a pre-round row.

### 2. Sibling-facing `PROVINCE.md` ranges (adjacency)

- `git show <c>:PROVINCE.md | head -n 232 | sha256sum`: `12e5cb234530a980…` at both `c725aa37`
  and `a730ecf`. The whole file at `c725aa37` has the same hash, so lines 1–232 are byte-identical.
- `diff <(git show c725aa37:PROVINCE.md | sed -n 3,16p) <(git show a730ecf:PROVINCE.md | sed -n 3,16p)`
  prints `identical`. The anchors still sit where tsukuroi points: line 3 is
  `**Domain:** fleet & host observability`, line 6 is `**Owns (read-only probes):**`, line 12 is
  `**Refuses:** dispatch and orchestration mechanism`, and line 16 is
  `**Detection and report only — never remediation.**`.
- These tsukuroi pointers all fall inside the unchanged lines 1–232:
  - `../mori-shokunin/PROVINCE.md:3-16` (`tsukuroi-shokunin/PROVINCE.md:49` ADJ-04;
    `corpus/knowledge/adjacency-handoffs-fleet-r1.md:52`; `adjacency-anchors-r19.md:85`)
  - `:12-16` (`adjacency-handoffs-fleet-r1.md:53`; `adjacency-anchors-r19.md:87`)
  - `:6-16` (`tsukuroi-shokunin/PROVINCE.md:33`; `adjacency-anchors-r19.md:81`)
  - the inbound ranges `:1-33`, `:3-33`, `:35-74`, `:38-42`, `:49` (`adjacency-anchors-r19.md:143-155`)

  Some of those historical inbound ranges had already drifted in earlier rounds. For example, line
  49 now holds FR6, and `git log -- PROVINCE.md` shows edits in `0d8f2d5` and `8cb4afb`. That drift
  predates round 24.
- Whole-file pin: tsukuroi's `aac98b22…` pin (`adjacency-handoffs-fleet-r1.json:11,24`) matches
  only mori commit `27acf40c`. It already failed at `c725aa37` (whole-file `12e5cb23…`), so the
  round-24 hash `e6bb37a5…` changes nothing for that pin.
- I searched the fleet for pointers into mori `PROVINCE`, `SKILL`, `SCORECARD`, `LOG`, `corpus/*`
  and `tools/*` with line numbers (`rg … -e 'mori(-shokunin)?/(PROVINCE|SKILL|SCORECARD|LOG)\.md:[0-9]' …`,
  outside mori). There were no hits beyond the tsukuroi pointers above, which use the `../mori-shokunin/` form.

### 3. The `corpus/SOURCES.md` mid-file insert (the only non-append change)

- Hunks `@@ -95,0 +96,8 @@` (rows S090–S097) and `@@ -103,0 +112 @@` (one Paths line) shift every
  later line by +8 or +9. This covers `## Paths`, `## Search log` and `## Leads`.
- Live pointers resolved against the tip: `git grep -nE 'SOURCES\.md:[0-9]+' a730ecf -- ':!.ufo'`
  finds only `PROVINCE.md:54-57` and `corpus/README.md:342-345`, which point to lines 7–8, 11–12,
  16, 20–21, 23–26 and 28–32. All of those are above the insert, so none of them moved.
- Pointers at or below the insert (`SOURCES.md:98`, `:100`, `:113-119`, `:132`, `:137`) exist only
  in earlier rounds' `.ufo/waves/round-*/falsify/*.md` and round-24 w1 reports. They cite the tip
  of their own round, and the registry table convention adds rows in place: round 23 did the same
  (`round-23/falsify/ReviewRegistryDelta.md:47-48`). **No harm.**

### 4. Existing tools, census and pinned baselines (operability)

- Blob identity: for every one of the 21 paths under `tools/` at `c725aa37`,
  `git rev-parse c725aa37:$f` equals `git rev-parse a730ecf:$f`. Result: `checked 21 files`, with
  0 `CHANGED`. Round 24 only adds `tools/mori-pressure.py`, `tools/mori-routed-check.py` and
  `tools/fixtures/mori-pressure/cases.json`.
- Census bytes: `sha256(a730ecf:tools/mori-census.sh)` is
  `87b8d680b9b2572e89977a10ff9b91630fbaf689f23f4892e06be427b977ab28`, which equals the wave-1
  pinned digest (`w1/CensusNoHarmBaseline.md:40,120`).
- Census selftest, run in each clone with `TMPDIR=<scratch>/tmp bash tools/mori-census.sh --selftest`:
  exit 0 and `MORI_CENSUS_SELFTEST: PASS (134 cases, 134 passed, 0 failed)` at both commits. The
  stdout sha256 is `a67a336bf02cb9d88453917a7ed53d1aec673a76e8c85f7016051d449554777f` at both,
  which equals the wave-1 pin (`CensusNoHarmBaseline.md:62`).
- Pre-existing selftests, run at both commits. Indirect harm (an old tool globbing `tools/` or
  `corpus/` and reacting to the new files) would show up here as a difference:

| tool (`--selftest` unless noted) | c725aa37 | a730ecf |
|---|---|---|
| `mori-silence-cases.sh tools/mori-census.sh` | exit 0, `matched=28 total=28` | same |
| `mori-content-review.py` (TMPDIR=`<clone>/.scratch`) | exit 0, `CONTENT_REVIEW_SELFTEST_CLEAN` | same |
| `mori-dispatch-ledger.py` | exit 0, `PASS 14/14` | same |
| `mori-evidence-loss.py` | exit 0, `checks 114, failures []` | same |
| `mori-freeze-order.py` (TMPDIR=`<clone>/.scratch`) | exit 0, `PASS 12/12` | same |
| `mori-journal-window.py` | exit 0, `16/16` | same |
| `mori-misroot-sweep.py` | exit 0, `MORI_MISROOT_SELFTEST_OK` (12 arms) | same |
| `mori-retention-gate.py` (TMPDIR=`<clone>/.scratch`) | exit 0, `PASS 21/21` | same |
| `mori-retention-reconcile.py` | exit 0, `RECONCILE_SELFTEST_PASS` 4 | same |
| `mori-round13-regressions.py` | exit 0, `checks=33 cases=2` | same |
| `mori-round14-regressions.py` | exit 0, `checks=20` | same |
| `mori-round15-regressions.py` | exit 0, `SELFTEST PASS` | same |
| `mori-round16-regressions.py` | exit 0, `SELFTEST ok` (6 arms) | same |
| `mori-round16-context-check.py` | exit 0, 15 arms | same |
| `mori-round17-context-check.py` | exit 0, 31 arms | same |
| `mori-round17-seat-regressions.py` | exit 0, `SELFTEST ok` | same |
| `mori-round17-jj-regressions.py` | **exit 1**, `cases=17 match=8 mismatch=9 … failed=9` | **exit 1**, identical first line (sha256 `3f9c2a70f5c24add…` at both) |
| `mori-seat-terminal.py` | exit 0, 49/49 | same |
| `mori-wave-settlement.py` | exit 0, `PASS (23 cases…)` | same |

  The `mori-round17-jj-regressions.py` failure is identical at the round-23 tip, so it predates
  round 24. The tool was last changed in `2be8294` (2026-10-20), and the host has
  `jj 0.45.1-7c41cdeb16b6`. I did not find its cause, and it is not a round-24 harm. It is worth
  routing as a separate operability debt, because the SKILL gate registry lists the r17 jj suite
  as a gate.
- Without a TMPDIR inside the checkout, `content-review`, `freeze-order` and `retention-gate` fail
  closed (`FAIL 0/11`, `FAIL 0/21`, `SELFTEST_TMPDIR`) at **both** commits. This is the documented
  precondition (`mori-retention-gate.py:458-466`, `mori-freeze-order.py:497-514`,
  `mori-content-review.py:355-368`), not a regression.

- Live census, run once from the tip clone with the documented invocation
  (`TMPDIR=<scratch>/tmp MORI_SHOKUNIN_ROOT=/home/vgpnk/Projects/shokunin bash tools/mori-census.sh`
  at `ts=2026-10-22T09:02:28Z`):
  - The summary was `MORI_CENSUS: DRIFT (findings=30 drift=12 unavailable=1 surfaces=8)`, the same
    as the wave-1 baseline (`CensusNoHarmBaseline.md:84`).
  - Stdout was 63 lines, as in the baseline, and stderr was 0 bytes.
  - All 30 findings carry `script_sha256=87b8d680…`.
  - Exit code **1** (DRIFT), the same as the baseline (`CensusNoHarmBaseline.md:83`); wall time 111.7 s.
- The finding-ID multiset is **not** identical to the baseline, and the differences are host state:
  - `LANE_SILENT` (kake) is gone, because kake relaunched (`lane.kake: young … launch_epoch=1792657002`).
  - `WATCHDOG_STALE` appeared, because the watchdog log `age_s` went from 86 to 1831, past
    `stale_threshold_s=900`.

  The surface list, the census bytes and the selftest stdout are byte-equal to the baseline, and
  nothing in the census calls `mori-pressure.py`. So the ID drift is not a round-24 effect. Strictly,
  wave-1's "same finding id set" criterion (`CensusNoHarmBaseline.md:127-128`) cannot be met
  across a 46-minute gap on a live fleet. The judge should compare census bytes, the selftest tally
  and the surface set, as `CensusNoHarmBaseline.md:157-159` itself concedes. Normalized diff:
  `diff <(sed 's/ts=[0-9TZ:-]*/ts=<T>/g' /fast/scratch/hyaku/mori-r24-a2/live.out) <(sed … out/live.out)`.
  Only the watchdog age, cgroup and disk counters, and the lane rows for kaidoku, kasegi and kake differ.

### 5. Depth and freshness

- Depth: no knowledge entry, lesson or QUALITY criterion that existed before was edited (zero
  deletions; QUALITY and README are pure appends). Round 24 adds one knowledge entry and one lesson.
- Freshness: no `recheck` or `last-checked` cell of a pre-round SOURCES row changed (zero
  deletions). The drift-pin bytes (`tools/mori-census.sh --pin/--drift`) are unchanged by blob.
  No dated receipt under `corpus/evidence/` or earlier `.ufo/waves/round-*/` changed (§1).

## Findings

### A1 — Adjacency: the shared system memory PSI surface is undisclosed (fixable defect, not a pointer harm)

- **Counterexample.** `PROVINCE.md:274-277` ("Owns-scope extension") widens mori's owned read-only
  probes "to the one-shot system CPU/IO/IRQ/memory pressure read". `tools/mori-pressure.py` reads
  `/proc/pressure/memory`. Tsukuroi's Core census reads the same file by default
  (`tsukuroi-shokunin/tools/tsukuroi-census.sh:376`, `PRESSURE_FILE=${TSUKUROI_PRESSURE_FILE:-/proc/pressure/memory}`;
  C6 arm `:1100-1115`) for OS triage (`tsukuroi-shokunin/PROVINCE.md:30-33`).
- Mori's tsukuroi adjacency row (`PROVINCE.md:66`, unchanged since `c725aa37`; wave-1 cited it as
  `:65` in `ConnectSiblingPsi.md:83-85`) names only `systemd-oomd`, `earlyoom`, `memory.events` and
  `MESSAGE_ID`. It does not record this co-read. The landed note at `PROVINCE.md:284` says "no other lane's surface
  is claimed".
- Wave-1 `ConnectSiblingPsi.md:132-139` proposed appending three things: the co-read sentence, the
  route sending an `irq` `PRESSURE_HIGH` that needs device or driver attribution to tsukuroi's
  driver plane, and a statement that C2 does not close tsukuroi's pre-kill capture gap
  (`kill-event-deep-r8.md:265`). None of the three is in the landed bytes:
  `git diff -U0 c725aa37..a730ecf -- . ':!.ufo' | rg -c '^\+.*(tsukuroi-census|driver plane|driver-firmware|pre-kill)'`
  printed no count (zero matches). The only round-24 tsukuroi mentions route kernel and boot
  configuration diagnosis to tsukuroi (`PROVINCE.md:247-248`; SKILL `unsupported` row).
- **Why it is not a scored harm.** No pointer moves, and tsukuroi's own text already says "Shared
  evidence is not shared ownership" (`tsukuroi-shokunin/PROVINCE.md:41`) and cedes fleet
  correlation to mori (`:30-33`, ADJ-04 `:49`). The two lanes ask different questions of one file.
  However, an undisclosed second reader of one host surface is the duplicate-authority pattern this
  attack looks for, and the `irq` driver-attribution route is missing entirely. A judge may count
  that against adjacency 6.
- **Impacted axis:** adjacency (held 6).
- **Smallest safe correction:** append one round-24 PROVINCE bullet after line 285, without
  touching lines 3–16. It should say: tsukuroi's census C6 arm also reads system
  `/proc/pressure/memory` (`../tsukuroi-shokunin/tools/tsukuroi-census.sh:376,1100-1115`) for OS
  triage; shared evidence is not shared ownership; an `irq` `PRESSURE_HIGH` needing device or
  driver attribution routes to tsukuroi's driver plane; and C2 does not close tsukuroi's pre-kill
  capture gap. It is append-only and needs no tool, case or count change.

### A2 — Wording risk only: `PRESSURE_HIGH` exits 1 (recorded, not a harm)

`tools/mori-pressure.py:42` documents "1 on PRESSURE_HIGH", and the SKILL registry kind is
"gate (host-surface verdict; …)" (`SKILL.md:641`). That label matches the existing gate-row
convention (`SKILL.md:164-168`), and the "Never infer" column plus
`system-pressure-r24.md` ("No health claim") keep the threshold local and uncalibrated, as wave-1
contradiction 1 requires (`ConnectSiblingPsi.md:95-101`). `git grep -n 'mori-pressure' a730ecf`
finds no consumer outside the round-24 docs, so no dispatcher or slot gate turns exit 1 into a
control. No correction is needed now. A future consumer that keys on exit 1 would cross
`PROVINCE.md:12` (dispatch mechanism refused, routed to kumitate).

## What I ran

All commands below were read-only against the lane. Selftests and the census ran in scratch clones.

1. `git log --oneline`, `git diff --stat`, `--numstat`, `--name-status` and `-U0` hunk headers over
   `c725aa37..a730ecf`; per-commit `--numstat` for in-round deletions.
2. Prefix and whole-file hashes for `PROVINCE.md`, a `diff` of lines 3–16, and a `git rev-list`
   scan for the commit matching tsukuroi pin `aac98b22…`.
3. Fleet `rg` and Grep for line-number pointers into mori; `git grep` for live `SOURCES.md:N` pointers.
4. `git rev-parse` blob comparison over all 21 pre-round `tools/` paths, and `sha256` of the census.
5. Every pre-existing selftest at both commits (table in §4), the silence oracle against the census,
   and one live census run from the tip clone (§4).
6. Reads of `contract.md:95-168`, `w1/CensusNoHarmBaseline.md`, `w1/ConnectSiblingPsi.md`,
   `tsukuroi-shokunin/PROVINCE.md:1-35`, and `tsukuroi-census.sh:370-385,1100-1115`.

Not run: tsukuroi's census or `check-adjacency-anchors.py`, mutants, and any write to `/proc`,
`/sys` or a cgroup. No PSI trigger was registered.

## Tooling

I installed or upgraded nothing; no tool was needed beyond git, ripgrep, python3, bash and
coreutils already on the host. I read `/home/vgpnk/.omp/agent/RULES.md` first. The pacman guard
was not touched.
