# SeekDocs — approximate seek and retained-anchor test semantics

Seat: `MoriR16.SeekDocs` (scout, leaf). Date: 2026-10-20.
Target: `/home/vgpnk/Projects/shokunin/mori-shokunin`.
Mode: static document/code review only after the L1 no-live-checks clarification. No journal
query, no measurement loop, no background job, no build/test/lint/gate/selftest/formatter, no
`/tmp` output, no outside-lane write, no broadcast, no commit. Only this report was written.

## Disclosure of pre-clarification probe

Before L1's no-live-checks clarification arrived, this seat ran **one** `journalctl --version`
invocation (banner only; it read no journal entries and performed no cursor or window query).
It also ran `pkg-config --modversion libsystemd`, `man -w`, and local `man journalctl` reads.
No `/tmp` files, no background jobs, no tests/builds, no outside-lane writes, no `agent://all`.
The version banner is disclosed as environment metadata only; it is **not** behavioral evidence
and no live result is used to support any claim below. All later tooling was HTTP source reads,
local `man` reads, and read-only file inspection.

## Question

What do the official `sd_journal_seek_cursor(3)` and `sd_journal_test_cursor(3)` documents, plus
the systemd 261 implementation the host ships, actually promise about (a) an approximate
cursor seek and (b) proving that the anchor entry is retained? Scope is only the round-16
new-since-anchor window; no claim about vacuum, deletion, completeness, authenticity or counts.

## Sources opened (2026-10-20, no file saved)

| id | source | version | use |
|---|---|---|---|
| S039 | `sd_journal_seek_cursor(3)` family, https://www.freedesktop.org/software/systemd/man/latest/sd_journal_seek_cursor.html | systemd 262 | documented seek and fallback contract |
| S040 | `sd_journal_get_cursor(3)` / `sd_journal_test_cursor(3)`, https://www.freedesktop.org/software/systemd/man/latest/sd_journal_get_cursor.html | systemd 262 | cursor opacity/aliasing and test result meaning |
| S014 | `journalctl(1)`, https://www.freedesktop.org/software/systemd/man/latest/journalctl.html | systemd 262 | `--cursor`, `--after-cursor`, `--output-fields`, `--no-tail`, `--quiet`, scope |
| S015 | `systemd.journal-fields(7)`, https://www.freedesktop.org/software/systemd/man/latest/systemd.journal-fields.html | systemd 262 | `__CURSOR`, `_BOOT_ID`, address-field rules |
| src261 | `systemd` tag **v261**, `src/libsystemd/sd-journal/sd-journal.c`, `journal-file.c`, `src/journal/journalctl*.c`, `src/shared/logs-show.c` (raw.githubusercontent.com) | systemd 261 (host major/minor per package metadata) | implementation-level semantics |
| src262 | same cursor block in `src/journal/journalctl-show.c` at tag **v262** | systemd 262 | version-stability check of journalctl cursor path |

Host: systemd **261.2-1-arch** (from the disclosed banner); libsystemd pkg-config reports 261.
The v261 journalctl cursor block is byte-identical in the compared region to v262, so the
documented 262 behavior and the inspected 261 source agree for this path. The host package was
not live-queried, so this is source-version equivalence, not measured host behavior.

## Observed facts

### 1. What a canonical cursor contains

`sd_journal_get_cursor()` serializes the current entry with exactly one fixed format
(`sd-journal.c`, `sd_journal_get_cursor()`; the seek parser at `sd-journal.c:1263-1363`):

```
s=<file-header seqnum_id>;i=<entry seqnum>;b=<entry boot_id>;m=<entry monotonic>;t=<entry realtime>;x=<entry xor_hash>
```

Every value is hex text; the result is printable and opaque. `sd_journal_seek_cursor()` parses
six optional tags (`s,i,b,m,t,x`), silently ignores unknown tags, and requires at least one
usable key: `(s and i) or (m and b) or t`, else `-EINVAL` (`sd-journal.c:1331-1334`). So the
seek API accepts **partial** cursors, not only the canonical six-tag form. The round-16 contract's
anchor is therefore shape-validated only; it is not known to be canonical, and the tool must not
parse it.

