# Mo54ScribeProvince — PROVINCE.md, round-54 scope append (draft, not applied)

Seat: PROVINCE.md accuracy for round 54 (mori-shokunin). Assignment: draft the minimal append that keeps the
province document accurate after this round — hardware memory-failure kills (SIGBUS/SIGKILL from
`mm/memory-failure.c`, the per-node counters, `HardwareCorrupted`) as kill-event ground, knowledge only, with the
boundary (no injection, no sysctl write; host repair → tsukuroi/operator; MCE/EDAC hardware health not held) — or
state that no change is needed, with line pointers. I wrote no file but this report; PROVINCE.md is unchanged by me.

## 0. Revision and state observed

- Lane root `/home/vgpnk/Projects/shokunin/mori-shokunin`; entering tip `39dcf4d7`, freeze `6830f3af`, data
  `78295c764093ff1f6cee08d7246679900bde7265`, HEAD `2d0347a32b6befd7fd946a83319e04f6d8f004b9` (wave-spec commit).
- The working tree **already carries** an uncommitted round-54 PROVINCE block. That was true of my first `git status`
  (` M PROVINCE.md`), before any read or write of mine, and no round-54 commit touches the file
  (`git log --oneline -3 -- PROVINCE.md` ends at `7b90a3c6`, round-53 attempt 2). The block's author is not
  authenticated by me; `.ufo/waves/round-54/w1/Mo54SentC2Boundary.md:144-148` calls it "the L1's uncommitted
  round-54 PROVINCE note". I treat it as the text under review.
- Sizes: committed tip `PROVINCE.md` is 456 lines; working tree is 476; the addition is one hunk
  `@@ -456,0 +457,20 @@`, i.e. a `## Round-54 appended scope notes (2026-10-27)` section at `PROVINCE.md:457-476`.
  Working-tree digest `sha256 e1afa247f169a104a1fc459e7a50a5329e00f5fb79d11a6ae6cbd020bcfc353b`, 45768 bytes,
  mtime 2026-10-27 01:40:05 -0300 (all observed after my reads; I performed no write to the file).

## 1. Verdict

**A change is needed**, and only inside that block: three factual defects and one boundary gap. It is not a
wholesale rewrite — the paragraphs stay in place and the accurate sentences are kept. Two of the defects are in the
sentence that carries the claim relation to the existing census (`PROVINCE.md:465-466`), one is a category error
about what `HardwareCorrupted` is (`:463-464`), and the boundary list omits `vm.enable_soft_offline` (`:468-469`).
The draft in §3 replaces `PROVINCE.md:457-476` with 31 lines; everything at `PROVINCE.md:1-456` is untouched, so no
existing line citation into the file moves.

## 2. Evidence (command → output → exit code)

### 2.1 The block in the working tree

```
$ git -C /home/vgpnk/Projects/shokunin/mori-shokunin show 2d0347a3:PROVINCE.md | wc -l
456
$ wc -l PROVINCE.md
476 PROVINCE.md
$ git diff -U0 -- PROVINCE.md | grep '^@@'
@@ -456,0 +457,20 @@ at `:94` has drifted (the default now sits near `:237`, `:321`; ScoutProvinceSta
$ git log --oneline -3 -- PROVINCE.md
7b90a3c6 round-53: attempt 2 — residual a2r1 dispatch (8 seats) and 7 returned reports; …
0df80303 round-53: hyaku run-9 orchestrator salvage of unlanded attempt-1 w1 wave state, …
af42101d round-30: routed R7 — PROVINCE stale statements fixed by same-line substitution …
```

Exit 0 throughout. The block begins at `PROVINCE.md:458` with its `##` heading (line 457 is the blank separator
line the diff adds first), and ends at `:476`.

### 2.2 What the memory-failure sources say (v7.3 copies, read-only)

