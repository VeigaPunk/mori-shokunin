# SourcePlan — minimal capability and failure universe for the FR11 cursor window

Seat: `MoriR16.SourcePlan` (scout). Read-only except this report. No production code,
no fixture pack, no harness, no test execution. This is advisory author-lane source
ground for the L1 planner, not outside verification and not a delivered-behavior claim.

## Axes

- **Coverage (owned, 6, lowest non-retired)** is the axis this round is allowed to
  advance. **Operability (7)** is the guardrail: every ambiguity must become a
  deterministic refusal, never a partial count.
- The move this report supports: one strict validator whose failure universe is closed
  over the stated interface. That improves coverage by making a bounded observation
  possible and protects operability by making refusal deterministic. No score move is
  claimed by this seat.

## Code state at read time

`tools/mori-journal-window.py` and `tools/mori-round16-regressions.py` were **absent**
from `tools/` at read time (`tools/` held only `mori-census.sh`,
`mori-round13/14/15-regressions.py`, and `mori-silence-cases.sh`). This report is
contract/source ground for the planner; it does not review delivered code. Wave 2 must
review the actual bytes. No live/synthetic probe was run to compensate for the absence.

## What FR11 may advance this round (and what it may not)

`SCORECARD.md:898-916` declares the round-16 capability: a bounded, read-only,
MESSAGE-free new-since-anchor observation for one named scope and boot; the first
retained record must reproduce the exact anchor cursor and boot; only later same-boot
records are observed; nearest seeks, missing anchors, boot boundaries, and
failed/truncated captures stay unavailable; no automatic cursor-state mutation and no
census cutover. `corpus/README.md:341` and `PROVINCE.md:51` keep rotation/vacuum
behavior and cross-boot ordering as FR11 remainder. `SCORECARD.md:916-919` fixes the
metric: finite committed CLI cases, capability absent at the entering revision versus
delivered implementation; absence is capability red, not a historical production bug.

Non-claims that the implementation and report must preserve: complete retention, an
authenticated emitter, unique victims, universal ordering, alarm/severity override,
and any claim that a zero means no event occurred.

## Primary sources opened this round

All URLs opened 2026-10-20. Host tool metadata: `journalctl` **systemd 261
(261.2-1-arch)**; the man pages below are **systemd 262**. The pinned source commit is
`cf8ebfc6159cf0b3b99aa9a0164ccb07c4c9c5af` (2026-10-19), the same commit already used
by S013/S035/S036/S038 in `corpus/SOURCES.md`.

