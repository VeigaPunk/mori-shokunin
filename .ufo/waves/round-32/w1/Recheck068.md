# S068 — C1 recheck (wave 1, seat MoriR32A2.Recheck068)

## 1. Fetch record

| field | value |
|---|---|
| id | S068 |
| url | https://docs.python.org/3/library/os.html |
| accessed | 2026-10-23T01:31:23Z (`date -u +%FT%TZ` written immediately before the successful fetch) |
| bytes | 790778 |
| sha256 | 2ac87dd3ac1f30a3210cb1631c5bd41f3708f100cbeeb2b5874ea4b29e17d993 |
| scratch copy | /fast/scratch/hyaku/mori-r32/MoriR32A2.Recheck068/S068.src |
| normalised text | /fast/scratch/hyaku/mori-r32/MoriR32A2.Recheck068/S068.text (`seat-check.py text S068.src`, 188034 bytes) |

Command: `curl -sSL --fail -m 60 https://docs.python.org/3/library/os.html -o S068.src` — exit 0 on try 1 of 3.
No redirect: `curl -sS -o /dev/null -w 'effective=%{url_effective} code=%{http_code} redirects=%{num_redirects} size=%{size_download}\n' -L --max-time 60 <url>`
printed `effective=https://docs.python.org/3/library/os.html code=200 redirects=0 size=790778`.

Integrator action required: commit the unchanged bytes at `corpus/evidence/recheck-r32/S068.src`
(contract.md:23-24). My bounds allow writes only to this report and my scratch dir, so the copy is staged at the
scratch path above; sha256 must remain `2ac87dd3ac1f30a3210cb1631c5bd41f3708f100cbeeb2b5874ea4b29e17d993`.

## 2. Ready-to-paste row

```
| S068 | https://docs.python.org/3/library/os.html | 2026-10-23T01:31:23Z | 2ac87dd3ac1f30a3210cb1631c5bd41f3708f100cbeeb2b5874ea4b29e17d993 | "Perform the equivalent of an lstat() system call on the given path. Similar to stat() , but does not follow symbolic links."; "This function normally follows symlinks; to stat a symlink add the argument follow_symlinks=False , or use lstat() ."; "If follow_symlinks is False , and the last element of the path to operate on is a symbolic link" | current |
```

All three quotes are verbatim substrings of the normalised copy (each occurs exactly once; verified with
`str.count`), are pure ASCII with no `&`, `|`, or zero-width characters, and start and end on whole words.

## 3. Quote → teaches-cell bearing

Teaches cell: "A report-presence check must lstat the final component: os.stat follows a symlink by default, lstat
inspects the link itself."

1. `Perform the equivalent of an lstat() system call on the given path. Similar to stat() , but does not follow
   symbolic links.` — os.lstat entry, normalised offset 69547, immediately after the signature
   `os. lstat ( path , * , dir_fd = None )`. Bears on "lstat inspects the link itself": it states lstat does not
   follow symbolic links and is otherwise stat-like, i.e. the difference is confined to the link itself. The
   negation is kept intact inside the quote.
2. `This function normally follows symlinks; to stat a symlink add the argument follow_symlinks=False , or use
   lstat() .` — os.stat entry, offset 91963, inside
   `os. stat ( path , * , dir_fd = None , follow_symlinks = True )` (signature verified present). Bears on
   "os.stat follows a symlink by default" and names the two escapes: `follow_symlinks=False` or `lstat()`. This
   is the same sentence already recorded at corpus/lessons/round-20.md:47, so the teachable wording has not moved.
3. `If follow_symlinks is False , and the last element of the path to operate on is a symbolic link` — the
   "not following symlinks" paragraph of the follow_symlinks section, offset 57549. Bears on the "final component"
   scope: the paragraph's scope is exactly the last element of the path. The quote keeps the conditional prefix
   (`If follow_symlinks is False , and`) rather than cutting it, per the control-wave rule; the consequence clause
   was left out only because the full sentence is 28 words and the limit is 25, and quote 1 already supplies the
   consequence ("does not follow symbolic links").

Verdict `current`: all three passages are live, unchanged in language, and jointly state both halves of the teaches
cell (stat follows by default; lstat operates on the link; the distinction is the final path component). The
used-by claims were checked against the live page and still hold: corpus/knowledge/wave-settlement-r20.md:6,81,87
cites S068 for "os.stat/lstat symlink semantics" and relies on "lstat-then-open" path checks;
corpus/lessons/round-20.md:47,75 quotes the very sentence in quote 2.

## 4. seat-check output

```
$ timeout 300 python3 .ufo/waves/round-32/seat-check.py row S068 S068.src '<quotes cell from §2>'
sha256=2ac87dd3ac1f30a3210cb1631c5bd41f3708f100cbeeb2b5874ea4b29e17d993
quotes=3 words=[22, 18, 19] in_copy=[True, True, True]
shared_tokens=['follow', 'follows', 'link', 'lstat', 'path', 'stat', 'symlink', 'symlinks'] topic_ok=True
live_quotes_ok=True
ROW_CHECK=pass (judge R4 and R5 not checked here)
rc=0
```

## 5. Drift details

No material drift, so no `Round32` correction is drafted (contract.md:25-26 requires one only for `drifted`).

Observed non-material change: the page header now reads `Python 3.15.1 documentation` (normalised text offset 49),
while the population anchor cell says "Python 3.15.0 docs opened 2026-10-21". This is a docs version-label bump on
the in-development `/3/` branch; the two entries the row anchors on carry the same wording as on 2026-10-21
(quote 2 is byte-identical, after typographic folding only, to the sentence preserved in
corpus/lessons/round-20.md:47), and `os.stat`'s `follow_symlinks = True` default and `os.lstat`'s
`follow_symlinks=False` equivalence are unchanged. If the integrator wants the anchor date/label refreshed, that is
an SOURCES anchor edit, not a verdict change; R1-R5 do not require it.

## 6. Housekeeping

- No tools installed or updated this seat; no pacman/uv/npx invocation.
- No git or jj writes in the lane or fleet repo; read-only greps and reads only.
- No subagents, no background jobs; all commands capped with `timeout` (max 300 s) and all finished.
- Files written: this report and four scratch files under
  /fast/scratch/hyaku/mori-r32/MoriR32A2.Recheck068/ (`S068.src`, `S068.text`, `S068.text.err`,
  `S068.accessed.txt`).
