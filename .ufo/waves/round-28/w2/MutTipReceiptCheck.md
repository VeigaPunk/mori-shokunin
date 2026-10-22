# MutTipReceiptCheck — mutation probe of `check-tip-receipts.sh` (f2de0ee)

Seat: `MoriR28.MutTipReceiptCheck` (mutation-tester, leaf — no subagents dispatched).
Target: `.ufo/waves/round-28/check-tip-receipts.sh` at lane commit
`f2de0eedcd60d2e354da75265ea6122bc3896073` (QUALITY 84 check). Detector bytes are the
target blob byte-for-byte (sha256 `172f140751de38b753cd6d5eca37fe215855dc8828933e890b4879f4cc3a492c`,
verified equal to `git show f2de0ee:.ufo/waves/round-28/check-tip-receipts.sh`).
No byte of the target was edited: the sandbox object database is selected at run time with
`GIT_DIR`/`GIT_WORK_TREE`/`GIT_INDEX_FILE`; every git call the detector makes is a read.

## Method

Scratch: `/fast/scratch/hyaku/mori-r28-w2/MutTipReceiptCheck/`. The lane clone sits at
`lane/` (HEAD = f2de0ee). Each fixture is two commits built from a temp index + `commit-tree`
(no fixture ever sees another fixture's history; the sandbox working tree is untouched):

- `P` = fixture parent (the revision the receipts must name),
- `T` = fixture tip batch (child of P) carrying receipts + report citations.

Detector run: `bash mut/pristine-at-f2de0ee.sh <T> 28` with the sandbox `GIT_DIR`. The real
lane was never written (lane `.git/index` sha256 `c8b58d0352b35a263e09b7ae4a449e438e577990ad483f341fbbedf1db078724`
before and after; lane HEAD unchanged; the only lane changes are the pre-existing untracked
files from the working seat).

Verdicts: `killed` = detector exited 1 and printed the defect (correctly rejected);
`survived` = detector exited 0 / `tip_receipts=met` on a defective batch (fail-open);
`inconclusive` = detector exit 2 (bad rev / no parent / missing contract / usage).

## Results (32 fixtures)

| # | fixture | exit | verdict | what the detector was given |
|---|---------|------|---------|------------------------------|
| 1 | s00_met | 0 | met (baseline) | three receipts name P, `exit: 0`, stdout, all cited |
| 2 | m01a_wrong_parent | 1 | killed | c1 receipt names the grandparent; P absent |
| 3 | m01b_wrong_parent_but_P_present | 0 | **survived** | c1 receipt's `revision:` names the grandparent; P mentioned elsewhere in body |
| 4 | m01c_short_hash | 1 | killed | c1 receipt names P as 7-hex prefix |
| 5 | m01d_no_revision_line | 0 | **survived** | c1 receipt has no `revision:` line at all (P only inside `command:`) |
| 6 | m01e_parent_of_parent_only | 1 | killed | c1 receipt names the grandparent; P absent |
| 7 | m02a_no_exit_line | 1 | killed | c1 receipt has stdout but no `exit:` line |
| 8 | m02b_exit_equals_style | 1 | killed | c1 receipt writes `exit=0` (house style of `evidence/c1-before-a1.txt`, `c2-before-*.txt`, `misroot-*.txt`) |
| 9 | m02c_nonzero_exit | 0 | **survived** | c1 receipt records `exit: 1` (`C1=unmet`) |
| 10 | m02d_no_stdout | 0 | **survived** | c1 receipt has headers + `exit: 0`, no stdout line |
| 11 | m02e_three_lines_only | 0 | **survived** | c1 receipt is exactly 3 lines (revision, command, `exit: 0`) |
| 12 | m03a_c2_not_cited | 1 | killed | c2 receipt valid but uncited (cited_lane=no) |
| 13 | m03b_c2_cited_by_longer_name | 0 | **survived** | receipt file `tip-c2.txt`; report cites `r28-tip-c2.txt` (basename substring) |
| 14 | m03c_negative_citation | 0 | **survived** | report says "No receipt named r28-tip-c2.txt was produced" (substring match) |
| 15 | m03d_extra_uncited_receipt_after | 1 | killed | extra uncited c1 receipt collates before the cited one → picked first → uncited |
| 16 | m03e_extra_uncited_receipt_before | 1 | killed | extra uncited c1 receipt collates first → picked first → uncited |
| 17 | m03f_receipt_cited_in_lesson_only | 0 | met | c2 cited only in the round lesson (valid: "cited by name in a report") |
| 18 | m04a_c2_receipt_absent | 1 | killed | count-c2.sh has no receipt at all |
| 19 | m04b_c2_receipt_names_no_counter | 1 | killed | c2 receipt never names `count-c2.sh` |
| 20 | m04c_retention_receipt_absent | 1 | killed | retention scan has no receipt |
| 21 | m05_shared_receipt | 0 | **survived** | one receipt names both `count-c1.sh` and `count-c2.sh` (no separate c2 receipt) |
| 22 | m06_receipt_outside_evidence_dir | 1 | killed | c2 receipt sits outside `.ufo/waves/round-28/evidence/` |
| 23 | m07_c2_named_in_c1_receipt_only | 0 | **survived** | c1 receipt merely mentions `count-c2.sh` in a note; c2 has no receipt |
| 24 | m08_citation_by_longer_name | 0 | **survived** | report cites only `r28-tip-c1.txt.bak` (substring) |
| 25 | m09_indented_exit_line | 1 | killed | `  exit: 0` (regex is line-anchored) |
| 26 | m10_uncited_duplicate_sorts_after | 0 | **survived** | extra uncited c1 receipt collates after the cited one → never examined |
| 27 | m11_uncited_duplicate_sorts_before | 1 | killed | extra uncited c1 receipt collates before → picked first → uncited |
| 28 | m12_retention_wrong_parent | 0 | **survived** | retention receipt names grandparent but mentions P elsewhere |
| 29 | m13_retention_no_exit_line | 1 | killed | retention receipt lacks `exit:` line |
| 30 | m14_citation_by_suffix_name | 0 | **survived** | report cites only `r28-tip-c1.txt.bak`; receipt basename is a suffix of it |
| 31 | m15_contract_drops_c2_counter | 0 | **survived** | tip batch edits `contract.md` to rename `count-c2.sh`; no c2 receipt needed |
| 32 | m16_contract_drops_retention_clause | 1 | killed | tip batch edits `contract.md` to rename `mori-retention-gate.py`; retention receipt still required (checked by name in evidence, not contract grep) |

Restore: the met case (s00_met) re-ran after every mutant — same output, exit 0,
`tip_receipts=met`.

## Fail-open paths (survivors — coverage findings)

1. **Wrong parent accepted when P is mentioned anywhere in the body** (m01b, m12): the
   detector checks `case "$body" in *"$P"*)` — a whole-body substring test, not "the
   `revision:` line names P". A receipt measured at the grandparent that merely *mentions*
   the parent hash (e.g. `compared_with_parent: <P>`) passes. Same for the retention receipt.
2. **No `revision:` field required** (m01d): P in the `command:` line is enough.
3. **Exit value never checked** (m02c): `exit: 1` (or any `^exit: *[0-9]+` line) satisfies
   the check; a receipt of a *failed* counter run (`C1=unmet`) renders `tip_receipts=met`.
4. **"At least one line of stdout" is not enforced** (m02d, m02e): the code requires ≥3
   non-empty lines in the whole body (`grep -cE '.' >= 3`); header lines (revision, command,
   exit) satisfy it with zero stdout. Headers themselves count toward the 3-line floor.
5. **Citation is a bare basename substring over the concatenated report text** (m03b, m03c,
   m08, m14): citing `r28-tip-c2.txt` satisfies a receipt named `tip-c2.txt`; a *negative*
   sentence ("No receipt named … was produced") counts as a citation; `r28-tip-c1.txt.bak`
   cites `r28-tip-c1.txt`.
6. **Only the first matching receipt per counter is citation-checked** (m10 vs m11): the loop
   `for f in $RECEIPTS; do …; hit=$f; break` stops at the first receipt satisfying the body
   checks, in `ls-tree|sort` (locale-collated) order. An uncited duplicate that collates after
   the cited receipt is never examined (m10 survived); one that collates before is what fails
   (m11 killed) — verdict depends on filename collation.
7. **A counter is satisfied by any receipt whose body contains its script name** (m05, m07):
   a single receipt naming both counters, or a c1 receipt whose note mentions `count-c2.sh`,
   counts as the c2 receipt. The detector never checks that the receipt was produced by that
   counter or that its stdout belongs to it.
8. **Counter set is read from the contract at `$R`** (m15): a tip batch can edit
   `contract.md` (renaming `count-c2.sh`) so the counter disappears from the required set and
   no receipt is demanded. (Eliminating the retention mention does not help — retention is
   matched by the tool name in the evidence body, not the contract grep.)

## Killed directions (correctly rejected)

Absent `exit:` line, `exit=0` style, indented `exit:` line, short/absent/foreign revision
without P anywhere, uncited selected receipt, missing c1/c2/retention receipt, receipt outside
`evidence/`, and deleting the retention clause from the contract all exit 1.

Note: `exit=0` (house style in 7 of the 10 pre-existing round-28 evidence files) is *rejected*
by `^exit: *[0-9]+` — the L1's tip receipts must use `exit: 0` (colon).

## Can it pass on a round-28 last batch?

- **Structurally yes**: the met fixture exits 0: three receipts measured at the batch's first
  parent, `exit: 0`, stdout, basename-cited in LOG.md and/or the lesson. The last batch must
  add its own receipt files naming its own parent, and the citation must already be visible at
  `$R` (in LOG.md or the lesson) since reports are read at `$R`.
- **On the real lane now (f2de0ee): no**. Every counter receipt is MISSING (measured parent
  `d21b8bd38...` appears in no receipt for count-c1.sh / count-c2.sh / retention). The check is
  designed to fail until the last batch lands.
- **Caveats for the L1**: (a) exit `exit: 0` (not `exit=0`); (b) keep the receipt's
  `revision:` line exactly equal to the first parent's full 40-hex and cite receipts by their
  exact basename; (c) the fleet-report mode (`--report-repo/--report-rev`) additionally
  requires the fleet `.ufo/reports/round-28/mori.md` to cite the receipt names — at the real
  fleet HEAD this file is not in the tree, so that mode cannot pass until the fleet report is
  committed and cites the receipt names.
