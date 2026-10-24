VERDICT: PARTIAL. Per-dispatch-file accuracy HOLDS; lane coverage is BROKEN for round 24.

Per-dispatch-file accuracy HOLDS: the tool's 479-member output matches my independent recomputation on every member, and every difference from the 10:38:39Z ground truth (GtLaneKagi.md) or the committed snapshot (c2-live-fleet.json) is live round-25 completion or a tool error. Coverage is BROKEN: a 2-seat `fix` spawn in round 24 has no dispatch JSON, so C2 cannot see it, and both seats are recorded as executor deaths.

Seat MoriR20.LiveKagi (leaf, no subagents). Read-only on kagi-shokunin and the fleet. Writes: this report, and scratch `falsify/LiveKagi/` (`scan.json`, `scan-stdout.json`, `scan-rerun.json`, `oracle-rows.pkl`, `transitions-gt-to-now.tsv`). A `/tmp` fixture was created and removed. Installs or updates: none. "Tool" means `tools/mori-wave-settlement.py`; line refs are to that file.

## 1. Per-dispatch-file comparison

"Tool" = scan at 11:01:03Z (`scan.json`; byte-identical rerun at 11:06:08Z). "Oracle" = my independent recomputation (lstat, trailer rule, JSON census; no tool code imported).

| dispatch file (under `.ufo/waves/`) | members | GT 10:38:39Z present/missing | tool 11:01:03Z present/missing | tool state | oracle present/missing |
|---|---:|---:|---:|---|---:|
| round-22/build-dispatch.json | 64 | 60/4 | 60/4 | partial | 60/4 |
| round-22/falsify-dispatch.json | 66 | 66/0 | 66/0 | settled | 66/0 |
| round-23/falsify-dispatch.json | 64 | 64/0 | 64/0 | settled | 64/0 |
| round-23/parent-build-dispatch.json | 66 | 66/0 | 66/0 | settled | 66/0 |
| round-24/build-dispatch.json | 67 | 66/1 | 66/1 | partial | 66/1 |
| round-24/falsify-dispatch.json | 64 | 56/8 | 56/8 | partial | 56/8 |
| round-25/build-dispatch.json | 88 | 6/82 | 86/2 | partial | 86/2 |
| **lane** | **479** | **384/95** | **464/15** | 3 settled, 4 partial | 464/15 |

- `stub`, `misrooted`, `empty`, `unparsed`, `unsafe` are 0 in every row of GT, tool and oracle.
- GT states implied by its counts and the contract rule (`contract.md:78-81`, `tool:276-285`): 3 settled, 4 partial. Same as tool.
- Tool totals: `{"empty":0,"members":479,"misrooted":0,"missing":15,"name_hinted_waves":0,"present":464,"states":{"partial":4,"settled":3},"stub":0,"unique_dispatch_sha256":7,"unparsed":0,"unsafe":0,"waves":7}`; `ignored_json` 96 (= 103 − 7); `unreadable_json` 0.
- Committed `c2-live-fleet.json:246-258` (kagi row; file mtime 10:46:53Z): present 437, missing 42, misrooted 0, empty 0, unparsed 0, unsafe 0, unreadable_json 0, waves 7, exit 1. It has no per-file rows and no `stub` field, so per-file comparison is impossible. It has no kagi entry in `dispatch_filename_flags`, consistent with `name_hinted_waves` 0.
- Member level: tool vs oracle identical on name, agent and status for 479/479. Trailer selection: 0 differences between the tool's rule (`tool:208-209`, splitlines + fullmatch) and a `split("\n")` + prefix rule. No CR, VT, FF, U+0085, U+2028 or U+2029 appears in any task body. Each task has exactly one trailer line (histogram {1: 479}).

## 2. Differences, each explained

