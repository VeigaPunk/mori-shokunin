# CriticC1Cutover — round23 C1 clean-cutover falsification

Seat: `MadoR22-2.CriticC1Cutover` (UFO-FSD critic, read-only). Production pin
`f3dc07c0bf423cc1947d0ffa91afa9ce236fbe3c`; seal `22772c10f6e3c1d8d3fe1b72083a6194e9f4e687`
(verified strict ancestor, `git merge-base --is-ancestor` rc0). Evidence read: `contract.md`,
`preseal-amendment.md`, `frozen/c1-*.json`, `oracle-rename.py`,
`build/MeasureDriver/measure-round23-v2.py`, `evidence/measure4/*` (committed at `6eb889c`),
r22 `oracle-reconcile{,-v2}.py`, `refinement-reconcile.py`, `measure-round22.py`, SKILL/knowledge/lesson/LOG text.
No tool executed except read-only git, `sha256sum`, and in-memory Python over committed bytes.
No installs. Scratch dir `/fast/scratch/hyaku/mori-r23/CriticC1Cutover/` created, left empty.

## Verdict

The C1 claim holds as stated: original26 is 25/26 → 26/26 (only R25 red before), alias runs 8 → 0,
and the exact two-transform source guard is sound. No C1 check fails in measure4. Two of the
supplementary guards don't discriminate anything: C22 (guard self-test) and the C35 twin. They
should be disclosed as such. One clause rests on static evidence only and was never run: r22
reproduction at `da40bb2`. Nothing found changes the 26/26 or needs a production, frozen or oracle edit.

## Clause-by-clause

