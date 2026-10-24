VERDICT: BROKEN (narrow). One count in corpus/knowledge/wave-settlement-r20.md does not match its evidence: line 20 says "14 frozen + 7 refinement cases". The tool has 8 refinement cases (22 selftest cases in total). The other roughly 45 counts in the document match their cited evidence. Claim-level defects are listed in section 3; none of them changes a number.

Scope: corpus/knowledge/wave-settlement-r20.md (78 lines) checked against c2-live-mori.json, c2-live-fleet.json, c2-before.json, c2-after.json, the 24 build/Gt*.md ground-truth reports, and the cited build/, frozen/ and tool files. Read-only. Nothing in the lane was written.

## 1. Count mismatches (path:line)

- corpus/knowledge/wave-settlement-r20.md:20 — `--selftest  # 14 frozen + 7 refinement cases`.
  Observed: 8 refinement cases. tools/mori-wave-settlement.py:39-50 lists r1-godspeed-trailer, r1-crlf-trailer, r2-stub, r3-name-hint, r4-duplicate-dispatch, r5-duplicate-report-path, r6-taskcall-missing, r7-dotdot-inside-lane. Line 617 runs `cases + REFINEMENT_CASES`, so the total is 14 + 8 = 22.
  Run: copied the tool and frozen/c2-expected.json to /tmp/rkS (both tool copies have sha256 e5c06dad076b8e5aebbebcd53cf7c32de41592b4899319502b8cca003d4b8a48), then ran `python3 tools/mori-wave-settlement.py --selftest` from /tmp/rkS.
  Output: `MORI_WAVE_SETTLEMENT_SELFTEST: PASS (22 cases, 22 passed, 0 failed)`, exit 0.

No other count in the document is wrong.

## 2. Counts checked and matching

| doc line | claim | evidence | result |
|---|---|---|---|
| :12 | `probe_waves` at tools/mori-census.sh:865-932; results.json + 0 of 3 seat reports classed settled | census.sh:865 and :932 (probe_waves() { … }); CensusWavesSurface.md:7, :88 (T1, "0 of 3") | match |
| :20 | 14 frozen cases | frozen/c2-expected.json `.cases` length 14 | match |
| :29 | stub reads ≤16 bytes | tool:35 (STUB_CONTENTS, 16 B max), :229 (`size <= max(len(stub))`) | match |
| :40 | exit 0 / 1 / 2 | tool:366 (rc = 0 iff all settled/no-spawn), :674 and :683 (return 2), argparse exit 2 | match |
| :41-42 | exit 0 can coexist with unreadable_json > 0 | frozen malformed-dispatch expects exit 0, unreadable 1; live lore: unreadable_json 1, exit 0 (c2-live-fleet.json lanes[lore]) | match |
| :46 | 96 tabi clone tasks | TrailerVariants.md:12, :33, :60; GtLaneTabi.md:127 (3 trees × 32) | match |
| :54 | two name-hinted payloads never dispatched | GtLaneMado.md:39 (0/32 unsettled, "preview"); GtLaneRevenger.md:40 (0/32) | match |
| :55 | twelve name-hinted payloads executed | ContractReview.md:74 (12 of 14 non-nested). Recount: kake round-21 wave1-validation 64/64 (GtLaneKake.md:21); tabi canonical validation.json, 10 files, all present > 0 (GtLaneTabi.md:39-47, :49); tameshi validation-current.json 27/72 (GtLaneTameshi.md:38). Total 12 | match |
| :56 | kama r19 falsify = 66 | GtLaneKama.md:41 (row 16), :72 (refused 66, spawned 0) | match |
| :56 | kama r21 build = 86 | GtLaneKama.md:44 (row 19), :20, :75 | match (cause: see C1) |
| :60 | 63 same-stem .txt beside missing .md | GtLaneTabi.md:123, :129 (63 siblings of 64 missing in round-12/w1 + round-13/w1; AriaEntry has none) | match |
| :66 | oracle capability_absent 14 → 14/14 matched | c2-before.json `.counts` {capability_absent:14}; c2-after.json `.counts` {matched:14, mismatched:0}; both have 14 results | match |
| :68-70 | harness v0 scored 13/14 | c2-after-oracle-v0-fixture-defect.json `.counts` {matched:13, mismatched:1}; the failing case is no-spawn | match |
| :68-69 | v0 no-spawn wrote {"tasks":null} | OracleHarness/c2-oracle-v0.py:33 (`"taskCall": {"tasks": tasks}`), :138-139 (no-spawn passes None) | match |
| :71-74 | mori per-wave counts (table below) | c2-live-mori.json `.waves[]` and per-seat GT reports | match |
| :75-78 | 21 lanes; 196 dispatch files | c2-live-fleet.json `.lanes` length 21; Σ lanes[].waves = 196; TrailerVariants.md:9 and ContractReview.md:36 also give 196 | match |
| :77-78 | fleet per-lane totals (table below) | c2-live-fleet.json `.lanes[]` vs GtLane*.md totals | match |

