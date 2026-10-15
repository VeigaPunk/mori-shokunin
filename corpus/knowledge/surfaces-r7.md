# Surface gaps r7 — the four `observability-surfaces-r2.md` gaps closed or deferred

source: `tools/mori-census.sh` sha256
`c7c3569b842ab3911cbfdf415eb7023766c950c60f354af95f6a4f020b5671af`
(`VERSION=census-r4`, 2004 lines); oracle `tools/mori-silence-cases.sh` sha256
`448f77238c73a5c929a898dad0f0c495fd2a66cc4b90a00ae84ede69a86beeb5`.
verified-at: 2026-10-15T19:47–19:52Z — note-writer battery (`--selftest`, oracle ×2,
live census, both memory arms of a pinned temp fixture, old-vs-new field-set diff), plus
the durable receipts
`corpus/evidence/surfaces-r7-20261015T1948Z-{selftest,oracle,tmux,memory,diskrate,live}.log`.
recheck: `bash tools/mori-census.sh --selftest` (hermetic, /tmp only) ·
`bash tools/mori-silence-cases.sh` (28 cases, exit 0 iff all pass) ·
`bash tools/mori-census.sh` (live, writes nothing, exit 0 CLEAN | 1 DRIFT | 2 setup).
scope: detection and report only (`PROVINCE.md:16-18`); nothing here remediates. All r7
thresholds are **local placeholders**, labeled `threshold_label=local` on every row and
finding that carries one (`tools/mori-census.sh:167-175`).

This note is the r7 closure of the four Gaps sections in
`corpus/knowledge/observability-surfaces-r2.md` (tmux §7 `:276-282`, cgroup §4 `:202-214`,
disk §5 `:226-235`, watchdog §1 `:105-115` + defect 4 `:311-312`). Before-side measurements
are receipt-backed in `.ufo/round-7/goal-wave/measurements-ledger.md` (scribe, 19:23–19:29Z);
this note carries the after side. The r2 note's own sections are updated by its owner seat,
not here.

## Verdict summary — one line per gap

| # | r2 gap | r7 status | probe (impl) | hermetic proof (selftest cases) | live/fixture row |
|---|---|---|---|---|---|
| 1 | tmux session relevance | **implemented** | `probe_tmux` pane-cwd classification `:1242-1302`, rule `pane_cwd_under_fleet_root` | 3 cases `:1861`, `:1871`, `:1880` | fixture `sessions=2 relevant=1 foreign=1 unclassified=0`; live `tmux ls` rc 1 → relevance unavailable (see §1 limitation) |
| 2 | memory-pressure threshold | **implemented** (thresholds local) | PSI `some`/`full` avg10 `:656-682`; fill current/max or host-ram floor `:690-731` | 5 cases `:1888`, `:1895`, `:1903`, `:1910`, `:1917` | live `psi_some_avg10=0.00 … mem_fill_scope=host-ram host_mem_avail_pct=66`; fixture both arms (§2) |
| 3 | disk write-rate | **implemented as since-boot average** + **bounded deferral** of the instantaneous rate (precondition named `:48-52`) | `dev_of`/`io_of` `:764-787`, probe `:789-868` | 3 cases `:1927`, `:1933`, `:1940` | live `io_avg_since_boot=dm-0:9615432Bps/11474s io_avg_unavailable=tmpfs:not-a-block-device` |
| 4 | `state_rounds` count-only | **implemented** | value loop `:390-427`, row `:445`, `LAG`/`AHEAD` info `:421`/`:424` | 4 cases `:1951`, `:1959`, `:1967`, `:1973` | live `state_rounds=21 state_rounds_max=18 state_lag=0 state_ahead=0 state_cmp=21 state_val_unreadable=0` |

No gap was left untouched; one half-gap (instantaneous write rate) is an explicit
bounded deferral with its precondition written into the impl header, per the round's
either/or rule.

## 1. tmux — session relevance (r2 §7 gap: count-only, no names, no relevance test)

