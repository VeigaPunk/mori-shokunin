# Round 8 verdict — integration draft (scribe seat, goal wave)

Integration target: append as a `## Round 8 verdict — 2026-10-15 (goal wave)` section in
`SCORECARD.md` (parent-owned; append-only — the round-7 section `SCORECARD.md:339-385` and
everything above it stay untouched). Verdict vocabulary only (`improved` / `harmed` /
`unchanged` / `unprovable-but-better`); no scalar scores. Every figure below is bound to a
landed artifact, a receipt, or a command run at a pinned SHA; `[PARENT: …]` marks values
only the integration commit or the parent's acceptance re-run can bind; `[PENDING: …]`
marks values unlanded at this draft's clock.

- Evidence commit: `[PARENT: wave integration commit hash under the mori identity]`
- Lane baseline entering the wave: `ed9de46` (round-7 records; evidence `d30b4e4`).
- Round-count claim: `[PARENT: verified-round accounting 7 → 8 on admission]`
- Draft status: **v2** by the scribe seat. Before-side measured first-hand at the frozen r7
  pair census `c7c3569b842ab3911cbfdf415eb7023766c950c60f354af95f6a4f020b5671af`
  (`VERSION=census-r4`, 2004 lines) / oracle
  `448f77238c73a5c929a898dad0f0c495fd2a66cc4b90a00ae84ede69a86beeb5`, 20:09–20:17Z; residual
  probes against a frozen HEAD copy (`/tmp/mori-scribe-r8/before/mori-census-r7.sh`, sha
  re-verified `c7c3569b…`) with hermetic `/tmp` fixtures. After-side measured first-hand at
  census `390ab9cd2db17b9d71508639f4f61cc61646ae090b61bf48243cda3e7211cae1`
  (`VERSION=census-r5`, 2380 lines; +397/−21 vs HEAD) / oracle `448f7723…` (**unchanged — no
  rebase landed at scribe clock**), 20:22–20:31Z, census SHA re-verified unchanged across the
  battery + 5 selftest runs. Lesson
  `corpus/lessons/2026-10-15-probe-pricing-dwell-bounds-filter-drop.md` landed.
  `corpus/knowledge/surfaces-r8.md` and the r8 receipts were **not landed at scribe clock** —
  named as a gap, not claimed. Scratch `/tmp/mori-scribe-r8/{before,after}/`.

## Round 8 verdict

Round scope (the round-7 residuals, `surfaces-r7.md` "Honest residuals"; `SCORECARD.md:381-384`):

1. **instantaneous disk write-rate** — r7 deferred it without a measured cost; the
   precondition (impl header `:49-52`): measure the wall-time a second sample adds.
2. **tmux per-session freshness** — r7 classified relevance only (note §1 limitation b).
3. **`*.round` symlink/dir invisibility** — the r7 walk filtered on `-type f`.
4. **memory-probe residuals** — the three `surfaces-r7.md` §2 limitations (thresholds local,
   only the host-ram arm live-observable, fixture arms hermetic-only).

Registered claim: before — the four named residuals stand receipt-backed; after — each is
closed with a measured probe + selftest coverage, or its deferral carries measured numbers;
**AND** selftest all-pass (+N, none removed), oracle `28/28` exit 0 at the new pinned SHAs
(additive-only re-baseline), live census honest, existing rows byte-semantics-stable,
thresholds labeled local, no new bare pipelines (the pipefail lesson), worst-case probe
latency bounded and measured.

**Before** (scribe first-hand, 20:09–20:17Z at `c7c3569b…`/`448f7723…`; fixtures `/tmp` only):

- **R1 disk** — live row `io_basis=since-boot io_avg_since_boot=dm-0:9470717Bps/12757s
  io_avg_unavailable=tmpfs:not-a-block-device`; the deferral carried no number. Scribe's own
  two-sample measurement: 0.2 s variant median 211 ms (208–216, n=5), 1.0 s variant median
  1015 ms (1011–1024); the 0.2 s window read a zero delta in 3 of 5 reps.
- **R2 tmux** — token `activity` count in the census source = 0; two fixtures whose `tmux ls`
  text differs wildly in created/activity columns produce byte-identical tmux rows
  (relevance only) — per-session freshness unmeasured.
- **R3 `*.round`** — a symlink and a directory named `*.round` beside a regular
  `kagi.round`(3): row `state_rounds=1 state_rounds_max=3 … state_val_unreadable=0`,
  byte-identical to the single-file control after fixture-path normalization; tokens
  `altsym`/`altdir` = 0 → invisible, no reason code.
- **R4 memory** — `memory.peak` in the census source = 0; thresholds local (`:173-175`
  `MEM_PSI_WARN_AVG10=10` / `MEM_FILL_WARN_PCT=85` / `MEM_AVAIL_MIN_PCT=10`); live
  `memory.max` = `max` (only the host-ram arm observable).
