# CriticC1Counter — round 31 wave 1: falsifying the C1 counter and controls

Seat: MoriR31.CriticC1Counter (critic, leaf). Lane tip read: `8baccf4ac9c44a38848d90c34df52392e804c168`.
Inputs: `.ufo/waves/round-31/contract.md:28-54`, `.ufo/waves/round-31/count-c1.py:1-180`,
`.ufo/waves/round-31/evidence/c1-controls.txt:1-35`, `scripts/hyaku/lane-addendum.md:203-225` (fleet root),
`AXES.md:11-12,20-22` (fleet root).
Sandbox: `/fast/scratch/hyaku/mori-r31/CriticC1Counter/lane` (a `git clone --no-hardlinks` of the lane, git run with
GIT_DIR, GIT_WORK_TREE and GIT_INDEX_FILE unset). No lane writes except this report. No tools installed. No processes
left running. The skill file `skill://godspeed` could not be found on disk (`find / -xdev -type d -name godspeed` → no
output), so I worked without it.

## Verdict

The frozen counter prints `C1=met` (exit 0) on an entry that has no sourced content at all. The cheapest control that
skips the claimed work therefore reaches the target. Addendum §9 (`lane-addendum.md:212-216`) says this means "the
counter or target is wrong". The counter is frozen, so I propose no change to it. The result is that a `C1=met` receipt
is necessary but not sufficient: the depth substance can only come from the hand residual below, and that residual is
wider than the one the contract names (`contract.md:53`).

## F1 — counterexample run under the frozen counter (Critical)

Sandbox commit `9140d11c24ff3aad52c626c634d368bd50401d5a` (parent: the lane tip). Receipt:
`/fast/scratch/hyaku/mori-r31/CriticC1Counter/f1-receipt.txt`. Diff: `.../CriticC1Counter/f1-diff.patch`.

```
$ python3 .ufo/waves/round-31/count-c1.py 9140d11c24ff3aad52c626c634d368bd50401d5a --repo /fast/scratch/hyaku/mori-r31/CriticC1Counter/lane
rev=9140d11c24ff3aad52c626c634d368bd50401d5a
entry=present head_lines=yes
tables=1 decision_tables=1
rows=8 rows_ok=8 new_id_rows=8 new_ids=4 (S161,S162,S163,S164)
S161 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/fs/binfmt_script.c
S162 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/refs/tags/v7.2/fs/binfmt_script.c
S163 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/filesystems/proc.rst
S164 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/fs/proc/base.c
gates_ok=4/4 copies_ok=4/4 fetch_ok=4/4
skill_rows=4
C1=met
exit=0
```

What F1 contains. Each property below is accepted independently, as the cited code shows:

1. **Nothing renders.** The head lines, the table, the Gate rows, the SOURCES rows and the SKILL lines all sit inside
   `<!-- ... -->` HTML comments. The counter scans raw lines with no awareness of comments or code fences
   (`count-c1.py:92`, `:97-107`, `:83-86`, `:135`, `:166`).
2. **Empty quotes.** Every Gate row's only quote is `(0 words): ""`. The regex `"((?:[^"\\]|\\.)*)"` accepts an empty
   string (`:147`). An empty quote has 0 words, so it passes `<= 25` (`:148`). `norm('') in norm(copy)` is always true
   (`:155-156`). There is no `file:L-M` locator either: the regex never reads the `` `file:L-M` `` part of the binding
   format (`contract.md:45`). The declared N is never compared with the real word count.
3. **Head lines with no content**: `source: none`, `verified-at: never`, `recheck: never`. The check is only
   `startswith` (`:92`).
4. **Duplicated rows**: eight identical `| x | x | x | S097 S161 S162 S163 S164 |` rows. No row is checked for being
   distinct (`:116-126`).
5. **Rows that cite a rejected source**: S097 has status `rejected` (`corpus/SOURCES.md:103`). Row validity only asks
   whether some `| S### |` line exists (`:83-86`, `:121`). That set includes 17 rejected and 25 queued rows (an awk count
   of the status column over `SOURCES.md:7-166`: 118 mined, 25 queued, 17 rejected).
6. **Four "new" ids that are two files, both already registered**:
   - S161 and S162 are the same file reached by two URL spellings (`v7.2/` and `refs/tags/v7.2/`). Both hash to
     `81b0293a89908d56575f2b00b3550f927eb80714ef540f9634272bce56f9c656` (4358 B, fetched 2026-10-22T23:45:27Z).
   - S163 is S082's URL with S082's bytes: `SOURCES.md:88` records `sha256 e760f716f8278dee`, and my fetch hashes to
     `e760f716f8278deefab17a63739033cadc7faee93663c49e76455afaaf40d126`.
   - S164 is the URL and bytes of S127 and S148: `cef1a2cf…915c6` (`SOURCES.md:133,154`,
     `corpus/lessons/round-28.md:68`).
   - The counter never compares sha256 or URL across new ids, or against existing rows (`:134-161`).
7. **Empty SOURCES rows**: `| S161 | x | x | x | x | x | x | rejected | x | x | x |`. Only the count of rows is
   checked (`:138`). Status, URL and scope are not.
