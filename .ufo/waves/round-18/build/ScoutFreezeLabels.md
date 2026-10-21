# Round-17 freeze-label inventory

Reviewed 2026-10-21. Scope: round-17 claim-related freeze, precommit, preregistration, fixed-universe and before/after language at lane tree `29b0dc7`, plus the filed fleet report `/home/vgpnk/Projects/shokunin/.ufo/reports/round-17/mori.md`; compared against `.ufo/waves/round-18/frozen/c2-register.json`.

## Axes and method

- **Coverage:** identify all relevant round-17 claim sites, not every incidental use of “frozen” in code or retained data.
- **Classification:** separate a claim that inputs existed before initial implementation from a later pre-measurement pin or a before/after invariant.
- **Register fidelity:** check `declared` and `declared_at` against the cited source and identify omitted evidence or misleading wording.
- **Provenance:** distinguish lane-authored assertions from the non-author spot-check and evidence-receipt fields.

Used the assigned read-only command `git -C /home/vgpnk/Projects/shokunin/mori-shokunin grep -niE 'precommit|pre-?regist|frozen before|fixed before|constant .* universe|pre-build' 29b0dc7` (exit 0), then scoped expanded literal `git grep` searches for `frozen`, `fixed`, `constant`, `predeclared`, `committed before`, and related terms (each returned exit 0). Searched `inputs_match_precommitted` under `tools/` (exit 1: no matching tracked tool source) and counted **32** round-17 JSON receipt files carrying that field. Read the relevant contract, scorecard, log, lesson, falsification and report contexts plus the frozen C1 policy/population, C2 register and C3 ledger format. The mounted tool set has no LSP device; literal grep was therefore the semantic-search fallback, with targeted source reads for context.

The lane’s observed `HEAD` is `11db4df` (round-18 wave-1 landing); the history shows `29b0dc7` immediately before it and `d005cdd` before that. All lane searches above explicitly target `29b0dc7`. The lane tree has no `.ufo/reports/round-17/` at `29b0dc7` or `11db4df`; it has report directories for rounds 2–11. The required round-17 report is the fleet-root file and was searched separately. The reported fleet commit `0e52bc4d019fb0f41676da86dde157e252fbc28e` is not an object in the mori lane repository (`git cat-file -t` exit 1), consistent with the fleet/lane distinction. No files other than this report were written; no tools were installed.

**Classification key:** `candidate` = register treats “precommitted” as a pre-build declaration, hence an overclaim candidate; the cited wording itself usually establishes only commitment before a later run. `constancy` = same inputs, case inventory, or hashes across a measured before/after comparison, without asserting they were fixed before initial implementation. `counterevidence` = explicitly says the item postdated build dispatch or denies initial preregistration.

## Register-cited round-17 declarations

The C2 register has three round-17 rows:

| Claim | Register fields | Cited location and observed statement | Assessment |
|---|---|---|---|
| r17-C1 (coverage) | `declared: unlabeled`; `declared_at: []` | No lane-authored prose pre-build-freeze declaration located. | Accurate as to absence of an explicit pre-build label. Receipt hash matching (below) is not a declaration that C1 expectations preceded implementation. |
| r17-C2 (operability) | `declared: unlabeled`; `declared_at: [LOG.md:1197]` | `LOG.md:1197` separates “constant C2 assertion universe” from C3’s precommitted pins. | Correctly classifies C2 as a constancy statement, not a pre-build label. Related omitted C2 constancy references are listed below. |
| r17-C3 (calibration) | `declared: pre-build`; `declared_at` has five locations | `.ufo/reports/round-17/mori.md:25,94`; `SCORECARD.md:1114`; `LOG.md:1197`; `corpus/lessons/round-17.md:245`. Each uses “precommitted” for C3 witness/control/expectation/recipe pins. | All five paths and line numbers exist and support the register’s **candidate-label** mapping. None, read in context, demonstrates the expectation/control universe existed before initial implementation; they establish precommit or hash binding for later measurements. Under the C2 register’s verdict rule, the pre-build label versus co-evolved verdict is the single overclaim candidate. |

The one `LOG.md:1197` line has two distinct clauses: C2 universe constancy and C3 precommitted pins. The register’s split use of that line is appropriate. The cited C3 phrase “precommitted” is temporally underspecified; the later, explicit timing records below resolve it as pre-run rather than pre-build. The register’s `declared: pre-build` should therefore be read as the historical label under test, not evidence that a pre-build freeze actually occurred.

## Additional round-17 claim-related sites omitted from `declared_at`

### C3: pre-run commitment, hash binding, and one misleading “frozen” label

