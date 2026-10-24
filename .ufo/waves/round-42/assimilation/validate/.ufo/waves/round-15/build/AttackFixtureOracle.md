# AttackFixtureOracle — round 15 (critic, report-only)

Axis: **coverage**. Milestone: retain validated positives without fabricated totals.
Target: the fixture-pack oracle `{want_oom, want_signal, invalid_class}`. Attack: a gate that checks
only the two booleans, without the findings, rc/roll and raw aggregate tokens, passes mutants that
break the milestone. It also passes fixtures that never reach the parser.

Nothing was executed. All claims come from reading these files:
- `tools/mori-census.sh` (current bytes, no r15 positive code yet: grep `positive_` = 0 hits)
- `tools/mori-round14-regressions.py`
- `.ufo/waves/round-15/spec.json`
- `.ufo/waves/round-15/fixtures/KernelSystem.json` (the only pack on disk when I read)

`tools/mori-round15-regressions.py` did not exist yet.

## A1 (blocker): the default r14 stub filters out the "mixed" records, so the cases test nothing

**Anchor.** `tools/mori-round14-regressions.py:518-528`. In `honor` mode the stub keeps a record
only if `str(rec.get(k)) == v` for every `FIELD=value` match word. `-b` is ignored (`:450`), so the
stub never filters by `_BOOT_ID`. `ignore-filters` (`:510`) is the only mode that hands every record
of a scope to every query. The pack schema has no `mode` field, so the harness picks the mode.

**Counterexample.** Concrete, using `fixtures/KernelSystem.json` in `honor` mode:

| case | what the honor stub returns to the kernel query | raw `system kernel_oom_notice` | frozen entering census | boolean oracle |
|---|---|---|---|---|
| `kernsys_array_same_id_retains_valid_oom` | only the scalar record; `str(['fe6f…'])` ≠ `'fe6f…'`, so the array record is dropped | `1` (ok) | already fires OOM crit (r14 path `:1316`) | green on **both** frozen and new census |
| `kernsys_empty_array_retains_valid_oom` | only the scalar record | `1` | fires | green on both |
| `kernsys_multi_array_ordered_retains_valid_oom` | only the scalar record (the multi-valued record is dropped from both the kernel and unit queries) | `1` | fires | green on both |
| `kernsys_array_only_never_positive` | nothing | **`0`**, a numeric zero, although `invalid_class` claims unavailable | CLEAN | green on both |

Results:
- None of the four cases is red on the pinned red control (`0e41cb83…`).
- The fourth case shows the exact fabricated zero the milestone forbids, and the booleans cannot see it.

Two other packs have the same defect by construction:
- KernelUser ("wrong MESSAGE_ID"): the scalar mismatch is filtered.
- ProcessUser ("malformed EXIT_STATUS"): `EXIT_STATUS=9` is a match word (`mori-census.sh:1196`), so a record with a non-`"9"` or array status is filtered.

UnitUser's malformed `MESSAGE_ID` record is also filtered (match `MESSAGE_ID=d9b3…`, `:1201`).

**The same cases in `ignore-filters` mode do discriminate.** Example, `kernsys_array_same_id`:
- Both records reach the kernel query. `.MESSAGE_ID == $id` fails on the array record, so the else-branch (`:973`) yields `record-invalid`.
- The same records reach the unit query, which is also `record-invalid`.
- Frozen census: no OOM, CLEAN rc 0, so it is red against `want_oom: true`.
- A correct r15 census: `positive_kernel_oom=1` (system), OOM crit, rc 1.

**Smallest correction (HarnessBuild).**
1. Run every case whose `invalid_class` is non-null with stub mode `ignore-filters`. Run `invalid_class: null` cases in `honor` mode so that CleanControls keep r14 behaviour.
   - In `ignore-filters` mode, a homogeneous valid kernel record also poisons the unit, oomd, coredump, segfault and sigkill queries of its scope.
   - So running controls under `ignore-filters` would silently change "previous behavior", and the booleans would still pass.
2. Record a per-case red-control result. Every case with `invalid_class != null` and (`want_oom` or `want_signal`) must be red on the frozen census.
   - A mixed-positive case that is green on frozen means the fixture is vacuous. Treat it as **gate 2 (could-not-evaluate)**, never pass and never waive.
   - A single "frozen failed at least one case" aggregate is not enough: the honor-filtered cases would ride along vacuously.

Realism caveat for SKILL/knowledge seats: `ignore-filters` models an adversarial or defective producer, not journalctl semantics. Real journalctl with `MESSAGE_ID=X` does not return a record whose scalar id differs. Realistic mixing comes from multi-valued fields: real journalctl matches a field if any value equals X and prints the field as a JSON array (S015). The stub's `str(list)` comparison under-models that. Neither stub mode is a measurement of real journal frequency. `[INFERENCE]` from the stub code and S015 as cited in round-13/14 notes; the source was not reopened here.

## A2: booleans-only checking passes mutants that break the milestone

