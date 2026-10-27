# Mo53ScribeGate — Gate-block draft for rows S502–S513 (round 53, wave w1)

Seat: scribe/gate drafter. Lane root `/home/vgpnk/Projects/shokunin/mori-shokunin`, working tree at
`95cf78eef71979f9b740ef6bc3c5299b6beff86e` (data `2a4213bf`, freeze `f4da3fd4`). Scratch
`/fast/scratch/hyaku/mori-r53/Mo53ScribeGate/` (created, used, removed at the end of this seat). No file outside my
own report was written; no git/jj mutation was run.

## Behavior

1. Read the frozen contract (`/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-53/contract.md`) and the
   house Gate shape in `corpus/lessons/round-52.md` §Gate.
2. Read the twelve SOURCES rows S502–S513 and the S499 used-by change from the data commit diff
   (`git diff f4da3fd4 2a4213bf -- corpus/SOURCES.md`).
3. Hashed all twelve copies in `corpus/evidence/sources-r53/` and compared them with the freeze pins
   (`evidence/freeze-sha256.txt:22-33`) and with the 12-hex prefixes quoted in the SOURCES rows.
4. Selected one quote per row (≤ 25 words) and verified each by substring test on the committed copy — pasted
   below. Derived the located line span from the same substring position.
5. Fetched both reject candidates live (raw.githubusercontent.com v7.3 path, and
   `https://www.kernel.org/doc/html/latest/admin-guide/sysctl/vm.html`) and recorded status/bytes/sha256.
6. Resolved tags v7.2/v7.3 read-only (`git ls-remote`) to check the tag→commit figures the rows cite.
7. Spot-checked the SOURCES anchor line numbers against the copies.

## Gates (observed)

### 1. Copies, pins, prefixes

`sha256sum` of the twelve copies (all in `corpus/evidence/sources-r53/`) — full digests:

```
d6c5807421a69eac21efd737b39d099c711b3132b371dc34986d181746e3deda  meminfo.c.v7.3
ed691b24afbc0dc45090e149d115d707af0c5f7369a10b7722d491075f26a754  mm_init.c.v7.2
277e99e23ecc1b5babfdf041e7e7e3f9d280113b3b0a9f7e8340c0e13d7b391b  mm_inline.h.v7.3
d7bf787c910d9a7cbabee3a50c512ce3aad78d63659b0c968adca16b5916b058  mman.h.v7.3
8e51fb1c10fee6943c9edc26b72952137b4098b00cc050ea1e6ade6e27197feb  mmap.c.v7.3
767ab88153c4494e54fcf2db4e5bd01921d6bd8350f1596ada508cb5e4b4927f  overcommit-accounting.rst.v7.3
2c26e67751f939dfb21ff6221884280ae84a2a94a54de4468fb9dc8746130d6d  percpu_counter.c.v7.2
4a107bc381b3b5425b8ff441f7487d97ba6883dc6f5b426c4bd361ad7cbef896  percpu_counter.h.v7.2
bc178ff511e05c1b5e0c2413feb18223edcaeb2797ce499b714b98120cabf3c8  proc.rst.v7.3
c50205bc19974566d7bfe1c161f253cf71321c06ecc1327abb2a775be8a0de71  show_mem.c.v7.3
4dfcce2b8fa8f18c350565950a10248b3590e3d3c0c9335fef6d47daa7a9e1f2  util.c.v7.3
f81feb3dfca5f054cf8b76c71d7a4525a88d629d3ea8239743996b9d87bb391b  vm.rst.v7.3
```

`freeze-sha256.txt:22-33` lists those same twelve paths; comparing pin to working-tree bytes per path printed
`OK` twelve times (`awk`/`sha256sum` loop, exit 0). Each digest above also extends the 12-hex prefix written in
its SOURCES row's locator cell. `git status --porcelain corpus/evidence/sources-r53 corpus/SOURCES.md` → empty
(no drift after the data commit).

### 2. Quote substring tests (pasted)

`quotecheck2.py` (run from my scratch with `TMPDIR` set there; the copy dir is absolute):

