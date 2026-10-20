# OomAttack — critic review of the C1 OOM repair plan (round 14)

Seat: `MoriR14.OomAttack` (critic, leaf). Judged axis: coverage. Milestone: restore OOM alarm and structured fleet routing.
Scope: attack the CensusRepair C1 plan on the OOM paths only. Routing details (UNIT vs `_SYSTEMD_UNIT`, substring predicate) belong to RoutingAttack/FleetPredicate; I cite them only where they decide whether an OOM alarm fires.
Nothing was executed against the census, harness or journal. No files outside this report were edited. No tools were installed or updated.

## Inputs read

- `corpus/lessons/round-13-verifier-spotcheck.md` (all 140 lines; decisive items at :77-89 and :132).
- Production `tools/mori-census.sh`, SHA-256 `39abda0a…3985`, unchanged from H, git-clean at the time of reading: `probe_journal` :879-1130, `emit_finding` :392-404, verdict :1965, `DRIFT_COUNTER_KEYS` :1995-2006, drift pairing :2111-2155, journal stub :2276-2302, selftest journal cases :2738-2844, :3085-3088.
- Historical `.ufo/waves/round-13/frozen/mori-census.sh` (pre-r13, `3da5b098…`): `probe_journal` :847-912, selftest :2475-2479.
- `tools/mori-round13-regressions.py` :100-150, :1245-1310, :1853-1868.
- `corpus/knowledge/structured-journal-scopes-r13.md`, `kill-classes-by-message-id-r12.md`, `observability-census-r1.md:93-97`.
- Pinned systemd sources at `cf8ebfc6159cf0b3b99aa9a0164ccb07c4c9c5af`, fetched 2026-10-20 to `/tmp/oomattack`. Fetching is not evidence; the anchors are the raw URLs below. The catalog SHA-256 `e53707db…6592` equals the S013 pin.
  - `src/core/cgroup.c`
  - `src/core/service.c`
  - `src/core/scope.c`
  - `src/core/unit.c`
  - `src/systemd/sd-messages.h`
  - `catalog/systemd.catalog.in`

## Source facts that decide the attack

| # | Fact | Anchor |
|---|---|---|
| F1 | A kernel OOM kill seen through a unit's `memory.events`/`.local` counter makes systemd log `fe6faa94…` with the MESSAGE "The kernel OOM killer killed some processes in this unit.", and then call `unit_notify_cgroup_oom(u, false)`. | cgroup.c:3055-3105, :3097-3102 |
| F2 | A systemd-oomd kill (xattr `user.oomd_ooms`) makes systemd log `d989611b…` and then call `unit_notify_cgroup_oom(u, true)`. That is the same downstream path. | cgroup.c:3004-3053, :3039-3050 |
| F3 | For both triggers, a service or scope with `OOMPolicy` ≠ continue ends with result `SERVICE_FAILURE_OOM_KILL` / `SCOPE_FAILURE_OOM_KILL`, whose string is `"oom-kill"`. `unit_log_failure` then emits `d9b373ed…` with `UNIT_RESULT=oom-kill`. | service.c:4704-4758, :6598; scope.c:575-600, :725, :267-275; unit.c:6333-6342 |
| F4 | `OOMPolicy=continue` returns before any result change. Delegated units default to continue. Such a unit gets the `fe6faa94` notice and **no** `oom-kill` result. | service.c:1260-1261, :4712-4713; scope.c:173-174, :583-584 |
| F5 | Slices are not watched, so they produce no notice. Only units that implement `notify_cgroup_oom` (service, scope) can produce the result. | cgroup.c:2075-2078; service.c:6740; scope.c:775 |
| F6 | A kernel OOM victim dies by SIGKILL. A unit main process killed that way is logged as `98e32220…` with `EXIT_CODE=killed EXIT_STATUS=9`. | unit.c:6355-6392 |
| F7 | The subject field is chosen by manager type: the system manager writes `UNIT=` and the user manager writes `USER_UNIT=`. Both are client-supplied fields. | unit.c:6995-6997, :2579 |
| F8 | One kill fans out across scopes and units. The retained sample showed 5 kernel victim records, 7 user notices and 9 system notices. | kill-classes-by-message-id-r12.md:6, :24 |
| F9 | **The historical alarm did not fire on the `fe6faa94` notice text.** The frozen regex `Out of memory\|oom-kill\|oom_reaper\|Killed process` (frozen :874) does not match "The kernel OOM killer killed some processes in this unit." It did match `Failed with result 'oom-kill'.` (unit.c:6340), and that same line was also counted as a unit failure (frozen :890-891). It read the user journal only (frozen :855). Kernel `Out of memory: Killed process` lines are kernel-transport records, so the user journal normally does not contain them; that line appears only in the selftest fixture (frozen :2476). | frozen :849-912 |
| F10 | The host has a real case of exactly this shape: `app-Hyprland-xdg-terminal-exec-dd9e67bd.scope: Failed with result 'oom-kill'` (a non-fleet user scope). | observability-census-r1.md:93-94 |

