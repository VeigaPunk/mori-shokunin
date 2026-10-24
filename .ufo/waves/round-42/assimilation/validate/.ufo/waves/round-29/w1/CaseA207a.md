# Round 29 A2-07 blind cases — CaseA207a

## Cases

```json
[
  {
    "id": "r29-a2-07-dryrun-before-boundary",
    "rule": "A2-07",
    "author": "CaseA207a",
    "why": "A2-07 requires splitting at each version line so this earlier dry-run invocation does not suppress the later real send (round-27 contract.md:55; round-26 contract.md:180-181). The active invocation's version line is inside the nonzero scope, and its in-scope SIGTERM is positive evidence (round-26 contract.md:78-79, 93-98).",
    "inputs": {
      "earlyoom_show": "LoadState=loaded\nActiveState=active\nUnitFileState=enabled\nActiveEnterTimestampMonotonic=2000",
      "oomd_show": "LoadState=loaded\nActiveState=inactive\nUnitFileState=disabled\nActiveEnterTimestampMonotonic=0",
      "earlyoom_journal": [
        {"MESSAGE": "earlyoom 1.9.0", "__MONOTONIC_TIMESTAMP": "1000"},
        {"MESSAGE": "dryrun mode enabled, will not kill anything", "__MONOTONIC_TIMESTAMP": "1100"},
        {"MESSAGE": "earlyoom 1.9.0", "__MONOTONIC_TIMESTAMP": "2100"},
        {"MESSAGE": "sending SIGTERM to process 901 uid 1201 \"sample-worker\": oom_score 321, oom_score_adj 0, VmRSS 42 MiB, cmdline \"/usr/bin/sample-worker\"", "__MONOTONIC_TIMESTAMP": "2200"}
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
        "earlyoom.actions.sigkill": 0,
        "earlyoom.actions.escalations": 0,
        "earlyoom.actions.kill_failed": 0,
        "earlyoom.actions.low_memory_warnings": 0,
        "earlyoom.dryrun_send_lines": 0,
        "earlyoom.process_group_lines": 0,
        "earlyoom.earlier_invocation_send_lines": 0,
        "oomd.state": "inactive",
        "oomd.notices_this_boot": 0
      }
    }
  },
  {
    "id": "r29-a2-07-two-prior-invocations",
    "rule": "A2-07",
    "author": "CaseA207a",
    "why": "A2-07 applies dry-run state per invocation, and A2-06 separately counts sends outside the current invocation while leaving an active-unit verdict unchanged (round-27 contract.md:54-55; round-26 contract.md:175-181). The pre-boundary SIGKILL is outside scope; the current invocation's in-scope SIGTERM is positive evidence (round-26 contract.md:78-79, 85, 97-98).",
    "inputs": {
      "earlyoom_show": "LoadState=loaded\nActiveState=active\nUnitFileState=enabled\nActiveEnterTimestampMonotonic=4000",
      "oomd_show": "LoadState=loaded\nActiveState=inactive\nUnitFileState=disabled\nActiveEnterTimestampMonotonic=0",
      "earlyoom_journal": [
        {"MESSAGE": "earlyoom 1.9.0", "__MONOTONIC_TIMESTAMP": "1000"},
        {"MESSAGE": "dryrun mode enabled, will not kill anything", "__MONOTONIC_TIMESTAMP": "1100"},
        {"MESSAGE": "earlyoom 1.9.0", "__MONOTONIC_TIMESTAMP": "2000"},
        {"MESSAGE": "sending SIGKILL to process 902 uid 1202 \"sample-indexer\": oom_score 322, oom_score_adj 0, VmRSS 43 MiB, cmdline \"/usr/bin/sample-indexer\"", "__MONOTONIC_TIMESTAMP": "2100"},
        {"MESSAGE": "earlyoom 1.9.0", "__MONOTONIC_TIMESTAMP": "5000"},
        {"MESSAGE": "sending SIGTERM to process 903 uid 1203 \"sample-worker\": oom_score 323, oom_score_adj 0, VmRSS 44 MiB, cmdline \"/usr/bin/sample-worker\"", "__MONOTONIC_TIMESTAMP": "5100"}
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
        "earlyoom.actions.sigkill": 0,
        "earlyoom.actions.escalations": 0,
        "earlyoom.actions.kill_failed": 0,
        "earlyoom.actions.low_memory_warnings": 0,
        "earlyoom.dryrun_send_lines": 0,
        "earlyoom.process_group_lines": 0,
        "earlyoom.earlier_invocation_send_lines": 1,
        "oomd.state": "inactive",
        "oomd.notices_this_boot": 0
      }
    }
  },
  {
    "id": "r29-a2-07-dryrun-inside-scope",
    "rule": "A2-07",
    "author": "CaseA207a",
    "why": "The earlier real send precedes the bounded scope; inside it, a dry-run invocation is followed by a new real invocation. A2-07 requires the later invocation's real send to remain real; A2-06 reports the earlier send separately (round-27 contract.md:54-55; round-26 contract.md:78-79, 175-181). The in-scope SIGKILL is positive evidence (round-26 contract.md:85, 97-98).",
    "inputs": {
      "earlyoom_show": "LoadState=loaded\nActiveState=active\nUnitFileState=enabled\nActiveEnterTimestampMonotonic=3000",
      "oomd_show": "LoadState=loaded\nActiveState=inactive\nUnitFileState=disabled\nActiveEnterTimestampMonotonic=0",
      "earlyoom_journal": [
        {"MESSAGE": "earlyoom 1.9.0", "__MONOTONIC_TIMESTAMP": "1000"},
        {"MESSAGE": "sending SIGTERM to process 904 uid 1204 \"sample-renderer\": oom_score 324, oom_score_adj 0, VmRSS 45 MiB, cmdline \"/usr/bin/sample-renderer\"", "__MONOTONIC_TIMESTAMP": "1100"},
        {"MESSAGE": "earlyoom 1.9.0", "__MONOTONIC_TIMESTAMP": "3500"},
        {"MESSAGE": "dryrun mode enabled, will not kill anything", "__MONOTONIC_TIMESTAMP": "3600"},
        {"MESSAGE": "earlyoom 1.9.0", "__MONOTONIC_TIMESTAMP": "4000"},
        {"MESSAGE": "sending SIGKILL to process 905 uid 1205 \"sample-indexer\": oom_score 325, oom_score_adj 0, VmRSS 46 MiB, cmdline \"/usr/bin/sample-indexer\"", "__MONOTONIC_TIMESTAMP": "4100"}
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
        "earlyoom.actions.sigterm": 0,
        "earlyoom.actions.sigkill": 1,
        "earlyoom.actions.escalations": 0,
        "earlyoom.actions.kill_failed": 0,
        "earlyoom.actions.low_memory_warnings": 0,
        "earlyoom.dryrun_send_lines": 0,
        "earlyoom.process_group_lines": 0,
        "earlyoom.earlier_invocation_send_lines": 1,
        "oomd.state": "inactive",
        "oomd.notices_this_boot": 0
      }
    }
  }
]
```