```python
import hashlib, pathlib, re
D = pathlib.Path("/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/evidence/sources-r53")
R = [
 ("S502","proc.rst.v7.3","An estimate of how much memory is available for starting new applications, without swapping."),
 ("S503","show_mem.c.v7.3","Estimate the amount of memory available for userspace allocations, without causing swapping or OOM."),
 ("S504","meminfo.c.v7.3",'show_val_kb(m, "Committed_AS:   ", committed);'),
 ("S505","mm_inline.h.v7.3","0 if @folio is a normal anonymous folio, a tmpfs folio or otherwise ram or swap backed folio."),
 ("S506","overcommit-accounting.rst.v7.3","The total address space commit for the system is not permitted to exceed swap + a configurable amount (default is 50%) of physical RAM."),
 ("S507","vm.rst.v7.3","When this flag is 0, the kernel compares the userspace memory request size against total memory plus swap and rejects obvious overcommits."),
 ("S508","util.c.v7.3","if (percpu_counter_read_positive(&vm_committed_as) < allowed) return 0;"),
 ("S509","mman.h.v7.3","static inline void vm_acct_memory(long pages) { percpu_counter_add_batch(&vm_committed_as, pages, vm_committed_as_batch); }"),
 ("S510","mmap.c.v7.3","if (flags & MAP_NORESERVE) { /* We honor MAP_NORESERVE if allowed to overcommit */ if (sysctl_overcommit_memory != OVERCOMMIT_NEVER) vma_flags_set(&vma_flags, VMA_NORESERVE_BIT);"),
 ("S511","mm_init.c.v7.2","For policy OVERCOMMIT_NEVER, set batch size to 0.4% of (total memory/#cpus), and lift it to 25% for other policies"),
 ("S512","percpu_counter.c.v7.2","if (unlikely(abs(count + amount) >= batch)) {"),
 ("S513","percpu_counter.h.v7.2","static inline s64 percpu_counter_read_positive(struct percpu_counter *fbc)"),
]
def norm(text):
    # drop leading comment decoration (" * ", " *") so mid-sentence comment breaks rejoin, then collapse whitespace
    stripped = "\n".join(re.sub(r"^[ \t]*\*[ \t]?", "", ln) for ln in text.split("\n"))
    return " ".join(stripped.split())
ok = 0
for sid, fn, q in R:
    p = D / fn
    raw = p.read_text()
    h = hashlib.sha256(p.read_bytes()).hexdigest()
    found = norm(q) in norm(raw)
    ok += found
    print(f"{sid:5s} {fn:30s} sha256={h[:12]} words={len(q.split()):2d} found={found} exact_bytes={q in raw}")
print(f"FOUND {ok}/{len(R)}")
```

Output (exit 0):

```
S502  proc.rst.v7.3                  sha256=bc178ff511e0 words=14 found=True exact_bytes=False
S503  show_mem.c.v7.3                sha256=c50205bc1997 words=14 found=True exact_bytes=False
S504  meminfo.c.v7.3                 sha256=d6c5807421a6 words= 4 found=True exact_bytes=True
S505  mm_inline.h.v7.3               sha256=277e99e23ecc words=18 found=True exact_bytes=False
S506  overcommit-accounting.rst.v7.3 sha256=767ab88153c4 words=24 found=True exact_bytes=False
S507  vm.rst.v7.3                    sha256=f81feb3dfca5 words=22 found=True exact_bytes=False
S508  util.c.v7.3                    sha256=4dfcce2b8fa8 words= 6 found=True exact_bytes=False
S509  mman.h.v7.3                    sha256=d7bf787c910d words=10 found=True exact_bytes=False
S510  mmap.c.v7.3                    sha256=8e51fb1c10fe words=20 found=True exact_bytes=False
S511  mm_init.c.v7.2                 sha256=ed691b24afbc words=19 found=True exact_bytes=False
S512  percpu_counter.c.v7.2          sha256=2c26e67751f9 words= 7 found=True exact_bytes=True
S513  percpu_counter.h.v7.2          sha256=4a107bc381b3 words= 6 found=True exact_bytes=True
FOUND 12/12
```

`found=True` for all twelve, every quote ≤ 25 words. `exact_bytes=True` marks the three quotes that are one
physical line; the other nine span a line break inside a C comment or a wrapped rst paragraph, so the test strips
leading ` * ` decoration and collapses whitespace before matching. A stricter whole-file exact-bytes test would
reject nine of twelve quotes that are word-for-word present — the normalisation is the honest fix, and it is
disclosed here rather than hidden.

