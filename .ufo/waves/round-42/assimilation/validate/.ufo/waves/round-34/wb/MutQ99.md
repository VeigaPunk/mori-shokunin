measured 2026-10-23T07:48:19Z
# QUALITY 99 Check-sentence mutation probe

## Scope and axes

Target: attempt-2 draft `/fast/scratch/hyaku/mori-r34/a3-L1/drafts/corpus_QUALITY.md:735-746`, not the committed QUALITY 98 or the frozen C1 counter.
Axes: receipt completeness; pre-data timing; generator-label coverage; live-bound direction; negative-control discrimination; exact restoration.
All bare evidence filenames below resolve under `/fast/scratch/hyaku/mori-r34/a3-MutQ99/`.

The exact attacked sentence is:
> Check: the contract's control table names both controls and the receipt scores each `unmet` under the frozen counter before the first data commit.
Source: the target draft, lines 741-742; captured in `check-sentence.txt:1` without its `Check:` prefix.

## Fixture and detector

- `contract-b9fb029e.md:1-150` is the byte-exact `git show b9fb029e:.ufo/waves/round-34/contract.md` copy. Its SHA-256 is recorded at `hashes-before.txt:6` and `hashes-after.txt:6`.
- The conforming **synthetic table fixture** is `pristine.md:77-78,153-162`: the label control covers all 41 possible offline names plus every fed-live generator name; the harness control recognizes FIFO/namespace/tmpfs/interval/seed and returns zero outside it; both receipt lines say `C1=unmet` under the exact frozen counter hash at 05:13:09Z. Offline bounds are exact; the live fixture declares positive activity and bounds 1 through 4096, excluding zero.
- The offline name domain follows the frozen generator's eight disks, up to three partitions per disk, four stacked names, four virtual names and `xyz9` (`count-c1-a1-b9fb029e.py:111-166`); fed-live uses real sysfs names (`count-c1-a1-b9fb029e.py:296-303`). The fixture's complete offline map is at `pristine.md:158`.
- The fixture sets first data to the tool landing `ba525e1a`, 2026-10-23T05:30:38Z, the first commit after the pre-data `b9fb029e` receipt commit (`provenance.txt:1-7,10-14`). Variant 2 uses 05:30:39Z, so it is after that data commit, not merely after the control freeze (`v2-post-tool-receipt.md:162`).
- **These are fixture receipt lines, not invented historical counter results.** No claim is made that P-C1-A1 was run on the invented controls or that the synthetic live bounds were measured (`pristine.md:153-155`). The requested exercise is the sufficiency of 99's written Check.
- 99 supplies natural language, not an executable or receipt schema. `detect-q99-check.py:1-5,12-52` implements only its explicit conjuncts: table names, both scores exactly `unmet`, exact frozen-counter identity, and receipt dates strictly before the stated first-data time. It does not silently add generator-semantic or live-bound checks.
- Consequently, “names both controls” is operationalized as naming the two control kinds, not proving their implementations satisfy the preceding definitions. If that phrase instead imports those definitions as proof obligations, 99 gives no mechanical procedure for discharging them; the survivor verdicts below are scoped to the explicit name/receipt Check, not every possible semantic reading.
- Same command on pristine, mutated, restored bytes for every variant: `timeout 10s python3 /fast/scratch/hyaku/mori-r34/a3-MutQ99/detect-q99-check.py /fast/scratch/hyaku/mori-r34/a3-MutQ99/active.md`, with 256 MiB address-space cap and 12-second supervising timeout (`probe-output.txt:1`). Python is 3.14.8 (`hashes-before.txt:9-10`).

## Actual outputs and verdicts

Control output (repeated on each pristine and restored run):
```
names=label:yes,harness:yes scores=label:unmet,harness:unmet frozen=label:yes,harness:yes before-data=label:yes,harness:yes CHECK=PASS reason=none
```
All five baseline exits were 0 and all five restored exits were 0; therefore none is a baseline-failure/inconclusive result (`probe-output.txt:3-56`).

### 1. Harness control present, receipt missing
Mutation: delete only its receipt; table entry remains (`v1-no-harness-receipt.md:78,161`). Expected written detector: reject missing score/receipt.
Actual: pristine/mutant/restored exits **0/1/0**; output:
```
names=label:yes,harness:yes scores=label:unmet,harness:MISSING frozen=label:yes,harness:missing before-data=label:yes,harness:missing CHECK=FAIL reason=harness-receipt-missing
```
Evidence: `probe-output.txt:2-12`.
VERDICT: variant 1 killed

### 2. Receipt after tool/data commit
Mutation: change only the harness receipt date from 05:13:09Z to 05:30:39Z (`v2-post-tool-receipt.md:162`). Expected written detector: reject the post-data date.
Actual: exits **0/1/0**; output:
```
names=label:yes,harness:yes scores=label:unmet,harness:unmet frozen=label:yes,harness:yes before-data=label:yes,harness:no CHECK=FAIL reason=harness-not-before-data
```
Evidence: `probe-output.txt:13-23`.
VERDICT: variant 2 killed

