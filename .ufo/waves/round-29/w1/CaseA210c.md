# CaseA210c — A2-10 blind cases

## Cases

```json
[
  {
    "id": "r29-a2-10-inactive-lone-missing-stamp",
    "rule": "A2-10",
    "author": "CaseA210c",
    "why": "Round-26 contract.md:186-187 says a journal record without a numeric __MONOTONIC_TIMESTAMP is left uncounted and makes scope incomplete. Lines 102-104 make inactive earlyoom actions null and quiet/exit 0 the result without positive evidence. Lines 175-179 decide the zero earlier-invocation send count; round-27 contract.md:51-52 decide the zero process-group and dry-run send counters because neither message occurs. Round-26 lines 82 and 90-95 decide version and grammar; lines 90-98 decide oomd notices_this_boot from the supplied zero count.",
    "inputs": {
      "earlyoom_show": "LoadState=loaded\nActiveState=inactive\nUnitFileState=disabled\nActiveEnterTimestampMonotonic=4100000",
      "oomd_show": "LoadState=loaded\nActiveState=inactive\nUnitFileState=disabled\nActiveEnterTimestampMonotonic=0",
      "earlyoom_journal": [
        {
          "MESSAGE": "earlyoom 1.9.0",
          "__MONOTONIC_TIMESTAMP": "4100000"
        },
        {
          "MESSAGE": "sending SIGTERM to process 8101 uid 8101 \"fixture-inactive-worker\": oom_score 900, oom_score_adj 0, VmRSS 12 MiB, cmdline \"fixture-inactive-worker --a2-10\""
        }
      ],
      "oomd_notices": 0
    },
    "expect": {
      "verdict": "KILLERS_QUIET",
      "exit": 0,
      "fields": {
        "earlyoom.state": "inactive",
        "earlyoom.version": "1.9.0",
        "earlyoom.grammar": "verified-1.9.0",
        "earlyoom.scope_complete": false,
        "earlyoom.actions": null,
        "earlyoom.earlier_invocation_send_lines": 0,
        "earlyoom.dryrun_send_lines": 0,
        "earlyoom.process_group_lines": 0,
        "oomd.notices_this_boot": 0
      }
    }
  },
  {
    "id": "r29-a2-10-failed-stamped-positive",
    "rule": "A2-10",
    "author": "CaseA210c",
    "why": "Round-26 contract.md:186-187 says the nonnumeric timestamp record is left uncounted and makes scope incomplete. Lines 162-163 map failed to unavailable. Lines 97-100 say a stamped in-scope send is positive evidence despite incomplete scope, deciding KILLER_ACTED/exit 1. Lines 175-179 decide the zero earlier-invocation send count; round-27 contract.md:51-52 decide the zero process-group and dry-run send counters because neither message occurs. Round-26 lines 82 and 90-95 decide version and grammar; lines 90-98 decide oomd notices_this_boot from the supplied zero count.",
    "inputs": {
      "earlyoom_show": "LoadState=loaded\nActiveState=failed\nUnitFileState=disabled\nActiveEnterTimestampMonotonic=5200000",
      "oomd_show": "LoadState=loaded\nActiveState=inactive\nUnitFileState=disabled\nActiveEnterTimestampMonotonic=0",
      "earlyoom_journal": [
        {
          "MESSAGE": "earlyoom 1.9.0",
          "__MONOTONIC_TIMESTAMP": "5200000"
        },
        {
          "MESSAGE": "sending SIGTERM to process 8122 uid 8122 \"fixture-failed-worker\": oom_score 900, oom_score_adj 0, VmRSS 16 MiB, cmdline \"fixture-failed-worker --a2-10\"",
          "__MONOTONIC_TIMESTAMP": "5200001"
        },
        {
          "MESSAGE": "sending SIGKILL to process 8123 uid 8123 \"fixture-unclocked-worker\": oom_score 900, oom_score_adj 0, VmRSS 20 MiB, cmdline \"fixture-unclocked-worker --a2-10\"",
          "__MONOTONIC_TIMESTAMP": "not-a-number"
        }
      ],
      "oomd_notices": 0
    },
    "expect": {
      "verdict": "KILLER_ACTED",
      "exit": 1,
      "fields": {
        "earlyoom.state": "unavailable",
        "earlyoom.version": "1.9.0",
        "earlyoom.grammar": "verified-1.9.0",
        "earlyoom.scope_complete": false,
        "earlyoom.earlier_invocation_send_lines": 0,
        "earlyoom.dryrun_send_lines": 0,
        "earlyoom.process_group_lines": 0,
        "oomd.notices_this_boot": 0
      }
    }
  },
  {
    "id": "r29-a2-10-not-found-earlier-stamped-positive",
    "rule": "A2-10",
    "author": "CaseA210c",
    "why": "Round-26 contract.md:186-187 says the nonnumeric timestamp record is left uncounted and makes scope incomplete. Lines 175-179 count the stamped send before ActiveEnterTimestampMonotonic as an earlier-invocation send and positive evidence for a non-active killer; lines 180-183 also make not-found send lines this boot positive. Lines 90-95 and 180-183 decide absent state, lines 102-104 make absent actions null, lines 97-98 decide KILLER_ACTED/exit 1, and lines 82 and 90-95 decide the version and grammar. Round-27 lines 51-52 decide the zero process-group and dry-run send counters because neither message occurs.",
    "inputs": {
      "earlyoom_show": "LoadState=not-found\nActiveState=inactive\nUnitFileState=not-found\nActiveEnterTimestampMonotonic=6300000",
      "oomd_show": "LoadState=loaded\nActiveState=inactive\nUnitFileState=disabled\nActiveEnterTimestampMonotonic=0",
      "earlyoom_journal": [
        {
          "MESSAGE": "sending SIGTERM to process 8301 uid 8301 \"fixture-removed-worker\": oom_score 900, oom_score_adj 0, VmRSS 24 MiB, cmdline \"fixture-removed-worker --a2-10\"",
          "__MONOTONIC_TIMESTAMP": "6299000"
        },
        {
          "MESSAGE": "earlyoom 1.9.0",
          "__MONOTONIC_TIMESTAMP": "6300000"
        },
        {
          "MESSAGE": "sending SIGKILL to process 8302 uid 8302 \"fixture-unclocked-removed-worker\": oom_score 900, oom_score_adj 0, VmRSS 28 MiB, cmdline \"fixture-unclocked-removed-worker --a2-10\"",
          "__MONOTONIC_TIMESTAMP": "unknown"
        }
      ],
      "oomd_notices": 0
    },
    "expect": {
      "verdict": "KILLER_ACTED",
      "exit": 1,
      "fields": {
        "earlyoom.state": "absent",
        "earlyoom.version": "1.9.0",
        "earlyoom.grammar": "verified-1.9.0",
        "earlyoom.scope_complete": false,
        "earlyoom.actions": null,
        "earlyoom.earlier_invocation_send_lines": 1,
        "earlyoom.dryrun_send_lines": 0,
        "earlyoom.process_group_lines": 0,
        "oomd.notices_this_boot": 0
      }
    }
  }
]
```

