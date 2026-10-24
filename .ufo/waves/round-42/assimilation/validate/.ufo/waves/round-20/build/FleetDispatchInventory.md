# FleetDispatchInventory, round 20 (MoriR20.FleetDispatchInventory)

Result: complete. Read-only inventory of `ufo-swarm-wave-dispatch-v1` JSON across the `*-shokunin` lanes. The lanes were still writing while I ran (section 6), so every number is the snapshot at `generated_utc` 2026-10-21T10:36:16Z.

## 1. Artifacts

- `mori-shokunin/.ufo/waves/round-20/build/FleetDispatchInventory/inventory.json`: one row per dispatch file (196 rows: `path`, `sha256`, `wave`, `task_count`, `resume_count`, plus `lane`, `lane_path`, `bytes`, `task_call`, `resume_sends`, `counts`, `registry_report_dir`, `duplicate_of`, `checks`), per-lane summaries, totals, outside-glob rows, edge cases. Schema `mori-fleet-dispatch-inventory-v1`.
- `mori-shokunin/.ufo/waves/round-20/build/FleetDispatchInventory/scan.py`: stdlib Python 3 scanner that produces that file. `python3 scan.py --out FILE` (default root is the fleet root). It writes nothing except `--out`.
- This report.

## 2. Bottom line

