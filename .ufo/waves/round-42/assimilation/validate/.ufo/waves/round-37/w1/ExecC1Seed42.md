# ExecC1Seed42 — round-37 C1 measurement replay at seed 42

**Seat:** `mori-r37-w1-ExecC1Seed42` (executor, leaf)
**Item attacked:** the C1 claim — that `python3 .ufo/waves/round-37/count-c1.py <tip>` decides
`C1=met` for the scored tip, i.e. that the calibration measurement rejects a real-arm memoizer
and a summary-only printer while the honest gate passes blind (24 run-time histories), real
(lane history) and challenge (real-arm clothing) arms.

**Verdict:** `VERDICT: PASS` — `C1=met`, exit code 0, reproduced on three independent runs of
the exact target command plus a same-seed concurrent pair and four extra seeds.

---

## 1. Target command (exact) and full output

```
cd /home/vgpnk/Projects/shokunin/mori-shokunin && python3 .ufo/waves/round-37/count-c1.py e57c58b57c025364e79d130fbdf764d2674d83d6 --seed 42; echo EXIT=$?
```

Full output (stdout+stderr, byte-exact; canonical run captured to
`/fast/scratch/hyaku/mori-r37/ExecC1Seed42/target-run.txt`, 2113 bytes):

```
P-C1: at revision R, tools/mori-sources-appendonly.py prints exactly the counter's hidden truth for ids, deleted, superseded and round_changed, and exactly the truth's per-id `changed`/`deleted` lines, on each of 24 sandbox SOURCES.md histories drawn at run time, on the lane's own history (rev 6bd57097, round base f10a320d) where the independent oracle lists at least one id, and on one run-time-drawn challenge history presented in real-arm clothing (lane path, lane git identity, lane title); and the same counter rejects all three negative fixtures: a real-arm memoizer, a constant printer, and a summary-only printer.
tool: /tmp/mori-c1-tool-qa9r4rx4/mori-sources-appendonly.py
blind arm: 24/24 sandbox histories matched the hidden truth (2.0s; coverage: deletions=22 changed-back=16 superseded=8)
real arm: pass (0.3s)
  tool:   appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]
  oracle: appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]
  tool exit=1
challenge arm (real-arm clothing): pass (0.1s)
  truth:  appendonly_violations=5 ids=[S095,S162] deleted=[S203,S231,S287] superseded=[S095,S162] round_changed=[S162,S203,S231]
  tool:   appendonly_violations=5 ids=[S095,S162] deleted=[S203,S231,S287] superseded=[S095,S162] round_changed=[S162,S203,S231]
negative memo-n1.py     rejected (challenge: lists differ: want appendonly_violations=6 ids=[S210] deleted=[S091,S129,S243,S292,S293] superseded=[S210] round_changed=[S091,S129,S210,S216,S243,S292,S293] got appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193])
negative const.py       rejected (blind 4/4 (repo200: lists differ))
negative summary-only.py rejected (blind 4/4 (repo200: per-id lines differ (malformed=0)))
C1=met
seed=42
EXIT=0
```

**Exit code: 0.** Acceptance condition (C1=met and exit 0) is satisfied.

Two further independent runs of the identical command produced the identical verdict with only
the mktemp tool path and the wall-clock timings differing
(`/tmp/mori-c1-tool-pz103cby/...` → `blind arm: 24/24 … (1.8s)`, `C1=met`, `EXIT=0`;
`/tmp/mori-c1-tool-j2bdr0dm/...` → `blind arm: 24/24 … (2.9s)`, `C1=met`, `EXIT=0`).

## 2. Arm-by-arm reading (what the counter actually decided)

| Arm | Result | Evidence in output |
|---|---|---|
| blind (24 run-time-drawn sandbox `SOURCES.md` histories) | pass 24/24 | `blind arm: 24/24 sandbox histories matched the hidden truth (2.0s; coverage: deletions=22 changed-back=16 superseded=8)` |
| real (lane history rev `6bd57097`, round base `f10a320d`) | pass; oracle lists ≥1 id (18 ids) | `real arm: pass`, tool line == oracle line, `tool exit=1` |
| challenge (run-time-drawn history in real-arm clothing) | pass | `challenge arm (real-arm clothing): pass (0.1s)`; truth == tool, truth drawn from the counter's op log (violations=5, deleted=[S203,S231,S287]) |
| negative `memo-n1.py` (real-arm memoizer) | **rejected** | `challenge: lists differ` — memoizer printed the published real-arm constant (violations=18) instead of the challenge truth (violations=6) |
| negative `const.py` (constant printer) | **rejected** | `blind 4/4 (repo200: lists differ)` |
| negative `summary-only.py` (correct lists, no per-id lines) | **rejected** | `blind 4/4 (repo200: per-id lines differ (malformed=0))` |

