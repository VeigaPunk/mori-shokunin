measured 2026-10-23T08:00:46Z
# CritQ99Revised — residual review of QUALITY 99

VERDICT: admit with listed fixes — retain the narrower label/harness repair; make Check (c) arm-attributable and activity-qualified, and correct the two evidence descriptions below. This is a review recommendation, not canonical admission.

## Scope, axes and evidence names

Axes: calibration (does rejection establish the intended discrimination?), operability (can the Check be applied without supplying new rules?), coverage (generator families and named arms), and provenance (frozen bytes and receipt ancestry).

Paths used below:
- `Q` = `/fast/scratch/hyaku/mori-r34/a3-L1/residual-snap/corpus_QUALITY.md`.
- `M` = `/fast/scratch/hyaku/mori-r34/a3-MutQ99/`.
- `W` = `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-34/`.
- `G` = `/fast/scratch/hyaku/mori-r34/a3-CritQ99Gap/`.
- `C` = `W/count-c1-a1.py`; `F` = `M/contract-b9fb029e.md`.

Reviewed Q:733-760, not a later working-tree revision. Command `timeout 15s prlimit --as=268435456 --cpu=10 -- sha256sum <Q> <M/count-c1-a1-b9fb029e.py> <C> <F>` returned, respectively:
```
6677d4100c00b624d6e5b1c3b8708ed30587338e6b606fda8d34f5ed205d45df
c14c3494d7356fa7c619a0e30c10cd9b71baa99eb0fb74cfd34c7f21b3b181e2
c14c3494d7356fa7c619a0e30c10cd9b71baa99eb0fb74cfd34c7f21b3b181e2
695c8412769da278932b44198649853c140d0eeda88e7591f71bc2950765cc11
```
The requested `timeout 30s prlimit --as=536870912 --cpu=25 -- git -C /home/vgpnk/Projects/shokunin/mori-shokunin show b9fb029e:.ufo/waves/round-34/contract.md` was read directly; its control table and A1 agree with F:65-88,111-150.

## Applying revised Check (a)-(c)

These are document/source applications, not new frozen-counter executions. Check text: Q:742-746.

| Object | (a): both qualifying controls; label families | (b): both unmet, committed ancestor of first data | (c): two boundary receipts per named arm | Application |
|---|---|---|---|---|
| Round 34 at b9fb029e | FAIL: C-labelkey is fixed-input-byte keyed; no harness-keyed row (F:69-81,142-150) | FAIL: the required harness control has no receipt; the existing label receipt does not qualify for (i) (W/evidence/c1-controls.txt:23-25) | FAIL: no complete arm-bound receipt pairs; the real-live zero hole remains (C:273-293) | fails |
| MutQ99 variant 3, retained bytes | FAIL: row 77 still explicitly keys on the 12 fixed-seed input bytes; an appendix listing labels cannot change that behavior (M/v3-fixed-seed-bytes-only.md:77,158) | Not established: synthetic scores/date strings, no receipt-commit anchor (same file:155-162) | FAIL: bounds are descriptions, not the newly required boundary receipts (same file:159-162) | fails |
| MutQ99 variant 4, retained bytes | Both kinds and a label-domain cross-reference are present; strict row-local family listing still needs expansion (M/v4-upper-only-live.md:77-78,158) | Not established: the same synthetic-provenance limitation (same file:155-162) | FAIL: live explicitly accepts zero and has only an upper bound; no boundary receipt pairs (same file:160-162) | fails |
| My conforming logical table below | satisfies by construction | satisfies under the expressly synthetic commit graph | satisfies under the expressly synthetic receipt facts | expected pass [INFERENCE], not a measured pass |

The retained pristine also lacks (c)'s new receipts and (b)'s commit anchors (M/pristine.md:155-162). Therefore rejection of those unmodified old files is **not** a new valid baseline/mutant/restoration experiment. MutQ99's old detector checks names, scores, hashes and dates only; it must not be reported as a detector of the revised text (M/detect-q99-check.py:2-4,29-48).

