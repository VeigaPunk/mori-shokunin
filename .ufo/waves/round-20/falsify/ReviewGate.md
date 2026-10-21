VERDICT: PARTIAL

Gate quote lengths HOLD. Gate rows with URL and access date HOLD for every new row. Bounded search 11 arithmetic closes internally, but the entry does not match its cited evidence (scribe count, opened population) and does not record the supersession rows added during review.

## Snapshot
The lane registry and lesson changed four times during this review (S073, S074, S075 rows and the Bounded search 11 correction appended; line numbers shifted). Every result below is for this snapshot:
- corpus/lessons/round-20.md sha256 65c7ad2bca3eb3ab…, 78 lines
- corpus/SOURCES.md sha256 f2ff7d92d9b9ac3a…, 118 lines
Re-run the checks if the L1 edits again.

## 1. Gate quotes <= 25 words: HOLDS
Located-quote word counts (round-20.md Gate table):
- S066 :43 = 15; S067 :44 = 22; S068 :45 = 16; S069 :46 = 17; S070 :50 = 22; S071 :51 = 12; S072 :52 = 14. Maximum 22.
- S073 :47, S074 :48, S075 :49 carry no quote of their own ("Same quote", "Same quote and location as S071", "Same quote and anchors"). They inherit 17, 12 and 22 words.
- Independent count: the seven quotes were written to /tmp/r20-gate/quotes.txt. Command: `while IFS= read -r q; do printf '%s\n' "$q" | wc -w; done < quotes.txt` gave 15 22 16 17 22 12 14, exit 0. Python str.split() agrees.

Borderline readings (not violations under the established convention):
- S067's cell also quotes "It's a trick question." (4 words) as a location label. Summing every quoted string gives 26.
- Whole-cell counts (decision + quote + location): S067 34, S070 27, S073 26, S074 31. The limit is applied to the located quote: accepted rows already exceed 25 whole-cell (round-19.md:42, S064 cell 44 words, quote 13; round-18.md:27, S049 cell 26, quote 19). The frozen contract has no Gate or quote-length rule (read in full, lines 1-117).

## 2. Each new SOURCES row has a Gate row with URL and access date: HOLDS
- S066-S072 (SOURCES:72-78, 11 cells each): one Gate row each (round-20.md:43, 44, 45, 46, 50, 51, 52). Gate URL equals registry URL; Gate access 2026-10-21 equals registry "opened"; tier matches decision (A/B/C = Admit A / Admit B / Reject C).
- Also present: S073 (SOURCES:79, Gate:47), S074 (SOURCES:80, Gate:48), S075 (SOURCES:81, Gate:49). URL and date match.
- Cosmetic: the Gate column reads "Access", not "Access date". S073-S075 sit out of ID order inside the table.

## 3. Bounded search 11 (SOURCES.md:114): arithmetic closes, accounting does not
Closes internally: identified 10 = screened 10; included 6 + excluded-as-row 1 + not-rowed 3 = 10. No single "excluded" total is written (1 + 3 = 4 by sum).

Defects:
(a) Scribe count. Entry: "seven round-20 source scribes (`.ufo/waves/round-20/build/Src*.md`)". The glob returns 6 files: SrcApprovalTests, SrcBashLead, SrcCharacterization, SrcK8sController, SrcPathContainment, SrcPythonLstat.md (exit 0; the build/ root listing shows no other Src-prefixed file). [INFERENCE] a seventh seat wrote no build report.
(b) Opened references missing from the ten:
  - ApprovalTests.Documentation explanations/what_are_approvals.md. Opened by SrcApprovalTests (SrcApprovalTests.md:44, HTTP 200), quoted, screened as "not proposed as a row" (:50-52). Not named in the entry; not among the three not-rowed.
  - os.path (docs.python.org/3/library/os.path.html). Listed under "Sources opened" (SrcPathContainment.md:9), quoted (:19-20), not rowed. The entry says "Python os"; [INFERENCE] it means os.html (S068) only.
  With the Documentation page alone: identified 11, not-rowed 4. With both: 12 and 5. Both close arithmetically; the ten is not the full opened population.
(c) Supersession not reflected. Three supersessions now exist: S073 supersedes S069 (Gate:47), S074 supersedes S071 (Gate:48), S075 supersedes S070 (Gate:49). Bounded search 11 carries one correction, for S073 only (SOURCES.md:114). At reference level the count still closes (pathlib, Kubernetes and Bash are one reference each). At row level it does not: nine new rows (S066-S075); the range "included 6 (S066-S071)" contains the superseded S069, S070 and S071 and excludes S073-S075.
(d) Unit undefined. The GNU Bash manual counts once although seven web URLs were tried and the FTP tarball was opened (SrcBashLead.md:9-18). Feathers' book and the snippet-only blogs were identified but not opened (SrcCharacterization.md:24, 39-40) and are not counted. The entry should say whether unopened candidates count.

## 4. Locator spot-checks on new rows (beyond the three items)
- docs.python.org/3/library/pathlib.html (curl HTTP 200, 271189 bytes; scratch /tmp/r20-gate/pathlib.html): "assumes that no symlinks are present in the path; call resolve() first ..." sits inside `<div class="admonition warning">` under PurePath.relative_to, lines 916-923. S073's corrected locator ("Warning naming walk_up") matches the page. S069's "walk_up paragraph" was a looser locator for the same sentence.
- kubernetes.io controller page (curl HTTP 200, 509019 bytes; /tmp/r20-gate/k8s-controller.html): "responsible for making the current state come closer to that desired state." is the third sentence of "Controller pattern", lines 892-896. S071 and S074 quotes verified.
- Not re-fetched: S066, S067, S068, S070, S072, S075 (scribe-recorded text only). The lesson's claim that the L1 matched every quote byte-for-text was not re-verified beyond these two spot-checks.

## 5. Adjacent defects (outside the three items)
- round-20.md:55-56 says "Status/recheck/used-by changes to existing rows: none", then lists in-place used-by changes. The registry shows them (SOURCES:72, 73, 74, 77, 79, 80 now include corpus/lessons/round-20.md). "Old cells unchanged" is therefore false for used-by cells.
- round-20.md:14 and :16 still cite S069 and S071 as sources for C2 and C1; both are now superseded (S073, S074). Lines seen at the 76-line snapshot; lines above the Gate table were unchanged by later edits.
- The lesson cites a "CORPUS.md tier rule" (Gate:48). corpus/CORPUS.md does not exist at that path (skipped as missing); not checked.

## Recommended for L1 (not applied by me)
1. Add corrections for S074 and S075 to Bounded search 11; restate included and excluded at reference and row level.
2. Decide whether ApprovalTests.Documentation and os.path are identified; update identified, screened and not-rowed (4 or 5).
3. Replace "seven" with the number of Src reports present (6), or locate the seventh.
4. Correct the "none" statement at round-20.md:55-56 to match the in-place used-by edits.

## Tooling and bounds
- Installs or updates: none. Used system curl, wc, tr; the Python eval kernel; read, grep and glob.
- Read only named paths: corpus/SOURCES.md; corpus/lessons/round-18.md, round-19.md, round-20.md; .ufo/waves/round-20/contract.md; .ufo/waves/round-20/build/ (directory listing, Src*.md, head of SourcesRecheck.md); SKILL.md and PROVINCE.md (no quote-length rule). Not opened: .ufo/interactive-sessions/, .ufo/worktrees/, .jj/, ~/.omp.
- No lane file edited. Scratch files: /tmp/r20-gate/ only.
