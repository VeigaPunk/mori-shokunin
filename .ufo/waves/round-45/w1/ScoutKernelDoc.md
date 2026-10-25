# ScoutKernelDoc — kernel v7.2 cgroup-v2: `memory.events` vs `memory.events.local`

Seat: `L1Mori45.ScoutKernelDoc` (scout, mori r45 wave 1). Lane:
`/home/vgpnk/Projects/shokunin/mori-shokunin`.
Work window: 2026-10-25T10:41:18Z – 2026-10-25T10:43:37Z.
Read-only on the lane: this report is the only lane file written; every fetched
byte stays under TMPDIR (section 7). No tool was installed; nothing was deleted.

All line numbers below refer to the fetched copy
`TMPDIR/cgroup-v2.rst`, 133236 bytes, 3524 lines,
sha256 `a9433bb0e16a67f07a93424c7bf842f47616e9b0a27b51e17d7b34cff246b7ad`.

## 1. Plain answers

**Does the doc say `memory.events` is hierarchical? Yes.** Lines 1474-1476
(leading TAB stripped; `printf '%s\n' "<quote>" | wc -w` = **24**):

> Note that all fields in this file are hierarchical and the file modified
> event can be generated due to an event down the hierarchy.

**Does the doc say the `.local` fields are non-hierarchical? Yes.** Lines
1518-1519 (leading TAB stripped; `wc -w` = **17**):

> Similar to memory.events but the fields in the file are local to the cgroup
> i.e. not hierarchical.

**The exact separating wording** is the cross-reference that closes the
`memory.events` paragraph, lines 1476-1477 (`wc -w` = **10**):

> For the local events at the cgroup level see memory.events.local.

The `.local` block then states the notification consequence, lines 1519-1520
(`wc -w` = **13**): "The file modified event generated on this file reflects
only the local events."

Supporting wording, the boot-time switch, `memory_localevents` (lines
202-208). Two separate sentences on 203-205, quoted separately, each within
the 25-word cap (`wc -w` = **13**, then **15**):

> Only populate memory.events with data for the current cgroup, and not any
> subtrees.

> This is legacy behaviour, the default behaviour without this option is to
> include subtree counts.

## 2. Retrieval evidence (observed, not inferred)

| route | URL | HTTP | bytes | sha256 | fetched (UTC) | retained |
|---|---|---|---|---|---|---|
| primary (jsDelivr) | `https://cdn.jsdelivr.net/gh/torvalds/linux@v7.2/Documentation/admin-guide/cgroup-v2.rst` | 200 | 133236 | `a9433bb0e16a67f07a93424c7bf842f47616e9b0a27b51e17d7b34cff246b7ad` | 10:41:18Z | `cgroup-v2.rst` |
| raw.githubusercontent | `https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/admin-guide/cgroup-v2.rst` | 200 | 133236 | same | 10:41:25Z | `raw-gh.rst` |
| git.kernel.org cgit | `https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/Documentation/admin-guide/cgroup-v2.rst?h=v7.2` | 200 | 133236 | same | 10:41:26Z | `gko.rst` |
| GitLab mirror (independent host) | `https://gitlab.com/linux-kernel/linux/-/raw/v7.2/Documentation/admin-guide/cgroup-v2.rst` | 200 | 133236 | same | 10:42:11Z | `gitlab-mirror.rst` |
| bootlin elixir (independent rendering) | `https://elixir.bootlin.com/linux/v7.2/source/Documentation/admin-guide/cgroup-v2.rst` | 200 | 3157249 (HTML) | `88dca0d9a960d1bb6ca6481f79d84d72b89535fd903db0c5efbb4159e686066d` | 10:42:06Z | `elixir.html` |
| probe only | `https://gitlab.com/torvalds/linux/-/raw/v7.2/Documentation/admin-guide/cgroup-v2.rst` | 403 | 5408 (discarded) | n/a | 10:42:11Z | none |
| probe only | `https://codebrowser.dev/linux/linux/Documentation/admin-guide/cgroup-v2.rst.html` | 404 | 153 (discarded) | n/a | 10:42:11Z | none |

