# ConnKumitate — kumitate r48 run-agreement vs mori r37 C1 challenge arm

**Item attacked:** the claimed novelty/independence of this round's C1 challenge arm against the
fleet repertoire: kumitate round 48 admitted `counter-rerun` (run-agreement). Does mori's C1
duplicate or contradict it?

**Relationship: none — neither duplicate nor contradiction.** The two techniques police disjoint
failure classes on disjoint objects; each survives the other's kill class. Two named boundaries
stop a verbatim transplant (below). One bounded synthesis is proposed.

**Installs:** none (pacman paused host-wide; nothing needed installing).

## A. What kumitate r48's run-agreement is

- Claim: "C2 — capability acquisition `counter-rerun`: new `scripts/counter-rerun.mjs`
  mechanizing R47-1's routed repeat-run rule (predicate COUNTER_RERUN)" —
  `/home/vgpnk/Projects/shokunin/.ufo/reports/round-48/kumitate.md:8`; scored
  "`COUNTER_RERUN: AGREE (runs=2)` … both runs `held=4/4`, summary sha256 `f3c23bdc…`" at
  `kumitate.md:21`; the r47 origin (verdict moved 3/5→4/5 at one rev under load) at
  `kumitate-shokunin/scripts/counter-rerun.mjs:5-13`.
- Mechanism: run ONE counter K times over the same (lane, rev, args); AGREE iff every run exits 0
  AND every run's **final summary line** (last non-empty stdout line) is byte-identical —
  `counter-rerun.mjs:215-229` (decide), `:32-34` (final-line definition), `:224-226` (byte
  compare), `:221-223` (exit-0 requirement). Explicitly scoped: "FINAL-SUMMARY-LINE AGREEMENT
  ONLY … never 'this counter's whole output reproduced' and never 'this counter's site-level
  reading is correct'" — `counter-rerun.mjs:36-44`. Probe invocation convention is
  `node <probe> <lane> <rev> <probe args>` — `counter-rerun.mjs:21-24`.
- Object policed: the **counter's verdict stability** (flake), not correctness of what it measures.

## B. What mori r37 C1's challenge arm is

- Predicate P-C1 — `mori-shokunin/.ufo/waves/round-37/contract.md:18-26` and
  `count-c1.py:42-51`: one counter invocation judges the **tool under test** on 24 run-time-drawn
  sandbox histories + the lane's real history + one challenge history + 3 negative fixtures.
- Challenge arm — `count-c1.py:754-791`: ONE run-time-drawn synthetic history in "real-arm
  clothing" (repo under the lane's own `.ufo/waves/round-37/scratch`, `count-c1.py:56,762-763`;
  lane git identity and lane SOURCES title, `count-c1.py:288-289,768`), truth from the counter's
  own op log, "never a published constant" — `count-c1.py:760-761`. Target defect class: a tool
  that classifies sandbox-vs-real by path/identity/title and prints the receipt's constant
  (w2/RevNgC2 N1) — `count-c1.py:18-22`.
- Object policed: the **tool's honesty** within a single run, not the counter's across-run
  stability. Scored runs randomize the draw: seed from `os.urandom`, `--seed` only pins replay —
  `count-c1.py:10,847,851`; exit 0 iff `C1=met` — `count-c1.py:949-952`; the last stdout line is
  `seed=<N>` — `count-c1.py:950-951` (also visible in `evidence/c1-after.txt:14-15`).

## C. Why not a duplicate

1. Different object: counter-rerun judges the counter's own output across identical reruns
   (`counter-rerun.mjs:10-13`); mori's challenge arm judges the tool under test against hidden
   truth inside one run (`count-c1.py:754-791`). Kumitate's instrument "knows nothing about what
   the counter measures" (`counter-rerun.mjs:11-13`); mori's arm is domain truth (SOURCES.md
   registry semantics).
2. Each survives the other's kill class: a deterministic memoizer (fixture `memo-n1.py`) prints
   the same wrong constant every run — counter-rerun reads AGREE (it explicitly does not claim
   reading correctness, `counter-rerun.mjs:36-44`) while mori's challenge arm kills it (observed:
   `c1-after.txt:11`, "rejected (challenge: lists differ)"). Conversely a flaky counter passes
   mori's single-run challenge arm while counter-rerun's flake-injection case exists precisely to
   kill it (`counter-rerun.mjs:65-66`; selftest case 6 below).
3. No shared machinery: kumitate = K-run byte comparison of one line; mori = randomized-draw
   truth comparison of summary + per-id lines per arm (`count-c1.py:676-717,779-788`).

## D. Why not a contradiction

Neither practice forbids or negates the other; both can hold on the same counter. Two fit
boundaries for a verbatim transplant (scope limits, not conflicts):

1. **Byte-level AGREE misreads mori's scored form.** counter-rerun compares the last non-empty
   stdout line (`counter-rerun.mjs:32-34,224`); for `count-c1.py` that line is `seed=<N>`
   (`count-c1.py:951`), which is run-varying by design in scored runs (`count-c1.py:851`). A
   verbatim wrap of the unseeded scored command would print DISAGREE for every honest pair
   (observed: unseeded run's last line `seed=1274921218405755840` vs pinned runs' `seed=424242`);
   with `--seed` pinned the compared line is a tautology and the verdict reaches the decision
   only via the exit-0 requirement (`counter-rerun.mjs:221-223`; `C1=met` ⟺ exit 0,
   `count-c1.py:949-952`).
