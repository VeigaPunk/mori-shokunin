# CaseHostLike — C2 fixture case for the host-like default pair (btrfs /home + xfs /tmp)

## Result

One independent C2 fixture case authored and written to
`.ufo/waves/round-23/cases-proposed/CaseHostLike.json` (schema
`mori-quota-case-v1`, `id` `CaseHostLike`). Seat: `MadoR22-2.CaseHostLike-8`
(wave-1 assignment key `CaseHostLike`).

Scenario: a btrfs `/home` subvolume (mountinfo `major:minor` `0:30` while the
path's `st_dev` is `0:57`, i.e. the per-subvolume anonymous device) whose single
listed uuid carries device `dm-0` with qgroups absent, plus an xfs `/tmp` whose
super options end in `noquota` and whose `major:minor` equals the path `st_dev`.
Two paths, in the tool's default order (fleet root, then `/tmp`).

Expected verdict, derived from `contract.md` §C2 only:

| # | path | fstype | mount_point | quota_state | enforcement | basis |
|---|---|---|---|---|---|---|
| 1 | `/home/vgpnk/Projects/shokunin` | `btrfs` | `/home` | `disabled` | `n/a` | `btrfs_qgroups_dir_absent` |
| 2 | `/tmp` | `xfs` | `/tmp` | `disabled` | `n/a` | `xfs_noquota_option` |

Exit `0`, `finding_id` `QUOTA_DISABLED` (no path is `enabled`, none is
`unknown`, so contract §C2 verdict precedence lands on the disabled row).

Independence: no implementation was read — not
`.ufo/waves/round-23/build/ImplQuota/`, not `.scratch/round23/ImplQuota`, not
`.ufo/waves/round-23/build/OracleQuota/`, and no other author's case file. The
expectation was derived from `contract.md` (frozen at lane commit
`4dc80c1be48308075e83af17f15fbfe7e95e6cb8`) and the named kernel sources only.

## Derivation

1. **Mount resolution.** Fixture `mountinfo` (all three lines parsed per
   proc.rst §3.5: fields (1)–(6), optional `tag[:value]` fields until the `-`
   separator, then fstype, source, super options):

   ```
   25 1 0:30 / / rw,relatime shared:1 - btrfs /dev/mapper/root rw,relatime,ssd,space_cache,subvolid=256,subvol=/@
   26 25 0:30 /@home /home rw,relatime shared:1 - btrfs /dev/mapper/root rw,relatime,ssd,space_cache,subvolid=257,subvol=/@home
   29 25 8:2 / /tmp rw,relatime - xfs /dev/sda2 rw,attr2,inode64,logbufs=8,logbsize=32k,noquota
   ```

   Path 1 `/home/vgpnk/Projects/shokunin` (realpath identical) is covered by
   `/` (length 1) and by `/home` (length 5, realpath starts with `/home/`);
   the longest mount point wins → `/home`, `btrfs`, `major:minor` `0:30`.
   Path 2 `/tmp` is covered by `/` and by `/tmp` (equal to the realpath);
   longest → `/tmp`, `xfs`, `major:minor` `8:2`.
   Anchor: S082 `Documentation/filesystems/proc.rst` v7.2 — §3.5 header line
   1965, field (3) *major:minor: value of st_dev for files on filesystem*
   line 1975, optional fields 1979, separator 1980, (m+3) mount source 1982,
   (m+4) super options 1983, "Parsers should ignore all unrecognised optional
   fields." 1985 (re-opened by seat `MadoR22-2.SrcProcMountinfo-8`; line
   numbers re-verified here against the same upstream file).
2. **Device check, path 1 (btrfs).** `0:30 ≠ 0:57`, but contract §C2 states
   that for btrfs a mismatch is expected and is recorded as `device_check`
   `btrfs_subvolume_skipped`; the `device_mismatch` → `unknown` rule is
   explicitly scoped to non-btrfs fstypes. Therefore path 1 is *not* unknown
   and the btrfs classification table is reached. Anchor: S081
   `fs/btrfs/inode.c:8246` — `stat->dev = BTRFS_I(inode)->root->anon_dev;`
   (per-subvolume anonymous device).
