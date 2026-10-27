# Mo56LabCensusSpace — the census parser's 0–3 leading-space rule, probed

Seat: Mo56LabCensusSpace · lane mori-shokunin · round 56 wave w1 · 2026-10-27
Role: detection and report only. No counter, predicate, control or kill rule is
proposed for change; every weakness below is a **named limit + a routed item for
round 57**, not a fix.

## Scope actually executed

The assignment named one experiment: copy `corpus/SOURCES.md` into scratch, append
one row with **two leading spaces** whose id collides with a staged shokuknow id
(**S471**, from `/home/vgpnk/Projects/shokuknow/merge/mori/SOURCES.append.md`), run
`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file <copy>`,
show the collision/malformed behaviour, then append the same row at column zero and
diff the validator output. Then: report whether the 0–3-space pattern matters for
mori's registry hygiene under the assimilation contract's collision check.

Everything below was produced by running the real census script against a mirror of
the freeze-tip lane tree; no repo in `/home/vgpnk/Projects/shokunin` was written.

## Fixture construction (and one correction to the assignment's recipe)

The assignment says to copy `corpus/SOURCES.md` into scratch and validate `--file`
that copy. **Taken literally this does not work**, because `--file` resolves the
lane root as `dirname(file)/..` (`sources-census.sh:500-501`), so the E11 used-by
existence check is relative to the *copy's* parent, not the lane:

```
$ cp base-SOURCES.md /fast/scratch/hyaku/mori-r56/Mo56LabCensusSpace/bare/SOURCES.md
$ sources-census.sh validate --file .../bare/SOURCES.md ; echo rc=$?
rc=1
  E11 findings: 361     (--file dir base = /fast/scratch/hyaku/mori-r56/Mo56LabCensusSpace)
  E03 findings: 0
```

361 spurious E11s, because `corpus/knowledge/…` does not resolve under the scratch
parent. The workable fixture is a **full lane mirror** — the same shape round-50
used (`assimilation/a2/mirror-validate.txt`): `git archive <freeze-tip> corpus
SKILL.md PROVINCE.md SCORECARD.md tools`, plus the freeze tip's own `corpus/`
tree. With that mirror the baseline is clean and reproduces the frozen receipt:

```
$ sources-census.sh validate --file .../mirror/mori-shokunin/corpus/SOURCES.md ; echo rc=$?
rc=0
lines=24  W04=23  E-codes=0
$ sources-census.sh census --file .../mirror/mori-shokunin/corpus/SOURCES.md
  file  rows 318   tier.A 287  tier.B 14  tier.C 17
  file  status.mined 267  status.queued 24  status.rejected 27
```

Baseline W04=23 matches `evidence/census-start.txt` (23 W04, `ok`, `exit=0`).
The census selftest is green at the freeze tip (`sources-census.sh selftest` →
`selftest ok`, rc 0, 0 SURVIVED).

The mirror recipe that *does* work, with the minimum file set, is confirmed:
`git archive 8be2717b corpus SKILL.md PROVINCE.md SCORECARD.md tools` → validate
rc=0, E11 count 0. That is the same set round-50 recorded.

## The assigned experiment, run verbatim

The staged row, taken byte-for-byte from `merge/mori/SOURCES.append.md` line 7:

```
| S471 | 第61回 Linuxカーネルのコンテナ機能 - cgroup v2から使うメモリコントローラ（6） — https://gihyo.jp/article/2026/03/linux_containers-0061 | docs | B | … | … | a cgroup's memory-event counters can be **watched** rather than polled — inotify IN_MODIFY or poll POLLPRI — … | mined | 2026-10-23 | 180d | corpus/knowledge/oom-evidence-loss-r38.md, corpus/knowledge/kernel-oom-line-attribution-r12.md |
```

### (a) two leading spaces, inserted in the Registry table before the lane's own S471 (line 250)

```
$ sources-census.sh validate --file <mirror> ; echo rc=$?
rc=1
  file	E01	S471 fields=12
```

**Not** `E03 duplicate id`. The reason is a property of the staged row itself, not
of the indentation: the row contains a literal **backslash-pipe** inside the
`teaches` cell (`grep -ciE 'inotify\|POLLPRI'`), so `awk -F'|'` sees **13 raw
pipes / NF=14 / 12 fields** instead of the contract's 11 columns. The census emits
`E01` and stops there.

### (b) the same row at column zero

```
$ sources-census.sh validate --file <mirror> ; echo rc=$?
rc=1
  file	E01	S471 fields=12

$ diff -u out-2space.validate.txt out-col0.validate.txt
  IDENTICAL (diff empty, rc 0)
```

