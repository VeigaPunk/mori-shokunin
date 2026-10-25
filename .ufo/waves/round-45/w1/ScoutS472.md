# ScoutS472 — independent reopening of registry row S472 (Arch `proc.5.zh_TW`)

Seat: leaf scout, round 45 wave 1. Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin`.
Question: can the source behind `corpus/SOURCES.md:251` (S472,
`https://man.archlinux.org/man/proc.5.zh_TW`) be reopened — the round-44 verifier
could not (ECONNRESET) — and does the page carry the quote the lane records, and
does it say anything the entry `corpus/knowledge/pid-probe-conclusion-r44.md`
does not already claim?

## Verdict

`source-reopened` + `quote-present`.

- **`source-reopened`** — the fetch succeeded on the first attempt, HTTP 200,
  default `curl` flags (no `--http1.1` workaround). The round-44 verifier's
  ECONNRESET did not reproduce; the source is reachable from this host.
- **`quote-present`** — the sentence the lane carries is on the page. Content is
  identical after whitespace normalisation; **not byte-identical**: the lane
  rendered two ASCII punctuation marks as fullwidth (details below). The page
  states nothing that contradicts the entry, and adds two statements the entry
  does not claim (both outside its claim, neither load-bearing for FR5).

## Fetch receipt

| field | value |
|---|---|
| URL | `https://man.archlinux.org/man/proc.5.zh_TW` |
| command | `curl -fsSL --max-time 40 -o proc.5.zh_TW.html -w 'HTTP=%{http_code} BYTES=%{size_download} CT=%{content_type}\n' '<url>'` |
| exit | 0 |
| HTTP status | **200** |
| `size_download` | **61889** bytes |
| content-type | `text/html; charset=utf-8` |
| fetched-at | **2026-10-25T07:41:18-03:00** = `2026-10-25T10:41:18Z` (file mtime); receipt printed 10:41:22Z |
| sha256 (raw bytes) | **`b8ede81db8d462b46f5312b392caab7c5fe8d125057ca6093c2d3152efba8be7`** |
| size on disk / sha recheck | 61889 bytes, same digest re-run at 10:42:19Z |
| decoded-text sha256 | `ad23958d02652b76927eae53a1c846ca0bd5ea6bdf6c4245cb3baef2fa0f868f` |
| decode | `html.unescape(raw)`; raw 61889 bytes / 61861 chars → decoded 39488 bytes / 30674 chars |
| encoding | numeric character references: **4490** entity tokens, **530** distinct (e.g. `&#x7A0B;`), so the Chinese must be entity-decoded before searching (a raw-string search for the quote fails) |

Scratch copy: `.ufo/waves/round-45/tmp/ScoutS472/proc.5.zh_TW.html` (under the
wave `tmp/`, `TMPDIR` set there; nothing written outside the report and that
scratch dir).

## Location

- HTML: `<dt id="cmdline"><a class="permalink" href="#cmdline"><i>cmdline</i></a></dt>`
  — **raw line 90**, raw byte offset 4124, decoded char offset 3251.
