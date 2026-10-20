# SeparateThree — C1/C2/C3 causal separability

Seat: `MoriR17.SeparateThree-4` (leaf, report only). Attacked the settled claim that C1 coverage, C2 operability, and C3 calibration each verify with the other implementations absent; that the context checker is conformance support; that calibration 5 is the lowest-axis target; and that C3 was declared before L1 measurements.

No tool was installed or updated. No selftest, gate, census, or misroot probe was rerun. No VCS mutation.

## Axes

| Axis | Round-17 claim | Entering score at `24526ea` (`SCORECARD.md:979-984`) |
|---|---|---|
| coverage | C1 seat terminal-at-scan | 6 |
| operability | C2 branch-anchored census | 7 |
| calibration | C3 blind-sweep witness | 5 |
| depth, freshness | no round-17 claim | 5 and 5 (tie with calibration) |
| adjacency | no round-17 claim | 6 |

`AXES.md:31-33` requires claims to be causally separable (each verifiable without the others having landed), on distinct axes, with at least one on the lowest-scoring non-retired axis. Calibration is tied for that lowest score with depth and freshness. It is not uniquely lowest.

## Finding

Cross-claim execution is separable: the three counting commands name disjoint programs, and none of the four round-17 tools references another claim's implementation. That part of the contract sentence at `contract.md:29-30` was not falsified.

C3's own before leg does not meet the absence pattern C1 and C2 use. Both `evidence/c3-before.json` and `evidence/c3-after.json` invoke the landed `tools/mori-misroot-sweep.py`. The legacy miss is `--legacy-pathspec` on that same binary. There is no frozen legacy sweeper and no receipt whose tool path is absent. Deleting the detector removes both sides of the published `1→0` together. The before number is a mode of the after implementation, not an independently landed implementation.

The same commit cites a separability memo that still classifies that detector as conformance-only, and whose contract line anchors now fall inside the C3 paragraph that was inserted above C1.

## Evidence

### 1. Counting argv are disjoint (read from committed receipts)

| Claim | Receipt | Started (`-03:00`) | Program named | Prior implementation in argv |
|---|---|---|---|---|
| C1 | `evidence/c1-before.json:3-14` | 16:32:40.855 | `tools/mori-round17-seat-regressions.py` | `--tool` `frozen/absent-seat-tool.py` (gate stdout: path does not exist; 54 capability_absent) |
| C1 | `evidence/c1-after.json:3-13` | 16:32:40.904 | same gate | `--tool` `tools/mori-seat-terminal.py` |
| C2 | `evidence/c2-before.json:3-14` | 16:32:55.823 | `tools/mori-round17-jj-regressions.py` | `--census` `frozen/mori-census.sh` |
| C2 | `evidence/c2-after.json:3-13` | 16:32:57.594 | same gate | `--census` `tools/mori-census.sh` |
| C3 | `evidence/c3-before.json:3-17` | 16:34:52.901 | `tools/mori-misroot-sweep.py` | `--legacy-pathspec` `.ufo/waves` `.ufo/reports` on that binary |
| C3 | `evidence/c3-after.json:3-13` | 16:34:52.934 | same binary | no pathspec |

`evidence/count-c{1,2,3}.json` are `jq` over those receipts at 16:35:15, all `measured_commit` `273aa74ab73701f41fea38ec7bd1c47b4b2bfbc7`. None of the six argv lists a sibling claim's program.

Source cross-references (workspace `rg`, rc 0, no matches):

- `tools/mori-census.sh` for `mori-seat-terminal|mori-misroot|mori-round17`
- `tools/mori-round17-jj-regressions.py` for `mori-seat-terminal|mori-misroot|context-check`
- `tools/mori-round17-seat-regressions.py` for `mori-census|mori-misroot|context-check`
- `tools/mori-misroot-sweep.py` and `tools/mori-seat-terminal.py` for the other claim tools

C3's scanned sandbox reported `regular_files` 0 then 2 (`c3-before` stdout `scan`; `c3-after` stdout `scan`). That is the planted pair, not the seat tool or the census. [INFERENCE] The two files were already planted for the before scan: the detector does not create them, and the after scan started 1 ms after the before scan ended. The before receipt does not record a directory listing or a content digest, so an empty tree is the same JSON as a pathspec miss (`untracked_entries` 0, `bytes_read` 0).

### 2. C3 admission counter does not bind the byte-exact witness

Contract `contract.md:22-25` requires a sandbox retaining byte-exact `MoriR16.Lesson`, a legacy miss, a no-pathspec find, and unclaimed sibling/tracked controls.