**The 2-space and column-zero validator outputs are byte-identical.** Same for the
census mode output. And the same for the repaired (well-formed) variant of the row:

```
  2 spaces:  file	E03	S471 duplicate id
  column 0:  file	E03	S471 duplicate id
  diff:      IDENTICAL
```

### Answer to the assigned question

**For a 1-, 2- or 3-space-indented row, the 0–3-space pattern does NOT change the
census's collision verdict.** The census's `row_pass` strips the indentation
(`sub(/^ {0,3}/,"",line)`, `sources-census.sh:616`) and then applies the same
section-scoped logic, so a 2-space duplicate inside `## Registry` yields the same
`E03` a column-zero duplicate yields, and a 2-space row outside `## Registry`
yields the same `E12`. Round-50's guard-proof already established this for the
grep side; this seat confirms it holds for the **census script** itself.

**But the 0–3-space rule is not the whole story, and the real divergences are
elsewhere.** Eight findings, in descending severity.

## Detailed findings

### F1 — HIGH — The census's `E01` short-circuit suppresses `E03`, so a colliding id that is *malformed* is reported as malformed and never as a collision

`row_pass` (`sources-census.sh:634-642`):

```
634	      if (mode=="validate") {
635	        if (NF!=13) {
636	          printf "%s\tE01\t%s fields=%d\n",lane,id,NF-2
637	          if (id !~ /^S[0-9]{3,}$/) printf "%s\tE02\t%s\n",lane,id
638	          next
639	        }
640	        if (id !~ /^S[0-9]{3,}$/) printf "%s\tE02\t%s\n",lane,id
641	        else if (id in seen) printf "%s\tE03\t%s duplicate id\n",lane,id
642	        seen[id]=1
```

The `next` at 638 precedes `seen[id]=1` at 642. Consequences, both measured:

* A malformed copy of a colliding id is reported as `E01` **only** — never `E03`:

```
$ # malformed staged S471 (NF=14) placed immediately before the lane's well-formed S471
$ sources-census.sh validate --file <mirror> ; echo rc=$?
rc=1
  file	E01	S471 fields=12
```

* And because the malformed row never reaches `seen[id]=1`, a **well-formed** row
  carrying the same id is *not* flagged as a duplicate either. Probe with a clean
  pair (malformed S900 then well-formed S900, and the reverse order) — **both
  orders produce `E01` alone**, never `E03`:

```
  (a) malformed S900 THEN well-formed S900:   file	E01	S900 fields=12
  (b) well-formed S900 THEN malformed S900:   file	E01	S900 fields=12
```

So one malformed cell in one row silently removes the duplicate-id signal for that
id from the whole file. This is exactly the staged material's shape: **5 of the
136 staged rows** (`S471, S502, S503, S504, S505`, lines 7, 38–41) carry a literal
`\|` and are NF=14 under the census. `mori`'s own registry currently has **0** such
rows (`grep -cE '^ {0,3}\|.*\\\|' corpus/SOURCES.md` → 0), so the exposure is in
the staged material mori is about to append, not in the landed registry.

Routing note (not a fix proposal): the collision check mori performs itself is
grep-based over `^ {0,3}\|[[:space:]]*S[0-9]{3,}` (round-49/50 lessons), and *that*
check does see the duplicate — the grep multiset contains S471 twice where the
census reports E01 only. The two registry-hygiene mechanisms disagree about the
same bytes. A routed round-57 item should decide which is authoritative and
whether `E01` should also carry the id's duplicate status.

### F2 — HIGH — The census and `count-c3.py` disagree on whether the staged S471 row is well-formed, because they split cells differently

The census splits on **every** pipe (`gawk -F'|'`); `count-c3.py` splits on
**unescaped** pipes only (`FIELDS = re.compile(r"(?<!\\)\|")`,
`.ufo/waves/round-45/count-c3.py:57`). On the same staged bytes:

```
line 7  id=S471: raw_pipes=13 escaped_pipes=1 census_gawk_NF=14 census_fields=12  c3_cells=11  c3_status='mined'
line 38 id=S502: … census_fields=12  c3_cells=11  c3_status='mined'
line 39 id=S503: … census_fields=12  c3_cells=11  c3_status='mined'
line 40 id=S504: … census_fields=12  c3_cells=11  c3_status='mined'
line 41 id=S505: … census_fields=12  c3_cells=11  c3_status='mined'
```

Feeding the staged row through `count-c3.py`'s own `census_rows()`:

```
count-c3 census_rows -> {'S471': 11}
  status (cells[7]) = 'mined'
  used-by (cells[10]) = 'corpus/knowledge/oom-evidence-loss-r38.md, corpus/knowledge/kernel-oom-line-attribution-r12.md'
```

`count-c3.py` reads the row as a **valid 11-cell mined row**; the census reads the
same row as **malformed with 12 fields**. Two tools in the same lane, same bytes,
opposite verdicts. `SOURCES-CONTRACT-v1.md:69-70` states "11 columns means NF=13"
without saying whether an escaped pipe counts — the ambiguity is in the contract,
and the two implementations resolved it differently.

### F3 — MED — The census's *second* parser (the used-by pass) silently skips rows whose extra pipe is not the last one

The census runs two parsers: the gawk `row_pass` above, and a bash `usedby_findings`
(`sources-census.sh:538-573`) that splits with `IFS='|' read -r -a cells` and reads
`status=cells[8]`, `usedby=cells[11]` by **fixed index**. A row with an extra pipe in
the *middle* shifts every later cell:

```
$ # '| S902 | … | teaches with inotify\|POLLPRI inside | mined | … | corpus/knowledge/does-not-exist.md |'
$ sources-census.sh validate --file <fixture> ; echo rc=$?
rc=1
  file	E01	S902 fields=12
```
```
  bash usedby_findings view: cells[1]= S902  cells[8]=POLLPRI inside  cells[11]= 90d
```

`cells[8]` is `POLLPRI inside`, not `mined`, so the row is skipped by the used-by
pass and **the dangling `used-by` is never reported**. The control (same row
well-formed) does report it:

```
  control (well-formed):  file	E11	S903 missing used-by corpus/knowledge/does-not-exist.md
```

And with the extra cell at the *end* instead of the middle, E11 does fire
(`cells[8]= mined`, `cells[11]= corpus/knowledge/does-not-exist.md`) — so the
coverage of the used-by check depends on *where* the malformation sits. The staged
S471 row has its extra pipe in the middle (`teaches`), so it lands in the silent
case: `cells[8]` = the teaches tail, `cells[11]` = `180d`.

### F4 — MED — The frozen contract's own canonical census block is column-0 only, so it and the census script disagree about indented duplicates

`SOURCES-CONTRACT-v1.md:67-80` is the command block every lane's census receipts
are measured against. Its duplicate-id line is:

```
76  awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {…print i}' corpus/SOURCES.md | sort | uniq -d
```

`^\|` — **column zero only**, despite the block's own comment on line 67 reading
"# rows (spacing-tolerant)". Measured on a fixture carrying a 1-space duplicate:

```
  contract block (SOURCES-CONTRACT-v1.md:76): ''   <- EMPTY, collision MISSED
  census:                                      file	E03	S471 duplicate id
```

So the contract's canonical duplicate-id command misses exactly the indented
duplicates that the census script catches, and the round-49/50 lessons' own grep
pattern (`^ {0,3}\|…`) catches. Two of the three registry-hygiene mechanisms in
this fleet disagree on the same bytes, and the one that is *named as canonical* is
the strictest.

### F5 — LOW — The 4-space boundary is confirmed, and a 4-space row is invisible to *every* code, including `E12`

Round-50's lesson established that a 4-space row is "treated as code, not as a
row" for the grep side. Confirmed for the census script, and the boundary is
complete — not merely "not counted" but wholly unreportable:

```
  4-space duplicate inside Registry:  validate rc=0, "file ok", census rows stays 318
  4-space row outside Registry:       validate rc=0, "file ok"   (no E12 either)
  1-space row outside Registry:       file	E12	S471 row outside Registry section
```

The `## Paths` control matters: `E12` is emitted for out-of-section rows
(`sources-census.sh:618-623`) but only when the row matches
`^\|[ \t]*S[0-9]{3,}[ \t]*\|`. A 4-space row is skipped at line 615
(`if (line !~ /^ {0,3}\|/) next`) before any section check, so it produces no
`E12` either. A 4-space row is a complete blind spot for every code in the census.

### F6 — LOW — `S471x` (prefix-only id) is reported by nothing when it is outside the Registry section

`E12`'s regex requires `S<digits>` followed by optional space then `|`. `S471x`
does not match, so the row escapes every code:

```
  | S471x | … |   outside Registry:  file	ok	<path>      (no E12, no E02, no E03)
  | S471x | … |   inside  Registry:  file	E02	S471x
```

