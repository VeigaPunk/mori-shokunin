# Round 29 no-harm base — RetentionBase

## Retention scan

Ran the requested baseline in a no-hardlinks sandbox clone, checked out detached at `7118f320a5ef18d20c1e361eff77db0e1a97b2d6`. Exact setup command: `mkdir -p /fast/scratch/hyaku/mori-r29/RetentionBase && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone --no-hardlinks /home/vgpnk/Projects/shokunin/mori-shokunin /fast/scratch/hyaku/mori-r29/RetentionBase/clone && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/mori-r29/RetentionBase/clone checkout --detach 7118f320a5ef18d20c1e361eff77db0e1a97b2d6` (tool output confirmed the requested HEAD).

Working directory: `/fast/scratch/hyaku/mori-r29/RetentionBase/clone`

Command:

```sh
python3 -I -B tools/mori-retention-gate.py scan --repo /fast/scratch/hyaku/mori-r29/RetentionBase/clone --rev 7118f320a5ef18d20c1e361eff77db0e1a97b2d6 --policy .ufo/waves/round-18/frozen/c1-policy.json --allowlist corpus/evidence/retention-allowlist.json
```

Complete stdout: `artifact://12745:raw:1-1` (one JSON record; no protected values observed in its fields). Stderr: empty. Exit code: `1` (Bash result). The record reports `metric=4`, `non_author=5`, `routed=0`, `forbidden_allowlist=[]`, `warnings=[]`, and four unallowlisted hits; commit is the requested baseline revision. The exact scan command and result are retained above and in the linked complete output.

Comparison: the round-28 receipt reports metric `4` and exit `1` at revision `5ef4e8db397b57299616258cb2e1c045c46564e7` (`.ufo/waves/round-28/evidence/tip-retention.txt:1-6`). Thus this entering baseline is equal to the recorded round-28 tip metric; the contract's no-harm criterion is that the later landed-tip metric not exceed the entering baseline (`.ufo/waves/round-29/contract.md:85-88`).

## Requested no-harm self-tests

Both paths exist in the clone: `tools/mori-pressure.py` and `tools/mori-census.sh`.

Pressure command, from the clone working directory:

```sh
python3 -I -B tools/mori-pressure.py --selftest
```

Exact marker/tally output:

```text
MORI_PRESSURE_SELFTEST: PASS 12/12
MATCHER: rejected 48/48 corrupted expectations
```

Census command, from the clone working directory:

```sh
bash tools/mori-census.sh --selftest
```

Exact marker/tally output:

```text
MORI_CENSUS_SELFTEST: PASS (134 cases, 134 passed, 0 failed)
```

Both commands returned normally (exit 0). No OOM-killers tool was opened or run. No tools were installed or updated. This is the requested entering-tip baseline only, not a landed-tip measurement.

## Scope and blockers

Only this report was written in the lane. No blocker encountered. The parent integration owner should compare the eventual landed-tip retention metric against baseline `4` and assess the two self-test tallies.
