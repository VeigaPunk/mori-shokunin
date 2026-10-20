# ReviewAnchor — round16 C1 window: first-record anchor equality, missing/vacuum behavior

Reviewer: MoriR16.ReviewAnchor (leaf, read-only, no execution)
Target: /home/vgpnk/Projects/shokunin/mori-shokunin
Git HEAD at read time: b83edc6ee3db6822382ab673d7e6e984e420f22f
Porcelain at read time: `?? .ufo/waves/round-16/` only.

## Read-time state (explicit)

- **`tools/mori-journal-window.py` did NOT exist at read time.** Neither did
  `.ufo/waves/round-16/fixtures/` nor any journal-window code in the repo (glob and
  content search over the tree found only spec/registry text under
  `.ufo/waves/round-16/` and the r15 knowledge note).
- Therefore this review is **contract-level**, not code-level. Every finding below is
  a spec/design finding to be re-checked against the implementation once WindowTool
  lands. Nothing here is a claim about shipped code.
- Spec read: `.ufo/waves/round-16/wave1-spec.json` (shared context + WindowTool/WindowHarness
  prompts, read in full).

## Sources opened this lane

- Local `man journalctl` (systemd 261.2-1-arch, `journalctl --version`): `--cursor=`
  ("Start showing entries from the location in the journal specified by the passed cursor"),
  `--after-cursor=`, `-b`/`--boot`, `--output-fields=` (`__CURSOR`, `_BOOT_ID` always printed
  in json), `--user`/`--system` (no flag: "show all messages that the user can see"),
  `--vacuum-*`. The local page does **not** state what `--cursor` does when the cursor entry
  is absent.
- Official `sd_journal_seek_cursor` (freedesktop, systemd 262 docs): "If no entry matching
  the specified cursor is found the call will seek to the next closest entry (in terms of
  time) instead."
- Official `sd_journal_test_cursor` (freedesktop): "cursor strings do not uniquely identify
  an entry: the same entry might be referred to by multiple different cursor strings, and
  hence string comparing cursors is not possible." Test-after-seek is the library's own
  verification step.
- NOT opened by this lane: S014/S015 source files (owned by CursorDocs/FieldDocs/Registry
  peers). Not verified here.

Tools installed/updated by this lane: none.

## Findings (by severity)

### F1 — High (contract is sound on its face; code must implement it exactly)
**Exact first-record anchor equality is the only in-tool detector of a missing or vacuumed anchor.**
Per the seek docs, a cursor with no matching entry resolves to the next closest entry. So
`journalctl --cursor=<anchor>` on a vacuumed anchor does NOT fail; it emits the successor.
The spec's rule (first parsed record must have `__CURSOR` equal to the anchor cursor AND
`_BOOT_ID` equal to the anchor boot_id; otherwise rc2 UNAVAILABLE) is the right refusal.
Implementation requirements the code must meet (not yet verifiable):
- Compare the JSON-decoded `__CURSOR` string byte-for-byte with the anchor `cursor`. No trim,
  casefold, Unicode normalization, or prefix match.
- A `__CURSOR` that is missing, null, array, object, or non-string → UNAVAILABLE (not equality
  false-negative that silently continues).
- The first parsed element must be a JSON object. A malformed first line → UNAVAILABLE; do not
  skip it and treat the next line as "first".
- Only after both cursor and boot match is the first record dropped. A cursor match with boot
  mismatch → UNAVAILABLE (reason distinct or at least stable), never "anchor found".

### F2 — Medium (limitation to state, not a defect)
**String equality is conservative, not proof of entry identity.** `sd_journal_test_cursor`
explicitly says the same entry may carry multiple cursor strings and string comparison of
cursors is "not possible". Consequence for this design:
- Mismatch → refuse is fail-closed and correct.
- Match → accept is justified only under the assumption that journalctl emits the cursor it
  was given for that entry (the normal `--cursor` path). The window is therefore "anchor
  string observed as first record", not "entry identity proven".
- The shared context and the Knowledge/Province prose must say "exact-cursor-string
  observation, conservative refusal on any mismatch" rather than "exact-anchor proof" without
  qualification. Otherwise the claim overreaches the API docs.

### F3 — High (scope contamination; spec gap)
**Scope flag mapping is unspecified.** The Interface says "Query one scope with --cursor=..."
but the argv list contains no `--user` or `--system`. Per the local man page, with neither flag
journalctl shows every journal the caller can see. A `--scope user` window run without `--user`
can therefore mix system records (and a merged-journal anchor can match), and the four
positive counts would then be computed over the wrong population.
- Required: `--scope user` → argv includes `--user`; `--scope system` → `--system`. The
  harness wrappers must record argv so the selftest can assert the flag.
- Note from man: `--user` only works with persistent logging; absence should surface as
  UNAVAILABLE, not an empty clean window.

### F4 — Medium (ambiguity that will produce wrong refusal reasons)
**"Missing anchor" is used for two different conditions.**
- (a) Anchor file missing/unreadable/schema-invalid/bad boot_id/bad cursor charset → the spec
  says setup invalid anchor → `MORI_JOURNAL_WINDOW_SETUP` rc2.
- (b) Anchor cursor retained-or-not in the journal (vacuumed, rotated away, never existed)
  → "missing/vacuumed anchor ... stay unavailable" → `MORI_JOURNAL_WINDOW_UNAVAILABLE` rc2.
