# CaseExt4Usrquota — independent C2 fixture case (mori round 23)

Seat: `MadoR22-2.CaseExt4Usrquota-8` (leaf member; no subagent dispatch).
Case file: `.ufo/waves/round-23/cases-proposed/CaseExt4Usrquota.json`
(schema `mori-quota-case-v1`, id `CaseExt4Usrquota`).
Claim under test: C2 (FR2 quota-surface coverage capability, `tools/mori-quota-surface.py`).

Independence: derived only from `.ufo/waves/round-23/contract.md` (frozen at lane commit
`4dc80c1be48308075e83af17f15fbfe7e95e6cb8`) and the named kernel v7.2 sources
(proc.rst, ext4.rst). No candidate implementation, no oracle, no sibling case file was read
while deriving the expectation.

---

## 1. Scenario

An ext4 mount at `/srv/data` carries the `usrquota` quota option in its **super options**
(last mountinfo field). Two requested paths resolve to that mount — the mount point itself
(`/srv/data`) and a subdirectory (`/srv/data/projects/app`). The mount's `major:minor`
(`8:2`) equals the paths' `st_dev`, so the device check matches and the ext quota-option
row applies.

## 2. Fixture (`mori-quota-fixture-v1`, exactly the five contract keys)

`schema`, `mountinfo`, `paths`, `device_links`, `btrfs_sysfs` — no extra top-level keys,
no missing ones, so the contract's "missing/extra top-level keys → exit 2 `QUOTA_SETUP`"
rule is not triggered.

mountinfo (7 lines, each parsed per proc.rst §3.5 — fields 1–6, optional `tag[:value]`
fields, `-` separator, fstype, source, super options):

```
25 0 8:1 / / rw,relatime shared:1 - ext4 /dev/nvme0n1p2 rw,errors=remount-ro
26 25 0:21 / /proc rw,nosuid,nodev,noexec,relatime shared:11 - proc proc rw
27 25 0:22 / /sys rw,nosuid,nodev,noexec,relatime shared:7 - sysfs sysfs rw,nosuid,nodev,noexec
28 25 0:23 / /dev rw,nosuid shared:2 - devtmpfs devtmpfs rw,size=4028624k,nr_inodes=1007631,mode=755
29 25 259:3 / /home rw,relatime shared:4 - btrfs /dev/mapper/root rw,compress=zstd:3,ssd,discard=async,space_cache=v2,subvolid=257,subvol=/@home
30 25 0:41 / /srv rw,nosuid,nodev,noexec,relatime shared:9 - tmpfs tmpfs rw,nosuid,nodev,noexec,relatime,size=163840k,inode64
31 30 8:2 / /srv/data rw,relatime shared:13 - ext4 /dev/nvme0n1p4 rw,usrquota
```

Realistic-field notes: field 3 is `major:minor` as the kernel prints it (`8:1`, `0:21`,
`0:22`, `0:23`, `259:3`, `0:41`, `8:2`); field 4 is the mount root inside the filesystem
(`/`, and `/@home` for the btrfs subvolume, matching the host observation recorded in
`frozen/c2-expected-real.json`); field 6 is the per-mount option set (`rw,relatime`,
`shared:N` is an optional field); the `-` separator is followed by fstype, mount source and
the **super options** last field. `device_links` maps `/dev/mapper/root → dm-0` and
`btrfs_sysfs` records the one uuid that lists `dm-0` with `qgroups: false` — both inert for
this scenario (the chosen fstype is ext4, and the btrfs line at `/home` is not a covering
mount for either path), but they keep the fixture schema-complete and host-consistent.

## 3. Expected outcome (derived, not observed)

```
exit: 1
finding_id: QUOTA_ENABLED
paths:
  /srv/data           fstype ext4  mount_point /srv/data  enabled  unknown  ext_quota_option
  /srv/data/projects/app fstype ext4  mount_point /srv/data  enabled unknown  ext_quota_option
```

### 3.1 Mount resolution (contract §C2)

Candidate mounts for realpath `/srv/data`: mount point equals the realpath (`/srv/data`),
is `/` (the ext4 root at `8:1`), or is a `/`-boundary prefix (`/srv`, tmpfs at `0:41`).
**Longest mount point wins** → `/srv/data` (9 chars) beats `/srv` (4) and `/` (1). The
same mount covers `/srv/data/projects/app` by the prefix rule, so both paths report
`mount_point: /srv/data`.

### 3.2 Device check (contract §C2)

