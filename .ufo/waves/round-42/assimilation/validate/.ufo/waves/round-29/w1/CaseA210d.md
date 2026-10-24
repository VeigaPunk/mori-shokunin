# A2-10 blind cases — CaseA210d

## Cases

```json
[
  {
    "id": "r29-a2-10-empty-and-letters",
    "rule": "A2-10",
    "author": "CaseA210d",
    "why": "A2-10 says a record without a numeric __MONOTONIC_TIMESTAMP is left uncounted and makes scope incomplete (round-27/contract.md:58; round-26/contract.md:186-188), so the empty and alphabetic records leave earlyoom.scope_complete false despite the numeric version record at ActiveEnterTimestampMonotonic=51000000 (round-26/contract.md:78-82). The active state, version, and grammar outputs are decided by the declared output and version-line grammar (round-26/contract.md:82,90-95). The numeric dry-run marker sets dryrun true; A2-04 directs sends to dryrun_send_lines and keeps SIGTERM/SIGKILL at zero (round-27/contract.md:53; round-26/contract.md:166-167). None of the numeric records matches an action, failure, warning, process-group, or send/escalation grammar (round-26/contract.md:85-89; round-27/contract.md:51,54), so those counts are zero. With inactive oomd and zero notices there is no positive evidence; active earlyoom with incomplete scope is KILLERS_UNKNOWN, exit 2 (round-26/contract.md:95,97-101).",
    "inputs": {
      "earlyoom_show": "LoadState=loaded\nActiveState=active\nUnitFileState=enabled\nActiveEnterTimestampMonotonic=51000000\n",
      "oomd_show": "LoadState=loaded\nActiveState=inactive\nUnitFileState=disabled\nActiveEnterTimestampMonotonic=0\n",
      "earlyoom_journal": [
        {"MESSAGE": "earlyoom 1.9.0", "__MONOTONIC_TIMESTAMP": "51000000"},
        {"MESSAGE": "dryrun mode enabled, will not kill anything", "__MONOTONIC_TIMESTAMP": "51000001"},
        {"MESSAGE": "empty-stamp record", "__MONOTONIC_TIMESTAMP": ""},
        {"MESSAGE": "letter-stamp record", "__MONOTONIC_TIMESTAMP": "clock"},
        {"MESSAGE": "ordinary numeric-stamp record", "__MONOTONIC_TIMESTAMP": "51000002"}
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
        "earlyoom.dryrun_send_lines": 0,
        "earlyoom.process_group_lines": 0,
        "earlyoom.earlier_invocation_send_lines": 0,
        "oomd.state": "inactive",
        "oomd.notices_this_boot": 0
      }
    }
  },
  {
    "id": "r29-a2-10-negative-and-decimal",
    "rule": "A2-10",
    "author": "CaseA210d",
    "why": "A2-10 says a record without a numeric __MONOTONIC_TIMESTAMP is left uncounted and makes scope incomplete (round-27/contract.md:58; round-26/contract.md:186-188), so the negative and fractional records are excluded while the numeric version and escalation records at 62000000 and 62000003 remain in scope (round-26/contract.md:78-82). The numeric escalation matches the declared escalation format and is positive evidence; positive evidence stands despite incomplete scope, so this is KILLER_ACTED, exit 1 (round-26/contract.md:86,97-98). The active state, version, grammar, action, and oomd output paths are specified at round-26/contract.md:82,90-95. The other numeric records match no action, failure, warning, process-group, or earlier-invocation send/escalation format (round-26/contract.md:85,87-89; round-27/contract.md:51,54), so their counts are zero. Oomd is inactive with zero notices (round-26/contract.md:95), and does not add positive evidence.",
    "inputs": {
      "earlyoom_show": "LoadState=loaded\nActiveState=active\nUnitFileState=enabled\nActiveEnterTimestampMonotonic=62000000\n",
      "oomd_show": "LoadState=loaded\nActiveState=inactive\nUnitFileState=disabled\nActiveEnterTimestampMonotonic=0\n",
      "earlyoom_journal": [
        {"MESSAGE": "earlyoom 1.9.0", "__MONOTONIC_TIMESTAMP": "62000000"},
        {"MESSAGE": "negative-stamp record", "__MONOTONIC_TIMESTAMP": "-62000002"},
        {"MESSAGE": "decimal-stamp record", "__MONOTONIC_TIMESTAMP": "62000002.5"},
        {"MESSAGE": "escalating to SIGKILL after 1.500 seconds", "__MONOTONIC_TIMESTAMP": "62000003"},
        {"MESSAGE": "ordinary numeric-stamp record", "__MONOTONIC_TIMESTAMP": "62000004"}
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
        "earlyoom.actions.sigkill": 0,
        "earlyoom.actions.escalations": 1,
        "earlyoom.actions.kill_failed": 0,
        "earlyoom.actions.low_memory_warnings": 0,
        "earlyoom.process_group_lines": 0,
        "earlyoom.earlier_invocation_send_lines": 0,
        "oomd.state": "inactive",
        "oomd.notices_this_boot": 0
      }
    }
  },
  {
    "id": "r29-a2-10-whitespace-and-missing",
    "rule": "A2-10",
    "author": "CaseA210d",
    "why": "A2-10 says a record without a numeric __MONOTONIC_TIMESTAMP is left uncounted and makes scope incomplete (round-27/contract.md:58; round-26/contract.md:186-188), so the whitespace and missing-key records make the scope incomplete. The ordinary numeric record at 73999999 is before the invocation boundary, while the version and dry-run records at 74000000 and 74000001 are in scope (round-26/contract.md:78-82). The active state, version, grammar, and declared output fields follow round-26/contract.md:82,90-95. The dry-run marker makes dryrun true and the absence of sends leaves dryrun_send_lines and SIGTERM/SIGKILL at zero (round-27/contract.md:53; round-26/contract.md:166-167). The other numeric records contain no action, failure, warning, process-group, or earlier-invocation send/escalation pattern (round-26/contract.md:85-89; round-27/contract.md:51,54), so those counts are zero. With no positive evidence, active earlyoom and incomplete scope produce KILLERS_UNKNOWN, exit 2 (round-26/contract.md:97-101).",
    "inputs": {
      "earlyoom_show": "LoadState=loaded\nActiveState=active\nUnitFileState=enabled\nActiveEnterTimestampMonotonic=74000000\n",
      "oomd_show": "LoadState=loaded\nActiveState=inactive\nUnitFileState=disabled\nActiveEnterTimestampMonotonic=0\n",
      "earlyoom_journal": [
        {"MESSAGE": "ordinary pre-scope record", "__MONOTONIC_TIMESTAMP": "73999999"},
        {"MESSAGE": "earlyoom 1.9.0", "__MONOTONIC_TIMESTAMP": "74000000"},
        {"MESSAGE": "dryrun mode enabled, will not kill anything", "__MONOTONIC_TIMESTAMP": "74000001"},
        {"MESSAGE": "whitespace-stamp record", "__MONOTONIC_TIMESTAMP": "   "},
        {"MESSAGE": "missing-stamp record"},
        {"MESSAGE": "ordinary numeric-stamp record", "__MONOTONIC_TIMESTAMP": "74000003"}
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
        "earlyoom.dryrun_send_lines": 0,
        "earlyoom.process_group_lines": 0,
        "earlyoom.earlier_invocation_send_lines": 0,
        "oomd.state": "inactive",
        "oomd.notices_this_boot": 0
      }
    }
  }
]
```