8. **SKILL lines that only point at the path**: four identical lines, each `Round31 knowledge/watchdog-identity-r31.md`.
   The check is a plain substring match (`:166`). It also accepts the path without `corpus/`, and `Round31` also matches
   `Round310`.

Answer to the first question: yes, every shortcut named in the assignment prints `C1=met`. The F1 commit combines all of
them. Each one also passes on its own, because none is checked anywhere in the code paths cited above.

## F2 — the committed controls do not include the cheapest skip (High)

Control (b) (`c1-controls.txt:20-34`) differs from F1 only in using copies that are not the upstream bytes, so it only
exercises the fetch check (`fetch_ok=0/4`). No control uses real upstream bytes with vacuous or irrelevant quotes. That
is the obvious cheap skip once the URLs are public, and addendum §9 requires it ("build the cheapest control that skips
the claimed work", `lane-addendum.md:213-216`). The controls receipt therefore does not establish that a skip cannot
reach the target. F1 shows that one can.

## F3 — pre-assigned new ids that are existing sources renumbered (High, affects the >=4 new ids count)

| pre-assigned id | URL in the assignment | existing row with identical URL and bytes |
|---|---|---|
| S166 | Linux v7.2 `fs/proc/base.c` | S127 (`SOURCES.md:133`) and S148 (`SOURCES.md:154`); sha `cef1a2cf…915c6` |
| S168 | Linux v7.2 `Documentation/filesystems/proc.rst` | S082 (`SOURCES.md:88`); sha `e760f716…` |
| S169-S172 | man-pages 6.20 single pages | S146 is the man-pages 6.20 release tarball (`SOURCES.md:152`, status mined) [INFERENCE: the single pages are members of that tarball; I did not unpack it] |

The lane has precedent for re-registering a file under a narrower scope (S148 repeats S127's URL list). So a new
scope-limited row is not by itself false provenance. But the counter treats S166 and S168 as new sources, and the
contract surface rests on "no SOURCES row on pgrep matching, /proc/<pid>/comm truncation or /proc/<pid>/stat start time
exists" (`contract.md:13-14`). A reviewer must check that the ids counted toward ">=4 such ids" are not byte-identical
to rows that existed at the entering tip. If S166 and S168 are kept, S161-S165, S167 and S173 remain as truly new files.

## F4 — where the code diverges from the predicate sentence (Medium; all fail-closed except the last)

Predicate: `contract.md:30-37`, repeated in the docstring at `count-c1.py:5-14`.

| predicate clause | code | direction |
|---|---|---|
| "every row naming at least one S### that is a SOURCES.md row" | every id in the row must exist, ids are read from the `sources` column only, and the row's cell count must equal the header's (`:120-121`) | stricter: a row citing S027 plus a mistyped S999, or with an unescaped `\|` inside a cell, fails although the predicate is met |
| "exactly one table whose header holds the cells …" | exactly one *matching* table; other tables are allowed (`:108-113`) | reading of an ambiguous sentence; harmless |
| "an https URL" | the first cell that *starts* with `https://` (`:145`) | stricter: `<https://…>` or text before the URL is missed |
| "a 64-hex sha256" | the first backticked lowercase 64-hex string anywhere in the row (`:146`) | stricter on uppercase hex |
| "at least one quote of at most 25 words" | the `(N words): "…"` regex anywhere in the row; empty quotes accepted; N not checked; locator not read (`:147-148`) | literal, but vacuous (F1 point 2) |
| "contains every quote" | substring match after whitespace collapse, not bounded at word edges (`:155-156`) | literal; a one-letter quote passes |
| "naming both Round31 and the entry path" | `'Round31' in l and 'knowledge/watchdog-identity-r31.md' in l` (`:166`) | **looser**: the path without `corpus/` counts; `Round310` counts |

None of these divergences lets a sourced entry pass that the predicate would reject, except the SKILL looseness, which
is minor. The real gap is that the predicate itself is satisfiable without content. That is a tradeoff fixed before
data, not a coding defect.

## F5 — false-negative risks for honest work (Medium)

- **The man-pages URL form in the assignment returns 404.** `https://git.kernel.org/pub/scm/docs/man-pages/man-pages.git/plain/man5/proc_pid_comm.5?h=man-pages-6.20`
  gives `curl: (22) … error: 404`. The form `…/plain/man/man5/proc_pid_comm.5?h=man-pages-6.20` gives HTTP 200,
  1347 B, and the same sha prefix `31aee9e50c23579e` on two fetches. The S169-S172 Gate rows must use the `man/manN/`
  path, or `fetch` fails (`:158-159`).
- **Fetches are stable.** gitlab raw for procps v4.0.7 was stable under the counter's plain `curl -sSL --fail`:
  `pgrep.1` was 9702 B with sha prefix `c2024c384dd88df2` twice, and `pgrep.c` was 45309 B with sha prefix
  `af711983209fa083` twice. No bot challenge appeared.
- A network outage at measurement time gives an honest `unmet` (three tries, `:50-55`).

## F6 — the axis: depth by surface, but the number alone is quality work under §9 (Medium)

- **By surface, depth is right.** The C1 surfaces are a knowledge entry with a decision table and cited sources, plus
  `SKILL.md` lines. That is the literal definition of depth: "decision tables with real thresholds, named error
  signatures, cited sources" (`AXES.md:11`). The ground is FR5 (`PROVINCE.md:48`, `corpus/README.md:338`), which has
  only the open false-positive class D06 (`corpus/knowledge/audit-r11.md:201`).
- **It is not coverage.** Coverage moves a governed surface (`AXES.md:12`). §9 asks for "the surface it moves … and the
  command that would show it unmoved" (`lane-addendum.md:223-225`). C1 adds no probe and does not change
  `probe_watchdog`. FR5 stays frontier [INFERENCE: nothing in the C1 file list (`contract.md:22-23`) touches a tool].
- **But §9 applies to the count.** §9 says "counting rows a sourceless fixture also counts, is quality work, never
  coverage or depth" (`lane-addendum.md:222-223`). F1 is a contentless fixture that reaches every count C1 declares. So
  `C1=met` by itself evidences quality work. Depth credit needs a non-author's hand finding that the rows are sourced
  and actionable.
- **The SKILL clause does not test depth's signal.** Depth's signal is "a reader can act on SKILL.md alone"
  (`AXES.md:11`). The counter accepts four pointer lines (F1 point 8). Round 30's convention put real decision rows in
  SKILL.md (`SKILL.md:744-755`). The counter does not require that.
- **Judge-level consequence.** This is a tradeoff the judge must weigh, not a defect the L1 can fix after data:
  §9:217-220 forbids changing the rule once seats score. The contract already says "Score policy: depth stays 5 unless
  an admitted closure states the move" (`contract.md:54`). That is the correct holding position.

## F7 — the receipt hides the evidence a reviewer needs (Low)

- The receipt prints neither the `--repo` path nor any quote text or word count (`:78`, `:161`). An F1-style receipt
  looks the same as a lane receipt except for the revision.
- A reviewer must confirm the revision is a lane commit (`git -C <lane> cat-file -e <rev>^{commit}`) and open the
  lesson rows.

## Residual a reviewer must check by hand (ordered by severity)

```
C1 hand residual (non-author; read-only on the lane; every item is outside count-c1.py)
1. Rendering: the entry's head lines and decision table, the Round31 SKILL lines, the S161+ SOURCES rows and
   their Gate rows are not inside an HTML comment or a code fence.
2. Quotes: each admit Gate row for a counted id has at least one non-empty quote; the `file:L-M` locator
   exists and the quote occurs within those lines of the S###.src copy; the declared N equals `wc -w`
   of the unescaped quote.
3. Row support: for each data row, at least one quote from a cited id states the observation-to-reading
   mechanism the row asserts; a row whose only new ids are cited by name and not supported is not a new-id row.
4. Distinct sources: the counted new ids have pairwise distinct sha256 values, and none equals the sha256 or
   URL of a row present at a12c68ae (check S082, S127, S148 for S168 and S166). Fewer than 4 distinct new
   files means the >=4 new ids clause is met only in name.
5. Distinct rows: the >=8 data rows are pairwise distinct observations (not copies or trivial rewordings).
6. SOURCES rows: each S161+ row has status mined, its URL equals the Gate URL, and its scope matches the quotes;
   no cited pre-existing id is rejected or queued.
7. SKILL lines: the four or more Round31 lines carry decision content a reader can act on (AXES.md:11), not
   only the path; each names corpus/knowledge/watchdog-identity-r31.md in full.
8. Head lines: source:, verified-at: and recheck: carry real values (source ids, a UTC date, a runnable or
   dated recheck).
9. Receipt: the measured revision is a lane commit, and the counting command ran without --repo.
```

## Smallest safe correction (no change to the frozen counter)

1. Commit F1 to the round's evidence as a disclosed post-freeze control that **meets** under the frozen counter:
   `f1-receipt.txt`, plus a note that `C1=met` is necessary and not sufficient. Keep the predicate, counter and
   contract sentence unchanged (`contract.md:5-7`).
2. Route the nine-item hand residual above to wave-2 non-authors, in place of the single line at `contract.md:53`. The
   closure should admit depth only if items 1-6 pass. That matches the existing score policy at `contract.md:54`. Do not
   ship the residual as a second counter, because two counting authorities for one claim would be a duplicate
   authority.
3. When choosing ids, do not count S166 or S168 toward ">=4 such ids" unless their scope rows are plainly new. Write
   the S169-S172 URLs with the `plain/man/manN/` path, or their fetches will 404.

## Evidence index

- F1 commit `9140d11c24ff3aad52c626c634d368bd50401d5a` in `/fast/scratch/hyaku/mori-r31/CriticC1Counter/lane`;
  receipt `.../CriticC1Counter/f1-receipt.txt` (two runs, both `C1=met`, exit 0); diff `.../f1-diff.patch` (68 lines).
- Upstream copies: `.../CriticC1Counter/src/{71581951,718c5cef,822c27fc,578ce15a}`, fetched 2026-10-22T23:45:27Z
  with `curl -sSL --fail -m 60`.
- Tools installed or updated: none.
