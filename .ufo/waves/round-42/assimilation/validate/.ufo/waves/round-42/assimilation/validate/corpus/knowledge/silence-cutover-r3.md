# Silence grading r2 cutover — round-3 acceptance note

seat: **cutover-note-writer** (round-3 flash wave, 32 seats) · lane mori-shokunin ·
written 2026-10-15T17:01Z · detection and report only; nothing here remediates.
This seat writes this file only (SCORECARD.md / LOG.md are parent-owned).

describes: `tools/mori-census.sh` at sha256
`fe22a14f0bb6d90ffed14506abfcd76153ebf31cf3cb769b97e7eec61cc2f3c9`
(`VERSION=census-r2`, `:61`) — the revision measured for every figure below. The file was
mid-edit 16:49:56–16:54:36Z (intermediate shas `e2056b1d…`, `d9e598ad…`, `952f3ba6…`,
`1fddb609…`, `35c9a0c6…`); `fe22a14f` was first seen 16:55:10Z and verified unchanged
through the last check 17:02Z. No figure in this note was measured against an
intermediate revision.
frozen oracle: `tools/mori-silence-cases.sh` sha256
`505a7504811401b13fd96f8925605e744fbb54970c8ac65ac331b053d647e580` (unmodified; verified
before and after every run — the frozen round-3 oracle).
supersedes: `corpus/knowledge/silence-grading-r2.md` §"Supersedes" items 1–4
(`SKILL.md:111-129` rolling-window text, `mori-census.sh:488-489` in-code note,
`corpus/README.md:13-14` known gap, `SCORECARD.md:47` state-of-world line) become
descriptions of superseded behavior **once the parent binds admission** (spec precondition
5, `silence-grading-r2.md:229-230` — parent-owned; this note is the cutover receipt
documentation, not the admission act). `PROTOCOL.md:153-168` remains the authority;
`corpus/knowledge/lane-silence-r2.md` remains the precursor.

## 1. What the r2 probe implements (spec row map)

All line numbers are the r2 census at `fe22a14f`. Spec pointers are
`corpus/knowledge/silence-grading-r2.md`.

