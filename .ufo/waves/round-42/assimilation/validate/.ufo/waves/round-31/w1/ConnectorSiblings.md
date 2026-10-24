# Round 31 w1 — Connector sibling-overlap scan (C1 FR5, C2)

Seat `MoriR31.ConnectorSiblings`. Read-only scan of `corpus/` and `tools/` in the 20 sibling lanes under
`/home/vgpnk/Projects/shokunin/*-shokunin` (mori excluded from the hit tables; its own predecessors listed separately).
No lane, fleet or sibling write; no git write; no install (rg, sed, grep, sha256sum were already on the host).

Method note: the `grep` tool returned "No matches found" for valid patterns when the path was the multi-lane glob
`/home/vgpnk/Projects/shokunin/*-shokunin/corpus` (single-directory calls worked), so the cross-lane passes used
`rg -n` through `timeout 90` in bash. Passes covered `*/corpus/knowledge`, `*/corpus/SOURCES.md`,
`*/corpus/PROVINCE.md` and `*/tools`; the `files.?opened` pass additionally excluded `**/evidence/**`,
`**/live/**`, `**/frozen/**` to keep the listing bounded.

Scan commands (all read-only, `timeout 90`, run from `/home/vgpnk/Projects/shokunin`; `--glob '!mori-shokunin/**'`):

```sh
rg -n -i 'pgrep' */corpus/knowledge */corpus/SOURCES.md */corpus/PROVINCE.md */tools
rg -n -i 'cmdline|/proc/[0-9<]|starttime|start time|start-time|btime' */corpus/knowledge */corpus/SOURCES.md */corpus/PROVINCE.md */tools
rg -n -i 'files.?opened|opened files|blind' */corpus/knowledge */corpus/SOURCES.md */corpus/PROVINCE.md */tools
rg -n -i 'watchdog|liveness' */corpus/knowledge */corpus/SOURCES.md */corpus/PROVINCE.md */tools
rg -n 'shokunin-watchdog' */corpus */tools */PROVINCE.md
rg -n 'TASK_COMM|comm truncat|/proc/<pid>/comm|comm field' */corpus/knowledge */corpus/SOURCES.md */tools
```

Verdict vocabulary: **cite** = mori's entry/tool should name it (prose prior art or boundary);
**defer (adjacency)** = the sibling owns that claim, mori names it and does not restate or absorb it;
**ignore** = no bearing on C1/C2 (name collision or different mechanism).

## Headline

1. C1 has substantial sibling prior art on **pid identity binding** (souji, tameshi, kumitate) but **none on the fleet
   watchdog itself**: no other lane probes `scripts/shokunin-watchdog.sh` for liveness. The prior art is therefore
   prose-adjacency, not a duplicate entry.
2. C1's stated premise is imprecise: mori's own `corpus/knowledge/oom-victim-selection-r27.md:30` already states that
   `/proc/<pid>/comm` is "at most 15 bytes". S169 is still a new *page-level* source, but the entry must acknowledge
   r27 rather than present comm truncation as first discovery (contract text is frozen; the counter itself is unaffected).
3. C2 has **no sibling prior art**: no sibling tool or knowledge entry parses a writer's files-opened list. The nearest
   hits are a syscall open-trace method and a boot-writer verifier, both different mechanisms.
4. Neither **kumitate** nor **tsukuroi** PROVINCE claims daemon liveness. Tsukuroi explicitly routes "liveness or
   progress correlation" to mori and limits itself to OS/unit state (`tsukuroi-shokunin/PROVINCE.md:49-50`).

## Table A — C1 hits (watchdog identity from pid probes)

