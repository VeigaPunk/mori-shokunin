# mori round 7 — goal-wave report draft (scribe seat)

Integration target: the round report (idiom of `.ufo/reports/round-6/mori-goalwave.md`;
final path `[PARENT]`, likely `.ufo/reports/round-7/mori-goalwave.md`). Parent owns the
final path, the identity and the commit binding. Every figure is bound to a landed
artifact, a receipt, or a command run at a pinned SHA; `[PARENT: …]`/`[PENDING: …]` as
elsewhere.

- Status: `[PARENT: completion statement + verified-round-count claim 6 → 7]`
- Evidence commit: `[PARENT: wave integration commit hash under the mori identity]`
- Baseline: `80a80f6` (round-6 records; evidence `92b2e42`)
- Wave: `[PARENT: bind the wave record — batch shape, seat completion/loss counts, any backfill]`
- Report time: `[PARENT]`
- Draft status: **v3** by the scribe seat. Before-side at census `af2d4e79…` / oracle
  `3307761a…`, 19:23–19:25Z; after-side at census `c7c3569b…` (`VERSION=census-r4`, 2004
  lines) / oracle `448f7723…`, 19:42–19:52Z (SHA re-verified unchanged across every run).
  Scratch `/tmp/mori-scribe-r7/{before,after}/`.

## Work performed

- Selected axis **coverage** — the registered round-6 pivot (`SCORECARD.md:333-337`): close
  the four surface gaps measured in round 2 (`corpus/knowledge/observability-surfaces-r2.md`
  Gaps sections): tmux session relevance (§7), memory-pressure threshold (§4), disk
  write-rate (§5), `state_rounds` count-only (§1).
- Registered claim: before — all four gaps unmeasured (receipt-backed); after — each gap
  either implemented as a measured probe (selftest coverage, receipt-backed live rows,
  labeled-local thresholds, no new crash paths per the pipefail lesson, additive-only
  output) or an explicit bounded-deferral with a named precondition; the verdict machine
  stays green (selftest all-pass, oracle 28/28 exit 0 at the new pinned SHAs, re-baselined
  only for additive output, live census honest).

## Before → after measurements (scribe first-hand)

| Gap | Before at `af2d4e79…` (19:23–19:25Z) | After at `c7c3569b…` (19:42–19:52Z) |
|---|---|---|
| tmux relevance | 3-session stub → `sessions=3`; 0 session names in output; count-only | `sessions=3; relevant=1 foreign=2 unclassified=0 rule=pane_cwd_under_fleet_root` + 2 × `TMUX_FOREIGN_SESSION` info; no-pane-data arm → `relevance=unavailable` + `TMUX_RELEVANCE_UNAVAILABLE` info; live host had no tmux server → row `unavailable` (fixture-proved only) |
| memory pressure | `high=5000 max=2000` fixture → printed, no finding | PSI 42 → `MEM_PRESSURE_HIGH warn … threshold_avg10=10 threshold_label=local`; fill 95% vs numeric max → `MEM_FILL_HIGH`; host-ram 5% → `MEM_AVAIL_LOW`; `psi_source=ok/absent/unreadable`; `local_oom_kill=` on the row; live `psi_some_avg10=0.00 … mem_fill_scope=host-ram host_mem_avail_pct=65/66` |
| disk write-rate | `grep -c diskstats` = 0; df point-in-time only | `io_basis=since-boot io_avg_since_boot=dm-0:9696649Bps/11222s` (byte-matching an independent computation; live `dm-0:9714994Bps/11166s`, note `9615432Bps/11474s` — mutable), reasons in `io_avg_unavailable=`, `DISK_IO_UNMEASURED` info when unmeasurable; instantaneous rate a bounded deferral with named precondition (header `:44-52`) |
| `state_rounds` | values 3/5 vs 99/100 → byte-identical rows; values never read | values read: `state_rounds=3 state_rounds_max=9 state_lag=1 state_ahead=1 state_cmp=2` + `WATCHDOG_STATE_LAG`/`_AHEAD` info; live `state_rounds=21 state_rounds_max=18 state_lag=0 state_ahead=0 state_cmp=21` |
| verdict machine | selftest 30/30 exit 0; oracle 28/28 exit 0; live `DRIFT (15/14/1)` exit 1 | selftest `PASS (45 cases, 45 passed, 0 failed)` exit 0 (+15, zero removed); oracle 28/28 exit 0 ×2 seeds + pinned pair byte-identical; live `DRIFT (15/14/1)` exit 1 — same shape |

