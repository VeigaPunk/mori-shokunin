# RevengeStDev — why btrfs st_dev differs from mountinfo major:minor at v7.2, and what the C2 `device_check` rule mishandles

Seat: `MadoR22-2.RevengeStDev-8` (leaf, revenger). Date: 2026-10-21. Detection and report only.
Reconstructed from Linux v7.2 sources only. No live host probes beyond nothing — every claim below is static
source evidence; runtime-dependent statements are tagged `[INFERENCE]`. No installs, no tool updates
(tooling directive record: nothing installed; fetches via stock `curl` into the scoped scratch dir only).
No debt carried or cleared by this seat; existing open debt untouched.

Godspeed axes: (A) anchor precision — exact file:line from pinned v7.2 bytes; (B) causal completeness — the full
stat(2) → st_dev chain and the mountinfo emission chain; (C) rule failure-mode coverage — every reachable
misbehavior of `device_check`; (D) fetch economy — 16 files, no tree clone.

## 0. Artifacts and provenance

Fetched to `/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/round23/RevengeStDev/src/` (v7.2 tags,
kernel.org cgit plain; fallback raw.githubusercontent not needed):

| file | sha256 (prefix) |
|---|---|
| fs/btrfs/inode.c | 01a6ad07c09cd1a0… |
| fs/btrfs/super.c | d1731b24b5c1e134… |
| fs/btrfs/disk-io.c | aa40ed0700e8de5a… |
| fs/btrfs/ctree.h | e8bbcaa60f262566… |
| fs/stat.c | 47d331643ef846d0… |
| fs/super.c | e55ec2a5e2916c47… |
| fs/proc_namespace.c | fd82c0db52055ae8… |
| fs/namespace.c | 3c2417e6bd81a82d… |
| fs/ext4/inode.c | 6b39727851b3a0f9… |
| fs/ext4/super.c | 4cae23697c957723… |
| fs/xfs/xfs_iops.c | b72074a39adfd6b0… |
| fs/xfs/xfs_super.c | 0a95697dcfcdab8f… |
| mm/shmem.c | eb5d1e9107b287c8… |
| fs/overlayfs/inode.c | 6d0e2e57670184c5… |
| fs/overlayfs/super.c | 84f52247ef79671a… |
| include/linux/fs.h | e4bf4fea744e2b33… |
| include/linux/kdev_t.h | 88c47d8d1979f2c0… |
| Documentation/filesystems/proc.rst | e760f716f8278dee… |

Cross-validation: my independent fetches reproduce the DraftSourceRows digests byte-for-byte for S081
(fs/btrfs/inode.c `01a6ad07c09cd1a0…`), S082 (proc.rst `e760f716f8278dee…`) and S078 (fs/xfs/xfs_super.c
`0a95697dcfcdab8f…`). Three-way byte identity on 2026-10-21.

## 1. Reconstructed contract (the causal chain)

Two independent numbers are being compared by `device_check`:

- **st_dev** of `os.stat(path)`: produced by the stat path, not by the mount.
- **field 3 (major:minor)** of the covering `/proc/self/mountinfo` line: produced from the superblock,
  not from the file.

Chain A — where st_dev comes from:

1. `stat(2)/lstat(2)` → `vfs_getattr` (fs/stat.c:254-263) → `vfs_getattr_nosec` (fs/stat.c:181-231).
2. fs/stat.c:210-219: if `inode->i_op->getattr` exists it is called; otherwise
   `generic_fillattr(idmap, request_mask, inode, stat)`.
3. fs/stat.c:88 — the default rule: `stat->dev = inode->i_sb->s_dev;`
4. ABI: `st_dev` reaches userspace packed (`tmp.st_dev = new_encode_dev(stat->dev)`, fs/stat.c:480 and :828;
   packing at include/linux/kdev_t.h:39-44: `(minor & 0xff) | (major << 8) | ((minor & ~0xff) << 12)`).
   statx gives it unpacked: `tmp.stx_dev_major = MAJOR(stat->dev); tmp.stx_dev_minor = MINOR(stat->dev);`
   (fs/stat.c:729-730).

Chain B — where `sb->s_dev` comes from per filesystem:

| fstype | mount path | s_dev setter | value |
|---|---|---|---|
| ext4 | `get_tree_bdev(fc, ext4_fill_super)` fs/ext4/super.c:5860 | `sget_dev` → `super_s_dev_set` → `set_bdev_super`: `s->s_dev = *(dev_t *)data` (fs/super.c:1314-1323, 1325-1329, 1608-1665) | real block device dev_t |
| xfs | `get_tree_bdev(fc, xfs_fs_fill_super)` fs/xfs/xfs_super.c:2034 | same | real block device dev_t |
| tmpfs | `get_tree_nodev(fc, shmem_fill_super)` mm/shmem.c:5060-5063 | `vfs_get_super` → `sget_fc(fc, test, set_anon_super_fc)` (fs/super.c:1260-1294) | anonymous `MKDEV(0, n)` |
| btrfs | `sget_fc(fc, btrfs_fc_test_super, set_anon_super_fc)` fs/btrfs/super.c:1906 | `set_anon_super_fc` → `set_anon_super` → `get_anon_bdev(&s->s_dev)` (fs/super.c:1228-1233) | anonymous `MKDEV(0, X)` — one per mounted btrfs filesystem |

`get_anon_bdev` (fs/super.c:1203-1221) allocates minor `1..(1<<MINORBITS)-1` from `unnamed_dev_ida` and always
returns `MKDEV(0, dev)` — major 0, minor ≥ 1 ("Many userspace utilities consider an FSID of 0 invalid", :1208-1210).
The backing bdev of a btrfs mount appears only in `sb->s_id` naming (fs/btrfs/super.c:1971-1973) and in the
f_fsid hash (:1849-1854); it never lands in `s_dev`. Teardown confirms: `btrfs_kill_super` calls
`kill_anon_super` (fs/btrfs/super.c:2154-2158), which frees the anonymous dev (fs/super.c:1235-1242).

Chain C — who overrides stat->dev after filling:

- ext4: `ext4_getattr` calls `generic_fillattr` (fs/ext4/inode.c:6263; wrapper `ext4_file_getattr` :6267-6303)
  and never writes `stat->dev`. → st_dev = real bdev.
- xfs: `xfs_vn_getattr` writes `stat->dev = inode->i_sb->s_dev;` explicitly (fs/xfs/xfs_iops.c:697), no override.
  → st_dev = real bdev.
- tmpfs: `shmem_getattr` calls `generic_fillattr` (mm/shmem.c:1316), no override. → st_dev = the tmpfs
  superblock's own anonymous dev.
