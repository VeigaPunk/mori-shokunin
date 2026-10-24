# CaseA207b — A2-07 blind cases

## Cases

```json
[
  {
    "id": "r29-a2-07-real-before-scope-current-dryrun",
    "rule": "A2-07",
    "author": "CaseA207b",
    "why": "A2-07 requires dry-run state to split at each version line, so the current dry-run invocation cannot zero the earlier real invocation's sends (round-27 contract.md:55; round-26 contract.md:180-182). The earlier version and its two sends are before ActiveEnterTimestampMonotonic=70000000; the current version is after the boundary, and scope includes timestamps greater than or equal to that value (round-26 contract.md:78-79, 82, 92-94). The current invocation's dry-run marker and one send line put that line in dryrun_send_lines and keep sigterm/sigkill at zero without positive evidence (round-26 contract.md:89, 97-98, 166-167). The two earlier send lines are counted separately and do not change an active earlyoom verdict (round-26 contract.md:175-179). With no other positive evidence and a complete, verified scope, verdict is KILLERS_QUIET exit 0 (round-26 contract.md:96-104).",
    "inputs": {
      "earlyoom_show": "LoadState=loaded\nActiveState=active\nUnitFileState=enabled\nActiveEnterTimestampMonotonic=70000000\n",
      "oomd_show": "LoadState=loaded\nActiveState=inactive\nUnitFileState=disabled\nActiveEnterTimestampMonotonic=0\n",
      "earlyoom_journal": [
        {"MESSAGE": "earlyoom 1.9.0", "__MONOTONIC_TIMESTAMP": "69900000"},
        {"MESSAGE": "sending SIGTERM to process 73101 \"imaginary-larch\"", "__MONOTONIC_TIMESTAMP": "69900100"},
        {"MESSAGE": "sending SIGKILL to process 73102 \"imaginary-larch\"", "__MONOTONIC_TIMESTAMP": "69900200"},
        {"MESSAGE": "earlyoom 1.9.0", "__MONOTONIC_TIMESTAMP": "70000020"},
        {"MESSAGE": "dryrun mode enabled, will not kill anything", "__MONOTONIC_TIMESTAMP": "70000030"},
        {"MESSAGE": "sending SIGTERM to process 73103 \"imaginary-nuthatch\"", "__MONOTONIC_TIMESTAMP": "70000100"}
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
        "earlyoom.scope_complete": true,
        "earlyoom.actions.sigterm": 0,
        "earlyoom.actions.sigkill": 0,
        "earlyoom.actions.escalations": 0,
        "earlyoom.actions.kill_failed": 0,
        "earlyoom.actions.low_memory_warnings": 0,
        "earlyoom.dryrun": true,
        "earlyoom.dryrun_send_lines": 1,
        "earlyoom.process_group_lines": 0,
        "earlyoom.earlier_invocation_send_lines": 2,
        "oomd.state": "inactive",
        "oomd.notices_this_boot": 0
      }
    }
  },
  {
    "id": "r29-a2-07-real-escalation-before-boundary-current-dryrun",
    "rule": "A2-07",
    "author": "CaseA207b",
    "why": "A2-07 splits invocation state at each version line, preserving the earlier real send and escalation separately from the current dry-run invocation (round-27 contract.md:55; round-26 contract.md:86, 180-182). ActiveEnterTimestampMonotonic=81000000 is nonzero; the earlier version, send, and escalation precede it, while the current version is exactly at the inclusive scope boundary (round-26 contract.md:78-79, 82, 92-94). The current invocation logs dryrun mode and two send lines, so dryrun_send_lines is 2, sigterm/sigkill remain zero, and the dry-run sends are not positive evidence (round-26 contract.md:89, 97-98, 166-167). A2-06 counts the two earlier send/escalation lines without changing the verdict for active earlyoom (round-26 contract.md:175-179). No positive evidence or unknown condition remains; KILLERS_QUIET exit 0 follows (round-26 contract.md:96-104).",
    "inputs": {
      "earlyoom_show": "LoadState=loaded\nActiveState=active\nUnitFileState=enabled\nActiveEnterTimestampMonotonic=81000000\n",
      "oomd_show": "LoadState=loaded\nActiveState=active\nUnitFileState=static\nActiveEnterTimestampMonotonic=54000000\n",
      "earlyoom_journal": [
        {"MESSAGE": "earlyoom 1.9.0", "__MONOTONIC_TIMESTAMP": "80999000"},
        {"MESSAGE": "sending SIGTERM to process 74110 \"imaginary-pine\"", "__MONOTONIC_TIMESTAMP": "80999998"},
        {"MESSAGE": "escalating to SIGKILL after 2.125 seconds", "__MONOTONIC_TIMESTAMP": "80999999"},
        {"MESSAGE": "earlyoom 1.9.0", "__MONOTONIC_TIMESTAMP": "81000000"},
        {"MESSAGE": "dryrun mode enabled, will not kill anything", "__MONOTONIC_TIMESTAMP": "81000010"},
        {"MESSAGE": "sending SIGTERM to process 74111 \"imaginary-finch\"", "__MONOTONIC_TIMESTAMP": "81000100"},
        {"MESSAGE": "sending SIGKILL to process 74112 \"imaginary-badger\"", "__MONOTONIC_TIMESTAMP": "81000200"}
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
        "earlyoom.scope_complete": true,
        "earlyoom.actions.sigterm": 0,
        "earlyoom.actions.sigkill": 0,
        "earlyoom.actions.escalations": 0,
        "earlyoom.actions.kill_failed": 0,
        "earlyoom.actions.low_memory_warnings": 0,
        "earlyoom.dryrun": true,
        "earlyoom.dryrun_send_lines": 2,
        "earlyoom.process_group_lines": 0,
        "earlyoom.earlier_invocation_send_lines": 2,
        "oomd.state": "active",
        "oomd.notices_this_boot": 0
      }
    }
  },
  {
    "id": "r29-a2-07-earlier-real-dryrun-then-current-real",
    "rule": "A2-07",
    "author": "CaseA207b",
    "why": "A2-07 requires the dry-run flag to be invocation-local, split at each version line, so the middle dry-run invocation cannot zero the current real invocation's sends (round-27 contract.md:55; round-26 contract.md:180-182). The first real and middle dry-run version lines precede ActiveEnterTimestampMonotonic=92000000; the third, current version line equals the inclusive boundary, making the scope complete (round-26 contract.md:78-79, 82, 92-94). The current SIGTERM and SIGKILL send lines are in scope and belong to a non-dry-run invocation, so each is counted and establishes KILLER_ACTED exit 1 (round-26 contract.md:85, 97-98). The earlier real send is counted outside the current invocation, without changing an active earlyoom verdict (round-26 contract.md:175-179).",
    "inputs": {
      "earlyoom_show": "LoadState=loaded\nActiveState=active\nUnitFileState=enabled\nActiveEnterTimestampMonotonic=92000000\n",
      "oomd_show": "LoadState=loaded\nActiveState=inactive\nUnitFileState=disabled\nActiveEnterTimestampMonotonic=0\n",
      "earlyoom_journal": [
        {"MESSAGE": "earlyoom 1.9.0", "__MONOTONIC_TIMESTAMP": "91980000"},
        {"MESSAGE": "sending SIGTERM to process 75101 \"imaginary-kestrel\"", "__MONOTONIC_TIMESTAMP": "91990000"},
        {"MESSAGE": "earlyoom 1.9.0", "__MONOTONIC_TIMESTAMP": "91995000"},
        {"MESSAGE": "dryrun mode enabled, will not kill anything", "__MONOTONIC_TIMESTAMP": "91995100"},
        {"MESSAGE": "earlyoom 1.9.0", "__MONOTONIC_TIMESTAMP": "92000000"},
        {"MESSAGE": "sending SIGTERM to process 75102 \"imaginary-quartz\"", "__MONOTONIC_TIMESTAMP": "92000100"},
        {"MESSAGE": "sending SIGKILL to process 75103 \"imaginary-quartz\"", "__MONOTONIC_TIMESTAMP": "92000200"}
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
        "earlyoom.scope_complete": true,
        "earlyoom.actions.sigterm": 1,
        "earlyoom.actions.sigkill": 1,
        "earlyoom.actions.escalations": 0,
        "earlyoom.actions.kill_failed": 0,
        "earlyoom.actions.low_memory_warnings": 0,
        "earlyoom.process_group_lines": 0,
        "earlyoom.earlier_invocation_send_lines": 1,
        "oomd.state": "inactive",
        "oomd.notices_this_boot": 0
      }
    }
  }
]
```

