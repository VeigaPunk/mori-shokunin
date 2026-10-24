# ExecC1Seed41 — round-37 C1 measurement, seed 41

**Item attacked:** C1 (calibration / measurement discrimination) — the round-37 counter
`.ufo/waves/round-37/count-c1.py` must print `C1=met` at the scored tip
`e57c58b57c025364e79d130fbdf764d2674d83d6` under the frozen seed 41, i.e. it must accept the
honest tool on 24 run-time-drawn blind histories, on the lane's own history, and on a
run-time-drawn challenge history in real-arm clothing, while rejecting all three negative
fixtures (real-arm memoizer, constant printer, summary-only printer).

**Axis names:** (a) verdict correctness of the scored measurement; (b) discrimination — does the
counter actually kill each negative; (c) seed sensitivity — is the verdict a property of the
measurement or of one lucky draw; (d) provenance — is the counter under test the frozen one.

**Outcome:** C1=met, exit 0, no defect found.

---

## 1. Target command (verbatim output)

```
cd /home/vgpnk/Projects/shokunin/mori-shokunin && python3 .ufo/waves/round-37/count-c1.py e57c58b57c025364e79d130fbdf764d2674d83d6 --seed 41; echo EXIT=$?
```

Full output:

```
P-C1: at revision R, tools/mori-sources-appendonly.py prints exactly the counter's hidden truth for ids, deleted, superseded and round_changed, and exactly the truth's per-id `changed`/`deleted` lines, on each of 24 sandbox SOURCES.md histories drawn at run time, on the lane's own history (rev 6bd57097, round base f10a320d) where the independent oracle lists at least one id, and on one run-time-drawn challenge history presented in real-arm clothing (lane path, lane git identity, lane title); and the same counter rejects all three negative fixtures: a real-arm memoizer, a constant printer, and a summary-only printer.
tool: /tmp/mori-c1-tool-vd8sk3jn/mori-sources-appendonly.py
blind arm: 24/24 sandbox histories matched the hidden truth (2.8s; coverage: deletions=21 changed-back=14 superseded=12)
real arm: pass (0.5s)
  tool:   appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]
  oracle: appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]
  tool exit=1
challenge arm (real-arm clothing): pass (0.1s)
  truth:  appendonly_violations=4 ids=[S054,S116,S236] deleted=[S081] superseded=[S054] round_changed=[S081,S116,S236]
  tool:   appendonly_violations=4 ids=[S054,S116,S236] deleted=[S081] superseded=[S054] round_changed=[S081,S116,S236]
negative memo-n1.py     rejected (challenge: lists differ: want appendonly_violations=3 ids=[S179] deleted=[S066,S116] superseded=[S179] round_changed=[S066,S116] got appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193])
negative const.py       rejected (blind 4/4 (repo200: lists differ))
negative summary-only.py rejected (blind 4/4 (repo200: per-id lines differ (malformed=0)))
C1=met
seed=41
EXIT=0
```

Exit code: **0**. Verdict line: **`C1=met`**.

## 2. Axis (a) — verdict correctness

- blind arm 24/24 matched the counter's hidden truth, with the coverage counters
  `deletions=21 changed-back=14 superseded=12`, above the counter's own frozen floor
  (`delete >= 12`, `changed_back >= 12`, `supersede >= 1` — `count-c1.py:906-909`).
- real arm: the tool's four lists are byte-identical to the counter's independent git-walk
  oracle (`ids`/`deleted`/`superseded`/`round_changed` all equal; 18 violations, at least one id
  as the predicate requires).
- challenge arm: the tool matched the counter's op-log truth on a history wearing the lane path,
  the lane git identity (`mori-shokunin <mori@shokunin.local>`) and the lane SOURCES title —
  `deleted=[S081]` present, so the arm is not vacuous (the counter raises
  `challenge draw carried no deletion witness` otherwise, `count-c1.py:772-773`).

## 3. Axis (b) — discrimination (the three negatives)

Each negative was rejected, each by a different mechanism, so no single comparison is doing the
work:

| fixture | rejected by | evidence |
|---|---|---|
| `memo-n1.py` (real-arm memoizer) | challenge arm — it printed the published real-arm constant where the hidden challenge truth was expected | `lists differ: want …ids=[S179] deleted=[S066,S116]… got …ids=[S041,…,S193] deleted=[]…` |
| `const.py` (constant printer) | blind arm, 4/4 histories | `blind 4/4 (repo200: lists differ)` |
| `summary-only.py` (correct lists, no per-id `deleted` lines) | blind arm, 4/4 histories, on the **per-id** check | `blind 4/4 (repo200: per-id lines differ (malformed=0))` |

