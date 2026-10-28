# Mo59Scout54 — settlement/results JSON shape census (.ufo/waves/)

Read-only reconnaissance. Seat spec: enumerate distinct top-level key sets and
member key sets across all committed `*-results.json` and `*settlement*.json`
under `.ufo/waves/`; report a shape census table. No commits, no VCS mutation,
no production/corpus edits. Lane revision surveyed: entering
`2b9f03975bfb6e508f35074ac8181ec8bf54e805` worktree (`git status --porcelain`
shows only untracked round-59 wave files; no uncommitted results/settlement JSON).

Contract/counters read first: `.ufo/waves/round-59/contract.md`,
`.ufo/waves/round-59/count-c1.py`, `.ufo/waves/round-59/count-c2.py`
(freeze `60b3a76ad0524c8978cc51922940be1c8c388915`).

## Enumeration (commands)

```
git -C /home/vgpnk/Projects/shokunin/mori-shokunin ls-files '.ufo/waves/' \
  | grep -E '(-results\.json|settlement.*\.json)$' | sort
```

→ 25 committed files: 14 `*-results.json` seat-roster files, 2 bounded
mutation-probe results (r23), 9 `*settlement*.json` artifacts (r17–r22, r58).

## Shape census — A. `*-results.json` wave-results family (orchestrator C2 target)

Top-level key sets (distinct = 2):

| Top-level key set (sorted) | Files |
|---|---|
| `{lane, round, wave, seats, results}` | r47 w1, r47 w2, r48 w1, r48 w2, r50 a2w1, r51 w1, r52 w1, r53 a2r1, r54 w1, r55 w1, r56 w1, r57 w1, r58 w1 (13 files) |
| `{lane, round, wave, seats, spawned, outputs_recovered, settled_by, note, results}` | r53 w1 only (1 file) |

r53 w1 extra keys located: line 8 `"settled_by": "orchestrator session exit (no seat live)"`,
plus `spawned`/`outputs_recovered`/`note` (SIGHUP-killed orchestrator session;
outputs recovered from transcript).

Member (`results[]`) key sets (distinct = 2):

| Member key set | Files | Members |
|---|---|---|
| `{agent, name, note, output}` | all 13 canonical files | 788 total; uniform within every file |
| `{agent, name, note, output, report_file}` | r53 w1 only | 67 members, all carry `report_file` |

Quote: `   "report_file": ".ufo/waves/round-53/w1/Mo53Fr01.md"`
(`.ufo/waves/round-53/w1-results.json:16`; same key on all 67 members).

Member field typing:

- `name`: unique within every file (0 duplicate names anywhere).
- `agent`: role enum union across all files = `{connector, critic, executor,
  mutation-tester, reviewer, scribe, scout, sentinel, simplifier, revenger}`
  (10 distinct; `revenger` absent only from r47 w1/w2, r48 w1, r53 a2r1;
  `sentinel`+`simplifier` absent from r53 a2r1 which is reviewer/critic-only,
  8 seats).
- `output` / `note` polarity flips by wave: build waves carry `output: str` +
  `note: null` (r47w2, r48w1, r50a2w1, r51–r52, r53a2r1, r54–r58) while
  falsify/verdict waves carry `output: null` + `note: str` (r47w1, r48w2,
  r50a2w1 is a build-wave exception: `output: null` + `note: str`).
  r53 w1 is mixed: `output` str ×66, null ×1; `note` str ×67.

`seats` == `len(results)` in every file (verified: 42,37,49,34,64,68,68,8,
67,74,64,64,64,64).

### B. r23 bounded mutation-probe results (`bounded-results.json`)

Distinct top-level key sets (2):

| Key set | File | schema value |
|---|---|---|
| `{schema, seat, verdict, observed_base, observed_branch, expectation_seal, scratch_clone, source, production_source_not_edited, source_function, inserted_statement, insertion_point, source_sha256, detector, detector_sha256_all_three_runs, runtime, launch_prefix, runs, fixture_witness, safety, scope, tool_installs_or_updates}` (23 keys) | r23 falsify/MutModeRead/bounded-results.json | `mori-r23-mut-mode-read-summary-v1` |
| `{mutation_error, restoration, runs, schema, scope, seat, verdict}` (7 keys) | r23 falsify/MutSetupPartial/bounded-results.json | `mori-r23-mutation-probe-v1` |

Member (`runs[]`) key sets: MutModeRead — 2 shapes:
`{argv, cases_passed, cases_total, exit_code, mode_open_attempts, phase, raw_json_receipt}` ×2
and + `{failed_case, failure, observed}` variant ×1.
MutSetupPartial — 1 shape (25 keys): `{address_space_bytes, argv, case_sha256,
cpu_seconds, cwd, detector_exit, elapsed_seconds, env_overrides, fixture_sha256,
headline, oracle_sha256, parsed, phase, primary_pass, reason, source_sha256,
status, stderr, stderr_truncated, stdout, stdout_truncated, supplementary,
supplementary_pass, timeout, tool_exit, wall_timeout_seconds}`.