The SCORECARD reproduction command (`SCORECARD.md:1048`) is:

```sh
jq -s '[.[] | (.stdout|fromjson) | 1 - ([.candidates[]|select(.path=="MoriR16.Lesson")]|length)]' \
  evidence/c3-before.json evidence/c3-after.json
```

`evidence/count-c3.json:18` records stdout `[1, 0]`, rc 0. That expression does not read exit status, `legacy_pathspec`, `matched_in`, sibling path, or sha256. `c3-after` stdout happens to show one candidate, `matched_in: ["path"]`, `size_bytes` 847. It does not emit a digest. The second of the two regular files is unnamed, so the receipt does not show that the sibling was `TabiR16.Lesson`.

`frozen/c3-expected.json:5-12` pins sha256 `15f9f82d707d5c79b11643eed1ab4754b6959d2bede5887e07364442ada5510e`, sibling `TabiR16.Lesson`, and `default_expected_matched_in: ["path"]`. The counting command does not open that file.

The in-tool selftest sibling is a different control: `tools/mori-misroot-sweep.py:370-371` uses `TabiNote.md` and the text `TabiR17`, not `TabiR16.Lesson`. `evidence/misroot-selftest.json` stdout records `fixture_sha256` `15f9f82d…` and `planted_found_with_legacy_pathspec: false`. Lesson M10 treats seat selftests as non-admission; the same split applies here. The selftest digest does not repair the admission counter.

`_status_argv` (`mori-misroot-sweep.py:97-105`) does pass pathspecs through to git; the before receipt's `git_command` includes them. The miss is not a hard-coded empty candidate list. It is still not a second implementation. The historical command in the module docstring (`mori-misroot-sweep.py:6-7`) is `git status --porcelain -- .ufo/waves .ufo/reports`. The receipt adds `--porcelain=v1 -z --untracked-files=all`. For one root-level file the pathspec miss agrees. [INFERENCE] Nested untracked directories would not: porcelain's default collapsing differs from `--untracked-files=all`.

### 3. Cited separability memo contradicts the three-claim contract

`LOG.md:1139` (present in `273aa74`) says `` `build/ClaimSeparability.md` records independent scopes. ``

That file's only commit is `273aa74` (blob `fc92d20023cf2818a8136717d5a617273b53669f`, identical at HEAD). It never names C3 as a claim. `build/ClaimSeparability.md:18` says the misroot sweep "is also conformance-only" and "does not implement either feature."

Line anchors were written against a shorter contract and were not moved when C3 was inserted at `contract.md:21-27`:

| Memo cite | What it claims to point at | Where that line is now |
|---|---|---|
| `contract.md:24-67` (`ClaimSeparability.md:7`) | C1 tool contract | line 24 is still the C3 sentence "root file while the no-pathspec…" |
| `contract.md:69-78` | C1 gate | C1 fixtures header is line 77; the gate command is line 82 |
| `contract.md:9-22` | C1 and C2 axis assignment | lines 21-22 are the C3 claim |

`contract.md:27` says the MisrootSweep work "is no longer merely unclaimed conformance work." The memo committed in the same snapshot still says it is. Those two sentences cannot both be the separability record.

### 4. Context checker stays conformance support

`tools/mori-round17-context-check.py:6-75` is a static phrase check over spec `context` strings. It sets `claims_runtime_prevention` false and does not import or execute the seat tool, the census, or the misroot sweep.

Committed results: `evidence/context-check-wave1.json` and `evidence/context-check-wave2.json` are `CONTEXT_OK`, `static_only: true`, `claims_runtime_prevention: false`. They are not inputs of `count-c1.json`, `count-c2.json`, or `count-c3.json`.

Attribution mix, not a fourth claim: `PINNED_INPUTS.json:11` stores `tools/mori-round17-context-check.py` in the same `files` object as the three claim binaries. A conformance-only byte change moves the ledger SCORECARD calls the claim input pin. The counters themselves do not hash it.

### 5. Calibration 5 and declaration time

Entering active row, parent `24526ea`, `SCORECARD.md:979-984`: coverage 6, operability 7, depth 5, freshness 5, calibration 5, adjacency 6. `## Retired` is none (`ScorecardAxisCheck.md:72`, consistent with `SCORECARD.md:28-30` as cited there). C3 on calibration works one axis in the three-way tie at 5. It does not dissolve the tie. Depth and freshness stay unworked. That satisfies "at least one" under `AXES.md:33`. It does not make calibration the unique lowest axis. The contract's "lowest owned axis 6" wording remains the reading `ScorecardAxisCheck.md` rejected; C3 is the later patch for the literal reading.

