# Blind-wave mutation findings

Scope: `check-blind-wave.sh`; synthetic inputs were committed only in the isolated clone at `4838b3669bf8c73805acbcac3dfdda6579bbbaec`. The detector’s writer-header and report-reference patterns are at `.ufo/waves/round-29/check-blind-wave.sh:59-64`; its non-writer and writer checks are at `:91-112` and `:115-155`.

## Committed-directory runs

- From the lane, the requested round-28 command (`bash .../check-blind-wave.sh 84abe93e6cde117b0bc86c46e163467596fa19a6 .ufo/waves/round-28/w1 '^CaseA2r'`) printed `blind_violations=38`, including `CaseA2r03.md:187:writer-forbidden-opened-path`, and exited 1.
- From the lane, the requested round-29 command (`bash .../check-blind-wave.sh 8809a3fe1eaa87a0afa177a15263d174378e7462 .ufo/waves/round-29/w1 '^CaseA2(07|10)[a-d]\.md$'`) printed `blind_violations=20`, including seven `writer-missing-files-opened-list` entries and eleven reported non-writer tool-run-output entries, and exited 1.
- Both pristine aggregate runs fail, so under the mutation-test rule they are **inconclusive** as aggregate pass/fail evidence, not mutant kills. Their outputs were rerun after restoration and matched (38 and 20 respectively).

## Synthetic scenarios (pristine outputs; all from the committed sandbox tree)

1. Non-writer `Review.md` cites `mori-oom-killers.py:313-332` (`.../nonwriter-citation/Review.md:3`; the cited tool lines exist at `tools/mori-oom-killers.py:313-332`): `blind_violations=1`, `:3:nonwriter-tool-citation`, exit 1. **Correct catch; no FP/FN.**
2. Non-writer `Review.md` says `KILLERS_QUIET exit 0` (`.../nonwriter-quiet/Review.md:3`): `blind_violations=1`, `:3:nonwriter-tool-run-output`, exit 1. **Correct catch; no FP/FN.**
3. Writer list names `w1/CriticC2Design.md` (`.../writer-forbidden-list/CaseWriter.md:3-4`): `blind_violations=1`, `:4:writer-forbidden-opened-path`, exit 1. **Correct catch on pristine; no FP/FN.**
4. Clean non-writer report has only an unrelated `exit 0` (`.../clean-exit/Review.md:3`): `blind_violations=0`, exit 0. **Correct clean result; no FP/FN.**
5. A writer uses `## Opened files and URLs` with only `corpus/SOURCES.md` (`.../writer-heading/CaseWriter.md:3-4`): pristine prints `blind_violations=1`, `:1:writer-missing-files-opened-list`, exit 1. **False positive**: the valid heading is not accepted by the end-anchored `files_header_re` (`check-blind-wave.sh:59`).

## Mutation, fix probe, and restoration

- Pristine detector SHA-256 was `b0573035ca4f16b8df48d97a074483bcffe1ff92746a3c7046418af29a5d6e0f` (lane file and clone matched).
- One plausible defect mutant changed only `report_ref_re` at line 60 from accepting `w[12]/` to accepting only `w2/`; its SHA-256 was `090fe923c626dd3363ca67fc1b474cdeff3c7a71db5ad6f47f4beee6d20c1387`. On synthetic scenario 3 it changed the expected one violation/exit 1 to `blind_violations=0`/exit 0: **mutant killed** by the writer-path probe (a false negative in the mutant). The round-28 aggregate also fell 38→37 and dropped `CaseA2r03.md:187:writer-forbidden-opened-path`; that report names the out-of-list `w1/CriticC2Design.md` at `round-28/w1/CaseA2r03.md:187-190`. The round-29 aggregate remained 20. The pristine aggregate failures make those aggregate runs inconclusive, but the changed concrete violation is a regression.
- Smallest tested false-positive fix: append `([[:space:]]+and[[:space:]]+urls)?` before the final decoration/whitespace class in `files_header_re` at line 59 (the script lowercases lines at line 89). Candidate SHA-256: `1e8687632975c7e17661c7dcf53bf9056d42b9f98718e5d6a1303ae835934a18`. It changed scenario 5 to `blind_violations=0`, exit 0, while scenario 3 still printed its one forbidden-path violation. On round 28 it produced the same 38 violations and same listed violation lines as pristine; **no new round-28 false negative observed**.
- Restored exact detector bytes: SHA-256 returned to `b0573035ca4f16b8df48d97a074483bcffe1ff92746a3c7046418af29a5d6e0f`, matching the lane file. Restored reruns reproduced the pristine output on round 28, round 29, and all five synthetic cases, including scenario 3 = 1 violation and scenario 5 = 1 missing-list violation.

No tools were installed or updated.