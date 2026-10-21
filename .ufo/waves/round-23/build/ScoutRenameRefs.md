# ScoutRenameRefs — `raw_unallowlisted` reference census (round 23)

Seat: `MadoR22-2.ScoutRenameRefs-8` (scout, leaf member; no subagent dispatch, no delegation,
no edits outside this report). Authority: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/contract.md`
§"Routed items" 1 / §C1, frozen at lane commit `4dc80c1be48308075e83af17f15fbfe7e95e6cb8`
(contract sha256 `2bb35aefb08d3fafc467260f859453c0f096effe18b2446503f2b2ee87fe69e7`, matching
`frozen/c1-requirements.json.contract_sha256`). Snapshot: 2026-10-21; verified working tree is
tracked-clean at HEAD `4dc80c1` (`git status --porcelain` has only `??` untracked entries).

Tool installs: none. No package transaction, no service change, no execution of the tool/oracle/
cases, no live host probe, no session transcript read, no credential/auth/agent.db read.

## Method and status of the instrument

- Enumeration by **literal byte search** (`grep -rIl`, then a per-file `os.walk` census that
  records every line containing the literal and the byte occurrence count).
- The mounted toolset exposes **no `lsp` device** (`read xd://lsp` → `No such tool: xd://lsp`),
  so no language server answers these Markdown/JSON/Python files. This census is therefore a
  literal-reference enumeration, not LSP semantic proof. The producer is nevertheless read
  directly: the key is a plain dict string literal, and no name construction produces it
  (`grep -n "raw_" tools` shows no concatenation/format string for the output key).
- Scope/exclusions: `.scratch/` excluded per assignment. `.git/`, `.jj/`, `.ufo/worktrees/`
  excluded as VCS state per lane bounds. Compliance note (disclosed, not hidden): the initial
  repo-wide literal membership scan (`grep -rIl . --exclude-dir=.scratch`, and two whole-tree
  `os.walk` count passes that were backgrounded) was **not path-filtered** and therefore
  traversed `.ufo/interactive-sessions` and `.ufo/worktrees` as byte streams while testing for
  the one literal. Neither produced a match; no session transcript or worktree content was
  decoded, printed, quoted or used, and no such path appears in any match list. All per-line
  census passes after that were restricted to the matched files and `.ufo/waves/round-22` /
  `.ufo/waves/round-23`. This report file is excluded from its own census (it necessarily
  contains the literal). Binary matches are counted separately.
- Snapshot caveat: `.ufo/waves/round-23/build/` is untracked and being written by peers; its
  counts can move after this snapshot. `wave1-*.json` are untracked host-generated payloads.

## Totals

| Class | Files | Occurrences |
|---|---|---|
| Tool code (live, mutable) | 1 | 1 |
| Live documentation — reference present | 5 | 6 |
| Live documentation — named surface, no reference | 1 (`corpus/README.md`) | 0 |
| r22 frozen/historical evidence (must stay byte-unchanged) | 163 | 2616 |
| r22 generated cache (untracked binary, not evidence) | 1 | 1 |
| r23 harness / sealed pre-implementation artifacts | 6 | 24 |
| r23 wave build artifacts (untracked, moving) | 8 | 69 |
| **Text files with ≥1 occurrence** | **183** | **2716** |

Arithmetic: text files = 1 tool + 5 live-doc + 163 r22 + 6 harness + 8 build = 183;
occurrences = 1 + 6 + 2616 + 24 + 69 = 2716. Adding `corpus/README.md` (named surface,
0 occurrences) and the untracked `.pyc` (1 binary occurrence) gives 185 paths named in total.

---

## 1. Tool code — 1 file, 1 occurrence

| Path:line | Observed content | Role |
|---|---|---|
| `tools/mori-retention-reconcile.py:234` | `'scanner_total':len(scanner),'raw_unallowlisted':len(unallowed),'scanner_unallowlisted':len(unallowed),` | **Sole producer.** The result object from `check()`. |

Adjacent non-literal anchors (needed for the C1 change, not references):
`tools/mori-retention-reconcile.py:16` `SCHEMA='mori-retention-reconciliation-v1'`;
`:231` check output; `:235` `raw_not_allowlisted` (already present); `:274` selftest output;
`:287`/`:289` setup-error outputs. All outputs build from the single `SCHEMA` constant, so
removing the key at `:234` and bumping `:16` covers check, setup error and selftest. The tool
contains no other literal occurrence.

