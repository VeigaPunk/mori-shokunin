# Round 15 — partial positive evidence without complete totals

date: 2026-10-20 · lane: mori-shokunin · entering commit: `0fa5e0d`.
Record: LOG.md round-15; fleet report `.ufo/reports/round-15/mori.md`.

## Declared claim

C1 coverage works the lowest owned non-retired axis (6 versus operability7):
retain OOM critical/DRIFT and user-signal WARN/DRIFT from individually valid
current-boot structured records when another record invalidates the aggregate
class. Aggregate totals and subject partitions remain unavailable. Additive
positive evidence is not a replacement complete total, unique-victim count,
authenticated emitter or fleet-cause claim. No malformed-JSON recovery.

## Mistakes

| id | class | evidence pointer | captured-by | fix |
|---|---|---|---|---|
| M1 | attribution | `round-14-verifier-spotcheck.md:83,136`: `dirty=true` without retained exact porcelain | Q2/Q31; PROTOCOL two evidences | Retain start/end porcelain path scope in new receipts and hash verdict-driving inputs; freeze committed input before measurement. This does not reconstruct unknown historical dirty paths. |
| M2 | scope | `round-14-verifier-spotcheck.md:137`; `knowledge/journal-alarm-routing-r14.md:218–222,386–390` | Q3/Q25/Q29 | The r14 phrase “fail-loud on positive validated records” meant positive validated **class counts**, not every record; mixed invalid records could suppress otherwise valid positives. The new r15 note explicitly supersedes that active reading. The r15 frozen-red comparison must fail that suppression case before repair counts. |
| M3 | scope | `round-14-verifier-spotcheck.md:138`; r14 note `:382–384` | Q3/Q16 | Legacy KILL_SIGNAL `count`/`process_sigkill` can be `unavailable:<reason>` while an independently available user-unit signal arm raises WARN. Neither unavailable nor the distinct unit-signal count is a fabricated process zero. SCORECARD nonzero vectors are explicitly fixture observations in this round's correction. |
| M4 | scope | `.ufo/waves/round-15/build/AttackProvenance.md`, completion admits `agent://all` broadcast reached Main/other lanes | campaign prompt §6.2 expressly forbids `agent://all` | L1 sent exact-id correction to every seat; no broadcast is authorized. This procedural violation is disclosed, not counted as a successful tested repair or hidden by the otherwise bounded production work. |
| M5 | scope | `.ufo/waves/round-15/build/RegistryFrontier.md:63–72` states source fetches were written under `/tmp` | lane-only seat write contract | Temporary source downloads are not admitted durable evidence or an authorized lane write expansion. L1 independently reopened the canonical URLs; these outside-lane temporary writes are disclosed as procedural debt, not silently treated as conformant. |
| M6 | scope | HarnessBuild handoff reports isolated-wrapper selftests and repeat checks before L1's integration barrier | wave contract forbids seat builds/tests/gate runs | L1 stopped further seat verification and does not use those runs as the delivered production proof. Main verification is recorded separately after committed inputs settle; the midflight check violation remains disclosed. |

The prior raw nonzero vectors in SCORECARD.md round-14 (`3/0/2/1/2/1`
user and `2/1/4/3/0/2` system) are **fixture vectors**, not live positive
load. Live 12/12 zero agreement was only the cited r14 boot/window.

## Gate

Admission bar: corpus/QUALITY.md. The 64 dispatched seats are author-lane
advisers, not the required non-author verifier. Independent round-15 outside
admit/reject sampling is pending closure.