Also note the two registry-hygiene id extractors use **prefix** matching, not exact
tokens: `grep -oE 'S[0-9]{3,}'` over `| S471x |` yields `S471`, so the grep
multiset records S471 **twice** (319 occurrences / 318 distinct) — a phantom
duplicate of a real id. `count-c3.py` avoids this by matching whole tokens
(`ROW_RE = re.compile(r"^ {0,3}\|\s*(S\d{3,})\s*\|")`, `count-c3.py:56`), which is
why its collision arm is sound where the grep arm is not.

### F7 — LOW — The staged file has no `## Registry` heading, so the census reads 0 rows from it while grep sees 136 ids

Applying the census to the staged file directly:

```
  census rows: 0            (no '## Registry' heading in SOURCES.append.md)
  grep id-set size: 136
  validate rc=1: 136 × "E12 <id> row outside Registry section"
```

This is expected behaviour (the staged file is an append fragment, not a registry),
but it means the staged ids can never be validated by the census in place — the
collision check must be the grep/`comm` one, and per F1/F6 that one is
prefix-based. Measured collision set for this round's assimilation:

```
  reg-ids=318  staged-ids=136  →  75 collisions
  S471 S472 … S545  (the whole staged range S471–S545 collides with the lane's)
```

`S471` — the id this seat was told to use — is the **first** of those 75.

### F8 — LOW — The frozen census receipt does not contain a rows line, though the contract cites "316 rows"

The contract states: "Start census receipt: `evidence/census-start.txt` (exit 0,
316 rows, 23 W04)". The file is 25 lines: 23 × `W04`, one `mori ok`, one `exit=0`.
There is **no rows line** in it (`grep -cE 'rows' evidence/census-start.txt` → 0).
The 316 figure is reproducible by re-running the census at the entering tip —
`git archive 5b295eee corpus SKILL.md PROVINCE.md SCORECARD.md tools` → census
rows **316**, validate rc=0, **23** W04, matching the receipt's W04 count and
`ok`/`exit=0` exactly. So the number is correct and derivable; it is simply not
carried by the receipt bytes. This is adjacent to the round-55 routed defect
("census before→after must be captured bytes or the counting command"), and it is
routed rather than fixed here.

## What the 0–3-space pattern means for mori's registry hygiene — the summary

| mechanism | 0–3 spaces | 4+ spaces | exact-id? | malformed row? |
|---|---|---|---|---|
| census script `row_pass` (E01/E02/E03/E05–E12) | seen, section-scoped | invisible | yes | `E01` short-circuits `E03` |
| census script `usedby_findings` (E11) | seen, index-based | invisible | n/a | skipped if the extra pipe is mid-row |
| `SOURCES-CONTRACT-v1.md:76` canonical block | **col-0 only — misses indented duplicates** | invisible | prefix | n/a |
| lane grep `^ {0,3}\|[[:space:]]*S[0-9]{3,}` (round-49/50) | seen, whole file | invisible | **prefix** (`S471x`→`S471`) | sees the duplicate the census calls E01 |
| `count-c3.py` (`:56-57`) | seen, whole file | invisible | **yes, whole tokens** | **reads the staged row as valid** |

The 0–3-space pattern is **not** where mori's registry hygiene is at risk: the
census and the lane's own grep agree on 1–3 spaces, and both treat 4+ spaces as
code. The risk is in the **malformed-row** axis (F1, F2, F3): the staged material
that mori is about to append contains 5 rows whose escaped pipe makes them
NF=14 under the census, and a malformed row silently drops the duplicate-id
signal for its id from the census, is read as *valid* by `count-c3.py`, and has its
`used-by` existence check skipped by the census's own second parser.

## Recommended routed items for round 57 (routing only — no fix is proposed or applied here)

1. **R56-L1** — Decide whether the census's `E01` arm should also report the id's
   duplicate status (and whether a malformed row should register in `seen[]`), so
   one malformed cell cannot delete a duplicate-id signal. Currently
   `sources-census.sh:635-642`.
2. **R56-L2** — Resolve the escaped-pipe cell-splitting ambiguity at the contract
   level ("11 columns means NF=13" does not say whether `\|` counts) and make the
   census and `count-c3.py` resolve it the same way.
3. **R56-L3** — Align the census's `usedby_findings` cell indexing with the
   gawk pass so a mid-row extra pipe cannot silently skip the used-by existence
   check (`sources-census.sh:538-573`).
4. **R56-L4** — Either widen `SOURCES-CONTRACT-v1.md:76` to the 0–3-space pattern
   its own line-67 comment advertises, or record that the canonical block is
   deliberately column-0 and route the indented-duplicate case to the census.
