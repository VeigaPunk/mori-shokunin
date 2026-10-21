# drift re-pin r20 — classifying every r10 drift token, re-pinning, and what the new baseline certifies

source: `tools/mori-census.sh` sha256 `87b8d680b9b2572e89977a10ff9b91630fbaf689f23f4892e06be427b977ab28`
(unchanged this round); old baseline `corpus/evidence/baseline-r10-20261015T2231Z.json` (byte-unchanged,
sha256 `0993b235…0478`); register `corpus/evidence/drift-classification-r20.json`; new baseline
`corpus/evidence/baseline-r20-20261021T1051Z.json` (sha256 `e528bc15…8433`, `pinned_ts=2026-10-21T10:53:07Z`).
Sources: S066 (approval flow: examine every difference before updating the master), S067 (a
characterization baseline records actual behavior, not desired behavior). Drafted from
`.ufo/waves/round-20/build/DraftDriftNote.md`; classifications from the twelve `Tok*` seats and four
`Hist*` census-history reviewers under `.ufo/waves/round-20/build/`.
verified-at: 2026-10-21, census sha256 87b8d680…ab28; pin 10:53:07Z; post-pin drift none 10:55:31Z
recheck: `bash tools/mori-census.sh --drift corpus/evidence/baseline-r20-20261021T1051Z.json` and classify every token against `corpus/evidence/drift-classification-r20.json` with `.ufo/waves/round-20/build/RegisterCheck/check-register.py`

## 1. Why the r10 pin stayed red for nine rounds

Rounds 12–19 each re-observed or carried `--drift baseline-r10` exit 1 and declined to re-pin
(SCORECARD rounds 12–19 freshness rows). Round 13 left a register whose entries were free-text
buckets (`[INFERENCE] current watchdog/wave/lane activity…`) without class or evidence. At the
round-20 entering tip the live drift had 50 tokens; 8 were absent from that register
(`.ufo/waves/round-20/evidence/c1-drift-entering.json`), and a strict register checker scores the
round-13 file `unclassified=50 invalid=43` (`build/RegisterCheck.md`). Carrying red is not a
disposition (QUALITY 65).

## 2. Closed classes and the rule used

`census-schema-change` (intended, declared emitter change) · `roster-change` (lane membership) ·
`live-state` (census code unchanged, host/fleet state differs) · `census-regression` (unintended
behavior change; blocks a re-pin). Classify by **cause**, with an evidence pointer per token.

Result over the 50 entering tokens: census-schema-change 26, live-state 19, roster-change 5,
census-regression 0 (wave-2 `falsify/FamRosterLanes.md` moved audio, game-dev-2d and game-dev-3d to
roster-change: their conf rows were removed before the r10 pin). Corrections against round 13: `-FINDING:KILL_SIGNAL_JOURNAL` is the r13
text-to-structured redefinition (schema), not live activity; `+SURFACE:lane.kotodama` and
`+SURFACE:lane.souji` are lanes minted after the r10 pin (roster), not r12 schema.

## 3. Dissent and blind spots (recorded, not resolved by the author)

- `-FINDING:WATCHDOG_STALE` and `-FINDING:WAVE_UNSETTLED_AGE`: VolatileContract (K2 for STALE, K3 for WAVE)
  argues census-regression; C1Critic, the round-12 register and wave-2 AdjudicateWaves argue it for WAVE
  only; wave-2 AdjudicateStale and FamWatchdog keep STALE live-state. The disappearance is false-clean
  (daemon still absent; aggregator waves emptied by sweep e20f4fa, not settled). The L1 classes both live-state:
  the probes are byte-identical since r10 and the finding toggles with state. Measured: STALE was
  absent from the entering drift (log written by the inline driver at 07:18 -03) and **present again**
  in the 10:51Z pre-pin drift (log idle > 900 s), so the rule still fires when its input says so.
  Both carry `blind_spot` in the register; the census design fixes (daemon identity instead of log
  mtime, wave memory for emptied directories) are routed to a future census round (FR5, FR3).