Line spans from the same substring position (`spans.py`, same normalisation, mapping each normalised character
back to its source line; exit 0):

```
S502 :1128-1129   S503 :45-46    S504 :126      S505 :25-26    S506 :20-22    S507 :839-840
S508 :994-995     S509 :76-79    S510 :563-566  S511 :199-200  S512 :100      S513 :118
```

Cross-checked with `grep -n`/`sed -n` on the copies: `proc.rst.v7.3:1128`, `show_mem.c.v7.3:45`,
`meminfo.c.v7.3:126`, `mm_inline.h.v7.3:25`, `overcommit-accounting.rst.v7.3:20`, `vm.rst.v7.3:839`,
`util.c.v7.3:994`, `mman.h.v7.3:76`, `mmap.c.v7.3:563`, `mm_init.c.v7.2:199`, `percpu_counter.c.v7.2:100`,
`percpu_counter.h.v7.2:118`.

### 3. Anchor spot-check against the copies

Every line number the twelve SOURCES rows cite, printed from the committed copy (exit 0):

```
proc.rst.v7.3:1221 CommitLimit            proc.rst.v7.3:1239 Committed_AS
show_mem.c.v7.3:73  }                     meminfo.c.v7.3:34 static int meminfo_proc_show(struct seq_file *m, void *v)
mm_inline.h.v7.3:28 static inline int folio_is_file_lru(const struct folio *folio)
vm.rst.v7.3:82 admin_reserve_kbytes       vm.rst.v7.3:823 overcommit_kbytes   vm.rst.v7.3:834 overcommit_memory
vm.rst.v7.3:859 overcommit_ratio          vm.rst.v7.3:1106 user_reserve_kbytes  vm.rst.v7.3:1116 user_reserve_kbytes defaults to min(3% of the current process size, 128MB).
util.c.v7.3:904 unsigned long vm_commit_limit(void)   util.c.v7.3:916 }
util.c.v7.3:959 int __vm_enough_memory(const struct mm_struct *mm, long pages, int cap_sys_admin)
util.c.v7.3:1003 }                        mm_init.c.v7.2:226 static int __init mm_compute_batch_init(void)
mm_init.c.v7.2:233 __initcall(mm_compute_batch_init);
percpu_counter.c.v7.2:93 void percpu_counter_add_batch(struct percpu_counter *fbc, s64 amount, s32 batch)
percpu_counter.c.v7.2:113 }               percpu_counter.h.v7.2:126 }
```

### 4. Tag resolution and the reject-candidate fetches

```
$ git ls-remote --tags https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git v7.2 v7.3 'v7.3^{}' 'v7.2^{}'
237a1c39e8dfd3e1c6f1f023eea37a48ec04cc63	refs/tags/v7.2
8d3ae59288f1e7d58d76558a6ee96d533bc5019f	refs/tags/v7.2^{}
091b06388b117fefdcb63336ac09956a4914b961	refs/tags/v7.3
c03c1a14507dfaf8b856c2608f9ac216021fc222	refs/tags/v7.3^{}
rc=0
```

Both annotated-tag objects and both commits match what rows S502–S510/S511–S513 cite (v7.3 `091b06388b11` →
`c03c1a14507d`; v7.2 `237a1c39e8df` → `8d3ae59288f1`).

Reject candidate 1 — raw.githubusercontent.com at tag v7.3 (four probes, same session, 2026-10-26):

```
RAW_STATUS=200 BYTES=43965   https://raw.githubusercontent.com/torvalds/linux/v7.3/mm/util.c
  sha256(raw bytes) 4dfcce2b8fa8f18c350565950a10248b3590e3d3c0c9335fef6d47daa7a9e1f2  (== util.c.v7.3 copy)
Documentation/mm/overcommit-accounting.rst -> 200
mm/show_mem.c                              -> 200
include/linux/mman.h                       -> 429
```

Reject candidate 2 — kernel.org rendered docs (`latest`):

```
KORG_STATUS=200 BYTES=69002  https://www.kernel.org/doc/html/latest/admin-guide/sysctl/vm.html
sha256 423d043409bcf9914d72bce7de28516fd164b91a01413dd875c51423fbc42efa
served header: <p class="blurb">7.3.0</p>   <title>Documentation for /proc/sys/vm/ — The Linux Kernel  documentation</title>
"overcommit_memory" occurs 6 times; the S507 sentence ("rejects obvious overcommits") is present on the page
```

