```json
[
  {
    "id": "r30-disputed-missing-stamp-one-send",
    "rule": "A2-shape-r30",
    "author": "CaseR30a",
    "why": "Rule text lines 82-83 make a missing ActiveEnterTimestampMonotonic unbounded and scope_complete false. Lines 29, 32, 37-42, and 85-86 identify version and send lines, separate earlier sends from the current invocation, and define actions; the earlier send count is 1 and current actions.sigterm is 0 because no send follows the final version line. Lines 46-48 make an active earlyoom with incomplete scope KILLERS_UNKNOWN (exit 2); lines 85-88 say earlier sends are reported but do not change an active earlyoom verdict. No other optional fields are pinned.",
    "inputs": {
      "earlyoom_show": "LoadState=loaded\nActiveState=active\nUnitFileState=enabled",
      "oomd_show": "LoadState=loaded\nActiveState=inactive\nUnitFileState=enabled\nActiveEnterTimestampMonotonic=0",
      "earlyoom_journal": [
        {
          "MESSAGE": "earlyoom 1.9.0",
          "__MONOTONIC_TIMESTAMP": "100000"
        },
        {
          "MESSAGE": "sending SIGTERM to process fixture-process-alpha",
          "__MONOTONIC_TIMESTAMP": "200000"
        },
        {
          "MESSAGE": "earlyoom 1.9.0",
          "__MONOTONIC_TIMESTAMP": "300000"
        }
      ],
      "oomd_notices": 0
    },
    "expect": {
      "verdict": "KILLERS_UNKNOWN",
      "exit": 2,
      "fields": {
        "earlyoom.actions.sigterm": 0,
        "earlyoom.earlier_invocation_send_lines": 1,
        "earlyoom.scope_complete": false
      }
    }
  },
  {
    "id": "r30-disputed-missing-stamp-two-sends-warning",
    "rule": "A2-shape-r30",
    "author": "CaseR30a",
    "why": "Rule text lines 82-83 make a missing ActiveEnterTimestampMonotonic unbounded and scope_complete false. Lines 29, 32, 37-42, and 85-86 identify version and send lines, separate earlier sends from the current invocation, and define actions; the earlier send count is 2 and current actions.sigterm is 0 because no send follows the final version line. The current-invocation warning matches line 35 but is not positive action evidence under lines 44-48. Lines 46-48 make an active earlyoom with incomplete scope KILLERS_UNKNOWN (exit 2); lines 85-88 say earlier sends are reported but do not change an active earlyoom verdict. No other optional fields are pinned.",
    "inputs": {
      "earlyoom_show": "LoadState=loaded\nActiveState=active\nUnitFileState=enabled",
      "oomd_show": "LoadState=loaded\nActiveState=inactive\nUnitFileState=enabled\nActiveEnterTimestampMonotonic=0",
      "earlyoom_journal": [
        {
          "MESSAGE": "earlyoom 1.9.0",
          "__MONOTONIC_TIMESTAMP": "100000"
        },
        {
          "MESSAGE": "sending SIGTERM to process fixture-process-alpha",
          "__MONOTONIC_TIMESTAMP": "150000"
        },
        {
          "MESSAGE": "sending SIGTERM to process fixture-process-beta",
          "__MONOTONIC_TIMESTAMP": "200000"
        },
        {
          "MESSAGE": "earlyoom 1.9.0",
          "__MONOTONIC_TIMESTAMP": "300000"
        },
        {
          "MESSAGE": "low memory! at or below SIGTERM limits: mem 10.00%, swap 10.00%",
          "__MONOTONIC_TIMESTAMP": "400000"
        }
      ],
      "oomd_notices": 0
    },
    "expect": {
      "verdict": "KILLERS_UNKNOWN",
      "exit": 2,
      "fields": {
        "earlyoom.actions.sigterm": 0,
        "earlyoom.earlier_invocation_send_lines": 2,
        "earlyoom.scope_complete": false
      }
    }
  }
]
```

| Case | Field | Value | rule-text.md line |
|---|---|---|---|
| r30-disputed-missing-stamp-one-send | verdict | KILLERS_UNKNOWN | 46-48, 82-83, 85-88 |
| r30-disputed-missing-stamp-one-send | exit | 2 | 46-48 |
| r30-disputed-missing-stamp-one-send | earlyoom.actions.sigterm | 0 | 29, 32, 37-42, 85-86 |
| r30-disputed-missing-stamp-one-send | earlyoom.earlier_invocation_send_lines | 1 | 85-86 |
| r30-disputed-missing-stamp-one-send | earlyoom.scope_complete | false | 82-83 |
| r30-disputed-missing-stamp-two-sends-warning | verdict | KILLERS_UNKNOWN | 46-48, 82-83, 85-88 |
| r30-disputed-missing-stamp-two-sends-warning | exit | 2 | 46-48 |
| r30-disputed-missing-stamp-two-sends-warning | earlyoom.actions.sigterm | 0 | 29, 32, 37-42, 85-86 |
| r30-disputed-missing-stamp-two-sends-warning | earlyoom.earlier_invocation_send_lines | 2 | 85-86 |
| r30-disputed-missing-stamp-two-sends-warning | earlyoom.scope_complete | false | 82-83 |

## Files opened
/home/vgpnk/.agents/skills/godspeed/SKILL.md
/home/vgpnk/.omp/agent/RULES.md
/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-30/rule-text.md
https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/main.c — accessed 2026-10-22T21:12:12Z; sha256 08656b0bc90c85f23738661456b25c97af908bc5e2cfea78e0a69697b5f9d0e4; excerpt :523 (7 words): "low memory! at or below SIGTERM limits:"
https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/kill.c — accessed 2026-10-22T21:12:12Z; sha256 b32e0fad65e298235102f98aff37e02c94400b544d454cb57192ae697b100bf3
https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/msg.h — accessed 2026-10-22T21:12:12Z; sha256 e36604984a916fb00a624c27c73034bcd87d7d6facff9b290a6a561ee58de56c
https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/MANPAGE.md — accessed 2026-10-22T21:12:12Z; sha256 cc48b02e79255ae27bad9b2c49364fcae1b6b5eb20fe8e83ecef432f360dfeda
https://raw.githubusercontent.com/systemd/systemd/v262/man/org.freedesktop.systemd1.xml — accessed 2026-10-22T21:12:12Z; sha256 59cfeea5144e169369ee81f2b797fe9eb63ec18cb6aa918c2e66a7d5218117ca; inspected :2244, :2783

The scratch JSON passed python3 json.load; I opened no lane tool source, lane tool output, lane fixture, or other report.