| # | hit (path:line) | what it covers | verdict |
|---|---|---|---|
| A1 | `souji-shokunin/corpus/knowledge/process-residue-observations.md:46-48`; `souji-shokunin/corpus/SOURCES.md:95` (S075) | Identity binder `(pid, starttime, boot_id)`; starttime is `stat` field 22 in clock ticks; "A pid alone is never identity" | **cite (prose)**: direct prior art for pre-assigned S171; S075 is souji's id and must not appear in mori's table (count-c1.py reads mori `corpus/SOURCES.md` only) |
| A2 | `souji-shokunin/corpus/SOURCES.md:105,108` (S085, S088) | S088 supersedes S085's teaches because "never as a liveness proof" was lane policy, not page text | **cite** as Gate-draft discipline for S171/S173: teach only what the fetched page says |
| A3 | `tameshi-shokunin/corpus/knowledge/guard-kill-closure.md:79,84,89` | PID reuse after leader exit; keep `(pid, starttime)`; "same-tick PID reuse can race ... starttime has tick granularity" | **cite**: supplies the measured "cannot" cell for the start-time rung |
| A4 | `kumitate-shokunin/corpus/knowledge/singleton-and-queue-ownership.md:22-27` | "PID existence alone can't distinguish reuse — starttime+bootId bind identity"; lock users `fleet-dispatcher`, `ufo-l0-watch`, `ufo-stale-watchdog` | **defer (adjacency)**: same principle, **different daemon** (ufo-fsd-alpha `ufo-mission-result.mjs` locks), not `scripts/shokunin-watchdog.sh` |
| A5 | `kumitate-shokunin/corpus/knowledge/queue-and-claim.md:47-50`; `enqueue-admission.md:30-31` | Stale lock reclaim: a live pid whose `/proc/<pid>/cmdline` lacks `fleet-dispatcher.mjs` is abandoned; empty cmdline counts as owner | **defer (adjacency)**: the closest sibling *cmdline-discriminant* test; it is dispatcher ownership semantics, not the fleet watchdog |
| A6 | `tabi-shokunin/corpus/knowledge/webbridge-daemon-disposition.md:73-78,101` (+ `webbridge-revival-assessment.md:88,260`) | Daemon-down disposition by independent surfaces: no listener, `pgrep -x` none, stale pid/addr pointers, process cmdline, persistence via parent | **cite**: method precedent — absence was never decided by one probe; mori's table should demand the same |
| A7 | `mado-shokunin/corpus/knowledge/idle-lock-plane.md:368-374` | Session-child daemon invisible to `systemctl --user is-active`; "only the `pgrep` half discriminates"; measured present→absent transition | **cite**: supports the "unit status is not process presence" row |
| A8 | `game-dev-3d-shokunin/corpus/knowledge/unreal-mcp/executability/gameplay-gas.md:167,177` | `pgrep -af` empty throughout while one `ss` sample showed a foreign sibling process on the port; a port-open sample was not the named daemon | **cite**: measured foreign-process false positive for a name probe |
| A9 | `kama-shokunin/corpus/knowledge/endpoint-identity.md:88,99` | Liveness/identity are different questions; "A refusal or timeout is `DEAD` for that sample ... not proof the process has stopped" | **cite (analogue)**: the exact epistemic rule C1 needs for a failed or degraded pid probe; different probe layer, keep the boundary explicit |
| A10 | `kotoba-shokunin/corpus/knowledge/dispatch-prompt-audit-round7.md:6,55,60`; `kumitate-shokunin/corpus/knowledge/round-close-gate.md:68,94,122`; `kimi-skills-plugins.md:116,124` | Three audits of the same `scripts/shokunin-watchdog.sh` for prompt generation, round-close (`report_of()`), and a recorded size of 5,540 B | **defer (adjacency)**: kotoba owns prompt fidelity, kumitate owns round-close. Their line numbers are stale: current script is v5, 17,846 B, sha256 `04a3a2148ef...`, `report_of()` at `:144`. Pin sha, never their line numbers |
| A11 | `tabi-shokunin/corpus/knowledge/closeout-r11.md:141` | Watchdog `LANES` roster omission | **ignore**: fleet membership, not liveness |
| A12 | `tsukuroi-shokunin/corpus/knowledge/boot-writers-r19.md:21`; `mado-shokunin/corpus/SOURCES.md:98` (S086) | Other lanes' `pgrep -f` guards (snapper watcher; walker launcher) | **ignore**: unrelated daemons; same argv-substring pattern, no identity rule to cite |
| A13 | mori lane: `observability-census-r1.md:12,23,31`; `observability-surfaces-r2.md:89-95,110-126`; `audit-r11.md:200-201` | The lane's own probe (`pgrep -af shokunin-watchdog`, `pids=0`, `WATCHDOG_ABSENT`, pgrep-missing arm) and the open classes D05 (unavailable ≠ absent) and D06 (argv-substring false positive; "mori with kumitate for authoritative daemon identity") | **cite (in-lane predecessors)**: the entry must supersede/reconcile r2's measured statements, not restate them as new |
| A14 | mori `oom-victim-selection-r27.md:30` | `/proc/<pid>/comm`, at most 15 bytes (earlyoom `--prefer/--avoid/--ignore`) | **cite**: contradiction with the contract's "no knowledge entry ... on comm truncation" premise; reconcile in prose |

