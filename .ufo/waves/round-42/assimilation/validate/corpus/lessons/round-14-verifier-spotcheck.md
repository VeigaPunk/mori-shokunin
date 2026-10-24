# Round 14 verifier spot-check

author: hyaku closure (non-author integrator, @m_strong)
date: 2026-10-20

## Boundary and decision

Reviewed entering `dbe85009253c092fe50e4e93056fceeae273ec31` (B) against delivered `52512aea760472e30e9d08f8838ad48d122dd109` (H), not an uncommitted tree. **Status ok; admitted true, at the report's bounded scope.** One declared claim, C1 coverage: restore structured OOM critical/DRIFT, fleet/non-fleet subject partition and tsukuroi triage while retaining six separately scoped counters. The legacy user signal-result warning is restored too. This does not admit exhaustive old-MESSAGE equivalence, authenticated membership, unique-victim counts, positive-load live behavior or comprehensive OOM coverage.

The integrator ran plain Git/Python/JSON counts, reopened primary sources, and ran the required fleet source validator. **No mori-owned gate, selftest, census or drift command was executed by closure.** Behavioral results below are committed-evidence verification, not fresh behavioral execution. Two fresh read-only reviewer seats assisted with receipt integrity and production-source/no-harm review; their suggestions were adjudicated, not treated as independent verdict authorities.

## Step-1 conformance

- `git log --format='%an %H %cI' -- .ufo/reports/round-14/mori.md` returned `mori-shokunin f9ad86cc19e2005c7143f608417284b617c2fe58 2026-10-20T03:51:29-03:00`. Real work, evidence, LOG links, source/trend sections and four separate `[~]` assessment lines under `## SHONEN` are present. Not a marker.
- Lane H committed at `2026-10-20T03:49:40-03:00`, before the report commit. `git -C <lane> status --porcelain` printed nothing; `git -C <lane> rev-list --count @{u}..HEAD` returned `0`. H was clean and pushed before closure writes.
- Extracted report commit references, resolved each with `git rev-parse --verify <ref>^{commit}`, then ran `git merge-base --is-ancestor <resolved> HEAD`: all returned 0. Unique lane commits: H, `5601d1201926124f7884bc694568abac2ead6d5c`, `8d22d18fb4a4124becb35123ca839c93cbae0028`, `a5cc3134ff9c1b9f1d77a6d25783be8bcea0f2eb`, B, historical `80bd58a42f23866ac2fdad2400cc0072dfa5a3d9`, `c13df48d50e1dbcdb7245a66ac3511b302ffa7d3`. `304cb223` is a digest abbreviation, and `cf8ebfc6…` an external systemd revision, not dead lane-commit citations.
- Read the dispatched prompt completely. Rendered the committed `templates/round-prompt.md` by substituting LANE=mori, ROUND=14, FLEET_ROOT and the dispatched axes, plus `<mori-repo>`=mori-shokunin. `prompt.startswith(rendered_template.rstrip())` was **True**. The canonical contract and campaign addendum are present; the latter explicitly maps planner to L1 and forbids model parameters. Prompt is committed in `e9934d885692323d9073cecd36d4ee5e7c9a8c58`.
- Committed dispatch JSON counts: spawn=32/resume=0/total=32; task list length 32; explicit model keys 0. Roles independently recounted: executor9/scout6/connector3/reviewer3/critic4/scribe3/sentinel2/revenger1/mutation-tester1. Bound registry records 32 `MoriR14.*` identities. This is documentary wave evidence, not a replay of dispatch.
- `git diff --name-only B H -- SHONEN.md 'corpus/lessons/*verifier*' 'corpus/lessons/*aggregator*'` printed nothing. Checklist remains the canonical four unchecked boxes. Protected reviews were not rewritten.

Dispatch/completion digest copied from the closure prompt (mutable runtime log is not the durable pointer):

```text
2026-10-20T02:52:22-03:00 launch mori round=14 pgid=1549200 driver=hyaku-inline attempt=1
2026-10-20T03:51:58-03:00 complete mori round=14; hyaku-inline attempt=1
```

## C1 re-check: measured counts versus evidence-verified behavior

All paths here resolve under the lane repo. The following plain counting command was executed by closure, exit 0:

```sh
jq -s '[.[] | [.claims[] | select(.id == "R14_OOM_ALARM_USER" or .id == "R14_OOM_ALARM_SYSTEM" or .id == "R14_UNIT_OOM_KILL" or .id == "R14_UNIT_FAILED_FLEET" or .id == "R14_UNIT_FAILED_NONFLEET" or .id == "R14_UNIT_SIGNAL_WARN") | select(.status == "fail")] | length]' .ufo/waves/round-14/evidence/red-before-accepted/evidence.json .ufo/waves/round-14/evidence/green-after-accepted/evidence.json
# [6, 0]
```