| Spec element | Implementation | Verdict |
|---|---|---|
| states `silent/progressing/progressing-weak/young/not-open/unavailable` | `grade_lane` `:664-810`; per-lane row `:837` | implemented |
| launch input, live grammar `<ISO+offset> launch <lane> round=<N> <tail>` | `ledger_anchor` `:576-627`; tails ignored (token match only) | implemented |
| legacy `<ISO> steer <lane> -> round <N>` | `:603-609`, anchored `:621-622` when no launch line exists | implemented |
| order rule: later line wins, clock is not the tie-breaker | single pass, last match overwrites (`:581-618`) | implemented |
| `launch-fail` / `lane-round-failed` never start a mission | no verb match; ignored (spec `:77`) | implemented |
| launch epoch = field 1 parsed with OS clock; `ts=` fallback for the synthetic grammar | `iso_to_epoch` `:555-559`, `ledger_ts_fallback` `:561-572`, `:599-600` | implemented |
| row 1 unavailable (ledger/repo/git/tree unreadable, ts unparseable) | `:670-691`, `:699-702` | implemented |
| row 2 not-open (no launch line) | `:695-698` | implemented |
| row 3 young (future launch) | `:704-707` | implemented |
| row 4 closed (later same-round complete/wrap; no grade) | close matched later-file-order + same round `:624`, grade `:708-712` | implemented |
| row 5 reopen (close followed by later same-round launch) | relaunch becomes the anchor; prior close no longer later (`:619-623`) | implemented |
| row 6 closed by committed report | `ps_report_closed` `:648-661`: `cat-file -e HEAD:<path>` rc 0 AND newest path commit `launch < ct ≤ NOW`; called `:736-740` | implemented |
| row 7 state round advanced | `:713-719` (delta D2 below) | implemented (label reconciled) |
| row 8 young, strict `age_s > gate` | `:722-725` (`-le` → young) | implemented |
| row 9 authorship A–D | `:743-809` | implemented |
| A: subject commit, all post-launch commits, exact `%an <%ae>` line incl. closing `>` | `:747-773` (`log` not `-1`; `grep -Fxq -- "<lane>-shokunin <lane>@shokunin.local>"` `:768`; never `%cn/%ce`, never repo config) | implemented (D1-corrected recipe) |
| B: untracked/dirty recent files, attribution inference disclosed | `ls-files -mo --exclude-standard` `:728`; `in_lane_scope` `:544-553`; mtime > launch `:785-801`; disclosure `rowb_files/attribution=inference/example` `:799` | implemented (scope deltas D4) |
| C: other-authored commits only → progressing-weak | `:766-773`, `:803-807` | implemented |
| D: silent — the only `LANE_SILENT` | `:808-809`; finding only in the silent case `:825-828` | implemented |
| report path `.ufo/reports/round-<N>/<lane>.md` from the fleet root repo | `:650` (PROTOCOL.md:137; driver `report_of()`) | implemented |
| output: per-lane `SURFACE lane.<id>: <state> (…; ts=…)` | `:837` — carries lane/round/launch_epoch/age_s/basis/reason (superset, delta D6) | implemented |
| output: aggregate `SURFACE silence:` counters | `:844` — spec counters plus `young=/not_open=/unavailable=`, `skipped=0` kept (delta D5) | implemented |
| output: `FINDING LANE_SILENT` carries lane/round/launch_epoch/age_s, replaces `head_epoch=/newest_epoch=` | `:827` (`gate_s=`, `basis=row-D` added) | implemented |
| exit: silent ⇒ DRIFT when other surfaces quiet; unavailable/not-open/young ⇒ no finding, no DRIFT | only row D sets `st=drift` `:826`; unreadable surfaces counted, never unhealthy (selftest `silence: unreadable subtree …` exit 0 CLEAN) | implemented |
| `MORI_TIMELINE_FILE` override (harness expects it) | `:81` — default `$WATCHDOG_LOG`; no separate ledger file | implemented |
| no fixture branching in the silence path | zero `MORI_FIXTURE` references in `:503-845`; the only remaining branch in the file is the pre-existing r1 journal JSON arm `:358-362` (out of this move) | verified |

## 2. Deltas from the spec (named)

- **D-a — row order: age (row 8) is checked before report closure (row 6).** For a lane
  `age_s ≤ gate` that also has a fresh committed report, the probe grades `young`; the
  spec's table order would grade "closed — no grade" (rendered `not-open` by the output
  contract, as frozen case 21 shows). Both are non-DRIFT with no finding; no frozen case
  distinguishes them. Reason: the closure probe costs git calls; the age gate is cheaper
  and the observable difference is one label.
- **D-b — row 7 is rendered `not-open` (`basis=row-7`).** The spec's "superseded — the new
  round's launch owns the grade" is achieved by the last-launch-line-wins rule (`:619-623`):
  a launch line for the new round is the anchor and owns the grade. `row-7` fires only when
  the state counter is ahead of *every* launch line, i.e. no launch for the current round
  exists — where row 2's intent also yields not-open. Label-only reconciliation.
- **D-c — window composition (the rule D3 left to the cutover).** `git log --since=@launch`
  is a committer-date prefilter only; the strict window `(launch, NOW]` is applied by an
  explicit `%ct` comparison in awk (`:764-765`), and identity is matched on `%an <%ae>`
  (`:768`). This is what keeps `ct == launch` out of both attribution and closure
  (micro-semantics measured in `corpus/knowledge/progressing-weak-r2.md:107-124`).
- **D-d — root-lane scope refinement.** Rows A/C exclude `.ufo` entirely and nested
  `**/*-shokunin/**` via git pathspec (`:752`); row B keeps `.ufo/reports/**` (deliverable
  path) while excluding `.ufo` churn and nested checkouts (`in_lane_scope` `:544-553`).
  The frozen oracle pins both sides of this line: case 26 requires subject-identity
  `.ufo/state` churn NOT to confer progress; case 25 requires an untracked recent
  `.ufo/reports/` marker to confer row-B progress.
