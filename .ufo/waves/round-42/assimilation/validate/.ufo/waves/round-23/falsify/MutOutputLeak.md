# MutOutputLeak — scoped C2 output-minimization mutation

## Axes and verdict

**Mutant: KILLED by both assigned supplementary detectors.** This is a single-case mutation result, not a judgment, integration or admission of C2.

- **Coverage:** challenge output minimization on the exact frozen `CaseExt4Journaled` fixture, independently of its six-field primary classification.
- **Calibration:** keep primary and supplementary outcomes separate; an expected tool exit 2 is not a failing control. C1 was not exercised by this seat.
- **Isolation/restoration:** change one behavior-bearing line only in an actual separate sparse clone; restore identical bytes and repeat the same detector.

Production revision: `f3dc07c0bf423cc1947d0ffa91afa9ce236fbe3c`. Expectation seal: `22772c10f6e3c1d8d3fe1b72083a6194e9f4e687`. Observed clone HEAD was the production revision; its own branch is `round23/MutOutputLeak`.

Isolated clone: `/fast/scratch/hyaku/mori-r23/MutOutputLeak/clone`. It was created with `git clone --shared --no-checkout --no-tags --single-branch`, then sparsely populated with only the quota source, sealed oracle and assigned frozen case. Shared Git objects were only read; lane refs/index/jj were not mutated. No unrelated history is archived in the report artifacts.

## Mutant and expected detector

Target: `/fast/scratch/hyaku/mori-r23/MutOutputLeak/clone/tools/mori-quota-surface.py`, function `evaluate`, after original line 549. The sole added line was:

```python
    result["option_values"] = [part.split("=", 1)[1] for part in mount.super_options.split(",") if "=" in part]
```

This plausible diagnostic-field defect emits selected mount-option values in a new per-path key. It is generic: no filesystem, case ID, expected output or canary value is hard-coded. Classification, finding, tool exit, canonical `quota_option_keys` and the six primary fields are untouched.

Expected supplementary failures, from the unchanged sealed oracle:

1. `path_key_set`: rejects the extra per-path `option_values` key.
2. `no_leakage`: rejects the distinctive synthetic option-value canary from the supplied journaled-quota fixture.

The top-level `output_key_set` is a different check and was expected to remain passing. The exact one-line insertion matched once and the added nonempty field was observed in the assigned case's actual mutant output; the mutation was applicable, not merely a source edit that failed to execute.

## Pinned inputs and detector

- Oracle: `/fast/scratch/hyaku/mori-r23/MutOutputLeak/clone/.ufo/waves/round-23/oracle-quota.py` — SHA-256 `f1f4a027728180436fc5161171b0f6ad4ca4176229b5240aabb33e3f2af36bec`.
- Frozen case: `/fast/scratch/hyaku/mori-r23/MutOutputLeak/clone/.ufo/waves/round-23/frozen/quota-cases/CaseExt4Journaled.json` — SHA-256 `d317ccb1141271ed0cda2d2b2209fcfb965b57016e6dfc4e0efcf34560c9fb40`.
- Extracted fixture: `/fast/scratch/hyaku/mori-r23/MutOutputLeak/CaseExt4Journaled.fixture.json` — SHA-256 `52b9d2336b9300b6ebe9c9143d3f7c12d1e8adaa6a62b407f50c232320d5746c`; its parsed object equals the frozen case's `fixture` exactly. Neither the case nor its expectation was edited.

Source bytes matched the production Git blob; oracle and case bytes matched their exact seal Git blobs before execution. Original/corrected case decisions, the contract, preseal amendment, round-23 lesson and S082/S083 source decisions were read; the accepted corrected case, not the superseded original enabled expectation, was used.

The same detector function called `oracle.evaluate_case(case_obj, parsed, child.returncode, child.stdout)` for all three phases. Composite detector acceptance required its separate primary result, **every supplementary check**, and empty stderr. Detector-source SHA-256: `fb46649a3a2421c5e4fb0860a477c7e5992fb59162aca68808c6858a52291e07`; exact function text is retained in the argv/hash receipt.

