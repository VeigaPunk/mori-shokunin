# GtLaneKumitate: C2 independent fleet ground truth, kumitate lane

Seat: MoriR20.GtLaneKumitate (leaf; no subagents). Manual and read-only. Nothing was written, moved or edited under `/home/vgpnk/Projects/shokunin/kumitate-shokunin`. No git/jj commands. `tools/mori-wave-settlement.py` was not run (it is the tool under test). `round-20/frozen/c2-expected.json` was not read (independence). No transcripts or `~/.omp` session files were opened.

## Result

- `*.json` under `kumitate-shokunin/.ufo/waves`: 33. Top-level schema `ufo-swarm-wave-dispatch-v1`: **6**.
- Members across the 6 dispatch files: **512**. Report trailers parsed **512**, unparsed **0**.
- Under the lane root: present **468**, empty **0**, missing **44**. Misrooted **0**.
- Wave states: **4 settled** (round-35 build, round-35 falsify, round-36 build, round-37 falsify), **2 partial** (round-38 build, round-38 falsify).
- Filename suggests never dispatched (preview / undispatched / validation): **0 of 6**.

## Method

1. Discovery: `find <waves> -type f -name '*.json'` gave 33 files. `find -type l` under waves gave 0 symlinks. Python `json.load` on all 33 gave 0 unreadable. Top-level `schema` was read with `/usr/bin/jq` (jq-1.8.2, official package, already installed): `find <waves> -type f -name '*.json' -exec jq -r '[input_filename, (.schema // "NO_SCHEMA_KEY")] | @tsv' {} +`.
2. Member count: `.taskCall.tasks | length`. It equals `.registry.members | length` and `.counts.total` in all six files. Task names equal the registry key set in all six, with no duplicates.
3. Trailer: `jq -r '.taskCall.tasks[] | .task | split("\n")[] | select(test("^Report:"))'`. Each task has exactly one such line, and every line is `Report: write your scoped findings to <path>`. The contract regex `^Report: write your scoped findings to (\S+)$` matched all 512.
4. Status: `os.path.isfile` plus `getsize` under the lane root (`present` = size > 0, `empty` = size 0). `missing` paths were checked under `/home/vgpnk/Projects/shokunin` at the same relative path (`misrooted`).
5. Counts were recomputed with the Python stdlib (`json`, `os.path`, `hashlib`) and agree with the jq counts.

Tooling: nothing was installed or updated by this seat. The bare `jq` name in the persistent shell resolves to a builtin that reports `jaq 3.1.1`. No number here came from it; all jq results came from `/usr/bin/jq` (jq-1.8.2) or the `~/.local/bin/jq` PATH binary, which also reports jq-1.8.2.

## Per-file totals

| # | dispatch file (under `kumitate-shokunin/.ufo/waves/`) | wave | members | trailers parsed / unparsed | present | empty | missing | misrooted | wave state | filename hint |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | `round-35/build-dispatch.json` | kumitate-r35-build | 95 | 95 / 0 | 95 | 0 | 0 | 0 | settled | none |
| 2 | `round-35/falsify-dispatch.json` | kumitate-r35-falsify | 75 | 75 / 0 | 75 | 0 | 0 | 0 | settled | none |
| 3 | `round-36/build-dispatch.json` | kumitate-r36-build | 96 | 96 / 0 | 96 | 0 | 0 | 0 | settled | none |
| 4 | `round-37/falsify-dispatch.json` | kumitate-r37-falsify | 68 | 68 / 0 | 68 | 0 | 0 | 0 | settled | none |
| 5 | `round-38/build-dispatch.json` | kumitate-r38-build | 90 | 90 / 0 | 89 | 0 | 1 | 0 | partial | none |
| 6 | `round-38/falsify-dispatch.json` | kumitate-r38-falsify | 88 | 88 / 0 | 45 | 0 | 43 | 0 | partial | none |
| | **lane total (6 files)** | | **512** | **512 / 0** | **468** | **0** | **44** | **0** | 4 settled, 2 partial | 0 of 6 |

Per-file totals:

- All six files have `schema`, `wave`, `policy`, `counts`, `registry`, `compaction`, `taskCall`, `resumeSends` (empty) and `note`. `counts.resume` is 0, every member is `kind: spawn`, and `compaction.applied` is false.
- Trailer path prefix is `.ufo/waves/<round>/<build|falsify>/` and the basename is `<member name>.md` for all 512. No path is absolute, contains `..`, or is a symlink leaf. Every path is unique.
- The filename hint applies to none of the six. The only `preview|undispatched|validation` name under waves is `round-37/wave-plan-validation.json`, whose schema is `ufo-swarm-wave-v1`, so it is not a dispatch file and is excluded.

## Missing members (lane root)

