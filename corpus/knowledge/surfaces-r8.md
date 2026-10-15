# Surface gaps r8 — the four r7 residuals: disposition, sampling-cost adjudication, open items

source: `tools/mori-census.sh` sha256
`390ab9cd2db17b9d71508639f4f61cc61646ae090b61bf48243cda3e7211cae1`
(`VERSION=census-r5`, 2380 lines); oracle `tools/mori-silence-cases.sh` sha256
`448f77238c73a5c929a898dad0f0c495fd2a66cc4b90a00ae84ede69a86beeb5`
(1090 lines, **byte-unchanged from r7** — no re-baseline was required; it passes
28/28 at the new census bytes, see the verdict table).
verified-at: 2026-10-15T20:17–20:39Z — note-writer battery: `--selftest` (×16),
oracle ×2, live census ×2, one hermetic fixture arm per residual plus the hang arms
(FIFO-in-input, FIFO `*.round`, 8 s stub, TERM-ignoring stub), the r7-vs-r8 field-set
diff on one identical fixture and on live, an interleaved old-vs-new fixture timing,
and an n=15 reproduction of the two-sample disk cost. My raw logs:
`/tmp/mori-r8-note/{baseline,after,probes,micro-repro.log}` (ephemeral). Durable
receipts: `corpus/evidence/residuals-r8-20261015T2040Z-{selftest,oracle,live,tmux,
instantaneous,memory,roundfiles}.log` — every one pinned to the same pair
(`CENSUS_SHA256_BEFORE=AFTER=390ab9cd…`), and the oracle receipt's set-close check
re-verifies both SHAs at 2026-10-15T20:48:18Z against the set opened 20:39:32Z, so the
pair these numbers bind to was byte-stable across that 8 m 46 s window.
recheck: `bash tools/mori-census.sh --selftest` (hermetic, /tmp only) ·
`bash tools/mori-silence-cases.sh` (28 cases, exit 0 iff all pass) ·
`bash tools/mori-census.sh` (live, writes nothing, exit 0 CLEAN | 1 DRIFT | 2 setup).
scope: detection and report only (`PROVINCE.md:16-18`); nothing here remediates. All
r8 thresholds are **local placeholders**, labeled `threshold_label=local` on every row
and finding that carries one (`tools/mori-census.sh:249-250`).

This note is the r8 closure of the four residuals the round-7 verdict registered
(`SCORECARD.md:381-385`, `.ufo/reports/round-7/mori-goalwave.md:42-48`). Before-side
measurements are first-hand in `.ufo/round-8/goal-wave/measurements-ledger.md`
(scribe) and in my own r7-vs-r8 arms below; this note carries the after side. The
r7 note's own text is owned by its updater seat, not here.

## Verdict summary — one line per residual

| # | residual (r7 source) | r8 disposition | probe (impl) | selftest cases | my arms | live/fixture row |
|---|---|---|---|---|---|---|
| 1 | instantaneous disk write-rate (`surfaces-r7.md:140-151`) | **DEFERRED, now with measured numbers** (0.2 s variant min 208 ms ≫ 50 ms bar) | header only, `:80-92` | 0 new | 15-run reproduction + gate-level tallies | live row unchanged: `io_basis=since-boot io_avg_since_boot=dm-0:9374197Bps/13983s` |
| 2 | tmux per-session freshness (`surfaces-r7.md:65-70`) | **IMPLEMENTED, timeout-bounded** | `probe_tmux` `:1413-1540`, `run_timeout` `:344` | 6 | 6 arms incl. an 8 s hang stub | live `tmux ls` rc 1 → unavailable; arms below |
| 3 | `*.round` symlink/dir invisibility (`SCORECARD.md:381-383`) | **IMPLEMENTED, with reason codes** | entry walk `:514`, classes `:525-545`, row `:587` | 3 | 3 arms | live `state_val_unread_reasons=file:0 symlink:0 dir:0 other:0`; arms split 1/1 |
| 4 | memory-probe residuals (`surfaces-r7.md:110-118`) | **CLOSED for scope/live-evidence; threshold placement upgraded with a measured window, still labeled local** | `memory.peak` + anchor `:876-905`, row `:925` | 2 | 7 arms | live `mem_peak=28812898304 mem_peak_source=ok mem_peak_anchor=1792082289` |

