```json
[
  {
    "id": "r30-disputed-absent-clock",
    "rule": "A2-shape-r30",
    "author": "MoriR30.CaseR30c",
    "why": "rule-text.md:82-83 and 109 make a missing ActiveEnterTimestampMonotonic leave scope_complete false; lines 25-26 and 84-88 separate earlier-invocation sends from current-invocation actions and say earlier sends do not change an active earlyoom verdict; lines 46-48 therefore yield KILLERS_UNKNOWN, exit 2, while the active state and zero current-invocation SIGTERM count follow from the show text and journal order.",
    "inputs": {
      "earlyoom_show": "LoadState=loaded\nActiveState=active\nUnitFileState=enabled",
      "oomd_show": "LoadState=loaded\nActiveState=inactive\nUnitFileState=static\nActiveEnterTimestampMonotonic=0",
      "earlyoom_journal": [
        {"MESSAGE": "earlyoom 1.9.0", "__MONOTONIC_TIMESTAMP": "1000000"},
        {"MESSAGE": "sending SIGTERM to process fixture-alpha", "__MONOTONIC_TIMESTAMP": "1500000"},
        {"MESSAGE": "earlyoom 1.9.0", "__MONOTONIC_TIMESTAMP": "2000000"},
        {"MESSAGE": "sending SIGKILL to process fixture-bravo", "__MONOTONIC_TIMESTAMP": "2500000"},
        {"MESSAGE": "earlyoom 1.9.0", "__MONOTONIC_TIMESTAMP": "3000000"}
      ],
      "oomd_notices": 0
    },
    "expect": {
      "verdict": "KILLERS_UNKNOWN",
      "exit": 2,
      "fields": {
        "earlyoom.state": "active",
        "earlyoom.scope_complete": false,
        "earlyoom.actions.sigterm": 0,
        "earlyoom.earlier_invocation_send_lines": 2
      }
    }
  },
  {
    "id": "r30-disputed-zero-clock",
    "rule": "A2-shape-r30",
    "author": "MoriR30.CaseR30c",
    "why": "rule-text.md:82-83 and 109 make ActiveEnterTimestampMonotonic=0 leave scope_complete false; lines 25-26 and 84-88 separate the single earlier-invocation send from current-invocation actions and say earlier sends do not change an active earlyoom verdict; lines 46-48 therefore yield KILLERS_UNKNOWN, exit 2, while the active state and zero current-invocation SIGTERM count follow from the show text and journal order.",
    "inputs": {
      "earlyoom_show": "LoadState=loaded\nActiveState=active\nUnitFileState=enabled\nActiveEnterTimestampMonotonic=0",
      "oomd_show": "LoadState=loaded\nActiveState=inactive\nUnitFileState=static\nActiveEnterTimestampMonotonic=0",
      "earlyoom_journal": [
        {"MESSAGE": "earlyoom 1.9.0", "__MONOTONIC_TIMESTAMP": "1000000"},
        {"MESSAGE": "sending SIGTERM to process fixture-charlie", "__MONOTONIC_TIMESTAMP": "1500000"},
        {"MESSAGE": "earlyoom 1.9.0", "__MONOTONIC_TIMESTAMP": "2000000"},
        {"MESSAGE": "earlyoom 1.9.0", "__MONOTONIC_TIMESTAMP": "3000000"}
      ],
      "oomd_notices": 0
    },
    "expect": {
      "verdict": "KILLERS_UNKNOWN",
      "exit": 2,
      "fields": {
        "earlyoom.state": "active",
        "earlyoom.scope_complete": false,
        "earlyoom.actions.sigterm": 0,
        "earlyoom.earlier_invocation_send_lines": 1
      }
    }
  }
]
```

| Case | Field | Value | rule-text.md line |
|---|---|---|---|
| r30-disputed-absent-clock | verdict | KILLERS_UNKNOWN | 46-48, 84-88 |
| r30-disputed-absent-clock | exit | 2 | 43-48 |
| r30-disputed-absent-clock | earlyoom.state | active | 37-38, 71-72 |
| r30-disputed-absent-clock | earlyoom.scope_complete | false | 82-83, 109 |
| r30-disputed-absent-clock | earlyoom.actions.sigterm | 0 | 25-26, 84-88 |
| r30-disputed-absent-clock | earlyoom.earlier_invocation_send_lines | 2 | 84-86, 110 |
| r30-disputed-zero-clock | verdict | KILLERS_UNKNOWN | 46-48, 84-88 |
| r30-disputed-zero-clock | exit | 2 | 43-48 |
| r30-disputed-zero-clock | earlyoom.state | active | 37-38, 71-72 |
| r30-disputed-zero-clock | earlyoom.scope_complete | false | 82-83, 109 |
| r30-disputed-zero-clock | earlyoom.actions.sigterm | 0 | 25-26, 84-88 |
| r30-disputed-zero-clock | earlyoom.earlier_invocation_send_lines | 1 | 84-86, 110 |
| Both | Other fields | Not pinned; no values are claimed where the extract does not decide them, and no field outside the allowed list is pinned. | 37-42 |

## Files opened
- /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-30/rule-text.md:1-114
- /home/vgpnk/.agents/skills/godspeed/SKILL.md
- https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/main.c — accessed 2026-10-22T21:12:39Z; sha256 `08656b0bc90c85f23738661456b25c97af908bc5e2cfea78e0a69697b5f9d0e4`; :161 (5 words): `fprintf(stderr, "earlyoom " VERSION "\n");`
- https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/kill.c — accessed 2026-10-22T21:12:39Z; sha256 `b32e0fad65e298235102f98aff37e02c94400b544d454cb57192ae697b100bf3`; :627 (17 words): `warn("sending %s to process %d uid %d \"%s\": oom_score %d, oom_score_adj %d, VmRSS %lld MiB, cmdline \"%s\"\n",`
- https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/msg.h — accessed 2026-10-22T21:12:39Z; sha256 `e36604984a916fb00a624c27c73034bcd87d7d6facff9b290a6a561ee58de56c`; :17 (8 words): `int warn(const char* fmt, ...) __attribute__((format(printf, 1, 2)));`
- https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/MANPAGE.md — accessed 2026-10-22T21:12:39Z; sha256 `cc48b02e79255ae27bad9b2c49364fcae1b6b5eb20fe8e83ecef432f360dfeda`; :41 (11 words): `earlyoom sends SIGTERM once **both** available memory **and** free swap are`
- https://www.freedesktop.org/software/systemd/man/262/org.freedesktop.systemd1.html — accessed 2026-10-22T21:12:41Z; sha256 `e49014d28b05291658105a30aaaf4b7aee546073dd22e8a0fff3018bef714711`; :1297 (10 words): `The fields are 0 in case such a transition has`

I opened no lane tool, lane tool output, lane fixture, or other report.
