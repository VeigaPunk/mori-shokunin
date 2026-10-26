# Mo49CritC2Counter — round 49 w1: attack on `count-c2.py` (C2 depth counter)

- Seat: Mo49CritC2Counter (critic, leaf; no subagent, no judge seat, no edit to lane files)
- Instrument: `.ufo/waves/round-49/count-c2.py`, sha256
  `be39475d997f5cf4e67c7d69f66f176b1632985451ed0a6b8a5a4c2a495dd837` — identical to the
  `count-c2.py` line in `evidence/freeze-sha256.txt`, i.e. the bytes I attacked are the frozen ones.
- Revisions: entering `b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86`, freeze
  `0df17b7b4e667dd0aaaef0adc7d7d9973e6aa115`. At the start of this review the tree held no C2 data
  (`corpus/knowledge/journal-reach-r49.md` absent, `corpus/SOURCES.md` clean at HEAD); while I worked,
  another seat wrote the entry (untracked) and modified `SOURCES.md` with S485–S488. I captured the
  in-flight bytes read-only — entry sha256 `6a5c78c05189ba5547c26a37a8da4dbffada7be5fb49470297fdbe451cca7ded`
  (21 table rows), `SOURCES.md` sha256 `2411aa96ec7ff6d5b94fbcf1d391310ead9da2542047d96ad6de3a7f08d40453` —
  and re-scored the junk entry against those real rows (§“In-flight real data”). The file was moving
  while read, so those two digests, not a commit, identify what I scored; I changed neither byte.
- Tooling: nothing installed; `pacman` was not run; python3 stdlib only. Scratch:
  `/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r49-Mo49CritC2Counter/` (untracked), used as
  `TMPDIR` for every run. Read-only git only (`log`, `show`, `ls-tree`, `rev-parse`, `status`); no
  `git add/commit/stash/checkout/reset/pull/push`, no jj command.

## Instrument checks (observed)

```
$ python3 .ufo/waves/round-49/count-c2.py --selftest
C2_SELFTEST pass=26 fail=0                                    [exit 0]
$ python3 .ufo/waves/round-49/count-c2.py b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86
C2=unmet claims=0 located=0 quote_missing=0 bad_rows=0 sources=0 source_rows=bad pins=bad provenance=bad rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 failed=entry_absent,pins   [exit 1]
$ python3 .ufo/waves/round-49/count-c2.py 0df17b7b4e667dd0aaaef0adc7d7d9973e6aa115
C2=unmet claims=0 located=0 quote_missing=0 bad_rows=0 sources=0 source_rows=bad pins=ok provenance=bad rev=0df17b7b4e667dd0aaaef0adc7d7d9973e6aa115 failed=entry_absent   [exit 1]
$ sha256sum corpus/evidence/sources-r49/*
75440570… journalctl.1.html           b4a9b53e… journald.conf.5.html
a7b44356… systemd-journald.service.8.html   be3952cb… host-journal-reach.txt
```

All four working-tree copies match the four frozen digests, so `pins=ok` in the in-memory runs below
is a real statement about the committed copies, not a bypass.

## Method

