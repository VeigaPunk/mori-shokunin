# Round 10 — scribe measurement ledger (working record)

Seat: scribe (round-10 goal wave, drift pin) · lane mori-shokunin · writes only under
`.ufo/round-10/goal-wave/`. Detection and report only; scratch under `/tmp/mori-scribe-r10/`.
Status: **complete at scribe clock 2026-10-15T22:35Z** — before-side at the entering bytes,
after-side at the settled `d7710981…`; every figure below is first-hand unless a source is
named.

## Pinned bytes

| Artifact | sha256 | Note |
|---|---|---|
| `tools/mori-census.sh` entering | `1c49238a7fd87277151ff5776acfb4d62fadd9d69764a02f0ede03ef0d3902d2` | r9 bytes, `census-r5`, 2394 lines |
| `tools/mori-census.sh` settled | `d7710981aa1c7571ff9d6fd7f75822811173010e5f4e298ac3c47fab274a0b20` | 2833 lines, `git diff --numstat` 475+/36− |
| `tools/mori-silence-cases.sh` (ORACLE) | `448f77238c73a5c929a898dad0f0c495fd2a66cc4b90a00ae84ede69a86beeb5` | byte-frozen all round (sha re-checked before/after my oracle run) |
| THE lane baseline `corpus/evidence/baseline-r10-20261015T2231Z.json` | `0993b23505deab2aeb05b2309bdf7dd6eaad2b82f27852491352511aa9670478` | receipts-writer's pin **at the settled bytes**; 6779 B, 39 lines; header `census_sha256=d7710981…`, `pinned_ts=2026-10-15T22:26:29Z`; my `--drift` against it → `none` exit 0 (32 s, 22:31Z) |
| interim pin `corpus/evidence/baseline-r10-20261015T2210Z.json` | was `bdf464968003ed48014ea8da23045a5112628dbf11cc164755fbdff0af4c5649` | pinned at the pre-settlement `1ddb7ff8…` (22:09:37Z); present ~22:10–22:25Z, **removed by its owner before my final clock** (consolidated into the 2231Z pin); my `none` reading against it (39 s, 22:20Z) is historical |
| my `pin1.txt` (at `1ddb7ff8…`) | `c9596585af3afaeecbf82a5e53a67b806233d4f187eed7ddbb8da1cc61b22fcd` | ephemeral `/tmp` |
| my `pin2.txt` (at `d7710981…`) | `09e56d2c419b1ed4c96ee823e14685a5f2e817b7b81c15532a1d1112e09867fe` | ephemeral `/tmp` |

Baseline commit entering the wave: `6a549b9` (round-9 records; evidence `cffb37e`).

## Before-side (first-hand, 21:50–21:55Z)

The capability does not exist at the entering bytes:

```
$ bash tools/mori-census.sh --pin /tmp/mori-scribe-r10/pin-test.txt
mori-census: unknown argument: --pin
... usage ...
exit=2
$ bash tools/mori-census.sh --drift /tmp/mori-scribe-r10/pin-test.txt
mori-census: unknown argument: --drift
exit=2
$ ls corpus/evidence/ | grep -i 'baseline\|pin'
NONE
```

Live census at entering bytes: `MORI_CENSUS: DRIFT (findings=15 drift=14 unavailable=1
surfaces=7)` exit 1, wall 48 s, stderr 0 B (`/tmp/mori-scribe-r10/before/live-entering.log`).
Per-surface key sets + finding multiset extracted (`keysets.sh`) →
`before/keysets-entering.txt`: 17 surface rows, findings WATCHDOG_STALE ×1, WATCHDOG_ABSENT
×1, WAVE_UNSETTLED_AGE ×11, KILL_SIGNAL_JOURNAL ×1, SEGFAULT_JOURNAL ×1.

## The impl's landing history (my poller, 20 s tick; seat clock)

Ten visible revisions between 21:57:55Z and 22:12:17Z; the two structurally significant ones
are `1ddb7ff8…` (the whole pin/drift mechanism, 65 cases) and `d7710981…` (+14 lines: the
baseline-volatile-list comparison in `run_drift` + selftest case 66). Intermediate:
`ef787505` → `72da04b8` → `357455e2` → `7c54e02a` → `c37b2ee6` → `9fb9256c` → `d2f7fb65` →
`6d61ff16` → `62e76cfd` → `1ddb7ff8` → `d7710981`. My verification battery binds the settled
bytes; one pin (`pin1`) was taken at `1ddb7ff8…` and is labelled as such below.

