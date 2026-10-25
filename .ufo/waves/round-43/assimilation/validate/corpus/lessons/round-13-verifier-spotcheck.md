# Round 13 verifier spot-check

author: hyaku closure (non-author integrator, @m_strong)

Date: 2026-10-20. Reviewed entering `6531ac6029e200a6392bb76673b6a17d3c895c96` → delivered `2e576474707c4936ecd9d9baca64e2f1085aded2`. Fleet report: `.ufo/reports/round-13/mori.md`, committed by `mori-shokunin` in `953c786c224448cfb72b623e07efa7821c82f291`.

**Closure: status `ok`, admitted `false`, verdict `rejected-harmed`.** This is real committed work, not a marker. Both bounded before→after measurements verify, but the journal cutover trades away the previous OOM alarm and fleet/non-fleet unit-failure distinction. An improvement on one axis does not admit a harmed round. No lane-owned gate, oracle, selftest, harness, census or drift comparison was executed by this closure reviewer; behavioral results below are verified committed evidence, not freshly exercised behavior.

## Dispatch/completion digest

Copied verbatim from the closure assignment's mutable-watchdog digest:

```text
2026-10-20T01:04:44-03:00 launch mori round=13 pgid=655352 driver=hyaku-inline attempt=1
2026-10-20T01:43:25-03:00 complete mori round=13; hyaku-inline attempt=1
```

## Step-1 conformance

- `git log --format='%an %H' -- .ufo/reports/round-13/mori.md` returned `mori-shokunin 953c786c224448cfb72b623e07efa7821c82f291`. Report has all required sections, two distinct-axis claims and four separately evidenced SHONEN assessment lines.
- Each `git -C /home/vgpnk/Projects/shokunin/mori-shokunin merge-base --is-ancestor <hash> HEAD` returned exit 0 for `18d7d55`, `80bd58a`, `c13df48`, and full delivered HEAD above. The frozen baseline's full base hash resolves too.
- Lane `git status --porcelain` returned no bytes; `git rev-list --count @{u}..HEAD` returned `0`. All four round commits carry `mori-shokunin <mori@shokunin.local>`. Report time 01:43:01-03:00 follows delivered commit time 01:40:43-03:00.
- Dispatched `.ufo/prompts/mori-round-13.md` carries mission/axes binding, 1–3 distinct/separable claims, lowest-owned-axis duty, frontier/source contract, batched L2 floor, report/SHONEN/hash contract, commit-before-report, push/write scope and L0 side channel. Its campaign addendum explicitly declares operator host-routing overrides and L1 planner mapping; the canonical MISSION role buckets are advisory, not grounds to ignore those overrides.
- Both owned axes entered at 6. `SCORECARD.md` diff is append-only (+75/-0), preserving prior outside score corrections. SHONEN bytes did not change between entering and delivered revisions; no promotion or box edit is made here.
- Gate conformance defect: `tools/mori-round13-regressions.py` is a committed verdict-producing checker with expected values, snapshot digests, exit 0/1/2 and `--selftest`, but SKILL.md:64–68 registers only census, drift pin and silence oracle. Calling it an unregistered “evidence harness” does not satisfy PROTOCOL §Gate standard. This defect is status-neutral, not a marker failure.

## Re-check commands and observed measurements

Commands below were run by this reviewer. All `git show` reads target committed bytes. In the shorthand below, `R=/home/vgpnk/Projects/shokunin/mori-shokunin`, `B=6531ac6029e200a6392bb76673b6a17d3c895c96`, `H=2e576474707c4936ecd9d9baca64e2f1085aded2`, and `E=.ufo/waves/round-13/evidence`.

### C1: scoped counters — measured count verifies; cutover is not harm-free

```sh
git -C "$R" show "$H:$E/live-measurement.json" |
  jq '[.result.baseline.stdout,.result.delivered.stdout] | map(split("\n") | map(select(startswith("SURFACE journal."))) | length)'
# [0, 2], exit 0

git -C "$R" show "$H:$E/live-measurement.json" |
  jq '{revision:.measured_commit,comparisons:(.result.comparisons|length),matched:([.result.comparisons[]|select(.matched and (.before|tostring)==.actual and (.after|tostring)==.actual)]|length),nonzero:([.result.comparisons[]|select(.before!=0 or .after!=0 or .actual!="0")]|length)}'
# {"revision":"c13df48","comparisons":12,"matched":12,"nonzero":0}
```