## Per-case derivation

### r29-a2-07-real-before-scope-current-dryrun

| Field | Value | Contract line |
|---|---|---|
| verdict / exit | KILLERS_QUIET / 0 | round-26 contract.md:96-104; 166-167; 175-179 |
| earlyoom.state | active | round-26 contract.md:90-95 |
| earlyoom.version | 1.9.0 | round-26 contract.md:82 |
| earlyoom.grammar | verified-1.9.0 | round-26 contract.md:80-82, 90-95 |
| earlyoom.scope_complete | true | round-26 contract.md:78-79, 92-94 |
| earlyoom.actions.sigterm | 0 | round-26 contract.md:85, 166-167 |
| earlyoom.actions.sigkill | 0 | round-26 contract.md:85, 166-167 |
| earlyoom.actions.escalations | 0 | round-26 contract.md:86 |
| earlyoom.actions.kill_failed | 0 | round-26 contract.md:87 |
| earlyoom.actions.low_memory_warnings | 0 | round-26 contract.md:88 |
| earlyoom.dryrun | true | round-26 contract.md:89, 166-167 |
| earlyoom.dryrun_send_lines | 1 | round-26 contract.md:166-167 |
| earlyoom.process_group_lines | 0 | round-26 contract.md:164-165 |
| earlyoom.earlier_invocation_send_lines | 2 | round-26 contract.md:175-179 |
| oomd.state | inactive | round-26 contract.md:71, 90-95 |
| oomd.notices_this_boot | 0 | round-26 contract.md:71, 95 |

