# w1 seat report — ExecQuoteFinderErrno (quote inventory: errno.h + Aliyun NAS page)

Seat: ExecQuoteFinderErrno (leaf, godspeed). Scope: quote inventory for
`corpus/evidence/sources-r48/errno.h` and `corpus/evidence/sources-r48/aliyun-nas-quota.html`,
normalised exactly like `count-c2.py` (imported `normalise()`), verified by substring test.

## Files read

- `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-48/contract.md` (P-C2, round shape)
- `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-48/v3-spec.md`
- `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-48/count-c2.py` — `normalise()`
  imported from this file (lines 59-62: strip `<[^>]+>` → space, `html.unescape`, collapse `\s+`
  → single space). Word count computed exactly as the counter (lines 142-143): `q = re.sub(r"\s+", " ", quotes[0]).strip()`, `words = q.split(" ")`.
- `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/evidence/sources-r48/errno.h`
  (kernel v7.2 `asm-generic/errno.h`; EDQUOT line at raw line 107)
- `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/evidence/sources-r48/aliyun-nas-quota.html`
  (page body lines 167-216; the article also appears once more inside the escaped
  `window.__ICE_APP_DATA__` JSON on raw line 75 — a `<script>`-embedded copy)

## Result: 8 candidate quotes, all PASS (6-25 words, substring-located)

Verification command (run with `TMPDIR=/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r48-ExecQuoteFinderErrno`):

```
python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r48-ExecQuoteFinderErrno/verify_quotes.py
```

Output (exit 0):

```
#    file   words   occ PASS/FAIL
1    errno.h     6     1 PASS
2    errno.h     7     1 PASS
3    errno.h     7     1 PASS
4    aliyun     8     2 PASS
5    aliyun    11     2 PASS
6    aliyun     7     2 PASS
7    aliyun    11     2 PASS
8    aliyun     7     2 PASS
ALL PASS
exit=0
```

`occ` = number of times the quote occurs in the normalised committed copy. The two
`aliyun` occurrences are one in the rendered body and one in the embedded JSON copy (offsets
below), so every quote is genuinely visible on the page.

## Quote table

| # | Source copy | Quote (backticked span, exactly as it would appear in the entry cell) | Topic | Words (counter) | Occurrences in normalised copy |
|---|---|---|---|---|---|
| 1 | errno.h | `EDQUOT 122 /* Quota exceeded */` | EDQUOT = 122 + its comment line | 6 | 1 |
| 2 | errno.h | `ESTALE 116 /* Stale file handle */` | neighbour ESTALE line (context) | 7 | 1 |
| 3 | errno.h | `EREMOTEIO 121 /* Remote I/O error */` | neighbour EREMOTEIO line (context) | 7 | 1 |
| 4 | aliyun-nas-quota.html | `dd: closing output file '/data/1G.txt': Disk quota exceeded` | directory quota write error (`Disk quota exceeded`) | 8 | 2 (offsets 5002, 15296) |
| 5 | aliyun-nas-quota.html | `验证目录配额限制 由于以 subpath 方式挂载的 NAS 动态存储卷开启了目录配额功能，且声明容量为 20 GiB，因此当挂载目录下写入的数据超过 20 GiB 时，系统会提示磁盘超出配额。` | when the write error is triggered (subPath dir quota, 20 GiB claim) | 11 | 2 (4438, 14732) |
| 6 | aliyun-nas-quota.html | `单击 配额管理 。在 配额管理 页面可以看到已自动生成对应的目录配额，单击 管理配额 可查看详细信息。` | where quota state is viewed (配额管理 page) | 7 | 2 (4360, 14654) |
| 7 | aliyun-nas-quota.html | `默认情况下，在 ACK 集群中挂载 NAS 存储卷时，PVC 中声明的 storage 并不会生效，PV 中实际可用的容量为 NAS 文件系统的所有容量` | enforcement scope: PVC-declared `storage` NOT enforced unless directory quota enabled | 11 | 2 (1208, 11593) |
| 8 | aliyun-nas-quota.html | `如果 allowVolumeExpansion 参数配置为 true ， volumeCapacity 的参数配置将不会生效，目录配额会始终开启。` | enforcement scope: directory quota stays on when `volumeCapacity` ineffective | 6 | 2 (2635, 12988) |

All 8 quotes are pairwise-distinct strings (uniqueness requirement satisfied). All are within
6-25 words as the counter computes them. Chinese spans reach 6+ words by including the page's
space-separated mixed ASCII tokens (`NAS`, `PVC`, `storage`, `subPath`, `20 GiB`,
`allowVolumeExpansion`, `volumeCapacity`, `true`, `ACK`, `Disk quota exceeded`); no Chinese-only
span can reach 6 words because the page's Chinese runs are single whitespace-separated tokens —
no fallback to a nearest English span was needed. Quotes keep the original characters for all
Chinese text. Only one backtick span per quote cell.

