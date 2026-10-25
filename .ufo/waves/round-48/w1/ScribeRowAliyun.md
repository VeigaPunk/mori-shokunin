# ScribeRowAliyun — round 48 w1: draft lane SOURCES row S482 (Aliyun NAS directory quota)

Seat: ScribeRowAliyun (leaf; no subagents). Lane: mori-shokunin. Round: 48, wave w1.
Scope: draft the lane `corpus/SOURCES.md` row for
`https://help.aliyun.com/zh/nas/user-guide/set-quotas-on-the-subdirectories-of-nas-nfs-volumes`
as id **S482** (kind `docs`, tier A), and report a Gate block.

## What I opened

- Frozen contract: `mori-shokunin/.ufo/waves/round-48/contract.md` (C2 predicate; four frozen
  URLs in `count-c2.py` COPIES, including this URL → committed copy
  `corpus/evidence/sources-r48/aliyun-nas-quota.html`, sha256
  `747fef1bcc8c6d6c18908f4534879922bebdaece1a476831d48be93c4e22719f`).
- `count-c2.py` source (quote rule: `SPAN.findall`, `q.split(" ")`, 6–25 whitespace tokens;
  source-row checks: 11 cells, URL substring in cell 2, status `mined`, opened `2026-10-25`,
  entry path listed in `used-by` cell 11).
- Committed copy `corpus/evidence/sources-r48/aliyun-nas-quota.html` (269 lines).
- Live URL fetched 2026-10-25 with a browser User-Agent.
- Staged assimilation package `/home/vgpnk/Projects/shokuknow/merge/mori/` (read-only):
  `SOURCES.append.md` row S479 already proposes the same URL (different scope: `Disk quota
  exceeded` on the failing write and the console 配额管理 view; fetched 2026-10-23). Note for
  integration: the lane S482 row below is the round-48 re-opened row for C2; it does not
  duplicate staged S479's claims.

## Commands (evidence)

### 1. Local committed copy hash (matches frozen sha256)

```
$ sha256sum mori-shokunin/corpus/evidence/sources-r48/aliyun-nas-quota.html
747fef1bcc8c6d6c18908f4534879922bebdaece1a476831d48be93c4e22719f  .../aliyun-nas-quota.html
```
exit 0. Matches `count-c2.py` COPIES digest for this URL.

### 2. Live fetch with browser User-Agent (scratch, TMPDIR=…/.scratch/r48-ScribeRowAliyun)

```
$ TMPDIR=/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r48-ScribeRowAliyun \
  curl -sSL -A 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36' \
  -o .../.scratch/r48-ScribeRowAliyun/aliyun-nas-quota-live.html \
  -w 'http_code=%{http_code} size=%{size_download} url=%{url_effective} final=%{num_redirects}\n' \
  https://help.aliyun.com/zh/nas/user-guide/set-quotas-on-the-subdirectories-of-nas-nfs-volumes
http_code=200 size=117506 url=https://help.aliyun.com/zh/nas/user-guide/set-quotas-on-the-subdirectories-of-nas-nfs-volumes final=0
```
exit 0. Page served HTTP 200 on 2026-10-25 (no redirect).

### 3. Page's own revision/date text (committed copy and live response agree)

Committed copy and live response both carry:
- `<meta name="last-modified" content="2026-10-13T14:26:17+08:00">`
- `<meta name="date" content="2023-01-11T04:26:20+08:00">`
- visible header `<span class="Header--updateTime--YXGPhcZ">更新时间：</span>` (time rendered by JS;
  the meta values are the server-provided revision text)
- `docid="2856790"` on the taskbody element.

Live fetch on 2026-10-25 confirms both meta values unchanged (verified by extraction from the
live scratch copy). The page's own revision text therefore states last-modified
2026-10-13T14:26:17+08:00.

### 4. Heading anchor

