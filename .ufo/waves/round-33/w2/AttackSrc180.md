# AttackSrc180 — wave 2 attack on source row S180

Seat: MoriR33.AttackSrc180 (leaf). Target: `corpus/SOURCES.md:186`, Gate row `corpus/lessons/round-33.md:15`,
committed copy `corpus/evidence/sources-r33/S180.src` at lane revision
62db24c01d5b7c2247f43852ea2b28d0ae5e40c8. Verdict: **no blocker, no major. Two minor anchor/scope gaps, both
free to repair and both outside what the C1 counter parses.**

## 1. Live re-open and hashes

- URL: `https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/block/stat.rst`.
- Command: `curl -sSL --fail -m 60 -w 'HTTP:%{http_code} SIZE:%{size_download} URL:%{url_effective}' <url> -o live.src`
  → `HTTP:200 SIZE:4315 URL:https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/block/stat.rst`
  (no redirect, no 429, no retry needed). Response headers include `content-length: 4315` and `x-cache: HIT`
  (`/fast/scratch/hyaku/mori-r33/AttackSrc180/hdrs.txt`).
- `sha256sum live.src` → `4c35b795a518ceefea985f11e53b51f71d58fc99bf5a0920ca3738f13c90cb2e` = Gate sha256
  (`round-33.md:15`) = `sha256sum corpus/evidence/sources-r33/S180.src` = the copy at revision 62db24c
  (`git show 62db24c:corpus/evidence/sources-r33/S180.src | sha256sum`). Three-way match.
- Byte-identity to the ref, not just to the Gate: `api.github.com/repos/torvalds/linux/contents/Documentation/block/stat.rst?ref=v7.2`
  → `{'sha': 'a1cd9db2058f94a4918112842a2441df9f3cb2fb', 'size': 4315, 'type': 'file'}`, and
  `cat S180.src | git hash-object --stdin` → `a1cd9db2058f94a4918112842a2441df9f3cb2fb`. The committed copy is the
  exact blob at tag v7.2; no CRLF/BOM/truncation is possible (`file`: ASCII text, 103 lines, ends `example).\n`).

## 2. Quote locators and containment (all four verified)

| Gate locator | stated words | measured | line text at locator |
|---|---|---|---|
| `S180.src:21-22` | 17 | 17 | 21 `The stat file consists of a single line of text containing 17 decimal` / 22 `values separated by whitespace.  The fields are summarized in the` |
| `S180.src:71-73` | 13 | 13 | 71 `... The "sectors" in question are the` / 72 `standard UNIX 512-byte sectors, not any device- or filesystem-specific` / 73 `block size.  The counters are incremented when the I/O completes.` |
| `S180.src:73` | 8 | 8 | quote is the tail of line 73 |
| `S180.src:79-80` | 17 | 17 | 79 `... If there are multiple I/O requests waiting,` / 80 `these values will increase at a rate greater than 1000/second; for` |

- Containment: all four quotes are substrings of the copy after collapsing whitespace runs to one space
  (`tr -s '[:space:]' ' '`, 4/4 `COLLAPSED-HIT`; counter's own `norm` replica also 4/4 `True`).
- All four locators point at the lines that actually hold the quoted words. No mislocated quote.
- Note (not a defect): quote 2 begins mid-sentence at line 71 (subject `The "sectors" in question` dropped) and
  quote 4 truncates before `; for example...`. Both are verbatim contiguous fragments, so R-J's "located in the
  committed copy" is satisfied; I record it only so the judge is not surprised by the fragments.

## 3. SOURCES cells against quotes and anchored lines

- Anchor `Documentation/block/stat.rst:21-22,71-73,79-80; tag v7.2`: every locator verified (§2);
  `api.github.com/repos/torvalds/linux/git/ref/tags/v7.2` → `{"ref":"refs/tags/v7.2", "object":{"sha":"237a1c39e8dfd3e1c6f1f023eea37a48cc63"… "type":"tag"}}`.
  v7.2 is a real annotated tag, so the anchor's "tag v7.2" is true.
- Teaches cell `corpus/SOURCES.md:186`: clause by clause —
  (a) "one line of 17 decimal values" = quote 1; (b) "standard 512-byte sector, not a device or filesystem block
  size" = quote 2; (c) "grow when an I/O completes" = quote 3; (d) "tick values can rise faster than 1000 per
  second when several requests wait" = quote 4 except for the word "tick" (finding F1). No other clause
  overreaches; the copy's own field table (17 rows, `S180.src:29-45`) independently matches the "17" claim.
- Scope cell "the v7.2 /sys/block/<dev>/stat format: the 17-value line, the 512-byte sector unit, completion-time
  counting and the tick fields": the format claims are quotes 1-4; the path `/sys/block/<dev>/stat` is stated at
  `S180.src:2` and `S180.src:5` but is not inside the anchored ranges (finding F2).
- `kind=docs`: the file is `Documentation/block/stat.rst`, prose documentation. `tier=A`: official upstream
  (torvalds/linux) primary source; matches the registry's A usage for other v7.2 docs/code rows (e.g. `S003`,
  `S181`). Status `mined` and `used-by corpus/knowledge/disk-write-rate-r33.md` are accurate: rows 1, 2, 7, 12
  (`disk-write-rate-r33.md:19,20,25,30`) cite S180.

## 4. Findings

