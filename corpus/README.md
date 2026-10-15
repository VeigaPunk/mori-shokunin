# mori-shokunin — corpus

## Coverage map

| Note | Holds | Sources |
|---|---|---|
| `knowledge/observability-census-r1.md` | the six census surfaces, the live receipt, and the finding-id compare contract | `tools/mori-census.sh`, live run 2026-10-15 |
| `knowledge/observability-surfaces-r2.md` | one note per surface family (7, incl. tmux) with Measures/Status/Gaps + six measured census defects | round-2 wave, 2026-10-15 |
| `knowledge/silence-grading-r2.md` | launch-aware, authorship-aware silence-grading decision table with proven/proposed labels (implemented by census r2 — see the cutover note) | round-2 wave, derived from `lane-silence-r2.md` |
| `knowledge/progressing-weak-r2.md` | authorship discrimination proof (extractable 10-case check, 10/10) + named deferral preconditions | round-2 wave |
| `knowledge/silence-cutover-r3.md` | the r3 cutover receipt: spec-row map for census r2 `fe22a14f…`, named deltas, `:517`/`:283` hardening, selftest 25/25, frozen-oracle re-baseline 25/27 per case | round-3 wave, 2026-10-15 |
| `knowledge/verdict-machine-r4.md` | the r4 verdict machine at oracle `be0e28b8…` / census `af2d4e79…`: the matcher defect and its `want_match` fix, the sniffer channels and the named order-replay residual, the `:227` rc-gate, per-anchor-round close tracking, final tallies | round-4 wave, 2026-10-15 |
| `knowledge/verdict-machine-r5.md` | the r5 run-order close at oracle `7143ccc2…` / census `af2d4e79…` (frozen): seeded shuffle + per-run nonce, the enumerated attack-class tallies, and the residual seed channels R1–R4 | round-5 wave, 2026-10-15 |
| `knowledge/verdict-machine-r6.md` | the r6 verdict machine at oracle `3307761a…` / census `af2d4e79…` (frozen): the r5 stdout-backchannel (fd/1 header + pinned environ) and naive content-keyed classes closed — header printed only after the case loop, pins scrubbed from the exec-time environ by a one-time self re-exec, per-run salt woven into fixture content — with the attack tallies and the two named residuals (full-grammar normalizing memorizer; surviving-ancestor pin) | round-6 wave, 2026-10-15 |
| `knowledge/surfaces-r7.md` | the r7 closure of the four r2 surface Gaps (tmux relevance, memory pressure, disk write-rate, `state_rounds` values): per-gap probe design, hermetic proofs + live rows, named limits, and the additive-only oracle re-pin at census `c7c3569b…` / oracle `448f7723…` | round-7 wave, 2026-10-15 |
| `lessons/2026-10-15-errexit-pipefail-silent-crash.md` | the pipefail silent-crash class (rc 1 collides with DRIFT, no verdict line); `:517`/`:283` hardened (r3), `:227` rc-gated (r4, `verdict-machine-r4.md` §3) | round-3 wave, `/tmp` canaries |
| `lessons/2026-10-15-forgeable-oracle-visible-fixtures.md` | the forgeable-oracle class: visible case identity + a matcher taking expanded alternation literally let a no-logic census reach the ceiling (27/27); r4 opaque case dirs drop the same sniffer to 1/28 | round-4 wave, `/tmp` canaries |
| `lessons/2026-10-15-run-order-spoofing-shuffle-nonce-limits.md` | the r5 lesson: the seeded shuffle + per-run nonce close the enumerated replay classes, and the two forgers that still reach 28/28 (content memorizer; `/proc` run-header leak), with countermeasures | round-5 wave, `/tmp` canaries |
| `lessons/2026-10-15-run-secret-timing-and-content-freshness-limits.md` | the r6 lesson: when a run secret is emitted is part of the secret (timing), and freshness woven into fixture content re-prices memorization rather than closing it — the pattern-normalizing memorizer still reaches 28/28; fingerprint size drift as a derived component | round-6 wave, `/tmp` canaries |

## Known gaps

- One note per surface family: **landed round 2** — `knowledge/observability-surfaces-r2.md`
  (seven surfaces incl. tmux; the r1 "six surfaces" framing is superseded) together with
  `knowledge/silence-grading-r2.md` (decision table) and
  `knowledge/progressing-weak-r2.md` (authorship discrimination check).
- `progressing-weak`: the discrimination proof **landed round 2** (runnable check,
  10/10); the r2 grading **landed round 3 in census r2** (bullet below). The
  parent-owned admission/receipt binding is the one spec precondition still open
  (`knowledge/silence-grading-r2.md:229-230`).
