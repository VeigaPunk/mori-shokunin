# CaseEnabledPlusUnknown — C2 fixture case (round 23)

Seat: `MadoR22-2.CaseEnabledPlusUnknown-8` (wave-1 fixture-case author, reviewer role).

Case file written (exactly one):
`/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/cases-proposed/CaseEnabledPlusUnknown.json`
sha256 `73b489c634cfd1d61fef35f1f7d9cbc1cc669685585b80811163330feb57d8ff`, 6449 bytes.
Object keys: `schema` (`mori-quota-case-v1`), `id` (`CaseEnabledPlusUnknown`), `scenario`,
`fixture`, `expected`, `rationale`, `sources` — matching the sibling case convention.

Independence: derived from `contract.md` (§C2, frozen at lane commit
`4dc80c1be48308075e83af17f15fbfe7e95e6cb8`) and the named kernel sources only. I did not open
`.ufo/waves/round-23/build/ImplQuota/` or `.scratch/round23/ImplQuota`. I did not consult any
oracle. A repo-wide grep for the S-ids incidentally surfaced *rationale prose* of sibling case
files (CaseUnsupported, CaseTmpfsHardlimit, CaseXfsDevMismatch, …) before my case was fixed;
I did not copy any expectation from them — my mount points (`/srv/quota`, `/mnt/nfs4`), device
numbers (`0:57`, `0:82`) and super-option text are my own construction, and my expectation is
derived step by step below from the contract table and the kernel anchors.

## 1. Scenario

Two paths in one fixture:

| path | realpath | fstype | mount point | super options (last field) | expected state |
|---|---|---|---|---|---|
| `/srv/quota/data` | `/srv/quota/data` | `tmpfs` | `/srv/quota` | `rw,size=1626620k,nr_inodes=406655,inode64,usrquota` | enabled / enforced / `tmpfs_quota_option` |
| `/mnt/nfs4/data` | `/mnt/nfs4/data` | `nfs4` | `/mnt/nfs4` | `rw,vers=4.2,hard,proto=tcp,timeo=600,retrans=2,sec=sys,rsize=1048576,wsize=1048576` | unknown / n/a / `unsupported_fstype` |

Run verdict: exit **1**, finding_id **`QUOTA_ENABLED`** — the enabled sibling must win, the
unknown sibling must not downgrade it, and the unknown path must still be reported in `paths`.

## 2. Derivation, step by step

1. **Fixture schema.** Contract §C2: `mori-quota-fixture-v1` is a JSON object with *exact* keys
   `schema`, `mountinfo`, `paths`, `device_links`, `btrfs_sysfs`; missing/extra top-level keys,
   non-absolute paths, malformed `st_dev`, malformed JSON or an unparseable mountinfo line are
   setup errors (exit 2 `QUOTA_SETUP`), never a partial verdict. My fixture has exactly those five
   keys, two absolute paths, and `st_dev` strings in `MAJ:MIN` form (`0:57`, `0:82`).
   `device_links` and `btrfs_sysfs` are populated consistently with the inert btrfs root line
   (source `/dev/mapper/root` → `dm-0`; one uuid listing device `dm-0`, `qgroups` false).

2. **mountinfo realism (S082).** `Documentation/filesystems/proc.rst` §3.5 (v7.2, lines
   1965–1990) fixes the layout: (1) mount ID, (2) parent ID, (3) major:minor, (4) root,
   (5) mount point, (6) mount options, optional `tag[:value]` fields, (m+1) the `-` separator,
   (m+2) filesystem type, (m+3) mount source, (m+4) super options; "Parsers should ignore all
   unrecognised optional fields." Every one of my six lines carries exactly fields (1)…(6), the
   separator, fstype, source and super options — 10 whitespace-separated fields, separator at
   index 6 — so no line can be read as unparseable. Kernel confirmation of the emitter:
   `fs/proc_namespace.c` `show_mountinfo()` prints `r->mnt_id`, `r->mnt_parent->mnt_id`,
   `MAJOR(sb->s_dev):MINOR(sb->s_dev)`, the root path, the mount point via
   `seq_path_root(..., " \t\n\\")`, ` ro`/` rw` plus the per-mount flags, then `" - "`, the type,
   the devname, ` ro`/` rw`, `show_sb_opts()` and `sb->s_op->show_options()`. So the *last* field
   of each line is the super-options string — exactly where the contract reads quota keys from.

