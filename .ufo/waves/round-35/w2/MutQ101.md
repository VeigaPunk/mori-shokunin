measured 2026-10-23T09:16:52Z
# MutQ101 — QUALITY 101

## Scope and detector

Pinned source revision: `cedb0ec4f3a4f672804deac388b7191258f01fcd`. Lane-relative source citations below refer to that revision, read with bounded `git show`, never the moving working tree.

Axes: negative discrimination, positive specificity, fidelity to the written Check, exact-byte restoration and containment.

The detector is QUALITY 101's field-by-field Check (`corpus/QUALITY.md:788-798`), not P-C1. Its stated rejection conditions are empty, denying or off-topic fields. The declared five fields are key, capability, what it can now do, evidence, first-working round; the inventories below retain all 18 rows and 90 fields.

Scratch root `S` = `/fast/scratch/hyaku/mori-r35/MutQ101`. `S/field-census.py:1-7,38-68` inventories fields and aggregates **manual semantic readings**, recorded before replay in `S/cases.json:9,197-198,387-388,577-583,772-773`. It is not an independent or general-purpose prose classifier. In particular, the 9d result below is the literal manual reading, not evidence that a new automated Q101 oracle exists.

Historical `C1=met` results and the joint non-skip ruling are committed at `.ufo/waves/round-35/evidence/c1-controls.txt:36-44`. The two invented receipts supply `C1=met` as a stimulus; I did not run P-C1 or claim new counter measurements (`S/cases.json:584,774`).

## Mutation and bounded replay

Each isolated `S/receipt-<case>.json` contains one met entry. Pristine ruling: `skip`. The sole behavioral edit was line 4, changing that ruling to `not a skip`; restoration put back the exact original line. These are normalized ruling-only witnesses, not byte-exact transplants of the complete historical receipt. Positive acceptance is a calibration control, not a planted defect.

The identical command for every stage was:

`timeout 45 prlimit --as=536870912 --cpu=30 -- python3 -I -B /fast/scratch/hyaku/mori-r35/MutQ101/field-census.py <case>`

Four independent cases ran concurrently per stage, with all children awaited. Full commands, stdout, stderr and exits: `S/{pristine,mutated,restored}-<case>.txt:1-97`. Q101 is one-way: a skip ruling does not assert that deficient content does the claimed work, so the pristine receipts pass this particular Check.

| Case | Expected mutated Check | Observed mutated Check | Pristine / mutated / restored exits |
|---|---|---|---|
| 10c, empty capability/what | fail | fail; 36 empty fields | 0 / 1 / 0 |
| 9d, strong evidence plus dangling plaintext | fail | pass; no listed rejection condition established | 0 / 0 / 0 |
| Invented denial-prose receipt | fail | fail; one explicitly denying field | 0 / 1 / 0 |
| Invented fully-filled positive receipt | pass | pass; no deficient field | 0 / 0 / 0 |

Actual mutated summaries (`S/mutated-<case>.txt:95`; each stderr is empty at :97):

```text
10c: fields=90 empty=36 denying_by_manual_review=0 off_topic_by_manual_review=0 Q101=fail
9d: fields=90 empty=0 denying_by_manual_review=0 off_topic_by_manual_review=0 Q101=pass
invented-denial: fields=90 empty=0 denying_by_manual_review=1 off_topic_by_manual_review=0 Q101=fail
invented-positive: fields=90 empty=0 denying_by_manual_review=0 off_topic_by_manual_review=0 Q101=pass
```

VERDICT: killed — 10c non-skip ruling.
VERDICT: survived — 9d non-skip ruling; the required negative did not fail the written Check.
VERDICT: killed — invented denial-prose non-skip ruling.
VERDICT: survived — invented positive non-skip ruling, as expected; not a coverage hole.

## Field-by-field application

The following are the first rows; every remaining row's five contents are listed in `S/mutated-<case>.txt:10-94`.

| Field | 10c | 9d | Invented denial | Invented positive |
|---|---|---|---|---|
| key | `rounds[313].capabilities_added[0]` | same key | same key | same key |
| capability | empty | sources-registry (34 rows; census clean) | same topical capability | same topical capability |
| what it can now do | empty | bound to closure record | explicit denial of capability-to-closure binding | sources-registry |
| evidence | backticked `corpus/SOURCES.md` | backticked `corpus/SOURCES.md` plus unbackticked `.ufo/waves/round-34/w1/notes-00.md` | backticked `tools/mori-census.sh` | backticked `tools/mori-census.sh` |
| first-working round | 12 | 12 | 12 | 12 |

