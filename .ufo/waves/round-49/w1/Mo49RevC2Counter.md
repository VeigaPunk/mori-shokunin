# Mo49RevC2Counter — line review of `.ufo/waves/round-49/count-c2.py` (round 49, w1)

Seat: reviewer, C2 counter only. Leaf seat: no subagents. I edited nothing in the lane; my only
writes are this report and `.scratch/r49-Mo49RevC2Counter/`. All reads absolute, all lane-tool runs
with `TMPDIR=/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r49-Mo49RevC2Counter`.

## Frozen inputs checked first

| file | sha256 | compare |
|---|---|---|
| `.ufo/waves/round-49/count-c2.py` | `be39475d997f5cf4e67c7d69f66f176b1632985451ed0a6b8a5a4c2a495dd837` | == `evidence/freeze-sha256.txt`, == `git show 0df17b7:.ufo/waves/round-49/count-c2.py` |
| `corpus/evidence/sources-r49/journald.conf.5.html` | `b4a9b53e3e53dc5384bfffeb777218ced4c91712b0222b71405146ab470bc340` | == `COPIES`, == freeze receipt, == `git show HEAD:` |
| `corpus/evidence/sources-r49/systemd-journald.service.8.html` | `a7b443568865bb09f45d1ec83f3a8ad0e6a158d4e2cd21053e72499eb5f51212` | same |
| `corpus/evidence/sources-r49/journalctl.1.html` | `75440570fb1f71859229ca88fed0a6764b2057c7dd90651701b3d022a5649722` | same |
| `corpus/evidence/sources-r49/host-journal-reach.txt` | `be3952cb6fdac6d6ced15a9a0092447db80fe699221b8478970bb402a558eb12` | same |

`git rev-parse HEAD` = `0df17b7b4e667dd0aaaef0adc7d7d9973e6aa115` (the freeze commit); entering tip
`b3e3453d…` is its parent. At the entering tip the four copies do not exist, which is why the
do-nothing receipt reads `pins=bad`.

## 1. `normalise()` (lines 59–64) against the four real copies

Order: `script|style` block drop → comment drop → tag strip → `html.unescape` → whitespace collapse.

Measured layout of each committed copy (open/close counts via `re.finditer`, not grep):

| copy | bytes | `<script …>` open/close | `<style>` open/close | comments `<!--`/`-->` | normalised chars | stray `<`/`>`/`|` after normalise |
|---|---|---|---|---|---|---|
| journald.conf.5.html | 39204 | 2 / 2 (both external `src=`, empty body) | 1 / 1 | 0 / 0 | 22245 | 6 `<` (all from `&lt;`), 0 `>`, 0 `|` |
| systemd-journald.service.8.html | 28143 | 2 / 2 (same) | 1 / 1 | 0 / 0 | 13421 | 0 / 0 / 0 |
| journalctl.1.html | 87375 | 2 / 2 (same) | 1 / 1 | 0 / 0 | 41288 | 0 / 0 / 4 `|` (synopsis: `-u , --unit= UNIT | PATTERN`, etc.) |
| host-journal-reach.txt | 3026 | — | — | 0 | 2963 | 0 / 0 / 0 |

- No `<script>` opener in any copy has a `>` inside its attributes; the two scripts are external and
  their bodies are empty, so `<(script|style)\b.*?</\1\s*>` (line 60) is exercised only by the
  `<style>` block. That block is 432 bytes and **does** contain `>` (CSS child-combinator selectors);
  the non-greedy match to `</style>` removes it correctly — normalised text has 0 occurrences of
  `color-scheme`, `nav.js`, `jquery`, `{`, `}`, `</`.
- No copy contains an HTML comment at all, so line 61 is dead code on the frozen data (see F4).
- Uppercase/mixed-case `<SCRIPT>…</script>` is handled: Python applies `IGNORECASE` to the
  backreference `\1` (verified: `normalise("alpha <SCRIPT>var secret=1;</script> beta visible")` = `alpha beta visible`).
- `<script data-x="a>b">secret</script>` → `alpha beta` (handled).
- Unclosed constructs leak: `normalise("alpha <script>var secret=1; beta visible")` = `alpha var
  secret=1; beta visible`; `normalise("alpha <!-- hidden remark beta visible")` = `alpha <!-- hidden
  remark beta visible`. So "script, style and comment blocks dropped" holds only for closed blocks.
- Tag stripping over-eats prose containing a bare `<` and a later `>`: `normalise("size < 4G and free
  > 1G")` = `size 1G`. No live case: every raw `<` in the three pages starts a tag, and `&lt;`
  decodes only after stripping.
