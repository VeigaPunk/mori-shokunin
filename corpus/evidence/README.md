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

## Round-5 receipts (run-order close: seeded shuffle + per-run nonce) — produced by the receipts-writer seat

Round-5 goal wave, seat `receipts-writer`. Detection and report only — nothing was
remediated, killed, restarted or reconfigured; no host or fleet state was written. This
receipt set closes the round-4 correction (`SCORECARD.md:229-238`): the run-order spoofing
channel. Two tool revisions are pinned by this set (and only by these SHAs):

- `tools/mori-silence-cases.sh` sha256 `7143ccc2a14221713334c33ade56e24ca711fbd0d3d17f31d33e151be544f017`
  (r5 oracle, 970 lines): run header `SHUFFLE_SEED=` / `RUN_NONCE=` / `CASE_ORDER=`; the 28
  case ids are executed in a seed-shuffled order (Fisher-Yates with a local xorshift32,
  `:944-960`) and every case requires the current run's nonce token in the census output
  (fixture disk-target token `nonce-<N>`, check `:422-427`, `:490-494`). Seed pin
  `MORI_SHUFFLE_SEED=<int>` (same seed ⇒ same order); nonce pin `MORI_RUN_NONCE=<int>`.
  The order seed is deliberately not exported to the census (`:353`).
- `tools/mori-census.sh` sha256 `af2d4e79e69b70bb0b5aecd6acc9608fc7c16b0716766d4a60310e0689d350d7`
  (`VERSION=census-r3`) — **frozen this round**, byte-identical before/after every run.

Every receipt carries its own `*_SHA256_BEFORE` / `*_SHA256_AFTER` pair (identical within
each receipt) and the exact command; the oracle receipts carry SHUFFLE_SEED, RUN_NONCE and
the full CASE_ORDER of their run.

| File | Captured UTC | Exit | Verdict / tally |
|---|---|---|---|
| `order-r5-20261015T180431Z-oracle-1.log` | 2026-10-15T18:04:31Z | 0 | `matched=28 total=28`; seed `1612512038`; order recorded; sorted per-case tuples sha `a70af583…` |
| `order-r5-20261015T180431Z-oracle-2.log` | 18:04:33Z | 0 | `matched=28 total=28`; fresh seed `1323201475`, different order; same sorted tuple sha |
| `order-r5-20261015T180431Z-oracle-3.log` | 18:04:35Z | 0 | seed pinned to oracle-1's (`MORI_SHUFFLE_SEED=1612512038`): `CASE_ORDER` identical to oracle-1, `diff` vs oracle-1 = the RUN_NONCE line only; `matched=28 total=28` |
| `order-r5-20261015T180431Z-selftest.log` | 18:04:37Z | 0 | `MORI_CENSUS_SELFTEST: PASS (30 cases, 30 passed, 0 failed)` at the frozen census sha |
| `order-r5-20261015T180431Z-live.log` | 18:04:38Z (+ reverify 18:05:04Z) | 1 | `MORI_CENSUS: DRIFT (findings=15 drift=14 unavailable=1 surfaces=7)`; finding-id sets of the two spots identical; the 1 unavailable is tmux, never DRIFT |
| `order-r5-20261015T180431Z-sniffer.log` | before 17:59:18Z / after 18:05:21–18:06:18Z | 0 (before) / 1 each (after) | same attackers: r4 snapshot (`be0e28b8…`) `28/28` exit 0 → r5 `0/28` (v3a/v3b/v3c canned, v3e stale-nonce) and `6/28` (v3d live-nonce echo + positional table), all exit 1; channel probe: run seed/CASE_ORDER 0 hits in 29 census env dumps, nonce visible by design |

Receipt-file SHA-256 at build time:

- `3b074829314007a125cbc99b9253180655690a33578778788e7e8116ec97327b` (oracle-1)
- `6a8e66061c86ccd6d2d9a0b5236e60d6e0ecf4cf979305990fe1dc69b619635e` (oracle-2)
- `bb88e332b2feaeaab2f1aea6386e93b90b1472a4d1d5807e1a6d84464acb0620` (oracle-3)
- `de80300d0ad75fa63c62cd632dfaf4b2eebaf16d64800a94ed48d74c7ece55a7` (selftest)
- `8f6b5d9f743d73933f7bfc9a59073fee5378c54c1d0c273d15a46416f77f6541` (live)
- `3c51f5373723252c9349941ab9e9699bbb4808f14037bfbabb85d809a7e27c0f` (sniffer)

**What moved vs the round-4 record.** The three no-logic attackers that reached
`matched=28 total=28` exit 0 at the r4 oracle (re-verified before the landing against a
byte-checked r4 snapshot) score `0/28` exit 1 at the landed revision; the strongest
adaptation measured (fresh-nonce echo + fixed positional table; no case identification)
scores `6/28` exit 1 — the residual 6 are accidental positional coincidences, which the
seeded shuffle closes further; the stale-nonce replay scores `0/28`. The honest census is
unaffected: `28/28` exit 0 at three seeds with byte-identical per-case grade tuples
(`a70af583bb01b8362a49f07aa8f2b66814fac22b119a22f9b273c5024573c752`), and the pinned seed
reproduces the exact run order. Channel probe (embedded in the sniffer receipt): over all
29 census invocations of a probe run, the order seed and CASE_ORDER appear 0 times in the
census env; the nonce token appears (exported as `MORI_RUN_NONCE` and inside
`MORI_DISK_TARGETS`) — by design, and v3d shows that alone is not sufficient.

Re-run recipes (cwd = lane root; this receipt set applies only at the two SHAs above):

```sh
cd /home/vgpnk/Projects/shokunin/mori-shokunin
sha256sum tools/mori-silence-cases.sh  # must equal 7143ccc2… for this whole set
sha256sum tools/mori-census.sh         # must equal af2d4e79…
bash tools/mori-silence-cases.sh       # expect exit 0: header seed/nonce/CASE_ORDER + matched=28 total=28
env MORI_SHUFFLE_SEED=<seed> bash tools/mori-silence-cases.sh   # same seed => same CASE_ORDER
bash tools/mori-census.sh --selftest   # hermetic; expect exit 0, PASS (30 cases, 30 passed)
bash tools/mori-census.sh              # live; expect a MORI_CENSUS verdict + per-lane rows
# attacks (sources embedded verbatim in the sniffer receipt; run from /tmp only):
#   bash tools/mori-silence-cases.sh /tmp/<sniffer>.sh   ; before-side needs an r4
#   oracle snapshot (git show 5b62c897:tools/mori-silence-cases.sh must hash be0e28b8…)
```

**Re-run preconditions (recorded, not invented):** the live receipt describes the host at
its capture time; finding counts are mutable observations — a re-run is "same receipt" only
in formula, never in byte equality. The hermetic receipts reproduce only at the pinned
oracle+census SHAs; a different sha invalidates them. The pinned-seed reproduction depends
on the documented `MORI_SHUFFLE_SEED` interface; an unpinned run necessarily produces a
fresh seed and a different order. The attack tallies are properties of the attacker scripts
embedded in the sniffer receipt, not of the census.

**Not claimed here:** no remediation, kill, restart or host/unit change was performed or is
implied; no causal claim about fleet liveness. The after-side is an attack-class measurement
of the named round-5 claim, not an impossibility proof: a forger keyed on fixture *content*
(memorized content→expectation table) remains out of scope, as do channels outside the
census process env/paths probed here (seed-guessing is bounded by the probe showing no
census-side seed or order channel, not by a cryptographic claim).

## Round-6 receipts (r1 stdout-backchannel close + r2 content-keyed forgery close) — produced by the receipts-writer seat

