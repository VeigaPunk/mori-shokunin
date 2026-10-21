# `policy_rules` audit

## Finding — gate/reconciler schema-domain mismatch (high confidence)

`/home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-retention-reconcile.py:90` requires the policy class list to be non-empty. The direct producer contract in `/home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-retention-gate.py:63-86` checks that this field is a list, then accepts an empty list. Its scanner at lines 89-103 naturally emits no class hits for that policy. A committed policy with an empty class list and empty path-rule lists therefore passes the gate and can yield a valid empty-hit receipt, but the reconciler's sole direct call at `mori-retention-reconcile.py:166` rejects it as setup-invalid before comparing the receipt. This is a concrete accepted-input mismatch, not a count-only conclusion.

## Bounded audit

The corrected denominator rule is accounted for: `policy_rules` returns the non-author globs; the reconciliation path scans the revision and partitions hits by those globs rather than specially removing the supplied policy file. In the reviewed function, the policy schema check, rule-list element types, duplicate class-id rejection, regex compilation error mapping, and return types otherwise align with the gate's corresponding validator. The only caller found is `check()` at line 166. No material repeated work/allocation issue was found in this scope.

Semantic LSP lookup was unavailable: no `lsp` device is mounted (`xd://lsp` reported no such tool). Caller linkage was therefore checked with literal search and source inspection, not semantic-reference evidence. Static inspection only; no execution or tests performed.
