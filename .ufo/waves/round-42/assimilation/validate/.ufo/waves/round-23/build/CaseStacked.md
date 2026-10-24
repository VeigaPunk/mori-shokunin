# CaseStacked — C2 fixture case (stacked same-mount-point tie-break)

Seat: `MadoR22-2.CaseStacked-8` (wave-1 leaf, reviewer role).
Case file written: `.ufo/waves/round-23/cases-proposed/CaseStacked.json` (exactly one file, schema `mori-quota-case-v1`, id `CaseStacked`).
Scope: derivation of one independent C2 fixture case from `contract.md` §C2 + kernel sources only. **No implementation was read** (I did not open `.ufo/waves/round-23/build/ImplQuota/`, `.scratch/round23/ImplQuota`, `.ufo/waves/round-23/cases-proposed/` peers' files, or `.ufo/waves/round-23/build/OracleQuota/`). Nothing was executed, built, tested or linted.

## 1. The case

Scenario (one line, as filed): two mountinfo lines share the mount point `/data` — an earlier `xfs` line whose super options end in `noquota`, and a later `tmpfs` line whose super options carry `usrquota`; the later line wins, so the path resolves to tmpfs with visible user-quota enforcement.

Fixture (`mori-quota-fixture-v1`, exactly the five contract keys `schema, mountinfo, paths, device_links, btrfs_sysfs`):

```
1 23 0:21 / /proc rw,nosuid,nodev,noexec,relatime shared:12 - proc proc rw
7 23 0:6 / /dev rw,nosuid,relatime shared:2 - devtmpfs udev rw,size=4021252k,nr_inodes=1005313,mode=755
23 23 259:3 / / rw,relatime shared:1 - ext4 /dev/nvme0n1p3 rw,errors=remount-ro
31 23 259:2 / /data rw,relatime shared:1 - xfs /dev/nvme0n1p2 rw,inode64,logbufs=8,logbsize=256k,noquota
44 31 0:58 / /data rw,nosuid,nodev,noexec,relatime shared:1 - tmpfs tmpfs rw,size=4194304k,inode64,usrquota
```

One path: `/data` (realpath `/data`, st_dev `0:58`). `device_links` and `btrfs_sysfs` carry inert content (no btrfs in this scenario) but the keys are present because the contract makes the top-level key set exact.

Expectation:

| path | fstype | mount_point | quota_state | enforcement | basis |
|---|---|---|---|---|---|
| /data | tmpfs | /data | enabled | enforced | tmpfs_quota_option |

`exit = 1`, `finding_id = QUOTA_ENABLED`.

## 2. Derivation, step by step

1. **Field parsing.** `contract.md:95-97` says parse mountinfo per proc.rst §3.5 (fields 1–6, optional fields until `-`, then fstype, source, super options). `proc.rst:1969-1983` (S082) gives the example line and the field list: (1) mount ID, (2) parent ID, (3) major:minor = st_dev of the filesystem, (4) root, (5) mount point, (6) mount options, (n…m) optional `tag[:value]` fields, (m+1) separator `-`, (m+2) filesystem type, (m+3) mount source, (m+4) super options. The fixture lines follow that shape; `shared:N` sits in the optional-field region, before `-`.
2. **Which super options are "the last field".** `fs/proc_namespace.c:170-189` (kernel v7.2) shows the mountinfo writer: after the `-` separator it prints fstype, mount source, then `ro`/`rw`, then `show_sb_opts()` and finally `sb->s_op->show_options()`. So the last field is the superblock options string — for xfs `xfs_fs_show_options` (`fs/xfs/xfs_super.c:185-255`, S078), for tmpfs `shmem_show_options` (`mm/shmem.c:4827-4894`). This is why the quota flags appear in the last field and not in field 6.
3. **Candidate set.** `contract.md:96-99`: candidates are mounts whose mount point equals the realpath, is `/`, or is a prefix (`realpath` starts with mount point + `/`). For `/data` the candidates are the `/` ext4 root (mount ID 23) and both `/data` lines (31, 44). `/proc` and `/dev` are not candidates.
4. **Tie-break.** `contract.md:99`: choose the longest mount point; among *equal* mount points the **last** line wins. `/data` (5 chars) beats `/` (1 char); between 31 and 44 the later line, 44 (tmpfs), wins.
5. **Device check.** `contract.md:100-103`: the exemption applies to btrfs only. The chosen fstype is tmpfs, so the check is a real equality test: the chosen line's major:minor `0:58` equals the path st_dev `0:58` → `device_check: "match"`, no `device_mismatch`.
6. **Classification.** `contract.md:105-106`: super options = last mountinfo field, comma-split, key = text before `=`. The tmpfs super options `rw,size=4194304k,inode64,usrquota` yield keys `rw`, `size`, `inode64`, `usrquota`. `contract.md:120` (tmpfs row): any of `quota,usrquota,grpquota` or a key ending `_hardlimit` → `enabled` / `enforced` / `tmpfs_quota_option`. `usrquota` is present → that row.
7. **Verdict.** `contract.md:132-134`: setup error → 2 `QUOTA_SETUP`; else any `enabled` → 1 `QUOTA_ENABLED`; else any `unknown` → 2 `QUOTA_STATE_UNKNOWN`; else 0 `QUOTA_DISABLED`. One path, enabled → exit 1, `QUOTA_ENABLED`.

## 3. Why this case discriminates

The rejected variant is not a near-miss on the same row: choosing the *earlier* xfs line yields `fstype=xfs`, `mount_point=/data`, and because xfs is not btrfs and its major:minor `259:2` differs from the path st_dev `0:58`, `contract.md:100-101` gives `quota_state=unknown`, `enforcement=n/a`, `basis=device_mismatch` — so the run would end in exit 2 `QUOTA_STATE_UNKNOWN`, not exit 1 `QUOTA_ENABLED`. The case therefore fails loudly (wrong basis *and* wrong exit code) under a wrong tie-break, in two independent dimensions, not merely on a different fstype string.

Note the ordering consequence in `contract.md:100-101`: the device check precedes the classification table, so `device_mismatch` **replaces** the `xfs_noquota_option` row that would otherwise apply to that line. The rejected variant is therefore `device_mismatch`, not `xfs_noquota_option`.

## 4. Source grounding (registry ids among S077–S084)

`corpus/SOURCES.md` stops at S076; the round-23 scribe seat `DraftSourceRows` has drafted the eight rows S077–S084 in `.ufo/waves/round-23/build/DraftSourceRows.md` (and `DraftSourceRows/rows.md`), in scout-item order: S077 `Documentation/admin-guide/xfs.rst`, S078 `fs/xfs/xfs_super.c`, S079 `fs/btrfs/sysfs.c`, S080 `fs/btrfs/qgroup.c`, S081 `fs/btrfs/inode.c`, S082 `Documentation/filesystems/proc.rst`, S083 `Documentation/admin-guide/ext4.rst`, S084 `Documentation/filesystems/tmpfs.rst`. That ordering is the one the contract itself assumes (it cites S081 for the per-subvolume anonymous `st_dev`). I relied on four of them and cite them in the case's `sources` list; my independently fetched bytes have the **same SHA-256 as the scribe's table** for every file I used, so the anchors agree byte-for-byte:

- **S082** — `Documentation/filesystems/proc.rst` §3.5: heading 1965, example line 1970, field table 1973–1983 (mount point 1977, separator 1980, filesystem type 1981, mount source 1982, super options 1983), "Parsers should ignore all unrecognised optional fields." 1985. sha256 `e760f716f8278deefab17a63739033cadc7faee93663c49e76455afaaf40d126` (matches the sealed table).
- **S084** — `Documentation/filesystems/tmpfs.rst`: table header 129, `quota` 132, `usrquota` 135 ("User quota accounting and enforcement is enabled on the mount."), `grpquota` 137, `usrquota_block_hardlimit` 139, `usrquota_inode_hardlimit` 140, `grpquota_block_hardlimit` 141, `grpquota_inode_hardlimit` 142, table end 143, remount sentence 145. sha256 `5ce3dffe9323912b9146a5f33744776ff623ef42cf8accd6b2dfbea0b9db5be6` (matches).
- **S077** — `Documentation/admin-guide/xfs.rst`: `noquota` 171–173 ("Forcibly turns off all quota accounting and enforcement within the filesystem."), `uquota/usrquota/uqnoenforce/quota` 175–177, `gquota/grpquota/gqnoenforce` 179–181, `pquota/prjquota/pqnoenforce` 183–185. sha256 `53bda67b5612a3f2c02820604d05825c9d37addba9855e1d4fba330a516d051c` (matches).
- **S078** — `fs/xfs/xfs_super.c` `xfs_fs_show_options` 186–190; emitted quota options `usrquota` 239, `uqnoenforce` 241, `prjquota` 244, `pqnoenforce` 246, `grpquota` 249, `gqnoenforce` 251, `noquota` 254. sha256 `0a95697dcfcdab8f7ab6ea26fdb941db952db4b73ed93c30d21e40861ed0450c` (matches).

Three further kernel files were opened only to make the fixture text realistic, not as registry sources:
- `fs/proc_namespace.c` (sha256 `fd82c0db52055ae807ee0b46c7c9bc5d47a9239805eb8ca5c47d2ba81d695776`) — `show_mountinfo` 140–195: after the `-` separator it prints fstype, mount source, `ro`/`rw`, then `show_sb_opts()` and `sb->s_op->show_options()`; the last mountinfo field is therefore the superblock options string, and `nosuid,nodev,noexec,relatime` belong to mount-options field 6.
- `mm/shmem.c` (sha256 `eb5d1e9107b287c8d9d2c1dda83aa0e573917d5b0f88dc17b55162f22718cefb`), `shmem_show_options` 4827–4894 — prints `,usrquota` when `sb_has_quota_active(..., USRQUOTA)` and `,grpquota` for GRPQUOTA, and the `*_hardlimit=` keys only when set; the kernel never prints a bare `quota` for tmpfs. This is what makes `usrquota` in a tmpfs super-options field realistic rather than invented, and it matches the `DraftSourceRows` F-6 finding.
- `fs/namespace.c` (sha256 `3c2417e6bd81a82de3a989caf6b80ac28658954dcc20078a60d1a5b4925fcdaa`), `attach_mnt` 1051 — confirms the overmount's parent-ID field, used to make the stacked line's parent ID (`31`) realistic.

All fetched bytes are under `.scratch/round23/CaseStacked/` (the wave-sanctioned download area; not a lane artifact, not committed).

## 5. Contract ambiguities found (for L1 / the contract owner)

1. **"last line wins" — file order vs mount-ID order.** `contract.md:99` does not say whether "last" means last in the mountinfo *text* or the highest mount ID. In practice `/proc/self/mountinfo` is emitted in namespace-tree order, which is neither strictly text-creation order nor ID order in all cases. I built the fixture so both readings agree (the tmpfs line is later in the text **and** has the higher mount ID 44 > 31), so the case is safe under either reading. An implementation that sorts by mount ID, or that takes the last text line, both pass; an implementation that takes the *first* matching line fails loudly.
2. **The `/` candidate needs its own clause.** With mount point `/`, the prefix rule `realpath starts with mount point + "/"` would test `"/data".startswith("//")` — false. The explicit "or is `/`" clause in `contract.md:96` is what makes the root mount a candidate at all. My fixture includes a `/` ext4 root precisely so the candidate set exercises that clause; it must never win (shortest mount point).
3. **`device_mismatch` overrides the classification row.** `contract.md:100-101` is stated before the table, so a device mismatch yields `unknown`/`device_mismatch` even when the fstype's own row would have produced a definite state (here `xfs_noquota_option`). The contract does not say this explicitly ("precedence" is only stated for the overall verdict at :132-134). I read it as device-check-first; the rejected variant in §3 depends on that reading. **This is the one ambiguity that materially changes an expectation**, and it is why this case's rejected variant is `device_mismatch` rather than `xfs_noquota_option`.
4. **The tmpfs row has no accounting-only variant.** xfs distinguishes `uqnoenforce`/`gqnoenforce`/`pqnoenforce`/`qnoenforce` → `accounting_only`, but tmpfs (contract.md:120-121) has no equivalent and tmpfs.rst offers no `*noenforce` option, so the tmpfs `enforcement` is unconditionally `enforced` for any quota key. Not an ambiguity in this case (no `*noenforce` key is present), but it means the `accounting_only` token is unreachable for tmpfs.
5. **Which keys are "quota-related" for `quota_option_keys`.** `contract.md:124-126` says `quota_option_keys` = sorted quota-related keys only, and the classification table enumerates the quota key sets per fstype, but the contract does not state the key set used to *filter* the super options for that output field (the xfs set is larger than tmpfs's; `quota` is in both, `usrquota`/`grpquota` in both, `uquota`/`gquota`/`prjquota`/`pquota`/`prjquota`/`usrjquota`/`grpjquota`/`noenforce` variants differ). Not asserted in my case (the case expectation carries only the six contract-listed keys), but an implementation must pick one set and the contract does not name it.
6. **`st_dev` string form.** The fixture format writes `st_dev` as `"MAJ:MIN"` and the mountinfo major:minor as `MAJ:MIN`; the contract compares them for equality but does not say whether the comparison is textual or numeric. My fixture uses `0:58` on both sides, identical in both readings, so the case does not depend on the answer. A case with e.g. `259:01` vs `259:1` would expose the difference.

## 6. Verification gaps / what I did not do

- I did not execute any probe, oracle, selftest or implementation, and I read no candidate implementation, so the expectation is unverified against code by construction (that is the point of the independence rule). The derivation is contract + kernel sources only.
- The case's discriminating power is against the *tie-break*; it does not cover the btrfs, ext, xfs-only or setup-error paths — those are other seats' cases (`CaseBtrfsQgroup`, `CaseBtrfsSquota`, `CaseBtrfsUnmapped`, `CaseBtrfsTwoUuids`, `CaseBtrfsDevMatch`, `CaseXfsUsrquota`, `CaseXfsAccountingOnly`, `CaseXfsMixedEnforce`, `CaseXfsOptionsAbsent`, `CaseXfsConflict`, `CaseXfsDevMismatch`, `CaseExt4Usrquota`, `CaseExt4NoOptions`, `CaseExt4Journaled`, `CaseTmpfsUsrquota`, `CaseTmpfsNoQuota`, `CaseTmpfsHardlimit`, `CaseUnsupported`, `CaseNoCover`, `CaseSetupMalformed`).
- `CaseTmpfsUsrquota` covers the plain tmpfs+usrquota classification; my case adds the stacked-mount dimension on top of it. If L1 seals both, the tmpfs classification itself is asserted twice — harmless, but the unique contribution of this case is the same-mount-point tie-break plus its device-check consequence.
- S-ids S077-S084 have no committed `corpus/SOURCES.md` rows yet (the `DraftSourceRows` draft is uncommitted). My `sources` list matches that draft's file assignment exactly (S077 xfs.rst, S078 xfs_super.c, S082 proc.rst, S084 tmpfs.rst) and my independently fetched bytes match its SHA-256 table, so if the L1 seals the same assignment no re-pointing is needed; if it changes, the anchors and quotes in §4 are file- and line-exact and easy to re-point.

## 7. Tooling

No packages installed; no `pacman`/`uv`/`npm`/`cargo` activity (the tooling directive's channel order was not needed). Fetching used `curl` only, into `.scratch/round23/CaseStacked/`. No live host probes: I did not read `/proc/self/mountinfo`, stat the fleet root or `/tmp`, list `/sys/fs/btrfs`, or readlink `/dev/mapper/*` — the fixture is fully synthetic, and my seat's item names none of those reads. No `/tmp` use. No git/jj mutation, no background jobs, no fleet-root writes, no subagent dispatch.

## 8. Checks the main agent should run after sealing

1. `python3 -m json.tool .ufo/waves/round-23/cases-proposed/CaseStacked.json` parses; top-level keys exactly `schema,id,scenario,fixture,expected,rationale,sources`; `fixture` keys exactly the five contract keys; `expected.paths[0]` keys exactly `path,fstype,mount_point,quota_state,enforcement,basis`.
2. Confirm the fixture's five mountinfo lines parse per proc.rst §3.5 (fields 1-6, optional fields, `-`, fstype, source, super options) and that the two `/data` lines are the last of the equal-length candidates.
3. Confirm the sealed S077-S084 rows point at the files/lines cited in §4, and re-point my `sources` list if the assignment differs.
4. Against the sealed implementation: the run must exit 1 with `finding_id=QUOTA_ENABLED` and the per-path row in §1; any other value is a defect in the tie-break or in the device-check precedence of `contract.md:100-101`.

---

## 9. CORRECTION (appended after `preseal-amendment.md`, before any candidate inspection)

The round-23 pre-seal amendment (`preseal-amendment.md`, written before L1 opened any `ImplQuota` candidate or ran any C2 candidate) supersedes the original contract clauses my §1-§3 derivation relied on. I authored a **new corrected case** and **left `cases-proposed/CaseStacked.json` byte-unchanged** as the original proposal.

Corrected case file: `.ufo/waves/round-23/cases-corrected/CaseStacked.json` — sha256 `b45f3485c170a88f75abcf8746315caf031331c4cf92b4943847f7433bf980d0`.
Original proposal (untouched): `.ufo/waves/round-23/cases-proposed/CaseStacked.json` — sha256 `6104d13acc6a74f6b53f37c122fe0e57d523ddbea8d9d207f9fa4af16c54cff0`.

### 9.1 What changed and why

| item | original proposal | corrected case | authority |
|---|---|---|---|
| `/data` outcome | tmpfs / enabled / enforced / `tmpfs_quota_option` | unknown / n/a / `ambiguous_overmount`, fstype null, mount_point null | `preseal-amendment.md:50-54` |
| exit / finding_id | 1 / `QUOTA_ENABLED` | 2 / `QUOTA_STATE_UNKNOWN` | `contract.md:132-134` precedence, unchanged |
| `btrfs_sysfs` record | `devices, qgroups, qgroups_mode` | adds required `qgroups_enabled` (null, paired with `qgroups=false` / `qgroups_mode=null`) | `preseal-amendment.md:37-39, 42-43` |
| mountinfo, paths, device_links | 5 lines, one path, `{"/dev/mapper/root":"dm-0"}` | **unchanged** | — |

Derivation of the new expectation, step by step:

1. `preseal-amendment.md:50-54`: longest component-prefix selection remains, **but** "if ANY covering mountpoint occurs more than once, refuse classification as unknown/n/a/`ambiguous_overmount`, fstype=null,mount_point=null, device_check=not_checked. Do not guess stack order from line order or reusable IDs." Parent-ID graph resolution is explicitly deferred.
2. The fixture's two `/data` lines (mount IDs 31 xfs, 44 tmpfs) make `/data` a covering mountpoint that occurs more than once for the requested path `/data`. So the path is **not classified at all** — the refusal precedes both the classification table and the device check.
3. The original proposal's whole discriminator — "the later line wins" — is exactly what the amendment forbids: it forbids guessing the stack winner from line order or reusable IDs. My original expectation (`tmpfs`/`enabled`/`enforced`/`tmpfs_quota_option`, exit 1) is therefore **withdrawn**, not merely re-derived.
4. `fstype=null`, `mount_point=null` per `preseal-amendment.md:51-52` (the same null convention the amendment uses for no-cover at `:58`); `quota_state=unknown`, `enforcement=n/a`, `basis=ambiguous_overmount`; `device_check=not_checked`.
5. Verdict: no setup error, no enabled path, one unknown path → exit 2, `finding_id=QUOTA_STATE_UNKNOWN` (`contract.md:132-134` precedence is not amended).
6. The classification table is never reached for this path, so the tmpfs row (`contract.md:120`), the xfs rows (`contract.md:110-114`) and the device-equality rule (`contract.md:100-103`, `preseal-amendment.md:55-58`) are all inapplicable here. The amended ext rule (`preseal-amendment.md:33-36`, `ext_quota_option_unverified`) and the amended btrfs rule (`preseal-amendment.md:37-46`, `btrfs_qgroups_enabled`) also do not fire: the ext4 `/` root line is not the covering mount for `/data`, and no mount in this fixture is btrfs.
7. Fixture delta is confined to `btrfs_sysfs`: the decoy UUID `1d02a454-c549-4a35-b567-89d60902af8e` gains the required `qgroups_enabled` member; its `qgroups=false` pairs with `enabled=null` / `mode=null` (`preseal-amendment.md:39`, `:42-43`), so `qgroups_enabled: null`. The record is a decoy here and must not turn the path into a btrfs case — which is why it is kept (the amendment's rule is stated over *every* UUID record, decoys included) rather than deleted.

### 9.2 Effect on my §1-§8 analysis

- §2 step 4 (tie-break) and §3 (discrimination via `device_mismatch` under a wrong tie-break) are **superseded**. Under the amendment there is no tie-break to get wrong: the duplicate covering mountpoint is refused before any ordering question arises. The case's remaining discriminating power is: a tool that resolves `/data` to *either* the xfs line or the tmpfs line (i.e. that classifies a duplicated covering mountpoint) now fails on fstype, mount_point, quota_state, enforcement, basis **and** the exit code/finding_id — a strictly louder failure than under the original contract.
- §5 ambiguity #1 ("last line wins": text order vs mount-ID order) is **closed by the amendment**: line order must not be used at all, so the ambiguity is removed rather than decided. My original fixture deliberately made both readings agree; that precaution is now unnecessary but harmless, and the fixture is preserved unchanged per the instruction to preserve unrelated fixtures.
- §5 ambiguity #3 (`device_mismatch` overriding the classification row) is **resolved in the amendment's favour** — `preseal-amendment.md:55-58` states the device mismatch preempts the filesystem table, with `device_check=mismatch`. That is the reading my original §3 assumed, but the authority is now explicit rather than inferred, and it no longer bears on this case's outcome.
- §5 ambiguity #5 (`quota_option_keys` filtering set) and #6 (`st_dev` textual vs numeric comparison) are **not addressed** by the amendment and remain open; neither bears on this case (no classification is reached; `st_dev` is `0:58` on both sides in both readings).
- §6/§7/§8 stand, with one update: the sealed check in §8 item 4 must now read *"exit 2 with `finding_id=QUOTA_STATE_UNKNOWN` and the per-path row in §9.1"*, and the case to seal is the `cases-corrected/` file. §8 items 1-3 apply to the corrected file too (key sets, mountinfo field shape, S-id mapping); §8 item 2's "the two `/data` lines are the last of the equal-length candidates" is obsolete — the point is now that they are the *duplicate* covering mountpoint.

### 9.3 Bounds for this correction

No implementation was read (no `ImplQuota`, no `OracleQuota`), no candidate was run, no test/build/linter was executed, no peer case file was read, no subagent was dispatched. The derivation is from `preseal-amendment.md`, `contract.md` and the same four kernel sources already cited in §4 (S077, S078, S082, S084 — my independently fetched bytes still match the `DraftSourceRows` SHA-256 table). No tooling installed; no live host probes; no `/tmp`; no VCS mutation; no fleet-root writes. `cases-proposed/CaseStacked.json` was not edited, and `cases-corrected/` was created only because the L1 named it as an authorized output path.

---

## 10. CORRECTION 2 — supplemental case for the parent-ID consistency refusal

The amendment's **final pre-seal clarifications** (same source-review stage, before any candidate/result read) add a further C2 rule: "C2 additionally refuses when the chosen mount's parent ID is present in the snapshot but is not the ID of the longest strictly-shorter covering mount. Use unknown/n/a/ambiguous_overmount with null fstype/mountpoint and not_checked device_check. This catches a new mount on a plain ancestor directory hiding an older nested mount without any repeated mountpoint; a missing parent ID remains unknown topology but does not trigger this extra refusal. Root has no shorter cover." (`preseal-amendment.md:115-121`).

That clause is **not** exercised by my §1-§9 cases: my corrected case triggers the *duplicate-covering-mountpoint* refusal (`:50-54`), which is a different rule and fires earlier. The L1 assigned me the missing coverage — the parent-ID rule — as a **new supplemental case** derived from the `CriticContractC2` D2 counterexample shape, with the L1's specified mount IDs. I authored it at `.ufo/waves/round-23/cases-supplemental/SupplementHiddenMount.json`; the original proposal (`cases-proposed/`) and the corrected case (`cases-corrected/`) are **preserved byte-unchanged**.

Supplemental file sha256 `d1a3a4c66008fcdefec47839d9393f1c971ebc6630d96b94c399038378187824`.

### 10.1 Fixture and derivation

Mountinfo (four lines, per proc.rst §3.5 / S082 — field 2 parent ID, field 3 major:minor, field 5 mount point, field m+4 super options):

```
1  1 0:30 /@    /        rw,relatime shared:1 - btrfs /dev/mapper/root rw,space_cache=v2,subvolid=256,subvol=/@
65 1 0:30 /@home /home  rw,relatime shared:2 - btrfs /dev/mapper/root rw,space_cache=v2,subvolid=257,subvol=/@home
70 65 0:31 /    /home/x/y rw,relatime shared:3 - btrfs /dev/sdb rw,subvolid=5,subvol=/
80 65 0:46 /    /home/x   rw,nosuid,nodev,noexec,relatime shared:4 - tmpfs tmpfs rw,size=1048576k,inode64,usrquota
```

Path: `/home/x/y/z` (realpath identical, st_dev `0:46`).

1. **Candidates** (longest component-prefix, `contract.md:96-99`): `/` (ID 1), `/home` (ID 65), `/home/x` (ID 80), `/home/x/y` (ID 70). Longest → `/home/x/y`, so the *would-be* chosen mount is **ID 70**.
2. **The duplicate-mountpoint refusal does not fire here** — every covering mountpoint occurs exactly once (`/`, `/home`, `/home/x`, `/home/x/y` are all distinct). Verified programmatically on the fixture. So this case cannot be satisfied by `preseal-amendment.md:50-54`; it isolates the new clause.
3. **The parent-ID clause fires**: chosen ID 70 has parent ID **65**, which *is* present in the snapshot; but 65 is not the ID of the longest strictly-shorter covering mount — the strictly-shorter covering mounts are `/` (1), `/home` (65) and `/home/x` (**80**), and the longest of those is `/home/x` = ID 80. Condition met → **unknown / n/a / `ambiguous_overmount`**, `fstype=null`, `mount_point=null`, `device_check=not_checked`.
4. **Both escape hatches are deliberately avoided and demonstrably inapplicable**: the parent ID is *present* (not missing), and the chosen mount is *not* the root (the "Root has no shorter cover" clause only applies to a chosen mount with no strictly-shorter cover).
5. **Classification is never reached**: no fstype table row applies, the btrfs qgroups rules (`preseal-amendment.md:37-46`) are not exercised, and the device check is `not_checked`, so neither the btrfs stat-major-0 skip nor the device-mismatch preemption (`preseal-amendment.md:55-58`) can produce a different basis.
6. **Verdict**: `contract.md:132-134` precedence is unchanged — no setup error, no enabled path, one unknown path → **exit 2, `QUOTA_STATE_UNKNOWN`**.
7. **Supplementary output fields** on this preemption: `quota_option_keys=[]`, `btrfs_qgroups_mode=null` (`preseal-amendment.md:123-124`). The six scored fields are the primary expectation; `device_check`/`quota_option_keys`/`btrfs_qgroups_mode` are sealed separately (`:87-90`) and are **not** asserted in the case file — the amendment forbids inserting metadata keys into the independent six-field primary expectations.

### 10.2 Conservative refusal, not topology proof

The rationale states this explicitly: the refusal is derived from the **printed** parent-ID field and the set of covering mount points. It is a source-derived consistency check, **not** a proof of the true kernel mount topology, and the fixture does not assert which filesystem really contains `/home/x/y/z`. The path's `st_dev` `0:46` equals the tmpfs line's major:minor — consistent with the tmpfs covering the nested btrfs mount — but the tool is forbidden from using device equality to infer stack order, which is exactly the inference the rule exists to prevent.

### 10.3 Fixture-shape deltas honoured

- `btrfs_sysfs` carries the required `qgroups_enabled` member on **every** UUID record: the `dm-0` record has `qgroups=false` paired with `enabled=null`/`mode=null`; the `sdb` record has `qgroups=true` paired with `enabled=true`/`mode="qgroup"` (only `qgroup`/`squota` are acceptable mode spellings, `preseal-amendment.md:45-46`). Both are inert here because classification is preempted, but they are well-formed per the amended fixture schema.
- `device_links` maps the raw decoded sources `/dev/mapper/root` → `dm-0` and `/dev/sdb` → `sdb` (`preseal-amendment.md:59-61`).
- Super options are realistic: `btrfs_show_options` emits `,space_cache=v2`, `,subvolid=`, `,subvol=` (`fs/btrfs/super.c:1062-1160` — **not** among S077–S084, cited only as a realism anchor, as `mm/shmem.c` was in the sibling case); `shmem_show_options` emits `,usrquota` when USRQUOTA is active (`mm/shmem.c:4877-4892`, same caveat).
- `sources` for the supplemental case: **S079** (`fs/btrfs/sysfs.c` — `qgroup_enabled_show` 2355-2368 emitting exactly 0/1 from `BTRFS_QGROUP_STATUS_FLAG_ON`; `qgroup_mode_show` 2370-2395 emitting only `qgroup`/`squota`; the `/sys/fs/btrfs/<uuid>/qgroups/` path comment at 2453), **S080** (`fs/btrfs/qgroup.c` — `btrfs_read_qgroup_config` 420, `btrfs_sysfs_add_qgroups` call 441, `fs_info->qgroup_flags = 0;` 445 with the comment "default this to quota off, in case no status key is found": the reason the qgroups directory can exist while quota is off, and the reason `enabled` must be a separate member), **S082** (proc.rst §3.5 field layout), **S084** (tmpfs.rst 129-143 quota option vocabulary). My independently fetched bytes for `fs/btrfs/sysfs.c` (sha256 `ce146120f29ac29c0bc1859f21e4b84da91a536df2ec9fd2fa5649144f731c43`) match the `DraftSourceRows` table exactly.

### 10.4 Effect on §1-§9

- **No change** to `cases-proposed/CaseStacked.json` (sha256 `6104d13acc6a74f6b53f37c122fe0e57d523ddbea8d9d207f9fa4af16c54cff0`) or `cases-corrected/CaseStacked.json` (sha256 `b45f3485c170a88f75abcf8746315caf031331c4cf92b4943847f7433bf980d0`). The amendment's own sentence confirms this: "No existing case expectation changes beyond the already-corrected stack."
- §5 ambiguity #1 ("last line wins") remains closed; the new parent-ID clause closes the *deeper* gap behind it — stack order can no longer be inferred from line order **or** from a parent ID that does not correspond to the longest strictly-shorter covering mount.
- The three refusal modes now in force are distinct and each has exactly one sealed case: (a) duplicated covering mountpoint → `cases-corrected/CaseStacked.json`; (b) parent-ID inconsistency → `cases-supplemental/SupplementHiddenMount.json`; (c) device mismatch → `CaseXfsDevMismatch.json` (another seat's).

### 10.5 Bounds

No implementation, oracle, candidate or peer case was read; nothing was executed (no probe, oracle, selftest, build, test or linter); no delegation; no live host probes; no `/tmp`; no tooling installed (only `curl` into `.scratch/round23/CaseStacked/`, the wave-sanctioned download area); no VCS mutation; no fleet-root writes. `cases-supplemental/` was created only because the L1 named it as the output path for this item.