3. **Mount resolution.** Contract §C2: candidates are mounts whose mount point equals the
   realpath, is `/`, or is a prefix of the realpath at a `/` boundary; the longest mount point
   wins, ties broken by the last line. For `/srv/quota/data` the candidates are the btrfs root
   `/` and the tmpfs `/srv/quota`; `/srv/quota` is longer, so tmpfs is chosen. For
   `/mnt/nfs4/data` the candidates are `/` and `/mnt/nfs4`; `/mnt/nfs4` is longer and is chosen.
   The `proc`, `sysfs`, `devtmpfs` and btrfs lines are inert for these two paths but make the
   text structurally realistic (a real `/proc/self/mountinfo` always carries them).

4. **Device check.** Contract §C2: "If chosen fstype is not btrfs and its major:minor ≠ the
   path's `st_dev` → `unknown` basis `device_mismatch`." Both chosen fstypes are non-btrfs, so
   this branch is reachable and must *not* fire: the fixture sets each path's `st_dev` equal to
   its chosen mount's major:minor (`0:57` tmpfs, `0:82` nfs4). That equality is the normal
   non-btrfs situation, because the kernel prints the superblock device in the mountinfo
   major:minor field (`MAJOR(sb->s_dev):MINOR(sb->s_dev)`) and a file on that filesystem reports
   the same `st_dev`. (For btrfs the mismatch is expected — per-subvolume anonymous `st_dev`,
   S081 — but no probed path resolves to btrfs here, so `btrfs_subvolume_skipped` is not exercised
   and no btrfs expectation is asserted.)

5. **Path 1 classification — tmpfs.** Contract table row: *tmpfs | any of `quota`,`usrquota`,
   `grpquota` or a key ending `_hardlimit` | enabled | enforced | `tmpfs_quota_option`*. The
   tmpfs line's last field contains the key `usrquota` (key = text before `=`), so the row
   applies: `quota_state enabled`, `enforcement enforced`, `basis tmpfs_quota_option`.
   Kernel anchor **S084** (`Documentation/filesystems/tmpfs.rst` v7.2, quota mount-option table,
   lines 129–143): `usrquota` = "User quota accounting and enforcement is enabled on the mount",
   `quota` = "User and group quota accounting and enforcement is enabled on the mount",
   `grpquota` = the group equivalent, and the four `*_hardlimit` options set global limits.
   The kernel emits these flags into the mountinfo super-options field through the tmpfs
   `show_options` callback (`mm/shmem.c` `shmem_show_options()` prints `,usrquota` when
   `sb_has_quota_active(sb, USRQUOTA)` is true, `,grpquota` likewise, then the
   `*_hardlimit=<bytes>` entries), so `usrquota` in the last field is realistic. The value bytes
   of the size/inode entries are immaterial: the contract parses keys only.

6. **Path 2 classification — nfs4.** `nfs4` is not xfs, not btrfs, not ext2/ext3/ext4 and not
   tmpfs, so the table's final row applies: *other | — | unknown | n/a | `unsupported_fstype`*.
   The nfs4 super options contain no quota key, so nothing else can be inferred, and the
   contract's limits state plainly "no NFS/server-side or overlay/fuse quota" — the probe must
   not guess a server-side quota state from mount options. Expected: `quota_state unknown`,
   `enforcement n/a`, `basis unsupported_fstype`.
   Note this is exactly the branch that a `device_mismatch` would otherwise pre-empt, which is
   why step 4's st_dev equality matters for this path.

7. **Verdict precedence.** Contract §C2: "setup error → 2 `QUOTA_SETUP`; else any `enabled` → 1
   `QUOTA_ENABLED` (positive evidence is never hidden by an unknown sibling); else any `unknown`
   → 2 `QUOTA_STATE_UNKNOWN`; else 0 `QUOTA_DISABLED`." No setup error; one path is enabled ⇒
   **exit 1, finding_id `QUOTA_ENABLED`**. `QUOTA_ENABLED` is a runway-reporting finding, not a
   failure claim, and the nfs4 path is still emitted with its own unknown state — the case is
   precisely the anti-suppression check.

## 3. Expected object

```json
{"exit": 1, "finding_id": "QUOTA_ENABLED",
 "paths": [
   {"path": "/srv/quota/data", "fstype": "tmpfs", "mount_point": "/srv/quota",
    "quota_state": "enabled", "enforcement": "enforced", "basis": "tmpfs_quota_option"},
   {"path": "/mnt/nfs4/data", "fstype": "nfs4", "mount_point": "/mnt/nfs4",
    "quota_state": "unknown", "enforcement": "n/a", "basis": "unsupported_fstype"}]}
```

