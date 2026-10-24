# AttackSrc187 — S187 (Linux /proc/diskstats ABI description v7.2)

Seat: MoriR33.AttackSrc187 (leaf scout, wave 2). Verdict is not counted; this is an attack report.
Lane revision checked: 62db24c01d5b7c2247f43852ea2b28d0ae5e40c8 (S187.src blob at rev = 6a719cf2…, identical to the working tree).

## What I attacked

- `corpus/SOURCES.md:193` — the S187 registry row (scope / anchor / teaches / kind / tier / status / used-by).
- `corpus/lessons/round-33.md:22` — the S187 Gate row (url, accessed, sha256, four quotes with locators and word counts, decision).
- `corpus/evidence/sources-r33/S187.src` — the committed copy (43 lines, 1243 bytes).
- `corpus/knowledge/disk-write-rate-r33.md:26` (entry row 8, the only S187-only row), `:19,:23,:25,:29,:30` (other rows citing S187), `:10` (numbering preamble).

## Checks run and results

**1. Live re-open and three-way hash.** `curl -sSL --fail -m 60 https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/ABI/testing/procfs-diskstats -o live.src` → `exit=0`, `1243` bytes, `43` lines.
`sha256sum live.src` = `0f2ffdc724e0a666c54aa3b1f1e94f93ce6b76745827d301dd164d789bbdd3b7`
= `sha256sum corpus/evidence/sources-r33/S187.src` = the Gate sha256 at `round-33.md:22`.
`cmp committed.src live.src` → `CMP: identical`. No 429, no retry needed. No bytes differ anywhere, so no quote can drift from the copy.

**2. Quotes at their locators.** Script split the copy per line, collapsed whitespace (`re.sub(r'\s+',' ')`) and tested containment inside exactly the stated line range, plus containment in the whole-file collapsed text, plus the claimed word counts:

| Gate locator | claimed words | actual words | in stated range | in whole collapsed copy |
|---|---|---|---|---|
| `S187.src:6-7` | 7 | 7 | yes | yes |
| `S187.src:19-21` | 13 | 13 | yes | yes |
| `S187.src:26-27` | 14 | 14 | yes | yes |
| `S187.src:36` | 9 | 9 | yes | yes |

Locator detail: `6-7` spans "…Each line contains the following 14 / fields:" (line 6 tail, line 7 alone); `19-21` covers the table rows `10 sectors written`, `11 time spent writing (ms)`, `12 I/Os currently in progress`; `26-27` spans "…for discard / tracking putting the total at 18:"; `36` is one whole line. All four are contiguous in the copy, so none repeats the round-33 `SrcSectorSize` split-quote defect.

