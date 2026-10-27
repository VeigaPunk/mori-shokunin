# Mo55Rev02 — XFS inode/free-block and tmpfs inode semantics against the pinned copies

Seat: `Mo55Rev02` (revenger, leaf, no dispatch). Lane `mori-shokunin`, round 55, wave `w1`.
Surface: C2 rows 9–12 (XFS, S537) and rows 20–23 (tmpfs, S540), plus carrier rows 2–3 and 6–8 where the
`statfs`/`statvfs` interface decides how XFS and tmpfs readings reach userspace.
Entering tip `ca52426ea496bc6592e3e867cc9d28843e45f196`; data revision `b8b7064c2b54c8b6b22c288232a96c43fae1af47`
(entry blob `9317eec114e708fcee6ee643c6ceb219966f1ba70da632b5c59edf9ab5251cd7`, byte-identical to the working tree).

Non-voter. The C2 voter set is `Mo55En01`–`Mo55En12`; this seat is outside it, so this report carries no vote
lines and cannot satisfy an entailment vote.

## Method and boundaries

- Reverse-engineered the two filesystem contracts from the frozen source copies first (literal line citations),
  then tested every derived invariant against read-only host readings. Grep was used only over frozen text files;
  the `lsp` device is not mounted in this runtime (`read xd://lsp` → "No such tool"), so no semantic
  definition/reference navigation was available and none of the line citations below are presented as LSP results.
- No production edits, no git/jj mutation, no mounts, sysctls, cgroups, quota or repair operations, no
  ENOSPC/OOM forcing, no installs. Scratch `/fast/scratch/hyaku/mori-r55/Mo55Rev02` used for two revision
  extracts and removed at the end. `scripts/hyaku/disk-guard.sh status` clear at start and end (27% on
  `/fast/scratch/hyaku`, 590 G free); no ENOSPC condition observed.
- Pin check: `sha256sum` over all nine C2 copies in `corpus/evidence/sources-r55/` matched
  `.ufo/waves/round-55/evidence/freeze-sha256.txt`, including `xfs_super.c.v7.3`
  `0f806bf4…91eed831`, `tmpfs.rst.v7.3` `5ce3dffe…22b954be6`, `statfs.c.v7.3` `34e684be…0905398`,
  `statvfs.3.man-pages-6.19` `5f65e9ce…6ae0b58`, `statfs.2.man-pages-6.19` `3dc4ed70…3b9d`,
  `coreutils.texi.v9.12` `e6521c9b…6148db9`, `errno-base.h.v7.3` `2c148e92…95793c`,
  `btrfs_super.c.v7.3` `6715b89d…cee43fc`, `btrfs_sysfs.c.v7.3` `098cb522…b467377`. Exit 0.

## Reconstructed contract A — XFS `statfs` (v7.3 copy)

Call site `fs/xfs/xfs_super.c:986-1002`: `xfs_statfs_data(mp, st)` → `xfs_statfs_inodes(mp, st)` → optional
`xfs_statfs_rt(mp, st)` (989-991) → optional `xfs_qm_statvfs(ip, st)` (993-996) → `st->f_bavail = st->f_bfree`
(1002) → `return 0`. Consequences that matter for the claims:

1. Block path (911-927): `fdblocks = xfs_sum_freecounter(mp, XC_FREE_BLOCKS)` (915-916);
   `st->f_bfree = max(0LL, fdblocks - xfs_freecounter_unavailable(mp, XC_FREE_BLOCKS))` (918-920);
   `st->f_blocks = sb_dblocks - xfs_internal_log_size(mp)` (926).
