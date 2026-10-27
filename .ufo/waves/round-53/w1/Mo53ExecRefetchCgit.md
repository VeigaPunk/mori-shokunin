# Mo53ExecRefetchCgit — independent cgit re-fetch of the twelve round-53 source copies

Seat: Mo53ExecRefetchCgit (round 53, wave w1). Assignment: re-fetch the twelve copies under
`corpus/evidence/sources-r53/` from git.kernel.org cgit and report HTTP status, bytes and sha256 against the
frozen pins in `.ufo/waves/round-53/count-c1.py` (`V73`) and `.ufo/waves/round-53/evidence/freeze-sha256.txt`;
then re-fetch the same nine paths at v7.2 and compare with the lane's committed v7.2 copies under
`corpus/evidence/sources-r51/` and `sources-r52/`. Nothing in the lane was changed; every number below is a
command plus its output.

Scratch: `/fast/scratch/hyaku/mori-r53/Mo53ExecRefetchCgit/` (`mkdir -p`, `TMPDIR` set to its `tmp/`; one
`git clone --no-checkout` of tag v7.3 plus a `git fetch --depth 1` of tag v7.2 into the same repo; removed at
exit). Lane HEAD during the run: `95cf78eef71979f9b740ef6bc3c5299b6beff86e` (data commit
`2a4213bf8da72f7cd78189baa5bb9be825dca1df`); `git status --porcelain` showed only the pre-existing untracked
wave artefacts (`.ufo/waves/round-53/evidence/selftests/`, `w1.ready`, `w1.ready.partial`, `w1/`), none of them
written by this seat. Disk guard before the runs: `scripts/hyaku/disk-guard.sh check` → `ok root=/tmp use=4%
soft=70%`, `ok root=/var/tmp use=34% soft=70%`, `ok root=/fast/scratch/hyaku use=24% soft=70%`, exit 0.

No tool was installed or upgraded for this seat.

## 1. Re-fetch of the nine v7.3 copies against the cgit pins in `count-c1.py` `V73`

URL form is the one the counter pins: `https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/<path>?h=v7.3`.
Every request returned HTTP 200 with `size_download` equal to the file size on disk; each file was then
compared byte for byte (`cmp`) with the lane's committed copy at the data commit.

| kernel path | committed copy | HTTP | bytes | sha256 (my fetch = counter pin = committed) | cmp |
|---|---|---|---|---|---|
| `Documentation/filesystems/proc.rst` | `proc.rst.v7.3` | 200 | 107605 | `bc178ff511e05c1b5e0c2413feb18223edcaeb2797ce499b714b98120cabf3c8` | identical |
| `mm/show_mem.c` | `show_mem.c.v7.3` | 200 | 13281 | `c50205bc19974566d7bfe1c161f253cf71321c06ecc1327abb2a775be8a0de71` | identical |
| `fs/proc/meminfo.c` | `meminfo.c.v7.3` | 200 | 6046 | `d6c5807421a69eac21efd737b39d099c711b3132b371dc34986d181746e3deda` | identical |
| `include/linux/mm_inline.h` | `mm_inline.h.v7.3` | 200 | 17667 | `277e99e23ecc1b5babfdf041e7e7e3f9d280113b3b0a9f7e8340c0e13d7b391b` | identical |
| `Documentation/mm/overcommit-accounting.rst` | `overcommit-accounting.rst.v7.3` | 200 | 2647 | `767ab88153c4494e54fcf2db4e5bd01921d6bd8350f1596ada508cb5e4b4927f` | identical |
| `Documentation/admin-guide/sysctl/vm.rst` | `vm.rst.v7.3` | 200 | 45908 | `f81feb3dfca5f054cf8b76c71d7a4525a88d629d3ea8239743996b9d87bb391b` | identical |
| `mm/util.c` | `util.c.v7.3` | 200 | 43965 | `4dfcce2b8fa8f18c350565950a10248b3590e3d3c0c9335fef6d47daa7a9e1f2` | identical |
| `include/linux/mman.h` | `mman.h.v7.3` | 200 | 4265 | `d7bf787c910d9a7cbabee3a50c512ce3aad78d63659b0c968adca16b5916b058` | identical |
| `mm/mmap.c` | `mmap.c.v7.3` | 200 | 51299 | `8e51fb1c10fee6943c9edc26b72952137b4098b00cc050ea1e6ade6e27197feb` | identical |