3. **Quota classification, path 1 (btrfs).** The mount source
   `/dev/mapper/root` resolves to device `dm-0` through the fixture's
   `device_links` (the contract's own fixture example uses exactly this
   key/value pair). Exactly one uuid lists `dm-0` in its `devices`, so the
   device *is* mapped (the row "zero or several uuids list the device" →
   `btrfs_device_unmapped` does not apply). That uuid's `qgroups` is `false`,
   i.e. `/sys/fs/btrfs/<uuid>/qgroups` is absent. Contract table row
   *"btrfs | … exactly one uuid, `qgroups` false"* → `quota_state` `disabled`,
   `enforcement` `n/a`, `basis` `btrfs_qgroups_dir_absent`; `btrfs_qgroups_mode`
   is `null` (no qgroups dir ⇒ no `qgroups/mode` file).
   Anchors: S079 `fs/btrfs/sysfs.c` — sysfs layout comment line 38
   (`qgroup_attrs /sys/fs/btrfs/<uuid>/qgroups/<level>_<qgroupid>`), the
   `qgroups` kobject created by `btrfs_sysfs_add_qgroups()` (line 2586, kobject
   added as `"qgroups"` at 2604–2605), attributes `enabled` (2368) and `mode`
   (2395, `qgroup_mode_show` 2370–2394); S080 `fs/btrfs/qgroup.c` —
   `btrfs_qgroup_mode()` (33–40) returns `BTRFS_QGROUP_MODE_DISABLED` unless
   `BTRFS_FS_QUOTA_ENABLED` is set, `btrfs_qgroup_enabled()` (43–45), and
   `btrfs_sysfs_add_qgroups()` is called from the quota-enable paths (441,
   1032). The btrfs super options carry no quota key, which is consistent:
   btrfs quota state is not a mount option.
4. **Device check, path 2 (xfs).** `8:2 == 8:2` → `device_check` `match`
   (proc.rst field (3), S082). Had it differed, the row *"xfs … major:minor ≠
   st_dev"* would have produced `unknown` / `device_mismatch`.
5. **Quota classification, path 2 (xfs).** Super options are the last
   mountinfo field: `rw,attr2,inode64,logbufs=8,logbsize=32k,noquota`. Split on
   commas, key = text before `=` ⇒ keys `rw`, `attr2`, `inode64`, `logbufs`,
   `logbsize`, `noquota`; `logbufs`/`logbsize` are deliberately value-carrying
   non-quota keys so the "key = text before `=`" rule is exercised. `noquota`
   is present and none of `usrquota,uquota,quota,grpquota,gquota,prjquota,
   pquota` is → contract row *"xfs | `noquota` and no quota key"* →
   `quota_state` `disabled`, `enforcement` `n/a`, `basis` `xfs_noquota_option`.
   Anchors: S078 `fs/xfs/xfs_super.c` — `Opt_noquota` (114–115),
   `fsparam_flag("noquota", Opt_noquota)` (158) next to the other quota flags
   (157–164), and `xfs_showargs()` emitting `",usrquota"` (239), `",prjquota"`
   (244), `",grpquota"` (249) and `",noquota"` (254) — the latter exactly when
   no quota accounting flag is set, which is why a super-option string ending
   in `noquota` is the realistic shape of an xfs mount without quota; S077
   (xfs quota documentation) for the same option set.
6. **Verdict.** Precedence in contract §C2: setup error → any `enabled` → any
   `unknown` → else disabled. Both paths are `disabled` ⇒ exit `0`,
   `finding_id` `QUOTA_DISABLED`.

Relation to the frozen real control (`frozen/c2-expected-real.json`): this case
is the synthetic twin of it — fleet root → btrfs, mount point `/home`,
`disabled`, `btrfs_qgroups_dir_absent`, `device_check` `btrfs_subvolume_skipped`;
`/tmp` → xfs, `/tmp`, `disabled`, `xfs_noquota_option`, `device_check` `match`.
`device_check` is not part of this case's `expected.paths` because the case
format fixes those objects to exactly `path, fstype, mount_point, quota_state,
enforcement, basis`; the device-check outcomes are stated here instead.

