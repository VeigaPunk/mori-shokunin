measured 2026-10-23T07:58:08Z

# ReJudgeLesson8 — re-judgment of round-33.md "### Item 8" (round-34 corrections) + audit of wave-A JudgeLessonItem8

Reviewer: MoriR34A3.ReJudgeLesson8 (UFO-FSD reviewer, wave-B). Target: block `corpus/lessons/round-33.md:253-261` at `8d56809afccefe0ab80c8e73ac3e1ea57c25f5f3`, answering routed defect §8 item 8 of `corpus/lessons/round-33-verifier-spotcheck.md:241-243` (CtlLocatorStale + S117 preamble overstatement). No tool installed/updated (read-only git + read/grep only). No lane writes beyond this report; scratch under `/fast/scratch/hyaku/mori-r34/a3-MoriR34A3.ReJudgeLesson8/`.

## Append-only check (required)

- `git diff f10a320d9056d19a6d007420df49d7b16a3bf857 8d56809afccefe0ab80c8e73ac3e1ea57c25f5f3 -- corpus/lessons/round-33.md` → `1 file changed, 50 insertions(+)`, 0 deletions (verified: `grep -c '^-[^-]'` → 0; `^+[^+]'` → 29 non-blank + lines on 50 added). Deletion count 0 ⇒ no line modified. Confirmed append-only.
- Only commit touching the file in range: `8d56809` (commit msg: "…lesson r33 corrections (pre-judgment)"). Commit times: `f10a320d` 2026-10-23T00:27:16-03:00; `8d56809` 2026-10-23T02:34:40-03:00.

## Independent re-judgment of Item 8 (from committed bytes, before reading wave-A report)

### Sub-block 1 — Locator-address control (round-33.md:255-259)

1. "CtlLocatorStale found that the round-33 counter does not validate the line address in a Gate locator." — supported: receipt table row `.ufo/waves/round-33/w2/CtlLocatorStale.md:23` (M1 "Survived; locator-address coverage residual"); `:82` ("a syntactically valid Gate locator can point past EOF while the counter reports `gate=ok` and `C1=met`; it checks whole-copy quote presence, not the locator's address").
2. "In its synthetic M1 control, `S180.src:21-22` was changed to `S180.src:999999`." — supported: `CtlLocatorStale.md:57` ("the first `S180.src:21-22` became `S180.src:999999`"). Gate row for S180 (`round-33.md:13`) indeed carries `S180.src:21-22`.
3. "the quote remained in the committed copy, and the counter still returned `C1=met` (exit 0)." — supported: `CtlLocatorStale.md:57-81` (quotes/copies/hashes/entry/dispatch/receipt unchanged; output `C1=met`, "Exit 0; survived").
4. "The counter checks quote presence in the whole copy, not within the located line range (`count-c1-a1.py:59,239-242`; `CtlLocatorStale.md:55-82`)." — supported, citations exact: `count-c1-a1.py:59` = `QUOTE_RE` (parses locator shape, captures only quote text); `:239` loads the whole copy (`copy = show(..., f'{COPIES}/{sid}.src')`); `:241-242` = `cok = ... all(norm(q) in copies[sid] for q in located)` (substring over whole copy). Lane counter sha256 = `9ec4d87c4eee79b2ef27b60f3f2b7ae73ee8d5bf2d3f2a73b19526b04145eda6`, matching the receipt's named hash. M1 section = receipt lines 55 (header)–82 (conclusion).
5. "Thus a passing counter does not establish that a `file:L` locator addresses the quote." — supported (`CtlLocatorStale.md:82`: "Do not equate passing this counter with re-locating evidence").
6. "This is a counter residual demonstrated with synthetic data, not evidence that a live lane locator is false." — supported (`CtlLocatorStale.md:82`: "a counter residual rather than a demonstrated bad locator in current lane data"; the M1 run was on the synthetic clone, not lane data).

### Sub-block 2 — S117 recheck-scope clarification (round-33.md:260-261)

