# Mo61Reviewer06 — 12-row ledger quote spot-check

## Findings (severity order)

**High — four sampled, semantically correct `same` rows fail the frozen counter's extra minimum-word requirement.** `.ufo/waves/round-61/count-c2.py:137-139` rejects quotes below five whitespace-separated words; the frozen contract `contract.md:64-67` requires only ≤25 words and ≥8 distinct bytes. Sampled anchors `psi.c:1686`, `psi.c:1269-1270`, `psi.c:1257-1258`, and `psi.c:1711-1719` have 4, 4, 2, and 4 words respectively. Their complete pinned ranges have maximum single-line token counts 4, 4, 2, and 4: selecting another same-range single-line quote cannot satisfy that guard. The ledger parser consumes physical lines (`count-c2.py:119-122`), so a literal multiline quote cannot bridge this gap. This is a frozen predicate/contract mismatch, not evidence that the upstream anchors moved. No counter/contract changes proposed or applied.

**No quote-location or status defect found in the 12-row sample.** All twelve quotes are byte-present at their stated `same` anchor ranges, ≤25 words, ≥8 distinct bytes, and pairwise distinct. For each sampled range, the complete v7.2 and v7.3 line slices are byte-identical, independently establishing `same`, rather than merely finding the chosen quote somewhere in the file.

## Scope and axes

Axes: byte-location accuracy; status fidelity; quote size/uniqueness; frozen-gate compatibility; read-only evidence integrity.

Systematic sample: enumerate/deduplicate the counter's six-file pointer grammar in `corpus/knowledge/system-pressure-r24.md`, then select zero-based indices `[::4]`. This gives canonical ordinals **1,5,9,13,17,21,25,29,33,37,41,45**, twelve of 47 pointers. Starting at ordinal 4 would give only eleven, hence the explicitly stated phase.

Drafts reviewed: `.ufo/waves/round-61/w1/Mo61ScribePsi1.md:89-128` (41-row draft; sha256 `cbac1ad8accd5135fc306c2ded4d8ce98d886266abb3f0e34b3777eec6224330`), plus the verbatim cgroup row supplied directly by `Mo61ScribePsi2` for its report `.ufo/waves/round-61/w1/Mo61ScribePsi2.md` while that report was being written. The production ledger path was absent at inspection; this is a **draft** review, not a claim about landed data.

All paths below are relative to the lane `/home/vgpnk/Projects/shokunin/mori-shokunin`; source-line pointers in the table mean `corpus/evidence/sources-r61/<file>:<line>`. All actual filesystem accesses used absolute paths.

## Per-row verdicts

`PASS / short` means all assigned contract checks pass, but the frozen counter rejects its additional minimum-five-word check. `same ✓` means the entire original anchor range is byte-identical to the committed v7.2 baseline.

| Ordinal | Anchor | Draft evidence | Exact quote | Pinned quote line | Words | Distinct bytes | Status | Verdict |
|---|---|---|---|---|---:|---:|---|---|
| 1 | psi.rst:60-65 | Psi1:89 | `The ratios (in %) are tracked as recent trends over ten, sixty, and` | psi.rst:60 | 13 | 21 | same ✓ | PASS |
| 5 | psi.c:1379-1380 | Psi1:93 | `if (!privileged && window_us % 2000000)` | psi.c:1379 | 6 | 23 | same ✓ | PASS |
| 9 | psi.c:1686 | Psi1:97 | `return psi_show(m, &psi_system, PSI_IRQ);` | psi.c:1686 | 4 | 25 | same ✓ | PASS / short |
| 13 | psi.rst:40-43 | Psi1:100 | `some avg10=0.00 avg60=0.00 avg300=0.00 total=0` | psi.rst:42 | 5 | 16 | same ✓ | PASS |
| 17 | psi.c:1282-1288 | Psi1:104 | `if (!(group == &psi_system && res == PSI_CPU && full)) {` | psi.c:1283 | 11 | 26 | same ✓ | PASS |
| 21 | psi.c:1269-1270 | Psi1:108 | `group->avg_next_update = update_averages(group, now);` | psi.c:1270 | 4 | 23 | same ✓ | PASS / short |
| 25 | psi.c:1364-1367 | Psi1:112 | `if (res == PSI_IRQ && --state != PSI_IRQ_FULL)` | psi.c:1365 | 8 | 23 | same ✓ | PASS |
| 29 | psi.c:1257-1258 | Psi1:115 | `if (static_branch_likely(&psi_disabled))` | psi.c:1257 | 2 | 21 | same ✓ | PASS / short |
| 33 | psi.c:1711-1719 | Psi1:119 | `proc_create("pressure/io", 0666, NULL, &psi_io_proc_ops);` | psi.c:1714 | 4 | 24 | same ✓ | PASS / short |
| 37 | psi.rst:102-104 | Psi1:121 | `The kernel accepts window sizes ranging from 500ms to 10s, therefore min` | psi.rst:102 | 12 | 25 | same ✓ | PASS |
| 41 | cgroup-v2.rst:1066-1081 | Psi2 direct draft | `This control attribute is not hierarchical, so disable or enable PSI` | cgroup-v2.rst:1073 | 11 | 20 | same ✓ | PASS |
| 45 | psi.c:551 | Psi1:128 | `sample = group->total[PSI_AVGS][s] - group->avg_total[s];` | psi.c:551 | 5 | 26 | same ✓ | PASS |

