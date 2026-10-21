# SimplifyRules — contract §C2 quota classification table

Seat: `MadoR22-2.SimplifyRules-8`  
Authority: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/contract.md` (frozen lane commit `4dc80c1be48308075e83af17f15fbfe7e95e6cb8`), §C2 lines 105–122 plus mount preamble 95–103.  
Tool installs: none.

## Godspeed axes

| Axis | This pass |
|------|-----------|
| Outcome equivalence | Every table row maps to one branch; order fixes silent overlaps. |
| Procedure size | One fstype dispatch; XFS as ordered predicates, not five prose rows. |
| Determinism | Explicit first-match where the table’s English overlaps (XFS R3 vs R5). |
| Observable contract | `quota_state`, `enforcement`, `basis` unchanged; no new outcomes invented. |

## Key sets (super options: comma-split, key = text before `=`)

```text
XFS_Q   = {usrquota, uquota, quota, grpquota, gquota, prjquota, pquota}
XFS_NE  = {uqnoenforce, gqnoenforce, pqnoenforce, qnoenforce}
EXT_Q   = {quota, usrquota, grpquota, prjquota, usrjquota, grpjquota}
TMPFS_Q = {quota, usrquota, grpquota}
TMPFS_H = any key k where k.endswith("_hardlimit")
```

`quota_option_keys` (output): sorted keys from the union relevant to the resolved fstype (XFS: `XFS_Q ∪ XFS_NE ∪ {noquota}`; ext: `EXT_Q`; tmpfs: `TMPFS_Q` plus any `*_hardlimit` keys present). btrfs classification ignores super-option quota keys; `btrfs_qgroups_mode` comes from sysfs separately.

## Preconditions (before the table; not rows in the table)

Per path, after mountinfo parse + longest mount point (ties: **last** line wins):

1. No covering mount → `(quota_state=unknown, enforcement=n/a, basis=no_covering_mount)`; `fstype`/`mount_point` null.
2. Non-btrfs and mount major:minor ≠ path `st_dev` → `(unknown, n/a, device_mismatch)`.
3. btrfs and mismatch → continue classification; set `device_check=btrfs_subvolume_skipped` (equal → `match`).

Only if none of (1–2) apply does **classify_quota(fstype, option_keys, btrfs_device→uuid/qgroups)** run below.

## Minimal equivalent decision procedure

```text
function classify_quota(fstype, keys, btrfs_map):
  # btrfs_map: resolve source basename via device_links → uuids listing that device in sysfs

  if fstype == "xfs":
    has_no = ("noquota" in keys)
    has_q  = (∃ k ∈ keys : k ∈ XFS_Q)
    if has_no and has_q:
      return (unknown, n/a, xfs_conflicting_quota_options)
    if has_no and not has_q:
      return (disabled, n/a, xfs_noquota_option)
    if has_q:
      return (enabled, enforced, xfs_quota_option)
    if keys ≠ ∅ and every k ∈ keys satisfies k ∈ XFS_NE:
      return (enabled, accounting_only, xfs_quota_option)
    return (unknown, n/a, xfs_quota_options_absent)

  if fstype == "btrfs":
    uuids = btrfs_map.uuids_for_mount_source_device()
    if |uuids| == 1:
      if btrfs_map.qgroups_present(uuids[0]):
        return (enabled, unknown, btrfs_qgroups_dir_present)
      else:
        return (disabled, n/a, btrfs_qgroups_dir_absent)
    return (unknown, n/a, btrfs_device_unmapped)

  if fstype in {ext2, ext3, ext4}:
    if ∃ k ∈ keys : k ∈ EXT_Q:
      return (enabled, unknown, ext_quota_option)
    return (unknown, n/a, ext_quota_superblock_unobservable)

  if fstype == "tmpfs":
    if (∃ k ∈ keys : k ∈ TMPFS_Q) or (∃ k ∈ keys : k.endswith("_hardlimit")):
      return (enabled, enforced, tmpfs_quota_option)
    return (disabled, n/a, tmpfs_quota_options_absent)

  return (unknown, n/a, unsupported_fstype)
