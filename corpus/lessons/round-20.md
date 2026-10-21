author: mori-shokunin (L1 MoriR20)
round: 20, attempt 1

# Round 20 — classified drift re-pin and per-seat wave settlement

Entering tip `2061780117e6ca637725004897bd288d3ba7e988` (round 19 admitted, MANIFEST closure
CloseMori19). Frozen contract and C2 cases landed at `e4d9384da2a0d7c39387ca29e9fbc7d6a4b2b935`
before any implementation; the C2 tool landed at `2eeae048c441ba4712c42380c347eb64b5a331fb`.

## Claims

- **C1 freshness (lowest-score tie with depth and calibration; calibration was selected in rounds
  17–19):** classify every token of the live r10 drift into the closed set with evidence, then
  re-pin. Sourced: S066, S067.
- **C2 coverage (capability, FR3 advance):** `tools/mori-wave-settlement.py` counts per-seat report
  presence for every dispatch file. Sourced: S068, S073, S074 (S073/S074 supersede S069/S071).

## Mistakes

| ID | Class | Evidence | Captured-by | Fix and fail-capability |
|---|---|---|---|---|
| M1 | survivor / wave settlement | r19 wave 1 returned 64 IDs and kept 16 reports; the 48 gaps were counted by hand at recovery and closure (`.ufo/waves/round-19/wave1-settlement.json`; MANIFEST round-19 mori closure notes) | none — `SURFACE waves` grades directories only (`.ufo/waves/round-20/build/CensusWavesSurface.md`) | C2 tool; shown to fail on that wave: r19 W1 `partial`, 16/64, exit 1 (`.ufo/waves/round-20/evidence/c2-live-mori.json`); QUALITY 64 |
| M2 | carried-red / freshness | r10 drift pin red rounds 12–19; r13 register free-text with no class or pointer; 8 of 50 entering tokens unclassified | none — QUALITY 41 allowed "stays carried debt" | closed-class register plus counting command; fails on the r13 register (8 unclassified; strict checker `unclassified=50 invalid=43`, `build/RegisterCheck.md`); QUALITY 65 |
| M3 | vacuous count (this round) | the round-20 seat protocol wrote `STATUS: started` first; under the frozen `present` = size>0 rule the markers counted present (57 of 76 at DraftSettlementNote's observation, 18 at ~10:40Z per `build/ContractReview.md`) | frozen C2 cases had no marker case | co-evolved R2 `stub`; removing it fails selftest case `r2-stub` (wave-2 `falsify/MutStubCounted.md`), though the frozen oracle cannot see it; live scan showed 6 stubs at 10:46Z; QUALITY 66 |
| M4 | oracle fixture defect (this round) | independent harness v0 wrote `taskCall: {"tasks": null}` for the frozen `no-spawn` case and scored the tool 13/14 (`evidence/c2-after-oracle-v0-fixture-defect.json`) | the differential run itself (tool selftest 21/21 then, harness 13/14) | harness repaired to the frozen setup text (`taskCall: null`); v0 bytes kept as `build/OracleHarness/c2-oracle-v0.py`; repaired 14/14; the repaired oracle still catches a planted frozen-case defect (wave-2 `falsify/ReviewLesson.md`) |
| M5 | number / reference drift (this round) | frozen `contract.md` says the r10 baseline is "nine census revisions old" (git: seven census commits since r10) and that the 48 were "found only by hand … (MANIFEST closure notes)" (the closure gives counts, not that wording) | wave-1 seats `build/VolatileContract.md` and `build/RevR19NoReport.md` caught both before integration | erratum only (frozen bytes stay): read "seven census commits" and "counted by hand at recovery/closure per wave1-settlement.json". An erratum is not fail-capable; the fail-capable part is M9. |
| M6 | classification dispute | `-FINDING:WATCHDOG_STALE` / `-FINDING:WAVE_UNSETTLED_AGE`: cause is live state, but the disappearance is false-clean; `build/VolatileContract.md` K2/K3, `build/C1Critic.md` and wave-2 `falsify/AdjudicateWaves.md` (BROKEN) recommend census-regression and no re-pin; `falsify/AdjudicateStale.md` and `FamWatchdog.md` keep live-state | none — the frozen closed set does not define its classes | L1 kept live-state by cause and pinned; register `blind_spot` + route; STALE fires again at the 10:51Z pre-pin drift; the 18 removed aggregator files carry souji per-path cleanup receipts. This is an open disagreement for the non-author closure, not a resolved fix; QUALITY 67 |
| M7 | misroot (this round) | DraftProvince first wrote its draft under the fleet root `.ufo/waves/round-20/build/DraftProvince/`, then copied it to the lane (`cmp` equal) and removed its own stray copy (`build/DraftProvince.md`); the stray no longer exists | wave context named the lane root; the seat self-detected | wave-2 `falsify/FleetMisrootEnd.md` found no mori file left at the fleet root; `.ufo/waves/round-20/final/AuditCase07.md` there is attributed to souji [INFERENCE] and not touched |
| M8 | scope | broad greps by several wave-1 seats (SrcK8sController, TokUnitOOS, ContractReview, TokWatchdog, TokWaves, GtMoriR19W1) surfaced names or snippets from `.ufo/interactive-sessions/`; their reports say nothing was opened or quoted | context forbade opening, not matching | wave-2 context forbade searching those trees at all; ReopenS071 still ran one whole-lane search (disclosed). Text bounds are not enforcement; no compliance credit |
| M9 | counting-command defect (this round) | the frozen C1 command set `LC_ALL=C` on `comm` only; under `en_US.UTF-8` it prints 37/33 instead of 8/0 (wave-2 `falsify/CountC1.md`, `DraftLog.md`) | wave-2 CountC1 / DraftScorecard | corrected command exports `LC_ALL=C` for the whole pipeline; receipt `evidence/c1-count.json`; the as-typed command is shown to fail (37) and the corrected one gives 8/0/7/0 |
| M10 | misclassification (this round) | register classed `+SURFACE:lane.audio/game-dev-2d/game-dev-3d` census-schema-change on a false "member at the pin" reason; their conf rows were removed by 99efc52 before the pin and re-declared by db25a48 (wave-2 `falsify/FamRosterLanes.md`) | wave-2 FamRosterLanes | reclassed roster-change (26/19/5); neither class blocks the pin |

## Co-evolved C2 refinements (after dispatch; frozen bytes unchanged)

R1 last matching trailer line after `rstrip` (96 tabi clone tasks end with `| godspeed`); R2 `stub`;
R3 `name_hint`; R4 `duplicate_of` / `unique_dispatch_sha256`; R5 `duplicate_report_paths`; plus a
missing-`taskCall` case and, after wave-2 mutant MutTraversalAllowed survived both detectors, an
in-lane `..` case (`r7-dotdot-inside-lane`) that kills it (`.ufo/waves/round-20/evidence/mut-r7/`).
Eight refinement selftest cases; the frozen 14 are loaded unchanged.

## Gate

| Row | URL | Access | Decision / located quote (≤25 words) |
|---|---|---|---|
| S066 | https://github.com/approvals/ApprovalTests.Python/blob/5d98f0c166ad2dde7ff60effb12427db8183805e/README.md | 2026-10-21 | Admit A (approval flow). “Either you will update the master because you expected the changes and they are good” — README.md line 75, Overview. |
| S067 | https://michaelfeathers.silvrback.com/characterization-testing | 2026-10-21 | Admit B. “The purpose of characterization testing is to document your system’s actual behavior, not check for the behavior you wish your system had.” — final sentence of the “It's a trick question.” paragraph. |
| S068 | https://docs.python.org/3/library/os.html | 2026-10-21 | Admit A. “This function normally follows symlinks; to stat a symlink add the argument follow_symlinks=False, or use lstat().” — os.stat entry. |
| S069 | https://docs.python.org/3/library/pathlib.html | 2026-10-21 | Admit A. “assumes that no symlinks are present in the path; call resolve() first if necessary to resolve symlinks.” — PurePath.relative_to, walk_up paragraph. |
| S073 | https://docs.python.org/3/library/pathlib.html | 2026-10-21 | Admit A, narrowed correction of S069 after wave-2 `ReopenS069` found its teaches over-reached and its locator loose. Same quote, located in the PurePath.relative_to Warning naming walk_up. |
| S074 | https://kubernetes.io/docs/concepts/architecture/controller/ | 2026-10-21 | Admit A, supersedes S071 after wave-2 `ReopenS071`: official project docs are tier A (CORPUS.md tier rule), and the observe-only clause was the lane's own boundary. Same quote and location as S071. |
| S075 | https://ftp.gnu.org/gnu/bash/bash-5.3.tar.gz (doc/bashref.texi) | 2026-10-21 | Admit A, queued; supersedes S070 after wave-2 `ReopenS070`: its teaches over-claimed an early-exit effect and PIPESTATUS scope. Same quote and anchors. |
| S076 | https://michaelfeathers.silvrback.com/characterization-testing | 2026-10-21 | Admit B; supersedes S067 after wave-2 `ReopenS067`: the census-baseline clause was the lane's application. Same quote and location. |
| S070 | https://ftp.gnu.org/gnu/bash/bash-5.3.tar.gz (doc/bashref.texi) | 2026-10-21 | Admit A, queued. “If set, the return value of a pipeline is the value of the last (rightmost) command to exit with a non-zero status” — bashref.texi:6063-6064. |
| S071 | https://kubernetes.io/docs/concepts/architecture/controller/ | 2026-10-21 | Admit B, vocabulary only. “responsible for making the current state come closer to that desired state.” — Controller pattern, third sentence. |
| S072 | https://en.wikipedia.org/wiki/Characterization_test | 2026-10-21 | Reject C. “a means to describe (characterize) the actual behavior of an existing piece of software” — lead sentence; adds nothing over S067. |

The L1 re-opened all seven URLs this round and matched each quote byte-for-text (S066 raw sha256
`db6b2f6a…de0b`; S070 tarball sha256 `0d5cd869…31ba`). Status/recheck/used-by changes to existing
rows: none; S067 is superseded by S076, S069 by S073, S070 by S075 and S071 by S074 (append-only corrections, old cells unchanged). In-place used-by changes (old → new): S066, S067 `corpus/knowledge/drift-repin-r20.md` → `+ corpus/lessons/round-20.md`; S068, S071 `corpus/knowledge/wave-settlement-r20.md` → `+ corpus/lessons/round-20.md` (S073 was written that way at insertion) (CORPUS.md: lessons citing a row are listed; wave-2 ReopenS071). The round-12 Bash lead has its source admitted (S070/S075); linkage to `knowledge/verdict-contract-r13.md` is pending.

## Routed round-19 items

`build/SpotcheckR19.md` (author-side lane pointer for the inline round-19 closure spot-check, R15):
S01 dispatch digest form — the round-20 receipt now records its serialization and a canonical
sha256; S02 exit-0-with-unreadable — documented in `knowledge/wave-settlement-r20.md` §2; S03 before
mode — `c2-before.json` is the harness's own run against the entering tree; R03 → QUALITY 68;
R11 → QUALITY 64 (cause labels need a named per-seat record). The 155 unresolved content-review
dispositions and the 39 unknown-cause r19 W1 seats stay carried, unchanged.

### Independent admit/reject spot-check

Verifier: **Main (orchestrator, non-author; not a wave seat)**, received 2026-10-21 by exact-id
coordination after the L1 request:

- **S068 — agree admit A.** The Gate quote is verbatim from the os.stat entry; tier A is right for
  primary Python documentation.
- **S072 — agree reject C.** Wikipedia is tertiary; its lead sentence adds nothing over S067; the
  conditional flip is properly scoped.

Wave-2 author-side re-openings (`.ufo/waves/round-20/falsify/Reopen*.md`) are separate evidence and
are not this outside check.
