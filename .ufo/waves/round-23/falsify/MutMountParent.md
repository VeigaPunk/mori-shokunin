# MutMountParent — parent-ID refusal mutation probe

**Verdict: KILLED.** The applicable one-statement mutant makes frozen `SupplementHiddenMount` fail the unchanged sealed detector; the unchanged original-derived `CaseXfsUsrquota` control passes in pristine, mutant and restored phases. Both cases pass again after exact byte restoration. This is a focused detector-sensitivity result, not a C2 admission or an outside-lane judgment.

## Axes and isolation

- C2 coverage: sensitivity to omission of the conservative parent-ID consistency refusal.
- Specificity: preserve the unrelated original XFS enabled control.
- Evidence integrity: pinned independent clone, immutable case/oracle bytes, bounded fixture execution and byte-exact restoration.

Actual separate clone: `/fast/scratch/hyaku/mori-r23/MutMountParent/clone`. Its observed HEAD was `f3dc07c0bf423cc1947d0ffa91afa9ce236fbe3c`, and its unique branch was `refs/heads/round23/MutMountParent`. Expectation seal: `22772c10f6e3c1d8d3fe1b72083a6194e9f4e687`. The clone was created with `--no-checkout --no-hardlinks --revision=f3dc07c0bf423cc1947d0ffa91afa9ce236fbe3c` and a sparse checkout; production/lane Git refs and index were not changed. No other seat's files were edited.

## Mutant and expected detector

Only `/fast/scratch/hyaku/mori-r23/MutMountParent/clone/tools/mori-quota-surface.py:461` was changed:

```diff
-            return None, "ambiguous_overmount"
+            pass
```

This models an omitted early refusal: the code can identify inconsistent parent topology but falls through to classification. The separate duplicate-covering-mountpoint refusal remains intact. No path-specific exception, fixture, expected tuple, oracle or contract change was made.

