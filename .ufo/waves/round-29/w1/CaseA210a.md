# CaseA210a — A2-10 blind cases

## Cases

```json
[
  {
    "id": "r29-a2-10-unbounded-missing-stamp-alone",
    "rule": "A2-10",
    "author": "CaseA210a",
    "why": "A2-10 leaves a send without a numeric __MONOTONIC_TIMESTAMP uncounted and makes the scope incomplete (.ufo/waves/round-27/contract.md:58; .ufo/waves/round-26/contract.md:186-188). The active unit has no ActiveEnterTimestampMonotonic, so A2-05 also leaves the invocation unbounded and incomplete (round-27:53; round-26:173-174). With no counted send or oomd notice, an active incomplete scope has KILLERS_UNKNOWN/exit 2 (round-26:96-102).",
    "inputs": {
      "earlyoom_show": "LoadState=loaded\nActiveState=active\nUnitFileState=enabled",
      "oomd_show": "LoadState=loaded\nActiveState=inactive\nUnitFileState=disabled\nActiveEnterTimestampMonotonic=0",
      "earlyoom_journal": [
        {"MESSAGE": "earlyoom 1.9.0", "__MONOTONIC_TIMESTAMP": "73100000"},
        {"MESSAGE": "sending SIGTERM to process 4101 \"fictional-orchid\""}
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
        "earlyoom.process_group_lines": 0,
        "earlyoom.earlier_invocation_send_lines": 0,
        "earlyoom.dryrun": false,
        "earlyoom.dryrun_send_lines": 0,
        "oomd.state": "inactive",
        "oomd.notices_this_boot": 0
      }
    }
  },
  {
    "id": "r29-a2-10-zero-unbounded-mixed-sigterm",
    "rule": "A2-10",
    "author": "CaseA210a",
    "why": "A2-10 leaves the nonnumeric SIGKILL record uncounted and makes the scope incomplete; ActiveEnterTimestampMonotonic=0 is also unbounded under A2-05 (.ufo/waves/round-27/contract.md:53,58; .ufo/waves/round-26/contract.md:173-174,186-188). The stamped SIGTERM is within the scope beginning at 0, and positive evidence elsewhere stands despite incompleteness, so the verdict is KILLER_ACTED/exit 1 (.ufo/waves/round-26/contract.md:78,96-99).",
    "inputs": {
      "earlyoom_show": "LoadState=loaded\nActiveState=active\nUnitFileState=enabled\nActiveEnterTimestampMonotonic=0",
      "oomd_show": "LoadState=loaded\nActiveState=inactive\nUnitFileState=disabled\nActiveEnterTimestampMonotonic=0",
      "earlyoom_journal": [
        {"MESSAGE": "earlyoom 1.9.0", "__MONOTONIC_TIMESTAMP": "82000000"},
        {"MESSAGE": "sending SIGKILL to process 5202 \"fictional-aurora\"", "__MONOTONIC_TIMESTAMP": "not-numeric"},
        {"MESSAGE": "sending SIGTERM to process 5203 \"fictional-birch\"", "__MONOTONIC_TIMESTAMP": "82000300"}
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
        "earlyoom.process_group_lines": 0,
        "earlyoom.earlier_invocation_send_lines": 0,
        "earlyoom.dryrun": false,
        "earlyoom.dryrun_send_lines": 0,
        "oomd.state": "inactive",
        "oomd.notices_this_boot": 0
      }
    }
  },
  {
    "id": "r29-a2-10-zero-unbounded-mixed-sigkill",
    "rule": "A2-10",
    "author": "CaseA210a",
    "why": "A2-10 leaves the SIGTERM record with its timestamp key absent uncounted and makes the scope incomplete; ActiveEnterTimestampMonotonic=0 is also unbounded under A2-05 (.ufo/waves/round-27/contract.md:53,58; .ufo/waves/round-26/contract.md:173-174,186-188). The stamped SIGKILL is within the scope beginning at 0, and positive evidence elsewhere stands despite incompleteness, so the verdict is KILLER_ACTED/exit 1 (.ufo/waves/round-26/contract.md:78,96-99).",
    "inputs": {
      "earlyoom_show": "LoadState=loaded\nActiveState=active\nUnitFileState=enabled\nActiveEnterTimestampMonotonic=0",
      "oomd_show": "LoadState=loaded\nActiveState=inactive\nUnitFileState=disabled\nActiveEnterTimestampMonotonic=0",
      "earlyoom_journal": [
        {"MESSAGE": "earlyoom 1.9.0", "__MONOTONIC_TIMESTAMP": "91000000"},
        {"MESSAGE": "sending SIGTERM to process 6301 \"fictional-cirrus\""},
        {"MESSAGE": "sending SIGKILL to process 6302 \"fictional-driftwood\"", "__MONOTONIC_TIMESTAMP": "91000600"}
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
        "earlyoom.process_group_lines": 0,
        "earlyoom.earlier_invocation_send_lines": 0,
        "earlyoom.dryrun": false,
        "earlyoom.dryrun_send_lines": 0,
        "oomd.state": "inactive",
        "oomd.notices_this_boot": 0
      }
    }
  }
]
```