- **Silence probe cutover (landed round 3):** `tools/mori-census.sh` r2
  (`VERSION=census-r2`, sha `fe22a14f…`) implements the
  `knowledge/silence-grading-r2.md` contract — launch-anchored, authorship-aware
  per-lane rows (`silent` / `progressing` / `progressing-weak` / `young` /
  `not-open` / `unavailable`), the closure predicate, `LANE_SILENT` only for row D,
  `unavailable` ≠ unhealthy, strict age gate, no fixture branching in the silence
  path. Receipts under `corpus/evidence/cutover-r3-*`; spec-row map and named
  deltas in `knowledge/silence-cutover-r3.md`. The r4 oracle `be0e28b8…`
  supersedes the frozen `505a7504…`, and the r5 oracle `7143ccc2…` supersedes
  that in turn (anti-sniff round-5 bullet below); the r6 working-tree revision
  `3307761a…` supersedes the r5 bytes in turn (anti-sniff round-6 bullet below).
- **Oracle tally (round-3 residual, closed in round 4):** the frozen oracle's
  matcher (`tools/mori-silence-cases.sh:362-365` at `505a7504…`) compared the
  `|`-joined want string literally, pinning the honest census at `matched=25
  total=27` exit 1; the fix is the exact-string `want_match()` helper
  (`be0e28b8…:342-348`, call `:389`). At oracle `be0e28b8…` / census `af2d4e79…`:
  `MORI_SILENCE_CASES: matched=28 total=28`, exit 0 — the 27 case ids and
  want-strings byte-identical to the frozen revision, plus the new
  `shape-invariance` case (`corpus/evidence/verdict-r4-20261015T173551Z-oracle.log`;
  mechanism in `knowledge/verdict-machine-r4.md` §1).
- **`:227` pipefail instance (closed in round 4):** the watchdog `state_n` pipeline
  is rc-gated at census `af2d4e79…` (`cap find` + `state_read` branch, `:233-241`,
  `:256-260`): an unreadable `.ufo/state` now renders `state_rounds=unavailable
  state_unreadable=1` in a full verdict (at the r2 bytes: rc 1, header only, 0
  verdict lines). Receipt
  `corpus/evidence/verdict-r4-20261015T173551Z-canary227.log`; class in
  `lessons/2026-10-15-errexit-pipefail-silent-crash.md`.
- **Round-4 verdict machine (oracle `be0e28b8…`, census `af2d4e79…` =
  `VERSION=census-r3`):** all four registered defects addressed — matcher, `:227`,
  the fixture-identity leak, and close tracking keyed per anchor round (a later
  `complete … round=5` no longer erases a closed r7 anchor; `:653-661`). selftest
  25 → 30 cases, `PASS (30 cases, 30 passed, 0 failed)` exit 0
  (`…-selftest.log`); live census honest: `MORI_CENSUS: DRIFT (findings=15
  drift=14 unavailable=1 surfaces=7)` exit 1, 9/9 roster lanes `progressing`,
  zero `LANE_SILENT`, the 1 `unavailable` is tmux (`…-live.log`).
- **Anti-sniff (round 4): case-id channel closed, order-replay residual named.**
  Opaque `mktemp` case dirs, no `MORI_FIXTURE` export and the `shape-invariance`
  case drop the verbatim round-3 case-id sniffer from `matched=27 total=27`
  exit 0 to `matched=1 total=28` exit 1 (`…-sniffer-v2.log`). **At the r4 oracle
  only:** an invocation-order replay that agreed with itself on both shape runs
  still reached `28/28` exit 0 (`knowledge/verdict-machine-r4.md` §2.4); the r5
  oracle's seeded shuffle drops the same replay class to `0/28` exit 1 (next
  bullet).
- **Anti-sniff (round 5): the enumerated position-keyed replay classes fail at
  oracle `7143ccc2…` (census frozen `af2d4e79…`); the residual seed channels
  stay named.** The 28 cases run in a seeded-shuffled order
  (Fisher-Yates/xorshift32; run header `SHUFFLE_SEED=` / `RUN_NONCE=` /
  `CASE_ORDER=`; same seed ⇒ same order; `MORI_SHUFFLE_SEED` / `MORI_RUN_NONCE`
  pins) and every case requires the current run's nonce token (`nonce-<N>`,
  echoed by the frozen census's disk row) in its output. Receipts
  `corpus/evidence/order-r5-20261015T180431Z-*.log`: the round-4 forgers drop
  `28/28` exit 0 (r4 snapshot) → `0/28` exit 1; a live-nonce echo with a fixed
  positional table scores `6/28` exit 1; stale/recorded replay `0/28` exit 1;
  honest census unaffected — `28/28` exit 0 at three seeds with byte-identical
  per-case grade tuples (sha `a70af583…`). **Not closed — "cannot fake a pass"
  is not claimed:** a seed-reading attacker reaches `28/28` exit 0 whenever it
  can reach the seed — `/proc/<ppid>/environ` on a `MORI_SHUFFLE_SEED`-pinned
  run (R1), or the oracle's own captured stdout (`CASE_ORDER=` in a
  regular-file capture, i.e. the `> log` receipt pattern; pipe captures do not
  expose it, 0–1/28 — R2); the nonce alone is echo-able by design and gates
  staleness only (R3); a fixture-content memorizer still reaches `28/28` (R4,
  carried from round 4) (`knowledge/verdict-machine-r5.md` §4;
  `lessons/2026-10-15-run-order-spoofing-shuffle-nonce-limits.md`). The
  oracle-reachable seed channels (R1/R2) and the naive content memorizer (R4)
  are closed at the r6 oracle `3307761a…`; the surviving-ancestor pin and the
  full-grammar normalizer stay named (round-6 bullet below).
