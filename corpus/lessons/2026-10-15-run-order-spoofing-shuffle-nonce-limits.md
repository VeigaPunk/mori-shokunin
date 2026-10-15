# Lesson — closing a spoofing channel moves the attack: seeded shuffle + per-run nonce, and the two forgers that still reach 28/28

date: 2026-10-15 · lane: mori-shokunin · round: 5 · source seat: lessons-distiller
(flash wave) · write scope: this file only; detection and report only, nothing here
remediates a fleet process.

Measured against the round-4 oracle `tools/mori-silence-cases.sh` sha256
`be0e28b8bf3cc34e2a35e6cea7c05bffff376111b42d985b6bec7f0e21f59456` (git HEAD bytes; the
round-4 note pinned the same hash, `corpus/knowledge/verdict-machine-r4.md:12`) and the
round-5 revision sha256
`7143ccc2a14221713334c33ade56e24ca711fbd0d3d17f31d33e151be544f017` (working tree at
18:04–18:11Z, stable since 18:03:36Z). Census frozen at `af2d4e79e69b70bb0b5aecd6acc9608fc7c16b0716766d4a60310e0689d350d7`
(`VERSION=census-r3`), unchanged throughout. All scratch under `/tmp/mori-lessons-r5/`;
every figure carries its sha. If either tool byte changes, re-measure.

## The lesson

This lane has now run the same experiment three rounds in a row, and the result is a
pattern worth naming: **each hardening closed the attacker class it was aimed at and
moved the attack to the next stable, SUT-visible regularity.**

- Round 3–4: the fixture path embedded the case id, so a no-logic census replayed the
  answer key (`corpus/lessons/2026-10-15-forgeable-oracle-visible-fixtures.md`).
- Round 4 residual (registered in `verdict-machine-r4.md` §2.4): cases still ran in
  **fixed order** and carried **no per-run secret**, so a census that counted its own
  invocations and replayed a canned grade sequence reached `matched=28 total=28`, exit 0.
- Round 5 (this round) added **seeded Fisher-Yates shuffle of case order** + a **per-run
  nonce every case must echo**. Measured: the enumerated attack classes all die — but
  **two forgers still reach `28/28` exit 0**: a fixture-content memorizer, and a
  run-header leak read from the oracle's own process while it runs.

Three durable statements, each with a measurement behind it:

1. **A spoofing channel is any SUT-visible regularity that is stable across runs** —
   paths, order, content, and now the harness's own run header. Closing one leaves the
   others.
2. **Echoing a per-run secret authenticates freshness, not measurement.** The nonce
   check (`tools/mori-silence-cases.sh:427`, gate `:491-493`) tests that the output
   *contains* the current token. Any attacker that can read the environment can echo it
   (`MORI_RUN_NONCE` and the token-bearing `MORI_DISK_TARGETS` are in the census env by
   design, `:377-378`). A memorizer that replays a canned row **plus the env token**
   passes; only a *stale or missing* token fails.
