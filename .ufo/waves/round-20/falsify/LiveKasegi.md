# Falsify C2 accuracy — lane kasegi — MoriR20.LiveKasegi

**Verdict: HOLDS** (lane kasegi). The fresh scan, the wave-1 ground truth (`build/GtLaneKasegi.md`) and the committed fleet snapshot (`evidence/c2-live-fleet.json`) agree on every field they record, for all 64 members. Zero differences, so no live-change or tool-error explanation is needed.

Adjacent defects found while attacking, outside the kasegi row (not counted against the verdict; detail in §5-§6):
- **BROKEN — fleet snapshot totals:** the `mori-shokunin` row in `c2-live-fleet.json` sums 6 short of its 671 members. The generator drops the `stub` bucket.
- **Residual — settlement tool silent false-clean:** a symlinked `.ufo` or `.ufo/waves` yields rc 0 with zero waves. Contract-literal; kasegi unaffected.

## 1. Fresh scan (read-only)

Exact command:
```
python3 /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-wave-settlement.py scan --lane-root /home/vgpnk/Projects/shokunin/kasegi-shokunin --fleet-root /home/vgpnk/Projects/shokunin --out /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-20/falsify/LiveKasegi/scan.json
```
Exit 1 (`EXIT=1`; state `partial` per contract exit rule). Output: one dispatch-v1 file `.ufo/waves/round-23/build-dispatch.json`, sha256 `7ced1f2585dd7df5ff819d23d85a69f071028bdcb4aec7f6ed7ab2379e8efa9d`; members 64; present 44; missing 20; empty 0; misrooted 0; stub 0; unparsed 0; unsafe 0; state `partial`; ignored_json 12; unreadable_json 0; name_hint null; duplicate_of null; duplicate_report_paths 0.

Second run, identical arguments but `--out /tmp/LiveKasegi-scan2.json`: rc 1, output byte-identical to the first (4,860 B).

## 2. Per-dispatch comparison (single dispatch-v1 file)

| Field | Fresh scan | GtLaneKasegi.md (manual) | c2-live-fleet.json kasegi row | Difference |
|---|---|---|---|---|
| members | 64 | 64 | 64 | none |
| present | 44 | 44 | 44 | none |
| missing | 20 | 20 | 20 | none |
| misrooted | 0 | 0 | 0 | none |
| empty | 0 | 0 | 0 | none |
| unparsed | 0 | 0 | 0 | none |
| unsafe | 0 | 0 (all 64 trailers relative, no `..`) | 0 | none |
| stub | 0 | not a Gt field; all 44 present files are ≥2,665 B against the 16-byte stub ceiling (`tools/mori-wave-settlement.py:35`) | not recorded (`COUNT_FIELDS` omits it, `c2-fleet-live.py:17-20`) | none |
| state | partial | derivable: 44 present / 20 not ⇒ partial | not recorded (exit 1 only) | none |
| waves | 1 | 1 | 1 | none |
| exit | 1 | — | 1 | none |
| unreadable_json | 0 | — | 0 | none |

Non-dispatch JSON under `.ufo/waves`: 12 (11 keyless + `ufo-swarm-registry-v1` at `build/swarm-registry.json`), matching `ignored_json` 12.

## 3. Per-member (64/64 agreement)

- Tool status list == my independent re-derivation (own trailer parse with the same regex, own `lstat`/size logic) == Gt per-member table rows 0–63 (name, agent, status), same order.
- The 20 missing trailer paths: `os.path.lexists` is False for all 20 (no file, no dangling symlink). None exists at `/home/vgpnk/Projects/shokunin/.ufo/waves/round-23/build` (directory absent).
- `.ufo/waves` holds 59 entries: 2 directories, 13 regular JSON, 44 other regular files. The 44 other files are exactly the 44 present trailer paths (checked by set equality), so no missing report was written under any other name anywhere in `.ufo/waves`.
- Trailer rule: each of the 64 tasks has exactly one trailer-matching line, and it is the literal last line. Refinement R1 (last matching line) therefore changes nothing for kasegi.
- Present sizes: min 2,665 B (`RecheckManifest.md`), max 16,548 B (`CraVuln.md`), confirmed by `stat`.

## 4. Difference accounting

No differences to explain. Timeline (all -03; mtimes from `stat`, GNU):

| Time | Event |
|---|---|
| 2026-10-20 18:33:30 | dispatch `round-23/build-dispatch.json` written |
| 18:42:19 | `round-23/build/swarm-registry.json` last written (18,218 B) |
| 18:43:50 – 18:48:23 | 44 report files written; newest `build/CraRecipients.md` at 18:48:23 |
| 2026-10-21 07:30:37 | Gt observation time (file `GtLaneKasegi.md` mtime 07:34:26) |
| 07:46:53 | `c2-live-fleet.json` last written (commit `2eeae04`, 07:47:09 -03) |

The newest of all 59 entries under `.ufo/waves` is 18:48:23 on 10-20, so nothing changed after either comparator was taken. There is no live change to explain. The 20 unwritten reports are a dispatch-time fact; their cause is not observable from read-only artifacts [INFERENCE: spawned members did not complete the write].