Consequence of F9 and F10: on a live host, the faithful structured mirror of the historical alarm is **`UNIT_RESULT=oom-kill`**, not the `fe6faa94` notice. Raising the notice to crit is a wider proxy that the spec explicitly requires. Implementing the notice alarm alone silently loses the path the historical alarm actually used.

## Counterexamples against the plan

**CX1 — The notice-only alarm misses the historical path.**
The plan's headline is "positive kernel OOM notice in either scope → crit". Two inputs defeat a notice-only gate:
- An oomd-driven kill (F2→F3) produces `d989611b` plus `UNIT_RESULT=oom-kill`, and no `fe6faa94`.
- A unit whose notice was lost or rate-limited (catalog `e9bf28e6`, :58-64) can still keep its failure record.

Historically, both cases were crit because the text `oom-kill` matched. Under a notice-only repair both are CLEAN, which is a false negative and repeats the r13 harm.

Correction: `OOM_KILL_JOURNAL crit` fires when **either** `kernel_oom_notice > 0` in either scope **or** the oom-kill result subset is > 0 in either scope. Each path alone must produce DRIFT.

**CX2 — Folding subject validation into the gate turns one bad record into a lost alarm and a lost counter.**
Today every class uses a single `all(...)` validator (`JOURNAL_JQ_*`, :926-929). If CensusRepair adds `(.UNIT|type)=="string"` or `.USER_UNIT` to that `all()`, one `d9b373ed` record that lacks a subject, or carries a JSON array (S014 `json` :215, documented in structured-journal-scopes-r13.md:22), grades the whole class `record-invalid`. That has three effects:
- `unit_failure_record` becomes `unavailable`. r13 counted it without a subject, so this is a counter regression.
- The `oom-kill` alarm in the same query disappears.
- A valid fleet failure in the same query disappears.

This is the "without valid subject" trap.

Correction: the gate validates only identity fields (`_BOOT_ID`, `MESSAGE_ID`, plus `UNIT_RESULT` for the subset). Subject validity selects only the routing bucket: `fleet`, `nonfleet` or `unknown`. A record with an `oom-kill` result and an unknown subject still raises the alarm, as the parent directive also requires.

**CX3 — Deduplicating the overlap drops a finding.**
The temptation is to send `oom-kill` failures to OOM only, so the alarm is not "doubled". History counted the same line in both `c_oom` and `c_unit`/`c_unit_fleet` (frozen :874, :890-891, :904-909). If a fleet unit's `oom-kill` is removed from `UNIT_FAILURE_JOURNAL`, the fleet-failure finding is lost. If the same is done for a non-fleet unit, the tsukuroi-routed `UNIT_FAILURE_OUT_OF_SCOPE` is lost.

The reverse error also exists: suppressing `KILL_SIGNAL_JOURNAL` because OOM "explains" the SIGKILL (F6) loses the preserved generic SIGKILL warn.

Correction: the classes overlap by design.
- The `oom-kill` result count is a **subset** of `unit_failure_record`, the same pattern as `segfault_signal11` ⊂ coredump. It is never subtracted from the total.
- Fleet and non-fleet routing include `oom-kill` results.
- KILL_SIGNAL warn co-fires.

