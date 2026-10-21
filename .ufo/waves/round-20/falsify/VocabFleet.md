# VocabFleet falsification: "never says dead / failed / killed" (mori-wave-settlement)

**PARTIAL**

- **Holds, live:** 0 of 40,923 tool-owned strings (keys plus state/status/schema/name_hint values) across 21 lanes, 148 waves and 9,453 members contain `dead|failed|killed`. No scan-mode line of the tool contains the triad.
- **Broken as a tested guarantee:** the only vocabulary assertion (`no_vocab`) runs on a fixture where no seat is missing. A mutant that emits `failed` on every missing seat passes `--selftest` 23/23 and emits 88 tool-owned triad strings on the live mori lane.
- **Not literally true of the whole output:** `--selftest` prints `failed` as a count label. Dispatch-authored text is echoed verbatim (24 live occurrences, out of search scope per the brief). An object-valued dispatch field can inject an output key named `failed`.

## 1. Setup

- Tool under test: `mori-shokunin/tools/mori-wave-settlement.py`, sha256 `5027bdc7d788301f2ed4dc2529d5dd2d9ea012999954f959d6ccd9988aac8447`. Stable across the final run. It changed twice during this run, see section 5.
- Frozen oracle: `mori-shokunin/.ufo/waves/round-20/frozen/c2-expected.json`, sha256 `0984806922da727a02a7944c00154df7a5aaff356c91c6fb36f47467c4f7d2af`. Unchanged across the whole run.
- Snapshot: final capture at 2026-10-21T11:13:43Z.
- Lanes: the 21 `*-shokunin` directories, non-recursive.
- Command per lane (read-only, stdout captured, no `--out`):
  `python3 mori-shokunin/tools/mori-wave-settlement.py scan --lane-root <lane> --fleet-root /home/vgpnk/Projects/shokunin`
  Exit codes: 15 lanes rc 1, 6 lanes rc 0, 0 lanes rc 2. Stderr was 0 bytes in every lane.
- **Tool-owned scope:** every key at every depth, plus string values of `schema`, `state`, `status`, `name_hint`.
- **Excluded scope (dispatch-authored or path data):** values and keys under `wave`, `name`, `agent`, `missing`, `dispatch_path`, `dispatch_sha256`, `duplicate_of`, `lane_root`.
- **Pattern:** case-insensitive substring `dead|failed|killed`. Correction: my first pass used word boundaries (`\b...\b`). That misses `failed_count` and reported 0 raw hits. The substring pass finds 24 raw hits, all in the excluded scope. I used substring for every reported number.
- **Self-checks:** tool hits + echo hits = raw hits in every lane (asserted, passed). The pattern fires on the selftest's `failed` label (positive control).

## 2. Counts (final snapshot)

| lane | rc | waves | members | non-present | tool-owned strings | tool-owned hits | echo hits | ignored_json | unreadable_json |
|---|---|---|---|---|---|---|---|---|---|
| audio-shokunin | 0 | 0 | 0 | 0 | 19 | 0 | 0 | 0 | 0 |
| chousa-shokunin | 1 | 2 | 136 | 16 | 601 | 0 | 0 | 11 | 0 |
| game-dev-2d-shokunin | 0 | 0 | 0 | 0 | 19 | 0 | 0 | 0 | 0 |
| game-dev-3d-shokunin | 0 | 0 | 0 | 0 | 19 | 0 | 0 | 0 | 0 |
| kagi-shokunin | 1 | 7 | 479 | 14 | 2063 | 0 | 0 | 96 | 0 |
| kaidoku-shokunin | 1 | 14 | 959 | 135 | 4109 | 0 | 7 | 3358 | 39 |
| kake-shokunin | 1 | 5 | 325 | 64 | 1412 | 0 | 0 | 172 | 0 |
| kama-shokunin | 1 | 19 | 1198 | 128 | 5156 | 0 | 4 | 398 | 1 |
| kasegi-shokunin | 1 | 1 | 64 | 20 | 294 | 0 | 0 | 12 | 0 |
| kengaku-shokunin | 1 | 5 | 387 | 11 | 1659 | 0 | 2 | 12 | 0 |
| kotoba-shokunin | 0 | 0 | 0 | 0 | 19 | 0 | 0 | 0 | 0 |
| kotodama-shokunin | 0 | 0 | 0 | 0 | 19 | 0 | 0 | 0 | 0 |
| kumitate-shokunin | 1 | 6 | 512 | 44 | 2177 | 0 | 1 | 27 | 0 |
| lore-shokunin | 0 | 0 | 0 | 0 | 19 | 0 | 0 | 1101 | 1 |
| mado-shokunin | 1 | 16 | 1030 | 116 | 4431 | 0 | 0 | 410 | 2 |
| mori-shokunin | 1 | 14 | 742 | 113 | 3243 | 0 | 6 | 702 | 3 |
| revenger-shokunin | 1 | 1 | 32 | 32 | 167 | 0 | 0 | 8 | 0 |
| souji-shokunin | 1 | 12 | 783 | 120 | 3370 | 0 | 0 | 43 | 0 |
| tabi-shokunin | 1 | 16 | 1007 | 116 | 4348 | 0 | 3 | 221 | 0 |
| tameshi-shokunin | 1 | 16 | 965 | 108 | 4170 | 0 | 1 | 90 | 0 |
| tsukuroi-shokunin | 1 | 14 | 834 | 66 | 3609 | 0 | 0 | 221 | 0 |
| **total** | rc0 6 / rc1 15 / rc2 0 | **148** | **9,453** | **1,103** (1,078 missing, 24 stub, 1 unsafe) | **40,923** | **0** | **24** | 6,882 | 46 |

