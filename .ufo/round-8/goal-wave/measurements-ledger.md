# Round 8 — scribe measurement ledger (working record)

Seat: scribe (round-8 goal wave) · lane mori-shokunin · writes only under
`.ufo/round-8/goal-wave/`. Detection and report only; fixtures `/tmp` only; no fleet writes.
This ledger carries the raw first-hand measurements the three drafts cite; it is a working
record, not a deliverable.

## Pinned bytes at scribe clock (before-side)

| Artifact | sha256 | Version/label |
|---|---|---|
| `tools/mori-census.sh` (r7 HEAD `ed9de46`) | `c7c3569b842ab3911cbfdf415eb7023766c950c60f354af95f6a4f020b5671af` | `VERSION=census-r4`, 2004 lines |
| `tools/mori-silence-cases.sh` (r7 HEAD) | `448f77238c73a5c929a898dad0f0c495fd2a66cc4b90a00ae84ede69a86beeb5` | r7 oracle, 1090 lines |

`git show HEAD:tools/mori-census.sh | sha256sum` = `c7c3569b…` (r7 bytes); the live working
tree file was already mid-edit at scribe clock (see "WIP observation" below), so the
before-side residual probes were run against a frozen copy extracted from HEAD:
`/tmp/mori-scribe-r8/before/mori-census-r7.sh` (sha256 `c7c3569b…`, re-verified).

## Verdict-machine baseline (before, first-hand, 2026-10-15T20:09Z)

| Check | Command | Verbatim tail | Exit | wall |
|---|---|---|---|---|
| selftest | `bash tools/mori-census.sh --selftest` | `MORI_CENSUS_SELFTEST: PASS (45 cases, 45 passed, 0 failed)` | 0 | 13891 ms |
| oracle | `bash tools/mori-silence-cases.sh` | `MORI_SILENCE_CASES: matched=28 total=28` (run1 + run2) | 0 | 9890 ms (run1) |
| live census | `bash tools/mori-census.sh` | `MORI_CENSUS: DRIFT (findings=15 drift=14 unavailable=1 surfaces=7)` | 1 | 14676 ms |

stderr 0 B on every run. Wall times are host-under-wave-load (32 seats), not idle-host
figures; they are recorded as measured, not as a baseline. Scratch `/tmp/mori-scribe-r8/before/`.

## Residual probe battery — before side (r7 bytes, hermetic /tmp fixtures)

Probe script `/tmp/mori-scribe-r8/before/run-residuals.sh` (census path parameterized);
run at `CENSUS=/tmp/mori-scribe-r8/before/mori-census-r7.sh`; log
`/tmp/mori-scribe-r8/before-r7-residuals.log`.

### Residual 3 — `*.round` symlink/dir invisibility (r7 note §4, report residual 3)

Fixture `fx-symlinkdir`: `.ufo/state/` holds `kagi.round` (regular, value 3) **plus**
`altsym.round` (symlink → `kagi.round`) and `altdir.round/` (empty directory). Control
`fx-control` holds only `kagi.round`. Both run at pinned `MORI_NOW_EPOCH=1700000000`.

```
A row: SURFACE watchdog: ok (… state_rounds=1 state_rounds_max=3 state_lag=0 state_ahead=0 state_cmp=0 state_val_unreadable=0; ts=…)
C row: SURFACE watchdog: ok (… state_rounds=1 state_rounds_max=3 state_lag=0 state_ahead=0 state_cmp=0 state_val_unreadable=0; ts=…)
normalized A vs C watchdog rows identical after fixture-path normalize: YES
tokens 'altsym'/'altdir' in A output: 0
symlink still a symlink: yes ; dir still a dir: yes  (fixture intact)
```

At `c7c3569b…` the state walk is `find "$STATE_DIR" -maxdepth 1 -type f -name '*.round'`
(census `:394` at that SHA): a symlink or directory named `*.round` is not counted, not
read, not compared, not disclosed — byte-identical rows to the control. Invisibility proven.

### Residual 2 — tmux per-session freshness (r7 note §1 limitation b, report residual 2)