## Draft: `## Gate` block for the round-53 lesson (fenced; house shape of `corpus/lessons/round-52.md` §Gate)

```markdown
## Gate

### New SOURCES rows (each opened this round; rule 1)

Twelve rows, all opened 2026-10-26, appended after S501, 11 cells each, status `mined`, recheck `on-release`:
S502–S510 `used-by corpus/knowledge/kernel-v7.3-recheck-r53.md`, S511–S513 `used-by
corpus/knowledge/commit-runway-read-r53.md`. All twelve were copied into `corpus/evidence/sources-r53/` and pinned
by sha256 in `.ufo/waves/round-53/evidence/freeze-sha256.txt:22-33`; each working-tree byte sequence still equals
its pin at the data commit (twelve `OK`, `git status --porcelain corpus/evidence/sources-r53 corpus/SOURCES.md`
empty). `corpus/SOURCES.md` gains 15 lines and loses 0 between `f4da3fd4` and `2a4213bf` (`git diff --numstat` →
`15 1`): the twelve new rows, one replaced row (S499, below), one round-53 bounded-search paragraph and one
queued-candidate bullet. The nine v7.3 files were opened on git.kernel.org cgit; the three band files are at v7.2,
the host's kernel line.

| id | URL / locator | accessed | copy sha256 (full) | ≤25-word located quote | decision |
|---|---|---|---|---|---|
| S502 | https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/Documentation/filesystems/proc.rst?h=v7.3 — copy `proc.rst.v7.3` | 2026-10-26 | `bc178ff511e05c1b5e0c2413feb18223edcaeb2797ce499b714b98120cabf3c8` | "An estimate of how much memory is available for starting new applications, without swapping." (14 words, `:1128-1129`) | admit, mined, tier A docs |
| S503 | https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/mm/show_mem.c?h=v7.3 — copy `show_mem.c.v7.3` | 2026-10-26 | `c50205bc19974566d7bfe1c161f253cf71321c06ecc1327abb2a775be8a0de71` | "Estimate the amount of memory available for userspace allocations, without causing swapping or OOM." (14 words, `:45-46`) | admit, mined, tier A code |
| S504 | https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/fs/proc/meminfo.c?h=v7.3 — copy `meminfo.c.v7.3` | 2026-10-26 | `d6c5807421a69eac21efd737b39d099c711b3132b371dc34986d181746e3deda` | `show_val_kb(m, "Committed_AS:   ", committed);` (4 words, `:126`; CommitLimit one line above at `:125`) | admit, mined, tier A code |
| S505 | https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/include/linux/mm_inline.h?h=v7.3 — copy `mm_inline.h.v7.3` | 2026-10-26 | `277e99e23ecc1b5babfdf041e7e7e3f9d280113b3b0a9f7e8340c0e13d7b391b` | "0 if @folio is a normal anonymous folio, a tmpfs folio or otherwise ram or swap backed folio." (18 words, `:25-26`) | admit, mined, tier A code |
| S506 | https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/Documentation/mm/overcommit-accounting.rst?h=v7.3 — copy `overcommit-accounting.rst.v7.3` | 2026-10-26 | `767ab88153c4494e54fcf2db4e5bd01921d6bd8350f1596ada508cb5e4b4927f` | "The total address space commit for the system is not permitted to exceed swap + a configurable amount (default is 50%) of physical RAM." (24 words, `:20-22`) | admit, mined, tier A docs |
| S507 | https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/Documentation/admin-guide/sysctl/vm.rst?h=v7.3 — copy `vm.rst.v7.3` | 2026-10-26 | `f81feb3dfca5f054cf8b76c71d7a4525a88d629d3ea8239743996b9d87bb391b` | "When this flag is 0, the kernel compares the userspace memory request size against total memory plus swap and rejects obvious overcommits." (22 words, `:839-840`) | admit, mined, tier A docs |
| S508 | https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/mm/util.c?h=v7.3 — copy `util.c.v7.3` | 2026-10-26 | `4dfcce2b8fa8f18c350565950a10248b3590e3d3c0c9335fef6d47daa7a9e1f2` | `if (percpu_counter_read_positive(&vm_committed_as) < allowed) return 0;` (6 words, `:994-995`) | admit, mined, tier A code |
| S509 | https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/include/linux/mman.h?h=v7.3 — copy `mman.h.v7.3` | 2026-10-26 | `d7bf787c910d9a7cbabee3a50c512ce3aad78d63659b0c968adca16b5916b058` | "static inline void vm_acct_memory(long pages) { percpu_counter_add_batch(&vm_committed_as, pages, vm_committed_as_batch); }" (10 words, `:76-79`) | admit, mined, tier A code |
| S510 | https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/mm/mmap.c?h=v7.3 — copy `mmap.c.v7.3` | 2026-10-26 | `8e51fb1c10fee6943c9edc26b72952137b4098b00cc050ea1e6ade6e27197feb` | "if (flags & MAP_NORESERVE) { /* We honor MAP_NORESERVE if allowed to overcommit */ if (sysctl_overcommit_memory != OVERCOMMIT_NEVER) vma_flags_set(&vma_flags, VMA_NORESERVE_BIT);" (20 words, `:563-566`) | admit, mined, tier A code |
| S511 | https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/mm/mm_init.c?h=v7.2 — copy `mm_init.c.v7.2` | 2026-10-26 | `ed691b24afbc0dc45090e149d115d707af0c5f7369a10b7722d491075f26a754` | "For policy OVERCOMMIT_NEVER, set batch size to 0.4% of (total memory/#cpus), and lift it to 25% for other policies" (19 words, `:199-200`) | admit, mined, tier A code |
| S512 | https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/lib/percpu_counter.c?h=v7.2 — copy `percpu_counter.c.v7.2` | 2026-10-26 | `2c26e67751f939dfb21ff6221884280ae84a2a94a54de4468fb9dc8746130d6d` | `if (unlikely(abs(count + amount) >= batch)) {` (7 words, `:100`) | admit, mined, tier A code |
| S513 | https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/include/linux/percpu_counter.h?h=v7.2 — copy `percpu_counter.h.v7.2` | 2026-10-26 | `4a107bc381b3b5425b8ff441f7487d97ba6883dc6f5b426c4bd361ad7cbef896` | `static inline s64 percpu_counter_read_positive(struct percpu_counter *fbc)` (6 words, `:118`) | admit, mined, tier A code |
| — | https://raw.githubusercontent.com/torvalds/linux/v7.3/… (the same nine v7.3 paths) | 2026-10-26 | `mm/util.c` returned 43965 bytes, sha256 `4dfcce2b…9e1f2` (byte-identical to the S508 copy); `include/linux/mman.h` returned HTTP 429 in the same session | — | **reject**: the host throttles per path (three 200s and one 429 in one sitting, and the L1's opening fetches got 429), so a row opened there cannot claim a stable locator for the bytes it quotes; the cgit `plain/<path>?h=v7.3` endpoint serves the same bytes and answered for all nine. Flip: every cited v7.3 path answers 200 with sha256 equal to the frozen cgit copy on the day it is opened — then raw is admissible as a second locator for these rows, never as a new row |
| — | https://www.kernel.org/doc/html/latest/admin-guide/sysctl/vm.html (rendered docs, `latest`) | 2026-10-26 | HTTP 200, 69002 bytes, sha256 `423d0434…42efa`; the page renders `<p class="blurb">7.3.0</p>` | the page carries the S507 sentence today ("rejects obvious overcommits") | **reject**: `latest` moves with each release (it renders 7.3.0 today, not the v7.3 bytes the rows pin tomorrow after v7.4), so a quote located there proves nothing pinned; S507's raw tag copy carries the same text. Flip: a release-pinned rendered URL (`/doc/html/v7.3/…`) would be admissible as a second locator for S507, not as a new row |

Every quote above was located by substring test against the committed copy on 2026-10-26 (twelve of twelve found;
nine of them span a C-comment or rst line break, so the test strips leading ` * ` decoration and collapses
whitespace before matching, and the three single-line quotes also match byte for byte). The cited anchor line
numbers of all twelve rows print the named symbol on the named line in the committed copy. Tag resolution check
(`git ls-remote`): `refs/tags/v7.3` → `091b06388b11`, `^{}` → `c03c1a14507d`; `refs/tags/v7.2` → `237a1c39e8df`,
`^{}` → `8d3ae59288f1` — as the rows state.

### S499 used-by change (same commit, no other cell touched)

`corpus/knowledge/overcommit-commit-limit-r52.md` → `corpus/knowledge/overcommit-commit-limit-r52.md,
corpus/knowledge/commit-runway-read-r53.md` (`git diff f4da3fd4 2a4213bf -- corpus/SOURCES.md`, the one removal in
that diff). The round-52 entry's S499 row now names the round-53 band entry too, because the band entry's batch rule
rests on the same `mm/util.c` reading; the locator, anchor, quote, status, tier and recheck cells are unchanged.
```

## Out of scope for this seat

- I did not run `count-c1.py` or `count-c2.py`, did not score any claim, and did not touch the ledger rows,
  dispositions, votes, the tool, its fixtures, SKILL.md, SHONEN.md, SCORECARD.md, LOG.md, PROVINCE.md,
  `corpus/`, `tools/` or `considerthese/`.
- I did not verify that every one of the 46 ledger rows draws on S502–S510 (only that the ledger exists with 46
  rows and names S502–S506 in its `source:` lines, and that the band entry names S511–S513 in its `source:` lines
  and quotes S511 three times).
- I did not re-fetch the nine v7.3 cgit URLs in this seat (the copies' pin identity is what I checked); source
  re-opening is another seat's assignment.
- Nothing was installed; no pacman/uv/npx call; no tool upgrade was needed.

## Findings

- **MED — Gate reject reason for raw.githubusercontent.com must say "throttled per path", not "HTTP 429 on
  2026-10-26".** `contract.md` (C1 surface paragraph) and `corpus/SOURCES.md:344` (round-53 bounded-search
  paragraph) both state raw answered 429, and the data commit rested on that. My probe on the same date returned
  200 for `v7.3/mm/util.c` (43965 bytes, sha256 `4dfcce2b…9e1f2`, byte-identical to the S508 copy), 200 for
  `v7.3/Documentation/mm/overcommit-accounting.rst`, 200 for `v7.3/mm/show_mem.c`, and 429 for
  `v7.3/include/linux/mman.h`. Neither statement is false — the endpoint is intermittent — but a bare "answered
  429" reads as a host-wide outage and invites the wrong flip test. The draft above states the intermittency and
  keeps the flip condition on the bytes, not on the status alone. No data change needed; the L1 chooses whether to
  amend the sentence.
- **LOW — the reject decision does not reach the lane's older raw-hosted rows.** S497–S501 (and therefore today's
  S499) still cite `https://raw.githubusercontent.com/torvalds/linux/v7.2/…`, so a reader can see an admitted row
  on a host the Gate rejects. Those rows' evidence is the committed copy and its pin, so nothing is wrong today;
  the draft scopes the reject to "new rows opened this round" and to a second-locator role. `corpus/SOURCES.md`
  rows 274–278.
