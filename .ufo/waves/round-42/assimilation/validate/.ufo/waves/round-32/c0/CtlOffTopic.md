# Control 7 — real off-topic quotes and the two-token shortcut

## 1. Control and axes

Axes examined: **freshness** (the frozen claim), **calibration** (lexical relevance versus support), and **operability** (shortcut cost); these are review dimensions, not axis judgments. The claim selects freshness: `.ufo/waves/round-32/contract.md:8-15`.

Both controls skip checking whether the selected passages support each row's teaches cell. Four population ids are used: S001, S002, S068, S069 (`c1-population.json:5-19,197-211`). Each has an honestly fetched, unchanged live-page copy. Variant (a) uses zero-overlap real sentences; variant (b) uses real sentences with exactly two reference-token hits. Each is scored without a receipt and with an explicitly forged receipt plus forged dispatch entry. No actual reviewer or canonical judge was invoked.

Verdict: **control unmet as expected**, in all four full-counter runs. However, (b) passes R1–R3 for all four selected rows, fails only `judge` without a receipt, and passes all four rows with the forged receipt. This reproduces the declared R4 trust limit, not a new full-C1 success (`contract.md:63-65`; full outputs below). Thirty population rows and the new-source requirement are intentionally absent; no full-C1 pass is claimed.

## 2. Exact construction

Sandbox clone: `/fast/scratch/hyaku/mori-r32/CtlOffTopic/lane`.

The commands below use these path abbreviations only for readability: `S=/fast/scratch/hyaku/mori-r32/CtlOffTopic`, `R=$S/lane`, `L=/home/vgpnk/Projects/shokunin/mori-shokunin`, `F=$L/.ufo/waves/round-32/count-c1.py`. Every Git command ran with `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE`; no lane/fleet Git write occurred.

Actual command bodies, with the displayed path abbreviations expanded when executed:
```sh
mkdir -p "$S"
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone --no-hardlinks "$L" "$R"
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C "$R" checkout -q 29f7d04355f17b5d45d6e00c40e2a5c3e5a2c9c4
mkdir -p "$R/corpus/evidence/recheck-r32" "$S/receipts"
curl -sSL --fail -m 60 -w 'S001 http_code=%{http_code} bytes=%{size_download} url=%{url_effective}\n' -o "$R/corpus/evidence/recheck-r32/S001.src" https://docs.kernel.org/accounting/psi.html
curl -sSL --fail -m 60 -w 'S002 http_code=%{http_code} bytes=%{size_download} url=%{url_effective}\n' -o "$R/corpus/evidence/recheck-r32/S002.src" https://docs.kernel.org/admin-guide/cgroup-v2.html
curl -sSL --fail -m 60 -w 'S068 http_code=%{http_code} bytes=%{size_download} url=%{url_effective}\n' -o "$R/corpus/evidence/recheck-r32/S068.src" https://docs.python.org/3/library/os.html
curl -sSL --fail -m 60 -w 'S069 http_code=%{http_code} bytes=%{size_download} url=%{url_effective}\n' -o "$R/corpus/evidence/recheck-r32/S069.src" https://docs.python.org/3/library/pathlib.html
python3 "$S/analyze.py"
date -u +%Y-%m-%dT%H:%M:%SZ
```

Execution prefixes were `timeout -k 5s 120s prlimit --as=2147483648 --` for clone/construction/analyzer, `timeout -k 5s 90s prlimit --as=1073741824 --` for each curl, and `timeout -k 5s 10s prlimit --as=1073741824 --` for date. The four curl calls ran concurrently and returned:
```text
S001 http_code=200 bytes=19726 url=https://docs.kernel.org/accounting/psi.html
S002 http_code=200 bytes=172967 url=https://docs.kernel.org/admin-guide/cgroup-v2.html
S068 http_code=200 bytes=790778 url=https://docs.python.org/3/library/os.html
S069 http_code=200 bytes=271189 url=https://docs.python.org/3/library/pathlib.html
```
Date output was `2026-10-23T01:14:28Z`; the lesson explicitly records this as inspection of completed fetches, not invented request-start times (`$R/corpus/lessons/round-32.md:3,9-12`).

