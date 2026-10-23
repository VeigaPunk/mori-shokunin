# Round 33 wave 2 — attack on source row S189

Seat: MoriR33.AttackSrc189 (leaf, no subagents). Measured revision `62db24c01d5b7c2247f43852ea2b28d0ae5e40c8`.
Attacked: `corpus/SOURCES.md:195` (row S189), `corpus/lessons/round-33.md:24` (Gate row), and the entry row that
cites it, `corpus/knowledge/disk-write-rate-r33.md:28` (row 10). Fetch at measurement time: live. No tool installed or
updated; nothing written outside this report and `/fast/scratch/hyaku/mori-r33/AttackSrc189/`.

## Verdict

Three **minor** findings, no blocker, no major. Every mechanical gate condition I could re-run holds; the defects are
citation-reach defects (an anchor that stops one line short, and a teaches clause the two landed quotes do not state
without the pronoun's antecedent), not false facts.

| id | attacks | defect | severity |
|---|---|---|---|
| F1 | `corpus/SOURCES.md:195` anchor cell | "appended to the stat files" is stated on S189.src:8, which the anchor `patch lines 9-10,14` omits | minor |
| F2 | `corpus/SOURCES.md:195` teaches cell | "its own" and the subject of quote 1 are not stated by either landed Gate quote; they rest on S189.src:7,17 | minor (major if R-R is extended to SOURCES teaches cells) |
| F3 | `corpus/lessons/round-33.md:24` vs `.ufo/waves/round-33/w1/SrcDiscardCommit.md:23` | the seat's 20-word four-stat enumeration quote was dropped; the landed single line 14 states only one of the four | minor |

## Passes (checks run, no defect found)

**P1 — live re-fetch, byte identity (item 1).** HTTP 200, 9,498 bytes:

```
timeout 90 curl -sSL --fail -m 60 'https://github.com/torvalds/linux/commit/bdca3c87fb7ad1cc61d231d37eb0d8f90d001e0c.patch' -o live.src -w 'HTTP=%{http_code} size=%{size_download}\n'
HTTP=200 size=9498
sha256sum live.src
f265ef76e862e4e48cdbdae1b4702cbe47b356501d5d6cbfe9abeaaacd4cf318  live.src
sha256sum corpus/evidence/sources-r33/S189.src
f265ef76e862e4e48cdbdae1b4702cbe47b356501d5d6cbfe9abeaaacd4cf318  corpus/evidence/sources-r33/S189.src
```

Gate sha256 (`corpus/lessons/round-33.md:24`) is `f265ef76…4cf318`: live, Gate and committed copy agree. `wc -l -c`
on the copy: `243 9498`. No retry was needed (no 429). The seat's own two fetches at 2026-10-23T02:40:27Z and mine are
therefore three independent fetches with one digest.

**P2 — quote locators and containment (item 2).** Both quotes sit where the Gate says. `cat -A` on the copy:

```
9  /proc/diskstats.  These are tracked with the same four stats as reads$
10 and writes:$
14 Number of discard sectors completed$
```

- Q1 `S189.src:9-10` (12 words): collapse of lines 9-10 is `/proc/diskstats. These are tracked with the same four
  stats as reads and writes:` — the quote is a substring of that segment (True) and occurs **once** in the
  whitespace-collapsed copy (True). It is not a raw-byte substring only because it crosses the newline, which the
  contract's parity level (`contract.md`, "collapses whitespace runs to one space") permits; the repo's own admitted
  multi-line quotes (e.g. `round-33.md:16` `S181.src:33-34`) are the same shape. Word count 12 = Gate's label.
- Q2 `S189.src:14` (5 words): `Number of discard sectors completed` is an exact raw substring of the copy; word count
  5 = Gate's label; contained once in the collapsed copy.
- No `^M` and no trailing space on lines 9, 10 or 14.
- Counter syntax also matches: `QUOTE_RE` (`count-c1-a1.py:59`) requires `` `file:L-M` (N words): "…" ``; both Gate
  quotes match it, and both are within the 3-25 word window.

**P3 — uniqueness (item 4).** The URL is a 40-hex commit permalink
(`…/commit/bdca3c87fb7ad1cc61d231d37eb0d8f90d001e0c.patch`), so it is commit-pinned, and GitHub's `.patch` view for a
commit is immutable — confirmed by three identical fetches across 17 minutes. Exactly one SOURCES row carries it:

```
grep -c '^| S189 ' corpus/SOURCES.md corpus/lessons/round-33.md   → 1 and 1
grep -c 'f265ef76…4cf318' corpus/lessons/round-33.md              → 1 (11 distinct sha256 for S180-S190)
grep -rn 'bdca3c87fb7ad1cc61d231d37eb0d8f90d001e0c' corpus/ .ufo/waves/round-33/
  corpus/SOURCES.md:1  corpus/lessons/round-33.md:1  corpus/evidence/sources-r33/S189.src:1
  .ufo/waves/round-33/evidence/build_sources.py:1  .ufo/waves/round-33/w1/SrcDiscardCommit.md:8
git show 7d382043…:corpus/SOURCES.md | grep -n 'bdca3c87\|b6866318'  → no match (exit 1), file has 236 lines
```

The SHA appears in no other registry row and not at the entering tip. The other three `torvalds/linux` registry hits
(`SOURCES.md:102,151` = commit 52b1364b for S096/S145; `:194` = S188's different commit b6866318) are different
commits.

**P4 — kind/tier (item 5).** `code` / `A` is right: the row's source is the upstream kernel commit's own patch on
`github.com/torvalds/linux`, i.e. official upstream code, which the assignment's standard and the registry's own
precedent (`SOURCES.md:188,194` — S003/S004/S005/S096/S145/S188 all `code | A`) both give A. The scope cell's "stat
files and /proc/diskstats" is factually correct: the patch extends the sysfs stat printer `part_stat_show` in
`block/partition-generic.c` (`S189.src:190-199`) and `diskstats_show` for `/proc/diskstats` (`S189.src:160-171`), and
the message says so at `S189.src:7-9`. (The tier legend itself is not in SOURCES.md; `corpus/QUALITY.md:53` points at
"contract v1". Not a defect of this row.)

**P5 — entry row 10 mechanics.** I replicated `count-c1-a1.py`'s functions verbatim against row 10
(`disk-write-rate-r33.md:28`, cites S189+S182). `readings_copying_quotes` for row 10: no 6-word run of the reading cell
occurs in any Gate quote of S189 or S182 (`6-gram hits: []`); quote overlap is 6 distinct 4+ letter words (`discard,
four, reads, same, stat_discard, writes`), well over the 2 required; the observation `The discard values on a line` is
distinct from row 11's. Row 10's `STAT_DISCARD` clause is carried by the source it cites, S182:
`S182.src:1403` = `seq_put_decimal_ull(seqf, " ", stat.sectors[STAT_DISCARD]);` (verified by
`grep -n 'stat.sectors\[STAT_DISCARD\]'` → `1403:`), so that clause is not an S189 overreach. Verdict cell "leave
discarded sectors out of a write rate" follows from the reading without a further fact.

## F1 — anchor cell stops one line short (minor)

Attacks `corpus/SOURCES.md:195`, anchor cell: `patch lines 9-10,14 (commit message)`.
The scope cell it anchors says "…its own four statistics, **appended to the stat files** and /proc/diskstats". The words
that state the appending are on line 8, not in the anchor and not in either quote:

```
7 Add tracking of REQ_OP_DISCARD ios to the partition statistics and
8 append them to the various stat files in /sys as well as
9 /proc/diskstats.  These are tracked with the same four stats as reads
```

Anchored line 9 supplies only `/proc/diskstats`; "append", "stat files" and "in /sys" are all on line 8. The fact is
true and present in the committed copy (and in the diff at `S189.src:53` and `:190-199`), so this is locator
incompleteness, not a false claim. Repair: widen the anchor to `patch lines 7-14,17 (commit message)`.

## F2 — teaches cell leans on unquoted lines 7 and 17 (minor; major under R-R)

Attacks `corpus/SOURCES.md:195`, teaches cell: "Discard I/O is tracked with **its own** four statistics of the kinds
kept for reads and writes, including discard sectors completed."

- "four statistics … of the kinds kept for reads and writes" is stated verbatim in Q1 ("the same four stats as reads
  and writes") — supported.
- "including discard sectors completed" is Q2 verbatim — supported.
- "**its own**" (the statistics are discard's separate counters) is stated by neither Q1 nor Q2. It is stated in the
  committed copy at `S189.src:7` ("append them…") and `:17` ("adding a new STAT_DISCARD define"), and demonstrated by
  the hunks (`:210` `STAT_DISCARD,`, `:218-226` `op_is_discard`), but the Gate cites only lines 9-10 and 14.
- The subject is also pronoun-borne: Q1's subject is "These"; the antecedent "REQ_OP_DISCARD ios" is on line 7, outside
  the quote.

Why minor rather than major: no frozen rule binds a SOURCES `teaches` cell this round. R-J (`contract.md:41-47`) binds
the decision table's observation/reading/verdict, and P-C1-A1 tests only that the id has one `mined` row, one admit
Gate row, the URL, the sha256, 1-4 quotes of 3-25 words and a matching copy (`count-c1-a1.py:200-230`); it never reads
the teaches cell. Row 10's parallel clause survives R-J through the union with S182's quote (P5). If the judge extends
R-R (`contract.md:83-88`) to SOURCES teaches cells and treats only the Gate quotes as "quotes", "its own" is
unsupported and this becomes **major**. Repair (same as F3) closes it.

## F3 — the four-stat enumeration was dropped from the Gate quotes (minor)

Attacks `corpus/lessons/round-33.md:24` against what the wave-1 seat actually located,
`.ufo/waves/round-33/w1/SrcDiscardCommit.md:23`: the seat quoted four passages, the first being `` `SRC.src:12-15`
(20 words): "Number of discard ios completed. Number of discard ios merged Number of discard sectors completed
Milliseconds spent on discard requests" ``. The landed Gate row keeps only `9-10` and `14`, so the enumeration and the
ABI note (`S189.src:53`, "Kernel 4.18+ appends four more fields for discard tracking putting the total at 18") are no
longer quoted. Effect: the only landed evidence for "four" in both the teaches cell and row 10's reading is the phrase
"the same four stats", and the only named discard measure is sectors — the count's own list is unquoted.

I checked the obvious repair is free: the dropped quote is 20 words (inside the Gate's 3-25 window), contiguous in the
collapsed copy (`contained: True`), and adds no 6-word overlap with row 10's reading cell (`6-gram hits: []` under the
A1 `reading_copies_quote` rule), so restoring it as a third quote would not push any row into
`corpus/lessons/round-33.md`'s or the counter's failure modes. Recommended: add `` `S189.src:12-15` (20 words):
"Number of discard ios completed. Number of discard ios merged Number of discard sectors completed Milliseconds spent
on discard requests" `` to Gate row 24, which supports both "its own four statistics" (F2) and the scope cell. The
landed narrowing is otherwise unexplained in the lesson: its Gate preamble says only that a non-contiguous seat quote
was replaced (`corpus/lessons/round-33.md:7-9`), and this quote was contiguous.

## Remaining unknowns

- Whether the C1 judge applies R-R to SOURCES `teaches` cells at all. F2's severity hinges on that and nothing in the
  frozen text settles it; my reading of the rule's target ("population page", "the row's own source cell") is that it
  does not, which is why I report minor.
- The line-8-only status of "appended to the stat files" is a locator judgement: a judge reading the committed copy
  (not just the anchor) finds it immediately. I could not test a judge's inclination.
