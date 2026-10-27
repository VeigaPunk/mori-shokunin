# Mo54ScribeLog — round-54 LOG.md `## Round 54` draft

Seat: Mo54ScribeLog (scribe, leaf). Task: draft the append-only LOG.md round-54 entry, fenced, no product edits.
Read-only over the lane; the only file written is this report.

## Behavior (observed)

Reads performed (all read-only, absolute paths; no lane mutation, no git/jj mutation, no network):

| read | what it gave |
|---|---|
| `.ufo/waves/round-54/contract.md` (150 lines) | the two claims, target lines, controls, kill rules, frontier step, routed defects D1–D3 |
| `git log --oneline -12` in the lane | entering tip `39dcf4d7`, freeze `6830f3af`, data `1116c092`, correction `78295c76`, spec `2d0347a3` |
| `.ufo/waves/round-54/evidence/c1-at-data.txt`, `c2-at-data.txt` | at-data counter lines and exits |
| `.ufo/waves/round-54/evidence/control-c1-do-nothing.txt`, `control-c2-do-nothing.txt` | before receipts and their literal commands |
| `evidence/selftest-c1.txt`, `selftest-c2.txt` | `C1_SELFTEST pass=57 fail=0`, `C2_SELFTEST pass=54 fail=0` |
| `evidence/freeze-sha256.txt` | 37 pinned entries |
| `evidence/census-start.txt` | 23 W04 rows, `exit=0` |
| `evidence/d3-relocation.txt` | eight byte-exact moves (`cmp=ok`) and the `--repo/` rmdir |
| `evidence/sweeps.txt` | host read of the memory-failure surfaces on 7.2.11; assimilation sweep 0 |
| `corpus/knowledge/kernel-v7.3-recheck-r54.md` (109 lines) | 31 ledger rows, the moved-line table, the drift note |
| `corpus/knowledge/memory-failure-kills-r54.md` (86 lines) | 21 rows, decision table, sysctl table, host section |
| `corpus/lessons/round-53-verifier-spotcheck.md:38-70,155-180` | the routed defects and the closure's routing list |
| `corpus/QUALITY.md` rows 149–151, `SCORECARD.md:2818-2875` | D3's criterion, D2's appended correction |
| `.ufo/waves/round-54/w1-spec.json` (via `python3 -c`) | 74 items; roles reviewer 19, critic 18, executor 15, scribe 9, scout 4, sentinel 3, mutation-tester 2, connector 2, revenger 1, simplifier 1 |

Not measured at drafting time, therefore `[L1 fills]` in the draft: the at-landed counter lines and their revision,
the vote tallies and dissent, `w1-results.json` counts (absent: `ls .ufo/waves/round-54/w1-results.json` → no such
file), census-end (absent), the D2 landing commit (SCORECARD.md is modified in the working tree, uncommitted), the
considerthese result, the round total, and the "not done" list. The wave was mid-flight (21 report files under
`w1/` when read).

## Draft (fenced; append after the round-53 section at the end of LOG.md)

