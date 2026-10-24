# RevScratch — scratch uniqueness & path discipline (mori r37, w1)

**Attack item:** contract row g (seed-collision scratch paths, `mkdtemp` per arm) + row e (`display_path`
repo-relative printing) against `count-c1.py`/`count-c2.py`. Method: two same-seed concurrent counter runs
vs a serial run, source inspection of `_scratch_parent`/`mkdtemp`, and an absolute-path scan of all output.

**Version note (all runs below specify which counter):** the freeze pin (`evidence/freeze-r37.txt`) matches
the blobs at the scored tip `e57c58b` (verified: `git show e57c58b:…` → `count-c1.py 7518fef8`,
`count-c2.py 6213cf9a` = pinned). The worktree/HEAD (`e33bb56`, moved twice mid-review) carries a *newer*
counter generation (`count-c1.py` 1020 ln, adds a "drawn arm"; `count-c2.py` 236 ln). I measured **both**:
pinned blobs extracted to `/fast/scratch/hyaku/mori-r37/RevScratch/pinned/` and the worktree files.

## Measurements

### 1. Pinned counter (scored artifact) — concurrent same-seed

```
cd /home/vgpnk/Projects/shokunin/mori-shokunin
git show e57c58b5:.ufo/waves/round-37/count-c1.py > pinned/count-c1.py   # hash 7518fef8 = pin
python3 pinned/count-c1.py e57c58b5 --seed 11   # run A ─┐ launched concurrently (background &)
python3 pinned/count-c1.py e57c58b5 --seed 11   # run B ─┘
python3 pinned/count-c1.py e57c58b5 --seed 11   # run C, serial
exits: A=0  B=0  C=0        all print C1=met, seed=11
```

`diff p1-A.txt p1-B.txt` — the ONLY difference is the mkdtemp tool-copy path:

```
2c2
< tool: /tmp/mori-c1-tool-s5byr5rm/mori-sources-appendonly.py
---
> tool: /tmp/mori-c1-tool-868kx3nr/mori-sources-appendonly.py
```

Identical verdicts, identical blind/real/challenge/negative lines, identical coverage counts — the same
seed draws the same 24 sandboxes in **distinct** scratch roots (see §3), so no collision.

```
python3 pinned/count-c2.py e57c58b5   # A and B concurrent
exits: A=0  B=0        diff p2-A.txt p2-B.txt: EMPTY (byte-identical, deterministic; C2=met)
```

### 2. Worktree counter (new generation) — concurrent same-seed

```
python3 .ufo/waves/round-37/count-c1.py e57c58b5 --seed 11   # A,B concurrent; C serial
exits: A=0  B=0  C=0        C1=met, seed=11 (adds "drawn arm: pass (4.3s) rev=52d636d501 base=5dff52a1ba")
diff A vs B: only line 2 differs — tool: /tmp/mori-c1-tool-zzf0w4z4/… vs /tmp/mori-c1-tool-h1smpkn6/…

python3 .ufo/waves/round-37/count-c2.py e57c58b5            # A,B concurrent; C serial
exits: A=1  B=1  C=1        C2=unmet — knowledge FAIL (cited_commit=False), live FAIL (sentence=False)
                            (new counter demands commit `1caa242` + a different live sentence; scored tip
                             still measures C2=met under the PINNED counter — pin is what was scored)
python3 .ufo/waves/round-37/count-c2.py e57c58b5 --seed 11  → exit 2
  stderr: "count-c2.py: error: unrecognized arguments: --seed 11"   (c2 has no seed; deterministic)
```

### 3. Scratch directories observed (20 ms poll during the concurrent window)

- Two concurrent runs each created their own `mkdtemp` roots, e.g. `…/mori-r37/c1-h4bemae2/` vs
  `c1-qlz0n1oq/` concurrently, `c1-neg-*` ×2, `/tmp/mori-c1-tool-*` ×2, `challenge-*` under
  `.ufo/waves/round-37/scratch/` — all `mkdtemp`, no seed-derived name (`Sandbox.path = <scratch>/repo%02d`
  under the per-run root).
- **Cleanup: all of my runs' dirs removed** (tool dirs `zzf0w4z4 h1smpkn6 t6oxgqv1 s5byr5rm 868kx3nr`
  verified gone). Stale dirs from OTHER seats exist: `…/mori-r37/c1-3f9no6a8/` (mtime 17:16:51, holds
  repo00–03 — a leaked blind draw from an interrupted seat) and empty `/tmp/mori-c1-tool-88kzu18y/`,
  `/tmp/mori-c1-tool-s2zsi9z8/` (17:16–17:19, predate my window 17:22+). The counter only masks cleanup
  errors (`rmtree(ignore_errors=True)`), so a hard-killed seat leaks scratch — harmless but observable.
