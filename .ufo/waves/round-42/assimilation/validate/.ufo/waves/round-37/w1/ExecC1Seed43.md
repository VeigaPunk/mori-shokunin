# w1/ExecC1Seed43 — C1 counter execution at seed 43

**Item attacked:** claim C1 (measurement discrimination) as a *measured* artifact — this seat
executes the scored predicate command at `--seed 43`, replays it, and probes the border states the
receipt does not cover (control revisions, exit-code semantics, timeout state, seed stability,
path hygiene).

**Verdict:** `VERDICT: PASS` — `C1=met`, exit 0 at seed 43, reproduced; all controls behave.
Three non-blocking observations are recorded in §6 (a v3 counter/contract predicate divergence,
a drawn-arm pool dependency, and `--tool` relative-path handling).

Lane bounds honoured: read-only on the lane; this report is the only file written by this seat.
Scratch: `/fast/scratch/hyaku/mori-r37/ExecC1Seed43/`. No tool installs.

---

## 1. Axes (godspeed)

| axis | question |
|---|---|
| A1 acceptance | does the assigned command print `C1=met` and exit 0? |
| A2 replay | does the same seed reproduce the same measured arms? |
| A3 seed robustness | is the pass a property of the counter or of seed 43? |
| A4 controls | does the counter still say `unmet`/setup-error when it must (tool absent, bad rev, hanging tool)? |
| A5 hygiene | does a run leak absolute operator paths or scratch into the lane? |
| A6 instrument identity | is the counter that ran the counter that is pinned/committed? |

## 2. Target (A1) — the assigned command

```
cd /home/vgpnk/Projects/shokunin/mori-shokunin && python3 .ufo/waves/round-37/count-c1.py e57c58b57c025364e79d130fbdf764d2674d83d6 --seed 43; echo EXIT=$?
```

Observed (final run of three, counter blob `3e15f9fd35b6a926396732ddc970ff92ced8c113`):

```
P-C1: at revision R, tools/mori-sources-appendonly.py prints exactly the counter's hidden truth for ids, deleted, superseded and round_changed, and exactly the truth's per-id `changed`/`deleted` lines, on each of 24 sandbox SOURCES.md histories drawn at run time, on the lane's own history (rev 6bd57097, round base f10a320d) where the independent oracle lists at least one id, and on one run-time-drawn challenge history presented in real-arm clothing (lane path, lane git identity, lane title); and the same counter rejects all three negative fixtures (a real-arm memoizer, a constant printer, a summary-only printer) and matches the standing truth on one run-time-drawn ancestor revision of the lane repository whose expected answer is not the published real-arm…
tool: /tmp/mori-c1-tool-gch6msj6/mori-sources-appendonly.py
blind arm: 24/24 sandbox histories matched the hidden truth (1.9s; coverage: deletions=21 changed-back=15 superseded=10)
real arm: pass (0.3s)
  tool:   appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]
  oracle: appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]
  tool exit=1
drawn arm: pass (4.2s) rev=f04acbe512 base=30dfe70fad
  truth:  appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] round_changed=[]
  tool:   appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] round_changed=[]
challenge arm (real-arm clothing): pass (0.1s)
  truth:  appendonly_violations=3 ids=[S023,S267] deleted=[S129] superseded=[S267] round_changed=[S023]
  tool:   appendonly_violations=3 ids=[S023,S267] deleted=[S129] superseded=[S267] round_changed=[S023]
negative memo-n1.py     rejected (challenge: lists differ: want appendonly_violations=4 ids=[S193] deleted=[S074,S164,S199] superseded=[] round_changed=[S074,S199,S238] got appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193])
negative const.py       rejected (blind 4/4 (repo200: lists differ))
negative summary-only.py rejected (blind 4/4 (repo200: per-id lines differ (malformed=0)))
C1=met
seed=43
EXIT=0
```

The printed predicate is line-truncated at 768 bytes by the tool harness in this transcript; the
counter's full `PREDICATE` literal was extracted independently (§6.1) and ends
`...whose expected answer is not the published real-arm constant.`