| id | source opened | observed fact used here |
|---|---|---|
| S014 | journalctl(1), systemd 262, https://www.freedesktop.org/software/systemd/man/latest/journalctl.html | `--cursor=`: "Start showing entries from the location in the journal specified by the passed cursor." `--after-cursor=`: "Start showing entries from the location ... after the location specified by the passed cursor." |
| S014 | Output Options → `--no-tail` | "Show all stored output lines, even in follow mode. Undoes the effect of `--lines=`." Source confirms `arg_no_tail` sets `arg_lines = ARG_LINES_ALL` (`journalctl.c:913-914`). |
| S014 | Output Options → `-q, --quiet` | "Suppresses all informational messages ... any warning messages regarding inaccessible system journals when run as a normal user." Errors are not suppressed. |
| S014 | Output Options → `--output-fields=` | "For the former, the `__CURSOR`, `__REALTIME_TIMESTAMP`, `__MONOTONIC_TIMESTAMP`, and `_BOOT_ID` fields are always printed." |
| S014 | Output Options → `json` | Oversized fields → `null`; non-unique fields → JSON array; non-UTF8 bytes → arrays of numbers. |
| S014 | Exit status | "On success, 0 is returned; otherwise, a non-zero failure code is returned." |
| S014 | Source Options → `--user` | `--user` "only works if persistent logging is enabled, via `Storage=`". Scope semantics are conditional, not guaranteed. |
| S015 | systemd.journal-fields(7), systemd 262, https://www.freedesktop.org/software/systemd/man/latest/systemd.journal-fields.html | `__CURSOR=`: "A cursor is an opaque text string that uniquely describes the position of an entry in the journal and is portable across machines, platforms and journal files." |
| S015 | Address Fields preamble | These fields "are not proper fields when stored in the journal" and "may also not be used as matches"; they are serialization addresses. |
| S015 | `MESSAGE_ID=` | "A 128-bit message identifier ID for recognizing certain message types"; lower-case hexadecimal, and a user (client-supplied) field. |
| S015 | Trusted Journal Fields | "Fields prefixed with an underscore are trusted fields, i.e. fields that are implicitly added by the journal and cannot be altered by client code." `_BOOT_ID=` is "The kernel boot ID ... formatted as a 128-bit hexadecimal string." |
| cursor API | sd_journal_get_cursor(3), sd_journal_test_cursor(3), systemd 262 | "Seeking to a cursor position without the specific entry being available locally will seek to the next closest (in terms of time) available entry." Also: "the same entry might be referred to by multiple different cursor strings, and hence string comparing cursors is not possible." `test_cursor` is the documented post-seek verification. |
| cursor API | sd_journal_seek_cursor(3), systemd 262 | "If no entry matching the specified cursor is found the call will seek to the next closest entry (in terms of time) instead." The seek does not position; a `next`/`previous` call selects the entry. |
| seqnum API | sd_journal_get_seqnum(3), systemd 262 | Sequence numbers are assigned when written; rewritten entries (e.g. volatile to persistent flush) "will get new sequence numbers assigned"; rotation continues the series; different journald instances have distinct sequence-number IDs. |
| format | Journal File Format, https://systemd.io/JOURNAL_FILE_FORMAT (documents the systemd 246 format; code is authoritative) | Entry objects carry seqnum, realtime, monotonic, boot_id, xor_hash; sequence numbers are unique among files with the same `seqnum_id`; rotation continues the sequence; entry arrays are sorted by on-disk offset. |
| source | `src/libsystemd/sd-journal/sd-journal.c:1292-1418` | Cursor serialization is exactly `s=<seqnum_id>;i=<seqnum>;b=<boot_id>;m=<monotonic>;t=<realtime>;x=<xor_hash>`. The parser accepts a cursor if `(s and i)` or `(m and b)` or `t` is present; otherwise `-EINVAL`. |
| source | `sd-journal.c:1187-1197` | The next-entry selector explicitly tracks the file holding the cursor's exact `seqnum_id`+`seqnum`; the comment says cross-boot ordering via `compare_boot_ids()` "can produce incorrect cross-boot ordering" without a reliable RTC (systemd issue #31516). |
| source | `src/journal/journalctl-show.c:50-103` | For `--cursor=`/`--after-cursor=`, journalctl seeks then calls `sd_journal_step_one()`. `--after-cursor=` advances only when `sd_journal_test_cursor()` says the current entry matches. If no entry follows, it sets `arg_lines = 0` and still exits 0 with empty output. |
| source | `src/journal/journalctl.c:649-650, 941, 913-914` | JSON output implies `arg_quiet = true`; `--cursor` is mutually exclusive with `--after-cursor`/`--cursor-file`/`--since`; `--no-tail` removes the line limit. |
| catalog | `catalog/systemd.catalog.in:561,568,604` | `d9b373ed55a64feb8242e02dbe79a49c` = "Unit failed"; `98e322203f7a4ed290d09fe03c09fe15` = "Unit process exited"; `fe6faa94e7774663a0da52717891d8ef` = unit process killed by the OOM killer. |
| emitter | `src/core/unit.c:6339-6392` | `unit_log_failure` writes `UNIT_RESULT=%s`; `unit_log_process_exit` writes `EXIT_CODE=%s` and `EXIT_STATUS=%i`. |
| lane | `corpus/knowledge/journal-positive-evidence-r15.md` §2, §5; `tools/mori-census.sh:1038-1055,1190-1277` | The four r15 predicates, exact catalog IDs, `EXIT_CODE == "killed"` plus scalar status 9, and the existing reason vocabulary `malformed-json`, `record-invalid`, `multi-boot`, `boot-mismatch`. |

