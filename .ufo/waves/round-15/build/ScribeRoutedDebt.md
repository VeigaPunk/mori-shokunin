# ScribeRoutedDebt — round-15 mapping of the six round-14 routed items

Seat: `MoriR15.ScribeRoutedDebt` (scribe, leaf). Lane root: `/home/vgpnk/Projects/shokunin/mori-shokunin`.
Claim context: round-15 C1 coverage (positive validated OOM/signal evidence). Other debt is unclaimed conformance.

## Scope and method

- Source of the six items: `corpus/lessons/round-14-verifier-spotcheck.md` section "Routed defects and operator notes", items 1–6 (lines 136–141). Item 5 restates the six round-13 defects (`corpus/lessons/round-13-verifier-spotcheck.md:132–137`), tabled in `.ufo/waves/round-14/build/HistoricalCorrections.md` §0.
- Evidence: reads and greps of committed files only. Counts are file-grep counts taken in this pass.
- No census, harness, selftest, oracle, drift run, build, lint or test was executed. No git writes. No commits.
- Tooling: none installed, updated or removed. Host-safety notice acknowledged: no `pacman` action was needed or taken.

## Mapping table

| # | Round-14 routed item (spotcheck line) | Owner | Current state (file evidence) | Concrete closure requirement | Claimed in r15 C1? |
|---|---|---|---|---|---|
| 1 | Dirty-path scope when a gate records `dirty=true` (:136) | mori gate owner for `tools/mori-round14-regressions.py`; L1 for measurement | OPEN. `tools/mori-round14-regressions.py`: 0 matches for `dirty`/`porcelain`, so the r14 gate records no dirty flag at all. `tools/mori-round13-regressions.py` records a boolean only (`revision.dirty`, lines 1088–1094, 2521), with no path list. | Either the gate evidence records the dirty path list (from `git status --porcelain` on covered paths) when dirty is true, or the receipt is measured from an explicitly frozen clean input tree with output outside it. L1 confirms on a clean tree. | No |
| 2 | Qualify `journal-alarm-routing-r14.md:221` "fail-loud on positive validated records" as positive validated class counts, cross-linked to :386–390 (:137) | mori knowledge owner (`corpus/knowledge/journal-alarm-routing-r14.md`) | OPEN. Line 221 still reads "fail-loud on positive validated records" unqualified. The cross-link target exists: lines 386–391 disclose the mixed-stream limit (`R14_SEC_DUP_MSGID_MIXED`). | Reword :221 to "positive validated class counts" and cite :386–390. Wording only: do not state the inherited mixed-MESSAGE_ID suppression path is repaired. | Adjacent only. r15 adds positive_* tokens but does not claim mixed-stream completeness. This item must stay wording-only. |
| 3 | Interface clarity: legacy `KILL_SIGNAL_JOURNAL` `count`/`process_sigkill` may be `unavailable:<reason>` while the user-unit-signal arm warns; label SCORECARD nonzero vectors "fixture" (:138) | mori knowledge and SCORECARD owners | PARTIAL/OPEN. Knowledge :383–384 documents `count=0` on signal-only WARN but has 0 matches for `unavailable:`, so the unavailable state is undocumented. SCORECARD has 0 matches for a fixture/nonzero label. | (a) Add a sentence to `journal-alarm-routing-r14.md` near :383 stating legacy count/process_sigkill can be `unavailable:<reason>` and that this is not a fabricated zero. (b) Label each round-14 SCORECARD nonzero vector "fixture". | Adjacent. r15 requires raw counts to stay unavailable when invalid, which this item documents. |
| 4 | Old r10 drift pin still red at 5601d12; status-neutral conformance debt (:139) | mori drift-pin owner (SKILL "drift pin" row); L1 for any re-pin | OPEN, carried. Pin exists at `corpus/evidence/baseline-r10-20261015T2231Z.json`. Current red/green state was not observed in this pass. | A re-pin only after reasoned semantic review of each drift token, committed with per-token classification. Otherwise keep it routed as status-neutral debt. No silent re-pin. | No (unclaimed conformance) |
| 5 | The six round-13 defects "landed or qualified" (:140) | mori (round-13 routing); closure already accepted by the r14 spot-check | MOSTLY LANDED, with two partials (see detail §5). | Per item: keep the landed state; close the two partials named below. | Partly (item 1 is the C1 OOM path) |
| 6 | Operator: four SHONEN boxes (:141) | Operator only (promotion is operator-owned) | OPEN by design. `SHONEN.md:5–8` shows 4 of 4 boxes unchecked (`- [ ]`). | Operator ruling only. Mori does not edit SHONEN boxes. | No |

## Detail

### 1. Dirty-path scope
- Grep of `tools/mori-round14-regressions.py` for `dirty|porcelain`: 0 hits.
- Grep of `tools/mori-round13-regressions.py`: dirty recorded as a boolean (`self.dirty`, `record_revision`, `"dirty": self.dirty`), with `MORI_EVIDENCE_DIRTY` override. No path list is retained.
- Closure is in §Mapping. The round-14 spot-check itself says current verdict-driving hashes match the cited revision, so no behavioral mismatch is inferred. This is provenance debt only.

