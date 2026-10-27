# Mo56ScoutLogGrammar — w1 seat report: watchdog.log line-shape recon vs the frozen C1 grammar

Seat: Mo56ScoutLogGrammar (mori-shokunin, leaf; detection and report only).
Target log: `/home/vgpnk/Projects/shokunin/.ufo/watchdog.log` (1728 newlines; 1729
non-blank lines because the final line is unterminated). First ts
`2026-09-28T15:44:59-03:00`, last ts `2026-10-27T10:56:54-03:00`.
Grammar under test: frozen docstring lines 13-30 of
`/home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-driver-liveness.py`, plus the
tool's actual regexes `LINE_RE`, `LAUNCH_REST_RE`, `COMPLETE_REST_RE`, `DEAD_REST_RE`,
`LAUNCHFAIL_RE`, `WRAP_REST_RE` (the acceptance semantics).
Method: imported the tool module read-only (importlib) and classified every line with
its own `parse_ts`/`LINE_RE`/rest regexes; cross-checked with grep counts; ran the
frozen probe itself read-only (`--fleet-root /home/vgpnk/Projects/shokunin`, rc 0,
verdict `DRIVER_LIVENESS_OK`) — its self-reported shape facts match my classification
exactly (`lines=1729 malformed=0 other_lines=121`; per-lane event totals sum to 1608).
No frozen file was modified; all work in scratch `/fast/scratch/hyaku/mori-r56/Mo56ScoutLogGrammar/` (removed after).

## 1. Census

| class | count | detail |
|---|---|---|
| accepted event lines | 1608 | launch 842, complete 571, lane-dead-no-report 166, wrap 22, launch-fail 7 |
| other_line (ts-first, not an event) | 121 | tick=N 70, lane-round-failed 35, steer 15, `watchdog tick …` 1 |
| malformed | 0 | every line's first token parses as ISO-8601 (`date -Is` output) |

Probe self-view (evidence): `log: {"lines": 1729, "malformed": 0, "other_lines": 121, "newest_ts": 1793109414.0}`; per-lane totals `launches=842 completes=571 deads=166 launch_fails=7 wraps=22`.

## 2. Shapes NOT accepted (all are other_line; zero malformed)

Every one of these parses as a timestamp then fails `LINE_RE`, so the tool counts it as
driver prose and it never reaches any per-lane row.

1. `<ts> tick=<N>` — 70 lines (tick=1×13, 2×5, 3×4, 4×3, 5×3, 6–13×2 each, 14–39×1 each).
   Sample: line 10 `2026-09-28T15:50:56-03:00 tick=1`; last: line 402 `2026-10-15T01:58:27-03:00 tick=2`.
   Writer: the cited `scripts/shokunin-watchdog.sh:452` (`log "tick=$tick"`).