## Mechanical receipt and reproduction

Executed Python computations through Eval, not a counter or alternate lane runtime. For each table row, with `q = quote.encode()`, `new = pinned.read_bytes().splitlines()`, `old = baseline.read_bytes().splitlines()`, and inclusive anchor bounds `lo, hi`:

```python
matches = [n for n in range(lo, hi + 1) if q in new[n - 1]]
same_span = old[lo - 1:hi] == new[lo - 1:hi]
words = len(quote.split())
distinct_bytes = len(set(q))
```

Actual aggregate output:

```text
pointers=47 selected=12
sample_rows 12 all_location_ok True all_same_span True all_contract_word_byte_limits True pairwise_distinct True
frozen_counter_short_quotes ['psi.c:1686', 'psi.c:1269-1270', 'psi.c:1257-1258', 'psi.c:1711-1719']
psi.c:1686 maximum_line_tokens=4
psi.c:1269-1270 maximum_line_tokens=4
psi.c:1257-1258 maximum_line_tokens=2
psi.c:1711-1719 maximum_line_tokens=4
```

Source identity was independently checked with read-only commands of this exact form, invoked with argument arrays:

```text
git -C /home/vgpnk/Projects/shokunin/mori-shokunin show 7370a731abcafc4c803111de7c22cd6264d63be1:corpus/evidence/sources-r61/psi.c
```

The same command was executed for each of the three new copies and three old baselines below. Every returned blob equaled the worktree bytes (`worktree_matches_freeze=True` six times). New-copy sha256 values match frozen `count-c2.py:31-36`:

| File | New pinned SHA256 | v7.2 baseline path under corpus/evidence/sources-r55/ | Baseline SHA256 |
|---|---|---|---|
| psi.c | c4edc1e7c18ca76e6e29668093fa0b26d4251cb088f2d5feab24681f285ec63f | kernel_sched_psi.c.v7.2 | 452318beaca3e6d19ab81a16528ae6b1695828a9ed080e329d07dedd9a3312c5 |
| psi.rst | 11c6b7129103b4547c31895cb1cfc0ff75b741c95a24bfcaeb01dece37b82692 | Documentation_accounting_psi.rst.v7.2 | 11c6b7129103b4547c31895cb1cfc0ff75b741c95a24bfcaeb01dece37b82692 |
| cgroup-v2.rst | 2750c11a6324e18f4d3a9bb63032b55f3268bd7077b80897af2f15a712611b68 | Documentation_admin-guide_cgroup-v2.rst.v7.2 | a9433bb0e16a67f07a93424c7bf842f47616e9b0a27b51e17d7b34cff246b7ad |

Frozen counter inspected SHA256: `82d0fee6124685f8a50f93550f3665703a33dce644948958db642a77d5aec2d8`.

## Residual risk and verification gaps

- Pairwise distinctness is proved for these twelve rows; the eleven Psi1 quotes were also checked against all 41 Psi1 draft rows, with zero collisions. No claim is made about all 47 finalized rows, provenance, source-registry admission, or a live C2 result. No counter was executed by this seat.
- No sampled row is `moved` or `changed`; those status paths are not exercised. All twelve `same` statuses were checked against actual old/new range bytes.
- LSP unavailable: reading `xd://lsp` returned `No such tool`; thus no status/references/definition/diagnostics device could answer. Text parsing and direct byte comparisons are literal evidence, not semantic LSP proof.
- The disk-guard command `bash /home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status` printed `/tmp 24% 97.5G`, `/var/tmp 41% 533.9G`, `/fast/scratch/hyaku 58% 341.1G` before its consumer walk timed out at 30 seconds. No ENOSPC or heavy clone work occurred; no successful full status completion claimed.
- Created and set TMPDIR to `/fast/scratch/hyaku/mori-r61/Mo61Reviewer06`; it remained empty and was removed before report handoff (`scratch_removed=True`). No tools installed, no production edits, no VCS mutations, no remediation.

Self-evaluation: accuracy 5 (byte comparisons and frozen blob identity), completeness 4 (12 requested rows checked; companion row reviewed from direct draft rather than finalized report), clarity 5 (individual verdicts separate contract from counter), actionability 5 (four exact failing anchors and canonical guard), conciseness 4 (reproduction hashes lengthen receipt). Average 4.6. This recommendation is not an admission or integration verdict.
