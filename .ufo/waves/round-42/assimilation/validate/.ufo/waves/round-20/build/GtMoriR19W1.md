# GtMoriR19W1: round-19 wave 1 per-seat settlement, manual ground truth (C2)

Result: 16 of 64 members present; 48 missing; 0 empty; 0 misrooted. Every recorded closure count agrees with this manual check.
Seat: leaf, read-only, no subagents, no census or settlement tool run. Tools installed or updated: none.

## Method
- Source: `.ufo/waves/round-19/wave1-run.json`, `taskCall.tasks` (64 entries, names unique). Names and task text are identical to `wave1-taskcall.json` (checked with jq).
- Trailer extraction with `/usr/bin/jq` 1.8.2: last line of each `task` matching `^Report: write your scoped findings to (\S+)$`. Each task has exactly one line containing `write your scoped findings`, and it is the final line. Ten tasks contain a second occurrence of the word "Report" in body text, but none has a second trailer-form line. All 64 paths match `^\.ufo/waves/round-19/build/[A-Za-z0-9]+\.md$`, with no `..`, no absolute path, and no duplicates.
- Presence: `stat -c '%F|%s|%n'` (does not follow links) at `/home/vgpnk/Projects/shokunin/mori-shokunin/<path>`. If ABSENT, the same relative path was checked at `/home/vgpnk/Projects/shokunin/<path>`. Directory components `.ufo`, `.ufo/waves`, `.ufo/waves/round-19`, `.ufo/waves/round-19/build` are real directories, not links.
- Classifier probes: a throwaway empty file reported `regular empty file|0`; a throwaway symlink reported `symbolic link`. Both probes were deleted.
- Environment: bare `jq` on PATH is `~/.local/bin/jq`, a regular 2,267,912-byte file; `jq --version` prints `jaq 3.1.1`. The GNU build is `/usr/bin/jq` (jq-1.8.2, root-owned), which I used throughout. Any contract command that calls bare `jq` runs jaq on this host. [INFERENCE] its output may differ from jq on some filters; not tested.

## Totals
| measure | count |
|---|---|
| members (taskCall.tasks) | 64 |
| present (regular, non-symlink, >0 B) | 16 |
| empty (0 B) | 0 |
| missing | 48 |
| misrooted (absent at lane root; regular file at same relative path under fleet root) | 0 |
| symlink | 0 |
| unsafe | 0 |
| unparsed | 0 |
| wave state (C2 rule: ≥1 present, ≥1 not) | partial |

Present sizes: 1,307 to 6,733 B. The fleet root has no `.ufo/waves/round-19/` directory, so all 64 fleet-root checks returned ABSENT.

## name | status
| name | status |
|---|---|
| ContentGate | present |
| FreezeMetadata | present |
| RegressionHarness | missing |
| Content01 | missing |
| Content02 | missing |
| Content03 | present |
| Content04 | missing |
| Content05 | missing |
| Content06 | missing |
| Content07 | missing |
| Content08 | missing |
| Content09 | missing |
| Content10 | missing |
| Content11 | missing |
| Content12 | missing |
| Content13 | missing |
| Content14 | missing |
| Content15 | missing |
| Content16 | missing |
| Content17 | missing |
| Content18 | missing |
| Content19 | present |
| Content20 | missing |
| Content21 | missing |
| Content22 | missing |
| Content23 | missing |
| Content24 | present |
| Content25 | present |
| Content26 | missing |
| Content27 | present |
| Content28 | missing |
| Content29 | missing |
| Content30 | missing |
| Content31 | missing |
| Content32 | missing |
| Content33 | missing |
| Content34 | missing |
| Content35 | missing |
| Content36 | missing |
| QuoteS055 | present |
| QuoteS057 | missing |
| QuoteS059 | present |
| QuoteS063 | present |
| SrcGitRevision | missing |
| SrcHashlibReject | present |
| GateCoverage | missing |
| GatePrivacy | missing |
| GateDigests | missing |
| MetaInput | missing |
| MetaTopology | missing |
| MetaErrors | missing |
| HarnessC1 | missing |
| HarnessC2 | missing |
| CriticScope | present |
| CriticProvenance | present |
| CriticTrends | present |
| ConnectPrivacy | missing |
| ConnectObserve | missing |
| ConnectOracle | missing |
| DraftLesson | present |
| DraftCapabilities | missing |
| DraftCorrections | missing |
| FindHomeResiduals | missing |
| FindSW1Content | present |

## Comparison with recorded counts
| source (read-only) | recorded for round-19 wave 1 | manual result | verdict |
|---|---|---|---|
| `.ufo/waves/round-19/wave1-settlement.json` | returned 64; `reports_present` 16; `known_provider_failed` 8; `known_cancelled` 1; `no_report_terminal_cause_unestablished` 39 | present 16; missing 48 | match. jq set differences are empty both ways for the 16 present names and for the 48 non-present names (= 8+1+39). |
| `mori-shokunin/LOG.md` lines 1354-1355 (section "Round 19 (mori19attempt2)", starts line 1299) | "Waves64+70=134 ... Wave1 retains16 reports, 8 observed provider failures, 1 cancellation and39 unreported unknown causes" | 16 / 48 | match |
| `/home/vgpnk/Projects/shokunin/MANIFEST.json` `rounds[]` row, lane mori, round 19, closed 2026-10-21T10:15:02Z (row lines 10116-10174; notes line 10171) | "W1 64 returned IDs,16 reports,8 known provider failures,1 cancellation,39 unknown no-report causes" | 16 / 48 | match |
| `mori-shokunin/SCORECARD.md` round-19 section (lines 1153-1231) | no wave-1 settlement count recorded (C1/C2 receipts only) | not applicable | no conflict; no count to compare |
| fleet `LOG.md`, fleet `SCORECARD.md`, mori `SCORECARD.md` (grep for W1 count phrasings) | no hits for this wave | not applicable | no count recorded |
| `mori-shokunin/MANIFEST.json` | file does not exist (stat ENOENT) | not applicable | not a source for this lane |