- `…/round-37/scratch/` (CHALLENGE_PARENT) persists as an empty dir after runs — `makedirs(exist_ok=True)`
  is created once and never removed; untracked, harmless.

### 4. Absolute-path scan of outputs

`grep -E '/home/|/fast/|/tmp/'` over all captured stdout/stderr: only `tool: /tmp/mori-c1-tool-*/…`
(outside the repo — correct per `display_path` contract) and `counter setup error:` echoes below. **No
absolute lane path in any measured output.** With `--tool` passed ABSOLUTE
(`--tool /home/vgpnk/…/fixtures/memo-n1.py`): `tool: .ufo/waves/round-37/fixtures/memo-n1.py` — repo-relative ✓.
Receipts confirm: `c1-before-memo.txt` was manually redacted (`<lane>`) — predates `display_path`; the
current counter makes that redaction unnecessary for the tool line.

## Findings (severity order)

1. **MEDIUM — worktree counters drifted past the freeze mid-wave.** `count-c1.py`/`count-c2.py`/`contract.md`
   in the worktree (HEAD `e33bb56`) are NOT the pinned blobs (pins match `e57c58b` exactly). Re-running the
   receipt command on the worktree reproduces C1 but reports `C2=unmet` (new checks demand commit `1caa242`
   and a different live sentence). The contract sanctions this ("a change … is a new counter version"), and
   the pin keeps the scored claim anchored — but anyone re-executing worktree counters against the scored
   tip gets a different verdict than the receipt. Evidence: `git diff e57c58b..HEAD --stat` →
   `count-c1.py 70 +/-`, `count-c2.py 27 +/-`, `contract.md +38`; run outputs above.
2. **LOW — setup-error paths echo absolute lane paths on stderr.** `python3 pinned/count-c1.py deadbeef
   --seed 11` → exit 2, stderr: `counter setup error: … failed in /home/vgpnk/Projects/shokunin/mori-shokunin:
   fatal: Needed a single revision` (pinned counter `:857-860`, `:868`, `:877`; same pattern in worktree
   `:905-913`). `display_path` is applied only to the `tool:` stdout line; error paths print `args.repo`/
   fixture args verbatim. Row-e's scope ("evidence carries no absolute operator path") still holds since
   these only fire on exit-2 and echo caller-supplied args — but the letter of "lane paths print
   repo-relative" is not universal.
3. **LOW — committed bytecode at the scored tip embeds absolute paths.**
   `git show e57c58b5:.ufo/waves/round-37/__pycache__/count-c1.cpython-314.pyc | strings` contains
   `/home/vgpnk/Projects/shokunin/mori-shokunin`, `/home/vgpnk/…/round-37/count-c1.py`,
   `/fast/scratch/hyaku/mori-r37`. A committed `.pyc` (someone ran the counter in-place and committed the
   cache) carries exactly the operator paths row e wanted out of committed state. Already deleted between
   tip and HEAD.
4. **LOW/residual — `display_path` uses `abspath`, not `realpath`.** Demonstrated: with `--repo` given via
   symlink `/tmp/lanelink-r37 → lane`, `display_path(<lane>/tools/x.py, '/tmp/lanelink-r37')` → prints
   `/home/vgpnk/…/tools/x.py` absolutely. Also: `challenge_arm` materializes a nested git repo inside the
   lane worktree (`os.makedirs(CHALLENGE_PARENT)`, `count-c1.py:810-811`); transient and cleaned in
   `finally`, but a `jj` snapshot landing inside the window could absorb the untracked scratch repo into a
   working-copy commit. Neither fires in the declared invocation.

## Residual risk / gaps

- Collision→exit-2 is structural (`mkdtemp` `FileExistsError` → outer `except` → exit 2); not exercised live
  since real collisions are astronomically unlikely. Forced error paths (`deadbeef` rev, `c2 --seed`) do
  return 2 as claimed.
- Stale scratch from killed seats accumulates under `/fast/scratch/hyaku/mori-r37/` (observed), and
  `…/round-37/scratch/` lingers empty — cosmetic.
- `count-c2.py` cannot take `--seed`; "same seed" applies only to c1. C2's determinism makes the concurrent
  criterion trivially satisfied (byte-identical output).

No tools installed (pacman paused; none needed). Scratch: `/fast/scratch/hyaku/mori-r37/RevScratch/`
(captures: `c1-{A,B,C}.*`, `c2-{A,B,C}.*`, `pinned/p{1,2}-*`, `polldirs.txt`, `c1-badrev.txt`).

**VERDICT: PASS** — concurrent same-seed runs both complete with identical verdicts on both the pinned and
worktree counters (collision ⇒ exit 2 by mkdtemp failure, never a wrong verdict), and every lane path in
measured output prints repo-relative; findings are edge/hygiene residuals that do not falsify rows e/g.