Round-6 goal wave, seat `receipts-writer`. Detection and report only — nothing was
remediated, killed, restarted or reconfigured; no host or fleet state was written.
This set tests the round-6 claim on two residuals reproduced at the round-5 oracle:
(R1) the run header must print only **after** the case loop, so no living census
invocation can read seed/nonce/order from the oracle's stdout or environ; (R2)
fixture content must carry per-run freshness, so memorized content→row tables are
stale at the next run.

Two revisions are pinned by this set (and only by these SHAs):

- `tools/mori-silence-cases.sh` sha256
  `3307761a04a1eab8f33859a69d2eb63fb6312afb8f8041f7b09da4544be174b9` (r6 oracle,
  uncommitted working-tree edit at capture time; the file held this SHA for 10
  consecutive 30 s checks 19:06:33–19:11:43Z before capture and did not change
  during or after any leg). Mechanism: header printed after the case loop; pins
  removed by a one-time self re-exec (`tools/mori-silence-cases.sh:196-221`);
  per-run nonce + content salt woven into fixture bodies and commit messages.
- `tools/mori-census.sh` sha256 `af2d4e79…` — **FROZEN this round**; identical
  before/after every leg of every receipt (`CENSUS_SHA256_BEFORE/_AFTER` pairs).

The **before-legs** embedded in the two attack receipts are static LEG blocks
captured by this seat in the same dispatch at the r5 oracle `7143ccc2…`; the
after-legs are at the r6 bytes above. Every leg records its own
`ORACLE_SHA256_BEFORE/_AFTER` and raw-output SHA-256; all 26 after-leg pairs are
identical (`3307761a…`). An earlier r6 intermediate revision (`b2ebe5e7…`) was
captured while the impl was still iterating and then superseded by the re-exec
revision above; those superseded receipts were removed from this directory in
favor of the settled-revision set below.

| File | Captured UTC | Exit | Verdict / tally |
|---|---|---|---|
| `backchannel-r6-20261015T191216Z-oracle-1.log` | 19:12:16–19:12:20Z | 0 | `matched=28 total=28`; seed `1387974308`, nonce `1744128128`; header at output lines **29-31**, last case line 28; per-case tuple sha `a70af583bb01b8362a49f07aa8f2b66814fac22b119a22f9b273c5024573c752`; `REGISTRY_BLOCK_IDENTICAL_TO_R5_HEAD` (diff empty); full uncommitted r5→r6 diff embedded (325 lines) |
| `…-oracle-2.log` | 19:12:20Z | 0 | `matched=28 total=28`; fresh seed `2126228259`; different `CASE_ORDER` (28 ids); same tuple sha; `per-case_grade_tuples=BYTE-IDENTICAL_ACROSS_RUNS` |
| `…-oracle-3.log` | 19:12:21–19:12:23Z | 0 | seed pinned to oracle-1's: `CASE_ORDER` **identical** to oracle-1; `oracle-3b` (both pins) output **byte-identical** to oracle-1's |
| `…-selftest.log` | 19:12:25–19:12:28Z | 0 / 2 / 2 | `MORI_CENSUS_SELFTEST: PASS (30 cases, 30 passed, 0 failed)`; setup-contract: missing census → exit 2, `MORI_SHUFFLE_SEED=abc` → exit 2 |
| `…-live.log` | 19:12:28–19:12:50Z (+ reverify) | 1 | two spots `MORI_CENSUS: DRIFT (findings=15 drift=14 unavailable=1 surfaces=7)`; finding-id sets identical; the 1 unavailable is tmux, never DRIFT |
| `…-attack-r1.log` | r5 legs 18:44–18:56Z / r6 legs 19:12:57–19:13:07Z | before 0/1, after 1 | R1 class 28/28 exit 0 → **0/28 exit 1** (redirect and pipe); mid-run probe 29/29 header-readable → **0/29**, incl. 0/29 seed-in-environ on the pinned run |
| `…-attack-r2.log` | r5 legs 18:44–18:51Z / r6 legs 19:13:08–19:13:21Z | before 0, after 1 | R2 class 28/28 exit 0 → **0/28 exit 1** (old table, fresh-learn replay, and the nonce-normalized variant); learn-A vs learn-B fingerprint overlap **0** |

