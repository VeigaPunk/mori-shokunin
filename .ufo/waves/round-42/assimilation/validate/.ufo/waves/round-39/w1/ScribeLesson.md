# ScribeLesson — `corpus/lessons/round-39.md` verification (L1 mori-r39, wave 1)

Scored tip: `13bfba23b7ca063c76d3504a2ff6eb7b6a294932`. Entering tip: `13f3db7e5c7163e7ef300259ff597a42a79f81f1`.
Target: Gate rows (S227/S228) and mistake rows M20–M22 of `corpus/lessons/round-39.md`.
Method: read-only inspection + read-only command runs. The worktree lesson is byte-identical to the tip blob
(`sha256 76e40cbb…f3a6` both), so line refs below are valid at `13bfba23`.

## Verdict

| Check | Result |
|---|---|
| Gate rows: quotes verbatim at the cited spans | **PASS** (both) |
| Gate rows: ≤25 words | **PASS** (17 and 24) |
| M20 evidence pointer resolves at `13bfba23` | **PASS** |
| M20 fix shown able to fail by a runnable command | **FAIL** — counterfactual only; no red receipt |
| M21 evidence pointer resolves at `13bfba23` | **PASS** (with one reconstruction step, see F4) |
| M21 fix shown able to fail by a runnable command | **PASS** — command archived in the artifact; I reproduced it |
| M22 evidence pointer resolves at `13bfba23` | **PARTIAL** — `c7-after.txt` resolves; the FAIL citation does not |
| M22 fix shown able to fail by a runnable command | **FAIL** — FAIL string exists only in the lesson |

## Gate rows — row-by-row

| row | source | cited span | quote verbatim? | words stated / actual | ≤25 | copy at tip | verdict |
|---|---|---|---|---|---|---|---|
| `corpus/lessons/round-39.md:7` | S227 gitrevisions(7) | `S227.src:2542-2544` | **YES** | 18 / **17** | YES | `corpus/evidence/sources-r39/S227.src` (tracked) | **PASS**, word annotation off by one |
| `corpus/lessons/round-39.md:8` | S228 `os.path.realpath` | `S228.src:657-659` | **YES** | 24 / **24** | YES | `corpus/evidence/sources-r39/S228.src` (tracked) | **PASS** |

Evidence for "verbatim": tags stripped + whitespace normalised, the quoted string is a contiguous substring of the
cited span, and occurs exactly once in the file.

- S227 span text: `to the syntax explained in SPECIFYING REVISIONS above), you can ask for commits that are reachable from r2 excluding those that are reachable from r1 by ^r1 r2 and it can be written as r1..r2.` The quote begins at "you can ask" (line 2542) and ends at "r1" (line 2544). Independent check: `SOURCES.md:233` cites the same `:2542-2544`.
- S228 span text: `Return the canonical path of the specified filename, eliminating any symbolic links encountered in the path (if they are supported by the operating system). On Windows, …`. The quote is the exact sentence through "system)." (line 659), i.e. the cited range is exactly right (this is the correction S228 exists to land; `corpus/SOURCES.md:232` still carries `:657-658`).
- S228 row's provenance claim "differs from `S226.src` only in the docs build footer": verified — `diff corpus/evidence/sources-r38/S226.src corpus/evidence/sources-r39/S228.src` = one changed line, `Last updated on Oct 23, 2026 (20:21 UTC)` → `Oct 24, 2026 (00:13 UTC)` (4 diff lines total).

No misquote and no count over 25: the Gate rows pass the acceptance's explicit FAIL triggers.

## Mistake rows — row-by-row

