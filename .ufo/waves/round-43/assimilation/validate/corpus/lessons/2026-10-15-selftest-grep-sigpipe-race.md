# Lesson — `producer | grep -q` under `pipefail`: the match succeeds, the writer dies of SIGPIPE, and the pipeline rc says "missing"

date: 2026-10-15 · lane: mori-shokunin · round: 9 · source seat: lessons-distiller (flash wave)

Measured against `tools/mori-census.sh` revision r5 sha256
`390ab9cd2db17b9d71508639f4f61cc61646ae090b61bf48243cda3e7211cae1`
(`VERSION=census-r5`, 2380 lines; sha re-verified unchanged after every battery below)
and the frozen oracle `tools/mori-silence-cases.sh` sha256
`448f77238c73a5c929a898dad0f0c495fd2a66cc4b90a00ae84ede69a86beeb5` (untouched by this
note). All measurements 2026-10-15T21:07–21:16Z, bash 5.3.15, host load average
85–110 (the round's own wave). Instruments and raw logs under `/tmp/lesson-r9/`
(ephemeral); nothing here shortened any lane file. This note records the class and
what I measured; it does not claim to have retro-attributed the r8 observations.

## The lesson

Under `set -euo pipefail`, the expression

```
printf '%s\n' "$out" | grep -qE -- "$re" || miss="$miss |$re|"
```

— the assertion shape at `tools/mori-census.sh:1783` and `:1809` — can take the
`||` branch **even when grep found the match**. Mechanically:

1. `grep -q` exits 0 the moment it sees a match and closes its end of the pipe;
2. the writer element (a forked subshell running the bash `printf` builtin) is
   still mid-payload — it emits the captured output through many small `write(2)`
   calls (63 calls for a 2 292-byte payload in the traced rep below);
3. its next write gets `EPIPE` and the process dies of `SIGPIPE` (exit 141);
4. `pipefail` makes the **pipeline's** rc the rightmost non-zero rc — 141 — even
   though the consumer that produced the verdict exited 0;
5. the `||` guard reads rc≠0 as "no match" and records `missing match |$re|`
   (the message template at `:1786`) — a false FAIL.

The general rule: **under `pipefail` a pipeline's rc answers "did every element
exit 0", not "did the consumer match". Any consumer that exits early (`grep -q`,
`-m1`, `-l`) can kill its producer with SIGPIPE, so a *successful* verdict can
ride on a *failing* rc — and whatever guard you attach to the pipeline decides
how the misread is phrased.** It is a flake, not a crash: whether the writer is
descheduled long enough for the consumer to exit first depends on scheduling.

## Every occurrence in `tools/mori-census.sh` (r5 `390ab9cd…`), classified

| site | shape | consumer exit | consequence of the race |
|---|---|---|---|
| `:1783` `check()` | `printf "$out" \| grep -qE -- "$re" \|\| miss=…` | early (`-q`) | **false FAIL** `missing match` (named in r8) |
| `:1809` `check_cli()` | same shape | early (`-q`) | false FAIL `missing …` |
| `:1771` | `elif ! printf "$out" \| grep -qE "^MORI_CENSUS: …"` | early (`-q`) | `!` flips → false FAIL `verdict want …` |
| `:1773` | `elif printf "$out" \| grep -qE 'integer expected\|…'` | early (`-q`) | false FAIL `shell diagnostic noise …` |
| `:1779` | `"$(printf "$out" \| grep -m1 -E …)"` (message text only) | early (`-m1`) | diagnostic snippet lost; no verdict flip |
| `:1322` (production silence path) | `printf "$inwin" \| sed … \| grep -Fxq -- …` inside `if` | early (`-Fxq`) | **condition inversion**: subject commit graded non-subject |
| `:456`, `:702-719`, `:1428` | `printf … \| grep -c[iE] …` (+ `\|\| true`) | full read | not this class — `-c` reads to EOF, never closes early |
| `:636` | `grep -qE … "$cand"` (a file) | — | no writer process; safe |

The two r8-named lines are the false-FAIL instances; the same construct was also
present at `:1771`/`:1773`/`:1779` of the harness and at `:1322` of the
**production** path. Because the round freezes production bytes, a fix that
touches only the `--selftest` path eliminates the harness sites but leaves
`:1322` as same-class, named debt (measured below; its failure mode is a wrong
grade, not a failed case).

## What was measured

### A. Construct-level sweep — the pipeline rc without any guard

`out=$(seq 1 N)`; reps of `printf '%s\n' "$out" | grep -qE -- PAT`, counting
rc=141 (SIGPIPE via pipefail) vs rc=0 (`/tmp/lesson-r9/iso.sh`, `iso4.sh`):

