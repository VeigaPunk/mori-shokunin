# KnownGaps — round 22 frontier scope and historical index row

Seat `MoriR22.KnownGaps` (scout, read-only). Inputs: `corpus/README.md` (414 lines, sha256
`5a5aec4f3c68375120e2ff8978be170a87c8859298ae6b19246254ee994b14f1`, blob `c78173c3…` at both
entering `77a5bbe8…` and HEAD `306e06ec…`, i.e. unchanged by the two round-22 commits),
`.ufo/waves/round-22/contract.md` (sha256 `1658c390…` = `frozen/requirements.json`
`contract_sha256`), and the public evidence the README or contract points at directly:
`corpus/knowledge/evidence-minimization-r18.md`, `.ufo/waves/round-21/evidence/historical-provenance.json`,
and the r21 `mori-r21-command-receipt-v1` retention receipts under `.ufo/waves/round-21/evidence/final/`.
Only path, class, line, digest and count metadata was read from the receipts. No matched text
appears below. No tests, builds, or measurements were run, and no tools were installed.

## 1. Current frontier (observed)

- `## Frontier` (`README.md:328-342`) lists FR1–FR14. None of them is retention,
  evidence minimization, or receipt reconciliation. Retention is own-lane hygiene ground
  indexed only in `## Round19 retrospective index repair (not new growth)`
  (`README.md:379-395`, row `knowledge/evidence-minimization-r18.md`, "Frozen regex floor plus
  content adjudication; line digests are provenance, not secrecy").
- The most recent growth table is `## Round-20 coverage additions` (`README.md:397-403`):
  FR3 per-seat wave settlement, plus the drift re-pin. The latest section, `## Round21
  correction` (`README.md:405-414`), demotes the r20 re-pin row to historical and records
  "FR3 independent lifecycle disposition remains frontier; retaining unknowns does not grow
  authoritative settlement coverage."
- Precedent: round 19 labelled a retrospective index fix as "not newly explored frontier
  ground" (`README.md:394-395`), and round 21 used a "correction" heading. The README has no
  round-22 text yet.

## 2. Calibration repair versus expansion

| Question | Round-22 C1 | Why |
|---|---|---|
| Advances any FR1–FR14 boundary? | No | The contract claims calibration only (`contract.md:3`), and its subject is the lane's own retention receipt, not a surface listed in `## Frontier`. |
| New coverage ground? | No | Same ground as the existing r18 row: the R-class floor, the allowlist, and `non_author_paths_glob`. The new tool recomputes an existing receipt and changes nothing in the retention gate, policy, allowlist, or history (`contract.md:16`). |
| New public sources? | None admitted at this clock | `contract.md:22` allows source rows only after they are opened, with a located quote. Admission is decided by the outside closure. |
| Capability acquisition? | Yes, as calibration | Before is `capability_absent` (`frozen/requirements.json` `before_kind`). |
| Privacy clearance? | No | `privacy_clearance=false` is fixed. A matched receipt, or a zero new-hit delta, is not clearance (`contract.md:5,14`). |
| FR9 durable fixtures | Adjacent, not advanced | `contract.md:20` requires the fixture generator to be committed before integration. That meets FR9's precondition for this tool only [INFERENCE]; it is not lane-wide FR9 closure and should not be indexed as such. |

Conclusion: index round 22 under a non-growth heading, as rounds 19 and 21 did, and add no row
to the `## Frontier` table or to any "coverage additions" table.

## 3. Proposed historical index row (draft, unmeasured)

Proposed for L1 to append after `README.md:414`. The row contains no measured values; L1 adds
its receipt path and observed values only after measuring.

```markdown
## Round22 calibration — retention receipt reconciliation (not new growth)

| Existing ground | Entry | Scope retained |
|---|---|---|
| Own evidence retention (r18 row) | `tools/mori-retention-reconcile.py`; requirements `.ufo/waves/round-22/frozen/requirements.json` | Independent recomputation of an existing r21 retention receipt from Git blobs at its measured revision: raw hit multiset by (path,line,class,line_sha256), allowlist/non-author/forbidden partitions, and exactly-one-path policy exclusion reported separately. The raw denominator stays authoritative. Agreement is accounting, not privacy clearance (`privacy_clearance=false`); retained unallowlisted hits stay red. R21 permission control RED11/12, unknown disappearance dispositions and blocked baseline acceptance carry unchanged. |
```

## 4. Gaps found in the direct evidence (observed)

The committed r21 receipt `.ufo/waves/round-21/evidence/final/retention-floor.json` (commit
`77a5bbe`, sha256 prefix `4001e2d9…`, wrapper `measured_revision` `9fb1f911…`, `exit_code` 1,
`finding_id` `RETENTION_FINDINGS`) partitions as: 95 hits = 86 allowlisted + 4 unallowlisted +
5 non-author, with 0 forbidden-allowlist entries, `metric` 4, and no duplicate hit identities.

**G1. The policy denominator does not equal 5/90 under the contract's exact-path rule.**
`contract.md:7` says "raw95 includes5policy source hits, scanner90". Exact-path exclusion of
`.ufo/waves/round-18/frozen/c1-policy.json`, as `contract.md:14` requires, gives:

| Quantity | Value | Where it comes from |
|---|---|---|
| Hits on the policy path | 4 | Classes R2, R5, R6, R8, all allowlisted |
| Scanner total | 91 | 95 − 4 |
| Scanner unallowlisted | 4 | The policy-path hits are all allowlisted, so none are removed |

The figure 5 matches the receipt's `non_author` count instead; those hits sit on 2 other paths,
none of them the policy path. 95 − 5 = 90 [INFERENCE]: the "scanner90" figure may subtract
non-author hits, or may come from a different scanner that was not opened here. The source of
the 5/90 figures is unresolved. This does not affect the synthetic R03 arm
(5/1/4 is a fixture), but any oracle or acceptance text that expects policy_excluded=5 and
scanner_total=90 on the real r21 receipt will disagree with exact-path recomputation.

**G2. The four retained unallowlisted hits are on a copy of the policy file, and they must stay.**
All 4 unallowlisted hits are on
`.ufo/waves/round-20/falsify/NoHarmRun/rg/.ufo/waves/round-18/frozen/c1-policy.json`. At HEAD
that path holds the same Git blob (`8bf285bd…`) as the real policy file, and its 4 hit
(line, class, digest) tuples equal the policy path's 4 exactly. Under exact-path exclusion
they stay in the scanner population, which matches `contract.md:5` ("must continue to show
four unallowlisted hits"). Any basename, glob or content-identity exclusion would drop them and
falsely report clean. Mutation arms should target this case [INFERENCE: these are probably not
private-data lines, since they are copies of the policy text; privacy is not adjudicated here,
and the hits must not be cleared on that basis].

**G3. The `-entering` receipt's wrapper names a different revision than its own scan.**
In `.ufo/waves/round-21/evidence/final/retention-floor-entering.json` (sha256 prefix
`87899139…`):

| Field | Value |
|---|---|
| Wrapper `measured_revision` | `9fb1f911…` |
| argv `--rev` | `e9f340ce…` |
| stdout `commit` | `e9f340ce…` |

Its hit lists equal the other receipt's, so a tool that recomputes only at `measured_revision`
would return `RETENTION_RECONCILED` on a receipt whose scan ran at a different commit. The
contract (`contract.md:10,12`) binds `measured_revision` as an ancestor, but it does not
require `measured_revision == stdout.commit == argv --rev`, and requirement R13 tests only
mismatched or unresolvable revisions against the input. The contract leaves this ambiguous;
the safer reading is exit 2 (setup error, inconsistent fields) [INFERENCE]. The wrapper's
`measured_revision` does equal its stdout `commit` in `retention-floor.json`.

**G4. Input-stability preconditions hold for the real receipt.**
The policy (`8bf285bd…`) and allowlist (`f8be55b1…`) blobs are identical at `9fb1f911` and at
HEAD, and `9fb1f911` is an ancestor of HEAD. For the real receipt, R15 and R16
(changed policy/allowlist bytes) should not fire; only their fixtures exercise them.

## 5. Unresolved

- Where the contract's 5/90 figures come from (G1). Resolving it needs the r21 scanner source,
  which this seat did not open.
- How `measured_revision` should be checked against stdout `commit` and argv `--rev` (G3).
  This is L1's contract decision.
- No session, journal, config or credential surface was read, and nothing was measured.

## 6. Checks for L1 after integration

Run `tools/mori-retention-reconcile.py check` against `retention-floor.json` at the real
inputs. Expected observations under exact-path exclusion, to be measured rather than assumed:
raw_total 95, policy_excluded 4, scanner_total 91, unallowlisted 4 in both populations,
non_author 5, forbidden_allowlist 0, `privacy_clearance=false`. Also run it against the
`-entering` receipt to see how G3 is handled.