| row | evidence pointer | resolves at `13bfba23` | fail-showing command | verdict |
|---|---|---|---|---|
| M20 (`:19`) | `git show 13f3db7e:corpus/SOURCES.md`; S228 row `corpus/SOURCES.md:234` | **YES** — command ran: prints `:657-658` at `SOURCES.md:232` of 13f3db7e; tip row 234 reads `:657-659` + `supersedes S226` | **none recorded.** "an in-place anchor edit **would** list the row in the gate's `ids=[...]`" is counterfactual; no red receipt exists. The supporting arm does exist (`tools/mori-sources-appendonly.py:634`, `("immutable edit", …, ids=["S001"], exit 1)`), but the row cites no invocation of it and cites no red output. The only command in the cell (`git show`) demonstrates the pre-fix suffix, not the fix failing. | **FAIL** (third condition) |
| M21 (`:20`) | `evidence/c9-red-a.txt` third block = lines 17–22 | **YES** — tracked at tip; block 3 is `landing is the last edit commit (dag-d…)` with `supersede_timing superseded_as_of=[] stale_supersede=[S001]`, `EXIT=1` | **YES** — the artifact's first line is the invocation (`c9-red-a.txt:1`); I ran it and reproduced all three blocks byte-identically (diff of `tail -n +2` empty). Divergence claim holds: pre-fix fixture dag-a is `stale` under both gates (`c9-red-a.txt:7` vs `c9-after-fixture-a.txt:5`, no divergence), fixture D is `stale` under r38 bytes (`c9-red-a.txt:21`) and `superseded_as_of=[S001]` under v2 (`c9-after-fixture-d.txt:5`). Fixture D code confirmed at `tools/mori-sources-appendonly.py:558` (`("landing is the last edit commit", "dag-d", …)`, both-branch edit + side-branch supersede row at `:530-535`). | **PASS** |
| M22 (`:21`) | `evidence/c7-after.txt` (line 11) | **PARTIAL** — `c7-after.txt` is tracked and line 11 is exactly `check drift_kill_v2    PASS (drawn=fresh … want_drifted=['S103'] flips_ok=True)`; but "the smoke-run output **above**" is not a path and has no artifact. `git grep -n "drift_kill_v2 FAIL" 13bfba23` matches **only** `corpus/lessons/round-39.md:21`. | **NO** — no committed red. `git log --all -- .ufo/waves/round-39/count-c7.py` lists 4 commits; **all four plus the tip carry the same blob** `d7066610…`, i.e. the pre-fix counter that parsed the honest `row_states` was never committed, so the cited `FAIL (mutation anchor or table unparsable)` cannot be reproduced or re-run. The fix description itself checks out (`count-c7.py` `parse_got_want`, `:343-365`, parses the mutant got/want tables structurally; the probe emits got/want on failure per `tools/mori-source-drift.py:387-389`). | **FAIL** (third condition; one pointer unresolved) |

Related M20 premises verified: `corpus/lessons/round-38.md:47` carries the M16 entry recording the `:657-658` one-line-short finding; `corpus/QUALITY.md:918` is item 113 ("A registry row's located-quote correction rides a superseding row, never an in-place `anchor` edit: S228").

## Exact commands run (read-only)

1. Lesson at tip: `git show 13bfba23:corpus/lessons/round-39.md | sha256sum` → `76e40cbb4d0ad08f176cf3e6f232975a5838ed8f5d7d5decfc253215ee58f3a6`, identical to worktree.
2. Quote check: Python strip-tags + whitespace-normalise over the cited line spans → `in-span: True` for both; occurrences of the S227 quote in the file = 1; `len(quote.split())` = 17 (S227), 24 (S228).
3. `git show 13f3db7e:corpus/SOURCES.md | grep -n S226` → line 232 with `:657-658`.
4. `git show 13bfba23:corpus/SOURCES.md | grep -n "S226\|S227\|S228"` → 232 (`:657-658`), 233 (S227), 234 (`:657-659`; `supersedes S226`).
5. `diff corpus/evidence/sources-r38/S226.src corpus/evidence/sources-r39/S228.src` → one footer line changed.
6. `git ls-tree -r --name-only 13bfba23 -- corpus/evidence/sources-r39` → `S227.src`, `S228.src`.
7. `diff <(git show 13f3db7e:tools/mori-sources-appendonly.py) .ufo/waves/round-39/scratch/gate-r38.py` → identical; `diff <(git show 13bfba23:tools/…) scratch/gate-v2.py` → identical.
8. `python3 .ufo/waves/round-39/fixtures/run-c9-dags.py .ufo/waves/round-39/scratch/gate-r38.py /home/vgpnk/Projects/shokunin/mori-shokunin /tmp/mori-scribe-r39/c9-red-a-rerun.txt` → EXIT=0; `diff <(tail -n +2 rerun) <(tail -n +2 .ufo/waves/round-39/evidence/c9-red-a.txt)` → empty (`BLOCKS-IDENTICAL`).
9. `git grep -n "drift_kill_v2 FAIL" 13bfba23` → only the lesson row.
10. `git log --all --oneline -- .ufo/waves/round-39/count-c7.py` → 97b826a, 2de113e, 89956c5, da8d942; `git rev-parse <c>:<path>` all `d70666106fd9f6e32e44e7fbe0eeae4b995b0144` = tip blob.
11. `grep -n '"immutable edit"\|"landing is the last edit commit"' tools/mori-sources-appendonly.py` → 634, 558.

