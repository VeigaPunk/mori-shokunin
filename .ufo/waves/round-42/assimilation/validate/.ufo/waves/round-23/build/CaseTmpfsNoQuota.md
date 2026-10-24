# CaseTmpfsNoQuota — C2 fixture case (tmpfs with no quota options)

Seat: `MadoR22-2.CaseTmpfsNoQuota-8` (leaf fixture-case author, round 23, wave 1).
Single deliverable, exactly as assigned:

- **Case file:** `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/cases-proposed/CaseTmpfsNoQuota.json`
- **SHA-256:** `f4814c94a8a0f330df82caa46ef1695318e5b3b297545e3b2b888519c4dd4dbb` (5386 bytes)

Contract read in full: `.ufo/waves/round-23/contract.md` (frozen at lane commit
`4dc80c1be48308075e83af17f15fbfe7e95e6cb8`); §C2 is the claim under test. The case is
derived **only** from that contract plus the named kernel sources (S082, S084).
Independence held: no candidate implementation (`.ufo/waves/round-23/build/ImplQuota/`,
`/fast/scratch/hyaku/mori-r23/ImplQuota`) and no proposed case or oracle was opened.
No live host read was performed, no test/lint/build was run, no VCS command was issued.

## 1. Scenario and expectation

Fixture: a synthetic `/proc/self/mountinfo` of an ordinary host (ext4 root, proc, sysfs,
tmpfs `/run`, tmpfs `/run/user/1000`) in which the `/run/user/1000` tmpfs carries **no
quota-related key at all** in its super-options column. Two paths are probed: the mount
point itself and a subdirectory of it, both with `st_dev` `0:52`.

Expected (contract-derived, not implementation-derived):

| field | value | why |
|---|---|---|
| `exit` | `0` | verdict precedence: no path `enabled`, no path `unknown` → `QUOTA_DISABLED` |
| `finding_id` | `QUOTA_DISABLED` | same row |
| `path` | `/run/user/1000`, `/run/user/1000/mori` | the probed paths, echoed |
| `fstype` | `tmpfs` | mountinfo field (m+2) of the chosen line |
| `mount_point` | `/run/user/1000` | mountinfo field (5) of the chosen line, for both paths |
| `quota_state` | `disabled` | tmpfs row 2: no quota key present |
| `enforcement` | `n/a` | tmpfs row 2 |
| `basis` | `tmpfs_quota_options_absent` | tmpfs row 2 basis token |

## 2. Derivation, step by step (contract → sources only)

1. **Mount resolution.** Contract §C2 "Mount resolution": parse mountinfo per `proc.rst`
   §3.5 (fields 1–6, optional fields until `-`, then fstype, source, super options);
   candidate mounts are those whose mount point equals the realpath, is `/`, or is a
   prefix of the realpath; choose the **longest** mount point. For both realpaths the
   candidates are the ext4 root (`/`), the tmpfs `/run`, and the tmpfs `/run/user/1000`;
   the longest is `/run/user/1000`, so `fstype` = `tmpfs`, `mount_point` =
   `/run/user/1000` for both paths. The `/run` tmpfs line is not chosen for either path.

2. **Super options.** The contract takes the option list from the last mountinfo field
   (super options). The chosen line's super options are
   `rw,size=1622560k,nr_inodes=405640,mode=700,uid=1000,gid=1000,inode64`; the keys are
   `rw`, `size`, `nr_inodes`, `mode`, `uid`, `gid`, `inode64`. None is `quota`,
   `usrquota` or `grpquota`, and none ends with `_hardlimit`, so the tmpfs row
   "none of them" applies.

3. **Classification.** Contract §C2 table, tmpfs rows:
   `tmpfs | any of quota,usrquota,grpquota or a key ending _hardlimit | enabled | enforced | tmpfs_quota_option`
   and
   `tmpfs | none of them | disabled | n/a | tmpfs_quota_options_absent`.
   Second row ⇒ `quota_state` `disabled`, `enforcement` `n/a`, `basis`
   `tmpfs_quota_options_absent`. `size`, `nr_inodes` and `mode` are capacity and
   permission settings, not quota mechanisms, and must not be read as quota evidence.

