# Mo51RevSourcesRows — SOURCES rows S492–S496 at 87e0c374537557754bf71dd68036ded3ddc6699c

Seat: Mo51RevSourcesRows (leaf reviewer). Item: review rows S492–S496 of
`mori-shokunin/corpus/SOURCES.md` at the data commit 87e0c374537557754bf71dd68036ded3ddc6699c
against the 11-column SOURCES schema in `/home/vgpnk/Projects/shokunin/CORPUS.md`, the
evidence copies under `corpus/evidence/sources-r51/`, and the census script
`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`.

Method: all reads are read-only git objects at the data commit (`git show` / `git ls-tree`
in `/home/vgpnk/Projects/shokunin/mori-shokunin`); the census validator was run over the
`SOURCES.md` extracted from that commit into seat scratch
(`/fast/scratch/hyaku/mori-r51/Mo51RevSourcesRows/`). No fleet/lane/corpus/tool files were
modified. No ENTAIL lines (not an entailment seat). Scratch removed on completion.

## 1. Schema conformance (CORPUS.md `## SOURCES.md` section: 11 columns, NF=13)

All five rows parse with NF=13 (checked with the CORPUS.md census awk, `NF!=13` count = 0
for these rows):

| id | kind | tier | status | opened | recheck | used-by | validator |
|---|---|---|---|---|---|---|---|
| S492 | docs | A | mined | 2026-10-26 | on-release | corpus/knowledge/memavailable-estimate-r51.md | W04 only |
| S493 | code | A | mined | 2026-10-26 | on-release | corpus/knowledge/memavailable-estimate-r51.md | clean |
| S494 | code | A | mined | 2026-10-26 | on-release | corpus/knowledge/memavailable-estimate-r51.md | clean |
| S495 | code | A | mined | 2026-10-26 | on-release | corpus/knowledge/memavailable-estimate-r51.md | clean |
| S496 | code | A | mined | 2026-10-26 | on-release | corpus/knowledge/memavailable-estimate-r51.md | clean |

- kind: `docs` for proc.rst (official kernel documentation) and `code` for the three
  `mm/*.c`/`include/linux/*.h` sources and for the commit patch S496 are all valid enum
  values (E05 enum check passed). A commit `.patch` is a diff of kernel source, so `code`
  is the correct enum bucket (primary artefact of the change), and it is the original
  2014 commit that introduced MemAvailable — tier A is appropriate.
- tier A for all five (no E06/E10). All are primary or authoritative for their scopes.
- status mined with non-`—` used-by (no W01/W03). opened 2026-10-26 ≤ today (no E08).
- recheck `on-release` is a symbolic cadence — accepted (see §5).

## 2. Census: S492 is W04, not E04

Command (run in seat scratch over the data-commit bytes):

```
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --today 2026-10-26 \
    --file /fast/scratch/hyaku/mori-r51/Mo51RevSourcesRows/corpus/SOURCES.md
```

Deciding output lines (excerpt):

```
file	W04	S168 duplicate url raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/filesystems/proc.rst across scopes
file	W04	S492 duplicate url raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/filesystems/proc.rst across scopes
```

No `E04` line is emitted for S492 (nor for any row). No E02/E03/E05/E06/E07/E08/E09/E10
line is emitted for S492–S496. Exit code was `1`, caused exclusively by `E11` lines that are
artifacts of running against the extracted file: the E11 check (`usedby_findings`, lines
538–571) resolves `used-by` paths against `$dir = realpath(dirname(file)/..)` — the seat
scratch root — which does not contain the lane's corpus tree. The real targets exist at the
data commit (see §4). The lane's actual registry at 87e0c37 would therefore report only the
W04 family (S168, S492, …) plus whatever other pre-existing findings the full tree holds —
not asserted here (data-commit working tree not checked out; read-only constraint).

Deciding script lines (`scripts/sources-census.sh`), quoted verbatim:

```
643:        scope_key=u SUBSEP scope
644:        if (u!="" && (u in url_seen) && !(scope_key in url_scopes))
645:          printf "%s\tW04\t%s duplicate url %s across scopes\n",lane,id,u
646:        if (u!="" && (scope_key in url_scopes) && status!="rejected" &&
647:            url_scope_nonrejected[scope_key] &&
648:            teaches !~ /supersedes S[0-9]{3}/)
649:          printf "%s\tE04\t%s duplicate url %s within scope %s\n",lane,id,u,scope
```

