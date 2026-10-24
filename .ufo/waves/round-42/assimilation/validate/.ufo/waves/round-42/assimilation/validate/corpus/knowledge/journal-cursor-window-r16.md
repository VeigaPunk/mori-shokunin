source: S014 — https://www.freedesktop.org/software/systemd/man/latest/journalctl.html — systemd 262 man page: `-c, --cursor=` “Start showing entries from the location in the journal specified by the passed cursor.”; `--after-cursor=` “Start showing entries from the location in the journal after the location specified by the passed cursor.”; `--show-cursor` “The format of the cursor is private and subject to change.”; `-q, --quiet` “any warning messages regarding inaccessible system journals when run as a normal user.”; `--output-fields=` “the "__CURSOR", "__REALTIME_TIMESTAMP", "__MONOTONIC_TIMESTAMP", and "_BOOT_ID" fields are always printed.”. S015 — https://www.freedesktop.org/software/systemd/man/latest/systemd.journal-fields.html — systemd 262 man page: `__CURSOR=` “A cursor is an opaque text string that uniquely describes the position of an entry in the journal”; `_BOOT_ID=` “The kernel boot ID for the boot the message was generated in”. S039 — https://www.freedesktop.org/software/systemd/man/latest/sd_journal_seek_cursor.html — sd_journal_seek_cursor(3), systemd 262: “If no entry matching the specified cursor is found the call will seek to the next closest entry (in terms of time) instead.” S040 — https://www.freedesktop.org/software/systemd/man/latest/sd_journal_test_cursor.html — sd_journal_test_cursor(3) (page served as sd_journal_get_cursor), systemd 262: “cursor strings do not uniquely identify an entry: the same entry might be referred to by multiple different cursor strings”; “The cursor identifies a journal entry globally and in a stable way”.
verified-at: 2026-10-20 — the four public systemd 262 pages above were opened for this note by static reads. No journal was queried, no host journalctl query was run, and no fixture, wrapper, test or gate was run. Host systemd version was not verified; no behaviour is claimed for any host version.
recheck: `curl -fsSL https://www.freedesktop.org/software/systemd/man/latest/sd_journal_test_cursor.html | grep -oF 'The cursor identifies a journal entry globally and in a stable way'`; `curl -fsSL https://www.freedesktop.org/software/systemd/man/latest/sd_journal_seek_cursor.html | grep -oF 'seek to the next closest entry'`; `curl -fsSL https://www.freedesktop.org/software/systemd/man/latest/journalctl.html | grep -oF 'Start showing entries from the location in the journal specified by the passed cursor.'`.

# New-since-anchor journal window — exact-anchor proof, approximate seeks, boot and access limits — round 16

## Claim

A window is available only when one captured `journalctl` stream from one scope proves its own starting point. The proof is byte-level: the first parsed record must carry exactly the anchor's cursor string and exactly the anchor's `_BOOT_ID`. Only records after that first record are counted, and only when every one of them is a scalar-cursor object from the same boot. Nothing else is claimed. The byte-equal test is a conservative acceptance test. It is not a dedup key, not a completeness statement, and not proof that the stream is the anchor's full scope.

This note supports FR11 only as an exact-retained, same-boot, read-only window. It does not authenticate emitters, count unique victims, or prove that the journal lost nothing between the anchor and the end of the window.

## Evidence

### 1. What the first record can show

S014 defines `--cursor=` as the starting location: “Start showing entries from the location in the journal specified by the passed cursor.” S039 gives the API behaviour for an absent cursor: “If no entry matching the specified cursor is found the call will seek to the next closest entry (in terms of time) instead.”

The `journalctl` CLI's behaviour for an absent cursor is not documented in S014. The API fallback in S039 does not establish a CLI success case: the CLI may begin at a neighbouring entry, or it may exit nonzero. The wrapper must handle both. Its acceptance rule is the same either way: the first record's `__CURSOR` must equal the anchor string exactly, and its `_BOOT_ID` must equal the anchor boot. Any other first record, any nonzero exit, and any empty capture are refused.

`--after-cursor=` is not used. S014 defines it as starting “after the location specified by the passed cursor”, so the anchor record is skipped without any check that it is present. Using it would make a missing anchor indistinguishable from a successful window.

### 2. What byte equality does and does not establish

S040 says the cursor “identifies a journal entry globally and in a stable way”. Its first sentence on identity is “cursor strings do not uniquely identify an entry: the same entry might be referred to by multiple different cursor strings”. The page gives aliasing as the reason. It does not state whether a string can also match more than one entry. This note makes no claim either way, and it treats the page's wording as the limit: a byte-equal first record is a conservative acceptance test, not proof of identity.

Consequences for the wrapper:

- **Alias false refusal.** If the journal presents the anchor entry under a different byte string than the one stored in the anchor file, the byte test refuses the window even though the anchor exists. That is a conservative loss of coverage, not a wrong count.
- **Mismatch is not a diagnosis.** A first record that is not the anchor does not show why. It may mean the anchor is absent, aliased, or not the start the CLI chose. The wrapper must not name a cause it did not observe.
- **No dedup.** Byte equality of cursors is never used to deduplicate records, to count distinct entries, or to equate a window record with an event elsewhere.
- **The API test is not used.** S040 describes a test call after a seek. That is a libsystemd call, not a `journalctl` flag documented in S014. The CLI wrapper cannot make it. Adding a libsystemd binding is out of scope for this round.

### 3. Same-boot boundary

S015 defines `_BOOT_ID=` as “The kernel boot ID for the boot the message was generated in”, and it is a trusted field: fields prefixed with an underscore “cannot be altered by client code”. Of the requested output fields, only `_BOOT_ID` is trusted.

The contract's query adds no `_BOOT_ID=` match and no `-b` option, so the captured stream may span boots. The wrapper checks every record:

- the first record must have the anchor's `_BOOT_ID`;
- every later record must have that same `_BOOT_ID` as a scalar.

A later record from another boot in the captured stream refuses the current window: that run is unavailable, and the wrapper does not drop the foreign-boot records and keep the rest. Dropping them would present a same-boot segment as if it were the whole window.

What this does and does not say:

- It refuses the current window only. It makes no claim about whether the foreign-boot record persists in the journal or is absent at a later query. No permanent-retention claim is made.
- The anchor is not advanced automatically. Any advance is an explicit later step outside this round.

### 4. Subsets, not totals

The contract's query requests an explicit field list. S014 says `--output-fields=` restricts the output for the JSON modes, and that `__CURSOR`, `__REALTIME_TIMESTAMP`, `__MONOTONIC_TIMESTAMP` and `_BOOT_ID` are always printed. `MESSAGE` is not in the requested list, so the captured stream contains no `MESSAGE` field. This note makes no claim about what `journalctl` reads internally; the claim is limited to the captured stream the wrapper parses.

Three subset properties follow:

- `records_after_anchor` counts every record in the captured stream after the anchor, in this scope. It is not a class count. It counts returned records, so it is a lower bound on what was in the stream. A zero means no record after the anchor was in this capture, not that nothing happened.
- The four `positive_*` tokens count only object records that pass the r15 identity and class predicates (`corpus/knowledge/journal-positive-evidence-r15.md`). They are validated witnesses, not totals, and never victim counts. These window tokens are after-anchor and whole-window-refusing: a foreign-boot or malformed record refuses the entire capture, so no positive is kept beside an invalid sibling. The census `positive_*` tokens are a separate identity, which keeps positives beside invalid siblings (r15 §3). The two are not comparable, and neither is an alarm source.
- A capture that exceeds `--max-bytes` is not truncated and kept. Overflow is unavailable: a stream is either complete within the byte bound or refused.

### 5. Access limits

- **Scope.** S014 says the system journal is readable by root and certain groups, and `--user` shows the current user's journal. The contract's scope flag must be explicit so the window reads one scope. Without a flag, S014 says `journalctl` shows “all messages that the user can see”, which mixes scopes.
- **Quiet partial access.** S014 `-q` suppresses “any warning messages regarding inaccessible system journals when run as a normal user.” A normal user can therefore get a quiet stream that contains the anchor and only the accessible subset of later records. The anchor's presence does not prove the user can read the whole scope. Stderr silence is not an access proof, and a partial stream is not a complete window.
- **Empty capture.** Empty stdout is unavailable under the contract. An anchor-only stream (one record, the anchor) is a valid capture with zero later records; it is not the same as empty stdout.

Retention, vacuum, rotation and rate-limiting are not opened in this note. Records removed before the query are absent from `records_after_anchor` and from every positive token. This note makes no claim about how often that happens.

## [INFERENCE]

- A byte-equal first record is the case in which the anchor is present and not aliased, because the anchor file was built from the same `__CURSOR` string. This is inferred from the design, not measured.
- The conservative direction is the right one for an FR11 probe. A false refusal is a coverage loss, reported only by the probe's rc2. A false available would be a fabricated window. The string-equality rule only risks the first.
- Refusing the whole window on a captured foreign-boot record, rather than dropping it, is the only design that keeps a same-boot segment from standing in for the window.
- The four `positive_*` tokens are only as complete as the window they sit in. They inherit every subset limit above.

## [UNKNOWN]

- How `journalctl --cursor=` behaves on an absent cursor (neighbour, nonzero exit, or otherwise), on any version. S014 does not document it and this note does not measure it.
- How often a journal presents a cursor under a different string than one recorded earlier. Not measured; no journal was read.
- Whether a foreign-boot record captured in one query is still retained at a later query. Not claimed.
- The journald retention and rate-limit behaviour that determines which records exist to be returned. Not opened this round.
- The end cursor from `--show-cursor`: S014 calls its format private, so the wrapper must not parse it and must not echo it.
- Any live window size, `records_after_anchor` value or positive count. No prediction is made.

