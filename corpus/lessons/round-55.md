# Round 55 lesson (L1 MoriR55)

Entering tip `ca52426ea496bc6592e3e867cc9d28843e45f196`; round-54 closure is admitted. Freeze `c9b908f0bb89974f30b927776ce2450ae4198b10`. Claims: C1 freshness, 78 pointer groups from three entries; C2 depth, 23 located claims on filesystem ENOSPC runway. One v2 wave `w1` is dispatched after the data commit. Receipts and seat outcomes are under `.ufo/waves/round-55/`.

## Gate

### New source rows (S526–S543)

All were opened 2026-10-27 from their pinned URLs, fetched to `corpus/evidence/sources-r55/` and hashed in the registry/counter. Each quote is located in the committed source copy; the counter pins full bytes. Rows S526–S534 support the pointer ledger; S535–S543 support the disk-runway entry.

| id | URL | accessed | ≤25-word located quote | decision |
|---|---|---|---|---|
| S526 | https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/fs/proc/base.c?h=v7.3 — `corpus/evidence/sources-r55/fs_proc_base.c.v7.3:583` | 2026-10-27 | `static int proc_oom_score(struct seq_file *m, struct pid_namespace *ns,` | admit, tier A |
| S527 | https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/mm/page_alloc.c?h=v7.3 — `corpus/evidence/sources-r55/mm_page_alloc.c.v7.3:4248` | 2026-10-27 | `should_compact_retry(gfp_t gfp_mask, struct alloc_context *ac, int order,` | admit, tier A |
| S528 | https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/include/trace/events/oom.h?h=v7.3 — `corpus/evidence/sources-r55/include_trace_events_oom.h.v7.3:76` | 2026-10-27 | `TRACE_EVENT(mark_victim,` | admit, tier A |
| S529 | https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/Documentation/accounting/psi.rst?h=v7.3 — `corpus/evidence/sources-r55/Documentation_accounting_psi.rst.v7.3:4` | 2026-10-27 | `PSI - Pressure Stall Information` | admit, tier A |
| S530 | https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/kernel/sched/psi.c?h=v7.3 — `corpus/evidence/sources-r55/kernel_sched_psi.c.v7.3:796` | 2026-10-27 | `static void psi_group_change(struct psi_group *group, int cpu,` | admit, tier A |
| S531 | https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/include/linux/psi_types.h?h=v7.3 — `corpus/evidence/sources-r55/include_linux_psi_types.h.v7.3:65` | 2026-10-27 | `PSI_IRQ_FULL,` | admit, tier A |
| S532 | https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/Documentation/admin-guide/kernel-parameters.txt?h=v7.3 — `corpus/evidence/sources-r55/Documentation_admin-guide_kernel-parameters.txt.v7.3:5540` | 2026-10-27 | `psi=		[KNL] Enable or disable pressure stall information` | admit, tier A |
| S533 | https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/Documentation/admin-guide/cgroup-v2.rst?h=v7.3 — `corpus/evidence/sources-r55/Documentation_admin-guide_cgroup-v2.rst.v7.3:1938` | 2026-10-27 | `  memory.pressure` | admit, tier A |
| S534 | https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/kernel/fork.c?h=v7.3 — `corpus/evidence/sources-r55/kernel_fork.c.v7.3:1795` | 2026-10-27 | `sig->oom_score_adj = current->signal->oom_score_adj;` | admit, tier A |
| S535 | https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/include/uapi/asm-generic/errno-base.h?h=v7.3 — `corpus/evidence/sources-r55/errno-base.h.v7.3:32` | 2026-10-27 | `#define ENOSPC 28 /* No space left on device */` | admit, tier A |
| S536 | https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/fs/statfs.c?h=v7.3 — `corpus/evidence/sources-r55/statfs.c.v7.3:62` | 2026-10-27 | `memset(buf, 0, sizeof(*buf)); retval = security_sb_statfs(dentry);` | admit, tier A |
| S536 | https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/fs/statfs.c?h=v7.3 — `corpus/evidence/sources-r55/statfs.c.v7.3:67` | 2026-10-27 | `if (retval == 0 && buf->f_frsize == 0) buf->f_frsize = buf->f_bsize;` | admit, tier A |
| S541 | https://git.kernel.org/pub/scm/docs/man-pages/man-pages.git/plain/man/man2/statfs.2?h=man-pages-6.19 — `corpus/evidence/sources-r55/statfs.2.man-pages-6.19:42` | 2026-10-27 | `fsblkcnt_t f_bfree; /* Free blocks in filesystem */ fsblkcnt_t f_bavail; /* Free blocks available to` | admit, tier A |
| S541 | https://git.kernel.org/pub/scm/docs/man-pages/man-pages.git/plain/man/man2/statfs.2?h=man-pages-6.19 — `corpus/evidence/sources-r55/statfs.2.man-pages-6.19:45` | 2026-10-27 | `fsfilcnt_t f_files; /* Total inodes in filesystem */ fsfilcnt_t f_ffree; /* Free inodes in filesystem */` | admit, tier A |
| S542 | https://git.kernel.org/pub/scm/docs/man-pages/man-pages.git/plain/man/man3/statvfs.3?h=man-pages-6.19 — `corpus/evidence/sources-r55/statvfs.3.man-pages-6.19:228` | 2026-10-27 | `Under Linux, .I f_favail is always the same as .IR f_ffree , and there's no way for a filesystem to report otherwise.` | admit, tier A |
| S542 | https://git.kernel.org/pub/scm/docs/man-pages/man-pages.git/plain/man/man3/statvfs.3?h=man-pages-6.19 — `corpus/evidence/sources-r55/statvfs.3.man-pages-6.19:233` | 2026-10-27 | `This is not an issue, since no filesystems with an inode root reservation exist.` | admit, tier A |
| S543 | https://raw.githubusercontent.com/coreutils/coreutils/v9.12/doc/coreutils.texi — `corpus/evidence/sources-r55/coreutils.texi.v9.12:11950` | 2026-10-27 | `List inode usage information instead of block usage.` | admit, tier A |
| S537 | https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/fs/xfs/xfs_super.c?h=v7.3 — `corpus/evidence/sources-r55/xfs_super.c.v7.3:999-1003` | 2026-10-27 | `* XFS does not distinguish between blocks available to privileged and * unprivileged users. */ st->f_bavail = st->f_bfree; return 0;` | admit, tier A |
| S537 | https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/fs/xfs/xfs_super.c?h=v7.3 — `corpus/evidence/sources-r55/xfs_super.c.v7.3:919` | 2026-10-27 | `st->f_bfree = max(0LL, fdblocks - xfs_freecounter_unavailable(mp, XC_FREE_BLOCKS));` | admit, tier A |
| S537 | https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/fs/xfs/xfs_super.c?h=v7.3 — `corpus/evidence/sources-r55/xfs_super.c.v7.3:952` | 2026-10-27 | `uint64_t fakeinos = XFS_FSB_TO_INO(mp, st->f_bfree); st->f_files = min(icount + fakeinos, (uint64_t)XFS_MAXINUMBER);` | admit, tier A |
| S537 | https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/fs/xfs/xfs_super.c?h=v7.3 — `corpus/evidence/sources-r55/xfs_super.c.v7.3:955` | 2026-10-27 | `if (M_IGEO(mp)->maxicount) st->f_files = min_t(typeof(st->f_files), st->f_files,` | admit, tier A |
| S538 | https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/fs/btrfs/super.c?h=v7.3 — `corpus/evidence/sources-r55/btrfs_super.c.v7.3:1771` | 2026-10-27 | `Account global block reserve as used, it's in logical size already` | admit, tier A |
| S538 | https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/fs/btrfs/super.c?h=v7.3 — `corpus/evidence/sources-r55/btrfs_super.c.v7.3:1803-1804` | 2026-10-27 | `* We only want to claim there's no available space if we can no longer * allocate chunks for our metadata profile` | admit, tier A |
| S538 | https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/fs/btrfs/super.c?h=v7.3 — `corpus/evidence/sources-r55/btrfs_super.c.v7.3:1804-1805` | 2026-10-27 | `* allocate chunks for our metadata profile and our global reserve will * not fit in the free metadata space.` | admit, tier A |
| S538 | https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/fs/btrfs/super.c?h=v7.3 — `corpus/evidence/sources-r55/btrfs_super.c.v7.3:1792` | 2026-10-27 | `delta to a 4M threshold. (Practically observed delta was ~2M.)` | admit, tier A |
| S538 | https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/fs/btrfs/super.c?h=v7.3 — `corpus/evidence/sources-r55/btrfs_super.c.v7.3:1797` | 2026-10-27 | `succeed even if the Avail is zero. But this is better than the other` | admit, tier A |
| S539 | https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/fs/btrfs/sysfs.c?h=v7.3 — `corpus/evidence/sources-r55/btrfs_sysfs.c.v7.3:897` | 2026-10-27 | `SPACE_INFO_ATTR(total_bytes); SPACE_INFO_ATTR(bytes_used); SPACE_INFO_ATTR(bytes_pinned); SPACE_INFO_ATTR(bytes_reserved); SPACE_INFO_ATTR(bytes_may_use); SPACE_INFO_ATTR(bytes_readonly);` | admit, tier A |
| S539 | https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/fs/btrfs/sysfs.c?h=v7.3 — `corpus/evidence/sources-r55/btrfs_sysfs.c.v7.3:677` | 2026-10-27 | `return btrfs_show_u64(&block_rsv->size, &block_rsv->lock, buf); } BTRFS_ATTR(allocation, global_rsv_size, global_rsv_size_show);` | admit, tier A |
| S540 | https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/Documentation/filesystems/tmpfs.rst?h=v7.3 — `corpus/evidence/sources-r55/tmpfs.rst.v7.3:83` | 2026-10-27 | `nr_inodes The maximum number of inodes for this instance. The default` | admit, tier A |
| S540 | https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/Documentation/filesystems/tmpfs.rst?h=v7.3 — `corpus/evidence/sources-r55/tmpfs.rst.v7.3:101` | 2026-10-27 | `extended attributes: "df -i"'s IUsed and IUse% increase, IFree decreases.` | admit, tier A |
| S540 | https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/Documentation/filesystems/tmpfs.rst?h=v7.3 — `corpus/evidence/sources-r55/tmpfs.rst.v7.3:95` | 2026-10-27 | `if nr_inodes=0, inodes will not be limited. It is generally unwise to mount with such options,` | admit, tier A |
| S540 | https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/Documentation/filesystems/tmpfs.rst?h=v7.3 — `corpus/evidence/sources-r55/tmpfs.rst.v7.3:92` | 2026-10-27 | `the default, when neither size nor nr_blocks is specified, is size=50%` | admit, tier A |

