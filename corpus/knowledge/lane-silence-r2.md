# Lane silence — launch-aware, authorship-aware grading (round 2 operational note)

source: `PROTOCOL.md:157-168` + `:174-188` (fleet tree, read-only);
`scripts/shokunin-watchdog.sh:10,43-45,65-85,88-116`; `.ufo/watchdog.log`
(live driver log, line anchors below); `tools/mori-census.sh:16,95,484-543,852-856`
(round-1 probe — its rule divergence is `LOG.md:73-80` / `SKILL.md:111-129`);
round-2 shared contract (L1) with the parent's mid-wave closure-window refinement
(2026-10-15, quoted in "Closure" below). `young`, `not-open`, `unavailable` and the
`SURFACE lane.<id>` row shape are **round-2 contract vocabulary, not protocol text** —
the protocol anchors only silent / progressing / progressing-weak.
verified-at: 2026-10-15T04:56Z — read-only recon of the sources above (every count,
epoch and line number in this note was observed in that window; commands re-listed so
any reader can re-measure). No r2 grader behavior is claimed here — see "Evidence
status".
recheck: the per-row commands below, then `bash tools/mori-census.sh` (live) and
`bash tools/mori-silence-cases.sh [path-to-census]` (fixture driver, one PASS/FAIL per
behavioral case, terminating in `MORI_SILENCE_CASES: matched=N total=M`; exit 0 iff
all matched). Baseline (pre-cutover) receipt of record:
`corpus/evidence/round-2/live-before.txt` (r1 grader, `script_sha256=e3073a2b…`,
`window_s=900`).

## Status and scope

Detection and report only (`PROVINCE.md:16`). This note is the operational decision
table for grading a lane's round as `silent` / `progressing` / `progressing-weak` /
`young` / `not-open` / `unavailable`. It grades nothing itself; it fixes the inputs,
the rule order and the falsifiers so one grader, one scenario driver and one doc
agree. Nothing here kills, restarts or records `failed` — the integrator of record is
the only actor that records failure, and only for a graded `silent` mission
(`PROTOCOL.md:167-168`).

## Why the round-1 rolling window mis-graded (measured, not theorized)

The r1 probe (`tools/mori-census.sh:484-543`) aged from `git log -1 --format=%ct` +
`find -newermt @window` inside a `LANE_SILENCE_S` (default 7200, `:95`) window, with
neither a launch line nor an author check. Two divergences were recorded at
`LOG.md:73-80` / `SKILL.md:111-129`:

- **Ungraded missions got grades.** `PROTOCOL.md:157-158` grades a *still-open*
  mission aged from its launch line. kasegi round 17 wrapped on 2026-09-28
  (`.ufo/watchdog.log:287`: `… wrap kasegi round=17 complete; NOT respawning
  (fleet-wrap)`) yet the window grader still scored it.
- **Sibling activity became `progressing`.** The aggregator's in-window evidence was
  a gitignored `game-dev-3d` `watch.log` picked up by `find` on the fleet root plus
  `protocol-shokunin` / `shokunin-fleet` commits — `PROTOCOL.md:162-164` requires
  that be `progressing-weak` (or nothing), never `progressing`.

The r1 probe also had no `unavailable` state: an unread repo or HEAD read as epoch 0
and could surface as `LANE_SILENT` (named debt at
`corpus/knowledge/observability-census-r1.md:182-184`).

## Inputs and their live formats (measured anchors)

All commands run from the fleet root `/home/vgpnk/Projects/shokunin` (read-only).