```
## Round 54 (L1 MoriR54, attempt 1; C1 freshness, C2 depth)

Entering tip `39dcf4d7`; freeze `6830f3af` (contract, both counters with selftests `C1_SELFTEST pass=57 fail=0`
and `C2_SELFTEST pass=54 fail=0`, fourteen control receipts, `evidence/freeze-sha256.txt` with 37 entries,
census-start rc 0 with 23 W04, sweeps, ten v7.3 copies); data `1116c092` and correction `78295c76` (C2 row 1
reworded and a decision-table counting note added before any seat ran; per-row claim files
`evidence/c1-claims.txt`, `evidence/c2-claims.txt`); wave spec `2d0347a3` (one v2 wave w1, 74 seats: the 24 voter
seats Mo54Rc01–12 and Mo54En01–12, 39 attack seats). Trigger: the round-53 `Planned (round 54)` named the v7.3
trigger for what its ledger does not cover, and the counter's `--scope` at `39dcf4d7` still pinned 31 claim rows to
Linux v7.2 (`evidence/c1-scope.txt`), so freshness (5) and depth (5) both had open ground.

C1 — freshness: the remaining 31 v7.2-pinned claim rows re-verified at Linux v7.3 (ledger
`corpus/knowledge/kernel-v7.3-recheck-r54.md`, one row per claim hash: derived status, a v7.3 source row S515–S520
— S508/S514 for `mm/util.c` and `mm/mm_init.c` — the v7.3 line where the quote begins, the quote and a
disposition; counter `count-c1.py`). Surface: 22 rows of `oom-memcg-stat-r50.md`, 8 of
`commit-runway-read-r53.md`, 1 of `quota-observability-r48.md`. Re-verification result: 31 held, 0 absent; all 31
v7.2 quotes still occur verbatim in the v7.3 copies, and four of the eight source files did not change between the
tags (`mm/oom_kill.c`, `lib/percpu_counter.c`, `include/linux/percpu_counter.h`,
`include/uapi/asm-generic/errno.h`). Three files moved the quoted lines: `mm/memcontrol.c` (258 changed lines; the
OOM report block +45, the `memory.stat` reader +84), `mm/mm_init.c` (+4) and the rendered cgroup-v2 page (+31);
`mm/util.c` changed 14 lines, none at a quoted line. Dispositions read `holds` pending the wave's votes: [L1
fills] (RECHECK seats, per-row tally, dissent). New against round 53: a line arm — each row names where its quote
begins in the v7.3 copy — and voter binding — a voter counts only when `w1-results.json` lists a result of that
name.

C2 — depth: new entry `corpus/knowledge/memory-failure-kills-r54.md` — hardware memory-failure kills at Linux
v7.3, the kill class an OOM-line census cannot see (`SIGBUS`/`SIGKILL` from `mm/memory-failure.c`, the
`recovery action` line, the five per-node `memory_failure` counters, `HardwareCorrupted`, the early/late and
recovery sysctls, v7.3's `panic_on_unrecoverable_memory_failure`, `ras:memory_failure_event`): 21
claim|source|quote rows over six copies (S521 `mm/memory-failure.c`, S522 `hwpoison.rst`, S523
`sysfs-devices-node`, S524 `trace/events/memory-failure.h`; S507 `vm.rst` and S502 `proc.rst`, whose used-by gains
the entry), a decision table (kernel line → kill class) and a sysctl table, counter `count-c2.py`. Host read
2026-10-27 on 7.2.11: node0 counters all 0, `HardwareCorrupted: 0 kB`, recovery 1, early kill 0, and the v7.3
panic sysctl absent. Votes: [L1 fills] (ENTAILMENT seats, per-row tally, dissent).

Before and after. Counting commands `python3 .ufo/waves/round-54/count-c1.py R` and
`python3 .ufo/waves/round-54/count-c2.py R`. Before (entering `39dcf4d7`): `C1=unmet scope=31 rows=0 matched=0
status_ok=0 line_ok=0 quote_ok=0 source_rows=bad pins=bad provenance=bad held=0 absent=0 holds=0 changed=0 voted=0
dissent=0 … failed=ledger_absent,pins`, exit 1 (`evidence/control-c1-do-nothing.txt`); `C2=unmet claims=0
located=0 quote_missing=0 bad_rows=0 sources=0 source_rows=bad pins=bad provenance=bad entailed=0 dissent=0 …
failed=entry_absent,pins`, exit 1 (`evidence/control-c2-do-nothing.txt`). At data `78295c76`: `C1=unmet scope=31
rows=31 matched=31 status_ok=31 line_ok=31 quote_ok=31 source_rows=ok pins=ok provenance=ok held=31 absent=0
holds=31 changed=0 voted=0 dissent=0 rev=78295c76… failed=votes`, exit 1 (`evidence/c1-at-data.txt`);
`C2=unmet claims=21 located=21 quote_missing=0 bad_rows=0 sources=6 source_rows=ok pins=ok provenance=ok
entailed=0 dissent=0 rev=78295c76… failed=entailment`, exit 1 (`evidence/c2-at-data.txt`). After: [L1 fills]
(`evidence/c1-at-landed.txt`, `evidence/c2-at-landed.txt`, R = [L1 fills]). Controls that skip the work stay
unmet: C1 do-nothing, copies-only, no-votes, unsettled-voters, no-line, v72-copies; C2 do-nothing, copies-only,
quote-echo, unlocated, no-votes, two-sources. Both witnesses met (feasibility, disclosed): C1 `C1=met … voted=31
dissent=0` exit 0; C2 `C2=met claims=14 located=14 … sources=6 … entailed=14 dissent=0` exit 0.

Assimilation: none — `merge/mori/` holds 0 files naming memory failure, hwpoison, SIGBUS, percpu_counter or v7.3
(`evidence/sweeps.txt`). considerthese: `2026-10-26.md` suggestion 3 — re-execute what closures only
evidence-verified: a wave seat re-runs the round-53 frozen counters and the commit-runway selftest at the scored
revision `0b36d23e` and reports agreement or the exact divergence; it lands as a lesson section. Result:
[L1 fills]. Mistakes mined (lesson): M1 a SCORECARD row citing a non-landed receipt (round-53 closure D2, and the
round-50 pair the same sweep found); M2 eight lane-root strays carried for 26 rounds (D3). Further wave findings
[L1 fills].

Round-53 closure routed defects. D1 (attribution: the salvage commit `0df80303` was made by the hyaku
orchestrator under the lane identity): disclosed only, recorded not rewritten. D2 (the round-53 C1/C2 After cells
cite the at-salvage receipts at `0df80303`): an appended SCORECARD correction names `evidence/c1-at-landed.txt`
and `evidence/c2-at-landed.txt` (R = `0b36d23e596276c70725873621fe15a28c87189f`) as the landed measurement,
token-identical to the cells apart from `rev=`; the same sweep found the round-50 pair and appended a second
note; landing commit [L1 fills]. D3 (the eight inherited lane-root strays): seven relocated byte-exact under
`.ufo/waves/round-28/misroot-lane-root/` (`base.c`, `main.c`, `meminfo.c`, `oom_kill.c`, `sd-main.c`,
`user@.service.in`, `MANPAGE.md`) and `0` under `.ufo/waves/round-38/misroot-lane-root/`, every file `cmp=ok`, the
empty untracked `--repo/` removed, receipt `evidence/d3-relocation.txt`, landed with the data commit `1116c092`;
QUALITY 149 keeps the lane-root listing checked. Census start rc 0, 23 W04 (`evidence/census-start.txt`); end
`evidence/census-end.txt` [L1 fills].

Named limits stand: the line arm proves where a quote begins, not that the surrounding code means the same; votes
are lane seats and the results binding proves the orchestrator recorded a seat of that name, not who wrote the
report bytes; the C2 rows are read from v7.3 source, and no memory failure has been observed on this host (the
v7.3 panic sysctl is absent from 7.2.11). Not done, stated: [L1 fills]. Wave route: [L1 fills] seats returned of
74, round total [L1 fills].
```

