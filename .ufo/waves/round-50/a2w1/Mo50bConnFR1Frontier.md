# Mo50bConnFR1Frontier — frontier mapping: FR1 re-verification and next-entry proposal

Seat: connector (frontier drafting), mori-shokunin round 50 attempt 2, wave a2w1.
Scope: read-only. Nothing in the lane was edited. Scratch `/fast/scratch/hyaku/mori-r50/Mo50bConnFR1Frontier/` was created, used, and removed (trap-equivalent verified: `ls` shows it gone). No kernel-log `MESSAGE` text was read; all kernel evidence comes from the committed source copies under `corpus/evidence/sources-r50/` (source code and documentation, not host logs). No tools were installed or upgraded.

Verification revision: **R = `487941b9395e89678af0053cc443cdb49cdee6e3`** (attempt-2 landed data). Entering tip for scout-time claims: `7197160b927f04db294c9553fb48fadcc7a3f4e3`. Spec commit on top (`4548a34d`) touches none of the corpus/README/PROVINCE/SHONEN/SCORECARD paths (`git diff --stat` empty).

Counters re-run at R myself (read-only, TMPDIR in scratch):
- `python3 .ufo/waves/round-50/count-c1.py 487941b9395e89678af0053cc443cdb49cdee6e3 --scratch …/tmp/c1` → `C1=met items=8 axes=6 pins=2 boxes=4 mismatches=0 errors=0 hidden=0 manifest=a94551c5bc8d rev=487941b9…` rc 0.
- `python3 .ufo/waves/round-50/count-c2.py 487941b9395e89678af0053cc443cdb49cdee6e3` → `C2=met claims=22 located=22 quote_missing=0 bad_rows=0 sources=3 source_rows=ok pins=ok provenance=ok rev=487941b9…` rc 0.

## Verdict on the salvaged scout report (`w1/Mo50ScoutCoverageFR1.md`)

**Every factual claim re-verified CONFIRMED; none WRONG.** Two of its integration recommendations are still unlanded at R (and at `4548a34d`) — flagged below as the connector move, since the L1 holds integration.

### Claim-by-claim re-verification at R

1. **FR1 Frontier row** — CONFIRMED. `corpus/README.md:341` at R carries "Kernel OOM event-time attribution and fleet correlation", first evidence `knowledge/kernel-oom-line-attribution-r12.md:10-16`; `knowledge/audit-r11.md:203-204` (D08/D09 rows), boundary naming round-13 advance, token validation + fleet correlation as remaining frontier, catalog-ID not authenticated unique kills. `PROVINCE.md:44` is the same row's province form. The FR1 row is **byte-identical** between entering `7197160b` and R (`diff` of the two lines: IDENTICAL) — the landed data did not rewrite it, matching the scout's "do not rewrite" instruction.
2. **Round-49 FR1 note present, append-only** — CONFIRMED. `corpus/README.md:683` at R: "Dated note (append-only): the FR1 Frontier row gains the retention rule behind its boundary; no frontier row is rewritten." (journal-reach-r49, S485–S488; map row at `:681`).
3. **Latest FR1 map touches** — CONFIRMED. Round-42 block (`:612-617`) adds `oom-evidence-loss-r38.md` and `oom-victim-context-r41.md`; round-45 `census-cgroup-levels-r45.md` states at its `:66` "No FR1 closure and no FR12 advance."; round-49 row cites `journal-reach-r49.md` (S485–S488); `oom-tracepoints-r47.md` is `coverage-map: FR13` only (r47 confirmed FR13-only).
4. **Lane-wide grep at entering tip: one hit** — CONFIRMED in substance and now overtaken. At R the pattern `Memory cgroup stats|memory_stat_format|failcnt|mem_cgroup_print_oom_meminfo|mem_cgroup_print_oom_context|memory\.stat` hits only `corpus/SOURCES.md` (the new S489–S491 rows), `corpus/knowledge/kernel-oom-line-attribution-r12.md:1` (the `source:` line), and the new `corpus/knowledge/oom-memcg-stat-r50.md`. `corpus/README.md`, `PROVINCE.md`, `SKILL.md`, `SHONEN.md`, `SCORECARD.md`: **0 hits** at R. The memcg-block ground is now held exactly where the scout said it belongs (FR1).
5. **What the four named entries hold** — CONFIRMED.
   - `kernel-oom-line-attribution-r12.md:1` cites S003 `oom_kill.c` v7.2 and S004 `memcontrol.c` **master commit `c03c1a14…:1820-1826`**; the claim text is summary/victim tokens only, never the usage/limit/failcnt lines or the stats block.
   - `oom-tracepoints-r47.md` table: exactly 8 tracepoint rows (`oom_score_adj_update`, `reclaim_retry_zone`, `mark_victim`, `wake_reaper`, `start_task_reaping`, `finish_task_reaping`, `skip_task_reaping`, `compact_retry`); only `mark_victim` carries victim identity (pid, comm, uid, rss fields); **no row carries a cgroup path**; v7.2 copies sha256-pinned.
   - `oom-victim-context-r41.md`: abstract-only (IEEE TSC via OpenAlex, S262), `coverage-map: FR13, FR1`; says nothing about host one-workload-per-cgroup.
   - `census-cgroup-levels-r45.md`: quotes the `memory.events` hierarchical vs `.local` distinction from `cgroup-v2.rst` (`:46-52`); the r50 entry contains no `events.local` restatement — no collision.
