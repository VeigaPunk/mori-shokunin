# C1 security and privacy review

## Verdict

**Yes: the frozen population commits an unsalted SHA-256 for every matching line, creating an offline confirmation/dictionary oracle for any low-entropy or guessable private line.** The population and reference enumerator do not include matched plaintext. A public salt would not fix targeted guessing; omit per-line content digests, including from allowlists and gate output, before implementation.

The no-history-rewrite boundary is correctly routed to operator/kagi in the contract, but that routing is ownership, not containment: old blobs remain retrievable to readers with access to the retained commit graph. No history rewrite or exposure response was attempted here.

## Scope and evidence

Reviewed the frozen inputs and contract at requirement freeze `29b0dc79e193b9d67845e39850a091a84bad66bd`, then checked committed round-18 paths at current `HEAD` `11db4df00bca48f49fada47a2a19b371e86f8778`. The current tree has 15 round-18 paths; the freeze tree had 7. The C1 gate source is absent from current `HEAD` (`git ls-tree` returned no path), so statements about its output below describe the frozen design/reference, not an implemented tool. No external URLs were consulted.

C1's population summary is 119 hits, 40 hits in must-redact paths, 3 non-author hits, and 116 in the before metric (`.ufo/waves/round-18/frozen/c1-population.json:5-10`). Its hit records span lines 12-727. Aggregated by class from those records: R1=22, R2=30, R3=9, R4=3, R5=4, R6=6, R7=13, R8=11, R9=21. The policy defines those classes at `frozen/c1-policy.json:6-15` and the must-redact/allowlist rules and recall limitation at `:17-29`.

The reference enumerator decodes each non-binary blob line and appends `path`, `line`, `class`, and `line_sha256`, computed as plain SHA-256 of the UTF-8 re-encoded complete line; it adds no salt or secret (`frozen/c1-population-cmd.py:30-42`). It serializes these records to JSON (`:45-54`). The contract says the tools never print matched private text and output only path/line/class/SHA-256 (`contract.md:47-53`); allowlist rows also require `line_sha256` (`:55-61`). Thus **the planned output does not print matched text**, but does expose the digest and correlating metadata. The C1 policy itself explicitly calls its regexes a recall floor, not a privacy proof (`frozen/c1-policy.json:29`).

Committed-file SHA-256 provenance (whole files, not any per-line digest):

| Lane-relative file | SHA-256 |
|---|---|
| `.ufo/waves/round-18/contract.md` | `6986c9338b4c38f8b66831526d4427c04c589226adc43e0240ff34ce08fcf11b` |
| `.ufo/waves/round-18/frozen/c1-policy.json` | `db06e9810bbfd243fb0a753a46960573df39083ea90174ce463cf2a0ab523128` |
| `.ufo/waves/round-18/frozen/c1-population-cmd.py` | `9e896f7a845c749bf306d7ce11d25145283580d613d3427337037c230d70733e` |
| `.ufo/waves/round-18/frozen/c1-population.json` | `392c5ab49df3b019bab57ead013a4066cbdb9ad4e06bc7abb2f0166a97e251a2` |
| `.ufo/waves/round-18/frozen/c2-register.json` | `a654f3802d62126a3e93fee275e3b16e9cd8ac1da28d6994ebd1ffe304609efb` |
| `.ufo/waves/round-18/frozen/c3-ledger-format.json` | `323ba0f38cf73adbe0998fe00f5310aee101415484d864c21a923b020d23f876` |

The C1 files have the same committed blob identities at freeze and current `HEAD`. No raw `line_sha256` value is reproduced in this report.

## Findings

### HIGH — Per-line hashes enable low-entropy disclosure

**Exploit path:** a reader takes a row's source location, class, and unsalted digest, enumerates plausible complete line candidates (or likely values in a known line template), computes SHA-256, and tests for a match. A short status, small choice set, or otherwise guessable value can be recovered or confirmed cheaply. Path/line/class metadata and the class regex narrow candidate space. This is an offline attack; no access to the gate or its host is required. No cracking attempt was made.

**Impact:** the digest is not encryption. It can reveal/confirm private line contents even though the JSON contains no plaintext. It also persists as a stable correlator after a later working-tree redaction. The same risk exists in future allowlist entries because their schema includes the digest. The summary's 40 must-redact-path hits make the population especially inappropriate as a privacy-safe committed snapshot; this count does not establish that all 40 preimages are private values.