| clause | status | evidence |
|---|---|---|
| original26 before 25/26, unmet `[R25]` | PROVEN | `c1-before-observed.json`: only R25 false; `misleading_alias_runs` 8, `parsed_runs` 18, `schema_v2_runs` 0 |
| original26 after 26/26 | PROVEN | `c1-after-observed.json`: R01–R26 all true; `parsed_runs` 18 = `schema_v2_runs` 18; alias runs 0 |
| R01–R24 = r22 v2 predicates with only the key substitution | PROVEN | I took r22 `oracle-reconcile-v2.py`, substituted `raw_unallowlisted` → `scanner_unallowlisted` in the R01..R24 block, and diffed it against `oracle-rename.py`. Zero differing lines (15 = 15). |
| frozen pins | PROVEN | sha256 matches the pins: `oracle-rename.py` a55b2b50…, `contract.md` 2bb35aef…, r22 builder 1b3e16f7…, r22 requirements 48ea2369…. Oracle/requirements/expected-real first committed at `4dc80c1`, before implementation `1979a9d`. |
| alias 8 = exactly the check-shaped arms | PROVEN | The entering replays carry the alias on valid, drop, inject, digest, line, class, metric and forbidden. Each entering alias value equals `scanner_unallowlisted` (1×7, and 3 on forbidden). The 10 setup envelopes never had it. |
| exact two-source-byte guard (C21) | PROVEN, replayed independently | Baseline blob `1bfe708` sha 0795bac9…. Each replacement appears exactly once; applying both gives 4599ee1a… = frozen `transformed_sha256` = blob at `f3dc07c` = working tree. Mode is 100755 at both revisions. After the transform: 0 `raw_unallowlisted`, 0 v1 literals. `git diff 1bfe708 f3dc07c -- tools/mori-retention-reconcile.py` shows the two hunks only. Outside `.ufo`, the tools delta is reconciler M plus quota A. |
| semantic no-delta from the deletion | PROVEN by source | The deleted entry `'raw_unallowlisted':len(unallowed),` has no side effects. The adjacent `'scanner_unallowlisted':len(unallowed)` evaluates the same expression, so there is no new exception path. Output uses `sort_keys`, so no ordering change. The reconciler imports only stdlib and shells out only to `git`, so no other lane file is behaviour-coupled. |
| guard discriminates mutants (C22) | VACUOUS | See counterexample 1. |
| same-instance object equality (C23) | PROVEN with caveats | 18/18 arms: replays run on the after-oracle fixture instance. argv, stderr, exit, key sets and values are all equal. The before tool reports 0795bac9…, the after tool 4599ee1a…, and the after replay is byte-equal to the oracle record. Instance sameness matters: the before and after oracle fixture sets differ in 130 of 740 files. Caveats are in counterexample 3. |
| selftest schema (C24) | PROVEN, narrow | v1 → v2, 4/4 both, exit 0 both. The selftest's own 4 arms assert only exit, finding_id and privacy_clearance, so they can't see either renamed key. C24 shows the schema field changed and nothing more. |
| schema v2 on every output path | PROVEN statically, partly unobserved | Check, setup and selftest are observed. The `usage` path (`-h`, unknown arg) and `input_unavailable` envelopes were never captured in a receipt: the selftest's `--unknown` arm discards its stdout. All 4 emitters use the single `SCHEMA` constant (source lines 231/274/287/289). |
| real control values (C25/C26) | PROVEN | scanner_unallowlisted 4, raw_not_allowlisted 9, raw_total 95, allowlisted 86, policy_excluded 5, scanner_total 90, red, privacy_clearance false, schema v2, no forbidden key. Inputs, revisions, argv and tool_sha256 match. The entering tool emitted the alias with value 4. |
| real identity pins (C35 identity_match) | PROVEN, lineage-qualified | `frozen/c1-expected-real-identities.json` is byte-identical to r22's `frozen/expected-real-identities.json` (`cmp` equal; schema still `mori-r22-real-identities-v1`). It shows the v2 output's hit populations equal the r22-era co-evolved digests. Its own qualification says it is not historical-execution authentication. |
| twin (C35 twin_rejected) | VACUOUS | See counterexample 2. |
| archival API break disclosure | PROVEN for content, one handoff gap | See below. |
| r22 reproducible only in a checkout of `da40bb2` | UNPROVEN (not executed) | The driver's scope note says "not attempted". Static reading of `measure-round22.py` supports it [INFERENCE]: line 58 runs `LANE/tools/...`, and lines 60–69 compare bound files with `--revision` blobs and exit 2 `measurement_inputs_uncommitted` on a mismatch, so it fails closed in the current checkout. The reconciler is unchanged between `da40bb2` and `1bfe708` (empty diff). |

## Counterexamples

1. **C22 never runs the guard on a mutant.** It builds three strings from `expected_source`
   (lines 699–709) and sets `guard_rejects = data != expected_source`. That tests Python `!=`, not
   the `guard_ok` predicate (lines 641–652). The pass is a constant for any non-identical string,
   so C22 would still be green with a broken guard: for example, `and` → `or`, a dropped
   `expected_source == retention_after_bytes`, or an ignored mode. No mode mutant (100644) and no
   wrong-transform mutant (v1 literal kept, alias kept, wrong key deleted) is ever fed through the
   guard. C21 is still sound, because its byte equality is redundant with three independent sha
   pins that I replayed by hand. Impacted axis: calibration/provenance (guard-of-guard evidence).
   Smallest safe correction (future driver revision, not this seal): factor `guard_ok` into
   `guard_passes(source_bytes, mode)` and apply it to staged mutant bytes and modes. Until then,
   label C22 "byte-inequality sanity, not guard discrimination".
2. **The C35 twin is decided by the frozen file alone.** `twin_observed` swaps the observed
   scanner and policy digests (driver lines 923–926, copied byte-for-byte in construction from
   `measure-round22.py` lines 145–147). Once `identity_match` holds, `twin_rejected` is true exactly
   when expected `scanner_hits` ≠ expected `policy_excluded_hits`. That is a property of the frozen
   pins (9690b3a9… vs 17c348f0…), so it is always true and adds nothing over `identity_match`.
   Any tool output that would make the twin "match" already fails `identity_match`. The LOG line
   1579 and knowledge-note wording "pins/twin control" overstate it. Smallest safe correction:
   disclose it as an inherited non-discriminating twin. A real twin would rerun the same command on
   a perturbed committed input or a category-swapping tool mutant and require a mismatch.
