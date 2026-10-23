# Recheck039 — S039 (C1 freshness)

Seat: MoriR32A2.Recheck039. Question: does the live sd_journal_seek_cursor page still support the S039 row's teaches cell? Verdict: **current**.

## 1. Fetch record

- id: **S039**
- population url: https://www.freedesktop.org/software/systemd/man/latest/sd_journal_seek_cursor.html
- effective url (curl `%{url_effective}`, `%{num_redirects}`=0): same URL, HTTP 200 — no redirect.
- fetch command: `curl -sSL --fail -m 60 <url> -o /fast/scratch/hyaku/mori-r32/MoriR32A2.Recheck039/S039.src` (try 1 succeeded)
- accessed (UTC at fetch): 2026-10-23T01:31:24Z
- byte size: 9052
- sha256: b13d9928c1ea07a6a75dfe80d2227405c1f3ea6ac5b708219bef44fe15f6cd7b
- scratch copy: /fast/scratch/hyaku/mori-r32/MoriR32A2.Recheck039/S039.src
- normalised text (seat-check.py text): /fast/scratch/hyaku/mori-r32/MoriR32A2.Recheck039/S039.norm.txt
- page identity: the rendered title reads "systemd 262", matching the anchor's "systemd 262 page accessed 2026-10-20".
- tooling installed/updated: none.

## 2. Ready-to-paste Recheck row

```markdown
| S039 | https://www.freedesktop.org/software/systemd/man/latest/sd_journal_seek_cursor.html | 2026-10-23T01:31:24Z | b13d9928c1ea07a6a75dfe80d2227405c1f3ea6ac5b708219bef44fe15f6cd7b | "If no entry matching the specified cursor is found the call will seek to the next closest entry (in terms of time) instead."; "these calls do not actually make any entry the new current entry" | current |
```

## 3. Quote → teaches-cell mapping

Teaches cell: *A seek to an absent cursor lands on the next closest entry in time, and seeking does not by itself make that entry current.*

- Quote 1 — `If no entry matching the specified cursor is found the call will seek to the next closest entry (in terms of time) instead.` (23 words). Bears on clause 1: absent/non-matching cursor → seek to next closest entry by time. It is the exact anchor sentence, found verbatim in the live normalised text (`seat-check.py text` output). Supports verdict `current`.
- Quote 2 — `these calls do not actually make any entry the new current entry` (12 words). Bears on clause 2: after a seek, no entry becomes current until a separate `sd_journal_next(3)` call. Verbatim substring of the live sentence "Note that these calls do not actually make any entry the new current entry, this needs to be done in a separate step with a subsequent sd_journal_next (3) invocation (or a similar call)." Supports verdict `current`.
- Shared content tokens (seat-check): call, closest, current, cursor, entry, found, instead, make, matching, next, seek, specified, terms, time — 14, well over the 2 required.
- Both quotes were copied from the `seat-check.py text` output, not the rendered page; both start and end on whole words; neither drops a negation (quote 2 keeps "do not"); neither contains `&`, a pipe, a typographic character, or page furniture.

Why `current` follows: the two clauses of the teaches cell are each stated verbatim by the live page, and nothing on the page contradicts them. The fallback rule also matches prose the page repeats: "If no entry exists that matches exactly the specified seek address, the next closest is sought to."

## 4. seat-check output (verbatim)

```
$ timeout 300 python3 .ufo/waves/round-32/seat-check.py row S039 S039.src '"If no entry matching the specified cursor is found the call will seek to the next closest entry (in terms of time) instead."; "these calls do not actually make any entry the new current entry"'
sha256=b13d9928c1ea07a6a75dfe80d2227405c1f3ea6ac5b708219bef44fe15f6cd7b
quotes=2 words=[23, 12] in_copy=[True, True]
shared_tokens=['call', 'closest', 'current', 'cursor', 'entry', 'found', 'instead', 'make', 'matching', 'next', 'seek', 'specified', 'terms', 'time'] topic_ok=True
live_quotes_ok=True
ROW_CHECK=pass (judge R4 and R5 not checked here)
```

Note `live_quotes_ok=True`: seat-check re-fetched the live URL and both quotes were present in its own normalisation, independent of my saved copy.

## 5. Drift details / correction

None. Verdict is `current`, so no `Round32` correction is drafted for `corpus/knowledge/journal-cursor-window-r16.md`. For the record, that file's line 17 already quotes the same fallback sentence, and its line 25 claims about cursor identity are on S040, outside this recheck.

Remaining unknowns: none for S039. (Whether the *CLI* `journalctl --cursor=` shares this fallback remains undetermined — the knowledge note already records that as an explicit gap, line 77, and this page does not speak to the CLI.)
