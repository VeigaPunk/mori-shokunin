# Mo53ExecRefetchGit — independent git channel for the C1 v7.3 pins

Seat: Mo53ExecRefetchGit (round 53, wave w1). Scope: re-fetch the Linux v7.3 bytes of S502–S510 over an
independent git channel and compare them with the lane's committed copies; check the tag/commit anchors.
Nothing was changed in the lane. Every claim below is a command + output reading.

## Method (independent channel)

The seat spec named `git init` + `git remote add origin https://github.com/torvalds/linux` +
`git fetch --depth 1 --filter=blob:none origin tag v7.3`. That was done in the seat scratch, one clone-equivalent
per seat, blob-filtered (never a full clone):

```
$ mkdir -p /fast/scratch/hyaku/mori-r53/Mo53ExecRefetchGit/tmp
$ cd /fast/scratch/hyaku/mori-r53/Mo53ExecRefetchGit && git init -q linux
$ cd .../linux && git remote add origin https://github.com/torvalds/linux
$ git fetch --depth 1 --filter=blob:none origin tag v7.3
 * [new tag]         v7.3       -> v7.3
```

Exit 0. The tree was never checked out; each path was read as a blob with `git show v7.3:<path>` into
`.../blobs/<path with / replaced by _>`.

The lane's own channel was cgit (`git.kernel.org .../plain/<path>?h=v7.3`). To separate "the tag's bytes" from
"what cgit served", I also fetched the same nine paths from cgit over HTTP into `.../cgit73/` and compared the
two channels against each other and against the lane's committed copies. The v7.2 side was fetched the same way
(`git fetch --depth 1 --filter=blob:none origin tag v7.2`, plus cgit for the two blobs GitHub rate-limited) and
compared against the lane's committed v7.2 copies in `corpus/evidence/sources-r51/` and `sources-r52/`.

Scratch: `/fast/scratch/hyaku/mori-r53/Mo53ExecRefetchGit/` (one repo, `linux/`, plus `blobs/`, `blobs72/`,
`cgit73/`, and three verification scripts). Removed before finishing. No file was written outside the scratch
and this report. `git status --porcelain` in the lane after the run shows only the pre-existing untracked
`.ufo/waves/round-53/` wave artefacts (4 entries: `evidence/selftests/`, `w1.ready`, `w1.ready.partial`, `w1/`),
none of them mine.

## Tag and commit anchors

```
$ git -C linux rev-parse v7.3
091b06388b117fefdcb63336ac09956a4914b961
$ git -C linux rev-parse v7.3^{commit}
c03c1a14507dfaf8b856c2608f9ac216021fc222
$ git -C linux cat-file -t v7.3
tag
$ git -C linux ls-remote origin refs/tags/v7.3 'refs/tags/v7.3^{}'
091b06388b117fefdcb63336ac09956a4914b961	refs/tags/v7.3
c03c1a14507dfaf8b856c2608f9ac216021fc222	refs/tags/v7.3^{}
```

- Tag object `091b06388b11…` and peeled commit `c03c1a14507dfaf8b856c2608f9ac216021fc222` match the anchors the
  SOURCES rows S502–S510 carry (`tag v7.3 (091b06388b11, commit c03c1a14507d)`) and the contract's
  `refs/tags/v7.3^{}` → `c03c1a14507d…`. **equal**.
- `v7.3` is an annotated tag object pointing at that commit — `git cat-file -t v7.3` prints `tag`.

## Per-path result: my independently fetched v7.3 blob vs the lane's committed copy

The comparison is `cmp` (byte-exact) plus sha256 of both sides.

