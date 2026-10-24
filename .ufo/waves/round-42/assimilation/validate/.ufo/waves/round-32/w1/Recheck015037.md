# Recheck S015, S037 — C1 freshness (round 32, wave 1)

Seat: MoriR32A2.Recheck015037. Both ids share one population URL; one live fetch served both rows
(the contract explicitly allows two ids sharing one URL to keep the same bytes).

Fetch: `curl -sSL --fail -m 60 <url> -o .../S015.src`, exit 0, at 2026-10-23T01:31:25Z.
Redirect check on the same URL: `redirects=0`, `code=200`, `effective=<population url>` — no move.
`S037.src` is `cp S015.src S037.src`; `cmp` reports identical bytes.

## 1. Per id: url, accessed, size, sha256, scratch copy

- S015 — https://www.freedesktop.org/software/systemd/man/latest/systemd.journal-fields.html —
  2026-10-23T01:31:25Z — 33900 bytes —
  sha256 `906e5d34b38913ddaf729f74f468f5511f8a143bb3f86f0fdda06957af7bf5e7` —
  `/fast/scratch/hyaku/mori-r32/MoriR32A2.Recheck015037/S015.src`
- S037 — https://www.freedesktop.org/software/systemd/man/latest/systemd.journal-fields.html —
  2026-10-23T01:31:25Z — 33900 bytes —
  sha256 `906e5d34b38913ddaf729f74f468f5511f8a143bb3f86f0fdda06957af7bf5e7` —
  `/fast/scratch/hyaku/mori-r32/MoriR32A2.Recheck015037/S037.src`

Normalised text used for quoting:
`/fast/scratch/hyaku/mori-r32/MoriR32A2.Recheck015037/S015.norm.txt`
(`seat-check.py text S015.src`; 13947 bytes, one line). The live page still says
"systemd 262" (`S015.norm.txt:1`), matching both anchors.

## 2. Ready-to-paste table rows

```markdown
| S015 | https://www.freedesktop.org/software/systemd/man/latest/systemd.journal-fields.html | 2026-10-23T01:31:25Z | 906e5d34b38913ddaf729f74f468f5511f8a143bb3f86f0fdda06957af7bf5e7 | "The human-readable message string for this entry. This is supposed to be the primary text shown to the user"; "A 128-bit message identifier ID for recognizing certain message types"; "Fields prefixed with an underscore are trusted fields" | current |
| S037 | https://www.freedesktop.org/software/systemd/man/latest/systemd.journal-fields.html | 2026-10-23T01:31:25Z | 906e5d34b38913ddaf729f74f468f5511f8a143bb3f86f0fdda06957af7bf5e7 | "The name of a unit. Used by the system and user managers when logging about specific units"; "the systemd unit name, the unit name in the systemd user manager (if any)"; "of the process the journal entry originates from" | current |
```

## 3. Quote -> teaches-cell fact (S015)

- "The human-readable message string for this entry. This is supposed to be the primary text shown
  to the user" — supports "MESSAGE is display text rather than metadata": the page calls MESSAGE a
  human-readable message string and the primary text shown to the user
  (`S015.norm.txt:1`, section `MESSAGE=`). Quote is contiguous in normalised text (in_copy=True,
  seat-check below).
- "A 128-bit message identifier ID for recognizing certain message types" — supports "MESSAGE_ID is
  the typed key": the field is a 128-bit identifier for recognizing message types
  (`S015.norm.txt:1`, section `MESSAGE_ID=`).
- "Fields prefixed with an underscore are trusted fields" — supports "underscore-prefixed fields are
  trusted": direct definition in Trusted Journal Fields (`S015.norm.txt:1`).
Verdict `current`: the live page still carries all three passages verbatim; nothing in the
teaches cell (display-vs-metadata, MESSAGE_ID identifier, underscore trust) changed.

## 3b. Quote -> teaches-cell fact (S037)

- "The name of a unit. Used by the system and user managers when logging about specific units" —
  supports "UNIT/USER_UNIT identify units a manager logs about" (`UNIT= , USER_UNIT=` section,
  `S015.norm.txt:1`; the section still ends "Added in version 251", matching the anchor).
- "the systemd unit name, the unit name in the systemd user manager (if any)" — supports the trusted
  `_SYSTEMD_UNIT` description (`_SYSTEMD_CGROUP= , ... _SYSTEMD_UNIT=` section).
- "of the process the journal entry originates from" — supports "trusted _SYSTEMD_UNIT fields
  describe the emitting process": the `_SYSTEMD_*` group is defined as fields of the process the
  journal entry originates from (same `S015.norm.txt:1`). The page never says "failed subject"; the
  "not necessarily the failed subject" part is the contrast with `UNIT=` (manager logging about a
  unit) versus `_SYSTEMD_UNIT` (origin process), which the page's wording supports.
Verdict `current`: the live page still defines UNIT/USER_UNIT for manager logs about units and
_SYSTEMD_UNIT for the process the entry originates from; no drift.

## 4. Seat-check output (verbatim)

```
$ timeout 300 python3 .../round-32/seat-check.py row S015 S015.src '<quotes>'
sha256=906e5d34b38913ddaf729f74f468f5511f8a143bb3f86f0fdda06957af7bf5e7
quotes=3 words=[19, 10, 8] in_copy=[True, True, True]
shared_tokens=['fields', 'message', 'prefixed', 'text', 'trusted', 'underscore', 'user'] topic_ok=True
live_quotes_ok=True
ROW_CHECK=pass (judge R4 and R5 not checked here)

$ timeout 300 python3 .../round-32/seat-check.py row S037 S037.src '<quotes>'
sha256=906e5d34b38913ddaf729f74f468f5511f8a143bb3f86f0fdda06957af7bf5e7
quotes=3 words=[17, 14, 8] in_copy=[True, True, True]
shared_tokens=['journal', 'manager', 'process', 'systemd', 'unit', 'units', 'user'] topic_ok=True
live_quotes_ok=True
ROW_CHECK=pass (judge R4 and R5 not checked here)
```

## 5. Drift details

None. Both rows are `current`; no `Round32` correction paragraphs are needed.

Notes: no tool installed or updated (nothing needed); no pacman run. All processes bounded with
`timeout` and finished before return. Scratch dir:
`/fast/scratch/hyaku/mori-r32/MoriR32A2.Recheck015037/`.
