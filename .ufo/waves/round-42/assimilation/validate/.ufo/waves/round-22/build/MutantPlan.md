# Round22 — three nonexecuted mutation designs

## Scope and axes

Axes: exact hit-identity fidelity; raw/scanner denominator separation; privacy non-escalation; independent detector strength; isolation and byte restoration.

**Design only.** No mutation, detector, CLI, selftest, build, test, linter, formatter, gate, or smoke run was executed. No scratch fixture or clone was created. Only this assigned report is written; no production, fleet, sibling, configuration, or historical evidence bytes are changed.

Authority read in full: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-22/contract.md`. Requirement membership was read from `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-22/frozen/requirements.json`. Existing receipt partition semantics were inspected at `/home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-retention-gate.py`, particularly `_scan_result`; that gate must not become the recomputation oracle.

The proposed target is `/home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-retention-reconcile.py`, **in a separately assigned disposable copy only, never in that production location**. The tools directory did not contain that new implementation at inspection, and `/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/round22` was absent. Consequently the snippets below specify semantic mutation sites, not observed implementation symbols, line numbers, or applied patches. Bind each to its corresponding existing expression after integration; do not refactor the implementation just to create a mutation site. No scratch ownership is assigned by this report.

## M1 — replace exact hit equality with count equality

**Smallest behavior-bearing change:** at the authoritative receipt-versus-recomputed hit-identity comparison, replace multiset equality with list-length equality. Keep schema checks, duplicate-hit rejection, counts, partitions, and provenance handling unchanged.

Illustrative semantic before/after; identifiers are explanatory, not claimed source names:

```python
# Before: hit_key includes path, line, class, and line_sha256.
hits_equal = Counter(hit_key(h) for h in receipt_hits) == Counter(hit_key(h) for h in raw_hits)
# Mutant:
hits_equal = len(receipt_hits) == len(raw_hits)
```

**Bounded detector:** frozen R07, with R01 as the valid-receipt positive control. Start with the committed synthetic valid receipt. Replace one non-policy, unallowlisted hit digest with a different valid 64-hex digest, without creating a duplicate. Keep path, line, class, list cardinalities, metrics, and receipt exit unchanged. Update any repeated representation of that same receipt identity consistently so the input remains well-formed; do not modify the independently recomputed tree or policy/allowlist. Keep the R07 fixture fixed across pristine, mutated, and restored executions.

**Expected killed requirement/control:** R07 (altered digest must return exit 1 and `RETENTION_RECONCILIATION_MISMATCH`); R01 must still return exit 0 and `RETENTION_RECONCILED` on its separate unchanged fixture. Count-changing R05/R06 alone are insufficient to kill this mutation.

**[INFERENCE] Expected mutant signature:** if the selected expression is authoritative, the same-cardinality wrong identity can be accepted as exit 0 / `RETENTION_RECONCILED`, failing R07. A setup error is not the required R07 behavior. If another untouched identity check still rejects it correctly, this particular one-site mutant may survive; record that observation rather than weakening another check or changing the fixture after seeing the result.

**Actual detector output:** not run. **Verdict:** NOT RUN — proposed mutation, neither killed nor survived.

## M2 — clear privacy on receipt agreement

**Smallest behavior-bearing change:** replace the literal false privacy value at final result construction with the receipt-agreement boolean. Do not alter reconciliation exit selection or retained-red accounting.

```python
# Before:
"privacy_clearance": False,
# Mutant:
"privacy_clearance": receipt_match,
```

**Bounded detector:** frozen R02, using an independently expected valid receipt that exactly agrees while both `raw_unallowlisted` and `scanner_unallowlisted` are positive. Require exit 0, `RETENTION_RECONCILED`, `receipt_match is True`, `retention_state == "red"`, and `privacy_clearance is False`. The last check is an exact JSON boolean check, not truthiness or an exit-code proxy. Expected values must not be derived from the mutated tool.

**Expected killed requirement/control:** R02, agreement is not privacy clearance. The detector must not demand a reconciliation failure merely because retention is red.

**[INFERENCE] Expected mutant signature:** exit 0 and the same agreement/red accounting, but `privacy_clearance` becomes true; R02 fails despite the unchanged successful reconciliation exit.

The original permission control remains RED11/12. A detector result cannot repair that control, authorize retention, or establish either unknown historical disappearance disposition.

**Actual detector output:** not run. **Verdict:** NOT RUN — proposed mutation, neither killed nor survived.

## M3 — remove the exact policy-source exclusion

**Smallest behavior-bearing change:** delete only the exact supplied-policy-path predicate from construction of the scanner population. Keep the raw scan, policy-path resolution, separately reported excluded identities, allowlist, and non-author rules unchanged. Do not broaden or remove any unrelated exclusion.

```python
# Before:
scanner_hits = [h for h in raw_hits if h["path"] != policy_path]
# Mutant:
scanner_hits = [h for h in raw_hits]
```

**Bounded detector:** frozen R03 and R04 on the same committed synthetic fixture: `raw_total == 5`, exactly one policy-path hit, and `scanner_total == 4`. Independently form identity multisets using `(path, line, class, line_sha256)` and require:

- the policy-excluded identity multiset is exactly the raw identities whose path equals the supplied policy path;
- the scanner identity multiset is exactly raw minus that multiset;
- no policy-path identity remains in scanner output and every non-policy identity remains;
- raw equals the disjoint scanner-plus-policy-excluded accounting, with multiplicities preserved.

Also retain the fixture's expected exit 0 / `RETENTION_RECONCILED` and `privacy_clearance is False`; those alone do not detect a denominator defect. R03/R04 must inspect actual scanner identities and independently expected counts, not a total obtained by subtracting two values reported by the same tool.

**Expected killed requirement/control:** R03 (5/1/4 denominator requirement) and R04 (exact policy-source exclusion by identity).

**[INFERENCE] Expected mutant signature:** scanner identities include the policy hit and scanner cardinality becomes 5, while raw remains 5. If displayed metrics are separately computed as 5 minus 1 and still say 4, R04's identity assertion must still kill the mutant. If the tool instead rejects its own inconsistent result, the unchanged valid-fixture exit/finding control must detect that regression.

**Actual detector output:** not run. **Verdict:** NOT RUN — proposed mutation, neither killed nor survived.

## Execution and restoration contract — not authorization to run

These three cases are independent alternatives, never cumulative mutations. Current wave restrictions prohibit execution; only L1 may later measure after integration and separately authorize any scratch probe.

For any authorized future probe:

1. Use only the exact isolated copy assigned to that probe under `/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/round22`, with `TMPDIR=/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch`. Do not borrow or modify an executor's copy. No deliberate output goes to `/tmp`.
2. Freeze detector, fixture, expected outputs, and invocation before mutation. Preserve pristine target bytes and their SHA-256 outside the scanned fixture tree. Record fixture/policy/allowlist/detector identities and executing-tool SHA-256 so only the intended target bytes differ between arms.
3. Run the same bounded detector on pristine, then the one-site mutant, then exact restored bytes. Record real exit codes, finding IDs, sanitized assertions, and before/mutated/restored hashes. The executing-tool hash necessarily changes for the mutant; retain it as provenance rather than treating the change itself as a detector failure.
4. Restore exact pristine bytes in unconditional cleanup even if invocation or parsing fails. Confirm restored hash equals pristine hash and run the unchanged detector on restored bytes. No whole-suite, sibling-source, production-evidence, session, process, service, journal, or configuration probe is part of these designs.
5. Call a mutant **killed** only when pristine and restored satisfy the intended detector and mutated bytes trigger the specific contract assertion. A failed prerequisite/baseline, failed restoration, crash unrelated to the planned assertion, or absent capability is inconclusive, not a killed mutant. A passing mutant is a survival/coverage finding; never alter the contract to manufacture a kill.
6. Retain minimized evidence only: hashes, numeric counts, boolean assertions, sanitized finding IDs, and statuses. Never retain or print matched line text, unsanitized stderr/exception bytes, or credential/session content.

## Evidence ledger

| Mutation | Planned detector | Actual output | Verdict | Before / mutant / restored SHA-256 | Restoration evidence |
|---|---|---|---|---|---|
| M1 count-only equality | R07; R01 control | Not executed | NOT RUN | Not collected; no mutation applied | No source bytes changed; no restoration operation performed |
| M2 agreement grants clearance | R02 | Not executed | NOT RUN | Not collected; no mutation applied | No source bytes changed; no restoration operation performed |
| M3 missing policy-source filter | R03 + R04 | Not executed | NOT RUN | Not collected; no mutation applied | No source bytes changed; no restoration operation performed |

No pass rate, killed count, behavioral output, source hash, or restoration hash is claimed. The contract-stated retained 95 raw / 5 policy-source / 90 scanner, four unallowlisted, and zero new hits are not measurements from this seat. Both historical dispositions remain unknown and baseline acceptance remains blocked. A source hash would identify bytes, not establish secrecy, authenticity, or privacy clearance.

Tools installed or updated: none; version/channel/reason not applicable.
