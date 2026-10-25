# Lesson — a run secret has a *time* and a fixture has a *shape*: the r6 backchannel/freshness closures, and the pattern-normalizing memorizer that still reaches 28/28

date: 2026-10-15 · lane: mori-shokunin · round: 6 · source seat: lessons-distiller
(flash wave) · write scope: this file only; detection and report only, nothing here
remediates a fleet process.

Measured against three pinned revisions of `tools/mori-silence-cases.sh`:

| revision | sha256 | role |
|---|---|---|
| r5 oracle (before) | `7143ccc2a14221713334c33ade56e24ca711fbd0d3d17f31d33e151be544f017` | git HEAD bytes; round-5 admission |
| r6 oracle (measured) | `b2ebe5e7fce787713fa27aca088817d90c40f98b889d4da4b6ccd1bc4e092314` | snapshot I measured (stable 4×30 s checks 19:01–19:03Z) |
| r6 oracle (final) | `3307761a04a1eab8f33859a69d2eb63fb6312afb8f8041f7b09da4544be174b9` | lane bytes at 19:08:52Z; **diff vs `b2ebe5e7…` is comment-only (13 diff lines, 0 code lines)** — every after-side figure below therefore holds at both; line numbers cited are the final revision's |

Census `tools/mori-census.sh` frozen at
`af2d4e79e69b70bb0b5aecd6acc9608fc7c16b0716766d4a60310e0689d350d7` — re-verified
byte-identical before and after every run. All scratch under `/tmp/mori-lessons-r6/`
(the interrupted earlier dispatch of this wave left R1/R2 before-side artifacts in the
same directory; `before/r1-leak.out`, `before/r2-mem*.out` independently reproduce the
same 28/28 before-tallies, so the before side is double-sourced). If either tool byte
changes, re-measure everything here.

## The lesson

Four durable statements, each with a measurement behind it:

1. **When a run secret is emitted is part of the secret.** "Not exported to the SUT"
   (round-5 lesson) did not survive `/proc` ancestry: a census reads the oracle's run
   header from the oracle's captured stdout *while it runs* — and the reproducibility
   pins from the oracle's process environ. Round 6 removes the secret from every
   SUT-readable surface while any census invocation lives (header printed only after
   the loop; pins moved out of the exec-time environ by a one-time self re-exec;
   failure texts redacted). Both channels measured closed (table below).
2. **Echoing a per-run secret authenticates freshness, not measurement** (r5, still
   true) — and round 6 adds: **freshness woven into fixture *content* re-prices
   memorization rather than closing it.** The naive memorizer dies; an attacker that
   treats the randomized annotation bytes as noise to normalize away still reaches the
   ceiling with zero grading logic, because the salt changes *bytes*, not *answers*.
3. **A fingerprint has derived components.** File *size* changes with the nonce's digit
   count (the annotation length is data-dependent), so a size-keeping memorizer's keys
   go stale intermittently — its success can depend on whether two runs drew e.g.
   9-digit vs 10-digit nonces. Measured both ways below; normalize every run-dependent
   component before claiming a closure either direction.
4. **Each hardening closes the enumerated class and moves the attack** (r3 path → r4
   order → r5 header/seed + content → r6 timing/freshness). The attacker list you
   re-run after each hardening *is* the security statement; the surviving member is the
   next round's claim.

## What was measured (2026-10-15, /tmp/mori-lessons-r6/)

`before-*` outputs are this seat's runs at `7143ccc2…`; `after/final-*` at the r6
bytes above. All tallies are the oracle's own `MORI_SILENCE_CASES` line.