- **Anti-sniff (round 6): the r5 stdout-backchannel and content-keyed classes
  closed at oracle `3307761a…` (census frozen `af2d4e79…`); two residuals stay
  named.** The run header (`SHUFFLE_SEED=` / `RUN_NONCE=` / `CASE_ORDER=`) now
  prints only **after** the case loop (`tools/mori-silence-cases.sh:1066-1072`),
  per-case lines redact the nonce token (`:545`), and a pinned
  `MORI_SHUFFLE_SEED`/`MORI_RUN_NONCE` is scrubbed from the exec-time
  environment by a one-time self re-exec that passes the pins on a pipe fd
  (`:207-220`); every fixture's content is per-run — committed bodies and commit
  messages carry `[nonce-<N> <salt>]` (`:417`,`:419`) and the case dir gains
  salt/blob files (`:309`,`:314-315`), with four cases binding the marker into
  untracked/dirty content (`:823`,`:836`,`:899`,`:921`). Receipts
  `corpus/evidence/backchannel-r6-20261015T{190229,190453,191216}Z-*.log` (the
  `T191216Z` set binds the final sha): fd/1 `CASE_ORDER` replay `28/28` exit 0
  (r5 bytes) → `0/28` exit 1; pinned-environ reader `28/28` → `0/28`; r5-learned
  content table `28/28` → `0/28`; fresh learn-then-replay `0/28`; honest census
  unchanged — `28/28` exit 0 across shuffles, per-case tuples byte-identical
  (sha `a70af583…`). **Not closed — named residuals:** a full-grammar
  normalizing memorizer (strips both marker grammars; a bracket-only normalizer
  dies at `24/28`, the four untracked/dirty-marker cases) reaches `28/28` exit
  0, and a pin in a *surviving ancestor's* exec-time environ (wrapper-CI
  pattern) stays readable for the whole run (`knowledge/verdict-machine-r6.md`
  §4-§5; `lessons/2026-10-15-run-secret-timing-and-content-freshness-limits.md`).
- **Surface gaps closed (round 7): census `c7c3569b…` (`VERSION=census-r4`), oracle
  `448f7723…`.** All four `knowledge/observability-surfaces-r2.md` Gaps are measured
  probes now: tmux sessions classified by pane current path under the fleet root
  (`sessions= relevant= foreign= unclassified= rule=pane_cwd_under_fleet_root`;
  `TMUX_FOREIGN_SESSION` names the session); memory graded — PSI `some`/`full` avg10
  (`MEM_PRESSURE_HIGH`) and fill `current/max` or a named host-ram floor
  (`MEM_FILL_HIGH`/`MEM_AVAIL_LOW`), thresholds labeled local; disk gains a since-boot
  write average (`io_basis=since-boot io_avg_since_boot=<dev>:<rate>Bps/<uptime>s`,
  unmeasurable targets named with a reason, never 0 B/s); `state_rounds` VALUES read
  and compared with the lane's last ledger launch round (`state_rounds_max state_lag
  state_ahead state_val_unreadable`; `WATCHDOG_STATE_LAG`/`_AHEAD` info-only). Machine
  green: selftest 30 → 45, `PASS (45 cases, 45 passed, 0 failed)` exit 0; oracle
  re-pin additive-only — 8 inserted lines, 0 deletions, 28 ids/wants byte-identical —
  `matched=28 total=28` exit 0; live `DRIFT (findings=15 drift=14 unavailable=1
  surfaces=7)` exit 1; every r6 field name still present (field-set diff). Method,
  live rows and per-gap limits: `knowledge/surfaces-r7.md`; receipts
  `corpus/evidence/surfaces-r7-20261015T1948Z-*.log`.
- **Round-7 named limits:** the instantaneous disk write rate is a bounded deferral
  (precondition: measure the wall-time a second sample adds —
  `tools/mori-census.sh:48-52`); the since-boot average counts every write to the
  device, not fleet-attributable, and the second default target `/tmp` is tmpfs on
  this host (`io_avg_unavailable=`); tmux relevance is fixture-proved only (no tmux
  server live this round, so the live row keeps the r6 unavailable shape) and
  per-session freshness stays unmeasured; the three memory thresholds are local
  placeholders that **do** flip the roll; `state_cmp` can be smaller than
  `state_rounds` for a lane with no ledger launch line.
- **Row-6 closure is presence + window only (spec residual):** a fresh,
  contentless committed marker satisfies it while the running driver would reject
  that shape (`knowledge/silence-grading-r2.md:191-197`). No frozen-behavioral
  drift pin exists (round-3 debt, carried).

- **Journal scope (measured 2026-10-15):** the census reads the USER journal only
  (0 segfault lines); the system journal holds 626, with 1228 core dumps. A
  system-journal probe with its own finding id is the named unblock.
