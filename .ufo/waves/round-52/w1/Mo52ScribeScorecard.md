# Mo52ScribeScorecard — draft of `SCORECARD.md` `## Round 52`

Seat: scribe. Scope: draft the round-52 section in the house shape of the round-51 section at the end of
`SCORECARD.md` (claim table, controls line, limits, `Planned (round 53)`). Nothing outside this report was
written; the After cells are left as `[L1 fills]` because the landed tip does not exist yet.

Scratch: `/fast/scratch/hyaku/mori-r52/Mo52ScribeScorecard/` (created with `mkdir -p`, `TMPDIR` set under it;
one `git diff` capture, `data-diff-living.txt`, 44 lines). Removed at the end of this seat.

## What I read and observed

All reads are read-only git (`show`, `diff`, `log`) and file reads from the lane at
`/home/vgpnk/Projects/shokunin/mori-shokunin`; no command wrote into the lane, no git index or jj state touched,
no `pacman` run, no tool installed.

1. `.ufo/waves/round-52/contract.md` — read whole. `sha256sum .ufo/waves/round-52/contract.md` →
   `b1ea7b83bc9bf273958918ba1b3f58e759c6fcf7c80df1cd18ab420d1d176d19`, identical to its line in
   `evidence/freeze-sha256.txt` (exit 0). L1 `MoriR52`, attempt 1; entering tip `4f266ef2`, freeze `d3a8ea59`,
   data `8524904a`.
2. `git log --oneline -3 8524904a` (exit 0):
   `8524904a round-52: data — …`, `d3a8ea59 round-52: freeze — …`, `4f266ef2 round-51 verifier spot-check …`.
