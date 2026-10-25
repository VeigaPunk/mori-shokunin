# ScribeEntryDraft — C3 knowledge-entry draft (FR5, round 44 wave 1)

Seat: scribe (leaf). Round 44 wave 1. One file written by this seat: this report.
No instrument, corpus file, registry row, README byte or SCORECARD byte was edited;
the draft in §1 is the copy target for the integration owner.

- Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin`, instruments frozen at
  `7cb59c6891d4f5d0266fe062565f094da835dc84`.
- Copy target: `corpus/knowledge/pid-probe-conclusion-r44.md`.
- Copy-target state: the path **already exists untracked**, written outside this seat,
  and it changed under me while I worked: 4261 bytes at 05:12, rewritten to 5526 bytes
  at 05:16:27 (both observed with `ls -l --time-style=+%H:%M:%S` on 2026-10-25). This
  report does not touch it; §5 lists where my draft differs from the 05:16 version and
  why.
- Sources opened 2026-10-25, both fetched twice (read pass, then recheck replay):
  S471 = `https://manpages.ubuntu.com/manpages/focal/ja/man5/proc.5.html` (376 399 bytes),
  S472 = `https://man.archlinux.org/man/proc.5.zh_TW` (61 889 bytes). Both pages encode
  their non-ASCII text as numeric character references; every quote below was checked
  against `html.unescape()`d, tag-stripped text (§3.6).
- Tooling installed/upgraded: **none** (system `python3`, `curl`, `git` sufficed).
- Campaign ids **not** adopted: the staged entry at
  `/home/vgpnk/Projects/shokuknow/merge/mori/knowledge/corpus/knowledge/probe-absent-vs-dead-r39.md`
  uses S490/S491. The lane ids are S471 (Ubuntu ja page) and S472 (Arch zh_TW page),
  matching the two registry rows already in the worktree (`corpus/SOURCES.md:250-251`).

## 1. Draft entry (verbatim copy target)

