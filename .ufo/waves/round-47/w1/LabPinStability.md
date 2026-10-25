# LabPinStability — w1 report (round 47)

Seat: LabPinStability (leaf, detection/report only). Hypothesis: every self-test command bound by
mori-pin-check at `2d85e33d14198d388fd3cda9cc15ec07e57e7a53` prints the same tally on repeated runs.

## Verdict

**Supported — no flaky pin.** All measured runs print byte-identical full outputs, including all 26
per-pin `observed=` tally fields and all 5 digest pins. C1's tally set at the entering revision is
reproducible; nothing suggests irreproducibility of `PIN_CHECK=unmet` (the single mismatch at
`SKILL.md:912` is stable: pinned `pass=15 fail=0` vs observed `pass=22 fail=0` on every run).

## Method and evidence

Mandated command: `python3 tools/mori-pin-check.py --rev 2d85e33d14198d388fd3cda9cc15ec07e57e7a53
--min-tally-pins 26`, cwd = lane root `/home/vgpnk/Projects/shokunin/mori-shokunin`, `TMPDIR` =
`.scratch/r47-LabPinStability/`.

| run | instrument | exit | wall | stdout | stderr | result |
|---|---|---|---|---|---|---|
| run1 | working-tree `tools/mori-pin-check.py` (hash `e3ef425a…` at execution) | 1 | 70.69s | 5279 B | 0 B | `PIN_CHECK=unmet tally_pins=26 digest_pins=5 mismatches=1 unparsed=0 no_command=0 dropped=0` |
| run2 | working-tree tool (sibling-mutated mid-run, see Ambient finding) | 1 | 1.55s | 0 B | 915 B | crash: `NameError: name 'bound' is not defined` in `pin_commands` (traceback in run2.err) |
| f1 | frozen copy `git show 63eecf2:tools/mori-pin-check.py` (hash `e3ef425abde30974faf53a894f96650af11570d2125a5bf621395f6ab0d903e1`) + `--repo` | 1 | 70.12s | 5279 B | 0 B | same `PIN_CHECK=unmet …` line as run1 |
| f2 | same frozen copy | 1 | 69.90s | 5279 B | 0 B | identical output to f1 |
| f3 | same frozen copy | 1 | 70.63s | 5279 B | 0 B | identical output to f1 |

Diffs (on `observed=` fields extracted per tally pin, and on full outputs):
- `f1.observed.sorted` vs `f2.observed.sorted` — identical (26/26).
- `f1.observed.sorted` vs `f3.observed.sorted` — identical (26/26).
- `run1.observed.sorted` vs `f1.observed.sorted` — identical (26/26).
- Full-file `diff f1.out f2.out`, `diff f1.out f3.out`, `diff f1.out run1.out` — all empty
  (`ALL_FOUR_FULL_OUTPUTS_IDENTICAL`).

So three independent executions of the frozen instrument, plus the one successful working-tree execution,
agree on every bound tally. Exit 1 every run is the expected `PIN_CHECK=unmet` (contract "Before"
state, contract.md line 33: `unmet tally_pins=26 digest_pins=5 mismatches=1`).

## Ambient finding (workflow hazard, not a flaky pin)

Run2 crashed because a sibling wave seat transiently mutated the working-tree copy of
`tools/mori-pin-check.py` during the measurement window: at 16:43:57 the file was rewritten
(sha256 `104cf3dd…`, size 23218) with the `bound = []` initialization removed from
`pin_commands` (the loop then returns the undefined name). By 16:44 the file was restored to the
frozen bytes (`e3ef425a…`, `git status --porcelain -- tools/mori-pin-check.py` clean again). The
crash is therefore sibling churn, not selftest nondeterminism — but it confirms that the working-tree
instrument is not stable while mutation-tester seats are live. Recommendation for L1: measure C1 at
landing with the frozen instrument (`git show 63eecf2:tools/mori-pin-check.py` = `e3ef425a…`), as
the contract already provides for ("If the working-tree bytes ever differ, the claim is measured with
`git show <freeze>:<path>`").

## Scope notes

- No tool installs/updates performed (nothing needed; channel record N/A).
- No subagent/labrat spawned (leaf seat; evidence gathered directly).
- Read-only host/lane access throughout; no git mutation, no `sudo`, no tracefs access.
- Scratch artifacts under `.scratch/r47-LabPinStability/` (`run1.out`, `run2.err`, `f1..f3.out`,
  `*.observed.sorted`, `mori-pin-check-freeze.py`), kept for L1 inspection.

## Output/exit recap

- run1: exit 1, full output byte-identical to f1/f2/f3.
- run2: exit 1, stdout empty, stderr = NameError traceback (file mutated mid-wave — see above).
- f1/f2/f3: exit 1, `PIN_CHECK=unmet` with exactly the contract's entering-state numbers.