| Path:line | Claim | Observed assertion | Classification / register comparison |
|---|---|---|---|
| Fleet `.ufo/reports/round-17/mori.md:139,142` | C3 | “pinned exact witness/probe”; recipe “already committed before the run”; digests bound before/after. | **Constancy / pre-run only**, not pre-build. `:142` is an important qualifier omitted from the register’s citations. |
| `.ufo/waves/round-17/contract.md:150` | C3 | Expectations and replay recipe committed before the final measurement. | **Pre-run only**; no initial-build timing asserted. Omitted from `declared_at`. |
| `LOG.md:1164,1204,1212` | Cross-claim, then C1/C2/C3 inputs, then C3 | The input ledger binds a revision to counting receipts (`:1164`); the final declared-input ledger pins inputs before runs (`:1204`); corrected source and predeclared controls land at the later correction commit (`:1212`). | **Receipt/run binding or post-build predeclaration**, not a pre-build freeze. Omitted from `declared_at`. |
| `corpus/lessons/round-17.md:105,171,310-311` | Cross-claim / C3 | Input digests and receipt metadata (`:105`); C3 committed before L1 measurements (`:171`); final input ledgers index measurements (`:310-311`). | **Pre-measurement/binding** only. Omitted from `declared_at`. |
| `corpus/lessons/round-17.md:138` | C3 | The initial measurement narrative calls `c3-expected.json` “Frozen” and says it pins the witness hash. | **Misleading freeze wording for the initial run.** `falsify/ReceiptInputs.md:123` identifies that expectation as post-hoc, and `falsify/ReceiptPins.md:115` says it was not a preregistered frozen instrument. The later correction at `corpus/lessons/round-17.md:245` says the initial expectation/recipe postdated that run. The C2 register omits this early wording and its correction context. |
| `SKILL.md:176` | C3 | Registry describes the in-script exact r16 artifact and expected outcomes, with the retained round-17 witness. | **Control identity/pinning**, not a claim that the final expectation set preceded initial implementation. Omitted from `declared_at`. |
| `SCORECARD.md:1095,1013` | C3 | Strict pinned controls match; same retained witness is used across the two sweep modes. | **Control/before-after constancy**, not pre-build. Omitted from `declared_at`. |
| Fleet `.ufo/reports/round-17/mori.md:224` | C3 / executable instructions | SHONEN text points to pinned fixture tables and the capture recipe. | **Artifact pointer**, not evidence of pre-build freezing. Omitted from `declared_at`. |
| `.ufo/waves/round-17/evidence/final/c3-before-pinned.json:73`; `c3-after-pinned.json:69` | C3 | Both carry `inputs_match_precommitted: true`; the pinned C3 receipt also records matching before/after bound-input digests. | **Measurement-time input binding**, not pre-build freezing. Omitted from `declared_at`. No tracked tool emits this field; the receipt wrapper is not present under `tools/`. |

The fleet report itself supplies counterevidence at `.ufo/reports/round-17/mori.md:8-9`: C3 was added after build reconnaissance and before L1 measurement. Its `:25` witness phrase must also be distinguished from the oracle/recipe: the non-author spot-check records that the witness was committed with the initial build, while expanded expected/control pins co-evolved later (`corpus/lessons/round-17-verifier-spotcheck.md:207-213`). Thus, a pre-existing witness does not establish a pre-build freeze of the complete C3 expectations and controls.

### C2: same-universe / before-after constancy sites omitted from `declared_at`

| Path:line | Assertion | Classification |
|---|---|---|
| `.ufo/waves/round-17/contract.md:145` | C2 retains the same scenario universe while adding expected-diagnostic checks. | **Before/after universe constancy**, not a pre-build declaration. |
| `.ufo/waves/round-17/build/ReviewC2Metric.md:9` | Predeclared C2 assertions should fail on the entering census and pass on delivered census; both sides use the same sandbox/input/assertion inventory. | **Comparison criterion and measured invariance**, not proof that the inventory predated implementation. |
| `.ufo/waves/round-17/build/JjGate.md:123-124,197,203,207` | Fixed-universe arm/totals and the 12-case/204-assertion before/after comparison. | **Measurement-universe constancy**. The outside ruling says the universe was not proven frozen before initial implementation. |
| `SKILL.md:175` | The r17 jj gate has an in-script fixed case/assertion universe and frozen entering census. | **Implementation/input pin**, with no assertion of pre-build timing. |
| `LOG.md:1229,1251`; `SCORECARD.md:1012,1094,1107`; `corpus/lessons/round-17.md:287,316-317` | C2’s final 204 assertions are described as the same/constant universe on both sides. | **Before/after constancy**, not pre-build. These are omitted from the C2 `declared_at` list. |

The non-author ruling independently resolves this distinction: `corpus/lessons/round-17-verifier-spotcheck.md:169-172` says the C2 tool/harness were co-developed and both changed in `2be8294`; the final harness then stayed fixed before a later census correction. The 204-assertion universe was not proven frozen before initial implementation.

### C1/C2 process-control snapshot (not the claim requirement universe)

`.ufo/waves/round-17/build/ContextCheck17.md:182-192` calls the wave-2 context a committed regression arm, exact bytes frozen at the wave-2 revision, and guards a sentence’s count before selftest arms run. This is a **later process-control snapshot**, not a pre-build C1/C2 requirement freeze. `corpus/lessons/round-17.md:218` explicitly says Amendment A1 was developed after initial build dispatch but committed before the first measurements (**counterevidence** to pre-build timing). The C1 outside ruling also says the original expected table and implementation were co-committed and then changed together (`corpus/lessons/round-17-verifier-spotcheck.md:120-130`).