Both rejected probes were re-run with the mandated `-fsSL`:
`gitlab.com/torvalds/linux` → `curl: (22) The requested URL returned error: 403`,
exit 22; `codebrowser.dev` → `curl: (22) The requested URL returned error:
404`, exit 22. The 5408/153-byte bodies shown above came from a non-`-f`
probe used only to read the status and were discarded, never retained.

`cmp -s` proves `cgroup-v2.rst == raw-gh.rst == gko.rst == gitlab-mirror.rst`
(exit 0 for all three comparisons). The elixir page is not raw bytes, but its
second `<pre>` block, HTML-unescaped and tag-stripped, equals the `.rst`
byte-for-byte: `sha256(pre text) = a9433bb0…b7ad`, `pre lines = rst lines =
3524`, Python `txt==rst` → `True`. So line numbering is corroborated by a
second, independently delivered rendering, not only by the primary.

Tag provenance (GitHub API, HTTP 200):
`refs/tags/v7.2` → annotated tag object
`237a1c39e8dfd3e1c6f1f023eea37a48ec04cc63`, tag `v7.2`, dereferencing to commit
`8d3ae59288f1e7d58d76558a6ee96d533bc5019f`.

## 3. `memory.events` section, with line numbers

Heading `  memory.events` at **line 1468**; block runs 1468-1515. Numbered
bytes, with leading TABs rendered as `\t` (source bytes verified via `od -c`):

```
1468:  memory.events
1469:\tA read-only flat-keyed file which exists on non-root cgroups.
1470:\tThe following entries are defined.  Unless specified
1471:\totherwise, a value change in this file generates a file
1472:\tmodified event.
1473:
1474:\tNote that all fields in this file are hierarchical and the
1475:\tfile modified event can be generated due to an event down the
1476:\thierarchy. For the local events at the cgroup level see
1477:\tmemory.events.local.
```

The required quote is the clause on 1474-1476 up to `hierarchy.` (24 words);
the separating cross-reference is the remainder of 1476 plus 1477 (10 words).

## 4. `memory.events.local` section, with line numbers

Heading `  memory.events.local` at **line 1517**; block runs 1517-1520:

```
1517:  memory.events.local
1518:\tSimilar to memory.events but the fields in the file are local
1519:\tto the cgroup i.e. not hierarchical. The file modified event
1520:\tgenerated on this file reflects only the local events.
```

Required quote: 1518-1519 (17 words). The "not hierarchical" phrase is on
line 1519.

## 5. Every `<controller>.events.local` the doc names

`grep -n 'events\.local' cgroup-v2.rst` returns exactly 6 hits: 5 headings
plus the cross-reference at 1477. No other `.local` events file exists.

| file | heading line | "not hierarchical" line | block | same 17-word sentence? |
|---|---|---|---|---|
| `memory.events.local` | 1517 | 1519 | 1517-1520 | yes |
| `pids.events.local` | 2450 | 2452 | 2450-2453 | yes |
| `rdma.events.local` | 2845 | 2847 | 2845-2848 | yes |
| `hugetlb.<hugepagesize>.events.local` | 2932 | 2934 | 2932-2935 | yes |
| `misc.events.local` | 3020 | 3022 | 3020-3023 | yes |

Corroboration: the elixir rendering contains `i.e. not hierarchical` exactly
**5** times, one per `.local` block.

Parent `.events` files and whether *their* blocks call the fields hierarchical
(the task only asks about memory, recorded here for precision):

| parent | heading line | hierarchical wording in block |
|---|---|---|
| `memory.events` | 1468 | explicit: 1474, "all fields in this file are hierarchical" |
| `pids.events` | 2441 | **absent** (block 2441-2448 defines `max` only) |
| `rdma.events` | 2823 | 2831: "This is a hierarchical counter: the event is propagated upward to all ancestor cgroups." (14 words) |
| `hugetlb.<hugepagesize>.events` | 2926 | **absent** (block 2926-2930 defines `max` only) |
| `misc.events` | 3010 | 3013-3014: "All fields in this file are hierarchical." (7 words) |
| `cgroup.events` | 955 | no `.local` sibling in this doc |
| `memory.swap.events` | 1853 | no `.local` sibling in this doc |

That asymmetry (two parents silent) does not weaken the memory answer: for
`memory.events` the hierarchy claim is explicit at line 1474, and the contrast
object for `.local` is named in the same paragraph.