- `&nbsp;` → `\xa0` collapses under `\s+`; `&lt;` → `<` survives as visible text (6 in journald).

## 2. `parse_claims()` (lines 67–89)

Measured behaviour with fixtures built on the real normalised copies and 11-cell SOURCES rows:

| shape | result |
|---|---|
| standard table (8 rows, 3 cells) | `C2=met claims=8 located=8 …` |
| header + separator + all rows indented 4 spaces | `C2=met` (F3) |
| only some data rows indented 4 spaces | `C2=met` (F3) |
| header cells bold `**claim**`/`source`/`quote` | `C2=unmet … failed=…,table` (F11) |
| whole entry inside a fence | `C2=unmet` (arm 340) |
| second `claim/source/quote` table after a blank line | first table kept, second ignored (`claims=8`, `met`) — the blank line hits the break at lines 75–77, so a blank line inside a table truncates it |
| second table with a 4-column header | ignored (header never matches) |

- The blank-line branch at line 78–79 is effectively dead once rows exist: lines 75–77 `break`
  before line 78 is reached. The expression `header = header if rows else None` is therefore always
  `None` when executed. Harmless, but it reads as if blank lines were tolerated inside a table.
- Fence detection (line 70) uses `line.lstrip()[:3]`, so indented and 4-backtick fences toggle; the
  table-inside-fence arm (line 338–340) confirms the toggle is load-bearing.
- Header match (line 83) lowercases only; exact three cells, no bold/backtick tolerance.
- Entry rows are matched with `line.lstrip().startswith("|")` (line 75), i.e. **no 4-space rule on
  the entry side** — the asymmetry with `sources_row`'s `^ {0,3}` (line 94) is F3.

## 3. Row validation order (lines 136–186)

Order per row: cells/claim-word test → S-id/one-span test → quote word bounds + global uniqueness →
S-id registered (`ids_in_table.add`, line 150) → SOURCES lookup → `row_ok` (mined/opened/used-by/URL)
→ quote locate. Consequences I observed:

- `claims = len(rows)` (line 128) counts parsed rows **before** validation, so an unmet line can read
  `claims=8` with `bad_rows=1` (seen in the 4-word-claim and pipe-quote runs). Under `met` the two are
  equal because any bad row sets `bad_rows`.
- A bad row is skipped before the locate step, so it is counted once (in `bad_rows`), never in
  `quote_missing`/`located`. Consistent.
- `ids_in_table` receives the S-id before `row_ok`, so ids from rows already marked bad still gate
  `provenance` and `srows_ok` (line 180, 184). No `met` effect (bad ⇒ unmet), but the variable name
  overstates what it holds.
- `srows_ok` is `ok` only if `ids_in_table` is non-empty and `bad == 0` (line 184); the `source_rows`
  failure token is appended whenever it is not `ok` (185–186). It is a summary label, not an
  independent check.

## 4. `used-by` split (line 162)

`entry_path in [u.strip() for u in re.split(r"[,;]", srow[10])]` — exact match after strip.

