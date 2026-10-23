# Round-32 C1 recheck — S128, S149 (seat Recheck128149)

URL (both ids, exactly the population url): `https://man7.org/linux/man-pages/man5/proc_pid_oom_score_adj.5.html`
Fetch: `curl -sSL --fail -m 60 <url> -o .../S128.src` exit 0, `date -u` at fetch = **2026-10-23T01:31:22Z**. Bytes saved unchanged (11,680 B).
Redirect probe afterwards: `http=200 redirects=0 effective=https://man7.org/linux/man-pages/man5/proc_pid_oom_score_adj.5.html size=11680 type=text/html` — the page did not move.

## 1. Per-id receipts

- **S128** — url https://man7.org/linux/man-pages/man5/proc_pid_oom_score_adj.5.html · accessed 2026-10-23T01:31:22Z · 11,680 B · sha256 769edf3b9c054934db07f16173297fc5fd63c3a4c807682355f08fa45cde80a9 · copy `/fast/scratch/hyaku/mori-r32/Recheck128149/S128.src`
- **S149** — url https://man7.org/linux/man-pages/man5/proc_pid_oom_score_adj.5.html · accessed 2026-10-23T01:31:22Z · 11,680 B · sha256 769edf3b9c054934db07f16173297fc5fd63c3a4c807682355f08fa45cde80a9 · copy `/fast/scratch/hyaku/mori-r32/Recheck128149/S149.src`

Both ids share one population URL, so `S149.src` is a byte-identical copy of the same fetch (rule permits one copy per id).
The sha256 is identical to the sha recorded inside the population row for its 2026-10-22T15:46Z fetch, i.e. the page has not changed since that recording; the accessed stamp above is this round's fresh fetch.
Normalised text used for quoting: `python3 .ufo/waves/round-32/seat-check.py text S128.src` → 5,218 B (saved as `S128.txt`).

## 2. Ready-to-paste rows

```markdown
| S128 | https://man7.org/linux/man-pages/man5/proc_pid_oom_score_adj.5.html | 2026-10-23T01:31:22Z | 769edf3b9c054934db07f16173297fc5fd63c3a4c807682355f08fa45cde80a9 | "Acceptable values range from -1000 (OOM_SCORE_ADJ_MIN) to +1000 (OOM_SCORE_ADJ_MAX)."; "The value of oom_score_adj is added to the badness score before it is used to determine which task to kill."; "a new process inherits its parent's oom_adj setting. A process must be privileged ( CAP_SYS_RESOURCE ) to update this file" | current |
| S149 | https://man7.org/linux/man-pages/man5/proc_pid_oom_score_adj.5.html | 2026-10-23T01:31:22Z | 769edf3b9c054934db07f16173297fc5fd63c3a4c807682355f08fa45cde80a9 | "root processes are given 3% extra memory over other tasks"; "a new process inherits its parent's oom_adj setting. A process must be privileged ( CAP_SYS_RESOURCE ) to update this file"; "Acceptable values range from -1000 (OOM_SCORE_ADJ_MIN) to +1000 (OOM_SCORE_ADJ_MAX)." | current |
```

## 3. Quote → teaches-cell fact

Offsets below are character offsets into the normalised text (`S128.txt`); section spans are `DESCRIPTION` 348–3116, `HISTORY` 3116–4012, `SEE ALSO` 4012–4057, `COLOPHON` 4057–5206.

S128 (teaches: writable -1000..+1000 preference, adjustment added, legacy oom_adj carries the inheritance/privilege sentences):
- `"Acceptable values range from -1000 (OOM_SCORE_ADJ_MIN) to +1000 (OOM_SCORE_ADJ_MAX)."` (offset 1857, inside DESCRIPTION) — bears on "the writable -1000..+1000 preference" and anchor `:104-110`. Present verbatim.
- `"The value of oom_score_adj is added to the badness score before it is used to determine which task to kill."` (offset 1720, INTRODUCTION of the adjustment inside DESCRIPTION) — bears on anchor `:102-103` (adjustment "added") and on the contrast with oom_adj's "scaled linearly" wording at offset 2831, i.e. the two files are indeed described as different contracts.
- `"a new process inherits its parent's oom_adj setting. A process must be privileged ( CAP_SYS_RESOURCE ) to update this file"` (offset 3678, inside HISTORY) — bears on the distinctive clause "the page's inheritance and privilege sentences belong to the legacy oom_adj file, not to oom_score_adj". Evidence of placement: `inherits` occurs exactly once on the whole page (offset 3692) and `privileged` exactly once (offset 3749); both sit after `HISTORY top` (3116) and before `SEE ALSO top` (4012), and the surrounding text is `The default value for this file is 0;` … `, although a process can always increase its own oom_adj setting (since Linux 2.6.20)`. Nothing in DESCRIPTION mentions inheritance or privilege for oom_score_adj.
Verdict `current`: every page-borne assertion of the teaches cell is still present verbatim, including the placement claim that distinguishes S128.

