# S128 routed repair findings

## Outcome and evidence boundary

- Applied the frozen R-R rule in `.ufo/waves/round-33/contract.md:85-92`: an individual teach needs a quote in a committed copy of a URL named by the row, and `current` requires the population page alone to support every teach clause. The round-32 receipt records S128 as `current` (`corpus/lessons/round-32.md:52`); the closure identifies the population gaps as `totalpages/1000` and the read-only `[0,2000]` export (`corpus/lessons/round-32-verifier-spotcheck.md:90`).
- S128's source cell names the two man7 URLs at `corpus/SOURCES.md:134`. The round-32 population method selected only the first URL (`corpus/evidence/recheck-r32/README.md:35-36`), so committed `corpus/evidence/recheck-r32/S128.src` is the `proc_pid_oom_score_adj(5)` page (title at `S128.src:8`). The second URL was already present in S128; the URL search returned that row, so it is not a new source.
- Opened `https://man7.org/linux/man-pages/man5/proc_pid_oom_score.5.html` twice with `curl -sSL --fail -m 60`, writing unchanged responses to `/fast/scratch/hyaku/mori-r33/RepairS128/proc_pid_oom_score.fetch1.src` and `...fetch2.src`. `date -u +%FT%TZ` immediately before each fetch returned `2026-10-23T02:40:28Z`; both requests succeeded on attempt 1. `sha256sum` returned `6169628d8a2cdc512795cfda74f3598d5b7a25e5b71921d4088c0539cf71b2bc` for each file. Metadata is in the matching `.meta` files under the same scratch directory. This second-page copy is scratch-only, not a committed copy, so its quotes are observations for the draft and do not yet satisfy R-R's committed-copy condition.
- No product file, source row, Gate row, commit, or judge receipt was changed; this report is the sole lane write. No tool was installed or updated. No counter, judge, build, or test was run. Round-32 C1 remains a miss as required by the contract (`.ufo/waves/round-33/contract.md:90-92`).

## Teaches-cell clauses under R-R

Population-page quotes below refer to committed `corpus/evidence/recheck-r32/S128.src`. The second-page quotes refer to the fetched scratch copy and are not committed evidence yet.

| Teach clause (split) | Located page text | R-R result |
|---|---|---|
| The two proc files are different contracts. | Population `S128.src:102-103` describes only adding `oom_score_adj` to badness. The second URL says `proc_pid_oom_score.fetch1.src:73-75` (23 words): "This file displays the current score that the kernel gives to this process for the purpose of selecting a process for the OOM-killer." | Unsupported on the population page: it does not give the second file's contract. The scratch second-page quote is not yet in a committed copy. |
| `oom_score_adj` accepts `-1000..+1000` and is a user-space preference. | Population `S128.src:104-106` (19 words): "Acceptable values range from -1000 (OOM_SCORE_ADJ_MIN) to +1000 (OOM_SCORE_ADJ_MAX). This allows user space to control the preference for OOM-killing," | Supported by the population page. |
| `oom_score_adj` is writable. | Population `S128.src:126-127` (13 words): "Writing to /proc/pid/oom_score_adj or /proc/pid/oom_adj will change the other with its scaled value." | Supported by the population page. |
| The kernel scales the adjustment by `totalpages/1000`. | No quote in population `S128.src:72-132` states that formula. The S128 anchor points to S127 kernel-code locations, including `base.c`'s formula, but those are not either man7 page named in S128's source cell (`corpus/SOURCES.md:134`). | Unsupported under R-R; an anchor or companion code row cannot replace the population-page quote. |
| `oom_score` is a displayed/exported score. | The population page does not document the second file. The fetched second URL says `proc_pid_oom_score.fetch1.src:73-75` (23 words): "This file displays the current score that the kernel gives to this process for the purpose of selecting a process for the OOM-killer." | Unsupported for `current` on the population page. The second URL text would support the display clause only after a committed copy is supplied. |
| `oom_score` is read-only. | No quote in the population page's text at `S128.src:72-157` states read-only access. The second-page description at `proc_pid_oom_score.fetch1.src:72-99` describes the displayed score and its factors, but does not state a read-only mode. | Unsupported. Absence from the inspected description is not affirmative support. |
| `oom_score` has range `[0,2000]`. | No quote in either inspected manual-page description (`S128.src:72-157`; `proc_pid_oom_score.fetch1.src:72-99`) states this range. S128's anchor attributes `[0,2000]` to S127 `base.c` comments, not to either S128 URL (`corpus/SOURCES.md:134`). | Unsupported under R-R. |
| The `oom_score` export reflects the adjustment. | The second URL says `proc_pid_oom_score.fetch1.src:97-98` (16 words): "The oom_score also reflects the adjustment specified by the oom_score_adj or oom_adj setting for the process." Population `S128.src:102-103` speaks of the adjustment being added to badness, not that the `oom_score` export reflects it. | Unsupported for population-page-only `current`; the second URL quote is scratch-only pending a committed copy. |
| The inheritance sentence belongs to the legacy `oom_adj` paragraph, not the `oom_score_adj` description. | Population `S128.src:145-146` (8 words): "a new process inherits its parent's oom_adj setting." The paragraph heading identifies `/proc/pid/oom_adj` at `S128.src:134`. | Supported as page attribution. |
| The privilege sentence belongs to the legacy `oom_adj` paragraph, not the `oom_score_adj` description. | Population `S128.src:147-149` gives the complete privilege sentence, including its exception (full corrected Q3 quote below); its paragraph heading is `S128.src:134`. | Supported as page attribution, provided Q3 is not cut before the exception. |

