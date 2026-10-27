# Mo58Critic30 — C1 pointer-resolution attack

## Counterexample

The frozen counter false-greens missing/malformed evidence pointers that do not begin exactly with `.ufo/`, `tools/`, or `corpus/`. In `count-c1.py:90-98`, the backtick regex extracts the row tokens, then `cat-file -e` is called only after the prefix test. A fixture with otherwise conformant active-register rows and the first row evidence set to `scripts/no-such.sh` produced:

```
C1=met rows=2 pointers=ok manifest=ok binding=ok failed=none rev=9b47cf4cec384b38ee784c0b86ad17e14e3a4093
```

The file was absent from that fixture's measured commit. The same result occurred for `no-such.py` (root path), `./tools/no-such.py`, and `/definitely/not/here.py`. Thus the broad §9 control (“a fixture register whose two rows name a nonexistent evidence path MUST score ... failed=pointers”) is not enforced for these forms; nor does the counter resolve every evidence pointer claimed by C1. The empty-evidence fixture also scored met: both evidence cells contained `none` and had no pointer tokens.

## Bounded method and observed controls

Imported and ran the byte-identical frozen `count-c1.py` (`sha256 6ecdb627bb55522c258dc484ed5c530cfd6f7c57c6a89b4c38179df4c0f84e4b`) against isolated throwaway git fixtures; counter bytes were not changed. Fixture repos were created only under `/fast/scratch/hyaku/mori-r58/Mo58Critic30/fixtures/`, with `git -C <fixture>` for git commands. Each fixture used the counter's active-register preamble, >=10 keyed rows, and a local manifest fixture.

| Fixture evidence pointer | Observed verdict |
|---|---|
| valid `tools/mori-vote-bind.py` | met, pointers=ok |
| missing `tools/no-such.py` | unmet, pointers=bad, failed=pointers |
| missing `scripts/no-such.sh` | **met, pointers=ok** |
| missing root `no-such.py` | **met, pointers=ok** |
| missing `./tools/no-such.py` | **met, pointers=ok** |
| absolute `/definitely/not/here.py` | **met, pointers=ok** |
| existing directory `tools/` | met, pointers=ok (directory object accepted as evidence) |
| `tools//mori-vote-bind.py` | unmet, pointers=bad |
| `tools/../tools/mori-vote-bind.py` | unmet, pointers=bad |
| `tools/../../etc/passwd` | unmet, pointers=bad |
| missing `tools/no-such-dir/` | unmet, pointers=bad |
| `tools/later-only.py`, committed only after measured revision | unmet, pointers=bad |
| `README.md` | **met, pointers=ok** |
| no pointer in either evidence cell | **met, pointers=ok** |

The baseline under-prefix missing path and wrong-tree path fail as intended. The freeze-revision measure itself returned met (and the measured counter bytes match freeze); this attack does not show the actual frozen rows fail pointer resolution, only that the predicate admits false-green fixtures outside its prefix filter / with no evidence pointer.

## Impacted axes

C1 calibration: pointer-resolution predicate and its §9 negative control. The weakness is in the frozen counter/predicate coverage, not evidence that the two current frozen rows are invalid. No C2 finding.

## Smallest safe correction

Extract and validate the evidence-column pointers specifically, rather than treating only three hard-coded prefixes as paths. Require at least one evidence pointer per claimed row; reject absolute, `./`, traversal, malformed, and unsupported path forms; then run `git cat-file -e R:<normalized repo-relative path>` for every accepted pointer and fail closed on any parse/lookup error. Extend the frozen control fixtures to include a missing path outside the existing prefixes, an absolute path, a root-level path, and an empty evidence cell.

## Other observed output

At freeze revision `fe8801120a67c1a6b8899d7d0423839caa09e7d0` and current lane HEAD `4272736cfc5147586e1543413772f80daf44b04b`, the command printed `... binding=ok failed=none rev=...`; it did not include `selftest=ok` in the measure line. Selftest is a separate command. This is outside my pointer attack scope.