### Reused source rows and row changes

S502 `used-by`: `kernel-v7.3-recheck-r53.md` → that path plus `kernel-v7.3-recheck-r55.md`. S516 `used-by`: `kernel-v7.3-recheck-r54.md` → that path plus `kernel-v7.3-recheck-r55.md`. Both are append-only field changes; row payloads otherwise unchanged. No other old source row changed.

The 404 response for the attempted v7.3 `Documentation/ABI/testing/sysfs-fs-btrfs` path was not admitted as a source; the kernel's implementation is instead grounded in S538 (`fs/btrfs/super.c`) and S539 (`fs/btrfs/sysfs.c`).

### Non-author gate dispositions (pending wave settlement)

The wave reviewers re-opened C1's v7.3 source copies and C2's source copies; the final admitted and rejected sample decisions and reasons are recorded in the w1 results/seat reports, summarized here after settlement. No claim is accepted solely from its located quote.

### Round-54 routed defects and corrections

D1: r54 `census-end.txt` was typed rather than captured; its spaces/tabs and S349 URL differ from the command. R55's `census-start.txt` and later `census-end.txt` preserve raw command output plus exit status. D2: four wrong Gate locators corrected append-only in `round-54.md`'s errata (S515 1850, S520 rendered 1409, S522 70, S525 3). D3: appended correction says the r54 control receipt limitation is 12/14 unresolvable revisions, not ten. D4: `.ufo/waves/round-54/w1.ready.dispatched` is already tracked at the r55 entering tip (the orchestrator committed it as `ca52426e`), so no new relocation was needed. D5: 73/74 reports exist, only `Mo54RevC1Counter` is missing. D6: r54 lesson append adds resolvable `M1`/`M2` headings for QUALITY 148/149.

