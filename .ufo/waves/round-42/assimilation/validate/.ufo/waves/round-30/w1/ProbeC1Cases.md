# Probe C1 cases — round 30

## Scope and execution

- Read C1 conditions in `.ufo/waves/round-30/contract.md:23-42` and invocation scope/A2 rules in `.ufo/waves/round-30/rule-text.md:25-26,67-99,101-114`.
- Enumerated case IDs from `tools/fixtures/mori-oom-killers/cases.json` (32), `cases-supplementary.json` (32), and `cases-a2.json` (30) using the `cases[].id` JSON query. The 13 selected IDs below cover the requested shapes; the supplementary file had no additional needed shape.
- For each selected case, wrote its `inputs` object to `/fast/scratch/hyaku/mori-r30/ProbeC1Cases/<case-id>.inputs.json`, then ran `python3 -I -B /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-oom-killers.py --inputs /fast/scratch/hyaku/mori-r30/ProbeC1Cases/<case-id>.inputs.json`.
- Compared the command return code with `expect.exit`, output `verdict` with `expect.verdict`, and every key in `expect.fields` with its output value. Captured runner result: `ALL_CASES_MATCH=True COUNT=13` (output of the selected-case runner). Fields shown below are from `expect.fields` and matched the tool output.
- No tools were installed or updated.

## Ready-to-paste decision table

```markdown
| shape | verdict | fields | case | sources |
|---|---|---|---|---|
| Bounded invocation: send exactly at the inclusive ActiveEnterTimestampMonotonic | KILLER_ACTED | `earlyoom.actions.sigterm=1`; `earlyoom.scope_complete=true`; `earlyoom.state="active"` | `c03-scope-boundary-exactly-at` — cases.json | S??? |
| Bounded invocation: send one microsecond before the stamp | KILLERS_QUIET | `earlyoom.actions.sigterm=0`; `earlyoom.scope_complete=true`; `earlyoom.state="active"` | `c02-scope-boundary-one-microsecond-before` — cases.json | S??? |
| Version line one microsecond before the stamp; later in-scope send still counts | KILLER_ACTED | `earlyoom.actions.sigterm=1`; `earlyoom.scope_complete=false`; `earlyoom.grammar="unverified"` | `c04-incomplete-scope-with-action` — cases.json | S??? |
| Version line outside scope, with no in-scope action | KILLERS_UNKNOWN | `earlyoom.scope_complete=false`; `earlyoom.grammar="unverified"`; `earlyoom.state="active"` | `c05-incomplete-scope-without-action` — cases.json | S??? |
| Active unit with zero start stamp and no send lines | KILLERS_UNKNOWN | `earlyoom.scope_complete=false`; `earlyoom.dryrun=false`; `earlyoom.state="active"` | `a2-05-monotonic-zero-active-quiet` — cases-a2.json | S??? |
| Missing start stamp; journal has an escalation, and OOMD notices are positive | KILLER_ACTED | `earlyoom.scope_complete=false`; `oomd.notices_this_boot=3`; `oomd.state="active"` | `a2-05-monotonic-missing-active-oomd-notices` — cases-a2.json | S??? |
| Inactive earlyoom with sends in earlier invocation(s) | KILLER_ACTED | `earlyoom.actions=null`; `earlyoom.earlier_invocation_send_lines=3`; `earlyoom.state="inactive"` | `a2-06-inactive-earlier-invocation-sends-acted` — cases-a2.json | S??? |
| Earlier dry-run invocation adjacent to a current real invocation | KILLER_ACTED | `earlyoom.actions.sigterm=1`; `earlyoom.actions.escalations=1`; `earlyoom.scope_complete=true` | `a2-07-earlier-dryrun-then-current-real` — cases-a2.json | S??? |
| A2-10: action record has a nonnumeric monotonic timestamp | KILLERS_UNKNOWN | `earlyoom.actions.sigterm=0`; `earlyoom.scope_complete=false`; `earlyoom.version="1.9.0"` | `a2-10-malformed-action-line-uncounted` — cases-a2.json | S??? |
| A2-01: journald suppression line inside scope | KILLERS_UNKNOWN | `earlyoom.scope_complete=false`; `earlyoom.version="1.9.0"`; `earlyoom.state="active"` | `a2-01-suppressed-in-scope-active-quiet` — cases-a2.json | S??? |
| A2-02: non-steady ActiveState=failed | KILLERS_UNKNOWN | `earlyoom.state="unavailable"`; `earlyoom.scope_complete=false`; `oomd.state="inactive"` | `a2-02-earlyoom-activestate-failed` — cases-a2.json | S??? |
| A2-08: null earlyoom journal with active earlyoom and readable oomd | KILLERS_UNKNOWN | `earlyoom.actions=null`; `earlyoom.state="active"`; `oomd.state="active"` | `a2-08-null-journal-active-earlyoom-readable-oomd` — cases-a2.json | S??? |
| A2-09: not-found unit with a send and zero start stamp | KILLER_ACTED | `earlyoom.state="absent"`; `earlyoom.scope_complete=false`; `oomd.state="inactive"` | `a2-09-removed-unit-single-sigterm-send` — cases-a2.json | S??? |
```

