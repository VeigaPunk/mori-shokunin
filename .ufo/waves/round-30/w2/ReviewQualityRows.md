# W2 review — QUALITY 88-93 (seat MoriR30.ReviewQualityRows)

Verdict: **agree with defects found** — every fail/pass state each criterion names reproduces exactly from committed
bytes; two findings: QUALITY 92 is unmet at the round-30 tip (`limit_stated=no`: no SKILL/knowledge line names a
frozen case id), and QUALITY 93's stated check cannot detect the unadjudicated-receipt condition its own text
requires. No check is unable to fail.

Lane tip measured: 713be294 (wave-2 spec); QUALITY 88-93 committed at ad0f047 (QUALITY.md:466-663), working copy
byte-identical to HEAD. Tooling: none installed (bash/git/python3 as shipped); all runs are read-only commands plus
scratch repos under /fast/scratch/hyaku/mori-r30-w2/ReviewQualityRows/.

Method: the three inline check scripts were extracted verbatim from committed fences
(`git show HEAD:corpus/QUALITY.md`, fences at :495-518, :534-568, :608-646), dedented 4 spaces, placeholders
substituted, and executed. The two lane scripts were run from their commit blobs via `bash <(git show <rev>:<path>)`.
Nothing in the lane was written except this report.

## Per-criterion results (claimed vs observed)

### 88 — tip receipts cited where the tip check reads (QUALITY.md:468)
- FAIL claim: b581173a/29 → observed exactly: `counter=count-c1.sh … cited_lane=no`, `counter=count-c2.sh …
  cited_lane=no`, `retention receipt=… cited_lane=yes`, `tip_receipts=unmet`, rc=1
  (`bash <(git show 1c4c186:.ufo/waves/round-28/check-tip-receipts.sh) b581173a 29`; script identical at HEAD).
- PASS claim: 1fc6bb0/28 → observed: all three receipts `cited_lane=yes`, `tip_receipts=met`, rc=0.
- "LOG.md at the parent already names `tip-count-c1.txt`" — verified: LOG.md:1907 is byte-identical at 1fc6bb0 and
  1fc6bb0^ (`… tip-count-c1.txt, tip-count-c2.txt, tip-retention.txt`). At b581173a the same LOG line names the
  round-28 names, so round-29's `tip-c1.txt`/`tip-c2.txt` are cited only in SCORECARD.md:1796-1797 — matches the
  spotcheck R1 statement (round-29-verifier-spotcheck.md:154-157).

### 89 — absence reject rows need command + output (QUALITY.md:486, script :496-517)
- FAIL claim: a66751b1/29 → observed exactly: `line=65 absence_reason_without_grep_command_or_output`,
  `absence_reject_rows=1 malformed=1`, rc=1. Line 65 at a66751b1 is the S155 reject row (verified by sed -n 65p).
- PASS claim: scratch Gate row with `` `grep -in dryrun f.go` -> `0`, exit 1 `` → observed
  `absence_reject_rows=1 malformed=0`, rc=0 (scratch repo sc89, one commit).
- Red input "command but no output" → observed `line=5 … malformed=1`, rc=1 (sc89r).

### 90 — word-count labels equal wc -w (QUALITY.md:526, script :535-567)
- FAIL claim: a66751b1/29 → observed exactly: five mismatches `:57 11/10, :60 11/10, :61 5/4, :62 17/16, :63 8/6`,
  `word_labels=16 mismatched=5`, rc=1 — every line number and pair as written.
- Round-28 claim: at 1fc6bb0/28 → observed `line=67 label=11 wc=14` on the `` `async.maxJobs` \| … `` cell (S147),
  `word_labels=6 mismatched=1`, rc=1 — the `\|`-as-token behavior the row discloses.
- PASS claim: scratch lesson, 3 correct labels (before-form, after-form, `/`-joined pair) → observed
  `word_labels=3 mismatched=0`, rc=0 (sc90).

### 91 — gate enters counted conditions only with a committed discriminating --selftest (QUALITY.md:580)
- FAIL claim at a66751b1: `git cat-file -e a66751b1:.ufo/waves/round-30/check-blind-wave.sh` → rc=128, fatal "not in
  'a66751b1'" — exactly the row's "(git cat-file -e exits 128)".
- Round-29 gate claim at d6d5cb0a: run from a file named check-blind-wave.sh, `--selftest` prints exactly
  `usage: check-blind-wave.sh <lane-rev> <wave-report-dir> <writer-name-regex>` and exits 2. (Via process substitution
  the same script prints `usage: 63 …` — $0 artifact, same exit code.)
- PASS at HEAD: `bash <(git show HEAD:.ufo/waves/round-30/check-blind-wave.sh) --selftest` → `PASS`, rc=0, run with
  cwd inside the lane (the script writes only under mktemp /tmp). Matches the committed receipt
  .ufo/waves/round-30/evidence/gate-selftest.txt at 32e287ff (`PASS`, `exit: 0`), which is committed before the freeze
  db1ec469 (32e287ff is an ancestor: `git log --format=%H db1ec469 | grep -c 32e287ff5589…` = 1).
- The selftest's own discrimination is committed in the script: synthetic clean run (scanned=6, four leak classes
  present, false-vocabulary lines absent) plus the round-29 wave at d6d5cb0a (scanned=8, blind_violations=9, exact
  expected (file,rule) pairs, no false hits) — consistent with lesson round-29.md:32-37, :96-99 and spotcheck
  R5 (:162-163, "20 hits all adjudicated false positives").