**CX4 — Treating a duplicate alarm as a duplicate kill count is false provenance.**
For one kernel kill on this host shape (F8, F10), the expected records are:
- 1 user `fe6faa94` (USER_UNIT = the scope);
- possibly 1 system `fe6faa94` (UNIT = `user@1000.service`);
- 1 user `d9b373ed` with `UNIT_RESULT=oom-kill`;
- possibly 1 user `98e32220` with `killed/9`.

The defects to watch for:
- (a) a `count=`/`total=` token that sums these (2, 3 or 4 for one kill);
- (b) one `OOM_KILL_JOURNAL` line per scope or per path, so `drift=` grows with fan-out;
- (c) wording that says "kernel OOM" when the trigger was the result path, which F2/F3 show may be oomd;
- (d) the existing subject text at :1100, "unit process exited on SIGKILL; **not an OOM** or fleet-caused kill". That is already an overclaim, because a kernel OOM victim exits on SIGKILL (F6). The honest wording is cause unknown.

Correction:
- Emit exactly **one** `OOM_KILL_JOURNAL crit` line per run, so the alarm count is 1.
- Carry separate per-scope, per-path tokens with no sum: `kernel_oom_notice` user/system and `unit_oom_kill_result` user/system, labelled `unit=notice` / `unit=record`, `victims=unmeasured`, `attribution=none`, `trust=client-supplied`.
- Name the result path "OOM kill (kernel or systemd-oomd)".
- Fix the :1100 note.

`drift=` counts alarm classes, not kills. One kill that produces OOM crit plus SIGKILL warn gives `drift=2`, and that is correct.

