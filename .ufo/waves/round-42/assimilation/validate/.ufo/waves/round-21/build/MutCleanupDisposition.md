# MutCleanupDisposition — proposed bounded mutation/control

## Status and scope

**PROPOSED / NOT EXECUTED.** This seat wrote a standalone probe for later L1 verification. No target execution, mutation run, census, pin, build, lint, formatter, broad test, or production edit was performed. No killed/survived verdict is claimed.

Candidate: `.ufo/waves/round-21/build/MutCleanupDisposition/probe_cleanup_disposition.py`.

Axes named for this probe:
- **C1 freshness:** retaining an observation must not permit acceptance while its disposition remains unknown.
- **C2 calibration:** a cleanup receipt from the cleanup actor is not independent disposition. The accepting independent-actor control prevents credit for an auditor that simply rejects every disposed row. This probe exercises `audit`, not the separate `classify` rule evaluator; it does not verify C2's full before/after classification claim.

Authority: `.ufo/waves/round-21/contract.md:7-16`, especially line 14's independent actor requirement and unresolved blocking rule. Historical cleanup by the same identity does not settle either disappeared-wave observation. This proposal introduces no historical settlement and permits no real pin.

## Concrete mutant and controls

Use one **synthetic** `aggregator-r10` required row with committed baseline, deletion, and cleanup copies. Baseline and accounting share the exact baseline reference; required evidence is `evidence/baseline.md:1`. Synthetic actors are `synthetic-cleanup-author` and `synthetic-independent-reviewer`; these fixture markers are not claims about real historical independence.

The baseline row is `state: unresolved`, `independent_disposition: null` (script lines 153-172). The input mutant changes only those two accounting fields: `state: disposed` plus an independent-disposition reference declaring `independent: true`, but with the **same actor as cleanup** (lines 174-181). Its referenced committed JSON has matching `id`, `actor`, `wave_id`, `disposition: cleanup-accounted`, and `independent: true`. Its path, revision, and SHA-256 are valid. Therefore a successful rejection must not be credited to missing, uncommitted, stale, mismatched, or malformed evidence.

The positive control uses the same disposed-row structure and receipt fields, except the receipt actor is genuinely distinct within the synthetic fixture; the referenced filename/hash differ mechanically with its bytes (lines 182-186). Both receipt files are committed before any detector call, so no evidence or Git revision changes between detector phases.

The implementation owner, `MoriR21.ImplLoss-4`, supplied the proposed concrete interface by peer message:
- Required row: `{id,baseline,evidence}`; `baseline` is `{path,revision,sha256}`; `evidence` is a relative `path:positive-line` string.
- Cleanup reference additionally carries `actor`.
- Disposition reference carries `{path,revision,sha256,independent:true,actor,wave_id,disposition}`; referenced JSON is exactly `{id,actor,wave_id,disposition,independent:true}`.
- Expected same-actor finding: `mori-evidence-loss:audit:aggregator-r10:independent_disposition:independent_actor_not_distinct`.

These are interface-design statements, not observed detector output. At initial inspection the production `tools/mori-evidence-loss.py` was absent; the owner's candidate was still being authored. Final implementation compatibility remains unexercised.

## Expected detector

Every phase runs the identical command against one immutable copied auditor and the same required/accounting paths (script lines 191-194):

```text
<current-python> -I -B <seat-run>/auditor.py audit --root <seat-run>/isolated-repo --required <seat-run>/isolated-repo/required.json --accounting <seat-run>/isolated-repo/accounting.json
```

| Phase | rc | omitted | retained | unresolved | disposed | invalid | pin_allowed |
|---|---:|---:|---:|---:|---:|---:|---|
| pristine unresolved | 1 | 0 | 1 | 1 | 0 | 0 | false |
| independent actor control | 0 | 0 | 1 | 0 | 1 | 0 | true |
| same-actor mutant | 1 | 0 | 1 | not asserted | 0 | 1 | false |
| exact restored baseline | 1 | 0 | 1 | 1 | 0 | 0 | false |

The mutant additionally must emit the exact finding ID above. Its unresolved count is preserved in actual output but is not used to guess whether invalid rows are also counted unresolved.

Verdict rules (lines 263-307):
- **killed:** pristine, independent positive control, and restored control all satisfy their expected contracts; inputs remain immutable during each detector run; the mutant is blocked with the expected stable actor finding and invalid-row accounting; exact restoration succeeds.
- **survived:** those controls succeed but the mutant returns rc0 and `pin_allowed:true`. This is a coverage finding, never permission to change the contract.
- **inconclusive:** any baseline/control failure, setup failure, timeout, malformed output, unexpected blocker/finding, immutable-input drift, missing run, or restoration failure. A baseline failure is never called a killed mutant.

## Isolation, bounds, and restoration

- Script creates a fresh `probe-*` directory beneath its own assigned seat, with a minimal isolated Git repository; it never clones unrelated fleet history or reads transcripts.
- Git writes use explicit absolute `git -C <seat-run>/isolated-repo` and remain in that synthetic repository. Git global/system config and hooks are disabled; an isolated home and clean subprocess environment avoid reading operator credentials/config.
- Only the chosen auditor's source bytes are copied from the lane; original auditor bytes are never modified. All four calls use that single snapshot.
- Four detector calls only, each with a 10-second subprocess timeout. No `--selftest`, discovery, census, classifier sweep, or pin command is included. `TMPDIR` is set to the assigned lane `.scratch` path.
- `finally` restores saved accounting, required input, copied auditor, and every fixture evidence file before the restored detector call, then restores them again afterward, even when a detector fails (lines 238-254).
- Each phase stores actual raw stdout/stderr, return code, parsed JSON, accounting before/after SHA-256, and immutable-input drift. Final `result.json` stores before/after hashes plus exact-byte equality for every saved input and restored/pristine behavior equality (lines 197-236, 256-262, 308-320).
- Generated repositories and output artifacts remain isolated for L1 evidence review. Synthetic fixture acceptance cannot authorize a real pin or establish independent disposition of historical observations.

## Later L1 invocation — not run here

From the mori lane root, after the auditor has landed:

```text
python3 .ufo/waves/round-21/build/MutCleanupDisposition/probe_cleanup_disposition.py --auditor tools/mori-evidence-loss.py
```

The wrapper prints the verdict and exact `result.json` path. Wrapper exit codes are 0 killed, 1 survived, 2 inconclusive/setup. L1 should inspect all four actual detector outputs and restoration hashes; this proposal alone is not evidence that the invariant holds.

## Actual outputs and hashes from this seat

Only file creation, scoped reads/searches, interface coordination, and artifact hashing were exercised. The probe itself was **not run**, including no syntax-check execution.

Observed `sha256sum` output:

```text
94a214a21377ebe28f3ed10de2827de372989bbf1053afa17d34a5896845d20e  .ufo/waves/round-21/build/MutCleanupDisposition/probe_cleanup_disposition.py
c49e66c2db9572225a0355ac8ab73f3feacd1f78b5fc157210d5d516c9b3ec6f  .ufo/waves/round-21/contract.md
```

Actual detector outputs: **none — intentionally deferred**. Actual mutant verdict: **not run**. Actual pristine/mutated/restored fixture hashes and runtime restoration evidence: **not available before execution**; the script records these rather than fabricating them. No target bytes were mutated by this seat, so no production restoration was necessary.

Tool installs/updates: **none**.

Report: .ufo/waves/round-21/build/MutCleanupDisposition.md
