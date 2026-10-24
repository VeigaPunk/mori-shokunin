# Round-17 privacy re-sweep at e2bfbd6

## Scope and method

Axes: **privacy recall**, **classification accuracy**, **report minimization**. Read-only sweep of tracked text blobs at `e2bfbd6f8dccc51fc06455efc41f720301112dd4`, restricted to `.ufo/waves/round-17/`. The two `git grep` queries used `-n -I -E`; exit status was `0` for each:

- `git -C /home/vgpnk/Projects/shokunin/mori-shokunin grep -n -I -E -i -e '(/home/vgpnk/|\.config/|sessions?|[0-9]+T[0-9]+|Z_[0-9A-Fa-f]{8}|Documents|history|sudo|\buid\b|provider|model|fallback)' e2bfbd6f8dccc51fc06455efc41f720301112dd4 -- .ufo/waves/round-17/`
- `git -C /home/vgpnk/Projects/shokunin/mori-shokunin grep -n -I -E -e '([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}|\b[A-Z][a-z]{2,}\s+[A-Z][a-z]{2,})' e2bfbd6f8dccc51fc06455efc41f720301112dd4 -- .ufo/waves/round-17/`

Counts below are distinct matching **path:line** records per family, not token occurrences; a line may count in multiple families. `-I` excludes binary blobs. Broad tokens such as `sessions`, `history`, `provider`, `model`, and `fallback` include benign prose/code. Category assignment uses the matched format and source path without reproducing matched text; it is a privacy-conservative classifier, not semantic proof. The proper-name regex is heuristic; exact-email counts are stronger evidence than name-shaped counts.

## Family counts and classification

Columns are: synthetic fixture / lane-fleet path / public doc / private-context candidate.

| ID | Family | Total lines | Synthetic | Lane/fleet | Public | Private candidate |
|---|---|---:|---:|---:|---:|---:|
| X1 | `/home/vgpnk/` path | 14,133 | 1,522 | 12,534 | 2 | 75 |
| X2 | `.config/` path | 59 | 12 | 27 | 0 | 20 |
| X3 | `sessions` | 3,557 | 708 | 2,823 | 2 | 24 |
| X4 | timestamp/session-like (`digitsTdigits`, `Z_…`) | 7,442 | 1,211 | 6,206 | 0 | 25 |
| X5 | personal name/email | 313 | 34 | 72 | 18 | 189 |
| X6 | `uid` | 21 | 0 | 10 | 2 | 9 |
| X7 | `Documents` | 29 | 5 | 22 | 2 | 0 |
| X8 | `history` | 92 | 5 | 85 | 1 | 1 |
| X9 | `sudo` | 7 | 0 | 6 | 0 | 1 |
| X10 | `provider`/`model` | 822 | 321 | 501 | 0 | 0 |
| X11 | `fallback` | 359 | 89 | 269 | 1 | 0 |

X5 includes 211 email-shaped lines and 102 capitalized two-word lines. Of the 189 conservative private candidates, 187 are exact non-placeholder email-shaped hits and 2 are name-shaped/contextual hits. These counts are candidate line counts, not a claim that each unique value is a different person. X1/X2, X3/X4, and X5/X6 may overlap at the same line.

## Private-context candidate index (no values reproduced)

Each identifier below is a sweep class. The SHA-256 is a digest of the sorted canonical set `path:line:SHA256(UTF-8-decoded matched line)\n`; it commits to the indexed lines without quoting them. Line numbers refer to the scanned revision. A candidate listing is not a ruling that every match is genuinely private; synthetic/policy contexts are not classified as private.

### X1 — `/home/vgpnk/` paths outside lane/fleet (75 lines)
Set SHA-256: `dfe7caa0b3c8625a5813b4ef1de739b417e4e19ad007886605b23f40a40c5d1c`

