# Mo56ExecDriverFixtures — C1 driver fixtures, re-run and independently re-derived

Seat: `Mo56ExecDriverFixtures` (leaf executor, no subagents). Lane: mori-shokunin.
Fleet root: `/home/vgpnk/Projects/shokunin`. Lane repo: `/home/vgpnk/Projects/shokunin/mori-shokunin`.
Freeze tip under test: `8be2717b0809281d07dffe83dad424a4859e0747` (entering tip
`5b295eeebd87ebd610d8d39bfe2035742f740cfa`).
Scratch: `/fast/scratch/hyaku/mori-r56/Mo56ExecDriverFixtures/` (created, used, removed — see §9).
Tooling: none installed or upgraded this seat (python3 3.14.8, awk, grep, git as shipped).
No pacman transaction was run. No write outside my report and my scratch.

## 1. Method

Four independent layers, in order:

- **L1 (tool as shipped)** — `tools/mori-driver-liveness.py --fixture DIR` on each of the 9 frozen
  fixture dirs, `--now 1800000000` for determinism.
- **L2 (strict hand count, POSIX ERE only)** — `grep -E`/`sed -E` counter that validates the
  timestamp by calendar field ranges (month 01-12, day 01-31, hour ≤23, min/sec ≤59) and the
  five event rest-grammars; no Python, no import of the tool.
- **L3 (strict per-lane awk model)** — independent implementation of the event grammar and the
  open-launch pairing, compared field-by-field against the tool's `lanes` object.
- **L4 (mutation probes)** — the frozen counter's own arms (pin, selftest, fixtures) attacked from
  outside: mutate `EXPECT_FIX`, mutate fixture bytes, mutate the tool's grammar.

Every artifact cited below was produced in this session; commands, output and exit codes are quoted
verbatim from the transcript. Nothing is cited from /tmp.

## 2. The 9 fixture results (layer L1)

Command (once per fixture, `$n` the fixture name):

```
python3 /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-driver-liveness.py \
  --fixture /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-56/fixtures/driver/$n \
  --now 1800000000
```

| fixture | rc | verdict | lines | malformed | other | lanes | frozen `EXPECT_FIX` |
|---|---|---|---|---|---|---|---|
| hyaku-pairing | 0 | DRIVER_LIVENESS_OK | 2 | 0 | 0 | 1 | 0 |
| attempt-rollover | 0 | DRIVER_LIVENESS_OK | 4 | 0 | 0 | 1 | 0 |
| legacy-grammar | 0 | DRIVER_LIVENESS_OK | 2 | 0 | 0 | 1 | 0 |
| in-flight | 0 | DRIVER_LIVENESS_OK | 1 | 0 | 0 | 1 | 0 |
| malformed | 0 | DRIVER_LIVENESS_OK | 7 | **5** | 1 | 1 | **5** |
| fails-and-dead | 0 | DRIVER_LIVENESS_OK | 2 | 0 | 0 | 1 | 0 |
| state-shapes | 0 | DRIVER_LIVENESS_OK | 1 | 0 | 0 | 1 | 0 |
| two-lanes | 0 | DRIVER_LIVENESS_OK | 3 | 0 | 0 | 2 | 0 |
| variants | 0 | DRIVER_LIVENESS_OK | 12 | 0 | 2 | 6 | 0 |

Frozen table in `count-c1.py:40-44`:

```
EXPECT_FIX = {
    "hyaku-pairing": 0, "attempt-rollover": 0, "legacy-grammar": 0,
    "in-flight": 0, "malformed": 5, "fails-and-dead": 0, "state-shapes": 0,
    "two-lanes": 0, "variants": 0,
}
```

**All 9 fixtures: verdict `DRIVER_LIVENESS_OK`, rc 0, malformed count equal to the frozen value.**
No fixture disagrees with its frozen malformed count.

Per-lane facts returned by the tool (shape: launches, completes, deads, launch_fails, wraps,
in_flight, unclosed):