- **D-e — aggregate row shape.** Adds `young=/not_open=/unavailable=`; `skipped=0` kept so
  r1-era compare scripts still parse. Silence surface state is `unavailable` only when
  *every* roster lane is unavailable (`:841-843`); a mixed roster stays `ok`/`drift` by
  content.
- **D-f — per-lane rows and the finding carry `basis=row-*` and `reason=`/extra fields**
  beyond the required set — a superset, for auditability of which row decided.
- **D-g — cross-verb precedence.** "'launch' outranks the legacy 'steer'" (`:522-523`):
  steer anchors only when the lane has no launch line at all. The spec's parser binding
  names both tokens but not their precedence; no frozen case exercises both for one lane.

## 3. `:517` / `:283` hardening (registered) and the remaining `:227` instance

- **r1 `:517`** — the silence probe's `newest_t=$(find "$repo" … | sort -n | tail -1 | cut …)`
  construct is **deleted**. The r2 probe gates readability first: `ps_walk` (`:633-641`)
  walks directories with `cap` and grades `tree-unreadable` → `unavailable`
  (`:686-691`); file evidence comes from rc-checked `ls-files -mo` (`:728-733`).
  Evidence the crash is gone: frozen case `unreadable-git-unavailable` — r1 emitted
  *no* `MORI_CENSUS` verdict, rc 1 (before receipt, verbatim); r2 grades `unavailable`
  with verdict and rc 0. Selftest case `silence: unreadable subtree -> unavailable
  verdict, no crash` asserts both the row and `^MORI_CENSUS: CLEAN `.
- **r1 `:283`** — the waves age is read via `cap find` with an rc branch (`:296-302`):
  rc ≠ 0 increments `n_age_unread`, disclosed as `age_unreadable=` (`:320`), and no
  age-threshold finding can fire from an unprovable read. evidence: receipts-writer's
  minimal repro-vs-control (§4 of `corpus/evidence/cutover-r3-20261015T164140Z-before.log`:
  r1 repro rc 1, header only, no verdict; control rc 0 CLEAN) plus selftest case
  `waves: unreadable wave age -> no crash, no false finding` (`age_unreadable=1`).
- **NOT hardened (named, out of the registered scope): `:227`.** The watchdog probe's
  `state_n=$(find "$STATE_DIR" … | wc -l | tr -d ' ')` (`:227`) is the same bare-pipeline
  shape. Measured by this seat at `fe22a14f`: a control root runs full (rc 0, verdict,
  11 lines) while the same root with `.ufo/state` `chmod 000` exits rc 1 with the header
  line only, **0** verdict lines, 0 bytes stderr — the r1 crash signature. Independently
  measured by the lessons seat at `35c9a0c6…`
  (`corpus/lessons/2026-10-15-errexit-pipefail-silent-crash.md`, canary B, which also
  names `:220` = the r1 line number). The wave brief registered `:517`/`:283` only;
  this instance remains open and is the named follow-up.

## 4. Selftest: 14 → 25 cases (11 new + 1 reworked), all passing

Receipt: `corpus/evidence/cutover-r3-20261015T165712Z-selftest.log` (exit 0,
`MORI_CENSUS_SELFTEST: PASS (25 cases, 25 passed, 0 failed)`, census sha verified before
and after). New cases (`:1185-1311`):

`silence: subject commit post-launch -> progressing` ·
`silence: pre-launch commit only -> silent` ·
`silence: commit at ct==launch is not post-launch -> silent` ·
`silence: other-authored commit only -> progressing-weak` ·
`silence: strict age gate (age == gate) -> young` ·
`silence: synthetic ts= ledger anchor` ·
`silence: unparseable launch ts -> unavailable` ·
`silence: committed report in window -> not-open` ·
`silence: git rc!=0 -> unavailable, never silent` ·
`silence: unreadable subtree -> unavailable verdict, no crash` ·
`waves: unreadable wave age -> no crash, no false finding`