Nothing was left untouched; one residual (disk) keeps its r7 deferral, now carrying
the measured cost the r7 precondition demanded, per the round's either/or rule.

## Sampling-cost adjudication — residual 1 (the round's decision input)

The round's condition: implement a windowed (two-sample) rate **iff the 0.2 s variant
adds < 50 ms median wall time**; else record a deferral-with-measurement. Two seats
measured; two more parties corroborated.

**Census-impl seat, isolated structural cost** (`/tmp/r8m/micro-disk.log`, n=30/arm,
two-sample block in the census's own idioms, no other probes): floor (two date calls)
median 3 ms (0–7); two extra diskstats reads, no dwell, median 16 ms (5–32, p90 27);
pure `sleep 0.2` median 206 ms (202–215); reads + 0.2 s dwell median **229 ms**
(210–265, p90 240); reads + 1.0 s dwell median 1025 ms (1011–1051).

**Cost seat, through the whole live gate** (`/tmp/mori-r8-cost/results.tsv`, 5
interleaved runs per arm, frozen /tmp copies): baseline (r7 bytes) median 18905 ms at
load ≈76, and the closing baseline re-run median 24146 ms at load ≈114 — a ~5.2 s
drift caused by load alone, larger than any effect under test. sleep 0.2: median
32881 ms (load 103–153); sleep 1.0: median 26798 ms; straddle (no added dwell): median
19662 ms. Conclusion: **the gate-level wall time cannot resolve a 200 ms effect under
this host's wave load** — reported as unusable, not as the decision (the census header
`:89-92` states the same for the impl's own gate-level pair: medians 13583 / 12551 /
16272 / 17438 ms, spread >10 s).

**Corroborating reproductions.** Scribe (`.ufo/round-8/goal-wave/measurements-ledger.md`):
0.2 s → 211 ms median (208–216), 1.0 s → 1015 ms. Mine (n=15, 20:17:30–20:18:31Z):
floor median 1 ms (0–6), two reads 19 ms (10–31), two-sample 0.2 s **222 ms**
(213–234), 1.0 s 1019 ms (1014–1026). The durable receipt's bare pair (receipts-writer,
`corpus/evidence/residuals-r8-20261015T2040Z-instantaneous.log`: reads + `sleep` without
the census's surrounding structure) reads 200.7–203.7 ms across its five 0.2 s reps —
the floor of the class, still 4× the budget; its 1.0 s reps read 1000.1–1002.4 ms.

**Decision (recorded in the impl header `:80-92`):** the 0.2 s variant's *minimum* over
all three isolations is 208 ms — 4.16× the 50 ms budget — so the instantaneous rate
stays unimplemented and the numbers above replace r7's bare precondition. The extra
reads alone are 16 ms median / 27 ms p90; the dwell is the entire cost. Note the same
window is also noisy on this host: the scribe's 0.2 s sample pairs read 0 sectors in 3
of 5 reps, and the r7 diskrate receipt measured the same shape at a 10 s window — the
probe would buy a noisy number at a hard latency price.

## 1. disk — write rate: since-boot average unchanged, instantaneous rate deferred with numbers

The live row is byte-stable from r7: `io_basis=since-boot
io_avg_since_boot=dm-0:9374197Bps/13983s io_avg_unavailable=tmpfs:not-a-block-device`
(battery run 20:33Z; `warn_pct=85 crit_pct=95` unchanged, no threshold touched). The
r2 note's rule — do not install a "better" percent without a measured write rate — was
already met in r7 by the average; this round adds no rate, by adjudication. Limitations
carried unchanged: the average counts every write to the device since boot (OS and
desktop included), is not fleet-attributable, and cannot see a burst.

## 2. tmux — per-session freshness: implemented, bounded, INFO-only