Dedicated upstream-source check: `grep -n -i 'proc_pid_stat|proc_pid_comm|proc_pid_cmdline|pgrep|PR_SET_NAME|pid_max|procps' mori-shokunin/corpus/SOURCES.md` → **NO PRIOR ROW**. No mori source row shares the pre-assigned URL space, so S161-S173 are genuinely fresh pins (souji's S068/S075 are the same proc_pid_stat page at man-pages 6.19; state that as adjacency, not duplication).

## Table B — C2 hits (files-opened / blind-writer gate)

| # | hit (path:line) | what it covers | verdict |
|---|---|---|---|
| B1 | `tameshi-shokunin/corpus/knowledge/input-keyed-coldread-credit.md:54-62`; `tameshi-shokunin/corpus/SOURCES.md:69` (S060) | `strace -f -y` open trace: regular files "opened read-only by name"; cannot see env, stat-only checks, inherited fds | **ignore**: syscall-trace completeness, not a static parser of brief text; no shared contract with C2 |
| B2 | `souji-shokunin/tools/impl-42.sh:730` | Prints "files opened for header" in an evidence inventory | **ignore**: report formatting, not a gate |
| B3 | `tsukuroi-shokunin/tools/check-boot-writers.py:2-6` | Verifier for `/boot/limine.conf` writer attribution | **ignore**: name collision only ("writers" = boot-chain writers) |
| B4 | `chousa-shokunin/corpus/knowledge/gate-baseline-r8.md:90`; `hardening-r10.md:271`; `kagi-shokunin/corpus/knowledge/op-ref-consumption.md:245` | Gates' own blind spots / masked sets | **ignore**: meta-gate limits, not writer blindness |
| B5 | `souji-shokunin/tools/impl-06.sh:18,92,348-350` | Author + blind seat must emit matching SAFE verdicts for a vault target | **ignore**: blind-seat pairing, not a files-opened list |
| B6 | mori `.ufo/waves/round-30/check-blind-wave.sh` (in-lane) | Predecessor gate; D1 defects (parses past the list, one hit per file, label-form miss) | **cite as baseline only** (C2 supersedes it; not a sibling) |

Negative result (verified): `rg -l -i 'files.?opened|opened files|writer-forbidden|writer-missing'` over sibling
`corpus/knowledge` and `tools` returns only B1-B2 plus prose uses of "files opened" in source notes. **No sibling gate
parses a writer's files-opened list.** C2 must therefore not claim cross-lane portability or prior art; the only
predecessor is mori's round-30 gate.

## PROVINCE liveness check

- **kumitate** (`kumitate-shokunin/PROVINCE.md:1-38`): owns "orchestration & tooling", the origin script/runtime
  layers, the kimi substrate and its gates; Frontier rows are OMP harness, MCP, isolation, durable execution. A
  case-insensitive scan for `liveness|alive|watchdog|daemon|pgrep|pidof` matched **zero lines in this file**. It claims
  no daemon liveness. Its knowledge entry A4 is lock identity, not liveness.
- **tsukuroi** (`tsukuroi-shokunin/PROVINCE.md:49-50`): ADJ-04 routes "Host pressure or a kill signal needs fleet/wave
  attribution, **liveness** or progress correlation" to **mori**, retaining "OS memory, journal and boot diagnosis";
  ADJ-05 retains "systemd and resource evidence" but states "**unit liveness cannot prove dispatch correctness**" and
  routes dispatch to kumitate. So tsukuroi explicitly **disclaims** daemon liveness; it does not compete for FR5.
- Supporting boundary: mori `PROVINCE.md:48` (FR5) already says "an unavailable pid probe is not absence, and
  argv-substring matches do not establish daemon identity"; mori `PROVINCE.md:82-83` assigns endpoint health to kama
  and records that souji routes liveness/resource findings to mori.

## Contradictions and second-order risks

1. **Contract premise vs r27:30.** The C1 premise says no knowledge entry covers comm truncation; mori's own r27 line
   does. The frozen counter does not read that sentence, so P-C1 is unaffected, but an entry that claims first
   discovery is falsifiable from the lane's own corpus. Reconcile in prose and keep the new id's teaches page-scoped.
2. **Sibling line-number drift.** The same watchdog script is cited at `:39` (kotoba), `:44` (kumitate) and `:188-194`
   (mori r2); current v5 has `report_of()` at `:144` and `mission_live` at `:227-236`, 17,846 B, sha256 `04a3a214...`.
   Any citation of a sibling's line numbers is a stale-fact hazard; pin the script sha and read the current file.
3. **Daemon-name ambiguity.** Kumitate's `ufo-stale-watchdog`/`fleet-dispatcher` belong to ufo-fsd-alpha; mori's target
   is the fleet-root `scripts/shokunin-watchdog.sh`. Absorbing A4/A5 as if they were the same daemon would be a
   wrong-owner claim. Name both sides explicitly.
4. **Counter mechanics.** count-c1.py resolves every `S###` against mori's `corpus/SOURCES.md`; sibling ids (S060,
   S075, S086) in a table row would be unresolvable. Sibling prior art belongs in prose with pinned commits.
