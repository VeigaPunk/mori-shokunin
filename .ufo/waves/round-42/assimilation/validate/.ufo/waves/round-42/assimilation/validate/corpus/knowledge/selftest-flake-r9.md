# selftest flake r9 — the `printf | grep -q` SIGPIPE race: mechanism, archaeology, the capture-file fix, batteries, and a determinism gate

source: `tools/mori-census.sh` before sha256
`390ab9cd2db17b9d71508639f4f61cc61646ae090b61bf48243cda3e7211cae1`
(`VERSION=census-r5`, 2380 lines) → after sha256
`1c49238a7fd87277151ff5776acfb4d62fadd9d69764a02f0ede03ef0d3902d2`
(`VERSION` still `census-r5`, `:201` — the fix is a revision of r5 distinguished by SHA,
not a version bump). The oracle `tools/mori-silence-cases.sh` sha256
`448f77238c73a5c929a898dad0f0c495fd2a66cc4b90a00ae84ede69a86beeb5` is **byte-unchanged**
this round (verified at the entering clock and again after the fix) and returns
`matched=28 total=28` exit 0 at the new census bytes (this note's own run, 18 s,
`/tmp/mori-r9-note/oracle-after.log`).
verified-at: 2026-10-15T21:05–21:35Z — GNU bash 5.3.15, host load average ≈90–140 (the
round's own 32-seat wave); my two loaded arms added 4 CPU hogs each and killed them at
arm end (verified gone from `ps`). Instruments and raw logs under `/tmp/mori-r9-note/`
(ephemeral): `before-battery.log`, `replay.log`, `replay2.log`, `after-battery.log`,
`oracle-after.log`, `case-sizes.log`, `cases.tsv`. No durable r9 receipt had landed in
`corpus/evidence/` at this note's clock; the numbers here are first-hand plus the two
cross-references named in §5.
scope: detection and report only; this seat wrote no lane file but this note.

## 1. The race, measured

The r5 harness asserted every selftest case with a live pipeline (`tools/mori-census.sh`
r5 `:1783` in `check()`, `:1809` in `check_cli()`):

```
printf '%s\n' "$out" | grep -qE -- "$re" || miss="$miss |$re|"
```

Under the file's `set -euo pipefail` (`:194`), the chain is:

1. `grep -q` exits **0 at the first match** and closes its end of the pipe;
2. the producer element (a forked subshell running the bash `printf` builtin) is still
   mid-payload — it emits the captured output in **many small writes, one per line**
   (measured below), not one write;
3. its next write gets `EPIPE` and the process dies of `SIGPIPE` (exit 141);
4. `pipefail` makes the pipeline rc the rightmost non-zero element — 141 — **even
   though the consumer that produced the verdict exited 0**;
5. `|| miss=` reads rc≠0 as "no match" and records `missing match |$re|` — a false
   FAIL on whichever case the scheduler let the reader win. Green on rerun, because the
   writer usually finishes before grep is rescheduled.

Independent corroboration with different instruments (PIPESTATUS capture showing
`ps0=141 ps1=0`, and strace showing 63 `write(1)` calls for a 2 292-byte payload) is in
the r9 lesson `corpus/lessons/2026-10-15-selftest-grep-sigpipe-race.md` — the distiller
renamed it mid-round to exactly the path the fix comment cites.

### 1a. The writer's chunking (why a 3 KB payload can race at all)

`strace -f -e trace=write` on the bare construct:

```
3-line payload, printf '%s\n':  write(1,"aaa\n",4) write(1,"bbb\n",4) write(1,"ccc\n",4)
same payload,  printf '%s':     write(1,"aaa\n",4) write(1,"bbb\n",4) write(1,"ccc",3)
single 2 906-char line:         one write of the whole line
```

The payload is delivered **one line per write**, so every line after the matched line is
a window in which `grep` can exit first. A pipe-capacity model is therefore wrong: a
2-line payload sweep (0/20 fires at 3 011 / 4 011 / 5 011 / 8 203 / 16 395 / 32 779 B;
19/20 at 65 547 B; 20/20 at 66 011 B — the 64 KiB `fcntl` pipe size) predicted inertness
at the harness's sizes and was falsified by the multi-line replays below.

### 1b. The real cases, replayed (all 56 case payloads × their exact regexes)

The 56 `$out` payloads of a passing run (2 3xx–3 442 B, mean 11.1 lines, max 13 — all
far below 64 KiB) were replayed through the exact pipeline with the exact patterns,
100 iterations each, under 4 CPU hogs at load ≈130:

```
replay.log:  TOTAL trials=13300 matched=13298 signal_fires=2
  SIGNAL rc=141 case=disk: device missing from diskstats -> unmeasured disclosed
         pat=FINDING DISK_IO_UNMEASURED
  SIGNAL rc=141 case=watchdog: all four non-value classes counted by reason
         pat=state_rounds=2 state_rounds_max=7
```

Both fires are real payload/pattern pairs with the match present. A second sweep,
3 000 reps per match position (`replay2.log`), shows the window is the tail after the
match:

```
first line   (^SURFACE watchdog: ok, 12 lines after)    3/3000 fires
line 2 of 13 (state_rounds=2 state_rounds_max=7)        1/3000
line 10 of 11 (FINDING DISK_IO_UNMEASURED, 1 line after) 2/3000
last line    (^MORI_CENSUS: )                            0/3000
```

### 1c. End to end: the harness's own failure string, produced by the race

The real payload + real pattern through the exact `check()` fragment, with a padded tail
to widen the window (no hogs; `e2e-proof.sh`), reproduces the r8 symptom literally:

```
tail=2 lines    0 false-FAILs / 200
tail=20 lines   0 / 200
tail=200 lines  2 / 200   FAIL drift: DISK_IO_UNMEASURED: missing match |FINDING DISK_IO_UNMEASURED| (iteration=…)
tail=1000 lines 9 / 200
```

That is the message shape r8's admission recorded (`SCORECARD.md:413-422`:
`FAIL drift: CGROUP_OOM_KILL: missing match |FINDING CGROUP_OOM_KILL|`, 55/56).

