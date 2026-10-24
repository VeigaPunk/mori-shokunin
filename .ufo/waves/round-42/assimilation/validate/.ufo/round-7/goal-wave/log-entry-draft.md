# Round 7 log-entry draft (scribe seat, goal wave)

Integration target: append as a `## Round 7 — … (goal wave)` entry at the end of `LOG.md`
(parent-owned; append-only — nothing above the new section changes). `[PARENT: …]` marks
what only the integration commit/acceptance can bind; `[PENDING: …]` marks values unlanded
at this draft's clock (v3, 2026-10-15T19:56Z).

---

## Round 7 — coverage pivot: the four round-2 surface gaps closed (goal wave)

**Round 7 — goal-wave admission (2026-10-15).** Motivating evidence: the round-6
admission's registered pivot (`SCORECARD.md:333-337`; LOG round-6 entry) — with the verdict
machine complete (oracle `3307761a…` 28/28 exit 0, census `af2d4e79…` selftest 30/30),
round 7 turns to **coverage**: the four surface gaps measured in round 2
(`corpus/knowledge/observability-surfaces-r2.md` Gaps sections) — (1) tmux session
relevance, (2) memory-pressure threshold, (3) disk write-rate, (4) `state_rounds`
count-only. Scribe re-measured all four first-hand before the impls landed (19:23–19:25Z at
`af2d4e79…`/`3307761a…`; scratch `/tmp/mori-scribe-r7/before/`): tmux `sessions=3`
count-only with zero session names in output; cgroup `high=5000 max=2000` printed with no
finding; `grep -c diskstats` = 0 while `/proc/diskstats` held 9 unread lines; two
`state_rounds` fixtures with values 3/5 vs 99/100 producing byte-identical rows. Baseline
beside the gaps: selftest `PASS (30 cases, 30 passed, 0 failed)` exit 0; oracle
`matched=28 total=28` exit 0; live `DRIFT (findings=15 drift=14 unavailable=1 surfaces=7)`
exit 1.

Landed (evidence commit `[PARENT]`): `tools/mori-census.sh` `c7c3569b…`
(`VERSION=census-r4`, 2004 lines, +584/−18 vs `af2d4e79…`) — tmux relevance classification
(pane-current-path rule, `TMUX_FOREIGN_SESSION` info, `relevance=unavailable` arm,
`:1242-1302`); PSI memory-pressure grading (`MEM_PRESSURE_HIGH` at labeled-local
`MEM_PSI_WARN_AVG10=10`, `:649-685`), fill/avail grading (`MEM_FILL_HIGH` at local 85 for
numeric `memory.max`; `MEM_AVAIL_LOW` at local 10% host MemAvailable floor, `:686-741`) and
the r2 defect-3 disclosure (`local_oom_kill=` on the row); since-boot write average per
target device (`io_basis=since-boot io_avg_since_boot=<dev>:<Bps>/<uptime>s`, reasons in
`io_avg_unavailable=`, `DISK_IO_UNMEASURED` info when nothing measurable, `:764-868`) with
the instantaneous rate left a **bounded deferral**, precondition named in the header
(`:44-52`); `state_rounds` VALUES read with per-lane ledger comparison
(`WATCHDOG_STATE_LAG`/`_AHEAD` info, `:390-451`). Selftest 30 → 45 cases (+15, zero
removed). `tools/mori-silence-cases.sh` `448f7723…` — the entire diff vs the frozen r6
bytes is **+8/−0 lines**: fixture pins `MORI_DISKSTATS`/`MORI_UPTIME` so the new disk
row's live-varying divisor cannot break case 28's two-shape invariance; registry (28
`CASE_IDS`) unchanged, no assertion touched. `corpus/knowledge/surfaces-r7.md` (249 lines —
per-gap probe design at file:line, fixture receipts, limitations, defect log, additive
field-set proof); lesson
`corpus/lessons/2026-10-15-free-lunch-measurements-counter-baselines.md`; receipts
`corpus/evidence/surfaces-r7-20261015T1948Z-{selftest,oracle,live,tmux,memory,diskrate,staterounds}.log`
(indexed in `corpus/evidence/README.md`, incl. the old→new `key=`-diff table showing
`old_only_keys=[]` for all seven surfaces); SKILL.md r7 rows (`state_lag=`/`state_ahead=`,
PSI/fill thresholds, `io_avg_since_boot`, tmux relevance); `corpus/README.md` r7 rows incl.
the named-limits section; `corpus/knowledge/observability-surfaces-r2.md` r7 updates landed
(+65 lines across its four Gaps sections).

