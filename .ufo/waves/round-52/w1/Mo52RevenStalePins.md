# Mo52RevenStalePins — when each stale living pin went stale (round 52, wave w1)

Seat: Mo52RevenStalePins (reverse-engineering of the living-document pins in `corpus/QUALITY.md` and
`corpus/README.md` for `tools/mori-sources-appendonly.py` and round-39 `conform.py`).
Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin`, lane HEAD measured `075436b1346ca659afb8be7a46f0e67e4170aa83`
(round-52 wave-spec commit), data commit `8524904adb25e44f24d9f25aac7eae909625c18c`, entering tip
`4f266ef2fdf74d8b046f5b4f5a5c4945f65b966d`.
Scratch: `/fast/scratch/hyaku/mori-r52/Mo52RevenStalePins/` (TMPDIR `/fast/scratch/hyaku/mori-r52/Mo52RevenStalePins/tmp`),
`disk-guard.sh status` at start: `/fast/scratch/hyaku` 24 % used, 614.9 G free; `/tmp` 4 %, 123.9 G free.
No tool installed or upgraded (no need: `git`, `python3` suffice). Nothing written in the lane except this report;
every lane git call was read-only (`log`, `show`, `grep`). No clone and no archive was needed — the instrument is a
single file, so each historical revision was extracted with `git show <rev>:<path>` into scratch and run there.

Everything below is observed. Commands are quoted literally with the exit code.

## 1. The instrument's own tally chain (measured, not inferred)

`tools/mori-sources-appendonly.py` was created in round 36 and touched in exactly five commits
(`git -C <lane> log --follow -- tools/mori-sources-appendonly.py`). For each revision I extracted the file
(`git show <rev>:tools/mori-sources-appendonly.py > $S/rev/<rev>/tool.py`) and ran it from scratch:

    cd /fast/scratch/hyaku/mori-r52/Mo52RevenStalePins/rev/<rev> && TMPDIR=<same> python3 tool.py --selftest

| commit | date | subject | bytes | printed |
|---|---|---|---|---|
| `bf0df77f` | 2026-10-23 | round-36: C1/C2 data — append-only gate + index-clean | 20887 | `MORI_SOURCES_APPENDONLY_SELFTEST pass=8 fail=0` exit 0 |
| `daa1d4d2` | 2026-10-23T17:55:19-03:00 | round-38 data: timed supersede in the append-only gate | 25922 | `pass=9 fail=0` exit 0 |
| `97b826a9` | 2026-10-24T00:01:48-03:00 | round-39: freeze — gate v2 ancestry timing | 37365 | `pass=12 fail=0` exit 0 |
| `265a955c` | 2026-10-24T01:31:20-03:00 | round-40: instruments — gate v3 (P-C11) | 43848 | `pass=15 fail=0` exit 0 |
| `d72ac167` | 2026-10-24T03:28:48-03:00 | round-41: freeze C1-C3 contracts and controls | 51996 | `pass=22 fail=0` exit 0 |
| `4f266ef2` (entering tip) | 2026-10-26 | round-51 closure | 51996 | `pass=22 fail=0` exit 0 |
| HEAD `075436b1` (working tree) | 2026-10-26 | — | 51996 | `MORI_SOURCES_APPENDONLY_SELFTEST pass=22 fail=0` exit 0 |

The printed count equals the number of case tuples in the three case-list functions (`_selftest_cases`,
`_selftest_dag_cases`, `_selftest_r41_dag_cases`): a grep of those lists gives 12 / 15 / 22 at `97b826a9` /
`265a955c` / `d72ac167`, so `pass=N` is the case count, not a coincidence.

The tool has not changed since the round-41 freeze:
`sha256sum tools/mori-sources-appendonly.py` → `75af8f6fc63dc736f07c02617bed4bf6c1ad7f880ffb49849b065b4d40d8f76b`,
and `git show d72ac167:tools/mori-sources-appendonly.py | sha256sum` → the same hash. So the tally `22` has been
the honest reading from the round-41 freeze through 12 further rounds of data commits.

So the growth past 12 is **`265a955c` (round-40 instruments, 12 → 15)**, and the later tally **`d72ac167`
(round-41 freeze, 15 → 22)**. Both are `git log -S` hits on the living documents as well:

    git log --format='%h %ad %s' --date=short -S 'pass=15' -- corpus/QUALITY.md corpus/README.md
    4dea3d09 2026-10-25 round-47: data — SKILL.md:912 pin repair …
    git log ... -S 'pass=22' -- corpus/QUALITY.md corpus/README.md
    8524904a 2026-10-26 round-52: data … / 4dea3d09 2026-10-25 round-47: data …
    git log ... -S 'pass=12' -- corpus/QUALITY.md corpus/README.md
    8524904a / 7c0b6232 (round-51) / f920eaf7 (round-39 data)

## 2. Timeline of the `pass=12` pins — `corpus/QUALITY.md:909` and `corpus/README.md:608`

Both pins were **true when they landed**. Row identities were verified by hashing the line at birth and at HEAD
(`git show <rev>:<path>` and sha256 of the single line):

| pin | at birth `f920eaf7` | at HEAD `075436b1` | line sha256 (16 hex) |
|---|---|---|---|
| QUALITY 112 check, `pass=12 fail=0` | line 909 | **line 909** (no drift) | `066bf0f17d613be1` both |
| README "Ancestry-based timed supersede", `pass=12 fail=0` | line **606** | line **608** | `b7b09365319cd114` both |
| README "Counter conformance v2", bare `--selftest` → `pass=9` | line **605** | line **607** | `c3ba7da3faa2fc48` both |

Timeline (all dates `-03:00`, from `git log -1 --format=%ad --date=iso-strict`):

1. `f920eaf7` **2026-10-24T01:02:20** — round-39 data lands QUALITY 112 (line 909, `Check: python3
   tools/mori-sources-appendonly.py --selftest → pass=12 fail=0`) and the two README round-39 rows (lines 605/606).
   The committed tool at that commit is the `97b826a9` bytes → prints 12. **The pins are correct at birth.**
2. `265a955c` **2026-10-24T01:31:20** — round-40 instruments grow the selftest 12 → 15. **The `pass=12` pins go
   stale here, 29 minutes after they landed.** No living-document line was added or changed in this commit.
3. `d72ac167` **2026-10-24T03:28:48** — round-41 freeze grows the selftest 15 → 22. The pins are now stale by 10.
   This same commit inserted one map row at the front of `corpus/README.md`
   (`| knowledge/conform-bindings-r41.md | …`, hunk `@@ -46,6 +46,7 @@`), which moves the two pin rows to 606/607.
4. `18fd68b0` **2026-10-25T08:08:04** (round-45) — one more front-of-file map row
   (`| knowledge/census-cgroup-levels-r45.md | …`, hunk `@@ -47,6 +47,7 @@`) moves the pin rows to 607/608.
5. `64c2d5fc` (round-49), `7c0b6232` (round-51) — touch the living documents; neither names these two pins and
   neither rewrites them.
6. `4f266ef2` (round-52 entering tip) — the frozen control still reads them stale:
   `.ufo/waves/round-52/evidence/control-c1-do-nothing.txt:12` `item living corpus/QUALITY.md:909
   expect=pass=12_fail=0 got=MORI_SOURCES_APPENDONLY_SELFTEST_pass=22_fail=0_rc=0 state=mismatch`, `:14` the same
   for `corpus/README.md:608`.
7. `8524904a` **2026-10-26T21:06:45** — round-52 data **supersedes** them without touching them: QUALITY 141
   (lines 1356-1365) quotes the stale pin and prints the live `pass=22`; the README "Round-52 corrections (living
   pins)" note at line 727 quotes `pass=12` and names `pass=22`. The comparator at data reads
   `.ufo/waves/round-52/evidence/c1-at-data.txt:11,14` `got=superseded state=ok`.

Stale window for the `pass=12` pins: `265a955c` → `8524904a` = **2 d 19 h 35 min**, spanning the data of rounds
40 through 52 (12 rounds of data commits with no supersession line), after having been true for 29 minutes.

Adjacent pin on the same instrument, `SKILL.md:912` (not in my named surface, recorded because it is the same
instrument): created at `daa1d4d2` with `pass=9`, rewritten to `pass=15` at `265a955c` (true then), stale from
`d72ac167` (1 h 57 min after 15 was written), repaired **in place** at `4dea3d09` (round-47, 2026-10-25T16:42:35)
to `pass=22`. Stale ~1 d 13 h.

## 3. `corpus/README.md:607` — the bare `--selftest` → `pass=9`: which round-39 command it meant

The row is the round-39 "Counter conformance v2" row; its third cell pins
`` `python3 .ufo/waves/round-39/conform.py <rev>` → `CONFORM=met` … `` and then pin text `` `--selftest` → `pass=9 fail=0` ``.
The command the `pass=9` belongs to is the round-39 conformance checker with its positional revision — it takes a
revision, and the `--selftest` flag is additive:

    python3 .ufo/waves/round-39/conform.py <rev> --selftest

Observed at HEAD with the round-39 file bytes (identical to the `f920eaf7` bytes:
`sha256sum .ufo/waves/round-39/conform.py` = `git show f920eaf7:.ufo/waves/round-39/conform.py | sha256sum` =
`fe0be179aba9df7150f0b6cdb50a5f9bbdb411efb1263b46ffa6b21d46ef7987`), run from scratch:

    python3 <lane>/.ufo/waves/round-39/conform.py --selftest
    conformance setup error: expected str, bytes or os.PathLike object, not NoneType
    exit=2
    python3 <lane>/.ufo/waves/round-39/conform.py 4f266ef2fdf74d8b046f5b4f5a5c4945f65b966d --selftest
    … PASS scratch … PASS selftest_conjunct …
    CONFORM_SELFTEST pass=9 fail=0
    exit=0

So: `pass=9` is real for the runnable form and the bare form names no command at all (it fails exactly as QUALITY
111 recorded for the round-38 checker, `corpus/QUALITY.md:898-903`). The row's pin is **not a stale tally — it is a
pin that never carried a runnable command**, from `f920eaf7` until round-52 superseded it at `8524904a` (2 d 20 h).
The round-39 receipt is itself non-literal, which is why the successor convention (round-51 closure item 7) was
needed: `.ufo/waves/round-39/evidence/c8-after-selftest.txt:1` reads
`command: r39 conform --selftest at f920eaf7` (no argv), while `.ufo/waves/round-39/w1/RevScorecard.md:42` records
the literal form as `conform.py 13bfba2 --selftest` → nine `PASS` lines and `CONFORM_SELFTEST pass=9 fail=0`.

## 4. Was any round's QUALITY/README edit an in-place rewrite of a pin? — no, for these two documents

    git log -p --format='COMMIT %h' -- corpus/QUALITY.md corpus/README.md | grep -cE '^-[^-].*pass=[0-9]'
    0

Zero removed lines carry a `pass=<digits>` tally anywhere in the history of the two documents. The round-52 data
commit removed **0 lines** from either file (`git show 8524904a --format='' -- corpus/QUALITY.md corpus/README.md |
grep -cE '^-[^-]'` → `0`), so its supersession is a pure append, as QUALITY 141 requires.

Two adjacent in-place edits exist and are worth naming because they are the only ones in this surface:

- `4bfa0490` (round-37, 2026-10-23T17:23:23) rewrote one **README coverage row in place** — the only removed
  `--selftest` line in the file's history (`grep -cE '^-[^-].*--selftest'` → `1`). A pipeline-split word diff shows
  the change is a pointer repair only: `` `8ff9bba` `` → `` `1caa242` `` in a paragraph, and a reflow in the third
  cell; its pin text `` (`--selftest` 6 cases) `` was left unchanged and still holds today
  (`python3 tools/mori-source-drift.py --selftest` → `MORI_SOURCE_DRIFT_SELFTEST: PASS (6 cases)`, exit 0).
  This predates QUALITY 141 and does not falsify it (no tally moved).
- `4dea3d09` (round-47) rewrote **`SKILL.md:912`** in place: `git show 4dea3d09^:SKILL.md | sed -n 912p` and
  `git show 4dea3d09:SKILL.md | sed -n 912p` carry `MORI_SOURCES_APPENDONLY_SELFTEST pass=15 fail=0` →
  `… pass=22 fail=0`, one row in its own "gate" table, line number unchanged. `SKILL.md` history holds 12 removed
  lines carrying a `pass=<digits>` tally. So the lane's "never an in-place rewrite" rule holds for
  `corpus/QUALITY.md` and `corpus/README.md` across their whole history and **has been violated in `SKILL.md`** —
  evidence for the round-52 in-lane-writer inventory (contract §5 item 8), not for a QUALITY/README rewrite.

## 5. Named limits observed against the frozen C1 counter (arm C, `LPIN`)

`count-c1.py:76-79` enumerates a living pin only when one line holds a `python3|bash <path> … --selftest` span
immediately followed by `(N/M)` or `→ [PREFIX ]pass=N fail=K`. Two pins on my surface fall outside that shape and
were never enumerated (`corpus/QUALITY.md:899-900` and the round-37 README row), so I re-ran them by hand:

- `corpus/QUALITY.md:899-900` (QUALITY 111): command span on line 899, tally `→ CONFORM_SELFTEST pass=6 fail=0`
  on line 900 — split across lines. Run at HEAD:
  `python3 .ufo/waves/round-38/conform.py 4f266ef2… --selftest --counter .ufo/waves/round-38/count-c1.py` →
  `CONFORM_SELFTEST pass=6 fail=0`, exit 0 (42.8 s). Still true; a hidden pin, not a stale one.
- round-37 README row: `(`--selftest` 6 cases)` carries no `pass=N fail=K`; still true (§4).

Both agree with the contract's named limit ("a pin split across lines is not enumerated"); at this tip the
enumeration gap hides no staleness, because the two stale pins were the ones enumerated (`living=4` at data =
`QUALITY.md:909`, `README.md:607`, `README.md:608` + the new `README.md:727`).

Nothing about the counters, predicates, controls or kill rules is proposed for change; §5 and the `SKILL.md`
observation are round-53 routed items and named limits for this round's report.

## 6. Line-number drift of the pin rows (why `path:N` labels age)

`README.md:605/606` (at birth) → `:606/607` (from `d72ac167`) → `:607/608` (from `18fd68b0`): each of the two
commits inserted exactly one row at the **front** of the file's coverage map, so an append-only document still
shifts every later line. `QUALITY.md:909` never moved (all later QUALITY rows append at the end). A `path:N`
reference to a living pin is therefore valid only at one tip: the round-52 contract's own labels
(`QUALITY.md:909`, `README.md:608`, `README.md:607`) are exact at the landed tip `075436b1` and wrong for the round
in which those rows landed (where the same rows were `:909`, `:606`, `:605`). The counter is not affected — it
derives the line from the scan and checks the expected string there — but any human or seat pointer copied from a
report is.

## 7. Lane writes seen while measuring (not mine, and a scoring hazard)

The round-39 conformance instrument cannot be kept out of the lane: `.ufo/waves/round-39/conform.py:54` sets
`SCRATCH_ROOT = os.path.join(LANE, ".ufo", "waves", "round-39", "scratch")`, so its selftest fixtures land there
whatever `TMPDIR` and cwd are. Observed while this report was being written (read-only `stat`/`find`):

    stat -c 'birth=%w mtime=%y %n' .ufo/waves/round-39/scratch
    birth=2026-10-24 01:26:25 -0300 mtime=2026-10-26 21:20:19 -0300   # parent predates this round
    ls .ufo/waves/round-39/scratch            # 4 entries, births 21:19:59, 21:20:03, 21:20:07, 21:20:19

i.e. fixture directories `mori-conform-selftest-*` are being born every few seconds by a concurrent wave seat while
this seat ran no conform selftest. The parent directory predates my first run (2026-10-24), so I attribute no
fixture to myself and deleted nothing (a live sibling fixture would be destroyed). `git status --porcelain` lists
`?? .ufo/waves/round-39/scratch/` as untracked.

That matters for scoring: `count-c1.py:527-531,562-565` snapshots `git status --porcelain --ignored
--untracked-files=all` before the run and flags every **new** line as a lane write. A pre-existing untracked
directory is harmless (`before` carries it), but any sibling write during the counter's own run — a wave report, a
conform fixture, a counter's scratch — appears as a new status line and turns `lane_writes` nonzero, which the
counter treats as a failure (line 438 appends `lane_writes` to `failed`). The L1's scoring run must therefore be
serialised against the rest of the wave; this is a race in the scoring environment, not in my surface.

## Findings

- **MED — `corpus/QUALITY.md:909`**: the `pass=12` check pin was true at birth (`f920eaf7`, 2026-10-24T01:02:20)
  and went stale 29 minutes later at `265a955c` (round-40, selftest 12 → 15), then stale by 10 from `d72ac167`
  (round-41, → 22); it sat unreconciled for 2 d 19 h across rounds 40-51 and was superseded only in round 52
  (`8524904a`, QUALITY 141).
- **MED — `corpus/README.md:608`**: same row class, same landings and same stale window as the QUALITY pin; the
  supersession note is `corpus/README.md:727`. Neither document was ever rewritten in place (0 removed tally
  lines), so the 12-round survival is an enumeration/discipline gap, not an edit accident.
- **MED — `.ufo/waves/round-39/conform.py:54` + `count-c1.py:527-531,562-565` (scoring race)**: the frozen round-39
  instrument writes `mori-conform-selftest-*` fixtures into the lane's `.ufo/waves/round-39/scratch/`
  (`SCRATCH_ROOT`) regardless of `TMPDIR`, and the C1 counter flags every *new* `git status --porcelain --ignored`
  line during its own run as a lane write. Four such fixtures were born between 21:19:59 and 21:20:19 while a
  concurrent wave seat ran the instrument; the L1's scoring run must have no sibling writing in the lane, or `C1`
  reads `lane_writes>0` and fails on a write that is not the claim's. (Parent directory predates this round:
  birth 2026-10-24T01:26:25; nothing deleted by this seat.)
- **LOW — `corpus/README.md:607`**: the bare `--selftest` → `pass=9` pin never named a runnable command; the
  command it meant is `python3 .ufo/waves/round-39/conform.py <rev> --selftest` (verified `CONFORM_SELFTEST
  pass=9 fail=0`, exit 0; bare form exit 2). It survived un-runnable for 2 d 20 h until `8524904a`.
- **LOW — `SKILL.md:912` (round-47 `4dea3d09`)**: the lane's only observed in-place rewrite of a tally pin
  (`pass=15` → `pass=22`, same line number), at odds with the "supersession, never rewrite" house rule that holds
  for the two documents QUALITY 141 governs; route with the in-lane-writer inventory (contract §5 item 8).
- **LOW — `corpus/README.md:605-606` → `:607-608` line drift**: two one-line insertions above the pin rows
  (`d72ac167` round-41, `18fd68b0` round-45) move every `path:N` pointer to them; the round-52 contract labels are
  valid at the landed tip only.
- **LOW — `count-c1.py:76-79` arm-C shape (`LPIN`)**: pins with the tally on the following line
  (`corpus/QUALITY.md:899-900`, `pass=6`) or phrased as "N cases" (round-37 README row, 6 cases) are not
  enumerated; both were re-run here and are still true today, so no staleness is hidden at this tip — a round-53
  counter item, not a change proposed for this round.
- **LOW — `.ufo/waves/round-39/evidence/c8-after-selftest.txt:1`**: the round-39 receipt header `command: r39
  conform --selftest at f920eaf7` is not a literal argv, which is how the un-runnable pin survived round 39
  unnoticed; the literal form appears only in `.ufo/waves/round-39/w1/RevScorecard.md:42`.
