# Mo55Rev01 — btrfs zero-Avail decision (v7.3): reconstruction and prose tests

Seat Mo55Rev01, leaf revenger, lane mori-shokunin. Detection and report only: no production edits, no git/jj
mutation, no host changes, no spawn. Measured revision `b8b7064c2b54c8b6b22c288232a96c43fae1af47` (data rev);
entering tip `ca52426ea496bc6592e3e867cc9d28843e45f196`. Scratch `/fast/scratch/hyaku/mori-r55/Mo55Rev01`
(created, used, removed before yield). This seat casts no votes; nothing here is a vote line.

## 0. Integrity and measurement receipt

```
$ /home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status        # exit 0; /fast 26% used, 594.6G free
$ git -C mori-shokunin rev-parse --show-toplevel                          # /home/vgpnk/Projects/shokunin/mori-shokunin
$ git -C mori-shokunin log --oneline -1                                   # b8a70adf round-55: publish w1 ready marker
$ sha256sum corpus/evidence/sources-r55/btrfs_super.c.v7.3
6715b89d60575dd4438710fab318c1a3f501f2df3b5c5c1d142ebc3c5eee43fc   # == freeze pin for S538
$ sha256sum corpus/evidence/sources-r55/btrfs_sysfs.c.v7.3
098cb522131501deabde61ffcdc56138a8516098f4e980f9c34cb9e62b467377   # == freeze pin for S539
$ git show b8b7064c:corpus/evidence/sources-r55/btrfs_super.c.v7.3 | sha256sum   # same 6715b89d…
$ git show b8b7064c:corpus/evidence/sources-r55/btrfs_sysfs.c.v7.3 | sha256sum   # same 098cb522…
$ python3 .ufo/waves/round-55/count-c2.py b8b7064c2b54c8b6b22c288232a96c43fae1af47   # exit=1
C2=unmet claims=23 located=23 quote_missing=0 bad_rows=0 sources=9 source_rows=ok pins=ok provenance=ok entailed=0 dissent=0 rev=b8b7064c2b54c8b6b22c288232a96c43fae1af47 failed=entailment
```

The counter output at the measured rev reproduces the contract's data read except the rev field (see D7:
`.ufo/waves/round-55/evidence/c2-at-data.txt` records `rev=f70051dd…`, an earlier revision, with otherwise identical
counts). All entry text below is read as `git show b8b7064c:corpus/knowledge/disk-runway-enospc-r55.md`; the worktree
copy is dirty (D6) and is not the measured object.

## 1. Surface and call site

- S538 = `corpus/evidence/sources-r55/btrfs_super.c.v7.3`, pin `6715b89d…`; S539 =
  `corpus/evidence/sources-r55/btrfs_sysfs.c.v7.3`, pin `098cb522…`.
- Registration: `btrfs_super.c.v7.3:2540` — `.statfs = btrfs_statfs` in `btrfs_super_ops` (2530–2545). Handler body:
  1707–1830. VFS zeroes the reply buffer before dispatch (S536 `statfs.c.v7.3`, dependency of row 2, not this seat's
  surface), so every field the handler omits reaches the caller as zero.
- Handler sets only `f_blocks`, `f_bfree`, `f_bavail`, `f_type`, `f_bsize`, `f_namelen`, `f_fsid` (1767–1830).
  `grep -n "f_files\|f_ffree\|f_favail"` over both pinned btrfs copies returns nothing, so btrfs supplies **no** inode
  capacity; host `f_files=f_ffree=0` follows from the VFS memset, not from an exhausted inode table.

## 2. Reconstructed decision (v7.3 source, exact)

Units: `bits = fs_info->sectorsize_bits`; all block counts are shifted by `bits`; `f_bsize = sectorsize` (1814).
`factor = 1`, set from the populated raid types of each DATA space_info via `btrfs_bg_type_to_factor` (1746–1750).
`block_rsv = &fs_info->global_block_rsv`, guard `G = block_rsv->size` bytes (1731; comment 1771: "it's in logical size already").

Space-info census (1737–1765), one pass over `fs_info->space_info`:

```
total_free_data += disk_total - disk_used            (DATA space_info, subgroup != DATA_RELOC, 1738–1744)
                 -= btrfs_account_ro_block_groups_free_space(found)          (1743–1744)
mixed            = true if a space_info carries DATA **and** METADATA (1756–1758)
total_free_meta += disk_total - disk_used            (METADATA-only space_info, 1759–1761)
total_used      += disk_used                         (all space_info, 1764)
```
`disk_total`/`disk_used` are the physical (profile-multiplied) counters, not `total_bytes`/`bytes_used` (logical).

Reported figures:

```
f_blocks = (super_total_bytes / factor) >> bits                                   (1767–1768)
f_bfree  = f_blocks - ((total_used / factor) >> bits)                             (1769)
           lock(&block_rsv->lock):
             f_bfree -= G >> bits   if f_bfree >= G >> bits
             f_bfree  = 0           otherwise                                     (1771–1778)
f_bavail = ((total_free_data / factor) + (device_unalloc / factor)) >> bits       (1780–1785)
```
`device_unalloc` = `btrfs_calc_avail_data_space` (1603–1705): per device `avail = rounddown(total_bytes - bytes_used,
BTRFS_STRIPE_LEN)`; devices with `avail <= BTRFS_DEVICE_RANGE_RESERVED + min_stripe_size` are skipped; otherwise
`avail -= BTRFS_DEVICE_RANGE_RESERVED`; descending sort, greedy stripe allocation (`* num_stripes`, 1694–1697).

Zero-Avail rule (1800–1811), with `thresh = SZ_4M` (1800) and `M = total_free_meta`:

```
zeta  <=>  !mixed  AND  block_rsv->space_info->full
           AND ( M < thresh  OR  M - thresh < G )                                 (1809–1811)
zeta  =>  buf->f_bavail = 0
```
Consequences:
- For `M >= thresh` the rule is `M < G + thresh`; on this host (`G = 536,870,912`) the boundary is
  `M0 = G + 4 MiB = 541,065,216` bytes. Verified truth table: `M=G+4MiB-1` fires, `M=G+4MiB` does not.
- The first disjunct is load-bearing, not decorative: in C the second operand is not evaluated when `M < thresh`
  (short-circuit), so the unsigned `M - thresh` never wraps. Written in the reverse order the same values would make
  a full metadata space_info report positive Avail. [INFERENCE from C unsigned semantics; the source text at
  1809–1811 is the observed order.]
- `!mixed` is semantic: on a mixed-bg profile the metadata space_info also carries DATA, `mixed = true`, and
  `total_free_meta` stays 0 (1756–1761). Without the guard, `M = 0 < thresh` would zero Avail on a filesystem whose
  metadata is accounted inside data.
- The rule mutates `f_bavail` only; `f_bfree` is untouched. Avail can therefore be zero from the data term alone,
  with or without the metadata rule; and `f_bfree` can reach zero independently via the reserve clamp.
- `!mixed` and `full` are the same conditions as `block_rsv->space_info->full`; `block_rsv->space_info` being the
  METADATA space_info, `btrfs_super_total_bytes` reading the super block total, and the setter/clearer of `full` live
  in files not pinned this round (`block-rsv.c`, `ctree.h`/`volumes.h`, `space-info.c`). Those three points are
  [INFERENCE], supported only by the handler's own comment 1803–1807 ("chunks for our metadata profile … If we
  aren't ->full then we still can allocate chunks").

## 3. Live falsification on the host (read-only)

Kernel 7.2.11-arch1-1, btrfs on `/` (uuid `1d02a454-…`), sectorsize 4096, metadata profile DUP. One Python process
read `os.statvfs("/")` and `/sys/fs/btrfs/<uuid>/allocation/{data,metadata,system}/{total_bytes,bytes_used,
disk_total,disk_used}` plus `global_rsv_size`; the model was recomputed from those inputs:

```
statvfs  f_bsize=4096 f_blocks=243661568 f_bfree=163970261 f_bavail=154623293 f_files=0 f_ffree=0
sysfs    data      total=277033779200 used=242226049024 disk_total=277033779200 disk_used=242226049024
         metadata  total=61203283968  used=41826271232  disk_total=122406567936 disk_used=83652542464
         system    total=33554432     used=65536        disk_total=67108864     disk_used=131072
         global_rsv_size=536870912
model    f_bfree  = 243661568 - (325878722560/4096) - (536870912>>12) = 163970261   residual 0
model    f_bavail = 8497981 + (598530326528 rounded down to 64KiB)/4096 - 1MiB/4096 = 154623293   residual 0
```
Six consecutive samples 150 ms apart gave residual 0 for both figures (free counters moved with concurrent fleet
writes; the model tracked each sample exactly). This falsifies any reading that statfs consumes the logical
`total_bytes`/`bytes_used` pair: on this DUP metadata profile `disk_used = 2 x bytes_used`, and a logical-counter
model is off by ~41.8 GB (10.2 million blocks).