## 2. Live documentation

| Path:line | Content/status | Correction verdict |
|---|---|---|
| `SKILL.md:556` (paragraph `:556-564`, EOF) | "Field caveats (wave2 FinalR02/NoHarm): `raw_unallowlisted` and `scanner_unallowlisted` are one existing gate metric reported twice…" — true for the v1 bytes; after C1 the key is absent from every v2 output. | **Needs an append-only block after `:564`.** Do not rewrite `:556-564`. |
| `corpus/knowledge/retention-reconciliation-r22.md:27` and `:35` (paragraph `:27-36`) | `:27` "The output's `raw_unallowlisted` and `scanner_unallowlisted` intentionally name the same…"; `:35` "…the frozen field name `raw_unallowlisted` keeps its frozen alias meaning (4)…". | **Needs an append-only block after `:36`** (before blank `:37` / `## Provenance limits` `:38`). Do not rewrite `:27-36`. |
| `corpus/lessons/round-22.md:87` | "a truthful `raw_not_allowlisted` beside the frozen alias `raw_unallowlisted`" — historical r22 wave2 record, true at r22. | No edit required. The r23 lesson carries the cutover (draft already at `build/DraftLesson.md:88,95,97`). |
| `LOG.md:1527` | Live r23 round entry: "a pre-registered rename of the misleading frozen field `raw_unallowlisted` … C1 (calibration) removes the alias with a schema v2 cutover". | No correction: pre-registration language remains true after the cutover. |
| `SCORECARD.md:1422` | Live r23 C1 target row: "C1 remove misleading `raw_unallowlisted` … Targets, not results." | No correction: remains true; L1 records results at measurement. |
| `corpus/README.md` | **0 occurrences.** Coverage-map row `:420` describes `knowledge/retention-reconciliation-r22.md` without naming the key ("explicitly distinguishes policy non-author exclusions from source-file subtraction. Agreement is not clearance"). | No correction required for C1; the row stays true. |
| `README.md`, `PROVINCE.md`, `MINT.md`, `SHONEN.md`, `AGENTS.md`, `considerthese/` | **0 occurrences each.** | No correction. |

Named-surface check required by the assignment: `SKILL.md`, `corpus/knowledge/…`, and
`corpus/README.md` — the first two need the correction, the third has no reference to correct.

## 3. Harness — r23 sealed/pre-implementation artifacts (6 files, 24 occurrences)

These are frozen/sealed or host-generated and are **not** documentation to correct here.

| Path:lines | Role |
|---|---|
| `.ufo/waves/round-23/contract.md:9,30,32,39,42,49,56` | Frozen contract (7). Never edit. |
| `.ufo/waves/round-23/frozen/c1-expected-real.json:21` | `forbidden_keys: ["raw_unallowlisted"]` (1). Sealed. |
| `.ufo/waves/round-23/oracle-rename.py:5,82` | Oracle docstring and `misleading_alias_runs` counter (2). Sealed; must keep reading the removed key to measure absence. |
| `.ufo/waves/round-23/wave1-spec.json:5,185,205,285` | Host-generated wave payloads embedding task text (4). Untracked harness input. |
| `.ufo/waves/round-23/wave1-run.json:421,601,621,701` | Host-generated run payloads (4). Untracked harness transcript. |
| `.ufo/waves/round-23/wave1-response8.json:2` | One physical line, 6 occurrences (embedded spawn prompts). Untracked harness transcript. |

`.ufo/waves/round-23/frozen/c1-requirements.json` has **0 literal occurrences**; requirement
R25's absence assertion lives in `oracle-rename.py:82` and `frozen/c1-expected-real.json:21`,
so no requirement-file edit is implied.

### r23 wave build artifacts — untracked, moving (8 files, 69 occurrences)