- `round-38/build` (1): `ConnSibling` → `.ufo/waves/round-38/build/ConnSibling.md`. Evidence: `round-38/build-dispatch.json:906` (registry member) and `:1380-1382` (task entry).
- `round-38/falsify` (43): `Check03 Check04 Check05 Check06 Check07 Check09 Check12 Check14 Check15 Check20 Check22 Check23 Check24 Check25 Check30 Check32 Check35 Check38 Check39 Check40 Check41 Check42 Check48 Check50 Check54 Check55 Check56 Check58 Check60 Check63 Check65 Check66 Check67 Check70 Check73 Check75 Check76 Check78 Check79 CritNoHarm SentFinal VerifyIndependent VerifyRecords`.

Misrooted: 0.

- `/home/vgpnk/Projects/shokunin/.ufo/waves/round-38/` does not exist, so no misrooted copy is possible for round-38.
- A basename search of the fleet root (depth ≤ 7, pruned of node_modules, .git, .jj, target; not exhaustive) found none of the 44 names inside the kumitate lane. It found four basename-only hits in other lanes at other rounds: `kagi-shokunin/.ufo/waves/round-23/falsify/CritNoHarm.md`, `tabi-shokunin/.ufo/waves/round-20/w1/ConnSibling.md`, `tsukuroi-shokunin/.ufo/waves/round-18/build/ConnSibling.md`, `tsukuroi-shokunin/.ufo/waves/round-18/build/CritNoHarm.md`. Different round and relative path, so not counted as misrooted.

## Present-file checks

- Empty (0 bytes): 0. Whitespace-only: 0. Single-line `STATUS:` stubs: 0.
- Present sizes: min 1169 B, median 6541 B, max 145317 B.

## Dispatch file SHA-256 (raw bytes, Python `hashlib`)

- `round-35/build-dispatch.json` f2f3497e14ee467323cf62dff7103f548ded4a9c9b730041127f2dc18c275aa4
- `round-35/falsify-dispatch.json` 9b6e69330b23a66ce016b125a42b935f500b4f11494cd83d6fa81fb78dc5cbb2
- `round-36/build-dispatch.json` 879128fd41e9cc78eb72881eeb145eee75d16fe3b8f4069d69bd735fd5eac191
- `round-37/falsify-dispatch.json` 894aac3a7986085e394f1d25ffa69f56f990dce6ffa8e03e6f68c832764ffaa1
- `round-38/build-dispatch.json` 5b24206b841d33f27f62de34edf95e62779093cce0c41dccd274cf09c70e07c5
- `round-38/falsify-dispatch.json` 3140900b9a0be5161be8a1c2c91f2f96dd804a98042bca6cf97faedb14e33c10

## Discovery totals (all of `.ufo/waves`)

- 33 `*.json`: 6 dispatch-schema, 27 ignored, 0 unreadable.
- Ignored by schema: `ufo-swarm-registry-v1` 6 (one `swarm-registry.json` per wave/`falsify`/`build` directory); `ufo-swarm-wave-v1` 3 (`round-37/wave-plan-validation.json`, `round-38/build-plan.json`, `round-38/falsify-plan.json`); `kumitate-anchor-truth-frozen-v1` 2 (`round-38/frozen/expected.json`, `expected-c938.json`); no top-level `schema` 16 (including `round-36/baseline/rows.json`, a top-level array).

## Lane self-reports (cross-reference only; not used as ground truth)

- `round-38/evidence/falsify-summary.json`: `dispatch_count` 88, `reports` 45, `dead_seats` 43. The 43 names are set-equal to the 43 missing falsify members and to the keys of `round-38/evidence/falsify-dead-seat-results.json`.
- `round-38/evidence/build-seat-accounting.txt:1`: "Build wave: 90 dispatched, 89 scoped reports, 1 failed seat (never replaced): ConnSibling". Matches the filesystem count for round-38 build.
- The lane labels the 43 falsify misses "dead seats" and the build miss a "failed seat". Those labels were not independently verified here. The frozen contract says tool output must say `missing`, not `dead`/`failed`.
- `falsify-dead-seat-results.json` values carry `resolvedPath` strings under `~/.omp/agent/sessions/`. These appeared in a jq field printout. No file at those paths was opened.

## Expected values for the L1 comparison

Derived from the lane's own files, for `scan --lane-root kumitate-shokunin`:

- Waves discovered 6; `ignored_json` 27; `unreadable_json` 0.
- Per wave: `settled` 95/95, 75/75, 96/96, 68/68. `partial` 89/90 (missing `ConnSibling`) and 45/88 (43 missing, listed above).
- Totals: members 512; present 468; empty 0; missing 44; misrooted 0; unsafe 0; unparsed 0; no-spawn 0; unavailable 0.
- Exit code 1 (two waves not settled, per the frozen contract).

## Not verified / not run

- The tool was not run and the oracle was not read.
- No `dead`/`failed` status was checked against agent-side records.
- The fleet-root basename search is bounded (depth ≤ 7, pruned) and not exhaustive.