- **Verdict machine beside the residuals** — selftest `PASS (45 cases, 45 passed, 0 failed)`
  exit 0; oracle `matched=28 total=28` exit 0 ×2; live
  `MORI_CENSUS: DRIFT (findings=15 drift=14 unavailable=1 surfaces=7)` exit 1; all stderr 0 B.

**After** at census `390ab9cd…` / oracle `448f7723…` (census SHA verified unchanged through
every run; the oracle did not move):

- **R1 disk — deferral upgraded with measured numbers (not implemented; condition fails).**
  The impl header's r8 block records isolated 30× micro-benchmarks (`/tmp/r8m/micro-disk.log`):
  two extra diskstats reads floor min 5 / median 16 / p90 27 / max 32 ms; +0.2 s dwell min
  210 / median 229 / p90 240 / max 265; +1.0 s min 1011 / median 1025 / max 1051; the 0.2 s
  variant's **minimum 210 ms is 4.2× the 50 ms budget**, so the windowed rate stays out and
  the deferral now stands on measurement. Gate-level wall time could not resolve the effect
  under wave load (medians 13583/12551/16272/17438 ms, spread >10 s) and is reported unusable,
  not as the decision. The row is unchanged (`io_basis=since-boot …`) — byte-semantics stable.
- **R2 tmux — implemented.** Per fleet-relevant session, one
  `tmux display-message -p -t <session> '#{session_activity}'` under `run_timeout`
  (`MORI_TMUX_TIMEOUT_S`, default 2 s; rc 124 = bound fired). Scribe fixtures: fresh →
  `freshness=ok probed=1 idle=0 freshness_unavailable=0 idle_warn_s=3600`; idle (activity =
  NOW−100000) → `idle=1` + `FINDING TMUX_SESSION_IDLE info … idle_s=100000 threshold_s=3600
  threshold_label=local basis=session_activity`; hang guard (stub sleeps 30 s, bound 1 s) →
  `reason=rc-124` with the whole census at **1308 ms wall** — the bound is measured, not
  asserted; unavailable arms `unparseable-probe-output`, `rc-1`, `no-timeout-bin` (the last
  refuses to run unbounded). Only relevant sessions are probed (a foreign session's quiet is
  not fleet evidence). **Live boundary:** the host again had no tmux server
  (`SURFACE tmux: unavailable (cmd=tmux ls; rc=1)`), so the live row is unavailable and the
  probe is fixture/selftest-proved, not live-proved.
- **R3 `*.round` — implemented.** The walk no longer filters on `-type f`; every `*.round`
  entry is classified before any read, and a non-regular entry is counted with its reason:
  fixture → `state_val_unreadable=2 state_val_unread_reasons=file:0 symlink:1 dir:1 other:0`
  + `FINDING WATCHDOG_STATE_ENTRY_UNREADABLE … reason=symlink-not-followed` and
  `reason=is-directory`; symlinks never followed (selftest's link target `99` must not reach
  `state_rounds_max`). `state_rounds` keeps its r7 meaning (regular entries) so pre-r8 state
  dirs read as before; live row shows `state_val_unread_reasons=file:0 symlink:0 dir:0 other:0`.
- **R4 memory — each of the three residuals carries a measurement.** Header r8 block, taken
  read-only 20:09–20:12Z: (a) 21 PSI/avail samples 3 s apart — `psi_some_avg10` observed
  0.00–0.39 against the local 10 (25× away), host `MemAvailable/MemTotal` 49–53 % against the
  local floor 10 (4.9× away) — the placeholders stay labeled local; (b) a walk of 108
  `memory.max` files: 107 the literal `max`, exactly 1 numeric (`system.slice/polkit.service`
  = 33554432 B), 0 unreadable — the closed-container ratio exists in 1 of 108 scopes, not in
  the fleet's user slice; `memory.peak` is the live scope-local substitute and is now on the
  row with its instance anchor (`mem_peak=28812898304 mem_peak_source=ok
  mem_peak_anchor=1792082289` live; fixture arm `mem_peak=28801970176 … anchor=1792096104`;
  non-integer peak refused as `mem_peak_source=shape-refused`); (c) the same window is this
  host's own pressure record while a 32-seat wave ran — the fixture arms no longer stand alone.
- **Verdict machine green.** selftest `PASS (56 cases, 56 passed, 0 failed)` exit 0 — **+11 vs
  r7's 45, zero removed** (5 consecutive runs); oracle `matched=28 total=28` exit 0 ×2 at
  `448f7723…` (seeds `1255880576` / unpinned; `[PENDING: registry-diff statement]`);
  **oracle re-baseline clause NOT demonstrated** — the oracle sha is unchanged from r7 and the
  new probes are all tolerated by the existing 28 cases (28/28 exit 0); live
  `MORI_CENSUS: DRIFT (findings=15 drift=14 unavailable=1 surfaces=7)` exit 1, 0 B stderr.
  **No new bare pipelines:** the pipefail sweep over the r8 bytes lists only `printf |
  grep/sort/awk || true` shapes and rc-gated readers (`cap`, `run_timeout`, `num_of`); every
  new read path goes through those helpers.

