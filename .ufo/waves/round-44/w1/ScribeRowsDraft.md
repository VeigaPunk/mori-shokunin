# ScribeRowsDraft — C3 registry rows S471, S472 (mori round 44, wave 1)

Seat: `L1Mori44-4.ScribeRowsDraft` (scribe, leaf). Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin`.
Instruments frozen at `7cb59c6891d4f5d0266fe062565f094da835dc84`; `HEAD` at run time = `7cb59c68`.
Run date: 2026-10-25. Scratch sandbox: `/tmp/mori44rows.EJYXKR` (nothing outside it and this report was written).
No frozen instrument, `SKILL.md`, `SCORECARD.md`, `LOG.md`, `corpus/` file, or sibling repo was edited. No git or jj mutation ran. No tool was installed or upgraded.

Deliverable: the two `corpus/SOURCES.md` registry rows for C3 (S471, S472), drafted as an append block, with the column, word-count and `|`-absence proofs the seat requires. The integration owner decides whether to replace the as-landed rows (§8).

## 1. Sources opened (CORPUS.md rule 1: a row is written only after opening the source this round)

```
curl -fsSL --max-time 60 'https://manpages.ubuntu.com/manpages/focal/ja/man5/proc.5.html' -o S471.html   # exit 0
curl -fsSL --max-time 60 'https://man.archlinux.org/man/proc.5.zh_TW'            -o S472.html   # exit 0
wc -c: 376399 S471.html / 61889 S472.html
sha256: f64b0cded10f755e6135f8d9d4aba8f5c769290128572f92faad1dc5a2c6364b  S471.html
        b8ede81db8d462b46f5312b392caab7c5fe8d125057ca6093c2d3152efba8be7  S472.html
```

Page-own revision markers, read from the served pages (not inferred):

- S471 — `Provided by: manpages-ja (Version: 0.5.0.0.20180315+dfsg-1)`, Ubuntu `focal` (20.04) ja rendering, served by `Ubuntu Manpage Operator`.
- S472 — `Package name: extra/man-pages-zh_tw`, `Version: 1.6.4.5-1`, `Upstream: https://github.com/man-pages-zh/manpages-zh`, `[中文版最新更新] 2000/11/26`, page footer `22 July 1996 Linux Programmer's Manual`.

Both pages encode CJK as numeric character references (`&#x30BE;…`), so a raw-HTML grep for a word returns 0. Text was extracted by stripping tags and `html.unescape`; all quotes below are from that decode and were re-checked against the raw byte stream.

## 2. Located positions and grounding quotes (Gate input)

S471 — section `/proc/[pid]/cmdline`:

> 「この読み出し専用のファイルはプロセスの完全なコマンド行を保持する。ただし、そのプロセスがゾンビプロセスの場合は、このファイルは空となる。つまり、このファイルを読み出しても一文字も返らない。」

S471 — section `/proc/[pid]/stat`, field `(3) state`, entries `Z` and `X`:

> 「Z ゾンビ (Zombie)」 / 「X 死亡 (Dead) (Linux 2.6.0 以降)」

S471 — section `/proc/[pid]/stat`, field `(2) comm`:

> 「実行形式がスワップアウトされているかどうかによらず、見ることができる。」

S472 — section `cmdline` (page permalink `#cmdline`):

> 「該檔案儲存了程序的完整命令列. 如果該程序已經被交換出記憶體, 或者該程序已經僵死, 那麼就沒有任何東西在該檔案裡, 這時候對該檔案的讀操作將返回零個字元.」

S472 — section `stat`, field `state` (page permalink `#state`):

> 「";RSDZT"; 中的一個, R 是正在執行, S 是在可中斷的就緒態中睡眠, D 是在不可中斷的等待或交換態中睡眠, Z 是僵死, T 是被跟蹤或被停止(由於收到訊號).」

S472 — section `stat`, field `comm` (page permalink `#comm`):

> 「該檔案是否可見取決於該檔案是否已被交換出記憶體.」

Anchor capability actually observed, not assumed: S472 wraps each section heading in `<a class="permalink" href="#cmdline">`, and exposes `id="cmdline" id="stat" id="state" id="comm"`; it has no line anchors (`grep -coE 'id="l[0-9]+"|href="#l[0-9]+"'` = 0). S471 has no `id` or permalink for `/proc/[pid]/cmdline`, `/proc/[pid]/stat`, or `comm` (`grep -oE 'id="[^"]*(cmdline|stat|status)[^"]*"'` = no output) and no line anchors (same grep = 0); its per-section ids belong to `/proc/stat` fields (`rchar`, `btime`, `cpu`, …). Both rows therefore locate by heading name, and say so.

