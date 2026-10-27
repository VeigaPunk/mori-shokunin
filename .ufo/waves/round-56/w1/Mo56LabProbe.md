# Mo56LabProbe — probe-the-probe: 12 injections against the frozen driver-liveness reader

Seat: Mo56LabProbe (leaf, no subagents). Wave w1, lane mori-shokunin.
Scope: empirically probe `tools/mori-driver-liveness.py` (C1 surface) by injecting
unobserved-but-plausible lines, one at a time, into a copy of the REAL fleet log,
and reporting classification vs expectation under the frozen grammar. Crash or
hang = HIGH per seat spec.

I did not judge the claims, widen scope, or propose counter/predicate changes.
Everything below is observed command + output + exit code.

## Artifact identity (the thing I probed is the frozen thing)

```
$ cd /home/vgpnk/Projects/shokunin/mori-shokunin && sha256sum tools/mori-driver-liveness.py
6b3dba74c639190e7e96b6bed8e6ac8f285a51ce6d910fbe92e6dd39bf7be997  tools/mori-driver-liveness.py
$ git show 8be2717b0809281d07dffe83dad424a4859e0747:tools/mori-driver-liveness.py | sha256sum
6b3dba74c639190e7e96b6bed8e6ac8f285a51ce6d910fbe92e6dd39bf7be997  -
```

Matches `PIN` in `.ufo/waves/round-56/count-c1.py:19` and the freeze tip
`8be2717b`. Working tree, data commit `6ced9da9` and freeze tip are byte-identical,
so findings here apply to the pinned artifact.

Counter control (read-only, run for context only):

```
$ python3 .ufo/waves/round-56/count-c1.py 8be2717b0809281d07dffe83dad424a4859e0747
C1=met selftest=ok fixtures=ok entry=ok row=ok norem=ok rev=8be2717b0809281d07dffe83dad424a4859e0747
rc=0
```

So C1's frozen predicate passes. The defects below are outside what that
predicate exercises (named limits, routed to round 57), except where noted.

## Method

Scratch `/fast/scratch/hyaku/mori-r56/Mo56LabProbe/` (removed at end; every
result cited below is copied into this report). Base input is a plain copy of
the live log:

```
$ cp /home/vgpnk/Projects/shokunin/.ufo/watchdog.log $S/base.log
$ wc -l $S/base.log        -> 1729
$ ls -l                    -> 163775 bytes
```

Per injection: `cp base.log inj/<name>.log`, append exactly one line, run the
probe with a fixed `--now 1800000000`, diff the report against the base report.
Classification is read off four deltas: `malformed+1` → malformed,
`other_lines+1` → other, a new lane row → parsed.

Base run:

```
$ python3 tools/mori-driver-liveness.py --log $S/base.log --state-dir $S/emptystate --now 1800000000
rc=0
{"examples": [], "lines": 1729, "malformed": 0, "mtime_age_s": 6889929.49,
 "newest_ts": 1793109414.0, "other_lines": 121}
lanes=23  verdict=DRIVER_LIVENESS_OK  rc=0
```

(Note for the L1: `corpus/knowledge/driver-liveness-r56.md:49` cites 1728 lines;
the live log is append-only and gained one `complete kake round=63` line after
that measurement. Reproduced shape is otherwise identical — not a defect.)

## The 12 injections: expectation vs observation

Expectations are derived only from the frozen regexes at
`tools/mori-driver-liveness.py:54-62` plus the docstring grammar at `:12-30`.