- Real SOURCES rows use `", "`-separated lists (e.g. S003's used-by has three entries, S001 one).
- Tested: entry as second item after `", "` → `met`; after `","` with no space → `met` (strip makes
  both work); `used-by` = `—` → `bad_rows=8` (arm 318). So the comma split and the strip are both
  load-bearing for real rows, but **no arm exercises a multi-entry cell** (F6: removing either leaves
  all 26 arms green).
- Exact-string compare means a cell like `…/journal-reach-r49.md (this entry)` or a backticked path
  fails (F16).

## 5. The 0–3-space row rule (`sources_row`, line 94)

`^ {0,3}\|\s*S485\s*\|`. Pinned in both directions by arms 319–322: indent 3 → `met`, indent 4 →
`unmet`; mutants `0-3→0-4` and `0-3→0-2` each fail exactly one arm (`code_indented_row_unmet`,
`indented_row_ok`). This is the strongest-pinned guard in the file. The rule is not applied to lines
inside fenced blocks of SOURCES.md (no fences there today), and the first 0–3-space match wins if an
id is duplicated.

## 6. `own-work: host-journal-reach` matching (lines 36–44, 155–158)

The URL key is searched as a substring of **cell 1 only** (`u in srow[1]`), first dict key wins.
Measured with a realistic S488 row:

| S488 source cell | result |
|---|---|
| `own-work: host-journal-reach — …host-journal-reach.txt` | `C2=met … sources=4` |
| `host journal reach — …host-journal-reach.txt` | `C2=unmet … bad_rows=2` |
| `corpus/evidence/sources-r49/host-journal-reach.txt` (path only) | `C2=unmet … bad_rows=2` |
| `own-work host-journal-reach receipt` (no colon) | `C2=unmet … bad_rows=2` |

The exact literal is therefore mandatory. Wave-1 dispatch item 19 (`w1-spec.json[19]`) tells the row
scribe to write exactly those words, and items 16–18 give the three page URLs verbatim, so the
landing is coordinated; but nothing in P-C2 or the counter docstring (line 14 says "names its URL",
which is not a URL for the receipt) states the literal (F9).

## 7. The 26 selftest arms — 48 single-guard mutants

Copied the frozen file byte-identical into `.scratch/r49-Mo49RevC2Counter/.ufo/waves/round-49/`
(with `corpus` symlinked one level up so the selftest's `lane = dirname×3` resolves to the lane) and
mutated one guarded expression per run. Baseline reproduced twice: `C2_SELFTEST pass=26 fail=0`,
exit 0. 48 mutants, ~4.3 s total; "arm(s) that failed" is the list of `FAIL` lines from that run.

| line | guard | mutation | arm(s) that failed |
|---|---|---|---|
| 31 | `OPENED = "2026-10-25"` | →`2026-10-24` | `row_opened_other_day_unmet` |
| 32 | `MIN_CLAIMS = 8` | →9 / →7 | `honest_met`,`indented_row_ok` / `claims_floor_unmet` |
| 33 | `MIN_SOURCES = 3` | →2 / →4 / →5 | **NONE** / **NONE** / `honest_met`,`indented_row_ok` |
| 34 | `MIN_WORDS,MAX_WORDS = 6,25` | →4 / →7 / →24 / →40 | **NONE** ×4 (only the 2-word and 26-word fixtures are outside) |
| 60 | script/style drop | script arm removed / style arm removed | `normalise_drops_script_text` / `normalise_drops_style_text` |
| 61 | comment drop | regex → `t` | **NONE** (F4) |
| 62 | tag strip | regex → `t` | `normalise_keeps_visible_text` |
| 63 | `html.unescape` | off | **NONE** |
| 64 | whitespace collapse | off | CRASH (no `C2_SELFTEST` line) |
| 70 | fence toggle | `if False` | `table_inside_fence_unseen_unmet` |
| 76–77 | table scan break | `if False` | **NONE** |
| 79 | blank-line reset | (dead) | not separately mutable; see §2 |
| 83 | header lowercase | off | **NONE** (fixtures are already lowercase) |
| 94 | `^ {0,3}` | →`{0,4}` / →`{0,2}` | `code_indented_row_unmet` / `indented_row_ok` |
| 108 | pin `b is None or` | off | **NONE** |
| 108 | pin digest compare | always-mismatch | `pin_mismatch_unmet` |
| 118 | `entry is None` | off | CRASH |
| 121 | head window `[:14]` | →`[:40]` | **NONE** |
| 129 | claims-floor append | off | `claims_floor_unmet` |
| 136 | `len(cells) != 3` | →`< 3` | **NONE** |
| 136 | claim cell `<5` words | →`<1` | `claim_cell_short_unmet` |
| 139 | `sid.strip("` ")` | off | **NONE** |
| 141 | `S[0-9]{3,}` | →`S[0-9]+` | **NONE** |
| 141 | `len(quotes) != 1` | →`< 1` | **NONE** |
| 146 | quote word bounds | off | **NONE** |
| 146 | `q in seen_quotes` | off | `duplicate_quote_unmet` |
| 155/160 | `len(srow) == 11` | →`>= 11` (both sites) | **NONE** |
| 157 | `u in srow[1]` | any cell | **NONE** (only loosens) |
| 160 | `srow[7] == "mined"` | →`True` | `row_not_mined_unmet` |
| 161 | `srow[8] == OPENED` | →`True` | `row_opened_other_day_unmet` |
| 162 | used-by membership | drop conjunct | `used_by_missing_unmet` |
| 162 | `re.split(r"[,;]")` | →`[;]` | **NONE** (F6) |
| 162 | `u.strip()` | →`u` | **NONE** (F6) |
| 175 | sources floor | `< MIN_SOURCES` → `< 0` | **NONE** (F1) |
| 180 | `has("source")` | drop | **NONE** (redundant with the subset test) |
| 180 | `has("recheck")` | →`True` | **NONE** (F7) |
| 180 | `has("verified-at")` | drop | `verified_at_missing_unmet` |
| 184 | `srows_ok` label | always `"ok"` | **NONE** (F18) |
| 173 | `if missing:` | off | `altered_quote_unmet`,`quote_from_wrong_copy_unmet` |

`--selftest` loads the copies from the working tree (lines 230–235), not from a revision, so the
selftest is green on a dirty tree; `evaluate()` still pins bytes at R.

## 8. Production run (before state)

```
$ cd /home/vgpnk/Projects/shokunin/mori-shokunin
$ TMPDIR=.scratch/r49-Mo49RevC2Counter python3 .ufo/waves/round-49/count-c2.py b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86
C2=unmet claims=0 located=0 quote_missing=0 bad_rows=0 sources=0 source_rows=bad pins=bad provenance=bad rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 failed=entry_absent,pins
exit=1
```

Byte-equal to `evidence/control-c2-donothing.txt` (which also records `exit=1`). The entry does not
exist at the freeze/HEAD, so the "after" predicate is not scoreable from this seat; the counter was
exercised against fixtures built from the four real normalised copies and the real 11-column SOURCES
schema (all 259 registry rows parse to exactly 11 cells; ids S485–S488 are free, max is S484).

## Findings

| # | severity | finding | file:line |
|---|---|---|---|
| F1 | **MED** | The `sources_floor` arm does not isolate its guard. `sources_floor_unmet` (309–312) builds 5 rows (`only2` has 4 + 1 duplicate), so it fails on `claims_floor`, `bad_rows` and `source_rows` simultaneously; the assertion is only `not met`. A guard-removal mutant (`line 175` → `< 0`) keeps **all 26 arms green**, and on a fixture of 8 valid distinct quotes over 2 pages it prints `C2=met claims=8 located=8 … sources=2` (frozen counter prints `C2=unmet … failed=sources_floor`). The receipt's claim that the arm carries this entry-level control with its reason isolated is not true. | `count-c2.py:175`, `309–312` |
| F2 | **MED** | Hidden extra constraint not in P-C2 and not in either entry-scribe dispatch: a claim cell must contain **≥5 whitespace-separated words** (`len(cells[0].split()) < 5`, line 136). A P-C2-conforming terse claim (`retention ceiling is SystemMaxUse`, 4 words) on one row produces `C2=unmet … bad_rows=1 failed=bad_rows,source_rows`; the same row with 6 words is `met`. This can turn an otherwise correct landed entry into `C2=unmet` under the kill rule. | `count-c2.py:136` |
| F3 | **MED** | The entry side has no 4-space rule: `parse_claims` uses `line.lstrip().startswith("\|")` (75), so a claim table written as an indented code block is scored as a table. Measured: all header+rows indented 4 spaces → `C2=met`; only two data rows indented 4 spaces → `C2=met`. Markdown renders those as code, not a table, so `C2=met` can be printed for a document that displays no table. The SOURCES side enforces `^ {0,3}` (94) and the arms pin it (319–322); the entry side has no arm. | `count-c2.py:75`, `81`, `94` |
| F4 | **MED** | `normalise_drops_comment_text` (345) does not exercise line 61: its sample has no inner `>`, so the tag-strip regex removes the comment body on its own. Mutant `comment drop → t` passes 26/26. Where the regex is load-bearing the arm is silent: `normalise("<!-- see <a href=\"x\"> link -->visible")` = ` visible` with the regex, ` link -->visible` without. Unclosed comments and unclosed `<script>` leak their bodies either way (`alpha <!-- hidden remark beta visible`, `alpha var secret=1; beta visible`). No live effect: all four copies contain zero `<!--` and zero unclosed scripts. | `count-c2.py:60–61`, `345` |
| F5 | LOW | Quote word bounds are unpinned between the fixture extremes: `MIN_WORDS` 6→4 or →7 and `MAX_WORDS` 25→24 or →40 all leave 26/26 green (only the 2-word and 26-word fixtures discriminate). | `count-c2.py:34`, `146` |
| F6 | LOW | `used-by` comma-split and strip are load-bearing for real rows (S003 etc. use `", "` lists) but no arm has a multi-entry used-by cell; dropping either the `[,;]` comma or `u.strip()` leaves 26/26 green. | `count-c2.py:162` |
| F7 | LOW | The required `recheck:` key is unpinned: `has("recheck") → True` passes 26/26 (only `verified-at` and `source` are exercised). | `count-c2.py:180` |
| F8 | LOW | The 11-cell SOURCES row and 3-cell entry row exactness are unpinned: `len(srow)==11 → >=11` (155/160) and `len(cells)!=3 → <3` (136) both leave 26/26 green; no fixture has a 12-cell row or a 4-cell entry row. | `count-c2.py:136`, `155`, `160` |
| F9 | LOW | Receipt source matching requires the exact substring `own-work: host-journal-reach` in cell 1 (36–44, 157); the receipt path alone, `host journal reach`, or `own-work host-journal-reach` all give `bad_rows`. P-C2 only says "names its source among the four frozen sources", and the docstring (line 14) says "names its URL" (the receipt key is not a URL). Dispatch item 19 supplies the literal, so the risk is contained but undocumented in the frozen text. | `count-c2.py:14`, `36–44`, `157` |
| F10 | LOW | A quote containing `|` cannot be scored: unescaped it splits the row (`bad_rows`), escaped as `\|` it keeps the backslash and reads `quote_missing`. journalctl's normalised text has 4 visible pipes (e.g. `-u , --unit= UNIT | PATTERN`), so a legitimate synopsis quote is unrepresentable. | `count-c2.py:51`, `144` |
| F11 | LOW | Header must be unformatted: `**claim**`/`` `claim` `` → table not found, `C2=unmet failed=…,table`. P-C2 does not forbid emphasis in header cells; false-red risk for a natural markdown table. | `count-c2.py:83` |
| F12 | LOW | Tag stripping over-eats visible prose containing `<` … `>`: `size < 4G and free > 1G` → `size 1G`. No live case in the four copies (all raw `<` start tags; entities decode after stripping). | `count-c2.py:62` |
| F13 | LOW | `sid = cells[1].strip("` ")` accepts a backticked S-id even though P-C2 says "one S-id"; a leniency with no arm. | `count-c2.py:139` |
| F14 | LOW | `ids_in_table.add(sid)` runs before `row_ok` (150), and `claims = len(rows)` (128) counts rows before validation; diagnostics only (`met` implies `bad_rows=0`), but `claims=N`/`srows_ok` can describe ids/rows already marked bad. Line 79 is dead code (lines 76–77 break first). | `count-c2.py:79`, `128`, `150` |
| F15 | LOW | `--repo`/`--entry` with no value raise `IndexError` (traceback) instead of `C2_SETUP` exit 2. | `count-c2.py:210–213` |
| F16 | LOW | The `--entry` value must equal the `used-by` string byte-for-byte (162), so `./corpus/…` or an absolute path yields `bad_rows`; the contract's command does not use `--entry`, so no live effect. | `count-c2.py:162`, `212` |
| F17 | LOW | `--selftest` loads the four copies from the working tree (230–235), not from the frozen commit, so it can be green while committed bytes differ; `evaluate()`'s digest check still protects the claim. | `count-c2.py:230–235` |
| F18 | LOW | Output fields with no asserting arm: `srows_ok` (`always "ok"` passes), `head` window 14 (`[:40]` passes), and `MIN_SOURCES` is only pinned at its top end (values 1–4 all pass). | `count-c2.py:121`, `184`, `33` |
| F19 | LOW | The whitespace-collapse mutant crashes the selftest (`t.index`/`split` traceback) instead of producing a named `FAIL`; `quote_from`'s `t.index(needle)` would also crash the whole selftest if a needle ever disappears from a copy. | `count-c2.py:64`, `~250` |

No HIGH finding: with the frozen bytes the four pins verify at `HEAD`, `normalise` handles every tag
shape actually present in the copies, and no fixture produced `C2=met` with `quote_missing>0`,
`bad_rows>0`, `pins=bad`, or `provenance=bad`; `met` implies `located == claims` on every path I
exercised.

## Residual risk and verification gaps

- The entry does not exist at the freeze/HEAD; I could not score the real `C2=met` line. Fixtures used
  the four real normalised copies and the real 11-column SOURCES schema, but not the scribes' drafts.
- I did not open the live freedesktop pages; "the copy is the page today" is P-C2's named limit and
  stays a wave-2 question.
- Not exercised: wave-2 attack classes (duplicate SOURCES ids shadowing, tab-indented rows, fenced
  examples inside SOURCES.md), and the `--entry`/`--repo` CLI paths beyond the contract command.
- The mutant battery is in `.scratch/r49-Mo49RevC2Counter/` (48 `m_*.py` files plus
  `m_srcfloor.py`); the 48 full selftest runs took 4.3 s wall in one batch.

## Tooling

No install or upgrade was run (nothing needed). No pacman transaction. Lane tools ran with
`TMPDIR=/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r49-Mo49RevC2Counter`; scratch contains
a symlink `corpus -> /home/vgpnk/Projects/shokunin/mori-shokunin/corpus` so the selftest's
`dirname×3` lane resolution works on mutant copies.
