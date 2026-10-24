# MutExtEnabled — assigned C2 mutation probe

**Verdict: KILLED.** Both exact corrected, sealed ext cases pass on pristine bytes, fail on the applicable mutant, and pass again after exact restoration. This is a two-case mutation-sensitivity result, not a full-C2 pass or admission verdict.

## Axes and isolation

Axes: C2 ext-hint epistemic calibration; exact frozen-row detector sensitivity; scratch isolation and byte restoration.

- Production pin: `f3dc07c0bf423cc1947d0ffa91afa9ce236fbe3c`.
- Expectation seal: `22772c10f6e3c1d8d3fe1b72083a6194e9f4e687`.
- Actual separate shallow clone: `/fast/scratch/hyaku/mori-r23/MutExtEnabled/clone`; unique scratch branch `round23/MutExtEnabled`, observed HEAD at the production pin. File-protocol cloning used `--no-local --no-checkout --depth 1 --revision=<pin>`; only the named quota source, sealed oracle and two sealed cases were materialized. Scratch branch initialization did not modify lane refs/index/jj. No unrelated Git history is archived with this report.
- `TMPDIR=/fast/scratch/hyaku/mori-r23/MutExtEnabled`; no `/tmp` fallback.
- Read the contract, preseal amendment, original ext proposals, sealed case decisions, round23 lesson and quota knowledge note. The amendment supersedes the original ext-enabled rule: hints and journal settings do not establish runtime enablement.

## Mutant

The sole behavior change is at `/fast/scratch/hyaku/mori-r23/MutExtEnabled/clone/tools/mori-quota-surface.py:504`, the existing ext2/ext3/ext4 quota-option branch:

```diff
-            return ("unknown", "n/a", "ext_quota_option_unverified"), None
+            return ("enabled", "n/a", "ext_quota_option_unverified"), None
```

Only the state literal changes. Enforcement and basis stay untouched, so failure cannot be attributed to changing those expected fields. This deliberately models promoting an option hint into positive enablement evidence. No input, expectation, oracle, production or sibling source was edited.

## Expected detector and byte identities

The same bounded detector at `/fast/scratch/hyaku/mori-r23/MutExtEnabled/detector.py` imports the unchanged sealed quota oracle and calls its `evaluate_case` function. It compares the actual process exit, finding ID, and ordered six-field path tuples: `path`, `fstype`, `mount_point`, `quota_state`, `enforcement`, `basis`. Supplementary checks are retained separately.

Detector SHA-256: `30caaf66c5137453fa3aed3a99770bb7313485cb770a810e2b81519e3072af08`.

Sealed quota oracle SHA-256: `f1f4a027728180436fc5161171b0f6ad4ca4176229b5240aabb33e3f2af36bec`.

The two case files and oracle were read from the production pin and compared byte-for-byte to their seal versions before use:

| Case | Exact sealed case SHA-256 | Derived fixture SHA-256 |
|---|---|---|
| CaseExt4Usrquota | `4db2fcd87bb1a2efcfadaff13311426eb8a6fc129663cfa486190a93ac959cda` | `8c2259a846eff1ba97e407f5ced28888a8a5f7841e3be52f2cd7bce8557314c8` |
| CaseExt4Journaled | `d317ccb1141271ed0cda2d2b2209fcfb965b57016e6dfc4e0efcf34560c9fb40` | `52b9d2336b9300b6ebe9c9143d3f7c12d1e8adaa6a62b407f50c232320d5746c` |

Each fixture child uses the same argv across all three stages:

```text
/usr/bin/prlimit --as=402653184 --cpu=15 -- /usr/bin/python3 -B /fast/scratch/hyaku/mori-r23/MutExtEnabled/clone/tools/mori-quota-surface.py --fixture /fast/scratch/hyaku/mori-r23/MutExtEnabled/fixtures/<CaseID>.fixture.json
```

The outer detector also has a 384 MiB address-space limit, 15-second CPU limit and 15-second tool deadline. Each fixture child has a 15-second wall timeout. Exactly one fixture child runs at a time; six fixture-only CLI children were exercised, two per stage. No child timed out; observed individual child durations were 0.032269–0.038034 seconds. No real/default-path invocation, public selftest, full driver, mount or privileged command was run.

## Actual outputs

Both cases expect actual process exit **2**, `finding_id=QUOTA_STATE_UNKNOWN`, and the following exact primary rows:

| Case / path | fstype | mount_point | quota_state | enforcement | basis |
|---|---|---|---|---|---|
| CaseExt4Usrquota: `/srv/data` | ext4 | `/srv/data` | unknown | n/a | ext_quota_option_unverified |
| CaseExt4Usrquota: `/srv/data/projects/app` | ext4 | `/srv/data` | unknown | n/a | ext_quota_option_unverified |
| CaseExt4Journaled: `/srv/journal/data` | ext4 | `/srv/journal` | unknown | n/a | ext_quota_option_unverified |

