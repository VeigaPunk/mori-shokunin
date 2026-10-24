# Controls 1–3: do-nothing, junk table, all-unreachable

Axes: negative-control discrimination; frozen-detector fidelity; isolation and exact restoration.

## 1. Controls and skipped work

Sandbox: `/fast/scratch/hyaku/mori-r32/CtlDoNothingJunk/lane`. All receipts below use the frozen lane counter in live mode, never `--no-live`.

| Control | Scored commit | rows_ok | new_ok | Verdict |
| --- | --- | --- | --- | --- |
| Do-nothing base | 641a6e86ecc60634d215c0a47ab86c47661abf86 | 0/34 | 0 | control unmet as expected |
| Do-nothing freeze | 29f7d04355f17b5d45d6e00c40e2a5c3e5a2c9c4 | 0/34 | 0 | control unmet as expected |
| Junk table | f5dad76e8145c2fb8fcfe169a11c11cc3f30a476 | 0/34 | 0 | control unmet as expected |
| All-unreachable | 50ff0b9a87431617c48ce8cafa953ba3337bd93a | 0/34 | 0 | control unmet as expected |

Expected detector: P-C1 / R1–R5 / new-source check, `.ufo/waves/round-32/count-c1.py:6-30`.
Do-nothing skips all work. Junk supplies 34 correctly shaped rows but no fetched copies, genuine quotes, judge or new source. All-unreachable replaces the verdicts and supplies 34 fabricated transcripts without fetching evidence. Construction and detector outputs below are the evidence.

## 2. Exact construction

Initial commands (all exited 0):
```sh
timeout 120 prlimit --as=2147483648 -- mkdir -p /fast/scratch/hyaku/mori-r32/CtlDoNothingJunk
timeout 120 prlimit --as=2147483648 -- env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone --no-hardlinks /home/vgpnk/Projects/shokunin/mori-shokunin /fast/scratch/hyaku/mori-r32/CtlDoNothingJunk/lane
timeout 120 prlimit --as=2147483648 -- env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/mori-r32/CtlDoNothingJunk/lane checkout -q 29f7d04355f17b5d45d6e00c40e2a5c3e5a2c9c4
```
Every subsequent command used an environment with GIT_DIR, GIT_WORK_TREE and GIT_INDEX_FILE removed, and PYTHONUNBUFFERED=1. Bounded runner: `timeout --kill-after=5 <seconds> prlimit --as=2147483648 -- <argv>`; 120 seconds for Git, 600 for scoring. Both pristine scores ran concurrently; both fabricated-control scores ran concurrently and were awaited.

