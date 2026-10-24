# AttackR09 — critic report on frozen R09 ("altered class returns 1")

Seat: MoriR22.AttackR09 (critic). Static review only. No tests, builds, or tool runs of either the gate or the reconciler. No installs.
Inputs read: `.ufo/waves/round-22/contract.md`, `tools/mori-retention-gate.py` (full), the r21 receipt `.ufo/waves/round-21/evidence/final/retention-floor.json` (field shape and metadata counts only, no matched text), the frozen policy at r21 measured revision `9fb1f911…`, and `build/swarm-registry.json`. At review time, no Impl/Fixture/Oracle candidate exists in `build/`; all three members have `agentId: null`. Nothing was waited on or polled.

## Verdict

R09 is the requirement most exposed to a superficial pass. Changing a hit's `class` leaves every count the contract names unchanged: `hits` length, `metric`, `non_author`, `routed`, receipt `exit_code` and `finding_id`, per-path counts, and per-line counts. A reconciler that checks counts, exit and finding_id, or each field as a separate projection, returns 0 RETENTION_RECONCILED on a tampered receipt. R09 also collides with R19 (duplicate hit, exit 2) and with the unspecified "unknown class id" case. A careless fixture can therefore "pass" R09 through exit 2, or give it a nondeterministic expectation.

## Observed facts from local evidence (metadata only)

- In the receipt `stdout`, five lists carry `class`: `hits`, `unallowlisted_hits`, `allowlisted_hits`, `forbidden_allowlist` (`line: null`), and `warnings` (stale rows, `line: null`). Hit fields are exactly `path, line, class, line_sha256` (`HIT_FIELDS`, gate line 31).
- The gate emits one hit per matching class per line (`_blob_hits`, gate lines 89–103). Its selftest arm `multi-class-line` proves that one line yields R4 and R6 hits with an identical `(path, line, line_sha256)`.
- In the real r21 receipt there are 95 hits, and 15 lines match more than one class, accounting for 46 of those hits. 44 of the 46 are in `allowlisted_hits`; none are in `unallowlisted_hits` (4 hits, all single-class lines).
- Classes R1 and R3 never occur in the real r21 receipt. Altering any real hit to R1 or R3 therefore cannot create a duplicate identity.
- The allowlist key `(path, class, line_sha256)` has 0 collisions across the real 95 hits. Class is part of the allowlist binding, so a class change also changes allowlisted versus unallowlisted membership on recomputation.
- The real receipt is evaluable, so a real-receipt R09 arm is not masked by exit 2:
  - The policy blob SHA-256 at `9fb1f911…` equals the receipt's `policy_sha256` (`db06e981…`).
  - The policy and allowlist blob ids at `9fb1f911…` equal those at entering `77a5bbe8…`.
  - `9fb1f911…` is an ancestor of `77a5bbe8…`.

## Counterexample fixtures (concrete, deterministic)

### Synthetic tree at measured commit T

Input revision I is a child of T with byte-identical policy and allowlist. To avoid putting matched text in any artifact, reuse the gate's own base64 selftest payloads by name (`texts[...]` and `multi_text` in `tools/mori-retention-gate.py` lines 505–515 and 587). The selftest positive arms prove each `texts["Rk"]` hits exactly class Rk.