| # | injected line (after ts) | expected | observed | rc | lane row |
|---|---|---|---|---|---|
| I01 | `launch x round=1 driver=hyaku-inline slot=2` | malformed | **malformed** | 0 | empty row created |
| I02 | `launch x round=1 pgid=1 driver=hyaku-inline slot=2` | parsed | **parsed** | 0 | launches=1 unclosed=1 |
| I03 | `launch x round=1 pgid=1 driver=hyaku-inline attempt=1 slot=2` | malformed | **malformed** | 0 | empty row |
| I04 | `launch x round=1 pgid=1 driver=hyaku-inline attempt=1 extra=1` | malformed | **malformed** | 0 | empty row |
| I05 | `launch x round=1 pgid=1 driver=hyaku-inline attempt=1 mission=m_abc` | parsed | **parsed** | 0 | launches=1 unclosed=1 |
| I06 | `complete x round=1; hyaku-inline` | malformed | **malformed** | 0 | empty row |
| I07 | `wrap x round=1 landed` | parsed | **parsed** | 0 | wraps=1 |
| I08 | `2035-01-01T00:00:00+00:00 launch x round=1 pgid=1` | parsed | **parsed** | 0 | launches=1, last_launch_age_s=**-251222400.0** |
| I09 | `launch … attempt=1 ` + 5000 `A` | malformed | **malformed** (example truncated to 120) | 0 | empty row |
| I10 | `launch-fail x round=1 :: ` + 5000 `B` | parsed | **parsed** (launch_fails=1) | 0 | — |
| I11 | `lane-round-failed x round=1 :: marker/contentless report; NOT advancing` | other | **other** (other_lines+1, no lane row) | 0 | — |
| I12 | `launch x round=1 round=` + 5000 `9` | malformed-or-crash | **CRASH, no JSON** | **1** | — |

11 of 12 match the expectation the frozen grammar implies. Two behaviours worth
naming even where they matched:

* I01/I03/I04/I06/I09 all produced a **lane row with `rounds_seen=1` and every
  counter 0**. `parse_log` calls `lanes.setdefault(lane, …)` and
  `row["rounds"].add(int(round_s))` at `:112-114`, *before* the per-event rest
  regex rejects the line at `:123-126`. A lane that only ever appears on a
  malformed line shows up as a zeroed lane. Shape fact, not a verdict, but it
  inflates `len(lanes)` above the number of lanes with real events.
* I12 crash detail below.

## I12 — uncaught exception kills the entire report (crash)

```
$ cp base.log inj/t.log; printf '2026-10-27T11:00:00-03:00 launch x round=%s\n' "$(python3 -c 'print("9"*5000)')" >> inj/t.log
$ python3 tools/mori-driver-liveness.py --log inj/t.log --state-dir emptystate --now 1800000000
rc=1   (stdout empty)
  File ".../mori-driver-liveness.py", line 479, in <module>
  File ".../mori-driver-liveness.py", line 473, in main
  File ".../mori-driver-liveness.py", line 222, in run
  File ".../mori-driver-liveness.py", line 113, in parse_log
    row["rounds"].add(int(round_s))
ValueError: Exceeds the limit (4300 digits) for integer string conversion: value has 5000 digits;
use sys.set_int_max_str_digits() to increase the limit
```

Threshold measured exactly (both conversion sites, `round=` and `attempt=`):

```
round=4299 digits -> ok | attempt=4299 digits -> ok
round=4300 digits -> ok | attempt=4300 digits -> ok
round=4301 digits -> ValueError | attempt=4301 digits -> ValueError
```

Three reachable sites, all converting an unbounded `(\d+)` capture:
`:113` and `:114` (`int(round_s)`), `:128`/`:129` (`int(m2.group(4))`, launch
attempt), `:140` (`int(m2.group(1))`, complete attempt). `pgid=` and `slot=`
are captured but never converted, so a 100 000-digit `pgid=`/`slot=` is fine —
the crash is specific to `round=` and `attempt=`.

Why this is worse than "one bad line is miscounted": the exception escapes
`parse_log` → `run` → `main` with no handler, so **all 23 lane rows are lost**,
stdout is empty, and the exit code is `1`. The docstring's contract at `:39` is
`rc 0 / 2 (setup)`, and `:29-30` promises an unrecognized event line is
"counted, capped examples, never silent". Here one line is silent *and* fatal.

Writer plausibility, stated honestly: no current writer can emit this. The round
number is validated as digits and normalised by `round_of()` at
`scripts/shokunin-watchdog.sh:133-143`, and `normalized=$((10#$n))` on a
5000-digit value collapses to `-1` → then `1`, so the writer cannot produce a
long digit run. `attempt=` is a claim counter (`scripts/hyaku/inline.sh:36`).
The realistic trigger is therefore a corrupt, torn or foreign line in a shared
append-only file that two writers and any operator `>>` can touch — which is
precisely the input class the "malformed, never silent" clause exists for. I
rate it HIGH per the seat rule (crash), with the trigger noted as
not-writer-produced.

