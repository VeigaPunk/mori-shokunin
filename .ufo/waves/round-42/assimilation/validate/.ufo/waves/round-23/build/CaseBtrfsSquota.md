# CaseBtrfsSquota — C2 fixture case (btrfs, qgroups true, mode "squota")

Seat: `CaseBtrfsSquota` (agent `MadoR22-2.CaseBtrfsSquota-8`), wave `mori-r23-build`, role reviewer.
Case file written: `.ufo/waves/round-23/cases-proposed/CaseBtrfsSquota.json` (exactly one file).
Independence: derived from `.ufo/waves/round-23/contract.md` §C2 and the kernel sources under
`.scratch/round23/src/` only. No candidate implementation, no oracle, no sibling case file was read.
No host probe was run (this seat's item names no live read). No tool was installed or updated this
wave (none needed; python3 from the base system was used only to re-parse the JSON I authored).

## 1. Case as written

| field | value |
|---|---|
| schema / id | `mori-quota-case-v1` / `CaseBtrfsSquota` |
| scenario | btrfs subvolume path whose single mapped uuid has `qgroups` true and `qgroups_mode` `"squota"` → enabled / unknown / `btrfs_qgroups_dir_present`, exit 1 `QUOTA_ENABLED` |
| fixture path | `/srv/data` (realpath `/srv/data`, `st_dev` `0:57`) |
| fixture mountinfo | 4 lines per proc.rst §3.5: `ext4 /` , `btrfs /srv` (source `/dev/mapper/srv`, `0:30`), `proc /proc`, `tmpfs /run` |
| device_links | `{"/dev/mapper/srv": "dm-3"}` |
| btrfs_sysfs | `6f0c9e42-58ab-4d71-9c30-6b1fe4ad2753` → devices `["dm-3"]`, `qgroups` true, `qgroups_mode` `"squota"` |
| expected | exit `1`, finding_id `QUOTA_ENABLED`, one path: `path /srv/data`, `fstype btrfs`, `mount_point /srv`, `quota_state enabled`, `enforcement unknown`, `basis btrfs_qgroups_dir_present` |
| sources cited | S079, S080, S081, S082 |

## 2. Derivation, step by step

1. **Mount selection.** Contract §C2 "Mount resolution (per path)": parse mountinfo per proc.rst §3.5;
   candidate mounts are those whose mount point equals the realpath, is `/`, or is a prefix of the
   realpath followed by `/`; choose the longest mount point, ties broken by the last line.
   For realpath `/srv/data` the candidates are `/` (line 1) and `/srv` (line 2); `/srv` is longer and
   wins → `fstype btrfs`, `mount_point /srv`. The `proc` and `tmpfs` lines never cover `/srv/data`.
   Anchor: S082 — `Documentation_filesystems_proc.rst:1965-1990` (§3.5 field layout: mount ID, parent
   ID, major:minor, root, mount point, mount options, optional fields, `-`, filesystem type, mount
   source, super options). Each fixture line was re-parsed against that layout.
2. **Device → uuid mapping.** The mount source `/dev/mapper/srv` resolves (contract real-mode input
   `os.path.realpath(mount_source)` basename; fixture equivalent `device_links`) to device name
   `dm-3`. Exactly one uuid lists `dm-3` in `devices` → the btrfs table row that applies is the
   "exactly one uuid" one; the `btrfs_device_unmapped` row (zero or several uuids) is not reached.
3. **Classification.** Contract table, btrfs row *"source basename maps to exactly one uuid whose
   `qgroups` is true"* → `quota_state enabled`, `enforcement unknown`, `basis btrfs_qgroups_dir_present`.
   The row does not branch on the mode text, so `"squota"` does not change any of the three tokens.
   Kernel anchors for what "squota" means and when the attribute exists:
   - S079 — `fs_btrfs_sysfs.c:2355-2368` (`qgroups/enabled` attribute) and `:2370-2395`
     (`qgroups/mode` attribute; `qgroup_mode_show` emits `"qgroup\n"` for `BTRFS_QGROUP_MODE_FULL` and
     `"squota\n"` for `BTRFS_QGROUP_MODE_SIMPLE`), i.e. the mode string is a property of the
     `qgroups` directory that exists when quota is enabled.
   - S080 — `fs_btrfs_qgroup.c:33-50` (`btrfs_qgroup_mode`: `DISABLED` unless `BTRFS_FS_QUOTA_ENABLED`,
     `SIMPLE` when `BTRFS_QGROUP_STATUS_FLAG_SIMPLE_MODE`, else `FULL`; `btrfs_qgroup_enabled` ⇔ mode ≠
     `DISABLED`).
   - supplementary (row attribution pending L1's source rows): `ch-quota-intro.rst:191-250`
     ("Simple quotas (squota)" — squotas share the qgroups API but do not track shared vs exclusive
     usage). This explains why the mode is worth surfacing but is not a distinct quota *state*.
4. **Device check (not in the expected keys).** Path `st_dev` `0:57` differs from the mount's
   `0:30`, which is the normal btrfs subvolume situation: S081 — `fs_btrfs_inode.c:8246`
   (`stat->dev = BTRFS_I(inode)->root->anon_dev`, the per-subvolume anonymous device). Contract: for
   btrfs a mismatch is expected and is recorded as `device_check "btrfs_subvolume_skipped"`; it is not a
   verdict-changing condition, and `device_check`, `quota_option_keys`, `btrfs_qgroups_mode` are output
   fields that the contract's sealed-case comparison and this case's `expected` deliberately exclude.
5. **Verdict precedence.** Contract §C2: setup error → 2 `QUOTA_SETUP`; else any `enabled` → 1
   `QUOTA_ENABLED`; else any `unknown` → 2 `QUOTA_STATE_UNKNOWN`; else 0 `QUOTA_DISABLED`. One path,
   `enabled`, no setup error → exit `1`, finding_id `QUOTA_ENABLED`. `QUOTA_ENABLED` is a
   runway-reporting finding, not a failure claim.
6. **Enforcement `unknown`.** The probe reads no per-user/group/project limit or usage values
   (contract limits), and "btrfs qgroup presence ≠ any limit set". `enabled` therefore means "a quota
   mechanism is visibly present", never "a limit is set".

## 3. Sources relied on

| S-id | source | what it grounded here |
|---|---|---|
| S079 | `fs_btrfs_sysfs.c` | `qgroups/enabled`, `qgroups/mode` attributes; mode text `squota` = simple mode |
| S080 | `fs_btrfs_qgroup.c` | `btrfs_qgroup_mode` / `btrfs_qgroup_enabled` semantics; mode ⇒ quota on |
| S081 | `fs_btrfs_inode.c` | per-subvolume anonymous `st_dev` (`root->anon_dev`) → `btrfs_subvolume_skipped` |
| S082 | `Documentation_filesystems_proc.rst` §3.5 | mountinfo field layout used to author the fixture text |

**S-id ↔ file mapping is an inference, not a registry fact.** `corpus/SOURCES.md` currently ends at
S076; rows S077–S084 are being drafted this round (scribe seat `DraftSourceRows`). The contract pins
exactly one id: "per-subvolume anonymous st_dev, **S081**" — and the only source in
`.scratch/round23/src/` carrying the per-subvolume anonymous device is `fs_btrfs_inode.c`, which is the
5th source-scribe seat (`SrcBtrfsGetattr`). I therefore numbered the eight scouts in wave seat order
(SrcXfsDoc S077, SrcXfsShowargs S078, SrcBtrfsSysfs S079, SrcBtrfsQgroup S080, SrcBtrfsGetattr S081,
SrcProcMountinfo S082, SrcExt4Doc S083, SrcTmpfsDoc S084), which is consistent with the contract's own
S081 citation. **If L1 assigns the rows differently, the `sources` array in this case file must be
renumbered**; the rationale's file:line anchors are unaffected and remain the load-bearing evidence.

## 4. Contract ambiguities found (for L1 / the oracle author)

1. **"source basename" is not defined for fixture mode.** §C2 says the btrfs row applies when the
   "source basename maps to exactly one uuid", and the real-mode inputs use
   `os.path.realpath(mount_source)` basename plus `device_links` in fixture mode, but the fixture spec
   never states whether the comparison is against the basename of the raw mount source string or of the
   resolved link target. The frozen real control settles it in practice (host: source `/dev/mapper/root`
   → `/dev/dm-0`, sysfs `devices` lists `dm-0`), so the resolved name is the intended one; the
   contract text should say so. This fixture keeps the `device_links` value (`dm-3`) identical to the
   sysfs device name, so both readings of "device name" coincide; only the unresolved-basename reading
   (`srv`) differs, and that reading contradicts the frozen real control.
2. **The btrfs table has no `squota` row.** `squota` (simple quota accounting) and `qgroup` (full
   accounting) are materially different mechanisms — see `ch-quota-intro.rst` — yet both map to
   `enabled / unknown / btrfs_qgroups_dir_present`, and the mode is visible only in the output field
   `btrfs_qgroups_mode`. The case is therefore a *mode-fidelity* case, not a *verdict-discrimination*
   case: it proves the mode text is carried and does not leak into the verdict, and it cannot detect an
   implementation that drops or mislabels `btrfs_qgroups_mode` unless the oracle also compares that
   field. The contract's own sealed-case comparison lists only `(path, fstype, mount_point,
   quota_state, enforcement, basis)` — so a squota/qgroup mix-up is invisible to the sealed comparison.
   Recommend either a stated comparison of `btrfs_qgroups_mode` for btrfs fixtures, or an explicit
   note that the mode text is unverified by the sealed cases.
3. **`enforcement unknown` for btrfs, `enforced` for xfs/tmpfs.** The asymmetry is defensible (btrfs
   limits are not observable at all; xfs/tmpfs super options state enforcement directly) but it means
   the same token `unknown` covers "btrfs quota present, limits unobservable" and "ext4 quota present,
   limits unobservable". Consumers of the finding must not read `unknown` as "not enforced".
4. **`device_check` is unobservable in sealed cases.** The contract's per-path expected key set
   excludes `device_check`, `quota_option_keys` and `btrfs_qgroups_mode`; the `btrfs_subvolume_skipped`
   vs `match` distinction therefore cannot be asserted by any fixture case and survives only in raw
   output. The real control (`frozen/c2-expected-real.json`) does assert `device_check`, so the
   behaviour is checked in real mode only.
5. **Exit code 1 is shared by "finding" and would-be "failure" reading.** §C2 states `QUOTA_ENABLED`
   is a runway-reporting finding, not a failure claim, yet it is the only non-zero, non-setup exit.
   Downstream tooling that treats exit ≠ 0 as failure will misread it; the contract already pins the
   meaning, but the case carries `exit: 1` without a machine-readable marker of that distinction.

## 5. Provenance of the local source copies I read

Local copies under `.scratch/round23/src/` (SHA-256, byte length):

| file | sha256 | bytes |
|---|---|---|
| `fs_btrfs_sysfs.c` | `ce146120f29ac29c0bc1859f21e4b84da91a536df2ec9fd2fa5649144f731c43` | 72925 |
| `fs_btrfs_qgroup.c` | `121a0af27f9553a9749c837536d618e2ea50d44ce54b30b032fa56e6f3df6ed5` | 139049 |
| `fs_btrfs_inode.c` | `01a6ad07c09cd1a05fbccab640c15362c91b57b85faa94c2fd9b9c0128110fdf` | 319770 |
| `Documentation_filesystems_proc.rst` | `e760f716f8278deefab17a63739033cadc7faee93663c49e76455afaaf40d126` | 107560 |
| `ch-quota-intro.rst` (supplementary) | `dbc52519b92053be9c95cb415d08a473f85183492bc4305d0ae468362cdcecb3` | 12355 |

Version correspondence check: the two sibling scout reports that landed in this wave record the
kernel `v7.2` fetches `Documentation/admin-guide/ext4.rst` (27676 bytes) and
`Documentation/filesystems/tmpfs.rst` (13078 bytes); the local copies in `.scratch/round23/src/` have
exactly those byte lengths, so that directory holds the v7.2 kernel sources and my line anchors are
v7.2-consistent. The five files above were read read-only; none was modified.

## 6. Scope notes

- Deliberately **not** included, to stay independent of sibling seats: a second uuid (zero/several-uuid
  rows belong to `CaseBtrfsUnmapped` / `CaseBtrfsTwoUuids`), a non-btrfs second path (covered by the
  xfs/ext4/tmpfs seats and by `CaseEnabledPlusUnknown` for precedence), and a symlinked path (covered
  by `CaseSymlinkRealpath`).
- The fixture's extra mountinfo lines (`/` ext4, `/proc` proc, `/run` tmpfs) exist to make the text
  realistic and to exercise longest-mount-point selection; none of them can become the chosen mount
  for `/srv/data`, so they contribute no expected token.
- No build, test, lint, formatter or smoke run was performed in this wave; the only check executed was
  a JSON re-parse of the file I authored plus a field-position re-parse of my own mountinfo text
  against proc.rst §3.5.

---

# Correction (appended after the round-23 pre-seal amendment)

Authority: `.ufo/waves/round-23/preseal-amendment.md` ("C2 final rules superseding only
erroneous/ambiguous original clauses"), received before any candidate inspection or result on my seat.
Original proposal `.ufo/waves/round-23/cases-proposed/CaseBtrfsSquota.json` is left **byte-untouched**
as an original proposal. Corrected case: `.ufo/waves/round-23/cases-corrected/CaseBtrfsSquota.json`
(same `id` = `CaseBtrfsSquota`, same `schema` = `mori-quota-case-v1`). No implementation, oracle or
candidate was read; no test or build was run.

## Delta applied (the amendment clauses that touch this seat)

| # | Amendment clause | Applied to my case |
|---|---|---|
| 1 | "Add required fixture member `qgroups_enabled` to each btrfs_sysfs UUID record: true/false/null" | UUID record `6f0c9e42-58ab-4d71-9c30-6b1fe4ad2753` now has `qgroups_enabled: true` (its `qgroups` was already true; the `qgroups false ⇒ enabled=null/mode=null` pairing rule is not triggered here — no false/decimal-decoy record exists in my fixture) |
| 2 | "Present plus enabled=true → enabled/unknown/`btrfs_qgroups_enabled`" | `expected.paths[0].basis` changed `btrfs_qgroups_dir_present` → `btrfs_qgroups_enabled`; `quota_state enabled`, `enforcement unknown`, `fstype btrfs`, `mount_point /srv` unchanged |
| 3 | "Fixture source resolution: lookup RAW decoded source in device_links; use its mapped basename when present, otherwise basename(source)" | Re-derived: raw decoded source `/dev/mapper/srv` → `device_links` hit → mapped basename `dm-3` → compared against the UUID `devices` list → exactly one UUID match (zero/multiple stays unknown). Same conclusion as before, now by the amended rule |
| 4 | "Parse separator and the last THREE fields of EACH chosen line"; octal-decode root/mountpoint/source with exactly 040/011/012/134 | Re-verified my 4 fixture lines: separator index and last three fields (`btrfs` / `/dev/mapper/srv` / super options) parse per line; no backslash escapes present, so no decode and no `QUOTA_SETUP` |
| 5 | "if ANY covering mountpoint occurs more than once → unknown/n/a/`ambiguous_overmount`, fstype=null, mount_point=null, device_check=not_checked" | Not triggered: covering mount points for `/srv/data` are `/` and `/srv`, each appearing exactly once in my mountinfo text. Expected stays `fstype btrfs`, `mount_point /srv` |
| 6 | "Device mismatch PREEMPTS the filesystem table … Btrfs skips equality only when stat major is 0" | `st_dev "0:57"` has major 0, so the btrfs skip applies and no `device_mismatch` preemption; `device_check` would be `btrfs_subvolume_skipped`. (Had I used a nonzero major, the expected basis would have been `device_mismatch` — the fixture deliberately keeps major 0.) |
| 7 | Fixture typing rules (nonempty unique normalized absolute path/realpath, canonical decimal `MAJ:MIN` `0:57`, canonical UUID key, plain nonempty device basenames `dm-3`, exact bool/bool-or-null/mode-or-null record fields, no extra record keys) | All satisfied by the corrected fixture: one path `/srv/data`, `realpath` identical, `st_dev "0:57"` (no sign, no leading zero), one canonical UUID key, `devices ["dm-3"]`, `qgroups true`, `qgroups_enabled true`, `qgroups_mode "squota"`, record keys exactly `devices, qgroups, qgroups_enabled, qgroups_mode` |
| 8 | "Output tuples remain the original six scored fields; supplementary sealed checks additionally verify device_check, quota_option_keys and qgroups_mode where given" | `expected.paths[0]` keeps exactly the six scored keys. Supplementary values this fixture implies, for L1/oracle use only: `device_check "btrfs_subvolume_skipped"`, `quota_option_keys []` (btrfs mechanism is sysfs, not mount options), `qgroups_mode "squota"` (only `qgroup`/`squota` accepted; unavailable/other would be null) |
| 9 | Verdict precedence (unchanged) | One `enabled` path, no setup error → exit `1`, finding_id `QUOTA_ENABLED` |

Clauses with no effect on this seat: ext2/3/4 always unknown/n/a and the `ext_quota_option_unverified`
basis; the ext positive cases of other seats; the duplicated-covering-point (`ambiguous_overmount`) case
of another seat; XFS precedence; tmpfs hardlimit vocabulary. Nothing outside my fixture or expectations
was touched ("preserve unrelated fixtures/expectations").

## Delta summary (machine-checkable)

Structural diff of the two case files shows exactly four differing leaves/strings:

- `fixture.btrfs_sysfs["6f0c9e42-58ab-4d71-9c30-6b1fe4ad2753"].qgroups_enabled`: absent → `true`
- `expected.paths[0].basis`: `btrfs_qgroups_dir_present` → `btrfs_qgroups_enabled`
- `scenario`: reworded to name `qgroups_enabled true` and the new basis
- `rationale`: rewritten to cite the amendment's btrfs clause and the amended resolution rules

Unchanged: top-level key set (`schema, id, scenario, fixture, expected, rationale, sources`), fixture
key set (`schema, mountinfo, paths, device_links, btrfs_sysfs`), the entire `mountinfo` text, `paths`,
`device_links`, the UUID key, `devices`, `qgroups`, `qgroups_mode`, `exit`, `finding_id`,
`quota_state`, `enforcement`, `fstype`, `mount_point`, and `sources`.

## Amendment ambiguity noted by this seat

The amendment makes `qgroups_enabled` a **required** fixture member, i.e. it changes the fixture format
materially, yet it does not rename the fixture schema string; my corrected file therefore still carries
`"schema": "mori-quota-fixture-v1"` (renaming it myself would risk a strict loader rejecting the case
as an unknown schema). Consequence: `mori-quota-fixture-v1` now denotes two different shapes (with and
without `qgroups_enabled`), so a loader keyed only on the schema string cannot distinguish them, and the
pre-amendment proposals in `cases-proposed/` are structurally invalid against the amended loader while
still being valid history. Recommend L1 either bump the fixture schema string for the amended shape or
state explicitly that the amended shape is `mori-quota-fixture-v1` with the extra required member and
that only `cases-corrected/` is loadable.

## Final hashes (sha256)

| file | sha256 | bytes |
|---|---|---|
| `.ufo/waves/round-23/cases-corrected/CaseBtrfsSquota.json` (corrected case) | `b3a641541e536ce1f313b521ae25a33cd8296e2e2d8daf647bf24c168254240a` | 4590 |
| `.ufo/waves/round-23/cases-proposed/CaseBtrfsSquota.json` (original proposal, untouched: mtime still 2026-10-21T14:27:40-0300, its authoring time) | `db77e8b64ca57feaa00019de1bc20c4c280b9495f11e6abe4158359bdc376308` | 3879 |
| `.ufo/waves/round-23/build/CaseBtrfsSquota.md` (this report) | reported to L1 in the seat reply; recomputable with `sha256sum` over the sealed copy (a file cannot contain its own digest) | — |
