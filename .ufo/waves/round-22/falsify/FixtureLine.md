# FixtureLine — static falsification of the frozen v2 `line` variant (R08)

Seat: MoriR22.FixtureLine (critic, static only). No fixture, oracle, SUT, selftest, test, build or linter was executed. No installs or updates. No matched text emitted. Read-only commands only: `sha256sum` plus `git log` and `git diff --no-index` against lane files.

Inputs read: `denominator-correction.md` (first), `contract.md`, `frozen/fixture-builder-v2.py`, `frozen/fixture-builder.py` (v1), `frozen/requirements-v2.json`, `oracle-reconcile-v2.py`, shipping `tools/mori-retention-reconcile.py` at HEAD `5888b565`, `tools/mori-retention-gate.py` (scan, partition and result code), and `build/AttackR08.md` (prior note; I re-verified it against current source below).

## Verdict

R08 is **sound as a MISMATCH-versus-SETUP discriminator**, and its expected truth is correct. Two defects remain:

- **F1 (fixable, calibration).** R08 cannot tell which receipt list the SUT compared. The prior build note's claim that the mutation lands in `hits` only is false.
- **F2 (false provenance in retained evidence).** For mutated variants, the builder's `expected_*` identities are post-mutation aliases, and they are persisted in the oracle's run records.

Neither defect produces a false R08 pass against the current shipping SUT.

## Provenance (verified)

- These hashes equal the bindings recorded in `requirements-v2.json`:
  - `fixture-builder-v2.py` sha256 `1b3e16f7…d15d1`
  - `oracle-reconcile-v2.py` `dcd1c7c6…d8adb`
  - `contract.md` `1658c390…321a1`
  - `denominator-correction.md` `968945b2…724f9`
- The builder, oracle and requirements were each touched only by `e2f549b` (10:55:59). The SUT was first committed later, in `8cb4afb` (11:02:25), then changed in `3985b3d`. The freeze-before-implementation order holds.
- `git status` reports no worktree drift on frozen paths.
- v1→v2 builder diff: 4 insertions and 3 deletions. The changes are `rule='b'`, forbidden rows excluding `rule`, and `expected_policy_hits`/`expected_scanner_hits` now keyed on `non-author.txt`. The `line` variant line is byte-identical between v1 and v2. The oracle diff is only the builder path.

## What the `line` variant actually produces (static trace)

1. **`hits[0]` is the `policy.json` hit.** The `files` dict puts `POLICY` first. In the sorted, 2-space-indented policy JSON, the only matching line is line 13, `"synthetic": …`. The regex line `"[R]22_SAMPLE"` does not self-match, and `"R22"` lacks the `_SAMPLE` suffix.
2. **The mutation:** `result['hits'][0]['line'] += 1` changes line 13 to 14. Line 14 exists (the closing `}`) and carries no hit, so the mutated 4-tuple collides with nothing. That rules out `duplicate_receipt_hit` (R19/SETUP), and an in-range line rules out any stricter line-in-range validator.
3. **Aliasing (refutes the prior note).**
   - `allowed = [h for h in hits if …]` holds the *same dict objects*. `result['allowlisted_hits'] = allowed_effective = allowed`, and `result['hits'] = hits`.
   - `wrapper['stdout'] = json.dumps(result)` is re-run after the mutation (builder line 93). So the committed receipt carries line 14 in **both** `hits` and `allowlisted_hits`.
   - The receipt is internally consistent. It is not "hits only", and `differences` is not `['hits']`.
4. **Shipping SUT path, line by line.** No `Invalid` is raised:
   - `resolve` and `committed` pass, and the measured tree OID is variant-independent because dates and identity are fixed.
   - Policy and allowlist bytes are equal at measured and input revisions.
   - `normalize_hits` passes: the line is an int ≥ 1 and keys are unique.
   - `auxiliary([])` passes, and there are no population keys.
   - Result: exit 1, `RETENTION_RECONCILIATION_MISMATCH`, `differences == ['hits','allowlisted_hits']`, all counters equal to the valid arm (5/1/4, unallowlisted 1), `privacy_clearance: false`. [INFERENCE: static trace, not executed.]
5. **Line convention truth.** The fixture's identity `(path, line, class, line_sha256)` matches the real gate exactly: `text.split("\n")`, 1-based `enumerate`, and the line hash taken without the newline (gate:94–101; SUT:146–148). The fixture line numbering is therefore representative of real receipts.

## Target reason vs unrelated setup error

- **Distinguishable at class level: yes.** The oracle requires exit 1 + `RETENTION_RECONCILIATION_MISMATCH` + empty stderr, and every setup failure is exit 2 + SETUP.
- The mutation avoids each nearby setup trap:
  - type: no bool or non-int value;
  - duplicate: line 14 is unoccupied;
  - binding: argv, commit and policy digest are untouched.