`sd_journal_test_cursor()` is component-conjunctive subset matching, not string equality
(`sd-journal.c:1366-1448`): each recognized tag present in the cursor is compared against the
current entry, and the function returns **1** if all present components match, **0** on the first
mismatch, negative errno on parse/positioning failure. `s=` is compared to the **current file
header's** `seqnum_id`, not to an entry field (`sd-journal.c:1379-1384`). A cursor with only
`t=` can match many entries at that realtime. Unknown-only cursors return 1 if positioned, but
`seek_cursor()` rejects them first, so journalctl cannot reach that state. Unpositioned context is
`-EADDRNOTAVAIL`.

### 2. Seek is deferred; positioning is approximate and key-ordered

`sd_journal_seek_cursor()` only parses the string into `j->current_location` with type
`LOCATION_SEEK`; it does not select an entry (`sd-journal.c:1336-1363`; S039: "these calls do not
actually make any entry the new current entry"). The first `sd_journal_next()` (journalctl uses
`sd_journal_step_one(j, !arg_reverse)`, forward here) resolves the location.

Resolution order per journal file (`find_location_with_matches()`, `sd-journal.c:924-971`):

1. `LOCATION_HEAD`/`LOCATION_TAIL` conventional handling;
2. if `seqnum_set` **and** the file header's `seqnum_id` equals the cursor's `s=`, bisect entries
   by seqnum (`journal_file_move_to_entry_by_seqnum()`, `journal-file.c:3381-3397`) — exact match
   when present, otherwise the nearest entry in iteration direction;
3. else if `monotonic_set` (`m=` and `b=`), bisect by monotonic inside entries carrying that
   boot's `_BOOT_ID` data object (`journal-file.c:3475-3495`); a match here wins;
4. else if `realtime_set` (`t=`), bisect by realtime (`journal-file.c:3421-3437`);
5. only for a monotonic-only cursor with no realtime component, fall back to the boot range.

For a canonical cursor all of `s,i,b,m,t,x` are present, so the practical chain is
**seqnum (same seqnum_id) → monotonic (same boot) → realtime**, and the result for forward
iteration is the first entry **at or after** the anchor under the chosen key. It never selects an
earlier entry: seqnum/realtime bisection returns `>= needle` for `DIRECTION_DOWN`, and the
monotonic fallback also moves forward. This is the precise meaning of S039's "next closest entry
(in terms of time)".

Across multiple journal files, `real_journal_next()` (`sd-journal.c:1129-1177`) asks every file
for its candidate and keeps the earliest by `compare_locations()` (`sd-journal.c:1083-1127`):
seqnum first when the `seqnum_id` matches, then boot identity/monotonic, then realtime, then xor
hash. So the first emitted record is the earliest surviving position at or after the seek key in
the union of queried files. "After" here is **journal iteration order**, not wall-clock order; a
clock step can produce a later record with a smaller realtime but a larger seqnum.

### 3. `journalctl --cursor=` has no retained-anchor test of its own

`seek_journal()` (`journalctl-show.c:50-103`) for `--cursor=`:

```
r = sd_journal_seek_cursor(j, cursor);     // parse only
r = sd_journal_step_one(j, true);          // forward; first entry at/after
// --cursor: no test, output starts here
if (after_cursor && r > 0) {               // --after-cursor only
        k = sd_journal_test_cursor(j, cursor);
        if (k > 0) r = sd_journal_step_one(j, true);   // skip only on positive match
}
if (r == 0 && !arg_follow) arg_lines = 0; // nothing at/after: zero output, success
```

Consequences, all [OBSERVED] in source:

- `--cursor=` is **inclusive**: if the anchor is retained, the anchor record is the first output
  line. If it is missing, the first line is the nearest later entry (or nothing). journalctl does
  **not** call `test_cursor` and does **not** warn or change exit status on a nearest seek.
- `--after-cursor=` is **unusable as proof**: journalctl skips the first line only when
  `test_cursor` returns positive; a missing anchor silently starts at the nearest following entry,
  and a retained anchor with no successor yields an empty stream. Source and docs agree.
