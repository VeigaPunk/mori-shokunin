# Round 22 bool-line fixture — static audit

## Scope and method

Static review only; no fixture/oracle/SUT execution and no production edits. Read the effective denominator correction before the v2 fixture, oracle, requirements and current shipping reconciler. The v2 requirement pins the builder and oracle SHA-256 values; read-only checksum comparison matched both frozen values. No `lsp` device is present in the available tool inventory, so the source trace below is textual, not LSP semantic evidence.

## Findings

### The bool-line target path has a distinct internal error, but R18 does not assert it

- In `tools/mori-retention-reconcile.py`, `integer()` accepts only `type(value) is int`; `normalize_hits()` applies it to each `line` and raises `Invalid('receipt_hit_type')` for a JSON boolean. `check()` normalizes `hits` before the other receipt hit lists and before identity/counter comparison. `main()` converts that `Invalid` into exit 2, `RETENTION_RECONCILIATION_SETUP`, `error='receipt_hit_type'`, `receipt_match=false`, and `privacy_clearance=false`. **Static conclusion (high confidence):** if the bool-line fixture reaches this validation, the SUT's intended setup reason is specifically the line-type rejection, not an identity mismatch.
- `oracle-reconcile-v2.py` records R18 with only exit-code 2, `finding_id == RETENTION_RECONCILIATION_SETUP`, and empty stderr. It never checks the returned `error` token, `receipt_match`, privacy type/value, or fixture mutation delta. Thus **the oracle cannot distinguish the intended `receipt_hit_type` result from an unrelated setup error** that returns the same public finding and exit code. R01 is a separate generated valid fixture, not a paired valid control against this exact mutated fixture. The additional bool-metric arm is conjoined into R18 with the same generic setup checks, not a reason-specific assertion.
- The builder mutates only `result['hits'][0]['line']`; it does not mutate matching entries in `unallowlisted_hits` or `allowlisted_hits`. Consequently the receipt is also cross-list inconsistent. The current SUT rejects the first `hits` entry on type before it can classify that inconsistency, but R18 alone does not prove validation of boolean lines in the other two lists.

### Synthetic expected population is correct for the valid arm; bool-line contaminates returned expected identities

- The builder's measured tree contains five matching source identities: one in the policy blob, two distinct lines in `allowed.txt`, one in `unallowed.txt`, and one in `non-author.txt`; the NUL-containing blob is skipped. The frozen non-author glob matches the one `non-author.txt` identity. Therefore raw=5, excluded=1, scanner=4, with scanner identities equal to the other four raw identities. The allowlist rows include the required `rule='b'`; its path/class/digest key covers the two allowed lines. The valid receipt's three allowlisted hits and one unallowlisted hit agree with those identities. These claims follow from the fixture bytes' construction and the current SUT's glob/allowlist logic; they were not executed.
- The partition code in the builder uses literal path equality for `non-author.txt`, rather than evaluating the glob. This is correct for the frozen one-literal-pattern fixture, but is not a general independent glob oracle.
- Important provenance defect in the bool-line arm: `result['hits']` aliases the local `hits` list. Assigning `True` to the first receipt hit therefore also changes `hits`; the builder constructs `expected_scanner_hits` from that mutated list afterward. For this variant, that returned expected list contains the boolean line rather than the source-derived integer line. R18 does not consume this expected identity list, so it does not alter the R18 verdict; it is nevertheless not a truthful expected-source identity set for the malformed arm.

### Mutation and restoration provenance

- `make()` creates a new, non-existing repository per variant, commits the measured tree, applies the selected receipt mutation, then commits the receipt. `invoke()` caches by variant and uses a separate fixture directory for each variant; the valid R01 arm and bool-line R18 arm do not share a repository. The bool-line mutation is serialized into the committed receipt and does not mutate the shipping tool or the original measured tree.
- There is no restoration/rollback step or assertion that a mutant differs from a valid receipt in exactly one JSON value. Isolation by fresh per-variant repositories avoids a shared fixture to restore, but the oracle does not provide explicit restoration evidence. No generated fixture or restoration was executed/observed in this audit.

## Expected real partition and limits

The corrected contract says exclusion is identity-based membership in `non_author_paths_glob`, not policy-source-path exclusion. The frozen `expected-real.json` and correction state raw=95, excluded=5, scanner=90, allowlisted=86, scanner-unallowlisted=4, and privacy clearance false. `expected-real-identities.json` labels its digests a co-evolved transcription, not historical execution authentication. Those frozen real identity digests were not independently recomputed in this scoped bool-line audit; treat them as qualified metadata, not authenticated proof. No conclusion here changes the frozen values or clearance status.

## Verdict

**R18 is not reason-discriminating:** the SUT source has the expected specific type error, but the independent oracle accepts any generic setup failure with exit 2 and the setup finding. Also, the bool-line builder's shared-list alias corrupts the returned expected scanner identities for that variant, and no mutation-delta/restoration assertion exists. Synthetic valid-arm counts and partitions are statically consistent with v2 correction semantics. No test, build, selftest, or fixture run was performed.