| Path:lines | Occurrences |
|---|---|
| `.ufo/waves/round-23/build/CriticRenameHarm.md:1,18,60,108,110,115,119,128,159,169,172` | 11 |
| `.ufo/waves/round-23/build/DraftRenameDocs.md:22,39,80,100,102,108` | 6 |
| `.ufo/waves/round-23/build/DraftRenameDocs/corrections.md:28,29,40,45,62,68,77,81,104,108,110,144` | 13 |
| `.ufo/waves/round-23/build/DraftLesson.md:88,95,97` | 3 |
| `.ufo/waves/round-23/build/DraftLesson/mistakes.md:31,32,35,36,37` | 17 (some lines repeat the literal) |
| `.ufo/waves/round-23/build/MeasureDriver.md:31,99,106` | 3 |
| `.ufo/waves/round-23/build/MeasureDriver/measure-round23.py:56` | 1 |
| `.ufo/waves/round-23/build/ReviewOracleRename.md:59,60,61,82,85,159,178,183,195,220,223,224,279,282` | 15 |

These are seat outputs/proposals, not production docs; L1 owns sealing/rejection. They were
read only to avoid conflicting recommendations, not edited.

## 4. r22 frozen/historical evidence — must stay byte-unchanged (163 files, 2616 occurrences)

Everything below is under `.ufo/waves/round-22/`. All 163 files are tracked r22 records; the
contract's declared consequence applies: r22's `oracle-reconcile-v2.py` R02/R11/R12 (`:48,52,53`)
and `measure-round22.py`'s output whitelist (`:20`, comment `:149`) read the old key and no
longer pass against post-C1 tool revisions; the r22 claim stays reproducible at its bound
revision `da40bb20f81da125d798f73cd1653655be1255ca`.

### 4.1 Contract and frozen builders/oracles — 8 files, 17 occurrences

| Path:lines | Occ |
|---|---|
| `.ufo/waves/round-22/contract.md:13` | 1 |
| `.ufo/waves/round-22/frozen/expected-real.json:21` | 1 |
| `.ufo/waves/round-22/frozen/fixture-builder.py:103` | 1 |
| `.ufo/waves/round-22/frozen/fixture-builder-v2.py:104` | 1 |
| `.ufo/waves/round-22/measure-round22.py:20,149` | 2 |
| `.ufo/waves/round-22/oracle-reconcile.py:48,52,53` | 3 |
| `.ufo/waves/round-22/oracle-reconcile-v2.py:48,52,53` | 3 |
| `.ufo/waves/round-22/refinement-reconcile.py:186,187,188,191,192` | 5 |

### 4.2 r22 build reports — 30 files, 81 occurrences

| Path:lines | Occ |
|---|---|
| `.ufo/waves/round-22/build/AttackR01.md:198` | 1 |
| `.ufo/waves/round-22/build/AttackR02.md:16,40,53,69,89,110,117,122,124,160,167,168,205` | 14 |
| `.ufo/waves/round-22/build/AttackR03.md:23,93,103,108` | 4 |
| `.ufo/waves/round-22/build/AttackR04.md:55,100,124` | 3 |
| `.ufo/waves/round-22/build/AttackR05.md:63,91` | 2 |
| `.ufo/waves/round-22/build/AttackR06.md:34,49,66` | 3 |
| `.ufo/waves/round-22/build/AttackR07.md:28,78` | 2 |
| `.ufo/waves/round-22/build/AttackR08.md:23,27,45` | 3 |
| `.ufo/waves/round-22/build/AttackR09.md:65` | 1 |
| `.ufo/waves/round-22/build/AttackR10.md:36,102,114` | 3 |
| `.ufo/waves/round-22/build/AttackR11.md:28,42,62,73,78` | 5 |
| `.ufo/waves/round-22/build/AttackR12.md:47,60,94,118,139` | 5 |
| `.ufo/waves/round-22/build/AttackR18.md:30,53` | 2 |
| `.ufo/waves/round-22/build/AttackR19.md:60,84` | 2 |
| `.ufo/waves/round-22/build/AttackR23.md:19` | 1 |
| `.ufo/waves/round-22/build/AttackR24.md:46` | 1 |
| `.ufo/waves/round-22/build/ConnectKagi.md:50,68` | 2 |
| `.ufo/waves/round-22/build/ConnectSouji.md:68,95` | 2 |
| `.ufo/waves/round-22/build/CriticAdmission.md:47,72,77,133` | 4 |
| `.ufo/waves/round-22/build/CriticNoHarm.md:34,68` | 2 |
| `.ufo/waves/round-22/build/CriticPopulation.md:54,121` | 2 |
| `.ufo/waves/round-22/build/CriticTrust.md:44` | 1 |
| `.ufo/waves/round-22/build/EnteringPartition.md:67` | 1 |
| `.ufo/waves/round-22/build/GateRegistry.md:67` | 1 |
| `.ufo/waves/round-22/build/MutantPlan.md:45` | 1 |
| `.ufo/waves/round-22/build/PriorMistake.md:49,60` | 2 |
| `.ufo/waves/round-22/build/QualityDenom.md:29,67` | 2 |
| `.ufo/waves/round-22/build/RawPartition.md:63,109` | 2 |
| `.ufo/waves/round-22/build/ReportContract.md:50` | 1 |
| `.ufo/waves/round-22/build/RequirementTrace.md:23,53,62,63,93,109` | 6 |

