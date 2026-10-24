measured 2026-10-23T18:57:52Z

# CritAdmission — whole-round admission dry run

Seat: `mori-r36-w2-CritAdmission-25` (critic, leaf).
Item attacked: the inference that successful C1/C2 counter receipts, source-census success and a large swarm suffice to admit round 36.
Scope: delivered data revision `bf0df77fee4b6ef54a90aea09335c7617f125151` (R), entering revision `6bd57097` (B), and explicitly identified live evidence. Historical blobs and live repairs are distinguished below. This is a recommendation, not a canonical Rust judgment; no judge/runtime, counter, self-test, live fetch, git/jj mutation, remediation or signal was invoked by this seat. Only this report was written. No tools installed or updated.

## Axes and strongest counterexample

- C1: **freshness technique**, exploratory; neither semantic freshness nor a measured freshness-score gain.
- C2: **operability**, measured acquisition of the registered SOURCES history gate and deletion operation.
- Guard axes: **calibration** (receipt versus admission honesty), **depth** (accurate documentation), **adjacency** (detection/report-only scope). No coverage gain, saturation, retirement or score increment follows automatically from a counter token.

The strongest actual counterexample is the round itself: both byte/behavior predicates return `met`, yet the inspected record contains no qualifying named outside judgment of C1. Canonical assignment `.ufo/prompts/mori-round-36.md:29-40` requires that judgment; canonical `AXES.md:43-51` expressly excludes dispatched subagents. The live contract also retains this requirement (`contract.md:128-129`). Technical reviewers in this wave are not a substitute, including when Main physically dispatches the lane-authored payload (`dispatch-log.txt:33-34`).

Thus even granting **no axis harm**, `C2_verified AND C1_verified AND no_harm` is false at this evidence snapshot. More seeds, rejected controls, source rows or successful reviewer checks cannot repair the missing conjunct.

**Exact dry-run recommendation:** retain C2's measured success; land C1 as **unprovable**, with its `C1=met` receipt labeled byte-behavior evidence only; recommend **admitted=false / rejected-honest-stop**. Do not rename C1, drop it after data, or treat “exploratory” as exempt from verification. A genuinely outside named reviewer could supply the missing reasoned `unprovable-but-better` judgment, but no such judgment was found in the inspected record. This report does not supply one. Report status is conditional on a substantive committed final report; an in-flight missing report is not itself a fabricated `failed` closure.

## Claim-by-claim assembly

These are **archived observations, not runs by this seat**. Paths below are under `.ufo/waves/round-36/` unless stated otherwise. Commands are the recorded counting commands at their measured revisions.

| Claim | Command / evidence | Observed output | What it supports |
|---|---|---|---|
| C2 before | `python3 .ufo/waves/round-36/count-c2.py 6bd57097`; `evidence/c2-before.txt:1-5` | `tool_absent`, `C2=unmet`, `EXIT=1` | Operation absent before round. |
| C2 after | `python3 .ufo/waves/round-36/count-c2.py bf0df77fee4b6ef54a90aea09335c7617f125151`; `evidence/c2-after.txt:1-9`, `dispatch-log.txt:28-29` | blind `24/24`, real arm `pass`, identical tool/oracle summaries, `C2=met`, seed `15440749816798970567` | Frozen P-C2 met at R; not every possible git-history edge proved. |
| C1 before | `python3 .ufo/waves/round-36/count-c1.py 6bd57097`; `evidence/c1-before.txt:1-4` | `tool_absent`, `C1=unmet`, `EXIT=1` | Probe absent before round. |
| C1 byte evidence after | `python3 .ufo/waves/round-36/count-c1.py bf0df77fee4b6ef54a90aea09335c7617f125151`; `evidence/c1-after.txt:1-6` | `blind_rows=40 ... mismatches=0`; real `oracle_fetched=58 oracle_fresh=49 oracle_drifted=9 oracle_excluded=0 ... mismatches=0`; `C1=met`, seed `7388485190103051243`, `C1_EXIT=0` | P-C1 byte behavior only. C1's exploratory admission remains unprovable without outside judgment. |

