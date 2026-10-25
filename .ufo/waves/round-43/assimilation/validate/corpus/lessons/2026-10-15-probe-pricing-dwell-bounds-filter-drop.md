# Lesson — a deferred probe has four prices the requesting code never shows: the counter's found-ness, the marginal wall time, the enforceable bound, and the filter's drop set

date: 2026-10-15 · lane: mori-shokunin · round: 8 · source seat: lessons-distiller (flash wave)

Measured on host kernel `7.2.3-arch1-3`, 2026-10-15T20:07–20:20Z, inside the round-8
32-seat wave (`/proc/loadavg` 69 → 148 on 32 cores — it doubled inside a single
2.5-minute measurement window). Instruments: the round-7 census bytes pinned to a /tmp
copy (`git show HEAD:tools/mori-census.sh` → sha256
`c7c3569b842ab3911cbfdf415eb7023766c950c60f354af95f6a4f020b5671af`, `VERSION=census-r4`,
2004 lines; run with `MORI_SHOKUNIN_ROOT` pinned so every arm of a comparison saw
identical probe work — the lane root for the A/B/C wall-time run, the fleet root for the
before/after fixture pair, so the pinned copy's absolute times are *not* comparable to
the live gate's, only arm-to-arm within one run); the round-8 working bytes
`7f3fcacfa4420bf6de7376eaec29d08bedef90e43d25ee312a52439fa1bb20f4` (2373 lines — a
verified snapshot, **not** the round's final bytes: both implementing seats were still
editing and the census changed six times inside this seat's 13-minute window —
`c7c3569b` → `a63a6848` → `d7523248` → `30f44be6` → `3fded0cc` → `b144af82` →
`7f3fcacf`); the
oracle `tools/mori-silence-cases.sh` sha256
`448f77238c73a5c929a898dad0f0c495fd2a66cc4b90a00ae84ede69a86beeb5`, unchanged at every
check; the census changed once more as this note closed (`390ab9cd…` at 20:21Z), so every
line number below is valid **at `7f3fcacf…` only**. Everything read-only; the only
writes are `/tmp/mori-r8-lessons/*`. Detection and report only — nothing here
remediates, and nothing here is the verdict on the round's closure.

Context: round 8 buys the measurements round 7 deferred (instantaneous disk write rate,
tmux per-session freshness, `*.round` symlink/dir invisibility, the memory-probe
residuals) under an explicit budget rule — *implement iff the 0.2 s variant adds < 50 ms
median wall time; otherwise record a deferral that carries the measured number*. This
note distils the measurement-cost lesson those four purchases instantiate; the one
round-level claim it also carries (§2) was reached independently by this seat and by the
implementing seat.

## The lesson

Round 7's lesson asked which measurements are **free** (source-aggregated → one read; a
rate the source does not maintain → a dwell). Round 8 shows that when you pay, the price
is **four numbers, none of which appears in the code that asks for the measurement**:
each is a property of the instrument, not of the intent, and each failed differently in
this round's own probes.

1. **Found-ness — a counter you did not find reads zero.** A probe that computes
   `(s2 - s1) / elapsed` from a lookup that matched nothing prints a confident `0 B/s`.
   The zero of "found nothing" and the zero of "nothing happened" are the same bytes
   unless the probe says which one it is. (Measured below: my own first two-sample
   attempt.)
2. **Marginal wall time — measured inside one span or in pairs; consecutive medians on
   a loaded host measure the host.** In a one-shot gate the only honest question is what
   the dwell adds to *this* run, and that is only resolvable when the instrument's own
   noise is below the budget. Measured here: the gate's wall time moved by seconds while
   a 50 ms budget was being tested. The dwell itself priced inside a controlled span:
   **serial = +212 ms median, overlapped behind work already running = 0 ms median.**
   The cost belongs to the scheduling, not to the window.