Mori per-wave (doc :71-74 vs c2-live-mori.json `.waves[]`, index in brackets; GT source):

| wave | live present/members | GT | per-seat sets |
|---|---|---|---|
| r13 [0] | 32/32 | GtMoriR13.md:71, :73 | equal |
| r14 [1] | 32/32 | GtMoriR14.md:52 | equal |
| r15 [2] | 64/64 | GtMoriR15.md:20-22 | equal |
| r16 [3] | 64/64 | GtMoriR16W1.md:84-86 | equal |
| r17 W1 [4] | 70/70 | GtMoriR17W1.md:95 | equal |
| r17 W2 [5] | 64/64 | GtMoriR17W2.md:85 | equal |
| r18 W1 [6] | 53/68, 15 missing | GtMoriR18W1.md:89-90 | equal |
| r18 W2 [7] | 67/67 | GtMoriR18W2.md:87 | equal |
| r19 W1 [8] | 16/64, 48 missing | GtMoriR19W1.md:17-19 | equal |
| r19 W2 [9] | 48/70, 22 missing | GtMoriR19W2.md:13-15 | equal |

Fleet per lane (doc :77-78 vs c2-live-fleet.json; GT source):

| lane | doc | live | GT source |
|---|---|---|---|
| chousa | 120/136 | 120/136 | GtLaneChousa.md:24-26 |
| kaidoku | 824/959 | 824/959 | GtLaneKaidoku.md:36 |
| kake | 261/325 | 261/325 | GtLaneKake.md:7 |
| kasegi | 44/64 | 44/64 | GtLaneKasegi.md:32-34 |
| kengaku | 376/387 | 376/387 | GtLaneKengaku.md:33 |
| kumitate | 468/512 | 468/512 | GtLaneKumitate.md:33 |
| mado | 914/1030 | 914/1030 | GtLaneMado.md:59-60 |
| revenger | 0/32 | 0/32 | GtLaneRevenger.md:40 |
| souji | 662/783, 1 misrooted | 662/783, misrooted 1 | GtLaneSouji.md:36, :47 |
| tameshi | 857/965 | 857/965 | GtLaneTameshi.md:39 |
| tsukuroi | 767/834 | 767/834 | GtLaneTsukuroi.md:11, :31 |

Mid-round lanes (doc :78 says "moved between snapshots"): kagi GT 384 present (GtLaneKagi.md:47, 10:38:39Z) → live 437; kama GT 989 (GtLaneKama.md:17, 10:34:51Z) → live 997; tabi GT 3357 at T2 (GtLaneTabi.md:113, 07:36:54 −03 = 10:36:54Z) → live 3371. Movement confirmed.

Checks on the doc's § 5 (:73) claim that the 15 r18 missing names equal `wave1-dead-seats.json` (see C4): set-equal, 15 = 15, no duplicates.

## 3. Claim-level defects (no number changes)

