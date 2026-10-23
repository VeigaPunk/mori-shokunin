# AttackCopies — round 32 residual R1

Seat: `MoriR32A2.AttackCopies`. Examined revision: `837b2802c60a6e37a9d462f2354107307fba6ef1`.
Axes: committed-byte integrity, fetched-page completeness, live-byte reproducibility, live-quote retention, isolated restoration.
This is detection evidence, not a C1 judgment or integration decision.

## Evidence and commands

All scratch paths below are under `/fast/scratch/hyaku/mori-r32/MoriR32A2.AttackCopies/`:
- **A** = `audit-output.txt`; **J** = `audit-results.json`; **S** = `summary-output.txt`.
- **C** = `counter-no-live.txt`; **M** = `mutation-output.txt`.
- Line references such as A:4 resolve to the named scratch path above.
- Auditor: `audit_copies.py` (historical blobs read with `git show REV:path`; counter functions imported from the committed counter copy).
- Audit command: `timeout --kill-after=3 115 prlimit --as=2147483648 -- env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE TMPDIR=/fast/scratch/hyaku/mori-r32/MoriR32A2.AttackCopies/tmp PYTHONDONTWRITEBYTECODE=1 python3 /fast/scratch/hyaku/mori-r32/MoriR32A2.AttackCopies/audit_copies.py`.
- Each distinct non-API population URL received one `curl -sSL --fail -m 60` operation, with write-out metadata only; redirects followed, no retries. All recorded starts: `2026-10-23T01:42:22Z` (A:37-95).
- Frozen counter SHA256: `cfa0b988a51fc59720382016c0608408c022b9aaedc19f92c24453493d1a84fe`; invoked lane bytes equal the committed copy (S:5-6).

## Results

**33/33 copy SHA256 values match their committed table rows; all 33 pass the requested structural completeness checks** (A:2,4-36).
There are 30 HTML copies ending in `</html>` after trailing whitespace, one PDF ending in `%%EOF`, and two JSON copies parsed successfully (S:1,4).
Those are structural checks, not a claim that a terminator alone proves every upstream section or API pagination was captured.
All copy quotes occur in frozen-counter-normalised copy text (A:4-36).

**27 distinct non-API URL operations: 26 HTTP 200 successes, one HTTP 403; zero API operations** (A:3,37-95).
The successes cover 31 population rows: 26 byte-equal, five byte-different; all 85 quoted passages occur in live normalised text (S:2-3).
S117 and S137 were not fetched, as instructed; their committed JSON copies parse, with 29 and 30 top-level items respectively (S:4).

### Every committed copy

Every SHA256 below was recomputed and equals the row's SHA256. `G`, `R`, `C` identify difference explanations below.
`Live quotes` is matched/total for that row, not a semantic-support judgment. API rows have copy checks only.

