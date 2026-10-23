# AttackSrc190 — wave 2 falsification of source row S190 (sysstat v12.8.0 iostat.c)

Seat: MoriR33.AttackSrc190. Lane rev read: 62db24c0 (working tree identical for the files cited). Read-only on the
lane; all scratch under `/fast/scratch/hyaku/mori-r33/AttackSrc190/`. No installs, no edits outside this report, no
processes left running.

## Verdict

**One blocker.** Row S190's bytes, locators, hashes and word counts all hold, and the URL is genuinely tag-pinned
(proved at git-blob level). What fails is the *claim*: the landed teaches cell (`corpus/SOURCES.md:196`) and entry
row 14 (`corpus/knowledge/disk-write-rate-r33.md:32`) state the 0.0 clamp as iostat's behaviour, but in the
committed copy that clamp exists only in the extended-stat path; the default report path prints an unclamped value
from the same two samples, and a full counter set-back is caught by a reset heuristic that produces a value computed
from zero instead. Under R-J that is exactly "a row the judge would accept only with a caveat".

## Checks that passed (with commands)

1. **Live fetch == committed copy == Gate sha256.** `curl -sSL --fail -m 60 <url>` → 71,360 bytes, exit 0;
   `sha256sum live.src` = `f099229c0051be9538f220d63fe7953247ee947f112d367ff647d791953b9dce`;
   `sha256sum corpus/evidence/sources-r33/S190.src` = same; Gate row (`corpus/lessons/round-33.md:25`) carries the
   same 64-hex value. No retry needed (no 429).
2. **Tag pinning proved at blob level.** `git hash-object corpus/evidence/sources-r33/S190.src` =
   `76987d6a855a9904663e3cfac8a095e5fdd8d2f6`; GitHub contents API at `?ref=v12.8.0` reports
   `blob_sha: 76987d6a855a9904663e3cfac8a095e5fdd8d2f6 size: 71360`. `git/ref/tags/v12.8.0` exists as an annotated
   tag (`type: tag`, object `d4204de358b…`), tagger date `2026-08-28T16:10:14Z`, commit `ffabe8175aa9…`. So the
   bytes are the tag's bytes, not a moving branch head, and the "(C) 1998-2026" header (S190.src:3) matches a 2026 tag.
3. **Gate quote 1 at its locator.** `sed -n '1151p' S190.src` → ` * @ioi		Current sample statistics.` (4 words ✔).
4. **Gate quote 2 at its locator.** `sed -n '1152p' S190.src` → ` * @ioj		Previous sample statistics.` (4 words ✔).
5. **Gate quote 3 at its locator.** `sed -n '1516,1517p' S190.src` →
   `xios.wsectors = ioi->wr_sectors < ioj->wr_sectors ? 0.0 :` / `S_VALUE(ioj->wr_sectors, ioi->wr_sectors, itv);`
   — the quote is the two lines joined; 11 words ✔ (`python3 -c "len(q.split())"` on all three quotes → 4, 4, 11).
6. **All three quotes present in the whitespace-collapsed copy.** `tr -s '[:space:]' ' ' < S190.src` then `grep -F`
   each quote → FOUND, FOUND, FOUND.