The fetched second manual describes a display and adjustment reflection, but its DESCRIPTION does not state `read-only`, `[0,2000]`, or `totalpages/1000` (`proc_pid_oom_score.fetch1.src:72-99`). The stronger assumptions are not supplied by the population page; the existing closure names the two central omissions at `corpus/lessons/round-32-verifier-spotcheck.md:90`. Therefore S128 cannot remain `current` under R-R even if the second URL is later committed: the population page still lacks multiple teaches-cell clauses.

## Defect 4: corrected Q3

Round-32 Q3 ends after "to update this file", omitting the exception identified by the closure (`corpus/lessons/round-32.md:52`; `corpus/lessons/round-32-verifier-spotcheck.md:193-194`). Replace it with the complete sentence at committed `S128.src:147-149`:

> "A process must be privileged (CAP_SYS_RESOURCE) to update this file, although a process can always increase its own oom_adj setting (since Linux 2.6.20)."

This is 23 lexical words in rendered text; the earlier quote audit counts 25 whitespace tokens when the parenthesis marks are split (`.ufo/waves/round-32/r1/AttackQuoteBounds.md:22`). It meets the 25-word limit and retains the exception; no shorter-clause fallback is needed.

## Draft correction rows and paragraph

| Draft row | Correction text |
|---|---|
| S128 teaches/current | Under R-R, mark the round-32 `current` verdict unsupported: the committed population page supports the range/preference/writing and the legacy `oom_adj` placement, but not `totalpages/1000`, the read-only `[0,2000]` `oom_score` export, or the export's adjustment reflection. The second URL's fetched page supports display and adjustment reflection only; commit its source copy before treating those two quotes as admissible, and do not use it to satisfy the population-page-alone condition. |
| S128 Q3 | Replace the truncated quote with `S128.src:147-149`: "A process must be privileged (CAP_SYS_RESOURCE) to update this file, although a process can always increase its own oom_adj setting (since Linux 2.6.20)." (23 rendered words; 25 normalized tokens per the existing quote audit). |

Correction paragraph: S128's round-32 `current` label is unsupported under the frozen R-R rule because the first-URL population copy does not state the code-level `totalpages/1000` scaling or the `oom_score` read-only `[0,2000]` range/export; the row's second URL, fetched here, states only that the file displays a current score and reflects the adjustment, and is not yet present as a committed copy. Record the row-level correction without changing round-32 C1's miss, and replace Q3 with the full privilege sentence so it preserves the source's exception (`.ufo/waves/round-33/contract.md:85-92`; `corpus/lessons/round-32-verifier-spotcheck.md:90,193-194`).

## Touched surfaces and limits

- Lane write: `.ufo/waves/round-33/w1/RepairS128.md` only.
- Scratch fetches and metadata: `/fast/scratch/hyaku/mori-r33/RepairS128/proc_pid_oom_score.fetch1.src`, `proc_pid_oom_score.fetch2.src`, and their `.meta` files.
- Read-only evidence consulted: `corpus/SOURCES.md:134`, `corpus/evidence/recheck-r32/S128.src`, `corpus/evidence/recheck-r32/README.md:35-36`, `corpus/lessons/round-32.md:52`, `corpus/lessons/round-32-verifier-spotcheck.md:90,193-194`, `.ufo/waves/round-32/r1/AttackQuoteBounds.md:17-22`, and `.ufo/waves/round-33/contract.md:85-99`.
- Out of scope: no rewrite of the S128 registry row or old lesson, no new source ID or Gate row (the second URL is already registered at `corpus/SOURCES.md:134`), no application of the correction, no judge/counter execution, and no commit or push.