### 4.3 r22 falsification reports — 21 files, 63 occurrences

| Path:lines | Occ |
|---|---|
| `.ufo/waves/round-22/falsify/CodeAuxiliary.md:27,29,33,44,49,108` | 6 |
| `.ufo/waves/round-22/falsify/CodeCheck.md:13,15,17,18,77` | 5 |
| `.ufo/waves/round-22/falsify/CodeCommitted.md:18,20,22,23,26,27,30` | 7 |
| `.ufo/waves/round-22/falsify/CodeMain.md:37,43` | 2 |
| `.ufo/waves/round-22/falsify/CodeNoDuplicates.md:14,71` | 4 |
| `.ufo/waves/round-22/falsify/CodeSafePath.md:120` | 1 |
| `.ufo/waves/round-22/falsify/FinalR02.md:47,78,80,82,83,87` | 6 |
| `.ufo/waves/round-22/falsify/FinalR04.md:118` | 1 |
| `.ufo/waves/round-22/falsify/FinalR10.md:28` | 1 |
| `.ufo/waves/round-22/falsify/FinalR11.md:10,12` | 2 |
| `.ufo/waves/round-22/falsify/FinalR12.md:42,47` | 2 |
| `.ufo/waves/round-22/falsify/FinalR22.md:29,70,74` | 3 |
| `.ufo/waves/round-22/falsify/FinalR23.md:17` | 1 |
| `.ufo/waves/round-22/falsify/FixtureForbidden.md:28,38,74,82,84` | 5 |
| `.ufo/waves/round-22/falsify/FixtureInject.md:132,136` | 2 |
| `.ufo/waves/round-22/falsify/FixtureInvalidRevision.md:23` | 1 |
| `.ufo/waves/round-22/falsify/FixtureLine.md:93` | 1 |
| `.ufo/waves/round-22/falsify/FixtureMetric.md:27,70,98` | 3 |
| `.ufo/waves/round-22/falsify/MutationScope.md:100` | 1 |
| `.ufo/waves/round-22/falsify/NoHarm.md:31,35,37,39,41,44` | 6 |
| `.ufo/waves/round-22/falsify/RequirementsFreeze.md:111,112,114` | 3 |

### 4.4 r22 evidence JSON — 104 files, 2455 occurrences

All are tracked. Each result object serializes the reconciler output on its own physical line,
so occurrences equal line hits. Grouped by identical line set (every file named):