## Per-case derivations

### r29-a2-10-empty-and-letters

| Field | Value | Contract line |
|---|---|---|
| verdict | KILLERS_UNKNOWN | round-26/contract.md:97,99-101 |
| exit | 2 | round-26/contract.md:99-101 |
| earlyoom.state | active | round-26/contract.md:90-95 |
| earlyoom.version | 1.9.0 | round-26/contract.md:82,90-95 |
| earlyoom.grammar | verified-1.9.0 | round-26/contract.md:82,91 |
| earlyoom.scope_complete | false | round-27/contract.md:58; round-26/contract.md:186-188 |
| earlyoom.actions.{sigterm,sigkill,escalations,kill_failed,low_memory_warnings} | 0 each | round-26/contract.md:85-89; round-27/contract.md:53 |
| earlyoom.dryrun | true | round-27/contract.md:53; round-26/contract.md:166-167 |
| earlyoom.dryrun_send_lines | 0 | round-27/contract.md:53 |
| earlyoom.process_group_lines | 0 | round-27/contract.md:51 |
| earlyoom.earlier_invocation_send_lines | 0 | round-27/contract.md:54 |
| oomd.state | inactive | round-26/contract.md:90-95 |
| oomd.notices_this_boot | 0 | round-26/contract.md:95 |

### r29-a2-10-negative-and-decimal

| Field | Value | Contract line |
|---|---|---|
| verdict | KILLER_ACTED | round-26/contract.md:86,97-98 |
| exit | 1 | round-26/contract.md:97-98 |
| earlyoom.state | active | round-26/contract.md:90-95 |
| earlyoom.version | 1.9.0 | round-26/contract.md:82,90-95 |
| earlyoom.grammar | verified-1.9.0 | round-26/contract.md:82,91 |
| earlyoom.scope_complete | false | round-27/contract.md:58; round-26/contract.md:186-188 |
| earlyoom.actions.sigterm | 0; earlyoom.actions.sigkill | 0; earlyoom.actions.escalations | 1; earlyoom.actions.kill_failed | 0; earlyoom.actions.low_memory_warnings | 0 | round-26/contract.md:85-88; round-27/contract.md:58; round-26/contract.md:97-98 |
| earlyoom.process_group_lines | 0 | round-27/contract.md:51 |
| earlyoom.earlier_invocation_send_lines | 0 | round-27/contract.md:54 |
| oomd.state | inactive | round-26/contract.md:90-95 |
| oomd.notices_this_boot | 0 | round-26/contract.md:95 |

