# CriticDecisionVsKernelKill — round 27 wave 2

Scope: kernel versus earlyoom event routing only. Review target: landed entry and SKILL Round27 section. No lane edits except this report; no installs or updates. Axes: C1 depth, calibration, operational routing; privacy held by reporting counts and process classes only.

## Counterexample and observed evidence

The retained boot -1 contains BOTH earlyoom activity and a separate kernel OOM kill. An active earlyoom and a positive earlyoom count therefore cannot classify every kill in that boot as earlyoom.

Read-only capture on 2026-10-22, completed before `date -u +%FT%TZ` returned `2026-10-22T17:10:25Z`:

For each retained boot below, the requested summary counter was executed:

```sh
journalctl -k -b <n> -q --grep='^oom-kill:constraint=' -o json --output-fields=_BOOT_ID | wc -l
```

The executed loop suppressed journal stderr. These are observed retained-record counts, not a proof of journal completeness. No raw journal messages were printed into this report.

| Boot | Kernel OOM summaries | Kernel killed-process records | Kernel invocations | Unit oom-kill results | Earlyoom send records |
|---|---:|---:|---:|---:|---:|
| -5 | 0 | 0 | 0 | 0 | 0 |
| -4 | 0 | 0 | 0 | 0 | 0 |
| -3 | 0 | 0 | 0 | 0 | 0 |
| -2 | 0 | 0 | 0 | 0 | 0 |
| -1 | 1 | 1 | 1 | 1 | 39 |
| 0 | 0 | 0 | 0 | 0 | 0 |

Evidence: executed journal count loop, output `boot=-1 oomkill_summary=1 killed_process=1 invoked=1 unit_result_oomkill=1 earlyoom_send=39`; all other listed boots returned zeros. The extra columns used the kernel killed-process and invocation markers, the unit oom-kill result marker, and earlyoom-unit send markers, respectively. They are corroborating counts, not an identity join.

The kernel event at 2026-10-22T06:54:59Z killed one `other`-class process. This is already documented at `.ufo/waves/round-27/w1/ConnFleetSeatKillPath.md:81`. A memory-only classifying read independently returned victim class `other`, adjustment 200, and constraint state `CONSTRAINT_NONE`. This does not identify a fleet process or explain why earlyoom did not intervene. No such explanation is established here.

The earlyoom burst was at 06:15:59–06:16:05Z, not 06:54:59Z (`ConnFleetSeatKillPath.md:80-81`). These are distinct events. No seat/session identity can be joined from their class labels (`ConnFleetSeatKillPath.md:118-126`).

## Statement verdicts

### 1. Earlyoom send totals exclude the kernel event — holds

The entry explicitly titles Fact 5 as earlyoom signalling and reports 39 sends (`corpus/knowledge/oom-victim-selection-r27.md:123-139`). Its counter filters the earlyoom unit before matching the send grammar (`.ufo/waves/round-27/evidence/boot-send-classes.py:29-44`). The kernel event is not accidentally included in those 39. Do not change this to 40 sends or 12 other-class earlyoom sends.

Likewise, the earlyoom-specific SKILL ranking row is conditional on an earlyoom send (`SKILL.md:727`); it does not literally direct a kernel event through earlyoom's prefer/avoid scoring. No demonstrated reverse misclassification exists in that row.

Severity: none for the count or explicit conditional.

### 2. “Only the system journal tells earlyoom kills from kernel kills” — holds as a distinction, unsupported as executable routing

The entry states the distinction but omits the known kernel event and supplies no event-source decision row (`corpus/knowledge/oom-victim-selection-r27.md:141-163`). The SKILL section routes an earlyoom-to-omp observation but has no general first step that separates kernel evidence from earlyoom evidence (`SKILL.md:725-733`).

Counterexample: boot -1 satisfies the earlyoom activity branch while also containing the independent 06:54:59Z kernel event. [INFERENCE] A reader using only that table could stop at earlyoom activity and fail to consider the kernel event; the table does not require that mistake, but does not guard against it.

Severity: medium. Fixable depth/routing omission, not evidence that the existing 39-send count is false.

### 3. Python send implies session survival — unsupported

