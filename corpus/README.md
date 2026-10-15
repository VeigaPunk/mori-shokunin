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
| `lessons/2026-10-15-errexit-pipefail-silent-crash.md` | the pipefail silent-crash class (rc 1 collides with DRIFT, no verdict line); `:517`/`:283` hardened (r3), `:227` rc-gated (r4, `verdict-machine-r4.md` §3) | round-3 wave, `/tmp` canaries |
| `lessons/2026-10-15-forgeable-oracle-visible-fixtures.md` | the forgeable-oracle class: visible case identity + a matcher taking expanded alternation literally let a no-logic census reach the ceiling (27/27); r4 opaque case dirs drop the same sniffer to 1/28 | round-4 wave, `/tmp` canaries |

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
  supersedes the frozen `505a7504…` (bullets below).
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
  exit 0 to `matched=1 total=28` exit 1 (`…-sniffer-v2.log`). **Not closed in
  general:** an invocation-order replay that agrees with itself on both shape
  runs still reaches `28/28` exit 0 (`knowledge/verdict-machine-r4.md` §2.4);
  randomized case order / decoy runs are the named unblock — "cannot fake a
  pass" holds for the case-id class, not for arbitrary forgers.
- **Row-6 closure is presence + window only (spec residual):** a fresh,
  contentless committed marker satisfies it while the running driver would reject
  that shape (`knowledge/silence-grading-r2.md:191-197`). No frozen-behavioral
  drift pin exists (round-3 debt, carried).

- **Journal scope (measured 2026-10-15):** the census reads the USER journal only
  (0 segfault lines); the system journal holds 626, with 1228 core dumps. A
  system-journal probe with its own finding id is the named unblock.
