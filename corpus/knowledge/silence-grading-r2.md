# Silence grading r2 — launch-aware, authorship-aware decision table for `probe_silence`

seat: **silence-rules** (round-2 flash wave, 13 seats) · lane mori-shokunin · written 2026-10-15T15:30Z
derived from: `corpus/knowledge/lane-silence-r2.md` (precursor note, sha256
`1d1d3debce4f38855bf32b36b9b1f07ab9858bf9ff054ccaa4e59ffa3d5ef8a5`),
`SCORECARD.md:32-95` (blocked round-2 attempt), `LOG.md:73-80` (round-1 correction 8) and
`LOG.md:100-190` (round 2). This seat writes this file only; SCORECARD.md and LOG.md are
parent-owned.

**Revision scope.** Line citations to `tools/mori-silence-cases.sh` below name pre-wave
revision `61db3df3` (the quarantined candidate); the shipped revision is `505a7504`, which moved
line numbers (e.g. `gc()` now `:230-258`; the sibling-hidden authorship case now `:499-501`).
Case ids and assertions are unchanged — the falsifier seat verified the shipped `assert_case`
table is byte-identical to its pre-registered registry.

**Labels.** Every rule below is `proven` or `proposed`.

- `proven` — a binding source or a measured observation exists now: protocol text, the live
  on-disk grammar measured on this host, or measured round-1 behavior. The pointer is given.
  A proven rule speaks to the *rule*; it does not mean the r2 grader implements it — at this
  note's clock the production grader is still r1 (`tools/mori-census.sh` sha256
  `e3073a2b5e89bf717c1955e7a3d7bd995bf1096d61b6887af98b4517ee92f3f2`, SCORECARD.md:60-61).
- `proposed` — introduced by the round-2 contract (precursor note / driver contract in
  `tools/mori-silence-cases.sh` / parent closure refinement) and not derivable from
  `PROTOCOL.md`. A named precondition gates it; the precondition numbers are in the
  "Named preconditions" section.

Detection and report only. Nothing here kills, restarts, records `failed` or edits host state
(`PROVINCE.md:16-17`); the integrator of record alone records failure, and only for a graded
`silent` mission (`PROTOCOL.md:167-168`).

## Supersedes — the round-1 rolling-window description

This decision table supersedes the round-1 description of lane-silence grading at:

1. `SKILL.md:111-129` — the section "Lane-silence grading is a PROVISIONAL approximation" and
   its statement that "the landed `probe_silence` uses a rolling 7200 s window with no launch
   line and no author check". **This is the primary description this note supersedes**; its
   two measured divergences (`SKILL.md:118-124`) are the correctness case for the table.
2. `tools/mori-census.sh:488-489` — the in-code description "r1 approximation without
   launch-ts ledger: window = NOW - LANE_SILENCE_S", with the implementing logic at `:497-543`
   and the deferred author check noted at `:523-527`.
3. `corpus/README.md:13-14` — the known-gap bullet "`progressing-weak` (sibling-authored
   activity) is deferred: the probe cannot yet prove authorship".
4. `SCORECARD.md:47` — the state-of-world line "`probe_silence` remains the rolling-window
   implementation; no production cutover admitted" (superseded on receipt landing).

**Effective on receipt.** The *description* is superseded from the moment the r2 cutover
receipt binds (precondition 5). Until then the running probe still behaves per the superseded
description — measured: the r1 live receipt `corpus/evidence/round-2/live-before.txt:13`
(`silent=2 progressing=16 progressing_weak=0 skipped=0 window_s=900`) and `:28-29`
(`FINDING LANE_SILENT … head_epoch=1791965515 newest_epoch=1791965515`).

**Not superseded:** `PROTOCOL.md:153-168` is the upstream authority this table implements;
`corpus/knowledge/lane-silence-r2.md` is the precursor note this table is derived from (the two
are meant to be read together, not as rivals); the LOG/SCORECARD histories keep their truth.

## Vocabulary

| State | Label | Pointer |
|---|---|---|
| `silent` / `progressing` / `progressing-weak` | proven | `PROTOCOL.md:159-165` — progressing = a commit authored by the lane **or** files modified under its repo since launch; silent = neither; sibling-authored activity alone is `progressing-weak`, named as such, never `progressing`, never silent/`failed` on its own |
| `young` / `not-open` / `unavailable`, per-lane rows | proposed — precondition 1+5 | r2 contract only: the precursor note `:8-10` calls these "round-2 contract vocabulary, not protocol text"; the driver reads them at `tools/mori-silence-cases.sh:28-35,46-48`. `unavailable` closes the proven r1 debt "an unread `HEAD` (epoch 0) can surface as `LANE_SILENT`" (`corpus/knowledge/observability-census-r1.md:182-184`) |

