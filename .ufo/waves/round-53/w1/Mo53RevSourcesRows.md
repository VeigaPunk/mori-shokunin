# Mo53RevSourcesRows — rows S502–S513 against the SOURCES registry contract

Seat: reviewer, round 53 wave w1. Reviewed at data commit `2a4213bf8da72f7cd78189baa5bb9be825dca1df`
(entering tip `20edafa59b38dac1ca358893f0259b1f436372d3`). Contract read first:
`.ufo/waves/round-53/contract.md`; registry contract read from `/home/vgpnk/Projects/shokunin/CORPUS.md`
§`SOURCES.md — where a shokunin learns` (contract v1, frozen) and §Rules 1–6.

Working tree at review time: `git rev-parse HEAD` → `95cf78eef71979f9b740ef6bc3c5299b6beff86e` (w1 spec commit, on top of the
data commit); `git diff --stat 2a4213bf 95cf78ee -- corpus/SOURCES.md` printed nothing, so the working-tree
`corpus/SOURCES.md` is byte-identical to the data commit. All reads below are of that file; row line numbers are
its lines.

Scratch: `/fast/scratch/hyaku/mori-r53/Mo53RevSourcesRows/` (created with `mkdir -p`, `TMPDIR` exported;
removed at the end). Only cgit fetches and `git show`/`diff` reads were performed against the lane; no lane file,
git index or jj state was touched.

## What was checked

| contract cell | check performed | result |
|---|---|---|
| id | `S`+digits, next unused, never reused | S502–S513 follow S501 contiguously; duplicate-id sweep prints nothing |
| source | title — canonical URL | each row carries a URL; S502–S510 cgit `plain/<path>?h=v7.3`, S511–S513 cgit `?h=v7.2` |
| kind | enum | docs (S502, S506, S507), code (S503, S504, S505, S508, S509, S510, S511, S512, S513) — all in enum |
| tier | A/B/C, scoped | all A; source code and official docs are A by definition; no `community` row, no tier inflation |
| scope | claim/topic | present in all 12; two scope/anchor mismatches (F12, F5) |
| anchor | exact lines + revision | revision strings verified against `git ls-remote` (`evidence/sweeps.txt`); all line numbers spot-verified in the committed copies (table below); one range wrong (F2) |
| teaches | one grounded benefit | present in all 12; three cells understate the diff they describe (F3, F8, F9) |
| status | `mined` = cited by ≥1 `used-by` path | all 12 `mined`; every named path exists and cites the row (see next table) |
| opened | ISO date of opening | all 2026-10-26; matches the access date in `evidence/sweeps.txt` (2026-10-26) and my own re-fetch date |
| recheck | ISO date or cadence | all `on-release` — legal cadence |
| used-by | repo-relative paths, exist, and the entry cites the row | verified row by row (table below) |

### `used-by` resolution (path exists → entry cites the row)

| row | used-by path | path exists | entry cites the row |
|---|---|---|---|
| S502–S510 | `corpus/knowledge/kernel-v7.3-recheck-r53.md` | yes | yes — nine `source:` lines 3–11 and ledger rows 48–93 |
| S511, S512, S513 | `corpus/knowledge/commit-runway-read-r53.md` | yes | yes — `source:` lines 4–6 and claim rows 24–28 |
| S499 (after change) | `corpus/knowledge/overcommit-commit-limit-r52.md`, `corpus/knowledge/commit-runway-read-r53.md` | both yes | both cite S499 (r52 rows + r53 entry line 3 and rows 29–31) |

## Anchor verification (independent, against the copies and against cgit)

Revision strings first: `git ls-remote https://github.com/torvalds/linux refs/tags/v7.3 'refs/tags/v7.3^{}' refs/tags/v7.2`
(`evidence/sweeps.txt`) gives `091b06388b11…` = the annotated tag object, `c03c1a14507d…` = `v7.3^{}` commit,
`237a1c39e8df…` = `refs/tags/v7.2`. The rows' `tag v7.3 (091b06388b11, commit c03c1a14507d)` and `tag v7.2 (237a1c39e8df)`
match exactly.