- `<h1>配置NAS NFS存储卷容量</h1>` — no `id` attribute on the h1.
- Document root anchor: `<main id="task-2287334">` (the h1's surrounding content element).
- Named section heading anchors (h2/h3 with ids):
  - `#e9eea3ad839hn` — 使用场景
  - `#d41e26` — 前提条件
  - `#f44c5ec5bc3au` — 验证目录配额限制
  - `#878e57d55btaw` (h3) — 步骤二：创建应用并挂载 NAS 存储卷
- Anchor cell below cites the h1 (no id), `main#task-2287334`, and the two section anchors.

### 5. Located quote (original Chinese; word count rule)

Count rule (matches `count-c2.py`): strip tags, decode entities, collapse whitespace
(`normalise`), take the backticked span, then count tokens as `span.split(" ")`
(whitespace-delimited); the span must be 6–25 tokens and occur in the committed copy.

Selected quote (the page's shortdesc paragraph, normalized):

```
CSI 组件支持为通用型 NAS 存储卷的子目录设置配额限制。使用 subPath 方式挂载 NAS 子目录时，可启用目录配额功能，限制子目录容量，提升资源利用率。当子目录存储卷达到配额上限时，可通过更新 PVC 的 storage 实现在线扩容，无需中断业务。
```

Verified programmatically:
- `quote in normalise(committed_copy)` → True
- `quote in normalise(live_copy)` → True
- token count = 12 (`CSI`, `组件支持为通用型`, `NAS`, `存储卷的子目录设置配额限制。使用`,
  `subPath`, `方式挂载`, `NAS`, `子目录时，可启用目录配额功能，限制子目录容量，提升资源利用率。当子目录存储卷达到配额上限时，可通过更新`,
  `PVC`, `的`, `storage`, `实现在线扩容，无需中断业务。`) → within 6–25.

The quote is shortdesc (short description) of the doc, immediately below the h1; it is the
paragraph the page's own `<meta name="description">` repeats verbatim (as preserved in the
committed copy).

## Draft lane SOURCES.md row (S482)

Draft (fenced; for the L1 to integrate — I do not edit `corpus/SOURCES.md`):

```markdown
| S482 | 配置NAS NFS存储卷容量 — https://help.aliyun.com/zh/nas/user-guide/set-quotas-on-the-subdirectories-of-nas-nfs-volumes | docs | A | Alibaba NAS directory quotas only — the vendor's own statement that a directory-scoped quota is a CSI-mounted NAS subdirectory feature (volumeCapacity: true), the exhausted-quota error a workload sees, and the console 配额管理 view; not mori's own thresholds and not the POSIX or XFS quota syscall surface | h1「配置NAS NFS存储卷容量」(no id), main#task-2287334, section anchors 使用场景#e9eea3ad839hn and 验证目录配额限制#f44c5ec5bc3au; docid 2856790; page meta last-modified 2026-10-13T14:26:17+08:00, date 2023-01-11, both unchanged on live fetch 2026-10-25 | limit: this page documents Alibaba Cloud NAS product semantics — the directory quota is a product feature of NAS NFS volumes mounted via CSI, not a general POSIX quota interface; quotes from this row may ground claims about Alibaba NAS volume behavior only, never about the host's xfs or quota syscall surface | mined | 2026-10-25 | 180d | corpus/knowledge/quota-observability-r48.md |
```

11 columns: `S482 | source | docs | A | scope | anchor | teaches | mined | 2026-10-25 | 180d | corpus/knowledge/quota-observability-r48.md`.
No `|` inside any cell; status `mined`; opened 2026-10-25; recheck `180d`; `used-by` names the
C2 entry path.

## Gate block

```markdown
## Gate — S482 (mined, opened 2026-10-25)
- Local copy `corpus/evidence/sources-r48/aliyun-nas-quota.html` sha256 = frozen value
  747fef1bcc8c6d6c18908f4534879922bebdaece1a476831d48be93c4e22719f (exit 0).
- Live fetch 2026-10-25, browser UA: HTTP 200, 117506 bytes, no redirect; page self-reports
  last-modified 2026-10-13T14:26:17+08:00 (meta date 2023-01-11), unchanged from the committed copy.
- Heading anchor: h1「配置NAS NFS存储卷容量」has no id; content anchor `<main id="task-2287334">`;
  section anchors `#e9eea3ad839hn` (使用场景), `#d41e26` (前提条件), `#f44c5ec5bc3au` (验证目录配额限制).
- Located quote (kept in original Chinese; 12 tokens by the counter's normalise + split(" ") rule,
  within 6–25): `CSI 组件支持为通用型 NAS 存储卷的子目录设置配额限制。使用 subPath 方式挂载 NAS 子目录时，可启用目录配额功能，限制子目录容量，提升资源利用率。当子目录存储卷达到配额上限时，可通过更新 PVC 的 storage 实现在线扩容，无需中断业务。`
  Occurs in both the committed copy and the live copy after tag-strip/entity-decode/space-collapse.
- Verdict: admit S482 as mined, tier A, scope limited to Alibaba NAS directory quotas; the
  teaches cell states that limit (documents another product's semantics).
```

## Notes / limits

- Staged `SOURCES.append.md` S479 (from `/home/vgpnk/Projects/shokuknow/merge/mori/`, read-only)
  proposes the same URL with a different claim set (exhaustion string `Disk quota exceeded` and
  配额管理 view, fetched 2026-10-23). The lane S482 row is distinct in scope (CSI volumeCapacity
  directory-quota feature) and opened 2026-10-25; whether both rows survive is the L1's call.
- UNVERIFIED: none for the row's required facts. I did not run `count-c2.py` end-to-end (entry
  `corpus/knowledge/quota-observability-r48.md` does not exist yet; that is another seat's build).
- I wrote only my report file and scratch under `.scratch/r48-ScribeRowAliyun/`; no production
  file touched.