- **Echo hits (24):** 23 in member `name` values, 1 in a `missing` list entry. Words: `dead` 21, `failed` 2, `killed` 1. Lanes: kaidoku 7, mori 6, kama 4, tabi 3, kengaku 2, kumitate 1, tameshi 1. Member names are not recorded here, per the brief.
- **Digest false positives:** `dispatch_sha256` is in the excluded scope, and a hex digest can contain `dead` as a substring. No such hit occurred live.

**Live tool-owned vocabulary** (closed; none contains the triad):
- Keys (32): agent, counts, dispatch_path, dispatch_sha256, duplicate_of, duplicate_report_paths, empty, ignored_json, lane_root, members, misrooted, missing, name, name_hint, name_hinted_waves, no-spawn, partial, present, schema, settled, state, states, status, stub, totals, unique_dispatch_sha256, unparsed, unreadable_json, unsafe, unsettled, wave, waves.
- Values (12): missing, mori-wave-settlement-v1, no-spawn, partial, present, settled, stub, undispatched-name:preview, undispatched-name:undispatched, undispatched-name:validation, unsafe, unsettled.
- Observed states: settled 82, partial 58, unsettled 7, no-spawn 1. Observed statuses: present 8,350, missing 1,078, stub 24, unsafe 1. Statuses `empty`, `misrooted`, `unparsed` and state `unavailable` are reachable in code but were not observed live.

**Why the live count is 0:** tool-owned keys and values are compile-time literals (`STATUS_NAMES`, the five state strings, the four `NAME_HINT_RE` tokens, the schema constant). The only escape routes are dispatch- or filesystem-controlled fields (section 4).

**Static audit (current source):** the triad occurs only at `tools/mori-wave-settlement.py:18` (docstring "A missing report is not a dead seat"), `:636` (selftest FAIL literal "0 failed"), and `:661-664` (selftest `failed` variable and summary print). No scan-mode line contains it.

**Usage and error paths:** `--help` rc 0; no arguments rc 2; `scan` without `--lane-root` rc 2; unreadable lane root rc 2 (stderr `mori-wave-settlement: lane root is unreadable`). 0 triad hits in stdout+stderr for all four.

**Literal occurrence in tool output:** `--selftest` prints `MORI_WAVE_SETTLEMENT_SELFTEST: PASS (23 cases, 23 passed, 0 failed)`, rc 0. The word is a case-count label, not a seat state. Count: 1 per run.

## 3. Attack on the guarantee's own test (main finding)

- **Coverage gap:** the frozen `no_vocab` assertion is on exactly one case, `deterministic` (read of `frozen/c2-expected.json` with a jq filter returns one element). Code: `tools/mori-wave-settlement.py:611`, `if "no_vocab" in expected:`. The `deterministic` fixture (`:503`) gives every member a report. Observed: member statuses `['present']`, rc 0, states settled/settled. No vocabulary assertion ever sees a missing, stub, misrooted, unsafe or unparsed member.
- **Mutant A (survives):** scratch copy at `/tmp/vocabfleet/mut3/A-reason-on-missing/`. Each `missing` member also gets `"reason": "seat failed"` (`:284`).
  - `--selftest`: `MORI_WAVE_SETTLEMENT_SELFTEST: PASS (23 cases, 23 passed, 0 failed)`, rc 0. Zero failing cases.
  - Live mori: 94 triad substrings = 88 tool-owned (one per missing member) + 6 echo.
- **Mutant B (caught, by fixture shape):** scratch copy at `/tmp/vocabfleet/mut3/B-status-rename/`. `missing` renamed to `failed` in `STATUS_NAMES` (`:35`) and in `_member_status` (`:246`).
  - `--selftest`: `MORI_WAVE_SETTLEMENT_SELFTEST: FAIL (23 cases, 21 passed, 2 failed)`, rc 1.
  - Failing cases: `symlink-report` (frozen `not_followed` assertion, `:599-603`, requires the literal `"missing"`) and `deterministic` (`no_vocab`, triggered by the `counts` key `failed`, which appears in every wave even at zero).
  - Live mori: 109 triad substrings = 103 tool-owned (88 status values, 14 `counts` keys, 1 `totals` key) + 6 echo.
  - My prior prediction that B would survive was wrong. This is the measured result.
- **Net:** a new triad string emitted only on the missing-report path passes `--selftest`. That is the path the guarantee exists for.

