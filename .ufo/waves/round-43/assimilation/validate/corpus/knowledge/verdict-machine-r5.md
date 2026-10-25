# The verdict machine, round 5 — the run-order channel, the seeded shuffle, and the residual seed channels

seat: **note-writer** (round-5 flash wave) · lane mori-shokunin · written
2026-10-15T18:16Z · detection and report only; nothing here remediates a fleet
process. This seat writes **this file only** (SCORECARD.md / LOG.md are
parent-owned; `corpus/evidence/` belongs to the receipts-writer).

Describes the two tools at their pinned revisions:

| tool | sha256 | revision |
|---|---|---|
| `tools/mori-silence-cases.sh` | `7143ccc2a14221713334c33ade56e24ca711fbd0d3d17f31d33e151be544f017` | r5 oracle, 970 lines (working tree; uncommitted at this seat's clock) |
| `tools/mori-census.sh` | `af2d4e79e69b70bb0b5aecd6acc9608fc7c16b0716766d4a60310e0689d350d7` | `VERSION=census-r3` (`:61`), 1438 lines — **frozen this round** |

Lane HEAD `7a3629a83c2e81774ebeb65b4b92a07b65830add`; the r5 oracle blob was
first seen at 18:00:27Z and stabilized at 18:03:35Z (three consecutive 30 s
sha checks), then was re-verified `7143ccc2…` unchanged before and after every
run below. The "before" column is the round-4 oracle `be0e28b8…` (git HEAD
bytes `5b62c897`), also re-verified. The frozen census sha was checked before
and after every measurement; the receipts-writer's set
`corpus/evidence/order-r5-20261015T180431Z-*.log` was produced at the same two
SHAs and agrees with every figure that overlaps — disagreements are stated.

All scratch for this note is under `/tmp/mori-vnw-r5/` (never in the lane
tree); attacker and probe sources are sha-pinned in §5.

## 1. The run-order channel — why fixed order made a canned sequence correct

The round-4 oracle ran its 28 cases at source level in registry order, one
`assert_case` per case, so **one oracle run produced 29 census invocations in
one fixed order** (27 graded runs — 26 `assert_case` + the read-only guard —
plus the two shape runs). Nothing per-run entered the census environment: the
`env -i` export list (`be0e28b8…:279-306`) is constant across every run.

Two properties composed into a forgery channel:

1. **Position was a fixed bijection to case identity.** Invocation *k* of every
   run was always the same case; the oracle's expectation table is a constant
   of the case, not of the run. So a table indexed by invocation position *was*
   the answer key.
2. **The attacker needs no fixture byte to count its own position.** The census
   can derive the oracle's per-run `$WORK` from its own env — `MORI_STUB_DIR=
   <work>/case.XXXXXXXX/stub`, so `work=$(dirname "$(dirname "$sd")")` — and
   keep a counter under `$WORK` (this exact derivation is the round-4 receipt's
   `v2b` attacker; `corpus/evidence/verdict-r4-20261015T173551Z-sniffer-v2.log`).
   The counter mutates only `$WORK`, never the fingerprinted `CASE_DIR`, so the
   read-only guard does not see it.

Measured by this seat at the r4 bytes (`/tmp/mori-vnw-r5/before/`, pinned
`be0e28b8…` + `af2d4e79…`, shas verified before/after):

| attacker | tally | note |
|---|---|---|
| critic's `sniffer-v3.sh` `ba2a11ba…` (verbatim) | **`matched=28 total=28` exit 0** | canonical round-4 attacker, re-run by me (`before/critic-v3-before.out`) |
| my self-agreeing counter `2446f697…` | **`matched=28 total=28` exit 0** | answers positions 28 and 29 identically so shape-invariance agrees with itself |
| v2b verbatim `fb9faf44…` (round-4 receipt source) | `matched=27 total=28` exit 1 | its single FAIL is `shape-invariance` — a one-line difference in the attacker's table (`before/v3-counter.out`) |
| record-once/replay-by-position (`0987dbf8…`) | run 1 (record, proxies the census) 28/28; **run 2 (pure replay) 28/28 exit 0** | the recorded transcript *is* a valid answer for every position (`before/replay-r2.out`) |

So the honest statement of the round-4 residual, measured: **a zero-logic
census could reach the ceiling**, and shape-invariance caught only the variants
that disagreed with themselves between the two shape runs — a choice of the
attacker, not a property of the oracle
(`corpus/knowledge/verdict-machine-r4.md` §2.4).

## 2. The r5 design — seeded shuffle + independent per-run nonce

Both mechanisms live in the oracle only; the census was not touched (frozen
sha verified before/after every run).

### 2.1 Seeded shuffle of a case registry

- The 28 cases are functions `case_<id with '-'→'_'>` and a registry array
  `CASE_IDS` in source order (`:902-931`); the runner executes
  `"case_${case_it//-/_}"` for each id **in the shuffled order** (`:958-960`).
- The shuffle is Fisher-Yates in place over the 28 ids, driven by a local
  xorshift32 `xs32()` (`:936-942`; Marsaglia constants, 32-bit masked),
  `shuffle_case_ids()` (`:944-951`).
- Entropy: `rand32()` (`:142-153`) draws 4 bytes from `/dev/urandom`
  (`od -An -N4 -tu4`), with a `RANDOM`/`$$`/`date +%s` fallback if urandom is
  unreadable; a draw of 0 is rejected (`:160`, `:166`) so the xorshift32 state
  is never 0.
- The header is printed before the first case and logs everything a re-run
  needs (`:954-956`): `SHUFFLE_SEED=<seed>`, `RUN_NONCE=<nonce>`,
  `CASE_ORDER=<id> <id> …`.

### 2.2 Per-run nonce, independent of the seed

- `RUN_NONCE` is a second, independent `rand32()` draw (`:161-167`) — the
  header comment says so (`:132-141`) and the code path confirms it: two
  separate `rand32` calls, no derivation from `RUN_SEED`. Guessing the order
  seed therefore does not reveal the nonce.
- The token is `NONCE_TOKEN="nonce-<RUN_NONCE>"` (`:167`) and it is planted in
  **every** fixture by `case_skeleton()` (`:226-227`): a `$CASE_DIR/run-nonce`
  file and a `$CASE_DIR/nonce-<N>` directory — both under `CASE_DIR`, i.e.
  never untracked files inside a graded repo.
- It reaches the census three ways (`run_census`, `:377-378`): as the
  `MORI_DISK_TARGETS` path (`"$CASE_DIR/$NONCE_TOKEN"`), as the exported
  variable `MORI_RUN_NONCE`, and through the fixture tree itself.
- The **frozen census echoes it without any census change**: the disk surface
  renders `targets=$DISK_TARGETS` verbatim (`tools/mori-census.sh:516-518`,
  measured `targets=/tmp/mori-silence-cases.eySu93/case.yrddkQsB/nonce-626021442`
  at `RUN_NONCE=626021442`). A wrapper run that captured all 29 census outputs
  found the current token in **29/29** of them (`/tmp/mori-vnw-r5/tee/`).
- Grading: `nonce_present()` (`:427`) is a literal substring check on the
  case's census output; `assert_case` requires it (`:493`, failure text
  `run-nonce want=[…] missing (canned/replayed output?)`), and both the
  read-only guard (`:837`) and the shape case (`:886`, both shape runs) now
  assert it too.

### 2.3 The seed contract

- Order pin: `MORI_SHUFFLE_SEED=<non-negative int>` (`:155-160`). Same seed ⇒
  same `CASE_ORDER`. The seed is deliberately **not exported to the census**
  (comment `:126-131`); measured below.
- Nonce pin: `MORI_RUN_NONCE=<non-negative int>` (`:161-166`), documented as
  the reproducibility pin only.
- With both pins set the run is fully reproducible: two runs at
  `MORI_SHUFFLE_SEED=12345 MORI_RUN_NONCE=99` produced **byte-identical**
  output (`diff` empty, `/tmp/mori-vnw-r5/after/pin-1.out` vs `pin-2.out`).
- Non-integer pins abort with exit 2 (`:158`, `:164`) — setup failures stay
  distinct from case verdicts.

What each half defends against:

| defense | closes | does not close |
|---|---|---|
| shuffle | position-keyed canned sequences (v2b/v3a-class, v3b, critic v3) | any attacker that *reads* the seed (see §4) |
| nonce gate | transcript replay — a recorded previous run carries a stale (or absent) token; canned answers carry none | a live attacker: `MORI_RUN_NONCE` is exported to the census by design, so echoing the current token is one line |
| both together | every attacker in the round-5 receipts and in §3 | §4's seed channels, and content-keyed memorization |

## 3. Measured after-side (pinned `7143ccc2…` × frozen `af2d4e79…`)

Honest side (`after/honest-h1..h4.out`, `honest-final.out`; receipts
`order-r5-20261015T180431Z-oracle-{1,2,3}.log`):

| probe | result |
|---|---|
| `bash tools/mori-silence-cases.sh` (fresh seed+nonce) ×5 | `matched=28 total=28` exit 0 every run |
| orders across fresh runs | distinct every time (my h1-h4: four distinct `CASE_ORDER` shas `cdeb838a…`, `b43253f7…`, `adb26c83…`, `105821ce…`; receipts oracle-1 vs oracle-2 differ) |
| same seed (`MORI_SHUFFLE_SEED=12345`) ×2 | identical `CASE_ORDER` (`3082a33651bc1ab2…`); seed `54321` gives a different order (`76d6ca0b2ca15a3d…`); receipts oracle-1 vs oracle-3 (pinned to oracle-1's seed) reproduce the same order |
| per-case grade tuples across shuffled runs | `PASS` lines sorted by case id hash `a70af583bb01b8362a49f07aa8f2b66814fac22b119a22f9b273c5024573c752` in **all** of my runs (5 honest + 2 seed-pinned + 2 fully pinned) and in the receipts' three runs — byte-identical tuples across shuffled orders, as claimed |

Attack side (my runs; the receipts' independent set in parentheses):

| attacker | vs r4 oracle | vs r5 oracle | where |
|---|---|---|---|
| critic `sniffer-v3.sh` `ba2a11ba…` | `28/28` exit 0 | **`0/28` exit 1** | `after/atk-critic-v3.out` |
| self-agreeing counter `2446f697…` | `28/28` exit 0 | **`0/28` exit 1** | `after/atk-v3b-selfagree.out` |
| v2b verbatim `fb9faf44…` | `27/28` exit 1 | `0/28` exit 1 | `after/atk-v2b-verbatim.out` |
| positional table + **live nonce echo** (`b5600a1a…`) | n/a | `6/28` exit 1 — 6 positional coincidences | `after/atk-nonce-echo.out` (receipt v3d: `6/28`, same class) |
| record-once replay `0987dbf8…` | run2 `28/28` exit 0 | run2 `0/28`, run3 `0/28`, exit 1 | `after/atk-replay-r2/r3.out` |
| stale-token replay (receipt v3e) | n/a | `0/28` exit 1 | `order-r5-…-sniffer.log` |

The failure texts show the two defenses independently: canned attackers fail
with `run-nonce want=[nonce-…] missing` on **every** assert case *and* on the
read-only and shape cases; the live-nonce attacker passes the nonce gate
everywhere but fails on shuffled-state mismatch (e.g. `state want [progressing]
got [silent]`).

Reachability of the two secrets from inside the fixture (my probes, matching
the receipts' channel probe):

| channel | `SHUFFLE_SEED` | `RUN_NONCE` |
|---|---|---|
| census env (`env` inside the SUT, 29 invocations) | 0/29 | 29/29 (exported by design) |
| fixture tree + `$WORK` top-level listing | absent | present (by design) |
| oracle process environ `/proc/<ppid>/environ`, **unpinned run** | 0/29 | 0/29 |
| oracle process environ, **`MORI_SHUFFLE_SEED=31337` pinned** | **29/29** | 0/29 |

## 4. Residuals — named, with witnesses

These are this seat's findings beyond the round-5 claim; they do not negate the
measured closures in §3, but they bound them.

**R1 — a pinned seed is readable by the SUT.** The reproducibility pin arrives
through the environment, so in a pinned run the pin sits in the oracle's own
process environ; a cheating census reads it at `/proc/<ppid>/environ`. Witness:
`/tmp/mori-vnw-r5/sniffer-v5-seedreader.sh` (`3969ce3b…`) — reimplements the
oracle's xorshift32 Fisher-Yates from the **read** seed, maps its invocation
index to the case id, replays a canned table and echoes `MORI_RUN_NONCE`:

```
$ bash oracle-r5.sh sniffer-v5-seedreader.sh            # unpinned
MORI_SILENCE_CASES: matched=1 total=28   exit 1         # seed unreachable; only shape passes
$ env MORI_SHUFFLE_SEED=31337 bash oracle-r5.sh sniffer-v5-seedreader.sh
MORI_SILENCE_CASES: matched=28 total=28  exit 0         # seed read from /proc
```

**R2 — the logged seed is readable through a captured stdout.** The oracle
prints `SHUFFLE_SEED=` to its stdout by design (`:954`), and in any run whose
stdout is redirected to a **regular file** — the standard receipt/CI pattern —
the census can walk its ancestry (`/proc/<pid>/stat` field 4) to the oracle
shell, whose `fd/1` is that file, and read the current seed from the header,
which is written before the first case runs. Witness `sniffer-v5c-ancestorfd.sh`
(`fc26c9f3…`, unpinned, regular-file capture): `matched=28 total=28` exit 0,
reproduced on three fresh seeds (`after/atk-v5c-{unpinned,unpinned-r2,file2}.out`).
Scope: with a **pipe** capture the ancestor `fd/1` is a pipe and not readable
this way (`1/28` exit 1, `after/atk-v5c-pipe2.out`); on a tty the naive
ancestor-walk *blocks* reading the terminal — the fixed probe reads only
regular files, so it degrades to `1/28` rather than hanging. What R1 and R2
mean together: the shuffle closes position-keyed replay **only while the seed
stays out of the attacker's reach**, and the oracle's own reproducibility
header puts it into the capture file that the SUT can open through `/proc`.
This is named, not remediated (detection/report only; the fix — e.g. log a
seed hash instead of the seed, or keep the pin out of the SUT-visible process
tree — is the parent's call).

**R3 — the nonce alone is a thin gate.** `MORI_RUN_NONCE` is SUT-visible by
design, so a live attacker echoes the token; measured, that alone still yields
only `6/28` (positional table) — the load-bearing closure is the shuffle, and
the nonce's real job is killing stale replays (transcript replay `0/28`).

**R4 — carried from round 4, unchanged:** a forger keyed on fixture *content*
(memorize content→expectation) is not closed by any of this, only made
expensive (`corpus/lessons/2026-10-15-forgeable-oracle-visible-fixtures.md`,
Limits); the frozen-behavioral drift pin is still absent; row 6 (committed
report) still checks presence + commit window only.

**Independent corroboration (lessons-distiller, same wave).**
`corpus/lessons/2026-10-15-run-order-spoofing-shuffle-nonce-limits.md`
reaches the same two residuals from a different attacker set and adds one
sharper measurement: an order-aware attacker with the correct per-case states
but only a **stale** token scores `0/28` with all 28 FAILs citing `run-nonce`
(0 citing `state`) — i.e. the nonce gate alone killed a state-perfect replay;
and a **content memorizer** (fixture-content fingerprint → expectation, token
echoed) reaches `28/28` at three different seeds, which is R4 made concrete at
the r5 bytes.

## 5. Scratch inventory (re-run material, `/tmp` only)

| file | sha256 (prefix) | role |
|---|---|---|
| `oracle-r5-7143ccc2…sh` | `7143ccc2a1422171` | pinned r5 oracle snapshot (all after-side runs) |
| `oracle-r4-be0e28b8.sh` | `be0e28b8bf3cc34e` | pinned r4 oracle snapshot (all before-side runs) |
| `census-frozen-af2d4e79.sh` | `af2d4e79e69b70bb` | frozen census snapshot |
| `sniffer-v3-counter.sh` | `fb9faf442a14202d` | v2b verbatim (round-4 receipt source) |
| `sniffer-v3b-selfagree.sh` | `2446f6976c54f7cb` | self-agreeing positional counter |
| `sniffer-v4-nonce-echo.sh` | `b5600a1ae945f055` | positional table + live nonce echo |
| `sniffer-replay.sh` | `0987dbf811cd7291` | record-once/replay-by-position |
| `sniffer-v5-seedreader.sh` | `3969ce3b0722339f` | reads the pin from `/proc/<ppid>/environ` |
| `sniffer-v5c-ancestorfd.sh` | `fc26c9f30b427bc9` | reads the seed from an ancestor's captured `fd/1` |
| `probe-env-dump.sh` / `probe-leak.sh` / `probe-chain.sh` | `04609fda…` / `4e749ef5…` / `4c95f7af…` | SUT-visibility probes |

Re-run recipe (cwd = lane root; applies only at the SHAs at the top of this
note):

```sh
sha256sum tools/mori-silence-cases.sh   # must equal 7143ccc2… for this note
sha256sum tools/mori-census.sh          # must equal af2d4e79…
bash tools/mori-silence-cases.sh        # expect exit 0, matched=28 total=28
MORI_SHUFFLE_SEED=12345 bash tools/mori-silence-cases.sh   # expect the same order as another seed-12345 run
bash tools/mori-census.sh --selftest    # expect PASS (30 cases, 30 passed, 0 failed)
```

If either tool changes from the hashes above, re-measure everything here.

## 6. Final pinned tallies and receipts

| probe | before (`be0e28b8` / `af2d4e79`) | after (`7143ccc2` / `af2d4e79`) | receipt / measurement |
|---|---|---|---|
| `bash tools/mori-silence-cases.sh` | `matched=28 total=28` exit 0 | `matched=28 total=28` exit 0, ×5 + receipts ×3 | `order-r5-20261015T180431Z-oracle-{1,2,3}.log`; my `after/honest-*.out` |
| sorted per-case tuples across orders | n/a (one order) | sha `a70af583…573c752` in every run | receipts oracle-1..3 + my five runs |
| critic v3 `ba2a11ba…` | `28/28` exit 0 | `0/28` exit 1 | my `before/` + `after/`; receipt sniffer v3a-class `0/28` |
| self-agreeing counter | `28/28` exit 0 | `0/28` exit 1 | my runs; receipt v3b `0/28` |
| record-once replay | `28/28` exit 0 (replay run) | `0/28`, `0/28` exit 1 | my `after/atk-replay-*` |
| live-nonce positional attacker | n/a | `6/28` exit 1 | my `atk-nonce-echo.out`; receipt v3d `6/28` |
| stale-token attacker | n/a | `0/28` exit 1 | receipt v3e (`order-r5-…-sniffer.log`) |
| seed via `/proc` environ (pinned) | n/a | `28/28` exit 0 (R1 witness) | `after/atk-v5-pinned.out` |
| seed via captured stdout `/proc` fd (unpinned) | n/a | `28/28` exit 0 ×3 (R2 witness) | `after/atk-v5c-*.out` |
| `bash tools/mori-census.sh --selftest` | PASS 30/30 exit 0 | PASS 30/30 exit 0 (census frozen) | `order-r5-20261015T180431Z-selftest.log` |
| live census | r4: `DRIFT (findings=15 …)` | `MORI_CENSUS: DRIFT (findings=15 drift=14 unavailable=1 surfaces=7)` exit 1, 9/9 lanes `progressing`, 0 `LANE_SILENT`, two spots identical | `order-r5-20261015T180431Z-live.log` |

## 7. Limits

- Everything here is measured against two pinned SHAs; the census is frozen
  this round, so the nonce mechanism rides entirely on the oracle's export
  list and the census's existing disk-row echo (`tools/mori-census.sh:516-518`).
- R1/R2 are channel measurements with witnesses, not claims that any real
  census used them; §4 also notes R2 does not apply to pipe captures and that
  a naive tty ancestor-walk blocks (a hanging attacker is a tell, not a pass).
- Live figures are a pinned clock, not a baseline; no causal claim about fleet
  liveness; no admission or axis verdict (parent), no scalar score, no
  remediation.
