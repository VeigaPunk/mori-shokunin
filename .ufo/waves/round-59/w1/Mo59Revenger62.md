# Mo59Revenger62 — dead-seat reconstruction: how the wave settlement artifact records partial settlement

Seat: `Mo59Revenger62` (revenger, leaf) · wave `mori-r59-w1` (`round-59/w1`) · lane `mori-shokunin`.
Mode: read-only reconstruction of committed evidence. No production, corpus, registry, `SCORECARD.md`,
`LOG.md`, lesson or VCS write; no fleet or sibling-repo write; no subagent dispatch; no installs.
Scratch: `/fast/scratch/hyaku/mori-r59/Mo59Revenger62` (created with `mkdir -p`, `TMPDIR` set there,
removed before yield). Freeze `R = 60b3a76ad0524c8978cc51922940be1c8c388915`; entering
`E = 2b9f03975bfb6e508f35074ac8181ec8bf54e805`; lane HEAD while reporting `8ff344ff`.

## Verdict

**Counterexample found — but it does not kill C2.** A committed `w1-results.json` member
(`Mo55Rc14`, round 55) has **no report file and no serialized result**, yet the artifact and the frozen
C2 scanner both treat the wave as structurally complete (`SETTLEMENT_SCAN_OK`, `members == seats`,
`failures=[]`). Partial settlement for that wave is recorded **out of band**, in a different artifact
and schema (`mori-wave-settlement-v1`), not in the `*-results.json` that C2 validates. The frozen C2
predicate is exactly the structural one it measures and is **met**; what is falsified is the
tool docstring's stronger reading that a results file exists "when every seat of the wave settles"
(`tools/mori-settlement-scan.py:4-6`), and any downstream claim that `SETTLEMENT_SCAN_OK` means every
seat delivered.

## E1 — the dead seat, exact bytes

Committed artifact `.ufo/waves/round-55/w1-results.json`
(sha256 `2e5b0a0f94d1fa5b90b2804d370db87d25d5197fa65bc4f26441d939b8d9763b`, 197 729 bytes;
identical at `R`, at `E`, and at HEAD; copy `corpus/evidence/sources-r59/w1-results-r55.json` is
byte-equal).

Member at line 86, byte offset 13 737:

```
"name": "Mo55Rc14"            (line 86)
"agent": "critic"             (line 87)
"output": "Need claim hash map actual source entries and compare contexts. ... Yet ledger disposition holds as pointer"   (line 88)
"note": null                  (line 89)
```

- `output`: 1055 bytes, `sha256 = caa69518591b4e2261a5dde26170eb314aef4e24f9497b93f8ca4a87b87a41af`,
  **no newline**, does not parse as JSON, contains no verdict/vote token, ends mid-sentence without
  terminal punctuation. It is raw in-flight reasoning text, not a serialized seat result.
  [INFERENCE] the seat's stream was captured at death; the artifact records the capture, not a result.
- Report: frozen dispatch expects `.ufo/waves/round-55/w1/Mo55Rc14.md`
  (`.ufo/waves/round-55/w1-dispatch.json` → `taskCall.tasks[Mo55Rc14].task`, trailer
  `Report: write your scoped findings to .ufo/waves/round-55/w1/Mo55Rc14.md`). The file **does not
  exist**: `git ls-tree -r R -- .ufo/waves/round-55/w1/` lists 64 entries = 63 `.md` + `swarm-registry.json`,
  zero matching `Mo55Rc14`; `git log --all --oneline -- .ufo/waves/round-55/w1/Mo55Rc14.md` prints
  nothing (never added, never deleted). Working tree agrees: 63 `.md` for 64 member names, and
  `members_without_md = ['Mo55Rc14']`, `md_without_member = []`.

Frozen scanner over the five C2 real-scan files, run from the frozen bytes (`git show R:tools/mori-settlement-scan.py`
→ sha256 `4c04bf21…5ac9a9` = frozen PIN), all fetched at `R`:

```
$ python3 scan-frozen.py in/round-{54,55,56,57,58}/w1-results.json
SETTLEMENT_SCAN_OK   failures=[]
round-54 seats=74 members=74 empty_output=0 notes_nonnull=0
round-55 seats=64 members=64 empty_output=0 notes_nonnull=0
round-56 seats=64 members=64 empty_output=0 notes_nonnull=0
round-57 seats=64 members=64 empty_output=0 notes_nonnull=0
round-58 seats=64 members=64 empty_output=0 notes_nonnull=0
```