```
small-early    bytes=2291    pat=^5$       reps=300  rc0=299  rc141=1
small-late     bytes=2291    pat=^600$     reps=300  rc0=300  rc141=0
mid30k-early   bytes=23892   pat=^5$       reps=300  rc0=298  rc141=2
big70k-early   bytes=60893   pat=^5$       reps=300  rc0=284  rc141=16
big70k-late    bytes=60893   pat=^12000$   reps=300  rc0=300  rc141=0
huge-early     bytes=1288894 pat=^5$       reps=100  rc0=0    rc141=100
huge-late      bytes=1288894 pat=^200000$  reps=100  rc0=100  rc141=0
follow-up:  small-early 3/5000 · small-late 0/5000 · small-mid 0/3000
            h34-early 1/3000 · h34-mid 1/3000 · h34-late 0/3000   (bytes=3491)
```

Two properties: (a) an **early** match on a 2.3 KB payload — the harness's
ballpark — races at roughly 1/1000–1/3000 per assertion under this load;
(b) a match near the **end** of the payload did not race at all in 300–5 000
reps, because by the time grep has read that far the writer has usually
finished. The harness's own captured outputs are 453–3 435 bytes (measured over
the 32-run battery below), i.e. squarely inside the racing band.

### B. Attribution — grep matched while the pipeline said otherwise

3 000 reps of the 2 291-byte early-match case with `PIPESTATUS` captured
(`iso2.sh`):

```
rep=2684 ps0=141 ps1=0
raw-pipeline hits=1 / 3000
```

`ps1=0` is the decisive bit: **grep exited 0 — it matched**. `ps0=141` is the
printf element killed by SIGPIPE. With `pipefail` the pipeline rc is 141, the
`||` fires, and the case is reported missing exactly as in r8
(`SCORECARD.md:413-418`: "missing match" on a random case, green on rerun).

### C. The dying syscall — strace

The same loop under `strace -f -e trace=write,close -e signal=SIGPIPE`
(`iso3.strace`; first hit at rep 16 because tracing widens the window
massively):

```
632044 write(1, "46\n47\n…56"…, 129) = 129
632044 write(1, "220\n221\n…227"…, 128 <unfinished ...>
632046 close(255) = 0 · close(3) = 0 (×9)  ← grep element
632046 +++ exited with 0 +++
632044 <... write resumed>) = -1 EPIPE (Broken pipe)
632044 --- SIGPIPE {si_signo=SIGPIPE, si_code=SI_USER, si_pid=632044, si_uid=1000} ---
632044 +++ killed by SIGPIPE +++
```

Writer identification (execve+write trace, `t3.txt`): the printf element is a
forked bash subshell (no execve; 63 `write(1)` calls for the 2 292-byte
payload), `/usr/bin/seq` wrote its captured output in 1 call, `/usr/bin/grep`
made 0 writes. So the payload is emitted in many small writes, which is what
lets the reader close mid-payload even at harness sizes.

### D. The production-shaped 3-stage variant (`:1322`'s shape)

