# Round 81 — mori (L1 MoriR81)

round: 81
date: 2026-11-04
entering: 44bc941a0e3e9676fa33a882b43d6e9793cbf74d

Axes: operability 7, calibration 5, coverage 6, depth 5, freshness 5,
adjacency 6. C1 works operability; C2 works calibration, tied for the lowest
non-retired score. No scalar score change is asserted.

- **C1 — operability (7):** close the r80 counters' seven routed exposures.
  Keeper: `python3 -I .ufo/waves/round-81/count-c1.py <rev>`;
  target `C1=met wrong=0 fixtures=7 real_c1=met real_c3=met`, exit 0.
- **C2 — calibration (5):** land `tools/mori-record-sweep.py` and correct
  unresolved after-cells and stale pinned record counts. Keeper:
  `python3 -I .ufo/waves/round-81/count-c2.py <rev>`;
  target `C2=met pending=0 pinned=0 tool=present agree=1`, exit 0.

Frozen authority: `.ufo/waves/round-81/contract.md` (P-C1, P-C2, fixture
expectations and interface); this lesson does not amend it. Targets above
are not measured after-results. The L1 appends measured after-blocks and
Gate verdicts at landing.

Entering controls, verbatim from
`.ufo/waves/round-81/evidence/controls-r81.txt:21-34` (inherited receipts,
not rerun by this lesson seat):

```text
$ python3 -I .ufo/waves/round-81/count-c1.py 44bc941a0e3e9676fa33a882b43d6e9793cbf74d
A2_summary_contradicts_mismatch_line expected=unmet got=met rc=0
A3_two_contradicting_summaries expected=unmet got=met rc=0
A4_second_carrier_row_stale expected=unmet got=met rc=0
A5_repo_path_with_space expected=met got=setup rc=2
B1_subdir_path_counts_as_naming expected=unmet got=met rc=0
B2_own_lane_prefix_excluded expected=met got=unmet rc=1
B6_directory_named_as_tool expected=met got=unmet rc=1
C1=unmet wrong=7 fixtures=7 real_c1=met real_c3=met rev=44bc941a0e3e
rc=1

$ python3 -I .ufo/waves/round-81/count-c2.py 44bc941a0e3e9676fa33a882b43d6e9793cbf74d --pins .ufo/waves/round-81/record-pins.json
C2=unmet pending=3 pinned=1 tool=absent agree=0 rev=44bc941a0e3e
rc=1
```

These are the same commands a do-nothing round leaves unchanged. A setup
exit is never a passing fixture. The controls also preserve the real-lane
r80 C1/C3 green arms; seven wrong fixture verdicts are not seven failures
on the actual lane.

## Gate

Source candidates are Mo81Sc02Source's opened candidates. Dispositions
below are the lesson draft's recommendations, not the L1's final Gate
verdicts or proof that a row has landed. The next unused entering row id
is **S596** (entering registry ends at S595). Intended entry path:
`corpus/knowledge/record-claim-integrity-r81.md`.

| Candidate | Draft disposition and reason | Located quote and access |
|---|---|---|
| `https://man7.org/linux/man-pages/man2/stat.2.html` | Admit narrowly: `st_mode` carries file type; the example distinguishes directory and regular-file cases. This grounds B6's type distinction, not the lane's policy for grading directories. | Access 2026-11-04. HISTORY, fetched HTML lines 234–236: “lstat() on a symbolic link need return valid information only in the st_size field and the file type of the st_mode field” (22 words). |
| `https://docs.python.org/3/library/os.html#os.DirEntry.is_dir` | Admit narrowly: the directory predicate follows symlinks by default; listing/name presence alone is not regular-file proof. Same base URL already appears as S068 under another scope; reconcile the document-keyed scope before assigning another row. | Access 2026-11-04. `os.DirEntry.is_dir`, fetched HTML lines 3447–3448: “Return True if this entry is a directory or a symbolic link pointing to a directory” (16 words). Signature at line 3446 states `follow_symlinks=True`. |

Source fetching, HTTP status and final durable pin paths belong to
`.ufo/waves/round-81/w1/Mo81Sc02Source.md`; the quotes above were read from
that seat's fetched HTML during drafting. No source quote establishes a
passing counter or a correct record count. Reject the broader candidate
claim that either document proves the complete C1/C2 gates: neither
specifies the lane's record grammar or fixture verdicts. Flip condition:
a directly located source for the stronger statement, followed by a
separate Gate decision, not an inference from path type.

### R80 correction set — work items, not new external sources

