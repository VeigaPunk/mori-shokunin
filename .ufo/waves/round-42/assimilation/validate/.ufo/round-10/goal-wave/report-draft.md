# mori round 10 — goal-wave report draft (scribe seat)

Integration target: the round report (idiom of `.ufo/reports/round-9/mori-goalwave.md`;
final path `[PARENT]`, likely `.ufo/reports/round-10/mori-goalwave.md`). Parent owns the final
path, the identity and the commit binding. Every figure is bound to a landed artifact, a
receipt, or a command run at a pinned SHA; `[PARENT: …]`/`[PENDING: …]` as elsewhere. Draft
status: **v1.2** by the scribe seat, 2026-10-15T22:37Z.

- Status: `[PARENT: completion statement + verified-round-count claim 9 → 10]`
- Evidence commit: `[PARENT: wave integration commit hash under the mori identity]`
- Baseline: `6a549b9` (round-9 records; evidence `cffb37e`)
- Wave: `[PARENT: bind the wave record — batch shape, seat completion/loss counts, any backfill]`
- Report time: `[PARENT]`
- Draft basis: before-side (entering bytes census `1c49238a…` / oracle `448f7723…`,
  first-hand 21:50–21:55Z); after-side (settled census `d7710981…`, stable from 22:12:09Z
  through the battery; oracle byte-frozen). Scratch `/tmp/mori-scribe-r10/`.
- **Landing state at scribe clock:** the note (`corpus/knowledge/drift-pin-r10.md`), the
  lesson (`corpus/lessons/2026-10-15-volatile-contract-behavioral-baselines.md`), the lane
  baseline (`corpus/evidence/baseline-r10-20261015T2231Z.json`, pinned at the settled
  `d7710981…`; an interim pre-settlement pin was consolidated into it), `corpus/README.md` r10
  rows and the `SKILL.md` r10 row all landed. Named gaps: the r10 section of
  `corpus/evidence/README.md` `[PENDING]`; `SKILL.md:75` still says "56 → 65 cases" though the
  settled file has 66 (`[DEFECT for its owner]`).

## Work performed

- Selected axis **freshness** — the drift pin, the last carried freshness item (registered by
  the round-9 verdict, `SCORECARD.md:475-478`; carried since round 2).
- Registered claim: before — no baseline exists; after — `--pin`/`--drift` with a declared
  volatile-field contract, the lane's own live baseline committed under `corpus/evidence/`
  with a re-run recipe, default census output byte-unchanged (oracle 28/28, wants unchanged),
  and selftest arms for pin→drift-clean, injected-regression detection, volatile churn, and
  missing-baseline exit 2.

## Landed changes (at scribe clock)

- `tools/mori-census.sh` → `d7710981aa1c7571ff9d6fd7f75822811173010e5f4e298ac3c47fab274a0b20`
  (2833 lines; 475+/36−; `VERSION` stays `census-r5`). Ten visible revisions 21:57:55Z →
  22:12:17Z (my 20 s poller); the mechanism landed at `1ddb7ff8…` (65 cases) and
  `d7710981…` added the baseline-volatile-list comparison in `run_drift` + selftest case 66.
  Diff scope: no hunk touches old lines 299–1568 (the `emit_*` helpers, all probes and the
  `run_census` body are byte-identical); deletions confined to the usage text, the selftest
  runner and `main()`.
- Lane baseline `corpus/evidence/baseline-r10-20261015T2231Z.json` (sha `0993b235…`; 6779 B,
  39 lines; `census_sha256=d7710981…`, `pinned_ts=2026-10-15T22:26:29Z`; `mori-drift-baseline
  v1` text format despite the `.json` suffix; reads `MORI_DRIFT: none` in my run, 32 s). An
  interim pin (`…T2210Z.json`, sha `bdf46496…`, pinned at the pre-settlement `1ddb7ff8…`)
  read `none` from the settled bytes (mine, 39 s, 22:20Z; the note-writer's 22:12Z reading
  agrees) and was consolidated into the 2231Z baseline at ~22:26:58Z.
- Note `corpus/knowledge/drift-pin-r10.md` (contract `:145-188`, mask classes, measured
  churn rationale, over-mask blind spots, under-mask env caveat, re-run recipe §4, ritual §5);
  lesson `corpus/lessons/2026-10-15-volatile-contract-behavioral-baselines.md`;
  `corpus/README.md` r10 rows; `SKILL.md` r10 row. Oracle `tools/mori-silence-cases.sh`
  untouched (`448f7723…`, sha re-checked before/after my oracle run).