Fixture `fx-tmux-act1` vs `fx-tmux-act2`: identical pane data (`fleet` pane cwd under the
fixture root, `scratch` pane at `/tmp`), but the `tmux ls` stub text differs wildly in its
created/activity columns (act1: "created Mon Oct 13 … (attached)"; act2: "created Wed Oct 15
20:00 … (activity Wed Oct 15 20:05 …)" and an epoch-zero activity).

```
B1 row: SURFACE tmux: ok (… sessions=2; relevant=1 foreign=1 unclassified=0 rule=pane_cwd_under_fleet_root; ts=…)
B2 row: SURFACE tmux: ok (… sessions=2; relevant=1 foreign=1 unclassified=0 rule=pane_cwd_under_fleet_root; ts=…)
normalized B1 vs B2 tmux rows identical despite different activity text: YES
token 'activity' in census source: 0
```

At `c7c3569b…` the probe asks only `tmux ls` (count) and `tmux list-panes -a -F
'#{session_name}\t#{pane_current_path}'` (relevance, census `:1260` at that SHA). No
`session_activity` read exists; per-session freshness is unmeasured. Proven.

### Residual 4 — memory-probe residuals (r7 note §2 limitations)

```
memory.peak in r7 census source: 0        # grep -c 'memory\.peak' /tmp/…/mori-census-r7.sh
live memory.max: max                       # /sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/memory.max
thresholds block (r7): :173 MEM_PSI_WARN_AVG10=${MORI_MEM_PSI_WARN_AVG10:-10}
                       :174 MEM_FILL_WARN_PCT=${MORI_MEM_FILL_WARN_PCT:-85}
                       :175 MEM_AVAIL_MIN_PCT=${MORI_MEM_AVAIL_MIN_PCT:-10}
```

The three residuals named in `surfaces-r7.md` §2 limitations: (a) the three thresholds are
local placeholders, not host-measured; (b) on this host `memory.max` is `max`, so the
closed-container fill ratio never exists and only the host-ram scope is live-observable;
(c) the fixture arms are hermetic proofs of arithmetic/direction, not a measurement of the
fleet's own memory-pressure distribution. `memory.peak` — the free, scope-local
high-watermark the r7 lesson §5 named — is unread at the r7 bytes.

### Residual 1 — instantaneous disk write-rate (r7 note §3, report residual 1)

At `c7c3569b…` the disk row is `io_basis=since-boot io_avg_since_boot=<dev>:<Bps>/<s>s …`
(census `:866` at that SHA); the two-sample/instantaneous rate is a bounded deferral with
the precondition named in the header (`:49-52` at that SHA): "measure the wall-time a second
sample adds and record it in the round note".

Scribe's independent two-sample cost measurement (read `/proc/diskstats` field 10 for
`dm-0`, sleep, read again; 5 reps each; host under wave load):

```
sleep=0.2 rep=1 wall_ms=208 sectors=242701376->242701376 delta=0
sleep=0.2 rep=2 wall_ms=213 sectors=242701376->242701376 delta=0
sleep=0.2 rep=3 wall_ms=210 sectors=242701376->242701640 delta=264
sleep=0.2 rep=4 wall_ms=216 sectors=242701640->242701640 delta=0
sleep=0.2 rep=5 wall_ms=211 sectors=242701640->242701640 delta=0
sleep=1.0 rep=1 wall_ms=1015 sectors=242701640->242703944 delta=2304
sleep=1.0 rep=2 wall_ms=1024 sectors=242703944->242707040 delta=3096
sleep=1.0 rep=3 wall_ms=1016 sectors=242707040->242712752 delta=5712
sleep=1.0 rep=4 wall_ms=1011 sectors=242712752->242714608 delta=1856
sleep=1.0 rep=5 wall_ms=1011 sectors=242714608->242732360 delta=17752
```

Median added wall: **0.2 s variant ≈ 211 ms** (min 208, max 216); **1.0 s variant ≈ 1015 ms**.
Both are far above the round's 50 ms median bar for the 0.2 s variant. The 0.2 s window also
mostly reads a zero delta on this host (3 of 5 reps: 0 sectors), i.e. it is both expensive
and noisy — the same shape the r7 diskrate receipt measured at a 10 s window.

## WIP observation (not a deliverable — for tracking only)

At scribe clock the working-tree `tools/mori-census.sh` was already mid-edit
(`db2894dd…` at 20:14Z, `+291/−9` vs HEAD), containing r8 work for residuals 2/3/4
(`WATCHDOG_STATE_ENTRY_UNREADABLE` + `state_val_unread_reasons=file/symlink/dir/other`,
`mem_peak=`/`mem_peak_source=`/`mem_peak_anchor=`, `TMUX_TIMEOUT_S` + `run_timeout` +
`TMUX_SESSION_IDLE`/`TMUX_FRESHNESS_UNAVAILABLE`). Residual 1 (disk) was not yet touched at
that revision (`:849-850` still "No sampling interval is added"). These are intermediate
bytes; the drafts bind only the final landed SHAs.

## Ledger status

Before-side complete. After-side pending the landed census + oracle SHAs and the landed
`corpus/knowledge/surfaces-r8.md`; drafts to be built from those.

## Revision history observed (working tree, mid-wave — for tracking only)

The census iterated through many revisions between scribe start and this note (SHA prefix +
observed state; none is a draft binding):

