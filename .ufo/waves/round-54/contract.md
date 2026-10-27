# mori round 54 — frozen contract (L1 MoriR54, attempt 1)

Entering lane tip: `39dcf4d7e410d362781a47e8365ca23b5c807598` (round 53 closure,
`corpus/lessons/round-53-verifier-spotcheck.md`, admitted). This file, both counters, `controls/` (the two data
appliers and the control runner), the control receipts, both counter selftest receipts, the C1 scope listing, the
census-start receipt, the sweeps and the ten source copies under `corpus/evidence/sources-r54/` land in one freeze
commit before any wave seat runs. A predicate, counter, floor or kill rule changed after any seat has scored is not
the claim's rule. Frozen bytes are listed with sha256 in `evidence/freeze-sha256.txt`; a frozen file is never
edited in place; if working-tree bytes ever differ, the claim is measured with `git show <freeze>:<path>`.

Scores entering (`SCORECARD.md` `## Axes`): coverage 6, operability 7, depth 5, freshness 5, calibration 5,
adjacency 6. Lowest non-retired axes: depth, freshness, calibration (tied at 5). Both claims work a lowest axis:
C1 freshness, C2 depth. No stagnation waiver, no exploratory claim. Two claims.

## C1 — freshness: the remaining v7.2-pinned located-quote claims re-verified at Linux v7.3

Surface: `corpus/knowledge/` claim tables. Round 53 re-verified 46 rows of two entries and its `Planned (round 54)`
names the rest ("the v7.3 trigger for what D does not cover"). The counter's `--scope` at the entering tip lists
every remaining claim|source|quote row whose source row pins Linux tag v7.2 (raw.githubusercontent, cgit `?h=v7.2`,
jsdelivr `@v7.2`, docs.kernel.org/7.2): **31 rows** (`evidence/c1-scope.txt`) — `oom-memcg-stat-r50.md` 22
(S489 rendered cgroup-v2 7.2, S490 `mm/memcontrol.c`, S491 `mm/oom_kill.c`), `commit-runway-read-r53.md` 8 (S499
`mm/util.c`, S511 `mm/mm_init.c`, S512 `lib/percpu_counter.c`, S513 `include/linux/percpu_counter.h`),
`quota-observability-r48.md` 1 (S481 `include/uapi/asm-generic/errno.h`). No other entry's table pins v7.2.

New entry `corpus/knowledge/kernel-v7.3-recheck-r54.md` (the ledger) and rows S515–S520 (six v7.3 copies: four
cgit files, errno.h, and the release-pinned rendered page `https://docs.kernel.org/7.3/admin-guide/cgroup-v2.html`
— the flip the round-53 closure named for rendered docs), plus S508 (`util.c` v7.3) and S514 (`mm_init.c` v7.3),
whose used-by gains the new ledger.