| candidate | decision | reason |
|---|---|---|
| Individually validated positive alarm evidence alongside unavailable aggregate totals | candidate until measured receipt is appended | Separate evidence of presence from unsupported completeness; matching current boot and scalar class/result guards remain mandatory. |
| Treat an invalid aggregate as zero or infer health from no validated positive | rejected | No positive witness does not prove a complete scan or absence of events. |
| Parse MESSAGE or salvage syntactically malformed JSON for alarms | rejected | No safe structured evidence is available; capture/parser failure stays unavailable. |
| Treat foreign-boot/array-valued identifiers or malformed result values as positive evidence | rejected | They do not satisfy the admitted scalar current-boot record predicate. |
| Re-pin old drift baseline merely to silence red | rejected | The carried r10 pin remains status-neutral conformance debt; this round performs no semantic re-pin. |

## Routed items disposition

All six items in the r14 outside record are retained: exact dirty scope is
new provenance work (not retroactive reconstruction); active wording and
legacy signal availability are clarified by this lesson and the new r15
knowledge/skill interface; old drift pin remains red debt with no re-pin;
prior r13 repair qualifications, trust/access/retention/name-token limits
remain; SHONEN boxes stay unchecked and promotion remains operator-owned.
Protected verifier/aggregator artifacts are not edited.

## Source openings

L1 reopened on 2026-10-20:
- S014, https://www.freedesktop.org/software/systemd/man/latest/journalctl.html,
  systemd262 Filtering Options → `--boot`: “This will add a match for
  \"_BOOT_ID=\".” Source selection does not authenticate client MESSAGE_ID.
- S015/S037, https://www.freedesktop.org/software/systemd/man/latest/systemd.journal-fields.html,
  Description: “field values that may include binary data, and with non-unique
  field names permitted.” User fields opening: “User fields are fields that are
  directly passed from clients and stored in the journal.”

No new row is preclaimed. Registry changes and measured gate decisions are
appended only after their actual evidence is available.

### Registry changes — opened sources, existing scopes

RegistryFrontier reopened S014/S015/S037/S038 on 2026-10-20; L1 also opened
the three distinct URLs (S015/S037 share one). No new row, status change or
recheck change is warranted. Existing scopes cover the field/boot/result
rules; no row count is treated as learning.

| row | used-by old → new |
|---|---|
| S014 | `corpus/knowledge/kill-classes-by-message-id-r12.md, corpus/knowledge/kernel-oom-line-attribution-r12.md, corpus/knowledge/structured-journal-scopes-r13.md` → `corpus/knowledge/kill-classes-by-message-id-r12.md, corpus/knowledge/kernel-oom-line-attribution-r12.md, corpus/knowledge/structured-journal-scopes-r13.md, corpus/knowledge/journal-positive-evidence-r15.md` |
| S015 | `corpus/knowledge/kill-classes-by-message-id-r12.md, corpus/knowledge/kernel-oom-line-attribution-r12.md, corpus/knowledge/structured-journal-scopes-r13.md, corpus/knowledge/journal-alarm-routing-r14.md` → `corpus/knowledge/kill-classes-by-message-id-r12.md, corpus/knowledge/kernel-oom-line-attribution-r12.md, corpus/knowledge/structured-journal-scopes-r13.md, corpus/knowledge/journal-alarm-routing-r14.md, corpus/knowledge/journal-positive-evidence-r15.md` |
| S037 | `corpus/knowledge/journal-alarm-routing-r14.md` → `corpus/knowledge/journal-alarm-routing-r14.md, corpus/knowledge/journal-positive-evidence-r15.md` |
| S038 | `corpus/knowledge/journal-alarm-routing-r14.md` → `corpus/knowledge/journal-alarm-routing-r14.md, corpus/knowledge/journal-positive-evidence-r15.md` |

S038 URL:
https://raw.githubusercontent.com/systemd/systemd/cf8ebfc6159cf0b3b99aa9a0164ccb07c4c9c5af/src/core/service.c
— `service_result_table:6588–6602`, quote
`[SERVICE_FAILURE_OOM_KILL] = "oom-kill",` (whitespace normalized), opened
2026-10-20. S037 located quote, User Journal Fields → UNIT=/USER_UNIT=:
“Used by the system and user managers when logging about specific units.”

### Advisory adjudication