**Probe design.** After the existing `tmux ls` count (`:1254-1256`, unchanged row shape
when classification fails), `probe_tmux` runs `tmux list-panes -a -F
'#{session_name}\t#{pane_current_path}'` (`:1258-1260`). Each tab-separated pane line maps its
session to `fleet` iff the pane's current path is `$TMUX_SCOPE_ROOT` (default `$ROOT`,
`:156`) or under it; any pane outside marks the session `foreign` unless another pane
already marked it fleet (`:1282-1290`). Every foreign session emits
`TMUX_FOREIGN_SESSION` info **naming the session** (`:1286`); the row carries
`sessions=N relevant=F foreign=X unclassified=U rule=pane_cwd_under_fleet_root` (`:1301`).
Non-tab output (a stub `tmux ls` table, truncated line) is not guessed at (`:1266-1270`);
no pane data or a failed pane probe yields `relevance=unavailable reason=…` plus
`TMUX_RELEVANCE_UNAVAILABLE` info while the count survives (`:1299`).

**My fixture receipt** (note-writer, pinned `MORI_NOW_EPOCH`, temp tree; stdout saved to
`/tmp/mori-r7-note/final/gaps-maxarm.out`):

```
SURFACE tmux: ok (cmd=/tmp/mori-r7-note/bin/tmux ls; sessions=2; relevant=1 foreign=1 unclassified=0 rule=pane_cwd_under_fleet_root; ts=2026-10-15T04:50:57Z)
FINDING TMUX_FOREIGN_SESSION severity=info obs=session=scratch relevance=foreign rule=pane_cwd_under_fleet_root scope_root=/tmp/mori-r7-note/fx/root ts=… script_sha256=c7c3569b842a…
```

**Rule boundary, disclosed by the impl itself** (`:31-33`): a session whose panes all sit
outside the fleet root is classified foreign even if its process tree works on fleet files.
That is a deliberate rule, not a measured causal link: the probe reads pane cwd, never
`/proc/<pid>/environ` (r1 `:220-221` forbids it).

**Limitations.** (a) The host had **no tmux server** during this round
(`tmux ls` → `error connecting to /tmp/tmux-1000/default (No such file or directory)`,
rc 1, socket dir empty; live row `SURFACE tmux: unavailable (cmd=tmux ls; rc=1; …)`), so
relevance classification is fixture-proved today, not live-proved. (b) Per-session
freshness remains unmeasured — r7 classified relevance only; fleet sessions are counted
and foreign ones named, but no session is individually listed with `session_activity`.

## 2. cgroup — memory pressure (r2 §4 gap: "printed only; no threshold exists and none is measured here")

