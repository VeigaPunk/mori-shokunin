# CaseA2r07 — blind case writer for rule A2-07 (round 28, C2)

Seat: `CaseA2r07` (executor, leaf). Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin`.
Rule under test: **A2-07** — "dry-run applies per invocation (split at each version line): one dry-run
invocation does not zero another invocation's real sends" (`/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-27/contract.md:55`).

Required pinned field (L1 amendment A1, `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-28/contract.md:94`):
`earlyoom.earlier_invocation_send_lines` with an integer value above 0. Two of the three cases below pin it at
`2`; the third deliberately leaves it unpinned and says why.

**Status: 3 cases written, JSON validated, not committed (the L1 assembles the ten seats' cases into
`tools/fixtures/mori-oom-killers/cases-a2.json`).**

## Files changed

- `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-28/w1/CaseA2r07.md` — this report (the only file
  written in the lane).
- Scratch only (outside the lane): `/fast/scratch/hyaku/mori-r28/CaseA2r07/cases-a2-r07.json` (the same JSON array,
  validated there), plus `up-kill.c`, `up-main.c`, `up-msg.h` fetched by curl.

## The cases (one fenced JSON array)

```json
[
  {
   "id": "a2-07-earlier-real-then-current-dryrun",
   "rule": "A2-07",
   "why": "A2-07 (round-27/contract.md:55): dry-run applies per invocation, split at each version line, so one dry-run invocation does not zero another invocation's real sends. This journal holds two invocations of earlyoom in the same boot: an earlier real one and the current dry-run one. The version line 'earlyoom 1.9.0' (main.c:161) is the first line of an invocation (round-26/contract.md:82), so the split falls at the two version lines. ActiveEnterTimestampMonotonic is 42000000 and the current version line is stamped exactly 42000000, so the current invocation's version line is inside the scope (round-26/contract.md:78, '>=' is inclusive; frozen case c03 pins the same inclusive boundary), while the earlier invocation lies entirely outside it. The earlier invocation is real: it logged no 'dryrun mode enabled' line, so by the per-invocation split of round-26/contract.md:180-182 its two 'sending ... to process' lines are real sends that the dry-run invocation does not zero. They are sends of this boot outside the current invocation, so they are counted by round-26/contract.md:175-179 as earlier_invocation_send_lines, which is 2 (send and escalation lines; here two send lines). The current invocation logged 'dryrun mode enabled' (main.c:295, round-26/contract.md:89), so its own send line goes to dryrun_send_lines, sigterm and sigkill stay 0, and it is never positive evidence (round-26/contract.md:166-167, round-27/contract.md:52): dryrun_send_lines is 1. The following line 'dryrun, not actually sending any signal' (kill.c:272) matches none of the grammar forms of round-26/contract.md:80-89 and is not counted. The verdict is KILLERS_QUIET exit 0: a dry-run send is never positive evidence (round-26/contract.md:166-167) and oomd notices are 0 (round-26/contract.md:97); the non-zero earlier_invocation_send_lines is reported but does not change the verdict for an active earlyoom (round-26/contract.md:178-179, round-27/contract.md:54, the same limit frozen case c02 pins). scope_complete is true because the current invocation's version line is in scope (round-26/contract.md:92-93) and the grammar is verified (round-26/contract.md:91; frozen cases c01 and c09). The process names are invented and no uid or command line is carried in the fixture. Not pinned: the count fields that would be zero here, because the contract text does not decide between a zero count and a null count for a field with no hits, and the output field earlyoom.dryrun, whose single value the contract does not fix for a boot that holds more than one invocation.",
   "inputs": {
    "earlyoom_show": "LoadState=loaded\nActiveState=active\nUnitFileState=enabled\nActiveEnterTimestampMonotonic=42000000\n",
    "oomd_show": "LoadState=loaded\nActiveState=inactive\nUnitFileState=disabled\nActiveEnterTimestampMonotonic=0\n",
    "earlyoom_journal": [
     {"MESSAGE": "earlyoom 1.9.0", "__MONOTONIC_TIMESTAMP": "30000000"},
     {"MESSAGE": "sending SIGTERM to process 61001 \"imaginary-kestrel\"", "__MONOTONIC_TIMESTAMP": "30005000"},
     {"MESSAGE": "sending SIGKILL to process 61002 \"imaginary-lantern\"", "__MONOTONIC_TIMESTAMP": "30010000"},
     {"MESSAGE": "earlyoom 1.9.0", "__MONOTONIC_TIMESTAMP": "42000000"},
     {"MESSAGE": "dryrun mode enabled, will not kill anything", "__MONOTONIC_TIMESTAMP": "42000001"},
     {"MESSAGE": "sending SIGTERM to process 61003 \"imaginary-mistral\"", "__MONOTONIC_TIMESTAMP": "42010000"},
     {"MESSAGE": "dryrun, not actually sending any signal", "__MONOTONIC_TIMESTAMP": "42010001"}
    ],
    "oomd_notices": 0
   },
   "expect": {
    "verdict": "KILLERS_QUIET",
    "exit": 0,
    "fields": {
     "earlyoom.state": "active",
     "earlyoom.version": "1.9.0",
     "earlyoom.grammar": "verified-1.9.0",
     "earlyoom.thresholds": null,
     "earlyoom.scope_complete": true,
     "earlyoom.actions.sigterm": 0,
     "earlyoom.actions.sigkill": 0,
     "earlyoom.actions.escalations": 0,
     "earlyoom.actions.kill_failed": 0,
     "earlyoom.actions.low_memory_warnings": 0,
     "earlyoom.dryrun": true,
     "earlyoom.dryrun_send_lines": 1,
     "earlyoom.earlier_invocation_send_lines": 2,
     "oomd.state": "inactive",
     "oomd.notices_this_boot": 0
    }
   }
  },
  {
   "id": "a2-07-earlier-dryrun-then-current-real",
   "rule": "A2-07",
   "why": "A2-07 (round-27/contract.md:55) read from the other side: a dry-run invocation earlier in the boot must not zero the real sends of the invocation in scope. The journal holds two invocations: the earlier one logged 'dryrun mode enabled' (main.c:295, round-26/contract.md:89) and never reached the memory limits, so it logged no send line at all; the current invocation logged 'earlyoom 1.9.0' (main.c:161) and then sent a real signal. ActiveEnterTimestampMonotonic is 52000000 and the current version line is stamped exactly 52000000, so the current invocation's version line is inside the scope (round-26/contract.md:78, inclusive; frozen case c03) and the earlier invocation lies entirely outside it. Because the dry-run flag belongs to the earlier invocation alone (round-26/contract.md:180-182), the current invocation's 'sending SIGTERM to process ' line is a real action: one action each (round-26/contract.md:85) and positive evidence, so the verdict is KILLER_ACTED exit 1 (round-26/contract.md:97). The escalation line 'escalating to SIGKILL after ' (kill.c:318, round-26/contract.md:86) is in scope, so it counts as one escalation and is positive evidence (round-26/contract.md:97). scope_complete is true because the current invocation's version line is in scope (round-26/contract.md:92-93) and the grammar is verified (round-26/contract.md:91; frozen cases c01 and c09). The oomd side is active and silent: oomd notices of 0 are not positive evidence (round-26/contract.md:97). Not pinned: the count fields that would be zero here, because the contract text does not decide between a zero count and a null count for a field with no hits; and the output field earlyoom.dryrun, because round-27/contract.md:55 fixes how the dry-run flag applies per invocation to send lines but does not say which invocation the single boolean field reports, and the two readings differ here since only an earlier invocation logged the dry-run line. Process names are invented and no uid or command line is carried.",
   "inputs": {
    "earlyoom_show": "LoadState=loaded\nActiveState=active\nUnitFileState=enabled\nActiveEnterTimestampMonotonic=52000000\n",
    "oomd_show": "LoadState=loaded\nActiveState=active\nUnitFileState=static\nActiveEnterTimestampMonotonic=12345678\n",
    "earlyoom_journal": [
     {"MESSAGE": "earlyoom 1.9.0", "__MONOTONIC_TIMESTAMP": "40000000"},
     {"MESSAGE": "dryrun mode enabled, will not kill anything", "__MONOTONIC_TIMESTAMP": "40000001"},
     {"MESSAGE": "earlyoom 1.9.0", "__MONOTONIC_TIMESTAMP": "52000000"},
     {"MESSAGE": "sending SIGTERM to process 62011 \"imaginary-tessellate\"", "__MONOTONIC_TIMESTAMP": "52010000"},
     {"MESSAGE": "escalating to SIGKILL after 3.250 seconds", "__MONOTONIC_TIMESTAMP": "52015000"}
    ],
    "oomd_notices": 0
   },
   "expect": {
    "verdict": "KILLER_ACTED",
    "exit": 1,
    "fields": {
     "earlyoom.state": "active",
     "earlyoom.version": "1.9.0",
     "earlyoom.grammar": "verified-1.9.0",
     "earlyoom.thresholds": null,
     "earlyoom.scope_complete": true,
     "earlyoom.actions.sigterm": 1,
     "earlyoom.actions.sigkill": 0,
     "earlyoom.actions.escalations": 1,
     "earlyoom.actions.kill_failed": 0,
     "earlyoom.actions.low_memory_warnings": 0,
     "oomd.state": "active",
     "oomd.notices_this_boot": 0
    }
   }
  },
  {
   "id": "a2-07-three-invocations-dryrun-in-the-middle",
   "rule": "A2-07",
   "why": "A2-07 (round-27/contract.md:55) with three invocations in one boot, so the split at each version line has to be made twice: the earliest invocation is real, the middle invocation is a dry-run that logged no send line, and the current invocation is real. The three version lines 'earlyoom 1.9.0' (main.c:161, round-26/contract.md:82) are the invocation boundaries. ActiveEnterTimestampMonotonic is 63000000 and the current version line is stamped exactly 63000000, so the current invocation's version line is inside the scope (round-26/contract.md:78, inclusive; frozen case c03) and both earlier invocations lie outside it. The earliest invocation is real, so its two 'sending ... to process' lines are real sends of this boot outside the current invocation and are counted by round-26/contract.md:175-179 as earlier_invocation_send_lines, which is 2: the dry-run flag of the middle invocation must not zero them (round-26/contract.md:180-182, round-27/contract.md:55). The current invocation is not a dry-run invocation, so its two send lines are real actions (round-26/contract.md:85), one SIGTERM and one SIGKILL. The current invocation's send lines are in scope, so they are positive evidence and the verdict is KILLER_ACTED exit 1 (round-26/contract.md:97). Every invocation printed the two limit lines (main.c:414 and main.c:416, round-26/contract.md:83-84) with the same values, so the thresholds block is the same whichever invocation the reader takes them from: term 10.0 and 10.0, kill 5.0 and 5.0 (round-26/contract.md:91-92; frozen case c01 pins the same numbers for the same texts, PRIPCT is '%5.2lf%%' at msg.h:10, so 5.00 renders with a pad space). scope_complete is true because the current invocation's version line is in scope (round-26/contract.md:92-93) and the grammar is verified (round-26/contract.md:91; frozen cases c01 and c09). No escalation, kill failed or low memory line is present, so those counts are 0 (round-26/contract.md:86-88), and the oomd side is inactive with no notices, which is not positive evidence (round-26/contract.md:97). Not pinned: the count fields that would be zero here, because the contract text does not decide between a zero count and a null count for a field with no hits; and the output field earlyoom.dryrun, because round-27/contract.md:55 fixes the per-invocation application of the dry-run flag to send lines but does not say which invocation the single boolean field reports, and here the dry-run invocation is not the current one. Process names are invented and no uid or command line is carried.",
   "inputs": {
    "earlyoom_show": "LoadState=loaded\nActiveState=active\nUnitFileState=enabled\nActiveEnterTimestampMonotonic=63000000\n",
    "oomd_show": "LoadState=loaded\nActiveState=inactive\nUnitFileState=disabled\nActiveEnterTimestampMonotonic=0\n",
    "earlyoom_journal": [
     {"MESSAGE": "earlyoom 1.9.0", "__MONOTONIC_TIMESTAMP": "50000000"},
     {"MESSAGE": "sending SIGTERM when mem avail <= 10.00% and swap free <= 10.00%,", "__MONOTONIC_TIMESTAMP": "50000000"},
     {"MESSAGE": "        SIGKILL when mem avail <=  5.00% and swap free <=  5.00%", "__MONOTONIC_TIMESTAMP": "50000000"},
     {"MESSAGE": "sending SIGTERM to process 63021 \"imaginary-pumice\"", "__MONOTONIC_TIMESTAMP": "50005000"},
     {"MESSAGE": "sending SIGTERM to process 63022 \"imaginary-pumice\"", "__MONOTONIC_TIMESTAMP": "50010000"},
     {"MESSAGE": "earlyoom 1.9.0", "__MONOTONIC_TIMESTAMP": "55000000"},
     {"MESSAGE": "dryrun mode enabled, will not kill anything", "__MONOTONIC_TIMESTAMP": "55000001"},
     {"MESSAGE": "sending SIGTERM when mem avail <= 10.00% and swap free <= 10.00%,", "__MONOTONIC_TIMESTAMP": "55000000"},
     {"MESSAGE": "        SIGKILL when mem avail <=  5.00% and swap free <=  5.00%", "__MONOTONIC_TIMESTAMP": "55000000"},
     {"MESSAGE": "earlyoom 1.9.0", "__MONOTONIC_TIMESTAMP": "63000000"},
     {"MESSAGE": "sending SIGTERM when mem avail <= 10.00% and swap free <= 10.00%,", "__MONOTONIC_TIMESTAMP": "63000000"},
     {"MESSAGE": "        SIGKILL when mem avail <=  5.00% and swap free <=  5.00%", "__MONOTONIC_TIMESTAMP": "63000000"},
     {"MESSAGE": "sending SIGTERM to process 63023 \"imaginary-quartzite\"", "__MONOTONIC_TIMESTAMP": "63010000"},
     {"MESSAGE": "sending SIGKILL to process 63024 \"imaginary-quartzite\"", "__MONOTONIC_TIMESTAMP": "63015000"}
    ],
    "oomd_notices": 0
   },
   "expect": {
    "verdict": "KILLER_ACTED",
    "exit": 1,
    "fields": {
     "earlyoom.state": "active",
     "earlyoom.version": "1.9.0",
     "earlyoom.grammar": "verified-1.9.0",
     "earlyoom.thresholds.term_mem_pct": 10.0,
     "earlyoom.thresholds.term_swap_pct": 10.0,
     "earlyoom.thresholds.kill_mem_pct": 5.0,
     "earlyoom.thresholds.kill_swap_pct": 5.0,
     "earlyoom.scope_complete": true,
     "earlyoom.actions.sigterm": 1,
     "earlyoom.actions.sigkill": 1,
     "earlyoom.actions.escalations": 0,
     "earlyoom.actions.kill_failed": 0,
     "earlyoom.actions.low_memory_warnings": 0,
     "earlyoom.earlier_invocation_send_lines": 2,
     "oomd.state": "inactive",
     "oomd.notices_this_boot": 0
    }
   }
  }
]
```

## Derivation table — case 1 `a2-07-earlier-real-then-current-dryrun`

| field | value | contract line that decides it |
|---|---|---|
| `earlyoom.earlier_invocation_send_lines` | 2 | r26 `contract.md:175-179` (send/escalation lines of this boot outside the current invocation are counted here) with `:180-182` (dry-run is per invocation, so the earlier *real* invocation's sends are not zeroed by the later dry-run invocation); rule text r27 `contract.md:55` |
| `earlyoom.dryrun_send_lines` | 1 | r26 `contract.md:166-167` (after `dryrun mode enabled`, send lines go to `dryrun_send_lines`); r27 `contract.md:52` |
| `earlyoom.actions.sigterm` | 0 | r26 `contract.md:166-167` (`sigterm`/`sigkill` stay 0 under dry-run) |
| `earlyoom.actions.sigkill` | 0 | r26 `contract.md:166-167` |
| `earlyoom.actions.escalations` | 0 | r26 `contract.md:86` (no `escalating to SIGKILL after ` line in the journal) |
| `earlyoom.actions.kill_failed` | 0 | r26 `contract.md:87` (no `kill failed: ` line) |
| `earlyoom.actions.low_memory_warnings` | 0 | r26 `contract.md:88` (no `low memory! at or below ...` line) |
| `earlyoom.dryrun` | true | r26 `contract.md:89` (the dry-run flag line is in the current invocation, `:78` scope) — the one field the two readings of a multi-invocation boot cannot differ on here, because the *current* invocation is the dry-run one |
| `earlyoom.state` | `active` | r26 `contract.md:90` (state list) with the `ActiveState=active` show text |
| `earlyoom.version` | `1.9.0` | r26 `contract.md:82` (version grammar line, `main.c:161`) |
| `earlyoom.grammar` | `verified-1.9.0` | r26 `contract.md:91`; frozen `cases.json` c01/c09 |
| `earlyoom.thresholds` | null | r26 `contract.md:91-92` (thresholds block or null) — no `sending SIGTERM when mem avail` / `SIGKILL when mem avail` line anywhere in this journal; frozen c19 pins `null` for the same shape |
| `earlyoom.scope_complete` | true | r26 `contract.md:92-93` (the version line of the current invocation is inside the scope `:78`, `>=` inclusive at exactly 42000000); frozen c03 |
| `oomd.state` | `inactive` | r26 `contract.md:95` with the `ActiveState=inactive` oomd show text; frozen c01 |
| `oomd.notices_this_boot` | 0 | r26 `contract.md:95` from `oomd_notices: 0` |
| `verdict` | `KILLERS_QUIET` | r26 `contract.md:97` (the only in-scope send line is a dry-run send, never positive evidence, `:166-167`; `oomd_notices` is 0) and `:178-179` (an active earlyoom reports a non-zero earlier count without a verdict change); frozen c02 |
| `exit` | 0 | r26 `contract.md:102-104` (KILLERS_QUIET) |

## Derivation table — case 2 `a2-07-earlier-dryrun-then-current-real`

| field | value | contract line that decides it |
|---|---|---|
| `earlyoom.actions.sigterm` | 1 | r26 `contract.md:85` (one action per `sending SIGTERM to process ` line) with `:180-182` (the earlier invocation's dry-run flag does not reach the current invocation's sends); rule text r27 `contract.md:55` |
| `earlyoom.actions.escalations` | 1 | r26 `contract.md:86` (one per `escalating to SIGKILL after ` line) |
| `earlyoom.actions.sigkill` | 0 | r26 `contract.md:85` (no `sending SIGKILL to process ` line in the journal) |
| `earlyoom.actions.kill_failed` | 0 | r26 `contract.md:87` |
| `earlyoom.actions.low_memory_warnings` | 0 | r26 `contract.md:88` |
| `earlyoom.state` | `active` | r26 `contract.md:90` |
| `earlyoom.version` | `1.9.0` | r26 `contract.md:82` |
| `earlyoom.grammar` | `verified-1.9.0` | r26 `contract.md:91`; frozen c01/c09 |
| `earlyoom.thresholds` | null | r26 `contract.md:91-92`; frozen c19 |
| `earlyoom.scope_complete` | true | r26 `contract.md:92-93` with `:78`; frozen c03 |
| `oomd.state` | `active` | r26 `contract.md:95` with the `ActiveState=active` oomd show text; frozen c10/c28 |
| `oomd.notices_this_boot` | 0 | r26 `contract.md:95` from `oomd_notices: 0` |
| `verdict` | `KILLER_ACTED` | r26 `contract.md:97` (an in-scope `sending SIG…to process` line and an in-scope escalation line are positive evidence) |
| `exit` | 1 | r26 `contract.md:97` |

Not pinned in this case: `earlyoom.earlier_invocation_send_lines` (the value would be 0 — no send or escalation
line of this boot lies outside the current invocation — but the contract text does not decide between a zero count
and a null count for a field with no hits, so the field is left unpinned); `earlyoom.dryrun_send_lines` (same
reason: the only dry-run invocation logged no send line); `earlyoom.dryrun` (the rule text fixes how the flag
applies per invocation to send lines, not which invocation the single boolean reports, and here the dry-run
invocation is not the current one).

## Derivation table — case 3 `a2-07-three-invocations-dryrun-in-the-middle`

| field | value | contract line that decides it |
|---|---|---|
| `earlyoom.earlier_invocation_send_lines` | 2 | r26 `contract.md:175-179` (the earliest invocation's two send lines are of this boot and outside the current invocation) with `:180-182` (the middle invocation's dry-run flag must not zero them); rule text r27 `contract.md:55` |
| `earlyoom.actions.sigterm` | 1 | r26 `contract.md:85` with `:180-182` |
| `earlyoom.actions.sigkill` | 1 | r26 `contract.md:85` with `:180-182` |
| `earlyoom.actions.escalations` | 0 | r26 `contract.md:86` |
| `earlyoom.actions.kill_failed` | 0 | r26 `contract.md:87` |
| `earlyoom.actions.low_memory_warnings` | 0 | r26 `contract.md:88` |
| `earlyoom.state` | `active` | r26 `contract.md:90` |
| `earlyoom.version` | `1.9.0` | r26 `contract.md:82` |
| `earlyoom.grammar` | `verified-1.9.0` | r26 `contract.md:91`; frozen c01/c09 |
| `earlyoom.thresholds.term_mem_pct` | 10.0 | r26 `contract.md:83` (term threshold grammar line, `main.c:414`) with `:91-92`; frozen c01 pins 10.0 for the same text |
| `earlyoom.thresholds.term_swap_pct` | 10.0 | r26 `contract.md:83`; frozen c01 |
| `earlyoom.thresholds.kill_mem_pct` | 5.0 | r26 `contract.md:84` (kill threshold grammar line, `main.c:416`) with `:91-92`; frozen c01 pins 5.0 for the same text |
| `earlyoom.thresholds.kill_swap_pct` | 5.0 | r26 `contract.md:84`; frozen c01 |
| `earlyoom.scope_complete` | true | r26 `contract.md:92-93` with `:78`; frozen c03 |
| `oomd.state` | `inactive` | r26 `contract.md:95`; frozen c01 |
| `oomd.notices_this_boot` | 0 | r26 `contract.md:95` from `oomd_notices: 0` |
| `verdict` | `KILLER_ACTED` | r26 `contract.md:97` (the current invocation's two in-scope send lines are positive evidence) |
| `exit` | 1 | r26 `contract.md:97` |

Not pinned in this case: `earlyoom.dryrun_send_lines` (the middle dry-run invocation logged no send line, so the
value would be 0 and the contract text does not decide zero vs null for an empty count) and `earlyoom.dryrun`
(the dry-run invocation is not the current one, so the two readings of the single boolean differ).

## Rule coverage and distinctness

- **A2-07 is exercised in both directions.** Case 1 has the dry-run invocation *last*: the earlier real
  invocation's two sends survive as `earlier_invocation_send_lines = 2` and the current invocation's dry-run send
  is counted separately in `dryrun_send_lines = 1`. Case 2 has the dry-run invocation *first*: the current real
  invocation's send is counted as a real action (`actions.sigterm = 1`) instead of being zeroed. Case 3 puts a
  dry-run invocation *between* two real ones, so the split must be made at three version lines.
- **Required field**: `earlyoom.earlier_invocation_send_lines` is pinned above 0 in cases 1 and 3 (value 2 each).
  Case 2 leaves it unpinned (the value would be 0 and its representation is not decided by the contract text).
- **Distinctness**: the three `inputs` objects differ in journal length (7, 5, 14 records), in invocation count
  (2, 2, 3), in which invocation is the dry-run one (last, first, middle), in the send/escalation mix, and in the
  oomd side (inactive, active, inactive). No case reuses a round-26 frozen case's journal.
- **Grammar coverage inside the cases**: version line (`:82`), term/kill threshold lines (`:83-84`), SIGTERM and
  SIGKILL send lines (`:85`), an escalation line (`:86`), the dry-run flag line (`:89`), and one deliberately
  out-of-grammar line (`dryrun, not actually sending any signal`, kill.c:272) that must not be counted.

## Blindness statement

**I did not open, grep, cat or run `tools/mori-oom-killers.py`, nor any copy of it.** I did not open
`.ufo/waves/round-26/evidence/`, `.ufo/waves/round-26/w1`, `.ufo/waves/round-26/w2`,
`.ufo/waves/round-27/w1` or `.ufo/waves/round-27/w2`. I ran no self-test and no tool of the lane.

### Files I opened

1. `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-27/contract.md` (lines 40-80 for the rule table,
   plus a grep for the A2 rows at lines 49-58).
2. `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-26/contract.md` (whole spec: interface, grammar,
   output and verdict lines 59-113; Amendment A2 lines 152-200).
3. `/home/vgpnk/Projects/shokunin/mori-shokunin/tools/fixtures/mori-oom-killers/cases.json` (schema and journal
   line shapes only).
4. `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-28/contract.md` (the claim contract and its
   amendments, for the required-field map).
5. `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-28/wave1-dispatch.json` (my own seat entry only).
6. `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-27/count-c2.sh` (the counter's shape, for the
   `rule` key and the `expect` shape).

### Upstream sources fetched (curl, public URLs)

- `https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/kill.c` — fetched 2026-10-22T17:58:49Z, sha256
  `b32e0fad65e298235102f98aff37e02c94400b544d454cb57192ae697b100bf3`. Lines used: 272 `warn("dryrun, not actually
  sending any signal\n");`, 318 `warn("escalating to SIGKILL after %.3f seconds\n", secs);`, 627
  `warn("sending %s to process %d uid %d \"%s": oom_score %d, oom_score_adj %d, VmRSS %lld MiB, cmdline "%s"\n",`.
- `https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/main.c` — fetched 2026-10-22T17:58:49Z, sha256
  `08656b0bc90c85f23738661456b25c97af908bc5e2cfea78e0a69697b5f9d0e4`. Lines used: 161
  `fprintf(stderr, "earlyoom " VERSION "\n");`, 295 `warn("dryrun mode enabled, will not kill anything\n");`,
  414 `fprintf(stderr, "sending SIGTERM when mem avail <= " PRIPCT " and swap free <= " PRIPCT ",\n",`, 416
  `fprintf(stderr, "        SIGKILL when mem avail <= " PRIPCT " and swap free <= " PRIPCT "\n",`.
- `https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/msg.h` — fetched 2026-10-22T17:58:49Z, sha256
  `e36604984a916fb00a624c27c73034bcd87d7d6facff9b290a6a561ee58de56c`. Line 10: `#define PRIPCT "%5.2lf%%"`.

## Risks and blockers

- **Zero-vs-null on the new count fields.** `dryrun_send_lines` and `earlier_invocation_send_lines` are named by
  the A2 rules but their output shape (0 vs null when empty) is not stated in the contract text I was allowed to
  read. I therefore pinned them only where the value is unambiguously non-zero. If the tool emits `null` rather
  than `0` for an empty count, the unpinned fields are unaffected; if the tool emits `0`, they would still be
  unaffected because the field is not asserted. The two fields I do assert (`dryrun_send_lines = 1` in case 1 and
  `earlier_invocation_send_lines = 2` in cases 1 and 3) are non-zero under every reading.
- **The `earlyoom.dryrun` boolean in a multi-invocation boot.** The contract text fixes the *application* of the
  dry-run flag per invocation to send lines (`:180-182`) but not which invocation the single boolean field reports.
  I pinned it only in case 1, where the current invocation is the dry-run one and both readings give `true`.
- **The tool's own choice of which invocation's threshold lines populate `earlyoom.thresholds`.** In case 3 all
  three invocations print identical limit lines, so the four threshold numbers are the same whichever invocation
  the reader takes them from.
- No blocker: the three cases are written, schema-checked and JSON-validated, and are ready to be merged into
  `tools/fixtures/mori-oom-killers/cases-a2.json` by the L1.

## Tooling

No tool was installed or upgraded by this seat. Used as found: `python3` 3.14.8 (JSON validation) and
`curl` 8.23.0 (upstream fetch). No `pacman`, `uv tool`, `npm` or `cargo` transaction was run.

## Validation performed

```
$ python3 -c 'import json,sys;json.load(sys.stdin)' < cases-a2-r07.json
JSON_OK
$ python3 <schema assertions>
ALL_OK   # ids unique and printable ASCII, rule == "A2-07", exit is an int (not a bool),
         # inputs keys == {earlyoom_show, oomd_show, earlyoom_journal, oomd_notices},
         # expect keys == {verdict, exit, fields}, journal records == {MESSAGE, __MONOTONIC_TIMESTAMP}
         # with numeric timestamps, the three inputs objects pairwise distinct
```

Cases: 3, ids `a2-07-earlier-real-then-current-dryrun`, `a2-07-earlier-dryrun-then-current-real`,
`a2-07-three-invocations-dryrun-in-the-middle`.