## Per-case derivation

### `r29-a2-10-inactive-lone-missing-stamp`

| Field | Value | Contract line |
|---|---|---|
| `verdict` | `KILLERS_QUIET` | round-26 contract.md:97-104 |
| `exit` | `0` | round-26 contract.md:102-104 |
| `earlyoom.state` | `inactive` | round-26 contract.md:90-95, 162-163 |
| `earlyoom.version` | `1.9.0` | round-26 contract.md:82, 90-95 |
| `earlyoom.grammar` | `verified-1.9.0` | round-26 contract.md:80-82, 90-95 |
| `earlyoom.scope_complete` | `false` | round-26 contract.md:186-187 |
| `earlyoom.actions` | `null` | round-26 contract.md:102-104 |
| `earlyoom.earlier_invocation_send_lines` | `0` | round-26 contract.md:175-179, 186-187 |
| `earlyoom.dryrun_send_lines` | `0` | round-27 contract.md:52; round-26 contract.md:166-167 |
| `earlyoom.process_group_lines` | `0` | round-27 contract.md:51; round-26 contract.md:164-165 |
| `oomd.notices_this_boot` | `0` | round-26 contract.md:95-98 |

### `r29-a2-10-failed-stamped-positive`

| Field | Value | Contract line |
|---|---|---|
| `verdict` | `KILLER_ACTED` | round-26 contract.md:97-100, 186-187 |
| `exit` | `1` | round-26 contract.md:97-100 |
| `earlyoom.state` | `unavailable` | round-26 contract.md:162-163 |
| `earlyoom.version` | `1.9.0` | round-26 contract.md:82, 90-95 |
| `earlyoom.grammar` | `verified-1.9.0` | round-26 contract.md:80-82, 90-95 |
| `earlyoom.scope_complete` | `false` | round-26 contract.md:186-187 |
| `earlyoom.earlier_invocation_send_lines` | `0` | round-26 contract.md:175-179, 186-187 |
| `earlyoom.dryrun_send_lines` | `0` | round-27 contract.md:52; round-26 contract.md:166-167 |
| `earlyoom.process_group_lines` | `0` | round-27 contract.md:51; round-26 contract.md:164-165 |
| `oomd.notices_this_boot` | `0` | round-26 contract.md:95-98 |

