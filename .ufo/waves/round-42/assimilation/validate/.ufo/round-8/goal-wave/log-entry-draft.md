# Round 8 log-entry draft (scribe seat, goal wave)

Integration target: append as a `## Round 8 — … (goal wave)` entry at the end of `LOG.md`
(parent-owned; append-only — nothing above the new section changes). `[PARENT: …]` marks
what only the integration commit/acceptance can bind; `[PENDING: …]` marks values unlanded
at this draft's clock (v2, 2026-10-15T20:32Z).

---

## Round 8 — coverage: the four r7 residuals closed or upgraded with measured numbers (goal wave)

**Round 8 — goal-wave admission (2026-10-15).** Motivating evidence: the round-7 admission's
named residuals (`SCORECARD.md:381-384`; `corpus/knowledge/surfaces-r7.md` "Honest
residuals") — (1) instantaneous disk write-rate deferred with no measured cost, (2) tmux
per-session freshness unmeasured, (3) `*.round` symlink/dir invisibility, (4) the three
memory-probe residuals in `surfaces-r7.md` §2. Scribe re-measured all four first-hand before
the impls landed (20:09–20:17Z at `c7c3569b…`/`448f7723…`; scratch
`/tmp/mori-scribe-r8/before/`; residual probes against a frozen HEAD copy so the mid-edit
working tree could not contaminate the before-side): disk row `io_basis=since-boot
io_avg_since_boot=dm-0:9470717Bps/12757s` with no instantaneous field and the deferral
carrying no number (scribe's own 0.2 s/1.0 s two-sample cost: median 211 ms / 1015 ms, n=5);
tmux source token `activity` = 0 and two wildly different activity-text fixtures producing
byte-identical tmux rows; a `.round` symlink + directory producing a row byte-identical to
the single-file control (`state_rounds=1 … state_val_unreadable=0`); `memory.peak` unread
(grep 0), thresholds local (`:173-175`), live `memory.max=max`. Baseline beside the
residuals: selftest `PASS (45 cases, 45 passed, 0 failed)` exit 0; oracle `matched=28
total=28` exit 0 ×2; live `MORI_CENSUS: DRIFT (findings=15 drift=14 unavailable=1 surfaces=7)`
exit 1; stderr 0 B.

Landed (evidence commit `[PARENT]`): `tools/mori-census.sh` `390ab9cd…`
(`VERSION=census-r5`, 2380 lines, +397/−21 vs HEAD) — `*.round` entry classification with
reason codes (`WATCHDOG_STATE_ENTRY_UNREADABLE`; `state_val_unread_reasons=file:N symlink:N
dir:N other:N`; symlinks never followed; `state_rounds` keeps its r7 meaning);
`run_timeout`-bounded tmux per-session freshness (`tmux display-message -p -t <session>
'#{session_activity}'`, `MORI_TMUX_TIMEOUT_S` default 2 s, rc 124 = bound;
`TMUX_SESSION_IDLE` INFO at labeled-local `MORI_TMUX_IDLE_WARN_S`; `TMUX_FRESHNESS_UNAVAILABLE`
for rc/junk/no-timeout-bin, the last refusing to run unbounded; only fleet-relevant sessions
probed); `mem_peak` + `mem_peak_source` + `mem_peak_anchor` (scope high-watermark with its
instance anchor; non-integer refused); the disk-rate deferral upgraded to measured numbers in
the header r8 block (isolated 30× arms: two extra reads median 16 ms, +0.2 s min 210 /
median 229 / p90 240 / max 265 ms, +1.0 s min 1011 / median 1025 / max 1051 — the 0.2 s
minimum is 4.2× the 50 ms budget, so the windowed rate stays unimplemented; gate-level
medians declared unusable, spread >10 s); selftest 45 → 56 cases (+11, zero removed). Lesson
`corpus/lessons/2026-10-15-probe-pricing-dwell-bounds-filter-drop.md` landed. **Not landed at
scribe clock (named gap):** `corpus/knowledge/surfaces-r8.md`, the r8 receipts under
`corpus/evidence/`, and any oracle re-baseline — `tools/mori-silence-cases.sh` is unchanged at
`448f7723…` and still passes 28/28 exit 0 ×2 against the new census; SKILL.md / `corpus/README.md`
r8 rows `[PENDING]`.

**Parent acceptance (`[PARENT: 2026-10-15T__Z]`).** `[PARENT: re-run — selftest 56/56 exit 0;
oracle 28/28 exit 0 (≥2 seeds; pinned pair byte-identical); live census; the four residual
probes.]` This seat's independent battery at the landed census `390ab9cd…` (SHA re-verified
unchanged across the battery + 5 selftest runs; 20:22–20:31Z): selftest `PASS (56 cases, 56
passed, 0 failed)` exit 0 (5 runs, 0 B stderr); oracle `matched=28 total=28` exit 0 ×2 (seed
`1255880576`); live `DRIFT (findings=15 drift=14 unavailable=1 surfaces=7)` exit 1 (0 B
stderr). Probe A `state_val_unreadable=2 state_val_unread_reasons=file:0 symlink:1 dir:1
other:0` + the two `WATCHDOG_STATE_ENTRY_UNREADABLE` findings; Probe B fresh `freshness=ok
probed=1 idle=0`, idle `TMUX_SESSION_IDLE idle_s=100000 threshold_s=3600 threshold_label=local`,
hang guard `reason=rc-124` at **1308 ms wall against a 30 s stub**; Probe C live
`mem_peak=28812898304 mem_peak_source=ok mem_peak_anchor=1792082289`; Probe D disk row
unchanged (`io_basis=since-boot io_avg_since_boot=dm-0:9451748Bps/13831s
io_avg_unavailable=tmpfs:not-a-block-device`) + the deferral numbers in the header. Pipefail
sweep: no new bare pipelines (all new reads go through `cap`/`run_timeout`/`num_of`). Mid-wave
revision history (measured, not at the stable bytes): ≥9 observed census revisions; at
`7f3fcacf…` the selftest printed PASS but exited 2 (`line 2385: return: …`), and one 55/56
FAIL (`missing state dir`) was observed against a file being rewritten — neither reproduces
at the stable bytes.

**Verdicts.** `[PARENT: bind — expected ADMIT on the evidence above; no scalar score.]` Read:
coverage **improved** (all four residuals closed or measured-deferred; +11 selftest cases,
none removed), operability **improved** (worst-case probe latency bounded and measured via
the hang guard; no new bare pipelines; oracle 28/28), depth **improved** (lesson with the
four prices of a deferred probe), freshness **improved narrowly** (SHA-pinned battery;
receipts `[PENDING]`), calibration **improved** (the disk cost measured, not assumed; local
thresholds re-affirmed with observed distances; peak anchor printed), adjacency **unchanged**;
none harmed. Named debt for round 9: instantaneous-rate deferral (measured grounds); tmux
freshness live-proof (no server); `surfaces-r8.md` + receipts + oracle re-baseline unlanded
at scribe clock; carried — drift pin, row-6 report-body residual, receipt-binding and
role-routing debts.

**Boundaries held.** Detection/report only; no remediation/kills/config edits; new reads are
read-only (`/proc/diskstats`, `/proc/uptime`, PSI/`memory.peak` files, one bounded
`tmux display-message`); fixtures `/tmp`; seats committed nothing; parent integrated under the
mori identity. `[PARENT: confirm from the integration diff]`

Round report: `[PARENT: .ufo/reports/round-8/mori-goalwave.md]` · Verified lane rounds:
`[PARENT: 7 → 8]`.