4. **Source anchors.**
   - **S084** `Documentation/filesystems/tmpfs.rst` at v7.2, lines 129–143: the complete
     set of tmpfs quota mount options — `quota`, `usrquota`, `grpquota`,
     `usrquota_block_hardlimit`, `usrquota_inode_hardlimit`, `grpquota_block_hardlimit`,
     `grpquota_inode_hardlimit`. No other key could have carried quota state.
   - **S082** `Documentation/filesystems/proc.rst` at v7.2, §3.5, lines 1965–1990: the
     field layout (1–6, optional `tag[:value]` fields, `-` separator, then fstype,
     source, super options), which is why fstype comes from field (m+2) and the option
     list from field (m+4). The `shared:N` fields in the fixture are the documented
     optional fields and are skipped.
   - Supplementary kernel anchor outside the S077–S084 registry rows:
     `mm/shmem.c` at v7.2 (sha256 `eb5d1e9107b287c8d9d2c1dda83aa0e573917d5b0f88dc17b55162f22718cefb`):
     `shmem_show_options` (4877–4894) prints exactly `,usrquota`, `,grpquota` and the four
     `,*_hardlimit=` keys, and prints `size`, `nr_inodes`, `mode`, `uid`, `gid`,
     `inode64` independently of quota — so a tmpfs mounted without a quota option emits
     no quota key. `shmem_parse_one` (4620–4672) shows only `quota`/`usrquota`/`grpquota`
     set `ctx->quota_types` and the hardlimit options set only `ctx->qlimits`.

5. **Device check.** The chosen fstype is tmpfs, not btrfs, so the chosen mount's
   `major:minor` must equal the path's `st_dev` or the result would be
   `unknown` / `device_mismatch`. The fixture makes them equal (`0:52` both sides).
   That is what a real tmpfs instance reports: a tmpfs superblock takes an anonymous
   block device, major 0 with a per-instance minor (`mm/shmem.c` `shmem_get_tree` →
   `get_tree_nodev`; `fs/super.c` `vfs_get_super` → `set_anon_super_fc` →
   `get_anon_bdev` → `MKDEV(0, dev)`).

6. **Verdict.** No path is `enabled` and no path is `unknown`, so contract precedence
   yields exit `0` and `QUOTA_DISABLED`.

## 3. Contract ambiguities found (reported, not silently resolved)

1. **tmpfs "quota" key is not observable in the super-options column.** The contract's
   tmpfs enabled row lists `quota` among the recognized keys, but the kernel never
   prints a bare `,quota` in `shmem_show_options`; `-o quota` sets both user and group
   quota types and therefore surfaces as `,usrquota` and `,grpquota`
   (`mm/shmem.c` 4620–4636, 4877–4881). The contract's key list is therefore a superset
   of what a real tmpfs line can contain. Harmless for this case (the case is the
   negative direction), and the *enabled* direction is unaffected in practice, but the
   contract should say so.
2. **"a key ending `_hardlimit`" is broader than the kernel.** `tmpfs.rst` 139–142
   documents exactly four hardlimit keys; the contract's wording would also admit an
   arbitrary key such as `foo_hardlimit`. The round-23 pre-seal amendment narrows this
   to the four documented keys, which matches the source. Worth an explicit pointer in
   the contract text.
3. **A hardlimit alone does not enable accounting.** In the kernel a hardlimit option
   only sets `ctx->qlimits`; the quota machinery is enabled only when
   `SHMEM_SEEN_QUOTA` is set by `quota`/`usrquota`/`grpquota` (`mm/shmem.c` 4620–4636 vs
   5027–5040). The kernel therefore always pairs a nonzero hardlimit with an active
   quota flag in the same mount; a hardlimit-only super-options line is a synthetic
   input, not an observable host state. Flagged for the hardlimit case author.
4. **`enforcement` for tmpfs is `enforced` when the flag is present**, because
   `shmem_enable_quotas` loads quotas with `DQUOT_USAGE_ENABLED | DQUOT_LIMITS_ENABLED`
   (`mm/shmem.c` 298–320) — unlike btrfs, where qgroup presence is not proof of any
   limit. The contract's tmpfs/btrfs asymmetry is source-consistent.
5. **tmpfs `st_dev` has major 0** (anonymous block device), so the contract's
   btrfs-only major-0 exception is *not* needed for tmpfs — but the equality check is
   still required there, which the case exercises by making the values equal.

## 4. Scope notes

- The fixture is synthetic; no host state was read. `btrfs_sysfs` and `device_links`
  are empty objects: this fixture contains no btrfs mount and no device-mapper link, and
  neither field is consulted for a tmpfs path. The empty maps are the correct
  representation of that absence, not an omission.
- Both path entries give `path` equal to `realpath`, so the expectation does not depend
  on whether the probe echoes the requested path or the resolved realpath.
- Expected path objects carry exactly the six scored fields; the contract's
  `device_check` / `quota_option_keys` / `btrfs_qgroups_mode` are not asserted here.
- Scratch used for the kernel fetches: `/fast/scratch/hyaku/mori-r23/CaseTmpfsNoQuota/`
  (fetched bytes only; sha256 of `tmpfs.rst` = `5ce3dffe9323912b9146a5f33744776ff623ef42cf8accd6b2dfbea0b9db5be6`,
  `proc.rst` = `e760f716f8278deefab17a63739033cadc7faee93663c49e76455afaaf40d126`).

## 5. Tooling

No tool was installed or updated in this seat; no package transaction was performed
(all pacman transactions are paused host-wide for this wave).
