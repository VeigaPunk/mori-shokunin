# FinalR16 — falsification of R16 (changed allowlist bytes returns 2)

Seat: MoriR22.FinalR16 (critic). Static analysis only: no executions, builds, tests, fixtures, production edits or delegation. Tools installed or updated: none.

Inputs verified this seat (sha256 of current bytes):
- `tools/mori-retention-reconcile.py` d6870fb6db7c7d0886f1823b42399821f4f54a4ff0290ee1b43adf9400ac0ce7 (last touched by 3985b3d)
- `.ufo/waves/round-22/oracle-reconcile-v2.py` dcd1c7c6…d8adb, matches `requirements-v2.json` `oracle_sha256`
- `.ufo/waves/round-22/frozen/fixture-builder-v2.py` 1b3e16f7…15d1, matches `fixture_builder_sha256`
- `contract.md` 1658c390… and `denominator-correction.md` 968945b2…, both match `requirements-v2.json`

The correction (policy_excluded means identities matched by the non-author glob) does not change what R16 means. R16 is still the contract's rule that policy and allowlist bytes at the input revision must equal the bytes at the measured revision, and that a mismatch is unevaluable (exit 2). The prior build note `build/AttackR16.md` cites line numbers from 8cb4afb. Every claim below was re-derived from the current source and is not taken from that note.

## Verdict

- **SUT branch: R16 HOLDS.** Static trace on fixture variant `allowlist-changed`:
  1. `resolve` succeeds for the input revision.
  2. `committed` reads the receipt, policy and allowlist from input-revision blobs.
  3. The wrapper schema check passes.
  4. `measured_revision` is a full OID and resolves to itself.
  5. `merge-base --is-ancestor` returns 0, because the measured commit is the parent.
  6. The loop at reconcile.py:164-165 compares policy bytes first; they are equal.
  7. The allowlist comparison sees measured bytes `files[ALLOW]` against input bytes `files[ALLOW]+b'\n'` and raises `Invalid('allowlist_changed')`.
  8. `main` outputs `{"finding_id":"RETENTION_RECONCILIATION_SETUP","error":"allowlist_changed",...}`, exit 2, empty stderr.

  The gate runs before `policy_rules`/`allow_rows` and before any recomputation, so the bytes that were compared are the bytes that get consumed. I found no input that changes allowlist bytes and gets exit 0 or 1. Missing, non-regular, symlinked or gitlinked allowlists at either revision fail earlier with exit 2. A changed policy at the same time reports `policy_changed` first, which is still exit 2.
- **Oracle evidence: R16 is NOT branch-proving.** `record('R16','allowlist-changed',2,SETUP)` (oracle:53) asserts only exit 2, the finding, and empty stderr. It never reads `error`. A green R16 row therefore proves only that some setup branch fired. It does not prove that the byte-equality branch fired.

## Smallest counterexample: an oracle-green mutant with no byte binding

The fixture's only R16 change is one extra trailing newline, committed in the same commit as the receipt. That single change is also a formatting difference: every other fixture allowlist uses the canonical form `encoded()` (`json.dumps(sort_keys, indent=2)+'\n'`).

Mutant M1 changes the SUT in two ways:
- delete `'allowlist'` from the loop at reconcile.py:164-165;
- add `require(raw['allowlist']==(json.dumps(parse(raw['allowlist']),sort_keys=True,indent=2)+'\n').encode(),'allowlist_noncanonical')`.

Oracle result for M1, traced by hand: every other variant's allowlist is canonical, so R01–R15 and R17–R24 are unchanged. On `allowlist-changed`, M1 exits 2 with SETUP (`allowlist_noncanonical`), so R16 passes. The oracle reports `R22_REQUIREMENTS_MATCH` 24/24 even though the byte-binding requirement is gone.

Real impact of M1: change the allowlist at the input revision in canonical form, for example by adding a row that covers the retained unallowlisted hit, and forge the receipt to claim clean. M1 then applies the current allowlist to a historical scan and reports `RETENTION_RECONCILED`. That is exactly what the contract forbids ("not silently current policy applied historically").

A second mutant, M2, is an identity substitution: it compares the allowlist against `rev^` instead of `measured_revision`. It is also oracle-green, because the fixture's input revision is exactly one commit after the measured commit (fixture-builder-v2.py:96-99). It is wrong whenever measured and input are more than one commit apart.

## Missing same-command red control

- **Oracle:** the only green reference for R16 is R01, which runs in a different repository (`<fixtures>/valid`), with a different `--repo` path, a different `--rev`, and a different receipt blob (the receipt embeds the root path). No arm runs the same command, differing only in `--rev`, where the allowlist is unchanged (expect 0) and changed (expect 2 with `allowlist_changed`). As a result, R16's red cannot be attributed to the allowlist change.
- **SUT `--selftest`** (reconcile.py:233-261): it has 4 arms (match, mismatch, unsafe path, unknown flag). None changes policy or allowlist bytes, so the R15/R16 branch has no self-exercised red arm at all. The 4 arms assert exit and `finding_id`, never `error`.

## Impacted axes

- Calibration: a green oracle overstates branch coverage.
- Provenance and identity: the measured-versus-input binding is not discriminated against a `rev^` substitution.
- No hidden regression in the shipping SUT, no duplicate authority, no false provenance in its output.

This is a fixable defect in the evidence, not a tradeoff. The canonical judge should treat R16 as "SUT holds, oracle row non-discriminating" until the correction lands.

## Smallest safe correction (detection-side only, new v3 artifacts; frozen v2 stays byte-unchanged)

1. Strengthen the R16 predicate with `v.get('error')=='allowlist_changed'`, and the R15 predicate with `'policy_changed'`. This changes one predicate each and needs no new fixture.
2. Add a same-repository control chain: measured → G (receipt commit, allowlist unchanged) → R1 (canonically encoded allowlist change, for example an edited `reason` text) → R2 (an unrelated file with no hits). Run identical argv except `--rev`:
   - `--rev G` expects 0, `RETENTION_RECONCILED`;
   - `--rev R1` expects 2, `allowlist_changed`, which kills M1;
   - `--rev R2` expects 2, `allowlist_changed`, which kills M2.
3. Optionally add an `allowlist-changed` arm to the SUT `--selftest` that asserts exit, `finding_id` and `error`. This is an L1 production edit; this seat does not make it.

Residual risk, outside R16's power: the r21 receipt schema binds `policy_sha256` but not an allowlist digest. R16 can therefore prove only that the committed trees agree, never that the allowlist the scan actually used matches; the SUT reports `receipt_authenticity:'unattested'`. Privacy clearance stays false.
