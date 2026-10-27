# Mo56RevDriverProbe — falsification review of tools/mori-driver-liveness.py

seat: Mo56RevDriverProbe (leaf reviewer, mori round 56 w1) · lane mori-shokunin · 2026-10-27
scope: code review of the frozen driver-liveness probe. Probed per seat order:
LAUNCH_REST_RE looseness, pairing semantics (complete/wrap/dead/launch-fail
closes), other_lines vs malformed boundary, state_shapes symlink handling,
mtime_age None handling. Method: crafted fixture logs under
/fast/scratch/hyaku/mori-r56/Mo56RevDriverProbe/ (removed on finish),
regex battery on the landed bytes, read-only survey of the live
.ufo/watchdog.log. No vote items in this wave.

Verdict: the tool is sound on its frozen fixtures and on committed live bytes
(live run: lines=1730 malformed=0 other_lines=121 lanes=23, rc 0). Four MED
limits (unhandled lane-round-failed event class; close-path asymmetry that
leaks attempt-keyed launches; malformed lines mutating lane/rounds/newest_ts
before rejection; naive timestamps silently interpreted in host-local time)
and a set of LOWs. None kills the frozen C1 predicate; all are named limits
routed to round 57.

## Baseline

```
sha256sum tools/mori-driver-liveness.py
6b3dba74c639190e7e96b6bed8e6ac8f285a51ce6d910fbe92e6dd39bf7be997   # == counter PIN
python3 tools/mori-driver-liveness.py --selftest
DRIVER_LIVENESS_SELFTEST pass=13 fail=0 skipped=0        # rc 0
python3 tools/mori-driver-liveness.py --fleet-root /home/vgpnk/Projects/shokunin
rc 0; log: lines=1730 malformed=0 other_lines=121 lanes=23; state_dir {regular:21}
```

## 1. Grammar looseness — LAUNCH_REST_RE (tools/mori-driver-liveness.py:50-52)

Direct regex calls on the landed file (python3, importlib):

```
' pgid=x'                          -> MALFORMED
' pgid=1 driver=a attempt=b'       -> MALFORMED
' pgid=1 attempt=1 driver=d'       -> MALFORMED   # token order is fixed
' pgid=1 slot=x'                   -> MALFORMED
' pgid=1 mission=m extra'          -> MALFORMED
' runId=r tail' / ' runId=' / ' mission=m x' / ' pid=-1'  -> MALFORMED
' pgid=1 driver=attempt=1'         -> ACCEPT      # driver=(\S+) swallows the attempt token
' pgid=1 attempt=2'                -> ACCEPT      # attempt= without driver= keys (r,2)
' pgid=1 slot=2'                   -> ACCEPT      # slot arm, not in docstring grammar list
' pgid=1 driver=d slot=2 attempt=3 mission=m' -> ACCEPT
' pid=0' / ' pgid=000000000000000000001' / complete '; hyaku-inline attempt=0' -> ACCEPT
4 MB junk tails ('x '*2e6, 'a'*4e6) -> MALFORMED, whole run 1.1 s user; no backtracking blowup
```

In the fixture run, every ACCEPT line produced a full lane row
(launches=1, unclosed=1, in_flight=true): ` pgid=1 driver=attempt=1` is
counted as a real launch keyed (round,None), so a later `; hyaku-inline
attempt=1` or `; respawning` complete would close it — junk that stays in
the fixed key order is silently absorbed into per-lane facts. Reordered or
trailing-space junk is refused correctly.

Docstring fidelity (:11 "every variant observed in the committed live log
2026-09-28..2026-10-27"): the live log itself contains ` pid=N` (68 lines,
e.g. `:309 launch kake round=16 pid=2647554`) and ` slot=` (3 lines, e.g.
`launch kama round=N pgid=V driver=V slot=V attempt=V`) which the regex
accepts but the grammar list omits, plus the `lane-round-failed` event
(section 4) which nothing parses. The list under-documents the regex.

## 2. Pairing semantics (:108-162)