| Fact | Format on disk | Command | Measured anchor |
|---|---|---|---|
| launch (start) | `<ISO-8601+offset> launch <lane> round=<N> pid=<pid>` **or** `… runId=<rid>` | `grep -E ' launch <lane> round=' .ufo/watchdog.log \| tail -1` | both tails live: 50 `pid=` lines vs 93 `runId=` lines; `:400` = `2026-10-15T01:50:57-03:00 launch mori round=2 pid=2685430`; committed script writes the `runId=` form (`shokunin-watchdog.sh:81`) |
| legacy launch | `<ISO ts> steer <lane> -> round <N>` | `grep -nE ' steer [a-z0-9-]+ -> round ' .ufo/watchdog.log` | 15 lines; `:2` = `… steer kake -> round 1` |
| failed launch (NOT a start) | `… launch-fail <lane> round=<N> :: …` | `grep -c 'launch-fail' .ufo/watchdog.log` | `:296-306` (six-lane `SUBSTRATE_CMD unset` burst) |
| close | `… complete <lane> round=<N>; respawning` / `… wrap <lane> round=<N> complete; NOT respawning (fleet-wrap)` | `grep -E ' (complete\|wrap) <lane> round=<N>' .ufo/watchdog.log \| tail -1` | `:287` wrap kasegi r17; `:399` complete mori r1 |
| driver marker rejection (live) | `… lane-round-failed <lane> round=<N> :: marker/contentless report; NOT advancing` | `grep -n 'lane-round-failed' .ufo/watchdog.log \| tail` | `:383,:387,:389,:393` (kaidoku r1, kasegi r17, aggregator r10, protocol r14) |
| launch epoch | field 1 parsed with the OS clock, never log mtime, never the `tick=` counter (resets on driver restart — `PROTOCOL.md:159`; tick lines `shokunin-watchdog.sh:114`) | `date -u -d '<field-1>' +%s` | `date -u -d '2026-10-15T01:50:57-03:00' +%s` = `1792039857` (measured) |
| current round | integer in `.ufo/state/<lane>.round` (advanced only when the driver accepts the report) | `cat .ufo/state/<lane>.round` | mori=2, aggregator=10 (measured; `shokunin-watchdog.sh:43,80`) |
| committed report | path `.ufo/reports/round-<N>/<lane>.md` at fleet HEAD | `git cat-file -e HEAD:.ufo/reports/round-<N>/<lane>.md; echo rc=$?` | rc 0 for `round-10/aggregator.md` and `round-14/protocol.md` (measured) |
| report path-commit time | epoch of the newest commit touching that path | `git log -1 --format=%ct -- .ufo/reports/round-<N>/<lane>.md` | aggregator r10: `ct=1790649698`, author `integrator <integrator@shokunin.local>`; protocol r14: `ct=1790650347` (measured) |
| driver tick | `INTERVAL=450` s, so *two driver ticks* = 900 s — the age gate fixtures pin | `grep -n 'INTERVAL=' scripts/shokunin-watchdog.sh` | `:10` (measured); census selftest already grades at `MORI_LANE_SILENCE_S=900` (`tools/mori-census.sh:853`) |

**Parser rule:** key on `<ts> launch <lane> round=N` and ignore the tail field —
`pid=` and `runId=` both occur. A `launch-fail` line never starts a mission. When two
launch lines share a round, **the later line in file order wins** (the log is
append-only; the clock is not the tie-breaker).

## Lifecycle / age decision table (run in order; first match wins)

`age_s = NOW_EPOCH − launch_epoch`, gate `LANE_SILENCE_S` (default 7200 at
`tools/mori-census.sh:95`; fixtures pin 900; live may use 900 = two driver ticks).
Only `age_s > LANE_SILENCE_S` **strictly** is gradeable-old; equal is young.