## 4. Echo channel (out of search scope; defeats the literal claim)

- Member `name` values and the `missing` list echo dispatch text verbatim. Live: 24 hits (section 2).
- `dispatch_path` and `lane_root` echo filesystem names, so a lane or file named with a triad word leaks the same way. Not observed live.
- **Key injection:** `wave`, `name` and `agent` are copied as arbitrary JSON. Scratch lane `/tmp/vocabfleet/echo/lane` (unmodified tool, 5027bdc7): dispatch with `"wave": {"failed": "..."}` and task name `killed-seat` gives rc 1, state `unsettled`, output key `failed` under `wave`, and `killed-seat` under `name` and `missing`. Total 3 hits. The output key space is not closed for dispatch-controlled fields.

## 5. Adjacent observations (not vocabulary; they change how "never says failed" reads to a consumer)

- **Exit code:** rc 1 for 15 of 21 lanes, meaning any wave not `settled` or `no-spawn`. That includes `partial` lanes where seats did report. Code: `:375`, `rc = 0 if all(...) else 1`. The words stay clean, but rc 1 is the conventional failure code for shell callers [INFERENCE on how consumers read it].
- **Vacuous clean:** 6 lanes discover zero waves, so `all([])` gives rc 0 with no state word.
  - audio-shokunin, game-dev-2d-shokunin, game-dev-3d-shokunin, kotodama-shokunin: no `.ufo` directory.
  - kotoba-shokunin: `.ufo` without `waves`.
  - lore-shokunin: `.ufo/waves` holds 1,101 non-dispatch JSON files and 1 unreadable file, and still returns rc 0.
- **Discovery takes scratch:** the tool walks all of `.ufo/waves/` for `schema == ufo-swarm-wave-dispatch-v1`. mori went from 13 to 14 waves between my first capture and the mutant runs. The added wave is `.ufo/waves/round-20/falsify/SentinelTool/probe-20261021/outside/secret.json`, a sibling seat's probe. I recorded the path only; contents not opened.
- **Tool changed during this run:** sha256 went `e5c06dad...` → `203c716e...` → `5027bdc7...`. My older mutant build differs from the `203c716e` build only in 9 docstring lines. The `203c716e` → `5027bdc7` change adds an R8 docstring line and one selftest case (22 → 23). I did not diff every intermediate. All reported numbers come from the `5027bdc7` run.
- **Live drift:** between my 11:11:49Z and 11:13:43Z snapshots, mori non-present went 122 → 113 and mori ignored_json went 691 → 702.

## 6. Recommendations (for the lead)

1. Apply `no_vocab` to every fixture, or at minimum the missing, stub, misrooted, unsafe, unparsed and symlink cases. Also assert the member key set is exactly `{name, agent, status}`.
2. Re-run check: `TMPDIR=/tmp/vocabfleet/tmp python3 /tmp/vocabfleet/mut3/A-reason-on-missing/tools/mori-wave-settlement.py --selftest`. It passes today. A fix should make it FAIL.
3. Close the key space: require dispatch `wave`, `name` and `agent` to be strings (or hash or drop them). Otherwise document the echo channel as outside the guarantee.
4. Either document rc 1 as "not all settled" or split it so `partial` is not coded as failure.
5. Make zero discovered waves non-vacuous, e.g. rc 2 or a state word when `.ufo/waves` exists but yields no dispatch files.
6. Skip scratch trees (e.g. `falsify/`) in `_dispatch_files`, or require a registry marker.

## 7. Bounds, writes, installs (disclosed)

- **Lane write by me (cleaned up):** my `importlib` loads of the lane tool created `mori-shokunin/tools/__pycache__/mori-wave-settlement.cpython-314.pyc` at 11:05:36Z. I removed that directory during the 11:11:49Z snapshot cell (birth-time check: it post-dated my scratch dir).
- **Lane write not mine (left alone):** `tools/__pycache__/mori-wave-settlement.cpython-314.pyc` reappeared with birth 11:12:18Z, after my removal. I did not create it: later loads used scratch copies with `sys.dont_write_bytecode=True`, and lane runs were script-mode subprocesses. [INFERENCE: another process imported the lane tool.] It is still present at the end of the run. I did not delete it.
- **Bounds deviation (disclosed):** my first `glob` call used the fleet root with no narrowing pattern. It returned file names from several lanes' `.ufo/` and `waves/` trees. Names only; no content read. No `.ufo/interactive-sessions/`, `.ufo/worktrees/`, `.jj/` or `~/.omp` path opened.
- **Installs:** none. Python 3 standard library only.
- **Not done:** no git or jj commands, no census run, no subagents, no lane-file edits.
- **Scratch:** `/tmp/vocabfleet/` (final captures in `final2/`, mutants in `mut3/`, echo lane in `echo/`).
- **Unobserved [INFERENCE]:** the `--out` file is byte-identical to stdout (same `_json_bytes` path; not run). The R8 symlink-parent behaviour is covered only by the selftest.