## Minimal capability

The smallest implementation that satisfies the interface has seven parts. Everything
else is out of scope.

### M1 — Arguments and anchor validation (setup)

- Parse `--anchor PATH`, `--scope user|system`, optional `--journalctl PATH`,
  `--timeout SECONDS`, `--max-bytes N`, and `--selftest`.
- Read the anchor **once**, keep the raw bytes for a SHA-256, and decode UTF-8 strictly.
- Require a JSON object with exactly `schema`, `scope`, `boot_id`, `cursor` (recommended:
  reject extra keys, duplicate JSON keys, and non-string values). `schema` must be
  `mori-journal-anchor-v1`; anchor `scope` must equal `--scope`; `boot_id` must match
  `^[0-9a-f]{32}$`; `cursor` must be non-empty, at most 4096 characters, and
  printable with no controls (journal-generated cursors are ASCII; an ASCII-only
  check would be stricter than the interface).
- Setup failures return rc2 with `finding_id = MORI_JOURNAL_WINDOW_SETUP` and a stable
  reason. No journalctl process is spawned and no file is written.

### M2 — Search and query (one query, no MESSAGE)

Fixed argv, no shell, one scope, one cursor:

```
journalctl --user|--system \
  --cursor=<anchor.cursor> \
  --no-tail --quiet --output=json \
  --output-fields=__CURSOR,_BOOT_ID,MESSAGE_ID,UNIT_RESULT,EXIT_CODE,EXIT_STATUS
```

- Use `--cursor=` (inclusive), **not** `--after-cursor=`. The inclusive seek is what
  makes the first output record able to prove the anchor. `--after-cursor` cannot:
  journalctl only skips when `test_cursor` matches (`journalctl-show.c:84-98`), so an
  absent anchor silently starts at the nearest following entry.
- Do not pass `-b` (the anchor's boot is proven record-by-record; a `_BOOT_ID=` match
  would silently exclude a foreign-boot record instead of refusing the window),
  `--since`, a `MESSAGE_ID=` match, `-g`, `-o cat`, `--all`, `--follow`,
  `--show-cursor`, or `--cursor-file`. `--cursor-file` writes and `--show-cursor`
  appends a private-format line; both are forbidden. `MESSAGE` must never appear in
  argv or output fields.
- Do not independently read the current boot id (`/proc/sys/kernel/random/boot_id`):
  the anchor defines the boot. An older retained boot is in scope when its records
  are still in the journal; a current-boot check would wrongly refuse it.
- `--output=json` already sets `arg_quiet` internally (`journalctl.c:649-650`);
  `--quiet` is still required by the interface and additionally suppresses
  inaccessible-journal warnings. Errors still reach stderr.
- Piped stdout does not invoke a pager; `--no-pager` is not in the stated argv and is
  not required. Adding it would be semantically harmless but is an unrequested flag.

### M3 — Bounded capture

- Spawn without a shell; separate stdout/stderr pipes; never inherit the caller's
  stdin (use a closed/empty stdin).
- Enforce the deadline and the stdout byte cap **while draining both pipes**. The cap
  is inclusive: exactly `N` bytes succeeds, `N+1` refuses. A single `communicate()`
  without a cap, or an unbounded `read()`, is the known deadlock/overrun defect class;
  `ReviewCapture.md` names the same hazard in the sibling harness pattern.
