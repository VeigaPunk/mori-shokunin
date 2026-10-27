# Mo55Exec02 — every frozen source-copy hash verified (round 55, w1)

Seat: Mo55Exec02 (executor, leaf; detection only). Lane `mori-shokunin`, fleet root
`/home/vgpnk/Projects/shokunin`, measure revision `b8a70adf93ebd9d1e4e95bef8627a220f2fa816b`
(qualifying data `b8b7064c2b54c8b6b22c288232a96c43fae1af47`, freeze `c9b908f0…`,
entering tip `ca52426e…`). No production edits, no git/jj mutation, no installs.
Scratch `/fast/scratch/hyaku/mori-r55/Mo55Exec02` created and removed; disk guard read
first: `/fast` 26% used, 594.6G free, no ENOSPC.

Vote lines: none. This is not a counting seat, and no line below begins with a vote token.

## What was verified

Frozen source-copy hashes were checked at four independent layers:

1. **Freeze manifest self-consistency** — `sha256sum -c` over all 35 pinned paths.
2. **Copy bytes vs manifest vs committed blobs** — each `corpus/evidence/sources-r55/*`
   hashed in the working tree and recomputed from git blobs at `c9b908f0`, `b8b7064c`, `HEAD`.
3. **Counter-embedded pins** — every `(path, sha256)` pair declared inside the frozen
   `count-c1.py` / `count-c2.py` tables, plus the pins written in `corpus/SOURCES.md` rows.
4. **Live upstream provenance** — each copy re-fetched from its pinned upstream URL
   (18 tag-v7.3 rows) or the tag-v7.2 path (6 paired copies) and re-hashed.

## Command / output / exit evidence

### E1 — manifest over the whole freeze set

```
cd /home/vgpnk/Projects/shokunin/mori-shokunin
sha256sum -c .ufo/waves/round-55/evidence/freeze-sha256.txt > check-freeze-all.txt 2>&1
showed:  35 lines, all ": OK"
grep -c ': OK$'  -> 35
grep -v ': OK$'  -> (no output)
exit=0
```
35/35 OK. The manifest covers 11 freeze artefacts (`.ufo/waves/round-55/checks/*`,
`contract.md`, `controls/c1data.py`, `controls/c2data.py`, `count-c1.py`, `count-c2.py`,
`evidence/c1-scope-count.txt`, `evidence/c1-scope.txt`, `evidence/selftest-c1.txt`,
`evidence/selftest-c2.txt`) and the 24 source copies on manifest lines 12–35.

### E2 — copy bytes vs manifest (24/24)

Every file in `corpus/evidence/sources-r55/` is a regular file (0 symlinks, 24 files), and the
directory listing equals the manifest's source-copy name set (`diff` of sorted names: empty).
Per-copy result — frozen prefix, recomputed prefix, and live upstream re-fetch:

| copy | frozen sha256 | actual sha256 | file vs freeze | live upstream |
|---|---|---|---|---|
| Documentation_accounting_psi.rst.v7.2 | 11c6b7129103b454 | 11c6b7129103b454 | match | MATCH |
| Documentation_accounting_psi.rst.v7.3 | 11c6b7129103b454 | 11c6b7129103b454 | match | MATCH |
| Documentation_admin-guide_cgroup-v2.rst.v7.2 | a9433bb0e16a67f0 | a9433bb0e16a67f0 | match | MATCH |
| Documentation_admin-guide_cgroup-v2.rst.v7.3 | 2750c11a6324e18f | 2750c11a6324e18f | match | MATCH |
| Documentation_admin-guide_kernel-parameters.txt.v7.2 | 23b1a690210b6884 | 23b1a690210b6884 | match | MATCH |
| Documentation_admin-guide_kernel-parameters.txt.v7.3 | b5a13c038a27e688 | b5a13c038a27e688 | match | MATCH |
| btrfs_super.c.v7.3 | 6715b89d60575dd4 | 6715b89d60575dd4 | match | MATCH |
| btrfs_sysfs.c.v7.3 | 098cb522131501de | 098cb522131501de | match | MATCH |
| coreutils.texi.v9.12 | e6521c9b2e677dd2 | e6521c9b2e677dd2 | match | MATCH |
| errno-base.h.v7.3 | 2c148e92b8318dee | 2c148e92b8318dee | match | MATCH |
| fs_proc_base.c.v7.3 | fb419e9a64d61703 | fb419e9a64d61703 | match | MATCH |
| include_linux_psi_types.h.v7.2 | 483269b27c82b438 | 483269b27c82b438 | match | MATCH |
| include_linux_psi_types.h.v7.3 | 483269b27c82b438 | 483269b27c82b438 | match | MATCH |
| include_trace_events_oom.h.v7.3 | 82f04ad4108ba949 | 82f04ad4108ba949 | match | MATCH |
| kernel_fork.c.v7.2 | 359882ea981b58f5 | 359882ea981b58f5 | match | MATCH |
| kernel_fork.c.v7.3 | fa32ca5a79d4d000 | fa32ca5a79d4d000 | match | MATCH |
| kernel_sched_psi.c.v7.2 | 452318beaca3e6d1 | 452318beaca3e6d1 | match | MATCH |
| kernel_sched_psi.c.v7.3 | c4edc1e7c18ca76e | c4edc1e7c18ca76e | match | MATCH |
| mm_page_alloc.c.v7.3 | 315ef97b0ec1c6d7 | 315ef97b0ec1c6d7 | match | MATCH |
| statfs.2.man-pages-6.19 | 3dc4ed703d7e2b5e | 3dc4ed703d7e2b5e | match | MATCH |
| statfs.c.v7.3 | 34e684be1575eb3c | 34e684be1575eb3c | match | MATCH |
| statvfs.3.man-pages-6.19 | 5f65e9ce697bf5ce | 5f65e9ce697bf5ce | match | MATCH |
| tmpfs.rst.v7.3 | 5ce3dffe9323912b | 5ce3dffe9323912b | match | MATCH |
| xfs_super.c.v7.3 | 0f806bf4ea1859a4 | 0f806bf4ea1859a4 | match | MATCH |

