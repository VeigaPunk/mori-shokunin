STATUS: complete

# TrailerVariants: round-20 `Report:` trailer census (read-only)

Seat `MoriR20.TrailerVariants` (leaf; no subagents). Scope: every regular `*.json` under `/home/vgpnk/Projects/shokunin/*-shokunin/.ufo/waves/` whose top-level `schema` equals `ufo-swarm-wave-dispatch-v1`. Snapshot B: 2026-10-21 10:35:43Z to 10:36:04Z. Candidate-list sha256 prefix `aafa1259f8d4ec60`.

## Result

- 196 dispatch files and 12,307 `taskCall.tasks[*]` entries. Last line of each task tested against `^Report: write your scoped findings to \S+$`:
  - **12,211 match.** All are relative `.ufo/...` paths; none absolute, none with a `..` component.
  - **96 do not match.**
- **Distinct non-matching shapes: one**, last line `` `\| godspeed` `` (10 bytes). All 96 are in tabi-shokunin's `final-clones/` copies of one dispatch file (32 tasks in each of 3 trees). In these tasks the trailer is present but sits two lines above the end, followed by a blank line and `| godspeed`.
- No other lane has a non-matching task. Outside tabi's `final-clones/`: 9,382 tasks, all matching.
- Every one of the 12,307 tasks contains exactly one trailer line.

## Per-lane counts (snapshot B)

| Lane | `*.json` under `.ufo/waves` | unparseable | dispatch (schema match) | of which in `final-clones/` | `taskCall: null` | tasks | match | non-match |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| chousa-shokunin | 13 | 0 | 2 | 0 | 0 | 136 | 136 | 0 |
| kagi-shokunin | 103 | 0 | 7 | 0 | 0 | 479 | 479 | 0 |
| kaidoku-shokunin | 3,411 | 36 | 14 | 0 | 0 | 959 | 959 | 0 |
| kake-shokunin | 177 | 0 | 5 | 0 | 0 | 325 | 325 | 0 |
| kama-shokunin | 296 | 2 | 19 | 0 | 0 | 1,198 | 1,198 | 0 |
| kasegi-shokunin | 13 | 0 | 1 | 0 | 0 | 64 | 64 | 0 |
| kengaku-shokunin | 17 | 0 | 5 | 0 | 0 | 387 | 387 | 0 |
| kumitate-shokunin | 33 | 0 | 6 | 0 | 0 | 512 | 512 | 0 |
| lore-shokunin | 1,102 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| mado-shokunin | 428 | 2 | 16 | 0 | 0 | 1,030 | 1,030 | 0 |
| mori-shokunin | 480 | 1 | 11 | 0 | 0 | 671 | 671 | 0 |
| revenger-shokunin | 9 | 0 | 1 | 0 | 0 | 32 | 32 | 0 |
| souji-shokunin | 55 | 0 | 12 | 0 | 0 | 783 | 783 | 0 |
| tabi-shokunin | 5,160 | 0 | 67 | 51 | 3 | 3,932 | 3,836 | 96 |
| tameshi-shokunin | 106 | 0 | 16 | 0 | 0 | 965 | 965 | 0 |
| tsukuroi-shokunin | 227 | 0 | 14 | 0 | 0 | 834 | 834 | 0 |
| **total** | **11,630** | **42** | **196** | **51** | **3** | **12,307** | **12,211** | **96** |

- Tabi outside `final-clones/`: 16 dispatch, 1,007 tasks, all match.
- Tabi inside `final-clones/` (3 trees): 51 dispatch, 2,925 tasks: 2,829 match, 96 non-match.
- Lanes with no `.ufo/waves`: audio, game-dev-2d, game-dev-3d, kotodama, kotoba (the last has `.ufo` only). Near-miss directory `tameshi-shokukin` (typo; not matched by `*-shokunin`) has `.ufo/waves` with 0 files; excluded.

## Distinct non-matching shapes

| Last line (verbatim) | Last three lines, reduced to kinds | Tasks | Lanes |
|---|---|---:|---|
| `\| godspeed` | `<TRAILER>` / `<blank>` / `\| godspeed` | 96 | tabi-shokunin only |