### 1d. Honest rate statement

At this clock's pressure the per-run rate was **below my batteries' resolving power**: my
pre-fix battery (10 runs at the pinned entering bytes, `/tmp/mori-r9-note/before-battery.log`)
is **10/10 PASS, 0 false-FAILs** (560 case-verdicts); the distiller's 32-run instrumented
battery at the same bytes was likewise green; the scribe's 16-run battery 0/16. r8's 1/8
and ≈25% are the load-sensitive end of the same distribution; the construct-level replays
are what prove the class at these bytes. A second r8 cause produces the same "random
case, green on rerun" symptom — reading the census while it was still being written
(`corpus/knowledge/surfaces-r8.md` defect 2) — and must not be conflated with this one.

## 2. Site inventory in the entering bytes (r5)

| site | shape | consumer exit | consequence of the race |
|---|---|---|---|
| `:1783` `check()` | `printf "$out" \| grep -qE -- "$re" \|\| miss=…` | early (`-q`) | **false FAIL `missing match`** — the r8-named symptom |
| `:1809` `check_cli()` | same shape | early (`-q`) | false FAIL `missing …` |
| `:1771` | `elif ! printf "$out" \| grep -qE "^MORI_CENSUS: …"` | early (`-q`) in principle | verdict line is printed last, so grep drains the stream in practice; a fire would invert the `!` and skip the verdict check (path to a false PASS) — never observed |
| `:1773` | `elif printf "$out" \| grep -qE 'integer expected\|…'` | early (`-q`) on a match | a real shell-diagnostic defect could be **masked** (the `elif` sees rc 141 and moves on) — never observed |
| `:1779` | `"$(printf "$out" \| grep -m1 -E …)"` | early (`-m1`) | failure-message text lost; no verdict flip |
| `:1322` (**production** silence path) | `printf "$inwin" \| sed … \| grep -Fxq -- …` inside `if` | early (`-Fxq`) | condition inversion — a wrong authorship grade, not a failed case; **out of this round's scope** (production bytes frozen) and left as named same-class debt |

After the fix the only pipelines left in the selftest path have consume-all readers: the
error message `printf '%s' "$out" | tail -n3 | tr`, and `fx_hash`'s
`find | sort | sha256sum | cut`. Neither can close a pipe early.

## 3. Git archaeology — the race is as old as the harness

