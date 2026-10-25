# R48RevEntryErrnoAliyun — round 48 wave w2 falsify review

**Attacked:** rows S481 + S482 (claims-table lines 37–40) and the boundary lines 57–60 for S483/S484
of `corpus/knowledge/quota-observability-r48.md` at `e4dfff32d4f97c7ef250e9a7538fa75d4f284492`,
against the committed copies under `corpus/evidence/sources-r48/` (`errno.h`,
`aliyun-nas-quota.html`, `arch-mips-errno.h`, `arch-sparc-errno.h`), plus the seat-asked checks:
Aliyun quotes are rendered page text not script/JSON, and `Disk quota exceeded` is the vendor
example not a general rule.

**Verdict: HOLDS.** All four in-scope rows verified; no defect found.

## Row verdicts

### S481 — generic errno header — HOLDS

- Committed copy `errno.h:107`: `#define\tEDQUOT\t\t122\t/* Quota exceeded */`. Normalised
  (whitespace collapsed) this is the quote cell `` `#define EDQUOT 122 /* Quota exceeded */` ``
  verbatim. Line number cited in the source line (line 107) matches.
- Claim "the generic Linux ABI header gives EDQUOT the number 122" follows directly.
- Live upstream check 2026-10-25: `curl raw.githubusercontent.com/torvalds/linux/v7.2/
  include/uapi/asm-generic/errno.h` → EDQUOT at line 107, value 122 (exit 0). Copy is current
  against the pinned tag; sha256 `66a5ad60…be` equals the C2 pin.

### S482 — Aliyun NAS page, three rows — HOLDS

- **Failing-write string** (line 38): the rendered HTML (line 213) contains
  `<pre …><code>dd: closing output file '/data/1G.txt': Disk quota exceeded</code></pre>` —
  the quote is verbatim rendered page text, preceded by `预期返回如下，提示超出磁盘配额` and the
  write command `dd if=/dev/zero of=/data/1G.txt bs=1M count=1024`. The identical string is also
  embedded once in the `window.__ICE_PAGE_PROPS__` JSON at line 75 (2 total occurrences); the
  rendered occurrence exists independently, so the quote is not JSON-only. Claim "in the vendor's
  directory-quota example the failing write prints the English string" is exactly what the page
  shows: the string appears nowhere else on the page (`grep -o 'quota exceeded[^<]*'` → 2 hits,
  both the same `dd` sentence, JSON + render).
- **`subPath` feature row** (line 39): the rendered shortdesc (line 167) contains
  `CSI 组件支持为通用型 NAS 存储卷的子目录设置配额限制。使用 subPath 方式挂载 NAS 子目录时，可启用目录
  配额功能，限制子目录容量，提升资源利用率。` after tag-strip/whitespace-collapse — quote verbatim,
  rendered body text (also duplicated in `<meta name="description">` line 35, `og:description`
  line 42, and JSON line 75). The claim's "mounted by `subPath`" glosses 使用 subPath 方式挂载
  accurately.
- **Console-page row** (line 40): the rendered HTML contains, at both line 213 and line 216,
  `，然后单击 配额管理 。在 配额管理 页面，单击目录对应的 管理配额 可查看详细信息。` — the exact comma
  variant quoted in the table. (The first `配额管理` is a `<b class="uicontrol">` button, the
  second a `<b class="uicontrol">` page title, both stripped to text.) This passage sits in a
  different list item than the `dd` example, supporting "a separate console page, not in the
  failing write." The JSON embed carries all three variants of this sentence too.
- **"Vendor example, not a general rule" check:** the page contains no other `quota exceeded` /
  `exceed` English phrasing; the only English error string is the `dd` output line. The table
  row is scoped to "the vendor's … example" and the Boundaries section (lines 64–67) already
  limits S482 to a comparison shape — no over-generalisation to fix. [Note: the string happens
  to be glibc's EDQUOT message, which is what the `audit-r11.md` precedent in "What the lane
  held before" reflects; that precedent is cited as lane history, not attributed to S482.]

### S483/S484 boundary claims (lines 57–59) — HOLD

- Committed copies: `arch-mips-errno.h:131` `#define EDQUOT\t\t1133\t/* Quota exceeded */` and
  `arch-sparc-errno.h:43` `#define\tEDQUOT\t\t69\t/* Quota exceeded */` — values and line numbers
  as stated; the mips quote in the boundary text matches the copy after whitespace collapse.
- Live upstream v7.2 check 2026-10-25: mips EDQUOT line 131 = 1133, sparc line 43 = 69
  (both exits 0). Values and line numbers match upstream at the pinned tag.
- Boundary correctly labels both "not in the claims table" in the source lines and draws the
  correct lesson (match the platform constant or symbolic name, never a copied number).
- Side note: sparc line 43 quote text is not reproduced in the boundary (only the line cite) —
  consistent with these being boundary cites, not table quotes; the value is correct.

## Location integrity

- `python3 .ufo/waves/round-48/count-c2.py e4dfff32…` →
  `C2=met claims=15 located=15 quote_missing=0 bad_rows=0 sources=4 source_rows=ok pins=ok provenance=ok` (exit 0).
- Working-tree sha256 of all four in-scope copies equals `git show` at the tip, and `errno.h` /
  `aliyun-nas-quota.html` equal the frozen pins in `count-c2.py` (`66a5ad60…be`,
  `747fef1b…19f`); `arch-mips-errno.h` `006286df…` and `arch-sparc-errno.h` `530c3cc2…` match
  tip and working tree (these two are outside the counter's pin set, as the source lines state).

## Residual risk / verification gaps

- The counter locates quotes anywhere in the page bytes (JSON embed included). Verified here
  that all three S482 quotes also occur in the rendered `<main id="task-2287334">` body, so the
  location is not JSON-only — the stronger property the seat asked about holds.
- Live upstream confirmed for the three errno headers. The Aliyun live page was not re-fetched
  (recheck command in the source header covers it; committed copy verified); the last-modified
  meta (1791872777000 → 2026-10-13) matches the source line's claim — VERIFIED against the copy,
  UNVERIFIED against the live page.
- The claim row for S482 line 40 says "not in the failing write": supported (different list
  item, different `<ol>`), but the page's own structure is the only evidence; no independent
  vendor source. Within scope — flag only.

No installs needed; all checks used system `grep`/`awk`/`curl`/`python3`/`git` (read-only).