5. **No C2 overclaim.** With no sibling gate, a header sentence claiming fleet-wide applicability would be unsourced;
   the honest statement is "supersedes the round-30 lane gate; no sibling equivalent exists (scan date)".
6. **Axis check.** C1 move: depth ↑ (sourced decision table), calibration ↑ (measured "cannot" rows), freshness neutral
   (pins are current), operability neutral. C2 unchanged. No axis harmed.

## Proposed move (one bounded synthesis)

Shape C1's table as a **five-rung discriminant ladder** whose verdict column states what each observation binds and
what it cannot, capped by the daemon's own identity rule:

1. `pgrep -x <name>` (comm/name match) — cannot see a bash-script daemon: the kernel execs the interpreter and comm is
   the interpreter's name (S169, S163/S164, S165).
2. `pgrep -af <string>` (full-cmdline substring) — can count any process whose argv mentions the string (editor, grep,
   the probe itself); one positive sample is not identity (S161/S162, S168; mori audit-r11 D06; A8).
3. `/proc/<pid>/cmdline` — binds argv at exec; can be empty (kernel thread/zombie) and is rewritten for interpreted
   scripts (S170, S165, S166/S167; kumitate A5 shows the empty-cmdline edge).
4. `/proc/<pid>/stat` field 22 starttime + boot id — binds a process across samples; tick granularity leaves a
   same-tick reuse window (S171, S163, S173; tameshi A3); pid_max wrap bounds pid space (S173).
5. Daemon side effects (`watchdog.log` mtime, `.ufo/state/*.round` age) — independent of pid identity, but lag by
   design (default tick 450 s; `scripts/shokunin-watchdog.sh:9,27-32`).

[INFERENCE] pending the S161-S173 Gate quotes: rung 1's interpreter-comm reading and rung 3's empty/cmdline-rewrite
cases must each be re-derived from the fetched quote before the row lands; none of these is a measured host fact yet.

Ceiling paragraph: the driver's own identity rule is a live pid whose environ carries `SHOKUNIN_LANE=<lane>`
(script `:190,227-236`), authoritative for lanes but not readable by an external probe without crossing mori's privacy
bound. Therefore every external observation is **consistent-only**: "alive" is at best "not contradicted", and a
missing or degraded probe is never absence (S161 exit statuses; mori D05; kama A9). Cite A1-A10, A13-A14 in prose with
pinned sibling commits; keep the table to mori S-ids (S161-S173 plus pre-existing mori ids). This is additive to
r1/r2 (which measured the probe) rather than a restatement, and it converts D06's "mori with kumitate" note into an
explicit boundary instead of an unresolved dependency.

For C2, add one header line recording the verified negative: no sibling gate exists; supersedes only the round-30
gate. No other C2 change follows from this scan.

## Verification (for the L1, after drafting)

- `python3 .ufo/waves/round-31/count-c1.py <lane-rev>` → expect `C1=met`; before the entry it is `entry=absent`.
- `rg -o 'S[0-9]{3}' corpus/knowledge/watchdog-identity-r31.md | sort -u` → every id must be a mori
  `corpus/SOURCES.md` row (no S060/S075/S086).
- `grep -c` each Gate quote against its `corpus/evidence/sources-r31/S###.src`, and `wc -w` ≤ 25 per quote.
- `sha256sum scripts/shokunin-watchdog.sh` → `04a3a2148efad2cd1be9bff2496cac520ab14597cab978eca241771226bb8d85`;
  `wc -c` → 17846. Re-read `:144` and `:227-236` at that sha before citing them.
- Re-run this scan's two decisive greps: `rg -l -i 'files.?opened|writer-forbidden' ../*/corpus/knowledge ../*/tools`
  (expect B1-B2 only) and `rg -n -i 'pgrep|proc_pid_stat|proc_pid_comm|proc_pid_cmdline' corpus/SOURCES.md`
  (expect no prior row).
- C2 remains the lane's own run: `bash tools/mori-blind-check.sh <lane-rev> .ufo/waves/round-31 <writer-regex>
  <allow-file>` against the frozen fixtures; this scan adds no C2 evidence.

## Tooling

No install or update was made; the directive's record requirement is satisfied with an empty row. Tools used:
`rg` (ripgrep), `grep`, `sed`, `sha256sum`, `wc`, `ls`.
