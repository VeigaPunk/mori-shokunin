# CriticPopulation — raw vs policy-excluded population equality (round 22)

Seat `MoriR22.CriticPopulation`, critic, read-only. Scope: whether the round-22 reconciliation compares populations by exact hit identity multisets rather than scalar totals, under duplicate, relocation and changed-line cases.

Inputs examined:
- `contract.md` (df880b4) and `denominator-correction.md`, `frozen/requirements-v2.json`, `frozen/fixture-builder-v2.py` and `oracle-reconcile-v2.py` (all from e2f549b).
- The untracked candidate `tools/mori-retention-reconcile.py`, SHA-256 `8600850fd2e3d07aabe528028835dcd9fc1a76220dc8c68351de2809c97b7a9a`.
- The retained receipts `round-21/evidence/final/retention-floor{,-entering}.json`.

No tests, builds, SUT runs, oracle runs, linters or formatters were executed. No tools were installed.

## What was exercised

I ran read-only metadata recounts. Each one used `git -C <lane> ls-tree`/`cat-file`, or parsed the receipt JSON, and printed only counts, paths, booleans and object IDs. No line text was printed.

1. **Exact identity recount of the measured tree.** I used an independent stdlib re-scan of every tracked blob at `9fb1f91` (gate split semantics, with the regexes taken from the committed policy blob). The result is 95 hits, multiset-equal to `retention-floor.json` `hits` on (path, line, class, line_sha256): 0 extra, 0 missing.
2. **Partition by identity.** Raw 95 = 86 allowlisted + 4 unallowlisted + 5 non-author (the hits matching `non_author_paths_glob`). Allowlisted ∩ non-author = ∅, so `raw == un ⊎ al ⊎ na` holds as multisets. Other figures:
   - The policy path `.ufo/waves/round-18/frozen/c1-policy.json` has 4 hits, and all 4 are allowlisted.
   - Raw minus the policy path is 91, not 90.
   - Raw minus non-author is 90.
   - This independently confirms `denominator-correction.md`: the "5" was the non-author count, not hits in the policy source file.
3. **Relocation in the real data.** `.ufo/waves/round-20/falsify/NoHarmRun/rg/.ufo/waves/round-18/frozen/c1-policy.json` is the same blob as the policy file (`8bf285bd…`) at every revision checked (`e9f340c`, `9fb1f91`, `77a5bbe`, `306e06e`).
   - Its 4 hits equal the policy file's 4 hits as a (line, class, sha) multiset.
   - Those 4 hits are exactly the 4 retained unallowlisted hits.
   - They count as unallowlisted only because the allowlist key includes the path.
4. **Scalar coincidence in the real data.** Raw minus policy path minus non-author = 86, which equals the allowlisted count. As identity multisets the two differ: the policy file's 4 allowlisted hits are swapped for the copy's 4 unallowlisted hits.
5. **Wrong-tree equality in the real data.**
   - In `retention-floor-entering.json`, the wrapper says `measured_revision=9fb1f91`, but `argv --rev` and `stdout.commit` are `e9f340c`.
   - The diff between those two trees is 120 files.
   - Re-scanning `9fb1f91` still gives a population identity-equal to that receipt's `hits`.
   - It is the only r21 command receipt where the wrapper revision and the scanned revision differ.
6. **Parity surface present at `9fb1f91`.**
   - 4 symlink blobs, none with hits.
   - 337 NUL blobs.
   - 3 blobs containing CR.
   - 0 non-UTF-8 or control-character paths.
   - 0 blobs where `str.splitlines()` would change any hit identity compared with `split("\n")`.
   - No policy class matches an empty string or a lone CR.
   - 15 lines carry more than one class (46 hits), and there are 60 distinct line digests among the 95 hits.

## Verdict on the candidate (by inspection only; not executed)

The candidate keeps the path in every identity. It compares `hits`, `allowlisted_hits` and `unallowlisted_hits` as `Counter`s over the full 4-tuple. It caches parse results by blob object ID but re-attaches each path, so the policy file and its copy stay distinct, and it scans symlink blobs as the gate does.

