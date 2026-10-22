# CaseA207c — A2-07 blind cases

## Cases

```json
[
  {
    "id": "r29-a2-07-dryrun-then-real-missing-enter",
    "rule": "A2-07",
    "author": "CaseA207c",
    "why": "A2-05 makes the missing ActiveEnterTimestampMonotonic leave scope_complete false (round-27/contract.md:53; round-26/contract.md:173-174). A2-07 splits the records at each version line, so the second invocation is real even though the first enabled dry-run (round-27/contract.md:55; round-26/contract.md:180-182). Its single SIGTERM send is in the current invocation, so earlyoom.actions.sigterm is 1; the current invocation has no dry-run sends and the earlier invocation has no send lines (A2-04/A2-06: round-27/contract.md:52,54). Other action counts are zero because no matching action grammar lines occur (round-26/contract.md:85-88,93-95). The real in-scope send is positive evidence despite incomplete scope, giving KILLER_ACTED/exit 1 (round-26/contract.md:97-101).",
    "inputs": {
      "earlyoom_show": "LoadState=loaded\nActiveState=active\nUnitFileState=enabled\n",
      "oomd_show": "LoadState=loaded\nActiveState=inactive\nUnitFileState=disabled\nActiveEnterTimestampMonotonic=0\n",
      "earlyoom_journal": [
        {"MESSAGE": "earlyoom 1.9.0", "__MONOTONIC_TIMESTAMP": "42000000"},
        {"MESSAGE": "dryrun mode enabled, will not kill anything", "__MONOTONIC_TIMESTAMP": "42000010"},
        {"MESSAGE": "earlyoom 1.9.0", "__MONOTONIC_TIMESTAMP": "43000000"},
        {"MESSAGE": "sending SIGTERM to process 6417 uid 417 \"cedar-wren\": oom_score 311, oom_score_adj 0, VmRSS 91 MiB, cmdline \"fixture-worker\"", "__MONOTONIC_TIMESTAMP": "43000010"}
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
        "earlyoom.scope_complete": false,
        "earlyoom.actions.sigterm": 1,
        "earlyoom.actions.sigkill": 0,
        "earlyoom.actions.escalations": 0,
        "earlyoom.actions.kill_failed": 0,
        "earlyoom.actions.low_memory_warnings": 0,
        "earlyoom.dryrun": false,
        "earlyoom.dryrun_send_lines": 0,
        "earlyoom.earlier_invocation_send_lines": 0,
        "oomd.state": "inactive",
        "oomd.notices_this_boot": 0
      }
    }
  },
  {
    "id": "r29-a2-07-real-then-dryrun-zero-enter",
    "rule": "A2-07",
    "author": "CaseA207c",
    "why": "A2-05 makes ActiveEnterTimestampMonotonic=0 leave the invocation unbounded and scope_complete false (round-27/contract.md:53; round-26/contract.md:173-174). The second version line starts a dry-run invocation: its one SIGTERM line is counted in earlyoom.dryrun_send_lines and leaves current sigterm/sigkill at zero, never positive evidence (round-27/contract.md:52,55; round-26/contract.md:166-167,180-182). The earlier real invocation's SIGTERM is one earlier_invocation_send_lines record (round-27/contract.md:54; round-26/contract.md:175-179); for active earlyoom that earlier count does not change the verdict. With no positive evidence in the incomplete current scope, the verdict is KILLERS_UNKNOWN/exit 2 (round-26/contract.md:99-101). Other action counts are zero because no matching lines occur (round-26/contract.md:85-88,93-95).",
    "inputs": {
      "earlyoom_show": "LoadState=loaded\nActiveState=active\nUnitFileState=enabled\nActiveEnterTimestampMonotonic=0\n",
      "oomd_show": "LoadState=loaded\nActiveState=inactive\nUnitFileState=disabled\nActiveEnterTimestampMonotonic=0\n",
      "earlyoom_journal": [
        {"MESSAGE": "earlyoom 1.9.0", "__MONOTONIC_TIMESTAMP": "52000000"},
        {"MESSAGE": "sending SIGTERM to process 7281 uid 526 \"violet-fern\": oom_score 287, oom_score_adj 0, VmRSS 73 MiB, cmdline \"fixture-worker\"", "__MONOTONIC_TIMESTAMP": "52000010"},
        {"MESSAGE": "earlyoom 1.9.0", "__MONOTONIC_TIMESTAMP": "53000000"},
        {"MESSAGE": "dryrun mode enabled, will not kill anything", "__MONOTONIC_TIMESTAMP": "53000010"},
        {"MESSAGE": "sending SIGTERM to process 7393 uid 638 \"amber-lark\": oom_score 302, oom_score_adj 0, VmRSS 88 MiB, cmdline \"fixture-worker\"", "__MONOTONIC_TIMESTAMP": "53000020"}
      ],
      "oomd_notices": 0
    },
    "expect": {
      "verdict": "KILLERS_UNKNOWN",
      "exit": 2,
      "fields": {
        "earlyoom.state": "active",
        "earlyoom.version": "1.9.0",
        "earlyoom.grammar": "verified-1.9.0",
        "earlyoom.scope_complete": false,
        "earlyoom.actions.sigterm": 0,
        "earlyoom.actions.sigkill": 0,
        "earlyoom.actions.escalations": 0,
        "earlyoom.actions.kill_failed": 0,
        "earlyoom.actions.low_memory_warnings": 0,
        "earlyoom.dryrun": true,
        "earlyoom.dryrun_send_lines": 1,
        "earlyoom.earlier_invocation_send_lines": 1,
        "oomd.state": "inactive",
        "oomd.notices_this_boot": 0
      }
    }
  },
  {
    "id": "r29-a2-07-real-dryrun-real-missing-enter",
    "rule": "A2-07",
    "author": "CaseA207c",
    "why": "A2-05 makes the missing ActiveEnterTimestampMonotonic leave scope_complete false (round-27/contract.md:53; round-26/contract.md:173-174). The three version-separated invocations are real, dry-run, then real; A2-07 makes the third invocation independent of the second invocation's dry-run flag (round-27/contract.md:55; round-26/contract.md:180-182). The third invocation's single SIGKILL line therefore gives earlyoom.actions.sigkill=1; the first invocation's one SIGTERM is an earlier send and the middle dry-run invocation has no sends (round-27/contract.md:54-55; round-26/contract.md:175-182). The real current send is positive evidence despite incomplete scope, giving KILLER_ACTED/exit 1 (round-26/contract.md:97-101). Other action counts are zero because no matching lines occur (round-26/contract.md:85-88,93-95).",
    "inputs": {
      "earlyoom_show": "LoadState=loaded\nActiveState=active\nUnitFileState=enabled\n",
      "oomd_show": "LoadState=loaded\nActiveState=inactive\nUnitFileState=disabled\nActiveEnterTimestampMonotonic=0\n",
      "earlyoom_journal": [
        {"MESSAGE": "earlyoom 1.9.0", "__MONOTONIC_TIMESTAMP": "62000000"},
        {"MESSAGE": "sending SIGTERM to process 8129 uid 749 \"silver-pine\": oom_score 334, oom_score_adj 0, VmRSS 96 MiB, cmdline \"fixture-worker\"", "__MONOTONIC_TIMESTAMP": "62000010"},
        {"MESSAGE": "earlyoom 1.9.0", "__MONOTONIC_TIMESTAMP": "63000000"},
        {"MESSAGE": "dryrun mode enabled, will not kill anything", "__MONOTONIC_TIMESTAMP": "63000010"},
        {"MESSAGE": "earlyoom 1.9.0", "__MONOTONIC_TIMESTAMP": "64000000"},
        {"MESSAGE": "sending SIGKILL to process 8231 uid 851 \"mossy-owl\": oom_score 907, oom_score_adj 0, VmRSS 107 MiB, cmdline \"fixture-worker\"", "__MONOTONIC_TIMESTAMP": "64000010"}
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
        "earlyoom.scope_complete": false,
        "earlyoom.actions.sigterm": 0,
        "earlyoom.actions.sigkill": 1,
        "earlyoom.actions.escalations": 0,
        "earlyoom.actions.kill_failed": 0,
        "earlyoom.actions.low_memory_warnings": 0,
        "earlyoom.dryrun": false,
        "earlyoom.dryrun_send_lines": 0,
        "earlyoom.earlier_invocation_send_lines": 1,
        "oomd.state": "inactive",
        "oomd.notices_this_boot": 0
      }
    }
  }
]
```