## 3. The append block (exact bytes, lane 11-column schema)

Append after `| S470 |` in the `## Registry` table:

```
| S471 | proc(5) 日本語訳 (Ubuntu 20.04 focal, manpages-ja) — https://manpages.ubuntu.com/manpages/focal/ja/man5/proc.5.html | docs | A | the Japanese manpages-ja rendering of the /proc/[pid]/stat state alphabet (Z ゾンビ, X 死亡 since Linux 2.6.0), of the zombie cmdline zero-character read, and of comm visibility regardless of swap; not the upstream English contract, which the lane holds as S170 and S171, and not a probe recipe | 節「/proc/[pid]/cmdline」, 節「/proc/[pid]/stat」の (2) comm 欄 and (3) state 欄; this rendering exposes no per-section or line anchor for any of these headings (no id and no permalink, checked 2026-10-25), so the headings locate it; package manpages-ja 0.5.0.0.20180315+dfsg-1, Ubuntu focal (20.04); opened 2026-10-25 | The Japanese proc(5) lists Z ゾンビ and X 死亡 as stat states, and a zombie's cmdline read returns no character. | mined | 2026-10-25 | 180d | corpus/knowledge/pid-probe-conclusion-r44.md |
| S472 | proc(5) 中文翻譯 (Arch Linux zh_TW, man-pages-zh_tw) — https://man.archlinux.org/man/proc.5.zh_TW | docs | B | the LDP-era zh_TW rendering of the cmdline zero-character read, naming a swapped-out or zombie process, of comm visibility under swap, and its five-letter state alphabet RSDZT with no X; not the upstream English contract and not a current-revision statement of any of the three | section cmdline (page permalink #cmdline), section stat fields state (#state) and comm (#comm); the page exposes section permalinks only, no line anchors; package extra/man-pages-zh_tw 1.6.4.5-1, Chinese translation last updated 2000/11/26, page dated 22 July 1996; opened 2026-10-25 | The zh_TW proc(5) names a swapped-out or zombie process as its zero-character cmdline cases, and its state field lists only RSDZT. | mined | 2026-10-25 | 180d | corpus/knowledge/pid-probe-conclusion-r44.md |
```

Column-by-column conformance:

| cell | required | drafted | evidence |
|---|---|---|---|
| id | next unused, never reused | S471, S472 | registry at `7cb59c68`: 243 rows, max id S470, no S471/S472 (`git show 7cb59c68:corpus/SOURCES.md`); campaign id-space conflict in §9.3 |
| source | title — canonical URL | title + `— https://…` | §1 fetch, exit 0 |
| kind | enum | `docs` | both are man-page renderings |
| tier | A/B/C scoped | A (ja) / B (zh_TW) | §5 tier rationale |
| scope | claim the tier applies to | narrowed, names what it is not | §5 |
| anchor | section/heading + line anchors if exposed, plus revision | headings, permalink/`no anchor` statement, package version, access date | §2 |
| teaches | one sentence, ≤25 words | 20 / 21 words | §6 |
| status | enum | `mined` | seat requirement; entry cites both ids |
| opened | ISO date | 2026-10-25 | seat requirement; sources opened this round |
| recheck | ISO date or cadence | `180d` (bare) | seat requirement |
| used-by | repo-relative path(s) or `—` | `corpus/knowledge/pid-probe-conclusion-r44.md` | entry exists at `HEAD` worktree and carries `source: S471` / `source: S472` |

## 4. Proof: no literal or escaped `|` in any cell

```
$ awk -F'|' '{print NF}' rows.txt
13
13
$ grep -c '\\|' rows.txt
0
```

Counter's own parser (`FIELDS = re.compile(r"(?<!\\)\|")`, `cells = FIELDS.split(line.strip().strip("|"))`, `.ufo/waves/round-44/count-c3.py:32,82`):

```
11 cells; id=S471 tier=A status=mined opened=2026-10-25 recheck=180d used=corpus/knowledge/pid-probe-conclusion-r44.md
11 cells; id=S472 tier=B status=mined opened=2026-10-25 recheck=180d used=corpus/knowledge/pid-probe-conclusion-r44.md
```

Both parsers agree on 11 cells and on `status=mined` / `used-by` naming the entry (`count-c3.py` reads `cells[7]` and `cells[10]`).

