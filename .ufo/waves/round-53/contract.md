# mori round 53 — frozen contract (L1 MoriR53, attempt 1)

Entering lane tip: `20edafa59b38dac1ca358893f0259b1f436372d3` (round 52 closure,
`corpus/lessons/round-52-verifier-spotcheck.md`, verdict admitted). This file, both counters, `controls/`
(data applier and control builder), the control receipts, the counter selftest receipts, the census-start
receipt, the sweeps and the twelve source copies under `corpus/evidence/sources-r53/` land in one freeze commit
before any wave seat runs. A predicate, counter, floor or kill rule changed after any seat has scored is not the
claim's rule. Frozen bytes are listed with sha256 in `evidence/freeze-sha256.txt`; a frozen file is never edited
in place (round-51 closure routed defect 6); if working-tree bytes ever differ, the claim is measured with
`git show <freeze>:<path>`.

Scores entering (`SCORECARD.md` `## Axes`): coverage 6, operability 7, depth 5, freshness 5, calibration 5,
adjacency 6. Lowest non-retired axes: depth, freshness, calibration (tied at 5). C1 works a lowest axis
(freshness, last moved before round 29). C2 is a coverage move with a capability row. No stagnation waiver, no
exploratory claim. Two claims.

## C1 — freshness: the release-pinned located-quote claims re-verified at Linux v7.3

Surface: `corpus/knowledge/` — the claim tables of `memavailable-estimate-r51.md` (21 rows) and
`overcommit-commit-limit-r52.md` (28 rows) pin their quotes to tag v7.2 bytes and carry `recheck: on-release`.
v7.3 is tagged (`evidence/sweeps.txt`: `refs/tags/v7.3^{}` → `c03c1a14507d…`); the lane holds no v7.3 recheck
(same receipt: 0 `v7.3` hits in `corpus/knowledge`, `corpus/SOURCES.md`, `SKILL.md`). The release trigger has
fired and nothing answered it. Of the 49 rows, 46 cite a v7.2 file (the scope D, `evidence/c1-scope.txt`); 3 cite
the 2014 commit patch, which a release cannot change, and are out of scope. Six of the nine files changed between
v7.2 and v7.3 (proc.rst, show_mem.c, mm_inline.h, vm.rst, util.c, mmap.c); in two rows (mm/mmap.c, the
MAP_NORESERVE rule) the v7.2 quote no longer occurs: v7.3 spells the flag write `vma_flags_set(&vma_flags,
VMA_NORESERVE_BIT)`.

New entry `corpus/knowledge/kernel-v7.3-recheck-r53.md` (the ledger) and rows S502–S510 (the nine files at
v7.3, git.kernel.org cgit, because raw.githubusercontent.com answered HTTP 429 on 2026-10-26).

**P-C1.** The predicate is the docstring of `count-c1.py` verbatim (same sentence): one ledger row per hash of
D with the counter-derived status (`held` / `absent`), a v7.3 source row opened this round, a quote located in
the v7.3 copy (the v7.2 quote itself when held), a `holds`/`changed` disposition, pinned copies, and ≥ 2 RECHECK
voters (`Mo53Fr01`–`Mo53Fr12`) whose final unfenced line carries that disposition, none carrying the other, an
author's vote not counted on a quote it proposed.

Counting command: `python3 .ufo/waves/round-53/count-c1.py R`.

- Before (entering `20edafa5`): `C1=unmet scope=46 rows=0 … pins=bad … failed=ledger_absent,pins`, exit 1
  (`evidence/control-c1-do-nothing.txt`).
- Target after: `C1=met scope=46 rows=46 matched=46 status_ok=46 quote_ok=46 source_rows=ok pins=ok provenance=ok
  … voted=46 dissent=0` at the landed tip.
- Controls (commits in throwaway clones built by `controls/controls.py`, scored before any seat ran):
  do-nothing; all-held (every row labelled held with its v7.2 quote, rows and votes present); v72-copies (the
  six changed v7.3 copies replaced by the committed v7.2 bytes); no-votes (ledger and rows, no voter); witness
  (feasibility only: ledger, rows and two synthetic voters — disclosed, not the claim's landing). Readings in the
  table at the end.
- Kill rule: `C1=unmet` (or exit 2) at the landed tip → C1 not verified. A dissent is resolved only by a voter's
  own later line (`RECHECK <h> <word>`, last unfenced line wins) or by a changed disposition that two voters
  carry; votes are never deleted; no re-scoring under a changed counter.
- Named limits (before data): `held` proves the words still occur somewhere in the v7.3 file, not at the same
  place nor with the same meaning — the disposition and its two votes carry the meaning; votes are seats of the
  lane, not outside verification; D covers two entries' tables only (not `oom-tracepoints-r47.md`, the round-50
  memcg entry whose recheck is `90d`, prose outside the tables, or the SOURCES anchors); the pins prove the bytes
  are what the L1 fetched from cgit, not that cgit served the tag — wave seats re-fetch independently.