3. **The enforceable bound — never the nominal one, and its exit-code vocabulary is
   larger than the comment says.** `timeout 0.3` reported its bound (`rc=124`) at
   **1510 ms** against a peer that ignores SIGTERM; `timeout -k 1 2` enforced it
   (3007 ms, `rc=137`). Per-call bounds multiply in a loop (3 sequential bounded calls
   measured 9032 ms), and the grace kill's shell diagnostic is construct-dependent
   (0 B stderr inside the census's `$(...)` construct — measured).
4. **The filter's drop set — an enumeration's count means "entries that survived the
   filter".** `find -maxdepth 1 -type f -name '*.round'` over 9 `*.round` entries
   returned 4: a symlink→file, a dangling symlink, a symlink→dir, a directory and a fifo
   were invisible. The filter cannot simply be deleted — reading the fifo blocks
   (measured) — so the fix is to keep the filter and count what it drops *by reason*.

The round-level form of (2): **a budget rule of the shape "implement X iff cost(X) < T"
is decidable only if the instrument's noise is below T.** Measured here the gate's
end-to-end wall time was not such an instrument for a 200 ms effect, let alone a 50 ms
one: identical work ranged 9249–32345 ms across nine interleaved runs. The implementing
seat reached the same conclusion from its own arm (`tools/mori-census.sh:94-97` at
`7f3fcacf`): *"Gate-level wall time could not resolve a 200 ms effect under today's load
(medians of 5 interleaved runs: r7 base 13583 / +reads 12551 / +0.2 s 16272 / +1.0 s
17438 ms, spread >10 s) and is reported as unusable, not as the decision."* Two
independent measurements, same call: the isolated/in-span measurement is the decision
instrument, and the gate-level one is evidence that the host was busy.

## What was measured (verbatim, 2026-10-15T20:07–20:20Z, all read-only)

### 1. Found-ness: the 0 that was an artifact, and the 0 that was real

My first two-sample disk probe printed, on every window, before I noticed why:

```
target_source=/dev/mapper/root[/@home] resolved= uptime_s=12819.09
window=0.2  elapsed_us=208634   sectors_delta=0      bytes/s=0
window=0.2  elapsed_us=210763   sectors_delta=0      bytes/s=0
window=1.0  elapsed_us=1010894  sectors_delta=0      bytes/s=0
```

`findmnt -no SOURCE` returns the btrfs subvolume form `/dev/mapper/root[/@home]`;
`readlink -f` on that literal resolves to the empty string; `awk '$3==""'` matched no
line; and `0 sectors / elapsed` is a well-formed zero. With the suffix stripped and the
device resolved (`readlink -f /dev/mapper/root` → `/dev/dm-0`) the counter exists and
advances:

```
target=dm-0 counter_start=244335112 load=145.68 105.78 69.18
reference window=3.0s delta=12576 sectors rate=2132171 Bps
...
counter_end=244353768 load=146.99 106.71 69.68
```

The same rule is why the r7 disk row already prints `io_avg_unavailable=<dev>:<reason>`
— a probe that can report a number must first be able to report that it could not find
the counter.

The *real* zeros underneath that fix are a separate finding, and they are the
resolvability argument for the deferred window. Ten samples of `sleep 0.2` on dm-0,
taken while the counter demonstrably advanced 18,656 sectors (~9.5 MiB) over the same
period:

```
sample= 1 nominal_us=200000 measured_us=219172   over_pct=  9 delta_sectors=0      rate_measured_elapsed=0 Bps
sample= 2 nominal_us=200000 measured_us=206601   over_pct=  3 delta_sectors=0      rate_measured_elapsed=0 Bps
sample= 3 nominal_us=200000 measured_us=213817   over_pct=  6 delta_sectors=2192   rate_measured_elapsed=5248899 Bps
sample= 4 nominal_us=200000 measured_us=218888   over_pct=  9 delta_sectors=24     rate_measured_elapsed=56138 Bps
sample= 5 nominal_us=200000 measured_us=217793   over_pct=  8 delta_sectors=0      rate_measured_elapsed=0 Bps
sample= 6 nominal_us=200000 measured_us=217991   over_pct=  8 delta_sectors=840    rate_measured_elapsed=1972925 Bps
sample= 7 nominal_us=200000 measured_us=215121   over_pct=  7 delta_sectors=272    rate_measured_elapsed=647375 Bps
sample= 8 nominal_us=200000 measured_us=220564   over_pct= 10 delta_sectors=1720   rate_measured_elapsed=3992673 Bps
sample= 9 nominal_us=200000 measured_us=226227   over_pct= 13 delta_sectors=200    rate_measured_elapsed=452642 Bps
sample=10 nominal_us=200000 measured_us=221907   over_pct= 10 delta_sectors=0      rate_measured_elapsed=0 Bps
```

4 of 10 samples read `0 B/s` on an actively-writing device, and the non-zero ones span
56 kB/s to 5.2 MB/s — a 0.2 s window aliases write bursts. Two smaller numbers in that
table are also load-bearing: the *measured* elapsed (`sleep 0.2` → 206.6–226.2 ms,
+3…+13% over nominal) must be the divisor; using the nominal window inflates every rate
by 3–15%.

### 2. Marginal wall time: pairs or spans, never consecutive medians

(a) The gate as a clock, r7 bytes, live, three consecutive runs of identical work:
`15566 / 16921 / 17790 ms`. Pinned bytes, interleaved A/B/C (A = census alone, B =
census + trailing serial `sleep 0.2`, C = `sleep 0.2` overlapped with the running census):

```
A census alone                       : 14982 11945 19228
B census + trailing serial sleep 0.2 : 9249 10168 28535
C sleep 0.2 overlapped with census   : 10527 15799 32345
paired B-A per pair                  : -5733 -1777 9307
paired C-A per pair                  : -4455 3854 13117
spread_of_A=7283 ms  spread_of_C=21818 ms
load_before=75.56 62.45 48.72 / load_after=147.83 90.47 60.80
```

B came out **5733 ms faster** than A in the first pair. A 200 ms dwell cannot be priced
in that signal; the run also shows why pairing is not a cure by itself when the host
load more than doubles mid-measurement.

(b) Inside one span the same dwell is unambiguous. A busy-loop "pass" of ~1000 ms
(clock = bash builtin `$EPOCHREALTIME`, no forks), interleaved solo/serial/overlap,
5 rounds at load 145.77, reporting `total − pass_internal`:

```
solo     pass_internal_ms=1001  total_ms=1001  total_minus_pass=0
serial   pass_internal_ms=1000  total_ms=1206  total_minus_pass=206
overlap  pass_internal_ms=1003  total_ms=1003  total_minus_pass=0
solo     pass_internal_ms=1000  total_ms=1000  total_minus_pass=0
serial   pass_internal_ms=1001  total_ms=1217  total_minus_pass=216
overlap  pass_internal_ms=1000  total_ms=1000  total_minus_pass=0
solo     pass_internal_ms=1000  total_ms=1000  total_minus_pass=0
serial   pass_internal_ms=1002  total_ms=1217  total_minus_pass=215
overlap  pass_internal_ms=1006  total_ms=1006  total_minus_pass=0
solo     pass_internal_ms=1006  total_ms=1006  total_minus_pass=0
serial   pass_internal_ms=1000  total_ms=1212  total_minus_pass=212
overlap  pass_internal_ms=1000  total_ms=1007  total_minus_pass=7
solo     pass_internal_ms=1000  total_ms=1000  total_minus_pass=0
serial   pass_internal_ms=1000  total_ms=1205  total_minus_pass=205
overlap  pass_internal_ms=1000  total_ms=1000  total_minus_pass=0
```

Serial: +212 ms median (205/206/212/215/216). Overlapped: 0 ms median (0/0/0/0/+7) —
the dwell hides behind work already on the critical path, provably, while load is at
4.5× core count. The implementing seat's isolated numbers agree on the serial side
(`tools/mori-census.sh:85-90` at `7f3fcacf`: "pure `sleep 0.2`: min 202 median 206 max
215; reads + 0.2 s dwell: min 210 median 229 p90 240 max 265", extra reads alone "min 5
median 16 p90 27 max 32") and its conclusion — stay deferred, minimum 4.2× the 50 ms
budget — is sound **for the serial scheduling it measured**. The refinement this
measurement adds is that the price it measured is the dwell's serialization, not the
window's: a bracketed variant trades the dwell for the two extra reads (their isolated
arm: 16 ms median for both), and the binding constraint on a 0.2 s window turns out to be
§1's aliasing, not its cost.

### 3. The bound: nominal, enforced, and the vocabulary

```
timeout (GNU coreutils) 9.11
baseline: sleep 0.3                                  rc=0      305 ms
timeout 0.3 sleep 5   (cooperative peer)             rc=124    307 ms
timeout 0.3 stub: trap TERM, sleep 1.5               rc=124   1510 ms
timeout -k 0.2 0.3 stub: trap TERM, sleep 1.5        rc=137    509 ms
timeout 1 false       (peer rc 1)                    rc=1        5 ms
timeout 1 sh -c exit 2 (peer rc 2)                   rc=2        9 ms
timeout 0.5 sh -c exit 1 (absent-server shape)       rc=1        7 ms
overhead: 200 x "timeout 5 true": 746 ms total, 3730 us each
```

`timeout 0.3` on a stub that traps TERM returned **rc 124 at 1510 ms**: the call only
returned when the stub itself exited at 1.5 s — the bound was reported, not enforced.
The r8 census uses the `-k` form (`tools/mori-census.sh:344-348` at `7f3fcacf`:
`CAP_OUT=$("$TIMEOUT_BIN" -k 1 "$secs" "$@" 2>&1)`), whose measured shape at the
default `TMUX_TIMEOUT_S=2` is:

```
cooperative: sleep 9 (bound spent, grace not)              rc=124   2013 ms
TERM-ignoring stub: sleep 1.5 (ends by itself)             rc=0     1509 ms
TERM-ignoring stub: sleep 9 (bound + grace spent)          rc=137   3007 ms
five worst-case runs: 3003 / 3006 / 3004 / 3008 / 3006 ms
3 calls in sequence:                                       9032 ms total
```

So the enforceable bound is `secs + grace` (3 s, not 2 s), and the bound's exit-code
vocabulary is **{124, 137}**, not the `{124}` the comment names (`:337-343`). The
census's per-session loop (`:1496-1512`) makes one such call per fleet session, so its
worst case is `n_fleet × 3 s` — bounded, but only as a product. Two further measured
details, both good news for this gate and both construct-dependent:

- the grace kill prints a `Killed` job-control line on the *invoking* shell's stderr
  when the bounded command is a plain foreground command
  (`/tmp/mori-r8-lessons/timeout-k.sh: line 6: 3059288 Killed …`), but **not** inside a
  command substitution: replicating the census construct exactly
  (`CAP_OUT=$(timeout -k 1 2 bash -c 'trap "" TERM; sleep 9' 2>&1)`) gave
  `CAP_RC=137 CAP_OUT=[]` with **0 B stderr**. The "0 B stderr" admission criterion
  survives the grace path in this shape.
- `rc-137` reaches the row as a *reason string* (`reason=rc-$CAP_RC`, `:1502`), so an
  analyst can tell the code from a peer's own rc only by knowing the bound's vocabulary
  — the reason string discloses the code, not its author. The durable part is the
  principle: enumerate every code the bound can produce and label which side produced
  it.

### 4. The filter's drop set (and the residual-3 closure, at the snapshot)

`find -maxdepth 1 -type f -name '*.round'` (the r7 walk) over a fixture holding a
regular file, a symlink→file, a dangling symlink, a symlink→dir, a directory, a fifo, a
mode-000 file, a hidden file and a second regular file returned **4**:

```
/tmp/mori-r8-lessons/enum/state/a.round
/tmp/mori-r8-lessons/enum/state/f.round
/tmp/mori-r8-lessons/enum/state/.hidden.round
/tmp/mori-r8-lessons/enum/state/target.round
```

and the shipped row said exactly that, with no trace of the other five (before-arm,
r7 bytes, `MORI_STATE_DIR` pinned at the fixture):

```
SURFACE watchdog: drift (… state_rounds=4 state_rounds_max=9 state_lag=0 state_ahead=0 state_cmp=0 state_val_unreadable=1; ts=2026-10-15T20:19:49Z)
```

The filter is not removable — the fifo it protects against blocks the reader (a read of
`e.round` under a 0.3 s bound → rc 124 at 304 ms; the `[ -r ]` gate is no help: the same
fifo read in the `read_file` shape, `[ -r ]` then `head -n 1`, under a 0.5 s bound →
rc 124 at 508 ms). Hence the r8 shape, verified
at `7f3fcacf` on the same fixture:

```
SURFACE watchdog: drift (… state_rounds=4 state_rounds_max=9 state_lag=0 state_ahead=0 state_cmp=0 state_val_unreadable=6 state_val_unread_reasons=file:1 symlink:3 dir:1 other:1; ts=2026-10-15T20:19:21Z)
FINDING WATCHDOG_STATE_ENTRY_UNREADABLE severity=info obs=reason=symlink-not-followed entry=b.round path=/tmp/mori-r8-lessons/enum/state/b.round …
FINDING WATCHDOG_STATE_ENTRY_UNREADABLE severity=info obs=reason=is-directory entry=d.round …
FINDING WATCHDOG_STATE_ENTRY_UNREADABLE severity=info obs=reason=non-regular entry=e.round …
```

`state_rounds` keeps its old meaning (4 regular files, so an existing state dir reads
byte-identically), and the five entries that used to be nothing are now *counted by
reason* (`state_val_unread_reasons`, census `:587`; classification `:525-541`), stderr
0 B. The general rule: when a walk filters, the row must carry the filter's drop set by
reason, or "counted" silently means "survived the filter".

## Applying it (any lane)

- Before writing a probe, write down its four prices: the counter (and how "not found"
  will be reported), the scheduling (serial or overlapped, with the measured marginal),
  the bound (nominal + grace, and every code it can produce), the filter (and the count
  of what it drops).
- Price dwells in pairs or inside one span; never compare consecutive medians on a
  shared host. If the budget is smaller than the instrument's observed spread, the
  honest answer is "unusable as a decision instrument", and the isolated measurement is
  the decision.
- Prefer the overlapped/bracketed scheduling when the dwell is the entire cost: a sleep
  that runs behind work already on the critical path measured 0 ms, five times out of
  five, at load 4.5× cores.
- Bound every read whose peer is not the kernel (server, fifo, symlink target) with
  `timeout -k`, and give the bound's code its own reason string; `timeout` without `-k`
  reports a bound it does not enforce.
- Keep the type filter; count its drops by reason. The filter is what stops the
  blocking read.
- Report the measured elapsed as the divisor, never the nominal window; `sleep 0.2` was
  206–226 ms under this load.
- A numeric zero from a probe must be accompanied by the proof that its counter was
  found.

## Limits

- One host, one kernel, one load regime (69–148 on 32 cores, wave-induced). The
  *spread* numbers in §2(a) are properties of this host at that time, not constants;
  the in-span numbers in §2(b) held at load 145 because they compare within one second,
  not across runs.
- GNU coreutils 9.11 `timeout`. The specific code for the grace kill (137) and the
  "waits for a TERM-ignoring child" behavior are measurements on this host/toolchain;
  the durable part is "enumerate the codes the bound can produce", not the digits.
- The TERM-ignoring peer was a `/tmp` stub. This host had no tmux server at any clock in
  this seat's window, so **no claim is made** that a real tmux client ignores SIGTERM or
  that the per-session probe ever spent its bound — only that the bound behaves as
  measured against a hostile stub, and that its worst case is `n_fleet × (bound + 1 s)`
  by construction.
- The r8 bytes cited are a mid-wave snapshot; every line number above is valid at
  `7f3fcacf…` only. No claim is made about the round's final bytes, its selftest tally,
  or its oracle.
- Nothing here proposes a threshold, a window length, or a design. The four prices are
  what this seat and the two implementing seats measured; the disc write-rate window
  the round asked about is still unimplemented at the snapshot, and this note does not
  argue for or against that decision — it supplies the pricing method.

## Logs (ephemeral, /tmp only)

`/tmp/mori-r8-lessons/`: `baseline-timing.txt` · `dwell-pairs-pinned.txt` (the A/B/C
census run above) · `dwell-controlled.out` (the in-span run) · `timeout-semantics.out` ·
`timeout-k.out` · `cmdsub-probe.sh`/`cmdsub-err.txt`/`cmdsub-out.txt` (the census
construct, 0 B stderr) · `enum-filter.out` + `find-L-stderr.txt` · `disk-window.out`
(the artifact) · `disk-window2.out` · `disk-window3.out` · `state-fixture-before.txt` /
`state-fixture-after.txt` + `before-stderr.txt`/`after-stderr.txt` · `mori-census-r7.sh`
(the pinned r7 bytes).