3. **The C23 reporting caveats don't change the verdict.**
   - Two replay arms are labelled `valid`. Index 16 is the `../receipt.json` receipt-override arm
     (`unsafe_input_path`), but rows are keyed by `row.get('variant')` without the override, so
     `divergent=[...]` lists would be ambiguous.
   - `same_instance: True` is a hardcoded literal (line 732), not a measurement.
   - For the 10 setup arms, sameness rests only on reused argv, because setup envelopes carry no
     input digests or revisions.
   - The before alias value is never compared with `scanner_unallowlisted` (it is excluded as a
     special key). I checked it from the receipts and it is equal on all 8 check arms.

   Correction: key rows by index plus override, and record a fixture-tree digest before and after
   each pair.
4. **R02 now repeats one conjunct.** After the substitution R02 reads
   `v['scanner_unallowlisted']==1 and v['scanner_unallowlisted']==1`, where r22 had two distinct
   keys. This is exactly the contracted pure substitution, and R26 (=2 on valid) covers the raw
   complement, so no assertion was lost. R02 is just weaker than it reads. The frozen bytes stay as
   they are; disclose only.

## Archival API break disclosure

- Breakages are enumerated correctly and match the source:
  - r22 `oracle-reconcile-v2.py` (and v1 `oracle-reconcile.py`) R02/R11/R12;
  - exactly five refinement checks: `clean-control`, `non-author-overlap`, `forged-clean`,
    `nested-policy-copy`, `forbidden-only` (`refinement-reconcile.py` 186–192);
  - `measure-round22.py`'s expected-real all-keys comparison (line 139, against r22
    `frozen/expected-real.json`, which has `raw_unallowlisted: 4`).
- The subset whitelist `set(value)<=allowed` (line 28) does not break when the key is removed.
  That is correct.
- The original contract wrongly said the r22 driver stages the tool from `--revision`. The
  amendment, SKILL 566–576, the knowledge note 46–62 and lesson M6 all correct this. The historical
  SKILL caveat at line 556 is explicitly marked historical v1 at 566–567.
- There is no executable consumer outside the lane. A fleet-wide `rg` (excluding mori-shokunin,
  .git, .jj, .scratch and interactive-sessions) found `raw_unallowlisted` only in fleet-root
  `MANIFEST.json` and `.ufo/reports/round-22/mori.md`, 2 hits each, both archival text. In-lane
  code outside the waves: only the reconciler names these fields.
- **Handoff gap, not a C1 defect:** fleet `MANIFEST.json` line 12007 (rounds[427] row) still
  records the reconciler as `sha256 0795bac9…de32`, next to the old alias text. The lane can't write
  the fleet root, so outside closure must mark that pin superseded by 4599ee1a… for the r23 API.

## Failures retained

measure4 exits 1. The C1 checks C17–C26, C31 and C35 all pass. The failing checks are:

- **C34:** 29/30.
- **C30:** 30/31. Its single unmet item is the same `CaseEscapedSpace.json` (status `unmet`); the
  C2 real-control headline matched on exit, finding and paths.

There are no additional C1 failures. C2 stays strict-UNPROVABLE as recorded.

## Open debt (unchanged)

The following are not cleared by anything here:

- 4 unallowlisted inherited hits (raw95/allowlisted86/non-author5);
- original permission RED 11/12;
- two unknown dispositions;
- baseline acceptance blocked;
- `privacy_clearance=false`.

## Process note

The fleet-wide search took about 880 s of wall time. It was read-only static text search, with no
host, journal, session or credential reads.
