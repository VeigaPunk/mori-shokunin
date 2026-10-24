# F1DigestDrift — static falsification of C1 case `digest_drift`

Seat: MoriR19Recovery.F1DigestDrift (leaf reviewer). Read-only; nothing executed.
Reviewed working-tree state pinned by SHA-256 (concurrent integration was landing during review):

- `tools/mori-round19-regressions.py` — 1139 lines, sha256 `9a21606e0a4f92fa77b6d8df1a55d99065be197504d5b744fbcf3262450339f6`
- `tools/mori-content-review.py` — 493 lines, sha256 `fa88a6b034d1cdb955fc9db1c0aa38efd44bcc9495d6086873b3ebd6476b29cc`
- HEAD at observation: `7fa136f9d03b9c27667ab50487910ab299e617f2` (neither the wave2 integrated commit `367927c56eb1a00613e1fed65e5c47245fd570b9` nor base `b3602869…`). Anchor re-pin against the actually integrated commit is L1's verification step; the file mutated at least twice during this review (1152→1159→1139 lines) before stabilizing.

Oracle (frozen, `.ufo/waves/round-19/frozen/expected.json`): `c1_cases.digest_drift = 1`, `c1_required_finding.digest_drift = "CONTENT_REVIEW_STALE"`.

## Verdict trace (no counterexample on the primary claim)

Static trace of the single digest_drift input through actual code:

1. Fixture: `tools/mori-round19-regressions.py:339-340` replaces the first row's `blob_sha256` with the digest of different bytes; second row untouched; population pin set to the population file digest (`:352-357`), so no exit-2 pin confusion.
2. Gate: `tools/mori-content-review.py:326-327` — row digest ≠ sha256 of `git show` blob bytes at REV → per-path `CONTENT_REVIEW_STALE`. `:35-39` STALE ∈ FAIL_CODES; `:192-196` → status `failed`, exit 1. Matches frozen exit 1 + required finding.
3. Finding isolation: drifted row only; second row intact → no INCOMPLETE (`:331-333` both rows present), no INVALID path (row fields exactly the five allowed, valid decision/basis, `:288-306`), no POPULATION_PIN. Exactly one finding, on the drift path, matching the harness's path expectation (`mori-round19-regressions.py:321`).
4. Harness verification of this case: exit code (`:384-386`), receipt status/exit coherence (`:404-406`), path-scoped required finding (`:407-411` → `c1_code_present` `:267-279`), receipt metadata hashes vs actually loaded bytes (`:396-403` → `c1_output_valid` `:243-275`; tool self-digest via `read_script_digest` vs `sha256_file` of the executed regular file — `run_tool` `:182-201` rejects symlinks, so the hashed and executed bytes coincide).
5. False-clean check: the sole skip condition for the drift comparison is a failed blob read (`tools/mori-content-review.py:326`, `path_value in blob_digests`), which instead yields PATH_UNAVAILABLE → exit 2. No silent pass path exists for a drifted row whose population path exists at REV. Digest comparison lowercases both sides (`:326`), so textual case alone is not drift — consistent with the frozen case, which drifts the value.
6. Before/after divergence: none. The C1 path is mode-independent; `--mode` gates only C2 bound invocations (`mori-round19-regressions.py:1040-1060`). Both modes verify against the same oracle bytes pinned to the freeze commit (`expected_from_pinned_commit` `:823-863` git-show comparison, plus pre/post stability hashing `:971-974`, `:1083-1095`).
7. Leak check: gate receipt carries only schema/status/exit/metadata-digests/counts/findings{code,path} (`tools/mori-content-review.py:140-190`, `emit` `:339-342`); reasons and blob contents are never copied into output. Harness scans stdout+stderr for reasons, blob contents, and the sentinel (`mori-round19-regressions.py:380-384`); process receipts store only lengths and digests (`:203-215`).
8. Cross-consistency: the gate's built-in selftest independently encodes digest_drift → exit 1 + STALE (`tools/mori-content-review.py:424`), agreeing with the harness fixture and the frozen oracle.

Primary claim holds in the reviewed state: expected exit 1, stable path-level `CONTENT_REVIEW_STALE`, metadata complete, no value leak.

## Findings

- **F1 [Medium — harness false-pass channel, latent]** `tools/mori-round19-regressions.py:268-270` — `c1_code_present` returns True when a top-level `finding_id` equals the required code, bypassing the path-scoped findings scan and ignoring the expected path (`:318-324`). No receipt field named `finding_id` exists in the contract schema, and `c1_output_valid` (`:243-275`) does not forbid extra top-level keys, so a future gate emitting `finding_id` with an empty `findings` list would pass the digest_drift oracle check without any path-level finding — contradicting the contract's path-level-finding-codes requirement. Delivered gate never emits that field, so no live divergence today. Required correction: delete the short-circuit; keep only the path-scoped scan (optionally also reject unknown top-level receipt keys).
- **F2 [Low — unverified receipt counts]** `tools/mori-round19-regressions.py:258-263` — `c1_output_valid` requires the four count keys to be non-negative ints but never cross-checks `counts["findings"]` against `len(findings)` (nor the finding_codes sum), although the gate derives both from the same list (`tools/mori-content-review.py:180-186`). A receipt with lying counts passes receipt-fields. Required correction: assert `counts["findings"] == len(findings)` inside `c1_output_valid`.
- **F3 [Info — fixture/gate coupling]** `tools/mori-round19-regressions.py:293-298` — the population fixture carries an extra non-contract key; the gate tolerates unknown population keys (`tools/mori-content-review.py:247-249` checks only schema + paths list), asymmetric with rows' exact-field rule (`:307`). Contract-compliant, but if the gate ever tightens P to exact keys, every C1 case including digest_drift flips to exit 2. No action required now.

## Residual risk and verification gaps

- Anchors are pinned to the SHA-256s above; the tree changed during review and HEAD advanced beyond both cited round commits. L1 must re-verify anchors against the commit actually integrated (read-only `git -C … diff` between `367927c…` and the landing tip restricted to these two files) before relying on line numbers.
- Everything above is static derivation; no execution, tests, or smokes were run (restriction). Runtime exit/status behavior awaits L1's single post-settle run.
- Only26 of194 C1 population paths have delivered reviews; this report says nothing about coverage of the others and claims no clean review coverage from missing work.