- C1. :56-58 says kama r19 falsify (66) and r21 build (86) "were refused at the job cap". GtLaneKama.md:72 supports the cap for r19 falsify only ("Background job limit reached (100)"). GtLaneKama.md:75 records r21 build "refused all 86" on attempt 1 and gives no cause. The cap cause for r21 is not supported by the cited source. [INFERENCE] it may have been the cap, but nothing observed says so.
- C2. :46-50 (§3) describes R1–R5 only. The tool also implements R6 (tools/mori-wave-settlement.py:47, taskCall missing → unavailable) and R7 (:48-50, `..` inside the lane → unsafe), and selftests both. The tool docstring (:5-15) also lists only R1–R5. Together with the wrong count in C-§1, the refinement set is undocumented.
- C3. Decision table (:23-38) and the `missing` field:
  (a) The wave-level `missing` array holds every non-present member (tools/mori-wave-settlement.py:290-291), including stub, empty, misrooted, unsafe and unparsed. In live data, c2-live-mori.json `.waves[10]` (mori-r20-build) has `missing` = [ContractReview, HistR13, HistR14R15, TokPathAge, TokSilenceA, VolatileContract], all status `stub`, while `.counts.missing` = 0. The document does not say this. Its :29 (stub) and :31 (missing) rows imply the opposite.
  (b) No row covers symlink, directory, FIFO or unreadable (EACCES) report paths. `_member_status` (tools/mori-wave-settlement.py:224-237) sends every non-regular lane path to `missing`. The frozen symlink-report case pins this (tool:582-586 expects `missing` with not_followed). The behaviour matches the contract, but :31 "no file anywhere checked → missing" is inaccurate for these cases.
  (c) :30 says the fleet path must "exist". The code requires a regular file with no size check (tool:233-236).
- C4. :73 cites `wave1-dead-seats.json` without a path. The file is .ufo/waves/round-18/evidence/wave1-dead-seats.json (seats at lines 7-21), not a round-20 file.
- C5. :14-16 says the scan finds "a non-empty report". The tool's `present` also excludes the start stub (tool:229-231), and a stub is non-empty. Wording should read "present (non-empty, not the start stub)".
- C6. :60 says tabi r12/r13 "wrote 63 same-stem .txt files". The evidence shows 63 .txt siblings exist beside missing .md paths (GtLaneTabi.md:129). It does not show who wrote them, and GtLaneTabi.md:162 marks the format as [INFERENCE]. Wording should read "exist beside".
- C7. :75 says "Fleet scan 10:46:50Z". c2-live-fleet.json has no timestamp field. Its file mtime is 10:46:53.06Z (stat). The mori scan time 10:46:42Z matches its file mtime (10:46:42.50Z). [INFERENCE] 10:46:50Z is the scan start. It cannot be confirmed from the evidence.
- C8. :41-42 tells the reader to "always read the count" of unreadable_json, but §5 gives none for any lane. Live values: kaidoku 39 (GtLaneKaidoku.md:58), mado 2 (GtLaneMado.md:27), mori 2 (c2-live-mori.json top-level), kama 1 (GtLaneKama.md:96), lore 1 (c2-live-fleet.json lanes[lore]; no GT). Total 45, matching ContractReview.md:43.
- C9. :71-74 says "all ten historical mori waves". That is accurate, but c2-live-mori.json has 11 waves. The 11th (mori-r20-build, in flight, 70/76 with 6 stub) is omitted, and the lane totals (waves 11, partial 4, settled 7, members 671, present 580, missing 85, stub 6) are not reported.
- C10. :54-55 "two" and "twelve" are counts over the 14 non-nested payloads (ContractReview.md:74). c2-live-fleet.json `.dispatch_filename_flags` lists 47 (33 under final-clones/). The document does not state its scope.
- C11. R3 `name_hint` (tools/mori-wave-settlement.py:301) emits "undispatched-name:<word>" for every match, including `validation`. The 12 executed validation payloads (C-§1 :55) would therefore carry the label "undispatched-name:validation". :49 says "shape only" but does not disclose the label text.
- C12. Tool docstring (tools/mori-wave-settlement.py:9-10) says stub reads "at most 64 bytes". The code reads ≤16 (:229). The document's ≤16 (:29) is correct; the docstring is stale.