Also independently parsed `git show H:<receipt>` using Python `json.loads` and `collections.Counter(c['status'] for c in data['claims'])`: red **43 fail**, green **44 pass**. The shared 43 case IDs agree; the extra green assertion is the frozen-red control. This reproduces the report, but **43 is not a count of historical production defects**: new required metadata makes controls fail too. The six selected arms additionally have substantive alarm/routing reasons.

Read the retained `runs` entries selecting the explicit `sut.<id>` or `frozen.<id>`, then opened each committed `stdout_path` via `git show H:<relative-path>`. Observed:

| Acceptance arm | Entering frozen output | Delivered output | Result |
|---|---|---|---|
| User/system OOM notices | CLEAN, no OOM critical finding | DRIFT, one `OOM_KILL_JOURNAL severity=crit`; separate source/scope counts | verifies |
| `UNIT_RESULT=oom-kill` | no OOM critical finding | critical/DRIFT plus appropriate subject route; missing/array subject cases also alarm | verifies |
| Fleet failed subject | unpartitioned generic finding | fleet-only `UNIT_FAILURE_JOURNAL severity=info owner=mori` | verifies |
| Non-fleet failed subject | generic fleet-named finding, no tsukuroi route | `UNIT_FAILURE_OUT_OF_SCOPE severity=info owner=tsukuroi` | verifies |
| User `UNIT_RESULT=signal` | no warning | `KILL_SIGNAL_JOURNAL severity=warn`, DRIFT; `process_sigkill=0 user_unit_signal=1` | verifies |
| Six scoped raw counters | user 3/0/2/1/2/1; system 2/1/4/3/0/2 | exactly the same vectors | preserved |

Counter order: kernel-OOM notice, oomd notice, coredump notice, signal11 record, process-SIGKILL record, unit-failure record. Closure independently parsed the raw `SURFACE journal.user/system` lines of all three retained SCOPED_PARITY runs (red frozen, green frozen, green SUT), extracting `key=value` tokens; their stdout digests matched. These are **nonzero synthetic fixture** observations, not live load.

For live evidence, independently parsed `live-measurement.json`'s delivered stdout and the `before_queries`/`after_queries` observations. For each of the six classes in each scope, compared `before count == int(delivered token) == after count`: **12/12**, all zeros, with two scoped rows retained. No embedded reproducer was executed. The all-zero live result cannot prove positive-load alarms, unique victims or fleet causation.

Source spot-read: `tools/mori-census.sh:399–409` makes warn/crit set DRIFT; `:1001–1036` partitions solely from exactly one valid UNIT/USER_UNIT and derives result subsets independently; `:1267–1290` separates fleet/non-fleet/unattributed findings; `:1293–1331` emits one global critical OOM line; `:1334–1353` restores the separate user signal arm. Literal `emit_finding OOM_KILL_JOURNAL crit` and non-fleet `emit_finding UNIT_FAILURE_OUT_OF_SCOPE info` calls each count **0→1** over B/H committed source. Source counts corroborate, not replace, the behavioral receipts. Six raw class counters retain their names/order at `:1359–1366`; emitter fields are not used for subject classification.

### Revision and Gate-standard evidence

Used `hashlib.sha256(subprocess.check_output(['git','-C',lane,'show',rev+':'+path])).hexdigest()` over committed bytes:

| Delivered input | SHA-256 at H |
|---|---|
| census | `0e41cb83fce2e8c5c711171e1cde2e6fa2809dcfce630eccabe52bcbe41516d9` |
| r13 gate | `304cb22336da40c6d465b55f135ec9bb9bf53fdea4656c63c24c37963b6718f2` |
| r14 gate | `c39e5a7352666d09dc662293e1ea7be47ee3523b53247a5a6ae02e7dda19288d` |
| silence oracle | `34cd5770889ec6e7521b477aa9976cece7a64e07b83774c12ce2aea73161abfa` |

Frozen r14 census is byte-identical to B: `39abda0a67028575d888d9157b8548dec0b4944c3d8c165691e88ab657fc3985`. All four production inputs are byte-identical between measured `5601d12` and H. Census/r13-gate/oracle also match their earlier measured `8d22d18` bytes. Reviewer checked every retained stdout/stderr digest in the paired bundles (86 green-bundle runs plus 43 red-bundle runs), with no mismatch.

Committed receipts, not re-executed here:

| Receipt under `.ufo/waves/round-14/evidence/` | Verified result | Measured revision |
|---|---|---|
| `census-selftest.json` | 104 PASS, 0 FAIL; exit 0 | 8d22d18 |
| `r13-selftest.json` | checks=33, isolated cases=2; exit 0 | 8d22d18 |
| `r14-selftest-accepted.json` | checks=20; actual subprocess red rc1/tamper rc2; exit 0 | 5601d12 |
| `red-before-accepted/evidence.json` | strict 43 fail, exit 1 | 5601d12 wrapper |
| `green-after-accepted/evidence.json` | 43 cases + frozen-red control = 44 pass, exit 0 | 5601d12 wrapper |
| `r13-preserved/evidence.json` | 24 pass + 2 mutation-red, exit 0; F01 exact-author and F02 honest28/28/BANANA0/28 retained | 8d22d18 |
| `drift-current.json` | exit 1; old drift baseline remains red | 5601d12 |

Both verdict-producing regression gates now have SKILL registry rows, declared 0/1/2 maps, persisted input pins and isolated exit+stable-id self-invocations. Literal expected counts/verdicts are independent of SUT recomputation. Same-commit authorship is not a Gate-standard violation: no rule requires expectations be committed before implementation. Consistency invariants do not replace those literals. Initial setup-crash receipts remain retained and are explicitly excluded from behavioral red evidence. Final receipt timestamps precede the shipping H commit.

The r13 preserved receipt says `revision.dirty=true`. This is provenance debt, **not established input drift**: closure/reviewer matched census, oracle, SHONEN, frozen manifest and frozen scripts to the cited committed bytes; synthetic git stubs prevent live repository state from driving fixture verdicts. The registry row was already committed and unchanged. Exact contemporary porcelain was not retained; untracked output receipts are a supported explanation, not a proved complete dirty-path list. Route clearer dirty-scope capture below. F01 remains a whole-function transplant and F02 a reconstructed shim; neither establishes original-byte single-line causality. Original frozen historical failures remain primary.

## Per-axis judgment and no-harm adjudication

`git diff B H -- SCORECARD.md` showed **82 additions, zero deletions**: an appended correction withdraws unsupported prior coverage credit, preserves the verified operability gain and holds coverage6/operability7/depth5/freshness5/calibration5/adjacency6. Repair is not an extra scalar point.

| Axis | Verdict | Evidence |
|---|---|---|
| coverage | improved | C1 six selected arms 6→0, raw scoped gains retained, unknown-subject classification explicit |
| operability | unchanged | verified r13/F01/F02 behavior retained; delivered gate selftests/registries supplied; setup failure honestly corrected |
| depth | unchanged | sourced typed semantics support C1; no separate depth move |
| freshness | unchanged | live bracket rechecked; old drift pin still red, not silently re-pinned |
| calibration | unchanged | bounded claims, fixture/live separation and historical corrections; no scalar or outside self-credit |
| adjacency | improved | measured tsukuroi non-fleet route restored; no diagnosis/actuation ownership takeover |

The source reviewer initially compared malformed-stream behavior with pre-r13 text matching. That is not a new B→H loss: B already invalidated the whole malformed class and lacked the OOM alarm. The reviewer withdrew the harm finding. Class-wide invalidation remains a serious, **disclosed inherited limitation**, not part of this bounded repair's guarantee. The source review also suspected an unmigrated SYSTEM aggregate consumer; direct fixture inspection disproves it: `mori-round13-regressions.py:1491–1514,1952–2014` expects raw system failures=4, fleet=2, missing=1, ambiguous=1 and a fleet-only SYSTEM finding count=2. Its committed routing receipt passes. The SYSTEM id's narrowing is explicitly documented at census `:934–937`; all inspected active callers use the new split. No new harm was established. This does not claim every pre-r13 MESSAGE alarm is restored.

## Outside discernment and source spot-check

Sampled the round lesson's `## Gate` including its appended `## Measured gate decision`, which supersedes the pending candidate row.

