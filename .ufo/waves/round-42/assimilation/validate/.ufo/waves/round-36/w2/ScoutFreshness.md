# ScoutFreshness — round 36 freshness sweep (data tip vs entering base)

Attack: freshness of the round's new claims. Every path added or changed at `bf0df77fee4b6ef54a90aea09335c7617f125151` versus `6bd57097f7ab2b471b4593ed2019c980b1368c68` must be tied to a SCORECARD section, a LOG entry, or `corpus/lessons/round-36.md`, and every LOG entry must carry its own re-verification result. Prompt rule: `.ufo/prompts/mori-round-36.md:107-108` (every landed change tied to a LOG.md entry and the commit that carries it).

Axes used: inventory completeness, one-line role from the file or its spec, pointer presence in those three docs, re-verification attached to the entry that states the claim.

No tools installed.

## Measurements

```
git diff --name-status --find-renames 6bd57097 bf0df77fee4b6ef54a90aea09335c7617f125151 | wc -l
→ 118
git log --oneline 6bd57097..bf0df77
→ bf0df77 data
  5842dc0 C1 declared exploratory
  c1a026c C0 receipts + v2 counters
  da12b37 freeze
  c081375 considerthese daily reflection
git show bf0df77:LOG.md | grep -c 'Round 36'
→ 0
grep -n '^## Round' LOG.md | tail -1
→ 2097:## Round 35 (attempt 1, L1 MoriR35) — capabilities register vs the closure record; round-34 repairs
git rev-parse HEAD
→ 5a2fe05d2d403943912b8080ba1477a02cf2e9f5
git status --short
→ ?? .scratch/
  ?? .ufo/waves/round-36/w2/MutC2Deleted.md
  ?? .ufo/waves/round-36/w2/ScribeLesson.md
  ?? .ufo/waves/round-36/w2/SentData.md
  ?? .ufo/waves/round-36/w2/SentTools.md
```

Pointer search was the round-36 LOG slice (from `LOG.md:2109` "- Round 36"), the SCORECARD section from `SCORECARD.md:1999`, and all of `corpus/lessons/round-36.md`. A basename or path hit is "named". A group count is a pointer only when the membership file is named and the absence list matches the files on disk.

At `bf0df77`, SCORECARD and LOG had no round-36 text (also `w2/RevReportSections.md:44-45`, `w2/RevSHONEN.md:27-28`). Integration commits after the data tip (`9ca8f2e`, `6827d6e`, `8ff9bba`, `5a2fe05`) added the prose below. The defects are what that prose still does not bind.

## Defects

1. The round-36 LOG text is not a LOG entry. `LOG.md:2097` is still the last `##` heading. `LOG.md:2109-2118` (the round-36 narrative) and `LOG.md:2119-2124` (the freshness re-verification) are bullets of the Round 35 section. Round 35 already has its own re-verification at `LOG.md:2107-2108` (S182/S193). The second re-verification is about the nine drifted rows, not about round 35, and round 36 has no heading to attach it to. `git show bf0df77:LOG.md | grep -c 'Round 36'` was 0; the integration added sentences, not an entry.

2. `considerthese/2026-10-23.md` (added by `c081375`, inside the range) is named in none of the three docs. `c081375` is named in none of them. Prompt `.ufo/prompts/mori-round-36.md:107-108` requires the commit hash. The file is a daily reflection through `6bd5709` (`considerthese/2026-10-23.md:1-3`), not a C1/C2 artifact, but silence does not exclude it.