It also refuses the wrong-tree case in finding 5: `argv --rev` and `stdout.commit` must both equal `measured_revision`, otherwise the result is `receipt_revision_conflict`, exit 2.

[INFERENCE] On the real `retention-floor.json` it should produce:

| Field | Value |
| --- | --- |
| `raw_total` | 95 |
| `policy_excluded` | 5 |
| `scanner_total` | 90 |
| `raw_unallowlisted` | 4 |
| `scanner_unallowlisted` | 4 |
| `allowlisted` | 86 |
| `retention_state` | red |
| exit | 0 (RETENTION_RECONCILED) |

On `retention-floor-entering.json` it should exit 2.

No population-equality defect was found in the candidate's computation. The defects are in the frozen falsifiers: the 24-arm oracle cannot tell this candidate apart from several path-blind or partition-blind mutants.

## Counterexamples

### P1 — Path-blind identity comparison survives all 24 arms
- **Counterexample:** a mutant that compares `Counter((line, class, sha))` without the path.
  - No fixture variant changes only a hit's path.
  - R05 changes the count, R06 injects a zeros digest, and R07/R08/R09 change the digest, line or class.
  - A receipt that relocates a hit (same line, class and sha under a different path) keeps every total and every path-free identity, so the mutant reconciles it.
- **Evidence:** in `fixture-builder-v2.py`, mutations touch only `result['hits'][0]` fields other than `path`. Finding 3 shows that path is the only thing separating the real red from an allowlisted hit.
- **Axes:** calibration and depth.
- **Smallest safe correction:** add one variant that relocates only the path of one `hits` entry (for example `unallowed.txt` to `moved.txt`, keeping line, class and sha), with expected exit 1 and RETENTION_RECONCILIATION_MISMATCH.

### P2 — Partition lists are never mutated
- **Counterexample:** a mutant that stops comparing `allowlisted_hits` and `unallowlisted_hits` (keeping only `hits` plus `metric`) passes all 24 arms. It would accept a receipt whose `unallowlisted_hits` names a different identity at the same count.
- **Evidence:** no oracle variant edits either partition list, `forbidden_allowlist` or `warnings`. R11 is honest-only.
- **Axes:** calibration, because this is exactly "population equality by scalar" inside the partitions.
- **Smallest safe correction:** two variants, each with expected exit 1:
  - swap one `unallowlisted_hits` entry for an allowlisted hit's identity, keeping `metric` unchanged;
  - alter only the `line` of one `allowlisted_hits` entry.

### P3 — Allowlist key collapsing across paths is invisible to the synthetic suite
- **Counterexample:** a mutant that keys allowlist matching on (class, sha) instead of (path, class, sha) passes all 24 arms, because the fixture has no line content repeated across two paths.
  - On real data the same mutant would allowlist the 4 copy hits.
  - The recomputed metric would drop to 0 and the run would report MISMATCH.
  - So only an L1 run on the real input would catch it, and that run is not one of the frozen arms.
  - A content- or blob-ID-based "policy source" exclusion would likewise erase the real red: scanner_unallowlisted would go from 4 to 0, a false clean.
- **Evidence:** findings 3 and 4.
- **Axes:** calibration (R02 and R11 intent), depth.
- **Smallest safe correction:** add a byte-identical copy of `allowed.txt` at a second path to the valid fixture, with no allowlist row for it. Expected: those hits are unallowlisted, raw and scanner counts rise by 2, and `scanner_hits` contains both paths. This also requires re-deriving the frozen totals (see the tradeoff note below).

### P4 — Overlap between allowlisted and non-author hits is never exercised
- **Counterexample:** under gate semantics, `allowlisted_hits` includes non-author hits that match a row, and `non_author` still counts them.
  - A mutant that builds `allowed` from scanner hits only, or any scalar `raw = al + un + na` check, survives all arms.
  - Both the fixture and the real data have an empty overlap, and the scalar sum holds only because of that.