- Section path: `描述` → `/proc` → `[number]` → **`cmdline`**. The page's
  directory placeholder is `[number]`, not `[pid]`; the anchor id is exactly
  `cmdline`. (This is the page's `/proc/[number]/cmdline` file entry.)

## The sentence, in the page's own characters

Decoded block as the page carries it (line breaks are the page's; punctuation is
ASCII `,` and `.`, not the fullwidth forms):

```
      如果該程序已經
      被交換出記憶體,
      或者該程序已經僵死,
      那麼就沒有
      任何東西在該檔案裡,
      這時候對該檔案的讀操作將返回零
      個字元.
```

Whitespace-normalised single line (what a browser renders):

```
如果該程序已經 被交換出記憶體, 或者該程序已經僵死, 那麼就沒有 任何東西在該檔案裡, 這時候對該檔案的讀操作將返回零 個字元.
```

Codepoints of the non-Han characters in that sentence:
`0x2c` (記憶體,) `0x2c` (僵死,) `0x2c` (檔案裡,) `0x2e` (end). No fullwidth
comma and no `。` anywhere in it.

**Non-space character count: 59** — 55 Han characters + three U+002C commas +
one U+002E period. Excluding punctuation: **55**.

## Does the quote the lane's registry carries appear on the page?

The lane's English registry cell (`corpus/SOURCES.md:251`, `teaches`) reads:

> A swapped-out or zombie process leaves nothing in the cmdline file and the read
> returns zero characters — a translation-level statement, not current upstream.

That is an accurate rendering of the page, and the anchor cell 「cmdline」段
matches the located entry.

The lane's **Chinese** quote lives in `corpus/lessons/round-44.md:26-28` and in
`corpus/knowledge/pid-probe-conclusion-r44.md` ("…the zombie case in the same
breath as the swap-out case: 「…」"). Both carry:

```
如果該程序已經被交換出記憶體, 或者該程序已經僵死, 那麼就沒有任何東西在該檔案裡，這時候對該檔案的讀操作將返回零個字元。
```

Comparison against the page: whitespace-normalised, the two strings differ in
exactly **two characters** (both punctuation substitutions, everything else
identical):

| offset in sentence | page | lane | note |
|---|---|---|---|
| after `該檔案裡` | `,` **U+002C** | `，` **U+FF0C** | ASCII comma rendered as fullwidth |
| sentence end | `.` **U+002E** | `。` **U+3002** | ASCII full stop rendered as ideographic |

So: **the quote is present in content, not byte-exact** — two punctuation marks
were modernised, nothing lexical. If "present" means byte-for-byte inside the
lane's `「」`, the honest answer is "present modulo those two substitutions"; if
it means the sentence the lane quotes exists on the page, the answer is yes.

The `comm` sentence the entry also attributes to S472 —
「該檔案是否可見取決於該檔案是否已被交換出記憶體」 — **is present and exact**
(modulo a page line break inside `可` / `見`), in the `comm` entry at raw line
267:

> 該檔案是否可\n      見取決於該檔案是否已被交換出記憶體.

## Count discrepancy in the lane record (errata for the L1 — not edited)

`corpus/lessons/round-44.md:28` records **(44 non-space characters)** for the
cmdline quote. Measured on the reopened page and on the lane's own string: **59**
(55 Han + 4 punctuation). The number 44 is exactly the non-space count of the
**suffix** beginning 「或者該程序…」 (verified: that suffix is 44), i.e. the count
covers only the second clause while the quoted span starts at 「如果該程序」. The
entry `pid-probe-conclusion-r44.md` does not carry a count, so only the round-44
lesson is affected. Registry and entry are append-only; flagged here for the L1.

## Does the page say anything the entry does not already claim?

**Yes — two statements in the same `cmdline` entry, both unclaimed, neither
contradicting:**

1. 「該檔案儲存了程序的完整命令列.」 — the file stores the process's complete
   command line. (The entry says nothing about what a non-empty `cmdline`
   contains.)
2. 「該檔案以空字元 null 而不是換行符作為結束標誌.」 — the file is terminated by
   a NUL character, not by a newline. (The entry's boundary section discusses what
   S170's rendered contract states, but never states the terminator itself.)

Everything else the entry attributes to S472 checks out on the page, so the page
adds **no unclaimed substance bearing on the FR5 claim**:

- The swap-out/zombie → empty-file → zero-character-read rule: present verbatim
  (above).
- The `comm`-file swap-out sentence: present (above).
- The state alphabet stops at `T`: page has `";RSDZT";` with `Z 是僵死, T
  是被跟蹤或被停止`. **No `X`, no `I`** — the entry's boundary ("S472's alphabet
  stops at T and predates `X` entirely") is confirmed.
- `1.3.11` provenance: 「本手冊頁基本上是針對 Linux 1.3.11 核心」 and 「最後更新也是
  針對 Linux 1.3.11.」
- `2000-11-26` last Chinese update: page heading `[中文版最新更新]`, body
  `<b>2000/11/26</b>` (the entry writes it ISO-style).
- `foot-date` **22 July 1996**, `Linux Programmer's Manual`; package
  `extra/man-pages-zh_tw` version **1.6.4.5-1**, upstream
  `github.com/man-pages-zh/manpages-zh` (page does not claim a Debian
  `manpages-ja`-style package — that boundary is about S471, unaffected).

Nothing on the page contradicts the entry. The entry's "different objects"
divergence (S472's `comm` file vs S471's `stat` comm field) is exactly what the
two pages show; this seat did not re-open S471.

## Remaining unknowns

- Whether the page ever rendered differently (Arch ships `man-pages-zh_tw
  1.6.4.5-1` today; a package bump would move the digest, so the digest above is
  the anchor for this fetch, not a permanent one).
- The entry's "1.3.11-era" label is grounded by the page's own 遵循 section; the
  "last Chinese update 2000-11-26" is grounded as `2000/11/26`, but the page does
  not state the date's timezone or whether it is a translation-revision date.
- Not checked (out of this seat's question): S471's page, the entry's mm-less
  measurement receipt, and the registry's other rows.

## For the L1 to append to the round lesson (copy-paste)

```markdown
- S472 — `https://man.archlinux.org/man/proc.5.zh_TW` — **`source-reopened` +
  `quote-present`** (round-45, ScoutS472). `curl -fsSL --max-time 40`, first
  attempt, exit 0, HTTP 200, `text/html; charset=utf-8`, 61889 bytes, sha256
  `b8ede81db8d462b46f5312b392caab7c5fe8d125057ca6093c2d3152efba8be7`, fetched
  2026-10-25T10:41:18Z. Entity-decoded (4490 numeric refs, 530 distinct) and
  located at `<dt id="cmdline">`, raw line 90, section `cmdline` (under
  `描述` → `/proc/[number]`). Quote: 「如果該程序已經被交換出記憶體, 或者該程序
  已經僵死, 那麼就沒有任何東西在該檔案裡, 這時候對該檔案的讀操作將返回零個字元.」
  — present; the lane's rendering differs in two punctuation marks only
  (page U+002C `,` → lane U+FF0C `，` at 檔案裡; page U+002E `.` → lane U+3002 `。`
  at the end). Non-space count **59** (55 Han + 3 commas + 1 period); the
  round-44 lesson's "(44 non-space characters)" is the suffix-only count
  (「或者…」 onward) — errata for the L1, not edited here. The page adds two
  unclaimed statements (完整命令列 stored; NUL- rather than newline-terminated),
  contradicts nothing the entry claims, confirms `";RSDZT"` with no `X`/`I`,
  and carries `1.3.11`, `2000/11/26`, foot-date 22 July 1996, package
  `extra/man-pages-zh_tw 1.6.4.5-1`. The round-44 verifier's ECONNRESET did not
  reproduce.
```

## Reproduce

```bash
cd /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-45/tmp/ScoutS472
curl -fsSL --max-time 40 -o proc.5.zh_TW.html \
  'https://man.archlinux.org/man/proc.5.zh_TW'
sha256sum proc.5.zh_TW.html          # b8ede81d… → 61889 bytes
python3 - <<'PY'
import html,re
raw=open('proc.5.zh_TW.html',encoding='utf-8').read()
txt=html.unescape(raw)
a=txt.find('<dt id="cmdline"'); b=txt.find('<dt id="cwd"')
body=re.sub(r'<[^>]+>','',txt[a:b])
print(' '.join(body.split()))
q=re.search(r'如果該程序.*?個字元\.',' '.join(body.split())).group(0)
print(q, len(re.sub(r'\s','',q)))
PY
```

No tools installed or upgraded. No file outside this report and
`.ufo/waves/round-45/tmp/ScoutS472/` was written.
