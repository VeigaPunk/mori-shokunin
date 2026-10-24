# Lesson — a behavioral baseline is only as strong as its declared volatile-field contract

date: 2026-10-15 · lane: mori-shokunin · round: 10 · source seat: lessons-distiller

Measured against the entering round-10 bytes `tools/mori-census.sh`
sha256 `1c49238a7fd87277151ff5776acfb4d62fadd9d69764a02f0ede03ef0d3902d2`
(`VERSION=census-r5`) and the frozen oracle
`448f77238c73a5c929a898dad0f0c495fd2a66cc4b90a00ae84ede69a86beeb5`.
The pin/drift *implementation* landed mid-round and kept moving; its checks are pinned
separately at `c37b2ee6…`, `6d61ff16…` and `62e76cfd…` (named where used, §Limits).
All raw logs are ephemeral under `/tmp/mori-r10-lessons/`; the durable
cross-references are the committed receipts named per section.

## The lesson

A "pin the output, diff it later" baseline is **unusable as-is** on any gate whose
output contains the clock it was read at, and **vacuous** if you fix that by masking
lines instead of fields. Between those two failures sits the only workable design: a
baseline is (raw artifact) + (an explicit, per-field, named volatile set) +
(the derivation window and host it was derived on). None of the three can be omitted,
and the volatile set is empirical — it must be measured, not guessed.

Measured here, at the bytes above:

- A **live** census pair 72 s apart differs on **32 of 33 lines**; the only stable
  byte in the whole output is the verdict line. So the naive baseline fails on
  essentially every field and on every line, on hardware that is working correctly.
- A **pinned fixture** run twice is **byte-identical** (raw diff = 0 lines) with no
  mask at all. The churn is therefore the *inputs* (this host's clock and counters),
  not nondeterminism in the gate. Proof that `ts=` is an input and not a behavior:
  `MORI_NOW_EPOCH=1792100000` produced exactly `ts=2026-10-15T21:33:20Z` in the
  header of every fixture run.
- Masking at **line** granularity destroys the detector: 32/33 live lines contain a
  volatile-looking token, including **all 15 `FINDING` lines** (every finding carries
  `ts=`). A "drop lines that look volatile" rule keeps 1 of 33 lines — the verdict —
  which is a baseline that can never fire.
- Masking at **field** granularity keeps detection power: one fixture fact changed in
  place (a wave settled) is still named, hunk by hunk, by the masked diff (below).

## What was measured

### 1. The churn, three live runs (`/tmp/mori-r10-lessons/live-{1,2,3}.out`)

```
run1 rc=1 wall=69s   MORI_CENSUS: DRIFT (findings=15 drift=14 unavailable=1 surfaces=7)
run2 rc=1 wall=47s   MORI_CENSUS: DRIFT (findings=15 drift=14 unavailable=1 surfaces=7)
run3 rc=1            MORI_CENSUS: DRIFT (findings=15 drift=14 unavailable=1 surfaces=7)
```

- lines per run: 33; run1 vs run2: `comm -12 <(sort live-1.out) <(sort live-2.out)` = **1**
  identical line (the verdict), `diff live-1.out live-2.out | grep -c '^[<>]'` = **64**
  (32 changed line pairs).
- distinct field tokens in the output: **79**
  (`grep -oE '[a-z_]+=' live-1.out | sort -u | wc -l`).
- of those 79, exactly **6** changed value between run1 and run2, 71 did not:
  `age_s current host_mem_avail_pct io_avg_since_boot mtime_age_s ts`.

### 2. The mask, and the fact that it holds out-of-sample

The six classes above, masked as a *frozen* filter (derived on the pair run1–run2,
then applied unchanged to every other pair):

```awk
# /tmp/mori-r10-lessons/mask.awk  (verbatim)
{
  s=$0
  gsub(/ts=[0-9TZ:.-]+/,            "ts=@", s)
  gsub(/age_s=[0-9]+/,              "age_s=@", s)
  gsub(/mtime_age_s=[0-9]+/,        "mtime_age_s=@", s)
  gsub(/io_avg_since_boot=[^ ;)]+/, "io_avg_since_boot=@", s)
  gsub(/current=[0-9]+/,            "current=@", s)
  gsub(/host_mem_avail_pct=[0-9]+/, "host_mem_avail_pct=@", s)
  print s
}
```

```
$ diff -q live-1.masked live-2.masked   # in-sample, the pair the mask was derived from
IDENTICAL
$ diff -q live-2.masked live-3.masked   # holdout: different pair, same frozen mask
IDENTICAL
```

Both 32-line churn sets normalize to identical. Two runs of the same *shape* are
`MORI_DRIFT: none` under this mask — and that is a real, falsifiable statement about
this host at this clock, not a tautology, because the same mask still exits 1 on a
genuine change (next section).

### 3. Detection power is retained (deterministic fixture, in-place mutation)

Fixture built from the census's own env contract (`MORI_NOW_EPOCH`,
`MORI_SHOKUNIN_ROOT`, `MORI_WAVES_DIR`/`MORI_STATE_DIR`/`MORI_WATCHDOG_LOG`,
`MORI_CGROUP_*`, `MORI_MEMINFO`, `MORI_DISKSTATS`/`MORI_UPTIME`,
`MORI_DF_BIN`/`MORI_PGREP_BIN`/`MORI_JOURNALCTL_BIN`/`MORI_TMUX_BIN`/`MORI_GIT_BIN`
stubs, clock pinned) — the recipe is the same env block the census's own selftest
uses at `tools/mori-census.sh:1736-1768` (entering bytes `1c49238a…`).

