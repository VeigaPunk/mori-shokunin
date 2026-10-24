# S149 repair findings

Axes: source support under R-R; quote completeness; provenance.

## Ruling

S149's round-32 `current` verdict is unsupported under R-R. The population URL is the `oom_score_adj` manual page (round-32 recheck row at `corpus/lessons/round-32.md:54`); its committed copy is `corpus/evidence/recheck-r32/S149.src`. R-R requires page quotes in committed copies and the population page alone to support every teaches clause (`.ufo/waves/round-33/contract.md:85-88`). The row names two manual-page URLs, but its other kernel-file references do not make `fs/proc/base.c` or `mm/oom_kill.c` a population page; the strict spotcheck already records the kernel-path attribution issue (`corpus/lessons/round-32-verifier-spotcheck.md:91`).

## Located page facts and quotes

Population-page facts, stated separately from their quotes:

1. The page documents the adjustment range and user-space preference. `S149.src:104-107` (19 words): "Acceptable values range from -1000 (OOM_SCORE_ADJ_MIN) to +1000 (OOM_SCORE_ADJ_MAX). This allows user space to control the preference for OOM-killing".
2. It says a write through either proc path changes the other value using a scaled value. `S149.src:126-127` (13 words): "Writing to /proc/pid/oom_score_adj or /proc/pid/oom_adj will change the other with its scaled value."
3. The page describes an additional root-related memory allowance. `S149.src:86-88` (20 words): "There is an additional factor included in the badness score: root processes are given 3% extra memory over other tasks."
4. In the legacy `oom_adj` passage, the page states inheritance and the privilege rule, followed by an exception. `S149.src:146-149` (23 words): "A process must be privileged (CAP_SYS_RESOURCE) to update this file, although a process can always increase its own oom_adj setting (since Linux 2.6.20)."

Companion-page facts, from the second URL named by S149. These bytes were fetched to scratch, not committed in the lane, so the quotes are content observations, not R-R-admissible evidence:

1. The page describes `/proc/pid/oom_score` as displaying a process's current selection score. `proc_pid_oom_score.5.html.src:73-76` (23 words): "This file displays the current score that the kernel gives to this process for the purpose of selecting a process for the OOM-killer."
2. It says that score reflects either adjustment setting. `proc_pid_oom_score.5.html.src:97-98` (16 words): "The oom_score also reflects the adjustment specified by the oom_score_adj or oom_adj setting for the process."

The named manual pages do not state the fork-time copy/floor, an unprivileged-write floor, the kernel's `totalpages/1000` formula, a read-only `[0,2000]` export, or the absence of a root allowance in v7.2 `oom_badness`. The score-page quote about displaying a score does not state its permission mode or numeric range. The `only` in the claim that inheritance/privilege wording occurs only in the legacy paragraph is also not stated by a quote. These are unsupported under R-R, not inferred from silence.

## Per-clause R-R review

| S149 teaches clause | Named-page evidence | Result under R-R |
|---|---|---|
| Supersedes S128 / describes what the old row said | Neither manual page states lane row history; no page quote. | Unsupported as a page-teaching clause; keep this as correction history, not source teaching. |
| Inheritance and privilege wording is in the legacy `oom_adj` passage, and only there | Population page quote 4 occurs under the legacy passage (`S149.src:134-149`). It states the inheritance/privilege sentence, but does not state exclusivity. | The placement is visible; the full clause including “only” is unsupported. |
| That placement is a documentation gap, not an absent kernel rule | No quote in either manual page states this assessment. | Unsupported. |
| Kernel copies `oom_score_adj` and its floor at fork | No quote in either named manual page. | Unsupported. |
| Kernel rejects an unprivileged write below `oom_score_adj_min` | No quote in either named manual page. | Unsupported. |
| The two proc files have different documented roles | Population quote 1 describes adjustment as a user-space preference; companion quotes 1-2 describe score display and adjustment reflection, but the companion copy is scratch-only. | Not supported under R-R: the needed companion quote is not in a committed copy, and the population page alone does not state the score-page role. |
| `oom_score_adj` is writable and its accepted values are -1000 through +1000 | Population quotes 1-2 (`S149.src:104-107,126-127`). | Supported by the committed population page. |
| Kernel scales the adjustment by `totalpages/1000` | No quote in either named manual page; quote 2 only says the two settings change with a scaled value. | Unsupported. |
| `oom_score` is a read-only `[0,2000]` export | Companion quote 1 only says the page displays a current score; neither manual quote states read-only access or this range. Companion copy is also uncommitted. | Unsupported. |
| The score includes the adjustment | Companion quote 2 says it reflects the setting, but that quote is from an uncommitted scratch copy and is not the population page. | Unsupported under R-R. |
| The manual documents the 3% root-memory clause | Population quote 3 (`S149.src:86-88`). | Supported by the committed population page. |
| The 3% root term has no implementation in v7.2 `oom_badness` | No quote in either named manual page. | Unsupported. |

The round-32 judge's note that kernel clauses cite S127/S003 is not accurate as an in-cell source attribution: the frozen row has file/path references, while the strict spotcheck says no source IDs occur in the cell (`git show` output for `7d382043:corpus/SOURCES.md`, line 155; `corpus/lessons/round-32-verifier-spotcheck.md:91`; judge reason at `.ufo/waves/round-32/judge/JudgeRecheck.md:76`). In any event, those code paths are not either named manual-page URL and cannot satisfy the population-page test.

