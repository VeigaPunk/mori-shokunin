# Mo82S02Knowledge — scoped findings

## Behavior and touched surfaces

Produced only:
- `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/knowledge/record-revision-precision-r82.md`
- `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-82/w1/Mo82S02Knowledge.md` (this report).

Axes named: operability, freshness, depth, coverage, calibration, adjacency. No score change or passing round claim is asserted. Entry covers the defect class, four ordered message tokens/actions, original frozen population, separately attributed A1 replacement population, actual D81-1 absence observation and scope limits. Opening source is `S597 (pending Gate landing)`: two source-registry searches found no S597; no URL was invented. Gate registration remains another seat's responsibility.

## Findings and authority conflict

1. **Original binding 3 fails row-value by inspection.** Worktree `SCORECARD.md:4018` first table row containing `Control-receipt binding guard` has no `pass=19`; it describes 19/19 instead. `pass=19` occurs only in correction prose at `:4026`. At historical `142998f5`, the corresponding lines are 4016 and 4024. Thus historical token presence is not row-value conformity. In-flight `tools/mori-record-sweep.py:119-132` selects the first matching table row and applies `contains_value`; this inspection predicts `row-value`, not a measured gate result. No file was repaired by this seat.
2. **Population conflict, retained rather than judged.** The canonical assignment says “the real binding population (the three frozen bindings)” and “Round claims (frozen before this wave; do not change them).” The observed worktree contract appends `Pre-data amendment A1` after its original 179 lines; it says verbatim: `The "Real bindings" table's first row is replaced.` Its table supplies three replacement rows (`row_tally=19`, `survivors=0`, `wrong=0 fixtures=7`). L1 MoriR82 replied verbatim: “A1 is the authority; document A1's three bindings, not the superseded three.” Entry records both populations with attribution, marks originals historical/not green, and does not judge the contract amendment. A1 explains original binding 1's moving-pointer conflict with the r81 pinned arm; original binding 3 has the independent row-value defect above.
3. **D81-1 byte absence reproduced.** `075574c8:SCORECARD.md` has zero lines containing `pointers=240`. The historical graded count 237 is inherited reviewer evidence, not independently recounted here.
4. **In-flight state is not landed evidence.** Observed HEAD `08e13729b60382e121956c461f4ad0fd9194553a`; worktree modifications included the contract, SCORECARD, QUALITY and record-sweep tool, plus untracked C3 binding evidence. These were other seats' bytes and were not touched. A1's claimed pre-data timing was read, not independently established.

## Exact shell commands and observed outcomes

Commands below are copied from this seat's tool calls. Outputs are quoted or explicitly summarized; long file/diff content was read, not promoted to gate evidence. Every shell call used cwd `/home/vgpnk/Projects/shokunin`, timeout 60 seconds, non-interactive. No test, selftest, counter, census, clone, network fetch, install or mutating git/jj command was run.

### 1 — Historical counts (batch exit 1)

```sh
cd /home/vgpnk/Projects/shokunin/mori-shokunin && echo '--- 075574c8 pointers=240 count:' && git show 075574c8:SCORECARD.md | grep -c 'pointers=240'; echo '--- 482dc48d pointers=240 count:' && git show 482dc48d:SCORECARD.md | grep -c 'pointers=240'; echo '--- 142998f5 pass=26 count:' && git show 142998f5:SCORECARD.md | grep -c 'pass=26'; echo '--- 142998f5 pass=19 count:' && git show 142998f5:SCORECARD.md | grep -c 'pass=19'; echo '--- 142998f5 Control-receipt binding guard + pass=19 row:' && git show 142998f5:SCORECARD.md | grep 'Control-receipt binding guard' | grep -c 'pass=19'
```

```text
--- 075574c8 pointers=240 count:
0
--- 482dc48d pointers=240 count:
1
--- 142998f5 pass=26 count:
1
--- 142998f5 pass=19 count:
1
--- 142998f5 Control-receipt binding guard + pass=19 row:
0
```