Harness: `.scratch/r49-Mo49CritC2Counter/attack-c2.py`; raw output
`.scratch/r49-Mo49CritC2Counter/results.txt`. Each case imports the frozen `evaluate()` and passes a
dict-backed `read`: the four frozen copies (working-tree bytes, digests verified), a fabricated
`corpus/SOURCES.md` in the lane's exact 11-column shape (ids S485–S488, `mined`, `2026-10-25`,
`used-by corpus/knowledge/journal-reach-r49.md`), and the candidate entry at
`corpus/knowledge/journal-reach-r49.md`. Scoring therefore follows the same code path as `main()`
(`evaluate(git_reader(...), rev)`), only the bytes are supplied in memory. Every quote below was
checked to be an exact substring of the `normalise()`d copy for the row's S-id (the `words_ok` column
in the harness output); none is an artefact of a failed substring. The junk entry was then re-scored a
second time against the real in-flight `SOURCES.md` and its real S485–S488 rows (same entry bytes, ids
remapped to the rows' actual pages); see §“In-flight real data”.

## Results (observed; `rev=R` is the in-memory revision tag)

| case | junk class under test | result |
|---|---|---|
| A_nav_sliding_windows | breadcrumb/navigation text, 3 sources | **met** `C2=met claims=8 located=8 quote_missing=0 bad_rows=0 sources=3 source_rows=ok pins=ok provenance=ok` |
| B_code_and_license_only | `<pre>` samples, synopsis code paths, `<code>` unit list, license boilerplate | **met** `C2=met claims=8 located=8 … sources=4 source_rows=ok pins=ok provenance=ok` |
| C_host_header_junk | host-receipt comment header, command header + output spans, `[exit 0]` joins | **met** `C2=met claims=8 located=8 … sources=3 source_rows=ok pins=ok provenance=ok` |
| D_vacuous_claim_cells | claim cells with no content (`lorem ipsum dolor sit amet`, `TODO TODO TODO TODO TODO`, `. . . . .`, claim = quote) | **met** `C2=met claims=8 located=8 … sources=3 …` |
| E_element_boundary_spans | quotes joined across heading→body, output→exit→prompt, breadcrumb→synopsis | **met** `C2=met claims=8 located=8 … sources=4 …` |
| K_multi_url_sources_row | SOURCES row whose source cell lists journalctl first and journald.conf second; quote only in journald.conf | **met** `C2=met claims=8 located=8 … sources=3 …` |
| L_bogus_verified_at_recheck | `verified-at: 1999-01-01`, `recheck: never — this field is not read` | **met** `C2=met claims=8 located=8 …` |
| M_empty_scope_anchor_teaches | SOURCES rows `kind=junk tier=Z scope=∅ anchor=∅ teaches=∅` | **met** `C2=met claims=8 located=8 …` |
| N_one_sentence_six_windows | 6 of 8 quotes are one-token-slid windows of **one breadcrumb sentence** | **met** `C2=met claims=8 located=8 … sources=3 …` |
| P_exactly_six_word_quotes | every quote exactly 6 words (the floor) | **met** `C2=met claims=8 located=8 …` |
| Q_source_table_cell_spans | quotes joining `<table>` header and data cells (“Available Disk Space Burst Multiplier <= 1MB 1 <= 16MB”) | **met** `C2=met claims=8 located=8 … sources=4 …` |
| S_midword_fragments | quotes beginning/ending mid-word (`ournald.conf Index · …`) | **met** `C2=met claims=8 located=8 … sources=4 …` |
| T_honest_prose | control: 8 real prose quotes (SystemMaxUse/MaxRetentionSec/journalctl/receipt output) | met `C2=met claims=8 located=8 …` (no general false red) |
| F_pipe_unescaped | quote containing a literal `\|`, written raw in the cell (8-row entry) | **unmet** `C2=unmet claims=8 located=7 quote_missing=0 bad_rows=1 sources=3 source_rows=bad pins=ok provenance=ok` (row splits into 4 cells) |
| G_pipe_escaped | same quote with GFM escape `\\|` | **unmet** `C2=unmet claims=8 located=7 … bad_rows=0 … failed=quote_missing` |
| H/I/J survivors | quote present only in `<script>`, `<script type=application/ld+json>`, `<!-- -->` | **unmet** each: `located=7 quote_missing=1 failed=quote_missing` |
| R_multi_url_named_page_fails | same multi-URL row, quote from the page the row names (journalctl) | **unmet** `failed=quote_missing` |

## The cheapest junk entry that scores `C2=met` (exact bytes)

Built at `.scratch/r49-Mo49CritC2Counter/cheapest-entry.md`, 1198 bytes, sha256
`45732e4422150a1028073710fb4119d06322901691b28866a4028ddd17e47d8c`. Every quote is breadcrumb text;
every claim cell is the same six-word non-claim. Scored:

```
C2=met claims=8 located=8 quote_missing=0 bad_rows=0 sources=3 source_rows=ok pins=ok provenance=ok rev=R
```

```markdown
# Journal reach

source: S485 S486 S487 S488
verified-at: 2026-10-25
recheck: 180d — none

| claim | source | quote |
|---|---|---|
| This row says a located thing. | S485 | `journald.conf Index · Directives systemd 262 Name journald.conf` |
| This row says a located thing. | S485 | `Index · Directives systemd 262 Name journald.conf, journald.conf.d, journald@.conf` |
| This row says a located thing. | S485 | `Directives systemd 262 Name journald.conf, journald.conf.d, journald@.conf — Journal service configuration files` |
| This row says a located thing. | S486 | `systemd-journald.service Index · Directives systemd 262 Name systemd-journald.service,` |
| This row says a located thing. | S486 | `Index · Directives systemd 262 Name systemd-journald.service, systemd-journald.socket,` |
| This row says a located thing. | S486 | `Directives systemd 262 Name systemd-journald.service, systemd-journald.socket, systemd-journald-dev-log.socket,` |
| This row says a located thing. | S487 | `journalctl Index · Directives systemd 262 Name journalctl — Print` |
| This row says a located thing. | S487 | `Index · Directives systemd 262 Name journalctl — Print log entries from` |
```

The only registry work it needs is three rows (S488 is cited but unused; 3 is the floor); exact
fabricated rows used in the score (`sources=3`, `source_rows=ok`):

```markdown
| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S485 | title — https://www.freedesktop.org/software/systemd/man/latest/journald.conf.html | docs | A | journal retention reach | — | — | mined | 2026-10-25 | 180d | corpus/knowledge/journal-reach-r49.md |
| S486 | title — https://www.freedesktop.org/software/systemd/man/latest/systemd-journald.service.html | docs | A | journal retention reach | — | — | mined | 2026-10-25 | 180d | corpus/knowledge/journal-reach-r49.md |
| S487 | title — https://www.freedesktop.org/software/systemd/man/latest/journalctl.html | docs | A | journal retention reach | — | — | mined | 2026-10-25 | 180d | corpus/knowledge/journal-reach-r49.md |
```

`count-c2.py` reads only `srow[1]` (URL substring), `srow[7]` (`mined`), `srow[8]` (`opened`) and
`srow[10]` (`used-by`) — `kind/tier/scope/anchor/teaches/recheck` can be empty or false (case M/L).

## In-flight real data (read-only; identified by digest, not a commit)

At the end of this review the C2 author's data was present in the working tree (entry untracked,
`SOURCES.md` modified): entry sha256
`6a5c78c05189ba5547c26a37a8da4dbffada7be5fb49470297fdbe451cca7ded` (21 table rows at capture; the
file was still growing while read), `SOURCES.md` sha256
`2411aa96ec7ff6d5b94fbcf1d391310ead9da2542047d96ad6de3a7f08d40453` (S485–S488 each 11 cells,
`mined`, `2026-10-25`, `used-by` the entry, exactly one frozen URL per row). Scored through the frozen
`evaluate()` with a dict reader over those bytes:

```
real entry (21 rows)
C2=met claims=21 located=21 quote_missing=0 bad_rows=0 sources=4 source_rows=ok pins=ok provenance=ok rev=WORKTREE   [exit 0]
cheapest junk entry, 8 rows remapped to the real ids (S485 journald.conf, S486 journalctl,
S487 systemd-journald) and scored against the real SOURCES.md
C2=met claims=8 located=8 quote_missing=0 bad_rows=0 sources=3 source_rows=ok pins=ok provenance=ok rev=WORKTREE   [exit 0]
```

Bytes for the second: `.scratch/r49-Mo49CritC2Counter/cheapest-real-registry.md`, 1198 B, sha256
`85b084b65ce8eea3946dbdcdc129f6931217094ccea92e455ba4c3dfed919da8`. The real depth entry and the
breadcrumb-only entry print the same arms on the counter; only `claims` differs. The real rows do not
exercise the multi-URL trap (each names one URL), so finding F3 is latent here, not a defect in this
round's data.

## Junk classes that still score `met` (limits of the instrument)

All of these were scored with the frozen `evaluate()`; the exact row bytes are in
`.scratch/r49-Mo49CritC2Counter/attack-c2.py` (cases A–S) and the raw lines in `results.txt`.

1. **Navigation / breadcrumb / synopsis** (A, N, P). Six of eight rows can be one-token-slid windows of
   one breadcrumb sentence: `journald.conf Index · Directives systemd 262 Name journald.conf,` …
   `262 Name journald.conf, journald.conf.d, journald@.conf — Journal service`. Exactly-6-word quotes
   (`journalctl Index · Directives systemd 262`) meet the floor.
2. **Code samples and example values** (B): `<pre>` text
   `mkdir -p /var/log/journal systemd-tmpfiles --create --prefix /var/log/journal`; the synopsis path
   list `/etc/systemd/journald.conf /run/systemd/journald.conf /usr/local/lib/systemd/journald.conf …`;
   the match-expression sample `_SYSTEMD_UNIT= name .service + UNIT= name .service _PID=1 + …`.
3. **License boilerplate** in the own-work receipt (B):
   `systemd is free software; you can redistribute it and/or modify it`.
