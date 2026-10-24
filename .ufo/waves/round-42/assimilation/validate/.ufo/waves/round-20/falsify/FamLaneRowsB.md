HOLDS — 6/6 AGREE (class `live-state`). Every cause pointer I re-derived holds. No row lacks a valid pointer; three rows need added pointers and the register's dissent premise needs correcting (§3). None of this changes a class.

Scope: seat MoriR20.FamLaneRowsB, leaf, no subagents. Census NOT executed (not in my item). Lane rows derived from census source, `.ufo/watchdog.log` (ledger), `.ufo/state/*.round` and git. Seat report `build/TokSilenceA.md` used as a lead only (§4).

## 1. Per-token verdicts

| token | class | verdict | cause re-derived | pointer note |
|---|---|---|---|---|
| +subject_commits | live-state | AGREE | aggregator row-B→row-A via commit 1bcf59e | add 1bcf59e and watchdog.log:390 (P2) |
| +window | live-state | AGREE | same | same (P2) |
| -attribution | live-state | AGREE | aggregator row-B line removed; row-A precedes row-B | none |
| -rowb_files | live-state | AGREE | same | none |
| -subject_commits | live-state | AGREE | kagi, kengaku, kake → row-6; kumitate → row-4; kama → row-8 | kumitate and kama causes absent from row; 204807e not operative (P3) |
| -window | live-state | AGREE | same five lanes | same (P3) |

## 2. Evidence re-derived

**Time window.** NOW ∈ [1792577885, 1792578120) = [07:18:05, 07:22:00)-03. Lower: entering drift ran "after the 07:18:05-03 launch" (`c1-drift-entering.json:6`; `watchdog.log:584`). Upper: `corpus/knowledge/drift-repin-r20.md:56` says "before 10:22Z"; mado round-21 report `850b075` (ct 1792578159 = 07:22:39-03) would otherwise add a sixth lane to `-subject_commits`.

**Baseline (`corpus/evidence/baseline-r10-20261015T2231Z.json`).** L14 aggregator: `basis=row-B rowb_files=<V> attribution=inference example=<V>`. L13, L15–21 (protocol, kasegi, kengaku, kake, kumitate, kotoba, kagi, kama): `basis=row-A subject_commits=yes window=launch..NOW`. L4 masks `rowb_files` and `example`, not `attribution`, `subject_commits` or `window`. So the six are key-presence changes, not masking artifacts.

**Census (`tools/mori-census.sh`, sha256 87b8d680 at 2061780 and at HEAD).**
- Ladder (HEAD): row-4 `:2362–2364`, row-6 `:2409–2411`, row-8 `:2377`, row-A `:2472–2473`, row-B `:2492–2494`. Row-A is tested before row-B.
- Key diff: `-$k` `:2860`, `+$k` `:2864` (`drift_field_report` `:2849–2868`). `drift_report` `:2874–2918` unions tokens and `sort -u`s them, so each token appears once however many lanes cause it.
- `git log -S` (mori repo) for `subject_commits=yes window=launch..NOW`, `rowb_files=$n_rowb attribution=inference`, `reason=committed-report`, `age_le_gate` → `1439c47` (r3) only. `attribution` → 8d22d18, 18d7d55, 1439c47. `rowb_files` → 5be8943, 1439c47.
- Pin blob 5be8943 (sha d7710981): `git grep` finds the row-A and row-B GL_EXTRA strings at `:1380` and `:1401`; reading the file, the row-4/6/8 strings sit at `:1312`, `:1340`, `:1325`. Same text as HEAD `:2473`, `:2494`, `:2364`, `:2411`, `:2377`. Ladder order unchanged.
- Non-text changes on these rows: env-scrub wrappers (18d7d55); branch-anchored revision `refs/heads/<branch>` (273aa74); root_rev fallback and author diagnostic moved earlier (2be8294). For this tree each gives the same row result: fleet root HEAD = refs/heads/master = `7fd7c78`, and the author diagnostic emits no row change.

**Aggregator (+subject_commits, +window, -attribution, -rowb_files).**
- Anchor: `watchdog.log:390` `launch aggregator round=10`, 2026-10-15T01:50:57-03 = 1792039857. No later aggregator launch, complete or steer line exists in the file.
- Row-6 not closed: `.ufo/reports/round-10/aggregator.md` last commit `f5d8507`, ct 1790649698 < anchor.
- Command (exit 0): `git -C /home/vgpnk/Projects/shokunin log --format='%H %ct %an <%ae>' --since=@1792039857 refs/heads/master -- . ':(exclude).ufo' ':(exclude,glob)**/*-shokunin/**'` → 305 lines. The only `aggregator-shokunin <aggregator@shokunin.local>` line is #130: `1bcf59e… 1792459053`.
- `1bcf59e`: author = committer = `aggregator-shokunin <aggregator@shokunin.local>`; ct = at = 1792459053 (2026-10-19T22:17:33-03); ancestor of master (rc 0); touches 3 non-excluded paths (first `LOG.md`).
- `window=launch..NOW` also appears in the r17 LANE_AUTHOR_MISMATCH finding text (`:2541`). That finding is absent from the drift (no `+FINDING:LANE_AUTHOR_MISMATCH` token), so it cannot produce `+window`.
- Row-7 cannot fire (`.ufo/state/aggregator.round` = 10 = anchor round). Row-A ✓.