```
hyaku-pairing    {"mori": [1, 1, 0, 0, 0, false, 0]}
attempt-rollover {"mori": [2, 1, 1, 0, 0, false, 0]}
legacy-grammar   {"mori": [1, 1, 0, 0, 0, false, 0]}
in-flight        {"mori": [1, 0, 0, 0, 0, true, 1]}
malformed        {"mori": [1, 0, 0, 0, 0, true, 1]}
fails-and-dead   {"mori": [0, 0, 1, 1, 0, false, 0]}
state-shapes     {"mori": [1, 0, 0, 0, 0, true, 1]}
                 state_dir {"regular": 1, "symlink": 1, "dir": 1, "other": 0}
two-lanes        {"kake": [1, 1, 0, 0, 0, false, 0], "mori": [1, 0, 0, 0, 0, true, 1]}
variants         {"kagi": [1,1,0,0,0,false,0], "kama": [1,1,1,0,0,true,1],
                  "kasegi": [1,0,0,0,0,true,1], "kengaku": [1,1,0,0,0,false,0],
                  "kotoba": [0,0,0,0,1,false,0], "mado": [0,0,0,0,1,false,0]}
```

## 3. Independent re-derivation of the counts (layer L2 and L3)

Fixture bytes as read (`cat -A`, so trailing whitespace and CR are visible):

```
######## hyaku-pairing
2026-10-27T10:00:00-03:00 launch mori round=56 pgid=620717 driver=hyaku-inline attempt=1$
2026-10-27T10:20:00-03:00 complete mori round=56; hyaku-inline attempt=1$
######## attempt-rollover
2026-10-27T09:00:00-03:00 launch mori round=56 pgid=111 driver=hyaku-inline attempt=1$
2026-10-27T09:19:00-03:00 lane-dead-no-report mori round=56; retry same round (hyaku-inline attempt=1: L1 died at start)$
2026-10-27T09:22:00-03:00 launch mori round=56 pgid=222 driver=hyaku-inline attempt=2$
2026-10-27T09:49:00-03:00 complete mori round=56; hyaku-inline attempt=2$
######## legacy-grammar
2026-10-15T01:50:57-03:00 launch mori round=2 pgid=1234$
2026-10-15T02:30:00-03:00 complete mori round=2; advancing to round=3$
######## in-flight
2026-10-27T10:08:36-03:00 launch mori round=56 pgid=620717 driver=hyaku-inline attempt=1$
######## malformed
total garbage line$
2026-10-27T10:00:00-03:00 launch mori round=56 pgid=620717 driver=hyaku-inline attempt=1$
2026-99-99T99:99:99-03:00 complete mori round=56; hyaku-inline attempt=1$
another broken thing$
2026-10-27T11:00:00-03:00 complete mori round=56; advancing nowhere$
tick=1$
2026-10-27T10:30:00-03:00 steer mori -> round 57$
######## fails-and-dead
2026-10-27T08:00:00-03:00 launch-fail mori round=56 :: SUBSTRATE_CMD unset$
2026-10-27T08:05:00-03:00 lane-dead-no-report mori round=56; retry same round$
######## state-shapes
2026-10-27T10:00:00-03:00 launch mori round=56 pgid=620717 driver=hyaku-inline attempt=1$
######## two-lanes
2026-10-27T09:56:00-03:00 launch kake round=63 pgid=336804 driver=hyaku-inline attempt=1$
2026-10-27T09:59:00-03:00 launch mori round=56 pgid=620717 driver=hyaku-inline attempt=1$
2026-10-27T10:04:00-03:00 complete kake round=63; hyaku-inline attempt=1$
######## variants
2026-09-28T15:50:56-03:00 launch kagi round=1$
2026-09-28T15:56:52-03:00 launch kengaku round=4 mission=m_5ddf2cabcef146ccb3eb1328dd1bfc8a$
2026-09-28T15:56:53-03:00 launch kasegi round=4 pgid=999 mission=m_5ddf2cabcef146ccb3eb1328dd1bfc8a$
2026-09-28T16:00:00-03:00 complete kagi round=1; respawning$
2026-09-28T16:05:00-03:00 complete kengaku round=4; respawning$
2026-10-19T23:24:27-03:00 lane-dead-no-report kama round=11; retry same round (hyaku: headless attempt ended by operator directive to run in-session)$
2026-10-19T23:30:00-03:00 complete kama round=11; hyaku-inline attempt=2$
2026-10-20T00:00:00-03:00 wrap kotoba round=9 landed; NOT respawning (fleet-wrap)$
2026-09-28T15:50:55-03:00 steer kake -> round 1$
2026-09-28T15:44:59-03:00 watchdog tick (live-missions-in-last-status~=64)$
2026-10-20T00:05:00-03:00 launch kama round=55 runId=shokunin-r5-kama-r1790622131$
2026-10-20T00:06:00-03:00 wrap mado round=51 complete; NOT respawning (fleet-wrap)$
```