**The seat's stated expectation does not hold, and is reported rather than faked.** The seat says `awk -F'|' '{print NF}'` must give "12 fields for an 11-column row". A lane row carries a leading *and* a trailing pipe, so 11 cells + 2 boundary delimiters = 13 fields; that is exactly what `CORPUS.md`'s frozen census requires (`# malformed rows — 11 columns means NF=13; must print 0`). 12 is what the same row gives once the trailing pipe is removed:

```
$ sed 's/|$//' rows.txt | awk -F'|' '{print NF}'
12
12
```

and such a row is malformed under the lane census (E01 `NF!=13`). The rows are drafted in lane format (NF=13, 11 cells); the "12" figure is not reproducible for a valid lane row.

## 5. Tier and scope rationale (curation, not truth)

- **S471 = A.** The scope is *the Japanese rendering itself* — what the Ubuntu-shipped `manpages-ja` page states and where — not the upstream contract, which the lane already holds at tier A in English (`S170` `proc_pid_cmdline(5)`, `S171` `proc_pid_stat(5)`). The page is the primary artifact for its own wording, is a human translation shipped in an official Ubuntu package, and carries kernel-version qualifiers (`X` since Linux 2.6.0; `t` since 2.6.33). Lane contrast: `S241` is tier B because it is a *machine-translated vendor* page, not a shipped translation of a man page. If the reviewer holds that no translation may ever be tier A, the same row at B still supports the entry — tier is not scored by any frozen instrument.
- **S472 = B.** It tracks an LDP-era revision: page date `22 July 1996`, Chinese update `2000/11/26`, package `man-pages-zh_tw 1.6.4.5-1`. Its state field is `";RSDZT";` — five letters, no `X`, no `K`/`P`, no `t` — so it cannot ground a current-revision state claim. Its unique content is the *swapped-out* branch and the `comm`-visibility sentence, both stated as this page's claims and scoped as such.
- Neither scope repeats `S170`/`S171`; both name them as the held English contract.

## 6. teaches word counts

```
$ awk -F'|' '{t=$8; gsub(/^ +| +$/,"",t); n=split(t,a," "); print NR": "n" words"}'
1: 20 words
2: 21 words
```

`$8` is the teaches cell (`$1` is the empty field before the leading pipe). Both are one sentence and under 25 words.

## 7. Census on the staged registry (read-only)

The live `corpus/SOURCES.md` already carries S471/S472 as **uncommitted** insertions (`git diff --numstat corpus/SOURCES.md` → `2 0`). To test *my* drafted cells rather than the landed ones, the sandbox holds a mirrored repo root (`/tmp/mori44rows.EJYXKR/repo`: symlinks to every lane top-level entry and every `corpus/` entry, with `corpus/SOURCES.md` a real staged file = live registry, landed S471/S472 removed, drafted rows inserted after S470).

```
$ bash scripts/sources-census.sh validate --file /tmp/mori44rows.EJYXKR/repo/corpus/SOURCES.md --today 2026-10-25   # (fleet-root scripts/)
file	ok	/tmp/mori44rows.EJYXKR/repo/corpus/SOURCES.md
EXIT=0
```

Only pre-existing `W04` duplicate-URL warnings were emitted (none for S471/S472; different URLs). The `CORPUS.md` manual census block on the same staged file:

```
rows: 245
malformed: 0
dupes: 0
enum-violations: 0
missing-used-by: 0
```

Live registry, same tools, unmodified file:

```
$ bash scripts/sources-census.sh validate --file corpus/SOURCES.md --today 2026-10-25
file	ok	/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md
EXIT=0
$ bash scripts/sources-census.sh census --file corpus/SOURCES.md
file	rows	245
file	tier.A	214
file	tier.B	14
file	tier.C	17
file	status.mined	194
```

## 8. Divergence from the rows already in the worktree

The integration owner had already appended S471/S472 to the worktree before this seat ran (`git status`: `M corpus/SOURCES.md`, 2 insertions; `corpus/knowledge/pid-probe-conclusion-r44.md` untracked). They are semantically the same rows on id/source/kind/status/opened/recheck/used-by. Differences, all in the two free-text cells:

1. **S471 anchor** — landed: `節「/proc/[pid]/cmdline」 and 節「/proc/[pid]/stat」の state 欄 (…); Ubuntu focal (20.04) ja 翻訳; fetched 2026-10-25`. Drafted adds the package revision (`manpages-ja 0.5.0.0.20180315+dfsg-1`), the `(2) comm` field the entry actually cites, and the explicit statement that this rendering exposes no section or line anchor.
2. **S471 scope** — landed omits `comm`; the entry's `source: S471` line cites the `comm` sentence, so the landed scope does not cover a position its `used-by` entry cites.
3. **S472 anchor** — landed: `「cmdline」段; Arch Linux man page, zh_TW; fetched 2026-10-25`. It names no page-exposed permalink (`#cmdline`, `#stat`, `#state`, `#comm`), no package version, no translation date, and does not name the `stat`/`comm` ground its own scope claims.
4. **S472 scope** — landed claims `including a swap-out branch the modern English contract the lane holds does not state`. The bytes of `S170` carry that branch as a roff comment, not in the body: `.\" In Linux 2.3.26, this also used to be true if the process was swapped out.` (line 15 of `proc_pid_cmdline.5` at `man-pages-6.20`); the body says only `unless the process is a zombie.` (line 14). The clause is true for the body contract and false for the page's full bytes as written, so the draft drops the comparative clause.
5. **S471 source title** — landed `(Ubuntu 20.04 focal)`; drafted adds `manpages-ja`, the package that fixes the revision.

Because the landed rows are **uncommitted**, replacing them now is not an append-only violation of a committed row (CORPUS.md rule 2 governs committed bytes). After commit, the same correction would need a new `supersedes S471 —` row.

## 9. Frozen-instrument verdict and conflicts (reported, not patched)

### 9.1 C3 at the worktree — FAIL, and the cause is inside the frozen counter

```
$ python3 .ufo/waves/round-44/count-c3.py WORK --entry corpus/knowledge/pid-probe-conclusion-r44.md --row S471 --row S472
check entry_present    PASS (5526 bytes)
check entry_meta       PASS (sources S471,S472)
check rows_present     PASS (rows S471,S472 mined)
check census_ok        FAIL (exit=1)
check readme_row       PASS (names entry)
rev=WORK
C3=unmet
EXIT=1
```

The same counter over the registry carrying *my* drafted rows (`--repo` = the mirrored sandbox root, `--census` = the fleet census):

```
check entry_present    PASS (5526 bytes)
check entry_meta       PASS (sources S471,S472)
check rows_present     PASS (rows S471,S472 mined)
check census_ok        FAIL (exit=1)
check readme_row       PASS (names entry)
C3=unmet
EXIT=1
```

Cause, reproduced independently of the lane: `count-c3.py:133-144` stages the registry as `/tmp/c3-*/SOURCES.md` and runs the census with `--file` only; the census resolves each `used-by` path against the *grandparent of the staged file* (`sources-census.sh:497-502, 566`), i.e. `/tmp`. Same committed bytes, staged in `/tmp`:

```
$ T=$(mktemp -d); cp corpus/SOURCES.md "$T/SOURCES.md"
$ bash scripts/sources-census.sh validate --file "$T/SOURCES.md" > out; echo EXIT=$?
EXIT=1
E11 lines: 279   (E-codes: 279)
```

Same bytes under a repo root → `file ok`, exit 0 (§7). So `census_ok` is unreachable at any revision and the contract's P-C3 "After" (`C3=met`) cannot be printed by this instrument as frozen. The counter's `--selftest` cannot see it because it substitutes a fixture census:

```
$ python3 .ufo/waves/round-44/count-c3.py --selftest | tail -4
selftest PASS red_census_unmet
selftest PASS readme_without_row_unmet
selftest PASS missing_coverage_map_unmet
C3_SELFTEST pass=6 fail=0
EXIT=0
```

Per the contract's `## Freeze`, a post-freeze defect is recorded and routed, never patched in place: this seat did not edit `count-c3.py`, `sources-census.sh`, or any fixture.

### 9.2 Conflict — seat's "12 fields" vs the frozen census's "NF=13"

Quoted verbatim, seat: `print the row with \`awk -F'|' '{print NF}'\` -> 12 fields for an 11-column row`. Quoted verbatim, `CORPUS.md` census: `# malformed rows — 11 columns means NF=13; must print 0`. Both cannot hold for a lane-format row; §4 shows the measured 13 (and the 12 that a missing trailing pipe produces).

### 9.3 Conflict — round-43 id-space sentence vs round-44 ids

