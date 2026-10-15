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

## Round-3 receipts (r2 census cutover) — produced by the receipts-writer seat

Round-3 goal wave, seat `receipts-writer`. Detection and report only — nothing was
remediated, killed, restarted or reconfigured; no host or fleet state was written.
`tools/mori-silence-cases.sh` is FROZEN this round (sha `505a7504…`; its sha was
recorded around the oracle runs and did not change). `tools/mori-census.sh` moved from r1
`e3073a2b…` to r2 `fe22a14f0bb6d90ffed14506abfcd76153ebf31cf3cb769b97e7eec61cc2f3c9`,
which was stable before, during and after every capture (the `CENSUS_SHA256_BEFORE`
/ `_AFTER` pairs inside each receipt are identical). Every receipt carries its own
`CAPTURED_UTC`, exact command, exit code, duration and the script SHA-256 under test.

| File | Captured UTC | Exit | Verdict / tally |
|---|---|---|---|
| `cutover-r3-20261015T164140Z-before.log` | 16:41:40–16:49:31Z | 0 / 1 / 1 | before-leg at r1: selftest `PASS (14 cases, 14 passed, 0 failed)`; oracle `matched=10 total=27` (17 FAILs, full list in the file); live `DRIFT (findings=21 drift=21 unavailable=1 surfaces=7)`; §4 `:283` repro rc=1 vs control rc=0 |
| `cutover-r3-20261015T165712Z-selftest.log` | 2026-10-15T16:57:12Z | 0 | `MORI_CENSUS_SELFTEST: PASS (25 cases, 25 passed, 0 failed)` at r2 `fe22a14f…` |
| `cutover-r3-20261015T165712Z-oracle.log` | 2026-10-15T16:57:13Z | 1 | `MORI_SILENCE_CASES: matched=25 total=27`; 15 cases moved FAIL→PASS; the 2 remaining FAILs are the frozen matcher defect below, each with passing state/finding/rc halves |
| `cutover-r3-20261015T165712Z-live.log` | 2026-10-15T16:57:14Z | 1 | `census-r2` live: 9× `SURFACE lane.*: progressing` (kasegi `basis=row-A`; aggregator `basis=row-B attribution=inference`), `SURFACE silence: ok (silent=0 progressing=9 progressing_weak=0 young=0 not_open=0 unavailable=0 skipped=0)`, `DRIFT (findings=14 drift=14 unavailable=1 surfaces=7)` where the 1 unavailable is tmux — not DRIFT; reverify exit/finding-set identical |
| `cutover-r3-20261015T165712Z-oracle-counterfactual.log` | 2026-10-15T16:58:24Z | 1 (frozen) / 0 (cf) | scratch copy with a one-block matcher fix, same census bytes: frozen 25/27 exit 1 vs counterfactual **27/27 exit 0**; frozen oracle sha unchanged (was never edited) |

Receipt-file SHA-256 at build time:

- `bb5491394b2153106f2fa4d420952b91f20235e29cbe239ab3f4f0264fd34912` (before)
- `59d3980b1323d8400d28b69a35e2e335149662b915545e5e9dc85d70e8491970` (selftest)
- `335c7b658c26fcb6a611241338ec52621c0ce440d84fcf9a52355e740c684a9d` (oracle)
- `913d129a02bc8524213c0e3819ae20a3330c48271ce133611ef34912f250ab2c` (live)
- `44208f357b7823102fdca34b599b1144ff6bd6f970a98927f3724b3f7322f130` (counterfactual)

**Why the 2 remaining oracle FAILs are a harness defect, not census behavior.**
`tools/mori-silence-cases.sh` asserts with `case "$obs" in $want)`; measured on
this host (bash 5.3.15), a `|` introduced by parameter expansion is a LITERAL
character, not alternation (`w='a|b'; case a in $w)` → no match). Two calls pass
alternation strings — `:455` `'not-open|unavailable'` (case
`ledger-missing-not-silent`) and `:613` `'progressing-weak|silent'` (case
`report-future-no-close`) — so those two cases can never match any state and the
registered end-goal `matched=N total=M, N=M` is unattainable at the frozen sha
(maximum 25/27). The counterfactual receipt carries the semantics probe, the
one-block patch (`[[ "$obs" =~ ^($want)$ ]]`) and both runs at the same census
sha. The frozen file was not edited; the fix belongs to round 4.