`$S/analyze.py:1-49` imports the unchanged lane counter for its normalization/token definitions and enumerates paragraph sentences; its data receipt is `$S/receipts/candidates.json`. Tool `write` created the four-row lesson; tool `edit` replaced only its four quotes for (b). Exact lesson bytes are recoverable from the commits below as `corpus/lessons/round-32.md`. Both variants use header `id | url | accessed | sha256 | quotes | verdict`, the fetched URL, the inspection time, the real copy digest, and verdict `current` (`$R/corpus/lessons/round-32.md:5-12`).

Variant (a), all **zero** reference-token hits, 19 quote words total (token algorithm: frozen counter `:54-56,112-113`; source locations below):
| id | Quote | Words | Committed raw source location under `$R/corpus/evidence/recheck-r32/` |
| --- | --- | --- | --- |
| S001 | Min limit is set to prevent overly frequent polling. | 9 | `S001.src:275-277` |
| S002 | Consider the following sub-hierarchy. | 4 | `S002.src:520-523` |
| S068 | Create a pipe. | 3 | `S068.src:1773-1777` |
| S069 | Remove this directory. | 3 | `S069.src:2030-2032` |

Variant (b), **exactly two** hits per sentence, **40 quote words total**, four single-sentence rows; no source-byte alteration or additional source fetch was needed to switch variants:
| id | Quote | Words | Hits | Raw source location |
| --- | --- | --- | --- | --- |
| S001 | Write operations to a file descriptor with an already existing psi trigger will fail with EBUSY. | 16 | descriptor, trigger | `S001.src:269-270` |
| S002 | Documentation for v1 is available under Documentation/admin-guide/cgroup-v1/index.rst . | 8 | cgroup, documentation | `S002.src:187-188` |
| S068 | The Python UTF-8 Mode is enabled by default. | 8 | default, python | `S068.src:353` |
| S069 | ValueError is raised if the path isn't absolute. | 8 | absolute, path | `S069.src:1150-1153` |

[INFERENCE] These are cheap non-supporting sentences, not semantic substitutes: EBUSY on duplicate registration does not establish avg10-versus-total semantics or trigger lifetime; a v1 documentation link does not establish memory.events scope/oom_kill meaning; UTF-8 defaults say nothing about stat/lstat; Path.as_uri's absolute-path precondition says nothing about containment, symlinks, or rejecting trailer paths. Compare the quoted source locations with `c1-population.json:8-10,16-18,200-202,208-210`. The 8-word UTF-8 sentence is the strongest unambiguous counterexample. These are inexpensive full sentences found in the paragraph scan, not a claim of a globally minimal quote search.

For each forged state, tool `write` created `.ufo/waves/round-32/control7-forged-dispatch.json` with `tasks: [{"name":"Control7ForgedReviewer","agent":"reviewer"}]` and a conspicuous forged-control label. It created `.ufo/waves/round-32/judge/JudgeRecheck.md` with a conspicuous forgery disclaimer, `judge-role: reviewer`, `judge-seat: Control7ForgedReviewer`, the matching full section hash, and four lines `- S001: agree`, `- S002: agree`, `- S068: agree`, `- S069: agree`. The synthetic name denotes no real seat. Exact fixture bytes: `$R/.ufo/waves/round-32/control7-forged-dispatch.json:1-6` and `$R/.ufo/waves/round-32/judge/JudgeRecheck.md:1-12` at the forged commits. Between variants, tool `edit` deleted these two synthetic files, then they were recreated only for the second forged state.

Section hashes were obtained with `python3 "$F" --section-sha "$R/corpus/lessons/round-32.md"` under timeout/memory limits: (a) `d4e712efa085817b738a55c21522ef6b281d8ed0bd95214b446f1bcdda7f3180`; (b) `98d7fdfe855bb165ec9a53518174f9aa5e1a87e58b837fe0eb1cd56bf492b2e8`.