**Probe design.** PSI: `memory.pressure` (`:145`) is read with `cap` and the `some`/`full`
`avg10` values pass a shape gate (`is_decimal`, `:273`; `psi_avg10`, `:288`) before
printing, so an operator-pinned path cannot leak arbitrary bytes into the row
(`:656-674`). `some` avg10 integer part ≥ `MORI_MEM_PSI_WARN_AVG10` (default 10, `:173`) →
`MEM_PRESSURE_HIGH` warn (`:680`) and the surface drifts. Fill: `memory.max` (`:146`) is
accepted only as the literal `max` or digits (`:698-703`); with a numeric limit and a
numeric `memory.current` the row carries `mem_fill_pct` (`:748`) graded at
`MORI_MEM_FILL_WARN_PCT` (default 85, `:174`) → `MEM_FILL_HIGH` warn (`:727`). When the
limit is the literal `max` (unlimited — this host's user slice), the grade moves to the
host's own `MemAvailable/MemTotal` ratio with the scope **named on the row**
(`mem_fill_scope=host-ram host_mem_avail_pct=…`, `:750`) against
`MORI_MEM_AVAIL_MIN_PCT` (default 10, `:175`) → `MEM_AVAIL_LOW` warn (`:717`); a missing
MemInfo pair yields `mem_fill_scope=unavailable` (`:752`) rather than a silent pass.

The r2 note's defect 3 disclosure is also closed in the same row: the bare `oom_kill=` is
still the parent cumulative counter, and the session-service reading is printed next to it
as `local_oom_kill=` (`:754`), no longer only inside finding text.

**Live rows (two clocks, same shape).**

```
19:34:15Z … current=24777338880; local_oom_kill=0 psi_some_avg10=0.00 psi_full_avg10=0.00 psi_source=ok psi_warn_avg10=10 mem_fill_pct=unavailable mem_fill_scope=host-ram host_mem_avail_pct=69
19:48:56Z … current=17736376320; local_oom_kill=0 psi_some_avg10=0.00 psi_full_avg10=0.00 psi_source=ok psi_warn_avg10=10 mem_fill_pct=unavailable mem_fill_scope=host-ram host_mem_avail_pct=66
```

**My fixture receipt, both arms** (`/tmp/mori-r7-note/final/gaps-{maxarm,numarm}.out`;
same fixture, only `memory.max` differs):

```
max arm:  … psi_some_avg10=42.00 psi_full_avg10=20.00 psi_source=ok psi_warn_avg10=10 mem_fill_pct=unavailable mem_fill_scope=host-ram host_mem_avail_pct=6
          FINDING MEM_PRESSURE_HIGH … psi_some_avg10=42.00 threshold_avg10=10 threshold_label=local
          FINDING MEM_AVAIL_LOW … scope=host-ram host_mem_avail_pct=6 floor_pct=10 threshold_label=local
num arm:  … mem_fill_pct=90 mem_fill_scope=cgroup
          FINDING MEM_FILL_HIGH … scope=cgroup mem_fill_pct=90 threshold_pct=85 threshold_label=local current=900000 limit=1000000
```

**Limitations.** The three thresholds are **local placeholders, deliberately not derived
from a measurement of this host** — the impl states the rule (`:167-172`): the numbers
exist so the gap stops being unmeasured, and must be recalibrated by any operator reusing
the gate elsewhere. `MEM_PRESSURE_HIGH`/`MEM_FILL_HIGH`/`MEM_AVAIL_LOW` are `warn`, i.e.
they **do** flip the roll, unlike the r7 watchdog value findings — a local placeholder can
therefore produce DRIFT at a host someone calibrated differently. On this host `memory.max`
is `max`, so the closed-container ratio never exists here and only the host-ram scope is
live-observable. The fixture arms are hermetic proofs of the arithmetic/direction, not a
measurement of the fleet's own memory-pressure distribution.

## 3. disk — write rate (r2 §5 gap: "df is point-in-time; no write-rate evidence exists")

**Probe design.** `MORI_DISKSTATS` (`:147`) and `MORI_UPTIME` (`:148`) feed a
**since-boot average**: `dev_of` maps each `df` source (`/dev/mapper/root`) through
`readlink -f` to the diskstats name (`dm-0`) (`:764-769`); `io_of` finds the device's line
and computes `sectors_written × 512 / uptime_s` (`:771-787`, field 10 = sectors written).
The divisor travels **with** the value (`io_avg_since_boot=dm-0:9615432Bps/11474s`) so a
standalone numeric field cannot drift away from its basis (`:44-48`). Non-block-device
targets (tmpfs `/tmp`) get a reason, never a fake zero: `io_avg_unavailable=tmpfs:not-a-block-device`;
missing device / missing uptime / absent diskstats each yield `unavailable:<reason>`. If
no target device yields a rate, `DISK_IO_UNMEASURED` info discloses it (`:860`). The row
keeps `warn_pct=85 crit_pct=95` unchanged (`:866`) — the r2 note's rule was "do not install
a 'better' number without a measured write rate"; the impl measured a rate but changed no
threshold.

**My fixture receipt** (`/tmp/mori-r7-note/final/gaps-maxarm.out`): uptime 500 s, 20000
sectors written → `io_basis=since-boot io_avg_since_boot=fake0:20480Bps/500s
io_avg_unavailable=none` — the arithmetic is exact (20000×512/500), and the selftest case
`:1927` asserts the same string, so a wrong divisor or wrong field fails the suite.

**Bounded deferral (explicit).** The **instantaneous** write rate (two-sample delta) is
NOT implemented; the impl header `:49-52` names the precondition to lift it: *measure the
wall-time a second sample adds and record it in the round note*. Rationale recorded at
`:761-763`: no sampling interval was added to census runtime, so the only rate derivable
from per-boot counters is the average. **The precondition's datum now exists**: the r7
diskrate receipt measured a two-sample pair on dm-0 (13984 sectors over 10 s →
715980 Bps), the whole gate's wall time at 3436 ms, and — measured, not assumed — that a
10 s idle window on this host yields tiny/zero deltas, i.e. an in-census instantaneous
rate would be noisy *and* cost the interval
(`corpus/evidence/surfaces-r7-20261015T1948Z-diskrate.log:16-18`). The in-census
two-sample probe therefore stays deferred, now on measured grounds, until an operator
accepts that runtime cost.

**Limitations.** The average is **not attributable to the fleet**: it counts every write
to that device since boot, OS and desktop included (`dm-0` on this host is the btrfs
system+home device, `9615432Bps/11474s` = ~9.6 MB/s average). It says nothing about
per-process or per-lane write behavior, and it cannot detect a burst (an instantaneous
trap). `/tmp` is tmpfs here, so the second default target structurally has no rate.

## 4. watchdog — `state_rounds` values (r2 §1 gap + defect 4: "counts files, never values")

**Probe design.** The `.ufo/state/*.round` walk (`:389-397`) is unchanged and still
rc-gated (r4 fix), but the file list is copied before any further `cap` call — the impl
records the measured reason: `load_ledger` (`:297`) overwrites `CAP_OUT`, and reading the
state list out of `CAP_OUT` after it iterated the ledger instead of the files (`:396-399`).
For each file, `read_file`-gated values (`:407`); a non-integer value counts into
`state_val_unreadable` instead of silently becoming zero (`:410-413`); the maximum is
reported; and each value is compared with the lane's last `launch <lane> round=N` ledger
line (`ledger_last_launch_round`, `:309`) — the state file the watchdog itself writes in
the same tick as that line (`scripts/shokunin-watchdog.sh:80-81`). Below → `WATCHDOG_STATE_LAG`
info (`:421`); above → `WATCHDOG_STATE_AHEAD` info (`:424`). Both are **info and never
flip the roll** by design (`:386-389`): an inconsistent state file is evidence, not proof
of fleet ill health. The row adds `state_rounds_max state_lag state_ahead state_cmp
state_val_unreadable` (`:445`).

**Live row** (19:48:56Z): `state_rounds=21 state_rounds_max=18 state_lag=0 state_ahead=0
state_cmp=21 state_val_unreadable=0` — all 21 files read, all compared, values 1–18, none
lagging or ahead of the ledger at that clock.

**My fixture receipt** (`gaps-maxarm.out`): `state_rounds=2 state_rounds_max=9 state_lag=1
state_ahead=1 state_cmp=2 state_val_unreadable=0` with `FINDING WATCHDOG_STATE_LAG … lane=kagi
state_round=3 ledger_round=5` and `FINDING WATCHDOG_STATE_AHEAD … lane=kama state_round=9
ledger_round=5`, verdict `CLEAN`-compatible for the surface's own state (the drift in that
fixture run comes from the unrelated `WATCHDOG_ABSENT`). The four selftest cases cover both
directions, the matching case, and an unreadable value file.