```
$ ls /sys/devices/system/node/node0/memory_failure/
delayed  failed  ignored  recovered  total
$ sed -n '188,232p' corpus/evidence/sources-r54/sysfs-devices-node.v7.3
What: /sys/devices/system/node/nodeX/memory_failure/total      … The total number of raw poisoned pages …
What: /sys/devices/system/node/nodeX/memory_failure/ignored    … how many pages are ignored by memory error recovery …
What: /sys/devices/system/node/nodeX/memory_failure/failed     … failed by memory error recovery attempt …
What: /sys/devices/system/node/nodeX/memory_failure/delayed    … delayed by memory error recovery attempt …
What: /sys/devices/system/node/nodeX/memory_failure/recovered  … recovered by memory error recovery attempt.
$ sed -n '130,175p' corpus/evidence/sources-r54/memory-failure.c.v7.3
.procname = "memory_failure_early_kill" / "memory_failure_recovery" / "enable_soft_offline" /
             "panic_on_unrecoverable_memory_failure"      (four entries, register_sysctl_init("vm", …) at :2710)
$ grep -n 'TRACE_SYSTEM\|TRACE_EVENT' corpus/evidence/sources-r54/memory-failure-trace.h.v7.3
7:#define TRACE_SYSTEM ras
74:TRACE_EVENT(memory_failure_event,
$ grep -n 'pr_fmt' corpus/evidence/sources-r54/memory-failure.c.v7.3
37:#define pr_fmt(fmt) "Memory failure: " fmt
2716:#undef pr_fmt
2717:#define pr_fmt(fmt)	"Unpoison: " fmt
$ grep -i hardwarecorrupted /proc/meminfo
HardwareCorrupted:     0 kB                                   (exit 0)
$ sed -n '1269,1271p' corpus/evidence/sources-r53/proc.rst.v7.3
HardwareCorrupted
              The amount of RAM/memory in KB, the kernel identifies as
              corrupted.
```

So the counters are exactly five (`total`, `ignored`, `failed`, `delayed`, `recovered`), `HardwareCorrupted` is a
host-wide KB amount (not a per-event record), the tracepoint is `ras:memory_failure_event`, and the `vm` memory-error
sysctl family has **four** members, including `enable_soft_offline` (also `vm.rst.v7.3:287,311-316`).

### 2.3 What the census classes do — the "never see it" check

```
$ grep -n 'JOURNAL_JQ_MSGID=\|JOURNAL_JQ_SIGKILL=\|JOURNAL_JQ_SIGSEGV=\|JOURNAL_ID_COREDUMP=\|local -a classes=' tools/mori-census.sh
1076:JOURNAL_ID_COREDUMP=fc2e22bc6ee647b6b90729ab34a250b1
1082:JOURNAL_JQ_MSGID="… (.MESSAGE_ID == \$id) …"                       # no COREDUMP_SIGNAL term
1083:JOURNAL_JQ_SIGKILL="… (.MESSAGE_ID == \$id) and (.EXIT_CODE == \"killed\") and ((.EXIT_STATUS | tostring) == \"9\") …"
1084:JOURNAL_JQ_SIGSEGV="… ((.COREDUMP_SIGNAL | tostring) == \"11\") …"
1337:  local -a classes=(kernel_oom_notice oomd_notice coredump_notice segfault_signal11 unit_sigkill_record unit_failure_record)
$ sed -n '1325,1326p;1468p' tools/mori-census.sh
    user:coredump_notice)      printf '%s' COREDUMP_NOTICE_JOURNAL_USER ;;
    system:coredump_notice)    printf '%s' COREDUMP_NOTICE_JOURNAL_SYSTEM ;;
      emit_finding "$(journal_finding_id "$scope" "$cls")" info "$subj"
$ man 7 signal | grep -E '^ *SIGBUS'
     SIGBUS       P2001      Core    Bus error (bad memory access)
$ grep -rn "HardwareCorrupted\|memory_failure\|hwpoison\|SIGBUS" tools/ --include='*.py' --include='*.sh' | wc -l
0                                                              (grep exit 1: no match)
```

