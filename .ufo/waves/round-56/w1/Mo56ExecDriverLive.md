# Mo56ExecDriverLive — live run of the round-56 C1 driver-liveness probe

Seat: Mo56ExecDriverLive (executor, mori-shokunin lane, round 56 wave w1).
Lane scope: fleet and host observability — fleet liveness, wave settlement, kill/OOM events,
resource runway. Detection and report only; nothing was remediated.

Frozen inputs read:
- `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-56/contract.md` (C1 predicate,
  kill rules, "counters/predicates/controls are frozen" clause).
- Tool under test: `/home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-driver-liveness.py`.

MACHINE_ID: host read-only; no machine identifier, credential, session token or private URL is
reproduced anywhere in this report.

---

## 1. What was executed

Scratch (operator directive 2026-10-25), removed at the end of the seat:

```
mkdir -p /fast/scratch/hyaku/mori-r56/Mo56ExecDriverLive/tmp
export TMPDIR=/fast/scratch/hyaku/mori-r56/Mo56ExecDriverLive/tmp
cd /fast/scratch/hyaku/mori-r56/Mo56ExecDriverLive
```

Disk gate first: `bash /home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status` → exit 0,
`/fast/scratch/hyaku` 28% used, 586.0G free. No ENOSPC condition; no pacman / no tool install was
needed (stock `python3` only), so no tool/version/channel row to record.