All nine `V73` pins match my fetch, and all nine URLs in the counter equal the URL form I requested
(asserted for every entry: `url.endswith(path + "?h=v7.3")`). `pins=ok` in `c1-at-data.txt` is reproducible from
independent bytes.

## 2. Re-fetch of the three v7.2 copies (C2's band sources) against `freeze-sha256.txt`

These are `?h=v7.2` requests for `mm/mm_init.c`, `lib/percpu_counter.c`, `include/linux/percpu_counter.h`. They
are **not** in `count-c1.py`'s `V73` dict (that dict is the nine v7.3 copies); their pins live only in
`evidence/freeze-sha256.txt`.

| kernel path | committed copy | HTTP | bytes | sha256 (= freeze pin = committed) | cmp |
|---|---|---|---|---|---|
| `mm/mm_init.c` | `mm_init.c.v7.2` | 200 | 78178 | `ed691b24afbc0dc45090e149d115d707af0c5f7369a10b7722d491075f26a754` | identical |
| `lib/percpu_counter.c` | `percpu_counter.c.v7.2` | 200 | 10932 | `2c26e67751f939dfb21ff6221884280ae84a2a94a54de4468fb9dc8746130d6d` | identical |
| `include/linux/percpu_counter.h` | `percpu_counter.h.v7.2` | 200 | 6977 | `4a107bc381b3b5425b8ff441f7487d97ba6883dc6f5b426c4bd361ad7cbef896` | identical |

All twelve `sources-r53/` copies listed in `freeze-sha256.txt` verify against the working tree (loop over the
file's `sources-r53/` lines → 12 × `MATCH`), and all twelve verify at the data commit
(`git show 2a4213bf…:corpus/evidence/sources-r53/<copy>` → same twelve sha256 values).

## 3. The tag is really what cgit served (not just "bytes are what the L1 fetched")

The contract's named limit says the pins "prove the bytes are what the L1 fetched from cgit, not that cgit
served the tag — wave seats re-fetch independently". Three independent readings were taken (tag refs, tag-tree
blob ids over the git protocol, and a second HTTP origin) and all agree.

**3a. Tag resolution (`git ls-remote`, 2026-10-26, exit 0).**

```
237a1c39e8dfd3e1c6f1f023eea37a48ec04cc63	refs/tags/v7.2
8d3ae59288f1e7d58d76558a6ee96d533bc5019f	refs/tags/v7.2^{}
091b06388b117fefdcb63336ac09956a4914b961	refs/tags/v7.3
c03c1a14507dfaf8b856c2608f9ac216021fc222	refs/tags/v7.3^{}
```

`v7.3^{}` = `c03c1a14507dfaf8b856c2608f9ac216021fc222`, the commit the contract and `evidence/sweeps.txt`
name. The rows S502–S510 also cite the annotated tag object `091b06388b11`, which matches.

**3b. Blob-identity check over the git protocol (not cgit HTTP).** A `git clone --no-checkout --depth 1 --branch
v7.3 --single-branch` of the same repository in scratch (58 s; the server answered
`warning: filtering not recognized by server, ignoring`, so it is a full-object clone of one commit), then
`git fetch --depth 1 origin refs/tags/v7.2:refs/tags/v7.2`. For each fetched file I computed
`git hash-object` on **my cgit bytes** and compared it with `git rev-parse <tag>^{}:<path>`, i.e. the blob id in
the tag's own tree:

| tag | paths checked | result |
|---|---|---|
| v7.3 | all nine | 9/9 `MATCH` |
| v7.2 | the same nine | 9/9 `MATCH` |
| v7.2 | mm_init.c, percpu_counter.c, percpu_counter.h | 3/3 `MATCH` |

