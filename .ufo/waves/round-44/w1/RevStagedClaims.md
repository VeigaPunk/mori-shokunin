# Revenger — what the staged C3 entry actually asserts, against the primary documents

lane: mori · round: 44 · wave: 1 · role: revenger (leaf, no dispatch) · date: 2026-10-25
lane repo: `/home/vgpnk/Projects/shokunin/mori-shokunin` · instruments frozen at `7cb59c6891d4f5d0266fe062565f094da835dc84`
fleet + shokuknow: read-only · nothing written outside this file · scratch: `/tmp/r44revstage.zUmP` (`mktemp -d`)

Object of review: `/home/vgpnk/Projects/shokuknow/merge/mori/knowledge/corpus/knowledge/probe-absent-vs-dead-r39.md`
(the staged campaign entry, read-only), against the two pages it cites and against the current upstream
contract and kernel read path. Method: decode both pages, quote the located sentences, then test each
load-bearing sentence against (i) the page, (ii) current upstream man-pages, (iii) the kernel source that
implements the read, (iv) an executed probe on this host. Where a conclusion rests on reading code and not
on an executed observation it is marked **[INFERENCE]**.

---

## 0. Bottom line

The entry's *quotations* are accurate. Its *conclusions* are not. Four of them are false or unsupported
against the primary documents, and one of them (the `comm` rule) would import a rule that the entry's own
second source contradicts.

| # | staged assertion | verdict |
|---|---|---|
| 1 | zombie ⇒ `cmdline` empty, read returns not one character | **STATED** verbatim by S490 — adoptable |
| 2 | a swapped-out process also leaves `cmdline` empty | **STATED by S491 only**; retired upstream at Linux 2.3.26; not current behaviour |
| 3 | "whether `comm` is even visible depends on whether the file has been swapped out" | **UNSUPPORTED** — a mistranslation; upstream says the opposite at every revision checked, and S490 says the opposite |
| 4 | an empty read is consistent with "the process never existed" | **UNSUPPORTED / false** — a nonexistent pid gives `ENOENT` at `open()`, not a zero-length read |
| 5 | an empty read is consistent with "alive but swapped out" | **UNSUPPORTED** — obsolete wording; the real non-zombie empty-read class is a live task with no user `mm` (kernel thread) |
| 6 | `I` is a present-and-alive state per S490 | **UNSUPPORTED by S490** — the focal-era list has no `I`; current upstream does |
| 7 | "A process that is alive and running (no empty read at all)" | **FALSE on this host** — 226 of 227 live processes read zero-length |
| 8 | both `recheck:` lines demonstrate the claim | **NO** — they grep a word, they return `0` today as written, and they are blind to the entry's two novel claims |

---

## 1. Inputs and fetch receipts

| id | URL | status | bytes | encoding note |
|---|---|---|---|---|
| S490 | `https://manpages.ubuntu.com/manpages/focal/ja/man5/proc.5.html` | 200 | 376 399 | UTF-8; **all CJK is numeric character references** (`&#x30BE;` …) |
| S491 | `https://man.archlinux.org/man/proc.5.zh_TW` | 200 | 61 861 | UTF-8; **all CJK is numeric character references** |
| U1 | `https://man7.org/linux/man-pages/man5/proc_pid_cmdline.5.html` | 200 | 7 918 | man-pages **6.19**, tarball fetched 2026-09-09 |
| U2 | `https://man7.org/linux/man-pages/man5/proc_pid_stat.5.html` | 200 | 20 647 | man-pages 6.19 |
| U3 | `https://manpages.ubuntu.com/manpages/focal/en/man5/proc.5.html` | 200 | — | focal **English** (the source S490 translates) |
| H1–H3 | `man-pages-2.00 / 3.00 / 4.00` `man5/proc.5` (kernel.org archive) | 200 | — | roff, for the wording history |
| K1–K4 | `fs/proc/base.c`, `fs/proc/array.c`, `include/linux/sched.h`, `kernel/exit.c` (torvalds/master) | 200 | — | the code that serves the read |

Provenance of the two staged pages, from their own bytes:

- S490 footer: `Provided by: manpages-ja (Version: 0.5.0.0.20180315+dfsg-1)`; breadcrumb `"name":"focal"`.
  It is a **third-party Japanese translation hosted by Ubuntu**, and a partial one (e.g. the
  `/proc/[pid]/comm` entry is still English upstream text).
- S491 body: 「本手冊頁基本上是針對 Linux 1.3.11 核心 … 最後更新也是針對 Linux 1.3.11.」 and
  「[中文版最新更新] 2000/11/26」; package footer `extra/man-pages-zh_tw 1.6.4.5-1`.
  It is a translation of a **Linux 1.3.11-era** `proc(5)`.

That provenance is load-bearing for every verdict below: S491's underlying English text predates both the
`X` state (2.6.0) and the retirement of the swap-out clause (2.3.26).

---

## 2. What each page actually says (quoted, with section)

### S490 — §「/proc/[pid]/cmdline」

```
この読み出し専用のファイルはプロセスの完全なコマンド行を保持する。
ただし、そのプロセスがゾンビプロセスの場合は、このファイルは空となる。
つまり、このファイルを読み出しても一文字も返らない。
```

**Zombie, singular. No swap-out clause anywhere in this block** (no スワップ occurrence in the section).

### S490 — §「/proc/[pid]/stat」, field `(2) comm %s`

```
括弧でくくられた実行形式のファイル名。
実行形式がスワップアウトされているかどうかによらず、見ることができる。
```

= "visible **regardless of whether** the executable is swapped out." This is the sentence the staged entry's
`comm` claim contradicts, on the same desk.

### S490 — §「/proc/[pid]/stat」, field `(3) state %c`

```
R 実行中 (Running) · S Sleeping in an interruptible wait · D Waiting in uninterruptible disk sleep
Z ゾンビ (Zombie) · T (シグナルでの) 停止 … · t トレースによる停止 (Tracing stop) (Linux 2.6.33 以降)
W ページング中 (Linux 2.6.0 より前のみ) · X 死亡 (Dead) (Linux 2.6.0 以降)
x 死亡 (Dead) (Linux 2.6.33 から 3.13 までのみ) · K Wakekill (2.6.33–3.13) · W Waking (2.6.33–3.13)
P Parked (Linux 3.9 から 3.13 までのみ)
```

Twelve entries, **no `I`**. The §「/proc/[pid]/status」 `State:` block repeats the same set and also stops at
`"X (dead; 死亡)"`. The only アイドル occurrences on the whole page are PowerPC `htab`, PowerPC pre-zero page,
and `/proc/uptime` — none is a `stat` state.

### S491 — §「cmdline」

```
該檔案儲存了程序的完整命令列.
如果該程序已經被交換出記憶體, 或者該程序已經僵死,
那麼就沒有任何東西在該檔案裡, 這時候對該檔案的讀操作將返回零個字元.
```

**Two** causes stated (swapped out **or** zombie). The page never mentions a third, never uses the word
"ambiguous", and never says the two are indistinguishable.

### S491 — §「stat」, `comm %s` and `state %c`

```
comm %s
執行檔的檔名, 包括路徑.
該檔案是否可見取決於該檔案是否已被交換出記憶體.
state %c
";RSDZT"; 中的一個, R 是正在執行, … Z 是僵死, T 是被跟蹤或被停止(由於收到訊號).
```

Alphabet `RSDZT` — five letters, **no `X`**, no 死亡 on the page. (The stray semicolons are an
archmanweb/mandoc conversion artifact, not source text.)

---

## 3. (a) Is `X`/dead a `stat` state on current upstream Linux, or only on the cited translations?

**It is on current upstream, and it is code-mapped — not translation-only.** But it is a teardown-window
state, not a probe-reachable world, and the staged entry's use of it overstates what it buys.

1. Upstream, current — `proc_pid_stat(5)` (man-pages 6.19), field (3): `X  Dead (from Linux 2.6.0 onward)`,
   and the list also carries `I  Idle (Linux 4.14 onward)`. The **focal English** `proc(5)` already carries
   `X Dead (from Linux 2.6.0 onward)` too — so S490's `X` is not a translation invention.