3. Wave-1 membership does not re-derive. `w1-spec.json` has 33 items. Disk has 28 `w1/*.md` plus `w1/swarm-registry.json`. Lesson `:60-61` and the LOG bullet name four non-returns (MutC1Novel, MutC2Novel, CritC1Counter, CritC2Counter), which predicts 29 reports. The fifth absence is BuildDriftTool (spec item: write `tools/mori-source-drift.py`; no `w1/BuildDriftTool.md`). `grep BuildDriftTool` on `LOG.md`, `SCORECARD.md`, and `corpus/lessons/round-36.md` is empty. The only reconciling sentence is `dispatch-log.txt:21-24`, and `dispatch-log.txt` is not named in the three docs (lesson `:62` says "the dispatch log" with no path). Lesson M3 (`:55`) says "28 wave-1 reports" which matches the disk, but the named-absence list does not.

4. Data-tip receipts and pins the claim record does not name:

| path | why it matters | where a reader is sent instead |
|---|---|---|
| `.ufo/waves/round-36/evidence/freeze.txt` | v1 pin (`contract.md`, both counters) at 11:47:16Z | SCORECARD `:2002` names commit `da12b37` only |
| `.ufo/waves/round-36/evidence/freeze-v2.txt` | v2 pin the task calls sha-pinned (`86dd3b7a…` / `c7edaacfff…`); "25/25 unmet, REF met" | SCORECARD `:2002` names `evidence/freeze-v3.txt` (added after `bf0df77`) |
| `.ufo/waves/round-36/evidence/census-start.txt` | round-start census receipt | LOG `:2123` states 204→220 and exit 0 with no path |
| `.ufo/waves/round-36/evidence/refs/ref-c1.py` | throwaway C1 reference; freeze-v2 says REF1 met | not named |
| `.ufo/waves/round-36/evidence/refs/ref-c2.py` | throwaway C2 reference; freeze-v2 says REF2 met | not named |
| `corpus/evidence/sources-r36/S205.src`–`S220.src` | open-time bodies for the 16 new rows | lesson Gate names the ids and `w2/RevSupS*`, not the copies. Indirect only: lesson M2 cites `corpus/knowledge/source-drift-r36.md`, whose `:48` names the directory |

5. Close-out receipts already on `HEAD` and still uncited (post-`bf0df77`, same three-doc search):

- `.ufo/waves/round-36/evidence/c1-after-final.txt` is a second `C1=met` (`seed=15951461284190234552`, `:4-5`). LOG `:2114` and SCORECARD `:2012` pin the other receipt, `evidence/c1-after.txt`, seed `7388485190103051243`. Two met receipts, one cited.
- `.ufo/waves/round-36/evidence/census-end.txt` ends `mori ok` (`:16`) and is the only file that shows the two new W04 lines (S218 `:14`, S220 `:15`). LOG `:2123` states that result and does not name the file.

`git status --short` at the end of this sweep also showed four untracked wave-2 reports (`MutC2Deleted.md`, `ScribeLesson.md`, `SentData.md`, `SentTools.md`). They are not at `HEAD`. `.scratch/` is the pre-round untracked path (`dispatch-log.txt:2`), not this round's.

## Inventory (118) — role and required pointer

Status is versus `6bd57097`. "Required pointer" is the SCORECARD / LOG / lesson cite that makes the file re-findable. "Now" is what those three docs contain at `HEAD` `5a2fe05`.

### `c081375` — not a claim artifact

| path | role | required pointer | now |
|---|---|---|---|
| `considerthese/2026-10-23.md` | daily reflection, window through `6bd5709` (`:1-3`) | LOG entry names path + `c081375`, or an explicit exclusion line with that hash | unnamed. Defect 2 |

### `da12b37` — freeze, before any data seat