Blind coverage at seed 42 (`deletions=22`, `changed-back=16`, `superseded=8`) clears the
counter's own frozen minimums (12/12/1, `count-c1.py:892-895` region: "blind coverage below the
frozen minimum"), so the draw was not degenerate.

## 3. Calibration controls I ran myself (do not trust the claim's own arithmetic)

### 3a. Negative control: the counter does not rubber-stamp a constant printer

A constant tool that prints `appendonly_violations=0 ids=[] deleted=[] superseded=[] round_changed=[]`
and exits 0 was placed in my scratch (`/fast/scratch/hyaku/mori-r37/ExecC1Seed42/bogus.py`) and
substituted via the counter's own `--tool` switch:

```
python3 .ufo/waves/round-37/count-c1.py e57c58b57c025364e79d130fbdf764d2674d83d6 --seed 42 --tool /fast/scratch/hyaku/mori-r37/ExecC1Seed42/bogus.py
→ blind arm: 0/24 sandbox histories matched the hidden truth
→ real arm: FAIL ; challenge arm: FAIL
→ C1=unmet ; EXIT=1
```

So `C1=met` at seed 42 is a discrimination result, not a default.

### 3b. Same-seed concurrency (r36 routed debt g, scratch uniqueness)

Two copies of the exact target command launched simultaneously, same seed 42:

```
conc_a.txt: C1=met  A=0
conc_b.txt: C1=met  B=0
lane scratch residue after both runs: 0 files
```

No collision, no residue in `<lane>/.ufo/waves/round-37/scratch/`. Each arm uses
`tempfile.mkdtemp` (`_scratch_parent`, `count-c1.py:820-838`), so seed-derived shared directories
are not used.

### 3c. Seed sensitivity (the claim must not be a lucky seed)

```
seed=1        rc=0 :: blind arm: 24/24 (1.9s; coverage: deletions=20 changed-back=16 superseded=10) real arm: pass challenge arm: pass C1=met
seed=7        rc=0 :: blind arm: 24/24 (2.2s; coverage: deletions=22 changed-back=15 superseded=10) real arm: pass challenge arm: pass C1=met
seed=999      rc=0 :: blind arm: 24/24 (1.9s; coverage: deletions=20 changed-back=15 superseded=9)  real arm: pass challenge arm: pass C1=met
seed=20261023 rc=0 :: blind arm: 24/24 (2.2s; coverage: deletions=20 changed-back=15 superseded=9)  real arm: pass challenge arm: pass C1=met
```

### 3d. The tool under test is the frozen one

```
git rev-parse e57c58b5...:tools/mori-sources-appendonly.py   → dfb5040b159f7a0b4afedc90a633d997352908f0
git hash-object tools/mori-sources-appendonly.py             → dfb5040b159f7a0b4afedc90a633d997352908f0   (worktree == tip)
git diff --stat e57c58b5... -- tools/mori-sources-appendonly.py → (empty)
```

Matches the freeze pin in `.ufo/waves/round-37/evidence/freeze-r37.txt`
(`dfb5040b159f7a0b4afedc90a633d997352908f0  tools/mori-sources-appendonly.py`). The counter
materialises the tool from `git show <rev>:tools/mori-sources-appendonly.py`, so the measured
program is the committed one, not a working-tree edit.

Tool self-test at the tip (independent of the counter):

```
python3 <tool at rev> --selftest
→ MORI_SOURCES_APPENDONLY_SELFTEST pass=8 fail=0
→ SELFTEST_EXIT=0
```

### 3e. The counter under test is the frozen one

```
git hash-object .ufo/waves/round-37/count-c1.py        → 7518fef8f54afff69ee38a99f2acbf518006f5ad
git rev-parse e57c58b5...:.ufo/waves/round-37/count-c1.py → 7518fef8f54afff69ee38a99f2acbf518006f5ad
sha256sum .ufo/waves/round-37/count-c1.py             → 86699627c7627cc3eea3ba9ea952079d081db390f9ba2be1e1d4d685dd98cdae
```

