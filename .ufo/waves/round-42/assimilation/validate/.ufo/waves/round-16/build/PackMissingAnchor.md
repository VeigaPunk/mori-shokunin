# PackMissingAnchor — round-16 fixture pack report

## Files changed (exclusive write)
- `.ufo/waves/round-16/fixtures/MissingAnchor.json` — new, 3060 bytes,
  sha256 `fca571e28ceeb7acf25afea9540b375fa2a071f5bb57e3f66e196cd51c1a7646`.

## Behavior covered (4 distinct cases, all refusal-arms of the topic)
Topic: missing/vacuumed anchor and empty capture must yield rc2
`MORI_JOURNAL_WINDOW_UNAVAILABLE` — never a positive window, never a count.

1. `empty_stdout_anchor_unproven` (scope=user) — journalctl wrapper returns
   rc0, empty stderr, and zero stdout bytes. With no first record the anchor
   cursor is unproven → rc2 unavailable. Catches an implementation that
   treats empty output as an empty post-anchor window (rc0, 0 records).
2. `nearest_cursor_not_anchor` (scope=system) — single valid-looking record
   on the anchor's boot whose `__CURSOR` differs in the last hex nibble
   (`...x=10ff00ef` vs anchor `...x=10ff00ee`): the "nearest but different"
   shape a vacuumed or seek-approximate capture produces. Exact-equality
   must fail → rc2; any prefix/substring match or "close enough" acceptance
   leaks counts.
3. `anchor_present_but_not_first` (scope=user) — the anchor record exists in
   the stream but is NOT the first parsed record; a same-boot positive
   (98e32220 killed/9) precedes it. Contract requires the FIRST record to
   match anchor cursor+boot exactly → rc2. Separates "anchor somewhere in
   stream" (wrong) from "anchor is first record" (required).
4. `anchor_vacuumed_positive_trap` (scope=user) — anchor fully absent;
   stream contains only later same-boot records including a catalog
   kernel-OOM (`fe6faa94e7774663a0da52717891d8ef`) and a coredump
   (`fc2e22bc6ee647b6b90729ab34a250b1`). Even with real positive material
   present, the window is unavailable: rc2 and no positive totals may be
   emitted (contract: unavailable → no numeric positive totals).

Every case sets `want_rc: 2`, `want_id: "MORI_JOURNAL_WINDOW_UNAVAILABLE"`,
`stderr: ""`, `returncode: 0` on the stub. `want` is omitted on all cases:
unavailable results carry no positive-total fields.

## Retained evidence
- Catalog MESSAGE_ID bytes verified against `tools/mori-census.sh` lines
  1032–1036 (JOURNAL_ID_* constants) before writing: kernel OOM
  `fe6faa94e7774663a0da52717891d8ef`, oomd `d989611b15e44c9dbf31e3c81256e4ed`,
  coredump `fc2e22bc6ee647b6b90729ab34a250b1`, unit sigkill
  `98e322203f7a4ed290d09fe03c09fe15`, unit failure
  `d9b373ed55a64feb8242e02dbe79a49c`. **Discrepancy noted**: the dispatch
  hint's unit-failure id `d9b373ed55a64e6c8e2e7d70a0fce472` does NOT match
  census bytes; source is authoritative, hints are not (this pack uses
  `d9b373ed55a64feb8242e02dbe79a49c` where a unit-failure record appears).
- Local parse validation only (allowed static check, no tool/harness run):
  pack JSON loads, all `stdout` strings decode as JSONL with every line a
  valid JSON object, anchors satisfy schema mori-journal-anchor-v1
  (32-hex boot_id, printable scalar cursor, no control chars).
- No execution of mori-journal-window.py or any harness — per contract.

## Risks / blockers
- Schema questions sent to MoriR16.WindowHarness (exact id): whether rc2
  cases may omit `want` (chosen: omit) vs empty object; whether a stable
  `reason` token should be pinned (chosen: not pinned — contract leaves
  reason free-form stable); stdout-as-single-JSONL-string encoding (chosen
  per contract literal `"JSONL escaped string"`); whether wrapper scope
  derives from case `scope` field.
- If the harness later requires `want: {}` or a `reason` field for rc2,
  this pack needs a one-line-per-case update — flagged, not a current
  blocker.
- Anchor cursor strings are synthetic well-formed `s=…;i=…;b=…;m=…;t=…;x=…`
  journal cursor shapes matching the fixture example style; none are real
  host cursors, none echoed anywhere but inside this pack file.

## Tooling installs
None. No pacman/uv/npx transactions performed.
