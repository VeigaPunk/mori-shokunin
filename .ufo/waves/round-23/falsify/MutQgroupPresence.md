# MutQgroupPresence — C2 directory-presence mutation

## Result and axes

**Mutation verdict: KILLED by both assigned named cases.** The same bounded detector passed both pristine controls, rejected both mutated rows, and passed both restored controls. This is a mutation-probe result, not a claim-admission, integration, health or privacy decision.

Axes: **coverage** (distinguish initialized btrfs qgroups from enabled accounting), **calibration/evidence integrity** (identify exact failing expected rows rather than infer from an aggregate), and **isolation/restoration** (separate pinned clone; exact original bytes restored).

## Pin, isolation and mutant

- Production pin: `f3dc07c0bf423cc1947d0ffa91afa9ce236fbe3c`.
- Expectation seal: `22772c10f6e3c1d8d3fe1b72083a6194e9f4e687`.
- Actual separate shallow clone: `/fast/scratch/hyaku/mori-r23/MutQgroupPresence/clone`.
- Observed clone HEAD: `f3dc07c0bf423cc1947d0ffa91afa9ce236fbe3c`; observed branch: `refs/heads/round23/MutQgroupPresence`.
- Mutated only `/fast/scratch/hyaku/mori-r23/MutQgroupPresence/clone/tools/mori-quota-surface.py`, function `classify_btrfs`, line 480:

```diff
-    if record["enabled"] is True:
+    if record["qgroups"] is True:
```

This is a plausible regression to directory-presence truth. The preceding checks already handle unavailable and absent directories; the replacement therefore incorrectly returns enabled for every remaining present-directory record, including enabled=false and enabled=null. Actual mutant bytes equaled the pinned source with exactly this one replacement; no other source delta was accepted.