## Per-case derivation

### Case 1 — dry-run, then real; monotonic start missing

| field | value | contract line |
|---|---:|---|
| verdict / exit | KILLER_ACTED / 1 | round-26/contract.md:97-98 |
| earlyoom.state | active | round-27/contract.md:50; round-26/contract.md:90-95 |
| earlyoom.version | 1.9.0 | round-26/contract.md:80-83 |
| earlyoom.grammar | verified-1.9.0 | round-26/contract.md:80-95 |
| earlyoom.scope_complete | false | round-27/contract.md:53; round-26/contract.md:173-174 |
| earlyoom.actions.sigterm | 1 | round-27/contract.md:55; round-26/contract.md:85,97-98 |
| earlyoom.actions.sigkill | 0 | round-26/contract.md:85-95 |
| earlyoom.actions.escalations | 0 | round-26/contract.md:86-95 |
| earlyoom.actions.kill_failed | 0 | round-26/contract.md:87,93-95 |
| earlyoom.actions.low_memory_warnings | 0 | round-26/contract.md:88,93-95 |
| earlyoom.dryrun | false | round-27/contract.md:52,55; round-26/contract.md:166-167,180-182 |
| earlyoom.dryrun_send_lines | 0 | round-27/contract.md:52,55; round-26/contract.md:166-167,180-182 |
| earlyoom.earlier_invocation_send_lines | 0 | round-27/contract.md:54; round-26/contract.md:175-179 |
| oomd.state | inactive | round-26/contract.md:90-95 |
| oomd.notices_this_boot | 0 | round-26/contract.md:95,97-98 |