- **Attribution is by differential construction only.** R08 has no predicate. Causality comes from R01 (valid → MATCH) on a fixture that differs only in the root path, which the SUT binds path-relatively, and in the receipt bytes. That holds today.
- **Fragility, unasserted.** If `files` order changed or the `synthetic` key were dropped, `hits[0]` would become `allowed.txt` line 1. Its +1 lands exactly on the sibling's 4-tuple (same path, class and sha), which yields `duplicate_receipt_hit` → exit 2. R08 would then fail as SETUP. That is not a false pass, but the builder never asserts its non-collision precondition.
- **Shared confound.** If the oracle is invoked with a relative `--output`, then `str(root)` is relative and every arm (R01 included) hits `receipt_repo_binding`. That is symmetric, so it cannot yield a false R08 pass. L1 must pass an absolute `--output`.

## F1 — counterexample: R08 cannot distinguish list-specific comparison

Because the mutation is aliased into two lists, consider a SUT that compares the full 4-tuple **only for `allowlisted_hits`**, and compares `hits` by count or 3-tuple. That SUT passes R08. Symmetrically, a `hits`-only comparator also passes.

Neither class is caught for the safety-relevant partition: no frozen arm mutates `line` in an `unallowlisted_hits` (retained-red) identity, or in a non-author identity.

- **Shipping SUT:** not affected. It compares all three lists as Counters of the full `hit_key` (lines 116–117, 212–213).
- **Prior-note correction:** because the receipt is internally consistent and the allowlist join omits `line`, the frozen arm already kills "no-recompute / internal-consistency-only" checkers for `line`. The prior note's "frozen R08 admits that false pass" is refuted for R08 specifically.
- **Prior-note correction:** its "selftest has no MISMATCH arm" is stale. Current `selftest()` has 4 arms, including `wrong.json` (`hits: []`) → exit 1 MISMATCH (lines 250–256).

## F2 — false expected identities after mutation (mutation/restoration provenance)

- **No restoration.** The builder mutates the shared `hits` dicts in place, then returns `expected_scanner_hits = [h for h in hits if …]` from the mutated objects.
  - For `line`: `expected_scanner_hits` lists `policy.json` line 14, which is not the truth (truth is 13).
  - For `inject` and `duplicate`: `hits` itself grows (`.append` on the aliased list), so `expected_scanner_hits` includes the injected or duplicated row.
  - For `digest`, `class` and `bool-line`: the same in-place leak.
- **Persistence.** The oracle stores `'fixture': f` in every `runs[]` row. Retained observations therefore label false identities as "expected".
- **Valid-arm truth is intact.** Each variant calls a fresh `make`, so nothing leaks across variants. The valid arm's `expected_policy_hits` = [non-author.txt:1] and `expected_scanner_hits` = {policy:13, allowed:1, allowed:2, unallowed:1}. Both are correct per the correction's non-author-glob semantics, and they are the only expected identities consumed by R04.
- **On-disk inputs are unaffected.** Tree files are written before mutation, and `expected_receipt_sha256` is computed from the bytes actually written.

## Impacted axes

- Calibration (primary): R08's discriminating power, and false-labelled expected identities in evidence.
- Depth (secondary): no arm covers `line` in the retained-red or non-author partitions.

## Smallest safe corrections

The frozen files are hash-bound, so no in-place edit is allowed.

1. **F2, disposition only (no refreeze).** L1 records that `runs[].fixture.expected_*` is authoritative **only for `variant == 'valid'`**. For mutated variants those fields are post-mutation aliases and MUST NOT be cited as truth. The R08 pass/fail judgment is unaffected.
2. **F1, if the canonical judge requires list-specific attribution (a v3 freeze; a tradeoff, not a defect in the shipping SUT):**
   - the builder serializes `result` from `copy.deepcopy` snapshots per list before mutating;
   - it asserts the mutated tuple is absent from the original population;
   - it adds an `unallowed.txt` line arm applied to `hits` + `unallowlisted_hits`;
   - the oracle adds the predicate `v['differences'] == [expected lists] and v['privacy_clearance'] is False`.
   Otherwise R08 stays a valid class-level (exit/finding) requirement, as the contract text words it ("altered line returns1").

## Adjacent (outside this seat's scope, verified only, not judged)

The SUT sets `raw_unallowlisted` and `scanner_unallowlisted` to the same `len(unallowed)`, drawn from scanner hits (line 223). On the real input, raw-population unallowlisted non-author identities (5) are therefore never surfaced as a distinct raw figure. Route this to the seat that owns denominators.
