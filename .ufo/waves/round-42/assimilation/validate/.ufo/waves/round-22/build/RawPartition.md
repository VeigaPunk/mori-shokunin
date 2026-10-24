# RawPartition — round-21 retention-floor receipt partition audit (read-only scout)

Seat `MoriR22.RawPartition`. Source analysed: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-21/evidence/final/retention-floor.json` (file sha256 `4001e2d94afcc652b710d5d0afe63bffce2185256f120d5a5f7d33de6be8c840`, 33050 bytes; unchanged by this seat). Also read: `.ufo/waves/round-22/contract.md`. The referenced policy and allowlist were read as Git blobs at the measured revision through `git -C <repo> cat-file`/`ls-tree`/`merge-base` (read-only plumbing). No matched text, no line content, and no `must_redact_paths` values were printed or recorded. No tests, builds, gates or scanners were run. No tools were installed or updated.

## Headline finding (observed)

**The "5 policy source hits" in the open debt are actually the 5 non-author glob exclusions, not hits on the policy file.** Hits whose path equals the supplied policy path number **4**, not 5, and all 4 are *allowlisted*. So 95 − 90 = 5 is the non-author exclusion. It is not a policy-path exclusion. Under the round-22 contract definition (remove exactly the supplied policy path), the counts are: scanner-compatible total **91**, policy_excluded **4**, scanner_unallowlisted **4**.

The 4 retained unallowlisted hits all sit on a committed nested copy of the policy file: `.ufo/waves/round-20/falsify/NoHarmRun/rg/.ufo/waves/round-18/frozen/c1-policy.json`. That copy is byte-identical to the policy: same Git blob `8bf285bddce57f7fdefbbf514cb0b3bf97652742`, sha256 `db06e981…3128`. Its 4 (line, class, line_sha256) tuples equal the exact policy path's 4 tuples (lines 8, 11, 12, 14). The allowlist has 4 rows on the exact policy path and 0 rows on the nested copy.

## Wrapper fields (observed)

| field | value |
|---|---|
| schema | `mori-r21-command-receipt-v1` |
| measured_revision | `9fb1f911cfdd6061005c300795f44b1b45523897` (object type `commit`; ancestor of entering branch `77a5bbe8…`: yes) |
| argv | 11 elements: `python3 tools/mori-retention-gate.py scan --repo … --rev <measured> --policy …/.ufo/waves/round-18/frozen/c1-policy.json --allowlist …/corpus/evidence/retention-allowlist.json` (absolute paths) |
| exit_code | 1 (int) |
| stderr | empty |
| stdout | 29662 chars, sha256 `c9f427a63e7ff25a3bc1c4b5754bfa0bfdaf1f039631e9f0cc4c454e4ae2c381` |
| stdout.commit | equals measured_revision |
| stdout.finding_id | `RETENTION_FINDINGS` |
| stdout.policy_sha256 | `db06e9810bbfd243fb0a753a46960573df39083ea90174ce463cf2a0ab523128` = policy blob sha256 at measured rev (3224 bytes) |

The receipt has no loaded-input or executing-tool sha256 fields beyond `policy_sha256`. There is no allowlist sha256 and no gate-script sha256. Contract R24 provenance must therefore be computed by the new tool. The r21 wrapper does not supply it.

## Raw total and every partition counter (observed)

| counter | value | how derived |
|---|---|---|
| raw total (`hits`) | **95** | 95 distinct identities, 0 duplicates |
| `allowlisted_hits` | **86** | subset of hits |
| `unallowlisted_hits` | **4** | subset of hits; disjoint from allowlisted |
| non-author residual (hits − allowlisted − unallowlisted) | **5** | equals receipt `non_author`=5 |
| receipt `metric` | **4** | equals the unallowlisted count |
| receipt `non_author` | **5** | |
| receipt `routed` | **0** | |
| `forbidden_allowlist` | **0** entries | |
| `warnings` | **0** entries | |
| allowlist rows at measured rev | 86 | equals the allowlisted count |
| hits on `must_redact_paths` (3 paths, values not printed) | 0 | |
| **policy-path hit count** (exact path `.ufo/waves/round-18/frozen/c1-policy.json`) | **4** | 4 allowlisted, 0 unallowlisted, 0 non-author |
| hits on the byte-identical nested policy copy | 4 | all 4 unallowlisted |

The partition closes exactly by identity: 86 + 4 + 5 = 95, all three parts are pairwise disjoint, and every part is a subset of `hits`.

The 5 non-author hits are exactly the raw hits matching the policy `non_author_paths_glob`, which is `['corpus/lessons/round-*-verifier-spotcheck.md', 'corpus/lessons/operator-*.md']`. They fall as 3 on `corpus/lessons/round-17-verifier-spotcheck.md` and 2 on `corpus/lessons/round-18-verifier-spotcheck.md`. Their classes are R6×3, R5×1, R9×1.

Class histograms:
- raw: R6 37, R9 15, R5 14, R7 10, R4 8, R8 8, R2 3.
- policy-path hits: R2, R5, R6, R8, one each.
- unallowlisted hits: R2, R5, R6, R8, one each.

The policy declares classes R1–R9.

## Contract denominators derived from receipt identities (inference from observed lists, not an independent regex rescan)

| contract field | value |
|---|---|
| raw_total | 95 |
| policy_excluded | 4 |
| scanner_total (raw minus exact policy path only) | 91 |
| raw_unallowlisted | 4 |
| scanner_unallowlisted | 4 |
| non_author | 5 |
| forbidden_allowlist | 0 |
| privacy_clearance | false (always) |

Removing the policy path does not change the unallowlisted count, because all 4 policy-path hits are allowlisted. The 4 unallowlisted hits survive because their path is a different path, even though the bytes are identical.

## Digest-only identities

The identity digest is the sha256 of the compact JSON `[path,line,class,line_sha256]`, using `separators=(',',':')`. Multiset digests are the sha256 of the sorted identity digests joined with `\n`.

Exact policy-path hits (4):
- `12d9a6dbab471a6e8266cf343fa1d393a16c774f7f87118e4dce28a040cdc78a`
- `851e3d63040b64d8da5db85632c3b00019ff26be570de0c247abf5aff82b4573`
- `ad0e0edff5defd2a5bb21e9d636063c3304cb9b9fb5e4a220c1def0ce90b0e7e`
- `daf2a1b96cfb45a737ca5ec33845179b3a0b5f9bd7b883cf72b1ff5870772f43`

Unallowlisted hits on the nested copy (4):
- `6bf2ed98d905b330117f8669df1ba41b370e0dc62097f94dbbc978a45c7e41e8`
- `8e1fb22d709d7fd38410ad9503a29829dab8b17e2232e4fb51ffac1ae00b769e`
- `ef3e414f66ea3ba54cf07a11bf17ccdeece7670e47360f9cab9c77478904513a`
- `f845baef6168cbba48fbffa7041a326b31e7f019dc516e899c8c1b1a011a7a6c`

Non-author residual (5):
- `11c9a1596783056f6a1126ba000785699c859735243e0222dc1a1a34b97791cc`
- `4716019932415fdc7b9e4d7da61affb2a9f0c2987005a7214391f7654d2f18be`
- `6a8a60db57594d9a7152de5428c73cf32ec0d3ba6de13a4967174d307d71cfcf`
- `b922918d6149558a658510adf6a3a6305864d2a946808656fe5625544164ef59`
- `de3e7716c51d7d592510b0a0cdd531411544d53209ef1bd158a268dc059b6e53`

Multiset digests:
- raw (95): `f32d12cc3e1757eb9340c0f9222dc4f94fd8edb80fa04c383eab63939d5ff7c9`
- allowlisted (86): `ea9aeb12d0efbd31a1950acd3d3b73a06b2c52e3f6a9c939a90bab97fd9b90ca`
- unallowlisted (4): `721b2d5014cfed3d4dae405ecec5cc4b413c9b601a727f5ba3de0eb076e0ad80`
- policy-path (4): `27f5af96e9f6ade35b9d3ffaf81b824d5ad97c623d141683530b10752450ff97`
- scanner-compatible (91): `ece92e524e3b7735a85da63f8e9eb0a5bce6acd5ea0990af4c8a4dfd4f8ea60e`

## Input-tree binding (observed)

- Policy blob sha256 `db06e981…3128` at the measured rev equals the value at the entering branch `77a5bbe8…`.
- Allowlist blob sha256 `f46c78ecad4c6d31fa9ac0ba0cfd6c72eb9137ab6b58ab4baf4239d11ea0c63b` (28354 bytes) at the measured rev equals the value at the entering branch.
- So for this receipt, R15 (changed policy bytes) and R16 (changed allowlist bytes) would not trip. Both inputs are mode `100644` blobs, not symlinks.

## Implications for L1 / code seats (inference)

1. The contract's "raw95 incl 5 policy" premise is wrong by identity. A tool that asserts `policy_excluded=5` or `scanner_total=90` against the real retained receipt would be checking count subtraction, which is exactly the trap the contract's root lesson forbids. Expected real-receipt values should be policy_excluded=4, scanner_total=91, non_author=5, raw_unallowlisted=4, scanner_unallowlisted=4. The synthetic R03 fixture (5/1/4) is separate and unaffected.
2. Trap worth a mutant: if the policy exclusion is done by content (blob hash or line digest) instead of exact path, it removes all 8 hits on the policy bytes. That drops scanner_unallowlisted to 0 and falsely "cleans" the 4 retained unallowlisted hits. The exclusion must be by exact path only.
3. The receipt's hit lists are sorted by (path, line, class, digest) and contain no duplicates. A dropped, injected or altered hit (R05–R09) is detectable from identity multisets alone.

## Remaining unknowns

- I did not run an independent regex recomputation over the measured tree. Every count above restates the receipt's own lists and checks that they are internally consistent. Whether the true tree yields the same 95 is for the new tool or L1 to measure.
- Why the round-20 falsify run committed a nested copy of the policy, and its historical disposition, were not investigated (out of scope).
- Whether the 4 nested-copy hits should become allowlisted is a policy decision, not this seat's. They remain unallowlisted, and privacy_clearance=false.