6. **MED finding — r12's memcontrol.c line numbers are master-commit numbers** — CONFIRMED. In the committed v7.2 copy, `mem_cgroup_print_oom_context` is at line **1770** (`oom_memcg=`/`task_memcg=` prints at ~1775/1780), versus r12's `:1820-1826`. The S490 row scopes this correctly ("not the master-commit path labels of S004"). The new entry quotes v7.2 bytes and never reuses r12's numbers.
7. **Sibling ownership sweep** — CONFIRMED. The fleet-wide grep `memory\.stat|Memory cgroup stats|failcnt` over `*-shokunin/corpus` + `PROVINCE.md` (excluding mori) returns exactly the same four tsukuroi files the scout listed: `kill-event-deep-r8.md`, `kill-oom-boundary-r33.md`, `memory-arm-ver-s8.md`, `oom-event-plane.md`. Zero hits in kumitate/kama/kagi/souji or any other sibling. The four hold live slice readings and a global-vs-memcg **label count** only (tsukuroi `kill-event-deep-r8`: 1 vs 0 in 13 boots; `kill-oom-boundary-r33` boundary table cites S182, `oom_kill.c:1168-1170` label split, victim record `945-951`). tsukuroi `SOURCES.md` S119/S149/S182 are all `oom_kill.c` **v7.2** (same URL as mori S491/S003/S476) — CONFIRMED; `memcontrol.c` appears in **no tsukuroi source row** (the single `grep -c memcontrol` hit is a round-25 bounded-search *narrative*, line 300, not a `| S-id |` row) — CONFIRMED with that nuance. tsukuroi `PROVINCE.md:30` "Host memory and kill-event measurements support OS triage" — CONFIRMED; its `ADJ-04` row routes host-pressure-needs-fleet-correlation to mori — CONFIRMED.
8. **MED finding — S489–S491 absent at entering tip** — CONFIRMED and resolved. `git show 7197160b:corpus/SOURCES.md`'s last row is S488. At R, S489 (cgroup-v2 v7.2 docs page; "adopts staged S533 renumbered by document"), S490 (`memcontrol.c` v7.2), S491 (`oom_kill.c` v7.2; "same URL as S003 and S476 with a different scope") are present, all `mined`, `opened 2026-10-26`, used-by lists `corpus/knowledge/oom-memcg-stat-r50.md`.
9. **Frozen-copy digests** — CONFIRMED. `.ufo/waves/round-50/evidence/freeze-sha256.txt` entries for the three `sources-r50/` copies equal `git show R:<copy> | sha256sum` for all three (cgroup-v2.7.2.html `2d716cb7…`, memcontrol.c.v7.2 `8a28e0bc…`, oom_kill.c.v7.2 `452f1348…`).
10. **LOW finding — oom_kill.c v7.2 URL overlap with tsukuroi S119/S149/S182** — CONFIRMED; mori keeps its own row (S491), per the existing no-merge rule (`PROVINCE.md:90`).
11. **Entry content vs the copies (independent quote spot-check)** — CONFIRMED for all 22 rows. I re-extracted all 22 table quotes from the entry at R and searched the committed copies under the counter's own normalization (`.ufo/waves/round-50/count-c2.py:70-75`: script/style/comment blocks dropped, tags replaced with a **space**, entities decoded, whitespace collapsed): `rows: 22, all located`. Note for reviewers: a naive tag-strip that deletes tags instead of spacing them joins `file`+`Amount` into `fileAmount` and falsely misses the three S489 `file`/`shmem`/`kernel` quotes — that is a checker artifact, not an entry defect.
12. **Scout's honest-limit acknowledgment** — CONFIRMED fair. The scout did not open the copies or verify the kernel print format; the landed entry's quotes are now independently located evidence (item 11).

### Claims of the scout that are NOT yet true at R (recommendations, not facts)