- `.ufo/waves/round-17/build/ContextCheck17.md:46,116,141`
- `.ufo/waves/round-17/build/CriticFrontier.md:161`
- `.ufo/waves/round-17/build/FleetRootUntracked.md:3,11`
- `.ufo/waves/round-17/build/JjEnvFacts.md:16,20,26,27,48,49,162,178`
- `.ufo/waves/round-17/build/MisrootR16Facts.md:13,57`
- `.ufo/waves/round-17/build/MisrootSweep.md:165-167`
- `.ufo/waves/round-17/build/OmpRetryDocs.md:11,16,330,332`
- `.ufo/waves/round-17/build/OverlapTsukuroi.md:34`
- `.ufo/waves/round-17/build/PacmanTxnToday.md:120,141`
- `.ufo/waves/round-17/build/QualityCriteriaDraft.md:18`
- `.ufo/waves/round-17/build/RevengerOmpTerminal.md:11,33-38`
- `.ufo/waves/round-17/build/ReviewC1Metric.md:43`
- `.ufo/waves/round-17/build/SentinelTranscripts.md:5`
- `.ufo/waves/round-17/build/SkillRegistry.md:115,120,369`
- `.ufo/waves/round-17/evidence/final/fleet-misroot-final.json:9,23`
- `.ufo/waves/round-17/evidence/final/fleet-status-full.json:11`
- `.ufo/waves/round-17/evidence/final/jj-after/run-manifest.json:19,25`
- `.ufo/waves/round-17/evidence/final/jj-before/run-manifest.json:19,25`
- `.ufo/waves/round-17/evidence/final/sources-census-final.json:9`
- `.ufo/waves/round-17/evidence/jj-after/run-manifest.json:19,25`
- `.ufo/waves/round-17/evidence/jj-before/run-manifest.json:19,25`
- `.ufo/waves/round-17/evidence/jj-snapshot-audit.json:6`
- `.ufo/waves/round-17/evidence/sources-census-end.json:9`
- `.ufo/waves/round-17/falsify/CensusNewBranches.md:120`
- `.ufo/waves/round-17/falsify/MutBranch.md:48,55,181`
- `.ufo/waves/round-17/falsify/ReceiptC3.md:50`
- `.ufo/waves/round-17/falsify/ReportTrace.md:75`
- `.ufo/waves/round-17/falsify/SourceCensus.md:20,22`
- `.ufo/waves/round-17/frozen/mori-round17-context-initial.py:39,110,504,531`
- `.ufo/waves/round-17/frozen/wave2-no-background.json:5`
- `.ufo/waves/round-17/frozen/wave2-no-live-journal.json:5`
- `.ufo/waves/round-17/wave1-context.txt:3,7`
- `.ufo/waves/round-17/wave1-dispatch.json:457,577`
- `.ufo/waves/round-17/wave1-spec.json:5,125`
- `.ufo/waves/round-17/wave2-dispatch.json:421`
- `.ufo/waves/round-17/wave2-spec.json:5`

### X2 — host `.config/` paths (20 lines)
Set SHA-256: `a59fdc513db1609bd4a281129410d7be3d7b543b2ce79c9b4d6172e0cdba1b39`

- `.ufo/waves/round-17/build/JjEnvFacts.md:26,49,162`
- `.ufo/waves/round-17/build/ReviewJjAuditRouting.md:67`
- `.ufo/waves/round-17/build/SentinelJjSandbox.md:7,26,27,32,90,94,101,193,200,203`
- `.ufo/waves/round-17/build/SkillRegistry.md:188`
- `.ufo/waves/round-17/falsify/LessonAudit.md:73`
- `.ufo/waves/round-17/wave1-dispatch.json:482,792`
- `.ufo/waves/round-17/wave1-spec.json:30,340`

### X3 — concrete session path/identity context (24 lines)
Set SHA-256: `bbf9b5eb757610fbba40b6ad01267114b0d341dd42178f5fa9b0a40c5c892a7a`

- `.ufo/waves/round-17/build/SentinelTranscripts.md:31,196`
- `.ufo/waves/round-17/build/SiblingSeatDeathTools.md:10`
- `.ufo/waves/round-17/build/TranscriptTailBounds.md:84`
- `.ufo/waves/round-17/evidence/final/seat-after-fixed/run-manifest.json:1`
- `.ufo/waves/round-17/evidence/final/seat-after/run-manifest.json:1`
- `.ufo/waves/round-17/evidence/final/seat-before/run-manifest.json:1`
- `.ufo/waves/round-17/evidence/final/seat-initial-red/run-manifest.json:1`
- `.ufo/waves/round-17/evidence/r13-preserved/evidence.json:81,542,1697,2958`
- `.ufo/waves/round-17/evidence/r14-preserved/evidence.json:159,2495`
- `.ufo/waves/round-17/evidence/r15-preserved/run-manifest.json:7445,8211,8740,9254`
- `.ufo/waves/round-17/evidence/seat-after/run-manifest.json:1`
- `.ufo/waves/round-17/evidence/seat-before/run-manifest.json:1`
- `.ufo/waves/round-17/falsify/CaseReview25.md:14`
- `.ufo/waves/round-17/falsify/ConformanceAudit.md:38`
- `.ufo/waves/round-17/wave1-dispatch.json:557`
- `.ufo/waves/round-17/wave1-spec.json:105`

### X4 — timestamp/session-like identifier context (25 lines)
Set SHA-256: `50344fc7e838a452403c3b3a74d40db01bbc6b6be62929a44e34e8f29a067f65`

