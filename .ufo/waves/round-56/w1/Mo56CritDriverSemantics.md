# Mo56CritDriverSemantics — mori round 56 w1: attack on the C1 driver-liveness probe's fact semantics

Seat: Mo56CritDriverSemantics (leaf critic, lane mori-shokunin, wave w1).
Date: 2026-10-27. Scope: `tools/mori-driver-liveness.py` fact semantics only;
frozen counters/predicates/controls are NOT proposed for change — every
weakness found is named here as a limit plus a routed item for round 57.
This wave carries no vote items; no line below starts with a vote keyword.

## Baseline (unchanged by my attack)

- Tool sha256 at working tree: `6b3dba74c639190e7e96b6bed8e6ac8f285a51ce6d910fbe92e6dd39bf7be997` == frozen PIN in `count-c1.py:46`. Command: `sha256sum tools/mori-driver-liveness.py`, exit 0.
- Selftest: `python3 tools/mori-driver-liveness.py --selftest` -> `DRIVER_LIVENESS_SELFTEST pass=13 fail=0 skipped=0`, exit 0.
- Frozen counter at freeze tip: `python3 .ufo/waves/round-56/count-c1.py 8be2717b0809281d07dffe83dad424a4859e0747` -> `C1=met selftest=ok fixtures=ok entry=ok row=ok norem=ok rev=8be2717b0809281d07dffe83dad424a4859e0747`, exit 0. (The contract's literal `R` argument is a placeholder; the counter resolves real revs, `C1_SETUP: unresolvable revision R` exit 2 for the literal.)
- No probe output in any run below contains a health-verdict string (checked `healthy|unhealthy|failed lane` absent; verdicts are `DRIVER_LIVENESS_OK`/`_UNAVAILABLE`). No kill-rule condition is touched.

All attack fixtures are synthetic, under scratch
`/fast/scratch/hyaku/mori-r56/Mo56CritDriverSemantics/`, run via
`python3 tools/mori-driver-liveness.py --fixture <dir> --now 1793200000`
(lane repo tool, read-only). Fixture = `watchdog.log` (+ optional `state/`).
Scratch removed after the report was written; outputs cited inline.

## Scenario 1 — launch r1, launch r2, complete r1

Fixture `fx-a-interleave/watchdog.log`:
```
2026-10-27T09:00:00-03:00 launch mori round=1 pgid=111 driver=hyaku-inline attempt=1
2026-10-27T09:05:00-03:00 launch mori round=2 pgid=222 driver=hyaku-inline attempt=1
2026-10-27T09:50:00-03:00 complete mori round=1; hyaku-inline attempt=1
```
Probe output (trimmed), exit 0:
```
mori: launches=2 completes=1 in_flight=false unclosed=1 rounds_seen=2
log: lines=3 malformed=0 verdict=DRIVER_LIVENESS_OK
```
Facts: the round-2 launch never completed, so round 2 IS in flight; the probe
reports `in_flight=false` because `in_flight` is defined as "last event is a
launch" (`tools/mori-driver-liveness.py:172`). The true in-flight state is
only recoverable from `unclosed=1`, a field a consumer can easily miss.
Misleading as a liveness fact: YES — the field name asserts the property its
definition does not deliver. Severity: MED (the report `notes` disclaim it as
a log-shape fact, and the selftest never exercises a last-event-complete with
open launches; the name still overclaims).

## Scenario 2 — dead r1, launch r1 attempt=2, stale complete r1 attempt=1

Fixture `fx-b-stale-complete/watchdog.log`:
```
2026-10-27T09:00:00-03:00 launch mori round=1 pgid=111 driver=hyaku-inline attempt=1
2026-10-27T09:10:00-03:00 lane-dead-no-report mori round=1; retry same round (hyaku-inline attempt=1: L1 died)
2026-10-27T09:15:00-03:00 launch mori round=1 pgid=222 driver=hyaku-inline attempt=2
2026-10-27T09:45:00-03:00 complete mori round=1; hyaku-inline attempt=1
```
Probe output (trimmed), exit 0:
```
mori: launches=2 completes=1 deads=1 in_flight=false unclosed=1
```
What closes: NOTHING. The dead clears all round-1 opens (`:157`); the
attempt=2 launch opens `(1,2)`; the stale `complete ... attempt=1` keys
`(1,1)`, is not open, and the `(1,None)` fallback (`:119`) does not fire —
so `(1,2)` stays open. Two readings:
- SAFE direction: the stale complete does NOT close the live attempt=2
  launch. No false close. Good.
- Misleading residue: the stale complete still increments `completes`
  (`:141`), so "completes" silently includes completes that paired with
  nothing, and `in_flight=false` is again reported while an open launch
  exists (the (1,2) attempt may still be running; the log's last word is a
  dead attempt's complete). The combination "completes=1, in_flight=false,
  unclosed=1" reads as "finished cleanly, one stray open" when the honest
  log-shape reading is "one complete line paired with nothing".
Severity: MED for the stale-complete-counted-plus-in_flight interaction;
the refusal-to-close itself is correct.

Related real-mode (stronger, observed in the fleet log): duplicate
`(round, attempt)` keys. mori round=38 in the live log has EIGHT launches
with attempts `1,2,3,1,2,3,1,1` and ONE `complete ... attempt=1`: one
complete can close only one of three colliding `(38,1)` opens, leaving two
permanent ghosts (`open_launches` is a list, `:133` appends blindly). Fleet
mechanism census below counts 54 such collisions.

## Scenario 3 — wrap r1, then launch r1

Fixture `fx-c-wrap-launch/watchdog.log`:
```
2026-10-27T09:00:00-03:00 launch mori round=1 pgid=111 driver=hyaku-inline attempt=1
2026-10-27T09:30:00-03:00 wrap mori round=1 landed; NOT respawning (fleet-wrap)
2026-10-27T10:00:00-03:00 launch mori round=1 pgid=333 driver=hyaku-inline attempt=1
```
Probe output (trimmed), exit 0:
```
mori: launches=2 wraps=1 in_flight=true unclosed=2
```
`in_flight=true` is correct (a launch is genuinely the last event). The
defect is `unclosed=2`: the wrap closes only `(round,None)`-keyed opens via
`close_round()` (`:116-120`, called at `:150`), so the attempt-carrying
`(1,1)` launch is NOT closed by the wrap; the relaunched `(1,1)` after the
fleet-wrap collides with the still-open `(1,1)` across the wave boundary
(round numbering restarts per wave, so `(lane,round,attempt)` keys are not
unique across waves). Minimal form `fx-c2-wrap-attempt` (launch attempt=1,
then `wrap ... landed; NOT respawning (fleet-wrap)`, nothing else):
```
mori: launches=1 wraps=1 in_flight=false unclosed=1
```
a parked lane (driver explicitly NOT respawning) permanently reports
`unclosed=1`. Companion asymmetry: `launch-fail` never clears opens
(`:158-163`) — a failed launch of a round leaves any earlier same-round
launch open forever. Real-log occurrence: NOT observed as attempt-launch+wrap
in the 1730-line committed log (0 instances); observed via the bare-launch
era instead — aggregator/kake/kagi carry `(round,None)` opens from the
2026-09-28 fleet-wrap whose rounds were wrapped twice with 2-4 bare launches
open (e.g. kake round=16: 4 bare opens, 2 wraps, 1 launch-fail -> 2
permanent ghosts). Severity: MED as a code-level asymmetry with a real
historical analog; the fleet-wrap era means `unclosed` for wrapped lanes is
inflated by construction.

## Scenario 4 — two lanes; can kake's complete close mori's round?

The grammar gives each line exactly one lane token (`LINE_RE`,
`tools/mori-driver-liveness.py:44-45`), so "kake completes mori's round" is
unwritable; there is no lane pair in any event line. Fixture
`fx-d-cross-lane/watchdog.log` interleaves same-round (56) events for both
lanes and adds a case-variant `Mori` launch:
```
2026-10-27T09:00:00-03:00 launch mori round=56 pgid=111 driver=hyaku-inline attempt=1
2026-10-27T09:01:00-03:00 launch kake round=56 pgid=222 driver=hyaku-inline attempt=1
2026-10-27T09:40:00-03:00 complete kake round=56; hyaku-inline attempt=1
2026-10-27T09:41:00-03:00 complete mori round=56; hyaku-inline attempt=1
2026-10-27T09:42:00-03:00 launch Mori round=57 pgid=444 driver=hyaku-inline attempt=1
```
Probe output (trimmed), exit 0:
```
kake: launches=1 completes=1 in_flight=false unclosed=0
mori: launches=1 completes=1 in_flight=false unclosed=0
Mori: launches=1 in_flight=true unclosed=1
```
Result: cross-lane pairing does NOT happen — kake's complete closed only
kake's open; mori's open survived until mori's own complete. Pairing keying
is per-lane row (`lanes.setdefault(lane, ...)` at `:110`) plus `(round,
attempt)`: SOUND. The one crack: lane identity is case-sensitive, so `Mori`
became a second lane row with its own `in_flight=true`. No committed writer
emits case-variant lane names (grammar variants in the tool docstring are all
lowercase; frozen fixtures too), so this is latent only. Severity: LOW.

## Real fleet log confirmation (read-only)

`python3 tools/mori-driver-liveness.py --fleet-root /home/vgpnk/Projects/shokunin`
exit 0, verdict DRIVER_LIVENESS_OK, 1730 lines, malformed=0, other=121.
Per-lane scan for the misleading shapes:

- `in_flight=false` with `unclosed>0`: 9 lanes — kagi(10), kaidoku(6),
  kake(12), kasegi(6), kengaku(6), kotoba(7), kotodama(4), revenger(4),
  tsukuroi(5). Scenario 1/2's misleading shape is production-real, not
  hypothetical.
- `wraps>0` with `unclosed>0`: 9 lanes (aggregator, kagi, kake, kama,
  kasegi, kengaku, kotoba, kumitate, protocol).
- Mechanism census of all 124 fleet-wide opens (replay classifier over the
  committed log): 54 duplicate-`(round,attempt)` launches (mori r38:
  attempts 1,2,3,1,2,3,1,1 -> two permanent `(38,1)` ghosts), 56 launches
  with zero same-round follow-up lines (mori r20,21,22,37 from 2026-10-21/23
  have launch lines only — no complete, no dead, ever), 13
  dead-then-relaunch-never-completed, 1 plausibly current (mori r56 attempt=1
  — consistent with the in-flight fixture). So ≥123 of 124 emitted `unclosed`
  are historical ghosts, and for mori itself 9 of 10.
- Probe-side no-close events in the same replay: `complete_no_open` and
  `wrap_no_open` exist (e.g. aggregator r10, kake r16) — completes/wraps that
  paired with nothing — matching the scenario-2/3 residue semantics.

This is the strongest counterexample to the probe's usefulness framing: the
one number a consumer will read first (`unclosed`, "launches with no
same-(lane,round,attempt) complete") is ~99% historical residue on the real
log. The docstring (`:34-36`) and notes (`:239`) do disclaim it as a pairing
count, so the frozen predicate is not violated — but as a *liveness* fact the
field is materially misleading at fleet scale.

## Round-57 routed items (limits; no frozen-counter change proposed)

1. `unclosed` semantics: emit a decomposition (current-round opens vs
   ghost-by-mechanism) or rename to `unpaired_launches`; make `wrap` and
   `launch-fail` close same-round opens of any attempt (or document that
   they deliberately do not); consider attempt-collision handling (e.g.
   pair most-recent open, or flag `(round,attempt)` reuse).
2. `in_flight`: derive from non-empty `open_launches`, or rename the field
   to `last_event_is_launch` so the name stops asserting a liveness property.
3. `completes`/`wraps` counters: either pair-only counting or an explicit
   `completes_unpaired` companion so stale/duplicate completes are visible.
4. Lane identity: case-fold lane tokens (or assert lowercase in the grammar)
   to prevent case-split lane rows.
5. Selftest gap: no frozen fixture exercises last-event-non-launch with open
   launches, attempt+wrap closure, launch-fail after an open launch, or
   duplicate-`(round,attempt)` launches — all four modes above pass silently.

## Findings

- HIGH — `unclosed` is dominated by permanent ghosts on the real fleet log
  (124 opens fleet-wide, ≥123 historical; mori 9 of 10), from three
  mechanisms the probe neither closes nor flags: duplicate `(round,attempt)`
  launches, launches with zero follow-up, dead-then-relaunch; consumers
  reading it as in-flight work are misinformed. Concerns
  `tools/mori-driver-liveness.py:112-133,157,172-173`. Fixable defect (routed
  item 1), not a frozen-contract violation.
- MED — `in_flight=false` while launches are open: scenario 1/2 constructed
  plus 9 lanes in the real log. The field name asserts a liveness property
  its definition ("last event is a launch", `:172`) cannot deliver.
  `tools/mori-driver-liveness.py:172`. Routed item 2.
- MED — stale or duplicate completes count into `completes` while pairing
  with nothing (`:141-143`); combined with the `in_flight` definition a lane
  whose last line is a stale complete reads "finished, one stray open".
  Scenario 2 + real `complete_no_open` instances. Routed item 3.
- MED — `wrap` and `launch-fail` never close attempt-keyed same-round opens
  (`:116-120,150,158-163`); across a fleet-wrap with restarted round
  numbering this inflates `unclosed` by construction (scenario 3; real
  bare-launch-era analogs aggregator/kake/kagi rounds 10/16). Routed item 1.
- LOW — lane identity is case-sensitive; `Mori` split into a second row
  (scenario 4). Latent: no committed writer varies case. Routed item 4.
- LOW — frozen selftest (13 cases) covers none of the four misleading modes;
  all pass silently. `.ufo/waves/round-56/fixtures/driver/`. Routed item 5.
- INFO — cross-lane pairing keying verified sound: no grammar line can name
  two lanes, and a sibling lane's complete/dead/wrap never closes this
  lane's opens (scenario 4, both directions tested). No defect.

No files outside this report and scratch were written. Scratch
`/fast/scratch/hyaku/mori-r56/Mo56CritDriverSemantics/` removed after
reporting. Host reads were read-only; no processes steered; no journal
MESSAGE-text counting used. No installs were needed (no tool/version/channel
entries).
