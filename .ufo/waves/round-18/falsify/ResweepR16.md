# Round-16 privacy re-sweep at attacked tip

## Scope and method

Scanned every tracked text blob under `.ufo/waves/round-16/` at `e2bfbd6f8dccc51fc06455efc41f720301112dd4` with read-only `git grep -n -I -E`; `-I` excludes binary blobs. The family counts below are matching lines (one result per matching line, not occurrences). Matched source text was kept out of the report and the scan output; private-hit SHA-256 values are for the matched line text with the terminal newline omitted.

Command template used (one invocation per family):

```text
git -C /home/vgpnk/Projects/shokunin/mori-shokunin grep --no-color -n -I -E [-i] -e PATTERN e2bfbd6f8dccc51fc06455efc41f720301112dd4 -- .ufo/waves/round-16/
```

Return-code convention: `0` = matches; `1` = no matches. Final family results: email `1/0`; two-title-case-word name heuristic `0/40`; absolute host-home path `0/858`; `.config/` `0/1`; `sessions` `0/1`; broad timestamp-like `digitsTdigits|Z_` `0/55`; `Documents` `1/0`; `history` `0/5`; `sudo` `0/132`; `uid` `0/3`; `provider|model` `0/6`; `fallback` `0/27`. The exact C1 frozen patterns R1–R9 each returned `1` with zero matching lines. A first location-only wrapper selected the wrong colon fields because `git grep` prefixes the revision; I discarded those locations and used corrected captured output for these counts. No installs or updates were made.

## Family classification

| Family | Matching lines and classification | C1 result / assessment |
|---|---|---|
| Personal names / emails | Email-shaped: 0. A broad two-adjacent-title-case-word heuristic produced 40 candidate lines: 33 lane-authored text and 7 URL-bearing/public-source text. | No email or confirmed personal identity. The heuristic is noisy; `[INFERENCE]` the candidates are title/source phrasing, not personal names. |
| Absolute host-home paths | 858 lines: 632 lane/fleet paths, 220 synthetic-fixture paths, and **6 private-context paths outside the lane/fleet**. | The six private lines match no frozen R1–R9 class. This is the actionable C1 recall gap. |
| `.config/` | 1 synthetic illustrative example in a lane threat-model document; it uses a placeholder rather than an observed host value. | Not a private-context hit; no C1 class hit. |
| `sessions` | 1 lane-authored documentation use; no session-store path. | No R2 hit and no session identity found. |
| Timestamp/session-like strings | 55 broad matches: 51 lane-authored date/identifier text and 4 synthetic-fixture lines. | Strict R1 session-ID pattern: 0. No session identity found. |
| `Documents` | 0. | No R4 hit. |
| `history` | 5 lane-authored documentation uses; none is a shell-history path. | No R5 hit. |
| `sudo` | 132 lane-authored command/guard terminology; none is a privileged-config path/value. | No R6 (`sudoers`) hit. |
| `uid` | 3 lane-authored field/term mentions; no numeric UID assignment. | No private identity value found. |
| Provider/model strings | 6 lane-authored field/term mentions; no provider/model assignment or common provider/model identifier was found. | Consistent with the allowlisted field/aggregate distinction in triage; no private routing value found. |
| `fallback` | 27 lines: 23 lane-authored documentation uses and 4 URL-bearing/public-source lines. The sole colon-following prose match is ordinary narrative, not a configuration assignment. | No frozen R8 routing-table key or private fallback value found. |

The family classifications distinguish synthetic examples and public-source references from lane/fleet material; a keyword by itself (for example `sudo`, `uid`, or `history`) is not treated as private context without a private value/path.

## Private-context hits

New sweep family `S-HOME-OUTSIDE` (not represented by C1 R1–R9): six absolute host-home dot-directory path lines outside the lane/fleet. For each, replace only the full host-private path token with `<redacted-home-path>` while retaining the surrounding key/line structure.

| Location (lane-relative) | Sweep class | Frozen C1 class | Count | SHA-256 of matched line |
|---|---|---|---:|---|
| `.ufo/waves/round-16/build/ReviewCounts.md:11` | S-HOME-OUTSIDE | none (R1–R9) | 1 | `4bb1c973e3997cb824e8afb848f7f3b1a487cbd973b260dff474373f80da56b8` |
| `.ufo/waves/round-16/frozen/round15-spec.json:3` | S-HOME-OUTSIDE | none (R1–R9) | 1 | `cd724e288f1d1d75774995f6a48eba67e82b92069f0b1e74a29a36be48916d81` |
| `.ufo/waves/round-16/wave1-context-corrected-not-dispatched.json:3` | S-HOME-OUTSIDE | none (R1–R9) | 1 | `f57c950975d62cb98c34224acf74f5bee8a13051817ad27e4020648dc0e40874` |
| `.ufo/waves/round-16/wave1-dispatch.json:421` | S-HOME-OUTSIDE | none (R1–R9) | 1 | `87e9cd39461ce30fbb926d8a36503cfa87ee276aa683a6043f43b662f673ce8f` |
| `.ufo/waves/round-16/wave1-spec.json:3` | S-HOME-OUTSIDE | none (R1–R9) | 1 | `bf1fd13e3fbbe639215b96554789e4419f655a41c3e67b8e4e9df6b3dfad4d36` |
| `.ufo/waves/round-16/wave2-spec.json:3` | S-HOME-OUTSIDE | none (R1–R9) | 1 | `e72408b9cc8e6c6e7fecc1fb5060494810fbfeff151fe77d35eda6da3469f7cd` |

The known privileged-group-membership carry at `.ufo/waves/round-16/build/SiblingScope.md:20` is a separate, already-triaged private-context item, not a hit in the requested token families: count 1; class `triage-carry/privileged-group-membership` (no frozen R1–R9 class); line SHA-256 `737771706c75d9dfc9d6db94181652a17ce0a3f3eb8f5bcd99c503d588e321a6`. Keep its private value minimized independently of this token sweep.

## Comparison with L1 triage

`out-of-metric-triage.md:10-17` states the broad privacy rule; `:23` and `:29` already cover identity/session/document/config and name/email families; `:26` covers provider/model fields and aggregates; and `:34` explicitly carries the SiblingScope privileged-group item. Those are not new omissions.

**Miss / incorrect disposition:** `out-of-metric-triage.md:28` discusses host environment paths but rejects them on the rationale that the home path is already present in lane paths. This re-sweep finds six actual absolute home-dotdir values outside the lane/fleet in other round-16 files, none covered by a frozen C1 class and none individually disposed in the triage table. The family needs minimization; the stated lane-path rationale does not fit these six hits. This also falsifies the draft's claim of complete whole-round privacy repair (`draft-verdicts.md:8`): the path-family sweep remains partial.

**Non-actionable wording gaps:** the triage disposition table does not name standalone `uid` or generic `fallback` as separate families. The observed hits are lane documentation/field terminology without UID or routing values, so they do not establish a privacy omission. The literal `.config/` hit is an illustrative placeholder, not an operator path.
