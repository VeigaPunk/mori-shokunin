# Mo81Sc02Source — round 81 w1 source pin (C1 B6 ground)

Seat: scout, leaf member (no subagent dispatch). Lane root `/home/vgpnk/Projects/shokunin/mori-shokunin`.
Access date for every fetch and every line read below: **2026-11-04**.

**Verdict.** Two rows proposed for admission, one candidate rejected.

| disposition | id | carrier | what it grounds |
|---|---|---|---|
| ADMIT (queued) | **S596** | stat(2), man-pages 6.19 | the file type is carried in `st_mode`; `S_IFDIR` and `S_IFREG` are alternative cases of one `S_IFMT` selector, so a path that exists as a directory is not a regular file |
| ADMIT (queued) | **S597** | git-ls-tree(1) | the entering B6 mechanism: default field 2 is the object type, and `-t` makes tree entries appear under `-r`, so `objecttype == tree` at path P reports P as a directory, not a blob |
| REJECT | none (S068 carries the URL) | Python 3.15.2 `os` page | `os.scandir`/`DirEntry` is a directory-listing API, not the r80 C3 path test; the canonical URL is already S068 at `corpus/SOURCES.md:74` (QUALITY 155) |

The prompt's candidate 2 (`docs.python.org/3/library/os.html`) was opened, pinned and
screened, and is the rejected candidate. `git-ls-tree(1)` was opened because the entering
B6 counter does not stat or list-directory a path at all: it runs
`git ls-tree -r --name-only` (**§5**). The source that grounds the fixture's code path is
therefore git's object-type field, not `st_mode` and not `DirEntry`.

## 1. Files produced

| absolute path | sha256 | lines | bytes |
|---|---|---|---|
| `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/evidence/sources-r81/stat.2.man-pages-6.19.html` | 0067346ded7cc8259ad614874993bd99b3edff372b61057d236c9dfe5e40501e | 544 | 25836 |
| `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/evidence/sources-r81/git-ls-tree.html` | ff06fbc8b15b0fee505a259e4dc54096c9fba0460f4f02b449d55ecce7818267 | 1873 | 39083 |
| `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/evidence/sources-r81/python-os-3.15.2.html` | ee706c46011ab0f4767fa54fe8f39dfdb2d93d3ac5696aeb0478f7acce87ec41 | 7318 | 791358 |
| `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/evidence/sources-r81/README.md` | (prose; 1326 bytes) | — | 1326 |
| `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-81/w1/Mo81Sc02Source.md` | this report | — | — |

`corpus/evidence/sources-r81/` did not exist before this seat (`ls` returned rc 2); the
directory and its README are new. No other path was created or modified.

**Commit state (not my act).** While this seat was still writing, the L1 committed the four
evidence files as `075574c8` ("round-81: pinned source bytes for S596 (stat(2) man-pages
6.19) with the fetch index", 2026-11-04T03:54:03-03:00). For every file the worktree blob
equals HEAD's (`git rev-parse HEAD:<path>` equals `git hash-object <path>`:
`stat.2…` 72e53f68…, `git-ls-tree.html` f9dfe2c9…, `python-os-3.15.2.html` d8ad3676…,
`README.md` 14e99a05…). This seat ran no `git add`/`commit` and no other mutation; the
commit is the L1's.

Line-count nuance: `wc -l` on `python-os-3.15.2.html` prints 7318 because its final line
has no trailing newline (last byte `>`, 7318 `\n` bytes); git reports 7319 insertions for
the same file. The sha256 is unaffected.

## 2. Fetch receipts (two independent fetches per page, byte-compared)

```
$ curl -sSL -o stat.2.html -w 'STAT %{http_code} %{size_download} %{url_effective}\n' https://man7.org/linux/man-pages/man2/stat.2.html
STAT 200 25836 https://man7.org/linux/man-pages/man2/stat.2.html
$ curl -sSL -o os.html     -w 'OS %{http_code} %{size_download} %{url_effective}\n'   https://docs.python.org/3/library/os.html
OS 200 791358 https://docs.python.org/3/library/os.html
$ curl -sSL -o git-ls-tree.html -w 'LSTREE %{http_code} %{size_download}\n' https://git-scm.com/docs/git-ls-tree
LSTREE 200 39083
```

