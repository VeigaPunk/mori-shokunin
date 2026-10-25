# CritV2Junk — wave w2 falsification report (round 47)

Seat: CritV2Junk (leaf, no subagents). Target: the **v2** standing tool
`tools/mori-pin-check.py` at the landed tip **T = `68d66ca53d89be5c34a62f46af7c37449d9f9b63`**
(working-tree bytes == T blob, sha256 `9832e38c3863ba82f7a740921e8c9d23d6cf2e702c2bb62ee2ad71fcc21bc2b6`;
the frozen v1 claim bytes `e3ef425a…` are the C1 score instrument, not this seat's target).

Attack surface: NEW junk edits **not** in `.ufo/waves/round-47/controls/c1-junk/`
(which cover: old/`.scratch/`/inline-`-c` bindings, weakened pins, prefix rename, row delete,
entry-cell rebind, lowercase-`selftest` hide + duplicate). All measurements below use the T
measure with `--rev 68d66ca… --min-tally-pins 26 --baseline-rev 2d85e33… --skill <scratch SKILL.md>`.

- Measured-tree base: byte-exact `SKILL.md` at T (939 lines) via `git archive` into
  `.scratch/r47w2-CritV2Junk/tree/`; each variant = base + one edit (diffs below).
- Scratch: `.scratch/r47w2-CritV2Junk/` (variants/ + results/). TMPDIR inside this scratch.
- Baseline (pristine T, exit 0):
  `PIN_CHECK=met tally_pins=28 digest_pins=5 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 min_tally_pins=26 rev=68d66ca… baseline=yes`

## Verdict: **HOLDS with five new false-green classes** (all `PIN_CHECK=met`, exit 0)

---

## FG1 — a gate table whose header cell reads `selftest` (no hyphen) is invisible; its corrupt pins pass

Exact edit (one table, lines 936–939 at T):
- `SKILL.md:936` header cell `self-test` → `selftest` (`| name | kind | entry | verdict map | selftest | pinned values | write scope | owner |`).
- `SKILL.md:938` pin `PIN_CHECK_SELFTEST pass=34 fail=0` → `PIN_CHECK_SELFTEST pass=1 fail=0`.
- `SKILL.md:939` pin `C2_SELFTEST pass=13 fail=0` → `C2_SELFTEST pass=1 fail=0`.

Command + result:
```
python3 tools/mori-pin-check.py --rev 68d66ca53d89be5c34a62f46af7c37449d9f9b63 --min-tally-pins 26 --baseline-rev 2d85e33d14198d388fd3cda9cc15ec07e57e7a53 --skill .scratch/r47w2-CritV2Junk/variants/v1-header-selftest-corrupt-pins.md
PIN_CHECK=met tally_pins=26 digest_pins=5 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 min_tally_pins=26 …
exit=0
```
Why it evades: `parse_registry` only recognizes a table whose header has a cell whose
lowercased text is exactly `self-test`. `selftest` (the word the rest of the registry uses
everywhere else) is not recognized, so rows 938–939 are never parsed: their pins are neither
counted nor checked, and — because rows 938–939 do not exist at baseline E — the `dropped`
guard is not triggered. The two visibly false `pass=1` claims sail through while the round‑47
floor is still met (28 − 2 = 26). The same table's honest pins were checked and matched in
variant v6 (below), proving the only thing standing between the corrupt pins and a red result
is the header spelling.

Note this is exactly the ``-47 section (two new rows with no baseline obligation); hiding a
table whose rows DO have baseline keys fails via `dropped` (see N2).

## FG2 — Unicode homoglyph tally prefix on a parsed new row is silently ignored (fullwidth underscore)

Exact edit (append row after line 939, inside the Round47 table):
```
| r47 pin reconciler — fullwidth | gate | `python3 tools/mori-pin-check.py <rev>` | 0/1/2 | `python3 tools/mori-pin-check.py --selftest` → `PIN_CHECK＿SELFTEST pass=999 fail=0` | none | none | mori |
```
(the prefix uses U+FF3F FULLWIDTH LOW LINE, not ASCII `_`).

```
PIN_CHECK=met tally_pins=28 digest_pins=5 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 …
exit=0
```
Why it evades: tally-pin recognition is `re.match(r"([A-Z][A-Z0-9_]*SELFTEST)(.*)$", span)`.
The fullwidth underscore is outside `[A-Z0-9_]`, so the span is neither a tally pin nor an
executable command; the row parses `ok` and contributes nothing. A manifestly false `pass=999`
claim is never seen. ASCII control (same row, ASCII prefix) is **red**:
```
pin line=940 kind=tally prefix=PIN_CHECK_SELFTEST state=mismatch pinned='pass=999 fail=0' observed='pass=34 fail=0' rc=0 …
PIN_CHECK=unmet … mismatches=1 … exit=1
```
so the homoglyph is precisely what flips red → green.

## FG3 — Unicode homoglyph tally prefix, Cyrillic «Е» (same class)

Exact edit:
```
| r47 pin reconciler — cyrillic | gate | `python3 tools/mori-pin-check.py <rev>` | 0/1/2 | `python3 tools/mori-pin-check.py --selftest` → `PIN_CHECK_SЕLFTEST pass=999 fail=0` | none | none | mori |
```
(U+0415 CYRILLIC CAPITAL LETTER IE inside `SELFTEST`.)
```
PIN_CHECK=met tally_pins=28 … exit=0
```
Same mechanism as FG2. Any non-ASCII confusable inside the prefix defeats the parser without
any `unparsed`/`no_command`/`mismatch` signal.

## FG4 — brand-new row pinning a stale tally bound to a committed *archived* tool copy

Exact edit (append row after line 939):
```
| SOURCES append-only timing (r38) — gate-v2 extract | gate | `python3 .ufo/waves/round-40/fixtures/extracted/gate-v2-bb1f2457.py <rev> --round-base REV` | summary exit as before | `python3 .ufo/waves/round-40/fixtures/extracted/gate-v2-bb1f2457.py --selftest` → `MORI_SOURCES_APPENDONLY_SELFTEST pass=12 fail=0` | none | none | mori |
```
Ground truth: `.ufo/waves/round-40/fixtures/extracted/gate-v2-bb1f2457.py` is an **archived
earlier copy** of `mori-sources-appendonly.py` (its own docstring says so) and prints
`MORI_SOURCES_APPENDONLY_SELFTEST pass=12 fail=0` rc 0, while the live
`tools/mori-sources-appendonly.py` prints `pass=22 fail=0` (both measured directly).
```
pin line=940 kind=tally prefix=MORI_SOURCES_APPENDONLY_SELFTEST state=match pinned='pass=12 fail=0' observed='pass=12 fail=0' rc=0 cmd='python3 .ufo/waves/round-40/fixtures/extracted/gate-v2-bb1f2457.py --selftest'
PIN_CHECK=met tally_pins=29 digest_pins=5 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 … exit=0
```
Why it evades: the baseline guard keys on `(row name, prefix)` from E. A brand-new row name
has no baseline obligation, so nothing compares its binding against the live instrument; the
check verifies only that the named committed bytes print the pinned text. The round-47 C1
motivation (the r38 stale `pass=15` incident) was exactly this shape: a stale tally left in the
registry while the tool's arms grew. A new row can re-create the stale‑claim class by naming an
archived copy of the same instrument, and v2 reports `met`.

## FG5 — fenced replacement elides the two new Round47 pins (verification elision)

Exact edit: replace lines 938–939 with
```
```markdown
| registry pin reconciler (r47, C1) | … | `python3 tools/mori-pin-check.py --selftest` → `PIN_CHECK_SELFTEST pass=34 fail=0` | …
| r47 tracepoint catalogue (C2) | … | `python3 .ufo/waves/round-47/count-c2.py --selftest` → `C2_SELFTEST pass=13 fail=0` | …
```
```
```
PIN_CHECK=met tally_pins=26 … exit=0
```
Fenced tables are documented as ignored, and a fence block may contain any gate-looking table,
including a corrupt one, with zero accounting: the two real pins vanish from the tally (still
≥ 26 floor), and if the fenced rows instead carried corrupt pins they would be invisible exactly
like FG1 (FG1 is the corrupt-pair variant of this channel). Combined with FG1 this reads: any
2 of the 28 pins can be silently removed from verification (or replaced by unchecked junk) while
the verdict stays green, because the floor is 26.

---

## Negative controls (the tool correctly goes red — evidence the above are the only escape channels)

- **N1 (visible corrupt pin):** only `SKILL.md:938` pin → `pass=1` (header untouched).
  `pin line=938 … state=mismatch pinned='pass=1 fail=0' observed='pass=34 fail=0' rc=0` →
  `PIN_CHECK=unmet … mismatches=1`, exit 1. The tool catches a corrupt pin the moment it can see it.
- **N2 (table-termination hiding of baseline-keyed rows):** prose line inserted before row 911,
  row 912's pin changed to stale `pass=15`. The hidden rows *do* exist at baseline E →
  `pin kind=baseline state=dropped row='SOURCES append-only timing (r38)' pin=MORI_SOURCES_APPENDONLY_SELFTEST count=1` (and `CONFORM_SELFTEST`),
  `PIN_CHECK=unmet … dropped=2`, exit 1. The baseline guard covers every key present at E;
  hiding only breaks new-key rows (938–939) — which is why FG1/FG5 target exactly those.
- **N3 (trailing escaped pipe):** row 912's closing `|` → `\|`. Still `PIN_CHECK=met … tally_pins=28 …`,
  exit 0 — `split_cells` keeps cell count intact; the edit is benign (no parsing shift, no pin loss).
  No false green; recorded as attempted per the seat brief.
- **N4 (ASCII lookalike control):** see FG2 — red as expected.

## Observations

- **O1:** a blank line inserted between a table's header and its first data row silently drops that
  row (and any following rows until the next header) from scrutiny with no counter. Found while
  crafting the new-row variants (my first V4 append landed after a blank line; the new pin was
  not counted, tally stayed 28, verdict still `met`). Same family as FG1/FG5: structural
  separation is never accounted for.
- **O2:** "change the pinned text and the tool bytes together" is not reproducible at a fixed
  measured revision: with `--rev` the measured tree is a read-only `git archive` export and the
  tool bytes are immutable (only `--skill` is replaceable). The closest realizability is FG4 —
  pairing a new-but-text with a committed path that prints it.

## Impacted axes

- **calibration (C1)** — primary: P-C1's `PIN_CHECK=met` is produced by registries whose gate
  tables are invisible (header spelling), whose pins are unreadable (homoglyph), whose verified
  content is elided (fence/blank/termination), or whose new rows canonize archived stale
  instruments — the round's own motivating defect class.
- Adjacent (not scored here): operability/freshness of the registry (a stale tally presented as
  current is an observability lie), but no other claim in this round is re-scored.

## Smallest safe corrections

1. **Header detection:** accept both `self-test` and `selftest` (case-insensitive) as the
   self-test header cell; or detect gate tables structurally and flag any unrecognized
   header spelling containing `selftest`/`self-test`/`self test` as `unparsed` (table-level).
2. **ASCII-strict tally pin:** require the span to be ASCII before prefix matching, and count a
   non-ASCII span inside a self-test cell as `unparsed` instead of ignoring it (kills FG2/FG3).
3. **Baseline guard by instrument, not just row name:** record baseline binding multiset by
   `(prefix, argv)`; a new row that binds an existing instrument's prefix to an argv not seen
   at baseline (e.g. an archived copy) is `rebound` unless the instrument is genuinely new
   (kills FG4).
4. **Account for visibility elision:** count any unrecognized self-test-like table, fenced
   gate-table block, blank-line-separated row, and terminated-table tail as `unparsed` (or add
   a `hidden=` counter and make it fatal). This closes FG1/FG5/O1 and prevents silent
   verification reduction below the floor's intent.

## Evidence

- Scratch: `.scratch/r47w2-CritV2Junk/` — `variants/v1…v10.md`, `results/v1…v10.txt`
  (full command + pin lines + verdict line per variant), `tree/` (T export), `gen_variants.py`.
- Tool bytes: `tools/mori-pin-check.py` sha256 `9832e38c…` (== T blob; freeze F v1 =
  `e3ef425a…`).
- Archived printer ground truth: `.ufo/waves/round-40/fixtures/extracted/gate-v2-bb1f2457.py
  --selftest` → `MORI_SOURCES_APPENDONLY_SELFTEST pass=12 fail=0` rc 0; live
  `tools/mori-sources-appendonly.py <T> --selftest` → `pass=22 fail=0` rc 0.
- Baseline E has 912 lines and no `PIN_CHECK_SELFTEST`/`C2_SELFTEST pass=13` rows (so rows
  938–939 carry no baseline obligation; verified via `git show 2d85e33:SKILL.md`).
