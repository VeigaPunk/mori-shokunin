# LabC1Concurrent — concurrent-runs probe of `count-c1.py`

Seat: `mori-r37-w1-LabC1Concurrent` (leaf). Scored revision probed: `e57c58b57c025364e79d130fbdf764d2674d83d6`.
Lane repo read-only; all scratch under `/fast/scratch/hyaku/mori-r37/LabC1Concurrent/`.

## Hypothesis under test (what this attacks)

Two concurrent runs of the C1 counter with the same explicit seed never produce a wrong
verdict: either both print `C1=met` (exit 0) or a genuine scratch collision surfaces as a
setup error (exit 2). Any run printing `C1=unmet` (exit 1), a differing verdict line, a
`counter setup error`, or a coverage/negative result that differs from its twin falsifies it.

Why it is not vacuous: `--seed` makes the blind and challenge draws reproducible, so two
same-seed runs build the same sandbox indices (`repo00..repo23`, challenge index) and would
land on the same directory names if any writable root were fixed instead of per-run unique.

## Method

- Seed `20261023`, identical for all runs; revision argument `e57c58b57c025364e79d130fbdf764d2674d83d6`.
- Cwd = lane repo; candidates launched with `&` back-to-back and joined with `wait`, three rounds.
- Canonical batch (`run-pairs.sh`): three rounds x two concurrent runs = the six required runs,
  stdout/stderr/exit code captured per child (`r{1,2,3}-{a,b}.{out,err,code}`).
- Timed replicate (`run-timed.sh`): same three-pair shape again, each child recording its own
  start/end epoch (`t{1,2,3}-{a,b}.span`) so overlap is measured rather than assumed.

Command for every run (from `/home/vgpnk/Projects/shokunin/mori-shokunin`):

```
python3 .ufo/waves/round-37/count-c1.py e57c58b57c025364e79d130fbdf764d2674d83d6 --seed 20261023
```

## Result — canonical six runs

| run | exit | verdict line | seed line | arm block |
|---|---|---|---|---|
| r1-a | 0 | `C1=met` | `seed=20261023` | blind 24/24 (deletions=20 changed-back=15 superseded=9); real pass; challenge pass; 3/3 negatives rejected |
| r1-b | 0 | `C1=met` | `seed=20261023` | identical |
| r2-a | 0 | `C1=met` | `seed=20261023` | identical |
| r2-b | 0 | `C1=met` | `seed=20261023` | identical |
| r3-a | 0 | `C1=met` | `seed=20261023` | identical |
| r3-b | 0 | `C1=met` | `seed=20261023` | identical |

Verbatim tail of each of the six `.out` files:

```
negative memo-n1.py     rejected (challenge: lists differ: ...)
negative const.py       rejected (blind 4/4 (repo200: lists differ))
negative summary-only.py rejected (blind 4/4 (repo200: per-id lines differ (malformed=0)))
C1=met
seed=20261023
```

Exit codes read from the six `.code` files: `0 0 0 0 0 0`. No `counter setup error`, no
`tool_absent`, no `C1=unmet`, no stderr bytes on any run (`*.err` all empty).

## Result — timed replicate (overlap evidence)

Each pair starts on the same clock tick and the two children overlap for essentially the whole
run; all six exit 0 with `C1=met`:

```
t1: a=[1792786313.598,1792786317.809) b=[1792786313.598,1792786317.793) overlap=4.195s
t2: a=[1792786317.810,1792786321.932) b=[1792786317.810,1792786321.934) overlap=4.122s
t3: a=[1792786321.941,1792786326.197) b=[1792786321.941,1792786326.222) overlap=4.255s
   t1-a: exit=0 verdict=['C1=met'] ['seed=20261023']      t1-b: exit=0 verdict=['C1=met'] ['seed=20261023']
   t2-a: exit=0 verdict=['C1=met'] ['seed=20261023']      t2-b: exit=0 verdict=['C1=met'] ['seed=20261023']
   t3-a: exit=0 verdict=['C1=met'] ['seed=20261023']      t3-b: exit=0 verdict=['C1=met'] ['seed=20261023']
```

## Result — cross-run identity

All twelve outputs (six canonical + six timed) hash to a single normalized value:
`sha256[:12] = ef2f25ee9312` (12/12), after normalizing only elapsed-seconds fields and the
per-run `/tmp/mori-c1-tool-*/` directory name:

```
ef2f25ee9312 12 ['r1-a.out','r1-b.out','r2-a.out','r2-b.out','r3-a.out','r3-b.out',
                 't1-a.out','t1-b.out','t2-a.out','t2-b.out','t3-a.out','t3-b.out']
distinct normalized outputs: 1
```

So concurrency changed neither the coverage counts, the real-arm lists
(`appendonly_violations=18 ids=[S041,...,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]`),
the challenge truth, nor any negative verdict.

## Mechanism (why no collision is reachable by design)

Every writable location is a fresh per-run `mkdtemp`; no fixed shared filename exists in the
counter:

- `count-c1.py:872` — `tool_dir = tempfile.mkdtemp(prefix="mori-c1-tool-")` (extracted tool copy).
- `count-c1.py:891-892` — `_scratch_parent()` then `tempfile.mkdtemp(prefix="c1-", dir=parent)` (blind + real arm sandboxes).
- `count-c1.py:932` — `tempfile.mkdtemp(prefix="c1-neg-", dir=parent)` (negative draws).
- `count-c1.py:763` — `tempfile.mkdtemp(prefix="challenge-", dir=CHALLENGE_PARENT)` (real-arm-clothing repo).
- `count-c1.py:823` — probe dir is `mkdtemp` + `rmdir`, so the parent probe is race-safe.
- Inner sandbox paths are `repo%02d` under that unique root (`count-c1.py:314`), never absolute-global.
- Real arm runs read-only git on the lane repo (`count-c1.py:686-737`); no index/HEAD writes.

## Artifact check (no residue)

```
-- lane challenge scratch:
   (empty)
-- shared scratch root: (only the assigned seat dirs; no c1-*/challenge-* leftover)
-- git status (porcelain, lane): 12 lines, all sibling reporters' `w1/*.md` and `.scratch/`;
   nothing from this probe
```

`git status --porcelain` line count: 12, unchanged set of sibling untracked files; no
`challenge-*`, `c1-*` or `.probe-*` entries.

## Risks / notes

- Transient nesting: `challenge_arm` creates a throwaway git repo inside the lane working copy
  (`.ufo/waves/round-37/scratch/challenge-*`) and removes it in `finally` (`count-c1.py:762-795`).
  During those ~0.1 s a concurrent *jj* snapshot by another seat could observe the nested repo.
  Not observed here (no seat ran jj during the probe), and outside this leaf's province.
- Shared scratch parent `/fast/scratch/hyaku/mori-r37` is probed by `mkdtemp`/`rmdir`
  (`count-c1.py:821-825`), so a sibling's cleanup sweep cannot make the probe pick a bad parent.
- No tools installed or upgraded. No model parameter passed. No pacman.
- Only read-only lane commands were run (`python3 .ufo/waves/round-37/count-c1.py`, `git status --porcelain`, `ls`).

## Acceptance mapping

Six concurrent runs, exit codes `0 0 0 0 0 0`, verdict lines all `C1=met` with `seed=20261023`;
no setup error, no `C1=unmet`, no divergent arm/negative line. Hypothesis survived.

VERDICT: PASS