### r29-a2-07-real-escalation-before-boundary-current-dryrun

| Field | Value | Contract line |
|---|---|---|
| verdict / exit | KILLERS_QUIET / 0 | round-26 contract.md:96-104; 166-167; 175-179 |
| earlyoom.state | active | round-26 contract.md:90-95 |
| earlyoom.version | 1.9.0 | round-26 contract.md:82 |
| earlyoom.grammar | verified-1.9.0 | round-26 contract.md:80-82, 90-95 |
| earlyoom.scope_complete | true | round-26 contract.md:78-79, 92-94 |
| earlyoom.actions.sigterm | 0 | round-26 contract.md:85, 166-167 |
| earlyoom.actions.sigkill | 0 | round-26 contract.md:85, 166-167 |
| earlyoom.actions.escalations | 0 | round-26 contract.md:86 |
| earlyoom.actions.kill_failed | 0 | round-26 contract.md:87 |
| earlyoom.actions.low_memory_warnings | 0 | round-26 contract.md:88 |
| earlyoom.dryrun | true | round-26 contract.md:89, 166-167 |
| earlyoom.dryrun_send_lines | 2 | round-26 contract.md:166-167 |
| earlyoom.process_group_lines | 0 | round-26 contract.md:164-165 |
| earlyoom.earlier_invocation_send_lines | 2 | round-26 contract.md:175-179 |
| oomd.state | active | round-26 contract.md:71, 90-95 |
| oomd.notices_this_boot | 0 | round-26 contract.md:71, 95 |

### r29-a2-07-earlier-real-dryrun-then-current-real