```
# two runs, nothing changed:
$ diff fx-a1.out fx-a2.out | grep -c '^[<>]'
0                      # raw diff empty — inputs pinned ⇒ gate is deterministic
# then one fact changed in the same tree (waves/wa/swarm-registry.json:
#   "closed":false → true, mtime refreshed), same fixture, same clock:
$ diff fx-a3.masked fx-a4.masked ; echo "exit=$?"
3c3
< SURFACE waves: drift (... total=2 settled=1 unsettled=1 aged_unsettled=1 empty=0 ...)
---
> SURFACE waves: ok (... total=2 settled=2 unsettled=0 aged_unsettled=0 empty=0 ...)
20d19
< FINDING WAVE_UNSETTLED_AGE severity=warn obs=wave=wa age_s=@ threshold_s=7200 reg=1 disp=0 run=0 settle=0 ts=@ script_sha256=1c49238a...
22c21
< MORI_CENSUS: DRIFT (findings=4 drift=3 unavailable=2 surfaces=7)
---
> MORI_CENSUS: DRIFT (findings=3 drift=2 unavailable=2 surfaces=7)
exit=1
```

The masked diff names the changed surface tokens, the vanished finding, and the
verdict-count change — exactly the three places the fact moved. `age_s=@` inside the
dropped finding line shows the mask is field-scoped, not line-scoped.

### 4. The volatile set is not a property of the field name — it is a property of the window

Three datums at different clocks, all on the live host:

| field(s) | clock A | clock B | Δt | verdict |
|---|---|---|---|---|
| `ts= age_s= mtime_age_s= io_avg_since_boot= current= host_mem_avail_pct=` | live-1 21:50:07Z | live-2 21:51:19Z | 72 s | churned |
| `segfault=` (journal class count) | `residuals-r8-20261015T2040Z-live.log`, 20:41:18Z: `kill_signal=1 segfault=104` | my run, 21:50:07Z: `kill_signal=1 segfault=225` | ~69 min | churned (**not** covered by the mask above) |
| `mem_peak=` / `mem_peak_anchor=` | `residuals-r8-20261015T2040Z-memory.log:16` (20:40:20Z): `28812898304`/`1792082289` | same file `:39` (20:47:03Z): `28801970176`/`1792097058` | ~7 min | churned, and the anchor moved with it (cgroup instance recreated) |
| `launch_epoch=1792039857`, `state_rounds=21 state_rounds_max=18`, `kill_signal=1`, `mem_peak` (in my window) | r8 live receipt 20:41:18Z | my run 21:50:07Z | ~69 min | stable |