| id | Recomputed SHA256 (= row) | Complete format | Live bytes | Live quotes | Evidence |
|---|---|---|---|---|---|
| S001 | f752c8d5447760a315048037eb8f53007f8e4862d58617264f587cccd8798258 | HTML | equal | 3/3 | A:4,37-38 |
| S002 | b478c1bae99899df476d6b4989cbb516f7ca93c5f009cdff64b802bbc24f3d4b | HTML | equal | 3/3 | A:5,39-40 |
| S007 | 56460ffb24d7ea3ccd771b7f834a460786b646038411c0744b981ad532af6f0a | HTML | equal | 3/3 | A:6,41-42 |
| S012 | a51157e7c5de1389832e31abe2064c786f971ba1ade9d25e0945b2fc56898052 | HTML | differs G | 2/2 | A:7,43-44 |
| S014 | 75440570fb1f71859229ca88fed0a6764b2057c7dd90651701b3d022a5649722 | HTML | equal | 3/3 | A:8,45-46 |
| S015 | 906e5d34b38913ddaf729f74f468f5511f8a143bb3f86f0fdda06957af7bf5e7 | HTML | equal | 3/3 | A:9,47-48 |
| S031 | 22809fe16836722f0359b10b59b4c0971cf3edf6ffb26528c41bd1a383f2a58e | HTML | equal | 2/2 | A:10,50-51 |
| S037 | 906e5d34b38913ddaf729f74f468f5511f8a143bb3f86f0fdda06957af7bf5e7 | HTML | equal | 3/3 | A:11,47,49 |
| S039 | b13d9928c1ea07a6a75dfe80d2227405c1f3ea6ac5b708219bef44fe15f6cd7b | HTML | equal | 2/2 | A:12,52-53 |
| S040 | 5ada44c28aa31dc7495276e2bf6a11a3370e33ae71277051736641882e5e9980 | HTML | equal | 3/3 | A:13,54-55 |
| S041 | 3924746f977d3bd8b086fe275ccd67dc344271753e355cc9eaa9d7e698f0886b | HTML | differs R | 3/3 | A:14,56-57 |
| S043 | 4a6ac09770cabd93d0e16a65bfc23669e85b019c23e28ddb74ea33e88d82feb4 | HTML | equal | 3/3 | A:15,58-59 |
| S044 | db9c9a760810386858e6b1bad4a7a334c56bd48c77692dbc1c343657ae0ca254 | HTML | equal | 3/3 | A:16,60-61 |
| S045 | 5df178565d444fbc99dc4459cdd7c80ac09b67069eb7b22405d3a45c053089ef | HTML | equal | 2/2 | A:17,62-63 |
| S046 | 0dc2f88a4935851e824b3d35c8236d7d4ad4603554b2ff24cc25ec83962868f3 | HTML | equal | 3/3 | A:18,64-65 |
| S047 | 0d2ea49c643107a5fbb4c74f944114c48fe13152158b8255ceb4e71bea20791c | HTML | equal | 2/2 | A:19,66-67 |
| S049 | 604378c015d263638d7fd3c066762e7da7ed104be7fa974223f085b5bf330bb9 | HTML | equal | 3/3 | A:20,68-69 |
| S051 | 555b9df82af12de4ca887efc21c0a9e159a14485d5d570f44b32ef15c6c62470 | PDF | equal | 3/3 | A:21,70-71 |
| S052 | 6104b09c73e65514ed10d7eea302bcdaed88fa12982cd77e5b3049d0df949f80 | HTML | equal | 3/3 | A:22,72-73 |
| S058 | 6eca09d9ef21dd4270ff2c73cac7ee26964aebc470f4dfc52705eb27749ce65f | HTML | equal | 3/3 | A:23,76-77 |
| S062 | 4dd9f775b3e6b5977df3e43c56c4e7530be988f9bf8fc0d5b5be202aafae76c9 | HTML | differs R | 3/3 | A:24,78-79 |
| S064 | 64c603545b3f9799cc9525228ba70cf80444a063b32a4be37de2a5ca09b83421 | HTML | equal | 3/3 | A:25,80-81 |
| S067 | 5d706e27809602eeeb566fd8baf0a569d7f42adc985f9d4f13a18b4dae70de16 | HTML | differs C | 2/2 | A:26,82-83 |
| S068 | 2ac87dd3ac1f30a3210cb1631c5bd41f3708f100cbeeb2b5874ea4b29e17d993 | HTML | equal | 3/3 | A:27,85-86 |
| S069 | a5cfbc6b1fc4d570c434f1b737547ea87a3f964dd79b15e42ff01627b6fe85f0 | HTML | equal | 3/3 | A:28,87-88 |
| S071 | 96ad0ef9661c7a3fff3b360ce9643a6c1bc120bcec52b82385c94481194581cb | HTML | equal | 2/2 | A:29,90-91 |
| S073 | a5cfbc6b1fc4d570c434f1b737547ea87a3f964dd79b15e42ff01627b6fe85f0 | HTML | equal | 3/3 | A:30,87,89 |
| S074 | 96ad0ef9661c7a3fff3b360ce9643a6c1bc120bcec52b82385c94481194581cb | HTML | equal | 3/3 | A:31,90,92 |
| S076 | 5d706e27809602eeeb566fd8baf0a569d7f42adc985f9d4f13a18b4dae70de16 | HTML | differs C | 2/2 | A:32,82,84 |
| S117 | 423c43617a2a299315180292f43447936f6ddde01efff5baece3fc46ed8b1869 | JSON | API skipped | unrun | A:33; S:4 |
| S128 | 769edf3b9c054934db07f16173297fc5fd63c3a4c807682355f08fa45cde80a9 | HTML | equal | 3/3 | A:34,93-94 |
| S137 | b658df9d6c52fd46c43db155022dd22c75e46fdd0abb86323ebcfc5c208bf775 | JSON | API skipped | unrun | A:35; S:4 |
| S149 | 769edf3b9c054934db07f16173297fc5fd63c3a4c807682355f08fa45cde80a9 | HTML | equal | 3/3 | A:36,93,95 |