## Inputs and parse rules (launch-aware)

Launch evidence is read per lane, keyed on the lane's **current round** and anchored to the
**launch epoch**; never to log mtime, never to the `tick=` counter (`PROTOCOL.md:158` "age
from the launch timestamp, not the tick counter").

| Fact | Grammar / measured anchor | Label |
|---|---|---|
| launch (live) | `<ISO-8601+offset> launch <lane> round=<N> <tail>` — 147 launch lines in `.ufo/watchdog.log` (402 lines, measured 2026-10-15T15:30Z); `:400` = `2026-10-15T01:50:57-03:00 launch mori round=2 pid=2685430` | proven |
| tail field | `pid=` (50 lines) / `runId=` (93) / `mission=` (3) all occur live, plus **one untailed launch** (`.ufo/watchdog.log:3`, `launch kagi round=1`) = 147 total — ignore the tail; current writer uses `runId=` (`scripts/shokunin-watchdog.sh:81`) | proven |
| launch epoch | field 1 parsed with the OS clock: `date -u -d '2026-10-15T01:50:57-03:00' +%s` → `1792039857` (measured) | proven |
| legacy start | `<ISO ts> steer <lane> -> round <N>` — 15 lines; `:2` = `2026-09-28T15:50:55-03:00 steer kake -> round 1` | proven |
| failed launch | `… launch-fail <lane> round=<N> :: …` never starts a mission — 7 lines measured; writer `shokunin-watchdog.sh:83` | proven |
| close | `… complete <lane> round=<N>; respawning` / `… wrap <lane> round=<N> complete; NOT respawning (fleet-wrap)` — `:399` complete mori r1; `:287` wrap kasegi r17 | proven |
| driver rejection | `… lane-round-failed <lane> round=<N> :: marker/contentless report; NOT advancing` — `:383,:387,:389,:393`; evidence, not a close | proven |
| synthetic (fixture) ledger | **superseded in-wave** (revision `505a7504`): fixtures now append the **live** grammar into `watchdog.log` (`tools/mori-silence-cases.sh:194-200`); the `TIMESTAMP … ts=` shape existed only in the pre-wave candidate `61db3df3:43-45,163-166`. The census-side parser for the live grammar remains **proposed** — precondition 1 |
| order rule | append-only log; the **later** launch line for the same lane+round wins (the clock is not the tie-breaker) — measured support: relaunch lines `:355,:357,:360` and `:388,:390,:394` follow the `lane-round-failed` lines and the Sep-28 wraps; round counters not advanced (kasegi=17, aggregator=10, protocol=14) | proposed — precondition 1; basis measured |
| current round | integer in `.ufo/state/<lane>.round` — measured mori=2 aggregator=10 kasegi=17 protocol=14; the driver advances it only when it accepts the report (`shokunin-watchdog.sh:43,80`) | proven |

Parser binding (proposed — precondition 1+3): token-match ` launch <lane> round=N` and
` steer <lane> -> round N`; take the epoch from the first parseable timestamp token (field 1
in the live grammar, `ts=` in the synthetic grammar); ignore every tail field. One live
observation that motivates the grammar item: the fleet root has **no** `.ufo/timeline.log`
(measured absent), so production launch evidence is `.ufo/watchdog.log` alone.

## Lifecycle / age decision table (run in order; first match wins)

`age_s = NOW_EPOCH − launch_epoch`; gate `LANE_SILENCE_S` (production default 7200 at
`tools/mori-census.sh:95`; the driver's two ticks are 900 s — `INTERVAL=450` at
`scripts/shokunin-watchdog.sh:10` — and the existing silence selftest already grades at 900,
`tools/mori-census.sh:853-857`). Only `age_s > gate` **strictly** is gradeable-old.

| # | Observable condition | Grade | Label | Basis / precondition | Falsifier |
|---|---|---|---|---|---|
| 1 | log/ledger unreadable or missing, launch ts unparseable, repo dir absent, `git` rc≠0 | `unavailable` | proposed — precondition 1 | contract (precursor note:82); closes proven r1 debt (`observability-census-r1.md:182-184`); r1 skips absent repos (`mori-census.sh:504-507`) | any unavailable input rendered `silent` / zero-age |
| 2 | no launch/steer line for the lane's current round | `not-open` | proposed — precondition 1 | contract; no protocol anchor exists | a not-open lane counted into the silent set |
| 3 | `launch_epoch > NOW_EPOCH` | `young` | proposed — precondition 1 | contract: a future launch cannot be old | a future-dated launch graded old |
| 4 | a `complete`/`wrap` line for the same lane+round at later file order than the last launch | closed — **no grade** | proven | `PROTOCOL.md:153-157` grades only a mission "still open"; measured closes `:287`,`:399` | grading a wrapped mission — the r1 measured defect (kasegi r17, `LOG.md:73-80`, `SKILL.md:122-124`) |
| 5 | the close of row 4 is followed by a later same-round `launch` | open again — continue to the age rows | proposed — precondition 1 | contract; measured relaunch lines (inputs table) | a clock-only parser that cannot say which of two same-round events wins |
| 6 | committed report at HEAD **and** newest commit touching that path has `launch < ct ≤ NOW` | closed — **no grade** | proposed — precondition 1+4 | parent closure refinement (precursor note:151-159); measured anchors below | counting the Sep-28 marker to close the Oct-15 relaunch (gap 1,390,159 s) |
| 7 | `.ufo/state/<lane>.round` has advanced past the graded round | superseded — the new round's launch owns the grade | proposed — precondition 1 | contract | double-grading an advanced round and its successor |
| 8 | `age_s ≤ gate` | `young` | proven | `PROTOCOL.md:155-158` "more than two driver ticks" → strict `>`; two ticks = 900 s measured | a young lane emitting `LANE_SILENT` |
| 9 | `age_s > gate` and open | → authorship table | proven | `PROTOCOL.md:159-167` | silently skipping the authorship check (the r1 defect) |

Row 6 measured anchors (proven, 2026-10-15T15:30Z): `git cat-file -e
HEAD:.ufo/reports/round-10/aggregator.md` rc 0, newest path commit `ct=1790649698` author
`integrator <integrator@shokunin.local>`; same for `round-14/protocol.md` rc 0, `ct=1790650347`.
Both markers predate the Oct-15 relaunch epoch `1792039857`, so the old markers close nothing —
presence alone is not enough; the strict window is what stops them.

## Authorship decision table (open-and-old only)

Search **all** post-launch commits, not only HEAD — a subject commit hidden behind a later
sibling HEAD commit still counts (`tools/mori-silence-cases.sh:445-453` encodes that case).
Match the two author fields verbatim.

| # | Observable condition | Grade | Label | Basis / precondition | Falsifier |
|---|---|---|---|---|---|
| A | ≥1 post-launch commit with author exactly `<lane>-shokunin <lane>@shokunin.local` | `progressing` | proven | `PROTOCOL.md:160` "a commit authored by the lane"; identity formula measured (above) | HEAD-only scan; `%cn`/`%ce` misuse; substring collision (measured traps below) |
| B | no subject commits; files newer than launch that are **untracked or dirty in the lane's own repo** and not explained by any post-launch committed path | `progressing` — the row must disclose the attribution inference | proposed — precondition 1+4 | protocol basis `PROTOCOL.md:160-161` (the protocol's own probe is `find <repo> -newermt <launch-ts> -type f -not -path '*/.git/*'`); scope rules below are contract | a clean tracked file whose newest touch is a sibling commit's path promoted to subject progress (`tools/mori-silence-cases.sh:455-464`) |
| C | no subject commits and no unexplained recent files; post-launch commits exist authored by other lanes and the checkout is clean | `progressing-weak` | proven | `PROTOCOL.md:162-165` — named as such, never `progressing`, never silent/`failed` on its own | sibling-only activity recorded `progressing` (the r1 aggregator defect, `LOG.md:78-80`) or `failed` |
| D | no subject commits, no sibling commits, no unexplained recent files | `silent` — the **only** `LANE_SILENT` emission | proven | `PROTOCOL.md:162,165-167` — commit sparsity is the norm; the absence of a commit is not silence; `failed` belongs to the integrator, silent-only | firing on commit absence alone |