Pristine and restored outputs match every row above. The mutant changes **all three** rows' `quota_state` to `enabled`, with the other five primary fields unchanged. Both mutant processes exit **1** and emit `finding_id=QUOTA_ENABLED` and `exit_code=1` instead of the frozen expected unknown result. Thus the mutation is reached and applicable; it is not a setup error, syntax failure or nonmatching replacement.

| Stage | Detector exit | CaseExt4Usrquota | CaseExt4Journaled | Supplementary checks |
|---|---:|---|---|---|
| Pristine | 0 | pass; tool exit2 / QUOTA_STATE_UNKNOWN | pass; tool exit2 / QUOTA_STATE_UNKNOWN | 18/18 pass |
| Mutant | 1 | unmet; tool exit1 / QUOTA_ENABLED | unmet; tool exit1 / QUOTA_ENABLED | 18/18 pass |
| Restored | 0 | pass; tool exit2 / QUOTA_STATE_UNKNOWN | pass; tool exit2 / QUOTA_STATE_UNKNOWN | 18/18 pass |

For **each** mutant case, `exit_match=false`, `finding_match=false`, and `paths_match=false`. On both controls, all three fields are true. Both cases retain `device_check=match`, null `btrfs_qgroups_mode`, and their recognized option keys (`usrquota`; `jqfmt`, `usrjquota`). Stderr is empty; no additional supplementary failures were observed. Full synthetic stdout and individual check records are retained in the stage receipts.

## Restoration evidence

| Source stage | SHA-256 |
|---|---|
| Before / pinned pristine | `e485741334d2e72a0f007481f1d2bc5b38658f54c04232965e4bbf552b8f7e92` |
| Exercised mutant | `b270d9799b608d6b85ced0cd90bad7d00d3a5a9dcb9724eb40957445315d2437` |
| After exact restoration | `e485741334d2e72a0f007481f1d2bc5b38658f54c04232965e4bbf552b8f7e92` |

A `finally` block restored the exact pinned source bytes before the restored detector ran, including after the mutant detector's expected exit1. The restored parsed output objects equal the pristine objects for both cases. The archived mutant's hash equals the exercised mutant's hash. Detector hash, case hashes, fixture hashes and child argv remain identical across stages.

All **43** protected lane-file hashes are identical across pristine, mutant and restored snapshots: both production tools, all JSON files beneath the frozen directory, and the named contract, amendment and quota/rename oracles. These snapshots are included in each receipt. No lane production, frozen, rule or oracle bytes changed.

## Retained scope and debt

- This assigned ext mutation was killed independently by both corrected sealed cases; it does not change the frozen population or denominator.
- Strict C2 remains **UNPROVABLE at 29/30**, with frozen CaseEscapedSpace's expected enabled row conflicting with the sealed parent-topology refusal. That case/rule/oracle remains unchanged; it was not special-cased, relabelled or repaired. The full driver's known exit1 is not evidence of this mutant's kill and was not rerun here.
- No C1 execution or new C1 claim. No conflation with the separately corrected co-evolved selftest arm or its reported49/49.
- Four inherited unallowlisted hits, raw95/allowlisted86/non-author5, original permission RED11/12, two unknown dispositions, blocked baseline acceptance and `privacy_clearance=false` remain unchanged. This report provides no outside closure, health, clearance, admission or promotion authority.
- Existing tools only: Git2.56.0, Python3.14.8, prlimit from util-linux2.42.4. No installs, updates, service operations, subagents or other runtime were invoked.
- Evidence collection encountered `read` appending a display footer to an explicit raw range. Reported through `xd://report_issue`; complete receipts were recovered from exact ranged payloads. No behavioral invocation was repeated because of that display issue.

## Archived artifacts

- `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/falsify/MutExtEnabled/mutant-source.py`
- `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/falsify/MutExtEnabled/argv-hashes.json`
- `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/falsify/MutExtEnabled/before.json` — SHA-256 `6cfebbdeba1f4b659ffa72e81b6cc3e8e8a883a1a8bcf42a260cc963b441dd16`
- `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/falsify/MutExtEnabled/mutant.json` — SHA-256 `357dffdeb414755206b510c9286ec02eaa47c9f328f47d6cef5ffd0d41bfd627`
- `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/falsify/MutExtEnabled/after.json` — SHA-256 `378517749bb1c5834094883ea9afee97b0dcf6b6792b5df9c83f85998d5a1583`

Report: .ufo/waves/round-23/falsify/MutExtEnabled.md
