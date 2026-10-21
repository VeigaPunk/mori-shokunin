# HistoryRetention — Q51 / Q68 evidence-copy audit

## Scope and verdict

Reviewed `corpus/QUALITY.md:154-160,251-278`, `.ufo/waves/round-21/contract.md:7,13-15,27`, the five files under `.ufo/waves/round-21/evidence/`, and the relevant findings in `.ufo/waves/round-21/build/ConnectSouji.md:33-59`. No live census, pin, gate, build, or source edit was performed.

**Q51: not demonstrated.** The copies are scoped to the two disappeared wave identities, but some retain raw path/commit metadata rather than only a summary/count/hash. No Q51 retention-gate result (zero unallowlisted hits, with must-redact files excluded from allowlisting) was present in the round-21 build/evidence material searched. The source classification needed to call the raw metadata a definitive privacy violation is not established here.

**Q68: partial digest trail, not a complete explicit mapping.** Recomputed digests match the recorded source/projection/copy digests below, and I found no observed substitution of a sanitized-copy digest for the original baseline digest. The mapping does not explicitly record all three required facts—entering-revision digest, present digest, and bound status—for each artifact; no rerun or pin was performed, so the original-revision rerun condition is untested.

## Observed copy contents and minimization

- `.ufo/waves/round-21/evidence/cleanup-receipts.tsv:1-18` retains 18 full path/status rows for the two target waves. `build/ConnectSouji.md:36-38,54-59` identifies the upstream approval list as 96 rows and the retained file as an 18-row projection. This is materially scoped down, but it remains copied row content, not just the count and digest.
- `.ufo/waves/round-21/evidence/removal-metadata.txt:1-36` retains full commit metadata/message and the 18 deletion paths. `.ufo/waves/round-21/evidence/historical-provenance.json:7-21,23-40` also retains absolute command paths and actor identity strings alongside source revisions and hashes.
- `.ufo/waves/round-21/evidence/census-before.json` is a summary object (exit code, row count, warning IDs and observation), but its recorded command includes absolute tool/root paths. The unchanged baseline `corpus/evidence/baseline-r10-20261015T2231Z.json:1-12` includes census command/path and threshold metadata. `.ufo/waves/round-21/evidence/source-spotcheck.json:2-11` is a short decision/reason summary rather than a copied source passage.
- These raw fields exceed the minimal visible C1 accounting need (per-wave identity plus baseline/deletion/cleanup provenance and hashes). Whether any such field is classified private, an operator configuration value, or otherwise unallowlisted is unresolved; the hashes do not redact accompanying contents. The Q51 search over the round-21 build/evidence directories for `unallowlisted`, `must-redact`, `retention gate`, `allowlist row`, and `Q51` returned no matches, so these copies cannot be declared Q51-clean from this material.

## Digest/provenance checks

`historical-provenance.json:3-5,19-20,31-40` records the baseline revision/hash, deletion revision/metadata hash, and cleanup source revision/blob hash plus projection hash. `corpus/evidence/loss-accounting-r21.json:5-23,26-45` retains both observations as `unresolved`, points to the committed baseline and round-21 evidence copies, and has `independent_disposition: null` for each.

Observed SHA-256 results:

| Artifact | Original/source reference and digest | Present copy digest | Result |
|---|---|---|---|
| Baseline | `e9f340ce986f82a60baad1b8e5ead655ab818a1c`; `0993b23505deab2aeb05b2309bdf7dd6eaad2b82f27852491352511aa9670478` | Current baseline file: same `0993b23505deab2aeb05b2309bdf7dd6eaad2b82f27852491352511aa9670478` | Match; baseline bytes remain the original, not a sanitized replacement. |
| Deletion metadata | `e20f4fa3fd3fc9550641af38da3eddcf3d35f528`; SHA-256 of the recorded `git show --format=fuller --name-status` output: `4276625be64ab1943bb5781dab7a3d9e8c912bdb48ea562870f20b70b753263e` | `removal-metadata.txt` at copy revision `a8442a018aa9c51b21b92c3ce3b17736317375b1`: same `4276625be64ab1943bb5781dab7a3d9e8c912bdb48ea562870f20b70b753263e` | Match for the metadata projection; this is not a SHA-256 of the deleted wave files. |
| Cleanup receipt | Source approval-list blob at `2f303dc6e30d7650e1e513e3cbad75412efdc353`: `550da61f5da587b4d09b826259f49978c826f3cbe2ed8440b86c413251d45715` | 18-row `cleanup-receipts.tsv` at copy revision `a8442a018aa9c51b21b92c3ce3b17736317375b1`: `46f84c3a60ac701ec7d0c16523e5bbfa999be3999cb61029be8fba50785970a7` | Source and projection hashes both match their recorded values; they are distinct digests. |

The loss-accounting references correctly identify `a844…` as the revision of the committed own-lane copies, while the provenance note keeps source revisions distinct from projection revisions (`historical-provenance.json:40`). However, the files do not carry explicit `entering_revision_digest`, `present_digest`, and `bound` fields per artifact. For the baseline a single hash matches both the entry-revision and current bytes, but that equality is established by this audit rather than represented as two mapped values. For deletion metadata the stored digest is of the `git show` output, with the source commit ID but no separate source-content digest. These are partial provenance controls, not a complete Q68 mapping.

## C1 boundary and remaining unknowns

Both required identities remain present in `loss-accounting-r21.json` as unresolved with null independent disposition; `historical-provenance.json:38-40` says settlement is unknown. This supports retaining the evidence-loss blocker, not settling either wave. QUALITY Q69 (`corpus/QUALITY.md:263-275`) distinguishes same-identity cleanup/recoverability from independent per-wave disposition. No pin or disposition was inferred here.

Remaining unknowns: (1) whether the copied paths/actor metadata are classified as private or unallowlisted by the active Q51 policy; (2) the measured-revision Q51 gate result; and (3) explicit per-artifact Q68 bound/entering/present mapping plus any original-revision rerun evidence. QUALITY `:277-278` and the round-21 contract `:27` already identify Q68 as qualified debt; this audit does not claim it was repaired.

**Confidence:** High on the inspected contents, references, and digest matches; medium on minimization severity because the private/unallowlisted classification and measured retention-gate output are absent.