### L2 — strict grep/sed ERE hand count (draft, reproduced verbatim)

```bash
#!/bin/bash
# independent hand-count of malformed lines per fixture, POSIX ERE only (grep/sed), no python
TSPAT='^[0-9]{4}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])T([01][0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9]([+-][0-9]{2}:[0-9]{2}|Z)?'
L='[A-Za-z0-9_-]+'; R='[0-9]+'
for f in "$@"; do
  nonblank=$(grep -c '[^[:space:]]' "$f")
  tsvalid=$(grep -E -c "$TSPAT" "$f")
  bodies=$(mktemp)
  grep -E "$TSPAT" "$f" | sed -E 's/^[^ ]+ //' > "$bodies"
  ev=$(grep -E -c "^(launch|complete|lane-dead-no-report|launch-fail|wrap) " "$bodies")
  m_launch=$(grep -E -c "^launch $L round=$R( pgid=$R( driver=[^ ]+)?( slot=$R)?( attempt=$R)?( mission=[^ ]+)?| pid=$R| mission=[^ ]+| runId=[^ ]+)?\$" "$bodies")
  m_complete=$(grep -E -c "^complete $L round=$R; (hyaku-inline attempt=$R|advancing to round=$R|respawning)\$" "$bodies")
  m_dead=$(grep -E -c "^lane-dead-no-report $L round=$R; retry same round( \(.*\))?\$" "$bodies")
  m_fail=$(grep -E -c "^launch-fail $L round=$R :: .*\$" "$bodies")
  m_wrap=$(grep -E -c "^wrap $L round=$R (landed|complete)(; NOT respawning \(fleet-wrap\))?\$" "$bodies")
  matched=$((m_launch+m_complete+m_dead+m_fail+m_wrap))
  bad_ts=$((nonblank-tsvalid)); bad_rest=$((ev-matched))
  echo "$(basename $(dirname "$f")) nonblank=$nonblank ts_valid=$tsvalid other=$((tsvalid-ev)) event=$ev matched=$matched malformed=$((bad_ts+bad_rest))  [bad_ts=$bad_ts bad_rest=$bad_rest]"
  rm -f "$bodies"
done
```

Output (9 fixtures, exit 0):

```
attempt-rollover nonblank=4 ts_valid=4 other=0 event=4 matched=4 malformed=0  [bad_ts=0 bad_rest=0]
fails-and-dead nonblank=2 ts_valid=2 other=0 event=2 matched=2 malformed=0  [bad_ts=0 bad_rest=0]
hyaku-pairing nonblank=2 ts_valid=2 other=0 event=2 matched=2 malformed=0  [bad_ts=0 bad_rest=0]
in-flight nonblank=1 ts_valid=1 other=0 event=1 matched=1 malformed=0  [bad_ts=0 bad_rest=0]
legacy-grammar nonblank=2 ts_valid=2 other=0 event=2 matched=2 malformed=0  [bad_ts=0 bad_rest=0]
malformed nonblank=7 ts_valid=3 other=1 event=2 matched=1 malformed=5  [bad_ts=4 bad_rest=1]
state-shapes nonblank=1 ts_valid=1 other=0 event=1 matched=1 malformed=0  [bad_ts=0 bad_rest=0]
two-lanes nonblank=3 ts_valid=3 other=0 event=3 matched=3 malformed=0  [bad_ts=0 bad_rest=0]
variants nonblank=12 ts_valid=12 other=2 event=10 matched=10 malformed=0  [bad_ts=0 bad_rest=0]
```