## Sources relied on

| S-id | source | anchor used |
|---|---|---|
| S077 | xfs quota documentation (`Documentation/filesystems/xfs.rst`) | quota mount-option set (`noquota`, `uquota/usrquota/uqnoenforce/quota`, `gquota/grpquota/gqnoenforce`, `pquota/prjquota/pqnoenforce`) |
| S078 | `fs/xfs/xfs_super.c` (v7.2) | `fsparam_flag("noquota", Opt_noquota)` (158); `xfs_showargs()` `",noquota"` (254) emitted iff no quota accounting flag is set |
| S079 | `fs/btrfs/sysfs.c` (v7.2) | `/sys/fs/btrfs/<uuid>/qgroups` kobject (`btrfs_sysfs_add_qgroups()` 2586/2604–2605; attrs `enabled` 2368, `mode` 2395) |
| S080 | `fs/btrfs/qgroup.c` (v7.2) | `btrfs_qgroup_mode()` 33–40 (`DISABLED` unless `BTRFS_FS_QUOTA_ENABLED`), `btrfs_qgroup_enabled()` 43–45, `btrfs_sysfs_add_qgroups()` call sites 441/1032 |
| S081 | `fs/btrfs/inode.c` (v7.2) | `stat->dev = BTRFS_I(inode)->root->anon_dev;` (8246) — per-subvolume anonymous `st_dev` |
| S082 | `Documentation/filesystems/proc.rst` (v7.2) | §3.5 field layout (1965–1985): fields (1)–(6), optional fields until `-`, fstype, source, super options; field (3) `major:minor` = `st_dev` (1975) |

S083 (ext4) and S084 (tmpfs) were **not** relied on: no ext2/3/4 or tmpfs path
appears in this case.

S-id caveat: `corpus/SOURCES.md` still ends at S076; the rows S077–S084 are
being drafted this round by the scribe seat `DraftSourceRows`. I mapped
S077–S084 by the wave-1 source-reopener order (SrcXfsDoc, SrcXfsShowargs,
SrcBtrfsSysfs, SrcBtrfsQgroup, SrcBtrfsGetattr, SrcProcMountinfo, SrcExt4Doc,
SrcTmpfsDoc), which is the same mapping the sibling case authors used and is
the only mapping consistent with the contract's own pin of **S081** for
"per-subvolume anonymous `st_dev`". If L1 assigns the rows differently, the
`sources` array in this case file must be remapped before sealing.

## Contract ambiguities found (for L1; none changes this case's expectation)

- **A1 — `quota_option_keys` and `noquota`.** The output field is specified as
  "sorted quota-related keys only", but the contract never says whether
  `noquota` counts as quota-related (the classification table treats it as
  distinct from the "quota key" set). Path 2 here ends in `noquota`, so the
  two readings give `["noquota"]` vs `[]`. This case's `expected` deliberately
  excludes `quota_option_keys`, so it is immune; the tool and the oracle still
  need one fixed reading (recommendation: `noquota` **is** a quota-related key,
  since it is a quota option, but it must not be counted as a quota *enabler*).