```markdown
# A zero-character cmdline read is three worlds, and the `stat` state field is the discriminator

source: S471 — https://manpages.ubuntu.com/manpages/focal/ja/man5/proc.5.html — 節「/proc/[pid]/cmdline」 (the zombie empty-read sentence, `proc.5.html:446-449`; section `:444-452`), 節「/proc/[pid]/stat」 field (2) comm (`:1417-1420`) and the state-letter list (`:1427-1458`: `Z` at `:1433-1434`, `X` at `:1446-1447`, `x` at `:1448-1450`); Ubuntu focal (20.04) ja translation of Linux man-pages release 3.79 (page footer, `:4756-4760`); opened 2026-10-25
source: S472 — https://man.archlinux.org/man/proc.5.zh_TW — 「cmdline」段 (`:90-100`), 「stat」段 state 欄 (`:272-279`) and 「遵循」段 (`:855-861`); Arch Linux `extra/man-pages-zh_tw` 1.6.4.5-1 (upstream man-pages-zh), a page whose 遵循 section says it targets Linux 1.3.11, with foot date 22 July 1996 (`:912`) and Chinese update 2000/11/26 (`:895`); opened 2026-10-25
verified-at: 2026-10-25 (lane instruments at 7cb59c6891d4f5d0266fe062565f094da835dc84; both pages opened 2026-10-25; no host /proc probe was run for this entry)
recheck: 180d — `python3 -c 'import urllib.request,html;g=lambda u:html.unescape(urllib.request.urlopen(u,timeout=40).read().decode());a=g("https://manpages.ubuntu.com/manpages/focal/ja/man5/proc.5.html");b=g("https://man.archlinux.org/man/proc.5.zh_TW");print("ja",a.count("一文字も返らない"),a.count("死亡 (Dead)"),"zh",b.count("返回零"),b.count("僵死"))'` -> `ja 1 2 zh 1 2` (ran 2026-10-25)
coverage-map: FR5 — watchdog daemon identity and degraded-pgrep visibility
ground: frontier item FR5 — "an unavailable pid probe is not absence, and argv-substring matches do not establish daemon identity" (`PROVINCE.md:48`)

## Claim

A probe that reads `/proc/<pid>/cmdline` and reports nothing has not established
that the process was not there. The two opened translations state two different
mechanisms for the same empty read, and neither mechanism is "the process does
not exist".

S471, 節「/proc/[pid]/cmdline」: 「ただし、そのプロセスがゾンビプロセスの場合は、このファイルは空となる。つまり、このファイルを読み出しても一文字も返らない。」
— for a zombie the file is empty, and reading it returns not one character.

S472, 「cmdline」段: 「該檔案儲存了程序的完整命令列. 如果該程序已經被交換出記憶體, 或者該程序已經僵死, 那麼就沒有任何東西在該檔案裡, 這時候對該檔案的讀操作將返回零個字元.」
— a process swapped out of memory, or one that has died, leaves nothing in the
file and the read returns zero characters. (Quotes are joined across the pages'
line breaks; characters verbatim, whitespace normalized.)

So a zero-character read is consistent with three worlds:

1. **not present** — the pid never existed, or it exited and was reaped, so the
   read had nothing to open. [INFERENCE: that the kernel answers such a read
   with an error rather than with zero bytes; neither opened page states the
   error form. The world enters the set because a probe that reports "no
   output" has already discarded the difference between a failed read and an
   empty one.]
2. **present but dead** — the pid exists as a zombie (S471's empty-cmdline
   sentence), and `stat`'s state letter says so: `Z` — 「ゾンビ (Zombie)」 (S471),
   or `X` — 「死亡 (Dead) (Linux 2.6.0 以降)」 (S471).
3. **present and alive, command line not in memory** — swapped out (S472): the
   read returns zero characters for a process that is neither a zombie nor
   gone.

The read alone separates none of the three. What this entry adds is that the
third world is stated in the lane's sources at all, and that `stat`'s state
field is what separates world 2 from worlds 1 and 3.

## The discriminator — `stat` field 3

`/proc/<pid>/stat` field 3 is the state letter, and it follows the
parenthesised task name; the lane already holds that positional fact
(`corpus/knowledge/watchdog-identity-r31.md:29`).

- `Z` → world 2. S471 lists `Z` with the gloss 「ゾンビ (Zombie)」.
- `X` → world 2. S471 lists `X` with the gloss 「死亡 (Dead) (Linux 2.6.0 以降)」,
  and a second dead letter `x` for Linux 2.6.33 to 3.13 only (`:1448-1450`). A
  discriminator must accept the letters its kernel revision defines, not only
  the ones one page happens to list.
- any live letter → world 3, or a live process with a readable command line.
  S472 glosses `D` as 「D 是在不可中斷的等待或交換態中睡眠」, placing swap-state
  sleep in `D`; `R`, `S` and `T` are live letters on both pages.
- `stat` unreadable while the `cmdline` read was empty → world 1.

A pid probe must therefore return three-valued evidence — present-and-alive,
present-but-dead, not-present — never the two-valued alive/absent. An
argv-substring probe never reads the state field, so it cannot decide between
the worlds even when it finds a match.

Two translation-level cautions:

- **The alphabets differ by revision.** S472 lists the set as `";RSDZT";` — no
  `X` — so a probe that took that page as its authority could not recognise a
  dead letter. S471's list (man-pages 3.79) carries `R`, `S`, `D`, `Z`, `T`,
  `t`, `W`, `X`, `x`, `K`, a second `W` (Waking) and `P`.
- **The two pages describe different objects when they talk about `comm`.**
  S471 says `stat`'s comm field is visible whether or not the executable is
  swapped out: 「実行形式がスワップアウトされているかどうかによらず、見ることができる。」
  S472 says the `comm` file's visibility depends on swap-out: 「該檔案是否可見取決於該檔案是否已被交換出記憶體.」
  A field of `stat` and the `comm` file are different objects, so the two
  sentences do not contradict each other; each page is silent on the other's
  object, and neither says a `stat` read cannot fail.

## What the lane already holds

- The zombie exception and its 0-character read, in English: S170
  (`proc_pid_cmdline.5` at man-pages 6.20). S170's recorded scope carries the
  zombie exception and states no swap-out branch.
- The English `stat` field list, including state letters `S`, `Z` and `X`: S171
  (`proc_pid_stat.5` at man-pages 6.20, `:49-50`, `:56-57`, `:69-70`).
- The reading that an empty `cmdline` read is not proof the process exited:
  `corpus/knowledge/watchdog-identity-r31.md:28`.

So this entry does not introduce the letters `Z` or `X` to the lane and does
not re-assert the zombie rule. It adds (a) the two translations' accounts, (b)
the swap-out world, stated only by a page targeting Linux 1.3.11, and (c) the
three-world conclusion with the state field as the discriminator.

## Boundaries — what this entry does not license

- **It is not a way to identify the watchdog daemon.** A state field says
  whether a pid is dead; it says nothing about which program holds the pid.
  FR5 stays open, the identity ground remains
  `corpus/knowledge/watchdog-identity-r31.md`, and neither opened page
  establishes daemon identity from a degraded probe.
- **It makes no claim about the lane's census.** It does not describe, endorse,
  measure or change the census probe, and it asserts nothing about what the
  census reports on any host or in any round. No probe, surface, finding id or
  threshold is added.
- **It is not current upstream.** The swap-out branch is stated by S472, whose
  遵循 section says the page targets Linux 1.3.11 and whose foot date is 22 July
  1996; the modern English contract the lane holds (S170) states the zombie
  exception only. Neither opened page dates the branch's removal, so this entry
  does not say it was retired at any revision — only that S170 does not carry
  it.
- **It does not enumerate the worlds exhaustively.** Neither page addresses a
  task whose argv is genuinely empty (a kernel thread, or `execve` with an empty
  argv); such a task would also read zero characters. The three worlds above are
  the ones the opened pages state plus the absent-pid reading a degraded probe
  reports.
- **`X` is a state name, not a retained entry.** S471 lists `X` as a state; it
  does not say that a task in that state keeps a readable `/proc/<pid>` entry.
- **A translation is not an authentication.** Where a translation diverges from
  upstream English, upstream English (S170, S171) wins.

## [INFERENCE]

- A live process is never in `X`. S471 glosses `X` as 死亡 (Dead) and bounds it
  by kernel revision; no cited line says a live task's `stat` can show it.
- A `stat` read succeeds in the swap-out world. S471 says `stat`'s comm field is
  visible regardless of swap-out, which implies the file is readable there;
  neither page says the read cannot fail.
- The error form of a read on a nonexistent pid (world 1, above).

## What it changes for mori

A pid probe that reads `/proc/<pid>/cmdline` must report three values and must
read `stat` field 3 before it concludes anything. An empty `cmdline` plus state
`Z` or `X` is present-but-dead; an empty `cmdline` plus a live letter is a live
process whose command line is not in memory; an empty `cmdline` with `stat`
unreadable is not-present — and only that last case may be reported as absence,
scoped to the query. No row here changes a probe.

## Delivery paths this cannot see

A `/proc` that is not mounted; a pid-namespace mismatch, where the state field
belongs to another namespace and says nothing about this one; a probe that reads
only `cmdline`; a process alive with a genuinely empty argv; kernels whose state
alphabet carries letters neither opened page lists.

## Fills

Coverage-map ground: FR5 (degraded-pgrep visibility and pid-probe conclusions).
Frontier row: `corpus/README.md` Round-44 coverage additions names this entry.
```