## 4. Evidence-internal observations (for L1; not errors in the document)

- E1. c2-live-fleet.json lanes[mori-shokunin]: members 671, but present 580 + missing 85 + misrooted 0 = 665. The 6 stub members have no field in the fleet schema (c2-live-mori.json `.totals.stub` = 6).
- E2. GtLaneTabi.md:129 says "round-12/w1 (31 of 32 missing)". Its own table (GtLaneTabi.md:36) gives 32 missing, and the same paragraph says "64 missing members". 64 − 1 (AriaEntry) = 63, which is the figure the document uses.
- E3. GtLaneSouji.md:36, :47 counts 1 misrooted inside 121 "missing". The live record counts 120 missing plus 1 misrooted. The totals agree (121); the definition differs.
- E4. Stub timing: ContractReview.md (mtime 10:47:54Z), TokSilenceA (10:49:57Z), VolatileContract (10:48:25Z), TokPathAge (10:52:45Z), HistR13 (10:54:01Z), HistR14R15 (10:56:37Z) were all written after the 10:46:42Z scan. Their stub status at scan time is therefore consistent, not a defect.
- E5. c2-live-fleet.json carries lane totals only (no per-seat or per-wave arrays). Fleet per-seat claims can be checked only against GT totals.

## 5. Verification log

- Per-seat sets (python in the eval kernel, read-only): for all 10 historical waves, GT names == live member names, GT present set == live present set, GT missing set == live missing set, no duplicate names. Result: 10/10 equal.
- r18 dead seats: c2-live-mori `.waves[6].missing` (15) vs round-18/evidence/wave1-dead-seats.json `.seats` (15): set-equal, True.
- Refinement count: static, 8 entries (tool:39-50); dynamic, 22/22 PASS (section 1).
- Frozen count: c2-expected.json `.cases` = 14.
- Fleet sums: Σ waves = 196; Σ members = 12,307 (= TrailerVariants.md:36); Σ present 10,678 + Σ missing 1,622 + misrooted 1 + stub 6 = 12,307; Σ unreadable_json = 45 (39+1+1+2+2).
- git (read-only: cat-file, log): e4d9384 = "round-20: freeze C1/C2 contract and entering drift receipt before implementation" (2026-10-21T07:23:18-03:00). 2eeae04 = "round-20: C2 wave-settlement tool, independent oracle before/after, live lane and fleet scans, wave-1 dispatch evidence" (07:47:09-03:00); tools/mori-wave-settlement.py exists at 2eeae04. Both doc hashes (:3-4) verified.
- stat (read-only): c2-live-mori.json 07:46:42.500 −0300; c2-live-fleet.json 07:46:53.060 −0300; c2-before.json 07:46:29.967; c2-after.json 07:46:30.524.
- Oracle independence (doc :66): OracleHarness/c2-oracle.py imports argparse, json, os, pathlib, subprocess, tempfile. It does not import the tool; it runs it as a subprocess (:166). Matches the document.
- Selftest rc: 0. Scan rc (not run): tool:366 defines it.

## 6. Not verified / [INFERENCE]

- Fleet per-seat states (evidence has totals only).
- Whether the r21 build refusal was a job-cap refusal (C1). No cause is recorded in the cited sources.
- Authorship of the 63 .txt files (C6).
- Scan start time 10:46:50Z (C7).

## 7. Tooling and bounds

- Installs or updates: none. Used python3 3.14.8 stdlib (eval kernel and tool selftest), git read-only (cat-file, log), stat, sha256sum, cp, rm.
- Scratch: /tmp/rkS (tool copy and frozen oracle copy). The lane was not modified.
- Not run: tools/mori-census.sh; any scan of the lane or fleet .ufo/waves (the tool's scan was not run).
- Not opened: .ufo/interactive-sessions/, .ufo/worktrees/, .jj/, ~/.omp logs.
- Glob and grep were limited to named paths: build/Gt*.md, build/GtLane*.md, build/OracleHarness/*, round-20 directory listing, and the named tool, evidence and frozen files.
