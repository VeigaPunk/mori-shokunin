# Mo81Sc01RecordCensus — round 81 w1: read-only census of the lane record at `44bc941a`

Seat: Mo81Sc01RecordCensus (leaf, no subagent dispatch). Round 81, attempt 1, wave w1.
Scope: detection and report only; no lane byte edited except this file.

## 0. Method and provenance

- Committed bytes were read with `git -C /home/vgpnk/Projects/shokunin/mori-shokunin show 44bc941a:<path>`.
  The four record carriers (and `PROVINCE.md`) are **byte-identical** between `44bc941a` and the
  worktree when measured (03:45–03:52 local), proven by sha256 on both sides:

  ```text
  $ for f in SCORECARD.md SKILL.md LOG.md SHONEN.md PROVINCE.md; do
      git show 44bc941a:$f | sha256sum; sha256sum $f; done
  SCORECARD.md same 676b69180638bb177159d211afa590e14967391e7c69f09e0d4a0287a98ff661
  SKILL.md     same 504faf2ba5e1eee57258c5c88713bd5d25fc6ac065c36753bffde817283b8010
  LOG.md       same 798842ed8a6038cd81bd905930871245618fda2ec6ebabaa133d67166b1ec83e
  SHONEN.md    same d169d324c95850521388c4e16ba84e8b9930e0c68b44ba262dbc889978d547f6
  PROVINCE.md  same 0f442982fc356c532758e7e60cb83dec55a7a24fa56df860dc10d49590e9a13e
  ```

- **The worktree moved under this seat** (round-81 siblings landing): `git status --porcelain` at 03:51
  showed `M .ufo/waves/round-80/count-c1.py`, `M .ufo/waves/round-80/count-c3.py`,
  `M .ufo/waves/round-81/count-c1.py`, `M .ufo/waves/round-81/count-c2.py`,
  `M .ufo/waves/round-81/evidence/controls-r81.txt`, `M corpus/README.md`, plus new
  `tools/mori-record-sweep.py`, `corpus/lessons/round-81.md`, `corpus/knowledge/record-claim-integrity-r81.md`,
  `corpus/evidence/sources-r81/`, `.ufo/waves/round-81/battery.sh`, etc. mtimes ran 03:46:03–03:50:34;
  HEAD was `19765553` (committed 03:43:50).
- Because the worktree was not stable, every command in §2 was run twice: once with cwd=the lane
  (early, before most sibling writes) and once in a **pinned scratch clone**
  `/fast/scratch/hyaku/mori-r81/Mo81Sc01RecordCensus/clone-44bc941a`
  (`git clone --shared --no-hardlinks` + `git checkout --detach 44bc941a`, verified
  `git rev-parse --short HEAD` = `44bc941a`). The two runs produced **identical** outputs for all 62
  commands. Values below are the clone run (committed bytes at the entering revision); no lane file
  was written. `python3 -B` was inserted after the interpreter for Python commands to suppress
  `.pyc` writes; `TMPDIR` was a directory under the clone (`PYTHONDONTWRITEBYTECODE=1` in env).
  This changes no stdout.
- The three r80 after-measurements were also re-run from the clone with the **committed** r80 counter
  bytes at `44bc941a` (§3).
- No tool was installed or upgraded. No mutating git/jj command was run.

## 1. Exact-`PENDING` cells inside `## Round ...` sections

Parser: scan `git show 44bc941a:SCORECARD.md`; a round section starts at each `^## Round` heading and
ends at the next `##` heading; inside it, table cells are split on unescaped `|` and each cell is
`.strip()`ed; a hit is exact equality with `PENDING`.

| file:line | round | claim (column 1) | after-column | value |
|---|---|---|---|---|
| `SCORECARD.md:4048` | `## Round 80` | C1 self-assessment sweep lands and the D79-1 current row tally is corrected | `After (measured this round)` | `PENDING` |
| `SCORECARD.md:4049` | `## Round 80` | C2 round-79 counter selftests kill all six frozen mutants, sourced S595 | `After (measured this round)` | `PENDING` |
| `SCORECARD.md:4050` | `## Round 80` | C3 PROVINCE names every committed Python and shell instrument with class, registry row and purpose | `After (measured this round)` | `PENDING` |

