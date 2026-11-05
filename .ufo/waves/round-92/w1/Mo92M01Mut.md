# Mo92M01Mut — mutation test of the frozen counters and the entering digest tool (round 92, wave w1)

Seat: Mo92M01Mut (mutation-tester). All runs in an isolated scratch clone; the lane was never written.

## Scope and method

- Scratch clone: `/fast/scratch/hyaku/mori-r92/Mo92M01Mut/repo`, created `git clone --shared`, detached at
  `f63d1ab030d4179576e494342f48ef8718e497a5`; `git rev-parse --show-toplevel` verified equal to the clone
  before any change; `git status --porcelain` clean at start.
- Finding: `.ufo/waves/round-92/` (contract, counters, evidence) is **not in f63d1ab0's tree**
  (`git ls-tree f63d1ab0 -- .ufo/waves/round-92` is empty). It is committed at `699f6276`, which is not an
  ancestor of the entering revision. The frozen counter bytes used here are the 699f6276 blobs, verified
  byte-identical to the lane tree copies: `count-c1.py` sha256 `cfa154d6f14ffd5b048508bb351dc265784d2e53e4cffc5a4d771428fed80618`,
  `count-c2.py` sha256 `ebe4077d2d6644f408daa3cdf79c0cf9e64143c9c0f6d934e0ac47f4cdc64ebb`.
  Counters were run as scratch copies against the clone (`python3 -I <scratch copy> f63d1ab0… --repo <clone>`).
- Entering tool: `tools/mori-source-digest.py` sha256 `a692b159646e8979f9fc95d5eee82a9a30cee4d8f67432ee824fff7e9d30cee7`
  (tracked at f63d1ab0), run exactly as the round-91 receipt ran it, cwd = clone root.
- Pinned digests recomputed at f63d1ab0 (`git show <rev>:<path> | sha256sum`, exit 0):
  `.ufo/waves/round-90/w1/Mo90S01Sources/sources/python-ast-3.15.2.html` → `7891c58897fe9f78cf16d15fd3464b746a187214c82587ac94b0f83b9a8a42f5`;
  `corpus/evidence/sources-r42/S235.pdf` → `9855a4986a312dfc946b1b97b6010a8e4f1e65a4a30dca99359e6df057ad8020`. Both match the contract.
- Method per mutant: exact single-point string replacement (asserted to occur exactly once), sha256 recorded,
  detector run, `git diff f63d1ab0 -- tools/mori-source-digest.py` captured as the patch file, then pristine
  bytes rewritten and hash-verified. No installs (system python3 + git only); pacman untouched.

## Baselines (pristine bytes; all reproduce the committed entering controls)

| Detector | Verdict line | Exit |
|---|---|---|
| tool | `DIGEST_CHECK rows=121 ok=87 mismatch=2 prefix_only=31 unpinned=1` | 1 |
| count-c1 | `C1=unmet knowledge=98 missing=19 floor=98 rev=f63d1ab030d4` | 1 |
| count-c2 | `C2=unmet mismatch=2 superseded=None superseded_ids=- prefix_only=31 unpinned=1 negatives=0 selftest=absent checks_failed=run_rc,mismatch,superseded_ids,negatives,selftest rev=f63d1ab030d4` | 1 |

The no-harm clause is NOT failing at entering (prefix_only=31, unpinned=1 both hold), so it is correctly absent
from the entering `checks_failed`. A first counter baseline attempt failed rc=2 because the counter paths do not
exist in the f63d1ab0 tree (finding above); it was rerun from scratch copies — the rc=2 attempt is not evidence
of anything except the tree layout.

## 1. Tool mutants (`tools/mori-source-digest.py`)

Kill rule: summary must differ from `DIGEST_CHECK rows=121 ok=87 mismatch=2 prefix_only=31 unpinned=1` or the
exit code must differ.

