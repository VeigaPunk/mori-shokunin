# TokUnitOOS: C1 token classification (round 20)

Status: complete. Scope: the one token assigned, `+FINDING:UNIT_FAILURE_OUT_OF_SCOPE` (listed unclassified in `.ufo/waves/round-20/evidence/c1-drift-entering.json`).
Lane HEAD `e4d9384`. Census `tools/mori-census.sh` sha256 `87b8d680b9b2572e…`, identical at the receipt commit `2061780117e6…` (`git diff` empty). Read-only. No census run. No subagents. No tool installs or updates.

## 1. Result (JSON-ready)

token|class|reason|evidence
---|---|---|---
+FINDING:UNIT_FAILURE_OUT_OF_SCOPE|live-state|Baseline logic reproduces it on today's host. The r10 predicate (text lines matching "Failed with result" or "Unit entered failed state", minus fleet-marker lines) counts 270 minus 0 = 270 in the current boot (since 2026-10-20 09:57:08), so that logic would print this finding now. The r10 baseline's boot had no non-fleet line, so the + token is a state difference. The r13/r14 predicate change (text to MESSAGE_ID-structured subject triage) is intended and documented but outcome-neutral on this state: structured non-fleet 270, fleet 0, unknown 0. Fleet token list identical at r10 and HEAD; no roster input. Not a regression.|tools/mori-census.sh:1491-1493 (emit gate and line, user scope), :1409-1420 (structured count, nonfleet=vec[2] at :1420), :1122-1136 (subject classifier), :1121 (FLEET_UNIT_TOKENS), :2812 (drift id); baseline corpus/evidence/baseline-r10-20261015T2231Z.json:2-3 (census d7710981, pinned 2026-10-15T22:26:29Z), :24-39 (no UNIT_FAILURE_* line); 5be8943:tools/mori-census.sh:766-767,783-784 (r10 text predicate; sha d7710981 equals baseline header); 486a4e3 (r1 text emission); 18d7d55 (r13 emission removed; census sha 39abda0a has zero OUT_OF_SCOPE matches; .ufo/waves/round-13/build/CensusFix.md:110 "retired as text"); 8d22d18 (r14 structured re-emission, census lines 1279/1281); LOG.md:766-768 and SCORECARD.md:745-747 (r14 intent); corpus/knowledge/journal-alarm-routing-r14.md:120-122; corpus/QUALITY.md:72; live count-only 2026-10-21T07:35:16-03:00 (r10 text 270/0; structured total 270, nonfleet 270, fleet 0, unknown 0; system 0); corpus/evidence/drift-r12-20261019T2204Z-classification.md:29,31 (live-state, Regression No); LOG.md:558-562 and corpus/lessons/round-12.md:38 (M15 baseline aging)

JSON:

```json
[{"token":"+FINDING:UNIT_FAILURE_OUT_OF_SCOPE","class":"live-state","reason":"Baseline logic reproduces it on today's host: the r10 text predicate counts 270 minus 0 = 270 non-fleet unit-failure lines in the current boot (since 2026-10-20 09:57:08); the r10 baseline boot had none. The r13/r14 structured predicate change is intended and documented but outcome-neutral here (structured non-fleet 270, fleet 0, unknown 0). Fleet token list identical; no roster input. Not a regression.","evidence":["tools/mori-census.sh:1491-1493","tools/mori-census.sh:1409-1420","tools/mori-census.sh:1122-1136","tools/mori-census.sh:1121","tools/mori-census.sh:2812","corpus/evidence/baseline-r10-20261015T2231Z.json:2-3","corpus/evidence/baseline-r10-20261015T2231Z.json:24-39","git 5be8943:tools/mori-census.sh:766-767,783-784","git 486a4e3 (r1 text emission)","git 18d7d55 (r13 emission removed)","git 8d22d18 (r14 structured re-emission, census lines 1279,1281)",".ufo/waves/round-13/build/CensusFix.md:110","LOG.md:766-768","SCORECARD.md:745-747","corpus/knowledge/journal-alarm-routing-r14.md:120-122","corpus/QUALITY.md:72","live count-only 2026-10-21T07:35:16-03:00","corpus/evidence/drift-r12-20261019T2204Z-classification.md:29","LOG.md:558-562","corpus/lessons/round-12.md:38"]}]
```