Each mutant below passes both booleans in `ignore-filters` mode on the case named. Each line gives the smallest assertion that catches it.

| # | Mutant (plausible implementation slip) | Case that slips through | Required assertion |
|---|---|---|---|
| M1 | **Salvage total.** When the aggregate is invalid, write the positive count into the raw token (`kernel_oom_notice=1`) | `kernsys_array_same_id` | raw `system kernel_oom_notice` = `unavailable:record-invalid` exactly, in the SURFACE row **and** in the OOM finding field `system_notice=`. The r14 byte-equality check (`r14 :1789-1802`) is not enough: M1 changes the surface and the finding consistently. |
| M2 | **Cross-stream positive count.** In `ignore-filters` mode the same kernel record arrives in all six per-class streams; summing "positive-shaped" records across streams gives `positive_kernel_oom=6` | `kernsys_array_same_id` | exact literal `positive_kernel_oom=1` (system), `positive_unit_oom=0`, `positive_unit_signal=0`, `positive_process_sigkill=0`; user scope all `0` |
| M3 | **Double alarm.** The raw path and the positive path each emit an OOM line | any fanout case | `count_ids(OOM_KILL_JOURNAL)==1` and `KILL_SIGNAL_JOURNAL ≤ 1` (reuse `exact_counts`, `r14 :1777`) |
| M4 | **Severity or roll drift.** A positive alarm emitted at `warn`/`info`, or after the roll | any want-true case | OOM `severity=crit`; KILL `severity=warn`; rc 1 plus `MORI_CENSUS: DRIFT` iff `want_oom or want_signal`, else rc 0 plus CLEAN (the fx-quiet baseline is CLEAN, `r14 :757-758`) |
| M5 | **Summed or salvaged KILL count.** `count=` or `process_sigkill=` set to the positive count | ProcessUser mixed case | the KILL fields `count=` and `process_sigkill=` byte-equal the user SURFACE `unit_sigkill_record` raw token (`unavailable:record-invalid`); `user_unit_signal=` byte-equals the user raw `unit_signal`. r14 has this invariant for OOM only (`:1784`), not for KILL. |
| M6 | **System leaks into user WARN.** Positives summed across scopes | a case with user and system signal positives | user/system positive literals; KILL fires only on **user** `positive_unit_signal`/`positive_process_sigkill` |
| M7 | **Path loss masked.** The `positive_unit_oom` path (or `positive_unit_signal`) is never consulted | Fanout cases where another path also fires | per-path positive literals per scope; KILL `paths=` names every firing path, and the OOM line names every positive source |
| M8 | **Zero on failure.** Positive tokens emit `0` when capture or parse failed | **not expressible in the pack schema** (no rc/stderr fields) | built-in harness cases outside the packs: stderr-nonempty, rc 1 and `malformed` stub mode must give every `positive_*=unavailable:<status>` and no alarm |

## A3: `invalid_class` (a single string) does not pin what is invalid

- In `ignore-filters` mode one nonmatching record invalidates **every** class in its scope, so one string is only a lower bound.
- The string names neither the scope nor the status (`record-invalid` / `multi-boot` / `boot-mismatch`).
- Counterexample: a mutant that salvages only the classes *not* named (for example the unit aggregate in `kernsys_array_same_id`, giving `unit_failure_record=0`) passes a check limited to `invalid_class`.

**Smallest correction, in order of preference (L1 decision; the schema is shared):**
- (a) Add pack-level literals `want_unavailable: ["system:kernel_oom_notice", "system:unit_failure_record", …]` and `want_positive: {user:{4}, system:{4}}`. These are static and independent of the SUT, matching the contract wording.
- (b) If the schema stays frozen: the harness carries its own Python restatement of the four positive predicates **from the spec text**, not from the census jq, and computes the literals per case.
  - It asserts that every class in a poisoned scope is `unavailable:` with a reason from the frozen r14 vocabulary.
  - It asserts that no raw token in that scope equals a positive count.
  - It persists the derived literals in the expected manifest so the derivation is pinned.

## Holds (checked, not defects)

- The rc derivation from the booleans is sound: in the fx-quiet baseline only the OOM crit and the user KILL warn flip the roll (`mori-census.sh:398`, `:1262` routing comment; r14 negative cases expect CLEAN rc 0).
- KernelSystem's system-only want-true cases do catch a "user-scope-only positives" mutant. Keep at least one system-only positive case.
- Negative `kernsys_array_only_never_positive` is correctly CLEAN on frozen and new census in both stub modes. It satisfies "pass negative controls", but only with the A3 raw check is it more than a no-alarm check.

## Impacted axes

- **coverage (owned).** Without A1, the C1 claim has no discriminating witness: the r15 gate could be green with zero mixed records ever parsed.
- **no-harm / operability.** M1, M5 and M8 are fabricated totals and zeros; a booleans-only gate cannot reject them.
- **evidence.** "Red on frozen" is the only proof the change did something.

## Tooling

No installs or updates. The parent's host-safety notice was received, and no package manager was used.