**Probe design.** For every session classified fleet-relevant (the r7 pane-cwd rule),
`probe_tmux` runs one `tmux display-message -p -t <session> '#{session_activity}'`
(`:1496-1502`, `run_timeout` call `:1497`) wrapped in `run_timeout` (`:344`) with
default bound `MORI_TMUX_TIMEOUT_S=2` (`:249`); rc 124 from the bound, a non-integer
answer, and a probe rc≠0 each yield `freshness=unavailable` with its reason
(`:1493`, `:1498-1508`), never an `idle=0` guess. A missing `timeout` binary refuses
the probe outright (`reason=no-timeout-bin`, `:1493`) rather than running a client call
that can block a wedged server forever. Foreign sessions are never probed (a foreign
quiet is not fleet evidence). `idle = NOW_EPOCH − session_activity`, clamped ≥0, graded
against `MORI_TMUX_IDLE_WARN_S` (default 3600, **local**) into the **INFO** finding
`TMUX_SESSION_IDLE` (`:1512-1516`) — a quiet pane is evidence, not proof, so a local
placeholder cannot flip the roll. Row: `freshness=… probed=… idle=…
freshness_unavailable=… idle_warn_s=…` (`:1539`).

**My arms** (fixture; the stub answers `display-message` from a file, sleeps only in
the hang arm):

```
fresh:   SURFACE tmux: ok (… relevant=1 foreign=0 unclassified=0 rule=pane_cwd_under_fleet_root freshness=ok probed=1 idle=0 freshness_unavailable=0 idle_warn_s=3600)      wall 342 ms
idle:    … freshness=ok probed=1 idle=1 … + FINDING TMUX_SESSION_IDLE severity=info obs=session=fx_session idle_s=7200 threshold_s=3600 threshold_label=local basis=session_activity
hang:    stub sleeps 8 s → whole gate wall 2328 ms; … freshness=unavailable probed=0 idle=0 freshness_unavailable=1 idle_warn_s=3600 reason=rc-124 + FINDING TMUX_FRESHNESS_UNAVAILABLE … reason=rc-124 timeout_s=2 probe=display-message
garbage: … reason=unparseable + FINDING … reason=unparseable-probe-output
rc-1:    … reason=rc-1 ; no-timeout-bin: … reason=no-timeout-bin + FINDING … unbounded_probe_refused
```

**Limitations.** The live host had **no tmux server** at every clock this round
(`tmux ls` rc 1; live row `SURFACE tmux: unavailable (cmd=tmux ls; rc=1; …)`), so
per-session freshness is fixture-proved only — the same shape as r7's relevance
finding. The idle number is a labeled-local placeholder, and `session_activity` is
updated by the server's own events, so a worker writing no output can read as idle.
The bound is **per call and enforceable, not nominal**: I measured a TERM-cooperative
8 s stub (bound fires at 2 s, rc 124, whole gate 2328 ms) and a TERM-ignoring 9 s stub
(the `-k 1` grace is spent, rc 137, whole gate 3369 ms) — so one wedged session costs
up to 3 s, `timeout_s=2` + 1 s grace, and a server wedging N relevant sessions costs up
to N × 3 s (the product shape `corpus/lessons/2026-10-15-probe-pricing-dwell-bounds-filter-drop.md`
§3 measures in isolation).

## 3. `*.round` symlink/dir invisibility: implemented with reason codes

**Probe design.** The state walk no longer filters on `-type f` (`:514`); the entry
list is sorted (`:523`, `LC_ALL=C sort || true` — the pipefail lesson applied to the
one new pipeline) and every entry is classified **before** any read: a symlink is
counted `state_unread_sym` with `WATCHDOG_STATE_ENTRY_UNREADABLE
reason=symlink-not-followed`
(`:529`, never followed — a link's target is arbitrary bytes and would let a foreign
integer into the rows), a directory `reason=is-directory` (`:534`), any other
non-regular entry `reason=non-regular` (`:539`). `state_rounds` keeps its r7 meaning
(regular files) so an existing state dir reads exactly as before, and the row splits
the total into reasons: `state_val_unreadable=<total>
state_val_unread_reasons=file:N symlink:N dir:N other:N` (`:587`).