| # | Observable condition | Grade | Rule source | Falsifier |
|---|---|---|---|---|
| 1 | log/`grep` unreadable, launch ts field unparseable (`date -d` rc≠0), repo dir absent, or `git log` rc≠0 | `unavailable` | contract: missing data must not become silent; closes r1 debt at `observability-census-r1.md:182-184` | any `unavailable` input reported as `silent` (epoch-0 collapse) is the bug r1 was named for |
| 2 | no `launch`/`steer` line for the lane's current round anywhere in the log | `not-open` | contract extension (no protocol anchor) | a `not-open` lane counted in the silent set |
| 3 | `launch_epoch > NOW_EPOCH` (future-dated line) | `young` | contract: "future launch cannot be old" | a future launch graded old |
| 4 | a `complete`/`wrap` line for the same lane+round exists at **later file order** than the last launch line | **ungraded (closed)** | `PROTOCOL.md:157` (grade a mission "still open"); measured pair `:287`→`:388` and `:399`→`:400` show closes and relaunches as distinct lanes | grading kasegi r17 silent at a clock before `:388` (its Oct-15 relaunch) |
| 5 | the *later* of rows 4/close evidence is followed by a same-round `launch` line | **open again** (continue to authorship table) | contract: a later launch supersedes prior completion, line order; live: `:387-396` relaunch of kasegi r17, aggregator r10, protocol r14 after their Sep-28 wraps | ignoring file order (a clock-only parser reads both and cannot say which wins) |
| 6 | committed-report closure: `cat-file -e` rc 0 **AND** the newest commit touching that path has epoch `c` with `launch_epoch < c ≤ NOW_EPOCH` | **ungraded (closed)** | contract + parent refinement (2026-10-15): HEAD-committed presence AND strictly post-launch, not-future commit time. Presence alone does not close; untracked/staged alone does not close | counting the aggregator r10 marker (`ct=1790649698`) as closing round 10 while its relaunch epoch is `1792039857` — the commit predates the mission it would close by 1,390,159 s (~16.1 days). Same shape: protocol r14 `ct=1790650347` |
| 7 | `.ufo/state/<lane>.round` has advanced past the graded round | superseded; the *new* round's launch row owns the grade | contract ("advanced round counter closes") | double-grading an advanced round and its successor |
| 8 | `age_s ≤ LANE_SILENCE_S` | `young` | contract gate; `PROTOCOL.md:157-159` (two ticks) | a young lane emitting `LANE_SILENT` |
| 9 | `age_s > LANE_SILENCE_S` and open | → authorship table | `PROTOCOL.md:157` | silently skipping the authorship check (the r1 defect) |

## Authorship decision table (open-and-old missions only)

Search **all** post-launch commits, not just HEAD — a subject commit hidden behind a
sibling's newer HEAD still counts:
`git -C <repo> log --after=@<launch_epoch> --format='%an <%ae>'`.

| # | Observable condition | Grade | Rule source | Falsifier |
|---|---|---|---|---|
| A | ≥1 commit with author identity exactly `<lane>-shokunin <lane>@shokunin.local` (match `%an`/`%ae` fields verbatim — never `%cn`/`%ce`, never substring) | `progressing` | `PROTOCOL.md:160` ("a commit authored by the lane") | using `%cn`/`%ce`: measured in the last 60 fleet commits an author `João Pedro Veiga` with committer `GitHub`, and lane-shaped ids (`integrator`, `shokunin-fleet`, `ci`) that substring-match carelessly |
| B | no subject commits; files newer than `@<launch_epoch>` that are **untracked or dirty in the lane's own repo** and not explained by any post-launch committed path | `progressing` (protocol filesystem evidence; the attribution inference must be disclosed in the row) | `PROTOCOL.md:160-161` — the protocol's own probe is `find <repo> -newermt <launch-ts> -type f -not -path '*/.git/*'` | treating a clean-tracked file's mtime as subject work (see "Filesystem ≠ authorship") |
| C | no subject commits and no unexplained recent files; post-launch commits exist whose authors are **other lanes** and the checkout is clean | `progressing-weak` | `PROTOCOL.md:162-165` — named as such, never called `progressing`, **never silent or `failed` on its own** | a sibling-only (or weak) lane recorded `failed` — the protocol grants `failed` only to `silent` (`:167`) |
| D | no subject commits, no sibling commits, no unexplained recent files | `silent` → the **only** `LANE_SILENT` emission case | `PROTOCOL.md:162` ("silent means neither") | firing on commit absence alone: commit sparsity is the norm, "the absence of a commit is not silence" (`PROTOCOL.md:165-166`) |

## Exact identity policy

The subject identity is the formula pair for the lane id: author name
`<lane>-shokunin`, email `<lane>@shokunin.local`. Match the two fields **verbatim**:

```
git -C <repo> log --after=@<launch_epoch> --format='%an <%ae>' \
  | grep -Fxq "<lane>-shokunin <lane>@shokunin.local>"
```