Timing of the committed C3 sentence versus L1 probes:

| Event | Time |
|---|---|
| Wave1 registry `build/swarm-registry.json` `createdAt` / `updatedAt` | `2026-10-20T18:38:06Z` / `18:54:21Z` (15:38:06 / 15:54:21 `-03:00`) |
| `273aa74` author date | `2026-10-20T15:26:13-03:00` |
| `273aa74` committer date | `2026-10-20T16:31:56-03:00` |
| First L1 probe `c1-before` `started_at` | `2026-10-20T16:32:40.855229-03:00` |
| Measurement commit `5c1dfb8` | `2026-10-20T16:37:09-03:00` |

`git grep` of `24526ea` for `C3 calibration` in `contract.md` and `SCORECARD.md` returned no hits (rc non-zero, empty). The same string is in `273aa74:.ufo/waves/round-17/contract.md:21`. Probe receipts set `measured_commit` to `273aa74`, so they ran against a tree that already contained that line. Committer date is after the wave1 registry `updatedAt` and before `c1-before`.

The author date is before wave1 `createdAt`. It cannot date the C3 sentence: the finalized tree also contains `build/ClaimSeparability.md`, which did not exist as a committed blob before `273aa74`. [INFERENCE] Author date was preserved across a later snapshot (amend or `GIT_AUTHOR_DATE`); committer date is the snapshot clock. The "before L1 measurement" clause holds for the committed tree. It is not evidenced by the author timestamp, and there is no intermediate commit that contains C3 text without the three implementations.

## Contradiction (not a score)

- Implementations: C1's absent path, C2's frozen census, and C3's legacy flag are three different "before" objects. Only the first two are implementations that can be missing while the claim gate still runs.
- Documents: `contract.md:27-30` makes the sweep a separable claim. `ClaimSeparability.md:18` and `LOG.md:1139` still treat the sweep as non-claim conformance and cite that memo for independent scopes.
- Witness: `count-c3.json` reports `1→0` from candidate-path cardinality. `frozen/c3-expected.json` and the selftest require a digest, a named sibling, and path-only match. The counter does not check those, and the selftest sibling is `TabiNote.md`, not `TabiR16.Lesson`.

## Proposed move

One ledger change, no edit to the seat classifier or the census.

Keep C1 and C2 receipts as they are. Replace the C3 before leg with the round-16 git command shape (`git status --porcelain -- .ufo/waves .ufo/reports`) run in a sandbox whose pre-scan sha256 of `MoriR16.Lesson` equals `frozen/MoriR16.Lesson`, and keep the after leg as `mori-misroot-sweep.py` with no pathspec. Accept `1→0` only when that digest matches, the sibling path from `frozen/c3-expected.json` is present and absent from `candidates`, and the receipt names neither `mori-seat-terminal.py` nor `mori-census.sh`. Stop citing `build/ClaimSeparability.md` as the three-claim separability record; leave it as the wave-1 C1/C2 memo with stale line numbers.

Affected axis: calibration. Coverage and operability commands stay on their own binaries. Depth, freshness, and adjacency are untouched.

## Risks

A raw `git status --porcelain` before-leg can disagree with `--legacy-pathspec` on nested untracked directories because of `--untracked-files`. The contracted witness is one root file; the two commands still need one recorded comparison on that sandbox, not an assumption they match. Tightening the counter can turn today's `[1, 0]` into an incomplete receipt until a pre-scan digest is stored. That is the calibration gap becoming visible. It does not change seat classes or census findings.

## Verification performed

Read-only. `git log` / `git rev-parse` / `git grep` / `git diff-tree --name-only` / `git show 24526ea:SCORECARD.md` on `/home/vgpnk/Projects/shokunin/mori-shokunin`, rc 0 except the `24526ea` `C3 calibration` grep, which was empty. File reads of `contract.md`, `AXES.md`, `ClaimSeparability.md`, `ScorecardAxisCheck.md`, `PINNED_INPUTS.json`, the six probe wrappers, the three count receipts, `c3-capture-recipe.json`, `frozen/c3-expected.json`, context-check evidence, and the cited tool ranges. `rg` cross-reference searches listed above, no matches.

Not run: selftests, seat/jj/misroot gates, live probes, pacman, journal queries. No `/tmp` writes.