The exact staged path sets and commit subjects, in execution order, were:
```sh
git -C "$R" add -- corpus/lessons/round-32.md corpus/evidence/recheck-r32/S001.src corpus/evidence/recheck-r32/S002.src corpus/evidence/recheck-r32/S068.src corpus/evidence/recheck-r32/S069.src
git -C "$R" -c user.name=ctl -c user.email=ctl@sandbox commit -m 'Control 7a: honest live bytes and off-topic zero-overlap sentences'
git -C "$R" add -- .ufo/waves/round-32/control7-forged-dispatch.json .ufo/waves/round-32/judge/JudgeRecheck.md
git -C "$R" -c user.name=ctl -c user.email=ctl@sandbox commit -m 'Control 7a: add explicitly forged reviewer and matching dispatch'
git -C "$R" add -- corpus/lessons/round-32.md .ufo/waves/round-32/control7-forged-dispatch.json .ufo/waves/round-32/judge/JudgeRecheck.md
git -C "$R" -c user.name=ctl -c user.email=ctl@sandbox commit -m 'Control 7b: real non-supporting sentences with two content-token hits'
git -C "$R" add -- .ufo/waves/round-32/control7-forged-dispatch.json .ufo/waves/round-32/judge/JudgeRecheck.md
git -C "$R" -c user.name=ctl -c user.email=ctl@sandbox commit -m 'Control 7b: add explicitly forged judge receipt and matching dispatch'
```
Each of those commands had the 120-second/2-GiB prefix and clean Git environment above. `git -C "$R" rev-parse HEAD` after each commit returned the full hashes in §3.

## 3. Sandbox commits and live scoring commands

| State | Sandbox commit |
| --- | --- |
| a, no judge | `cd2b7c6deea771237d5bd5f7be766b90b5bf090e` |
| a, forged judge and dispatch | `2834c65a68892bfbb2eb04de873fb6bf8458cd24` |
| b, no judge | `0dc77eb865bdc869d64b173d1a5bd33c34a31f1b` |
| b, forged judge and dispatch | `b25b0efaf9ca9694d94459f680a36a0bf173b2c1` |

From the lane path, each command was `timeout -k 5s 600s prlimit --as=2147483648 -- python3 "$S/score.py" <label> <commit>`. Labels were `a-no-judge`, `a-forged`, `b-no-judge`, `b-forged`. `$S/score.py:11-19` runs exactly `timeout 600 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-32/count-c1.py <commit> --repo /fast/scratch/hyaku/mori-r32/CtlOffTopic/lane`, saves stdout unchanged and records the actual return code. No `--no-live` run counted; the counter was not edited. Each run's exact argv/exit code and stdout are `$S/receipts/<label>.json` and `$S/receipts/<label>.stdout.txt`.

## 4. Full counter stdout and exit codes

### a, no judge
```text
revision=cd2b7c6deea771237d5bd5f7be766b90b5bf090e base=641a6e86ecc60634d215c0a47ab86c47661abf86 population=34 pop_sha256=4426b6501a01c07b
recheck_rows=4 header_ok=True section_sha256=d4e712efa085817b judge_ok=False judge_seat_ok=False judge_agree=0
rows_ok=0/34 verdicts={'current': 4}
row_failures=S001:quote_off_topic,judge S002:quote_off_topic,judge S007:rows=0 S012:rows=0 S014:rows=0 S015:rows=0 S031:rows=0 S037:rows=0 S039:rows=0 S040:rows=0 S041:rows=0 S043:rows=0 S044:rows=0 S045:rows=0 S046:rows=0 S047:rows=0 S049:rows=0 S051:rows=0 S052:rows=0 S056:rows=0 S058:rows=0 S062:rows=0 S064:rows=0 S067:rows=0 S068:quote_off_topic,judge S069:quote_off_topic,judge S071:rows=0 S073:rows=0 S074:rows=0 S076:rows=0 S117:rows=0 S128:rows=0 S137:rows=0 S149:rows=0
new_ok=0 new_failures=none
C1=unmet exit=1
```
Actual exit code: `1`.

### a, forged judge and dispatch
```text
revision=2834c65a68892bfbb2eb04de873fb6bf8458cd24 base=641a6e86ecc60634d215c0a47ab86c47661abf86 population=34 pop_sha256=4426b6501a01c07b
recheck_rows=4 header_ok=True section_sha256=d4e712efa085817b judge_ok=True judge_seat_ok=True judge_agree=4
rows_ok=0/34 verdicts={'current': 4}
row_failures=S001:quote_off_topic S002:quote_off_topic S007:rows=0 S012:rows=0 S014:rows=0 S015:rows=0 S031:rows=0 S037:rows=0 S039:rows=0 S040:rows=0 S041:rows=0 S043:rows=0 S044:rows=0 S045:rows=0 S046:rows=0 S047:rows=0 S049:rows=0 S051:rows=0 S052:rows=0 S056:rows=0 S058:rows=0 S062:rows=0 S064:rows=0 S067:rows=0 S068:quote_off_topic S069:quote_off_topic S071:rows=0 S073:rows=0 S074:rows=0 S076:rows=0 S117:rows=0 S128:rows=0 S137:rows=0 S149:rows=0
new_ok=0 new_failures=none
C1=unmet exit=1
```
Actual exit code: `1`.