2. Inode path (946-965):
   `icount = percpu_counter_sum(&mp->m_icount)`, `ifree = percpu_counter_sum(&mp->m_ifree)` (950-951);
   `fakeinos = XFS_FSB_TO_INO(mp, st->f_bfree)` (952);
   `st->f_files = min(icount + fakeinos, (uint64_t)XFS_MAXINUMBER)` (954);
   if `M_IGEO(mp)->maxicount`, `st->f_files = min_t(…, st->f_files, M_IGEO(mp)->maxicount)` (955-957);
   then `st->f_files = max_t(…, st->f_files, mp->m_sb.sb_icount)` (959-961, comment: "If sb_icount overshot
   maxicount, report actual allocation"); finally
   `st->f_ffree = max_t(int64_t, 0, st->f_files - (icount - ifree))` (963-964).
3. So the reported inode total is piecewise, not a single formula: candidate `icount+fakeinos`, capped by the
   geometry maximum, floored at the on-disk allocation. It tracks free blocks only while
   `icount + fakeinos < maxicount`; at or above that point the total is pinned at `maxicount` (or at
   `sb_icount` if that is larger).
4. `f_bavail == f_bfree` unconditionally at return, because the assignment is last (1002), after the RT and
   project-quota overrides. The RT override replaces `f_bfree`/`f_blocks` with realtime-device values (935-943)
   and is *not* clamped; the claim rows on this surface describe the data-device path and the host mounts have
   no realtime device (`xfs_info`: `realtime =none`), so this is a scope note, not a divergence.
5. The handler never assigns `f_frsize` (no occurrence in the copy). `statfs.c:67-68` then fills it from
   `f_bsize`; `f_bsize = sb_blocksize` is set at 983. `f_namelen = MAXNAMELEN-1` (982; observed 255 — the
   `MAXNAMELEN` definition itself is not in the frozen copy); `f_type = XFS_SUPER_MAGIC` (981).

## Reconstructed contract B — how those fields reach userspace

- `statfs_by_dentry` clears the reply buffer before any filesystem code:
  `memset(buf, 0, sizeof(*buf)); retval = security_sb_statfs(dentry);` (`fs/statfs.c:62-63`), then calls
  `dentry->d_sb->s_op->statfs` (66), then `if (retval == 0 && buf->f_frsize == 0) buf->f_frsize = buf->f_bsize`
  (67-68). `vfs_statfs` additionally overwrites `f_flags` after the handler (`statfs.c:88-92`).
- Therefore "a field the filesystem never sets is zero" holds for filesystem-owned fields, but not literally
  for the two fields the VFS computes (`f_frsize`, `f_flags`). Btrfs is the clean witness: `btrfs_statfs`
  assigns `f_blocks`, `f_bfree`, `f_bavail`, `f_type`, `f_bsize`, `f_namelen`, `f_fsid` and never touches
  `f_files`/`f_ffree` (`btrfs_super.c:1720-1855`; grep for `f_files`/`f_ffree` in that file returns nothing),
  and the host reads `files=0 ffree=0`.
- `statvfs.3.man-pages-6.19:38-44` declares the four block/inode pairs; 228-234 states
  "Under Linux, f_favail is always the same as f_ffree, and there's no way for a filesystem to report
  otherwise. This is not an issue, since no filesystems with an inode root reservation exist."
  `f_favail` does not exist in the kernel `kstatfs` path at all (grep of `statfs.c`: no match), so the equality
  is produced in the libc `statvfs` mapping, exactly as the manual describes.
- `statfs.2.man-pages-6.19:42-46` declares `f_bfree` and `f_bavail` separately and `f_files`/`f_ffree`;
  `coreutils.texi.v9.12:11950` (and 12262) says the inode mode lists "inode usage information instead of block
  usage", i.e. a replacement column set.

## Reconstructed contract C — tmpfs size and inode limits (v7.3 doc)

- `tmpfs.rst:76-81`: `size` is "The limit of allocated bytes for this tmpfs instance. The default is half of
  your physical RAM without swap"; `nr_blocks` is the same in PAGE_SIZE blocks.
- `tmpfs.rst:83-86`: `nr_inodes` is "The maximum number of inodes for this instance. The default is half of the
  number of your physical RAM pages, or (on a machine with highmem) the number of lowmem RAM pages, whichever
  is the lower."
- `tmpfs.rst:88-92`: both parameters are remountable; "the default, when neither size nor nr_blocks is
  specified, is size=50%".
- `tmpfs.rst:94-97`: `nr_blocks=0`/`size=0` and `nr_inodes=0` remove the respective limits; "It is generally
  unwise to mount with such options".
- `tmpfs.rst:100-101`: with a nonzero `nr_inodes`, the inode allowance is "also used up by extended
  attributes: \"df -i\"'s IUsed and IUse% increase, IFree decreases."
- `tmpfs.rst:103`: "tmpfs blocks may be swapped out, when there is a shortage of memory" — residency can be
  disk-backed while the size cap stays RAM-derived.

## Live evidence (read-only; four readings)

`R0` = captured snapshot `.ufo/waves/round-55/evidence/host-disk-snapshot.txt` (file mtime 03:39 local).
`R1` (06:44Z), `R1b` (06:46Z) and `R2` (06:48Z) = this seat's `os.statvfs`/`stat -f`/`df` re-reads; the table
shows R0 and R2, and the intermediate re-reads gave `/tmp` bfree 32,795,425 / ffree 67,004,118 (both R1, R1b),
`/fast` bfree 155,858,346 / ffree 418,568,813 (R1) then 155,417,601 / 418,317,143 (R1b), `/` bfree 163,998,515 /
bavail 154,651,211 (R1), `/dev/shm` bfree 2,088,839 / ffree 3,965,126 (R1), `/run/user/1000` bfree 792,429 /
ffree 791,583 (R1).

| mount | fs | R0 bfree=bavail | R0 files | R0 ffree | R2 bfree=bavail | R2 files | R2 ffree |
|---|---|---|---|---|---|---|---|
| /tmp | xfs | 32,795,553 | 67,108,864 | 67,004,121 | 32,795,418 | 67,108,864 | 67,004,117 |
| /fast | xfs | 155,927,507 | 421,271,552 | 418,617,687 | 155,094,506 | 421,271,552 | 418,332,887 |
| / | btrfs | 164,012,985 / avail 154,665,001 | 0 | 0 | 163,998,515 / avail 154,651,211 | 0 | 0 |
| /dev/shm | tmpfs | 2,096,303 | 3,965,224 | 3,965,173 | 2,084,207 | 3,965,224 | 3,965,105 |
| /run/user/1000 | tmpfs | 792,437 | 793,044 | 791,759 | 792,416 | 793,044 | 791,547 |

Invariants observed in every read: XFS `bavail == bfree` exactly (and tmpfs likewise); `favail == ffree` on all
five mounts including the btrfs zeros; `frsize == bsize == 4096` on all five; btrfs `files == ffree == 0`.
`/fast` free moved by 833,001 blocks (3.18 GiB) between R0 and R2 while `files` stayed byte-identical.

Geometry is independently readable unprivileged, which is what makes the XFS reconstruction numeric rather than
merely textual:

```
$ xfs_info /tmp   # exit 0
meta-data isize=512  agcount=32, agsize=1048576 blks
data      bsize=4096  blocks=33554432, imaxpct=25
log       internal log bsize=4096 blocks=25087
$ xfs_info /fast  # exit 0
meta-data isize=512  agcount=32, agsize=6582368 blks
data      bsize=4096  blocks=210635776, imaxpct=25
log       internal log bsize=4096 blocks=102849
```

Derivations (arithmetic, all exact):

- `f_blocks`: 33,554,432 − 25,087 = 33,529,345 (observed /tmp); 210,635,776 − 102,849 = 210,532,927
  (observed /fast). The `sb_dblocks - internal_log` line (xfs_super.c:926) is reproduced to the block.
- `maxicount` = `sb_dblocks × (bsize/isize) × imaxpct/100` = `dblocks × 8 × 25/100` = `2 × dblocks`:
  67,108,864 for /tmp and 421,271,552 for /fast — exactly the two observed `f_files` values.
  Because `fakeinos = 8 × bfree` is 262,363,400 and 1,240,756,048 respectively, i.e. 3.9× and 2.9× the cap,
  the `min_t(…, maxicount)` branch (955-957) is the branch that binds on both mounts, and `f_files` cannot
  move while the cap binds. The `max_t(…, sb_icount)` floor (959-961) is inactive here (`sb_icount` is far below
  the cap), which is why the observed value equals `maxicount` exactly.
- Crossover: `f_files` starts tracking free blocks only when `bfree < maxicount/8 = sb_dblocks/4`, i.e. once
  block utilisation passes 75%. /tmp is 2.2% used and /fast ~26% used, so both are far above the crossover and
  the "moves with free space" behaviour is inert on this host. (Conditional on the default isize=512 and
  imaxpct=25 shown by `xfs_info`; for other geometry the crossover is `maxicount/inopb`.)
- `f_ffree`: the code derives it as `f_files − (icount − ifree)` (964). df's `IUsed` is itself computed as
  `f_files − f_ffree`, so the observed agreement (`/tmp` 104,746; `/fast` 2,847,315–2,938,665) is consistent
  but not independent: `icount`/`ifree` are percpu counters that the kernel does not export here
  (`/sys/fs/xfs/<dev>/stats/stats` contains no `icount`/`ifree` line; grep count 0). Treat line 964 as
  code-entailed, not live-verified.
- tmpfs defaults: `MemTotal = 31,721,796 kB` → 7,930,449 pages → floor(half) = 3,965,224 = observed
  `/dev/shm` `f_files`, with `size=8388608k` (`/proc/mounts`) and no `nr_inodes` option. The two ceilings are
  numerically independent: 2,097,152 blocks (= 8 GiB / 4096) versus 3,965,224 inodes.
  `/run/user/1000` is mounted `size=3172176k,nr_inodes=793044`; 3,172,176/4 = 793,044, and observed
  `f_blocks = f_files = 793,044`, i.e. an explicitly configured inode ceiling is reported as `f_files`.
  (The kernel `shmem_statfs` body is not among the pinned copies, so the `f_files = nr_inodes` mapping is a
  two-mount inference, not a source citation.)
- tmpfs `f_bfree` is page-granular against `size`: `/dev/shm` `f_blocks = 8,388,608 KiB / 4 = 2,097,152`.

## Divergences and adjudications on this surface

### D1 — row 11 (`4aab9fc1a48b`, entry line 21): overclaim confirmed

Claim as written: "XFS computes its reported inode total as inodes already allocated plus how many more the
current free blocks could hold, **so that total moves with free space**." The computation is entailed
(xfs_super.c:950-954), but the consequence is not: the same expression is `min(…, XFS_MAXINUMBER)` (954), the
next branch re-caps at `maxicount` (955-957), and the final total is floored at `sb_icount` (959-961). The host
demonstrates the failure of the consequence: `f_files` is 67,108,864 and 421,271,552 in all four readings while
`bfree` moves by up to 833,001 blocks, because both mounts sit exactly at their geometry-derived `maxicount`.
Movement resumes only below the 75%-used crossover. Exact unsupported clause: "so that total moves with free
space" (unqualified).

Correction text the lane can adopt (not a vote line, not written to the entry by this seat): "XFS starts its
reported inode total from inodes already allocated plus how many more the current free blocks could hold, then
caps that total, so it tracks free space only until a cap applies." Same quote; hash changes, so the row needs
fresh votes.

### D2 — row 12 (`d51f0bfc539f`, entry line 22): overclaim confirmed on the literal cap

Claim: "When an XFS mount has a maximum inode count configured, the reported inode total is **additionally
capped by that maximum** before free inodes are derived." The cap is applied (955-957) and `f_ffree` is derived
afterwards (963-964), but it is not an invariant: 959-961 immediately raises the total back to `sb_icount`, with
the comment "If sb_icount overshot maxicount, report actual allocation". So the reported total can exceed
`maxicount`; the claim's absolute wording is not entailed. Operational risk is low (requires on-disk allocation
above `maxicount`, which needs `imaxpct`/geometry drift), but under a kill rule that counts any overclaim the
literal wording is exposed. Note also that `imaxpct=25` is present on both host mounts without any option, so
"has a maximum inode count configured" is true of a default XFS, not only of an explicitly tuned one.