The `malformed` fixture decomposes exactly as `bad_ts=4` + `bad_rest=1`:

| # | line | class | why |
|---|---|---|---|
| 1 | `total garbage line` | bad_ts | first token not a timestamp |
| 2 | `… launch mori round=56 pgid=620717 driver=hyaku-inline attempt=1` | valid | launch rest matches |
| 3 | `2026-99-99T99:99:99-03:00 complete …` | bad_ts | month 99 is not a calendar value |
| 4 | `another broken thing` | bad_ts | first token not a timestamp |
| 5 | `2026-10-27T11:00:00-03:00 complete mori round=56; advancing nowhere` | bad_rest | `; advancing nowhere` is not one of the three complete rests |
| 6 | `tick=1` | bad_ts | first token not a timestamp |
| 7 | `2026-10-27T10:30:00-03:00 steer mori -> round 57` | other_line | ts-first, not an event verb |

5 malformed + 1 other + 1 event = 7 non-blank lines, matching the tool's
`lines=7 malformed=5 other_lines=1`.

**Note on the timestamp validation.** A first hand-count of mine that validated the timestamp by
*shape* (`^[0-9]{4}-[0-9]{2}-[0-9]{2}T…`) reported `malformed=4` for this fixture, because
`2026-99-99T99:99:99-03:00` passes a shape test and was then accepted as a `complete`. The tool
validates calendar fields (`datetime.fromisoformat`, `tools/mori-driver-liveness.py:70-75`) and
therefore counts it malformed. The frozen value 5 is the calendar-correct one; my shape-only pass
was the defective counter, not the fixture. The strict L2 script above reproduces 5.

### L3 — per-lane awk model vs tool (all 9 fixtures)

```
OK   hyaku-pairing
OK   attempt-rollover
OK   legacy-grammar
OK   in-flight
OK   malformed
OK   fails-and-dead
OK   state-shapes
OK   two-lanes
OK   variants
```

The L3 model compares `launches/completes/deads/launch_fails/wraps` per lane, the lane set, plus
`log.malformed` and `log.other_lines`. All 9 match exactly. Model draft (the strict variant; note
`round=<n>` may carry a trailing `;` on complete/dead lines):