**Before → after, my arms** (same fixture, one entry added):

```
r7 bytes:  symlink arm row ≡ base arm row — state_rounds=1 … state_val_unreadable=0 (invisible; scribe measured the same by normalized-row equality)
r8 bytes:  base     state_rounds=1 … state_val_unreadable=0 state_val_unread_reasons=file:0 symlink:0 dir:0 other:0
           symlink  state_rounds=1 … state_val_unreadable=1 state_val_unread_reasons=file:0 symlink:1 dir:0 other:0 + FINDING WATCHDOG_STATE_ENTRY_UNREADABLE … reason=symlink-not-followed entry=sym.round
           dir      state_rounds=1 … state_val_unreadable=1 state_val_unread_reasons=file:0 symlink:0 dir:1 other:0 + FINDING … reason=is-directory entry=dir.round
           dangling symlink: symlink:1, same finding class
           fifo (mkfifo pipe.round): other:1, reason=non-regular, whole gate 418 ms — the entry is CLASSIFIED, never opened, so the reader cannot block on it (the r7 `-type f` filter cannot simply be deleted for exactly this reason; census-impl classified instead — `corpus/lessons/2026-10-15-probe-pricing-dwell-bounds-filter-drop.md` §4)
```

**Live row** (20:33Z): `state_rounds=21 state_rounds_max=18 state_lag=0 state_ahead=0
state_cmp=21 state_val_unreadable=0 state_val_unread_reasons=file:0 symlink:0 dir:0
other:0` — 21 regular files, zero non-regular entries, so the new fields are all-zero
and every r7 field keeps its value. Three selftest cases (`:2247`, `:2257`, `:2275`).

## 4. memory-probe residuals: the three r7 limitations, each with a measurement

r7 §2 named three residuals; the impl header `:122-140` states the closure and the
memory-tester seat ran an independent arm battery. My own readings are noted where
they differ.

1. **Thresholds are local placeholders, not host-measured.** Now there is a measured
   window behind them: the impl sampled 21 PSI/avail readings 3 s apart
   (2026-10-15T20:09–20:12Z, `/tmp/r8m/mem-samples.log`): `psi_some_avg10` 0.00–0.39,
   `psi_full` 0.00–0.39, host `MemAvailable/MemTotal` 49–53%. My independent 60 s
   window (13 samples 5 s apart, 20:11:09–20:12:10Z, `/tmp/mori-r8-note/probes/host-mem-samples.txt`)
   read `psi_some` 0.03–0.65 and avail 50–54% — same magnitude, slightly wider. The
   placeholders sit 15–25× (PSI some: 10 vs ≤0.65 observed) and ~4.9× (avail floor 10%
   vs 49–54%) away from everything either window produced. They stay **labeled local**:
   a distribution is not a calibration, and one window is not a distribution.