2. **Calling convention does not transplant.** counter-rerun invokes its probe as
   `node <probe> <lane> <rev> …` (`counter-rerun.mjs:21-24`; selftest case 13); mori's counter is
   `python3 count-c1.py <rev> [--repo DIR]` (`count-c1.py:4-5`). Wrapping needs a shim.

Cross-reference status in mori's record: `grep 'counter-rerun|COUNTER_RERUN|run-agreement|run
agreement'` over the mori repo hits only the wave-spec assignment text
(`.ufo/waves/round-37/gen-wave-spec.py:563-568`, `w1-plan.json:785`, `w1-spec.json:310`,
`w1-taskcall.json:307`, `w1-tasks.json:305`) — nothing in `contract.md`, SCORECARD, or corpus.
The relationship was undocumented until this report.

## Measurements (command → observed)

1. Pinned-seed determinism of mori's counter (twice) and one unseeded scored-form run, rev
   `e57c58b57c025364e79d130fbdf764d2674d83d6`:
   ```
   python3 .ufo/waves/round-37/count-c1.py e57c58b5… --seed 424242   # ×2
   python3 .ufo/waves/round-37/count-c1.py e57c58b5…                 # unseeded
   ```
   Observed (receipts `/fast/scratch/hyaku/mori-r37/ConnKumitate/c1-run{1,2,3}-*.txt`): run1 and
   run2 both `blind arm: 24/24 … (coverage: deletions=24 changed-back=16 superseded=9)`, `real
   arm: pass`, `challenge arm (real-arm clothing): pass`, all three negatives `rejected`,
   `C1=met`, exit 0; the two outputs differ only in the temp tool path
   (`/tmp/mori-c1-tool-wxyjqh4w` vs `/tmp/mori-c1-tool-e4qn3ods`) and one timing digit
   (1.9s vs 2.0s); both end `seed=424242`. Unseeded run3: `C1=met`, exit 0, last line
   `seed=1274921218405755840` — the final line is the run-varying seed, not the verdict.
2. Kumitate's instrument, re-run read-only:
   ```
   node scripts/counter-rerun.mjs --selftest   (cwd kumitate-shokunin)
   ```
   Observed: exit 0, 14 `PASS` case lines, final line `COUNTER_RERUN_SELFTEST: PASS` — matches
   the "14 cases" claim at `kumitate.md:21`. Cases include "flake injection … DISAGREEs" and
   "a counter that exits non-zero DISAGREEs even when its summary lines are identical"
   (receipt `/fast/scratch/hyaku/mori-r37/ConnKumitate/counter-rerun-selftest.txt`).

## Affected axes

- **calibration (C1):** informational, no defect found — the challenge arm and run-agreement are
  complementary; C1's single-shot scored run is the open gap (below), not an error.
- **freshness (C2):** untouched (no drift-probe surface involved).
- **repertoire/frontier:** kumitate r48 already registered `counter-rerun` as a fleet capability
  (`kumitate.md:31`); mori's record citing it would be an adoption note, not a new capability.

## Proposed move (one, bounded)

Adopt kumitate r48's repeat-run **rule** at verdict level, not its byte-level form: bind a
two-run agreement pair for C1 in the round record — `evidence/c1-after.txt` (seed
`13985344346805549517`) plus the in-flight `ExecC1Seed43` receipt (independent seed, observed
running, output unpublished at report time) — requiring both to read `C1=met` exit 0 with all
three negatives rejected, both seeds recorded. Record why `counter-rerun.mjs`'s byte-level AGREE
does not transplant (final line `seed=`, §D.1) and cite
`/home/vgpnk/Projects/shokunin/.ufo/reports/round-48/kumitate.md:8,21` as the precedent. No edit
to frozen P-C1 (`contract.md:4-6` freezes the predicate; this move adds receipts only).

## Risks

- An independent-seed rerun can legitimately exit 2 (blind coverage below the frozen minimum is
  a counter setup error, `count-c1.py:905-908`) — the pair rule must score that as "no reading,"
  never as disagreement, mirroring kumitate's exit-2-is-never-a-score rule
  (`counter-rerun.mjs:49-52`).
- Cost: one extra full C1 run (~4–6 s + sandbox churn) — bounded.
- Record-only change: risk of misreading it as a predicate change — the move adds receipts and a
  provenance note; P-C1 bytes stay frozen.

## Verification (for main)

- `python3 .ufo/waves/round-37/count-c1.py e57c58b5… --seed 424242` twice → identical verdicts
  (§M.1).
- `node /home/vgpnk/Projects/shokunin/kumitate-shokunin/scripts/counter-rerun.mjs --selftest`
  → `COUNTER_RERUN_SELFTEST: PASS`, exit 0 (§M.2).
- Confirm the ExecC1Seed43 receipt lands with `C1=met` exit 0 and its own seed before binding
  the pair.

VERDICT: PASS
