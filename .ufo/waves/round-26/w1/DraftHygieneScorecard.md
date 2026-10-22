# DraftHygieneScorecard — round 26 wave 1 (hygiene, not a claim)

Seat: `MoriR26.DraftHygieneScorecard` (scribe). Scope: routed defects **R2, R4, R6** from
`corpus/lessons/round-25-verifier-spotcheck.md:180-196`. Deliverable: draft append-only correction
text (exact old text + the appended text) for the L1 integration owner. No product file was
edited by this seat; the only lane write is this report.

Measured against lane tip `248408f5` (round 25 admitted, `MANIFEST.json` rounds[455]).

## What I verified (own measurements, not wave-2 hearsay)

| Fact | How | Result |
|---|---|---|
| MANIFEST: mori round 13 | `jq '.rounds[] \| select(.lane=="mori" and .round==13)' MANIFEST.json` (fleet root) | `verdict "rejected-harmed"`, `admitted false`, `verdicts.operability "improved"`, commit `dbe85009` |
| MANIFEST: mori round 14 | same, `.round==14` | `verdict "admitted"`, `admitted true`, `verdicts.operability "unchanged"`, commit `0fa5e0de` |
| MANIFEST: mori round 25 | same, `.round==25` | `capabilities_added[0]` already reads "bounded to block-style configs (72 of 307 probe configs read a false 100, routed R1)" — the fleet record is scoped; the lane's SCORECARD row is not |
| 72 of 307 false-absent, re-derived | re-ran the wave-2 differential probe (copy of `harness/diff_vs_bun.py`, read-only, in my scratch) against the tip tool blob `239dd8be…`, Bun 1.4.3 | `total 307`, `FALSE_ABSENT 72`, `FALSE_SET 12`, `NUMBER_ON_PARSE_ERROR 21`, `DEFAULT_ON_PARSE_ERROR 15`, `abstain 155`, `agree 32`; false-absent by header `H4 31, H9 31, H1 4, H2 4, F1 1, X1 1` (62 header spellings + 10 child/root forms) |
| D5 rule and falsifier | `tools/mori-routed-r24.py` read + predicate replay on the tip blob and on my proposed row text | D5 reads the **Last change** cell: `if score != round1 and D5_ROUND1_RE.search(last_change)` (`tools/mori-routed-r24.py:739-741`); with the row's Last change set to `round 1` the gate goes red `axis_stale_round_1: operability`; my proposed row text keeps D5 held |
| D5 at the tip | `python3 -I -B tools/mori-routed-r24.py --repo . --rev 248408f5` | `items 4, held 4, mismatches 0`, exit 0 |
| Upstream clamp/floor/throw | `curl` of `sdk.ts`, `async/job-manager.ts`, `eval/agent-bridge.ts`, `task/workpool.ts`, `docs/tools/eval.md` at tag `v18.12.6` (2026-10-22) | `sdk.ts:2284` `maxRunningJobs: () => Math.min(100, cfgAsyncMaxJobs.get(settings)),` (sha256 `c0228add…` = S099); `job-manager.ts:334` `Math.max(1, Math.floor(value ?? DEFAULT_MAX_RUNNING_JOBS))`, `:43` `DEFAULT_MAX_RUNNING_JOBS = 15`, `:370-373` throw in `register()` (sha256 `0f37afaa…` = S098); `agent-bridge.ts:210` `manager.register(`; `workpool.ts:175,363` `manager.register(` and **no** `atCapacity` in either file; `docs/tools/eval.md:258` "agent() fails with `Background job limit reached` once that cap is full" (sha256 `fb2fc4a1…` = S103) |
| Round-25 commit order | `git log --format='%h %ad %s' --date=format:'%H:%M:%S' --reverse 28b79d3d..248408f5` | A1 `51ddd01` 07:05:20 · A3 `042d75b` 07:20:37 · tool `e54b644` 07:44:02 · A4 `9b1a2f1` 07:44:17 · A5 `efaa157` 07:54:12 · D5 code `e06d4a0` 08:07:03 |
| Stale pointer strings in the standing table | read `SCORECARD.md:10-15` | none of "per-surface notes still owed", "14/14", "no drift pin yet", "`progressing-weak` deferred" occurs there any more; three of six Last change cells still read `round 1` |

