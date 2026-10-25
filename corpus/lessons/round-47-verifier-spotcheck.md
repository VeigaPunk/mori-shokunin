author: hyaku closure (non-author integrator, @m_sonnet)

# Round 47 — non-author closure spot-check (mori)

Lane HEAD before `2d85e33d14198d388fd3cda9cc15ec07e57e7a53`, after `dd17d927ffcb10908c191893472bd60e5d028c29`.
Driver digest (`.ufo/watchdog.log:1397,1406`): `2026-10-25T16:15:01-03:00 launch mori round=47 pgid=601372 driver=hyaku-inline attempt=1`;
`2026-10-25T17:25:39-03:00 complete mori round=47; hyaku-inline attempt=1`.
No lane gate or selftest was executed as a verdict source. Plain re-measurements were run in a
throwaway `git archive dd17d927` export under `/tmp`; the remaining gate verdicts are evidence-verified from
committed receipts.

## 1. Conformance (step 1)

| check | result |
|---|---|
| report committed by lane identity | `git log --format='%an %H' -- .ufo/reports/round-47/mori.md` → `mori-shokunin ced6393a66ec82f0514e1e63c03772ddc998db0b` (filed 17:27:24, two minutes after the driver's `complete` line — noted, status-neutral) |
| `SHONEN` heading, one line per box | present; four boxes, each `[~]` with a pointer |
| cited lane commits are ancestors of `master` | `63eecf27 4dea3d09 af2250d8 68d66ca5 dd17d927` → all `merge-base --is-ancestor … master` true |
| pushed | `jj-lane.sh state` → `local=remote=dd17d927… ahead=0 behind=0` |
| no uncommitted round work | **defect**: `git status --porcelain` shows 53 untracked paths — `.scratch/r47-*` and `.scratch/r47w2-*` directories, plus round work `.ufo/waves/round-47/w2-results.json`, `w2/CritV2Junk.md`, `w2/MutV2Rebound.md`, `w2/ScoutMisroot.md`. The report says these three seats had not returned; their files now exist on disk but were never committed |
| prompt carries the template contract | `.ufo/prompts/mori-round-47.md` has §1–§5 of `templates/round-prompt.md` plus §6 hyaku addendum |

Defects stay status-neutral; the report is a real report (five landed commits, evidence tree), not a marker.

## 2. Claims (step 2)

### C1 — registry self-test pins reproduce from committed bytes (calibration)

Lane verdict: **unprovable** (frozen v1 scorer is green on five junk edits). I rule on the *change* independently.

Re-measured (plain):

- `git show 2d85e33:SKILL.md | sed -n 912p` → pin text `MORI_SOURCES_APPENDONLY_SELFTEST pass=15 fail=0`; `git show dd17d927:SKILL.md | sed -n 912p` → `pass=22 fail=0`. A substitution diff (`pass=15`/`pass=22` → `X`) shows the only other change on that row is an added provenance annotation.
- In `git archive dd17d927`: `python3 tools/mori-sources-appendonly.py dd17d927… --selftest` → `MORI_SOURCES_APPENDONLY_SELFTEST pass=22 fail=0`, rc 0. So the repaired pin equals the committed tool's output; the entering pin did not (the tool at `d72ac167` onward prints 22 per `w1/RevPinHistory.md`).
- Same export: `sha256sum tools/mori-gate-registry.py` → `8b82ac999091…`, `python3 tools/mori-gate-registry.py --selftest` → `GATE_REGISTRY_SELFTEST pass=15 fail=0`, matching the row at `SKILL.md:184`.
- `git diff --stat af2250d8 dd17d927 -- SKILL.md tools corpus/knowledge corpus/SOURCES.md corpus/QUALITY.md` is empty, so the lane's after-receipts (measured at `af2250d8`) cover the final bytes.

Evidence-verified, not executed (lane-owned gate `tools/mori-pin-check.py`):

- `evidence/control-c1-donothing.txt` → `PIN_CHECK=unmet tally_pins=26 … mismatches=1`, line 912 `state=mismatch pinned='pass=15 fail=0' observed='pass=22 fail=0'`.
- `evidence/after-c1-v1-frozen.txt` and `evidence/after-c1-v2.txt` → `PIN_CHECK=met tally_pins=28 digest_pins=5 mismatches=0 …`; `evidence/selftest-pin-check.txt` is the frozen v1 (22 arms); the 34-arm v2 tally is recorded at `SKILL.md:938` and echoed in `after-c1-v2.txt` line `pin line=938 … observed='pass=34 fail=0'`.
- `evidence/v1-junk/*` vs `evidence/v2/*`: the frozen v1 prints `met` on v2/v3/v4/v7/v8 junk (`grep '^PIN_CHECK='`), v2 prints `unmet` on every junk variant and `met` on the honest variant. This supports the lane's own `unprovable` ruling for the **frozen counter** and the hardening in v2.

Ruling: the lane's repair is measurably real (one stale pin corrected, my own re-run agrees); the frozen counter is not a discriminating scorer, as the lane says. Re-measured: line 912 and gate-registry row. Evidence-verified: the 28-pin sweep, the junk receipts and the v2 selftest tally. Calibration: **improved** (the r45–r46 stale-cell class had one surviving mismatch at entry; it is gone and the lane ships a hardened reconciler).

### C2 — v7.2 OOM tracepoint catalogue (depth)

Re-measured (plain, live upstream at tag v7.2):

- `curl …/v7.2/include/trace/events/oom.h | grep -c '^TRACE_EVENT('` → `8`; lines `12 34 76 118 134 150 166 183` = `oom_score_adj_update reclaim_retry_zone mark_victim wake_reaper start_task_reaping finish_task_reaping skip_task_reaping compact_retry` — exactly the entry's table rows.
- sha256 of the upstream header = `82f04ad4108ba9499b638fe298967f124269c0a2feb6ddbb14b1ade59c974e0d` = the committed copy `corpus/evidence/sources-r47/include_trace_events_oom.h` (`git show dd17d927:… | sha256sum`).
- `grep -n 'trace_' mm/oom_kill.c` at v7.2 → `skip_task_reaping` 567, 578; `start_task_reaping` 582; `finish_task_reaping` 595; `wake_reaper` 673; `mark_victim` 774 — all match the entry's emitting lines.
- In the export: `python3 .ufo/waves/round-47/count-c2.py dd17d927… --repo <lane>` → `C2=met events=8 rows=8 name_mismatch=0 field_mismatch=0 callsite_mismatch=0 pin_mismatch=0 source_row=ok provenance=ok`.
- Host: `sudo -n ls /sys/kernel/tracing/events/oom` lists the same eight names plus `enable`/`filter`; `mark_victim/format` has `field:uid_t uid;	offset:48;	size:4;	signed:0;`; `events/oom/enable` reads `0`; kernel `7.2.11-arch1-1`. Matches S477.
- Registry: `git show <rev>:corpus/SOURCES.md | grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}'` → 247 at `2d85e33`, 251 at `dd17d927`.

Evidence-verified: `evidence/control-c2-donothing.txt` → `C2=unmet … failed=entry_absent,pins,source_row` rc 1 at `2d85e33`; `evidence/after-c2.txt` → met rc 0; the counter's `C2_SELFTEST pass=13` is registered at `SKILL.md:939`. The counter's known survivors (used-by arm, indented rows, one-path-per-cell; lesson M5) are disclosed. Depth: **improved**. Verified, not exploratory.

### Axes (SCORECARD.md diff, spot reads)

`git diff 2d85e33 dd17d927 -- SCORECARD.md` is 22 insertions, 0 deletions; the Axes table is unchanged and no score change is claimed. Spot reads of `SKILL.md` (1 row repaired + new section), `corpus/QUALITY.md` (123–124 appended, lesson-backed), `corpus/README.md` (Round-47 coverage block appended), `corpus/SOURCES.md` (4 rows appended, S005 status/used-by edited in place) show no deletions of held content.

| axis | verdict | basis |
|---|---|---|
| calibration | improved | C1 re-measured: stale `pass=15` → `pass=22` equals the committed tool; frozen counter's non-discrimination disclosed and v2 hardening evidence-verified |
| depth | improved | C2 re-measured: 8 events, field sets, call sites, sha pinned copy |
| operability | improved | new reconciler `tools/mori-pin-check.py` with a registered 34-arm selftest (evidence-verified, not executed) |
| coverage | improved | FR13 held as a full event set plus lifecycle; README block added; previously only abstract-level S262 and queued S005 |
| freshness | unchanged | S005 re-opened, status flip only; no knowledge entry re-verified |
| adjacency | unchanged | PROVINCE.md untouched; no sibling file edited |

No owned axis harmed.

## 3. Discernment spot-check (step 3, `corpus/lessons/round-47.md` `## Gate`)

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S478 ROMA full text (staged S507) | admit | `curl -A 'Mozilla/5.0 …' https://ieeexplore.ieee.org/ielx8/4629386/11644734/11540439.pdf` (first plain curl got HTTP 418; browser UA gave 200) → sha256 `1603404d…6add2`, 4 pages; `pdftotext -layout` | **agree** | page header `3016` at line 76; the lines 122–125 read "It lever-/ages eBPF to hook into OOM-related kernel tracepoints such / as mark_victim, start_task_reaping, and fin-/ish_task_reaping" — the row's quote (17 words, ≤25) is present with only hyphenation differences; DOI `10.1109/TSC.2026.3698682` at line 72 |
| staged `oom-tracing-tracepoints-r42.md` "exactly three named tracepoints" | reject | `/home/vgpnk/Projects/shokuknow/merge/mori/knowledge/corpus/knowledge/oom-tracing-tracepoints-r42.md:12`; v7.2 `oom.h` | **agree** | the staged line says "has exactly three named tracepoints"; the paper says "such as" (three examples) and the header defines 8 `TRACE_EVENT`s — the count claim is unsupported |
| newly written row S475 | admit | upstream `oom.h` lines 76–77 | **agree** | "TRACE_EVENT(mark_victim, TP_PROTO(struct task_struct *task, uid_t uid)," is present (lines 76–77); `grep -c` → 8 |
| newly written row S476 | admit | upstream `mm/oom_kill.c` | **agree** | `trace_start_task_reaping(tsk->pid);` at 582 and `trace_mark_victim(tsk, cred->uid.val);` at 774 verbatim |
| newly written row S477 | admit | live host tracefs via `sudo -n` | **agree** | uid field line reproduces; `enable` = 0; the receipt (`host-tracefs.txt:63`) carries the same text |
| staged S501 (ROMA abstract record) | reject (already held as S262) | not re-opened beyond the lane's collision statement | not re-opened | grades `unprovable`, not harmed; no evidence against |
| `sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori` | — | rerun at `dd17d927` working tree | pass | rc 0, final line `mori ok …/corpus/SOURCES.md`; 19 inherited W04 duplicate-url warnings, one of which is S476 (also S003) |

QUALITY 124 (counts of kernel objects need the enumerating command) is lesson-backed by M3, which my spot-check supports; QUALITY 123 is lesson-backed by M1–M2.

## 4. Trend verdicts

- **expansion: improved** — one admitted entry on FR13 ground the map held only at abstract level, citing mined S475–S478; four new rows re-opened above; coverage map updated.
- **quality: unchanged** — no entry re-verified or superseded; the S005 status flip is not a re-verification; one stale registry cell repaired. No admitted entry failed its re-check (C2 checks re-derived).
- **discernment: improved** — the outside spot-check agrees with the gate on admits (S475–S478) and the staged-count reject, and the disagreement-class (M3, an over-claimed count) became QUALITY 124 with a lesson behind it. The lane's in-round honest stop on C1 (`unprovable`) also agrees with my reading.

## 5. Routed defects (lane must fix next round)

1. Commit or delete the 53 untracked paths at lane tip: `.scratch/r47-*`, `.scratch/r47w2-*`, `.ufo/waves/round-47/w2-results.json`, `w2/CritV2Junk.md`, `w2/MutV2Rebound.md`, `w2/ScoutMisroot.md`. The report says the three late seats "had not returned"; their results exist but are in no commit, so the report's 79-seat accounting (34 of 37 w2 reports) is not what the repo holds. Append a correction entry in the next round's LOG naming them.
2. The report was filed after the driver's `complete` line (17:27:24 vs 17:25:39).
3. Carry the lane's own routes: successor `count-c2.py` (used-by arm, 0–3-space rows, one path per cell); v2 selftest arms for symlink containment, argv sub-checks and case-insensitive unparsed; line-count and truncated-digest pins; lesson F4 citation precision.
4. Lesson `## Spot-check` says "no spot-check exists yet"; the next round may cite this file.
5. Refetching S478 from the IEEE URL needs a browser User-Agent; say so in the row's recheck so a plain-curl re-open does not read as `could not re-open`.

## 6. SHONEN note for the operator

All four boxes are `[~]`. The evidence behind boxes 1–3 (`SKILL.md` decision tables, the 34-arm selftest, LOG entry, PROVINCE unchanged) is checkable by a non-author; promotion stays operator-owned.
