# Round 7 verdict — integration draft (scribe seat, goal wave)

Integration target: append as a `## Round 7 verdict — 2026-10-15 (goal wave)` section in
`SCORECARD.md` (parent-owned; append-only — the round-6 section `SCORECARD.md:287-337` and
everything above it stay untouched). Verdict vocabulary only (`improved` / `harmed` /
`unchanged` / `unprovable-but-better`); no scalar scores. Every figure below is bound to a
landed artifact, a receipt, or a command run at a pinned SHA; `[PARENT: …]` marks values
only the integration commit or the parent's acceptance re-run can bind; `[PENDING: …]`
marks values unlanded at this draft's clock.

- Evidence commit: `[PARENT: wave integration commit hash under the mori identity]`
- Lane baseline entering the wave: `80a80f6` (round-6 records; evidence `92b2e42`).
- Round-count claim: `[PARENT: verified-round accounting 6 → 7 on admission]`
- Draft status: **v3 2026-10-15T19:56Z** by the scribe seat. Before-side measured
  first-hand at the frozen census `af2d4e79…` (`VERSION=census-r3`, 1438 lines) and oracle
  `3307761a…` (1082 lines), 19:23–19:25Z. After-side measured first-hand at the landed
  census `c7c3569b842ab3911cbfdf415eb7023766c950c60f354af95f6a4f020b5671af`
  (`VERSION=census-r4`, 2004 lines; +584/−18 vs `af2d4e79…` per `git diff --numstat`) and
  oracle `448f77238c73a5c929a898dad0f0c495fd2a66cc4b90a00ae84ede69a86beeb5`
  (registry 28 ids unchanged; the entire diff vs the frozen r6 bytes is **+8/−0 lines**),
  19:42–19:52Z; SHA re-verified unchanged across every battery. Landed note
  `corpus/knowledge/surfaces-r7.md` (249 lines; coverage authority) + lesson
  `corpus/lessons/2026-10-15-free-lunch-measurements-counter-baselines.md`; durable
  receipts `corpus/evidence/surfaces-r7-20261015T1948Z-{selftest,oracle,live,tmux,memory,diskrate,staterounds}.log`
  (indexed in `corpus/evidence/README.md`, incl. the additive `key=`-diff table);
  `corpus/README.md` r7 rows landed (incl. the named-limits section);
  `corpus/knowledge/observability-surfaces-r2.md` r7 updates landed in its four Gaps
  sections (+65 lines: state_rounds, memory-pressure, write-rate, relevance). Scratch:
  `/tmp/mori-scribe-r7/{before,after}/` (batteries `run-gaps.sh`, `run-after.sh`,
  `after-probes.sh`).

## Round 7 verdict

Round scope (registered round-6 pivot, `SCORECARD.md:333-337`; LOG round-6 entry): the
**coverage** pivot to the four surface gaps measured in round 2 —
`corpus/knowledge/observability-surfaces-r2.md` Gaps sections: (1) tmux session relevance
(§7 `:276-282`), (2) memory-pressure threshold (§4 `:202-214`), (3) disk write-rate (§5
`:216-235`), (4) `state_rounds` count-only (§1 `:105-115`, defect 4 `:311-312`).

Registered claim: before — all four gaps unmeasured, receipt-backed in the r2 note; after —
each gap is either **(a)** implemented as a measured probe with selftest coverage,
receipt-backed live rows, labeled-local thresholds, no new crash paths (the pipefail
lesson), additive-only output — or **(b)** an explicit bounded-deferral with a named
precondition recorded in the note; **AND** the verdict machine stays green: selftest
all-pass, oracle `28/28` exit 0 at the new pinned SHAs (re-baselined ONLY for additive
output, never for semantic change), live census honest.

**Before** (scribe first-hand, 19:23–19:25Z at `af2d4e79…` / `3307761a…`; fixtures `/tmp`
only; receipts `/tmp/mori-scribe-r7/before/`):

- **GAP1 tmux** — a 3-session stub (one fleet-named, two not) → `SURFACE tmux: ok (…
  sessions=3; …)`; session names visible in output: 0. Probe was a line count
  (`tools/mori-census.sh:896-897` at that SHA).
- **GAP2 cgroup** — fixture `high 5000 / max 2000` → `SURFACE cgroup: ok (… high=5000
  max=2000 …)` with no finding; fields read at `:444-445`, printed at `:466`; threshold
  logic existed for `oom_kill` only (`:459-464`).