- **A. "Must link" cross-links absent from the landed entry.** The scout listed 4 required + 2 more + 2 optional links (r12, r41, r47, r45, `oom-kill-counter-kernel-only-r12.md`, `oom-evidence-loss-r38.md`, optional tsukuroi paths). The landed `oom-memcg-stat-r50.md` contains **zero** references to any of them (grep over the entry for `r12|r41|r47|r45|r38|oom-line-attribution|victim-context|tracepoints|cgroup-levels|evidence-loss`: no hits). It stands alone with `coverage-map: FR1` plus its own Limits/Boundaries.
- **B. Round-50 coverage-map block and FR1 Frontier note absent from README.** `git show R:corpus/README.md | grep -i "oom-memcg-stat-r50\|Round-50\|round 50"` → no output. This follows the contract's separability clause (C2 touches only the entry, its SOURCES rows and the copies), so it reads as deferred wave-2 integration, not an error.

## FR1 sub-questions still open after `oom-memcg-stat-r50.md`

The entry lands the "what the kernel prints" half of FR1 (detection rule: a stats block means the kill was charged to a scope). Remaining open, each traced to evidence:

1. **Live-record token validation against the three-part burst** (FR1's "kernel summary/victim token validation" half). r12 validated the two summary-line tokens; the block composition, per-line units and victim fields exist only as a sourced schema from frozen v7.2 copies — the lane rule forbids reading kernel-log `MESSAGE` text, so no host record has ever been validated against this schema. Open.
2. **Fleet task correlation** (the second half of FR1's name). Nothing maps the printed cgroup path (`oom_memcg=`/`task_memcg=`, stats-block path) to a fleet seat or workload. Mori is consume-only (FR14); the identity source must be fleet-side records (MANIFEST closures, watchdog `launch`/`complete` lines, systemd unit/scope names). tsukuroi's ADJ-04 explicitly hands this correlation to mori. Open, untouched.
3. **Authenticated unique kills.** FR1 boundary unchanged: catalog-ID records are not authenticated unique kills. Open.
4. **Burst under-determination.** The entry's own limit: the victim line prints outside the `__ratelimit` guard, so `Killed process` lines can occur with no block; a missing block is not global-kill evidence. This gives `oom-evidence-loss-r38.md`'s lossy-link ground a sourced mechanism, but no lane tool encodes the classification rule. Open.
5. **Group-kill accounting.** One `memory.oom.group` event prints one victim line per killed mm while `oom_kill` counts processes and `oom_group_kill` counts events; the sourced distinction is in the entry but no census/ledger arm uses it. Open.
6. **Block truncation.** `SEQ_BUF_SIZE` overflow under `oom_lock` prints only a warning; a truncated block is possible at event time. Open.
7. **Charge-to-cause.** The entry's own boundary: the block names the charged cgroup, not what made it grow. Cause attribution stays open (and out of lane scope).

## Proposed next FR1 entry (for README's Frontier note, one sentence)

> **Next FR1 entry:** a validation-schema entry that turns the round-50 three-part burst into a strict read-only parse schema — regexes for the two usage lines, the stats-block key set with per-line units, and the victim-line fields — so a retained kernel record can be classified memcg-vs-global and its scope path extracted without echoing `MESSAGE` text, extending r12's two-line token validation to the full burst; **sources needed: all already held in-lane** (S489 cgroup-v2 v7.2, S490 `memcontrol.c` v7.2, S491 `oom_kill.c` v7.2, S014/S015 journal-field docs) — no new external source required.

The entry after that (the fleet-correlation half) would be the first to need a new source: a systemd cgroup-path/unit document (e.g. `systemd.resource-control(5)` or the systemd.io cgroup-delegation page, new S-row) plus fleet cgroup-naming evidence, and it should be proposed only after the schema entry lands.

Draft for the L1's append-only Frontier note (fenced, README-only; the FR1 row itself stays byte-unchanged):

```
## Round-50 Frontier note — FR1 half advanced, not closed

Dated note (append-only): the FR1 row above is not rewritten. `knowledge/oom-memcg-stat-r50.md`
(S489–S491, opened 2026-10-26) advances FR1's "what the kernel prints" half only: the memcg OOM
usage/limit/failcnt lines, the `Memory cgroup stats` block (same formatter as memory.stat, per-key
lookup, byte units), and the per-victim `Killed process` fields, with the memcg-vs-global split
(`__show_mem` versus the stats block) as the detection rule. Still frontier: live-record validation
against that schema (no MESSAGE read), fleet task correlation of the printed cgroup path (consume-
only; tsukuroi ADJ-04 hands correlation to mori), authenticated unique kills, burst and truncation
loss modes, group-kill event accounting, and charge-to-cause. Next FR1 entry: the strict parse
schema for the three-part burst (sources already held: S489–S491, S014/S015).
```

## Connector move (one bounded proposal)

**Evidence.** Items A/B above: the scout's two integration recommendations (entry cross-links; README round-50 map row + Frontier note) are the only unlanded pieces of an otherwise fully confirmed report, and both are README/prose-level. The counter input surfaces were checked: `count-c1.py` reads only `SCORECARD.md`, `SHONEN.md`, `.ufo/waves/round-50/evidence/selftests/` and the fleet MANIFEST; `count-c2.py` reads only the entry, `SOURCES.md`, the three copies and `freeze-sha256.txt` (verified from the counter bodies and by both re-runs at R). Neither reads `corpus/README.md` or `PROVINCE.md`.

**Affected axes.** Depth (frontier mapping gains the dated FR1 note the contract's Frontier-step section expects) and adjacency (the note names the tsukuroi overlap and ADJ-04 handoff); coverage is helped at the margin. Calibration and operability are untouched. No harm to C1/C2: both counters re-print `met` with identical tokens after such an edit because none of their input bytes change (if the links go in README's block and the entry is left byte-unchanged; adding a prose `## Links` section inside the entry is also P-C2-invisible since the predicate reads only the header fields and table rows, but README-only is the zero-risk variant).

**Proposed move.** In wave-2 integration the L1 lands exactly two prose artifacts: (1) the README round-50 coverage row ("FR1 — kernel memcg OOM print block and memory.stat key meanings" → `oom-memcg-stat-r50.md`) plus the fenced Frontier note above; (2) the entry's `## Links` block (README-side copy or entry tail — either satisfies the scout's must-link list: r12, r41, r47, r45, `oom-kill-counter-kernel-only-r12.md`, `oom-evidence-loss-r38.md`, with the two tsukuroi paths cited as adjacent-only). This completes the scout's confirmed plan at zero predicate risk.

**Risks.** (a) If the Frontier note paraphrases FR1's remaining scope too loosely, a later seat could misread FR1 as narrowed — mitigated by keeping the row byte-unchanged and the note append-only, matching the round-24/round-49 precedent. (b) A links block inside the entry changes entry bytes, which wave-2 quote re-openers must re-read — mitigated by the README-only variant. (c) The next-entry proposal asserts "no new external source required" — true only while S489–S491 and S014/S015 remain open; the note dates itself against that.

**Verification.** After integration: re-run both counters at the new tip — expected `C1=met items=8 axes=6 pins=2 boxes=4 mismatches=0 errors=0 hidden=0` and `C2=met claims=22 located=22 quote_missing=0 bad_rows=0 sources=3 source_rows=ok pins=ok provenance=ok` with byte-identical output to the R re-runs quoted above (counter inputs unchanged); then `git diff R..tip -- corpus/README.md` shows only the appended block, and the FR1 row at line 341 diffs empty.

## Findings

- **MED** — `corpus/knowledge/oom-memcg-stat-r50.md` (landed entry): the scout's "must link" cross-links (r12, r41, r47, r45, `oom-kill-counter-kernel-only-r12.md`, `oom-evidence-loss-r38.md`) are absent from the entry; it stands alone. Recommend wave-2 integration add the links (README block or entry `## Links` tail).
- **MED** — `corpus/README.md` (after `:683`): no round-50 coverage-map row and no FR1 Frontier note at R or `4548a34d`; the scout's recommendation is unlanded. Recommend the L1 land the fenced note above with the map row; zero counter risk (verified counter input surfaces exclude README).
- **LOW** — `corpus/knowledge/kernel-oom-line-attribution-r12.md:1,12`: still cites S004 `memcontrol.c` at master commit `c03c1a14:1820-1826`; the v7.2 copy holds the same function at line 1770. S490's scope note covers it; an erratum or re-pin is optional, not required.
- **LOW** — `.ufo/waves/round-50/count-c2.py:73`: tag-stripping replaces tags with a space, so quote location passes for the three S489 `file`/`shmem`/`kernel` rows; a checker that deletes tags instead will falsely report `quote_missing=3`. Named limit for wave-2 reviewers re-opening rows.
- **LOW** — `corpus/SOURCES.md:491`: S491 shares its URL with tsukuroi S119/S149/S182; overlap acknowledged in the row's scope cell. Keep separate per `PROVINCE.md:90`; no merge.
- **LOW** — tsukuroi `SOURCES.md:300`: the word `memcontrol` occurs once, inside a round-25 bounded-search narrative, not a source row; the scout's "no tsukuroi memcontrol.c row" stands with this nuance.
- **INFO** — counters re-run at R: `C1=met … mismatches=0` rc 0; `C2=met claims=22 located=22 … sources=3` rc 0; all three frozen-copy sha256 match; all 22 entry quotes located under the counter's normalization. Scout report: 0 of its factual claims wrong.
