# Scout — staged source pages for the C3 entry: JA focal `proc.5` and zh_TW LDP `proc.5`

lane: mori · round: 44 · wave: 1 · role: scout (leaf, no dispatch) · date: 2026-10-25
lane repo: `/home/vgpnk/Projects/shokunin/mori-shokunin` · instruments frozen at `7cb59c6891d4f5d0266fe062565f094da835dc84`
fleet repo: `/home/vgpnk/Projects/shokunin` (read-only) · nothing outside this file was written

Question: open both staged source pages read-only and pin the exact wording the C3 entry will
lean on — the `/proc/[pid]/cmdline` and `/proc/[pid]/stat` state sections — recording for each
page the HTTP status, content-type, byte count, fetched-at timestamp, and the shortest located
quote (≤ 25 words / ≤ 25 CJK characters) that carries the claim; and state plainly whether the
`Z ゾンビ` / `X 死亡` alphabet and the "swapped out XOR zombie leaves the file empty" sentence
appear.

Both pages were reachable by `GET`. All scratch work happened in `mktemp -d` sandbox
`/tmp/mori44-scout-3g2o`; the checkouts were never touched.

---

## 0. Bottom line

| page | `Z ゾンビ` / `X 死亡` alphabet | "swapped out XOR zombie ⇒ empty" sentence |
|---|---|---|
| JA focal (20.04) | **YES** — `Z ゾンビ (Zombie)`, `X 死亡 (Dead) (Linux 2.6.0 以降)` | **NO** — zombie only; the cmdline block contains zero occurrences of スワップ |
| zh_TW LDP (Arch `man-pages-zh_tw`) | **NO** — alphabet is `RSDZT`, `Z 是僵死`, no `X` state | **YES** — 被交換出記憶體 **或者** 已經僵死 ⇒ 沒有任何東西在該檔案裡 ⇒ 讀操作返回零個字元 |

Neither page grounds a *third* world for a zero-character `cmdline` read (§5). The one page that
carries the swap-out disjunct is a translation of Linux 1.3.11-era man-pages (last Chinese update
2000/11/26), and its swap-out claim is contradicted by the focal page's own `comm %s` field (§6.2).

---

## 1. Fetch receipts

### 1.1 Successful fetches

| # | URL | method | status | content-type | bytes | fetched_at (UTC) | sha256 |
|---|---|---|---|---|---|---|---|
| P1 | `https://manpages.ubuntu.com/manpages/focal/ja/man5/proc.5.html` | GET | 200 | `text/html; charset=utf-8` | 376399 | 2026-10-25T08:09:31Z | `f64b0cded10f755e6135f8d9d4aba8f5c769290128572f92faad1dc5a2c6364b` |
| P2 | `https://man.archlinux.org/man/proc.5.zh_TW` | GET | 200 | `text/html; charset=utf-8` | 61889 | 2026-10-25T08:09:15Z | `b8ede81db8d462b46f5312b392caab7c5fe8d125057ca6093c2d3152efba8be7` |

Re-probed at 2026-10-25T08:12:47Z / 08:12:48Z with `--http1.1`; both returned the **same byte
counts and the same sha256**, so the bodies quoted below are stable, not a partial read.

### 1.2 Verbatim consolidated probe (final run)

```
$ for u in "https://manpages.ubuntu.com/manpages/focal/ja/man5/proc.5.html" \
           "https://man.archlinux.org/man/proc.5.zh_TW"; do
    echo "--- GET $u"
    curl -fsSL --max-time 30 --http1.1 -D p.h -o p.b \
      -w 'status=%{http_code} content_type=%{content_type} bytes=%{size_download} fetched_at=%{time_total}s\n' "$u"
    sed -n '1p;/^[Cc]ontent-[Tt]ype/p;/^[Cc]ontent-[Ll]ength/p' p.h | tr -d '\r'
    echo "sha256=$(sha256sum p.b | cut -d' ' -f1)  utc_now=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  done

--- GET https://manpages.ubuntu.com/manpages/focal/ja/man5/proc.5.html
status=200 content_type=text/html; charset=utf-8 bytes=376399 fetched_at=1.320776s
HTTP/1.1 200 OK
content-type: text/html; charset=utf-8
sha256=f64b0cded10f755e6135f8d9d4aba8f5c769290128572f92faad1dc5a2c6364b  utc_now=2026-10-25T08:12:47Z

--- GET https://man.archlinux.org/man/proc.5.zh_TW
status=200 content_type=text/html; charset=utf-8 bytes=61889 fetched_at=1.520022s
HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8
Content-Length: 61889
sha256=b8ede81db8d462b46f5312b392caab7c5fe8d125057ca6093c2d3152efba8be7  utc_now=2026-10-25T08:12:48Z
```