7. "Clarification to the §1 preamble at lines 50-53 … it must not be read to say that every page named by every repaired row was committed and checked." — Supported, with the same location nuance the wave-A report notes: the preamble is in the lane lesson `corpus/lessons/round-33.md:50-53` (the Round-32-repair narrative, "copies are committed at `corpus/evidence/recheck-r33/` …"), not in the fleet report — the fleet report `.ufo/reports/round-33/mori.md` (commit `80c1542` at 2026-10-23T00:17:20-03:00, fleet repo) does not contain a §1 S117 preamble at :50-53 and contains no repair narrative. The spotcheck's ":50-51" (`spotcheck.md:147,242`) is the first two lines of that preamble; "50-53" is the fuller preamble span (the S117 table row begins at :57). Statement accurate as a clarification of the phrase's scope.
8. "For S117, the committed `corpus/evidence/recheck-r33/` tree at `89791013` contains copies of nine of the row's ten pages" — **WRONG (defect)**: `git ls-tree -r 89791013 -- corpus/evidence/recheck-r33/` contains exactly EIGHT S117 copies (`S117-README-v1.9.0.src`, `S117-kill-v1.7/1.8/1.9.0.src`, `S117-main-v1.7/1.8/1.9.0.src`, `S117-msg-v1.9.0.src`); `SHA256SUMS` likewise has 8 S117 entries. The S117 source cell (`corpus/SOURCES.md:123` at 89791013) names ten pages: tags API, releases API, main/kill/msg.h/README at v1.9.0, main/kill at v1.8 and v1.7. Nine committed copies exist repo-wide only when adding the tags-JSON copy `corpus/evidence/recheck-r32/S117.src` (verified: file head is the tags-API JSON `[{"name":"v1.9.0","zipball_url":…`). The sentence attributes nine copies to the r33 tree alone — false.
9. "but no copy of the GitHub releases feed/API page." — supported: no releases-feed copy anywhere in the tree (S117 blob grep: 8 r33 copies + `recheck-r32/S117.src` tags JSON; no releases). Verifier agrees (`spotcheck.md:147`).
10. "The release-local literals listed in the S117 table were checked against the committed copies" — supported (spot-verified the eight citation sites of `round-33.md:59`): `S117-main-v1.8.src:382-383` "sending SIGTERM when mem avail <=" / "SIGKILL when mem avail <="; `S117-main-v1.9.0.src:414-415` same; `S117-main-v1.7.src:326-327` "mem <="; `S117-kill-v1.7.src:167,377` "escalating to SIGKILL after %.1f seconds" / "sending %s to process … badness %d, VmRSS %lld MiB"; `S117-kill-v1.8.src:230,539` "%.3f seconds" / "oom_score"; `S117-kill-v1.9.0.src:318,627` "%.3f seconds" / "oom_score_adj"; `S117-msg-v1.9.0.src:9-10` `PRIPCT "%5.2lf%%"`; `S117-README-v1.9.0.src:146` padded example `mem avail <=  5.00%`. All resolve.
11. "the cross-release clauses remain unsupported on those copies and unchecked against the missing feed (`round-33.md:59`)" — supported: `round-33.md:59` lists the six cross-release clauses under "unsupported on every page the row names" and states the feed was not committed; no feed copy exists to check against.
12. "S117 remains `not current`." — supported: `round-33.md:59` row verdict "current → not current"; verifier agrees (`spotcheck.md:147`).

VERDICT: repaired — with one wrong detail (statement 8: nine vs eight in `recheck-r33/`; the ninth copy, the tags JSON, lives in `recheck-r32/S117.src`).

## Audit of wa/JudgeLessonItem8.md

Factual claims the round would cite, marked agree/disagree with my evidence:

1. Append-only `+50 −0`: agree (diff --stat: 1 file changed, 50 insertions(+); 0 deletions; the only hunk is the appended Round-34-corrections section).
2. Commit times block: agree (`7d382043` 2026-10-22T23:21:08-03:00; `89791013` 2026-10-23T00:16:50-03:00; `f10a320d` 2026-10-23T00:27:16-03:00; `8d56809` 2026-10-23T02:34:40-03:00 — all re-verified).
3. Claims 1-6 (CtlLocatorStale M1 facts): agree (same receipt/counter bytes; `:23` table row; `:57` mutation; `:57-81` output; `count-c1-a1.py:59,239-242` verified exact; receipt's own `:59,223-242` is the broader span; M1 section = lines 55-82).
4. Claim 7 (§1 preamble at :50-53): agree in substance and in the cited preamble lines; minor incompleteness — neither the wave-A report nor the block names the file, and the fleet report carries no such preamble; the preamble cited is the lane lesson's Round-32-repair narrative at `round-33.md:50-53` (the S117 table row at :57). This is a location gap, not a factual error, and it is mine as well.
5. Claim 8 (recheck-r33 contains nine of ten S117 pages = DEFECT): agree (independent ls-tree count: 8 copies in `recheck-r33/`; tags JSON at `recheck-r32/S117.src`; row names ten pages per `SOURCES.md:123`).
6. Claim 9 (no releases-feed copy): agree (whole-tree grep; tags JSON confirmed; verifier `spotcheck.md:147`).
7. Claim 10 (eight citation sites resolve): agree — all eight independently spot-verified at the exact lines (incl. `kill-v1.7.src:167,377`, `msg-v1.9.0.src:9-10`, `README-v1.9.0.src:146`, `main-v1.8.src:382-383`, `main-v1.7.src:326-327`, `kill-v1.8.src:230,539`, `kill-v1.9.0.src:318,627`, `main-v1.9.0.src:414-415`).
8. Claim 11 (cross-release clauses unsupported/unchecked): agree (`round-33.md:59`; no feed copy).
9. Claim 12 (S117 remains not current): agree (`round-33.md:59`; `spotcheck.md:147`).
10. VERDICT "repaired" with the one wrong count: agree (matches my independent c).

## Audit of <report>

AUDIT: agree 10 / disagree 0

## Residual risk / verification gaps

- The counter binary was not re-run (mutation M1 outcome is attested by the committed receipt, whose counter hash matches the lane's; the block's claims are byte-level and were cross-checked against receipt and counter source).
- Live-fetch of the GitHub releases API was not attempted; only its absence as a committed copy is asserted and verified.
- Statement 8's count error does not change the repair's substance (feed never committed; nine of ten pages copied repo-wide), but it is an inaccuracy in the round's own corrective record, carried verbatim from `round-33.md:59`/spotcheck. The attempt-2 draft corrects it: `corpus_lessons_round-34.md:117-118` ("read 'contains copies of nine of the row's ten pages' as 'contains copies of eight of the row's ten pages; a ninth, the tags JSON, is `corpus/evidence/recheck-r32/S117.src`'") — accurate.