## Exact identity policy (proven)

Subject identity is the formula pair for the lane id:

```
git -C <repo> log --after=@<launch_epoch> --format='%an <%ae>' \
  | grep -Fxq "<lane>-shokunin <lane>@shokunin.local>"
```

- Formula measured on lane repos, not assumed: `git -C kagi-shokunin config user.name
  user.email` → `kagi-shokunin` / `kagi@shokunin.local`; same shape for `mori`
  (`mori-shokunin` / `mori@shokunin.local`).
- The fleet **root** repo's own config is `ci <ci@local>` (measured) — for the main-repo lanes
  (`protocol`, `aggregator` → ROOT, `tools/mori-census.sh:490-495`) the identity must be
  *derived from the lane id*, never read from repo config. Both exact pairs exist live:
  `protocol-shokunin <protocol@shokunin.local>` (57 of the fleet root's last 400 commits) and
  `aggregator-shokunin <aggregator@shokunin.local>` (10).
- The verbatim pair match closes measured traps in the fleet root's last 400 commits: human
  author `<operator ambient git identity withheld>` (56; plus one accented `João` spelling),
  fleet identities `ci <ci@local>` (74), `shokunin <shokunin@local>` (22),
  `shokunin-fleet <fleet@shokunin.local>` (20), `integrator <integrator@shokunin.local>` (6),
  and near-miss lane names `kagi <kagi@shokunin.local>` (1) and
  `kumitate <kumitate@shokunin.local>` (1) — lane-shaped emails whose names do not carry the
  exact `<lane>-shokunin` shape.
- Never `%cn`/`%ce`: author≠committer is measured in fleet history (precursor note:100 —
  author `João Pedro Veiga` with committer `GitHub`; not re-measured by this seat).
- Substring matching is unsafe: `kake` is a substring of longer strings, and identity fields
  collide across lane-shaped names — `tools/mori-silence-cases.sh:482-498` encodes the name
  and email substring traps (`kagi-helper-shokunin`, `kagi-helper@shokunin.local` must both
  grade `progressing-weak`).

## Filesystem scope for row B (proposed — precondition 1+4)

An mtime change says *something touched the bytes*; it does not say the subject lane did.
Proposed scope:

- child lanes: the lane's own repo `<ROOT>/<lane>-shokunin` (`mori-census.sh:490-495`);
- main-repo lanes (`protocol`, `aggregator` → ROOT): exclude nested `<ROOT>/*-shokunin/*`
  checkouts and `<ROOT>/.ufo/*` driver churn — `watchdog.log` gains a line every 450 s, so a
  `.ufo`-inclusive `find` makes silence unobservable by construction
  (`shokunin-watchdog.sh:10,114`);
- cross-check candidates against `git -C <repo> ls-files -mo --exclude-standard` and the
  post-launch committed paths (`git log --after=@<launch_epoch> --name-only`). A clean tracked
  file whose newest post-launch touch is a sibling commit's path is row C, not B
  (`tools/mori-silence-cases.sh:455-464`).

Measured r1 falsifier (proven): the aggregator's in-window "progress" was a gitignored
`game-dev-3d` `watch.log` on the fleet root plus `protocol-shokunin`/`shokunin-fleet` commits —
`LOG.md:78-80`, `SKILL.md:118-121`. `tools/mori-silence-cases.sh:571-590` encodes the
main-repo noise set (nested lane repo with fresh commits, `.ufo/state` churn under the subject
identity, ignored `work/` tree → `silent`).

## Closure by committed report (row 6 detail)

Predicate (proposed): report present at HEAD (`git cat-file -e HEAD:<path>` rc 0) **AND** the
newest commit touching that path has `launch_epoch < ct ≤ NOW_EPOCH`. An untracked or merely
staged report does not close; a report predating a same-round relaunch does not close it
(`tools/mori-silence-cases.sh:521-548`).

- Live path (protocol + driver): `.ufo/reports/round-<N>/<lane>.md` (`PROTOCOL.md:137`;
  `scripts/shokunin-watchdog.sh:45`). **Reconciled in-wave** (revision `505a7504`): fixtures now use
  the live path (`tools/mori-silence-cases.sh:576-624`); the old `reports/<lane>.md` shape existed
  only in the pre-wave candidate. Precondition 4 is closed harness-side.
- Presence is not content conformance: `PROTOCOL.md:174-190` requires a `SHONEN` heading with
  one box line per item plus minimum substance, and assigns content validation to the
  driver/integrator; this grader parses no report bodies (detection/report scope). Residual
  risk, named: a *fresh*, contentless marker committed at the path satisfies presence+window
  here while the running driver rejects that exact shape (`watchdog.log:383,387,389,393`). The
  committed driver copy is itself presence-only (`shokunin-watchdog.sh:45`); the grader asserts
  only the narrower fact it can prove from git.

## Output contract (proposed — precondition 1+5)

- Per lane: `SURFACE lane.<id>: <state> (lane=<id> round=<N> launch_epoch=<e> age_s=<s>; ts=…)`
  with state ∈ {`silent`, `progressing`, `progressing-weak`, `young`, `not-open`,
  `unavailable`} (precursor note:192-202). The scenario driver reads this row when present and
  otherwise derives the state from the aggregate counters
  (`tools/mori-silence-cases.sh:270-284`).
- Aggregate `SURFACE silence:` keeps per-state counts (`silent=` / `progressing=` /
  `progressing_weak=` / `skipped=`).
- `FINDING LANE_SILENT severity=warn` fires **only** for row D, carrying
  lane/round/launch_epoch/age_s — replacing the r1 `head_epoch=`/`newest_epoch=` pair
  (`tools/mori-census.sh:537`; the r1 pair is visible at `live-before.txt:28-29`).
- Exit: `silent` ⇒ DRIFT (rc 1, warn finding, `mori-census.sh:139-143`) when other surfaces
  are quiet; `unavailable`/`not-open`/`young` ⇒ no finding, no DRIFT — a missing surface is
  reported as `unavailable`, never as unhealthy (`SKILL.md:43`). No `failed`, kill, restart or
  steer anywhere in the output path (`PROVINCE.md:16-17`).

## Named preconditions (admission checklist)

1. **Implementation**: r2 `probe_silence` lands in `tools/mori-census.sh` (currently r1, sha
   `e3073a2b…`; no `MORI_TIMELINE_FILE` reference exists in the census — grep 2026-10-15T15:30Z).
2. **Harness**: **satisfied in-wave** (revision `505a7504`): the `gc` chain is deterministic
   stage-then-commit with `die` → exit 2; measured post-wave: `bash tools/mori-silence-cases.sh`
   runs all 27 cases → `MORI_SILENCE_CASES: matched=10 total=27`, exit 1 (the honest
   r2-contract gradient). The pre-wave failure it replaced (exit 1 in fixture setup at sha
   `61db3df3…`) is the record at `LOG.md:146-152`.
3. **Grammar**: real-vs-synthetic timeline binding under one parser (live `.ufo/watchdog.log`:
   ISO-8601+offset, tails `pid=|runId=|mission=`; fixture: `TIMESTAMP … ts=`; no live
   `$UFO/timeline.log` — measured absent).
4. **Report path**: `.ufo/reports/round-<N>/<lane>.md` (live) vs `reports/<lane>.md` (fixture).
5. **Admission/receipt**: the parent admits the r2 vocabulary/output contract and binds the
   post-cutover live receipt into LOG/SCORECARD (parent-owned; this seat edits neither).
6. **progressing-weak authorship proof**: **deferred** with precondition 1+2. Its definition:
   the driver's authorship cases pass end-to-end — subject commit hidden behind a sibling HEAD
   (`tools/mori-silence-cases.sh:445-453`), clean-checkout non-promotion / sibling-clean weak
   (`:455-464`), author-vs-committer split (`:466-480`), identity substring traps (`:482-498`)
   — terminating in `MORI_SILENCE_CASES: matched=N total=M` with `N = M`. No tally exists at
   this note's clock; nothing here claims the proof.

## Evidence status

Claimed and re-measured 2026-10-15T15:30Z (all read-only, re-runnable from the fleet root):
`.ufo/watchdog.log` 402 lines, 147 launch lines (50 `pid=` / 93 `runId=` / 3 `mission=` + 1 untailed at line 3),
15 `steer`, 7 `launch-fail`, close/reopen/rejection anchors `:287,:354-360,:383-394,:399-400`;
`date -u -d '2026-10-15T01:50:57-03:00' +%s` = `1792039857`; `.ufo/timeline.log` absent;
report markers (`cat-file -e` rc 0, `ct=1790649698` / `1790650347`, author
`integrator <integrator@shokunin.local>`); state rounds (mori=2, aggregator=10, kasegi=17,
protocol=14); identities (kagi/mori repo configs, root `ci <ci@local>`, fleet-root author
inventory over the last 400 commits); `shokunin-watchdog.sh:10,45,81,83,114`;
`PROTOCOL.md:137,153-168,174-190`; census sha `e3073a2b…`; harness sha `61db3df3…` plus its
exit-1/no-tally run; derived-from revision of `corpus/knowledge/lane-silence-r2.md`
(sha `1d1d3deb…`).

Not claimed: any r2 grader behavior, any post-cutover per-lane grade, any
`MORI_SILENCE_CASES` tally, any receipt binding, any promotion or axis movement. The live
figures above are mutable observations pinned to a clock, not a frozen baseline. If a receipt
contradicts a table row, the row's falsifier names what re-anchoring is needed — re-anchor the
table, do not rewrite the receipt. `corpus/README.md`'s coverage map and the `SKILL.md`
cutover edits are parent integration acts and are not performed here.