There are exactly **3**, all in the Round 80 table, all in its last column. This matches the frozen
C2 entering arm (`pending=3`). The Round 80 prose at
`SCORECARD.md:4043-4044` says so explicitly ("all three after cells are PENDING for the L1's
post-integration measurements"). There is **no `## Round 81` section** in SCORECARD at this revision.

Sibling carriers — exact-cell test over any table (same cell trim rule), and heading check:

```text
$ grep -nE '\|[[:space:]]*PENDING[[:space:]]*\|' SCORECARD.md SKILL.md LOG.md SHONEN.md
SCORECARD.md:4048:...| PENDING |
SCORECARD.md:4049:...| PENDING |
SCORECARD.md:4050:...| PENDING |
rc=0
# no SKILL.md, LOG.md or SHONEN.md line matched
$ grep -c "^## Round 81" SCORECARD.md SKILL.md LOG.md SHONEN.md
SCORECARD.md:0
SKILL.md:0
LOG.md:0
SHONEN.md:0
rc=1
```

A Python table parse over `git show 44bc941a:{SKILL,LOG,SHONEN}.md` independently returned
`exact-cell hits=0, any-mentions=0` for all three.

## 2. Capability and gate-registry rows with a stated `<key>=<integer>` count

Selection (documented so it can be re-audited):
- **Capability tables** = SCORECARD tables whose header carries a capability/name/key column, an
  `evidence` column and a `first-working` column. There are **16 tables / 47 rows** (headings:
  `## Capabilities`, `## Capabilities (round 12 demonstrations)`, `### Capabilities demonstrated round 13`,
  `### capabilities: round18 table-shape repair`, `…round19`, `…round 20`, `…round 24`, `…round 25`,
  `…round 26`, `## Capabilities` at :1965, `…round 47`, `…round 48`, `…round 49`, `…round 53`,
  `## Round 75 backfill…`, `### Capabilities (round 80)`). A row is graded when its **evidence cell**
  contains both a `<key>=<integer>` token and a quoted command. **16 rows** qualify.
- **Gate registry** = every SKILL table with the PROTOCOL schema
  `name | kind | entry | verdict map | self-test | pinned values | write scope | owner`
  (`## Gates`, Round61/73 backfills, Round79 rows; **104 rows**). A row is graded when its **self-test
  cell** contains both a `<key>=<integer>` token and a quoted command. **55 rows** qualify (54 parsed
  plus `SKILL.md:938`, whose escaped `\|` breaks naive cell splitting; extracted by direct line read).
- Explicitly **not** graded: verdict-map cells and `what it can do` prose. Their `=0`/`=1` tokens are
  exit-contract grammar, not measurements of the entering bytes. A row-wide scan (count anywhere in
  the row + command anywhere in the row) adds 4 capability rows and 12 registry rows; the measured
  ones among them are listed in §2b, the rest are verdict-map grammar and are excluded.
- **71 rows** total. All commands ran with cwd=the `44bc941a` clone; every rc is 0 unless shown.
  For host-live tokens the quoted Windows live command is not re-derivable on this Linux host; the
  row's selftest tally is still graded.

| row | name | stated | command | live | rc | verdict |
|---|---|---|---|---|---|---|
| `SCORECARD.md:2609` | registry pin reconciler (v2) | `pass=34, fail=0` | `python3 tools/mori-pin-check.py --selftest` | `PIN_CHECK_SELFTEST pass=125 fail=0` | 0 | **STALE: 34 → 125** |
| `SCORECARD.md:2636` | junk-variant calibration counter | `pass=34, fail=0` | `python3 .ufo/waves/round-48/count-c1.py --selftest` | `C1_SELFTEST pass=34 fail=0` | 0 | AGREE |
| `SCORECARD.md:2637` | unlanded-work check | `pass=13, fail=0` | `python3 tools/mori-unlanded-check.py --selftest` | `UNLANDED_SELFTEST pass=17 fail=0` | 0 | **STALE: 13 → 17** |
| `SCORECARD.md:2667` | opaque-handle junk-variant counter | `pass=44, fail=0` | `python3 .ufo/waves/round-49/count-c1.py --selftest` | `C1_SELFTEST pass=44 fail=0` | 0 | AGREE |
| `SCORECARD.md:2668` | flagged-versus-fixed count | `flagged=45, fixed=18, unfixed=9` | `python3 .ufo/waves/round-49/flagged-fixed/count-flagged.py` | `flagged=45 fixed=18 unfixed=9` | 0 | AGREE (last line is `na=18`) |
| `SCORECARD.md:3044` | counter-execution boundary v2 (`count-c3.py`) | `cases=5` | `python3 .ufo/waves/round-61/count-c3.py 986d4b46… --scratch <dir>` | `C3=… cases=5 failed=r61 counters absent …` | 1 | COUNT AGREE; the command is not runnable as written (literal `986d4b46…` and `<dir>`); rc 1 is the artifact |
| `SCORECARD.md:3076` | per-cgroup pressure probe | `pass=12, fail=0, ok=0, absent=4` | `python tools/mori-cgroup-pressure.py --selftest` | `MORI_CGROUP_PRESSURE_SELFTEST: pass=12 fail=0` | 0 | AGREE on pass; `ok=0/absent=4` are Windows-host live tokens |
| `SCORECARD.md:3128` | Windows host-events probe | `pass=10, fail=0, surfaces=4, ok=4, matched=209, window=200` | `python tools/mori-host-events-win.py --selftest` | `HOST_EVENTS_WIN_SELFTEST pass=10 fail=0` | 0 | AGREE on pass; rest host-live |
| `SCORECARD.md:3178` | Windows resource-runway probe | `surfaces=2, ok=2, unavailable=0` | `python tools/mori-runway-win.py --selftest` | `RUNWAY_WIN_SELFTEST: PASS (9 cases)` | 0 | AGREE on 9 cases; rest host-live |
| `SCORECARD.md:3419` | per-response separation receipt | `stable=1497`; cell also states `PASS (6 cases)` | `python tools/mori-ua-variance.py --selftest` | `MORI_UA_VARIANCE_SELFTEST: PASS (14 cases)` | 0 | **STALE: 6 → 14**; `stable=1497` host-live |
| `SCORECARD.md:3539` | Windows host-uptime read | `surfaces=1, ok=1, uptime_d=5` | `python tools/mori-uptime-win.py --selftest` | `UPTIME_WIN_SELFTEST: PASS (8 cases)` | 0 | AGREE on 8 cases; rest host-live |
| `SCORECARD.md:3590` | Windows working-state read | `surfaces=1, ok=1` | `python tools/mori-workstate-win.py --selftest` | `WORKSTATE_WIN_SELFTEST: PASS (10 cases)` | 0 | AGREE on 10 cases; rest host-live |
| `SCORECARD.md:3591` | boot-window-paired events receipt | `events_ok=1, uptime_ok=1, matched=209, window=200` | `python tools/mori-events-context-win.py --selftest` | `EVENTS_CONTEXT_SELFTEST: PASS (10 cases)` | 0 | AGREE on 10 cases; rest host-live |
| `SCORECARD.md:3646` | anchor-checker | `mislocated=1, wordcount_mismatch=2` | `python tools/mori-anchor-check.py --selftest` | `ANCHOR_CHECK_SELFTEST: PASS (11 cases)` | 0 | AGREE on 11 cases; the two tokens are live-run A–E values |
| `SCORECARD.md:3786` | rotation-recurrence schedule | `window_s_computed=31, wall_s=429` | `python tools/mori-rotation-schedule.py --selftest` | `MORI_ROTATION_SCHEDULE_SELFTEST: PASS (13 cases)` | 0 | AGREE on 13 cases; rest host-live |
| `SCORECARD.md:4036` | self-assessment claim sweep | `pass=30, fail=0, …, pointers=232` | `python3 -I tools/mori-claim-sweep.py --selftest` / `… --root . --pins .ufo/waves/round-80/claim-pins.json` | `CLAIM_SWEEP_SELFTEST pass=30 fail=0` / `CLAIM_SWEEP … pointers=233` | 0 | **STALE: pointers 232 → 233**; selftest 30 agrees |
| `SKILL.md:166` | silence oracle | `pass=24, fail=0` | `bash tools/mori-silence-cases.sh --selftest` | `MORI_SILENCE_CASES_SELFTEST pass=24 fail=0` | 0 | AGREE |
| `SKILL.md:182` | r19 finite regressions | `pass=26, fail=0` | `python3 tools/mori-round19-regressions.py --selftest` | `R19_SELFTEST pass=26 fail=0` | 0 | AGREE (clone; lane cwd exits 2 `explicit-lane-tmpdir-invalid` by the tool's own guard) |
| `SKILL.md:183` | r44 figure ledger (C1) | `pass=6, fail=0` | `python3 .ufo/waves/round-44/count-c1.py --selftest` | `C1_SELFTEST pass=6 fail=0` | 0 | AGREE |
| `SKILL.md:184` | r44 gate registry (C2) | `pass=15, fail=0` | `python3 tools/mori-gate-registry.py --selftest` | `GATE_REGISTRY_SELFTEST pass=15 fail=0` | 0 | AGREE |
| `SKILL.md:185` | r44 gate conformance (C2) | `pass=5, fail=0` | `python3 .ufo/waves/round-44/count-c2.py --selftest` | `C2_SELFTEST pass=5 fail=0` | 0 | AGREE |
| `SKILL.md:186` | r44 corpus coverage (C3) | `pass=6, fail=0` | `python3 .ufo/waves/round-44/count-c3.py --selftest` | `C3_SELFTEST pass=6 fail=0` | 0 | AGREE |
| `SKILL.md:187` | disk write rate (r34) | `pass=14, fail=0` | `python3 tools/mori-disk-rate.py --selftest` | `MORI_DISK_RATE_SELFTEST pass=14 fail=0` | 0 | AGREE |
| `SKILL.md:189` | r41 calibration | `pass=10, fail=0` | `python3 tools/mori-round41-calibration.py --selftest` | `MORI_R41_CALIBRATION_SELFTEST pass=10 fail=0` | 0 | AGREE |
| `SKILL.md:190` | r45 ledger counter (C1) | `pass=16, fail=0`; mutant `pass=15 fail=1` | `python3 .ufo/waves/round-45/count-c1.py --selftest` | primary `C1_SELFTEST pass=16 fail=0`; mutant bytes `C1_SELFTEST pass=15 fail=1` | 0 / 1 | AGREE (both groups verified: mutant run is `.ufo/waves/round-45/fixtures/mutants/count-c1.py`) |
| `SKILL.md:191` | r45 gate conformance (C2) | `pass=14, fail=0` | `python3 .ufo/waves/round-45/count-c2.py --selftest` | `C2_SELFTEST pass=14 fail=0` | 0 | AGREE |
| `SKILL.md:192` | r45 corpus coverage (C3) | `pass=19, fail=0`; mutant `pass=17 fail=2` | `python3 .ufo/waves/round-45/count-c3.py --selftest` | primary `C3_SELFTEST pass=19 fail=0`; mutant bytes `C3_SELFTEST pass=17 fail=2` | 0 / 1 | AGREE (both verified) |
| `SKILL.md:193` | r44 figure ledger — write-scope superseded | `pass=6, fail=0` | `python3 .ufo/waves/round-44/count-c1.py --selftest` | `C1_SELFTEST pass=6 fail=0` | 0 | AGREE |
| `SKILL.md:194` | r44 gate registry — write-scope superseded | `pass=15, fail=0` | `python3 tools/mori-gate-registry.py --selftest` | `GATE_REGISTRY_SELFTEST pass=15 fail=0` | 0 | AGREE |
| `SKILL.md:195` | r44 gate conformance — write-scope superseded | `pass=5, fail=0` | `python3 .ufo/waves/round-44/count-c2.py --selftest` | `C2_SELFTEST pass=5 fail=0` | 0 | AGREE |
| `SKILL.md:196` | r44 corpus coverage — write-scope superseded | `pass=6, fail=0` | `python3 .ufo/waves/round-44/count-c3.py --selftest` | `C3_SELFTEST pass=6 fail=0` | 0 | AGREE |
| `SKILL.md:665` | routed round-23 items (r24, C1) | `pass=20, fail=0` | `python3 -I tools/mori-routed-check.py --selftest` | `ROUTED_CHECK_SELFTEST pass=20 fail=0` | 0 | AGREE |
| `SKILL.md:740` | routed round-24 items (r25, C1) | `pass=26, fail=0` | `python3 -I -B tools/mori-routed-r24.py --selftest` | `ROUTED_R24_SELFTEST pass=26 fail=0` | 0 | AGREE |
| `SKILL.md:817` | blind-writer gate (r31) | `scanned=14, blind_violations=13` | `bash tools/mori-blind-check.sh --selftest` | `PASS` | 0 | NOT-EMITTED: the command prints only `PASS`; 14/13 are internal fixture expectations |
| `SKILL.md:912` | SOURCES append-only timing (r38) | `pass=22, fail=0`; historical `pass=15` | `python3 tools/mori-sources-appendonly.py --selftest` (cell quotes a bare `--selftest` beside `tools/mori-pin-check.py`) | `MORI_SOURCES_APPENDONLY_SELFTEST pass=22 fail=0` | 0 | AGREE (22); `pass=15` is the explicitly-named old round-40 bytes |
| `SKILL.md:938` | registry pin reconciler (r47, C1) | `pass=125, fail=0` | `python3 tools/mori-pin-check.py --selftest` | `PIN_CHECK_SELFTEST pass=125 fail=0` | 0 | AGREE (escaped `\|` in the row required a direct line read) |
| `SKILL.md:939` | r47 tracepoint catalogue (C2) | `pass=13, fail=0` | `python3 .ufo/waves/round-47/count-c2.py --selftest` | `C2_SELFTEST pass=13 fail=0` | 0 | AGREE |
| `SKILL.md:971` | r48 junk-variant counter (C1) | `pass=34, fail=0` | `python3 .ufo/waves/round-48/count-c1.py --selftest` | `C1_SELFTEST pass=34 fail=0` | 0 | AGREE |
| `SKILL.md:972` | r48 quota entry counter (C2) | `pass=22, fail=0` | `python3 .ufo/waves/round-48/count-c2.py --selftest` | `C2_SELFTEST pass=22 fail=0` | 0 | AGREE |
| `SKILL.md:973` | unlanded check (r48) | `pass=17, fail=0` | `python3 tools/mori-unlanded-check.py --selftest` | `UNLANDED_SELFTEST pass=17 fail=0` | 0 | AGREE |
| `SKILL.md:1009` | r49 opaque-handle counter (C1) | `pass=44, fail=0` | `python3 .ufo/waves/round-49/count-c1.py --selftest` | `C1_SELFTEST pass=44 fail=0` | 0 | AGREE |
| `SKILL.md:1010` | r49 journal-reach entry counter (C2) | `pass=26, fail=0` | `python3 .ufo/waves/round-49/count-c2.py --selftest` | `C2_SELFTEST pass=26 fail=0` | 0 | AGREE |
| `SKILL.md:1056` | r50 calibration counter (C1) | `pass=34, fail=0` | `python3 .ufo/waves/round-50/count-c1.py --selftest` | `C1_SELFTEST pass=34 fail=0` | 0 | AGREE |
| `SKILL.md:1057` | r50 memcg report-block counter (C2) | `pass=31, fail=0` | `python3 .ufo/waves/round-50/count-c2.py --selftest` | `C2_SELFTEST pass=31 fail=0` | 0 | AGREE |
| `SKILL.md:1113` | r51 MemAvailable entry counter (C2) | `pass=34, fail=0` | `python3 .ufo/waves/round-51/count-c2.py --selftest` | `C2_SELFTEST pass=34 fail=0` | 0 | AGREE |
| `SKILL.md:1273` | r52 calibration counter (C1) | `pass=42, fail=0` | `python3 .ufo/waves/round-52/count-c1.py --selftest` | `C1_SELFTEST pass=42 fail=0` | 0 | AGREE |
| `SKILL.md:1274` | r52 overcommit ledger counter (C2) | `pass=45, fail=0` | `python3 .ufo/waves/round-52/count-c2.py --selftest` | `C2_SELFTEST pass=45 fail=0` | 0 | AGREE |
| `SKILL.md:1275` | r53 release-recheck counter (C1) | `pass=37, fail=0` | `python3 .ufo/waves/round-53/count-c1.py --selftest` | `C1_SELFTEST pass=37 fail=0` | 0 | AGREE |
| `SKILL.md:1276` | r53 commit-runway counter (C2) | `pass=30, fail=0` | `python3 .ufo/waves/round-53/count-c2.py --selftest` | `C2_SELFTEST pass=30 fail=0` | 0 | AGREE |
| `SKILL.md:1277` | r54 memory-failure recheck (C1) | `pass=57, fail=0` | `python3 .ufo/waves/round-54/count-c1.py --selftest` | `C1_SELFTEST pass=57 fail=0` | 0 | AGREE |
| `SKILL.md:1278` | r54 memory-failure entry (C2) | `pass=54, fail=0` | `python3 .ufo/waves/round-54/count-c2.py --selftest` | `C2_SELFTEST pass=54 fail=0` | 0 | AGREE |
| `SKILL.md:1279` | r55 pointer-ledger counter (C1) | `pass=44, fail=0` | `python3 .ufo/waves/round-55/count-c1.py --selftest` | `C1_SELFTEST pass=44 fail=0` | 0 | AGREE |
| `SKILL.md:1280` | r55 ENOSPC entry counter (C2) | `pass=10, fail=0` | `python3 .ufo/waves/round-55/count-c2.py --selftest` | `C2_SELFTEST pass=10 fail=0` | 0 | AGREE |
| `SKILL.md:1281` | r56 capability counter (C1) | `pass=1, fail=0` | `python3 .ufo/waves/round-56/count-c1.py --selftest` | `C1_COUNTER_SELFTEST pass=1 fail=0` | 0 | AGREE |
| `SKILL.md:1282` | r56 unclosed-pairing counter (C2) | `pass=1, fail=0` | `python3 .ufo/waves/round-56/count-c2.py --selftest` | `C2_COUNTER_SELFTEST pass=1 fail=0` | 0 | AGREE |
| `SKILL.md:1286` | r58 register-recheck counter (C1) | `pass=4, fail=0` | `python3 .ufo/waves/round-58/count-c1.py --selftest` | `C1_SELFTEST pass=4 fail=0` | 0 | AGREE |
| `SKILL.md:1287` | r58 entry counter (C2) | `pass=6, fail=0` | `python3 .ufo/waves/round-58/count-c2.py --selftest` | `C2_SELFTEST pass=6 fail=0` | 0 | AGREE |
| `SKILL.md:1288` | r59 active-register counter (C1) | `pass=6, fail=0` | `python3 .ufo/waves/round-59/count-c1.py --selftest` | `C1_SELFTEST pass=6 fail=0` | 0 | AGREE |
| `SKILL.md:1289` | r59 settlement counter (C2) | `pass=9, fail=0` | `python3 .ufo/waves/round-59/count-c2.py --selftest` | `C2_SELFTEST pass=9 fail=0` | 0 | AGREE |
| `SKILL.md:1290` | r60 pointer-honesty counter (C1) | `pass=6, fail=0` | `python3 .ufo/waves/round-60/count-c1.py --selftest` | `C1_SELFTEST pass=6 fail=0` | 0 | AGREE |
| `SKILL.md:1291` | r60 entry-claims counter (C2) | `pass=8, fail=0` | `python3 .ufo/waves/round-60/count-c2.py --selftest` | `C2_SELFTEST pass=8 fail=0` | 0 | AGREE |
| `SKILL.md:1292` | r60 execution-boundary counter (C3) | `pass=3, fail=0` | `python3 .ufo/waves/round-60/count-c3.py --selftest` | `C3_SELFTEST pass=3 fail=0` | 0 | AGREE |
| `SKILL.md:1293` | vote binder (r56 tool) | `pass=16, fail=0` | `python3 tools/mori-vote-bind.py --selftest` | `VOTE_BIND_SELFTEST pass=16 fail=0` | 0 | AGREE |
| `SKILL.md:1294` | driver-liveness probe (r56 tool) | `pass=13, fail=0, skipped=0` | `python3 tools/mori-driver-liveness.py --selftest` | `DRIVER_LIVENESS_SELFTEST pass=13 fail=0 skipped=0` | 0 | AGREE |
| `SKILL.md:1295` | register checker (r59 tool) | `pass=12, fail=0` | `python3 tools/mori-register-check.py --selftest` | `REGCHECK_SELFTEST pass=12 fail=0` | 0 | AGREE |
| `SKILL.md:1296` | settlement scanner (r59 tool) | `pass=10, fail=0` | `python3 tools/mori-settlement-scan.py --selftest` | `SETSCAN_SELFTEST pass=10 fail=0` | 0 | AGREE |
| `SKILL.md:1297` | entry-claims checker (r60 tool) | `pass=13, fail=0` | `python3 tools/mori-entry-claims-check.py --selftest` | `ENTRYCLAIMS_SELFTEST pass=13 fail=0` | 0 | AGREE |
| `SKILL.md:1317` | receipt-complete guard (r63 tool) | `pass=8, fail=0` | `python tools/mori-receipt-complete.py --selftest` | `RECEIPT_COMPLETE_SELFTEST pass=8 fail=0` | 0 | AGREE |
| `SKILL.md:1318` | host-events probe (r63 tool) | `pass=10, fail=0` | `python tools/mori-host-events-win.py --selftest` | `HOST_EVENTS_WIN_SELFTEST pass=10 fail=0` | 0 | AGREE |
| `SKILL.md:1365` | control-receipt guard (r79 tool) | `pass=19, fail=0` | `python tools/mori-control-receipt.py --selftest` | `CONTROL_RECEIPT_SELFTEST pass=19 fail=0` | 0 | AGREE |
| `SKILL.md:1366` | self-assessment claim sweep (row 14) | `pass=30, fail=0` | `python3 -I tools/mori-claim-sweep.py --selftest` | `CLAIM_SWEEP_SELFTEST pass=30 fail=0` | 0 | AGREE |

### 2b. Measured case-count / `N/N` rows outside the `<key>=<int>` strict set

These were run because they state a measured tally with a command, even though the tally is not in
`key=integer` form. All agree except `SCORECARD.md:3294` (stale; see §4):

| row | stated | command run | live | rc |
|---|---|---|---|---|
| `SCORECARD.md:2003` | `16/16 selftest` | `python3 tools/mori-vote-bind.py --selftest` | `VOTE_BIND_SELFTEST pass=16 fail=0` | 0 |
| `SCORECARD.md:3968` | `PASS (12 cases)` | `python3 tools/mori-counter-win.py --selftest` | `COUNTER_WIN_SELFTEST: PASS (12 cases)` | 0 |
| `SCORECARD.md:4016` | `selftest 19 in-memory cases`; evidence also names `18/18` as the r79 freeze | `python3 tools/mori-control-receipt.py --selftest` | `CONTROL_RECEIPT_SELFTEST pass=19 fail=0` | 0 |
| `SKILL.md:905` | `PASS (6 cases)` | `python3 tools/mori-source-drift.py --selftest` | `MORI_SOURCE_DRIFT_SELFTEST: PASS (6 cases)` | 0 |
| `SKILL.md:911` | `CONFORM_SELFTEST pass=11 fail=0` | `python3 .ufo/waves/round-40/conform.py 265a955c --selftest` | `CONFORM_SELFTEST pass=11 fail=0` | 0 |
| `SKILL.md:1284` | `C2=met claims=8 source=ok quotes=ok` at `7370a731` | `python3 .ufo/waves/round-57/count-c2.py 7370a731` | `C2=met claims=8 source=ok quotes=ok rev=7370a731` | 0 |
| `SKILL.md:1285` | `ok rows=8 mismatches=0` | `python3 .ufo/waves/round-57/verify-c2-source.py corpus/knowledge/watchdog-unclosed-r57.md corpus/evidence/sources-r57/mori-driver-liveness.py` | `C2_SOURCE_CHECK ok rows=8 mismatches=0` | 0 |
| `SKILL.md:1321` | `PASS (10 cases)` | `python tools/mori-drift-recheck.py --selftest` | `MORI_DRIFT_RECHECK_SELFTEST: PASS (10 cases)` | 0 |
| `SKILL.md:1322` | `PASS (14 cases)` | `python tools/mori-ua-variance.py --selftest` | `MORI_UA_VARIANCE_SELFTEST: PASS (14 cases)` | 0 |
| `SKILL.md:1325` | `PASS (10 cases)` | `python tools/mori-events-context-win.py --selftest` | `EVENTS_CONTEXT_SELFTEST: PASS (10 cases)` | 0 |
| `SKILL.md:1328` | `PASS (12 cases)` | `python tools/mori-counter-win.py --selftest` | `COUNTER_WIN_SELFTEST: PASS (12 cases)` | 0 |
| `SCORECARD.md:3294` → see §4 | `PASS (7 cases)` | `python tools/mori-drift-recheck.py --selftest` | `MORI_DRIFT_RECHECK_SELFTEST: PASS (10 cases)` | 0 |

`SKILL.md:911` is **not runnable as quoted**: the cell quotes `--selftest` alone, and
`conform.py --selftest` exits 2 with `conformance setup error: expected str, bytes or os.PathLike
object, not NoneType` because the selftest needs the revision positional. With the documented
`265a955c` it prints 11. This is a cell self-containment defect, not a count defect.

## 3. The three r80 `PENDING` after-values, from receipts and re-measurement

### 3a. Committed receipts (quoted exactly, with line numbers)

Entering controls, `git show 44bc941a:.ufo/waves/round-80/evidence/controls-r80.txt`:

```text
controls-r80.txt:34  C1=unmet tool=absent sweep=- mismatches=- row_tally=- live_tally=- rev=d58889220d3c      (rc 1)
controls-r80.txt:45  MUTATION_C2 survivors=2 killed=4 total=6 rev=d58889220d3c                                 (rc 1)
controls-r80.txt:50  C3=unmet named=14 present=55 missing=41 extra=0 rev=d58889220d3c                        (rc 1)
```

After receipt, `git show 44bc941a:.ufo/waves/round-80/evidence/after-r80.txt`:

```text
after-r80.txt:3   C1=met tool=present sweep=0 mismatches=0 unresolved=0 tallies=0 stale=0 row_tally=19 live_tally=19 rev=97ce0c96c779   (rc 0)
after-r80.txt:7   CLAIM_SWEEP mismatches=0 unresolved=0 tallies=0 stale=0 carriers=4 pointers=233                                        (rc 0)
after-r80.txt:57  MUTATION_C2 survivors=0 killed=6 total=6 unmutated=green rev=97ce0c96c779                                            (rc 0)
after-r80.txt:62  C3=met named=56 present=56 missing=0 extra=0 rev=97ce0c96c779                                                        (rc 0)
```

### 3b. Fresh re-measurement at the entering tip `44bc941a` (this seat)

The committed after receipt cites `97ce0c96c779`, while the r80 round table lives in the
`44bc941a` tree (D80-4's precision class). I re-ran the same three commands from the pinned clone
using the **committed r80 counter bytes at `44bc941a`**, grading revision `44bc941a`:

```text
$ python3 -B .ufo/waves/round-80/count-c1.py 44bc941a0e3e9676fa33a882b43d6e9793cbf74d --scratch <clone>/.scratch/r80-c1
C1=met tool=present sweep=0 mismatches=0 unresolved=0 tallies=0 stale=0 row_tally=19 live_tally=19 rev=44bc941a0e3e
rc=0

$ python3 -B .ufo/waves/round-80/mutate-c2.py --rev 44bc941a0e3e9676fa33a882b43d6e9793cbf74d --scratch <clone>/.scratch/r80-c2
unmutated survived rc=0 C2_COUNTER_SELFTEST pass=7 fail=0
mutant drop_admitted killed rc=1 C2_COUNTER_SELFTEST pass=6 fail=1
mutant raise_ceiling killed rc=1 C2_COUNTER_SELFTEST pass=5 fail=2
mutant count_other_verdicts killed rc=1 C2_COUNTER_SELFTEST pass=5 fail=2
mutant cut_clause_boundary killed rc=1 C2_COUNTER_SELFTEST pass=6 fail=1
mutant any_round_in_cell killed rc=1 C2_COUNTER_SELFTEST pass=4 fail=3
mutant met_ignores_mismatch killed rc=1 C2_COUNTER_SELFTEST pass=2 fail=5
MUTATION_C2 survivors=0 killed=6 total=6 unmutated=green rev=44bc941a0e3e
rc=0

$ python3 -B .ufo/waves/round-80/count-c3.py 44bc941a0e3e9676fa33a882b43d6e9793cbf74d --scratch <clone>/.scratch/r80-c3
C3=met named=56 present=56 missing=0 extra=0 rev=44bc941a0e3e
rc=0
```

So the three cells at `SCORECARD.md:4048-4050` can be filled from receipts, not re-invented:

| cell | measured after value | measured revision | receipt |
|---|---|---|---|
| `SCORECARD.md:4048` (C1) | `C1=met tool=present sweep=0 mismatches=0 unresolved=0 tallies=0 stale=0 row_tally=19 live_tally=19`, rc 0 | `44bc941a` (also `97ce0c96c779` in `after-r80.txt:3`) | `after-r80.txt` |
| `SCORECARD.md:4049` (C2) | `MUTATION_C2 survivors=0 killed=6 total=6 unmutated=green`, rc 0 | `44bc941a` (also `97ce0c96c779` in `after-r80.txt:57`) | `after-r80.txt` |
| `SCORECARD.md:4050` (C3) | `C3=met named=56 present=56 missing=0 extra=0`, rc 0 | `44bc941a` (also `97ce0c96c779` in `after-r80.txt:62`) | `after-r80.txt` |

The `PENDING` prose at `SCORECARD.md:4043-4044` ("all three after cells are PENDING for the L1's
post-integration measurements") is the same debt in narrative form.

## 4. Counts that disagree with a sibling carrier

Same-tool, same-count comparisons across `SCORECARD.md` / `SKILL.md` / `LOG.md` at `44bc941a`
(selftest tallies grouped by tool path; round-scoped historical statements excluded and named):

| class | carrier A | carrier B | live at `44bc941a` | verdict |
|---|---|---|---|---|
| unlanded check | `SCORECARD.md:2637` `pass=13 fail=0` | `SKILL.md:973` `pass=17 fail=0` | `UNLANDED_SELFTEST pass=17 fail=0` | **A stale; B correct** |
| UA-variance probe | `SCORECARD.md:3419` `PASS (6 cases)` (also `:3415` "6 cases at entering") | `SCORECARD.md:3490` `PASS (14 cases)`; `SKILL.md:1322` `PASS (14 cases)` | `MORI_UA_VARIANCE_SELFTEST: PASS (14 cases)` | **:3419 stale; the r69 row and SKILL correct**; `:3415` is explicitly the entering value |
| pin reconciler | `SCORECARD.md:2609` `pass=34 fail=0` | `SKILL.md:938` `pass=125 fail=0` | `PIN_CHECK_SELFTEST pass=125 fail=0` | **:2609 stale; SKILL correct** |
| drift re-check | `SCORECARD.md:3294` `PASS (7 cases)` (r66 capability row) | `SCORECARD.md:3351` `PASS (10 cases)` (r67 extension); `SKILL.md:1321` `PASS (10 cases)` | `MORI_DRIFT_RECHECK_SELFTEST: PASS (10 cases)` | **:3294 stale as a present-tense capability row; 10 is live** |
| claim sweep pointers | `SCORECARD.md:4036` `pointers=232` | `after-r80.txt:7` `pointers=233`; live sweep `pointers=233`; SKILL row 14 does not state the pointer count | `CLAIM_SWEEP … pointers=233` | **:4036 stale (D80-2)** |
| control-receipt guard | `SCORECARD.md:4016` `19 in-memory cases` / `19/19`; `SCORECARD.md:4024` `pass=19` | `SKILL.md:1365` `pass=19` | `CONTROL_RECEIPT_SELFTEST pass=19 fail=0` | **no disagreement**; the only `18` is explicitly labelled the r79 wave-freeze value at `SCORECARD.md:4016` and `SKILL.md:1365`'s "froze 18 arms" history |

Notes on apparent diffs that are **not** defects:
- `LOG.md:3675` "MORI_UA_VARIANCE_SELFTEST: PASS (6 cases)" is the r68 landing record; the tool later
  grew to 14 (r69), stated in `LOG.md`'s r69 entry and `SCORECARD.md:3486/3490`.
- `SKILL.md:912`'s `pass=15` is explicitly the round-40 bytes; 22 is the current tally.
- `SKILL.md:190/192`'s second `pass/fail` pair is the mutant run (verified 15/1 and 17/2), not the
  primary counter.
- `CONFORM_SELFTEST` values 6/9/11/14 belong to different per-round tools
  (`.ufo/waves/round-37…40/conform.py`), not one tool with a drifting count.

**C2 relevance (report only, no edit):** `.ufo/waves/round-81/record-pins.json` has exactly one
binding (`pointers`, `SCORECARD.md`, row containing `tools/mori-claim-sweep.py`). The four other
stale capability-row tallies above are the same class the C2 claim describes but are **not pinned**,
so the `pinned` arm cannot see them. At the entering bytes the pointer fixed point is **233**; once
the round-81 capability/registry rows land, the same pinned command prints **240** (the sibling C2
edit observed at 03:55 states 240), so the cell must carry the live output at the landed tree, not
the entering 233. The four unpinned stale counts are then the remaining record debt; whether to add
bindings is the L1's call.

## 5. Other defects / observations in other seats' bytes (file:line)

1. `SKILL.md:911` (r40 conformance row): self-test cell quotes `--selftest` without the required
   revision; the exact quoted command exits 2. With `265a955c` it prints `CONFORM_SELFTEST pass=11`.
2. `SKILL.md:912` (SOURCES append-only row): the self-test cell quotes a bare `--selftest` fragment
   beside `tools/mori-pin-check.py`; the 22 tally belongs to `tools/mori-sources-appendonly.py`.
   Running the cell literally (`python3 tools/mori-pin-check.py` with no args) exits 2.
3. `SKILL.md:817` (blind-writer row): states `scanned=14`, `blind_violations=13`, but the quoted
   command prints only `PASS`; the numbers are internal fixture expectations, not observable output.
4. `SCORECARD.md:3044`: the quoted command embeds an ellipsized revision (`986d4b46…`) and `<dir>`,
   so it is not runnable as written; the `cases=5` token does reproduce when the literal is supplied,
   but rc is 1 because the revision cannot resolve.
5. `SCORECARD.md:4043-4044` + `:4048-4050`: D80-1, the three after cells are still `PENDING` although
   the after receipt is measured (§3).
6. `SCORECARD.md:4036` + `SKILL.md:1366`: D80-2 wording ("integration re-run pending" /
   "integration re-run owned by L1") and the `232` count (§4).
7. `SCORECARD.md:2609`, `:2637`, `:3294`, `:3419`: stale capability-row tallies not covered by the
   round-81 pins (§4). These are the same class as the D80-2 pointer count.
8. Provenance hazard: the lane worktree was being written by siblings during this census
   (03:46–03:50; see §0). Any live-value census that runs directly in the worktree during a wave is
   reading a moving target; the clone-at-revision method in §0 is the stable form.

## 6. What I verified, what I could not, and cleanup

**Verified (commands run, not receipts read):** the 62-command deduped set of §2, run twice (lane
worktree early, then the pinned clone; identical output), plus every supplemental command named in
§2b/§4 run in the clone, plus the three r80 after-claims at `44bc941a`; the 71-row count census, the
case-count rows, the exact-`PENDING` parse, the zero-`PENDING` result for SKILL/LOG/SHONEN, and the
sha256 identity of the five record carriers between `44bc941a` and the worktree.

**Could not verify on this host:** the Windows-host live tokens (`matched=209`, `window=200`,
`uptime_d=5`, `surfaces=…/ok=…`, `stable=1497`, `mislocated=1/wordcount_mismatch=2`,
`window_s_computed=31,91,304`, `wall_s=429`, `ok=0 absent=4`). These were measured on the Windows
workspace host named in the rows; they are not re-derivable on this Linux host, and I did not run
mutating or networked live probes. Their selftest tallies do reproduce. `SCORECARD.md:3044`'s
ellipsized command is not reproducible as written. `SKILL.md:817`'s internal 14/13 counts are not
emitted. Whether the four stale capability rows are intended as round-scoped history or current
claims is a judgment the L1 must make; the live values are measured.

**Lane cleanliness:** no lane file was written by this seat except this report path. At the time of
the census (03:45–03:52) `git status` showed only sibling round-81 work, no `__pycache__` newer than
30 minutes, and the record carriers hash-identical to `44bc941a`. `SCORECARD.md` was then modified by
the C2 seat at 03:55 (the Round 81 section and the 240-pointer correction), after this census's
pinned measurements; that later state is not graded here. Scratch
`/fast/scratch/hyaku/mori-r81/Mo81Sc01RecordCensus` (including the clone, export, TMPDIRs and the
JSON run logs `census-runs.json`, `census-runs-clone.json`, `r80-clone-remeasure.json`,
`row-census.json`) was deleted before this report was yielded; the commands and outputs are quoted
here because a `/tmp` or scratch path is not citable evidence.

**Tooling:** none installed or upgraded; system `python3` 3.14.8 and `git` only.
