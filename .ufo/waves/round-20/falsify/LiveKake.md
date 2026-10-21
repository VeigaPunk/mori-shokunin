HOLDS: for kake-shokunin, every per-file count, state, missing set, dispatch digest and member status from the fresh scan equals the wave-1 GT, an independent recomputation, and the committed fleet lane totals. Scope is kake only. Five tool defects (T1-T5, section 5) are residual risk; none changes a kake count. T1 (absent or symlinked wave root gives silent exit 0) matters for other lanes.

# LiveKake: C2 accuracy on kake-shokunin (falsify, round 20)

## 1. What was run (read-only)

| Step | Command or source | Result |
|---|---|---|
| Required scan | `python3 /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-wave-settlement.py scan --lane-root /home/vgpnk/Projects/shokunin/kake-shokunin --fleet-root /home/vgpnk/Projects/shokunin --out .../falsify/LiveKake/scan.json` | exit 1; scan.json mtime 11:00:30Z |
| Rerun, same arguments | `--out .../falsify/LiveKake/scan-rerun.json` (mtime 11:09:41Z) | exit 1; `cmp` identical to scan.json |
| Final run, current working copy | `--out .../falsify/LiveKake/scan-final.json` (after 11:11:12Z) | exit 1; `cmp` identical to scan.json |
| Independent oracle | `falsify/LiveKake/oracle.py`, no import of the tool; output `falsify/LiveKake/oracle.json` | exit 0 (second run; see D2) |
| Committed tool blob | `git cat-file -p 2eeae048:tools/mori-wave-settlement.py \| sha256sum`; same for `HEAD` (`git rev-parse --short HEAD` = 8f8c58e) | both `c6e6091937e4bcb02775cea81ce33990924c6e27487a6ce255d2959d94f4e795`, 28261 bytes |
| Tool file state | `stat`, `sha256sum`, `diff -u` committed copy vs working copy (`/tmp/liveKake-tool-diff.txt`) | section 4 |
| Edge fixtures | four temp lanes under /tmp, run against committed blob and working copy (eval, python subprocess) | section 5, T1 |
| Lane counts | `find .ufo/waves -name '*.json' -type f \| wc -l` = 177; `find .ufo/waves -type l \| wc -l` = 0 | matches tool and oracle |

Tool version for the required scan: committed blob c6e6 (equal to 2eeae04 and HEAD). Its file mtime was 10:45:51Z, and it was unchanged at 11:03:31Z when sha was read. The scan ran at 11:00:30Z, so it used c6e6 [INFERENCE from mtime and sha; blob equality observed].

## 2. Per-dispatch-file comparison

Columns: tool `scan.json` = oracle = GT (GT §2 table, §4 name lists).

| # | Dispatch file (under `.ufo/waves/`) | members | present | missing | misrooted | stub | empty | unsafe | unparsed | state | vs GT | vs oracle |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | round-21/wave1-validation.json | 64 | 64 | 0 | 0 | 0 | 0 | 0 | 0 | settled | equal | equal |
| 2 | round-22/w1-dispatch.json | 64 | 60 | 4 | 0 | 0 | 0 | 0 | 0 | partial | equal | equal |
| 3 | round-22/w2-dispatch.json | 64 | 43 | 21 | 0 | 0 | 0 | 0 | 0 | partial | equal | equal |
| 4 | round-23/w1-dispatch.json | 69 | 69 | 0 | 0 | 0 | 0 | 0 | 0 | settled | equal | equal |
| 5 | round-23/w2-dispatch.json | 64 | 25 | 39 | 0 | 0 | 0 | 0 | 0 | partial | equal | equal |
| | Lane | 325 | 261 | 64 | 0 | 0 | 0 | 0 | 0 | 2 settled, 3 partial | equal | equal |

Lane row against the committed fleet scan (`evidence/c2-live-fleet.json`, kake entry at lines 274-278 and nearby): exit 1, members 325, present 261, missing 64, misrooted 0, unparsed 0, unsafe 0, empty 0, waves 5, unreadable_json 0. All equal.

The committed fleet file has no per-file kake rows. Its only kake-specific per-file data is one `dispatch_filename_flags` entry (round-21). A per-file comparison against that file is therefore impossible. Per-file comparison used GT and the oracle.

