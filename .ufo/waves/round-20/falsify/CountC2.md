VERDICT: HOLDS

The C2 counts reproduce on the current tree: `[14,0]` and `matched = 14`. The "before" is an observed harness run, not an assumed number: its bytes regenerate exactly from the entering-tip path, and the absence it records is confirmed against git and a snapshot. Five weaknesses sit beside the arithmetic. §3 shows the independent 14-case oracle is blind to one contract clause, and §4A shows a silent exit 0 when no waves are discovered. Neither changes the counts.

Seat: MoriR20.CountC2 (leaf, no subagents). Checks ran 08:00–08:09 (-03). Tools: system python3, /usr/bin/jq, sha256sum, cmp, stat. git read-only only (`cat-file`, `show`, `log`, `ls-tree`, `rev-parse`) under `GIT_OPTIONAL_LOCKS=0`. Installs or updates: none.

## 1. Counts

Contract command on committed evidence (rc 0):
```
$ jq -s '[.[].counts.capability_absent]' evidence/c2-before.json evidence/c2-after.json
[14, 0]
$ jq .counts.matched evidence/c2-after.json
14
```

Regenerated with the harness (all rc 0; outputs in falsify/CountC2/):
- `c2-oracle.py --tool /tmp/countc2/absent.py --out before-now.json` gives `{capability_absent 14, matched 0, mismatched 0}`. `/tmp/countc2/absent.py` does not exist (`test -e` false).
- `c2-oracle.py --tool tools/mori-wave-settlement.py --out after-now.json` gives `{capability_absent 0, matched 14, mismatched 0}`.
- `jq -s '[.[].counts.capability_absent]' before-now.json after-now.json` gives `[14, 0]`. `jq .counts.matched after-now.json` gives `14`.

Byte checks (cmp; all equal to the committed evidence):
- before regenerated with the entering-snapshot path `/tmp/mori-r20/entering/tools/mori-wave-settlement.py` equals `evidence/c2-before.json`. The absent.py run differs only in the 15 `"tool"` lines, as expected.
- after regenerated at 08:01:43, when the tool was the HEAD version (8f8c58e, 682 lines), equals `evidence/c2-after.json`.
- after regenerated at 08:05:49, against the working tree with R7 (sha256 e5c06dad…, 689 lines, mtime 08:04:26), equals `evidence/c2-after.json`.

## 2. Before: observed, not assumed

Observed independently:
1. Harness provenance. `c2-before.json` regenerates byte-for-byte from `c2-oracle.py`. It has schema `mori-r20-c2-oracle-v1`, 14 results, each `status: capability_absent` with `observed: {tool_exists: false}`. It is not hand-written.
2. Tool absent at the entering tip. `git cat-file -e 2061780117e6ca637725004897bd288d3ba7e988:tools/mori-wave-settlement.py` prints `fatal: path 'tools/mori-wave-settlement.py' exists on disk, but not in '2061780…'` and exits 128. This matches contract.md:90-92.
3. Snapshot is faithful for tools/. `/tmp/mori-r20/entering/tools` holds 18 files. All 18 are byte-equal to `git show 2061780:tools/<f>` (0 differing). Directory mtime is 06:38:23, before the freeze (07:23) and the tool (07:45). I checked only tools/, not the whole tree.
4. Presence is the discriminator. With an absent path, `c2-oracle.py:341-348` returns capability_absent before any scan runs. With an empty present file, the result is `{matched 0, mismatched 14}` (out_file_missing, output_json_unavailable), so absent is not conflated with broken. With the lane tool present, the result is 14 matched.
5. Frozen cases unchanged. `git show e4d9384:.ufo/waves/round-20/frozen/c2-expected.json` is byte-equal to the working file. The tool first enters history in 2eeae04 (07:47:09), after the freeze commit e4d9384 (07:23:18).

Limits (stated, not defects):
- The before measures presence only. No frozen case is executed in the before state, so 14 = len(frozen cases) × absence bit. contract.md:90-92 calls this "capability red", which fits the intent, but it says nothing about case behaviour.
- v0→v1 harness repair. `diff c2-oracle-v0.py c2-oracle.py` touches only lines 33–35 (the no-spawn `taskCall`). v0 regenerated now is byte-identical to `c2-after-oracle-v0-fixture-defect.json`, and it fails only `no-spawn` (exit 0 expected, 1 observed; state unavailable). The repair follows frozen/c2-expected.json:18 (`taskCall null`). It is a fidelity fix, and the v0 bytes are kept.

## 3. Sensitivity of the 14/14 (scratch mutants of the 689-line tool; lane untouched)

Each mutant is a copy under /tmp/countc2/mut, changed by one line (diff verified, 2 diff lines each).