Zero-rule inputs on the host: `M = 122,406,567,936 - 83,652,542,464 = 38,754,025,472` bytes;
`G + 4MiB = 541,065,216`; `M >> G + 4MiB`, so the rule is false and Avail is nonzero — as observed. The host's
`metadata` space_info `full` flag is not exported (section 5, D2), so that conjunct is inference on this host.

## 4. Prose conditions tested (rows 13–19; rows 1–12, 20–23 outside this seat)

Mechanical check at `b8b7064c`, per row: cited span located in the pinned copy (whitespace-collapsed substring),
uniqueness within the claim table, word count 6–25, claim hash recomputed from the entry:

```
row=13 src=S538 hash=f26a22184676 words=11 located=True unique=True
row=14 src=S538 hash=51e630031934 words=22 located=True unique=True
row=15 src=S538 hash=5961ec3475c0 words=20 located=True unique=True
row=16 src=S538 hash=c159bdf1a5a9 words=10 located=True unique=True
row=17 src=S538 hash=1b8e15e9537e words=14 located=True unique=True
row=18 src=S539 hash=a179fcbe3d08 words=6  located=True unique=True
row=19 src=S539 hash=efba48156572 words=8  located=True unique=True
```

| row | condition as written | test against 1720–1830 / 672–1045 | verdict |
|---|---|---|---|
| 13 | global block reserve counted as consumed; free figure below raw capacity by the reserve | 1771–1778 subtracts `G>>bits` from `f_bfree` under the reserve lock, clamp to 0. Host: pre-reserve 164,101,333 vs reported 163,970,261 blocks = exactly 131,072 blocks = 512 MiB = `G` (sample in §3). Clamp means below-`G` free reports 0, not negative | holds (for `f_bfree`; `f_bavail` is not reduced by `G`) |
| 14 | zero Avail once the metadata profile can take no more chunks | `block_rsv->space_info->full` is necessary (1809) but the rule also needs the metadata branch (1810) and `!mixed` (1809). `mixed` omitted; "once" reads as sufficient | necessary-not-sufficient as phrased; mixed guard omitted (D5) |
| 15 | the rule "also requires" the global reserve not to fit in remaining metadata space | The enforcing clause is `M - thresh < G`, i.e. `G > M - 4MiB`, and only when `M >= 4MiB`. Counterexample with `G=2MiB, M=3MiB`: rule fires (branch 1) while `G <= M` — the reserve *does* fit | holds for `G >= 4MiB` (host: 512 MiB); literal universal reading false, boundary off by `thresh` (D3) |
| 16 | exhaustion test compares remaining metadata room against a fixed 4 MiB, chosen because the observed gap was ~2 MiB | `thresh = SZ_4M` at 1800 and comment 1792 "Practically observed delta was ~2M" both hold. But the operating comparison at 1810 is `delta = M - G` against 4 MiB (comment 1788–1792: "remaining metadata space minus global reserve … compare the delta to a 4M threshold"); only the short-circuit branch compares `M` itself to 4 MiB | constant and rationale hold; "remaining metadata room" is the delta after the reserve, not `M` (D4) |
| 17 | Avail zero does not guarantee every write fails; small metadata operations can still succeed | comment 1794–1797: "some operations that consume a few metadata will succeed even if the Avail is zero" | holds as source-stated; not observable here (no ENOSPC forcing permitted) — unverified live |
| 18 | per-space-type allocated total and used bytes are separate sysfs counters, with pinned/reserved/may-use | `SPACE_INFO_ATTR(total_bytes|bytes_used|bytes_pinned|bytes_reserved|bytes_may_use|bytes_readonly)` at 896–908; attrs array 1023–1045. Note `disk_used`/`disk_total` are also exported (904–905, 1032–1033) and are the pair statfs actually reads | holds; the guidance sentence built on it is incomplete (D1) |
| 19 | global-reserve size published under the allocation directory, read under the reserve's own lock | 672–679: `btrfs_show_u64(&block_rsv->size, &block_rsv->lock, buf)` in `global_rsv_size_show`, `BTRFS_ATTR(allocation, global_rsv_size, …)`; listed in `allocation_attrs[]` (1066–1068), created on `space_info_kobj` (2345), path map `/sys/fs/btrfs/<uuid>/allocation` at line 37; locking helper 661–669. Host path exists and was read (`allocation/global_rsv_size = 536870912`) | holds |