| clock | census sha prefix | observed state |
|---|---|---|
| 20:14Z | `db2894dd` | +291/−9 vs HEAD; r8 work for R2/R3/R4 present; R1 untouched |
| 20:15Z | `b144af82` | +295/−9; `state_val_unread_reasons` present |
| 20:17Z | `c764ff68` | still iterating |
| 20:18Z | `5c10243f` | selftest 56/56 exit 0; oracle 28/28 ×2; live `DRIFT (15/14/1)` |
| 20:21Z | `7f3fcacf` | `VERSION=census-r5`, 2373 lines; **selftest printed `PASS (56 cases, 56 passed, 0 failed)` but exited 2 with stderr `line 2385: return: can only 'return' from a function or sourced script`** — an intermediate-revision defect (a top-level `return`) |
| 20:24Z | `390ab9cd` | **selftest FAIL: `FAIL watchdog: missing state dir -> provable 0, no crash: missing match \|^SURFACE watchdog: ok\|` (55/56)** — still red mid-edit |

Oracle remained `448f7723…` throughout (no rebase landed yet). No `surfaces-r8.md`, no r8
receipts, no r8 lesson at 20:24Z. These are intermediate bytes; the drafts bind only the
final landed SHAs. If the final bytes land green, the two red intermediate states above are
"not at the pinned bytes" (the r7 pattern) and belong in the round's correction note.

## After-side battery at the stable landed bytes (scribe, 20:22–20:31Z)

Pinned: census `390ab9cd2db17b9d71508639f4f61cc61646ae090b61bf48243cda3e7211cae1`
(`VERSION=census-r5`, 2380 lines, +397/−21 vs HEAD); oracle `448f7723…` (**unchanged** — no
rebase landed). Census SHA re-verified unchanged across the battery + 5 selftest runs. Logs:
`/tmp/mori-scribe-r8/after-battery.log`, `/tmp/mori-scribe-r8/after-battery2.log`, scratch
`/tmp/mori-scribe-r8/after/`.

| Check | Verbatim tail | Exit | stderr |
|---|---|---|---|
| selftest ×5 | `MORI_CENSUS_SELFTEST: PASS (56 cases, 56 passed, 0 failed)` (45 → 56, +11, zero removed) | 0 | 0 B |
| oracle ×2 | `MORI_SILENCE_CASES: matched=28 total=28` (seed `1255880576`; `448f7723…` unchanged) | 0 | 0 B |
| live census | `MORI_CENSUS: DRIFT (findings=15 drift=14 unavailable=1 surfaces=7)` | 1 | 0 B |

Residual probes (hermetic /tmp fixtures):

- **R3 `*.round`** — `state_rounds=1 state_rounds_max=3 … state_val_unreadable=2
  state_val_unread_reasons=file:0 symlink:1 dir:1 other:0` +
  `FINDING WATCHDOG_STATE_ENTRY_UNREADABLE … reason=is-directory entry=altdir.round` and
  `… reason=symlink-not-followed entry=altsym.round`.
- **R2 tmux** — fresh `freshness=ok probed=1 idle=0 freshness_unavailable=0 idle_warn_s=3600`;
  idle `idle=1` + `FINDING TMUX_SESSION_IDLE info … idle_s=100000 threshold_s=3600
  threshold_label=local basis=session_activity`; hang guard (stub sleeps 30 s, bound 1 s) →
  `reason=rc-124`, **census wall 1308 ms**.
- **R4 memory** — live `mem_peak=28812898304 mem_peak_source=ok mem_peak_anchor=1792082289`;
  fixture `mem_peak=28801970176 … anchor=1792096104`; source `memory.peak` refs = 6.
- **R1 disk** — row unchanged (`io_basis=since-boot io_avg_since_boot=dm-0:9451748Bps/13831s
  io_avg_unavailable=tmpfs:not-a-block-device`); the deferral carries the measured numbers in
  the header r8 block (0.2 s min 210 ms = 4.2× the 50 ms budget).

Live rows (20:27:58Z): watchdog `state_rounds=21 state_rounds_max=18 state_lag=0 state_ahead=0
state_cmp=21 state_val_unreadable=0 state_val_unread_reasons=file:0 symlink:0 dir:0 other:0`;
cgroup `psi_some_avg10=0.00 … mem_fill_scope=host-ram host_mem_avail_pct=65
mem_peak=28812898304 mem_peak_source=ok mem_peak_anchor=1792082289`; disk `io_basis=since-boot
…`; tmux `unavailable (cmd=tmux ls; rc=1)`.

Pipefail sweep at `390ab9cd…`: no new bare-pipeline assignments; every new read path uses
`cap` / `run_timeout` / `num_of`; the one new pipeline (`state_list=$(printf … | LC_ALL=C
sort || true)`) has a `printf` producer and `|| true`.

## Ledger status (final at scribe clock)

Drafts v2 (`scorecard-verdict-draft.md`, `log-entry-draft.md`, `report-draft.md`) are built
from the sections above. After-side pinned to census `390ab9cd…` / oracle `448f7723…`
(unchanged). **Named gap:** `corpus/knowledge/surfaces-r8.md`, the r8 receipts, and any oracle
re-baseline were NOT landed at scribe clock; the drafts mark them `[PENDING]` and the parent's
acceptance must re-verify the final census SHA (it may move after this clock) and re-run the
battery before admitting.