Hunk map at `d7710981` (`git diff -U0`): header comment (`+145,41`), usage text
(`-290 +332`, `-292,0 +335,6`, `-298 +346`), drift section inserted after `run_census`
(`-1569,0 +1618,262`), selftest runner + cases (`-1718,0 +2029,41`, `-1734,0 +2086`,
`-1736,33 +2088`, `-1828,0 +2149,34`, `-2367,0 +2722,73`, `-2369,0 +2797,2`), `main()`
(`-2378 +2807`, `-2381,0 +2811,2`, `-2390,0 +2822,8`). **No hunk touches old lines 299–1568**
— the `emit_*` helpers, all probe functions and the `run_census` body are byte-identical.

## Contract as landed (read from the settled file)

- `--pin <path>`: runs the live census read-only, normalizes the full output, writes the
  baseline (`run_pin` `:1795-1812`); header records `census_sha256`, `pinned_ts`,
  `volatile_fields` verbatim; write failure → exit 2; success `MORI_PIN: ok path=…` exit 0
  **whatever the census's own roll**.
- `--drift <path>`: (`run_drift` `:1815-1878`) baseline missing/unreadable/malformed
  (marker absent / `volatile_fields` absent / empty block) → exit 2; equal canonical block →
  `MORI_DRIFT: none` exit 0; different → `MORI_DRIFT: <tokens>` exit 1, tokens naming changed
  keys, `-key`/`+key`, `-FINDING:<id>`/`+FINDING:<id>`, `output-order`, `volatile_fields`
  (a baseline pinned under a different volatile list); writes nothing.
- Normalization: one `sed` pass over a captured variable (`drift_normalize` `:1652-1667`),
  no live pipes in the section. `census_sha256` is informational — behavior, not revision, is
  compared.

## First-hand battery (verbatim key lines; all at `d7710981…` unless noted)

| Leg | rc | wall | Verbatim |
|---|---|---|---|
| `--pin` (at `1ddb7ff8…`) | 0 | 32 s | `MORI_PIN: ok path=/tmp/…/pin1.txt` (baseline 6779 B, 39 lines) |
| `--drift` vs pin1, same revision | 0 | 32 s | `MORI_DRIFT: none` |
| `--drift` vs pin1, ~4 min later, cross-revision churn | 0 | 55 s | `MORI_DRIFT: none` |
| mutant: `DISK_WARN_PCT` 85→84 (from `1ddb7ff8…`) | 1 | 61 s | `MORI_DRIFT: warn_pct` |
| mutant: finding id `KILL_SIGNAL_JOURNAL`→`…_X` | 1 | 75 s | `MORI_DRIFT: +FINDING:KILL_SIGNAL_JOURNAL_X -FINDING:KILL_SIGNAL_JOURNAL` |
| oracle at settled bytes | 0 | 14 s | `MORI_SILENCE_CASES: matched=28 total=28` + 28 `^PASS ` lines; oracle sha before=after |
| default live | 1 | 62 s | `MORI_CENSUS: DRIFT (findings=15 drift=14 unavailable=1 surfaces=7)`, stderr 0 B; key sets identical to entering |
| masked identity, entering vs settled | — | — | `diff mask(live-entering 21:50Z) mask(live-a 22:17:57Z)` → empty (`MASKED-IDENTICAL`); raw line diff was 64 changed lines (32 line pairs) |
| `--selftest` ×2 | 0 | 14 s each | `MORI_CENSUS_SELFTEST: PASS (66 cases, 66 passed, 0 failed)`; the two output files are byte-identical |
| `--drift` vs the interim pin (2210Z, at `1ddb7ff8…`) | 0 | 39 s | `MORI_DRIFT: none` (22:20Z; the file was later consolidated away) |
| `--drift` vs the lane baseline (2231Z, at `d7710981…`) | 0 | 32 s | `MORI_DRIFT: none` (22:31Z) |
| my `--pin` (settled) + `--drift` (same revision) | 0/0 | 40 s/37 s | `MORI_PIN: ok`; `MORI_DRIFT: none` |
| mutant: rewritten `volatile_fields` line in pin2 | 1 | 35 s | `MORI_DRIFT: volatile_fields` |
| mutant: `DISK_WARN_PCT` 85→84 (from settled) | 1 | 31 s | `MORI_DRIFT: warn_pct` |
| mutant: `count=$c_kill`→`count=$((c_kill+4))` | 0 | 29 s | `MORI_DRIFT: none` — blind spot demonstrated: the mutant emits `count=5` where the baseline emitted `count=1` (both live greps recorded) |
| `--drift` missing baseline | 2 | 65 ms | `mori-census: --drift baseline missing: …` |
| `--drift` marker absent / no volatile list / empty block | 2 | — | `malformed (canonical marker absent)` / `malformed (volatile_fields contract absent)` / `malformed (empty canonical block)` |
| `--pin` write failure | 2 | — | `mori-census: --pin failed to write baseline path=/nonexistent-dir-xyz/b.txt` |
| `--pin`/`--drift` without path | 2 | — | `mori-census: --pin requires a baseline path` / `… --drift requires a baseline path` |