**D1. round-25 +80 present (GT to now).** Transitions GT to now: present to present 384, missing to missing 15, missing to present 80, present to missing 0, path mismatches 0. Per-member rows with mtimes: `falsify/LiveKagi/transitions-gt-to-now.tsv`. The 80 reports' mtimes run from 10:38:43Z to 11:02:37Z: 45 in (10:38:39Z, 10:46:53Z], 35 in (10:46:53Z, 11:02:37Z]; none is at or before 10:38:39Z. All 384 GT-present reports still exist with mtime at or before 10:38:39Z, so none was rewritten. Cause: live round-25 executors writing reports. Membership did not change: all seven dispatch JSONs predate the snapshot (latest `round-25/build-dispatch.json`, 10:31:38Z).

**D2. GT timeline cross-check (GtLaneKagi.md:58-59).** Consistent with mtimes. `round-25/build-dispatch.json` 10:31:38Z (GT: 07:31:38 -0300). `round-25/build-task-result.txt` and `build-refusals.json` both 10:35:04Z (GT: 07:35:04 -0300). The three GT reports "at 10:36:58Z" are ScribeReadmeFrontier 10:36:29Z, ScribeSkillRows 10:36:30Z and ScribeQuality 10:36:53Z. The other three are CritC3 10:37:13Z, ScribeLog 10:37:39Z and MutCitations 10:38:24Z.

**D3. lane total vs committed snapshot (384 to 437 to 464).** Bounds: present-now with mtime at or before 10:46:53Z is 429, so 429 <= 437 <= 464 holds. If no report was deleted, 53 became non-empty between 10:38:39Z and the snapshot, and 27 after it. [INFERENCE] Of the 53, 8 were later rewritten, so their mtime is after the snapshot; this cannot be observed because the committed row has no per-member data.

**D4. remaining 2 round-25 members** (`XReleaseClock`, `XMeasureC2`). Absent on disk, and absent at their exact relative path in all 21 committed-snapshot lanes. The coop roster at my start listed `KagiR25.XReleaseClock-2` as running. [INFERENCE] Still in flight.

**D5. tool error on the first run** (no count difference). Exit 2, "mori-wave-settlement: cannot write --out", no stdout, no file. Explained by F2.

## 3. Findings

**F1. Coverage BROKEN: the round-24 `fix` spawn is invisible to C2.**
- Spawn: `round-24/fix-task-result.txt:1` (mtime 09:17:34Z): "Spawned 2 background agents using executor": `KagiR24-2.FixGateConfinement`, `KagiR24-2.FixIdentityInstrument-2`.
- Outcome: `round-24/falsify-outcomes.json:512-514` lists both under `repair_executor_deaths`, "Retry budget exhausted after 5 retries ... turn_rate_limit_exceeded".
- The lane's own numeric keys (`falsify-outcomes.json?q=with_entries(select((.value|type)=="number"))`): `total_round_seats` 133, `wave1` 67, `wave2` 64, `ordinary_implementation` 2, `size` 64, `reported` 56, `dead` 8. 133 = 67 + 64 + 2. C2 covers 67 + 64 = 131. [INFERENCE] The size-64 block is the falsify wave; its 56/8 equals C2's present/missing for that wave.
- No output on disk: `round-24/fixes/` absent; `gate-confinement.txt` and `identity-instrument.txt` absent (`stat`).
- No dispatch JSON names them (name search under `kagi-shokunin/.ufo/waves`: hits only `falsify-outcomes.json:513-514` and `fix-task-result.txt:1`). Their task text says "report gate-confinement.txt beside it" with no `Report: write your scoped findings to` trailer, so the trailer rule (`tool:204-218`) could not parse them even if discovery reached them.
- Contract scope: discovery is `*.json` with schema `ufo-swarm-wave-dispatch-v1` (`contract.md:64-67`), so under the frozen rule this is out of scope. The problem statement describes this same failure: "Nothing in the lane counts which dispatched seats left their report" (`contract.md:51-54`). GT flagged it (`GtLaneKagi.md:76`); the tool does not address it.

**F2. Tool error: `--out` parent directory not created (`tool:670-676`).** `main()` opens `args.out` directly and returns 2 on OSError. Contrast `_write_json` (`tool:379-380`), which calls `os.makedirs`. Reproduced: exit 2, nothing written. Writes stay within `--out` (`contract.md:56-57`). Not an accuracy defect.