Second fetch of each, then `cmp`:

```
$ cmp -s stat.2.html stat.2.fetch2.html && echo STAT_IDENTICAL || echo STAT_DIFFERS
STAT_IDENTICAL
$ cmp -s os.html os.fetch2.html && echo OS_IDENTICAL || echo OS_DIFFERS
OS_IDENTICAL
$ cmp -s git-ls-tree.html git-ls-tree.fetch2.html && echo LT_IDENTICAL || echo LT_DIFFERS
LT_IDENTICAL
$ sha256sum stat.2.html stat.2.fetch2.html os.html os.fetch2.html
0067346ded7cc8259ad614874993bd99b3edff372b61057d236c9dfe5e40501e  stat.2.html
0067346ded7cc8259ad614874993bd99b3edff372b61057d236c9dfe5e40501e  stat.2.fetch2.html
ee706c46011ab0f4767fa54fe8f39dfdb2d93d3ac5696aeb0478f7acce87ec41  os.html
ee706c46011ab0f4767fa54fe8f39dfdb2d93d3ac5696aeb0478f7acce87ec41  os.fetch2.html
$ sha256sum git-ls-tree.html git-ls-tree.fetch2.html
ff06fbc8b15b0fee505a259e4dc54096c9fba0460f4f02b449d55ecce7818267  git-ls-tree.html
ff06fbc8b15b0fee505a259e4dc54096c9fba0460f4f02b449d55ecce7818267  git-ls-tree.fetch2.html
$ wc -lc corpus/evidence/sources-r81/*.html
  1873  39083 corpus/evidence/sources-r81/git-ls-tree.html
  7318 791358 corpus/evidence/sources-r81/python-os-3.15.2.html
   544  25836 corpus/evidence/sources-r81/stat.2.man-pages-6.19.html
```

HTTP `Last-Modified`: stat(2) `Mon, 02 Nov 2026 20:20:30 GMT`; os page
`Wed, 04 Nov 2026 03:29:24 GMT`; git-ls-tree `Mon, 02 Nov 2026 06:50:41 GMT`.

Page revisions as the bytes state them: stat(2) is **man-pages 6.19**, page date
2026-02-08, HTML rendering created 2026-09-09 (`:363`, `:373`, `:472`); git-ls-tree changelog
says "git-ls-tree last updated in 2.42.0" with "2.42.1 → 2.56.0 no changes" (`:1322`,
`:1328`); the os page is the **Python 3.15.2** build, "Last updated on Nov 04, 2026
(03:27 UTC)" (`:7308`).

## 3. Candidate 1 — stat(2), man-pages 6.19 → proposed S596

URL `https://man7.org/linux/man-pages/man2/stat.2.html`, HTTP 200, 25836 bytes,
pin `corpus/evidence/sources-r81/stat.2.man-pages-6.19.html`.

### 3.1 Duplicate sweep (run before the row was drafted)

```
$ grep -n 'man7\.org/linux/man-pages/man2/stat\.2\.html' corpus/SOURCES.md ; echo rc=$?
rc=1
$ grep -n 'man2/stat\.2' corpus/SOURCES.md ; echo rc=$?
rc=1
$ grep -n 'stat(2)' corpus/SOURCES.md ; echo rc=$?
rc=1
$ grep -n '0067346ded7cc825' corpus/SOURCES.md ; echo rc=$?
rc=1
$ grep -n 'stat\.3type' corpus/SOURCES.md ; echo rc=$?
rc=1
$ grep -n '^| S596 \|^| S597 ' corpus/SOURCES.md ; echo rc=$?
rc=1
```

