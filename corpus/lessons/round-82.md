# Round 82 — mori (L1 MoriR82), attempt 1, wave w1

round: 82
date: 2026-11-04
entering: ebcf2c72df203c855cfafb5223c6e22b1e12c481
freeze: 20551e56

Axes: operability 7, freshness 5, depth 5, coverage 6, calibration 5,
adjacency 6. C1 works operability (capability acquisition); C2 freshness and
C3 depth work tied-lowest axes. No scalar score change is asserted.
Detection and report only; neither a source nor a receipt authorizes remediation.

Frozen authority: `.ufo/waves/round-82/contract.md`, P-C1/P-C2/P-C3,
mutation set, drift derivation table, revision-arm interface and real bindings.
This lesson does not amend that authority. The following are targets, not
observed after-values:

| Claim | Keeper (run from the lane root) | Target, exit 0 |
|---|---|---|
| C1 — operability (7): a committed revision-agnostic mutation harness replaces the deleted scratch-only r81 recipe | `python3 -I .ufo/waves/round-82/count-c1.py <rev>` | `C1=met harness=present killed=11 survivors=0 total=11 pristine=green` |
| C2 — freshness (5): retire the r10 acceptance pin with baseline-derived classification of all live drift tokens, keeping the live drift run red | `python3 -I .ufo/waves/round-82/count-c2.py <rev>` | `C2=met tokens=64 classified=64 agreed=64 residual=0 retired=1 cell=1` (also `stale=0`) |
| C3 — depth (5): revision-precision arm and three real bindings | `python3 -I .ufo/waves/round-82/count-c3.py <rev>` | `C3=met tool=present arms>=30 defeated=1 bindings=3 revisions=0` |

C1's eleven kills confirm the r81 closure at the current bytes; they are
not eleven new kills. The capability delta is the durable harness. C2 does
not accept the rejected r20 re-pin or erase retained evidence loss. C3 tests
registered literal value/revision bindings, not semantic command provenance
or arbitrary unregistered revision claims.

Entering controls, copied verbatim from
`.ufo/waves/round-82/evidence/controls-r82.txt`. These are inherited receipts,
not rerun by this lesson seat:

```text
# mori round-82 do-nothing controls — revision ebcf2c72df203c855cfafb5223c6e22b1e12c481
# taken before any wave seat existed; each counter grades that revision's own bytes.
# freezing commit: this file (see LOG.md round-82 for the landed hash)

$ python3 -I .ufo/waves/round-82/count-c1.py --selftest --scratch /fast/scratch/hyaku/mori-r82/l1
PASS sensitive_killed harness=present killed=1 survivors=0 total=1 pristine=green | MUTANT sensitive.py trip_guard killed rc=1
PASS blind_survives harness=present killed=0 survivors=1 total=1 pristine=green
PASS duplicate_anchor_excluded harness=present killed=0 survivors=0 total=0 pristine=green
PASS red_pristine_reported harness=present killed=0 survivors=0 total=0 pristine=red
C1_COUNTER_SELFTEST pass=4 fail=0
rc=0

$ python3 -I .ufo/waves/round-82/count-c1.py ebcf2c72
C1=unmet harness=absent rev=ebcf2c72df20
rc=1

$ python3 -I .ufo/waves/round-82/count-c2.py --selftest --scratch /fast/scratch/hyaku/mori-r82/l1
PASS conformant tokens=4 classified=4 agreed=4 residual=0 stale=0 retired=1 cell=1
PASS unclassified_token tokens=4 classified=3 agreed=3 residual=0 stale=0 retired=1 cell=1
PASS class_disagrees tokens=4 classified=4 agreed=3 residual=0 stale=0 retired=1 cell=1
PASS residual_keeps_unmet tokens=4 classified=4 agreed=3 residual=1 stale=0 retired=1 cell=1
PASS stale_classification tokens=4 classified=4 agreed=4 residual=0 stale=1 retired=1 cell=1
PASS red_cell_keeps_unmet tokens=4 classified=4 agreed=4 residual=0 stale=0 retired=1 cell=0
PASS retired_row_required tokens=4 classified=4 agreed=4 residual=0 stale=0 retired=0 cell=1
PASS green_pin_is_unmet tokens=0 classified=0 agreed=0 residual=0 stale=4 retired=1 cell=1
PASS classification_file_absent tokens=4 classified=0 agreed=0 residual=0 stale=0 retired=1 cell=1
C2_COUNTER_SELFTEST pass=9 fail=0
rc=0

$ python3 -I .ufo/waves/round-82/count-c2.py ebcf2c72
unclassified +FINDING:OOM_KILL_JOURNAL
unclassified +FINDING:ROSTER_SET_MISMATCH
unclassified +FINDING:SEGFAULT_SIGNAL11_JOURNAL_USER
C2=unmet tokens=64 classified=0 agreed=0 residual=0 stale=0 retired=0 cell=0 rev=ebcf2c72df20
rc=1

$ python3 -I .ufo/waves/round-82/count-c3.py --selftest --scratch /fast/scratch/hyaku/mori-r82/l1
PASS summary_parse {'revisions': 2, 'bindings': 5}
PASS pins_schema [{'carrier': 'A', 'rev': 'x', 'path': 'A', 'key': 'k', 'value': 1, 'row_contains': 'r'}]
PASS pins_absent_list no revisions key
PASS carrier_drift_guard text compare
PASS arms_floor floor=30
C3_COUNTER_SELFTEST pass=5 fail=0
rc=0

$ python3 -I .ufo/waves/round-82/count-c3.py ebcf2c72
C3=unmet tool=present arm=absent rev=ebcf2c72df20
rc=1
```