### Case 2 — real, then dry-run; monotonic start is zero

| field | value | contract line |
|---|---:|---|
| verdict / exit | KILLERS_UNKNOWN / 2 | round-26/contract.md:99-101 |
| earlyoom.state | active | round-27/contract.md:50; round-26/contract.md:90-95 |
| earlyoom.version | 1.9.0 | round-26/contract.md:80-83 |
| earlyoom.grammar | verified-1.9.0 | round-26/contract.md:80-95 |
| earlyoom.scope_complete | false | round-27/contract.md:53; round-26/contract.md:173-174 |
| earlyoom.actions.sigterm | 0 | round-27/contract.md:52,55; round-26/contract.md:166-167,180-182 |
| earlyoom.actions.sigkill | 0 | round-27/contract.md:52; round-26/contract.md:166-167 |
| earlyoom.actions.escalations | 0 | round-26/contract.md:86-95 |
| earlyoom.actions.kill_failed | 0 | round-26/contract.md:87,93-95 |
| earlyoom.actions.low_memory_warnings | 0 | round-26/contract.md:88,93-95 |
| earlyoom.dryrun | true | round-27/contract.md:52,55; round-26/contract.md:166-167,180-182 |
| earlyoom.dryrun_send_lines | 1 | round-27/contract.md:52,55; round-26/contract.md:166-167,180-182 |
| earlyoom.earlier_invocation_send_lines | 1 | round-27/contract.md:54; round-26/contract.md:175-179 |
| oomd.state | inactive | round-26/contract.md:90-95 |
| oomd.notices_this_boot | 0 | round-26/contract.md:95,97-98 |

### Case 3 — real, dry-run, real; monotonic start missing