Chosen fstype is `ext4`, not btrfs, so the btrfs subvolume exemption does not apply.
Its `major:minor` `8:2` equals the paths' `st_dev` `8:2` → the check matches and
classification proceeds (no `device_mismatch`).

### 3.3 Quota classification (contract §C2 table, ext row)

Contract row: `ext2/ext3/ext4 | any of quota,usrquota,grpquota,prjquota,usrjquota,grpjquota
| enabled | unknown | ext_quota_option`. The super options of the chosen line are
`rw,usrquota`; comma-split with key = text before `=` yields the key `usrquota`, which is in
the listed set → `quota_state: enabled`, `enforcement: unknown`, `basis: ext_quota_option`.

`enforcement: unknown` (not `enforced`) is required by the contract row, and it is also the
honest reading of the source: ext4.rst:261-265 says the `quota, noquota, grpquota, usrquota`
options "are ignored by the filesystem. They are used only by quota tools to recognize
volumes where quota should be turned on" — i.e. the option is visible evidence of intent,
not evidence of enforcement. The contract's own limits section says the same
("ext quota feature in the superblock is unobservable without privileged tools").

### 3.4 Verdict precedence (contract §C2)

No setup error; at least one path is `enabled` → exit **1**, `finding_id` **QUOTA_ENABLED**
(a runway-reporting finding, not a failure claim).

## 4. Source anchors

| S-id | source | anchor used |
|---|---|---|
| S082 | `Documentation/filesystems/proc.rst` (Linux v7.2) | §3.5, lines 1965–1990: field layout `(1)` mount ID, `(2)` parent ID, `(3)` major:minor = "value of st_dev for files on filesystem", `(4)` root, `(5)` mount point, `(6)` mount options, optional `tag[:value]` fields until the `-` separator, then filesystem type, mount source, **super options**; "Parsers should ignore all unrecognised optional fields." |
| S083 | `Documentation/admin-guide/ext4.rst` (Linux v7.2) | lines 261–265 `quota, noquota, grpquota, usrquota` ("ignored by the filesystem … used only by quota tools to recognize volumes where quota should be turned on"); lines 267–271 `jqfmt=<quota type>, usrjquota=<file>, grpjquota=<file>` (the `key=value` forms the contract's "key = text before `=`" rule reduces to the keys `usrjquota` / `grpjquota`). |

Both were re-opened from the pinned upstream v7.2 raw URLs during this seat
(`raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/filesystems/proc.rst`,
`.../Documentation/admin-guide/ext4.rst`); line numbers above are from those fetches.

Kernel corroboration read but **not** registry-cited (it is outside the S077–S084 set the
contract fixes for this wave, so it anchors plausibility only, not the expectation):
`fs/ext4/super.c` — the mount-option table maps `usrquota` to
`EXT4_MOUNT_QUOTA | EXT4_MOUNT_USRQUOTA` (`MOPT_SET | MOPT_Q`) and `_ext4_show_options()`
prints quota option tokens that differ from the superblock default, which is how a quota
option can surface in the mountinfo super-options field.

## 5. Contract ambiguities found (reported, not resolved unilaterally)

1. **ext4 `noquota` has no row.** The contract's ext table has exactly two rows: "any of
   quota,usrquota,grpquota,prjquota,usrjquota,grpjquota → enabled" and "none of them →
   unknown / `ext_quota_superblock_unobservable`". `noquota` (documented for ext4 at
   ext4.rst:261, and a real ext4 mount option in `fs/ext4/super.c`) is in neither row. An
   ext4 mount whose super options carry only `noquota` therefore falls into the "none of
   them" row → `unknown` / `ext_quota_superblock_unobservable`, whereas xfs has an explicit
   `noquota → disabled` row. The asymmetry is consistent with "the ext superblock quota
   feature is unobservable", but the contract never says so. Not exercised by this case
   (my fixture has `usrquota`), but it should be pinned before the oracle is sealed — a
   fixture carrying `noquota` alone would be ambiguous under the current text.
2. **"enforcement" vocabulary for ext.** The contract's ext row uses `unknown` in the
   enforcement column while the xfs and tmpfs rows use `enforced` / `accounting_only`. The
   same token `unknown` therefore means "state not determined" in the `quota_state` column
   and "enforcement not determined" in the `enforcement` column. My expectation follows the
   table literally, but the token is overloaded.
3. **Superblock-feature case is invisible.** An ext4 filesystem with the on-disk quota
   feature enabled and no quota mount option prints no quota key in super options, so it
   classifies as `unknown` / `ext_quota_superblock_unobservable` even though quota is
   actually on. The basis token names this honestly, but a reader could mistake
   `ext_quota_superblock_unobservable` for "quota off". Worth stating in the tool's own
   `limits` text that `unknown` for ext means *unobservable*, never *disabled*.