- W04 (line 645) fires when the same normalized URL has been seen before but under a
  different scope string, and is a warning (validate main loop lines 738–746 emits
  `[EW][0-9]+` lines; only `E` lines set `findings=1`; the selftest pins
  `W04-does-not-fail-validation` → exit 0).
- E04 (lines 646–649) requires the same URL **and** scope key to have been seen before,
  among non-rejected rows, without a `supersedes` teaches.
- S082's scope is "textual mountinfo field layout only"; S492's scope is the
  `/proc/meminfo` field definitions; S168's scope is the rejected-candidate note. All three
  strings differ, so `scope_key` stays distinct and E04 cannot fire; W04 does.
- Therefore: S492 is a W04 (same URL across scopes), not an E04, and its scope cell string
  is genuinely distinct from S082 and S168 (E04 guard would also have rejected S168 had it
  duplicated any non-rejected same-scope row — it did not).

## 3. Anchors really cover what they name (evidence copies opened)

All five copies exist at the data commit (`git ls-tree 87e0c37:corpus/evidence/sources-r51/`
→ `34e431b0.patch, meminfo.c.v7.2, mm_inline.h.v7.2, proc.rst.v7.2, show_mem.c.v7.2`).
Line numbers below are the committed byte ranges (verified by `grep -n` on the blob).