- **GAP3 disk** — `grep -c 'diskstats' tools/mori-census.sh` → `0` while `/proc/diskstats`
  held 9 lines (raw feed available, unread); the probe was `df -P` point-in-time percent
  only (`:470-520`).
- **GAP4 `state_rounds`** — two fixtures, same round-file count (2), different values
  (3/5 vs 99/100): byte-identical watchdog rows after path/ts normalization; 0 standalone
  value tokens in the output (`g4-receipt.txt`). Count at `:233-241`, row at `:256-260`.
- **Verdict machine beside the gaps** — selftest `PASS (30 cases, 30 passed, 0 failed)`
  exit 0; oracle `matched=28 total=28` exit 0; live census
  `MORI_CENSUS: DRIFT (findings=15 drift=14 unavailable=1 surfaces=7)` exit 1.

**After** at the landed SHAs (`c7c3569b…` / `448f7723…`; SHA verified unchanged through
every run; note + receipts at the same SHAs):

- **GAP1 tmux — implemented.** Stub with pane data: `SURFACE tmux: ok (… sessions=3;
  relevant=1 foreign=2 unclassified=0 rule=pane_cwd_under_fleet_root; …)` plus two
  `FINDING TMUX_FOREIGN_SESSION severity=info` lines naming `work-notes` and `scratch`;
  rule is pane-current-path under the fleet root (`:1242-1302`; foreign emit `:1286`).
  Degraded arm (stub answers `ls` only): `relevance=unavailable reason=no-pane-data` +
  `FINDING TMUX_RELEVANCE_UNAVAILABLE info … unnoticed_but_counted` (`:1298`) — counted,
  not implied-classified. Three selftest cases. **Boundary (note §1):** the host had **no
  tmux server** in this round (`tmux ls` rc 1; live row `unavailable`), so relevance
  classification is fixture/selftest-proved, not live-proved; per-session freshness remains
  unmeasured (r7 claimed relevance only).
- **GAP2 memory pressure — implemented.** PSI: fixture `some avg10=42.00` →
  `FINDING MEM_PRESSURE_HIGH warn psi_some_avg10=42.00 threshold_avg10=10
  threshold_label=local` (`:680`); a just-under fixture stays clean (selftest). Fill:
  numeric `memory.max` 1000000000 + current 950000000 → `mem_fill_pct=95
  mem_fill_scope=cgroup` + `FINDING MEM_FILL_HIGH warn … threshold_pct=85
  threshold_label=local` (`:727`); unlimited `max` → host scope with
  `host_mem_avail_pct=5` → `FINDING MEM_AVAIL_LOW warn … floor_pct=10
  threshold_label=local` (`:717`). Row carries `local_oom_kill=` (the r2 note's defect-3
  disclosure) and tri-state `psi_source=ok|absent|unreadable` (unreadable canary →
  `psi_source=unreadable`; unreadable `memory.max` → `mem_fill_scope=unavailable`). Five
  selftest cases. Defaults declared LOCAL placeholders at `:167-175`
  (`MEM_PSI_WARN_AVG10=10`, `MEM_FILL_WARN_PCT=85`, `MEM_AVAIL_MIN_PCT=10`); on this host
  the slice's `memory.max` is `max`, so only the host-ram scope is live-observable (live:
  `psi_some_avg10=0.00 … mem_fill_scope=host-ram host_mem_avail_pct=65/66`). Note §2
  boundary: these are the only new findings that **do** flip the roll (warn), unlike the
  state-value findings.
- **GAP3 disk — implemented as a since-boot average; the instantaneous rate is a bounded
  deferral.** Live rows: `io_basis=since-boot io_avg_since_boot=dm-0:9714994Bps/11166s
  io_avg_unavailable=tmpfs:not-a-block-device` (this seat) and `dm-0:9615432Bps/11474s`
  (note, 19:48:56Z — mutable clocks); the fixture run gave `dm-0:9696649Bps/11222s`, and
  this seat's independent computation from the raw sources (`sectors_written=212530864` ×
  512 ÷ `uptime=11222 s`) yielded the **same byte value**. Non-block-device targets
  disclose `not-a-block-device` and never 0 B/s; `FINDING DISK_IO_UNMEASURED info …
  basis=since-boot` (`:860`) when nothing was measured. Canaries (pipefail lesson applied
  to the new read paths): unreadable `MORI_DISKSTATS` → `dm-0:no-diskstats`; unreadable
  `MORI_UPTIME` → `dm-0:no-uptime`; garbage/no-device diskstats →
  `dm-0:device-not-in-diskstats`; non-integer field 10 → `dm-0:counter-parse` — every
  canary produced a full verdict line, graded rc, 0 stderr bytes. Three selftest cases.
  **Deferral (note §3):** the instantaneous (two-sample) write rate is NOT implemented;
  precondition named in the impl header (`:44-52`): measure the wall time a second sample
  adds and record it in the round note. The precondition datum was measured in-wave and
  recorded in the note §3 and `…-diskrate.log`: a 10 s sample pair read `sectors 219266952
  → 219280936` (= 715980 Bps) against the same clock's since-boot average 9549258 Bps, at
  +10 s cost (whole gate 3436 ms) — the deferral stands as designed (no interval added to
  the gate).
  85/95 kept unchanged — the r2 note's "measured write rate" precondition is met by the
  average, but the SKILL r7 text and the note both state it is not a licence to
  recalibrate. Note §3 boundary: the average counts every write to the device since boot
  (OS/desktop included) and cannot detect a burst.