| path | role | required pointer | now |
|---|---|---|---|
| `.ufo/waves/round-36/contract.md` | frozen C1/C2 claim contract (`:1`) | SCORECARD claim rows | SCORECARD `:2002`; lesson M1. Later commits edit it |
| `.ufo/waves/round-36/count-c1.py` | frozen C1 counter (byte classification, not a freshness verdict) | SCORECARD C1 before/after command | SCORECARD `:2012`. LOG slice does not say `count-c1` |
| `.ufo/waves/round-36/count-c2.py` | frozen C2 counter for the append-only gate | SCORECARD C2 command + capability row | all three |
| `.ufo/waves/round-36/dispatch-log.txt` | L1 dispatch record (census, slot grants, dead seats, inheritance) | LOG entry names this path; it is the absence list for defect 3 | unnamed (lesson `:62` says "dispatch log" only) |
| `.ufo/waves/round-36/evidence/c1-before.txt` | `tool_absent` / `C1=unmet` / exit 1 | SCORECARD before cell | SCORECARD `:2012` |
| `.ufo/waves/round-36/evidence/c2-before.txt` | `tool_absent` / `C2=unmet` / exit 1 | SCORECARD before cell | SCORECARD `:2011` |
| `.ufo/waves/round-36/evidence/census-start.txt` | round-start `sources-census.sh validate mori` stdout | LOG re-verification names the path next to 204→220 | unnamed. Defect 4 |
| `.ufo/waves/round-36/evidence/freeze.txt` | v1 sha pin of contract + both counters | SCORECARD pin sentence names the file | unnamed. Defect 4 |

### `c1a026c` — C0 (25 seats) and v2 re-freeze

`c0-dispatch.json` is 25 tasks. Each control is one shortcut shape; each `Ctl*.md` is that seat's counter receipt. Required pointer for the set: LOG or SCORECARD names `c0-dispatch.json` (membership) and `evidence/c0-rescore-v2.txt` (v2 result: 25/25 unmet, REF met). Now: LOG `:2118` and lesson `:60` say "c0 25" and do not name the dispatch file. Lesson M2 says "c0-rescore" without the path. SCORECARD `:2016` says "fails all 25 v2 controls" without the receipt path.

| path | role |
|---|---|
| `.ufo/waves/round-36/c0-dispatch.json` | C0 payload, 25 mutation-tester tasks |
| `.ufo/waves/round-36/c0/controls/K1.py` + `c0/CtlK1.md` | C1 skip-work / do-nothing |
| `K2.py` + `CtlK2.md` | C1 generic rows |
| `K3.py` + `CtlK3.md` | C1 sha-only, no excerpt state |
| `K4.py` + `CtlK4.md` | C1 no-reader / observed column |
| `K5.py` + `CtlK5.md` | C1 denial (labels inverted) |
| `K6.py` + `CtlK6.md` | C1 word bag |
| `K7.py` + `CtlK7.md` | C1 off-topic |
| `K8.py` + `CtlK8.md` | C1 label- or id-keyed |
| `K9.py` + `CtlK9.md` | C1 harness-keyed (met v1; unmet v2) |
| `K10.py` + `CtlK10.md` | C1 server echo / length-only |
| `K11.py` + `CtlK11.md` | C1 content-free |
| `K13.py` + `CtlK13.md` | C1 oldest-copy skip (met v1; unmet v2) |
| `J1.py` + `CtlJ1.md` | C2 skip-work |
| `J2.py` + `CtlJ2.md` | C2 prior-state skip |
| `J3.py` + `CtlJ3.md` | C2 generic rows |
| `J4.py` + `CtlJ4.md` | C2 endpoint-only `round_changed` |
| `J5.py` + `CtlJ5.md` | C2 no deleted-row arm |
| `J6.py` + `CtlJ6.md` | C2 position-keyed |
| `J7.py` + `CtlJ7.md` | C2 supersede-discharges |
| `J8.py` + `CtlJ8.md` | C2 denial |
| `J9.py` + `CtlJ9.md` | C2 word bag |
| `J10.py` + `CtlJ10.md` | C2 label- or id-keyed |
| `J11.py` + `CtlJ11.md` | C2 harness-keyed (met v1; unmet v2) |
| `J12.py` + `CtlJ12.md` | C2 off-topic. Report file added at `bf0df77`, not in `c1a026c` |
| `J13.py` + `CtlJ13.md` | C2 content-free |
| `.ufo/waves/round-36/evidence/c0-rescore-v2.txt` | L1 re-score of all 25 under v2 (`:1`) |
| `.ufo/waves/round-36/evidence/freeze-v2.txt` | v2 pin; supersedes v1 counter bytes (`:1`) |
| `.ufo/waves/round-36/evidence/refs/ref-c1.py` | throwaway C1 reference implementation |
| `.ufo/waves/round-36/evidence/refs/ref-c2.py` | throwaway C2 reference implementation |
| `.ufo/waves/round-36/w1-spec.json` | wave-1 spec, 33 items (re-rendered at this commit; dispatch payload lands at `bf0df77`) |

