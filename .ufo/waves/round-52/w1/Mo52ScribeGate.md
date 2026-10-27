# Mo52ScribeGate — Gate block draft for S497–S501

Seat: leaf scribe, mori round 52 wave w1. Scope: the lesson's `## Gate` block for the five new SOURCES rows
S497–S501, each cell's URL, access date 2026-10-26, copy sha256 and one ≤25-word located quote verified by a
substring test on the copy under `corpus/evidence/sources-r52/`, plus one admit decision per row and one reject
decision for the rendered `latest` page. House shape read from `corpus/lessons/round-51.md` §"## Gate".

Read-only throughout: no product file, counter, contract, control or frozen artifact was written; nothing under the
lane was created or modified except this report. No git or jj mutation was run (read-only `log`/`cat-file`/`diff`
only). Scratch `/fast/scratch/hyaku/mori-r52/Mo52ScribeGate/` was created with `TMPDIR` set to its `tmp/`, held one
clone-free working set (five live tag fetches, three HTML fetches, three small Python scripts) and was removed after
this file was written. No tool was installed or upgraded; all pacman transactions stayed untouched. No host write,
no sysctl, no cgroup, no journal action; the only host reads were the files in the lane and five HTTPS GETs to
`raw.githubusercontent.com`, `www.kernel.org` and `docs.kernel.org`.

## Receipts

### Copy hashes: worktree = row cell = freeze list = freeze commit = data commit = live tag fetch

```
$ sha256sum corpus/evidence/sources-r52/*
d7bf787c910d9a7cbabee3a50c512ce3aad78d63659b0c968adca16b5916b058  corpus/evidence/sources-r52/mman.h.v7.2
449b858385c7ece0ff88a8b41893efadb70a437fb8585a296c4ef0461a4c1545  corpus/evidence/sources-r52/mmap.c.v7.2
767ab88153c4494e54fcf2db4e5bd01921d6bd8350f1596ada508cb5e4b4927f  corpus/evidence/sources-r52/overcommit-accounting.rst.v7.2
e702754c45bd7bd69e5da22a6505c9c1016eaafe6e883b746cc3cdbd413ebe7c  corpus/evidence/sources-r52/util.c.v7.2
bf8ca0265fefc019250697b6ee47a0679709b2ee45f4d1893b3dfd95c1f8c1ce  corpus/evidence/sources-r52/vm.rst.v7.2
rc=0

$ grep -n 'sources-r52' .ufo/waves/round-52/evidence/freeze-sha256.txt
20:d7bf787c910d9a7cbabee3a50c512ce3aad78d63659b0c968adca16b5916b058  corpus/evidence/sources-r52/mman.h.v7.2
21:449b858385c7ece0ff88a8b41893efadb70a437fb8585a296c4ef0461a4c1545  corpus/evidence/sources-r52/mmap.c.v7.2
22:767ab88153c4494e54fcf2db4e5bd01921d6bd8350f1596ada508cb5e4b4927f  corpus/evidence/sources-r52/overcommit-accounting.rst.v7.2
23:e702754c45bd7bd69e5da22a6505c9c1016eaafe6e883b746cc3cdbd413ebe7c  corpus/evidence/sources-r52/util.c.v7.2
24:bf8ca0265fefc019250697b6ee47a0679709b2ee45f4d1893b3dfd95c1f8c1ce  corpus/evidence/sources-r52/vm.rst.v7.2
rc=0

$ git cat-file -p 8524904adb25e44f24d9f25aac7eae909625c18c:corpus/evidence/sources-r52/<file> | sha256sum
overcommit-accounting.rst.v7.2 767ab88153c4494e54fcf2db4e5bd01921d6bd8350f1596ada508cb5e4b4927f  -
vm.rst.v7.2                     bf8ca0265fefc019250697b6ee47a0679709b2ee45f4d1893b3dfd95c1f8c1ce  -
util.c.v7.2                     e702754c45bd7bd69e5da22a6505c9c1016eaafe6e883b746cc3cdbd413ebe7c  -
mman.h.v7.2                     d7bf787c910d9a7cbabee3a50c512ce3aad78d63659b0c968adca16b5916b058  -
mmap.c.v7.2                     449b858385c7ece0ff88a8b41893efadb70a437fb8585a296c4ef0461a4c1545  -
rc=0  (5/5 equal to the cells and the freeze list)

$ git cat-file -p d3a8ea5957b73bddbde750a8c0af2fba8da8b7c2:corpus/evidence/sources-r52/<file> | sha256sum
(same five values, rc=0 — the freeze commit holds the same bytes)

$ python3 verify.py   # live tag fetch, see block below
  S497 overcommit-accounting.rst.v7.2 sha256=767ab881…b4927f live_equal=True
  S498 vm.rst.v7.2                  sha256=bf8ca026…f8c1ce live_equal=True
  S499 util.c.v7.2                  sha256=e702754c…3ebe7c live_equal=True
  S500 mman.h.v7.2                  sha256=d7bf787c…16b058 live_equal=True
  S501 mmap.c.v7.2                  sha256=449b8583…4c1545 live_equal=True
  (live files: curl -sS -L https://raw.githubusercontent.com/torvalds/linux/v7.2/<path>, HTTP 200, bytes
   2647 / 42424 / 43913 / 4265 / 51223, rc=0 each)
```

