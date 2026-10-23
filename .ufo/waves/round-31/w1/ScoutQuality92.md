# W1 scout — QUALITY 92 at the round-30 tip, and the 85+ can-fail census (routed D3)

Seat: MoriR31.ScoutQuality92. Read-only. No subagents, no background jobs.
Tip measured: `a12c68ae81257fb6f918bb165bcb39c73f82d212` (round-30 verifier spot-check; `git rev-parse` resolves it,
`git log --oneline` names it "round-30 verifier spot-check (integrator, hyaku): non-author admit/reject").
`corpus/QUALITY.md` at that commit is 663 lines, criteria 85-93 — no 94 (extracted verbatim to
`/fast/scratch/hyaku/mori-r31/ScoutQuality92/QUALITY.at-tip.md`, `wc -l` = 663).
All checks below were extracted verbatim from the committed fences at that rev, dedented 4 spaces, placeholders
substituted, and run with `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE timeout … bash`. Every git operation was
read-only (`show`, `rev-parse`, `log`, `ls-tree`, `grep`, `diff`). The only lane write is this report.
Tooling: nothing installed or updated (bash 5.3.20, git, python3 as shipped).

## Part A — Is QUALITY 92 met at `a12c68ae`? No.

### What it requires (`corpus/QUALITY.md:599-654` at the tip)

Three conjuncts, over committed bytes only:

1. **A frozen case pins the disputed A2a shape.** A case in `tools/fixtures/mori-oom-killers/cases-a2-r30.json`
   whose blob equals the blob at the first commit that added the file, for the shape: earlyoom `ActiveState=active`,
   `ActiveEnterTimestampMonotonic` absent or `0`, at least two journal version lines, a real send line before the last
   version line and none after it, then a plain restart, with `expect.verdict = KILLERS_UNKNOWN` (`:599-604`, check
   `:607-645`).
2. **The limit is stated where the next reader looks.** A line in `SKILL.md` or a `corpus/knowledge/` entry that names
   the case id **and** `limit`, saying the rule does not attribute a send that precedes the latest version line
   (`:603-606`). The check implements this literally as one line matching `\blimit` (case-insensitive) **and**
   containing the id of a disputed case (`:635-639`).
3. **The check's own exit contract:** `pinned=<n> limit_stated=<yes|no> frozen=<yes|no>`, exit 0 only when
   `pinned>=1`, `limit_stated=yes`, `frozen=yes`; 2 on a missing/unparseable case file (`:646-653`).

### Which artifact it applies to

Two carriers, not one: the frozen fixture `tools/fixtures/mori-oom-killers/cases-a2-r30.json`, and one documentation
line in `SKILL.md` or under `corpus/knowledge/`. The criterion fails if either carrier is missing or if the doc line
exists but does not co-name the id and `limit`.

### The evidence

Reproduced at the tip (script extracted from `corpus/QUALITY.md:609-646` at `a12c68ae`):

```
$ bash check92.run.sh            # lane=<lane>; rev=a12c68ae8125…; python3 -I -B body verbatim
pinned=8 limit_stated=no frozen=yes
rc=1
```

