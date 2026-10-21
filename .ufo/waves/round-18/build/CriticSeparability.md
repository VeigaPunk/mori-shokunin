# Round 18 — causal separability and axis distinctness

## Verdict

The three measurements use different evidence (retention hits, freeze-order labels, and dispatch-payload bindings), but the contract's strict claim that they are each causally separable is not true at the final-gate level.

- **C1:** mechanically evaluable at any selected revision without C2/C3 tools. Its result is a whole-tree snapshot, however, so later C2/C3 commits can change the count; an intermediate pass is not a stable final pass.
- **C2:** **not independently passable as specified.** Its frozen register includes r18-C1 and r18-C3 as pre-build claims, and the C2 metric counts register overclaims. The frozen verdict rule makes an absent implementation path `no-implementation`, not `pre-build`; therefore the C2 zero-overclaim claim depends on both other axes' implementation commits existing.
- **C3:** mechanically evaluable from its own committed attempt ledgers and dispatch payloads without C1/C2 implementations. It has no direct dependency on their result artifacts.

Thus C2 is a cross-axis freeze-order gate, while C1 is a repository-wide snapshot gate and C3 is a ledger-local gate. The contract should not describe all three final results as independently certifiable.

## Strongest counterexample: C2 has r18-C1/C3 in its denominator

`frozen/c2-register.json` includes r18-C1 and r18-C3 with declared label `pre-build`, and names their implementation paths (`frozen/c2-register.json:30-41`). Its rules define `I` as the first commit touching an implementation path, with no such commit producing `no-implementation`; `overclaim` is true when the effective label is `pre-build` and the verdict is not (`frozen/c2-register.json:4-14`). The contract counts uncorrected overclaims and requires all three r18 claims to verify pre-build (`contract.md:31-37`).

Consequently, at a measured tip before C1 or C3 has an implementation commit, that row is an overclaim by the frozen rule. C2 can report that failure, but cannot meet its stated after-count of zero until both C1 and C3 implementation paths have landed. The historical r17 correction/oracle comparison can be checked separately; it does not remove this dependency from the all-claims result.

**Smallest safe correction:** for this already-frozen attempt, retain the aggregate across every register row but label it a cross-axis integration gate; do not claim it is independently passable or drop r18 rows. For a genuinely separable C2 axis, a future freeze can define a scored calibration subset independently and keep r18-C1..C3 chronology as a separate integration check.

## C1 repair overlap and C1/C3 independence

C1 is defined as unallowlisted retention hits at the measured revision, excluding non-author paths; the target includes zero hits in the three required-redaction reports (`frozen/c1-policy.json:17-29`; `contract.md:24-29`). The frozen population reports 119 total hits, 3 non-author hits, 40 must-redact hits, and a metric baseline of 116 (`frozen/c1-population.json:5-10`). Removing hits from the required-redaction files is therefore both the privacy repair and a direct improvement to C1. The repair-first work also requires a whole-round reading sweep and a lesson/quality criterion; those broader/manual findings are not all represented by C1's regex floor (`frozen/c1-policy.json:27-29`).

There is **real evidence overlap**, but the contract gives no scoring or credit-allocation rule, so it does not establish that anyone actually double-counted. [INFERENCE] If repair completion and C1 are later awarded as separate axis credit for the same redacted hits, that is duplicate credit, not two independent improvements. The spot-check itself is excluded from C1 as a non-author path; its frozen-population entries are 3 hits (R6: 2, R9: 1), so those are not eligible C1 reductions. No source text is reproduced here.

C1 can run without C2/C3, but it scans every tracked blob at the measured revision (`frozen/c1-policy.json:5,27-29`), so C2/C3 additions containing unallowlisted matches can change its result. C3's binding calculation is local to each ledger row's dispatch path and does not require C1/C2 outputs (`frozen/c3-ledger-format.json:4-20`).

**Smallest safe correction:** preserve C1's full metric, but state that the redaction work is a prerequisite/remediation obligation, not a second scored axis; award the shared hit reduction once through C1. Keep the whole-tree/manual sweep and its lesson criterion as repair acceptance, and do not imply C1's regex count is a complete privacy proof.

## Routed defects 1–6

Source classification: `corpus/lessons/round-17-verifier-spotcheck.md:388-417`, SHA-256 `98f8f1c631fcb565af69d884330177ebe01bfb31f21218028157d2acc40698dd`. Frozen-population entries for this non-author file are at `:312` (R9), `:315` (R6), and `:341` (R6): 3 hits total (R6: 2, R9: 1). No matched text is reproduced here.

1. **Privacy retention — addresses current-tree remediation; historical exposure is deferred.** The contract requires redaction of named reports plus repeated mentions found by the sweep, adds the lesson/quality requirement, and sets a C1 zero target. It expressly leaves already-pushed history/exposure assessment to the operator-owned route (`contract.md:9-13`; spot-check `:390-397`). C1 omits non-author paths and is only a regex recall floor, so it is not a complete privacy assurance (`frozen/c1-policy.json:23-29`).
2. **Freeze/calibration — addresses the new round; preserves historical limits.** Round-18 inputs are frozen before implementation; C2 retains historical comparisons and requires an appended correction rather than relabeling the r17 record (`contract.md:14-15,31-37`; spot-check `:398-402`). The cross-axis coupling described above remains.
3. **Scope enforcement — partially addresses by instruction; runtime prevention is not supplied.** The contract carries concrete pre-action boundaries in wave contexts and explicitly characterizes them as instruction text, not runtime prevention (`contract.md:16-17`; spot-check `:403-407`). Any claim of enforced prevention is therefore deferred/unsupported here.
4. **Evidence provenance — addresses per-attempt binding, with a stated limit.** C3 requires a digest/size/task-count binding on each attempt row and tests tampering/mismatch cases (`contract.md:39-43`; `frozen/c3-ledger-format.json:4-20`). The frozen format explicitly cannot prove the task tool received those exact bytes absent L1 copying them unchanged and returned IDs matching the registry (`frozen/c3-ledger-format.json:21`; spot-check `:408-411`).
5. **Inherited gate debt — explicitly deferred and kept open.** The contract says the old qualifications stay named/open and forbids repinning; it does not resolve or rerun them (`contract.md:19`; spot-check `:412-414`).
6. **Package/boot-chain events — explicitly deferred to the owning operator domain.** The contract specifies detection-only handoff, not remediation or an ownership inference by Mori (`contract.md:20`; spot-check `:415-417`).

## Read-only evidence and scope

Read the contract, the C1 policy and population plus C2 register and C3 ledger-format frozen inputs, and the requested spot-check range. Ran only `sha256sum /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/lessons/round-17-verifier-spotcheck.md` (exit 0; digest above). No validators, self-tests, builds, or mutating VCS commands were run.