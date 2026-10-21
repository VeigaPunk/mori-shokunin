# MutSetupPartial — setup-error partial-path mutation

## Scope and axes

Assigned C2 mutation only: challenge the no-partial-verdict invariant. Axes named: **coverage** (primary and supplementary sensitivity), **calibration** (a local kill is not overall C2 acceptance), and **operability** (isolated bounded execution and exact restoration). No round judgment, integration, shipping, or C1 remeasurement.

Production pin: `f3dc07c0bf423cc1947d0ffa91afa9ce236fbe3c`. Expectation seal: `22772c10f6e3c1d8d3fe1b72083a6194e9f4e687`. An actual separate shallow, blob-filtered clone was created at `/fast/scratch/hyaku/mori-r23/MutSetupPartial/clone`, and its observed HEAD was the production pin on branch `round23/MutSetupPartial`. Only the named source, sealed oracle/case copies, and derived synthetic fixture were materialized for this probe. No lane index, jj state, or lane refs were changed.

Authority read: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/contract.md` C2 requires QUOTA_SETUP with no partial verdict; `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/preseal-amendment.md` reiterates paths=[] on setup failures. The original and selected CaseSetupMalformed proposals, `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/frozen/case-decisions.json`, and `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/lessons/round-23.md` were read. The selected case deliberately omits device_links and expects exit=2, finding_id=QUOTA_SETUP, paths=[]. Its corrected qgroups_enabled member leaves that missing top-level key as the intended defect. Original S078/S079/S081/S082 source sections were also read; the no-partial rule itself is contract authority, not a kernel-state claim.

## Mutant and expected detector

One behavior-bearing replacement at `/fast/scratch/hyaku/mori-r23/MutSetupPartial/clone/tools/mori-quota-surface.py:790`, inside setup_payload:

```python
# pristine
"paths": [],
# mutant: manufacture a default unknown row despite setup rejection
"paths": [evaluate({"path": FLEET_ROOT, "realpath": FLEET_ROOT}, [], {}, os.path.basename)],
```

This is a generic erroneous fallback for every setup error, not a CaseSetupMalformed special-case. Empty synthetic mount input yields a complete nine-field unknown/no_covering_mount row, without host reads. Source bytes were confirmed to differ by exactly this replacement; applicability was true.

Expected rejection has two separately retained channels from the unchanged sealed oracle `/fast/scratch/hyaku/mori-r23/MutSetupPartial/clone/.ufo/waves/round-23/oracle-quota.py`:

1. evaluate_case primary `paths_match` must be false because the frozen expectation is an empty ordered path list.
2. supplementary `setup_no_partial_verdict` must be unmet because QUOTA_SETUP carries a nonempty paths list. The row is otherwise schema-shaped, so this is not a kill caused by malformed row keys.

The same evaluate_case function and the same CLI argv were used on pristine, mutant, and restored bytes. No oracle CLI main, full driver, selftest, or real-control arm was executed.

## Bounded command and actual output

Working directory: `/fast/scratch/hyaku/mori-r23/MutSetupPartial/clone`. Environment overrides: TMPDIR=`/fast/scratch/hyaku/mori-r23/MutSetupPartial`, PYTHONDONTWRITEBYTECODE=1. One child at a time, 402653184-byte (384 MiB) address-space ceiling, 15 CPU seconds, and a 15-second subprocess wall timeout:

```sh
/usr/bin/prlimit --as=402653184 --cpu=15 -- /usr/bin/python3 -B /fast/scratch/hyaku/mori-r23/MutSetupPartial/clone/tools/mori-quota-surface.py --fixture /fast/scratch/hyaku/mori-r23/MutSetupPartial/CaseSetupMalformed.fixture.json
```

| Phase | Tool exit / finding / error | paths length | Primary exit_match / finding_match / paths_match | Supplementary | Combined detector exit |
|---|---|---:|---|---|---:|
| Pristine | 2 / QUOTA_SETUP / fixture_key_set | 0 | true / true / true | 10/10 pass | 0 |
| Mutant | 2 / QUOTA_SETUP / fixture_key_set | 1 | true / true / false | 9/10 pass; setup_no_partial_verdict unmet | 1 |
| Restored | 2 / QUOTA_SETUP / fixture_key_set | 0 | true / true / true | 10/10 pass | 0 |

Actual mutant paths:

```json
[
  {
    "basis": "no_covering_mount",
    "btrfs_qgroups_mode": null,
    "device_check": "not_checked",
    "enforcement": "n/a",
    "fstype": null,
    "mount_point": null,
    "path": "/home/vgpnk/Projects/shokunin",
    "quota_option_keys": [],
    "quota_state": "unknown"
  }
]
```

All three runs had empty stderr, no timeout, and no retained-output truncation. Elapsed seconds, pristine/mutant/restored: 0.044558, 0.043257, 0.038843. Only the parsed output field `paths` changed in the mutant. Restored stdout and stderr were byte-identical to pristine. The child correctly exits 2 in the passing controls because that is the frozen expected setup outcome; detector exit 0 means the expected error was observed.

## Verdict and restoration

**KILLED.** The baseline passed, the applicable mutant emitted the forbidden nonempty list, and both the primary frozen case and the separate sealed no-partial assertion rejected it. All nine other supplementary checks passed. This is a bounded detector-sensitivity finding, not a production defect or permission to change the contract.

Restoration ran in a finally block before the restored control invocation. Exact source-byte equality was observed; both original and restored lengths are 66644 bytes.

| Bytes | SHA-256 |
|---|---|
| Pristine | `e485741334d2e72a0f007481f1d2bc5b38658f54c04232965e4bbf552b8f7e92` |
| Mutant | `376de48986531f5f1de63e54b50a782bd7bc25d3c21a7a788310a329b2c55f1c` |
| Restored | `e485741334d2e72a0f007481f1d2bc5b38658f54c04232965e4bbf552b8f7e92` |
| Frozen CaseSetupMalformed | `833cd8a536b33770ef11291ddc4e05ecd9cbf18ff7dcfa9abfe566021b916fe7` |
| Sealed oracle-quota.py | `f1f4a027728180436fc5161171b0f6ad4ca4176229b5240aabb33e3f2af36bec` |
| Derived fixture | `760e9dad34359da61f5ea532aacbb0e38625dd093f2ad8fe872ac42d3dd8db18` |

Case, oracle, and fixture hashes were unchanged in all three detector invocations. Production and frozen/oracle/expectation files were never edited by this seat. No live quota inputs, qgroups attributes, journal, transcripts, credentials, privileged commands, or sibling sources were accessed by the probe. No tools were installed or updated; existing versions observed: Git 2.56.0, Python 3.14.8, prlimit/util-linux 2.42.4.

## Durable evidence and limits

- Small complete mutant source: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/falsify/MutSetupPartial/mutant-source.py`.
- Exact argv, pin/seal/control hashes, mutation applicability, and restoration receipt: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/falsify/MutSetupPartial/argv-hashes.json`.
- Complete bounded stdout/stderr, parsed outputs, individual primary/supplementary assertions, and restored control: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/falsify/MutSetupPartial/bounded-results.json`.

Only the assigned three-phase mutation probe was exercised. C1 was not rerun. The supplied strict C2 disposition remains UNPROVABLE at29/30; the frozen CaseEscapedSpace contradiction was not run, changed, excluded, relabelled, or treated as this arm. No aggregate pass/admission is claimed. Inherited retention debt, permission RED11/12, unknown dispositions, blocked baseline acceptance, and privacy_clearance=false remain unchanged.