- **LOW — SOURCES locator cells carry only a 12-hex sha256 prefix.** Twelfth-row convention consistent with
  S497–S501 (`corpus/SOURCES.md:281-292`); all twelve prefixes extend to the full digests I recomputed, and the
  full digests live in `evidence/freeze-sha256.txt:22-33`. Recorded so the Gate text does not imply the row cell
  is the pin.
- **LOW — line-anchor drift risk in the Gate table.** Nine of twelve quotes span a line break, so the quoted span
  (`:1128-1129`, `:45-46`, `:25-26`, `:20-22`, `:839-840`, `:994-995`, `:76-79`, `:563-566`, `:199-200`) depends on
  the wrapping of the adopted copy, not on the kernel text. If a copy is ever re-fetched with different wrapping
  the quotes still match after normalisation but the spans move; the draft therefore names the copy file in the
  same cell as the URL.
- **LOW — the S507 rendered-docs reject contradicts one sentence of the round-52 lesson's precedent.** Round 52
  recorded the same `latest` page header as "The Linux Kernel 7.3.0"; today the same URL serves
  `<p class="blurb">7.3.0</p>` with the `<h1 class="logo">` text reading "The Linux Kernel" and the `<title>`
  carrying no version. Same conclusion (reject), different literal evidence; the draft quotes the bytes I saw, not
  round 52's wording. `corpus/lessons/round-52.md` §Gate last table row.