- On timeout or cap: kill the child (use a process group so a wrapper's children die),
  drain, reap, and refuse. Never parse bytes collected after a kill as a window.
- Any stderr byte count > 0 is refusal, even when rc is 0. Never parse, store, or echo
  stderr bytes.
- Any non-zero rc is refusal. Do not try to interpret journalctl-specific error text.

### M4 — Strict parse and first-record anchor proof

- Decode stdout as strict UTF-8 and split into JSON Lines. An empty capture is refusal;
  a malformed/partial line is refusal; blank interior lines are refusal (recommended);
  a final line without a trailing newline is acceptable only if it parses.
- Each line must be a JSON **object**. A non-object is `record-invalid`.
- The first object must carry string `__CURSOR` equal to the anchor cursor after JSON
  decoding, with no trim, case-fold, or Unicode normalization, and string `_BOOT_ID`
  equal to the anchor boot id. For the ASCII cursors journald emits this is byte
  equality; do not compare the anchor file's escaped JSON text. Only then is the anchor
  proven; drop this record. If the entry is absent and a nearest seek produced some
  entry, the mismatch is refusal, never a window.
- Extra JSON keys are expected and must be tolerated: `--output-fields` always adds
  `__REALTIME_TIMESTAMP`, `__MONOTONIC_TIMESTAMP`, and `_BOOT_ID` (`S014`).

### M5 — Later-record validation and the four counts

Every later object must satisfy all of:

- `_BOOT_ID` is a string exactly equal to the anchor boot id (not an array, `null`,
  number, object, or a different boot);
- `__CURSOR` is a non-empty printable, control-free string of at most 4096 characters, and has
  not appeared before in this window (recommended: include the anchor cursor in the
  seen set);
- the record itself is an object.

Then, over this validated set only, count exactly the r15 predicates:

| token | predicate |
|---|---|
| `positive_kernel_oom` | `MESSAGE_ID` is the string `fe6faa94e7774663a0da52717891d8ef` |
| `positive_unit_oom` | `MESSAGE_ID` is `d9b373ed55a64feb8242e02dbe79a49c` and `UNIT_RESULT` is exactly `oom-kill` |
| `positive_unit_signal` | same id and `UNIT_RESULT` is exactly `signal` |
| `positive_process_sigkill` | `MESSAGE_ID` is `98e322203f7a4ed290d09fe03c09fe15`, `EXIT_CODE` is exactly `killed`, and `EXIT_STATUS` is scalar equal to 9 |

Missing or non-scalar predicate fields make that record non-matching for that class;
they do **not** invalidate the record (only identity/boot/cursor do). `MESSAGE_ID`
arrays or `null` are not string equality. `EXIT_STATUS`: production accepts the string
`"9"` or a JSON number numerically equal to 9 (including `9.0`/`9e0`); booleans,
arrays, objects, and other scalars are not 9. Packs should use `"9"` or integer `9`.
WindowTool should align with `ExistingPredicates` and `mori-census.sh:1054`; do not
add a broader coercion. Cursor uniqueness is a rejection guard only: do not sort by
cursor or use byte equality to deduplicate events.

`records_after_anchor` is the number of validated later records, independent of class.

### M6 — Output contract, state, and non-leakage

- Success: rc0, one JSON object on stdout with
  `finding_id = MORI_JOURNAL_WINDOW_OK`, `scope`, integer `records_after_anchor`, the
  four separate integer counts, and `evidence_basis = validated-record-subsets`.
- Refusal: rc2, `finding_id = MORI_JOURNAL_WINDOW_UNAVAILABLE`, stable `reason`, no
  numeric positive totals (omit them or use a non-numeric `unavailable` marker; L1
  should freeze one form).
- Setup: rc2, `finding_id = MORI_JOURNAL_WINDOW_SETUP`, stable `reason`.
- Never echo the anchor cursor, any record cursor, any record body, any stderr bytes,
  or any `MESSAGE`. A SHA-256 of the validated anchor bytes is allowed and is the only
  anchor-derived value recommended.
- Never write the anchor, a cursor file, or any state. The anchor is never advanced.
- No timestamps, durations, PIDs, hostnames, random values, or environment-dependent
  text in stdout: the harness pins tool digests and compares cases, so output must be
  deterministic. JSON key order should be fixed by construction.

### M7 — `--selftest` (implemented, not executed by this seat)

- Must invoke the actual CLI as a subprocess with fake `journalctl` executables inside
  an isolated temporary tree; no network, no live journal, no reads of the host
  journal; assert rc and the stable finding id (and the key counts) per arm.
- Cover at minimum: valid anchor with 0 and with positive records; missing anchor
  (nearest seek); boot boundary; foreign first boot; duplicate cursor; invalid cursor
  shape; malformed/empty capture; stderr; non-zero rc; timeout; overflow; setup
  errors; stdout must not contain the raw anchor cursor.
- Implementing the selftest is not permission to run it here; L1 runs it later.

## Failure universe

The interface says "reason stable" but does not enumerate reasons. Pack authors cannot
pin `want` values until L1 freezes a closed vocabulary. The proposed vocabulary below
reuses the r13 census strings where the situation is the same (`malformed-json`,
`record-invalid`, `boot-mismatch`) and adds only cursor-window-specific names. This is
a recommendation to L1, not a source-derived requirement. Every reason must name the
**observed condition**, never a cause: use `anchor-not-retained`, never `vacuumed`,
`rotated`, `deleted`, or `rewritten`. A cursor-string mismatch can be an alias or a
missing entry and does not prove why; the docs say cursor strings are not a one-to-one
entry identity.

### Setup (rc2, `MORI_JOURNAL_WINDOW_SETUP`)

| trigger | proposed reason |
|---|---|
| anchor path missing, unreadable, or not a regular file | `anchor-unreadable` |
| anchor bytes are not UTF-8 or not valid JSON | `anchor-not-json` |
| anchor JSON is not an object | `anchor-not-object` |
| schema/schema value/keys/types wrong | `anchor-schema-invalid` |
| anchor scope not `user`/`system` | `anchor-scope-invalid` |
| anchor scope differs from `--scope` | `anchor-scope-mismatch` |
| boot id not 32 lower-case hex | `anchor-boot-id-invalid` |
| cursor empty, non-string, >4096, or contains a control | `anchor-cursor-invalid` |
| bad `--timeout`/`--max-bytes`, empty journalctl path, unknown argument | `argument-invalid` |

An anchor that is syntactically valid but semantically unusable as a cursor (for
example a string the journal parser rejects) is **not** setup: `sd_journal_seek_cursor`
returns `-EINVAL`, journalctl exits non-zero, and the result is `producer-exit`.
Setup validates shape only; the seek plus first-record proof validates meaning.

### Unavailable (rc2, `MORI_JOURNAL_WINDOW_UNAVAILABLE`)

| stage | trigger | proposed reason |
|---|---|---|
| spawn | journalctl path missing / not executable | `journalctl-unavailable` |
| spawn | other `OSError` before a child exists | `spawn-failed` |
| capture | deadline expired; child killed and reaped | `timeout` |
| capture | stdout exceeded `--max-bytes`; child killed and reaped | `capture-overflow` |
| capture | child exited non-zero (includes invalid cursor, permission error) | `producer-exit` |
| capture | any stderr bytes, even with rc 0 | `stderr-nonempty` |
| parse | stdout is empty (journalctl found no entry at/after cursor; it exits 0 — `journalctl-show.c:100-102`) | `empty-capture` |
| parse | invalid UTF-8, invalid JSON, truncated final object, blank line | `malformed-capture` |
| first record | not a JSON object, or missing/non-string cursor or boot | `record-invalid` |
| first record | object is valid but cursor differs from anchor (nearest seek) or boot differs from anchor | `anchor-not-retained` |
| later record | not a JSON object, or boot missing/non-string | `record-invalid` |
| later record | boot string differs from anchor boot (boot boundary / foreign boot) | `boot-mismatch` |
| later record | cursor missing/non-string/control/>4096 | `cursor-invalid` |
| later record | cursor repeats a cursor already seen in this window | `cursor-duplicate` |

Determinism requires a fixed precedence, for example:

1. argument/setup validation;
2. spawn;
3. whichever of deadline/byte-cap trips first (a kill is reported as `timeout` only if
   the deadline expired before the cap, otherwise `capture-overflow`);
4. non-zero rc;
5. non-empty stderr;
6. empty/UTF-8/JSON parse;
7. first-record object/anchor proof;
8. later-record validation;
9. success.

Two distinctions matter for cases:

- **Empty capture is not a zero window.** rc0 plus empty stdout is the documented
  "could not find the next entry" path, which does not prove the anchor. A genuine
  zero window contains exactly the validated anchor line, is dropped, and returns
  `records_after_anchor = 0` with numeric zero counts.
- **A malformed JSON line is not a malformed record.** Invalid JSON, a truncated final
  line, and non-UTF8 bytes refuse the whole capture (`malformed-capture`). A valid JSON
  object that fails identity/type rules refuses the window differently
  (`record-invalid`, `boot-mismatch`, `cursor-invalid`), but still refuses: this tool
  has no r15-style positive salvage and no second query.

## FR11 boundary matrix (source-grounded)

| situation | verdict | why |
|---|---|---|
| Anchor cursor retained in the queried scope and boot; first line reproduces it; later lines are same-boot objects with unique cursors | success | Inclusive `--cursor` plus exact first-record proof; later records are the validated subset. |
| Anchor entry missing or vacuumed; nearest later entry exists | unavailable (`anchor-not-retained`) | `sd_journal_seek_cursor` seeks to the nearest entry; exact cursor+boot proof fails. |
| Anchor entry rewritten by volatile→persistent flush | unavailable (`anchor-not-retained`) | Rewritten entries get new sequence numbers (`sd_journal_get_seqnum(3)`), so the exact cursor string cannot be reproduced. |
| Anchor entry only in the other scope | unavailable | Different journal files/sequence-number IDs; nearest seek cannot reproduce the exact cursor. |
| Anchor from an earlier boot; its entry is retained | unavailable if any later record is from another boot; otherwise success | Same-boot rule: the anchor boot is the reference, and the first foreign boot record refuses the window; a reboot boundary is never crossed silently. |
| Anchor is the last same-boot record | success with `records_after_anchor = 0` | The anchor line itself is present, validated, and dropped; no later lines. |
| A reboot occurs after the anchor and the new boot's records are in the capture | unavailable (`boot-mismatch`) | The window is same-boot only; cross-boot ordering is explicitly unreliable (`sd-journal.c:1187-1197`, issue #31516). |
| Duplicate cursor line (same `__CURSOR` twice) | unavailable (`cursor-duplicate`) | Position continuity is ambiguous; the interface requires unique cursors. |
| Two logical copies of one event with different cursors (e.g. two files) | success, counted twice | Cursor uniqueness is string-level, not event identity; r15 already discloses that duplicates are separate records. |
| Malformed JSON, truncated line, overflow, timeout, stderr, non-zero rc | unavailable | Capture integrity is a precondition for every count; no salvage. |
| Empty stdout with rc 0 | unavailable (`empty-capture`) | Documented no-next-entry behavior; absence of the anchor line proves nothing. |

Limits that survive a success: journald rate limiting/loss (`SplitMode=`, storage
policy), unreadable/partial scope files, `--user` requiring persistent logging
(`S014`), unprivileged system-journal visibility, retention beyond the query, and
client-supplied class fields. `--quiet` also suppresses journalctl's
inaccessible-system-journal warning, so an unprivileged partial system capture can
look like a valid window; the claim remains "records observed in this capture", never
"all events in this boot" or "the whole scope was readable".

## Design tensions L1 must resolve before implementation freezes

1. **Exact string vs documented identity.** `sd_journal_test_cursor(3)` says the same
   entry may have multiple cursor strings and that string comparison is not an identity
   test. The interface intentionally demands exact anchor bytes. That is a
   conservative continuity test, not semantic entry identity: a mismatch is refusal,
   never proof that a different event occurred. The claim must say "exact retained
   cursor-string continuity", not "same entry" or "complete window".
2. **End-cursor reporting.** "End cursor optional reported but not written" conflicts
   with "stdout MUST NOT echo raw cursor". Recommendation: omit the end cursor
   entirely; if a field is required, report only a boolean `end_cursor_observed` or a
   SHA-256, never the cursor string. The anchor SHA-256 over validated file bytes is
   explicitly safe.
3. **Defaults.** `--timeout` and `--max-bytes` defaults are not specified. The r13
   census uses a 2 s per-class query bound (`mori-census.sh:318-323`), which is not
   obviously right for a whole-window read. L1 should fix both numbers and document
   them in the tool help so cases are deterministic.
4. **Reason vocabulary.** Freeze the closed set (or an equivalent) before pack authors
   write `want` strings; otherwise packs will pin different words for the same
   refusal. Keep `malformed-json` vs `record-invalid` distinct, as r13/r15 do.
5. **Anchor strictness.** Reject extra keys and duplicate JSON keys as setup errors
   (recommended). This is stricter than the minimum wording but prevents two anchors
   that differ only in ignored bytes from hashing the same behavior differently.
6. **Uniqueness scope.** Include the anchor cursor in the seen set. A later record
   reproducing the anchor cursor is a duplicate position and should refuse the window.
7. **EXIT_STATUS scalar.** Accept string `"9"` and number `9` exactly, matching
   `JOURNAL_JQ_POS_SIGKILL`; reject bool/array/object/null. Confirm with
   `ExistingPredicates` so the tool and packs share one truth table.
8. **Argv visibility.** The cursor is passed on the journalctl command line and is
   visible to same-user `/proc` readers. This is inherent to the read-only interface
   (`--cursor-file` would write); it is not an output leak, but should not be
   described as secret handling.

## Planner checklist (minimal ordered data walk)

1. Freeze output schema, reason vocabulary, defaults, and the EXIT_STATUS rule.
2. Implement M1: one-read anchor parse, exact schema, strict cursor/boot validation,
   SHA-256 of raw bytes.
3. Implement M2/M3: fixed argv, no shell, separate pipes, concurrent drain, deadline,
   byte cap, process-group kill, reap, stderr byte count.
4. Implement M4/M5: strict JSONL, first-record anchor proof, later-record validation,
   four predicates, unique cursor set.
5. Implement M6: deterministic JSON, rc/id mapping, no raw cursor/records/MESSAGE, no
   writes, anchor never advanced.
6. Implement M7 with fake journalctl wrappers; do not execute.
7. Hand the tool to the harness/pack seats. Do not wire it into `mori-census.sh`; do
   not query the live journal from author lanes; do not mutate the anchor.

## [INFERENCE]

- Exact cursor-string equality is sufficient in the common retained case because
  `sd_journal_get_cursor` regenerates the same canonical `s;i;b;m;t;x` serialization
  from the same entry and file; it is not a general identity test, which is why the
  mismatch direction must stay refusal.
- An unprivileged `--system` capture may be silently partial rather than failing; the
  tool's contract already treats the capture as an observed window, not a complete
  scope, so this changes no verdict but must be disclosed in any capability note.
- `--quiet` plus JSON mode makes empty stderr a practical integrity gate for the
  normal path, but stderr must remain a refusal gate because errors are not suppressed.

## [UNKNOWN]

- The exact behavior of the installed 261 build for every edge case versus the 262
  pages; no live journal query was run, so this is not measured. The harness uses
  executable wrappers, so production behavior is whatever the actual CLI does.
- Whether a retained anchor can ever serialize to a different cursor string in this
  host's store; the docs allow multiple strings, so the tool refuses rather than
  assumes.
- Whether a live mixed-boot or duplicate-cursor stream occurs on this host; the
  interface treats both as refusal regardless.
- The final defaults for timeout and max-bytes, and the final reason vocabulary; L1
  owns these decisions.
- Any census/gate tally: L1 owns delivered measurement.

## Disclosure

No live `journalctl` journal query, no probe/measurement loop, no tests, gates, builds,
formatters, or smoke runs were performed by this seat. Only static file reads and web
primary-source reads were used. `journalctl --version` was run once for systemd version
metadata (261.2-1-arch), not a journal read. Read-only shell use was limited to a
directory listing, local grep/sed, a local JSON spec summary, and that version check;
two of those calls were auto-backgrounded by the harness. No `/tmp` output, no
downloads outside the lane, no other-lane writes, no `agent://all`, no tool installs or
upgrades, no `agent.db`/credential access, no omp CLI invocation, and no commit.