Decision-table rows tied to this surface, tested:
- "btrfs reports low/zero Avail with nonzero ordinary free blocks → metadata/global reserve may be limiting": the
  metadata rule does not read `f_bfree`, so zero Avail + nonzero `f_bfree` is consistent with the rule but does not
  establish it; data-term exhaustion and the rule are independent paths to zero. The hedge "may" is correct; the
  prescribed reads are not sufficient (D1, D2).
- "btrfs `df -i` zero total/free is not evidence of inode exhaustion": confirmed source-side — no `f_files`/`f_ffree`
  assignment exists in the pinned handler, so the zero comes from the VFS memset.

## 5. Divergences found

- **D1 (medium, guidance):** the entry's btrfs decision row tells the operator to read
  `allocation/{data,metadata,system}/{total_bytes,bytes_used,…}`. The handler reads `disk_total`/`disk_used`
  (1742, 1760, 1764). On this host metadata is DUP: logical `M = 19,377,012,736` vs physical `M = 38,754,025,472`
  (ratio 2.0). An operator using the prescribed pair misjudges the distance to the zero boundary by 2x. Evidence:
  `btrfs_super.c.v7.3:1742,1760,1764` vs `btrfs_sysfs.c.v7.3:1025–1026,1032–1033`; live sample §3. The captured
  snapshot itself recorded only `{total_bytes,bytes_used}` (`evidence/host-disk-snapshot.txt:26–33`), so the pinned
  host observation cannot reproduce the handler's inputs at all.
- **D2 (medium, observability):** the primary conjunct `block_rsv->space_info->full` has no sysfs attribute in v7.3
  (`space_info_attrs[]`, `btrfs_sysfs.c.v7.3:1023–1045`; `grep -n full` over the copy hits only comments at 251,
  1114). The trigger cannot be confirmed from the counters the entry prescribes; only the symptom (Avail 0 with
  nonzero `f_bfree`) is observable.
- **D3 (low, precision):** row 15's "reserve not to fit in remaining metadata space" understates the enforcing clause
  by `thresh` and ignores the `M < thresh` branch (counterexample in §4). Correct statement: for `M >= 4MiB` the rule
  is `M < G + 4MiB`; for `M < 4MiB` it fires with no reserve comparison. Evidence:
  `btrfs_super.c.v7.3:1809–1811`.
