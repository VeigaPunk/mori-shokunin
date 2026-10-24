# S059 — git-log(1)

- **URL:** https://git-scm.com/docs/git-log
- **Accessed:** 2026-10-21. The opened page identifies git-log 2.56.0 as latest (last updated 2026-09-28).
- **Actual location:** `OPTIONS` → `--diff-merges=<format>`, rendered lines 2241–2244. The adjacent `on` format description at lines 2258–2260 says `log.diffMerges` can change the default format.
- **Located quote (15 words):** “Default is `off` unless `--first-parent` is in use, in which case `first-parent` is the default.”
- **Source scope:** The git-log command reference documents log traversal/output options and merge-diff formatting behavior. This passage supports conditional merge-diff defaults; it does not establish the round-19 contract’s permitted command set or a plumbing/porcelain boundary.
- **Proposed disposition: REJECT** for the C2 freeze-order verdict: retain the existing row’s rationale that git-log is a porcelain alternative outside the contract’s plumbing set and adds no needed ordering fact beyond the admitted plumbing references. The opened text confirms that its merge-diff presentation can vary with `--first-parent` and the adjacent `log.diffMerges` setting, but that is not needed for the freeze-order claim.
- **Flip:** Admit only as a narrowly scoped cross-check if the verdict must interpret rendered merge-diff output; its scope would be merge presentation/defaults, not the C2 traversal/order authority.

Append this correction as a lesson only; do not rewrite the immutable S059 registry row. No tests or verification runs were performed.