- `sd_journal_test_cursor()` is not exposed as a CLI flag; the only in-band CLI proof available
  to the tool is comparing the first emitted `__CURSOR`/`_BOOT_ID` to the anchor.

### 4. Empty stdout with rc 0 is a normal outcome, not an error

Two source paths produce rc 0 with no records:
`sd_journal_step_one()` returns 0 after the seek, setting `arg_lines = 0`
(`journalctl-show.c:100-102`), and `action_show()` returns 0 early when
`journal_boot_has_effect()` is false (`journalctl-show.c:531-536`). In both cases `show()` never
prints a record, `--output=json` already forces `arg_quiet = true` (`journalctl.c:627-629`), and
`--quiet` suppresses even the `-- No entries --` hint (`journalctl-show.c:604-606`). Therefore:

- empty capture cannot prove the seek landed on anything, least of all the anchor;
- a genuine **zero-new-record** window is different: `--cursor=` inclusivity still emits the
  anchor line, which the tool validates and drops. Success with `records_after_anchor = 0` is
  possible only when the anchor line is present and validated.
- empty stdout must be `MORI_JOURNAL_WINDOW_UNAVAILABLE`, never zero counts.

This is the strongest source-level justification for the contract's empty-capture refusal.

### 5. First-record canonical-cursor equality is a sound retention proof (and a non-necessary one)

`__CURSOR` in JSON is generated by `sd_journal_get_cursor()`, hence it is always the **full
canonical** six-tag string (`logs-show.c:1254-1278`; the two timestamp, boot, seqnum and seqnum-id
address fields are added unconditionally around it). This yields a one-directional proof:

- **Equality ⇒ retained.** If the first record's `__CURSOR` bytes equal the anchor string, then
  the anchor string has exactly the canonical tag values `s,i,b,m,t,x` of that record. Each tag
  is present, so `sd_journal_test_cursor()` would compare all six and return 1; and `s=` equals
  the emitting file's header `seqnum_id` while `i=` is that file's entry seqnum. Sequence numbers
  are unique among files sharing a `seqnum_id` (rotation inherits `seqnum_id` from the template,
  `journal-file.c:440-444`; append enforces one sequence per file, `journal-file.c:2367-2378`),
  so equal full cursors denote the same recorded entry. [OBSERVED from source; INFERENCE for the
  uniqueness step, which relies on journal-file ordering rather than a cryptographic guarantee.]
- **Inequality ⇏ not retained.** S040 explicitly says the same entry may be referred to by
  multiple cursor strings and that string comparison is not an identity test. A byte mismatch is
  therefore refusal evidence only. It must never be reported as vacuum, rotation, deletion or a
  different event. The refusal reason must be positional (`anchor-not-retained` or equivalent).

Because the tool never parses the anchor, this proof does not assume the anchor was canonical: a
partial or forged anchor string cannot equal a canonical emitted string unless it is byte-identical
to that entry's canonical form, in which case it identifies that entry. A forged anchor that is
byte-identical to a canonical cursor is not an authenticity claim: it proves only which entry the
seek resolved to, never who emitted it or that the record set is complete.

`_BOOT_ID` is unconditional in JSON (`logs-show.c:1268-1272`) and, like the cursor's `b=`, comes
from the entry's boot id, so requiring first-record `_BOOT_ID == anchor.boot_id` as well as cursor
equality rejects a cursor/boot pair whose components disagree without parsing the cursor.

### 6. Alias and gap modes that a strict reader must tolerate as refusals/limits

- **Rotation/duplication.** journald rotation creates files from a template and inherits
  `seqnum_id`; for keyed-hash files systemd deliberately computes the xor hash unkeyed so that
  "cursors for old and new journal files are completely identical" (`journal-file.c:2612-2628`).
  Identical duplicate records are suppressed by `next_beyond_location()`'s discrete-location loop
  (`sd-journal.c:1056-1078`), so normal rotation does not normally create alias cursors or
  duplicate window records.
- **Merged/foreign files.** A record present in another journal generation with a different
  `seqnum_id` (or read via `--merge`/`--directory`) would carry a different `s=` and often a
  different `i=`, so the same entry can present a different cursor string. The round-16 query
  does not use merge/directory, but this remains a source of safe false-unavailability.
