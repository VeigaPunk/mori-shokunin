# Mo82E03C3Pins — C3 bindings

## Scope and axes

Axes: operability, freshness, depth, coverage, calibration, adjacency. Detection/report only. No scalar score or whole-claim pass asserted.

Produced only:
- `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-82/record-pins.json`
- `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-82/evidence/c3-bindings-r82.txt`
- `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-82/w1/Mo82E03C3Pins.md`

Pins follow L1's directed replacement population in contract Pre-data amendment A1, not the original freeze table. Exactly three revision bindings; `bindings` is empty. SCORECARD and the sweep implementation were not edited.

## Measured independent evidence

Carrier revision: `20551e564da8bbb941c6a2ace7405192ceb74969`.

| row_contains | frozen SCORECARD line | key=value | target revision | matching lines | match rc |
|---|---:|---|---|---:|---:|
| row_tally=19 | 4049 | row_tally=19 | 075574c83eae044ff8570cbd02d594943a87ced3 | 1 | 0 |
| survivors=0 | 4050 | survivors=0 | 075574c83eae044ff8570cbd02d594943a87ced3 | 1 | 0 |
| wrong=0 fixtures=7 | 4118 | wrong=0 | 482dc48d49670de0f7645d0d8e87e18816145256 | 1 | 0 |

Each selector matches exactly one frozen table row. The receipt retains each complete row. Substituting `7ca17b11be694ad112fda21464b26321cab94ee0` independently yields zero matching lines and match rc 1 for each of those three tokens. The receipt-only D81-1 defeated shape, `pointers=240` at `075574c83eae044ff8570cbd02d594943a87ced3`, also yields zero, match rc 1. None of these deliberate negatives enters the pins file.

## Exact executed command families and output

All commands used read-only subprocesses in the Python Eval kernel, with this prefix:

`git -C /home/vgpnk/Projects/shokunin/mori-shokunin`

Executed argument vectors:
- `rev-parse 20551e56^{commit}` → `20551e564da8bbb941c6a2ace7405192ceb74969`
- `rev-parse 482dc48d^{commit}` → `482dc48d49670de0f7645d0d8e87e18816145256`
- `rev-parse 075574c8^{commit}` → `075574c83eae044ff8570cbd02d594943a87ced3`
- `rev-parse 142998f5^{commit}` → `142998f53fb3393838180b4eb60fb6045333c643`
- `rev-parse 44bc941a^{commit}` → `44bc941a0e3e9676fa33a882b43d6e9793cbf74d`
- `log --reverse --format=%H -- SCORECARD.md` → first line `7ca17b11be694ad112fda21464b26321cab94ee0`; remaining lines used only as historical discovery output, not retained evidence.
- `show <SHA>:SCORECARD.md` for each of the six full SHAs above → committed SCORECARD bytes, rc 0. Selected rows and derived counts are retained in `evidence/c3-bindings-r82.txt`.

Every git subprocess returned rc 0. Matching-line counts were computed directly from git stdout with `sum(token in line for line in blob.splitlines())`; match rc is 0 if nonzero, otherwise 1. This is equivalent to the requested grep counts for these literal tokens, but **no shell grep command was run**, because the overriding tool policy prohibits shell grep. The receipt states that distinction rather than claiming an unexecuted command. No mori tool was trusted or run for these measurements.

Earlier original-population checks were all positive: pointers=240 at 482dc48d, pass=26 at 142998f5, pass=19 at 142998f5 each counted 1. Wrong-revision exploration: pass=26 at 44bc941a counted 0, but pass=19 at 44bc941a counted 1; that last candidate was not a sensitive negative and was replaced with earliest SCORECARD revision, where pass=19 counted 0. These exploratory results are disclosed in the receipt and not represented as active bindings.

## Risks, defects and boundaries

- Initial contract read still showed only the original table. L1 subsequently appended A1 at contract lines 183–204; reread before producing pins. No authority conflict remains for this seat's implementation.
- Precision limitation, not a new out-of-scope repair: the frozen SCORECARD row at line 4118 names `075574c8` in its prose while A1 binds that row's `wrong=0` to `482dc48d`. The interface checks registered revision bytes, not agreement with every prose revision label. No other-seat implementation defect was established.
- Token occurrence can be coincidental; these checks do not prove measurement provenance or rerun a measurement command. The full claim awaits L1 integration.
- No build, test suite, formatter, selftest, counter, or landed sweep was run. L1 should run the tool selftest, real sweep with these pins, and round-82 C3 counter after integration. No LSP operation was needed: no source symbols were edited; no LSP tool is exposed in this seat.
- No scratch files/directories created; nothing to clean. No tools installed or updated. No git mutation, external-state remediation, credential read, or subagent dispatch.

## Self-evaluation

Accuracy 4/5: exact git-derived counts retained, but the requested shell grep was replaced with disclosed literal counting under tool policy. Completeness 4/5: A1 population and all negative checks delivered; integration deliberately belongs to L1. Clarity 4/5: supersession and preliminary nonsensitive control disclosed. Actionability 4/5: usable pins and named parent checks. Conciseness 4/5: original-population exploration adds length but preserves honest provenance. Overall 4.0/5; improvement: parent should retain the integrated sweep result, not infer it from these independent byte checks. The user should agree that this is binding evidence, not a whole-C3 verdict.