Reworked: `drift: LANE_SILENT` now constructs the row-D shape from a real-grammar launch
line instead of backdating mtimes (`:1165-1183`). Fixture-side: the dispatcher's git stub
is arg-aware (`git-rev-parse`/`git-ls-files`/`git-cat-file`/`git-log`/`git-log1`
`:931-944`) and `fx_hash` survives unreadable subtrees (`:956-959`).

## 5. Oracle re-baseline at `fe22a14f`: `matched=25 total=27`, exit 1 — per-case

Before (census `e3073a2b…`): `matched=10 total=27`, exit 1, 17 FAILs
(`corpus/evidence/cutover-r3-20261015T164140Z-before.log`; this seat's independent run at
16:41:39Z identical). After (census `fe22a14f…`): `matched=25 total=27`, exit 1; three runs
by this seat (16:56–17:02Z) case-line byte-identical, matching the receipts-writer's receipt
(`…T165712Z-oracle.log`). 15 of the 17 r1 FAILs moved to PASS; the 10 r1 PASSes held — no
regression. Justifications (case ids as in `tools/mori-silence-cases.sh`; `spec` =
`silence-grading-r2.md`, `r1`/`r2` = observed state):

| # | case | want | r1 | r2 | justification |
|---|---|---|---|---|---|
| 1 | silent-open | silent | silent P | silent P | row D `:808`; spec `:126`; finding+rc consistent |
| 2 | completed-not-open | not-open | silent F | not-open P | row 4 ledger close `:624`,`:708-712`; spec `:102` |
| 3 | young-under-gate | young | silent F | young P | row 8 `:722-725` (age 800 ≤ 900); spec `:106` |
| 4 | young-age-equals-gate | young | silent F | young P | strict `-le` at `:722`; spec `:95` "only > gate" |
| 5 | young-future-launch | young | silent F | young P | row 3 `:704-707`; spec `:101` |
| 6 | nolane-launch-not-open | not-open | silent F | not-open P | row 2 `:695-698`; `launch-fail` not a start verb (`:594-616`); spec `:77` |
| 7 | ledger-missing-not-silent | `not-open\|unavailable` | silent F | unavailable P* | row 1 ledger-unreadable `:670-674`; spec `:99`; *harness matcher artifact (below) |
| 8 | repo-missing-unavailable | unavailable | unavailable P | unavailable P | row 1 `:675-679`; spec `:99` |
| 9 | unreadable-git-unavailable | unavailable | **crash F** | unavailable P | row 1 `:680-685`; r1 crash closed (hardening §3) |
| 10 | same-round-relaunch-silent | silent | silent P | silent P | row 5: relaunch after close re-anchors (`:619-623`); spec `:103` |
| 11 | legacy-steer-open-silent | silent | silent P | silent P | steer anchor `:603-609`,`:621`; spec `:76`; row D |
| 12 | subject-postlaunch-progressing | progressing | silent F | progressing P | row A `:766-779`; spec `:123` |
| 13 | subject-hidden-behind-sibling-head | progressing | silent F | progressing P | row A scans ALL post-launch commits (`log`, not `-1`) `:747-773`; spec `:117` |
| 14 | sibling-clean-checkout-weak | progressing-weak | silent F | progressing-weak P | clean tracked file not promoted (only `ls-files -mo` paths, `:785-793`); row C `:803-807`; spec `:124-125` |
| 15 | author-sibling-committer-subject-weak | progressing-weak | silent F | progressing-weak P | identity on `%an/%ae` only (`:747`,`:768`); spec `:152` (never `%cn/%ce`) |
| 16 | author-subject-committer-sibling-progress | progressing | silent F | progressing P | row A (`:768`); spec `:123` |
| 17 | substring-name-mismatch-weak | progressing-weak | silent F | progressing-weak P | exact-line `grep -Fxq` incl. `>` (`:768`); spec `:128-135` (D1-corrected) |
| 18 | substring-email-mismatch-weak | progressing-weak | silent F | progressing-weak P | same as 17, email field |
| 19 | dirty-same-path-as-sibling-progress | progressing | progressing P | progressing P | row B dirty path `:785-801`; spec `:124`; inference disclosed |
| 20 | untracked-recent-progress | progressing | progressing P | progressing P | row B untracked mtime > launch; spec `:124` |
| 21 | committed-report-closes | not-open | silent F | not-open P | row 6 `:648-661`,`:736-740`; path-scoped newest commit; spec `:104`,`:180-197` |
| 22 | old-report-before-relaunch-silent | silent | silent P | silent P | report ct ≤ relaunch anchor does not close; spec `:185`; row D |
| 23 | report-eq-launch-no-close | silent | silent P | silent P | strict `ct > launch` in closure `:658` and attribution window `:764-765`; D3 rule |
| 24 | report-future-no-close | `progressing-weak\|silent` | progressing F | silent P* | future ct excluded from closure `:659` and window `:765` → row D; case comment allows silent; *harness matcher artifact |
| 25 | untracked-report-progress | progressing | progressing P | progressing P | report not at HEAD → not closed; `.ufo/reports/**` kept in row-B scope `:549`; spec `:530-532` |
| 26 | main-repo-noise-silent | silent | progressing F | silent P | rows A/C pathspec excludes `.ufo` + nested repos `:752`; row B scope `:544-553`; ignored tree out via `--exclude-standard`; spec `:158-178` |
| 27 | readonly-no-mutation | fingerprint | P | P | census mutates no fixture; spec `:291-293` |