Correction text available to the lane: "When an XFS mount has a maximum inode count, the candidate inode total
is capped by it, then floored at the actual on-disk allocation, before free inodes are derived."

### D3 — row 23 (`b7cd35201fee`, entry line 33): not an overclaim on this surface

Claim: "A tmpfs mounted without any size option may grow to half of physical memory, so its block runway is
bounded by RAM rather than by a disk device." `tmpfs.rst:92` states the default size is 50% when neither size
nor nr_blocks is given, and 78-81 states the default is half of physical RAM; 103 notes blocks may be swapped.
The swap line concerns where pages are stored, not the size ceiling: the runway limit remains a RAM-derived
50%, and "rather than by a disk device" contrasts the ceiling with a partition size, which the copy supports.
The overclaim objection recorded in the wave ("does not support excluding disk-backed swap from its backing")
adds a residency condition the claim does not assert. Recommendation: do not sustain dissent on this row; if
the lane wants belt-and-braces wording, use "gets a default limit of half of physical memory, so its block
runway is set by RAM rather than by a disk partition size." Live note: neither host tmpfs mount exercises the
default-size path (`/dev/shm` size=8G, `/run/user/1000` size=3,172,176k), so the claim rests on the doc quote.

### D4 — row 2 (`e581c99e0a8d`, entry line 12): precision boundary, not a semantic defect