| field | value | contract line |
|---|---:|---|
| verdict / exit | KILLER_ACTED / 1 | round-26/contract.md:97-98 |
| earlyoom.state | active | round-27/contract.md:50; round-26/contract.md:90-95 |
| earlyoom.version | 1.9.0 | round-26/contract.md:80-83 |
| earlyoom.grammar | verified-1.9.0 | round-26/contract.md:80-95 |
| earlyoom.scope_complete | false | round-27/contract.md:53; round-26/contract.md:173-174 |
| earlyoom.actions.sigterm | 0 | round-26/contract.md:85-95 |
| earlyoom.actions.sigkill | 1 | round-27/contract.md:55; round-26/contract.md:85,97-98 |
| earlyoom.actions.escalations | 0 | round-26/contract.md:86-95 |
| earlyoom.actions.kill_failed | 0 | round-26/contract.md:87,93-95 |
| earlyoom.actions.low_memory_warnings | 0 | round-26/contract.md:88,93-95 |
| earlyoom.dryrun | false | round-27/contract.md:52,55; round-26/contract.md:166-167,180-182 |
| earlyoom.dryrun_send_lines | 0 | round-27/contract.md:52,55; round-26/contract.md:166-167,180-182 |
| earlyoom.earlier_invocation_send_lines | 1 | round-27/contract.md:54; round-26/contract.md:175-179 |
| oomd.state | inactive | round-26/contract.md:90-95 |
| oomd.notices_this_boot | 0 | round-26/contract.md:95,97-98 |

## Validation and scope

- JSON validation: ran `python3 -c 'import json, pathlib; p=pathlib.Path("cases-a2-07-r29.json"); data=json.load(p.open(encoding="utf-8")); print(f"json.load OK: {len(data)} cases")'` in `/fast/scratch/hyaku/mori-r29/CaseA207c`; output: `json.load OK: 3 cases`.
- No builds, linters, formatters, self-tests, or implementation-tool runs were performed. No tools were installed or updated.
- Risk: the case expectations are contract-derived and were not checked against the prohibited implementation. No other blocker.

## Files and URLs opened

- `/home/vgpnk/.agents/skills/godspeed/SKILL.md` and `/home/vgpnk/.omp/agent/RULES.md` (required instructions).
- `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-27/contract.md:40-80`.
- `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-26/contract.md:78-190`.
- `/home/vgpnk/Projects/shokunin/mori-shokunin/tools/fixtures/mori-oom-killers/cases.json` and `cases-a2.json` (schema and journal record shapes only).
- Scratch downloads opened: `/fast/scratch/hyaku/mori-r29/CaseA207c/main.c`, `kill.c`, `msg.h`, `MANPAGE.md`, and `systemd.journal-fields.html`; validated JSON `/fast/scratch/hyaku/mori-r29/CaseA207c/cases-a2-07-r29.json`.

Fetched source evidence (UTC access time; SHA-256 of fetched bytes; quote with source line):

| URL | Accessed | SHA-256 | Quote |
|---|---|---|---|
| `https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/main.c` | 2026-10-22T19:55:49Z | `08656b0bc90c85f23738661456b25c97af908bc5e2cfea78e0a69697b5f9d0e4` | L161: `earlyoom `; L295: `dryrun mode enabled, will not kill anything` |
| `https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/kill.c` | 2026-10-22T19:55:49Z | `b32e0fad65e298235102f98aff37e02c94400b544d454cb57192ae697b100bf3` | L627: `sending %s to process %d uid %d` |
| `https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/msg.h` | 2026-10-22T19:55:49Z | `e36604984a916fb00a624c27c73034bcd87d7d6facff9b290a6a561ee58de56c` | L10: `#define PRIPCT "%5.2lf%%"` |
| `https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/MANPAGE.md` | 2026-10-22T19:55:49Z | `cc48b02e79255ae27bad9b2c49364fcae1b6b5eb20fe8e83ecef432f360dfeda` | L206: `dry run (do not kill any processes)` |
| `https://www.freedesktop.org/software/systemd/man/latest/systemd.journal-fields.html` | 2026-10-22T19:55:49Z | `906e5d34b38913ddaf729f74f468f5511f8a143bb3f86f0fdda06957af7bf5e7` | L207: `__MONOTONIC_TIMESTAMP=`; L210: `formatted as a decimal.` |

I did not open or run `tools/mori-oom-killers.py`, inspect any of its output, or open any other report.