Formula verified on lane repos, not assumed: `git -C kagi-shokunin config user.name
user.email` → `kagi-shokunin`, `kagi@shokunin.local`; same shape for `mori`. Fleet
commits carry `protocol-shokunin <protocol@shokunin.local>` (measured, `git log
--format='%an <%ae>' -5`). Two traps the verbatim match closes: substring collision
across lane-shaped names (`kake` ⊂ longer strings; `integrator`, `shokunin-fleet`,
`ci` are fleet identities, not lane ones), and committer≠author (row A falsifier).
The fleet **root's own config is `ci` / `ci@local`** (measured) — so for the
main-repo lanes (`protocol`, `aggregator` → ROOT per `tools/mori-census.sh:490-495`)
the identity must be *derived from the lane id*, never read from repo config.

## Filesystem progress is evidence, not proof of authorship

An mtime change inside a checkout says *something touched the bytes*; it does not say
the subject lane did. Siblings commit into these trees and a checkout's mtimes move
when anyone commits, pulls or wraps. Concretely for the main-repo lanes, `find` on the
fleet root must **exclude** what r1 measured as false evidence:

- nested lane repositories: `-not -path '<ROOT>/*-shokunin/*'` (ROOT contains every
  lane checkout — the r1 aggregator false-`progressing` came from a gitignored
  `game-dev-3d` `watch.log`, `LOG.md:78-80`);
- `.ufo` driver churn: `-not -path '<ROOT>/.ufo/*'` — `watchdog.log` gains lines every
  `INTERVAL=450` s (`shokunin-watchdog.sh:10,114`), so any `.ufo`-inclusive find makes
  silence unobservable by construction; `prompts/` and driver-written `state/` files
  are driver-authored;
- ignored unrelated trees — the narrow git-aware scope instead:
  `git -C <repo> ls-files -mo --exclude-standard` (tracked-modified + untracked,
  honoring `.gitignore`) intersected with the `find -newermt @<launch_epoch>` result.

Cross-check before crediting row B: compare each candidate recent file against
post-launch committed paths (`git -C <repo> log --after=@<launch_epoch> --name-only
--format= --diff-merges=off` plus `git -C <repo> status --porcelain=v1`); a clean
tracked file whose newest post-launch touch is a sibling commit's path is row C, not
B. Where a row-B grade stands on mtimes alone, the row must disclose the attribution
inference — that is the protocol's filesystem evidence, and it is weaker than a
signed commit by exactly the margin above.

## Closure by committed report: presence, window, and what it still is not

The full closure predicate (row 6): HEAD-committed presence
(`git cat-file -e HEAD:.ufo/reports/round-<N>/<lane>.md` → rc 0) **AND** the newest
commit touching that path is strictly after `launch_epoch` and no later than `NOW`.
An untracked or merely staged report file does not close (it is not at HEAD). A report
that predates a same-round relaunch does not close it — measured: both the aggregator
r10 (`ct=1790649698`) and protocol r14 (`ct=1790650347`) markers sit at HEAD with rc
0, and both predate the 2026-10-15 relaunch epoch `1792039857`.

What closure still does **not** mean:

- **Presence is not content conformance.** `cat-file -p HEAD:.ufo/reports/round-10/aggregator.md`
  begins `# aggregator round-10 closeout (marker)` — a self-declared marker, verified
  live. `PROTOCOL.md:174-188` (marker vs report) assigns content validation to the
  driver/integrator; this grader parses no report bodies (contract scope: detection
  and report). The residual risk is concrete, not generic: a *fresh*, post-launch
  contentless marker commit at the report path satisfies the presence+window
  predicate and closes the round here, while the live driver rejects exactly that
  shape (`lane-round-failed … marker/contentless report`, `watchdog.log:383-393`).
- **This is not full driver equivalence.** The committed watchdog's own `report_of()`
  (`shokunin-watchdog.sh:45`) is a presence-only file test, and the running driver
  that emitted the `lane-round-failed` verdicts is evidently stricter than that
  committed copy. The grader agrees with neither's content logic; it asserts only the
  narrower presence+window fact it can prove from git.