- `[PENDING: corpus/evidence/README.md r10 index section (receipts set + re-run recipe)]`.

## Before → after measurements (scribe first-hand)

| Item | Before at `1c49238a…` | After at `d7710981…` |
|---|---|---|
| pin/drift capability | `--pin`/`--drift` → `unknown argument`, exit 2; no baseline artifact | `--pin` → `MORI_PIN: ok` exit 0 (32–40 s; 6779 B baseline); `--drift` → `MORI_DRIFT: none` exit 0 (32–37 s) |
| drifted baseline (churn / cross-revision) | — | `none` after ~4 min of churn (55 s); `none` against the interim pre-settlement pin from the settled bytes (39 s; since consolidated away); `none` against the current settled-bytes baseline (32 s) |
| injected regression | — | `DISK_WARN_PCT` 85→84 → `MORI_DRIFT: warn_pct` exit 1; finding rename → `+FINDING:KILL_SIGNAL_JOURNAL_X -FINDING:KILL_SIGNAL_JOURNAL` exit 1; rewritten volatile list → `MORI_DRIFT: volatile_fields` exit 1 |
| absence / malformed | — | missing → exit 2 (65 ms, no census run); marker-absent / volatile-absent / empty-block → exit 2; pin write failure → exit 2; flags without path → exit 2 |
| blind spot (honest boundary) | — | `count=1→5` mutant emits `count=5` vs `count=1`, `--drift` still `none` — demonstrated, not asserted |
| selftest | `PASS (56 cases…)` | `PASS (66 cases, 66 passed, 0 failed)` exit 0 ×2, byte-identical outputs (10 r10 arms, `:2722-2798`) |
| oracle `448f7723…` | 28/28 exit 0 (r9) | 28/28 exit 0 at the settled bytes (28 `^PASS ` lines); oracle byte-frozen |
| default live output | `DRIFT (findings=15 drift=14 unavailable=1 surfaces=7)` | same verdict, stderr 0 B; per-surface key sets identical; mask(entering 21:50Z) == mask(settled 22:17:57Z) despite a 64-line raw diff |
| masked surface | — | 177 `<V>` instances; 51 distinct exact-`<V>` keys + the device-kept rate; thresholds/ids/states/cmd text unmasked (the sensitive surface) |

## Corrections and honest boundaries

1. **The counter class is a declared blind spot, demonstrated.** Magnitudes inside an
   existing finding id (`count=`, `size=`, `rowb_files=`) read `none`; ≈47% of the schema sits
   in the counter class (lesson). Bounded by: appearance/disappearance of a finding id is
   caught.
2. **The baseline records no `MORI_*` env.** Pin and drift must share the invocation; a
   roster/env difference reports drift that is an env difference (note §3.2).
3. **Mid-wave revision history.** Ten visible revisions; one pin (`pin1`) binds `1ddb7ff8…`
   and is labelled; the battery's settled-side legs bind `d7710981…`. If the census moves
   again, re-run the first legs at the final bytes.
4. **Direction of safety:** false red preferred to false green; re-pinning to silence a red
   baseline is the failure mode the ritual forbids (recorded act with a reason).
5. **Baseline consolidation observed mid-battery:** the interim 2210Z pin (pinned at the
   pre-settlement bytes) was removed by its owner at ~22:26:58Z and superseded by the 2231Z
   file pinned at the settled bytes; the current reference is the 2231Z file. The
   cross-revision reading remains evidence of behavioral stability across the revision, but
   the interim file no longer exists.
6. **Defect (not mine to fix):** `SKILL.md:75` "(56 → 65 cases, r10)" is stale against the
   settled 66; the case list there also omits the volatile-contract arm.
7. **Clock observation:** the r10 lesson dates the `72da04b8…` move at ~22:11Z; my poller
   observed it at 21:58:15Z (seat clocks in this wave differ). All my figures use my clock.

## SHONEN

- [ ] · [ ] · [ ] · [ ] — all four remain `[ ]`: no named non-author verifier; wave seats are
  the lane per protocol.

Boundaries held: detection/report only; no remediation/kills/config edits; oracle byte-frozen;
`--pin` wrote exactly the named `/tmp` paths, `--drift` nothing; fixtures/baselines under
`/tmp`; no lane file written by this seat outside `.ufo/round-10/goal-wave/`; seats made no
commits; fleet root read-only for seats. `[PARENT: confirm from the integration diff]`