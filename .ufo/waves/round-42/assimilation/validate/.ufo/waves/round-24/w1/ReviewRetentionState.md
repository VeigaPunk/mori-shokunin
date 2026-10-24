# ReviewRetentionState — C1 retention floor re-run (mori round 24, wave 1, attempt 2)

Seat: MoriR24.ReviewRetentionState (read-only reviewer). Date: 2026-10-22.
Measured revision: `29c1bf45dde6af48fc9a07aef447bd7d7f822cc5` (pinned by the assignment;
an ancestor of the lane tip `4059ffb5e4b81da6f4a1a00056ba8364cac123c8`, verified with
`git merge-base --is-ancestor`).

**Verdict: the round-23 retained-context debt R2 must preserve is unchanged at the
measured revision.** Exit 1 with finding `RETENTION_FINDINGS` and metric 4, byte-identical
to the recorded floor `.ufo/waves/round-23/evidence/retention-floor-final.json` in every
compared field: metric, routed sub-count, non-author count, raw/allowlisted hit counts,
policy hash, and all four unallowlisted debt rows (path, class, line, line hash). Exit 1 is
the gate's designed value for a nonzero debt, not a tool failure.

## Scope and method

- Sandbox clone only; the lane repo was never written. Clone made with
  `git clone --no-hardlinks /home/vgpnk/Projects/shokunin/mori-shokunin
  /fast/scratch/hyaku/mori-r24-a2/retention-check`, then
  `git checkout --detach 29c1bf45dde6af48fc9a07aef447bd7d7f822cc5` inside the clone.
  All git writes (clone, checkout) happened in that sandbox clone; lane-repo git use was
  read-only (`rev-parse`, `cat-file`, `merge-base --is-ancestor`, `diff --stat`).
- `TMPDIR=/fast/scratch/hyaku/mori-r24-a2/retention-check-tmp`; the scan's stdout is kept
  at `retention-check-tmp/scan-stdout.json` under that tmp root, outside the lane tree.
- Command run, from the clone as working directory (wall time 11.7 s):

```
TMPDIR=/fast/scratch/hyaku/mori-r24-a2/retention-check-tmp python3 -I tools/mori-retention-gate.py scan \
  --repo /fast/scratch/hyaku/mori-r24-a2/retention-check \
  --rev 29c1bf45dde6af48fc9a07aef447bd7d7f822cc5 \
  --policy .ufo/waves/round-18/frozen/c1-policy.json \
  --allowlist corpus/evidence/retention-allowlist.json
```

- Because the clone is checked out at the measured revision, the tool, policy, and
  allowlist read from the working tree are exactly the committed `29c1bf45` versions. The
  prescription's working-tree invocation is therefore rev-consistent; additionally
  `git diff --stat 29c1bf45..4059ffb5 -- tools/mori-retention-gate.py
  .ufo/waves/round-18/frozen/c1-policy.json corpus/evidence/retention-allowlist.json` is
  empty, so these three files are byte-identical between the measured revision and the
  current lane tip.
- Report prose hygiene: per CriticC1Vacuity's warning, the R2 predicate scans any added
  lane line, so this report never places the privacy-clearance key, a separator, and the
  affirmative value on one line; the predicate is paraphrased and cited to the contract.

## Result — re-run versus recorded floor

Both sides are gate stdout JSON (`emit` writes one object; fields per
`tools/mori-retention-gate.py:289-307`).

| Field | Recorded floor (round-23 evidence) | Re-run at `29c1bf45` |
|---|---|---|
| exit | 1 | 1 |
| finding_id | `RETENTION_FINDINGS` | `RETENTION_FINDINGS` |
| commit | `4994c0df54ee793c0c25c34d178729d42c045803` | `29c1bf45dde6af48fc9a07aef447bd7d7f822cc5` |
| metric (unallowlisted) | 4 | 4 |
| routed | 0 | 0 |
| non_author | 5 | 5 |
| raw hits | 95 | 95 |
| allowlisted hits | 86 | 86 |
| stale warnings / forbidden rows | 0 / 0 | 0 / 0 |
| policy_sha256 | `db06e9810bbfd243fb0a753a46960573df39083ea90174ce463cf2a0ab523128` | same |

