# mori-shokunin — evidence index

Round-2 watch receipts produced by the **watch-receipts** seat (one seat of the
round-2 coverage wave). Detection and report only — nothing here was remediated,
killed, restarted, or reconfigured; no host or fleet state was written.

## Method (read this first)

`tools/mori-census.sh` has **no watch/interval/repeat mode**: `main()` accepts only
`--selftest`, `--help`, and a silently-consumed `verify` alias (`tools/mori-census.sh:880-895`).
The seat therefore ran **repeated spaced censuses** — three live runs at
`15:27:46Z` / `15:28:55Z` / `15:30:03Z` (start-to-start 0 / 69 / 137 s apart) — and states plainly
that this is a sampling method, not a watch mode. One minute is far below the fleet
driver's `INTERVAL=450` s (`scripts/shokunin-watchdog.sh:10`), so the spacing cannot
show a full driver tick; it only bounds change over the window.

## Receipts (r2)

| File | Captured UTC | Exit | Verdict | Finding-id set vs reverify¹ |
|---|---|---|---|---|
| `watch-r2-20261015T152746Z.log` | 2026-10-15T15:27:46Z | 1 | `MORI_CENSUS: DRIFT (findings=23 drift=20 unavailable=0 surfaces=7)` | identical |
| `watch-r2-20261015T152855Z.log` | 2026-10-15T15:28:55Z | 1 | `MORI_CENSUS: DRIFT (findings=23 drift=20 unavailable=0 surfaces=7)` | identical |
| `watch-r2-20261015T153003Z.log` | 2026-10-15T15:30:03Z | 1 | `MORI_CENSUS: DRIFT (findings=22 drift=19 unavailable=0 surfaces=7)` | differs — receipt lacks `WATCHDOG_ABSENT` |

¹ The **reverify census** ran at `2026-10-15T15:31:21Z`, exit 1, same script
SHA-256 `e3073a2b…`. Its output stayed in seat-local scratch
(`/tmp/mori-watch-r2/reverify.out`) and is not a committed artifact; the comparable
facts (exit code, finding-id set) are recorded in each receipt's
`---- receipt-level verification ----` block.

Each receipt carries: `CAPTURED_UTC`, the exact command, `EXIT_CODE`, `DURATION_S`,
`SCRIPT_SHA256`, the full census stdout verbatim (`---- census stdout+stderr
(verbatim) ----`), the verification block, and a read-only state probe taken once at
`2026-10-15T15:32:30Z` and shared verbatim across all three receipts.

Receipt-file SHA-256 at build time:
`1ea8441f44d1bf3114e0410a65e270beea99e814d27bf4ca69e693f521a08057` (152746Z),
`36ae6522be24b05d2dddbc322e3934c3f8c20231ea5fa8f32619e56d0bfbff1b` (152855Z),
`b44f98c0ddffd58ac5fa0badf7578e86d3b6a704c8413c6f1b29d2a44198aa96` (153003Z).

## Drift comparison across the three spots

- **Stable across all three:** `WATCHDOG_STALE` (log age ~37.8 ks against a 900 s
  threshold), 11 × `WAVE_UNSETTLED_AGE` with the same wave ids, 6 × `LANE_SILENT`
  (kasegi, kake, kumitate, kotoba, kagi, kama), `OOM_KILL_JOURNAL` (user-journal
  text class, count 1), `SEGFAULT_JOURNAL` (718), `UNIT_FAILURE_OUT_OF_SCOPE` (63),
  `CGROUP_OOM_KILL_CUMULATIVE` (parent-slice counter 1, service scope 0), and the
  same surface states (`watchdog/waves/journal/silence` drift; `cgroup/disk/tmux` ok).
- **The one in-window change:** `WATCHDOG_ABSENT` is present in spots 1–2
  (`pids=0`) and **absent in spot 3** (`pids=1`), which is the whole 23→22 finding
  difference. `WATCHDOG_STALE` stayed in all three — a process match does not make
  the log fresh.
- The independent probe (15:32:30Z) could not reproduce any real `shokunin-watchdog`
  process: `pgrep` rc=1, `ps` shows none. **The transient match behind spot-3's
  `pids=1` was not captured and its mechanism is unproven** — recorded as a measured
  anomaly, not explained away. Note the census's own filter
  (`tools/mori-census.sh:188-193`) greps `pgrep -af` output for the search string, so
  a short-lived concurrent process whose command line merely *mentions*
  `shokunin-watchdog` can register as `pids≥1`; that is a hypothesis for the
  anomaly, not proof.
- Fleet HEAD was `11493bf1e2b5f54361d8c7a3873ccd81e374654d` at capture and probe
  time (merged 15:09:03Z, before spot 1) — the drift above is not a fleet-HEAD swap.
- `watchdog.log` did not grow during the window: size 27518 and
  `mtime_epoch=1792040307` (2026-10-15 01:58:27 -0300, last line `tick=2`) are
  identical in every receipt; last driver lines are the mori r1 close and its r2
  relaunch.

## Re-running a receipt

```sh
# 1. Capture (cwd = lane root; identical command as documented in each receipt)
cd /home/vgpnk/Projects/shokunin/mori-shokunin
bash tools/mori-census.sh            # expect exit 1 (DRIFT) on today's fleet; exit 0 CLEAN
                                     # diff the finding-id set, not the byte stream:
diff <(grep -oE '^FINDING [A-Z_]+' corpus/evidence/watch-r2-20261015T152746Z.log | sort -u) \
     <(bash tools/mori-census.sh 2>&1 | grep -oE '^FINDING [A-Z_]+' | sort -u)
# 2. State probe (read-only; same facts the receipts' probe block records)
pgrep -af shokunin-watchdog; ps -eo pid,etimes,cmd | grep -F shokunin-watchdog
stat -c 'size=%s mtime=%Y' /home/vgpnk/Projects/shokunin/.ufo/watchdog.log
tail -1 /home/vgpnk/Projects/shokunin/.ufo/watchdog.log
sha256sum tools/mori-census.sh       # must be e3073a2b… for the receipt to apply
```

**Re-run preconditions (recorded, not invented):** the receipts describe the live
host at their capture times. Finding *counts* are mutable observations: a re-run is
"same receipt" only in formula — exit code, finding-id set, and per-row anchors
(lane ids, wave ids, `age_s` growth ≈ elapsed time) — never in byte equality.
`command not found`, missing `journalctl`/`pgrep`/`tmux`, or a different script
SHA-256 yield `unavailable` rows and do not reproduce these receipts.

## Not claimed here

- No remediation, kill, restart, or host/unit change was performed or is implied.
- No causal claim: the three points sample a ~2-minute window and cannot prove the
  watchdog's liveness story (a daemon could have died before spot 1; note the
  `WATCHDOG_ABSENT` vs `pids=1` flip inside the window).
- No frozen behavioral baseline or drift pin is claimed — see `SCORECARD.md`'s
  freshness note; that artifact is not owned by this seat.
- Journal content remains count-only; `OOM_KILL_JOURNAL count=1` is a user-journal
  text-class count since boot, not a fleet-process kill attribution.

## Other evidence (not produced by this seat)

- `round-1-cgroup-dispatch.json` — round-1 cgroup/dispatch evidence.
- `round-2/live-before.txt` — pre-cutover baseline census (r1 grader,
  `script_sha256=e3073a2b…`, `window_s=900`); `round-2/completed-before.txt`,
  `round-2/dispatch.json` — round-2 attempt records (see `SCORECARD.md` round-2
  section and `LOG.md`).