### Why live bytes differ

- **G / S012:** request-specific GitHub metadata (`fetch-nonce`, `html-safe-nonce`, request/visitor metadata) and generated button/tooltip/dialog identifiers differ; normalised text is identical. Changed blocks are at copy/live lines 114,120,294,297,443,1231-1314; attribute names, not token values, were retained (A:44; J, S012 `diff_blocks`). Live SHA256: `28ae2829c884be8f47f6a95601cd70cd7ea79e21ae280bfe51d427a07c2fe867` (A:43).
- **C / S067,S076:** the differing lines are CSRF metadata and hidden `authenticity_token` fields at 84,249,419; normalised text is identical (A:82-84). Live SHA256: `c5084db25d28f65e8c239582181e3364bc3b38fd15315f014211c35833d691d8` (A:82).
- **R / S041:** one redirect to `https://www.rfc-editor.org/info/rfc6585/`; bytes differ at HTML lines 1,118,698, covering the metadata, Nuxt-rendered body and footer/hydration blocks. Normalised text also differs, although all three quotes remain present. Live SHA256: `4f236a46c6379ffbde1c30c72f828fb4c8192fcec51ec46a79eed57d7a236cba` (A:56-57).
- **R / S062:** one redirect to `https://www.rfc-editor.org/info/rfc8785/`; bytes differ at HTML lines 1,124,1696 in analogous metadata, Nuxt body and footer/hydration blocks. Normalised text also differs; all three quotes remain present. Live SHA256: `4fff20a81088aa91d118406a71a4bc1cb64eb61e9ef9477f78167bcd7aca4311` (A:78-79).
- **RFC limitation:** the retained evidence records differing blocks/attribute names and normalised hashes, not their exact changed values. [INFERENCE] request-dependent rendering may explain those differences; this probe does **not** establish that they are solely tokens or that every unquoted sentence is unchanged. No second fetch was made to resolve that uncertainty (J, S041/S062 `diff_blocks`, `normalised_equal`, normalised hashes).

## S056 transcript and one fresh plain curl

The committed transcript is copied unchanged at `committed/corpus/evidence/recheck-r32/S056.fetch.txt` in scratch.
Its lines 7-9 record three separate failed tries, each `exit=22 http=403 bytes=0`; lines 11-13 record three additional failed tries.
Its lines 19-23 record the earlier Cloudflare challenge response. No `.src` is claimed for this unreachable row (`committed/corpus/lessons/round-32.md:40`).

The one fresh curl operation used the population URL `https://www.pnas.org/doi/10.1073/pnas.1708274114` with ordinary `curl -sSL --fail -m 60` plus write-out fields. Output (A:74-75):

```text
exit=22 http=403 bytes=0 redirects=0 final=https://www.pnas.org/doi/10.1073/pnas.1708274114
curl: (22) The requested URL returned error: 403
```

