measured 2026-10-23T07:57:16Z

# AuditScorecardLog — attempt-2 SCORECARD.md / LOG.md round-34 sections vs committed bytes at fd2521351c6c and the frozen contract

Object audited: `/fast/scratch/hyaku/mori-r34/a3-L1/drafts/SCORECARD.md` and `.../LOG.md` (sections after `fd2521351c6cef47384aef30afbe1e4db7e6912e`, per `attempt2-tracked.diff`). Committed tip moved to `5216d78` (wave-B spec commit) during the audit; `fd25213` remains the reference revision. No tools installed (operator directive: `git`, `python3`, `grep` sufficed). Read-only git only; no writes outside the report.

## Verdicts, statement by statement

VERDICT: agree — declared cells copy the frozen contract. SCORECARD C1 row: axis coverage (contract.md:17-18 "a new tool operation ... (coverage)"), predicate P-C1-A1, before `tool=absent C1=unmet` exit 1 at `f10a320d` (contract.md:60,140; receipt `evidence/c1-before.txt` lines 1-4, committed at `fd25213`), after `C1=met` at the landed tip (contract.md:61,140). C2 row: calibration 5, "no counting command", `unprovable-but-better` only with a named non-author reviewer — verbatim to contract.md:90-97. Anti-loop line ("rounds 32 (freshness) and 33 (depth) are not repeated") copies contract.md:7-8. "16 negative controls C1=unmet and 2 positive C1=met under P-C1-A1" copies contract.md:142-144 and matches committed `evidence/c1-controls.txt` (C-absent line and POS-l1-oracle-copy/POS-sectl lines verified).

VERDICT: agree — "Held" scores match the committed axes table. `git show fd25213:SCORECARD.md` axes table gives coverage 6, operability 7, depth 5, freshness 5, calibration 5, adjacency 6; the draft's Held line ("coverage 6, calibration 5, depth 5, freshness 5, operability 7, adjacency 6") is the same set (order differs, set identical). Also agrees with the committed round-33 Held line ("freshness 5, calibration 5, coverage 6, operability 7, adjacency 6, depth 5").

VERDICT: disagree — cited file `evidence/c1-tip.txt` does not exist. Absent from `ls .ufo/waves/round-34/evidence/` on disk and from `git ls-tree -r fd25213 .ufo/waves/round-34/`. The claim it supports ("same at the tip") is corroborated by wave-A report `.ufo/waves/round-34/wa/ExecRerunLane.md` (run_head at rev `fd25213`, 05:40:39Z, `C1=met`, :100), so the substance holds but the named receipt is dangling; if the section is kept, either land the receipt or cite `wa/ExecRerunLane.md`.

VERDICT: agree — `evidence/c1-after.txt` exists on disk and records exactly `count-c1-a1.py ba525e1a0394...c539c` → `fixed_pass=12/12 random_pass=300/300 coverage=ok live=ok C1=met` exit 0, measured 05:30:42Z before wave-A dispatch (receipt lines 1-9). Uncommitted (not in `git ls-tree fd25213`); same flag applies to `c1-before.txt` being committed vs `c1-after.txt` not — receipts land at closure per lane convention, consistent with round-33 history.

VERDICT: agree — `ef936fb4` is a sandbox-clone commit (parent `fd25213`), not a lane object: `git cat-file -t ef936fb4` fails in the lane; `evidence/ctl-postdata-shortcut/receipt.txt:2` states it is `/fast/scratch/.../a2-CritPostDataShortcut/clone rev ef936fb4e08...9d27`, tool bytes sha256 `cd5389b9...`, and the receipt's counter output prints `C1=met` exit 0. The draft's description ("skips the real two-sample read and R3") matches receipt.txt lines 3-4 verbatim.

VERDICT: agree — "not verified (honest stop, §9)": receipt.txt:11 rules "a post-data shortcut that skips the claimed operation meets the frozen P-C1-A1; under addendum §9 C1 is not verified". §9 is the prompt/addendum section — CritPostDataShortcut's dispatch prompt (`wa-spec.json` item prompt) says "Adversarial §9 attack on C1 after data ... If it meets, C1 fails under §9"; `wa/ReviewC2Judge.md:49` cites `mori-round-34.md:343-365`. The §9 file itself is not under `.ufo/waves/round-34/` — inherited term, consistent usage, no §9 section exists in contract.md. [INFERENCE: §9 lives in the round prompt file referenced by the judge; consistent across receipt, judge, lesson draft and both drafts.]

VERDICT: agree — C2 row verdict cell: `ReviewC2Judge.md` verdict line is `VERDICT: unprovable-but-better` (the only such verdict in wave A), and `wa/MutQ98.md` carries a `survived` variant consistent with "variant 2 survives ... M2". Named reviewer ReviewC2Judge, non-author per spec.

VERDICT: agree — entering tip `f10a320d9056d19a6d007420df49d7b16a3bf857` (`git rev-parse f10a320d` resolves to the full hash) and round-33 closed `rejected-honest-stop` (`git show fd25213:corpus/lessons/round-33-verifier-spotcheck.md:218` `status=ok`, `admitted=false`, `verdict rejected-honest-stop`).

VERDICT: agree — LOG attempt-1 facts: `24603186` = `2460318` "freeze C1/C2 contract, counter, before and positive-control receipts"; `b9fb029e` = `b9fb029` "C0 control receipts and Amendment A1 (pre-data)"; C0 had 10 seats (contract.md:113; ten `c0/Ctl*.md` reports committed). The 35-seat wave-1 figure matched `wave1-spec.json` (35 items) read earlier this audit; the `wave1-*.json` files were deleted from the working tree mid-audit (uncommitted attempt-1 scratch) — count verified before deletion, "died unsettled" consistent with no committed wave-1 reports.