| path | lane copy | sha256 (both sides) | result |
|---|---|---|---|
| Documentation/filesystems/proc.rst | proc.rst.v7.3 | bc178ff511e05c1b5e0c2413feb18223edcaeb2797ce499b714b98120cabf3c8 | **equal** |
| mm/show_mem.c | show_mem.c.v7.3 | c50205bc19974566d7bfe1c161f253cf71321c06ecc1327abb2a775be8a0de71 | **equal** |
| fs/proc/meminfo.c | meminfo.c.v7.3 | d6c5807421a69eac21efd737b39d099c711b3132b371dc34986d181746e3deda | **equal** |
| include/linux/mm_inline.h | mm_inline.h.v7.3 | 277e99e23ecc1b5babfdf041e7e7e3f9d280113b3b0a9f7e8340c0e13d7b391b | **equal** |
| Documentation/mm/overcommit-accounting.rst | overcommit-accounting.rst.v7.3 | 767ab88153c4494e54fcf2db4e5bd01921d6bd8350f1596ada508cb5e4b4927f | **equal** |
| Documentation/admin-guide/sysctl/vm.rst | vm.rst.v7.3 | f81feb3dfca5f054cf8b76c71d7a4525a88d629d3ea8239743996b9d87bb391b | **equal** |
| mm/util.c | util.c.v7.3 | 4dfcce2b8fa8f18c350565950a10248b3590e3d3c0c9335fef6d47daa7a9e1f2 | **equal** |
| include/linux/mman.h | mman.h.v7.3 | d7bf787c910d9a7cbabee3a50c512ce3aad78d63659b0c968adca16b5916b058 | **equal** |
| mm/mmap.c | mmap.c.v7.3 | 8e51fb1c10fee6943c9edc26b72952137b4098b00cc050ea1e6ade6e27197feb | **equal** |

9/9 equal, 0 differ. Each sha256 also equals the 12-hex prefix pinned in the SOURCES row's anchor cell
(S502 bc178ff511e0, S503 c50205bc1997, S504 d6c5807421a6, S505 277e99e23ecc, S506 767ab88153c4, S507 f81feb3dfca5,
S508 4dfcce2b8fa8, S509 d7bf787c910d, S510 8e51fb1c10fe) and the full sha256 pinned inside `count-c1.py`'s `V73`
table.

### Cross-channel: my git fetch vs cgit (the lane's channel)

All nine paths fetched from `https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/<path>?h=v7.3`
into `cgit73/` are byte-identical to my `git show v7.3:<path>` output (`cmp` silent on all nine). So the git
channel and the cgit channel agree, and both agree with the committed copies. The contract's named limit ("the
pins prove the bytes are what the L1 fetched from cgit, not that cgit served the tag") is discharged for these nine
paths by an independent git-protocol fetch of the tag object and its tree entries.

## Independent re-derivation of the ledger's status and quote arms

I did not take the lane's committed copies as the input of the derivation. I re-derived each row's status from
the bytes I fetched, using the counter's own rule (whitespace-collapsed containment of the row's v7.2 quote in the
v7.3 copy), and checked the ledger's quote cell and status cell against that.

```
$ python3 rederive.py
rows=46 status_ok=46 quote_ok=46 held=44 absent=2 mismatches=0
```

The derivation, verbatim from my scratch script (the lane's committed copies appear only as the comparison
target, never as the input of the derivation):

```python
def fetch(path, tag="v7.3"):
    """Read a path's bytes straight out of the fetched git objects."""
    out = subprocess.run(["git", "-C", REPO, "show", "%s:%s" % (tag, path)],
                         capture_output=True, check=True).stdout
    return out.decode("utf-8", "surrogateescape")

...
        f, l = fetched[path], lane[path]
        # 1. derivation from MY bytes
        derived = "held" if ws(c["quote72"]) in f else "absent"
        if derived != l_status:
            mismatches.append((h, "status", "ledger=%s derived=%s" % (l_status, derived)))
        else:
            status_ok += 1
        # 2. quote cell occurs in MY bytes
        if l_quote not in f:
            mismatches.append((h, "quote-not-in-my-bytes", l_quote[:70]))
            continue
        # 3. quote cell must equal the v7.2 quote when held
        if derived == "held" and l_quote != ws(c["quote72"]):
            mismatches.append((h, "held-quote-not-equal-v72", l_quote[:70]))
            continue
        # 4. my bytes == lane bytes (whitespace-collapsed)
        if f != l:
            mismatches.append((h, "my-bytes-differ-from-lane", path))
            continue
        quote_ok += 1
```

The four checks per row, all against my bytes: derived status == ledger status cell; ledger quote cell occurs in
my v7.3 bytes; for `held` rows the quote cell equals the v7.2 quote; and my bytes == lane bytes
(whitespace-collapsed) for that path.

The two rows whose v7.2 quote does not occur in my v7.3 bytes are exactly the two the ledger marks `absent`:

```
0fbd62f51ce8  mm/mmap.c   (MAP_NORESERVE, ordinary mappings)
d7a1dc88dcb3  mm/mmap.c   (hugetlb strict-overcommit carve-out)
```

In my v7.3 `mm/mmap.c` the flag is now written `vma_flags_set(&vma_flags, VMA_NORESERVE_BIT);` at lines 537, 566
and 570, against `vm_flags |= VM_NORESERVE;` at lines 527, 553, 557 in my v7.2 copy — the same two conditions, respelled.
The ledger's v7.3 quote for each `absent` row is present in my bytes:

```
563: 	if (flags & MAP_NORESERVE) {
564: 		/* We honor MAP_NORESERVE if allowed to overcommit */
565: 		if (sysctl_overcommit_memory != OVERCOMMIT_NEVER)
566: 			vma_flags_set(&vma_flags, VMA_NORESERVE_BIT);
567:
568: 		/* hugetlb applies strict overcommit unless MAP_NORESERVE */
569: 		if (file && is_file_hugepages(file))
570: 			vma_flags_set(&vma_flags, VMA_NORESERVE_BIT);
571: 	}
```

(the ledger's `mmap.c.v7.3:563-571` pointer names this block; line 563 is `if (flags & MAP_NORESERVE) {`).

Also checked against my bytes: all 46 v7.2 quotes occur in my **v7.2** copies (46/46), so the scope's quote side
is anchored on the same bytes the round-51/52 entries cite.

## Claim-hash mapping and row attribution

`verify_hash.py` re-derives the frozen scope D from the lane's own entering-tip read
(`git show 20edafa5…:corpus/knowledge/{memavailable-estimate-r51.md,overcommit-commit-limit-r52.md}` plus
`corpus/SOURCES.md` at the same tip), recomputes `sha256(ws(claim))[:12]` and compares with the claims file and
the ledger:

```
scope_D_size=46
claims_file_rows=46 scope_mismatches=0
ledger_rows=46 sources_problems=0
dispositions: Counter({'holds': 46})
statuses: Counter({'held': 44, 'absent': 2})
```

Zero mismatches on hash, entry, path, quote, claim text and SOURCES-row attribution. Each ledger source cell names
a SOURCES row at the data commit whose URL is the frozen cgit v7.3 URL of that path, whose anchor names both
`091b06388b11` and `c03c1a14507d`, whose tier is A, whose opened date is 2026-10-26, whose status is `mined`,
whose recheck is `on-release`, and whose used-by names the recheck entry. SOURCES rows S502–S510 do not exist at
the entering tip (they land with the data commit) — the scope D derivation must therefore read the entering tip
while the ledger's source-cell arm reads the data commit; using one revision for both is a parse error I hit and
corrected, not a lane defect.

## The ledger's v7.2 → v7.3 change table, recomputed from my own bytes

The ledger's `## What changed between v7.2 and v7.3 in the nine files` table states a changed-line count per file.
Recomputed as `diff -u <my v7.2 copy> <my v7.3 copy> | grep -c '^[-+][^-+]'`:

| file | ledger count | my count | result |
|---|---|---|---|
| Documentation/filesystems/proc.rst | 3 | 3 | equal |
| mm/show_mem.c | 22 | 22 | equal |
| include/linux/mm_inline.h | 49 | 49 | equal |
| Documentation/admin-guide/sysctl/vm.rst | 64 | 64 | equal |
| mm/util.c | 14 | 14 | equal |
| mm/mmap.c | 190 | 190 | equal |

And the three files the ledger calls byte-identical between v7.2 and v7.3 (`fs/proc/meminfo.c`,
`Documentation/mm/overcommit-accounting.rst`, `include/linux/mman.h`) are byte-identical in my own fetch (`cmp`
silent). All nine lane v7.2 copies (`sources-r51/proc.rst.v7.2`, `show_mem.c.v7.2`, `meminfo.c.v7.2`,
`mm_inline.h.v7.2`; `sources-r52/overcommit-accounting.rst.v7.2`, `vm.rst.v7.2`, `util.c.v7.2`, `mman.h.v7.2`,
`mmap.c.v7.2`) are byte-identical to my independently fetched v7.2 blobs.

The prose descriptions in that table also check out against my diffs: proc.rst changed lines are a typo fix
("any page page") and a new `ur` userfaultfd line, both outside the meminfo field definitions (which start at
line 1043 in my copy); show_mem.c changes are the `page_alloc.h` include, `const nodemask_t *` parameters and
`%luKB` → `%lukB` printk units, and `si_mem_available` (lines 33–73) is untouched; mm_inline.h's change is the
removal of the uffd-wp pte helper, with `folio_is_file_lru` (line 28) untouched; vm.rst gains the
`panic_on_unrecoverable_memory_failure` section plus its index line and drops the `mm/swap.c` pointer; util.c's
changes are `vm_mmap_pgoff` and the shadow-stack helper (`vm_flags_t` → `vma_flags_t`), with `vm_commit_limit`
(lines 904–916) and `__vm_enough_memory` (lines 959–1003) untouched; mmap.c carries the `vm_flags_t` →
`vma_flags_t` conversion including the MAP_NORESERVE block.

## S511–S513 (the C2 band's v7.2 sources), same channel

Not in my seat's scope, but the same fetch covers them, so the observation is recorded: the lane's
`mm_init.c.v7.2`, `percpu_counter.c.v7.2` and `percpu_counter.h.v7.2` copies are byte-identical to my
independently fetched v7.2 blobs, and their SOURCES pins (ed691b24afbc, 2c26e67751f9, 4a107bc381b3) match. The
batch rule the C2 band relies on is visible in my `mm/mm_init.c` bytes (lines 191–210):

```
195: 	s32 batch = max_t(s32, nr*2, 32);
199: 	 * For policy OVERCOMMIT_NEVER, set batch size to 0.4% of
200: 	 * (total memory/#cpus), and lift it to 25% for other policies
204: 	if (overcommit_policy == OVERCOMMIT_NEVER)
205: 		memsized_batch = min_t(u64, ram_pages/nr/256, INT_MAX);
209: 	vm_committed_as_batch = max_t(s32, memsized_batch, batch);
```

i.e. `batch = max(min(ram_pages/cpus/256, INT_MAX), max(2*cpus, 32))` for mode 2 — the rule the counter's REF
function encodes. `percpu_counter_add_batch` is at lib/percpu_counter.c lines 93–113 (SMP path) as the S512 anchor
says; `percpu_counter_read_positive` at include/linux/percpu_counter.h lines 118–126 (SMP) as S513 says.

## Counter cross-read (read-only, informational)

```
$ cd /home/vgpnk/Projects/shokunin/mori-shokunin
$ python3 .ufo/waves/round-53/count-c1.py 2a4213bf8da72f7cd78189baa5bb9be825dca1df
C1=unmet scope=46 rows=46 matched=46 status_ok=46 quote_ok=46 source_rows=ok pins=ok provenance=ok held=44 absent=2 holds=46 changed=0 voted=0 dissent=0 rev=2a4213bf8da72f7cd78189baa5bb9be825dca1df failed=votes
exit 1
```

The counter's own numbers agree with my independent derivation on every arm I can check (scope 46, status_ok 46,
quote_ok 46, held 44, absent 2, pins ok, source_rows ok, provenance ok). It reads `voted=0 failed=votes` because no
voter report existed in `.ufo/waves/round-53/w1/` at that moment — that is the expected pre-vote reading of
the data commit, not a defect. The vote arm is not mine to score and I did not attempt it.

