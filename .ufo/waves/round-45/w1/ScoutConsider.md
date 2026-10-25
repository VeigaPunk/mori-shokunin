# ScoutConsider — considerthese proposal census (mori round 45, wave 1)

Lane `/home/vgpnk/Projects/shokunin/mori-shokunin`, HEAD
`3ad8faaa637ae466c61f9427fea1c208bf49ea82` (2026-10-25 07:40:05 −03, the r45
freeze). Read-only: this report is the only file written; `considerthese/` bytes
are unchanged (§6 digests); no git mutation, no tool installed, no subagent.

## 0. Inputs and id scheme

`considerthese/` holds six reflections, `2026-10-19.md` … `2026-10-24.md`; there
is **no `2026-10-25.md`**. Ids here are `P<file-dd>-<n>`, numbering the bullets
inside each file's own proposals section. For `2026-10-24.md` the lane already
uses `P1`–`P4` (r44 `w1/ScoutConsider.md` §1 and `corpus/lessons/round-44.md:101`),
so `P24-n` keeps those numbers.

Depth note: one proposal is grounded end to end (§3, `P24-3`); the rest are
triaged by artifact presence at the tip with the grep named in the row. A triage
row says "absent" only about the instrument the proposal asks for — never that
the underlying evidence is absent. Where a row cites `tools/*`, the load-bearing
claims were re-pinned with `git grep <rev>`; at the time of this pass three
tools carry uncommitted r45 edits (`mori-gate-registry.py`,
`mori-round19-regressions.py`, `mori-routed-check.py`), so a worktree-only read
of those files would not be rev-pinned evidence.

## 1. Each file's own marking (verbatim heading, line, count)

| file | marking heading (verbatim) | line | proposals |
|---|---|---|---|
| `2026-10-19.md` | `## Self-improvement suggestions (proposals only, not acted on)` | 15 | 6 (17–22) |
| `2026-10-20.md` | `## Self-improvement suggestions (proposals only, not acted on)` | 18 | 5 (20–24) |
| `2026-10-21.md` | `## Self-improvement suggestions (proposals only, not acted on)` | 18 | 5 (20–24) |
| `2026-10-22.md` | `## Self-improvement proposals (proposals only, not acted on)` | 24 | 4 (26–29) |
| `2026-10-23.md` | `## Suggestions for improving my own reviews (proposals only)` | 15 | 5 (17–21) |
| `2026-10-24.md` | `## Suggestions for improving my own reviews (proposals only)` | 19 | 4 (21–24) |