### F1 — minor: the "tick" attribution is stated only by copy lines that are in neither the quote nor the anchor
Attacks `corpus/SOURCES.md:186` (teaches clause "tick values can rise …") and, through it,
`corpus/knowledge/disk-write-rate-r33.md:25` (row 7 reading "this tick value climbs by more than 1000 for each
wall-clock second"). Evidence: quote 4 is `S180.src:79-80` and says only "these values"; the referent is fixed by
`S180.src:78` ("These values count the number of milliseconds that I/O requests have waited on this block device.")
and the section header `S180.src:75` ("read ticks, write ticks, discard ticks, flush ticks"). The anchor lists only
21-22,71-73,79-80. So the word "tick" is not in the quotes and not in the anchored lines, though it is in the copy
two lines above the quote.
Counter-safe repair (anchor cell only): write `Documentation/block/stat.rst:21-22,71-73,75,78-80; tag v7.2`. Do NOT
extend the Gate quote to 78-80: that passage is 33 words, over the counter's 25-word cap
(`count-c1-a1.py`, gate_fields check), and a fifth quote exceeds its 4-quote cap — the anchor cell is not parsed by
the counter, so putting the referent lines there is the only zero-risk fix.

### F2 — minor: scope names `/sys/block/<dev>/stat`, which no quoted or anchored line states
Attacks `corpus/SOURCES.md:186` (scope cell). Evidence: the path appears at `S180.src:2` ("Block layer statistics in
/sys/block/<dev>/stat") and `S180.src:5` ("This file documents the contents of the /sys/block/<dev>/stat file."), and
neither line is in the anchor range 21-22,71-73,79-80. The claim is true of the page; only the anchor is incomplete.
Counter-safe repair: add `:2` or `:5` to the anchor cell (anchor text is not machine-checked).

### F3 — none: no duplicate registration, no stale copy, no conflicting second S180
Checks: `grep -c 'block/stat.rst' corpus/SOURCES.md` → `1`; `grep -o 'https\?://[^ |)]*' corpus/SOURCES.md | sort |
uniq -c | sort -rn` shows S180's URL is not among the duplicated URLs; at the entering tip
`git show 7d382043016e8854e3be2ee523a095b409c3d8a1:corpus/SOURCES.md | grep -c 'Documentation/block/stat.rst'` → `0`;
`grep -c '^| S180 ' corpus/SOURCES.md` → `1` and `grep -c '^| S180 ' corpus/lessons/round-33.md` → `1`;
only `corpus/evidence/sources-r33/S180.src` exists for this id (no stale r32 copy).

## 5. Counter replica (row S180 only, no verdict issued)

Parsed `round-33.md:15` at revision 62db24c with `count-c1-a1.py`'s own `cells`/`QUOTE_RE`/`norm`/`canon`:
`gate_rows 1`, `cells 6`, last cell `admit, A, mined`, `located 4 anyq 4`, words `17/13/8/17` (all inside 3-25),
`copy_sha_ok True`, `containment [True, True, True, True]`, `source_rows 1 url_in_source_cell True`,
`status_cell mined`. Six-word-run copying check (stricter than the counter, applied to observation+reading+verdict
of every S180-citing row): rows 1, 2, 7 and 12 all `sixgram_overlap_with_S180 0`. S180 survives every mechanical
gate on its own row.

## 6. Checks run that found nothing else

- Wave-1 provenance: `.ufo/waves/round-33/w1/SrcStatRst.md:9-13` records two fetches (02:39:46Z, 02:39:55Z), both
  4,315 bytes, both `4c35b795…`, `cmp` identical — the Gate header's "fetched twice" claim holds for S180, and my
  third fetch (02:58Z) agrees.
- Copy completeness: 103 lines, ends on a finished sentence, and its field table lists exactly 17 statistics,
  consistent with the document's own "17 decimal values" and with S187's 14 + 4 discard + 2 flush minus the 3
  identity fields.
- Consistency with the rows S180 supports: 512-byte unit and not-device-block-size (row 1), completion-time
  increment (row 2), >1000/s tick rate (row 7), one line of 17 whitespace-separated values (row 12) are each inside
  S180's quoted text. Row 1's `2**9` comes from S186's quote (`round-33.md:21`), row 7's field numbering from S187's
  (`round-33.md:22`) — neither is claimed from S180.

## 7. Remaining unknowns

- Whether the judge counts copy context around a located quote as part of "the quotes" under R-J. If it does, F1 is
  cosmetic; if it does not, F1 is the only thing standing between row 7 and a caveat. I cannot decide that rule.
- Other new ids S181-S190 were not audited by me (separate seats); the full `count-c1-a1.py` was not run (judge
  seat).

## 8. Containment and tooling

Read-only only: lane `git show/log/rev-parse/cat-file/hash-object`; no writes outside this report and
`/fast/scratch/hyaku/mori-r33/AttackSrc180/` (`live.src`, `hdrs.txt`, `collapsed.txt`). One `find` job I started
(`bg_2938`) was killed; no other process left running. No tool was installed or updated (nothing was needed).

Disclosure: my first write of this report used a relative path and landed at
`/home/vgpnk/Projects/shokunin/.ufo/waves/round-33/w2/AttackSrc180.md` (fleet root) for about two minutes, because
the session cwd is the fleet root, not the lane. I moved that file into the lane path above with `mv` and removed the
empty `.ufo/waves/round-33/w2` and `.ufo/waves/round-33` directories I had created (`rmdir`); `.ufo/waves/` itself
and every pre-existing fleet file are untouched, and no lane file other than this report was created or modified.