## Notes for the L1 integrator

- Quote cells must contain exactly one backticked span (`SPAN.findall` count = 1), and the cell
  after backtick-stripping must equal the quote (the counter does not strip inner text of the
  cell beyond `q = re.sub(r"\s+", " ", quotes[0]).strip()`).
- The claim cell needs ≥ 5 whitespace-separated words (`len(cells[0].split()) >= 5`).
- S-ids are assigned by the document (renumbered); the source cell cites those ids, and each
  SOURCES.md row must be mined, opened 2026-10-25, carry the frozen URL, and list the entry in
  `used-by` (counter lines 158-160). None of that is this seat's call.
- Quotes 4-8 also exist inside the escaped JSON copy of the article (`window.__ICE_APP_DATA__`);
  that does not affect P-C2 (substring test on the normalised committed copy — one occurrence is
  in the rendered body). If a reviewer wants body-only provenance, body offsets are the second of
  the two listed.

## Scratch / tooling

- Scratch: `/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r48-ExecQuoteFinderErrno/`
  (`dump_windows.py`, `verify_quotes.py`). Script below in the fenced block.
- No tools installed or upgraded (nothing needed; the generic-rules install authorization was
  not exercised).

### Verification script (as run)

```python
#!/usr/bin/env python3
"""Verify quote candidates the way count-c2.py does: normalise() + substring test.

Word count = len(q.split(" ")) after re.sub(r"\\s+", " ", span).strip() (counter lines 142-143).
"""
import importlib.util
import os
import re
import sys

spec = importlib.util.spec_from_file_location(
    "count_c2",
    "/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-48/count-c2.py",
)
cc2 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cc2)
normalise = cc2.normalise

BASE = "/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/evidence/sources-r48"
errno = open(os.path.join(BASE, "errno.h"), encoding="utf-8").read()
aliyun = open(os.path.join(BASE, "aliyun-nas-quota.html"), encoding="utf-8").read()
n_errno = normalise(errno)
n_aliyun = normalise(aliyun)

CANDIDATES = [
    ("errno.h", n_errno, "EDQUOT 122 /* Quota exceeded */"),
    ("errno.h", n_errno, "ESTALE 116 /* Stale file handle */"),
    ("errno.h", n_errno, "EREMOTEIO 121 /* Remote I/O error */"),
    ("aliyun", n_aliyun, "dd: closing output file '/data/1G.txt': Disk quota exceeded"),
    ("aliyun", n_aliyun,
     "验证目录配额限制 由于以 subpath 方式挂载的 NAS 动态存储卷开启了目录配额功能，且声明容量为 20 GiB，因此当挂载目录下写入的数据超过 20 GiB 时，系统会提示磁盘超出配额。"),
    ("aliyun", n_aliyun,
     "单击 配额管理 。在 配额管理 页面可以看到已自动生成对应的目录配额，单击 管理配额 可查看详细信息。"),
    ("aliyun", n_aliyun,
     "默认情况下，在 ACK 集群中挂载 NAS 存储卷时，PVC 中声明的 storage 并不会生效，PV 中实际可用的容量为 NAS 文件系统的所有容量"),
    ("aliyun", n_aliyun,
     "如果 allowVolumeExpansion 参数配置为 true ， volumeCapacity 的参数配置将不会生效，目录配额会始终开启。"),
]

print("%-4s %-6s %5s %5s %s" % ("#", "file", "words", "occ", "PASS/FAIL"))
ok = True
for i, (fname, ntext, cand) in enumerate(CANDIDATES, 1):
    q = re.sub(r"\s+", " ", cand).strip()
    words = len(q.split(" "))
    occ = ntext.count(q)
    good = 6 <= words <= 25 and occ >= 1
    ok = ok and good
    print("%-4d %-6s %5d %5d %s" % (i, fname, words, occ, "PASS" if good else "FAIL"))
    if not good:
        print("   quote repr:", repr(q))
print("ALL PASS" if ok else "SOME FAIL")
sys.exit(0 if ok else 1)
```

## Risks / blockers

- None. All 8 candidates verified; exit 0. Entry assembly, SOURCES rows and S-ids are for the
  document/L1 (`used-by` must list the entry path `corpus/knowledge/quota-observability-r48.md`).
- UNVERIFIED: nothing — every claim above is tool output of the run shown.