Evidence: ExecFrozen copy, `taskCall.tasks[0].task`, text lines 14 to 17 (checked with `cat -A`):

```
(blank)
Report: write your scoped findings to .ufo/rounds/fleet-round-1-interactive-20261015/seats/TabiNote01.md
(blank)
| godspeed
```

- The same 32-task block is in the `ExecFixtures`, `ExecFrozen` and `ExecCounter` copies of `.ufo/rounds/fleet-round-1-interactive-20261015/wave.dispatch.json` under `tabi-shokunin/.ufo/waves/round-20/final-clones/<tree>/`. All three share sha256 prefix `4562e0f096e84cdc`.
- Members: TabiNote01 to TabiNote23 and TabiAudit01 to TabiAudit07 (reviewer), TabiPublicPlugin (scout), TabiWitnessConnector (connector).
- Every task in those files opens with `/skill:godspeed` on line 1, as the standard tasks do. The trailing `| godspeed` line is the only difference in the tail.
- Each variant trailer points into `.ufo/rounds/fleet-round-1-interactive-20261015/seats/<Name>.md`. These 96 are the only trailers under `.ufo/rounds/` in the corpus (0 among the 12,211 matches).

Tail shapes over all 12,307 tasks:

| Tail shape (last three lines) | Tasks | Lanes |
|---|---:|---|
| `<line> ~ <blank> ~ <TRAILER>` | 12,211 | 15 lanes |
| `<TRAILER> ~ <blank> ~ \| godspeed` | 96 | tabi-shokunin (clone trees only) |

## Dispatch-level shapes (not tasks; not counted above)

- 3 `wave-validation.json` receipts, one per clone tree, have `taskCall: null` and top-level `counts.total: 32`. Their `run_not_invoked` reads "Dispatch blocked by required taxonomy alias mismatch; ... No claimed spawn/handle." They contribute 0 tasks.
- For the 193 non-null `taskCall`s, `tasks` length equals `counts.total`. Sum of `counts.total` = 12,307 = extracted tasks.
- No non-object task entries, no task without a string `task`, no `taskCall` without a `tasks` array.

## Findings for the integration owner (facts)