`printf '%s\n' "$inwin" | sed -E 's/^[0-9]+ //' | grep -Fxq -- "lane-shokunin <lane@shokunin.local>"`,
fixture = 200 identical `1700000000 lane-shokunin <lane@shokunin.local>` lines
(9 399 bytes; the census's `%ct %an <%ae>` format), match on line 1
(`iso6b.sh`, `iso6c.sh`):

```
3-stage (exact-line fixture): ok=2929 bad=71 / 3000
3-stage pipefail-nonzero despite match: 88 / 3000
rep=29 ps0=0 ps1=141 ps2=0   (first hits)
```

Here **sed** is the element that dies of SIGPIPE (grep matched, rc 0), the
pipeline rc is 141, and the `if` takes the else — a subject commit graded as
non-subject, i.e. fail-toward-wrong-grade, not fail-closed. The rate is ~2–3%
in this window; it scales with the window (it is the same mechanism as A).

### E. Countermeasure measured, not asserted

`grep -qE -- "$re" <<< "$out"` (here-string: no forked producer, no writer to
SIGPIPE, rc = grep's rc) under the same `pipefail` loop (`iso2.sh`, `iso5.sh`):

```
2 291 B:   0 misses / 3000
60 893 B:  0 misses / 300
1 288 894 B: 0 misses / 100
```

Zero misses at exactly the sizes where the raw pipeline fails (16/300 and
100/100 respectively). `case "$out" in *"$re"*)` / `[[ "$out" =~ $re ]]` are
equivalent-class options (no pipe at all) but carry shell-glob/ERE semantic
differences — the here-string is the drop-in that keeps grep's exact `-E`
semantics.

### F. My own battery at the frozen r8 bytes — reported honestly

32 instrumented selftest runs (20 at 4-way, 12 at 6-way concurrency) at
`390ab9cd…`, every assertion's rc logged (`battery/*.checks.log`): **32/32 runs
green, 4 256/4 256 assertions rc=0, sizes 453–3 435 bytes, 0 flakes.** The sha
was re-verified unchanged after the battery. So at these sizes the class is
rare per assertion (~1/3000 in section A), and I did **not** reproduce a
selftest flake in my battery; r8's live rate (admission ~25% in one battery,
parent 1/8) is the load-sensitive end of the same distribution. The
construct-level sections B/C/D are the decisive mechanism evidence; section F
bounds the rate at this host/load. A second, different cause seen in r8 —
reading the census file while it was still being written
(`corpus/knowledge/surfaces-r8.md:237-246`, defect 2) — produces the same
"random case, green on rerun" symptom and should not be conflated with this
class.

## Countermeasures that fit this codebase

1. **Capture, then match — no live pipe.** Replace
   `printf '%s\n' "$out" | grep -qE -- "$re" || miss=…` with
   `grep -qE -- "$re" <<< "$out" || miss=…` (measured: 0/3 400). The guard then
   reads grep's real verdict, not a producer's death.
2. **Never `|| true` your way out.** The writer's SIGPIPE is harmless only if
   the *consumer's* answer is what you read; `|| true` discards the answer
   together with the rc. Restructure; don't mask.
3. **Guard the family, not the instance.** Search the file for `grep -q`,
   `grep -m1`, `grep -l`, and `grep -Fxq` over pipes — not only the lines that
   happened to flake (the r8 report named two; this note finds five harness
   occurrences plus one production). `grep -c` and greps over real files are
   not this class.
4. **If a pipeline must stay live, make the writer's death impossible or
   irrelevant**: `grep -qE -- "$re" < <(producer 2>/dev/null)` still has a
   producer whose SIGPIPE is harmless (the substitution's rc is not the
   pipeline rc), but a here-string is simpler when the payload is already
   captured.

## Applying it (any lane)

- Grep your harness/gate for `\<producer\> | grep -q\|-m1\|-l` under
  `pipefail`: each is a potential "successful check reports failure" — and in
  an `if` without a guard, a silent condition inversion.
- Remember the algebra: pipeline rc = rightmost non-zero element. A consumer's
  exit-early death certificate for its producer is `141`, and `141 ≠ 1`: any
  rc-based match test that does not distinguish "consumer said no" from
  "producer was killed" is reading a lie.
- Reproduce cheaply: loop the exact construct 3 000× with `PIPESTATUS`
  captured (recipe in section B); under `strace -f` the same loop flakes within
  tens of reps, which makes the mechanism visible without waiting for a natural
  flake.
- A determinism gate should *run* the suite repeatedly and require equal
  verdicts (r8's registered admission addition); but per this note, a green
  battery is not proof of absence — the probabilistic form was still
  demonstrable at the same bytes (B/C/D) while my 32-run battery read clean
  (F).

## Limits

- Single host, bash 5.3.15, load average 85–110 during the measurements; the
  per-assertion rates are scheduling-dependent and are bounds for this load,
  not constants.
- I cannot retro-attribute r8's specific observations (no rc logs survived):
  the class is *sufficient* for the observed `missing match` symptom and the
  fix eliminates it by construction, but the causal claim rests on this note's
  live repro, not on the r8 runs.
- Section D's fixture is a bounded 9 399-byte window with the match on line 1;
  the production risk at `:1322` grows with the post-launch window size and is
  not sized for the live fleet here.
- The countermeasure (here-string) is measured for `grep -qE` with the
  harness's own patterns; `case`/`[[ =~ ]]` alternatives are named but not
  separately measured.
- This note is the class + evidence; the round-9 fix and its verification are
  other seats' claim. Fix state observed while this note was being finalized:
  no diff at 21:16Z; a fuller revision at 21:18Z (sha `1c49238a…`, +21/−7)
  rewrote all five harness sites (`:1771`/`:1773`/`:1779`/`:1783`/`:1809` at r5
  numbering) to grep one captured `$OUT_FILE` — no live pipes left in the
  harness, production untouched (so `:1322` stands as named debt under the
  byte-freeze). All numbers above are pinned to the pre-fix r5 bytes
  `390ab9cd…`; verifying the fix belongs to the fix/verifier seats.