**CX5 — An unknown or missing `UNIT_RESULT` must not read as zero.**
A `d9b373ed` record with no `UNIT_RESULT`, a non-string value, or an array value cannot be classed as oom or non-oom. If the subset counter reports `unit_oom_kill_result=0` beside it, that is a look-alike zero (QUALITY #15/#16 spirit; the r13 note at :32 refuses partial counts).

Correction:
- Report the subset as `unavailable:result-unknown`, or report an explicit `unit_result_unknown=N` next to it.
- Keep `unit_failure_record` counted.
- If a notice is positive, the alarm still fires.

**CX6 — One failed scope or path must not mask the other.**
The per-class loop at :1088-1093 skips classes that are not ok, which keeps the classes independent. Any rewrite that gates the alarm on "all journal classes ok", or on the scope row's `st`, makes a user rc1 hide a positive system notice.

Correction: the alarm is computed per path from whatever is ok. When nothing positive is available and some path is unavailable, the surface is unavailable. There is never a crit, and never a CLEAN-looking zero.

**CX7 — Harness and fixture blind spots.**
- **Stub routing.** The stub routes on `MESSAGE_ID` alone (:2288-2293). A separate `MESSAGE_ID=d9b373ed UNIT_RESULT=oom-kill` query reads the same `journal-<scope>-unit_failure` slot as the generic failure query. A mixed slot then grades `record-invalid` under an `all(.UNIT_RESULT=="oom-kill")` filter, so a selftest can go green or red for stub reasons. Prefer one `d9b373ed` query requesting `_BOOT_ID,MESSAGE_ID,UNIT_RESULT,UNIT,USER_UNIT` and partition it inside jq. Otherwise extend the stub to key on `UNIT_RESULT=`.
- **Drift masking.** `drift_normalize` masks only keys listed in `DRIFT_COUNTER_KEYS` (:1995-2006, `\b(key)=`). New tokens such as `unit_oom_kill_result`, `fleet`, `nonfleet` or `unknown` counts must be registered there. Otherwise `--drift` reports every count change as a field change. Prefixed keys like `user_kernel_oom_notice=` do **not** match the registered `\bkernel_oom_notice`.
- **Literal scan (convenience only, not an admission criterion).** The closure's re-check scanned for the literal strings `emit_finding OOM_KILL_JOURNAL crit` and `emit_finding UNIT_FAILURE_OUT_OF_SCOPE` (spotcheck :77-79), and the spotcheck itself says identifiers alone are not evidence (:82). The behavioral cases OA01–OA18 are the primary evidence. Literal call sites only make a static re-scan read 1/1. If they are routed through `journal_finding_id`, that is fine as long as the behavioral cases pass.
- **r13 harness.** `tools/mori-round13-regressions.py:1245-1310` (`R13_C1_CLEAN_VERDICT`) still expects CLEAN with system kernel notices = 2 and forbids `OOM_KILL_JOURNAL`. Against the repaired census this goes red by design. HarnessMigration must migrate it without editing the frozen inputs.

**CX8 — System-scope alarm: a possible policy question, not a finding of harm.**
History alarmed on the user journal only (frozen :855). Raising system-scope `fe6faa94` to crit adds DRIFT for host OOM kills with no fleet tie. The r1 lesson at observability-census-r1.md:93-97 is about a cumulative parent cgroup counter causing a persistent false DRIFT. It is not a ruling against reporting a current-boot host OOM.

L1 rules that this is operator-required restoration scope: mori reports host OOM within its province and routes diagnosis to tsukuroi, with no ownership takeover. Under that reading there is no adjacency harm. Whether the boundary holds is an operator policy interpretation, not a conclusion of this critic. Do not demote the alarm. Recording the stated boundary — report and route, no tsukuroi diagnosis or remediation absorbed — keeps the reading auditable.

Optional, not required: add non-severity routing tokens (fleet/nonfleet/unknown notice counts, owner hint) to the single OOM line. Never vary its severity by subject.

## Required acceptance cases (no execution — for JournalRegression and the CensusRepair selftest)

Every case uses current-boot `_BOOT_ID` records with no `MESSAGE` key in assertions, and a canary `MESSAGE` that must not appear in stdout. Expectations are stable finding ids and tokens, independent of SUT wording.

- **Before → after:** "Frozen r13" means the census at `39abda0a…`. "Repaired" is the result after CensusRepair.
- **OOM line count:** the number of `FINDING OOM_KILL_JOURNAL` lines.
- **Six totals** means the per-scope `SURFACE journal.<scope>` tokens `kernel_oom_notice`, `oomd_notice`, `coredump_notice`, `segfault_signal11`, `unit_sigkill_record` and `unit_failure_record`. They must match the records in the fixture, unchanged from r13 semantics.

| ID | Fixture | Repaired expectation | Frozen r13 | Kills |
|---|---|---|---|---|
| OA01 | user `fe6faa94`×1 only | exactly one `OOM_KILL_JOURNAL` crit line: `user_notice=1 system_notice=0 user_unit_oom=0 system_unit_oom=0`, each byte-equal to the scope SURFACE token; no `count=`; DRIFT rc1, `drift=1` | INFO only, CLEAN rc0 (red) | notice-only, user scope |
| OA02 | system `fe6faa94`×1 only | exactly one `OOM_KILL_JOURNAL` crit line with `system_notice=1`, all other tokens 0; DRIFT rc1 | CLEAN (red) | system-scope alarm |
| OA03 | user `d9b373ed` `UNIT_RESULT=oom-kill`, valid `USER_UNIT` (non-fleet), no notice | one `OOM_KILL_JOURNAL` crit line with `user_unit_oom=1` and both notice tokens 0; `unit_failure_record=1`; `UNIT_FAILURE_OUT_OF_SCOPE` info owner tsukuroi | CLEAN, no route (red) | CX1 notice-only gate |
| OA04 | as OA03 but `UNIT`/`USER_UNIT` absent | `OOM_KILL_JOURNAL` crit still present with `user_unit_oom=1`; `unit_failure_record=1` (not unavailable); `UNIT_FAILURE_UNATTRIBUTED_JOURNAL` info `scope=user count=1 owner=unresolved reason=subject-metadata-unknown`; neither `UNIT_FAILURE_JOURNAL` nor `OUT_OF_SCOPE` | — | CX2, "without subject" |
| OA05 | as OA03 but `USER_UNIT` is a JSON array; variant: both `UNIT` and `USER_UNIT` present, even if identical | same as OA04; class not `record-invalid` | — | CX2 array/both-present poisoning |
| OA06 | one-kill fan-out: user `fe6faa94`×1, system `fe6faa94`×1, user `d9b373ed` oom-kill×1 (valid subject), user `98e32220` killed/9×1 | exactly one `OOM_KILL_JOURNAL` line with `user_notice=1 system_notice=1 user_unit_oom=1 system_unit_oom=0`; `KILL_SIGNAL_JOURNAL` warn present; verdict `drift=2`; no token valued 2 or 3 that sums scopes or paths; no other OOM id | — | CX3/CX4 alarm vs count |
| OA07 | system `d9b373ed` oom-kill with a fleet `UNIT` | one `OOM_KILL_JOURNAL` crit with `system_unit_oom=1`; `UNIT_FAILURE_JOURNAL` info count includes it | — | CX3 overlap dedup |
| OA08 | user `d9b373ed` oom-kill with a non-fleet `USER_UNIT` (F10 shape) | `OOM_KILL_JOURNAL` crit with `user_unit_oom=1`; `UNIT_FAILURE_OUT_OF_SCOPE` info owner tsukuroi | — | CX3 tsukuroi omission |
| OA09 | `d9b373ed` `UNIT_RESULT=failed` with a fleet subject only | `UNIT_FAILURE_JOURNAL` **info**; CLEAN rc0; no OOM line | — | generic fleet failure stays INFO (parent directive) |
| OA10 | `d9b373ed` with `UNIT_RESULT` absent or non-string | `unit_failure_record=1`; `unit_oom_result_unknown=1`; the oom token is never `=0` as if measured; no crit unless another path is positive | — | CX5 look-alike zero |
| OA11 | user `d9b373ed` slot rc1; system `fe6faa94`×2 | one `OOM_KILL_JOURNAL` crit with `system_notice=2` and `user_unit_oom=unavailable:rc-1`, byte-equal to the user SURFACE token | — | CX6 cross-scope masking |
| OA12 | notice slot rc1; nothing else positive | no OOM line; surface unavailable with `rc=1`; never reported as 0 | — | CX6 fake zero |
| OA13 | oom-kill record with a foreign `_BOOT_ID` | no crit; `unavailable:boot-mismatch` | — | boot control |
| OA14 | system `d989611b`×1 only, no result | no `OOM_KILL_JOURNAL` (historical parity, F9); `OOMD_NOTICE_JOURNAL_SYSTEM` info; CLEAN | — | over-alarm control |
| OA15 | legacy text only: `Out of memory: Killed process` / `Failed with result 'oom-kill'` in the fallback slot | no `OOM_KILL_JOURNAL`; canary absent (Q15, :2780-2790 guard still valid for the single id) | — | MESSAGE-free |
| OA16 | empty journal, both scopes | CLEAN rc0; all six totals = 0 in both rows; boot token present | — | baseline |
| OA17 | `d9b373ed` oom-kill and `UNIT_RESULT=failed` mixed in one scope | `unit_failure_record=2`; oom subset 1; class ok (not `record-invalid`) | — | CX7 stub/partition |
| OA18 | `--pin` then `--drift` with only the OA03 count changed (1→2) | no drift field reported for `user_notice`, `system_notice`, `user_unit_oom`, `system_unit_oom`, `unit_oom_result_unknown` or the routing counts; all of these are registered in `DRIFT_COUNTER_KEYS` | — | CX7 mask registry |
| OA19 | OA01 fixture, then OA06 fixture | the OOM line count is still 1; only the token values differ; `drift=` changes only through `KILL_SIGNAL_JOURNAL` | — | duplicate-alarm regression |

Mutation hooks for MutationDesign, red-required:
- Demote the OOM line to info: OA01, OA02 and OA03 go red.
- Drop the result path: OA03 goes red.
- Put the subject in `all()`: OA04 and OA05 go red.
- Subtract the oom subset from the unit totals: OA07 and OA08 go red.
- Emit OOM lines per scope or per source, or emit a `count=` sum: OA06 and OA19 go red.

## Impacted axes

- **coverage** (judged): CX1, CX2, CX3, CX5 and CX6 are direct false-negative paths. Each one reproduces the round-13 harm.
- **calibration:** CX4, the "not an OOM" note at :1100, and "kernel" wording on an oomd-reachable path. CX5's look-alike zero.
- **adjacency:** CX3 (tsukuroi route lost under deduplication) is a concrete defect if it happens. CX8 is a possible policy interpretation only, not a harmed axis; L1 rules it as operator-required restoration with tsukuroi routing.
- **operability:** CX7 (stub routing, `--drift` mask, r13 harness migration). The literal scan is a review convenience only.

## Smallest safe correction (summary)

1. Add one `d9b373ed` query that requests `UNIT_RESULT,UNIT,USER_UNIT`.
2. Gate that query only on boot, ID and the presence of the result field. Partition in jq into total / `oom-kill` / result-unknown and fleet / nonfleet / unknown.
3. Emit one `OOM_KILL_JOURNAL crit` when any notice in either scope is > 0 **or** any oom-kill subset is > 0. It carries unsummed per-scope, per-path tokens. A literal call site is optional; behavior is the criterion.
4. Keep:
   - the six totals and the SIGKILL warn;
   - fleet failures as `UNIT_FAILURE_JOURNAL` **info**, with `oom-kill` included;
   - non-fleet failures as `UNIT_FAILURE_OUT_OF_SCOPE info` with owner tsukuroi;
   - unknown-subject failures as an explicit unknown count.
5. Register the new counter keys in `DRIFT_COUNTER_KEYS`.
6. Reword :1100.

## Coordination

The must-have cases were sent directly to `MoriR14.CensusRepair` and `MoriR14.JournalRegression`, per the parent's request.

**L1 final ruling (relayed by CensusRepair).** CensusRepair briefly proposed one alarm row per scope and source; L1 withdrew those per-scope ids in favour of the shape below.

- **The OOM finding is one line per census:** `OOM_KILL_JOURNAL crit`.
  - It carries `user_notice`, `system_notice`, `user_unit_oom` and `system_unit_oom`, each once and each byte-equal to its scope's SURFACE token.
  - It has no `count=` sum. `drift=` counts the alarm line, not records.
  - The historical `OOM_KILL_JOURNAL` universe is the union of these four counters.
  - The result path is described as kernel OOM or systemd-oomd.
  - The SIGKILL note says cause unknown.
- **Unknown subjects** go to `UNIT_FAILURE_UNATTRIBUTED_JOURNAL` (and `_SYSTEM`), info, `owner=unresolved reason=subject-metadata-unknown`. A record carrying both `UNIT` and `USER_UNIT`, even when they are identical, goes to the unknown bucket.

This matches CX4. Residual checks:

1. **New keys must be masked.** The four new keys, plus `unit_oom_result_unknown` and the routing counts, are integers. They must be in `DRIFT_COUNTER_KEYS`.
2. **"Byte-equal" includes unavailable values.** An unavailable path must appear in the OOM line as its exact `unavailable:<reason>` SURFACE value, never as 0 (OA11).
3. **Selftest guard.** The legacy-text guard at :2788 is valid again for the single id. It should still fail if any per-scope id sneaks back in.

Literal call sites land; that is harmless and not a criterion.

The parent ruled that generic fleet failure stays INFO. That resolves a conflict: the JournalRegression brief said "fleet UNIT_FAILURE_JOURNAL warn", but frozen :905 and r13 both use info. A warn would be unrequested severity drift.

## Recommended L1 verification (not run here)

- `bash tools/mori-census.sh --selftest`, checking that OA-equivalent cases are present.
- The new `tools/mori-round14-regressions.py --census <frozen r13> --output …` must exit 1 with OA01–OA08 red.
- The same command with `--census tools/mori-census.sh` must exit 0.
- `--selftest` on the new gate.
- Optional and secondary: the spotcheck :77 jq scan on the repaired bytes. It is a static identifier check, not an admission criterion; behavioral cases decide.