**Lane rows (-subject_commits, -window).**

| lane | anchor (ledger) | row at NOW | cause |
|---|---|---|---|
| kagi | round 24 launch `:543` (02:43:10-03) | row-6 | `1eed508` ct 1792577229 (07:07:09-03), latest commit to `.ufo/reports/round-24/kagi.md`; `01d1c22` superseded |
| kengaku | round 26 launch `:541` (02:22:27-03) | row-6 | `9a28017` ct 1792572867 (05:54:27-03) |
| kake | round 23 launch `:558` (03:26:44-03) | row-6 | `4487889` ct 1792573299 (06:01:39-03) |
| kumitate | round 38 launch `:561` (04:04:24-03); `complete … round=38` `:579` (05:10:38-03) | row-4 (`:2362`, precedes row-6) | ledger close. `204807e` (ct 05:09:07-03) would also satisfy row-6 but is not operative |
| kama | round 21 launch `:583` (07:17:03-03) | row-8 (age 62–297 s ≤ 7200, `:2377`) | relaunch |

Still row-A (checked, no drop):
- protocol: anchor 10-15 round 14; round-14 report last ct 2026-09-29; 139 protocol-authored commits in (anchor, 07:22-03].
- kotoba: anchor 10-15 round 16; report last ct 2026-09-29; 62 subject commits in its repo, none after NOW.
- kasegi: anchor `:519` round 23 (10-20 18:30:58-03); no round-23 report; `8bf9807` ct 1792535631 in window.

Row-7 cannot fire: `.ufo/state/{kagi,kengaku,kake,kumitate,kama}.round` = 16, 13, 16, 18, 1 (stale, all below anchor round).

Sibling tokens `+reason +path +gate_s age_s basis round` come from the same lane-row pairs, are classed live-state with consistent causes, and were not re-attacked.

## 3. Defects (no class changes)
- **P1 repo qualification.** `1bcf59e 01d1c22 1eed508 9a28017 4487889 204807e` exist only in the fleet root (`/home/vgpnk/Projects/shokunin`, master). `git -C /home/vgpnk/Projects/shokunin/mori-shokunin cat-file -t 1bcf59e` → `fatal: Not a valid object name` (rc 128); in the fleet root → `commit` (rc 0). The register must name the repo.
- **P2** `+subject_commits` and `+window` evidence omit `1bcf59e` and `watchdog.log:390`. Add both.
- **P3** `-subject_commits` and `-window` evidence: add `watchdog.log:541,543,558,561,579,583` and `tools/mori-census.sh:2362-2364`. State that `204807e` is sufficient but not operative for kumitate (row-4 precedes row-6). Replace `01d1c22` with `1eed508`.
- **P4 premise.** Register `dissent` (line 18) says "census code byte-identical since r10". That is false for the file: pin blob 5be8943 (d7710981) ≠ HEAD (87b8d680); seven census commits since the pin (1f07f1d 18d7d55 8d22d18 26f6589 273aa74 2be8294 fe9fa90); `git diff --stat 5be8943 HEAD -- tools/mori-census.sh` → 2027 insertions, 116 deletions. The checked statement is per emitter (§2). `drift-repin-r20.md` §2 ("census code unchanged") needs the same scoping.
- **P5 time.** The register records no exact drift start second. The five-lane list holds only for NOW < 1792578159. Record the start second.

## 4. Seat lead (`build/TokSilenceA.md`)
Its facts agree with my re-derivation: commits, ct values, ledger lines, row mapping, `-S` history. Line-ref error: it cites `:2862` for `-$k` and `:2866` for `+$k`. Actual lines are `:2860` and `:2864` (2862 is the loop's `done`, 2866 the id fallback). Its range `2849–2868` is correct.

## 5. Bounds, tools, gaps
- Read-only: git read verbs with `--no-optional-locks`; `date`, `sha256sum`, `stat`, `cat` on `.ufo/state/*.round`; `read`/`grep` on named files. Scratch only in `/tmp/famlanerowsb/`. Not opened: `.ufo/interactive-sessions/`, `.ufo/worktrees/`, `.jj/`, `~/.omp`. Census not executed.
- Tools installed: none.
- Gaps: lane rows at NOW were derived by hand from source, not by executing it. `c1-drift-entering.json` stdout is truncated, so I used its `tokens[]` (50 entries; the six target tokens are at lines 44–45, 51, 53–55).
- Lane states have moved since measurement (kagi round 25 launched 07:23:21-03, `:585`, and reads row-8 now). Expected for live-state; the classes are measurement-time claims.
