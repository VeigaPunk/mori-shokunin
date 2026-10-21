# Round-13 privacy re-sweep at e2bfbd6

## Scope and method

Swept tracked entries under `.ufo/waves/round-13/` at revision `e2bfbd6` with read-only `git -C /home/vgpnk/Projects/shokunin/mori-shokunin ls-tree` and `git grep -n -I -E`; the tree contains 283 tracked entries. `-I` excludes binary blobs. Counts below are matching lines (not distinct values); probes overlap, so totals are not additive. No probe output was written to disk. The only write from this seat is this report; no tool was installed or updated and no tests/builds were run.

Matched `git grep` scans returned 0; no-match scans returned 1 (normal no-match status). Count-only pipelines completed with status 0. SHA-256 values below identify whole blobs at the swept revision and are provenance only.

## Family counts and classification

| Family / probe | Matching lines (files) | Classification and result |
|---|---:|---|
| Personal names / email-like strings | 90 (21) | Email-shaped hits were synthetic author-fixture identities and systemd unit-field spellings. No personal address was identified. No standalone human name was confirmed by this token scan; the operator account identifier appears in the separate `uid` finding below. A token scan cannot prove absence of prose-embedded names. |
| Absolute operator-home paths outside lane/fleet | 2 (2) | Private-context candidates [INFERENCE]; detailed paths below. |
| `~` / `$HOME` paths | 8 (4) | Private-context candidates [INFERENCE]; one line overlaps the absolute-path probe, for 9 unique path-bearing lines total. |
| `.config/` | 0 | No match. |
| `session` (case-insensitive) | 514 (25) | Mixed lane documentation/code and synthetic regression-capture output. No session identity or store path was found by the frozen-form probes. |
| Timestamp-like forms | 613 for `[0-9]+T[0-9]+` or `Z_`; 573 for ISO date-time form | Lane receipts and synthetic test timestamps, not session identities. Exact frozen R1 identity form and `Z_` outside R1: 0. |
| `Documents` | 1 (1) | Generic technical prose, not a personal-document path. |
| `history` (case-insensitive) | 108 (41) | Git/journal/history terminology in lane docs and artifacts; no shell-history marker. |
| `sudo` (case-insensitive) | 3 (3) | Lane probe/install command text; no privileged-config path. |
| `uid` (whole word, case-insensitive) | 33 (12) | 30 technical UID references; 3 lines contain an operator account identifier and, on one line, privileged-group membership. See confirmed finding below. |
| Provider/model vendor identifiers | 0 | No match for the vendor/model identifier probe. |
| `fallback` (case-insensitive) | 37 (11) | Technical fallback discussion/code; no private routing-table key or value matched. |
| Supplementary `.omp` / `agent.db` / `oauth` / `credential` probe | 19 (15) | Generic lane prose and negative assertions; no credential or operator configuration value identified. |

The frozen C1 forms R1–R9 were also checked in this scope: no session identity/store path, tool-output artifact id, personal-document path, shell-history marker, sudoers/config reference, routing-table key, or session-record-value form matched. The `Documents` word hit is not an R4 path. This confirms only the probed forms, not general privacy safety.

## Private-context findings and candidates

### `R13-UID-GROUP` — observed private-context family

The matched lines are `.ufo/waves/round-13/build/JSONAttack.md:179,186,263` (3 lines, one blob). These expose the operator account identity in host-observation material; one line also exposes privileged-group membership. This is consistent with the out-of-metric register's personal-identity rule and its carried privileged-group precedent, but the round-13 occurrences are not named in that register.

Minimal redaction: replace the account label with a generic `<account>` marker and retain only the group-count or the minimum boolean needed for the technical claim. Preserve unrelated UID/cgroup mechanics.

Whole-file SHA-256: `.ufo/waves/round-13/build/JSONAttack.md` — `544247290c44d64e20e3a278135228d460bf059cc1d647ff4413737970d6b9ca`.

### `R13-HOME-PATH` — conservative candidate, not a confirmed L1-rule breach [INFERENCE]

Private-context candidate path:line references (no values reproduced):

- `.ufo/waves/round-13/build/JSONAttack.md:36,93,148,202`
- `.ufo/waves/round-13/build/Safety.md:171`
- `.ufo/waves/round-13/build/SiblingOverlap.md:48`
- `.ufo/waves/round-13/build/ReviewPromotion.md:13-14,18`

The matches include user-local executable paths and project/tool paths outside the literal lane and fleet roots. The out-of-metric register explicitly rejects generic host HOME/XDG-path disclosures when they are merely lane environment facts (`out-of-metric-triage.md:28`), so these are not asserted as confirmed findings. However, its decision does not individually adjudicate the user-local executable and non-fleet project/tool paths above; this re-sweep conservatively flags them for L1 review.

Minimal redaction: retain only the needed technical fact (for example, that a user-local executable wins PATH resolution); replace home-rooted executable and project/config locations with generic labels, omitting user and project names.

Whole-file SHA-256 values:

- `.ufo/waves/round-13/build/JSONAttack.md` — `544247290c44d64e20e3a278135228d460bf059cc1d647ff4413737970d6b9ca`
- `.ufo/waves/round-13/build/Safety.md` — `9ee7ac7a0325f8c8f8aa1fa525e0c0a90609a5cabdfc3f2caacb379b07afa892`
- `.ufo/waves/round-13/build/SiblingOverlap.md` — `eaf8ce4648a137a42c34ce63b4077d37e335c1ed45e3e08c3ae66eb6272ef522`
- `.ufo/waves/round-13/build/ReviewPromotion.md` — `c786ed055c0b49a00761645d8148d5a91a86a6d37ea0e0d88588da8090b7667c`

## Comparison with the out-of-metric triage

The triage says the frozen classes are a recall floor and that personal identities/emails, session identities, personal documents, shell history, privileged configuration, and configuration/routing values are within its privacy rule (`out-of-metric-triage.md:3-16`). It also records a coverage gap for the round-13/14 sweep (`:35`).

Freshly surfaced family: the specific round-13 account/group observations at `JSONAttack.md:179,186,263` are not listed in the triage's named dispositions, although personal identity is already within its general rule and privileged-group membership is noted as a carried r16 item at `out-of-metric-triage.md:34`. This is a missed occurrence, not a new policy class.

Potential additional gap: home-rooted tool/project paths outside the lane/fleet are only indirectly covered by the broad HOME/XDG rejection at `out-of-metric-triage.md:28`; the specific non-fleet path disclosures remain unresolved. Recommend L1 adjudication rather than treating the existing rejection as proof that all such paths are harmless.

Other requested families either resolve to synthetic fixtures/lane or public technical material, are covered by the triage/frozen rules without matching private forms, or had no matches. No report excerpts or private values are reproduced here.