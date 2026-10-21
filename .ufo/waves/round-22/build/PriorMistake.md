# PriorMistake — round21 lesson mined for round22 C1 (retention reconciliation)

Seat: MoriR22.PriorMistake (scout, read-only). Inputs opened: `corpus/lessons/round-21.md`,
`.ufo/waves/round-22/contract.md`, and the directly referenced public receipts
`.ufo/waves/round-21/evidence/final/{summary,retention-floor,retention-floor-entering,fixture-original-control,fixture-trust-refinement}.json`,
plus the policy/allowlist blobs named in those receipts' argv
(`.ufo/waves/round-18/frozen/c1-policy.json`, `corpus/evidence/retention-allowlist.json`).
Methods: JSON field/count projections (no matched text printed or copied) and read-only
`git -C … rev-parse / merge-base --is-ancestor`. No tests, builds, gates, tool runs, installs.
No session, journal, config or credential reads. No tool installs or updates.

## Axes

A1 denominator identity (populations equal by identity set + named exclusions, not by subtraction);
A2 clearance separation (reconciliation agreement ≠ privacy clearance);
A3 preserved red controls (retention rc1 / metric4, permission control RED 11/12);
A4 fail-capability (each fix has a fixture or mutant that can flip it).

## Observed facts (receipt `retention-floor.json`, scanned commit 9fb1f911…, wrapper exit 1)

| Partition | Count | Source |
|---|---|---|
| `hits` (raw) | 95 | stdout list, 0 duplicate (path,line,class,line_sha256) identities |
| `allowlisted_hits` | 86 | equals allowlist `rows` count 86 |
| `unallowlisted_hits` = `metric` | 4 / 4 | all at `.ufo/waves/round-20/falsify/NoHarmRun/rg/.ufo/waves/round-18/frozen/c1-policy.json` (a committed **copy** of the policy) |
| `non_author` | 5 (count only; no identity list in receipt) | the 5 hits outside allow∪unallow are exactly at `corpus/lessons/round-17-verifier-spotcheck.md` (3) and `round-18-verifier-spotcheck.md` (2); both match `non_author_paths_glob` |
| hits at the **supplied policy path** `.ufo/waves/round-18/frozen/c1-policy.json` | 4 (R2,R5,R6,R8) | all 4 allowlisted (4 allowlist rows on that path) |
| `routed` / `forbidden_allowlist` / `warnings` | 0 / 0 / 0 | |

Partition check: allow(86) ∩ unallow(4) = ∅; hits − (allow ∪ unallow) = 5 = `non_author`. So
95 = 86 + 4 + 5 holds by identity, not only by count.

`retention-floor-entering.json`: argv `--rev` and stdout `commit` = e9f340ce… (entering revision),
but wrapper `measured_revision` = 9fb1f911… (the revision of the repository the tool ran from). Its hit, allowlisted and
unallowlisted identity multisets are **identical** to the final receipt. Ancestry: e9f340 → 9fb1f9 → 77a5bbe
(both `--is-ancestor` rc0). Policy blob 8bf285bd… and allowlist blob f8be55b1… are byte-identical at all
three revisions; file sha256 of the policy matches receipt `policy_sha256` prefix db06e981….

Allowlist rows carry (path, class, line_sha256, rule, reason) — **no line number**.

## Disagreements to mine

### D1 — the "raw95 incl 5 policy-source / scanner90" debt does not reproduce from the r21 receipt (A1)

The contract open-debt line says that raw95 includes 5 policy-source hits and that scanner90 includes 4 unallowlisted.
The opened receipt shows 4 hits at the supplied policy path, not 5. 95 − 90 = 5 coincides with
`non_author` = 5 (the two verifier-spotcheck lessons). Under the contract's own definition
("secondary scanner-compatible denominator removes that one source file only"), this receipt gives
**scanner_total = 95 − 4 = 91**, policy_excluded = 4, scanner_unallowlisted = 4, raw_unallowlisted = 4.
[INFERENCE] The 90 came from subtracting the non-author count. That is the count-subtraction error the round22 root lesson
forbids. Unresolved: no opened referenced evidence contains a 90 or a "scanner" receipt (targeted grep of
`.ufo/waves/round-21/evidence` returned no matches), so a separate scanner run with its own population
cannot be excluded. Consequence: frozen real-receipt expectations MUST NOT hard-code scanner_total=90 or
policy_excluded=5 without a receipt that produces them. Non-author exclusion (5) and policy-path exclusion (4)
are distinct populations and must be reported separately (R12 vs R03/R04).

### D2 — scoping policy exclusion by path is what keeps the red control red (A1, A3)