- Comparator limits (r10 code): `drift_scan` compares only the first word of a multi-word value
  (the new `nvme0n1p1` device in `io_avg_since_boot` is invisible; `build/TokIoAvg.md`), concatenates
  duplicate keys (`round`), and pairs findings positionally (`obs`).
- Positive-gated findings hide zero-count classes: a regression in a class with no records on either
  side produces no token (`build/HistR13.md`, F1/F3 at 18d7d55). Zero census-regression tokens is not
  proof of zero census regressions; the selftest and the round-14 restoration carry that load.

## 4. The re-pin (L1, 2026-10-21)

| step | time (UTC) | result |
|---|---|---|
| entering drift vs r10 | receipt written 10:22:34Z (start not recorded) | rc 1, 50 tokens, 8 unclassified (r13 register) → 0 (r20 register) |
| pre-pin drift vs r10 | 10:51:14Z | rc 1, 49 tokens (`-FINDING:WATCHDOG_STALE` gone: STALE firing again); 7 unclassified (r13) → 0 (r20) |
| `--pin baseline-r20-20261021T1051Z.json` | 10:53:07Z | `MORI_PIN: ok`, census sha `87b8d680…`, roll line `MORI_CENSUS: DRIFT (…)` retained |
| post-pin drift vs r20 | 10:55:31Z | `MORI_DRIFT: none` rc 0 |

Receipts: `.ufo/waves/round-20/evidence/c1-drift-r10-prepin.txt`, `c1-drift-r20-postpin.txt`, and the
transcribed job stdout with the timestamps and `MORI_PIN: ok` line, `c1-repin-timeline.txt`. Count only
line 1 of the pre-pin file (line 2 is an `rc=` trailer).
The earlier scratch pin (10:22:12Z) drifted 65 s later with `+path +reason -subject_commits -window
basis round`: mado's round-21 report commit at 10:22:39Z moved its lane row from row-A to row-6
(`build/TokPinFlap.md`). Lane rows follow live launches and report commits, so the stability window
of any live pin is minutes to hours; the next lane event names those field families again, and each
must be classified, not suppressed.

## 5. What the new baseline certifies

Sameness of census behavior since 10:53:07Z on this host, nothing more (lane application of S076: a characterization baseline records actual, not desired, behavior). Standing warnings at
pin time (`WATCHDOG_ABSENT`, ten `WAVE_UNSETTLED_AGE`) are part of the reference; the census roll still
reports them every run. `MORI_DRIFT: none` means "unchanged since pin", never "healthy" (S066's
master is approved, not proven correct). The pin header records no environment and `CENSUS_RC` is not
checked by `--pin` (VolatileContract K10/K11): the L1 ran it with no `MORI_*` variables set.

## Round21 erratum — r20 baseline acceptance rejected

Supersedes sections2–3's cause-only permission and any reading of sections4–5
as an accepted reference. The non-author CloseMori20 closure rejected C1:
`aggregator-r10` and `aggregator-r10-resume` lost required observation markers
without independent per-wave settlement or cleanup disposition. Unchanged
census code explains the cause but does not restore observation completeness.
This removed-wave component is `census-regression` in evidence assurance;
the newly aged w24 remains separate live-state. The r20 register's zero count
is a historical author classification, not the effective acceptance ruling.

The baseline and register bytes remain for reproducibility. The r20 baseline
is **invalid for acceptance**, not deleted or silently replaced. Its historical
post-pin `none` remains an observed comparison only. Use QUALITY69 and the
round21 retained evidence-loss accounting before considering any future pin;
the two old lifecycle dispositions remain unknown and block acceptance.
Same-identity posthoc preservation receipts are not independent settlement.
No round21 census, pin, or drift run is represented here.

Evidence: `lessons/round-21.md#M1`, `.ufo/waves/round-20/falsify/AdjudicateWaves.md:5-29`,
`.ufo/waves/round-21/evidence/historical-provenance.json`.
