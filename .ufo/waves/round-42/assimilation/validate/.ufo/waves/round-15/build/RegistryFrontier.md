# RegistryFrontier — round 15

- **Seat:** `MoriR15.RegistryFrontier` (executor, leaf member)
- **Owned file:** `corpus/SOURCES.md` only
- **Judged on:** coverage
- **Milestone:** retain validated positives without fabricated totals
- **Report path:** `.ufo/waves/round-15/build/RegistryFrontier.md`
- **Lane root:** `/home/vgpnk/Projects/shokunin/mori-shokunin`

No build, test, lint, format, smoke or verification command was executed. No subagent,
background job, commit, push or sibling-file write was made. No tool was installed or updated.
No row was added: the reopened material falls inside the existing immutable scopes.

## 1. Axes named

- **Coverage:** the new r15 positive-evidence knowledge document is attributable, in the
  registry, to the four primary sources its lane actually reopens and uses, so a later reader can
  re-derive the positive-class/current-boot rules from S014/S015/S037/S038 instead of treating
  them as unsourced harness behavior.
- **No harm:** existing raw counts, unavailable semantics and every immutable registry cell are
  untouched; only the four `used-by` cells gain one trailing path, so prior knowledge paths and
  row scopes remain exactly as before.

## 2. File changed

`corpus/SOURCES.md` — four `used-by` cells only. `git diff --stat` reports
`1 file changed, 4 insertions(+), 4 deletions(-)`; each change is a line replacement whose only
content difference is the appended path.

### 2.1 Exact old → new cells

| Row | Old `used-by` cell | New `used-by` cell |
|---|---|---|
| S014 | `corpus/knowledge/kill-classes-by-message-id-r12.md, corpus/knowledge/kernel-oom-line-attribution-r12.md, corpus/knowledge/structured-journal-scopes-r13.md` | `corpus/knowledge/kill-classes-by-message-id-r12.md, corpus/knowledge/kernel-oom-line-attribution-r12.md, corpus/knowledge/structured-journal-scopes-r13.md, corpus/knowledge/journal-positive-evidence-r15.md` |
| S015 | `corpus/knowledge/kill-classes-by-message-id-r12.md, corpus/knowledge/kernel-oom-line-attribution-r12.md, corpus/knowledge/structured-journal-scopes-r13.md, corpus/knowledge/journal-alarm-routing-r14.md` | `corpus/knowledge/kill-classes-by-message-id-r12.md, corpus/knowledge/kernel-oom-line-attribution-r12.md, corpus/knowledge/structured-journal-scopes-r13.md, corpus/knowledge/journal-alarm-routing-r14.md, corpus/knowledge/journal-positive-evidence-r15.md` |
| S037 | `corpus/knowledge/journal-alarm-routing-r14.md` | `corpus/knowledge/journal-alarm-routing-r14.md, corpus/knowledge/journal-positive-evidence-r15.md` |
| S038 | `corpus/knowledge/journal-alarm-routing-r14.md` | `corpus/knowledge/journal-alarm-routing-r14.md, corpus/knowledge/journal-positive-evidence-r15.md` |

All other S014/S015/S037/S038 cells (`source`, `kind`, `tier`, `scope`, `anchor`, `teaches`,
`status`, `opened`, `recheck`) are byte-unchanged. No row was added, removed or reordered.

### 2.2 Why all four are genuinely used

The knowledge lane `MoriR15.KnowledgePositive` was assigned
`corpus/knowledge/journal-positive-evidence-r15.md` and its prompt names
“S014/S015/S037/S038 URLs reopened yourself”. Direct peer confirmation (agent message,
2026-10-20) states the document uses all four, with these facets:

- **S014:** `--boot` adds a `_BOOT_ID=` match; JSON encodes duplicate fields as arrays;
  `--output-fields` limits the returned fields.
- **S015:** `MESSAGE_ID` is a 128-bit identifier; `_BOOT_ID` is trusted; non-underscore fields are
  client-supplied.
- **S037:** `UNIT=`/`USER_UNIT=` name the unit a manager logs about (subject, not emitter).
- **S038:** `service_result_table` provides the exact `oom-kill` and `signal` literals.

Those facets map directly to the r15 rule that only records with a scalar matching `MESSAGE_ID`
and a scalar current `_BOOT_ID` are positive, and that only the exact result strings
`oom-kill`/`signal` classify unit positives. No other source in this seat's assignment is
attributed.

## 3. Reopen record — 2026-10-20

Two URLs cover the four rows: S037 shares the S015 `systemd.journal-fields(7)` URL; the
S014 and S015 pages both self-identify as **systemd 262**. Fetched artifacts were written outside
the repository (`/tmp`) and hashed; no content was edited.

