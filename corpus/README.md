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
| `lessons/2026-10-15-errexit-pipefail-silent-crash.md` | the pipefail silent-crash class (rc 1 collides with DRIFT, no verdict line); `:517`/`:283` hardened (r3), `:227` rc-gated (r4, `verdict-machine-r4.md` §3) | round-3 wave, `/tmp` canaries |
| `lessons/2026-10-15-forgeable-oracle-visible-fixtures.md` | the forgeable-oracle class: visible case identity + a matcher taking expanded alternation literally let a no-logic census reach the ceiling (27/27); r4 opaque case dirs drop the same sniffer to 1/28 | round-4 wave, `/tmp` canaries |
| `lessons/2026-10-15-run-order-spoofing-shuffle-nonce-limits.md` | the r5 lesson: the seeded shuffle + per-run nonce close the enumerated replay classes, and the two forgers that still reach 28/28 (content memorizer; `/proc` run-header leak), with countermeasures | round-5 wave, `/tmp` canaries |

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
  that in turn (anti-sniff round-5 bullet below).
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
  `lessons/2026-10-15-run-order-spoofing-shuffle-nonce-limits.md`).
- **Row-6 closure is presence + window only (spec residual):** a fresh,
  contentless committed marker satisfies it while the running driver would reject
  that shape (`knowledge/silence-grading-r2.md:191-197`). No frozen-behavioral
  drift pin exists (round-3 debt, carried).

- **Journal scope (measured 2026-10-15):** the census reads the USER journal only
  (0 segfault lines); the system journal holds 626, with 1228 core dumps. A
  system-journal probe with its own finding id is the named unblock.