**Parent acceptance (`[PARENT: 2026-10-15T__Z]`).** `[PARENT: re-run — selftest 45/45 exit
0; oracle 28/28 exit 0 (≥2 seeds; pinned pair byte-identical); live census; gap probes.]`
This seat's independent battery at the landed SHAs (19:42–19:52Z, SHA re-verified
unchanged): selftest `PASS (45 cases, 45 passed, 0 failed)` exit 0; oracle `matched=28
total=28` exit 0 ×2 (seeds `3600785900`/`1106091929`) + pinned pair byte-identical (3002
bytes); live `DRIFT (findings=15 drift=14 unavailable=1 surfaces=7)` exit 1 — unchanged
shape. Gap probes: tmux `sessions=3; relevant=1 foreign=2 unclassified=0` + 2 ×
`TMUX_FOREIGN_SESSION`; PSI 42 → `MEM_PRESSURE_HIGH … threshold_label=local`; cgroup fill
95% → `MEM_FILL_HIGH`; host-ram 5% → `MEM_AVAIL_LOW`; disk
`io_avg_since_boot=dm-0:9696649Bps/11222s` byte-matching this seat's independent
computation from `/proc/diskstats` × 512 ÷ `/proc/uptime`; state fixture →
`state_rounds=3 state_rounds_max=9 state_lag=1 state_ahead=1` + LAG/AHEAD findings.
Canaries on the new read paths (unreadable diskstats/uptime, garbage diskstats,
non-integer sector field, unreadable PSI, unreadable `memory.max`): every one produced a
full verdict line, graded rc, 0 stderr bytes — the pipefail crash class is not
reintroduced. The write-rate deferral's precondition datum is recorded in the diskrate
receipt: a 10 s sample pair read 715980 Bps against the same clock's since-boot average
9549258 Bps, at +10 s gate cost (whole gate 3436 ms). Note-recorded in-wave defect: `[: max: integer expected` on stderr at
intermediate revisions (`619e0232…`/`75dd142d…`), fixed at the final bytes by testing the
literal `max` first; the selftest now fails any case with shell-diagnostic noise
(`:1518-1524`).

**Verdicts.** `[PARENT: bind — expected ADMIT on the evidence above; no scalar score.]`
Read: coverage **improved** (four gaps closed; +15 selftest cases, zero removed; one
sub-question — the instantaneous write rate — a named bounded deferral; tmux relevance is
fixture-proved, not live-proved this round — no tmux server, named), operability
**improved** (selftest 30→45; oracle 28/28 across three independent seed sets + pinned
byte-identical; live census honest; new read paths canaried; the stderr defect closed and
guarded), depth **improved**, freshness **improved narrowly** (six receipts; index rows
pending), calibration **improved** (thresholds labeled local; tri-state `psi_source`;
never-0-B/s disclosures; info-vs-warn distinction stated), adjacency **unchanged**; none
harmed. Named debt for round 8: the instantaneous-rate deferral precondition; tmux
per-session freshness (unmeasured, note §1); the labeled-local memory thresholds must be
recalibrated by any operator reusing the gate (note §2); carried — drift
pin, row-6 report-body residual, receipt-binding and role-routing debts.

**Boundaries held.** Detection/report only; no remediation/kills; the new probes are
read-only reads of `/proc/diskstats`, `/proc/uptime`, PSI files and `tmux list-panes`;
fixtures `/tmp`; seats committed nothing; parent integrated under the mori identity.
`[PARENT: confirm from the integration diff]`

Round report: `[PARENT: .ufo/reports/round-7/mori-goalwave.md]` · Verified lane rounds:
`[PARENT: 6 → 7]`.