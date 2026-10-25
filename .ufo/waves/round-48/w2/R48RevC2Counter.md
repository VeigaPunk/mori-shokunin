# R48RevC2Counter — w2 review of frozen `count-c2.py`

**Attacked:** the frozen counter `.ufo/waves/round-48/count-c2.py` (sha256 `0055aed1…`, matches
`evidence/freeze-sha256.txt`) — `normalise()` on the four real copies, `parse_claims`, the
`sources_row` 0–3-space rule, the used-by split, and the 22 selftest arms.
**Verdict: C2 HOLDS at the landed tip** — `C2=met claims=15 located=15` is earned on rendered
body text, not on script/JSON content. The wave-1 finding that script/JSON text scores `met`
is confirmed independently below and remains an open instrument hole (latent harm class:
over-acceptance), plus a family of smaller over-/under-acceptance defects in the table and
cell parsers. No defect found that flips the landed tip's verdict in either direction.

## Observed baseline (command + output + exit)

- `sha256sum .ufo/waves/round-48/count-c2.py` → `0055aed101bd…ae561`, equal to
  `freeze-sha256.txt:2`. Exit 0.
- `TMPDIR=…/r48w2-R48RevC2Counter python3 .ufo/waves/round-48/count-c2.py e4dfff32d…`:
  `C2=met claims=15 located=15 quote_missing=0 bad_rows=0 sources=4 source_rows=ok pins=ok
  provenance=ok rev=e4dfff32d…` — exit 0.
- `… count-c2.py --selftest` → `C2_SELFTEST pass=22 fail=0` — exit 0.
- `harm.py` (scratch): all four pinned copies hash-match their frozen digests at
  `e4dfff32d`; `parse_claims` reads header `['claim','source','quote']`, 15 rows; every
  quote occurs exactly ≥1× in its normalised copy.

## Defects (by severity)

### F1 — HIGH (latent): script/style/JSON-LD element content scores `located`

`normalise()` (lines 59–62) strips tag *syntax* (`re.sub(r"<[^>]+>", " ", text)`, line 60)
but keeps the *contents* of `<script>`, `<style>`, `<noscript>`, `<template>` elements and
HTML comments; `evaluate` then substring-searches the whole normalised copy (line 164
`if q in norm[url]`). Confirmed `w1/CritC2Counter.md` independently with a fresh payload:
8 unique 6-word script-only fragments across S479 (Statcounter/Google-Analytics JS), S480
(same shared man7 script) and S482 (schema.org JSON-LD), junk claim text, valid rows →
`C2=met claims=8 located=8 quote_missing=0 bad_rows=0 sources=3 …` (scratch `attack2.py`
run reproduced in-line; payload strings in transcript below).

**Harm sized for this entry — zero.** Re-normalising each copy after deleting
`<script>/<style>/<noscript>/<template>` element bodies and `<!-- -->` comments leaves
all 15 quotes located (each ≥1 occurrence): rows 1–11 (S479/S480 man pages, 3.9%/7.7%
script content) and row 12 (errno.h, 0%) unaffected; rows 13–15 (S482; the copy is 39.4%
script/comment content — `window.__ICE_PAGE_PROPS__` embeds the whole body as JSON) drop
from 2×/2×/4× loose occurrences to 1×/1×/2× strict, i.e. the JSON duplicates go away but
the rendered-body occurrence remains (raw line 213 for `Disk quota exceeded` sits outside
every `<script>` block, verified by block-map). The defect is therefore exploitable
surface, not the reason this entry passed. Residual entailment risk (claim ⟸ quote)
stays the contract's named limit (contract.md:82–85), and w1 `CritEntryRisk.md` already
routed the six claim/quote pairs for reviewer check — out of counter scope.

### F2 — MODERATE: `sources_row` is fence-blind and table-blind (lines 90–94)