**R1 — stdout-backchannel (receipt `…-attack-r1.log`).** Attacker: zero fixture
reads, zero grading logic; reads the run's `CASE_ORDER` (else `SHUFFLE_SEED`) from
the oracle's own captured stdout via `/proc` ancestry mid-run, replays a canned
position table and echoes the env nonce. Before (r5 `7143ccc2…`): regular-file
capture `matched=28 total=28` exit 0; pipe capture `0/28` exit 1 (channel
control); pinned-seed run `28/28` exit 0 (environ sub-channel); per-invocation
probe `29/29` invocations read the header from the oracle's captured fd/1, and on
the pinned run `29/29` read `MORI_SHUFFLE_SEED` from the oracle's environ. After
(r6 `3307761a…`): redirect `matched=0 total=28` exit 1; pipe `0/28` exit 1;
pinned-environ `0/28` exit 1; probe `0/29` header hits and `0/29` seed-in-environ
hits (unpinned **and** pinned runs) while the env nonce remains visible by design
(`29/29`). Header position is measured in the run output itself: the
`SHUFFLE_SEED=`/`RUN_NONCE=`/`CASE_ORDER=` lines sit at output lines 29-31 with
the last case line at 28 in every r6 run; the probe logs the examined ancestor
chain (`chain=<pid>:bash,…,<pid>:kimi`) per invocation. The attacker's fail text
is `census emitted no MORI_CENSUS verdict (rc=0)` — the mid-run read finds no
header, so the forged row is never emitted.

**R2 — content-keyed forgery (receipt `…-attack-r2.log`).** Witness class: learn
(F = sha256 over every file path+size+content under the case tree, excluding
`run-nonce`, `nonce-*`, `.git/index`) → (state, finding, rc) in one observed run;
replay the table in a **separate** run with the env nonce echoed; zero grading
logic. Before (r5): learn `28/28`; replay `28/28` exit 0; the nonce-normalized
variant (strips the current nonce from paths and contents before fingerprinting)
also learn/replay `28/28` exit 0 (addendum 2 in the receipt). After (r6): the
r5-learned table `0/28` exit 1; a **fresh** table learned at r6 (learn-A, 29
rows, 0 conflicts) replayed in a later run `0/28` exit 1; the normalized variant
`0/28` exit 1; learn-A vs learn-B (two separate runs) share **zero** fingerprints
(`F_set_overlap_learnA_vs_learnB=0`). Mechanism evidence: two content probes (29
invocations each) show the run nonce woven into committed file bodies
(`./root/kagi-shokunin/LOG.md`, `notes.md`, `./root/.ufo/reports/round-2/aggregator.md`,
`README.md`, …) and per-run F multisets that differ between two runs
(`80058d3e…` vs `7dff44fb…`).

Receipt-file SHA-256 at build time (final bytes, after embedded sources/addenda):

- `f9947ef1dd521ae7fb71ae10e18b5149674397f5b8093bdc6c0759677594d05d` (attack-r1)
- `5c520f2591bab2e7169c1ccda0b2e6761aace5622a3b0ced911a44c91302a9d7` (attack-r2)
- `9da735b2ea8dc34b8da974b5adaf79bf1b7a79bc16b8f99a918c3437d28af4a2` (live)
- `d0ce730a451b54e8af9ca97e8ad611e8d0cdea69c150bb8f63de3b017a5150bc` (oracle-1)
- `dcb5dff68c9f2cedfe905e813e7cf9eabb5825a392d0a4b457bb27a205838a4e` (oracle-2)
- `43ac38aca6b0a3cfa878772f9bac147a5eb800197088ebb5a3fa9e1f62bdfaf5` (oracle-3)
- `e547fdce92c0b2080c4e2f58eb186e6776e4ddcd8fc3793a165eb3320729174f` (selftest)