Any hash group naming more than one path is upstream-true, not a copy error: the accounting
`psi.rst` pair and the `include/linux/psi_types.h` pair are byte-identical at tags v7.2 and v7.3
in the pinned upstream (both were fetched separately from `?h=v7.2` and `?h=v7.3` and returned the
same bytes). The other four pairs differ, matching the C1 ledger's `moved` entries for
kernel-parameters (5505→5540) and page_alloc (4265→4311).

### E3 — committed blobs at the three cited revisions

```
for rev in c9b908f0 b8b7064c HEAD:
  git ls-tree -r --name-only $rev -- corpus/evidence/sources-r55   (24 paths)
  git cat-file blob $rev:<path> | sha256sum                        (24 hashes)
  diff <manifest source lines> <rev hash list>  ->  empty
```
`c9b908f0: identical to manifest`, `b8b7064c: identical to manifest`, `HEAD: identical to manifest`
— exit 0, 24/24 each. Freeze-time, data-time and tip bytes are the same bytes.

The manifest itself is `sha256 9820cae1cb5ce87ada6d87302b9fcf70412e0dc6baea0d7eacd3bbd1629353fa`,
4,085 bytes, last touched by `c9b908f0` (the freeze commit), so the pin list read here is the
frozen one, not a later rewrite.

### E4 — freeze paths unchanged since the freeze commit

```
git diff --stat c9b908f0 HEAD -- <all 35 manifest paths>   -> empty
git status --porcelain -- <all 35 manifest paths>          -> empty
```
No drift between the freeze commit and the working tree over any frozen path.

### E5 — counter-embedded copy hashes

`count-c1.py` `COPIES` (starts line 62) declares 22 distinct `(path, sha256)` pairs, `SRC_DIR` on
line 53. Recomputed all 22: **0 mismatches, 0 missing files**. Fifteen are `sources-r55` copies
(the 12 C1 pointer pairs plus 3 v7.3-only), seven are prior-round copies outside this round's
manifest (`sources-r47/fs_proc_base.c`, `sources-r47/include_trace_events_oom.h`,
`sources-r47/mm_page_alloc.c`, `sources-r50/oom_kill.c.v7.2`, `sources-r51/proc.rst.v7.2`,
`sources-r53/proc.rst.v7.3`, `sources-r54/oom_kill.c.v7.3`); every one of those seven also hashes
to the value the frozen counter states, so the counter's input set is intact too.

`count-c2.py` declares its nine sources relative to `SRC_DIR = corpus/evidence/sources-r55/`
(lines 59, 63–79). Recomputed all nine: **0 mismatches**, each equal to the round-55 manifest line.

`corpus/SOURCES.md`: 18 rows (S526–S543) carry a full 64-hex `sha256` plus a
`copy corpus/evidence/sources-r55/…v7.3` path; 18/18 equal both the file and the manifest.
The six v7.2 paired copies carry 16-hex pins in the earlier rows that admitted those bytes
(S090 `11c6b7129103b454`, S091 `452318beaca3e6d1`, S092 `a9433bb0e16a67f0`,
S094 `23b1a690210b6884`, S095 `483269b27c82b438`, S127 `359882ea981b58f5`); all six prefixes
match the current bytes.

