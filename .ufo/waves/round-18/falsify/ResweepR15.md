# Round-15 privacy resweep — falsification of L1 triage

## Scope and method

- Scanned the explicitly requested attacked snapshot `e2bfbd6f8dccc51fc06455efc41f720301112dd4` under `.ufo/waves/round-15/`, using read-only `git -C /home/vgpnk/Projects/shokunin/mori-shokunin grep -n -I -E` searches. `-i` was added for case-insensitive terms. `-I` excluded binary blobs; scope is every tracked text blob searchable by `git grep` at that snapshot. `git ls-tree -r --name-only ... | wc -l` counted 1,403 tracked paths (pipeline exit 0).
- The scan counts matching lines, not repeated matches within a line. For broad tokens, counts include technical prose and source code as well as fixture data; they are not private-hit counts.
- Revision caveat: at observation time `git log -1 --format=%H master` returned `95c615836c2cf74ee11539c4289a1ce06a81cfcb` (exit 0), while the requested snapshot resolved to `e2bfbd6f8dccc51fc06455efc41f720301112dd4` (exit 0). Every sweep query was pinned to the requested snapshot, not the moving branch name.
- No tools were installed or updated. No external URLs were used.

## Observed family counts and classification

The following are raw line counts from the token-family `git grep` scans. A successful non-empty grep pipeline returned 0; a zero-match grep pipeline returned 1 (`set -o pipefail`, count piped through `wc -l`). Exact-shape zero checks are separately noted below.

| Family | Matching lines | Classification / exact-shape result |
|---|---:|---|
| Email-shaped strings | 193 | Synthetic self-test author/address fixtures plus a technical template mention; contextual review found 0 confirmed personal email addresses. The non-placeholder heuristic subset was source-test data/template syntax, not personal identity. |
| Personal-name candidates | 746 broad two-capitalized-word candidates; 0 explicit author/name/contact-label matches | The broad form is too noisy to establish people; it catches technical/document phrases. No personal name was confirmed. Residual gap: unlabelled personal names cannot be ruled out by this lexical screen. |
| Host-home paths | 9,453 | 9,446 lane/fleet paths; 3 outside-root fixture/example-context lines; 4 private-context lines outside the lane/fleet. These four are listed below without their path values. |
| `.config/` | 0 | No match (grep pipeline exit 1). |
| `sessions` / `session` | 1,209 | Generic technical/document and synthetic-fixture mentions; no exact session-store path found. No frozen R1 or `Z_` identifier shape was found (see below). |
| Timestamp/session-like candidates (`digits T digits` or `Z_`) | 7,644 | 7,265 lines are in evidence run outputs, 355 in other evidence, 17 in build reports, and 7 elsewhere. 7,582 lines match one of the checked compact or ISO date-time patterns; the remaining 62 match the broader digit-T-digit form. By file location, these are test/run timestamps or technical records; no session ID was confirmed. `Z_` count: 0 (exit 1); frozen C1 R1 identity shape: 0 (exit 1). |
| `Documents` | 9 | General technical/document mentions; personal-document path forms: 0 (exit 1). |
| `history` | 104 | Technical prose and fixture/source references; shell-history path forms: 0 (exit 1). |
| `sudo` | 129 | Technical instructions/source references; privileged-config (`sudoers`) token: 0 (exit 1). |
| `uid` | 21 | Technical field/variable references in source copies and reports; no personal account record or operator UID value confirmed. |
| Provider/model strings | 18 | Technical/lane/product terminology and synthetic/source references; no private routing assignment or operator model value confirmed. |
| `fallback` | 171 | Technical prose/source and fixture references; no `fallbackChains` key or JSON `fallback` value key (combined exact-key check: 0, exit 1). No private routing value confirmed. |

The exact personal-name label scan had 0 lines (grep exit 1); the 746-line broad candidate scan is not semantic proof of a name. The `uid`, provider/model, and `fallback` family matches are classified as technical/lane documentation or fixture/source material, not private context. For session, document, history, and privileged-configuration families, the broad token hits are not path/value hits; the exact checks above found none.

## Private-context findings

One out-of-metric class was observed: `RS1` = host-home path value outside the lane/fleet. Count: **4 lines across 4 blobs**. The original path values are deliberately omitted. Minimal redaction: replace only each host-specific absolute path token with `<HOME_PATH>`; in source-census records, retain a repo-relative path where that preserves the evidence purpose.