`.ufo/waves/round-43/assimilation/guard/collisions-post.txt` (2026-10-24T22:37:14-03:00) states verbatim: `Free id space at this round's end: S471, then S475+ (S472-S474 are the campaign's own tail rows).` The round-44 contract states verbatim: `registry 245 rows (S471, S472) with census exit 0`. Under the round-43 rule the free lane ids would be S471 and S475+, not S471+S472. The round-43 rule also fixes which side yields: `the lane ids stand and the staged ids are shadowed`, and the campaign's staged S471/S472 are different documents (gihyo.jp cgroup-v2 articles, `/home/vgpnk/Projects/shokuknow/merge/mori/SOURCES.append.md:7-8`). The ids here follow the document, not arithmetic; the collision is with the campaign's *provisional* numbering, not with a lane row.

### 9.4 Conflict — the two pages disagree on `comm` under swap

- S471, `stat` field `(2) comm`: 「実行形式がスワップアウトされているかどうかによらず、見ることができる。」 (visible *regardless* of swap).
- S472, `stat` field `comm`: 「該檔案是否可見取決於該檔案是否已被交換出記憶體.」 (visibility *depends* on swap).

This is version drift, not translation noise: the S472 rendering is a 1996/2000 LDP-era page. The drafted S472 scope says `not a current-revision statement of any of the three`, so neither row silently flattens the disagreement. The knowledge entry already treats it as a contradiction section; these rows do not adjudicate it.

### 9.5 Located-position defect in the entry (not my file, reported)

`corpus/knowledge/pid-probe-conclusion-r44.md:3` cites S471's comm sentence at `節「/proc/[pid]/comm」`. That sentence is not in the `/proc/[pid]/comm` section of the page; it is in 節「/proc/[pid]/stat」, field `(2) comm` (single occurrence in the decoded page: `grep -c 'スワップアウトされているかどうか'` → 1, in the stat field list). CORPUS.md requires that a quote name its location. My S471 anchor names the stat `(2) comm` field, so the row does not repeat the mislocation.

### 9.6 Recheck commands against raw HTML return 0 (entity encoding)

The staged campaign entry's recheck lines (`/home/vgpnk/Projects/shokuknow/merge/mori/knowledge/corpus/knowledge/probe-absent-vs-dead-r39.md:7-8`) claim `grep -c 'ゾンビプロセス'` → 1 and `grep -c '僵死'` → 2. Run today, verbatim:

```
$ curl -fsSL 'https://manpages.ubuntu.com/manpages/focal/ja/man5/proc.5.html' | grep -c 'ゾンビプロセス'
0     (exit 1)
$ curl -fsSL 'https://man.archlinux.org/man/proc.5.zh_TW' | grep -c '僵死'
0     (exit 1)
```

Both pages entity-encode CJK, so the counts are right only after `html.unescape`: decoded `ゾンビプロセス` = 1, `一文字も返らない` = 1, `僵死` = 2, on the fetched bytes. The r44 entry already decodes (`| python3 -c 'import sys,html; …'`); the r39 staged entry does not, and its bare `grep` lines are not reproducible. Also noted: the r39 staged entry quotes 「…このファイルは空となります。…」 while the page reads 「…このファイルは空となる。…」 (plain form); the r44 entry quotes the page verbatim.

## 10. Out of scope, not done

- No edit to `corpus/SOURCES.md`, `corpus/README.md`, `corpus/knowledge/pid-probe-conclusion-r44.md`, `SKILL.md`, `SCORECARD.md`, `LOG.md`, the contract, counters, `tools/mori-gate-registry.py`, or `fixtures/`.
- No commit, push, checkout, stash, reset, or jj mutation; no write to the fleet root, `shokuknow`, or any sibling repo (the fleet census script and staged campaign files were read/executed read-only; the census was invoked with `--file` into a sandbox copy).
- No fix to the C3 instrument defect in §9.1 (frozen; routed to the lesson/round 45).
- Not verified: whether the `man-pages` upstream English page states the swap-out branch anywhere in its body beyond the `2.3.26` roff comment — only the S170 bytes at `man-pages-6.20` were read (lines 14-15).

## 11. Artifacts

- This report: `.ufo/waves/round-44/w1/ScribeRowsDraft.md` (the only file written).
- Scratch (not committed, disposable): `/tmp/mori44rows.EJYXKR/` — `S471.html`, `S472.html`, `S471.txt`, `S472.txt`, `S170.txt`, `rows.txt`, `SOURCES.staged.md`, `repo/` (mirrored root with the staged registry).
- Frozen verdicts quoted above: `C3=unmet` (worktree and drafted-row registry), `census_ok FAIL (exit=1)`, `C3_SELFTEST pass=6 fail=0`; census `file ok` exit 0 on both the staged and the live registry.
