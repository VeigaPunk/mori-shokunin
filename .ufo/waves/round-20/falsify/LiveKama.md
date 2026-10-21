# LiveKama: C2 falsification on lane kama (live scan vs wave-1 GT vs committed fleet scan)

Seat: MoriR20.LiveKama (leaf; read-only on kama; no subagents). Scope: kama dispatch files only.

## Verdict: HOLDS

C2 accuracy on lane kama holds. At every instant I measured, the live tool output matched an independent recomputation exactly (19 waves, 1198 members, per-member status, wave state, missing-name lists, dispatch hashes). Every difference from the wave-1 ground truth (`GtLaneKama.md`, scan 10:34:51Z) and from the committed fleet scan (`c2-live-fleet.json`, 10:46:53Z) is live report writing in `round-21/build`, attributed to file mtimes. I found no kama classification error. Tool defects are in section 4; none changes a kama count.

Caveat: the lane is live and the tool file was edited five times during this wave (section 4, F7). Every number below carries its timestamp and tool hash.

## 1. Runs (all read-only on kama; writes only under `falsify/LiveKama/` and `/tmp`)

Assigned command, first attempt, exit code 2:
```
python3 .../mori-wave-settlement.py scan --lane-root .../kama-shokunin --fleet-root .../shokunin --out .../round-20/falsify/LiveKama/scan.json
stderr: mori-wave-settlement: cannot write --out      (exit 2)
```
Cause: `falsify/LiveKama/` did not exist and `main` does not create the parent (tool:698-704, F1). I created that seat scratch directory with `mkdir -p` and re-ran the identical command: exit 1 (expected, because not every wave is settled), JSON written at 11:03:11Z.

Tool versions (sha256 prefix, mtime UTC). HEAD = commit `2eeae04` (10:47:09Z), sha `c6e60919…`:

| tag | sha256 | mtime (UTC) | delta vs HEAD |
|---|---|---|---|
| v1 (HEAD) | c6e60919 | 10:45:51 | none |
| v2 | e5c06dad | 11:04:26 | r7 selftest case and fixture |
| v3 | 203c716e | 11:11:12 | docstring 64→16 bytes; R6/R7 notes; r7 selftest |
| v4 | 5027bdc7 | 11:13:06 | R8 production change (symlinked parent → unsafe); r8 selftest |
| v5 | aae79d15 | 11:15:18 | `name_hint` label `undispatched-name:` → `filename:` |
| v6 | c134c57b | 11:15:31 | fleet root `realpath` + must be a directory (tool:327-329); error text |

Measured runs. Each bracketed run has an independent oracle snapshot before and after (`S*`), taken seconds apart:

| run | UTC | tool | present | missing | misrooted | stub | empty | unparsed | unsafe | ignored_json | unreadable_json | oracle diffs |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| scan.json (assigned) | 11:03:11 | v1 | 1067 | 131 | 0 | 0 | 0 | 0 | 0 | 385 | 1 | not bracketed; differs from A/B by 2 mtime-attributed members (3.4) |
| A | 11:06:03 | v2 | 1069 | 129 | 0 | 0 | 0 | 0 | 0 | 397 | 1 | 0 (S0, S1) |
| B | 11:06:03 | v2 | 1069 | 129 | 0 | 0 | 0 | 0 | 0 | 397 | 1 | 0 (S1, S2); A and B byte-identical |
| C | 11:12:39 | v3 | 1069 | 129 | 0 | 0 | 0 | 0 | 0 | 398 | 1 | 0 (S3, S4) |
| D | 11:14:11 | v4 | 1070 | 128 | 0 | 0 | 0 | 0 | 0 | 399 | 1 | 0 (S5, S6); sha stable through run |
| E (latest) | 11:15:34 | v6 | 1070 | 128 | 0 | 0 | 0 | 0 | 0 | 400 | 1 | 0 (S7, S8); sha stable through run; E = D apart from ignored_json |

Selftest (`--selftest`): v4 `PASS (23 cases, 23 passed, 0 failed)`, exit 0; v6 same, exit 0.

## 2. Per-dispatch comparison

GT = `GtLaneKama.md` (scan 10:34:51Z), columns m/p/miss/mis/stub/state. Tool = run E (11:15:34Z). Fleet = `c2-live-fleet.json` (10:46:53Z): it records totals only (no per-dispatch detail), so it is reconciled in section 3, not per file.