Also modified here, already listed: `contract.md`, `count-c1.py`, `count-c2.py`, `dispatch-log.txt`.

### `5842dc0` — C1 exploratory, before any tool

Modified only: `contract.md` (declaration; lesson M1, commit named) and `dispatch-log.txt` (still unnamed).

### `bf0df77` — data: tools, sources, wave-1 reports

| path | role | required pointer | now |
|---|---|---|---|
| `tools/mori-source-drift.py` | re-fetch each SOURCES row that has a committed copy; classify fresh/excerpt/drifted/unavailable/no-copy. Not a freshness verdict | SCORECARD C1 + LOG + lesson Gate | all three |
| `tools/mori-sources-appendonly.py` | rule-2 gate: in-place edits, deleted rows, superseders, `round_changed` | SCORECARD capability row (`:2023`) + LOG + lesson | all three |
| `tools/mori-index-clean.sh` | read-only index gate (`staged` / `intent_to_add`), QUALITY 103 | LOG or lesson names the path | LOG `:2117` says "index-clean gate" only. Path is `SKILL.md:868` via "SKILL Round36 rows". Lesson does not name it |
| `SKILL.md` (+20) | `## Round36` plus three registry rows (`:856-876`) | LOG "SKILL Round36 rows" | LOG `:2116`; lesson M2 |
| `corpus/QUALITY.md` (+25) | criteria 103 (index), 104 (append-only gate), 105 (drifted ≠ source change) (`:820-843`) | LOG names 103–105 | LOG `:2116` says "QUALITY 103–105". Lesson and SCORECARD name 105 only |
| `corpus/SOURCES.md` (+16) | rows S205–S220, one line each (`:211-226`) | lesson Gate per id | lesson `:17-32`; LOG and SCORECARD name the range |
| `corpus/knowledge/source-drift-r36.md` | C1 knowledge note (S205; copy classification; nine-row enumeration lives in later edits) | lesson | lesson M1/M2 |
| `corpus/evidence/sources-r36/S205.src`–`S220.src` | raw curl bodies for those ids | lesson Gate names the directory | unnamed. Defect 4 |
| `.ufo/waves/round-36/w1-dispatch.json` | validated 33-task payload | LOG names it next to "w1 33" | unnamed |
| `.ufo/waves/round-36/w1/swarm-registry.json` | 33 members | same | lesson names the w2 registry's null ids (`:63`), not this file |
| `.ufo/waves/round-36/c0/CtlJ12.md` | late C0 receipt (seat settled last, `dispatch-log.txt:18`) | with the C0 set | unnamed, same as the other Ctl reports |

Wave-1 reports on disk (28). Required pointer: LOG or lesson names `w1-spec.json` and lists all five absences (the four it already names, plus BuildDriftTool). Now: only CritAxisFit and SupS183 are named (SCORECARD `:2017`, lesson `:11` and M1).

