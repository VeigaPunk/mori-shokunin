# Wave-2 review — QUALITY criteria 85-87 (seat ReviewQualityCriteria)

Scope: QUALITY 85-87 as appended to `corpus/QUALITY.md` at `8809a3fe` (tail), the round-29 note on 85, and the
round-29 lesson `corpus/lessons/round-29.md`. Every check was run on committed bytes; no lane/fleet writes were
made. Runner for 85: `bash .ufo/waves/round-29/check-blind-wave.sh <rev> <dir> <regex>` (same script at the tip).
Runner for 86: the awk command quoted in QUALITY 86, verbatim. Runner for 87: the bash command quoted in QUALITY 87,
with `check-tip-receipts.sh` from `.ufo/waves/round-28/`.

## 1. Observed runs

### 85 — check-blind-wave.sh

- FAIL run 1 (stated fail input): `check-blind-wave.sh 84abe93e .ufo/waves/round-28/w1 '^CaseA2r'`
  → `blind_violations=38`, exit 1. Violations: 9 `nonwriter-tool-run-output` (BuildCountC2.md), 13
  `nonwriter-tool-citation` + 5 `nonwriter-tool-run-output` (CriticC2Design.md), 12 `nonwriter-tool-run-output`
  (ReviewA2SpecVsTool.md), 1 each ReviewQ80AtR27Tip.md / SupersedeS096.md / SupersedeS129.md / SupersedeS131.md,
  1 `writer-forbidden-opened-path` (CaseA2r03.md:187), 2 `writer-missing-files-opened-list`
  (CaseA2r06.md, CaseA2r10.md).
- FAIL run 1b (criterion's own M6 fail input): `check-blind-wave.sh d21b8bd3 .ufo/waves/round-28/w1 '^CaseA2r'`
  → `blind_violations=32`, exit 1 (first hits: CaseA2r03.md:187 writer-forbidden-opened-path; CaseA2r06.md and
  CaseA2r10.md missing files-opened list; CriticC2Design.md citations).
- FAIL run 2 (round-29 pre-freeze, evidence file): `evidence/blind-check-prefreeze.txt` at lane `221cbd8f`
  → `blind_violations=20`, exit 1 (20 hits listed, incl. 7 writer-missing-files-opened-list).
- FAIL run 3 (round-29 tip): `check-blind-wave.sh 8809a3fe .ufo/waves/round-29/w1 '^CaseA2(07|10)[a-d]\.md$'`
  → `blind_violations=20`, exit 1: AxisOperability.md:19; BuildTipReceipts.md:5,135,136,137,140; CaseA207a/b/c/d.md
  :1 and CaseA210a/b/d.md:1 (writer-missing-files-opened-list); DraftQualityCriteria.md:75,76,77,86; ReviewLateMutCountC1Amended.md:78;
  ReviewLateMutHeadingCheck.md:37,39. Identical hit set to the pre-freeze run.
- PASS run (synthetic clean dir, sandbox clone at
  `/fast/scratch/hyaku/mori-r29/w2/ReviewQualityCriteria/sandbox`): wave dir with only two writer reports
  (CaseA201a.md, CaseA201b.md) each carrying a `## Files opened` list naming safe paths
  (fixture JSON; own path) → `blind_violations=0`, exit 0.

So 85 can fail (exit 1, n>0) and can pass (exit 0, n=0) as stated. Note: at the round-29 tip the criterion's own
freeze commit still reports 20 violations; no committed round-29 freeze state passes the check today.

### 86 — Gate awk

- FAIL run 1 (stated fail input): `git show 7118f320:corpus/lessons/round-28.md | awk ...`
  → `gate_reject_rows=0 none_declared=0 malformed=0`, exit 1.
- PASS run (stated pass input): `git show 8809a3fe:corpus/lessons/round-25.md | awk ...`
  → `gate_reject_rows=7 none_declared=0 malformed=0`, exit 0.
- FAIL run 2 (round-29 tip): `git show 8809a3fe:corpus/lessons/round-29.md | awk ...`
  → `gate_reject_rows=0 none_declared=0 malformed=0`, exit 1. Yet the round-29 Gate table contains 8 reject rows
  (`| — | ... | reject, ... |`, lesson lines 56, 58-61, 63-65) and 3 S-id admit rows (S153, S154, S155). The awk only
  counts rows matching `^\| *S[0-9]+ *\|`; the reject rows carry an em-dash id (`—`), so they are invisible to the
  check. With no `reject sample: none met` declaration present, the check must exit 1.
- This is a check/format mismatch: 86 as written cannot pass on a Gate whose reject rows use the em-dash id form
  (the format the round-29 lesson itself uses, and which the lesson text at lines 49-51 describes as the reject-row
  form). If the intended round-29 Gate format is kept, the awk's row regex (or the table's id cells) must be
  reconciled before any round can claim 86.