- **Conjunct 1 holds, and the freeze is real.** `pinned=8`: all eight case ids match the disputed predicate and expect
  `KILLERS_UNKNOWN` (`tools/fixtures/mori-oom-killers/cases-a2-r30.json`, ids `r30-disputed-missing-stamp-one-send`,
  `…-two-sends-warning`, `…-escalation`, `…-sigkill`, `…-absent-clock`, `…-zero-clock`, `…-zero-stamp-kill-failed`,
  `…-absent-stamp-ordered`). `frozen=yes`: the file's blob at the tip is
  `a05863ccb0ac028e1b401dfa696f51bc735b9762`, identical to the blob at its adding commit
  `db1ec4694242a9c1acef03fef2852c7e943b1ed7` ("round-30: C2 freeze — cases-a2-r30.json (8 cases, 4 writers x 2)
  assembled without edits …"). `git show a12c68ae:…/cases-a2-r30.json | sha256sum` =
  `b68843e754977e78465039d196582f6d099f85ac7b17f7330fb8a8145f993735`, matching the `sha256 b68843e7…3735` recorded in
  that freeze commit message.
- **Conjunct 2 fails.** `git grep -n "r30-disputed" a12c68ae -- SKILL.md corpus/knowledge/` exits 1 with no output:
  no committed line in either carrier names a frozen case id. The A2a limit *is* stated in prose, but never on a line
  that also carries an `r30-disputed-*` id:
  - `SKILL.md:753` — "This is the A2a limit: for an `active` unit an earlier-invocation send is reported but is not a
    verdict input …" (no case id on the line);
  - `corpus/knowledge/earlyoom-invocation-scope-r30.md:6` — the title names "the A2a limit" (no case id);
  - same entry `:56-60` — names `a2-06-active-earlier-invocation-sends-quiet`, which is not an `r30-disputed-*` id;
  - same entry `:117` — "A2a: an active earlyoom's earlier sends never change the verdict" (no id, and the word
    `limit` is absent).
  So the reader can find the rule but cannot join it to the frozen case; the criterion's "names the case id and
  `limit`" conjunct is unmet, exactly as `corpus/lessons/round-30.md:228` records ("ReviewQualityRows finds QUALITY 92
  unmet at the tip (`limit_stated=no`: no `r30-disputed-*` id is named in SKILL or knowledge)") and as
  `.ufo/waves/round-30-verifier-spotcheck.md:183` routes ("QUALITY 92 is unmet at the tip (`limit_stated=no`)").
  Independent reproduction: `.ufo/waves/round-30/w2/ReviewQualityRows.md:79-80` printed the same
  `pinned=8 limit_stated=no frozen=yes`, exit 1.
- **No machine receipt records the miss.** `git grep -ln "limit_stated" a12c68ae` lists exactly five files:
  `corpus/QUALITY.md`, `corpus/lessons/round-30.md`, `corpus/lessons/round-30-verifier-spotcheck.md`,
  `.ufo/waves/round-30/w1/DraftQualityRows.md`, `.ufo/waves/round-30/w2/ReviewQualityRows.md`. Nothing under
  `.ufo/waves/round-30/evidence/` carries the string, so the round-30 C2 record (`c2-after.txt`,
  `blind_violations=1`, cited at `corpus/QUALITY.md:663`) does not disclose this second miss. That matches
  `ReviewQualityRows.md:1-4` ("the miss is not in the round's receipts") and `round-30.md:228`, which records the miss
  only in the lesson's prose.

**Verdict: QUALITY 92 is UNMET at `a12c68ae`** on the limit-line conjunct only; the case-pin and freeze conjuncts
hold. Severity: documentation-local — one `SKILL.md`/knowledge line naming an `r30-disputed-*` id together with
`limit` and the sentence "a send before the latest version line is not attributed" would satisfy the check. Note the
check is weaker than the text: any line containing a disputed id and the substring `limit` (e.g. "rate limit") passes,
so a fix should also carry the semantic sentence, else the row can be satisfied cosmetically.

## Part B — Every QUALITY criterion numbered 85 or higher at `a12c68ae`, and whether it can fail on its stated property

Nine criteria exist: 85, 86, 87, 88, 89, 90, 91, 92, 93 (`corpus/QUALITY.md:416, :433, :448, :468, :486, :526, :580,
:599, :656`). "Can fail" is judged on the check as specified at the tip, not on the criterion's good intentions; each
row names the run that shows it, either observed by me at `a12c68ae`/`5c99f2d` or reproduced from the row's own
committed FAIL case.

| # | Stated property (can it fail on it?) | Can fail? | Evidence (path:line, observed output) |
|---|---|---|---|
| 85 | A writer-blind wave's writer reports list files opened and cite no tool line/output; non-writer reports cite neither. | **Yes — can fail.** Observed exit 1 at the tip. Vacuous on an empty writer match. | `bash .ufo/waves/round-30/check-blind-wave.sh a12c68ae .ufo/waves/round-30/w1 '^CaseR30'` → `scanned=4`, `blind_violations=1`, `.ufo/waves/round-30/w1/CaseR30a.md:105:writer-forbidden-opened-path`, rc=1. With `'^NoSuchWriter'` → `scanned=0 blind_violations=0`, rc=0: a wave whose reports are all misnamed passes. Criterion `corpus/QUALITY.md:416-432`. Known parser defect (first hit only) does not make it unable to fail — routed D1, `round-30-verifier-spotcheck.md:176-178`. |
| 86 | Every reject decision its source work met is a Gate row with reason, source and located quote (or `reject sample: none met`). | **Yes — can fail** on a malformed cell or an all-admit Gate with no declaration. Cannot detect a reject row silently dropped. | At tip: `gate_reject_rows=22 none_declared=0 malformed=0`, rc=0 (non-vacuous). FAIL case `corpus/QUALITY.md:443-445`: round 28 at `7118f320` → `gate_reject_rows=0 none_declared=0`, exit 1. Criterion `:433-447`. |
| 87 | A receipts-only tip batch's files open with the exact `# measured at parent <40-hex>` header and add only evidence files. | **Yes — can fail.** Passes at the round-30 receipts batch. | Headers at `5c99f2d`: all three (`tip-c1.txt`, `tip-c2.txt`, `tip-retention.txt`) line 1 = `# measured at parent 926ac1460c0b9a542725257870f530f98e94e4b1; the landed tip adds only receipt files under .ufo/waves/round-30/evidence/`; `git diff --name-only 5c99f2d^ 5c99f2d` lists exactly those three. FAIL case `QUALITY.md:455-457`: `1fc6bb0` → `header_not_parent=…/tip-count-c1.txt`, exit 1. Criterion `:448-467`. |
| 88 | Tip receipts are cited by name in `LOG.md`/the round lesson before the receipts-only batch lands them. | **Yes — can fail.** Met at the round-30 receipts batch. | `bash .ufo/waves/round-28/check-tip-receipts.sh 5c99f2d 30` → three `receipt=… cited_lane=yes`, `tip_receipts=met`, rc=0. FAIL case `QUALITY.md:479-481`: `b581173a` → `cited_lane=no`, `tip_receipts=unmet`, exit 1. (The same command at `a12c68ae` prints `receipt=MISSING` only because `a12c68ae^1` is the receipts batch itself, so no receipt can name that parent — not a criterion-88 failure.) Criterion `:468-485`. |
| 89 | An absence-asserting Gate reject row carries the exact `grep` invocation in backticks and its output in the same row. | **Yes — can fail on a malformed row, but vacuous at the tip.** | At tip: `absence_reject_rows=0 malformed=0`, rc=0 — the round-30 Gate has 22 reject rows and none asserts absence, so the criterion is untested and certifies nothing about round 30 (`corpus/lessons/round-30.md:229` records the same vacuity). FAIL case `QUALITY.md:521-522`: `a66751b1` → `line=65 absence_reason_without_grep_command_or_output`, `absence_reject_rows=1 malformed=1`, exit 1. No `n>0` guard (unlike 90). Criterion `:486-525`. |
| 90 | Every `(N words)` label equals `wc -w` of its quoted text, `\|` counted as a token, with at least one label required. | **Yes — can fail**, with an explicit non-vacuity guard. | At tip: `word_labels=26 mismatched=0`, rc=0 (`n>0`). FAIL case `QUALITY.md:571-573`: `a66751b1` → `word_labels=16 mismatched=5`, exit 1 (`:57` 11/10, `:60` 11/10, `:61` 5/4, `:62` 17/16, `:63` 8/6). Criterion `:526-579`. |
| 91 | A gate enters a counted condition only with a committed `--selftest` that discriminates (clean→0, each planted class→violation) **and was committed before the counted run and the freeze**. | **Partly.** Can fail on a missing/weak selftest; **cannot fail on the ordering conjunct** — the specified check only runs `--selftest`, which passes at any commit. | At tip: `bash .ufo/waves/round-30/check-blind-wave.sh --selftest` → `PASS`, rc=0. FAIL case `QUALITY.md:591-593`: `a66751b1` path absent (`git cat-file -e` 128). The timing clause at `:581-584` is never exercised by the check at `:589-591`; round-30's own M5 (gate edited after its run, frozen without rerun) would pass this check. Criterion `:580-598`. |
| 92 | A frozen case pins the disputed A2a verdict, and a `SKILL.md`/knowledge line names the case id together with `limit`. | **Yes — can fail**, and does at the tip. | `pinned=8 limit_stated=no frozen=yes`, rc=1 at `a12c68ae` (Part A). FAIL cases reproduced by `ReviewQualityRows.md:64`: verdict `KILLER_ACTED` → `pinned=0`; second commit edits the case → `frozen=no`; limit line removed → `limit_stated=no`; all exit 1. Criterion `:599-654`. |
| 93 | A gate's counted condition carries a pre-freeze receipt of the **frozen** gate blob on the round's own inputs **with every hit adjudicated by a non-author seat**. | **No — cannot fail on its stated property.** This is the D3 class. | Check `QUALITY.md:660-661` tests only (a) receipt commit is an ancestor of the freeze and (b) the receipt names the freeze gate blob. Adjudication and non-authorship are never tested. Round-30's receipt `.ufo/waves/round-30/evidence/gate-a2-prefreeze.txt` carries 4 hits with a prose note, authored by the round seat; had the gate blob not changed between run (`893e69d1…` at `32e287ff`) and freeze (`dbcbe50e…` at `db1ec469`), both conjuncts pass with unadjudicated hits (`ReviewQualityRows.md:89-95`; `corpus/lessons/round-30.md:215`). The row's own "shown able to fail" run fails on the blob-change accident, not on adjudication. Criterion `:656-663`. |

### Reading of the census

- **Exactly one criterion is in the D3 class at the tip: 93.** Its check, as written, cannot detect the two conditions
  its own text names (per-hit adjudication, non-author seat). Confirmed independently by
  `corpus/lessons/round-30.md:215` and `round-30-verifier-spotcheck.md:181`.
- **91 shares 93's defect on one conjunct** (the pre-freeze ordering is not exercised by its check) and is a
  near-neighbour of the class, but it can fail on the discrimination conjunct it mostly cares about.
- **Two criteria are honest but vacuous in the round-30 state:** 89 measures 0 rows and 85 measures 0 writers when the
  regex matches nothing; both pass without testing what they claim. Neither is D3 (each has a demonstrated failing
  run), but neither certifies anything about a round that lacks the triggering rows. Criterion 90 shows the remedy the
  others lack — an explicit `n>0` guard (`:528-530`, `:567`).
- **89's vacuity is the largest unchecked surface**: a Gate could omit an absence-reject row entirely and 89 would
  still print `absence_reject_rows=0 malformed=0`, exit 0.
- Criteria 85-88, 90, 92 all have a demonstrated failing run at a named revision, observed or reproduced.

## Inference and unresolved gaps

- [INFERENCE] The criterion-92 fix is documentation-only and cannot change a counted verdict: the fixture is frozen
  (`frozen=yes`) and `pinned=8`, so only conjunct 2 is open. Not measured: whether any round-31 seat has already added
  such a line — at the time of writing the working tree's `corpus/QUALITY.md` differs from `a12c68ae` by +16 lines
  (criterion 94, uncommitted round-31 draft: "Supersedes criterion 93 (routed D3 …)"), and nothing in the tip's
  `SKILL.md`/knowledge carries a fixed line.
- [INFERENCE] `git grep` over `SKILL.md` + `corpus/knowledge/` is a text search, not a semantic proof. Here it is the
  criterion's own mechanism (the check is `git show` + regex over those files), so it is the right tool; a case id
  split across a line break would be invisible to both the criterion and this report, and none of the eight ids is
  near a wrap point in the two carriers.
- Not measured (out of scope for this ticket): whether round 31's C1/C2 artifacts should carry criterion 92 at all;
  the D1 parser defect's own gate-quality; criterion 94's can-fail status (it is another seat's draft and uncommitted).
- No blockers. No tool installs. No processes left running (all runs `timeout`-capped; scratch under
  `/fast/scratch/hyaku/mori-r31/ScoutQuality92/`).
