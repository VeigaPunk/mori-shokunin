# CtlLocatorStale — bounded mutation controls

Axes: evidence addressability, copy integrity, cited-span binding, and exact restoration. Findings only; no admission judgement.

Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin`.
Clone: `/fast/scratch/hyaku/mori-r33/CtlLocatorStale/repo`.
Counter: Lane `.ufo/waves/round-33/count-c1-a1.py` (sha256 `9ec4d87c4eee79b2ef27b60f3f2b7ae73ee8d5bf2d3f2a73b19526b04145eda6`).

## Setup and detector

Created the isolated clone with `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone --no-hardlinks --no-checkout <Lane> <Clone>`, then checked out `62db24c01d5b7c2247f43852ea2b28d0ae5e40c8` detached. Both commands exited 0 under `timeout 120 prlimit --as=1073741824 --`.
Added and committed only a synthetic receipt and dispatch before the baseline. Clone `.ufo/waves/round-33/judge/JudgeC1Rows.md:5` quotes R-J verbatim, `:7` binds the entry hash, and `:9-22` marks all 14 rows supported with located spans; `dispatch.json:3` quotes R-J verbatim. These are deliberately fabricated controls, not genuine judge receipts. The named residual is contract.md:73-75,130-134.

Every scoring invocation used this same command, with Git override variables removed and `PYTHONDONTWRITEBYTECODE=1`:
```sh
timeout --kill-after=5 590 prlimit --as=1073741824 -- timeout 900 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-33/count-c1-a1.py HEAD --repo /fast/scratch/hyaku/mori-r33/CtlLocatorStale/repo
```
The outer timeout enforces the binding process limit; the requested inner scoring command is unchanged. Every invocation completed within two seconds; stderr was empty. All three listed perturbations were independent, with restoration and a passing detector between them.

| State | Expected detector | Actual | Verdict |
|---|---|---|---|
| Synthetic baseline | met, exit 0 | met, exit 0 | Positive control; declared forged-receipt residual reproduced |
| M1: one impossible Gate locator | Reject invalid evidence address | met, exit 0 | Survived; locator-address coverage residual |
| M2: append to committed copy, leave Gate hash unchanged | unmet, sources, exit 1 | unmet, sources, exit 1 | Killed |
| M3: cite a copy lacking the receipt span, keep judged hash correct | unmet, judge, exit 1 | unmet, judge, exit 1 | Killed |

## Actual output: synthetic baseline

```text
rev=36a750c9ba81e3b41ef7121c3edebf2a0ac9ab8f repo=/fast/scratch/hyaku/mori-r33/CtlLocatorStale/repo
entry=present entry_sha256=8e04b9efc391d5c5e1764e796f6731e59cb12a758bd652bf822cb715891b8d15 head_lines=yes html_comments=0
tables=1 decision_tables=1 unfenced_decision_tables=1
rows=14 rows_ok=14 distinct_rows=14 distinct_observations=14 short_readings=0
new_id_rows=14 new_ids=11 (S180,S181,S182,S183,S184,S185,S186,S187,S188,S189,S190)
S180 gate=ok quotes=4 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/block/stat.rst
S181 gate=ok quotes=4 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/admin-guide/iostats.rst
S182 gate=ok quotes=4 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/block/genhd.c
S183 gate=ok quotes=2 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/include/linux/part_stat.h
S184 gate=ok quotes=3 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/block/blk-core.c
S185 gate=ok quotes=2 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/block/blk-mq.c
S186 gate=ok quotes=3 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/include/linux/blk_types.h
S187 gate=ok quotes=4 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/ABI/testing/procfs-diskstats
S188 gate=ok quotes=3 copy=ok fetch=ok url=https://github.com/torvalds/linux/commit/b6866318657717c8914673a6394894d12bc9ff5e.patch
S189 gate=ok quotes=2 copy=ok fetch=ok url=https://github.com/torvalds/linux/commit/bdca3c87fb7ad1cc61d231d37eb0d8f90d001e0c.patch
S190 gate=ok quotes=3 copy=ok fetch=ok url=https://raw.githubusercontent.com/sysstat/sysstat/v12.8.0/iostat.c
gates_ok=11/11 copies_ok=11/11 fetch_ok=11/11 distinct_sources=yes
rows_without_quote_overlap=0
readings_copying_quotes=0
dispatch_rule=yes receipt_rule=yes judged_sha=ok covered=yes supported=14 supported_new=14 spans_bad=[] unsupported=[]
skill_rows=5
C1=met
```
Exit 0.

## Actual output: M1 impossible locator

Only Clone `corpus/lessons/round-33.md:15` changed: the first `S180.src:21-22` became `S180.src:999999`. Quotes, copies, hashes, entry, dispatch and receipt stayed unchanged.
```text
rev=5c524030d1e4113b698631816f02609c63d9c261 repo=/fast/scratch/hyaku/mori-r33/CtlLocatorStale/repo
entry=present entry_sha256=8e04b9efc391d5c5e1764e796f6731e59cb12a758bd652bf822cb715891b8d15 head_lines=yes html_comments=0
tables=1 decision_tables=1 unfenced_decision_tables=1
rows=14 rows_ok=14 distinct_rows=14 distinct_observations=14 short_readings=0
new_id_rows=14 new_ids=11 (S180,S181,S182,S183,S184,S185,S186,S187,S188,S189,S190)
S180 gate=ok quotes=4 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/block/stat.rst
S181 gate=ok quotes=4 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/admin-guide/iostats.rst
S182 gate=ok quotes=4 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/block/genhd.c
S183 gate=ok quotes=2 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/include/linux/part_stat.h
S184 gate=ok quotes=3 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/block/blk-core.c
S185 gate=ok quotes=2 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/block/blk-mq.c
S186 gate=ok quotes=3 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/include/linux/blk_types.h
S187 gate=ok quotes=4 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/ABI/testing/procfs-diskstats
S188 gate=ok quotes=3 copy=ok fetch=ok url=https://github.com/torvalds/linux/commit/b6866318657717c8914673a6394894d12bc9ff5e.patch
S189 gate=ok quotes=2 copy=ok fetch=ok url=https://github.com/torvalds/linux/commit/bdca3c87fb7ad1cc61d231d37eb0d8f90d001e0c.patch
S190 gate=ok quotes=3 copy=ok fetch=ok url=https://raw.githubusercontent.com/sysstat/sysstat/v12.8.0/iostat.c
gates_ok=11/11 copies_ok=11/11 fetch_ok=11/11 distinct_sources=yes
rows_without_quote_overlap=0
readings_copying_quotes=0
dispatch_rule=yes receipt_rule=yes judged_sha=ok covered=yes supported=14 supported_new=14 spans_bad=[] unsupported=[]
skill_rows=5
C1=met
```
Exit 0; survived. Severity: **minor**, a counter residual rather than a demonstrated bad locator in current lane data. Attack: lesson `:15`; implementation: counter `:59,223-242`. Its regex checks locator shape but captures only quote text; matching then searches the entire committed copy, not the addressed lines. `timeout 120 prlimit --as=1073741824 -- wc -l <Clone>/corpus/evidence/sources-r33/S180.src` returned `103 <path>`, so line 999999 cannot exist. The frozen predicate requires locator syntax and quote presence (contract.md:32-35); this probe does not establish a frozen-predicate miss. Do not equate passing this counter with re-locating evidence.

## Actual output: M2 stale copy hash

Only Clone `corpus/evidence/sources-r33/S180.src:104` changed: appended `CtlLocatorStale appended mutation line.` after the receipt commit, without changing the Gate sha or receipt.
```text
rev=320b793a93d7c4f1c184f510f983a6c817580cf6 repo=/fast/scratch/hyaku/mori-r33/CtlLocatorStale/repo
entry=present entry_sha256=8e04b9efc391d5c5e1764e796f6731e59cb12a758bd652bf822cb715891b8d15 head_lines=yes html_comments=0
tables=1 decision_tables=1 unfenced_decision_tables=1
rows=14 rows_ok=14 distinct_rows=14 distinct_observations=14 short_readings=0
new_id_rows=14 new_ids=11 (S180,S181,S182,S183,S184,S185,S186,S187,S188,S189,S190)
S180 gate=ok quotes=4 copy=bad fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/block/stat.rst
S181 gate=ok quotes=4 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/admin-guide/iostats.rst
S182 gate=ok quotes=4 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/block/genhd.c
S183 gate=ok quotes=2 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/include/linux/part_stat.h
S184 gate=ok quotes=3 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/block/blk-core.c
S185 gate=ok quotes=2 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/block/blk-mq.c
S186 gate=ok quotes=3 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/include/linux/blk_types.h
S187 gate=ok quotes=4 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/ABI/testing/procfs-diskstats
S188 gate=ok quotes=3 copy=ok fetch=ok url=https://github.com/torvalds/linux/commit/b6866318657717c8914673a6394894d12bc9ff5e.patch
S189 gate=ok quotes=2 copy=ok fetch=ok url=https://github.com/torvalds/linux/commit/bdca3c87fb7ad1cc61d231d37eb0d8f90d001e0c.patch
S190 gate=ok quotes=3 copy=ok fetch=ok url=https://raw.githubusercontent.com/sysstat/sysstat/v12.8.0/iostat.c
gates_ok=11/11 copies_ok=10/11 fetch_ok=11/11 distinct_sources=yes
rows_without_quote_overlap=0
readings_copying_quotes=0
dispatch_rule=yes receipt_rule=yes judged_sha=ok covered=yes supported=14 supported_new=14 spans_bad=[] unsupported=[]
skill_rows=5
unmet_conditions=sources
C1=unmet
```
Exit 1; killed by counter:241-258. Severity: **none**; stale copy bytes were detected even though every receipt span remained present.

## Actual output: M3 span source removed from row citations

Clone `corpus/knowledge/disk-write-rate-r33.md:19`: replaced row 1's source cell `S187, S180, S186` with `S180`. Its receipt span stayed `Each line contains the following 14 fields:`, which is in S187 but not S180. Refreshed only receipt `:7` to the new entry hash to avoid conflating this probe with stale judged-sha256. No observation, reading, verdict, source copy, Gate, span or supported verdict changed.
```text
rev=ea87640252262ab24e020bf9902f952e06a94cd8 repo=/fast/scratch/hyaku/mori-r33/CtlLocatorStale/repo
entry=present entry_sha256=a34fd510dfb4b9ff194b525f1c8babd7b607185f95b3811d1b4f38f76e450c7d head_lines=yes html_comments=0
tables=1 decision_tables=1 unfenced_decision_tables=1
rows=14 rows_ok=14 distinct_rows=14 distinct_observations=14 short_readings=0
new_id_rows=14 new_ids=10 (S180,S181,S182,S183,S184,S185,S187,S188,S189,S190)
S180 gate=ok quotes=4 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/block/stat.rst
S181 gate=ok quotes=4 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/admin-guide/iostats.rst
S182 gate=ok quotes=4 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/block/genhd.c
S183 gate=ok quotes=2 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/include/linux/part_stat.h
S184 gate=ok quotes=3 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/block/blk-core.c
S185 gate=ok quotes=2 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/block/blk-mq.c
S187 gate=ok quotes=4 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/ABI/testing/procfs-diskstats
S188 gate=ok quotes=3 copy=ok fetch=ok url=https://github.com/torvalds/linux/commit/b6866318657717c8914673a6394894d12bc9ff5e.patch
S189 gate=ok quotes=2 copy=ok fetch=ok url=https://github.com/torvalds/linux/commit/bdca3c87fb7ad1cc61d231d37eb0d8f90d001e0c.patch
S190 gate=ok quotes=3 copy=ok fetch=ok url=https://raw.githubusercontent.com/sysstat/sysstat/v12.8.0/iostat.c
gates_ok=10/10 copies_ok=10/10 fetch_ok=10/10 distinct_sources=yes
rows_without_quote_overlap=0
readings_copying_quotes=0
dispatch_rule=yes receipt_rule=yes judged_sha=ok covered=yes supported=13 supported_new=13 spans_bad=[1] unsupported=[]
skill_rows=5
unmet_conditions=judge
C1=unmet
```
Exit 1; killed by counter:299-313 despite 13 other valid supported rows. Severity: **none**. The source-count and lexical checks still passed; the failed condition was the cited-span binding.

## Hashes and exact restoration

`timeout 120 prlimit --as=1073741824 -- sha256sum <paths>` produced these SHA-256 values. Each restored value equals its before value:

| Clone file | Before and restored | Mutated |
|---|---|---|
| `corpus/lessons/round-33.md` | `d5fb45a5ce08af23356283c430293ba8c5bdcd3734c57fbbe9cfe5e49795c271` | `f4a323ef8a20780a5938ceda49770f9fb6f0c8e25d3033672b6a6c0f3201e6c2` |
| `corpus/evidence/sources-r33/S180.src` | `4c35b795a518ceefea985f11e53b51f71d58fc99bf5a0920ca3738f13c90cb2e` | `9444c630cd6f9bf07589fc2e06e50df873d63ccaa4852e9adeb2a39e7a6a690e` |
| `corpus/knowledge/disk-write-rate-r33.md` | `8e04b9efc391d5c5e1764e796f6731e59cb12a758bd652bf822cb715891b8d15` | `a34fd510dfb4b9ff194b525f1c8babd7b607185f95b3811d1b4f38f76e450c7d` |
| `.ufo/waves/round-33/judge/JudgeC1Rows.md` | `4c72308bfcdb44db8d1ae6efa91f0bd71844ebacf5aff6f98bf8b496a2ed28e6` | `282d046fa8947ea837198b8130d846dfdb19290db73d0d9faac2ca7c4c8c9f31` |

Dispatch remained `63ec542292063a1612759649679cc03be2058139c1863a088bdeeca0937a6974`; the lane counter remained the hash named above. No detector code changed.
Each restore was committed, then scored with the identical detector:

| Restore | Commit | Actual output and exit |
|---|---|---|
| M1 | `1279a18dcd1a0bb0b7d1b48bb3cd667ef5567fb4` | `C1=met`, exit 0 |
| M2 | `935d08d837867e6d0769fd6f8a09511109e9dc4a` | `C1=met`, exit 0 |
| M3 | `e134c5117d90fe99484847a3c024206e2a13b05c` | `C1=met`, exit 0 |

For every restoration, `timeout 120 prlimit --as=1073741824 -- git -C <Clone> rev-parse 'HEAD^{tree}'` returned synthetic-baseline tree `58274fce9d78cbc9edab2b3fbc7bbb1ba3df087a`. Comparing all restored stdout lines after the revision header against baseline returned `RESTORATION_OUTPUTS_EQUAL_EXCEPT_REV=True`; before/final SHA output comparison returned `BASELINE_BYTE_HASHES_EQUAL=True`. Thus all mutation points were restored exactly, including the receipt hash update; synthetic fixtures remain only in the clone.

## Handoff

Lesson-ready residual: a syntactically valid Gate locator can point past EOF while the counter reports `gate=ok` and `C1=met`; it checks whole-copy quote presence, not the locator's address. Synthetic receipt acceptance remains the separately declared integrity residual. Stale committed-copy hashes and spans found only in now-uncited copies were both caught. These controls do not adjudicate R-J support in the measured entry.
Only this report was written in the lane; no lesson, source, counter, index or lane commit was changed. No subagents, background jobs, tool installs, service actions or other runtimes were invoked. All launched scoring and Git commands completed synchronously.
