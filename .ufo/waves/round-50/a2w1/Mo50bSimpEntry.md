# Mo50bSimpEntry — redundancy pass on the C2 entry, prose sections only

Seat: `Mo50bSimpEntry` (simplifier, a2w1). Lane bounds: leaf, no subagents spawned. Nothing written except
this file. No tool installed or upgraded (nothing was needed); **no pacman transaction was attempted**
(host-wide pause), no `uv`/`npx`/binary install. Scratch
`/fast/scratch/hyaku/mori-r50/Mo50bSimpEntry/` was created, used with `TMPDIR` inside it, and removed at the end
(`shutil.rmtree`); nothing cited below lives there any more — every quoted byte is reproduced in this file.

Target: `corpus/knowledge/oom-memcg-stat-r50.md` at the landed revision
`487941b9395e89678af0053cc443cdb49cdee6e3` (`git show 487941b9:corpus/knowledge/oom-memcg-stat-r50.md`,
83 lines, 1585 words, sha256 `0fac741cce21d76eda26b9b0a915509e34be499b52041cb7e6c3b1c8cb97c109` — identical to the
working-tree file). Lane HEAD during the pass: `4548a34dc8b4072abaa4335c1f54a9efcfcc314a`; the lane tree was not
modified (`git status --porcelain`: only the pre-existing untracked `a2w1/` wave dir, `a2w1.ready`, and
round-40 scratch dirs of other seats — see F5).

Reads: `.ufo/waves/round-50/contract.md`, `count-c2.py` (all 391 lines: `normalise`/`normalise_text`,
`words_beyond`, `parse_claims`, `sources_row`, `evaluate`, `git_reader`, `main`, and the full selftest),
`corpus/SOURCES.md` rows S489–S491 (lines 268–270), the three committed copies, the mandated shape in
`.ufo/waves/round-50/w1-spec.json` (`Mo50ScribeEntryA` prompt), and the sibling a2w1 reports that quote this
entry's prose (`Mo50bScoutStagedCharge.md`, `Mo50bRevRowsCgroupB.md`, `Mo50bExecHostStatKeys.md`,
`Mo50bRevRowsMemcgA.md`) to avoid breaking peer citations.

## Method

- Frozen C2 counter run unmodified; no predicate, counter, control or kill rule touched. The claims table
  (26-line block `## Claims` … last row, lines 17–42) and the front matter (lines 1–8) were kept **byte-identical**;
  only the intro paragraph, `## Reading rules` and `## Limits` were rewritten. `## Boundaries` is unchanged verbatim.
- Scored two ways: (a) the requested importlib + dict-backed `read`, (b) the real `count-c2.py` CLI against a
  throwaway fixture repo built with `git init` in scratch, `git rev-parse --show-toplevel` verified equal to the
  fixture path before the first commit, identity passed per-commit via `-c user.name=fixture
  -c user.email=fixture@invalid.invalid` (no other repo touched).

## Evidence — instrument runs

1. Baseline, frozen command at the landed rev (unmodified file):
   ```
   $ python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-50/count-c2.py 487941b9395e89678af0053cc443cdb49cdee6e3
   C2=met claims=22 located=22 quote_missing=0 bad_rows=0 sources=3 source_rows=ok pins=ok provenance=ok rev=487941b9395e89678af0053cc443cdb49cdee6e3
   exit=0
   ```
2. Draft, importlib `c2.evaluate(read, rev)` with a dict-backed reader whose only override is the entry path
   (every other path is `git show 487941b9:<path>` bytes; the three copy sha256s recompute `True` against
   `COPIES`, so `pins=ok` is genuine, not inherited):
   ```
   ORIG:  True C2=met claims=22 located=22 quote_missing=0 bad_rows=0 sources=3 source_rows=ok pins=ok provenance=ok rev=487941b9395e89678af0053cc443cdb49cdee6e3
   DRAFT: True C2=met claims=22 located=22 quote_missing=0 bad_rows=0 sources=3 source_rows=ok pins=ok provenance=ok rev=487941b9395e89678af0053cc443cdb49cdee6e3
   ```