## Findings

- **F1 (FAIL, M22):** the fail-showing evidence is unarchived. The row's red state (`drift_kill_v2 FAIL (mutation anchor or table unparsable)`) lives only in prose; no path at `13bfba23` contains it, and the pre-fix counter is not in any commit (single blob across all four commits touching the file). No runnable command reproduces the FAIL.
- **F2 (FAIL, M20):** "an in-place anchor edit would list the row in the gate's `ids=[...]`" is a counterfactual with no red receipt. The claim is instrument-backed in code (`tools/mori-sources-appendonly.py:634` immutable-edit arm, exercised by the 12/12 selftest recorded in `evidence/gate-selftest-after.txt`), but that arm yields a PASS assertion, and the row cites neither the arm nor any traced invocation. The only command the row does cite (`git show 13f3db7e:…`) shows the stale suffix, not the fix failing.
- **F3 (minor, Gate S227):** the annotated word count is wrong by one — 18 stated (`lesson:7`, repeated in `SOURCES.md:233`), 17 actual. The quote itself is verbatim and well under the 25-word cap, so this does not trip an acceptance trigger, but the annotation should be 17.
- **F4 (note, M21 reproducibility):** the archived command's first argument, `.ufo/waves/round-39/scratch/gate-r38.py`, is not tracked at `13bfba23` (scratch is untracked). The r38 bytes are recoverable exactly as `run-c9-dags.py:6-7` documents (`git show 13f3db7e:tools/mori-sources-appendonly.py`); the worktree copy I ran is byte-identical to that blob. So M21's receipt is reproducible with that one extraction step, not from a clean checkout as-is.
- **Path convention (note):** `evidence/…` in the mistake rows resolves relative to `.ufo/waves/round-39/` (the only place `c9-red-a.txt` / `c7-after.txt` exist); under that convention both referenced files are tracked at `13bfba23`.

## Touched surfaces

- Wrote exactly one file: this report, `.ufo/waves/round-39/w1/ScribeLesson.md`.
- Scratch: `/tmp/mori-scribe-r39/c9-red-a-rerun.txt` only.
- No lane file edited; no `git add/commit/push/fetch/reset/stash`; no `jj` mutation; no tool install/upgrade; no process kills; no remediation.

## Out of scope / not run

- Did not run C1's `count-c7.py`, C2's `conform.py`, or the gate selftest (other seats own those claims; rerunning would not strengthen this target). M21's fixture runner was run only to test the cited command's reproducibility, with output to `/tmp`.
- Word counts are whitespace-token counts; the quoted strings are as written in `corpus/lessons/round-39.md:7-8`.
- The historical claims in M20/M21 evidence cells that have no artifact (e.g. "brute-forcing 16 DAG constructions × 2 date orders", "routed by the r38 closure") were not re-derived; they are not pointers and not needed to adjudicate the row.
