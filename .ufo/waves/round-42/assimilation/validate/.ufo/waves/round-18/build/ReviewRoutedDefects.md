# Round 18 routed-defect disposition review

## Scope and source identity

This is a disposition/evidence map, not a claim that round-18 remediation has already passed. Sources reviewed:

- `corpus/lessons/round-17-verifier-spotcheck.md:303-320` (15 V-rows and L1) and `:388-417` (six routed recommendations); 16 classified rows, SHA-256 `98f8f1c631fcb565af69d884330177ebe01bfb31f21218028157d2acc40698dd`.
- `corpus/lessons/round-16-verifier-spotcheck.md:190-226` (five open-queue items); SHA-256 `6a8e706e992e86d857df1f4726c6aaa6e57e8595b0ee4fb4dd80d164ed3305be`.
- `.ufo/waves/round-18/contract.md` (contract categories and tool interfaces); SHA-256 `6986c9338b4c38f8b66831526d4427c04c589226adc43e0240ff34ce08fcf11b`.

No code, build, tests, or runtime behavior were checked. Evidence below is what L1 must provide for a round-18 claim; it is not an assertion that such evidence exists.

## Round-17 routed recommendation dispositions

| Routed item | Owner | Round-18 disposition in contract | Evidence L1 must produce |
|---|---|---|---|
| 1. Privacy retention / committed handoff material | Mori/L1 for redaction and criterion; Operator/Kagi for exposure assessment | **C1 + criterion**, contract `:11-13, :24-29`. History is not rewritten; exposure assessment is expressly external. | Hash-only C1 evidence at the measured commit: reproduce the frozen base population, show zero hits in all three must-redact reports and no allowlist rows for them; retain the whole-tree repeated-mention sweep result; include the lesson and QUALITY criterion. Do not present the regex count as a privacy proof (frozen policy `:27-29`). |
| 2. Freeze/calibration | Mori/L1 | **C2**, contract `:14-15, :31-37`. The frozen register also requires the round-18 C1-C3 labels to be checked as pre-build. | Append the correction row for the prior overclaim; retain the C2 output showing zero overclaims and 3/3 oracle agreement, plus the measured C1-C3 pre-build determinations. Preserve historical expectations rather than rewriting them. |
| 3. Scope enforcement | Mori/L1 | **Criterion**, contract `:16-17`: concrete pre-action VCS, scratch, and field-projection bounds in every wave context; it explicitly says this is instruction text, not runtime prevention. | Retain each dispatched wave context and show the required boundaries are present. Do not claim that context text or a clean final state proves historical/runtime compliance. The contract does not require an execution-enforcement receipt. |
| 4. Evidence provenance | Mori/L1 | **C3**, contract `:18, :39-43`; row semantics in frozen `c3-ledger-format.json:4-21`. | For every attempt, retain the dispatch payload and ledger whose digest, byte count, and task count recompute consistently; show contiguous attempts, nondecreasing timestamps, exactly one final started/partial row, and matching started IDs. Preserve failure-capable evidence for tampered payload, digest mismatch, non-final start, and duplicate start cases. State the frozen known limit: binding is to the committed payload, not independent proof of bytes received by the task tool. |
| 5. Inherited gate debt | Mori/L1 | **Carried open with reason**, contract `:19`: r10 red and r13-r16 qualifications remain named; no repin. | Preserve the named open qualifications and the existing red receipt; identify them as open and do not repin or convert HEAD metadata into landed-branch proof. The contract does not call for a new pass or erase the historical result. |
| 6. Package/boot-chain events | Operator/Tsukuroi; Mori/L1 only hands off | **Detection-only handoff**, contract `:20`. | Retain a detection-only handoff pointer/receipt to Operator/Tsukuroi. Do not infer actor/authorization or perform remediation in Mori. |

## V1-V15 and L1 mapping