2. `<ts> lane-round-failed <lane> round=<n> :: marker/contentless report; NOT advancing` — 35 lines
   (kake 5, kagi 5, kotoba 5, kengaku 5, kama 5, kasegi 5, aggregator 2, protocol 2, kaidoku 1).
   Sample: line 295 `2026-10-15T01:42:28-03:00 lane-round-failed kake round=16 :: marker/contentless report; NOT advancing`.
   Writer: NOT in either cited script. This vocabulary exists only in the running
   kimi-port driver's source, which fleet evidence already records as committed nowhere
   in the repo (`.ufo/waves/kaika-w1/driver.md`: "The log's message vocabulary
   (`lane-round-failed …`, `launch <lane> round=N pid=<pid>`) exists only in K's source, not F's").
   Live effect: e.g. lane `aggregator` reports `deads=0 launch_fails=0` in the probe
   output while 2 `lane-round-failed aggregator` lines exist in the log.
3. `<ts> steer <lane> -> round <n>` — 7; `<ts> steer <lane> -> round <n> via <id>` — 8 (15 total).
   Samples: line 2 `2026-09-28T15:50:55-03:00 steer kake -> round 1`; line 18
   `2026-09-28T15:52:38-03:00 steer protocol -> round 3 via shokunin-r1-protocol`.
   Writer: old watchdog generation (`git log -S 'steer ' -- scripts/shokunin-watchdog.sh`
   → 930502c7 v2, 655a41da v3); not in current scripts.
4. `<ts> watchdog tick (live-missions-in-last-status≈64)` — 1 (line 1, the log's first line). Old daemon.

No line in the log is malformed under the tool's definition (non-ISO first token, or
event head with unrecognized rest). The malformed path is exercised only by the frozen
`malformed` fixture.

## 3. Accepted shapes vs the cited writer sources

Live counts by regex-variant signature (tool's own capture groups):

| shape | live | producer | in cited sources? |
|---|---|---|---|
| `launch … pgid=N driver=hyaku-inline attempt=A` | 692 | `scripts/hyaku/inline.sh:149` | yes |
| `complete …; hyaku-inline attempt=A` | 473 | `scripts/hyaku/inline.sh:176` | yes |
| `lane-dead-no-report …; retry same round (<free>)` | 159 | `scripts/hyaku/inline.sh:182` | yes |
| `launch … runId=ID` | 93 | ufo-fsd (docstring's own attribution); binary not on PATH now | no |
| `launch … pid=N` | 50 | uncommitted kimi-port driver (see §2 item 2) | no; **also absent from the docstring** |
| `complete …; respawning` | 98 | legacy respawn (old daemon, 2026-09-28/10-15); no current writer | no current |
| `launch … mission=ID` (no pgid) | 3 | old steered launches 2026-09-28 (lines 21,23,25) | no |
| `launch … pgid=N driver=hyaku slot=S attempt=A` | 3 | headless slot driver, added c030d1f0, removed cadb3e3e (lines 403-405, 2026-10-19) | no current |
| `lane-dead-no-report …; retry same round` (bare) | 7 | `scripts/shokunin-watchdog.sh:448` shape | yes (but see note) |
| `launch-fail … :: <reason>` | 7 | `scripts/shokunin-watchdog.sh:241-249` shape | yes (but see note) |
| `launch … ` (bare) | 1 | old daemon (line 3, `launch kagi round=1`) | no |
| `wrap … complete; NOT respawning (fleet-wrap)` | 22 | old driver generation (lines 270-293); **not** the `:398` text | no |

Note on the last rows: `shokunin-watchdog.sh`'s own event shapes (`launch … pgid=N`,
`complete …; advancing`, `wrap … landed…`) have **zero** live occurrences (§4), so the
2026-10-15 batch of `launch-fail`/`lane-dead-no-report`-bare lines may equally have
been written by the uncited port rather than by `shokunin-watchdog.sh` itself. The only
event lines certainly attributable to the two cited scripts are inline.sh's three
shapes (692+473+159 = 1324 of 1608). At least 284 event lines match vocabulary no
current fleet script emits.

## 4. Grammar shapes with ZERO live occurrences (over-breadth / staleness)

Docstring shapes (lines 13-30) accepted by the regexes but never seen in the live log:

1. `launch <lane> round=<n> pgid=<pid>` — 0 (the `shokunin-watchdog.sh:266` shape).
2. `launch <lane> round=<n> pgid=<pid> mission=<id>` — 0 ("steered launch, old driver").
3. `complete <lane> round=<n>; advancing to round=<n+1>` — 0 (the `shokunin-watchdog.sh:405` shape).
4. `wrap <lane> round=<n> landed[; NOT respawning (fleet-wrap)]` — 0 (the `shokunin-watchdog.sh:398` shape; both the bare `landed` and `landed; NOT…` forms).

Regex-only alternatives with zero live occurrences (accepted, undocumented, unobserved):
`launch … pgid=N driver=X` (driver without attempt); any `slot=` combination other than
the 3 live `driver+slot+attempt` lines; `wrap … complete` (bare); `wrap … landed` (bare);
`launch … pid=N` combined with any other field.

Stale parenthetical: docstring line 21 says `respawning` is "(120 in log)"; the exact
shape `complete …; respawning` occurs 98 times. 120 is the count of lines containing
the word "respawning" anywhere (98 complete lines + 22 wrap `NOT respawning` lines).

## 5. Live accepted shapes the docstring omits (under-documentation)

1. `launch <lane> round=<n> pid=<pid>` — 50 live lines (e.g. line 309, 2026-10-15),
   accepted via the undocumented ` pid=(\d+)` alternative of `LAUNCH_REST_RE`.
2. `wrap <lane> round=<n> complete; NOT respawning (fleet-wrap)` — 22 live lines,
   accepted via the undocumented ` complete` alternative of `WRAP_REST_RE`.
3. `launch … driver=<d> slot=<s> attempt=<a>` — 3 live lines; `slot=` appears nowhere
   in the docstring grammar.

The docstring preamble ("two writers, one log; every variant observed in the committed
live log 2026-09-28..2026-10-27") is therefore falsified in both directions: the log's
vocabulary comes from at least five writers (inline.sh; shokunin-watchdog.sh; the
removed headless slot driver; ufo-fsd; the uncommitted kimi-port driver; plus the
2026-09-28 daemon/steer generation for `steer`/`watchdog tick`/bare launch), and the
listed 12 shapes neither cover everything observed (pid=, wrap-complete, slot=) nor
all occur (4 shapes at zero).

## 6. Named limits for round 57 (routed items, no counter/grammar change proposed this round)

- LIM-1: the probe's per-lane rows never surface `lane-round-failed` (35 live lines);
  a driver-detected round-failure signal is demoted to other_line by design of the
  frozen grammar. Coverage consequence for C1's "second liveness source": fail events
  that the driver itself logged are invisible per lane.
- LIM-2: docstring grammar is stale/both-directions-incomplete vs the live log
  (§4, §5); any r57 grammar revision must re-derive from the log, not from the two
  cited scripts.
- LIM-3: 284 of 1608 event lines come from writers with no committed source
  (kimi-port driver) or no current source (slot driver, ufo-fsd, legacy daemons);
  fixture-derived confidence does not cover them.

## Findings

- HIGH — `lane-round-failed <lane> round=<n> :: marker/contentless report; NOT advancing`
  (35 live lines) is classified as other_line and never reaches per-lane rows; the
  docstring's claim that the 12 listed shapes are "every variant observed" is false.
  Concerns: tool docstring lines 13-30 (grammar preamble) and `parse_log`'s other_line
  path (`tools/mori-driver-liveness.py`, LINE_RE event list).
- MED — four documented grammar shapes have zero live occurrences
  (`launch … pgid=N`; `launch … pgid=N mission=ID`; `complete …; advancing to round=`;
  `wrap … landed[; NOT respawning (fleet-wrap)]`), while three observed accepted shapes
  are undocumented (`launch … pid=N` ×50; `wrap … complete; NOT respawning` ×22;
  `slot=` ×3); "two writers, one log" is false (≥5 writers). Tool docstring lines 13-30.
- MED — only 1324/1608 accepted event lines are attributable to the two cited writer
  scripts; 284 lines (runId 93, pid 50, respawning 98, mission 3, slot 3, bare launch 1,
  wrap-complete 22, plus 7 launch-fail and 7 dead-bare of uncertain provenance) come
  from uncited or uncommitted writers. Writers: `scripts/hyaku/inline.sh:149,176,182`;
  `scripts/shokunin-watchdog.sh:266,398,405,448` and :241-249; removed slot driver
  (c030d1f0/cadb3e3e); ufo-fsd; uncommitted kimi-port driver.
- LOW — docstring line 21 parenthetical "(120 in log)" for `respawning` counts the
  word across 98 `complete; respawning` + 22 wrap `NOT respawning` lines; the exact
  shape is 98.
- LOW — zero malformed lines in the live log; the malformed path is exercised only by
  the frozen `malformed` fixture (log-shape fact, not a defect).
- LOW — the log's final line lacks a trailing newline (1728 newlines, 1729 lines);
  the probe reads the log correctly (self-reported `lines=1729`).

Report: .ufo/waves/round-56/w1/Mo56ScoutLogGrammar.md