`coredump_notice` is counted by MESSAGE_ID alone (`:1082`), in both scopes, and emits an `info` finding whenever the
count is above zero (`:1468`); only `segfault_signal11` filters on `COREDUMP_SIGNAL=11` (`:1084`), and
`unit_sigkill_record` filters `EXIT_CODE=killed` + `EXIT_STATUS=9` (`:1083`). SIGBUS's default action is core
(`man 7 signal`). Therefore a memory-failure SIGBUS death that produces a coredump **is** counted by the existing
census as a `coredump_notice` record, and the handler's SIGKILL to a unit process **is** counted as a
`unit_sigkill_record` with `attribution=none` — neither carries the memory-failure cause. The working-tree sentence
"the existing kill/OOM reads above never see it" (`PROVINCE.md:465-466`) is false at record level; what is true is
that no OOM class and no signal-11 count sees it. No tool reads `HardwareCorrupted`, the per-node counters, hwpoison
or SIGBUS (grep exit 1, 0 matches), so the block's "no probe … reads it yet" part is true.

### 2.4 C1 freshness bullet: counter scope vs ledger rows

```
$ grep -c '^h=' .ufo/waves/round-54/evidence/c1-scope.txt
31
$ awk '/^## Ledger/{f=1;next} /^## /{f=0} f&&/^\| [0-9a-f]{12} \|/{print substr($0,3,12)}' \
    corpus/knowledge/kernel-v7.3-recheck-r54.md | sort -u | wc -l
31
$ diff scope.txt ledger.txt && echo SETS-IDENTICAL
SETS-IDENTICAL
$ awk -F'entry=' '{split($2,a," "); print a[1]}' .ufo/waves/round-54/evidence/c1-scope.txt | sort | uniq -c
     22 corpus/knowledge/oom-memcg-stat-r50.md
      8 corpus/knowledge/commit-runway-read-r53.md
      1 corpus/knowledge/quota-observability-r48.md
```

The ledger's 31 hashes are exactly the counter's scope set. The ledger's second table
(`## Where the quotes moved`) also has 31 rows (`awk` per section: 31, 31). The per-entry split in the block
(22/8/1) is correct.

One qualifier the block lacks: `corpus/knowledge/overcommit-commit-limit-r52.md:56-58` still reads "what it means
at v7.2" and cites `util.c.v7.2:978-995` in a **decision table**, and `system-pressure-r24.md`'s decision rows still
say v7.2. These are not claim|source|quote rows, so "no claim-table row of the lane pins v7.2 unrechecked" stays
true, but a reader can over-read it as "no v7.2 pointer anywhere". The draft names the r52 column.

### 2.5 Host reads (read-only, allowed by the seat spec)

```
$ uname -r
7.2.11-arch1-1
$ for f in total ignored failed delayed recovered; do printf '%s=%s ' "$f" "$(cat /sys/devices/system/node/node0/memory_failure/$f)"; done
total=0 ignored=0 failed=0 delayed=0 recovered=0
$ for f in memory_failure_recovery memory_failure_early_kill enable_soft_offline panic_on_unrecoverable_memory_failure; \
    do printf '%s=%s ' "$f" "$(cat /proc/sys/vm/$f 2>/dev/null || echo ABSENT)"; done
memory_failure_recovery=1 memory_failure_early_kill=0 enable_soft_offline=1 panic_on_unrecoverable_memory_failure=ABSENT
$ grep -i hardwarecorrupted /proc/meminfo
HardwareCorrupted:     0 kB
```

This reproduces the entry's `## On this host` block. Nothing was written; no module, no injection, no sysctl write,
no OOM, no cgroup change.

## 3. Draft — replace `PROVINCE.md:457-476` with this block

Rationale for each change is in §4. The block is append-only at EOF and leaves `PROVINCE.md:1-456` byte-identical.

