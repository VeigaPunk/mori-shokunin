# Mo50bScoutQuarantine — quarantine slice re-derivation and collision re-check (a2w1)

Read-only seat. Scratch `/fast/scratch/hyaku/mori-r50/Mo50bScoutQuarantine/` (TMPDIR under it); removed before yield. Lane HEAD seen: `4548a34d` (`487941b9` is its ancestor; `git diff --stat 487941b9 HEAD -- corpus` printed nothing, so `corpus/` is identical to the landed data). Tooling installed: none.

## 1. Quarantine slice (§6 item 10, prompt's awk verbatim, output redirected into scratch)

Register `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md`, sha256 `5afe1810a6c3d62f37987b575a954f5b1197daa23005d4bb2f1d982f64bad833`.

    awk -F'|' -v l='mori' '$2 ~ ("`" l "`") && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/ {print $4, $5}' "$R" > $S/quarantine-slice   # exit 0

Derived (3 lines, `cat -A`):

     S244`   the cited source could not be fetched, so no quote was checked $
     S262`   the cited source could not be fetched, so no quote was checked $
     S268`   the cited source could not be fetched, so no quote was checked $

`diff` against `assimilation/quarantine-slice` → identical (rc 0); both sha256 `8494dc0b4942527cdcc724cf1550653b98be679bd811b74d20e43ce5a6207349`. Raw register rows (`grep -n '`mori`'`): `:356` round1 S244 (DOI 10.1145/3643916.3644413), `:357` round4 S262 (DOI 10.1109/TSC.2026.3698682), `:358` round5 S268 (same DOI). Every line carries an S-id. All three carry the prose class "could not be fetched" (unchecked family → unverifiable, not fabrication). The id cell is the malformed `S244\`` (backtick instead of ` |`) that rounds 44/45 already noted.

## 2. Per row: round-48 verdict, and who cites it

Round-48 verdict from `corpus/lessons/round-48.md:77-84` (unchanged since; `round-49.md:140-146` and `contract.md:137` restate it):

| id | register row | round-48 verdict | lane row | cited by S489-S491 rows or `corpus/knowledge/oom-memcg-stat-r50.md` |
|---|---|---|---|---|
| S244 | `:356` | PRESENT — arXiv 2403.18832 abstract carries "98.9% of commits in our dataset contain sentences with rationale information" (`w1/ScoutQuarantineS244.md`); lane has no S244 row | none (staged S483) | no |
| S262 | `:357` | PRESENT — ROMA, same document as lane S262/S478; quote in publisher PDF fetched with a browser User-Agent (`w1/ScoutQuarantineS262.md`); earlier failure = IEEE bot wall | yes, `corpus/SOURCES.md:243`, `mined`, `used-by corpus/knowledge/oom-victim-context-r41.md` (recheck 180d) | no |
| S268 | `:358` | PRESENT — same ROMA PDF, sha256 `1603404d…`, lines 139-141 (`w1/ScoutQuarantineS268.md`); register row carried no quote, the quote is the renumbered staged S507's | none (staged S507) | no |

Citation check, case-insensitive grep counts over `oom-memcg-stat-r50.md` and over the three rows `corpus/SOURCES.md` S489, S490, S491 (rows `:268-270`), for each pattern `S244`, `S262`, `S268`, `S483`, `S507`, `3643916`, `2403\.18832`, `98\.9`, `3698682`, `ROMA`, `11540439`, `rationale`: **0 in entry, 0 in rows, for every pattern**. `git grep -nE 'S(244|268)\b' 487941b9 -- corpus/SOURCES.md corpus/knowledge` → no output. The entry's `source:` lines are S489, S490, S491 only. Expectation "none" holds. S262 remains cited only by the pre-existing `oom-victim-context-r41.md` row (unchanged).

## 3. Collision check re-run (§6 item 10 commands, outputs into scratch) vs `assimilation/{reg-ids,staged-ids,collisions}`

    grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md | grep -oE 'S[0-9]+' | sort > reg-ids
    grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' $S/merge/mori/SOURCES.append.md | grep -oE 'S[0-9]+' | sort > staged-ids
    comm -12 reg-ids staged-ids > collisions

| file | landed lines | now lines | diff |
|---|---|---|---|
| reg-ids | 261 | 264 | `262a263,264`-style: now adds exactly **S489, S490, S491** (`261a262,264`), nothing else |
| staged-ids | 136 | 136 | identical (rc 0); S471-S606 |
| collisions | 18 (S471-S488) | 21 (S471-S491) | adds exactly S489, S490, S491 |

Explanation: the lane registry grew S489-S491 at `487941b9`; the staged package already carried S489-S491, so the intersection grows by those three ids. The collisions are id-only, not same-document: staged S489 = Alibaba CloudMonitor threshold-alarm doc, staged S490 = proc(5) Japanese (Ubuntu focal), staged S491 = proc(5) zh_TW (Arch) — none adopted — while lane S489/S490/S491 = cgroup-v2.html v7.2 / memcontrol.c v7.2 / oom_kill.c v7.2. The adopted staged row S533 (→ lane S489 "by document") is in no collision (`S533` absent from `reg-ids`; staged S534/S539 not adopted, as in `contract.md:133-139`). The renumber-by-document map therefore stands: staged S533 → lane S489; S490/S491 are lane-original rows (the entry's memcontrol.c and oom_kill.c sources, no staged counterpart). The frozen contract's "18 collisions" figure is the entering-state count and is now stale by 3 (21); the contract is frozen, so this is a named limit, not a fix request.

Corollary for any later round: appending staged S489-S491 as-is would be a duplicate-id (census E03) against the three landed lane rows; the guard (pattern `^ {0,3}\|[[:space:]]*S[0-9]{3,}`) catches it, as the 21-line `collisions` shows.

## Findings

- LOW — `assimilation/quarantine-slice`: re-derived byte-identical (sha256 `8494dc0b…`); 3 rows S244/S262/S268, all unverifiable-class, none fabrication. No defect.
- LOW — `corpus/lessons/round-48.md:77-84`: verdicts PRESENT for all three stand; none of S244, S262, S268 (nor their staged twins S483, S507, nor the DOIs/quote text) is cited by `corpus/knowledge/oom-memcg-stat-r50.md` or `corpus/SOURCES.md` S489-S491. Expected "none" confirmed.
- LOW — `.ufo/waves/round-50/assimilation/{reg-ids,collisions}` and `contract.md:133-134` ("261 registry ids … 18 collisions"): stale after `487941b9` (live: 264 registry ids, 21 collisions; extra S489-S491, all different documents from the staged same-numbered rows). `staged-ids` unchanged. Not a data error; the lane's own S489-S491 rows were appended after the frozen snapshot, as the round's rules allow. Report the 18→21 drift in the L1 lesson if it quotes the counts.
- LOW — `assimilation/guard-proof/` unaffected; guard still catches indented rows (21 hits, includes the new ids).
- LOW — register id cell is malformed (`S244\``); the awk prints the backtick with the id — the slice lines carry it, harmless since the pattern matches `S[0-9]+`.