No challenge bypass was attempted. This independently confirms the 403, not the truth of historical network events beyond what the transcript records.

## Frozen counter — one requested --no-live run

Command: `timeout --kill-after=3 300 prlimit --as=2147483648 -- env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE TMPDIR=/fast/scratch/hyaku/mori-r32/MoriR32A2.AttackCopies/tmp PYTHONDONTWRITEBYTECODE=1 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-32/count-c1.py 837b2802c60a6e37a9d462f2354107307fba6ef1 --no-live`.
Actual output, exit **1** (C:1-6):

```text
revision=837b2802c60a6e37a9d462f2354107307fba6ef1 base=641a6e86ecc60634d215c0a47ab86c47661abf86 population=34 pop_sha256=4426b6501a01c07b
recheck_rows=34 header_ok=True section_sha256=251bf664717bbdf4 judge_ok=False judge_seat_ok=False judge_agree=0
rows_ok=0/34 verdicts={'current': 33, 'unreachable': 1}
row_failures=S001:judge S002:judge S007:judge S012:judge S014:judge S015:judge S031:judge S037:judge S039:judge S040:judge S041:judge S043:judge S044:judge S045:judge S046:judge S047:judge S049:judge S051:judge S052:judge S056:judge S058:judge S062:judge S064:judge S067:judge S068:judge S069:judge S071:judge S073:judge S074:judge S076:judge S117:judge S128:judge S137:judge S149:judge
new_ok=3 new_failures=none
C1=diagnostic exit=1 (live check R3 skipped)
```

Every reported row failure is `judge`. This is a diagnostic failure at the requested revision, **not** C1=met; live R3 is skipped. It is not used as a mutation kill (C:2-6).

## One isolated mutation probe

Mutant: remove only the final `>` byte from scratch `copies/S001.src:381` (`</html>` becomes `</html`), simulating a truncated transfer while retaining every quote.
Expected detector: `detect_copy.py` checks the frozen row's SHA256, HTML terminator and all frozen-counter-normalised quotes. The same bounded command ran on pristine, mutated and restored bytes:
`timeout --kill-after=3 30 prlimit --as=1073741824 -- python3 /fast/scratch/hyaku/mori-r32/MoriR32A2.AttackCopies/detect_copy.py /fast/scratch/hyaku/mori-r32/MoriR32A2.AttackCopies/copies/S001.src` (clean Git environment and scratch TMPDIR).
Actual outputs (M:1-11):

```text
phase=pristine detector_exit=0
id=S001 bytes=19726 sha256=f752c8d5447760a315048037eb8f53007f8e4862d58617264f587cccd8798258 row_sha_ok=True html_complete=True quotes=[True, True, True]
COPY_CHECK=pass
phase=mutated detector_exit=1
id=S001 bytes=19725 sha256=2864ddac46613e1d91b488f8c3f11a9d815f50cc88f909943a3c08f691fee690 row_sha_ok=False html_complete=False quotes=[True, True, True]
COPY_CHECK=fail
phase=restored detector_exit=0
id=S001 bytes=19726 sha256=f752c8d5447760a315048037eb8f53007f8e4862d58617264f587cccd8798258 row_sha_ok=True html_complete=True quotes=[True, True, True]
COPY_CHECK=pass
restoration_exact=True
verdict=killed
```

**Verdict: killed by the copy detector**, with a passing pristine baseline and exact byte-for-byte restoration. Quote presence alone would not have noticed this truncation; SHA256 and HTML closure both do (M:1-11). No mutant was applied to the lane, and no counter contract was changed.

## Bounds and handoff

No tools installed or updated. No API fetches, git/jj writes, subagents, background jobs, runtime launches, host-service operations or out-of-scope source edits. Every child command used timeout and a memory limit; every command returned and no started job remains. Only this report and own scratch artifacts were written. The integrator must not read the requested counter's diagnostic exit as an acceptance pass; API live checks remain intentionally unrun, and RFC byte-difference causes remain bounded as above.