Counter identity was checked directly with command `sha256sum .ufo/waves/round-36/count-c1.py .ufo/waves/round-36/count-c2.py`. Observed:
```
86dd3b7ab2d2563bbc811e83717b35dfea3d69717dab4d41d454f8b87c8764c0  .ufo/waves/round-36/count-c1.py
c7edaacfff029c2055bee6ddda42ff6f5c040dad7fbac81e9d169602edcbac34  .ufo/waves/round-36/count-c2.py
```
These match `evidence/freeze-v2.txt:3-4`. `read(evidence/c0-rescore-v2.txt:1-28,1147-1172)` and the targeted verdict sweep `^C[12]=(met|unmet)$|^== [JK]|^EXIT=` show the committed negative-control outcomes and positive references: all J/K entries are `unmet`/`EXIT=1`, REF1/REF2 are `met`/`EXIT=0`. This is useful discrimination evidence, not an outside exploratory judgment.

## Trend-proof obligations

### 1. End census: behavioral evidence present; final durability still owed

Recorded command, `w2/ExecCensusEnd.md:23-50`:
```
bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori; echo "EXIT=$?"
```
Observed there: `mori ok /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md`, `EXIT=0`, with W04 warnings; the new warnings name S218 and S220. The complete output is in that report. Start receipt `evidence/census-start.txt:14-15` also records `mori ok`, `EXIT=0` for the same census command (`dispatch-log.txt:3`). W04 superseder warnings are not E-errors or demonstrated axis harm.

This supplies a real end-census observation for the data-era tree. It is **not evidence for a later edited final tree**: S205's used-by has since changed in the live file, and further lane work is in flight. The final end census and both outputs must be durably attached to the final delivered bytes, per canonical assignment `:54-66`; do not relabel the earlier run as a later measurement. No census rerun was performed by this critic.

### 2. Opened source: substantive grounding present, final source bookkeeping incomplete at R

`git -C /home/vgpnk/Projects/shokunin/mori-shokunin diff --unified=0 6bd57097 bf0df77fee4b6ef54a90aea09335c7617f125151 -- corpus/SOURCES.md` observed **16 insertions, 0 deletions**, including S205 at `corpus/SOURCES.md:211`. S205 names the pinned fleet CORPUS commit, `opened=2026-10-23`, and the append-only/recheck anchors. `read(corpus/evidence/sources-r36/S205.src:101-121)` directly shows the recheck definition and rule 2. `w1/SrcCorpus.md:6-14,22-23` carries its fetch command, digest, access date and located quotes; `w2/RevSupS205.md:7-26` records a fresh matching-body check.

C2's tool explicitly implements that rule (`tools/mori-sources-appendonly.py:2,8-11`); `contract.md:16-17` grounds both claims in that pinned document. The landed knowledge entry explicitly cites **S205** at `corpus/knowledge/source-drift-r36.md:1`. Therefore this is not sourceless fixture work, and at least one round claim has an actual S205-citing landed entry. The final C2 evidence/lesson should make the `C2 → S205 → rule 2` linkage explicit rather than relying on the contract's still-unassigned-row prose.

At R, however, `corpus/lessons/round-36.md` is absent, so its required Gate and Mistakes record are not landed. S205's landed used-by also names a tool rather than the citing knowledge entry (`w2/RevKnowledgeDrift.md:103-116`). The live used-by now names `corpus/knowledge/source-drift-r36.md` (`read(corpus/SOURCES.md:211:raw)`); this is a pending repair, not historical proof at R. Record its old→new change when landing it. A green census checks existence, not citation directionality (`w2/RevCensusRows.md:99`).

## L2 floor and wave conformance

Read/query commands and observations:
- `read(c0-dispatch.json?q={wave,count:(.tasks|length),taskKeys:(.tasks[0]|keys)})` → wave `mori-r36-c0`, count **25**.
- `read(w1-dispatch.json?q={counts,roleCounts:(.taskCall.tasks|map(.agent)|group_by(.)|map({role:.[0],n:length})),firstTask:(.taskCall.tasks[0]|{name,agent}),note,wave})` → `spawn=33 resume=0 total=33`; one taskCall; connector, executor, scribe, scout, reviewer and critic roles present, no planner role.
- Same query on `w2-dispatch.json` → `spawn=66 resume=0 total=66`; connector, executor, scribe, scout, reviewer and critic roles present, no planner role.
- `read(dispatch-log.txt:4-18)` → an additional **2 executor** counter builders; C0 and w1 each recorded as one batched call. The assignment and this running seat establish w2's actual dispatch; the JSON alone is a dispatch payload, not completion proof.

