# CaseA210b — A2-10 blind cases

## Cases

```json
[
  {
    "id": "r29-a2-10-unclocked-send-alone",
    "rule": "A2-10",
    "author": "CaseA210b",
    "why": "Round-26 contract.md:80-95 defines the version/grammar/state/action/notice fields, and :164-179 defines added counters; :186-187 leaves this send uncounted and makes scope incomplete; :99-101 maps an active incomplete scope with no positive evidence to KILLERS_UNKNOWN/2. Round-27 contract.md:58 states A2-10.",
    "inputs": {
      "earlyoom_show": "LoadState=loaded\nActiveState=active\nUnitFileState=enabled\nActiveEnterTimestampMonotonic=7200000\n",
      "oomd_show": "LoadState=loaded\nActiveState=inactive\nUnitFileState=disabled\nActiveEnterTimestampMonotonic=0\n",
      "earlyoom_journal": [
        {"MESSAGE": "earlyoom 1.9.0", "__MONOTONIC_TIMESTAMP": "7200000"},
        {"MESSAGE": "sending SIGTERM to process 48152"}
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
        "earlyoom.dryrun_send_lines": 0,
        "earlyoom.process_group_lines": 0,
        "earlyoom.earlier_invocation_send_lines": 0,
        "oomd.state": "inactive",
        "oomd.notices_this_boot": 0
      }
    }
  },
  {
    "id": "r29-a2-10-stamped-send-survives",
    "rule": "A2-10",
    "author": "CaseA210b",
    "why": "Round-26 contract.md:80-95 defines the version/grammar/state/action/notice fields, and :164-179 defines added counters; :186-187 leaves the nonnumeric-timestamp SIGKILL uncounted and makes scope incomplete; :97-98 says the stamped in-scope SIGTERM is positive evidence that stands despite incomplete scope, yielding KILLER_ACTED/1. Round-27 contract.md:58 states A2-10.",
    "inputs": {
      "earlyoom_show": "LoadState=loaded\nActiveState=active\nUnitFileState=enabled\nActiveEnterTimestampMonotonic=8300000\n",
      "oomd_show": "LoadState=loaded\nActiveState=inactive\nUnitFileState=disabled\nActiveEnterTimestampMonotonic=0\n",
      "earlyoom_journal": [
        {"MESSAGE": "earlyoom 1.9.0", "__MONOTONIC_TIMESTAMP": "8300000"},
        {"MESSAGE": "sending SIGTERM to process 58152", "__MONOTONIC_TIMESTAMP": "8300020"},
        {"MESSAGE": "sending SIGKILL to process 58153", "__MONOTONIC_TIMESTAMP": "clock-unavailable"}
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
        "earlyoom.dryrun_send_lines": 0,
        "earlyoom.process_group_lines": 0,
        "earlyoom.earlier_invocation_send_lines": 0,
        "oomd.state": "inactive",
        "oomd.notices_this_boot": 0
      }
    }
  },
  {
    "id": "r29-a2-10-oomd-evidence-survives",
    "rule": "A2-10",
    "author": "CaseA210b",
    "why": "Round-26 contract.md:80-95 defines the version/grammar/state/action/notice fields, and :164-179 defines added counters; :186-187 leaves the nonnumeric-timestamp SIGTERM uncounted and makes scope incomplete; :97-98 says oomd_notices > 0 is positive evidence that stands despite incomplete scope, yielding KILLER_ACTED/1. Round-27 contract.md:58 states A2-10.",
    "inputs": {
      "earlyoom_show": "LoadState=loaded\nActiveState=active\nUnitFileState=enabled\nActiveEnterTimestampMonotonic=9400000\n",
      "oomd_show": "LoadState=loaded\nActiveState=active\nUnitFileState=enabled\nActiveEnterTimestampMonotonic=650000\n",
      "earlyoom_journal": [
        {"MESSAGE": "earlyoom 1.9.0", "__MONOTONIC_TIMESTAMP": "9400000"},
        {"MESSAGE": "sending SIGTERM to process 69152", "__MONOTONIC_TIMESTAMP": "not-a-decimal"}
      ],
      "oomd_notices": 2
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
        "earlyoom.actions.sigkill": 0,
        "earlyoom.actions.escalations": 0,
        "earlyoom.actions.kill_failed": 0,
        "earlyoom.actions.low_memory_warnings": 0,
        "earlyoom.dryrun_send_lines": 0,
        "earlyoom.process_group_lines": 0,
        "earlyoom.earlier_invocation_send_lines": 0,
        "oomd.state": "active",
        "oomd.notices_this_boot": 2
      }
    }
  }
]
```

