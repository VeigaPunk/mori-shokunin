# A zero-character cmdline read is not absence: two documented worlds, one measured world, and a retired one

source: S471 — https://manpages.ubuntu.com/manpages/focal/ja/man5/proc.5.html — 節「/proc/[pid]/cmdline」, 節「/proc/[pid]/stat」の state 欄 (`Z ゾンビ (Zombie)`, `X 死亡 (Dead) (Linux 2.6.0 以降)`) and 同節 field `(2) comm` (`スワップアウトされているかどうかによらず`); Ubuntu focal (20.04) ja 翻訳, fetched 2026-10-25
source: S472 — https://man.archlinux.org/man/proc.5.zh_TW — 「cmdline」段 and the `comm` sentence `該檔案是否可見取決於該檔案是否已被交換出記憶體`; Arch Linux man page, zh_TW translation of Linux 1.3.11-era man-pages (last Chinese update 2000-11-26), fetched 2026-10-25
verified-at: 2026-10-25 — both pages fetched 2026-10-25; this entry first lands in round 44 (no earlier revision holds it)
recheck: 180d — `curl -fsSL --max-time 40 'https://manpages.ubuntu.com/manpages/focal/ja/man5/proc.5.html' | python3 -c 'import sys,html;print(html.unescape(sys.stdin.read()).count("ゾンビ"))'` -> 3; `curl -fsSL --http1.1 --max-time 40 'https://man.archlinux.org/man/proc.5.zh_TW' | python3 -c 'import sys,html;print(html.unescape(sys.stdin.read()).count("僵死"))'` -> 2 (ran 2026-10-25)
coverage-map: FR5 — watchdog daemon identity and degraded-pgrep visibility
ground: frontier item **FR5** — "an unavailable pid probe is not absence, and argv-substring matches do not establish daemon identity" (`PROVINCE.md`, Frontier FR5)

## Claim

**What the lane already holds, and what is new here.** `watchdog-identity-r31.md:27`
already carries the zero-character `cmdline` read (S170) and `:29` the `Z (zombie)`
state; S171's scope already names the `X` state letter. This entry does not
re-assert those. Its new ground is the **measured mm-less world** below (which no
lane record carries), the two translations' accounts and their disagreement, and
the `ENOENT` boundary for a pid that does not exist.

A probe that reads `/proc/<pid>/cmdline` and gets nothing has not established
that the process does not exist. **A pid that does not exist is not an empty
read at all** — `open("/proc/999999/cmdline")` returns `ENOENT` (measured on this
host, `errno=2`, `evidence/cmdline-empty-by-state.txt`). So an empty read is
evidence about an existing task, and it has three explanations:

1. **The task is a zombie or dead (`Z`, `X`).** S471, 節「/proc/[pid]/cmdline」:
   「ただし、そのプロセスがゾンビプロセスの場合は、このファイルは空となる。つまり、このファイルを
   読み出しても一文字も返らない。」 S471's state alphabet names `Z ゾンビ (Zombie)`
   and `X 死亡 (Dead) (Linux 2.6.0 以降)`; S472 names the zombie case in the same
   breath as the swap-out case: 「如果該程序已經被交換出記憶體, 或者該程序已經僵死, 那麼就沒有
   任何東西在該檔案裡，這時候對該檔案的讀操作將返回零個字元。」
2. **The task has no `mm` — a kernel thread.** Measured on this host (kernel
   7.2.11-arch1-1): of 1931 `/proc` entries, 1698 read a zero-length `cmdline`,
   and every one of them was state `I` (1489) or `S` (209)
   (`evidence/cmdline-empty-by-state.txt`). No `Z`/`X` was present at that
   instant. **This is the load-bearing reading: the state letter does not
   separate this world from a sleeping user process** — `S` covers both a
   sleeping user task with an `mm` and an mm-less kernel thread. The
   discriminator is the absence of an `mm`, not the state field.
3. **The task was swapped out — retired wording, not current behaviour.** S472
   states it; S471 contradicts the coupling for the neighbouring `comm` field:
   「実行形式がスワップアウトされているかどうかによらず、見ることができる。」
   S472 is a translation of Linux 1.3.11-era man-pages (last Chinese update
   2000-11-26), so its sentence describes a 1.3.x kernel.

So: the read alone separates none of these; `stat`'s state field separates the
`Z`/`X` world from the rest, an `mm` check separates the kernel-thread world, and
a presence-and-identity check (the pidfd / start-time path the lane holds
elsewhere) is what distinguishes a live task from a reused pid. FR5's sentence
stands: none of these is daemon identity.

## Boundaries — what this entry does not license

- **`X` buys no decision power beyond `Z`.** It is documented upstream as well as
  in S471 (a teardown-window state), and it collapses into the same "empty
  `cmdline`, dead" reading as `Z`. S472's alphabet stops at `T` and predates `X`
  entirely — which is why the two pages differ, and why the `X` version qualifier
  「(Linux 2.6.0 以降)」 must travel with any quote of it.
- **The mm-less world is measured here, not documented by the two pages.** The
  focal-era state list in S471 ends at `P`; it does not name `I`. The claim that
  kernel threads read zero-length is this host's reading, and the general
  mechanism is not quoted from either page.
- **The zombie/0-character rule itself is already held** in English as S170
  (`proc_pid_cmdline(5)` at man-pages 6.20). This entry adds the state alphabet,
  the measured mm-less world, the contradiction between the two translations, and
  the ENOENT boundary; it does not re-assert the held rule and does not supersede
  S170.
- **It does not identify the watchdog daemon.** FR5 stays open: a state field read
  is not an argv-substring probe, and neither one establishes daemon identity.
- **It does not change the census.** No probe, surface, finding id or threshold is
  added; the lane's census bytes are untouched by this entry.
- **It is not evidence about a crash.** An empty `cmdline` is a state, not a
  cause; kill/OOM classification stays with the journal and cgroup rows.
- **A translation is not an authentication.** Both pages are translations; where
  they disagree with current upstream English, upstream wins, and where they
  disagree with each other the newer page wins. S471 is a partial translation
  (`manpages-ja 0.5.0.0`), so "the Japanese official man page" is not earned.