The construct was born in the census's **first commit** and survived every revision,
including the rounds that hardened the file around it (none of the four hardenings
touched the harness's assertion mechanics):

| revision | commit (date) | census sha256 (8) | site lines (`check` / `check_cli`) |
|---|---|---|---|
| r1 landing | `7ca17b1` (2026-10-14) | `7432255f` | `:642` / `:668` |
| r1 final (recorded as "r1") | `0715198` (2026-10-14) | `e3073a2b` | `:642` / `:668` (same shape) |
| r2 | `1439c47` (2026-10-15) | `fe22a14f` | `:1055` / `:1081` |
| r3 | `5b62c89` (2026-10-15) | `af2d4e79` | `:1090` / `:1116` |
| r4 | `d30b4e4` (2026-10-15) | `c7c3569b` | `:1528` / `:1554` |
| r5 (entering r9) | `9738f1a` (2026-10-15) | `390ab9cd` | `:1783` / `:1809` |

The recorded "r1 census `e3073a2b…`" is the *last* r1 revision (`0715198`), not the
landing commit (whose bytes hash to `7432255f…`); the race sites exist in both. The
other harness occurrences are younger: the diagnostic-noise check (`:1773`) and its
`grep -m1` message (`:1779`) were added in round 7 (`d30b4e4`); the verdict check
(`:1771`) and its `grep | head` message (`:1772`) date from the r1 landing. The r8
flake was therefore not a regression of any round's change: it is a latent property of
the harness's assertion idiom since 2026-10-14, and r8's +11 cases only increased the
number of draws per run.

## 4. The fix at `1c49238a…` — capture, then match

One addition to `run_selftest()`: a per-run capture file, declared at `:1572`
(`local … OUT_FILE`) and set at `:1585` (`OUT_FILE="$work/.last-out"`, inside the mktemp
work dir the EXIT trap removes). `check()` writes the captured output once
(`:1781 printf '%s\n' "$out" > "$OUT_FILE"`) and every assertion then greps the **file**:
`:1784`, `:1785`, `:1786`, `:1792`, `:1796` (the two message-path greps are additionally
`|| true`-guarded because a grep miss is not a verdict there); `check_cli()` does the
same at `:1817` and `:1823`. There is no producer process left for `grep -q` to kill, at
any payload size or match position.

Why this shape: the capture already exists in `$out`; writing it once and letting every
check grep the same bytes keeps grep's exact `-E` semantics. The lesson measures the
here-string drop-in (`grep -qE -- "$re" <<< "$out"`: 0 fires at sizes where the pipeline
fires 16/300 and 100/100); `case`/`[[ =~ ]]` are equivalent-class but change the regex
dialect.

Verification of the fix (all at `1c49238a…`):

- **Class eliminated at every harness occurrence**: the five live-pipe greps above are
  file reads now; `awk 'NR>=1571' tools/mori-census.sh | grep -nE '\|'` yields only the
  consume-all pipelines named in §2. Of the six added lines that contain `|`, none is a
  pipeline: one is a comment, one is a `|| true` guard, two carry the alternation of the
  diagnostic regex, and two are `|| miss=` guards whose `|` is inside the miss-message
  string.
- **Selftest-only scope**: all diff hunks fall inside `run_selftest()` (`git diff -U0`
  hunk headers `@@ -1572 … @@ -1823`; +21/−7), and `run_selftest` is reached only from
  the `--selftest` branch (`:2388`, under `if [ "$selftest" -eq 1 ]` at `:2387`). The
  production probe code is untouched by the diff — the frozen oracle agrees at the new
  bytes (`28/28`, want-sets unchanged), and the live-row equivalence is the round's
  receipt work, not this note.
- **Selftest count unchanged**: `MORI_CENSUS_SELFTEST: PASS (56 cases, 56 passed,
  0 failed)` exit 0 at the new bytes (mine, 18–22 s per run; the entering bytes' runs at
  this clock took 28–41 s, but load varied between arms — not a claimed speedup).
- **Fixed-form counter-measurement**: the payload/pattern pair that fired 3/3000 in
  `replay2.log` yields **0/2000** through the fixed form (grep over a file, no writer;
  `fixed-form.sh`).
- **Detection power retained** (the fix must not neuter assertions): a `/tmp` copy with
  `emit_finding WATCHDOG_STALE warn` → `WATCHDOG_AGED` (a mutation that changes the
  asserted substring) fails exactly as it should — `FAIL drift: WATCHDOG_STALE: missing
  match |FINDING WATCHDOG_STALE|`, 55/56, exit 1. (A mutation that only renamed the id
  to `WATCHDOG_STALE_X` still passes, because the harness asserts unanchored substring
  regexes — expected semantics, not a gap.)

## 5. Battery evidence

Batteries ran on pinned `/tmp` copies; the lane file's sha was re-verified unchanged
before and after (`after-battery.log` carries `LANE_SHA before=after=1c49238a…`).

| battery | bytes | runs | added load | result | log |
|---|---|---|---|---|---|
| pre-fix (mine) | `390ab9cd…` | 10 | none | **10/10 PASS, 0 FAIL**, walls 28–41 s | `before-battery.log` |
| after, arm A (mine) | `1c49238a…` | 20 | none | **20/20 PASS, 0 FAIL**, walls 18–32 s | `after-battery.log` |
| after, arm B (mine) | `1c49238a…` | 20 | 4 CPU hogs (load ≈91 at arm start) | **20/20 PASS, 0 FAIL**, walls 18–25 s | `after-battery.log` |

Every one of the 50 post-fix runs printed the identical tally
`MORI_CENSUS_SELFTEST: PASS (56 cases, 56 passed, 0 failed)`, exit 0. My two arms are the
round's independent batteries; the loaded arm is the one that matters (the race needs
scheduling pressure to fire). Cross-references (not my runs): lessons-distiller 32-run
instrumented battery at `390ab9cd…`, green (their lesson §F); scribe before-battery,
16 runs green (`.ufo/round-9/goal-wave/measurements-ledger.md`); frozen-oracle run at
the new bytes, `matched=28 total=28` exit 0 (mine, §preamble). No durable r9 receipt was
present in `corpus/evidence/` at this note's clock.