Example (mm/mmap.c): tree blob at `v7.3^{}` = `4bf26b0f1e6e36dc089cfa8abd90b015a943fd77` = `git hash-object` of
my cgit fetch. So the twelve copies are the exact blobs of the named tag trees, not merely self-consistent
copies of one HTTP fetch.

**3c. cgit honours `?h=` (controls).** A bogus tag answers HTTP 404 with cgit's error page
(`?h=v9.9-nonexistent` → 404, 2956 bytes of HTML), and `?h=v7.1` returns v7.1's bytes (`mm/show_mem.c` v7.1
sha256 `dba76b26…`, equal to v7.2's — that file did not change between those two tags). Omitting `?h=`
(serving HEAD) returns the v7.3 bytes (`c50205bc…`). So the query parameter selects the tag and does not fall
through to a cached default.

**3d. Second origin (raw.githubusercontent.com).** The contract recorded HTTP 429 on 2026-10-26; that is
intermittent, not structural. The first request this seat made got `429: Too Many Requests` (199-byte body), and
later requests in the same run returned 200 for some paths and 429 for others. With bounded retry (≤ 10
attempts, exponential backoff) all eighteen requests — the nine paths at both tags — returned HTTP 200 from
`https://raw.githubusercontent.com/torvalds/linux/<tag>/<path>`, and **every one was byte-identical to the cgit
fetch and to the lane's committed copy** (`cmp`: `raw_vs_cgit identical=18 differ_or_missing=0`;
`raw_vs_lane identical=18 differ=0`). Retry counts: most paths succeeded on attempt 1; `mm_inline.h` v7.3 and
`sysctl/vm.rst`/`mman.h` v7.3 needed 2–3 attempts.

| path | raw.github sha256 (first 16) | cgit sha256 (first 16) | bytes |
|---|---|---|---|
| proc.rst v7.3 | `bc178ff511e05c1b` | `bc178ff511e05c1b` | 107605 |
| show_mem.c v7.3 | `c50205bc19974566` | `c50205bc19974566` | 13281 |
| meminfo.c v7.3 | `d6c5807421a69eac` | `d6c5807421a69eac` | 6046 |
| mm_inline.h v7.3 | `277e99e23ecc1b5b` | `277e99e23ecc1b5b` | 17667 |
| overcommit-accounting.rst v7.3 | `767ab88153c4494e` | `767ab88153c4494e` | 2647 |
| vm.rst v7.3 | `f81feb3dfca5f054` | `f81feb3dfca5f054` | 45908 |
| util.c v7.3 | `4dfcce2b8fa8f18c` | `4dfcce2b8fa8f18c` | 43965 |
| mman.h v7.3 | `d7bf787c910d9a7c` | `d7bf787c910d9a7c` | 4265 |
| mmap.c v7.3 | `8e51fb1c10fee694` | `8e51fb1c10fee694` | 51299 |
| proc.rst v7.2 | `e760f716f8278dee` | `e760f716f8278dee` | 107560 |
| show_mem.c v7.2 | `dba76b263bbdf933` | `dba76b263bbdf933` | 13204 |
| meminfo.c v7.2 | `d6c5807421a69eac` | `d6c5807421a69eac` | 6046 |
| mm_inline.h v7.2 | `2d4accbbc1ec139b` | `2d4accbbc1ec139b` | 19417 |
| overcommit-accounting.rst v7.2 | `767ab88153c4494e` | `767ab88153c4494e` | 2647 |
| vm.rst v7.2 | `bf8ca0265fefc019` | `bf8ca0265fefc019` | 42424 |
| util.c v7.2 | `e702754c45bd7bd6` | `e702754c45bd7bd6` | 43913 |
| mman.h v7.2 | `d7bf787c910d9a7c` | `d7bf787c910d9a7c` | 4265 |
| mmap.c v7.2 | `449b858385c7ece0` | `449b858385c7ece0` | 51223 |

Two origins (GitHub mirror over HTTPS, kernel.org git protocol) plus the tag-tree blob ids in §3b now agree on
all twelve copies, so the "cgit served the tag" arm is closed for both tags, not just asserted.

