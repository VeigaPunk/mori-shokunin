# mori round 52 — frozen contract (L1 MoriR52, attempt 1)

Entering lane tip: `4f266ef2fdf74d8b046f5b4f5a5c4945f65b966d` (round 51 closure,
`corpus/lessons/round-51-verifier-spotcheck.md`). This file, both counters, `controls/` (data applier and control
builder), the control receipts, the counter selftest receipts, the census-start receipt, the sweep and the five
source copies under `corpus/evidence/sources-r52/` land in one freeze commit before any wave seat runs. A
predicate, counter, floor or kill rule changed after any seat has scored is not the claim's rule. Frozen bytes are
listed with sha256 in `evidence/freeze-sha256.txt`; if working-tree bytes ever differ, the claim is measured with
`git show <freeze>:<path>`, and a frozen file is never edited in place (round-51 closure routed defect 6).

Scores entering (SCORECARD.md `## Axes`): coverage 6, operability 7, depth 5, freshness 5, calibration 5,
adjacency 6. Lowest non-retired axes: depth, freshness, calibration (tied at 5). Both claims work a lowest axis
(C1 calibration, C2 depth). No stagnation waiver; no exploratory claim; no capability claim. Two claims.

## C1 — calibration: the self-assessment agrees with the fleet record, its instruments and its own pointers

Surface: `SCORECARD.md` `## Axes`, `SHONEN.md`, and the command-tally pins of the two living documents
`corpus/QUALITY.md` and `corpus/README.md`. Routed by `corpus/lessons/round-50-verifier-spotcheck.md` §5 item 3
(successor counter closing the named survivors — verdict-word substring, a second `## Axes`, the unread Score
column, the vacuous `admitted` arm, a symlinked pin path — and K4 beyond SHONEN) and carried by the round-51
closure §5 item 4. Also closes round-51 closure items 1 (the counter has a `--selftest`) and 7 (every receipt
records its literal command line).