Same command also executed against the **revision-pinned v1 counter**, extracted from the scored
tip rather than the worktree (`git show e57c58b…:…/count-c1.py` →
`/fast/scratch/hyaku/mori-r37/ExecC1Seed43/count-c1-pinned-v1.py`), `--seed 43`: `C1=met`, `EXIT=0`,
with `real arm: pass`, `challenge arm: pass` (`truth/tool` = `violations=2 ids=[S267] deleted=[S201]
superseded=[S267] round_changed=[S201]`), three negatives rejected. Receipt copy:
`run-pinned-v1.txt`.

## 3. Replay (A2)

Two runs at `--seed 43`, normalising only arm timings (`(N.Ns)` → `(Xs)`) and the `mkdtemp` tool
path, are byte-identical under the v1 counter:

```
diff <(sed -E 's/\(([0-9.]+)s\)/(Xs)/; s#/tmp/mori-c1-tool-[a-z0-9_]+/#/tmp/TOOL/#' run43.txt) \
     <(sed -E 's/\(([0-9.]+)s\)/(Xs)/; s#/tmp/mori-c1-tool-[a-z0-9_]+/#/tmp/TOOL/#' final-run.txt)
```

→ only the blind-arm timing line differs. Blind coverage identical (deletions=21 changed-back=15
superseded=10), real-arm lists identical, challenge truth identical (`S267`/`S201`), negative
rejection reasons identical. Under the current (v2/v3) counter, two runs at seed 43 differ in the
*drawn arm rev only* — see §6.2.

## 4. Seed robustness (A3)

```
for s in 41 42 43 44 100 2024 7777; do python3 .ufo/waves/round-37/count-c1.py e57c58b… --seed $s; done
```

observed, current counter:

```
seed=41 rc=0 C1=met acc=0 drawn=1
seed=42 rc=0 C1=met acc=0 drawn=1
seed=43 rc=0 C1=met acc=0 drawn=1
seed=44 rc=0 C1=met acc=0 drawn=1
seed=100 rc=0 C1=met acc=0 drawn=1
seed=2024 rc=0 C1=met acc=0 drawn=1
seed=7777 rc=0 C1=met acc=0 drawn=1
```

`acc=0` = no negative fixture printed `ACCEPTED`. Seed 43 is not a lucky draw at the counter
level; blind coverage at seed 43 clears the frozen floors (deletions 21 ≥ 12, changed-back 15 ≥ 12,
superseded 10 ≥ 1). Same seven-seed sweep on the v1 counter: all `C1=met`, no `ACCEPTED`.

## 5. Controls (A4) and hygiene (A5)

| control | command | observed |
|---|---|---|
| tool absent at rev | `count-c1.py 5842dc045bb3d3b7aa2bdaaf462dcff536358444 --seed 43` (parent of the tool's add commit `bf0df77`) | `tool_absent` / `C1=unmet` / `seed=43` / `EXIT=1` |
| unresolvable rev | `count-c1.py deadbeef… --seed 43` | `counter setup error: git rev-parse --verify … failed` on stderr, `EXIT=2` |
| challenge clothing | challenge sandbox rebuilt with the counter's own `build_sandbox` (`identity=LANE_IDENTITY, title=LANE_TITLE`) | `git config --local user.name` = `mori-shokunin`, `user.email` = `mori@shokunin.local`, first SOURCES line = `# mori-shokunin — SOURCES registry (challenge arm)`; blind sandboxes carry `mori counter` + `# SOURCES - sandbox registry`, so `memo-n1.py` is honest only in the blind arm |
| timeout, plain hang | copied counter, `TOOL_TIMEOUT_S=3`, sleeper child through `check_blind` | `ok: False`, `exit: 124`, `reason: no summary line (exit 124)` — distinct from a list mismatch |
| timeout, SIGTERM-ignoring child | same, child ignores SIGTERM | `ok: False`, `exit: None`, `reason: tool_timeout: tool exceeded 63s (SIGTERM, then SIGKILL after 1s)` |
| absolute-path leak | `grep -n "/home/"` over a full seed-43 run's stdout+stderr | `NO_HOME_PATH_AT_ALL` (only `/tmp/mori-c1-tool-*` is printed; lane paths go through `display_path`) |
| lane mutation | `git status --porcelain` after all runs | no lane file touched by this seat; the only untracked paths are the wave's own `w1/` reports and `.scratch/`. Counter leaves an empty `.ufo/waves/round-37/scratch/` parent (challenge `mkdtemp` parent) and removes each `challenge-*` root |

## 6. Instrument identity (A6) — three observations, none blocking C1=met

### 6.1 Counter/contract predicate divergence (current counter)

The contract's frozen P-C1 blockquote (`.ufo/waves/round-37/contract.md:20-26`) still equals the
**v1** counter predicate exactly:

```
python3 - (normalised compare) -> contract==v1: True ; contract==v2: False
```

while the current counter (blob `3e15f9fd35b6a926396732ddc970ff92ced8c113`, v3 pin) prints a
**longer** predicate: the negatives clause becomes
`…rejects all three negative fixtures (a real-arm memoizer, a constant printer, a summary-only
printer) and matches the standing truth on one run-time-drawn ancestor revision of the lane
repository whose expected answer is not the published real-arm constant.`
(776 bytes vs 624 for v1.)

So the contract's stated invariant "P-C1 (frozen, verbatim in the counter's PREDICATE and in the
report)" holds for the scored tip `e57c58b` (v1) but **not** for the amended counter now committed
at `HEAD a187534`. `evidence/freeze-r37-v3.txt` declares the counter amendment as a new version, but
the contract's P-C1 text was not updated to match, so the two no longer compare equal. Recorded, not
remediated (lane is read-only for this seat).