### SOURCES diff shape and cell count

```
$ git diff --numstat 4f266ef2fdf74d8b046f5b4f5a5c4945f65b966d 8524904adb25e44f24d9f25aac7eae909625c18c -- corpus/SOURCES.md
5	0	corpus/SOURCES.md

$ git diff <same range> -- corpus/SOURCES.md | grep '^+' | grep -v '^+++'
+| S497 | Linux Documentation/mm/overcommit-accounting.rst at tag v7.2 — …
+| S498 | Linux Documentation/admin-guide/sysctl/vm.rst at tag v7.2, overcommit and reserve knobs — …
+| S499 | Linux mm/util.c at tag v7.2 — …
+| S500 | Linux include/linux/mman.h at tag v7.2 — …
+| S501 | Linux mm/mmap.c at tag v7.2 — …
rc=0   (five added lines, ids in order; the single `^-` match is the `--- a/corpus/SOURCES.md` header, so 0 content
        lines were removed)

$ awk 'NR>=276 && NR<=280 {n=gsub(/\|/,"|"); printf "%d pipes=%d\n", NR, n}' corpus/SOURCES.md
276 pipes=12
277 pipes=12
278 pipes=12
279 pipes=12
280 pipes=12   (12 pipes = 11 cells per row)
```

### Quote verification (substring test on the copy, ≤25 words, negative control per quote)

The test normalises each copy's whitespace runs to one space, then asks `quote in normalised_copy`; the negative
control changes the quote's last whitespace token to `ZZZ` and must not be found. Line spans are computed by
mapping the normalised match back to raw offsets.

```
$ python3 verify.py
== quote check: substring on whitespace-normalised copy, <=25 words ==
  S497 words=24 <=25=yes found=True lines=20-22 negative_control_absent=True
  S498 words=22 <=25=yes found=True lines=841-842 negative_control_absent=True
  S499 words= 9 <=25=yes found=True lines=911-912 negative_control_absent=True
  S500 words= 3 <=25=yes found=True lines=78-78 negative_control_absent=True
  S501 words= 7 <=25=yes found=True lines=552-553 negative_control_absent=True

== extra located quotes ==
  S497 words=16 found=True lines=37-38
  S498 words=17 found=True lines=831-832
  S501 words= 6 found=True lines=1595-1595
rc=0
```

### Entry quotes against the row anchors (all 28 claim rows of the entry)

```
$ python3 anchorcheck.py
row@entry:29 S497 OUTSIDE quote_lines=48-48 anchor=[(7, 28), (33, 37), (45, 45), (54, 64), (83, 84)] q='In mode 2 the MAP_NORESERVE flag is ignored.'
row@entry:31 S497 OUTSIDE quote_lines=83-85 anchor=[(7, 28), (33, 37), (45, 45), (54, 64), (83, 84)] q='To Do ===== * Account ptrace pages (this is hard)'
checked=28 outside=2
rc=0
```