`grep -c` prints 0 and exits 1 for no matches. Batch exit 1 is not a setup error or passing gate.

### 2 — Historical row locations (batch exit 0)

```sh
cd /home/vgpnk/Projects/shokunin/mori-shokunin && echo '=== 142998f5 Control-receipt binding guard ===' && git show 142998f5:SCORECARD.md | grep -n 'Control-receipt binding guard' | cut -c1-200; echo '=== 142998f5 pass=19 ===' && git show 142998f5:SCORECARD.md | grep -n 'pass=19' | cut -c1-200; echo '=== 142998f5 mori-record-sweep.py ===' && git show 142998f5:SCORECARD.md | grep -n 'mori-record-sweep.py' | cut -c1-200; echo '=== 142998f5 pass=26 ===' && git show 142998f5:SCORECARD.md | grep -n 'pass=26' | cut -c1-200; echo '=== 482dc48d pointers=240 line ===' && git show 482dc48d:SCORECARD.md | grep -n 'pointers=240' | cut -c1-160
```

Observed locations: Control-receipt row 4016; `pass=19` correction prose 4024; record-sweep capability row 4103 and prose 4129; `pass=26` row 4103; `pointers=240` row 4036 at `482dc48d`. Displayed row excerpts were deliberately truncated by `cut`; absence counts in command 1 consumed full bytes.

### 3 — Read-time state and current rows (batch exit 0)

```sh
cd /home/vgpnk/Projects/shokunin/mori-shokunin && echo 'HEAD:' && git rev-parse HEAD && echo 'status:' && git status --porcelain | head -5 && echo '=== 142998f5 line 4016 (binding-3 candidate row), tail 400 chars:' && git show 142998f5:SCORECARD.md | awk 'NR==4016' | tail -c 400 && echo && echo '=== worktree lines with Control-receipt binding guard:' && grep -n 'Control-receipt binding guard' SCORECARD.md | awk -F: '{print $1}' && echo '=== worktree: does any of those rows contain pass=19?' && grep 'Control-receipt binding guard' SCORECARD.md | grep -c 'pass=19'; echo '=== worktree: first table row containing mori-record-sweep.py, tail 300 chars:' && grep -n 'mori-record-sweep.py' SCORECARD.md | head -1 | cut -d: -f1 | xargs -I{} awk -v n={} 'NR==n' SCORECARD.md | tail -c 300; echo; echo '=== worktree: first row containing mori-claim-sweep.py contains pointers=240?' && grep 'mori-claim-sweep.py' SCORECARD.md | grep -c 'pointers=240'
```

Observed HEAD above. First five status lines:

```text
 M .ufo/waves/round-82/contract.md
 M SCORECARD.md
 M corpus/QUALITY.md
 M tools/mori-record-sweep.py
?? .ufo/waves/round-82/evidence/c3-bindings-r82.txt
```

This is a truncated status sample, not an exhaustive dirtiness claim. Control-receipt row location 4018; matching-row `pass=19` count 0. Historical row tail says `selftest 18/18 at the r79 wave freeze; the landed blob runs 19/19`. Record-sweep row tail contains `RECORD_SWEEP_SELFTEST pass=26 fail=0`. Claim-sweep matching-row `pointers=240` count 1.

### 4 — Current row locations (batch exit 0)

```sh
cd /home/vgpnk/Projects/shokunin/mori-shokunin && for pat in 'mori-claim-sweep.py' 'mori-record-sweep.py' 'Control-receipt binding guard'; do echo "=== first line number containing '$pat':"; grep -n "$pat" SCORECARD.md | head -1 | cut -d: -f1; done; echo '=== global pass=19 occurrences in worktree SCORECARD:'; grep -n 'pass=19' SCORECARD.md | cut -c1-120; echo '=== 482dc48d row 4036 tail (binding-1 rev-bytes row):'; git show 482dc48d:SCORECARD.md | awk 'NR==4036' | tail -c 260
```

