# mori-shokunin — corpus

## Coverage map

| Note | Holds | Sources |
|---|---|---|
| `knowledge/observability-census-r1.md` | the six census surfaces, the live receipt, and the finding-id compare contract | `tools/mori-census.sh`, live run 2026-10-15 |
| `knowledge/observability-surfaces-r2.md` | one note per surface family (7, incl. tmux) with Measures/Status/Gaps + six measured census defects | round-2 wave, 2026-10-15 |
| `knowledge/silence-grading-r2.md` | launch-aware, authorship-aware silence-grading decision table with proven/proposed labels (implemented by census r2 — see the cutover note) | round-2 wave, derived from `lane-silence-r2.md` |
| `knowledge/progressing-weak-r2.md` | authorship discrimination proof (extractable 10-case check, 10/10) + named deferral preconditions | round-2 wave |
| `knowledge/silence-cutover-r3.md` | the r3 cutover receipt: spec-row map for census r2 `fe22a14f…`, named deltas, `:517`/`:283` hardening, selftest 25/25, frozen-oracle re-baseline 25/27 per case | round-3 wave, 2026-10-15 |
| `lessons/2026-10-15-errexit-pipefail-silent-crash.md` | the pipefail silent-crash class (rc 1 collides with DRIFT, no verdict line); `:517`/`:283` hardened, `:227` measured still open | round-3 wave, `/tmp` canaries |

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
  deltas in `knowledge/silence-cutover-r3.md`. Frozen oracle stays `505a7504…`.
- **Frozen-oracle tally (round-3 residual):** re-baselined to
  `matched=25 total=27`, exit 1; the two FAILs (`ledger-missing-not-silent`,
  `report-future-no-close`) are a matcher artifact in the frozen oracle
  (`tools/mori-silence-cases.sh:362-365` compares the `|`-joined want string
  literally; `:455` and `:613` pass alternation strings), so the registered
  `N = M` is unreachable at that sha. A counterfactual witness at the same census
  bytes scores 27/27 exit 0
  (`corpus/evidence/cutover-r3-20261015T165712Z-oracle-counterfactual.log`); the
  one-block matcher fix is the named round-4 unblock.
- **`:227` pipefail instance (open, out of round-3 scope):** the watchdog `state_n`
  pipeline is still unhardened — measured at `fe22a14f`, an unreadable `.ufo/state`
  exits rc 1 with the header line only and 0 verdict lines. The round-3 brief
  registered `:517`/`:283` only; class and canaries in
  `lessons/2026-10-15-errexit-pipefail-silent-crash.md`.
- **Row-6 closure is presence + window only (spec residual):** a fresh,
  contentless committed marker satisfies it while the running driver would reject
  that shape (`knowledge/silence-grading-r2.md:191-197`). No frozen-behavioral
  drift pin exists (round-3 debt, carried).

- **Journal scope (measured 2026-10-15):** the census reads the USER journal only
  (0 segfault lines); the system journal holds 626, with 1228 core dumps. A
  system-journal probe with its own finding id is the named unblock.