3. Axes table at the data commit (`git show 8524904a:SCORECARD.md`): Score column coverage 6, operability 7,
   depth 5, freshness 5, calibration 5, adjacency 6 — unchanged from the entering tip and from the contract's
   "scores entering". `## Axes` occurs once outside fences (the counter's arm A reports `axes=6` rows).
4. Entering-tip vs data, the two lagging Last change cells (script over `git show <rev>:SCORECARD.md`):
   - operability, `4f266ef2`: `round 47 (improved, score held); round 31 …` → `8524904a`:
     `round 51 (improved, score held); round 47 (improved, score held); …`
   - depth, `4f266ef2`: `round 50 (improved, score held); round 49 …` → `8524904a`:
     `round 51 (improved, score held); round 50 (improved, score held); round 49 …`
   - operability Evidence cell gains `round-51 closure grades operability improved (C1: a `--rev` pin
     re-execution is hermetic and classes mismatches) and states the score 7`
     (`corpus/lessons/round-51-verifier-spotcheck.md:130`); depth Evidence cell gains
     `round-51 closure grades depth improved (C2 re-measured 21/21, the MemAvailable entry) and states the score 5`
     (`…:131`).
5. `SHONEN.md` is byte-unchanged between the two commits (`git diff -U0 4f266ef2 8524904a -- SHONEN.md` prints
   no hunk); 4 checklist boxes, 2 `--selftest` tally pins; pins read `(125/125)` and `(17/17)` and cite the
   round-51 receipt paths. The round-52 observed lines the counter's arm B reads are new at the data commit:
   `git ls-tree` shows `.ufo/waves/round-51/evidence/selftests/{mori-pin-check,mori-unlanded-check}.txt` present
   already at `4f266ef2`, while `count-c1.py:68` reads `RECEIPT_DIR = ".ufo/waves/round-52/evidence/selftests/"`;
   the data commit adds those two files (`git diff --stat 4f266ef2 8524904a -- .ufo/waves/round-52/evidence/
   selftests`: `mori-pin-check.txt | 128 +`, `mori-unlanded-check.txt | 20 +`, 148 insertions, exit 0).
6. Data diff for the living documents (captured at `<scratch>/data-diff-living.txt`, 44 lines, exit 0): two
   append-only hunks, no rewrite.
   - `corpus/QUALITY.md` +21 lines at 1353: heading `## Criteria added round 52 — a living pin is current or
     superseded, and a self-assessment pointer lands on its words`; criterion 141 (supersedes 112's check cell
     only) with its `Check:` command `python3 tools/mori-sources-appendonly.py --selftest` →
     `MORI_SOURCES_APPENDONLY_SELFTEST pass=22 fail=0` and its "shown able to fail" / "not covered" lines;
     criterion 142 (a pointer lands on the words it reports), citing the round-28 `5 → 6` pair moving from
     `SCORECARD.md:1771` to `:1781`.
   - `corpus/README.md` +13 lines at 721: heading `## Round-52 corrections (living pins)`, a dated note
     (append-only, 2026-10-26) and two one-line supersede bullets for the round-39 `pass=12` pin and the round-39
     bare `--selftest` pin, with the stated reason that each bullet is one line (the counter reads a quoted
     stale pin only when its replacement stands on the same line), and the counter pointer (QUALITY 141).
7. Receipts at the data commit (read, not re-run):
   - `evidence/c1-at-data.txt`: `C1=met items=42 axes=6 pins=2 boxes=4 living=7 superseded=4 locators=27
     mismatches=0 errors=0 hidden=0 lane_writes=0 manifest=6209bdb8e400 rev=8524904a…`, `exit=0`; the locator
     arm reads `item locator SCORECARD.md:1781 expect=pair:5_→_6 got=found state=ok`.
   - `evidence/c2-at-data.txt`: `C2=unmet claims=28 located=28 quote_missing=0 bad_rows=0 sources=5
     source_rows=ok pins=ok provenance=ok entailed=0 dissent=0 … failed=entailment`, `exit=1`.
   - `evidence/control-c1-do-nothing.txt`: `C1=unmet items=37 … living=4 superseded=1 locators=25 mismatches=8
     errors=0 hidden=0 lane_writes=0 … failed=mismatch`, `exit=1`, with the eight mismatch items visible:
     operability and depth Last change, two pins `receipt_missing`, `QUALITY.md:909`, `README.md:607`
     (`unrunnable`), `README.md:608`, `SCORECARD.md:1771` `pair:5_→_6 got=absent`.
   - `evidence/control-c2-do-nothing.txt`: `C2=unmet claims=0 … source_rows=bad pins=bad provenance=bad
     entailed=0 dissent=0 … failed=entry_absent,pins`, `exit=1`.
   - other C1 controls (`grep -E '^C1='`): axes-only `items=39 … locators=27 mismatches=5`; receipts-only
     `items=37 … mismatches=6`; living-only `items=40 … living=7 superseded=4 mismatches=5`; rewrite-in-place
     `items=42 … mismatches=3`; delete-stale-pins `items=39 … living=1 … mismatches=3`; repeat-stale-tally
     `items=42 … living=7 superseded=4 mismatches=3`; witness `items=42 … mismatches=0 errors=0 hidden=0
     lane_writes=0`, `exit=0`.
   - selftests: `C1_SELFTEST pass=42 fail=0` (`evidence/selftest-c1.txt`, `exit=0`);
     `C2_SELFTEST pass=45 fail=0` (`evidence/selftest-c2.txt`, `exit=0`).
8. C2 landing at the data commit: `corpus/knowledge/overcommit-commit-limit-r52.md` (75 lines; `source:` lines
   S497–S499 … at the head); `corpus/SOURCES.md` rows S497 (line 276) through S501 (line 280); five copies in
   `corpus/evidence/sources-r52/` (`mman.h.v7.2`, `mmap.c.v7.2`, `overcommit-accounting.rst.v7.2`,
   `util.c.v7.2`, `vm.rst.v7.2`); `evidence/c2-hashes-at-data.txt` holds 28 `row=… hash=… claim=…` lines
   (`wc -l` = 30 including the `$ … --hashes` header and the closing line), so the data-time shape is 28 rows.
9. `evidence/w1-validate-refused.txt` currently holds one line: `{"schema":"ufo-swarm-wave-error-v1","code":
   "unknown_role","message":"items[39].role \"labrat\" is not a swarm role"}` — noted only as a wave-dispatch
   artifact that the L1 owns; it does not touch the counters.
10. Contract's named limits and its round-51-closure carrier list were read verbatim; the limits paragraph below
    is a condensation of them, with one pointer to the wave's integrated findings left for the L1 to fill.

## Draft — Appendix-in-one-block, to be inserted after the round-51 section at the end of `SCORECARD.md`

```markdown
## Round 52 — the self-assessment agrees with the fleet record, its living pins and its own pointers (C1) and CommitLimit/Committed_AS at v7.2 (C2)

L1 MoriR52, attempt 1. Entering tip `4f266ef2fdf74d8b046f5b4f5a5c4945f65b966d`; freeze
`d3a8ea5957b73bddbde750a8c0af2fba8da8b7c2` (`.ufo/waves/round-52/contract.md`); data
`8524904adb25e44f24d9f25aac7eae909625c18c`. Scores entering: coverage 6, operability 7, depth 5, freshness 5,
calibration 5, adjacency 6; both claims work a lowest (tied 5) axis. One v2 wave `w1` was dispatched after the
data commit — twelve ENTAILMENT voters for C2's rows, attacks on both counters and both claims, source re-opening,
frontier drafting, the considerthese re-execution and the in-lane-writer inventory. No score change is claimed by
the lane; the non-author closure rules.

| Claim | Axis (held) | Counting command | Before | After |
|---|---|---|---|---|
| C1 the self-assessment agrees with the fleet `MANIFEST.json`, its instruments and its own pointers — the six `## Axes` rows, the two `SHONEN.md` tally pins, every single-line command-tally pin in `corpus/QUALITY.md` and `corpus/README.md` (K4 beyond `SHONEN.md`), the freshness pin, and every `path:N` locator in the Axes rows and SHONEN boxes | calibration 5 | `python3 .ufo/waves/round-52/count-c1.py R [--scratch DIR]` | `C1=unmet items=37 axes=6 pins=2 boxes=4 living=4 superseded=1 locators=25 mismatches=8 errors=0 hidden=0 lane_writes=0 manifest=6209bdb8e400 rev=4f266ef2fdf74d8b046f5b4f5a5c4945f65b966d failed=mismatch`, rc 1 — `evidence/control-c1-do-nothing.txt` | `[L1 fills]` — at the data commit the same command read `C1=met items=42 axes=6 pins=2 boxes=4 living=7 superseded=4 locators=27 mismatches=0 errors=0 hidden=0 lane_writes=0`, rc 0 (`evidence/c1-at-data.txt`); that is not the landed reading |
| C2 what `/proc/meminfo`'s `CommitLimit` and `Committed_AS` are at kernel v7.2 — the overcommit ledger, enforced only under `vm.overcommit_memory=2` — 28 located quotes over 5 sources, each row entailed by two ENTAILMENT seats that did not write it | depth 5 | `python3 .ufo/waves/round-52/count-c2.py R` | `C2=unmet claims=0 located=0 quote_missing=0 bad_rows=0 sources=0 source_rows=bad pins=bad provenance=bad entailed=0 dissent=0 failed=entry_absent,pins`, rc 1 — `evidence/control-c2-do-nothing.txt` | `[L1 fills]` — at the data commit `C2=unmet claims=28 located=28 quote_missing=0 bad_rows=0 sources=5 source_rows=ok pins=ok provenance=ok entailed=0 dissent=0 failed=entailment`, rc 1 (`evidence/c2-at-data.txt`): every arm but the vote already reads its target there |

The C1 landing lives in four places and rewrites none of them in place. The operability and depth Last change
cells now lead with round 51, and their Evidence cells name
`corpus/lessons/round-51-verifier-spotcheck.md` — the two lagging cells the do-nothing run names. `SHONEN.md`
keeps its two tally pins, and `.ufo/waves/round-52/evidence/selftests/mori-pin-check.txt` and
`…/mori-unlanded-check.txt` hold the lines those pins printed at R, which is what the counter's receipt arm reads.
`corpus/QUALITY.md` gains criteria 141 (a living pin is current or superseded, never rewritten; it supersedes
112's check cell only, whose criterion stands) and 142 (a pointer lands on the words it reports), and
`corpus/README.md` gains a `## Round-52 corrections (living pins)` note that supersedes the two stale round-39
pins — the `pass=12` tally and the bare `--selftest` that names no command — instead of editing them. The
freshness cell's round-28 `5 → 6` pointer now lands at `SCORECARD.md:1781`, where the pair is, not at `:1771`,
which holds the amendment paragraph. The C2 landing is `corpus/knowledge/overcommit-commit-limit-r52.md`, rows
S497–S501 in `corpus/SOURCES.md` (opened 2026-10-26) and the five v7.2 copies under
`corpus/evidence/sources-r52/`.

Controls that skip the work stay unmet (receipts under `.ufo/waves/round-52/evidence/`): C1 do-nothing
`items=37 … mismatches=8`; axes-only `items=39 … locators=27 mismatches=5`; receipts-only `items=37 …
mismatches=6`; living-only `items=40 … living=7 superseded=4 mismatches=5`; rewrite-in-place `mismatches=3`
(the three restated pins read `pin_removed_or_rewritten`); delete-stale-pins `living=1 … mismatches=3`
(`pin_removed_or_rewritten` ×3);
repeat-stale-tally `items=42 … living=7 superseded=4 mismatches=3` (a superseding line that repeats the stale
tally still runs and fails). The witness — feasibility only, built by the L1 with `controls/c1-data.py`,
disclosed — met (`items=42 … mismatches=0 errors=0 hidden=0 lane_writes=0`). C2 do-nothing `claims=0 …
failed=entry_absent,pins`; the data commit before any vote reads `failed=entailment`. Counter selftests:
`C1_SELFTEST pass=42 fail=0`, `C2_SELFTEST pass=45 fail=0` (`evidence/selftest-c1.txt`, `evidence/selftest-c2.txt`).

No capability row is claimed by this draft. The round's new instruments are successor counters over surfaces
that already existed (K4 widens the pin set that `count-c1.py`'s predecessor already read); whether K4 beyond
`SHONEN.md` constitutes a capability is the L1's ruling, not this section's `[L1 decides]`.

Limits named before data, and found by the wave: `[L1 fills the wave's integrated findings —
`corpus/lessons/round-52.md` `## Wave w1 — integrated findings`]`. Named before data: a pin split across lines,
or carrying a placeholder such as `<rev>`, is not enumerated as a living pin; a matching tally proves the
instrument prints it today, not that its arms are good; the locator arm checks quoted strings and
`proposed A → B` pairs only, other prose before a pointer is range-checked; the Score arm trusts the newest
closure's per-axis table; `lane_writes` sees only paths `git status --ignored` lists, so a write into `.git/` is
not seen; the pinned commands run unsandboxed in an archive of R. For C2: a located quote proves the words occur
in the committed copy; two `entailed` votes prove two ENTAILMENT seats recorded that judgment for that exact text
— seats are the lane, so this is a committed reviewer step, not outside verification; a `REPLACE` line is the
only authorship signal read; v7.2 bytes say nothing about other kernels or about this host's sysctl values.

Planned (round 53): the in-lane writers the wave inventories — the hardcoded lane path
`LANE = "/home/vgpnk/Projects/shokunin/mori-shokunin"` at `.ufo/waves/round-38/conform.py:37`,
`round-39/conform.py:53`, `round-41/conform.py:66` and `round-42/conform.py:73`, and the `--scratch` default
`<repo>/.scratch` at `.ufo/waves/round-48/count-c1.py:292` and `.ufo/waves/round-49/count-c1.py:332` — get a
successor freeze with its own counter, because editing those frozen files in place is what this round's item 6
forbids. `tools/mori-pin-check.py` is no longer in that set: v5.1 moved its export out of the lane
(`tools/mori-pin-check.py:898`).

The locator sweep goes beyond the six Axes rows and the SHONEN boxes: arm (D) reads those two surfaces only, and
the 43 `path:N` pointers in `corpus/QUALITY.md` and the 35 in `corpus/README.md` are read by no arm. The counter
limits wave `w1` names (`corpus/lessons/round-52.md`) become routed items rather than in-round edits, since both
predicates are frozen.
```

## Notes on the draft (not part of the block)

- The After cells are `[L1 fills]`: no landed tip exists, and I did not run either counter (the seat's rule is to
  report observed evidence, not to re-measure the claim). The data-commit lines quoted in those cells come from
  the committed receipts, not from a run of mine.
- The `[L1 decides]` marker on the capability sentence, and the `[L1 fills …]` marker on the wave's integrated
  findings, are the only two unresolved slots I left; everything else is filled from bytes at
  `8524904adb25e44f24d9f25aac7eae909625c18c`.
- Heading choice: the house pattern is `## Round N — <what C1 does> (C1) and <what C2 does> (C2)`; I followed it
  with C1's three surfaces named (fleet record, living pins, own pointers).
- The draft avoids starting any line with `ENTAIL` or `REPLACE`; the one occurrence of `REPLACE` is inside a
  sentence, and no `ENTAIL <hash>` line exists here, so this report cannot be read as a vote by
  `count-c2.py` (it is not in the frozen voter list either).
- If the L1 prefers the round-51 sentence on capability ("No capability row is claimed: the pin reconciler
  predates round 51"), the equivalent here is that the K4 arm is an extension of an existing arm; the draft says
  that and hands the ruling up rather than asserting either way.

## Findings

- MED — `SCORECARD.md` round-52 section (this draft, After cells): the claim is not yet landed, so both After
  cells must stay `[L1 fills]`; a scribe that copied the data-commit lines into them would report the data
  commit as the landed tip. The draft quotes those lines inside the cell with the explicit caveat "that is not
  the landed reading".
- MED — `SHONEN.md:7` vs `.ufo/waves/round-52/count-c1.py:68`: the pins cite round-51 receipt paths while the
  counter reads only `.ufo/waves/round-52/evidence/selftests/`; the claim holds because the data commit adds
  those two files, but a reader following the SHONEN pin text finds the round-51 receipts, not the ones the
  counter read. Named as a C1-arm limit for round 53 rather than an in-round edit (frozen counter).
- LOW — `corpus/README.md` Round-52 corrections: the supersede bullets must each stay on one line, because the
  counter recognizes a quoted stale pin only when the replacement stands on the same line; a future edit that
  wraps them silently re-opens the stale pin. The appended note states this; the fragility remains.
- LOW — `SCORECARD.md` `## Axes`, freshness cell: the round-28 `5 → 6` pointer is now `:1781`, but it is a fixed
  line number inside an append-only file, so any insertion above it (the round-50 correction paragraph is
  exactly such an insertion, which is why the pin read `:1771` at the entering tip) invalidates it silently;
  arm (D) re-reads it each round and is the only thing that catches the drift. Worth a line in the round-53
  locator sweep: pointers into `SCORECARD.md` should name an anchor string as well as a line.
- MED — `SCORECARD.md:2701` (the round-50 section's "Planned (round 51)" paragraph): it pins two producers that no
  longer exist in that form — `tools/mori-pin-check.py:884-887` "exports a full tree into the lane" (at
  `8524904a` those lines assemble the `PIN_CHECK=` output line; v5.1 moved the export out, recorded at
  `tools/mori-pin-check.py:898`) and `.ufo/waves/round-40/conform.py:69` "hardcodes the lane path" (that file now
  derives `LANE` from `__file__` at `:71-72`, with the comment "scratch lives under TMPDIR, not inside the lane").
  A Planned paragraph is a dated record, so K4 does not run it and no arm reads it; the pointers survived a round
  in which both producers were actually fixed. That is why the round-52 draft's Planned paragraph names its
  writers by verified line (`.ufo/waves/round-38/conform.py:37`, `round-39`:53, `round-41`:66, `round-42`:73,
  `round-48/count-c1.py:292`, `round-49/count-c1.py:332`) and states that `tools/mori-pin-check.py` is out of the
  set.
- MED — arm (D) scope: `corpus/QUALITY.md` carries 43 backticked `path:N` pointers and `corpus/README.md` 35
  (`grep -oP '`[A-Za-z0-9_./-]+\.(md|py|sh):\d+(-?\d+)?`' | wc -l`), and no arm reads them; the predicate's
  locator arm is the six Axes rows and the SHONEN boxes only. The contract declares this boundary, so the claim
  is not overstated, but the sweep is the largest unread pointer surface in the lane and belongs in round 53.
- LOW — `evidence/w1-validate-refused.txt`: the wave dispatch was refused once for `items[39].role "labrat"`; the
  file is a wave-harness artifact, not counter evidence, and should not be read as a control receipt. Flagged so
  the L1 does not cite it as one.
- INFO — `.ufo/waves/round-52/evidence/c1-at-data.txt` and `c2-at-data.txt` are the only round-52 readings that
  exist; `c1-at-landed.txt` / `c2-at-landed.txt` promised by the house shape of round 51 do not exist yet, and
  the draft deliberately does not name them.