## 4. The nine paths at v7.2 vs the lane's committed v7.2 copies (`sources-r51/`, `sources-r52/`)

Same bytes, all nine. The lane's committed copies were themselves fetched from `raw.githubusercontent.com`
(S492–S501), so this comparison is cgit against raw.githubusercontent for the same tag — and that origin was
also re-requested directly this run (§3d), giving the same bytes for all nine.

| path | fetched v7.2 sha256 (= committed) | lane copy | cmp |
|---|---|---|---|
| `Documentation/filesystems/proc.rst` | `e760f716f8278deefab17a63739033cadc7faee93663c49e76455afaaf40d126` | `sources-r51/proc.rst.v7.2` | identical |
| `mm/show_mem.c` | `dba76b263bbdf93323a277a29c9281a892ff3fb35ddd6f0ddaf9ba1acb5b02f5` | `sources-r51/show_mem.c.v7.2` | identical |
| `fs/proc/meminfo.c` | `d6c5807421a69eac21efd737b39d099c711b3132b371dc34986d181746e3deda` | `sources-r51/meminfo.c.v7.2` | identical |
| `include/linux/mm_inline.h` | `2d4accbbc1ec139bfe11a356d4d17a55a2543769f3e10057a8a8584429c45ef6` | `sources-r51/mm_inline.h.v7.2` | identical |
| `Documentation/mm/overcommit-accounting.rst` | `767ab88153c4494e54fcf2db4e5bd01921d6bd8350f1596ada508cb5e4b4927f` | `sources-r52/overcommit-accounting.rst.v7.2` | identical |
| `Documentation/admin-guide/sysctl/vm.rst` | `bf8ca0265fefc019250697b6ee47a0679709b2ee45f4d1893b3dfd95c1f8c1ce` | `sources-r52/vm.rst.v7.2` | identical |
| `mm/util.c` | `e702754c45bd7bd69e5da22a6505c9c1016eaafe6e883b746cc3cdbd413ebe7c` | `sources-r52/util.c.v7.2` | identical |
| `include/linux/mman.h` | `d7bf787c910d9a7cbabee3a50c512ce3aad78d63659b0c968adca16b5916b058` | `sources-r52/mman.h.v7.2` | identical |
| `mm/mmap.c` | `449b858385c7ece0ff88a8b41893efadb70a437fb8585a296c4ef0461a4c1545` | `sources-r52/mmap.c.v7.2` | identical |

Each of those sha256 values also equals the `sha256` prefix written in the SOURCES row that declares the copy
(S492–S501), checked row by row: 9/9 `MATCH`.

## 5. Independent re-derivation of the C1 ledger from my own bytes, not the lane's copies

The point of a re-fetch is to test the data through a path the L1 did not use. I re-derived both C1 arms from
my own fetched bytes: `scope()` and `parse_table()`/`one_quote()` were imported read-only from the frozen
`count-c1.py` (scope read at the entering tip `20edafa5`, as the counter does), and the v7.3 file bodies were
the ones I fetched.

```
ledger_table_found=True rows=46 scope=46
rows_scored=46 status_agree=46 status_disagree=0
dispositions={'holds': 46}
quote_ok=46 quote_bad=0
my derivation from my own bytes: held=44 absent=2 total=46
ledger status column: Counter({'held': 44, 'absent': 2})
```

Both `absent` rows are the two `mm/mmap.c` `MAP_NORESERVE` rows the contract predicted
(`0fbd62f51ce8`, `d7a1dc88dcb3`), and the ledger's v7.3 replacement quotes for them occur in my bytes.
This reproduces `status_ok=46 quote_ok=46 held=44 absent=2` of `evidence/c1-at-data.txt` without touching the
committed copies.

## 6. The ledger's own drift narrative checks out against my bytes

The ledger's `## What changed between v7.2 and v7.3 in the nine files` table is a factual claim about the two
tags, so it is checkable from the re-fetch. `diff -u` over my own pairs, counting `^[-+][^-+]` lines, reproduces
every number in that table exactly, and the narrative sentences are correct:

| path | ledger says | my diff count | narrative check |
|---|---|---|---|
| `proc.rst` | 3 changed lines, outside the meminfo definitions | 3 | both hunks are at v7.3 lines 516 and 611 (a repeated word, and a new `ur` userfaultfd flag row), well outside the meminfo section 1043–1240 |
| `show_mem.c` | 22 | 22 | `+#include "page_alloc.h"`, `const nodemask_t *` on three signatures, `%luKB`→`%lukB` (2), `local_pcp:%ukB`→`%lukB`, and three format/sign fixes (`K((unsigned long)this_cpu_read(...))`, `%ld`→`%lu` for pagecache, `%lu`→`%ld` for hwpoisoned); `si_mem_available` body byte-identical across tags (1204 bytes, equal) |
| `meminfo.c` | byte-identical | 0 | sha256 equal at both tags |
| `mm_inline.h` | 49, "removal of the uffd-wp pte helper; `folio_is_file_lru` untouched" | 49 | `uffd_wp` occurrences 3 → 0; `folio_is_file_lru` body identical |
| `overcommit-accounting.rst` | byte-identical | 0 | sha256 equal |
| `vm.rst` | 64, "a new `panic_on_unrecoverable_memory_failure` section and index line; a dropped `mm/swap.c` pointer" | 64 | `+- panic_on_unrecoverable_memory_failure` index line and the section at v7.3:926; `-files can be found in mm/swap.c.` present at v7.2:23 and absent at v7.3 |
| `util.c` | 14, "`vm_mmap_pgoff` and the shadow-stack helper …; `vm_commit_limit`, `__vm_enough_memory` untouched" | 14 | `vm_commit_limit` and `__vm_enough_memory` bodies identical across tags; edits are `EMPTY_VMA_FLAGS`, `vma_flags_t`/`VMA_SHADOW_STACK`, `vma_start_pgoff` |
| `mman.h` | byte-identical | 0 | sha256 equal |
| `mmap.c` | 190, "the `vm_flags_t` → `vma_flags_t` conversion, including the `MAP_NORESERVE` block" | 190 | `vm_flags \|= VM_NORESERVE` 3 → 0 occurrences; `VMA_NORESERVE_BIT` 1 → 5 |

The reading-rules row "v7.3 writes the `MAP_NORESERVE` decision with
`vma_flags_set(&vma_flags, VMA_NORESERVE_BIT)` … the two conditions are the same | `mmap.c.v7.3:563-571`" is
exact: v7.3:563 `if (flags & MAP_NORESERVE) {` through 571 `}`, with the two `vma_flags_set` calls at 566 and
570, structurally the same two conditions as v7.2:550–558.

## 7. The cited line numbers in rows S502–S513 are correct in my fetched bytes

Each SOURCES row states where its item sits. Spot-checked against my fetch (line number → text at that line):

- S502 `proc.rst.v7.3`: 1043 `meminfo`, 1127 `MemAvailable`, 1221 `CommitLimit`, 1239 `Committed_AS`.
- S503 `show_mem.c.v7.3`: 33 `long si_mem_available(void)`, 73 `}`.
- S504 `meminfo.c.v7.3`: 34 `static int meminfo_proc_show(...)`, 125 `CommitLimit:` line, 126 `Committed_AS:` line.
- S505 `mm_inline.h.v7.3`: 28 `static inline int folio_is_file_lru(...)`.
- S508 `util.c.v7.3`: 806 `overcommit_policy_handler`, 904 `vm_commit_limit(void)`, 916 `}`, 959
  `__vm_enough_memory(...)`, 1003 `}`.
- S509 `mman.h.v7.3`: 76 `vm_acct_memory`, 81 `vm_unacct_memory`.
- S510 `mmap.c.v7.3`: 563 `if (flags & MAP_NORESERVE) {`, 571 `}`, 1566 `init_user_reserve`, 1587
  `init_admin_reserve`.
- S511 `mm_init.c.v7.2`: 191 `void mm_compute_batch(int overcommit_policy)`, 210 `}`, 226
  `static int __init mm_compute_batch_init(void)`, 233 `__initcall(mm_compute_batch_init);`.
