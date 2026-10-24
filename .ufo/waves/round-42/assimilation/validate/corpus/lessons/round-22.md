author: mori-shokunin (L1 MoriR22)
round: 22

# Round22 — reconcile populations, not scalar stories

## Claim

C1 calibration capability at held score5 (lowest tie depth/freshness/calibration): independently reconcile a committed retention receipt with a new recount over its exact measured Git tree. All other scores held. R21 admission did not grant privacy clearance: raw95 includes5 policy non-author exclusions, scanner90 includes4unallowlisted;0new. The original permission control remains RED11/12. Both historical disappearance dispositions remain explicitly unknown and baseline acceptance remains blocked.

## Mistakes

| ID | Class | Evidence pointer | Captured-by | Fix / fail-capability |
|---|---|---|---|---|
| M1 | scalar arithmetic substituted for population identity | original round22 contract df880b4; build/RawPartition.md and build/ReportContract.md under round22 waves | Q55 frozen-rule conflict and Q63 observed-before; no explicit denominator-identity criterion | L1 misread 'policy-excluded' as excluding the policy source file. Five are actually non-author-glob exclusions; exact policy file has4allowlisted hits. Retain original freeze and append denominator-correction.md plus corrected v2 fixtures/oracle at e2f549b before implementation. Gate compares exact path/line/class/digest multisets and derives non-author identities, never picks an exclusion to force90. Actual red/green controls are recorded after exercise. |
| M2 | dispatch instruction omissions | evidence/context-before.json CONTEXT_MISSING7clauses; evidence/context-after.json CONTEXT_OK12 at306e06e, under round22 waves | Q44 static pre-dispatch context gate | Retain red receipt and repair context before dispatch; red→green shown by same checker. Text conformance is not runtime prevention. |
| M3 | contradictory wrapper provenance | retained r21 retention-floor-entering.json: wrapper9fb1f911 versus argv/output e9f340ce; build/EnteringPartition.md | Q58/63 bound-revision requirement | Reconciler rejects disagreeing wrapper/command/inner revisions, instead of allowing identical hit counts to conceal the wrong measured tree. Original receipt is never edited; final consistent receipt is the positive real control. |

M1 is the L1's own mistake, not a correction to the operator's given totals. Corrected meaning: policy_excluded = non_author_paths_glob identities, not source-file exclusion. The policy and its nested copy are both scanned normally. Non-author and allowlisted sets can overlap, so the general invariant is set membership, not raw=allowlisted+unallowlisted+non-author arithmetic. Their observed disjointness in r21 is contingent.

## Gate

Reopened existing rows only, on2026-10-21:

| Row | URL | Access | Decision and located quote (≤25 words) |
|---|---|---|---|
| S064 | https://git-scm.com/docs/git-rev-parse | 2026-10-21 | Re-admit A only for resolving an existing commit. OPTIONS --verify: “git rev-parse \"$VAR^{commit}\" will make sure $VAR names an existing object that is a commit-ish”. It does not establish authorship, push status or privacy. |
| S065 | https://docs.python.org/3/library/hashlib.html | 2026-10-21 | Re-reject C as sole provenance/privacy authority. Hash algorithms, first paragraph: “At any point you can ask it for the digest of the concatenation of the data fed to it so far.” Bytes-in→digest-out does not identify the repository supplying bytes. |

S064 used-by old→new: `corpus/lessons/round-19.md` → `corpus/lessons/round-19.md, corpus/lessons/round-22.md`. Status/recheck unchanged. S065 status/recheck/used-by unchanged. No new rows or tier inflation. Immutable original version/anchor cells are not rewritten because a live page version changed.

Admit: bounded accounting reconciliation, strict committed-input provenance and retained-red reporting. Reject: successful accounting as privacy clearance; policy-source or policy-copy subtraction; a digest as secrecy/authentication; cleanup receipts as independent wave disposition; turning the old11/12control green by silently changing expectations. Author-dispatched seats are author-side evidence, not outside spot-checks. Outside admit/reject review remains pending unless a separately retained named non-author record is appended.

## Implementation and verification provenance

The three executor seats and both scribe seats died on provider capacity/rate limits and were not replaced. L1 authored the independent fixture builder/oracle, froze corrected v2 expectations before implementing the tool, and authored the shipping code and this lesson. This is a pre-implementation frozen oracle, not a non-author oracle. Original dead-seat records remain evidence. Additional implementation refinements and actual receipts are appended after exercise; no unrun check is represented as passing.