| id | change (current tool line) | independent oracle | tool `--selftest` |
|---|---|---|---|
| M1 | empty report counted present (227) | 13/14, fails `empty-report` | FAIL 21/22 |
| M2b | misroot detection disabled (233, `if False:`) | 13/14, fails `misrooted` | not run |
| M2 | misroot condition inverted (233) | 11/14, fails one-missing, none-present, misrooted (not a clean single fault; [INFERENCE] exception from `_inspect_report_path(None, …)`) | FAIL 18/22 |
| M3 | exit code forced 0 (366) | 6/14, fails 8 | FAIL 10/22 |
| M5 | `_lstat` → `os.stat`, follows symlinks (71) | 13/14, fails `symlink-report` | FAIL 21/22 |
| M4 | `..` component check removed (162) | **14/14, survives** | FAIL 21/22 (r7 case, line 50) |
| lead's `evidence/mut-r7/mutant-no-lexical-dotdot.py` | same class as M4 | **14/14, survives** | FAIL 21/22 (matches `selftest-mutant.txt`) |

Concrete behaviour on fixture `/tmp/countc2/dotlane`, whose report path is `.ufo/../.ufo/waves/round-1/build/A.md` and non-empty:
- production tool: status unsafe, state unavailable, rc 1.
- M4 / lead's mutant: status present, state settled, rc 0.

The frozen `traversal` case (`../../outside.md`, frozen/c2-expected.json:14) is rejected by the containment check in both versions, so the 14 cases cannot tell them apart. Only the in-tool r7 case (tool line 50) can.

## 4. Adjacent findings (surfaced while attacking the count)

A. Zero discovered waves exits 0 silently. Results:
- Empty lane (no `.ufo`): rc 0, `waves: []` (`falsify/CountC2/zero-empty-lane.json`).
- `.ufo/waves` symlinked to a directory holding an unsettled dispatch: rc 0, `waves: []`, and no unreadable or ignored count (`zero-symlink-waves.json`).
- Same dispatch in a real directory: rc 1, unsettled, missing [A] (`control-real-waves.json`).
- Cause: `_wave_root` returns None for a missing or symlinked `.ufo`/`waves`. `rc = 0 if all(...)` on an empty list is 0 (tool line 366).
- No frozen case covers this. contract.md:87 literally permits it, but it is the false-clean class the lesson's M6 names. Severity: medium for fleet-wide scans.

B. Independent oracle blind spot. contract.md:70-72 requires "contain no `..` component". The 14 frozen cases test only outside-lane traversal. The clause is covered only by the tool's own r7 case (tool line 50). The lesson now discloses R7 (lesson lines 35–37, "Eight refinement selftest cases"). The independent harness still passes the mutant 14/14, and the lesson does not claim otherwise.

C. Independence not evidenced [INFERENCE]. The harness is black-box: it imports only argparse, json, os, pathlib, subprocess and tempfile, and it only runs the CLI. But harness and tool were first committed together in 2eeae04 under the same author name, so separate authorship cannot be shown from git.

D. Provenance of after.json. Evidence records a tool path, not a digest or commit. The working-tree tool changed at 08:04:26 (R7 added, 682→689 lines), after the 07:46 evidence was written and after HEAD 8f8c58e (07:57:29). The committed after.json still reproduces byte-for-byte, so 14/14 holds on both versions. Nothing in the evidence binds it to a tool version.

E. Minor.
- (i) `c2-oracle.py:416` exits 0 whenever mismatched is 0, so the before run reads green with 14 capability_absent.
- (ii) The tool docstring (lines 4–16) lists R1–R5 only, while REFINEMENT_CASES now has 8 entries including r6 and r7.
- (iii) R2 `stub` makes `present` stricter than the frozen definition (contract.md:74-75, size > 0). This is disclosed in lesson R2 and is not re-litigated here.

## 5. Caveats for the judge

- The count claim (`[14,0]`, 14) survives. "14/14 by an independent oracle" is weaker than stated for the `..` clause (§3, §4B). If the judge needs the independent oracle alone to cover that clause, score that part PARTIAL.
- Suggestion only, not applied: add an in-lane `..` case to the independent harness with expected `unsafe 1`, then re-run. I did not edit the harness or any lane file.
- The zero-wave exit 0 (§4A) is outside the count but inside C2's coverage promise.

## 6. Bounds and artifacts

- Not opened: `.ufo/interactive-sessions/`, `.ufo/worktrees/`, `.jj/`, `~/.omp`. No grep or glob of the lane or fleet. `mori-census.sh` not run (not in the item).
- Scratch: `falsify/CountC2/` holds before-now, after-now, before-entering-now, v0-after, mut-*-oracle, zero-*, control-real-waves, dotdot-inside-lane-*. `/tmp/countc2/` holds absent.py (deliberately absent), mut/ and mutlane/ copies, and the dotlane, symlane and nowaves fixtures.
- Lane writes: none outside `falsify/CountC2/` and this report. No mutating git or jj commands.