- **Rewrite.** A volatile→persistent rewrite gets a new sequence number (S039/S040 family,
  `sd_journal_get_seqnum(3)`), so the old cursor cannot be reproduced; that is refusal, not
  deletion proof.
- **Silent corrupt-entry skip.** JSON serialization converts `-EBADMSG`/`-EADDRNOTAVAIL` from
  cursor/timestamp generation into `corrupted_skip`, which logs at **debug** level and drops the
  record (`logs-show.c:1218-1226,1322-1327`). With default log level this is invisible: no stderr,
  no rc change. A capture can therefore contain validated records with an unobservable gap. The
  window claim is `validated-record-subsets`, never completeness. Cursor continuity between
  emitted records still holds; missing records are simply unobservable.
- **Scope.** `--system` and `--user` select disjoint journals; omitting both shows "all messages
  that the user can see" (S014). The contract's one-scope query therefore requires an explicit
  scope flag. `--user` additionally requires persistent logging (S014).
- **Boot scoping.** `-b`/`_BOOT_ID=` is a **match filter** (S014), so it would hide a boot
  boundary instead of exposing it. The contract's no-`-b` query plus a per-record `_BOOT_ID` check
  is the only form that can refuse a foreign-boot record. A captured window that crosses a reboot
  is refused, not narrowed.

### 7. JSON field shape constraints for the parser

- `--output-fields=` cannot reduce the address fields away: `__CURSOR`,
  `__REALTIME_TIMESTAMP`, `__MONOTONIC_TIMESTAMP`, `_BOOT_ID` are always printed in JSON modes
  (S014). The v261 source additionally emits `__SEQNUM` and `__SEQNUM_ID` before the field filter
  (`logs-show.c:1254-1280`), so a fixed exact key set of five requested names is wrong. The tool
  must tolerate these extras while still never echoing them.
- Journal fields may be non-unique; JSON emits an **array** when a name repeats
  (`logs-show.c:1305-1318`), and oversized values become `null` (S014). A `__CURSOR`/`_BOOT_ID`
  value that is not a scalar string is invalid; a repeated `MESSAGE_ID`/`UNIT_RESULT`/`EXIT_*`
  value is not a scalar predicate value.
- JSON output sets `arg_quiet` internally (`journalctl.c:627-629`), so `--quiet` is redundant
  for the stream but still suppresses inaccessible-journal warnings; it does not suppress fatal
  errors, which remain stderr + nonzero rc.
- No write side effects: `update_cursor()` writes or prints only for `--cursor-file`/
  `--show-cursor` (`journalctl-show.c:496-520`), neither of which the contract uses. The query is
  read-only and the anchor is never advanced.

## Direct answers

**Approximate seek semantics.** `sd_journal_seek_cursor()` is parse-only. Positioning happens on
the next forward step and chooses the nearest entry at or after the cursor by seqnum when the
`seqnum_id` matches, else by boot+monotonic, else by realtime, taking the earliest candidate across
files. A missing anchor is not an error: it silently yields the nearest later entry. Forward
selection never goes backwards.

**Retained-anchor test semantics.** The API's test is `sd_journal_test_cursor()`, a per-component
conjunctive match returning 1/0/negative; it is not string equality and treats `s=` file-relative.
The CLI never runs it for `--cursor=`. The contract's substitute — first record's canonical
`__CURSOR` bytes equal to the anchor plus matching `_BOOT_ID` — is **sufficient but not necessary**:
equality implies all six canonical components match (so the API test would pass) and the same
seqnum in the same sequence, while inequality may be an alias and is refusal-only. Empty output
proves nothing and must be unavailable; zero-new-record success requires the validated anchor line.

## Advisory implications for the tool (not implementation)

1. Use `--cursor=<anchor>` inclusive, never `--after-cursor`, `--cursor-file` or `--show-cursor`.
2. Always pass exactly one of `--system`/`--user`; do not add `-b`, `_BOOT_ID=` match, `--merge`,
   `--directory`, `--follow`, `--all`, `--grep` or `--reverse`.
