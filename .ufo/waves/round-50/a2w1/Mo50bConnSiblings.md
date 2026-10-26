# Mo50bConnSiblings — sibling-overlap scan (read-only), mori round 50 wave a2w1

Seat: Mo50bConnSiblings (connector, leaf — no subagents dispatched).
Scope: `/home/vgpnk/Projects/shokunin/*-shokunin`, skipping each lane's `.scratch/` and `.ufo/waves/` trees, plus fleet-root closure reports under `.ufo/reports/` and `.ufo/waves/hyaku/` phase logs (fleet-level, not a lane's wave dir). All reads read-only (`git grep`, `grep`, `sed`, `ls`). No installs. No host probes beyond reading files. Scratch `/fast/scratch/hyaku/mori-r50/Mo50bConnSiblings/` was created and removed (no clones, no fixtures; nothing cited from it).
Entering data tip for cross-checks: mori `487941b9395e89678af0053cc443cdb49cdee6e3` (landed counters C1=met / C2=met per the seat brief).

Scan commands (representative, all exit 0 unless noted):

```text
$ for d in /home/vgpnk/Projects/shokunin/*-shokunin; do git -C "$d" grep -l -i -E 'memory\.stat|memcg|Memory cgroup stats' \
    -- . ':(exclude).ufo' ':(exclude).scratch' ':(exclude)*.html'; done
# hits: kaidoku-shokunin (LOG.md, SCORECARD.md, SKILL.md, corpus/knowledge/2026-10-18-arc2-r6-pe-midrung.md,
#   corpus/knowledge/2026-10-18-arc2-r7-pe-wall.md, 2 lessons), kumitate-shokunin
#   (corpus/knowledge/agent-isolation-substrates.md), tsukuroi-shokunin (SKILL.md, corpus/SOURCES.md,
#   corpus/knowledge/{boot-plane,degraded-triage-r4,kill-event-deep-r8,kill-oom-boundary-r33,
#   memory-arm-ver-s8,memory-pressure-r25,oom-event-plane}.md, corpus/lessons/round-33.md, plans/*, tools/*)
$ for d in *-shokunin; do git -C "$d" grep -l 'shokunin/MANIFEST.json\|../MANIFEST.json\|fleet.*MANIFEST' \
    -- tools/ scripts/ quality/ verifiers/ corpus/ reports/ plans/ | grep -v '.ufo/'; done
# tool hits outside .ufo/waves: kama tools/manifest-crosscheck.py; kaidoku tools/round-32/c2-capability-calibration-v2.py, v3.py
$ grep -rn -E 're-executed|re-scored|reproduced|re-derived' .ufo/reports/ | head -30   # fleet closure reports
```

## 1. memcg OOM report / memory.stat / cgroup-limit knowledge — ownership and adjacency