| Mutant | Single-point edit | Summary line (rc) | Verdict |
|---|---|---|---|
| m1 | `pair_verdict`: `recorded == actual` → `recorded[:16] == actual[:16]` | `rows=121 ok=89 mismatch=0 prefix_only=31 unpinned=1` (1) | **KILLED** |
| m2 | `combine`: insert `if any(v == "ok" for v in verdicts): return "ok"` before the mismatch check | identical (1) | **SURVIVED** |
| m3 | counting site: `counts[row_verdict] += 1` → unpinned counted as ok | `rows=121 ok=88 mismatch=2 prefix_only=31 unpinned=0` (1) | **KILLED** |
| m4 | `combine`: prefix-only branch returns `"ok"` | `rows=121 ok=118 mismatch=2 prefix_only=0 unpinned=1` (1) | **KILLED** |
| m5 | summary print: `counts["mismatch"]` → `counts["mismatch"] - 1` | `rows=121 ok=87 mismatch=1 prefix_only=31 unpinned=1` (1) | **KILLED** |
| m6 | row loop: `if not digests:` → `if not digests or "pinned" in text.lower():` (skip) | `rows=100 ok=74 mismatch=1 prefix_only=24 unpinned=1` (1) | **KILLED** |
| m7 | `extract_digests`: labelled digest `m.group(1).lower()` → `m.group(1)` | identical (1) | **SURVIVED** |
| m8 | `combine`: `if missing_copies: return "unpinned"` → `return "ok"` | `rows=121 ok=88 mismatch=2 prefix_only=31 unpinned=0` (1) | **KILLED** |

Mechanisms observed:
- m1 flips both mismatch rows: S615's recorded digest `7891c588…b8f1a60ad1a6f0` and S235's recorded
  `9855a498…0cda99359e6df057ad8020` each match their pinned actual through the first 16 hex chars and diverge later.
- m6 skips 27 rows whose text contains "pinned" (S062, S170, S181, S213, S565–S571, S580, S581, S583, S585–S587,
  S589–S591, S597, S598, S612–S616); S615 (mismatch) is among them, S235 is not.
- m8 flips exactly one row: `DIGEST S125 unpinned recorded=e60f1bbc… actual=-` → `DIGEST S125 ok …`. Instrumented
  run (ROWSPY over all 121 scored rows) shows S125 is the only row with unresolved copy paths
  (`.ufo/waves/round-25/capture/capture.txt`, `.ufo/waves/round-25/capture/capture-earlyoom.txt`; verdicts list empty).

## 2. Counter mutants (`count-c1.py`; control `C1=unmet knowledge=98 missing=19 floor=98 rev=f63d1ab030d4`, exit 1)

| Mutant | Single-point edit | Verdict line (rc) | Verdict |
|---|---|---|---|
| c1 | `HEAD_LINES = 12` → `6` (check only first 6 lines) | `C1=unmet knowledge=98 missing=46 floor=98 rev=f63d1ab030d4` (1) | **KILLED** |
| c2 | `met = missing == 0 and n >= FLOOR` → `met = missing == 0` (floor conjunct dropped) | identical (1) | **SURVIVED** |
| c3 | absent-keys: append `and k != "recheck"` (recheck-only files count present) | `C1=unmet knowledge=98 missing=13 floor=98 rev=f63d1ab030d4` (1) | **KILLED** |

c3 arithmetic corroborates the committed evidence: exactly 6 of the 19 missing files list `keys=recheck` only
(19−6=13).

## 3. Counter mutants (`count-c2.py`; control verdict above, exit 1)

| Mutant | Single-point edit | Verdict line (rc) | Verdict |
|---|---|---|---|
| c2m1 | main tool run skipped (`main_run = subprocess.CompletedProcess(args=[], returncode=0, stdout="", stderr="")`) | `C2=unmet mismatch=None superseded=None superseded_ids=- prefix_only=None unpinned=None negatives=0 selftest=absent checks_failed=mismatch,superseded_ids,no_harm,negatives,selftest rev=f63d1ab030d4` (1) | **KILLED** |
| c2m2 | `if tuple(ids) != tuple(sorted(SUPERSEDED)) or superseded != 2 or not succ_ok:` → `if False:` | `C2=unmet mismatch=2 superseded=None superseded_ids=- prefix_only=31 unpinned=1 negatives=0 selftest=absent checks_failed=run_rc,mismatch,negatives,selftest rev=f63d1ab030d4` (1) | **KILLED** |
| c2m3 | `if prefix_only != PREFIX_ONLY or unpinned != UNPINNED:` → `if False:` | identical (1) | **SURVIVED** |

## 4. Survivor analysis (equivalence, corpus- and revision-relative)

All four survivors are equivalent **only at the entering revision/corpus**, not in general:

- **m2** (row passes if any one digest matches): at f63d1ab0 no row produces mixed pair verdicts — ROWSPY
  instrumentation over all 121 scored rows shows zero rows with more than one distinct verdict among their pairs,
  so "any-ok ⇒ ok" is unobservable. The two mismatch rows (S235, S615) each record a single digest. Latent gap:
  a future row recording several digests with one ok pair would pass under the mutant.