- **S492** proc.rst `1124-1135` (MemFree label 1124, MemAvailable label 1126 + definition
  1127–1134, Buffers label 1135), `1138-1141` (Cached label 1138 + definition 1139–1141),
  `1192-1201` (Shmem 1192–1193, KReclaimable 1194–1197, SReclaimable 1200–1201). Every
  field the scope names is present in its range. The entry's five S492 quotes land inside
  these ranges (e.g. "An estimate of how much memory is available for starting new
  applications, without swapping." = 1127–1128; "In-memory cache for files read from the
  disk (the pagecache) as well as tmpfs & shmem." = 1139–1141).
- **S493** show_mem.c `23,32-73`: line 23 is the `totalreserve_pages` global
  (declaration feeding the base term); lines 32–73 contain the whole `si_mem_available()`
  body — wmark sum loop 40–41, free-minus-reserve base 47, file-LRU term 54–57, reclaimable
  kernel term 64–67, zero clamp 69–71, return 71. Every entry quote lands at 26–27+47,
  38+40–41, 50–51, 56–57, 60–61, 66–67, 69–71 — all inside the named ranges.
- **S494** meminfo.c `27-31,48-51,56,61-64,105`: 27–31 = `show_val_kb` helper
  (signature 28, `seq_put_decimal_ull_width(… PAGE_SHIFT - 10 …)` 30, kB suffix 31);
  48–51 = Cached derivation (`cached = global_node_page_state(NR_FILE_PAGES) -
  total_swapcache_pages() - i.bufferram;` 48–49, non-negative clamp 51); 56 =
  `available = si_mem_available();`; 61–64 = the MemFree (61) / MemAvailable (62) lines;
  105 = Shmem line. All three scope items ("kB helper, Cached derivation, MemFree and
  MemAvailable lines") are covered; all entry quotes land inside.
- **S495** mm_inline.h `13-31`: doc comment 13–18 states file-LRU (14–15) vs anon/tmpfs
  (16–17) sorting; `folio_is_file_lru()` body 19–22. Both entry quotes land at 14–15 and
  16–17.
- **S496** commit patch: message lines 6–27 = the motivation ("They generally do this by
  adding up \"free\" and \"cached\", which was fine ten years ago," = 7–8; Cached/shared
  memory/tmpfs wrongness = 11–14); hunks for `fs/proc/meminfo.c` present at `@@ -26,7
  +26,11`, `@@ -47,12 +51,44`, `@@ -105,6 +141,7` (additions include the `MemAvailable`
  print line). Both named items are covered.

Copy hashes computed from the blobs match both the row cells and the freeze manifest
(`.ufo/waves/round-51/evidence/freeze-sha256.txt` at 87e0c37): proc.rst
`e760f716f8278deefab17a63739033cadc7faee93663c49e76455afaaf40d126`, show_mem.c
`dba76b263bbdf93323a277a29c9281a892ff3fb35ddd6f0ddaf9ba1acb5b02f5`, meminfo.c
`d6c5807421a69eac21efd737b39d099c711b3132b371dc34986d181746e3deda`, mm_inline.h
`2d4accbbc1ec139bfe11a356d4d17a55a2543769f3e10057a8a8584429c45ef6`, 34e431b0.patch
`9f571a04fc365858d8c82d31b309217a5e40f37877732da70416b0b1b42563d0`.

## 4. teaches grounded; used-by exact; on-release accepted

- Every `teaches` sentence is a paraphrase of text present in the anchored ranges above
  (S492: estimate-for-starting-applications; Cached includes tmpfs/shmem. S493: formula
  terms and clamp. S494: kB shift helper, Cached base difference. S495: tmpfs folios →
  anon LRU. S496: free+cached overstates startable memory because Cached holds non-freeable
  shared memory and tmpfs).
- `used-by` cell is exactly `corpus/knowledge/memavailable-estimate-r51.md` for all five
  rows, and that file exists at the data commit (`git ls-tree 87e0c37:corpus/knowledge/`
  → blob `b34adda32cc581ca58fdf7de449181592a17336c`). The entry's `source:` block lists
  all five rows (S492–S496) with matching URLs, kinds, tiers and opened dates.
- `on-release` is valid: the parser treats symbolic cadences via `symbolic()` (line 582),
  E09 rejects only non-ISO/non-NNd/non-symbolic values (line 665), and `overdue` mode
  reports symbolic cadences but never judges them overdue (lines 676–682). Observed:

```
$ sources-census.sh overdue --today 2026-10-26 --file <scratch>/corpus/SOURCES.md
file	cadence	S492 recheck=on-release opened=2026-10-26
file	cadence	S493 recheck=on-release opened=2026-10-26
file	cadence	S494 recheck=on-release opened=2026-10-26
file	cadence	S495 recheck=on-release opened=2026-10-26
file	cadence	S496 recheck=on-release opened=2026-10-26
(exit 0; none reported overdue)
```

## Findings

- **LOW** — `corpus/SOURCES.md` row S492, scope cell: the phrase "S168 was the rejected
  same-scope duplicate" is inaccurate. S168's own record says it was rejected at round 31
  as a duplicate **of S082's URL** ("duplicate URL already carried by S082 (sha256 prefix
  e760f716f8278dee); not re-registered", teaches cell; scope cell "rejected candidate: same
  URL and bytes as S082"). It was never scoped to the `/proc/meminfo` field definitions, so
  it was not a same-scope duplicate of S492. Fix: reword to "S168 was the rejected
  same-URL candidate (duplicate of S082)" or drop the clause.
- **LOW** — consistency nit: row S493's anchor cell ends at `show_mem.c:23,32-73` while
  the entry prose cites `show_mem.c.v7.2:32-72`; both cover the full formula, so this is
  cosmetic, but aligning the trailing line would prevent a future recheck ambiguity.

No HIGH/MED defects found in scope: schema conformance, kind/tier classification, scope
distinctness (W04, not E04), anchor coverage, teaches grounding, used-by exactness, and
`on-release` acceptance all hold at 87e0c37.

## Named limits

- The E11 findings in the scratch run are artifacts of running the validator over an
  extracted file outside the lane tree (used-by paths resolve against the scratch root); the
  five used-by targets were verified present at the data commit via git objects instead.
  A full-registry validate verdict for the lane at 87e0c37 was not produced (read-only
  constraint; working tree not used).
- Verdict covers only rows S492–S496; other registry findings (e.g. other W04 rows) were
  observed but not adjudicated by this seat.
- The W04 for S492 depends on registry order (S082 precedes S492 in the file) — true for
  the committed file (S082 at line 88, S168 at line 174, S492 at line 271).

Seat scratch `/fast/scratch/hyaku/mori-r51/Mo51RevSourcesRows/` removed at exit.
