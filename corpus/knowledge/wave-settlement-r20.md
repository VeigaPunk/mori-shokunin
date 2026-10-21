# wave settlement r20 — per-seat report presence for dispatched swarm waves

source: `tools/mori-wave-settlement.py` (round 20; frozen contract `.ufo/waves/round-20/contract.md` C2,
frozen cases `.ufo/waves/round-20/frozen/c2-expected.json`, frozen at `e4d9384`; tool landed `2eeae04`).
Drafted from `.ufo/waves/round-20/build/DraftSettlementNote.md`; numbers below are L1 runs.
Sources: S068 (os.stat/lstat symlink semantics), S073 (supersedes S069: lexical containment assumes no symlinks; the `..`/absolute rejection is the tool's own rule),
S074 (supersedes S071: declared vs current state vocabulary; mori's observe-only boundary is its own, not the source's).
verified-at: 2026-10-21, tool sha256 79e7f9dedb8a16a9d9257644045c56c57ca97b27ab94640ca487b330527b28f9 (selftest 23/23; oracle 14/14)
recheck: `python3 tools/mori-wave-settlement.py --selftest` and `python3 .ufo/waves/round-20/build/OracleHarness/c2-oracle.py --tool tools/mori-wave-settlement.py --out /tmp/c2.json` (counts.matched 14); live: `scan --lane-root . --fleet-root ..` r19 W1 16/64

## 1. What it answers

`SURFACE waves` in the census grades whole wave directories by marker files and age; it never
reads dispatch members or per-seat reports (`.ufo/waves/round-20/build/CensusWavesSurface.md`:
`probe_waves` `tools/mori-census.sh:865-932`; a wave with `results.json` and 0 of 3 seat reports is
classed settled). The settlement scan answers the per-seat question: for every
`ufo-swarm-wave-dispatch-v1` file under a lane's `.ufo/waves/`, which declared members have a
non-empty report at their `Report:` trailer path.

```
python3 tools/mori-wave-settlement.py scan --lane-root DIR [--fleet-root DIR] [--out FILE]
python3 tools/mori-wave-settlement.py --selftest     # 14 frozen + 9 refinement cases
```

## 2. Decision table

| Observation | Status / state | Never conclude |
|---|---|---|
| regular non-symlink file, size > 0, not the start stub | `present` | that the report's content is correct or final |
| regular file, size 0 | `empty` | hygiene truncation vs. never-finished (FR3 frontier) |
| whole content is `STATUS: started` | `stub` (round-20 seat protocol; ≤16 bytes read, nothing emitted) | that the seat is still running |
| no file under lane root, same relative path exists under `--fleet-root` | `misrooted` | that it is safe to move it (owner L1 / souji routing) |
| no regular file at the trailer path (absent, or a symlink, directory or unreadable leaf) and not under `--fleet-root` | `missing` | **dead, failed or killed**; also not "never written": the seat may have written elsewhere (tabi r12/r13 wrote `.txt` as their Acceptance said, not the trailer's `.md`) |
| trailer absolute, contains `..`, escapes the root, or crosses a symlinked parent directory | `unsafe` (never followed) | — |
| no task line matches the trailer | `unparsed` | — |
| every member present | wave `settled` | that the wave's results are accepted (kumitate owns result semantics) |
| some present | `partial` | — |
| none present, ≥1 member | `unsettled` | that the wave was dispatched, or that its seats ran (see §4) |
| `taskCall: null` | `no-spawn` | — |
| no member with a parseable safe path (incl. missing `taskCall`) | `unavailable` | — |

Exit 0 = every wave `settled`/`no-spawn`; 1 = any other state; 2 = usage, unreadable lane root, or a
`--fleet-root` that is not a directory (the fleet root is resolved with realpath first).
Exit 1 is an observation, not an error. Exit 0 can coexist with `unreadable_json > 0` (frozen case
`malformed-dispatch`): always read the count.

## 3. Co-evolved refinements (after dispatch; frozen bytes unchanged)

R1 trailer = last *matching* line after `rstrip` (the frozen wording "the LAST line of a task matching"
— a `| godspeed` envelope can follow it: 96 tabi clone tasks, `build/TrailerVariants.md`); R2 `stub`;
R3 `name_hint` for `preview|undispatched|not-dispatched|validation` filenames (shape only); R4
`duplicate_of` + `unique_dispatch_sha256` (byte-identical copies exist in kengaku, tameshi, tabi);
R5 `duplicate_report_paths`; R6 a missing `taskCall` key reads `unavailable`; R7 an in-lane `..`
trailer is `unsafe` (added after a wave-2 mutant survived). Each has a selftest case
(`REFINEMENT_CASES`). The wave-level `missing` list names every member that is not `present`
(stub, empty, misrooted and missing alike); `counts` separates them. A report path that is a
symlink, a directory or not stat-able also reads `missing`. `name_hint` also fires on executed
`validation` payloads.

## 4. Limits (measured)

- A dispatch file is not dispatch evidence. Two name-hinted payloads were never dispatched
  (mado `dispatch-preview.json`, revenger `rendered-undispatched.json`), twelve name-hinted ones were
  executed (`build/ContractReview.md`); kama r19 falsify (66, refused at the job cap) and r21 build
  (86, no spawn recorded at scan time; cause not established) read `unsettled` exactly like a dispatched wave whose reports were lost
  (`build/GtLaneKama.md`). Spawn records live in lane-specific ledgers; binding them is frontier.
- Successor reports are not linked: 18 of the 21 missing kake r22/w2 seats have hand-derived,
  re-scoped successors in r23/w1 (3 have none) and still read `missing` (`.ufo/waves/round-20/falsify/KakeSuccessors.md`)
  (`build/GtLaneKake.md`); tabi r12/r13 wrote 63 same-stem `.txt` files beside missing `.md` paths.
- Zero discovered waves exit 0 (`waves: []`), and a symlinked `.ufo/waves` is not followed, so an
  unsettled dispatch behind it is invisible and still exits 0 (`.ufo/waves/round-20/falsify/CountC2.md`):
  read `totals.waves` before trusting exit 0. The frozen oracle does not cover the lexical `..` rule;
  only selftest case `r7-dotdot-inside-lane` does.
- Missing is mostly not "spawned and silent": over 44 non-settled fleet waves (708 missing members), at
  least 164 and at most 524 were declared-only, never spawned; at least 13 waves were refused at the job
  cap and later spawned (`.ufo/waves/round-20/falsify/DeclaredVsDispatched.md`). A spawn with no dispatch
  JSON (kagi round-24 `fix`, 2 seats) is invisible (`falsify/LiveKagi.md`); reports written to an
  off-trailer path inside the lane (kama r21 `out/<name>/`) read `missing`; `misrooted` checks only the
  fleet root. `--out` does not create its parent directory (exit 2).
- Discovery is JSON-only: a markdown dispatch receipt (revenger `kaika-r1/dispatch.md`, 10 members, all
  reports present) is invisible; a `.json` whose lstat fails (non-searchable directory) is skipped
  without a counter; totals are not de-duplicated across byte-identical dispatch copies (use
  `duplicate_of`) (`.ufo/waves/round-20/falsify/LiveRevenger.md`, `DiffAltImpl.md`).
- Member names may contain words like `dead`; the vocabulary guarantee covers the tool's own state words.
- Safety residuals (`.ufo/waves/round-20/falsify/SentinelTool.md`): path checks are lstat-then-open, so a
  concurrent writer can race them; no size or count limit on dispatch JSON; output carries the
  absolute `lane_root`, and byte determinism holds per path spelling, not across path aliases.
- Live trees move during a scan (tabi clone tree appeared mid-scan); cite the scan time.

## 5. Measurements (L1, 2026-10-21)

- Oracle (independent harness `build/OracleHarness/c2-oracle.py`, never imports the tool):
  entering tree `capability_absent` 14 → after 14/14 matched (`evidence/c2-before.json`,
  `evidence/c2-after.json`). The harness v0 had a fixture defect (`no-spawn` wrote `{"tasks":null}`)
  and scored 13/14; repaired, v0 bytes and red result retained (`c2-oracle-v0.py`,
  `evidence/c2-after-oracle-v0-fixture-defect.json`).
- Lane scan 10:46:42Z (`evidence/c2-live-mori.json`): all ten historical mori waves reproduce the
  independent wave-1 ground-truth seats exactly — r13 32/32, r14 32/32, r15 64/64, r16 64/64,
  r17 70/70 and 64/64, r18 53/68 (15 missing = the 15 names in `wave1-dead-seats.json`) and 67/67,
  **r19 W1 16/64 (48 missing), W2 48/70 (22 missing)**.
- Fleet scan started 10:46:50Z, file written 10:46:53Z (`evidence/c2-live-fleet.json`): 21 lanes, 196 dispatch files; static lanes
  match their ground-truth seats (chousa 120/136, kaidoku 824/959, kake 261/325, kasegi 44/64,
  kengaku 376/387, kumitate 468/512, mado 914/1030, revenger 0/32, souji 662/783 with 1 misrooted,
  tameshi 857/965, tsukuroi 767/834); kama, kagi, tabi were mid-round and moved between snapshots.