| Lane-relative location | Sweep class | Count | Blob SHA-256 |
|---|---|---:|---|
| `.ufo/waves/round-15/build/ConnectSiblingOverlap.md:52` | RS1 | 1 | `af388ea2c7a776594585125621a533d635c5c8c600dc27b18d2903b962f06b57` |
| `.ufo/waves/round-15/build/ReconProtectedTeaching.md:98` | RS1 | 1 | `4c78588bbadb696fd2ec7c1af64818087e00d09e95e93a2bb92032b6e4ac780d` |
| `.ufo/waves/round-15/evidence/sources-after.json:8` | RS1 | 1 | `4ee9beafbb490e2b666cba43fd1496bab5f114870d56b8758008a3681296e4c3` |
| `.ufo/waves/round-15/sources-after.json:8` | RS1 | 1 | `b7e885edecbe4742a4b84ec04eaa957468b710e7d6d6b253616f8750541936c1` |

Each SHA-256 was computed from `git show e2bfbd6:<path> | sha256sum`; all four pipelines exited 0. These hits are outside the frozen C1 token patterns (see `.ufo/waves/round-18/frozen/c1-policy.json:7-15`), so they are an out-of-metric privacy finding rather than a C1 count claim.

## Comparison with the L1 out-of-metric triage

Observed triage coverage: `.ufo/waves/round-18/out-of-metric-triage.md:10-16` names the general privacy rule and exclusions; `:22-29` disposition rows cover frozen-class identity tokens, session/document/config references, provider/model class tokens, host environment paths, and personal name/email; `:34-35` says earlier round-15 material is carried and the dead round-15 wave-1 sweep is a coverage gap. The provisional C1 verdict itself calls whole-round repair partial (`.ufo/waves/round-18/draft-verdicts.md:8`).

Falsification / gaps:

1. **Host-home-path rejection is overbroad for this snapshot.** The triage row at `out-of-metric-triage.md:28` rejects host environment paths on the rationale that the home path is already in every lane path. The four RS1 hits above are outside the lane/fleet root, so that rationale does not establish they are lane paths. The r15 `carry` row (`:34`) does not adjudicate these values. Recommend minimizing these four values rather than carrying them unchanged.
2. **Earlier-round personal-identity disposition is incomplete at file-family scope.** The triage's personal name/email row (`:29`) lists other locations; the r15 row and wave-1 coverage-gap row (`:34-35`) do not provide a per-family closure for all r15 text. This sweep found no confirmed personal email and no confirmed labeled personal name, but the 746 noisy name-form candidates remain a stated detection limitation.
3. **Literal `.config/`, `uid`, and `fallback` are not separately named in the triage disposition table.** The general rule at `:10-13` may subsume configuration/routing values, and no private `.config/`, UID, or fallback value was observed here; nevertheless, the table does not make their family-level handling explicit. The `fallback` exact-key check and C1 policy key coverage (`frozen/c1-policy.json:14-15`) do not convert the broad lexical hits into private values.
4. Session identities, personal-document paths, shell-history paths, and privileged-config tokens are addressed by the triage rule and frozen-class rows; this sweep found no exact private path/value instance for those families. Provider/model terminology is explicitly treated as an allowlisted class token/aggregate at `out-of-metric-triage.md:26`; none of the r15 matches established private configuration values.

## Evidence commands and statuses

- Sweep form: `git -C /home/vgpnk/Projects/shokunin/mori-shokunin grep -n -I -E '<family-pattern>' e2bfbd6 -- .ufo/waves/round-15/` (case-insensitive families used `-i`). Non-empty family pipelines returned exit 0; `.config/` returned 0 lines / exit 1.
- Exact no-match checks returned 0 lines / exit 1 for session-store paths, frozen C1 R1 session IDs, `Z_`, personal-document paths, shell-history paths, `sudoers`, explicit person-name labels, `fallbackChains`, and JSON `fallback` keys.
- Snapshot path count: 1,403; `git ls-tree ... | wc -l` pipeline exit 0. Branch/snapshot `git log -1` lookups both exited 0.
- No file content or private value is quoted in this report.