## 2. Decision test

The class turns on one question: would the baseline's own census logic print this finding on today's host? If yes, the token is state. If no, the logic change is the cause.

- Baseline logic (census d7710981, commit 5be8943): text grep count `c_unit` at :766 and fleet subset `c_unit_fleet` at :767 on `journalctl --user -b --no-pager` (:731, :741). Gate `c_unit > c_unit_fleet` at :783 emits the finding at :784.
- Today, same boot (uptime -s = 2026-10-20 09:57:08): `c_unit` = 270, `c_unit_fleet` = 0, so the gate is true and the baseline logic would emit `UNIT_FAILURE_OUT_OF_SCOPE count=270`.
- HEAD structured logic (census 87b8d680): total 270, one-subject non-fleet 270, fleet 0, neither-or-both subject 0. Same outcome on the same journal.
- Conclusion: the host state produces the token. The predicate change does not change its outcome on this state.

Count-only reads, 2026-10-21T07:35:16-03:00, `journalctl --user -b` and `--system -b`, no message text printed:
- `journalctl --user -b --no-pager | grep -ciE 'Failed with result|Unit entered failed state'` = 270
- same, fleet-marker subset = 0
- `journalctl --user -b -q -o json --output-fields=_BOOT_ID,MESSAGE_ID,UNIT,USER_UNIT,UNIT_RESULT MESSAGE_ID=d9b373ed55a64feb8242e02dbe79a49c | jq -s` = total 270, both-or-neither 0, non-fleet 270, fleet 0. This is a simplified one-subject filter, not the census's JOURNAL_JQ_UNITS run.
- system scope, same MESSAGE_ID = 0

The drift tokens agree: no `+FINDING:UNIT_FAILURE_JOURNAL`, `_UNATTRIBUTED_JOURNAL` or `_SYSTEM` variant in the entering receipt.

## 3. Commit history (`git log -S UNIT_FAILURE_OUT_OF_SCOPE --oneline -- tools/mori-census.sh`)

Three commits: 8d22d18 (round-14), 18d7d55 (round-13), 486a4e3 (round-1).
- 486a4e3 (round-1): text-based emission added, `count=$((c_unit - c_unit_fleet))`.
- 5be8943 (round-10 pin): same text predicate, lines 766-767 and 783-784. Its sha d7710981 equals the baseline header.
- 18d7d55 (round-13): text emission removed. Census sha 39abda0a (= c13df48) has no OUT_OF_SCOPE emission at all; user and system unit records go to `UNIT_FAILURE_JOURNAL(_SYSTEM)` (census-c13df48 :1026-1027, :1101-1106).
- 8d22d18 (round-14): structured fleet / non-fleet / unattributed routing restored. OUT_OF_SCOPE re-emitted at census-r14 lines 1279 (user) and 1281 (system).
- 26f6589, 273aa74, 2be8294, fe9fa90 (round-15/17): `git diff 8d22d18 HEAD` has no +/- line touching OUT_OF_SCOPE, the nonfleet count mapping, the JOURNAL_JQ_UNITS definition, or `def subject`/`def fleet`. Post-r14 changes are positive-subset, OOM, kill and silence rows.

## 4. Intent lines

- Round-13 rejected: LOG.md:291-300 ("collapsed the fleet/non-fleet UNIT_FAILURE_* split together with its tsukuroi owner routing"). Retirement row: .ufo/waves/round-13/build/CensusFix.md:110.
- Round-14 restore: LOG.md:766-768 ("separately route non-fleet UNIT_FAILURE_OUT_OF_SCOPE to tsukuroi"); SCORECARD.md:745-747; corpus/knowledge/journal-alarm-routing-r14.md:120-122 (non-fleet rule); corpus/QUALITY.md:72 (criterion 30).
- Round-12 class for this token: LOG.md:558-562 ("baseline aging across the 2026-10-19 boot; class in corpus/lessons/round-12.md#M15"); corpus/lessons/round-12.md:38 (M15: "Baseline aging was realized; re-pin is not a recorded act").

## 5. Comparison with older classifications