| probe (source sha256 prefix) | before `7143ccc2…` | after r6 | where |
|---|---|---|---|
| honest census, 2 fresh-seed runs | `matched=28 total=28` exit 0 | `matched=28 total=28` exit 0 ×2; sorted PASS tuples **byte-identical** sha `a70af583bb01b8362a49f07aa8f2b66814fac22b119a22f9b273c5024573c752` (same tuple hash as r5); registry 28 ids identical across runs | `final-battery.log` |
| R1 header-leak census (`0ee8525b…`, file-captured stdout, no fixture reads) | `matched=28 total=28` **exit 0** | `matched=8 total=28` **exit 1** (8 = the progressing-want cases + readonly + shape scoring by blind fallback) | `before-r1.out`, `final-battery.log:28-31` |
| R1 pinned-seed environ reader (`4f2bcf03…`, pipe **or** file stdout) | `matched=28 total=28` **exit 0** (`MORI_SHUFFLE_SEED=777`) | all-FAIL, **exit 1**; probe: `seed=[]` at every ancestor from invocation 1 (`SEEDREAD n=1 seed=[]`) | `before-r1-seedreader.out`, `final-battery.log:35-39` |
| R2 content memorizer, naive (`57798c89…`: relpath+size+content, excludes `.git/index` + `run-nonce`) | `matched=28 total=28` **exit 0**, 29/29 content hits, 0 misses | 0/29 hits — stale table 0/29; fresh-learn-at-r6 then replay 0/29; both exit 1 | `before-r2-attack.out`, `final-battery.log:40-50` |
| R2 nonce-normalizing variant (`44051479…`: strips `nonce-N`/bare N before fingerprinting) | n/a | 0/29 hits, exit 1 (the unannounced salt survives normalization) | `final-battery.log:53-58`; corroborated by receipts `backchannel-r6-20261015T190453Z-attack-r2.log` LEG `r2-normalize-replay-r6` exit 1 |
| **R2 pattern-normalizing memorizer (`6b79f776…`)** | n/a | **`matched=28 total=28` exit 0, 29/29 content hits, 0 misses** | `final-r2u-attack.out`, `final-battery.log:81-87` |
| content probe: fixture files containing `nonce-<N>` | 0 files (all 29 invocations) | 1–3 files per case (`root/.../LOG.md`, `notes.md`, scratch, report, README) | `before-probe-content.out`, `final-battery.log:62-68` |
| header probe: oracle `/proc/<oracle>/fd/1` head mid-run | `SHUFFLE_SEED=…|RUN_NONCE=…|CASE_ORDER=…` readable at INV=1 | empty at INV=1; later only redacted FAIL text (no token value) | `before-probe-header.out`, `final-battery.log:69-77` |
| fingerprint F multiset, learn run vs attack run | identical across runs (29/29 common; r5 lesson also measured this) | disjoint (29 vs 29, common=0) — content is per-run | `final-battery.log:51-52` |

Regression cross-checks: `bash tools/mori-census.sh --selftest` was not re-run by this
seat this round (census frozen, untouched); the honest oracle runs above are the honest
side, and the receipts-writer's r6 set (`corpus/evidence/backchannel-r6-20261015T190229Z-*`)
pins the same revisions.

## R1 mechanics — why the header leaked, and what closed it

At `7143ccc2…` the header printed **before the case loop** (`:954-956` then loop
`:958-960`). The census's parent is the oracle's command-substitution subshell
(measured process chain: oracle → subshell, fd/1 = command-substitution pipe → census);
the oracle is the **grandparent**. When the run's stdout is a regular file — every
`> log` / CI receipt pattern — invocation 1 reads the full `SHUFFLE_SEED`/
`RUN_NONCE`/`CASE_ORDER` from `/proc/<oracle>/fd/1` and maps position → id → the public
want table (with `shape-invariance` expanded to its two invocation slots). Probe:
`before-probe-header.out` INV=1 shows the header verbatim at ancestor level 2.

Probe-design trap, worth keeping: reading `/proc/$PPID/fd/1` **blind is a deadlock
risk** — the census's own parent holds the command-substitution pipe whose write end is
the census's own stdout, so `cat` blocks forever (`pipe_wait_readable`, reproduced and
killed as scratch). Walk the ancestor chain and only read a `test -f`-regular fd/1.

At r6 the header prints only after every case has run (`:1066-1072`: loop `:1066-1068`,
`SHUFFLE_SEED=`/`RUN_NONCE=`/`CASE_ORDER=` `:1070-1072`), so no living invocation can
read it; the mid-run capture file holds only PASS/FAIL lines and the FAIL texts are
redacted (no `want=[nonce-…]`). The pin channel is closed by a **one-time self re-exec**
when a pin is present (`:206-224`): the values travel through pipe fd 3 (`exec 3< <(…)`
`:211`), the pins are unset, `exec bash "$SELF" "$CENSUS"` `:214` replaces the image,
and the pipeline is drained at startup (`:219`). This replaced an earlier `unset`-based
scrub — and the impl's own comment records why the earlier reading was wrong: a runtime
`unset` does not rewrite the exec-time environ region; an apparent scrub was an artifact
of bash exec-optimizing a final `sleep` and replacing the process image
(`tools/mori-silence-cases.sh:196-205`). Measured: the pinned-run environ probe shows
`seed=[]` from invocation 1.

## R2 mechanics — what the fixture salt buys, and the attacker it does not stop

At `7143ccc2…` fixture content was nonce-free (0 token-bearing files) and run-invariant
(F stable across runs) — one observed run built a (content → output row) table that
replayed at 28/28.

At r6 every fixture carries per-run bytes (`:239-240` salt; salted salt/blob artifacts
under `CASE_DIR` `:309-314`; the nonce token + salt hex woven into committed file bodies
and commit messages `:417`,`:419`, and into the dirty/untracked/report fixtures), so:

* the naive memorizer (excludes only `.git/index` and the `run-nonce` artifact by name)
  misses **29/29** — its old tables and its fresh-learned tables both go stale;
* a variant that normalizes the **announced** nonce token still misses 29/29 — the salt
  is never printed, never exported, never pinnable (`:236-240` comments);