Arithmetic: **25 + 33 + 66 = 124** named control/build/attack seats; including the two counter builders gives **126** recorded dispatches. The numerical ≥8 batched L2 floor is plainly met and the documented total is within 128. Dispatches are not completed reviews: the assignment's dead/refused/missing-report distinctions must survive into closure.

Two separate conformance qualifications must not be hidden behind that numerical success:
1. Canonical assignment `:82-88` requires an L2 planner. The inspected role maps have none; `w1-dispatch.json:235` instead says **L1 holds the planner seat**. That is not an L2 planner. Report the role-split departure rather than retrospectively renaming an executor or counting L1 as L2.
2. Canonical assignment `:179-193` allows two **v1** waves or one **v2** wave. `read(w1-dispatch.json:4-19)` observes band `32–64`, total 33; `read(w2-dispatch.json:4-19)` observes band `64–128`, total 66. The actual hybrid is not the default two-v1 shape and not the one-v2 alternative. Validation under a permissive policy is not proof the chosen round shape satisfies the assignment. Record the departure / any actual operator ruling; do not invent one. These are conformance issues, not invented counter failures.

## Harms, duplicate authorities and false provenance

### F1 — receipt-to-admission laundering is blocked, not cured by success elsewhere

No qualifying C1 outside judgment was found in the bounded sweep `unprovable-but-better|named non.author|reviewer[: =]|verifier[: =]` over the round tree, knowledge note and SCORECARD. The matches are conditional rules, lane-wave roles and historical rounds, not a current reasoned C1 judgment; `w2/RevExploratoryHonesty.md:104-109` independently records the same absence. This missing prerequisite is not itself misconduct if reported honestly. It is decisive against admission. Impact: freshness admission and calibration.

Smallest safe correction: either attach an actual qualifying outside judgment with reasons, or explicitly stop with C1 unprovable. Never convert the counter's token into that judgment.

### F2 — the delivered prose and live repairs are different authorities

Direct command `git show R:.ufo/waves/round-36/contract.md` observed at landed line 13 **“flags stale source rows”** and an unqualified `C1=met` after-cell, while landed `:114-126` declares C1 exploratory and explicitly denies a freshness verdict. The live line 13 is corrected. Direct command `git show R:corpus/knowledge/source-drift-r36.md` observed at landed `:16-19` the exhaustive **seven**-row drift explanation, contradicted by the recorded after command above (`oracle_drifted=9`); the live note now explains the additional S210/S211 cases. Leaving these false delivered descriptions unmarked would harm documentation quality/calibration; do not claim the data tip already contains the fixes.

Direct command `git cat-file blob R:.ufo/waves/round-36/contract.md | sha256sum` observed `065a17b523b29840df8f1d516ca50eedb0da5e7d614198567439514a099dd93b`, versus freeze-v2's whole-contract pin `dbd3f6d793239a2f729f89778847eb47b901167fa7a98f57269621f4273c4127`. Peer identity review (`w2/RevPredIdentity.md:14-18`) finds predicate sentences unchanged; this is not grounds to invent P-C2=unmet. Preserve the original freeze and append a precise amendment/provenance explanation; do not rewrite the historical pin to pretend the exploratory declaration was inside the earlier frozen bytes, or alter counters after data.

Smallest safe correction: land the already-visible documentation corrections with their true revision and preserve the freeze/declaration chronology. Correct every standing mention, without turning this into a new predicate.

### F3 — “18 discharged” can falsely erase historical violations

The recorded gate command `python3 tools/mori-sources-appendonly.py R --round-base B` observed `appendonly_violations=18`, all carried ids in `superseded`, `deleted=[]`, `round_changed=[]`, exit 0 (`w2/ExecCensusEnd.md:176-204`; also `w2/RevAppendDebt.md:20-45`). Its exit 0 concerns **this round**, not absence of historical violations. QUALITY 102 explicitly forbids a superseder discharging the violation (`corpus/QUALITY.md:809-817`). The live SKILL now says “disposition, not a discharge” (`:864-867`), but live `corpus/README.md:574` still says **“it discharges the 18 in-place-edited ids … via the S205–S220 supersede rows”**. S205 is the new protocol source, not one of the new superseders; some dispositions predate this round.

Impact: calibration/provenance, not a C2 implementation failure. Smallest safe correction: say “all carried violations now have superseder dispositions; historical violations remain 18; no new round violation,” distinguishing the new S206–S220 dispositions from the pre-existing ones.