Each expected path object carries **exactly** the six keys the case brief requires (`path`,
`fstype`, `mount_point`, `quota_state`, `enforcement`, `basis`); the tool's extra output fields
(`device_check`, `quota_option_keys`, `btrfs_qgroups_mode`) are deliberately not asserted here.

## 4. Source anchors relied on

| S-id | source | anchor used |
|---|---|---|
| S082 | `Documentation/filesystems/proc.rst` (Linux v7.2) | §3.5, lines 1965–1990: field layout (1)…(6), optional fields until `-`, (m+2) fstype, (m+3) mount source, (m+4) super options; "Parsers should ignore all unrecognised optional fields." |
| S084 | `Documentation/filesystems/tmpfs.rst` (Linux v7.2) | quota mount-option table, lines 129–143: `quota`, `usrquota`, `grpquota` = accounting **and enforcement** enabled on the mount; `usrquota_block_hardlimit`, `usrquota_inode_hardlimit`, `grpquota_block_hardlimit`, `grpquota_inode_hardlimit` = global limit setters; remount note line 145. |

Corroborating code opened read-only for realism only, **not** S-numbered in this round and
therefore not cited in the case file's `sources`:
`fs/proc_namespace.c` (`show_mountinfo()`, `show_sb_opts()`, `seq_path_root(..., " \t\n\\")`),
`mm/shmem.c` (`shmem_show_options()` printing `,usrquota`/`,grpquota`/`*_hardlimit=<bytes>`),
`fs/xfs/xfs_super.c` and `Documentation/admin-guide/xfs.rst` (not needed for this case's rows).

S-id mapping note: `corpus/SOURCES.md` ends at S076; rows S077–S084 are drafted this round by the
source-scribe seats. I use the wave-1 scribe order (SrcXfsDoc S077, SrcXfsShowargs S078,
SrcBtrfsSysfs S079, SrcBtrfsQgroup S080, SrcBtrfsGetattr S081, SrcProcMountinfo S082, SrcExt4Doc
S083, SrcTmpfsDoc S084), which is pinned by the contract's own citation "per-subvolume anonymous
st_dev, **S081**" landing on `fs/btrfs/inode.c` (the fifth scribe). This is an inference, not a
registry fact: if L1 numbers the rows differently, this case's `sources` array must be remapped;
the expectation itself does not change, because it is derived from the contract table.

## 5. Contract ambiguities found (for L1 / the oracle author)

* **A1 — `expected.exit` vs the tool's `exit_code`.** The contract's output object names the
  field `exit_code`; the case brief names the expected field `exit`. I used `exit` per the brief,
  but the oracle must map `expected.exit` ↔ tool `exit_code` explicitly, otherwise every case
  fails on a field-name mismatch rather than on behaviour.
* **A2 — order of the output `paths` array is unspecified.** The contract says
  `paths: [{…}]` and "per-path (path, fstype, mount_point, quota_state, enforcement, basis)
  exactly", but never states whether the array preserves the `--path`/fixture order or is sorted.
  I assume **input order** (tmpfs first, nfs4 second). The oracle should compare per-path by
  `path` rather than by position, or the contract should fix the order.
* **A3 — `enforcement` for unknown/disabled rows is the literal string `"n/a"`.** The contract's
  table prints `n/a` in that column; a `null` would also be a defensible reading. I used the
  literal `"n/a"` (consistent with the sibling convention). The oracle must fix one spelling.
* **A4 — the contract reads quota keys from the super-options field, but S082 only documents the
  *layout*.** proc.rst §3.5 says nothing about which filesystem populates which key; the fact
  that tmpfs prints `usrquota` into the super-options field comes from `mm/shmem.c`
  `shmem_show_options()`, which is **outside** the S077–S084 set. The tmpfs row of the C2 table
  is therefore not fully backed by a registered source row. Recommend adding `mm/shmem.c` to the
  round's source set (or registering `shmem_show_options` under S084's row), otherwise the
  tmpfs-enabled row rests on documentation of mount options rather than on the observable
  mountinfo surface the probe actually reads.
* **A5 — `device_check` is not in the asserted key set.** The contract's per-path output includes
  `device_check`, but the case brief restricts the expected objects to six keys, so `device_check`
  (`match` here for both paths) is left unasserted by this case. If the oracle compares it, it
  must be added to the expected objects on L1's instruction.
* **A6 — informational, tmpfs `usrquota` alone.** S084 attributes "accounting **and
  enforcement**" to the `quota`/`usrquota`/`grpquota` flags, and describes the four `*_hardlimit`
  options only as global limit setters. The contract maps a lone `_hardlimit` key to
  `enforcement=enforced` as well; the sources support the flags reading but not a standing-alone
  hardlimit. This case does not depend on it (it uses `usrquota`), and no expectation change is
  warranted.