## Mistakes

| class | evidence pointer | captured-by | fix / shown able to fail |
|---|---|---|---|
| reference-drift | `corpus/lessons/round-54-verifier-spotcheck.md` D2: S515/S520/S522/S525 Gate line numbers | SOURCES row quote-and-locator rule (CORPUS.md rule 1) | appended the four corrected locators to `corpus/lessons/round-54.md`; the spot-check demonstrates the original locations do not start the quotes |
| number-drift | `corpus/lessons/round-54-verifier-spotcheck.md` D3: SCORECARD still said Ten where the observation was 12/14 | append-only correction sweep | append correction in scorecard; the direct `grep` of existing mentions finds the stale sentence, so a correction appended without searching every copy would fail the sweep |
| attribution | `corpus/lessons/round-54-verifier-spotcheck.md` D5/D6: four missing reports claimed vs 73/74; QUALITY pointers name nonexistent M1/M2 headings | `w1-results.json` count and resolved lesson anchors | corrected count and added M1/M2 headings append-only; `git ls-tree` derives 73 markdown reports from 74 results |

## Census

Start command `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori` was captured to `.ufo/waves/round-55/evidence/census-start.txt` with `exit=0`; initial registry had 298 rows and 23 W04 warnings. End receipt is captured mechanically after the last registry edit.

## Assimilation and quarantine

Assimilation: none. No `merge/mori/` package entry was adopted; the round's claims are sourced from opened kernel/man/coreutils source rows. `considerthese/2026-10-26.md` suggestions were checked; its outstanding pin-environment split and carry-over-flag ledger are not part of the frozen claims. The absent-defect register slice is re-derived and adjudicated in the round evidence; no campaign file is changed.

## Spot-check

Pending independent non-author closure; the wave is the lane. Candidate sample: admit S537 (XFS statfs source) and reject the absent btrfs ABI-document path (HTTP 404; implementation sourced from S538/S539).