**Smallest remediation:** before implementing C1, remove `line_sha256` from the frozen population, allowlist schema, expected-population comparison, and gate output. Compare structural hit identities (`path`, `line`, `class`) or publish only aggregate counts; keep content-derived values out of committed output. Do **not** substitute a public salt: a targeted guesser can hash each candidate with that salt. A secret-key MAC would require an unavailable non-committed key and would defeat public reproducibility, so it is not the minimal design. Keep the no-matched-text output rule as an explicit acceptance test.

### MEDIUM — Allowlist `reason` is free-form output risk

**Evidence:** the allowlist schema includes a free-form `reason` alongside the rule code (`contract.md:58-60`); the policy constrains which hits qualify but does not constrain the reason's character set or guarantee that implementations will not echo it (`frozen/c1-policy.json:27`).

**Exploit path / impact [INFERENCE]:** an author could paste source-derived private text into a reason; an implementation that serializes allowlist rows or stale-row findings could then disclose it, despite never printing the matched line itself. No current C1 implementation exists to establish that it echoes reasons.

**Smallest remediation:** make reasons fixed enum/code values, or keep free-form reasons out of tool output and reject reasons that contain copied source content. Test the output projection using a synthetic marker without printing the marker.

### MEDIUM — A zero metric is not a privacy proof

**Evidence:** the frozen policy says unclassified private context is discoverable only through a separate reading sweep and is outside the metric (`frozen/c1-policy.json:27-29`); NUL-containing blobs are skipped (`:5`).

**Impact:** a clean C1 count only means no unallowlisted match among these text regex classes at the measured revision. It cannot support a claim that all private context is absent.

**Smallest remediation:** retain the separately scoped content review as a separate required gate and label C1 results narrowly; do not turn count zero into a whole-repository privacy claim.

### HIGH residual exposure — Existing history remains in scope for operator/kagi

**Evidence:** the contract explicitly says history is not rewritten and the exposure assessment is operator/kagi-owned (`contract.md:11-18`); it records 116 before-metric hits and 40 routed-file hits at the base (`:24-29`). The frozen population is a later committed artifact describing those base-revision hits.

**Impact:** if the pre-redaction blobs remain reachable, a reader with repository-history access can retrieve their contents directly; removing the digest from a future commit would not erase prior objects or copies. Repository visibility, clones, mirrors, and backups were not assessed here.

**Routing answer:** **yes**, ownership is explicitly routed to operator/kagi and this lane must not rewrite history. That is adequate routing, not sufficient exposure response. Operator/kagi should decide the reachability/exposure assessment and any external notification, revocation, or history-remediation action. Do not infer that a zero post-redaction scan closes historical exposure.

## Other current round-18 artifacts

A read-only marker scan of all committed `.ufo/waves/round-18` paths found no R1 or R3 markers. R7/R8/R9 matches were only the C1 policy's own class definitions. R2/R4/R5/R6 marker matches in the other wave artifacts were located in context/task/prompt fields, not in standalone private-value fields: dispatch at `wave1-dispatch.json:445,550,555,560`, plan at `wave1-plan.json:4,555,560,565`, and spec at `wave1-spec.json:5,110,115,120`. **[INFERENCE]** These are copied scope/instruction references rather than private values; the marker scan cannot prove absence of unmarked content. The wave response and other payload strings were not reproduced or manually quoted. The C1 regex floor means this is not an exhaustive semantic privacy audit of every payload.

## Commands and exit codes

All reads were read-only. No tool was installed; no URL was accessed.

- `git -C <lane> log -1 --format=%H` — exit 0; current tip recorded above.
- `git -C <lane> ls-tree -r --name-only 29b0dc79e193b9d67845e39850a091a84bad66bd .ufo/waves/round-18` — exit 0; 7 paths.
- `git -C <lane> ls-tree -r --name-only HEAD .ufo/waves/round-18` — exit 0; 15 paths.
- `git -C <lane> ls-tree -r --name-only HEAD tools/mori-retention-gate.py` — exit 0, no path returned.
- `git -C <lane> grep -I -n -E <frozen C1 marker patterns> HEAD -- .ufo/waves/round-18 | cut -d: -f2,3` — exit 0; only path/line locations were emitted. The per-class `git grep -I -c` checks returned exit 1 for R1 and R3 (no matches), exit 0 for classes with matches; no matched source text was emitted.
- `set -o pipefail; git -C <lane> show <revision>:<file> | sha256sum` for each file in the provenance table — exit 0.