## Per-case derivation

Contract aliases: `round-27` = `.ufo/waves/round-27/contract.md`; `round-26` = `.ufo/waves/round-26/contract.md`.

### r29-a2-10-unbounded-missing-stamp-alone

| Field | Value | Contract line |
|---|---|---|
| `expect.verdict` | `KILLERS_UNKNOWN` | round-26:96-102 |
| `expect.exit` | `2` | round-26:99-102 |
| `earlyoom.state` | `active` | round-27:50; round-26:90-95 |
| `earlyoom.version` | `1.9.0` | round-26:80-84,90-95 |
| `earlyoom.grammar` | `verified-1.9.0` | round-26:80-95 |
| `earlyoom.scope_complete` | `false` | round-27:53,58; round-26:173-174,186-188 |
| `earlyoom.actions.sigterm` | `0` | round-26:85,93-98,186-188 |
| `earlyoom.actions.sigkill` | `0` | round-26:85,93-95,186-188 |
| `earlyoom.actions.escalations` | `0` | round-26:86,93-95 |
| `earlyoom.actions.kill_failed` | `0` | round-26:87,93-95 |
| `earlyoom.actions.low_memory_warnings` | `0` | round-26:88,93-95 |
| `earlyoom.process_group_lines` | `0` | round-27:51; round-26:164-165 |
| `earlyoom.earlier_invocation_send_lines` | `0` | round-26:175-179,186-188 |
| `earlyoom.dryrun` | `false` | round-26:89,166-167 |
| `earlyoom.dryrun_send_lines` | `0` | round-27:52; round-26:166-167 |
| `oomd.state` | `inactive` | round-26:90-95,102-104 |
| `oomd.notices_this_boot` | `0` | round-26:73-76,95,97 |

### r29-a2-10-zero-unbounded-mixed-sigterm

| Field | Value | Contract line |
|---|---|---|
| `expect.verdict` | `KILLER_ACTED` | round-26:96-99 |
| `expect.exit` | `1` | round-26:97-99 |
| `earlyoom.state` | `active` | round-27:50; round-26:90-95 |
| `earlyoom.version` | `1.9.0` | round-26:80-84,90-95 |
| `earlyoom.grammar` | `verified-1.9.0` | round-26:80-95 |
| `earlyoom.scope_complete` | `false` | round-27:53,58; round-26:173-174,186-188 |
| `earlyoom.actions.sigterm` | `1` | round-26:78,85,93-98,186-188 |
| `earlyoom.actions.sigkill` | `0` | round-26:85,93-95,186-188 |
| `earlyoom.actions.escalations` | `0` | round-26:86,93-95 |
| `earlyoom.actions.kill_failed` | `0` | round-26:87,93-95 |
| `earlyoom.actions.low_memory_warnings` | `0` | round-26:88,93-95 |
| `earlyoom.process_group_lines` | `0` | round-27:51; round-26:164-165 |
| `earlyoom.earlier_invocation_send_lines` | `0` | round-26:82,175-179,186-188 |
| `earlyoom.dryrun` | `false` | round-26:89,166-167 |
| `earlyoom.dryrun_send_lines` | `0` | round-27:52; round-26:166-167 |
| `oomd.state` | `inactive` | round-26:90-95,102-104 |
| `oomd.notices_this_boot` | `0` | round-26:73-76,95,97 |

### r29-a2-10-zero-unbounded-mixed-sigkill