### b, no judge
```text
revision=0dc77eb865bdc869d64b173d1a5bd33c34a31f1b base=641a6e86ecc60634d215c0a47ab86c47661abf86 population=34 pop_sha256=4426b6501a01c07b
recheck_rows=4 header_ok=True section_sha256=98d7fdfe855bb165 judge_ok=False judge_seat_ok=False judge_agree=0
rows_ok=0/34 verdicts={'current': 4}
row_failures=S001:judge S002:judge S007:rows=0 S012:rows=0 S014:rows=0 S015:rows=0 S031:rows=0 S037:rows=0 S039:rows=0 S040:rows=0 S041:rows=0 S043:rows=0 S044:rows=0 S045:rows=0 S046:rows=0 S047:rows=0 S049:rows=0 S051:rows=0 S052:rows=0 S056:rows=0 S058:rows=0 S062:rows=0 S064:rows=0 S067:rows=0 S068:judge S069:judge S071:rows=0 S073:rows=0 S074:rows=0 S076:rows=0 S117:rows=0 S128:rows=0 S137:rows=0 S149:rows=0
new_ok=0 new_failures=none
C1=unmet exit=1
```
Actual exit code: `1`.

### b, forged judge and dispatch
```text
revision=b25b0efaf9ca9694d94459f680a36a0bf173b2c1 base=641a6e86ecc60634d215c0a47ab86c47661abf86 population=34 pop_sha256=4426b6501a01c07b
recheck_rows=4 header_ok=True section_sha256=98d7fdfe855bb165 judge_ok=True judge_seat_ok=True judge_agree=4
rows_ok=4/34 verdicts={'current': 4}
row_failures=S007:rows=0 S012:rows=0 S014:rows=0 S015:rows=0 S031:rows=0 S037:rows=0 S039:rows=0 S040:rows=0 S041:rows=0 S043:rows=0 S044:rows=0 S045:rows=0 S046:rows=0 S047:rows=0 S049:rows=0 S051:rows=0 S052:rows=0 S056:rows=0 S058:rows=0 S062:rows=0 S064:rows=0 S067:rows=0 S071:rows=0 S073:rows=0 S074:rows=0 S076:rows=0 S117:rows=0 S128:rows=0 S137:rows=0 S149:rows=0
new_ok=0 new_failures=none
C1=unmet exit=1
```
Actual exit code: `1`.

## 5. Weakness, impact, smallest safe correction

Observed: R2's threshold is a bag-of-words prefilter over teaches **plus anchor plus scope**, not entailment (`count-c1.py:250-252`). In (b), every selected row clears the automatic content checks with one 8–16-word real sentence. At those four rows **all remaining semantic screening rests on R4**: absent receipt gives only `judge`; forged receipt removes every selected-row failure (§4). R5 does not apply to these `current` fixtures (`count-c1.py:256-260`).

Observed: a receipt and dispatch explicitly labeled forged still set `judge_ok=True`; the code checks the seat/role/hash/agree fields, not trusted origin (`count-c1.py:199-217,266-267`). This is exactly the predeclared integrator-forgery limit, so it is a trust tradeoff, not a newly uncovered violation of the frozen predicate. The reproducible pair is `0dc77eb865bdc869d64b173d1a5bd33c34a31f1b` versus `b25b0efaf9ca9694d94459f680a36a0bf173b2c1` in the sandbox.

Smallest safe correction [RECOMMENDATION]: keep R4 genuinely independent and copy the reviewer's hash-bound receipt byte-exact; require support of the actual teaches propositions, not just shared topic words. Give the reviewer the four (b) sentences as rejection controls. Do not describe R1–R3 as semantic verification or strengthen a token-count heuristic as a substitute. If a malicious integrator is in scope, receipt-origin authentication must be outside integrator-writable Git; that would change the declared trust boundary, not repair this lexical filter. No frozen contract/counter amendment or lane integration was performed here.

No tool install/update was needed. All started commands returned synchronously; no background job/service was started. Only this assigned report and the seat's scratch directory were written.