The memoizer is the one the r36 counter let through; here it is killed by the run-time-drawn
challenge history whose truth is never published, exactly as the frozen predicate requires. The
summary-only fixture is killed by the per-id line check, not by the summary comparison.

## 4. Axis (c) — seed sensitivity

Two additional seeds were run to confirm the verdict is a property of the measurement, not of
one draw:

```
$ python3 .ufo/waves/round-37/count-c1.py e57c58b… --seed 7   →  C1=met (exit 0)
$ python3 .ufo/waves/round-37/count-c1.py e57c58b… --seed 99  →  C1=met (exit 0)
```

Seed 7 shows the summary-only negative failing on 3 of 4 blind histories rather than 4 — the
per-arm failure count varies with the draw, but every negative is still rejected and the
verdict is stable. Re-running seed 41 reproduced byte-identical output (same challenge truth
`ids=[S054,S116,S236] deleted=[S081]`, same negative details), so the seed is a faithful replay
key.

## 5. Axis (d) — provenance of the counter under test

The counter exercised is the frozen one, not an edited local variant:

```
$ git rev-parse e57c58b57c025364e79d130fbdf764d2674d83d6:.ufo/waves/round-37/count-c1.py
7518fef8f54afff69ee38a99f2acbf518006f5ad
$ git hash-object .ufo/waves/round-37/count-c1.py
7518fef8f54afff69ee38a99f2acbf518006f5ad
$ sha256sum .ufo/waves/round-37/count-c1.py
86699627c7627cc3eea3ba9ea952079d081db390f9ba2be1e1d4d685dd98cdae
```

Both pins match `evidence/freeze-r37.txt` (blob `7518fef8…`, sha256 `86699627…`), and the
working-tree blob equals the blob at the scored tip (`git diff --stat 7518fef… -- …/count-c1.py`
is empty). The three negative fixtures likewise match their frozen pins (`19324701…`, `2f3993a…`,
`2d62f742…`) both in the working tree and at the scored tip. The tool under test is taken by the
counter from `git show <rev>:tools/mori-sources-appendonly.py`, and that file is unchanged between
the scored tip and HEAD (`git diff --stat e57c58b… HEAD -- tools/mori-sources-appendonly.py` is
empty). `git merge-base --is-ancestor e57c58b… HEAD` → exit 0, so the scored tip is on the lane's
history.

## 6. Hygiene observed

- The lane repo was not mutated by this seat: no `git add/commit/push/fetch/reset/stash`, no jj
  command, no lane file edited. `git status --porcelain` shows only untracked entries owned by
  other seats (`w1/*.md` reports, `.scratch/`, `scratch-rev/`). This seat's only write is this
  report.
- Scratch: the counter uses `tempfile.mkdtemp` per arm (`c1-`, `c1-neg-`, `challenge-`,
  `mori-c1-tool-`), so a replay of seed 41 cannot collide with a concurrent seat. After the run
  the lane's `.ufo/waves/round-37/scratch/` is empty (challenge dir removed in the `finally`,
  `count-c1.py:794`) and the `/fast/scratch/hyaku/mori-r37/` tree holds no `c1-*` directory from
  this run. The tool copy is removed in `main`'s `finally` as well.
- The counter prints the tool path as an absolute `/tmp/mori-c1-tool-…` path because it lies
  outside the repo; `display_path` (`count-c1.py:848-856`) relativizes only lane paths, so no
  operator absolute path is embedded in this report or in the counter's output.
- No tool was installed or upgraded by this seat; no pacman transaction was run.

## 7. Observation (not a defect, no action taken)

The real arm checks list equality and per-id line equality but not the tool's exit code, while the
blind arm (`count-c1.py:698-701`) and the challenge arm (`count-c1.py:783-785`) do compare the
exit status against the expected `1 if round_changed else 0`. In the measured run the real arm's
tool exit was 1 and the oracle's `round_changed=[S182,S193]` is non-empty, so the expected exit is
1 and the observed exit agrees — the missing check is latent, not exercised. The frozen predicate
P-C1 does not require an exit-code comparison on the real arm, so this is recorded as an
observation only; no change to the frozen counter is made here (a change to a predicate after
freeze would be a new counter version, per `contract.md`).

## 8. Risk / blocker notes

- None blocking. The counter's disclosed boundary (r36 debt f) is a 120 s tool budget with
  SIGTERM-then-SIGKILL after a 5 s grace, reported as `tool_timeout`; no arm in this run came near
  it (blind 2.8 s, real 0.5 s, challenge 0.1 s).
- The per-arm negative failure counts are draw-dependent (seed 7: summary-only failed 3/4 rather
  than 4/4); the pass/fail verdict was stable across seeds 7, 41 and 99.

VERDICT: PASS