### `r29-a2-10-not-found-earlier-stamped-positive`

| Field | Value | Contract line |
|---|---|---|
| `verdict` | `KILLER_ACTED` | round-26 contract.md:97-98, 175-183 |
| `exit` | `1` | round-26 contract.md:97-98, 175-183 |
| `earlyoom.state` | `absent` | round-26 contract.md:90-95, 180-183 |
| `earlyoom.version` | `1.9.0` | round-26 contract.md:82, 90-95 |
| `earlyoom.grammar` | `verified-1.9.0` | round-26 contract.md:80-82, 90-95 |
| `earlyoom.scope_complete` | `false` | round-26 contract.md:186-187 |
| `earlyoom.actions` | `null` | round-26 contract.md:102-104 |
| `earlyoom.earlier_invocation_send_lines` | `1` | round-26 contract.md:175-179 |
| `earlyoom.dryrun_send_lines` | `0` | round-27 contract.md:52; round-26 contract.md:166-167 |
| `earlyoom.process_group_lines` | `0` | round-27 contract.md:51; round-26 contract.md:164-165 |
| `oomd.notices_this_boot` | `0` | round-26 contract.md:95-98 |

**Unpinned output values:** `earlyoom.thresholds` has no threshold records or explicit absence rule; `earlyoom.dryrun` has no explicit default for the absence of a dry-run line; `oomd.state` has no mapping specified in the opened contract. The contract specifies `actions: null` for inactive/absent but does not specify the `actions` representation for `failed`/`unavailable`, so that field is not pinned for case 2. No blocker.

## Validation and retained upstream evidence

Validated the scratch case array with `python3 json.load`; result: valid JSON, 3 cases. No tool installation or update was needed. The five public sources below were fetched by `curl` at `2026-10-22T19:56:08Z`; each hash is SHA-256 of the fetched bytes.

| URL | Fetched UTC | SHA-256 |
|---|---|---|
| https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/main.c | 2026-10-22T19:56:08Z | `08656b0bc90c85f23738661456b25c97af908bc5e2cfea78e0a69697b5f9d0e4` |
| https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/kill.c | 2026-10-22T19:56:08Z | `b32e0fad65e298235102f98aff37e02c94400b544d454cb57192ae697b100bf3` |
| https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/msg.h | 2026-10-22T19:56:08Z | `e36604984a916fb00a624c27c73034bcd87d7d6facff9b290a6a561ee58de56c` |
| https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/MANPAGE.md | 2026-10-22T19:56:08Z | `cc48b02e79255ae27bad9b2c49364fcae1b6b5eb20fe8e83ecef432f360dfeda` |
| https://raw.githubusercontent.com/systemd/systemd/main/man/systemd.journal-fields.xml | 2026-10-22T19:56:08Z | `0af0086ce0e4f4b0a99cb22c6be8d8a7c5ef6e8c19227c3b0191aee91a809144` |

Quoted source evidence (each quote is at most 25 words):

- `main.c:161`: `earlyoom ` (version prefix).
- `kill.c:627`: `sending %s to process %d uid %d`
- `systemd.journal-fields.xml:666`: `<term><varname>__MONOTONIC_TIMESTAMP=</varname></term>`
- `systemd.journal-fields.xml:671`: `formatted as a decimal.`

Files opened:

- `skill://godspeed` (resolved to `/home/vgpnk/.agents/skills/godspeed/SKILL.md`)
- `/home/vgpnk/.omp/agent/RULES.md`
- `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-27/contract.md` (requested lines 40-80)
- `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-26/contract.md` (whole contract and cited A2/output ranges)
- `/home/vgpnk/Projects/shokunin/mori-shokunin/tools/fixtures/mori-oom-killers/cases.json` (schema and journal shapes only)
- `/home/vgpnk/Projects/shokunin/mori-shokunin/tools/fixtures/mori-oom-killers/cases-a2.json` (schema and journal shapes only)
- Scratch downloads: `/fast/scratch/hyaku/mori-r29/CaseA210c/main.c`, `kill.c`, `msg.h`, `MANPAGE.md`, and `systemd.journal-fields.xml`
- Scratch draft validated: `/fast/scratch/hyaku/mori-r29/CaseA210c/cases-a2-10.json`

I did not open or run `tools/mori-oom-killers.py`, inspect its output or run a self-test, or open any other report. No blocker.
The report itself was opened only to correct quote escaping; no other report was opened.