## 2. Requirement conformance

| requirement | where in the draft | check |
|---|---|---|
| `source:` lines with LANE ids | S471 (Ubuntu ja page), S472 (Arch zh_TW page), each `source:` on its own line and starting the id | id follows the document; no campaign ids |
| `verified-at: 2026-10-25` | line 4, date first in the cell | substring `verified-at:` present (count-c3 requirement) |
| `recheck: 180d — <one runnable command> -> <observed> (ran 2026-10-25)` | one line, one `python3 -c` command covering both pages, observed `ja 1 2 zh 1 2` | replayed 2026-10-25 (§3.4) |
| `coverage-map: FR5` | `coverage-map: FR5 — …` | `FR5` on the `coverage-map:` line (count-c3 requirement) |
| `ground:` quoting PROVINCE.md FR5 boundary | `ground:` line quotes the boundary verbatim with `PROVINCE.md:48` | `PROVINCE.md:48` read |
| three worlds | `## Claim`, numbered 1–3 | each tied to a source or marked `[INFERENCE]` |
| state-field discriminator | `## The discriminator — stat field 3` | `Z`/`X` from S471; live letters from both pages |
| Boundaries: not daemon identity | first boundary bullet | names `watchdog-identity-r31.md` as the identity ground |
| Boundaries: no claim about the lane's census | second boundary bullet | asserts nothing about census output |
| no absolute host paths in source cells | both `source:` cells | only URLs, page line anchors, release strings |
| no literal `|` in any proposed registry cell | draft contains no `|` at all | `grep -c '|'` on the draft text = 0 (the recheck command is pipe-free) |
| one file written | this report | `git status --porcelain` (§3.1) shows no edit by this seat |