(a) Round-13 register, `.ufo/waves/round-13/evidence/drift-classification.json`: no row for this token, and `unclassified` is empty for its own output. Agree/disagree: not comparable, so no conflict either way.
- Why there is no row: at its measurement (census sha 39abda0a = c13df48; capture `live-measurement.json` captured_utc 2026-10-20T04:33:14Z, boot 430d3038…), the census had no OUT_OF_SCOPE emission, and the user and system `unit_failure_record` counts were 0. So the token could not appear in that output. This is an expected silence, not a missed classification.
- I disagree with extending the register's schema label ("intentional journal schema/version/mask change", used for SEGFAULT_JOURNAL and the journal.* tokens) to this token. That label fits tokens whose outcome changed with the schema. Here the outcome is unchanged on the measured state.

(b) Round-12 receipt, `corpus/evidence/drift-r12-20261019T2204Z-classification.md:29`, with LOG.md:558-562 and M15: agree on class (live-state, Regression No). The count moved from 3 (boot 2026-10-19 08:11:44, measured 22:03:56Z, :31) to 270 (boot 2026-10-20 09:57:08, measured 07:35 on 2026-10-21). The r12 receipt cites census base 20e2255 at sha d7710981, the same predicate as r10 (line 3). That makes the r12 classification correct for r12, and it now also holds under the r14 predicate on today's state.

## 6. Rejected classes

- census-schema-change: rejected. The r13/r14 predicate change is intended and documented, but it does not cause this token here. Both predicates give 270 on the same journal, fleet 0 both, unknown 0 both. The class would apply only if the outcomes diverged. Falsifier: a later run where the r10 text count is 0 while the structured non-fleet count is above 0 (or the reverse) would reclassify this token as census-schema-change if documented, or census-regression if undocumented.
- census-regression: rejected. The emission is restored intentionally (LOG.md:291-300, :766-768), is covered by selftest assertions (census :3646, :3663), and matches the r10 outcome on today's state.
- roster-change: rejected. FLEET_UNIT_TOKENS is a fixed literal (census :1121; r10 :767 is the same token set inline). The r12 roster change (SCORECARD.md:613) touches SURFACE lane rows, not unit-failure subjects.

## 7. Caveats

- The class is boot-scoped. The token flipped between boots: r12 (2026-10-19 08:11:44) had 3, the r13 capture boot 430d3038 had 0, and the current boot (2026-10-20 09:57:08) has 270. A re-pin now would pin a 270-record, boot-specific finding into the baseline, and the next reboot can remove it again. That is the r12 M15 aging pattern, a re-pin policy question for L1, not a census defect.
- The equivalence of the text and structured predicates is measured on this boot only. Generalizing it to future boots is [INFERENCE].
- The entering receipt records tokens only, not the census's count value. The 270 is my independent count at 07:35 on the same boot. The census count at 07:18 is [INFERENCE] close to it.

## 8. Bounds and disclosures

- Bounds deviation: one broad `_grep` (pattern OUT_OF_SCOPE and related terms, path = lane root, gitignore false) matched text inside `.ufo/interactive-sessions/*.jsonl` retained transcripts and printed snippets in its output. I did not open any transcript. Nothing from those snippets is cited or used. All evidence above comes from tools/, corpus/, LOG.md, SCORECARD.md, `.ufo/waves/round-13/` and `.ufo/waves/round-14/` build notes, and read-only git and journal queries.
- Host reads: count-only `journalctl --user` and `--system` queries, `uptime -s`, `jq -s` counts. No journal message text printed. Not a census run.
- Git: read-only only (`log -S`, `show`, `diff`, `cat-file`, `merge-base --is-ancestor`, `rev-parse`). No mutating git or jj command. `tools/mori-census.sh` untouched.
- Scratch: I extracted git-object copies of census versions and diffs into `build/TokUnitOOS/` for grep, then removed them. They are regenerable with `git show <rev>:tools/mori-census.sh`.
- Tools: no installs or updates. jq and journalctl were already present.

## 9. For L1

- Register row: `+FINDING:UNIT_FAILURE_OUT_OF_SCOPE` → `live-state`, with the evidence pointers in section 1.
- Not census-regression, so it does not block a re-pin by itself. Re-pin timing is L1's call, subject to the boot-scoping caveat in section 7.
- No checks are required from me. After registering this row, the contract counting command should drop this token from the unclassified count.