"any field a filesystem never sets reaches userspace as zero" is true for filesystem-owned fields and is
demonstrated live by btrfs `f_files = f_ffree = 0`, but the VFS itself fills `f_frsize` when it is zero
(statfs.c:67-68 — the subject of row 3) and overwrites `f_flags` (statfs.c:88-92). "Any field" therefore has
two named exceptions inside the same copy. The memset itself (62) and the zero consequence are entailed; the
universal quantifier is the only loose part. Low severity; optional tightening to "any field the VFS does not
itself fill".

### D5 — row 20 (`8f7ef0a716f2`, entry line 30): precision boundary

"The inode ceiling … set through a mount option that is separate from the instance's size limit" is correct on
the separation, but `/dev/shm` has no `nr_inodes=` option in `/proc/mounts` and still reports the default
ceiling 3,965,224. Read strictly as "only when an option is given", the wording overstates; read as "the
parameter is a mount option (with a RAM-derived default)", it is entailed by tmpfs.rst:83-86. Optional
tightening: "set by a mount option, with a RAM-derived default, separate from the size limit". No dissent
recommended.

### D6 — entry-internal numeric inconsistency between prose and its own captured evidence (LOW)

The prose snapshot (`disk-runway-enospc-r55.md:50`) and the captured snapshot (`:58`, plus
`evidence/host-disk-snapshot.txt`) describe the same day but disagree:

| value | prose line 50 | captured line 58 | this seat at 06:48Z |
|---|---|---|---|
| /fast bfree=bavail | 147,466,003 | 155,927,507 | 155,094,506 |
| /fast f_ffree | 417,090,444 | 418,617,687 | 418,332,887 |
| /tmp bfree=bavail | 32,795,798 | 32,795,553 | 32,795,418 |
| /tmp f_ffree | 67,005,211 | 67,004,121 | 67,004,117 |
| / bfree / bavail | 164,023,017 / 154,680,289 | 164,012,985 / 154,665,001 | 163,998,515 / 154,651,211 |
| /dev/shm ffree | 3,965,092 | 3,965,173 | 3,965,105 |
| df -P /fast | 30% | 26% | 27% |

The /fast gap is 8,461,504 blocks = 32.3 GiB of free space, far outside the drift seen between the captured file
and a re-read nine minutes later (833,001 blocks). The captured file and the live re-read track each other for
`/tmp` and `/` to within normal churn, so the prose is a stale or earlier read, not a copy of the captured one.
Since the entry advertises the captured file as "the immediately reproducible point-in-time values", the prose
should be reconciled to it (or explicitly timestamped as an earlier read). No claim in the table depends on
these numbers, so this does not affect entailment; it affects reproducibility.

