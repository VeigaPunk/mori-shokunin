# MutRoutedD3D5 — mutation probe of `tools/mori-routed-r24.py` items D3 and D5 (round 25, wave 2)

## Verdict

**HELD.** C1's D3 and D5 predicates are behaviourally load-bearing: seven of the eight mutants I
built were **killed** — each one flips the tool's own verdict on a sandbox commit that the pristine
tool rejects. The single **survivor** (M7) is an *equivalent* mutant: it changes no verdict on any
input, because the pinned base file's whole text parses to exactly the same pinned score table as the
`1499-1506` window. No survivor weakens the claim. Two contract-scope coverage notes (D5 ignores the
Evidence-pointer cell and ignores axes outside the six named ones) are recorded below; the contract's
D5 wording does not ask for either, so neither is a defect in C1.

Nothing in the lane was mutated: this seat wrote only this report file. The lane tool bytes are
unchanged (`sha256 cf5ef5815f1118ae3595171edde7f527176fde03480665eb6bbb46921c2969ef` before and after
the probe), and the clone's tool bytes are identical to the lane's.

## Where the work ran

| Item | Value |
|---|---|
| Private clone | `/fast/scratch/hyaku/mori-r25/w2-MutRoutedD3D5` (`git clone --no-hardlinks` of the lane); removed after the run, artefacts kept in `/fast/scratch/hyaku/mori-r25/MutRoutedD3D5-artifacts/` |
| Tool under test | `tools/mori-routed-r24.py`, `sha256 cf5ef5815f1118ae3595171edde7f527176fde03480665eb6bbb46921c2969ef` |
| Lane tip measured | `51dc8209774399cbf8664a701b256f1edc4c6237` (the lane moved from `07a31ae` while I worked; the tool file did not change — `git diff 07a31ae 51dc820 -- tools/mori-routed-r24.py` is empty) |
| Sandbox base | `07a31ae8e22514bbc603afa13f2de7c8b2424cca` (identical lesson and `## Axes` table to `51dc820`: `git diff 07a31ae 51dc820 -- corpus/lessons/round-24.md` is empty, and the `## Axes` table is byte-identical) |
| Detector | the tool itself: `python3 -I -B tools/mori-routed-r24.py --repo <clone> --rev <sandbox sha>`; a mutant is **killed** when its JSON verdict (status / held / mismatches / per-item reasons / exit code) differs from the pristine run on the same input, **survived** when every input is identical |
| Logs (scratch, not the lane) | `/fast/scratch/hyaku/mori-r25/MutRoutedD3D5-artifacts/` — `mutation-run.log`, `mutation-results.json`, `sandbox-build.log`, `mutate.py`, `make_sandbox.sh`, `pristine-tool.py` |

Baseline re-check of the claim's after-value at the current lane tip, with the tool bytes above:

```
$ python3 -I -B tools/mori-routed-r24.py --repo . --rev 51dc8209774399cbf8664a701b256f1edc4c6237
held  held 4  mism 0   (D1 D2 D3 D5 held, D4 hygiene held, exit 0)
```

## Sandbox commits (built in the private clone; each changes exactly one thing; the three green rows are the unmodified control revisions — `07a31ae` from the clone and `51dc820` fetched from the lane)

| Input | Commit | Change | Pristine verdict |
|---|---|---|---|
| green-base | `07a31ae` | none (control) | held, mismatches 0, exit 0 |
| green-head | `07a31ae` (HEAD) | none (control) | held, mismatches 0, exit 0 |
| green-lanetip | `51dc820` | none (control, current lane tip) | held, mismatches 0, exit 0 |
| d3-revert | `a29e6c4` | the round-25 D3 correction block removed from `corpus/lessons/round-24.md` (the routed defect itself) | red, D3 `no_line_with_correction_s07_and_pass_marker` |
| d3-digit | `7924eba` | the correction line's two `PASS 7/7` become `PASS 7/77` (marker followed by a digit) | red, D3 `no_line_with_correction_s07_and_pass_marker` |
| d3-oldhex | `01c22f5` | both hex tokens on the line now name `a536b18`, a commit where the case file holds 6 cases, not 7 | red, D3 `no_hex_token_naming_a_commit_with_n_cases` |
| d3-nohex | `3c9f3d5` | the hex token names no commit (`deadbeef…`) | red, D3 `no_hex_token_naming_a_commit_with_n_cases` |
| d5-revert | `21e6897` | the `## Axes` table back to its round-1 scores (coverage 5, operability 6, depth 4, all `round 1`) | red, D5 `axis_score_mismatch: coverage 5!=6`, `operability 6!=7`, `depth 4!=5` |
| d5-score | `1e071f8` | coverage scored 7 instead of 6 | red, D5 `axis_score_mismatch: coverage 7!=6` |
| d5-dupe | `cbaf12a` | the coverage axis row is listed twice | red, D5 `axis_row_duplicated: coverage` |
| d5-stale | `b93ed16` | the coverage row keeps `round 1` in Last change while its score (6) differs from its round-1 value (5) | red, D5 `axis_stale_round_1: coverage` |