3. Draft, real CLI in a fixture repo (`corpus/SOURCES.md`, `corpus/evidence/sources-r50/` and the drafted entry
   extracted with `git archive 487941b9`, one commit, draft file sha256
   `81fb826698d8d084c9ab10114f472a941d31ce806093231080073750cb4c28c4`):
   ```
   $ python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-50/count-c2.py d3bf314da5f1bbf150612f7a825e11101ece934a --repo /fast/scratch/hyaku/mori-r50/Mo50bSimpEntry/tmp/fixture-final2
   C2=met claims=22 located=22 quote_missing=0 bad_rows=0 sources=3 source_rows=ok pins=ok provenance=ok rev=d3bf314da5f1bbf150612f7a825e11101ece934a
   exit=0   stderr: (empty)
   ```
4. Blindness arm (evidence for F3, run through the same importlib path): an entry consisting of the front matter
   plus the claims table and **no prose at all** still scores
   `C2=met claims=22 located=22 … provenance=ok`, exit 0. The counter cannot see any prose sentence; a prose-only
   edit is therefore verified by C2 only in the negative sense that nothing in the scored surface moved.

Reproduction (any scratch clone holding `corpus/SOURCES.md`, the three `corpus/evidence/sources-r50/` copies and the
entry): apply blocks A and B below to the entry, confirm the result's sha256 is
`81fb826698d8d084c9ab10114f472a941d31ce806093231080073750cb4c28c4` (1464 words, 77 lines), commit it in that
scratch repo and run `python3 <lane>/.ufo/waves/round-50/count-c2.py HEAD --repo <scratch>`; expected
`C2=met claims=22 located=22 quote_missing=0 bad_rows=0 sources=3 source_rows=ok pins=ok provenance=ok`, exit 0.
No such scratch repo is left on disk (directive).

## Redundancy removed (original line numbers; where the fact survives)

Notation: `R<n>` = claims-table row, numbered from the header: R1 = line 21 … R22 = line 42.