**Limitations.** Comparison is per-lane and requires a matching ledger launch line: a lane
with no such line is counted (`state_rounds`) but not compared, so `state_cmp` may be
smaller than `state_rounds` (not the case live today: 21/21). The ledger's "last matching
line in file order wins" semantics (r2 cutover) apply unchanged.

## Verdict machine — green at the new pinned pair (additive-only re-pin)

| Check | Result (verbatim tail) | Exit |
|---|---|---|
| `bash tools/mori-census.sh --selftest` | `MORI_CENSUS_SELFTEST: PASS (45 cases, 45 passed, 0 failed)` (was 30) | 0, stderr 0 B |
| `bash tools/mori-silence-cases.sh` ×2 (seeds 3979393213 / 2472526516) | `MORI_SILENCE_CASES: matched=28 total=28` both | 0, stderr 0 B |
| grade tuples, run1 vs run2 sorted | identical across shuffled orders (26 state tuples + the 2 check-style cases) | — |
| `bash tools/mori-census.sh` live | `MORI_CENSUS: DRIFT (findings=15 drift=14 unavailable=1 surfaces=7)` | 1, stderr 0 B |

Durable receipts (receipts-writer), all at `CENSUS_SHA256_BEFORE=AFTER=c7c3569b…`:
`corpus/evidence/surfaces-r7-20261015T1948Z-{selftest,oracle,tmux,memory,diskrate,live}.log`
— selftest (`EXIT_CODE=0`), oracle
(`RUN1_TALLY=MORI_SILENCE_CASES: matched=28 total=28 (exit 0)`,
`ORDER_IDENTICAL_WHEN_SEED_PINNED=yes`), tmux (live `rc=1` unavailable + stub fleet/rc2
arms), memory (live + PSI 99/9.99 arms + fill arms incl. `mem_fill_pct=26` under
threshold), diskrate (live ×2 + fixture + missing-device arm + the two-sample datum cited
in §3), live (new bytes ×2 + the r6 census from `git HEAD` ×1 on the same clock — the
additive-only comparison). My own logs:
`/tmp/mori-r7-note/final/{shas,selftest.out,oracle-1.out,oracle-2.out,live.out,gaps-maxarm.out,gaps-numarm.out}.txt|out`
(ephemeral; the durable set is the receipts above).