## Machine receipt field: all 32 locations

Every path below has `inputs_match_precommitted: true` at the stated line. These are **receipt assertions that inputs matched the wrapper’s committed pins at measurement**, not assertions that the pins preceded initial implementation. They are not textual preregistration claims; the field’s wording nevertheless makes them relevant omissions from a literal inventory. Claim mapping is by receipt name; context, preservation, and census receipts are cross-cutting rather than declarations for one C-claim.

- C1 seat/capability receipts: `evidence/final/c1-after-fixed.json:69`, `c1-after.json:69`, `c1-before.json:69`, `c1-initial-red.json:69`, `capability-absent-proof.json:70`, `seat-gate-selftest.json:64`, `seat-live-final.json:73`, `seat-selftest-fixed.json:64`, `seat-selftest.json:64`, `count-c1.json:66`.
- C2 census receipts: `c2-after.json:69`, `c2-before.json:69`, `census-selftest-fixed.json:64`, `census-selftest.json:64`, `jj-gate-selftest.json:66`, `count-c2.json:66`.
- C3 probe receipts: `c3-after-pinned.json:69`, `c3-before-pinned.json:73`, `misroot-selftest.json:64`, `count-c3.json:65`.
- Cross-cutting/context/preservation receipts: `context-liveban-after.json:65`, `context-positive-after.json:65`, `context-selftest.json:64`, `context-survivor-after.json:65`, `context-survivor-before.json:65`, `fleet-misroot-final.json:69`, `fleet-status-full.json:69`, `r13-preserved.json:67`, `r14-preserved.json:67`, `r15-preserved.json:67`, `silence-oracle.json:63`, `sources-census-final.json:66`.

The preserved r13–r15 and silence-oracle rows are historical no-regression inputs, not round-17 claim requirements. Their receipt field is not a freeze-order claim.

## Other explicit timing and oracle evidence

- Fleet `.ufo/reports/round-17/mori.md:8-9` says C3 was added after build reconnaissance but before measurement; `:142` says the recipe was committed before the run. Both are **counterevidence to pre-build**, not overclaims.
- `corpus/lessons/round-17.md:171` says C3 was committed before L1 measurements (**pre-run only**); `:218` says A1 came after initial build dispatch and before first measurements (**post-build**).
- The non-author spot-check is not a lane-authored freeze assertion. Its cited rulings agree with register `outside_ruling`/`ruling_at`: C1 at `:120-130`, C2 at `:169-172`, C3 at `:207-213` and `:398-402`. In particular, C3’s final exact pins preceded the measured run but do not establish blanket pre-build preregistration (`:213`). Its `:73` also says the later C3 addition is not evidence of an initially preregistered third claim.
- `falsify/ReceiptInputs.md:123` and `ReceiptPins.md:115` are reviewer findings rejecting initial C3 preregistration; they are **counterevidence**, not lane claims of a freeze.

## Register disposition

1. **No missing C3 “precommitted” prose occurrence among the five register-cited declarations.** The five citations exist and are the five principal prose uses that support the register’s overclaim-candidate label. However, `declared_at` is not exhaustive of related pin/pre-run language: the C3 entries above, especially contract `:150`, lesson `:138/:171`, LOG `:1204/:1212`, fleet report `:139/:142`, and the two pinned C3 receipts are omitted.
2. **C2 declared_at is underinclusive for constancy references**, not for a pre-build label: it cites only `LOG.md:1197`; it omits the same-universe/fixed-204 references listed above. The existing annotation (“before/after constancy, not a pre-build label”) is correct.
3. **C1 declared_at empty is not contradicted by an explicit lane pre-build-freeze declaration found here.** C1 receipts show input binding; the oracle records co-evolution, and the lesson records post-dispatch A1.
4. **Potential wording mislabel:** `corpus/lessons/round-17.md:138` calls the initial C3 expected file “Frozen” even though the retained falsification findings establish it postdated the first run. The later M18 correction at `:245` acknowledges that timing. This initial “frozen” wording should not be treated as evidence of preregistration.
5. **C3 `declared: pre-build` is the operative label being tested, but stronger than the literal time claim at its five cited sites.** Those sites say “precommitted”; other lane prose dates commitment before measurements/runs, and the non-author ruling classifies the final pins as post-build/co-evolved. The C2 register’s result of one C3 overclaim candidate is therefore consistent with the record; do not reinterpret “precommitted” as proof of a pre-build freeze.

## Scope exclusions

Round-2/4/13/14/15 scorecard, lesson, and gate hits concern other rounds’ claims/instruments and are not r17-C1/C2/C3. Generic code constants, data-shape “constant” observations, historical frozen-red controls, and fixed scan times in C1 falsification cases do not assert a pre-build freeze of the round-17 requirement universe. The round-18 contract/register’s own “frozen before implementation” labels concern r18-C1..C3 and are outside this question.