**What moved vs the round-5 record.** The two residuals named in `SCORECARD.md`
(R1 stdout-backchannel, R2 content-keyed forgery) are closed for the enumerated
witness classes at the pinned revision: every attack leg that reached `28/28 exit
0` at r5 reaches `0/28 exit 1` at r6, while the honest census stays `28/28` exit 0
across shuffled runs with byte-identical grade tuples and both pins reproduce
oracle-1 byte-for-byte. Registry block is byte-identical to r5 HEAD.

Re-run recipes (cwd = lane root; this receipt set applies only at the two SHAs above):

```sh
cd /home/vgpnk/Projects/shokunin/mori-shokunin
sha256sum tools/mori-silence-cases.sh  # must equal 3307761a… for this whole set
sha256sum tools/mori-census.sh         # must equal af2d4e79…
bash tools/mori-silence-cases.sh       # expect exit 0, matched=28 total=28, header AFTER the case lines
env MORI_SHUFFLE_SEED=<seed> bash tools/mori-silence-cases.sh   # same seed => same CASE_ORDER
bash tools/mori-census.sh --selftest   # hermetic; expect exit 0, PASS (30 cases, 30 passed)
bash tools/mori-census.sh              # live; expect a MORI_CENSUS verdict + per-lane rows
# attacks (sources embedded verbatim in each attack receipt; run from /tmp only):
#   bash tools/mori-silence-cases.sh /tmp/<attacker>.sh   ; the r5 before-side needs an
#   r5 oracle snapshot (git show HEAD:tools/mori-silence-cases.sh must hash 7143ccc2…)
```

**Re-run preconditions (recorded, not invented):** the live receipt describes the
host at its capture time; finding counts are mutable observations — a re-run is
"same receipt" only in formula (exit code, finding-id set, per-lane state
contract), never in byte equality. The hermetic receipts reproduce only at the
pinned r6 oracle + frozen census SHAs; a different SHA invalidates them. The
pinned-seed reproduction depends on the documented `MORI_SHUFFLE_SEED` interface;
an unpinned run necessarily produces a fresh seed and a different order. Attack
tallies are properties of the attacker scripts embedded in the receipts, not of
the census.

**Not claimed here:** no remediation, kill, restart or host/unit change was
performed or is implied; no causal claim about fleet liveness. The attack-side is
an attack-class measurement of the round-6 claim, not an impossibility proof:
only the enumerated witness classes were run (no-read replay, position-keyed
table, env-token echo, content memorization, nonce-normalized memorization, and
`/proc` stdout/environ walks); other channels (e.g. `ptrace`, non-Linux `/proc`
semantics) are outside this measurement. The environ sub-channel measurement
covers the re-exec design at `3307761a`; the earlier intermediate revision's
runtime-`unset` design and the exec-optimization artifact behind that earlier
reading are recorded in the oracle's own comments
(`tools/mori-silence-cases.sh:196-206`), not re-measured here.

## Round-7 receipts (coverage pivot: the four r2 surface gaps) — produced by the receipts-writer seat

Round-7 goal wave, seat `receipts-writer`. Detection and report only — nothing was
remediated, killed, restarted or reconfigured; no host or fleet state was written.
Fixtures live under `/tmp` only. Every receipt carries its own `CAPTURED_UTC`, exact
command(s), exit code(s) and the SHA-256 of the script bytes under test.

Two revisions are pinned by this set (and only by these SHAs). Both were uncommitted
working-tree edits at capture time; the bytes held stable for ≥2 min before the first
receipt and were re-verified unchanged at set close (19:54:52Z):

- `tools/mori-census.sh` sha256
  `c7c3569b842ab3911cbfdf415eb7023766c950c60f354af95f6a4f020b5671af` (`VERSION=census-r4`,
  2004 lines). Closes the four r2 gaps: tmux relevance (pane-cwd rule), memory pressure
  (PSI `avg10` + fill %, thresholds labeled local), disk write-rate (since-boot average;
  instantaneous rate is a bounded deferral), `state_rounds` values vs the ledger
  (`WATCHDOG_STATE_LAG`/`AHEAD` info findings).