- `.ufo/waves/round-17/build/SeatFixtures.md:338`
- `.ufo/waves/round-17/build/TranscriptTailBounds.md:70,84`
- `.ufo/waves/round-17/evidence/final/seat-after-fixed/run-manifest.json:1`
- `.ufo/waves/round-17/evidence/final/seat-after-fixed/runs/main_session_excluded_from_totals.stdout:1`
- `.ufo/waves/round-17/evidence/final/seat-after/run-manifest.json:1`
- `.ufo/waves/round-17/evidence/final/seat-after/runs/main_session_excluded_from_totals.stdout:1`
- `.ufo/waves/round-17/evidence/final/seat-before/run-manifest.json:1`
- `.ufo/waves/round-17/evidence/final/seat-initial-red/run-manifest.json:1`
- `.ufo/waves/round-17/evidence/final/seat-initial-red/runs/main_session_excluded_from_totals.stdout:1`
- `.ufo/waves/round-17/evidence/r13-preserved/evidence.json:81,542,1697,2958`
- `.ufo/waves/round-17/evidence/r14-preserved/evidence.json:159,2495`
- `.ufo/waves/round-17/evidence/r15-preserved/run-manifest.json:7445,8211,8740,9254`
- `.ufo/waves/round-17/evidence/seat-after/run-manifest.json:1`
- `.ufo/waves/round-17/evidence/seat-after/runs/main_session_excluded_from_totals.stdout:1`
- `.ufo/waves/round-17/evidence/seat-before/run-manifest.json:1`
- `.ufo/waves/round-17/falsify/CaseReview25.md:14`
- `.ufo/waves/round-17/frozen/mori-seat-terminal-initial.py:1433`

### X5 — personal email/name candidates (189 lines)
Set SHA-256: `0988b73e2ebf917943354a7f1630626a46d026f87f3950ceb9e4051c9c22fff7`

- `.ufo/waves/round-17/build/CensusConsumers.md:186`
- `.ufo/waves/round-17/build/CensusGitSites.md:154`
- `.ufo/waves/round-17/build/CriticC2.md:89`
- `.ufo/waves/round-17/build/HelperFailureWindows.md:28`
- `.ufo/waves/round-17/build/LiveLaneHeadVsBranch.md:53,54`
- `.ufo/waves/round-17/build/ReviewJjAuditRouting.md:15`
- `.ufo/waves/round-17/build/SentinelJjSandbox.md:93`
- `.ufo/waves/round-17/build/SrcRfc6585.md:9`
- `.ufo/waves/round-17/evidence/final/jj-after/run-manifest.json:1090,1095,1100,1220,1225,1230`
- `.ufo/waves/round-17/evidence/final/r14-preserved/targets/frozen.mori-census.sh:1147,1154,1726,2908,2919,2931,2942,2955,2956,2966,2977,2988,3010`
- `.ufo/waves/round-17/evidence/final/r14-preserved/targets/sut.mori-census.sh:37,1694,1701,2250,2463,2541,3949,3960,3972,3983,3996,3997,4007,4018,4029,4052,4073,4094,4103,4104,4122,4146,4166,4190,4219,4220,4280`
- `.ufo/waves/round-17/evidence/final/r15-preserved/targets/frozen.mori-census.sh:1406,1413,1985,3300,3311,3323,3334,3347,3348,3358,3369,3380,3402`
- `.ufo/waves/round-17/evidence/final/r15-preserved/targets/sut.mori-census.sh:37,1694,1701,2250,2463,2541,3949,3960,3972,3983,3996,3997,4007,4018,4029,4052,4073,4094,4103,4104,4122,4146,4166,4190,4219,4220,4280`
- `.ufo/waves/round-17/evidence/jj-after/run-manifest.json:1038`
- `.ufo/waves/round-17/evidence/r14-preserved/targets/frozen.mori-census.sh:1147,1154,1726,2908,2919,2931,2942,2955,2956,2966,2977,2988,3010`
- `.ufo/waves/round-17/evidence/r14-preserved/targets/sut.mori-census.sh:38,1658,1665,2350,2359,2364,2446,3828,3839,3851,3862,3875,3876,3886,3897,3908,3931,3952,3973,3982,3983,4001,4025,4045,4069`
- `.ufo/waves/round-17/evidence/r15-preserved/targets/frozen.mori-census.sh:1406,1413,1985,3300,3311,3323,3334,3347,3348,3358,3369,3380,3402`
- `.ufo/waves/round-17/evidence/r15-preserved/targets/sut.mori-census.sh:38,1658,1665,2350,2359,2364,2446,3828,3839,3851,3862,3875,3876,3886,3897,3908,3931,3952,3973,3982,3983,4001,4025,4045,4069`
- `.ufo/waves/round-17/falsify/CensusNewBranches.md:77`
- `.ufo/waves/round-17/falsify/CriticC2Final.md:157`
- `.ufo/waves/round-17/falsify/ReceiptC2Controls.md:76`
- `.ufo/waves/round-17/falsify/ReceiptC3.md:56`
- `.ufo/waves/round-17/frozen/mori-census.sh:1652,1659,2231,3647,3658,3670,3681,3694,3695,3705,3716,3727,3749`

