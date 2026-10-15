# Round 7 — scribe measurement ledger (working record)

Seat: scribe (round-7 goal wave, 32 seats) · lane mori-shokunin · writes only under
`.ufo/round-7/goal-wave/`. Detection and report only; fixtures `/tmp` only; no fleet writes.
This ledger carries the raw first-hand measurements the three drafts cite; it is a working
record, not a deliverable.

## Pinned bytes at scribe clock

| Artifact | sha256 | Version/label |
|---|---|---|
| `tools/mori-census.sh` (before) | `af2d4e79e69b70bb0b5aecd6acc9608fc7c16b0716766d4a60310e0689d350d7` | `VERSION=census-r3`, 1438 lines |
| `tools/mori-silence-cases.sh` (before) | `3307761a04a1eab8f33859a69d2eb63fb6312afb8f8041f7b09da4544be174b9` | r6 oracle, 1082 lines |

Both unchanged at 19:23:21Z (poll baseline) and re-verified 19:25Z.

## Verdict-machine baseline (before, first-hand)

| Check | Command | Verbatim tail | Exit |
|---|---|---|---|
| selftest | `bash tools/mori-census.sh --selftest` | `MORI_CENSUS_SELFTEST: PASS (30 cases, 30 passed, 0 failed)` | 0 |
| oracle | `bash tools/mori-silence-cases.sh` | `MORI_SILENCE_CASES: matched=28 total=28` | 0 |
| live census | `bash tools/mori-census.sh` | `MORI_CENSUS: DRIFT (findings=15 drift=14 unavailable=1 surfaces=7)` | 1 |

Oracle `CASE_ORDER` at this run (28 ids, one shuffled order; captured in `/tmp/scribe-oracle-pre.log`).

## Gap battery — before side (receipts under `/tmp/mori-scribe-r7/before/`)

All runs at census `af2d4e79…`, `MORI_NOW_EPOCH` pinned; fixture roots are minimal temp
trees (no fleet paths). Full scripts/outputs: `/tmp/mori-scribe-r7/before/run-gaps.sh`,
`g1.out`, `g2.out`, `g4-receipt.txt`, `live-before.log`.

### GAP1 — tmux session relevance (r2 note §7, `:276-282`)

Fixture: a tmux stub printing 3 sessions — `fleet-mori-r7: 3 windows`,
`work-notes: 1 windows`, `scratch: 2 windows`.

```
SURFACE tmux: ok (cmd=<fx>/stub/tmux ls; sessions=3; ts=2026-10-15T19:24:28Z)
```

Session names visible in the output: 0 occurrences. Probe at `tools/mori-census.sh:883-898`
(line-count at `:896`, row at `:897`). Before: no relevance classification, no per-session
freshness, no names — count-only, proven.

### GAP2 — memory-pressure threshold (r2 note §4, `:202-214`)

Fixture: `memory.events` with `high 5000 / max 2000 / oom 0 / oom_kill 0`.

```
SURFACE cgroup: ok (… oom_kill=0 oom=0 high=5000 max=2000 current=refused:outside-sysfs-cgroup; ts=…)
```

No `FINDING` for cgroup pressure; findings in that run: `WATCHDOG_ABSENT` only (module the
fixture has no watchdog process). Probe reads `high`/`max` at `:444-445`, prints at `:466`,
has threshold logic for `oom_kill` only (`:459-464`). Before: printed-only, unmeasured
threshold — proven.

### GAP3 — disk write-rate (r2 note §5, `:216-235`)

```
diskstats-reads-in-census: 0        # grep -c 'diskstats' tools/mori-census.sh
diskstats-source-lines: 9           # wc -l < /proc/diskstats  (raw feed available, unread)
   8       0 sda 249 4 15364 8139 0 0 0 0 0 7353 8139 0 0 0 0 0 0
```

Disk probe is `df -P` point-in-time percent only (`:470-520`; thresholds `:506-512`).
Before: no rate, raw feed unread — proven.

### GAP4 — `state_rounds` count-only (r2 note §1, `:105-115`; defect 4 `:311-312`)

Two fixtures, same file count (2 rounds), different values:

```
-- fixture alpha: kagi.round=3 kama.round=5
SURFACE watchdog: drift (… state_rounds=2; ts=<pinned>)
-- fixture beta:  kagi.round=99 kama.round=100
SURFACE watchdog: drift (… state_rounds=2; ts=<pinned>)
-- diff after path/ts normalization: IDENTICAL (values 3/5 vs 99/100 unreadable from the row)
-- standalone value tokens '99'/'100' in beta output: 0
```

Count at `:233-241`, row at `:256-260`. Before: values never read — proven.

## After-side (measured at `c7c3569b…` / `448f7723…`, 19:42–19:52Z; SHA re-verified unchanged)

