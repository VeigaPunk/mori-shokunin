# W2 seat RevC4Before — C1 before-state reproduction at `e37dcc6`

Verdict: **PASS** — the before-state reproduces the receipt byte-for-byte and fails the counter exactly as required. No defect found in the counter or the receipt.

## 1. Reproduction (run, not read)

Command (run from lane root, this session):
`python3 .ufo/waves/round-38/count-c4.py e37dcc6`

My run's stdout (saved at `.ufo/waves/round-38/scratch/RevC4Before/before-run.out`) is **IDENTICAL** line-for-line to the receipt's core (10 lines; verified programmatically after stripping the receipt's wrapper `command:`/`EXIT=` lines, which the counter does not print). Exit code observed: **1**.

Full five check lines plus verdict, exactly as printed by my run:

```
check anchors          FAIL (anchors=0 missing=[])
check capability       FAIL (paths=['tools/mori-source-drift.py', '.ufo/waves/round-37/evidence/c2-after.txt', 'evidence/drift-live-r37.txt'] missing=['evidence/drift-live-r37.txt'])
check live_rows        PASS (named=10 summary_drifted=10 unknown=[])
check named_row_drift  PASS (exit=0 row_states=('PASS', ''))
check drift_kill       PASS (exit=1 row_states=('FAIL', "got=[('S101', 'fresh'), ('S102', 'excerpt'), ('S103', 'excerpt'), ('S104', 'unavailable'), ('S105', 'unavailable'), ('S106', 'no-copy'), ('S107', 'no-copy'), ('S108', 'fresh'), ('S109', 'unavailable'), ('S110', 'unavailable')] want=[('S101', 'fresh'), ('S102', 'excerpt'), ('S103', 'drifted'), ('S104', 'unavailable'), ('S105', 'unavailable'), ('S106', 'no-copy'), ('S107', 'no-copy'), ('S108', 'fresh'), ('S109', 'unavailable'), ('S110', 'unavailable')]"))
C4=unmet
EXIT=1
```

(The trailing `EXIT=1` line in the receipt is the wrapper's echo of the exit code, not counter output; my process exited 1.)

Before-state fails as it must: 3/5 checks PASS, but `anchors` and `capability` FAIL ⇒ `C4=unmet`, exit 1. It does not spuriously pass. All three fabricated witnesses are still `rejected` at the before-state.

## 2. The `check capability` line's path mix

`check_capability` (count-c4.py:169-174) takes the **last** `SCORECARD.md` row starting with `|` that contains `source-drift re-fetch probe` (`capability_row`, count-c4.py:153-158), extracts backtick-quoted path-like tokens (`paths_in`, count-c4.py:160-167; PATH_RE at count-c4.py:67), requires the list non-empty, and — in `main` (count-c4.py:245-250) — additionally requires every cited path to resolve at R **from the repository root** via `git cat-file -e R:path` (`resolves`, count-c4.py:139-143). The printed detail shows the cited paths plus the unresolvable subset.

At `e37dcc6` the capability row is SCORECARD.md line 2059 (verified from `git show e37dcc6:SCORECARD.md`, copy at scratch/RevC4Before/scorecard-e37dcc6.md). It cites, in backticks:

- `tools/mori-source-drift.py` — repo-root-relative, resolves at `e37dcc6`
- `.ufo/waves/round-37/evidence/c2-after.txt` — repo-root-relative, resolves at `e37dcc6`
- `evidence/drift-live-r37.txt` — **wave-relative, truncated** citation

The mix exists because the row's author wrote two citations as repo-relative paths but the third as a path relative to the wave directory `.ufo/waves/round-37/`. The real receipt lives at `.ufo/waves/round-37/evidence/drift-live-r37.txt`; repo-root `evidence/drift-live-r37.txt` never existed. Ground truth (`git cat-file -e`, this session):

| path | at `e37dcc6` | at `f725f30` |
|---|---|---|
| `evidence/drift-live-r37.txt` | ABSENT | ABSENT |
| `.ufo/waves/round-37/evidence/drift-live-r37.txt` | RESOLVES | RESOLVES |
| `.ufo/waves/round-37/evidence/c2-after.txt` | RESOLVES | RESOLVES |
| `corpus/knowledge/source-drift-content-anchor-r38.md` | ABSENT | RESOLVES |

So the check-line listing two `.ufo/waves/...` paths alongside one bare `evidence/...` path is a faithful dump of the row's inconsistent citation style, and `missing=['evidence/drift-live-r37.txt']` is that truncated citation failing root-relative resolution.

## 3. Is the missing-path trigger genuine? Yes — three independent confirmations

1. **Real dangling reference, not a regex artifact.** `paths_in` extracts backticks verbatim; `evidence/drift-live-r37.txt` appears verbatim in the row (line 2059 of the `e37dcc6` SCORECARD, grep-extracted). The blob it means exists — just under the full path — so the row genuinely cites an unresolvable path, violating the counter's documented contract ("cites only paths that resolve at <rev> from the repository root", count-c4.py docstring).
2. **The trigger is exactly what the scored tip fixes.** At `f725f30` the same row (line 2059 of `git show f725f30:SCORECARD.md`) cites `.ufo/waves/round-37/evidence/c2-after-v3.txt` and `.ufo/waves/round-37/evidence/drift-live-r37.txt` — all repo-relative — and SCORECARD lines 2175-2177 record the correction verbatim: "its two wave-directory paths became repo-relative." Running the counter at `f725f30` this session: `check capability PASS (missing=[])`, `check anchors PASS (anchors=3 missing=[])`, `C4=met`, exit 0. The two before-FAILs flip to PASS and nothing else changes — the trigger discriminates before from after on the claimed fix.
3. **The resolution test bites.** The `witness-dangling-row` negative (a row citing a nonexistent path) is `rejected` at `e37dcc6` — the same `resolves()` gate rejects fabricated dangling citations, so the check is not a formality that only fires here.

Side note on the other before-FAIL: `anchors=0 missing=[]` is the absent-entry case — `corpus/knowledge/source-drift-content-anchor-r38.md` is ABSENT at `e37dcc6`, so `anchors_from(None)` returns 0 < `MIN_ANCHORS=3` (count-c4.py:147-151). At the tip the entry resolves and anchors=3 PASS. Both before-FAILs are genuine pre-fix absence, not counter malfunction.

## 4. Findings by severity

- **Blocker/Major/Minor: none.** Reproduction exact; counter behavior matches its documented contract at both revisions; receipt honest.
- Informational: `check_capability`'s standalone predicate is only `bool(paths)`; the missing-path conjunction lives in `main` (`real_cap = real_cap_ok and not cap_missing`, count-c4.py:250). By design — the FAIL detail carries the missing list — noted so no future reader mistakes the check function for the full predicate. No action.
- Informational: `capability_row` picks the last `|`-row containing the key; the prose mention at SCORECARD line 2175 (tip) does not start with `|` and is not captured. No false-capture risk observed.

## 5. Residual risk and verification gaps

- I verified one canonical runtime lane (`/home/vgpnk/Projects/shokunin/mori-shokunin`, git backend, revs `e33bb561…`/`e37dcc6`/`f725f30…` all `git cat-file -t commit`) and one counter version (v1, count-c4.py). A different `--repo` or a rewritten counter is out of scope; counter immutability is not attested by this seat.
- The receipt wrapper's `EXIT=1`/`EXIT=0` lines are wrapper echoes; I confirmed the exit codes by process status, not by the wrapper, so the wrapper itself is unattested (immaterial to the claim).
- Tip-side claims (witness discrimination quality at `f725f30`, C2/C3 calibration) belong to sibling seats; I ran the tip only as the discriminating control above.

No tool installs or upgrades were performed (python3 and git sufficed; tooling directive record: none).