No stray writes: `git status --porcelain` after the battery lists only the wave's expected
entries (census, SKILL.md, README.md modifications; the new corpus artifacts; `.ufo/round-10/`).

## Mask coverage (measured on the settled live capture)

- 177 `<V>` value instances in the canonical block; **51 distinct `key=` tokens carry an exact
  `<V>`**, plus one partial (`io_avg_since_boot=dm-0:<V>Bps/<V>s` — device name kept by design).
- Unmasked tokens include the sensitive constants/contract words: `warn_pct=85`, `crit_pct=95`,
  `stale_threshold_s=900`, `threshold_s=7200`, `psi_warn_avg10=10`, `window_s=7200`, plus
  `basis=`, `severity=`, `rc=`, `log=`, `cmd=`, ids and states.
- (Two extraction methods disagree by 1–2 tokens on the totals — grep counts 51 exact-`<V>`
  keys of ~81–83 distinct `key=` tokens; the classes, not the arithmetic, are the claim.)

## Honest boundaries (measured, not asserted)

1. **Counter magnitudes inside an existing finding id read `none`.** Demonstrated: the
   `count=$((c_kill+4))` mutant emits `count=5` vs the baseline's `count=1` and `--drift`
   returned `MORI_DRIFT: none` exit 0. Appearance/disappearance of a finding id *is* caught
   (rename mutant). ≈47% of the schema sits in the counter class (lesson).
2. **The baseline records no `MORI_*` env.** A pin and a drift under different envs (e.g.
   `MORI_ROSTER_LANES`) report drift that is an env difference (note §3.2; not re-measured by
   me). The re-run recipe must pin the invocation.
3. **Revision history.** `d7710981…` is a revision of `census-r5` distinguished by SHA;
   `VERSION` unchanged; the diff's deletions are confined to the usage text, the selftest
   runner and `main()`.
4. **Defect (not mine to fix):** `SKILL.md:75` says "Selftest coverage (56 → 65 cases, r10)"
   and its case list omits the volatile-contract arm, while the settled file and every
   artifact show **66**; the SKILL row was evidently written at `1ddb7ff8…`. Report only.
5. **Clock observation:** `corpus/lessons/2026-10-15-volatile-contract-behavioral-baselines.md`
   dates the `72da04b8…` move at ~22:11Z; my poller observed that revision at 21:58:15Z (seat
   clocks in this wave differ). All my figures use my seat's clock; baseline `pinned_ts` values
   are the census's own clock.
6. **Baseline consolidation observed mid-battery:** the receipts-writer's interim pin
   (`baseline-r10-20261015T2210Z.json`, pinned at the pre-settlement `1ddb7ff8…`) was removed
   between 22:24:43Z and 22:28:12Z and superseded by `baseline-r10-20261015T2231Z.json`
   (pinned at the settled `d7710981…`). The **current** reference is the 2231Z file; the
   cross-revision reading against the interim file (mine, 22:20Z, `none` exit 0) remains
   evidence of behavioral stability across the revision, but its file no longer exists.
7. **`[PENDING]` at scribe clock:** the r10 section of `corpus/evidence/README.md` (the
   receipts set's index + re-run recipe) had not landed; `LOG.md`/`SCORECARD.md` are
   parent-owned and untouched. The note's §4 and `SKILL.md` carry the recipe in the interim.

## Drafts built from this ledger

`scorecard-verdict-draft.md`, `log-entry-draft.md`, `report-draft.md` (all under this
directory; updated 2026-10-15T22:35Z for the baseline consolidation). If the census SHA moves
past `d7710981…` after this clock, re-run the battery's first legs (pin → drift → one mutant)
at the final bytes before integrating.