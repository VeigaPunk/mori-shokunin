# C0 — CtlCounterMutants
Axes: check sensitivity, failure isolation, live reproducibility, exact restoration (`/fast/scratch/hyaku/mori-r32/CtlCounterMutants/probe.py:4-6`).
Verdict: **control unmet as expected; all 10 mutants killed by the appropriate row/new-source metric**. No original or mutant printed C1=met; these intentionally omit 33 population rows (full outputs below; receipts cited in table).
Sandbox: `/fast/scratch/hyaku/mori-r32/CtlCounterMutants/lane`; freeze `29f7d04355f17b5d45d6e00c40e2a5c3e5a2c9c4`; base `641a6e86ecc60634d215c0a47ab86c47661abf86` (`.ufo/waves/round-32/contract.md:3-5`; output below).
## Exact construction and detector
`timeout 120 prlimit --as=2147483648 -- sh -c 'mkdir -p /fast/scratch/hyaku/mori-r32/CtlCounterMutants && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone --no-hardlinks /home/vgpnk/Projects/shokunin/mori-shokunin /fast/scratch/hyaku/mori-r32/CtlCounterMutants/lane && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/mori-r32/CtlCounterMutants/lane checkout -q 29f7d04355f17b5d45d6e00c40e2a5c3e5a2c9c4'` → exit 0.
`cp /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-32/count-c1.py /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-32/c1-population.json /fast/scratch/hyaku/mori-r32/CtlCounterMutants/`; repeat both copies beside each `mutants/<name>/count-c1.py` (the bounded setup command exited 0).
`curl -sSL --fail -m 60 https://docs.kernel.org/admin-guide/cgroup-v2.html -o /fast/scratch/hyaku/mori-r32/CtlCounterMutants/cgroup-v2.html` → exit 0, SHA256 `b478c1bae99899df476d6b4989cbb516f7ca93c5f009cdff64b802bbc24f3d4b`; ordinary public fetch only.
Exact per-control copy/add/commit commands plus outputs: `/fast/scratch/hyaku/mori-r32/CtlCounterMutants/construction.txt:1-177`; fixture bytes: `/fast/scratch/hyaku/mori-r32/CtlCounterMutants/controls/<name>/round-32.md:1-9` and `JudgeRecheck.md:1-7`. Synthetic judge/dispatch fixtures are not real reviewer decisions (`controls/dispatch.json:1-9` under the same scratch root).
Each scratch mutant removes only the named clause at the frozen counter line(s) in the table; SHA-format/existence checks and accessed syntax remain. The live mutant removes the current/drifted re-fetch branch, not the separate unreachable branch. Retained mutant bytes: `/fast/scratch/hyaku/mori-r32/CtlCounterMutants/mutants/<name>/count-c1.mutant.py`.
Executed each probe as `timeout 120 prlimit --as=2147483648 -- python3 /fast/scratch/hyaku/mori-r32/CtlCounterMutants/probe.py <name>`. Every counter invocation is `timeout 600 prlimit --as=2147483648 -- python3 <counter> <commit> --repo /fast/scratch/hyaku/mori-r32/CtlCounterMutants/lane`, cwd the lane, GIT_DIR/GIT_WORK_TREE/GIT_INDEX_FILE unset; original uses the frozen lane counter, mutant/restored use the scratch path (`probe.py:18-24,39-46,61-74` under the scratch root). No --no-live runs.
Positive fixture commit `92ff30561a9ba800faf778a7b3808a3d040af3cf` scored with the frozen lane counter: `rows_ok=1/34`, `new_ok=0`, `C1=unmet exit=1`, process exit 1; only 33 absent rows failed. Its source quote is the live oom_kill sentence (`https://docs.kernel.org/admin-guide/cgroup-v2.html`; `/fast/scratch/hyaku/mori-r32/CtlCounterMutants/cgroup-v2.html:1409-1410`).
## Mutant → killing control
O/M/R mean original/mutated/restored. Every receipt is `/fast/scratch/hyaku/mori-r32/CtlCounterMutants/receipt-<name>.json:1-38`; it contains the exact command, stdout, exit status and hashes. Original check lines refer to `.ufo/waves/round-32/count-c1.py`.
| Mutant / check | Killing control (work skipped) | Sandbox commit | rows_ok O/M/R | new_ok O/M/R | Verdict | Mutant SHA256 |
|---|---|---|---|---|---|---|
| url / R1:233-234 | Wrong row URL; live fetch still uses frozen S002 URL | `757f49a7fd08b139b842cc1aeac062dfe3825929` | 0/1/0 of 34 | 0/0/0 | killed | `23b78b12b83bff95fdd26bf61a2d23a50c01cecf6a9b7f68bb05d07420926052` |
| accessed_floor / R1:235 | Access time 2026-10-23T00:59:59Z; valid syntax, one second below floor | `7aa67c9b75fabd038374a2f346694b7493230c6a` | 0/1/0 of 34 | 0/0/0 | killed | `f2a7906d2b432dcb3c857e3de8b5efeedf2764c040cf29af018e7135ede03b55` |
| copy_sha / R2:242 | Correct fetched copy; row SHA is 64 zeroes | `a11917100281d15c95b3c2464cd50a3c1af566dd` | 0/1/0 of 34 | 0/0/0 | killed | `c40a1a40b0f546ad840ffcd4775fe361b5aafcbd7e7c98d0f19f487c64a58751` |
| quote_in_copy / R2:248-249 | Empty committed copy with its correct SHA; real live quote | `611c8b2eea939a9069dc58b84e0a5fca1b7433d1` | 0/1/0 of 34 | 0/0/0 | killed | `dcc1c0a51557cef6a02d8feaf99e5e048ad0e33eafa7a50b0a1c6563c76ae1aa` |
| topic_token / R2:250-252 | Real introductory quote with only documentation overlapping topic tokens | `97a6388386fec981219194b8a68102d4687f1bea` | 0/1/0 of 34 | 0/0/0 | killed | `d7b94f076ef30359d53f931e6ab2f83c349a5f37d3364fb3f39550f6c323e8bb` |
| live_refetch / R3:253-255 | Fabricated on-topic sentence in matching copy, absent from live page | `0d832cc7e0dc3d869227dba47a6876d3f57adb3c` | 0/1/0 of 34 | 0/0/0 | killed | `8f62364d1058fa5c279f29c9b1b4905ecc10c707594eac72b06a58f9a5c56eb1` |
| judge_sha / R4:216 | Syntactically valid judge SHA is 64 zeroes | `8168578d25e277fc74f662b7df948a042946d7d2` | 0/1/0 of 34 | 0/0/0 | killed | `f6c16889cebd3fea89861ad20bef0d532bf6d73ca1ce765b8ae82a444c09fee6` |
| judge_agree / R4:266 | Matching judge section SHA, but no S002 agree line | `303a9b14dd33c66abddc5b26f3219c86f4fa32a6` | 0/1/0 of 34 | 0/0/0 | killed | `11d6eddc88cefcceb417f350c22dc733bd6b76bc8f26f97c62191db8fe002c3b` |
| r5 / R5:256-260 | S002 drifted, with no added correction in any of its three knowledge paths | `6cc286aa4a23ca5eb166c41e1fef168974e0ceec` | 0/1/0 of 34 | 0/0/0 | killed | `7c91ec52bb022ccbc2f96bb6dd26d1c5560f93452e93250e62dc00347cdad140` |
| url_novelty / new:292 | S175 reuses the exact base S002 URL; Gate, copy and README otherwise valid | `d1f79e61dddb38aa40e491e3786b373583e724f4` | 1/1/1 of 34 | 0/1/0 | killed | `4ce7c0ca84b218d7e200286d25e9037bb30f03f21f26dbaccc71fe307fa73730` |
## Restoration and interpretation
All 10 tested counter paths began pristine and were restored byte-exact to SHA256 `cfa0b988a51fc59720382016c0608408c022b9aaedc19f92c24453493d1a84fe`; the lane counter had that same hash before/after every probe. All ten population copies remained SHA256 `4426b6501a01c07bdb3347c712c5e858447be47204fa9017c02ab6113e83e178` (each `receipt-<name>.json:5-8,25-27`).
All restored stdout, stderr, exit codes and counts exactly matched original observations (`receipt-<name>.json:28-37`). Restored full stdout/exit codes are preserved verbatim in `/fast/scratch/hyaku/mori-r32/CtlCounterMutants/stdout-<name>.txt:21-27`; no baseline anomaly, survivor or inconclusive result occurred.
No tested check is dead weight under these controls. **Rows-only is a metric hole for new-source novelty**, not a counter hole: novelty runs after rows_ok accumulation and changes new_ok only (`.ufo/waves/round-32/count-c1.py:271-293,315-323`; `receipt-url_novelty.json:14-23`). An exit-code-only detector would miss all ten mutations because the other 33 rows remain absent. These are row-level kills, not whole-predicate kills.
No counter weakness was demonstrated by this assigned probe; no lane counter edit or lane Git write was made. All probe commands returned in the foreground; none started a background job (`probe.py:30-32,39-41,48-100`; receipts above). No tools were installed or updated; versions observed: Python 3.14.8, Git 2.56.0, curl 8.23.0, timeout 9.12, prlimit 2.42.4 (`python3 --version; git --version; curl --version; timeout --version; prlimit --version` output).
## Positive fixture full stdout; actual process exit_code=1
```text
revision=92ff30561a9ba800faf778a7b3808a3d040af3cf base=641a6e86ecc60634d215c0a47ab86c47661abf86 population=34 pop_sha256=4426b6501a01c07b
recheck_rows=1 header_ok=True section_sha256=1c7d45c767e9799c judge_ok=True judge_seat_ok=True judge_agree=1
rows_ok=1/34 verdicts={'current': 1}
row_failures=S001:rows=0 S007:rows=0 S012:rows=0 S014:rows=0 S015:rows=0 S031:rows=0 S037:rows=0 S039:rows=0 S040:rows=0 S041:rows=0 S043:rows=0 S044:rows=0 S045:rows=0 S046:rows=0 S047:rows=0 S049:rows=0 S051:rows=0 S052:rows=0 S056:rows=0 S058:rows=0 S062:rows=0 S064:rows=0 S067:rows=0 S068:rows=0 S069:rows=0 S071:rows=0 S073:rows=0 S074:rows=0 S076:rows=0 S117:rows=0 S128:rows=0 S137:rows=0 S149:rows=0
new_ok=0 new_failures=none
C1=unmet exit=1
```
## Full original and mutant stdout, with actual process exit codes
```text
=== url original; exit_code=1 ===
revision=757f49a7fd08b139b842cc1aeac062dfe3825929 base=641a6e86ecc60634d215c0a47ab86c47661abf86 population=34 pop_sha256=4426b6501a01c07b
recheck_rows=1 header_ok=True section_sha256=b75970163ab5ae9e judge_ok=True judge_seat_ok=True judge_agree=1
rows_ok=0/34 verdicts={'current': 1}
row_failures=S001:rows=0 S002:url S007:rows=0 S012:rows=0 S014:rows=0 S015:rows=0 S031:rows=0 S037:rows=0 S039:rows=0 S040:rows=0 S041:rows=0 S043:rows=0 S044:rows=0 S045:rows=0 S046:rows=0 S047:rows=0 S049:rows=0 S051:rows=0 S052:rows=0 S056:rows=0 S058:rows=0 S062:rows=0 S064:rows=0 S067:rows=0 S068:rows=0 S069:rows=0 S071:rows=0 S073:rows=0 S074:rows=0 S076:rows=0 S117:rows=0 S128:rows=0 S137:rows=0 S149:rows=0
new_ok=0 new_failures=none
C1=unmet exit=1
=== url mutated; exit_code=1 ===
revision=757f49a7fd08b139b842cc1aeac062dfe3825929 base=641a6e86ecc60634d215c0a47ab86c47661abf86 population=34 pop_sha256=4426b6501a01c07b
recheck_rows=1 header_ok=True section_sha256=b75970163ab5ae9e judge_ok=True judge_seat_ok=True judge_agree=1
rows_ok=1/34 verdicts={'current': 1}
row_failures=S001:rows=0 S007:rows=0 S012:rows=0 S014:rows=0 S015:rows=0 S031:rows=0 S037:rows=0 S039:rows=0 S040:rows=0 S041:rows=0 S043:rows=0 S044:rows=0 S045:rows=0 S046:rows=0 S047:rows=0 S049:rows=0 S051:rows=0 S052:rows=0 S056:rows=0 S058:rows=0 S062:rows=0 S064:rows=0 S067:rows=0 S068:rows=0 S069:rows=0 S071:rows=0 S073:rows=0 S074:rows=0 S076:rows=0 S117:rows=0 S128:rows=0 S137:rows=0 S149:rows=0
new_ok=0 new_failures=none
C1=unmet exit=1
=== accessed_floor original; exit_code=1 ===
revision=7aa67c9b75fabd038374a2f346694b7493230c6a base=641a6e86ecc60634d215c0a47ab86c47661abf86 population=34 pop_sha256=4426b6501a01c07b
recheck_rows=1 header_ok=True section_sha256=4a26e545cf342bfb judge_ok=True judge_seat_ok=True judge_agree=1
rows_ok=0/34 verdicts={'current': 1}
row_failures=S001:rows=0 S002:accessed S007:rows=0 S012:rows=0 S014:rows=0 S015:rows=0 S031:rows=0 S037:rows=0 S039:rows=0 S040:rows=0 S041:rows=0 S043:rows=0 S044:rows=0 S045:rows=0 S046:rows=0 S047:rows=0 S049:rows=0 S051:rows=0 S052:rows=0 S056:rows=0 S058:rows=0 S062:rows=0 S064:rows=0 S067:rows=0 S068:rows=0 S069:rows=0 S071:rows=0 S073:rows=0 S074:rows=0 S076:rows=0 S117:rows=0 S128:rows=0 S137:rows=0 S149:rows=0
new_ok=0 new_failures=none
C1=unmet exit=1
=== accessed_floor mutated; exit_code=1 ===
revision=7aa67c9b75fabd038374a2f346694b7493230c6a base=641a6e86ecc60634d215c0a47ab86c47661abf86 population=34 pop_sha256=4426b6501a01c07b
recheck_rows=1 header_ok=True section_sha256=4a26e545cf342bfb judge_ok=True judge_seat_ok=True judge_agree=1
rows_ok=1/34 verdicts={'current': 1}
row_failures=S001:rows=0 S007:rows=0 S012:rows=0 S014:rows=0 S015:rows=0 S031:rows=0 S037:rows=0 S039:rows=0 S040:rows=0 S041:rows=0 S043:rows=0 S044:rows=0 S045:rows=0 S046:rows=0 S047:rows=0 S049:rows=0 S051:rows=0 S052:rows=0 S056:rows=0 S058:rows=0 S062:rows=0 S064:rows=0 S067:rows=0 S068:rows=0 S069:rows=0 S071:rows=0 S073:rows=0 S074:rows=0 S076:rows=0 S117:rows=0 S128:rows=0 S137:rows=0 S149:rows=0
new_ok=0 new_failures=none
C1=unmet exit=1
=== copy_sha original; exit_code=1 ===
revision=a11917100281d15c95b3c2464cd50a3c1af566dd base=641a6e86ecc60634d215c0a47ab86c47661abf86 population=34 pop_sha256=4426b6501a01c07b
recheck_rows=1 header_ok=True section_sha256=c033e1275b940b63 judge_ok=True judge_seat_ok=True judge_agree=1
rows_ok=0/34 verdicts={'current': 1}
row_failures=S001:rows=0 S002:copy_sha S007:rows=0 S012:rows=0 S014:rows=0 S015:rows=0 S031:rows=0 S037:rows=0 S039:rows=0 S040:rows=0 S041:rows=0 S043:rows=0 S044:rows=0 S045:rows=0 S046:rows=0 S047:rows=0 S049:rows=0 S051:rows=0 S052:rows=0 S056:rows=0 S058:rows=0 S062:rows=0 S064:rows=0 S067:rows=0 S068:rows=0 S069:rows=0 S071:rows=0 S073:rows=0 S074:rows=0 S076:rows=0 S117:rows=0 S128:rows=0 S137:rows=0 S149:rows=0
new_ok=0 new_failures=none
C1=unmet exit=1
=== copy_sha mutated; exit_code=1 ===
revision=a11917100281d15c95b3c2464cd50a3c1af566dd base=641a6e86ecc60634d215c0a47ab86c47661abf86 population=34 pop_sha256=4426b6501a01c07b
recheck_rows=1 header_ok=True section_sha256=c033e1275b940b63 judge_ok=True judge_seat_ok=True judge_agree=1
rows_ok=1/34 verdicts={'current': 1}
row_failures=S001:rows=0 S007:rows=0 S012:rows=0 S014:rows=0 S015:rows=0 S031:rows=0 S037:rows=0 S039:rows=0 S040:rows=0 S041:rows=0 S043:rows=0 S044:rows=0 S045:rows=0 S046:rows=0 S047:rows=0 S049:rows=0 S051:rows=0 S052:rows=0 S056:rows=0 S058:rows=0 S062:rows=0 S064:rows=0 S067:rows=0 S068:rows=0 S069:rows=0 S071:rows=0 S073:rows=0 S074:rows=0 S076:rows=0 S117:rows=0 S128:rows=0 S137:rows=0 S149:rows=0
new_ok=0 new_failures=none
C1=unmet exit=1
=== quote_in_copy original; exit_code=1 ===
revision=611c8b2eea939a9069dc58b84e0a5fca1b7433d1 base=641a6e86ecc60634d215c0a47ab86c47661abf86 population=34 pop_sha256=4426b6501a01c07b
recheck_rows=1 header_ok=True section_sha256=f1794d8b509dcfa1 judge_ok=True judge_seat_ok=True judge_agree=1
rows_ok=0/34 verdicts={'current': 1}
row_failures=S001:rows=0 S002:quote_not_in_copy S007:rows=0 S012:rows=0 S014:rows=0 S015:rows=0 S031:rows=0 S037:rows=0 S039:rows=0 S040:rows=0 S041:rows=0 S043:rows=0 S044:rows=0 S045:rows=0 S046:rows=0 S047:rows=0 S049:rows=0 S051:rows=0 S052:rows=0 S056:rows=0 S058:rows=0 S062:rows=0 S064:rows=0 S067:rows=0 S068:rows=0 S069:rows=0 S071:rows=0 S073:rows=0 S074:rows=0 S076:rows=0 S117:rows=0 S128:rows=0 S137:rows=0 S149:rows=0
new_ok=0 new_failures=none
C1=unmet exit=1
=== quote_in_copy mutated; exit_code=1 ===
revision=611c8b2eea939a9069dc58b84e0a5fca1b7433d1 base=641a6e86ecc60634d215c0a47ab86c47661abf86 population=34 pop_sha256=4426b6501a01c07b
recheck_rows=1 header_ok=True section_sha256=f1794d8b509dcfa1 judge_ok=True judge_seat_ok=True judge_agree=1
rows_ok=1/34 verdicts={'current': 1}
row_failures=S001:rows=0 S007:rows=0 S012:rows=0 S014:rows=0 S015:rows=0 S031:rows=0 S037:rows=0 S039:rows=0 S040:rows=0 S041:rows=0 S043:rows=0 S044:rows=0 S045:rows=0 S046:rows=0 S047:rows=0 S049:rows=0 S051:rows=0 S052:rows=0 S056:rows=0 S058:rows=0 S062:rows=0 S064:rows=0 S067:rows=0 S068:rows=0 S069:rows=0 S071:rows=0 S073:rows=0 S074:rows=0 S076:rows=0 S117:rows=0 S128:rows=0 S137:rows=0 S149:rows=0
new_ok=0 new_failures=none
C1=unmet exit=1
=== topic_token original; exit_code=1 ===
revision=97a6388386fec981219194b8a68102d4687f1bea base=641a6e86ecc60634d215c0a47ab86c47661abf86 population=34 pop_sha256=4426b6501a01c07b
recheck_rows=1 header_ok=True section_sha256=a06709274dba0c4a judge_ok=True judge_seat_ok=True judge_agree=1
rows_ok=0/34 verdicts={'current': 1}
row_failures=S001:rows=0 S002:quote_off_topic S007:rows=0 S012:rows=0 S014:rows=0 S015:rows=0 S031:rows=0 S037:rows=0 S039:rows=0 S040:rows=0 S041:rows=0 S043:rows=0 S044:rows=0 S045:rows=0 S046:rows=0 S047:rows=0 S049:rows=0 S051:rows=0 S052:rows=0 S056:rows=0 S058:rows=0 S062:rows=0 S064:rows=0 S067:rows=0 S068:rows=0 S069:rows=0 S071:rows=0 S073:rows=0 S074:rows=0 S076:rows=0 S117:rows=0 S128:rows=0 S137:rows=0 S149:rows=0
new_ok=0 new_failures=none
C1=unmet exit=1
=== topic_token mutated; exit_code=1 ===
revision=97a6388386fec981219194b8a68102d4687f1bea base=641a6e86ecc60634d215c0a47ab86c47661abf86 population=34 pop_sha256=4426b6501a01c07b
recheck_rows=1 header_ok=True section_sha256=a06709274dba0c4a judge_ok=True judge_seat_ok=True judge_agree=1
rows_ok=1/34 verdicts={'current': 1}
row_failures=S001:rows=0 S007:rows=0 S012:rows=0 S014:rows=0 S015:rows=0 S031:rows=0 S037:rows=0 S039:rows=0 S040:rows=0 S041:rows=0 S043:rows=0 S044:rows=0 S045:rows=0 S046:rows=0 S047:rows=0 S049:rows=0 S051:rows=0 S052:rows=0 S056:rows=0 S058:rows=0 S062:rows=0 S064:rows=0 S067:rows=0 S068:rows=0 S069:rows=0 S071:rows=0 S073:rows=0 S074:rows=0 S076:rows=0 S117:rows=0 S128:rows=0 S137:rows=0 S149:rows=0
new_ok=0 new_failures=none
C1=unmet exit=1
=== live_refetch original; exit_code=1 ===
revision=0d832cc7e0dc3d869227dba47a6876d3f57adb3c base=641a6e86ecc60634d215c0a47ab86c47661abf86 population=34 pop_sha256=4426b6501a01c07b
recheck_rows=1 header_ok=True section_sha256=558637dcd96c3a2f judge_ok=True judge_seat_ok=True judge_agree=1
rows_ok=0/34 verdicts={'current': 1}
row_failures=S001:rows=0 S002:live_quote S007:rows=0 S012:rows=0 S014:rows=0 S015:rows=0 S031:rows=0 S037:rows=0 S039:rows=0 S040:rows=0 S041:rows=0 S043:rows=0 S044:rows=0 S045:rows=0 S046:rows=0 S047:rows=0 S049:rows=0 S051:rows=0 S052:rows=0 S056:rows=0 S058:rows=0 S062:rows=0 S064:rows=0 S067:rows=0 S068:rows=0 S069:rows=0 S071:rows=0 S073:rows=0 S074:rows=0 S076:rows=0 S117:rows=0 S128:rows=0 S137:rows=0 S149:rows=0
new_ok=0 new_failures=none
C1=unmet exit=1
=== live_refetch mutated; exit_code=1 ===
revision=0d832cc7e0dc3d869227dba47a6876d3f57adb3c base=641a6e86ecc60634d215c0a47ab86c47661abf86 population=34 pop_sha256=4426b6501a01c07b
recheck_rows=1 header_ok=True section_sha256=558637dcd96c3a2f judge_ok=True judge_seat_ok=True judge_agree=1
rows_ok=1/34 verdicts={'current': 1}
row_failures=S001:rows=0 S007:rows=0 S012:rows=0 S014:rows=0 S015:rows=0 S031:rows=0 S037:rows=0 S039:rows=0 S040:rows=0 S041:rows=0 S043:rows=0 S044:rows=0 S045:rows=0 S046:rows=0 S047:rows=0 S049:rows=0 S051:rows=0 S052:rows=0 S056:rows=0 S058:rows=0 S062:rows=0 S064:rows=0 S067:rows=0 S068:rows=0 S069:rows=0 S071:rows=0 S073:rows=0 S074:rows=0 S076:rows=0 S117:rows=0 S128:rows=0 S137:rows=0 S149:rows=0
new_ok=0 new_failures=none
C1=unmet exit=1
=== judge_sha original; exit_code=1 ===
revision=8168578d25e277fc74f662b7df948a042946d7d2 base=641a6e86ecc60634d215c0a47ab86c47661abf86 population=34 pop_sha256=4426b6501a01c07b
recheck_rows=1 header_ok=True section_sha256=1c7d45c767e9799c judge_ok=False judge_seat_ok=True judge_agree=1
rows_ok=0/34 verdicts={'current': 1}
row_failures=S001:rows=0 S002:judge S007:rows=0 S012:rows=0 S014:rows=0 S015:rows=0 S031:rows=0 S037:rows=0 S039:rows=0 S040:rows=0 S041:rows=0 S043:rows=0 S044:rows=0 S045:rows=0 S046:rows=0 S047:rows=0 S049:rows=0 S051:rows=0 S052:rows=0 S056:rows=0 S058:rows=0 S062:rows=0 S064:rows=0 S067:rows=0 S068:rows=0 S069:rows=0 S071:rows=0 S073:rows=0 S074:rows=0 S076:rows=0 S117:rows=0 S128:rows=0 S137:rows=0 S149:rows=0
new_ok=0 new_failures=none
C1=unmet exit=1
=== judge_sha mutated; exit_code=1 ===
revision=8168578d25e277fc74f662b7df948a042946d7d2 base=641a6e86ecc60634d215c0a47ab86c47661abf86 population=34 pop_sha256=4426b6501a01c07b
recheck_rows=1 header_ok=True section_sha256=1c7d45c767e9799c judge_ok=True judge_seat_ok=True judge_agree=1
rows_ok=1/34 verdicts={'current': 1}
row_failures=S001:rows=0 S007:rows=0 S012:rows=0 S014:rows=0 S015:rows=0 S031:rows=0 S037:rows=0 S039:rows=0 S040:rows=0 S041:rows=0 S043:rows=0 S044:rows=0 S045:rows=0 S046:rows=0 S047:rows=0 S049:rows=0 S051:rows=0 S052:rows=0 S056:rows=0 S058:rows=0 S062:rows=0 S064:rows=0 S067:rows=0 S068:rows=0 S069:rows=0 S071:rows=0 S073:rows=0 S074:rows=0 S076:rows=0 S117:rows=0 S128:rows=0 S137:rows=0 S149:rows=0
new_ok=0 new_failures=none
C1=unmet exit=1
=== judge_agree original; exit_code=1 ===
revision=303a9b14dd33c66abddc5b26f3219c86f4fa32a6 base=641a6e86ecc60634d215c0a47ab86c47661abf86 population=34 pop_sha256=4426b6501a01c07b
recheck_rows=1 header_ok=True section_sha256=1c7d45c767e9799c judge_ok=True judge_seat_ok=True judge_agree=0
rows_ok=0/34 verdicts={'current': 1}
row_failures=S001:rows=0 S002:judge S007:rows=0 S012:rows=0 S014:rows=0 S015:rows=0 S031:rows=0 S037:rows=0 S039:rows=0 S040:rows=0 S041:rows=0 S043:rows=0 S044:rows=0 S045:rows=0 S046:rows=0 S047:rows=0 S049:rows=0 S051:rows=0 S052:rows=0 S056:rows=0 S058:rows=0 S062:rows=0 S064:rows=0 S067:rows=0 S068:rows=0 S069:rows=0 S071:rows=0 S073:rows=0 S074:rows=0 S076:rows=0 S117:rows=0 S128:rows=0 S137:rows=0 S149:rows=0
new_ok=0 new_failures=none
C1=unmet exit=1
=== judge_agree mutated; exit_code=1 ===
revision=303a9b14dd33c66abddc5b26f3219c86f4fa32a6 base=641a6e86ecc60634d215c0a47ab86c47661abf86 population=34 pop_sha256=4426b6501a01c07b
recheck_rows=1 header_ok=True section_sha256=1c7d45c767e9799c judge_ok=True judge_seat_ok=True judge_agree=0
rows_ok=1/34 verdicts={'current': 1}
row_failures=S001:rows=0 S007:rows=0 S012:rows=0 S014:rows=0 S015:rows=0 S031:rows=0 S037:rows=0 S039:rows=0 S040:rows=0 S041:rows=0 S043:rows=0 S044:rows=0 S045:rows=0 S046:rows=0 S047:rows=0 S049:rows=0 S051:rows=0 S052:rows=0 S056:rows=0 S058:rows=0 S062:rows=0 S064:rows=0 S067:rows=0 S068:rows=0 S069:rows=0 S071:rows=0 S073:rows=0 S074:rows=0 S076:rows=0 S117:rows=0 S128:rows=0 S137:rows=0 S149:rows=0
new_ok=0 new_failures=none
C1=unmet exit=1
=== r5 original; exit_code=1 ===
revision=6cc286aa4a23ca5eb166c41e1fef168974e0ceec base=641a6e86ecc60634d215c0a47ab86c47661abf86 population=34 pop_sha256=4426b6501a01c07b
recheck_rows=1 header_ok=True section_sha256=1a81f58dde53d23b judge_ok=True judge_seat_ok=True judge_agree=1
rows_ok=0/34 verdicts={'drifted': 1}
row_failures=S001:rows=0 S002:no_correction:corpus/knowledge/oom-kill-counter-kernel-only-r12.md,no_correction:corpus/knowledge/userspace-oom-killers-r12.md,no_correction:corpus/knowledge/journal-alarm-routing-r14.md S007:rows=0 S012:rows=0 S014:rows=0 S015:rows=0 S031:rows=0 S037:rows=0 S039:rows=0 S040:rows=0 S041:rows=0 S043:rows=0 S044:rows=0 S045:rows=0 S046:rows=0 S047:rows=0 S049:rows=0 S051:rows=0 S052:rows=0 S056:rows=0 S058:rows=0 S062:rows=0 S064:rows=0 S067:rows=0 S068:rows=0 S069:rows=0 S071:rows=0 S073:rows=0 S074:rows=0 S076:rows=0 S117:rows=0 S128:rows=0 S137:rows=0 S149:rows=0
new_ok=0 new_failures=none
C1=unmet exit=1
=== r5 mutated; exit_code=1 ===
revision=6cc286aa4a23ca5eb166c41e1fef168974e0ceec base=641a6e86ecc60634d215c0a47ab86c47661abf86 population=34 pop_sha256=4426b6501a01c07b
recheck_rows=1 header_ok=True section_sha256=1a81f58dde53d23b judge_ok=True judge_seat_ok=True judge_agree=1
rows_ok=1/34 verdicts={'drifted': 1}
row_failures=S001:rows=0 S007:rows=0 S012:rows=0 S014:rows=0 S015:rows=0 S031:rows=0 S037:rows=0 S039:rows=0 S040:rows=0 S041:rows=0 S043:rows=0 S044:rows=0 S045:rows=0 S046:rows=0 S047:rows=0 S049:rows=0 S051:rows=0 S052:rows=0 S056:rows=0 S058:rows=0 S062:rows=0 S064:rows=0 S067:rows=0 S068:rows=0 S069:rows=0 S071:rows=0 S073:rows=0 S074:rows=0 S076:rows=0 S117:rows=0 S128:rows=0 S137:rows=0 S149:rows=0
new_ok=0 new_failures=none
C1=unmet exit=1
=== url_novelty original; exit_code=1 ===
revision=d1f79e61dddb38aa40e491e3786b373583e724f4 base=641a6e86ecc60634d215c0a47ab86c47661abf86 population=34 pop_sha256=4426b6501a01c07b
recheck_rows=1 header_ok=True section_sha256=1c7d45c767e9799c judge_ok=True judge_seat_ok=True judge_agree=1
rows_ok=1/34 verdicts={'current': 1}
row_failures=S001:rows=0 S007:rows=0 S012:rows=0 S014:rows=0 S015:rows=0 S031:rows=0 S037:rows=0 S039:rows=0 S040:rows=0 S041:rows=0 S043:rows=0 S044:rows=0 S045:rows=0 S046:rows=0 S047:rows=0 S049:rows=0 S051:rows=0 S052:rows=0 S056:rows=0 S058:rows=0 S062:rows=0 S064:rows=0 S067:rows=0 S068:rows=0 S069:rows=0 S071:rows=0 S073:rows=0 S074:rows=0 S076:rows=0 S117:rows=0 S128:rows=0 S137:rows=0 S149:rows=0
new_ok=0 new_failures=S175:url_not_new
C1=unmet exit=1
=== url_novelty mutated; exit_code=1 ===
revision=d1f79e61dddb38aa40e491e3786b373583e724f4 base=641a6e86ecc60634d215c0a47ab86c47661abf86 population=34 pop_sha256=4426b6501a01c07b
recheck_rows=1 header_ok=True section_sha256=1c7d45c767e9799c judge_ok=True judge_seat_ok=True judge_agree=1
rows_ok=1/34 verdicts={'current': 1}
row_failures=S001:rows=0 S007:rows=0 S012:rows=0 S014:rows=0 S015:rows=0 S031:rows=0 S037:rows=0 S039:rows=0 S040:rows=0 S041:rows=0 S043:rows=0 S044:rows=0 S045:rows=0 S046:rows=0 S047:rows=0 S049:rows=0 S051:rows=0 S052:rows=0 S056:rows=0 S058:rows=0 S062:rows=0 S064:rows=0 S067:rows=0 S068:rows=0 S069:rows=0 S071:rows=0 S073:rows=0 S074:rows=0 S076:rows=0 S117:rows=0 S128:rows=0 S137:rows=0 S149:rows=0
new_ok=1 new_failures=none
C1=unmet exit=1
```