Non-present classes recorded in `wave1-settlement.json` (set-equal to the live missing list):
- `known_provider_failed` (8): DraftCorrections, DraftCapabilities, Content28, Content34, FindHomeResiduals, Content32, ConnectPrivacy, Content06
- `known_cancelled` (1): Content14
- `no_report_terminal_cause_unestablished` (39): ConnectObserve, ConnectOracle, Content01, Content02, Content04, Content05, Content07, Content08, Content09, Content10, Content11, Content12, Content13, Content15, Content16, Content17, Content18, Content20, Content21, Content22, Content23, Content26, Content29, Content30, Content31, Content33, Content35, Content36, GateCoverage, GateDigests, GatePrivacy, HarnessC1, HarnessC2, MetaErrors, MetaInput, MetaTopology, QuoteS057, RegressionHarness, SrcGitRevision

The settlement's own limit text: "Missing final bodies are not successful reviews and are not inferred permanent provider deaths." This check assigns no causes. `missing` is not a death, failure, or kill claim.

## Observations
1. Attempts ledger does not reconcile. `wave1-attempts.json` (schema `mori-r19-attempts-v1`) has one entry: attempt 1, state `started`, 64 started_ids, payload 118,996 B, payload_sha256 `884b848c...2263`. It has no attempt-2 entry and no terminal state for attempt 1. The fleet closure note (MANIFEST line 10171) records attempt 1 as `lane-dead-no-report` (04:40:20) and attempt 2 as launched at 04:51:00. [observed; not reconciled]
2. Registry parity holds. On-disk `build/swarm-registry.json` (64 members, all `kind: spawn`) and the registry snapshot in `wave1-record.json` stdout both match the taskCall names and roles exactly.
3. RegressionHarness is the only executor report missing. Its worktrees `.ufo/worktrees/round-19/RegressionHarness{Actual,Sparse}` have no `.ufo/waves/round-19/build/` and no report-named `.md`. The Actual copy holds only `contract.md` and `frozen/` under `.ufo/waves/round-19/`. The Sparse copy holds `tools/mori-round19-regressions.py` (45,969 B, mtime 05:45), a non-report artifact that is not counted.
4. Look-alike counts excluded. Fleet MANIFEST `rounds[]` W1 notes for other lanes: mado r19 "W1 86 members, 25 named missing reports after zai 429"; kaidoku r21 "W1 64seats26reports38reportless" (same seat count, different lane, not this wave); mori r18 "W1 68 seats with 15 provider-capacity deaths". Exactly one `rounds[]` row exists for mori round 19.
5. Recursive worktree hazard. Under `.ufo/worktrees/round-19/RegressionHarnessActual/.ufo/worktrees/round-19/` there is a self-similar nested chain of `ContentGate/.ufo/worktrees/round-19/` copies. A recursive `ls -laR` of `RegressionHarnessActual/.ufo` ran past the 300 s background budget; I cancelled it (bg_356). That listing showed file names and sizes under `RegressionHarnessActual/.ufo/interactive-sessions/`; I did not open any transcript. Any recursive scan of `.ufo/worktrees` must bound its depth.
6. Search limits. A whole-tree `_glob` for the 48 names timed out after 5 s, so it is not evidence of absence. Absence claims cover only the lane-root path, the fleet-root path, and worktree `build/*.md` and `.ufo/waves/round-19/build/*.md` paths. [INFERENCE] the 48 reports do not exist elsewhere in either tree.

## Evidence files (seat drafts only)
- `.ufo/waves/round-20/build/GtMoriR19W1/members.tsv`: 64 rows of name, agent, strict path, strict-match count, loose-match count, loose path, final-line flag.
- `.ufo/waves/round-20/build/GtMoriR19W1/lane-status.txt`: stat result per member at the lane root (16 `regular file`, 48 ABSENT).
- `.ufo/waves/round-20/build/GtMoriR19W1/fleet-status.txt`: stat result per member at the fleet root (64 ABSENT).

## Commands (summary)
- Extraction: `/usr/bin/jq -r '.taskCall.tasks[] | ... split("\n") ... select(test("^Report: write your scoped findings to (\\S+)$")) ... capture ...' wave1-run.json > members.tsv`
- Presence: per row, `stat -c '%F|%s|%n' -- "$ROOT/$p"`; on failure, `ABSENT`. Run once with `ROOT` = lane root and once with `ROOT` = fleet root.
- Reconciliation: `/usr/bin/jq -Rs --slurpfile s wave1-settlement.json '...'` computing set differences between the live lists and `reports_present` and the three non-present lists. All differences are empty.
