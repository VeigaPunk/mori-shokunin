# AttackSrc181 — source row S181 (falsification seat, wave 2)

Seat MoriR33.AttackSrc181. Target: SOURCES row `corpus/SOURCES.md:187`, Gate row `corpus/lessons/round-33.md:16`,
committed copy `corpus/evidence/sources-r33/S181.src`, URL
`https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/admin-guide/iostats.rst`.
Measurement revision 62db24c01d5b7c2247f43852ea2b28d0ae5e40c8. Read-only on the lane (git `show`/`grep` only);
scratch under `/fast/scratch/hyaku/mori-r33/AttackSrc181/`. No tool installed or updated this seat.

## Verdict summary

| check | result | severity |
|---|---|---|
| live re-fetch hash vs Gate vs committed copy | identical, byte-stable | none |
| 4 Gate quotes at stated locators, contiguous, word counts | all pass | none |
| URL tag-pinned, unique vs entering tip and other new ids | pass | none |
| kind/tier `docs`/`A` | consistent with registry usage | none |
| scope cell `field 10 (io_ticks)` | term absent from the source | **minor** |
| anchor cell does not carry the referent of quote 3 (line 76) | anchor incompleteness | **minor** |
| title parenthetical "tag-pinned source of the docs.kernel.org page in S033" | page renders 7.3.0, not v7.2 | **minor** |
| teaches cell, all four clauses | supported verbatim | none |

No blocker found against R-J or against P-C1-A1's per-id conditions for S181. Three minor defects are named below
with the cheap repair for each.

## 1. Live re-open, hashes

```
curl -sSL --fail -m 60 <url> -o live.src   ->  HTTP:200 SIZE:8592 URL:.../v7.2/Documentation/admin-guide/iostats.rst
sha256sum live.src                          ->  166bdc8fd4ee9e53bcb86804e0d22d50c89314dcfc1a248814b0069300034124
sha256sum corpus/evidence/sources-r33/S181.src -> 166bdc8fd4ee9e53bcb86804e0d22d50c89314dcfc1a248814b0069300034124
Gate sha256 (round-33.md:16)                ->  166bdc8fd4ee9e53bcb86804e0d22d50c89314dcfc1a248814b0069300034124
```

All three agree; the copy is 187 lines / 8592 bytes and byte-identical to the live fetch on 2026-10-23. No retry was
needed (no HTTP 429).

## 2. Gate quotes vs locators and vs the collapsed copy

Every quote printed from the committed copy at its stated `file:L-M`:

```
sed -n '22p'    -> Both files contain the same 17 statistics. ``/sys/block/<device>/stat``
sed -n '33,36p' -> All fields are cumulative, monotonic counters, except for field 9, which
                   resets to zero as I/Os complete. The remaining fields reset at boot, on
                   device reattachment or reinitialization, or when the underlying counter
                   overflows. Applications reading these counters should detect and handle
sed -n '76p'    ->     This field increases so long as field 9 is nonzero.
```

Whitespace-collapsed containment (`tr -s '[:space:]' ' '` then `grep -qF`): all four quotes CONTAINED.
Stated word counts verified by hand against the quotes: 17 / 17 / 10 / 7 — all correct, all within 3–25.
The counter's `QUOTE_RE` (`count-c1-a1.py:59`) accepts the `` `S181.src:33-34` (17 words): "..." `` form, the Gate
row carries exactly 4 quotes, and the row's URL sits in SOURCES cell 1, so the Gate row parses as the counter
expects.

## 3. Minor — scope cell names `io_ticks`, which the source never writes

`corpus/SOURCES.md:187` scope: "the v7.2 iostats field semantics: which fields are cumulative, when they reset,
**field 10 (io_ticks)**, and the sysfs/procfs equivalence".

```
grep -n -i 'io_ticks\|io ticks' corpus/evidence/sources-r33/S181.src   -> ABSENT (no match)
sed -n '75p' S181.src -> Field 10 -- # of milliseconds spent doing I/Os (unsigned int)
```

The committed copy calls field 10 "milliseconds spent doing I/Os"; the identifier `io_ticks` appears only in the
code sources S182 (`S182.src:1395` `jiffies_to_msecs(stat.io_ticks)`) and S184 (`S184.src:1067-1068`). The scope
cell therefore credits S181 with a term and an identity (field 10 = io_ticks) that no line of S181 states — a
clause the quotes and the anchored lines do not support. Repair: drop `(io_ticks)` from the scope cell, or write
"field 10 (the millisecond I/O-time counter, `io_ticks` in the code sources S182/S184)".

## 4. Minor — quote 3's referent sits outside the anchor cell