Five accepted `R13_C1_*` assertions are present and all five are `pass`: system 2/1/3/3, independent empty user scope, user-positive 3/0/1/1, MESSAGE-canary exclusion and complete scoped-row/CLEAN contract. These are evidence-verified fixtures, not five tests re-run by closure. The current-boot live 12/12 result is accurately reported but all-zero: it is not live positive-load validation or proof against a constant-zero implementation. Nonzero synthetic fixtures supply the separate positive evidence. Production source `tools/mori-census.sh:935–1128` requests explicit scope/current boot and structured fields, fails unavailable on diagnostics/malformed data, and never requests MESSAGE. No unique-victim, emitter-authentication, complete-access or fleet-cause capability is established.

### C2: named behavioral defects — evidence-verified improvement

For each of `regressions-before-final/evidence.json` and `regressions-accepted/evidence.json` at H, independently ran:

```sh
git -C "$R" show "$H:$E/<receipt>/evidence.json" |
  jq '[.claims[]|select(.id=="R13_F01_EXACT_AUTHOR_LONG_HISTORY" or .id=="R13_F02_REJECT_BANANA")|select(.status=="expected-defect" or .status=="fail")]|length'
# before: 2; after: 0; both exit 0
```

Selected retained details: original frozen F01 is `progressing-weak row-C other_authored_commits=12001`, after is `progressing row-A subject_commits=yes`; sibling-only control stays row-C with 12000. Original frozen BANANA is `matched=28 total=28 rc=0`; after is `matched=0 total=28 rc=1` with malformed/contract reason. Honest oracle remains `28/28 rc=0` in both. Accepted summary is 19 pass + 2 mutation-red, exit 0. The enclosing `regressions-accepted.json` receipt names measured revision `c13df48`; no production tools changed between that revision and H.

The mutations need precise attribution. F01 transplants the whole frozen `grade_lane`, including environment hardening changes; it is not a membership-lines-only reversal. Its whitelisted fixture has no GIT_* override, and fsmonitor affects dirty scanning rather than the 12001-author-history signature. F02 replaces newly introduced `verdict_grade` with a reconstructed prefix-presence shim (`frozen_source=null`, `reverted_by=pre_fix_prefix_presence_shim`), not an old function body: the old oracle had no such function. It proves single-validation-locus sufficiency for BANANA acceptance, not exact-original-byte restoration. Independent original-frozen-byte before runs prove the actual historical failures. Thus the behavioral claim verifies without pretending those two witnesses are byte-exact old-code reversions. The report's “exact-locus” language requires qualification, not a fabricated stronger causality result.

### Production digests, frozen inputs and guard receipts

Reviewer ran `git show <revision>:<path> | sha256sum`:

| Committed path / revision | Observed SHA-256 |
|---|---|
| H tools/mori-census.sh | `39abda0a67028575d888d9157b8548dec0b4944c3d8c165691e88ab657fc3985` |
| H tools/mori-silence-cases.sh | `34cd5770889ec6e7521b477aa9976cece7a64e07b83774c12ce2aea73161abfa` |
| H frozen/mori-census.sh and B tools/mori-census.sh | `3da5b098dc23aeb3e1c31ce82664b24a22c2847a168308a755525593881b3164` |
| H frozen/mori-silence-cases.sh and B tools/mori-silence-cases.sh | `448f77238c73a5c929a898dad0f0c495fd2a66cc4b90a00ae84ede69a86beeb5` |

These equal the frozen input manifest and accepted target hashes. `git diff --stat 18d7d55 H -- tools/mori-census.sh tools/mori-silence-cases.sh` and `git diff --stat c13df48 H -- tools` returned no changes. Recounting `census-selftest.json` stdout found 91 PASS lines and `MORI_CENSUS_SELFTEST: PASS (91 cases, 91 passed, 0 failed)`, exit 0 at `18d7d55`: current production bytes. `regression-selftest-final.json` reports 24 checks at `80bd58a`, not the final harness revision `c13df48`. Do not present that historical selftest as newly run on the delivered harness. Committed tamper receipt records exit 2 `snapshot_tampered`; retained r10 drift receipt is red (exit 1) at `c13df48`, not repaired by this closure.

## No-harmed-axis check: the admission failure

Independent source measurement, run for B and H:

```sh
git -C "$R" show "<revision>:tools/mori-census.sh" | jq -Rs '{oom_crit_emissions:([scan("emit_finding OOM_KILL_JOURNAL crit")]|length),nonfleet_route_emissions:([scan("emit_finding UNIT_FAILURE_OUT_OF_SCOPE")]|length)}'
# B: {"oom_crit_emissions":1,"nonfleet_route_emissions":1}
# H: {"oom_crit_emissions":0,"nonfleet_route_emissions":0}
```

