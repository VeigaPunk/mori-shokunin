# FixtureLoss — round 21 audit fixture runner

## Result

Added `.scratch/round21/FixtureLoss/fixture-loss.py`. It is an independent harness: it creates synthetic evidence in per-case local Git repositories beneath the caller's `TMPDIR`, then invokes only the supplied tool's public `audit` CLI in a subprocess. It does not import target code, read live wave evidence, or write production state. `--tool PATH --output FILE` are required; the report output must be an absolute, not-yet-existing file with an existing parent directory.

The fixture matrix contains 12 cases, each invoked twice against identical inputs to detect unstable results:

- absent required observation;
- present unresolved observation with baseline/deletion/cleanup provenance and null disposition;
- structurally complete synthetic disposed positive control retained from the original contract;
- `wrong-baseline-v0`, retaining the original candidate's nonmatching baseline as a negative control;
- digest tamper;
- duplicate accounting identity;
- symlink escape with matching bytes;
- absolute path;
- `..` path;
- absent evidence file;
- `independent: false`;
- cleanup-only disposition with the cleanup actor reused.

The original contract control expects `rc=0` for a structurally complete synthetic disposed declaration; the other cases expect `rc=1`. Exact counts are asserted for omitted, unresolved, and disposed controls. Mutation cases assert blocked pin (`pin_allowed=false`), zero disposed, and the contractually required invalid/unresolved minimums. Every emitted `finding_id` must be nonempty; each case's sorted IDs and counts must match across its two invocations. The contract does not give literal finding-ID values or define whether invalid counts count rows or issues, so those are not guessed: IDs are tested for repeatability and malformed-row counts use explicit lower bounds. Per-run stdout/stderr, byte lengths, SHA-256, truncation status, return code, counts, and parse failures are retained in the output file.

## Interoperability reconciliation

The actual required file, `.ufo/waves/round-21/frozen/required.json`, is included in commit `8fed329636f53455ae2f53930c171c6186aff1fd`; it uses `baseline` as a provenance object but `evidence` as a nonempty path-and-line string (`frozen/required.json:5-11,14-20`). The runner now emits `"evidence/required-evidence.json:1"` for each synthetic requirement, rather than treating `evidence` as provenance.

Per MoriR21's tool-interface note, a disposed row's hashed JSON evidence must itself declare the observation `id`, `actor`, `disposition`, and `independent`. The committed synthetic disposition payload now binds those values. The false-boolean and same-actor fixtures keep payload and accounting metadata consistent, so each tests the intended rejection condition rather than a digest/metadata mismatch. No `mori-evidence-loss.py` implementation source was inspected.

The frozen required file contains `aggregator-r10` and `aggregator-r10-resume`; `.ufo/waves/round-21/evidence/historical-provenance.json:38-39` records no independent wave disposition and unknown settlement. This runner creates synthetic cases only and does not assert or fabricate real disposition for either observation.

## Baseline identity refinement

MoriR21's additional tool-author interface refinement requires each accounting observation's `baseline` provenance to equal its matching required observation's `baseline` exactly. All controls except `wrong-baseline-v0` now reuse the required baseline object. That named case preserves the original candidate's separate `evidence/row-baseline.json` reference and expects refusal (`rc=1`, `disposed=0`, `pin_allowed=false`, with invalid and unresolved counts at least one); it is an explicit negative control, not a target result.

The actual required baseline objects (`.ufo/waves/round-21/frozen/required.json:5-10,14-19`) match the actual accounting baseline objects (`corpus/evidence/loss-accounting-r21.json:7-10,29-32`) in path, revision, and SHA-256. No real independent dispositions are claimed.

## Trust refinement

`.ufo/waves/round-21/trust-refinement.md:5` strengthens the contract: `independent:true` plus different actor strings are structural evidence, not proof of external acceptance; a submitted disposed declaration alone must remain blocked as `EXTERNAL_REVIEW_REQUIRED` until outside review. The original positive-disposed case and `rc=0` expectation remain unchanged as the contract control. If the refined audit blocks that declaration, a later run will report an expected-versus-observed mismatch and retain the observed output; this is not a test pass and is not silently normalized.

The trust refinement supplies no authenticated external-review mechanism or fixture schema, so this runner does not invent one or add a guessed pass case. The frozen classifier's positive independence cases remain synthetic conditional policy examples (`trust-refinement.md:7`), not verification of real dispositions. Current retained accounting still has both required observations unresolved with null disposition (`corpus/evidence/loss-accounting-r21.json:5-23,25-45`); the runner does not claim otherwise.

## Retained evidence

- `.ufo/waves/round-21/contract.md:13-16` defines the audit schemas, provenance fields, path restrictions, count fields, expected `rc` meanings, and required self-test mutation categories. The runner's hardcoded entry revision is the contract's `e9f340ce986f82a60baad1b8e5ead655ab818a1c` (`contract.md:3`).
- `.ufo/waves/round-21/contract.md:7-9` states the freshness and calibration claims; this runner covers the assigned audit freshness mutations only.
- Initial `glob` of `tools/` listed the existing Mori utilities but not `tools/mori-evidence-loss.py`; initial `glob` of round-21 `build/` showed only `swarm-registry.json`. Therefore the target was not available in those initial inventories.
- Initial read-only Git observation: `git -C /home/vgpnk/Projects/shokunin/mori-shokunin rev-parse HEAD` returned `b9b8b440aa5a35123b5c273fa8fb028149801d0a`; `git show -s` resolved `e9f340c` to `e9f340ce986f82a60baad1b8e5ead655ab818a1c`. The checkout already had unrelated dirty/untracked work; this seat changed only its assigned runner and report paths.

## Runs and failures

No target runs were performed. The assignment said “No runs yet”; the target CLI was also absent from the initial `tools/` listing. Thus there are no observed target failures to report, and runner behavior against the eventual implementation remains unverified. No build, test, lint, formatter, or self-test was run.

## Risks / blockers

- Running the fixture matrix requires the integrated `tools/mori-evidence-loss.py`, Python, and `git`. The runner uses the contract's `--root`, `--required`, and `--accounting` audit arguments.
- The expected machine-readable schema is tied to `mori-evidence-loss-audit-v1` and requires an `issues` list and `finding_id` on each issue, following the contract's stable finding-ID requirement. If integration chooses a different representation, reconcile it against the contract before running; do not weaken the stability assertion silently.
- The output report captures target stdout/stderr up to 1 MiB each; oversize output is explicitly marked and hashed, and counts as a harness failure rather than being reported as complete.
- Only the C1 audit fixtures are in this runner. C2 rule-classification cases are outside this assigned mutation matrix.