### X6 — concrete `uid` values (9 lines)
Set SHA-256: `942edb78fc7a6844e2b4d4948a53df87354136044af32c5c6fe181e4ddf7b284`

- `.ufo/waves/round-17/evidence/final/r14-preserved/targets/frozen.mori-census.sh:2364`
- `.ufo/waves/round-17/evidence/final/r14-preserved/targets/sut.mori-census.sh:3176`
- `.ufo/waves/round-17/evidence/final/r15-preserved/targets/frozen.mori-census.sh:2628`
- `.ufo/waves/round-17/evidence/final/r15-preserved/targets/sut.mori-census.sh:3176`
- `.ufo/waves/round-17/evidence/r14-preserved/targets/frozen.mori-census.sh:2364`
- `.ufo/waves/round-17/evidence/r14-preserved/targets/sut.mori-census.sh:3058`
- `.ufo/waves/round-17/evidence/r15-preserved/targets/frozen.mori-census.sh:2628`
- `.ufo/waves/round-17/evidence/r15-preserved/targets/sut.mori-census.sh:3058`
- `.ufo/waves/round-17/frozen/mori-census.sh:2883`

### X7 — shell-history reference (1 line)
Set SHA-256: `1450ca216fd7d609a1f32293327ebc256e19af5fe405663d82ca0f7674914179`

- `.ufo/waves/round-17/falsify/ConformanceAudit.md:46`

### X9 — privileged `sudoers` reference (1 line)
Same source line as X7, SHA-256 `1450ca216fd7d609a1f32293327ebc256e19af5fe405663d82ca0f7674914179`.

- `.ufo/waves/round-17/falsify/ConformanceAudit.md:46`

## Triage comparison and verdict

The frozen policy (`.ufo/waves/round-18/frozen/c1-policy.json:7-15,27-29`) is expressly a recall floor. It has direct classes for session IDs/store paths, Documents, shell history, sudoers, config-line references, routing keys, and selected session-record values, but no direct general class for home paths outside the fleet, `.config/` paths, personal names/emails, or numeric `uid` values. `uid` is the clearest family omitted by both the frozen C1 class list and the triage (`out-of-metric-triage.md:10-16,20-35`).

The triage does name personal identities/emails, host home-config paths, session identities, Documents, shell history, privileged config, and OMP routing values (`out-of-metric-triage.md:10-13,22-29`), but the scan still finds candidate lines outside the few locations listed in its dispositions. In particular, X5 includes many preserved r14/r15 target snapshots, and X1/X2 occur in multiple build/falsify/evidence paths. Treat these as uncovered residual candidates rather than assuming the disposition rows enumerate every occurrence. X3/X4 are partially covered by R1/R2 and the session-identity triage, but their broader shapes/locations should be checked. Documents/history/sudo are directly named by R4/R5/R6 and the triage; provider/model and fallback tokens are discussed by the triage, and no concrete operator routing assignment was classified as private by this sweep. 

**Likely triage gaps:** numeric `uid` (X6); additional personal email/name-bearing lines in archived target snapshots (X5); and broad host path/config occurrences beyond the individually cited host-env/config rows (X1/X2). The identifier patterns X3/X4 warrant confirmation as genuine session data versus synthetic fixture data. This is a falsification finding, not an admission or verdict.

**Minimal redaction:** replace host paths with `$HOME/[HOST-PATH]` (or a generic path class), `.config` details with `[HOST-CONFIG-PATH]`, session/timestamp identifiers with `[SESSION-ID]` while retaining only coarse non-session timing if needed, email/name values with `[EMAIL]`/`[PERSON]`, and numeric user IDs with `[UID]`. Keep schema/field names and aggregate counts; leave confirmed synthetic fixtures and public-source text intact after verifying their sentinel values are synthetic. No matched private values are reproduced here.

## Remaining uncertainty

The report classifies format/path candidates without exposing raw matched text. Name-shaped matches can be false positives; preserved tool/evidence snapshots may contain test fixtures as well as captured ambient metadata. A human adjudicator should confirm X1-X6 under the non-author privacy rules before treating candidate counts as confirmed leaks. No tool was installed or updated.
