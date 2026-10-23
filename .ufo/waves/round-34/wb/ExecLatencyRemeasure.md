measured 2026-10-23T07:49:50Z

# ExecLatencyRemeasure — FR6 wall-time re-measurement of `tools/mori-disk-rate.py` (wave B)

Seat: ExecLatencyRemeasure. Lane repo `/home/vgpnk/Projects/shokunin/mori-shokunin` (read-only use).
Judged object: `tools/mori-disk-rate.py`, working-copy sha256 `370932deb525b95135f0c30e4caaf2666b95c6feeffe76b70f06b48c09caa74b`;
blob `c7ea8bdac9c98b8d350a489fb8aca3a4750bcfbf` at both `ba525e1a0394154837eea5090e8bd27ed69c539c` and
`8d56809afccefe0ab80c8e73ac3e1ea57c25f5f3` (`git ls-tree <rev> tools/mori-disk-rate.py` → `100755 blob c7ea8bda…`, both).
Host: 32 CPUs, load 14.6–27.0 during the runs. Scratch: `/fast/scratch/hyaku/mori-r34/a3-ExecLatencyRemeasure/` (112 KB:
`measure.py`, `harness.json`, `harness-short.json`, `harness-b2.json`, `hf.json`). Nothing written outside this report.

## 0. Independence

Every number and every verdict in §1–§3 was measured and reached before
`/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-34/wa/ExecLatencyBudget.md` was opened; that file was
read only in §4. The draft note's cited text (`/fast/scratch/hyaku/mori-r34/a3-L1/drafts/corpus_README.md:549-551`)
was read before the audit and only to name the claim under test.

## 1. Method, and the `--interval-ms 0` question

Two instruments, both n=20 per interval, both against the same working-copy bytes:

- `measure.py` (stdlib): `subprocess.run([sys.executable, TOOL, "--interval-ms", str(N)])` timed with
  `time.perf_counter()`, stdout parsed as JSON, so each sample carries wall time *and* the reported
  `host_write_Bps` (that pairing is what lets §3 answer "does a fitting interval read zero").
- `hyperfine 2.0.0`: `hyperfine -N --warmup 1 --runs 20 --export-json hf.json
  "/usr/bin/python3 …/tools/mori-disk-rate.py --interval-ms N"` for N ∈ {10, 50, 100, 200}. Cross-check only;
  the rate question uses the stdlib harness because hyperfine discards the child's JSON.

`--interval-ms 0` is **not accepted**: `python3 tools/mori-disk-rate.py --interval-ms 0` →
`mori-disk-rate.py: error: --interval-ms must be a positive number of milliseconds`, `rc=2`
(`tools/mori-disk-rate.py:271-273`). There is no 0 ms arm to measure.

Install record (operator directive): **hyperfine 2.0.0**, channel = official GitHub release tarball
`hyperfine-v2.0.0-x86_64-unknown-linux-musl.tar.gz` (sha256 `38e59087bd65520930a13cf513d8a493b7043741e8ad62349a8a9929eb61bc5c`),
installed to `~/.local/bin/hyperfine`; reason `/usr/bin/time` is absent on this host (`command -v /usr/bin/time` → none)
and 20-run min/median/max needs a second instrument. No pacman transaction (paused host-wide). Tarball and unpacked tree
deleted after install.

## 2. Wall time, min/median/max per interval

Stdlib harness, two batches, host load taken from `/proc/loadavg` immediately before and after each batch:

| batch (load 1/5/15 before → after) | N=1 | 5 | 10 | 20 | 25 | 50 | 100 | 200 |
|---|---|---|---|---|---|---|---|---|
| B1 `24.44 33.73 38.39` → `26.93 33.98 38.42` (n=20 each) | 27.7/30.1/36.1 | 30.4/32.2/34.2 | 37.0/39.5/42.8 | — | — | 78.0/79.8/113.6 | 125.8/129.4/132.8 | 227.5/231.5/239.0 |
| B1-short `25.69 33.48 38.21` → `25.69 33.48 38.21` (n=20 each) | — | — | — | 46.7/47.9/52.3 | 50.6/53.4/57.5 | — | — | — |
| B2 `14.77 25.83 34.54` → `14.77 25.83 34.54` (n=20 each) | — | — | 35.6/39.6/42.8 | 44.1/47.4/52.7 | — | — | — | — |

min/median/max in ms. hyperfine (n=20, load `23.44 32.74 37.92` → `23.22 32.38 37.74`):

| N | min | median | mean | max | maxRSS (median) |
|---|---|---|---|---|---|
| 10 | 35.3 | 37.5 | 37.5 | 39.5 | 15.37 MiB |
| 50 | 76.1 | 79.0 | 79.0 | 82.0 | 15.31 MiB |
| 100 | 126.1 | 137.0 | 141.8 | 171.2 | 15.39 MiB |
| 200 | 231.2 | 248.5 | 246.6 | 293.1 | 15.55 MiB |

