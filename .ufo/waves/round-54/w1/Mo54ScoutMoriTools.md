# Mo54ScoutMoriTools — how the existing tools see a non-OOM kernel kill

Scope: read `tools/mori-oom-killers.py`, `tools/mori-census.sh`, `tools/mori-seat-terminal.py`,
`tools/mori-pressure.py` and SKILL.md's kill/OOM sections **at the data commit**
`78295c764093ff1f6cee08d7246679900bde7265` (all line numbers below are in that revision; the
working-tree SKILL.md has since grown an unpinned `## Round54` section — the pinned file ends at
line 1209 and has no memory-failure text at all). Question: what does each tool report for a
process killed by `SIGBUS`/`SIGKILL` from the memory-failure handler — silent, misattributed, or
`unknown`?

Baseline sweep: `grep -n 'memory_failure|HardwareCorrupted|SIGBUS|BUS_MCE|machine.check|hwpoison'`
over all four tools plus pinned SKILL.md → **zero hits** (exit 1). No instrument reads
`/sys/devices/system/node/*/memory_failure/*`, `HardwareCorrupted`, or the `ras` tracepoint; the
class is unmeasured everywhere except through generic journal fields.

## tools/mori-oom-killers.py — silent (with the wrong implied meaning)

Surveys only the two *userspace* killers: `earlyoom.service`/`systemd-oomd.service` units plus
earlyoom journal lines (EARLYOOM_UNIT/OOMD_UNIT, lines 59–61; message grammar lines 101–118 — all
`SIGKILL`/`SIGTERM`/threshold/escalation patterns from earlyoom's `kill.c`). A kernel
memory-failure kill emits none of these, so `acted` is false (lines 469–481) and the verdict is:

- `KILLERS_QUIET`, exit 0 (lines 68–70, 500–505; `EXIT_BY_VERDICT` maps QUIET→0) when every input
  read succeeds — **a quiet verdict after a real kernel kill**.
- `KILLERS_UNKNOWN` only when an input was missing (lines 483–498) — i.e. `unknown` reports the
  tool's own read gaps, never an unexplained kill.

Classification: **silent**, and quietly misleading — `KILLERS_QUIET` reads to an operator as
"nothing killed it", but the instrument's coverage ends at userspace killers. (Its own docstring
line 5 concedes the scope: "two userspace killers".)

## tools/mori-census.sh — misattributed or silent, never named

Kill classes are journal `MESSAGE_ID` classes plus two structured-field classes (IDs at lines
1074–1078; class loop 1396–1437). Per kill channel of a memory-failure event:

- **Kernel line.** `Memory failure:` lines have no `MESSAGE_ID`; `kernel_oom_notice`
  (`fe6faa94…`, line 1074) stays 0. The retired `kernel_victim_text`/`gpf_text` text heuristics
  stay unmeasured by design (`JOURNAL_CLASSES_UNMEASURED`, line 1377).
- **`memory.events oom_kill`.** The cgroup probe counts only the OOM-path counter
  (`oom_kill=$(cgroup_field "$CGROUP_EVENTS" oom_kill)`, line 1690; `CGROUP_OOM_KILL` at 1844).
  A memory-failure SIGKILL never increments it — the counter stays a true 0, and per pinned
  SKILL.md line 30's own rule it means only "no *kernel OOM* kills".
- **User unit killed by SIGBUS, no coredump.** systemd emits a `d9b373ed…` unit-failure record
  with `UNIT_RESULT=signal` → counted in the `signal` subset (jq `def sig`, line 1138;
  JOURNAL_JQ_POS_UNIT, 1097) → the generic `KILL_SIGNAL_JOURNAL warn` fires (line 1630) with
  `attribution=none` and a note naming only OOM as a possible cause. **Present but misattributed**:
  indistinguishable from any other signal death.
- **User unit killed by SIGBUS *with* a coredump.** systemd result is `core-dump`, not `signal` →
  misses the signal subset; the coredump notice (`fc2e22bc…`) counts, but the only structured
  signal class is `segfault_signal11` — hard-filtered `COREDUMP_SIGNAL=11` (lines 1084, 1406).
  SIGBUS is signal 7 → falls into `other_signals`, explicitly
  `structured-field-unimplemented` (line 1377). **Silent** beyond one unattributed notice/record.
- **Memory-failure SIGKILL (unmap failure, `kill_procs`).** `98e32220…` +
  `EXIT_CODE=killed`/`EXIT_STATUS=9` → counted as `unit_sigkill_record` /
  `positive_process_sigkill` (jq at 1096; positive at 1464's own note: "cause unknown (a kernel
  OOM can also deliver SIGKILL)"). **Misattribution-prone**: the only cause hint the line offers
  is OOM.
- **System scope.** `unit_sigkill_record` findings are user-only (continue at 1450); a system-unit
  victim is a bare `d9b373ed` record — counted, routed fleet/nonfleet by name token, no warn.

`absent_records=possible:no-retained-record-is-not-no-event` (1377) is honest about coverage, but
nothing in the census looks at the counters that *would* show the event
(`/sys/.../memory_failure/*`, `HardwareCorrupted`).

## tools/mori-seat-terminal.py — silent at the finding level

