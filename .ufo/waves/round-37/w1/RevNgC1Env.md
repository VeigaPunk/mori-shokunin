# RevNgC1Env — challenge-arm detection surface of count-c1.py (round-37 w1)

Godspeed axes: (1) detection-power per surface, (2) passing-power of a challenge-only lie,
(3) clothing fidelity of the challenge arm vs the real arm. Attacked claim: C1's challenge
arm (P-C1 clause "one run-time-drawn challenge history presented in real-arm clothing").

Target: `.ufo/waves/round-37/count-c1.py` at e57c58b57c025364e79d130fbdf764d2674d83d6
(working tree verified identical to that rev for the counter and the gate:
`git show e57c58b…:tools/mori-sources-appendonly.py | diff -q - tools/mori-sources-appendonly.py`
→ no output). Method: static reconstruction of the tool-visible surface + live fixture runs
under the real counter. Lane untouched except the counter's own scratch; all fixture code and
logs under `/fast/scratch/hyaku/mori-r37/RevNgC1Env/`.

## 1. Detection-key table

All arms launch the tool identically (`run_tool`, count-c1.py:532-536):
`timeout 120 <python> <tool> <rev> --repo <path> --round-base <sha>`, `cwd="/"`,
`env=clean_env()` (full inherited environ minus the six `GIT_*` redirection keys,
count-c1.py:80-87). Observed values are from the fixture logs recorded during the two live
counter runs (§3), not from source reading alone.

| # | Surface (tool-visible) | blind (24 sandboxes) | real | challenge | isolates challenge? |
|---|---|---|---|---|---|
| K1 | env | same process environ, `GIT_*` popped | identical | identical | **no** — one `clean_env()` at launch, arm-independent |
| K2 | cwd | `/` (observed) | `/` (observed) | `/` (observed) | **no** |
| K3 | parent / grandparent cmdline | `timeout 120 … <tool> …` ← `python3 .ufo/waves/round-37/count-c1.py <rev> [--tool F]` (observed; no arm-identifying argument) | same shape | same shape | **no** — identical strings across arms within one run |
| K4 | argv rev literal | `HEAD` | `6bd57097` (count-c1.py:729) | `HEAD` (count-c1.py:767) | **no alone** — isolates *real*; `HEAD ∧ repo-under-lane` isolates challenge |
| K5 | sandbox header (line 1 of the registry file) | `# SOURCES - sandbox registry` (count-c1.py:287) | `# SOURCES — where mori learns` (measured: `git show 6bd57097:corpus/SOURCES.md \| head -1`, and tip `corpus/SOURCES.md:1`) | `# mori-shokunin — SOURCES registry (challenge arm)` (count-c1.py:288) | **yes** — three distinct strings; title alone separates challenge from both others |
| K6 | git identity (`config --local`) | `mori counter <counter@example.invalid>` (count-c1.py:312,421; observed) | `mori-shokunin mori@shokunin.local` (measured on lane) | forced `mori-shokunin mori@shokunin.local` (`LANE_IDENTITY`, count-c1.py:289,765; observed) | **no** — equals real; separates blind from {real, challenge}. This is the memo-n1 gate, by design the *non*-isolating surface |
| K7 | repo path shape (frontier walk) | outside lane: `/fast/scratch/...` or TMPDIR//tmp (observed `.../c1-liwpvjos/repo00`) | exactly the lane root (observed) | strictly under lane root: `<lane>/.ufo/waves/round-37/scratch/challenge-*/repoNNN` (count-c1.py:56,763; observed `challenge-g11ibp0b/repo988`) | **yes** — `repo == lane_root → real; repo under lane_root → challenge; else blind`. Two directories cannot share a path string, so this key is structurally permanent |
| K8 | side channels (frontier walk) | none: `Sandbox.commit` writes only `corpus/SOURCES.md` (count-c1.py:356-359); truth/op log stay in counter memory; scored seed from `os.urandom` (count-c1.py:851), not in the child env | — | — | no on-disk truth to steal; counter-process memory would be a kernel-level channel outside the six named surfaces — not exercised |

Observation R2 (clothing defect): the challenge title constant `LANE_TITLE` is **not** the
lane's actual registry title. Real arm shows `# SOURCES — where mori learns` (at rev 6bd57097,
at base f10a320d, and at the tip), challenge shows `# mori-shokunin — SOURCES registry
(challenge arm)`. P-C1's prose "lane title" is implemented as a distinct third string, so the
challenge is title-distinguishable from the real arm with zero path logic. This divergence has
no effect on P-C1's operative requirement (the three named negatives are still rejected), but
it is a real seam in the "real-arm clothing" wording.

## 2. Detection key exercised

The fixture classifies by K7 path shape alone, reading no history on any arm:

```
real      : abspath(--repo) == /home/vgpnk/Projects/shokunin/mori-shokunin
challenge : abspath(--repo) strictly under that root
blind     : anything else
```