`SKILL.md:731` says “the seat's session survived unless it was also signalled.” A send to one process class proves neither survival nor ownership of another process. The same retained boot contains another killer, and the fleet records do not establish a session death cause (`ConnFleetSeatKillPath.md:118-126`; entry Fact 6 at `:143-152`). The observed kernel victim is `other`, so it does NOT establish that the kernel killed an omp session. It establishes why a positive earlyoom observation cannot close the event search.

Severity: high for the unsupported survival conclusion a reader could act on. The “at most one tool process ended” wording also assumes the victim was a fleet tool, despite that row's own ownership caveat. Correct to evidence about the selected process only; do not assert successful exit merely from a send.

## Smallest safe corrections — exact old to new

Paths below are relative to the lane. These are recommendations to the sole integration owner, not applied edits.

### A. Entry: replace the final Fact 6 bullet (`:151-152`)

Old:

```markdown
- Only the system journal tells earlyoom kills from kernel kills, and it names a process class, never a seat or a
  lane. Joining a send to a lane is a time-window inference, never an attribution.
```

New:

```markdown
- Separate the event sources before attributing a death: earlyoom-unit send records establish earlyoom signalling;
  kernel OOM summary and killed-process records establish kernel OOM activity. Both occurred in retained boot -1:
  39 earlyoom sends and one separate kernel kill of an `other`-class process at 2026-10-22T06:54:59Z. The retained
  kernel OOM summary counts for boots -5, -4, -3, -2, -1 and 0 were 0, 0, 0, 0, 1 and 0 at the wave-2 read.
  These are retained-record counts, not a completeness guarantee. The kernel event is not part of the 39 sends
  (wave-1 ConnFleetSeatKillPath; wave-2 CriticDecisionVsKernelKill). Neither event source identifies a seat or lane;
  joining a journal event to a lane by time window is inference, never attribution.
```

### B. Entry decision table: insert before the existing earlyoom ranking row (`:158`)

Old: no event-source row.

New:

```markdown
| a seat or lane died and the killer is unknown | check both journal event sources in the relevant boot and window: earlyoom-unit sends versus kernel OOM summaries and killed-process records; report each source separately | that earlyoom activity excludes a kernel kill, that kernel activity proves an earlyoom send, or that either class label identifies a seat or lane |
```

### C. SKILL: insert before the existing earlyoom ranking row (`:727`)

Old: no event-source row.

New:

```markdown
| a seat or lane died and the killer is unknown | check both journal event sources in the relevant boot and window: earlyoom-unit sends versus kernel OOM summaries and killed-process records; report each source separately | that earlyoom activity excludes a kernel kill, that kernel activity proves an earlyoom send, or that either class label identifies a seat or lane | `oom-victim-selection-r27.md` Fact 6 |
```

### D. SKILL: replace the python row (`:731`)

Old:

```markdown
| a `python`-class send in the same window as a dead seat | at most one tool process ended; the seat's session survived unless it was also signalled | that the process belonged to the fleet; an unrelated `python` reads the same | `oom-victim-selection-r27.md` Fact 5 |
```

New:

```markdown
| an earlyoom send to a `python`-class process in the same window as a dead seat | it establishes signalling of that selected process, not the session's survival or death; check separately for kernel OOM events and other earlyoom sends | that the process belonged to the fleet, that the signal proves exit, or that absence of an earlyoom send to the session excludes another cause | `oom-victim-selection-r27.md` Facts 5 and 6 |
```

### E. Entry closing summary: narrow the unsupported outcome (`:180-181`)

Old:

```markdown
systemd's code rather than guess it, and say why one earlyoom send to `omp` is a fleet-wide event while a `python`
send kills one tool process. The SKILL.md `Round27` decision table carries the routing.
```

New:

```markdown
systemd's code rather than guess it, and distinguish earlyoom signalling from kernel OOM activity without treating
process class as session identity or a send as proof of exit. The SKILL.md `Round27` decision table carries the routing.
```

## Boundary

No canonical judgment, admission, integration or lane modification was performed. No claim counter, build, test or retention gate was run. The journal reads above are the assigned investigation, not verification of a patch. The defects are locally repairable without changing C1's contract, counts or victim identities; judgment remains with the canonical Rust judge.