The immutable rule at `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/preseal-amendment.md:115–124` requires refusal when the chosen mount's parent is present but differs from the longest strictly-shorter cover's ID. In `SupplementHiddenMount`, chosen ID70 at `/home/x/y` has parent65, while the shorter covering `/home/x` has ID80. The four covering mountpoints are distinct, so this case specifically exercises the parent-ID check rather than duplicate-point refusal. Source field semantics were read at `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/evidence/sources/S082-Documentation_filesystems_proc.rst:1965–2002; original decisions and the round23 lesson were also read.

The SAME unchanged sealed `/fast/scratch/hyaku/mori-r23/MutMountParent/clone/.ufo/waves/round-23/oracle-quota.py` `evaluate_case(case_obj, parsed, exit_code, stdout_text)` function evaluated both cases in all three phases. Fixture payloads were extracted from the exact sealed JSON without changing their data. A detector pass requires `exit_match`, `finding_match` and `paths_match` all true, plus every independently listed supplementary check passing. This uses the oracle's original six-field ordered tuple, not a replacement expected result.

Every fixture child ran sequentially with address-space limit **402653184 bytes (384 MiB)**, CPU limit15s, wall timeout15s, core dumps disabled, `TMPDIR=/fast/scratch/hyaku/mori-r23/MutMountParent`, and `--fixture` only. There were six child invocations total, no concurrent fixture children, no timeouts, no invocation/JSON errors, and empty stderr for all six. No full driver, public selftest, build, formatter, lint, default-mode or live quota probe was run.

Exact fixture-child argv, unchanged across phases:

```json
["/usr/bin/python", "/fast/scratch/hyaku/mori-r23/MutMountParent/clone/tools/mori-quota-surface.py", "--fixture", "/fast/scratch/hyaku/mori-r23/MutMountParent/fixtures/SupplementHiddenMount.fixture.json"]
```
```json
["/usr/bin/python", "/fast/scratch/hyaku/mori-r23/MutMountParent/clone/tools/mori-quota-surface.py", "--fixture", "/fast/scratch/hyaku/mori-r23/MutMountParent/fixtures/CaseXfsUsrquota.fixture.json"]
```

## Actual detector outputs

`E/F/P` means the exact oracle fields `exit_match` / `finding_match` / `paths_match`. Supplementary checks are separate from those original headline predicates.

| Phase | Case | Actual process exit / finding_id | E/F/P | Supplementary | Detector |
|---|---|---|---|---|---|
| pristine | `SupplementHiddenMount` | 2 / `QUOTA_STATE_UNKNOWN` | true/true/true | 9/9 | pass |
| pristine | `CaseXfsUsrquota` | 1 / `QUOTA_ENABLED` | true/true/true | 9/9 | pass |
| mutated | `SupplementHiddenMount` | 1 / `QUOTA_ENABLED` | false/false/false | 9/9 | FAIL |
| mutated | `CaseXfsUsrquota` | 1 / `QUOTA_ENABLED` | true/true/true | 9/9 | pass |
| restored | `SupplementHiddenMount` | 2 / `QUOTA_STATE_UNKNOWN` | true/true/true | 9/9 | pass |
| restored | `CaseXfsUsrquota` | 1 / `QUOTA_ENABLED` | true/true/true | 9/9 | pass |

For `SupplementHiddenMount`, the frozen expected and pristine/restored primary row is:

```json
{"path":"/home/x/y/z","fstype":null,"mount_point":null,"quota_state":"unknown","enforcement":"n/a","basis":"ambiguous_overmount"}
```

Pristine/restored metadata: `device_check="not_checked"`, `quota_option_keys=[]`, `btrfs_qgroups_mode=null`; process exit2, `finding_id="QUOTA_STATE_UNKNOWN"`.

The mutant instead emits this primary row:

```json
{"path":"/home/x/y/z","fstype":"btrfs","mount_point":"/home/x/y","quota_state":"enabled","enforcement":"unknown","basis":"btrfs_qgroups_enabled"}
```

Mutant metadata: `device_check="btrfs_subvolume_skipped"`, `quota_option_keys=[]`, `btrfs_qgroups_mode="qgroup"`; process exit1, `finding_id="QUOTA_ENABLED"`. All three headline predicates fail. Its nine generic supplementary assertions still pass, so the actual kill is carried by the independent primary expectation, not by a modified supplementary target.

For `CaseXfsUsrquota`, BOTH ordered expected rows remain exactly matched in all phases:

```json
[
  {"path":"/srv/xfsquota","fstype":"xfs","mount_point":"/srv/xfsquota","quota_state":"enabled","enforcement":"enforced","basis":"xfs_quota_option"},
  {"path":"/srv/xfsquota/projects/data","fstype":"xfs","mount_point":"/srv/xfsquota","quota_state":"enabled","enforcement":"enforced","basis":"xfs_quota_option"}
]
```

Each control row has `device_check="match"`, `quota_option_keys=["usrquota"]`, `btrfs_qgroups_mode=null`. Control exit1/`QUOTA_ENABLED` is its EXPECTED positive-mechanism result, not a detector failure. Control return code/stdout/stderr are byte-identical across all three phases. No additional detector failures were observed in these two assigned cases.

## Hash and restoration evidence

SHA-256 of the quota source:

| State | SHA-256 |
|---|---|
| Pristine, equal to production pin | `e485741334d2e72a0f007481f1d2bc5b38658f54c04232965e4bbf552b8f7e92` |
| Mutant | `47f59c743ddbeb7d32035cdf9e8c44f1e9846c36371e6759ecef906579f2166c` |
| Restored | `e485741334d2e72a0f007481f1d2bc5b38658f54c04232965e4bbf552b8f7e92` |

After restoring the exact original statement, full source bytes compare equal to the saved pristine bytes, not merely equivalent behavior. Restored return code/stdout/stderr for BOTH cases match pristine byte-for-byte. The lane production source also still equals the original pin's bytes.

The following oracle/case bytes were checked equal between the expectation-seal Git objects, isolated clone and lane, and their hashes remained unchanged through the probe:

| Input | SHA-256 |
|---|---|
| `oracle-quota.py` | `f1f4a027728180436fc5161171b0f6ad4ca4176229b5240aabb33e3f2af36bec` |
| `SupplementHiddenMount.json` | `d1a3a4c66008fcdefec47839d9393f1c971ebc6630d96b94c399038378187824` |
| `CaseXfsUsrquota.json` | `3e1620f745d7a1cc6fa497b1f61f991539809cd1bde67f86b73860baaaa4244b` |

Exact absolute source/case paths and generated fixture payload hashes are retained in the receipt below. The sealed original-derived control is the selected `CaseXfsUsrquota`, unchanged during this probe; it is not a rewritten old-shape proposal.

## Retained artifacts and limits

- Small mutant source: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/falsify/MutMountParent/mori-quota-surface.parent-refusal-mutant.py`.
- Full bounded outputs, per-case expected objects, actual parsed JSON, raw stdout/stderr, exact argv, fixture hashes, oracle checks, bounds and restoration booleans: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/falsify/MutMountParent/probe-receipt.json`.
- Receipt SHA-256: `1937198b78c391b9c7ed6da1dea016d11b5c11323acd6501103793e1dc349902`.
- Restored scratch source: `/fast/scratch/hyaku/mori-r23/MutMountParent/clone/tools/mori-quota-surface.py`.

Only the small mutant source and result receipt were archived under the assigned evidence directory; no Git-history archive was made. No tools were installed or updated.

This probe does not rerun C1 or assert its aggregate results. It does not execute, modify, exclude or relabel frozen `CaseEscapedSpace`, and does not use the separate co-evolved selftest arm to repair it. The supplied strict C2 finding remains **UNPROVABLE at29/30**, with the original denominator and contradiction retained. Privacy clearance, health/admission, baseline acceptance and inherited debt are unchanged. No integration, shipment or further mutation is claimed.