- `tools/mori-silence-cases.sh` sha256
  `448f77238c73a5c929a898dad0f0c495fd2a66cc4b90a00ae84ede69a86beeb5` (1090 lines) —
  re-baselined only for the census's additive output; registry still 28 ids / 28 cases.

`CENSUS_SHA256_BEFORE`/`_AFTER` (and `ORACLE_SHA256_BEFORE`/`_AFTER` where exercised)
are identical within every receipt; the four gap receipts carry the oracle SHA
re-verified at set close.

| File (`surfaces-r7-20261015T1948Z-…`) | Captured UTC | Exit | Verdict / tally |
|---|---|---|---|
| `selftest.log` | 19:48:31–19:48:47Z | 0 | `MORI_CENSUS_SELFTEST: PASS (45 cases, 45 passed, 0 failed)`; 15 new cases: tmux ×3, pressure/fill ×5, write-rate ×3, state values ×4 |
| `oracle.log` | 19:49:13–19:49:39Z | 0 / 0 | `matched=28 total=28` both runs; fresh shuffle then `MORI_SHUFFLE_SEED=1503128629` rerun → `ORDER_IDENTICAL_WHEN_SEED_PINNED=yes`; header at output line 29, after all 28 case lines |
| `live.log` | 19:50:06–19:50:17Z | 1 / 1 / 1 | new ×2 + r6-from-HEAD ×1 all `DRIFT (findings=15 drift=14 unavailable=1 surfaces=7)`; per-surface `key=` diff old→new: `old_only_keys=[]` for all seven surfaces; added keys exactly `state_rounds_max/state_lag/state_ahead/state_cmp/state_val_unreadable` (watchdog), `local_oom_kill/psi_some_avg10/psi_full_avg10/psi_source/psi_warn_avg10/mem_fill_pct/mem_fill_scope/host_mem_avail_pct` (cgroup), `io_basis/io_avg_since_boot/io_avg_unavailable` (disk) |
| `tmux.log` | 19:50:42–19:50:52Z | 1 ×5 | live `unavailable (rc=1)` — no tmux server on this host at capture; controlled stub arm `sessions=2; relevant=1 foreign=1 unclassified=0` + `TMUX_FOREIGN_SESSION session=nw`; stub `list-panes` rc=2 arm → `relevance=unavailable reason=panes-rc=2` + `TMUX_RELEVANCE_UNAVAILABLE … unnoticed_but_counted` |
| `memory.log` | 19:51:45–19:52:03Z | 1 ×5 | live row: `psi_some_avg10=0.00 psi_full_avg10=0.00 psi_source=ok psi_warn_avg10=10 mem_fill_pct=unavailable mem_fill_scope=host-ram host_mem_avail_pct=59` (slice max=unlimited); arm `psi=99.00` → `MEM_PRESSURE_HIGH` warn (threshold 10, labeled local); control `9.99` silent; numeric limit at 90% fill → `MEM_FILL_HIGH` warn (threshold 85, labeled local); control 4× limit silent |
| `diskrate.log` | 19:53:31–19:54:02Z | 1 / 1 / 1 | live `io_basis=since-boot io_avg_since_boot=dm-0:9549258Bps/11748s io_avg_unavailable=tmpfs:not-a-block-device`; manual `sectors*512/uptime` = 9547128Bps ~11 s later (drift note in receipt); fixture diskstats → `dm-0:10534Bps/600s` = exact manual 12345*512/600; fixture without dm-0 → `dm-0:device-not-in-diskstats`; measured 10 s instant sample 715980Bps (addendum: single-pair noise is the datum behind the deferral) |
| `staterounds.log` | 19:54:26–19:54:36Z | 1 / 1 / 1 | live values listed next to the ledger's launch lines; fixture lag/ahead: `state_rounds=3 state_rounds_max=99 state_lag=1 state_ahead=1 state_cmp=3` + `WATCHDOG_STATE_LAG lane=kagi state_round=1 ledger_round=7` / `WATCHDOG_STATE_AHEAD lane=kama state_round=99 ledger_round=7`; mode-000 value arm → `state_val_unreadable=1`, verdict still emitted (no crash) |

