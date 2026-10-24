# MutMisroot — C3 filename-only witness mutation

Date: 2026-10-20. Seat: `MoriR17.MutMisroot-4`. Mutation verdict: **KILLED**.

## Attacked scope and axes

- Claim axis: **C3 calibration**, specifically the retained, byte-exact `MoriR16.Lesson` whose filename supplies the lane/round tokens and whose content does not. Authority: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-17/contract.md:21-27`; Amendment A1 at `:109-123` was read and does not replace this C3 requirement.
- Probe axes: filename-witness sensitivity; identical-detector repeatability; containment and byte-exact reversibility. These are probe dimensions, not additional round claims or admission judgments.
- Only behavior changed: path-token matching in the copied detector inside `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/MutMisroot`. No production correction, contract change, or independent C1/C2 assessment was attempted.
- Pinned provenance: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-17/PINNED_INPUTS.json:3,12,15` records measured commit `273aa74ab73701f41fea38ec7bd1c47b4b2bfbc7`, detector digest and witness digest. The observed clone source matched that detector digest; no VCS command was used to infer the clone's ref state.
- Lesson requirement: `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/lessons/round-17.md:34-36,135-139` rejects a convenient synthetic replacement and requires the exact archived witness. This probe used the copied tool's unchanged embedded 847-byte witness.

## Mutant and expected detector

Target copy:

`/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/MutMisroot/tools/mori-misroot-sweep.py`

One plausible regression: simplify candidate recognition to content-only, dropping both filename/path-token tests while retaining content tests, token regexes, status enumeration, fixture bytes, expected assertions, and all other code.

The mutation deleted exactly the following six original lines, `:290-295`, from `_scan`:

```python
        if lane_rx.search(rel_path):
            lane_hit = True
            matched_in.append("path")
        if round_rx.search(rel_path):
            round_hit = True
            matched_in.append("path")
```

The content matcher immediately following them, original `:296-302`, remained unchanged. This is one behavior-bearing mutation, not six independent mutants. It leaves content-bearing nested candidates detectable while making filename-only candidates invisible.

Expected detector: the **same copied script's `--selftest`**, run on pristine, mutated, and restored bytes. The existing `no-pathspec-round16` arm expects `MoriR16.Lesson` (`:534-544`), verifies its path-only attribution and exact size (`:693-712`), and fails if it is absent (`:736-762`). The separate `path-only-match` arm at `:594-598` is an additional sensitivity check, not a substitute for the exact r16 witness.

Expected mutation result: rc1, `MORI_MISROOT_SELFTEST_FAIL`, specifically `arm no-pathspec-round16: byte-exact planted witness not detected`, with `planted_found_without_pathspec:false`. A pristine failure would instead make the probe inconclusive.

**Mutant SHA-256:** `136b9abe904aca750c20d6c6df3d992efd2aee5e39e63dad8f697bd248b47598`.

## Commands and execution bounds

All three detector executions used the identical command below and working directory `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/MutMisroot`, with a 45-second outer deadline, no PTY, and no background execution:

```sh
/usr/bin/env TMPDIR=/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/MutMisroot/.scratch HOME=/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/MutMisroot/.scratch/home XDG_CONFIG_HOME=/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/MutMisroot/.scratch/xdg PYTHONDONTWRITEBYTECODE=1 GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_TERMINAL_PROMPT=0 /usr/bin/python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/MutMisroot/tools/mori-misroot-sweep.py --selftest
```

Sequence: pristine command; delete the six path-matching lines; hash mutant and run the same command; hash mutant again; restore the captured original lines; hash restored source and run the same command; hash restored source, production source, and frozen witness. The mutant command was prefixed with its hash command via `&&`; the restored command was bracketed with hash commands via `&&`. The mutant detector returned rc1 as expected; restoration was performed despite that return code.

Initial and final pin-hash command, rc0 each time:

```sh
/usr/bin/sha256sum /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/MutMisroot/tools/mori-misroot-sweep.py /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-misroot-sweep.py /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-17/frozen/MoriR16.Lesson
```

Mutant-before, mutant-after, and restored-before hash command, rc0 each time:

```sh
/usr/bin/sha256sum /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/MutMisroot/tools/mori-misroot-sweep.py
```

Runtime identification command, rc0:

```sh
/usr/bin/python3 --version && /usr/bin/git --version
```

Raw output:

```text
Python 3.14.8
git version 2.56.0
```

No tools were installed or updated; install/update channel and reason are not applicable.

## Actual raw detector outputs

The JSON below is retained verbatim from the detector outputs, not reconstructed from expectations. No stderr text was observed in the tool output for any of the three executions.

### Pristine — rc0

```json
{"arms": 11, "finding": "MORI_MISROOT_SELFTEST_OK", "fixture_bytes": 847, "fixture_sha256": "15f9f82d707d5c79b11643eed1ab4754b6959d2bede5887e07364442ada5510e", "planted_found_with_legacy_pathspec": false, "planted_found_without_pathspec": true, "planted_matched_in": ["path"], "sandbox_unchanged": true, "schema": "mori-misroot-sweep-v1"}
```

### Content-only mutant — rc1