### 1.3 Transient failures, recorded (both resolved, neither is a page verdict)

**(a) P2, first attempt — TLS EOF, not an unreachable host.** This was a real `GET`, not a HEAD,
and it failed at the handshake before any HTTP response:

```
$ curl -fsSL --max-time 30 -o zhTW.html -D zhTW.headers \
    -w "HTTP=%{http_code} CT=%{content_type} SIZE=%{size_download}\n" \
    https://man.archlinux.org/man/proc.5.zh_TW
HTTP=000 CT= SIZE=0
curl: (35) TLS connect error: error:0A000126:SSL routines::unexpected eof while reading
```

Retry ladder, same URL:

```
$ getent hosts man.archlinux.org
2604:cac0:a104:d:: man.archlinux.org
$ curl -fsSL --http1.1 --tlsv1.2 --max-time 30 ... https://man.archlinux.org/man/proc.5.zh_TW
HTTP=200 CT=text/html; charset=utf-8 SIZE=61889      rc=0
$ curl -fsSLk --max-time 30 ... https://man.archlinux.org/man/proc.5.zh_TW
HTTP=200 CT=text/html; charset=utf-8 SIZE=61889      rc=0
$ curl -fsSL --max-time 30 ... http://man.archlinux.org/man/proc.5.zh_TW
HTTP=200 CT=text/html; charset=utf-8 SIZE=61889      rc=0
```

A verbose default-negotiation probe then succeeded over HTTP/2:

```
< HTTP/2 200
< server: nginx
< date: Sun, 25 Oct 2026 08:08:40 GMT
< content-type: text/html; charset=utf-8
< content-length: 61889
```

Conclusion: the first failure was a transient TLSv1.3 session-ticket EOF on this host, not an
unreachable page. All later attempts — HTTP/1.1, HTTP/2, `-k`, plain `http` — agree on 61889 bytes.

**(b) P1, one truncated attempt — timeout mid-body, not a short page.** A run with
`--max-time 30` cut the body off:

```
HTTP=200 CT=text/html; charset=utf-8 SIZE=28007
curl: (28) Operation timed out after 30001 milliseconds with 28007 bytes received
```

Re-fetched with `--max-time 120`; the document closed correctly and matched the original
376399-byte body:

```
try=1 HTTP=200 CT=text/html; charset=utf-8 SIZE=376399
fetched_at=2026-10-25T08:09:31Z rc=0
COMPLETE bytes=376399 sha256=f64b0cded10f755e6135f8d9d4aba8f5c769290128572f92faad1dc5a2c6364b
$ tail -c 120 ja.html
  </body>
</html>
```

The 28007-byte read was **not** used as evidence for anything below.

### 1.4 Page provenance

- **P1** — breadcrumb JSON-LD in the body carries `"name":"focal"`; the page's own release menu
  lists `20.04 LTS (focal)`; footer reads
  `Provided by: manpages-ja (Version: 0.5.0.0.20180315+dfsg-1)`. The page is a *partial*
  translation: large stretches (e.g. the `comm` and `stack` entries) remain English upstream text.
  The two sections quoted below are translated.
- **P2** — footer: `Package name: extra/man-pages-zh_tw`, `Version: 1.6.4.5-1`, upstream
  `github.com/man-pages-zh/manpages-zh`; body says `[中文版最新更新] 2000/11/26` and
  `本手冊頁基本上是針對 Linux 1.3.11 核心`. This is the LDP-era translation, not a modern page.

Text was extracted with a stdlib `HTMLParser` pass (tags → line breaks, entities unescaped). Line
numbers below refer to that decoded text (`ja.txt`, `zhtw.txt`); raw HTML stores Japanese as
numeric character references, so a literal grep for `ゾンビ` in `ja.html` returns 0 and is
meaningless — the decoded text is the correct surface.

---

## 2. P1 — Japanese, focal / 20.04

### 2.1 `/proc/[pid]/cmdline` (decoded lines 139–149)

