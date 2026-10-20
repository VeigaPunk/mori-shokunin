# Round 14 — alarm and ownership preservation

date: 2026-10-20 · lane: mori-shokunin · entering commit: `dbe85009253c092fe50e4e93056fceeae273ec31`.
Record: LOG.md round-14; fleet report `.ufo/reports/round-14/mori.md`.

## Declared claim

**C1 coverage** repairs round 13's rejected-harmed cutover: restore structured OOM_KILL_JOURNAL critical/DRIFT alarms, fleet-only UNIT_FAILURE_JOURNAL and separate non-fleet UNIT_FAILURE_OUT_OF_SCOPE with tsukuroi triage routing, while preserving all six independent scoped counters and MESSAGE exclusion. Exactly one claim. Registration and wording repairs are conformance work, not extra axis claims. No re-pin or remediation.

## Mistakes

| id | class | evidence pointer | captured-by | fix |
|---|---|---|---|---|
| M1 | Selector improvement silently removed the critical OOM/DRIFT alarm | `round-13-verifier-spotcheck.md:72–89,130–132`; `build/NoHarmReview.md` under round-14 waves | Q3/Q25 were insufficiently operational; Q29 | Same structured `UNIT_RESULT=oom-kill` fixture requires critical OOM_KILL_JOURNAL/DRIFT before and after; frozen entering r13 bytes must fail. Notice alarms in both scopes and system-result alarms are explicit operator-required extensions, not a claim that the pre-r13 text regex matched every notice. Notice cardinality is not a reason to suppress policy alarms. |
| M2 | All failed units reused a fleet-only finding id and lost adjacent-owner context | `round-13-verifier-spotcheck.md:86,133` | Q25 and province boundary; Q29/Q30 | Classify subject UNIT/USER_UNIT metadata, not manager emitter fields; preserve separate fleet/non-fleet findings and tsukuroi diagnosis routing; missing subject metadata is unknown. |
| M3 | Unimplemented structured result/signal classes were described categorically as having no structured fields | `round-13-verifier-spotcheck.md:87,134`; S035/S036 | Q3/Q17; Q29 | Distinguish unimplemented structured classes, retired GPF/text heuristics, and delivery paths without retained records. No claim of live GPF regression is inferred. |
| M4 | Verdict-producing r13 checker omitted its protocol registry row and final delivered selftest evidence | `round-13-verifier-spotcheck.md:25,70,135` | PROTOCOL Gate standard; Q31 | Register both regression gates in SKILL.md, provide real isolated self-invocation checks and measure the actually delivered gate revision. Historical 24 checks at 80bd58a remain historical. |
| M5 | Whole-function F01 reversal and reconstructed F02 shim described as exact-locus without adequate provenance qualification | `round-13-verifier-spotcheck.md:57,136` | Q2/Q25; Q32 | Keep original-frozen failures primary. F01 restores the whole grade_lane function, including hardening deltas; F02 inserts a reconstructed prefix-presence shim, not an original function body. Neither proves original-byte single-line causality. |
| M6 | Corrected historical text-selected samples still appeared as MESSAGE-free kernel kills in active index cells | `round-13-verifier-spotcheck.md:137`; corpus/README.md rows 32–33, QUALITY criterion 16 quote | Q9/Q16 | Correct active index cells and explicitly qualify the retained historical quote; never rewrite old append-only lessons. |
| M7 | Pre-r13 user signal-result warning was only partly restored through process SIGKILL | frozen r12 `probe_journal:875,897–899`; `build/NoHarmReview.md` NH2 under round-14 waves | Q29 | User `UNIT_RESULT=signal` also requires KILL_SIGNAL_JOURNAL WARN/DRIFT from the existing failed-unit query; keep its count distinct from process signal-9 records, never infer signal9 or sender from generic signal result. Same red/green gate witnesses this path. |
| M8 | A new gate's setup exception collided with behavioral-failure exit 1 | `.ufo/waves/round-14/evidence/r14-selftest.json`, `red-before.json`, `green-after.json` at 8d22d18 | Q6/Q31; actual isolated selftest required stable ids and rejected the crash | Escape the literal shell printf placeholder inside Python formatting and explicitly map unexpected internal errors to could-not-evaluate exit 2. Preserve original setup-failure receipts; only fresh stable-id paired runs can count as red-before/green-after. |

## Gate