Anchor cell: `Documentation/admin-guide/iostats.rst:22,33-36,76; tag v7.2`. Quote 3 is line 76, which says
"This field …" without naming the field; the referent is fixed only by the block header at line 75
("Field 10 -- # of milliseconds spent doing I/Os"). Both lines are in the committed copy, so the teaches clause
"field 10 grows while field 9 is nonzero" is stated by the copy and the row survives R-J as written; but a judge
reading R-J as "the quotes alone state every fact" cannot name the field from the quote at 76. Repair: widen the
anchor to `75-76` (or quote line 75 as well). Note the counter does not validate locator accuracy
(`count-c1-a1.py` only checks collapsed containment), so this is judge-exposed, not counter-exposed.

## 5. Minor — title parenthetical about S033 is loose

`corpus/SOURCES.md:187` title: "… documentation v7.2 (tag-pinned source of the docs.kernel.org page in S033)".

```
curl -sSL https://docs.kernel.org/admin-guide/iostats.html  -> HTTP:200 SIZE:21784
<p class="blurb">7.3.0</p>   (page header; page text also carries "development" markers)
```

The live page S033 points at renders 7.3.0 (mainline/development tree), so the v7.2 tag is not the source of that
page. Substance is unaffected: the docs.kernel.org body contains all four Gate quotes verbatim, so no teaches or
observation fact changes, and the row is not a duplicate under P-C1 (different URL). Repair: "tag-pinned
counterpart of the docs.kernel.org page in S033".

## 6. Passed checks (with the commands that ran)

- **URL pinning and uniqueness.** Path is `/v7.2/` (tag, not branch/HEAD). `grep -n -F '<url>' corpus/SOURCES.md`
  → only line 187. `git show 7d382043…:corpus/SOURCES.md | grep -F '<url>'` → no match (exit 1), so the URL was not
  registered at the entering tip. `grep -c '^| S181 ' corpus/SOURCES.md` at the measurement rev → 1 row.
- **Gate row well-formedness.** `grep -c '^| S181 |' corpus/lessons/round-33.md` → 1 admit row, decision
  "admit, A, mined", accessed `2026-10-23T02:40:16Z`, matching the SOURCES date 2026-10-23 and status `mined`.
  The 11 Gate rows carry 11 distinct sha256 values (each `uniq -c` count 1), so S181's hash is not shared.
- **kind / tier.** `docs` / `A`: the file is upstream kernel documentation in the torvalds/linux tree at release
  tag v7.2, served from the official mirror — the same treatment the registry gives S033 (`docs`/`A`) and S180
  (`docs`/`A`), while kernel C files are rowed `code`/`A` (S182–S186). No contradicting tier legend exists in
  `corpus/README.md`, `PROVINCE.md` or `SKILL.md` (greps returned nothing); the registry's own `C` rows (S063,
  S107) are tertiary/rejected sources, unlike this one.
- **teaches cell, clause by clause.** (1) "All fields except field 9 are cumulative monotonic counters" — line
  33-34 verbatim; (2) "they reset at boot, on device reattachment or reinitialisation, or on counter overflow" —
  lines 34-36 ("The remaining fields … when the underlying counter overflows"); (3) "field 10 grows while field 9
  is nonzero" — line 76 under header 75; (4) "/proc/diskstats and /sys/block/<dev>/stat carry the same 17
  statistics" — line 22, with the two file names fixed at lines 5-6 and 22-23. No clause overreaches. Only
  cosmetic deltas: the cell's "reinitialisation"/"<dev>" vs the source's "reinitialization"/"<device>".
- **used-by cell.** `corpus/knowledge/disk-write-rate-r33.md` cites S181 in rows 4, 6, 12, 13, 14
  (`grep -n 'S181' …` → 6 hits incl. row 4's sources cell), so the cell is accurate. Rows 4, 12, 13 assert only
  facts the S181 quotes state verbatim, so they are not exposed through S181.

## 7. Adjacent exposure, not this seat's row (evidence only)

`corpus/knowledge/disk-write-rate-r33.md:24` (entry row 6) observation cell: "The io_ticks value of a line
(iostats.rst field 10)". The identity "iostats.rst field 10 = io_ticks" is stated by no quote in the copies it
cites: S181 never writes `io_ticks`; S182's quoted line 1395 shows `stat.io_ticks` being printed but its position
(10th) is only visible by counting the preceding `seq_put_decimal_ull` calls (`S182.src:1381-1395`); S184's quote
has no "field 10". [INFERENCE] Under R-J a judge can call that clause unsupported for lack of a quote. Flagged
for the row-6 seat; S181's own row cannot fix it beyond the scope-cell repair in §3.

## 8. Unknowns / not checked

- Whether docs.kernel.org served a v7.2 tree when S033 was opened (2026-10-19): only the live 2026-10-23 render
  (7.3.0) was observed; S033's anchor names docs commit c03c1a14507dfaf8b856c2608f9ac216021fc222, which was not
  re-opened here.
- Locator accuracy is invisible to `count-c1-a1.py`; this seat verified S181's four locators by hand only.
- No sandbox clone was made and no sandbox git was run: the lane reads needed (`git show`, `git log` not used) were
  read-only and sufficed.