```awk
function ists(t,   y,mo,d,h,mi,s) {
  if (t !~ /^[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]T[0-9][0-9]:[0-9][0-9]:[0-9][0-9]/) return 0
  y=substr(t,1,4); mo=substr(t,6,2)+0; d=substr(t,9,2)+0; h=substr(t,12,2)+0; mi=substr(t,15,2)+0; s=substr(t,18,2)+0
  if (mo<1||mo>12||d<1||d>31||h>23||mi>59||s>59) return 0
  return 1
}
{
  if ($0 ~ /^[ \t]*$/) next
  n++
  if (!ists($1)) { mal++; next }
  ev=$2; lane=$3
  if (ev!="launch"&&ev!="complete"&&ev!="lane-dead-no-report"&&ev!="launch-fail"&&ev!="wrap") { other++; next }
  rnd=$4; sub(/^round=/,"",rnd); sub(/;.*$/,"",rnd); if (rnd !~ /^[0-9]+$/) { mal++; next }
  if (lane !~ /^[A-Za-z0-9_-]+$/) { mal++; next }
  rest=$0; sub(/^[^ ]+ +[^ ]+ +[^ ]+ +round=[0-9]+/, "", rest)
  ok=0
  if (ev=="launch") {
    if (rest=="" || rest ~ /^ pgid=[0-9]+( driver=[^ ]+)?( slot=[0-9]+)?( attempt=[0-9]+)?( mission=[^ ]+)?$/) ok=1
    else if (rest ~ /^ pid=[0-9]+$/) ok=1
    else if (rest ~ /^ mission=[^ ]+$/) ok=1
    else if (rest ~ /^ runId=[^ ]+$/) ok=1
  } else if (ev=="complete") { if (rest ~ /^; (hyaku-inline attempt=[0-9]+|advancing to round=[0-9]+|respawning)$/) ok=1 }
  else if (ev=="lane-dead-no-report") { if (rest ~ /^; retry same round( \(.*\))?$/) ok=1 }
  else if (ev=="launch-fail") { if (rest ~ /^ :: .*$/) ok=1 }
  else if (ev=="wrap") { if (rest ~ /^ (landed|complete)(; NOT respawning \(fleet-wrap\))?$/) ok=1 }
  if (!ok) { mal++; next }
  c[lane,ev]++
}
END {
  for (k in c) { split(k,a,SUBSEP); printf "%s %s %d\n", a[1], a[2], c[k] }
  printf "TOTAL nonblank=%d malformed=%d other=%d\n", n, mal, other
}
```

## 4. State-dir shapes (the `state-shapes` fixture)

```
$ ls -la .../fixtures/driver/state-shapes/state/
lrwxrwxrwx kake.round -> mori.round
-rw-r--r-- mori.round          # content is "56\n"
drwxr-xr-x tabi.round          # contains one file "inner"
```
Tool: `state_dir {"regular": 1, "symlink": 1, "dir": 1, "other": 0}`, and the value `56` never
appears in the report.

Independently probed that values are never read and symlinks never followed: a `*.round` FIFO and a
`*.round` symlink to that FIFO were placed in a scratch fixture —

```
state_dir: {'dir': 0, 'other': 1, 'regular': 1, 'symlink': 1}
contains 56 value? False
exit=0 (no hang => never opened the fifo)
```

`other: 1` is the FIFO; `symlink: 1` is the symlink (counted, not followed — a follow would have
blocked on the FIFO). A `tabi.round` directory is counted as `dir` and not descended.

## 5. Counter, controls, pins

```
$ python3 .ufo/waves/round-56/count-c1.py 8be2717b0809281d07dffe83dad424a4859e0747
C1=met selftest=ok fixtures=ok entry=ok row=ok norem=ok rev=8be2717b0809281d07dffe83dad424a4859e0747
exit=0

$ python3 .ufo/waves/round-56/count-c1.py 5b295eeebd87ebd610d8d39bfe2035742f740cfa
C1=unmet selftest=bad fixtures=bad entry=bad row=bad norem=bad failed=tool_absent rev=5b295eeebd87ebd610d8d39bfe2035742f740cfa
exit=1                       # matches evidence/controls.txt line 1 (do-nothing-c1 PASS)

$ python3 .ufo/waves/round-56/count-c1.py --selftest
C1_COUNTER_SELFTEST pass=1 fail=0
exit=0

$ python3 tools/mori-driver-liveness.py --selftest
DRIVER_LIVENESS_SELFTEST pass=13 fail=0 skipped=0
exit=0
```

Pins and bytes:

```
sha256(tools/mori-driver-liveness.py @8be2717b) = 6b3dba74c639190e7e96b6bed8e6ac8f285a51ce6d910fbe92e6dd39bf7be997
sha256(tools/mori-driver-liveness.py @6ced9da9) = 6b3dba74… (same)
sha256(worktree tools/mori-driver-liveness.py)  = 6b3dba74… (same)
count-c1.py PIN                                 = 6b3dba74… (same)
```