### 3. Label control only recognizes fixed-seed bytes
Mutation: replace only the label-control row with round 34's actual C-labelkey description: answers 12 fixed-seed scenarios from input bytes, `{}` otherwise (`v3-fixed-seed-bytes-only.md:77`; original `contract-b9fb029e.md:77`). Its historical receipt actually reports fixed 12/12, random 0/300 and `C1=unmet` (`.ufo/waves/round-34/evidence/c1-controls.txt:23-25`).
Expected written detector: pass; the named control and both pre-data `unmet` receipts remain. A generator-coverage inspection would reject this substitution, but that is not an explicit Check conjunct.
Actual: exits **0/0/0**; output:
```
names=label:yes,harness:yes scores=label:unmet,harness:unmet frozen=label:yes,harness:yes before-data=label:yes,harness:yes CHECK=PASS reason=none
```
Evidence: `probe-output.txt:24-34`.
VERDICT: variant 3 survived

### 4. Live arm bounded above only
Mutation: replace the live-arm line with an upper-only bound that admits zero; both table entries and receipt lines remain (`v4-upper-only-live.md:160-162`). Expected written detector: pass; the Check says nothing about live bounds.
Actual: exits **0/0/0**; output:
```
names=label:yes,harness:yes scores=label:unmet,harness:unmet frozen=label:yes,harness:yes before-data=label:yes,harness:yes CHECK=PASS reason=none
```
Evidence: `probe-output.txt:35-45`.
VERDICT: variant 4 survived

### 5. Both controls scored, one met
Mutation: change only the harness receipt result from `C1=unmet` to `C1=met` (`v5-one-control-met.md:162`). Expected written detector: reject; “each unmet” is stronger than merely having scores.
Actual: exits **0/1/0**; output:
```
names=label:yes,harness:yes scores=label:unmet,harness:met frozen=label:yes,harness:yes before-data=label:yes,harness:yes CHECK=FAIL reason=harness-not-unmet
```
Evidence: `probe-output.txt:46-56`.
VERDICT: variant 5 killed

## Sentences not mechanically discharged by the Check

1. The first sentence requires output derived from generator labels rather than rule inputs, and harness-only work with no real-input work (target draft:735-740). Names and `unmet` lines do not demonstrate either behavior. It supplies no implementation-inspection rule, generator-domain comparator, harness-independence test or proof of “every judged output.” Variant 3 exposes the name-versus-definition gap (`probe-output.txt:24-34`).
2. The second sentence requires **each named arm**, **real input**, and bounds **in both directions** that defeat a constant (target draft:740-741). The Check has no arm inventory, real-input receipt or lower/upper-bound comparison. Variant 4 survives (`probe-output.txt:35-45`). The sentence also specifies no bounding formula or positive-activity precondition; [INFERENCE] a nominal two-sided interval `[0,U]` still permits zero, and an idle real sample cannot distinguish correct zero from constant zero.
3. The Check's timing/counter clauses are mechanically decidable only after supplying a receipt grammar, frozen-counter identity and first-data anchor, as this fixture does (`detect-q99-check.py:12-27,40-48`). A date alone does not establish that a run or receipt existed then; no receipt-commit/ancestry procedure is named in 99 (target draft:741-742). Also, its first sentence's “before any data seat” is not mechanically established by comparing dates with the later first data commit. No additional provenance attack was run.

These are coverage findings against the written Check, not permission to amend the frozen C1 contract, counter or target.

## Before/after hashes and restoration

Let P = `a93df31607fd24bf910359e3072238c1f97e1bf29d9e345ef6d5b608f3d5d925`.
Every cycle's before and restored SHA-256 equals P; mutation SHA-256 values were:

| Variant | Mutated SHA-256 | Evidence |
|---|---|---|
| 1 | `dcdce2b2778a8c4e0ed3add45acbb12e78ec9cee99b3766355c1c469d2dcb917` | `probe-output.txt:4,7,10` |
| 2 | `f229eb70b346f4ff7e9cc6b15357c6e57be7f79aa48e2e1afe810b26bab787e6` | `probe-output.txt:15,18,21` |
| 3 | `92905077b2f56b6c1359e04595a26a991bb023daeca64b8364ae2cd83e89010b` | `probe-output.txt:26,29,32` |
| 4 | `1c28866221d12cc8c054232d5ee573a7aa915bd241ec0dbdbee0ce70308f976d` | `probe-output.txt:37,40,43` |
| 5 | `0bac8f0c3494be3d436e33f2e905019a14554e26ecba304617aa43d04e610560` | `probe-output.txt:48,51,54` |

Final `active.md` and `pristine.md` both hash to P (`hashes-after.txt:9-10`). Draft QUALITY, lane contract, frozen counter, judged tool, pinned copies and detector have identical before/after hashes (`hashes-before.txt:2-8`; `hashes-after.txt:2-8`; `probe-output.txt:57`). The detector hash is `809445b5b7913a930f720e41e3e10bce79a80c75167f54415d6277fc58c91b9b`.

No installation/update, live disk load, block-device changes, lane commits, background jobs or other runtime launch was performed. All started detector/hash/version commands completed synchronously within their caps; the executed detector output and exit codes are retained in `probe-output.txt:1-57` and `probe-results.json`. Scratch fixtures and detector remain as the assigned evidence; only this report is written into the lane.