- **m7** (lowercase dropped): zero uppercase hex digests exist in any of the 391 registry rows' source/anchor
  cells (checked by regex over the full registry), so dropping `.lower()` is a no-op on this corpus.
- **c1-c2** (floor conjunct dropped): with missing=19 the verdict is unmet with or without `n >= FLOOR`; the floor
  clause can only change the verdict when `missing == 0 and knowledge < 98`, unreachable at f63d1ab0. (The
  behavior-bearing point of the floor check is the predicate conjunct; the `floor=98` print is reporting, not
  checking. Under the alternative reading that also deletes the print field, the mutant would be killed; I mutated
  the check, which is the smaller behavior-bearing point.)
- **c2m3** (no-harm clauses dropped): equivalent at entering **by construction** — the clause compares
  prefix_only/unpinned against the entering values (31/1), which hold at entering; it can only fire after
  integration if a landing regresses those counts. This mutant is unkillable at f63d1ab0; it must be rerun
  against the LANDED state to exercise its clause.

None of the survivors threatens the frozen contract; they are coverage findings, recorded as such.

## 5. Falsifier set for the L1 (run against the landed tool after integration)

Patches attached in this directory: `Mo92M01Mut-m1.patch` … `Mo92M01Mut-m8.patch` (each the exact single-point
edit above, generated with `git diff f63d1ab030d4179576e494342f48ef8718e497a5 -- tools/mori-source-digest.py`
in the scratch clone). The L1 must apply each patch to a scratch copy at the landing revision, run the landed
gate (`python3 -I tools/mori-source-digest.py corpus/SOURCES.md
.ufo/waves/round-90/w1/Mo90S01Sources/sources`) and `--selftest`, require the mutant to be DETECTED (run
summary/exit or `DIGEST_SELFTEST fail>0` diverging from the landed baseline), and restore exact bytes
(sha256-verified) after each probe. Expected detection at the landing rev:
m1, m3, m4, m5, m6, m8 must flip the landed gate's verdict (m1 flips any exact-equality digest comparison, m3/m8
hit the unpinned accounting, m4 the prefix-only accounting, m5 the summary, m6 row scope); m2 and m7 stay dormant
on any corpus without mixed-verdict rows / uppercase digests — their falsification must come from the landed
`--selftest` cases (mixed-pair row; uppercase recorded digest), which is exactly why the selftest needs those two
cases among its ≥8. Counter mutants c1, c3, c2m1, c2m2 are counter-side falsifiers (counter bytes are frozen; do
not patch the frozen counters — they are listed for the record only). c1-c2 and c2m3 exercise the floor and
no-harm clauses and can only fire in their armed states (post-integration for c2m3; `missing==0 ∧ knowledge<98`
for c1-c2).

## Restoration evidence

- After every cycle the mutated path was rewritten with pristine bytes and sha256-verified equal to the
  pre-cycle hash: tool `a692b159…`, count-c1 `cfa154d6…`, count-c2 `ebe4077d…`.
- After each tool cycle `git status --porcelain -- tools/mori-source-digest.py` in the scratch clone was empty.
- Final restored-bytes rerun of all three detectors reproduces all three baseline lines exactly (tool rc=1,
  count-c1 rc=1, count-c2 rc=1).
- Counter mutant files and the spy fixture lived only in scratch; the scratch clone's tree ends byte-identical
  to f63d1ab0 plus the two untracked counter copies placed for the runs (scratch is deleted after this report).

## Incident disclosure

One diagnostic cell ran `shutil.copy` with a kernel-cwd-relative destination, which created
`/home/vgpnk/Projects/shokunin/tools/mori-source-digest.py` (the file did not exist before: the directory-entry
mtime 05:12:56.450 marks its creation during my write window; `tools/` is untracked in the fleet repo,
`?? tools/`). The same cell immediately rewrote it with pristine bytes (hash verified `a692b159…`), and I have
since removed the file, restoring the prior state (absence). No lane file was touched. Lesson recorded: absolute
paths only, in every kernel.

## Tooling

Nothing installed or upgraded (system `python3` + `git` only). No pacman command run. No task tools, no
`agent://all`, no model passed.

Report: .ufo/waves/round-92/w1/Mo92M01Mut.md