```

Run-level aggregate (separate from per-path table; contract 132–135):

```text
if setup_error: exit 2 QUOTA_SETUP
elif any path quota_state == enabled: exit 1 QUOTA_ENABLED
elif any path quota_state == unknown: exit 2 QUOTA_STATE_UNKNOWN
else: exit 0 QUOTA_DISABLED
```

## Table rows: redundancy and overlap

### Structurally redundant (mergeable without outcome change)

| Rows | Note |
|------|------|
| btrfs R5 + R6 | Same guard `|uuids|==1`; differ only on boolean `qgroups`. One branch with two outcomes. |
| xfs R1 + R4 | Mutually exclusive on `has_q`; can be one `if has_no` with inner conflict test (procedure above). |

No row is a duplicate of another with identical `(quota_state, enforcement, basis)` on the same fstype.

### Overlapping English, order-dependent (not redundant)

| Rows | Overlap | Resolution |
|------|---------|------------|
| xfs R3 vs R5 | Both match when `!noquota`, no `XFS_Q` keys, and keys ⊆ `XFS_NE` only. R5 text (“neither noquota nor any quota key”) is also true. | **First-match:** R3 → `(enabled, accounting_only)`; R5 must not run. Reordering R5 before R3 would change outcomes (oracle cases: xfs with only `uqnoenforce`/`pqnoenforce`). |
| xfs R2 vs R3 | Mutually exclusive if R3 requires *only* noenforce keys (no `XFS_Q`). | R2 before R3 when any `XFS_Q` present. |
| xfs R1 vs R4 | Mutually exclusive on presence of quota keys. | Order irrelevant between them. |

### Non-overlapping partitions

- **ext** (2 rows): partition on `EXT_Q` present vs absent.
- **tmpfs** (2 rows): partition on `TMPFS_Q` / `*_hardlimit` vs absent.
- **other** (1 row): catch-all for remaining fstypes.

## Outcomes the table leaves undefined or under-specified

These are gaps relative to a total function `(fstype, keys, btrfs sysfs) → triple`; implementers must still follow the contract text outside the table.

1. **Pre-table paths** (contract 99–103): `no_covering_mount`, `device_mismatch` — not in the classification table.
2. **XFS row order**: Table does not state first-match; only implicit order makes R3 vs R5 deterministic (see overlap above).
3. **`noquota` + only `XFS_NE` (no `XFS_Q`)**: Matches R1 (`disabled`, `xfs_noquota_option`), not R4 (R4 requires a quota key). Physically odd but defined.
4. **`XFS_Q` + `XFS_NE` together, no `noquota`**: Only R2 applies (`enforced`); no row for “accounting-only with quota flags present.”
5. **Non-empty super options unrelated to quota on XFS** (e.g. only `rw`): R5 (`xfs_quota_options_absent`).
6. **XFS with non-empty keys mixing `XFS_NE` and non-quota, non-noenforce options** (e.g. `rw,uqnoenforce`): Fails R3 (“only noenforce”); falls through to R5 (`unknown`). Not named as its own basis.
7. **btrfs**: Super options ignored; no row for “btrfs but sysfs unreadable / uuid entry missing” beyond `btrfs_device_unmapped` when device lists zero or >1 uuid.
8. **btrfs `qgroups_mode` text**: Emitted in output; table does not say it affects `quota_state` / `enforcement`.
9. **NFS, overlay, fuse, etc.**: If mountinfo fstype is not one of {xfs, btrfs, ext2, ext3, ext4, tmpfs}, row **other** → `unsupported_fstype`. Limits prose (137–140) warns observability bounds; it does not add fstype-specific rows.
10. **`quota_option_keys` on btrfs**: Table silent; keys likely empty or btrfs-irrelevant super keys only — not specified in the table.
11. **Fixture vs real mode**: Malformed inputs → setup exit 2 before any row applies (contract 92–93).

## Preserved contract

- All twelve table rows remain reachable with the same `(quota_state, enforcement, basis)` when evaluated **top-to-bottom as in the contract** for XFS; the pseudocode is reorder-safe except it makes the required R3-before-R5 precedence explicit.
- Mount resolution, device_check rules, aggregate verdict precedence, and output schema are unchanged.

## Tradeoff

Collapsing the XFS five-row block into ordered predicates removes duplicate prose but **must** document R3-before-R5; a naive “mutually exclusive conditions” reading of the table without order would falsify sealed noenforce-only XFS cases.
