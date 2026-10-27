# Mo56ScoutCensusOverlap — census watchdog surface vs driver-liveness probe

Seat: Mo56ScoutCensusOverlap (mori-shokunin, leaf scout). Freeze tip analyzed:
`8be2717b0809281d07dffe83dad424a4859e0747`. Verified
`git diff 8be2717b acc62f54 -- tools/mori-census.sh tools/mori-driver-liveness.py`
is empty (both tools identical at freeze tip and working tree), so working-tree
reads are freeze-tip reads. Scratch: `/fast/scratch/hyaku/mori-r56/Mo56ScoutCensusOverlap/`
(removed at exit). No fleet files mutated; no votes carried.

## Question

Which reads overlap between the census `probe_watchdog` surface
(`tools/mori-census.sh:703-853`) and `tools/mori-driver-liveness.py`, which are
probe-unique, and is the probe docstring's claim — "the census fires
WATCHDOG_ABSENT every round and reads no launch/complete lines" — true at
8be2717b?

## Evidence (command + output + exit)

1. Process check: `pgrep -af shokunin-watchdog` → no output, `rc=1` (no
   shokunin-watchdog daemon runs under the hyaku inline driver).
2. Live census run (read-only mode, creates no files):
   `bash tools/mori-census.sh > census-live.out` → `exit=1` (DRIFT). Header:
   `mori-census census-r6 — ts=2026-10-27T13:59:24Z — mode=live — read-only`.
   Watchdog surface row:
   `SURFACE watchdog: drift (cmd=pgrep -af shokunin-watchdog; stat /home/vgpnk/Projects/shokunin/.ufo/watchdog.log; ls /home/vgpnk/Projects/shokunin/.ufo/state; pids=0; log=ok; age_s=150; stale_threshold_s=900; state_rounds=21 state_rounds_max=18 state_lag=15 state_ahead=0 state_cmp=21 state_val_unreadable=0 state_val_unread_reasons=file:0 symlink:0 dir:0 other:0; ts=2026-10-27T13:59:24Z)`.
   Finding line 48: `FINDING WATCHDOG_ABSENT severity=warn obs=no shokunin-watchdog process matched by pgrep ts=2026-10-27T13:59:24Z script_sha256=87b8d680b9b2572e89977a10ff9b91630fbaf689f23f4892e06be427b977ab28`.
   `sha256sum tools/mori-census.sh` = `87b8d680…ab28` — the stamped sha matches
   the freeze-tip file, tying the observation to 8be2717b.
3. Fifteen `WATCHDOG_STATE_LAG` findings, one per state entry, each citing a
   `ledger_round` parsed from the log, e.g.
   `lane=mori state_round=2 ledger_round=56` — matching the live log line
   `2026-10-27T10:08:36-03:00 launch mori round=56 pgid=620717 driver=hyaku-inline attempt=1`
   (`grep -m2 'launch mori round=56' /home/vgpnk/Projects/shokunin/.ufo/watchdog.log`).
   `state_cmp=21` = all 21 state entries were compared against launch lines.
4. Live driver probe:
   `python3 tools/mori-driver-liveness.py --fleet-root /home/vgpnk/Projects/shokunin`
   → `exit=0`, verdict `DRIVER_LIVENESS_OK`; log shape: lines=1729,
   malformed=0, other_lines=121, mtime_age_s≈184, 23 lane rows (mori: 66
   launches / 39 completes / 17 deads / in_flight / unclosed 10); state shapes
   `{regular: 21, symlink: 0, dir: 0, other: 0}` — values never read.
5. Code cross-refs (all at 8be2717b):
   - census log path: `mori-census.sh:297` `WATCHDOG_LOG=${MORI_WATCHDOG_LOG:-$UFO/watchdog.log}`,
     `:301` `TIMELINE_FILE=${MORI_TIMELINE_FILE:-$WATCHDOG_LOG}`.
   - census ledger load: `:665-670` `load_ledger` cats `$TIMELINE_FILE` into
     `LEDGER`; called from `probe_watchdog` at `:783`.
   - census launch parse: `:685-706` `ledger_last_launch_round` — filter
     `[ "$f2" = launch ] || continue` (launch lines only; fields 1-4 only;
     last-wins).
   - census pgrep/absent: `:710-726` pid count; `:828-830`
     `if [ "$pid_n" -eq 0 ]; then emit_finding WATCHDOG_ABSENT warn …`.
     pgrep-missing early return `:713-722` emits `WATCHDOG_PROBE_UNAVAILABLE`
     and returns without WATCHDOG_ABSENT.
   - census state walk: `:782` `find $STATE_DIR -maxdepth 1 -name '*.round'`;
     values read `:797-800`; per-entry shape class `:792-807`.
   - probe log read: `mori-driver-liveness.py:213-217` (whole text);
     mtime `:219`; `state_shapes` `:175-198` (classify only);
     launch grammar `:66-96`; complete/dead/fail/wrap grammar `:66-68`;
     pairing output `:181-196`; default paths `:462-469`
     (`<fleet-root>/.ufo/watchdog.log`, `<fleet-root>/.ufo/state`).
   - sibling surface: `probe_silence` (`:2511-2517`) loads the same ledger and
     `ledger_anchor` (`:2056-2099`) parses `complete|wrap` lines.
6. Note on receipts: `evidence/census-start.txt` (exit 0, 316 rows, 23 W04) is
   the output of `scripts/sources-census.sh` (source-registry duplicate-URL
   census over `corpus/SOURCES.md`), not `tools/mori-census.sh`; it carries no
   watchdog surface rows and is not evidence about WATCHDOG_ABSENT either way.

## Overlap map (both readers touch it)

