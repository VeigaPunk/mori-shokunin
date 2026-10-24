# RuleNoModePreset — round21 pre-implementation review

Seat: MoriR21.RuleNoModePreset-4 (leaf, detection/report only). Bounded item: **before/after counting must derive decisions from loaded booleans, not phase labels.**
Scope read: contract.md, frozen/{before-rule,after-rule,cases,required,before-accounting}.json, oracle-loss.py, candidate `.scratch/round21/ImplLoss/tools/mori-evidence-loss.py`. No tools installed. No production or candidate edits. Scratch fixtures under `.scratch/round21/RuleNoModePreset/` only.

## Verified clean (no preset in the decision or counting path)

- `classify()` (impl :681-716): observed decisions derive solely from `rule["evidence_loss_blocks"] and case["required_evidence_lost"] and not case["independent_disposition"]`; `mismatched` counts observed-vs-expected per case. No phase parameter exists anywhere in the tool (`phase` grep matches only `os.stat` locals at :123/:197).
- `--selftest` before/after blocks (impl :1086-1105): `before_rule` asserts rc1 mismatched=2 with loss-unknown/loss-cleanup-only `matched:false`, others matched; `after_rule` asserts rc0 mismatched=0. Phase names are labels; values are boolean-derived and asserted against real output.
- oracle-loss.py :59-90: loops phases passing each phase's own rule/accounting file to the same tool; independently recomputes `expected_omitted` (required minus accounting ids) and per-case mismatches from the frozen table, and flags any counter disagreement. It never presumes a verdict from the word before/after.
- C1 counting: audit omitted/retained/unresolved derive from loaded rows (impl :511-626); frozen `before-accounting.json` is `{"observations":[]}` → omitted=2, pin_blocked, rc1 — counted from the snapshot, not the phase label.

## Finding F1 (medium): rule admissibility keyed on presumed phase, not the loaded boolean

`.scratch/round21/ImplLoss/tools/mori-evidence-loss.py:648-651` (`_load_rule`):

```python
if not rule["evidence_loss_blocks"]:
    text = " ".join(str(rule.get(key, "")) for key in ("source", "interpretation"))
    if re.search(r"(?i)(?:QUALITY\s*67|Q67)", text) is None:
        raise SetupError("before_rule_must_cite_q67")
```

Any schema-valid rule with `evidence_loss_blocks:false` is rejected rc2 "setup/input failure" unless optional free-text fields self-cite Q67; a `true` rule needs no citation. This makes evaluator *acceptance* derive from what the boolean value is presumed to mean ("false ⇒ this is the before rule") instead of the decision semantics the boolean carries. The contract's citation requirement ("Historical Q67 is interpreted narrowly via explicit before-rule object citing Q67") attaches to the shipped before-rule artifact — `frozen/before-rule.json` already satisfies it in both `source` and `interpretation` — not to every false rule handed to classify. Contract for rule false: "reproduces Q67 cause-only permission, always live-state,true", rc2 = "setup/input failure" only.

### Concrete counterexample (measured, candidate tool, frozen cases.json)

`classify --rule minimal-false-rule.json --cases frozen/cases.json`, rule = `{"schema":"mori-evidence-loss-rule-v1","evidence_loss_blocks":false}` (schema-valid per `_load_rule`'s own `_require_keys`, :642-647, which allows absent source/interpretation):

- Observed: rc2 `{"error":"before_rule_must_cite_q67","finding_id":"mori-evidence-loss:setup:before_rule_must_cite_q67",...}`.
- Contract-expected: all six cases observed `live-state,true`; mismatched=2 (loss-unknown, loss-cleanup-only expect census-regression,false); rc1 expected red.

Asymmetry receipt: same object with `evidence_loss_blocks:true`, still no citation → rc0. Identical metadata content is admissible or not purely by boolean value — the mode is inferred from the value. Downstream effect in the C2 chain: oracle-loss.py would flag `<phase>:classify-...` instrument issues (exit 2 ≠ expected rc, per-case rows absent → 6 independent mismatches, counter absent), so a legitimate false-rule evaluation (e.g. an errata-era re-evaluation citing only the supersession errata, which correctly need not name Q67 as current authority) becomes unmeasurable. The gate is also no real assurance: appending "Q67" anywhere in optional free text satisfies it, so it only rejects honest minimal objects.

## Smallest safe change (candidate file only; for ImplLoss/L1)

1. Delete impl :648-651 (the four-line Q67 gate in `_load_rule`). `_load_rule` then admits any schema-valid rule; decisions continue to derive solely from the loaded booleans. Frozen outputs are unchanged: `frozen/before-rule.json` keeps its citation as descriptive metadata, and its measured result (rc1, mismatched=2) is byte-identical.
2. Keep the narrow-Q67-interpretation guarantee where it contractually lives: it is already carried by the frozen artifact `frozen/before-rule.json` (citable, content-frozen). Optionally add one `--selftest` check that the shipped before-rule fixture object cites Q67 — a fixture-level assertion, not a classify-input gate.
3. Add one `--selftest` case: minimal false rule without source/interpretation → rc1, mismatched=2, all six observed `live-state,true`. This turns the no-preset property into an asserted invariant (same pattern as existing `boolean_not_integer` checks at :1101-1104).

Harm check: no schema, output schema, rc contract, finding_id, or frozen fixture changes; one hunk removed plus one selftest block. The selftest needs no edit for the removal (no existing check asserts the gate — grep `must_cite` matches only the raising line :651).

## Residual risk and verification gaps

- If L1 intends the rc2 gate as a deliberate narrow-interpretation tripwire, the objection stands anyway: rc2 is contractually "setup/input failure" for a schema-valid input, and the error name `before_rule_must_cite_q67` hardcodes the phase inference. That alternative would need its own rc/wording change; removal is smaller and safer.
- I reviewed the ImplLoss candidate snapshot at `.scratch/round21/ImplLoss/tools/mori-evidence-loss.py` (1217 lines, read ranges cited); L1 integration may carry a different tip — recheck line numbers against the integrating copy.
- I did not run `--selftest` end-to-end (tests not authorized for this item); the three classify receipts above are the only executions performed, all read-only, no live writes, no network.
