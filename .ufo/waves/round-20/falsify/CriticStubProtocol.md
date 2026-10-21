PARTIAL — The initial “non-empty file = retained report” result is broken by the mandatory `STATUS: started` first write: it records bytes, not a completed report, and can falsely make a wave appear settled. The R2 `stub` bucket correctly separates the six stubs visible in the 10:46Z snapshot without dropping members. The evidence does not establish what happened to the other markers between snapshots, so it does not prove that all earlier marker-only paths became substantive reports.

## Counterexample and evidence

- `build/ContractReview.md:50-53` says `present` was defined by a regular, non-symlink file with size > 0; the seat protocol writes `STATUS: started` first; and the measured Mori R20 wave had 76/76 such files, hence `settled`, although 18 files were exactly the 15–16-byte marker. The report classifies those 18 as marker-only, not completed reports. This is a direct false-positive report-retention count and false `settled` state, not merely a theoretical risk.
- The earlier `evidence/wave1-settlement-scan.json:1` records the same R20 dispatch identity (`dispatch_sha256` `98487ee16e4c02454a624fe5245a11949305d3a4415d450783191d44acab51a0`) as `settled`, with 76 present and 0 stub. Its totals are 586 present, 0 stub, 671 members; state totals are 8 settled / 3 partial.
- The 10:46Z `evidence/c2-live-mori.json:1` retains that dispatch identity and 76-member denominator but classifies the R20 wave as `partial`: 70 present, 6 stub. Its six stub entries are TokPathAge, TokSilenceA, HistR13, HistR14R15, VolatileContract, and ContractReview. Global totals are 580 present, 6 stub, 671 members, 85 missing; state totals are 7 settled / 4 partial.
- Thus the observed R2 accounting moves six items out of `present` into `stub`, changes the affected wave from settled to partial, and preserves the member denominator (`580 + 6 + 85 = 671`). It does not inflate current `present` by counting these six markers. `build/ContractReview.md:140` describes the narrow correction: exact marker after whitespace stripping, bounded to 64 bytes, is `started` and not present. `build/ContractReview.md:209` explicitly leaves whether marker-only seats were still running as [INFERENCE].

The 18-to-6 difference is between captures, not a same-time before/after experiment. [INFERENCE] Some marker files may have been replaced between them; the evidence does not justify treating the remaining 12 as completed reports solely from that delta.

## Impacted axes

- **Report retention / completion semantics:** overstated by the original size-only predicate; a marker file exists but is not a report.
- **Count and state correctness:** the earlier count can overstate `present` and falsely settle a partially reported wave. The observed R2 `stub` classification corrects this for six current members.
- **Coverage denominator:** no regression observed; stubs remain declared members rather than disappearing or being added to `missing`.
- **Temporal comparability:** the two snapshots cannot explain the fate of all 18 earlier markers.

## Smallest safe correction / recommendation

Keep the R2 distinction: classify only the exact protocol marker (after the specified whitespace handling and size bound) as `stub`, never as `present`; do not omit it from the member denominator; and do not let a stub satisfy `settled`. Keep marker-only stubs separate from `missing`, since a file exists. Pin this with a marker-only test that expects `stub`, `present=0` for that member, and a non-settled wave. For claims about how many reports were retained, use a same-time snapshot and report substantive `present` separately from physically retained marker files. No evidence here supports changing the protocol's first write; the counting semantics are the defect.