1. **The variant defeats the contract's last-line rule.** `contract.md:70-73` takes the LAST line as the report path and classes a task without the trailer as `unparsed`. The 96 tasks carry the trailer above a trailing `| godspeed`. A "last non-blank line" reading still rejects them, because `| godspeed` is non-blank. Only a "trailer anywhere in the task" reading accepts them. [INFERENCE] Under the literal rule these 96 would be `unparsed`; no C2 implementation was read or run.
2. **Oracle gap.** `frozen/c2-expected.json` line 5 (`fixture_note`) says a task body ends with the trailer line. The only trailer-position case is `no-trailer` (line 13, expects `unparsed: 1`). No case covers a trailer that is present but not last.
3. **Scope.** Discovery (`contract.md:64-67`) takes every `*.json` under `.ufo/waves/`, so the clone trees are in scope as written: 51 of 196 dispatch files (26%) and 2,925 of 12,307 tasks (24%). Without `final-clones/`: 145 dispatch files, 9,382 tasks, 9,382 match, 0 non-match. Which reading the C2 scan and fleet-wide demonstration use is an L1 decision.
4. **Receipts vs counts.** `contract.md:68` maps `taskCall: null` to `no-spawn`, which is correct for these receipts. A counter keyed on `counts.total` would report 96 spawns that did not happen.
5. **The tree moved during this run.** Snapshot A (schema pass 10:30:32Z, extraction through about 10:34Z): 9,975 JSON, 178 dispatch, 11,244 tasks, 11,180 match, 64 non-match. Snapshot B: 11,630 JSON, 196 dispatch, 12,307 tasks, 12,211 match, 96 non-match. Delta: tabi +1,645 JSON from a new clone tree `final-clones/ExecCounter` (17 dispatch, 975 tasks, 32 non-match); kagi +5 JSON (1 dispatch, `round-25/build-dispatch.json`, 88 tasks, all match); mori +5 JSON (other seats' round-20 outputs, none dispatch). Any C2 verdict must cite the snapshot time and candidate digest.
6. **Exclusions (none counted).**
   - 32 files with `schema: ufo-swarm-wave-v1` (exact match only).
   - 7 files that contain the dispatch schema text but whose top-level `schema` is absent or different, e.g. `mori-shokunin/.ufo/waves/round-20/frozen/c2-expected.json` (`mori-r20-c2-expected-v1`).
   - 5 files that are not a single JSON document or have a non-string `schema` (4 multi-document, 1 numeric); none contains the dispatch text.
   - 42 unparseable `.json` (kaidoku 36, kama 2, mado 2, lore 1, mori 1); none contains the dispatch text.
   - 3 symlinked `*.json` (`case-symlink/cases/alias.json`, one per clone tree), not followed.

## Method

Run from `/home/vgpnk/Projects/shokunin`; scratch outputs in `mori-shokunin/.ufo/waves/round-20/build/TrailerVariants/`:
1. Enumerate: `find ./*-shokunin/.ufo/waves -type f -name '*.json'` gives `json-files.txt` (regular files only; symlinks not followed).
2. Schema: `/usr/bin/jq -s -r` reads the top-level `.schema`; exact string equality gives `schema-inventory.tsv` and `candidates.txt`. Unparseable files are marked `<UNREADABLE-JSON>`.
3. Extract: `jq -c --arg lane --arg file -f extract.jq` per candidate. Last line = last element after removing trailing newlines; class = `test("^Report: write your scoped findings to \\S+$")`. Output `task-rows.jsonl`.
4. Tail census: `tail.jq` gives `tail-rows.jsonl` (trailer-line count, distance from end, last three lines as kinds).
5. Cross-check: `/usr/bin/grep -cP '^Report: write your scoped findings to \S+$'` over the extracted last lines (`last-lines-B.txt`): 12,211 match, 96 non-match.

Checks that passed on snapshot B:
- Strict (no trailing-newline stripping) and lenient classes disagree on 0 tasks; 0 tasks end in a newline; 0 last lines end in CR.
- `jq` and `grep -P` agree.
- Tasks per dispatch equal `counts.total`.
- Representative clone files have identical digests across trees: `wave.dispatch.json` 4562e0f096e84cdc, `wave-validation.json` b0a14d47fa600a09, `round-20/w1/dispatch.json` 36a43610a4dfec76.
- The 51 clone-tree files reduce to 16 distinct contents (17 relative paths, one identical pair).

Tools:
- Canonical binaries for snapshot B: `/usr/bin/jq` (jq-1.8.2), `/usr/bin/grep` (GNU grep 3.12-modified, `-P`), plus coreutils `find`, `cut`, `sort`, `uniq`, `comm`, `cp`, `sha256sum`. No python or awk.
- The shell's own `jq` and `grep` are builtins reporting `jaq 3.1.1` and `pi-uu-grep 0.2.0`. Snapshot A used them; its task and tail rows were then byte-identical to the jq-1.8.2 output (`cmp`).
- Installs or updates: none. `jq` 1.8.2 and GNU grep 3.12 were already present.

Bounds: writes only under `.ufo/waves/round-20/build/TrailerVariants/` and this report. No lane file, MANIFEST, `.ufo/state/*`, watchdog log, git/jj state or host service was touched. No transcripts or `~/.omp` logs were opened; only dispatch JSON was read, not seat `.md` reports. No subagents; no census script run.

## Not observed

- Origin of the `| godspeed` suffix: [INFERENCE] an artefact appended when the clone trees were produced. No generator was inspected.
- Why `ExecCounter` appeared between snapshots A and B: not investigated.

## Reproduce

```
cd /home/vgpnk/Projects/shokunin; J=/usr/bin/jq; S=mori-shokunin/.ufo/waves/round-20/build/TrailerVariants
while IFS= read -r f; do lane=${f%%/*}; $J -c --arg lane "$lane" --arg file "$f" -f $S/extract.jq "$f"; done < $S/candidates.txt > $S/task-rows.jsonl
$J -r 'select(.kind=="task") | .last // "<NULL>"' $S/task-rows.jsonl | /usr/bin/grep -cvP '^Report: write your scoped findings to \S+$'
```