3. Require the first parsed object's `__CURSOR` (scalar string) to equal the anchor cursor
   **byte for byte** and `_BOOT_ID` to equal `anchor.boot_id`; drop it only after both pass.
4. Treat empty capture, nearest-seek mismatch, non-object line, non-scalar/missing cursor or boot,
   foreign boot on any later record, duplicate cursor, any stderr, nonzero rc, timeout or byte
   overflow as `rc2` unavailable with a stable positional reason.
5. Success with `records_after_anchor = 0` is valid only when the anchor line was present and
   validated. Never equate zero with "no event occurred".
6. Never parse the cursor, never name a cause for a mismatch (vacuum/rotation/deletion), and never
   use cursor string equality as event-identity dedup outside the contract's uniqueness guard.
7. Do not report the end cursor raw; omit it or report a SHA-256. The anchor SHA-256 is the only
   anchor-derived value safe to echo.

## Risks / contradictions for L1

- `journalctl` has no retained-anchor test; the proof is entirely a client-side first-record
  convention. That is exactly what the interface specifies, but the claim must stay
  "exact retained cursor-string continuity", not "the entry was not vacuumed".
- The contract says an unavailable result carries "a reason stable"; a byte mismatch has many
  possible causes and none is observable. Freeze a positional reason and forbid causal wording.
- "End cursor optional reported but not written" conflicts with "stdout MUST NOT echo raw
  cursor". Recommend omitting the end cursor or hashing it.
- `--quiet` + rc0 can hide an unreadable scope (S014 warns it suppresses inaccessible-system-
  journal warnings). Empty stdout is the only signal; it is already refusal.
- The round-16 claim is about journal **iteration order after the anchor**, not wall-clock time.
  Clock steps can make a later record carry an earlier realtime; do not describe the window as
  time-ordered.
- A corrupt record can be skipped at debug level with rc 0. Do not upgrade a validated subset into
  a completeness claim.

## Remaining unknowns

- Frequency and practical impact of cursor aliasing on this host (same entry, different canonical
  string). No live query was permitted; S040 establishes possibility only.
- How often the host journal can contain the same record under two `seqnum_id`s (merged/foreign
  files). The normal rotation path inherits `seqnum_id`, but the query's exposure is unmeasured.
- Whether any host journald configuration causes silent gaps (rate limiting, partial writes) in
  addition to the debug-level corrupted-entry skip. Retention/vacuum configuration documents were
  not opened this round.
- Host behavior was not measured. The v261 source region matches v262 for the journalctl cursor
  path and the v261 sd-journal functions were read directly, but this is source equivalence, not
  an executed host check; the disclosed version banner is not behavioral evidence.

## Corrections, registry, drift, tooling

- **Append-only correction carried:** r13's `--after-cursor=`-centred wording cannot prove anchor
  presence; round 16 uses inclusive `--cursor=` plus first-record equality. The historical r13 text
  is not rewritten here; `CursorDocs.md` already records the same correction from S014.
- **Registry:** S014 and S015 were opened this round by this seat as required; no registry file was
  written (Registry owns it). No new source row is needed from this lane; S039/S040 already exist
  in the working tree.
- **Old drift pin:** untouched, not re-pinned, remains red. No status change claimed.
- **Tooling:** no install or update. `curl` (web source reads), `man`/`col`/`sed -n` (local doc
  reads) and read-only file inspection only; no package transaction, no omp CLI, no credentials
  or agent DB access.
- **Round-15 procedural feedback:** the only deviation is the disclosed single pre-clarification
  `journalctl --version` (no journal read); it is not used as verification. After the
  clarification, no live probe, test, gate or formatter was run.

Bottom line: `seek_cursor` is a deferred, key-fallback **nearest** seek; `test_cursor` is a
component-subset match, not string equality, and journalctl never calls it for `--cursor=`. The
first emitted record's canonical `__CURSOR` plus `_BOOT_ID` equality is a sound sufficient proof of
retained-cursor continuity, but not a necessary one, and an empty stream must be unavailable rather
than a zero-event window.