| # | dispatch (under `.ufo/waves/`) | GT m/p/miss/mis/stub/state | tool E m/p/miss/mis/stub/state | equal |
|---|---|---|---|---|
| 1 | round-11/dispatch.json | 32/30/2/0/0 partial | 32/30/2/0/0 partial | yes |
| 2 | round-11/verification-dispatch.json | 32/32/0/0/0 settled | 32/32/0/0/0 settled | yes |
| 3 | round-12/dispatch.json | 32/32/0/0/0 settled | 32/32/0/0/0 settled | yes |
| 4 | round-13/dispatch.json | 32/32/0/0/0 settled | 32/32/0/0/0 settled | yes |
| 5 | round-14/dispatch.json | 32/32/0/0/0 settled | 32/32/0/0/0 settled | yes |
| 6 | round-15/build/dispatch.json | 64/60/4/0/0 partial | 64/60/4/0/0 partial | yes |
| 7 | round-15/falsify/dispatch.json | 32/32/0/0/0 settled | 32/32/0/0/0 settled | yes |
| 8 | round-16/build/dispatch.json | 81/81/0/0/0 settled | 81/81/0/0/0 settled | yes |
| 9 | round-16/falsify/dispatch.json | 79/79/0/0/0 settled | 79/79/0/0/0 settled | yes |
| 10 | round-17/build/dispatch.json | 82/82/0/0/0 settled | 82/82/0/0/0 settled | yes |
| 11 | round-17/falsify/dispatch.json | 80/73/7/0/0 partial | 80/73/7/0/0 partial | yes |
| 12 | round-18/build/dispatch-95.json | 95/75/20/0/0 partial | 95/75/20/0/0 partial | yes |
| 13 | round-18/build/dispatch.json | 75/75/0/0/0 settled | 75/75/0/0/0 settled | yes |
| 14 | round-18/falsify/dispatch.json | 76/66/10/0/0 partial | 76/66/10/0/0 partial | yes |
| 15 | round-19/build/dispatch.json | 64/64/0/0/0 settled | 64/64/0/0/0 settled | yes |
| 16 | round-19/falsify/dispatch.json | 66/0/66/0/0 unsettled | 66/0/66/0/0 unsettled | yes |
| 17 | round-20/build/dispatch.json | 72/71/1/0/0 partial | 72/71/1/0/0 partial | yes |
| 18 | round-20/falsify/dispatch.json | 86/73/13/0/0 partial | 86/73/13/0/0 partial | yes |
| 19 | round-21/build/dispatch.json | 86/0/86/0/0 unsettled | 86/81/5/0/0 partial | **no: live (3.1)** |
| | **totals** | 1198/989/209/0/0; settled 10, partial 7, unsettled 2 | 1198/1070/128/0/0; settled 10, partial 8, unsettled 1 | |
| | fleet 10:46:53Z totals | 1198/997/201; misrooted 0; empty 0; unparsed 0; unsafe 0; unreadable 1; exit 1; waves 19 | (reconciled in 3.2) | |

Also checked: all 19 dispatch sha256 values equal GT Appendix B (no dispatch file changed; newest dispatch mtime is 10:28:38Z, `round-21/build/dispatch.json`); the tool's `missing` lists equal the oracle's for every wave; `misrooted` is 0 (GT 0); `stub` is 0 (GT has no stub class, and no present report is ≤200 bytes); `duplicate_of` is null everywhere (no duplicate dispatch bytes); within-wave duplicate report paths are 0 (oracle and tool); `name_hinted_waves` is 0; unique report paths 1123 (GT claim confirmed), unique present 994 = 914 + 80 as of run B; wave order is sorted by path bytes.

## 3. Differences, explained

### 3.1 round-21/build (the only per-dispatch difference): GT 0/86 unsettled → E 81/86 partial