- **GAP4 `state_rounds` — implemented.** Fixture: `kagi.round=5` vs ledger launch round 7;
  `kama.round=9` vs 4; `mori.round=3` with no ledger line → row `state_rounds=3
  state_rounds_max=9 state_lag=1 state_ahead=1 state_cmp=2 state_val_unreadable=0`, plus
  `FINDING WATCHDOG_STATE_LAG info lane=kagi state_round=5 ledger_round=7` (`:421`) and
  `FINDING WATCHDOG_STATE_AHEAD info lane=kama state_round=9 ledger_round=4` (`:424`).
  Every value is compared with the lane's last `launch <lane> round=N` ledger line; both
  findings are info and never flip the roll (gap closed is invisibility, not severity).
  Unreadable values counted (`state_val_unreadable`; selftest case). Live row:
  `state_rounds=21 state_rounds_max=18 state_lag=0 state_ahead=0 state_cmp=21
  state_val_unreadable=0` — 21/21 compared (note §4).
- **Verdict machine green; additivity contract held.** selftest `PASS (45 cases, 45 passed,
  0 failed)` exit 0 — exactly **+15 cases vs r6, zero removed** (set diff of the receipt
  case lists) — receipt `…-selftest.log` + this seat's battery. Oracle `matched=28 total=28`
  exit 0 ×2 unpinned at different seeds (this seat `3600785900`/`1106091929`; receipt run1
  `796022666`; note `3979393213`/`2472526516`) + pinned pair byte-identical (3002 bytes);
  receipt `…-oracle.log` (`ORDER_IDENTICAL_WHEN_SEED_PINNED=yes`). Live census
  `MORI_CENSUS: DRIFT (findings=15 drift=14 unavailable=1 surfaces=7)` exit 1 — **identical
  shape to before**. The frozen registry (28 ids, want-sets) is unchanged; the entire oracle
  diff vs `3307761a…` is **+8/−0 lines** — fixture pins `MORI_DISKSTATS`/`MORI_UPTIME`
  (case 28's two-shape invariance would otherwise break on the ticking uptime divisor). No
  assertion changed. Additive-only output proved field-by-field (note): watchdog +5,
  cgroup +8, disk +3, tmux +4 new field names; waves/journal/silence field sets unchanged.

| axis | verdict | before → after evidence |
|---|---|---|
| coverage | **improved** *(selected axis)* | Before: all four gaps unmeasured (bullets above; r2 note). After: all four closed — tmux relevance (fixture-proved; live unavailable for lack of a server), PSI + fill/avail grading, since-boot write average per device, `state_rounds` values with lag/ahead. Selftest +15 cases (30→45), zero removed. One half-gap (instantaneous write rate) is a bounded deferral with the precondition in the header. Live shape unchanged (15/14/1). |
| operability | **improved** | selftest 30→45 exit 0 at `c7c3569b…`; oracle `28/28` exit 0 ×3 independent seed sets + pinned byte-identical at `448f7723…`; live runs to a full verdict. New read paths canaried: five diskstats/uptime failure shapes, unreadable PSI, unreadable `memory.max`, unreadable round value — every canary yields a verdict line, 0 stderr. The in-wave stderr defect (`[: max: integer expected`, intermediate revisions) was found and closed at the final bytes, and the selftest gained a shell-diagnostic guard (`:1518-1524`) so the class cannot return silently. |
| depth | **improved** | `corpus/knowledge/surfaces-r7.md` (249 lines: per-gap probe design at file:line, fixture receipts, limitations, defect log, additive field-set proof) + lesson `corpus/lessons/2026-10-15-free-lunch-measurements-counter-baselines.md` (source-aggregated vs dwell cost classification; the baseline seam measured across a reboot — four rows flipped at a byte-identical SHA); census header carries the per-gap dispositions + deferral precondition (`:36-70`); SKILL.md r7 rows. |
| freshness | **improved narrowly** | seven dated, hash-pinned receipts at `c7c3569b…`/`448f7723…` (`surfaces-r7-20261015T1948Z-{selftest,oracle,live,tmux,memory,diskrate,staterounds}.log`), indexed in `corpus/evidence/README.md` with the additive key-diff table; SHA re-verified before/after every battery; `corpus/README.md` r7 rows landed. Frozen-behavioral drift pin still absent — carried debt. |
| calibration | **improved** | Every new threshold labeled local on the row and in the finding (`threshold_label=local`); defaults block declares them placeholders, not host-measured (`:167-175`); tri-state `psi_source` proven by canaries; unmeasurable devices disclose reasons, never 0 B/s; state lag/ahead stay info while the memory warnings flip the roll — the difference is stated (note §2); the deferral is bounded with a named precondition; 85/95 kept. |
| adjacency | **unchanged** | Detection/report only; new reads are read-only (`/proc/diskstats`, `/proc/uptime`, PSI `memory.pressure`, `memory.max`, `tmux list-panes -a`); no remediation/kill/systemctl/host-config content; fixtures `/tmp`; fleet root read-only for seats. `[PARENT: confirm from the integration diff]` |

Admission: `[PARENT: bind the admission and round-count at integration. Expected disposition
on the evidence above: **ADMIT** — the four registered gaps are closed (three implemented
outright; the fourth implemented as a since-boot average with an explicitly bounded
deferral for the instantaneous rate, precondition named), the verdict machine is green with
the additivity contract held (oracle +8/−0 fixture-pin lines, registry unchanged; live
census same shape), and five axes improved. The one honest scope limit — tmux relevance is
fixture-proved, not live-proved this round (no tmux server) — is named, not hidden.]` No
scalar score.

Learning trends (lane idiom):

| Trend | Verdict | Evidence |
|---|---|---|
| expansion | **improved** | `surfaces-r7.md` + lesson `2026-10-15-free-lunch-measurements-counter-baselines.md`; SKILL.md r7 rows (question/answer + threshold/row-field bullets); seven receipts indexed in `corpus/evidence/README.md`; `corpus/README.md` r7 rows. |
| quality | **improved** | Multi-seat independent measurement (impl selftest/oracle receipts; note-writer battery; receipts-writer's five legs; this seat's battery, four positive gap probes and canary sweep); the disk rate independently corroborated byte-exact; the in-wave stderr defect found, closed and guarded; mid-wave revision history recorded (note defect 2); the sub-question deferral named rather than faked. |
| discernment | **unchanged** | No outside spot-check of an admit/reject exists — the wave's seats are the lane per protocol. `[PARENT: bind]` |

Named debt for round 8 (from the landed note/lesson; carried items unchanged):

1. **Instantaneous write rate** — bounded deferral; precondition: measure the wall time a
   second sample adds and record it in the round note (`tools/mori-census.sh:44-52`). The
   datum is measured and recorded (note §3 + `…-diskrate.log`: 10 s pair = 715980 Bps vs
   9549258 Bps since-boot, +10 s gate cost); the deferral stands until an operator lifts it.
2. **tmux per-session freshness** — r7 claimed relevance only; no `session_activity`
   per-session probe exists (note §1 limitation b), and relevance has no live observation
   this round (no server).
3. Carried: frozen-behavioral drift pin (`silence-cutover-r3.md:253-254`); row-6
   report-body presence-only residual (`silence-cutover-r3.md:250-252`); blocked-attempt
   receipt-binding and role-routing debts (`SCORECARD.md:128-131`); memory thresholds need
   recalibration by any operator reusing the gate elsewhere (labeled local).

`[PARENT: bind the integration commit and round-count; re-run `bash tools/mori-census.sh
--selftest` (expect 45/45 exit 0), `bash tools/mori-silence-cases.sh` (expect 28/28 exit 0;
≥2 seeds; pinned pair byte-identical), the live census (expect the `DRIFT (findings=15
drift=14 unavailable=1 surfaces=7)` shape — mutable), and the gap probes (recipes: this
seat's `/tmp/mori-scribe-r7/{run-after.sh,after-probes.sh}`; note `surfaces-r7.md`
recheck block; receipts `corpus/evidence/surfaces-r7-20261015T1948Z-*.log`).]`