### 6.2 Drawn arm is not seed-replayable

`draw_real_rev()` draws `rng.choice(candidates)` over `git rev-list --max-count=40 HEAD` of the lane
repo. Because the candidate pool is the *live* lane history, the same `--seed 43` drew different
arms across two consecutive runs of the same counter blob:

```
run 1: drawn arm: pass rev=5631efa997 base=0a05f7e676
run 2: drawn arm: pass rev=f04acbe512 base=30dfe70fad
```

and `evidence/c1-after-v2.txt` recorded `rev=1ae1d6d692 base=5631efa997`. All pass, but a seed does
not pin the drawn rev: replay evidence for that arm is only valid against a fixed repo state. The
blind arm (the seed-replayable part the docstring claims) is unaffected — coverage and results were
identical at seed 43 across runs.

### 6.3 `--tool` with a relative path fails

`run_tool()` executes with `cwd="/"` and passes `tool` through unchanged, so
`--tool .ufo/waves/round-37/fixtures/summary-only.py` runs
`python3 //.ufo/waves/…/summary-only.py` → `no summary line (exit 2)` on every blind history
(`blind arm: 3/24`, exit 1). Absolute `--tool` paths work. The scored path (no `--tool`; tool read
via `git show <rev>:…`) is unaffected, and the counter's own negative fixtures are passed as
absolute paths. Cosmetic.

## 7. Evidence index (all under `/fast/scratch/hyaku/mori-r37/ExecC1Seed43/`)

| file | content |
|---|---|
| `final-current.txt` | final seed-43 run, current counter (quoted §2) |
| `run-v2worktree.txt` | earlier seed-43 run, same counter blob |
| `run43.txt`, `final-run.txt` | two seed-43 runs, v1 counter (replay pair, §3) |
| `run-pinned-v1.txt` | seed-43 run of the counter extracted from `e57c58b` |
| `count-c1-pinned-v1.py` | v1 counter copy extracted from the scored tip |
| `pred-v1.txt`, `pred-v2.txt` | full `PREDICATE` literals, both versions |
| `c1copy.py` | counter copy used for the timeout/identity probes |

## 8. Files changed

- `.ufo/waves/round-37/w1/ExecC1Seed43.md` (this report) — the only lane write.
- All other writes are scratch under `/fast/scratch/hyaku/mori-r37/ExecC1Seed43/`.

Installs/upgrades: none.

## 9. Risks

- R1 (6.1): the contract's "verbatim in the counter's PREDICATE" invariant no longer holds for the
  committed v3 counter; a reader comparing contract P-C1 to a fresh run's first line will see a
  mismatch.
- R2 (6.2): drawn-arm replay claims cannot be checked from `--seed` alone; a receipt must record
  `rev`/`base` *and* the lane HEAD it was drawn from.
- R3 (5, timeout): the common hang path surfaces as `exit 124` / "no summary line", not
  `tool_timeout`; only a SIGTERM-ignoring child reaches `tool_timeout`. Both are distinct from a
  list mismatch, which is what the contract's debt-(f) disclosure requires.

VERDICT: PASS