| path | role |
|---|---|
| `w1/BuildAppendTool.md` | executor draft of the C2 gate (lane copy is the L1's) |
| `w1/BuildIndexCheck.md` | executor draft of `mori-index-clean.sh` |
| `w1/SrcCorpus.md` | scribe draft of S205 (fleet CORPUS.md) |
| `w1/SupS041.md` | supersede draft for in-place S041 |
| `w1/SupS044.md` | supersede draft for S044 |
| `w1/SupS051.md` | supersede draft for S051 |
| `w1/SupS062.md` | supersede draft for S062 |
| `w1/SupS064.md` | supersede draft for S064 |
| `w1/SupS179.md` | supersede draft for S179 |
| `w1/SupS180.md` | supersede draft for S180 |
| `w1/SupS181.md` | supersede draft for S181 |
| `w1/SupS183.md` | supersede draft for S183 (lesson cites `:29` word-count labels as wrong) |
| `w1/SupS184.md` | supersede draft for S184 |
| `w1/SupS185.md` | supersede draft for S185 |
| `w1/SupS186.md` | supersede draft for S186 |
| `w1/SupS188.md` | supersede draft for S188 |
| `w1/SupS189.md` | supersede draft for S189 |
| `w1/SupS190.md` | supersede draft for S190 |
| `w1/DraftDriftKnowledge.md` | scribe draft of `source-drift-r36.md` |
| `w1/DraftSkillRows.md` | scribe draft of the Round36 SKILL rows |
| `w1/DraftQuality103.md` | scribe draft of QUALITY 103 and 104 |
| `w1/MineCopyFidelity.md` | revenger: annotated excerpts and rebuild footers, not changed sources |
| `w1/ConnSiblings.md` | connector: sibling overlap of the two capabilities |
| `w1/ScoutSurfaces.md` | scout: per-surface map of rows that have a committed copy |
| `w1/ReviewPredicateIdentity.md` | reviewer: P-C1/P-C2 byte identity (QUALITY 97) |
| `w1/CritAxisFit.md` | critic: C1 cannot carry a freshness verdict |
| `w1/SentinelSafety.md` | sentinel: containment of the planned tools |
| `w1/ReviewDebtList.md` | reviewer: re-derive the append-only debt at `6bd57097` |

Absent from disk, must be named as absent: `BuildDriftTool` (not named — defect 3), `CritC1Counter`, `CritC2Counter`, `MutC1Novel`, `MutC2Novel` (named in lesson `:60-61`).

S205–S220 roles (the `.src` body is the opened page; the SOURCES row is the claim). Lesson Gate `:17-32` already has URL + quote for each id. That satisfies the Gate table. It does not cite the copy file.

| id | role |
|---|---|
| S205 | fleet CORPUS.md append-only rule (the row both claims rest on) |
| S206 | RFC 6585 §4, supersedes S041 |
| S207 | jj detached HEAD, supersedes S044 |
| S208 | NIST SP 800-122 PII minimum necessary, supersedes S051 |
| S209 | RFC 8785 JCS, supersedes S062 |
| S210 | git-rev-parse `--verify`, supersedes S064 |
| S211 | rejected duplicate of S056; supersedes S179 |
| S212 | Linux `stat.rst` v7.2, supersedes S180 |
| S213 | Linux `iostats.rst` v7.2, supersedes S181 |
| S214 | `part_stat.h` v7.2, supersedes S183 |
| S215 | `blk-core.c` v7.2, supersedes S184 |
| S216 | `blk-mq.c` v7.2, supersedes S185 |
| S217 | `blk_types.h` sector unit, supersedes S186 |
| S218 | flush iostat counters, supersedes S188 |
| S219 | discard statistics, supersedes S189 |
| S220 | sysstat `iostat.c` v12.8.0 extended path, supersedes S190 |

## What is already bound (not defects)

- C2 measured claim: SCORECARD `:2011`, `:2016`, capability `:2023`; LOG `:2110-2112`; lesson Gate `:9`. Evidence path `evidence/c2-after.txt` (lands after `bf0df77`).
- C1 exploratory, no freshness verdict: SCORECARD `:2012`, `:2017` ("unprovable"); LOG `:2112-2115`; lesson `:10`. The byte receipt is not offered as a freshness admission.
- Freshness re-verification prose exists (`LOG.md:2119-2122`) and names `evidence/drift-live-r36.txt`, `w2/RevQuality105.md`, `w2/ExecManualOracleSample.md`. It is filed under the wrong heading (defect 1). It does not re-run C2, the append-only gate, or index-clean; those are claim results, and the lane's label is "(freshness)" only. [INFERENCE] that narrower scope matches round 35's `:2107` label. It is not a second defect unless the integration treats `:2119` as the re-verification of the whole `:2109` bullet.
- Lesson Gate quotes for S205–S220 are present (`:17-32`), including the S211 rejection.

## Checklist the integration commit must satisfy

1. Add `## Round 36` to `LOG.md`. Move `:2109-2124` under it. Leave round 35's re-verification at `:2107-2108` as the only re-verification in that section.
2. Under that heading, name every commit in `6bd57097..tip` and the path it carries: `c081375` (`considerthese/2026-10-23.md`, or an explicit "not a claim" exclusion), `da12b37`, `c1a026c`, `5842dc0`, `bf0df77`, and the integration hash.
3. Put the freshness re-verification under the Round 36 heading. Keep the nine-row result. Add the receipt paths `evidence/census-start.txt` and `evidence/census-end.txt` next to 204→220.
4. Name `evidence/freeze.txt` and `evidence/freeze-v2.txt` in the SCORECARD pin sentence. `freeze-v3.txt` does not replace them.
5. Name `c0-dispatch.json`, `w1-spec.json`, `w1-dispatch.json`, and `dispatch-log.txt`. State the five wave-1 absences, including BuildDriftTool, so 33−5=28 matches `w1/*.md`.
6. Name `evidence/c0-rescore-v2.txt`, `evidence/refs/ref-c1.py`, and `evidence/refs/ref-c2.py` next to "25 unmet / REF met".
7. Name `corpus/evidence/sources-r36/` in the lesson Gate (the 16 bodies). Name `tools/mori-index-clean.sh` in the LOG or the lesson, not only "index-clean gate".
8. Cite exactly one C1 met receipt. Either cite `evidence/c1-after-final.txt` (seed `15951461284190234552`) as the tip re-score, or say it is not the claim receipt. Do not leave it uncited beside `c1-after.txt`.
9. For wave 2, name `w2-spec.json` (membership) and keep `.ufo/waves/round-36/w2/` as the return set. Any report still untracked at close (`MutC2Deleted.md`, `ScribeLesson.md`, `SentData.md`, `SentTools.md` at this sweep) is committed in that same entry or listed as discarded. A `w2/` directory cite without a membership file does not cover a count of "66" or "36+".
10. Re-check: `git diff --name-only 6bd57097 <integration>` paths are each a basename hit in the Round 36 LOG section, the Round 36 SCORECARD section, or `corpus/lessons/round-36.md`, or they sit in a directory whose membership file is itself a hit and whose absence list matches disk.

## Unknowns

- Whether a later commit after `5a2fe05` lands the four untracked w2 reports. This sweep's `git status` is a point reading.
- `c1-after-final.txt` was not re-run here; only its header was read. The seed differs from the cited receipt. That is enough to call it a second met receipt.

VERDICT: FAIL

Defects: `LOG.md:2097` (no `## Round 36`; re-verification `:2119` sits under Round 35), `considerthese/2026-10-23.md` + commit `c081375` uncited, `w1-spec.json` BuildDriftTool absent from LOG/SCORECARD/lesson while 33−4≠28, uncited `evidence/freeze.txt`, `evidence/freeze-v2.txt`, `evidence/census-start.txt`, `evidence/refs/ref-c1.py`, `evidence/refs/ref-c2.py`, `corpus/evidence/sources-r36/`, and post-tip `evidence/c1-after-final.txt` plus `evidence/census-end.txt`.
