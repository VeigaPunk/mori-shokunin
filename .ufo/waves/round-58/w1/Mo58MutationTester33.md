# Mo58MutationTester33 — C2 quote-binding mutation probe

## Result: counterexample — short substrings and duplicate keys survive

Bounded detector: frozen `count-c2.py --selftest` on the pinned bytes returned `C2_SELFTEST pass=6 fail=0` (exit 0). I then invoked the frozen `measure(rev)` function against four isolated throwaway git fixtures in `/fast/scratch/hyaku/mori-r58/Mo58MutationTester33/fixtures`, each containing a proper S550 row, required frontmatter, and a matching pinned copy/tool unless noted.

- **Valid locator on wrong line:** each of eight quotes was the ≥12-character phrase `open_launches bookkeeping #11`, which exists in the copy but not at its declared line. Output: `C2=unmet claims=8 located=0 copy=ok tree=ok rows=ok sources=ok failed=quotes` (exit 1). Killed.
- **Short substring:** eight distinct K rows each quote `` `def parse_log` `` at line 1. The quote is a short substring of the source line; output: `C2=met claims=8 located=8 copy=ok tree=ok rows=ok sources=ok failed=none` (exit 0). **Survived.** The check imposes no minimum quote length despite the ≥12-character restriction in its matching predicate; it accepts any backtick span that is a substring on the locator line.
- **Duplicate K numbers:** eight rows were labeled K1 seven times and K8 once, each with a matching source substring and line. Output: `C2=met claims=8 located=8 copy=ok tree=ok rows=ok sources=ok failed=none` (exit 0). **Survived.** Counter counts matching rows, not distinct K identifiers.
- **Stale pinned copy:** pinned copy differed from tool by one trailing `# stale pin` line. Output: `C2=unmet claims=8 located=8 copy=bad tree=bad rows=ok sources=ok failed=copy` (exit 1). Killed.

These are detector coverage findings only; no contract change/remediation proposed. Fabricated quotes absent from the copy are already covered by the junk-quotes selftest arm. The wrong-line arm above directly exercises valid locator plus quote present elsewhere, rather than relying on fabricated text.

## Restoration / bounds

No production bytes were changed. The scratch counter was the exact freeze-revision file; its SHA-256 before/after was `aab888ad787964f7a153d64d85dafa58f652f977e21e22eaa492706a691010d3`, byte-identical to `git show fe8801120a67c1a6b8899d7d0423839caa09e7d0:.ufo/waves/round-58/count-c2.py`. Fixture mutations were confined to disposable repositories in the seat scratch directory. Disk guard status reported `/fast/scratch/hyaku` at 32% use with 552.5G free. No tool installed or updated.
