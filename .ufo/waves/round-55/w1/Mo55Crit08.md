# Mo55Crit08 — C2 claim attack B: rows 9–16 vs XFS/btrfs source

- Seat: Mo55Crit08 (critic, C2 attack lane B). Round 55, w1.
- Scope: claim-table rows 9–16 of `corpus/knowledge/disk-runway-enospc-r55.md` (rows 9–12 XFS via S537, rows 13–16 btrfs via S538). Free/reserve interpretation challenged against pinned source context.
- Evidence base: pinned copies at `corpus/evidence/sources-r55/`, verified against `corpus/SOURCES.md` pins.
- No C1/C2 votes emitted (critic seat). All line refs are lane-relative.

## Provenance check

Commands run (cwd fleet root):

```
$ cd mori-shokunin/corpus/evidence/sources-r55 && sha256sum xfs_super.c.v7.3 btrfs_super.c.v7.3
0f806bf4ea1859a482d8a7031e2e4c2a80835b3bdd15a4d5fb2ae11c91eed831  xfs_super.c.v7.3
6715b89d60575dd4438710fab318c1a3f501f2df3b5c5c1d142ebc3c5eee43fc  btrfs_super.c.v7.3
```

Both match the S537/S538 pins in `corpus/SOURCES.md:317-318`. Repo HEAD `b8a70ad` sits on top of frozen data commit `b8b7064c`. Provenance clean.

## Row-by-row attack

### Row 9 — XFS f_bavail = f_bfree (ledger :19)

Claim: handler "explicitly assigns its available-block field to the same value as its reported free-block field". Source: `xfs_super.c.v7.3:999-1003` — comment "XFS does not distinguish between blocks available to privileged and unprivileged users." then `st->f_bavail = st->f_bfree; return 0;`. Quote is verbatim and stitching-accurate. Assignment happens after the RT-device override (`xfs_statfs_rt`, :938-943) and after the project-quota adjustment (`xfs_qm_statvfs`), so the equality holds for whatever f_bfree holds at return, including RT-reporting mounts. **Survives.** No defect.

### Row 10 — XFS f_bfree = max(0, fdblocks − unavailable) (ledger :20)

Claim verified at `xfs_super.c.v7.3:918-920`: `/* make sure st->f_bfree does not underflow */ st->f_bfree = max(0LL, fdblocks - xfs_freecounter_unavailable(mp, XC_FREE_BLOCKS));`. Quote verbatim. Attack surface: this is the data-device path (`xfs_statfs_data`). When the queried inode carries RTINHERIT/REALTIME on a realtime mount, `xfs_statfs_rt` (:938-943) overwrites `f_bfree` with `xfs_rtbxlen_to_blen(...)` — no unavailable-subtraction and no `max(0LL,...)` clamp there. Also, on the data path, `f_blocks` is already net of the internal log (`st->f_blocks = sb_dblocks - xfs_internal_log_size(mp)`, :927-928), so "free space" is relative to a log-shrunken total the claim does not mention. The claim's mechanism is accurate for the data device; as a universal statement about "XFS" it is overbroad for RT-inherit queries. **Survives with scope caveat** (see Findings F2).

### Row 11 — fakeinos inode total (ledger :21)

Claim verified at `xfs_super.c.v7.3:952-954`: `fakeinos = XFS_FSB_TO_INO(mp, st->f_bfree); st->f_files = min(icount + fakeinos, (uint64_t)XFS_MAXINUMBER);`. "Inodes already allocated plus how many more the current free blocks could hold, so that total moves with free space" — accurate paraphrase; `XFS_FSB_TO_INO` converts the *reported* (post-clamp, reserve-net) f_bfree via inode geometry. Note the ordering in `xfs_fs_statfs` (:983-994): `xfs_statfs_inodes` runs *before* the RT override, so inode totals always derive from data-device free even when the final f_bfree is replaced by RT values — the claim says "current free blocks" which matches the value of `st->f_bfree` at that point in the code. **Survives.** No defect.

### Row 12 — maxicount cap (ledger :22)

Claim: "the reported inode total is additionally capped by that maximum before free inodes are derived". Ordering verified: cap at `xfs_super.c.v7.3:955-957`, free-inode derivation at :964 (`st->f_ffree = max_t(int64_t, 0, st->f_files - (icount - ifree));`). Quote verbatim (mid-expression cut is honest). **Attack:** the very next statement, :959-961, undoes the cap in the overshoot case:

```
/* If sb_icount overshot maxicount, report actual allocation */
st->f_files = max_t(typeof(st->f_files), st->f_files, mp->m_sb.sb_icount);
```

So the reported total is NOT finally bounded by maxicount: when the on-disk `sb_icount` already exceeds the configured maximum, `f_files` is raised back to actual allocation, above maxicount, and `f_ffree` is then derived from that raised value. The unsupported clause in row 12 is the implied finality "capped by that maximum" (reader infers `f_files ≤ maxicount`); the source itself documents the exception. The temporal clause ("before free inodes are derived") is true. **Overclaim, LOW severity** (edge case, source-commented; see Findings F1).

### Row 13 — btrfs reserve-as-used (ledger :23)