The V-row adjudications are at `corpus/lessons/round-17-verifier-spotcheck.md:305-319`; L1 is at `:320`. The contract's scope category explicitly names V1-V3, V5-V14, and L1 (`contract.md:16-17`).

| Item | Owner | Round-18 disposition | Evidence L1 must produce / limitation |
|---|---|---|---|
| V1 | Mori/L1 | Scope criterion (routed recommendation 3). | Every wave context carries the pre-action VCS boundary. Preserve actual action evidence if making a conformance claim; the contract only specifies instruction text, and final branch state does not cure the earlier event. |
| V2 | Mori/L1 | Scope criterion (routed recommendation 3). | Every wave context states VCS and sandbox boundaries; executor evidence is limited to its assigned tool/fixtures and authorized clone. No inference from retained runs alone. |
| V3 | Mori/L1 | Scope criterion plus C1 where content is committed. | Retain field-projection instructions and hash-only C1/sweep evidence for committed material. C1 scans tracked blobs; it cannot by itself prove that disallowed input was never read or displayed. |
| V4 | Operator/Tsukuroi; Mori/L1 hands off | Operator/Tsukuroi detection-only handoff (routed recommendation 6). | Handoff receipt only; keep ownership/authorization unresolved unless established by the receiving owner. No Mori remediation. |
| V5 | Mori/L1 | Scope criterion (routed recommendation 3). | Contexts specify clone-local scratch and prohibited outside-lane writes. Any current-state cleanup observation is not proof that the historical write did not occur. |
| V6 | L1 authorizes; assigned executor runs its own test | Scope criterion plus the executor interface (`contract.md:47-52`): caller sets `TMPDIR` to its own clone's `.scratch`. | Retain the authorized invocation and test receipt showing clone-local `TMPDIR` and fixture placement. Do not claim this retrospectively validates the earlier baseline run. |
| V7 | L1 authorizes; assigned executor runs its own test | Scope criterion plus one-tool/fixture ownership and clone-local selftest boundary (`contract.md:45-52`). | Retain the per-executor authorization and receipt showing only its assigned tool/fixtures and isolated sandbox were used. No extra mutations are licensed by a sandbox. |
| V8 | Mori/L1 | Scope criterion plus C1 (including frozen R9; policy `:15, :27-29`). | Retain class/hash-only C1 output and the whole-tree reading-sweep result; do not retain the disallowed field values. C1's recall-floor limitation means a clean metric alone is insufficient. |
| V9 | Mori/L1; Operator/Kagi owns exposure assessment | C1 plus privacy criterion (routed recommendation 1). | Same C1 evidence as route 1, including zero hits in the named reports, no allowlisting there, and the sweep of repeated mentions. Keep exposure assessment with Operator/Kagi. |
| V10 | Mori/L1 | Field-projection scope criterion; privacy criterion is relevant to retained material. | Contexts must state the allowed projection, not merely promise suppressed output. The contract specifies instruction text rather than a runtime read-prevention mechanism; L1 must not claim that parsing and discarding was prevented without separate behavioral evidence. |
| V11 | Mori/L1; Operator/Kagi owns exposure assessment | C1/whole-tree privacy criterion where committed; historical exposure assessment remains external. | Retain hash-only C1 output and the non-metric reading-sweep result, plus the criterion. Do not include other-session output or private-source text in the handoff. |
| V12 | Mori/L1 | Scope criterion (routed recommendation 3), but the contract does not spell out this row's exact read restrictions or an execution receipt. | Retain the concrete per-wave VCS boundary and, if claiming compliance, an action receipt sufficient to establish use of the authorized read path and absence of the disallowed configuration read. The contract currently mandates context text only; metadata/final-state observations do not prove this. |
| V13 | Mori/L1 | Scope criterion plus C1/whole-tree privacy criterion. | Retain C1 class/hash-only output and a reading sweep for retained numeric/range material, with no values in the report. The frozen regex is a recall floor, so absence of a key-shape hit does not close this item. |
| V14 | Mori/L1 | Scope criterion (routed recommendation 3). | Retain the per-wave pre-action VCS boundary and action evidence for any conformance claim. The row was adjudicated as low/inferred risk, not as proof of a substantive mutation; a clean final count does not show whether an operation could refresh metadata. |
| V15 | No violation owner assigned by the adjudication; Mori/L1 only if it chooses to carry the residual provenance limit | **Not a routed violation** in the source adjudication. The separate source-fetch storage-location provenance limitation has no explicit disposition in the contract; C3 binds dispatch payload attempts, not source-fetch location. | If retained as an open limitation, L1 should identify the source provenance evidence and disposition, without treating C3 as covering it. This is a residual contract gap, not a V-row remediation requirement. |
| L1 | Mori/L1 | Scope criterion explicitly includes L1 authorization (`contract.md:16-17`); executor interfaces delimit tool ownership and selftests (`:45-52`). | Retain authorization boundaries for each executor/selftest against its assigned clone and tool/fixtures. Do not imply that later clone-local runs erase earlier broad authorization or late-guard defects. |