- **Battery** (`/tmp/mori-scribe-r7/after/summary.txt`, `battery-console.txt`): selftest
  `PASS (45 cases, 45 passed, 0 failed)` exit 0; oracle `matched=28 total=28` exit 0 ×2
  unpinned (seeds `3600785900` / `1106091929`) + pinned pair (seed 424242/nonce 777777)
  byte-identical, 3002 bytes, exit 0; live `DRIFT (findings=15 drift=14 unavailable=1
  surfaces=7)` exit 1. `census unchanged: yes`, `oracle unchanged: yes`.
- **Positive gap probes** (`after-probes.sh`; `after/g1b.out`, `g2b.out`, `g2c.out`,
  `g3b.out`, `g4c.out`):
  - tmux: `sessions=3; relevant=1 foreign=2 unclassified=0 rule=pane_cwd_under_fleet_root`
    + 2 × `TMUX_FOREIGN_SESSION info` (`work-notes`, `scratch`).
  - cgroup PSI: `psi_some_avg10=42.00` → `MEM_PRESSURE_HIGH warn … threshold_avg10=10
    threshold_label=local`; fill `mem_fill_pct=95 mem_fill_scope=cgroup` →
    `MEM_FILL_HIGH warn … threshold_pct=85 threshold_label=local`; host-ram
    `host_mem_avail_pct=5` → `MEM_AVAIL_LOW warn … floor_pct=10 threshold_label=local`.
  - disk: `io_avg_since_boot=dm-0:9696649Bps/11222s`; independent computation
    `sectors_written=212530864 × 512 ÷ uptime=11222 s = 9696649` — equal.
  - state: `state_rounds=3 state_rounds_max=9 state_lag=1 state_ahead=1 state_cmp=2
    state_val_unreadable=0` + `WATCHDOG_STATE_LAG` (kagi 5<7) + `WATCHDOG_STATE_AHEAD`
    (kama 9>4).
- **Negative gap probes** (battery g1/g2/g4a/g4b): degraded arms disclose
  `relevance=unavailable reason=no-pane-data` + `TMUX_RELEVANCE_UNAVAILABLE`;
  `psi_source=absent`; `DISK_IO_UNMEASURED` with `tmpfs:not-a-block-device`;
  state values visible (`state_rounds_max=5` vs `100` — distinguishable now).
- **Canary sweep on new read paths** (`/tmp/mori-scribe-r7/canary`; stderr captured
  separately and measured): unreadable diskstats → `dm-0:no-diskstats`; unreadable uptime →
  `dm-0:no-uptime`; garbage diskstats → `dm-0:device-not-in-diskstats`; non-integer field
  10 → `dm-0:counter-parse`; missing device → `device-not-in-diskstats`; mode-000 PSI →
  `psi_source=unreadable`; mode-000 `memory.max` → `mem_fill_scope=unavailable`. Every one:
  full verdict line, rc 1, **stderr_bytes=0** (8/8 measured).
- **Landed artifacts** at these bytes: note `corpus/knowledge/surfaces-r7.md` (249 lines);
  lesson `corpus/lessons/2026-10-15-free-lunch-measurements-counter-baselines.md`;
  receipts `corpus/evidence/surfaces-r7-20261015T1948Z-{selftest,oracle,live,tmux,memory,diskrate,staterounds}.log`;
  SKILL.md r7 rows; `corpus/README.md` r7 rows; `corpus/evidence/README.md` index rows
  (incl. the additive key-diff table); `corpus/knowledge/observability-surfaces-r2.md` r7
  updates landed (+65 lines). No lane artifact remains unlanded at ledger close.
- **Deferral datum** (from the diskrate receipt): 10 s sample pair = 715980 Bps vs the
  same clock's since-boot average 9549258 Bps, at +10 s gate cost (whole gate 3436 ms).
- **Note-recorded in-wave defect**: `[: max: integer expected` stderr at intermediate
  revisions (`619e0232…`/`75dd142d…`), fixed at final bytes (`:706-710`), selftest guard
  `:1518-1524`. Revision history `af2d4e79` → `619e0232` → `75dd142d` → `c7c3569b`.

## Ledger status

Drafts v3 (`scorecard-verdict-draft.md`, `log-entry-draft.md`, `report-draft.md`) are built
from the sections above. All lane-tool SHAs re-verified at ledger close.

## Landed r7 artifact notes (as observed)

- `corpus/lessons/2026-10-15-free-lunch-measurements-counter-baselines.md` (lessons-distiller,
  19:24–19:27Z at `af2d4e79…`/`3307761a…`): cost classification for the four gaps —
  tmux names + `state_rounds` values + PSI `avg10/60/300` + `memory.peak` are free
  (source-aggregated / same walk); disk write-rate is NOT free (no kernel file holds a
  rate; dwell ≥ window or persisted state — forbidden by read-only), free substitutes
  answer different questions (PSI io stall, diskstats magnitude); `memory.max` is `max`
  here so no percent-of-cap threshold is constructible without inventing a value;
  cumulative counters need their baseline printed (measured: a reboot flipped four rows
  at byte-identical SHA). Round-7 gap map states none of the four is closed at the
  pinned SHAs. This lesson predates the impls' landing — no claim about landed behavior.