* **A7 — `device_mismatch` vs `unsupported_fstype` ordering.** The contract states the device
  check before the classification table, so a non-btrfs path whose `st_dev` differs from the
  mount's major:minor yields `device_mismatch` and never reaches `unsupported_fstype`. This case
  fixes the equality deliberately so the `unsupported_fstype` row is reachable and observable.

## 6. Verification performed

* JSON parses; top-level keys exactly `schema,id,scenario,fixture,expected,rationale,sources`;
  `schema == "mori-quota-case-v1"`, `id == "CaseEnabledPlusUnknown"`.
* `fixture` keys exactly `schema,mountinfo,paths,device_links,btrfs_sysfs`;
  `fixture.schema == "mori-quota-fixture-v1"`.
* All six mountinfo lines re-parsed against the §3.5 layout: separator at index 6, 10 fields per
  line, `major:minor` well formed, root and mount point absolute, mount options beginning
  `rw`/`ro`.
* Both `paths` entries: keys exactly `path,realpath,st_dev`; absolute paths; `st_dev` in
  `MAJ:MIN` form.
* `expected` keys exactly `exit,finding_id,paths`; each expected path object keys exactly
  `path,fstype,mount_point,quota_state,enforcement,basis`; every `quota_state`/`enforcement`/
  `basis` value is a token taken verbatim from the contract's C2 table.
* No implementation, oracle, or sibling expectation was consulted for the expectation itself.
  No tests, builds, linters, or host probes were run: this wave's bounds forbid them for
  read-only seats, and the case is falsifiable only against the sealed implementation.

---

# Appendix — pre-seal amendment correction (appended after `preseal-amendment.md`)

Read `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/preseal-amendment.md`
before any candidate inspection or result. No candidate was opened, no C2 result was observed,
no implementation was read, and no test/build was run for this correction.

## A. Corrected case file

`/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/cases-corrected/CaseEnabledPlusUnknown.json`
sha256 `77440e32054aef813df90b9a22d9e03b526496a3b103940df0ff601bec775828`, 8680 bytes.
Same `id` (`CaseEnabledPlusUnknown`), same `schema` (`mori-quota-case-v1`), same top-level key
set (`schema, id, scenario, fixture, expected, rationale, sources`).

Original proposal **left untouched**: `.ufo/waves/round-23/cases-proposed/CaseEnabledPlusUnknown.json`
sha256 `73b489c634cfd1d61fef35f1f7d9cbc1cc669685585b80811163330feb57d8ff` — identical to the
digest recorded in §1 above, so the proposal remains the historical record and the corrected file
is a separately named, separately sealed artifact.

## B. Delta — exactly one change

The only difference between the original proposal and the corrected case is one added member in
the single `btrfs_sysfs` UUID record:

```
btrfs_sysfs["9f3c1c2e-6b47-4a55-9d0e-71c2b6f4a803"] =
  before: {"devices": ["dm-0"], "qgroups": false, "qgroups_mode": null}
  after:  {"devices": ["dm-0"], "qgroups": false, "qgroups_enabled": null, "qgroups_mode": null}
```

Machine-verified: `scenario`, `expected`, `sources`, and every other fixture member
(`schema`, `mountinfo`, `paths`, `device_links`) are byte-for-byte equal between the two files;
only `btrfs_sysfs` differs, and only by the added key.

**Why this value.** Amendment: "Add required fixture member `qgroups_enabled` to each
btrfs_sysfs UUID record: true/false/null. `qgroups` false must pair with `enabled=null/mode=null`."
This record has `qgroups=false`, so `qgroups_enabled=null` and `qgroups_mode=null` are the
mandated pairing. "Missing/extra record keys setup" — the record now carries exactly
`devices`, `qgroups`, `qgroups_enabled`, `qgroups_mode`, and the types are exact
(bool / bool-or-null / mode-or-null).

## C. Amendment rules checked against this case — none of the three named corrections applies