## Not claimed

- No authenticated emitter. `MESSAGE_ID`, `UNIT_RESULT`, `EXIT_CODE` and `EXIT_STATUS` are client-supplied fields (S015, User Journal Fields). Only `_BOOT_ID` is trusted.
- No unique victim, no kill cause, no fleet membership. The window observes returned records; it does not join them to processes or units.
- No completeness. A window does not prove the journal kept every record after the anchor, nor that no event occurred, nor that the user can read the whole scope.
- No cursor-state mutation. `--cursor-file=` (S014, which writes the cursor of the last entry) is not used. The wrapper writes nothing; any anchor advance is a later explicit step.
- No dedup by cursor. Byte equality is an acceptance test for the first record only.
- No permanent-retention claim about foreign-boot records, anchors or entries.
- No claim that a cursor string belongs to one entry only, or that any string is shared between entries.

## What it changes for mori

- FR11 advances for one narrow case: an exact-retained, same-boot window read by an explicit read-only probe, with the first record's cursor and boot matching the anchor. A first record that is not the anchor, a captured foreign-boot record, a failed or truncated capture, or any malformed record leaves FR11 unavailable.
- The wrapper does not name a cause for a first-record mismatch. The reason vocabulary belongs to the wrapper contract, not to this note.
- The scope flag is always explicit. The output contains only the requested fields; `MESSAGE` is not requested.
- The end cursor, if reported, is reported only as a safe SHA-256 digest. The raw string is never printed.
- No census cutover, no gate change, and no change to the r15 alarm contract.

## Delivery paths this cannot see

- An anchor present under an alias string: refused, although the anchor existed.
- A captured stream containing the anchor and later records from several boots: the whole window is refused; the same-boot part is not reported.
- A quiet partial read: the anchor and an accessible subset are returned, and the window is available for that subset only. Records the user cannot read are absent.
- Records removed before the query: absent from `records_after_anchor` and from every positive token.

## Source-registry state (for L1 and the Registry seat; not written by this seat)

When this seat last checked `corpus/SOURCES.md` by static read, it held rows **S039** (`sd_journal_seek_cursor(3)`, line 45) and **S040** (`sd_journal_test_cursor(3)`, line 46), both `docs`, `A`, `mined`, opened 2026-10-20. L1 reported only a combined S039 and no S040. That disagreement is for L1 and the Registry seat to reconcile; this note cites S039 for the seek fallback and S040 for the identity sentences. If the final registry has only a combined S039 row, the S040 citations map to that row's test-page sentences.

Mutable used-by cells this note needs (append-only; immutable cells unchanged):

- **S014** used-by gains `corpus/knowledge/journal-cursor-window-r16.md`.
- **S015** used-by gains `corpus/knowledge/journal-cursor-window-r16.md`.
- **S039** and **S040** used-by gain `corpus/knowledge/journal-cursor-window-r16.md`.

## L1 source-registry correction and measured scope

The draft reconciliation paragraph under **Source-registry state** is
superseded: final `corpus/SOURCES.md` has separate **S039 seek** and
**S040 test** rows, both mined and both used by this note. S014 and S015 also
list this note. There is no unresolved combined-row mapping. Exact changes
are retained in `.ufo/waves/round-16/evidence/sources-measurement.json`.

L1 subsequently measured the committed implementation at
`87a57c13dbb1fc2d3e049bba98aca1739822b8c9`: the finite gate matched64/64
(`evidence/capability-after/run-manifest.json` under round-16 waves; count
command `jq '.summary'`), and one live observation per scope returned
`MORI_JOURNAL_WINDOW_OK`, `records_after_anchor=0`, with all four positive
subsets0 (`evidence/live-window-{user,system}.json`). These are anchor-only
captures, not positive live load or evidence of no event. The author's
unmeasured-source discussion above is not a current claim that the host
path has never run. No alias/vacuum/cross-boot live experiment was performed
by L1; those boundaries remain finite-fixture and source-supported only.

## Round-17 appended freshness correction (2026-10-20)

The original `verified-at` statement that the host systemd version was not
verified is superseded for the **round-16 observation time**: the round-16 lesson
records host **261.2-1**, as confirmed by
`corpus/lessons/round-16-verifier-spotcheck.md:220–223`. It is not today's
current-version claim. Today's package log records systemd **261.2-1→262-1**
inside the 09:16 full-upgrade transaction (round-17 evidence
`.ufo/waves/round-17/build/{PacmanTxnToday,ProvinceNotesDraft}.md`).
No new journal query or re-pin is implied. The closure admitted the bounded
capability (`round-16-verifier-spotcheck.md:9–17`); alias false-unavailable,
vacuum/cross-boot unknowns and anchor-only live qualifications remain unchanged.

Primary version lookup pointers for that historical correction are
`corpus/lessons/round-16.md:69,73,153`; the non-author closure is the routing
authority, not the original version measurement. No current daemon-version
claim is inferred from the package upgrade.