### 92 — disputed A2a verdict pinned by frozen case + stated limit (QUALITY.md:599, script :609-645)
- FAIL claim: a66751b1 → observed `missing_case_file`, rc=2 (file absent at that rev).
- PASS claim: scratch one-commit repo, one disputed case + `Limit: case pin-a2a …` knowledge line → observed
  `pinned=1 limit_stated=yes frozen=yes`, rc=0 (sc92).
- All three documented red inputs reproduce: KILLER_ACTED verdict → `pinned=0 … ` rc=1 (sc92a); second commit edits
  the case → `frozen=no`, rc=1 (sc92b); limit line removed → `limit_stated=no`, rc=1 (sc92c).

### 93 — pre-freeze adjudicated receipt of the freeze gate blob (QUALITY.md:656, prose check)
- `git log --reverse --format='%H %s' -- .ufo/waves/round-30/evidence/gate-a2-prefreeze.txt` → the only commit is
  55f9a694 (A3), which is an ancestor of the freeze db1ec469 (`git log db1ec469 -- <path>` lists it).
- The receipt names the A2 gate ("blob at 32e287ff" = 893e69d1…), shows `scanned=4 / blind_violations=4` and a prose
  note — it does not name the freeze blob dbcbe50e… (the gate blob at db1ec469 and 55f9a694 are both dbcbe50e…;
  32e287ff's is 893e69d1…). The only receipt of a freeze-blob run, c2-after.txt (`blind_violations=1`), lands at
  0b828c2, not an ancestor of the freeze (`grep -c` = 0). `git log --all -S dbcbe50e…` is empty: no committed file
  ever carries the freeze gate blob hash. So the row's check fails on round-30 state — "shown able to fail" is
  honest, and the criterion is non-vacuous.

## Findings by severity

1. **Medium — QUALITY 92 is unmet at the round-30 tip, and the miss is not in the round's receipts.** Running the
   row's check at HEAD prints `pinned=8 limit_stated=no frozen=yes`, exit 1. The eight frozen case ids
   (`r30-disputed-missing-stamp-one-send`, …, `tools/fixtures/mori-oom-killers/cases-a2-r30.json`) appear in no
   committed line of SKILL.md or corpus/knowledge/ (`git grep -n "r30-disputed" HEAD -- SKILL.md corpus/knowledge/`
   → rc=1, no hits; ids exist only in w1/CaseR30a-d.md, CriticC2Design.md, wave1 JSON and the fixture). The A2a limit
   is stated in prose (SKILL.md:753; corpus/knowledge/earlyoom-invocation-scope-r30.md:6, :56-60, :115) but never on
   a line that also names a case id, so the row's "stated where the next reader looks" conjunct fails. Round 30 does
   not claim row 92 (consistent with its C2=unmet report), but its receipts record only `blind_violations=1`
   (c2-after.txt) as the miss reason; a reader would not learn the limit-line conjunct is also unmet. Fix is one
   SKILL/knowledge line naming a case id and the limit.

2. **Medium — QUALITY 93's stated check cannot detect what its text requires.** The row demands a receipt "with every
   hit adjudicated … by a non-author seat", but the Check tests only two conjuncts: receipt commit is an ancestor of
   the freeze, and the receipt names the freeze gate blob. Adjudication and authorship are never tested. Proof from
   the row's own demonstration: gate-a2-prefreeze.txt carries 4 hits with only a prose note, authored by the round
   seat itself; had the gate blob not changed between run (A2 893e69d1) and freeze (A3 dbcbe50e), both conjuncts
   would pass with unadjudicated hits and the row could be claimed. As written, the criterion is stronger than its
   check; the check needs an adjudication-line/non-author condition to be able to fail on the defect it names.

3. **Low — QUALITY 89 passes vacuously on a lesson with no absence-reject rows.** Its exit is 0 when
   `absence_reject_rows=0 malformed=0`; unlike row 90 (explicit `n>0` guard), a Gate scrubbed of such rows, or a
   lesson with no `## Gate`, passes. It can fail (line 65 run proves it), so this is not a cannot-fail defect — an
   asymmetry worth one line in the row if tightness matters.

4. **Info — QUALITY 93's parenthetical "(`32e287ff`, gate-a2-prefreeze.txt)" is loose about where the receipt
   lands.** 32e287ff is the gate-version commit (evidence/ there holds only census-start.txt and gate-selftest.txt);
   the prefreeze receipt first enters history at 55f9a694 — the same commit that updates the gate to A3. The row's
   numbers (4 unadjudicated hits; +1 at the freeze blob) are accurate; only the attribution is compressed. The
   lesson's own M5-retitled note (corpus/lessons/round-30.md:204) states the timing correctly.

## Residual risk and verification gaps

- The inline scripts were dedented (4-space block indent) before running; the dedent is lossless (no line had <4
  leading spaces; python bodies keep their relative indent), but a byte-exact runner would `git show` the block and
  `unindent` programmatically — no semantic difference observed.
- Row 90's escaped-quote edge (`\"` inside a quote) was exercised only by the real corpus lines at a66751b1/1fc6bb0,
  which is where the routed defect lives; no synthetic escaped-quote case was added.
- Row 92's `disputed()` was probed with positives and the three documented reds only; non-active-state negatives
  (`ActiveState != active`) were not separately planted.
- The selftest run for 91 was executed at HEAD only; the PASS receipt at 32e287ff was compared by content, not by
  re-running that historical blob.
- LSP was not used: every check here is a shell/python program over git bytes, so semantic proof is the executed
  command output itself, cited above.