* **but the class survives** once the attacker treats the annotations as noise:
  `attacker-r2-ultra.sh` (`6b79f776…`) fingerprints only non-`.git` files, excludes
  `salt-*`/`blob-*`/`run-nonce` by name, normalizes `nonce-<N>` and 16-hex salt patterns
  out of each file's bytes, **omits raw sizes** (see §3 of the lesson), and adds a
  mechanical readability marker (`find` stderr line count, which disambiguates
  `unreadable-git-unavailable` from content-identical `silent-open`). Result:
  29/29 content hits and `matched=28 total=28` exit 0 — memorized rows, no fleet
  semantics, no grading logic.

Two measured attacker-design pitfalls that bound *both* directions of such claims:

* **Key collisions understate the attacker.** A worktree-only fingerprint collides for
  cases whose distinguishing bytes live in `.git` (e.g. `silent-open` vs
  `unreadable-git-unavailable`): my first ultra run hit 29/29 keys but scored 27/28
  (one case answered with the wrong memorized row).
* **Size keys overstate the defense, intermittently.** With sizes kept, the same
  attacker hit only 1/29 keys in one learn→attack pair and 29/29 in another — the
  difference was the nonces' digit counts (annotation length is data-dependent). A
  closure claim that holds on one seed pair and fails on another is a coin flip, not a
  closure.

## Why the surviving attacker is the right thing to name

r5's lesson already stated it: **entropy that does not change the correct answer does
not stop memorization.** The r6 salt changes the *bytes* of every fixture but not the
*answer* for any case identity — so the only cost it imposes is "find and cancel the
variation pattern", which is a normalization step, not a measurement. The closure that
would bind is r5's countermeasure #1, still not applied: make **semantically relevant**
content vary per run (ledger epochs/rounds, which want-set branch is correct, mission
structure) so a memorized row is *wrong*, not merely *stale*, and any forgery must then
actually measure the fixture. Until that lands, "content freshness closes content-keyed
memorization" is true only for the enumerated naive class.

## Applying it (any lane)

- **Run secrets: enumerate surfaces, not exports.** Ask what a same-user descendant can
  read *while it runs*: `/proc/<pid>/fd/*`, `/proc/<pid>/environ`, `/proc/<pid>/cmdline`
  for every ancestor — and when the value is a durability feature (pins), move it out of
  the process surface (fd handoff + re-exec, not `unset`), or print it only after the
  graded processes are reaped. Redact failure texts: r5 leaked the nonce value inside
  `want=[…]`; r6 removed it.
- **Freshness: name the channel and the normalizer it beats.** "Content varies per run"
  is a claim about an attacker capability. Announce-token only defeats naive replay;
  pattern-shaped variation defeats nothing that a regex cannot strip; length-only
  variation is even weaker (data-dependent). Only variation in the *semantics the grade
  depends on* forces actual measurement.
- **When you evaluate an attacker class, fix its key first.** Collisions and size
  nondeterminism changed my scores from 27/28 to 1/29 to 28/28 on the *same* defense —
  always state the key definition, the digit/size handling, and re-run across seeds.
- **Re-run the whole forgery repertoire after every hardening** (no-read replay,
  env-token echo, content-hash lookup, process-walk, ancestor-fd, pinned-environ,
  pattern-normalizing memorizer). The list of survivors is the security statement.

## Limits

- Single host, GNU bash 5.3.15, same-user attacker, no ptrace needed (fd/environ are
  owner-readable). The fd attacks assume a **regular-file** stdout capture (the receipt
  pattern); pipe-mode runs were not re-measured this round (r5 measured pipe mode
  closed), and a tty ancestor-walk blocks (a hanging attacker is a tell).
- The ultra memorizer reads fixture content and needs one observed honest run to build
  its table (the r5 lesson's cost caveat); it is bound to the three SHAs above.
  "Zero grading logic" here means: no fleet semantics, no ledger/repo parsing — only
  normalized byte fingerprints and a memorized row.
- The `b2ebe5e7…` → `3307761a…` diff was verified comment-only (13 diff lines, none
  code); if the lane file changes again with any code line, re-measure.
- No liveness, admission, or remediation claim; this is a report of measured attacks.

## Repro (scratch, /tmp/mori-lessons-r6/)

- Before: `bash oracle-r5-7143ccc2.sh <attack>` (`attacker-r1-fdheader.sh`
  `0ee8525b…`, `attacker-r1-seedreader.sh` `4f2bcf03…`; R2: learn with `learner-r2.sh`
  `ff06cad9…`, replay `attacker-r2-memorizer.sh` `57798c89…`).
- After: same attackers vs `oracle-r6-final.sh` (`3307761a…`); ultra pair
  `learner-r2-ultra.sh` `8f4e2e99…` + `attacker-r2-ultra.sh` `6b79f776…`;
  normalizing pair `learner-r2-norm.sh` `475600b3…` + `attacker-r2-norm.sh`
  `44051479…`; probes `probe-header.sh` `2a723606…`, `probe-content.sh` `2f5ca49a…`.
- One-shot battery: `bash final-battery.sh` → `final-battery.log` (stability wait →
  snapshot → full battery → ultra → naive). The fingerprint sources, F-multiset
  comparison, and tuple hashes are in `after-tuples*.txt`, `final-battery.log`.