The two instruments agree on the floor: wall ≈ 28–30 ms of interpreter+import+argparse (`N=1` median 30.1 ms) + the
requested interval, so the marginal cost of the second sample is the interval itself. Under load the upper tail grows
(100 ms: 132.8 → 171.2 ms max, σ = 14.7 ms).

## 3. Which intervals fit 50 ms, and do they read anything

The bar is `corpus/knowledge/surfaces-r8.md:47-48` — "implement a windowed (two-sample) rate **iff the 0.2 s variant adds
< 50 ms median wall time**" — and r8 applied it to the whole block's added wall time, dwell included
(`:75-78`: "the 0.2 s variant's *minimum* over all three isolations is 208 ms — 4.16× the 50 ms budget", 208/50 = 4.16).
Two readings, both reported because they differ only at 50 ms:

- **Whole-probe wall** (what a census-embedded arm would add if it shelled out to the tool): fits at **1, 5, 10 ms**
  (all 60 runs < 43 ms); **20 ms fits on the median** (44.1–47.9) but not on the max (52.3–52.7); **25 ms and up never
  fit**.
- **In-census marginal** (startup already paid; add = 2 reads + dwell): measured gap at 100 ms = 100.310 ms median
  (`+0.31 %`), so the added cost ≈ the interval: fits at ≤ 20 ms, borderline at 50 ms, fails at 100 ms (≈100 ms) and
  200 ms (≈200 ms).

**Do the fitting intervals read zero? No, not reliably.** `host_write_Bps` was nonzero in:

| N | nonzero host runs | largest `host_write_Bps` |
|---|---|---|
| 1 | 0/20 | 0 |
| 5 | 0/20 | 0 |
| 10 | 6/20 (B1, load ≈25) + 0/20 (B2, load 14.8) = **6/40** | 1 180 876 800 B/s (1.18 GB/s) |
| 20 | 1/20 + 0/20 = **1/40** | 6 348 800 B/s |
| 25 | 0/20 | 0 |
| 50 | 12/20 | 124 600 320 B/s |
| 100 | 3/20 | 1 351 680 B/s |
| 200 | 15/20 | 2 232 320 B/s |

The 10 ms nonzeros are real per-device deltas, not a parse artefact — e.g.
`{'nvme1n1': 757760000, 'nvme1n1p1': 757760000, 'dm-0': 423116800, 'nvme0n1': 423116800, 'nvme0n1p2': 423116800}`,
`{'nvme1n1': 30310400, …}`, `{'nvme1n1': 409600, …}` (the 1.18 GB/s host total is the stacked-device run's two disks
summed). They appear only in the loaded batch: at load 14.8, 10 ms read 0 in 20/20. So at a fitting interval the reading
is **zero most of the time and a load-driven burst otherwise**, which is a different failure mode from "reads zero":
an operator cannot tell a quiet device from a short window, and a busy one appears as a spurious GB/s.

Two supporting checks, both n=50 against the tool's own code paths: one raw
`open`+`read`+`close` of `/proc/diskstats` = 0.0058 ms median (0.0057–0.0305); the tool's `read_sample` (which spawns
a thread per open, `tools/mori-disk-rate.py:118-137`) = 0.06 ms median (0.03–0.20). Reads are not the cost. The
divisor is the nominal interval, not the measured gap: measured gap = 10.214 ms at N=10 (`+2.14 %`), 100.310 ms at
N=100 (`+0.31 %`) — re-measured by replaying `read_live_samples`'s own sequence (`:175-183`).

One report on this host to fix the device frame: 11 devices, `host_basis`
`['nvme0n1','nvme1n1','sda','sr0']`, classes `disk` (4), `partition` (6), `stacked` (`dm-0`), all states `ok`.

VERDICT: note's numbers agree

(Subject: `corpus_README.md:550` — "about 128 ms at a 100 ms interval and about 243 ms at 200 ms". Measured: 100 ms
min 125.8/126.1, median 129.4/137.0, max 132.8/171.2; 200 ms min 227.5/231.2, median 231.5/248.5, max 239.0/293.1.
Both cited values sit inside the measured bands.)

VERDICT: unsupported

