HOLDS

Round-19 wave 1 (`mori-r19-attempt2-build`, `.ufo/waves/round-19/wave1-run.json`), member level. The scanner's `missing` list equals the GT table's non-present names, and its present list equals the GT's present names. Set differences are empty in both directions. Counts agree: 16 present, 48 missing, 0 empty, 0 stub, 0 misrooted, 0 unsafe, 0 unparsed; state `partial`.

Scope: C2 member-level only. Leaf seat: no subagents, no tool installs, no lane production writes, no git or jj. Scratch: `.ufo/waves/round-20/falsify/LiveMoriR19W1/`.

## 1. Scan runs
- `python3 tools/mori-wave-settlement.py scan --lane-root /home/vgpnk/Projects/shokunin/mori-shokunin --fleet-root /home/vgpnk/Projects/shokunin` exited 1 in all three runs (08:01:09, 08:04:15, 08:07:21 local). Exit 1 is by design for partial waves.
- Wave-1 entry, canonical JSON sha256 prefix `2682b12df994b331` (4,847 B), identical in all three runs.
- Tool at verdict: sha256 `e5c06dad076b8e5a...`, mtime 08:04:26 local. It was edited mid-wave (see R3).

## 2. Sets (sorted, `LC_ALL=C`, `comm`)
- tool missing (48) = GT missing (48):
  ConnectObserve ConnectOracle ConnectPrivacy Content01 Content02 Content04 Content05 Content06 Content07 Content08 Content09 Content10 Content11 Content12 Content13 Content14 Content15 Content16 Content17 Content18 Content20 Content21 Content22 Content23 Content26 Content28 Content29 Content30 Content31 Content32 Content33 Content34 Content35 Content36 DraftCapabilities DraftCorrections FindHomeResiduals GateCoverage GateDigests GatePrivacy HarnessC1 HarnessC2 MetaErrors MetaInput MetaTopology QuoteS057 RegressionHarness SrcGitRevision
- tool present (16) = GT present (16):
  Content03 Content19 Content24 Content25 Content27 ContentGate CriticProvenance CriticScope CriticTrends DraftLesson FindSW1Content FreezeMetadata QuoteS055 QuoteS059 QuoteS063 SrcHashlibReject
- `comm -23` and `comm -13` on missing: both empty. On present: both empty. Symmetric difference over all 64 names: empty. Per-name status mismatches: none.
- GT source: `GtMoriR19W1.md` lines 31-94, 64 rows, no duplicate names, status values {present, missing}. I extracted these rows myself with `/usr/bin/jq -R` capture.

## 3. Member-level checks independent of scanner and GT
- Trailers (own Python extraction, both `split("\n")` and `splitlines()` variants): 64 tasks. Each has exactly one trailer-form line, and it is the final line. No CR, VT, FF, FS, GS, RS, NEL, LS or PS characters. 64 distinct paths, all `.ufo/waves/round-19/build/<Name>.md`. No task body names another round-19 build path. Ten bodies contain "Report" outside the trailer, matching GT.
- lstat per trailer path (no following): lane root 16 regular non-empty and 48 ABSENT; fleet root 64 ABSENT.
- The 9 round-19 lane roots from MANIFEST rows (8 siblings plus this lane): 48 paths x 9 roots = 432 stat probes, no listing. 0 hits.
- Payload: `wave1-taskcall.json` (118,996 B, sha256 `884b848c...2263`) matches `wave1-attempts.json` `payload_sha256`. Its tasks are JSON-equal to `wave1-run.json` `taskCall.tasks`. `registry.members`, `build/swarm-registry.json` and `wave1-spec.json` items each carry the same 64 names.
- Recorded closure `wave1-settlement.json` (06:05:29 local, before the frozen C2 contract at 07:23:02): `reports_present` (16) equals tool present. `known_provider_failed` 8, `known_cancelled` 1 and `no_report_terminal_cause_unestablished` 39 together equal tool missing (48, disjoint, no duplicates). MANIFEST round-19 closure row: "W1 64 returned IDs,16 reports,8 known provider failures,1 cancellation,39 unknown no-report causes". Agrees.
- Timing: `wave1-run.json` mtime 08:05:28Z. The 16 present reports run from 08:19:14Z to 08:26:14Z, all later. MANIFEST's attempt-2 launch time (04:51:00, no zone) is not reconciled with these mtimes. It does not change the member result.
- Content, shape plus: no byte-identical pairs in `round-19/build`. Grep for provider-error or STATUS text in the 16 found none; the two hits were a hex digest containing "429" and a prose "Status:" line. Five JSON reports carry `reviewer: MoriR19Recovery.<Name>` matching their member. Markdown headings match member topics (e.g. QuoteS059 is a git-log quote). Six reports lack a final newline; their tails are complete, with no truncation sign.
- Cross-wave: no wave-1 report path is a trailer path of any other discovered dispatch wave (11 comparisons).
- Name collisions: basename prefix search under `.ufo/waves` for the 48 names gives one hit, `.ufo/waves/round-13/build/RegressionHarness.md` (16,710 B, 2026-10-20T04:25Z). Different path, correctly not counted. Round-19 subtree token search: `falsify/SourceS057.md` and `falsify/CriticCoverage.md` are wave-2 trailers (`wave2-run.json`), not wave-1 members.

