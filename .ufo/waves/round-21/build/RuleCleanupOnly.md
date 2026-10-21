# RuleCleanupOnly — bounded source-only review

## Scope and axes

Requirement: cleanup existence must not become independently evidenced accounting for frozen `loss-cleanup-only`. Axes: calibration correctness, blocked baseline acceptance, provenance independence, and minimal change scope. This is a detection/report recommendation, not an admission or lifecycle ruling. No candidate or production files were edited.

## Findings by severity

### P1 — historical cause-only permission admits the cleanup-only counterexample; current candidate addresses this slice

**Concrete evidence:** the retained r10 baseline names `aggregator-r10` and `aggregator-r10-resume` as required observations (`corpus/evidence/baseline-r10-20261015T2231Z.json:26-27`). The removal record identifies the cleanup actor and deletes their wave evidence (`.ufo/waves/round-21/evidence/removal-metadata.txt:1-17,19-36`). Eighteen `pushed` rows prove preservation receipts, not an independently authored per-wave disposition (`.ufo/waves/round-21/evidence/cleanup-receipts.tsv:1-18`). The provenance copy records the same actor for removal and cleanup, `independent_wave_disposition:null`, and settlement unknown (`.ufo/waves/round-21/evidence/historical-provenance.json:19-21,31-40`). The new accounting correctly retains both rows as `unresolved`, with cleanup references present and independent dispositions null (`corpus/evidence/loss-accounting-r21.json:5-23,26-44`).

**Counterexample:** required evidence is lost; cleanup receipts exist; no independent disposition exists. Thus the frozen input remains `required_evidence_lost=true, independent_disposition=false, ordinary_state_change=false`, not the positive `loss-independent-cleanup` case. Its required result is `census-regression,false` (`.ufo/waves/round-21/frozen/cases.json:12-26`; canonical contract `.ufo/waves/round-21/contract.md:14-15,20-23`).

Historical Q67 classes a disappearance caused by unchanged census code plus changed host/fleet state as live-state, with only a blind-spot route when needed (`corpus/QUALITY.md:245-250`). The explicit before-rule object models that permission with `evidence_loss_blocks:false` and does not claim historical executable code (`.ufo/waves/round-21/frozen/before-rule.json:2-5`). **[INFERENCE, not executed]** that rule produces `live-state,true` for the cleanup-only row, contradicting its frozen expectation. Equating `bool(cleanup)` with independent disposition would reproduce the same unsafe decision under the replacement rule.

This is the bounded historical/design counterexample, **not a newly observed defect in the current frozen case or candidate implementation**. The frozen cleanup-only case keeps independence false; appended Q69 explicitly distinguishes same-identity cleanup receipts from independent disposition (`corpus/QUALITY.md:263-271`).

## Smallest safe change

Keep the frozen expectations unchanged. For the replacement rule, evaluate `required_evidence_lost and not independent_disposition` before any cause/ordinary-state explanation; return `census-regression,false` when true. Never synthesize `independent_disposition` from cleanup presence, receipt count, `pushed` status, or the cleanup actor's own assertion. For real accounting, cleanup stays provenance; only a separate, validated per-wave disposition can support independent accounting under the canonical contract. Missing or invalid disposition remains blocked, not relabelled disposed.

The current isolated candidate already contains this narrow behavior, so **no additional candidate edit is recommended by this review**:

- `.scratch/round21/ImplLoss/tools/mori-evidence-loss.py:655-677` requires actual booleans for case inputs; `:681-692` loads the supplied rule and cases and checks the evidence-loss/independence predicate directly. It does not consult cleanup existence or let `ordinary_state_change` override that predicate.
- `.scratch/round21/ImplLoss/tools/mori-evidence-loss.py:537-545` validates cleanup separately and retains an unresolved row even when cleanup exists. `:546-579` rejects a missing disposition, a false/nonboolean independent flag, a same-string cleanup actor, or mismatched committed disposition content. The disposition record requires explicit identity, actor, wave, disposition, and independence fields (`:455-474`).
- `.scratch/round21/ImplLoss/tools/mori-evidence-loss.py:580-619` does not automatically clear acceptance even for a structurally valid declaration: it retains an external-review-required blocker, and pin permission requires no omitted, unresolved, or invalid rows. `:636` returns rc1 while blocked. This stronger behavior is an observed candidate detail, not a replacement instruction source for the frozen contract.
- The CLI reaches those functions through `.scratch/round21/ImplLoss/tools/mori-evidence-loss.py:977-984`; setup failures return rc2 with a false pin field (`:955-963`). **[INFERENCE, not executed]** both supplied unresolved historical rows therefore remain blocked rather than being cleared by their cleanup references.

## Residual risk and verification gaps

- Actor strings and `independent:true` are structural declarations, not authenticated independence. Distinct strings alone do not establish distinct real actors. The candidate's external-review blocker avoids treating that declaration as permission; independent disposition remains unknown for these historical rows.
- Frozen classifier booleans are policy inputs. Correct classification of those inputs does not establish the truth of an independence assertion or authorization to run a real pin.
- The LSP device is unavailable: `read xd://lsp` returned `No such tool: xd://lsp`. Status/references/definition/diagnostics could not be requested. Source and literal-search inspection are the fallback, not semantic caller proof.
- Read-only Git diff commands for the bounded target paths returned no diff text; the isolated candidate source was inspected directly (read snapshot `0E4A`). This report does not assert a committed implementation identity or completed integration.
- No tests, selftests, builds, lint, formatters, census, pin, or runtime were invoked. No resume-continuity, rerouting, saturation, independent lifecycle closure, or runtime-verification claim is made. Verification is static only; the integration owner must exercise the frozen cleanup-only decision and the real unresolved accounting if authorized.
- Tool installs/updates: none.