- **Evidence:** `retention-gate.py:261` (allowed is taken from all hits) versus the unallowlisted list at `:262-266`; my recount shows an empty overlap. `denominator-correction.md` itself asks to "preserve overlapping allowlisted/non-author semantics", yet no arm checks it.
- **Axes:** calibration, depth.
- **Smallest safe correction:** add a variant with an allowlist row for the `non-author.txt` hit. Expected: `allowlisted` 4, `non_author` 1, raw 5, exit 0 for the honest receipt.

### P5 — The non-author count has no lie arm, and the exclusion glob has no nesting arm
- **Lie arm:** a mutant that drops the `non_author` comparison survives, because R12 checks only the tool's own output and no variant falsifies the receipt's `non_author`.
- **Nesting arm:**
  - Gate parity depends on `fnmatch`, where `*` crosses `/`.
  - A `PurePath.match` mutant, which anchors on the right, would classify `sub/non-author.txt` as non-author.
  - The fixture has only a top-level path, and no real hit path exercises either difference.
- **Axes:** calibration and freshness (parity drift).
- **Smallest safe correction:** two arms:
  - a receipt `non_author` lie (1 → 0), expected exit 1;
  - a hit at `sub/non-author.txt`, expected to stay in the scanner population.

### P6 — The real wrong-tree shape is guarded only incidentally
- **Counterexample:** the shape in finding 5 (wrapper revision differs from the scanned revision, but the populations are identity-equal) would silently reconcile under any tool that scans the wrapper's `measured_revision`.
  - The candidate rejects it through `receipt_revision_conflict`.
  - But `invalid-revision` and `diverged` fail earlier, on resolve or ancestry, so no arm holds this guard in place.
- **Axes:** calibration (false provenance).
- **Smallest safe correction:** add a variant where `measured_revision` is a child commit that adds a non-matching file, while `argv --rev` and `commit` stay at the parent. Expected exit 2.

## Tradeoffs for the canonical judge (not fixable defects)

- **T1 — `raw_unallowlisted` and `scanner_unallowlisted` are the same number.** The candidate sets both to `len(unallowed)`, and gate unallowlisted is already computed in scanner scope. R02 therefore checks one value twice. A raw-scope count (raw minus allowlisted, non-author included) would be 9 on real data and 2 on the fixture, which conflicts with the frozen 1/1 and with the correction's figure of 4. Either state in the output that the two are equal by definition, or freeze a distinct raw-scope definition. Do not present them as two measurements.
- **T2 — Allowlist bytes are not bound to the receipt.** The receipt binds only `policy_sha256`. The gate read `--allowlist` from an absolute worktree path, and the receipt carries no digest for it. `inputs_sha256.allowlist` is the committed blob, so allowlist agreement shows that the partition was reproduced, not which bytes the gate loaded. The smallest honest correction is a label (for example `allowlist_binding: partition_reproduced`) or a check that the argv path is `argv --repo` + `/` + the REPO_REL input.
- **T3 — Non-UTF-8 paths fail closed.** The candidate decodes tree paths strictly and exits 2, where the gate decodes with `errors=replace`. This also makes replacement-collision duplicates impossible, so `normalize_hits` on the recomputation can never fire as `duplicate_receipt_hit`. That is an acceptable fail-closed divergence, but its error code would misattribute a recomputation duplicate as a receipt defect.
- **Fixture totals in P3.** Adding the copy changes the frozen 5/1/4 totals. If R03's totals must stay frozen, put the copy in a separate `relocated` variant instead.

## Bottom line

On real data, population equality holds by exact identity: 95 = 86 + 4 + 5, and the 4 red hits are the relocated policy copy. The corrected semantics match that. The frozen oracle, though, would also accept path-blind, partition-list-blind, overlap-blind and content-keyed mutants (P1–P5). Agreement on the 24 arms therefore does not yet establish identity-level population agreement.

None of this is privacy clearance: `privacy_clearance=false`, the original permission control remains RED 11/12, and baseline acceptance stays blocked.