The spec text uses "missing" for both. Required: the implementation and the packs must
distinguish (a) SETUP from (b) UNAVAILABLE, and the selftest must have one case of each.
Currently no pack is specified to pin (a) versus (b) explicitly.

### F5 — Medium (zero-record semantics must be pinned)
- Empty stdout with rc0 → UNAVAILABLE (no anchor record observed). It must NOT become
  `records_after_anchor: 0` success. The spec's "malformed/empty capture → unavailable" covers
  this; it must be an explicit test (PackMissingAnchor).
- The only legitimate zero is: first record equals the anchor, nothing follows → rc0,
  `records_after_anchor: 0`. Tests must distinguish these two zeros. Also the success output
  must not be read as "no events occurred" (no completeness claim).

### F6 — Medium (duplicate-anchor gap)
The spec requires every later record to have a unique valid cursor, but does not say whether the
anchor cursor itself is in the seen-set. A later record repeating the anchor cursor would pass
the uniqueness check as written. Required: seed the seen-set with the anchor cursor, so any later
repeat → UNAVAILABLE (duplicate). Add a pack case for it.

### F7 — Low (boot wording)
"Same-boot" is enforced against the anchor boot_id, not against the current boot. If the anchor
is from a prior boot and no later-boot records are returned, the window is a valid same-anchor-boot
window. Wording in Knowledge/Province/Quality should say "anchor boot" not "current boot". A
reboot after the anchor is caught only when journalctl returns records from the new boot
(foreign `_BOOT_ID` → UNAVAILABLE); absence of such records is not evidence of no reboot. Do not
claim cross-boot ordering or completeness.

### F8 — Low (hardening, undefined terms in spec)
- "printable scalar" for cursor is undefined. Journal cursors are ASCII (`s=`, `i=`, `b=`, `m=`,
  `t=`, `x=`). Recommend pinning the anchor cursor to printable ASCII 0x21–0x7e (length ≤4096)
  and rejecting everything else as SETUP.
- Pass the cursor as a single argv token `--cursor=<value>`, never `--cursor <value>`, so a
  leading `-` cannot be parsed as an option. Use list argv, no shell.
- Anchor file read must be bounded (size cap) and schema must be exact: reject unknown keys
  rather than ignoring them, so a typo in `scope`/`boot_id` cannot be silently dropped.
- Diagnostics: the mismatch reason must not echo the observed `__CURSOR` or the anchor cursor on
  stdout. Stable reason codes only.

### F9 — Info (ordering with bounds)
Timeout/overflow/stderr/nonzero rc must all be checked before any success is emitted, including
when the first-record check already passed on a prefix. A truncated stream whose first line matched
must still be UNAVAILABLE. This is consistent with the spec; flagging only because the first-record
check is a natural place for an early return that would skip the rest of the bound checks.

## Pinned-spec checks that pass on read (no finding)
- Anchor is never advanced; end cursor reported only, never written (spec).
- `--cursor` form (not `--after-cursor`) with the first record dropped matches the local man page
  ("entries from the location", inclusive) and is consistent with sd_journal's inclusive seek.
- `--output-fields` including `__CURSOR` and `_BOOT_ID` matches the man page (always printed in
  json); `MESSAGE` is absent from the field list, consistent with "never MESSAGE".

## Residual risk
- Entire implementation unverified at read time (file absent). F1, F3, F5, F6 are the
  highest-consequence items to recheck first when the tool lands.
- journalctl real behavior on an absent cursor on this host is inferred from the seek docs
  (systemd 262 docs; host has 261.2). Not confirmed by execution; execution is forbidden for this
  lane. [INFERENCE] until L1 runs the harness.
- S014/S015 not opened by this lane.

## Verification gaps
- No code read (absent).
- No fixture read (absent).
- No execution of journalctl, tools, or tests (by assignment).
- Local man page is systemd 261.2; seek docs read are systemd 262 "latest". Version delta not
  resolved.

## Recommended checks for L1 once WindowTool lands
1. Grep the landed tool for the first-record compare: exact `__CURSOR` string equality, boot
   equality, non-object first element handling.
2. Confirm argv contains `--user`/`--system` per scope and `--cursor=<value>` single token.
3. Confirm empty-stdout rc0 → UNAVAILABLE, and anchor-only → rc0 zero.
4. Confirm anchor-repeat in later records → UNAVAILABLE (F6).
5. Confirm SETUP vs UNAVAILABLE split (F4) with one case each.
6. Confirm no cursor/record echo in stdout on any refusal path.

## Execution disclosure (added after L1 clarification)

- Ran `journalctl --version` once (local binary version string; no journal read, no query, no `--cursor`). Disclosed as an execution of the journalctl binary; not a live journal query, not a probe, not admissible as evidence for any finding.
- Ran `man -P cat journalctl` twice (local documentation read only).
- Ran read-only git commands (`status --porcelain`, `rev-parse HEAD`).
- No live journalctl queries, no measurement or probe loops, no background jobs, no tests, gates, builds, or smoke runs.
- Only write: this report. No /tmp output. No writes to other lanes.
- No findings in this report depend on the `--version` output; all findings derive from static spec text and primary docs.
