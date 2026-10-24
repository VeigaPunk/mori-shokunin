measured 2026-10-23T12:07:06Z

# S190 source re-open

## Finding and decision

VERDICT: supported

At tip `6bd57097`, S190's scope, current/previous sample description, and write-sector reset claim are supported by the reopened v12.8.0 source. For precision, the draft names the excluded path as the non-extended basic-stat path rather than the less-specific default report. The basic path's separate calculation is also in the source. S190's earlier in-place scope, anchor, and teaches changes are recorded at `.ufo/waves/round-35/w2/ScoutAppendDebt.md:49`; that report classifies the changes as real content and says they were not logged old-to-new.

## Provenance and commands

- The frozen contract identifies lane entry tip `6bd57097f7ab2b471b4593ed2019c980b1368c68` at `.ufo/waves/round-36/contract.md:3`.
- `timeout 120s git -C /home/vgpnk/Projects/shokunin/mori-shokunin show 6bd57097:corpus/SOURCES.md | grep '^| S190 '` returned the tip row: `sysstat iostat.c at v12.8.0`, code/A, mined, opened `2026-10-23`, recheck `on-release`, used-by `corpus/knowledge/disk-write-rate-r33.md`; its tip scope, anchor and teaches are carried forward below.
- `timeout 120s git -C /home/vgpnk/Projects/shokunin/mori-shokunin show 62db24c0:corpus/SOURCES.md | grep '^| S190 '` returned the first-published row. It had scope about forming the write-sector rate and what it prints when the current count is lower; anchor `iostat.c:1151-1152,1516-1517`; teaches said it prints a write-sector rate of 0.0. `... show 62db24c0^:corpus/SOURCES.md | grep '^| S190 '` returned no match (pipeline exit 1), so the row was absent from that parent.
- The commit named for the in-place rewrite in the spot-check is `ab8f4cfe` (`ScoutAppendDebt.md:49`). `timeout 120s git -C /home/vgpnk/Projects/shokunin/mori-shokunin show ab8f4cfe^:corpus/SOURCES.md | grep '^| S190 '` returned the initial row; `... show ab8f4cfe:corpus/SOURCES.md | grep '^| S190 '` returned the revised cells reproduced in the tip row.
- `timeout 120s git -C /home/vgpnk/Projects/shokunin/mori-shokunin cat-file -e 6bd57097:corpus/knowledge/disk-write-rate-r33.md && printf 'tip path exists\\n'` printed `tip path exists`.
- Opened ordinarily with `curl` from `https://raw.githubusercontent.com/sysstat/sysstat/v12.8.0/iostat.c`; final HTTP status was `200`, response `content-length` was `71360`. Saved body: `/fast/scratch/hyaku/mori-r36/SupS190/S190.src`; SHA-256 `f099229c0051be9538f220d63fe7953247ee947f112d367ff647d791953b9dce` (`sha256sum` output). No challenge or retry was needed.
- `timeout 120s date -u +%FT%TZ` returned `2026-10-23T12:07:06Z`.

## Gate evidence

Quotes below are contiguous source excerpts (each under 25 words); locations are in the saved response body at `/fast/scratch/hyaku/mori-r36/SupS190/S190.src`.

- `iostat.c:1444-1464 (write_ext_stat)`, lines 1456-1457: `* @ioi Current sample statistics.` / `* @ioj Previous sample statistics.` Function signature at lines 1462-1464: `void write_ext_stat(unsigned long long itv, int fctr, int hpart, struct io_device *d, struct io_stats *ioi, struct io_stats *ioj, int tab, char *dname)`.
- `iostat.c:1516-1517`: `xios.wsectors = ioi->wr_sectors < ioj->wr_sectors ? 0.0 : S_VALUE(ioj->wr_sectors, ioi->wr_sectors, itv);`
- `iostat.c:1602-1615 (write_plain_basic_stat)`, line 1614: `wsectors = S_VALUE(ioj->wr_sectors, ioi->wr_sectors, itv);`
- `iostat.c:1728-1755 (write_basic_stat)`, lines 1753-1754: `write_plain_basic_stat(itv, fctr, ioi, ioj, dname, rd_sec, wr_sec, dc_sec);`
- `iostat.c:1941-1945`: `if (DISPLAY_EXTENDED(flags)) { write_ext_stat(itv, fctr, h, d, ioi, ioj, tab, dev_name); } else { write_basic_stat(itv, fctr, d, ioi, ioj, tab, dev_name); }`

DRAFT Gate line:

```text
Gate — https://raw.githubusercontent.com/sysstat/sysstat/v12.8.0/iostat.c; access 2026-10-23; HTTP 200; sha256 f099229c0051be9538f220d63fe7953247ee947f112d367ff647d791953b9dce; quotes: iostat.c:1456-1457 `* @ioi Current sample statistics.` / `* @ioj Previous sample statistics.`; iostat.c:1516-1517 `xios.wsectors = ioi->wr_sectors < ioj->wr_sectors ? 0.0 : S_VALUE(ioj->wr_sectors, ioi->wr_sectors, itv);`; iostat.c:1614 `wsectors = S_VALUE(ioj->wr_sectors, ioi->wr_sectors, itv);`; iostat.c:1753-1754 `write_plain_basic_stat(itv, fctr, ioi, ioj, dname, rd_sec, wr_sec, dc_sec);`; iostat.c:1941-1945 `if (DISPLAY_EXTENDED(flags)) { write_ext_stat(itv, fctr, h, d, ioi, ioj, tab, dev_name); } else { write_basic_stat(itv, fctr, d, ioi, ioj, tab, dev_name); }`; decision supported.
```

## Draft superseding row

The tip content is supported; the row makes the non-extended/basic-stat wording explicit and adds its source locators so the separate calculation is evidenced. It keeps the tip's source, kind, tier, status, opened date, recheck and single used-by path. The proposed `S2NN` is a placeholder.

DRAFT `corpus/SOURCES.md`:

```text
| S2NN | sysstat iostat.c at v12.8.0 — https://raw.githubusercontent.com/sysstat/sysstat/v12.8.0/iostat.c | code | A | the extended-statistics output path of iostat 12.8.0 (write_ext_stat) only: current and previous samples and the write-sector value when the current count is lower; not the non-extended basic-stat path | iostat.c:1444-1464,1516-1517 (write_ext_stat); 1602-1615 (write_plain_basic_stat); 1728-1755 (write_basic_stat); 1941-1945; tag v12.8.0 | supersedes S190 — In the extended-statistics output path, iostat labels ioi as the current sample and ioj as the previous sample and sets the write-sector value to 0.0 when the current sectors-written count is lower; the non-extended basic-stat path calculates wsectors separately with S_VALUE. | mined | 2026-10-23 | on-release | corpus/knowledge/disk-write-rate-r33.md |
```

## Surfaces and limits

- Written surfaces: this report and `/fast/scratch/hyaku/mori-r36/SupS190/S190.src` (SHA-256 above). No lane source, index or product code was edited; `corpus/knowledge/disk-write-rate-r33.md` was only checked for existence at the tip.
- No tools were installed. No tests, counters, builds or linters were run; this assignment was source-cell verification only.