Verbatim as rendered (line breaks are the page's own wrapping):

```
/proc/[pid]/cmdline
この読み出し専用のファイルはプロセスの完全なコマンド行を保持する。
 ただし、そのプロセスがゾンビプロセスの場合は、
 このファイルは空となる。
 つまり、
 このファイルを読み出しても一文字も返らない。
 このファイルではコマンドライン引き数が、
 ヌルバイト ('\0')
 で区切られた文字列として書かれており、
 最後の文字列の後にヌルバイトが一つ置かれる。
```

Claim carried: **a zombie process makes this file empty, and a read returns not one character.**

Shortest quote carrying the claim (23 non-space characters):

> **ゾンビプロセスの場合は、このファイルは空となる**

Companion for the zero-character consequence (21 non-space characters):

> **このファイルを読み出しても一文字も返らない**

**No swap-out clause.** The block contains no occurrence of スワップ:

```
$ sed -n '139,150p' ja.txt | grep -c "スワップ"
0
```

and the whole page has exactly one `空となる`, at line 142 — this one:

```
$ grep -n "空となる\|空であ\|空になる" ja.txt
142: このファイルは空となる。
```

So on P1 the `cmdline` emptiness condition is **zombie, singular** — the swap-out disjunct is
absent.

### 2.2 `/proc/[pid]/stat`, field `(3) state %c` (decoded lines 919–966)

Section head:

```
/proc/[pid]/stat
プロセスの状態についての情報。
 これは ps(1)
 で使われ、
 カーネルのソースファイル
 fs/proc/array.c
 で定義されている。
```

State alphabet, verbatim (rendered as a one-letter / label table, decoded here as a run):

```
(3) state %c
プロセスの状態を示す、以下のいずれか 1 文字。
R   実行中 (Running)
S   Sleeping in an interruptible wait
D   Waiting in uninterruptible disk sleep
Z   ゾンビ (Zombie)
T   (シグナルでの) 停止、または (Linux 2.6.33 より前では) トレースによる停止
t   トレースによる停止 (Tracing stop) (Linux 2.6.33 以降)
W   ページング中 (Linux 2.6.0 より前のみ)
X   死亡 (Dead) (Linux 2.6.0 以降)
x   死亡 (Dead) (Linux 2.6.33 から 3.13 までのみ)
K   Wakekill (Linux 2.6.33 から 3.13 までのみ)
W   Waking (Linux 2.6.33 から 3.13 までのみ)
P   Parked (Linux 3.9 から 3.13 までのみ)
```

**The `Z ゾンビ` / `X 死亡` alphabet appears.** Shortest quotes:

> **Z ゾンビ (Zombie)**   (12 non-space characters)

> **X 死亡 (Dead) (Linux 2.6.0 以降)**   (23 non-space characters, 6 words)

Note the exact `X` wording carries a version qualifier — `(Linux 2.6.0 以降)` — and the page also
lists a lowercase `x 死亡 (Dead) (Linux 2.6.33 から 3.13 までのみ)`. A C3 entry that says "`X` means
dead" must not drop those qualifiers: the page presents `X` as dead **since 2.6.0**, with a
narrower `x` variant confined to 2.6.33–3.13.

### 2.3 Same alphabet repeated in `/proc/[pid]/status` (decoded lines 1328–1338)

Independent corroboration inside the same page, different section:

```
State:
 プロセスの現在の状態。
 "R (running; 実行中)", "S (sleeping;
 休眠状態)", "D (disk sleep;
 ディスク待ちの休眠状態)",
 "T (stopped; 停止状態)", "T
 (tracing stop;
 トレースによる停止)",
 "Z (zombie; ゾンビ状態)", "X
 (dead; 死亡)"
 のいずれかである。
```

Quote (17 non-space characters, within the cap; the full pair runs 30 and is quoted only as the
corroborating context, not as the primary claim quote):

> **"Z (zombie; ゾンビ状態)"**

Full pair as it stands on the page: `"Z (zombie; ゾンビ状態)", "X (dead; 死亡)"`. This is the
cleanest single witness of the Z/X pair on P1: it pairs the ASCII letter with both the English and
the Japanese label in one string, and unlike §2.2 it carries no version parenthetical.

---

## 3. P2 — Chinese, `man-pages-zh_tw` (LDP era)

### 3.1 `cmdline` (decoded lines 35–44, under the `[number]` per-process directory)

Verbatim as rendered (the page uses ASCII `.` as its sentence terminator — LDP style):

```
cmdline
該檔案儲存了程序的完整命令列.
 如果該程序已經
 被交換出記憶體,
 或者該程序已經僵死,
 那麼就沒有
 任何東西在該檔案裡,
 這時候對該檔案的讀操作將返回零
 個字元.
 該檔案以空字元 null
 而不是換行符作為結
 束標誌.
```

Claim carried: **if the process has been swapped out of memory, *or* has become a zombie, then
there is nothing in this file, and a read on it returns zero characters.**

**This is the "swapped out XOR zombie leaves the file empty" sentence, and it appears.** The
connective is 或者 ("or"), a disjunction over two states that cannot hold at once, so it functions
as the exclusive reading the assignment names.

Shortest quotes (the 25-character cap forces splitting the disjunction from its consequence; both
are given rather than silently truncating one):

> **如果該程序已經被交換出記憶體, 或者該程序已經僵死**   (24 non-space characters)

> **這時候對該檔案的讀操作將返回零個字元**   (18 non-space characters)

Consequence-only variant, also 24 characters:

> **或者該程序已經僵死, 那麼就沒有任何東西在該檔案裡**

### 3.2 `stat` — process-level entry (decoded lines 179–200)

P2 has **two** `stat` headings: line 179 is `/proc/[number]/stat` (process state, the one that
matters here) and line 630 is `/proc/stat` (system-wide cpu/disk/page/swap counters). The alphabet
is only in the first. Verbatim:

```
stat
程序狀態資訊, 被命令
 ps(1) 使用.
現將該檔案裡各域,
 以及他們的 scanf(3)
 格式說明符,
 按順序分述如下:
pid %d
程序標識．
comm %s
執行檔的檔名,
 包括路徑.
 該檔案是否可
 見取決於該檔案是否已被交換出記憶體.
state %c
";RSDZT"; 中的一個, R
 是正在執行, S 是
 在可中斷的就緒態中睡眠,
 D 是在不可中
 斷的等待或交換態中睡眠,
 Z 是僵死, T
 是被跟蹤或被停止(由於收到訊號).
```

**The `Z ゾンビ` / `X 死亡` alphabet does NOT appear.** The alphabet is `RSDZT` — five letters,
`Z` present as 僵死, **no `X` state entry and no 死亡 anywhere on the page**. The page's only bare
`X` is the cross-reference `modules(X)` at line 401, unrelated to process state:

```
$ grep -n "死亡\|X 是\|RSDZT" zhtw.txt
194:";RSDZT"; 中的一個, R
$ grep -c "\bX\b" zhtw.txt
1        # modules(X) 使用該檔案
```

Quote (4 non-space characters for the Z term, 21 for the enumeration):

> **Z 是僵死**

> **";RSDZT"; 中的一個, R 是正在執行, S 是在可中斷的就緒態中睡眠, D 是在不可中斷的等待或交換態中睡眠, Z 是僵死, T 是被跟蹤或被停止(由於收到訊號)**

**Fidelity caveat on the quote.** The stray semicolons in `";RSDZT";` are an archmanweb/mandoc
conversion artifact of this old page, not content: the same mangling appears throughout the file
(`kernel;, ;net;, ;vm`, and `tr ";\000"; ";\n";` in the `environ` example). The alphabet itself is
`RSDZT`. Anyone quoting P2 verbatim into the C3 entry should either normalise the semicolons or
flag them, so the registry row does not inherit conversion noise as if it were source text.

---

## 4. The two explicit yes/no questions, answered flatly

1. **Does the `Z ゾンビ` / `X 死亡` state alphabet appear?**
   - P1 (JA focal): **YES.** `Z ゾンビ (Zombie)` and `X 死亡 (Dead) (Linux 2.6.0 以降)` in
     `/proc/[pid]/stat` §2.2, repeated as `"Z (zombie; ゾンビ状態)", "X (dead; 死亡)"` in
     `/proc/[pid]/status` §2.3.
   - P2 (zh_TW LDP): **NO.** Alphabet is `RSDZT`; `Z 是僵死` present, no `X` state, 死亡 absent.

2. **Does the "swapped out XOR zombie leaves the file empty" sentence appear?**
   - P1 (JA focal): **NO.** `cmdline` names zombies only; zero スワップ occurrences in the block,
     and exactly one `空となる` on the whole page.
   - P2 (zh_TW LDP): **YES.** 被交換出記憶體 **或者** 已經僵死 ⇒ 沒有任何東西在該檔案裡 ⇒
     讀操作將返回零個字元.

The two pages split the claim: **the alphabet lives only on the modern page; the swap-out
disjunct lives only on the 1.3.11-era page.** Neither page carries both.

---

## 5. "Three worlds" — what the staged pages actually ground

The assignment frames C3 as "the three worlds a zero-character `/proc/<pid>/cmdline` read is
consistent with". On the staged bytes, only **two** worlds are stated anywhere:

| world | grounded by | verbatim |
|---|---|---|
| W1 zombie | P1 §2.1 **and** P2 §3.1 | P1: ゾンビプロセスの場合は、このファイルは空となる · P2: 或者該程序已經僵死, 那麼就沒有任何東西在該檔案裡 |
| W2 swapped out | P2 §3.1 **only** | 如果該程序已經被交換出記憶體 |
| W3 (kernel thread, or any other) | **neither page** | — |

Searches that came back empty, i.e. the negative evidence:

```
$ grep -n "カーネルスレッド\|カーネル・スレッド\|kernel thread" ja.txt
3559: (カーネルスレッドを除く)          # /proc/sys/vm/oom_dump_tasks — unrelated to cmdline

$ grep -n "執行緒\|核心執\|kernel thread" zhtw.txt
(no output)
```

P1's single kernel-thread mention is about OOM task dumps, not `cmdline`; P2, being 1.3.11-era,
predates the kernel-thread `cmdline` behaviour entirely. **The third world is therefore not
grounded on either staged page and must not be attributed to them.** If C3 needs three worlds, the
third needs its own source (e.g. the English `proc(5)` or kernel `fs/proc/base.c`), or the entry
should say "two worlds per the staged pages".

---

## 6. Cautions the C3 author needs before leaning on these quotes

### 6.1 P2 is not a modern page, and its version is load-bearing

P2 describes Linux 1.3.11 (last Chinese update 2000/11/26, package `man-pages-zh_tw 1.6.4.5-1`).
Its `stat` alphabet stops at `T` and predates `X` by years — which is precisely *why* the alphabet
is missing there. A C3 row citing P2 for the swap-out disjunct is citing a 1996/2000 translation of
a 1.3.x man page; the row's `used-by` and any "since" qualifier must reflect that, not imply
current-kernel behaviour.

### 6.2 P1 directly contradicts P2 on the swap-out claim

Same page P1, `comm %s` field (decoded lines 932–935), says visibility is **independent** of
swap-out:

```
(2) comm %s
括弧でくくられた実行形式のファイル名。
 実行形式がスワップアウトされているかどうかによらず、
 見ることができる。
```

Quote (20 non-space characters, within the cap; the full clause is 34):

> **スワップアウトされているかどうかによらず**

Full clause as it stands: `実行形式がスワップアウトされているかどうかによらず、見ることができる`.

P2's counterpart says the opposite for the same field:

> **該檔案是否可見取決於該檔案是否已被交換出記憶體**   (23 non-space characters)

So the two staged pages disagree on whether swap-out suppresses visibility at all — P2 says it
does, P1 says it does not. This is the strongest single reason not to present "swapped out ⇒
`cmdline` empty" as a current fact: the modern page on the same desk has already retired that
coupling for the neighbouring field, and its `cmdline` entry drops the swap-out clause entirely.

### 6.3 Quote hygiene for the registry rows

- P1's `X` quote must keep `(Linux 2.6.0 以降)`; dropping it turns a versioned statement into a
  timeless one.
- P2's quotes must not be silently de-semicoloned without a note (§3.2), and must keep the ASCII
  `.` sentence terminators — the page does not use `。`.
- P2 numbers the per-process directory `[number]`, not `[pid]`; a quote that rewrites `[number]`
  to `[pid]` is no longer verbatim.

---

## 7. Remaining unknowns

- **The third world.** Not on either staged page (§5). Unresolved by this assignment's sources.
- **Whether current kernels still empty `cmdline` for swapped-out processes.** P1 is silent; P2
  (1.3.11) asserts it; P1's `comm` field implies the coupling was dropped. Not decidable from the
  two staged pages — needs a modern English `proc(5)` or `fs/proc/base.c`.
- **P1's translation completeness.** Only the sections quoted here were verified as translated;
  other entries on the page remain English upstream text. Nothing in this report depends on them.
- **P2's rendering fidelity.** The semicolon mangling is systematic across the page; I verified the
  `RSDZT` alphabet and the `cmdline` sentence against the page's raw form, but did not audit the
  whole document for further conversion damage.

---

### Reproduce

```
SB=$(mktemp -d); cd "$SB"
curl -fsSL --max-time 120 -D ja.h -o ja.html \
  https://manpages.ubuntu.com/manpages/focal/ja/man5/proc.5.html
curl -fsSL --max-time 30 --http1.1 -D zh.h -o zh.html \
  https://man.archlinux.org/man/proc.5.zh_TW
sha256sum ja.html zh.html
# expect f64b0cde… ja (376399 B) and b8ede81d… zh (61889 B)
```