Claim verified at `btrfs_super.c.v7.3:1769-1778`: `f_bfree = f_blocks - (total_used/factor >> bits)`, then `/* Account global block reserve as used, it's in logical size already */` with `if (f_bfree >= block_rsv->size >> bits) f_bfree -= ...; else f_bfree = 0;` under `block_rsv->lock`. Quote verbatim (:1771). **Attack:** the magnitude clause "sits below raw unallocated capacity by that reserve" holds only while `f_bfree ≥ reserve`; the else branch clamps to 0, so the gap can exceed the reserve. Additionally the adjacent source comment warns "Mixed block groups accounting is not byte-accurate, avoid overflow" — on mixed profiles the subtraction is approximate. Substantively supported; the equality-with-reserve is an upper-bound description. **Survives with caveat** (Findings F3, INFO).

### Row 14 — zero-Avail on metadata exhaustion (ledger :24)

Quote verified at `btrfs_super.c.v7.3:1804-1806`. The actual zeroing rule is :1809-1811:

```
if (!mixed && block_rsv->space_info->full &&
    (total_free_meta < thresh || total_free_meta - thresh < block_rsv->size))
        buf->f_bavail = 0;
```

The claim as written ("once its metadata profile can take no further chunk allocations") states one conjunct of a three-conjunct rule; the reserve-fit conjunct is correctly decomposed into row 15 and the threshold into row 16. The `!mixed` exception (mixed DATA+METADATA block groups never zero Avail via this rule) is not carried in any of rows 13–16. Per-row the quoted comment text supports the clause, and the ledger's decomposition pattern distributes the full condition across rows 14–16. **Survives as decomposed claim; INFO caveat** (Findings F4).

### Row 15 — reserve-fit requirement (ledger :25)

Verified: the zero rule's second half is `total_free_meta < thresh || total_free_meta - thresh < block_rsv->size` (:1809-1811); comment text "our global reserve will not fit in the free metadata space" (:1806-1807) is quoted verbatim. The claim's "requires the global block reserve not to fit in the remaining free metadata space" is supported, with the 4M margin (row 16) applying to the comparison. **Survives.** No defect.

### Row 16 — 4M threshold / ~2M observed delta (ledger :26)

Verified at `btrfs_super.c.v7.3:1788-1800`: comment "we apply some guesswork and compare the delta to a 4M threshold. (Practically observed delta was ~2M.)" and `thresh = SZ_4M;`. Quote verbatim (:1792). "compares remaining metadata room against a fixed four-megabyte threshold" fairly paraphrases `total_free_meta < thresh` plus the margin use `total_free_meta - thresh < rsv->size`. **Survives.** No defect.

## Summary table

| Row | Ledger line | Verdict | Severity |
|---|---|---|---|
| 9 | :19 | survives; equality holds at return incl. RT/quota overrides | — |
| 10 | :20 | survives for data device; RT-inherit path omits subtract+clamp; f_blocks net of internal log | LOW caveat |
| 11 | :21 | survives; total derives from data-device f_bfree at time of call | — |
| 12 | :22 | overclaim: maxicount cap undone by sb_icount floor at :959-961 (overshoot case) | LOW |
| 13 | :23 | survives; "below by that reserve" is an upper bound (clamp-to-0, mixed-profile inexactness) | INFO |
| 14 | :24 | survives as decomposed conjunct; `!mixed` exception absent from rows 9–16 | INFO |
| 15 | :25 | survives | — |
| 16 | :26 | survives | — |

## Findings

- **F1 — LOW — Row 12 overstates cap finality.** Unsupported clause: reported inode total "is additionally capped by that maximum" (implies `f_files ≤ maxicount`). Contradicted by `xfs_super.c.v7.3:959-961`, which floors `f_files` at `sb_icount` when the on-disk count overshot maxicount; `f_ffree` (:964) is then derived from the raised value. Smallest safe correction: append "unless the on-disk inode count already exceeds it, in which case actual allocation is reported" to row 12. Evidence: `corpus/evidence/sources-r55/xfs_super.c.v7.3:955-964`; claim at `corpus/knowledge/disk-runway-enospc-r55.md:22`.
- **F2 — LOW — Row 10 generality caveat.** The unavailable-subtraction + zero clamp is the data-device path only; RT-inherit/realtime queries get `f_bfree` from `xfs_statfs_rt` (`xfs_super.c.v7.3:938-943`) with neither subtraction nor clamp, and data-path `f_blocks` is pre-shrunk by the internal log (:927-928). No falsehood for the data device; the universal "XFS" phrasing omits the RT exception. Evidence: `xfs_super.c.v7.3:918-943`; claim at `disk-runway-enospc-r55.md:20`.
- **F3 — INFO — Row 13 magnitude clause is an upper bound.** When `f_bfree < reserve`, the reported figure is 0, a gap larger than the reserve (:1776-1777); mixed-profile accounting is "not byte-accurate" (:1772). Direction and mechanism stand. Evidence: `btrfs_super.c.v7.3:1769-1778`; claim at `disk-runway-enospc-r55.md:23`.
- **F4 — INFO — Row 14 standalone incompleteness.** The zero-Avail rule requires `!mixed && full && (meta < 4M || meta − 4M < rsv)` (`btrfs_super.c.v7.3:1809-1811`); rows 14–16 distribute the condition, but the mixed-block-group exception is carried nowhere in rows 9–16. Per-row decomposition is internally consistent, so this is a coverage note, not an overclaim. Evidence: `btrfs_super.c.v7.3:1809-1811`; claim at `disk-runway-enospc-r55.md:24`.

No votes emitted (critic seat). Strongest available counterexample is F1; it is a fixable precision defect, not a tradeoff requiring rejection. Rows 9, 11, 15, 16 show no defect under attack.