### r29-a2-10-whitespace-and-missing

| Field | Value | Contract line |
|---|---|---|
| verdict | KILLERS_UNKNOWN | round-26/contract.md:97,99-101 |
| exit | 2 | round-26/contract.md:99-101 |
| earlyoom.state | active | round-26/contract.md:90-95 |
| earlyoom.version | 1.9.0 | round-26/contract.md:82,90-95 |
| earlyoom.grammar | verified-1.9.0 | round-26/contract.md:82,91 |
| earlyoom.scope_complete | false | round-27/contract.md:58; round-26/contract.md:186-188 |
| earlyoom.actions.{sigterm,sigkill,escalations,kill_failed,low_memory_warnings} | 0 each | round-26/contract.md:85-89; round-27/contract.md:53 |
| earlyoom.dryrun | true | round-27/contract.md:53; round-26/contract.md:166-167 |
| earlyoom.dryrun_send_lines | 0 | round-27/contract.md:53 |
| earlyoom.process_group_lines | 0 | round-27/contract.md:51 |
| earlyoom.earlier_invocation_send_lines | 0 | round-27/contract.md:54 |
| oomd.state | inactive | round-26/contract.md:90-95 |
| oomd.notices_this_boot | 0 | round-26/contract.md:95 |

**Not pinned:** `earlyoom.thresholds` in all cases: no threshold messages are supplied, and the contract gives no default for their absence. In case 2, `earlyoom.dryrun` and `earlyoom.dryrun_send_lines` are also omitted because the contract specifies the dry-run path after a dry-run marker, and none is present. All other contract-decided output fields are pinned.

## Opened files, source URLs, and evidence

- Contract: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-27/contract.md` (requested :40-80; range rendering also showed context lines 39 and 81-83).
- Contract: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-26/contract.md` (:1-190; whole spec and A2).
- Fixtures: `/home/vgpnk/Projects/shokunin/mori-shokunin/tools/fixtures/mori-oom-killers/cases.json` (:1-8 and :6-44) and `.../cases-a2.json` (:1-11). The fixture reads also surfaced the first example's why/expect text beyond schema/journal shapes; those values were not used to derive these expectations. Range rendering showed collapsed case extents.
- Required instructions read: `/home/vgpnk/.omp/agent/RULES.md` (:1-14) and `/home/vgpnk/.agents/skills/godspeed/SKILL.md` (via `skill://godspeed`).
- Scratch sources fetched by curl and hashed at `2026-10-22T19:55:48Z` (SHA-256 of fetched bytes): [main.c](https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/main.c) `08656b0bc90c85f23738661456b25c97af908bc5e2cfea78e0a69697b5f9d0e4`; [kill.c](https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/kill.c) `b32e0fad65e298235102f98aff37e02c94400b544d454cb57192ae697b100bf3`; [msg.h](https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/msg.h) `e36604984a916fb00a624c27c73034bcd87d7d6facff9b290a6a561ee58de56c`; [MANPAGE.md](https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/MANPAGE.md) `cc48b02e79255ae27bad9b2c49364fcae1b6b5eb20fe8e83ecef432f360dfeda`; [systemd.journal-fields.html](https://www.freedesktop.org/software/systemd/man/latest/systemd.journal-fields.html) `906e5d34b38913ddaf729f74f468f5511f8a143bb3f86f0fdda06957af7bf5e7`.
- Upstream format quotes, each verbatim and under 25 words: `main.c:161` — `fprintf(stderr, "earlyoom " VERSION "\n");`; `main.c:295` — `warn("dryrun mode enabled, will not kill anything\n");`; `kill.c:318` — `warn("escalating to SIGKILL after %.3f seconds\n", secs);`; systemd docs `:207-210` — “The monotonic time (CLOCK_MONOTONIC) at the point in time the entry was received by the journal in microseconds, formatted as a decimal.”
- Fetched source files in scratch: `/fast/scratch/hyaku/mori-r29/CaseA210d/main.c` (:159-165, :294-298, :413-417), `kill.c` (:317-321, :618-630), `msg.h` (:1-18), and `systemd.journal-fields.html` (:200-216); `MANPAGE.md` was fetched but not read. Created `/fast/scratch/hyaku/mori-r29/CaseA210d/cases-a2-10.json`; `python3` `json.load` validated it: `VALID JSON: 3 cases; ids=r29-a2-10-empty-and-letters, r29-a2-10-negative-and-decimal, r29-a2-10-whitespace-and-missing`.
- No tool was installed or updated. I did not open or run `tools/mori-oom-killers.py`, did not view any of its output or a self-test, and opened no other report.