Admission bar: corpus/QUALITY.md. L1 wave seats are advisory and are not the independent outside verifier. Non-author round-14 admit/reject sampling remains pending until closure.

| candidate | decision | reason |
|---|---|---|
| Structured OOM alarm and subject-unit owner partition | candidate, awaiting measured evidence below | Restores explicit no-harm obligations while retaining record-count scope and source limits; S013/S015/S035/S036. |
| Journal notices equal unique victims or fleet-caused kills | rejected | Catalog units and client-supplied identifiers do not establish unique-victim cardinality or fleet causation. |
| Cgroup local counter substitutes for all journal OOM alarms | rejected | Selected memory.events.local excludes descendants and unrelated scopes; event planes are not equivalent. |
| Missing UNIT/USER_UNIT proves non-fleet membership | rejected | Missing evidence is unknown. _SYSTEMD_UNIT describes emitter, not necessarily the failed subject. |
| Re-pin to silence old drift or count wave seats as outside promotion verification | rejected | Neither repairs the alarm harm. Old baseline and unchecked SHONEN are preserved. |

## Provenance corrections

This entry supersedes the unrestricted round-13 admit in `round-13.md:32,100–102`, author no-harm assessment in SCORECARD/LOG, and any reading of the original “exact-locus” wording as byte-exact old-source restoration. It does not rewrite those records or retract the independently verified scoped-count/F01/F02 gains. Final measured outcomes, source access records and registry-cell changes are appended after integration.

The no-harm review distinguishes restoration from extension: the old user
OOM text warning matched `oom-kill` unit-result text, while the new typed
notice alarms and system-scope alarms extend that policy as explicitly
required by this round's operator direction. Host OOM detection/reporting
remains mori's province; tsukuroi retains OS diagnosis, operator actuation.
No attempt is made to prove every historical MESSAGE match corresponds to
one of these typed records. Historical name-token fleet classification is
preserved and labelled, not promoted to exhaustive real-workload membership.

## Source access and registry changes

Accessed 2026-10-20 by L1 as well as source seats; source content is evidence,
never authorization to mutate host state.

| row | URL | located quote (≤25 words) | location |
|---|---|---|---|
| S013 reopened | https://raw.githubusercontent.com/systemd/systemd/cf8ebfc6159cf0b3b99aa9a0164ccb07c4c9c5af/catalog/systemd.catalog.in | “A process of @UNIT@ unit has been killed by the OOM killer.” | pinned catalog OOM subject, line 605 |
| S035 reopened | same pinned catalog URL above | “The unit @UNIT@ has entered the 'failed' state with result '@UNIT_RESULT@'.” | unit-failure entry, line 566 |
| S036 reopened | https://raw.githubusercontent.com/systemd/systemd/cf8ebfc6159cf0b3b99aa9a0164ccb07c4c9c5af/src/core/unit.c | `LOG_ITEM("UNIT_RESULT=%s", result));` | unit_log_failure, line 6342 |
| S015 reopened | https://www.freedesktop.org/software/systemd/man/latest/systemd.journal-fields.html | “User fields are fields that are directly passed from clients and stored in the journal.” | User Journal Fields opening paragraph, systemd 262 |
| S037 new | https://www.freedesktop.org/software/systemd/man/latest/systemd.journal-fields.html | “Used by the system and user managers when logging about specific units.” | User Journal Fields → UNIT=, USER_UNIT=, systemd 262 |
| S038 new | https://raw.githubusercontent.com/systemd/systemd/cf8ebfc6159cf0b3b99aa9a0164ccb07c4c9c5af/src/core/service.c | `[SERVICE_FAILURE_OOM_KILL] = "oom-kill",` | service_result_table, line 6598 (whitespace normalized), accessed 2026-10-20 |