Both pins equal `freeze-r37.txt` (git blob `7518fef8…`, sha256 `86699627…`). Negative fixtures
at worktree also equal the freeze pins:
`memo-n1.py 19324701f23a225e5ded21c4785c491e7530ac7c`,
`const.py 2f3993a04906ce33033ab207a284d9ca7d7ff57a`,
`summary-only.py 2d62f742fbef39634a5ff04e25b399b87ce4c941`.

### 3f. Predicate is verbatim (contract ↔ counter ↔ report)

Programmatic comparison of the contract's block-quoted P-C1 against the counter's `PREDICATE`
constant (whitespace-normalised):

```
VERBATIM_MATCH: True len 623 623
```

The predicate printed in the run output is byte-identical to the contract's frozen block
(`.ufo/waves/round-37/contract.md:18-27`).

## 4. Files changed

None in the lane repo. This seat wrote exactly one file:

- `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-37/w1/ExecC1Seed42.md` (this report)

Scratch only under `/fast/scratch/hyaku/mori-r37/ExecC1Seed42/`: `bogus.py` (negative control),
`conc_a.txt`, `conc_b.txt`, `target-run.txt`. `git status --porcelain` in the lane shows no
tracked-file modification attributable to this seat; the only untracked lane paths are other
seats' reports and a pre-existing `.scratch/` tree dated 15:48 (round-22 residue, not mine).

No installs, no upgrades, no tool changes were made — no pacman/uv/npm action was required, so
nothing to record under the tooling directive.

## 5. Risks, limits, and open notes (disclosed, not defects found)

1. **Disclosed boundary (contract §C1 "Timeout boundary"):** the counter cannot distinguish a
   slow honest tool from a hung one; a `tool_timeout` is reported as a distinct state and scored
   unmet-by-timeout, never as a list mismatch. My runs showed no timeout (blind arm 1.8–2.9 s for
   24 histories, far under the 120 s budget), so this boundary was not exercised here.
2. **The real arm is a single fixed history** (rev `6bd57097` / base `f10a320d`), so the real-arm
   list set is a single point of truth: `violations=18`, `ids=[S041,…,S193]`,
   `round_changed=[S182,S193]`. This is by design in the frozen predicate, but it means the real
   arm alone would be weak evidence — the discrimination in this run comes from the challenge arm
   (kills the memoizer) and the per-id line check (kills summary-only), both of which fired.
3. **The challenge arm's truth is drawn from the counter's own op log**, so the challenge arm
   cannot catch a bug shared between the counter's op-log bookkeeping and the tool's independent
   git walk *if both are wrong in the same way*. The independent `oracle()` walk over the lane
   history covers that class of shared error for the real arm only; the challenge arm has no
   second oracle. Disclosed by the counter's own design.
4. **Negative fixtures are judged with a 4-history blind draw** (`NEG_BLIND = 4`) rather than 24;
   a negative fixture that happened to be correct on all 4 drawn histories and on the real arm
   and the challenge arm would be accepted. In this run each of the three negatives was rejected
   on a distinct, robust criterion (challenge / blind lists / blind per-id lines).
5. **The memoizer's rejection rests on the challenge arm.** `memo-n1.py` passes blind and (per
   the fixture's design) the real arm by printing a published constant; it is the challenge arm
   that catches it. If the challenge arm were removed, `C1=met` would return for the memoizer —
   matching the contract's stated kill rule.
6. **Concurrent same-seed runs are safe** (verified, §3b), but the challenge arm *does* create
   directories inside the lane repo at `<lane>/.ufo/waves/round-37/scratch/` during a run. Both
   my runs left that directory empty (0 entries), and it is removed in the counter's `finally`
   block; a hard kill mid-run could leave a `challenge-*` directory behind.
7. **Not measured here:** C2 (drift probe), the nine-row drift prose, the r37 `jj` regression
   side-effect scoping, and the knowledge/lesson/QUALITY corpus bindings. Those belong to other
   seats in this wave.

## 6. Conclusion

The C1 claim, as stated in the round-37 contract and as executed by
`.ufo/waves/round-37/count-c1.py` against the scored tip `e57c58b57c025364e79d130fbdf764d2674d83d6`
at seed 42, holds on every clause of P-C1: 24/24 blind histories matched, the real arm matched the
independent oracle (18 ids, non-empty), the challenge arm in real-arm clothing matched its
run-time-drawn truth, and all three negative fixtures were rejected. The counter is the frozen,
pinned artifact, the tool under test is the frozen, pinned artifact, the predicate is verbatim,
and the counter demonstrably refuses to pass a constant printer (`C1=unmet`, exit 1). No defect
found.

VERDICT: PASS
