# wave settlement r20 — per-seat report presence for dispatched swarm waves

source: `tools/mori-wave-settlement.py` (round 20; frozen contract `.ufo/waves/round-20/contract.md` C2,
frozen cases `.ufo/waves/round-20/frozen/c2-expected.json`, frozen at `e4d9384`; tool landed `2eeae04`).
Drafted from `.ufo/waves/round-20/build/DraftSettlementNote.md`; numbers below are L1 runs.
Sources: S068 (os.stat/lstat symlink semantics), S069 (pathlib lexical vs resolved containment),
S071 (desired vs current state vocabulary only — mori observes, it never reconciles).

## 1. What it answers

`SURFACE waves` in the census grades whole wave directories by marker files and age; it never
reads dispatch members or per-seat reports (`.ufo/waves/round-20/build/CensusWavesSurface.md`:
`probe_waves` `tools/mori-census.sh:865-932`; a wave with `results.json` and 0 of 3 seat reports is
classed settled). The settlement scan answers the per-seat question: for every
`ufo-swarm-wave-dispatch-v1` file under a lane's `.ufo/waves/`, which declared members have a
non-empty report at their `Report:` trailer path.

```
python3 tools/mori-wave-settlement.py scan --lane-root DIR [--fleet-root DIR] [--out FILE]
python3 tools/mori-wave-settlement.py --selftest     # 14 frozen + 7 refinement cases
```

## 2. Decision table

| Observation | Status / state | Never conclude |
|---|---|---|
| regular non-symlink file, size > 0, not the start stub | `present` | that the report's content is correct or final |
| regular file, size 0 | `empty` | hygiene truncation vs. never-finished (FR3 frontier) |
| whole content is `STATUS: started` | `stub` (round-20 seat protocol; ≤16 bytes read, nothing emitted) | that the seat is still running |
| no file under lane root, same relative path exists under `--fleet-root` | `misrooted` | that it is safe to move it (owner L1 / souji routing) |
| no file anywhere checked | `missing` | **dead, failed or killed** — a missing report is not a dead seat |
| trailer absolute, contains `..`, or escapes the root | `unsafe` (never stat'ed) | — |
| no task line matches the trailer | `unparsed` | — |
| every member present | wave `settled` | that the wave's results are accepted (kumitate owns result semantics) |
| some present | `partial` | — |
| none present, ≥1 member | `unsettled` | that the wave was dispatched (see §4) |
| `taskCall: null` | `no-spawn` | — |
| no member with a parseable safe path (incl. missing `taskCall`) | `unavailable` | — |

Exit 0 = every wave `settled`/`no-spawn`; 1 = any other state; 2 = usage or unreadable lane root.
Exit 1 is an observation, not an error. Exit 0 can coexist with `unreadable_json > 0` (frozen case
`malformed-dispatch`): always read the count.

## 3. Co-evolved refinements (after dispatch; frozen bytes unchanged)

R1 trailer = last *matching* line after `rstrip` (the frozen wording "the LAST line of a task matching"
— a `| godspeed` envelope can follow it: 96 tabi clone tasks, `build/TrailerVariants.md`); R2 `stub`;
R3 `name_hint` for `preview|undispatched|not-dispatched|validation` filenames (shape only); R4
`duplicate_of` + `unique_dispatch_sha256` (byte-identical copies exist in kengaku, tameshi, tabi);
R5 `duplicate_report_paths`. Each has a selftest case (`REFINEMENT_CASES`).

## 4. Limits (measured)

- A dispatch file is not dispatch evidence. Two name-hinted payloads were never dispatched
  (mado `dispatch-preview.json`, revenger `rendered-undispatched.json`), twelve name-hinted ones were
  executed (`build/ContractReview.md`); kama r19 falsify (66) and r21 build (86) were refused at the
  job cap and read `unsettled` exactly like a dispatched wave whose reports were lost
  (`build/GtLaneKama.md`). Spawn records live in lane-specific ledgers; binding them is frontier.
- Successor reports are not linked: kake r22/w2 seats re-run as r23/w1 still read `missing`
  (`build/GtLaneKake.md`); tabi r12/r13 wrote 63 same-stem `.txt` files beside missing `.md` paths.
- Member names may contain words like `dead`; the vocabulary guarantee covers the tool's own state words.
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
- Fleet scan 10:46:50Z (`evidence/c2-live-fleet.json`): 21 lanes, 196 dispatch files; static lanes
  match their ground-truth seats (chousa 120/136, kaidoku 824/959, kake 261/325, kasegi 44/64,
  kengaku 376/387, kumitate 468/512, mado 914/1030, revenger 0/32, souji 662/783 with 1 misrooted,
  tameshi 857/965, tsukuroi 767/834); kama, kagi, tabi were mid-round and moved between snapshots.
