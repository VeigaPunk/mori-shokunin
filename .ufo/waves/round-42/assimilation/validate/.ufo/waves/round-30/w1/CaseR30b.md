```json
[
  {
    "id": "r30-disputed-escalation",
    "rule": "A2-shape-r30",
    "author": "CaseR30b",
    "why": "rule-text.md:27-33 classifies version, threshold, send, and escalation lines. The prior invocation has one SIGTERM send and one escalation; rule-text.md:84-88 counts both outside the current invocation, so earlier_invocation_send_lines is 2 and current sigterm/sigkill counts are 0. The final version line starts the current plain restart and only threshold lines follow. ActiveState=active selects the active case (rule-text.md:37-40,46-48); ActiveEnterTimestampMonotonic=0 makes scope_complete false (rule-text.md:82), so with no current-invocation action the verdict is KILLERS_UNKNOWN and exit 2 (rule-text.md:46-48). No other fields are pinned; the supplied rule text does not decide additional permitted field pins for these inputs.",
    "inputs": {
      "earlyoom_show": "LoadState=loaded\nActiveState=active\nUnitFileState=enabled\nActiveEnterTimestampMonotonic=0",
      "oomd_show": "LoadState=loaded\nActiveState=inactive\nUnitFileState=enabled\nActiveEnterTimestampMonotonic=0",
      "earlyoom_journal": [
        {
          "MESSAGE": "earlyoom 1.9.0",
          "__MONOTONIC_TIMESTAMP": "1000000"
        },
        {
          "MESSAGE": "sending SIGTERM to process 4242 uid 1000 \"worker\": oom_score 512, oom_score_adj 0, VmRSS 256 MiB, cmdline \"worker --task\"",
          "__MONOTONIC_TIMESTAMP": "1100000"
        },
        {
          "MESSAGE": "escalating to SIGKILL after 0.250 seconds",
          "__MONOTONIC_TIMESTAMP": "1200000"
        },
        {
          "MESSAGE": "earlyoom 1.9.0",
          "__MONOTONIC_TIMESTAMP": "2000000"
        },
        {
          "MESSAGE": "sending SIGTERM when mem avail <= 10.00% and swap free <= 10.00%,",
          "__MONOTONIC_TIMESTAMP": "2100000"
        },
        {
          "MESSAGE": "        SIGKILL when mem avail <= 5.00% and swap free <= 5.00%",
          "__MONOTONIC_TIMESTAMP": "2200000"
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
        "earlyoom.state": "active",
        "earlyoom.scope_complete": false,
        "earlyoom.actions.sigkill": 0
      }
    }
  },
  {
    "id": "r30-disputed-sigkill",
    "rule": "A2-shape-r30",
    "author": "CaseR30b",
    "why": "rule-text.md:27-33 classifies version, threshold, and SIGKILL-send lines. The prior invocation has one SIGKILL send; rule-text.md:84-88 counts it outside the current invocation, so earlier_invocation_send_lines is 1 and current sigterm/sigkill counts are 0. The final version line starts the current plain restart, whose only later lines are thresholds. ActiveState=active selects the active case (rule-text.md:37-40,46-48); ActiveEnterTimestampMonotonic=0 makes scope_complete false (rule-text.md:82), so with no current-invocation action the verdict is KILLERS_UNKNOWN and exit 2 (rule-text.md:46-48). No other fields are pinned; the supplied rule text does not decide additional permitted field pins for these inputs.",
    "inputs": {
      "earlyoom_show": "LoadState=loaded\nActiveState=active\nUnitFileState=enabled\nActiveEnterTimestampMonotonic=0",
      "oomd_show": "LoadState=loaded\nActiveState=inactive\nUnitFileState=enabled\nActiveEnterTimestampMonotonic=0",
      "earlyoom_journal": [
        {
          "MESSAGE": "earlyoom 1.9.0",
          "__MONOTONIC_TIMESTAMP": "3000000"
        },
        {
          "MESSAGE": "sending SIGKILL to process 5151 uid 1001 \"renderer\": oom_score 640, oom_score_adj 0, VmRSS 512 MiB, cmdline \"renderer --isolated\"",
          "__MONOTONIC_TIMESTAMP": "3100000"
        },
        {
          "MESSAGE": "earlyoom 1.9.0",
          "__MONOTONIC_TIMESTAMP": "4000000"
        },
        {
          "MESSAGE": "sending SIGTERM when mem avail <= 10.00% and swap free <= 10.00%,",
          "__MONOTONIC_TIMESTAMP": "4100000"
        },
        {
          "MESSAGE": "        SIGKILL when mem avail <= 5.00% and swap free <= 5.00%",
          "__MONOTONIC_TIMESTAMP": "4200000"
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
        "earlyoom.state": "active",
        "earlyoom.scope_complete": false,
        "earlyoom.actions.sigkill": 0
      }
    }
  }
]
```

| case | field | value | rule-text.md line |
|---|---|---:|---|
| r30-disputed-escalation | earlyoom.actions.sigterm | 0 | 27-33, 84-88 |
| r30-disputed-escalation | earlyoom.earlier_invocation_send_lines | 2 | 84-88 |
| r30-disputed-escalation | earlyoom.state | active | 37-40, 46-48 |
| r30-disputed-escalation | earlyoom.scope_complete | false | 82 |
| r30-disputed-escalation | earlyoom.actions.sigkill | 0 | 27-33, 84-88 |
| r30-disputed-escalation | verdict | KILLERS_UNKNOWN | 46-48, 82-88 |
| r30-disputed-escalation | exit | 2 | 46-48 |
| r30-disputed-sigkill | earlyoom.actions.sigterm | 0 | 27-33, 84-88 |
| r30-disputed-sigkill | earlyoom.earlier_invocation_send_lines | 1 | 84-88 |
| r30-disputed-sigkill | earlyoom.state | active | 37-40, 46-48 |
| r30-disputed-sigkill | earlyoom.scope_complete | false | 82 |
| r30-disputed-sigkill | earlyoom.actions.sigkill | 0 | 27-33, 84-88 |
| r30-disputed-sigkill | verdict | KILLERS_UNKNOWN | 46-48, 82-88 |
| r30-disputed-sigkill | exit | 2 | 46-48 |

## Files opened
/home/vgpnk/.agents/skills/godspeed/SKILL.md
/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-30/rule-text.md
https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/main.c
https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/kill.c
https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/msg.h
https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/MANPAGE.md
I opened no lane tool, lane-tool output, fixture, or other report.