- btrfs: `btrfs_getattr` (fs/btrfs/inode.c:8215-8261; wired for dirs, files, specials, symlinks at :10698,
  :10795, :10807, :10817) calls `generic_fillattr` and then **overrides**:

  ```c
  fs/btrfs/inode.c:8245-8249
  generic_fillattr(idmap, request_mask, inode, stat);
  stat->dev = BTRFS_I(inode)->root->anon_dev;

  stat->subvol = btrfs_root_id(BTRFS_I(inode)->root);
  stat->result_mask |= STATX_SUBVOL;
  ```

  `root->anon_dev` is allocated per exposed subvolume root in `btrfs_init_fs_root`
  (fs/btrfs/disk-io.c:1076-1102): every fs-tree root with `root_refs > 0` gets its own `get_anon_bdev`
  (comment: "Don't assign anonymous block device to roots that are not exposed to userspace, the id pool is
  limited to 1M", :1091-1092); it is freed in `btrfs_free_fs_root` (:1836-1838) and can be preallocated for
  snapshots via `btrfs_get_new_fs_root` (:1397-1401). Field declared at fs/btrfs/ctree.h:242.

Chain D — where mountinfo field 3 comes from (`show_mountinfo`, fs/proc_namespace.c:135-190):

```c
fs/proc_namespace.c:143-144
seq_printf(m, "%i %i %u:%u ", r->mnt_id, r->mnt_parent->mnt_id,
           MAJOR(sb->s_dev), MINOR(sb->s_dev));
```

Field 3 is `MAJOR(sb->s_dev):MINOR(sb->s_dev)` — the superblock device, printed per mount line. Bind mounts
share the superblock, so all their lines print the same field 3. The device name (via `sb->s_op->show_devname`,
:172-177; btrfs prints `latest_dev`, fs/btrfs/super.c:2428-2430) lands only in the **mount source** field
(m+3), never in field 3. The documented invariant is proc.rst §3.5 (:1965-1990):

> (3) major:minor: value of st_dev for files on filesystem

**Result:** that doc invariant holds for ext4, xfs and tmpfs and fails only for filesystems whose getattr
rewrites `stat->dev`. At v7.2 those are exactly btrfs (per-subvolume-root anonymous dev) and overlayfs
(per-layer pseudo dev, §3 below).

Per-fs truth table:

| fstype | mountinfo field 3 | st_dev | equal? |
|---|---|---|---|
| ext4 | real bdev (set_bdev_super) | same sb s_dev | always → `match` |
| xfs | real bdev | same sb s_dev | always → `match` |
| tmpfs | anon 0:N (own sb) | same sb s_dev | always → `match` |
| btrfs | anon 0:X (sb, one per fs) | per-subvol-root anon 0:Y, Y ≠ X | **never** → skip is mandatory |
| overlayfs | anon 0:X (overlay sb) | 0:X or per-layer pseudo 0:Z | per entry, §3 |

Why Y ≠ X for btrfs: both numbers come from the same global `unnamed_dev_ida` while both holders are live,
so an ida allocation is never duplicated — the superblock's anonymous minor and every subvolume root's
anonymous minor are distinct. Even the top-level subvolume (id 5) is an fs-tree root with its own `anon_dev`
(fs/btrfs/disk-io.c:1093-1102 has no exemption for id 5), so **every** path on btrfs, including the mount
root itself, reports a minor that no mountinfo line carries: all `-o subvol=` and subvolume-directory mounts
of one filesystem share the single sb (fs/btrfs/super.c:2070-2147, `mount_subvol` :1173, called at :2135),
so their mountinfo lines all carry the same 0:X while their files' st_dev differ per subvolume (0:Y, 0:Z, …).
Consequence: btrfs st_dev is a host-unique identifier of (filesystem, subvolume) while alive, but it is
**not resolvable to any mountinfo line by construction**.

## 2. What the C2 `device_check` rule gets right (verified, keep)

Per the contract: "If chosen fstype is not btrfs and its major:minor ≠ the path's st_dev → `unknown` basis
`device_mismatch`. For btrfs a mismatch is expected (per-subvolume anonymous st_dev, S081) and is recorded as
`device_check: "btrfs_subvolume_skipped"`; equal → `match`."

1. **The btrfs skip is keyed on fstype and is complete.** No btrfs stat can ever match field 3 (§1), so
   skipping is not a heuristic; it is the exact kernel truth. Keying on the mountinfo fstype string (not on
   `st_dev` major 0) is also right: major 0 is shared by tmpfs, proc, sysfs, cgroup2, fuse, nfs and overlayfs
   supers — st_dev alone cannot identify btrfs.
2. **"Last line wins" tie-break is sound at v7.2.** mountinfo lines are emitted in rbtree order of
   `mnt_id_unique` (fs/namespace.c:1536-1570 `m_start`/`m_next`; insertion ordered by
   `mnt_id_unique = ++mnt_id_ctr`, :213-222, :1086), a monotonically increasing per-namespace counter. A mount
   stacked over an existing mount point is created later, so it always sorts after the shadowed mount and is
   the last line. Path resolution uses the topmost; the rule's tie-break picks the same mount.
3. **Per-run freshness.** `free_anon_bdev` returns minors to the ida (fs/super.c:1223-1226) and field-1
   `mnt_id` is explicitly reusable ("may be reused after umount", proc.rst :1973-1974; allocated from
   `mnt_id_xa`, fs/namespace.c:213-222). Reading mountinfo and st_dev fresh per run, as the contract fixes,
   is the only sound mode; any future caching keyed on dev or column-1 mnt_id would be unsound.
4. **"match" semantics are honest for nodev fs.** For tmpfs (and proc/sysfs/fuse/nfs), field 3 and st_dev are
   the same anonymous dev — `match` correctly means "consistent with its own mountinfo line", not "block-backed".

## 3. Edge cases the rule mishandles or misdescribes

M1 — **overlayfs (including overlay-on-btrfs mixes): `device_mismatch` false alarm.**
`ovl_getattr` (fs/overlayfs/inode.c:163-273) first gets real-fs attrs, then `ovl_map_dev_ino` (:104-152)
rewrites dev/ino: all-layers-same-fs → `stat->dev = dentry->d_sb->s_dev` (:108); xino-mapped → same (:122);
directories always → overlay sb dev (:141); **non-directory fallback → `stat->dev = ofs->fs[fsid].pseudo_dev`**
(:150), a per-distinct-layer-fs anonymous dev from the same pool (fs/overlayfs/super.c:980-991 lowerpath,
:1041-1049 fs[0]). Consequences for the rule:
- Single-fs overlay on btrfs (one upper, lowers on the same fs): every entry reports the overlay sb's anon
  dev → `match` vs the overlay mountinfo line. Benign — but the match certifies overlay-sb identity, not any
  quota-relevant device; the underlying btrfs qgroup state is invisible (contract limit "no overlay/fuse
  quota" is correct and load-bearing).
- Multi-fs overlay (e.g. lower on btrfs `/home`, upper on ext4/tmpfs) with xino unusable for an entry
  (`stat->ino` overflowing the xinobits window, :110-127) or xino off: non-dir entries report `pseudo_dev`,
  which appears in **no** mountinfo line → the rule classifies fstype `overlay` and records
  `device_check: "device_mismatch"`. The verdict is already `unknown`/`unsupported_fstype`, so the exit
  code is right, but the recorded basis misattributes a structural layering property to a device problem,
  and `device_check` flips between `match` (dirs) and `device_mismatch` (files) within one mount. If any
  consumer ever treats `device_mismatch` as "host state suspicious", this is a false signal.

M2 — **bind mounts: no false verdicts, one latent trap.** A bind mount never changes the superblock, so
field 3 is invariant across bind lines: btrfs binds stay fstype btrfs → skipped; ext4/xfs/tmpfs binds stay
`match`. The trap is ordering-derived: the soundness of "last line wins" rests on v7.2's rbtree-by-`mnt_id_unique`
emission order (§2.2). That holds per mount namespace and per read. Column 1 (`mnt_id`) is **not** the sort key
and is reusable — a future variant that orders or dedups by column 1, or that reads mountinfo in chunks assuming
creation order across namespaces, breaks the tie-break. Also note the doc says field 3 is "value of st_dev for
files on filesystem" — for a bind of a subdirectory, field 4 (root) is the subdirectory while field 3 is still
the whole sb's dev; that is consistent here only because s_dev is per-sb, not per-mount.

M3 — **st_dev is packed; naive integer comparison misfires for minors > 255.** `os.stat().st_dev` on Linux is
`new_encode_dev`-packed (fs/stat.c:480, :828; include/linux/kdev_t.h:39-44). An anonymous minor like 300
(routine: tmpfs/btrfs-subvol/container churn in a 2^20-wide pool) packs to `(300&0xff) | (0<<8) | ((300&~0xff)<<12)`
= 1048620 ≠ 300. Comparing `st_dev` directly against `major*1000+minor`, minor-only, or a naive `int("MAJ:MIN")`
derived value fails. Correct unpack is `os.major(st_dev)` / `os.minor(st_dev)`; statx `stx_dev_major/minor`
(fs/stat.c:729-730) needs no unpack. This is the top practical `device_check` bug class on non-btrfs anon fs
(tmpfs), and the fixture string form ("MAJ:MIN") does not exercise it — real mode does.

M4 — **`0:0` is a sentinel, never a real st_dev.** `get_anon_bdev` allocates from 1 (fs/super.c:1208-1219).
st_dev `0:0` therefore means an unpacking bug (M3) or a btrfs root whose `anon_dev` was never assigned
(non-exposed roots keep 0, fs/btrfs/disk-io.c:1093-1102) — the latter should not be stat-able through any
normal path `[INFERENCE]`.

M5 — **btrfs `device_check` value space is degenerate.** `btrfs_subvolume_skipped` fires for **every** btrfs
path; no btrfs comparison can ever yield `match` or `device_mismatch` (§1). The name says "subvolume" but the
top-level (id 5) is included. Reported so no oracle treats `match`-under-btrfs as reachable.

M6 — **kernel capabilities the rule cannot use this wave (frontier note, report-only).** v7.2 statx exposes
`stx_subvol` (fs/stat.c:735; populated by btrfs, fs/btrfs/inode.c:8248-8249) — `STATX_SUBVOL` in the result
mask is a direct "this path has btrfs subvolume semantics" signal with the subvol id, strictly stronger than
the fstype string; `STATX_MNT_ID` / `STATX_MNT_ID_UNIQUE` (fs/stat.c:303-308) and statmount/listmount
(fs/namespace.c:5319-5324) identify the exact covering mount without prefix heuristics. The contract fixes this
wave's input set (`os.stat`, mountinfo, sysfs); these are inputs for a later round, not a change now.

M7 — **FR2-adjacent exhaustion, one line, out of scope.** All anonymous devs — every anon sb (tmpfs, proc,
…), every exposed btrfs root, every overlay layer — share the 1M-slot `unnamed_dev_ida` (fs/super.c:1211;
fs/btrfs/disk-io.c:1091-1092 comment; fs/overlayfs/super.c:981, 1046); exhaustion fails mount/subvolume
creation with `-EMFILE`, invisible to `df`. Noted for the FR2 frontier; not a device_check issue.

## 4. Reachable `device_check` outputs on a real host (truth set)

- `match`: ext4, xfs, tmpfs, and every other single-sb fs (proc, sysfs, cgroup2, fuse, nfs, samefs overlay).
- `btrfs_subvolume_skipped`: every btrfs path, always.
- `device_mismatch`: only overlayfs entries whose dev falls back to layer `pseudo_dev` (M1). Nothing else at
  v7.2 produces a true mismatch for the covering mount of a non-btrfs path.

## 5. Confidence

High for §1-§2 and M1-M5: every claim is anchored to exact v7.2 lines from byte-verified fetches (three digests
independently cross-validated against S078/S081/S082). `[INFERENCE]`-tagged: M4's reachability of anon_dev-0
roots via normal paths, and any statement about runtime timing (id reuse windows, exhaustion) — static sources
pin the mechanism, not the schedule. No live probes were made; none were permitted.

## 6. Evidence index (anchor → file:line at v7.2)

- default st_dev: fs/stat.c:88; getattr dispatch: fs/stat.c:210-219; vfs_getattr: :254-263
- ABI packing: fs/stat.c:480, :828; include/linux/kdev_t.h:39-44; statx unpacked: :729-730; stx_subvol: :735; mnt_id: :303-308
- anon bdev: fs/super.c:1203-1221 (get_anon_bdev, MKDEV(0,dev), ida 1..2^20-1), :1223-1226 (free), :1228-1233 (set_anon_super), :1235-1242 (kill_anon_super), :1260-1294 (vfs_get_super/get_tree_nodev), :1314-1329 (set_bdev_super/super_s_dev_set), :1608-1665 (get_tree_bdev_flags/sget_dev)
- btrfs override: fs/btrfs/inode.c:8245-8249; ops wiring :10698/:10795/:10807/:10817; per-root alloc fs/btrfs/disk-io.c:1091-1102; free :1836-1838; snapshot prealloc :1397-1401; field fs/btrfs/ctree.h:242
- btrfs anon sb: fs/btrfs/super.c:1906 (sget_fc + set_anon_super_fc), :1971-1973 (bdev only for s_id), :1849-1854 (f_fsid), :2070-2147 + :1173/:2135 (subvol mounts share the sb), :2154-2158 (kill_anon_super), :2428-2430 (source-field devname)
- comparators: fs/ext4/inode.c:6263 (+ wrapper :6267-6303); fs/xfs/xfs_iops.c:697; mm/shmem.c:1316; trees: fs/ext4/super.c:5860, fs/xfs/xfs_super.c:2034, mm/shmem.c:5060-5063
- overlayfs: fs/overlayfs/inode.c:104-152 (map_dev_ino; pseudo_dev at :150), :163-273 (ovl_getattr); layer pseudo dev alloc fs/overlayfs/super.c:980-991, :1041-1049
- mountinfo: fs/proc_namespace.c:143-144 (field 3 = sb s_dev), :172-177 (source field devname); doc proc.rst:1965-1990 (§3.5, field (3) = "value of st_dev for files on filesystem", field (1) reuse)
- order/tie-break: fs/namespace.c:213-222 (mnt_id reusable, mnt_id_unique = ++ctr), :1086 (rbtree key), :1536-1570 (mountinfo iteration order), :5319-5324 (statmount ids)