Re-run recipes (cwd = lane root; the after receipts apply only at these SHAs):

```sh
cd /home/vgpnk/Projects/shokunin/mori-shokunin
sha256sum tools/mori-census.sh        # must equal fe22a14f… for the after receipts
sha256sum tools/mori-silence-cases.sh # must equal 505a7504… (frozen)
bash tools/mori-census.sh --selftest  # hermetic; expect exit 0, PASS (25 cases …)
bash tools/mori-silence-cases.sh      # frozen oracle; expect matched=25 total=27, exit 1
bash tools/mori-census.sh             # live; expect per-lane rows + deferred verdict
# counterfactual (optional, /tmp only; frozen untouched): recipe inside the receipt
```

**Re-run preconditions (recorded, not invented):** the live receipt describes the
host at its capture time; finding counts are mutable observations — a re-run is
"same receipt" only in formula (exit code, finding-id set, per-lane state
contract), never in byte equality (graded lanes' `age_s` grows; the journal
`kill_signal` count is a boot-scope observation). The hermetic receipts (selftest,
oracle, counterfactual) reproduce only at the pinned census sha; a different sha
invalidates them.

**Not claimed here:** no remediation, kill, restart or host/unit change was
performed or is implied; no causal claim about fleet liveness; the counterfactual
is a scratch experiment, not frozen-oracle behavior; live counts are one clock's
observation; the per-case move (15 FAIL→PASS) is bound to the before/after oracle
receipts plus the counterfactual, not to independent re-derivation.

## Round-4 receipts (round-4 oracle matcher + anti-sniff; census `:227`/close hardening) — produced by the receipts-writer seat

Round-4 goal wave, seat `receipts-writer`. Detection and report only — nothing was
remediated, killed, restarted or reconfigured; no host or fleet state was written.
Two tool revisions are pinned by this set (and only by these SHAs):

- `tools/mori-silence-cases.sh` sha256 `be0e28b8bf3cc34e2a35e6cea7c05bffff376111b42d985b6bec7f0e21f59456`
  (r4 oracle, 28 cases: alternation-safe `want_match` replacing `case "$obs" in $want)`;
  opaque `case.XXXXXXXX` / `shape.XXXXXXXX` fixture trees with no case id in any path
  handed to the census; `MORI_FIXTURE` no longer exported; new `shape-invariance` case).
- `tools/mori-census.sh` sha256 `af2d4e79e69b70bb0b5aecd6acc9608fc7c16b0716766d4a60310e0689d350d7`
  (`VERSION=census-r3`: `:227` state-count walk rc-gated with `state_rounds=unavailable
  state_unreadable=1` disclosure; close lines tracked per anchor round).

Both files had to hold the same SHA for 5 consecutive 20 s checks before capture; every
receipt carries its own `*_SHA256_BEFORE` / `*_SHA256_AFTER` pair and they are identical
within each receipt (capture window 17:35–17:37Z).