| Field | Value | Contract line |
|---|---|---|
| `expect.verdict` | `KILLER_ACTED` | round-26:96-99 |
| `expect.exit` | `1` | round-26:97-99 |
| `earlyoom.state` | `active` | round-27:50; round-26:90-95 |
| `earlyoom.version` | `1.9.0` | round-26:80-84,90-95 |
| `earlyoom.grammar` | `verified-1.9.0` | round-26:80-95 |
| `earlyoom.scope_complete` | `false` | round-27:53,58; round-26:173-174,186-188 |
| `earlyoom.actions.sigterm` | `0` | round-26:85,93-98,186-188 |
| `earlyoom.actions.sigkill` | `1` | round-26:78,85,93-98,186-188 |
| `earlyoom.actions.escalations` | `0` | round-26:86,93-95 |
| `earlyoom.actions.kill_failed` | `0` | round-26:87,93-95 |
| `earlyoom.actions.low_memory_warnings` | `0` | round-26:88,93-95 |
| `earlyoom.process_group_lines` | `0` | round-27:51; round-26:164-165 |
| `earlyoom.earlier_invocation_send_lines` | `0` | round-26:82,175-179,186-188 |
| `earlyoom.dryrun` | `false` | round-26:89,166-167 |
| `earlyoom.dryrun_send_lines` | `0` | round-27:52; round-26:166-167 |
| `oomd.state` | `inactive` | round-26:90-95,102-104 |
| `oomd.notices_this_boot` | `0` | round-26:73-76,95,97 |

`earlyoom.thresholds` is intentionally unpinned: the contracts identify threshold message grammar and an output object-or-null, but do not state the absent-threshold default. The cases pin `earlyoom.scope_complete` and the affected action counters; each has no threshold messages.

## Upstream source evidence

Quotes are verbatim and each is under 25 words. The UTC timestamp is the `date -u +%FT%TZ` result immediately after each curl fetch; hashes are SHA-256 of fetched bytes.

- `https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/main.c` — fetched 2026-10-22T19:55:56Z; SHA-256 `08656b0bc90c85f23738661456b25c97af908bc5e2cfea78e0a69697b5f9d0e4`. Quote, line 161: `fprintf(stderr, "earlyoom " VERSION "\\n");`
- `https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/kill.c` — fetched 2026-10-22T19:55:56Z; SHA-256 `b32e0fad65e298235102f98aff37e02c94400b544d454cb57192ae697b100bf3`. Quote, line 627: `warn("sending %s to process %d`
- Same URL, quote, line 318: `warn("escalating to SIGKILL after %.3f seconds\\n", secs);`
- `https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/msg.h` — fetched 2026-10-22T19:55:56Z; SHA-256 `e36604984a916fb00a624c27c73034bcd87d7d6facff9b290a6a561ee58de56c`. Quote, line 29: `term_kill_tuple_t parse_term_kill_tuple(const char* optarg, long long upper_limit);` This header contains no matching send-log template in the inspected declaration lines.
- `https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/MANPAGE.md` — fetched 2026-10-22T19:55:56Z; SHA-256 `cc48b02e79255ae27bad9b2c49364fcae1b6b5eb20fe8e83ecef432f360dfeda`. Quote, lines 211-212: `Usually this is not needed as systemd handles logging of all output.`
- `https://raw.githubusercontent.com/systemd/systemd/main/man/systemd.journal-fields.xml` — fetched 2026-10-22T19:55:56Z; SHA-256 `0af0086ce0e4f4b0a99cb22c6be8d8a7c5ef6e8c19227c3b0191aee91a809144`. Quote, lines 668-671: `The monotonic time (<constant>CLOCK_MONOTONIC</constant>) at the point in time the entry was received by the journal in microseconds, formatted as a decimal.`

## Opened files and scope

- Skill instructions: `skill://godspeed` (`/home/vgpnk/.agents/skills/godspeed/SKILL.md`).
- Allowed contract sources: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-27/contract.md` (requested 40-80); `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-26/contract.md` (whole file, including A2).
- Allowed fixture sources: `/home/vgpnk/Projects/shokunin/mori-shokunin/tools/fixtures/mori-oom-killers/cases.json` and `cases-a2.json` (schema/journal-shape queries).
- Fetched/read under my scratch directory: `/fast/scratch/hyaku/mori-r29/CaseA210a/earlyoom-main.c`, `earlyoom-kill.c`, `earlyoom-msg.h`, `earlyoom-MANPAGE.md`, `systemd-journal-fields.xml`.
- Draft written and opened only by the requested JSON validation: `/fast/scratch/hyaku/mori-r29/CaseA210a/cases-a2-10.json`.
- The public URLs and fetched timestamps/hashes are listed above. No tool was installed or updated.
- Reader-output note: selecting round-27 lines 40-80 rendered contextual lines 39 and 81-83 as well. The fixture queries also returned `oomd_notices` members in addition to schema/journal shapes; those extra values were not used in case derivations.
- I did not open or run `tools/mori-oom-killers.py`, any copy of it, or its self-test; no output from that tool was read or copied. I opened no other report, no lessons, no SCORECARD, no LOG, and no other file under `.ufo/waves/` beyond the two named contracts.

## Validation

`python3 -c 'import json; ... json.load(...) ...'` in `/fast/scratch/hyaku/mori-r29/CaseA210a` reported `json.load: ok; cases=3`.