The amended contract requires present+false → disabled/n/a/`btrfs_qgroups_disabled`, and present+null → unknown/n/a/`btrfs_qgroups_enabled_unavailable`. Source support read: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/evidence/sources/S079-fs_btrfs_sysfs.c`, lines 2355–2368 (explicit status flag), and `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/evidence/sources/S080-fs_btrfs_qgroup.c`, lines 432–476 (directory initialization before status-flag loading). Original contract, preseal amendment, source registry, case decisions and round-23 lesson were read; none was edited.

## Expected detector and exact input identities

Loaded `/fast/scratch/hyaku/mori-r23/MutQgroupPresence/bounded-detector.py` and called the identical `run_detector` function once for pristine, once for mutant, and once after restoration. It imports the sealed quota oracle's `evaluate_case`; primary comparisons are exit, finding_id and the ordered six-field path tuples. All supplementary checks and empty stderr are also required. No full-driver or real-mode arm was invoked.

Detector SHA-256: `e68a24a0fa66774168b2f523a31936f8ed1243a21498f54ffdd40a5104200758`.

Sealed oracle used: `/fast/scratch/hyaku/mori-r23/MutQgroupPresence/clone/.ufo/waves/round-23/oracle-quota.py`, SHA-256 `f1f4a027728180436fc5161171b0f6ad4ca4176229b5240aabb33e3f2af36bec`. Its clone and production bytes equaled the seal's committed bytes. The unexecuted rename oracle was also bound unchanged to the seal, SHA-256 `a55b2b50d3e7447a1d5312c8b066a13137a6a6895f0343b3240ebf081d97c5f2`.

Both case files were byte-identical in the production lane, pinned clone and expectation seal:

| Case file (absolute production path) | SHA-256 |
|---|---|
| `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/frozen/quota-cases/SupplementQgroupDisabled.json` | `f117bcb0b411cb2dd50910c62222481d8d283eeb49ff2169b40788b24dd09567` |
| `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/frozen/quota-cases/SupplementQgroupUnknown.json` | `22f77b779845660b131dc0b19f3e02ddf203165734dfda040c52f08a06755f56` |

The detector serializes each sealed `fixture` member without changing its values. Fixture hashes and scanner argv were identical in all three phases:

```text
/usr/bin/python -B /fast/scratch/hyaku/mori-r23/MutQgroupPresence/clone/tools/mori-quota-surface.py --fixture /fast/scratch/hyaku/mori-r23/MutQgroupPresence/fixtures/SupplementQgroupDisabled.fixture.json
/usr/bin/python -B /fast/scratch/hyaku/mori-r23/MutQgroupPresence/clone/tools/mori-quota-surface.py --fixture /fast/scratch/hyaku/mori-r23/MutQgroupPresence/fixtures/SupplementQgroupUnknown.fixture.json
```

- Disabled fixture SHA-256: `8eae5c0e63d9b55817bc3e36c69089f11618320aecd689f122c3ebf78d5c0f05`.
- Unknown fixture SHA-256: `482e9eebf1b8fee82e6f5fb5050c3c502e9c6c8ecd152ae01c2184863696c3b9`.
- Each scanner child: RLIMIT_AS **402653184 bytes (384 MiB)**, CPU limit **15 s**, subprocess wall timeout **15 s**. Exactly one scanner child at a time; six scanner invocations total. No timeout occurred; every child completed in under 0.05 s.
- `TMPDIR=/fast/scratch/hyaku/mori-r23/MutQgroupPresence`; bytecode writes disabled.

## Actual named-row outputs

For both cases, fstype remained `btrfs`, mount_point remained `/home`, device_check remained `btrfs_subvolume_skipped`, quota_option_keys remained `[]`, and btrfs_qgroups_mode remained null. The exact expected/scored differences were:

| Case / path | Phase | exit / finding_id | quota_state | enforcement | basis |
|---|---|---|---|---|---|
| SupplementQgroupDisabled — `/home/quota/disabled` | Expected; pristine; restored | 0 / QUOTA_DISABLED | disabled | n/a | btrfs_qgroups_disabled |
| SupplementQgroupDisabled — `/home/quota/disabled` | Mutant | 1 / QUOTA_ENABLED | enabled | unknown | btrfs_qgroups_enabled |
| SupplementQgroupUnknown — `/home/quota/unknown` | Expected; pristine; restored | 2 / QUOTA_STATE_UNKNOWN | unknown | n/a | btrfs_qgroups_enabled_unavailable |
| SupplementQgroupUnknown — `/home/quota/unknown` | Mutant | 1 / QUOTA_ENABLED | enabled | unknown | btrfs_qgroups_enabled |

For **each** mutant case, the sealed oracle returned `exit_match=false`, `finding_match=false`, `paths_match=false`; supplementary checks still passed. Thus the kill is attributable to the assigned behavior-bearing decision, not an inapplicable mutation, setup failure, timeout, schema/leakage failure, or pre-existing baseline failure. All six stderr outputs were empty.

| Detector phase | Passing named cases | Unmet named cases | Detector result code |
|---|---:|---:|---:|
| Pristine | 2/2 | 0 | 0 |
| Mutant | 0/2 | 2 | 1 |
| Restored | 2/2 | 0 | 0 |

## Before / mutant / after hashes and restored controls

| Source state | Bytes | SHA-256 |
|---|---:|---|
| Before | 66644 | `e485741334d2e72a0f007481f1d2bc5b38658f54c04232965e4bbf552b8f7e92` |
| Mutant | 66644 | `4c619add448792661c49ef2a888c9808768aaa5605501856c7d55435da532033` |
| After restoration | 66644 | `e485741334d2e72a0f007481f1d2bc5b38658f54c04232965e4bbf552b8f7e92` |

Restored source bytes equaled the saved pristine bytes exactly. For **both** named cases, restored stdout, stderr and exit code equaled pristine outputs exactly; argv, fixture hashes, case hashes and detector source hash were invariant across phases. Protected production files' before/after hashes also matched: both production tools, both oracles, contract, amendment, case decisions and both named cases. The per-file hashes are retained in the summary receipt. No production, frozen, oracle, expectation, sibling, lane index/ref or jj mutation was performed.

## Evidence retained

Only the small mutant source and bounded JSON receipts were archived; no Git history archive:

- `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/falsify/MutQgroupPresence/mutant-source.py` — 66644 bytes; SHA-256 `4c619add448792661c49ef2a888c9808768aaa5605501856c7d55435da532033`.
- `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/falsify/MutQgroupPresence/pristine.json` — actual argv, expected/actual outputs, limits, hashes and oracle checks; SHA-256 `324514d41692d2d6f7a8425337261a0fd2372e72e7ef45ab83fefaafd03a14cb`.
- `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/falsify/MutQgroupPresence/mutant.json` — same bounded receipt for the mutant; SHA-256 `7ccfb3708353a160e37cd86fb646a7bcb025bce599e6d3a83063bc2dcb6700c0`.
- `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/falsify/MutQgroupPresence/restored.json` — restored controls; SHA-256 `e9dbfb68d5075528cc38201b39940798245af866b168c304b2d1f2794ccda472`.
- `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/falsify/MutQgroupPresence/probe-summary.json` — revision/seal bindings, source identities, restoration and protected-file hashes; SHA-256 `2db99a38e65d9ddfd7d8428fdd19290dcb323729ca263c272bd39efaf8709c24`.

## Unchanged boundaries

This narrow probe does **not** replace the strict 30-case population. The retained disposition in `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/evidence/frozen-contradiction.json` remains: C2 strict target UNPROVABLE at 29/30 because frozen CaseEscapedSpace contradicts the sealed parent-ID rule. That case was neither executed here nor special-cased, excluded, relabelled or rewritten. No full driver was run, and its expected strict-red exit is not this mutant's kill criterion. The separately corrected public-selftest fixture was not invoked or confused with the frozen case.

C1 was not exercised by this C2-only assignment. No build, linter, formatter, selftest, live quota probe, mount operation, privileged command, session/transcript query, or other runtime was invoked. Existing open debt and privacy_clearance=false remain untouched. This author-lane subagent evidence is not outside closure or promotion authority.

Runtime used: existing `/usr/bin/python`, Python 3.14.8. **Tool installs/updates: none.**