K4 scope, decided before data: LOG.md and the SCORECARD round sections are dated records (each tally sits under a
`## Round N` heading and reports what was measured then); a tally there is history, not a current claim, so K4
does not run them. QUALITY.md criteria carry `Check:` commands that a reader runs today, and README coverage rows
carry the command that shows the bounded advance; those are the living pins K4 runs. The house rule for a stale
check is supersession by a later row (QUALITY 111 supersedes 109's check), never an in-place rewrite.

**P-C1.** The predicate is the docstring of `count-c1.py` verbatim (same sentence): at R, mismatches=0 and
errors=0 over arms (A) axes, (B) shonen, (C) living pins, (D) locators, with every floor held.

Counting command: `python3 .ufo/waves/round-52/count-c1.py R [--scratch DIR]` (DIR outside the lane).

- Before (entering `4f266ef2`): `C1=unmet items=37 … living=4 superseded=1 locators=25 mismatches=8 errors=0
  hidden=0 lane_writes=0 … failed=mismatch` (`evidence/control-c1-do-nothing.txt`). The eight: operability and
  depth Last change cells lag the round-51 closure (MANIFEST round 51 admitted, both improved); the two SHONEN pins
  have no round-52 receipt; `QUALITY.md:909` and `README.md:608` pin `pass=12` while the gate prints 22;
  `README.md:607` pins a bare `--selftest` that names no command; `SCORECARD.md:1771` holds no `5 → 6`.
- Target after: `C1=met … mismatches=0 errors=0 hidden=0 lane_writes=0` at the landed tip.
- Controls (commits in a throwaway `--no-local` clone built by `controls/c1-controls.py`, scored before data,
  receipts `evidence/control-c1-<name>.txt`): do-nothing; axes-only; receipts-only; living-only; rewrite-in-place
  (stale pins edited to the current tally); delete-stale-pins; repeat-stale-tally (superseding lines that repeat
  the stale tally); witness (feasibility only, built by the L1 with the data applier — disclosed, not the claim's
  landing). Readings are in the table at the end of this file.
- Kill rule: `C1=unmet` (or exit 2) at the landed tip → C1 not verified; no re-scoring under a changed counter.
- Named limits (before data): a pin split across lines is not enumerated; a matching tally proves the instrument
  prints it today, not that its arms are good; the locator arm checks quoted strings and `proposed A → B` pairs
  only, other prose before a pointer is range-checked; the Score arm trusts the newest closure's per-axis table;
  `lane_writes` sees only paths that `git status --ignored` lists (a write into `.git/` is not seen); the counter
  runs the pinned commands unsandboxed in an archive of R.

## C2 — depth: CommitLimit and Committed_AS — the overcommit ledger, enforced only under mode 2

Surface: `corpus/knowledge/` — resource runway. Round 51 said what `MemAvailable` is; the two other runway lines
of `/proc/meminfo`, `CommitLimit` and `Committed_AS`, are undefined in the lane. Sweep before data
(`evidence/sweep-overcommit.txt`, at `4f266ef2` over `corpus/SOURCES.md corpus/knowledge SKILL.md`): CommitLimit,
Committed_AS, overcommit_memory, overcommit_ratio, overcommit_kbytes, vm_commit_limit, __vm_enough_memory,
vm_committed_as, user_reserve_kbytes, admin_reserve_kbytes, MAP_NORESERVE, OVERCOMMIT_NEVER and
overcommit-accounting occur 0 times; `merge/mori/` has 0 files on the theme. New entry
`corpus/knowledge/overcommit-commit-limit-r52.md`; new rows S497–S501 (ids continue the registry):
`Documentation/mm/overcommit-accounting.rst`, `Documentation/admin-guide/sysctl/vm.rst`, `mm/util.c`,
`include/linux/mman.h` and `mm/mmap.c`, all at tag v7.2.

**P-C2.** The predicate is the docstring of `count-c2.py` verbatim (same sentence). The entailment arm is the
round-51 arm hardened per the round-51 closure §5 item 2: ≥ 2 distinct ENTAILMENT voters per row, unfenced lines
only, voters are exactly the frozen list `Mo52Ent01`–`Mo52Ent12` (report `w1/<voter>.md`), and a voter's vote does
not count for a row whose text that voter wrote (`REPLACE <old> :: <text>` line).

Counting command: `python3 .ufo/waves/round-52/count-c2.py R`.

- Before (entering `4f266ef2`): `C2=unmet claims=0 … pins=bad … failed=entry_absent,pins`
  (`evidence/control-c2-do-nothing.txt`).
- Target after: `C2=met claims=N located=N quote_missing=0 bad_rows=0 sources=5 source_rows=ok pins=ok
  provenance=ok entailed=N dissent=0`, N ≥ 12, at the landed tip.
- Controls: do-nothing (above); the data commit before any vote must read `failed=entailment` (receipt
  `evidence/c2-at-data.txt`). Selftest `C2_SELFTEST pass=45 fail=0` (`evidence/selftest-c2.txt`) carries the
  entry-level controls and the hardened-arm controls (one voter, same voter twice, non-voter seat, voter outside
  the list, fenced votes, fenced dissent, non-voter dissent, author vote, fenced REPLACE).
- Kill rule: `C2=unmet` at the landed tip → C2 not verified. An `overclaim` vote is resolved only by replacing the
  claim text with text that two voters who did not write it vote `entailed` (new hash). Votes are never deleted.
- Named limits: a located quote proves the words occur; two `entailed` votes prove two ENTAILMENT seats recorded
  that judgment for that exact text — seats are the lane (LEARNING.md), so this is a committed reviewer step, not
  outside verification; a REPLACE line is the only authorship signal read; v7.2 bytes say nothing about other
  kernels or this host's sysctl values.

## Separability

C1 touches `SCORECARD.md` Axes cells, `SHONEN.md` receipts, and appended supersession text in `corpus/QUALITY.md`
and `corpus/README.md`. C2 touches the entry, its SOURCES rows, `corpus/evidence/sources-r52/` and the voters'
`ENTAIL` lines. `count-c1.py` reads no knowledge entry and no SOURCES row; `count-c2.py` reads no SCORECARD,
SHONEN, QUALITY or README byte. Either counter can be run with the other claim's changes reverted.

## Frontier step, assimilation, mistake, considerthese (not claims)

- Census at round start: `evidence/census-start.txt` (rc 0; 23 W04 + `ok`). Round end: same command.
- Sourced claim: C2 rests on the five rows opened 2026-10-26.
- Assimilation: none — `merge/mori/` holds no staged entry or row on overcommit (`evidence/sweep-overcommit.txt`).
- considerthese: `considerthese/2026-10-26.md` suggestion 3 (re-execute what closures only evidence-verified):
  wave seats re-run the round-51 frozen counters at the measured revision `70e68cdd` and report agreement or the
  exact divergence; it lands as a lesson section.
- Mistake to mine: a living document's check command pinned at one round's tally and never superseded (the
  QUALITY 112 / README round-39 pins), and the round-51 lesson's locator drift (closure D-c).

## Round-51 closure routed defects (§5) — carriers

1 counter self-test → both counters ship `--selftest`; 2 entailment hardening → P-C2's arm; 3 round-51 C1 counter
survivors → that counter is frozen; wave mutation seats name each arm-isolating control, recorded as limits and
routed; 4 successor calibration counter and K4 → C1; 5 S493 locators and famzah attribution → appended erratum
`corpus/lessons/round-51-erratum.md`; 6 no in-place edits of frozen files → this round edits none (the in-lane
writers of item 8 are inventoried by the wave, not edited); 7 literal receipt commands → every round-52 receipt
records its command; 8 the remaining in-lane writers → a wave inventory item (read-only), and the fix is routed with
a successor-freeze design, because editing those frozen files in place is what item 6 forbids.

## Round shape

One v2 wave `w1` (policy `scripts/hyaku/ufo-wave-policy-v2.json`, band 64–128), dispatched after the data commit:
the twelve ENTAILMENT voters (`Mo52Ent01`–`Mo52Ent12`, three per block of seven rows), attacks on both counters
and both claims, source re-opening, frontier drafting, the considerthese re-execution and the in-lane-writer
inventory. Attack share ≥ 25 %. Total ≤ 128 including any residual call. The L1 holds the planner seat.

## C1 control readings (filled from the receipts before data)

| control | counter line (rev elided) | reading |
|---|---|---|
| do-nothing | `C1=unmet items=37 … living=4 superseded=1 locators=25 mismatches=8 errors=0 hidden=0 lane_writes=0 failed=mismatch` exit=1 | the target is not reachable without work; the eight mismatches are listed under C1 |
| axes-only | `C1=unmet items=39 … mismatches=5 … failed=mismatch` exit=1 | Axes cells and the locator fixed; receipts and living pins still open |
| receipts-only | `C1=unmet items=37 … mismatches=6 … failed=mismatch` exit=1 | SHONEN receipts alone leave the Axes, living and locator arms open |
| living-only | `C1=unmet items=40 … living=7 superseded=4 … mismatches=5 … failed=mismatch` exit=1 | supersession alone leaves Axes, receipts and locator open |
| rewrite-in-place | `C1=unmet items=42 … mismatches=3 … failed=mismatch` exit=1 | editing the stale pins to today's tally reads `pin_removed_or_rewritten` ×3 |
| delete-stale-pins | `C1=unmet items=39 … living=1 … mismatches=3 … failed=mismatch` exit=1 | deleting the stale pins reads `pin_removed_or_rewritten` ×3 |
| repeat-stale-tally | `C1=unmet items=42 … mismatches=3 … failed=mismatch` exit=1 | superseding lines that repeat the stale tally are run and fail |
| witness | `C1=met items=42 … living=7 superseded=4 locators=27 mismatches=0 errors=0 hidden=0 lane_writes=0` exit=0 | feasibility only; built by the L1 with `controls/c1-data.py` (all four parts), disclosed |

Pre-freeze note: `controls/c1-data.py` was edited once before freeze (the README supersede bullets became one line
each, because the counter reads a quoted stale pin as a quotation only next to its replacement); living-only and
witness were re-run after that edit; the other five controls do not use the README text and were not re-run.
Receipts record the literal command with the clone path and scratch path they used; both were removed after
the run (the commit hashes are the control commits in those clones and are not reachable from the lane).