Identical child argv for all three phases:

```json
["/usr/bin/python", "/fast/scratch/hyaku/mori-r23/MutOutputLeak/clone/tools/mori-quota-surface.py", "--fixture", "/fast/scratch/hyaku/mori-r23/MutOutputLeak/CaseExt4Journaled.fixture.json"]
```

Runtime: Python 3.14.8. Each fixture child ran serially with address-space limit 384 MiB (402653184 bytes), CPU limit 15 seconds, wall timeout 15 seconds, core dumps disabled, and `TMPDIR=/fast/scratch/hyaku/mori-r23/MutOutputLeak`. No `/tmp` fallback. The retained stdout/stderr size bound was 32768 bytes per stream; actual stdout was at most 1028 bytes. No timeout, detector error or stderr occurred.

## Actual outputs

| Phase | Tool exit / finding | Primary comparisons | Supplementary | Composite detector |
|---|---|---|---|---|
| Pristine | 2 / QUOTA_STATE_UNKNOWN | exit, finding, paths all match | 9/9 pass | pass |
| Mutated | 2 / QUOTA_STATE_UNKNOWN | exit, finding, paths all match | 7/9 pass; `path_key_set`, `no_leakage` unmet | fail |
| Restored | 2 / QUOTA_STATE_UNKNOWN | exit, finding, paths all match | 9/9 pass | pass |

All phases retained the expected path classification: ext4, mount point `/srv/journal`, quota state `unknown`, enforcement `n/a`, basis `ext_quota_option_unverified`. The mutant only added the leaking diagnostic field. Consequently the six-field primary detector alone would not kill this mutant; the separately sealed supplementary checks do.

Actual durations were 0.036975, 0.042721 and 0.038110 seconds. Stdout lengths were 988, 1028 and 988 bytes; stderr was empty in every run. Complete actual fixture-only stdout/stderr, all check names/status/details, exit codes, argv and hashes are retained in the bounded result, rather than replaced with an aggregate claim.

## Restoration evidence

| Source state | SHA-256 |
|---|---|
| Before | `e485741334d2e72a0f007481f1d2bc5b38658f54c04232965e4bbf552b8f7e92` |
| Mutant | `729669d080e247e55b65faf8369d57da972328a043731bbe9841b9570504e1d8` |
| After | `e485741334d2e72a0f007481f1d2bc5b38658f54c04232965e4bbf552b8f7e92` |

The added line was removed immediately after the mutant detector. Restored source bytes equal the saved pristine bytes exactly. Restored stdout, stderr and exit also equal the pristine control exactly; restored stdout SHA-256 is `1ecd0ff181b2222748ea990146a3bc65371508ff153aebbe379724d5ec84ff21`. Post-probe production quota source, lane oracle and frozen assigned case hashes equal their original bound bytes. No production, frozen, rule or oracle edits were made by this seat.

## Artifacts and retained boundaries

- Small mutant source (66756 bytes): `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/falsify/MutOutputLeak/mori-quota-surface.mutant.py`.
- Exact argv, dependency/source hashes, detector source and resource bounds: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/falsify/MutOutputLeak/argv-hashes.json`.
- Bounded actual results and restoration control: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/falsify/MutOutputLeak/bounded-result.json`.

Only the three authorized fixture invocations were executed. No full driver, selftest, C1 oracle, live quota/sysfs/mount inspection, quota tool, mount, privileged command, model/runtime dispatch, install or update was performed. Tools installed/updated: **none**.

The strict frozen C2 target remains the parent's known **29/30 / UNPROVABLE**, with `CaseEscapedSpace` unchanged; that full-driver result was not remeasured here. This kill does not fix or waive its parent/topology contradiction and must not be conflated with the separately corrected co-evolved selftest arm. C1's separately reported original26 and guards were not revalidated by this probe. Four inherited unallowlisted hits, original permission RED11/12, unknown dispositions, blocked baseline acceptance and `privacy_clearance=false` remain unchanged context. No clearance, health, promotion or outside-closure claim is made.