Historical pins, for context (both reproduce): `count-c1.py 3f494b49` → `C1=met …` (this is the
`rev` recorded in `evidence/c1-at-freeze.txt`); `count-c1.py 6ced9da9` → `C1=met …`;
`count-c1.py c419fe6d` → `C1=unmet … failed=pins,norem` (the pre-docstring-correction data commit —
the pin and the no-health-word arm both fire, which is the intended pre-correction state).

Fixture tree identity vs the freeze tip:

```
$ git diff --stat 8be2717b -- .ufo/waves/round-56/fixtures/driver/ tools/mori-driver-liveness.py
(empty)
$ git diff --raw 8be2717b -- .../state-shapes/state/kake.round
(empty)
$ git ls-tree -r 8be2717b .ufo/waves/round-56/fixtures/driver/
100644 attempt-rollover/watchdog.log
100644 fails-and-dead/watchdog.log
100644 hyaku-pairing/watchdog.log
100644 e9c272f… in-flight/watchdog.log
100644 legacy-grammar/watchdog.log
100644 malformed/watchdog.log
120000 state-shapes/state/kake.round        <- symlink, blob = "mori.round"
100644 state-shapes/state/mori.round
100644 state-shapes/state/tabi.round/inner
100644 state-shapes/watchdog.log
100644 two-lanes/watchdog.log
100644 variants/watchdog.log
```

Measurement trap, recorded so it is not re-chased: `git hash-object <path>` **dereferences** a
symlink, so hashing `state-shapes/state/kake.round` yields the blob of `mori.round`'s content
(`f6b91e0e…`) and looks like drift against the tree blob `7ea287d0…`. `git diff` and `ls-tree` show
no drift; `git cat-file -p 7ea287d0…` is the 10 bytes `mori.round`. The fixture tree is
byte-identical to the freeze tip.

## 6. Mutation probes — are the frozen arms load-bearing?

Run in a scratch `git clone --shared` of the lane at the freeze tip (verified
`git rev-parse --show-toplevel` = the scratch clone before every commit; throwaway identity only
inside that clone).

| mutation | counter output | verdict |
|---|---|---|
| `EXPECT_FIX["malformed"] 5 → 4` (counter copy in scratch) | `C1=unmet … fixtures=bad … failed=fixtures`, exit 1 | fixtures arm catches a wrong expectation |
| extra `extra garbage line` appended to the `malformed` fixture (committed in clone) | `C1=unmet … selftest=bad fixtures=bad … failed=pins,selftest,fixtures`, exit 1 | fixture bytes are live inputs |
| drop the `pid=(\d+)` alternative from `LAUNCH_REST_RE` (committed in clone) | `C1=unmet … selftest=ok fixtures=ok … failed=pins`, exit 1 | **only the pin catches it** — selftest and fixtures do not exercise `pid=` |

The third row is a coverage limit, not a counter failure: the pin is doing its job, but the
selftest+fixture arms carry no regression signal for the `pid=` branch (nor for `slot=`). See
finding F2.

## 7. Read-only and determinism

- Fixture tree hashed before/after two runs (`find -type f -exec sha256sum`, plus `readlink` of
  every symlink): identical → the tool wrote nothing.
- Every fixture re-run twice with `--now 1800000000`: byte-identical output (all 9
  `DETERMINISTIC`). Without `--now`, only `last_launch_age_s` / `mtime_age_s` vary; the counter
  never asserts them.
- The tool's only write is the empty-log selftest case's temp file (`tools/mori-driver-liveness.py:354`),
  created under `TMPDIR` and removed by that case.

## 8. Live-log cross-check (outside the fixture mandate, used only to test the grammar)

Snapshot `sha256=594d96e6df8ba9f02415213f2b25eba758e8fe2dc737948b4eb03595f1815622`, 1730 non-blank
lines, copied to scratch before measuring (the live log is being appended to).

```
tool: DRIVER_LIVENESS_OK, lines=1730, malformed=0, other_lines=121, 23 lanes,
      state_dir {regular:21, symlink:0, dir:0, other:0}, total unclosed=124
mine: nonblank=1730 ts_valid=1730 other=121 event=1609 matched=1609 malformed=0
      per-lane unclosed model == tool for all 23 lanes (diff empty)
```

