# C2 counter mutation probe — data side

## Setup and baseline

The counter selects its lane from `MORI_C2_LANE` (`.ufo/waves/round-29/count-c2.sh:8`); its required-case, provenance, pin, blob, freeze and final C2 checks are at `count-c2.sh:180-215, 229-268`. C2's frozen-file, writer, unchanged-after-freeze and self-test requirements are in `.ufo/waves/round-29/contract.md:55-64`; provenance and decisive-pin amendments are at `:157-160,170-178`.

Sandbox: `/fast/scratch/hyaku/mori-r29/w2/MutCountC2/lane`, detached at `8809a3fe1eaa87a0afa177a15263d174378e7462`. Detector command for each run (using the script's `MORI_C2_LANE` variable): `MORI_C2_LANE=/fast/scratch/hyaku/mori-r29/w2/MutCountC2/lane bash /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-29/count-c2.sh HEAD`.

Pristine output: `blind_exit=1`, `blind_violations=20`, `a2_r29_selftest=FAIL(exit=1)`, `C2=unmet` (exit 1). Restored output repeated those same values. Because the pristine detector already fails, the mutation verdict for every row is **inconclusive**, not killed; the observed column records whether its mutation-specific output changed as expected. The underlying C2 failure is retained, not attributed to these mutants.

## Mutants

All commits below were made in the sandbox from the pristine tip, then the clone was checked out back to that exact tip before the next probe. Hashes are SHA-256 before → after for the changed path; rename preserves content hash, deletion's after-state is absent.

| Edit (sandbox commit) | Expected detector signal | Observed detector output | SHA-256 before → after | Verdict |
|---|---|---|---|---|
| Change a frozen case's expected verdict (`a8c8c5f`) | Freeze changed; report no longer matches case | `freeze_edits=1; freeze_blob_versions=2; cases_changed_since_freeze=1; provenance=23/24 unselected=1` | `1c76ea1f10e08acedb82c001a875ea84a9f552acf931ca2837645d482bb9d252` → `7614c20deea401399121e429fe4e33a4363155bdb29c9c0210332a535a6651aa` | Inconclusive; signal observed |
| Drop one case (`f130d0b`) | Freeze changed; count/provenance gap | `cases_changed_since_freeze=1; a2_r29_cases=23; A2-07 cases=11; provenance=23/23 unselected=1` | `1c76ea1f10e08acedb82c001a875ea84a9f552acf931ca2837645d482bb9d252` → `701b283a2145c431ad6ba9adb908a652ebe7df6719f7a9bddac7e5ab64f5575b` | Inconclusive; signal observed |
| Add an L1-authored case (`5aff716`) | Reject non-writer author / unmatched provenance | `a2_r29_schema=error case_24_author_invalid; provenance=24/25 unselected=0` | `1c76ea1f10e08acedb82c001a875ea84a9f552acf931ca2837645d482bb9d252` → `315fd038d28dce344c95ecb4569e7c613061c1444e7618e60993508531e60252` | Inconclusive; signal observed |
| Reassign one case's author key to another valid A2-07 writer (`2782810`) | Provenance must fail | `provenance=23/24 unselected=1; a2_r29_schema=ok` | `1c76ea1f10e08acedb82c001a875ea84a9f552acf931ca2837645d482bb9d252` → `b0931ca7cfb8d2234b608c53d291d57db7860726e6662f51046576df9a96944e` | Inconclusive; signal observed |
| Replace a case input with one from `cases.json` (`dddf9f3`) | Detect overlap with legacy input | `a2_r29_legacy_input_overlaps=1; a2_r29_input_checks=fail:input_distinctness` | `1c76ea1f10e08acedb82c001a875ea84a9f552acf931ca2837645d482bb9d252` → `8214309366ed8eb22268f384de76f9da0bbe528b03bebc8a2c0375b5952d0e6f` | Inconclusive; signal observed |
| Remove the positive SIGTERM pin from an A2-07 shape case (`117f91d`) | Case must stop contributing to shape count | `shape_a207=2/2` (pristine `3/2`); `a2_r29_shape_checks=ok` | `1c76ea1f10e08acedb82c001a875ea84a9f552acf931ca2837645d482bb9d252` → `5bdc8bc5f6743280efc974550e6b8226058143aa24a8093e4b9dd3daef9352e0` | Inconclusive; signal observed |
| Delete writer report `CaseA207a.md` (`8a8b9a7`) | Report absence/provenance must fail | `writer_absent=CaseA207a; provenance=21/24 unselected=0; blind_violations=19` | `6ac883d4db539465d4eeffa4843d52d86d850d5b54292a110c64bb0d45fecbbb` → absent | Inconclusive; signal observed |
| Rename the frozen case file (`35c5ce4`) | Required path/freeze must be absent | `cases_a2_r29_blob=absent; a2_r29_schema=absent; provenance=0/0 unselected=24` | `1c76ea1f10e08acedb82c001a875ea84a9f552acf931ca2837645d482bb9d252` → same hash at renamed path | Inconclusive; signal observed |
| Change `cases-a2.json` expected exit (`97ecddd`) | Baseline blob mismatch and old-file self-test fail | `cases_a2_blob_state=mismatch; cases_a2_selftest=FAIL(exit=1)` | `ec04a74a3eb65f856dedb3f0509122ee07fdfba7f49e90781d86ab2a393ea6aa` → `81a4f4acf118e5848ba8a06a1a6d322cf62e822845d4850519d42bc8b9a0081c` | Inconclusive; signal observed |

Each observed string is the corresponding detector output; each mutant run also ended `C2=unmet` (exit 1). No mutant is classified as killed or survived because the pristine detector fails. The direct expected signal appeared for all nine; therefore this run reports no survivor-based counter gap.

## Restoration and tooling

After the final probe the sandbox was returned to `8809a3fe1eaa87a0afa177a15263d174378e7462`; `git status --short` was empty. Restored SHA-256 values: `cases-a2-r29.json` = `1c76ea1f10e08acedb82c001a875ea84a9f552acf931ca2837645d482bb9d252`; `cases-a2.json` = `ec04a74a3eb65f856dedb3f0509122ee07fdfba7f49e90781d86ab2a393ea6aa`; `cases.json` = `84d2343f1d672a4597a4ec5efe0fd048eb399e8b4f0f5b86cc483ff8f2e547af`; deleted writer report restored from the same tip and its SHA-256 was `6ac883d4db539465d4eeffa4843d52d86d850d5b54292a110c64bb0d45fecbbb`.

Operational note: the first relative-path rename briefly resolved under `/home/vgpnk/Projects/shokunin/tools/` instead of the sandbox. It was immediately moved into the sandbox with an absolute destination; a directory listing then showed no file at the workspace location and the renamed file only under the sandbox. No lane or fleet Git writes were run. No tools were installed or updated.