```markdown
## Round-54 appended scope notes (2026-10-27)

- **Hardware memory-failure kills (kill events, knowledge only).** The kill/OOM ground above names catalog-ID
  journal records, `memory.events` and the kernel-OOM unit notices. The kernel also kills for a hardware memory
  error: `mm/memory-failure.c` sends SIGBUS — forced `BUS_MCEERR_AR` to the task that touched the poisoned page,
  ordinary `BUS_MCEERR_AO` to the other mappers — or, when unmapping the corrupted page failed, SIGKILL. Its own
  evidence is the `Memory failure:` line prefix, the five per-node counters
  `/sys/devices/system/node/node<N>/memory_failure/{total,ignored,failed,delayed,recovered}`, the host-wide
  `HardwareCorrupted` amount in `/proc/meminfo`, and the `ras:memory_failure_event` tracepoint (entry
  `corpus/knowledge/memory-failure-kills-r54.md`, S521–S524, S502, S507). None of it passes the OOM killer — no
  `memory.events oom_kill`, no kernel-OOM or oomd catalog notice, no `oom:mark_victim` — and the signal-11 count is
  not it. The record classes above are blind to the cause, not to every death: a SIGBUS death that dumps core still
  counts in `coredump_notice`, whose predicate reads no signal field, and the handler's SIGKILL to a unit process
  still counts in `unit_sigkill_record` with `attribution=none`. This section records the ground as knowledge, not a
  capability: no probe, `SURFACE` row or tool reads these files, counts come from the counters and never from
  kernel text (QUALITY 15), and the rows are v7.3 source bytes that were never observed firing — on this 7.2.11
  host the counters and `HardwareCorrupted` read 0 and the v7.3 panic switch is absent.
- **Boundaries:** injecting or unpoisoning a page, loading hwpoison-inject, and writing any `vm` memory-error sysctl
  (`memory_failure_early_kill`, `memory_failure_recovery`, `enable_soft_offline`,
  `panic_on_unrecoverable_memory_failure`) are host actions (operator; host repair → tsukuroi); mori never writes
  one. Soft offline (`enable_soft_offline`, migrating a page with corrected errors) kills no process and is not a
  kill event here. Corrected-error accounting (EDAC, `rasdaemon`, MCE decoding) is hardware-health ground this lane
  does not hold; no sibling is named for it. Mori reads the counters and reports.
- **Freshness:** the remaining 31 v7.2-pinned claim rows (`oom-memcg-stat-r50.md` 22, `commit-runway-read-r53.md`
  8, `quota-observability-r48.md` 1) are rechecked at v7.3 in `corpus/knowledge/kernel-v7.3-recheck-r54.md`, one row
  per claim hash with a v7.3 source row (S515–S520, S508, S514), the line its quote begins on, and a disposition.
  The ledger's 31 hashes are exactly the counter's scope set, so no claim-table row of the lane pins v7.2
  unrechecked after this round; readings outside the claim tables still name v7.2 and are not rechecked
  (`oom-tracepoints-r47.md`, `system-pressure-r24.md`, `overcommit-commit-limit-r52.md:56-58`). No ownership
  change, no new frontier row and no admission claimed here — both claims are scored by the round-54 counters, and
  the section is appended at EOF, so no existing line citation moves.
```

## 4. Per-change rationale

| # | working-tree text | change | why (evidence) |
|---|---|---|---|
| 1 | `:461` "`memory.events` and the kernel OOM path" | "`memory.events` and the kernel-OOM unit notices" | `## Core` `:24` names "kernel-OOM unit notices"; the kernel OOM *event-time attribution* is FR1 (`:47`), not part of the kill/OOM catalog classes this section refers to. |
| 2 | `:463-464` "records the event in … `HardwareCorrupted` of `/proc/meminfo`" | "the host-wide `HardwareCorrupted` amount in `/proc/meminfo`" | `proc.rst.v7.3:1269-1271` — an amount of RAM in KB, not an event record; the per-event record is the counter update (`memory-failure.c.v7.3` `update_per_node_mf_stats`, C2 row 10). |
| 3 | `:465-466` "None of it passes the OOM killer, so the existing kill/OOM reads above never see it." | keep the OOM half, replace the "never see" half | `tools/mori-census.sh:1082` counts `coredump_notice` by MESSAGE_ID with no signal term, both scopes, and emits `info` at count>0 (`:1468`); `:1083` counts `unit_sigkill_record` on `EXIT_CODE=killed` + `EXIT_STATUS=9`; `man 7 signal` gives SIGBUS default action core. So the death is seen, the cause is not. |
| 4 | `:468-469` boundary lists only `vm.memory_failure_*` + the panic switch | lists all four `vm` memory-error sysctls, adds the soft-offline boundary | `memory-failure.c.v7.3:153-158` (`enable_soft_offline` entry) and `:2710` `register_sysctl_init("vm", memory_failure_table)`; `vm.rst.v7.3:287,311-316`; soft offline migrates a page and kills nothing (entry `## Boundaries`). |
| 5 | no host-state or non-admission clause | one clause: rows never observed firing; on 7.2.11 the counters/`HardwareCorrupted` read 0 and the panic switch is absent; no admission claimed | contract C2 named limit ("nothing here was observed firing … the v7.3 bytes describe the current release while the host runs 7.2.11"); §2.5 host reads; rounds 52/53 append the same "no admission" clause (`:455`). |
| 6 | freshness bullet: no per-entry counts; no note that r52's decision table still reads v7.2 | counts 22/8/1; names the r52 column | §2.4 (`uniq -c` 22/8/1); `overcommit-commit-limit-r52.md:56-58` observed. |