Three live runs (the assignment's requirement), plus a fourth run 20 s later and one run with the
tool's own default `--fleet-root` derivation:

```
$ for i in 1 2 3; do python3 .../tools/mori-driver-liveness.py \
      --fleet-root /home/vgpnk/Projects/shokunin > run$i.json 2> run$i.err; echo "run$i exit=$?"; done
run1 exit=0
run2 exit=0
run3 exit=0
```

All three stderr captures are 0 bytes. A fourth run (run4) and a default-args run were also taken;
`default-run.json` used the same log path `/home/vgpnk/Projects/shokunin/.ufo/watchdog.log`
(default fleet root resolves to the parent of the tool's repo, i.e. the fleet root) and produced
the same 23-lane report.

---

## 2. Required checks — all pass, all three runs

| Check | Result | Runs |
|---|---|---|
| Output is valid JSON | yes — `json.loads` succeeded on run1/run2/run3 (keys: `lanes, log, notes, rc, schema, state_dir, verdict`) | 3/3 |
| `verdict == "DRIVER_LIVENESS_OK"` | yes | 3/3 |
| Exit code 0 | yes | 3/3 |
| `lanes` set == union(lane ids in `shokunin.conf`, `*.round` names in `.ufo/state/`) | yes — exact set equality, `missing=[] extra=[]` | 3/3 |
| `mori.in_flight == true` | yes | 3/3 |
| `log.malformed == 0` | yes | 3/3 |

Lane-set computation was done independently of the tool (the tool never reads `shokunin.conf`):

- lane ids parsed from `/home/vgpnk/Projects/shokunin/shokunin.conf` (regex `^\s*([A-Za-z0-9_.-]+)\|`,
  multi-line `LANES=` accumulation): **23** — aggregator, audio, chousa, game-dev-2d, game-dev-3d,
  kagi, kaidoku, kake, kama, kasegi, kengaku, kotoba, kotodama, kumitate, lore, mado, mori, protocol,
  revenger, souji, tabi, tameshi, tsukuroi.
- `*.round` names in `/home/vgpnk/Projects/shokunin/.ufo/state/`: **21** (kotodama and souji have no
  `.round` file — only `.report-baseline`).
- union = **23**; the tool's `lanes` key set = **23**, equal.
- All 23 conf lane ids are inside the tool's lane charset `[A-Za-z0-9_-]` (0 ids outside it), so no
  conf lane can be silently dropped by the grammar.

### Per-run mutable values (the assignment asked for lane count and mori unclosed across runs)

| run | lanes | mori.unclosed | mori.in_flight | mori.launches/completes/deads | log.lines | log.malformed | log.other_lines |
|---|---|---|---|---|---|---|---|
| 1 | 23 | 10 | true | 66 / 39 / 17 | 1729 | 0 | 121 |
| 2 | 23 | 10 | true | 66 / 39 / 17 | 1729 | 0 | 121 |
| 3 | 23 | 10 | true | 66 / 39 / 17 | 1729 | 0 | 121 |
| 4 (+20 s) | 23 | 10 | true | 66 / 39 / 17 | 1729 | 0 | 121 |

The only byte-level differences between run1 and run3 are the age fields
(`last_launch_age_s` ×23 and `log.mtime_age_s`), i.e. the wall-clock derivative — `diff run1.json run3.json`
shows 24 changed lines, all of them `last_launch_age_s`/`mtime_age_s`. No count, verdict, or
lane-membership field moved. `mori.last_launch_age_s` was 3039.24 / 3039.27 / 3039.299 across the
three runs — a ~50-minute-old launch, consistent with the live mori r56 dispatch at
`2026-10-27T10:08:36-03:00`.

### mori `unclosed=10` is stable across runs, but 9 of the 10 are historical residue

Recomputing the pairing independently (same grammar, no tool code) yields the identical set for
mori: `[(2,None), (19,2), (20,1), (21,1), (22,1), (37,1), (38,1), (38,3), (40,1), (56,1)]`.
Only `(56,1)` is the currently-live round; the other nine are rounds 2–40 whose `complete` line was
never written in the log (see Finding 2). So `unclosed` is a monotone historical backlog counter, not
a "10 things are running now" number. This is consistent with the tool's own note ("unclosed … a
pairing count, not a failure claim") and with the contract wording, but a reader skimming only the
number can easily misread it.

---

## 3. Full JSON (run 1, verbatim)

```json
{
 "lanes": {
  "aggregator": {
   "completes": 7,
   "deads": 0,
   "in_flight": true,
   "last_launch_age_s": 1069698.24,
   "last_launch_ts": 1792039857.0,
   "launch_fails": 0,
   "launches": 9,
   "rounds_seen": 8,
   "unclosed": 2,
   "wraps": 2
  },
  "audio": {
   "completes": 0,
   "deads": 0,
   "in_flight": true,
   "last_launch_age_s": 1070013.24,
   "last_launch_ts": 1792039542.0,
   "launch_fails": 0,
   "launches": 1,
   "rounds_seen": 1,
   "unclosed": 1,
   "wraps": 0
  },
  "chousa": {
   "completes": 30,
   "deads": 13,
   "in_flight": true,
   "last_launch_age_s": 8585.24,
   "last_launch_ts": 1793100970.0,
   "launch_fails": 0,
   "launches": 49,
   "rounds_seen": 35,
   "unclosed": 7,
   "wraps": 0
  },
  "game-dev-2d": {
   "completes": 0,
   "deads": 0,
   "in_flight": true,
   "last_launch_age_s": 1070013.24,
   "last_launch_ts": 1792039542.0,
   "launch_fails": 0,
   "launches": 1,
   "rounds_seen": 1,
   "unclosed": 1,
   "wraps": 0
  },
  "game-dev-3d": {
   "completes": 0,
   "deads": 0,
   "in_flight": true,
   "last_launch_age_s": 1070013.24,
   "last_launch_ts": 1792039542.0,
   "launch_fails": 0,
   "launches": 1,
   "rounds_seen": 1,
   "unclosed": 1,
   "wraps": 0
  },
  "kagi": {
   "completes": 18,
   "deads": 0,
   "in_flight": false,
   "last_launch_age_s": 199673.24,
   "last_launch_ts": 1792909882.0,
   "launch_fails": 1,
   "launches": 28,
   "rounds_seen": 23,
   "unclosed": 10,
   "wraps": 2
  },
  "kaidoku": {
   "completes": 29,
   "deads": 8,
   "in_flight": false,
   "last_launch_age_s": 17709.24,
   "last_launch_ts": 1793091846.0,
   "launch_fails": 0,
   "launches": 42,
   "rounds_seen": 31,
   "unclosed": 6,
   "wraps": 0
  },
  "kake": {
   "completes": 51,
   "deads": 16,
   "in_flight": false,
   "last_launch_age_s": 3776.24,
   "last_launch_ts": 1793105779.0,
   "launch_fails": 1,
   "launches": 79,
   "rounds_seen": 57,
   "unclosed": 12,
   "wraps": 2
  },
  "kama": {
   "completes": 41,
   "deads": 14,
   "in_flight": true,
   "last_launch_age_s": 3587.24,
   "last_launch_ts": 1793105968.0,
   "launch_fails": 1,
   "launches": 66,
   "rounds_seen": 46,
   "unclosed": 11,
   "wraps": 3
  },
  "kasegi": {
   "completes": 33,
   "deads": 4,
   "in_flight": false,
   "last_launch_age_s": 21837.24,
   "last_launch_ts": 1793087718.0,
   "launch_fails": 1,
   "launches": 42,
   "rounds_seen": 34,
   "unclosed": 6,
   "wraps": 3
  },
  "kengaku": {
   "completes": 33,
   "deads": 3,
   "in_flight": false,
   "last_launch_age_s": 15355.24,
   "last_launch_ts": 1793094200.0,
   "launch_fails": 2,
   "launches": 40,
   "rounds_seen": 35,
   "unclosed": 6,
   "wraps": 3
  },
  "kotoba": {
   "completes": 41,
   "deads": 11,
   "in_flight": false,
   "last_launch_age_s": 132846.24,
   "last_launch_ts": 1792976709.0,
   "launch_fails": 1,
   "launches": 58,
   "rounds_seen": 42,
   "unclosed": 7,
   "wraps": 3
  },
  "kotodama": {
   "completes": 25,
   "deads": 12,
   "in_flight": false,
   "last_launch_age_s": 137416.24,
   "last_launch_ts": 1792972139.0,
   "launch_fails": 0,
   "launches": 40,
   "rounds_seen": 25,
   "unclosed": 4,
   "wraps": 0
  },
  "kumitate": {
   "completes": 49,
   "deads": 9,
   "in_flight": false,
   "last_launch_age_s": 24873.24,
   "last_launch_ts": 1793084682.0,
   "launch_fails": 0,
   "launches": 57,
   "rounds_seen": 49,
   "unclosed": 3,
   "wraps": 3
  },
  "lore": {
   "completes": 0,
   "deads": 1,
   "in_flight": true,
   "last_launch_age_s": 1069698.24,
   "last_launch_ts": 1792039857.0,
   "launch_fails": 0,
   "launches": 2,
   "rounds_seen": 1,
   "unclosed": 1,
   "wraps": 0
  },
  "mado": {
   "completes": 38,
   "deads": 21,
   "in_flight": true,
   "last_launch_age_s": 6203.24,
   "last_launch_ts": 1793103352.0,
   "launch_fails": 0,
   "launches": 61,
   "rounds_seen": 41,
   "unclosed": 5,
   "wraps": 0
  },
  "mori": {
   "completes": 39,
   "deads": 17,
   "in_flight": true,
   "last_launch_age_s": 3039.24,
   "last_launch_ts": 1793106516.0,
   "launch_fails": 0,
   "launches": 66,
   "rounds_seen": 46,
   "unclosed": 10,
   "wraps": 0
  },
  "protocol": {
   "completes": 11,
   "deads": 0,
   "in_flight": true,
   "last_launch_age_s": 1069698.24,
   "last_launch_ts": 1792039857.0,
   "launch_fails": 0,
   "launches": 13,
   "rounds_seen": 12,
   "unclosed": 2,
   "wraps": 1
  },
  "revenger": {
   "completes": 10,
   "deads": 2,
   "in_flight": false,
   "last_launch_age_s": 148654.24,
   "last_launch_ts": 1792960901.0,
   "launch_fails": 0,
   "launches": 16,
   "rounds_seen": 11,
   "unclosed": 4,
   "wraps": 0
  },
  "souji": {
   "completes": 21,
   "deads": 3,
   "in_flight": true,
   "last_launch_age_s": 18876.24,
   "last_launch_ts": 1793090679.0,
   "launch_fails": 0,
   "launches": 27,
   "rounds_seen": 22,
   "unclosed": 4,
   "wraps": 0
  },
  "tabi": {
   "completes": 23,
   "deads": 3,
   "in_flight": true,
   "last_launch_age_s": 3264.24,
   "last_launch_ts": 1793106291.0,
   "launch_fails": 0,
   "launches": 32,
   "rounds_seen": 27,
   "unclosed": 7,
   "wraps": 0
  },
  "tameshi": {
   "completes": 37,
   "deads": 21,
   "in_flight": true,
   "last_launch_age_s": 4193.24,
   "last_launch_ts": 1793105362.0,
   "launch_fails": 0,
   "launches": 65,
   "rounds_seen": 43,
   "unclosed": 8,
   "wraps": 0
  },
  "tsukuroi": {
   "completes": 35,
   "deads": 8,
   "in_flight": false,
   "last_launch_age_s": 21833.24,
   "last_launch_ts": 1793087722.0,
   "launch_fails": 0,
   "launches": 47,
   "rounds_seen": 37,
   "unclosed": 5,
   "wraps": 0
  }
 },
 "log": {
  "examples": [],
  "lines": 1729,
  "malformed": 0,
  "mtime_age_s": 140.28496313095093,
  "newest_ts": 1793109414.0,
  "other_lines": 121,
  "path": "/home/vgpnk/Projects/shokunin/.ufo/watchdog.log"
 },
 "notes": [
  "in_flight/unclosed are log-shape facts, not health verdicts",
  "state *.round values are never read here; symlinks never followed",
  "lane-dead-no-report clears that round's open launches (a retry follows)"
 ],
 "rc": 0,
 "schema": "mori-driver-liveness-v1",
 "state_dir": {
  "dir": 0,
  "other": 0,
  "regular": 21,
  "symlink": 0
 },
 "verdict": "DRIVER_LIVENESS_OK"
}
```

---

## 4. Independent corroboration of the live numbers

The tool's parsing was re-implemented from scratch in the seat scratch (regexes transcribed from the
frozen source, then applied to the raw log) so the probe is not graded on its own output:

- independent malformed count = **0**, independent non-event (other) lines = **121**, independent
  event lines = **1608**; total 1729 — exactly the tool's `lines=1729 / malformed=0 / other_lines=121`.
- independent lane set = 23 = tool's 23; independent union with conf + `*.round` = 23 = tool's 23.
- independent mori pairing open set = 10 keys = tool's `mori.unclosed=10`.
- `state_dir` shape census by the seat = `{'regular': 21}`; the tool reports
  `{"regular": 21, "symlink": 0, "dir": 0, "other": 0}` — matches. `*.round` file count on disk = 21.
- Read-only claim checked empirically: a full snapshot of every path under
  `/home/vgpnk/Projects/shokunin/.ufo` (mtime_ns + size) before and after a live run shows
  **0 files created, 0 files changed**. Run wall time 0.033 s, stdout 6190 bytes, rc 0.

Grammar census of the live log (independent, all 1608 event lines): launch forms = bare 1,
`mission` 3, `runId` 93, `pid` 50, `pgid+attempt` 695; complete forms = `; respawning` 98,
`; hyaku-inline attempt=1` 393, `=2` 62, `=3` 17, `=4` 1; dead forms = bare 7, with-parenthetical 159;
`launch-fail` 7; `wrap` 22 (all `; NOT respawning (fleet-wrap)`). Every one of these is in the
frozen grammar — hence malformed=0 is a real property of the current log, not a lenient parser.

---

## 5. Frozen counters re-run (read-only, at the named revisions)

The counters were run read-only against the frozen revisions; no fixture or repo file was touched.

```
$ python3 .../count-c1.py 8be2717b0809281d07dffe83dad424a4859e0747
C1=met selftest=ok fixtures=ok entry=ok row=ok norem=ok rev=8be2717b0809281d07dffe83dad424a4859e0747   exit=0
$ python3 .../count-c2.py 8be2717b0809281d07dffe83dad424a4859e0747
C2=met selftest=ok tally=ok control=ok contrast=voted0 entry=ok row=ok rev=8be2717b0809281d07dffe83dad424a4859e0747   exit=0
$ python3 .../count-c1.py 3f494b49cde612d929e82887a48e1660c022c359   -> C1=met ... exit=0
$ python3 .../count-c2.py 3f494b49cde612d929e82887a48e1660c022c359   -> C2=met ... exit=0
$ python3 .../count-c1.py 5b295eeebd87ebd610d8d39bfe2035742f740cfa
C1=unmet selftest=bad fixtures=bad entry=bad row=bad norem=bad failed=tool_absent rev=5b295eee...   exit=1
$ python3 .../count-c2.py 5b295eeebd87ebd610d8d39bfe2035742f740cfa
C2=unmet selftest=ok tally=ok control=ok contrast=voted0 entry=ok row=ok rev=5b295eee... failed=tool_absent   exit=1
```

The entering-tip (5b295eee) do-nothing result reproduces the frozen control receipt
`failed=tool_absent` exactly; the freeze-tip (8be2717b) and freeze-commit (3f494b49) results
reproduce `C1=met` / `C2=met`.

Frozen-tool identity check: `sha256sum tools/mori-driver-liveness.py` =
`6b3dba74c639190e7e96b6bed8e6ac8f285a51ce6d910fbe92e6dd39bf7be997`, identical to
`git show 8be2717b:tools/mori-driver-liveness.py | sha256sum` and equal to the `PIN` constant in
`count-c1.py:46`. The working-tree tool is byte-identical to the frozen blob (the lane worktree has
no modification to `tools/`).

Tool selftest and fixtures, run directly by the seat (independent of the counter):

```
$ python3 tools/mori-driver-liveness.py --selftest
DRIVER_LIVENESS_SELFTEST pass=13 fail=0 skipped=0        exit=0
```

All nine frozen fixtures re-parsed directly with the expected malformed counts:
hyaku-pairing 0, attempt-rollover 0, legacy-grammar 0, in-flight 0, malformed 5, fails-and-dead 0,
state-shapes 0, two-lanes 0, variants 0 — every one matching `EXPECT_FIX` in `count-c1.py`.

Note for the L1 (not a change request): the literal command in the round-56 brief and in the
contract, `python3 .../count-c1.py R`, exits 2 with `C1_SETUP: unresolvable revision R` — `R` is
not a resolvable git ref in this lane (`git rev-parse R` → exit 128; `jj log -r R` → "Change ID
prefix `r` is ambiguous"; there is no tag/branch named `R`). The frozen receipts were produced by
passing a concrete sha (`rev=3f494b49…` in `evidence/c1-at-freeze.txt`), so the receipts themselves
are sound. This is a reproducibility wart in the *invocation string*, not in the counter logic.

---

## 6. Falsification attempts on the live claim (what I tried to break)

| Attack | Method | Outcome |
|---|---|---|
| Break JSON validity | parse run1/2/3 with `json.loads` | all valid |
| Break verdict | n/a | `DRIVER_LIVENESS_OK` in 3/3 |
| Break lane-set equality | recompute union from conf + `*.round` independently | exact equality, 0 missing / 0 extra |
| Break `mori.in_flight` | recompute last-event-per-lane independently | `true` (last mori event = `launch mori round=56 … attempt=1` at 10:08:36) |
| Break `malformed=0` | re-implement the whole grammar and re-scan all 1729 lines | 0 malformed; the frozen grammar covers every observed form |
| Break read-only | snapshot all of `.ufo` before/after | 0 created, 0 changed |
| Break determinism | 3 runs + a 4th 20 s later | only age fields differ |
| Break `unclosed` semantics | independent pairing recompute | identical open-key set for mori (10 keys) |
| Break pairing on `wrap` | recompute with "wrap clears the whole round" instead of "wrap closes only the `(round,None)` key" | **identical totals** (123 open across all lanes in both models) — on this log the asymmetry is inert (see Finding 3) |
| Break pairing on a mismatched attempt | scan for a `complete … attempt=N` with no matching open `(round,N)` | exactly 1 case in the whole log (kumitate r50) — inert on totals (Finding 4) |
| Break `state_dir` shape census | recompute shapes from `os.path` | `{'regular': 21}` = tool output |
| Break the "no health verdict" claim | grep the **whole** tool source for `healthy|unhealthy|failed lane|is stuck|wedged` | one hit only, inside the guard case itself (`tools/mori-driver-liveness.py:422`, the `t_no_health_verdict` assertion); no health verdict in the emitted vocabulary |
| Break the lane-id charset assumption | feed `lane.with.dot` | dropped as `other_line` (not malformed), lane not reported — a silent-loss channel for any future lane id containing a dot (Finding 5) |
| Break the "missing log ≠ zero" rule | point `--log` at a nonexistent path | rc 2, `DRIVER_LIVENESS_UNAVAILABLE`, `state: absent` — "unavailable is never zero" holds |
| Break selftest robustness | run `--selftest` from a copy of the tool with no fixture tree beside it | `pass=2 fail=0 skipped=11`, **exit 0** — the selftest degrades to skips and still exits 0 (Finding 6) |

---

## Findings

1. **MED — `unclosed` is a monotone historical backlog, not a live-queue count.**
   `tools/mori-driver-liveness.py:143-152` (open-launch bookkeeping) and the emitted
   `unclosed` field. Live evidence: `mori.unclosed = 10` in all runs, but the independently
   recomputed open-key set is `[(2,None),(19,2),(20,1),(21,1),(22,1),(37,1),(38,1),(38,3),(40,1),(56,1)]`
   — only `(56,1)` is the current round; the other nine are rounds 2–40 whose `complete` line was
   never written. Because a launch is only closed by a `complete`/`wrap` for the same
   `(round, attempt)` key and `lane-dead-no-report` clears the round, every driver-advance that
   skips the `complete` line leaves a permanent residue entry. Consequence for the mori lane: a
   reader who takes `unclosed=10` as "10 rounds in flight" is wrong; the actionable live signal is
   `in_flight` plus `last_launch_age_s`. The tool's own notes say this, but the numeric field name
   invites the misreading. Named limit — route a round-57 item to expose an age-bounded or
   round-bounded open count (e.g. unclosed-for-the-current-round) alongside the raw counter. No
   change to the frozen predicate or counter is proposed or made here.

2. **MED — the driver log has no "round advanced without a complete" line, so a lane's residue is
   unrecoverable from the log.** Writer side: `/home/vgpnk/Projects/shokunin/scripts/hyaku/inline.sh`
   `advance` branch (lines ~203-212) writes `state/next/<lane>` and releases the claim but emits
   **no** `watchdog.log` line; only `inline.sh:176` (`log "complete … hyaku-inline attempt=…"`) and
   `inline.sh:182` (`lane-dead-no-report`) reach the log. Live evidence: mori rounds 19, 20, 21, 22
   appear in the log as `launch … attempt=N` with **no** matching `complete`, and the next round's
   launch follows. The probe therefore cannot distinguish "round finished but the complete line was
   never written" from "round is still open". The probe is correctly silent about this (it reports
   log-shape facts only); the missing signal is a driver-side one. Route to round 57: an
   `advance`-side log line (or a `state/next` cross-read) would close the loop. No fleet file was
   modified by this seat.

3. **MED — `wrap` closes only the `(round, None)` open key, unlike `lane-dead-no-report` which
   clears the whole round.** `tools/mori-driver-liveness.py:170-176` (wrap branch) vs. `:177-183`
   (dead branch): the wrap branch calls `close_round()`, which removes `(round,None)` only, so an
   attempt-keyed launch closed by a `wrap` stays counted as unclosed. Measured on the live log: the
   effect is **inert** — a recompute with "wrap clears the whole round" yields identical totals
   (123 open across all lanes in both models) and zero wrap events left an attempt-keyed launch
   open, because every live `wrap` is a legacy `pgid`-form round with no `attempt=` key. It is
   latent, not active: it would activate the first time the legacy watchdog and the inline driver
   overlap on the same lane/round. Route as a round-57 fixture case (wrap after an attempt-keyed
   launch); the frozen fixtures do not currently cover it.

4. **LOW — one live `complete` in the whole log matches no open launch.**
   `tools/mori-driver-liveness.py:158-166` (complete branch): a `complete … attempt=N` whose open
   key is `(round,N)` does not exist falls back to `(round,None)`; if neither exists the complete
   closes nothing. Live evidence: exactly one occurrence —
   `2026-10-23T22:23:30-03:00 complete kumitate round=50; hyaku-inline attempt=2`, where the open
   keys at that moment were `[(50,1),(50,3),(50,1)]` (kumitate r50 had three attempt-1/2/3 launches
   interleaved with `lane-dead-no-report` lines that had already cleared the round). Effect on the
   reported totals is nil (the round was later cleared by a dead/next event). Latent mis-pairing
   channel; route a fixture case for round 57.

5. **LOW — a lane id outside `[A-Za-z0-9_-]` is silently downgraded to `other_line`, not counted
   malformed.** `tools/mori-driver-liveness.py:81-84` (`LINE_RE` lane group). Probe: a log line
   `launch lane.with.dot round=1 pgid=1` yields `lanes=[]`, `malformed=0`, `other_lines=2` — the
   event disappears from the lane table without ever being flagged. Today's 23 conf lane ids are
   all inside the charset (verified), so there is no live loss; the risk is a future mint with a dot
   or another punctuation character. Route as a round-57 item (either widen the charset or count an
   unparseable-but-keyword-shaped line as malformed).

6. **LOW — `--selftest` exits 0 when the fixture tree is absent.** Probe: copying only
   `tools/mori-driver-liveness.py` to a directory with no `.ufo/waves/round-56/fixtures/driver/`
   yields `DRIVER_LIVENESS_SELFTEST pass=2 fail=0 skipped=11` with **exit 0**
   (`tools/mori-driver-liveness.py:436-447` treats `None` returns as skips). The C1 counter is not
   exposed to this (it materializes the fixtures itself and asserts the exact
   `pass=13 fail=0 skipped=0` string), so the frozen claim is unaffected; but a bare `--selftest`
   invocation is a weak gate on its own. Route as a round-57 item (fail when the fixture tree is
   missing, or when `skipped>0`).

7. **LOW — the `R` revision in the documented counter command does not resolve.**
   `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-56/contract.md` (C1 command
   `python3 .ufo/waves/round-56/count-c1.py R`) and the round-56 brief. Observed: exit 2,
   `C1_SETUP: unresolvable revision R`; `git rev-parse R` exits 128 and `jj log -r R` reports an
   ambiguous change-ID prefix. The frozen receipts were produced with a concrete sha
   (`evidence/c1-at-freeze.txt`: `rev=3f494b49cde612d929e82887a48e1660c022c359`) and reproduce
   exactly when re-run. Reproducibility wart in the invocation string only — a documented alias
   (e.g. the freeze commit sha) would make the receipt re-derivable verbatim.

8. **LOW — `DRIVER_LIVENESS_OK` is emitted for a log whose every line is garbage.**
   `tools/mori-driver-liveness.py:207-238` (`run`): the verdict is `OK` whenever the file is
   readable and non-empty, regardless of `malformed` count or lane coverage. Probe with a
   two-garbage-line fixture: `verdict=DRIVER_LIVENESS_OK`, `malformed=2`, `lanes=0`, rc 0. This is
   by design (the verdict is "the probe ran", not "the fleet is well"), and the contract's
   "per-lane log-shape facts only" reading supports it — but the string `DRIVER_LIVENESS_OK` on a
   report with zero lanes is the kind of token a downstream consumer can misread as a health
   signal. No change proposed to the frozen verdict vocabulary; flagged so round 57 can decide
   whether a lane-count or malformed-count precondition belongs in the contract's prose.

9. **LOW — the live log is single-file and never rotated, so the probe's history grows unbounded.**
   `/home/vgpnk/Projects/shokunin/.ufo/watchdog.log` is 163775 bytes, 1729 lines, first line
   `2026-09-28T15:44:59-03:00`, no `watchdog.log.*` siblings. The probe reads the whole file
   (0.033 s at current size), so this is not yet a cost problem, but every lane's `unclosed`
   residue (Finding 1) accumulates across the whole retained history and the per-run cost grows
   linearly with log age. Route to round 57 as an observability item (rotation policy, or a
   bounded window the probe states explicitly).

10. **INFO — `mori.in_flight=true` is corroborated by independent host evidence.**
    The last mori event in the log is `2026-10-27T10:08:36-03:00 launch mori round=56 pgid=620717
    driver=hyaku-inline attempt=1`, and `mori.last_launch_age_s` was ~3039 s at run time. The
    `.ufo/state/mori.round` file still reads `2` (stale — the inline driver tracks rounds in
    `state/next/<lane>`, not in `.ufo/state/*.round`), and no process with pgid 620717 was found
    in `/proc` at read time (the inline driver's `pgid=$$` is the short-lived dispatching shell,
    `inline.sh:149`, not the substrate process group). The fleet-level round-56 dispatch is
    confirmed instead by `.ufo/state/inline-dispatcher.log`
    (`partial mori 56 w1 24 64` at 11:01:50). Nothing here contradicts the probe, but it does mean
    the probe's `in_flight` is a log-shape fact about the last recorded event — not a process-liveness
    probe — which is exactly what its `notes` field states.

## Scope and hygiene

- Files written by this seat: this report only
  (`.ufo/waves/round-56/w1/Mo56ExecDriverLive.md`) plus the scratch tree
  `/fast/scratch/hyaku/mori-r56/Mo56ExecDriverLive/`, which was removed on exit.
- No git/jj mutation in `/home/vgpnk/Projects/shokunin` or `mori-shokunin`; only read-only
  `git log/show/rev-parse/status/for-each-ref` and `jj log/bookmark list` were used.
- No write to `/home/vgpnk/Projects/shokunin/.ufo/watchdog.log` or `.ufo/state`; verified by
  before/after snapshot (0 created, 0 changed).
- No host mutation: no sysctl, no cgroup, no systemctl, no process killed or steered; `/proc`,
  `/sys` and fleet logs were read only. No journal record was counted by MESSAGE text.
- The lane worktree already carried unrelated modifications (`LOG.md`, `SCORECARD.md`, `SHONEN.md`
  modified; untracked `.ufo/waves/round-56/w1/`, `corpus/lessons/round-56.md`,
  `.ufo/waves/round-56/w1.ready*`) at the time of the run; these are other seats'/the L1's work
  and were left untouched.
