# The verdict machine, round 6 — the stdout backchannel and content-keyed forgery closed, and the two residuals that remain

seat: **note-writer** (round-6 flash wave) · lane mori-shokunin · written
2026-10-15T19:12Z · detection and report only; nothing here remediates a fleet
process. This seat writes **this file only** (SCORECARD.md / LOG.md are
parent-owned; `corpus/evidence/` belongs to the receipts-writer).

Describes the two tools at their pinned revisions:

| tool | sha256 | revision |
|---|---|---|
| `tools/mori-silence-cases.sh` | `3307761a04a1eab8f33859a69d2eb63fb6312afb8f8041f7b09da4544be174b9` | r6 oracle, 1079 lines (working tree; uncommitted at this seat's clock) |
| `tools/mori-silence-cases.sh` (measured) | `b2ebe5e7fce787713fa27aca088817d90c40f98b889d4da4b6ccd1bc4e092314` | snapshot all figures below were taken at; diff to the final `3307761a…` is **comment-only (0 code lines)** — re-checked by this seat |
| `tools/mori-census.sh` | `af2d4e79e69b70bb0b5aecd6acc9608fc7c16b0716766d4a60310e0689d350d7` | `VERSION=census-r3` — **frozen this round**; re-verified byte-identical before and after every run |

Lane HEAD `848b3a6` (round-5 records); the r6 oracle is an uncommitted working-tree
revision. The "before" bytes are the round-5 oracle `7143ccc2a14221713334c33ade56e24ca711fbd0d3d17f31d33e151be544f017`
(the round-5 admission), snapshotted and re-verified by this seat. This seat's
measurements are double-sourced where they overlap with the receipts-writer's set
(`corpus/evidence/backchannel-r6-20261015T{190229,190453}Z-*.log`), the
lessons-distiller note (`corpus/lessons/2026-10-15-run-secret-timing-and-content-freshness-limits.md`)
and the critic seat's r6 evidence (`/tmp/mori-critic-r6/evidence-r6-330/`) — stated
explicitly where they disagree.

All scratch for this note is under `/tmp/mori-nwr-r6/` (never in the lane tree;
attackers and generator sources are sha-pinned in §7). An interrupted earlier
dispatch of this wave left preparation in `/tmp/mori-vnw-r6/`; its artifacts were
re-verified by this seat before reuse and the directory was abandoned when a stale
prior-dispatch poller pair kept writing it (no figure below depends on that dir).

## 1. The two residuals at r5 — mechanisms, re-measured by this seat at `7143ccc2…`

**R1 — stdout backchannel.** The r5 oracle printed its run header
(`SHUFFLE_SEED=`/`RUN_NONCE=`/`CASE_ORDER=`) to stdout **before the case loop**
(`7143ccc2…:954-956`, loop `:958-960`). The census's parent is the oracle's
command-substitution subshell; the oracle itself is the grandparent and holds the
capture file on fd/1. A census that walks its ancestry and reads
`/proc/<oracle>/fd/1` — or `/proc/<oracle>/environ` on pinned runs — could therefore
learn the run's order (and seed) **while it was still running**, map its own
invocation position to the case id, and replay the public want table: 28/28 with zero
grading logic. Re-verified before-side at the r5 bytes (exit codes are the oracle's):

| attacker (sha prefix) | r5 result |
|---|---|
| honest census | `matched=28 total=28` exit 0 |
| `attacker-leak.sh` `3f05915c…` (reads `CASE_ORDER` via `/proc/<gp>/fd/1`) | `matched=28 total=28` exit 0 |
| `sniffer-r1-ancestorfd.sh` `329ed307…` (reads the seed the same way, rebuilds the Fisher–Yates order) | `matched=28 total=28` exit 0 |
| `sniffer-r1-environ.sh` `48a6599…` (`/proc/<ppid>/environ`, pinned run) | `matched=28 total=28` exit 0 |
| `sniffer-r2-content.sh` `3e0fa4c7…` (content-keyed memorizer, R2) | `matched=28 total=28` exit 0 |

**R2 — content-keyed forgery.** Every fixture was byte-stable across runs apart
from the nonce artifacts (`run-nonce`, `nonce-<N>`) that a memorizer could exclude by
name, and the nonce was not bound to any graded content. One observed run therefore
sufficed to build a (fixture bytes → output row) table that replayed at every fresh
seed (`3e0fa4c7…`, above; corroborated by the r5 lesson's `3e0fa4c7…` figure).

## 2. The r6 design and its closures

### 2.1 R1 closed: the header prints only after the case loop, and the pins never live in a SUT-readable surface

- **Header-after-loop.** The runner executes all 28 cases first
  (`3307761a…:1066-1068`); only then does the oracle print `SHUFFLE_SEED=`,
  `RUN_NONCE=`, `CASE_ORDER=` (`:1070-1072`) and the tally (`:1075`). Mid-run stdout
  therefore carries only `PASS`/`FAIL` lines and the per-case census text.
- **No run secret in per-case lines.** The nonce token is stripped from any census
  fragment echoed into a report line by `redact()` (`:545`, applied at the two
  fragment sites); the missing-token failure text names no token value
  (`:599`). Measured: in a failing attacker run, `0` lines before
  `CASE_ORDER=` contain `nonce-<digits>` (F-r1-fd.out, F-r1-env.out, F-r2-stale.out).
- **Pins leave the exec-time environment by a one-time self re-exec** when
  `MORI_SHUFFLE_SEED`/`MORI_RUN_NONCE` are present (`:207-216`): the values travel
  through a pipe fd (`:211`, read at `:219`, closed at `:220`), the oracle re-execs
  itself with both variables unset (`:214`), and the new image — and every subshell
  it later forks — carries a scrubbed environment. The code comment records why a
  runtime `unset` was not enough (an earlier reading was an artifact of bash
  exec-optimizing its last command into `sleep`).
- Measured mid-run visibility from the census's own position: **0 of 29**
  invocations found `MORI_SHUFFLE_SEED` in any ancestor's environ on a pinned run;
  **0 of 29** fd/1 reads of a captured regular file contained the header
  (`probe-r6-channels.sh` `274e100b…`, dumps `/tmp/mori-nwr-r6/probe-dump-pin2/`).

### 2.2 R2 closed (for the naive memorizer): fixture content is per-run

- A third independent entropy draw, `RUN_SALT_HEX` (`:239-240`), is woven in two
  grammars: every **committed file body** gets `[nonce-<N> <salt-hex16>]` appended
  and every **commit message** gets `[<salt-hex16>]` (`gc()`, `:417` and `:419`;
  exceptions are the two file kinds the census parses — `.gitignore` and
  `*.round`); plus `case_skeleton` writes a `salt-<hex>` file and 0–2 random
  `blob-<i>-<hex>` files under `CASE_DIR` (`:309`, `:314-315`), so the file
  *count* varies too.
- Four cases bind the marker into **untracked/dirty worktree content** the census
  itself reads: `dirty-same-path-as-sibling-progress` (`:823`),
  `untracked-recent-progress` (`:836`), `untracked-report-progress` (`:899`),
  `main-repo-noise-silent` (`:921`), each in the unbracketed form
  `<word> nonce-<N> <salt-hex16>`.
- Consequence: the fingerprint a memorizer learned yesterday has no key today.
  Measured: the r5-learned table replays `matched=0 total=28` exit 1; a fresh
  learn-at-r6 then replay at a new seed (raw relpath+size+content fingerprint)
  also `0/28` exit 1.

### 2.3 What is unchanged

The 28 case ids and their want tuples are byte-identical to r5 (`CASE_IDS` block
sha `c27d5111…`; 26 `assert_case` want lines sha `bce578e2…`; only the two
`count_check` failure *messages* changed, for redaction). The census is untouched
(`af2d4e79…`), `--selftest` `PASS (30 cases, 30 passed, 0 failed)` exit 0.

## 3. Measured after-side at the pinned revision

Honest side (F-honest / G-honest runs; receipts `backchannel-r6-20261015T190229Z-oracle-*.log`):

| probe | result |
|---|---|
| `bash oracle-r6 <census>` ×3 fresh seeds | `matched=28 total=28` exit 0 every run |
| `CASE_ORDER` across those runs | distinct every run (`471cee13…`, `bd987656…`, `275e7841…`); same 28-id multiset |
| sorted per-case PASS tuples | byte-identical sha `a70af583bb01b8362a49f07aa8f2b66814fac22b119a22f9b273c5024573c752` in every r6 run (the r5 tuple hash too) |
| header vs case lines | `CASE_ORDER=` at line 31 of a 32-line run; all PASS/FAIL lines precede it |

Attack side (all zero-grading-logic probes; attacker sources pinned in §7):

| attacker | at r5 | at r6 | where |
|---|---|---|---|
| `attacker-leak.sh` (fd/1 `CASE_ORDER`) | `28/28` exit 0 | **`0/28` exit 1** | `G-r1-leak.out` `d1a8405d…` |
| `sniffer-r1-ancestorfd.sh` (fd/1 seed) | `28/28` exit 0 | `1/28` exit 1 (the shape dirs' blind fallback) | `F-r1-fd.out` |
| `sniffer-r1-environ.sh` (env-prefix pin) | `28/28` exit 0 | `1/28` exit 1 | `G-r1-env.out`, `F-r1-env.out` |
| `sniffer-r2-content.sh` (r5-learned content table) | `28/28` exit 0 | **`0/28` exit 1** | `G-r2-stale.out` `f4885b27…` |
| fresh raw content memorizer (learn r6 → replay r6) | `28/28` (r5 control) | **`0/28` exit 1** | `F-r2-raw.out` `c3742ed5…`; `raw` mode of §6 map |
| bracket-grammar normalizer (strips the `gc` weave only) | 28/28 (r5 control) | **`24/28` exit 1** — the four §4 cases fail | `F2-r2-norm.out` `7146b84d…` |
| full grammar normalizer (strips both marker grammars) | 28/28 (r5 control) | **`28/28` exit 0** — residual, §4 | `F3-r2-norm.out` `5264c4ac…`, `G-r2-norm.out` `43dd15c9…` |

The receipt set agrees on every overlapping figure: `r1-redirect-r6` `0/28`,
`r1-pipe-r6` `0/28`, `r1-pinned-environ-r6` `0/28`, `r2-oldtable-r6` `0/28`,
`r2-fresh-replay-r6` `0/28`, `r2-normalize-replay-r6` `0/28` (their normalizer
strips the nonce only; the unannounced salt survives it), and the before legs
`28/28` at the r5 bytes (`corpus/evidence/backchannel-r6-20261015T190453Z-attack-{r1,r2}.log`).

## 4. The discriminating cases and the residual normalizing attacker

Against a normalizer that knows only the *bracketed* `gc` grammar — a natural first
implementation, because that is the weave visible in committed bodies — exactly
**four cases discriminate**, and they are the four untracked/dirty-marker cases:

| case | marker file | oracle line |
|---|---|---|
| `dirty-same-path-as-sibling-progress` | `root/kagi-shokunin/LOG.md` (dirty, untracked edit) | `3307761a…:823` |
| `untracked-recent-progress` | `root/kagi-shokunin/scratch/notes.md` | `:836` |
| `untracked-report-progress` | `root/.ufo/reports/round-2/aggregator.md` | `:899` |
| `main-repo-noise-silent` | `root/work/inprogress.md` | `:921` |

Their content is written **outside `gc()`** in the unbracketed form
(`wip nonce-<N> <salt-hex>`, `draft …`, `ignored wip …`, `subject dirty work …`), so
the bracket-stripping normalizer's key still changes per run and the memorizer
misses those four (`24/28`, exit 1). Every other case's per-run bytes live in the
`gc` weave, which that normalizer removes.

Extending the normalizer to strip the unbracketed marker as well (one more regex,
still zero grading logic, still only reading fixture bytes) recovers invariance:
**`matched=28 total=28` exit 0** — measured twice (`F3-r2-norm.out`,
`G-r2-norm.out`) and independently by the lessons-distiller (its
`6b79f776…` pattern-normalizing memorizer, same 28/28) and the critic
(`EV-norm2.log` `28/28` at `3307761a…`). This is the **residual normalizing-attacker
class**: the salt re-prices memorization (a naive or partial normalizer dies) but
does not close it, because the per-run bytes are a *fixed grammar of annotations*
and the graded answers are unchanged by the salt.

## 5. The critic's next-channel findings and the named best residual

The critic seat's r6 battery (its files at `/tmp/mori-critic-r6/evidence-r6-330/`,
taken at `3307761a…`) and this seat's independent probes agree on the channel map:

1. **stdout fd channel — closed.** The critic's fd-reading attacker (their
   `r1-attacker.sh`) marks all 28 graded invocations `R1-MISS (no CASE_ORDER
   reachable)`; its blind fallback scores `matched=8 total=28` exit 1
   (`EV-r1.log`/`EV-r1.marks`). This seat: `0/28` (`G-r1-leak.out`) with the same
   reading. The header is simply not on stdout while any census lives.
2. **`/proc/<pid>/mem` — not a channel on this host.** Read attempts against every
   ancestor (including the oracle) fail `Permission denied` (yama `ptrace_scope=1`,
   GNU bash 5.3.15, Linux 7.2.3-arch1-3); `/proc/<pid>/maps` names are readable but
   the bytes are not (probe dump `probe-dump/run.inv.1`).
3. **The residual that survives — a pin that lives in a *surviving ancestor's*
   exec-time environ.** `/proc/<pid>/environ` shows the environment *at execve
   time*. A runtime `export` in a shell does not appear there, and the oracle's
   re-exec scrubs its own image — but a process that was **exec'd with the pin in
   its environment and stays alive for the run** exposes it for the whole run, and
   the oracle cannot scrub a process it does not own. The critic's
   `EV-r1p-export.log` shows `matched=28 total=28` for this pattern; this seat
   reproduced the mechanism directly:

   ```
   $ env MORI_SHUFFLE_SEED=31337 bash -c 'bash oracle-r6 <ancestry-reader>; true'
   ANCESTRY-READ lvl=3 seed=31337 k=1        # attacker reads the seed from its ancestry
   MORI_SILENCE_CASES: matched=28 total=28    # exit 0
   $ env MORI_SHUFFLE_SEED=31337 bash oracle-r6 <same attacker>       # control: no survivor
   ANCESTRY-READ lvl=9 seed=none k=1
   MORI_SILENCE_CASES: matched=1 total=28     # exit 1
   ```

   (`G-r1-liveanc.out` `f4b018a8…` vs `G-r1-prefix2.out` `311bcc41…`.) The
   precondition is precise: the pin must be in the exec-time environment of an
   intermediate shell that outlives the exec (e.g. an `env VAR=…`-prefixed
   compound command, a CI/wrapper step that runs `bash -c '…; …'`, or any ancestor
   exec'd with the pin exported). A plain `env VAR=… bash oracle.sh` prefix is
   closed, because the `env` process execs into the oracle with no survivor.
4. **The other residual** is §4's full-grammar normalizing memorizer (28/28 exit 0,
   fixture reads required; named independently by the lesson, the critic and this
   seat).

**Named best residual (this seat's call, evidence above):** the surviving-ancestor
environ channel. It needs no fixture reads, no grading logic, and under the
wrapper-CI invocation pattern reaches `matched=28 total=28` exit 0 while a pinned
run is in flight. It is a scope boundary rather than a defect of the r6 change —
the round's claim covers secrets reachable from **the oracle's** stdout/environ, and
the oracle scrubs exactly that; a pin in the caller's surviving shell is outside the
oracle's reach (the fix direction — a seed that never transits any environment, or
pinning via a private fd/file the operator owns — is the parent's call, not
remediated here). The content-binding residual of §4 is the best *R2-class*
residual.

## 6. Scratch inventory (re-run material, `/tmp` only)

| file | sha256 (prefix) | role |
|---|---|---|
| `oracle-r5-7143ccc2.sh` | `7143ccc2a1422171` | pinned r5 snapshot (before side) |
| `oracle-r6-stable2.sh` | `b2ebe5e7fce78771` | pinned r6 snapshot (all after figures; comment-only diff to final) |
| `oracle-r6-mid3.sh` | `3307761a04a1eab8` | snapshot of the final lane bytes (confirmatory battery G) |
| `census-frozen-af2d4e79.sh` | `af2d4e79e69b70bb` | frozen census snapshot |
| `attacker-leak.sh` | `3f05915cc24152ec` | fd/1 `CASE_ORDER` reader |
| `sniffer-r1-ancestorfd.sh` | `329ed307b429ee42` | fd/1 seed reader |
| `sniffer-r1-environ.sh` | `48a659970e8c6342` | single-level environ reader |
| `sniffer-r1-ancestry.sh` | `fa617ce636a81f9c` | full-ancestry environ walker (this seat; §5.3) |
| `sniffer-r2-content.sh` | `3e0fa4c79ed75341` | r5-learned content memorizer |
| `after/F-atk-raw.sh` | `5ee075c8437658cc` | fresh raw content memorizer (learned at r6) |
| `after/F2-atk-norm.sh` | `40933fa8b4d60805` | bracket-grammar normalizer (24/28) |
| `after/F3-atk-norm.sh` | `49f33928642ac043` | full-grammar normalizer (28/28) |
| `probe-r6-channels.sh` | `274e100b4f4b6a86` | ancestry/fd/environ/mem channel dump |
| `learn2.sh`, `gen2.py` | in-dir | learner/attacker generator (identical fingerprint code paths) |
| `map2-r6c.txt` | `e25a96d8ddfea58c` | learn-run map (raw + normalized F per invocation) |

Re-run recipe (cwd = lane root; applies only at the SHAs at the top of this note):

```sh
sha256sum tools/mori-silence-cases.sh   # must equal 3307761a… (or b2ebe5e7… behaviourally)
sha256sum tools/mori-census.sh          # must equal af2d4e79…
bash tools/mori-silence-cases.sh        # expect exit 0, matched=28 total=28
bash /tmp/mori-nwr-r6/oracle-r6-mid3.sh /tmp/mori-nwr-r6/sniffer-r2-content.sh   # expect 0/28 exit 1
bash tools/mori-census.sh --selftest    # expect PASS (30 cases, 30 passed, 0 failed)
```

If either tool byte changes, re-measure everything here.

## 7. Final pinned tallies

| probe | before (`7143ccc2` / `af2d4e79`) | after (`b2ebe5e7`/`3307761a` / `af2d4e79`) | receipt / measurement |
|---|---|---|---|
| honest census | `28/28` exit 0 | `28/28` exit 0 ×3 + receipts ×3 | `backchannel-r6-20261015T190229Z-oracle-{1,2,3}.log`; F/G-honest |
| per-case tuples across shuffles | (one order) | sha `a70af583…` every run | F/G-honest + receipts |
| fd/1 `CASE_ORDER` attacker | `28/28` exit 0 | `0/28` exit 1 | `G-r1-leak.out`; receipt `r1-redirect-r6` `0/28` |
| fd/1 seed reader | `28/28` exit 0 | `1/28` exit 1 | `F-r1-fd.out` |
| env-prefix pinned environ reader | `28/28` exit 0 | `1/28` exit 1; `0/29` invocations see the seed | `G-r1-env.out`; probe-dump-pin2 |
| surviving-ancestor pin (wrapper pattern) | n/a | **`28/28` exit 0** (residual §5) | `G-r1-liveanc.out`; critic `EV-r1p-export.log` |
| r5-learned content table | `28/28` exit 0 | `0/28` exit 1 | `G-r2-stale.out`; receipt `r2-oldtable-r6` `0/28` |
| fresh raw memorizer (r6→r6) | `28/28` exit 0 (r5 control) | `0/28` exit 1 | `F-r2-raw.out`; receipt `r2-fresh-replay-r6` `0/28` |
| bracket-grammar normalizer | `28/28` exit 0 (r5 control) | `24/28` exit 1 — the four §4 cases | `F2-r2-norm.out` |
| full-grammar normalizer | `28/28` exit 0 (r5 control) | **`28/28` exit 0** (residual §4) | `F3-r2-norm.out`, `G-r2-norm.out`; lesson `6b79f776…`; critic `EV-norm2.log` |
| registry ids + assert wants | — | byte-identical to r5 (`c27d5111…` / `bce578e2…`); 2 redaction messages differ | `registry-r5-verify.txt` vs `registry-r6-final.txt` |
| census selftest | PASS 30/30 exit 0 | PASS 30/30 exit 0 (frozen) | `backchannel-r6-20261015T190229Z-selftest.log` |

## 8. Limits

- Everything here is measured against pinned SHAs on one host (GNU bash 5.3.15,
  Linux 7.2.3-arch1-3, yama `ptrace_scope=1`); the r6 oracle was a working-tree
  revision at measurement time, and the final revision differs from the measured
  one only in comments (re-checked).
- §5.3 is a channel measurement with witnesses under a specific invocation
  pattern, not a claim that any receipt run used it; the plain `env`-prefix form is
  closed (measured).
- §4's normalizer is *a* grammar model built by this seat from the public oracle
  source; a different attacker could model the grammar differently, and the
  four-case list is the measured discriminating set for the model as stated.
- Live figures are a pinned clock, not a baseline; no causal claim about fleet
  liveness; no admission or axis verdict (parent), no scalar score, no remediation.