## Per-case derivation

### `r29-a2-10-unclocked-send-alone`

| Field | Value | Contract line |
|---|---:|---|
| `verdict` | `KILLERS_UNKNOWN` | Round-26:99-101 |
| `exit` | `2` | Round-26:99-101 |
| `earlyoom.state` | `active` | Round-26:90-95, 162-163 |
| `earlyoom.version` | `1.9.0` | Round-26:80-82, 90-95 |
| `earlyoom.grammar` | `verified-1.9.0` | Round-26:80-95 |
| `earlyoom.scope_complete` | `false` | Round-26:186-187 |
| `earlyoom.actions.sigterm` | `0` | Round-26:85, 93-95, 186-187 |
| `earlyoom.actions.sigkill` | `0` | Round-26:85-88, 93-95 |
| `earlyoom.actions.escalations` | `0` | Round-26:86-88, 93-95 |
| `earlyoom.actions.kill_failed` | `0` | Round-26:87-88, 93-95 |
| `earlyoom.actions.low_memory_warnings` | `0` | Round-26:88, 93-95 |
| `earlyoom.dryrun_send_lines` | `0` | Round-26:166-168, 180-181 |
| `earlyoom.process_group_lines` | `0` | Round-26:164-165 |
| `earlyoom.earlier_invocation_send_lines` | `0` | Round-26:175-179, 186-187 |
| `oomd.state` | `inactive` | Round-26:90-95 |
| `oomd.notices_this_boot` | `0` | Round-26:90-98 |

### `r29-a2-10-stamped-send-survives`

| Field | Value | Contract line |
|---|---:|---|
| `verdict` | `KILLER_ACTED` | Round-26:97-98 |
| `exit` | `1` | Round-26:97-98 |
| `earlyoom.state` | `active` | Round-26:90-95, 162-163 |
| `earlyoom.version` | `1.9.0` | Round-26:80-82, 90-95 |
| `earlyoom.grammar` | `verified-1.9.0` | Round-26:80-95 |
| `earlyoom.scope_complete` | `false` | Round-26:186-187 |
| `earlyoom.actions.sigterm` | `1` | Round-26:85, 93-98 |
| `earlyoom.actions.sigkill` | `0` | Round-26:85-88, 93-95, 186-187 |
| `earlyoom.actions.escalations` | `0` | Round-26:86-88, 93-95 |
| `earlyoom.actions.kill_failed` | `0` | Round-26:87-88, 93-95 |
| `earlyoom.actions.low_memory_warnings` | `0` | Round-26:88, 93-95 |
| `earlyoom.dryrun_send_lines` | `0` | Round-26:166-168, 180-181 |
| `earlyoom.process_group_lines` | `0` | Round-26:164-165 |
| `earlyoom.earlier_invocation_send_lines` | `0` | Round-26:175-179, 186-187 |
| `oomd.state` | `inactive` | Round-26:90-95 |
| `oomd.notices_this_boot` | `0` | Round-26:90-98 |

### `r29-a2-10-oomd-evidence-survives`

