# Recheck S014 — C1 wave 1 (seat Recheck014)

Seat scratch: `/fast/scratch/hyaku/mori-r32/Recheck014/`

## 1. Fetch record

- id: **S014**
- url (population, unchanged): `https://www.freedesktop.org/software/systemd/man/latest/journalctl.html`
- accessed (UTC, at fetch): `2026-10-23T01:31:24Z`
- HTTP: `HTTP_CODE=200`, no redirect (`FINAL_URL=` identical to the population url, single fetch, exit 0)
- byte size: 87375 (`-rw-r--r-- 1 vgpnk vgpnk 87375 Oct 22 22:31 S014.src`)
- sha256: `75440570fb1f71859229ca88fed0a6764b2057c7dd90651701b3d022a5649722`
- scratch copy (bytes unchanged): `/fast/scratch/hyaku/mori-r32/Recheck014/S014.src`
- normalised text: `/fast/scratch/hyaku/mori-r32/Recheck014/S014.text` (41412 bytes)
- fetch stderr: `S014.fetch.txt` is empty (no failures; no retry needed)

Page identity still matches the anchor's `systemd 262`: normalised header reads
`journalctl Index · Directives systemd 262 Name journalctl - Print log entries from the systemd journal`
(S014.text offset 38; `grep -c 'systemd 262' S014.text` -> `1`).

Anchor section names re-located on the live page (S014.text offsets):

| anchor element | live position |
|---|---|
| `Source Options` | 4470 |
| `Filtering Options` (contains `--after-cursor` at 8754) | 7605 |
| `Output Options` (contains `--output-fields` at 18703) | 15262 |

## 2. Ready-to-paste Recheck row

```markdown
| S014 | https://www.freedesktop.org/software/systemd/man/latest/journalctl.html | 2026-10-23T01:31:24Z | 75440570fb1f71859229ca88fed0a6764b2057c7dd90651701b3d022a5649722 | "The following options control where to read journal records from"; "Start showing entries from the location in the journal after the location specified by the passed cursor"; "A comma separated list of the fields which should be included in the output" | current |
```

## 3. Quote -> teaches-cell mapping

Teaches cell: *Select journal scope and cursor bounds, and request only structured fields for count-only queries.*

1. **"The following options control where to read journal records from"** (10 words, S014.text 4530-ish, under `Source Options ¶`) bears on **journal scope**: the live page still presents these as the scope/selection options (`--system`, `--user`, `-M`, `-m`, `-D`, `-i`, `--root`). Starts and ends on whole words; no tag-space artefacts inside the quote (the following `: --system , --user` comma spacing was left out of the quote on purpose).
2. **"Start showing entries from the location in the journal after the location specified by the passed cursor"** (17 words, the `--after-cursor=` body at S014.text 8754, inside `Filtering Options`) bears on **cursor bounds**: bounds are still expressed by passing a cursor and starting after that location. No negation or prefix was trimmed.
3. **"A comma separated list of the fields which should be included in the output"** (14 words, the `--output-fields=` body at S014.text 18703, inside `Output Options`) bears on **requesting only structured fields**: the option still restricts output to the named fields, which is the field-limited JSON/cat behaviour the row teaches. The continuation ("This has an effect only for the output modes which would normally show all fields ... as well as on cat") was not quoted because those mode lists render with tag-induced ` , ` spacing.

Shared content tokens with teaches+anchor+scope (computed by the counter): `cursor`, `fields`, `journal`, `options`, `output` (5 >= 2). Verdict follows because every clause of the teaches cell is still stated by the live page, and the page is still the `systemd 262` revision the anchor names.

## 4. seat-check output

```
$ timeout 300 python3 .../seat-check.py row S014 S014.src '"The following options control where to read journal records from"; "Start showing entries from the location in the journal after the location specified by the passed cursor"; "A comma separated list of the fields which should be included in the output"'
sha256=75440570fb1f71859229ca88fed0a6764b2057c7dd90651701b3d022a5649722
quotes=3 words=[10, 17, 14] in_copy=[True, True, True]
shared_tokens=['cursor', 'fields', 'journal', 'options', 'output'] topic_ok=True
live_quotes_ok=True
ROW_CHECK=pass (judge R4 and R5 not checked here)
```

## 5. Drift details / correction draft

**Verdict: `current` — no drift, so no `Round32` correction is drafted.** All five used-by files exist in the lane (`corpus/knowledge/…r12.md`, `…scopes-r13.md`, `…positive-evidence-r15.md`, `…cursor-window-r16.md`) and the page they cite is unchanged in substance.

One anchor note (not a verdict change): the numeric line anchors `--after-cursor:187-190` and `--output-fields:489-492` do not reproduce against this fetch either — the `--after-cursor=` text sits at 8754 and `--output-fields=` at 18703 of the single-line normalised text, and the rendered headings land far from 187/489. This is the same discrepancy already recorded append-only in `corpus/SOURCES.md:207` (2026-10-20 Registry seat correction: "the rendered `--after-cursor=` heading falls near display line 193, not 187-190; the section headings they name were confirmed"). Section names and the teaches/scope cells hold; immutable anchor cells were not edited.

## Tooling

Nothing installed or updated this seat (curl, python3, sha256sum already present). No pacman/lane/git writes performed; all writes confined to this report and `/fast/scratch/hyaku/mori-r32/Recheck014/`.