## Supplementary probes (beyond the 12; same method)

No hang was found. All 12 injections and the extras finished in 0.03 s wall
against a 1729-line base, well inside a 60 s timeout; 200 000 event lines took
0.51 s. ReDoS-shaped inputs are linear:

```
repeat driver= x20000        ok  0.000s
20000 open parens (dead)     ok  0.000s
200k-char launch-fail reason  ok  0.000s
200k spaces                  ok  0.000s
```

```
R1  CRLF-terminated event line      rc=0   parsed (text mode universal newlines)
R2  attempt= + 4301 digits          rc=1   ValueError (crash)
R3  complete attempt= + 4301 digits rc=1   ValueError (crash)
R4  mission= + 100000 chars         rc=0   parsed
R5  slot= + 100000 digits           rc=0   parsed
R7  round=+1                        rc=0   malformed (LINE_RE needs \d+)
R8  round=007                       rc=0   parsed as 7
R9  `launch  round=1 pgid=1` (empty lane) rc=0 malformed
P11 NUL byte inside ts token        rc=0   malformed
P12 tab-separated event line        rc=0   malformed (ts token becomes the whole line)
P13 invalid UTF-8 bytes (0xff 0xfe) rc=0   malformed, no crash (surrogateescape + ensure_ascii)
```

`parse_ts` is safe against timestamp extremes: across TZ=UTC,
Pacific/Kiritimati, Etc/GMT+12, America/Anchorage, Asia/Kathmandu, Pacific/Apia,
years 0001 and 9999 raise only `ValueError`/`OverflowError`, both caught at
`:73`. No `OSError` path found, so no crash there.

## Grammar and entry gaps found with the same harness

### `lane-round-failed` is a real, committed log variant outside the frozen grammar

The tool's `LINE_RE` alternation at `:54-55` is
`launch|complete|lane-dead-no-report|launch-fail|wrap`. The live log contains a
sixth lane-lifecycle event:

```
$ grep -c 'lane-round-failed' /home/vgpnk/Projects/shokunin/.ufo/watchdog.log
35
$ grep 'lane-round-failed' …/watchdog.log | cut -d' ' -f1 | cut -c1-10 | sort -u
2026-10-15
```

It is not a fleet-root-only artefact — it is in **committed bytes** inside the
docstring's claimed window:

```
$ git -C /home/vgpnk/Projects/shokunin ls-files .ufo/waves/hyaku/frozen/s3-after-eight-closures-20261021T232215Z/watchdog.log
.ufo/waves/hyaku/frozen/s3-after-eight-closures-20261021T232215Z/watchdog.log   (tracked)
    date range: 2026-09-28T15:44:59-03:00 .. 2026-10-21T17:55:52-03:00
    lane-round-failed count: 35  (all 2026-10-15)
```

Because the ts parses but the event name is not in the alternation, these lines
are routed to `other_lines` at `:101`, i.e. the bucket documented as "driver
prose such as `steer ...` or `watchdog tick ...`". Full composition of that
bucket in the live log:

```
tick=N              70
lane-round-failed   35
steer               15
watchdog             1
total              121   (= the report's other_lines)
```

So 35 of 121 "prose" lines are a per-lane round **failure** — the event the
probe exists to surface — and it appears in no lane row at all. The lane's own
sibling instrument already treats it as a real event:
`tools/mori-census.sh:1999` states "launch-fail and lane-round-failed never
start a mission".

This contradicts two written claims:

* `tools/mori-driver-liveness.py:12` — "every variant observed in the committed
  live log 2026-09-28..2026-10-27".
* `corpus/knowledge/driver-liveness-r56.md:25` — same sentence.

The grammar covers launch/complete/dead/wrap/launch-fail; it does not cover
every observed variant. Writer status for calibration: the emitter was removed
at fleet commit `08646c1c` ("Harden report baseline boundaries", 2026-10-19), so
it is a legacy variant still inside the claimed window rather than a live
emitter.