| Field | Value | Contract line |
|---|---:|---|
| `verdict` | `KILLER_ACTED` | Round-26:97-98 |
| `exit` | `1` | Round-26:97-98 |
| `earlyoom.state` | `active` | Round-26:90-95, 162-163 |
| `earlyoom.version` | `1.9.0` | Round-26:80-82, 90-95 |
| `earlyoom.grammar` | `verified-1.9.0` | Round-26:80-95 |
| `earlyoom.scope_complete` | `false` | Round-26:186-187 |
| `earlyoom.actions.sigterm` | `0` | Round-26:85, 93-95, 186-187 |
| `earlyoom.actions.sigkill` | `0` | Round-26:85-88, 93-95 |
| `earlyoom.actions.escalations` | `0` | Round-26:86-88, 93-95 |
| `earlyoom.actions.kill_failed` | `0` | Round-26:87-88, 93-95 |
| `earlyoom.actions.low_memory_warnings` | `0` | Round-26:88, 93-95 |
| `earlyoom.dryrun_send_lines` | `0` | Round-26:166-168, 180-181 |
| `earlyoom.process_group_lines` | `0` | Round-26:164-165 |
| `earlyoom.earlier_invocation_send_lines` | `0` | Round-26:175-179, 186-187 |
| `oomd.state` | `active` | Round-26:90-95 |
| `oomd.notices_this_boot` | `2` | Round-26:90-98 |

**Not pinned in each case:** `earlyoom.thresholds` and `earlyoom.dryrun`. The inputs contain no threshold-setting line or `dryrun mode enabled` line. The contract names the thresholds field as an object or null and documents the dry-run trigger, but does not state the output for a missing such line (Round-26:88-95, 166-168), so these values are intentionally not inferred.

## Upstream source evidence

Access times are UTC immediately before each `curl`; SHA-256 is over the fetched bytes.

| URL | Access time | SHA-256 | Quote (verbatim, line) |
|---|---|---|---|
| `https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/main.c` | `2026-10-22T19:55:54Z` | `08656b0bc90c85f23738661456b25c97af908bc5e2cfea78e0a69697b5f9d0e4` | `fprintf(stderr, "earlyoom " VERSION "\\n");` (main.c:161) |
| `https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/kill.c` | `2026-10-22T19:55:54Z` | `b32e0fad65e298235102f98aff37e02c94400b544d454cb57192ae697b100bf3` | `sending %s to process %d` (kill.c:627) |
| `https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/msg.h` | `2026-10-22T19:55:54Z` | `e36604984a916fb00a624c27c73034bcd87d7d6facff9b290a6a561ee58de56c` | `int warn(const char* fmt, ...) __attribute__((format(printf, 1, 2)));` (msg.h:17) |
| `https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/MANPAGE.md` | `2026-10-22T19:55:54Z` | `cc48b02e79255ae27bad9b2c49364fcae1b6b5eb20fe8e83ecef432f360dfeda` | `earlyoom sends SIGTERM once **both** available memory **and** free swap are below their respective PERCENT settings.` (MANPAGE.md:41-42) |
| `https://www.freedesktop.org/software/systemd/man/latest/systemd.journal-fields.html` | `2026-10-22T19:55:54Z` | `906e5d34b38913ddaf729f74f468f5511f8a143bb3f86f0fdda06957af7bf5e7` | `formatted as a decimal.` (systemd.journal-fields.html:210) |

## Files and URLs opened

- `/home/vgpnk/.agents/skills/godspeed/SKILL.md` (via `skill://godspeed`).
- `/home/vgpnk/.omp/agent/RULES.md`.
- `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-27/contract.md` (lines 40-80).
- `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-26/contract.md` (whole file).
- `/home/vgpnk/Projects/shokunin/mori-shokunin/tools/fixtures/mori-oom-killers/cases.json` (schema and journal shape only).
- `/home/vgpnk/Projects/shokunin/mori-shokunin/tools/fixtures/mori-oom-killers/cases-a2.json` (schema and journal shape only).
- Scratch files opened: `/fast/scratch/hyaku/mori-r29/CaseA210b/main.c`, `kill.c`, `msg.h`, `MANPAGE.md`, `systemd.journal-fields.html`, and `cases-a2-10.json`.
- URLs opened are the five URLs in the upstream evidence table above.

## Validation, tooling, and blindness

- Scratch JSON validation: `python3 -c 'import json; json.load(open("cases-a2-10.json", encoding="utf-8")); print("json.load: ok")'` in `/fast/scratch/hyaku/mori-r29/CaseA210b`; observed `json.load: ok`.
- No tools were installed or updated.
- No tool implementation was opened or run, and no output from that tool was viewed. No other report was opened.
- Risks/blockers: none beyond the intentionally unpinned fields described above.