### F4 — novelty must name the new population/operation, not erase prior programs

Live `corpus/README.md:565` says previously only manual sha re-checks. Counterexample inspected directly: round-32 `count-c1.py:116-120,253-255` programmatically fetches source URLs, and `read(.ufo/waves/round-32/evidence/c1-after.txt:1-8)` records command `python3 .ufo/waves/round-32/count-c1.py 7766732a98795467d0541630e9707a7acba518e1`, output `recheck_rows=34`, `rows_ok=34/34`, `C1=met exit=0`. That rejected calibration claim does not erase the executed fetch operation. This does **not** disprove novelty of the new newest-copy whole-registry sweep.

Impact: calibration and accuracy of C1's prior→after story. Smallest safe correction: contrast the new reusable all-copied-row byte probe with the earlier bounded round-specific recheck, rather than claim all prior re-fetching was manual.

### F5 — bounded C2 residual, not an observed met negative control

[INFERENCE, static trace only] In a history holding rows, deleting the entire SOURCES path and restoring identical bytes, the tool skips the absent state (`tools/mori-sources-appendonly.py:205-209,223-235`), so that transition contributes no `deleted_at`; the real oracle duplicates that skip (`count-c2.py:532-540,551-564`). The blind generator always writes the path (`:361-369`) and its operation selection removes rows, not the file (`:430-479`). This is a shared blind spot for a broader “every deleted/restored history” assertion. No such experiment or met negative control was run by this critic; the C2-axis peer likewise reported no observed met negative control.

Impact: operability scope and confidence in oracle independence. Smallest safe correction: disclose the unexercised edge and keep P-C2 success bounded to its frozen arms; any expanded counter is a separate future claim, never a post-data replacement of this claim.

### Scope allegations require evidence, not name matching

The landed note's `exit 2` action says “Restore” (`corpus/knowledge/source-drift-r36.md:28` at R); this is a genuine detection/report-only instruction defect against `PROVINCE.md:16`. The live note's `:41` routes restoration to the operator. Saving a source copy during lane curation is not equivalent to remediating the host. Likewise `count-c2.py:70-82` shows a timeout kill restricted to its newly created child process group, not an observed host/service kill; no evidence inspected establishes that handler ran. Do not promote mere SIGKILL text into a fabricated host-harm measurement, or edit a frozen counter to hide it.

## Delivery boundary and smallest complete correction

Direct command `git ls-tree -r --name-only R -- .ufo/waves/round-36/evidence/ corpus/lessons/round-36.md .ufo/waves/round-36/w2/ .ufo/waves/round-36/w2-dispatch.json` observed only `c0-rescore-v2.txt`, both before receipts, `census-start.txt`, both freeze files and `refs/ref-c1.py`, `refs/ref-c2.py`. After receipts, end receipt, lesson and w2 records are absent at R. Direct command `git diff --name-status B R -- LOG.md SCORECARD.md SHONEN.md PROVINCE.md` observed no output: those bookkeeping/protected files are unchanged at the data endpoints. The complete glob `.ufo/reports/round-36/*.md` observed only kake, kumitate and kotodama reports, not a mori final report. This is unfinished close-out evidence, not proof the in-flight lane has filed a marker.

Keep measured revision R distinct from the eventual delivery commit: land the actual receipts/w2 evidence, source Gate/Mistakes lesson, corrected standing prose and genuine LOG/SCORECARD records, then attach the final census and post-helper index-clean evidence to the true final revision. Record role/shape departures. Claim no scalar freshness change and no “all axes improved” shortcut. A round's expansion/quality/discernment verdicts need their own evidence: source-row growth alone is not expansion (`CORPUS.md:123-125`), an uncorrected false note cannot support clean quality, and lane-wave agreement is not outside discernment (`LEARNING.md:40-50`). No irreversible trade was established here; the documented prose/provenance defects are fixable. Even after fixing them, C1 remains an admission blocker absent the outside judgment. Canonical Rust closure alone rules on the delivered result.

Report: .ufo/waves/round-36/w2/CritAdmission.md
VERDICT: FAIL — admission is not established; C1 lacks the required outside judgment, landed contract.md:13 overstates stale-source detection, landed corpus/knowledge/source-drift-r36.md:16-19 contradicts the after receipt, and live corpus/README.md:574 still conflates superseder disposition with discharge.