4. **Host receipt header/command lines** (C): the capture comment
   `# captured 2026-10-25T20:43:09-03:00 on 7.2.11-arch1-1; no vacuum, rotate or config change was run`,
   the prompt+output join `$ journalctl --disk-usage Archived and active journals take up 56M in the file system.`,
   and the three-line join `56M in the file system. [exit 0] $ journalctl --system --disk-usage`.
5. **Source-page table cells joined** (Q): `Available Disk Space Burst Multiplier <= 1MB 1 <= 16MB` —
   a header row and data rows rendered as one “quote”; as prose it exists nowhere.
6. **Element-boundary joins** (E): `Description ¶ These files configure various parameters of the systemd…`
   (heading markup → paragraph), `Archived and active journals take up 37M in the file system. [exit 0] $ systemd-analyze cat-config`.
7. **Claim cells that say nothing** (D): `lorem ipsum dolor sit amet` (5 tokens is the threshold),
   `TODO TODO TODO TODO TODO`, `. . . . .`, or the quote copied into the claim cell. Eight *identical*
   claim cells pass.
8. **Mid-word fragments** (S): `ournald.conf Index · Directives systemd 262 Nam` — location is a bare
   substring test (`count-c2.py:166`), no word-boundary anchor.
9. **SOURCES provenance looseness** (K, L, M): a row whose source cell lists two of the four URLs is
   credited to the URL that comes first in the counter's own `COPIES` dict, not the row's named page;
   `verified-at`/`recheck` values are never parsed; `kind/tier/scope/anchor/teaches` are never read.

## Round-48 survivors (script / JSON / comment text) now fail — confirmed

The committed copies cannot exercise this directly: each HTML copy contains two **empty**
`<script></script>` tags and **zero** `<!-- -->`. I therefore injected one phrase at a time into a copy
and gave `evaluate(copies=…)` a matching digest so `pins` stayed `ok` (the only difference from the
real copy is the injected block):

- `<script>var note = "nav words are never evidence here";</script>` → `C2=unmet … located=7 quote_missing=1 failed=quote_missing`
- `<script type="application/ld+json">{"about": "retention reach phrase from json payload"}</script>` → same
- `<!-- retention reach phrase from comment block -->` → same

So the round-48 survivor class is closed at the `evaluate()` level, not just in the `normalise()`
selftest arms.

## False reds (honest entry blocked)

1. **A legitimate quote containing a literal `|` cannot be represented.** `journalctl.1.html` has four
   such prose-adjacent spans, e.g. `-u , --unit= UNIT | PATTERN ¶ Show messages for the specified systemd unit`.
   Raw in the cell → the row splits into four cells → `bad_rows=1` (case F). GFM-escaped as `\|` →
   the escape survives `split_cells` and the quote is compared with a backslash in it → `quote_missing=1`
   (case G). The counter never unescapes `\|` (`split_cells` at `count-c2.py:49-56`).
2. **Multi-URL source row is order-dependent.** With `srow[1] = "journalctl(1) — …/journalctl.html ; …/journald.conf.html"`,
   the loop at `count-c2.py:156` picks `journald.conf` because it is first in `COPIES`; a quote from
   journalctl (the page the row names) then fails (`R`: `quote_missing=1`) while a quote from
   journald.conf passes (`K`). The lane's SOURCES convention already lists multiple URLs with `;` (e.g. S476).
3. No other false red was found for ordinary prose: case T (8 honest prose quotes, 4 sources) scores
   `met` with no bad row, and the counter's own honest selftest arm passes.

## What the met evidence means