The only snapshot-vs-tool difference is projection: the snapshot has no `stub`, `state` or `ignored_json` key. That is the generator's field list, not a value conflict (§6).

## 5. Tool attacks (accuracy)

a. **Determinism:** byte-identical across two runs (§1). Pass.

b. **Stub:** kasegi has no member at or below 16 bytes, so stub = 0 is forced by the size floor, not assumed.

c. **Presence is size-based, not content-based.** 8 of 44 present reports do not contain their own member name: BountySymlink, NestedEscape, GlobEscape, PlaceholderEscape, BraceEscape, RangeLimits, EmptyCorpus, RevPlaceholder. Each opens with a heading for its own attack item (e.g., BountySymlink: `# C1 — bounty-mirror symlink escape`). The frozen contract (`.ufo/waves/round-20/contract.md`, C2 member status) defines `present` as size > 0 and makes no content claim, so this is a limit of the contract, not a tool error. 13 of 44 present reports name another member as a whole word; I did not classify those references.

d. **Symlink false-clean (tool, contract-literal):** `_wave_root` (`tools/mori-wave-settlement.py:74-92`) returns None when `.ufo` or `.ufo/waves` is a symlink or absent. `scan_lane` then sets `paths = []` (`:317-318`), and rc is `all([]) → 0` (`:366`). Fixture under `/tmp/LiveKasegi-fx/`:
   - control (real directory, one unsettled dispatch): rc 1, 1 wave, state `unsettled`, totals.missing 1;
   - same dispatch behind a symlinked `.ufo/waves`: rc 0, 0 waves, totals.missing 0.
   Kasegi is unaffected (real directory; the tool discovered its wave).

e. **Label overlap (tool):** wave-level `missing` (`:290`) includes stub members, while `totals.missing` (`:344-350`) counts only status `missing`. Mori's committed live scan (`evidence/c2-live-mori.json`): 91 names in wave-level `missing` vs `totals.missing` 85, with `totals.stub` 6. Kasegi: 20 vs 20 (no stubs).

## 6. Adjacent defect: fleet snapshot — BROKEN (not kasegi)

- Snapshot mori row (`evidence/c2-live-fleet.json`): members 671, present 580, missing 85, empty/misrooted/unparsed/unsafe 0. Bucket sum 665, so 6 members are unaccounted for.
- The tool's own mori totals (`evidence/c2-live-mori.json` `.totals`): present 580 + missing 85 + stub 6 = 671. The tool is internally consistent; the snapshot drops `stub`.
- Cause, in the L1 generator `mori-shokunin/.ufo/waves/round-20/build/LiveRunner/c2-fleet-live.py`: `COUNT_FIELDS` (lines 17-20) has no `stub`, and `parse_counts` copies only `COUNT_FIELDS[1:-1]` from `totals` (lines 69-74). The tool emits `stub` in `STATUS_NAMES` (`tools/mori-wave-settlement.py:33`) and aggregates it at `:344-350`.
- The other 20 lanes' bucket sums equal their members exactly (difference 0), so none had stub members at snapshot time. Only mori is affected in this snapshot. Kasegi's row is consistent: 44 + 20 = 64.
- Consequence for C2's live fleet demonstration: the committed snapshot under-accounts mori by 6 members, and would under-account any lane with stubs. Fix belongs to the L1 integration owner: add `stub` to `COUNT_FIELDS` and the snapshot schema, regenerate, and assert `sum(buckets) == members` per lane. I did not edit the generator (bounds).

## 7. Residual risk and gaps

- Cause of the 20 unwritten reports: not observable from read-only artifacts [INFERENCE].
- Searched: the full `.ufo/waves` tree (59 entries) and the `.ufo/rounds` JSON schemas (24 files: 20 keyless, 1 `ufo-swarm-registry-v1`, 3 `kasegi-*`; none dispatch-v1). I did not re-search outside `.ufo/waves` for the 20 names; Gt searched the fleet `.ufo` (depth 6) and the 14 `/tmp/kasegi-r23-*` clones.
- Not run: `mori-census.sh` (not requested). Not opened: `.ufo/interactive-sessions/`, `.ufo/worktrees/`, `.jj/`, or any session log. No subagents (leaf seat). No edits to any lane or mori production file.

## 8. Tools, scratch, corrections

- Installs or updates: none. Observed versions: `jq-1.8.2` (`/usr/bin/jq`, used for counts), Python 3.14.8 (`python3`).
- Scratch: `falsify/LiveKasegi/scan.json`; `/tmp/LiveKasegi-scan2.json`; `/tmp/LiveKasegi-fx/` (fixture).
- This file supersedes my earlier draft. Corrections: (1) I had said the snapshot "predates R2"; the snapshot does not show that. It was written at 10:46:53Z, the same minute as the lesson's stub observation, and the omission is the generator's `COUNT_FIELDS` (§6). (2) I had written the commit time as 07:47:09Z; it is 07:47:09 -03 (10:47:09Z). (3) "All dispatch JSON sha256-identical" is corrected: only one dispatch-v1 file exists, and its digest matches the scan. (4) "lstat FileNotFoundError" is corrected: the fleet-root check used `os.path.exists`/`lexists`. (5) "Filesystem-frozen" is narrowed to the wave tree, which I verified entry by entry.
