# AuditTypes — pre-implementation type-confusion probe

Axes: strict JSON type integrity; prevent false historical settlement/pin allowance; minimal schema-local change.

## Finding — accounting disposition must not be truth-tested as a boolean

**Concrete counterexample:** an accounting row with `state: "disposed"` and `independent_disposition: true` is malformed. Contract line 14 requires an object carrying provenance plus `independent: true`, a distinct actor, explicit wave id, and a settlement/cleanup-accounted disposition. `true` is not that object and must never resolve the row or permit pinning. A truthiness/presence check (or coercion) could accept it and erase the intended block. The same field name is deliberately a **boolean** in classifier cases at contract line 15, but **object-or-null** in accounting; do not share a truthiness-based check across those schemas.

The corresponding rule/case probe is `evidence_loss_blocks: 1` (or a case boolean supplied as `0`/`1` or `"false"`): each violates the declared boolean type. In particular, `bool("false")` is `True`, and Python's `bool`/`int` relationship makes permissive integer checks unsafe. No integer-valued input field is declared by this interface; numeric substitutes must not be coerced into booleans or strings. Null is permitted only for an unresolved accounting row's `independent_disposition`; required provenance and other typed fields must not be treated as null/false/empty substitutes. Frozen examples confirm these field roles: `frozen/cases.json:5-10`, `frozen/before-rule.json:2-5`, `frozen/required.json:5-10`.

**Smallest safe change:** validate types per schema before the existing decision logic: require actual booleans (`type(value) is bool`) for rule/case flags and `independent`; require an accounting disposition to be exactly null in the unresolved branch or an object in the disposed branch; validate its required fields and require `independent is True`. Require declared string identifiers/enums/provenance fields to remain strings. Do not use `bool()`, `str()`, numeric equivalence, or generic truthiness to normalize input. Keep the accounting and case validators separate for their differently typed `independent_disposition` fields.

## Evidence and limit

The contract is explicit at `contract.md:14-15`. The requested implementation file `tools/mori-evidence-loss.py` was not present when checked, so this is a concrete pre-implementation rejection case, **not a finding against observed implementation behavior**. No implementation diagnostics or runtime result are available. The `lsp_status` route is not mounted in the available devices. No tests were run and no production files were changed.