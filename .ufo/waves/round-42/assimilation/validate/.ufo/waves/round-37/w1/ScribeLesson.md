# Round 37 lesson audit — ScribeLesson

**Item attacked:** Gate quote anchors and Mistakes-row capture/fix evidence in `corpus/lessons/round-37.md`.
**Axes:** copy fidelity; evidence-to-capture/fix traceability.

## Gate quotes

| Row | Copy check | Result |
|---|---|---|
| S221 | `corpus/evidence/sources-r37/S221.src:7232-7234` | Quote matches; 25 words. |
| S222 | `corpus/evidence/sources-r37/S222.src:5031` | Rendered quote matches; 23 words. |
| S223 | `corpus/evidence/sources-r37/S223.src:1140-1142` | Quote matches through “without confirmation”; 23 words. |
| S224 | `corpus/evidence/sources-r37/S224.src:217-218` | Quote matches; 20 words. |
| S225 | `corpus/evidence/sources-r37/S225.src:8355-8356` | Quote text matches; 9 words, but the lesson cites only `S225.src:8355`. That line ends “then return a”; “network error” is on line 8356. Thus the cited location does not cover the complete quote. **Unresolved Gate row.** |

The source-copy checks above were reads, not fetches or freshness measurements. S225’s rendered text is contiguous across the HTML markup, but its current line anchor is incomplete.

## Mistakes rows

All six rows were checked against their cited code, receipts, or reports. Existing counter/selftest receipts were read, not re-run.

- **M1 — captured by the mutation probe; fix resolves.** The named pre-fix scratch transcript is not path-identified in the lane artifacts, so that historical traceback is not independently checked here. The fix is present at `tools/mori-source-drift.py:402-411` (literal 4 MiB body). Recorded run `python3 tool-capmut.py --selftest` in `w1/MutC2CapArm.md:155-164` reports `selftest huge_cap FAIL (over_cap=body at_cap=body len=4194304)` and `EXIT=1`; `evidence/c2-after.txt:4` independently records `check cap_kill PASS (exit=1 huge_cap=FAIL)`. The corrected arm is shown able to fail.
- **M2 — captured by the counter’s wrong-arm detail; fix resolves.** The frozen fixture now prints the 18 `changed` lines (`.ufo/waves/round-37/fixtures/memo-n1.py:34-37`). Recorded command `python3 .ufo/waves/round-37/count-c1.py e57c58b57c025364e79d130fbdf764d2674d83d6` → `evidence/c1-after.txt:3-14`: blind 24/24, real pass, challenge pass, memo negative rejected on `challenge: lists differ`, `C1=met`, `EXIT=0`. The before control `python3 .ufo/waves/round-36/count-c2.py bf0df77 --tool .ufo/waves/round-37/fixtures/memo-n1.py --seed 11` → `evidence/c1-before-memo.txt:8-10`: `C2=met`, `EXIT=0`. This supports the stated old-gate failure; the earlier wrong-arm diagnostic itself is not in that receipt.
- **M3 — captured by r36 `w2/MutC2Deleted`’s recorded limit; fix resolves.** The cited report’s limit is explicit at `.ufo/waves/round-36/w2/MutC2Deleted.md:246-251`: the old counter compares only the summary and does not check required `deleted <id>` lines. `QUALITY.md:862-868` adds the criterion. The old-control command `python3 .ufo/waves/round-36/count-c2.py bf0df77 --tool .ufo/waves/round-37/fixtures/summary-only.py --seed 12` → `evidence/c1-before-summary.txt:8-10`: `C2=met`, `EXIT=0`; the C1 receipt rejects `summary-only.py` for per-id lines (`c1-after.txt:13`).
- **M4 — captured by r36 `w2/ExecCensusRegression`; fix resolves.** The round-36 collateral note at `corpus/lessons/round-36.md:72-80` records the pre-fix `tools/mori-round17-jj-regressions.py --selftest` result: 9/204 red, all `jj_config_redirected`. The scoped assertion is present at `tools/mori-round17-jj-regressions.py:1040-1069`. Recorded post-fix `tools/mori-round17-jj-regressions.py --selftest` → `evidence/r17-jj-selftest-r37.txt:1-2`: `SELFTEST ok`, `EXIT=0`.
- **M5 — captured by the post-commit status sweep; fix resolves.** The lesson records the pre-fix `git status --porcelain` output `?? corpus/evidence/sources-r37/S225.src`. I ran read-only `git -C /home/vgpnk/Projects/shokunin/mori-shokunin ls-tree 52d636d5 corpus/evidence/sources-r37/`; observed all five `S221.src`–`S225.src` entries. The quoted pre-fix status is recorded inline in the lesson, not in a separate receipt.
- **M6 — captured by the two name-status sweeps; fix resolves.** `w1/SentScope.md:14-17` and `w1/ScoutCensusSurfaces.md:26-30` record both `.pyc` additions at the scored tip. Read-only `git ls-tree -r e57c58b57c025364e79d130fbdf764d2674d83d6 .ufo/waves/round-37/__pycache__` confirmed both files. `git check-ignore -v .ufo/waves/round-37/__pycache__/x.pyc` → `.gitignore:3:__pycache__/ …/x.pyc`. `git ls-tree bcf65505 .ufo/waves/round-37/__pycache__` and `git ls-tree HEAD .ufo/waves/round-37/__pycache__` produced no entries; `git rev-parse HEAD` → `0a05f7e6765b025c321bc0b71bb1f44e2600d591`. The ignore rule and post-fix absence are confirmed.

## Scope and provenance

Read-only review only; no lane files were edited except this report, no tests/counters were run, and no tools were installed. Product remediation is out of scope. The audited surfaces were `corpus/lessons/round-37.md`, the five `corpus/evidence/sources-r37/S###.src` copies, and the cited round-37 receipts/reports and code lines.

**Finding:** S225’s table citation omits line 8356, where the quoted clause ends. The quote itself is present, but the supplied anchor does not resolve its complete text. Other Gate quotes and Mistakes rows’ shown-failure/fix evidence resolve, with the historical transcript limitations stated above.

**Artifact:** `.ufo/waves/round-37/w1/ScribeLesson.md`

VERDICT: FAIL