- 196 dispatch-schema files in 15 lanes, 144 distinct byte contents. Declared tasks: 12,307. Counting each distinct content once: 9,198.
- Resume count is 0 everywhere. `counts.resume` is 0 in all 196 files, `resumeSends` is empty in all 193 files that carry the key, and all 12,307 registry members are `kind: spawn`.
- No dispatch has `taskCall: null` (the contract's `no-spawn` case). Three tabi validation records have no `taskCall` key at all.
- 19 dispatch files have a null `wave`: 16 in kama, 3 in tabi clone trees.
- Tabi holds three nested lane-like clones under `.ufo/waves/round-20/final-clones/` (ExecCounter, ExecFixtures, ExecFrozen), each with a `.git` entry and a `.ufo/` directory (section 5, F4). Together they account for 51 of the 196 dispatch files, 2,925 of the 12,307 declared tasks and 4,935 JSON files anywhere under the three trees. The contract's discovery rule counts them. Whether they belong in fleet-wide totals is an L1 decision; I changed nothing.

## 3. Method (exact rules are also in inventory.json `method`)

- Lanes: directories matching `*-shokunin` directly under the fleet root (not symlinks, not dot-prefixed). 21 matches; 16 have `.ufo/waves`.
- Walk `<lane>/.ufo/waves` with `os.walk(followlinks=False)`. Candidates are regular files named `*.json`. Symlinks are recorded and not followed (`contract.md:64-67`).
- Member: top-level JSON object whose `schema` equals `ufo-swarm-wave-dispatch-v1`. Other parseable JSON counts as `ignored_json`; unparseable counts as `unreadable_json`.
- Fields: `wave` = top-level `wave` (null if absent or JSON null). `task_count` = `len(taskCall.tasks)`, 0 when `taskCall` is null, null when the key is missing. `resume_count` = `counts.resume`. `resume_sends` = `len(resumeSends)`. `sha256` = over the raw bytes read.
- Dispatch shape, read from `mori-shokunin/.ufo/waves/round-19/wave2-run.json` and `round-13/dispatch.json`: top-level keys `schema, wave, policy, counts, registry, compaction, taskCall{context,tasks}, resumeSends, note`.

## 4. Lane totals (snapshot 10:36:16Z)

| lane | JSON | dispatch | distinct content | declared tasks | distinct-content tasks | tasks min–max | resume | resumeSends | wave null | flagged | unreadable JSON | JSON symlinks | other symlinks | non-JSON schema mentions | JSON mentions (not top-level) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| chousa-shokunin | 13 | 2 | 2 | 136 | 136 | 68–68 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| kagi-shokunin | 103 | 7 | 7 | 479 | 479 | 64–88 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 |
| kaidoku-shokunin | 3411 | 14 | 14 | 959 | 959 | 32–100 | 0 | 0 | 0 | 0 | 39 | 0 | 11 | 1 | 0 |
| kake-shokunin | 177 | 5 | 5 | 325 | 325 | 64–69 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| kama-shokunin | 296 | 19 | 19 | 1198 | 1198 | 32–95 | 0 | 0 | 16 | 16 | 1 | 0 | 0 | 5 | 3 |
| kasegi-shokunin | 13 | 1 | 1 | 64 | 64 | 64–64 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| kengaku-shokunin | 17 | 5 | 4 | 387 | 315 | 64–92 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| kumitate-shokunin | 33 | 6 | 6 | 512 | 512 | 68–96 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 |
| lore-shokunin | 1102 | 0 | 0 | 0 | 0 | – | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| mado-shokunin | 428 | 16 | 16 | 1030 | 1030 | 32–88 | 0 | 0 | 0 | 0 | 2 | 0 | 11 | 1 | 0 |
| mori-shokunin | 480 | 11 | 11 | 671 | 671 | 32–76 | 0 | 0 | 0 | 0 | 2 | 0 | 4 | 34 | 3 |
| revenger-shokunin | 9 | 1 | 1 | 32 | 32 | 32–32 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| souji-shokunin | 55 | 12 | 12 | 783 | 783 | 32–91 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| tabi-shokunin | 5160 | 67 | 17 | 3932 | 967 | 32–86 | 0 | 0 | 3 | 3 | 0 | 3 | 3 | 4 | 0 |
| tameshi-shokunin | 106 | 16 | 15 | 965 | 893 | 32–99 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| tsukuroi-shokunin | 227 | 14 | 14 | 834 | 834 | 32–81 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| **total, 21 lanes** | **11630** | **196** | **144** | **12307** | **9198** | **32–100** | **0** | **0** | **19** | **19** | **45** | **3** | **29** | **46** | **7** |

- Column notes: "distinct content" counts byte-identical files once. "tasks min–max" covers `task_call: ok` files only. "flagged" counts dispatch files with at least one consistency flag.
- Lanes with no `.ufo/waves`: audio-shokunin, game-dev-2d-shokunin, game-dev-3d-shokunin, kotodama-shokunin (no `.ufo` at all), kotoba-shokunin (has `.ufo`, no `waves`).
- Outside the glob, reported separately: `tameshi-shokukin/` (misspelled name; no regular files anywhere under it) and its nested `tameshi-shokunin/` (same). Zero JSON in both. Not merged into any total.
- Per-lane sums were re-added: dispatch 196, declared tasks 12,307, distinct content 144 (the per-lane distinct counts sum to 144, so no byte-identical content crosses lanes).

## 5. Findings

F1. **Resume: none recorded.** [observed] `jq` totals: `resume_total` 0, `resume_unknown` 0, `resumeSends` entries 0. Registry member kinds across all dispatch files: `12307 spawn`, no `resume` kind. Whether resumes are logged elsewhere is [INFERENCE] not checked; I did not read `.ufo/state` or session logs.

F2. **No-spawn dispatches: none.** [observed] `taskCall: null` appears in 0 files. Three tabi clone files have no `taskCall` key (`task_call: missing`). Their `counts.total` is 32 each, so Σ`counts.total` = 12,403 against Σ`task_count` = 12,307. The difference is exactly 3×32. The contract defines only `taskCall: null` → `no-spawn` (`contract.md:68-69`). The missing-key case is not defined there. [observed gap]

F3. **Null `wave`: 19 files.** [observed]
- kama (16), all under `kama-shokunin/.ufo/waves/`: `round-12/dispatch.json`, `round-13/dispatch.json`, `round-14/dispatch.json`, `round-15/build/dispatch.json`, `round-15/falsify/dispatch.json`, `round-16/build/dispatch.json`, `round-16/falsify/dispatch.json`, `round-17/build/dispatch.json`, `round-17/falsify/dispatch.json`, `round-18/build/dispatch-95.json`, `round-18/build/dispatch.json`, `round-18/falsify/dispatch.json`, `round-19/build/dispatch.json`, `round-19/falsify/dispatch.json`, `round-20/build/dispatch.json`, `round-21/build/dispatch.json`.
- tabi (3): the `wave-validation.json` files in the three clone trees (F2).
- kama `round-20/falsify/dispatch.json` has `wave: "falsify"`, which is a role label, not a wave identifier. Apart from `registry.reportDir` (kept as `registry_report_dir`), the null-wave files carry no wave identifier.

F4. **Three nested lane-like clones inside tabi's waves tree.** [observed] `tabi-shokunin/.ufo/waves/round-20/final-clones/{ExecCounter,ExecFixtures,ExecFrozen}/`. ExecCounter's top level (`ls -la`) contains `.git`, `.ufo`, `AGENTS.md`, `LOG.md`, `SKILL.md`, `corpus`, `plans`, `reports`, `scripts`. Each clone tree holds 1,645 JSON files anywhere under it (not only under `.ufo/waves`), 17 dispatch-schema files and 975 declared tasks. For comparison, native tabi `.ufo/waves` outside `final-clones` holds 225 JSON files, 16 dispatch files and 1,007 tasks. Directory mtimes (local, UTC-3): ExecFrozen 07:25 (10:25Z), ExecFixtures 07:27 (10:27Z), ExecCounter 07:34 (10:34Z). ExecCounter did not exist in the 10:32:27Z snapshot (section 6). The clones were still being written during the run.

F5. **Byte-identical duplicates.** [observed] 196 files, 144 distinct contents. Groups, each listed by path in `inventory.json` `dispatches[].duplicate_of`:
- tabi: 15 of the 16 native dispatch files have byte-identical copies in the clone trees; the exception is `round-20/w2/dispatch.json` (64 tasks). Example: `tabi-shokunin/.ufo/waves/round-13/w1/dispatch.json` equals `round-20/final-clones/{ExecCounter,ExecFixtures,ExecFrozen}/.ufo/waves/round-13/w1/dispatch.json`. Also `round-19/w2/dispatch.json` equals `round-19/w2/validation.json` within the native tree.
- kengaku: `round-26/build-dispatch.json` equals `round-26/build-registry-rebuild.json` (both wave `kengaku-r26-build`, 72 tasks).
- tameshi: `round-20/run1.json` equals `round-20/validation-current.json` (both `tameshi-r20-w1`, 72 tasks).

F6. **Wave values are not unique.** [observed] 17 wave values occur in more than one file: tabi 15, kengaku 1 (`kengaku-r26-build`), tameshi 1 (`tameshi-r20-w1`). Anything keyed on `wave` alone will collapse them. Key on `path`.

F7. **Validation-named files that carry the dispatch schema.** [observed] 45 files: tabi 43, kake 1 (`kake-shokunin/.ufo/waves/round-21/wave1-validation.json`, wave `kake-r21-build`, 64 tasks), tameshi 1 (`tameshi-shokunin/.ufo/waves/round-20/validation-current.json`). Each has the dispatch schema at top level, so the discovery rule counts it.

F8. **Internal consistency.** [observed] For all 196 files: `counts.total` equals `len(taskCall.tasks)` in 193 of 193 files that have a `taskCall`. `counts.spawn + counts.resume = counts.total` in 196 of 196. `len(registry.members)` equals the task count in 193 of 193. All 12,307 tasks carry `name`, `agent` and `task`. No file has duplicate task names. Per-file task counts range 32 to 100.

F9. **Symlinks (not followed).** [observed]
- JSON symlinks, 3 total: `…/final-clones/<tree>/corpus/evidence/round-19/validation/selftest-hardening/case-symlink/cases/alias.json -> ../target.json`, one per clone tree. The target's schema is `tabi-webmcp-validation-cases-v1`, not dispatch, so following these links would change no count.
- Other symlinks, 29 total: kaidoku 11 (including two self-referential `symlink-loop` links), mado 11 (including `round-17/tripwire/hardening/symlink-target.jsonl -> /etc/hostname`), mori 4 (under `round-17/fixtures/seat/`), tabi 3.
- No lane has a symlinked `.ufo` or `.ufo/waves`.

F10. **Unreadable JSON: 45.** [observed] kaidoku 39, mado 2, mori 2, kama 1, lore 1. None contain the schema bytes. The set mixes tool output saved as `.json` (for example `kaidoku-shokunin/.ufo/waves/arc2-loop1-round6/receipts/big-leg-refusal-envelope.json` begins `error: Analysis failed`) with deliberately malformed fixtures (for example `kama-shokunin/.ufo/waves/round-20/build/out/RegReceiptSixPin/nonjson.json`, 8 bytes; `mado-shokunin/.ufo/waves/round-18/tripwire/frozen/malformed-expected-json/expected.json`).

F11. **Non-JSON files that contain the schema string: 46.** [observed] Not discovered by the rule. mori 34 (mostly round-20 candidate drafts and scripts under `build/`, including `build/FleetDispatchInventory/scan.py`, `build/ImplSettlement/tools/mori-wave-settlement.py`, `build/OracleHarness/c2-oracle.py`, and a `__pycache__/*.pyc`), kama 5, tabi 4, kaidoku 1, kumitate 1, mado 1.

F12. **JSON that mentions the schema but is not top-level: 7.** [observed] kagi 1 (`round-22/registry-correction-render.json`), kama 3 (`round-15/build/validation.json`, `round-15/falsify/validation.json`, `round-15/falsify/validation-final.json`), mori 3 (`round-20/wave1-spec.json`, `round-20/frozen/c2-expected.json`, and the earlier copy of this inventory, see F14). Counted as `ignored_json`.

F13. **Mori round 19 matches the contract's demo input.** [observed] `round-19/wave1-run.json` has 64 tasks. The contract's live demonstration uses round-19 wave 1 with 64 members (`contract.md:95-96`). Mori's full dispatch list: round-13 32, round-14 32, round-15 64, round-16 wave1 64, round-17 wave1 70 and wave2 64, round-18 wave1 68 and wave2 67, round-19 wave1 64 and wave2 70, round-20 wave1 76. Sum 671.

F14. **Self-reference.** [observed] `inventory.json` sits inside mori's `.ufo/waves` tree and contains the schema name. Later scans count it in `json_files` and in `json_mentions_nontop`. `scan.py` contains the schema literal too, so it appears in the non-JSON mention list. Neither is a dispatch file.

F15. **Out-of-glob and stray entries.** [observed] `tameshi-shokukin/` contains no regular files at all: its `.ufo/waves` and the nested `tameshi-shokunin/.ufo/waves` are directories only. `tameshi-shokukin/` and its nested `tameshi-shokunin/` have mtime 02:50 local today. The fleet root also contains an entry literally named `bash: ` (it contains `home/`). Neither is a lane. Neither holds dispatch JSON.

## 6. Snapshots and drift

| snapshot | time (UTC) | method | dispatch files | JSON files | declared tasks | non-JSON mentions |
|---|---|---|---|---|---|---|
| A | 10:29:31 (per-lane `find`) and 10:30:34 (scan) | ad hoc Python | 178 | 9,977 | 11,244 | 20 |
| B | 10:32:27 | ad hoc Python | 179 | 9,980 | 11,332 | 24 |
| C (inventory.json) | 10:36:16 | scan.py | 196 | 11,630 | 12,307 | 46 |

- A to B: `kagi-shokunin/.ufo/waves/round-25/build-dispatch.json` appeared (wave `kagi-r25-build`, 88 tasks, sha256 `2fe68f5c…7e3532`).
- B to C: 17 dispatch files appeared, all under the ExecCounter clone, along with 1,645 JSON files. Tabi JSON went from 3,515 to 5,160.
- Per-file content did not change in either interval: no sha256 that existed in an earlier snapshot changed.
- Mori JSON count: 474, 477, 480 (same three times). Kagi: 98, 98, 103. Kama: 293 then 296, unchanged after.
- Snapshot C is internally consistent. Each `sha256` was checked against `sha256sum` right after the scan (section 7).
- Totals from a later run will differ. Re-run `scan.py` for current numbers.

## 7. Verification performed

1. `python3 scan.py --out inventory.json` (Python 3.14.8, stdlib, 3.67 s wall): exit 0, 21 lanes, 196 dispatch rows.
2. `diff` of `sha256sum` over all 196 listed paths against the `sha256` field: identical for 196 of 196.
3. Independent re-derivation with `jq` over each dispatch path (wave, `taskCall` length, `counts.resume`, `resumeSends` length) against the inventory fields: identical for 196 of 196. Note: the `jq` on PATH is jaq 3.1.1 (`jq --version` prints `jaq 3.1.1`), not canonical jq.
4. Totals re-added with `jq`: declared tasks 12,307; distinct sha256 144; resume 0; resumeSends 0.
5. Consistency checks listed in F8. Symlink check: no `.ufo` or `.ufo/waves` symlinks in any lane.
6. Not run: census, builds, tests, linters, git or jj commands.

## 8. Limits and [INFERENCE]

- Snapshot only. Lanes were writing during the run (section 6). Per-file rows and totals are exact for snapshot C; anything after 10:36:16Z is not represented.
- "Resume" here is the declared `counts.resume` plus `resumeSends`, both zero. That the fleet records no resumes anywhere is [INFERENCE], not established.
- `task_count` is the declared `taskCall` length. It was not checked against spawned seats. [INFERENCE] The C2 member count will match it, based on `contract.md:68`.
- Whether the three clone trees belong in fleet-wide totals follows the contract's discovery rule. Excluding them gives 145 dispatch files and 9,382 declared tasks. That view is shown only for the decision; I did not change the rule.
- Each clone tree has a `.git` entry (checked with `test -e`). I ran no git command in any of them.

## 9. Tooling and bounds

- No installs or updates were made. Tools used: python3 3.14.8 (stdlib only), `sha256sum`, jaq 3.1.1 (invoked as `jq`), `find`, `du`, `ls`, `stat`, `xargs`, `diff`, `sort`, `uniq`, `wc`, `paste`, `cat`. Three shell calls also used `grep -n`, `sed -n` and `awk` only to print lines; no edits were made through them.
- Writes: only under `mori-shokunin/.ufo/waves/round-20/build/`. Files: `FleetDispatchInventory.md` (this report, overwriting the status line), `FleetDispatchInventory/inventory.json`, `FleetDispatchInventory/scan.py`.
- Reads: lane `.ufo/waves` trees; `mori-shokunin/.ufo/waves/round-20/contract.md`; read-only grep hits in `scripts/`, `templates/`, `mori-shokunin/tools/` and `MANIFEST.json`. No `~/.omp` session logs, no retained transcripts, no lane file edits, no git or jj commands, no census run.
- Lane bounds: leaf seat, no subagents.
- Suggested next step for L1: decide whether the tabi `final-clones` trees count toward the fleet total, then re-run `python3 mori-shokunin/.ufo/waves/round-20/build/FleetDispatchInventory/scan.py --out <file>` against the frozen tree.