Fixtures (scratch): `/fast/scratch/hyaku/mori-r37/RevNgC1Env/honest.py` (control: logs the
K1-K7 surface values it observes, then computes honestly everywhere by `runpy`-executing the
lane's real gate) and `/fast/scratch/hyaku/mori-r37/RevNgC1Env/liar-challenge.py` (same
classification and logging; honest on blind and real; on the detected challenge arm prints the
published real-arm constant — the exact c1-after receipt line plus its 18 implied
`changed <id>` lines — reading no history). Logs: `honest.log`, `liar.log` in the same
directory.

## 3. Demonstrated attempts (measured)

**Run A — control (detection without lying).**
`python3 .ufo/waves/round-37/count-c1.py e57c58b57c025364e79d130fbdf764d2674d83d6 --tool /fast/scratch/hyaku/mori-r37/RevNgC1Env/honest.py`

```
blind arm: 24/24 ... (coverage: deletions=23 changed-back=14 superseded=6)
real arm: pass   tool/oracle: appendonly_violations=18 ids=[S041,...,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]
challenge arm: pass
  truth/tool: appendonly_violations=5 ids=[S171,S177] deleted=[S067,S087,S127] superseded=[S171] round_changed=[S067,S087,S127,S177]
negative memo-n1.py rejected (challenge: lists differ ...); const.py rejected (blind 4/4); summary-only.py rejected (blind 4/4)
C1=met   seed=17925880935222926857   EXIT=0
```

An arm-classifying tool passes all three arms: the counter penalizes wrong output, not
detection. `honest.log` recorded exactly 24 blind + 1 real + 1 challenge invocations with the
K1-K7 values of the table.

**Run B — challenge-only liar (the assigned attack).**
`python3 .ufo/waves/round-37/count-c1.py e57c58b57c025364e79d130fbdf764d2674d83d6 --tool /fast/scratch/hyaku/mori-r37/RevNgC1Env/liar-challenge.py`

```
blind arm: 24/24 ...
real arm: pass (constant = oracle, exit 1)
challenge arm: FAIL
  truth: appendonly_violations=4 ids=[S253] deleted=[S068,S266,S279] superseded=[S253] round_changed=[S068,S158,S279]
  tool:  appendonly_violations=18 ids=[S041,...,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]
  reason: lists differ ...
negative liar's peers unchanged; C1=unmet   seed=3341458938564573359
```

`liar.log` shows the classification fired exactly when it should: the single
`arm=challenge rev=HEAD repo_is_lane_root=False under_lane=True title='# mori-shokunin —
SOURCES registry (challenge arm)' user.name='mori-shokunin' cwd=/ repo=.../.ufo/waves/
round-37/scratch/challenge-g11ibp0b/repo988` line — i.e. **detection succeeded perfectly, and
the lie still failed the challenge arm**, flipping the counter to `C1=unmet`.

## 4. Why no detection key lets a liar pass the challenge

The challenge arm is passed only by an exact four-list summary, exact per-id
`changed`/`deleted` lines, and exit 1 iff `round_changed` is non-empty (count-c1.py:767-786).
Its truth is drawn at run time from the counter's RNG (new `os.urandom` seed per scored run)
and exists nowhere but the drawn git history: deleted ids and first-held immutable cells are
absent from the tip file, so no history-free output — constant, tip-derived, identity- or
title-derived — matches except by collision. Runs A/B show the two live draws differ from each
other and from the published constant. Therefore every challenge-isolating key (K5 title, K7
path, K4∧K7) grants detection only; the memo-n1 gate K6 (identity) cannot even isolate the
challenge. Lying *only* on the challenge cannot pass all three arms — demonstrated above.

Boundary note (opposite lie direction, one sentence): a fixture that lies on the *real* arm
only (honest on blind + challenge) does pass all three arms, because the real answer is a
fixed published constant — which is precisely why the challenge arm, the only arm whose truth
is both hidden and fresh, is the load-bearing one in P-C1.

## 5. Residuals (named)

- **R1 (permanent, zero passing power): path-shape detection (K7).** The challenge repo must
  live somewhere, and any `--repo` distinct from the lane root is classifiable; "real-arm
  clothing" can never cover the path axis. An honest tool may classify arms freely (Run A).
- **R2 (clothing divergence, zero passing power): title axis.** `LANE_TITLE`
  (count-c1.py:288) ≠ actual lane title at 6bd57097 (`# SOURCES — where mori learns`), so a
  title-gated detector separates challenge from real without path logic. Either matching the
  real title string or documenting the axis as non-hidden would close the prose/code gap; as
  is, it changes no verdict (all three negatives stay rejected).
- **R3 (not exercised, out of the assigned surface):** reading the counter process's memory or
  `/proc` state to recover the RNG/state would be a kernel-level channel outside env/cwd/
  parent/argv/header/identity; noted, not attempted, no evidence it is closed.

Bounds compliance: exactly one lane file written (this report); no lane edits, no installs
(none needed), no pacman, no subagents. Scratch: `/fast/scratch/hyaku/mori-r37/RevNgC1Env/`
(honest.py, liar-challenge.py, honest.log, liar.log).

VERDICT: PASS — no detection key lets a liar pass the challenge; the surviving detection keys
(R1 path shape, R2 title) are named residuals with zero passing power.
