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
  presence for every dispatch file. Sourced: S068, S069, S071.

## Mistakes

| ID | Class | Evidence | Captured-by | Fix and fail-capability |
|---|---|---|---|---|
| M1 | survivor / wave settlement | r19 wave 1 returned 64 IDs and kept 16 reports; the 48 gaps were counted by hand at recovery and closure (`.ufo/waves/round-19/wave1-settlement.json`; MANIFEST round-19 mori closure notes) | none — `SURFACE waves` grades directories only (`.ufo/waves/round-20/build/CensusWavesSurface.md`) | C2 tool; shown to fail on that wave: r19 W1 `partial`, 16/64, exit 1 (`.ufo/waves/round-20/evidence/c2-live-mori.json`); QUALITY 64 |
| M2 | carried-red / freshness | r10 drift pin red rounds 12–19; r13 register free-text with no class or pointer; 8 of 50 entering tokens unclassified | none — QUALITY 41 allowed "stays carried debt" | closed-class register plus counting command; fails on the r13 register (8 unclassified; strict checker `unclassified=50 invalid=43`, `build/RegisterCheck.md`); QUALITY 65 |
| M3 | vacuous count (this round) | the round-20 seat protocol wrote `STATUS: started` first; under the frozen `present` = size>0 rule 18 markers counted present at ~10:40Z (`build/ContractReview.md`, `build/DraftSettlementNote.md`) | frozen C2 cases had no marker case | co-evolved R2 `stub` status; selftest `r2-stub` fails if removed; live scan showed 6 stubs at 10:46Z; QUALITY 66 |
| M4 | oracle fixture defect (this round) | independent harness v0 wrote `taskCall: {"tasks": null}` for the frozen `no-spawn` case and scored the tool 13/14 (`evidence/c2-after-oracle-v0-fixture-defect.json`) | the differential run itself (tool selftest 14/14 vs harness 13/14) | harness repaired to the frozen setup text (`taskCall: null`); v0 bytes kept as `build/OracleHarness/c2-oracle-v0.py`; repaired 14/14 |
| M5 | number / reference drift (this round) | frozen `contract.md` says the r10 baseline is "nine census revisions old" (git: seven census commits since r10, `build/VolatileContract.md`) and that the 48 were "found only by hand … (MANIFEST closure notes)" (the closure gives counts, not that wording, `build/RevR19NoReport.md`) | none | erratum here; the frozen bytes stay unchanged: read "seven census commits" and "counted by hand at recovery/closure per wave1-settlement.json" |
| M6 | classification dispute | `-FINDING:WATCHDOG_STALE` / `-FINDING:WAVE_UNSETTLED_AGE`: cause is live state, but the disappearance is false-clean (`build/VolatileContract.md` H2/H3, `build/C1Critic.md`) | none — the closed set has no false-clean marker | register `blind_spot` field and route; STALE observed firing again at 10:51Z pre-pin drift; QUALITY 67; adjudication left to wave 2 and the non-author closure |
| M7 | misroot (this round) | DraftProvince first wrote under `/home/vgpnk/Projects/shokunin/.ufo/waves/round-20/build/DraftProvince/` (fleet root), then copied to the lane (`cmp` equal) and removed its own stray file (`build/DraftProvince.md`) | wave context named the lane root; the seat self-detected | L1 no-pathspec sweep at round end (report); fleet `.ufo/waves/round-20/final/AuditCase07.md` belongs to souji (`build/MisrootSweep.md`) and is not touched |
| M8 | scope | broad greps by SrcK8sController, TokUnitOOS, ContractReview, TokWatchdog, TokWaves surfaced snippets from `.ufo/interactive-sessions/*.jsonl`; none opened or quoted (their reports) | context forbade opening, not matching | wave-2 context restricts every search to named paths and excludes `.ufo/interactive-sessions/`, `.ufo/worktrees/`, `.jj/`; breaches disclosed, no compliance credit |

## Co-evolved C2 refinements (after dispatch; frozen bytes unchanged)

R1 last matching trailer line after `rstrip` (96 tabi clone tasks end with `| godspeed`); R2 `stub`;
R3 `name_hint`; R4 `duplicate_of` / `unique_dispatch_sha256`; R5 `duplicate_report_paths`; plus a
missing-`taskCall` case. Seven refinement selftest cases; the frozen 14 are loaded unchanged.

## Gate

| Row | URL | Access | Decision / located quote (≤25 words) |
|---|---|---|---|
| S066 | https://github.com/approvals/ApprovalTests.Python/blob/5d98f0c166ad2dde7ff60effb12427db8183805e/README.md | 2026-10-21 | Admit A (approval flow). “Either you will update the master because you expected the changes and they are good” — README.md line 75, Overview. |
| S067 | https://michaelfeathers.silvrback.com/characterization-testing | 2026-10-21 | Admit B. “The purpose of characterization testing is to document your system’s actual behavior, not check for the behavior you wish your system had.” — final sentence of the “It's a trick question.” paragraph. |
| S068 | https://docs.python.org/3/library/os.html | 2026-10-21 | Admit A. “This function normally follows symlinks; to stat a symlink add the argument follow_symlinks=False, or use lstat().” — os.stat entry. |
| S069 | https://docs.python.org/3/library/pathlib.html | 2026-10-21 | Admit A. “assumes that no symlinks are present in the path; call resolve() first if necessary to resolve symlinks.” — PurePath.relative_to, walk_up paragraph. |
| S070 | https://ftp.gnu.org/gnu/bash/bash-5.3.tar.gz (doc/bashref.texi) | 2026-10-21 | Admit A, queued. “If set, the return value of a pipeline is the value of the last (rightmost) command to exit with a non-zero status” — bashref.texi:6063-6064. |
| S071 | https://kubernetes.io/docs/concepts/architecture/controller/ | 2026-10-21 | Admit B, vocabulary only. “responsible for making the current state come closer to that desired state.” — Controller pattern, third sentence. |
| S072 | https://en.wikipedia.org/wiki/Characterization_test | 2026-10-21 | Reject C. “a means to describe (characterize) the actual behavior of an existing piece of software” — lead sentence; adds nothing over S067. |

The L1 re-opened all seven URLs this round and matched each quote byte-for-text (S066 raw sha256
`db6b2f6a…de0b`; S070 tarball sha256 `0d5cd869…31ba`). Status/recheck/used-by changes to existing
rows: none. The round-12 Bash lead is resolved by S070 (lead line rewritten as resolved).

## Routed round-19 items

`build/SpotcheckR19.md` (author-side lane pointer for the inline round-19 closure spot-check, R15):
S01 dispatch digest form — the round-20 receipt now records its serialization and a canonical
sha256; S02 exit-0-with-unreadable — documented in `knowledge/wave-settlement-r20.md` §2; S03 before
mode — `c2-before.json` is the harness's own run against the entering tree; R03 → QUALITY 68;
R11 → QUALITY 64 (cause labels need a named per-seat record). The 155 unresolved content-review
dispositions and the 39 unknown-cause r19 W1 seats stay carried, unchanged.
