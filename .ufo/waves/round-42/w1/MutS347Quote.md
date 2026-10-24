# MutS347Quote — mutation probe: S347 grounding quote ↔ source copy

Role: mutation-tester (leaf). Probe only; no integration judgment, no contract change.

## Target binding under test

- Entry: `corpus/knowledge/conform-source-order-r42.md` (sha256 `c1210a9c…f7f9a1`, 2476 bytes)
- Ground copy: `corpus/evidence/sources-r42/S347.html` (sha256 `6fc1fad2…c2a97e82`, 362029 bytes)
- Located quote (Claim, line 13): `ast.walk` "yields descendant nodes **"in no specified order"**".
- Copy location: byte 325634 of S347.html, inside the `id="ast.walk"` `<dl>` block
  (`…(including <em>node</em> itself), in no specified order.  This is useful if you only…`).
  Exactly one occurrence in the copy.

## Mutant (one word, behavior-bearing)

Scratch copy only (`/tmp/muts347-quote2/entry.md`); the lane file was never written.

```diff
--- a/corpus/knowledge/conform-source-order-r42.md
+++ b/corpus/knowledge/conform-source-order-r42.md
@@ -11,3 +11,3 @@
-`ast.walk` documents that it yields descendant nodes "in no specified order",
+`ast.walk` documents that it yields descendant nodes "in a specified order",
```

`no` → `a`: the documented absence of a guarantee is inverted into a fabricated
guarantee. Mutant sha256 `804858755e6280564c6cd2b3da4045fdc4ce466360c3d5b91ba013830a8e87fc` (2475 bytes).

## Expected detector (bounded, single behavior)

`D1-quote-to-copy` (`/tmp/muts347-quote/detector.py`), 3 assertions:

1. extract the double-quoted fragment following `yields descendant nodes` from the entry
   (quote must be extractable — exit 2 otherwise);
2. the exact quote string occurs **once** in the S347.html copy;
3. that occurrence lies inside the `id="ast.walk"` block (anchor → next `</dd></dl>`).

Exit 0 = PASS (binding holds), exit 1 = FAIL (quote-to-copy binding broken).
The same detector and the same frozen copy (`6fc1fad2…`) were used for all runs; only the
entry bytes varied.

## Runs — red-before witness

| run | entry bytes sha256 | detector quote extracted | occurrences in copy | inside ast.walk | exit | verdict |
|---|---|---|---|---|---|---|
| pristine (scratch, pre-mutation) | `c1210a9c…` | `in no specified order` | 1 | true | 0 | PASS |
| pristine (lane source, read-only) | `c1210a9c…` | `in no specified order` | 1 | true | 0 | PASS |
| **mutated** | `80485875…` | `in a specified order` | **0** | false | **1** | **FAIL** |
| restored | `c1210a9c…` | `in no specified order` | 1 | true | 0 | PASS |

Red-before is the mutated row: the detector emitted red (exit 1,
`occurrences_in_copy: 0`, `context: ""`) while the copy hash stayed
`6fc1fad2d634c8a5…` — the failure is attributable to the one-word entry mutation, not to
copy substitution. Baseline was green twice before the mutation (scratch and lane bytes),
so the failure is not a pre-existing detector defect.

Detector stdout (pristine): `{"quote":"in no specified order","occurrences_in_copy":1,
"inside_ast_walk_block":true,"context":"…itself), in no specified order.  This is useful…","verdict":"PASS"}`

Detector stdout (mutated): `{"quote":"in a specified order","occurrences_in_copy":0,
"inside_ast_walk_block":false,"context":"","copy_sha256":"6fc1fad2d634c8a5","verdict":"FAIL"}`

## Verdict

**KILLED** — by `D1-quote-to-copy`. The mutated quote has no byte sequence in the bound
copy, so a quote-to-copy verifier rejects the falsified entry.

## Coverage observation (finding, not a contract change)

The kill is delivered only by the assigned detector; **no committed lane artifact would
have caught this mutant**:

- The entry's own `recheck:` line (`grep -c 'no specified order'` -> 1) still returns `1` on
  the mutated entry — the pattern is a duplicated literal, not derived from the Claim quote,
  so the recorded recheck is insensitive to the falsified claim (measured: count 1).
- `corpus/SOURCES.md` row S347 still carries `in no specified order` (1 row), so the registry
  and the entry now contradict each other with no cross-file consistency check to notice.
- No quote/verbatim-binding check exists in the lane: grep for `quote|verbatim` across
  `.ufo/waves/round-42/**/*.py` returns only conform.py's unrelated contract "P-C7
  blockquote" guard; `conform.py` never reads `corpus/`. `contract.md` binds C1/C2/C3
  counters, not source quotes.
- The only residual signal is prose-level: the mutated sentence contradicts the entry's own
  title ("walk order is unspecified") and the following sentence ("cannot rely on
  construction order"). That is detectable by a reader, not by a mechanical check.

Consequence: quote-to-copy binding for S347 exists as a claim and as a copy, but is not
continuously enforced by any landed tool — the mutation survives every committed check and
is killed only by an out-of-tree probe.

## Restoration evidence

Lane files were never mutated; only `/tmp/muts347-quote2/entry.md` was edited, then
overwritten from `entry.orig`.

| artifact | before | after | equal |
|---|---|---|---|
| lane `corpus/knowledge/conform-source-order-r42.md` | `c1210a9c0a3958ccae27d4dece571859e14961b33634c8933acd05f35ef7f9a1` | same | yes |
| lane `corpus/evidence/sources-r42/S347.html` | `6fc1fad2d634c8a58045c865e0096370f2770f6729489c24e3f6c6b4c2a97e82` | same | yes |
| scratch entry after restore | — | `c1210a9c…f7f9a1` (= original) | yes |

Scratch: `/tmp/muts347-quote/`, `/tmp/muts347-quote2/` (disposable). No lane jj/Git index
writes, no fleet or sibling-repo writes, no secrets read.

## Tooling

None installed or updated (`python3` stdlib only: `re`, `hashlib`, `subprocess`, `difflib`).
`pacman` not invoked.