## 3. Evidence

### 3.1 Lane and worktree state (read-only)

```
$ git -C /home/vgpnk/Projects/shokunin/mori-shokunin rev-parse HEAD
7cb59c6891d4f5d0266fe062565f094da835dc84

$ git status --porcelain
 M SCORECARD.md
 M corpus/QUALITY.md
 M corpus/README.md
 M corpus/SOURCES.md
 M corpus/lessons/round-43.md
?? .ufo/waves/round-44/w1-spec.json
?? .ufo/waves/round-44/w1/
?? corpus/knowledge/pid-probe-conclusion-r44.md
```

All modifications and the untracked entry are sibling/integration work; this seat
wrote only `.ufo/waves/round-44/w1/ScribeEntryDraft.md`.

### 3.2 Registry rows and the literal sweep

```
$ grep -cE '^ {0,3}\| *S[0-9]{3,} *\|' corpus/SOURCES.md
245

$ git grep -l 'Z ゾンビ' 7cb59c6891d4f5d0266fe062565f094da835dc84 -- corpus/ | wc -l
0

$ git grep -l 'Z ゾンビ' -- corpus/
corpus/README.md
corpus/SOURCES.md
```

(`git grep` does not search untracked files; the untracked entry also contains the
token. See F5 for the consequence for the contract's `After` value.)

S471/S472 rows are present in the worktree with 11 cells each:

```
$ awk -F'|' '/^ {0,3}\| *S47[12] *\|/{print $2, NF-2}' corpus/SOURCES.md
 S471  11
 S472  11
```

Both rows: `status` `mined`, `opened` `2026-10-25`, `recheck` `180d`, `used-by`
`corpus/knowledge/pid-probe-conclusion-r44.md`.

### 3.3 Census on the worktree registry, and on a staged copy

```
$ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file corpus/SOURCES.md
file	W04	S035 duplicate url … (19 W04 lines)
file	ok	/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md
exit=0

$ T=$(mktemp -d); cp corpus/SOURCES.md "$T/SOURCES.md"
$ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file "$T/SOURCES.md"
file	E11	S001 missing used-by corpus/lessons/2026-10-15-…md
… (E11 for every mined row, including S471 and S472)
file	E11	S471 missing used-by corpus/knowledge/pid-probe-conclusion-r44.md
file	E11	S472 missing used-by corpus/knowledge/pid-probe-conclusion-r44.md
exit=1
```

### 3.4 Recheck replay (2026-10-25)

The draft's single command:

```
$ python3 -c 'import urllib.request,html;g=lambda u:html.unescape(urllib.request.urlopen(u,timeout=40).read().decode());a=g("https://manpages.ubuntu.com/manpages/focal/ja/man5/proc.5.html");b=g("https://man.archlinux.org/man/proc.5.zh_TW");print("ja",a.count("一文字も返らない"),a.count("死亡 (Dead)"),"zh",b.count("返回零"),b.count("僵死"))'
ja 1 2 zh 1 2
```

The `2` in each pair is two occurrences: the ja page glosses both `X` and `x` as
`死亡 (Dead)`, and the zh page says `僵死` twice (the `cmdline` sentence and the
`state` gloss).

Rejected variants, measured:

```
$ curl -fsSL --max-time 40 '<ja url>' | python3 -c '…count("ゾンビ")…'
3
$ curl -fsSL --http1.1 --max-time 40 '<zh url>' | python3 -c '…count("僵死")…'
curl: (35) TLS connect error: error:0A000126:SSL routines::unexpected eof while reading
0
$ curl -fsSL --max-time 40 '<zh url>' | python3 -c '…count("僵死")…'   (three runs)
2
2
2
$ grep -c '僵死' <zh html>
0            # the page encodes non-ASCII as numeric character references
$ grep -c '僵死' <zh .raw>
2
```

### 3.5 Counter replay at WORK (read-only; writes only a temp dir)

Run 1, before a sibling edited `corpus/README.md` (entry then 4261 bytes):

```
$ python3 .ufo/waves/round-44/count-c3.py WORK --entry corpus/knowledge/pid-probe-conclusion-r44.md --row S471 --row S472
check entry_present    PASS (4261 bytes)
check entry_meta       PASS (sources S471,S472)
check rows_present     PASS (rows S471,S472 mined)
check census_ok        FAIL (exit=1)
check readme_row       FAIL (no line names the entry)
rev=WORK
C3=unmet
exit=1
```

Run 2, at 05:24:43 after `corpus/README.md` was rewritten at 05:20:43 and the entry
at 05:16:27:

```
$ ls -l --time-style=+%H:%M:%S corpus/README.md corpus/knowledge/pid-probe-conclusion-r44.md corpus/SOURCES.md
-rw-r--r-- 1 vgpnk vgpnk  72753 05:20:43 corpus/README.md
-rw-r--r-- 1 vgpnk vgpnk 242248 05:13:02 corpus/SOURCES.md
-rw-r--r-- 1 vgpnk vgpnk   5526 05:16:27 corpus/knowledge/pid-probe-conclusion-r44.md

$ python3 .ufo/waves/round-44/count-c3.py WORK --entry corpus/knowledge/pid-probe-conclusion-r44.md --row S471 --row S472
check entry_present    PASS (5526 bytes)
check entry_meta       PASS (sources S471,S472)
check rows_present     PASS (rows S471,S472 mined)
check census_ok        FAIL (exit=1)
check readme_row       PASS (names entry)
rev=WORK
C3=unmet
exit=1
```

The entry measured is the pre-existing untracked file, not this draft. `census_ok` is
the only failing check in run 2, and it fails for the reason in F1 — not for anything
in the entry, the rows or the README.

### 3.6 Quote presence

Every quoted fragment in §1 was checked against the pages with tags stripped and
entities decoded, whitespace removed on both sides:

```
JA PRESENT J1 zombie-empty sentence
JA PRESENT J2 Z gloss
JA PRESENT J3 X gloss
JA PRESENT J4 stat comm visible regardless
JA PRESENT J5 footer release 3.79 (tag-stripped)
ZH PRESENT C1 cmdline swap-or-dead
ZH PRESENT C2 comm visibility
ZH PRESENT C3 D gloss
ZH PRESENT C4 遵循 1.3.11
ZH PRESENT C5 state set
```

Page metadata read for the source cells: ja footer 「この man ページは Linux man-pages
プロジェクトのリリース 3.79 の一部である。」 (`:4756-4760`); zh package block
`extra/man-pages-zh_tw` version `1.6.4.5-1`, upstream `man-pages-zh` (`:931-940`),
遵循 「本手冊頁基本上是針對 Linux 1.3.11 核心」 (`:855-861`), foot date `22 July 1996`
(`:912`), `2000/11/26` (`:895`).

## 4. Findings

**F1 — blocking instrument defect: `census_ok` cannot pass at any revision.**
`count-c3.py` copies `corpus/SOURCES.md` into `tempfile.mkdtemp()` and runs
`bash <fleet>/scripts/sources-census.sh validate --file <tmp>/SOURCES.md`
(`count-c3.py:133-147`). `sources-census.sh:497-503` resolves the lane root as
`dirname(file_abs)/..`, and `:566` tests `[ ! -e "$dir/$path" ]` for every
`used-by` path. Staged one level under `/tmp`, `$dir` is the temp dir's parent,
so every relative `used-by` dangles: the staged run emits `E11` for **every**
mined row and exits 1 (§3.3), while the same registry validates exit 0 in place.
Consequence: `check census_ok FAIL (exit=1)` is unconditional for this repo, so
P-C3's `C3=met` is unreachable through the frozen counter — in run 2 (§3.5) it
is the only failing check. Per the contract's Freeze clause this is a lesson to
record and route to round 45, not a patch. (The counter's own selftest cannot
see it: its `honest` arm uses `fixtures/fake-census.sh`, which ignores
`validate --file`.)

**F2 — `readme_row` was failing, then a sibling fixed the README.**
The check is `entry.encode() in readme_body` (`count-c3.py:150-152`), i.e. the
literal `corpus/knowledge/pid-probe-conclusion-r44.md`. At run 1 (§3.5) the
frontier row named the entry as `knowledge/pid-probe-conclusion-r44.md` and the
counter printed `readme_row FAIL (no line names the entry)`. `corpus/README.md`
was rewritten at 05:20:43 and now carries the `corpus/`-prefixed path at `:632`;
run 2 prints `readme_row PASS (names entry)`. Recorded because the requirement is
a literal, not a relative path, and the row can regress on any edit.

**F3 — the untracked entry's recheck command is not reproducible as written.**
Its zh leg uses `curl --http1.1` and printed a TLS error followed by `0` on the
first replay (§3.4), against the asserted `2`. The same URL without `--http1.1`
gave `2` on three consecutive runs. The draft's single pipe-free `urllib`
command was replayed and printed `ja 1 2 zh 1 2`.

**F4 — novelty overlap with S171.** `corpus/SOURCES.md:177` (S171) already
teaches the `stat` field 3 letters `S`, `Z` and `X` at man-pages 6.20
`:49-50,:56-57,:69-70`. Both the untracked entry (05:16 version, Boundaries) and
`corpus/README.md:638` say the entry "adds the state alphabet"; that is true only
at the literal-token level (the contract's `before` sweep `git grep -l 'Z ゾンビ'`
= 0 files, §3.2), not at the ground level. The draft states the held ground
explicitly (`## What the lane already holds`) and claims only the translations'
accounts, the 1.3.11-era swap-out world and the three-world conclusion.

**F5 — the contract's `After` value for the sweep will not hold.** P-C3 says the
sweep at the landed tip yields `1 file`. At landing the token `Z ゾンビ` sits in
three tracked files: the entry, the S471 row (`corpus/SOURCES.md:250`) and the
frontier row (`corpus/README.md:630`). Currently 2 tracked matches + 1 untracked
entry (§3.2). The `before` value (`0`) is correct.

**F6 — "contradiction" compares two different objects.** `corpus/README.md:634-637`
says the swap-out world "is contradicted by the focal page's own `comm` sentence
for the same field", and the untracked entry (05:16) repeats it under
`## The swap-out branch is contradicted on the same desk` with "S471 states the
opposite for the same field". The focal sentence is about `stat`'s comm **field**
(`:1417-1420`); the zh sentence is about the `comm` **file** (`:270-271`).
Different objects: silence on one object is not a contradiction of the other
(§1, "Two translation-level cautions"). The same README row says the entry
"records it as retired rather than current" (`:636`); neither page dates a
removal, so the draft says only that S170 does not carry the branch. These are
README/entry-text conflicts for the canonical judge, not changes this seat may
make.

**F7 — two token traps in the zh page.** (a) The page line-splits the sentence,
so `返回零個字元` is not a literal in the page text (`返回零` then `個字元`); a
recheck counting it yields 0. The draft counts `返回零`. (b) The state set is
`";RSDZT";` — no `X` — so a discriminator taken from that page cannot recognise a
dead letter; the draft says so and takes `Z`/`X` from S471.

**F8 — the staged campaign entry's recheck commands are non-runnable as written.**
`curl -fsSL '<ja html>' | grep -c 'ゾンビプロセス'` → `0` and
`curl -fsSL '<zh html>' | grep -c '僵死'` → `0` on 2026-10-25 (both pages encode
non-ASCII as numeric character references), against the asserted `1` and `2`.
This is why the draft decodes entities in the command; the campaign file was
read only and is not adopted.

**F9 — the 05:16 entry mislocates the focal `comm` sentence.** Its S471 source
cell cites 節「/proc/[pid]/comm」 (`スワップアウトされているかどうかによらず`). The
only swap-out sentence on that page is in 節「/proc/[pid]/stat」 field (2) comm at
`:1417-1420`; the `/proc/[pid]/comm` file section (`:455-469`, "Linux 2.6.33
以降") contains no swap-out sentence at all — `grep -n 'スワップアウト'` on the
decoded page lists `:1419` (the stat field) plus five later occurrences outside
this region, none inside `:455-469`. A locator that
names the wrong section is a corpus defect under the fleet rule "A quote names
its location"; the draft's source cell cites `:1417-1420`.

## 5. Deltas from the untracked entry already at the copy target

The file `corpus/knowledge/pid-probe-conclusion-r44.md` is untracked and was
rewritten while this seat worked: 4261 bytes at 05:12, 5526 bytes at 05:16:27.
The deltas below are against the 05:16 version, which already satisfies the
shape requirements (`entry_meta` PASS, §3.5 run 2):

1. **Recheck** — replaces the flaky `--http1.1` leg (F3) with one pipe-free
   `urllib` command over both pages, observed `ja 1 2 zh 1 2`; the loose token
   `ゾンビ` (count `3`, any occurrence on the page) is replaced by tokens tied to
   the claims (`一文字も返らない`, `死亡 (Dead)`, `返回零`, `僵死`).
2. **Three worlds, stated as three** — the 05:16 entry says "Two worlds are
   grounded here, not three" in Boundaries while its Claim lists three; the draft
   keeps all three, scopes the swap-out one to S472's 1.3.11-era page, and keeps
   the absent-pid world with its error-vs-empty caveat marked `[INFERENCE]`.
3. **No "contradiction" claim** — replaces "S471 states the opposite for the
   same field" with the field-versus-file distinction (F6); the draft says the
   two pages are silent on each other's object.
4. **No "retired" claim** — neither page dates a removal; the draft says only
   that S170 does not carry the branch.
5. **Novelty** — adds `## What the lane already holds` naming S170, S171 and
   `watchdog-identity-r31.md:28`, so the entry does not claim to introduce the
   `Z`/`X` alphabet (F4).
6. **`X` marked `[INFERENCE]`** — "a live process is not in `X`" is an inference
   from a state-name list, not a sourced sentence; the 05:16 entry states it
   flatly.
7. **Anchors** — every quote carries a page line anchor, and the S471 cell cites
   the `stat` field (2) comm section rather than the `comm` file (F9).
8. **Census boundary** — restated as "makes no claim about the lane's census"
   (does not describe, endorse, measure or change the census probe), rather than
   "does not change the census".
9. **No `|` anywhere** in the draft (the recheck command is pipe-free), so the
   text can be quoted into a registry cell without escaping.

## 6. Out of scope and untouched

- Not edited: `corpus/SOURCES.md` (S471/S472 rows are sibling work),
  `corpus/README.md` (frontier row is sibling work), `corpus/QUALITY.md`,
  `SCORECARD.md`, `corpus/lessons/round-43.md`, `corpus/knowledge/pid-probe-conclusion-r44.md`,
  every frozen instrument (`contract.md`, `count-c1.py`, `count-c2.py`,
  `count-c3.py`, `tools/mori-gate-registry.py`, `fixtures/`), `SKILL.md`,
  `LOG.md`, the fleet repo and `/home/vgpnk/Projects/shokuknow`.
- No `git add/commit/push/checkout/stash/reset`, no mutating `jj`; all scratch
  work under `mktemp -d` (`/tmp/c3ground` for the page copies).
- No host `/proc` probe was run; the draft claims no host measurement.
- Known limits: quotes are whitespace-normalized joins of the pages' typeset
  lines (§3.6 checks characters, not line breaks); both pages are translations,
  so their wording is evidence about the translations, not about upstream
  English; the zh page is a 1996-dated document served from a 1.6.4.5-1 package.

Report: `.ufo/waves/round-44/w1/ScribeEntryDraft.md`