**Oracle re-pin is exactly 8 inserted lines, 0 deletions** (`tools/mori-silence-cases.sh`,
`3307761a…` → `448f7723…`): the case skeleton now writes `CASE_STUB/uptime` and an empty
`diskstats` (`:340-345`) and the census env pins `MORI_UPTIME`/`MORI_DISKSTATS` to them
(`:477-478`), because an unpinned live uptime ticks inside the new disk row between runs
and would break the shape-invariance case. `CASE_IDS` diff vs HEAD is empty — the 28 ids
and their want-sets are byte-identical; no grade was re-baselined for a semantic change.

**Additive-only output, proved twice.** With one identical temp fixture and on live rows,
every field name the r6 census emitted is still present; only new names were added —
watchdog +5 (`state_rounds_max state_lag state_ahead state_cmp state_val_unreadable`),
cgroup +8 (`local_oom_kill psi_some_avg10 psi_full_avg10 psi_source psi_warn_avg10
mem_fill_pct mem_fill_scope host_mem_avail_pct`), disk +3 (`io_basis io_avg_since_boot
io_avg_unavailable`), tmux +4 (`relevant foreign unclassified rule`); waves/journal/silence
field sets unchanged (`diff` of sorted field-name sets, old bytes `af2d4e79…` vs new,
both fixture and live; logs in `/tmp/mori-r7-note/final/`). The tmux row on the live host
stays the old unavailable shape because `tmux ls` fails — the additive fields appear only
when classification succeeds.

## Defects measured this round

1. **Closed in-wave:** `[: max: integer expected` on stderr, from the cgroup fill test
   ordering — measured live at intermediate revisions `619e0232…`/`75dd142d…`
   (`tools/mori-census.sh:705` then): `[ max -gt 0 ]` is a bash arithmetic-argument error,
   printed to stderr while the `elif` still produced the correct host-ram answer. Fixed at
   the final bytes by testing the literal `max` **first** (`:705-710`) with the measurement
   recorded in the comment; verified: 0 B stderr in the live census and in both fixture
   arms at `c7c3569b…`. The selftest harness also gained a guard that fails any case whose
   census output contains a shell diagnostic (`:1518-1524`), so this class cannot return
   silently — the trap the r3 pipefail lesson named (verdict machinery hiding read errors)
   has a second, cheaper detector now.
2. **Not a defect, worth recording:** the impl iterated mid-wave
   (`af2d4e79…` → `619e0232…` → `75dd142d…` → `c7c3569b…`); the admission battery above
   pins the **final** bytes only. The defect in (1) was found at an intermediate revision
   and does not exist at the pinned one.

## What this note does not claim

- No remediation, no kill/restart, no systemctl, no host config change; every live row is
  read-only and pinned to one mutable clock.
- The three r7 memory numbers and the deferred instantaneous disk rate are **not** measured
  properties of this host; they are labeled-local placeholders. 85/95 disk percentages are
  still the r1 proposal pair, unchanged.
- No live tmux relevance observation exists for this round (no tmux server at either
  measurement clock); that gap's after-side is hermetic (selftest + my fixture) only.
- No claim that the since-boot write average is attributable to the fleet, and no claim
  that a per-session freshness/duration probe exists (it does not; the r7 claim was
  relevance).
- The r2 note's own Gaps sections and the round-1 files' six-vs-seven surface framing are
  owned by other seats; this note only points at them.