| # | Original lines | Redundancy | Action in draft | Fact still lands on |
|---|---|---|---|---|
| 1 | 11–12 | intro: “block written by the same formatter that writes memory.stat” restates R12 (line 32) in full | folded into a 9-word parenthetical, “the memory.stat breakdown, written by the same formatter” | R12 (quote), draft intro |
| 2 | 12 | intro: “carrying the victim’s own counters” restates R16 (line 36) | dropped from the intro | R16 claim + quote; draft reading rule 5 (“charge, not the victim's”) |
| 3 | 13–15 | intro: three sentences to say (a) global prints a summary instead of the block (=R18, line 38), (b) global names no scope (=R13, line 33), (c) the detection rule | merged into one 24-word sentence; the framing sentence “That difference is the detection rule this entry serves:” deleted | R18, R13 quotes; the rule itself kept (“a stats block means the kill was charged to one”) |
| 4 | 49–51 | reading rule restated R6 (line 26) verbatim (7-word run “a newer kernel can insert a counter”) and added the unactionable “the entries are ordered for humans” | kept the imperative (“Look keys up by name, not by position”) and deleted the restated justification | R6 claim + quote |
| 5 | 52–53 | glossary restated R2–R4 (lines 22–24), incl. R4's “tmpfs, shm segments, shared anonymous mmap” inheritance list; only “Do not add” was new | compressed to one clause that keeps the three-way distinction as guidance (“anon is the heap, file is page cache …, shmem is the swap-backed part of file”) + the warning verbatim | R2–R4 quotes; mandated “anon vs file vs shmem” topic kept |
| 6 | 54–55 | “`kernel` already contains kernel_stack, pagetables, percpu, vmalloc and slab, which are also printed on their own lines” restates R5 (line 25), whose claim already ends “each of those five is also printed under its own name” | reduced to “`kernel` already contains the sub-keys printed on their own lines;” + the new consequence | R5 claim + quote |
| 7 | 56–58 | two of three clauses restated R16 (victim's anon-rss/file-rss/shmem-rss) and R13/R14 (two labels) | kept “The block is the cgroup's charge, not the victim's.” verbatim (cited by `Mo50bScoutStagedCharge.md`:21) + the label distinction as one clause + the NOTE (prose-only) | R16, R13, R14 claims |
| 8 | 59–60 | replayed R15's 10-word quote `are going to be killed due to memory oom group` outside the table | replaced by “A `memory.oom.group` kill prints its own task-naming line” | R15 claim + quote |
| 9 | 61–62 | “or what caused the cgroup to grow” duplicated `## Boundaries` line 83 “not what made it grow” | dropped here, kept in Boundaries (attribution belongs there) | Boundaries line 83 (unchanged) |
| 10 | 70–72 | Limits bullet replayed R19's 9-word code quote verbatim and restated both of R19's facts (summary rate-limited, victim line not) | kept only the consequence and its reader-facing use (“`Killed process` is printed outside the rate-limited summary, and its message prefix says which kind of kill it was”) | R19 claim + quote; R17 for the prefix |
| 11 | 75–76 | “states what the kernel prints, not what any past kill on this host printed” repeated the preceding sentence's implication | two sentences merged into one (“No host block was read: … so this states …”) | same content, one colon instead of a sentence break |

Not changed (and deliberately so): the three `source:` lines and `recheck:` command/hashes, the 22 table rows, the
`## Boundaries` section, the mandated section names, and the four mandated `## Reading rules` topics (units per
line; look up keys, not positions; anon/file/shmem; what the block cannot tell) and four mandated `## Limits`
topics (v7.2 only; cgroup v2 only; no host block read; the MESSAGE-text rule).

## Preserved contract — phrases other seats cite, kept verbatim

Checked as exact substrings of the draft (all present): `The block is the cgroup's charge, not the victim's`
(`Mo50bScoutStagedCharge.md`:21), `summing every key double counts kernel memory`
(`Mo50bScoutStagedCharge.md`:68, `Mo50bRevRowsCgroupB.md`:23 — kept lowercase mid-sentence, as in the original),
`What the block cannot tell: which process held` (`Mo50bScoutStagedCharge.md`:88), `compile-time conditional`
(`Mo50bExecHostStatKeys.md`:273), `SEQ_BUF_SIZE` buffer (`Mo50bExecHostStatKeys.md`:245,
`Mo50bRevRowsMemcgA.md`:82), `one victim line per killed mm`, `missing block is not evidence`,
`Do not add `file` and `shmem``, `so a missing key is not a zero`, `` `K()` converts from pages ``.

Structural identity checks on the draft:
- front matter (lines 1–8): byte-identical to the original;
- claims block (`## Claims` … last row, 26 lines): byte-identical,
  sha256 `b8f7fadf22c825bc4eabe98a7473a4eecf7a89d7630ab6d92ff3831f1c83e9d8`;
- `## Boundaries` (6 lines): byte-identical;
- intro: 4 lines (mandated 3–5);
- no line over 122 chars outside front matter and table rows; no tabs, no trailing whitespace; single final newline.

## Draft (fenced) — prose sections only

Integration: (1) replace the intro paragraph (original lines 10–15) with block A; (2) replace everything from
`## Reading rules` through the end of `## Limits` (original lines 44–77) with block B; (3) leave lines 1–9, the
`## Claims` block (17–42) and `## Boundaries` untouched. Assembled that way, the file is 77 lines / 1464 words /
sha256 `81fb826698d8d084c9ab10114f472a941d31ce806093231080073750cb4c28c4`.

Block A — intro (replaces original lines 10–15):

```
mori attributes a kill at event time: which cgroup was over its charge, what it held, and which process died. A
memcg OOM prints all three in one burst: a usage/limit line, a `Memory cgroup stats for <path>:` block (the
memory.stat breakdown, written by the same formatter) and a per-victim `Killed process` line. A global OOM prints a
system-wide summary in place of that block and names no scope, so a stats block means the kill was charged to one.
```

Block B — replaces original lines 44–77 (`## Reading rules` … end of `## Limits`):

```
## Reading rules

- Units are per line: kB on the usage, swap and `Killed process` lines (`K()` converts from pages), pages in the
  `Tasks state` table, bytes in the stats block; convert before comparing across lines.
- Look keys up by name, not by position: the key set is compile-time conditional — `zswap`, `zswapped`, `swapcached`,
  `anon_thp`, `file_thp`, `shmem_thp` and `hugetlb` need their CONFIG options — so a missing key is not a zero.
- `anon` is the heap, `file` is page cache (tmpfs and shared memory included) and `shmem` is the swap-backed part of
  `file`. Do not add `file` and `shmem` — `file` already contains `shmem`.
- `kernel` already contains the sub-keys printed on their own lines; summing every key double counts kernel memory.
- The block is the cgroup's charge, not the victim's: the `oom-kill:` line carries the cgroup path and the victim's own
  path as separate labels, and the source's NOTE on `mem_cgroup_print_oom_context` says the two can differ when
  hierarchy is enabled.
- A `memory.oom.group` kill prints its own task-naming line and then one victim line per killed mm; `oom_kill` counts
  processes while `oom_group_kill` counts group events.
- What the block cannot tell: which process held which byte, or whether the charge was a leak or one large allocation.
  It reports state at the kill, not history.

## Limits

- Kernel v7.2 only, read from the frozen copies whose sha256 the counter pins; later kernels add or rename keys and can
  change the report path.
- cgroup v2 only. On a v1 hierarchy the same function prints `memory+swap` and `kmem` lines and a real per-page failcnt,
  which cgroup v2 does not have; nothing here carries over to v1.
- A missing block is not evidence that the kill was global: `Killed process` is printed outside the rate-limited summary,
  and its message prefix says which kind of kill it was.
- The block is formatted into a static `SEQ_BUF_SIZE` buffer under `oom_lock`, and an overflow only prints a warning, so
  a truncated block is possible at event time.
- No host block was read: the lane's rule forbids reading kernel journal MESSAGE text for kill records, so this states
  what the kernel prints, not what any past kill on this host printed.
- A located quote proves the quoted words occur in the committed copy, not that the claim cell follows from them.
```

## Prose-only assertions retained (no table row backs them)

These are claims; none was dropped, and each is checkable in the committed copies. They are listed because the
counter cannot see them (F3) and because they are the part of the entry that no row defends:

| Assertion (draft location) | Backing in the frozen copies |
|---|---|
| `` `K()` converts from pages `` (units rule) | **not in the three copies** — `K()` is not defined in any of them; `memcontrol.c.v7.2`:29 includes `<linux/page_counter.h>`, and the copies support only the kB-format inference (F2) |
| CONFIG-conditional key list (`zswap`, `zswapped`, `swapcached`, `anon_thp`, `file_thp`, `shmem_thp`, `hugetlb`) | `cgroup-v2.7.2.html`:1437, 1439, 1452, 1455, 1458, 1461, 1583 |
| “one victim line per killed mm” | `oom_kill.c.v7.2`:1042 (`__oom_kill_process` per victim) and 1050–1051 (`mem_cgroup_scan_tasks(oom_group, oom_kill_memcg_member, …)`); the print is 945 |
| `oom_kill` counts processes, `oom_group_kill` counts group events | `cgroup-v2.7.2.html`:1378, 1381 |
| NOTE on `mem_cgroup_print_oom_context` (labels can differ when hierarchy is enabled) | `memcontrol.c.v7.2`:1767–1774 |
| v1 prints `memory+swap` and `kmem` lines and a real per-page failcnt | `memcontrol.c.v7.2`:1816–1820 |
| static `SEQ_BUF_SIZE` buffer under `oom_lock`; overflow only warns → truncation possible | `memcontrol.c.v7.2`:1794, 1798, 1757–1758 |
| “`Killed process` is printed outside the rate-limited summary” | `oom_kill.c.v7.2`:1030–1033 (guard: `dump_header`, `dump_oom_victim`) vs 945–951 (`pr_err`), called from 1042 after the guard |
| Detection rule (a stats block ⇒ charge was in a scope) | inference from R13 + R18 |
| “It reports state at the kill, not history.” | inference from the block's content |
| later kernels add/rename keys, can change the report path | version bound, not a copy fact |

## Metrics

| Surface | Before | After | Delta |
|---|---|---|---|
| intro (lines 10–15) | 107 words / 6 lines | 80 words / 4 lines | −27 |
| `## Reading rules` | 294 words | 217 words | −77 |
| `## Limits` | 190 words | 173 words | −17 |
| `## Boundaries` | 40 words | 40 words | 0 |
| prose total | 631 words | 510 words | **−121 (−19.2%)** |
| whole file | 1585 words / 83 lines | 1464 words / 77 lines | −121 / −6 lines |
| prose bullets sharing a ≥7-word verbatim run with the table | 3 (runs of 7, 10, 9 words) | 0 (longest 6) | −3 |
| prose 4-grams that also occur in the table text | 22 / 628 (3.5%) | 3 / 505 (0.6%) | −19 grams |
| repeated 5-grams inside prose | 0 (the duplication was paraphrase, not literal) | 0 | 0 |

Claims in the table: 22 before, 22 after, byte-identical. Claims dropped: 0 (11 restatements removed, each traced
to the row or section that still carries it in the table above).

## Named limits of this pass

- The C2 counter is blind to every prose sentence (evidence: prose-less entry still `C2=met`). This pass is
  therefore **not** counter-verified in the positive direction: the counter proves only that the scored surface
  (front matter probe, 22 rows, sources, pins) is unchanged. The prose-level judgement below is mine as a
  dispatched seat, not an independent one.
- The simplification trades one hop for the duplicated mechanism: where the original restated *why* (the
  rate-limit guard, the group-kill string, the formatter identity), the draft names the print and leaves the cause
  to the row 20–40 lines above. A reader who does not scroll reads less justification, not different facts.
- Reading-rule topics are fixed by the w1 shape, so bullets 1 and 3 still overlap their rows at the level of
  vocabulary (units; key meaning); the overlap was reduced to the actionable form rather than eliminated.
- Not attempted: any edit to `corpus/SOURCES.md`, `SCORECARD.md`, `SHONEN.md`, `LOG.md`, `corpus/evidence/`, or any
  frozen file under `.ufo/waves/round-50/` other than this report. The claims table is off-limits to this seat, so
  the row-level precision issue in F1 is reported, not fixed.
- No host read of any kill record; no cgroup limit, unit or config touched; `/home/vgpnk/Projects/shokuknow` was
  not read at all in this pass.

## Findings

- **MED — F1, claims-table row 19 (file line 39) conflates two different prints.** Its claim says “the victim line is
  not [rate-limited]”, but its quote is the guarded block: `if (__ratelimit(&oom_rs)) { dump_header(oc);
  dump_oom_victim(oc, victim); }` at `corpus/evidence/sources-r50/oom_kill.c.v7.2`:1030–1033. `dump_oom_victim`
  (`oom_kill.c.v7.2`:444–453) prints the `oom-kill:` context line — the subject of row 20 — so the quote shows the
  *context* line being rate-limited. The unguarded victim print is the `Killed process` `pr_err` at
  `oom_kill.c.v7.2`:945–951 inside `__oom_kill_process`, called at line 1042 after the guard. The claim is true of
  `Killed process` only; as written a reviewer opening the quote reads the opposite. L1 decision (I may not edit the
  table): either name the print in the claim cell, or re-quote `__oom_kill_process`'s `pr_err` placement. The draft's
  `## Limits` bullet names the print explicitly, so the prose no longer carries the ambiguity.
- **MED — F2, one prose assertion has no source inside the frozen copy set.** `` `K()` converts from pages `` (units
  rule; also load-bearing for comparing kB and byte lines) is a macro no copy defines: `memcontrol.c.v7.2`:29 includes
  `<linux/page_counter.h>`, which is neither one of S489–S491 nor among the committed copies. The three copies support
  only the inference: the usage line's format string prints `%llukB` and its argument is
  `K((u64)page_counter_read(&memcg->memory))` (`memcontrol.c.v7.2`:1806, 1807; same shape at 1810–1811), so `K()`
  turns a page count into kB. A reader who checks the sentence against the three copies cannot close it. Options for
  L1: keep as prose (current), or cite the header as an additional source. Not fixable by this seat.
- **LOW — F3, C2 cannot see prose; a prose-only edit is unverified by the instrument.** Measured: the entry reduced
  to front matter + claims table scores `C2=met … provenance=ok`, exit 0. Recorded as a named limit rather than a
  counter change (counters are frozen for this round).
- **LOW — F4, `## Reading rules` is a one-off section name in this corpus.** `grep -l "^## Reading rules"
  corpus/knowledge/*.md` → only `oom-memcg-stat-r50.md`. Of the other 58 entries, 12 open with `## Claim`, 3 with
  `## Scope`, 10 have no `##` heading at all, and 33 open with a topic heading (e.g. `## Decision table`,
  `## Claims`, `## Why this entry`). The name was mandated by the w1 shape (`w1-spec.json`, `Mo50ScribeEntryA`:
  “Then `## Reading rules` (how to read the block…), `## Limits` … and `## Boundaries`”), so it is kept; noted only
  so the next round does not read it as drift.
- **LOW — F5, pre-existing untracked scratch in the lane tree, not mine.** `git status --porcelain` shows
  `.ufo/waves/round-40/scratch/mori-conform-selftest-*/` directories present before this pass began (contract §5
  item 4 lists them as to-delete at round end). This seat created none and deleted none.
- **LOW — F6, `## Limits` bullet “A located quote proves the quoted words occur …” is contract vocabulary, not a
  kernel limit.** Kept because it is the entry's honesty statement about P-C2's named limit; it is the only bullet
  a reader of the kernel cannot act on, and it is one sentence long.