Further checks, all equal:
- Discovery: 177 regular `*.json` under `.ufo/waves` (find 177, oracle 177) = 5 dispatch + 172 ignored (tool `ignored_json` 172, oracle 172). Unreadable 0. Symlinks 0.
- Member statuses: 325 of 325 match, per (wave, name), between scan.json and oracle.
- Member `agent` fields: 325 of 325 match.
- Dispatch digests: scan `dispatch_sha256` equals sha256 of the raw bytes for all 5 files (round-21 57b04379..., round-22/w1 517d3821..., round-22/w2 17a7236d..., round-23/w1 a8d68851..., round-23/w2 780e6481...).
- Missing-name sets: equal to GT §4 for round-22/w1 (4), round-22/w2 (21) and round-23/w2 (39), by set equality in the oracle (`gt_checks`). GT role counts reproduce: round-22/w2 reviewer 9, scout 8, connector 4; round-23/w2 reviewer 29, scout 9, connector 1; round-22/w1 scribe 4.
- Stub boundary: the smallest present report is 2187 bytes (oracle `present_min_size`). No present report begins with `STATUS: started`. The 16-byte stub guard cannot misclassify any kake report.
- Trailers: for all 325 members the trailer is the last non-blank line, and strict and lenient parses agree.
- Determinism: three runs (scan, rerun, final) are byte-identical.

## 3. Differences and their explanation

| ID | Where | Observed | Explanation | Class |
|---|---|---|---|---|
| D1 | round-21/wave1-validation.json, `name_hint` | scan says `undispatched-name:validation`; keyword is `validation` | Label prefix is hard-coded for every keyword: committed `tools/mori-wave-settlement.py:298` (working copy `:302`) | Tool label error (T2) |
| D2 | oracle run 1 | 3 false rows `oracle-missing-without-GT-list` (round-22/w1, round-22/w2, round-23/w2) | My harness compared GT key `round-22/w1` with file key `round-22/w1-dispatch.json`. Fixed; run 2 shows GT set equality 3 of 3 | Harness bug (mine). Not tool, not lane |
| D3 | GT §5 successors | 17 round-22/w2 names have same-named reports under `round-23/w1/` (mtimes 07:00:44Z to 07:15:28Z). Attack23 has `round-23/w1/Attack23WrongHost.md`. ReopenGoogleTroubleshoot, ReopenPythonURL and ReopenRFC6596 have none. The tool counts all 21 as missing | The frozen C2 definition has no successor link, and the tool follows it. Not a count error. The round-23/w1 task text says it carries the round-22 seat [observed text, run state not verified] | By design (limit) |
| D4 | committed fleet file | no per-file kake rows | Evidence limit | Not a difference |
| D5 | tool file during this run | working copy changed at 11:04:26Z and 11:11:12Z | Section 4. No kake output changed | Live change of the tool |

There is no count, state, missing-set or member-level difference between scan, oracle, GT and the committed lane totals.

## 4. Live changes since the snapshot (fleet scan 10:46:50Z)

Kake lane:
- 622 entries (directories and files) under `.ufo/waves` were lstat-checked. Zero have mtime after 10:46:50Z. Newest entry: `round-23/` at 2026-10-21T09:00:14Z (from `round-23/recovery-final-misroot.json`), 6395 s before the snapshot.
- Dispatch files: round-21 08:54:42Z; round-22/w1 21:33:31Z (10-20); round-22/w2 21:54:05Z (10-20); round-23/w1 06:38:20Z; round-23/w2 07:29:35Z. All predate the GT (10:37:11Z) and the snapshot.
- Every present report is newer than its dispatch file (oracle `present_older_than_dispatch` = []).
- No kake lane change after the snapshot was observed.