### `other_lines` has no examples, although the docstring says it does

```
$ python3 -c '… json.load(base.json)["log"]'
log keys: examples, lines, malformed, mtime_age_s, newest_ts, other_lines, path
other_lines: 121   examples: []
```

`examples` is populated only in `_bad()` (`:85-90`), i.e. only for malformed
lines. `:26-27` says an other_line is "counted, capped examples, never a lane
event and never malformed". There are no other-line examples, so an operator
facing `other_lines=121` cannot see that 35 of them are `lane-round-failed`.
This is what hides the previous finding.

### `wrap` does not close an attempt-bearing launch, contrary to the entry

`corpus/knowledge/driver-liveness-r56.md:40` says "a wrap closes the round like
a complete". Measured:

```
launch attempt=1  +  wrap     -> launches=1 completes=0 wraps=1 unclosed=1   <-- NOT paired
launch attempt=1  +  complete -> launches=1 completes=1 wraps=0 unclosed=0   <-- paired
launch bare       +  wrap     -> launches=1 completes=0 wraps=1 unclosed=0   <-- paired
```

Mechanism: `:114` sets `key=(round, None)` each iteration; only the complete
branch rebinds it (`:140`, `key=(round, attempt)`). The wrap branch calls
`close_round()` at `:150` with `key` still `(round, None)`, while
`open_launches` holds `(round, attempt)` from `:128-133`. `close_round` (`:116-120`)
can therefore never match, and its `elif` is the same test when `key` is
`(round, None)`.

Live exposure today is zero — all 22 wraps in the log follow a bare launch:

```
wrap predecessors: Counter({'bare': 22})
```

But the current driver's dominant launch shape is attempt-bearing (695 of 842
launches carry `attempt=`, `inline.sh:149`), and `shokunin-watchdog.sh:398` is
the wrap emitter, so a driver transition that wraps a hyaku-inline lane would
report `unclosed` one too high per wrap. The `variants` fixture cannot catch
this: its two wraps (`variants/watchdog.log`) have **no preceding launch**, and
`t_variants` asserts only `wraps==1`/`in_flight is False`.

Also note `wrap` in the live log is `complete; NOT respawning (fleet-wrap)`
(22 lines) while `:20` documents the shape as `landed[…]`; `WRAP_REST_RE` at
`:62` accepts both, so this is a docstring/observation mismatch, not a
misparse. I07 confirms `landed` parses.

### Minor

* I08: a future timestamp yields `last_launch_age_s = -251222400.0` (negative,
  unclamped) and pulls the report-wide `newest_ts` to 2035. Arithmetically
  honest as a shape fact; there is no note flagging a future-dated line.
* `--now nan` / `--now inf` / `--now 1e400` → rc 0 with `NaN` / `Infinity`
  literals in the JSON (`json.dumps` default `allow_nan=True`), which strict
  RFC 8259 parsers reject for a document declared as one JSON object. Operator
  input, not log input. Note `--now -inf` is rejected by argparse (rc 2,
  "expected one argument") because the leading `-`.
* `attempts` is built at `:112` and `:129` but never emitted; lane rows carry
  `launches/completes/deads/launch_fails/wraps/rounds_seen/last_launch_ts/
  in_flight/unclosed` only. Dead weight.

## UNVERIFIED

* Whether any other tool in the fleet consumes `other_lines` or `unclosed` in a
  way that a 35-line miscount or a +1 wrap error would corrupt — I did not
  audit consumers.
* Whether `lane-round-failed` is still emitted anywhere outside
  `scripts/` (I grepped `scripts/`, `mori-shokunin/tools/` and the fleet tree;
  `08646c1c` removed the emitter I found).
* C2 (`mori-vote-bind.py`) — out of this seat's scope, not examined.
* I did not run any build/lint/gate; per lane rules the parent owns that.

## Scratch and tooling

* Scratch: `/fast/scratch/hyaku/mori-r56/Mo56LabProbe/` (`base.log`, `inj/`,
  `emptystate/`, `inject.py`, `results.json`), removed at end. No /tmp evidence.
