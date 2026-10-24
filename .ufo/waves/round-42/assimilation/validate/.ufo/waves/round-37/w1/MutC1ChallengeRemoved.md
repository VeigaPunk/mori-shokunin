# MutC1ChallengeRemoved — is the C1 challenge arm load-bearing?

Scratch: `/fast/scratch/hyaku/mori-r37/MutC1ChallengeRemoved/`
Lane repo read-only throughout; all mutation ran on copies. No tools installed; no pacman.

## Assignment

Mutate `count-c1.py` so `challenge_arm` returns `(True, ...)` without running the tool, then run the
same counter on the honest tool and on `fixtures/memo-n1.py`. PASS iff the challenge arm is what
rejects the memoizer, i.e. the mutation flips `memo-n1.py` to ACCEPTED while the honest tool's arms
still pass.

## Mutation

`challenge_arm` is the only place a real-arm-clothed, run-time-drawn history is judged
(`counter:754-791`). Smallest behavior-bearing point: an unconditional early return at the top of the
body, before `os.makedirs`/`mkdtemp`/`run_tool`.

```diff
--- count-c1.pristine.py
+++ count-c1.mutant.py
@@ -759,6 +759,8 @@
     fooled; its truth comes from this counter's op log, so the published real-arm
     constant is not an answer to it."""
+    return True, None, {"violations": 0, "ids": [], "deleted": [],
+                        "superseded": [], "round_changed": []}, ""
     os.makedirs(CHALLENGE_PARENT, exist_ok=True)
     root = tempfile.mkdtemp(prefix="challenge-", dir=CHALLENGE_PARENT)
```

Hashes:

```
baseline/pristine 86699627c7627cc3eea3ba9ea952079d081db390f9ba2be1e1d4d685dd98cdae  count-c1.pristine.py
mutant            59019ee57f270e90650e8a5b9bb31f816d1eef8fdf43d6c4c725ba1219f716b4  count-c1.mutant.py
lane original     86699627c7627cc3eea3ba9ea952079d081db390f9ba2be1e1d4d685dd98cdae  .ufo/waves/round-37/count-c1.py
```

## Detector (identical on pristine, mutant, restored bytes)

```
python3 "<copy>/count-c1.py" e57c58b57c025364e79d130fbdf764d2674d83d6 \
  --repo /home/vgpnk/Projects/shokunin/mori-shokunin --seed 37037 \
  --tool /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-sources-appendonly.py
```

Fixed seed keeps the challenge draw constant across the three runs. The honest tool is passed
explicitly so the arms and the three negative fixtures are judged in one bounded run.

### Pristine — baseline

```
EXIT=0
blind arm: 24/24 sandbox histories matched the hidden truth (3.9s; coverage: deletions=21 changed-back=16 superseded=12)
real arm: pass (0.3s)
challenge arm (real-arm clothing): pass (0.1s)
  truth:  appendonly_violations=3 ids=[S083] deleted=[S012,S063] superseded=[S083] round_changed=[]
  tool:   appendonly_violations=3 ids=[S083] deleted=[S012,S063] superseded=[S083] round_changed=[]
negative memo-n1.py     rejected (challenge: lists differ: want appendonly_violations=3 ids=[S144] deleted=[S017,S040] superseded=[S144] round_changed=[S017,S040] got appendonly_violations=18 ids=[...] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193])
negative const.py       rejected (blind 4/4 (repo200: lists differ))
negative summary-only.py rejected (blind 4/4 (repo200: per-id lines differ (malformed=0)))
C1=met
seed=37037
```

`memo-n1.py` is rejected **by the challenge arm** — its real arm passes (published constant), its
blind arm passes (sandbox identity delegates to the honest tool).

### Mutant — challenge arm returns True without running the tool

```
EXIT=1
blind arm: 24/24 sandbox histories matched the hidden truth (2.2s; coverage: deletions=21 changed-back=16 superseded=12)
real arm: pass (0.3s)
challenge arm (real-arm clothing): pass (0.0s)
  truth:  appendonly_violations=0 ids=[] deleted=[] superseded=[] round_changed=[]
  tool:   (no summary line)
negative memo-n1.py     ACCEPTED (all three arms pass)
negative const.py       rejected (blind 4/4 (repo200: lists differ))
negative summary-only.py rejected (blind 4/4 (repo200: per-id lines differ (malformed=0)))
C1=unmet
seed=37037
```

Honest-tool verdict under the mutant: blind 24/24, real arm pass, challenge arm pass — the honest
tool still passes every arm (its honest output is what the pristine run shows; the mutation does not
touch it). Overall `C1` reads `unmet` only because `memo-n1.py` flipped to ACCEPTED, which is the
expected signature of the challenge arm being the sole discriminator, not an honest-tool regression.

Memoizer verdict flip: `rejected → ACCEPTED`, detail `challenge: lists differ …` → `all three arms
pass`. `const.py` and `summary-only.py` stay rejected (blind arm), so the mutation is surgical: only
the challenge arm's witness disappeared.

### Direct no-tool proof

`challenge_arm` was called in-process with `run_tool` and `build_sandbox` stubbed to raise:

```
=== pristine module ===
EXCEPTION challenge_arm invoked the tool/build_sandbox (tool/build invoked 1 time(s))
=== mutant module ===
RETURN ok=True got=None truth={'violations': 0, 'ids': [], 'deleted': [], 'superseded': [], 'round_changed': []} reason='' side_effect_calls=0
ACCEPTED_WITHOUT_TOOL_RUN=True
```

Pristine always enters the tool path; the mutant returns `(True, …)` with zero subprocess/build side
effects (mutant challenge elapsed 0.0s, no `challenge-*` dir under `.ufo/waves/round-37/scratch` —
`ls -la` shows the directory empty).

## Restoration evidence

```
cp count-c1.pristine.py count-c1.mutant.py
sha256sum count-c1.pristine.py count-c1.mutant.py .ufo/waves/round-37/count-c1.py
86699627…98cdae  count-c1.pristine.py
86699627…98cdae  count-c1.mutant.py
86699627…98cdae  .ufo/waves/round-37/count-c1.py
cmp count-c1.mutant.py .ufo/waves/round-37/count-c1.py  → RESTORED_BYTES_IDENTICAL
```

Restored-bytes rerun (same seed): challenge arm pass, `memo-n1.py rejected (challenge: lists differ…)`,
`const.py rejected`, `summary-only.py rejected`, `C1=met`, `EXIT=0` — baseline reproduced exactly.

Lane file checks after the probe: `git -C lane status --porcelain -- .ufo/waves/round-37/count-c1.py
.ufo/waves/round-37/fixtures tools/mori-sources-appendonly.py` → empty (rc=0);
`.ufo/waves/round-37/scratch/` empty. Lane `count-c1.py` hash unchanged.

Observation, not a defect: `git -C lane rev-parse HEAD` = `0a05f7e6765b025c321bc0b71bb1f44e2600d591`
(jj-colocated working-copy commit), while the counter explicitly resolves the scored tip
`e57c58b5…`, so all measurements are against the scored bytes.

## Verdict

- `fixtures/memo-n1.py`: **ACCEPTED** under the mutant (was rejected) — the challenge arm is
  load-bearing; removing it silently admits a real-arm memoizer.
- Honest tool: all three arms still pass; the gate's rejection of the memoizer is the only thing lost.
- Restoration: exact bytes, hash-verified, baseline reproduced.

Attacks: claim C1 "the same counter rejects a real-arm memoizer" / the challenge arm's necessity.

VERDICT: PASS