Not run (unrun is not a pass): the tool's own `--selftest` (frozen PASS 21/21 is evidence-verified at
`d3b7af2a`, not re-run here); the lane retention scan (not this seat's scope); Bun's parse of the
live host config (I read the host config's **structure** only — one column-0 `async:` key, one
direct `maxJobs:` child — and did not print its value, per the round-26 privacy bound).

## Ready-to-paste text

### 1. `SCORECARD.md` — append after the round-26 declaration block (current last line 1602)

```markdown
## Round 26 corrections (routed R2 and R4 — hygiene, not a claim)

Append-only: the round-25 sections above are left as filed, and each statement corrected here is
named with its old text.

### R2 — the round-25 runway capability row is scoped, not absolute

Old text (`SCORECARD.md:1568`, round-25 capability row "harness background-job runway read", "What
it can now do" cell): "report the configured `async.maxJobs` from one settings file, the clamp and
setting default compiled into the installed omp binary, the effective cap `max(1, min(clamp,
base))`, and a verdict that never turns an unreadable, ambiguous or unparseable input into a number"

That clause is false as written and is withdrawn. What the tool does: it is a line grammar over ONE
block-style settings file, and it abstains (`RUNWAY_UNKNOWN`, exit 2) only on the malformed forms it
can name. On other spellings of the same setting it reports a number. Re-measured at the round-26
entering tip `248408f5` with the tool blob `239dd8be…` and the round-25 wave-2 differential probe
(307 generated configs, Bun 1.4.3 as the omp-side parser): 72 of 307 configs read a false 100
(`RUNWAY_DEFAULT`, exit 0) where omp's parser reads 50 — 62 from unrecognised `async` header
spellings (`&a async:` and `"\x61sync":`, 31 each) and 10 from child or root forms under plain
headers (`{maxJobs: 50}`, `!!str maxJobs: 50`, `&a maxJobs: 50`, `"max\u004aobs": 50`, the flow root
`{async: {maxJobs: 50}}` and the indented root); 12 more report a configured number omp's parser does
not read as that number, and 36 (21 + 15) report a number or the default for files omp's parser
rejects. The claim that holds: the tool reads a block-style single settings file — a column-0
`async:` key with a direct `maxJobs:` child — and abstains on the forms it can name. The defect is
routed (round-25 R1: make rule 1 abstain on any top-level form it cannot read the way omp does); the
fleet record already carries the scoped form (`MANIFEST.json` rounds[455] `capabilities_added[0]`:
"bounded to block-style configs (72 of 307 probe configs read a false 100, routed R1)"). Evidence:
`.ufo/waves/round-25/w2/ReviewRunwayCode.md` F1–F2; the entry
`corpus/knowledge/harness-job-capacity-r25.md` already marks the false number. The probe corpus and
script are not committed to the lane (round-25 R1 asks for that); the 72 figure was re-derived by
re-running the wave-2 seat's copy read-only against the tip tool blob.

### R4 — three residuals of the round-25 D5 rewrite

**R4a — the standing Axes table's operability row.** The row credited round 13 with the move to 7.
Round 13 closed `rejected-harmed` (`MANIFEST.json` rounds[13]: `admitted false`), so its
self-assessed 6 → 7 was never admitted, and 7 was first admitted in round 14 (rounds[14]:
`admitted true`, `verdicts.operability "unchanged"`; `SCORECARD.md:793` reads "7 held"). The row is
corrected in place (old and new text below).

Old (`SCORECARD.md:11`):

| operability | 7 | census `--selftest` PASS (134 cases) before and after round 24 (`SCORECARD.md` round-24 measured outcome); held 7 in every round table since round 13 | round 13 (6 → 7) |

New:

| operability | 7 | census `--selftest` PASS (134 cases) before and after round 24 (`SCORECARD.md` round-24 measured outcome); held 7 in every round table since round 13, first admitted in round 14 (round 13 closed rejected-harmed) | round 14 (6 → 7; round 13's self-assessed 7 was not held) |

The score cell stays 7 (D5 pins it from `SCORECARD.md:1499-1506` at `28b79d3d`). The gate still
holds on this row text (replayed against the gate's own parser and predicates; the falsifier, Last
change `round 1`, turns D5 red with `axis_stale_round_1: operability`). If the standing table is
preferred to read "7 first admitted" rather than a move, the equivalent Last change cell is
"round 14 (7 first admitted; round 13's self-assessed 7 was not held)".

**R4b — the D5 note.** Old text (`SCORECARD.md:1584`, last line of the round-25 wave-2 corrections
bullet): "`28b79d3d`). D5 checks scores only, not evidence pointers or Last change text."

That sentence is wrong about the Last change cell. D5 checks two cells: the Score cell against the
pinned base scores, and the Last change cell for a stale `round 1` (round-25 contract A5: "no row's
Last change reads `round 1` unless its score equals its round-1 value"; `tools/mori-routed-r24.py:739-741`
implements it). It does not check the evidence-pointer cell. Corrected statement: "D5 checks the Score
cell and the Last change cell (no row's Last change may read `round 1` unless its score equals its
round-1 value); it does not check the evidence-pointer cell." This is why R4a lies inside the gate's
scope.

**R4c — the round-12 paragraph that describes the standing table.** Old text (`SCORECARD.md:620-621`,
round-12 section): "Correction to the score table at the top of this file (frozen at round 1; 4 of 6
pointers stale — STATE dossier §2): the table is left as filed; this section's scores supersede it.
Stale pointers:" (the pointer list continues at `:622-623`).

That paragraph is stale after the round-25 D5 rewrite (`e68855d5`), which replaced the standing
table: the table's scores are now the closure-admitted round-24 scores (`SCORECARD.md:1499-1506` at
`28b79d3d`; the note at `SCORECARD.md:17-19`), only three of the six Last change cells still read
`round 1`, and none of the four pointer strings it names at `:622-623` ("per-surface notes still
owed", "14/14", "no drift pin yet", "`progressing-weak` deferred") occurs in the standing table any
more. The scores it defers to are superseded too: that section's table (`:612-618`) reads
calibration 5 → 6 and operability unchanged 6, while the standing table holds calibration 5 and
operability 7. Superseding statement: the standing table is the round-25 D5 rewrite of the
closure-admitted round-24 scores; the round-1 pointer enumeration at `:622-623` is historical and no
longer describes that table.
```

### 2. `corpus/lessons/round-25.md` — append after line 110

```markdown
## Corrections appended in round 26 (routed defect R6)

Append-only: the sentences above are left as filed; each one is named below with its correction.

- **"The harness job cap is 100, whatever the config says."** (line 9, headline of the first learned
  fact) is false below 100. Upstream clamps with `min(100, async.maxJobs)` and floors at 1:
  `sdk.ts:2284` `maxRunningJobs: () => Math.min(100, cfgAsyncMaxJobs.get(settings)),` (v18.12.6,
  sha256 `c0228add…`, S099) and `async/job-manager.ts:334`
  `return Math.max(1, Math.floor(value ?? DEFAULT_MAX_RUNNING_JOBS));` with
  `DEFAULT_MAX_RUNNING_JOBS = 15` at `:43` (sha256 `0f37afaa…`, S098). A configured value below 100
  is honoured. The lesson's own body (line 12) is right that this host's configured value is above
  100 and its effective cap is 100; only the headline is wrong. Corrected headline: "**The harness
  job cap is `min(100, async.maxJobs)`, floored at 1 — 100 is the ceiling, not the value.**"
- **"only registration paths (explicit async bash, task spawns) throw `Background job limit reached
  (100)`"** (line 16, second learned fact) omits `agent()` and `workpool()`. The throw is inside
  `register()` and fires for every caller: `async/job-manager.ts:370-373`. `eval/agent-bridge.ts:210`
  calls `manager.register("task", …)` with no capacity pre-check, and `task/workpool.ts:175` and
  `:363` also call `manager.register(`, with no `atCapacity` test in either file. Upstream's own
  documentation says so: `docs/tools/eval.md:258` — "`agent()` fails with `Background job limit
  reached` once that cap is full" (v18.12.6, sha256 `fb2fc4a1…`, S103). Corrected sentence: "every
  `register()` call throws at the cap — explicit async bash, task spawns, eval `agent()` and
  `workpool()`; only the auto-backgrounded bash and eval branches fall through to a foreground run
  (S112, S113)."
- **"amendments A1–A4 each landed before the code it governs"** (lines 4-5, header) is wrong for A4
  and omits A5. Commit order and local times: A1 `51ddd01` 07:05:20, A3 `042d75b` 07:20:37, the C1
  tool `e54b644` 07:44:02, A4 `9b1a2f1` 07:44:17, A5 `efaa157` 07:54:12, the D5 code `e06d4a0`
  08:07:03. A1 and A3 landed before the tool; A4 landed 15 s after it and its own text describes
  `e54b644b` as "the landed tool"; A5 landed before the D5 code and is not listed at all.
  Corrected header clause: "amendments A1 and A3 landed before the C1 tool, A4 landed 15 s after it
  and records the banner-gate deviation, and A5 — which widened C1 with item D5 — landed before the
  D5 code".
- **"Fix: amendments A1, A3 and A4 before the tool landed"** (line 48, inside M3) is false for A4 by
  the same 15 s. Corrected clause: "amendments A1 and A3 before the tool landed; A4 landed after it
  and records its deviation".
- **"Refusals in this session's transcripts all name 100."** (line 18, third learned fact) is false
  as scoped. The census (`RefusalCensus.md`) scanned the whole omp session-transcript store — files
  with mtime in 2026-10-19..2026-10-22, 31,191 files in window, 3,424 transcripts, 45 workspaces
  (`:70-73`) — not one session's transcripts. Its delivered-refusal tiers are all 100: `toolresult`
  6,562 occurrences in 342 files, `harness` 5,313 in 150, `harness_error` 48 in 24 (`:89-105`); the
  lesson's 48 and its 2026-10-20T13:55Z..2026-10-22T10:04Z window are the `harness_error` tier and
  are right. The tiers that also count agent-authored prose contain exactly one occurrence naming
  15 — `all` 100=20,322 and 15=1, `transcript` 100=8,973 and 15=1, `prose` 100=2,411 and 15=1, the
  single one dated 2026-10-22T10:05:15Z (`:75-110`); upstream's fallback constant is 15
  (`job-manager.ts:43`), the undefined-option fallback S110 records. Corrected sentence: "Every
  delivered refusal names 100 — 48 as failed tool calls in 24 files from 2026-10-20T13:55Z to
  2026-10-22T10:04Z; the wider counts that also include agent prose contain one occurrence naming
  15, the undefined-option fallback."
- **"The SCORECARD Axes table at its top still shows round-1 scores (coverage 5, operability 6,
  depth 4)"** (lines 97-99, "For round 26") was true when written and is false at the round-25 tip:
  `e68855d5` brought the table to the closure-admitted round-24 scores and `e06d4a0` counted the
  check as item D5. The correction block at lines 101-104 already says so, but it shadows this
  bullet instead of removing it, which QUALITY 77 calls a defect ("the superseded wording is
  removed, not shadowed"). This bullet must be removed from the file rather than shadowed again;
  that removal edits the filed round-25 lesson and is left to the integration owner.
```

## Findings and conflicts for the canonical judge

1. **QUALITY 77 vs append-only (unresolved, needs a ruling).** QUALITY 77 (`corpus/QUALITY.md:349-355`)
   requires a corrected fact's superseded wording to be *removed, not shadowed*. My lane bound for
   this wave says: draft append-only corrections, never rewrite filed history, except the Axes table
   row itself. The two drafts above are therefore append-only and each names the old text; on a
   strict QUALITY 77 reading, the R2 capability row, the R4b D5 note, the R4c round-12 paragraph and
   the five R6 lesson sentences are still "contradicted lines left standing". Precedent both ways:
   the lane appended a correction to `corpus/lessons/round-24.md:98-100` in round 25 and the
   round-25 closure routed the same pattern as a defect (round-25 spot-check R5: "D3 holds beside
   the uncorrected `PASS 6/6` line"). Ruling needed: does round 26 sweep these in place, or does it
   append and accept the QUALITY 77 exposure? My drafts are written to be usable either way — each
   appended block names the exact old text, so an in-place sweep can be derived from it.
2. **R6, last item, cannot be closed append-only.** The shadowed "For round 26" Axes bullet
   (`corpus/lessons/round-25.md:97-99`) is defective *because* it is shadowed by the block at
   `:101-104`; a further appended block only adds a second shadow. The fix is deletion of lines
   97-99, an edit to the filed round-25 lesson, which my bounds bar me from proposing as an edit.
   Flagged for the L1.
3. **The same absolute wording survives in two other places** and is out of my scope: the tool
   docstring `tools/mori-job-runway.py:74` ("`RUNWAY_UNKNOWN` is never a false number") and the
   filed round-25 contract (`.ufo/waves/round-25/contract.md:156`). Both are false on the same 72
   configs; the docstring belongs to R1's tool owner, the contract is filed history.
4. **Two upstream files cited by the R6 correction have no `corpus/SOURCES.md` row**:
   `eval/agent-bridge.ts` (sha256 `1c34c1ab…`) and `task/workpool.ts` (sha256 `8cc4b17d…`), both
   fetched read-only at tag `v18.12.6` on 2026-10-22. The other cited files are registered (S098,
   S099, S103). Registering rows for these two is a gap for the L1 (adjacent to round-25 R7).
5. **Operator settings value.** `corpus/lessons/round-25.md:12` states the host's configured
   `async.maxJobs` value, which QUALITY 51 treats as out of scope for committed handoff material
   (wave-2 `ReviewQualityLesson.md` F12). Not routed in R1–R8 and not in my scope; I have not
   repeated the value in this report or in the drafted corrections.
6. **R2's number is re-derived but the corpus is not committed.** The 72/307 figure matches the
   routed claim exactly, but it comes from the wave-2 seat's uncommitted probe; until R1 commits the
   corpus as fixtures, the count cannot be re-derived from lane bytes alone.

## Out of scope (not drafted, not edited by this seat)

- R1, R3, R5, R7, R8 (tool defect, SKILL block, gate registry, knowledge corrections, retention scan).
- R4's coverage row (correct as filed: it already records round 13's self-assessed 7 as not held).
- Any lane commit, jj operation, push, or edit of `SCORECARD.md` / `corpus/lessons/round-25.md`.
- The wave-2 `ReviewRunwayCode.md` findings F3–F14 (tool-code defects, R1's owner).

## Gates and state

- `python3 -I -B tools/mori-routed-r24.py --repo . --rev 248408f5` → `items 4, held 4, mismatches 0`,
  exit 0 (read-only; no lane byte changed). My proposed Axes row text replays as D5-held; the
  `round 1` falsifier goes red.
- Lane working tree at my write: `M corpus/knowledge/userspace-oom-killers-r12.md` and
  `?? .ufo/waves/round-26/w1/` are other seats' work; untouched by this seat.
- Tooling: nothing installed or upgraded (all pacman transactions are paused host-wide; no
  `pacman -S/-Sy/-Syu/-U/-R` run). Tools used: `git` 2.56.0 (read-only), `python3` 3.14.8 (`-I -B`),
  `bun` 1.4.3 (read-only YAML parse), `curl` (public raw URLs only).

## Artifacts

- This report: `mori-shokunin/.ufo/waves/round-26/w1/DraftHygieneScorecard.md`.
- Scratch (read-only copies, outside the lane): `/fast/scratch/hyaku/mori-r26/DraftHygieneScorecard/`
  — upstream files `sdk.ts`, `async_job-manager.ts`, `eval_agent-bridge.ts`, `task_workpool.ts`,
  `tools_bash.ts`, `tools_eval.ts`, `docs_eval.md`; the probe copy `harness/diff_vs_bun.py`; the D5
  replay `d5sim.py` / `d5final.py`; the breakdown `breakdown.py`; fixture configs under `cfg/`.
