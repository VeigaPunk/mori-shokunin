# CaseA207d — A2-07 blind cases

## Cases

```json
[
  {
    "id": "r29-a2-07-dryrun-before-real-signals",
    "rule": "A2-07",
    "author": "CaseA207d",
    "why": "A2-07 (round-27/contract.md:55) splits at each version line, so the earlier dry-run marker applies only to its own invocation. The current version line is at ActiveEnterTimestampMonotonic (round-26/contract.md:78,82); its SIGTERM and SIGKILL lines are in scope and each is one action (round-26/contract.md:85). In-scope sends mean KILLER_ACTED/exit 1 (round-26/contract.md:96-98), regardless of the other invocation's dry-run sends.",
    "inputs": {
      "earlyoom_show": "LoadState=loaded\nActiveState=active\nUnitFileState=enabled\nActiveEnterTimestampMonotonic=60000000\n",
      "oomd_show": "LoadState=loaded\nActiveState=inactive\nUnitFileState=disabled\nActiveEnterTimestampMonotonic=0\n",
      "earlyoom_journal": [
        {"MESSAGE": "earlyoom 1.9.0", "__MONOTONIC_TIMESTAMP": "43000000"},
        {"MESSAGE": "dryrun mode enabled, will not kill anything", "__MONOTONIC_TIMESTAMP": "43000001"},
        {"MESSAGE": "sending SIGTERM to process 73101 uid 1000 \"imaginary-sable\": oom_score 300, oom_score_adj 0, VmRSS 45 MiB, cmdline \"imaginary-sable --fixture\"", "__MONOTONIC_TIMESTAMP": "43001000"},
        {"MESSAGE": "sending SIGKILL to process 73102 uid 1000 \"imaginary-lark\": oom_score 280, oom_score_adj 0, VmRSS 41 MiB, cmdline \"imaginary-lark --fixture\"", "__MONOTONIC_TIMESTAMP": "43002000"},
        {"MESSAGE": "earlyoom 1.9.0", "__MONOTONIC_TIMESTAMP": "60000000"},
        {"MESSAGE": "sending SIGTERM to process 73103 uid 1000 \"imaginary-pollen\": oom_score 400, oom_score_adj 0, VmRSS 55 MiB, cmdline \"imaginary-pollen --fixture\"", "__MONOTONIC_TIMESTAMP": "60001000"},
        {"MESSAGE": "sending SIGKILL to process 73104 uid 1000 \"imaginary-cinder\": oom_score 390, oom_score_adj 0, VmRSS 53 MiB, cmdline \"imaginary-cinder --fixture\"", "__MONOTONIC_TIMESTAMP": "60002000"}
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
        "earlyoom.actions.sigkill": 1,
        "earlyoom.actions.escalations": 0,
        "earlyoom.actions.kill_failed": 0,
        "earlyoom.actions.low_memory_warnings": 0,
        "oomd.state": "inactive",
        "oomd.notices_this_boot": 0
      }
    }
  },
  {
    "id": "r29-a2-07-real-before-dryrun-signals",
    "rule": "A2-07",
    "author": "CaseA207d",
    "why": "A2-07 (round-27/contract.md:55) splits at each version line, so the earlier real sends stay separate from the current dry-run invocation. A2-04 (round-26/contract.md:166-167) puts current dry-run send lines in dryrun_send_lines, keeps SIGTERM/SIGKILL at zero, and excludes them as positive evidence. A2-06 (round-26/contract.md:175-179) reports earlier send lines but does not change an active earlyoom's verdict. With no other positive evidence, the result is KILLERS_QUIET/exit 0 (round-26/contract.md:96-104).",
    "inputs": {
      "earlyoom_show": "LoadState=loaded\nActiveState=active\nUnitFileState=enabled\nActiveEnterTimestampMonotonic=85000000\n",
      "oomd_show": "LoadState=loaded\nActiveState=inactive\nUnitFileState=disabled\nActiveEnterTimestampMonotonic=0\n",
      "earlyoom_journal": [
        {"MESSAGE": "earlyoom 1.9.0", "__MONOTONIC_TIMESTAMP": "72000000"},
        {"MESSAGE": "sending SIGTERM to process 84211 uid 1000 \"imaginary-cedar\": oom_score 320, oom_score_adj 0, VmRSS 48 MiB, cmdline \"imaginary-cedar --fixture\"", "__MONOTONIC_TIMESTAMP": "72001000"},
        {"MESSAGE": "sending SIGKILL to process 84212 uid 1000 \"imaginary-mica\": oom_score 310, oom_score_adj 0, VmRSS 46 MiB, cmdline \"imaginary-mica --fixture\"", "__MONOTONIC_TIMESTAMP": "72002000"},
        {"MESSAGE": "earlyoom 1.9.0", "__MONOTONIC_TIMESTAMP": "85000000"},
        {"MESSAGE": "dryrun mode enabled, will not kill anything", "__MONOTONIC_TIMESTAMP": "85000001"},
        {"MESSAGE": "sending SIGTERM to process 84213 uid 1000 \"imaginary-fern\": oom_score 270, oom_score_adj 0, VmRSS 39 MiB, cmdline \"imaginary-fern --fixture\"", "__MONOTONIC_TIMESTAMP": "85001000"},
        {"MESSAGE": "sending SIGKILL to process 84214 uid 1000 \"imaginary-flint\": oom_score 260, oom_score_adj 0, VmRSS 37 MiB, cmdline \"imaginary-flint --fixture\"", "__MONOTONIC_TIMESTAMP": "85002000"}
      ],
      "oomd_notices": 0
    },
    "expect": {
      "verdict": "KILLERS_QUIET",
      "exit": 0,
      "fields": {
        "earlyoom.state": "active",
        "earlyoom.version": "1.9.0",
        "earlyoom.grammar": "verified-1.9.0",
        "earlyoom.scope_complete": true,
        "earlyoom.actions.sigterm": 0,
        "earlyoom.actions.sigkill": 0,
        "earlyoom.actions.escalations": 0,
        "earlyoom.actions.kill_failed": 0,
        "earlyoom.actions.low_memory_warnings": 0,
        "earlyoom.dryrun_send_lines": 2,
        "earlyoom.earlier_invocation_send_lines": 2,
        "oomd.state": "inactive",
        "oomd.notices_this_boot": 0
      }
    }
  },
  {
    "id": "r29-a2-07-all-dryrun-multiple-sends",
    "rule": "A2-07",
    "author": "CaseA207d",
    "why": "A2-07 (round-27/contract.md:55) applies dry-run to each version-delimited invocation. Both invocations here have a dry-run marker; the current invocation has two SIGTERM and two SIGKILL send lines. A2-04 (round-26/contract.md:166-167) therefore counts four current dry-run send lines, leaves both real-action counts at zero, and treats none as positive evidence. The earlier invocation has no send lines. With no other positive evidence, the complete active scope is KILLERS_QUIET/exit 0 (round-26/contract.md:96-104).",
    "inputs": {
      "earlyoom_show": "LoadState=loaded\nActiveState=active\nUnitFileState=enabled\nActiveEnterTimestampMonotonic=93000000\n",
      "oomd_show": "LoadState=loaded\nActiveState=inactive\nUnitFileState=disabled\nActiveEnterTimestampMonotonic=0\n",
      "earlyoom_journal": [
        {"MESSAGE": "earlyoom 1.9.0", "__MONOTONIC_TIMESTAMP": "88000000"},
        {"MESSAGE": "dryrun mode enabled, will not kill anything", "__MONOTONIC_TIMESTAMP": "88000001"},
        {"MESSAGE": "earlyoom 1.9.0", "__MONOTONIC_TIMESTAMP": "93000000"},
        {"MESSAGE": "dryrun mode enabled, will not kill anything", "__MONOTONIC_TIMESTAMP": "93000001"},
        {"MESSAGE": "sending SIGTERM to process 95321 uid 1000 \"imaginary-ash\": oom_score 350, oom_score_adj 0, VmRSS 52 MiB, cmdline \"imaginary-ash --fixture\"", "__MONOTONIC_TIMESTAMP": "93001000"},
        {"MESSAGE": "sending SIGTERM to process 95322 uid 1000 \"imaginary-birch\": oom_score 340, oom_score_adj 0, VmRSS 50 MiB, cmdline \"imaginary-birch --fixture\"", "__MONOTONIC_TIMESTAMP": "93002000"},
        {"MESSAGE": "sending SIGKILL to process 95323 uid 1000 \"imaginary-opal\": oom_score 330, oom_score_adj 0, VmRSS 48 MiB, cmdline \"imaginary-opal --fixture\"", "__MONOTONIC_TIMESTAMP": "93003000"},
        {"MESSAGE": "sending SIGKILL to process 95324 uid 1000 \"imaginary-garnet\": oom_score 320, oom_score_adj 0, VmRSS 46 MiB, cmdline \"imaginary-garnet --fixture\"", "__MONOTONIC_TIMESTAMP": "93004000"}
      ],
      "oomd_notices": 0
    },
    "expect": {
      "verdict": "KILLERS_QUIET",
      "exit": 0,
      "fields": {
        "earlyoom.state": "active",
        "earlyoom.version": "1.9.0",
        "earlyoom.grammar": "verified-1.9.0",
        "earlyoom.scope_complete": true,
        "earlyoom.actions.sigterm": 0,
        "earlyoom.actions.sigkill": 0,
        "earlyoom.actions.escalations": 0,
        "earlyoom.actions.kill_failed": 0,
        "earlyoom.actions.low_memory_warnings": 0,
        "earlyoom.dryrun_send_lines": 4,
        "earlyoom.earlier_invocation_send_lines": 0,
        "oomd.state": "inactive",
        "oomd.notices_this_boot": 0
      }
    }
  }
]
```