Per-PROVINCE ownership (each lane's `PROVINCE.md`, read in full where cited):

- **mori** — `mori-shokunin/PROVINCE.md:44` claims FR1 "Kernel OOM event-time attribution and fleet correlation" (event-time kernel summary/victim token validation is mori's frontier); `:24` Kill/OOM classes; `:9` cgroup `memory.events` counters as fleet evidence. New entry `corpus/knowledge/oom-memcg-stat-r50.md` sits squarely in FR1.
- **tsukuroi** — `tsukuroi-shokunin/PROVINCE.md:30-33`: "Host memory and kill-event measurements support OS triage; they do not establish which fleet wave caused pressure… fleet correlation belongs to mori." `:49` ADJ-04 routes fleet/wave attribution of host pressure to mori while tsukuroi retains "OS memory, journal and boot diagnosis". Refusal block (`:22-24`): "Never installs… never restarts services. Detection and report; the operator remediates." **So: cgroup limit *configuration* is the operator's; tsukuroi owns reading/diagnosing limit *state* (e.g. `memory.max` all-`max`, `oom.group=0`), mori owns kernel-print semantics + fleet correlation.** Mori's own entry agrees at `oom-memcg-stat-r50.md:81` ("Setting `memory.max`, `memory.oom.group` or `oom_score_adj` is tsukuroi's work; this entry licenses no configuration change") — see Finding L1 on the exact wording.
- **souji** — `souji-shokunin/PROVINCE.md:50` defers: "mori-shokunin observes fleet and host health (liveness, kill/OOM, …)" — no OOM-knowledge claim.
- **kaidoku, kumitate** — no ownership claim; their memcg mentions are incident narratives of their own seat kills (`CONSTRAINT_MEMCG`), see below.
- No other sibling PROVINCE mentions cgroup/memory/OOM ownership (grep over all 21 PROVINCE.md files).

Per-hit table (lane, path:line, owns/adjoins/conflicts, sentence for mori's report):

| # | lane | path:line | relation | sentence mori's report should carry |
|---|---|---|---|---|
| 1.1 | tsukuroi | `tsukuroi-shokunin/SKILL.md:1102` (memcg-limit OOM class), `:1103-1123` (C5 census arm) | **owns (adjoins)** | Tsukuroi's census classifies memcg-limit OOM prints and reads `memory.stat` pswpin/pswpout + `sock_throttled` as OS diagnosis; mori's r50 entry documents what those `memory.stat` keys and the report block *mean* (S489) — knowledge underpins tsukuroi's live readings, no overlap in content. |
| 1.2 | tsukuroi | `tsukuroi-shokunin/corpus/knowledge/kill-event-deep-r8.md:183` (`memory.stat` anon/file/slab live read), `:244` ("0 `Memory cgroup out of memory` prints in 13 boots; `memory.max`/`high`/`swap.max`/`zswap.max` all `max`, `oom.group` 0 → limit trigger closed"), `:333-334` | **owns (adjoins)** | Tsukuroi counts prints and reads limit state on this host; mori r50 states what the kernel would print (usage/limit/failcnt line, `Memory cgroup stats for` block, victim fields) — count/format split, not contested. |
| 1.3 | tsukuroi | `tsukuroi-shokunin/corpus/knowledge/oom-event-plane.md:266,271,369,420` (live `memory.stat` values, `memory.oom.group`, `memory.zswap.*` at `user.slice`/`user-1000.slice`) | **owns (adjoins)** | Same split: tsukuroi retains live slice readings; mori's entry is the sourced key-semantics reference those readings can cite. |
| 1.4 | tsukuroi | `tsukuroi-shokunin/corpus/SOURCES.md:125` (S119), `:155` (S149), `:188` (S182) — same v7.2 `oom_kill.c` URL and same raw-bytes sha256 `452f1348e79c…` as mori's S491 | **adjoins (shared source, distinct scope)** | Mori S491 and tsukuroi S119/S149/S182 cite byte-identical v7.2 `oom_kill.c` at different scopes (mori: report block + victim fields + memcg-vs-global split; tsukuroi: OOM_KILL counters, `oom_badness` victim selection, kill-log label taxonomy); same-URL-different-scope is a census W04 advisory, not a conflict (mori's own r47 census recorded this class; contract.md flags S491 as "a W04 warning, not an error"). |
| 1.5 | tsukuroi | `tsukuroi-shokunin/corpus/knowledge/kill-oom-boundary-r33.md:14` (memcg-limit OOM row), `:29` ("swap pressure… `memory.stat` pswpin/pswpout… OS diagnosis… gap at signature level: mori declares the theme, not these reads"), `:36` (S182 rationale) | **adjoins** | The r33 boundary register's recorded mori gap (live pswpin/pswpout-style reads) stands unchanged — r50 documents key meanings, not live reads; the two lanes' statements compose rather than collide. |
| 1.6 | tsukuroi | `tsukuroi-shokunin/corpus/knowledge/memory-pressure-r25.md:348,382` (MP6: kernel `OOM_KILL`/`MEMCG_OOM_KILL` counters vs PSI, "a userspace killer moves neither counter") | **adjoins** | MP6 covers counters/PSI; mori's r50 row "a rising oom_kill count does not prove a kernel memcg OOM" (S489) and S491 counter row are consistent with MP6 — no contradiction; the lanes independently sourced adjacent facts. |
| 1.7 | tsukuroi | `tsukuroi-shokunin/corpus/knowledge/memory-arm-ver-s8.md:64,146` (C5 arm reads `memory.stat` pswpin/pswpout/sock_throttled) | **owns (adjoins)** | Verification-arm live readings; unaffected by r50. |
| 1.8 | kaidoku | `kaidoku-shokunin/corpus/knowledge/2026-10-18-arc2-r6-pe-midrung.md:31` (`constraint=CONSTRAINT_MEMCG` at its own 9G cap), `2026-10-18-arc2-r7-pe-wall.md:19`, `SKILL.md:222`, `LOG.md:1150`, `SCORECARD.md:905` | **adjoins (incident narrative)** | Kaidoku reports its own seat-kill incidents using kernel vocabulary; it owns no OOM-print semantics — r50 is the reference those narratives can cite for what `constraint=CONSTRAINT_MEMCG` denotes. |
| 1.9 | kumitate | `kumitate-shokunin/corpus/knowledge/agent-isolation-substrates.md:141` (fixture: unit result `oom-kill`, kernel `constraint=CONSTRAINT_MEMCG`, 6/6 runs) | **adjoins (fixture evidence)** | Kumitate's fixture consumes the kill vocabulary as harness evidence; no ownership overlap with r50's sourced semantics. |
| 1.10 | mori (self) | `mori-shokunin/corpus/knowledge/oom-memcg-stat-r50.md:1-6,33-42,81-84`; rows S489-S491 in `corpus/SOURCES.md` | **owns** | r50 claims the memcg OOM report block, `memory.stat` key semantics, units, and the global-vs-memcg split under FR1 — a detection/knowledge surface neither tsukuroi nor any sibling has claimed. |

Conflict check: no sibling text contradicts any r50 claim. Closest proximity is 1.4/1.5 — same source bytes and the label `Memory cgroup out of memory`, at complementary scope. tsukuroi's live readings (anon/file/slab, pswpin/pswpout) and r50's documented keys (anon/file/shmem/kernel + block format) do not intersect on content.

## 2. Self-assessment reconcilers — does any sibling check SCORECARD/SHONEN against MANIFEST.json?

Answer: **none checks the exact mori-C1 shape** (SCORECARD Axes Last-change/Evidence cells + SHONEN tally pins vs fleet `MANIFEST.json` closure entries at a pinned fleet revision). Nearest siblings, pasted paths:

| lane | path | what it reconciles | vs fleet MANIFEST.json? |
|---|---|---|---|
| kama | `kama-shokunin/tools/manifest-crosscheck.py` (`:1-18` docstring) | lane trend-verdict ledger (TSV) vs fleet MANIFEST.json closure `trends` entries; exit 0 iff all agree — built for round-44 closure D4 | **YES** — but the lane-side artifact is a trend ledger, not SCORECARD/SHONEN |
| kaidoku | `kaidoku-shokunin/tools/round-32/c2-capability-calibration-v3.py` (`:1-22`) | SCORECARD.md `## Capabilities` table rows vs `capabilities_added` items of MANIFEST kaidoku round entries "at a pinned fleet commit, written by non-author closures" | **YES** — closest analog in shape (a SCORECARD table vs pinned fleet MANIFEST), different table |
| tsukuroi | `tsukuroi-shokunin/tools/check-self-assessment.py` (`:1-12` docstring) | SCORECARD `## Axes - round N` table (K01-K06) + SHONEN boxes 1-4 vs corpus paths (K24-K27), all read via `git show` at one revision | NO MANIFEST reference (grep `MANIFEST` → 0 hits) — reconciles against git-observed repo state |
| mado | `mado-shokunin/quality/check-axis-scores.py` (`:1-16`) | last published SCORECARD axis-table fractions vs re-derivations by the lane's own instruments | NO MANIFEST reference |
| souji | `souji-shokunin/tools/souji-capability-agreement.py` (`:1-8`) | SCORECARD capability rows vs committed bytes at REV (enumerated from preregistration) | NO MANIFEST reference |
| kaidoku | `kaidoku-shokunin/tools/round-25/a2/c1-calibration.py`, `tools/round-26/c2-calibration.py`, `tools/round-36/c2-counter.py`, `tools/round-38/c2-counter.py` | SHONEN/self-assessment calibration counters | NO MANIFEST reference (grep → 0 hits) |
| kotodama | `kotodama-shokunin/reports/round-5{1,2,3,4,5,6,7,8,9}/claims-agree.py`, `reports/round-51/calibration/ruler.py` | claims.json vs separability-manifest.json (lane-internal); ruler measures checker bytes | NO — lane-internal manifests, not the fleet closure |
| chousa | `chousa-shokunin/tools/research-gate.sh` (MANIFEST hits are its own gate-record format, `:4185` etc.), `corpus/evidence/round36/c1-count.py`, `round41/c1-count.py` | lane research-gate records | NO fleet MANIFEST |
| kotoba | `kotoba-shokunin/verifiers/verify_dispatch_prompts.py`, `box_proof_case_deletion.py:63,494`, `verify_alwayson.py` | lane fixture/dispatch manifests | NO fleet MANIFEST |

Also for completeness: mori's own `.ufo/waves/round-50/count-c1.py` (the frozen claim instrument, not a sibling) is the only instrument fleet-wide that reads SCORECARD Axes cells + SHONEN pins against the pinned fleet MANIFEST (`e014499613f63f8a467821219b0296121119ca53`) — so mori's C1 form is fleet-unique per this scan, and its drift class (SHONEN 60/60, 13/13 pins vs 114/17 selftests, mined as this round's mistake) has no sibling precedent to borrow from.

Sentence for mori's report: *Across the fleet only kama (`tools/manifest-crosscheck.py`) and kaidoku (`tools/round-32/c2-capability-calibration-v3.py`) reconcile a lane self-assessment artifact against the fleet `MANIFEST.json`, and neither touches the SCORECARD Axes/SHONEN shape mori C1 measures; tsukuroi (`tools/check-self-assessment.py`), mado (`quality/check-axis-scores.py`) and souji (`tools/souji-capability-agreement.py`) reconcile self-assessment against git-observed repo state without the fleet record — mori C1's MANIFEST-pinned form is fleet-unique and its drift class is unfalsified-by-precedent.*

## 3. Closure re-execution receipts

Fleet-level closure reports (outside any lane's `.ufo/waves`) carry standing re-execution receipts; examples observed:

| lane/round | path:line | receipt content |
|---|---|---|
| mori r12 | `.ufo/reports/round-12/mori.md:34-38` | "The L1 re-executed every recheck: `oom_kill.c` v7.2 at lines 935, 936, 447, 452, 945; `memcontrol.c@c03c1a14` at 1820, 1825, 4966; `oomd-util.c` v261 at 269, 306; catalog `@cf8ebfc6` at 66, 604, 884" — a per-source, per-line re-execution receipt |
| tsukuroi r29 | `.ufo/reports/round-29/tsukuroi.md:24` | "The C1 counter was hardened three times after attacks… each version re-measured the claim" under the frozen-counter rule |
| kake r43 | `.ufo/waves/hyaku/PHASE5.md:80` | "C1 NOT MET VERIFIED AS DECLARED (predicate byte-identical at freeze b49cba9c; closure re-scored 4 controls fresh-seed met + witnesses reproduced; 27-control tally spot-checked class by class)" |
| mori r27 | `.ufo/waves/hyaku/PHASE3.md:675` | fresh non-author closure `HyakuCloseMori27b` re-dispatched on the round-27 prompt (one re-dispatch, nothing inherited) — closure freshness receipt at the orchestrator level |
| all claim lanes | per-lane `corpus/lessons/round-*-verifier-spotcheck.md` counts: kama 32, mado 30, kake 35, kotoba 29, tsukuroi 27, kaidoku 24, souji 18, **mori 34** | the standing per-round spot-check lesson series is each lane's durable closure re-execution receipt store |
| mori r49 → r50 route | `mori-shokunin/corpus/lessons/round-49-verifier-spotcheck.md:111` | routes "commit a selftest output file for the tools" into `.ufo/waves/round-50/evidence/` "so the 114/114 and 17/17 tallies resolve at closure time" — the exact receipt class C1's `evidence/selftests/` now satisfies |

Sentence for mori's report: *Closure re-execution is fleet-standard and receipt-backed — mori's own series is 34 verifier-spotcheck lessons, r12's closure re-executed every knowledge recheck with per-line receipts (`.ufo/reports/round-12/mori.md:34-38`), and r50's selftest receipts answer the r49 closure's routed item 2 (`round-49-verifier-spotcheck.md:111`); no sibling gap observed on this axis.*

## Connector note — one bounded move (advisory)

- **Affected axes:** adjacency (6), depth (5, the C2 axis), calibration (5) — the round's three lowest.
- **Proposed move:** in the L1's integrated report, carry one explicit adjacency sentence for C2 — *"r50's S491 cites byte-identical v7.2 `oom_kill.c` (sha256 `452f1348…`) at a different scope from tsukuroi's S119/S149/S182, and documents `memory.stat` key semantics that tsukuroi's live census readings (`SKILL.md:1103-1123`) consume; tsukuroi retains live reads and limit-state diagnosis, mori retains kernel-print semantics and fleet correlation — adjoining, not conflicting (tsukuroi `PROVINCE.md:30-33,49`; mori `PROVINCE.md:44`)."*
- **Why it helps:** wave 2 will re-open every C2 row against its quote's surrounding text and will independently find the S491/S182 source sharing (it is a census W04 class mori itself records). Pre-stating the scope split converts a likely wave-2 adjacency finding into a carried limit, protecting depth/adjacency scores without touching frozen counters, predicates or data.
- **Risks:** none to frozen artifacts (report text only); the sentence must not be read as tsukuroi acknowledging mori's entry — tsukuroi's r27 register warns "a sibling citing this lane is not a recipient acknowledgement", and the same courtesy applies in reverse (LOW).
- **Verification:** re-run `python3 .ufo/waves/round-50/count-c2.py 487941b9395e89678af0053cc443cdb49cdee6e3` after integration — expected unchanged `C2=met … sources=3` (report-text-only change; counter reads no report).

## Findings

- **MED** — `mori-shokunin/corpus/knowledge/oom-memcg-stat-r50.md:5` (S491 row) and `corpus/SOURCES.md` S491: same v7.2 `oom_kill.c` URL+bytes as tsukuroi S119/S149/S182 (`tsukuroi-shokunin/corpus/SOURCES.md:125,155,188`; sha256 `452f1348e79c…` both sides). Relation: adjoins, distinct scope; flag in the integrated report so wave 2 does not score it as an unreported collision.
- **LOW** — `mori-shokunin/corpus/knowledge/oom-memcg-stat-r50.md:81`: "Setting `memory.max`, `memory.oom.group` or `oom_score_adj` is tsukuroi's work" — consistent with the fleet split, but per `tsukuroi-shokunin/PROVINCE.md:22-24` the configuration *act* is the operator's (tsukuroi diagnoses, refuses config writes; see also `mori-shokunin/PROVINCE.md:335` "the operator owns the configuration"). Wording is defensible ("tsukuroi's work" as diagnosis/repair lane) but could be misread as granting tsukuroi a write authority its PROVINCE refuses; no edit proposed this wave (data frozen except by L1 correction).
- **LOW** — `tsukuroi-shokunin/corpus/knowledge/kill-oom-boundary-r33.md:29` records a mori gap at signature level (live `memory.stat` pswpin/pswpout-style reads). r50 does not close that gap (it documents key semantics, not live reads). No action; the two statements compose. Carry the sentence so wave 2 does not misread r50 as claiming tsukuroi's live-read surface.
- **LOW** — kaidoku (`corpus/knowledge/2026-10-18-arc2-r6-pe-midrung.md:31`) and kumitate (`corpus/knowledge/agent-isolation-substrates.md:141`) consume `CONSTRAINT_MEMCG` vocabulary in incident/fixture narratives without owning semantics; relation adjoins. Informational for the adjacency cell only.
- **INFO** — Fleet-unique shape: no sibling reconciles SCORECARD Axes cells + SHONEN pins against the fleet MANIFEST.json (nearest: kama `tools/manifest-crosscheck.py`, kaidoku `tools/round-32/c2-capability-calibration-v3.py`, both different tables). Supports C1's novelty claim; no defect.

## Verification of this seat's own claims

- All lane citations above were read directly (grep/sed/git grep, exit 0); tsukuroi, kaidoku, kumitate, souji, mado, kama, kotodama, chousa, kotoba files opened at the cited lines.
- UNVERIFIED: I did not read every tsukuroi knowledge file end-to-end (oom-event-plane.md, kill-event-deep-r8.md, memory-pressure-r25.md, memory-arm-ver-s8.md were grepped at citation lines plus ±context only); absence of a sibling claim is per the greps listed, not a proof of non-existence.
- Disk guard not required (no heavy run); no tools installed; no clones created; scratch dir `/fast/scratch/hyaku/mori-r50/Mo50bConnSiblings` removed after writing this report.
