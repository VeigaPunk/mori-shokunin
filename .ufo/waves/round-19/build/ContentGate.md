# ContentGate implementation report

## Changed file
- `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-19/ContentGateSparse/tools/mori-content-review.py` — new C1 gate and isolated `--selftest` implementation.

## Behavior
- Resolves `--rev` to a full commit OID; pins the population bytes to `--expected-sha256`; reads the population/reviews files once each and hashes the same loaded bytes used for parsing.
- Requires the frozen schema, a unique normalized population path list, exactly one valid review row per path, a Git blob at the resolved revision, and matching full SHA-256 values. Duplicate/unknown rows, malformed input, unavailable paths, invalid revisions, and pin mismatch return could-not-evaluate (2). Missing rows, stale digests, unresolved decisions, and provenance-only reviews fail closed (1); a complete content-reviewed population returns clean (0).
- Emits resolved revision, population/review/script SHA-256 values, per-population full blob digests, counts, and stable finding codes. It does not emit review reasons or file contents. The selftest creates a synthetic Git fixture only under an explicit `TMPDIR` contained by this lane worktree.

## Retained evidence
- `.ufo/waves/round-19/contract.md:3` — entry revision context.
- `.ufo/waves/round-19/contract.md:6` — C1 scope and privacy class.
- `.ufo/waves/round-19/contract.md:9-10` — C1 interface and outcome classes.
- `.ufo/waves/round-19/contract.md:12` — synthetic fixture boundary.
- `.ufo/waves/round-19/frozen/expected.json:3-20` — C1 case and finding classes.
- `.ufo/waves/round-19/contract.md: f292d3bc64299908e831880632bb18480c80b0a35290b3bce5b70063452a5d1d` — full artifact SHA-256.
- `.ufo/waves/round-19/frozen/expected.json: c5c6c67f104ed1baa57a56bfb22728a2e871ca174a4915ff4005eb3485abe22a` — full artifact SHA-256.
- `.ufo/waves/round-19/frozen/content-population.json: 4a50e77a1f436d349a62100cbac59f4dd337c3f48e63b5a31519d1d2231d581b` — full artifact SHA-256.
- Freeze revision from assignment context: `5e393d20daa628a0b4ca9aa6a1626aa54285b3f0`; no runtime target revision was measured because the gate was not run.

## Risks and blockers
- Review outcome and `content_basis` are reviewer declarations; the gate enforces their schema and disposition but does not independently assess content or the semantic safety of a reason. Reasons remain un-emitted.
- No blocking implementation dependency. LSP is unavailable in the mounted tool inventory; this new standalone file has no existing symbols or callsites to refactor.

## Checks
- Not run: `--selftest`, round-19 acceptance harness, builds, tests, lint, formatting, or smoke checks. Parent integration owns post-wave verification.
