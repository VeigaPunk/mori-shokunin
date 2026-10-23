measured 2026-10-23T09:16:08Z

# JudgeRowsR15 — wave-2 row judgment, mori round 15

Scope: the single register row keyed `rounds[345].capabilities_added[0]` in the final `## Capabilities`
section of `SCORECARD.md` at lane tip `cedb0ec4f3a4f672804deac388b7191258f01fcd` (row at
`SCORECARD.md:1963` at that revision). I am a wave-2 non-author reviewer; I did not write the row.
Rule applied verbatim from `.ufo/waves/round-35/evidence/c1-controls.txt` (committed `913df22e`):
(a) non-empty, closure-faithful capability and what cells; (b) evidence cell holding only backticked
paths. Then, separately, (c) pointer relevance at closure commit
`b83edc6ee3db6822382ab673d7e6e984e420f22f`.

## Row under judgment (SCORECARD.md:1963 @ cedb0ec4)

`| rounds[345].capabilities_added[0] | partial positive journal alarms | On finite committed fixtures,
keeps individually qualified current-boot OOM and user-signal alarms beside invalid aggregate records,
whose raw totals stay unavailable; no live positive load is claimed. | tools/mori-round15-regressions.py | 15 |`

Closure record used: `MANIFEST.json` `$.rounds[345]` at fleet `37b51a24` (lane `mori`, `round` 15,
`admitted: true`, `verdict: admitted`, `commit` `mori-shokunin@b83edc6ee3db...`);
fleet report `.ufo/reports/round-15/mori.md` at fleet `37b51a24`; verification object
`corpus/lessons/round-15-verifier-spotcheck.md` at `b83edc6ee3db` (non-author `CloseMoriR15`).

## (a) Capability and what cells vs the record — sentence by sentence

MANIFEST `$.rounds[345].capabilities_added[0]` (MANIFEST.json@37b51a24, line 7744):
`partial positive journal alarms: retain qualified current-boot OOM/user-signal alarms while invalid
aggregate totals remain unavailable (finite committed fixtures only)`.

- Capability cell `partial positive journal alarms` — verbatim the name segment of the MANIFEST
  string (line 7744). Non-empty.
- `On finite committed fixtures` — the record's own bound: `(finite committed fixtures only)`
  (line 7744); spotcheck.md:11–12 `finite-fixture scope`.
- `keeps individually qualified current-boot OOM and user-signal alarms` — MANIFEST `retain qualified
  current-boot OOM/user-signal alarms` (line 7744); fleet report:5 `retain the existing critical
  OOM/DRIFT and user-signal WARN/DRIFT alarms from individually qualified current-boot structured
  records`. The added word `individually` is stated by the record at fleet-report:5.
- `beside invalid aggregate records` — report:5 `when an adjacent semantically invalid record
  invalidates the aggregate class`; the closure's own discernment row uses `Individually qualified
  positives beside unavailable aggregates` (spotcheck.md:191).
- `whose raw totals stay unavailable` — MANIFEST `invalid aggregate totals remain unavailable`
  (line 7744); report:5 `Preserve raw totals ... as unavailable, never substitute a subset for a
  total`; spotcheck.md:119 `unavailable raw arm retained, not replaced by a subset total`.
- `no live positive load is claimed` — record bound: spotcheck.md:167–168 `No live positive load ...
  is admitted`; report:75 `not positive-load evidence`; report:83 `fixtures ≠ live load`; report:137
  `no live positive OOM inferred`. The row disclaims exactly what the record disclaims — no overclaim.
- Nothing in the cells exceeds the record: no live-load, universal-coverage, authentication,
  victim-count or performance claim (all excluded at spotcheck.md:167–168).
- First-working round cell `15` equals `$.rounds[345].lane_round`/`round` (15).

## (b) Evidence cell

Cell content is a single backticked path `` `tools/mori-round15-regressions.py` `` and nothing else
(SCORECARD.md:1963 @ cedb0ec4). Rule (b) satisfied.

## (c) Pointer relevance at b83edc6ee3db

Opened `tools/mori-round15-regressions.py` at `b83edc6ee3db6822382ab673d7e6e984e420f22f`; its
SHA-256 is `6a55c33cc13e2cd862ebd44db66e8af635a35d7cd2a85168360569c886d62ffe`, identical to the
closure-measured gate digest recorded in report:32 (`Final gate SHA-256`) and the spotcheck digest
table — the pointer resolves to the exact bytes the closure verified. The file is the isolated
fixture-pack gate for the r15 C1 repair `retain validated positives without fabricated totals`
(docstring, gate:2–8). It demonstrates this capability: required per-scope positive tokens stay exact
integers `even when the named raw aggregate is unavailable` (gate:28–33); green paths emit
`FINDING OOM_KILL_JOURNAL ... user_notice=unavailable:record-invalid ... positive_kernel_oom=1`
(gate:1888–1910) and `FINDING KILL_SIGNAL_JOURNAL ... count=unavailable:record-invalid ...
positive_unit_signal=1` (gate:1912–1931) — a qualified alarm retained beside an invalid aggregate
whose raw totals read `unavailable:record-invalid`. Selectors are current-boot-qualified:
`positive_validation=scalar-id+current-boot(+exact-fields)` enforced at gate:1236–1239 and
1317–1320; `_BOOT_ID` mismatch disqualifies records (gate:424–427). Scope is finite committed
fixtures: digest-checked packs plus committed `expected.json` (`--pin-fixtures`, gate:54–63), and
host journal access is impossible (`MORI_JOURNALCTL_BIN` stub, gate:79–81). It is a distinct file
from the round-14 triage gate (`tools/mori-round14-regressions.py`, row at SCORECARD.md:1962) and
the round-16 window tool (`tools/mori-journal-window.py`, row at SCORECARD.md:1964); this is THIS
round's capability, and the closure names it as the C1 evidence (report:10).

## Verdicts

VERDICT: rounds[345].capabilities_added[0] supported — capability and what cells are non-empty and
closure-faithful (every stated fact cited above, bounded to finite committed fixtures with raw totals
unavailable and no live-positive claim); evidence cell holds only the backticked path
`tools/mori-round15-regressions.py`.

VERDICT: rounds[345].capabilities_added[0] pointer-relevance holds — at `b83edc6ee3db` the cited
artifact is the round-15 gate (sha256 6a55c33c… matches the closure-measured digest) whose claimed
checks and green paths directly exercise qualified-positive alarm retention beside unavailable
aggregate totals on finite committed fixtures; not another round's capability.

## Residual risk / gaps

- Judged the register row against the record, not the production behavior itself: red→green 34→0 was
  verified by the closure (spotcheck.md:95–119), not re-executed here (non-author seats do not rerun
  the gate; PROTOCOL gate standard, spotcheck.md:63–65).
- No defects found in scope. Tool installs/updates: none. No git/jj writes performed; all repo
  access was read-only `git show`. Working copies under
  `/fast/scratch/hyaku/mori-r35/JudgeRowsR15/` (~1.3 MB).
