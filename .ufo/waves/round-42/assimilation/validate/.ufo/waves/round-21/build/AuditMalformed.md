# AuditMalformed — round 21

## Finding — Medium: rc2 for malformed/missing-schema inputs is not demonstrated, and the current measurement oracle can accept an rc2 audit as clean

**Contract.** `.ufo/waves/round-21/contract.md:14` defines the `mori-required-observations-v1` and `mori-loss-accounting-v1` input schemas and specifies `rc2` for setup/input failure. The target evaluator is not available in the current `tools/` inventory or in `.scratch/round21/ImplLoss/tools/`, so I cannot claim an observed evaluator failure.

**Concrete counterexample to the current measurement path.** `.ufo/waves/round-21/oracle-loss.py:27-30` loads `required['observations']` and checks only non-empty/unique IDs; it does not check the required schema. A file such as `{"observations":[{"id":"probe"}]}` (missing `schema`) passes that check. The oracle records the child exit code at `:41`, but `:55-57` only flags an `omitted` mismatch, and `:86` returns success only when its `issues` list is empty. Thus, **[INFERENCE]** if the audit CLI correctly exits 2 for that input but emits a JSON error object whose `omitted` equals the independently calculated count, this oracle can still produce no instrument issue and return 0. No such target result was run or observed.

The independent fixture matrix also has no malformed-JSON or missing-top-level-schema input case: `.scratch/round21/FixtureLoss/fixture-loss.py:248-305` enumerates the current 11 cases, all focused on valid JSON observation/provenance rows and their evidence mutations. Its parser at `:330-338` validates the *audit output* schema, not malformed input behavior. The associated report confirms no target runs were performed (`.ufo/waves/round-21/build/FixtureLoss.md:30-37`).

**Smallest safe change.** At the public CLI boundary, reject unreadable/invalid JSON, non-object documents, and absent/wrong expected schema before audit/classification logic; report these as setup/input errors with `rc2`, never as a healthy/empty/missing observation result. Add black-box cases for malformed JSON and schema-less documents with otherwise valid observations, asserting `rc2` from `audit` (and the equivalent input files for `classify`). Also make the measurement oracle flag unexpected child exit codes rather than judging audit success from the `omitted` counter alone. These are narrow error-path checks; no redesign is needed.

## Residual risk

No implementation-level result is available: `tools/mori-evidence-loss.py` is absent from the observed production `tools/` listing and from the isolated implementation clone. Therefore the actual rc for malformed JSON or a missing schema remains unknown; the counterexample above is to the current oracle's acceptance logic, conditional on an rc2 result object containing a matching `omitted` value.

## Verification gaps

- LSP status/references/definition/diagnostics could not be obtained: `read xd://lsp` returned “No such tool” and the mounted-device inventory did not expose an LSP device. Source reads and literal search were used for discovery; grep output is not treated as semantic proof.
- No target CLI invocation, tests, build, lint, or production write was performed.