### 87 — tip receipt tip

- FAIL run (stated fail input): `bash -c '...' <lane> 1fc6bb0 28`
  → `counter=count-c1.sh receipt=tip-count-c1.txt measured=5ef4e8db... cited_lane=yes`
  `counter=count-c2.sh ... cited_lane=yes`, `retention receipt=tip-retention.txt ... cited_lane=yes`,
  `tip_receipts=met`, then `header_not_parent=.ufo/waves/round-28/evidence/tip-count-c1.txt`, exit 1 (line 1 of
  `tip-count-c1.txt` at `1fc6bb0` is `revision: 5ef4e8db...`, not the required header).
- PASS run (synthetic tip, sandbox clone at `.../sandbox87` checked out at `5ef4e8d`, tip `9dd65de` adding the
  three receipt files with the exact header `# measured at parent 5ef4e8db...; the landed tip adds only receipt
  files under .ufo/waves/round-28/evidence/`):
  → `counter=count-c1.sh receipt=... measured=5ef4e8db... cited_lane=yes` (same for count-c2 and retention),
  `tip_receipts=met`, `tip_receipts=met receipts=3 only_receipts=yes`, exit 0. The parent `5ef4e8d` cites all three
  receipts in `LOG.md:1907`, so the citation half passes too.

So 87 can fail (exit 1, `header_not_parent`) and can pass (exit 0) as stated.

## 2. Findings (by severity)

1. **[HIGH] The round-29 freeze does not satisfy 85.** At `8809a3fe` the check prints `blind_violations=20`
   (exit 1), identical to the pre-freeze run at `221cbd8f`. A C2 condition (amendment A4) demands
   `blind_violations=0`; the freeze commit itself does not meet it. The round-29 lesson already records this as M2
   ("a gate bound into a counted condition before it was run on a known-clean input", lines 32-37) and the L1's
   note on 85 says so. Nothing in the tip's committed state changes the count.
2. **[MEDIUM] 86's check cannot pass on the round-29 Gate format.** Em-dash reject rows (`| — | ...`) are not
   matched by `^\| *S[0-9]+ *\|`; the check reports `gate_reject_rows=0` although 8 reject rows exist, and exits 1.
   As written, the criterion is satisfiable only by a Gate with S-id reject rows or by a `reject sample: none met`
   declaration. This is a genuine gap between the criterion's statement ("each decision cell", "a reject row names
   the source") and its own check.
3. **[LOW] 87's wrapper is lane-coupled.** `check-tip-receipts.sh` hardcodes `LANE=/home/vgpnk/Projects/shokunin/mori-shokunin`
   (line 31), so the 87 command as quoted cannot be run against a synthetic clone without an environment override
   (`GIT_DIR=...sandbox87/.git` worked). Not a defect in the lane's own use; affects only verifier portability.
4. **[LOW] `check-blind-wave.sh` regex-validity probe casts `$writer_re` as a regex against `/dev/null`.**
   A regex invalid in ERE makes `grep -E -q` exit 2 and the script exits 2 (usage error) — matches the spec's
   "invalid writer-name regex" path; no finding beyond confirming exit-2 behavior exists for bad regex/revision.
5. **[INFO] 85's "PASS tally of an older case file" clause.** The selftest marker exemption
   (`PASS 30/30|32/32`) is implemented as stated (script lines 72-78); no violation line is printed for such lines.
   Not exercised on a real older-case-file report in these runs.

## 3. Residual risk / verification gaps

- No run of `check-blind-wave.sh` on a real clean round-28/29 wave commit exists (none is clean). The PASS evidence
  is a synthetic two-report directory; the writer list, forbidden-path and non-writer halves of the script were
  exercised by the fail runs (writer-forbidden-opened-path, writer-missing-files-opened-list, nonwriter-tool-citation,
  nonwriter-tool-run-output all observed).
- The 86 awk's stated PASS input `round-25.md` (at `8809a3fe`) was run: `gate_reject_rows=7`, exit 0. The
  stated FAIL inputs (round-28.md at `7118f320`; round-29.md at `8809a3fe`) both exit 1. The only gap: the
  criterion's red inputs (malformed decision cell, empty source/quote) were not separately run.
- 87's stated PASS input (synthetic two-commit repo) was reproduced; the real lane has no tip batch yet that adds
  only receipts with the parent header (round-29 receipts are created by `make-tip-receipts.sh`, not yet landed in
  this wave).
- All runs used commit bytes only; no working-tree reads (85/86/87 read `git show`/`git ls-tree` output).
- No tool installs were needed; nothing was installed (tooling directive: nothing to record).

## 4. Cleanup

No files were created outside this report and the seat scratch dir
(`/fast/scratch/hyaku/mori-r29/w2/ReviewQualityCriteria/`: sandbox clones `sandbox/`, `sandbox87/`, `check87.sh`,
all scratch-only). The lane was not modified.