Then every `sha256` cell, checked twice: against the committed copy under `corpus/evidence/sources-r53/`, and against a
fresh fetch from git.kernel.org cgit (2026-10-26, `curl -fsSL …/plain/<path>?h=<tag>` into scratch):

```
proc.rst.v7.3            bc178ff511e0…  cgit v7.3 bc178ff511e0…   S502 ok
show_mem.c.v7.3          c50205bc1997…  cgit v7.3 c50205bc1997…   S503 ok
meminfo.c.v7.3           d6c5807421a6…  cgit v7.3 d6c5807421a6…   S504 ok  (== v7.2 copy sha, byte-identical claim holds)
mm_inline.h.v7.3         277e99e23ecc…  cgit v7.3 277e99e23ecc…   S505 ok
overcommit-accounting.rst.v7.3 767ab88153c4…  cgit v7.3 767ab88153c4…  S506 ok (== v7.2 copy, byte-identical holds)
vm.rst.v7.3              f81feb3dfca5…  cgit v7.3 f81feb3dfca5…   S507 ok
util.c.v7.3              4dfcce2b8fa8…  cgit v7.3 4dfcce2b8fa8…   S508 ok
mman.h.v7.3              d7bf787c910d…  cgit v7.3 d7bf787c910d…   S509 ok  (== v7.2 copy, byte-identical holds)
mmap.c.v7.3              8e51fb1c10fe…  cgit v7.3 8e51fb1c10fe…   S510 ok
mm_init.c.v7.2           ed691b24afbc…  cgit v7.2 ed691b24afbc…   S511 ok
percpu_counter.c.v7.2    2c26e67751f9…  cgit v7.2 2c26e67751f9…   S512 ok
percpu_counter.h.v7.2    4a107bc381b3…  cgit v7.2 4a107bc381b3…   S513 ok
```

Line anchors, read from the committed copies:

| row | anchor claim | observed | verdict |
|---|---|---|---|
| S502 | meminfo section 1043-1240 (MemAvailable 1127, CommitLimit 1221, Committed_AS 1239) | `meminfo` heading 1043; MemAvailable 1127; CommitLimit 1221; Committed_AS 1239 — but the section runs to 1303 (`vmallocinfo` heading 1304) and Committed_AS's text runs 1239–1252 | field lines right, section extent wrong (F2) |
| S503 | si_mem_available 33-73 | `long si_mem_available(void)` 33, closing brace 73, `EXPORT_SYMBOL_GPL` 74 | exact |
| S504 | meminfo_proc_show from 34; CommitLimit/Committed_AS 125-126 | 34, 125, 126 | exact |
| S505 | folio_is_file_lru at 28 | 28 (`static inline int folio_is_file_lru`) | exact |
| S506 | whole file 1-85 | `wc -l` = 85 | exact |
| S507 | admin_reserve_kbytes 82-109, overcommit_kbytes 823, overcommit_memory 834, overcommit_ratio 859, user_reserve_kbytes 1106-1116 | 82, 823, 834, 859, 1106, 1116 | listed lines exact (109 is the section's blank tail); the `panic_on_unrecoverable_memory_failure` section (926-1004) that this row's `teaches` cell and the new lead cite is not anchored (F11) |
| S508 | overcommit_policy_handler 806, vm_commit_limit 904-916, __vm_enough_memory 959-1003 | 806; 904 with `}` at 916; 959 with `}` at 1003 | exact |
| S509 | vm_acct_memory 76, vm_unacct_memory 81 | 76, 81 | exact |
| S510 | MAP_NORESERVE block 563-571, init_user_reserve 1566, init_admin_reserve 1587 | 563 `if (flags & MAP_NORESERVE) {` … 571 `}`; 1566; 1587 | exact |
| S511 | mm_compute_batch 191-210, mm_compute_batch_init 226-233 | 191 … `}` 210; 226 … `__initcall` 233 | exact |
| S512 | percpu_counter_add_batch 93-113 (SMP path) | 93 … `}` 113 — but line 93 is the `#ifdef CONFIG_HAVE_CMPXCHG_LOCAL` variant (guard at 87, `#else` at 114); the file has no CONFIG_SMP gate | lines right, qualifier wrong (F4) |
| S513 | percpu_counter_read_positive 118-126 (SMP) | 118 … `}` 126, inside `#ifdef CONFIG_SMP` (20 … `#else /* !CONFIG_SMP */` 133) | exact |

`teaches` grounding, re-derived from the v7.2/v7.3 copies with `diff -u` and the entry's own stated command
`diff -u <v7.2 copy> <v7.3 copy> | grep -c '^[-+][^-+]'`:

```
proc.rst 3 ~ show_mem.c 22 ~ mm_inline.h 49 ~ vm.rst 64 ~ util.c 14 ~ mmap.c 190
```

These reproduce the entry's change table exactly (`corpus/knowledge/kernel-v7.3-recheck-r53.md:27-31`), so no number
drift. The three byte-identical claims (S504, S506, S509) are confirmed by both sha256 cells and the committed v7.2
copies. The two "absent" ledger rows citing S510 are the two `vma_flags_set(&vma_flags, VMA_NORESERVE_BIT)` spellings,
which is what S510's `teaches` cell says.

## The S499 `used-by` change (old → new)

`diff -u <(git show 20edafa5:corpus/SOURCES.md) <(git show 2a4213bf:corpus/SOURCES.md)` shows exactly one in-place
registry change plus the twelve appended rows:

```
-| S499 | … | mined | 2026-10-26 | on-release | corpus/knowledge/overcommit-commit-limit-r52.md |
+| S499 | … | mined | 2026-10-26 | on-release | corpus/knowledge/overcommit-commit-limit-r52.md, corpus/knowledge/commit-runway-read-r53.md |
```

Old value: `corpus/knowledge/overcommit-commit-limit-r52.md`. New value: the same path plus
`corpus/knowledge/commit-runway-read-r53.md`. The edit touches only `used-by`, which rule 2 permits in place; the
appended path exists and cites S499 (`corpus/knowledge/commit-runway-read-r53.md:3`, and its rows 29–31 quote it). No
other cell of S499 changed (anchor, scope, sha256, status, recheck all identical across the two revisions).
What rule 2 additionally requires — "each change is logged old→new in the round lesson" — is not yet satisfied: see F1.

## The round-53 search-log note

`corpus/SOURCES.md:344` (inserted inside `## Search log`, which starts at 304 and ends before `## Leads (unopened)` at
348). Checked against rule 5 field by field:

- question/query: present, two of them — C1 ("do the 46 v7.2-pinned claim rows … still hold at Linux v7.3?") and C2
  ("what sizes the error of the committed-memory count the mode-2 test reads?").
- where searched + date: "the nine cited paths at tag v7.3 from git.kernel.org cgit (`plain/<path>?h=v7.3`), opened
  2026-10-26 after raw.githubusercontent.com answered HTTP 429"; the C2 clause names the three v7.2 paths, same date.
- counts: C1 "Identified 9, screened/opened 9, included 9 as S502-S510, excluded 0"; C2 "identified 3, screened 3,
  included 3 as S511-S513, excluded 0"; also records that `mm/util.c` at v7.2 is already S499 rather than opening a
  duplicate row.
- exclusion reasons: n/a, both excluded 0.
- stop rationale: present ("each claim row maps to exactly one file and each band term … to exactly one function").

The note also asserts that "the same paths at v7.2 from cgit matched the lane's committed v7.2 copies byte for byte".
I re-fetched all nine v7.2 paths from cgit and compared sha256 with the committed copies — all nine match
(`proc.rst` e760f716…, `show_mem.c` dba76b26…, `meminfo.c` d6c58074…, `mm_inline.h` 2d4accbb…,
`overcommit-accounting.rst` 767ab881…, `vm.rst` bf8ca026…, `util.c` e702754c…, `mman.h` d7bf787c…,
`mmap.c` 449b8583…). The claim is true.

Two shape deviations: the note merges two bounded searches into one note (F6), and it points the located quotes at
`corpus/lessons/round-53.md` Gate, a file that does not exist at this commit (F7).

The lead bullet added at `corpus/SOURCES.md:351` sits in `## Leads (unopened)` — correct placement for a lead, and it
is a bullet, never a row. Its content ("new in v7.3") is true: `panic_on_unrecoverable_memory_failure` appears in
`vm.rst.v7.3:926` and in the v7.2→v7.3 diff, and not in `vm.rst.v7.2`.

## Census

Command as specified, from the lane root under this seat's scratch TMPDIR:

```
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori
… 23 W04 lines …
mori	ok	/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md
rc=0
```

Compared with `.ufo/waves/round-53/evidence/census-start.txt` (23 W04 lines, `mori ok`, rc 0 at `20edafa5`): the W04
streams are identical line for line — same 23 findings, none added, none removed, and no warning names any of
S502–S513. The 12 new rows therefore introduce no new duplicate-URL signal.

The frozen manual census commands from `CORPUS.md` were also run at the data tip:

```
rows 286 · malformed 0 · tier A=255 B=14 C=17 · status mined=236 queued=24 rejected=26
duplicate ids: (none) · enum/tier violations: (none) · mined used-by missing paths: (none)
```

Rows went 274 → 286 (`+12`), consistent with `git diff --numstat 20edafa5 2a4213bf -- corpus/SOURCES.md` = `15 1`
(twelve appended rows, the S499 rewrite, the search-log note, the lead).

## Residual risk and what I could not check

- The v7.3 copies are proven to be *some* cgit-served bytes and to match my independent re-fetch today; that the tag
  `v7.3` resolves to commit `c03c1a14507d` is proven from `ls-remote`, but I did not build a tag→tree walk of the nine
  paths (a peer seat is doing that). A cgit mis-service would pass my check.
- Access-history claims I cannot verify: that raw.githubusercontent.com answered HTTP 429 on 2026-10-26, and that the
  rows were opened on 2026-10-26 (the date matches the receipts and my fetch date, but opening is an author act).
- Round-53 lesson obligations (Gate rows, old→new log) are unverifiable because the file does not exist — treated as
  an open item, not as a proven violation.
- Census limit worth routing to round 54 rather than fixing here: the twelve new rows pin the same nine files as
  their v7.2 counterparts under different URLs (cgit vs raw.githubusercontent), so a URL-keyed duplicate detector
  cannot relate two rows describing one file. This is expected behaviour, not a row defect; noted so the unchanged
  W04 count is not read as proof that nothing new was added.
- Host kernel wording: `uname -r` = `7.2.11-arch1-1`; the pinned copy is upstream tag v7.2 (7.2.0). I did not obtain
  the Arch build's `mm_init.c`, so a byte-level claim about the host's build is UNVERIFIED.

## Findings

- **F1 · MED** — `corpus/SOURCES.md:278` (S499 `used-by`): the in-place `used-by` append is not logged old→new anywhere.
  Rule 2 requires "each change is logged old→new in the round lesson"; `corpus/lessons/round-53.md` does not exist at
  the data commit and has never existed (`git log --all --oneline -- corpus/lessons/round-53.md` prints nothing), and
  the round-53 search-log note does not state the old and new values. The L1 must land the log with the round lesson.
- **F2 · MED** — `corpus/SOURCES.md:281` (S502 anchor): "meminfo section lines 1043-1240" is not the section extent. In
  `proc.rst.v7.3` the `meminfo` section runs 1043–1303 (next heading `vmallocinfo` at 1304), and the range stops at
  1240, i.e. one line into the Committed_AS definition, which continues to 1252. The three named field lines
  (1127/1221/1239) are correct; the stated range is not.
- **F3 · MED** — `corpus/SOURCES.md:287` (S508 `teaches`): "the release's util.c edits sit in vm_mmap_pgoff and the
  shadow-stack helper" is incomplete. The v7.2→v7.3 diff has four sites; two are outside both named functions:
  `desc->pgoff = vma->vm_pgoff` → `vma_start_pgoff(vma)` in `compat_set_desc_from_vma`
  (`util.c.v7.2:1191` → `util.c.v7.3:1191`) and the same conversion in `call_vma_mapped`
  (`util.c.v7.2:1382` → `util.c.v7.3:1382`). The same wording is repeated at
  `corpus/knowledge/kernel-v7.3-recheck-r53.md:31`.
- **F4 · LOW** — `corpus/SOURCES.md:291` (S512 anchor): "(SMP path)" mislabels the branch. Lines 93–113 of
  `lib/percpu_counter.c` are under `#ifdef CONFIG_HAVE_CMPXCHG_LOCAL` (guard at 87, `#else` variant at 114/120); the
  file has no CONFIG_SMP gate. The SMP/non-SMP split is in `include/linux/percpu_counter.h`, which is why S513's
  "(SMP)" is right and S512's qualifier is not.
- **F5 · LOW** — `corpus/SOURCES.md:290` (S511 scope): "at v7.2 (the host kernel line)" overreaches. The host reports
  `7.2.11-arch1-1`; the pinned copy is upstream tag v7.2 (7.2.0). Nothing in the row establishes that the host
  build's `mm_init.c` is identical, so the parenthetical asserts an equivalence the row does not carry.
- **F6 · LOW** — `corpus/SOURCES.md:344` (round-53 search-log note): two bounded searches (C1 and C2) are merged into one
  prose note, where the contract's shape asks "one prose note per bounded search" and every earlier round records one
  question per note. Content fields are complete; only the shape deviates.
- **F7 · LOW** — `corpus/SOURCES.md:344`: the note says "located quotes in `corpus/lessons/round-53.md` Gate", a file that
  does not exist and never existed in this lane's history. Rule 1's Gate records for the twelve new rows (URL, access
  date, ≤25-word quote with its location grounding `teaches`) are therefore still owed, pending the same landing as
  the first finding.
- **F8 · LOW** — `corpus/SOURCES.md:284` (S505 `teaches`): names only the uffd-wp helper removal, but the v7.3 edit also
  rewrites two `memdesc_section(cur_page->flags)` sites to `memdesc_section(&cur_page->flags)`
  (`mm_inline.h.v7.2:653,663` → `mm_inline.h.v7.3:600,610`). The "unchanged `folio_is_file_lru`" half of the cell is
  correct.
- **F9 · LOW** — `corpus/SOURCES.md:282` (S503 `teaches`): the enumeration "an include, const nodemask parameters and
  printk units" omits the added `(unsigned long)` cast at `show_mem.c.v7.3:350` and the `local_pcp` unit change.
- **F10 · LOW** — `corpus/knowledge/kernel-v7.3-recheck-r53.md:27-31` with `corpus/SOURCES.md:286` (S507 `teaches`): the
  change-count label undercounts diffs in which added lines begin with `-`. The entry states its command
  (`grep -c '^[-+][^-+]'`), which reproduces 64 for `vm.rst`, but the same file's diff is 80 added + 3 removed = 83
  lines, and the 19 lines the filter drops are exactly the sysctl index bullets — including the added
  `panic_on_unrecoverable_memory_failure` index line that S507's `teaches` cell cites. Reproducible, but "changed
  lines" reads larger than it is.
- **F11 · LOW** — `corpus/SOURCES.md:286` (S507 anchor): the anchor pins five sysctl sections (82-109, 823, 834, 859,
  1106-1116) but not the `panic_on_unrecoverable_memory_failure` section (926-1004) that the same row's `teaches`
  cell cites and that the new lead at `corpus/SOURCES.md:351` depends on. A reader following only the anchor cannot
  reach that section; the anchor contract asks for the exact location of what the row teaches.
- **F12 · LOW** — `corpus/SOURCES.md:281` (S502 scope): scope says "for the v7.3 recheck of the round-51 MemAvailable
  claims", while the same row's anchor also pins CommitLimit 1221 and Committed_AS 1239, which no ledger row citing
  S502 uses (the round-52 doc claims route through S506/S507). Either widen the scope or drop the unused line refs.
- **F13 · LOW** — `corpus/SOURCES.md:281-292`: anchor sha256 cells are truncated to 12 hex characters, whereas S490–S501
  carry full 64-character pins and the counter's frozen table carries full digests. Every prefix I checked matches,
  so this is a convention deviation, not a wrong value.