Every pristine baseline matched the expected verdict (`expectation_ok` is true for all 11 inputs in
`mutation-results.json`), so no baseline failure was used to call a mutant killed.

## Mutants, one at a time

Each mutant was written into `tools/mori-routed-r24.py` in the clone, run against all 11 inputs, and
then the pristine bytes were restored and re-hashed. `restored_sha256 == pristine_sha256` for all
eight mutants and after the last run.

| Mutant | Site | Edit | Mutant sha256 | Verdict | Killed by |
|---|---|---|---|---|---|
| M1 | `tools/mori-routed-r24.py:820-821` | D3: delete `if not usable: reasons.append("no_hex_token_naming_a_commit_with_n_cases")` (the commit-has-n-cases check) | `81c142c0…3271` | **killed** | d3-oldhex, d3-nohex |
| M2 | `tools/mori-routed-r24.py:774` | D3: `marker_re = re.compile(re.escape(marker) + r"(?![0-9])")` → `re.compile(re.escape(marker))` (digit lookahead dropped) | `075253f9…4f0c` | **killed** | d3-digit |
| M3 | `tools/mori-routed-r24.py:736-738` | D5: delete the `if score != expected:` block (per-axis comparison against the pinned score) | `e414c81c…23b7f` | **killed** | d5-revert, d5-score |
| M4 | `tools/mori-routed-r24.py:727-729` | D5: delete the `if len(entries) > 1:` block (duplicate-row guard) | `fb94434b…d19` | **killed** | d5-dupe |
| M5 | `tools/mori-routed-r24.py:739-741` | D5: delete the `round 1` last-change guard | `327d1a14…9fa9b` | **killed** | d5-stale |
| M6 | `tools/mori-routed-r24.py:702-705` | D5: the pinned-revision parse is replaced by the hardcoded `D5_ROUND1_SCORES` table | `76c36af8…abba` | **killed** | all 11 inputs |
| M7 | `tools/mori-routed-r24.py:678` | D5: the parse drops the `1499-1506` line window and reads the whole pinned base file | `21fe8a7d…7d04` | **survived** | — (equivalent mutant, see below) |
| M8 | `tools/mori-routed-r24.py:698` | D5: the pinned base revision is read from REV instead of the pinned `28b79d3d` | `ae258ce4…ed1e7` | **killed** | all 11 inputs |

### Verdict changes (pristine → mutant), verbatim fields