## Raw command outputs

These are the tool stdout and exit codes from three selected-case runs. The cases are in `tools/fixtures/mori-oom-killers/cases.json`.

### `c03-scope-boundary-exactly-at`

Command: `python3 -I -B /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-oom-killers.py --inputs /fast/scratch/hyaku/mori-r30/ProbeC1Cases/c03-scope-boundary-exactly-at.inputs.json`  
Exit code: `1`

```json
{
  "earlyoom": {
    "actions": {
      "escalations": 0,
      "kill_failed": 0,
      "low_memory_warnings": 0,
      "sigkill": 0,
      "sigterm": 1
    },
    "dryrun": false,
    "dryrun_send_lines": 0,
    "earlier_invocation_send_lines": 0,
    "grammar": "verified-1.9.0",
    "process_group_lines": 0,
    "scope_complete": true,
    "state": "active",
    "thresholds": null,
    "version": "1.9.0"
  },
  "oomd": {
    "notices_this_boot": 0,
    "state": "inactive"
  },
  "schema": "mori-oom-killers-v1",
  "verdict": "KILLER_ACTED"
}
```

### `c02-scope-boundary-one-microsecond-before`

Command: `python3 -I -B /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-oom-killers.py --inputs /fast/scratch/hyaku/mori-r30/ProbeC1Cases/c02-scope-boundary-one-microsecond-before.inputs.json`  
Exit code: `0`

```json
{
  "earlyoom": {
    "actions": {
      "escalations": 0,
      "kill_failed": 0,
      "low_memory_warnings": 0,
      "sigkill": 0,
      "sigterm": 0
    },
    "dryrun": false,
    "dryrun_send_lines": 0,
    "earlier_invocation_send_lines": 1,
    "grammar": "verified-1.9.0",
    "process_group_lines": 0,
    "scope_complete": true,
    "state": "active",
    "thresholds": null,
    "version": "1.9.0"
  },
  "oomd": {
    "notices_this_boot": 0,
    "state": "inactive"
  },
  "schema": "mori-oom-killers-v1",
  "verdict": "KILLERS_QUIET"
}
```

### `c04-incomplete-scope-with-action`

Command: `python3 -I -B /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-oom-killers.py --inputs /fast/scratch/hyaku/mori-r30/ProbeC1Cases/c04-incomplete-scope-with-action.inputs.json`  
Exit code: `1`

```json
{
  "earlyoom": {
    "actions": {
      "escalations": 0,
      "kill_failed": 0,
      "low_memory_warnings": 0,
      "sigkill": 0,
      "sigterm": 1
    },
    "dryrun": false,
    "dryrun_send_lines": 0,
    "earlier_invocation_send_lines": 0,
    "grammar": "unverified",
    "process_group_lines": 0,
    "scope_complete": false,
    "state": "active",
    "thresholds": null,
    "version": null
  },
  "oomd": {
    "notices_this_boot": 0,
    "state": "inactive"
  },
  "schema": "mori-oom-killers-v1",
  "verdict": "KILLER_ACTED"
}
```

## Risks and blockers

- No blockers. L1 must replace `S???` placeholders with the admitted source IDs, as no source evidence was part of this scoped task.
- The missing-start A2-05 case also has `oomd_notices=3`, so its `KILLER_ACTED` result does not isolate whether the earlyoom escalation alone is positive evidence; the row states this explicitly. The fixture is `tools/fixtures/mori-oom-killers/cases-a2.json`, case `a2-05-monotonic-missing-active-oomd-notices`.