So the exact artifact the contract folds into the C2 real-scan arm is the artifact that carries the
dead seat, and the arm's expected verdict is produced with the dead seat inside it.

## E2 — how partial settlement is actually recorded

Four channels; only the last three say anything, and none is the C2 target:

| # | Channel | Record | Reach |
|---|---|---|---|
| 1 | `.ufo/waves/round-55/w1-results.json` (the C2 target) | 4-key member, `note:null`, non-JSON `output`; top level is only `lane, round, wave, seats, results` | No status field, no recovery counter, no report pointer, no free-text note. Partial state is recoverable **only** by attempting a JSON parse of `output` and joining to the dispatch trailer. |
| 2 | `.ufo/waves/round-58/evidence/w1-settlement.json` (schema `mori-wave-settlement-v1`, produced by `tools/mori-wave-settlement.py`) | wave `.ufo/waves/round-55/w1-dispatch.json` → `"state":"partial"`, `counts.missing=1`, `missing:["Mo55Rc14"]` (offset 212 602 / 213 543, line 1); totals: `states {partial:26, settled:36}`, `missing:391` of 3153 members | Explicit, per-seat, dispatch-derived — but post hoc (written in round 58) and, by the tool's own line 18, "A missing report is not a dead seat; this tool reports filesystem shape only." |
| 3 | `.ufo/waves/round-55/w1/Mo55Exec01.md:142,223` | "`Mo55Rc14` has written no report"; "C1 has 10 scoped rows with only one settled RECHECK voter … `MIN_VOTES=2`, so these 10 rows cannot satisfy the vote arm" | Sibling prose only; discovered in-wave by another seat, not by the artifact. |
| 4 | `corpus/lessons/round-58-verifier-spotcheck.md:46` | "64 `output` entries … all nonempty; 58 `w1/*.md` report files present; `evidence/w1-settlement.json` state `partial`" | Honest prose restatement; conflates "nonempty" with "delivered". |

The decisive contrast is r53, the wave that *did* record partial settlement in-band:

```
r53 top level: seats 67 (line 5), spawned 67 (line 6), outputs_recovered 66 (line 7),
               settled_by "orchestrator session exit (no seat live)" (line 8), note <kill narrative>
dead member  : line 187 {output: null, note: "spawned as job Mo53RevLedgerProse; still running at the
               session exit and killed - no output delivered", report_file: null}
```

r54 replaced that shape with `{name, agent, output, note}` only (`MEMBER_KEYS`,
`tools/mori-settlement-scan.py:41`); `report_file` and every recovery counter disappeared, and `note`
went null in all 74+64+64+64+64 members of r54–r58 (`notes_nonnull=0` in every scan above). Net effect:
the schema change removed the only in-band channel that distinguishes "seat delivered" from "session
captured a fragment", replacing it with a member record that is structurally indistinguishable from a
settled one.

## E3 — bounded census (receipt), cross-checked against the lane's own tool

Method: for each of r53–r58, take every `results` member, resolve its frozen dispatch `Report:` trailer
path, test existence on disk; separately count members whose `output` is not JSON. Read-only.

```
wave  members  result_names  dispatch_names  missing_reports
r53      67         67             67        ['Mo53RevLedgerProse']
r54      74         74             74        ['Mo54RevC1Counter']
r55      64         64             64        ['Mo55Rc14']
r56      64         64             64        []
r57      64         64             64        ['Mo57Reviewer15','Mo57MutationTester37']
r58      64         64             64        ['Mo58Reviewer10','Mo58Reviewer15','Mo58Reviewer19',
                                              'Mo58Critic31','Mo58Executor41','Mo58Executor47']
```

11 missing reports over six waves; **every** missing name is also a non-JSON-`output` member, and 2 of
the 13 non-JSON members (r58 `Mo58MutationTester40`, `Mo58Executor48`) have reports, so non-JSON output
is necessary but not sufficient for a dead seat. This receipt agrees exactly, wave by wave, with
`w1-settlement.json` (`missing` 1/1/1/0/2/6, `state partial` for r53/r54/r55/r57/r58, `settled` for r56)
— an independent confirmation that the missing-report set is real, not a path-resolution artifact.