The 4 unallowlisted hits are at a policy **copy** path, and the 4 policy-path hits are already allowlisted.
So with exact supplied-path exclusion, both raw_unallowlisted and scanner_unallowlisted stay 4. That gives the contract's R02 its real-data
value. Any broadened exclusion (suffix match on `…/frozen/c1-policy.json`, basename, content digest equal to
policy bytes, or "policy-like" regex) also removes the copy, and the result becomes scanner_unallowlisted = 0. That is
reclassification that makes red look clean. Fail-capable comparison: R03/R04 fixtures SHOULD
include a committed copy of the policy at a second path carrying ≥1 unallowlisted hit, and a mutant that
matches by suffix/basename/digest MUST flip scanner_unallowlisted to 0 and be killed. The r21 lesson (line 140) correctly states
"identical inherited synthetic-policy copy lines" but reports only metric 4→4 and `same_findings: true`
(summary.json). It gives no denominators, so a later round could not tell copy hits from policy-path hits.

### D3 — receipt revision field is ambiguous and the real receipts cannot catch mis-binding (A4)

The contract requires the "receipt target measured_revision" to be a full commit that is an ancestor of the input revision. The
wrapper field `measured_revision` is the repository revision the tool ran from, not the scanned target (the entering receipt shows 9fb1f9 vs scanned e9f340).
Because hits are identity-identical at e9f340 and 9fb1f9, recomputing at the wrong one of these
still yields RETENTION_RECONCILED. Real receipts cannot detect this mis-binding. Requirement to make it fail-capable:
bind the recomputation commit to argv `--rev` and stdout `commit`. Fail closed (2) if they disagree or are not full
commits. Record the wrapper `measured_revision` separately in provenance (R24). Use a synthetic fixture
where the two revisions differ in hit identities. Then a wrapper-field mutant returns 1/2 instead of 0. R15/R16
(changed policy/allowlist bytes) are likewise synthetic-only, because the blobs are unchanged across e9f340→77a5bbe.

### D4 — non-author partition exists only as a count (A1)

The receipt has `non_author: 5` but no identity list. Reconciliation has to derive the set
(hits matched by `non_author_paths_glob`, independent of allowlist) and assert |derived| = 5. It then has to assert that
allow ∪ unallow ∪ non_author = hits as a disjoint identity multiset, and that metric = |unallow|. A count-only check passes
a receipt that moves a hit from unallowlisted to non-author while keeping the totals unchanged. R10 "metric lie" SHOULD include such a
partition-swap variant where the counts are unchanged. Unknown: whether the existing gate's glob uses fnmatch (where `*` also matches `/`)
or segment-aware matching. Both of today's paths match under either reading, so no real receipt distinguishes the two. I did not open the gate source.

### D5 — allowlist identity omits line (A1, A4)

Allowlist rows match on (path, class, line_sha256). One row covers every same-content line in that file,
so the allowlist partition is invariant to line edits. R08 (altered line) still fails via hit identity,
but a fixture with two identical-content lines in one file is needed to exercise the multiset handling of
R19 (receipt duplicates rejected) and to separate it from legitimate recomputed duplicates.

### D6 — clearance and red controls are separate axes; r21 already shows the pattern (A2, A3)

r21 kept two opposite-sense receipts side by side instead of reclassifying. The original fixture control is rc1 at 11/12
(`fixture-original-control.json`), and the explicit `--trust-refinement` mode is rc0 at 12/12. The round22 analogue is
reconciliation exit 0 with retention_state=red, raw/scanner_unallowlisted=4 and privacy_clearance=false, all
asserted together. Mutants to kill: (a) privacy_clearance derived from receipt_match or from zero delta; (b)
retention_state derived from reconciliation exit; (c) a suffix/basename/digest policy exclusion (D2). Round22
does not change the original permission control: it remains RED 11/12, and neither receipt above may be rewritten.

## Carried r21 lesson points relevant to scope

- M3 (identity/index drift): cite populations by identity plus digest, never by observed count or index alone. Same
  root as D1.
- "Zero delta / no new hits" is not clearance (lesson 140–142; summary qualification). Keep that phrase in r22 output.
- The audit is a negative-only observation prerequisite (lesson 101–105). A RETENTION_RECONCILED result is equally not
  an authorization, pin or lifecycle disposition.

## Remaining unknowns

- The origin of "scanner90" and "5 policy-source hits" (D1). It needs the receipt L1 used. It is not in the opened evidence.
- The existing gate's glob, split and NUL semantics. I did not read the gate source, by scope.
- Both historical wave dispositions: still unknown. Baseline acceptance: still blocked. Nothing here changes that.

Confidence: facts in the table are high (direct JSON projection). D1's arithmetic is high, and its cause is [INFERENCE].
D2–D5 are design consequences of observed field shapes and have not been exercised.