### The two remaining FAILs are a frozen-oracle matcher artifact, not census behavior

`assert_case` compares with `case "$obs" in $want)` (`tools/mori-silence-cases.sh:362-365`).
A `|` introduced by parameter expansion is a **literal** character in a shell pattern, not
alternation — measured on this host, bash 5.3.15:

```
$ bash -c 'a="x|y"; for v in x y "x|y"; do case "$v" in $a) echo "$v: MATCH";; *) echo "$v: no-match";; esac; done'
x: no-match
y: no-match
x|y: MATCH
```

So `want [not-open|unavailable]` (case 7) and `want [progressing-weak|silent]` (case 24)
can only match the literal string `not-open|unavailable` / `progressing-weak|silent` —
never a real single state. Both FAIL lines show state-only mismatches (the `why` string
appends finding/rc clauses; none are present), so the finding and rc checks passed:

```
FAIL ledger-missing-not-silent: state want [not-open|unavailable] got [unavailable] via lane
FAIL report-future-no-close: state want [progressing-weak|silent] got [silent] via lane
```

For both, the observed state is inside the case's **intended** want-set (the case comments
at `:449-455` and `:604-613` say so), and it is the spec-correct one (case 7: row 1
`unavailable`; case 24: future commits filtered, → `silent`, "never not-open, never subject
progress"). The receipts-writer ran a **counterfactual witness**: a scratch copy of the
frozen oracle with only the matcher block replaced by `[[ "$obs" =~ ^($want)$ ]]` — the same
census bytes (`fe22a14f…`, sha-checked mid-run) score **`matched=27 total=27`, exit 0**
(`corpus/evidence/cutover-r3-20261015T165712Z-oracle-counterfactual.log`).

**Conclusion.** At `fe22a14f` all 27 cases satisfy their intended want-sets. The registered
end-goal `matched=N total=M` with `N = M` under the **frozen** oracle is arithmetically
unattainable for any implementation that emits single states — the honest frozen tally is
`25/27`, and the two FAILs are the matcher defect. Named unblock (future round, oracle is
frozen and guarded now): apply the one-block matcher fix; witness already recorded.

## 6. Live census honesty check (mutable spot, not a baseline)

`corpus/evidence/cutover-r3-20261015T165712Z-live.log` (two spots 16:57:14Z/16:57:30Z)
and this seat's run at 16:58:04Z: all three agree in shape — per-lane `SURFACE lane.<id>:`
rows for all 9 roster lanes, every one `progressing` (8 × `basis=row-A`, aggregator ×
`basis=row-B rowb_files=1 attribution=inference example=research/round-18-kimi-model-routing/battery/scripts/__pycache__/probes.cpython-314.pyc`),
`SURFACE silence: ok (… silent=0 progressing=9 progressing_weak=0 young=0 not_open=0 unavailable=0 skipped=0 window_s=7200 …)`,
`MORI_CENSUS: DRIFT (findings=14…)` exit 1 with zero `LANE_SILENT` findings. Against the
15:35Z r1 divergences (`progressing-weak-r2.md:158-176`): the under-credit case is gone
(kasegi is `progressing`, not silent-on-real-commits); the over-credit *mechanism* is gone
too — aggregator still reads `progressing`, but through the disclosed row-B inference on
an in-scope untracked file, not through non-aggregator commits.

Spot-checks against raw sources at 17:00Z: kama's last ledger launch line is
`2026-10-15T01:50:57-03:00 launch kama round=1 pid=2684953` and protocol's is
`… launch protocol round=14 pid=2685253` — identical to the census's parsed
`round=`/`launch_epoch=1792039857`; the aggregator row-B example file's mtime is
1792075570 > the launch epoch. The row-B inference on a `__pycache__` file is the spec's
disclosed-inference shape (scope rules `:158-166`), not asserted here to be "real"
progress — the row says `attribution=inference` and names its example. Live figures are
a pinned clock, not a frozen baseline.

## 7. Deferred / unmet / carried (named)

- **The literal `N = M` passing tally** (spec precondition 6's termination clause): unmet
  under the frozen oracle — matcher artifact, §5. The substantive half of precondition 6
  (the driver's authorship cases passing end-to-end) **is** met: cases 12–18 all PASS.
- **`:227`** watchdog `state_n` pipeline: still crashes on an unreadable `.ufo/state`
  (measured at `fe22a14f`, §3). Out of the registered `:517`/`:283` scope; the named
  follow-up for the next round; full class definition in
  `corpus/lessons/2026-10-15-errexit-pipefail-silent-crash.md`.
- **Report-body conformance**: this grader (per spec `:190-197`) checks presence + commit
  window only; a fresh, contentless committed marker still satisfies row 6 while the live
  driver would reject it. Spec-declared residual risk, carried unchanged.
- **Frozen-behavioral drift pin**: still absent (SCORECARD round-3 debt); not part of this
  move. **`SEGFAULT_SYSTEM`** (README named unblock) and the other surfaces' r2 gaps are
  outside this coverage move.
- **Precondition 5** (admission/receipt binding into LOG/SCORECARD): parent-owned; this
  note documents the receipt side only.

## 8. Evidence status

- **Claimed** (all re-runnable): census-r2 sha `fe22a14f…` (`VERSION=census-r2`);
  selftest 25/25 exit 0; oracle before 10/27 (r1 sha `e3073a2b…`) and after 25/27 at
  `fe22a14f`, three independent runs case-line-identical; counterfactual 27/27 exit 0 at
  identical census bytes; live spots at 16:57–16:58Z; canaries A (oracle case 9), C
  (selftest + before-receipt §4), B (`:227`, this seat's repro at `fe22a14f`); spec-row
  map and deltas cited at file:line. Receipt sha256:
  `bb549139…` (before), `335c7b65…` (oracle), `44208f35…` (oracle-counterfactual),
  `59d3980b…` (selftest), `913d129a…` (live) — files under `corpus/evidence/`.
- **Not claimed**: any admission or axis verdict (parent), any scalar score, any
  remediation; no census-r2 claim beyond sha `fe22a14f…` — if the file changes, re-measure
  everything here; live figures are mutable observations pinned to their clocks.