| axis | verdict | before → after evidence |
|---|---|---|
| coverage | **improved** *(selected axis)* | Before: four residuals unmeasured/invisible (bullets above). After: tmux freshness implemented (bounded, unavailable semantics), `*.round` symlink/dir classified with reason codes, memory residuals each measured (peak + anchor + two windowed observations), disk deferral upgraded to measured numbers. Selftest 45 → 56 (+11), zero removed. |
| operability | **improved** | Worst-case probe latency bounded and measured: `run_timeout -k 1` (default 2 s/session) + the hang-guard fixture (30 s stub → rc-124, census 1308 ms); a missing `timeout` binary refuses the probe rather than running unbounded; oracle 28/28 exit 0 ×2; live census runs to a full verdict; no new bare pipelines (sweep). |
| depth | **improved** | Lesson `2026-10-15-probe-pricing-dwell-bounds-filter-drop.md` (a deferred probe's four prices: found-ness, marginal wall time, enforceable bound, filter drop set); the census header carries the per-residual r8 dispositions with the measured numbers. `surfaces-r8.md` `[PENDING: not landed]`. |
| freshness | **improved narrowly** | The landed lesson + SHA-pinned census; r8 receipts `[PENDING: not landed at scribe clock]`; drift pin still absent — carried. |
| calibration | **improved** | The 0.2 s/1.0 s cost is measured, not assumed (30× isolated arms + 5× gate interleaved, gate numbers explicitly declared unusable); `TMUX_IDLE_WARN_S` labeled local and INFO-only; memory placeholders re-affirmed as local with observed distances (25×/4.9×); peak anchor printed so a cumulative high-watermark is instance-scoped. |
| adjacency | **unchanged** | Detection/report only; new reads are read-only (`/proc/*`, PSI/peak files, one bounded `tmux display-message`); fixtures `/tmp`; no remediation/kill/systemctl/host-config content; fleet root read-only for seats. `[PARENT: confirm from the integration diff]` |

Admission: `[PARENT: bind the admission and round-count at integration. Expected disposition
on the evidence above: **ADMIT** — all four registered residuals are closed or carry measured
deferrals; the verdict machine stays green (selftest 56/56 +11 none removed, oracle 28/28,
live honest); worst-case probe latency is bounded and measured. The honest limits: the disk
rate stays unimplemented (measured grounds), tmux freshness is not live-proved (no server),
the memory thresholds remain labeled-local placeholders, and the claim's "oracle
additive-only re-baseline" clause is not demonstrated (the oracle is unchanged and still
28/28).]` No scalar score.

Learning trends (lane idiom):

| Trend | Verdict | Evidence |
|---|---|---|
| expansion | **improved** | Lesson `2026-10-15-probe-pricing-dwell-bounds-filter-drop.md`; census header r8 block with measured numbers; `surfaces-r8.md` `[PENDING]`; SKILL.md r8 rows `[PENDING]`; receipts `[PENDING]`. |
| quality | **improved** | Multi-seat independent measurement (impl micro-benchmark 30× + gate 5×; scribe independent 5× two-sample; lesson seat's independent timing); the hang guard measured end-to-end (30 s stub bounded to 1308 ms); the disk decision made on a measured minimum vs the budget, with the unusable gate-level reading disclosed rather than cherry-picked. |
| discernment | **unchanged** | No outside spot-check of an admit/reject exists — the wave's seats are the lane per protocol. `[PARENT: bind]` |

Named debt for round 9 (carried items unchanged):

1. **Instantaneous write rate** — deferral stands on measured numbers (0.2 s variant min
   210 ms vs a 50 ms budget). Lift only if an operator accepts the runtime cost or a
   cheaper rate source appears.
2. **tmux freshness live-proof** — the probe has no live observation yet (no tmux server at
   the measurement clock); a live idle/fresh session reading is still owed.
3. **surfaces-r8.md + r8 receipts + oracle re-baseline** — not landed at scribe clock; the
   integration must land or explicitly drop them.
4. Carried: frozen-behavioral drift pin (`silence-cutover-r3.md:253-254`); row-6 report-body
   presence-only residual (`silence-cutover-r3.md:250-252`); blocked-attempt receipt-binding
   and role-routing debts (`SCORECARD.md:128-131`); memory thresholds need recalibration by
   any operator reusing the gate elsewhere (labeled local).

`[PARENT: bind the integration commit and round-count; re-run `bash tools/mori-census.sh
--selftest` (expect 56/56 exit 0), `bash tools/mori-silence-cases.sh` (expect 28/28 exit 0;
≥2 seeds; pinned pair byte-identical), the live census, and the residual probes (recipes:
`/tmp/mori-scribe-r8/after-battery.sh`; note `surfaces-r8.md` recheck block once landed).]`