**F3. Residual: a lane with no wave tree exits 0.** Fixture `/tmp/c2-nowaves-lane` (no `.ufo`): `scan` gives EXIT=0 and `{"waves":0,"totals":{"members":0,...,"states":{},...}}`. Path: `_wave_root` returns None (`tool:81-84`), so `paths = []` (`tool:314-315`), and `rc = 0 if all([]) else 1` gives 0 (`tool:363`). This matches the letter of `contract.md:87-88` but is green on nothing. Not triggered on kagi (7 waves found).

**F4. Residual: co-evolved refinements vs the frozen contract.** R2 `stub` (`tool:225-228`, docstring `:9-10`) adds a status absent from the frozen list (`contract.md:74-75`). R1, R3, R4 and R5 are not in the frozen text. On kagi every refinement is inert: 0 stub files (smallest present file 2149 bytes; no present file begins with `STATUS:`); one trailer per task; `name_hint` null on 7/7; `duplicate_of` none; `duplicate_report_paths` 0; 479 unique report paths. Frozen-rule numbers equal the reported numbers.

**F5. Design gap: the registry is never read.** GT claims registry checks (`GtLaneKagi.md:49`). I verified them: registry member names equal taskCall names (7/7) and are unique; `counts.total` equals the member count; `resumeSends` is empty; `compaction.applied` is false; all trailers sit under `registry.reportDir` (7/7). The tool checks none of this, so a registry/taskCall divergence would be silent. No effect now.

**F6. Residual: lstat errors fold into `missing`.** `_inspect_report_path` returns "unavailable" on other OSError (`tool:191-192`); `_member_status` then returns "missing" for anything not regular and not misrooted (`tool:234`). Not observed on kagi (oracle: 0 errors).

## 4. Commands and results
1. `python3 tools/mori-wave-settlement.py scan --lane-root .../kagi-shokunin --fleet-root .../shokunin --out .../falsify/LiveKagi/scan.json`. First attempt: EXIT=2 (stderr "cannot write --out"). Second attempt after `mkdir -p falsify/LiveKagi`: EXIT=1.
2. Rerun to `scan-rerun.json` (11:06:08Z): EXIT=1. `cmp scan.json scan-rerun.json` identical; `scan-stdout.json` identical to `scan.json`. The byte-identity clause holds (`contract.md:85-86`).
3. Oracle census (Python, lstat, JSON with NaN rejected): 103 `*.json` under `.ufo/waves` = 7 dispatch + 7 registry + 82 no-schema + 1 numeric + 6 array; 0 symlinks, 0 non-regular, 0 parse errors. GT's jq census agrees (GtLaneKagi.md:18-25).
4. Sibling-lane check: 21 lanes from `c2-live-fleet.json` `lanes[]` x 15 still-missing relative paths, exact `lexists`: 300 checks, 0 hits. Fleet root: 0 hits.
5. Fixture (F3): EXIT=0. Removed afterwards.

## 5. Verification gaps
- Basename or alternate-path misroutes were not swept. GT's fleet-wide basename search (GtLaneKagi.md:62-64) was not re-run, since fleet-wide globs are out of bounds. [INFERENCE] None exist.
- Non-JSON spawns were searched only under `kagi-shokunin/.ufo/waves` (name search for the two fix seats). Spawn records elsewhere were not searched.
- Per-member status in the committed snapshot is unrecoverable. The bounds check is consistent but is not a per-member proof.
- Timing: all "now" values are as of 11:01:03Z. Statuses were unchanged at the 11:06:08Z rerun. One report was rewritten at 11:02:37Z with no status change. Round-25 is still running.
- `mori-census.sh` was not run (not requested).

## 6. For the main agent
1. Decide how C2 treats spawns without a dispatch JSON (F1). Until then kagi's round-24 undercounts 2 seats that both died. "479" is the JSON-discovered member count, not the lane's spawned-seat count, which is at least 481 with the two fix seats.
2. Add a zero-wave guard (F3).
3. Create the `--out` parent, or document that it must exist (F2).
4. Re-scan kagi after round-25 finishes; 2 members are still missing.
5. If per-file pins are needed, the committed fleet snapshot must record per-wave rows.