## Per-case derivation tables

### `r29-a2-07-dryrun-before-boundary`

| Field | Value | Contract line(s) deciding it |
|---|---:|---|
| verdict | `KILLER_ACTED` | `round-26/contract.md:97-98` |
| exit | `1` | `round-26/contract.md:97-98` |
| earlyoom.state | `active` | `round-26/contract.md:90-101` |
| earlyoom.version | `1.9.0` | `round-26/contract.md:82, 90-95` |
| earlyoom.grammar | `verified-1.9.0` | `round-26/contract.md:80-82, 90-94` |
| earlyoom.scope_complete | `true` | `round-26/contract.md:78-79, 92-94` |
| earlyoom.actions.sigterm | `1` | `round-26/contract.md:85, 97-98` |
| earlyoom.actions.sigkill | `0` | `round-26/contract.md:78-79, 85` |
| earlyoom.actions.escalations | `0` | `round-26/contract.md:86, 90-94` |
| earlyoom.actions.kill_failed | `0` | `round-26/contract.md:87, 90-94` |
| earlyoom.actions.low_memory_warnings | `0` | `round-26/contract.md:88, 90-94` |
| earlyoom.dryrun_send_lines | `0` | `round-27/contract.md:52`; `round-26/contract.md:166-167` |
| earlyoom.process_group_lines | `0` | `round-27/contract.md:51`; `round-26/contract.md:164-165` |
| earlyoom.earlier_invocation_send_lines | `0` | `round-27/contract.md:54`; `round-26/contract.md:175-179` |
| oomd.state | `inactive` | `round-26/contract.md:90-95` |
| oomd.notices_this_boot | `0` | `round-26/contract.md:95, 97-98` |

### `r29-a2-07-two-prior-invocations`

| Field | Value | Contract line(s) deciding it |
|---|---:|---|
| verdict | `KILLER_ACTED` | `round-26/contract.md:97-98` |
| exit | `1` | `round-26/contract.md:97-98` |
| earlyoom.state | `active` | `round-26/contract.md:90-101` |
| earlyoom.version | `1.9.0` | `round-26/contract.md:82, 90-95` |
| earlyoom.grammar | `verified-1.9.0` | `round-26/contract.md:80-82, 90-94` |
| earlyoom.scope_complete | `true` | `round-26/contract.md:78-79, 92-94` |
| earlyoom.actions.sigterm | `1` | `round-26/contract.md:85, 97-98` |
| earlyoom.actions.sigkill | `0` | `round-26/contract.md:78-79, 85` |
| earlyoom.actions.escalations | `0` | `round-26/contract.md:86, 90-94` |
| earlyoom.actions.kill_failed | `0` | `round-26/contract.md:87, 90-94` |
| earlyoom.actions.low_memory_warnings | `0` | `round-26/contract.md:88, 90-94` |
| earlyoom.dryrun_send_lines | `0` | `round-27/contract.md:52`; `round-26/contract.md:166-167` |
| earlyoom.process_group_lines | `0` | `round-27/contract.md:51`; `round-26/contract.md:164-165` |
| earlyoom.earlier_invocation_send_lines | `1` | `round-27/contract.md:54`; `round-26/contract.md:175-179` |
| oomd.state | `inactive` | `round-26/contract.md:90-95` |
| oomd.notices_this_boot | `0` | `round-26/contract.md:95, 97-98` |