M1 on `d3-oldhex` (and `d3-nohex`):
```
pristine: status failed  held 3  mismatches 1  D3 reasons ['no_hex_token_naming_a_commit_with_n_cases']  exit 1
mutant  : status held    held 4  mismatches 0  D3 reasons []                                           exit 0
```
M2 on `d3-digit`:
```
pristine: status failed  held 3  mismatches 1  D3 reasons ['no_line_with_correction_s07_and_pass_marker']  exit 1
mutant  : status held    held 4  mismatches 0  D3 reasons []                                           exit 0
```
M3 on `d5-score` (and `d5-revert`):
```
pristine: status failed  held 3  mismatches 1  D5 reasons ['axis_score_mismatch: coverage 7!=6']  exit 1
mutant  : status held    held 4  mismatches 0  D5 reasons []                                          exit 0
```
M4 on `d5-dupe`:
```
pristine: status failed  held 3  mismatches 1  D5 reasons ['axis_row_duplicated: coverage']  exit 1
mutant  : status held    held 4  mismatches 0  D5 reasons []                                   exit 0
```
M5 on `d5-stale`:
```
pristine: status failed  held 3  mismatches 1  D5 reasons ['axis_stale_round_1: coverage']  exit 1
mutant  : status held    held 4  mismatches 0  D5 reasons []                                exit 0
```
M6 on `green-lanetip` (the claim's own after-value):
```
pristine: status held    held 4  mismatches 0  D5 reasons []                                                  exit 0
mutant  : status failed  held 3  mismatches 1  D5 reasons ['axis_score_mismatch: coverage 6!=5', 'axis_score_mismatch: operability 7!=6', 'axis_score_mismatch: depth 5!=4']  exit 1
```
M8 on `green-lanetip`:
```
pristine: status held    held 4  mismatches 0  D5 reasons []                       exit 0
mutant  : status failed  held 3  mismatches 1  D5 reasons ['pinned_scores_unparseable']  exit 1
```

M6 is the sharpest one for C1: if the tool parsed the pinned scores wrongly and fell back on the
hardcoded round-1 table, it would reject the lane's own corrected `## Axes` table — the very table
D5 exists to police. The mutant is caught by the claim's own after-value command.

## Findings

**F1 — survivor M7 (severity: informational, coverage note; no change to the contract).**
`_parse_pinned_scores` reads `SCORECARD.md` lines 1499–1506 at `28b79d3d`; M7 makes it read the whole
file. Both produce the same pinned table today:
```
window parse today:      {'calibration': 5, 'coverage': 6, 'operability': 7, 'depth': 5, 'freshness': 5, 'adjacency': 6}
whole-file parse today:  {'operability': 7, 'coverage': 6, 'depth': 5, 'freshness': 5, 'calibration': 5, 'adjacency': 6}
```
So the line window is currently redundant for the pinned base file and M7 is equivalent, not a hole in
the check. The input that would kill M7: a pinned base `SCORECARD.md` that carries an axis/score pair
*outside* lines 1499–1506 conflicting with the window's value — then the whole-file parse returns
`None` and the tool reports `pinned_scores_unparseable` on every revision. Demonstrated on a synthetic
base text:
```
window parse with the extra line: {'calibration': 5, 'coverage': 6, 'operability': 7, 'depth': 5, 'freshness': 5, 'adjacency': 6}
whole-file parse with the extra line -> conflict: True
```
Because `SCORECARD_BASE_REV` is pinned to `28b79d3d` and that commit cannot change, no input inside the
current contract can kill M7 — it is untestable, not undetected. Smallest fix if the lane wants the
window to be load-bearing: none is required for C1; the cheapest hardening is a comment at
`tools/mori-routed-r24.py:678` saying the window is the load-bearing pin and why, so a later edit that
widens it is not an accident.

**F2 — D5 does not read the Evidence-pointer cell (severity: informational, contract scope).**
Probe `sbx-probe-pointer` (`b9440d9`): the coverage row's evidence pointer is replaced with a
citation to a line that does not exist; the score is unchanged. Pristine verdict: `held`, mismatches 0,
exit 0. This matches the contract's D5 wording (it constrains "each row's Score" and the Last change),
and the lane's own wave-2 note in `SCORECARD.md` at `51dc820` ("Round-25 corrections from wave 2
(CriticC1Admission)") says "D5 checks scores only, not evidence pointers or Last change text".
Smallest fix if the lane later wants it: one extra comparison of the pointer cell
against the closure citation inside `_check_d5` (the pointer cell is already parsed as `cells[2]`).

**F3 — D5 ignores rows for axes outside the six named ones (severity: informational, contract scope).**
Probe `sbx-probe-extraaxis` (`959139f`): a seventh row `| safety | 4 | … | round 1 |` is added inside
the `## Axes` section. Pristine verdict: `held`, mismatches 0, exit 0 — `_check_d5` iterates
`D5_AXES` only. The contract says "exactly one row per axis (coverage, operability, depth, freshness,
calibration, adjacency)", which does not forbid extra axes. Smallest fix if the lane wants it: compare
`set(seen)` with `set(D5_AXES)` and report `axis_row_unknown` for any extra row.

No finding in this probe contradicts C1's declared after-value.

## Restoration evidence

```
pristine sha256 (before the probe)  cf5ef5815f1118ae3595171edde7f527176fde03480665eb6bbb46921c2969ef
restored sha256 after every mutant  cf5ef5815f1118ae3595171edde7f527176fde03480665eb6bbb46921c2969ef  (identical, all 8 mutants)
lane tools/mori-routed-r24.py      cf5ef5815f1118ae3595171edde7f527176fde03480665eb6bbb46921c2969ef  (identical to the clone)
```
Exact text of the last line: `cf5ef5815f1118ae3595171edde7f527176fde03480665eb6bbb46921c2969ef` for the
pristine file, and the same value for `restored_sha256` of all eight mutants in
`mutation-results.json`. The lane working copy is unchanged (`git status --porcelain` in the lane
lists only other seats' untracked report files and `.scratch/`).

## Tooling

No tool was installed or upgraded for this probe: the work needed only `python3` (standard library),
`git` and `bash`, all already present. No `pacman`, `uv tool`, `cargo` or `npm` transaction was run.

## Reproduce

The clone was removed after the run (lane bound: remove large extracts); the two scripts and the raw
logs are kept in `/fast/scratch/hyaku/mori-r25/MutRoutedD3D5-artifacts/`. Re-running from scratch:

```
git clone --no-hardlinks /home/vgpnk/Projects/shokunin/mori-shokunin /fast/scratch/hyaku/mori-r25/w2-MutRoutedD3D5
cd /fast/scratch/hyaku/mori-r25/w2-MutRoutedD3D5
cp /fast/scratch/hyaku/mori-r25/MutRoutedD3D5-artifacts/{mutate.py,make_sandbox.sh} .
bash make_sandbox.sh      # builds the sandbox commits listed above
python3 -I -B mutate.py   # pristine baseline, 8 mutants, restore, mutation-results.json
```
The sandbox commit SHAs quoted in this report are the ones this run produced; a re-run reproduces the
same file contents (the commit SHAs differ because commit timestamps differ).