2. Kernel — `fs/proc/array.c`:

   ```c
   "X (dead)",   /* 0x10 */
   "Z (zombie)", /* 0x20 */
   ```
   and `do_task_stat()` reads `state = *get_task_state(task);`. `get_task_state()` indexes that array by
   `task_state_index()`, and `include/linux/sched.h` defines:
   ```c
   unsigned int state = (tsk_state | tsk_exit_state) & TASK_REPORT;
   ```
   i.e. `exit_state == EXIT_DEAD` (0x10) is exactly what renders as `X`.
3. Where `EXIT_DEAD` is set — `kernel/exit.c:769-771`:
   ```c
   if (autoreap) {
           tsk->exit_state = EXIT_DEAD;
           list_add(&tsk->ptrace_entry, &dead);
   }
   ```
   i.e. after the task is already on the `dead` list and `release_task()` is imminent. **[INFERENCE]** the
   `X` window is the teardown window, and the pid may be detached between the `stat` read and the next
   syscall. My 227-process scan observed **no `X`** (and no `Z` at that instant) — a snapshot, not a proof.
4. Consequence for the entry: `X` **cannot come from S491** (its alphabet stops at `T`), and it adds **no
   decision power** over `Z` — the entry itself collapses them into one case ("present-but-dead — `state`
   says `Z` … or `X`"). So the honest claim is "the man page documents `X` since 2.6.0; a probe cannot rely
   on observing it; `Z` is the present-but-dead state you will actually see", not "two states a pid probe
   must be able to read apart".

**Verdict:** `X` is documented and code-backed on current Linux → the entry's *fact* is fine; its
*framing* ("the two states a pid probe must be able to read apart from a live process") is the campaign's,
not the page's.

---

## 4. (b) Does "swapped out" really empty `cmdline`, or is it older wording?

**Older wording — and upstream recorded it as no longer true.** This is the strongest single finding.

Wording history, roff bytes:

| revision | `/proc/[pid]/cmdline` text |
|---|---|
| man-pages **2.00** `man5/proc.5:61-63` | `This holds the complete command line for the process, unless the whole process has been swapped out or the process is a zombie. In either of these latter cases, there is nothing in this file: i.e. a read on this file will return 0 characters.` |
| man-pages **3.00** `man5/proc.5:92` | `unless the process is a zombie.` then the roff comment `.\" In 2.3.26, this also used to be true if the process was swapped out.` |
| man-pages **4.00** `man5/proc.5:387` | same comment, same demotion |
| man-pages **6.19** `proc_pid_cmdline(5)` | `unless the process is a zombie. In the latter case, there is nothing in this file: that is, a read on this file will return 0 characters.` — no swap branch |
| lane's own held row `corpus/evidence/sources-r31/S170.src:15` | `.\" In Linux 2.3.26, this also used to be true if the process was swapped out.` |

So the swap-out disjunct was **live text in 1999, demoted to a historical comment in 2008, and is absent
from the current contract**. S491 quotes the live 1.3.11-era form. The staged entry's own Boundary concedes
this ("its wording must be checked against current upstream before being relied on for a version claim") —
and then the Claim section relies on it for exactly that.

Mechanism on the current kernel (`fs/proc/base.c`) — **[INFERENCE from code, not executed]**:

```c
static ssize_t get_task_cmdline(...) {
        mm = get_task_mm(tsk);
        if (!mm)
                return 0;                 /* zombie / mm-less task: the empty read */
        ret = get_mm_cmdline(mm, buf, count, pos);
```
and `get_mm_cmdline()` returns 0 only for `!mm->env_end`, `arg_start >= arg_end`, or `pos >= len`; otherwise
it copies the argv range through `access_remote_vm(mm, pos, page, size, FOLL_ANON)`, which faults a swapped
page back in rather than reporting nothing. A swapped-out *userspace* process therefore does not produce a
zero-length read.

Executed counter-evidence to the "three worlds" enumeration (this host, linux 7.2.11-arch1-1):

| probe | result |
|---|---|
| child exits, not yet reaped | `/proc/<pid>` exists, `stat` state `Z`, `cmdline` = **0 bytes**, read succeeds |
| after `waitpid` | `/proc/<pid>` **gone** |
| `open("/proc/999999/cmdline")` | **`ENOENT`** — open fails; no zero-length read exists to be "consistent with never existed" |
| fd opened while the child was alive, child killed | subsequent `read()` = **0 bytes** |
| 227 visible pids, `cmdline` length + `stat` state | **226 zero-length, state `S` (180) / `I` (46)** — live, mm-less kernel threads; **1** non-empty (pid 1, 18 bytes); 0 `Z`, 0 `X` |
| `execv(prog, {NULL})` (argc = 0), live | state `S`, `cmdline` = **1 byte** (a single NUL) — not zero |

The dominant non-zombie zero-length read on a current kernel is **a live task with no user `mm`** — not a
swapped-out process. That is the third world the entry needed, and it is neither of the ones it names.

---

## 5. (c) Do the `recheck:` commands demonstrate the claim?

No. Three separate defects.

**(i) They grep for a word, not for the mechanism — and they are blind to the entry's own novel claims.**

```
recheck: 180d — `curl … focal/ja/proc.5.html | grep -c 'ゾンビプロセス'` -> 1
recheck: 180d — `curl … proc.5.zh_TW | grep -c '僵死'` -> 2
```

Located occurrences in the decoded pages:

| term | where it occurs | covers the state alphabet? | covers the `comm` rule? |
|---|---|---|---|
| `ゾンビプロセス` (1×) | §「cmdline」 only | **no** | no |
| `僵死` (2×) | §「cmdline」 + §「stat」 `state` | **no** (`X` absent from S491) | **no** |

So the recheck of S490 — the page that is supposed to ground the new `Z`/`X` alphabet — never touches the
state list, and the recheck of S491 never touches the `comm` sentence, which is the one load-bearing quote
the entry got wrong. If the entry had adopted the `comm` rule, the recheck would have gone green forever on
a page that still says the false thing.

**(ii) As written, both commands return `0` today (exit 1).** Both pages deliver CJK as numeric character
references, so the literal pattern never appears in the byte stream:

```
$ curl -fsSL 'https://manpages.ubuntu.com/manpages/focal/ja/man5/proc.5.html' | grep -c 'ゾンビプロセス'
0                                   # exit 1
$ curl -fsSL 'https://man.archlinux.org/man/proc.5.zh_TW' | grep -c '僵死'
0                                   # exit 1
```

The recorded `1` and `2` are exactly the counts **after `html.unescape()`**, and exactly the number of
*lines* containing each term — `grep -c` counts lines, not occurrences. The recorded outputs are therefore
consistent with a decoded rendering and **not** with the recorded pipeline; either the pipeline was not the
one run, or the numbers were taken from a decoded view and transcribed as if `grep` had produced them.

**(iii) Even a decoded phrase grep is fragile, because the pages wrap mid-phrase.** On S491 the mechanism
phrase is split by the page's own line break:

```
這時候對該檔案的讀操作將返回零
      個字元.
```

so `零個字元` occurs **0** times in the decoded text and **1** time only after whitespace collapse. Any
recheck that greps a phrase without normalising whitespace will report a false FAIL on an unchanged page.

**Mechanism-anchored replacement, run today** (tags stripped → entities unescaped → whitespace collapsed):

```
$ curl -fsSL --max-time 40 'https://manpages.ubuntu.com/manpages/focal/ja/man5/proc.5.html' \
  | python3 -c 'import sys,html,re
t=re.sub(r"\s+","",re.sub(r"<[^>]+>","",html.unescape(sys.stdin.read())))
print("X死亡:",t.count("X死亡"),"Zゾンビ:",t.count("Zゾンビ"),"一文字も返らない:",t.count("一文字も返らない"))'
X死亡: 1 Zゾンビ: 1 一文字も返らない: 1

$ curl -fsSL --max-time 40 'https://man.archlinux.org/man/proc.5.zh_TW' \
  | python3 -c 'import sys,html,re
t=re.sub(r"\s+","",re.sub(r"<[^>]+>","",html.unescape(sys.stdin.read())))
print("零個字元:",t.count("零個字元"),"被交換出記憶體:",t.count("被交換出記憶體"))'
零個字元: 1 被交換出記憶體: 2
```

These count the sentences the entry leans on. A word count cannot fail when the mechanism changes; these can.

---

## 6. Sentence-by-sentence verdicts on the staged entry

V = verdict: **STATED** (the page says it) · **INFERRED** (campaign synthesis, defensible but not page text) ·
**UNSUPPORTED** (contradicted by the page, by upstream, or by observed behaviour).

| staged sentence (abridged) | V | evidence |
|---|---|---|
| "A probe that finds nothing has three possible explanations…" | INFERRED / partly UNSUPPORTED | the "three" set is wrong (§3, §4); "absence is the one it cannot prove" matches `PROVINCE.md` FR5 |
| "The Japanese **official** man page states…" | UNSUPPORTED (provenance word) | footer: `manpages-ja (Version: 0.5.0.0.20180315+dfsg-1)` — a third-party translation hosted by Ubuntu, partially untranslated |
| "…the **two states a pid probe must be able to read apart** from a live process (`Z`, `X`)" | INFERRED | the page lists twelve state characters; the pair is a selection; `X` adds no decision power over `Z` (§3.4) |
| "And it states what a zombie's `cmdline` file looks like: 「ただし…一文字も返らない。」" | **STATED** | S490 §cmdline, verbatim |
| "The Chinese translation **adds a third case** and **states the ambiguity directly**" | INFERRED | S491 §cmdline states two causes; no third, no "ambiguity" |
| 「如果該程序已經被交換出記憶體…返回零個字元.」 | **STATED** (quote) / obsolete (rule) | S491 §cmdline; retired at 2.3.26 (§4) |
| "It adds the matching rule for the `comm` field: 「該檔案是否可見取決於該檔案是否已被交換出記憶體」" | **UNSUPPORTED** | upstream at 2.00/3.00/4.00/focal/6.19: "This is visible **whether or not** the executable is swapped out"; S490 §stat (2): 「…によらず、見ることができる」 |
| "an empty read … is consistent with … the process never existed" | **UNSUPPORTED** | `open("/proc/999999/cmdline")` → `ENOENT` (executed); contradicts the entry's own case 3 |
| "…or the process is alive but swapped out" | **UNSUPPORTED** (current Linux) | 2.3.26 note; absent from 6.19; `access_remote_vm(..., FOLL_ANON)` faults the page in; 226/227 live pids read empty with state `S`/`I` |
| "The probe must read the `state` field to tell them apart" | INFERRED / over-claims | `state` cannot separate world 1 — there is no file to read; `/proc/<pid>` presence does that |
| "…`state` is precisely the field an argv-substring probe never reads" | INFERRED, true by construction | `pgrep -f` matches `cmdline`; it never opens `stat` |
| "The cmdline-zero-character rule … already held … as the upstream `proc_pid_cmdline(5)` row (which also carries the Linux 2.3.26 swap-out note)" | **STATED / verified** | `corpus/SOURCES.md:176` (S170) and `corpus/evidence/sources-r31/S170.src:15` |
| "S490 is a translation of one Ubuntu release's man pages (focal / 20.04)" | **STATED / verified** | breadcrumb `"name":"focal"` |
| "S491 tracks the older LDP-era man-pages revision" | **STATED / verified, and understated** | page body: Linux 1.3.11, 2000/11/26, `man-pages-zh_tw 1.6.4.5-1` |
| Probe shape 1: "present-and-alive — `R`, `S`, `D`, `T`, `t`, `I`" | **UNSUPPORTED for `I`** | S490 has no `I` entry (focal-era list ends at `P`); `I` is upstream since 4.14; S490's `W`/`x`/`K`/`P` are omitted from the staged list |
| Probe shape 2: "present-but-dead — `Z` or `X`; the pid exists, the daemon does not work" | Z/X STATED; rest INFERRED | `X` is a teardown-window state (§3.3); `Z` verified empirically (state `Z`, `/proc` present) |
| Probe shape 3: "not-present — the `/proc/<pid>` entry is gone" | INFERRED | true, and it is the **only** case that yields `ENOENT` rather than an empty read |
| "Collapsing case 2 into case 3 is the error the lane's own boundary names" | INFERRED, sound | `PROVINCE.md` FR5: "an unavailable pid probe is not absence" |
| "`cmdline` is empty for a zombie and **possibly** for a swapped-out process" | first half STATED, second obsolete | §4 |
| "A census that reports 'watchdog absent' from an empty `cmdline` read is making a claim it cannot support" | INFERRED, sound — and strengthened | the empirical scan adds a fourth producer of the empty read (live mm-less task) |
| "Delivery paths this cannot see — A process that is alive and running (**no empty read at all**)" | **FALSE** | 226 of 227 live processes on this host read zero-length with state `S`/`I` |

**Lane-boundary claim checked:** "the lane holds no row for the state alphabet" — **true at the entering tip**:

```
$ git grep -l 'Z ゾンビ' 1429c791 -- corpus/ | wc -l   → 0
$ git grep -l 'X 死亡' 1429c791 -- corpus/ | wc -l     → 0
```

---

## 7. Sentences the lane MUST NOT adopt verbatim

1. **The `comm` rule.** 「該檔案是否可見取決於該檔案是否已被交換出記憶體」 / "whether `comm` is even
   visible depends on whether the file has been swapped out." *Why:* it is a translation inversion of
   "This is visible whether or not the executable is swapped out" — true in man-pages 2.00 (`proc.5:223`),
   3.00 (`:336`), 4.00 (`:1508`), focal English, and 6.19 `proc_pid_stat(5)`; and S490's translation of the
   same field says the opposite. Adopting it would (a) put a false rule in `corpus/`, (b) make S471 and S472
   contradict each other inside one entry, and (c) be locked green by a recheck that greps 僵死.
2. **"an empty read … is consistent with … the process never existed."** *Why:* a nonexistent pid produces
   `ENOENT` at `open()`, not a zero-length read — executed. The entry's own case 3 says so.
3. **"…or the process is alive but swapped out."** *Why:* 1.3.11-era wording, retired at 2.3.26, absent from
   the current contract, contradicted by the read path, and not the class that actually produces empty reads
   (live mm-less tasks do).
4. **"The Japanese **official** man page."** *Why:* it is `manpages-ja 0.5.0.0.20180315+dfsg-1`, a partial
   third-party translation; "official" is a provenance claim the page does not support. The lane's own S471
   row says 日本語訳 / translation — keep that wording.
5. **"the two states a pid probe must be able to read apart from a live process (`Z` and `X`)."** *Why:* the
   page lists twelve; `X` is a teardown-window state the entry then collapses into the same case as `Z`, so
   the pair buys nothing. Say instead: "the page documents `Z` and, since 2.6.0, `X`; `Z` is the state a
   probe will actually observe."
6. **"present-and-alive — `R`, `S`, `D`, `T`, `t`, `I`."** *Why:* `I` is not on the cited page; `W`, `x`,
   `K`, `P` are on it and omitted. Either quote the page's list whole, or say "the page's list, plus `I`
   from current upstream (Linux 4.14 onward)".
7. **"A process that is alive and running (no empty read at all)."** *Why:* false here — 226/227 live
   processes read empty. Replace with "a userspace process with a non-empty argv region".
8. **Both `recheck:` lines as written.** *Why:* they return `0` today (entity-encoded bodies), they count
   lines, and they do not touch either novel claim. Use the §5 replacement and record the real numbers.

---

## 8. What the lane *can* hold (adoptable core)

- S490 §cmdline, verbatim: 「ただし、そのプロセスがゾンビプロセスの場合は、このファイルは空となる。つまり、
  このファイルを読み出しても一文字も返らない。」 — zombie ⇒ empty file ⇒ not one character returned.
- S490 §stat (3): `Z ゾンビ (Zombie)`; `X 死亡 (Dead) (Linux 2.6.0 以降)` — **with** the version
  qualifier; plus `x 死亡 (Dead) (Linux 2.6.33 から 3.13 までのみ)`.
- S491 §cmdline, verbatim as a *translation-level* statement: swapped-out-or-zombie ⇒ nothing in the file ⇒
  zero characters returned — labelled "a 1.3.11-era translation of a clause upstream retired at 2.3.26",
  never as current behaviour.
- The operational rule, which the pages do support: an argv-substring probe (`pgrep -f`) can nominate a
  candidate but cannot decide liveness; `stat`'s state field plus `/proc/<pid>` presence is what separates
  "present, not running" (`Z`) from "not present" (`ENOENT`).
- The negative space, now evidenced rather than asserted: a zero-length read also comes from a **live**
  task with no user `mm` (226/227 pids here), so "empty read ⇒ the daemon is gone" is false for a second
  reason the entry did not have.

---

## 9. Residual defects in the uncommitted draft (separate from the staged entry)

`corpus/knowledge/pid-probe-conclusion-r44.md` exists on disk, untracked, at the lane tip (`git cat-file -e
HEAD:…` → absent). It already **drops** the `comm` rule and **demotes** the swap-out branch to a
translation-level statement — both correct. Three residual over-claims remain, for the integration owner:

1. "`stat`'s state field separates the second world from the third and **from the first**" — it cannot: the
   first world has no `/proc/<pid>` entry to read. The draft's next clause says exactly that
   ("a presence-and-identity check … distinguishes the first from the rest"), so the sentence contradicts
   itself. Fix: "`state` separates the zombie world from a live-but-empty one; presence separates both from
   `ENOENT`."
2. "a state that has existed since Linux 2.6.0 and that a live process is not in" — true but unusable: `X` is
   the teardown window (`kernel/exit.c:770`). Say "documented since 2.6.0; a probe will observe `Z`".
3. Its `recheck` (ゾンビ → 3) is honest about the entity encoding, but still a **word** count; `ゾンビ`
   occurs in §cmdline, §stat state, and §status — a removal of the state-list entry would only drop the
   count to 2, which reads as "the page moved" rather than "the mechanism changed". Use the §5 commands
   (`X死亡`, `Zゾンビ`, `一文字も返らない`; `零個字元`, `被交換出記憶體`).

---

## 10. Confidence

| finding | confidence | basis |
|---|---|---|
| staged quotes match the pages | **high** | decoded bytes, both pages, located sections |
| `comm` sentence is a translation inversion | **high** | five upstream revisions + S490's own rendering of the same field |
| swap-out clause retired at 2.3.26 | **high** | roff comment in 3.00/4.00/6.20 tree + lane S170.src |
| swap-out cannot produce a zero-length read on the current kernel | **medium** | **[INFERENCE]** from `get_mm_cmdline`/`access_remote_vm`; not exercised (no way to force swap-out here) |
| nonexistent pid ⇒ `ENOENT`, not an empty read | **high** | executed |
| 226/227 live pids read zero-length with state `S`/`I` | **high** (snapshot) | executed scan on linux 7.2.11-arch1-1; describes this host, not every kernel |
| `X` is a teardown-window state | **medium** | **[INFERENCE]** from `kernel/exit.c` + `__task_state_index`; no `X` observed in a 227-pid snapshot |
| recorded recheck outputs did not come from the recorded pipeline | **high** | verbatim rerun → 0/exit 1; recorded values equal decoded line counts exactly |

No tool was installed or upgraded for this report (operator directive satisfied vacuously); tools used were
`curl`, `python3` (stdlib), `gcc`, and read-only `git`.

---

## Reproduce

```sh
SB=$(mktemp -d); cd "$SB"
curl -fsSL --max-time 120 -o ja.html 'https://manpages.ubuntu.com/manpages/focal/ja/man5/proc.5.html'
curl -fsSL --max-time 40  -o zh.html 'https://man.archlinux.org/man/proc.5.zh_TW'
python3 - <<'PY'
import html,re
for f,terms in (("ja.html",["X死亡","Zゾンビ","一文字も返らない","によらず"]),
                ("zh.html",["零個字元","被交換出記憶體","該檔案是否可見取決於該檔案是否已被交換出記憶體","RSDZT"])):
    t=re.sub(r"\s+","",re.sub(r"<[^>]+>","",html.unescape(open(f,encoding="utf-8",errors="replace").read())))
    print(f,{k:t.count(k) for k in terms})
PY
# expect ja: X死亡 1, Zゾンビ 1, 一文字も返らない 1, によらず 1
#        zh: 零個字元 1, 被交換出記憶體 2, comm-inversion 1, RSDZT 1
# the verbatim staged rechecks, for the record:
curl -fsSL 'https://manpages.ubuntu.com/manpages/focal/ja/man5/proc.5.html' | grep -c 'ゾンビプロセス'   # 0, exit 1
curl -fsSL 'https://man.archlinux.org/man/proc.5.zh_TW'                     | grep -c '僵死'             # 0, exit 1
```