(a) `complete` cannot close the wrong round's launch — `close_round` only
removes keys of the complete's own `round=`. Verified negative.

(b) Cross-key fallback is real (:119-120 `elif` arm): an attempt-qualified
complete also removes a bare `(round,None)` open:

```
launch b round=3 pgid=9
complete b round=3; hyaku-inline attempt=1     -> unclosed=0 completes=1
```

(c) Close-path asymmetry — only `; hyaku-inline attempt=A` carries an
attempt; `wrap` and `; advancing`/`; respawning` completes key (round,None):

```
launch att  round=1 pgid=1 driver=hyaku-inline attempt=1
wrap   att  round=1 complete; NOT respawning (fleet-wrap)   -> unclosed=1 wraps=1
launch bare round=1 pgid=9
wrap   bare round=1 landed                                  -> unclosed=0 wraps=1
launch adv  round=1 pgid=1 driver=hyaku-inline attempt=1
complete adv round=1; advancing to round=2                  -> unclosed=1 completes=1
```

Same wrap line zeroes `unclosed` for a legacy `pid=` launch but leaks it for
an inline `attempt=` launch. All 22 committed wrap lines predate the inline
driver era, so committed bytes are unaffected — but any future/mixed
generation leaks `unclosed` through both wrap and advancing-close paths.
Note `in_flight=false` while `unclosed=1`: the two fields answer different
questions and must not be conflated by consumers.

(d) `dead` clearing is round-scoped, not attempt-scoped (:157):

```
launch m round=1 pgid=1 driver=hyaku-inline attempt=1
launch m round=1 pgid=2 driver=hyaku-inline attempt=2
lane-dead-no-report m round=1; retry same round (hyaku-inline attempt=1: died)
   -> unclosed=0   (both opens removed though the reason cites attempt=1)
```