- S512 `percpu_counter.c.v7.2`: 93 `percpu_counter_add_batch(...)`, 113 `}`.
- S513 `percpu_counter.h.v7.2`: 118 `percpu_counter_read_positive(...)`, 126 `}`.

All twelve rows' `sha256` prefixes also match my fetch (`12/12 copies`; S502–S510 v7.3 prefixes plus S511–S513
v7.2 prefixes).

## 8. One verified cross-check on C2's kernel ground (not a refetch result, but it uses these bytes)

The C2 entry says the mode-2 batch rule is unchanged at v7.3, and the C2 band source is the three v7.2 files
above. From the same clone: `mm_compute_batch`'s body is byte-identical between `v7.2^{}` and `v7.3^{}`
(sha256 `77c05d84ac250ae2…` both tags), `vm_memory_committed` in `mm/util.c` is identical (it is
`percpu_counter_sum_positive(&vm_committed_as)`, i.e. the exact sum, exactly as the entry says), and
`lib/percpu_counter.c` / `include/linux/percpu_counter.h` sha256 are equal at both tags — only `mm/mm_init.c`
differs as a whole file (74 insertions/137 deletions, none inside `mm_compute_batch`). The five quoted S511–S513
sentences in the entry's table occur verbatim (whitespace collapsed) in my fetched v7.2 bytes.

Host context the entry states, read live (read-only): `MemTotal: 31721796 kB`, `SwapTotal: 31722876 kB`, present
CPUs `0-31` (32), `overcommit_memory` = `0`, page size 4096, `uname -r` = `7.2.11-arch1-1`. `CommitLimit:
47583772 kB`, `Committed_AS: 41617632 kB` at read time.

The entry also calls the v7.2 copies "the host's kernel line (7.2.11)". Checked against the actual stable tag
(`https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/plain/<path>?h=v7.2.11`, HTTP 200 each):

| path | v7.2.11 sha256 | v7.2 tag sha256 | verdict |
|---|---|---|---|
| `lib/percpu_counter.c` | `2c26e67751f939df…` | `2c26e67751f939df…` | same bytes |
| `include/linux/percpu_counter.h` | `4a107bc381b3b542…` | `4a107bc381b3b542…` | same bytes |
| `mm/mm_init.c` | `adc2758996768cd92ff765afbf1a859ca2986e1f38ae3cdd0f157477622a5aa3` (78458 B) | `ed691b24afbc0dc4…` (78178 B) | **differs**, 27 changed lines |

The 27 lines are all node/zone initialisation (`free_area_init_core_hotplug`, `node_spanned_pages`,
`per_cpu_nodestats` allocation failure). `diff … \| grep -c 'memsized_batch\|vm_committed_as_batch\|num_present_cpus'`
→ 0, and `mm_compute_batch` read out of the v7.2.11 copy is byte-for-byte the v7.2 function. So the band rule does
describe the host, but the *copy* is the tag's bytes, not 7.2.11's.

## 9. Vote-state observation at read time (read-only; not a score)

The one place where a RECHECK seat could legitimately diverge from the ledger is the two `absent` rows, whose
`disposition` is `holds` (the rule is unchanged, only its spelling). A seat reading "disposition" as "the quote
text changed" would write `changed` and, under the frozen vote arm, create a dissent that fails C1. At my read
(2026-10-26, all twelve `Mo53Fr01`–`Mo53Fr12` reports present) the state was:

```
voters=12 distinct hashes voted=46
word counts: {'holds': 138}
hashes with <2 voters: none
votes per voter: Fr01..Fr06 = 12 each; Fr07..Fr12 = 11 each
```

`grep -rn 'RECHECK [0-9a-f]\{12\} changed' Mo53Fr*.md` → no matches. Both `absent` rows carried three `holds`
votes each (`0fbd62f51ce8`: Fr07:115, Fr08:30, Fr09:239; `d7a1dc88dcb3`: Fr10:20, Fr11:65, Fr12:24). So the
semantic fork did not materialise, but it exists: the ledger's `holds` on a respelled quote is a reading the
votes, not the bytes, have to carry.