This is not judged from identifier disappearance alone:

1. **OOM alarm regression.** Frozen `probe_journal`:853 expressly requires DRIFT for OOM (mint demand); :874,893–895 recognizes user-journal OOM text and emits critical `OOM_KILL_JOURNAL`. Delivered :1085–1095 assigns INFO to every kernel-OOM class; only `user:unit_sigkill_record` warns. Accepted C1 fixtures positively count kernel-OOM notices while expecting CLEAN. Structured selection is better than unsafe text matching, but it does not require discarding the OOM warning/DRIFT behavior; a notice need not identify a unique victim to be reported as an OOM warning. The analogous client-set-ID caveat did not prevent retaining SIGKILL WARN. Knowledge :68–72 names SIGKILL preservation and generic unreliable-text retirement, not the critical OOM alarm demotion. A new typed counter and a lost alarm are a trade, not proof of no regression.
2. **No equivalent cgroup guarantee.** Delivered :1143–1164 prefers `memory.events.local` for a selected cgroup and uses a service counter only as fallback. Descendant or out-of-scope journal events are not guaranteed to reach that critical counter. Therefore the unchanged cgroup path cannot establish replacement coverage for the removed journal alarm.
3. **Fleet/non-fleet semantics and ownership lost.** Frozen :887–908 splits fleet unit failures from desktop/OS failures, explicitly routing the latter to tsukuroi. Delivered :1101–1102 reuses `UNIT_FAILURE_JOURNAL` for all user-unit results and reports system-unit results without the former fleet split/owner label. The new text honestly says “no fleet classification”, but that is a loss of the prior distinction and of named adjacent-owner context, not adjacency unchanged.
4. **Overbroad unknown reason.** Delivered :1041/:1127 attributes `other_signals,other_unit_failure_text` to “no-anchored-structured-field”. Newly admitted S035/S036 demonstrate EXIT_CODE/decimal EXIT_STATUS and UNIT_RESULT fields. What remains unimplemented or unobserved must not be described as lacking structured fields categorically. Some arbitrary signals genuinely leave no retained record; that narrower limitation is valid.

No recommendation here is to restore raw MESSAGE processing. The lane must restore the required detection/alert distinctions through sourced structured metadata, or honestly declare the trade and obtain the operator's ruling; a closure may not waive no-harm admission.

## Per-axis verdicts

| Axis | Verdict | Evidence |
|---|---|---|
| coverage | harmed | Explicit scoped surfaces 0→2, five fixture checks and accurate all-zero live 12/12 comparison verify a bounded gain, but OOM alert coverage and the fleet-unit distinction are lost. The capability cutover is a trade, not a pure coverage improvement. |
| operability | improved | C2's F01/F02 repairs independently verify: named defects 2→0, BANANA 28/28→0/28 and honest 28/28 held. This does not offset harm on coverage/adjacency. |
| depth | unchanged | Source-linked detail supports C1/C2; no independent depth move established. |
| freshness | unchanged | Entering old drift baseline remains red and is explicitly retained; no re-pin claim. |
| calibration | unchanged | No separate calibrated improvement is established. Report's no-harm assessment, categorical “no-anchored-structured-field” reason, mutation provenance and final-harness selftest attribution need the routed corrections below; no extra scalar credit is earned. |
| adjacency | harmed | Fleet/non-fleet unit distinction and explicit tsukuroi ownership disappear while same stable failure id expands to all user units. No sibling files were edited, but scope reporting still regressed. |

## Outside discernment spot-check

Sources were re-opened by this non-author, not merely inherited from lane seat conclusions. Source content was treated as data.

