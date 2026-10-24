# mori round 8 — goal-wave report draft (scribe seat)

Integration target: the round report (idiom of `.ufo/reports/round-7/mori-goalwave.md`;
final path `[PARENT]`, likely `.ufo/reports/round-8/mori-goalwave.md`). Parent owns the
final path, the identity and the commit binding. Every figure is bound to a landed
artifact, a receipt, or a command run at a pinned SHA; `[PARENT: …]`/`[PENDING: …]` as
elsewhere.

- Status: `[PARENT: completion statement + verified-round-count claim 7 → 8]`
- Evidence commit: `[PARENT: wave integration commit hash under the mori identity]`
- Baseline: `ed9de46` (round-7 records; evidence `d30b4e4`)
- Wave: `[PARENT: bind the wave record — batch shape, seat completion/loss counts, any backfill]`
- Report time: `[PARENT]`
- Draft status: **v2** by the scribe seat. Before-side at census `c7c3569b…`
  (`VERSION=census-r4`, 2004 lines) / oracle `448f7723…`, measured 2026-10-15T20:09–20:17Z.
  After-side at census
  `390ab9cd2db17b9d71508639f4f61cc61646ae090b61bf48243cda3e7211cae1`
  (`VERSION=census-r5`, 2380 lines; +397/−21 vs HEAD) / oracle `448f7723…` (**unchanged —
  no rebase landed at scribe clock**), measured 20:22–20:31Z, census SHA re-verified
  unchanged across the whole battery + 5 selftest runs. Scratch
  `/tmp/mori-scribe-r8/{before,after}/`.
- **Unlanded at scribe clock (named gap, not claimed):** `corpus/knowledge/surfaces-r8.md`,
  the r8 receipts under `corpus/evidence/`, and any oracle re-baseline/edit. The drafts
  bind them as `[PENDING]`; the parent's acceptance should re-check once they land.

## Work performed

- Selected axis **coverage** — the four residuals named in round 7
  (`corpus/knowledge/surfaces-r7.md` "Honest residuals"; `SCORECARD.md:381-384`; r7 report):
  (1) instantaneous disk write-rate (deferred with no measured cost), (2) tmux per-session
  freshness (unmeasured), (3) `*.round` symlink/dir invisibility, (4) the three memory-probe
  residuals in `surfaces-r7.md` §2.
- Registered claim: before — the four residuals stand receipt-backed; after — each is closed
  with a measured probe + selftest coverage, or its deferral carries measured numbers;
  selftest all-pass (+N, none removed), oracle 28/28 exit 0 at the new pinned SHAs
  (additive-only re-baseline), live census honest, existing rows byte-semantics-stable,
  thresholds labeled local, no new bare pipelines (the pipefail lesson), worst-case probe
  latency bounded and measured.

## Before → after measurements (scribe first-hand)

| Residual | Before at `c7c3569b…` (20:09–20:17Z) | After at `390ab9cd…` (20:22–20:31Z) |
|---|---|---|
| 1 instantaneous disk rate | row `io_basis=since-boot io_avg_since_boot=dm-0:9470717Bps/12757s io_avg_unavailable=tmpfs:not-a-block-device`; header deferred with no number | **deferral now carries measured numbers** (header r8 block): isolated 30× arms — two extra diskstats reads median 16 ms (p90 27, max 32), +0.2 s dwell min 210 / median 229 / p90 240 / max 265, +1.0 s min 1011 / median 1025 / max 1051; the 0.2 s variant's **minimum 210 ms = 4.2× the 50 ms budget** → windowed rate stays unimplemented; gate-level medians declared unusable (spread >10 s). Row unchanged. Scribe's independent two-sample: 0.2 s median 211 ms, 1.0 s median 1015 ms (n=5). |
| 2 tmux per-session freshness | `activity` token in census = 0; two fixtures with different activity text → byte-identical tmux rows | `freshness=ok probed=1 idle=0 freshness_unavailable=0 idle_warn_s=3600`; idle fixture → `idle=1` + `FINDING TMUX_SESSION_IDLE … idle_s=100000 threshold_s=3600 threshold_label=local basis=session_activity`; hang guard (30 s stub, bound 1 s) → `reason=rc-124`, census **1308 ms wall**; arms `unparseable-probe-output`/`rc-1`/`no-timeout-bin` |
| 3 `*.round` symlink/dir | symlink + dir → row byte-identical to control (`state_rounds=1 … state_val_unreadable=0`), tokens `altsym`/`altdir` = 0 — invisible | `state_rounds=1 … state_val_unreadable=2 state_val_unread_reasons=file:0 symlink:1 dir:1 other:0` + `FINDING WATCHDOG_STATE_ENTRY_UNREADABLE … reason=symlink-not-followed` / `reason=is-directory`; symlink target (`99`) never read |
| 4 memory residuals | `memory.peak` in census = 0; thresholds local at `:173-175`; live `memory.max=max` | header r8 block: 21 PSI/avail samples 3 s apart (psi_some 0.00–0.39 vs local 10 = 25× away; host avail 49–53 % vs local floor 10 = 4.9× away — stay labeled local); 108 `memory.max` files walked (107 `max`, 1 numeric, 0 unreadable); live row `mem_peak=28812898304 mem_peak_source=ok mem_peak_anchor=1792082289`, fixture arm `mem_peak=28801970176 … anchor=1792096104` |
| verdict machine | selftest 45/45 exit 0; oracle 28/28 exit 0 ×2; live `DRIFT (15/14/1)` exit 1 | selftest `PASS (56 cases, 56 passed, 0 failed)` exit 0 (+11, zero removed; 5 runs); oracle `matched=28 total=28` exit 0 ×2; live `MORI_CENSUS: DRIFT (findings=15 drift=14 unavailable=1 surfaces=7)` exit 1; all stderr 0 B |