- **A2 — fixture-mode device resolution.** Real mode resolves the mount device
  as `os.path.realpath(mount_source)` basename (on a btrfs-over-dm-crypt host
  `/dev/mapper/root` resolves to `/dev/dm-0`, hence `dm-0` — that host
  `/dev/mapper/*` link was not read by this seat, so it is stated as the
  contract's own device-name bridge, not as an observation); in fixture mode there is no
  `realpath`, so the device name can only come from `device_links`. The
  contract does not state whether `device_links` is keyed by the mount source
  string as written (my fixture: `/dev/mapper/root`) or by its basename
  (`root`). An implementation that looks up the basename would find no uuid
  listing `root` and would answer `btrfs_device_unmapped` / `unknown` instead
  of `btrfs_qgroups_dir_absent` / `disabled`. The contract's own fixture
  example (`device_links` keyed `/dev/mapper/root` → `dm-0`) implies the
  full-path key, i.e. `device_links` stands in for the `realpath` step; this
  should be stated explicitly.
- **A3 — same source on several mounts.** My fixture mounts the same source
  (`/dev/mapper/root`) at `/` and `/home`. The contract's device→uuid mapping
  is per-source, not per-mount, which is consistent here; the rule is not
  written down, so an implementation that resolves the uuid per mount line
  would still agree on this fixture.
- **A4 — `paths[].realpath` authority.** The contract's fixture format carries
  `realpath` explicitly, but does not say whether the tool recomputes it in
  fixture mode or trusts the fixture. Mine sets `realpath == path` for both
  paths, so both readings agree.
- **A5 — `btrfs_qgroups_mode` when qgroups is absent.** The contract says the
  field is "the mode text or null" and the fixture example pairs
  `qgroups: false` with `qgroups_mode: null`; the kernel agrees (the `mode`
  attribute only exists inside the `qgroups` kobject, S079/S080). No conflict,
  recorded for completeness.
- **A6 — `enforcement` token for a disabled btrfs path.** The contract's btrfs
  row gives `n/a` for the disabled row (the `unknown` value there is only for
  the enabled row), matching the fixture's expectation.
- **A7 — the `/` line in a synthetic fixture.** No rule requires or forbids a
  root mount line in the fixture text. Mine includes it (host-like) so that
  mount selection by longest mount point is actually exercised rather than
  trivially satisfied.

## Bounds and tooling

- Files written: exactly two, both mine — the case file
  `.ufo/waves/round-23/cases-proposed/CaseHostLike.json` and this report
  `.ufo/waves/round-23/build/CaseHostLike.md`. The case file is named after the
  wave-1 assignment key `CaseHostLike` (matching the sibling case files and
  the report path); the agent seat id is `MadoR22-2.CaseHostLike-8`.
- No host probe of any kind was performed (no `/proc/self/mountinfo`, no
  `os.stat`, no `/sys/fs/btrfs`, no `/dev/mapper`): every host-shaped value in
  the fixture is either given by the assignment (`0:30`, `0:57`, `dm-0`,
  qgroups false, `noquota`) or chosen for internal consistency (`8:2` /
  `/dev/sda2` for the xfs pair, the uuid string, the mount ids).
- Upstream kernel sources were re-opened read-only over HTTPS
  (`raw.githubusercontent.com/torvalds/linux/v7.2/…`, `curl … | grep`), streamed
  to stdout only; nothing was downloaded to disk and no scratch file was
  created.
- Tool installs: none — `curl` was already present, so no pacman/uv/npx/cargo
  transaction was needed or performed (all pacman transactions remain paused
  host-wide).
- No build, test, lint, formatter or smoke run was executed; no VCS mutation
  (`git add/commit/push`, jj) and no `agent://all` broadcast.

---

## Correction — pre-seal amendment (appended after `.ufo/waves/round-23/preseal-amendment.md`)

Authored under the round-23 pre-seal amendment, which supersedes only the
erroneous/ambiguous clauses of `contract.md` §C2. A **new** corrected case was
written to `.ufo/waves/round-23/cases-corrected/CaseHostLike.json` (same `id`
`CaseHostLike`); the original proposal
`.ufo/waves/round-23/cases-proposed/CaseHostLike.json` is retained untouched.
No implementation was opened, no result was observed, no test was run.

### Delta

| element | original proposal | corrected case |
|---|---|---|
| `btrfs_sysfs[<uuid>]` record keys | `devices`, `qgroups`, `qgroups_mode` | `devices`, `qgroups`, **`qgroups_enabled`**, `qgroups_mode` |
| `qgroups_enabled` | absent | `null` (original `qgroups` is false) |
| `mountinfo`, `paths`, `device_links` | — | byte-identical |
| `expected` (exit, finding_id, paths) | — | identical |
| `sources` | — | identical (S077–S082) |

The amendment's mechanical mapping is applied: `qgroups_enabled = true` where
the original `qgroups` was true, `null` where it was false. This case has one
uuid record with `qgroups` false, so it gets `qgroups_enabled: null` and
`qgroups_mode: null` — an absent qgroups directory has neither an `enabled`
file nor a `mode` file. No decoy uuid records exist in this fixture, so no
decoy needed the pairing.

### Derivation under the amended rules (expectation unchanged)

The amendment changes three branches; none of them is reached by this case:

1. **btrfs qgroups semantics.** Presence of the qgroups directory now means
   *initialized*, not *enabled*; `qgroups/enabled` decides. This fixture has the
   directory **absent** (`qgroups` false, `enabled` null, `mode` null) and the
   uuid has a record, i.e. the parent inspection succeeded, so the absent-dir
   row is retained: `disabled` / `n/a` / `btrfs_qgroups_dir_absent`
   (`btrfs_qgroups_mode` null). The amendment's other btrfs rows
   (`btrfs_qgroups_enabled`, `btrfs_qgroups_disabled`,
   `btrfs_qgroups_enabled_unavailable`) need a *present* directory and are not
   reachable from this fixture.
2. **Device mismatch preemption.** A mismatch now preempts the filesystem
   table (`unknown` / `n/a` / `device_mismatch`), but the btrfs equality skip
   still applies because the path's stat major is `0` (`0:57`), so `0:30 ≠ 0:57`
   remains the expected per-subvolume anonymous device
   (`device_check` `btrfs_subvolume_skipped`) and the btrfs table is reached. A
   nonzero btrfs stat major with a mismatch would pre-empt — not the case here.
   Path 2 keeps `8:2 == 8:2` → `device_check` `match`.
3. **Mount resolution hardening.** `ambiguous_overmount` fires only when a
   covering mount point occurs more than once; here the covering mount points
   are `/` and `/home` (path 1) and `/` and `/tmp` (path 2), each occurring
   exactly once, so longest-mount-point selection still yields `/home` (btrfs)
   and `/tmp` (xfs). The fixture contains no backslash escapes, so the octal
   decoding of root, mount point and source is a no-op.

The xfs branch is unchanged in substance: the super options
`rw,attr2,inode64,logbufs=8,logbsize=32k,noquota` contain the key `noquota`
and no quota/enforcement/noenforce key, so the amended xfs precedence
(conflict → noquota → enforced → accounting-only → absent) selects the noquota
row: `disabled` / `n/a` / `xfs_noquota_option`. Path 1's `quota_option_keys`
is `[]` (a btrfs mechanism is sysfs, not mount options); path 2's is
`["noquota"]` (noquota plus recognized xfs keys, sorted). Those supplementary
fields are stated here and **not** added to the expected tuples, which the
case format fixes to exactly `path, fstype, mount_point, quota_state,
enforcement, basis`.

Verdict: neither path enabled, neither unknown → exit `0`, `QUOTA_DISABLED` —
identical to the original proposal.

### Fixture metadata conformance (amendment)

Paths nonempty, unique, normalized absolute with `realpath == path` and no
dot/dotdot components; `st_dev` canonical decimal `MAJ:MIN` (`0:57`, `8:2`, no
signs, no leading zeros other than the major `0`); uuid key canonical; devices
and the `device_links` value plain nonempty basenames without slashes or
control characters; qgroups fields typed exactly `false` / `null` / `null`; the
raw decoded source `/dev/mapper/root` is looked up in `device_links` and its
mapped basename `dm-0` matches exactly one uuid's `devices` list, so the
device is mapped (not the zero/several-uuid case).

### Hashes (final)

| file | sha256 |
|---|---|
| `.ufo/waves/round-23/cases-corrected/CaseHostLike.json` | `f4580093a6aa93eab53bef9c9f61667a2a0aa2224096b60568140904b148a63c` |
| `.ufo/waves/round-23/cases-proposed/CaseHostLike.json` (original, untouched) | `e83132fc329dc28dcd1e6ebdc51c645c78b9f8a15b5ffe701f7c75de793c9d93` |
| `.ufo/waves/round-23/build/CaseHostLike.md` (this file) | digest stated in the reply to L1 (`agent://MadoR22-2`) — a file cannot contain its own hash; measured after this append |