Every other claim row's quote sits inside its row's anchor ranges (S498 6/6, S499 9/9, S500 2/2, S501 4/4, and the
five S497 rows whose quotes fall in `7-28`, `33-37` and `54-64`). The two failures and the truncated S497 row-4
quote are findings 1–3 below.

### Reject candidate: rendered `latest`

```
$ curl -sS -L -o latest-overcommit-accounting.html -w 'http=%{http_code} bytes=%{size_download}\n' \
    https://www.kernel.org/doc/html/latest/mm/overcommit-accounting.html
http=200 bytes=13558
$ sha256sum latest-overcommit-accounting.html
aa4364195e1665bf991502dd46a84770d00231be49db22c55e232e926fe4fd97

$ curl … https://www.kernel.org/doc/html/v7.2/mm/overcommit-accounting.html   -> http=200 bytes=12762
$ sha256sum v7.2-overcommit-accounting.html
ee9af79464ebb2810171f63e2b8d4d71bd360d381f748d550e55e2d30b402536

$ curl … https://docs.kernel.org/7.2/mm/overcommit-accounting.html            -> http=200 bytes=12762
$ sha256sum docs72.html
ee9af79464ebb2810171f63e2b8d4d71bd360d381f748d550e55e2d30b402536   (same bytes as the kernel.org v7.2 rendering)
$ curl … https://docs.kernel.org/latest/mm/overcommit-accounting.html         -> http=404 bytes=146

$ grep -o '[0-9a-f]\{40\}' latest-overcommit-accounting.html | wc -l
0                                  (no commit id in the fetched bytes)
$ grep -o '7\.[0-9]\.0' v7.2-overcommit-accounting.html latest-overcommit-accounting.html
1 v7.2-overcommit-accounting.html:7.2.0
1 latest-overcommit-accounting.html:7.3.0
   markup: <p class="blurb">7.2.0</p>   vs   <p class="blurb">7.3.0</p>

$ python3 (article-body text diff, v7.2 rendering vs latest rendering)
body_equal = False   (block lists 133 vs 141)
--- v7.2
+++ latest
@@ -3 +3 @@
-7.2.0
+7.3.0
@@ -6,0 +7 @@ +Working with the development community
@@ -11,0 +13 @@ +Internal API manuals
@@ -27,0 +30 @@ +Development tools and processes
@@ -36,0 +40 @@ +User-oriented documentation
@@ -41,0 +46 @@ +Firmware-related documentation
@@ -43,0 +49 @@ +Architecture-specific documentation
@@ -44,0 +51 @@ +Other documentation
@@ -45,0 +53 @@ +Translations
   (the article body's own sentences are identical in both renderings today; the difference is the version banner
    plus eight navigation entries)
```

## Draft: the lesson's `## Gate` block, rows S497–S501