The recorded floor's argv also used the same frozen policy and allowlist paths and the same
`scan` form; its `measured_revision` is the round-18 measurement commit, so "unchanged"
here means metric and hit-multiset identity across revisions — exactly what was re-derived.

## The four debt rows (identical on both sides)

All four sit in the round-20 falsify-run copy of the frozen policy file; classes R2, R5,
R6, R8 at lines 8, 11, 12, 14, with line hashes:

- R2 line 8 — `8d92bfa35a8069140e7fc1376d7c4e8cac73c80819b3c27868c9f8f1efd0f1fb`
- R5 line 11 — `7f23448e6e231eed6c297714990f83f305deb8038785fe332cdab173c23228bd`
- R6 line 12 — `0cdc89722df0e3be7fefb7ee61c70c938abab86e85e5de2f367530a5772473a2`
- R8 line 14 — `1d2b6e6ed2ba144d0a7b8b61854ee0472d51c9a98ab8f3dadbfa816c8b855839`

Path for all four: `.ufo/waves/round-20/falsify/NoHarmRun/rg/.ufo/waves/round-18/frozen/c1-policy.json`.
These are the red rows the routed text requires preserved; nothing re-derived differs.

## Corroboration of the R2 blob predicates (supporting, read-only)

- Blob identity of both R2-protected evidence files from base `c725aa37` to the measured
  rev, and equality with the lane worktree copies I compared against:
  - `retention-floor-final.json`: blob `4954de42072b8c5520f95067a6b005a5c82fbbb2` at base,
    at `29c1bf45`, and in the worktree (all equal).
  - `retention-floor-final-comparison.json`: blob `1411d94a8b16f844e0d334ea6135bd7d85969318`
    at base, at `29c1bf45`, and in the worktree (all equal).
- Added-line sweep `git diff --unified=0 c725aa37..29c1bf45 | grep '^+' | grep -ic` for the
  contract's privacy-clearance affirmative pattern: 0 matches.

So the baseline file this review compared against is the committed, unaltered R2 blob, and
no added line between base and the measured revision turns R2's affirmative-value red.

## Findings by severity

- Blockers: none.
- Major: none.
- Minor (informational, no action):
  1. The recorded floor evidence carries `measured_revision 4994c0df…` (round-18), not the
     round-24 revision; equality had to be established at hit level across revisions, which
     this re-run does. A future floor re-derivation could record the new rev alongside the
     multiset to make that explicit, but this is not a defect in round-23's artifact.
  2. Tool-byte identity for the original round-23 run is not provable from the artifact: its
     argv records the lane worktree tool path, not a hash. Mitigated here by the policy hash
     matching on both runs and by the gate, policy, and allowlist being byte-identical across
     the entire `29c1bf45..4059ffb5` window checked.

## Residual risk and verification gaps

- The gate's policy states its own limit (frozen `c1-policy.json`, "known_limit"): regex
  classes are a recall floor, not a privacy proof. Metric 4 unchanged means the frozen
  floor is unchanged; it is not a statement that no private context exists beyond these
  tokens.
- Not run (and so not passed): the gate's `--selftest` (not prescribed for this item); any
  scan of the lane working tree (out of scope — the prescription is revision-scoped); the
  routed-check R1/R3/R4 items and sandbox mutants (owned by ReviewC1Predicates).
- Lane worktree dirty state, if any, is irrelevant to this result: every gate input was
  read from git objects at the pinned revision inside the sandbox clone.

## Tooling

No installs or upgrades performed. Runtime: system `python3` 3.14.8 and `git` 2.56.0;
`jq` for evidence extraction. Channels: none (preexisting system tools).

## Sandbox state left behind

- `/fast/scratch/hyaku/mori-r24-a2/retention-check` — clone, detached at `29c1bf45`.
- `/fast/scratch/hyaku/mori-r24-a2/retention-check-tmp/scan-stdout.json` — raw gate stdout.
- Lane-repo writes: this report file only.