4. **Where the ext4 quota key actually lives.** The contract reads quota keys from the
   super-options field only (last mountinfo field). ext4 prints its quota option tokens in
   that field only when they differ from the superblock default, so a fixture writer must
   put the quota key in the **last** field, not in field 6 (per-mount options). I did, and
   recorded the field-6 vs super-options distinction in the rationale so an oracle author
   does not look in the wrong place.

## 6. Verification and hygiene

- Case JSON written once and re-read programmatically: top-level keys are exactly
  `schema, id, scenario, fixture, expected, rationale, sources`; fixture keys are exactly
  `schema, mountinfo, paths, device_links, btrfs_sysfs`; fixture `schema` is
  `mori-quota-fixture-v1`; case `schema` is `mori-quota-case-v1`; all 7 mountinfo lines have
  the expected field count; `expected.paths` objects carry exactly
  `path, fstype, mount_point, quota_state, enforcement, basis`; every value is a token
  taken verbatim from the contract (`enabled`, `unknown`, `ext_quota_option`,
  `QUOTA_ENABLED`).
- No test, build, lint or smoke run was executed (forbidden in this wave; L1 measures
  after integration).
- No production file was edited; only the assigned case file and this report were written.
- No host probe, mount, quotactl, btrfs/xfs quota command, or privileged interface was
  invoked. The only reads were upstream raw source files over HTTPS.
- Tooling: **no installs and no updates were performed** in this seat — the task required
  only `curl`/`python3`/`git`-free local file writes, all already present. Nothing to
  record against the operator tooling directive.

---

# CORRECTION (appended) — pre-seal amendment, superseding §1–§6 above

Read `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/preseal-amendment.md`
before any candidate inspection or result. This correction was authored **before** any
ImplQuota candidate was opened and before any C2 candidate was run; no implementation was
read and no test was executed. The amendment states it supersedes only erroneous/ambiguous
original clauses and leaves `contract.md`, `frozen/c1-*` and the real controls at
`4dc80c1` immutable history.

## C.1 What changed and why (derivation + delta)

Corrected case file (new, same id, original proposal left byte-untouched):
`.ufo/waves/round-23/cases-corrected/CaseExt4Usrquota.json`

| # | Original proposal | Corrected case | Authority |
|---|---|---|---|
| 1 | `quota_state: enabled` for the ext4 path | `quota_state: unknown` | Amendment §C2 ext2/3/4 clause: "quota_state ALWAYS unknown, enforcement n/a". A mount-option hint does not prove runtime accounting enabled. |
| 2 | `enforcement: unknown` | `enforcement: n/a` | Same clause: ext enforcement is always `n/a` (not `unknown`). |
| 3 | `basis: ext_quota_option` | `basis: ext_quota_option_unverified` | Same clause: "If any quota-related option key is present use basis `ext_quota_option_unverified`; otherwise retain `ext_quota_superblock_unobservable`." My fixture's super options carry `usrquota`, a quota-related key, so the unverified basis applies and the superblock-unobservable basis is **not** used. |
| 4 | `exit: 1`, `finding_id: QUOTA_ENABLED` | `exit: 2`, `finding_id: QUOTA_STATE_UNKNOWN` | Verdict precedence re-evaluated under the corrected classification: no setup error, no `enabled` path, at least one `unknown` path → exit 2 `QUOTA_STATE_UNKNOWN`. |
| 5 | `btrfs_sysfs` UUID record had keys `devices, qgroups, qgroups_mode` only | adds required member `qgroups_enabled: null` (record keys now exactly `devices, qgroups, qgroups_enabled, qgroups_mode`) | Amendment §C2 btrfs clause: "Add required fixture member `qgroups_enabled` to each btrfs_sysfs UUID record: true/false/null. qgroups false must pair with enabled=null/mode=null." My record is a decoy with `qgroups: false`, so `qgroups_enabled: null` and `qgroups_mode: null` are the mandated pairing. This record is not a positive btrfs case, so the `btrfs_qgroups_enabled` basis does not arise here. |
| 6 | — | duplicated-covering-point rule not triggered | Amendment: "if ANY covering mountpoint occurs more than once, refuse classification as unknown/n/a/`ambiguous_overmount`, fstype=null, mount_point=null, device_check=not_checked". My fixture has each covering mount point (`/`, `/srv`, `/srv/data`) exactly once, so classification proceeds normally and no `ambiguous_overmount` expectation applies to this case. |

