measured 2026-10-23T05:39:32Z

# JudgeLessonItem8 — round-33.md "### Item 8" block (round-34 corrections)

Reviewer: MoriR34A2.JudgeLessonItem8 (UFO-FSD reviewer, wave-A). Target: block at corpus/lessons/round-33.md:253-261 (item 8) at 8d56809afccefe0ab80c8e73ac3e1ea57c25f5f3, answering routed defect §8 item 8 of corpus/lessons/round-33-verifier-spotcheck.md:241-243 (CtlLocatorStale + S117 preamble overstatement). Verdict words: `defect`/`no defect found` per statement; final VERDICT: `repaired` / `not repaired`.

No tool installed or updated (nothing needed; read-only git + read/grep only). No lane writes, no scratch files, no subagents. All git read-only.

## Append-only check (required)

- `git diff f10a320d9056d19a6d007420df49d7b16a3bf857 8d56809afccefe0ab80c8e73ac3e1ea57c25f5f3 -- corpus/lessons/round-33.md` ( 1 file changed, 50 insertions(+), 0 deletions(-). The only change is the appended `## Round-34 corrections` section (+ `## Round-34 corrections ...` header, + items 5-8 blocks). Confirm append-only.
- Commit times: `7d382043` 2026-10-22T23:21:08-03:00; `89791013` 2026-10-23T00:16:50-03:00; `f10a320d` 2026-10-23T00:27:16-03:00; `8d56809` 2026-10-23T02:34:40-03:00.

## Item 8, Locator-address control (round-33.md:257)

1. "CtlLocatorStale found that the round-33 counter does not validate the line address in a Gate locator." — supported: `.ufo/waves/round-33/w2/CtlLocatorStale.md:23` (M1 "Survived; locator-address coverage residual"), :82.
2. "In its synthetic M1 control, `S180.src:21-22` was changed to `S180.src:999999`." — supported: `.ufo/waves/round-33/w2/CtlLocatorStale.md:57` ("the first `S180.src:21-22` became `S180.src:999999`").
3. "the quote remained in the committed copy, and the counter still returned `C1=met` (exit 0)." — supported: `.ufo/waves/round-33/w2/CtlLocatorStale.md:57-82` (quotes/copies/hashes unchanged; output `C1=met`, exit 0, "survived").
4. "The counter checks quote presence in the whole copy, not within the located line range (`count-c1-a1.py:59,239-242`; `.ufo/waves/round-33/w2/CtlLocatorStale.md:55-82`)." — supported: `count-c1-a1.py:59` `QUOTE_RE` captures locator syntax + quote text only (line address is not existence-checked); `:239-242` loads the whole copy (`show(..., f'{COPIES}/{sid}.src')`) and tests `all(norm(q) in copies[sid] for q in located)`. Receipt's own implementation cite (`:59,223-242`) is the broader span; the block's `:239-242` is accurate. M1 section = receipt lines 55-82.
5. "Thus a passing counter does not establish that a `file:L` locator addresses the quote." — supported, matches receipt :82 ("Do not equate passing this counter with re-locating evidence").
6. "This is a counter residual demonstrated with synthetic data, not evidence that a live lane locator is false." — supported, receipt :82 ("a counter residual rather than a demonstrated bad locator in current lane data").

Locator sub-block: no defect found.

## Item 8, S117 recheck-scope clarification (round-33.md:259-261)

7. "Clarification to the §1 preamble at lines 50-53" — supported: round-33.md:50-53 hold the preamble ("The clauses were re-checked on the pages each row's own source cell names; copies are committed at `corpus/evidence/recheck-r33/` ..."), which overstates the per-row check; verifier §8 item 8 flags ":50-51" (spotcheck :242-243), block's "50-53" is the fuller preamble span. Statement itself is accurate.
8. "For S117, the committed `corpus/evidence/recheck-r33/` tree at `89791013` contains copies of nine of the row's ten pages" — **wrong (defect)**: `git ls-tree -r --name-only 89791013 corpus/evidence/recheck-r33/` contains exactly EIGHT S117 copies (`S117-README-v1.9.0.src`, `S117-kill-v1.7/1.8/1.9.0.src`, `S117-main-v1.7/1.8/1.9.0.src`, `S117-msg-v1.9.0.src`). The row cites ten pages (SOURCES.md:123): tags API, releases API, main/kill/msg/README at v1.9.0, main/kill at v1.8 and v1.7. Nine of ten copies exist repo-wide only when adding the tags-JSON copy `corpus/evidence/recheck-r32/S117.src` (verified: its head is the tags API JSON, not in the r33 tree). The sentence attributes nine copies to the r33 tree alone; that is false.
9. "but no copy of the GitHub releases feed/API page." — supported: whole-tree grep for `S117` at `89791013` shows no releases-feed copy (only the 8 r33 copies, `recheck-r32/S117.src` = tags JSON, and wave paperwork). Verifier agrees (spotcheck :147).
10. "The release-local literals listed in the S117 table were checked against the committed copies" — supported (spot-verified all eight citation sites of round-33.md:59): `S117-main-v1.8.src:382-383` and `S117-main-v1.9.0.src:414-415` contain "mem avail <="; `S117-main-v1.7.src:326-327` "mem <="; `S117-kill-v1.7.src:167/377` %.1f escalation + badness/VmRSS warn; `S117-kill-v1.8.src:230/539` %.3f + oom_score; `S117-kill-v1.9.0.src:318/627` %.3f + oom_score_adj; `S117-msg-v1.9.0.src:9-10` `PRIPCT "%5.2lf%%"`; `S117-README-v1.9.0.src:146` padded "mem avail <=  5.00%". All resolve.
11. "the cross-release clauses remain unsupported on those copies and unchecked against the missing feed (`round-33.md:59`)" — supported: round-33.md:59 lists the six cross-release clauses under "unsupported on every page the row names"; no feed copy exists to check against.
12. "S117 remains `not current`." — supported: round-33.md:59 row verdict "current → not current"; verifier agrees (spotcheck :147).

## VERDICT: repaired

The routed defect §8 item 8 (locator-address residual + S117 preamble overstatement) is answered correctly and the block is append-only. One statement in the corrective prose is factually wrong: item 8 above — the `recheck-r33` tree at `89791013` contains eight, not nine, of S117's ten page copies; the ninth (tags JSON) lives at `corpus/evidence/recheck-r32/S117.src`. All other statements checked (12/13) are supported by committed bytes.

## Residual risk / verification gaps

- The counter was not re-run (not required: the block's factual claims are all pinned to committed receipt/counter bytes, which I cross-checked directly).
- Live-fetch of the GitHub releases feed was not attempted; the block only asserts absence of a committed copy, which is established from the tree.
- Statement 8's error does not change the repair's substance (feed never committed; nine of ten pages copied repo-wide), but it is an inaccuracy in the round's own corrective record.