## Carried scope

Four unallowlisted retention hits remain open debt; this round performs no redaction, allowlist expansion or privacy/history clearance. R21 original permission control11/12 remains red; trust-refinement12/12 is a separate expectation mode, not authorization. Two historical loss dispositions stay unknown; no baseline or pin changes. Q64 discovery/time-binding, Q65 discriminator, Q66 marker variants and Q68 historical binding remain separate debt. No promotion, host remediation, dispatch-mechanism change or subsequent round.

## Co-evolved instrument refinements

Build-wave static attacks are author-side. CriticPopulation's path-blind and
partition-only mutants, CriticAdmission's path-binding concern, and
AttackR05/15/17/18/20/21's non-discriminating setup arms motivated18 explicit
supplementary controls without rewriting the frozen24 expectations.
AttackR05/08 prompted an actual exit1/finding selftest arm alongside0/2.
AttackR23 exposed the valid-arm-only leak test: the measurement driver now
checks every pristine fixture output against a bounded field whitelist and
synthetic payload markers, and includes a setup-only synthetic leak mutant
which the original24 oracle can miss. That fourth mutant must be killed by
the separate all-arm output check, not falsely credited to frozen24.
This finite check is not a proof against every transformation or privacy leak.

All additional expectations are co-evolved after the first implementation,
not pre-build-frozen or outside-adjudicated. The same committed counting
instrument runs before and after, and archived synthetic workspaces retain
the exact mutation/restore evidence. Actual outcomes are appended only
after exercise. The original failed executor identities are not replaced;
one connector attempted to notify an already-dead oracle seat, whose original
provider death remains a death even if a later peer-wake leaves a file.

## Outside source spot-check (supersedes "pending" in Gate)

Main (parent orchestrator, non-author) agreed with both decisions, reasons
retained in `.ufo/waves/round-22/evidence/source-spotcheck.json`: S064 re-admit
at existing-commit-resolution scope only; S065 re-reject as sole provenance/
privacy authority. Falsify seats SourceAdmit/SourceReject are author-side.
Erratum (SourceAdmit SA-2): S064's immutable `teaches` cell over-attributes the
blob-binding step; Git blob binding in the reconciler rests on lane code
(`ls-tree` mode + `cat-file` by object id), not S064. The live-version note
applies to S065 (3.15.0→3.15.1), not S064 (still 2.56.0).
S064 used-by old→new: `corpus/lessons/round-19.md, corpus/lessons/round-22.md`
→ same plus `corpus/knowledge/freeze-order-r18.md,
corpus/knowledge/retention-reconciliation-r22.md` (both cite it; SA-3).

## Wave2 falsification dispositions

The wave2 payload validated at 3985b3d was first issued after the L1's
provider death and resume (attempt1, 64 seats). Frozen24 still pass, but
FinalR02–R24/Fixture*/Code* showed most frozen arms check exit+finding only, and
mutants were credited for "any unmet requirement". Folded, without editing any
frozen v2 byte: distinct reason tokens (`measured_not_ancestor`,
`receipt_revision` for an unresolvable measured revision, `repo_not_absolute`,
`repo_not_toplevel`, strict UTF-8/BOM-free JSON, `-h`→usage exit2, regex
Overflow/Recursion→`policy_regex`, closed-stdout and MemoryError never exit1);
a truthful `raw_not_allowlisted` beside the frozen alias `raw_unallowlisted`;
52 co-evolved refinement controls; and 22 mutants each scored only when its
named target rows go red, with unmutated frozen+refinement controls green and
real identity digests plus a swapped-identity failing twin inside the gate.
Frozen R13–R21 remain exit-level evidence only; their reasons are proven by the
co-evolved controls. `expected-real.json` was committed with the implementation
(8cb4afb), not pre-build. Builder `expected_*` lists are trustworthy only for
the valid variant (shared-object aliasing, FixtureLine F2/FixtureInject).
Residual, not fixed: lone `\u` surrogate escapes, per-blob `cat-file` process
cost, non-UTF-8 tree paths fail closed where the gate tolerates them.
M4 (mistake): crediting mutants by any unmet row; captured-by Q63/Q70 spirit,
none explicit; fix = per-mutant target rows, shown able to fail by the 22
targeted kills with green unmutated controls (measure evidence).