- All 81 report files now present have mtime after the GT scan. Earliest 10:45:57Z (SimplifyAudit); latest 11:13:48Z (RevengeSpliceOrigin). None had mtime ≤ 10:34:51Z, so the GT's missing classification was correct at its instant. The full per-member table, with mtimes and sizes, is in `falsify/LiveKama/members-kama-r20.tsv` (1198 rows).
- Partition by mtime. Each window reproduces one snapshot total exactly:
  - mtime ≤ 10:46:53Z: 8 members (SimplifyAudit 10:45:57, LessonDraftC2 10:46:02, SimplifyGrid 10:46:13, KnowledgeSonameEntry 10:46:14, RegressInstallTreeGrid 10:46:19, SkillRowLinks 10:46:29, SkillRowAudit 10:46:32, ShonenMap 10:46:35). 989 + 8 = 997 = fleet present.
  - 10:46:53Z < mtime ≤ 11:03:11Z: 70 members. 997 + 70 = 1067 = scan.json present.
  - 11:03:11Z < mtime ≤ 11:06:03Z: 2 members (ClosureNotesSweep 11:04:07Z; LinksDigestEncoding 11:05:44Z). 1067 + 2 = 1069 = run A/B.
  - 11:06:03Z < mtime ≤ 11:14:11Z: 1 member (RevengeSpliceOrigin 11:13:48Z). 1069 + 1 = 1070 = run D/E.
- Still missing (5): AuditErrataMutants, AuditRegexMutants, LinksGateMutants, LinksGridMutants, RegressSkillGates. No file exists at the lane path and none exists at the fleet path (no misrooted copy).
- Fleet snapshot: its 997 present and 201 missing are exactly GT plus the 8 mtime-≤10:46:53Z members. Fleet per-dispatch detail is not in the committed file, so this is reconciled by mtime arithmetic, not per file [INFERENCE: no deletions between snapshots, which the counts are consistent with].

### 3.2 Other 18 waves

Members, per-member statuses, missing-name sets, and dispatch hashes are identical to GT Appendix A/B and to the oracle. No difference to explain.

### 3.3 JSON discovery counts (ignored_json and total JSON)

GT: 296 JSON = 19 dispatch + 276 ignored + 1 unreadable. Now (E): 420 = 19 + 400 + 1.
- 125 JSON files were born after the GT scan (birth time via `stat -c %W`; all 125 have mtime > 10:34:51Z; 0 pre-existing files were modified).
- Net +124 ignored = +125 births − 1 pre-GT non-dispatch JSON that no longer exists or was replaced. [INFERENCE: the GT recorded counts only, so that file cannot be named. It is not a dispatch file: all 19 dispatch hashes match, and the unreadable file is unchanged, `round-20/build/out/RegReceiptSixPin/nonjson.json`.]
- Tool discovery (the 1 unreadable file and 400 ignored) matches the oracle's walk exactly at every snapshot.

### 3.4 Deltas between runs (each mtime-attributed)

- scan.json (11:03:11Z) → oracle pass (11:05:27Z): +12 JSON files with mtime in (11:03:11, 11:05:27]; +2 members (3.1).
- A/B (11:06:03Z) → C (11:12:39Z): +1 JSON `round-21/recipe.json` (mtime 11:11:48Z). B and C are identical apart from `ignored_json`.
- C → D (11:14:11Z): +1 member RevengeSpliceOrigin (mtime 11:13:48Z); +1 JSON `round-21/runs/b76727f3/live-receipt.json` (mtime in the window).
- D → E (11:15:34Z): +1 JSON `round-21/runs/b76727f3/commands.json` (mtime 11:14:13Z).

## 4. Tool findings (line numbers for v6, c134c57b…; "HEAD" where v1 differs)

- **F1 (operational; reproduced).** `main` does not create the `--out` parent. The payload is built (tool:697) but on write failure the tool prints `cannot write --out` and returns 2 (tool:698-704) without emitting the JSON. Hit on the first assigned attempt. Not an accuracy issue; recommend creating the parent or documenting it.
- **F2 (latent; not triggered on kama).** `_dispatch_files` silently skips a `*.json` whose lstat fails with an error other than not-found (tool:116-119). Such a file is counted in neither `ignored_json` nor `unreadable_json`. Kama's totals close exactly (420 = 19 + 400 + 1 at E), so this branch was not hit.
- **F3 (latent; not triggered).** Any lstat error other than not-found or not-a-directory makes the report `unavailable` (tool:200). `_member_status` then maps it to `missing` (tool:246). A permission-denied report reads as missing, not as an error. The oracle saw no OSError on any kama report path.
- **F4 (ambiguity; not triggered on kama).** The misrooted check runs only when the lane kind is `missing` (tool:242). A lane path whose intermediate component is a regular file (kind `other`, tool:190) is `missing` with no misrooted check. Symlinked parents were `missing` until v4; R8 (tool:202-204, 233-234) now returns `unsafe`. Planted evidence: on v2, a regular fleet copy under a symlinked `round-11/advice` gave `missing` for `Measure`, which was the only mismatch (1 of 1198) in that run. On v4 all 32 members under that symlink are `unsafe`. The frozen contract reserves `unsafe` for traversal or escape; R8 is stricter (it rejects symlinks that resolve inside the lane). This is disclosed as R8.
- **F5 (contract deviation, disclosed as R2; not triggered).** `stub` is an exact-bytes match against `STATUS: started` or `STATUS: started\n` (`STUB_CONTENTS`; checked at tool:238-240). The frozen contract defines `present` as size > 0. A 17-byte start stub with an extra newline is `present` (planted case). No kama report is ≤200 bytes, so no kama count is affected.
- **F6 (doc drift; fixed in the working copy).** HEAD's header said "at most 64 bytes are read"; the code reads at most 16 (tool:238 `max(len(stub) …)`). v6 header (tool:10) says 16.
- **F7 (change control).** Five uncommitted edits after the commit, 11:04:26Z to 11:15:31Z (v2 to v6). Production-logic changes are R8 (v4) and the fleet-root `realpath` plus directory check (v6, tool:327-329, error at tool:694-695). The rest are docstrings, selftest cases, and the `name_hint` label (v5). Kama results are identical across v1, v2, v3, v4, and v6, apart from live-tree deltas (3.4).