- **D4 (low, precision):** row 16 names `M` where the operating branch compares `M - G` (the comment's "delta") with
  4 MiB. Evidence: `btrfs_super.c.v7.3:1787–1792,1809–1810`.
- **D5 (low, precision):** row 14 omits `!mixed`, which is semantic (mixed-bg profiles keep `M = 0` by construction,
  1756–1761) and "once" presents a necessary condition as a trigger. Evidence: 1756–1761, 1809.
- **D6 (data provenance, medium for seat conduct):** the worktree
  `corpus/knowledge/disk-runway-enospc-r55.md` is modified against HEAD and against the measured rev: row 4's claim
  reads "unprivileged **user** may still use" with hash `45120996891a` and its cited span is
  `fsblkcnt_t f_bavail; /* Free blocks available to unprivileged user */`, while `b8b7064c` (and the frozen
  `evidence/c2-claims.txt`) carry "unprivileged **process**", hash `22a23e3fb849`, and a two-field span. A seat that
  reads the file rather than `git show <rev>:` votes on different text than the counter hashes. Not mine to alter
  (no production edits this seat). Evidence: `git diff b8b7064c -- corpus/knowledge/disk-runway-enospc-r55.md`;
  `git status --porcelain` shows ` M corpus/knowledge/disk-runway-enospc-r55.md`.
- **D7 (low, receipt):** `evidence/c2-at-data.txt` records `rev=f70051ddcb903dc6c4393c410f8bab054951af82`, not the
  data rev named by the contract/prompt (`b8b7064c`). The counter output at `b8b7064c` is identical in every field
  except `rev`, but the at-data receipt does not evidence the measured rev. Evidence: counter run in §0.
- **D8 (low, snapshot consistency):** the entry's "On this host" prose and the cited
  `evidence/host-disk-snapshot.txt` disagree: `/` bfree 164,023,017 vs 164,012,985; `f_bavail` 154,680,289 vs
  154,665,001; metadata `bytes_used` 41,834,954,752 vs 41,824,190,464; `/fast` free 147,466,003 vs 155,927,507 and
  `df -P` 30% vs 26%; `/tmp` free 32,795,798 vs 32,795,553 and free inodes 67,005,211 vs 67,004,121. Both are labeled
  point-in-time on the same date; only the captured file is reproducible. Evidence: committed entry line 50
  (`git show b8b7064c:corpus/knowledge/disk-runway-enospc-r55.md`) and `evidence/host-disk-snapshot.txt:3–8,10–15,
  26–33`.

## 6. Limits and confidence

- High confidence in the v7.3 decision logic: read directly from the pinned copy; every branch and unit is cited;
  entry hashes and cited spans verified at the measured rev; pins match.
- High confidence that the host's statfs implements this arithmetic: residual exactly 0 for both `f_bfree` and
  `f_bavail`, including the 1 MiB `BTRFS_DEVICE_RANGE_RESERVED` and the 64 KiB stripe rounding, across six samples.
  The host runs 7.2.11 while the pinned copy is v7.3; the exact residual shows behavioural identity of the two
  figures, not byte identity of the two kernels.
- Medium confidence in `space_info->full` semantics (`block-rsv.c`/`space-info.c` not pinned) and in `total_bytes`
  naming of the super total: both marked [INFERENCE].
- Unverified by design: row 17's "writes can still succeed at Avail 0" (no ENOSPC replication allowed); the
  `full`-flag transition; mixed-bg behaviour (no mixed filesystem on this host).

## Findings

- **Medium — D1:** entry's btrfs decision row prescribes logical `total_bytes`/`bytes_used` while `btrfs_statfs` reads
  physical `disk_total`/`disk_used`; on the host's DUP metadata the two differ 2x (19.38 GB vs 38.75 GB).
  Evidence: `corpus/evidence/sources-r55/btrfs_super.c.v7.3:1742,1760,1764`,
  `corpus/evidence/sources-r55/btrfs_sysfs.c.v7.3:1025–1033`, live sample §3.
- **Medium — D2:** `block_rsv->space_info->full` (primary zero-Avail conjunct) is not exported by v7.3 sysfs, so the
  prescribed counters cannot confirm the trigger. Evidence: `btrfs_sysfs.c.v7.3:1023–1045`; `btrfs_super.c.v7.3:1809`.
- **Medium — D6:** worktree entry row 4 diverges from the measured rev and from the frozen claims snapshot
  (claim hash `45120996891a` vs `22a23e3fb849`), so file-readers and rev-readers vote on different text.
  Evidence: `git diff b8b7064c -- corpus/knowledge/disk-runway-enospc-r55.md`.
- **Low — D3:** row 15's reserve clause is off by the 4 MiB threshold and ignores the short-circuit branch; exact
  boundary `M < G + 4MiB` for `M >= 4MiB`. Evidence: `btrfs_super.c.v7.3:1809–1811`.
- **Low — D4:** row 16 compares `M` where the operating branch compares `M - G` (comment's "delta") to 4 MiB.
  Evidence: `btrfs_super.c.v7.3:1787–1792,1809–1810`.
- **Low — D5:** row 14 omits the semantic `!mixed` guard and reads a necessary condition as sufficient.
  Evidence: `btrfs_super.c.v7.3:1756–1761,1809`.
- **Low — D7:** `evidence/c2-at-data.txt` names `rev=f70051dd…`, not the measured `b8b7064c`; counts identical.
- **Low — D8:** entry "On this host" prose and the cited snapshot file publish different readings (seven values
  listed in §5). Evidence: committed entry lines 50–52; `evidence/host-disk-snapshot.txt`.
- **Info:** rows 13, 18, 19 hold as written against the pinned sources; rows 14–16 hold only with the qualifications
  in §4. Row 17 is source-supported and unverified live.