The 121 other lines decompose as: `tick=N` 70, `lane-round-failed …` 35, `steer …` 15,
`watchdog tick …` 1.

The committed live receipt does **not** reproduce numerically today:

```
receipt evidence/driver-liveness-live.txt : lines=1728, kake completes=50, unclosed=13, in_flight=true
re-run now                               : lines=1730, kake completes=51, unclosed=12, in_flight=false
(only lanes differing: kake; cause: a `2026-10-27T10:56:54-03:00 complete kake round=63;
 hyaku-inline attempt=1` line landed at 10:56:54, after the receipt was captured at 10:32:42)
```

mori's figures in the entry (66/39/17, in_flight, unclosed 10) still match. See finding F7.

## 9. Files changed

- Written: `.ufo/waves/round-56/w1/Mo56ExecDriverFixtures.md` (this report). Nothing else.
- Read-only: lane repo, fixture tree, `tools/`, `count-c1.py`, `evidence/`, `corpus/knowledge/`,
  the fleet `.ufo/watchdog.log`, `scripts/`.
- Scratch removed: `/fast/scratch/hyaku/mori-r56/Mo56ExecDriverFixtures/` (clone, fixture copy,
  probe dirs, arrows). One temp dir left by a counter run outside my scratch
  (`/tmp/mori-r56-c1-_k01y670`) was removed; that leak is finding F6.
- Untouched (pre-existing modifications by other seats / L1, not mine): `LOG.md`,
  `SCORECARD.md`, `SHONEN.md`, `corpus/lessons/round-56.md`, `.ufo/waves/round-56/w1/`.
- No tool install or upgrade; no pacman; no git/jj mutation in the fleet repo or lane.

## 10. Risks and blockers

- No blocker. Fixture verdict and all 9 frozen malformed counts reproduce, and two independent
  re-derivations agree.
- Risk carried to the L1: F1 and F2 are grammar/fixture limits that a tool correction (with re-pin)
  would need; the counters are frozen and were not touched.
- UNVERIFIED by this seat: the C2 arm (not my scope), and any judgement about whether the limits
  should change the round's verdict.

## Findings

