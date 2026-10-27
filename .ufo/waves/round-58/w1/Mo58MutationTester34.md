# Mo58MutationTester34 — C2 S550 registry binding probe

- Frozen counter: `.ufo/waves/round-58/count-c2.py`, sourced from freeze `fe8801120a67c1a6b8899d7d0423839caa09e7d0`; scratch copy SHA-256 `aab888ad787964f7a153d64d85dafa58f652f977e21e22eaa492706a691010d3`.
- Bounded method: imported the frozen counter unchanged; for each case built a separate throwaway Git fixture at `/fast/scratch/hyaku/mori-r58/Mo58MutationTester34/` using the counter's own `_mkrepo` fixture builder, with `ENTRY_OK`, `TOOL_TEXT`, and a varied SOURCES row. Called `measure(rev)` directly against each fixture revision. Pristine row is the counter's `ROW_OK`.
- Pristine output: `C2=met claims=8 located=8 copy=ok tree=ok rows=ok sources=ok failed=none rev=83cc6b40324a3fe76e9187fe134be4336d445b6a`, exit 0.

| Row mutation | Exact detector output | Exit | Verdict |
|---|---|---:|---|
| Duplicate S550 row | `C2=unmet claims=8 located=8 copy=ok tree=ok rows=bad sources=ok failed=rows rev=a24e796c88afdd19f41be848b72074769f0ce689` | 1 | Killed |
| Wrong status (`draft`) | `C2=unmet claims=8 located=8 copy=ok tree=ok rows=bad sources=ok failed=rows rev=580c42ff3324bc18115a6fc72d50432ae34cdfac` | 1 | Killed |
| Dangling used-by target | `C2=unmet claims=8 located=8 copy=ok tree=ok rows=bad sources=ok failed=rows rev=a6b6d0a17f6dbe0f480849dde072ddc07838f0a4` | 1 | Killed |
| Malformed (short) column count | `C2=unmet claims=8 located=8 copy=ok tree=ok rows=bad sources=ok failed=rows rev=53111f3c0791c477ad59c6d89fd18721608c987a` | 1 | Killed |
| Lookalike ID `S550x` | `C2=unmet claims=8 located=8 copy=ok tree=ok rows=bad sources=ok failed=rows rev=5c6cc6f27e74a96ace7dbdd55e3ef02bc9d995e0` | 1 | Killed |

No counterexample found among these five specified mutations. The baseline was met and all mutations were rejected by `rows=bad`; no detector-level inconclusive case. Counter bytes were never modified; no restoration was needed. Scratch fixture files were created only in the assigned scratch root and removed after copying this receipt here.