## 5. Verified accurate — kept, not rewritten

- The SIGBUS/SIGKILL kill relation (`:461-463`): forced `BUS_MCEERR_AR` for the consuming task
  (`memory-failure.c.v7.3:296`), ordinary `BUS_MCEERR_AO` for others (`:305`, with the "Don't use force here"
  comment), `SIGKILL` via `kill_procs` when unmap failed (`:462-472`, `do_send_sig_info(SIGKILL …)`), matching C2
  rows 3–5. Only the parenthetical grouping was tightened ("for a mapper" → the two roles).
- "five per-node counters" (`:463`): exactly five ABI entries (§2.2), and five files on this host.
- `ras:memory_failure_event` (`:464`): `memory-failure-trace.h.v7.3:4-7,74`.
- "no probe, census surface or tool reads it yet" (`:466-467`): tools grep exit 1, 0 matches.
- "counts come from the counters, never from kernel text (QUALITY 15)" (`:467`): matches the entry's decision-table
  counting note; nothing to change.
- "host actions (operator; host repair → tsukuroi)" and "hardware-health ground the lane does not hold" (`:469-471`):
  consistent with `PROVINCE.md:9` ("never remediation") and the Adjacent tsukuroi row (`:66`), and with the C2
  boundary. I checked whether a sibling should be *named* for EDAC/rasdaemon/MCE: `tsukuroi-shokunin/PROVINCE.md`
  names journal/boot triage (dmesg error classes) and the driver/firmware plane, and a grep for
  `EDAC|rasdaemon|machine.check|MCE|hwpoison|SIGBUS` over it returns no match — so naming tsukuroi for corrected
  error accounting would be a routing claim no province text supports. The draft therefore keeps it un-named.
- The freshness facts (31 rows, the three entries, the ledger path): §2.4.

## 6. Pointer integrity

- The draft replaces `:457-476` only; the committed head `:1-456` stays byte-identical, so every existing citation
  into `PROVINCE.md` (e.g. `:6-10`, `:22-28`, `:44-57`, `:94`, `:236`, `:294`, `:359`, `:375`, `:455`) still resolves.
- The block grows from 20 to 31 lines; nothing cites `:457-476` in a **committed** file (`grep -rn
  "PROVINCE.md:4[0-9][0-9]"` over `SKILL.md`, `corpus/README.md`, `SCORECARD.md`, `.ufo/waves/round-54/` finds only
  one hit, in the uncommitted sibling report below).
- `.ufo/waves/round-54/w1/Mo54SentC2Boundary.md:144-148` cites the block as `PROVINCE.md:456-472`, `+456,21`. The
  actual hunk is `+457,20` and the block ends at `:476`; that report's pointer is off. It is that seat's file, not
  mine to edit — flagged for the L1 (finding F7).

## 7. Scratch, host and tooling discipline

- Scratch `/fast/scratch/hyaku/mori-r54/Mo54ScribeProvince/` created with `mkdir -p`, `TMPDIR` set under it; it held
  only `scope.txt`, `ledger.txt`, `tmp/`, and was removed at the end. No clone, no fixture, no network fetch, so the
  network and one-clone rules were not exercised.
- Disk guard before the work: `/home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status` → exit 0,
  `/fast/scratch/hyaku` 27 % used, 593.2G free. No ENOSPC.