## Per-case derivation

Contract references below are relative to `round-26/contract.md` and `round-27/contract.md` in the lane.

### `r29-a2-07-dryrun-before-real-signals`

| Field | Value | Contract line(s) |
|---|---:|---|
| `expect.verdict` | `KILLER_ACTED` | r26:96-98 — in-scope send lines are positive evidence |
| `expect.exit` | `1` | r26:96-98 |
| `earlyoom.state` | `active` | r27:50; r26:90-95 |
| `earlyoom.version` | `1.9.0` | r26:82, 90-95 |
| `earlyoom.grammar` | `verified-1.9.0` | r26:80-90 — the invocation has the recognized 1.9.0 version line and send grammar |
| `earlyoom.scope_complete` | `true` | r26:78-79, 93-95; current version timestamp equals the inclusive active-enter boundary |
| `earlyoom.actions.sigterm` | `1` | r26:85; r27:55; only current invocation's real SIGTERM is counted |
| `earlyoom.actions.sigkill` | `1` | r26:85; r27:55; only current invocation's real SIGKILL is counted |
| `earlyoom.actions.escalations` | `0` | r26:87; no escalation line occurs |
| `earlyoom.actions.kill_failed` | `0` | r26:87; no failed-kill line occurs |
| `earlyoom.actions.low_memory_warnings` | `0` | r26:88; no warning line occurs |
| `oomd.state` | `inactive` | r26:95, 102-104 |
| `oomd.notices_this_boot` | `0` | r26:95, 102-104; input count is zero |