## Draft append-only correction rows

| Row | Draft correction |
|---|---|
| S149 | Record `current` as unsupported under R-R: the committed population copy supports only the page-stated adjustment range/preference, the proc-file write/scaled-value wording, the 3% root clause, and the legacy `oom_adj` paragraph wording. Fork copy/floor, unprivileged-write floor, kernel scaling, `[0,2000]`/read-only export, and v7.2 root-term absence remain unsupported. The second URL's text observation is not committed evidence and cannot make the row current. Preserve round-32 bytes and report its C1 miss, per `.ufo/waves/round-33/contract.md:90-92`. |
| S149 Q2 | Replace the clipped quote in `corpus/lessons/round-32.md:54` with `S149.src:146-149` (23 words): "A process must be privileged (CAP_SYS_RESOURCE) to update this file, although a process can always increase its own oom_adj setting (since Linux 2.6.20)." This preserves the exception to the privilege sentence; it concerns the legacy `oom_adj` setting, not an unprivileged write below the `oom_score_adj` floor. |

Append-only correction paragraph: S149 does not meet the strict round-32 `current` definition because its committed population page cannot support the kernel-copy/floor, write-floor, totalpages formula, `[0,2000]` read-only export, or v7.2 root-term-absence clauses. Its manual page does support the documented range/preference and 3% clause, and the full Q2 sentence at `S149.src:146-149` includes the `oom_adj` exception. The row's second manual URL was fetched and says that `oom_score` displays a current score and reflects its adjustment, but that copy is only in scratch and is neither committed R-R evidence nor a substitute for the population page; round 32 remains a C1 miss. (Sources: `corpus/evidence/recheck-r32/S149.src:86-149`; `corpus/lessons/round-32.md:54`; `.ufo/waves/round-33/contract.md:85-92`.)

## Companion fetch / source-opening record

The second URL was checked against `corpus/SOURCES.md` before fetching; it already appears as S128's and S149's companion URL (`corpus/SOURCES.md:134,155`). No new source ID or SOURCES row is drafted. Report-only fetch record:

| Existing row | URL | Fetch time(s), UTC | SHA-256 (both fetches) | Located quotes | Registry action |
|---|---|---|---|---|---|
| S149 companion | https://man7.org/linux/man-pages/man5/proc_pid_oom_score.5.html | 2026-10-23T02:40:18Z; 2026-10-23T02:40:24Z | `6169628d8a2cdc512795cfda74f3598d5b7a25e5b71921d4088c0539cf71b2bc` | `proc_pid_oom_score.5.html.src:73-76` and `:97-98` above | Existing URL; no new row or status change. |

Commands and observed outputs:

- `timeout 60 git -C /home/vgpnk/Projects/shokunin/mori-shokunin show 7d382043:corpus/SOURCES.md` — read-only output; S149 is line 155, with the two man-page URLs and the kernel-path references (line 155 in the captured output).
- `timeout 70 sh -c 'mkdir -p /fast/scratch/hyaku/mori-r33/RepairS149 && date -u +%FT%TZ && curl -sSL --fail -m 60 https://man7.org/linux/man-pages/man5/proc_pid_oom_score.5.html -o /fast/scratch/hyaku/mori-r33/RepairS149/proc_pid_oom_score.5.html.src && sha256sum /fast/scratch/hyaku/mori-r33/RepairS149/proc_pid_oom_score.5.html.src'` — output: `2026-10-23T02:40:18Z`; SHA-256 above.
- `timeout 70 sh -c 'date -u +%FT%TZ && curl -sSL --fail -m 60 https://man7.org/linux/man-pages/man5/proc_pid_oom_score.5.html -o /fast/scratch/hyaku/mori-r33/RepairS149/proc_pid_oom_score.5.html.second.src && sha256sum /fast/scratch/hyaku/mori-r33/RepairS149/proc_pid_oom_score.5.html.src /fast/scratch/hyaku/mori-r33/RepairS149/proc_pid_oom_score.5.html.second.src'` — output: `2026-10-23T02:40:24Z`; both files had SHA-256 `6169628d8a2cdc512795cfda74f3598d5b7a25e5b71921d4088c0539cf71b2bc`.
- `timeout 30 sh -c 'printf "%s\n" "A process must be privileged (CAP_SYS_RESOURCE) to update this file, although a process can always increase its own oom_adj setting (since Linux 2.6.20)." | wc -w'` — output: `23`.

## Surfaces, gates, and limits

- Written surface: this report only, `.ufo/waves/round-33/w1/RepairS149.md`. Scratch copies: `/fast/scratch/hyaku/mori-r33/RepairS149/proc_pid_oom_score.5.html.src` and `.second.src`. The committed population copy remains `corpus/evidence/recheck-r32/S149.src`.
- Read-only surfaces: base S149 source row; round-32 recheck and verifier spotcheck; round-32 judge rationale; round-32 and round-33 contracts; current SOURCES duplicate check.
- No product/source/lesson/judge/counter edits, no lane Git or jj writes, no counter or tests run, and no tool installed or updated (tooling rules read at `/home/vgpnk/.omp/agent/RULES.md`). The L1 must commit any companion-page copy before it can be cited as committed R-R evidence; even then it cannot replace the population-page-only requirement.
- No source row or gate admission is claimed. The report does not claim that the counter was run or that any round-32 verdict changed.