Verdict correlation: r54–r58 scan `OK`; r53 scans `FAIL` **solely** because its members carry
`report_file` (`member[i]:extra_keys=report_file`, 67 occurrences). So `SETTLEMENT_SCAN_OK` is
uncorrelated with report completeness, and the one file that encodes report linkage is the file the
contract requires to fail.

## E4 — falsification probes (scratch only, no lane bytes touched)

Frozen scanner, copies built in scratch:

- **P-A:** r55 with `Mo55Rc14.output = null` → `SETTLEMENT_SCAN_OK`, `failures=[]`, `empty_output=1`.
  The scanner *reports* empty output but does not treat it as failure (`empties += 1` at lines 94/98
  with no `fails.append`), so a seat with no output at all still yields the contract's target verdict.
- **P-B:** r55 with 3 members removed and `seats` rewritten to 61 → `SETTLEMENT_SCAN_OK`, `failures=[]`,
  `seats=61 members=61`. `members==seats` is self-referential — both numbers come from the same
  orchestrator write — and is never joined to `w1-dispatch.json` (`registry.members` = 64 names), which
  is on disk and would expose the loss.

Bounds: P-B is a synthetic probe of the predicate, not evidence that any committed file lost members;
no committed artifact shows a name-set mismatch with its dispatch (all six waves: 67/74/64/64/64/64
result names vs 67/74/64/64/64/64 dispatch names, no unmatched names either direction).

## Divergences

- **D1 (docstring overreach, medium).** `tools/mori-settlement-scan.py:4-6` states the file is "written
  beside `<wave>-dispatch.json` when every seat of the wave settles". Falsified by r54, r55, r57, r58:
  each has a committed results file while the lane's own `mori-wave-settlement-v1` classifies the wave
  `partial` with missing reports. The frozen C2 claim sentence does not inherit this sentence (it
  enumerates only structural checks), so this is a documentation/capability-boundary defect, not a
  frozen-claim counterexample.
- **D2 (arm selects for the defect, medium).** The C2 real-scan arm requires r54–r58 to be `OK`; four of
  those five are `partial` waves carrying 10 dead seats. The arm therefore *requires* tolerant behaviour
  on exactly the class being reasoned about, and cannot detect a regression that starts labelling dead
  seats as failures.
- **D3 (schema drift removed the witness, high for downstream use).** r53's `report_file` + `outputs_recovered`
  + populated `note` is the only in-band partial-settlement record in the family; r54 dropped it, and
  the drift arm classifies its presence as drift-to-be-reported. The C2 entry must not cite the r53
  `FAIL` as evidence that the current shape is the more audited one.
- **D4 (hostile-tree coverage hole, low).** The 12 frozen `trees-c2` trees model entry-grammar and row
  defects; none models a dead-seat member (non-JSON/no report). Adding one is out of scope now
  (frozen artifacts), but the gap should be recorded for a future round rather than papered over.

## What this permits the round-59 C2 entry to claim

Safe: `mori-settlement-scan.py` validates the enumerated structural shape; the five r54–r58 files
validate; r53 fails on `report_file` extra keys; `members==seats` is a self-consistency check confined
to the file itself.

Unsafe (would be false on committed bytes): "the five files prove every seat settled"; "`seats` counts
delivered results"; "a passing scan means no seat died"; "the scanner checks report presence"; citing
`w1-settlement.json`'s `partial`/`missing` semantics as produced or implied by the C2 tool (different
tool, different schema, dispatch-derived).

## Method bounds and confidence

Read-only: `git show` at `R`/`E`, `git ls-tree`, `git log --all`, `json` load of six results files, one
dispatch/registry file, one settlement census; frozen scanner executed from a scratch copy of its
frozen bytes. No lane working-tree writes, no fixture repos, no VCS mutation, no pacman, no installs.
Confidence: **high** on every quoted byte, name, count and offset (recomputed twice); **medium** on the
r58 census's `missing` definition matching mine (it agrees 6/6 waves, but its line 18 disclaims
dead-seat semantics, so I use it only as an existence cross-check); **[INFERENCE]** on seat-death
causation — the artifacts record a truncated stream and an absent report, not a reason.

Scratch `/fast/scratch/hyaku/mori-r59/Mo59Revenger62` removed before yield; no receipt larger than the
numbers above was needed.