**Group E1 — lines `955,991,1025,1061,1095,1137,1171,1207,1241,1277,1311,1347,1381,1417,1451,1487,1521,1591,1661,1731,1801,1871,1941,2017,2087,2157` (26 each; 49 files, 1274 occ):**
`measure1/after-observed.json`, `measure1/mutant-count-only-observed.json`,
`measure1/mutant-false-clearance-observed.json`, `measure1/mutant-setup-leak-observed.json`,
`measure1/mutant-wrong-population-observed.json`, `measure1/restored-observed.json`,
`measure2/after-observed.json`, `measure2/mutant-argv-empty-observed.json`,
`measure2/mutant-aux-unchecked-observed.json`, `measure2/mutant-count-only-observed.json`,
`measure2/mutant-exit-unchecked-observed.json`, `measure2/mutant-false-clearance-observed.json`,
`measure2/mutant-finding-unchecked-observed.json`, `measure2/mutant-forbidden-not-red-observed.json`,
`measure2/mutant-line-blind-raw-observed.json`, `measure2/mutant-metric-ignored-observed.json`,
`measure2/mutant-no-ancestor-observed.json`, `measure2/mutant-no-dotdot-observed.json`,
`measure2/mutant-non-author-unchecked-observed.json`, `measure2/mutant-one-sided-hits-observed.json`,
`measure2/mutant-output-sets-observed.json`, `measure2/mutant-policy-copy-excluded-observed.json`,
`measure2/mutant-routed-unchecked-observed.json`, `measure2/mutant-setup-leak-observed.json`,
`measure2/mutant-symlink-accepted-observed.json`, `measure2/mutant-wrong-population-observed.json`,
`measure2/restored-observed.json`, `measure3/after-observed.json`,
`measure3/mutant-argv-empty-observed.json`, `measure3/mutant-aux-unchecked-observed.json`,
`measure3/mutant-count-only-observed.json`, `measure3/mutant-exit-unchecked-observed.json`,
`measure3/mutant-false-clearance-observed.json`, `measure3/mutant-finding-unchecked-observed.json`,
`measure3/mutant-forbidden-not-red-observed.json`, `measure3/mutant-line-blind-raw-observed.json`,
`measure3/mutant-metric-ignored-observed.json`, `measure3/mutant-no-ancestor-observed.json`,
`measure3/mutant-no-dotdot-observed.json`, `measure3/mutant-non-author-unchecked-observed.json`,
`measure3/mutant-one-sided-hits-observed.json`, `measure3/mutant-output-sets-observed.json`,
`measure3/mutant-policy-copy-excluded-observed.json`, `measure3/mutant-repo-unbound-observed.json`,
`measure3/mutant-routed-unchecked-observed.json`, `measure3/mutant-setup-leak-observed.json`,
`measure3/mutant-symlink-accepted-observed.json`, `measure3/mutant-wrong-population-observed.json`,
`measure3/restored-observed.json` (all under `.ufo/waves/round-22/evidence/`).

**Group E2 — lines `26,51,76,101,301,326,376,551,576,701,726,826,851,876,976,1001,1026,1051,1076,1101,1126,1202` (22 each; 38 files, 836 occ):**
`measure2/mutant-argv-empty-refine-observed.json`,
`measure2/mutant-aux-unchecked-refine-observed.json`,
`measure2/mutant-count-only-refine-observed.json`,
`measure2/mutant-exit-unchecked-refine-observed.json`,
`measure2/mutant-false-clearance-refine-observed.json`,
`measure2/mutant-finding-unchecked-refine-observed.json`,
`measure2/mutant-forbidden-not-red-refine-observed.json`,
`measure2/mutant-line-blind-raw-refine-observed.json`,
`measure2/mutant-metric-ignored-refine-observed.json`,
`measure2/mutant-no-dotdot-refine-observed.json`,
`measure2/mutant-non-author-unchecked-refine-observed.json`,
`measure2/mutant-one-sided-hits-refine-observed.json`,
`measure2/mutant-output-sets-refine-observed.json`,
`measure2/mutant-policy-copy-excluded-refine-observed.json`,
`measure2/mutant-routed-unchecked-refine-observed.json`,
`measure2/mutant-setup-leak-refine-observed.json`,
`measure2/mutant-wrong-population-refine-observed.json`,
`measure2/refinement-observed.json`, `measure2/restored-refine-observed.json`,
`measure3/mutant-argv-empty-refine-observed.json`,
`measure3/mutant-aux-unchecked-refine-observed.json`,
`measure3/mutant-count-only-refine-observed.json`,
`measure3/mutant-exit-unchecked-refine-observed.json`,
`measure3/mutant-false-clearance-refine-observed.json`,
`measure3/mutant-finding-unchecked-refine-observed.json`,
`measure3/mutant-forbidden-not-red-refine-observed.json`,
`measure3/mutant-line-blind-raw-refine-observed.json`,
`measure3/mutant-metric-ignored-refine-observed.json`,
`measure3/mutant-no-dotdot-refine-observed.json`,
`measure3/mutant-non-author-unchecked-refine-observed.json`,
`measure3/mutant-one-sided-hits-refine-observed.json`,
`measure3/mutant-output-sets-refine-observed.json`,
`measure3/mutant-policy-copy-excluded-refine-observed.json`,
`measure3/mutant-routed-unchecked-refine-observed.json`,
`measure3/mutant-setup-leak-refine-observed.json`,
`measure3/mutant-wrong-population-refine-observed.json`,
`measure3/refinement-observed.json`, `measure3/restored-refine-observed.json`.