(Subject: `corpus_README.md:551` — "intervals short enough to fit read zero". At 10 ms, all 40 runs finished in
35.6–42.8 ms, inside a 50 ms budget, and 6/40 read nonzero, up to 1.18 GB/s. At 20 ms the median 47.4–47.9 ms fits and
1/40 read nonzero. Zero-in-20/20 holds only at 1 ms and 5 ms. The honest statement is "fits the budget but reads zero
most of the time and a load-driven burst otherwise".)

VERDICT: no defect found

(Subject: the tool's latency behaviour. One `time.sleep(interval_ms/1000.0)` at `tools/mori-disk-rate.py:183`; measured
inter-read gap = nominal + 0.31 % at 100 ms, + 2.14 % at 10 ms; `--interval-ms 0` rejected with `rc=2` by design at
`:271-273`. The nominal-divisor gap is contract-frozen behaviour (R6), not a latency defect.)

## Audit of /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-34/wa/ExecLatencyBudget.md

Each row is a factual claim that the round would cite, with my own evidence.

| # | claim (as written) | verdict | evidence |
|---|---|---|---|
| 1 | `/usr/bin/time` absent on this host | agree | `command -v hyperfine /usr/bin/time python3` → only `/usr/bin/python3` |
| 2 | tool blob `c7ea8bda…` at both `ba525e1a…` and `8d56809a…` | agree | `git ls-tree` both revs → `100755 blob c7ea8bdac9c98b8d350a489fb8aca3a4750bcfbf` |
| 3 | working-copy sha256 `370932de…` = `cat-file -p c7ea8bda… \| sha256sum` | agree | `sha256sum tools/mori-disk-rate.py` → `370932deb525b9…caa74b` |
| 4 | bar at `surfaces-r8.md:47-48`, applied to whole block incl. dwell (208/50 = 4.16×) | agree | read `:47-48`, `:53-57`, `:75-78`; the 4.16× arithmetic is on the 208 ms total |
| 5 | quiet batch live-100 median 127.93 ms, overall min 126.73 ms | agree | 100 ms min 125.8 (harness) / 126.1 (hyperfine), median 129.4 at load ≈25 |
| 6 | live-200 min 232.18 / median 242.65 / max 264.13 ms | agree | 200 ms min 227.5 / 231.2, median 231.5 / 248.5, max 239.0 / 293.1 |
| 7 | interval 1 ms → 0 in 5/5 | agree | 0/20 nonzero |
| 8 | interval 5 ms → 0 in 5/5 | agree | 0/20 nonzero |
| 9 | interval 10 ms → 0 in 5/5 | **disagree** | 6/40 nonzero (2 batches), max 1 180 876 800 B/s; it is a 5-run sample artefact at load ≈25 (at load 14.8: 0/20) |
| 10 | short-interval cost ≈48–54 ms wall at 15–20 ms | agree | N=20: 46.7/47.9/52.3 and 44.1/47.4/52.7; N=25: 50.6/53.4/57.5 |
| 11 | "a sub-50 ms wall is reachable only at intervals whose readings are zeros or 10²–10⁴× noise" | agree | 10 ms: 34/40 zero, 6/40 at 0.41–1.18 GB/s; 1–5 ms: 40/40 zero |
| 12 | CPU flat across intervals; RSS ~15–16 MiB (floor ~9.6) | agree | hyperfine maxRSS median 15.31–15.55 MiB; wall grows by exactly the interval |
| 13 | one open+read+close of `/proc/diskstats` = 0.008 ms median | agree | raw loop n=50: 0.0058 ms median (0.0057–0.0305) |
| 14 | measured gap = nominal + 0.13 % at 100 ms, + 1.3 % at 10 ms | agree | mine + 0.31 % / + 2.14 % (1.6–2.4× larger at load 25, same negligible-scale conclusion) |
| 15 | census has no call to the tool; only fixture comment at `tools/mori-census.sh:3199` | agree | `grep -c "disk-rate" tools/mori-census.sh` → `1`, line 3199 is the fixture comment |
| 16 | 11 devices; `host_basis ['nvme0n1','nvme1n1','sda','sr0']`; classes disk/partition/stacked | agree | `build_report` on a live pair prints exactly that basis and `dm-0: (stacked, ok)` |
| 17 | verdict: the tool's added latency does not meet the 50 ms budget | agree | no interval ≥ 50 ms fits under either reading (§3) |

AUDIT: agree 16 / disagree 1

The report's own §5(b) is defensible as written because it hedges ("zeros **or** 10²–10⁴× noise") and its §5(c) noise
argument holds at my measurements too. The one overreach is the bare 10 ms row, which a 5-run sample produced and which
the README then condensed into "intervals short enough to fit read zero" — dropping the noise half of the disjunction.
The draft's conclusion (FR6 stays deferred) survives either way: at 100 ms and 200 ms the bar fails by 2.6–5.9×, and at
fitting intervals the reading is not a measurement of a rate.

## Risks, blockers, unrun

- All wall figures are load-sensitive: batches at load 14.8–27.0 on 32 CPUs; the 100/200 ms max columns move 30–45 ms.
  The r8 lesson's rule (instrument noise must be below the threshold) applies here too: at 10 ms the noise is ~1.5 ms
  against a ~20 ms margin, so the "fits" conclusion at 10 ms is robust, while the 20 ms "fits on median" is not.
- I did not measure 500/1000 ms (not assigned). No load was generated; nothing was written to any device or setting.
- The nonzero bursts at 10 ms are background host write traffic and are not attributed to the fleet
  (`[INFERENCE]`: coincident with load 24–27 and absent at load 14.8; not proven).
- No blocker. The lane was not written; only this report was created.