Consequences, and they are the operative part of the lesson:

- A mask derived from **one** 72 s window is **incomplete**: it leaves `segfault=`
  (and by shape the other journal `count=`-class fields) unmasked, so a baseline pinned
  at 21:50 would go red inside the hour on a field that is not gate behavior at all.
- Conversely, fields that look "counter-shaped" were **stable across ~70 minutes**
  here (`state_rounds`, `launch_epoch`, `kill_signal`) — so "mask everything numeric"
  is not the rule either; it is measurably over-broad in this window and would hide
  real lifecycle facts.
- Therefore the contract must record: which fields are masked, **why** (churn class),
  **on what window and host they were measured**, and **when they must be re-derived**.
  A mask with no derivation record is indistinguishable from a mask that hides
  regressions.
- Where a value carries an instance anchor (`mem_peak_anchor`, `mem_peak_source`) the
  anchor lets a detector distinguish "the value moved because the instance was
  recreated" from "the value moved inside one instance". That is the same
  instance-comparability rule the lane already documents for `mem_peak`
  (`SKILL.md`, "cgroup `mem_peak=`… comparable only within one cgroup instance").

### 5. The exit contract needs a third value

Masking solves *churn*; it does not solve *absence*. A baseline file can be missing,
truncated, or written by a different revision, and a two-valued contract (0 clean /
1 drift) forces "cannot compare" to masquerade as "clean" — the exact failure shape
this lane already has two lessons about
(`corpus/lessons/2026-10-15-oracle-honesty-crash-masking.md`: a masked crash and a
genuine repair produce the identical tally;
`corpus/lessons/2026-10-15-errexit-pipefail-silent-crash.md`: a verdict machine that
dies silently reads as agreement). The round-10 contract's `--drift` exit 2 for
baseline-missing is the correct shape: the third value is what makes exit 0 mean
"compared and equal", not "compared nothing".

## Applying it

1. **Store the raw capture, not the mask output.** The artifact a human reads must be
   the verbatim gate output; the mask belongs to the comparison step (it is a
   *reading*, not a *record* — same principle as the r9 note's `OUT_FILE` capture:
   keep the bytes, then assert over them).
2. **Mask per field, never per line, and say so in the artifact.** A line-level rule
   keeps 1 of 33 lines here; a field-level rule keeps 32 and still fires on change.