Tool (mori lane, `tools/mori-wave-settlement.py`):
- Committed blob c6e6 (= 2eeae04 = HEAD 8f8c58e). File mtime 10:45:51Z until 11:04:26Z. This is the version that produced scan.json.
- 11:04:26Z: sha `e5c06dad076b8e5aebbebcd53cf7c32de41592b4899319502b8cca003d4b8a48`, 28797 bytes (observed 11:10:40Z, mtime unchanged since 11:04:26Z).
- 11:11:12Z: sha `203c716e1dc55fa6ac912335e15516c63a46d4d4bc7f6cd9554a2e45212061a9`, 28880 bytes (current at report time).
- Diff from committed to current (39 lines): R2 doc changed from "64 bytes" to "16 bytes"; an R6/R7 doc note was added; a selftest case `r7-dotdot-inside-lane` and its fixture were added. No hunk changes scan logic. Its `..` rejection (committed `:159`) already existed.
- Output identity: scan.json (c6e6) = scan-rerun.json (e5c06 state) = scan-final.json (203c7 state), all byte-identical.
- The e5c06 content was not copied. [INFERENCE: the 11:09:41Z rerun read the 11:04:26Z version, since its mtime did not change until 11:11:12Z.]
- Who edited the tool: unobserved.

## 5. Tool defects (residual risk)

Line numbers are for the committed blob c6e6 unless marked as the working copy.

- **T1 (medium, silent false-clean).** `_wave_root` returns None for an absent `.ufo` or `.ufo/waves`, for a non-directory, and for a symlink (committed `:79`, `:84`, `:87-88`). With zero waves, `rc = 0 if all(...)` is true (`:363`). Fixtures, identical on committed blob and working copy:
  - control (real directory, one dispatch with a missing report): rc 1, `unsettled`, missing 1;
  - no `.ufo`: rc 0, waves 0;
  - `.ufo` symlink to a store holding that dispatch: rc 0, waves 0;
  - `.ufo/waves` symlink: rc 0, waves 0.
  Not triggered by kake: `.ufo` and `.ufo/waves` are real directories and 177 JSON files were seen. The frozen text makes a zero-wave exit 0 vacuously true, so this is a contract-level gap [INFERENCE on intent]. L1 should adjudicate.
- **T2 (low, label).** `:298` (working copy `:302`) builds `"undispatched-name:" + keyword` for all four keywords. A `validation`-named file is labelled "undispatched" even though GT §6 and its 64 present reports show dispatch.
- **T3 (low, semantics).** The `missing` list (`:287`) includes every non-present status (empty, stub, misrooted, unsafe, unparsed). `counts.missing` (`:271`) counts only `missing`. These differ whenever another status occurs. Not triggered by kake: all four are 0.
- **T4 (low, latent).** `_dispatch_files` (`:108-111`) silently drops a `*.json` entry whose lstat raises an OSError other than FileNotFound. It is counted in neither `ignored_json` nor `unreadable_json`. Not triggered: 177 = 172 + 5.
- **T5 (doc; fixed in working copy).** Committed `:10` says "at most 64 bytes are read". The code reads only files of at most 16 bytes (guard `:226`, read `:144`). Working copy line 10 now says 16.

## 6. Lane records consulted (context for "missing"; the tool does not read them)

- `round-22/w1-deaths.json`: `dead` = RegistryDraft, Knowledge, LessonDraft, TrendDraft; error 429 rate limit; `credited` false; `replaced` false. Same four names as the tool's missing set.
- `round-23/w2-deaths.json`: 39 entries; name set equal to the 39 missing round-23/w2 names (oracle check); all `credited` false and `replaced` false.
- `round-23/w2-jobcap.json`: `refusedTries` [1], `grantedTry` 2.
- `round-23/residual-deaths.json`: cites a `~/.omp` session file. I read only this lane record and did not open the cited file.
- No death record in `.ufo/waves` names the 21 round-22/w2 missing seats (name search over `.ufo/waves` JSON files containing death, jobcap or residual).
- The tool makes no dead or never-ran classification, by design.

## 7. Bounds and records

- Read-only on the lane. Writes only under `falsify/LiveKake/` and `/tmp/liveKake-*`.
- Git: only `git rev-parse` and `git cat-file -p`, which do not touch the index or worktree. No mutating git or jj command.
- Not opened: `.ufo/interactive-sessions/`, `.ufo/worktrees/`, `.jj/`, any `~/.omp` session file.
- Not run: `mori-census.sh`, the tool's `--selftest`, any build or test.
- Leaf seat: no subagents. Tool installs or updates: none (python3 stdlib, git read-only).
- Unverified: dispatch-schema JSON outside `.ufo/waves` (outside the frozen discovery scope; whole-lane search forbidden). [INFERENCE: none affects these counts.]
- Report content correctness: not judged (frozen contract).