7. **URL not duplicated and not pre-existing.** `grep -c -F '<url>' corpus/SOURCES.md` = 1 (line 196);
   `grep 'sysstat|iostat'` on that file returns only S190; `git show 7d382043:corpus/SOURCES.md | grep -i sysstat`
   returns nothing (only S033's docs.kernel.org row matches `iostat`), so the entering tip did not carry it. The sha
   appears once in `corpus/lessons/round-33.md` and once as the URL — one admit Gate row.
8. **Kind / tier.** Official upstream repository (`github.com/sysstat/sysstat`, the project's own tree; header names
   the sysstat author, S190.src:3), C source file, release tag → `code` / `A` correct. `mined` + `on-release` +
   used-by `corpus/knowledge/disk-write-rate-r33.md` consistent with entry row 14's sources cell.

## Findings

### F1 — blocker: the 0.0 clamp is asserted for all of iostat but exists only in the extended-report path

Attacks: `corpus/SOURCES.md:196` teaches cell ("prints a write-sector rate of 0.0 when the current count is below the
previous one") and `corpus/knowledge/disk-write-rate-r33.md:32` observation + reading cells.

Evidence (committed copy `corpus/evidence/sources-r33/S190.src`):

- The clamp is in `write_ext_stat` (defined S190.src:1462), lines 1516-1517: `xios.wsectors = ioi->wr_sectors <
  ioj->wr_sectors ? 0.0 : S_VALUE(...)`.
- S190.src:1941-1945 dispatch: `if (DISPLAY_EXTENDED(flags)) { write_ext_stat(...) } else { write_basic_stat(...) }`.
  So the clamp is reached only with `-x`/`-e`.
- The default report recomputes the same rate with **no** `<` test and no 0.0:
  `1614: wsectors = S_VALUE(ioj->wr_sectors, ioi->wr_sectors, itv);` printed at 1640-1642 as
  `/* kB_read/s kB_wrtn/s kB_dscd/s */ cprintf_f(..., rsectors, wsectors, dsectors);`
  and the JSON basic twin at 1706: `S_VALUE(ioj->wr_sectors, ioi->wr_sectors, itv) / fctr` (column `Blk_wrtn/s`,
  1701).
- Wave 1's own seat had already recorded the divergence and it did not survive into the landed row:
  `.ufo/waves/round-33/w1/SrcSysstatIostat.md` fact 4 quotes 1739-1742 — `wr_sec = ioi->wr_sectors -
  ioj->wr_sectors; if ((ioi->wr_sectors < ioj->wr_sectors) && (ioj->wr_sectors <= 0xffffffff)) { wr_sec &=
  0xffffffff; }` — i.e. the basic path masks the *totals* instead of clamping the rate. The landed anchor
  (`iostat.c:1151-1152,1516-1517`) drops 1614, 1706 and 1739-1742 entirely.

Why it fails the rule: the entry asserts "iostat (sysstat 12.8.0) shows 0.0 for a device's write-sector rate" and
"it prints 0.0 instead of a rate from the two samples" without the `-x` qualifier. The same committed file prints the
write rate from two samples without any zero substitution in the default report, so the row is true only under a
caveat — R-J's "including a row the judge would accept only with a caveat". Same overreach in the teaches cell under
R-R. What the default path actually prints for a negative delta is not in the committed copy (S_VALUE is defined in
`common.h`, not in this file), so I state only that it is **not** the claimed 0.0; the sign is [INFERENCE].

Fix shape (for the owner, not applied): qualify both cells to the extended report, or re-anchor to 1614/1706/1739-1742
and state the two paths separately.

### F2 — major: the teaches cell's "prints" clause is not stated by any quote the row carries

Attacks: `corpus/SOURCES.md:196` teaches cell, under R-R ("a quote … states it").

The quoted text at 1516-1517 assigns a struct field, `xios.wsectors`. Nothing in the three Gate quotes says that field
is printed, or that it is the "write-sector rate": the display sites are 1249-1253 (`/* wkB/s */ cprintf_f(...,
xios->wsectors)`) and 1408 (`xios->wsectors /= fctr` in the JSON ext printer), and neither is in the anchor
`iostat.c:1151-1152,1516-1517`. A judge applying R-R strictly needs the caveat "given that this field is the printed
column" — which R-R names as unsupported. (Softer than F1: the chain is real, it is just unquoted.)

### F3 — major: the verdict's causal clause is contradicted by the reset heuristic in the same file

Attacks: `corpus/knowledge/disk-write-rate-r33.md:32` verdict cell — "a counter set back between samples also yields
zero".

S190.src:1887-1892, in `write_stats`, runs before the path dispatch: `/* Try to detect if device has been removed then
inserted again */ if (((ioi->rd_ios + ioi->wr_ios + ioi->dc_ios + ioi->fl_ios) < (ioj->rd_ios + ioj->wr_ios +
ioj->dc_ios + ioj->fl_ios)) && (!ioj->rd_sectors || (ioi->rd_sectors < ioj->rd_sectors)) && (!ioj->wr_sectors ||
(ioi->wr_sectors < ioj->wr_sectors)) && (!ioj->dc_sectors || (ioi->dc_sectors < ioj->dc_sectors))) { ioj = &iozero;
}`.

A counter set-back that resets all counters (device re-registered — the case the heuristic targets) trips every
conjunct, so the previous sample becomes all zeros and the printed value is computed from zero (a spike), not 0.0.
0.0 appears only for a set-back that escapes the heuristic (e.g. write sectors down while the IO total and read
sectors are up). So "a counter set back … yields zero" is true only for a partial set-back, and never for the default
report at all (F1). Neither the heuristic nor its consequence is quoted or anchored.

### F4 — minor: the scope cell names one behaviour for a file that has two disagreeing ones

Attacks: `corpus/SOURCES.md:196` scope cell — "how iostat 12.8.0 forms the write-sector rate from the current and
previous sample, and what it prints when the current count is lower". The file forms that rate in three places
(1517 guarded, 1614 unguarded, 1706 unguarded) and handles a lower current count two different ways (0.0 vs the
0xffffffff mask at 1739-1742). The scope, read literally, is satisfied by the anchor but hides the divergence the
row then asserts away. Reporting-accuracy, not a hash/locator defect.

## Not checked / remaining unknowns

- The definition and arithmetic of `S_VALUE` are not in the committed copy (`common.h` is not S190's page), so the
  sign/magnitude the default path prints for a negative delta is [INFERENCE]; F1 does not depend on it.
- No live repro: producing a counter set-back would require touching a block device, which this seat is forbidden to
  do. All findings are static, from the committed copy.
- Entry row 14's other source (S181) and the anti-copy span rules for that row are outside this seat (S181 seats).
- The Gate row's fetch timestamp (02:40:11Z) was not re-verified against the wave-1 log beyond the sha256 match with
  wave 1's two recorded fetches.