Content anchors: `.ufo/waves/round-35/c0/CtlSkipDesign-register.md:5-22`; `.ufo/waves/round-35/c0/CtlDangling-register.md:74-91`; `S/mutated-invented-denial.txt:5-9`; `S/mutated-invented-positive.txt:5-9`.

10c has two empty fields in every row, so its non-skip ruling fails directly; no reinterpretation of P-C1 is needed (`corpus/QUALITY.md:789-797`; `S/mutated-10c.txt:5-95`).

The invented denial changes only the first positive row's what-cell to this sentence: `This register does not bind any admitted capability to its closure.` It contradicts the claimed work despite every field being filled, so Q101 rejects the non-skip ruling (`S/cases.json:395-403,577-584`; `S/mutated-invented-denial.txt:7,95`).

The invented positive retains all 18 positive binding rows and filled topical prose. Historical runway settings prose was replaced with a topical capability name and action, without copying settings values. Its fields contain neither an empty cell nor a denial; acceptance is correct for this Check, not a certificate of every other QUALITY criterion (`S/cases.json:587-774`; `S/mutated-invented-positive.txt:5-95`).

## Hole: 9d is not forced red

9d's evidence field is nonempty and includes a real, topical evidence pointer alongside the dangling plaintext. Its key, capability, closure-binding prose and round are also filled and about the claimed object (`.ufo/waves/round-35/c0/CtlDangling-register.md:74-91`). A nonexistent extra pointer is not itself a denial; the field as a whole is not shown to be off-topic merely by that pointer's nonexistence. This semantic reading was recorded explicitly, not inferred from a zero keyword count (`S/cases.json:9,387-389`).

The written Check has no evidence-resolution requirement, no rule rejecting any invalid fragment in an otherwise topical field, and no requirement that the entire evidence cell consist exclusively of valid citations (`corpus/QUALITY.md:788-795`). The receipt's separate only-backticked-paths promise is at `.ufo/waves/round-35/evidence/c1-controls.txt:42`; importing it into Q101 would add a condition. Therefore the requested 9d rejection is not established by Q101 as written. This is the coverage finding; I did not amend the criterion or the frozen claim.

## Exact restoration evidence

SHA-256 values are printed by the same detector in `S/{pristine,mutated,restored}-<case>.txt:4`:

| Receipt | Pristine SHA-256 = restored SHA-256 | Mutated SHA-256 |
|---|---|---|
| 10c | `9c53dacd3774e4faa760f0595752e265e15e98778f0a8394cefdfb100dae7f92` | `3815f60fdfcdb9979c6d086ed4261f08585daefc4d138a5123b2493115fe8485` |
| 9d | `cbf6da05406dbeeb9d4e82df796a059074c366a32779a937a26a4a5550d6505d` | `a60eaef566e8755472c9d9e34454ec81874c6a720fc4eb33e7a41dc3b3af7afb` |
| invented-denial | `5e0264142c88a230cf07da3f19036bfb1859610f4f7ecf14c30c06feffe2c032` | `4b5a69be722f89bd18a5150f3135168ff55ce452148326b138e81e7db56cce7a` |
| invented-positive | `ef5b1b5b34a5a5a3451c567e6980ac73fff52c6f8a56b31db76d978789a8a497` | `4776eee0c78ca00e64c4b505f04378460fff8040aeb132f79cdd3218eb485ed6` |

All pristine and restored detector exits were 0, and their field counts and receipt hashes agree; no failing baseline was counted as a killed mutant (`S/replay-summary.json`, each stage's log :2,4,95). Historical register bytes were loaded read-only from the pinned commit at every stage (`S/field-census.py:21-35`).

Containment: only this report was written in the lane; scratch evidence stayed under `S`. No lane/fleet git writes, integrations, subagents, persistent jobs, live census/journal probes or installations/updates were performed. Live host queries were the report's UTC `date` readings and `timeout 10 prlimit --as=268435456 --cpu=5 -- df -h /fast`, which reported 165G available before scratch preparation; no clone or large artifact was created. All bounded detector subprocesses completed and were awaited before this handoff.