```json
{"arms": 11, "failures": ["arm no-pathspec-round16: candidates=['.ufo/waves/round-16/build/MoriNote.md'] want=['.ufo/waves/round-16/build/MoriNote.md', 'MoriR16.Lesson']", "arm no-pathspec-round16: byte-exact planted witness not detected", "arm poisoned-env-scans-intended-fleet: candidates=['.ufo/waves/round-16/build/MoriNote.md'] want=['.ufo/waves/round-16/build/MoriNote.md', 'MoriR16.Lesson']", "arm path-only-match: rc=0 want=1", "arm path-only-match: finding='MORI_MISROOT_CLEAN' want='MORI_MISROOT_CANDIDATE'", "arm path-only-match: candidates=[] want=['MoriR15.note']", "arm path-only-match: matched_in=[] want=['path']", "arm round-normalization: candidates=['.ufo/waves/round-16/build/MoriNote.md'] want=['.ufo/waves/round-16/build/MoriNote.md', 'MoriR16.Lesson']", "capability arm: planted root file not found without pathspec"], "finding": "MORI_MISROOT_SELFTEST_FAIL", "fixture_bytes": 847, "fixture_sha256": "15f9f82d707d5c79b11643eed1ab4754b6959d2bede5887e07364442ada5510e", "planted_found_with_legacy_pathspec": false, "planted_found_without_pathspec": false, "planted_matched_in": null, "sandbox_unchanged": true, "schema": "mori-misroot-sweep-v1"}
```

### Restored — rc0

```json
{"arms": 11, "finding": "MORI_MISROOT_SELFTEST_OK", "fixture_bytes": 847, "fixture_sha256": "15f9f82d707d5c79b11643eed1ab4754b6959d2bede5887e07364442ada5510e", "planted_found_with_legacy_pathspec": false, "planted_found_without_pathspec": true, "planted_matched_in": ["path"], "sandbox_unchanged": true, "schema": "mori-misroot-sweep-v1"}
```

## Hashes and exact restoration evidence

| Observed bytes | SHA-256 |
|---|---|
| Assigned copy, pristine before detector | `0a852fe67f14afa1da9f5f8e806c63fa640e8df2a90b87909e6a2453c66b3dca` |
| Assigned copy, mutant before detector | `136b9abe904aca750c20d6c6df3d992efd2aee5e39e63dad8f697bd248b47598` |
| Assigned copy, mutant after detector | `136b9abe904aca750c20d6c6df3d992efd2aee5e39e63dad8f697bd248b47598` |
| Assigned copy, restored before detector | `0a852fe67f14afa1da9f5f8e806c63fa640e8df2a90b87909e6a2453c66b3dca` |
| Assigned copy, restored after detector | `0a852fe67f14afa1da9f5f8e806c63fa640e8df2a90b87909e6a2453c66b3dca` |
| Production detector, before and after probe | `0a852fe67f14afa1da9f5f8e806c63fa640e8df2a90b87909e6a2453c66b3dca` |
| Frozen witness, before and after probe | `15f9f82d707d5c79b11643eed1ab4754b6959d2bede5887e07364442ada5510e` |

Initial and final three-file hash output, identical on both observations:

```text
0a852fe67f14afa1da9f5f8e806c63fa640e8df2a90b87909e6a2453c66b3dca  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/MutMisroot/tools/mori-misroot-sweep.py
0a852fe67f14afa1da9f5f8e806c63fa640e8df2a90b87909e6a2453c66b3dca  /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-misroot-sweep.py
15f9f82d707d5c79b11643eed1ab4754b6959d2bede5887e07364442ada5510e  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-17/frozen/MoriR16.Lesson
```

The exact deleted lines were retained in the edit tool's capture register and pasted back at the original gap; the restored edit snapshot returned to `46EB`, matching the pristine snapshot. The restored full-file SHA-256 also equals both the initial observed copy hash and the pinned input hash. No source restoration is outstanding.

## Finding, limits, and containment

**Killed, not inconclusive:** the unchanged bounded detector returned **0 → 1 → 0**. Under the mutant, the required exact `MoriR16.Lesson` witness disappeared while the content-bearing nested `MoriNote.md` still appeared. The detector explicitly reported the exact witness failure; this was not merely a failure of the synthetic empty-body `MoriR15.note` check. All three outputs retained the same 847-byte fixture digest, reported the legacy pathspec missing the planted root witness, and reported `sandbox_unchanged:true`.

This finding is limited to the assigned content-only regression in the copied selftest. It is not a blanket pass of C3, a fresh live fleet-root census, an independent admission decision, or a rerun of L1's committed C3 measurement. No broader defect search or extra probe was run.

Only the assigned clone's copied script was edited, then exactly restored, plus this assigned report. No production, sibling, fleet-root file, MANIFEST, state, or clone VCS metadata was edited by this seat. The expressly authorized copied selftest itself performs Git init/add/commit in its fresh sandboxes under the clone's `.scratch` (`:468-497`) and automatically removes those temporary sandboxes in its existing `finally` (`:781-782`). No direct VCS-mutating command was issued against any checkout, no jj/runtime integration command was invoked, and the assigned clone/script were retained for L1. No `/tmp` probe output/scratch, background job, live journal query, package transaction, or service operation was used.

L1 `MoriR17` remains sole planner/integrator and decides how this mutation evidence bears on admission.