On a normalized conforming model with all new receipt/provenance facts supplied, changing only (i) to fixed-seed bytes violates the explicit exclusion at Q:738 and (a); changing only the live bound to admit zero prevents the truthful below-bound rejection required by (c). Thus the revision now specifies rejection of variants 3 and 4 [INFERENCE]. No new execution or historical receipt is claimed.

For historical ancestry, `timeout 15s prlimit --as=268435456 --cpu=10 -- git -C /home/vgpnk/Projects/shokunin/mori-shokunin show -s --format='%H %P' ba525e1a0394154837eea5090e8bd27ed69c539c` returned:
```
ba525e1a0394154837eea5090e8bd27ed69c539c b9fb029e05dcfb79757c46821dc4b61cb79d1a29
```
This proves that b9fb029e is that tool/data commit's parent; it does not supply the missing controls or prove that every data-seat dispatch happened later (M/provenance.txt:10-14; Q:735,744).

## One conforming table written for this review

**Logical fixture only, not mori history or a counter run.** Define a hypothetical future frozen counter K and commit chain `freeze -> R -> D`, where D is first data and no data seat precedes R. K's bytes remain identical throughout. R contains the following complete receipts. These are stipulated test inputs, not asserted measurements; no fake hashes or historical commit identities are supplied.

The model claim names exactly two arms, saved-real-input and live-real-input. Its generator emits class labels `disk/*`, `partition/*`, `stacked/*`, `virtual/*`, `unknown/*` and state labels `absent/*`, `bad-line/*`, `gone/*`, `new/*`, `reset/*`, `ok/*`. Each arm has a genuine positive-activity `ok` witness with independently established bounds L=1, U=4096. Idle/non-ok cases remain separately valid. Each bound mutant changes only the named arm's numeric output; the baseline and other arm pass K on the same witness.

| shape / arm | control and listed families or boundary mutation | receipt under K, committed at R |
|---|---|---|
| (i) label-keyed | L: outputs depend only on class families `disk/*`, `partition/*`, `stacked/*`, `virtual/*`, `unknown/*` and state families `absent/*`, `bad-line/*`, `gone/*`, `new/*`, `reset/*`, `ok/*`, never saved input-byte tables or actual counters | `L unmet` |
| (ii) harness-keyed | H: recognizes the harness FIFO; does the work only there, returns constant zero on genuine input | `H unmet` |
| saved-real-input, low | replace that arm's output with 0 < L; other fields/work remain valid | `saved-low unmet reason=saved-lower-bound` |
| saved-real-input, high | replace that arm's output with 4097 > U; other fields/work remain valid | `saved-high unmet reason=saved-upper-bound` |
| live-real-input, low | replace that arm's output with 0 < L; other fields/work remain valid | `live-low unmet reason=live-lower-bound` |
| live-real-input, high | replace that arm's output with 4097 > U; other fields/work remain valid | `live-high unmet reason=live-upper-bound` |

With these declared facts, (a) has its family inventory, (b) has both frozen-counter unmet receipts at ancestor R, and (c) has the two boundary receipts for each named arm [INFERENCE]. This is a consistency example, not retroactive conformity of P-C1-A1. A real use needs actual immutable counter bytes, real witnesses, receipts and commit objects; a table alone cannot manufacture them.

## Strongest residual counterexample: wrong-arm rejection

Check (c) requires global `unmet`, but does not explicitly require a passing baseline, unchanged other arms, real-input witness identity, or a rejection attributed to the named bound (Q:744-746). There is already a concrete receipt demonstrating why that matters:

- C-zero-singleread has `fixed_pass=12/12 random_pass=300/300 live=fed-no-interval C1=unmet` under P-C1-A1 (W/evidence/c1-controls.txt:41-43).
- `lv = live(tool) or fed_live(tool, seed)` means a `fed-no-interval` result is reached only after the genuine live arm accepted the output (C:408; rejection origin C:358-359).
- That `unmet` therefore cannot certify a genuine-live lower-bound rejection. The harness-aware post-data probe repairs the fed behavior while retaining real zero rates and meets the entire predicate (W/evidence/ctl-postdata-shortcut/receipt.txt:3-9; rescore-a3.txt:7-12).