## Earlier round-16 open routed queue

The five rows below are the open queue in `corpus/lessons/round-16-verifier-spotcheck.md:199-226`. Items 1-4 have no complete disposition in the round-18 contract; item 3 is only partially covered by the generic context-text criterion.

| Round-16 item | Owner | Round-18 disposition in contract | Evidence L1 must produce / gap |
|---|---|---|---|
| 1. Undisclosed outside-lane write omitted from the lesson/sweep | Mori/L1 | **No explicit disposition.** The VCS criterion is generic, and C1 enumerates tracked blobs only (`contract.md:24-29`); neither commits to the append-only lesson correction nor a full workspace sweep that includes untracked material. | To close: append the correction without rewriting history and retain a whole-worktree sweep receipt that covers tracked and untracked paths. Current C1 evidence cannot establish this. |
| 2. Earlier open probe-method correction | Mori/L1 | **No explicit disposition.** The contract's VCS/scratch/field-projection context clause does not name this open issue or require the lesson correction. | To close: append the precision correction and include the relevant explicit pre-action prohibition and bounded evidence in every wave context. The contract currently does not ask for either artifact. |
| 3. Pre-dispatch context gate | Mori/L1 | **Partial only.** Contract `:16-17` requires context text but does not require running a checker/successor before dispatch or retaining its receipt. | To close: retain a pre-dispatch check result for every wave spec, tied to the exact dispatched context. A green check remains evidence of the check, not runtime prevention. |
| 4. Stale closure wording | Mori/L1 | **No explicit disposition.** No round-18 contract clause calls for correcting the stale status wording or adding the closure note. | To close: append a dated/sourced clarification to the affected documentation without rewriting history; retain the resulting citation/receipt. |
| 5. Carry-forward gate qualifications | Mori/L1 | **Carried open with reason**, contract `:19`; no repin. | Retain the named open state and prior red/qualification evidence, including the unresolved alias, vacuum/cross-boot, and fixture/live or anchor-only qualifications. Do not promote them to closed or substitute a repin. |

## Missing or incomplete contract dispositions

1. **Round-16 item 1:** no explicit append-only lesson correction or all-path worktree sweep covering untracked files; C1's tracked-blob scope is insufficient for that obligation.
2. **Round-16 item 2:** no explicit disposition of the open probe-method correction or required context prohibition/evidence.
3. **Round-16 item 3:** context content is required, but the pre-dispatch checker/successor and per-wave receipt are not.
4. **Round-16 item 4:** no stale-wording/closure-note correction is required.
5. **V15 residual provenance limit:** not an adjudicated violation, but its separate source-fetch storage-location limitation is not explicitly closed or carried by the contract; do not treat C3 as evidence for it.

The V1-V3/V5-V14/L1 category has a contract disposition, but it is instruction-only. The contract expressly disclaims runtime prevention; evidence of context text must not be reported as proof of actual command, scratch, or field-projection compliance.
