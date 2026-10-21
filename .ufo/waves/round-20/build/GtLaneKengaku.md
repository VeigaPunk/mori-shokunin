STATUS: complete

# GtLaneKengaku: C2 independent ground truth, lane kengaku-shokunin

Lane root: `/home/vgpnk/Projects/shokunin/kengaku-shokunin` (read-only). Fleet root for misroot checks: `/home/vgpnk/Projects/shokunin`.

Rules applied (contract.md, C2): trailer = last line of a task matching `^Report: write your scoped findings to (\S+)$`; the path must be relative, have no `..` component and resolve inside the lane root (else `unsafe`). `present` = regular non-symlink file with size > 0; `empty` = size 0; `missing` = absent under the lane root; `misrooted` = missing under the lane root but a regular file at the same relative path under the fleet root.

Method: jq for schema and member/trailer extraction; find, test and cmp for file types, sizes and existence; a one-off Python pass over the jq output for classification, cross-checked by independent `find` counts. `tools/mori-wave-settlement.py` was NOT run (manual ground truth). Installs or updates: none.

## 1. Every `*.json` under `.ufo/waves` (17 files)

- 17 regular files, 0 symlinks, 0 unreadable (all parsed with jq).
- Schema `ufo-swarm-wave-dispatch-v1`: 5 files (section 2).
- Counted by the tool as `ignored_json` = 12:
  - 5 with `ufo-swarm-registry-v1`: `round-25/build/swarm-registry.json`, `round-25/falsify/swarm-registry.json`, `round-26/build/swarm-registry.json`, `round-26/build/swarm-registry-pretrim-superseded.json`, `round-26/falsify/swarm-registry.json`.
  - 7 with no top-level `schema` key: `round-25/build-spec.json`, `round-25/falsify-spec.json`, `round-26/build-assignments.json`, `round-26/build-spec.json`, `round-26/falsify-assignments.json`, `round-26/falsify-dead-seats.json`, `round-26/falsify-spec.json`.

## 2. Per-file totals (paths relative to the lane root)

| # | dispatch file | wave | members (= `counts.total`) | parsed / unparsed / unsafe | present | empty | missing | misrooted | wave state | filename suggests never dispatched |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | round-25/build-dispatch.json | kengaku-r25-build | 92 | 92 / 0 / 0 | 92 | 0 | 0 | 0 | settled | no |
| 2 | round-25/falsify-dispatch.json | kengaku-r25-falsify | 87 | 87 / 0 / 0 | 87 | 0 | 0 | 0 | settled | no |
| 3 | round-26/build-dispatch.json | kengaku-r26-build | 72 | 72 / 0 / 0 | 72 | 0 | 0 | 0 | settled | no |
| 4 | round-26/build-registry-rebuild.json | kengaku-r26-build | 72 | 72 / 0 / 0 | 72 | 0 | 0 | 0 | settled | no (byte-identical to #3) |
| 5 | round-26/falsify-dispatch.json | kengaku-r26-falsify | 64 | 64 / 0 / 0 | 53 | 0 | 11 | 0 | partial | no |

Also checked for every file: `counts.total` equals the member count; member names are unique; no `taskCall: null` (no-spawn); all trailer paths are `.ufo/waves/<same round>/<build|falsify>/<Name>.md` (0 cross-round or cross-kind paths); no trailer path is absolute, contains `..`, or is a symlink.

## 3. Lane totals

- Raw sum over the five dispatch files: members **387**; parsed **387**; unparsed **0**; unsafe **0**; present **376**; empty **0**; missing **11**; misrooted **0**; symlink 0; other 0. Wave states by file: settled 4, partial 1, unsettled 0, unavailable 0, no-spawn 0.
- Distinct, with #4 deduplicated against #3 by report path: **315** distinct report paths; present **304**; missing **11**; misrooted **0**. Distinct waves: 4 (3 settled, 1 partial).
- Oracle values for comparison with a `scan` run under the contract's discovery rule: members 387, present 376, missing 11, misrooted 0, ignored_json 12, unreadable_json 0; per-file states as in section 2.

## 4. The 11 missing members (round-26 falsify, wave kengaku-r26-falsify)

Names: FxCensus, FxEntryMethod, FxHonesty, FxLowestAxis, FxMisroots, FxNoHarm, FxP3BIdSet, FxP3BRegistry, FxSeparability, FxSourcePythonRe, FxTrends. Expected path: `.ufo/waves/round-26/falsify/<Name>.md`.

- Under the lane root: absent (`test -e`: ABSENT ×11). At the same relative path under the fleet root: absent ×11, so misrooted = 0.
- The lane directory `.ufo/waves/round-26/falsify/` holds 53 `.md` files, and every one is referenced by a member (0 orphans). No report exists under another name in the lane. Whether a file was written and then removed is unobserved [INFERENCE: never written].
- Basename-only search of the fleet root (pruned `.git`, `node_modules`, `target`, `.venv`) found one hit, `tsukuroi-shokunin/.ufo/waves/round-17/falsify/FxNoHarm.md`. It is a different lane and round and not the same relative path, so it is not counted as misrooted.
- Cross-reference only: `.ufo/waves/round-26/falsify-dead-seats.json` (non-dispatch; the tool ignores it) has a `dead` list that is exactly these 11 names (set-equal). Its `status` is `"failed (exit 1)"`, its `shared_error` cites `Codex is at capacity ... (code=turn_rate_limit_exceeded)` after 5 retries, and its `handling` reads "No retry or replacement ... never a seat report". Per C2, these are missing reports. This seat does not classify them as dead.

## 5. Other observations

1. **Duplicate dispatch.** `round-26/build-registry-rebuild.json` is byte-identical to `round-26/build-dispatch.json` (`cmp` reports identical). It has the same wave `kengaku-r26-build` and the same 72 member rows and paths. Under the contract's discovery rule both are counted, so raw sums double-count 72 rows.
2. **Parser hazard.** Members `TallyR01`–`TallyR09` in `round-25/build-dispatch.json` (all present) each carry a second `Report:` substring mid-line in the task body. For TallyR01 it is 1-based line 11 of 17: "...(no python, no lane scripts). Report: every `## GT + scoring at close` block...". The trailer is line 17. The line-anchored last-line regex parses them correctly to `.ufo/waves/round-25/build/TallyRNN.md`. A parser that takes the first line containing `Report:` would read the body line instead.
3. **No placeholder-sized present files.** The smallest present report is 845 bytes (round-25 falsify). None is under 64 bytes. Only sizes were checked; no report content was read.
4. **Filename hints.** None of the 5 dispatch names and none of the 12 ignored names contains `preview`, `undispatched` or `validation`.
5. **Independent count check.** `find <dir> -maxdepth 1 -type f -name '*.md' -size +0c | wc -l` gives round-25/build 92, round-25/falsify 87, round-26/build 72, round-26/falsify 53. These match the classification. `find .ufo/waves -type l` gives 0.

## 6. Evidence and bounds

- Member-level evidence, 387 rows (dispatch file, wave, member, agent, status, misrooted, report path, size): `.ufo/waves/round-20/build/GtLaneKengaku/members.tsv` under the mori-shokunin root.
- Lane not modified: `find .ufo/waves -newer <this seat's status file>` returned no entries. No edits, no subagents, no messages sent. Only jq, find, test, cmp and a Python stdlib pass were used.
- Installs or updates: none.