3. **Pair the baseline with its derivation record**: mask list, churn tier, window,
   host, and the gate SHA. Re-derive deliberately at intervals, and treat re-pinning
   as a recorded act with a reason — the failure mode to avoid is re-pinning to make
   a red baseline green (the same shape as weakening an oracle's assertions).
4. **Enumerate the blind spots out loud.** Every masked field is a place where a real
   regression is invisible. Report the masked set in the drift output and in the
   index, so a reader knows what the "none" did not look at.
5. **Keep the fast tier small.** Here 6 of 79 fields (~8%) carried all the churn in a
   72 s window; masking those 6 was sufficient for shape equality and preserved
   detection. A mask that grows past the measured churn set is masking behavior.

## Limits of this note

- Two windows, one host, one gate revision. The churn tiers in §4 are observations of
  *this* host at *these* clocks; `segfault=` and `mem_peak=` are counter/watermark
  fields whose churn depends on host episodes, so the honest statement is "measured
  churning within X on this host", never "always volatile". A mask for another host
  must be re-derived there.
- The mask in §2 was derived from one pair and validated on one holdout pair. That is
  a cross-validation, not a proof of sufficiency: §4 already exhibits a field
  (`segfault=`) that this mask does not cover once the window widens ~60×.
- The fixture in §3 is minimal (2 wave dirs, no lanes resolvable — the stubbed `git`
  yields `unavailable` lane rows). It demonstrates that masked output is deterministic
  under pinned inputs and that a state change is still named; it does not exercise the
  silence/lane surfaces, whose rows also contain `age_s=`/`launch_epoch=`.
- The implementation of the round-10 pin/drift modes is **not** this seat's artifact
  (`tools/mori-census.sh` is pin-impl's), but its behavior was checked first-hand while
  this note was being finalized, because the contract's *mechanism* is this note's
  subject. The file moved under the measurement: `1c49238a…` → `72da04b8…` (docs only
  at ~22:11Z — header contract at `:145-190` plus usage text, `main()` still rejected
  both flags: measured `mori-census: unknown argument: --pin`, exit 2, no file written)
  → `c37b2ee6…` (code: `--pin` wired at `:2682`, `DRIFT_COUNTER_KEYS` at `:1636`) →
  `6d61ff16…` → `62e76cfd…`. The battery below ran at `6d61ff16…` with the sha identical
  before and after all six probes; the two pivotal cases were re-run at `62e76cfd…`
  with the same results, and the unchanged-state control reads `none`/exit 0 before the
  mutations and again after restoration.

  | probe (fixture of §3; control = unchanged state) | result | exit |
  |---|---|---|
  | `--pin <path>` | baseline written; header carries `volatile_fields=…` | 0 |
  | `--drift <path>`, nothing changed | `MORI_DRIFT: none` | 0 |
  | `--drift` with a missing baseline | `mori-census: --drift baseline missing: …` | 2 |
  | wave settled (`"closed":false→true`) | `MORI_DRIFT: -FINDING:WAVE_UNSETTLED_AGE SURFACE:waves` | 1 |
  | `warn_pct` 85→90 inside one line | `MORI_DRIFT: warn_pct` | 1 |
  | live `--pin`, then live `--drift` 25 s later | `MORI_DRIFT: none` | 0 |

  The three exit values and both report grammars (a changed key; a removed line id)
  behave as the round's claim states. The live pair spanned a mid-iteration revision
  change (`6d61ff16` → `62e76cfd`) and still read `none` — consistent with the design's
  behavioral (not revision-bound) comparison, but that pair is not pinned to one sha.
  A baseline pinned at `c37b2ee6…` compared at `6d61ff16…` likewise read `none`.
- A consequence of the declared counter class, now **measured** rather than inferred:
  masking counters absorbs churn *and* count-only change. Adding an empty wave
  directory to the §3 fixture moves a real output field —
  `total=2 settled=1 unsettled=1 aged_unsettled=1 empty=0` →
  `total=3 settled=1 unsettled=1 aged_unsettled=1 empty=1`, plainly visible in a raw
  diff — and `--drift` reports **`MORI_DRIFT: none` exit 0**, because `total` and
  `empty` are both in `DRIFT_COUNTER_KEYS` (measured at `6d61ff16…` and at
  `62e76cfd…`). So "none" means "no *unmasked* change", not "output identical": a
  count-only regression behind an existing line is silent by construction. Sized
  against this output, the counter class covers **37** of the 79 field tokens (`pids
  state_rounds state_rounds_max total settled unsettled aged_unsettled empty
  age_unreadable oom_kill kill_signal segfault unit_failure oom high max
  local_oom_kill silent progressing progressing_weak young not_open unavailable
  skipped findings drift surfaces reg disp run settle rowb_files count state_lag
  state_ahead state_cmp state_val_unreadable` — every one of them measured
  **unchanged** over the 72 s window, and `state_rounds`/`kill_signal` unchanged over
  ~70 min), i.e. ~47% of the schema is declared blind spot while the measured windows
  exhibit 7 churning fields. That is a defensible stability-versus-sensitivity trade,
  not a defect; the constructive follow-up, if the lane wants count visibility, is an
  info-only companion listing of masked-key changes — kept out of the drift verdict so
  the verdict keeps meaning "a non-volatile field moved".
- A live pinned baseline will legitimately go red as the fleet changes (a wave settles,
  a lane launches). That is baseline *aging*, not masking failure, and it is the
  re-pin policy of §3 of "Applying it" — deliberately not solved here.