**Group E3 — line `24` (1 each; 3 files, 3 occ):**
`measure1/real-reconciliation.json`, `measure2/real-reconciliation.json`,
`measure3/real-reconciliation.json`.

**Group E4 — lines `26,51,76,101,151,301,326,376,551,576,701,726,826,851,876,976,1001,1026,1051,1076,1101,1126,1202` (23 each; 2 files, 46 occ):**
`measure2/mutant-symlink-accepted-refine-observed.json`,
`measure3/mutant-symlink-accepted-refine-observed.json`.

**Group E5 — lines `26,51,76,101,201,301,326,376,551,576,701,726,751,776,826,851,876,976,1001,1026,1051,1076,1101,1126,1202` (25 each; 2 files, 50 occ):**
`measure2/mutant-no-byte-compare-refine-observed.json`,
`measure3/mutant-no-byte-compare-refine-observed.json`.

**Group E6 — lines `26,51,76,101,226,251,301,326,376,551,576,701,726,826,851,876,901,926,951,976,1001,1026,1051,1076,1101,1126,1202` (27 each; 2 files, 54 occ):**
`measure2/mutant-bool-lax-refine-observed.json`, `measure3/mutant-bool-lax-refine-observed.json`.

**Group E7 — lines `26,51,76,101,301,326,376,476,501,526,551,576,701,726,826,851,876,976,1001,1026,1051,1076,1101,1126,1202` (25 each; 2 files, 50 occ):**
`measure2/mutant-no-ancestor-refine-observed.json`,
`measure3/mutant-no-ancestor-refine-observed.json`.

**Group E8 — lines `955,991,1025,1061,1095,1137,1171,1207,1241,1277,1311,1347,1381,1417,1451,1487,1521,1591,1661,1731,1767,1801,1871,1941,2017,2087,2157` (27 each; 2 files, 54 occ):**
`measure2/mutant-no-byte-compare-observed.json`,
`measure3/mutant-no-byte-compare-observed.json`.

**Group E9 — lines `955,991,1025,1061,1095,1137,1171,1207,1241,1277,1311,1347,1381,1417,1451,1487,1521,1591,1661,1731,1801,1871,1907,1941,2017,2053,2087,2157` (28 each; 2 files, 56 occ):**
`measure2/mutant-bool-lax-observed.json`, `measure3/mutant-bool-lax-observed.json`.

**Group E10 — lines `26,51,76,101,301,326,376,551,576` (9; 1 file, 9 occ):**
`measure1/refinement-observed.json`.

**Group E11 — lines `26,51,76,101,301,326,376,551,576,701,726,826,851,876,976,1001,1026,1051,1076,1101,1126,1202,1252` (23; 1 file, 23 occ):**
`measure3/mutant-repo-unbound-refine-observed.json`.

Sum check: 49·26 + 38·22 + 3·1 + 2·23 + 2·25 + 2·27 + 2·25 + 2·27 + 2·28 + 9 + 23 = **2455**
occurrences in **104** files. All paths above are relative to
`.ufo/waves/round-22/evidence/` unless already prefixed.

### 4.5 Untracked generated cache (not evidence; 1 file, 1 occurrence)

`.ufo/waves/round-22/frozen/__pycache__/fixture-builder-v2.cpython-314.pyc` — byte-compiled
cache of the frozen builder; untracked (`??` in `git status`). Not part of r22 committed
evidence; must not be committed. No edit was made.

## 5. Recommended minimal documentation corrections (no edits made by this seat)