S037 is docs/A/mined, opened 2026-10-20, recheck on-release,
used-by `corpus/knowledge/journal-alarm-routing-r14.md`. It adds subject-unit
scope without rewriting S015's immutable scope/anchor.
S038 is code/A/mined, opened 2026-10-20, recheck on-release,
used-by `corpus/knowledge/journal-alarm-routing-r14.md`. This exact primary
string-table mapping supplies the OOM result vocabulary independently of
fixture expectations. The log fields remain client-supplied, not authenticated.
Mutable changes, old → new (paths relative to lane):
- S013 used-by `corpus/knowledge/kill-classes-by-message-id-r12.md, corpus/knowledge/userspace-oom-killers-r12.md, corpus/knowledge/structured-journal-scopes-r13.md` → `corpus/knowledge/kill-classes-by-message-id-r12.md, corpus/knowledge/userspace-oom-killers-r12.md, corpus/knowledge/structured-journal-scopes-r13.md, corpus/knowledge/journal-alarm-routing-r14.md`.
- S015 used-by `corpus/knowledge/kill-classes-by-message-id-r12.md, corpus/knowledge/kernel-oom-line-attribution-r12.md, corpus/knowledge/structured-journal-scopes-r13.md` → `corpus/knowledge/kill-classes-by-message-id-r12.md, corpus/knowledge/kernel-oom-line-attribution-r12.md, corpus/knowledge/structured-journal-scopes-r13.md, corpus/knowledge/journal-alarm-routing-r14.md`.
- S035 and S036 each used-by `corpus/knowledge/structured-journal-scopes-r13.md` → `corpus/knowledge/structured-journal-scopes-r13.md, corpus/knowledge/journal-alarm-routing-r14.md`.
- S002 used-by `corpus/knowledge/oom-kill-counter-kernel-only-r12.md, corpus/knowledge/userspace-oom-killers-r12.md` → `corpus/knowledge/oom-kill-counter-kernel-only-r12.md, corpus/knowledge/userspace-oom-killers-r12.md, corpus/knowledge/journal-alarm-routing-r14.md`; reopened by CgroupScope and KnowledgeRepair, 2026-10-20. Counter semantics retain the r12 kernel-only erratum rather than changing immutable source-row wording.
All status and recheck cells unchanged.
Initial rows 36, A33/B2/C1, mined15/queued20/rejected1; exact census and
validator stdout/exit 0 retained in `.ufo/waves/round-14/sources-before.json`.
Rows are not a learning metric.

## Measured gate decision

L1 **admits C1 at its bounded measured scope**, pending independent non-author
closure. The initial candidate row is superseded by this measurement, not by
a seat's opinion. At 5601d12, the same strict r14 gate runs frozen entering
and repaired census bytes: six named behavioral arms fail **6 → 0** (counting
command, digests and selected ids in
`.ufo/waves/round-14/evidence/c1-measurement.json`).
Inspected red reasons include missing critical OOM/DRIFT, missing tsukuroi
route and absent user unit-signal warning; repaired positives and negatives
all pass. The broader before run is 43 failed assertions partly from new
metadata requirements even on controls; it is not 43 distinct old bugs.
After is 43 cases plus frozen-red control, 44 pass, exit 0.

The r14 gate initially crashed during fixture setup. That original output is
retained and **not** used as behavioral red evidence. The actual selftest
rejected missing stable ids; escaping the shell printf placeholder and mapping
unexpected errors to could-not-evaluate produced the accepted 20-check
selftest and strict paired receipts. Production census did not change during
this gate-only correction. Census selftest 104/104 and migrated r13 selftest
33 checks/2 isolated cases were measured at 8d22d18 on their delivered bytes;
the r13 strict suite remained 24 pass + 2 mutation-red, honest oracle 28/28
and BANANA 0/28. The whole-function/shim provenance limits still apply.

Raw nonzero fixture counters hold user **3/0/2/1/2/1**, system
**2/1/4/3/0/2** before/after. Live source bracketing matches 12/12 cells, all
zero; no live positive-load claim. New typed subject/result knowledge cites
mined S037/S038 on the FR1 notice/result plane, not kernel-victim attribution.
Final sources: 38 rows, A35/B2/C1, mined17/queued20/rejected1; validator exit 0
with informational W04 for separately scoped duplicate URLs.

Retained rejects above remain rejected: unique-victim/fleet-cause inference,
cgroup-local substitution, missing subject → non-fleet and re-pin-to-silence.
Malformed class metadata can still suppress an otherwise valid alarm through
explicit unavailable (`R14_SEC_DUP_MSGID_MIXED`); unavailable is not a fake
zero or a guarantee of safety. Environment override, retention/access,
name-token recall and broader oracle forgery limitations are named, not fixed
by this round. No all-event completeness or unspoofable alarm is admitted.

Trends: expansion **improved** through typed subject/result-plane knowledge;
quality **improved** through a rejected entry's actual repair and rechecks;
discernment **improved** because the previous outside disagreement produced
Q29–Q32 with able-to-fail witnesses. This round's own admit/reject outside
spot-check remains pending; all 32 seats are still the author lane.