## 4. Residual risks and verification gaps
- R1 Worktrees not inspected. Bounds forbid listing or reading `.ufo/worktrees/**` and `.ufo/interactive-sessions/**`. A missing report could exist inside a seat's worktree. The tool never looks there by design. GT's worktree-absence claim is unverified by me.
- R2 GT provenance: `GtMoriR19W1.md` Observation 5 discloses that its seat ran a recursive `ls -laR` under `RegressionHarnessActual/.ufo`, which listed names and sizes under `.ufo/interactive-sessions/` (bounds class). I did not repeat it. The table still matches my independent lstat. Flag for main agent.
- R3 Tool edited mid-wave: `tools/mori-wave-settlement.py` grew 682 to 689 lines, last write 08:04:26 local. The header gains an `r7` refinement case. I did not locate every changed line. I re-read the scan path (`_dispatch_files`, `_inspect_report_path`, `_member_status`, `_summarize_wave`, `scan_lane`): line spans are unchanged, shifted +3. Wave-1 output is unchanged across the edit.
- R4 Lane-wide totals move during the session (waves 12 to 14; ignored 507 to 621). Falsify probes under `.ufo/waves/round-20/falsify/SentinelTool/` write dispatch-schema fixtures that the tool counts as live waves. Wave 1 is unaffected.
- R5 GT's "do not exist elsewhere" statement is an [INFERENCE]. The round-13 `RegressionHarness.md` above contradicts it for one name.

## 5. Latent under-count defects (probe in /tmp, removed; not triggered by wave 1)
- L1 `tools/mori-wave-settlement.py:194-195` returns `unavailable` on a non-ENOENT lstat error. `_member_status` then returns `missing` (line 237). Probe: report inside a mode-000 directory gave member `missing` although the file exists.
- L2 `tools/mori-wave-settlement.py:111-114` silently skips any `*.json` whose lstat fails: no entry in `waves`, no `unreadable_json`, no `ignored_json`. Probe: dispatch file inside a mode-0444 directory was absent, with counts 0/0.
- Wave 1 is unaffected: every lstat on its 64 trailer paths and on the `.ufo/waves/round-19` chain succeeded.

## 6. Process notes
- Probe fixtures for L1/L2 ran as uid 1000 under `/tmp/c2probe-*`. Permissions were restored and the tree removed.
- A stray no-op `awk ... /dev/null` and shell `grep` were used on my own scratch lists, not on lane trees. No effect on results.
- No installs, no subagents, no writes outside this report and the scratch dir.

Checks for main agent: none required for this item. If the tool changes again, re-run `scan` and confirm the wave-1 entry hash `2682b12df994b331`.