Observed first locations 4038, 4105, 4018 respectively. Only global `pass=19` match displayed: `4026:\`CONTROL_RECEIPT_SELFTEST pass=19 fail=0\`, rc 0. Only that row's in-memory tally`. Historical row tail cites the claim-sweep invocation and r81 pinned arm; this was a text read, not their execution.

### 5 — Other seats' in-flight diffs (batch exit 0)

```sh
cd /home/vgpnk/Projects/shokunin/mori-shokunin && echo '=== diff stat vs HEAD:' && git diff --stat -- SCORECARD.md .ufo/waves/round-82/contract.md && echo '=== SCORECARD diff hunks (first 80 lines):' && git diff -- SCORECARD.md | head -80 && echo '=== contract diff (first 60 lines):' && git diff -- .ufo/waves/round-82/contract.md | head -60
```

```text
 .ufo/waves/round-82/contract.md | 23 +++++++++++++++++++++++
 SCORECARD.md                    |  6 ++++--
 2 files changed, 27 insertions(+), 2 deletions(-)
```

Displayed SCORECARD diff retires the r10 pin and updates freshness; displayed contract diff appends A1 and its three-row replacement table. Neither is this seat's change or evidence of measured C2/C3 success.

### 6 — Scoped scratch lifecycle (exit 0)

```sh
S=/fast/scratch/hyaku/mori-r82/Mo82S02Knowledge; mkdir -p -- "$S" && trap 'rm -rf -- "$S"' EXIT && printf '%s\n' 'Scoped scratch created; EXIT trap removes it; no fixtures or gate executions.'
```

```text
Scoped scratch created; EXIT trap removes it; no fixtures or gate executions.
```

The shell completed normally with the EXIT cleanup trap. No scratch artifacts are cited as evidence; no `/tmp` write occurred.

## Tool-read provenance and gates

Read `skill://godspeed` and `skill://agent-self-evaluation`; contract and controls first, then required SCORECARD axes/retired/capabilities/r80/r81/planned sections, SKILL registry, PROVINCE inventory, QUALITY last criteria, corpus README Frontier, and both r81 lessons. Read sibling r80/r81 knowledge entries for existing style. Specialized source searches found S596 as the last row and no S597; tool reads, glob listing and searches did not execute gates. Read revision core at `tools/mori-record-sweep.py:28-150`; semantics and diagnostics in the entry derive from those in-flight bytes and the frozen interface.

The inherited entering control is `C3=unmet tool=present arm=absent`, rc 1 at `ebcf2c72`; it was read in `evidence/controls-r82.txt`, not rerun. No C1/C2/C3 after-value is claimed. No selftests, standing batteries, source census, final-tip binding sweep or publication checks were executed. Integration owner should run the final C3 counter and record sweep at the named committed revision and reconcile source registration/population authority. No tool installed or updated; no PATH directory changed.

## Out of scope and self-evaluation

No product code, judge, source registry, SCORECARD, LOG, SKILL, PROVINCE, host, service, credential, orchestration or foreign lane edits; no dispatch, commit, push, deploy or alternate runtime. Source Gate, amendment adjudication and final integration verification remain outside this seat's execution evidence.

Self-evaluation (not a gate): accuracy 4/5 (historical 237 inherited, not recounted); completeness 4/5 (S597 landing and authority adjudication intentionally external); clarity 4/5 (both populations necessarily retained to expose conflict); actionability 4/5 (diagnostic actions and exact observations present; final committed run unexecuted); conciseness 3/5 (exact command inventory is long). Average 3.8/5. Highest-impact actions belong to integration: resolve population authority explicitly, land S597, and retain actual final C3 execution receipt. Would the user agree: the entry meets the scoped content request without presenting unrun gates as passing; these limits remain explicit.