## Gate

**PENDING SCOUT — recommendation table, not an admission receipt.** At this
seat's first inspection, neither `corpus/evidence/sources-r82/` nor
`.ufo/waves/round-82/w1/Mo82Sc01Source.md` existed. No source body was opened
by this seat; no quote, hash, byte count or line count is invented. The
registry ends at S596: measured 369 source rows, maximum id S596, S597
absent. Thus **S597 is the next unused id**, not a row already admitted.

| Candidate | Recommendation | Evidence needed / flip condition |
|---|---|---|
| S597 candidate: official Git revision syntax documentation, scoped to `<rev>:<path>` | Admit ONE row only after the scout's located evidence is available and the L1 makes the Gate decision | Scout receipt must name URL/final URL, access/status, durable pinned path, full sha256, byte/line counts and a located quote of at most 25 words. This seat has none of those source observations yet. |
| Stronger claim: Git revision syntax documentation proves the complete record gate correct or proves that the named command produced the value | **Reject the stronger claim**, not an external source row; screening-only limitation, no source body accessed | Flip only with a separately opened, located source for the stronger assertion and independent execution evidence for the local gate. Syntax alone cannot establish local fixture coverage, all-binding iteration or command provenance. |

The recommendation does not establish exit behaviour beyond the source's
actual wording. A present pin or contractual scout assignment is not proof
that a fetch, quote check or admission occurred.

## Mistakes

The fixes below distinguish the committed frozen counting surfaces from
implementation closure. The three r82 keepers are delivered under the
freeze; this seat has not executed them. No contract-only implementation
seat is upgraded into a passing repair.

| Class | Evidence pointer | Captured-by | Fix delivered this round and what makes it able to fail |
|---|---|---|---|
| Repeated revision-label error: D80-4 followed by D81-1; a value true at the later tree is attributed to an earlier revision | `corpus/lessons/round-80-verifier-spotcheck.md:183-189`; `corpus/lessons/round-81-verifier-spotcheck.md`, D81-1: `pointers=240` labelled `075574c8`, where the graded count is 237; 240 holds at `482dc48d` | Non-author closures only at discovery; the r81 pinned arm compared values to a command, not to the revision label. QUALITY 9 should have required resolving the carrying reference; new QUALITY 168 explicitly names the class | Frozen `.ufo/waves/round-82/count-c3.py` makes absence of the revision arm unmet and requires an independent wrong-revision fixture to produce `revisions=1`, exit 1, plus at least three green real bindings and at least 30 selftest arms. The implementation repair is `tools/mori-record-sweep.py` plus `.ufo/waves/round-82/record-pins.json`; at this seat's inspection those implementation bytes were not yet present, so their closure is not asserted. |
| Scratch-only mutation recipe: the receipt survives but its command no longer resolves | `corpus/lessons/round-81-verifier-spotcheck.md`, D81-3; `.ufo/waves/round-81/evidence/mutation-recheck-r81.txt` names deleted `/fast/scratch/hyaku/mori-r81/l1/mut5.py` | QUALITY 9 and 23 should have caught unresolved replay evidence; routed by the non-author r81 closure | Committed `.ufo/waves/round-82/count-c1.py` is both harness and keeper: exports the requested revision, derives literal-anchor mutations, runs pristine selftests before mutants, and reports survivors. Inherited detector controls distinguish sensitive killed, blind surviving, duplicate-anchor exclusion and red pristine; these are not fresh runs by this seat. Any survivor, red pristine or changed frozen population prevents the stated eleven-kill target. |
| Round-10 drift debt remains red for 72 rounds without a complete classification surface | `SCORECARD.md` entering freshness cell; `corpus/evidence/baseline-r10-20261015T2231Z.json`; r82 entering controls: 64 tokens, classified 0; rejected r20 re-pin recorded in the Round21 correction | QUALITY 10/41 prohibit cosmetic re-pins; QUALITY 65 requires per-token disposition on re-observation; QUALITY 69 preserves retained-loss blockers | Frozen `.ufo/waves/round-82/count-c2.py` supplies the baseline-derived agreement check, requires the live run to remain red, and rejects missing, wrong, stale or residual classifications and absent retirement/cell evidence. The intended data repair is `corpus/evidence/drift-classification-r82.txt` with the named Retired row and freshness cell; the SCORECARD text was visible, but the data file was absent at this seat's inspection. No passing classification is inferred from that prose. |

These are finite falsifiers, not universal guarantees. In particular,
C3's literal occurrence test cannot disambiguate a coincidental value in an
unrelated line, and C2's classification is not a fleet-health verdict or a
waiver of the Round21 retained-evidence-loss ruling.

## Census

Before: **369 source rows, exit 0**, inherited from the r81 lesson's
`## Census` after-block, not rerun as an entering measurement by this seat.
The r81 receipt also records 35 tolerated W04 duplicate-URL warnings.

After, at this seat's working-tree observation: **369 source rows,
exit 0**, not a final committed round-82 census. Exact command executed:

```text
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori
```

Output: 35 W04 duplicate-URL warning lines, followed by
`mori\tok\t/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md`;
`census_rc=0` from the exit-status wrapper. Exit 0 does not mean no warnings.
A separate Python row-grammar count over that file printed:

```text
source_rows=369
max_id=S596
S597_present=False
```

The census validator itself prints no row total; 369 is the separate
measured row count, not attributed to its stdout. S597 admission and any
subsequent census belong to the L1's later, named-revision evidence. No
C1/C2/C3 after-run, final-tip verdict, publication or source admission was
performed by this lesson seat.