### C. `*settlement*.json` artifacts (4 distinct families)

| Top-level key set | schema | Files |
|---|---|---|
| `{waves, total_unique_seats, planner, build_jobcap_refusals, falsify_jobcap_refusals, resumed_writers, routing}` | (none) | r17 wave-settlement.json |
| `{schema, wave, returned_agent_ids, native_calls, reports_present, known_provider_failed, known_cancelled, no_report_terminal_cause_unestablished, error_classes, replacements, limits}` | `mori-wave-settlement-v1` | r19 wave1-settlement.json |
| `{schema, wave, native_calls, returned_agent_ids, reports_present, provider_failed_no_report, error_classes, replacements, slot_released, reports_are_author_side_not_independent_closure}` | `mori-wave-settlement-v1` | r19 wave2-settlement.json |
| `{ignored_json, lane_root, schema, totals, unreadable_json, waves}` | `mori-wave-settlement-v1` | r20 wave1-settlement-scan.json, r21 wave-settlement-observed.json, r22 settlement-final.json, r22 settlement-wave1.json, r58 w1-settlement.json |
| `{schema, measured_revision, argv, cwd, started_utc, elapsed_seconds, exit_code, stdout, stderr}` | `mori-r21-command-receipt-v1` | r21 final/wave-settlement.json (a wrapped command receipt whose `stdout` embeds a `mori-wave-settlement-v1` scan) |

Quotes: `  "total_unique_seats": 134,` / `  "planner": "MoriR17 L1",`
(r17 wave-settlement.json:40-41); `  "schema": "mori-r21-command-receipt-v1",`
(r21 final/wave-settlement.json:2); r58 w1-settlement.json:1
`{"ignored_json":1719,…,"schema":"mori-wave-settlement-v1",…,"waves":62}}`.

Scanner-scan member key sets (`waves[].members[]`): exactly one shape across
all 5 scan files — `{agent, name, status}` ×6486 members; `status` ∈
`{present: 5626, missing: 852, stub: 8}`.
`waves[]` element keys uniform ×116 waves: `{counts, dispatch_path,
dispatch_sha256, duplicate_of, duplicate_report_paths, members, missing,
name_hint, state, wave}` (10 keys); `state` ∈ `{settled: 68, partial: 47,
unsettled: 1}`; `counts` keys uniform `{empty, misrooted, missing, present,
stub, unparsed, unsafe}`; `missing[]` elements are bare strings.
`totals` keys uniform ×5 files: `{empty, members, misrooted, missing,
name_hinted_waves, present, states, stub, unique_dispatch_sha256, unparsed,
unsafe, waves}` (12 keys); `totals.states` sub-keys differ: r22
settlement-wave1 has `{partial, settled, unsettled}`, others `{partial,
settled}`.
Wave counts per scan file: r20→11, r21→13, r22→15+15, r58→62 (mori-r13-build
… r58; full monotonic accumulation).

Rounds with NO committed results/settlement artifact under `.ufo/waves/`:
24–46 except r23 probes, r49, r59 (round-59 has only untracked w1 dispatch
files; settlement coverage lives inside the r58 cumulative scan instead —
per-wave dispatch-derived, not seat-roster results).

## Contract binding (C2)

Contract (`contract.md:58-66`) claims `tools/mori-settlement-scan.py` validates
`object/seats==members/member key-set/name-unique/role enum` over
`*-results.json` artifacts; `count-c2.py:69` `REAL_SCAN` = the five
r54–r58 w1-results files (all shape `{agent,name,note,output}`,
`seats==len(results)`, unique names, roles ⊆ the 10-role union — consistent
with met). `count-c2.py:76` `DRIFT_SCAN` = `.ufo/waves/round-53/w1-results.json`
— census confirms both drift arms: top-level extra keys
(`spawned/outputs_recovered/settled_by/note`) AND the `report_file` member
extra key (line 16 and all 67 members), matching contract note "`report_file`
extra keys — schema drift, reported not fixed" (`contract.md:78-79`).

## Confidence / gaps

- Confident: key-set census is exhaustive over committed files (`git ls-files`
  + full JSON parse of all 25; no parse errors).
- `note`/`output` typing observed via parsed types; not byte-quoted per member.
- Not resolved (out of scope): whether dispatch.json files (excluded by
  pattern) share any shape; `missing[]` name formats inside scans.
- Remaining unknowns: none blocking; C2 scan/DRIFT arms corroborated.

Report: .ufo/waves/round-59/w1/Mo59Scout54.md