The live C2 tool, for the record, runs on this host and reads mode 0:

```
$ python3 -I -B tools/mori-commit-runway.py
{"band_kb": null, "batch_pages": null, "commit_limit_kb": 47583772, "committed_as_kb": 43803108,
 "cpus_present": 32, "enforced": false, "findings": [], "headroom_kb": 3780664, "limit_consistent": true,
 "limit_recomputed_kb": 47583772, "mode": 0, "notes": ["mode 0 (guess): only a single request above RAM + swap
 is refused; CommitLimit is printed, not enforced"], "reserve_kb": null, "schema": "mori-commit-runway-v1",
 "single_request_cap_kb": 63444672, "usable_kb": null, "verdict": "COMMIT_HEURISTIC"}
```

Host: `overcommit_memory=0`, `MemTotal 31721796 kB`, `SwapTotal 31722876 kB`, `CommitLimit 47583772 kB`,
`Committed_AS 43763740 kB` (read at a slightly different instant than the tool's 43803108), `present 0-31`,
kernel `7.2.11-arch1-1`. `single_request_cap_kb` 63444672 == (31721796 + 31722876) kB, which is the mode-0
single-request cap the contract specifies.

## Notes on method, for the report's named-limits section

- The whitespace-collapse rule matters: only 7 of the 46 v7.2 quotes occur in the v7.3 bytes as literal
  substrings; 39 more match only after collapsing whitespace. So the counter's `held` status is a
  whitespace-insensitive containment test, and the pinned sha256 (not the containment) is what pins the bytes.
  This is a property of the frozen counter, not a defect I propose to change.
- Two of the nine `git show` blob reads were served by the promisor remote after a 429 from GitHub during the
  v7.2 fetch; those two v7.2 blobs (mm/mmap.c, mm/util.c) were re-fetched over cgit instead and matched the lane's
  copies byte for byte. All nine v7.3 blobs were fetched over git in one pass with no rate-limit retry. The 429
  affected only the v7.2 side of my scratch, and the v7.2 side is corroboration, not the claim's evidence.
- No tool was installed or upgraded for this seat; the task needed only git, curl, python3 and sha256sum, all
  present. No pacman transaction was run.
- Disk guard was consulted before the fetch: `/fast/scratch/hyaku` at 24% used, 615.2G free; the clone is
  blob-filtered and the scratch peaked in the low megabytes of blobs plus a shallow git object store.

## Findings

- **LOW — no defect.** All nine S502–S510 paths are byte-identical between the lane's committed v7.3 copies and an
  independent blob-filtered git fetch of `refs/tags/v7.3` from `github.com/torvalds/linux`
  (`corpus/evidence/sources-r53/*.v7.3`); the cgit channel the L1 used serves the same bytes. No change proposed.
- **LOW — no defect.** The tag anchors are right: tag object `091b06388b117fefdcb63336ac09956a4914b961`, peeled
  commit `c03c1a14507dfaf8b856c2608f9ac216021fc222`, both matching the S502–S510 anchor cells and the contract's
  `refs/tags/v7.3^{}` value. No change proposed.
- **LOW — no defect.** The ledger's 46 status/quote cells re-derive from independently fetched bytes
  (44 held, 2 absent, 46/46 quote cells located); the two `absent` rows are exactly the two MAP_NORESERVE rows in
  `mm/mmap.c`, and the respelling is `vm_flags |= VM_NORESERVE` → `vma_flags_set(&vma_flags, VMA_NORESERVE_BIT)`.
  No change proposed.
- **LOW — no defect.** The ledger's v7.2→v7.3 changed-line counts and its "byte-identical" trio reproduce exactly
  from my own v7.2/v7.3 bytes, and the lane's committed v7.2 copies (`sources-r51/`, `sources-r52/`) match my
  independently fetched v7.2 blobs. No change proposed.
- **LOW — informational, counter property (not a proposed change).** `held` depends on whitespace-collapsed
  containment: 39 of 46 v7.2 quotes match only after collapsing whitespace. The counter's `status_ok`/`quote_ok`
  arms therefore prove word-presence, not literal-line presence. The sha256 pins are what carry byte identity.
  Route to round 54 as a named limit of the `held`/`absent` derivation, per the contract's "never propose a change
  to a frozen counter" rule.
- **LOW — informational, counter property (not a proposed change).** The counter's `source_rows` arm and its scope
  arm read `corpus/SOURCES.md` at different revisions (scope D at the entering tip, the v7.3 rows at the data
  commit); the S502–S510 rows do not exist at the entering tip, so a reader who checks both at one revision gets
  a parse error rather than a wrong answer. Route as a documentation point for round 54.
- **LOW — informational.** The C2 band's kernel rule (`mm/mm_init.c` lines 191–210) and the S511–S513 copies
  reproduce on this independent channel too, and the C2 tool runs live on this host with a mode-0 verdict that
  matches the contract's mode-0 arithmetic. Not my seat's claim; recorded as corroboration.

UNVERIFIED: whether the round-53 RECHECK voters' `holds` dispositions are correct readings of the v7.3 text — that
is the vote arm, owned by the twelve RECHECK seats, and I did not score it. UNVERIFIED: any claim outside the 46
rows of scope D (the three 2014-commit-patch rows, the SOURCES anchors of S492–S501, prose outside the two
tables) — out of scope by the contract's own definition.