| Read | Census probe_watchdog | Driver probe |
|---|---|---|
| `$FLEET/.ufo/watchdog.log` bytes | `load_ledger` cats whole file into LEDGER (:783,:665-670) | whole-text read (:213-217) |
| log mtime | `epoch_mtime` stat %Y → stale vs 900 s (:737-745) | `os.stat().st_mtime` → mtime_age_s (:219) |
| `$FLEET/.ufo/state/*.round` enumeration | `find` walk (:782) | `os.listdir` filter (:175-198) |
| entry shape class (symlink/dir/other) | classified per entry; findings on unreadable (:792-807) | counted into shapes (:175-198) |
| `launch <lane> round=N` lines | parsed, fields 1-4 only, for state-vs-ledger compare (:685-706) | parsed fully incl. pgid/driver/slot/attempt/mission/pid/runId (:66-96) |

## Probe-unique reads (census never does these)

- `complete` / `wrap` / `lane-dead-no-report` / `launch-fail` line parsing and
  counts (probe `:66-68`, `:97-135`; census watchdog filter admits only
  `launch`).
- Per-event pairing: `open_launches`, `in_flight`, `unclosed`, `rounds_seen`,
  per-attempt keys (:88-135, :181-196).
- `malformed` vs `other_lines` classification with capped examples, `newest_ts`,
  `last_launch_age_s` (:58-64, :136-144, :181-196).
- `DRIVER_LIVENESS_OK|UNAVAILABLE` verdict (:242).

## Census-unique reads (probe never does these)

- Process liveness: `pgrep -af shokunin-watchdog` pid count (:710-726).
- State file **values**: `read_file` + max/lag/ahead ledger comparison
  (`WATCHDOG_STATE_LAG`/`WATCHDOG_STATE_AHEAD`, :797-813). Probe never reads
  values, never follows symlinks (probe notes :248-250).
- Staleness threshold verdict and `WATCHDOG_ABSENT` emission (:737-745,
  :828-830).

## Verdict on the probe's claim

Claim: "the census fires WATCHDOG_ABSENT every round and reads no
launch/complete lines" (probe docstring :7-9; repeated in
`corpus/knowledge/driver-liveness-r56.md` "Why this probe exists").

- "fires WATCHDOG_ABSENT every round": TRUE at 8be2717b for current
  operation. Code emits it iff `pid_n=0` with pgrep available (:828-830); the
  pgrep-missing path returns early with `WATCHDOG_PROBE_UNAVAILABLE` instead
  (:713-722), so "every round" holds only while pgrep is present. Live:
  pgrep rc=1, census exit 1 with `FINDING WATCHDOG_ABSENT severity=warn`,
  stamped sha = freeze-tip file sha. Under the hyaku inline driver no daemon
  runs, so the finding fires on every round's census.
- "reads no launch/complete lines": FALSE for launch lines. The r7 watchdog
  surface has parsed launch lines from the same log since surfaces-r7
  (`mori-census.sh:755-766` comment): `load_ledger` cats the whole log and
  `ledger_last_launch_round` extracts each lane's last
  `launch <lane> round=N` to compare against state values — live evidence:
  `state_cmp=21`, 15 `WATCHDOG_STATE_LAG` findings citing `ledger_round`.
  Complete lines are not parsed by `probe_watchdog` itself (launch-only
  filter), but they are (a) read into `LEDGER` by the same `cat` and (b)
  parsed by the sibling lane-silence surface (`probe_silence` →
  `ledger_anchor`, `complete|wrap` arm :2089-2098). So "nobody reads" the
  launch/complete/dead lines is wrong both at the watchdog surface (launch
  lines) and at fleet-census level (complete/wrap via the silence surface).

The probe's functional behavior is unaffected: it reads the log, classifies
per-lane shape facts, reads no state values, emits no health verdict — live
run exit 0, `DRIVER_LIVENESS_OK`, 0 malformed over 1729 lines. The false part
is the motivating justification sentence in the docstring/knowledge file, i.e.
a stale premise (predating the r7 census change), not an operational defect.

Per round-56 rules the counters/pins are frozen; this is reported as a named
limit and routed item for round 57 (docstring/knowledge wording correction),
with the re-pin consequence of a `tools/mori-driver-liveness.py` edit noted
for the L1 to weigh — not proposed as any counter change.

## Findings

- MED — `tools/mori-driver-liveness.py` docstring :7-9 (and
  `corpus/knowledge/driver-liveness-r56.md` "Why this probe exists"): the
  claim "reads no launch/complete lines" is falsifiable and false at 8be2717b
  for launch lines (census r7 parses them; live `state_cmp=21`, 15
  WATCHDOG_STATE_LAG rows). Route to round 57 as a wording fix; editing the
  tool re-pins its sha256 (pinned `6b3dba74…` at data commit 6ced9da9).
- LOW — `tools/mori-census.sh` :713-722: `WATCHDOG_ABSENT` is unreachable on
  the pgrep-missing path (early return after `WATCHDOG_PROBE_UNAVAILABLE`),
  so "every round" is conditional on pgrep presence. Behavior is disclosed by
  the `WATCHDOG_PROBE_UNAVAILABLE` finding itself; no action needed beyond the
  round-57 wording note.
- LOW — `evidence/census-start.txt` (round-56) is a `scripts/sources-census.sh`
  receipt (SOURCES.md registry census), not a `tools/mori-census.sh` receipt;
  readers must not cite it as evidence about the watchdog surface.
- INFO — overlap confirmed on four reads (log bytes, log mtime, `*.round`
  enumeration, launch lines) plus shape classification; probe-unique surface
  is the complete/dead/fail/wrap parsing and per-event pairing
  (`in_flight`, `unclosed`); census-unique surface is process liveness and
  state-value lag/ahead comparison.