## 6. Determinism-gate recommendation (for future admissions)

A green battery is necessary but not sufficient — this round proves the probabilistic
form at bytes whose 10-run, 16-run and 32-run batteries were all green (§1d). In cost
order:

1. **Static race-class scan (seconds).** Fail admission if the selftest path contains a
   live-piped early-exit consumer: `awk 'NR>=1571' tools/mori-census.sh | grep -nE
   '\|[[:space:]]*(grep[[:space:]]+[^|]*-[A-Za-z]*q|grep[[:space:]]+[^|]*-m[0-9]|head)'`
   must be empty (it matched six lines before this fix), and `git diff` must add no pipe
   to the path. `grep -c` and greps over files are not this class. Scan the production
   path too — `:1322` remains same-class, named.
2. **Repeated-run battery at frozen bytes (minutes).** ≥20 consecutive `--selftest`
   runs, one arm under artificial load you own and kill, require the identical tally line
   and exit 0 every run; re-verify the SHA immediately before and after (a battery
   started across a file write is not evidence — r8's two observed failures happened
   while the file was being edited). Two independent batteries, not one.
3. **Construct-level probe (bounded, seconds).** Loop the exact assertion shape with
   `PIPESTATUS` captured, ≥3 000 reps with the match near the top of a multi-line
   payload; the claim is 0 rc=141. Recipe in the lesson §B. This is the falsifier that
   works when the run-level rate is under a battery's resolution.
4. **Detection-power probe (one run).** The battery proves the harness is stable, not
   that it can still fail: mutate one probe in a `/tmp` copy so an asserted substring
   changes, expect a FAIL (measured above: 55/56 exit 1). Pair it with the class scan —
   stability without sensitivity is not a verdict machine.
5. **Failure evidence rule.** Any harness FAIL should dump the full captured output for
   the failing case to the receipt. r8's flakes survived only as one-line messages,
   which is why attribution needed this round's replays; the new `OUT_FILE` makes the
   dump trivial if ever wanted.

## 7. What this note does not claim

- No remediation, no kill/restart of other seats' load processes, no config change, no
  git commit; every fixture under `/tmp`; the only lane file this seat wrote is this note.
- Per-assertion rates are scheduling-dependent bounds for this host and load (≈90–140),
  not constants; my pre-fix run-level battery (10 runs) and the distiller's 32 did not
  reproduce an r8-style run-level flake, so r8's specific observations are attributed by
  mechanism and symptom, not re-run.
- The fix comment's own engineering numbers (15/8000 early-match rc=141, 0/10000
  late-match) are flake-impl's measurements, consistent in shape with mine, not
  independently re-run here.
- The oracle's 28/28 and the live-row equivalence are the round's production-identity
  proof; this note contributes the diff-scope evidence (hunks confined to `run_selftest`)
  plus one oracle run of its own.
- `:1322` in the production silence path remains the same race class; with production
  bytes frozen this round it is registered debt, not a claim of closure.