## C2 — coverage: the commit ledger as a runway surface a mori tool reads, by overcommit mode

Surface: `tools/`. Round 52 admitted what `CommitLimit` and `Committed_AS` are; no mori tool reads them
(`evidence/sweeps.txt`: 0 hits of the commit-ledger names in `tools/` at `20edafa5`; `tools/mori-census.sh`
reads `/proc/meminfo` for other lines). PROVINCE names resource runway as mori ground. New tool
`tools/mori-commit-runway.py` (read-only: `/proc/meminfo`, five `/proc/sys/vm` files,
`/sys/devices/system/cpu/present`), its fixtures and `--selftest`, a SKILL.md registry row, and the entry
`corpus/knowledge/commit-runway-read-r53.md` for the band rule (rows S511–S513: `mm/mm_init.c`,
`lib/percpu_counter.c`, `include/linux/percpu_counter.h` at v7.2, the host's kernel line).

Interface the counter reads (frozen here): `python3 -I -B tools/mori-commit-runway.py [--meminfo PATH]
[--vm-dir DIR] [--cpu-present PATH] [--page-kb N] [--selftest]` → one JSON object, `schema:
mori-commit-runway-v1`, fields `verdict mode enforced commit_limit_kb committed_as_kb headroom_kb reserve_kb
usable_kb band_kb batch_pages cpus_present single_request_cap_kb limit_recomputed_kb limit_consistent`; verdicts
`COMMIT_OK` (0), `COMMIT_HEURISTIC` (0), `COMMIT_UNLIMITED` (0), `COMMIT_LOW` (1), `COMMIT_UNKNOWN` (2). Mode 2:
`usable_kb = CommitLimit − Committed_AS − admin_reserve_kbytes − user_reserve_kbytes`, `band_kb = batch × present
CPUs × page`, batch `= max(min(ram_pages / cpus / 256, INT_MAX), max(2 × cpus, 32))`, LOW iff `usable_kb ≤
band_kb`. Mode 0: `single_request_cap_kb = (ram + swap pages) × page`, never LOW. Mode 1: never LOW. The REF
function of `count-c2.py` is the reading, with hand-computed selftest arithmetic.

**P-C2.** The predicate is the docstring of `count-c2.py` verbatim (same sentence).

Counting command: `python3 .ufo/waves/round-53/count-c2.py R [--scratch DIR]` (DIR outside the lane).

- Before (entering `20edafa5`): `C2=unmet tool=absent … registry=bad live=error failed=registry,tool_absent`,
  exit 1 (`evidence/control-c2-do-nothing.txt`).
- Target after: `C2=met tool=present selftest=pass n≥12 fixtures=80 agree=80 disagree=0 registry=ok live=ok` at
  the landed tip.
- Controls: do-nothing; mode-blind (reference fields, verdict LOW whenever Committed_AS exceeds CommitLimit in
  any mode); no-band (mode-aware, LOW only below zero usable room); memoriser (exact on the 16 frozen fixtures,
  band-blind on the seeded ones); witness (the counter's own reference wrapped as a tool — feasibility only,
  disclosed). The junk tools print a fake `PASS 12/12` selftest, so the fixture arm alone separates them.
- Kill rule: `C2=unmet` at the landed tip → C2 not verified; the tool is not re-scored under a changed counter.
- Named limits (before data): REF and the tool share one author, so a shared misreading of the kernel passes
  both (wave seats recompute fixtures from the kernel copies independently); the band is an upper bound from the
  batch rule with present CPUs and today's totalram, not a measured deviation; the live leg compares stable
  fields only and depends on the host; the seeded fixtures are derivable from R, so a tool written after R could
  memorise them; the tool reads no cgroup-level commit (there is none) and gives no alert threshold — `COMMIT_LOW`
  is "inside the counter's own error band", not a calibrated alarm (FR8 stays open).

## Separability

C1 touches the ledger entry, rows S502–S510, `corpus/evidence/sources-r53/*.v7.3` and the RECHECK voters'
lines. C2 touches `tools/mori-commit-runway.py`, `tools/fixtures/mori-commit-runway/`, the SKILL.md registry row,
the band entry and rows S511–S513. `count-c1.py` reads no tool, SKILL byte or row S511–S513; `count-c2.py` reads no
knowledge entry, SOURCES row or vote. Either counter can be run with the other claim's data reverted.

## Frontier step, assimilation, mistake, considerthese (not claims)

- Census at round start: `evidence/census-start.txt` (rc 0; 23 W04). Round end: same command, exit 0 required.
- Sourced claims: C1 rests on S502–S510, C2 on S511–S513, all opened 2026-10-26.
- Assimilation: none — `merge/mori/` holds 0 files naming overcommit, CommitLimit, Committed_AS, percpu_counter
  or v7.3 (`evidence/sweeps.txt`).
- considerthese: `considerthese/2026-10-26.md` suggestion 2 (follow unfixed critic flags forward): a wave seat
  carries the round-52 critic and mutation findings forward — fixed, routed or silently dropped at `20edafa5` —
  and it lands as a lesson section.
- Mistakes to mine: the round-52 SCORECARD row whose numbers came from the at-data receipt while citing the
  landed one (closure D2), and the `[FILL]` self-citation in the round-52 report (closure D1).

## Round-52 closure routed defects (`corpus/lessons/round-52-verifier-spotcheck.md` §Routed defects)

1 SCORECARD correction (row cites `c1-at-landed.txt` but carries 42/27 instead of 43/28) → an appended correction
line naming the superseded text, this round; 2 report self-citation → the round-53 report names its own commit
by command (`git log --format=%H -- .ufo/reports/round-53/mori.md` on the fleet repo), never a placeholder, and the
lesson records the convention; 3 standing limits (locator arm scope, pure-text receipts, arm-A `admitted` pin) →
carried in `Planned (round 54)`; this round's counters are new and inherit none of them.

## Round shape

One v2 wave `w1` (policy `scripts/hyaku/ufo-wave-policy-v2.json`, band 64–128), dispatched after the data commit:
the twelve RECHECK voters (`Mo53Fr01`–`Mo53Fr12`, three per block), attacks on both counters, both claims and
the tool, independent fixture recomputation, source re-opening, frontier drafting, the considerthese item, the
routed-defect evidence. Attack share ≥ 25 %. Total ≤ 128 including any residual call. The L1 holds the planner
seat.

## Control readings (filled from the receipts before data)

| control | counter line (rev elided) | reading |
|---|---|---|
| c1 do-nothing | `C1=unmet scope=46 rows=0 … pins=bad provenance=bad … failed=ledger_absent,pins` exit=1 | no ledger, no v7.3 copies at the entering tip |
| c1 all-held | `C1=unmet … status_ok=44 quote_ok=44 … voted=46 dissent=0 failed=quote,status` exit=1 | labelling everything held fails exactly the two MAP_NORESERVE rows |
| c1 v72-copies | `C1=unmet … status_ok=44 quote_ok=44 … pins=bad … held=46 absent=0 … failed=pins,quote,status` exit=1 | v7.2 bytes presented as v7.3 fail the pins, and the two ledger rows that state the real drift then fail status and quote |
| c1 no-votes | `C1=unmet … status_ok=46 quote_ok=46 … voted=0 failed=votes` exit=1 | the data commit before any vote must read this |
| c1 witness | `C1=met … voted=46 dissent=0` exit=0 | feasibility only; synthetic voters, built by the L1 with `controls/c1-data.py` |
| c2 do-nothing | `C2=unmet tool=absent … failed=registry,tool_absent` exit=1 | no tool, no registry row |
| c2 mode-blind | `C2=unmet … agree=53 disagree=27 … failed=fixtures` exit=1 | a mode-blind LOW fails every mode-0/1 over-commit fixture |
| c2 no-band | `C2=unmet … agree=71 disagree=9 … failed=fixtures` exit=1 | ignoring the per-CPU band fails the band-edge fixtures |
| c2 memoriser | `C2=unmet … agree=71 disagree=9 … failed=fixtures` exit=1 | exact on the frozen 16, wrong on the seeded near-edge cases |
| c2 witness | `C2=met … agree=80 disagree=0 registry=ok live=ok` exit=0 | feasibility only; the counter's REF wrapped as a tool |

Receipts record the literal command with the clone and scratch paths they used; both were removed after the run
(the control commits live only in those clones).