The corrections are **append-only blocks** (QUALITY #4, `corpus/QUALITY.md:6`); the existing
bytes at the referenced lines stay unchanged. Only two surfaces need correction; both are
named in the C1 contract.

### Correction A — `SKILL.md`, append after line 564 (EOF)

> Round23 correction (append-only; schema v2 cutover, C1): against tool revisions after the
> cutover every reconciler output — check, setup error and selftest alike — carries schema
> `mori-retention-reconciliation-v2`, and the key `raw_unallowlisted` is removed from every
> output with no alias. Read the in-scope (non-author-filtered) unallowlisted count from
> `scanner_unallowlisted` alone; `raw_not_allowlisted` remains the truthful raw complement
> (unchanged meaning; 9 on the r21 receipt, 95−86). The caveat paragraph above describes
> schema v1 and stays true for the r22 bytes; r22 frozen evidence stays byte-unchanged and
> the r22 claim stays reproducible at its bound revision
> `da40bb20f81da125d798f73cd1653655be1255ca`. On the r21 receipt at
> `77a5bbe8a0b41dfbfd2546d024d36e294b814bd0` the v2 output is exit0 `RETENTION_RECONCILED`
> with `scanner_total` 90, `scanner_unallowlisted` 4, `raw_not_allowlisted` 9, `raw_total` 95,
> `allowlisted` 86, `policy_excluded` 5, `retention_state` red and `privacy_clearance` false.
> No other output key, value, exit code or finding id changes; the four unallowlisted hits,
> original permission control RED 11/12, the two unknown historical dispositions and blocked
> baseline acceptance carry unchanged. Nothing here is privacy clearance.

### Correction B — `corpus/knowledge/retention-reconciliation-r22.md`, append after line 36

> Round23 correction (append-only; schema v2 cutover, C1): against tool revisions after the
> cutover every output carries schema `mori-retention-reconciliation-v2` and no
> `raw_unallowlisted` key. The in-scope (non-author-filtered) unallowlisted count is read from
> `scanner_unallowlisted` alone; `raw_not_allowlisted` keeps its meaning as the truthful raw
> complement. The paragraph above freezes the v1 alias meaning (4 on the r21 receipt) and
> remains true for schema v1 and the r22 bound revision
> `da40bb20f81da125d798f73cd1653655be1255ca`. Declared consequence: r22's
> `oracle-reconcile-v2.py` R02/R11/R12 and `measure-round22.py`'s whitelist read the removed
> key and no longer pass against post-C1 tool revisions; the r23 oracle re-expresses R01–R24
> (R02/R11/R12 on `scanner_unallowlisted`, expected 1/3/1) and adds R25 (schema v2, key
> absent) and R26 (`raw_not_allowlisted` independent count). Values otherwise unchanged; the
> four unallowlisted hits, RED 11/12, the two unknown dispositions and blocked baseline
> acceptance carry unchanged; this is not privacy clearance.

### Explicitly no correction

- `corpus/lessons/round-22.md:87` — historical r22 record, accurate at r22; the r23 lesson
  (draft `build/DraftLesson.md:88,95,97`) carries the cutover.
- `LOG.md:1527`, `SCORECARD.md:1422` — live r23 pre-registration/target rows; they describe
  the removal and remain true. L1 records results at measurement, not an errata block.
- `corpus/README.md` — zero occurrences; row `:420` stays true.
- All 163 r22 files in §4 — byte-unchanged (contract requires r22 reproducibility).
- All r23 harness artifacts in §3 — sealed/generated; not documentation surfaces.

## 6. Observed facts vs inference vs unknowns

- **Observed:** every `path:line` list above (literal byte census at HEAD `4dc80c1`; tracked
  tree clean). `tools/mori-retention-reconcile.py:234` is the only producer literal and
  `:16` is the only schema constant; no dynamic construction exists in `tools/`.
- **Inference (medium):** because check (`:231`), selftest (`:274`) and both setup-error
  results (`:287`, `:289`) all use `SCHEMA`, bumping `:16` plus deleting `:234` satisfies
  "schema v2 in every output / key removed" without touching other literals. This is a
  source read, not an execution (wave bans runs).
- **Unknown / limits:** no LSP server was mounted, so this is literal enumeration, not
  semantic proof beyond the matched lines. `.ufo/worktrees/` was not inspected (lane VCS
  bound); writer clones live under excluded `.scratch/`. Untracked `build/` and `wave1-*.json`
  are moving, so their counts are a snapshot. No runtime output was produced or verified.
- Original evidence remains byte-unchanged; this seat performed no remediation, pin,
  dispatch, config change, test, build or gate.