```markdown
### New SOURCES rows (each opened this round; rule 1)

Five rows, all opened 2026-10-26, appended after S496 (`corpus/SOURCES.md:276-280`), 11 cells each, status `mined`,
recheck `on-release`, `used-by corpus/knowledge/overcommit-commit-limit-r52.md`. The five documents were copied into
`corpus/evidence/sources-r52/` and pinned by sha256 in `evidence/freeze-sha256.txt` (lines 20-24, the five
`sources-r52` entries); at the data commit `8524904a` the five committed blobs hash to exactly the values in the row
cells and in that list (`git cat-file -p 8524904a:corpus/evidence/sources-r52/<file> | sha256sum`, 5/5 equal), the
worktree bytes hash to the same five values (`sha256sum corpus/evidence/sources-r52/*`), the freeze commit
`d3a8ea59` blobs hash to them too, and each document re-fetched from its tag URL today
(`https://raw.githubusercontent.com/torvalds/linux/v7.2/<path>`, HTTP 200) hashes to the same value again, so every
copy is the tag's bytes as served on 2026-10-26. `corpus/SOURCES.md` gains five lines and loses none between the
entering tip `4f266ef2` and `8524904a` (`git diff --numstat` → `5	0`; the five added lines are S497-S501 in id
order), so no earlier row was edited this round. Changed in place after the wave, under the contract's allowance for
correcting data (in-round rows only), from `w1/Mo52ScribeGate.md` findings 1–4: S497 anchor
`7-28,33-37,45,54-64,83-84` → `7-29,33-38,43-48,54-64,83-85`; no other row cell changed.

| id | URL / locator | accessed | ≤25-word located quote | decision |
|---|---|---|---|---|
| S497 | https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/mm/overcommit-accounting.rst — copy `overcommit-accounting.rst.v7.2` (sha256 `767ab881…b4927f`) | 2026-10-26 | "The total address space commit for the system is not permitted to exceed swap + a configurable amount (default is 50%) of physical RAM." (24 words) — mode 2, copy lines 20-22; the quote is also the entry's row-2 quote. The meminfo sentence the entry's row-4 claim leans on, "The current overcommit limit and amount committed are viewable in ``/proc/meminfo`` as CommitLimit and Committed_AS respectively." (16 words), is at 37-38 inside the corrected anchor | admit, mined, kind docs, tier A, recheck `on-release`; scope is the three modes (7-29), the mode-2 cap and its failure wording (19-25), the two knobs taking effect only in mode 2 (33-35), the two meminfo lines (37-38), the `MAP_NORESERVE` gotcha (48), the per-mapping cost table (54-64) and the `To Do` ptrace gap (83-85) at v7.2 — and not another kernel's text |
| S498 | https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/admin-guide/sysctl/vm.rst — copy `vm.rst.v7.2` (sha256 `bf8ca026…f8c1ce`) | 2026-10-26 | "When this flag is 0, the kernel compares the userspace memory request size against total memory plus swap and rejects obvious overcommits." (22 words) — `overcommit_memory`, copy lines 841-842; the exclusivity note the entry's row-11 claim leans on, "Note: overcommit_kbytes is the counterpart of overcommit_ratio. Only one of them may be specified at a time." (17 words), is at 831-832 | admit, mined, kind docs, tier A, recheck `on-release`; scope is the five knobs at v7.2 — `overcommit_memory` (836-858), `overcommit_kbytes` (825-833), `overcommit_ratio` (861-866), `user_reserve_kbytes` (1029-1046), `admin_reserve_kbytes` (84-97) — and not the rest of the sysctl page |
| S499 | https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/util.c — copy `util.c.v7.2` (sha256 `e702754c…3ebe7c`) | 2026-10-26 | "allowed = ((totalram_pages() - hugetlb_total_pages()) * sysctl_overcommit_ratio / 100);" (9 words) — `vm_commit_limit()`, copy lines 911-912 | admit, mined, kind code, tier A, recheck `on-release`; scope is `vm_commit_limit()` (901-917), `vm_memory_committed()` (937-941), `__vm_enough_memory()` (959-1003), the policy handler with its per-CPU deviation comment and sync (806-834) and the five sysctl defaults (781-786) at v7.2 — the kernel's arithmetic and defaults, not a host reading |
| S500 | https://raw.githubusercontent.com/torvalds/linux/v7.2/include/linux/mman.h — copy `mman.h.v7.2` (sha256 `d7bf787c…16b058`) | 2026-10-26 | "percpu_counter_add_batch(&vm_committed_as, pages, vm_committed_as_batch);" (3 whitespace tokens) — `vm_acct_memory()`, copy line 78; the release half is the same call negated at 83 | admit, mined, kind code, tier A, recheck `on-release`; scope is the counter declaration and batch externs (61-72) and the charge/release inlines (76-84) at v7.2; the quote is short because the line is the whole mechanism — the "approximate read" wording rests on the batched per-CPU add here together with `percpu_counter_read_positive()` in S499's `__vm_enough_memory()` |
| S501 | https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/mmap.c — copy `mmap.c.v7.2` (sha256 `449b8583…4c1545`) | 2026-10-26 | "if (sysctl_overcommit_memory != OVERCOMMIT_NEVER) vm_flags |= VM_NORESERVE;" (7 whitespace tokens) — `do_mmap()`, copy lines 552-553; the boot cap the entry's row-27 claim leans on, "sysctl_user_reserve_kbytes = min(free_kbytes / 32, SZ_128K);" (6 tokens), is at 1595 | admit, mined, kind code, tier A, recheck `on-release`; scope is the `MAP_NORESERVE` block in `do_mmap()` (546-558, including the hugetlb carve-out 555-557) and the two boot initialisers (1579-1619, `init_user_reserve` 1589-1598 and `init_admin_reserve` 1610-1619) at v7.2, not `mremap` or `mprotect` |

The claim table these rows feed holds 28 rows (`corpus/knowledge/overcommit-commit-limit-r52.md:25-52`), each naming
exactly one of the five ids (source cells S497 7, S498 6, S499 9, S500 2, S501 4; `grep -cE '^\|'` → 36 = two headers
and two separators plus 28 claim rows plus the 4-row reading-rules table at 56-61), so all five sources are drawn on
and no row cites an id this Gate does not carry.

#### Rejected candidate — the rendered `latest` page (no id spent)

| candidate | fetched | observed on 2026-10-26 | decision |
|---|---|---|---|
| https://www.kernel.org/doc/html/latest/mm/overcommit-accounting.html | HTTP 200, 13558 bytes, sha256 `aa436419…6fe4fd97` | the page's own banner reads `<p class="blurb">7.3.0</p>`, so the page renders the development tree, not tag v7.2; no commit id occurs anywhere in the bytes (`[0-9a-f]{40}` → 0 matches); the article body's sentences are textually identical to the v7.2 rendering today, the difference against `/doc/html/v7.2/` being the banner and eight navigation entries; the rendering carries no line numbers | reject: `latest` is a moving rendering of the development tree and cannot carry this row's `path:N` locator or a stable sha256 pin |

Why a pinned tag copy is preferred: the row is scoped to tag v7.2, whose raw URL bytes are immutable and hash to the
row cell, the freeze list and today's live fetch (5/5); the row's locator is `path:N`, which requires the source's
own line structure — the HTML rendering has none and adds site navigation; and the page's bytes change whenever the
development tree moves, which the banner has already done (7.2.0 → 7.3.0) while the row's claim stayed at v7.2. The
body's present equality is the sharp part: a reader who substituted the `latest` page today would find every
sentence identical and no signal that the tree is unpinned, so only the pin separates the two, not a content check.

Flip condition: this candidate becomes admissible only when the URL is version-pinned and the page's own bytes say
which version they are — concretely, when the row is opened on
`https://www.kernel.org/doc/html/v7.2/mm/overcommit-accounting.html` (HTTP 200 today, 12762 bytes, sha256
`ee9af794…0b402536`, banner `<p class="blurb">7.2.0</p>`; `https://docs.kernel.org/7.2/mm/overcommit-accounting.html`
serves the same 12762 bytes with the same sha256, while `https://docs.kernel.org/latest/…` answers 404) and the row
carries (a) a saved HTML copy whose sha256 is the cell and (b) section-anchor locators (`#gotchas`, `#how-it-works`)
in place of `path:N`. Until both hold — and while `latest` renders 7.3.0 with no commit id in its bytes — the
candidate stays rejected, and it spends no id because its scope would duplicate S497's document.
```

## Findings

1. **MED — `corpus/SOURCES.md:276` (S497 locator cell): the anchor does not cover a quote its own claim row cites.**
   The cell reads `overcommit-accounting.rst:7-28,33-37,45,54-64,83-84`; `45` is the single line 45 (mid-sentence of
   the mremap gotcha, which runs 43-46), while entry row 5
   (`corpus/knowledge/overcommit-commit-limit-r52.md:29`) quotes "In mode 2 the MAP_NORESERVE flag is ignored.",
   which is copy line 48 and lies outside every range in the anchor. Suggested correction `45` → `43-48`
   (mechanical check: `python3 anchorcheck.py` → `row@entry:29 S497 OUTSIDE quote_lines=48-48`).
2. **MED — `corpus/SOURCES.md:276` (S497): the anchor stops at the `To Do` heading, not the bullet it promises.**
   `83-84` covers "To Do" and its underline; entry row 7 (`:31`) quotes the bullet "Account ptrace pages (this is
   hard)", which is line 85. Suggested `83-84` → `83-85`. Consequence if left: the row's scope sentence "the listed
   gaps" is anchored to a heading with no content (check: `row@entry:31 S497 OUTSIDE quote_lines=83-85`).
3. **LOW — `corpus/SOURCES.md:276` (S497) + `corpus/knowledge/overcommit-commit-limit-r52.md:28`: the meminfo
   sentence is anchored and quoted only up to its first line.** The anchor ends at 37 and row 4 quotes just
   "The current overcommit limit and amount committed are viewable in" — the predicate naming both fields
   ("as CommitLimit and Committed_AS respectively") is copy line 38 and is quoted nowhere in the entry, so the row's
   located quote by itself does not entail "published … as two meminfo lines". Data correction available to the L1
   (no counter change): anchor `33-37` → `33-38` and extend row 4's quote cell to the full 16-word sentence
   (verified present at 37-38).
4. **LOW — `corpus/SOURCES.md:276` (S497): `7-28` omits line 29**, the last line ("initialize every page.") of
   mode 2's "Useful for applications …" bullet, while the row's decision cell says the scope is "the three overcommit
   modes"; mode 2 therefore ends one line outside its own range. Suggested `7-29`.
5. **LOW — `corpus/SOURCES.md:279` (S500): the located quote is 3 whitespace tokens.** It is the entire mechanism and
   the release half is cited separately (line 83), but a 3-token quote gives an entailment voter almost nothing to
   test, and the entry's row 23 (`:47`) rests on the same single line. No rule is broken; recorded as a thin anchor
   for round-53 adjudication.
6. **LOW — `corpus/knowledge/overcommit-commit-limit-r52.md:31`: the row-7 quote joins two blocks.** It reads
   "To Do ===== * Account ptrace pages (this is hard)" — heading, underline and bullet concatenated rather than one
   sentence. It is locatable (83-85) but reads as two blocks; a quote of the bullet alone (line 85) would be cleaner.
7. **LOW — the rejected `latest` URL cannot be distinguished by content today.** Its article body is textually
   identical to the v7.2 rendering; only the `<p class="blurb">7.3.0</p>` banner and eight navigation entries differ.
   Any future spot-check that compares prose rather than bytes will pass the unpinned page, so the pin rule is the
   only detector. Concerns the rejected candidate, not a lane file; route to the round-53 lesson section.
8. **LOW — `corpus/SOURCES.md:280` (S501): the anchor begins mid-comment.** `1585-1619` starts inside the
   `init_user_reserve` comment (which opens at 1579); both claim lines (1595, 1616) are covered, so no correction is
   required, only noted because the range's start is arbitrary.

## Limits and unverified items

- The five copies were compared against the tag URL as served today (`raw.githubusercontent.com/torvalds/linux/v7.2/…`)
  and against the freeze and data commits. They were not compared against a local kernel git object database; the
  identification of those bytes as tag `v7.2` rests on the URL the row names.
- The rejection rests on provenance, not on drift: the `latest` page's prose equals v7.2's today. I did not observe
  the page change over time; the evidence that it is unpinned is the banner (7.3.0) and the absence of any commit id,
  not an observed edit.
- The entailment arm itself is not evaluated here: I cast no vote and wrote no line beginning with the two vote
  keywords. Findings 1–4 and 6 concern the row anchors and one entry quote cell, not the claim texts, so no claim
  hash in `evidence/c2-hashes-at-data.txt` is affected by them.
- `anchorcheck.py` treats a quote as inside an anchor only if one range contains it entirely; a quote straddling two
  ranges would be reported as outside even if every line is covered. Reviewing the 28 rows, no such case occurred
  (the two failures are genuinely uncovered lines, 48 and 85).
- The 25-word limit was counted as whitespace-separated tokens, the convention round-51 used for its code quotes;
  under any other tokenisation the S497 quote (24 tokens) and S498 quote (22) stay under 25 by at least one word,
  but the S499/S500/S501 code quotes could be counted higher if `(`/`;` were split off.
- Nothing was run from `tools/`, `.ufo/waves/round-38..49/` or any frozen instrument; the counters were not executed
  by this seat, so no counter receipt is claimed here.