Two wordings exist: "proposals only, not acted on" (19–22) and "proposals only"
(23–24). No file contains a "not implemented" string; the lane's corroboration
for "not acted on" is `corpus/lessons/round-42.md:73` ("one unimplemented
proposal mined … No other proposal was implemented") and the r43/r44 considerthese
sections. `2026-10-24.md` also has a `## Things I could not verify` section (15),
which is a finding, not a proposal.

## 2. Proposal census, per file

Status vocabulary: **implemented** (instrument landed), **criterion-only** (a
QUALITY rule exists, no instrument), **present-but-unwired** (parts exist, the
proposed arm does not), **present-but-unreviewed** (the mechanism exists, the
periodic review the proposal asks for does not), **partial** (some of the named
standing items are tracked, others are not), **opened-not-instrumented** (the
question was raised and routed, no artifact), **absent**, **practice-only**
(addresses the operator's own daily review; no lane artifact is the honest form).

### `2026-10-19.md`

| id | proposal | status | evidence at `3ad8faaa` |
|---|---|---|---|
| P19-1 | verify every path/SHA/test count in `SKILL.md`/`LOG.md` at HEAD | absent in general | no general verifier; nearest narrow arms: `tools/mori-round41-calibration.py` (r40-only, `RECORD_PATHS` at :16) and `tools/mori-gate-registry.py` (registry rows only) |
| P19-2 | run `--selftest` + `mori-silence-cases.sh` in a clone each review, compare counts | present-but-unwired | `tools/mori-silence-cases.sh` and per-round selftests exist; `ls tools \| grep -iE "run\|all\|suite"` → no runner |
| P19-3 | report EDQUOT blind spot every time; suggest read-only journal-count signal | absent | `git cat-file -e HEAD:tools/mori-quota-surface.py` → rc 128; `PROVINCE.md` FR2 still Frontier; r23 withdrawal |
| P19-4 | timeline of drift results + axis scores to calibrate thresholds | absent as instrument | `grep -rln trend tools/` → no output; the data lives in `SCORECARD.md` axis table and `corpus/evidence/` |
| P19-5 | review the drift pin's masked-field list | present-but-unreviewed | mask rules are explicit fixed regexes (`tools/mori-census.sh:2729-2734`); an edit surfaces as drift; no periodic review arm |
| P19-6 | track standing items (draft PR #1, 0/4 promotion, saturation) | partial | `SCORECARD.md:639` saturation 8/10, N=3; `:551` promotion 0/4; no `PR #1` string in `SCORECARD.md`/`LOG.md` |

### `2026-10-20.md`

| id | proposal | status | evidence |
|---|---|---|---|
| P20-1 | own no-harm diff each round (finding ids + alarm classes) | absent as instrument | `grep -rln "no.harm" tools/` → only `mori-round14-regressions.py`; per-round work is seat prose (e.g. r25 `w2/ReviewNoHarmCensus.md`) |
| P20-2 | run each round's gate, re-run older gates at HEAD | present-but-unwired | seven gates (`tools/mori-round1[3-9]-*regressions.py`); no aggregate runner |
| P20-3 | log author vs outside verdicts as calibration | practice-only | prose only: `SCORECARD.md` 18, `LOG.md` 12 `verifier-spotcheck` mentions; no table instrument |
| P20-4 | count seat-process violations per round | absent | no counter tool; violations live in lessons |
| P20-5 | age the carried debts | absent | no tool; debts tracked as prose rows |

### `2026-10-21.md`

| id | proposal | status | evidence |
|---|---|---|---|
| P21-1 | retention gate + content review on each day's new commits | present-but-unwired | both tools registered (`SKILL.md:178,181`); neither takes a revision *range* (`--since` occurs only in census/r16/r17) |
| P21-2 | one selftest runner with one scratch contract | absent | `SKILL.md:585-586` is guidance only; registry rows still carry different `TMPDIR` rules (e.g. `:178` "TMPDIR must be `<repo>/.scratch`") |
| P21-3 | track evidence growth per round | absent | same capability as `P24-3`; `git grep -n growth 3ad8faaa -- tools SKILL.md corpus/QUALITY.md corpus/knowledge` → no output |
| P21-4 | track closure lag | absent | no closure instrument; `tools/mori-wave-settlement.py` counts report settlement, not closure |
| P21-5 | follow open disputes like M6 to a ruling | opened, not instrumented | `corpus/lessons/round-20.md:27` (M6 "open disagreement for the non-author closure"); `PROVINCE.md` Round21 correction rejects the r20 re-pin; no file names `WATCHDOG_STALE` in `round-21.md` |

### `2026-10-22.md`

| id | proposal | status | evidence |
|---|---|---|---|
| P22-1 | re-run each committed selftest output at its named revision | **implemented** | `tools/mori-routed-r24.py --rerun` (`:11`, `:899`), registered `SKILL.md:721` |
| P22-2 | keep an "awaiting closure" ledger | absent | `grep -rln awaiting tools/ corpus/knowledge/` → one unrelated r14 note |
| P22-3 | track mutation survivors as coverage debt | criterion-only | QUALITY 114 (`corpus/QUALITY.md:927-929`); `git ls-files .ufo/waves/round-24 \| grep -ci survivor` → 0 |
| P22-4 | check dispatch times against commit times | absent | no backdate/committer arm in `mori-routed-r24.py` (`grep -n "backdat\|commit time\|committer"` → none) |

### `2026-10-23.md`

| id | proposal | status | evidence |
|---|---|---|---|
| P23-1 | warn about weak counters early (re-run pre-data controls) | absent as instrument | `grep -rln "pre-data" tools/` → none; the practice appears as a r45 seat (`ExecControlReceipts`) |
| P23-2 | re-run every OOM-killer fixture set daily | present-but-unwired | six sets in `tools/fixtures/mori-oom-killers/`; `--cases` takes one file per run, no multi-set runner |
| P23-3 | keep a structured verdict table | absent | no `LEARNING.md` in `corpus/`; no table tool; verdicts are prose in per-round spot-checks |
| P23-4 | point out tools without self-tests | **implemented** | `tools/mori-gate-registry.py` `no_selftest` arm (`:237`, `:262`, counted twice at the rev), registered `SKILL.md:184` (the C2 auditor this round hardens) |
| P23-5 | write a per-round digest when volume is high | absent | no digest instrument; `grep -rln "digest table"` → nothing |

### `2026-10-24.md`

| id | proposal | status | evidence |
|---|---|---|---|
| P24-1 | check that frozen instruments replay off-host | criterion-only | QUALITY 115 (`corpus/QUALITY.md:938`, mined r43); no sweep tool |
| P24-2 | keep a cumulative survivor ledger | criterion-only | QUALITY 114; no cumulative artifact |
| P24-3 | watch repository growth from scratch output | **absent** | §3 |
| P24-4 | reproduce headline numbers mechanically | criterion-only | QUALITY 117 (`:946`, mined r44) + `tools/mori-round41-calibration.py` (r40-only) |

Net: of 29 proposals, 2 are implemented (`P22-1`, `P23-4`), 4 are
criterion-only (`P22-3`, `P24-1`, `P24-2`, `P24-4`), 5 are present-but-unwired
(`P19-2`, `P19-5`, `P20-2`, `P21-1`, `P23-2`), 1 is partial (`P19-6`), 1 is
opened-not-instrumented (`P21-5`), 1 is practice-only (`P20-3`), and 15 are
absent. `P24-3` is the only one already routed *into* this round (r44 lesson:
"P3 … remains unimplemented and is routed to round 45",
`corpus/lessons/round-44.md:112`).

## 3. Grounded proposal — `P24-3` "Watch repository growth from scratch output"

Reflection text (`considerthese/2026-10-24.md:23`): "The r41 freeze alone added
165 files and about 40k lines, and 71 files under `.scratch/` are now tracked
even though the selftests treat `.scratch/` as a temp dir. I could report daily
growth and which tracked scratch files no receipt cites, without judging whether
they belong." Its sibling is `P21-3`.

### 3.1 Still unimplemented at the tip — observed

- `git ls-tree -r --name-only 3ad8faaa | grep -ci growth` → **0** (no file named
  for it anywhere in the tree). `git grep -n growth 3ad8faaa -- tools SKILL.md
  corpus/QUALITY.md corpus/knowledge` → **no output** (no tool, no registry row,
  no criterion, no knowledge note).
- No seat in this round builds it: the only r45 spec item that names `growth` or
  `considerthese` is this one (`ScoutConsider`); the other 36 items do not.
- The premise is live and worse than when written: tracked `.scratch/` files
  were **71 at `d72ac16`** (r41 freeze) and are **225 at the tip** (`git ls-tree
  -r --name-only <rev> -- .scratch | wc -l`), 29 MB on disk.
- `.gitignore` lists only `.ufo/interactive-sessions/`, `.ufo/worktrees/`,
  `__pycache__/`, `*.pyc` — no `scratch` entry (`git check-ignore -v
  .scratch/…/renamed-audit.out` → rc 1), so the tracked-vs-temp tension is real,
  as `tools/mori-retention-gate.py:459` also shows (`expected_tmp =
  (root / ".scratch").resolve()`).

### 3.2 What it points at

No tool is named; the entries it implies are: the tracked `.scratch/` tree, the
`.gitignore` that does not exclude it, the scratch contract in
`tools/mori-retention-gate.py:459` and `SKILL.md:585-586`, and the accounting
precedent `tools/mori-retention-reconcile.py` (population recount at a revision;
emits `raw_total`/`scanner_total`/`allowlisted`, `privacy_clearance:false`, never
growth deltas) and `tools/mori-evidence-loss.py` (retained-copy audit against
recorded SHA + commit; set-difference of required vs retained, never volume).

### 3.3 Capability verdict: **absent; the primitives are present and unwired**

Observed: nothing emits file/byte/line growth, per-round or per-day; nothing
computes the uncited-scratch set. `tools/mori-disk-rate.py` is a different
quantity (`/proc/diskstats`). The two primitives that would carry it exist —
population enumeration at a revision (`retention-reconcile`, `evidence-loss`) and
git object reads — but neither is wired to a growth or citation arm.

### 3.4 What implementing it would mean concretely

A new read-only instrument (working name `tools/mori-growth.py`), not an edit to
an existing one:

1. argv `--repo DIR --since REV [--rev REV] [--scratch] [--selftest]`, git
   objects only (`--no-replace-objects`, clean env, timeout), never the working
   tree — the `mori-routed-r24.py` pattern.
2. one schema (e.g. `mori-repo-growth-v1`): `tracked_total` at both revisions,
   `files_added`, `lines_added` (`diff --numstat`, binary rows counted
   separately), `bytes_added`, `ufo_share`, per-round breakdown, and, under
   `--scratch`, `tracked_scratch` + `uncited[]`.
3. report-only: a finding id, no alarm, no judgement of whether a file belongs
   (the reflection says so; removal authority is souji/operator).
4. a frozen case set before the tool (`--selftest`), including the hard case in
   §3.4a; a synthetic repo under `TMPDIR` for the add/delete/binary arms.
5. wiring: an 8-cell row in `SKILL.md` `## Gates` (else this round's C2
   predicate fails its own `unregistered=0` over `tools/*.py|*.sh`), and one
   QUALITY criterion citing the reflection by title, house shape
   (statement / Rationale / Check / Shown able to fail / Not covered).

**3.4a The definitional blocker that must be settled first (measured).** "No
receipt cites" cannot be implemented as a plain membership test: at `7cb59c68`
the r44 scout found **3** uncited files (`.scratch/round22/trial{1,2,3}.json`);
at the tip, by exact-path membership over tracked `*.md/*.json/*.txt`, **0 of 225
are uncited**, because the only tracked text naming those three is
`w1/ScoutConsider.md:140-142` — the r44 report that listed them *as uncited*
(re-running the r44 regex census at the tip also prints `uncited=0`). Publishing
the census discharges its own finding, so the arm is vacuous unless "receipt" is
defined as something narrower: a `corpus/evidence/*` or
`.ufo/waves/<round>/evidence/*` file (optionally a schema-bearing record), with
seat reports and scout/critic `w1/*` prose excluded. "Shown able to fail" then
has a real anchor: the same census at `d72ac16` prints 71 tracked / 40 uncited,
which the tip cannot reproduce.

### 3.5 Is it in PROVINCE?

`PROVINCE.md:3` scopes the lane to "fleet & host observability — whether the
fleet, its waves and its host are alive and progressing"; the appended round-18
note already declares a **Core** row for mori's own committed evidence ("Core,
own-evidence retention") and the round-22 section fixes the "own-evidence
accounting boundary", both appended rather than rewriting the header. A growth census of mori's own git tree
is own-record accounting, detection-and-report only, with no remediation; it
touches neither refused domain (dispatch/orchestration → kumitate; OS/package/
service → tsukuroi). **Verdict: in PROVINCE as own-record accounting by the
round-18/22 precedent, not by the domain sentence** [INFERENCE]; landing it
requires an appended scope note in the `## RoundNN` style (PROVINCE.md is
append-only so sibling line-range pointers stay valid), and it must leave
"whether a tracked scratch file belongs" to souji/operator — answering that
would be out of province. It is not a census surface: no `SURFACE` row, no
baseline re-pin.

## 4. Measured figures (all read-only, at `3ad8faaa` unless stated)

| figure | value | command |
|---|---|---|
| tracked files | 11834 | `git ls-files \| wc -l` |
| tracked under `.ufo/` | 11215 | `git ls-files \| awk -F/ …` |
| tracked `.scratch/` | 225 (29 MB) | `git ls-tree -r --name-only HEAD -- .scratch \| wc -l`; `du -sh .scratch` |
| same at `d72ac16` | 71 | `git ls-tree -r --name-only d72ac16 -- .scratch \| wc -l` |
| r41 freeze diff | 165 files, 40245 insertions | `git show --shortstat d72ac16` |
| r44 freeze → r45 freeze | 63 files, 17778 insertions | `git diff --shortstat 7cb59c68 3ad8faaa` |
| largest wave trees | r17 2273, r20 2190 files | per-round `git ls-files .ufo/waves` count |

The reflection's "about 40k lines" is exactly 40245; its "71 files under
`.scratch/`" is the `d72ac16` count, now 225.

## 5. Remaining unknowns

- Whether the L1 wants `P24-3` landed in r45 at all. It is routed here, but no
  r45 item builds it; if it is not landed this round it should be re-routed to
  r46 explicitly rather than left "routed" a second time.
- Cadence: the reflection says "daily"; the lane moves in rounds, so a per-round
  census (or a `--since <date>` arm) is the implementable form [INFERENCE].
- Byte vs line growth, and whether `.ufo/` share is by files or bytes: the two
  reflections say "files added, bytes added, and the share under `.ufo/`"
  (`2026-10-21.md:22`) and "daily growth" (`2026-10-24.md:23`) without fixing the
  basis. The criterion must fix it.
- `P19-6`'s "draft PR #1" has no trace in `SCORECARD.md`/`LOG.md` at the tip; I
  did not search the fleet repo (out of my read scope for this question).

## 6. Non-edit proof and commands

`md5sum considerthese/*.md` at the end of this pass equals the before-state:
`49f5f6bf… 2026-10-19.md`, `7a15640b… 2026-10-20.md`, `1398ad50… 2026-10-21.md`,
`b9b03fb6… 2026-10-22.md`, `848ca8ca… 2026-10-23.md`, `901bd4de… 2026-10-24.md`.

Read-only commands used: `git ls-files`, `git ls-tree`, `git grep <rev>`,
`git cat-file -e`, `git check-ignore -v`, `git log --oneline`, `git show
--shortstat`, `git diff --shortstat`, `grep -rn` over `tools/`, `SKILL.md`,
`corpus/`, `PROVINCE.md`, `du -sh`. Scratch: `TMPDIR` under
`.ufo/waves/round-45/tmp/ScoutConsider` only. Nothing was installed or upgraded.