| Item | Lane decision | Reopened source | Outside decision | Reason |
|---|---|---|---|---|
| Structured OOM alarm and subject-owner partition | admit, bounded measured scope | paired committed receipts; delivered census; [journal-fields UNIT/USER_UNIT and Trusted fields](https://www.freedesktop.org/software/systemd/man/latest/systemd.journal-fields.html#UNIT=) | agree | Positive typed fixtures restore critical/DRIFT and INFO ownership split; subject is not emitter, and raw counters remain separate. This is not exhaustive event coverage. |
| Missing UNIT/USER_UNIT proves non-fleet | reject | same official field reference; classifier `:1001–1015` | agree | Subject metadata and emitter metadata are different. Missing/dual/malformed subject remains unknown rather than proving non-membership. |
| Cgroup-local counter substitutes for all journal alarms | reject | [kernel cgroup-v2 memory.events.local](https://docs.kernel.org/admin-guide/cgroup-v2.html), local-event definition | agree | Definition says fields are local to the cgroup, not hierarchical. Selected-cgroup zero cannot cover other journal scopes or all units. |
| New S037 subject-unit source row | docs/A/mined | official journal-fields UNIT=/USER_UNIT=, systemd262, reopened 2026-10-20 | agree | Located quote: “Used by the system and user managers when logging about specific units.” **12 words** by whitespace split, within 25; present in cited section. Trusted fields describe the emitting process. |
| New S038 OOM vocabulary row | code/A/mined | [pinned service.c:6588–6602](https://github.com/systemd/systemd/blob/cf8ebfc6159cf0b3b99aa9a0164ccb07c4c9c5af/src/core/service.c#L6598), reopened 2026-10-20 | agree | Located whitespace-normalized quote `[SERVICE_FAILURE_OOM_KILL] = "oom-kill",` matches the service_result_table. Vocabulary supports selection, not authenticity. |

Required command executed by closure:

```sh
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori
```

Exit **0**, observed:

```text
mori W04 S035 duplicate url raw.githubusercontent.com/systemd/systemd/cf8ebfc6159cf0b3b99aa9a0164ccb07c4c9c5af/catalog/systemd.catalog.in across scopes
mori W04 S037 duplicate url www.freedesktop.org/software/systemd/man/latest/systemd.journal-fields.html across scopes
mori ok /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md
```

W04 is informational. Independently read committed B/H SOURCES bytes with Git, selected `^\|\s*S\d{3,}\s*\|`, split cells and counted tiers/statuses: **36→38, A33→A35/B2/C1, mined15→17/queued20/rejected1**. New IDs S037/S038 only; existing S002/S013/S015/S035/S036 changed only used-by cells. All observed registry deltas match the lesson/report.

## Trends

- **expansion: improved.** One new knowledge entry `journal-alarm-routing-r14.md` cites mined S037/S038 and advances FR1 typed subject/result handling, including explicit unknown subjects. The coverage map links the actually measured capability; row volume alone is not the improvement.
- **quality: improved.** Previously rejected OOM/route no-harm claims are explicitly superseded and repaired with positive/negative witnesses while independent scoped counters survive. Historical text-selected count and mutation provenance qualifications are carried into active docs. Minor wording/provenance debt below does not undo the bounded factual repair.
- **discernment: improved.** This outside sample agrees with both admits and rejects. Prior outside disagreement becomes lesson M1–M8 and grounded Q29–Q32, with actual able-to-fail witnesses. The author's 32 seats did not stand in for this closure.

## Routed defects and operator notes

1. **mori, next round — low provenance debt:** retain the dirty-path scope (or measure from an explicitly frozen clean input tree with output outside it) when a gate records `dirty=true`. Current verdict-driving hashes match the cited revision, so no behavioral mismatch is inferred; the exact historical porcelain is unknown.
2. **mori, next round — wording clarification:** qualify `journal-alarm-routing-r14.md:221` “fail-loud on positive validated records” as **positive validated class counts**, cross-linking the mixed-malformed-class limitation at `:386–390`. A valid record inside an invalidated class can be hidden; the report already discloses this. Do not convert the wording fix into a claim that the inherited suppression path was repaired.
3. **mori, next round — interface clarity:** document that legacy KILL_SIGNAL_JOURNAL `count`/`process_sigkill` can be `unavailable:<reason>` while an independently available user-unit signal arm raises WARN; these are not fabricated numeric zeros. The production code preserves availability honestly. Label SCORECARD's nonzero vectors explicitly “fixture” to match the already clear report/knowledge distinction.
4. **mori, carried gate debt:** old r10 drift pin is still red at measured 5601d12. Keep it routed as status-neutral conformance debt; a future re-pin needs reasoned semantic review, not merely silencing the red result. No full-freshness pass is admitted here.
5. All six mori repair items routed by round13 now have landed fixes or explicit qualifications: OOM/signal behavior, subject split/owner route, structured-vs-text limits, gate registration/delivered selftests, mutation provenance, and active historical-count wording. Retain disclosed trust/access/retention/name-token/forgery limitations; no expansion of the present claim is authorized.
6. **Operator:** all four SHONEN boxes now have checkable evidence at the bounded scope (SKILL tables/patterns/checklist and sources; logged live end-to-end observation; registered runnable instructions with committed receipts; detection-only province and repaired triage). This is not a promotion or fresh execution of every instruction. Boxes remain untouched; promotion remains operator-owned.

No tools were installed or updated by closure or its review seats. No credential/auth file or agent database was opened, and no separate omp CLI was launched.
