# KnowledgePositive — Round 15: validated positives under an invalid aggregate

- **Seat:** `MoriR15.KnowledgePositive` (leaf executor, knowledge + report only)
- **Lane root:** `/home/vgpnk/Projects/shokunin/mori-shokunin`
- **Milestone:** retain validated positives without fabricated totals
- **Assigned production file:** `corpus/knowledge/journal-positive-evidence-r15.md` (new)
- **Report:** `.ufo/waves/round-15/build/KnowledgePositive.md`
- **Status:** landed. No production code, no builds/tests, no measurement, no commits.

## Files changed

1. `corpus/knowledge/journal-positive-evidence-r15.md` — new 330-line knowledge note.
2. `.ufo/waves/round-15/build/KnowledgePositive.md` — this report.

No other file was edited. `corpus/SOURCES.md` used-by cells were handled by the
RegistryFrontier owner after my confirmation; I did not edit the registry. `corpus/README.md` is
handled by the IndexPositive owner; I supplied the Holds line and headings and did not edit it.

## What the note establishes

The note separates two claims that the r14 parser conflated:

- **Aggregate total:** every record returned for a class in the current boot passed the identity
  and scope preconditions; the count and splits are then meaningful.
- **Positive witness:** one object record independently passed the same identity/scope
  preconditions plus the class predicate. It can support the existing OOM/signal alarm even when
  an adjacent record makes the aggregate unavailable.

New per-scope tokens: `positive_kernel_oom`, `positive_unit_oom`, `positive_unit_signal`,
`positive_process_sigkill`. Predicates:

| token | identity | class predicate |
|---|---|---|
| `positive_kernel_oom` | object; scalar `_BOOT_ID` = current boot; scalar `MESSAGE_ID` = `fe6faa94e7774663a0da52717891d8ef` | none beyond identity |
| `positive_unit_oom` | object; scalar current `_BOOT_ID`; scalar `MESSAGE_ID` = `d9b373ed55a64feb8242e02dbe79a49c` | `UNIT_RESULT` exactly `oom-kill` |
| `positive_unit_signal` | object; scalar current `_BOOT_ID`; scalar `MESSAGE_ID` = `d9b373ed55a64feb8242e02dbe79a49c` | `UNIT_RESULT` exactly `signal` |
| `positive_process_sigkill` | object; scalar current `_BOOT_ID`; scalar `MESSAGE_ID` = `98e322203f7a4ed290d09fe03c09fe15` | `EXIT_CODE` exactly `killed`; `EXIT_STATUS` scalar equal to `9` |

Contract points the note makes explicit:

- Positives come from the same successful, stderr-free parsed capture; no second journal query,
  no retry, no line-by-line malformed-JSON repair.
- Capture/parser failure makes the positive fields `unavailable:<reason>`, not `0`.
- Invalid/nonmatching records are excluded from positives; they still make the raw aggregate
  `unavailable:<reason>`, never a partial count or a fabricated zero.
- One OOM critical line fires if any independently valid OOM positive exists, even when raw
  counts remain unavailable. One user `KILL_SIGNAL_JOURNAL` warning fires from either valid user
  signal arm. System signal stays non-warning.
- Raw counters, result subsets and the fleet/non-fleet/unattributed INFO partition stay
  aggregate-only. Positives do not repair them, do not become a route/actuation, and are never
  summed across scopes or sources.
- No authentication: all non-underscore fields are client-supplied; `_BOOT_ID` is the only
  trusted scope anchor.
- No completeness, unique victim, event-time, signal-sender/cause, or fleet-membership claim.
- Positive counts are records, may include duplicates, and are not deduplicated.
- FR1 failure-mode coverage is expanded; kernel event-time attribution and fleet correlation
  remain Frontier.

The note includes a 9-row decision table (homogeneous valid; valid zero; valid positive plus
identity-invalid; only-invalid/no-positive; unit result-field defects; unknown subject; process
field defect; capture/JSON failure; duplicates/order) and a separate alarm-contract section.
It predicts no measurement and claims no receipt; any actual measurement is L1-appended.

**Explicit r14 :221 correction and crosslink.** The note states that r14's “positive validated
records” meant a class whose every returned record passed validation (a validated *class count*),
not the r15 per-record positive subset. It keeps r14's “no positive alarm from an unavailable
class” for an unavailable *positive field*/capture failure, and corrects the class-level reading:
an aggregate class may be unavailable while independently validated positive records in the same
parsed stream fire the alarm. It crosslinks the r14 disclosed mixed-stream limitation
(`R14_SEC_DUP_MSGID_MIXED`, `journal-alarm-routing-r14.md:386-390`) as the failure mode this
round narrows, and says the limitation is not closed for malformed JSON, capture failure, or a
stream whose only positive is itself identity-invalid. The note also states the rule is a
conditional witness rule, not a universal survivor guarantee.

## Source evidence reopened by this seat (access date 2026-10-20)

All four URLs were fetched/reopened on 2026-10-20. Quotes below are exact normalized substrings
of the fetched bytes and are ≤25 words each (word count in parentheses).

### S014 — journalctl(1)

- URL: https://www.freedesktop.org/software/systemd/man/latest/journalctl.html
- Revision observed: systemd 262; `Last-Modified: Tue, 22 Sep 2026 13:31:34 GMT`; fetched
  sha256 `75440570fb1f71859229ca88fed0a6764b2057c7dd90651701b3d022a5649722`.