* Disk guard checked before work: `/fast/scratch/hyaku` at 28 %, 583 GB free.
* No tool installed, upgraded or removed; no pacman; no writes to
  `~/.local/bin`, the lane repo, the git/jj index, `.ufo/state` or
  `.ufo/watchdog.log`. Only this report file was written in the lane.

## Findings

1. **HIGH — uncaught `ValueError` crashes the whole probe; stdout empty, rc 1.**
   `tools/mori-driver-liveness.py:113` (`int(round_s)`), plus `:128-129` and
   `:140` (`int(m2.group(4))` / `int(m2.group(1))` for `attempt=`), convert
   unbounded `(\d+)` captures. Trigger: ≥4301 digits in `round=` or `attempt=`
   (4300 ok, 4301 raises). Fails the documented `rc 0 / 2` contract at `:39` and
   the "never silent" clause at `:29-30`; one line loses every lane row rather
   than being counted malformed. Not producible by the current writers
   (`scripts/shokunin-watchdog.sh:133-143` normalises and collapses long digit
   runs), so reachable only from a corrupt/torn/foreign shared-log line.

2. **MED — `lane-round-failed` (35 lines, 2026-10-15) is silently bucketed as
   "other" prose, so a per-lane round failure is invisible.**
   `tools/mori-driver-liveness.py:54-55` (`LINE_RE` alternation) and `:101`
   (fallthrough to `other_lines`). Present in committed bytes within the claimed
   window (`git ls-files` tracked
   `.ufo/waves/hyaku/frozen/s3-after-eight-closures-20261021T232215Z/watchdog.log`,
   35 lines, 2026-09-28..2026-10-21), which falsifies the completeness sentence
   at `tools/mori-driver-liveness.py:12` and
   `corpus/knowledge/driver-liveness-r56.md:25`. The sibling instrument already
   recognises the event (`tools/mori-census.sh:1999`).

3. **MED — `wrap` does not close an attempt-bearing launch, contradicting the
   entry, so `unclosed` is overstated by one per such wrap.**
   `tools/mori-driver-liveness.py:114` vs `:140` vs `:150`, with the dead `elif`
   at `:119-120`; entry claim at `corpus/knowledge/driver-liveness-r56.md:40`.
   Measured `unclosed=1` for launch(attempt=1)+wrap, `0` for
   launch(attempt=1)+complete and for launch(bare)+wrap. Latent today (all 22
   live wraps follow bare launches) but the dominant launch shape is
   attempt-bearing (695/842 launches). `fixtures/driver/variants/watchdog.log`
   wraps have no preceding launch, so `t_variants` cannot catch it.

4. **MED — `other_lines` carries no examples despite the docstring promising
   "counted, capped examples".** `tools/mori-driver-liveness.py:26-27` vs
   `_bad()`-only population at `:85-90`; measured `other_lines=121,
   examples=[]`. Without examples the 35 misclassified `lane-round-failed` lines
   are undiagnosable from the report, which is what lets finding 2 persist
   unnoticed.

5. **LOW — malformed event lines still create a zeroed lane row.**
   `tools/mori-driver-liveness.py:112-114` runs `lanes.setdefault()` and
   `rounds_seen` before the rest regex rejects the line (`:123-126`,
   `:145-147`, `:152-154`, `:159-161`). Observed on I01/I03/I04/I06/I09:
   `len(lanes)` counts lanes that have no valid event.

6. **LOW — a future-dated line yields a negative `last_launch_age_s` and pulls
   `newest_ts` into the future, unflagged.** `tools/mori-driver-liveness.py:232`
   (`round(now - last_launch_ts, 3)` with no clamp/sentinel); I08 gave
   `-251222400.0` and `newest_ts=2035…`.

7. **LOW — `--now nan|inf|1e400` emits `NaN`/`Infinity` literals with rc 0, not
   strict JSON.** `tools/mori-driver-liveness.py:474` (`json.dumps` defaults
   keep `allow_nan=True`) while the docstring declares one JSON object
   (`:35-39`). Operator-input only.

8. **LOW — dead field `attempts`.** Built at `tools/mori-driver-liveness.py:112`
   and `:129`, never serialised in the lane rows (`:167-174`).