## 6. Stale premise in the assignment (recorded, not judged)

The assignment says `raw.githubusercontent.com` "returns HTTP 429" and
`git.kernel.org` "serves a bot wall". Neither reproduced in this window:

- raw.githubusercontent: HTTP **200**, 133236 bytes, byte-identical
  (`curl -fsSL` exit 0 on both the `-o /dev/null` probe and the body fetch).
- git.kernel.org cgit: HTTP **200**, 133236 bytes, byte-identical; the body
  begins `.. _cgroup-v2:` — a real file, not a challenge page.
- The requested "second independent route" therefore was not needed to
  recover the text, but one exists and is byte-identical: the GitLab
  `linux-kernel/linux` mirror (and elixir as an independent rendering).

So today the primary route was not required, and the two named failure modes
are route conditions that vary with time/quota, not properties of the URL.
A later seat must not copy "429"/"bot wall" forward as fact without re-running
the fetch.

## 7. Retained artifacts (TMPDIR)

`TMPDIR=/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-45/tmp/ScoutKernelDoc`

| file | bytes | sha256 |
|---|---|---|
| `cgroup-v2.rst` (primary) | 133236 | `a9433bb0e16a67f07a93424c7bf842f47616e9b0a27b51e17d7b34cff246b7ad` |
| `raw-gh.rst` | 133236 | same |
| `gko.rst` | 133236 | same |
| `gitlab-mirror.rst` | 133236 | same |
| `elixir.html` | 3157249 | `88dca0d9a960d1bb6ca6481f79d84d72b89535fd903db0c5efbb4159e686066d` |

**Primary copy sha256 to cite: `a9433bb0e16a67f07a93424c7bf842f47616e9b0a27b51e17d7b34cff246b7ad`.**

## 8. Method (reproduction)

```
T=/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-45/tmp/ScoutKernelDoc
mkdir -p "$T"
curl -fsSL --max-time 40 -w 'HTTP=%{http_code} SIZE_DOWNLOAD=%{size_download}\n' \
  -o "$T/cgroup-v2.rst" \
  https://cdn.jsdelivr.net/gh/torvalds/linux@v7.2/Documentation/admin-guide/cgroup-v2.rst
# HTTP=200 SIZE_DOWNLOAD=133236, exit=0
sha256sum "$T/cgroup-v2.rst"; wc -lc "$T/cgroup-v2.rst"
grep -nE '^  [a-zA-Z][^ ]*\.events(\.local)?$' "$T/cgroup-v2.rst"
grep -n 'events\.local' "$T/cgroup-v2.rst"
grep -n 'not hierarchical' "$T/cgroup-v2.rst"
awk 'NR>=1474 && NR<=1476 {printf "%s ", $0}' "$T/cgroup-v2.rst"   # quote A
```

Word counts (one line each, from the exact quoted text):

```
$ printf '%s\n' 'Note that all fields in this file are hierarchical and the file modified event can be generated due to an event down the hierarchy.' | wc -w
24
$ printf '%s\n' 'For the local events at the cgroup level see memory.events.local.' | wc -w
10
$ printf '%s\n' 'Similar to memory.events but the fields in the file are local to the cgroup i.e. not hierarchical.' | wc -w
17
```

All quotes are <= 25 words. Line numbers are from `grep -n`/`awk NR` on the
retained primary copy; the elixir `<pre>` extraction independently reproduced
the same line indices (1474, 1517, 1519, 2452, 2847, 2934, 3022).

## 9. Confidence and remaining unknowns

- Confidence: **high**. Four HTTP deliveries are byte-identical under one
  sha256; a fifth (elixir) reproduces the identical text with identical line
  numbering after HTML unescape; the tag resolves to one commit via the
  GitHub API.
- Open, time-dependent only: whether raw.githubusercontent and git.kernel.org
  rate-limit or bot-wall later. Re-run the two `curl` probes before trusting
  any "unavailable" claim.
- Side observation, outside this ticket: `git -C <lane> rev-parse HEAD` at
  10:43:37Z printed `3ad8faaa637ae466c61f9427fea1c208bf49ea82`, while
  `.ufo/waves/round-45/contract.md` names the entering tip
  `554ff416459c92f0dea9762f834a556df2990187`. Recorded as observed; not
  investigated here.
