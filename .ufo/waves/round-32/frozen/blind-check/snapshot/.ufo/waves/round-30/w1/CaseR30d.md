```json
[
  {
    "id": "r30-disputed-zero-stamp-kill-failed",
    "rule": "A2-shape-r30",
    "author": "CaseR30d",
    "why": "ActiveState=active gives earlyoom.state=active (rule-text.md:37-42). The earlier version and send precede the last version line, which begins the current invocation; the send is therefore one earlier-invocation send, while no send follows the last version line, so current earlyoom.actions.sigterm is 0 and earlyoom.earlier_invocation_send_lines is 1 (rule-text.md:27-35, 84-88). The intervening kill failed line is not a send or escalation counted by that earlier-invocation field (rule-text.md:32-35, 85-86). A zero timestamp leaves scope_complete false (rule-text.md:82-83). The earlier send does not change the verdict for active earlyoom; with incomplete scope and no current-invocation positive evidence, verdict is KILLERS_UNKNOWN, exit 2 (rule-text.md:46-50, 86-88). No other action field is pinned.",
    "inputs": {
      "earlyoom_show": "LoadState=loaded\nActiveState=active\nUnitFileState=enabled\nActiveEnterTimestampMonotonic=0",
      "oomd_show": "LoadState=loaded\nActiveState=inactive\nUnitFileState=disabled\nActiveEnterTimestampMonotonic=0",
      "earlyoom_journal": [
        {
          "MESSAGE": "earlyoom 1.9.0",
          "__MONOTONIC_TIMESTAMP": "100"
        },
        {
          "MESSAGE": "sending SIGTERM to process 4242 uid 1000 \"worker\": oom_score 900, oom_score_adj 0, VmRSS 128 MiB, cmdline \"worker\"",
          "__MONOTONIC_TIMESTAMP": "200"
        },
        {
          "MESSAGE": "kill failed: Operation not permitted",
          "__MONOTONIC_TIMESTAMP": "250"
        },
        {
          "MESSAGE": "earlyoom 1.9.0",
          "__MONOTONIC_TIMESTAMP": "300"
        },
        {
          "MESSAGE": "sending SIGTERM when mem avail <= 10% and swap free <= 10%,",
          "__MONOTONIC_TIMESTAMP": "310"
        },
        {
          "MESSAGE": "        SIGKILL when mem avail <= 5% and swap free <= 5%",
          "__MONOTONIC_TIMESTAMP": "320"
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
        "earlyoom.scope_complete": false
      }
    }
  },
  {
    "id": "r30-disputed-absent-stamp-ordered",
    "rule": "A2-shape-r30",
    "author": "CaseR30d",
    "why": "ActiveState=active gives earlyoom.state=active (rule-text.md:37-42). The earlier version and send have the lowest timestamps and precede the last version line; that send is one earlier-invocation send, while no send follows the last version line, so current earlyoom.actions.sigterm is 0 and earlyoom.earlier_invocation_send_lines is 1 (rule-text.md:27-35, 84-88). An absent timestamp leaves scope_complete false (rule-text.md:82-83). The earlier send does not change the verdict for active earlyoom; with incomplete scope and no current-invocation positive evidence, verdict is KILLERS_UNKNOWN, exit 2 (rule-text.md:46-50, 86-88). No other action field is pinned.",
    "inputs": {
      "earlyoom_show": "LoadState=loaded\nActiveState=active\nUnitFileState=enabled",
      "oomd_show": "LoadState=loaded\nActiveState=inactive\nUnitFileState=disabled\nActiveEnterTimestampMonotonic=0",
      "earlyoom_journal": [
        {
          "MESSAGE": "earlyoom 1.9.0",
          "__MONOTONIC_TIMESTAMP": "10"
        },
        {
          "MESSAGE": "sending SIGTERM to process 5252 uid 1000 \"worker\": oom_score 900, oom_score_adj 0, VmRSS 128 MiB, cmdline \"worker\"",
          "__MONOTONIC_TIMESTAMP": "20"
        },
        {
          "MESSAGE": "earlyoom 1.9.0",
          "__MONOTONIC_TIMESTAMP": "100"
        },
        {
          "MESSAGE": "sending SIGTERM when mem avail <= 10% and swap free <= 10%,",
          "__MONOTONIC_TIMESTAMP": "101"
        },
        {
          "MESSAGE": "        SIGKILL when mem avail <= 5% and swap free <= 5%",
          "__MONOTONIC_TIMESTAMP": "102"
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
        "earlyoom.scope_complete": false
      }
    }
  }
]
```

| case | field | value | rule-text.md line |
|---|---|---|---|
| r30-disputed-zero-stamp-kill-failed | earlyoom.state | active | 37-42 |
| r30-disputed-zero-stamp-kill-failed | earlyoom.actions.sigterm | 0 | 29-35, 84-88 |
| r30-disputed-zero-stamp-kill-failed | earlyoom.earlier_invocation_send_lines | 1 | 32-35, 84-88 |
| r30-disputed-zero-stamp-kill-failed | earlyoom.scope_complete | false | 82-83 |
| r30-disputed-zero-stamp-kill-failed | verdict / exit | KILLERS_UNKNOWN / 2 | 46-50, 86-88 |
| r30-disputed-absent-stamp-ordered | earlyoom.state | active | 37-42 |
| r30-disputed-absent-stamp-ordered | earlyoom.actions.sigterm | 0 | 29-35, 84-88 |
| r30-disputed-absent-stamp-ordered | earlyoom.earlier_invocation_send_lines | 1 | 32-35, 84-88 |
| r30-disputed-absent-stamp-ordered | earlyoom.scope_complete | false | 82-83 |
| r30-disputed-absent-stamp-ordered | verdict / exit | KILLERS_UNKNOWN / 2 | 46-50, 86-88 |

## Files opened
/home/vgpnk/.agents/skills/godspeed/SKILL.md
/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-30/rule-text.md
https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/main.c
https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/kill.c
https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/msg.h
https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/MANPAGE.md
https://raw.githubusercontent.com/systemd/systemd/v262/man/org.freedesktop.systemd1.xml

I opened no lane tool, lane tool output, fixture, or other report.