Exact junk-table generator executed with Python eval and `tool.write` (population is the frozen JSON's `population` array; lesson is `/fast/scratch/hyaku/mori-r32/CtlDoNothingJunk/lane/corpus/lessons/round-32.md`):
```python
junk_text = '# Round 32 negative control\n\n## Recheck\n\n| id | url | accessed | sha256 | quotes | verdict |\n| --- | --- | --- | --- | --- | --- |\n' + ''.join('| ' + p['id'] + ' | ' + p['url'] + ' | 2026-10-23T02:00:00Z | ' + '0' * 64 + ' | "Fabricated narwhals juggle violet teapots" | current |\n' for p in population)
await tool.write({'i':'Creating fabricated recheck table','path':str(lesson),'content':junk_text})
```

```sh
timeout --kill-after=5 120 prlimit --as=2147483648 -- git -C /fast/scratch/hyaku/mori-r32/CtlDoNothingJunk/lane add -- corpus/lessons/round-32.md
```
Exit code: 0.

```sh
timeout --kill-after=5 120 prlimit --as=2147483648 -- git -C /fast/scratch/hyaku/mori-r32/CtlDoNothingJunk/lane -c user.name=ctl -c user.email=ctl@sandbox commit -m 'control: fabricated round-32 recheck table'
```
Exit code: 0.

All-unreachable used `tool.edit` on lesson lines 7–40, changing only the final `current` cell to `unreachable`. No `.src` copies were created. Then:
```python
transcript_text = 'attempt 1: curl exit 22\nattempt 2: curl exit 22\nattempt 3: curl exit 22\n'
for p in population:
    await tool.write({'i':'Creating fake unreachable transcript','path':str(repo / 'corpus/evidence/recheck-r32' / (p['id'] + '.fetch.txt')),'content':transcript_text})
```

```sh
timeout --kill-after=5 120 prlimit --as=2147483648 -- git -C /fast/scratch/hyaku/mori-r32/CtlDoNothingJunk/lane add -- corpus/lessons/round-32.md corpus/evidence/recheck-r32/
```
Exit code: 0.

```sh
timeout --kill-after=5 120 prlimit --as=2147483648 -- git -C /fast/scratch/hyaku/mori-r32/CtlDoNothingJunk/lane -c user.name=ctl -c user.email=ctl@sandbox commit -m 'control: all-unreachable with fabricated fetch transcripts'
```
Exit code: 0.

```sh
timeout --kill-after=5 120 prlimit --as=2147483648 -- git -C /fast/scratch/hyaku/mori-r32/CtlDoNothingJunk/lane branch ctl-junk-table f5dad76e8145c2fb8fcfe169a11c11cc3f30a476
```
Exit code: 0.

```sh
timeout --kill-after=5 120 prlimit --as=2147483648 -- git -C /fast/scratch/hyaku/mori-r32/CtlDoNothingJunk/lane branch ctl-all-unreachable 50ff0b9a87431617c48ce8cafa953ba3337bd93a
```
Exit code: 0.

Construction receipts: `/fast/scratch/hyaku/mori-r32/CtlDoNothingJunk/construction.json`. Control files remain addressable at sandbox refs `ctl-junk-table` and `ctl-all-unreachable`; lesson rows are at `corpus/lessons/round-32.md:7-40` in each corresponding commit.

## 3. Full counter stdout and actual exit codes

### do-nothing-base

```sh
timeout --kill-after=5 600 prlimit --as=2147483648 -- python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-32/count-c1.py 641a6e86ecc60634d215c0a47ab86c47661abf86 --repo /fast/scratch/hyaku/mori-r32/CtlDoNothingJunk/lane
```
```text
revision=641a6e86ecc60634d215c0a47ab86c47661abf86 base=641a6e86ecc60634d215c0a47ab86c47661abf86 population=34 pop_sha256=4426b6501a01c07b
recheck_rows=0 header_ok=False section_sha256=e3b0c44298fc1c14 judge_ok=False judge_seat_ok=False judge_agree=0
rows_ok=0/34 verdicts={}
row_failures=S001:rows=0 S002:rows=0 S007:rows=0 S012:rows=0 S014:rows=0 S015:rows=0 S031:rows=0 S037:rows=0 S039:rows=0 S040:rows=0 S041:rows=0 S043:rows=0 S044:rows=0 S045:rows=0 S046:rows=0 S047:rows=0 S049:rows=0 S051:rows=0 S052:rows=0 S056:rows=0 S058:rows=0 S062:rows=0 S064:rows=0 S067:rows=0 S068:rows=0 S069:rows=0 S071:rows=0 S073:rows=0 S074:rows=0 S076:rows=0 S117:rows=0 S128:rows=0 S137:rows=0 S149:rows=0
new_ok=0 new_failures=none
C1=unmet exit=1
```
Exit code: 1
Stderr: empty

### do-nothing-freeze

```sh
timeout --kill-after=5 600 prlimit --as=2147483648 -- python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-32/count-c1.py 29f7d04355f17b5d45d6e00c40e2a5c3e5a2c9c4 --repo /fast/scratch/hyaku/mori-r32/CtlDoNothingJunk/lane
```
```text
revision=29f7d04355f17b5d45d6e00c40e2a5c3e5a2c9c4 base=641a6e86ecc60634d215c0a47ab86c47661abf86 population=34 pop_sha256=4426b6501a01c07b
recheck_rows=0 header_ok=False section_sha256=e3b0c44298fc1c14 judge_ok=False judge_seat_ok=False judge_agree=0
rows_ok=0/34 verdicts={}
row_failures=S001:rows=0 S002:rows=0 S007:rows=0 S012:rows=0 S014:rows=0 S015:rows=0 S031:rows=0 S037:rows=0 S039:rows=0 S040:rows=0 S041:rows=0 S043:rows=0 S044:rows=0 S045:rows=0 S046:rows=0 S047:rows=0 S049:rows=0 S051:rows=0 S052:rows=0 S056:rows=0 S058:rows=0 S062:rows=0 S064:rows=0 S067:rows=0 S068:rows=0 S069:rows=0 S071:rows=0 S073:rows=0 S074:rows=0 S076:rows=0 S117:rows=0 S128:rows=0 S137:rows=0 S149:rows=0
new_ok=0 new_failures=none
C1=unmet exit=1
```
Exit code: 1
Stderr: empty

### junk-table

```sh
timeout --kill-after=5 600 prlimit --as=2147483648 -- python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-32/count-c1.py f5dad76e8145c2fb8fcfe169a11c11cc3f30a476 --repo /fast/scratch/hyaku/mori-r32/CtlDoNothingJunk/lane
```
```text
revision=f5dad76e8145c2fb8fcfe169a11c11cc3f30a476 base=641a6e86ecc60634d215c0a47ab86c47661abf86 population=34 pop_sha256=4426b6501a01c07b
recheck_rows=34 header_ok=True section_sha256=3e823e3b2d889c84 judge_ok=False judge_seat_ok=False judge_agree=0
rows_ok=0/34 verdicts={'current': 34}
row_failures=S001:copy_sha,quote_not_in_copy,quote_off_topic,live_quote,judge S002:copy_sha,quote_not_in_copy,quote_off_topic,live_quote,judge S007:copy_sha,quote_not_in_copy,quote_off_topic,live_quote,judge S012:copy_sha,quote_not_in_copy,quote_off_topic,live_quote,judge S014:copy_sha,quote_not_in_copy,quote_off_topic,live_quote,judge S015:copy_sha,quote_not_in_copy,quote_off_topic,live_quote,judge S031:copy_sha,quote_not_in_copy,quote_off_topic,live_quote,judge S037:copy_sha,quote_not_in_copy,quote_off_topic,live_quote,judge S039:copy_sha,quote_not_in_copy,quote_off_topic,live_quote,judge S040:copy_sha,quote_not_in_copy,quote_off_topic,live_quote,judge S041:copy_sha,quote_not_in_copy,quote_off_topic,live_quote,judge S043:copy_sha,quote_not_in_copy,quote_off_topic,live_quote,judge S044:copy_sha,quote_not_in_copy,quote_off_topic,live_quote,judge S045:copy_sha,quote_not_in_copy,quote_off_topic,live_quote,judge S046:copy_sha,quote_not_in_copy,quote_off_topic,live_quote,judge S047:copy_sha,quote_not_in_copy,quote_off_topic,live_quote,judge S049:copy_sha,quote_not_in_copy,quote_off_topic,live_quote,judge S051:copy_sha,quote_not_in_copy,quote_off_topic,live_quote,judge S052:copy_sha,quote_not_in_copy,quote_off_topic,live_quote,judge S056:copy_sha,quote_not_in_copy,quote_off_topic,live_quote,judge S058:copy_sha,quote_not_in_copy,quote_off_topic,live_quote,judge S062:copy_sha,quote_not_in_copy,quote_off_topic,live_quote,judge S064:copy_sha,quote_not_in_copy,quote_off_topic,live_quote,judge S067:copy_sha,quote_not_in_copy,quote_off_topic,live_quote,judge S068:copy_sha,quote_not_in_copy,quote_off_topic,live_quote,judge S069:copy_sha,quote_not_in_copy,quote_off_topic,live_quote,judge S071:copy_sha,quote_not_in_copy,quote_off_topic,live_quote,judge S073:copy_sha,quote_not_in_copy,quote_off_topic,live_quote,judge S074:copy_sha,quote_not_in_copy,quote_off_topic,live_quote,judge S076:copy_sha,quote_not_in_copy,quote_off_topic,live_quote,judge S117:copy_sha,quote_not_in_copy,quote_off_topic,live_quote,judge S128:copy_sha,quote_not_in_copy,quote_off_topic,live_quote,judge S137:copy_sha,quote_not_in_copy,quote_off_topic,live_quote,judge S149:copy_sha,quote_not_in_copy,quote_off_topic,live_quote,judge
new_ok=0 new_failures=none
C1=unmet exit=1
```
Exit code: 1
Stderr: empty

### all-unreachable

```sh
timeout --kill-after=5 600 prlimit --as=2147483648 -- python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-32/count-c1.py 50ff0b9a87431617c48ce8cafa953ba3337bd93a --repo /fast/scratch/hyaku/mori-r32/CtlDoNothingJunk/lane
```
```text
revision=50ff0b9a87431617c48ce8cafa953ba3337bd93a base=641a6e86ecc60634d215c0a47ab86c47661abf86 population=34 pop_sha256=4426b6501a01c07b
recheck_rows=34 header_ok=True section_sha256=03df5534cd7d16cc judge_ok=False judge_seat_ok=False judge_agree=0
rows_ok=0/34 verdicts={'unreachable': 34}
row_failures=S001:counter_fetch_ok,judge S002:counter_fetch_ok,judge S007:counter_fetch_ok,judge S012:counter_fetch_ok,judge S014:counter_fetch_ok,judge S015:counter_fetch_ok,judge S031:counter_fetch_ok,judge S037:counter_fetch_ok,judge S039:counter_fetch_ok,judge S040:counter_fetch_ok,judge S041:counter_fetch_ok,judge S043:counter_fetch_ok,judge S044:counter_fetch_ok,judge S045:counter_fetch_ok,judge S046:counter_fetch_ok,judge S047:counter_fetch_ok,judge S049:counter_fetch_ok,judge S051:counter_fetch_ok,judge S052:counter_fetch_ok,judge S056:judge S058:counter_fetch_ok,judge S062:counter_fetch_ok,judge S064:counter_fetch_ok,judge S067:counter_fetch_ok,judge S068:counter_fetch_ok,judge S069:counter_fetch_ok,judge S071:counter_fetch_ok,judge S073:counter_fetch_ok,judge S074:counter_fetch_ok,judge S076:counter_fetch_ok,judge S117:counter_fetch_ok,judge S128:counter_fetch_ok,judge S137:counter_fetch_ok,judge S149:counter_fetch_ok,judge
new_ok=0 new_failures=none
C1=unmet exit=1
```
Exit code: 1
Stderr: empty

### restored-freeze

```sh
timeout --kill-after=5 600 prlimit --as=2147483648 -- python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-32/count-c1.py 29f7d04355f17b5d45d6e00c40e2a5c3e5a2c9c4 --repo /fast/scratch/hyaku/mori-r32/CtlDoNothingJunk/lane
```
```text
revision=29f7d04355f17b5d45d6e00c40e2a5c3e5a2c9c4 base=641a6e86ecc60634d215c0a47ab86c47661abf86 population=34 pop_sha256=4426b6501a01c07b
recheck_rows=0 header_ok=False section_sha256=e3b0c44298fc1c14 judge_ok=False judge_seat_ok=False judge_agree=0
rows_ok=0/34 verdicts={}
row_failures=S001:rows=0 S002:rows=0 S007:rows=0 S012:rows=0 S014:rows=0 S015:rows=0 S031:rows=0 S037:rows=0 S039:rows=0 S040:rows=0 S041:rows=0 S043:rows=0 S044:rows=0 S045:rows=0 S046:rows=0 S047:rows=0 S049:rows=0 S051:rows=0 S052:rows=0 S056:rows=0 S058:rows=0 S062:rows=0 S064:rows=0 S067:rows=0 S068:rows=0 S069:rows=0 S071:rows=0 S073:rows=0 S074:rows=0 S076:rows=0 S117:rows=0 S128:rows=0 S137:rows=0 S149:rows=0
new_ok=0 new_failures=none
C1=unmet exit=1
```
Exit code: 1
Stderr: empty

## 4. Failure reasons and counter limit

Do-nothing: all 34 ids report `rows=0`. Junk: all 34 report `copy_sha,quote_not_in_copy,quote_off_topic,live_quote,judge`. All-unreachable: 33 report `counter_fetch_ok,judge`; S056 reports only `judge`. Every score reports `new_ok=0` (the absence of candidates prints `new_failures=none`, not success). See full stdout above and `/fast/scratch/hyaku/mori-r32/CtlDoNothingJunk/{do-nothing-base,do-nothing-freeze,junk-table,all-unreachable}.json`.

Transcript-content limit: the counter tests existence, not the claimed curl exit statuses (`.ufo/waves/round-32/count-c1.py:261-265`). Reproducer: score `50ff0b9a87431617c48ce8cafa953ba3337bd93a` in the sandbox with the exact live command above. S056's fabricated three-line transcript raises no transcript or live-fetch failure; only the missing judge rejects that row. This is not a demonstrated C1 bypass: all rows remain rejected and new_ok is zero. No negative control printed C1=met.

Strict mutation-kill classification: inconclusive, not killed/survived, because the pristine baseline itself is C1=unmet. These are successful negative-control rejections, not a passing-positive-baseline mutation claim.

## 5. Restoration and hashes

Restoration command (exit 0):
```sh
timeout --kill-after=5 120 prlimit --as=2147483648 -- git -C /fast/scratch/hyaku/mori-r32/CtlDoNothingJunk/lane checkout -q 29f7d04355f17b5d45d6e00c40e2a5c3e5a2c9c4
```
Restoration revision command and full output:
```text
$ timeout --kill-after=5 120 prlimit --as=2147483648 -- git -C /fast/scratch/hyaku/mori-r32/CtlDoNothingJunk/lane rev-parse HEAD 'HEAD^{tree}'
29f7d04355f17b5d45d6e00c40e2a5c3e5a2c9c4
82466f08cbb24cee335c4c0ee82817f3036d7625
exit_code=0
```
Before and restored tree: `82466f08cbb24cee335c4c0ee82817f3036d7625` (`/fast/scratch/hyaku/mori-r32/CtlDoNothingJunk/pristine.json:13-16`, `/fast/scratch/hyaku/mori-r32/CtlDoNothingJunk/restoration.json`, and revision output above). Before: lesson absent (cat-file exit 128), recheck evidence tree empty (ls-tree exit 0); restored: all 35 injected paths absent. Restored detector stdout equals pristine freeze stdout byte-for-byte. Evidence: `/fast/scratch/hyaku/mori-r32/CtlDoNothingJunk/pristine.json:19-28`, `/fast/scratch/hyaku/mori-r32/CtlDoNothingJunk/restoration.json`, `/fast/scratch/hyaku/mori-r32/CtlDoNothingJunk/restored-freeze.json`.

| Bytes | Before | Mutated | Restored |
| --- | --- | --- | --- |
| lesson | absent | junk SHA256 `6817b44703d5e0a99e099a114104857edd20cefef2dacea7f7ce4f854a01ef94`; unreachable SHA256 `60400d5ccb5faa0e17924fba25b9e88ddb666b44e3c884210789234c276ba81e` | absent |
| each fake transcript (34) | absent | SHA256 `d00da85827bc624f991c64d731e0d3d196dffe323676209ea57295b8ab5df967` | absent |
| frozen lane counter | SHA256 `cfa0b988a51fc59720382016c0608408c022b9aaedc19f92c24453493d1a84fe` | unchanged | same SHA256 |
| frozen population | SHA256 `4426b6501a01c07bdb3347c712c5e858447be47204fa9017c02ab6113e83e178` | unchanged | same SHA256 |

Actual before input hashes: `timeout 120 prlimit --as=2147483648 -- sha256sum /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-32/count-c1.py /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-32/c1-population.json`; actual after hashes were computed with `hashlib.sha256(path.read_bytes()).hexdigest()` and recorded under `inputs_after` in restoration.json. The before/after dictionaries compare equal. Mutated lesson/transcript hashes were read from the sandbox bytes before checkout; junk hash is of the exact bytes passed to tool.write (`construction.json`).

All started commands completed and their process trees were awaited; no background jobs, host services, lane Git/JJ writes, or other runtimes were used. Only the assigned report was written in the lane. Tool installs/updates: none.