`re.match(r"^ {0,3}\|\s*SID\s*\|", line)` accepts *any* `|`-delimited line, and stops at
the first. Inconsistent with `parse_claims`, which skips fenced regions (lines 68–72).
Demonstrated: (a) unit — `sources_row` returns an 11-cell row for `S999` inside a ```` ``` ````
block; (b) end-to-end — `SOURCES.md` whose only `S479` row sits inside a fence still scores
`C2=met claims=8 located=8` (a reader's ledger contains no S479 row). Also accepts rows of
*other* tables anywhere in the file as long as cell 0 is the S-id, and a duplicate S-id
row earlier in the file shadows the real one (first-match, conservative flip). Not hit by
the landed entry — `corpus/SOURCES.md` at `e4dfff32d` has zero fence markers and no
4-space-indented `|` lines (observed).

### F3 — MODERATE: `parse_claims` recognises non-tables as the claims table (lines 65–87)

The routed "0–3-space rows" rule is enforced for SOURCES rows (line 92) but **not** for the
claims table: `line.lstrip().startswith("|")` (line 73) drops the indent budget. Demonstrated
(`attack2.py`, all with the honest 8-row payload):

- claims table indented 4 spaces — a markdown code block, not a table → `C2=met`
  (asymmetric with selftest arm `code_indented_row_unmet`, which only covers SOURCES rows);
- table with no `|---|` separator at all — not a markdown table → `C2=met`
  (the separator row is only *skipped*, lines 84–85, never required);
- a prose line between header and separator — markdown aborts the table; the counter's
  `continue` at lines 74–75 only fires once `rows` is non-empty → `C2=met`.

Corollary tested and **rejected**: headerless `|` lines after a blank line do *not* merge
into the table — line 74–75 breaks once data rows exist (claims stayed 6 → unmet). And a
second `claim|source|quote` header is swallowed as a `bad` row, so two sub-8 tables cannot
pool — those attacks fail.

### F4 — LOW: quote cell may carry extra prose (line 139)

P-C2: each row's quote cell *is* one backticked span. The check is
`len(SPAN.findall(cells[2])) != 1` — span count only. `` `…` — see also the nav note ``
scores `located` and `met` (demonstrated). Same for a claim cell minimum of 5 words
(line 134) which is a counter-side invention — conservative direction, noted not defected.

### F5 — LOW: `\|` escapes are never undone — quotes containing `|` are unlocatable

`split_cells` (line 51) splits on `(?<!\\)\|` but leaves the backslash in the cell; nothing
unescapes it before the location check (lines 138–142). Demonstrated: a quote ending in
`NAME \|` extracts as `…NAME \|` → `found_in_copy: False`. Real consequence: the man7 nav
bars contain `NAME | SYNOPSIS | DESCRIPTION` in normalised text — no row can quote across
a literal `|`. False-negative (conservative) defect; severity low because the predicate is
satisfiable without such quotes.

### F6 — LOW: `normalise` destroys `<…>` text in non-HTML copies

Line 60 strips `<[^>]+>` unconditionally, so in the plain-text `errno.h` copy
`#include <asm-generic/errno-base.h>` is deleted (observed: `asm-generic/errno-base.h`
absent from `norm`, and `…_H` guard text collapses correctly). Any future quote spanning an
angle-bracket include or comparison in the C source is unlocatable. Same conservative
direction as F5.

### F7 — LOW: front-matter scan is fence-blind and indent-blind (lines 119–121, 175–181)

`has()`/`src_lines` match `^[-* ]*key\s*:` on the first 14 **non-blank** lines — a
4-space-indented (code-block) or fenced `source:` line counts as front matter, and
provenance is satisfiable from inside a fence. Conversely the 14-line window is tight: the
real entry's front matter ends exactly at non-blank line 13 (`coverage-map`), so one more
header line would have pushed `recheck:` out of the window → unmet despite a predicate-conformant
entry. `ids_in_table <= cited` (line 178) is stricter than P-C2 (extra cited sources allowed) —
conservative. Case-sensitivity (`Source:` fails) — conservative.

### F8 — LOW: trailing `--repo`/`--entry` crashes instead of setup exit 2 (lines 208–211)

`args[i + 1]` on a flag-last argv raises `IndexError`, traceback, process exit 1 — outside
the documented `C2_SETUP`/exit-2 contract (line 213). Observed directly.

### F9 — INFO: selftest coverage gaps vs. these defects

22 arms, all passing. All ten contract-named controls are present; the `no_table` arm uses
synthetic text rather than the byte-exact staged entry — I verified the real staged file
(`merge/mori/.../quota-observability-r38.md`, 118 lines) scores
`unmet failed=claims_floor,provenance,source_rows,sources_floor,table` with `parse_claims`
finding no table, so the control's intent holds anyway. Missing arms: F2 (fenced SOURCES
row), F3 (indented/no-separator/interrupted claims table), F4 (span+prose cell), F5/F6
representability — every over-acceptance finding above is arm-free, while the arms that do
exist lean conservative (`code_indented_row_unmet` tests the *other* table).

## What did not survive attack

- Blank-line merge of headerless pipe lines (F3 corollary) — refuted by line 74–75 break.
- Two sub-floor tables pooling rows — refuted (second header becomes a `bad` row).
- Byte-exact staged entry — unmet as required.
- Pin digests, used-by split (`[,;]` + exact path match at line 160 — right for this
  ledger), 11-cell column indices (srow[7]/[8]/[10] = status/opened/used-by, verified
  against real rows 258–261), word bounds 6–25 (row 12 sits exactly at 6 words), and the
  provenance subset rule — all correct on the landed data.

## Residual risk / verification gaps

- `normalise`'s tag stripping can also *eat* copy text containing stray `<…>` outside HTML
  (F6 generalisation); not exhaustively enumerated for all copies.
- Duplicate S-id shadowing (F2, first-match) and URL substring collision
  (`u in srow[1]`, line 155) were reasoned, not demonstrated end-to-end.
- The entailment limit is the contract's own; reviewer coverage of the six risky
  claim/quote pairs is a sibling seat's scope.

Scratch: `.scratch/r48w2-R48RevC2Counter/{harm.py,attack.py,attack2.py}`. No production,
frozen, or sibling file touched; git read-only; TMPDIR confined to scratch.