## Landed changes (evidence commit `[PARENT]`)

- `tools/mori-census.sh` → `c7c3569b…` (`VERSION=census-r4`; 2004 lines; +584/−18):
  tmux relevance (`:1242-1302`), PSI + fill/avail + defect-3 disclosure (`:649-753`),
  since-boot write average + disclosure (`:764-868`), state values + lag/ahead
  (`:390-451`), 15 new selftest cases (45 total), shell-diagnostic selftest guard
  (`:1518-1524`).
- `tools/mori-silence-cases.sh` → `448f7723…`: +8/−0 lines, fixture pins for
  `MORI_DISKSTATS`/`MORI_UPTIME`; registry 28 ids unchanged; no assertion change.
- `corpus/knowledge/surfaces-r7.md` (249 lines); lesson
  `corpus/lessons/2026-10-15-free-lunch-measurements-counter-baselines.md`; receipts
  `corpus/evidence/surfaces-r7-20261015T1948Z-{selftest,oracle,live,tmux,memory,diskrate,staterounds}.log`
  (indexed in `corpus/evidence/README.md`); SKILL.md r7 rows; `corpus/README.md` r7 rows
  (incl. named limits); `corpus/knowledge/observability-surfaces-r2.md` r7 updates landed
  (+65 lines across its four Gaps sections).

## Corrections and honest boundaries

1. **Instantaneous write rate is deferred, not implemented** — bounded deferral with the
   precondition named in the impl header (`:44-52`): measure the wall time a second sample
   adds and record it in the round note. The datum exists in the note §3 and the diskrate
   receipt: a 10 s
   sample pair read `sectors 219266952 → 219280936` (715980 Bps) against the same clock's
   since-boot average 9549258 Bps, at +10 s cost (whole gate 3436 ms) — the deferral
   stands as designed. The row's value is a since-boot AVERAGE, never an instantaneous
   rate; 85/95 remain unchanged, explicitly not recalibrated.
2. **tmux relevance is fixture-proved, not live-proved this round** — the host had no tmux
   server at every measurement clock (`tmux ls` rc 1); the live row stays the old
   `unavailable` shape. The classification rule (pane cwd under the fleet root) is a
   disclosed declaration; per-session freshness is unmeasured (note §1).
3. **The oracle's 8-line fixture pin** — required so the new disk row's live-varying uptime
   divisor cannot break case 28's two-shape invariance. Registry and assertions unchanged;
   disclosed in the diff itself (note: `CASE_IDS` diff empty).
4. **In-wave defect found and closed:** `[: max: integer expected` on stderr at intermediate
   revisions (`619e0232…`/`75dd142d…`); fixed at the final bytes by testing the literal
   `max` first (`:706-710`); the selftest now fails any case whose output contains a shell
   diagnostic — measured 0 B stderr at `c7c3569b…` live and both fixture arms (note
   §"Defects measured this round").
5. **Thresholds are local, not measured** — `MEM_PSI_WARN_AVG10=10`, `MEM_FILL_WARN_PCT=85`,
   `MEM_AVAIL_MIN_PCT=10` are declared placeholders for this host; on this host the
   slice's `memory.max` is `max`, so only the host-ram scope is live-observable.
6. **The since-boot average is not attributable to the fleet** — it counts all writes to the
   device (OS/desktop included) and cannot detect a burst (note §3).
7. **Revision history recorded** — the impl iterated mid-wave (`af2d4e79…` → `619e0232…` →
   `75dd142d…` → `c7c3569b…`); every acceptance figure above pins the FINAL bytes (note
   defect 2).

## SHONEN

- [ ] · [ ] · [ ] · [ ] — all four remain `[ ]`: no named non-author verifier; wave seats
  are the lane per protocol.

Boundaries held: detection and report only; no remediation/kills/config edits; the new
probes are read-only reads of `/proc/diskstats`, `/proc/uptime`, PSI files and
`tmux list-panes`; fixtures `/tmp`; seats made no commits; fleet root read-only for seats.
`[PARENT: confirm from the integration diff]`