### `r29-a2-07-dryrun-inside-scope`

| Field | Value | Contract line(s) deciding it |
|---|---:|---|
| verdict | `KILLER_ACTED` | `round-26/contract.md:97-98` |
| exit | `1` | `round-26/contract.md:97-98` |
| earlyoom.state | `active` | `round-26/contract.md:90-101` |
| earlyoom.version | `1.9.0` | `round-26/contract.md:82, 90-95` |
| earlyoom.grammar | `verified-1.9.0` | `round-26/contract.md:80-82, 90-94` |
| earlyoom.scope_complete | `true` | `round-26/contract.md:78-79, 92-94` |
| earlyoom.actions.sigterm | `0` | `round-26/contract.md:78-79, 85` |
| earlyoom.actions.sigkill | `1` | `round-26/contract.md:85, 97-98` |
| earlyoom.actions.escalations | `0` | `round-26/contract.md:86, 90-94` |
| earlyoom.actions.kill_failed | `0` | `round-26/contract.md:87, 90-94` |
| earlyoom.actions.low_memory_warnings | `0` | `round-26/contract.md:88, 90-94` |
| earlyoom.dryrun_send_lines | `0` | `round-27/contract.md:52`; `round-26/contract.md:166-167` |
| earlyoom.process_group_lines | `0` | `round-27/contract.md:51`; `round-26/contract.md:164-165` |
| earlyoom.earlier_invocation_send_lines | `1` | `round-27/contract.md:54`; `round-26/contract.md:175-179` |
| oomd.state | `inactive` | `round-26/contract.md:90-95` |
| oomd.notices_this_boot | `0` | `round-26/contract.md:95, 97-98` |

Unpinned: `earlyoom.thresholds` has no threshold records, and the contract gives an object-or-null shape without specifying the absent-threshold result (`round-26/contract.md:83-84, 90-94`). `earlyoom.dryrun` is omitted because the contract names the output field but does not define its aggregation for mixed invocations; A2-04/A2-07 define send classification, not that field's representation (`round-26/contract.md:94, 166-167, 180-181`).

## Opened files and URLs

Local files requested:

- `skill://godspeed` (`/home/vgpnk/.agents/skills/godspeed/SKILL.md`).
- `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-27/contract.md:40-80`.
- `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-26/contract.md:1-190` (whole contract).
- `/home/vgpnk/Projects/shokunin/mori-shokunin/tools/fixtures/mori-oom-killers/cases.json` and `cases-a2.json`. I requested each whole file once, then `:1-5`; the reader collapsed case bodies and automatic context displayed a preview of initial case content. I did not use existing case values to draft these cases.
- `/fast/scratch/hyaku/mori-r29/CaseA207a/cases.json` (the new JSON, validated and read to prepare this report).
- Curl downloads under `/fast/scratch/hyaku/mori-r29/CaseA207a/sources/` for the five URLs below; each was hashed after fetching.

External sources fetched by `curl` at `2026-10-22T19:56:11Z` (UTC timestamp recorded immediately before each request):

| URL | SHA-256 | Quote(s), verbatim, with upstream line number |
|---|---|---|
| `https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/main.c` | `08656b0bc90c85f23738661456b25c97af908bc5e2cfea78e0a69697b5f9d0e4` | `main.c:161` `fprintf(stderr, "earlyoom " VERSION "\n");`; `main.c:295` `warn("dryrun mode enabled, will not kill anything\n");` |
| `https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/kill.c` | `b32e0fad65e298235102f98aff37e02c94400b544d454cb57192ae697b100bf3` | `kill.c:627` `sending %s to process` |
| `https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/msg.h` | `e36604984a916fb00a624c27c73034bcd87d7d6facff9b290a6a561ee58de56c` | No quote used. |
| `https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/MANPAGE.md` | `cc48b02e79255ae27bad9b2c49364fcae1b6b5eb20fe8e83ecef432f360dfeda` | No quote used. |
| `https://www.freedesktop.org/software/systemd/man/latest/systemd.journal-fields.html` | `906e5d34b38913ddaf729f74f468f5511f8a143bb3f86f0fdda06957af7bf5e7` | No quote used. |

Validation: `python3 -c 'import json; json.load(open("/fast/scratch/hyaku/mori-r29/CaseA207a/cases.json", encoding="utf-8")); print("python3 json.load: valid")'` printed `python3 json.load: valid`. No other tests were run. No tool was installed or updated.

I opened no `tools/mori-oom-killers.py`, no output from it, and no other report.