## Gates run on this draft

- Draft length: the fenced block spans lines 35–111 of this report (Python scan of the fence markers), i.e. 75
  content lines.
- Append anchor (measured): LOG.md is 2888 lines and ends with a newline at 2888, no trailing blank lines; the
  round-53 heading at 2841 is preceded by two blank lines (2839, 2840). Appending in that pattern puts the
  `## Round 54` heading at LOG.md:2891 (blank at 2889, 2890) and the 75-line entry at LOG.md:2891–2965.
- Line-start safety: `grep -nE '^(RECHECK|QUOTE|ENTAIL|REPLACE)([^A-Za-z]|$)'` over this report → no match, rc 1
  (158 lines at that run; the words appear only inside sentences, never as a line-starting vote line).
- Append-only: the draft is a fenced block only; no LOG.md bytes were written or proposed for rewrite. Round-53
  section text is untouched.
- Every value in the draft was read from a named receipt, the ledger/entry, the contract, or the lane's git log;
  eight values are marked `[L1 fills]` because they were not measured at drafting time (`w1-results.json` absent,
  census-end absent, SCORECARD D2 note uncommitted, wave mid-flight).

## Touched surfaces

Written: `.ufo/waves/round-54/w1/Mo54ScribeLog.md` (this file) only.
Not written: LOG.md, SCORECARD.md, SKILL.md, SHONEN.md, PROVINCE.md, corpus/**, tools/**, considerthese/**,
any other file under `.ufo/waves/round-54/`.
Scratch: `/fast/scratch/hyaku/mori-r54/Mo54ScribeLog/` created for TMPDIR hygiene and removed at the end; nothing
was cloned, no fixture, no network fetch. No tool installed or upgraded this seat.

## Out of scope

No counter, predicate, control, kill rule or frozen file was read for change or proposed for change. No claim
verdict is issued here (this is a scribe seat, not a voter). No SKILL/PROVINCE/README/lesson drafting.

## Findings

1. **LOW — `corpus/QUALITY.md:1493,1511`** cite `corpus/lessons/round-54.md` (M1, M2), which does not exist in the
   working tree at drafting time (`test -f` → absent; `git status` shows no untracked copy). If the lesson is not
   integrated, QUALITY rows 149 and 151 point at a missing file. Transient if a drafting seat lands it.
2. **LOW — `SCORECARD.md:2852-2857` (D2 correction) is uncommitted** while the LOG draft has to name its landing
   commit; the draft marks that hash `[L1 fills]` rather than guessing. Same for `evidence/census-end.txt`.
3. **LOW — `LOG.md:2841` heading says "attempt 1"** although round 53 landed via attempt 2 (its body records it).
   The round-54 draft follows the same heading convention; if the L1 prefers an attempt-qualified heading, the
   first line is the only place to change.
4. **LOW — `w1-spec.json` role histogram (reviewer 19, critic 18)** does not by itself identify the 24 voter seats;
   the draft takes "24 voter seats" from the seat names (`Mo54Rc01–12`, `Mo54En01–12`) and the spec commit
   message, and "39 attack seats" from that message only — the attack count is not re-derived here.

## Artifact paths

- This report: `.ufo/waves/round-54/w1/Mo54ScribeLog.md`
- Draft source facts: `.ufo/waves/round-54/contract.md`, `evidence/{c1-at-data,c2-at-data,control-c1-do-nothing,control-c2-do-nothing,selftest-c1,selftest-c2,freeze-sha256,census-start,d3-relocation,sweeps,c1-scope}.txt|txt`, `corpus/knowledge/{kernel-v7.3-recheck-r54,memory-failure-kills-r54}.md`, `corpus/lessons/round-53-verifier-spotcheck.md`, `corpus/QUALITY.md`, `SCORECARD.md`, `LOG.md`, `w1-spec.json`.