| Row | URL | Response | Version marker | Digest / size |
|---|---|---|---|---|
| S014 | https://www.freedesktop.org/software/systemd/man/latest/journalctl.html | HTTP 200; `Last-Modified: Tue, 22 Sep 2026 13:31:34 GMT`; `ETag: "1554f-65c1262a14f2e"` | systemd 262 | SHA-256 `75440570fb1f71859229ca88fed0a6764b2057c7dd90651701b3d022a5649722`; 87,375 bytes |
| S015 | https://www.freedesktop.org/software/systemd/man/latest/systemd.journal-fields.html | HTTP 200; `Last-Modified: Tue, 22 Sep 2026 13:31:36 GMT`; `ETag: "846c-65c1262c73680"` | systemd 262 | SHA-256 `906e5d34b38913ddaf729f74f468f5511f8a143bb3f86f0fdda06957af7bf5e7`; 33,900 bytes |
| S037 | same URL as S015 (distinct subject-metadata scope) | HTTP 200; same headers/digest | systemd 262 | same digest as S015 |
| S038 | https://raw.githubusercontent.com/systemd/systemd/cf8ebfc6159cf0b3b99aa9a0164ccb07c4c9c5af/src/core/service.c | HTTP/2 200; git blob `etag: "26a3f300683356941c2651a5e32cf831dcbfd2f7d7ed79592a6f52fd134e9dd5"` | pinned commit `cf8ebfc6159cf0b3b99aa9a0164ccb07c4c9c5af` | SHA-256 `669cccf4356bd838b0ac9541ef435c9c1307f989a36f2c0f35584b8184d7731f`; 280,758 bytes |

### 3.1 Located quotes (≤25 words each; fetched-page line numbers)

**S014 — journalctl(1), systemd 262**

- `--after-cursor=` (`:120-121`): “Start showing entries from the location in the journal after
  the location specified by the passed cursor.” (17 words)
- `--boot=` (`:127-128`): “Show messages from a specific boot. This will add a match for
  `_BOOT_ID=`.” (13 words) — supports current-boot selection by a `_BOOT_ID=` match.
- `json` (`:209`): “formats entries as JSON objects, separated by newline characters” (10 words) —
  one record per line in the captured stream.
- `json` duplicate-field rule (`:213-215`): “if a non-unique field is encountered a JSON array is
  used as field value” (14 words) — an array value is not a scalar and cannot satisfy the
  scalar-field positive test.
- `--output-fields=` (`:230-231`): “A comma separated list of the fields which should be included
  in the output.” (14 words) — supports the same already-captured, field-limited stream.

**S015 — systemd.journal-fields(7), systemd 262**

- `MESSAGE=` (`:34-36`): “is not supposed to be parsed for metadata” (7 words).
- `MESSAGE_ID=` (`:40-43`): “A 128-bit message identifier ID for recognizing certain message
  types, if this is desirable.” (14 words).
- Trusted Journal Fields (`:83-85`): “Fields prefixed with an underscore are trusted fields, i.e.
  fields that are implicitly added by the journal and cannot be altered by client code.”
  (24 words).
- `_BOOT_ID=` (`:100-102`): “The kernel boot ID for the boot the message was generated in,
  formatted as a 128-bit hexadecimal string.” (18 words).

**S037 — same page, subject-unit scope**

- `UNIT=`/`USER_UNIT=` (`:78-83`): “Used by the system and user managers when logging about
  specific units.” (13 words) — subject metadata, not the emitting process.
- `_SYSTEMD_UNIT=` (`:93-95`): “of the process the journal entry originates from” (8 words) —
  emitter provenance, consistent with the immutable S037 teaches cell.

**S038 — service.c at pinned commit**

- `:6594` (inside `service_result_table`, `:6588-6602`):
  `[SERVICE_FAILURE_SIGNAL]          = "signal",`
- `:6598`: `[SERVICE_FAILURE_OOM_KILL]        = "oom-kill",`

Both exact literals are the only unit-result strings the r15 positive interface accepts; the
adjacent table entries (`exit-code`, `timeout`, …) are not promoted by this row.

## 4. No new rows, no immutable-cell changes

Every reopened facet lands inside an existing immutable row scope/anchor:

- S014 “journal source selection, cursor pagination and field-limited JSON output” already covers
  `--boot`/`_BOOT_ID=` selection, per-line JSON and `--output-fields`; the duplicate-field array
  encoding is part of the same JSON output contract.
- S015 “journal MESSAGE, MESSAGE_ID and trusted metadata fields” covers the MESSAGE metadata
  prohibition, the 128-bit `MESSAGE_ID` and trusted `_BOOT_ID`.
- S037 “subject UNIT/USER_UNIT versus emitting-process _SYSTEMD_UNIT metadata” covers the subject
  quote exactly.
- S038 “systemd service OOM-failure result string” covers `oom-kill`; `signal` is the same
  `service_result_table` vocabulary and was already implied by the `signal` result the r14 routing
  knowledge cites.

No genuinely novel scope was found (no new URL, no new field family, no new document class), so
no row was added and no anchor/scope/teaches cell was rewritten. This also preserves the
“retain validated positives without fabricated totals” milestone: the registry adds no count or
completeness claim.

## 5. Risks / blockers

- At the moment of the four edits, `corpus/knowledge/journal-positive-evidence-r15.md` had not yet
  landed (checked immediately before writing this report). Attribution rests on the lane
  assignment plus `MoriR15.KnowledgePositive`'s direct confirmation of the four facets above. L1
  should confirm the file lands under exactly this path and cites all four; if the delivered file
  drops a source, that `used-by` append would over-attribute and should be reverted for that row.
- If the delivered knowledge file additionally cites S035/S036, those `used-by` cells were outside
  this seat's assigned append set and were intentionally not touched; that is a separate registry
  decision for L1.
- The two documentation URLs are `latest`; their 2026-10-20 content is systemd 262. The existing
  `recheck=on-release` remains the appropriate freshness marker and was left unchanged.
- This seat ran no verification, per the lane contract; L1 owns post-integration checks.