No canonical-URL hit, no sha256 hit, no prose hit. The one neighbouring man2 row is S541
(`statfs(2)`, `corpus/SOURCES.md:321`) — a different page and a different struct. The id is
free (`S595` is the registry's max id and the last row). `grep -c '^| S[0-9]\{3\}'` was 368
rows at sweep time.

### 3.2 Located quotes (exact pinned bytes; the pin stores HTML, so tags are part of the text)

Primary quote, **:235-236**, 19 words (raw and rendered both 19; verified as two
single-line fragments because the checker's SPEC is one line per item):

```
valid information only in the <i>st_size</i> field and the file type of the <i>st_mode</i> field of the <i>stat</i> structure.
```

Context (`corpus/evidence/sources-r81/stat.2.man-pages-6.19.html`):

```
:234        According to POSIX.1-2001, <b>lstat</b>() on a symbolic link need return
:235        valid information only in the <i>st_size</i> field and the file type of
:236        the <i>st_mode</i> field of the <i>stat</i> structure.  POSIX.1-2008 tightens
:237        the specification, requiring <b>lstat</b>() to return valid information
```

Supporting quotes, the EXAMPLES program's one type selector:

```
:315                   printf("File type:                ");
:316  (blank)
:317                   switch (sb.st_mode &amp; S_IFMT) {
:318                   case S_IFBLK:  printf("block device\n");            break;
:319                   case S_IFCHR:  printf("character device\n");        break;
:320                   case S_IFDIR:  printf("directory\n");               break;
:321                   case S_IFIFO:  printf("FIFO/pipe\n");               break;
:322                   case S_IFLNK:  printf("symlink\n");                 break;
:323                   case S_IFREG:  printf("regular file\n");            break;
:324                   case S_IFSOCK: printf("socket\n");                  break;
```

- `:317` `switch (sb.st_mode &amp; S_IFMT) {` — 5 words.
- `:320` `case S_IFDIR:  printf("directory\n");               break;` — 4 words.
- `:323` `case S_IFREG:  printf("regular file\n");            break;` — 5 words.

`:320` and `:323` are alternative `case` labels of the same switch on
`st_mode & S_IFMT`; the page prints "File type:" immediately above it. That is the whole
of the exclusivity evidence: the man page has **no normative sentence** "a directory is
not a regular file" (`grep -n 'file type\|S_IFMT'` returns only `:235`, `:317`).

### 3.3 Anchor-check receipt (lane checker, run against the installed pin)

```
$ python3 -I tools/mori-anchor-check.py --pin corpus/evidence/sources-r81/stat.2.man-pages-6.19.html \
    --check "s596a|235|12|valid information only in the <i>st_size</i> field and the file type of" \
    --check "s596b|236|7|the <i>st_mode</i> field of the <i>stat</i> structure." \
    --check "s596c|317|5|switch (sb.st_mode &amp; S_IFMT) {" \
    --check "s596d|320|4|case S_IFDIR:  printf(\"directory\n\");               break;" \
    --check "s596e|323|5|case S_IFREG:  printf(\"regular file\n\");            break;"
anchor item=s596a span=235 verdict=ok located_on=235 occurrences=1 words_counted=12 words_recorded=12
anchor item=s596b span=236 verdict=ok located_on=236 occurrences=1 words_counted=7 words_recorded=7
anchor item=s596c span=317 verdict=ok located_on=317 occurrences=1 words_counted=5 words_recorded=5
anchor item=s596d span=320 verdict=ok located_on=320 occurrences=1 words_counted=4 words_recorded=4
anchor item=s596e span=323 verdict=ok located_on=323 occurrences=1 words_counted=5 words_recorded=5
ANCHOR_CHECK: PASS items=5 ok=5 pin_sha256=0067346ded7cc8259ad614874993bd99b3edff372b61057d236c9dfe5e40501e pin_bytes=25836
rc=0
```

### 3.4 Proposed 11-column Registry row

```
| S596 | Linux man-pages 6.19 stat(2) — https://man7.org/linux/man-pages/man2/stat.2.html | docs | A | the page's own EXAMPLES program and its HISTORY sentence: a path's file type is carried in the st_mode field, and one switch on st_mode & S_IFMT prints S_IFDIR as "directory" and S_IFREG as "regular file" as alternative cases. Not a normative definition of "regular file", not a stat call the lane makes, and not any live filesystem read. | EXAMPLES "File type:" then switch (sb.st_mode & S_IFMT):317, case S_IFDIR:320, case S_IFREG:323; HISTORY "the file type of the st_mode field of the stat structure":235-236; man-pages 6.19, page date 2026-02-08, HTML rendering 2026-09-09; sha256 0067346ded7cc8259ad614874993bd99b3edff372b61057d236c9dfe5e40501e; copy corpus/evidence/sources-r81/stat.2.man-pages-6.19.html; 544 lines, 25836 bytes | A path's type is read from st_mode's type bits; a directory (S_IFDIR) and a regular file (S_IFREG) are alternative cases of one selector, so a path that exists as a directory is not a regular file. Limit: the page demonstrates this in its example, not in a normative exclusivity sentence. | queued | 2026-11-04 | on-release | corpus/knowledge/record-claim-integrity-r81.md |
```

`used-by` is not `—` because `corpus/knowledge/record-claim-integrity-r81.md:1` already
cites S596 and this pin (the seat template's `—` is the pre-use default; filling the real
citation is the accurate cell). `corpus/knowledge/record-claim-integrity-r81.md` is another
seat's file and was not edited by me.

### 3.5 Limit of this row (do not let the Gate over-read it)

The HISTORY sentence is a statement about what POSIX.1-2001 required `lstat()` on a
symbolic link to return, not a general field-table entry; the EXAMPLES switch is a
demonstration program. Together they support "the type bits live in `st_mode` and
`S_IFDIR`/`S_IFREG` are disjoint `S_IFMT` cases". They do not support a normative
definition of a regular file, nor any claim about a path on this host.

## 4. Candidate 2 — Python 3.15.2 `os` page → REJECTED (duplicate carrier + mechanism mismatch)

URL `https://docs.python.org/3/library/os.html`, HTTP 200, 791358 bytes,
pin `corpus/evidence/sources-r81/python-os-3.15.2.html`.

### 4.1 Duplicate sweep (the hit that decides it)

```
$ grep -n 'docs\.python\.org/3/library/os\.html' corpus/SOURCES.md ; echo rc=$?
74:| S068 | Python os module documentation — https://docs.python.org/3/library/os.html | docs | A | os.stat versus os.lstat symlink following (final path component) | os.stat entry and os.lstat entry; follow_symlinks section; Python 3.15.0 docs opened 2026-10-21 | A report-presence check must lstat the final component: os.stat follows a symlink by default, lstat inspects the link itself. | mined | 2026-10-21 | on-release | corpus/knowledge/wave-settlement-r20.md, corpus/lessons/round-20.md |
rc=0
$ grep -in 'scandir\|DirEntry' corpus/SOURCES.md ; echo rc=$?
rc=1
$ grep -n 'ee706c46011ab0f4' corpus/SOURCES.md ; echo rc=$?
rc=1
```

QUALITY 155 (round 59): a canonical-URL hit means the source is a reconciliation
(`supersedes`/`duplicate`), **never** a fresh admit. S068 already holds this URL. The page
also moved builds since S068's anchor: S068 says "Python 3.15.0 docs"; the served page is
3.15.2, last updated 2026-11-04 03:27 UTC. That drift is recorded here and is not an edit
to S068's immutable `anchor` cell (QUALITY 113).

### 4.2 Located quotes (what the page does say)

```
:3446  <span class="sig-name descname"><span class="pre">is_dir</span></span>... <span class="pre">follow_symlinks</span>...<span class="pre">True</span>...
:3447  <dd><p>Return <code class="docutils literal notranslate"><span class="pre">True</span></code> if this entry is a directory or a symbolic link pointing
:3448  to a directory; return <code class="docutils literal notranslate"><span class="pre">False</span></code> if the entry is or points to any other
:3449  kind of file, or if it doesn’t exist anymore.</p>
```

- `:3447` `if this entry is a directory or a symbolic link pointing` — 11 words; with the
  `:3446` signature this is `is_dir(*, follow_symlinks=True)`, i.e. the default follows
  symlinks.
- `:3469-3471` is `is_file(*, follow_symlinks=True)`, whose body says
  `:3470` `if the entry is or points to a directory or other` / `:3471` `non-file entry, or
  if it doesn’t exist anymore.` — 11 words for the `:3470` span; a directory is not a file.

Anchor-check:

```
$ python3 -I tools/mori-anchor-check.py --pin corpus/evidence/sources-r81/python-os-3.15.2.html \
    --check "sX1|3447|11|if this entry is a directory or a symbolic link pointing" \
    --check "sX2|3470|11|if the entry is or points to a directory or other"
anchor item=sX1 span=3447 verdict=ok located_on=3447 occurrences=1 words_counted=11 words_recorded=11
anchor item=sX2 span=3470 verdict=ok located_on=3470 occurrences=1 words_counted=11 words_recorded=11
ANCHOR_CHECK: PASS items=2 ok=2 pin_sha256=ee706c46011ab0f4767fa54fe8f39dfdb2d93d3ac5696aeb0478f7acce87ec41 pin_bytes=791358
rc=0
```

### 4.3 Rejected candidate (reason + flip) and the row that would have been proposed

```
| — (no fresh id; S068 carries the canonical URL) | Python 3.15.2 os module documentation — https://docs.python.org/3/library/os.html | docs | A | REJECTED: os.scandir and DirEntry.is_dir/is_file with follow_symlinks default True — the page's directory-listing API, not the r80 C3 path-presence test | os.DirEntry.is_dir signature follow_symlinks=True:3446; "if this entry is a directory or a symbolic link pointing":3447; is_file "if the entry is or points to a directory or other":3470; Python 3.15.2 docs, Last updated 2026-11-04 03:27 UTC (:7308); sha256 ee706c46011ab0f4767fa54fe8f39dfdb2d93d3ac5696aeb0478f7acce87ec41; copy corpus/evidence/sources-r81/python-os-3.15.2.html; 7318 lines, 791358 bytes | REJECTED: duplicate carrier — the canonical URL is already S068 at corpus/SOURCES.md:74 (QUALITY 155) — and the mechanism does not match: the entering B6 counter runs git ls-tree -r --name-only (.ufo/waves/round-80/count-c3.py:40) and never enumerates entries with os.scandir or DirEntry. Flip: a counter that enumerates with os.scandir, or a claim that needs is_file(follow_symlinks=True) semantics; then land it as an S068 superseding row carrying this anchor, not as a fresh carrier admit. | rejected | 2026-11-04 | on-release | — |
```

The facts are true and citable; the rejection is about **this round's need and the
duplicate-carrier rule**, not about the page's quality.

## 5. Why B6 needs a second row — the entering mechanism is git's tree type

Read-only `git show` at the entering revision (no working-tree bytes were graded):

```
$ git show 44bc941a:.ufo/waves/round-80/count-c3.py | grep -n 'ls-tree\|def present_set\|^TOKEN'
31:TOKEN = re.compile(r"tools/([A-Za-z0-9_.-]+\.(?:py|sh))(?![\w.-])")
39:def present_set(repo, rev):
40:    p = run(["git", "-C", repo, "ls-tree", "-r", "--name-only", rev, "--", "tools/"])
$ git show 44bc941a:.ufo/waves/round-80/count-c1.py | grep -n 'isfile\|TOOL ='
34:TOOL = "tools/mori-claim-sweep.py"
79:    if not os.path.isfile(tool):
```

`:79` is the counter checking its own sweep tool; it is not B6. B6 is graded by count-c3,
whose `present_set` at `:40` passes `-r --name-only` and **no `-t`**, so a directory
`tools/pkg.py` is absent from `present`, while the PROVINCE mention still yields the
`named` token `pkg.py` through `TOKEN` at `:31`; `extra = named − present` is then
non-empty — the r80 LOW-12 shape. (The missing left boundary in that same `TOKEN` is
MEDIUM-6/B1, a different fixture; it does not decide B6.) The r81 B6 fixture writes
`tools/pkg.py/inner.py` (`.ufo/waves/round-81/count-c1.py:155-160`), so at R the path is a
git tree, and the fix's evidence is ls-tree's `-t` plus the object-type column.
Hence:

- **S596** grounds the reading in the r81 contract's named limits ("a named path that
  exists at R as a directory is not an instrument").
- **S597** grounds the code path that decides "exists as a directory".

Working-tree note: `.ufo/waves/round-80/count-c1.py` and `count-c3.py` already differ from
`44bc941a` in this worktree (`git diff --stat` shows 100 insertions, 35 deletions), i.e.
executor seats are mid-fix. I graded **no** working-tree byte; every mechanism claim above
is `git show 44bc941a:...`.

## 6. Additional screened source — git-ls-tree(1) → proposed S597

URL `https://git-scm.com/docs/git-ls-tree`, HTTP 200, 39083 bytes,
pin `corpus/evidence/sources-r81/git-ls-tree.html`.

### 6.1 Duplicate sweep

```
$ grep -n 'git-scm\.com/docs/git-ls-tree' corpus/SOURCES.md ; echo rc=$?
rc=1
$ grep -n 'ls-tree' corpus/SOURCES.md ; echo rc=$?
rc=1
$ grep -n 'ff06fbc8b15b0fee' corpus/SOURCES.md ; echo rc=$?
rc=1
```

No hit. The registry's git-scm rows are different pages (S046 merge-base, S047 symbolic-ref,
S058 rev-list/diff-tree, S059 log, S064/S210 rev-parse, S227 gitrevisions). `S595` remains
the max id; S597 is free.

### 6.2 Located quotes

```
:1666  <dt ... id="...--t"><a class="anchor" ...></a>-t </dt>
:1667  <dd>
:1668  <p>Show tree entries even when going to recurse them. Has no effect
:1669  if <span class='synopsis'><code>-r</code></span> was not passed. <span class='synopsis'><code>-d</code></span> implies <span class='synopsis'><code>-t</code></span>.</p>
:1670  </dd>
```

- `:1668` `Show tree entries even when going to recurse them.` — 9 words. This is why a
  tree entry appears at all under `-r`; without `-t` it does not (`:1669`).

```
:1752  <div class="literalblock">
:1753  <div class="content">
:1754  <pre>%(objectmode) %(objecttype) %(objectname)%x09%(path)</pre>
:1755  </div>
```

- `:1754` `%(objectmode) %(objecttype) %(objectname)%x09%(path)` — 3 whitespace tokens;
  the default output order: mode, **type**, object, TAB, path. The r81 fix in this
  worktree (unlanded, not graded here) splits each line on TAB and takes
  `metadata.split()[1]`, which is exactly `%(objecttype)`; the entering program at
  `44bc941a` passes `--name-only` and never sees that field at all (§5).

```
:1810  <dt ... id="...-objecttype"><a class="anchor" ...></a>objecttype </dt>
:1811  <dd>
:1812  <p>The type of the object (<span class='synopsis'><code>commit</code></span>, <span class='synopsis'><code>blob</code></span> or <span class='synopsis'><code>tree</code></span>).</p>
:1813  </dd>
```

- `:1812` `The type of the object (<span class='synopsis'><code>commit</code></span>, <span class='synopsis'><code>blob</code></span> or <span class='synopsis'><code>tree</code></span>).`
  — 12 raw tokens, 9 rendered words. The domain includes `tree`.

### 6.3 Anchor-check receipt

```
$ python3 -I tools/mori-anchor-check.py --pin corpus/evidence/sources-r81/git-ls-tree.html \
    --check "s597a|1668|9|Show tree entries even when going to recurse them." \
    --check "s597b|1754|3|%(objectmode) %(objecttype) %(objectname)%x09%(path)" \
    --check "s597c|1812|12|The type of the object (<span class='synopsis'><code>commit</code></span>, <span class='synopsis'><code>blob</code></span> or <span class='synopsis'><code>tree</code></span>)."
anchor item=s597a span=1668 verdict=ok located_on=1668 occurrences=1 words_counted=9 words_recorded=9
anchor item=s597b span=1754 verdict=ok located_on=1754 occurrences=1 words_counted=3 words_recorded=3
anchor item=s597c span=1812 verdict=ok located_on=1812 occurrences=1 words_counted=12 words_recorded=12
ANCHOR_CHECK: PASS items=3 ok=3 pin_sha256=ff06fbc8b15b0fee505a259e4dc54096c9fba0460f4f02b449d55ecce7818267 pin_bytes=39083
rc=0
```

### 6.4 Proposed 11-column Registry row

```
| S597 | git-ls-tree(1) — https://git-scm.com/docs/git-ls-tree | docs | A | the default ls-tree output field order and the -t flag: the second space-separated field is the object type (commit, blob or tree), and -t makes tree entries appear even when -r recurses. Not the counter's fix, not a claim that a tree entry is an instrument, and not ls-tree under --format or --name-only. | Output Format default "%(objectmode) %(objecttype) %(objectname)%x09%(path)":1754; FIELD NAMES objecttype "The type of the object (commit, blob or tree).":1812; OPTIONS -t "Show tree entries even when going to recurse them.":1668; git-scm.com docs build: page last updated in 2.42.0, no changes 2.42.1 to 2.56.0 (:1322, :1328), served 2026-11-04; sha256 ff06fbc8b15b0fee505a259e4dc54096c9fba0460f4f02b449d55ecce7818267; copy corpus/evidence/sources-r81/git-ls-tree.html; 1873 lines, 39083 bytes | git ls-tree's default second field is the object type and -t lists tree entries under -r; an entry whose second field is "tree" at path P reports P as a directory, not a blob, which is the type test the r80 C3 directory exclusion needs. | queued | 2026-11-04 | on-release | — |
```

### 6.5 Limit

The page states the type **domain** (`commit`, `blob` or `tree`) and the field order; it
does not print the sentence "a tree entry is a directory". Mapping `tree → directory` is
git's object model, and is labelled **[INFERENCE]** here; the page's own words support only
"the second field is the object type and `tree` is one of its values".

## 7. What these sources do not support

1. **No live read.** Nothing here observes a path on this host; `st_mode` and ls-tree are
   documented encodings, not measurements.
2. **stat(2) has no normative exclusivity sentence.** The distinctness of `S_IFDIR` and
   `S_IFREG` is shown by one example switch (`:317` with `:320`/`:323`). A claim that the
   page *defines* "directory is not a regular file" is not supported.
3. **The `st_mode` sentence is about `lstat()` on a symlink under POSIX.1-2001** (`:234`),
   not a general field table. The general type-bits reading rests on the EXAMPLES switch.
4. **The os page does not ground B6.** `DirEntry` is a listing API; the entering counter
   uses `git ls-tree`. Its `is_file` non-file paragraph is true but off-mechanism.
5. **git-ls-tree does not say "tree = directory"**; see §6.5.
6. **No claim about `stat(3type)`.** I opened
   `https://man7.org/linux/man-pages/man3/stat.3type.html` (HTTP 200, 13720 bytes) in
   scratch and saw `mode_t     st_mode;     /* File type and mode */` at its `:80`, which
   is the normative field declaration stat(2) delegates to. It is **not pinned and not
   proposed**; treat that observation as a lead for a later seat, not as evidence this
   round (an unpinned page is not citable).

## 8. Defects and observations in other seats' bytes

1. **`corpus/knowledge/record-claim-integrity-r81.md`** — the first version I read cited
   `S_IFREG` at `:326` (the switch's closing brace) and the pin as
   `corpus/evidence/sources-r81/stat.2.html`. Both were **my** error in an early IRC line
   to that seat, not the author's: I gave `:326` and the short filename before the exact
   extraction. The author corrected all three after my follow-up: `:1` now carries
   `corpus/evidence/sources-r81/stat.2.man-pages-6.19.html`, `:11` carries `:323`, and
   `:22` carries `inner.py` (`grep -n ':326'` now rc 1). Recorded so the Gate does not
   re-route a fixed defect.
2. **`corpus/knowledge/record-claim-integrity-r81.md:22`** — now says the entering counter
   "uses ls-tree without tree entries" and keeps the author's separate `__init__.py`
   scratch probe distinct from the r81 fixture's `inner.py`. No defect remains there.
3. **Unlanded executor edits in the r80 counters** — `.ufo/waves/round-80/count-c1.py` and
   `count-c3.py` in this worktree differ from `44bc941a` (100 insertions / 35 deletions).
   I did not read them as graded bytes, and no receipt here depends on them. Any seat that
   quotes the worktree copy as "the r80 bytes" is quoting an unlanded fix.
4. **S068 freshness** — `corpus/SOURCES.md:74` anchors "Python 3.15.0 docs"; the served
   page is 3.15.2 (last updated 2026-11-04). Append-only note only; the immutable `anchor`
   cell was not touched (QUALITY 113).

## 9. What I could not verify

- Whether the seven C1 fixtures pass at the landed revision — that is the counters' and the
  executors' receipts, not a source seat's. I read only `44bc941a` bytes.
- The normative `st_mode` field table in stat(3type), because I deliberately did not pin it
  (§7 item 6).
- The mapping `tree → directory` as a page sentence; it is inference (§6.5).
- The `os` page's `DirEntry` facts do not depend on a running interpreter here; they are
  read from the pinned page only.

## 10. Scratch and tooling

Scratch root `/fast/scratch/hyaku/mori-r81/Mo81Sc02Source/` — created, used, removed:

```
$ rm -rf -- /fast/scratch/hyaku/mori-r81/Mo81Sc02Source
$ ls -d /fast/scratch/hyaku/mori-r81/Mo81Sc02Source 2>&1
ls: cannot access '/fast/scratch/hyaku/mori-r81/Mo81Sc02Source': No such file or directory
ls_rc=2
```

Nothing was written under `/tmp`, `~/.local/bin`, `.scratch/`, `.ufo/state/`,
`.ufo/watchdog.log`, `MANIFEST.json`, or the fleet root. No git/jj mutation: only
`git show`, `git diff --stat`, `git ls-tree` and `git rev-parse`-class reads. The evidence
files reached HEAD through the L1's `075574c8` (§1); this seat's only untracked artifact is
this report (`git status --short` prints `?? .ufo/waves/round-81/w1/Mo81Sc02Source.md`).
No tool was installed or upgraded this seat (python3, curl, coreutils, and the lane's own
`tools/mori-anchor-check.py` were sufficient).

## 11. Self-defects (adversarial)

1. I sent the knowledge seat `:326` for `S_IFREG` before extracting the line mechanically;
   the correct line is `:323`. Caught only because I later dumped `:305-332` with numbers.
   The lesson is the lane's own QUALITY 61: never integrate a transport projection — take
   the line from the delivered bytes. Fixed by message; the author corrected the entry.
2. My first `:1812` extraction cut the quote at `).</p` instead of `).`; re-ran the
   anchor-check on the clean span and used that receipt.
3. Three shell batches were backgrounded by incoming IRC and returned asynchronously; no
   result was lost, but §2/§3 numbers are from the re-run invocations shown.
4. I initially intended to propose `os.html` as S597 (the seat's candidate 2). The entering
   `count-c3.py` mechanism check (`git show 44bc941a:...`) is what changed the disposition;
   had I not run it, the round would have admitted a row that grounds no code path.