| Item | Required correction and authority | Status in this draft |
|---|---|---|
| D80-1 | Replace the three Round-80 after-cell debts with the measured C1/C2/C3 values and measured revision; name the superseded declaration. `round-80-verifier-spotcheck.md:160-166`. | Work item; no closure claimed here. |
| D80-2 | Correct the capability evidence's `pointers=232` against its pinned command, name the supersession, and replace “integration re-run pending” / “integration re-run owned by L1” with measured-revision evidence. `round-80-verifier-spotcheck.md:167-174`. | Work item; 233 is the r80 landed receipt's value, not a prediction for a later tree. |
| D80-3 | Name superseded r80 shorthand “1 → 0”, “from 3 of 6”, “from 15 of 55”; preserve frozen bytes. The measured controls are survivors=2 and named=14/present=55/missing=41. Narrow the account of the second P-C1 conjunct to the receipt actually used. `round-80-verifier-spotcheck.md:175-182`. | Work item; no retroactive predicate amendment. |
| D80-4 | Name `97ce0c96c779278baa8e8bb45ade642f9fabf1e2` as the r80 after-receipt's measured revision, not final HEAD `44bc941a`; the closure describes subsequent changes as evidence-only. Alternatively retain a real tip-run receipt. `round-80-verifier-spotcheck.md:183-189`. | Work item; no unretained rerun is promoted to evidence. |

Conflict retained for adjudication: the r80 closure calls P-C1's entering
conjunct “unimplementable because the tool is absent at entering”; the
counter reviewer HIGH-2 (`Mo80R01Counter.md:62-68`) reports a later sweep
run against an entering export that finds the mismatch. These are different
execution models; neither changes the r80 frozen sentence. R81 avoids the
ambiguity by grading each revision's own exported bytes with the same
revision-agnostic keeper.

## Mistakes

| Class | Evidence pointer | Captured-by | Fix |
|---|---|---|---|
| Record incompleteness: three after-cells remained exactly `PENDING` at landed bytes while the report declared measured results | Entering `SCORECARD.md:4044,4048-4050`; `corpus/lessons/round-80-verifier-spotcheck.md:160-166`; retained after-receipt `.ufo/waves/round-80/evidence/after-r80.txt:1-63` | **none** — the r80 sweep graded pointers and tallies, not round-table cells; the non-author closure subsequently routed D80-1 | R81 `pending` arm plus the independent `count-c2` keeper; correct the cells with named measured-revision provenance. Fix is a target until the L1's landed receipt. |
| Counter trusts a summary against its own MISMATCH lines, repeated summaries, or later carrier rows (MEDIUM-7/8) | `.ufo/waves/round-80/w1/Mo80R01Counter.md:113-133`; r81 controls A2/A3/A4 | R80 counter reviewer's fixture A2, retained in the spotcheck's counter-review provenance; A3 and A4 expose the adjacent multiplicity arms | Parse all lines and all matching carrier rows; reject contradictory summaries or mismatch/summary disagreement. Add a selftest arm shown to fail on old code; the r81 entering control already records A2 expected unmet/got met. A passing repaired-arm execution is not asserted here. |
| Stale evidence count and unfinished-run wording survive beside the tool they describe | Entering `SCORECARD.md:4036`, `SKILL.md:1366`; `round-80-verifier-spotcheck.md:167-174` | R80 non-author closure D80-2; not the r80 pointer/tally sweep | Pinned numeric-claim comparison, named carrier correction and measured-revision wording; retain the capability row rather than deleting the claim. |
| Measured revision described as final tip | `round-80-verifier-spotcheck.md:183-189`; `.ufo/waves/round-80/evidence/after-r80.txt:2,49,61` names `97ce0c96` | R80 non-author closure D80-4 | State measured input and evidence-only successor separately; absence of a retained tip run is not a passed rerun. |

## Census

Before census: **368 source rows, exit 0, 35 tolerated W04 duplicate-URL
warnings**. Provenance: inherited entering-state evidence in
`corpus/lessons/round-80-verifier-spotcheck.md:197-198` and
`corpus/lessons/round-80.md:169-174`, not a fresh census by this seat.
The recorded census command is:

```text
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori
```

The recorded row-count command (run from the lane root) is:

```text
grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md
368
```

Exit 0 is not “no warnings”; W04 remains explicitly tolerated.

AFTER: filled by the L1 at landing

## Refusals

- **`merge/mori/` package:** first staged id S471 collides with the lane's
  registry, which already reaches S595. Adoption needs document-keyed
  renumbering, not append-by-id. Prior refusal records the r61 L0 and
  94/136 staged-id collisions (`corpus/lessons/round-79.md:24-26`);
  that is inherited evidence, not a fresh package census. No assimilation
  or operator clearance is claimed.
- **Over-broad source claim rejected:** neither `stat(2)` nor Python's
  DirEntry documentation proves record integrity, command/receipt
  semantic relevance, exhaustive fixture coverage, or the directory
  policy in the frozen contract. The admitted recommendation is limited
  to the located type/default statements. A separate scoped source and
  Gate decision would be needed to reverse this rejection.
- **Duplicate-as-new-coverage rejected:** Python's shared URL alone is
  not new ground; reconcile S068's existing scope and use a document-keyed
  row decision before claiming expansion.
- No host remediation, service/unit changes, credential work,
  orchestration takeover, scalar score increase, or passing after-state
  inferred from a contract-only assignment. The seven C1 fixtures and
  record-carrier C2 arms have the frozen contract's named limits; they
  are not a universal correctness or fleet-health guarantee.