VERDICT: agree — LOG attempt-2 facts: dead seat's draft scored `live=fed-no-interval C1=unmet` (`evidence/c1-tool-provenance.txt:4`, sandbox rev `54dc8567`); L1 live-arm fix described accurately (separate open/read/close per sample around the interval; `import stat` removed; provenance :6-30); landed at `ba525e1a` "C1 tool tools/mori-disk-rate.py (dead-seat draft + L1 live-arm fix) and provenance receipt"; `C1=met` per `c1-after.txt`.

VERDICT: agree — `8d56809a` commit message matches the LOG line verbatim: "SOURCES S191-S198 (copies re-fetched 05:32Z, sha match), entry rows 3r/6r/7r/13r + row 8 correction, SKILL Round34 + Round33 correction, QUALITY 98, lesson r33 corrections".

VERDICT: agree — wave-A seat count: `wa-spec.json` has 52 items, roles exactly 25 reviewer, 13 executor, 6 mutation-tester, 3 critic, 2 scribe, 1 scout, 1 connector, 1 sentinel — matches the LOG line.

VERDICT: agree — "8/8 sources admitted": eight `VERDICT: admit` lines across `wa/ReopenS191..S198.md` (`grep -h '^VERDICT' wa/*.md | sort | uniq -c`).

VERDICT: agree — "4/4 revised rows supported": `wa/JudgeRow3r.md`, `JudgeRow6r.md`, `JudgeRow7r.md`, `JudgeRow13r.md` each carry `VERDICT: row Nr: supported`.

VERDICT: agree — "routed items 3–8 repaired (two wrong details corrected in the lesson)": judges for the lesson corrections (`wa/JudgeLessonItem5.md` `VERDICT: repaired`; `Item6` no wrong statement; `Item7` `VERDICT: repaired` with one minor section-label mislabel; `Item8` `VERDICT: repaired` **but flags a new factual error in the corrective prose**: "the committed recheck-r33 tree at 89791013 contains eight, not nine, of S117's ten page copies" — `wa/JudgeLessonItem8.md:28,36`). Items 3–4 covered by the row-8 and SKILL correction judges. "Two wrong details corrected" is consistent (the :79/:52-53 word edit and the label/time-label detail), though the exact two are not enumerated in the LOG line. Residual: the Item-8 correction itself contains a new wrong detail — noted for the L1, not a defect of the draft's summary.

VERDICT: agree — "C1 re-measured `C1=met` in 15+ seat runs": `wa/ExecRerunLane.md` records 9 runs (8 fresh seeds + seed 1 at `8d56809`/`fd25213`/`ba525e1a`, 9/9 `C1=met`); `wa/ExecRerunClone.md` adds ≥6 fresh-seed and named-seed runs at `8d56809`/`ba525e1a` in a clone — ≥15 seat-side runs, all `C1=met`.

VERDICT: agree — "counter gaps from surviving mutants (M3)": mutation verdicts include `survived — M1, behavior-changing counter gap demonstrated` and equivalence/class mutants survived; draft lesson `corpus_lessons_round-34.md:88` defines M3 as "counter sensitivity to rule order was never measured before data". Consistent.

VERDICT: agree — "QUALITY 98 (C2) and 99 (M2)": criterion 98 is committed at `fd25213` (`git show fd25213:corpus/QUALITY.md:713-715`, "## Criteria added round 34 — round-33 routed defect 1"); criterion 99 exists in the draft `corpus_QUALITY.md` diff and is correctly labeled a round-34 addition. "FR6 frontier note appended" matches the README hunk in `attempt2-tracked.diff` ("Round-34 Frontier note — FR6 narrowed, not closed").

VERDICT: disagree — `corpus/lessons/round-34.md` cited in SCORECARD "Routed round-33 defects 2–8 landed and judged by non-author seats (`corpus/lessons/round-34.md`)" does not exist at `fd25213` (`git ls-tree` empty) nor on disk; it is a draft-only file (`/fast/scratch/.../corpus_lessons_round-34.md`). Not a factual error — the integration writes it — but the path is dangling as cited; flagged alongside `c1-tip.txt`.

## Disagreement summary

1. `evidence/c1-tip.txt` — file absent on disk and at `fd25213`; the underlying `C1=met` at `fd25213` is evidenced by `wa/ExecRerunLane.md` (uncommitted wave-A report).
2. `corpus/lessons/round-34.md` — absent at `fd25213` and on disk (draft-only); cited as the repair-judgment record.

Both are uncommitted-receipt citations, not wrong values; if the convention is "receipts land at the evidence commit", they are forward references that must exist at integration time — `c1-tip.txt` must be written (or the citation changed to `wa/ExecRerunLane.md`), and `corpus/lessons/round-34.md` must land.

## Residual risk / gaps

- `evidence/c1-after.txt`, `ctl-postdata-shortcut/*`, `wa/*.md` are uncommitted at `fd25213`; the drafts cite them correctly but they must land with the integration.
- The round-33 contract line behind C2's Before cell ("nine pre-data controls had no no-decision control") is a fair paraphrase of contract.md:92-94 ("nine pre-data controls ... a no-decision glossary met it after data"); the round-33 contract's C0 table (`.ufo/waves/round-33/contract.md:66-70`) indeed lists no depth-shaped control — agree, with the note "nine" counts the C0 control rows.
- JudgeLessonItem8's new wrong-detail finding (eight vs nine S117 copies) is a defect in the landed correction block, outside this seat's scope of the SCORECARD/LOG text itself — reported to L1 via this audit.
- Attempt-1 death timestamp `05:25:25Z` and "orchestrator died" could not be re-verified (run logs deleted mid-audit); consistent with provenance receipt times (last draft write 05:25:16Z). Marked [INFERENCE].