- Read-only throughout: `git show`/`log`/`diff`/`rev-parse` only (no add/commit/stash/checkout/reset/pull/push, no jj
  command), `/proc` and `/sys` reads only, `man 7 signal`. No pacman, no install, no upgrade, so there is no tooling
  change to record. No file under `corpus/`, `tools/`, `considerthese/` or the wave directory was written except this
  report. No credential material, session, private URL or machine id is reproduced here.

## 8. Limits

- I did not run `count-c1.py` or `count-c2.py`; the scope/ledger comparison in §2.4 is a hash-set comparison over
  the committed evidence file and the ledger table, not the counters' own output. Another seat measures the
  counters.
- I verified the `HardwareCorrupted` doc row and the five-counter ABI in the committed copies; I did not re-fetch the
  six v7.3 files (independent re-fetch is another seat's surface).
- The SIGBUS→coredump step rests on `man 7 signal` (default action core) plus the census predicate, not on an
  observed coredump; no memory failure has occurred on this host and I triggered none.
- The block's author is not authenticated by me; I reviewed the bytes present in the working tree.
- A dispatched seat is not an independent judge: these are drafting findings, and the L1 decides whether to apply
  the block and whether to correct the entry.

## Findings

| # | severity | file:line | finding |
|---|---|---|---|
| F1 | HIGH | `PROVINCE.md:465-466` (working-tree block) | "the existing kill/OOM reads above never see it" is false at record level: a memory-failure SIGBUS death that dumps core is counted by `coredump_notice`, whose predicate (`tools/mori-census.sh:1082`) has no signal term and which emits an `info` finding at count>0 (`:1468`), and the handler's SIGKILL to a unit process is counted by `unit_sigkill_record` (`:1083`). The census is blind to the cause, not to the death. Draft corrects. |
| F2 | MED | `PROVINCE.md:463-464` | `HardwareCorrupted` is named as something that "records the event"; it is a host-wide KB amount of memory the kernel identifies as corrupted (`proc.rst.v7.3:1269-1271`), read live as `0 kB`. Draft rewrites it as a host-wide amount. |
| F3 | MED | `PROVINCE.md:468-469` | The boundary lists `vm.memory_failure_*` and `vm.panic_on_unrecoverable_memory_failure` but omits `vm.enable_soft_offline`, a fourth `vm` memory-error sysctl (`memory-failure.c.v7.3:153-158,2710`; `vm.rst.v7.3:287,311-316`), and leaves soft offline (no kill) undefined in province terms. Draft completes both. |
| F4 | MED | `corpus/knowledge/memory-failure-kills-r54.md:16` (C2 row 1, hash `fcf9f378a818`) | The row's claim "Every message the memory-failure handler prints starts with the same prefix, 'Memory failure:'" is falsified for the unpoison/soft-offline half of the same file: `memory-failure.c.v7.3:2716-2717` re-defines `pr_fmt` to `"Unpoison: "`, and 16 `pr_*` calls after that line (in `unpoison_memory` at `:2736` and the soft-offline code) print with that prefix. The row is scoped to "the handler", so it may still be voted `entailed`; I report the counter-evidence, not a vote. Correcting the claim changes the row hash and needs fresh votes — an L1 decision, not a rule change. |
| F5 | LOW | `PROVINCE.md:457-476` | The block has no non-admission clause; rounds 52/53 append one (`:455`). Without it, a reader can take the section as a capability statement before the round-54 counters score. Draft adds one clause. |
| F6 | LOW | `PROVINCE.md:474-475` | "no claim-table row of the lane pins v7.2 unrechecked" is true but can be over-read: `overcommit-commit-limit-r52.md:56-58` still carries a "what it means at v7.2" decision column and `util.c.v7.2:978-995`, and `system-pressure-r24.md` decision rows still say v7.2. Draft names the r52 column. |
| F7 | LOW | `.ufo/waves/round-54/w1/Mo54SentC2Boundary.md:144-148` | That report cites the PROVINCE block as `PROVINCE.md:456-472`, `+456,21`; the actual hunk is `@@ -456,0 +457,20 @@`, block `:457-476` (committed tip 456 lines). If the block is applied, that pointer needs correcting. Either way, no committed file cites those lines, so replacing the block moves no citation. |