Classes (lines 118–127): `completed, aborted, dead_rate_limit, dead_quota, dead_error_other,
incomplete, unavailable, error_unsettled`. `dead_*` is reachable **only** when the transcript's
terminal record carries `stop_reason == "error"` (line 773) — i.e. an LLM API error, with Z.AI
business-code refinement (783–799). A seat process SIGBUS-killed mid-session writes no terminal
record: the last record is a mid-turn assistant/tool-use message → `incomplete` (773–774) or
`unavailable` with a metadata reason (`schema|no-message|unreadable|terminal-time`, lines
201–204). `dead = any(record["class"].startswith("dead_"))` (1105) → finding stays
`MORI_SEAT_TERMINAL_OK` (113) and **exit is 0** (docstring 81–82). A kernel-killed seat is
**invisible** to this tool — same class as a session still running. (No staleness check on
`incomplete`; the settle window applies only to errors, 779–781.)

## tools/mori-pressure.py — silent

Reads only `/proc/pressure/{cpu,memory,io,irq}` PSI stall files (docstring lines 12–15;
threshold at 346 → `PRESSURE_HIGH`; 344 → `PRESSURE_UNAVAILABLE`; 350 → `PRESSURE_OK`).
Hardware poison produces no PSI stalls; memory pressure and memory failure are disjoint events.
Verdict is `PRESSURE_OK`/exit 0 during and after a SIGBUS kill — correct for its own question,
**silent** on kills.

## Host read (read-only, 2026-10-27, kernel 7.2.11-arch1-1)

The surfaces the new entry names exist here and read zero — consistent with no event since boot:

```
/sys/devices/system/node/node0/memory_failure/{total,ignored,failed,delayed,recovered} = 0 0 0 0 0
HardwareCorrupted:     0 kB
/proc/sys/vm/memory_failure_recovery = 1 ; /proc/sys/vm/memory_failure_early_kill = 0
/proc/sys/vm/panic_on_unrecoverable_memory_failure → absent (v7.3 sysctl; exit 2 on ls)
```

So today's tools are unexercised by a real event, and — per the contract's named limit — every
kill line/counter above is read from v7.3 source, not observed firing.

## Proposed SKILL.md error-pattern row (fenced draft; pinned table is `## Error patterns`,
## `| Observation | Reading |`, lines 25–45 — L1 chooses final placement; the working tree's new
## `### Error patterns (memory-failure kills)` bullet list already covers adjacent ground)

```
| a process died with no OOM record (`memory.events oom_kill`=0, `OOM_KILL_JOURNAL` quiet, oomd/earlyoom quiet, seat transcript `incomplete`) | do not call it unexplained yet: the kernel's memory-failure handler kills outside the OOM path — SIGBUS (`BUS_MCEERR_AR`/`BUS_MCEERR_AO`) or SIGKILL on unmap failure (S521 `kill_proc`/`kill_procs`) — and leaves its own evidence, not OOM evidence; read `/sys/devices/system/node/node*/memory_failure/{total,ignored,failed,delayed,recovered}` and `HardwareCorrupted` in `/proc/meminfo` first — both unread by any probe today; then attribute from the `Memory failure:` kernel lines as text (attribution only, never a count — QUALITY 15). A SIGBUS victim reaches the census only as generic `UNIT_RESULT=signal` (warn is `attribution=none`) or an unattributed `fc2e22bc…` coredump — `segfault_signal11` counts signal 11 only and SIGBUS is 7; `segfault`'s sibling signals sit in `other_signals` (`structured-field-unimplemented`); a `d9b373ed` + `EXIT_STATUS=9` memory-failure SIGKILL is indistinguishable from a kernel-OOM SIGKILL — `corpus/knowledge/memory-failure-kills-r54.md` |
```

## Findings

- **HIGH** — `tools/mori-oom-killers.py:68-70,469-505` + `tools/mori-seat-terminal.py:773,1105`:
  a memory-failure kill is *invisible at the verdict layer*: `KILLERS_QUIET` exit 0 and
  `MORI_SEAT_TERMINAL_OK` exit 0 after a real kernel kill. An operator reading "quiet + OK"
  has no hint a second kill source exists.
- **HIGH** — `tools/mori-census.sh:1630,1464`: the only positive signals a memory-failure kill
  can raise (`KILL_SIGNAL_JOURNAL warn`, `unit_sigkill_record` info) are emitted with
  `attribution=none` and a cause note that names *only* "a kernel OOM" — actively steering the
  reader toward the wrong cause; `oom_kill=0` then "confirms" it (SKILL.md.at78295:30 names only
  userspace killers as the excluded class).
- **MED** — `tools/mori-census.sh:1084,1406,1377`: `segfault_signal11` hard-codes
  `COREDUMP_SIGNAL=11`; SIGBUS (7) is structurally out of scope (`other_signals` unimplemented)
  and a coredumped SIGBUS victim leaves only an unattributed `fc2e22bc…` record.
- **MED** — no instrument reads `/sys/devices/system/node/*/memory_failure/*` or
  `HardwareCorrupted` (meminfo probe reads `MemTotal`/`MemAvailable` only,
  mori-census.sh:1791-1792): the kernel's own structured counters for this kill class are
  unmeasured — routed item for round 55, not a counter change this round.
- **LOW** — `mori-seat-terminal.py:773-781`: `incomplete`/`unavailable` carry no age test, so a
  killed seat is indistinguishable from a still-running one indefinitely.
- **LOW** — host: all memory_failure counters 0, `HardwareCorrupted: 0 kB`,
  `panic_on_unrecoverable_memory_failure` absent on 7.2.11 — unexercised path; source-read only.
