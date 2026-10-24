# MutC3Manifest — mutation probe: C3 manifest path swap

role: mutation-tester (leaf, no dispatch)
target: `corpus/knowledge/inheritance-d72ac16-r42.md` graded by `.ufo/waves/round-42/count-c3.py`
lane tip at probe: `f3ec09775e9d81ccbba7314372ba546bd2be7e90` (landed-data tip `34b926730c30e0251e1aec531863d8355dc491f1` carries the same manifest blob)
clone: `/tmp/mutc3-manifest-1792885460` (`git clone --no-hardlinks` of the lane; disposable)

## Mutant (one plausible defect)

Cardinality-preserving swap inside the `### seat_reports` fence — the manifest
claims to name the d72ac16 inheritance and no path d72 did not add:

- deleted: `.ufo/waves/round-40/w1/ConnSiblingOverlap.md` (added by d72ac16)
- added: `.ufo/waves/round-40/w1/DecoySeatReport.md` (invented; d72ac16 did not add it)

Mutant commit `339968ea19dc08422883fd9c48469333597fe599` (single-file diff: 1 insertion, 1 deletion).
Manifest blob: pristine `8afe323130dd94241436c9c70b905b2b059a62f7` → mutant `f77de4afd141d6b92187c57e837c5b9af06f5c8e`.
Detector script untouched by the mutant (blob `e26e93fa7b8f8d383fe5f2ce90a3b4fb3f0b3f5c`, sha256 `def5eb7e40340463811954f58b7d5e381ea00909ff8a77e8828b8a460286c768`).

Rationale: a swap keeps every count at 67/7/71 and keeps total candidate lines at 145, so
only set-membership logic can catch it — a genuine probe of `manifest_covers_all` /
`manifest_no_extras`, not of the cardinality table.

## Expected detector

`count-c3.py` must print `C3=unmet` (rc=1) with:
- `manifest_covers_all FAIL missing=1 ['.ufo/waves/round-40/w1/ConnSiblingOverlap.md']`
- `manifest_no_extras FAIL extras=1 ['.ufo/waves/round-40/w1/DecoySeatReport.md']`
- cardinality checks still PASS (rows 67/7/71, inherited 145, freeze 20).

## Red-before witness (pristine, same detector, before mutation)

Run in the clone before any edit, at clone HEAD = lane tip `f3ec0977`:

```
check d72_ancestor           PASS (merge-base rc=0)
check d72_enumerated         PASS (paths=165)
check freeze_set_size        PASS (named-freeze paths=20 want 20)
check inherited_set_size     PASS (inherited paths=145 want 145)
check set_seat_reports       PASS (67 want 67)
check set_r40_evidence_scratch PASS (7 want 7)
check set_scratch            PASS (71 want 71)
check manifest_present       PASS (145 candidate path lines)
check manifest_covers_all    PASS (missing=0 [])
check manifest_no_extras     PASS (extras=0 [])
check manifest_seat_reports_rows PASS (listed=67 want 67)
check manifest_r40_evidence_scratch_rows PASS (listed=7 want 7)
check manifest_scratch_rows  PASS (listed=71 want 71)
C3=met
rc=0
```

Re-checked at the stated landing rev `34b92673` with the same clone: `manifest_covers_all PASS (missing=0)`,
`manifest_no_extras PASS (extras=0)`, `C3=met`, rc=0. Baseline is green; a failure below is attributable to the mutant.

## Mutant run (actual output)

`python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-42/count-c3.py 339968ea --repo /tmp/mutc3-manifest-1792885460`

```
check d72_ancestor           PASS (merge-base rc=0)
check d72_enumerated         PASS (paths=165)
check freeze_set_size        PASS (named-freeze paths=20 want 20)
check inherited_set_size     PASS (inherited paths=145 want 145)
check set_seat_reports       PASS (67 want 67)
check set_r40_evidence_scratch PASS (7 want 7)
check set_scratch            PASS (71 want 71)
check manifest_present       PASS (145 candidate path lines)
check manifest_covers_all    FAIL (missing=1 ['.ufo/waves/round-40/w1/ConnSiblingOverlap.md'])
check manifest_no_extras     FAIL (extras=1 ['.ufo/waves/round-40/w1/DecoySeatReport.md'])
check manifest_seat_reports_rows PASS (listed=67 want 67)
check manifest_r40_evidence_scratch_rows PASS (listed=7 want 7)
check manifest_scratch_rows  PASS (listed=71 want 71)
C3=unmet
rc=1
```

Exactly the two expected checks fire, naming the exact deleted and invented paths; no other check
changed state. The row-count checks demonstrate they are blind to a swap, and the set-diff arm is
what enforces the frozen contract.

## Verdict

**KILLED.** C3=unmet, rc=1, with the right failing checks and the right subjects. No survivor.

Coverage observation (not a contract change): fence ordering is not checked (the decoy was inserted
out of alphabetical position and nothing objected; the manifest elsewhere sorts sections
alphabetically), and `manifest_*_rows` checks are cardinality-only — the set-membership pair is the
load-bearing arm for swaps. No action requested.

## Restoration evidence

| state | file sha256 | git blob |
|---|---|---|
| pristine (before) | `d9cbae688f7672e64ea8c57d4a55c1ea3f85868f2de9a3e3d6826c1406154f25` | `8afe323130dd94241436c9c70b905b2b059a62f7` |
| mutant (during) | `91d4275f761f0a1249542293b24f3a4bbc9505443c3e636cc1a8b95d0d319bff` | `f77de4afd141d6b92187c57e837c5b9af06f5c8e` |
| restored (after) | `d9cbae688f7672e64ea8c57d4a55c1ea3f85868f2de9a3e3d6826c1406154f25` | `8afe323130dd94241436c9c70b905b2b059a62f7` |

Restored by `git show f3ec0977:corpus/knowledge/inheritance-d72ac16-r42.md > <file>` then
`git reset --hard f3ec0977`. Post-restore: `git status --porcelain` empty, HEAD `f3ec0977`,
file hash equals pristine byte-for-byte. Restored-bytes gate re-run: `C3=met`, rc=0.
Mutant commit `339968ea` remains addressable in the disposable clone for replay
(`git rev-parse 339968ea:corpus/knowledge/inheritance-d72ac16-r42.md` → `f77de4af…`).

## Bounds

- Wrote only this report under the lane. The lane's working tree, Git index, jj state and
  `.ufo/state` were untouched; all mutation ran in the `/tmp` clone.
- No tools installed or updated (python3/git already present), no credentials read, no pacman.
- Clone is disposable; no residual process left running.