[INFERENCE] A receipt-only implementation of (c) that accepts the first receipt as its zero witness can congratulate itself while leaving precisely the live hole it claims to close. This is not a demonstrated complete 99-conforming bundle; it is a locally measured wrong-reason witness against the missing attribution rule.

Smallest safe correction: in (c), enumerate the contract's arms; require a passing baseline and paired mutations on the same positive-activity real-input witness, changing only the selected arm's numeric output while retaining valid shape, classes, timing and all other arms. Require the receipt to identify that arm's lower/upper-bound failure, not merely global `unmet`, and bind it to the frozen counter and witness. State how the positive lower bound is established; otherwise mark the check unproved. An idle correct rate can be zero under R6 (F:46-47), so do not reject legitimate idle behavior merely to make the zero control fail.

## Truth and scope of the explanatory sentences

1. **Shown able to fail on the historical table: true.** Fixed-seed keying and absence of the harness control suffice to fail (a), independently of any receipt interpretation (F:77,142-150; Q:747-748).
2. **"Upper-only": accurate for an activity-relative lower bound, but qualify the zero-receipt conclusion.** C:275 also rejects negative rates: the actual numeric floor is 0, not absent. C:277-278 supplies only the activity-relative upper bound. Zero is accepted by that arm for nondecreasing outer counters, not necessarily by the entire counter. A globally constant-zero program fails exact offline/fed comparisons (C:233-238,252,364-365,410). Replace Q:749-750's "the zero receipt ... would read C1=met" with "the genuine-live arm accepts zero; an otherwise conforming offline/fed program can retain that shortcut and meet C1, as ef936fb4 demonstrates."
3. **Post-data probe and first-draft history: supported.** Its one-read/zero/FIFO/name-pattern description and met scores match the two receipts above. MutQ99 reports variants 3 and 4 surviving (W/wb/MutQ99.md:51-68); ReviewQ99 requests the subject/check repairs (W/wb/ReviewQ99.md:36-49). The new (a)/(c) address those textual omissions, but do not establish the stronger arm-attribution property by themselves.
4. **Correction of 98's M1 to M3: supported.** The lesson places the shortcut at M2 and rule-order/generator gaps at M3 (corpus/lessons/round-34.md:82-100, relative to the lane root).
5. **Not covered: the limitation is warranted, with one precision fix.** Both additional programs really have stored `C1=met` receipts (G/census-counter.txt:4-8; G/lexical-counter.txt:4-8), and explicit disagreeing witnesses (G/witnesses.txt:2-13). But the census program retains sysfs-only partitions and drops sysfs-only **non-partitions**, not all sysfs-only devices (W/wb/CritQ99Gap.md:18-24). Change Q:758-759 accordingly. The blacklist description matches that report:43-56. Its assessment of a future 99-compliant counter is explicitly inference, not an executed certification (same report:73-90); Q should retain that narrow limitation, not claim those programs were tested against a repaired counter.

## Mechanical applicability and disposition

(a) is inspectable once the generator-family inventory is supplied; the actual class families are explicit in C:111-166. State assignments are randomized separately at C:180-199, so do not invent state-correlated labels that this generator does not emit. Put the inventory in the row or explicitly permit a referenced inventory. (b) is decidable from frozen-counter identity, the two receipt commits and the first-data anchor; timestamps alone, as in the old synthetic fixtures, do not discharge ancestry. (c) is human-checkable for missing receipts/obvious upper-only bounds, but is not yet a self-contained mechanical certificate that the selected real-input bound caused rejection. The matched-arm correction above closes that gap without changing the frozen round's predicate or scores (Q:741-746; C:408-410).

These are fixable calibration/operability defects, not a demonstrated necessary tradeoff. Do not amend the historical counter, target or count to repair the criterion. The broader rule-level gaps are appropriately outside this specific shortcut repair (Q:757-760; W/wb/CritQ99Gap.md:92-96).

No frozen-counter reruns, new runtime invocation, installs/updates, Git/JJ writes, load generation, background jobs or writes outside this report were performed. All shell commands used timeout and bounded address-space/CPU limits and completed. The first timestamp is the output of `timeout 10s prlimit --as=134217728 --cpu=5 -- date -u +%FT%TZ`.

Report: .ufo/waves/round-34/wb/residual/CritQ99Revised.md