### 2. Wording at journal-alarm-routing-r14.md:221
- Line 221 unchanged: "The alarm is fail-loud on positive validated records, not a claim to be comprehensive or unspoofable."
- The limit is already disclosed at lines 386–391 (`R14_SEC_DUP_MSGID_MIXED`; a mixed stream with a malformed MESSAGE_ID can hide a valid OOM indication).
- Round-15 interaction: the r15 positive_* tokens are scoped to independently valid records. They do not change the r14 aggregate all-or-nothing class behavior. Item 2 must not be closed by claiming otherwise.

### 3. Interface clarity
- The census emits `KILL_SIGNAL_JOURNAL` once (`tools/mori-census.sh:1353`, one emit line). Its fields include `count=$ps process_sigkill=$ps user_unit_signal=$us`.
- The knowledge file documents `count=0` for signal-only WARN (:383–384). It does not document the `unavailable:<reason>` state.

### 4. Old r10 drift pin
- Baseline file present: `corpus/evidence/baseline-r10-20261015T2231Z.json`.
- Round-14 spot-check reports it red at measured 5601d12. No current measurement is available to this seat (none run, by lane rule).

### 5. Six round-13 defects (spotcheck :132–137), file-grounded status
1. OOM alarm: LANDED. `tools/mori-census.sh:1331` has one `emit_finding OOM_KILL_JOURNAL crit` line (count 1).
2. Fleet/non-fleet split and owner route: LANDED. `UNIT_FAILURE_OUT_OF_SCOPE` has 2 emit lines (`:1279` user, `:1281` system); `UNIT_FAILURE_JOURNAL` is fleet-only at `:1272`/`:1274`.
3. "no-anchored-structured-field" reason and retired GPF text: PARTIAL. The reason token has 0 matches in the census. The knowledge file annotates the GPF/text limit (`journal-alarm-routing-r14.md` §5 table). The census has 0 matches for `GPF|general protection`, so the census `unmeasured=` strings do not name it. Exact replacement wording in the census was not read in this pass [UNKNOWN].
4. Harness registration: LANDED for registration. `SKILL.md:74` (r13) and `:75` (r14) list the gates. The round-13 harness has 0 matches for `EVIDENCE HARNESS|NOT A GATE`; `not-registered` appears only in a docstring stating it is not a permanent identity (`:528`). PARTIAL for the delivered-revision selftest: SKILL cites 33 checks at 8d22d18 and the r14 gate 20 checks at 5601d12. Neither is the final delivered bytes.
5. F01/F02 qualifiers: LANDED. `corpus/knowledge/verdict-contract-r13.md:276–279` names the reconstructed prefix shim and function-locus sufficiency.
6. Correction sweep: LANDED. `corpus/README.md:32–33` now say "not MESSAGE-free kernel kills"; `corpus/QUALITY.md:33` carries the qualifier.

### Counts (file-grounded, this pass)
- `emit_finding OOM_KILL_JOURNAL`: 1 (census :1331).
- `emit_finding UNIT_FAILURE_OUT_OF_SCOPE` (+ `_SYSTEM`): 2 (:1279, :1281).
- `emit_finding KILL_SIGNAL_JOURNAL`: 1 (:1353).
- `no-anchored-structured-field` in census: 0.
- `dirty|porcelain` in r14 gate: 0.
- `unavailable:` in journal-alarm-routing-r14.md: 0.
- Unchecked SHONEN boxes: 4 of 4.
- Round-14 spot-check reported count `[6, 0]` (fail counts, red vs green). Reported from the spot-check text; not re-run here.

## Unresolved facts (named, not inferred)

- Current pass/fail state of the r10 drift pin (item 4).
- Whether the final delivered bytes have a selftest receipt for the r13 harness (item 5.4).
- The exact census `unmeasured=` wording for GPF/text classes (item 5.3).
- The exact row locations of round-14 SCORECARD nonzero vectors (item 3b); the grep found no fixture label, but the section was not read in full.
- Whether any live host record currently carries an invalid or ambiguous subject (round-14 `[UNKNOWN]`; not measured here).

## Out of scope for this seat

- No edits to production, tools, corpus, SHONEN, SCORECARD, fleet, sibling, MANIFEST or verifier files.
- No changes to the r15 claim. Items 2 and 3 are adjacent to C1 but are conformance debt, not C1 closures.
- No verification commands run (lane rule). L1 should run any gate measurement once, after integration.

## Checks for L1 (not run here)

1. Dirty-path: confirm the r14 gate receipt records dirty and paths on a dirty tree, or measure from a frozen clean tree.
2. Wording: `grep -n 'fail-loud on positive' corpus/knowledge/journal-alarm-routing-r14.md` should show "positive validated class counts" with a cross-link to :386–390.
3. Interface: `grep -n 'unavailable:' corpus/knowledge/journal-alarm-routing-r14.md` should be nonzero; SCORECARD nonzero rows should carry "fixture".
4. Drift pin: measure `tools/mori-census.sh --drift corpus/evidence/baseline-r10-20261015T2231Z.json` once and classify tokens; do not re-pin silently.
5. Item 5.3/5.4: census `unmeasured=` wording for GPF/text; selftest on the final bytes.
6. SHONEN: confirm the four boxes remain unchecked unless the operator rules otherwise.
