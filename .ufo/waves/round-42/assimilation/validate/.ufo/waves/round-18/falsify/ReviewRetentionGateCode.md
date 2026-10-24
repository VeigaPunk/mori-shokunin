# Review: C1 retention gate at `e2bfbd6`

## Axes reviewed
Scope fidelity; hit-count and allowlist adjudication; output confidentiality; reproducibility against the frozen population.

## Findings (severity order)

**No actionable findings.** The attacked implementation follows the frozen C1 scan and count rules on the inspected paths, and the requested base-revision run reproduces the frozen population exactly.

Evidence:

- The frozen policy defines the scan as every tracked blob, NUL-containing blobs skipped, UTF-8 decoding with replacement, and lines split on `\n` (`.ufo/waves/round-18/frozen/c1-policy.json:5`). The implementation resolves the revision to a commit, enumerates `git ls-tree -r -z --full-tree`, reads blob objects, and scans each blob (`tools/mori-retention-gate.py:177-204`). `_blob_hits` implements the NUL skip, replacement decoding, `\n` splitting, and one presence check per line/class; emitted hit objects contain only path, line number, class, and the line SHA-256 (`tools/mori-retention-gate.py:89-103`). Symlink entries are blobs and are included; gitlinks are not blobs.
- Non-author paths use the frozen patterns through `fnmatch.fnmatch`; the metric excludes those hits. Routed counts are taken from the unallowlisted hits whose paths are in `must_redact_paths` (`tools/mori-retention-gate.py:121-122, 258-268`; policy `:17-28`).
- Allowlist rows are validated against the frozen fields and allowed rule values (`tools/mori-retention-gate.py:136-167`; contract `contract.md:55-61`). A row for a must-redact path is reported as `allowlist_forbidden`; a non-matching ordinary row is added to warnings as `allowlist_stale`. The exit expression fails on metric hits, forbidden rows, or population mismatch, but not stale warnings alone (`tools/mori-retention-gate.py:237-288`).
- The scan output includes hit metadata, not matched line contents (`tools/mori-retention-gate.py:292-300`). I checked each of the 119 emitted hit digests against the corresponding base-revision line: zero digest mismatches and zero matched-line-content occurrences in stdout; stderr was empty.
- Exit mapping is consistent with the frozen interface: the required base scan returns 1 for findings, and setup/evaluation failures return 2 (`tools/mori-retention-gate.py:288, 749-758`; `contract.md:24-29, 55-61`).

## Verification performed

The requested scan was run read-only against `d005cdd` with the frozen policy and `--expect-population`. Result: **rc=1, metric=116, routed=40, population_match=true**; `new_hits=0`, `missing_population_hits=0`. The result contains 119 total hits, of which 3 are non-author hits. This matches `.ufo/waves/round-18/frozen/c1-population.json`'s summary (119 total, 3 non-author, 40 must-redact, 116 metric) and `.ufo/waves/round-18/evidence/c1-before-d005cdd.json`.

I independently reimplemented the frozen traversal/decoding/count procedure over the `d005cdd` Git tree and compared all `(path, line, class, line_sha256)` records: 119 vs. 119, zero new and zero missing. The frozen policy SHA-256 is `db06e9810bbfd243fb0a753a46960573df39083ea90174ce463cf2a0ab523128`; the population file SHA-256 is `392c5ab49df3b019bab57ead013a4066cbdb9ad4e06bc7abb2f0166a97e251a2`.

To bind the result to the attacked revision rather than a mutable worktree, I also invoked the source blob `e2bfbd6:tools/mori-retention-gate.py` in memory. Its SHA-256 is `9d42f403373d976405e804251ed4a5d010eb648f05c05e02cd909d08a8e52d05`; it returned rc=1, metric=116, routed=40, population_match=true. A later scan of the committed `daceeec` and `e2bfbd6` revisions returned metric=55 and routed=0, consistent with the draft C1 count; the base population correctly did not match those later trees.

The frozen directory had no diff between `29b0dc7` and `e2bfbd6`; the policy digest at the freeze commit matches the recorded policy digest. Read-only exit probes for a missing revision, missing policy, and missing allowlist each returned 2.

## Residual risks and verification gaps

- The frozen policy explicitly calls its regex classes a recall floor, not a privacy proof (`frozen/c1-policy.json:29`); this review verifies the frozen metric, not the out-of-metric reading sweep.
- I did not run `--selftest` or create fixtures: this review was limited to read-only scan commands. Forbidden-allowlist, stale-warning-only, and synthetic binary/encoding behavior were checked in the implementation, not exercised in a fresh fixture run.
- The `lsp` device is not mounted (`xd://lsp` returned “No such tool”), so no LSP status/references/definition/diagnostics were available. Literal searches were used only to locate source anchors; behavioral evidence above comes from the code and read-only executions.
- No tools were installed or updated.