Not pinned: `earlyoom.dryrun` has no defined multi-invocation aggregation semantics in the contract. `earlyoom.thresholds` is omitted because there are no threshold records and the contract does not specify the no-record value. The contract does not say whether dry-run sends from an earlier invocation also appear in `dryrun_send_lines` or `earlier_invocation_send_lines`, so neither is pinned here.

### `r29-a2-07-real-before-dryrun-signals`

| Field | Value | Contract line(s) |
|---|---:|---|
| `expect.verdict` | `KILLERS_QUIET` | r26:96-104; dry-run sends are not positive evidence and earlier sends do not change an active earlyoom verdict |
| `expect.exit` | `0` | r26:96-104 |
| `earlyoom.state` | `active` | r27:50; r26:90-95 |
| `earlyoom.version` | `1.9.0` | r26:82, 90-95 |
| `earlyoom.grammar` | `verified-1.9.0` | r26:80-90 |
| `earlyoom.scope_complete` | `true` | r26:78-79, 93-95; current version timestamp equals the inclusive active-enter boundary |
| `earlyoom.actions.sigterm` | `0` | r26:166-167; current invocation is dry-run |
| `earlyoom.actions.sigkill` | `0` | r26:166-167; current invocation is dry-run |
| `earlyoom.actions.escalations` | `0` | r26:87; no escalation line occurs |
| `earlyoom.actions.kill_failed` | `0` | r26:87; no failed-kill line occurs |
| `earlyoom.actions.low_memory_warnings` | `0` | r26:88; no warning line occurs |
| `earlyoom.dryrun_send_lines` | `2` | r26:166-167; two current-invocation send lines follow its dry-run marker |
| `earlyoom.earlier_invocation_send_lines` | `2` | r26:175-179; two earlier real send lines are outside the current invocation |
| `oomd.state` | `inactive` | r26:95, 102-104 |
| `oomd.notices_this_boot` | `0` | r26:95, 102-104; input count is zero |

Not pinned: `earlyoom.dryrun` aggregation semantics and `earlyoom.thresholds` with no threshold records are unspecified by the contract.

### `r29-a2-07-all-dryrun-multiple-sends`

| Field | Value | Contract line(s) |
|---|---:|---|
| `expect.verdict` | `KILLERS_QUIET` | r26:96-104; all current send lines are dry-run and no other positive evidence exists |
| `expect.exit` | `0` | r26:96-104 |
| `earlyoom.state` | `active` | r27:50; r26:90-95 |
| `earlyoom.version` | `1.9.0` | r26:82, 90-95 |
| `earlyoom.grammar` | `verified-1.9.0` | r26:80-90 |
| `earlyoom.scope_complete` | `true` | r26:78-79, 93-95; current version timestamp equals the inclusive active-enter boundary |
| `earlyoom.actions.sigterm` | `0` | r26:166-167; current invocation is dry-run |
| `earlyoom.actions.sigkill` | `0` | r26:166-167; current invocation is dry-run |
| `earlyoom.actions.escalations` | `0` | r26:87; no escalation line occurs |
| `earlyoom.actions.kill_failed` | `0` | r26:87; no failed-kill line occurs |
| `earlyoom.actions.low_memory_warnings` | `0` | r26:88; no warning line occurs |
| `earlyoom.dryrun_send_lines` | `4` | r26:166-167; four current-invocation send lines follow its dry-run marker |
| `earlyoom.earlier_invocation_send_lines` | `0` | r26:175-179; earlier invocation has no send lines |
| `oomd.state` | `inactive` | r26:95, 102-104 |
| `oomd.notices_this_boot` | `0` | r26:95, 102-104; input count is zero |