- Closure answers "is the mission open"; it never answers "did the work pass".

## Missing data is `unavailable`; weak is never `failed`; nothing here remediates

- Any unreadable input (missing log or line, unparseable timestamp, missing repo,
  `git` rc≠0) is `unavailable` (row 1) — reported, counted, and **never** converted
  into `silent`, `skipped`-into-invisibility, or a zero-epoch age that trips the gate.
  r1's skipped-counter behavior (`tools/mori-census.sh:504-507`) hid absent repos
  from the surface line; the r2 state set makes the hole observable.
- `progressing-weak` is a terminal grade: `PROTOCOL.md:164-165` forbids calling it
  `progressing`, `silent` or `failed`. `failed` belongs to the integrator of record
  for `silent` missions only (`:167-168`), and recording it is a ledger act, not a
  kill — mori never kills, restarts or steers (`PROVINCE.md:16-17`).
- A lane with no launch evidence is `not-open` (row 2), not silent — absence of a
  dispatch is not a stalled one.

## Output contract (round-2 spec)

Per lane: `SURFACE lane.<id>: <state> (lane=<id> round=<N> launch_epoch=<e>
age_s=<s> …; ts=…)` with state ∈ {`silent`, `progressing`, `progressing-weak`,
`young`, `not-open`, `unavailable`}. The aggregate `SURFACE silence:` line is
retained with per-state counts. `FINDING LANE_SILENT severity=warn` fires **only** for
row D (old + open + no attributed commits + no unexplained recent files) and carries
the same `lane= round= launch_epoch= age_s=` context — replacing the r1
`head_epoch= newest_epoch=` pair (`tools/mori-census.sh:537`, visible in
`corpus/evidence/round-2/live-before.txt:28-29`). No automatic `failed`, kill or
restart anywhere in the output path.

## Evidence status (what is claimed, what is not)

- **Claimed and re-verifiable by the commands above:** every line anchor, log format
  (15 steer / 93 `runId=` / 50 `pid=` launch lines), the two marker reports at HEAD
  with commit epochs `1790649698` / `1790650347`, relaunch epoch `1792039857`,
  `INTERVAL=450`, identities (`kagi-`/`mori-shokunin`, `ci@local` root), state files
  (mori=2, aggregator=10), and the r1 divergences already recorded in `LOG.md:73-80`.
- **Supplied by sibling seats, pending parent confirmation at binding:** the
  pre-cutover baseline `corpus/evidence/round-2/live-before.txt:13`
  (`silent=2 progressing=16 progressing_weak=0 skipped=0 window_s=900`, silent lanes
  kaidoku and kama at `:28-29`) — recorded here as the *before* half of the delta, not
  measured by this seat beyond quoting the file.
- **Not claimed:** any post-cutover census output, any scenario-case count
  (`matched=N total=M`), any live per-lane r2 grades, and every consequence that would
  make this note self-certifying. The parent runs the gates and the before/after
  driver once after integration and binds those receipts (into `LOG.md` /
  `SCORECARD.md`, which this seat does not edit). If the receipts contradict a table
  row, the row's falsifier names what re-anchoring is needed — fix the table, not the
  receipt.

## Prepared cutover for the parent's files (NOT applied by this seat)

- `SKILL.md:19` row → surface `launch line + post-launch authorship (this note)`,
  never-grades `a closed or not-open mission`, states
  `silent / progressing / progressing-weak / young / not-open / unavailable`.
- `SKILL.md:111-129` heading `Lane-silence grading is a PROVISIONAL approximation` →
  retitle to point at `corpus/knowledge/lane-silence-r2.md` **only after** the parent's
  receipts land; until then the section accurately describes the r1 probe and must
  stay as-is.
- `corpus/README.md` coverage map → add
  `knowledge/lane-silence-r2.md | launch-aware, authorship-aware silence decision table + live format anchors | PROTOCOL.md:157-168, .ufo/watchdog.log, shokunin-watchdog.sh`;
  retire the "`progressing-weak` … deferred" bullet (`:13-14`) in the same commit that
  ships the author check.