### D7 — data-read receipt revision does not match the assigned data revision (MED, bookkeeping)

`evidence/c2-at-data.txt` ends `rev=f70051ddcb903dc6c4393c410f8bab054951af82`; the assigned data revision is
`b8b7064c…`. The `rev` is the counter's resolved argument (`count-c2.py:313-342`), not HEAD, so the recorded
read was taken one commit early. Checked delta between the two revisions: the entry diff is exactly the
appended "Captured host snapshot" section; the 23 claim texts and their hashes are identical in order
(verified by recomputing the 23 hashes from both blobs), and `corpus/SOURCES.md`, the nine source copies, the
counter and the control code are unchanged (`git diff --stat` over those paths is empty). So the claim/quote/
pin/provenance columns of the receipt remain valid at `b8b7064c`, but (a) the receipt's `rev` should be re-taken
at the data revision to match the contract's "measure the latter", and (b) the read at `f70051dd` cannot have
covered the appendix, which is precisely the section D6 disputes.

### D8 — snapshot command does not capture `f_favail`; `findmnt` line returns nothing (LOW)

The captured command uses `stat -f -c 'type=%T bsize=%S blocks=%b bfree=%f bavail=%a files=%c ffree=%d'`, which
omits `%A` (`f_favail`), so the captured evidence cannot support or refute row 6's `favail == ffree`; this seat
had to add `os.statvfs` to observe it. The same file records `findmnt -n -o TARGET,FSTYPE,OPTIONS /tmp /fast /
/dev/shm` exiting 1 with no output (multi-target form is unsupported), even though the decision table instructs
readers to "inspect `findmnt` options (`size=`, `nr_inodes=`)". Single-target `findmnt` or `/proc/mounts` works;
this report used `/proc/mounts` to obtain `size=`/`nr_inodes=`. Neither point touches entailment of the table;
both reduce reproducibility of the snapshot.

### D9 — version gap and unpinned helpers (boundary, not a defect)

The pinned sources are `v7.3`/man-pages 6.19/coreutils 9.12; the host is Linux 7.2.11-arch1-1. Live confirmation
of a v7.3 code path on a 7.2 kernel is an inference (the entry's own `recheck:` line says "on-release", which is
consistent). Also outside the frozen copies: `XFS_FSB_TO_INO`, `xfs_sum_freecounter`,
`xfs_freecounter_unavailable` (used at xfs_super.c:915-920, 952), the `XFS_MAXINUMBER` value, the `shmem_statfs`
body, and the `maxicount` derivation (not in `xfs_super.c`; the copy only consumes `M_IGEO(mp)->maxicount` at
322-325/955-957). This seat recovered `maxicount` empirically from `xfs_info` geometry, so the contract above is
numerically exact on this host, but the step "maxicount comes from sb_imax_pct" is inference from geometry plus
arithmetic, not a citation from the frozen set.

## Unverified on this surface

- Row 21 (extended attributes consume the tmpfs inode allowance): would require writing to a tmpfs mount; out
  of bounds for this seat. Doc-entailed only (tmpfs.rst:100-101).
- Row 22 (`nr_inodes=0` removes the ceiling): no such mount on the host; doc-entailed only (tmpfs.rst:94-97).
- Row 23 under the default-size path: both host tmpfs mounts set `size=` explicitly, so the 50%-of-RAM default
  is confirmed only arithmetically for the *default inode* ceiling (/dev/shm), not for the default size.
- Rows 13–19 (btrfs) are another seat's surface; not adjudicated here. Row 14/15/16 are also contested in the
  wave and are outside this seat.
- The XFS project-quota override (`xfs_qm_statvfs`, handler 993-996) and realtime override (935-943) bodies are
  either unpinned or untested (host mounts are `noquota`, `realtime =none`).
- No ENOSPC/EDQUOT reproduction, no fills, no cache drops: all readings had free blocks and inodes.

## Findings