Unrelated content deliberately **preserved**: the fixture's mountinfo text (all 7 lines),
the two `paths` entries, `device_links`, the scenario's shape, the mount-resolution
outcome (`mount_point: /srv/data` for both paths via longest component-prefix), the device
result (`8:2 == 8:2` → `match`), and the `sources` list `[S082, S083]`.

## C.2 Corrected derivation

1. **Mount resolution** (amendment mount-resolution clause; S082 proc.rst §3.5): covering
   mount points for realpath `/srv/data` are `/` (ext4 root, `8:1`), `/srv` (tmpfs,
   `0:41`), `/srv/data` (ext4, `8:2`). Longest component-prefix wins → `/srv/data`;
   `/srv/data/projects/app` is covered by the same mount. Each covering mount point occurs
   once → no `ambiguous_overmount` refusal. The separator and the last three fields are
   taken per chosen line; the trailing newline is an empty trailing line and is ignored.
2. **Device check** (amendment device clause): chosen fstype is ext4, not btrfs, so the
   btrfs "stat major is 0" exemption does not apply; mount `8:2` equals path `st_dev`
   `8:2` → `device_check: match`, and the mismatch preemption does not fire.
3. **Classification** (amendment ext clause): super options of the chosen line are
   `rw,usrquota`; key = text before `=` → `usrquota`, which is in the ext quota-related
   vocabulary (original keys plus `noquota` and `jqfmt`) and is therefore **present** →
   `quota_state: unknown`, `enforcement: n/a`, `basis: ext_quota_option_unverified`.
   Supplementary sealed fields for this case: `device_check: match`,
   `quota_option_keys: ["usrquota"]` (sorted, values never emitted),
   `btrfs_qgroups_mode: null`.
   S083 (ext4.rst:261–265) is the anchor: the plain quota flags "are ignored by the
   filesystem. They are used only by quota tools to recognize volumes where quota should
   be turned on" — visible intent, not proof of runtime accounting.
4. **Verdict precedence**: no setup error; no `enabled` path; `unknown` present → exit **2**,
   `finding_id` **QUOTA_STATE_UNKNOWN**.
5. **Fixture source resolution** (amendment): the chosen line's raw decoded source is
   `/dev/nvme0n1p4`, absent from `device_links`, so `basename(source) = nvme0n1p4` would
   be compared against the UUID `devices` lists. Inert for this case because the chosen
   fstype is not btrfs; the single UUID record is a decoy.

## C.3 Effect on the ambiguities reported in §5

- Ambiguity 1 (ext4 `noquota` has no row) is **resolved by the amendment**: the ext
  vocabulary now explicitly adds `noquota` and `jqfmt`, and classification is `unknown`
  regardless. My earlier note is retained as history; the corrected case does not depend
  on it (the fixture uses `usrquota`).
- Ambiguity 2 (overloaded `unknown` token) is resolved: ext `enforcement` is now always
  `n/a`, so `unknown` appears only in the `quota_state` column for ext.
- Ambiguity 3 (superblock-feature case invisible) is resolved in favour of the honest
  reading: `ext_quota_option_unverified` names the state precisely — an option key was
  seen, but runtime accounting is unverified — and `ext_quota_superblock_unobservable`
  remains for the no-key case.
- Ambiguity 4 (where the ext4 quota key lives) stands and is unchanged: the key is read
  from the **super options** (last mountinfo field), not field 6. The corrected fixture
  keeps the key in the last field.

## C.4 Hygiene for this correction

- No implementation, candidate, oracle or driver was read; no test, build, lint or smoke
  run was executed.
- The original proposal `.ufo/waves/round-23/cases-proposed/CaseExt4Usrquota.json` was
  **not** edited (mtime 2026-10-21T14:36:36-0300, unchanged); the corrected case is a
  separate file in the authorized `cases-corrected/` directory.
- Only this seat's own files were written; no delegation, no background job, no host probe
  and no privileged quota interface was used.
- Tooling: no installs or updates were performed (nothing beyond local file writes and
  upstream HTTPS reads was needed).

## C.5 Final hashes (SHA-256 of file bytes)

| file | sha256 |
|---|---|
| `.ufo/waves/round-23/cases-corrected/CaseExt4Usrquota.json` | `4db2fcd87bb1a2efcfadaff13311426eb8a6fc129663cfa486190a93ac959cda` |
| `.ufo/waves/round-23/cases-proposed/CaseExt4Usrquota.json` (original, untouched) | `ba8b7f2018a33c1e1c9b13c914b98dee5ee33b0a5bfd37c2b5b9d2a24fa70b87` |