P-C2's named limit is “a located quote proves the quoted words occur in the committed copy, not that
the claim cell follows from them”. The counterexample shows the limit is larger than that sentence:
the claim cell need not contain a claim at all (5 whitespace tokens suffice), and the located text need
not be prose, need not be sentence- or word-aligned, and may come from breadcrumbs, `<pre>` samples,
table cells, prompt/output joins or license boilerplate. C2 therefore proves *quote location*, not
depth of reading. The entry the contract describes (retention rule, persistent/volatile split, vacuum
order, this host's ceilings) is satisfiable with zero sentences about retention.

## Impacted axes

- **depth** (primary): the axis gain C2 reports is not distinguished from a nav-only entry.
- **calibration**: the quote↔SOURCES-row coupling is weaker than it reads (multi-URL rows, unread
  `scope/anchor/teaches`).
- **operability**: an honest entry is blocked by two representational traps (pipe quotes, multi-URL rows).

## Smallest safe corrections (routed; NOT applied — the kill rule forbids re-scoring round 49)

1. `count-c2.py:56` — unescape GFM cell escapes: `return [p.strip().replace("\\|", "|") for p in parts]`.
   This alone fixes false red 1 and keeps header/`S`-id parsing unchanged.
2. `count-c2.py:156` — resolve the row URL from the row's first `;`-separated segment instead of the
   `COPIES` dict order; if more than one of the four URLs is in that first segment, mark the row bad.
   Fixes false red 2 and the K false green together.
3. To close the demonstrated junk classes without touching honest prose (next round's counter):
   (a) anchor the location test at word boundaries (`(?<!\S)` … `(?!\S)`) — kills S and, combined with
   (b), the breadcrumb/code/table classes; (b) require the matched occurrence to lie outside `<pre>`
   and `<table>` blocks and after the page's first `Description` marker (man pages) or after the first
   `$ ` prompt line (receipt) — kills A/B/C/E/N/P/Q; (c) require the claim cell to be distinct across
   rows and to share at least one ≥6-character token with its quote — kills D and the cheapest entry
   above. These are additive checks on the *next* frozen counter, not on this round's bytes.
4. Optional (LOW): parse `verified-at` as `YYYY-MM-DD` and require a non-empty `scope`, `anchor`,
   `teaches` in the SOURCES row (rejects L/M).

## Findings

- **HIGH — `.ufo/waves/round-49/count-c2.py:136,166` (claim-cell word floor + bare substring location):**
  an 8-row entry whose quotes are page breadcrumbs, claims identical six-word non-claims, scores
  `C2=met claims=8 located=8 … sources=3` (exact bytes above, 1198 bytes) — including when scored
  against the real in-flight S485–S488 rows (`cheapest-real-registry.md`, sha256 `85b084b6…`), where it
  prints the same arms as the author's 21-row entry (`claims=21`). The junk classes A–S all score
  `met`; C2 measures location only, so the depth gain is not measured. Route to wave 2 as a limit; do
  not re-score.
- **MED — `.ufo/waves/round-49/count-c2.py:49-56` (`split_cells`):** a legitimate quote containing `|`
  cannot pass in either form — raw splits the row (`bad_rows=1`), GFM-escaped `\|` fails location
  (`quote_missing=1`). Four such spans exist in `journalctl.1.html`. Fix: unescape `\|` before compare.
- **MED — `.ufo/waves/round-49/count-c2.py:156` (row-URL resolution by `COPIES` order):** a source row
  listing two of the four URLs is credited to the first URL in the counter's dict; text from a page the
  row does not name passes (K), and text from the named page fails (R). Fix: first `;` segment of
  `srow[1]`, else bad row.
- **LOW — `.ufo/waves/round-49/count-c2.py:180`:** `verified-at` and `recheck` are presence-only;
  `verified-at: 1999-01-01` / `recheck: never` score `provenance=ok` (case L).
- **LOW — `.ufo/waves/round-49/count-c2.py:160`:** `kind`, `tier`, `scope`, `anchor`, `teaches`,
  `recheck` of the SOURCES row are never read; placeholder rows (`kind=junk tier=Z scope=∅ anchor=∅
  teaches=∅`) score `source_rows=ok` (case M).
- **LOW — `.ufo/waves/round-49/count-c2.py:166`:** no word-boundary anchor; quotes cut mid-word pass
  (case S, `ournald.conf Index · Directives systemd 262 Nam`).

## Evidence index

- `.scratch/r49-Mo49CritC2Counter/attack-c2.py` — harness (cases A–T plus Z).
- `.scratch/r49-Mo49CritC2Counter/results.txt` — raw case output, one line per case.
- `.scratch/r49-Mo49CritC2Counter/cheapest-entry.md` — exact junk entry bytes (sha256 `45732e44…`, 1198 B).
- `.scratch/r49-Mo49CritC2Counter/cheapest-sources.md` — exact fabricated SOURCES rows used pre-data.
- `.scratch/r49-Mo49CritC2Counter/cheapest-real-registry.md` — same junk entry remapped to the real
  S485–S488 rows (sha256 `85b084b6…`, 1198 B), scored `met` against the in-flight `SOURCES.md`
  (sha256 `2411aa96…`).
- Frozen reads: `count-c2.py` sha256 `be39475d…`; four copies match `evidence/freeze-sha256.txt`;
  real in-flight entry scored at sha256 `6a5c78c0…`.

Report: .ufo/waves/round-49/w1/Mo49CritC2Counter.md