## 5. Planted-state test on v4 (scratch copy; 1198 expectations)

I copied kama's 19 real dispatch files to `/tmp/livekama-plant4-*/lane` and planted report states on real member paths, with a regular fleet copy in `/tmp/livekama-plant4-*/fleet`. Expected statuses were computed independently of the tool. Result: **0 mismatches across 1198 members**. Outcomes:

- stub: KnowledgeSonameEntry (`STATUS: started\n`) and LessonDraftC2 (`STATUS: started`) → stub.
- ShonenMap (`STATUS: started\n\n`, 17 bytes) → present (F5).
- SimplifyAudit (0 bytes) → empty. ClosureNotesSweep (real file) → present.
- SkillRowAudit (final-component symlink) → missing. SkillRowLinks (directory at path) → missing.
- Classifier (round-14, regular fleet copy, lane missing) → misrooted. Fixtures (round-14, fleet symlink) → missing.
- First round-12 member, trailer `.ufo/../…` → unsafe. First round-13 member, trailer without a path → unparsed. First round-15/build member, CRLF trailer → resolves correctly (missing).
- 32 members under symlinked `round-11/advice` → unsafe (R8).
- Totals: present 2, stub 2, empty 1, misrooted 1, unsafe 33, unparsed 1, missing 1158 (sum 1198).

## 6. Verification gaps and residual risk

- The lane is live. Numbers hold at their timestamps only; E (11:15:34Z) is the latest state. Round-21 still has 5 missing.
- The fleet snapshot has totals only, so its agreement is shown by mtime arithmetic, not per file.
- One pre-GT non-dispatch JSON file is gone or replaced (3.3, [INFERENCE]).
- The oracle is my own code. It shares the contract's rules, not the tool's code. Where the contract is ambiguous (symlink, non-directory component, permission error), kama has no such case, so no kama verdict depends on those rules.
- v5 and v6 were not planted-tested. v6's change is fleet-root resolution; v6 selftest passes 23/23 and E = D on kama.
- GT's narrative (round-21 "never spawned", [INFERENCE]) is superseded by 81 present reports. I did not inspect spawn records (outside C2).
- Not run: `tools/mori-census.sh` (not requested); `frozen/c2-expected.json` (not opened; the selftest loads it).

## 7. Artifacts

- `falsify/LiveKama/scan.json` (assigned output, 11:03:11Z, v1), `scan-A.json` and `scan-B.json` (v2, 11:06:03Z), `scan-C.json` (v3), `scan-D.json` (v4), `scan-E.json` (v6, latest).
- `falsify/LiveKama/members-kama-r20.tsv`: 1198 rows; GT, fleet (derived), scan 11:03:11, and run D statuses, with report mtime and size.
- `/tmp/livekama-plant-*` (v2 planted run, F4 evidence) and `/tmp/livekama-plant4-*` (v4 planted run, 0 mismatches).

## 8. Tooling

No installs or updates. Used `python3` stdlib, `sha256sum`, `stat`, `/usr/bin/jq` (not used for final figures), and read-only `git --no-optional-locks` log/show/diff on the mori repo. No pacman, no mutating git or jj command, nothing run in the kama lane.
