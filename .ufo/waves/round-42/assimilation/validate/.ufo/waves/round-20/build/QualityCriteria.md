# QualityCriteria: candidate criteria 64-66 (round 20)

Seat: MoriR20.QualityCriteria (leaf; no subagents; no edits outside this report).
Inputs read: corpus/QUALITY.md (criteria 1-63, all lines); corpus/lessons/round-19.md (all); .ufo/waves/round-20/contract.md (frozen; read first); the round-19 wave ledgers, settlement files and commit history; the round-12 to round-20 drift records named below. Times are UTC unless marked; the lane's local offset is -03:00.

## 1. Summary

- Proposed: **64** (wave-boundary settlement receipt; gap a), **65** (a drift result is cited as freshness only from the citing round's own run; gap b), **66** (a red drift result is dispositioned in the round that observes it; gap b). Each has an exact failing predicate (section 3) and a retrospective test on lane records. The tests check the proposals; they are not historical defect findings (criteria 57-58).
- Premise (a) confirmed. Wave 1 = 64 tasks: 16 present, 48 missing = 8 known provider failures + 1 cancellation + 39 no cause established. The tree already held the 16 reports at 08:47:35. The first committed settlement record is at 09:18:08, 28 min 39 s after wave 2 started (08:49:29.759864), and it has no time field.
- Premise (b) partly wrong. The baseline was red and unpinned for nine rounds (12-20), as the premise says. It was not re-observed in every round. Own exit-1 runs exist for rounds 12, 13, 14, 15 and 20. Rounds 16-19 carried the recorded red without a run: 16 and 17 cite the round-15 receipt or carry it in prose; 18 and 19 carry it by text only. contract.md:12-14 needs an append-only erratum (section 5).

## 2. Evidence for gap (a)

Timeline (commit times are committer time; author time is equal except where marked):

| UTC | Event | Source |
|---|---|---|
| 08:05:28 | wave-1 registry created, 64 members | .ufo/waves/round-19/wave1-record.json (stdout JSON, createdAt) |
| 08:18:42 | last wave-1 registry update | same file, updatedAt |
| 08:19:14-08:26:14 | the 16 present report files written (mtime range) | stat on .ufo/waves/round-19/build/*.md |
| 08:20:37 | commit 7d949b4: wave-1 attempts, record, taskcall; no settlement | git log |
| 08:47:35 | commit 367927c ("integrate content review ..."): tree holds 16 of 64 trailer paths | git log; git cat-file on each trailer path |
| 08:49:04 | commit 7fa136f: wave-2 plan and run | git log |
| 08:49:29.759864 | wave-2 started row, 70 tasks | .ufo/waves/round-19/wave2-attempts.json:4, 9, 11 |
| 09:18:08 | commit a4f79dd ("settle falsification ..."): first wave-1 settlement (16/8/1/39); wave-2 attempts row first committed | git log; wave1-settlement.json |
| 09:31:22 (author) / 09:38:23 (committer) | commit 2061780: wave-2 settlement (48/22); lane tip | git log |
| 10:15:02 | MANIFEST closed_at, mori round 19 | MANIFEST.json:10169 |

Observed facts:

- Wave 1, recounted from the 64 `Report:` trailers in .ufo/waves/round-19/wave1-run.json (taskCall.tasks[].task): 16 present, 48 missing, 0 empty, 0 unsafe, 0 unparsed. The present set equals `reports_present` in wave1-settlement.json exactly. The same 16/48 split holds in tree 367927c.
- Wave 2, recounted at tip 2061780: 48 present, 22 missing, of 70. Matches wave2-settlement.json (48 reports, 22 provider failures).
- No commit at any ref contains any of the 48 missing wave-1 paths. `git log --all --diff-filter=D` shows no deletion under .ufo/waves/round-19/build/.
- Neither settlement file carries a time or the dispatch payload SHA-256. Top-level keys of wave1-settlement.json: schema, wave, returned_agent_ids, native_calls, reports_present, known_provider_failed, known_cancelled, no_report_terminal_cause_unestablished, error_classes, replacements, limits. wave2-settlement.json has the same pattern with provider_failed_no_report and slot_released.
- wave1-attempts.json has no `at` field and uses `state` rather than `result`; MANIFEST.json:10171 already calls this ledger nonconformant.
- bc093c8 is a jj keep-ref predecessor (refs/jj/keep/bc093c8...) carrying the same 16 paths. It is not an ancestor of the tip. The lineage commit is 367927c. Criterion 47 applies to this distinction.
- MANIFEST.json:10171: "W1 64 returned IDs,16 reports,8 known provider failures,1 cancellation,39 unknown no-report causes (not successful reviews/deaths inferred); W2 70 returned IDs,48 reports,22 provider failures". The closure figures match the settlement files.

Interpretation:

- The 16/48 partition was determinable from the committed tree at 08:47:35, 114 s before the wave-2 started row. No committed settlement record existed before 09:18:08, and that record carries no time.
- Whether an uncommitted pre-boundary count existed is [UNKNOWN]. The lane records none.
- The round-19 lesson files the gap under "Recovery interruption and evidence gaps" (corpus/lessons/round-19.md:104-113), not in its M1-M9 tables. No mistake id or criterion points at it. contract.md:51-54 records the 48 as "found only by hand at recovery and closure."
- The phrase "not counted until closure" is accurate only in this sense: the first committed count is the closure-phase settlement commit a4f79dd, about 57 min before the MANIFEST closure record.

## 3. Proposed criteria (ready to append as "Criteria added round 20", after admission)

Terms used below:
- boundary(W): the earliest of (i) the `at` of the first started row of any later wave in the same round, or (ii) for the round's last wave, the first lesson, MANIFEST, SCORECARD or report sentence that states W's report or review count.
- round window: from the entering tip's committer time to the round's closure record.
- own run: a `--drift` invocation recorded by the citing round, with the receipt fields named in 65.
- counting command: the C1 command in contract.md:36-41, applied to a receipt's captured stdout (`jq -r .stdout RECEIPT`) and to the register.

**64. A wave's settlement is recorded at its boundary, not first at closure.** For each dispatched wave W, a committed boundary receipt exists whose `observed_at` end is no later than boundary(W). The receipt (a) binds W's dispatch payload by SHA-256 and states the ledger's `tasks_count`; (b) records `observed_at` as a UTC start and end at second precision, each recorded or bounded by a named launch or completion record, plus the lane head observed then (criterion 33); (c) partitions `tasks_count` into present, empty, missing, unsafe and unparsed, and partitions the missing set into recorded classes (provider-failed with its error class, cancelled, cause-not-established, or another named class); (d) never calls a missing member dead, failed or killed unless that member's provider terminal cause is recorded. ← corpus/lessons/round-19.md:104-113 ("Missing reports are missing evidence, not successful reviews or inferred provider deaths"); .ufo/waves/round-19/wave2-attempts.json:4, 9; contract.md:49-54, 82-86; criteria 22, 33, 44, 48, 53, 56.

Fails when any of:
- F1: no committed receipt for W has an `observed_at` end <= boundary(W). A receipt without `observed_at` never qualifies.
- F2: present + empty + missing + unsafe + unparsed != `tasks_count`; or `tasks_count` != the count of `taskCall.tasks[]` names; or the missing classes do not sum to missing.
- F3: a sentence calls W complete, settled or "N reviews" while missing > 0 and N != present.
- F4: a missing member is called dead, failed or killed with no recorded terminal cause.
- F5: the receipt lacks the dispatch payload SHA-256 or the observed lane head.

Round-19 retrospective:
- Wave 1: F1 fails (no committed receipt with a time <= 08:49:29.759864; the earliest committed settlement, a4f79dd at 09:18:08, has no time). F5 fails (wave1-settlement.json carries no SHA-256 or head). F2 passes (16+8+1+39 = 64 = 64 names). F3 passes (MANIFEST.json:10171 gives the partition and does not say "complete"). F4 passes (the record says "not successful reviews/deaths inferred").
- Wave 2: F1 fails (no time in wave2-settlement.json at any point before the closure record at 10:15:02). F5 fails. F2 passes (48+22 = 70 = 70 names). F3 and F4 pass.

Design consequence (for L1, not an edit to C2): C2's frozen output must be byte-identical across runs and carries no time (contract.md:82-86). `observed_at` and the lane head therefore belong in a wrapper receipt that embeds the tool stdout's SHA-256. Without that wrapper, F1 and F5 fail by construction.

Not claimed: that the 48 would have been reviews; that the C2 tool exists or is correct; that the missing reports caused any content defect.

**65. A drift result is cited as the current freshness state only from the citing round's own run.** A round may hold or improve its freshness score, and its freshness evidence may state a current red or clean state, only on a `--drift` receipt that the same round produced and that carries: `command` (naming the baseline), `rc`, `observed_at` (UTC start and end, second precision), `measured_commit`, `census_sha256`, `token_count` and `unclassified_count`. This is the shape of .ufo/waves/round-20/evidence/c1-drift-entering.json. A receipt from an earlier round may be cited, labelled with its own round and commit, and establishes only that earlier state. A round without its own run writes "not observed this round" in the freshness evidence cell and does not count the score as held. ← corpus/QUALITY.md:104 (criterion 41: a green gate never establishes freshness); :40-43 (criteria 20-21: the verdict vocabulary, and qualifications in the evidence cell, where the carry sat); :44-45 (criterion 22); corpus/lessons/round-12.md:38 (M15); corpus/knowledge/drift-pin-r10.md:241-243 (section 5.2: the first measurement of each round is `--drift`).

Fails when any of:
- F1: a freshness score is held or improved, or the freshness evidence states a current red or clean state, and the round window holds no receipt with the fields above.
- F2: a round cites another round's receipt as its own observation.
- F3: `observed_at` has no start second.

Round tests (retrospective):
- Rounds 12-15 pass on substance, though their field names predate this schema: corpus/evidence/drift-r12-20261019T2204Z-classification.md (observation 2026-10-19T22:03:56Z, rc 1); .ufo/waves/round-13/evidence/drift-retained-baseline.json (exit 1, measured_commit c13df48, started_utc); .ufo/waves/round-14/evidence/drift-current.json (exit 1, captured_utc); .ufo/waves/round-15/evidence/drift-current.json (exit 1, generated_utc 2026-10-20T08:23:07Z, per .ufo/waves/round-16/build/DriftDebt.md:18).
- Round 16 fails F1 and F2. The freshness row reads "unchanged | 5 held" (SCORECARD.md:982). It rests on the round-15 receipt: .ufo/waves/round-16/build/ClaimRubric.md:179 reads "exit 1 (red), unchanged ... r15 drift-current.json". .ufo/waves/round-16/build/DriftDebt.md:1 is titled "why this round neither reruns nor re-pins it".
- Round 17 fails F1. "5 held" (SCORECARD.md:1116); "r10 redness is carried without a new live drift run or re-pin" (LOG.md:1262-1263).
- Round 18 fails F1. "freshness ... unchanged 6/5/5 held ... r10 drift red carried, no repin" (SCORECARD.md:1148). No `--drift` text appears under .ufo/waves/round-18/.
- Round 19 fails F1. "freshness | 5 | unchanged | recorded r10 red retained, not re-pinned or re-evaluated as green" (SCORECARD.md:1218). No `--drift` text appears under .ufo/waves/round-19/. Its census-named files are sources-census outputs (evidence/census-start.txt, evidence/census-end-command.json).
- Round 20 (entering tip 2061780) fails F3 as written. The receipt's `observed_at` reads "2026-10-21, L1 background job bg_207 after the 07:18:05-03 launch; exact start second not recorded; wall 103.98 s". The launch is 10:18:05Z. One recorded field fixes this; the receipt is the L1's to amend.

Not claimed: that rounds 16-19 hid a regression; that a fresh run would change any verdict; that the census must run each round to score other axes.

**66. A red drift result is dispositioned in the round that observes it; carrying it is at most one deferral.** For baseline B, a round whose own receipt has `rc` != 0 records:
(i) classification coverage: the counting command returns 0 over that round's captured stdout against the round's register; every classification names one class from `census-schema-change | roster-change | live-state | census-regression` and carries an evidence pointer; and
(ii) exactly one disposition: `re-pin` (a new baseline at the measured commit, a recorded reason, and a semantic review naming what changed and why the new pin is correct, with zero `census-regression` tokens); `route` (a named finding with owner and due round, itself subject to this criterion in its due round); or `retire` (the baseline withdrawn with a reason, and the replacement or its absence stated).
The first red round may defer once, with a named due round. "Red retained", "carried", "no re-pin" and "planned" are not dispositions. Criteria 10 and 41 still reject a re-pin that only turns red green; this criterion requires a decision, not a re-pin. ← corpus/QUALITY.md:19 (criterion 10); :104 (criterion 41's "stays carried debt", narrowed here to one deferral); corpus/knowledge/drift-pin-r10.md:241-248 (sections 5.2-5.3: a red result "either explains an intended change (then re-pin ...) or is a regression the round must address"); contract.md:19-34 (the C1 path as a compliant example).

Fails when any of:
- F1: `rc` != 0, and the counting command over the round's captured stdout is != 0.
- F2: `rc` != 0, and no disposition of type (ii) is recorded.
- F3: a deferral names due round D, and round D or any later admitted round records no disposition for B.
- F4: a `Planned` drift item has no due round.

Round tests (retrospective):
- Round 12: rc 1; 11 tokens classified (corpus/evidence/drift-r12-20261019T2204Z-classification.md); "No re-pin (planned r13)" (LOG.md:669-673). First deferral, due round 13: passes.
- Round 13: coverage passes (.ufo/waves/round-13/evidence/drift-classification.json: `unclassified: []`, 42 tokens, measured_commit c13df48). No disposition: verdict "red retained; categories are not a regression-free proof; no re-pin" (same file; LOG.md:754; SCORECARD.md:694). F3 fails at due round 13. The planned re-pin (SCORECARD.md:641-643) was not executed. This is the earliest round the criterion would have failed.
- Round 14: rc 1 (.ufo/waves/round-14/evidence/drift-current.json); "no re-pin" (SCORECARD.md:791). F2 and F3 fail.
- Round 15: rc 1 (.ufo/waves/round-15/evidence/drift-current.json); "is not re-pinned" (corpus/lessons/round-15-verifier-spotcheck.md:161; SCORECARD.md:873). F2 and F3 fail.
- Rounds 16-19: no own run, so F2 is not reached. F3 fails each round, with no disposition recorded (LOG.md:1052-1056, 1262-1263; SCORECARD.md:982, 1116, 1148, 1218).
- Round 20 (entering): rc 1, token_count 50, unclassified_count 8 (.ufo/waves/round-20/evidence/c1-drift-entering.json). F1 fails until the register reaches 0. I reproduced the 8 from the captured stdout against the round-13 register (section 9). The C1 path (contract.md:19-34: register, zero census-regression, re-pin with review, re-run, record) satisfies F1-F3 when it lands.

Not claimed: that red must be re-pinned; that a route may be deferred indefinitely (each route has a due round); that any red token is a regression.

Scope note: 65 and 66 narrow criterion 41 by appended text. They do not edit 41 (criterion 4).

## 4. Existing criteria checked: why 1-63 do not already catch (a) or (b)

| Criterion | What it covers | Why it does not catch the gap |
|---|---|---|
| 9 | adopted baseline must resolve or be explicitly superseded | resolution, not age (b) |
| 10 | baseline declares its volatile set; re-pin is a recorded act with a reason | no clock; "not re-pinned" with a reason passes (b) |
| 20 | tally cites the counted universe recomputed from artifacts at the carrying commit | a closure-time recount satisfies it; silent on when the count was taken (a) |
| 21 | four verdict values; qualifications live in the evidence cell | "unchanged" with "carried" in the evidence cell is compliant (b) |
| 41 | a green gate never establishes freshness; red stays carried debt | the permission that let the carry run; no clock (b) |
| 44 | CONTEXT_OK receipt before each dispatch | spec text, not predecessor settlement (a) |
| 48 | missing and transcript classes are observations, not deaths | supports 64(d); sets no boundary (a) |
| 53, 56 | dispatch rows and ledgers | ledger only; wave-1 ledger nonconformant (MANIFEST.json:10171) but no criterion ties a settlement to the next started row (a) |
| 54 | carried procedural defects keep their disposition | names the disposition, sets no due round (b) |

## 5. Premise check for gap (b)

| Round | Own `--drift` run this round | Evidence | Lane text |
|---|---|---|---|
| 11 | exit 0 | corpus/knowledge/audit-r11.md:74, 133-134 | SCORECARD.md:568 "baseline still clean" |
| 12 | exit 1 | LOG.md:558-562; drift-r12 classification file | LOG.md:673 "No re-pin (planned r13)" |
| 13 | exit 1 at c13df48 | .ufo/waves/round-13/evidence/drift-retained-baseline.json | LOG.md:754 "not re-pinned" |
| 14 | exit 1 | .ufo/waves/round-14/evidence/drift-current.json | SCORECARD.md:791 "no re-pin" |
| 15 | exit 1 | .ufo/waves/round-15/evidence/drift-current.json | LOG.md:945-946 "not re-pinned" |
| 16 | no; cites the round-15 receipt | .ufo/waves/round-16/build/ClaimRubric.md:179; DriftDebt.md:1, 15-18 | LOG.md:1052-1056 "neither re-run ... nor re-pinned" |
| 17 | no | none | LOG.md:1262-1263 "carried without a new live drift run" |
| 18 | no | no `--drift` text under .ufo/waves/round-18/ | SCORECARD.md:1148 "r10 drift red carried, no repin" |
| 19 | no | no `--drift` text under .ufo/waves/round-19/ | SCORECARD.md:1218 "recorded r10 red retained" |
| 20 | yes, entering tip; rc 1; 8 of 50 unclassified | .ufo/waves/round-20/evidence/c1-drift-entering.json | contract.md:19-21 |

Result: nine red, unpinned rounds (12-20). Own exit-1 runs in five (12, 13, 14, 15, 20). Four rounds (16-19) without an own run. The premise "every round re-observed exit 1" is not supported for rounds 16-19. The record supports "carried red without re-observation" for those rounds, which is the failure 65 names.

## 6. Rejected candidates (criterion 5)

- R1 "Re-pin each red round so the round is clean." Rejected: turns red green (criteria 10 and 41; drift-pin-r10.md:244).
- R2 "Treat missing reports as dead after K rounds." Rejected: contradicts round-19.md:110-112 and criterion 48.
- R3 "Put `observed_at` into C2's own output." Rejected: C2 output must be byte-identical (contract.md:85-86). Use a wrapper (64).
- R4 "Extend criterion 20 to cover timing." Rejected as an edit to an admitted criterion (criterion 4). 64 is a new criterion.
- R5 "A numeric carry limit K." Rejected as arbitrary. "One deferral" is the minimal clock and is checkable.
- R6 "Wave 2 depended on the missing wave-1 reports." Not proposed. No wave-2 payload path cites a missing wave-1 report by name (checked against wave2-run.json and wave2-spec.json). Dependence is [UNKNOWN].

## 7. Design notes for L1 (not edits)

1. Erratum, append-only (criterion 4), for contract.md:12-14: rounds 16-19 did not re-observe exit 1 (section 5). The "unpinned for nine rounds" statement stands.
2. C2: carry `observed_at` and the lane head in a wrapper receipt that embeds the tool stdout SHA-256 (64).
3. The round-20 entering receipt: record the start second in `observed_at` (65 F3).
4. Criterion 41 ("stays carried debt") conflicts with drift-pin-r10.md section 5.2 ("explain then re-pin, or address the regression"). 66 resolves toward section 5.2 and adds a one-round clock. Narrow 41 by appended text.
5. The round-19 gap has no mistake id. 64 should cite round-19.md:104-113 as its source.
6. Wording: SCORECARD.md:1135 (round 18) reads "15 dead on provider capacity" for missing wave members. 64(d) and F4 forbid "dead" without a recorded terminal cause.
7. Outside the lane, for the skills owners: `skill://swarm` (Lane shape section) says later waves are dispatched after earlier waves but states no settlement predicate. The lane's SKILL.md:16 and :28 describe settled and unsettled waves as a measurement with no boundary gate.

## 8. Limits and unobserved items

- [UNKNOWN] whether an uncommitted, pre-boundary count existed. The lane records none before a4f79dd (09:18:08).
- [UNKNOWN] the recovery timing. corpus/lessons/round-19.md:104-108 is untimed.
- [INFERENCE] the 48 missing wave-1 paths were never on disk at the boundary. Established instead: they are absent from tree 367927c and from every commit at every ref.
- Round-18 and round-19 `--drift` absence was checked by text search under `.ufo/waves/round-18/` and `round-19/`. A run recorded only under a non-drift filename without the command text would be missed. Residual risk is low, [UNKNOWN].
- File mtimes are used only as an ordering aid beside commit times.
- Retrospective tests use the proposed criteria. They do not assert historical violations (criteria 57-58).

## 9. Checks run and disclosures

- Read-only commands only: git (`log`, `show`, `cat-file`, `ls-tree`, `for-each-ref`, `merge-base`, all with `--no-optional-locks`), jq, stat, grep, comm, awk, sed. No census run (`tools/mori-census.sh` not executed), no build, lint, pin or test run, and no edit outside this report.
- Reproduced from captured data (observed): the counting command over `.ufo/waves/round-20/evidence/c1-drift-entering.json` stdout against the round-13 register returns 8, with 50 tokens in the captured set. This matches contract.md:43-45.
- Reproduced (observed): wave 1 16 present / 48 missing, both at tree 367927c and at tip; wave 2 48 present / 22 missing at tip.
- Scratch files written by this seat and removed: /tmp/__qc_w1_trailers.tsv, /tmp/.qc_scratch_w1, /tmp/.qc_scratch_w2. They are not evidence (criteria 38, 45). Confirmed absent afterwards.
- Tool installs or updates: none. jq, git and coreutils were already present.
- Subagents: none.

## 10. Checks the main agent should run after integration

- The counting command over the final round-20 register; expect 0 (contract.md:43-45).
- The C2 live demonstration; expect wave 1 partial at 16 of 64 and wave 2 partial at 48 of 70, matching the counts in section 2 (contract.md:95-98).
- The frozen oracle and selftest, as the contract states. This seat did not run them.