2. **`memory.max` is `max` here → the closed-container ratio never exists.** Measured
   scope census (impl): 108 `memory.max` files walked — 107 read the literal `max`,
   exactly 1 numeric (`system.slice/polkit.service` = 33554432 B), 0 unreadable — so the
   fill ratio is constructible in 1 of 108 scopes and not in the fleet's user slice.
   The live scope-local substitute now exists: `memory.peak` is read (`:876-905`,
   row `:925`) with
   its source and `mem_peak_anchor` (the scope directory mtime — a cumulative
   high-watermark is comparable only within its cgroup instance; the nearest *free*
   anchor, not the instance's exact creation time). Live: slice
   `mem_peak=28812898304 mem_peak_source=ok mem_peak_anchor=1792082289`, unchanged across
   the whole window. My arms drive every source state: ok / `shape-refused` (literal
   `max` never echoed as bytes) / `unreadable` / `absent`; two selftest cases.
3. **The fixture arms were arithmetic proofs, not this host's distribution.** The two
   windows above are now this host's own pressure record *while a 32-seat wave ran*
   (host avail 49–54%, PSI some ≤0.65, slice peak constant 28812898304 = the service's
   28801970176 in the same window), so the fixture arms no longer stand alone. The
   numeric-`memory.max` arm remains fixture-only (see (2)) — named, not claimed.

## Verdict machine at the frozen pair (all numbers first-hand, 20:32–20:39Z)

| Check | Result (verbatim tail) | Exit |
|---|---|---|
| `bash tools/mori-census.sh --selftest` | `MORI_CENSUS_SELFTEST: PASS (56 cases, 56 passed, 0 failed)` (was 45) | 0, stderr 0 B |
| `bash tools/mori-silence-cases.sh` ×2 | `MORI_SILENCE_CASES: matched=28 total=28` both | 0, stderr 0 B |
| `bash tools/mori-census.sh` live ×2 | `MORI_CENSUS: DRIFT (findings=15 drift=14 unavailable=1 surfaces=7)` both | 1, stderr 0 B |
| case ledger, r7 → r8 | +11 labels, **−0** (comm on sorted label lists: removed_count=0) | — |
| field-set diff, one identical fixture | added exactly `freshness freshness_unavailable idle idle_warn_s mem_peak mem_peak_anchor mem_peak_source probed state_val_unread_reasons`; removed **none** | — |
| field-set diff, live rows (same pinned root) | added `mem_peak mem_peak_anchor mem_peak_source state_val_unread_reasons`; removed **none**; normalized row diff shows only mutable values (`age_s`, counters, `ts`) | — |
| interleaved old-vs-new, same fixture (n=5 pairs) | old median 363 ms, new median 377 ms → **Δ +14 ms** | — |

The 11 new cases: `watchdog: symlink *.round counted with reason, never followed` ·
`watchdog: directory *.round counted with reason` · `watchdog: all four non-value
classes counted by reason` · `tmux: fresh fleet session -> probed, not idle` · `tmux:
idle fleet session -> INFO finding, foreign session not probed` · `tmux: non-integer
activity -> freshness unavailable, never idle=0` · `tmux: activity probe rc!=0 ->
freshness unavailable reason=rc-1` · `tmux: sleeping probe is bounded -> rc-124
unavailable, no hang` · `tmux: no timeout binary -> freshness refused, never run
unbounded` · `cgroup: scope high-watermark read with its instance anchor` · `cgroup:
non-integer peak refused, bytes never echoed`.

**Oracle: unchanged bytes, no re-baseline needed.** `tools/mori-silence-cases.sh`
stayed at `448f7723…` throughout; the 28 ids and want-sets are untouched, and it
returned `matched=28 total=28` exit 0 twice at the new census bytes (the census's new
row fields are additive and every value they carry is fixture-stable in the oracle's
trees: the peak anchor is a directory mtime, the tmux activity stub is a file). The
pinned pair for this round is therefore (census `390ab9cd…`, oracle `448f7723…`).

## Defects and open items measured this round

1. **Still-open hang class (pre-existing, not an r8 regression; the `*.round` case of
   it IS closed).** The round's latency bound covers the new tmux client call, not the
   older reads: with `MORI_DISKSTATS` or `MORI_UPTIME` pointed at a writer-less FIFO the
   gate prints its header and never returns a verdict — measured by me at the r7 bytes
   (external 10 s cap: rc 124, 0 verdicts, both arms; `shakedown/fifo-r7-{dsk,up}.out`)
   and again at the r8 bytes (external 15 s cap: rc 124, 15003 ms / 15008 ms, 0
   verdicts; `after/60-fifo-*.out`). A FIFO **`*.round` entry** is no longer this class:
   the classifier counts it `other:1 reason=non-regular` and never opens it (whole gate
   418 ms, `after/90-fifo-round.out`), which is the trap the r7 `-type f` filter could
   not have been simply deleted for. The hang-guard seat tests the same input-file arms
   with a 150 s cap. Not fixed this round; named so the bound is not over-read.
2. **One-off selftest nondeterminism seen at the frozen prefix.** Of my 16 selftest
   runs at `390ab9cd…` (one in the battery, 7 around `20:25Z`, 8 repeats after the
   battery), one failed with `FAIL drift: CGROUP_OOM_KILL: missing match
   |FINDING CGROUP_OOM_KILL|` (exit 1, 55/56) and 15 passed; the scribe recorded a
   *different* single failure (missing state dir) at the same prefix
   (`.ufo/round-8/goal-wave/measurements-ledger.md` §"Revision history"). Both were
   observed while the census-impl seat was still writing the file
   (`20:21Z`–`20:25Z`); every later run at the frozen bytes was green (8/8 in the
   repeat set, SHA re-verified unchanged after the set). Not attributed to a code path
   in this note; the round's "selftest all-pass" claim rests on the frozen-bytes runs.
   **Disposition (r9, 2026-10-15).** Root-caused to the `printf | grep -q` SIGPIPE
   race: `grep -q` exits on its first match and closes the pipe while the forked
   `printf` producer is still writing line-by-line; the producer dies of SIGPIPE
   (rc 141), `pipefail` makes that rc the pipeline's, and the `|| miss=` records a
   false `missing match` on a random case (`corpus/knowledge/selftest-flake-r9.md`
   §1–§1c reproduces this item's exact message template with a different case; class
   lesson `corpus/lessons/2026-10-15-selftest-grep-sigpipe-race.md`). Fixed at census
   sha256 `1c49238a…` (+21/−7, hunks confined to `run_selftest()`): all five harness
   live-pipe greps (`:1771`/`:1773`/`:1779`/`:1783`/`:1809` at r5 numbering) now grep
   one captured `$OUT_FILE` — no producer remains to SIGPIPE. Verified: selftest
   `PASS (56 cases, 56 passed, 0 failed)` exit 0 (my run at the new bytes, sha
   re-verified unchanged around it); the note's two ≥20-run batteries (20 + 20, one
   under 4-CPU-hog load) read 0 flakes; its oracle run at the new bytes reads
   `matched=28 total=28` with `448f7723…` byte-frozen. Honest scope: r8's specific
   failures are attributed by mechanism and symptom, not re-run; a symptom-identical
   second cause (reading the census while it is being written — this item's
   observation window) is addressed by the note's battery rule, not by the code fix;
   `:1322` (production silence path) is the same race class, untouched under the
   production byte-freeze — named debt, not closure.
