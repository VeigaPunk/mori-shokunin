# Mo50bRevPromptConformance — prompt-conformance review of mori round 50 (attempt 2, wave a2w1)

Seat: reviewer, leaf (no subagents, no labrat spent). Scope: the round so far — frozen contract, data
commit, wave shapes, frontier step, assimilation, considerthese, round shape, report duties, misroot and
scratch discipline — checked against the round prompt `/home/vgpnk/Projects/shokunin/.ufo/prompts/mori-round-50.md`
(§2, §2b, §4, §5, §6 items 2–10, §7) and `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-50/contract.md`
(freeze `950e99be6757a52b00e9eb70ae1a1a7bbe2ea379`).

Method: read-only throughout — `git log/show/ls-tree/status/ls-files`, file reads, the two frozen counters
re-run with `TMPDIR` inside my scratch. No lane file edited except this report; no mutating git/jj command;
no pacman (host-wide pause honored); no tool installed (nothing needed); no kernel-log MESSAGE read; no
cgroup, limit or service touched; `/home/vgpnk/Projects/shokuknow` and `/home/vgpnk/Projects/shokuknow/merge/mori`
read as bytes only. Host reads: `scripts/hyaku/disk-guard.sh status` only (MACHINE_ID, rc 0: /tmp 2 %,
/var/tmp 36 %, /fast/scratch/hyaku 25 % — 607.8 G free). Scratch
`/fast/scratch/hyaku/mori-r50/Mo50bRevPromptConformance/` (only a `tmp/` dir; counter extractions self-removed)
was deleted before this report was finalised. Frozen counters, predicates, controls and kill rules were used
as committed and none is proposed for change; where I found a counter weakness it is named as a limit, not a fix.

## Verdict (answers first)

**The landed data is conformant and both frozen claims verify.** I re-ran both counters at the data commit
and at the current tip; both print `met` and exit 0, matching the committed after-receipts. Controls were
committed (and scored at the entering tip) before the data commit; the freeze bytes are intact
(`sha256sum -c` all OK). The assimilation mechanics are all on disk and I re-verified the collision-guard
proof arms myself. The frontier step's sourced-claim half is met (S489–S491, opened 2026-10-26).

**If the round stopped now it would fail ten integration duties** (all have drafts or assignments already
inside a2w1; none is a landed-bytes defect): the round-50 lesson (Gate, Mistakes, erratum, routed notes),
the LOG.md Round-50 entry, the SCORECARD per-claim records (C2 missing entirely; C1's counting command is
a `<rev>` placeholder), QUALITY additions, the round-end census run, the round report itself (absent),
the misroot record, the scratch deletions (`.scratch/` 190 entries/26 G and 14 regenerating
`round-40/scratch/mori-conform-selftest-*` dirs), the wave-evidence commit of the untracked a2w1 files,
and the author-date report filing.

