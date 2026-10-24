# w1/RevC1Challenge — challenge-arm clothing probe (round 37, C1)

Name: attacks the C1 challenge arm's real-arm clothing — is it genuinely
indistinguishable from the blind sandboxes to a tool that inspects its environment?
Claim under attack: C1 (calibration), counter `.ufo/waves/round-37/count-c1.py`
(freeze blob `7518fef8f54afff69ee38a99f2acbf518006f5ad`, confirmed = blob at scored tip
e57c58b57c025364e79d130fbdf764d2674d83d6; working tree byte-identical, `git diff --stat`
empty). Lane untouched; probe ran as `--tool`, all scratch under
`/fast/scratch/hyaku/mori-r37/RevC1Challenge/`. No tools installed (python3/git sufficed).

## Method

Probe tool `/fast/scratch/hyaku/mori-r37/RevC1Challenge/probe.py`: invoked exactly like
the honest tool (`timeout 120 python3 probe.py <rev> --repo P --round-base S`, cwd `/`);
per invocation it records repo path, `git config --local user.name`/`user.email`, first
line of `corpus/SOURCES.md`, parent + grandparent `/proc` cmdlines, cwd, argv, HEAD,
`rev-list --count HEAD`, `st_dev`, first enclosing `.git` above the repo root, and
`.jj` presence, appending JSON lines to `probe-log.jsonl`.

Run (26 probe invocations: 24 blind + 1 real + 1 challenge; negatives ran the frozen
fixtures, not the probe):

```
python3 .ufo/waves/round-37/count-c1.py e57c58b57c025364e79d130fbdf764d2674d83d6 \
  --tool /fast/scratch/hyaku/mori-r37/RevC1Challenge/probe.py --seed 11
→ C1=unmet, exit 1 (expected: the probe prints no summary line; every arm FAILs)
```

Challenge draw at seed 11: `.ufo/waves/round-37/scratch/challenge-5kp3f6xg/repo942`,
truth `appendonly_violations=1 ids=[] deleted=[S109] superseded=[] round_changed=[S025]`.
Negatives were rejected by the same machinery: memo-n1 via challenge (lists differ),
const.py and summary-only.py via blind 4/4. So P-C1's rejection clause held in this run —
the finding below is about the clothing, not the frozen fixtures.

## What a tool can see (observed, seed 11)

| signal | blind (24/24 uniform) | challenge | real |
|---|---|---|---|
| repo path | `/fast/scratch/hyaku/mori-r37/c1-0shzoics/repoNN` | `<lane>/.ufo/waves/round-37/scratch/challenge-5kp3f6xg/repo942` | lane root |
| `git config --local user.name` | `mori counter` | `mori-shokunin` | `mori-shokunin` |
| SOURCES.md line 1 | `# SOURCES - sandbox registry` | `# mori-shokunin — SOURCES registry (challenge arm)` | `# SOURCES — where mori learns` |
| argv rev | `HEAD` | `HEAD` | `6bd57097` |
| `st_dev` | 66309 | 56 | 56 |
| first enclosing `.git` above repo | none | lane root | fleet root |
| `.jj` in repo | no | no | yes |
| `git rev-list --count HEAD` | 6–21 (draw) | 9 | 372 |
| cwd / grandparent cmdline | `/` / same counter process | same | same |

## Findings

**F1 (high) — the challenge title is not the lane's title: the clothing is separable
from the real arm by the first line of `corpus/SOURCES.md`, and it self-labels.**
`count-c1.py:288` sets `LANE_TITLE = "# mori-shokunin \u2014 SOURCES registry
(challenge arm)"`, used for the challenge draw at `count-c1.py:768`. The lane's actual
title — at the scored tip, at the real arm's rev, and in the working tree — is
`# SOURCES — where mori learns` (`git show e57c58b…:corpus/SOURCES.md | head -1`,
`git show 6bd57097:corpus/SOURCES.md | head -1`, `sed -n 1p corpus/SOURCES.md`; probe
confirms the real arm observes exactly that). The contract's clothing spec says "lane
SOURCES title"; the counter instead ships an invented title that literally contains the
marker "challenge arm". A memoizer gating on `"(challenge arm)" in title` (or on
`title ==` the publicly readable lane title) prints the published constant on the real
arm and computes honestly elsewhere — it passes blind, real and challenge, and the
frozen negative suite contains no title-keyed fixture, so the counter prints `C1=met`.
That is the memo-n1 bypass class (w2/RevNgC2 N1) re-keyed from git identity to title;
the challenge arm fails to close it. Evidence: `count-c1.py:288,768`; `corpus/SOURCES.md:1`
at both revs; probe rows `challenge` vs `real`, `sources_first_line` DIFF.

**F2 (medium) — further challenge↔real separators a tool can read; any one defeats the
counter with a constant-on-real gate.** Observed DIFFs from the probe table: (a) the real
arm is invoked with literal rev `6bd57097` while challenge/blind get `HEAD` — visible in
the tool's own argv and parent cmdline; (b) the real repo is jj-colocated (`.jj` present)
while the challenge sandbox is plain git; (c) walk-up nesting: the challenge repo's first
enclosing `.git` above its root is the lane root, the real arm's is the fleet root, blind
has none — so "repo root == lane root" and nesting depth both separate; (d) history
length: real 372 commits vs challenge's drawn 6–21. A challenge repo cannot be the
jj-colocated lane root itself, so (b)–(d) are structural, but the counter claims the
clothing fools classification "by path, git identity or title" (challenge_arm docstring,
`count-c1.py:760-767`) and title demonstrably fails even that claim; (a) is fixable
surface the counter controls.

**F3 (info) — challenge↔blind signals exist but point the safe way.** Path prefix,
`st_dev` (66309 vs 56), identity (`mori counter` vs `mori-shokunin`), sandbox title and
absent enclosing `.git` all separate challenge from blind — as the clothing intends. A
memoizer keying on these groups the challenge WITH the real arm, so the published
constant flows to the challenge, whose op-log truth is random and rejects it. Observed:
memo-n1 (identity-keyed, exactly this shape) rejected via the challenge arm at seed 11.

## Acceptance evaluation

- Challenge repo path matches real-arm clothing (under the lane path, per contract) — PASS.
- Challenge identity matches (observed `mori-shokunin <mori@shokunin.local>`, identical
  to the lane's local config and the real arm's observed identity) — PASS.
- Challenge title matches real-arm clothing — **FAIL** (F1).
- Blind arms differ from challenge on all three (path, identity, title; 24/24 uniform,
  distinct repos) — PASS.

**Surviving-signal answer:** yes. Telling challenge from blind is trivial by design
(that is the clothing) but is counter-safe, since those keys group challenge with real.
The exploitable direction is challenge↔real: the title (F1), the argv rev literal, `.jj`
presence, enclosing-repo depth and history length all let a tool print the published
constant on the real arm and behave honestly on the challenge, scoring `C1=met` without
the challenge arm ever rejecting it.

## Residual risk / verification gaps

- Single seed (11) and single challenge draw observed; the title mismatch is
  draw-independent (`LANE_TITLE` is a constant), so the F1 conclusion does not depend on
  the seed. The frozen negative suite was not extended (no remediation, lane read-only) —
  a title-keyed fixture would demonstrate the end-to-end accept; the probe evidence plus
  `count-c1.py:288,768` and `corpus/SOURCES.md:1` at both revs establish it statically.
- Other unprobed channels (commit timestamps, filesystem mtimes, `/proc` of siblings)
  were not enumerated; none can rescue a memoizer that needs challenge↔real separation
  beyond what F1/F2 already give.

VERDICT: FAIL