Seat reports are historical observations at their own read time, frequently
before sibling edits landed; an absent-feature observation is not the final
tree verdict. Suggestions calling client-supplied records “authentic kills,”
assigning probability 1 to unenumerated streams, or raising coverage6→7
without a declared rubric are rejected. A 32-hex boot shape is not emitter
authentication, and ignored-filter fixtures are parser-robustness evidence,
not positive-load live attacks. The canonical metric remains measured finite
case assertions with separate alarm-loss counts, never a universal probability.

The new positive counters join existing count-magnitude normalization;
field existence/severity/verdict changes remain visible. This intentionally
changes the declared volatile-field set and does not bless the old red pin.
The contrary suggestion to leave only new count magnitudes unmasked is not
adopted; no whole-freshness improvement is claimed.

### Integration corrections before measurement

L1 separated two active SKILL phrasings: semantic aggregate invalidity permits
positive evidence; unsuccessful/stderr-bearing/syntactically invalid capture
does not. The illustrative failure list no longer conflates `record-invalid`,
`multi-boot` or `boot-mismatch` with JSON syntax failure.

L1 added explicit object-condition branches before aggregate field indexing,
plus three isolated census selftest cases: valid notice with primitive JSON
neighbors, primitives alone, and valid notice with truncated JSON. These
remove dependence on boolean short-circuit behavior for the object boundary;
the last case must still refuse arbitrary JSON salvage. The producer's
earlier conditional non-object caveat is superseded only if those delivered
tests pass, not by a static prediction.

The final internal gate review identified control-trust defects (any frozen
failure counted as red, and hidden flags could bypass the control), plus
bounded capture/provenance/path issues. They are routed back to the same
gate owner before pinning or measurement. A future receipt is not assumed
green merely because the source author called it finished.

### Boundary mistake found by L1

Class **scope** · evidence
`.ufo/waves/round-15/evidence/boundary-pin-red.json` · captured-by Q3/Q6/Q35 ·
fix: the gate's static trigger derivation must ignore a failed capture's
positive-looking bytes, while preserving positives from an unaffected scope.
The first boundary pin exited2 with an actual contradiction at `boundary_rc124`.
It is not counted as a production failure. The successful regenerated boundary
table includes that unchanged failing case plus a separately added surviving
other-scope case; no claim of whole-pack byte-identical causal isolation is
made for this setup repair. Core C1 red/green isolation remains the original
63 unchanged fixture cases on identical gate bytes.

## Measured Gate decision

The lane admits the bounded C1 knowledge and capability **pending independent
non-author closure**. At 1822145, final same-gate before/after behavioral
failures are34→0, core green63/63, frozen missing-alarm controls34/34, with
no inconclusive controls. Seven additional capture-boundary cases pass.
The counting command and actual values are in
`.ufo/waves/round-15/evidence/c1-measurement.json`; the paired manifests retain
all captured runs. The initial candidate row under `## Gate` is superseded
by this measured decision, not by an internal seat's endorsement.

Rejects remain rejected: no absence/health inference from subset0; no
MESSAGE or malformed-JSON salvage; no foreign/array identity promotion;
no re-pin-to-silence. The current delivered gate refuses the former hidden
control-bypass flags with exit2, and its selftest checks completed control
misses separately from exec error/timeout/integrity failure. These are actual
L1 executions over committed inputs, not the earlier midflight seat checks.

Source census before and after both exit0 with the same W04 informational
duplicate-URL warnings. `sources-before.json` and `sources-after.json` under
the round-15 wave retain stdout/rc/counts. Rows38→38, A35/B2/C1 held,
mined17/queued20/rejected1 held; rows added A0/B0/C0. Four used-by changes
are logged above; status/recheck unchanged. One new admitted knowledge entry
advances FR1 failure-mode ground, not kernel attribution or all-event scope.

Current outside admit/reject sampling remains pending; all 64 seats are the
author lane. M4–M6 procedural debt is disclosed and not called a passed gate.