- **MED (kill-relevant, row 11)** — `4aab9fc1a48b` overclaims "so that total moves with free space". The reported
  total is `min(icount+fakeinos, XFS_MAXINUMBER)` then `min(…, maxicount)` then `max(…, sb_icount)`
  (`corpus/evidence/sources-r55/xfs_super.c.v7.3:950-961`), and both host XFS mounts sit exactly at
  `maxicount` with `f_files` constant across four readings while `bfree` moved
  (`corpus/knowledge/disk-runway-enospc-r55.md:21`; evidence table above, R0/R2). Scoping fix available (D1).
- **MED (kill-relevant, row 12)** — `d51f0bfc539f` states the total is "capped by that maximum"; the code
  immediately floors at `sb_icount` with the comment "If sb_icount overshot maxicount, report actual
  allocation" (`xfs_super.c.v7.3:955-961`; claim at `disk-runway-enospc-r55.md:22`). Cap is real and binding on
  this host, but not an invariant. Scoping fix available (D2).
- **LOW (adjudication, row 23)** — `b7cd35201fee` is entailed as a statement about the size cap
  (`corpus/evidence/sources-r55/tmpfs.rst.v7.3:78-81,88-92,103`; claim at `disk-runway-enospc-r55.md:33`).
  Swap changes page residency, not the RAM-derived ceiling; the wave's overclaim objection adds a condition the
  claim does not assert. Do not sustain dissent on this row (D3).
- **LOW (precision, row 2)** — "any field a filesystem never sets reaches userspace as zero" has two exceptions
  in the same copy: `f_frsize` is filled by the VFS (`statfs.c.v7.3:67-68`, the subject of row 3) and `f_flags`
  is overwritten (`statfs.c.v7.3:88-92`). The memset and its zero consequence are entailed
  (`disk-runway-enospc-r55.md:12`); only the universal quantifier is loose (D4).
- **LOW (precision, row 20)** — default tmpfs inode ceiling exists without any `nr_inodes=` option
  (`/proc/mounts` for `/dev/shm`; observed `f_files=3,965,224 = floor(7,930,449/2)`), so "set through a mount
  option" reads strictly; separation from the size limit holds (`tmpfs.rst.v7.3:83-86,92`;
  `disk-runway-enospc-r55.md:30`) (D5).
- **LOW (reproducibility, entry)** — prose snapshot and the entry's own captured snapshot disagree, worst at
  `/fast` 147,466,003 vs 155,927,507 blocks (32.3 GiB) and 30% vs 26% df
  (`disk-runway-enospc-r55.md:50` vs `:58` and `evidence/host-disk-snapshot.txt`); live re-read tracks the
  captured file, not the prose (D6).
- **MED (bookkeeping, C2 data receipt)** — `evidence/c2-at-data.txt` records `rev=f70051dd…`, not the assigned
  data revision `b8b7064c…`; entry claim hashes and all pinned inputs are byte-identical across the two
  revisions, so the semantic columns survive, but the read predates the captured-snapshot appendix it would need
  to cover, and the contract says to measure `b8b7064c` (D7).
- **LOW (evidence capture)** — the snapshot's `stat -f` format omits `%A` (`f_favail`) and its multi-target
  `findmnt` line exits 1, so row 6's `favail == ffree` and the decision-table `findmnt` instruction are not
  reproducible from the captured file alone (D8).
- **Positive (rows 9, 10, 21, 22; row 20 with the D5 wording caveat)** — no divergence found. XFS
  `bavail == bfree` is assigned last
  (`xfs_super.c.v7.3:998-1002`) and observed equal on both mounts in all readings; the `max(0LL, …)` clamp is at
  919-920; tmpfs `nr_inodes`/`size`/xattr/unlimited wording matches `tmpfs.rst:83-101`; `f_frsize` fill
  (statfs.c:67-68) and `f_favail == f_ffree` (statvfs.3:228-234) hold on all five host mounts.
- **Method note** — `lsp` unavailable in this runtime (`read xd://lsp` → no such tool); all citations are
  literal source-copy inspection. No vote lines emitted (this seat is not in the `Mo55En01`–`Mo55En12` set).