| File | Captured UTC | Exit | Verdict / tally |
|---|---|---|---|
| `verdict-r4-20261015T173551Z-selftest.log` | 2026-10-15T17:35:51Z | 0 | `MORI_CENSUS_SELFTEST: PASS (30 cases, 30 passed, 0 failed)` — up from 25: +3 watchdog state-dir cases, +2 close-tracking cases |
| `verdict-r4-20261015T173551Z-oracle.log` | 2026-10-15T17:35:56Z | 0 | `MORI_SILENCE_CASES: matched=28 total=28` — the two r3 FAILs (`ledger-missing-not-silent`, `report-future-no-close`) now PASS; `PASS shape-invariance`; rerun at 17:36:33Z byte-identical |
| `verdict-r4-20261015T173551Z-live.log` | 2026-10-15T17:36:07Z (+ reverify 17:36:32Z) | 1 | live `DRIFT (findings=15 drift=14 unavailable=1 surfaces=7)`; 9/9 lanes `progressing`; `silence: ok`, zero `LANE_SILENT`; the 1 unavailable is tmux, never DRIFT; reverify exit + finding-id set identical |
| `verdict-r4-20261015T173551Z-canary227.log` | 2026-10-15T17:37:26Z | 0 (harness) | `:227` differential on one chmod-000 `.ufo/state` fixture: r3 snapshot rc 1, header only, 0 verdict lines → r4 census full verdict with `state_rounds=unavailable state_unreadable=1`; readable control `state_rounds=1` |
| `verdict-r4-20261015T173551Z-sniffer-v2.log` | 2026-10-15T17:36:54Z | 1 each | m4b verbatim (r3 attack) `matched=1 total=28`; m4c verbatim `1/28`; maximal counter-sniffer v2b `27/28` whose only FAIL is `shape-invariance`; none can fake a pass |

Receipt-file SHA-256 at build time:

- `f890989cf7743fb290b6ac61ae4ff9dfd06119a9d8d8ad282da6d295a2f43903` (selftest)
- `67a9110390318ba38dee56f60fdc3e74ead349f7a01c3d4d631898ab50bdf7ec` (oracle)
- `92808191b4cb873aea017372323202e80e451551067186d83e0802b3dc01ce04` (live)
- `3377c224412103f3bbe32449ce9fc93ae69fe9718abe49ed316aec6f4020daac` (canary227)
- `1aa525253303498079ae185683a04144073a17a90864cf2d8cd520c09537c7cf` (sniffer-v2)

**What moved vs the round-3 record.** Frozen-oracle tally 25/27 exit 1 → 28/28 exit 0
(the matcher defect is fixed; the end-goal `matched=N, N=M` is now attained under the
oracle itself, not only under a scratch counterfactual). Selftest 25 → 30. A no-logic
case-id sniffer that scored `27/27` exit 0 at the r3 oracle (round-3 record) scores
`1/28` exit 1 at the hardened oracle; the strongest no-logic adaptation (invocation-order
replay, source embedded in the receipt) scores `27/28` exit 1, caught by `shape-invariance`
alone. The `:227` crash class is closed at the exact site with a disclosure field instead
of a silent abort. The live census keeps an honest verdict shape (drift driven by
watchdog/waves/journal; unavailable counted, not unhealthy).

Re-run recipes (cwd = lane root; this receipt set applies only at the two SHAs above):

```sh
cd /home/vgpnk/Projects/shokunin/mori-shokunin
sha256sum tools/mori-census.sh        # must equal af2d4e79… for this set
sha256sum tools/mori-silence-cases.sh # must equal be0e28b8…
bash tools/mori-census.sh --selftest  # hermetic; expect exit 0, PASS (30 cases, 30 passed)
bash tools/mori-silence-cases.sh      # expect exit 0, matched=28 total=28
bash tools/mori-census.sh             # live; expect a MORI_CENSUS verdict, per-lane rows
# canary227 and the three sniffers: scripts are embedded verbatim inside their receipts
# (run from /tmp only; the before-side needs a snapshot of the r3 census fe22a14f…)
```

**Re-run preconditions (recorded, not invented):** the live receipt describes the host at
its capture time; finding counts are mutable observations — a re-run is "same receipt"
only in formula (exit code, finding-id set, per-lane state contract), never in byte
equality. The hermetic receipts (selftest, oracle, canary, sniffer) reproduce only at the
two pinned SHAs; a different sha invalidates them. The sniffer tally is a property of the
attacker scripts embedded in the receipt, not of the census.

**Not claimed here:** no remediation, kill, restart or host/unit change was performed or
is implied; no causal claim about fleet liveness; the sniffer receipt is an attack-class
measurement (the named round-4 claim), not an impossibility proof — the census process can
still detect that it runs inside a fixture tree, which `shape-invariance` neutralizes for
grade branching but does not forbid.