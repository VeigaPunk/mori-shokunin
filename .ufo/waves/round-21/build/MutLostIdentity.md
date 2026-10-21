# MutLostIdentity — proposed bounded C1 mutation/control

## Status and axes

**Proposal complete; target execution deliberately not performed. Experimental verdict: inconclusive/unexecuted, not a killed or surviving mutant.** No baseline, mutant or restored audit output has been observed. No broad tests, census, pin, Git writes, production edits, tool installs or other runtime invocations were performed.

Axes: omission sensitivity; lifecycle honesty; isolated, byte-exact restoration. C2 classification is outside this one probe.

Candidate: `.ufo/waves/round-21/build/MutLostIdentity/probe-lost-identity.py` (standalone Python stdlib runner; file creation succeeded, 13,024 bytes).

## Grounded control and mutation

- `.ufo/waves/round-21/contract.md:7` requires both historical identities visible, with zero omitted and two unresolved after retention; this is not settlement evidence.
- `.ufo/waves/round-21/contract.md:14` defines the audit fields, deliberate blocker rc1, and pin prohibition for unresolved evidence.
- `.ufo/waves/round-21/contract.md:27` retains FR3 lifecycle unknown.
- `.ufo/waves/round-21/frozen/required.json:5-20` explicitly requires `aggregator-r10` and `aggregator-r10-resume`.
- `corpus/evidence/loss-accounting-r21.json:5-23,26-44` retains those two rows as `unresolved`, each with `independent_disposition:null` and baseline/deletion/cleanup provenance.
- `.ufo/waves/round-21/evidence/historical-provenance.json:38-40` states independent disposition is null and settlement unknown; same-identity cleanup does not prove settlement.
- `.ufo/waves/round-21/frozen/before-accounting.json:3` is empty. It is **not** the pristine control for this mutation: using that already-incomplete register could disguise a baseline failure as mutation detection.

The runner freezes copies of the evaluator, required JSON and complete unresolved accounting in a new `MutLostIdentity/omission-*` directory. It removes exactly the accounting observation whose id is `aggregator-r10-resume`, preserving every other parsed field and the complete required set. It never edits the original accounting, frozen fixtures or evidence files. JSON formatting of the mutated copy is canonicalized; the only semantic change is the single observation removal. Restoration uses original bytes, not serialization.

The control must contain exactly these two identities, both unresolved with explicit null disposition. These setup requirements are enforced at `probe-lost-identity.py:73-85,193-199` within the candidate directory. The deletion is at `probe-lost-identity.py:200-203`.

## Expected detector, not measured output

The **same copied evaluator**, command, root, required file and accounting path are used for pristine, mutated and restored calls. Only that private accounting path's bytes change. Each call invokes `audit` once with a 15-second timeout; stdout JSON parsing is capped at 1 MiB. There is no suite, selftest, classify, census or pin invocation.

| Phase | rc | omitted | retained | unresolved | disposed | invalid | pin_allowed | Actual output |
|---|---:|---:|---:|---:|---:|---:|---|---|
| Pristine complete unresolved control | 1 | 0 | 2 | 2 | 0 | 0 | false | Not executed |
| Remove `aggregator-r10-resume` accounting row | 1 | 1 | 1 | 1 | 0 | 0 | false | Not executed |
| Restore exact pristine bytes | 1 | 0 | 2 | 2 | 0 | 0 | false | Not executed |

The decisive delta is **omitted +1**, not an exit-code transition: all three calls should return rc1. The unresolved counter falls by one because the row is no longer retained, **not** because its lifecycle became known. Disposed must stay zero and pin permission must stay false. Neither wave receives independent disposition or settlement from this experiment. The runner checks the specified counters and pin decision; it preserves `issues` verbatim without inventing an issue/finding-id shape absent from the shared interface.

Expected values are fixed at `probe-lost-identity.py:25-28`; audit capture and output validation are at `probe-lost-identity.py:92-141`.

## L1 invocation, only after integration authorization

Observed prerequisite at preparation: `tools/mori-evidence-loss.py` was absent (file discovery returned `Skipped missing paths`). This does not prevent delivering this proposal; L1 must supply the integrated evaluator before exercising it. The accounting/provenance control must pass the same evaluator before a mutant can be judged. This report makes no claim that its hashes or commit references have already passed validation.

```sh
TMPDIR=/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch \
python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-21/build/MutLostIdentity/probe-lost-identity.py \
  --root /home/vgpnk/Projects/shokunin/mori-shokunin \
  --required .ufo/waves/round-21/frozen/required.json \
  --accounting corpus/evidence/loss-accounting-r21.json \
  --evaluator tools/mori-evidence-loss.py
```

This command was **not run**. It is restricted to the assigned lane root and named seat directory. The child receives the required explicit TMPDIR and no copied private environment. The script does not create commits or synthetic settlement evidence.

## Verdict and restoration evidence contract

- **Killed / runner rc0:** pristine and restored controls match every expected value, mutant output is usable and matches every mutation expectation, all frozen hashes remain stable, and source accounting is restored exactly.
- **Survived / runner rc1:** pristine/restored controls pass, but a usable mutant audit fails the specified omission/blocking expectations. This is a coverage finding, not permission to alter the contract.
- **Inconclusive / runner rc2:** baseline/restored failure, missing/malformed detector output, audit setup/timeout/abnormal exit, input drift, source drift, or failed restoration. An expected baseline audit rc1 is not itself a failure.

Future actual output is saved per phase as `pristine|mutated|restored.stdout.json` and `.stderr.txt`, with a `result.json` receipt under the fresh seat-local run directory. The receipt records actual command, returncode, observed JSON/issues, raw-output hashes, original source paths/hashes, per-phase copied-input before/after hashes, expected pristine/mutated/restored accounting hashes, final restored hash, exact-byte comparison, expectation failures and verdict. Runner stdout also emits that receipt.

Both nested and outer `finally` restoration paths write the original accounting bytes (`probe-lost-identity.py:225-233,243-250`); source before/after hashing is at `probe-lost-identity.py:189-190,252-259`. No experimental before/after hashes or restoration success are claimed here because no mutation was applied and no target was executed. Syntax, build, lint and behavioral checks were not run, as instructed. All future kill/survival/restoration conclusions remain for L1's authorized run.