## 10. Named limits of this seat

- Byte identity cannot show that a later fetch of the same tag would return the same bytes forever; git tags
  are mutable in principle. The blob-id check in §3b ties today's bytes to the tag object
  `091b06388b11`/`c03c1a14507d`, which is the strongest available statement at this instant.
- §3d's raw.githubusercontent leg needed retries and reached 18/18 only because of backoff; a seat with a
  single-attempt budget would have measured a false "429 everywhere". The rate limit is per-request, not per-host
  state, and no conclusion here depends on a single attempt.
- My re-derivation in §5 shares the frozen `count-c1.py` parsing code with the counter (scope extraction, quote
  extraction, whitespace collapse). It tests the *bytes*, not the parser; a parser defect would be invisible to
  it. Independent parsers are other seats' work.
- I did not re-fetch `corpus/evidence/sources-r51/34e431b0.patch` (the 2014 commit patch, outside the twelve
  copies and outside C1's scope D) and did not test the S492–S501 v7.2 rows beyond their sha256 declarations.
- The host is `7.2.11`, so the v7.2 copies remain the host's own reading; nothing here re-scores the C1 or C2
  counters against the landed tip (that is the L1's call at the post-wave tip).

## Findings

- **LOW** — `corpus/knowledge/kernel-v7.3-recheck-r53.md` `## What changed` table: every line count (3, 22, 0,
  49, 0, 64, 14, 0, 190) and every narrative sentence reproduces exactly from independent bytes; no correction
  needed. Recorded because a wave seat checked a claim that the counter does not check (`count-c1.py` never
  diffs v7.2 against v7.3), so this arm rests on wave seats, not on the predicate.
- **LOW** — `.ufo/waves/round-53/count-c2.py`: the three v7.2 copies C2's band rests on
  (`sources-r53/mm_init.c.v7.2`, `percpu_counter.c.v7.2`, `percpu_counter.h.v7.2`) are pinned only in
  `evidence/freeze-sha256.txt`; no counter reads that file (`count-c1.py` pins only its nine `V73` copies, and
  `count-c2.py` reads no `corpus/` path at all — `grep -c 'evidence\|SOURCES' count-c2.py` = 0). Verified correct
  from cgit and from the tag tree this run, but the C2 predicate would pass unchanged if those three files were
  replaced. Named limit for the report, routed item for round 54.
- **LOW** — provenance wording in `.ufo/waves/round-53/evidence/sweeps.txt` / the contract: "raw.githubusercontent.com
  answered HTTP 429 on 2026-10-26" is a per-request observation, not a property of the host. This run got a 429 on
  its first request and then 200 on all eighteen retried requests, and both origins serve identical bytes (§3d).
  The cgit choice remains correct (tag-explicit, not rate-limited), but the recorded reason should read
  "rate-limited intermittently on 2026-10-26" so a later seat does not treat raw.githubusercontent as unavailable
  and so a single-attempt 429 is not mistaken for the host being down.
- **LOW** — `corpus/knowledge/commit-runway-read-r53.md` (boundary line, "v7.2 bytes, the host's kernel line
  (7.2.11)"): the copies are tag v7.2 bytes, but the host is 7.2.11 and `mm/mm_init.c` at stable v7.2.11 hashes
  `adc2758996768cd9…` (78458 B, 27 changed lines vs the tag) against the committed `ed691b24afbc0dc4…` (78178 B).
  Nothing in the band rule moves — `mm_compute_batch` is byte-identical at v7.2.11, and `lib/percpu_counter.c`
  and `include/linux/percpu_counter.h` are byte-identical between tag v7.2 and v7.2.11 — but the sentence
  conflates the tag with the host's stable line. Data-correctable wording (data, not predicate): say "tag v7.2
  bytes; the host's 7.2.11 line differs outside `mm_compute_batch`", or pin the copy to `?h=v7.2.11`.
- No defect found in the twelve copies, their pins, the tag anchors, the SOURCES sha256 declarations, or the
  ledger's derived statuses.

Report: .ufo/waves/round-53/w1/Mo53ExecRefetchCgit.md