* **"update enabled btrfs basis to `btrfs_qgroups_enabled`"** — no probed path resolves to a
  btrfs mount. The fixture's btrfs root line (`/` , source `/dev/mapper/root`) is inert: the
  tmpfs path resolves to `/srv/quota` and the nfs4 path to `/mnt/nfs4`, both strictly longer
  component-prefix candidates than `/`. No btrfs basis token is asserted anywhere in this case,
  so no basis rename is required here. (Had a btrfs path been probed, the record's
  `qgroups_enabled` would have driven the outcome; with `qgroups=false` the dir is absent and
  the amendment's "absent dir retains disabled/n/a/`btrfs_qgroups_dir_absent` only on a successful
  parent inspection" would apply — still not asserted here.)
* **"ext positive cases become unknown/n/a/`ext_quota_option_unverified`"** — no probed path is
  ext2/ext3/ext4; the fixture contains no ext mount at all. Not applicable.
* **"duplicated-covering-point case becomes unknown/null fstype+mountpoint/`ambiguous_overmount`"**
  — no mount point in this fixture occurs more than once. Machine-verified over the six parsed
  lines: `{/proc:1, /sys:1, /dev:1, /:1, /srv/quota:1, /mnt/nfs4:1}` — zero duplicates, so the
  amendment's ambiguous-overmount refusal (unknown / n/a / `ambiguous_overmount`,
  fstype=null, mount_point=null, device_check=not_checked) is not triggered and both paths keep
  their real fstype and mount point.

## D. Other amendment clauses re-verified against this case (expectations unchanged)

* **Mount resolution**: empty trailing lines ignored (the mountinfo text ends with `\n`, so it
  contributes no extra line — a trailing blank line must not be parsed as a malformed mount);
  separator and the last three fields parsed per chosen line, never file-wide; longest
  component-prefix selection; no duplicated covering mount point (above).
* **Device check**: mismatch preempts the filesystem table; btrfs skips equality only when the
  stat major is 0. Both probed fstypes are non-btrfs, so equality is live and is satisfied:
  `0:57` = tmpfs mount `0:57`, `0:82` = nfs4 mount `0:82`. Neither path takes
  `device_mismatch`. (Had the nfs4 st_dev differed, the nfs4 basis would have become
  `device_mismatch` rather than `unsupported_fstype` — the equality in the fixture is what makes
  the `unsupported_fstype` row observable.)
* **Fixture source resolution**: raw decoded source looked up in `device_links`, mapped basename
  compared against UUID `devices` lists. `/dev/mapper/root` → `dm-0`, and the single UUID lists
  `dm-0`, so the mapping is consistent (and inert for the two probed paths, whose fstypes are
  not btrfs).
* **Path rules**: nonempty, unique, normalized absolute `path`/`realpath` with no dot or dotdot
  components — verified; `st_dev` canonical decimal `MAJ:MIN` with no signs and no leading zeros
  except a bare `0` — verified (`0:57`, `0:82`); UUID key is a canonical UUID; `devices` and
  mapped `device_links` values are plain nonempty basenames without slashes or control chars.
* **XFS precedence** and **tmpfs hardlimit vocabulary**: no XFS path; the tmpfs path uses
  `usrquota`, a mechanism flag, so the amendment's narrowed hardlimit set (the four documented
  `usrquota_block_hardlimit` / `usrquota_inode_hardlimit` / `grpquota_block_hardlimit` /
  `grpquota_inode_hardlimit` keys only; an arbitrary `_hardlimit` suffix is not sufficient) does
  not bear on it, and "enforced describes mechanism flags, never a nonzero limit" is satisfied
  because `usrquota` is itself a mechanism flag.
* **Output tuples**: the original six scored fields are preserved verbatim
  (`path, fstype, mount_point, quota_state, enforcement, basis`); `device_check`, `quota_option_keys`
  and `ggroups_mode` remain unasserted by this case, as before.

## E. Corrected expectation (unchanged from the original proposal)

```
exit 1, finding_id QUOTA_ENABLED
/srv/quota/data  tmpfs  /srv/quota  enabled  enforced  tmpfs_quota_option
/mnt/nfs4/data   nfs4   /mnt/nfs4   unknown  n/a       unsupported_fstype
```

## F. Hashes

| artifact | sha256 | bytes |
|---|---|---|
| `.ufo/waves/round-23/cases-proposed/CaseEnabledPlusUnknown.json` (original, untouched) | `73b489c634cfd1d61fef35f1f7d9cbc1cc669685585b80811163330feb57d8ff` | 6449 |
| `.ufo/waves/round-23/cases-corrected/CaseEnabledPlusUnknown.json` (corrected) | `77440e32054aef813df90b9a22d9e03b526496a3b103940df0ff601bec775828` | 8680 |

Amendments consulted: `.ufo/waves/round-23/preseal-amendment.md` (C2 final rules; fixture,
device-check, mount-resolution, XFS/tmpfs/ext/btrfs clauses) and the frozen
`.ufo/waves/round-23/contract.md` §C2. No implementation, oracle, or sibling expectation was
read for the correction; no host probe, test, or build was run.