**Additive-only output.** The live receipt runs the r6 census bytes (`git show
HEAD:tools/mori-census.sh`, sha `af2d4e79…`) and the r7 census side by side and diffs
the per-surface `key=` token sets: no r6 key is lost on any of the seven surfaces, and
the only new keys are the four gaps' fields listed above. The verdict-line shape is
unchanged. This is the "re-baselined ONLY for additive output" check for this round.

**Live-state honesty.** `sessions=1`-style claims from r2 are superseded by the rule,
but on this host at capture time tmux had no server, so the live relevance row is
`unavailable` (disclosed, never DRIFT) and the classification is demonstrated only in
the controlled stub arm. All live numbers are mutable host observations pinned to one
clock; a re-run reproduces formula (exit codes, surface states, schema keys), never
byte equality. The r6 census run in `live.log` shows the host's drift too (journal
counts and wave ages differ from the round-6 receipts).

**Not claimed here:** no remediation/kill/restart/host-config change; no causal claim
about fleet liveness; the since-boot write average is not an instantaneous rate (that
is the recorded bounded deferral); the tmux relevance rule is path-based and its
boundary (a fleet worker whose pane cwd is outside the fleet root reads `foreign`) is
disclosed on the row; thresholds (`psi_warn_avg10=10`, `mem_fill 85`, `mem_avail 10`,
`io_basis`) are LOCAL placeholders, never tuned as universal.

Re-run recipes (cwd = lane root; this receipt set applies only at the two SHAs above):

```sh
sha256sum tools/mori-census.sh         # must equal c7c3569b… for this whole set
sha256sum tools/mori-silence-cases.sh  # must equal 448f7723…
bash tools/mori-census.sh --selftest   # hermetic; expect exit 0, PASS (45 cases, 45 passed)
bash tools/mori-silence-cases.sh       # expect exit 0, matched=28 total=28, header AFTER the case lines
bash tools/mori-census.sh              # live; expect a MORI_CENSUS verdict + the new gap fields on the rows
# controlled gap arms (fixtures /tmp only; sources embedded in each receipt):
#   tmux:   MORI_TMUX_BIN=<stub with ls + list-panes -a> bash tools/mori-census.sh
#   memory: MORI_CGROUP_PRESSURE=<fx pressure> bash tools/mori-census.sh
#           MORI_CGROUP_MAX=<fx limit>        bash tools/mori-census.sh
#   disk:   MORI_DISKSTATS=<fx> MORI_UPTIME=<fx> bash tools/mori-census.sh
#   state:  MORI_STATE_DIR=<fx> MORI_TIMELINE_FILE=<fx ledger> bash tools/mori-census.sh
```

Receipt-file SHA-256 at set close (after all embedded sources/addenda):

- `ca9f50fd3e398a11c795533ba941a92f3a72ea1fe8edaaf64d4068058d763d33` (selftest)
- `e29b9507dc4ac7659e5ac53d8466ebff30de67f5675890140f569f057b16a5ff` (oracle)
- `b8342bdd514fd17d31f66f560fc64b26eb05d76e024961ce7470c27f457ffcae` (live)
- `6a7ad7b138fb09decaedcfa7b390ad2c67c939fce681400ba9a12e9f303aaf7f` (tmux)
- `a5be36cb1196fc9659c29fc4e5b86a0e83dd48482e637a046fb64e3fdf5e8499` (memory)
- `8b6ec98377b0eb14b7b29b28e087ea4362808ab8f547f7eadd4a15faa0aee9d6` (diskrate)
- `b5e756922ac6b067a1b2e6e41e0f7fd96f8a78f710bb9d4dd6e160707b6054e7` (staterounds)