### E6 — live upstream re-fetch

Each of the 18 v7.3 rows was fetched from the exact URL in its `SOURCES.md` cell
(`git.kernel.org/…/plain/<path>?h=v7.3`, man-pages `?h=man-pages-6.19`, and
`raw.githubusercontent.com/coreutils/coreutils/v9.12/doc/coreutils.texi`); each of the six v7.2
paired copies was fetched from `git.kernel.org/…/plain/<same path>?h=v7.2`
(URL derivation is [INFERENCE] — the rows name only the v7.3 URL — but the resulting bytes hash to
the frozen values, so the mapping is confirmed by the hash, not assumed).
All 24 fetches returned HTTP-level success (`curl -fsSL` rc 0) and **24/24 sha256 equal the frozen
values** (`upstream_sha256 == frozen_sha256` at full 64-hex; recorded in scratch
`upstream-v73.json` / `upstream-v72.json` before cleanup, values reproduced above).
This rules out the residual hash-clean-but-wrong-file case: the bytes on disk are the bytes the
pinned upstream URL serves today.

## Observations (outside the source-copy hash scope, recorded for routing)

* The manifest does not pin two artefacts the contract's freeze sentence names
  (`contract.md:5`, "control readings, selftest receipts, census-start and misroot precheck"):
  `evidence/census-start.txt` was added at `b8b7064c` (after the freeze commit) and is not in
  `freeze-sha256.txt`, and no misroot-precheck file exists under
  `.ufo/waves/round-55/`. The selftest receipts and control *code* are pinned
  (`freeze-sha256.txt:1-11`), but the control *reading* outputs (`control-c1-do-nothing.txt`,
  `control-c2-do-nothing.txt`, added at `121093e2`) are not. This is a freeze-coverage wording
  gap, not a copy-hash defect; the source copies themselves are fully pinned.
* C2 claim 1 quotes `#define ENOSPC 28 /* No space left on device */`, while
  `errno-base.h.v7.3:32` is `#define\tENOSPC\t\t28\t/* No space left on device */`
  (tabs). The frozen counter collapses whitespace on both sides (`count-c2.py:95`, `:233`), so the
  located-quote arm accepts it; noted only because it is the one place a doc quote is not
  byte-verbatim.
* Nine `sources-r55` copies (btrfs/tmpfs/statfs/statvfs/errno/coreutils/xfs) are declared only in
  `count-c2.py`'s table, and the 15 C1-pointer copies only in `count-c1.py`'s. Union of both
  tables covers all 24 manifest copies; no copy is unpinned by a frozen counter.

## Files changed

`.ufo/waves/round-55/w1/Mo55Exec02.md` (this report). Nothing else.

## Risks and blockers

* None blocking. Two residual risks named: (a) live upstream equality was measured at
  `2026-10-27` fetch time; a later upstream force-push of a tag would change what a re-fetch shows
  even though the frozen bytes stay pinned by hash; (b) the freeze-coverage wording gap above is
  for the L1/validator to route, not for this seat to repair.
* Installations: none (no package manager invoked; `pacman` untouched).

## Findings

| severity | finding | evidence |
|---|---|---|
| none (verified) | 24/24 frozen source-copy hashes match the manifest, the committed blobs at `c9b908f0`/`b8b7064c`/`HEAD`, the frozen counters' embedded pins, the `SOURCES.md` rows, and a live upstream re-fetch; no discrepancy to report | `.ufo/waves/round-55/evidence/freeze-sha256.txt:12-35`; table E2 above; E1 exit 0 |
| none (verified) | whole freeze manifest verifies, 35/35 OK, and no frozen path changed between the freeze commit and the tip | `sha256sum -c` rc 0; E1, E4 above |
| low (out of assigned scope, wording) | contract's freeze sentence names census-start/misroot-precheck/control readings as frozen, but the manifest pins neither `census-start.txt`, the misroot precheck, nor the `control-*-do-nothing.txt` readings; those files landed after the freeze commit | `.ufo/waves/round-55/contract.md:5`; `git log --diff-filter=A -- .ufo/waves/round-55/evidence/census-start.txt` → `b8b7064c`; manifest lines 1–11 |
| info (non-defect) | C2 claim 1's quote reproduces tab-indented source bytes with spaces; the frozen counter normalizes whitespace, so the quote locates by design | `corpus/evidence/sources-r55/errno-base.h.v7.3:32`; `corpus/knowledge/disk-runway-enospc-r55.md:11`; `.ufo/waves/round-55/count-c2.py:95,233` |
