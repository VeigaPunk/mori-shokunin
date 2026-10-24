PARTIAL

Differential attack on C2 (`tools/mori-wave-settlement.py`) against the independent build (`build/ImplSettlementAlt/tools/mori-wave-settlement.py`). Four lanes, 56 waves, 3,491 members. Per-wave agreement holds on live data once R2-R4 are accounted for. The attack breaks specific edge behaviour in both implementations (sections 5-6). No file was edited; no tool was installed.

## 1. Verdict in brief

- HOLDS (live lanes): every one of the 56 waves agrees on sha256, wave id, member name/agent/status (production `stub` mapped to `present`), missing list and counts. Wave state agrees on 55 of 56. The one state difference is R2 (mori round-20 `wave2-run.json`). R3 and R4 differ only as extra fields.
- HOLDS (frozen contract): frozen 14 cases, production 14/14 matched, alt 14/14 matched (oracle, section 8). Production selftest 22/22 PASS.
- BROKEN, production, edge configurations:
  - P1: a misrooted member is reported `missing` when `--fleet-root` is reached through a symlink (contract's misrooted clause violated).
  - P2: a nonexistent or non-directory `--fleet-root` is silently accepted.
  - P3: a symlinked lane root is refused with exit 2 ("lane root is unreadable").
  - P4: uncaught RecursionError (exit 1 plus traceback) on a `.ufo/waves` tree about 1000 levels deep.
- BROKEN, alt:
  - A1: absent `taskCall` key read as `null`, giving `no-spawn` and exit 0 (fail-open).
  - A2: no R2, so live mori round-20 `wave2-run.json` reads `settled` with 67 of 67 "present" while 47 members still hold only `STATUS: started`. Production reads `partial`.
  - A3: no R1, so a `| godspeed` envelope, trailing whitespace or trailing prose after a valid trailer reads `unparsed`.
  - A5: accepts NaN/Infinity (non-RFC JSON).
  - A9: emits the same schema id `mori-wave-settlement-v1` with a different totals shape.
- SHARED: S1 symlinked dispatch files and a symlinked `.ufo` are dropped with no counter. S2 exit 0 when no readable dispatch exists. S3 seat probe fixtures under `round-20/falsify/**` are counted as waves in mori.

## 2. Method and provenance

- Production: `tools/mori-wave-settlement.py`, sha256 `e5c06dad076b8e5aebbebcd53cf7c32de41592b4899319502b8cca003d4b8a48`, mtime 2026-10-21 08:04:26 -0300 (11:04:26Z). It changed during my session from sha `c6e6091937e4bcb02775cea81ce33990924c6e27487a6ce255d2959d94f4e795`. Observed delta: +3 header lines (R7 comment and `REFINEMENT_CASES` entry); file grew by 7 lines in total. The other 4 lines were not inspected [INFERENCE: an r7 fixture branch in `_fixture`]. I re-read `_safe_report_path`, `_trailer`, `_member_status`, `_summarize_wave`, `scan_lane` and `main` after the change; their logic is unchanged and their line offsets shifted by +3. All reported results use e5c06dad.
- Alt: `.ufo/waves/round-20/build/ImplSettlementAlt/tools/mori-wave-settlement.py`, sha256 `59f3751c9309da2a90a1e5b1a9a74889ad32fcf3f0e74711afbf481a4808f26b`. Unchanged during the session.
- Interpreters: python3 3.14.8; `/usr/bin/jq` 1.8.2. Installs or updates: none.
- Lanes (all with `--fleet-root /home/vgpnk/Projects/shokunin`): mori-shokunin (own lane), tabi-shokunin, kaidoku-shokunin, souji-shokunin. Chosen because tabi has the largest name-hint and duplicate surface (10 `validation.json` waves, 1 duplicate), kaidoku has the only live unreadable-JSON path (39 files), and souji has the only live misrooted member (1).
- Primary run, `run1`: for each lane, production then alt back-to-back, output to `/tmp/diffalt-r20/run1/{prod,alt}-<lane>.json`, between 11:07:37Z and 11:07:39Z. Command shape:
  - `python3 <tool> scan --lane-root /home/vgpnk/Projects/shokunin/<lane> --fleet-root /home/vgpnk/Projects/shokunin --out <file>`
  - Exit codes: production 1, alt 1 for all four lanes (each lane has at least one non-settled wave).
  - Counters (ignored / unreadable / waves), identical for both tools: mori 657/2/14; tabi 221/0/16; kaidoku 3358/39/14; souji 43/0/12.
- Discovery-set identity: an in-process import of both modules, comparing production `_dispatch_files` with alt `_walk_json_files` against a direct `os.walk` census, gave identical JSON path sets for all four lanes at the time of the check.
- Per-lane states (prod / alt): mori {settled 8, partial 4, unsettled 1, no-spawn 1} / {settled 9, partial 3, unsettled 1, no-spawn 1}; tabi {settled 8, partial 6, unsettled 2} for both; kaidoku {settled 7, partial 7} for both; souji {settled 6, partial 5, unsettled 1} for both. Mori's difference is the R2 wave.
- Mapping used for the comparison: production `stub` treated as `present`. The alt has no `stub` status, and its `counts` dict is compared after the same mapping. Extra production fields (`name_hint`, `duplicate_of`, `duplicate_report_paths`, `unique_dispatch_sha256`, `name_hinted_waves`) are reported as attribution, not as mismatch.

## 3. Per-wave differential, run1 (56 waves)

Every row: `unexplained` = none. Columns: prod / alt state; present counts stub-inclusive; `explained by` = R-refinement or field-only.

| lane | dispatch (under .ufo/waves/) | wave id | members | prod state | alt state | present (incl. stub) | stub | missing | unsafe+unparsed | misrooted | explained by |
|---|---|---|---:|---|---|---:|---:|---:|---:|---:|---|
| mori | round-13/dispatch.json | mori-r13-build | 32 | settled | settled | 32 | 0 | 0 | 0 | 0 | - |
| mori | round-14/dispatch.json | mori-r14-repair | 32 | settled | settled | 32 | 0 | 0 | 0 | 0 | - |
| mori | round-15/dispatch.json | mori-r15-positive | 64 | settled | settled | 64 | 0 | 0 | 0 | 0 | - |
| mori | round-16/wave1-dispatch.json | mori-r16-window-build | 64 | settled | settled | 64 | 0 | 0 | 0 | 0 | - |
| mori | round-17/wave1-dispatch.json | mori-r17-w1-build | 70 | settled | settled | 70 | 0 | 0 | 0 | 0 | - |
| mori | round-17/wave2-dispatch.json | mori-r17-w2-falsify | 64 | settled | settled | 64 | 0 | 0 | 0 | 0 | - |
| mori | round-18/wave1-dispatch.json | mori-r18-w1-build | 68 | partial | partial | 53 | 0 | 15 | 0 | 0 | - |
| mori | round-18/wave2-dispatch.json | mori-r18-w2-falsify | 67 | settled | settled | 67 | 0 | 0 | 0 | 0 | - |
| mori | round-19/wave1-run.json | mori-r19-attempt2-build | 64 | partial | partial | 16 | 0 | 48 | 0 | 0 | - |
| mori | round-19/wave2-run.json | mori-r19-attempt2-falsify | 70 | partial | partial | 48 | 0 | 22 | 0 | 0 | - |
| mori | round-20/falsify/SentinelTool/probe-20261021/lane/.ufo/waves/round-1/dispatch.json | sentinel-scratch-probe | 4 | unsettled | unsettled | 0 | 0 | 3 | 1 | 0 | - (seat probe, S3) |
| mori | round-20/falsify/SentinelTool/probe-20261021/outside/secret.json | OUTSIDE-WAVE-CANARY | 0 | no-spawn | no-spawn | 0 | 0 | 0 | 0 | 0 | - (seat probe, S3) |
| mori | round-20/wave1-run.json | mori-r20-build | 76 | settled | settled | 76 | 0 | 0 | 0 | 0 | - |
| mori | round-20/wave2-run.json | mori-r20-falsify | 67 | partial | settled | 67 | 47 | 0 | 0 | 0 | R2: stub=47; state partial to settled |
| tabi | round-12/w1/dispatch.json | tabi-round-12-w1 | 32 | unsettled | unsettled | 0 | 0 | 32 | 0 | 0 | - |
| tabi | round-13/w1/dispatch.json | tabi-round-13-w1 | 32 | unsettled | unsettled | 0 | 0 | 32 | 0 | 0 | - |
| tabi | round-14/w1/dispatch.json | tabi-round-14-w1 | 32 | settled | settled | 32 | 0 | 0 | 0 | 0 | - |
| tabi | round-15/w1/validation.json | tabi-round-15-w1 | 64 | partial | partial | 49 | 0 | 15 | 0 | 0 | R3: name_hint (field only) |
| tabi | round-15/w2/validation.json | tabi-round-15-w2 | 32 | settled | settled | 32 | 0 | 0 | 0 | 0 | R3: name_hint (field only) |
| tabi | round-16/w1/validation.json | tabi-round-16-w1 | 84 | partial | partial | 78 | 0 | 6 | 0 | 0 | R3: name_hint (field only) |
| tabi | round-16/w2/validation.json | tabi-round-16-w2 | 73 | settled | settled | 73 | 0 | 0 | 0 | 0 | R3: name_hint (field only) |
| tabi | round-17/w1/validation.json | tabi-round-17-w1 | 86 | settled | settled | 86 | 0 | 0 | 0 | 0 | R3: name_hint (field only) |
| tabi | round-17/w2/validation.json | tabi-round-17-w2 | 78 | partial | partial | 52 | 0 | 26 | 0 | 0 | R3: name_hint (field only) |
| tabi | round-18/w1/validation.json | tabi-round-18-w1 | 70 | settled | settled | 70 | 0 | 0 | 0 | 0 | R3: name_hint (field only) |
| tabi | round-18/w2/validation.json | tabi-round-18-w2 | 80 | settled | settled | 80 | 0 | 0 | 0 | 0 | R3: name_hint (field only) |
| tabi | round-19/w1/validation.json | tabi-round-19-w1 | 72 | settled | settled | 72 | 0 | 0 | 0 | 0 | R3: name_hint (field only) |
| tabi | round-19/w2/dispatch.json | tabi-round-19-w2 | 72 | partial | partial | 70 | 0 | 2 | 0 | 0 | - |
| tabi | round-19/w2/validation.json | tabi-round-19-w2 | 72 | partial | partial | 70 | 0 | 2 | 0 | 0 | R3 name_hint + R4 duplicate_of (byte-identical to round-19/w2/dispatch.json; field only) |
| tabi | round-20/w1/dispatch.json | tabi-round-20-w1 | 64 | partial | partial | 63 | 0 | 1 | 0 | 0 | - |
| tabi | round-20/w2/dispatch.json | tabi-round-20-w2 | 64 | settled | settled | 64 | 0 | 0 | 0 | 0 | - |
| kaidoku | round-14/dispatch.json | kaidoku-r14-w1 | 32 | settled | settled | 32 | 0 | 0 | 0 | 0 | - |
| kaidoku | round-15/dispatch.json | kaidoku-r15-w1 | 32 | settled | settled | 32 | 0 | 0 | 0 | 0 | - |
| kaidoku | round-16/wave1-dispatch.json | kaidoku-r16-w1 | 64 | partial | partial | 36 | 0 | 28 | 0 | 0 | - |
| kaidoku | round-16/wave2-dispatch.json | kaidoku-r16-w2 | 32 | settled | settled | 32 | 0 | 0 | 0 | 0 | - |
| kaidoku | round-17/wave1-dispatch.json | kaidoku-r17-w1 | 78 | settled | settled | 78 | 0 | 0 | 0 | 0 | - |
| kaidoku | round-17/wave2-dispatch.json | kaidoku-r17-w2 | 69 | partial | partial | 67 | 0 | 2 | 0 | 0 | - |
| kaidoku | round-18/wave1-dispatch.json | kaidoku-r18-w1 | 89 | settled | settled | 89 | 0 | 0 | 0 | 0 | - |
| kaidoku | round-18/wave2-dispatch.json | kaidoku-r18-w2 | 98 | partial | partial | 94 | 0 | 4 | 0 | 0 | - |
| kaidoku | round-19/wave1-dispatch.json | kaidoku-r19-w1 | 90 | partial | partial | 48 | 0 | 42 | 0 | 0 | - |
| kaidoku | round-19/wave2-dispatch.json | kaidoku-r19-w2 | 72 | settled | settled | 72 | 0 | 0 | 0 | 0 | - |
| kaidoku | round-20/wave1-dispatch.json | kaidoku-r20-w1 | 100 | partial | partial | 98 | 0 | 2 | 0 | 0 | - |
| kaidoku | round-20/wave2-dispatch.json | kaidoku-r20-w2 | 71 | settled | settled | 71 | 0 | 0 | 0 | 0 | - |
| kaidoku | round-21/wave1-dispatch.json | kaidoku-r21-w1 | 64 | partial | partial | 26 | 0 | 38 | 0 | 0 | - |
| kaidoku | round-21/wave2-dispatch.json | kaidoku-r21-w2 | 68 | partial | partial | 49 | 0 | 19 | 0 | 0 | - |
| souji | round-13/w1-dispatch.json | souji-r13-w1 | 32 | settled | settled | 32 | 0 | 0 | 0 | 0 | - |
| souji | round-14/w1-dispatch.json | souji-r14-w1 | 32 | settled | settled | 32 | 0 | 0 | 0 | 0 | - |
| souji | round-15/w1-dispatch.json | souji-r15-w1 | 64 | settled | settled | 64 | 0 | 0 | 0 | 0 | - |
| souji | round-16/w1-dispatch.json | souji-r16-w1 | 65 | partial | partial | 63 | 0 | 2 | 0 | 0 | - |
| souji | round-16/w2-dispatch.json | souji-r16-w2 | 79 | partial | partial | 78 | 0 | 1 | 0 | 0 | - |
| souji | round-17/w1-dispatch.json | souji-r17-w1 | 78 | settled | settled | 78 | 0 | 0 | 0 | 0 | - |
| souji | round-17/w2-dispatch.json | souji-r17-w2 | 71 | partial | partial | 43 | 0 | 28 | 0 | 0 | - |
| souji | round-18/w1-dispatch.json | souji-r18-w1 | 91 | settled | settled | 91 | 0 | 0 | 0 | 0 | - |
| souji | round-18/w2-dispatch.json | souji-r18-w2 | 79 | settled | settled | 79 | 0 | 0 | 0 | 0 | - |
| souji | round-20/final-dispatch.json | souji-r20-final | 64 | partial | partial | 63 | 0 | 0 | 0 | 1 | - (misrooted, both tools) |
| souji | round-20/recovery-dispatch.json | souji-r20-recovery | 64 | partial | partial | 39 | 0 | 25 | 0 | 0 | - |
| souji | round-20/w1-dispatch.json | souji-r20-w1 | 64 | unsettled | unsettled | 0 | 0 | 64 | 0 | 0 | - |

Live check: mori round-19 wave1 (16/64, 48 missing) and wave2 (48/70, 22 missing) reproduce the figures recorded in the round-20 lesson for both tools.

## 4. Attribution of every difference

- R2 (stub): mori `round-20/wave2-run.json`. Production: 20 present, 47 stub (start stub `STATUS: started`), 0 missing, `partial`, exit contribution 1. Alt: 67 present, `settled`. This is the M3 vacuous-count failure the lesson describes, reproduced by the alt. Stub-mapped member lists, counts and missing lists match exactly. Stub count moved 60 (10:46Z) to 51 to 47 during my session as live seats wrote.
- R3 (`name_hint`): 10 tabi waves, all `validation.json`. Alt lacks the field. States agree.
- R4 (`duplicate_of`): 1 tabi wave, `round-19/w2/validation.json`, byte-identical to `round-19/w2/dispatch.json`. Alt lacks the field. `unique_dispatch_sha256` is absent from the alt's totals.
- R1 (trailer rstrip / last matching line): not exercised by any live wave in these four lanes (unparsed = 0 under both tools). R1 is exercised by fixtures C14, C15b, C16 and C40 (section 5).
- R5 (`duplicate_report_paths`): 0 in these lanes. Fixture C49 only.
- R6 (missing `taskCall` key, disclosed in the lesson, production selftest `r6-taskcall-missing`): 0 in these lanes. Fixture C01.

No difference in these four lanes is unexplained.

## 5. Edge-case differential (fixtures under /tmp/diffalt-r20/fx; outputs /tmp/diffalt-r20/fxout)

Notation: rc = exit code; ign / unr = ignored_json / unreadable_json.

| case | production | alt | attribution |
|---|---|---|---|
| C01 dispatch without `taskCall` key | rc1 `unavailable` | rc0 `no-spawn` | alt A1 (fail-open) |
| C03 misspelled `task_call` key, one member unreported | rc1 `unavailable` | rc0 `no-spawn` | alt A1 (fail-open) |
| C04 `"wave": NaN` in dispatch | rc0 unr=1, 0 waves | rc0 `settled` 1/1 | alt A5 (lenient JSON) |
| C05 `NaN` in non-dispatch JSON | unr=1 | ign=1 | alt A5 |
| C06 lane root is a symlink to the lane | rc2 "lane root is unreadable" | rc0/1, scanned normally | prod P3 |
| C07 `--fleet-root` nonexistent | rc1; misrooted check silently disabled | rc2 "fleet root is unavailable" | prod P2 |
| C08 `--fleet-root` is a symlink to fleet; report exists in fleet at same path | `missing` | `misrooted` | prod P1 |
| C09 literal file `..\x.md` in lane | `present` | `unsafe` | policy A7 |
| C10 member names null and 5 | `missing` list `[5, "Z", null]` | `["", "", "Z"]` | prod P6 / alt A6 |
| C12 lane symlink at report path to lane file; fleet has regular file | `missing` | `misrooted` | prod P5 / alt A8 (contract-ambiguous) |
| C13 lane directory at report path; fleet has regular file | `missing` | `misrooted` | prod P5 / alt A8 |
| C14 godspeed envelope line after trailer | `present` | `unparsed` | R1 (alt A3) |
| C15b two blank lines after trailer | `present` | `unparsed` | R1 (alt A3) |
| C16 trailing spaces after trailer | `present` | `unparsed` | R1 (alt A3) |
| C17 report content `STATUS: started\n` (16 bytes) | `stub` | `present` | R2 (alt A2) |
| C18 report content `STATUS: started` (15 bytes) | `stub` | `present` | R2 (alt A2) |
| C20 literal file `C:x.md` in lane | `present` | `unsafe` | policy A7 |
| C21 two byte-identical dispatch files | `duplicate_of` set on b.json | no field | R4 |
| C40 prose after trailer | `present` | `unparsed` | R1 (alt A3) |
| C49 two members share one report path | `duplicate_report_paths` 1 | no field | R5 |
| C50 `agent` is 5 | agent `5` | agent `null` | alt A6 |
| C51 dispatch at depth 1100 under `.ufo/waves` | rc1, RecursionError traceback, no output | rc0/1 scanned | prod P4 (threshold: ok at depth 990, crash at 1010) |

Same in both (no attribution needed beyond the shared rows in S1-S2): C02 (`taskCall: null`, no-spawn), C11, C15 (single trailing newline), C19 (CRLF stub, present in both), C22 (`dir.json` holding a dispatch), C23 (symlinked dispatch), C24 (FIFO at report path; no hang), C25 (unreadable small report counted present), C26 (unreadable dispatch), C27-C29 (no `.ufo/waves`, empty waves, `.ufo` symlink), C30, C31 (name `null`, lossy only in alt), C32-C33 (lane root file or missing, rc2), C34 (BOM), C35 (lone surrogate name), C36-C39 (report path `.`, trailing slash, absolute, two trailers), C41-C48, C52-C53 (invalid UTF-8; 5000-digit integer literal; both unreadable), C45-C46 (CRLF trailer; byte-order sort), C47 (intermediate symlink dir not followed), C48 (report path with a space: unparsed in both).

Full TSV: `falsify/DiffAltImpl/edge-fixtures-differential.tsv`.

## 6. Findings

### Production (`tools/mori-wave-settlement.py`, e5c06dad)

- P1 (medium, contract-violating in that configuration). `scan_lane` stores `fleet_root = os.path.abspath(...)` (line 317) without resolving it. `_inspect_report_path` lstats that root (lines 177-185); a symlinked root is `other`, so `_member_status` (lines 234-237) never sees the regular file. Result: a file under the fleet root at the same relative path is reported `missing`, not `misrooted`. Fixture C08. The contract says "If missing under the lane root but the same relative path is a regular file under --fleet-root, the member is misrooted."
- P2 (low-medium, silent degradation). `--fleet-root` is never validated. A nonexistent or non-directory path yields `missing` for every member and exit by state, with no error. Fixture C07. The alt exits 2.
- P3 (low-medium, false error). `scan_lane` lines 310-314 lstat the lane root and require `S_ISDIR`, so a symlinked lane root is refused with exit 2 "lane root is unreadable". Fixture C06. The lane is readable; the alt resolves it.
- P4 (low, crash). `_dispatch_files.visit` (lines 99-124) recurses per directory. Depth 990 passes; depth 1010 raises RecursionError, which escapes `main` (exit 1, traceback, no `--out`). Fixture C51 and depth probes. Exit 1 is indistinguishable from "unsettled" for a caller.
- P5 (low, narrower misroot rule). Misroot is checked only when `lane_kind == "missing"` (line 234). A lane symlink or directory at the report path is classed `other` and reported `missing` even when the fleet holds the file. Fixture C12/C13. The contract wording is ambiguous here [INFERENCE: intent is "lane has no regular report"].
- P6 (low, type drift). `_summarize_wave` (lines 263-264) passes raw `name` and `agent` through, so `missing` can contain `null` or `5` (fixtures C10, C31, C50).
- P7 (info, doc drift). The header (lines 5-15, 38) says R1-R5 plus missing taskCall; the code also has R6 and R7. R2's docstring says "at most 64 bytes are read"; the code reads only files of 16 bytes or fewer (line 229). The lesson says "seven refinement selftest cases"; there are eight.

### Alt (`ImplSettlementAlt/tools/mori-wave-settlement.py`, 59f3751c)

- A1 (high, fail-open). `document.get("taskCall")` (line 136) returns `None` for an absent key, which `_wave_state` maps to `no-spawn` (lines 118-120). Absent and `null` are conflated. C01 and C03 exit 0 where production exits 1. The production decision table (knowledge note section 2) and the frozen wording (`taskCall: null` -> no-spawn) both distinguish them. The production selftest case `r6-taskcall-missing` fails under the alt (exit 0 vs 1).
- A2 (high, false clean on live data). `_regular_report_state` treats any regular file with size > 0 as present (lines 57-77). Start stubs count as present. On the live mori round-20 `wave2-run.json`, 47 of 67 members hold only `STATUS: started`; the alt reports `settled`, production reports `partial`. Selftest `r2-stub` fails under the alt.
- A3 (medium). Trailer read from `lines[-1]` only (line 85). A godspeed envelope after the trailer (C14), trailing blank lines (C15b), trailing whitespace (C16) and trailing prose (C40) make the member `unparsed`. Selftest `r1-godspeed-trailer` fails under the alt. The lesson reports 96 tabi clone tasks with a godspeed envelope; I did not re-observe that (current tabi has 0 unparsed) [INFERENCE: tree has moved].
- A4 (low). No R3, R4 or R5 fields. Selftest `r3-name-hint`, `r4-duplicate-dispatch`, `r5-duplicate-report-path` fail under the alt on fields only.
- A5 (medium-low, lenient JSON). `json.loads(raw)` (line 132) accepts NaN and Infinity. C04 turns a file production counts as unreadable into a scored wave; C05 turns an unreadable non-dispatch file into an ignored one. The contract counts "unparseable JSON" as `unreadable_json`, and NaN is not RFC 8259 JSON.
- A6 (low). Non-string member names become `""` and non-string agents become `null` (lines 111-114). Two distinct malformed members collapse into one name.
- A7 (low, policy, fail-closed). `_safe_parts` also applies Windows path rules (`PureWindowsPath`, lines 47-49). `..\x.md` (C09) and `C:x.md` (C20) are `unsafe`. Production treats them as literal POSIX names (`present`). Neither reads outside the lane.
- A8 (low, policy). Misroot check runs for every lane status other than present or empty (lines 94-100), so a lane symlink or directory plus a fleet file is `misrooted` (C12/C13). See P5.
- A9 (medium for consumers). Same `schema` string as production, different shape: `totals` nests `counts`, `states` lists zeros, and `unique_dispatch_sha256`, `name_hinted_waves`, and per-wave `name_hint`, `duplicate_of`, `duplicate_report_paths` are absent (lines 240-264). `main` has no `--selftest` and writes to stdout only when `--out` is absent.
- Strengths of alt: resolves symlinked lane and fleet roots (C06, C08), exits 2 for a bad fleet root (C07), iterative walk (C51). It passes the frozen 14 and selftest `r1-crlf-trailer` and `r7-dotdot-inside-lane`.

### Shared

- S1 (medium, silent omission). A symlinked `*.json` dispatch file (C23) or a symlinked `.ufo` (C29) is skipped without any counter. Both tools exit 0 when that is the only dispatch. The contract's counters (`ignored_json`, `unreadable_json`) do not cover symlinks.
- S2 (medium, operational). Exit 0 whenever there are no readable dispatch records (C26 unreadable only; C27 empty `waves`; C28 no `.ufo`). This matches the contract's wording ("every discovered wave settled or no-spawn" is vacuously true) but is a fail-open trap for any caller that reads exit 0 as "settled".
- S3 (operational, contamination of live numbers). `.ufo/waves/round-20/falsify/SentinelTool/probe-20261021/` is walked as part of mori. It contributes `sentinel-scratch-probe` (unsettled, one deliberate `Traversal` unsafe member) and `OUTSIDE-WAVE-CANARY` (no-spawn). Both tools count these in mori's 14 waves. Contract-consistent (recursive discovery) but it inflates live totals and state counts.

## 7. Verification gaps and [INFERENCE]

- R1, R5 and R6 are exercised only by fixtures, not by live data in these lanes.
- The live trees moved during the session. Mori stub count 60 to 51 to 47; mori waves 11 to 14 since the 10:46:50Z fleet evidence; tabi 67 waves and 3,932 members in `.ufo/waves/round-20/evidence/c2-live-fleet.json` (waves field is a count) against 16 waves and 1,007 members now. [INFERENCE: live movement; not investigated.] Compare live totals only with a timestamp.
- Self-contamination, corrected: my first scratch outputs were written as JSON under `falsify/DiffAltImpl/`, inside mori's `.ufo/waves`. They raised mori `ignored_json` during the session (584 to 608). I moved them to `/tmp/diffalt-r20/scratch-moved/`. The seat directory now holds TSV files only, which the tools do not count.
- Earlier batch: the first run (production c6e6, before the change above) gave the same per-wave outcome apart from the live stub count. The reported run is run1 (e5c06dad).
- The alt selftest comparison (section 8) is my harness (`check_expect`), which mirrors the production `_check_case` for alt-visible fields. Fields the alt lacks count as failures.
- Not run: `tools/mori-census.sh`; not opened: `.ufo/interactive-sessions/`, `.ufo/worktrees/`, `.jj/`, session logs; no subagents.
- Not tested: concurrent writers during a scan; byte-identical reruns on live trees (the frozen `deterministic` case passes for both on fixtures).

## 8. Reproduction and artifacts

- Frozen oracle, production: `python3 .ufo/waves/round-20/build/OracleHarness/c2-oracle.py --tool tools/mori-wave-settlement.py --out <file>` -> counts `{"capability_absent":0,"matched":14,"mismatched":0}`, exit 0.
- Frozen oracle, alt: same command with `--tool .ufo/waves/round-20/build/ImplSettlementAlt/tools/mori-wave-settlement.py` -> `{"capability_absent":0,"matched":14,"mismatched":0}`, exit 0.
- Production selftest: `python3 tools/mori-wave-settlement.py --selftest` -> `MORI_WAVE_SETTLEMENT_SELFTEST: PASS (22 cases, 22 passed, 0 failed)`, exit 0.
- Production expectations run through the alt (my harness; outputs `falsify/DiffAltImpl/production-selftest-vs-alt.tsv`): 16 of 22 pass. Failing: r1-godspeed-trailer, r2-stub, r3-name-hint, r4-duplicate-dispatch, r5-duplicate-report-path, r6-taskcall-missing. Passing: the frozen 14, r1-crlf-trailer, r7-dotdot-inside-lane.
- Per-wave artifacts: `falsify/DiffAltImpl/per-wave-differential-run1.tsv` (56 rows); JSON outputs in `/tmp/diffalt-r20/run1/`.
- Edge artifacts: `falsify/DiffAltImpl/edge-fixtures-differential.tsv` (51 fixture rows plus 3 robustness rows and depth probes); fixture trees in `/tmp/diffalt-r20/fx/<case>/`; outputs `/tmp/diffalt-r20/fxout/`.
- No production or alt file was edited. Scratch lives under `/tmp/diffalt-r20/` and `falsify/DiffAltImpl/` (TSV only).

## 9. Suggested routing for L1 (detection only; no edits made)

1. P1, P2, P3: resolve roots with `os.path.realpath` before lstat, and validate `--fleet-root` as an existing directory (exit 2 otherwise). Add C06, C07, C08 as production selftest cases.
2. P4: make `_dispatch_files` iterative. Add a deep-tree selftest case.
3. A1 and S2: keep the production missing-taskCall rule. If the alt is kept as an oracle, port R1-R6 and the missing-taskCall rule to it.
4. S1: count skipped symlinks (`symlink_skipped`) and fail closed when any exists under `.ufo/waves`.
5. S3: exclude or label `falsify/` and other seat scratch subtrees in the live census, or state in the knowledge note that they count.