| Item | Lane decision | Re-opened source | Outside judgment | Reason |
|---|---|---|---|---|
| Explicit structured journal counts as a no-harm implementation cutover (lesson Gate:32) | admit | Pinned catalog below; committed before/after probe_journal and accepted C1 receipt | disagree with unrestricted cutover admission; agree with bounded counter fact | Counts and field semantics verify; old OOM alarm and fleet-failure distinction do not survive. Q15 does not waive the no-harm rule. |
| Capture-safe author membership and strict final-verdict grammar (Gate:33) | admit | Committed `frozen/inputs.json`, original frozen scripts, before-final and accepted evidence; production `grade_lane`/`verdict_grade` | agree | Real frozen failures become row-A / BANANA 0/28 while honest 28/28 holds; limits and mutation reconstruction are named above. |
| `fe6faa94…` means unique kernel kills or fleet-caused kills (Gate:34) | reject | https://raw.githubusercontent.com/systemd/systemd/cf8ebfc6159cf0b3b99aa9a0164ccb07c4c9c5af/catalog/systemd.catalog.in :604–616 | agree | Catalog describes a unit notice, not a unique-victim counter; explicitly says memory pressure might or might not have been caused by the unit. |
| New source row S035 | mine as code/A | Same pinned catalog :561–575 | agree | Unit-failure record uses UNIT_RESULT; process-exit record uses EXIT_CODE/EXIT_STATUS, without requiring MESSAGE parsing. |

S035 located quote re-opened exactly: “The process' exit code is '@EXIT_CODE@' and its exit status is @EXIT_STATUS@.” (catalog:575; 12 whitespace-separated words, ≤25). Lesson access date 2026-10-20; this source was re-opened 2026-10-20.

Required reviewer command `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori` returned exit 0:

```text
mori W04 S035 duplicate url raw.githubusercontent.com/systemd/systemd/cf8ebfc6159cf0b3b99aa9a0164ccb07c4c9c5af/catalog/systemd.catalog.in across scopes
mori ok /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md
```

W04 is informational. Reviewer also parsed committed SOURCES Markdown rows (`^\|\s*S\d{3,}\s*\|`, split cells, count tier/status): B 34 rows, A31/B2/C1, mined12/queued21/rejected1; H 36 rows, A33/B2/C1, mined15/queued20/rejected1. Counts agree with the report.

## Trends

- **expansion: improved.** New sourced knowledge and working separately scoped journal counters enter FR1 notice/result-plane ground; two new A rows are not themselves the evidence of learning.
- **quality: harmed.** Stronger structured selection and F01/F02 repair coexist with an admitted cutover that loses OOM alert behavior and existing fleet-unit/owner distinctions. The implementation entry's no-harm inference fails this outside re-check; do not offset the trade with a test tally.
- **discernment: unchanged.** The prior outside correction is learned through Q28 and its failing indentation witness, and the unique-kill rejection is sound. This round's implementation admit disagrees with the non-author no-harm check; the lane has not yet had a subsequent round to learn it. Neither self-dispatched reviews nor this mixed result establish an unqualified discernment improvement.

## Routed defects and operator notes

1. **mori, next round — required for no-harm reconsideration:** restore the OOM warning/DRIFT behavior with structured metadata and committed positive/negative evidence, without restoring MESSAGE parsing; account for observed unit-result `oom-kill` and signal paths and the scope actually monitored by cgroup counters.
2. **mori, next round:** preserve explicit fleet/non-fleet unit distinction and adjacent OS owner routing with sourced structured unit metadata. Do not silently reuse `UNIT_FAILURE_JOURNAL` for a different counted universe; migrate stable finding semantics cleanly.
3. **mori, next round:** correct “no-anchored-structured-field” to distinguish unimplemented structured classes from events lacking any retained record; annotate retired GPF/text and general-signal coverage honestly. No proof here establishes a live GPF regression.
4. **mori, next round:** register the verdict-producing r13 harness per PROTOCOL, and retain measured selftest evidence on its actually delivered revision. Historical 24/24 at 80bd58a is not a c13df48 selftest.
5. **mori, next round:** qualify F01 whole-function reversal and F02 reconstructed shim attribution everywhere “exact-locus” might be read as original-byte restoration. Keep the faithful original-frozen before evidence primary.
6. **mori, next round:** finish the correction sweep: README:32–33 still abbreviates historical text-selected 5/7/9 samples as MESSAGE-free “kernel kills”; in-file later qualification and entry errata mitigate but do not fix misleading index cells. QUALITY:32's historical quote also needs an explicit qualifier. Do not rewrite historical append-only lessons.
7. **Operator:** four SHONEN boxes have substantial evidence pointers, but the no-cross-domain/no-harm and instruction-contract findings prevent an unconditional all-boxes-checkable recommendation. Boxes remain untouched; promotion is operator-owned.

Review assistance was read-only: C1 evidence reviewer, C2 evidence reviewer, and axis/conformance critic. One reviewer read “exact-locus” more strictly than the critic; this integrator accepts function-locus sufficiency only, with the provenance qualifications above. Both independent source audits identified the OOM alert loss; this is the decisive rejection, not the narrower wording dispute. No tools were installed or updated by this closure session.