| path | line 1 | line 2 |
|---|---|---|
| `fixture/a.txt` | `texts["R5"]` (R5 only) | `texts["R6"]` (R6 only) |
| `fixture/b.txt` | `texts["R9"]` (R9 only), allowlisted by one row `{path: fixture/b.txt, class: R9, line_sha256: <digest>, rule: "a"}` | — |
| `fixture/multi.txt` | `multi_text` (R4 and R6 on one line) | — |
| `corpus/lessons/round-3-verifier-spotcheck.md` | `texts["R8"]` (non-author) | — |
| the supplied policy path | committed policy (its own lines hit; whatever R03's FixtureReconcile fixes) | — |

The baseline receipt M0 is produced by the existing gate `scan` at T, wrapped in `mori-r21-command-receipt-v1`. Expected baseline: exit 0, `RETENTION_RECONCILED`, `receipt_match=true`, `privacy_clearance=false`.

### How to mutate

1. Parse `stdout`.
2. Change only the fields named below.
3. Re-emit exactly as gate `emit()` does: `json.dumps(sort_keys=True, separators=(",",":")) + "\n"`.
4. Leave wrapper `exit_code`, `argv`, and `measured_revision` unchanged.

If you re-serialize any other way, a canonical-bytes check could mask R09 with exit 2.

### R09 pass arms: every arm MUST give exit 1 and `RETENTION_RECONCILIATION_MISMATCH`

| arm | mutation | defeats |
|---|---|---|
| M9a | In `hits` only, change `fixture/a.txt` line 1 from R5 to R3 | count-only, exit/finding-only, and key=(path,line,sha) implementations |
| M9b | Make the M9a change in both `hits` and `unallowlisted_hits` (self-consistent receipt, metric unchanged) | checkers that only test the receipt's internal consistency |
| M9c | Swap classes R5↔R6 between `fixture/a.txt` lines 1 and 2, in both `hits` and `unallowlisted_hits` | per-field projections and per-path class counters; only full 4-tuple identity detects it |
| M9d | In both `hits` and `allowlisted_hits`, change `fixture/b.txt` line 1 from R9 to R1 | implementations that trust receipt partition placement instead of recomputing the allowlist join |
| M9e | Change one supplied-policy-path hit to a known class not already on that line | implementations that reconcile only the scanner population; raw is authoritative |
| M9f | Change the non-author hit from R8 to R3, in `hits` only | implementations that skip non-author hits |
| M9g | Change class only in `unallowlisted_hits` (`hits` intact) | implementations that validate only `hits` |
| M9h (real) | In the r21 receipt copy, change one of the 4 `unallowlisted_hits` (and its `hits` twin) to R1 | proves R09 on the actual retained receipt, which cannot collide |

### Oracle assertions per arm (all required)

- `exit == 1` and `finding_id == "RETENTION_RECONCILIATION_MISMATCH"`.
- `receipt_match is False`.
- `privacy_clearance is False`, and it is a JSON bool.
- `raw_total`, `policy_excluded`, `scanner_total`, `raw_unallowlisted`, `scanner_unallowlisted`, `non_author` and `forbidden_allowlist` equal the M0 values, because they are recomputed from the tree, not from the receipt.
- `retention_state` equals M0.
- No fixture payload bytes and no `multi_text` bytes appear in stdout or stderr.
- If the implementation exposes identity-delta counters, a single alteration must show exactly 1 missing and 1 unexpected identity, and M9c must show 2 and 2. A delta of 0, or any value derived from count subtraction, is a defect.

### Precedence and negative controls (not R09 passes; pin them so R09 cannot pass for the wrong reason)

| control | mutation | required result |
|---|---|---|
| N1 | On `fixture/multi.txt`, change the R4 hit to R6, the line's other matching class | Duplicate identity, so exit 2 per R19, never 1. The oracle MUST NOT count this as R09. Duplicate rejection precedes reconciliation. |
| N2 | Class changed to an id outside the frozen policy: `"R10"`, `"r5"`, `"R5 "`, `"Ｒ5"` (fullwidth), or `""` | Recommend exit 2 `RETENTION_RECONCILIATION_SETUP` with a sanitized code (for example `receipt_hit_unknown_class`). This mirrors the gate's allowlist rule `class_id not in known_classes` (gate line 147). It MUST NEVER be 0: no strip, casefold, or NFKC normalization. |
| N3 | Class as int, null, bool, or list | Exit 2 (type/schema, adjacent to R18). |
| N4 | Permute `hits` order with no content change | Exit 0. Identity is a multiset, so M9a–M9h must fail on content, not list order. An ordered-equality implementation passes R09 but breaks N4, which exposes it. |

## Semantic ambiguities L1 must freeze before integration

1. **Unknown class id (N2).** The contract does not say whether this is exit 1 (value disagreement) or exit 2 (schema inconsistency). Pick one and commit it in expected values. I recommend exit 2. Either way, the R09 fixture MUST use known, non-colliding classes only.
2. **R09 versus R19 precedence (N1).** Freeze "duplicate-hit rejection is evaluated before identity reconciliation". Otherwise R09 on multi-class lines is order-dependent. A random real-receipt class mutation lands on a multi-class line in 46 of 95 cases, about 48%.
3. **Scope of "altered class".** R09 must cover all class-bearing lists, not just `hits`. That means M9g, plus the `forbidden_allowlist` and `warnings` rows, which R11's forbidden fixture and a stale-row fixture can carry. Freeze that each list is validated as a multiset against recomputation.

## Out-of-scope counterexample to the denominator premise (for L1; affects R02 and R03, not R09)

Under the contract's own rule that policy-excluded means "exactly the supplied policy path", the r21 receipt has 4 hits at `.ufo/waves/round-18/frozen/c1-policy.json`, not 5. Excluding that path gives `scanner_total = 91`, not 90. The observed number 90 equals `raw_total − non_author` (95 − 5).

A second copy of the policy, under `.ufo/waves/round-20/falsify/NoHarmRun/rg/…`, also carries 4 hits. Excluding it would be a broad path exclusion, which the contract forbids.

[INFERENCE] The contract's "5 policy source hits" conflates the non-author partition (5) with the policy-source partition (4). Expected values for any real-receipt arm must be recomputed by identity before being frozen; "95 / 5 / 90" must not be copied from the contract.

## Smallest safe correction (actionable criterion)

Freeze this R09 criterion in expected values:

> For each of M9a–M9h, a receipt that differs from M0 only in one or more `class` values is reconciled. Each changed value is a known policy id, the change creates no duplicate `(path, line, class, line_sha256)`, and `stdout` is re-emitted canonically. The result must be exit 1, `finding_id = RETENTION_RECONCILIATION_MISMATCH`, `receipt_match = false`, `privacy_clearance = false`, and recomputed counters identical to M0. N1 must give exit 2 (R19). N2 and N3 must give exit 2, never 0. N4 must give exit 0.

The comparison must be the multiset of full 4-tuples on each class-bearing list. Count, exit, finding_id, and per-field checks are not sufficient.

Impacted axes: calibration (primary), depth. No production, policy, allowlist, or history edits made or proposed.
