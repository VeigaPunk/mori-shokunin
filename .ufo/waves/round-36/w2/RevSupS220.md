# RevSupS220 — re-open S220 (sysstat iostat.c v12.8.0), attack: row + copy

Reviewer: mori-r36-w2-RevSupS220-23 (wave 2, attempt 2). Date: 2026-10-23.
Attacks: (a) the S220 row's teaches-cell language asserted at `iostat.c:1444-1464` (contiguous quote
≤25 words required); (b) the row's copy being sha256-equal to upstream v12.8.0; (c) the row's scope
caveat (extended-stat path only, not the basic-stat path); plus the S220→S190 supersedes honesty.

## Measurements (command → observed output)

### M1 — copy sha256-equal
```
$ curl -sS -o iostat-v12.8.0.c https://raw.githubusercontent.com/sysstat/sysstat/v12.8.0/iostat.c
$ sha256sum iostat-v12.8.0.c /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/evidence/sources-r36/S220.src
f099229c0051be9538f220d63fe7953247ee947f112d367ff647d791953b9dce  iostat-v12.8.0.c
f099229c0051be9538f220d63fe7953247ee947f112d367ff647d791953b9dce  .../sources-r36/S220.src
$ wc -lc <both>          ->  2448 71360 (both, identical)
```
PASS: the round-36 copy is byte-identical to my fresh upstream fetch (tag-pinned URL). Bonus
consistency: the superseded row's round-33 copy `corpus/evidence/sources-r33/S190.src` hashes to the
same `f099229c…` — S220 re-rows the same pinned bytes, no silent retarget.

### M2 — teaches language at 1444-1464 (contiguous quote ≤25 words)
`nl -ba iostat-v12.8.0.c` (fetched bytes, sha above):
- 1444-1461: doc comment of `write_ext_stat` ("Display extended stats …"); 1462-1464: signature.
- 1456: ` * @ioi		Current sample statistics.`
- 1457: ` * @ioj		Previous sample statistics.`
Contiguous quote from inside 1444-1464, 6 words: **"Current sample statistics. Previous sample
statistics."** Teaches cell says "iostat labels ioi as the current sample and ioj as the previous
sample" — semantics double-confirmed at the only dispatching caller: iostat.c:1870-1871
`ioi = d->dev_stats[curr]; ioj = d->dev_stats[!curr];`. PASS.

### M3 — "write-sector value to 0.0 when the current count is lower" (extended path)
iostat.c:1516-1517 (row anchor `1516-1517 (write_ext_stat)`):
```c
	xios.wsectors = ioi->wr_sectors < ioj->wr_sectors ? 0.0 :
			S_VALUE(ioj->wr_sectors, ioi->wr_sectors, itv);
```
Exactly the teaches claim; single `xios.wsectors` feeds both plain and JSON rendering of
`write_ext_stat` (comment 1446-1447 "in plain or JSON format"). PASS.

### M4 — scope caveat honored; basic-path contrast true
Row scope: "the extended-statistics output path … (write_ext_stat) only …; not the non-extended
basic-stat path". Teaches mentions the basic path only in the contrast clause "calculates wsectors
separately with S_VALUE" — verified everywhere the basic path produces a per-second write value:
- write_plain_basic_stat, iostat.c:1614 `wsectors = S_VALUE(ioj->wr_sectors, ioi->wr_sectors, itv);`
  (anchor 1602-1615 covers signature 1602-1605 through the three S_VALUE lines 1613-1615); no
  0.0-reset anywhere in 1602-1656.
- write_json_basic_stat, iostat.c:1706 `S_VALUE(ioj->wr_sectors, ioi->wr_sectors, itv) / fctr,`
  — likewise plain S_VALUE, no reset (def 1675-1711).
- write_basic_stat, iostat.c:1728-1755 (anchor exact): computes `wr_sec` by subtraction with 32-bit
  wrap masking (1739-1742) — a total, not the per-second value; then dispatches 1748-1755.
- Anchor 1941-1945 is the exact path split: `if (DISPLAY_EXTENDED(flags)) write_ext_stat(…) else
  write_basic_stat(…)`. PASS: the 0.0-reset claim is never attributed to the basic path; the caveat
  holds.

### M5 — supersedes honesty (S220 → S190)
`git diff 6bd57097..bf0df77fee4b6ef54a90aea09335c7617f125151 -- corpus/SOURCES.md` filtered to
S190/S220 rows shows only the added `+| S220 …` line; S190's row is byte-unchanged this round — the
discharge is the S220 supersede declaration itself, per the routed repair design. S220's "supersedes
S190 — …" summary faithfully restates S190's teaches (corpus/SOURCES.md:196: ioi current / ioj
previous, 0.0 "when the current sectors-written count is below the previous one") and adds precisely
what S190 lacked (basic-path contrast; S190 said only "the default report computes its rate
elsewhere and is not covered by this row"). used-by `corpus/knowledge/disk-write-rate-r33.md:33`
(row 14) describes exactly this behavior. PASS.

## Findings by severity
- Critical: none.
- Major: none.
- Minor: none.

## C1 note (freshness angle)
`.ufo/waves/round-36/evidence/c1-after.txt` is aggregate-only (6 lines, no per-row entries) — no
per-row or aggregate line infers freshness admission for S220. My M1 is a point-in-time byte
comparison at fetch time 2026-10-23, not a freshness verdict; nothing in S220's row or in the
receipt claims one.

## Residual risk / verification gaps
- Upstream raw.githubusercontent.com is CDN-served; M1 proves equality at my fetch instant, not
  perpetuity. Row recheck is `on-release`, tag-pinned — adequate per registry rules.
- I did not compile/run iostat; all evidence is source reading against sha-pinned bytes.
- LSP unavailable for C-source row checks in this context (external upstream file, no lane server);
  all checks are direct reads of the sha256-pinned artifact, so grep-level risk does not arise.
- No tools installed (tooling authorization unused; no pacman touched).

## VERDICT: PASS