New against round 53 (the round-53 limits routed here): a **line arm** — each ledger row names a line of the v7.3
copy on which its quote begins, derived by the counter (round 53's `held` proved the words occur somewhere, not
where); and **voter binding** — a RECHECK voter counts only when the orchestrator's `w1-results.json` lists a
result of that name (round 53's voter identity was the report filename alone).

**P-C1.** The predicate is the docstring of `count-c1.py` verbatim (same sentence).

Counting command: `python3 .ufo/waves/round-54/count-c1.py R`.

- Before (entering `39dcf4d7`): `C1=unmet scope=31 rows=0 … pins=bad provenance=bad … failed=ledger_absent,pins`,
  exit 1 (`evidence/control-c1-do-nothing.txt`).
- Target after: `C1=met scope=31 rows=31 matched=31 status_ok=31 line_ok=31 quote_ok=31 source_rows=ok pins=ok
  provenance=ok … voted=31 dissent=0` at the landed tip.
- Controls (commits in throwaway clones built by `controls/controls.py`, scored before any seat ran): do-nothing;
  copies-only (the freeze state); no-votes; unsettled-voters (voter files without a results file); no-line (every
  row held with its v7.2 quote and votes, no located line — the lazy relabel); v72-copies (v7.2 bytes presented as
  v7.3); witness (feasibility only: `controls/c1data.py` ledger and rows plus two synthetic voters in a fixture
  results file — disclosed, not the claim's landing). Readings in the table at the end.
- Kill rule: `C1=unmet` (or exit 2) at the landed tip → C1 not verified. A dissent is resolved only by the voter's
  own later line (`RECHECK <h> <word>`, last unfenced line wins) or by a changed disposition two voters carry; votes
  are never deleted; no re-scoring under a changed counter.
- Named limits (before data): all 31 v7.2 quotes still occur in the v7.3 copies, so the status arm cannot separate
  a lazy all-held labeller (the line, pin and vote arms do); the line arm proves where the words begin, not that
  the code around them means the same — the disposition and its votes carry the meaning; votes are lane seats, not
  outside verification, and the results binding proves the orchestrator recorded a seat of that name, not who
  wrote the report bytes; D covers claim|source|quote tables only (not prose, `oom-tracepoints-r47.md`'s catalogue
  or `system-pressure-r24.md`'s v7.2 anchors); the pins prove the bytes are what the L1 fetched — wave seats
  re-fetch them independently.

## C2 — depth: hardware memory-failure kills at Linux v7.3, the kill-event class an OOM-line census does not see

Surface: `corpus/knowledge/`. Mori's province names kill events; every kill entry it holds is an OOM kill (kernel
OOM killer, memcg OOM, userspace killers). The kernel also kills processes for hardware memory errors: the
memory-failure handler sends SIGBUS (or SIGKILL when unmapping fails) and prints its own lines under the prefix
`Memory failure:`, counts them per NUMA node in sysfs and in `HardwareCorrupted`, and emits `ras:memory_failure_event`.
At the entering tip no entry, SKILL row, PROVINCE line or tool names this class (`evidence/sweeps.txt`: the only
hit is a recheck-ledger quote); the round-53 lead `panic_on_unrecoverable_memory_failure` (new in v7.3) is unopened.
On this host the surfaces exist and read zero (node0 counters 0, `HardwareCorrupted: 0 kB`, recovery 1, early kill
0); the v7.3 panic sysctl is absent on the 7.2.11 kernel.

New entry `corpus/knowledge/memory-failure-kills-r54.md` with a claim|source|quote table and a decision table
(kernel line → kill class, sysctl → behaviour, counter → meaning); rows S521 `mm/memory-failure.c`, S522
`Documentation/mm/hwpoison.rst`, S523 `Documentation/ABI/stable/sysfs-devices-node`, S524
`include/trace/events/memory-failure.h` (all cgit `?h=v7.3`, opened 2026-10-27), plus S507 (`vm.rst` v7.3) and S502
(`proc.rst` v7.3), whose used-by gains the entry.

**P-C2.** The predicate is the docstring of `count-c2.py` verbatim (same sentence).

Counting command: `python3 .ufo/waves/round-54/count-c2.py R`.

- Before (entering `39dcf4d7`): `C2=unmet claims=0 … pins=bad provenance=bad … failed=entry_absent,pins`, exit 1
  (`evidence/control-c2-do-nothing.txt`).
- Target after: `C2=met claims≥14 located=claims quote_missing=0 bad_rows=0 sources≥4 source_rows=ok pins=ok
  provenance=ok entailed=claims dissent=0` at the landed tip.
- Controls: do-nothing; copies-only; quote-echo (claims restate their quotes); unlocated (quotes reordered);
  no-votes; two-sources (fourteen located rows from two copies); witness (feasibility only: synthetic claim text
  over real quotes, synthetic voters — disclosed).
- Kill rule: `C2=unmet` at the landed tip → C2 not verified; an `overclaim` vote is resolved only by rewording the
  row (a new hash) and two fresh `entailed` votes from voters who did not write it; never by re-scoring.
- Named limits (before data): a located quote proves the words exist in the copy; entailment votes are lane seats;
  nothing here was observed firing — no memory failure has occurred on this host, so every kill line and counter
  is read from source, not from a live event; the v7.3 bytes describe the current release while the host runs
  7.2.11 (a seat checks which claims hold on the host's kernel); the entry is detection knowledge only — mori
  never injects poison (`madvise(MADV_HWPOISON)`, hwpoison-inject) or writes a memory-failure sysctl.

## Separability

C1 touches the ledger, rows S515–S520, the used-by cells of S508/S514, `sources-r54/{memcontrol.c,oom_kill.c,
percpu_counter.c,percpu_counter.h,errno.h}.v7.3`, `sources-r54/cgroup-v2.7.3.html` and the RECHECK voters' lines.
C2 touches the memory-failure entry, rows S521–S524, the used-by cells of S502/S507,
`sources-r54/{memory-failure.c,hwpoison.rst,sysfs-devices-node,memory-failure-trace.h}.v7.3` and the ENTAILMENT
voters' lines. `count-c1.py` reads no C2 copy, row or vote; `count-c2.py` reads no ledger, C1 row or RECHECK vote.
Either counter can be run with the other claim's data reverted.

## Frontier step, assimilation, mistakes, considerthese, routed defects (not claims)

- Census at round start: `evidence/census-start.txt` (rc 0; 23 W04). Round end: same command, exit 0 required.
- Sourced claims: C1 rests on S515–S520 (opened 2026-10-27), C2 on S521–S524 (opened 2026-10-27).
- Assimilation: none — `merge/mori/` holds 0 files naming memory failure, hwpoison, SIGBUS, percpu_counter or v7.3
  (`evidence/sweeps.txt`).
- considerthese: `considerthese/2026-10-26.md` suggestion 3 (re-execute what closures only evidence-verified): a
  wave seat re-runs the round-53 frozen counters and the commit-runway selftest at the scored revision `0b36d23e`
  and reports agreement or the exact divergence; it lands as a lesson section.
- Round-53 closure routed defects: D2 → an appended SCORECARD note naming `c1-at-landed.txt`/`c2-at-landed.txt`
  (R = `0b36d23e`) as the landed measurement of the round-53 rows; D3 → the eight inherited lane-root strays
  (`0`, `base.c`, `main.c`, `meminfo.c`, `oom_kill.c`, `sd-main.c`, `user@.service.in` from the round-28 misroot
  sweep, plus `MANPAGE.md` from the same sweep, and `0` from round 38) relocated byte-exact under the rounds that
  swept them, with a LOG entry; the empty untracked `--repo/` dir removed; D1 disclosed only.
- Mistakes to mine: the round-53 SCORECARD rows citing the salvage receipt instead of the landed one (closure D2);
  the eight lane-root strays carried for 26 rounds (D3).

## Round shape

One v2 wave `w1` (policy `scripts/hyaku/ufo-wave-policy-v2.json`, band 64–128), dispatched after the data commit:
twelve RECHECK voters (`Mo54Rc01`–`Mo54Rc12`, three per block of the 31 rows), twelve ENTAILMENT voters
(`Mo54En01`–`Mo54En12`, three per block), attacks on both counters, both claims and the new entry, independent
source re-fetching, the live host read, drafting (SKILL rows, PROVINCE, README, lesson), the considerthese item and
the routed-defect checks. Attack share ≥ 25 %. Total ≤ 128 including any residual call. The L1 holds the planner
seat.

## Control readings (filled from the receipts before data)

| control | counter line (rev elided) | reading |
|---|---|---|
| c1 do-nothing | `C1=unmet scope=31 rows=0 … pins=bad provenance=bad … failed=ledger_absent,pins` exit=1 | no ledger, no v7.3 copies at the entering tip |
| c1 copies-only | `C1=unmet scope=31 rows=0 … pins=ok … failed=ledger_absent` exit=1 | the freeze state |
| c1 no-votes | `C1=unmet … line_ok=31 quote_ok=31 … voted=0 failed=votes` exit=1 | the data commit before any vote must read this |
| c1 unsettled-voters | `C1=unmet … voted=0 failed=votes` exit=1 | voter files the orchestrator never recorded do not count |
| c1 no-line | `C1=unmet … line_ok=0 quote_ok=31 … voted=31 failed=line` exit=1 | the all-held relabel without locating a line fails |
| c1 v72-copies | `C1=unmet … pins=bad … failed=pins` exit=1 | v7.2 bytes as v7.3 fail the pins (the quotes and lines are unchanged, so only the pins separate them) |
| c1 witness | `C1=met scope=31 rows=31 … line_ok=31 … voted=31 dissent=0` exit=0 | feasibility only |
| c2 do-nothing | `C2=unmet claims=0 … pins=bad … failed=entry_absent,pins` exit=1 | no entry, no copies |
| c2 copies-only | `C2=unmet claims=0 … pins=ok … failed=entry_absent` exit=1 | the freeze state |
| c2 quote-echo | `C2=unmet claims=14 … bad_rows=14 … failed=bad_rows,…` exit=1 | a claim that only restates its quote is not a row |
| c2 unlocated | `C2=unmet claims=14 located=0 quote_missing=14 … failed=quote_missing,sources_floor` exit=1 | unlocated quotes fail |
| c2 no-votes | `C2=unmet claims=14 located=14 … entailed=0 failed=entailment` exit=1 | the data commit before any vote must read this |
| c2 two-sources | `C2=unmet claims=14 located=14 … sources=2 failed=sources_floor` exit=1 | one-file depth fails the source floor |
| c2 witness | `C2=met claims=14 located=14 … sources=6 … entailed=14 dissent=0` exit=0 | feasibility only |

Receipts record the literal command with the clone path; clones were removed after the run (the control commits
live only in those clones).