3. **Doc nit:** the header `:76-78` points at
   `corpus/knowledge/surfaces-r7.md` (`Honest residuals`) — that section name is in the
   r7 *report* (`.ufo/reports/round-7/mori-goalwave.md:42-48`); the note carries
   "Limitations" sections. Pointer accuracy only; the four residuals themselves are
   correctly identified.
4. **Gate-level wall time is not a decision instrument under load** (both seats'
   measurements above, >5 s drift at wave load). The only usable cost numbers are the
   isolated ones; the round's adjudication says so explicitly.

## What this note does not claim

- No remediation, no kill/restart, no systemctl, no host config change; every live row
  is read-only and pinned to one mutable clock, and all fixtures live under `/tmp`.
- The disk deferral's numbers are single-host, one-window measurements under wave
  load; they bound the dwell's cost, they do not measure any fleet's write behavior.
- tmux per-session freshness is **fixture-proved only** this round (no tmux server on
  this host at any clock); `TMUX_IDLE_WARN_S=3600` is a labeled-local placeholder and
  fires INFO only.
- `mem_peak_anchor` is the scope directory's mtime — the nearest free anchor, not the
  cgroup instance's precise creation time; peaks are comparable within an instance,
  not across one.
- The memory thresholds remain local placeholders; the two sampled windows bound what
  this host produced during the wave, nothing more, and the numeric-`memory.max` arm
  stays fixture-only on this host.
- No claim that the *generic* read paths (`cap`, `read_file`) are latency-bounded —
  see defect 1; only the tmux client call is bounded, and that bound is what I measured
  (2328 ms whole-gate wall against an 8 s-hanging stub, `timeout_s=2`).
- The r2 note's Gaps sections and other seats' files are owned by their seats; this
  note only points at them.