**3. SOURCES cells vs the anchored lines.** Teaches cell has four clauses and each maps to an anchored quote in the copy that the row's own source cell names (`S187.src`, the URL's file):
- "A line has 14 fields" ← lines 5-7 ("Each line contains the following 14 fields:").
- "field 10 sectors written, 11 time spent writing in ms, 12 I/Os currently in progress" ← lines 19-21 ("(ms)" is the copy's rendering of "in ms"; same fact).
- "4.18+ appends four discard fields for 18" ← lines 26-27.
- "5.5+ appends two flush fields" ← line 36 ("two more fields for flush requests").
No teaches clause needs a page the source cell does not name, no caveat is required, and no clause rides on absence of contradiction — R-R is satisfied as written.
Scope cell ("field numbering and the field counts by kernel version"): numbering is printed 1-14 (lines 10-23), 15-18 (lines 30-33), 19-20 (lines 39-40); counts printed as 14 and 18. The 5.5+ *total* is never printed (see F2). The scope cell claims only "field counts by kernel version", which the 14/18 statements carry; the teaches cell wisely does not claim 20, so nothing overreaches. Severity of this item: none.
Anchor cell (`Documentation/ABI/testing/procfs-diskstats:6-7,19-21,26-27,36; tag v7.2`): path matches the tree path in the URL; the four ranges are exactly the four quotes' ranges, so every teaches clause has an anchor and no anchor is unused.

**4. Pinning and duplication.** `git show`/API: `https://api.github.com/repos/torvalds/linux/git/ref/tags/v7.2` → `"ref": "refs/tags/v7.2"`, `"object": {"sha": "237a1c39…", "type": "tag"}` — a real tag object, not a branch, so the bytes are immutable and "on-release" recheck is meaningful.
`grep -n -F '<url>' corpus/SOURCES.md` → one hit, line 193. `grep -n -i 'diskstats' corpus/SOURCES.md` → S033 (`docs.kernel.org/admin-guide/iostats.html`), S181, S182, S187, S189; only S187 carries this URL, and no row carries the rendered `docs.kernel.org` form of this ABI page. No duplicate.

**5. Kind / tier / bookkeeping.** `Documentation/ABI/testing/procfs-diskstats` is upstream kernel-tree documentation at a release tag → kind `docs`, tier A: correct, and consistent with sibling rows S180/S181.
Gate decision `admit, A, mined` matches the registry (tier A, status `mined`); `opened 2026-10-23` matches the Gate accessed stamp `2026-10-23T02:46:06Z` and `/fast/scratch/hyaku/mori-r33/L1/src/procfs-diskstats.accessed` (`2026-10-23T02:46:06Z`); `used-by corpus/knowledge/disk-write-rate-r33.md` exists and cites S187 at lines 10, 19, 23, 25, 26, 29.
Timestamp sanity: copy mtime `2026-10-22 23:51:27 -0300` = `02:51:27Z`, i.e. after the recorded access (host TZ is -03:00), so no "copy predates its fetch" anomaly.
Double fetch: the L1 kept two copies, `L1/src/procfs-diskstats.src` and `L1/src/procfs-diskstats.2.src`, both `0f2ffdc7…`, so the lesson's sentence "every seat fetched twice and both sha256 values matched" (`round-33.md:8`) holds for S187, which the L1 opened itself (`round-33.md:7`, `build_sources.py:73`).
Wave-1 coverage: `grep -rl 'S187' .ufo/waves/round-33/w1/` → no file; no wave-1 report asserts anything about S187, consistent with `round-33.md:7` ("S187 by the L1"). Nothing in wave 1 about this row needs falsifying.
Draft-vs-shipped: `/fast/scratch/hyaku/mori-r33/L1/sand/SOURCES.md:193` shows an earlier S187 row with anchor `…:6-7,19,26-27,36` and teaches "(field 10 sectors written)" only. The shipped row tightened the anchor to `19-21` and added fields 11-12. The shipped row is strictly better supported than the draft; no defect.

**6. Host corroboration (context only, not needed for R-J).** `awk '/ (nvme0n1|sda) /{print $3, NF}' /proc/diskstats` → `nvme0n1 20`, `sda 20`; first line `259 0 nvme0n1 20`. A 7.2 host prints exactly 20 values, matching the 14→18→20 chain of the copy.

## Findings

**F1 — major (R-J support risk), entry row 8's observation cell.**
Attacks `corpus/knowledge/disk-write-rate-r33.md:26`, observation cell: "The number of whitespace-separated values on a `/proc/diskstats` line". Row 8 cites S187 alone. Evidence: `grep -n -i -E 'whitespace|separat|space|tab' corpus/evidence/sources-r33/S187.src` → no output (exit 1), and none of the four Gate quotes (`round-33.md:22`) contains such a word; the ABI copy says only "Each line contains the following 14 fields:" (lines 6-7) and lays the fields out in an asciidoc table, never stating the on-disk separator. Under R-J's letter the quotes must state *every* fact the observation cell asserts, and whitespace separation is one. The entry itself shows the contrast: row 12 (`:30`) makes the same kind of claim but cites S180, whose Gate quote does say "…17 decimal values separated by whitespace". Cheapest fix that harms nothing: reword the observation to "The number of fields on a `/proc/diskstats` line". (Citing S182 would not close it cleanly: its quote set, `round-33.md:22`, shows `seq_put_decimal_ull(seqf, " ", …)` separators for two fields only, not a statement about the whole line.)

**F2 — minor (R-J caveat risk), entry row 8's verdict cell.**
Attacks `disk-write-rate-r33.md:26`, verdict: "Accept a line of 14, 18 or 20 fields…". The copy prints 14 (line 6-7), 18 (lines 26-27) and "two more fields" (line 36), but never prints 20; 20 exists only as 18+2. A judge reading "without any further fact" strictly could caveat the verdict, and the reading cell never states 20 either. This is arithmetic, not an outside fact, so I rate it minor; if L1 wants zero exposure, have the reading say "…add two flush fields after those, for 20 in all", making the number explicit in the reading the verdict follows from. The same arithmetic underlies the SOURCES scope cell's "field counts by kernel version", but the teaches cell never claims 20, so no R-R exposure there (severity none).

## Not a defect (attacked and held)

- All four SOURCES teaches clauses are stated by quotes in the named page's committed copy; no caveat, no absence-of-contradiction, no unnamed page (R-R met).
- Gate quotes, locators, word counts and sha256 are exact; live bytes equal committed bytes.
- URL is tag-pinned (`v7.2`, tag object) and unique in the registry; kind `docs`, tier A are correct; status/decision/date/used-by are internally consistent.
- Rows 1, 5, 7, 11 use S187 only for the field identity ("Field 10 … sectors written", "Field 12 … I/Os currently in progress", "Field 11 … time spent writing in milliseconds", flush fields 19-20), all stated at lines 19-21 and 36; their remaining reading facts come from sources they also cite (S180, S182, S188, S186).
- Numbering preamble `disk-write-rate-r33.md:10` ("iostats.rst … its field 9 is the ABI file's field 12") is correct: `S181.src:70` reads "Field  9 -- # of I/Os currently in progress", and S187 line 21 puts I/Os currently in progress at field 12.
- A1's quote-copy clause, S187's side only: no 6-consecutive-word run is shared between any S187 Gate quote and the reading cell of rows 1, 5, 7, 8, 11 (script over normalized words, `[A-Za-z0-9_]+`).

## Unrun / limits

- I did not score C1 or run `count-c1-a1.py` (judge's job, explicitly out of scope for this seat).
- I did not re-open the other ten sources; S188/S189/S190 and the code sources were outside this ticket.
- No tool installed or updated. No pacman call. No process left running (the one backgrounded grep, `bg_2950`, was cancelled before return). Scratch: `/fast/scratch/hyaku/mori-r33/AttackSrc187/`.

## Net

S187's own row (SOURCES:193 + Gate:22 + copy) is clean: hash, quotes, locators, word counts, pinning, uniqueness, kind/tier and R-R all hold. The only defect I can substantiate against the row's consumers is F1 on entry row 8 (unsupported "whitespace-separated"), with F2 a smaller arithmetic caveat risk in the same row.