## Landed changes (at scribe clock)

- `tools/mori-census.sh` → `390ab9cd…` (`VERSION=census-r5`, 2380 lines; +397/−21 vs HEAD):
  `*.round` entry classification + reasons (`WATCHDOG_STATE_ENTRY_UNREADABLE`,
  `state_val_unread_reasons`, symlinks never followed), `run_timeout`-bounded tmux
  freshness (`TMUX_SESSION_IDLE` / `TMUX_FRESHNESS_UNAVAILABLE`, `MORI_TMUX_TIMEOUT_S`
  default 2 s, `MORI_TMUX_IDLE_WARN_S` default 3600 labeled local), `mem_peak` +
  `mem_peak_source` + `mem_peak_anchor`, the measured disk-rate deferral block, 11 new
  selftest cases (45 → 56).
- **Lesson** `corpus/lessons/2026-10-15-probe-pricing-dwell-bounds-filter-drop.md` (landed;
  "a deferred probe has four prices": found-ness, marginal wall time, enforceable bound,
  filter drop set).
- SKILL.md r8 rows `[PENDING: confirm at integration]`; `corpus/README.md` r8 rows
  `[PENDING]`; `corpus/knowledge/surfaces-r8.md` `[PENDING: not landed at scribe clock]`;
  receipts `corpus/evidence/…r8…` `[PENDING]`.
- **Oracle `448f7723…` unchanged** — it still passes 28/28 exit 0 ×2 against the new
  census; no "additive-only re-baseline" edit landed at scribe clock (the claim's
  re-baseline clause is not demonstrated yet; the 28/28 clause is).

## Corrections and honest boundaries

1. **Instantaneous write rate remains unimplemented** — the round's condition (0.2 s
   variant < 50 ms median) fails on the measured numbers (min 210 ms = 4.2× budget); the
   deferral stands, now receipt-backed by the impl's own 30× isolated arms. The row's value
   is a since-boot AVERAGE, never a rate.
2. **tmux freshness is fixture/selftest-proved, not live-proved** — the host again had no
   tmux server (`SURFACE tmux: unavailable (cmd=tmux ls; rc=1)`), so the live row keeps the
   r7 `unavailable` shape; the bound is proved hermetically (the sleeping stub lives only
   under `/tmp`, never a real tool).
3. **Memory thresholds stay labeled local** — one host's distribution during a 32-seat wave
   is not a calibration; `MEM_*` placeholders unchanged; the new `TMUX_IDLE_WARN_S` fires
   INFO only so a local number cannot flip the roll.
4. **The memory residuals are upgraded, not all "closed"** — threshold placement and scope
   observability now carry measured numbers, and the fixture arms no longer stand alone
   (live window recorded); they remain placeholders by design.
5. **Mid-wave revision history (measured, not at the pinned bytes):** the census iterated
   through ≥9 observed revisions (`db2894dd…` → `390ab9cd…`); at `7f3fcacf…` the selftest
   printed `PASS (56 cases, …)` but exited 2 with stderr `line 2385: return: can only
   'return' from a function or sourced script`; at `390ab9cd…` one 55/56 FAIL
   (`missing state dir -> provable 0`) was observed against a file being rewritten and is
   not reproducible at stable bytes (5 consecutive 56/56 exit 0). The battery pins the
   stable bytes only.
6. **Post-battery risk named, not hidden:** the census could still be edited after the
   scribe clock (the wave's other seats were still landing note/receipts); the parent's
   acceptance must re-verify the final SHA and re-run the battery.

## SHONEN

- [ ] · [ ] · [ ] · [ ] — all four remain `[ ]`: no named non-author verifier; wave seats
  are the lane per protocol.

Boundaries held: detection and report only; no remediation/kills/config edits; new reads are
read-only (`/proc/diskstats`, `/proc/uptime`, PSI/`memory.peak` files, one bounded
`tmux display-message`); fixtures `/tmp`; seats made no commits; fleet root read-only for
seats. `[PARENT: confirm from the integration diff]`