S149 (teaches: supersedes S128; inheritance/CAP_SYS_RESOURCE live only in the oom_adj paragraph as a documentation gap; 3% root clause; the two contracts):
- `"root processes are given 3% extra memory over other tasks"` (offset 1082, DESCRIPTION) — bears on "the pages' 3% root clause (adj:86-88)"; the clause is still stated on the live page (S149 says it has no v7.2 oom_badness implementation, which is a code claim from row S003, not this URL).
- `"a new process inherits its parent's oom_adj setting. A process must be privileged ( CAP_SYS_RESOURCE ) to update this file"` (offset 3678, HISTORY) — bears on "the pages do place them only inside the oom_adj paragraph (adj:145-149)"; single occurrences at 3692/3749 bounded by HISTORY are exactly that placement.
- `"Acceptable values range from -1000 (OOM_SCORE_ADJ_MIN) to +1000 (OOM_SCORE_ADJ_MAX)."` (offset 1828, DESCRIPTION) — bears on S149's restated "writable -1000..+1000 preference" half of the two-contract sentence.
Verdict `current`: the page-borne half of the superseding teaches cell is unchanged and still matches; the code-level half (fork.c copy, base.c floor gate, oom_kill.c scoring) is not served by this URL and cannot be re-opened from this row's url cell.

## 4. seat-check output

```
$ timeout 120 python3 .ufo/waves/round-32/seat-check.py row S128 /fast/scratch/hyaku/mori-r32/Recheck128149/S128.src "$Q128"
sha256=769edf3b9c054934db07f16173297fc5fd63c3a4c807682355f08fa45cde80a9
quotes=3 words=[9, 20, 20] in_copy=[True, True, True]
shared_tokens=['added', 'kill', 'range', 'resource', 'score'] topic_ok=True
live_quotes_ok=True
ROW_CHECK=pass (judge R4 and R5 not checked here)
rc=0

$ timeout 120 python3 .ufo/waves/round-32/seat-check.py row S149 /fast/scratch/hyaku/mori-r32/Recheck128149/S149.src "$Q149"
sha256=769edf3b9c054934db07f16173297fc5fd63c3a4c807682355f08fa45cde80a9
quotes=3 words=[10, 20, 9] in_copy=[True, True, True]
shared_tokens=['range', 'resource', 'root', 'score'] topic_ok=True
live_quotes_ok=True
ROW_CHECK=pass (judge R4 and R5 not checked here)
rc=0
```

`$Q128` / `$Q149` are the quotes cells exactly as in the fenced rows above (also saved verbatim at `/fast/scratch/hyaku/mori-r32/Recheck128149/S128.quotes.txt` and `S149.quotes.txt`). No quote contains `&`, a pipe, a double quote or a zero-width character; the page text contains none of the last two issues (`has zero-width: False`).

## 5. Drift

Neither row drifted and neither was unreachable: both fetches returned HTTP 200 with byte-identical content to the sha already recorded in the population row, so no `Round32` correction is drafted and the used-by files listed in the two rows (`corpus/knowledge/oom-victim-selection-r27.md`, `PROVINCE.md`, `corpus/README.md`, `corpus/lessons/round-28.md`) need no edit on this evidence.

## 6. Bounds / remaining unknowns

- No writes outside this Report and `/fast/scratch/hyaku/mori-r32/Recheck128149/`; no git or jj invoked; no packages installed or updated (nothing needed); no pacman run; no host services touched.
- Remaining unknowns: the `proc_pid_oom_score(5)` page clauses quoted in both teaches cells (`score page:72-80,97-98,120`) are a different URL not in this row's population url cell, and the kernel-code clauses (fs/proc/base.c, kernel/fork.c, mm/oom_kill.c) belong to rows S127/S003 — this seat re-opened only the adj page, so those halves are [INFERENCE] here and were not re-verified.