**Three discrepancies need explicit handling in the report:** the round total is 104 dispatched seats
(4 over the run-8 ceiling of 100, the excess being the crashed attempt-1 wave); the considerthese item is
split between two files/suggestions (the frozen contract names 2026-10-25 #2, the a2w1 Gate ticket names
2026-10-26 #3 — the prompt caps one still-unimplemented proposal per round); and attempt-1's 35
report-less seats have no outcome record anywhere, so they must be reported as *unknown*, never as dead
or complete.

## 1. Evidence (commands I ran, outputs, exit codes)

```
$ python3 .ufo/waves/round-50/count-c1.py 487941b9395e89678af0053cc443cdb49cdee6e3   (TMPDIR in my scratch)
C1=met items=8 axes=6 pins=2 boxes=4 mismatches=0 errors=0 hidden=0 manifest=a94551c5bc8d rev=487941b9…  exit=0
$ python3 .ufo/waves/round-50/count-c2.py 487941b9395e89678af0053cc443cdb49cdee6e3
C2=met claims=22 located=22 quote_missing=0 bad_rows=0 sources=3 source_rows=ok pins=ok provenance=ok rev=487941b9…  exit=0
```
Both also `met`, exit 0, at HEAD `4548a34dc8b4072abaa4335c1f54a9efcfcc314a`; identical to the committed
after-receipts `.ufo/waves/round-50/evidence/a2-c1-at-data.txt` / `a2-c2-at-data.txt`.

```
$ sha256sum -c .ufo/waves/round-50/evidence/freeze-sha256.txt   → every line OK (no diff line printed)
$ git show -s --format='%h a=%ad c=%cd' … → 950e99be a=c=05:45:42; 487941b9 a=09:05:32 c=09:27:40; 4548a34d c=09:31:37
$ /home/vgpnk/Projects/shokunin/scripts/hyaku/jj-lane.sh state /home/vgpnk/Projects/shokunin/mori-shokunin
  state branch=master local=4548a34d… remote=4548a34d… ahead=0 behind=0
$ grep -n 'spawned mori 50' /home/vgpnk/Projects/shokunin/.ufo/state/inline-dispatcher.log
  1603: 2026-10-26T05:58:49 spawned mori 50 w1 40
  1786: 2026-10-26T09:50:39 spawned mori 50 a2w1 64      (grep -c 'done mori 50' → 0)
$ ls /home/vgpnk/Projects/shokunin/.ufo/reports/round-50/mori.md → No such file or directory
```

Collision-guard proof, re-run by me on the committed fixture `assimilation/guard-proof/registry.md`
(indented `  | S533 |`, `   | S534 |`, 4-space `    | S539 |`, col-0 `| S900 |`):

```
col-0-only pattern  ^\|[[:space:]]*S[0-9]{3,}   → S900            (catches neither indented row)
0–3-space pattern   ^ {0,3}\|[[:space:]]*S[0-9]{3,} → S533 S534 S900
staged-ids = S533 S534 S539;  comm -12 → collisions = S533 S534   (matches the committed guard-proof/collisions)
```

Scratch-mirror validation before append: `assimilation/a2/mirror-validate.txt` — `rc=0`, 22 W04 + `ok`
(the 21 entering warnings plus the predicted S491 duplicate-URL W04), stamped
`2026-10-26T09:26:59-03:00`, i.e. before the data commit's committer time 09:27:40. The L1's own re-open
of all three sources is `assimilation/a2/live-sha-L1.txt` (three sha256, 2026-10-26T09:26:36–37).

## 2. Checklist against the prompt

| requirement (prompt section) | status | evidence / pointer |
|---|---|---|
| §2: 1–3 claims, distinct axes, ≥1 lowest non-retired axis | **met** | Two claims (contract). Entering scores at `7197160b` `SCORECARD.md` Axes table: coverage 6, operability 7, depth 5, freshness 5, calibration 5, adjacency 6 — C1 works calibration, C2 works depth, both tied-lowest, distinct axes |
| §2/§9: calibration claim counts self-assessment mismatches | **met** | Do-nothing receipt `evidence/control-c1-do-nothing.txt`: `mismatches=6` (4 axis cells + 2 pins) at entering `7197160b`; after: `mismatches=0` at data (my re-run above). It is a count, not an assertion |
| Controls committed before data | **met** | Freeze `950e99be` (05:45:42) carries `controls/` + all receipts; data `487941b9` committed 09:27:40; do-nothing receipts scored at the entering tip |
| §2 item 5: per-claim SCORECARD record (delta, evidence pointer, counting command, measured commit) + LOG motivating evidence | **pending** | `SCORECARD.md:21-25` covers C1's command but binds no measured commit (`count-c1.py <rev>` placeholder) and states no delta line; **no C2 record anywhere in SCORECARD.md**; `grep -n 'Round 50' LOG.md` → nothing. Draft ready: `a2w1/Mo50bScribeLogScorecard.md` (with `[L1 fills]` markers) |
| §2b item 1: rows written after opening; Gate records URL/access-date/quote per new row | **partly** | Rows S489–S491 landed (`corpus/SOURCES.md:268-270`, `opened 2026-10-26`; L1 re-open `assimilation/a2/live-sha-L1.txt`); the Gate block **does not exist yet** — `corpus/lessons/round-50.md` is absent (`ls corpus/lessons` ends at `round-49-verifier-spotcheck.md`). Draft ready: `a2w1/Mo50bScribeGateQuotes.md`, `a2w1/Mo50bScribeLessonGate.md` |
| §2b item 2: census before → after, both outputs + exit codes pasted | **partly** | Before: `evidence/census-start.txt` (21 W04 + `ok`, `census-rc=0`, committed in the freeze). After: **not run at the round-end tip yet**; `a2w1/Mo50bExecCensusCounts.md` measured `git archive` copies instead (entering rc 0 / 21 W04; data rc 0 / 22 W04; rows 261→264, tier A 230→233, mined +3 — exactly the predicted delta). The prompt's command must still be run live at round end and pasted |
| §2b item 3: one mined mistake into `corpus/lessons/round-50.md` `## Mistakes` | **pending** | Lesson absent; the mistake is named in the contract (self-assessment drift: SHONEN pinned 60/60 and 13/13 since r48 vs tools at 114/17; four Axes Last-change cells lagging admitted closures — visible in `control-c1-do-nothing.txt`). Draft ready: `a2w1/Mo50bScribeMistakes.md` |
| §2b item 4: ≥1 sourced claim on a row opened this round | **met** | C2 rests on S489–S491, all `opened 2026-10-26`, `used-by corpus/knowledge/oom-memcg-stat-r50.md`; entry carries `coverage-map: FR1` and 22 located-quote rows (`C2=met claims=22 located=22`) |
| §6 item 10: one theme, 1–3 entries from `merge/mori/` | **met** | One theme (FR1 memcg OOM block composition): staged `scope-charge-fields-r46` + `scope-composition-in-the-block-r47` rewritten as one entry `corpus/knowledge/oom-memcg-stat-r50.md` (source:/verified-at:/recheck: header, 22-row table, Reading rules, Limits, Boundaries; committed in salvage `9b8562a3`, unchanged through data) |
| §6 item 10: ≥1 admit and ≥1 reject in Gate | **pending** | Contract names the admits (the two staged entries → one entry) and rejects (staged own-work rows S534/S539 — notes outside the lane; the r46 tmpfs hypothesis, the r47 entry's own refutation), but the Gate block is not landed. Draft ready: `a2w1/Mo50bScribeLessonGate.md` offers a `### Spot-check` with one admit + one reject |
| §6 item 10: 0–3-space collision guard proof before first append | **met** | `assimilation/guard-proof/` committed in the freeze; I re-ran both arms (§1 above): the col-0-only pattern catches neither indented row, the 0–3-space pattern catches both, `collisions` = S533+S534 |
| §6 item 10: scratch mirror validation exit 0 before first registry append | **met** | `assimilation/a2/mirror-validate.txt` rc 0 at 09:26:59 < data committer 09:27:40; E03/E04 absent (22 W04 allowed) |
| §6 item 10: renumber by document | **met** | Landed row S489 states "adopts staged S533 renumbered by document" (`corpus/SOURCES.md:268`); S534/S539 not adopted; adopted ids continue the registry append-only (S488 → S489–S491) |
| §6 item 10: quarantine slice | **met (re-check in flight)** | `assimilation/quarantine-slice` = S244, S262, S268 (round-48 verdicts stand; none cited by the entry — the entry cites only S489–S491); `a2w1/Mo50bScoutQuarantine.md` re-derives the slice with the prompt's awk and re-runs the collision check |
| considerthese item | **discrepancy — see F2** | Contract: `considerthese/2026-10-25.md` suggestion 2 (host-path portability count), "a measurement and a QUALITY criterion this round"; the criterion already exists (`corpus/QUALITY.md:1072-1079`, QUALITY 127, landed r48) and the measurement is assigned (`a2w1/Mo50bSentHostPaths…`). But the a2w1 Gate ticket says "considerthese **2026-10-26** suggestion 3" (`a2w1-dispatch.json`, Mo50bScribeLessonGate task) — a second proposal |
| Round shape 64–100 | **discrepancy — see F1** | w1 (attempt 1) 40 seats (v1 band 32–64, spawned 40/40, dispatcher log:1603) + a2w1 64 seats (v2 band 64–128, re-validated rc 0; attack roles 27/64 = 42 % ≥ 25 %; m_flash-role 39/64 = 61 % ≥ 50 %) = **104 dispatched**, over the run-8 ceiling of 100. No a2w2 is planned (no `a2w2` in either spec) |
| §6 item 2: attempt-1 seat accounting | **pending — see F3** | 5 report artifacts (`w1/Mo50*.md`, committed in salvage), 35 seats with no report and no outcome record: no `w1-results.json`, no `done mori 50 w1` line, registry `agentId` null for all members (builder initial state — evidences neither spawn nor death). Must be reported *unknown*, per `a2w1/Mo50bCritRoundShape.md` §2 |
| §4 report contract | **pending** | `/home/vgpnk/Projects/shokunin/.ufo/reports/round-50/mori.md` does not exist (the dir holds chousa/kake/kotoba/kotodama/kumitate only). All required sections plus the §6-item-6 extras (Stale-lane line, tool installs — none), the SHONEN section (`grep -c '^## SHONEN'` must print 1 + one line per box), the `Assimilation:` line in Sources & frontier, and the round-shape paragraph are still to be written; pre-report gates: `git ls-remote origin refs/heads/master` must print the final lane hash (currently remote = local = `4548a34d`, ahead=0), and the author-date two-commit filing of carrier 1 |
| §6 item 3: misroot sweep before the report | **pending (clean so far)** | `a2w1/Mo50bExecMisrootSweep.md`: fleet-root porcelain = 153 staged adds (all `.tower/*` + `.ufo/state/inline-dispatcher.log`), 17 modified (`.ufo/state/*` baselines + watchdog.log), 1 untracked (`.ufo/state/disk-guard.log`) — **none mori's**; my own `git status --porcelain` agrees. The L1 must still run the sweep at round end and record it (expected: nothing to salvage) |
| §7 scratch discipline | **pending — see F4** | Lane `.scratch/` = 190 entries, 26 G (routed defect 4, round-49 spot-check §5 item 4 — "Ignoring is not removal"); `.ufo/waves/round-40/scratch/mori-conform-selftest-*` = **14 dirs now** (13 at ~09:33, 6 at 09:50 — they are being *regenerated* during this wave, see F4); `/fast/scratch/hyaku/mori-r50/` = 12.4 G across running a2w1 seats + the L1's `l1` dir (328 M, holds the mirror-validation tree). All deletions are round-end L1 work; mine is done |
| Wave evidence committed | **partly** | w1 spec/dispatch/registry/reports committed (salvage); a2w1 spec/dispatch committed (`4548a34d`); `a2w1.ready`, `a2w1.ready.dispatched` and the whole `a2w1/` report dir are still **untracked** — must be committed as wave evidence at round end |
| Round-49 routed carriers (contract list) | 2 of 8 done, rest pending | Carrier 2 done (selftest receipts committed: `evidence/selftests/mori-pin-check.txt` tail `PIN_CHECK_SELFTEST pass=114 fail=0 exit=0`; `mori-unlanded-check.txt` tail `UNLANDED_SELFTEST pass=17 fail=0 exit=0`; counter selftests `C1_SELFTEST pass=34 fail=0`, `C2_SELFTEST pass=31 fail=0`). Carrier 5's "two seats with no report" resolved — both round-49 reports now tracked (`git ls-files .ufo/waves/round-49` lists `Mo49ExecCounterTiming.md`, `Mo49SimpCounters.md`). Carriers 1, 3, 4, 6, 7 (partial: K4 closed for SHONEN.md via the C1 pins; R11 carve-out + randomised handle stay routed), 8 pending — drafts ready (`Mo50bScribeRoutedNotes.md`, `Mo50bExecVariantsCount.md`, `Mo50bExecAuthorDate.md`, `Mo50bExecScratchInventory.md`) |
| §3 L2 floor | **met** | Both waves batched (single dispatch each, ready-file handoff, dispatcher spawn receipts); minimum role split present in both (connector/executor/scribe/scout/reviewer/critic); planner held by the L1 (validator rejects `planner` — verified by `a2w1/Mo50bCritRoundShape.md`) |
| Wave contexts carry the required sentences | **met** | Both `w1-dispatch.json` and `a2w1-dispatch.json` contexts contain the scratch-root/TMPDIR rule, the tooling-authorization sentence, the pacman guard, and the Report-trailer path rule (keyword-checked) |
| Write scope / freeze integrity | **met** | No tracked lane file modified outside the L1's commits (`git status --porcelain`: only untracked wave paths + round-40 scratch dirs); frozen bytes match (`sha256sum -c` all OK); no seat touched SKILL/SHONEN/SCORECARD/LOG/corpus/tools/considerthese |
| L0 side channel | **none open** | `.ufo/l0-questions.md` tail has no mori round-50 entry |

## 3. What the round would still fail if it stopped now

1. **`corpus/lessons/round-50.md` does not exist.** The frontier step's mistake mining (§2b item 3), the
   assimilation Gate with ≥1 admit + ≥1 reject and per-row URL/access-date/quote (§2b item 1, §6 item 10),
   the 48-vs-47 erratum (carrier 3), the variants=26-vs-27 note (carrier 6), the D-g wording note
   (carrier 8) and the routed-7/8 notes all live there. Drafts are ready in
   `a2w1/Mo50bScribeMistakes.md`, `a2w1/Mo50bScribeLessonGate.md`, `a2w1/Mo50bScribeGateQuotes.md`,
   `a2w1/Mo50bScribeRoutedNotes.md` — the L1 must integrate them.
2. **LOG.md has no Round-50 entry** (motivating evidence, §2 item 5; erratum correction entry, carrier 3).
   Draft ready: `a2w1/Mo50bScribeLogScorecard.md`.
3. **SCORECARD.md per-claim records are incomplete**: C1's counting command is a `<rev>` placeholder with
   no bound measured commit and no explicit delta line (`SCORECARD.md:21-25`); there is **no C2 record at
   all**. Same draft ready.
4. **QUALITY.md has no round-50 criteria** (drafts 134–136 ready in `a2w1/Mo50bScribeQuality.md`,
   including the re-execution criterion that operationalizes the 2026-10-26 #3 proposal).
5. **The round-end census has not been run.** `evidence/census-start.txt` exists; the prompt requires the
   same command at round end with both outputs and exit codes pasted in the report. The peer's archive
   measurement (`a2w1/Mo50bExecCensusCounts.md`, rc 0 both ends, +3 rows) supports it but is not the
   required live round-end run.
6. **The round report is absent** (`/home/vgpnk/Projects/shokunin/.ufo/reports/round-50/mori.md`): every
   §4 section, the SHONEN section, the `Assimilation:` line, the Stale-lane line, the tool-install line
   (none), the round-shape paragraph (paste-ready draft in `a2w1/Mo50bCritRoundShape.md` §5), the
   pre-report `ls-remote` gate, and the author-date two-commit filing (carrier 1).
7. **The misroot sweep record** — pre-sweep is clean (no mori-authored stray at the fleet root), but the
   L1 must run the sweep before the report and record it.
8. **Scratch deletions**: `.scratch/` (190 entries, 26 G) and the `round-40/scratch/mori-conform-selftest-*`
   dirs (14) with the `git status --porcelain --ignored` before/after count (carrier 4); the L1's `l1`
   scratch dir (328 M); the a2w1 seat dirs; then `$HYAKU_SCRATCH/mori-r50` after landing.
9. **Wave evidence**: `a2w1.ready`, `a2w1.ready.dispatched` and `a2w1/` (49 reports + registry) are
   untracked — commit them with the round-end lane commit.
10. **a2w1 settlement accounting**: no `a2w1-results.json` at my read; the report must take seat totals
    from the results file if it exists at filing, else state "settlement not recorded at filing: N report
    files on disk at HH:MM" — never a report-file count as a settled count.

## 4. Discrepancies and risks found (detail)

**F1 — round total 104 seats, 4 over the run-8 ceiling (MED).** Dispatcher spawn receipts
(`.ufo/state/inline-dispatcher.log:1603` w1 40, `:1786` a2w1 64) give 104 seats dispatched under round 50;
run 8: "Round size unchanged: 64–100 seats in total." The excess is entirely the crashed attempt-1 wave —
no seat was added to a wave, no residual call exists, no seat name is shared between attempts
(`Mo50*` vs `Mo50b*`), and the landed v2 wave sits exactly at the 64 floor with both run-8 shares met.
The sibling precedent counts crashed predecessors in the round total (kotodama round-50: "Total 139
dispatched seats"), so "round total 64" is the one sentence this round cannot afford. The report must
print 104, name the overshoot and its cause (watchdog `.ufo/watchdog.log:1518`), and let the operator
rule. Related: the contract's `## Round shape` line says "Two v1 waves … Total 64–100"; attempt 2 ran one
v2 wave instead — a disclosed deviation (no claim predicate, counter, floor or kill rule depends on wave
shape), which the report must state in the same paragraph or the contract and report disagree on their face.

**F2 — the considerthese item is split across two suggestions (MED).** The frozen contract names
`considerthese/2026-10-25.md` suggestion 2 (host-path portability count) as this round's item — "a
measurement and a QUALITY criterion this round" — and the measurement is assigned
(`a2w1/Mo50bSentHostPaths…`; the criterion half already exists as QUALITY 127,
`corpus/QUALITY.md:1072-1079`, landed r48). But the a2w1 Gate ticket instructs the scribe to record
"considerthese **2026-10-26** suggestion 3" (`a2w1-dispatch.json`, Mo50bScribeLessonGate task;
`considerthese/2026-10-26.md:54-56`, "Re-execute what closures only evidence-verified" — the proposal the
wave's Reexec seats are acting on). The prompt caps "at most ONE still-unimplemented proposal per round"
(§6 item 10). If the lesson's Gate records both as mined proposals, the cap is breached; the report and
Gate must name exactly one mined proposal and frame the other half as criterion-completion (the QUALITY 127
measurement) or as routed-defect work (the r49 closure's "evidence-verified, not re-executed" caveat), or
disclose the second explicitly.

**F3 — attempt-1 seat outcomes are unrecordable; they must be reported as unknown (MED).** No
`w1-results.json` exists, the dispatcher log has zero `done mori 50 w1` lines, and
`w1/swarm-registry.json` carries `agentId: null` for all 40 members — which also holds for all 64 a2w1
members, so the field evidences neither spawn nor death. Five report artifacts exist (05:51–06:08); the
other 35 seats have no report and no outcome record. The prompt requires every dead seat reported with its
last error text; that text is unobtainable (host crash, `.ufo/watchdog.log:1518`). The report must use the
unknown classification and the wave-level cause, never "35 dead seats" and never "0 dead seats".

**F4 — the scratch residue is being regenerated during the very wave that must delete it (MED).**
`.ufo/waves/round-40/scratch/mori-conform-selftest-*` went 13 dirs (~09:33, my first status) → 6 (09:50,
`a2w1/Mo50bExecScratchInventory.md`) → **14 (my last count)**: the re-execution seats
(`Mo50bExecReexecR47/R48/R49` — the 2026-10-26 #3 work) run round-40–43 instruments whose hardcoded
`LANE` (`round-40/conform.py:69`) and scratch defaults recreate the dirs inside the lane tree. That is
QUALITY 127's portability defect reproducing itself, and it means the routed-defect-4 deletion and its
before/after `--ignored` count must be sequenced **after the last instrument run**, or the round lands with
the residue back on disk. `.scratch/` behaves the same way (166 → 170 ignored entries between the peer's
two snapshots; 190 entries now) because `tools/mori-pin-check.py`'s workdir default lives there — the
round-end count must likewise be taken last.

**F5 — named limits already on record (no action).** The contract's named limits stand (Score column
unchecked; pin scan covers SHONEN.md only; a located quote proves occurrence, not entailment; v7.2/cgroup-v2
only; no host OOM block read — the entry's Limits section states the same). R11 carve-out and the
randomised handle stay routed per carrier 7; the lesson must restate that so the closure does not read K4
as fully closed.

## Findings

- **MED — F1**: round total 104 dispatched seats exceeds the run-8 ceiling of 100
  (`.ufo/state/inline-dispatcher.log:1603,:1786`; run-8 rule in the round prompt §6); and the executed
  shape (w1 v1 + a2w1 v2) deviates from `contract.md` `## Round shape` ("Two v1 waves"). Remedy is
  disclosure in the report's round-shape paragraph (paste-ready draft: `a2w1/Mo50bCritRoundShape.md` §5);
  no landed byte is wrong.
- **MED — F2**: considerthese accounting split — `contract.md` names `considerthese/2026-10-25.md`
  suggestion 2; the a2w1 Gate ticket (`a2w1-dispatch.json`, Mo50bScribeLessonGate) names
  `considerthese/2026-10-26.md` suggestion 3; prompt §6 item 10 caps one still-unimplemented proposal per
  round. The Gate/report must reconcile to one mined proposal (or disclose both).
- **MED — F3**: attempt-1 settlement unrecordable — no `w1-results.json`, no `done mori 50 w1` line,
  registry `agentId` null ×40 (and ×64 for a2w1, so the field proves nothing); 5 report artifacts, 35
  seats unknown. Report as unknown with the wave-level cause (`.ufo/watchdog.log:1518`), never as dead/complete.
- **MED — F4**: scratch residue present and regenerating — `.scratch/` 190 entries / 26 G
  (routed defect 4, `corpus/lessons/round-49-verifier-spotcheck.md:112-113` "Ignoring is not removal");
  `.ufo/waves/round-40/scratch/mori-conform-selftest-*` 14 dirs and growing during a2w1 via re-execution
  seats (root cause `round-40/conform.py:69` hardcoded `LANE` — QUALITY 127's defect class). Deletion +
  `--ignored` count must be sequenced after the last instrument run.
- **MED — pending integration (would fail if skipped)**: `corpus/lessons/round-50.md` absent (Mistakes,
  Gate with ≥1 admit/≥1 reject and per-row quotes, erratum, variants note, D-g note, routed 7/8);
  `LOG.md` Round-50 entry absent; `SCORECARD.md` has no C2 claim record and C1's command is an unbound
  `<rev>` placeholder (`SCORECARD.md:21-25`); `corpus/QUALITY.md` has no round-50 criteria; round-end
  census not yet run live; `a2w1.ready*` + `a2w1/` untracked. Drafts for all of these exist inside a2w1
  reports (Mo50bScribeMistakes / Mo50bScribeLessonGate / Mo50bScribeGateQuotes / Mo50bScribeRoutedNotes /
  Mo50bScribeLogScorecard / Mo50bScribeQuality / Mo50bExecCensusCounts).
- **MED — pending report duties**: `/home/vgpnk/Projects/shokunin/.ufo/reports/round-50/mori.md` absent —
  all §4 sections, SHONEN section, `Assimilation:` line, Stale-lane line, tool-install line (none), the
  round-shape paragraph, the pre-report `ls-remote` gate, and the author-date two-commit filing
  (carrier 1); plus the misroot-sweep record (pre-sweep clean: `a2w1/Mo50bExecMisrootSweep.md`) and the
  a2w1 settlement accounting from `a2w1-results.json` or an explicit unrecorded statement.
- **LOW — instrument workdir defaults write into the lane during the wave** (`tools/mori-pin-check.py`
  workdirs under `.scratch/`; round-40–43 instruments under `.ufo/waves/round-40/scratch/`): §7-conformant
  only in that they are not `/tmp`, but they make the routed-defect-4 count a moving target (see F4).
- **LOW — named limits restated**: counter limits (Score column unchecked; hidden-scan covers SHONEN.md
  only; quote location ≠ entailment; v7.2/cgroup-v2 only; no host block read) and the still-routed R11
  carve-out + randomised handle must appear in the lesson so the closure does not overstate K4's closure.

**Verified clean (no finding)**: both counters `met` at data and HEAD (my re-runs, §1); controls committed
and scored before data; freeze bytes intact; entering scores 6/7/5/5/5/6 at `7197160b` with C1/C2 on the
two tied-lowest axes; S489–S491 opened 2026-10-26 with L1 re-open receipts; entry grounded (22 located
rows, all 3 sources, coverage-map FR1); collision-guard proof both arms (my re-run); mirror validation
rc 0 before append; renumber by document; quarantine slice consistent and none of its rows cited; census
delta exactly +3 tier-A mined rows; both waves validated under their policies with the run-8 role shares
met; both wave contexts carry the required scratch/pacman/tooling/Report-trailer sentences; no tracked
lane file modified outside the L1's commits; no L0 question open for mori round 50; lane pushed
(local = remote = `4548a34d`, ahead=0); both round-49 late-seat reports now tracked.