- Located quotes:
  - “Journal entries permit non-unique fields within the same log entry.” (10)
  - “if a non-unique field is encountered a JSON array is used as field value, listing all field
    values as elements.” (20)
  - “Fields larger than 4096 bytes are encoded as null values.” (10)
  - “Fields containing non-printable or non-UTF8 bytes are encoded as arrays containing the raw
    bytes individually formatted as unsigned numbers.” (19)
  - “A comma separated list of the fields which should be included in the output.” (14)
  - “Show messages from a specific boot.” (6)
  - “except when the current boot is not the last boot” (10)
- Used for: query-time boot match, JSON array/null/numeric-array encoding (the structural reason
  a non-scalar field is not a match), and field-limited capture with no `MESSAGE`.

### S015 — systemd.journal-fields(7)

- URL: https://www.freedesktop.org/software/systemd/man/latest/systemd.journal-fields.html
- Revision observed: systemd 262; `Last-Modified: Tue, 22 Sep 2026 13:31:36 GMT`; fetched
  sha256 `906e5d34b38913ddaf729f74f468f5511f8a143bb3f86f0fdda06957af7bf5e7`.
- Located quotes:
  - “A 128-bit message identifier ID for recognizing certain message types, if this is
    desirable.” (14)
  - “This should contain a 128-bit ID formatted as a lower-case hexadecimal string, without any
    separating dashes or suchlike.” (18)
  - “Fields prefixed with an underscore are trusted fields, i.e. fields that are implicitly
    added by the journal and cannot be altered by client code.” (24)
  - “The kernel boot ID for the boot the message was generated in, formatted as a 128-bit
    hexadecimal string.” (18)
  - “User fields are fields that are directly passed from clients and stored in the journal.”
    (15)
- Used for: exact 128-bit ID matching, trusted `_BOOT_ID` as the current-boot anchor, and the
  client-supplied status of `MESSAGE_ID`/`UNIT_RESULT`/`EXIT_*`/subject fields.

### S037 — subject-unit metadata (same journal-fields page)

- URL: https://www.freedesktop.org/software/systemd/man/latest/systemd.journal-fields.html
- Same page and fetch as S015; reopened 2026-10-20.
- Located quotes:
  - “The name of a unit. Used by the system and user managers when logging about specific
    units.” (17) — `UNIT=`/`USER_UNIT=`.
  - “the process the journal entry originates from” (7) — trusted `_SYSTEMD_UNIT=` emitter
    metadata.
- Used for: positivity never reads subject fields; a valid unit OOM/signal result still alarms
  with absent/ambiguous subject; the fleet/non-fleet/unattributed INFO partition stays
  aggregate-only; `_SYSTEMD_UNIT` is never used for subject classification or positive
  validation.

### S038 — pinned service result vocabulary

- URL: https://raw.githubusercontent.com/systemd/systemd/cf8ebfc6159cf0b3b99aa9a0164ccb07c4c9c5af/src/core/service.c
- Revision: pinned commit `cf8ebfc6159cf0b3b99aa9a0164ccb07c4c9c5af`; fetched sha256
  `669cccf4356bd838b0ac9541ef435c9c1307f989a36f2c0f35584b8184d7731f`.
- Located literals (table alignment spaces normalized):
  - `SERVICE_FAILURE_SIGNAL` maps to `"signal"` at `:6594`.
  - `SERVICE_FAILURE_OOM_KILL` maps to `"oom-kill"` at `:6598`.
- Used for: exact, case-sensitive result vocabulary; establishes the emitted spellings, not
  emitter authenticity.

Catalog IDs and the unit-notice/process-exit semantics are carried from the r14 note and
S013/S035; this seat did not reopen S013/S035 this round, and the note says so.

## Verification performed

- Quote audit: every source quotation in the note was checked programmatically as a normalized
  exact substring of the fetched source bytes; all source quotes are ≤25 words (maximum 24).
- Source identity: SHA-256 of each fetched body recorded in the note header; `Last-Modified`
  recorded for the two `latest` man pages; S038 is commit-pinned.
- No journal query, census run, fixture execution, gate run, drift-pin change, build, lint,
  test, formatter or smoke run was performed (leaf editing-wave contract).
- No tool install or upgrade was performed (no pacman/uv/cargo/npm/official-binary install), so
  the parent's sync-DB safety ruling was not engaged.
- No commit, push, deploy or external-state remediation.

## Risks, residuals and blockers

- **Residual suppression is narrowed, not closed.** A malformed-JSON stream, a capture
  failure/timeout/stderr byte, or a case where the only positive record is itself
  identity-invalid still loses the alarm. The note states this explicitly.
- **Unit result defects versus process field defects.** Existing r14 semantics are retained: a
  non-scalar/wrong `UNIT_RESULT` does not invalidate the unit raw total (it is result-unknown or
  nonmatching), while the process class's `killed`/`9` pair is part of its all-records predicate,
  so a bad process status record makes that class unavailable. The note distinguishes these
  rather than applying one blanket invalidation rule.
- **Positives are not totals.** A zero positive beside an invalid aggregate means “no valid
  witness observed,” not zero records/events. A positive count may include duplicate records and
  is not a victim/event count.
- **No live mixed-stream prevalence is established.** Whether the host currently has a valid
  positive adjacent to an invalid record is unmeasured; the note says so.
- **`latest` man pages can drift.** Hashes and `Last-Modified` pin this observation; host systemd
  version equivalence is not claimed. S038 host-binary equivalence is not claimed either.
- **No blockers.** The assigned knowledge note and report are complete; index/registry owners
  were given the exact path, summary, headings and four-source confirmation.

## Coordination notes

- `MoriR15.RegistryFrontier` confirmed the four used-by cells (S014/S015/S037/S038) after I
  confirmed the note cites/uses all four; the exact filename is unchanged.
- `MoriR15.IndexPositive` received the Holds line, exact headings, “no measured receipt/
  interface-only” status, and landed-path confirmation. It will verify bytes before indexing.