3. **Entropy that does not change the correct answer does not stop memorization.** The
   shuffle randomizes *which case runs when*; the nonce randomizes *an accompanying
   token*. Neither changes *what the right grade is*. One observation of a run is enough
   to build (fixture → row), and the replay is immune to both defenses. The round-4
   lesson predicted exactly this ("only randomizing fixture parameters makes memorization
   cost approach real logic") — the round-5 nonce is one randomized parameter, and it is
   not the load-bearing one.

## What was measured (2026-10-15, ~18:01–18:11Z, /tmp/mori-lessons-r5/)

Oracle pre-impl = `be0e28b8…`, r5 = `7143ccc2…`; census = `af2d4e79…` throughout.
`before-*` outputs are this seat's runs at the pre-impl bytes; `after-*` at the r5 bytes.

| probe (sha of the program) | oracle | result |
|---|---|---|
| honest census (`af2d4e79…`), 1 run before | `be0e28b8…` | `matched=28 total=28`, exit 0 (`before-honest.out` `a502b35d…`) |
| honest census, 5 runs after (2 unseeded, same-seed ×2, seeds 1/2) | `7143ccc2…` | `matched=28 total=28`, exit 0 each; sorted per-case grade tuples **byte-identical across all 5**; each `CASE_ORDER=` a 28-id permutation; same seed ⇒ identical order; different seeds ⇒ different orders |
| honest census, seed+nonce pinned, 2 runs | `7143ccc2…` | full stdout byte-identical (`pinned-1/2.out` `be8b303c…` both) |
| run-order replay sniffer v3 (`29cb09ce…`, counts own invocations, reads no fixture) | `be0e28b8…` | **`matched=28 total=28`, exit 0** (`before-sniffer-v3.out` `be33047a…`) |
| v3, same bytes | `7143ccc2…` | `matched=0 total=28`, exit 1 (`after-sniffer-v3.out` `ba8c11ec…`) |
| v2b counter sniffer (`fb9faf44…`) | `be0e28b8…` | `matched=27 total=28`, exit 1 (shape-invariance only) |
| v2b, same bytes | `7143ccc2…` | `matched=0 total=28`, exit 1 |
| m4b / m4c case-id attackers (round-3 mutants) | `7143ccc2…` | `matched=0 total=28`, exit 1 each |
| order-aware attacker, perfect table for seed 777, **stale** token (`04e3171d…`) | `7143ccc2…` | `matched=0 total=28`, exit 1 — **28 FAIL lines cite `run-nonce`, 0 cite `state`**: the states were all correct; the nonce alone failed every case |
| order-aware attacker, same table, **echoes** env token (`0bd200d3…`) | `7143ccc2…`, seed 777 | `matched=28 total=28`, exit 0 — proves the nonce is echo-able and the shuffle's protection is exactly seed secrecy |
| same echo attacker, wrong seed 424242 | `7143ccc2…` | `matched=4 total=28`, exit 1 — guessing the order fails |
| **content memorizer** (`3e0fa4c7…`; table learned from one observed run; F = hash of every fixture file minus `.git/index` minus the nonce artifacts; echoes env token) | `7143ccc2…` | **`matched=28 total=28`, exit 0 at seeds 424242, 987654321, and unseeded** (`67275e0e…`, `87182b6e…`, `8715566b…`) |
| **header-leak attacker** (`3f05915c…`; reads `CASE_ORDER=` from the oracle's own stdout via `/proc/<gp>/fd/1` at runtime, replays the public table, echoes env token; reads no fixture) | `7143ccc2…` | stdout redirected to a file: **`matched=28 total=28`, exit 0** (`leak-attack-A.out` `94d1fb6b…`); stdout piped: `matched=0 total=28` (`leak-attack-B.out` `0f72679d…`) |
| /proc probe (`b7e7f520…`) | `7143ccc2…` | redirect mode: first invocation read `SHUFFLE_SEED=777` **and the full `CASE_ORDER=…`** from `/proc/<gp>/fd/1`; pipe mode: `<nothing>` |
| /proc environ probe (`f4a92936…`) | `7143ccc2…` | pinned run: `MORI_SHUFFLE_SEED=777` readable from `/proc/<gp>/environ` **in pipe mode too**; unseeded run: absent |

Verbatim, the two ends of the round's claim:

```
# pre-impl oracle be0e28b8…, run-order sniffer v3 (no fixture reads at all)
PASS shape-invariance
MORI_SILENCE_CASES: matched=28 total=28
EXIT 0

# r5 oracle 7143ccc2…, same sniffer
FAIL same-round-relaunch-silent: run-nonce want=[nonce-3603073599] missing (canned/replayed output?)
MORI_SILENCE_CASES: matched=0 total=28
EXIT 1

# r5 oracle, order-aware perfect table but stale token — every FAIL is the nonce alone
FAIL shape-invariance: run-nonce want=[nonce-893724484] missing in a shape run (canned/replayed output?)
MORI_SILENCE_CASES: matched=0 total=28
EXIT 1        (grep -c run-nonce = 28; grep -c 'state want' = 0)

# r5 oracle, header-leak attacker, stdout redirected to a file (receipt pattern)
MORI_SILENCE_CASES: matched=28 total=28
EXIT 0
```

## The r5 defenses and what each closes (file:line at `7143ccc2…`)

- **Seeded shuffle** — Fisher-Yates over the 28-id registry (`:902-931`) driven by a
  local xorshift32 (`:936-942`, `:944-951`), called before the runner (`:953`); the seed
  is logged (`:954`) and pinnable via `MORI_SHUFFLE_SEED` (`:155`); the runner never
  executes source order (`:958-960`). Closes: position-keyed tables (v3 0/28) and
  wrong-guess attacks (4/28). Same seed ⇒ same order; unseeded runs vary (measured).
- **Per-run nonce** — `rand32()` (`:142`), `RUN_NONCE` pinned or generated (`:161-166`),
  `NONCE_TOKEN=nonce-<N>` (`:167`); written into every fixture (`:226-227`) and handed
  to the census as its disk target (`:377`) and env (`:378`, by design); the frozen
  census echoes it in its own disk row (`tools/mori-census.sh:518`, and `:516` when the
  target is absent). Every case requires the current token: `assert_case` (`:427`,
  `:491-493`), readonly (`:837`), shape (`:886`). Closes: recorded-run replay (stale
  token) and canned answers (missing token) — with clean isolation (see table).
- **Honest census unaffected** — 28/28 exit 0 at every seed; per-case grade tuples
  identical across shuffles; pinning seed+nonce reproduces byte-identical runs.

## The two forgers that still reach 28/28

### A. Content-keyed memorizer (`fp-attacker.sh`, `3e0fa4c7…`)

One observed run is enough. The learner (`fp-learner2.sh`, `b2238ef3…`) records, per
invocation, F = sha256 over every file's relative path+size+content under the case tree,
excluding `run-nonce`, the `nonce-*` directory, and `.git/index` (the index embeds file
ctimes and is volatile; the rest of the fixture is byte-stable across runs — measured:
the F multisets of two runs at different seeds are identical). The attacker then maps F →
a canned row (learned from the honest census's own output), prints it, and echoes
`$MORI_DISK_TARGETS` so the nonce check passes. Measured `matched=28 total=28` exit 0 at
three different seeds. It reads the fixture (that is its cost) and implements **zero
grading logic**. Nothing in r5 changes the fixture→answer mapping, so the replay is
immune to both defenses. Note the lane's own receipts contain the full expected states
in plain text (`corpus/evidence/verdict-r4-20261015T173551Z-*.log`), so the learning
half of this attack is already public.

### B. Run-header leak via /proc (`attacker-leak.sh`, `3f05915c…`)

The oracle prints `SHUFFLE_SEED`, `RUN_NONCE`, and the full `CASE_ORDER` to its own
stdout **before any case runs** (`:954-956`). A same-user SUT can walk to the oracle
process (grandparent of the census, visible as ppid of ppid in `/proc/<pid>/stat`) and
read its stdout through `/proc/<gp>/fd/1`. When stdout is a regular file — every
`> log` or `tee file` receipt — the first census invocation reads the run's exact
shuffled order and the seed (measured, `probe-leak2.sh`). The attacker then maps
invocation position → id → the public want table and echoes the env nonce: `28/28`,
exit 0, **with no fixture reads and no grading logic**. Piped stdout closes this channel
(0/28). Second sub-channel: when the operator pins `MORI_SHUFFLE_SEED` for
reproducibility (the documented feature, `:155`), the pin is in the oracle process's
environment and readable via `/proc/<gp>/environ` **in any stdout mode** (measured in
pipe mode); unseeded runs do not expose it. So the comment "Never exported to the
census: the SUT must not be able to read the order" (`:130`, cf. `:353`) is true of the
*census environment* but not of the *process*: "not exported" is not "not reachable".

## Why it is easy to miss

- The defenses were validated against the enumerated attacker list (invocation-count,
  canned sequence, stale nonce, wrong-guess) and each closes exactly those. The class
  ("replay") is wider than the list: add a content-keyed lookup, an env-token echo, and
  a process-walk to every threat model.
- The tally is green in both directions again — honest census 28/28 **and** both forgers
  28/28. Only deliberately cheating SUTs separate them; a mutant-based check (making the
  SUT worse) never finds this class, as the round-4 lesson already said.
- The leak is created by an audit/reproducibility feature (logging the run's entropy)
  and exploited with an OS-level move (/proc) outside the harness's own I/O surface. The
  harness authors' mental model is "what do I export to the child"; the attacker's is
  "what can a same-user process read from its parent".
- The nonce tests presence, not provenance. An attacker reading the environment was
  never excluded by "the SUT must not read the fixture" — it does not need the fixture.

## Countermeasures that fit this codebase (the next move, not applied here)

1. **Make the correct answer vary with per-run randomness.** The only measured class
   that survives everything is the memorizer, because the expected states are constant.
   Randomize state-bearing fixture parameters per run (ledger epochs/rounds, mission
   structure, which branch of a want-set is correct) so that a (fixture → row) table
   learned yesterday is *wrong* today, and the forgery must then actually measure.
2. **Treat the run's own process surface as SUT-readable**: `/proc/<pid>/fd/*`,
   `/proc/<pid>/environ`, `/proc/<pid>/cmdline` for any process of the same user. Do not
   print run secrets to a stream that lands in a file while the graded process runs; log
   the entropy *after* the run, or keep it only in shell variables (not env, not argv,
   not files) — and know that a pinned seed handed through argv or env is readable in
   any output mode.
3. **Keep a capability-indexed forgery repertoire**: no-read replay (done), env-token
   echo (done), content-hash lookup (done here), process-walk (done here). Re-run all of
   them after every hardening and write down which still pass — that list *is* the
   security statement.
4. **Verify isolation, not just scores.** The stale-token row (0/28, zero state
   mismatches) is what proves the nonce is load-bearing; the 28/28 leak row is what
   proves it is not sufficient.

## Applying it (any lane)

- List every value the SUT can see (paths, env, argv, cwd, siblings, timing) **and**
  every value it can read from its ancestry (`/proc`). For each: is it stable across
  runs, and can it be mapped to expected output? If yes, a table attacker exists.
- When you add entropy, state precisely which attacker capability it removes. "The SUT
  cannot see X" must name the channel ($env ≠ /proc ≠ file ≠ argv).
- If you echo a secret to prove freshness, assume the attacker echoes it too; only use
  it to kill *stale* material, never as proof of work.
- Rebuild the memorizer from one observation of your own harness; if it passes, your
  suite still grades memory — not behavior.

## Limits

- Single host, GNU bash 5.3.15, same-user attacker, no ptrace needed for the /proc
  reads here (fd/environ are world-readable to the owner).
- The memorizer needs one observed run and a fixture that is byte-stable across runs
  (excluding `.git/index`, whose ctime field is volatile; worktree and git objects are
  stable — measured across two runs at different seeds). It reads the fixture content;
  that cost, not capability, is what distinguishes it from the round-4 no-read sniffers.
- The header-leak attack is mode-dependent (regular-file stdout); the pinned-seed
  environ leak is mode-independent but requires the operator to pin the seed. Unseeded
  pipe-mode runs exposed neither (measured).
- Not measured: coarser fingerprints (file counts/sizes alone), `/proc/<pid>/mem`
  (ptrace) leakage when all fds are pipes, and any non-Linux /proc semantics.
- All figures pinned to `be0e28b8…` / `7143ccc2…` / `af2d4e79…`; the r5 tool was a
  working-tree revision at measurement time.
- No liveness or remediation claim; this is a report of measured attacks, nothing more.

## Repro (scratch, /tmp/mori-lessons-r5/)

- Before: `cp tools/mori-silence-cases.sh oracle-preimpl.sh` (or `git show
  HEAD:tools/mori-silence-cases.sh`); `bash oracle-preimpl.sh census-frozen.sh` →
  28/28; `bash oracle-preimpl.sh sniffer-v3-runorder.sh` → 28/28 exit 0.
- After: `bash tools/mori-silence-cases.sh [prog]` at `7143ccc2…`. Attackers:
  `sniffer-v3-runorder.sh` `29cb09ce…`, `attacker-order-stale.sh` `04e3171d…`,
  `attacker-order-echo.sh` `0bd200d3…`, `attacker-leak.sh` `3f05915c…`,
  `fp-attacker.sh` `3e0fa4c7…` (learn with `fp-learner2.sh` `b2238ef3…` first, then
  `python3 gen-attacker.py` regenerates the table from the learned map), probes
  `probe-leak2.sh` `b7e7f520…` / `probe-environ.sh` `f4a92936…`.
- Pinned determinism: `env MORI_SHUFFLE_SEED=777 MORI_RUN_NONCE=55555 bash
  tools/mori-silence-cases.sh tools/mori-census.sh` → byte-identical reruns
  (`be8b303c…`).