- **F1 (MED)** — `lane-round-failed <lane> round=<n> :: <reason>` is a driver line shape present
  35 times inside the committed live log window `2026-09-28..2026-10-27` (all 2026-10-15, 9 lanes)
  but absent from the frozen grammar, so it is bucketed as prose (`other_lines`) and never closes
  its round. Consequence on the live snapshot: 9 unique open-launch keys (29 by multiplicity, of
  124) belong to `(lane, round)` pairs that also carry a `lane-round-failed` line — the probe
  reports those as `unclosed` though the legacy watchdog declared the round failed and relaunched.
  The completeness claim is in `tools/mori-driver-liveness.py:12-13` ("every variant observed in
  the committed live log 2026-09-28..2026-10-27") and `corpus/knowledge/driver-liveness-r56.md:24-25`;
  the bucket is `tools/mori-driver-liveness.py:99-102`. Writer was removed in fleet commit
  `08646c1c` (fleet repo `scripts/shokunin-watchdog.sh`), so this is a legacy-era shape; routed to
  round 57 (grammar change ⇒ tool sha ⇒ re-pin), not changed here.
- **F2 (MED)** — the frozen fixture set and the 13-case selftest do not exercise the `pid=` launch
  branch (50 lines in the live snapshot) or the `slot=` branch (3 lines). Measured: dropping
  `pid=(\d+)` from `LAUNCH_REST_RE` (`tools/mori-driver-liveness.py:56-58`) still yields
  `selftest=ok fixtures=ok`; only `failed=pins` fires. A future re-pin would therefore ship without
  a regression signal for those branches. Routed to round 57 (fixtures are frozen).
- **F3 (MED)** — a ts-first line carrying an event keyword but an invalid *lane token* (outside
  `[A-Za-z0-9_-]`) or a non-numeric/missing `round=` token is classified as `other_lines`, not
  `malformed`: `LINE_RE` (`tools/mori-driver-liveness.py:54-55`) requires lane+round to match before
  the rest is examined, and a failed `LINE_RE` goes to the prose bucket at line 99-102. Measured
  probes: `launch mori.sh round=56 pgid=1`, `launch mori round=abc pgid=1`, `launch mori pgid=1` each
  give `malformed=0 other=1 lanes=[]`, while a strict reader gives `malformed=1`. Not silent (the
  line is counted) but the malformed signal the docstring promises at
  `tools/mori-driver-liveness.py:26-29` does not fire for this class. No live occurrence today (all
  23 live lane tokens and all 1609 event lines match `LINE_RE`). Routed to round 57.
- **F4 (LOW)** — pairing asymmetry in `close_round()` (`tools/mori-driver-liveness.py:116-121`):
  an attempt-tagged complete can close an attempt-less launch (fallback at line 119), but an
  attempt-less complete (`; advancing to round=N`, `; respawning`) or a `wrap` never closes an
  attempt-tagged launch. Probes: launch(attempt=1)+complete(no attempt) → `unclosed=1`;
  launch(no attempt)+complete(attempt=1) → `unclosed=0`; launch(attempt=1)+wrap → `unclosed=1`.
  Zero such mixed `(lane,round)` pairs exist in the live snapshot in either direction, so no
  current mis-count; latent if the two writers interleave within a round.
- **F5 (LOW)** — `--selftest` degrades silently when the tool is copied away from a repo-shaped
  tree: `_fixture_dir()`/`_load_fixture()` (`tools/mori-driver-liveness.py:251-265`) return `None`
  and `selftest()` counts skips without failing (`:430-448`). Measured on a copy under
  `<scratch>/orphan/tools/`: `DRIVER_LIVENESS_SELFTEST pass=2 fail=0 skipped=11`, exit 0. The
  counter is safe (it asserts the exact string `pass=13 fail=0 skipped=0`), but a human running a
  copied tool sees a green exit with 11 of 13 cases skipped.
- **F6 (LOW)** — `count-c1.py:124` creates `tempfile.mkdtemp(prefix="mori-r56-c1-")` and never
  removes it (no `rmtree`, no `finally`). Measured: one 64K `mori-r56-c1-qaa_1p8k` left in a
  controlled `TMPDIR`; one `mori-r56-c1-_k01y670` left in `/tmp` when `TMPDIR` was unset (I removed
  that one). Repeated counter runs accumulate under `TMPDIR`.
- **F7 (LOW)** — `corpus/knowledge/driver-liveness-r56.md:52` states "re-running the command
  reproduces it modulo ages". Measured false for anything but ages: the log is append-only, so
  1730 vs 1728 lines, kake completes 50→51, unclosed 13→12, in_flight true→false after one new
  `complete kake round=63` line. The receipt is a correct point-in-time snapshot; the
  reproducibility wording is what overstates it.
- **F8 (LOW)** — dead weight in the tool: `row["attempts"]` is initialised and populated
  (`tools/mori-driver-liveness.py:112`, `:129`) but never read or emitted; `close_round`'s `elif`
  at `:119` repeats the `if` condition whenever `key == (round, None)` (live only for the
  cross-attempt fallback noted in F4).
- **F9 (INFO)** — no fixture, verdict or malformed-count disagreement found: all 9 fixtures return
  `DRIVER_LIVENESS_OK` with the frozen malformed values (0,0,0,0,5,0,0,0,0), and the strict
  grep/sed hand count and the strict awk per-lane model agree with the tool field-by-field. The
  frozen tool sha equals the `count-c1.py` pin at the freeze tip and in the worktree; the fixture
  tree is byte-identical to the freeze tip (a `git hash-object` symlink-dereference artifact
  explains the only apparent difference).