Documented in notes :241 ("clears that round's open launches"), and other
rounds are untouched (verified: a round-2 open survives a round-1 dead).
Two side-effects: the unclosed docstring definition (:31-32, "launches with
no same-(lane,round,attempt) complete") nowhere mentions that dead removes
launches that never completed — `launch d … attempt=1` + dead => unclosed=0,
completes=0; and the reason string's own attempt attribution is ignored.

(e) `launch-fail` does not close a same-round open (:158-162):

```
launch lf round=2 pgid=1 driver=hyaku-inline attempt=1
launch-fail lf round=2 :: SUBSTRATE_CMD unset   -> unclosed=1 launch_fails=1
```

Latent only: in committed bytes every launch-fail round has no preceding
open launch (verified against the live log).

(f) `row["attempts"]` (:129) is populated for attempt-keyed launches and
never read or emitted — write-only dead state.

## 3. other_lines vs malformed boundary (:96-101)

```
2026-01-01T00:00:00+00:00                            -> other_lines
2026-01-01T00:00:00+00:00 foo                        -> other_lines
2026-01-01T00:00:00+00:00 launch                     -> other_lines
2026-01-01T00:00:00+00:00 launch zed                 -> other_lines
2026-01-01T00:00:00+00:00 launch zed round=x         -> other_lines   # round= not \d+
2026-10-27T10:00:00-03:00  launch dblsp round=1      -> other_lines   # double space
2026-01-01T00:00:00+00:00 launch zed round=1 junk=   -> malformed
 2026-01-01T00:00:00+00:00 launch leadsp round=1     -> malformed     # bad first token
```

The "event line with an unrecognized rest is malformed" contract only fires
after LINE_RE matches, i.e. only when `round=\d+` is present. A corrupt
event line that loses its round (truncated `launch zed`, `round=x`,
double-spaced ts gap) lands in `other_lines`, lumped with genuine driver
prose (steer/tick=1) — per-lane invisible, indistinguishable from benign
noise.

## 4. Malformed lines mutate reported state before rejection (:108-113 vs :123+)

Lane row creation, `rounds.add`, and `newest_ts` update happen before the
per-event rest validation:

```
2027-01-01T00:00:00+00:00 launch ghost round=99 !!!totally-bogus-rest
  -> malformed=1  AND  lanes.ghost = {launches:0,…, rounds_seen:1}
     AND  log.newest_ts = 1798761600 (the rejected line's future ts)
```

A malformed line creates a phantom lane row, inflates `rounds_seen`, and
advances the log-freshness signal `newest_ts` — a future-dated garbage line
makes a stale log look fresh.

## 5. The committed-log event class the grammar misses

`lane-round-failed <lane> round=N :: <reason>` — 35 committed lines,
e.g. `:295 2026-10-15T01:42:28-03:00 lane-round-failed kake round=16 ::
marker/contentless report; NOT advancing`. LINE_RE's alternation (:48-49)
has no such verb, so these land in `other_lines` (the live run's 121
includes all 35): no per-lane count, no `last_event`, no effect on
in_flight/unclosed. Fixture f5 confirms the line contributes only
other_lines; the lane's failure fact is invisible in its row. Within C1's
claimed surface — "launch/complete/dead/wrap/fail lines … reported as
per-lane log-shape facts" — a real fail-class driver event produces zero
per-lane facts. This also falsifies docstring :11 verbatim (see section 1).

## 6. Timestamp parsing (:70-74)

`fromisoformat(...).timestamp()`: naive strings convert in HOST LOCAL time;
date-only accepted; far-future accepted. Verified:

```
2026-10-27T10:00:00   -> 1793106000.0   (host local, == UTC on this host)
2026-10-27T10:00:00Z  -> 1793095200.0   (correct UTC; 10800 s apart on a -03:00 log)
2026-10-27            -> 1793070000.0   (date-only accepted as local midnight)
9999-12-31T23:59:59+00:00 -> 253402300799.0
```

All committed bytes are `±HH:MM`-aware (verified: every live-log line starts
`\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}-03:00`), so latent — but a naive log
line ages silently wrong by the host tz offset.

## 7. state_shapes (:184-199)

Fixture state/: `reg.round` file, `broken.round` symlink→/nonexistent,
`linkdir.round` symlink→dir.round, `dir.round` dir, `fifo.round` fifo:

```
{"regular":1, "symlink":2, "dir":1, "other":1}
```

Broken symlink counts as `symlink` (os.path.islink is true for dangling
links) — consistent with "symlinks never followed" (the *entry's* shape is
a link whatever the target). But a symlink-to-dir also counts `symlink`,
not `dir`: dangling links and dir links are indistinguishable. `None`
return conflates state_dir-unset / not-a-directory / OSError mid-listing.

## 8. mtime_age (:223-227)

`os.stat` OSError → `mtime_age_s: null` — honest None handling (verified by
read; the open-then-stat-fails race is hard to trigger deterministically).
Negative ages unclamped: `--now 1` → `mtime_age_s: -1793110293.166201` — a
future-mtime/clock-skew condition surfaces as a negative "age" with no flag.
`os.stat` follows a symlinked log while state *.round entries are never
followed — asymmetric but consistent with `open()`.

## Findings

- **MED — `lane-round-failed` event class unhandled**
  (tools/mori-driver-liveness.py:48-49; live log e.g.
  `2026-10-15T01:42:28-03:00 lane-round-failed kake round=16 ::
  marker/contentless report; NOT advancing`, 35 committed lines). Falls into
  `other_lines`; produces no per-lane fact inside the claimed "fail" surface;
  falsifies docstring :11 "every variant observed". Fixture:
  `2026-10-15T01:42:28-03:00 lane-round-failed kake round=16 ::
  marker/contentless report; NOT advancing` → `other_lines=1`,
  `lanes.kake` unaffected. Route r57: add the verb, or split other_lines
  into prose vs unrecognized-event.
- **MED — close-path asymmetry leaks attempt-keyed launches**
  (tools/mori-driver-liveness.py:116-120,135-150). `wrap` and
  `; advancing`/`; respawning` completes key (round,None): they close bare
  launches but leave attempt-keyed opens permanently unclosed. Fixture:
  `launch att round=1 pgid=1 driver=hyaku-inline attempt=1` +
  `wrap att round=1 complete; NOT respawning (fleet-wrap)` → `unclosed=1`,
  while the same wrap closes a bare `pid=` launch (`unclosed=0`). Route
  r57: decide whether round-terminal events should clear all opens of the
  round (like dead) or none.
- **MED — malformed event lines mutate lane/rounds_seen/newest_ts before
  rejection** (tools/mori-driver-liveness.py:108-113 before :123+: rest
  validation). Fixture: `2027-01-01T00:00:00+00:00 launch ghost round=99
  !!!totally-bogus-rest` → `malformed=1` yet `lanes.ghost.rounds_seen=1`
  and `log.newest_ts=1798761600`. Phantom lane rows and freshness skew from
  rejected bytes. Route r57: validate rest before mutating.
- **MED — naive/bare-date timestamps accepted, interpreted in host-local
  time** (tools/mori-driver-liveness.py:70-74). Fixture:
  `2026-10-27T10:00:00 launch nai round=1 pgid=1` → `last_launch_ts`
  computed as local time; ages skew silently by the host tz offset on a
  non-UTC host. Latent (committed bytes are offset-aware). Route r57:
  reject or flag naive timestamps.
- **LOW — corrupt event lines lumped into `other_lines`**
  (tools/mori-driver-liveness.py:99-101). Fixture:
  `2026-01-01T00:00:00+00:00 launch zed round=x` → `other_lines`, not
  malformed; the malformed arm only fires when `round=\d+` matches.
- **LOW — LAUNCH_REST_RE value looseness** (tools/mori-driver-liveness.py:50-52).
  Fixture: `2026-10-27T10:02:00-03:00 launch a3 round=1 pgid=1
  driver=attempt=1` → counted launch keyed (round,None); `pgid=1 attempt=2`
  (no driver) accepted; `pid=0`, `attempt=0`, leading-zero ids accepted.
  Docstring grammar omits the regex's `pid=`/`slot=` arms though the live
  log uses both.
- **LOW — `dead` clears all opens of the round, ignoring the reason's
  attempt attribution and the unclosed definition**
  (tools/mori-driver-liveness.py:157 vs :31-32,:241). Fixture: two opens
  (attempt=1,attempt=2) + `lane-dead-no-report m round=1; retry same round
  (hyaku-inline attempt=1: died)` → `unclosed=0`; and a launch erased by
  dead counts as neither complete nor unclosed.
- **LOW — `launch-fail` never closes a same-round open**
  (tools/mori-driver-liveness.py:158-162). Fixture:
  `launch lf round=2 pgid=1 driver=hyaku-inline attempt=1` +
  `launch-fail lf round=2 :: SUBSTRATE_CMD unset` → `unclosed=1`. Latent
  in committed bytes.
- **LOW — state_shapes ambiguities** (tools/mori-driver-liveness.py:184-199).
  Fixture: `broken.round -> /nonexistent` and `linkdir.round -> dir.round`
  both count `symlink`; fifo counts `other`; `None` conflates
  absent/not-dir/OSError. The broken-symlink-as-symlink call is defensible
  under "never followed"; it is unmarked either way.
- **LOW — mtime_age edges** (tools/mori-driver-liveness.py:223-227).
  OSError → `null` is honest; negative age unclamped (`--now 1` →
  `mtime_age_s=-1793110293.17`); stat follows a symlinked log while
  *.round links are never followed.
- **INFO — verified non-defects.** `complete` cannot close a different
  round's launch (round-keyed); `dead` leaves other rounds' opens alone;
  no ReDoS on 4 MB rests; reordered keys, empty values, `pid=-1`, trailing
  junk all refused; malformed examples capped at 3×120 chars; duplicate
  completes counted (completes can exceed launches — honest fact);
  `row["attempts"]` (:129) is write-only dead state.
