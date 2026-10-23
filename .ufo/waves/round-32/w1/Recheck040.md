# Recheck040 — S040 (C1 freshness)

Seat: MoriR32A2.Recheck040. Question: does the live `sd_journal_test_cursor` page still support the S040 row's teaches cell? Verdict: **current**.

## 1. Fetch record

- id: **S040**
- population url: https://www.freedesktop.org/software/systemd/man/latest/sd_journal_test_cursor.html
- effective url (curl `%{url_effective}`, `%{num_redirects}`=0): same URL, HTTP 200 — **no redirect**.
- fetch command: `curl -sSL --fail -m 60 <url> -o /fast/scratch/hyaku/mori-r32/MoriR32A2.Recheck040/S040.src` (attempt 1 of 3 succeeded; stderr log at `/fast/scratch/hyaku/mori-r32/MoriR32A2.Recheck040/S040.fetch.txt`)
- accessed (UTC at fetch): 2026-10-23T01:31:25Z
- byte size: 8434
- sha256: 5ada44c28aa31dc7495276e2bf6a11a3370e33ae71277051736641882e5e9980
- scratch copy: `/fast/scratch/hyaku/mori-r32/MoriR32A2.Recheck040/S040.src` (bytes saved unchanged; `file`-head confirms DocBook HTML, `<title>sd_journal_get_cursor</title>`)
- normalised text used for quoting: `/fast/scratch/hyaku/mori-r32/MoriR32A2.Recheck040/S040.norm.txt` (`seat-check.py text S040.src`)
- page identity: rendered page reads "systemd 262" (`systemd 262` occurs in the normalised text), matching the anchor's "systemd 262 page accessed 2026-10-20". History section still says get_cursor added in 187, test_cursor in 195.
- note for the integrator: `corpus/evidence/recheck-r32/S040.src` must be a byte-identical copy of the scratch file above (sha 5ada44c2…9980); the lane is outside this seat's write bound.
- tooling installed/updated: none.

## 2. Ready-to-paste Recheck row

```markdown
| S040 | https://www.freedesktop.org/software/systemd/man/latest/sd_journal_test_cursor.html | 2026-10-23T01:31:25Z | 5ada44c28aa31dc7495276e2bf6a11a3370e33ae71277051736641882e5e9980 | "the same entry might be referred to by multiple different cursor strings, and hence string comparing cursors is not possible"; "whether the entry being sought to was actually found in the journal or the next closest entry was used instead"; "Seeking to a cursor position without the specific entry being available locally will seek to the next closest (in terms of time) available entry" | current |
```

## 3. Quote → teaches-cell mapping

Teaches cell: *Cursor strings do not uniquely identify an entry, so string comparison is not an identity test; sd_journal_test_cursor verifies the sought entry after a seek. No deduplication or completeness is implied.*

All three quotes are contiguous substrings of the `seat-check.py text` output (normalised), not of the rendered page; each starts and ends on a whole word, none drops a negation or prefix, none contains `&`, a pipe, a typographic character or page furniture.

- Quote 1 — `the same entry might be referred to by multiple different cursor strings, and hence string comparing cursors is not possible` (20 words). Bears on clauses 1–2: aliasing (one entry, several cursor strings) and the page's own conclusion that string comparison cannot be used as an identity test. It is the anchor sentence's continuation, so it also re-verifies the anchor verbatim.
- Quote 2 — `whether the entry being sought to was actually found in the journal or the next closest entry was used instead` (20 words). Bears on clause 2's second half: the test call exists to verify, after a seek, that the sought entry was actually found rather than a neighbour. In the page this is the object of "Use this call to verify after an invocation of sd_journal_seek_cursor (3) , …"; the fragment omits the cross-reference artifact only, not any negation.
- Quote 3 — `Seeking to a cursor position without the specific entry being available locally will seek to the next closest (in terms of time) available entry` (24 words). Bears on why verification is required: a seek may land on the next closest entry, so the sought entry is not guaranteed. Keeps the negation "without".
- Shared content tokens (seat-check): cursor, different, entry, journal, might, multiple, referred, seek, sought, string, strings — 11, well over the 2 required, and they hit teaches/anchor/scope terms directly ("cursor", "entry", "seek/sought", "string", "multiple").

Why `current` follows: the page still states verbatim that "cursor strings do not uniquely identify an entry", that "the same entry might be referred to by multiple different cursor strings, and hence string comparing cursors is not possible", and that the test call verifies after a seek whether the sought entry was found or the next closest used. Nothing on the page adds a uniqueness, deduplication or completeness guarantee, so the teaches cell's negative clauses are also unopposed. The used-by note at `corpus/knowledge/journal-cursor-window-r16.md:25` quotes "identifies a journal entry globally and in a stable way" and the aliasing sentence; both are still present verbatim in the live normalised text, so no correction is due.

## 4. seat-check output (verbatim)

```
$ timeout 300 python3 .ufo/waves/round-32/seat-check.py row S040 S040.src "$(cat quotes.txt)"
sha256=5ada44c28aa31dc7495276e2bf6a11a3370e33ae71277051736641882e5e9980
quotes=3 words=[20, 20, 24] in_copy=[True, True, True]
shared_tokens=['cursor', 'different', 'entry', 'journal', 'might', 'multiple', 'referred', 'seek', 'sought', 'string', 'strings'] topic_ok=True
live_quotes_ok=True
ROW_CHECK=pass (judge R4 and R5 not checked here)
```

`live_quotes_ok=True`: seat-check re-fetched the live URL itself and found all three quotes in its own normalisation, independent of my saved copy.

## 5. Drift details / correction

None. Verdict is `current`; no `Round32` correction is drafted for `corpus/knowledge/journal-cursor-window-r16.md`.

Residual observations (not drift):

- The URL still serves the combined page titled/`<title>`d `sd_journal_get_cursor` covering both functions, as `corpus/SOURCES.md:46` already records ("page served as sd_journal_get_cursor"). Version is still 262.
- The page's Description still says "The cursor identifies a journal entry globally and in a stable way" and separately "cursor strings do not uniquely identify an entry"; the tension between those two sentences is what the knowledge note already discusses (line 25), and this round's bytes do not change it.

Remaining unknowns: none for S040. (Whether a cursor string can also match more than one entry is not stated by the page — unchanged, and the knowledge note already records that as an explicit limit.)