Not pinned: `earlyoom.dryrun` aggregation semantics and `earlyoom.thresholds` with no threshold records are unspecified by the contract.

## Opened files and source evidence

### Lane files

- `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-27/contract.md` — requested range 40-80 for A2 rules.
- `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-26/contract.md` — whole file, including output rules and Amendment A2.
- `/home/vgpnk/Projects/shokunin/mori-shokunin/tools/fixtures/mori-oom-killers/cases.json` — opened while inspecting schema and journal record shapes.
- `/home/vgpnk/Projects/shokunin/mori-shokunin/tools/fixtures/mori-oom-killers/cases-a2.json` — opened around 794-955 while inspecting journal record shapes.
- `/fast/scratch/hyaku/mori-r29/CaseA207d/cases.json` — my draft; loaded by the JSON validation command below.

**Scope deviation:** the `cases-a2.json` read and searches over the fixture files displayed existing `expect`/verdict snippets, beyond the allowed schema and journal-line-shape inspection. I did not copy those cases; the tables cite the contracts for each expected value. Because I saw the snippets before drafting, I cannot guarantee they did not influence case selection or design, and cannot certify a clean blind process. L1 should decide whether to accept or discard this draft for the blind claim.

### Upstream sources fetched with `curl`

- `https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/main.c` — fetched 2026-10-22T19:55:31Z; SHA-256 `08656b0bc90c85f23738661456b25c97af908bc5e2cfea78e0a69697b5f9d0e4`. Quotes: line 161, `"earlyoom " VERSION "\n"`; line 295, `warn("dryrun mode enabled, will not kill anything\n");`.
- `https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/kill.c` — fetched 2026-10-22T19:55:32Z; SHA-256 `b32e0fad65e298235102f98aff37e02c94400b544d454cb57192ae697b100bf3`. Quotes: line 272, `warn("dryrun, not actually sending any signal\n");`; line 627, `warn("sending %s to process %d uid %d \"%s\": oom_score %d, oom_score_adj %d, VmRSS %lld MiB, cmdline \"%s\"\n",`.
- `https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/msg.h` — fetched 2026-10-22T19:55:32Z; SHA-256 `e36604984a916fb00a624c27c73034bcd87d7d6facff9b290a6a561ee58de56c`. Quote: line 10, `#define PRIPCT "%5.2lf%%"`.
- `https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/MANPAGE.md` — fetched 2026-10-22T19:55:32Z; SHA-256 `cc48b02e79255ae27bad9b2c49364fcae1b6b5eb20fe8e83ecef432f360dfeda`. Quote: line 206, `dry run (do not kill any processes)`.
- `https://www.freedesktop.org/software/systemd/man/latest/journalctl.html` — fetched 2026-10-22T19:55:31Z; SHA-256 `75440570fb1f71859229ca88fed0a6764b2057c7dd90651701b3d022a5649722`. Fetched and hashed; not inspected for a quote.
- `https://raw.githubusercontent.com/systemd/systemd/main/man/journalctl.xml` — fetched 2026-10-22T19:55:41Z; SHA-256 `d54bbede45d5b1e3dc856da9624649ef8cb0829731597c212be303a76a1edbdd`. Quote: line 587, `formats entries as JSON objects, separated by newline characters`.
- `https://raw.githubusercontent.com/systemd/systemd/main/man/systemd.journal-fields.xml` — fetched 2026-10-22T19:55:41Z; SHA-256 `0af0086ce0e4f4b0a99cb22c6be8d8a7c5ef6e8c19227c3b0191aee58de56c`. Quote: lines 670-671, `the entry was received by the journal in microseconds, formatted as a decimal.`

## Validation and limits

- Required JSON parse: `python3 -c 'import json; data=json.load(open("cases.json")); print(f"valid JSON: {len(data)} cases")'` from `/fast/scratch/hyaku/mori-r29/CaseA207d` printed `valid JSON: 3 cases`.
- No tool was installed or updated. No build, test, lint, or formatter was run.
- I did not open or run `tools/mori-oom-killers.py`, run a self-test, read output produced by that tool, or open another seat report. The only tool-like output examined was the required Python JSON parse result.