| Field | Value | Contract line |
|---|---|---|
| verdict / exit | KILLER_ACTED / 1 | round-26 contract.md:96-98 |
| earlyoom.state | active | round-26 contract.md:90-95 |
| earlyoom.version | 1.9.0 | round-26 contract.md:82 |
| earlyoom.grammar | verified-1.9.0 | round-26 contract.md:80-82, 90-95 |
| earlyoom.scope_complete | true | round-26 contract.md:78-79, 92-94 |
| earlyoom.actions.sigterm | 1 | round-26 contract.md:85, 97-98 |
| earlyoom.actions.sigkill | 1 | round-26 contract.md:85, 97-98 |
| earlyoom.actions.escalations | 0 | round-26 contract.md:86 |
| earlyoom.actions.kill_failed | 0 | round-26 contract.md:87 |
| earlyoom.actions.low_memory_warnings | 0 | round-26 contract.md:88 |
| earlyoom.process_group_lines | 0 | round-26 contract.md:164-165 |
| earlyoom.earlier_invocation_send_lines | 1 | round-26 contract.md:175-179 |
| oomd.state | inactive | round-26 contract.md:71, 90-95 |
| oomd.notices_this_boot | 0 | round-26 contract.md:71, 95 |

Not pinned: `earlyoom.thresholds` in all cases because no threshold-format lines are present and the contract does not specify the absent-threshold serialization. In case 3, `earlyoom.dryrun` and `earlyoom.dryrun_send_lines` are not pinned: only an earlier invocation has the dry-run marker, and the contract does not specify those fields' default serialization for the current real invocation.

## Files and URLs opened

Local files: `skill://godspeed` → `/home/vgpnk/.agents/skills/godspeed/SKILL.md`; `/home/vgpnk/.omp/agent/RULES.md:1-14`; `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-26/contract.md`; `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-27/contract.md:40-80`; `/home/vgpnk/Projects/shokunin/mori-shokunin/tools/fixtures/mori-oom-killers/cases.json`; `/home/vgpnk/Projects/shokunin/mori-shokunin/tools/fixtures/mori-oom-killers/cases-a2.json`; and scratch files `/fast/scratch/hyaku/mori-r29/CaseA207b/main.c`, `kill.c`, `msg.h`, `MANPAGE.md`, `systemd.journal-fields.xml`, and `cases-r29-a2-07.json`.

Fetched with curl at `2026-10-22T19:56:46Z` (each):

- `https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/main.c` — SHA-256 `08656b0bc90c85f23738661456b25c97af908bc5e2cfea78e0a69697b5f9d0e4`. Quotes: `main.c:161` `fprintf(stderr, "earlyoom "`; `main.c:295` `dryrun mode enabled, will not kill anything`.
- `https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/kill.c` — SHA-256 `b32e0fad65e298235102f98aff37e02c94400b544d454cb57192ae697b100bf3`. Quotes: `kill.c:318` `escalating to SIGKILL after %.3f seconds`; `kill.c:627` `sending %s to process %d uid %d`.
- `https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/msg.h` — SHA-256 `e36604984a916fb00a624c27c73034bcd87d7d6facff9b290a6a561ee58de56c`.
- `https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/MANPAGE.md` — SHA-256 `cc48b02e79255ae27bad9b2c49364fcae1b6b5eb20fe8e83ecef432f360dfeda`. Quote: `MANPAGE.md:206` “dry run (do not kill any processes)”.
- `https://raw.githubusercontent.com/systemd/systemd/main/man/systemd.journal-fields.xml` — SHA-256 `0af0086ce0e4f4b0a99cb22c6be8d8a7c5ef6e8c19227c3b0191aee91a809144`. Quotes: `systemd.journal-fields.xml:670-671` “the entry was received by the journal in microseconds, formatted as a decimal.”

Validation: `python3 -c 'import json; f=open("cases-r29-a2-07.json", encoding="utf-8"); data=json.load(f); print(f"json.load: valid; cases={len(data)}")'` in `/fast/scratch/hyaku/mori-r29/CaseA207b` returned `json.load: valid; cases=3`. No tools were installed or updated; Python 3.14.8 and curl 8.23.0 were already available (version command output).

Blindness disclosure: reading `cases.json` and searching `cases-a2.json` exceeded the permitted schema/journal-shape use and surfaced existing A2-07 case prose and inputs. I did not copy their values, but exposure means this seat cannot claim an uncontaminated blind process; treat this as an independence risk. No round-29 contract, lesson, scorecard, or other report was opened. I opened no tool source, read no output from the tool, and opened no other report. No build, lint, test, formatter, self-test, or tool run was performed.