5. **R56-L5** — State in the contract that the collision check compares **whole
   id tokens**, not the `grep -oE 'S[0-9]{3,}'` prefix, so `S471x` cannot be
   counted as a second `S471`.

## Reproduction

All fixtures and evidence live under
`/fast/scratch/hyaku/mori-r56/Mo56LabCensusSpace/` (scratch removed on exit; this
report quotes the outputs inline above). Mirror recipe:
`git -C <lane> archive 8be2717b corpus SKILL.md PROVINCE.md SCORECARD.md tools | tar -x -C <mirror>/mori-shokunin`.
Driver scripts: `final.sh` (the consolidated evidence, sections E0–E10),
`probe.sh`/`probe2.sh`/`probe3.sh`/`probe4.sh`/`probe5.sh`/`probe7.sh`/
`probe8.sh`/`probe9.sh`/`probe10.sh`/`probe11.sh`/`probe12.sh` (the individual
probes). The lane's `corpus/SOURCES.md` was **not** modified — `git diff --stat
HEAD -- corpus/SOURCES.md` in the lane is empty.

Tooling: no package was installed or upgraded for this seat; the census script,
`gawk`, `awk`, `sed`, `grep`, `python3` (stdlib only) and `git` as found on the
host were used. Nothing was written under `~/.local/bin` or any PATH directory.
No credential, session or private URL material appears in this report.

## Findings

| # | severity | finding | file / line |
|---|---|---|---|
| F1 | HIGH | `E01` short-circuit `next` precedes `seen[id]=1`, so a malformed colliding id is reported as malformed and never as a duplicate; a well-formed twin of the same id is also not flagged | `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh:635-642` (esp. 638 vs 642) |
| F2 | HIGH | The census splits on every pipe; `count-c3.py` splits on unescaped pipes only — the same staged S471 row is NF=14/12 fields to the census and a valid 11-cell mined row to `count-c3.py` (5 staged rows affected: S471, S502–S505) | `scripts/sources-census.sh:606` (`gawk -F'|'`) vs `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-45/count-c3.py:57` (`FIELDS = re.compile(r"(?<!\\)\|")`) |
| F3 | MED | The census's second (used-by) parser indexes cells by fixed position; an extra pipe in a *middle* cell shifts `status` off `cells[8]`, so the dangling `used-by` is never reported | `scripts/sources-census.sh:538-573` (esp. 553-556, `cells[8]`/`cells[11]`) |
| F4 | MED | The frozen contract's canonical census block is column-0 only (`^\|`) and misses indented duplicates that both the census script and the lane's own grep catch — its line-67 comment claims "spacing-tolerant" | `/home/vgpnk/Projects/shokunin/.ufo/waves/kaika/SOURCES-CONTRACT-v1.md:67,76` |
| F5 | LOW | A 4-space-indented row is invisible to every census code, including `E12` for out-of-section rows; the 1–3-space boundary is confirmed identical to column zero | `scripts/sources-census.sh:615` (`if (line !~ /^ {0,3}\|/) next`), `:618-623` (E12) |
| F6 | LOW | A prefix-only id (`S471x`) outside the Registry section is reported by nothing; the grep id-extractor is prefix-based and records `S471x` as a second `S471` (319 occurrences / 318 distinct) | `scripts/sources-census.sh:619` (E12 regex); `count-c3.py:56` (exact-token `ROW_RE`, which avoids it) |
| F7 | LOW | The staged file has no `## Registry` heading: census reads 0 rows from it while grep sees 136 ids; the round-56 collision set is 75 ids (S471–S545), S471 first | `/home/vgpnk/Projects/shokuknow/merge/mori/SOURCES.append.md` (read-only); `scripts/sources-census.sh:611` (`in_registry=(trim(substr(line,3))=="Registry")`) |
| F8 | LOW | The frozen census receipt carries no rows line, though the contract cites "316 rows"; 316 is reproducible at the entering tip (23 W04, rc 0) but is not in the receipt bytes | `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-56/evidence/census-start.txt` (25 lines, no rows line) vs `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-56/contract.md` ("exit 0, 316 rows, 23 W04") |
| — | LOW | A bare `corpus/SOURCES.md` copy validated with `--file` yields 361 spurious `E11`s, because `--file` resolves the lane root as `dirname(file)/..`; the round-50 mirror recipe (`corpus` + `SKILL.md PROVINCE.md SCORECARD.md tools`) yields rc 0 | `scripts/sources-census.sh:500-501` (`dir_abs=$(realpath -- "$(dirname -- "$file_abs")/..")`) |
