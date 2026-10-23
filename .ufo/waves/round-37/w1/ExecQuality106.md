# ExecQuality106 — memoizer fixture-list omission

**Item attacked:** QUALITY 106 / C1: whether the `C1=met` verdict alone ensures the memoizer negative was exercised.

**Axes:** (1) mutation survives as a verdict; (2) receipt-level visibility; (3) freeze-pin provenance; (4) memoizer fixture's role in the no-challenge kill rule.

## Mutation

Scratch copy: `/fast/scratch/hyaku/mori-r37/ExecQuality106/count-c1-nomemo.py`.

Starting point was the frozen `count-c1.py` (SHA-256 `86699627c7627cc3eea3ba9ea952079d081db390f9ba2be1e1d4d685dd98cdae`). The single-line diff is also retained at `/fast/scratch/hyaku/mori-r37/ExecQuality106/diff-vs-frozen.txt`:

```diff
-    for name in ("memo-n1.py", "const.py", "summary-only.py"):
+    for name in ("const.py", "summary-only.py"):
```

No lane source file was edited. The counter's challenge arm used its prescribed temporary directory under the lane scratch path and cleaned it; that directory was empty after the run.

## Primary measurement

Command:

```text
cd /fast/scratch/hyaku/mori-r37/ExecQuality106 && timeout 900 python3 ./count-c1-nomemo.py e57c58b57c025364e79d130fbdf764d2674d83d6 --seed 106
```

Observed output (`run-nomemo.txt`):

```text
P-C1: at revision R, tools/mori-sources-appendonly.py prints exactly the counter's hidden truth for ids, deleted, superseded and round_changed, and exactly the truth's per-id `changed`/`deleted` lines, on each of 24 sandbox SOURCES.md histories drawn at run time, on the lane's own history (rev 6bd57097, round base f10a320d) where the independent oracle lists at least one id, and on one run-time-drawn challenge history presented in real-arm clothing (lane path, lane git identity, lane title); and the same counter rejects all three negative fixtures: a real-arm memoizer, a constant printer, and a summary-only printer.
tool: /tmp/mori-c1-tool-ev2nuv54/mori-sources-appendonly.py
blind arm: 24/24 sandbox histories matched the hidden truth (2.0s; coverage: deletions=22 changed-back=17 superseded=11)
real arm: pass (0.3s)
  tool:   appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]
  oracle: appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]
  tool exit=1
challenge arm (real-arm clothing): pass (0.1s)
  truth:  appendonly_violations=5 ids=[S024,S163,S228] deleted=[S217,S270] superseded=[S024,S163] round_changed=[S024,S217,S228,S270]
  tool:   appendonly_violations=5 ids=[S024,S163,S228] deleted=[S217,S270] superseded=[S024,S163] round_changed=[S024,S217,S228,S270]
negative const.py       rejected (blind 4/4 (repo200: lists differ))
negative summary-only.py rejected (blind 3/4 (repo200: per-id lines differ (malformed=0)))
C1=met
seed=106
EXIT=0
```

**Result:** removing the fixture entry is possible with a one-line edit; the copy still prints `C1=met`, exit 0. The output no longer contains `negative memo-n1.py rejected`. Thus the verdict line/exit code alone does not attest that this fixture was run. A receipt-level check that requires the exact rejection line would catch this omission.

## Corroborating measurements

Unmutated same-seed control command:

```text
cd /fast/scratch/hyaku/mori-r37/ExecQuality106 && timeout 900 python3 ./count-c1-pristine.py e57c58b57c025364e79d130fbdf764d2674d83d6 --seed 106
```

Observed: `negative memo-n1.py rejected (challenge: lists differ: want appendonly_violations=2 ids=[S059] deleted=[S206] superseded=[S059] round_changed=[S118,S206] got appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193])`; `C1=met`; `EXIT=0`. Full output is `/fast/scratch/hyaku/mori-r37/ExecQuality106/run-pristine-seed106.txt`.

Memoizer as the candidate tool, with the memoizer fixture omitted (challenge arm retained):

```text
cd /fast/scratch/hyaku/mori-r37/ExecQuality106 && timeout 900 python3 ./count-c1-nomemo.py e57c58b57c025364e79d130fbdf764d2674d83d6 --seed 106 --tool /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-37/fixtures/memo-n1.py
```

Observed: blind `24/24`; real arm pass; challenge arm `FAIL` with the memoizer's published lists differing from the run-time truth; the two remaining negatives were rejected; `C1=unmet`; `EXIT=1`. This shows that with the challenge arm intact, the memoizer fixture omission does not itself make the memoizer candidate pass.

No-challenge kill-rule control, using scratch-only copies with `challenge_ok` forced true both at top level and in `run_negative`:

```text
python3 ./count-c1-nochall.py e57c58b57c025364e79d130fbdf764d2674d83d6 --seed 106
```

Observed: `negative memo-n1.py ACCEPTED (all three arms pass)`; `C1=unmet`; `EXIT=1`.

```text
python3 ./count-c1-nochall-nomemo.py e57c58b57c025364e79d130fbdf764d2674d83d6 --seed 106
```

Observed: only `const.py` and `summary-only.py` negatives were rejected; `C1=met`; `EXIT=0`. Full outputs: `/fast/scratch/hyaku/mori-r37/ExecQuality106/run-nochall-withmemo.txt` and `run-nochall-nomemo.txt`. This confirms the memoizer fixture is load-bearing for the contract's kill rule against a counter with no functioning challenge arm.

## Provenance and scope

Commands and observed hashes:

```text
git hash-object /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-37/count-c1.py
→ 7518fef8f54afff69ee38a99f2acbf518006f5ad

git hash-object /fast/scratch/hyaku/mori-r37/ExecQuality106/count-c1-nomemo.py
→ bcb60958042411d55a0709da427d699d4d475b61

git rev-parse e57c58b57c025364e79d130fbdf764d2674d83d6:.ufo/waves/round-37/count-c1.py
→ 7518fef8f54afff69ee38a99f2acbf518006f5ad
```

The frozen counter matches `evidence/freeze-r37.txt`; the mutated scratch copy does not. The blob pin is a separate way to detect a changed counter. `count-c1.py`'s final predicate is `met = (passed == N_SANDBOX and real_ok and challenge_ok and all(rejected))` (line 949); there is no explicit fixture-count assertion. QUALITY 106 at `corpus/QUALITY.md:853-860` also says the receipt must show `negative memo-n1.py rejected`, so the missing line would fail that receipt-level requirement even though the copy prints `C1=met`.

No tools installed.

**VERDICT: PASS** — the requested copy prints `C1=met` with the memoizer fixture omitted. This verdict follows the assignment's acceptance rule; the receipt-line and frozen-blob checks are distinct caveats above.
