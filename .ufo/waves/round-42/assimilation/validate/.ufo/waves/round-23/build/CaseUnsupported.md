# CaseUnsupported — C2 fixture case: nfs4 mount covering the path

Seat: `MadoR22-2.CaseUnsupported-8` (wave item `CaseUnsupported`)
Case file: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/cases-proposed/CaseUnsupported.json`
Case `id`: `CaseUnsupported` — the wave item name, matching the file name,
the report trailer path `.ufo/waves/round-23/build/CaseUnsupported.md` and
the sibling cases already proposed in this wave (`CaseBtrfsSquota.json`,
`CaseBtrfsUnmapped.json`, `CaseXfsDevMismatch.json`,
`CaseXfsMixedEnforce.json` all carry the item name as `id`). The authoring
seat is recorded in the rationale so the seal can attribute the row.
Scope: one independent fixture case for contract §C2, derived only from
`/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/contract.md`
(frozen at lane commit `4dc80c1be48308075e83af17f15fbfe7e95e6cb8`) and the
kernel source S082 (proc.rst v7.2).

Independence: I did not open any candidate implementation
(`.ufo/waves/round-23/build/ImplQuota/`, `.scratch/round23/ImplQuota`), the
oracle directory (`.ufo/waves/round-23/build/OracleQuota/`), or
`cases-proposed/`. Reads were: contract.md, `wave1-spec.json` (my own
prompt), `corpus/SOURCES.md` (registry shape, to confirm the S-id mapping),
the upstream kernel doc for S082, and — after my case was already written
and its expectation fixed — a metadata-only listing of the sibling case
files' `id` and top-level key names, to confirm the naming convention this
wave uses for the case `id`/file name. No sibling fixture, expectation or
rationale text was read, and none influenced this derivation.

## 1. Scenario and derivation

Fixture: an nfs4 server export mounted at `/mnt/nfs`, covering the requested
path `/mnt/nfs/data`. The mount's `major:minor` (`0:61`) equals the path's
`st_dev` (`0:61`), so the contract's device gate passes and the case reaches
the classification table rather than stopping at `device_mismatch`.

Step-by-step, with the contract row each step rests on:

1. **Mount resolution** (§C2 "Mount resolution (per path)"): candidates are
   mounts whose mount point equals the path realpath, is `/`, or is a
   prefix at a `/` boundary; the **longest** mount point wins. The fixture's
   mountinfo has two lines — a btrfs root at `/` and an nfs4 mount at
   `/mnt/nfs`. For realpath `/mnt/nfs/data` the nfs4 mount point
   (8 characters) is longer than `/` (1 character), so the nfs4 line is
   chosen. The `/` line is present deliberately so the case discriminates
   "longest mount point" from "first line in file" and from "root mount".
2. **Field parse** (§C2, "parse mountinfo per proc.rst §3.5"): each line is
   parsed as fields 1–6, then optional `tag[:value]` fields until the `-`
   separator, then fstype, source, super options. The nfs4 line yields
   fstype `nfs4`, mount point `/mnt/nfs`, source `nfs-server.example:/export`,
   super options `rw,vers=4.2,hard,proto=tcp,timeo=600,retrans=2,sec=sys,
   rsize=1048576,wsize=1048576`.
3. **Device check** (§C2, the paragraph after mount resolution): "If chosen
   fstype is not btrfs and its major:minor ≠ the path's st_dev → `unknown`
   basis `device_mismatch`." nfs4 is not btrfs, and `0:61 == 0:61`, so the
   path is **not** diverted to `device_mismatch`; it proceeds to
   classification with device_check `match`.
4. **Classification** (§C2 quota classification table, last row "other"):
   fstype `nfs4` is not xfs, not btrfs, not ext2/ext3/ext4, not tmpfs, so the
   row is `quota_state = unknown`, `enforcement = n/a`,
   `basis = unsupported_fstype`.
5. **Verdict precedence** (§C2, "Verdict precedence"): no path is `enabled`,
   one path is `unknown`, so exit **2** with finding_id
   **`QUOTA_STATE_UNKNOWN`** (not `QUOTA_SETUP`, which is reserved for
   fixture/CLI setup errors, and not `QUOTA_ENABLED`).

Expected per-path record (exactly the six contract-named keys, no
`device_check` / `quota_option_keys` / `btrfs_qgroups_mode`, since the case
schema fixes the expected object to `path, fstype, mount_point, quota_state,
enforcement, basis`):

```
path=/mnt/nfs/data  fstype=nfs4  mount_point=/mnt/nfs
quota_state=unknown  enforcement=n/a  basis=unsupported_fstype
```

Expected exit `2`, finding_id `QUOTA_STATE_UNKNOWN`.

The `unsupported_fstype` outcome is corroborated by the contract's own
limits line: "no NFS/server-side or overlay/fuse quota" — NFS quota is
enforced by the server, so neither mountinfo super options nor
`/sys/fs/btrfs` can make a client-side enablement claim for it. The probe
must therefore report *unknown*, never *disabled*: "disabled" would assert
an absence of server-side quota that the probe did not and cannot observe.

## 2. Fixture realism notes

* Both mountinfo lines follow proc.rst §3.5 field layout exactly: 11 space
  separated fields, one optional field (`shared:4`, `shared:9`) before the
  `-` separator, then fstype / source / super options. The btrfs line
  carries `subvolid=5,subvol=/` in its super options, as a real btrfs root
  mount does.
* `device_links` and `btrfs_sysfs` are populated with a coherent btrfs
  root (`/dev/mapper/root` → `dm-0`; one uuid whose `devices` list is
  `["dm-0"]`, `qgroups: false`, `qgroups_mode: null`) so the fixture does
  not depend on empty-collection semantics, and so a wrong implementation
  that mis-maps the nfs4 source onto the btrfs uuid is visibly wrong rather
  than accidentally right.
* `st_dev` is given as the string `MAJ:MIN` form the contract's fixture
  example uses (`"MAJ:MIN"`), here `0:61`. The nfs4 mount's `major:minor`
  is `0:61` too, so the device gate matches.

## 3. Contract ambiguities found (reported, not resolved by fiat)

1. **Device-check precedence vs. the `other` row is under-specified for
   non-btrfs fstypes.** The contract states the device rule as a separate
   sentence and the classification table separately; it never says whether
   `device_mismatch` outranks `unsupported_fstype` for a non-btrfs mount
   whose device also mismatches. I read the device rule as a gate (a
   mismatch short-circuits before classification) and therefore **matched**
   the st_dev deliberately, so the case exercises `unsupported_fstype`
   rather than depending on that precedence. A sibling case that
   deliberately mismatches a non-btrfs st_dev would be sensitive to the
   other reading. Recommend L1 state the precedence explicitly in the
   contract text before sealing.
2. **`n/a` is written as a literal string, not a null.** The table writes
   enforcement `n/a` while the output schema elsewhere allows null
   (`fstype`/`mount_point` null when no covering mount; `btrfs_qgroups_mode`
   the mode text or null). I used the literal string `"n/a"` because the
   table uses that spelling and the schema never lists `enforcement` among
   the nullable fields. If the implementation emits `null` for unknown
   enforcement, this expectation would mismatch — a real cutover
   ambiguity worth pinning.
3. **`quota_option_keys` is not asserted here** because the case schema
   fixes the expected path object to six keys. For this fixture the correct
   value would be the empty list (no quota-related key appears in the nfs4
   super options) — worth noting so a later case extension can assert it
   without changing this file.
4. **`unsupported_fstype` vs. the stated NFS limit.** The limits text says
   NFS quota is not covered, but the table's `other` row says
   `unsupported_fstype`, not an NFS-specific basis. The two agree for
   nfs4 as long as nfs4 is treated as "other"; the contract should say
   explicitly that `nfs`/`nfs4`/`fuse`/`overlay` all fall into the `other`
   row, so an implementer does not invent a `nfs_quota_not_observable`
   token.
5. **Mount-source disclosure.** The fixture necessarily contains the export
   path `nfs-server.example:/export`; the contract's output rules forbid
   echoing mount sources, so this case is also a check that the source
   string does not leak into `paths`. The expected object does not contain
   it, and a leak would show up as an extra key or extra value.
6. **`nfs4` is a single mountinfo token, not `nfs`+subtype.** proc.rst
   §3.5 line 1981 says the filesystem type has the form `type[.subtype]`;
   the kernel prints `nfs4` as one token, so a parser that splits on `.`
   sees fstype `nfs4`. The contract's table has no `nfs`/`nfs4` row, so the
   outcome is `unsupported_fstype` either way — the expectation is invariant
   under either reading, which is why the case is safe to seal. Recorded
   because a future case that asserts `fstype` verbatim needs the same
   invariance to hold.
7. **Non-quota super-option keys that look quota-ish.** The nfs4 super
   options contain `hard` and `vers=4.2`. `hard` is not in any contract
   quota key list and does not end in `_hardlimit` (the tmpfs rule), and
   `vers` is not quota-related, so `quota_option_keys` should be empty
   here. The case asserts only the six contract-named expected keys, so a
   divergent `quota_option_keys` value is not caught here — flagged so the
   seal can decide whether a `quota_option_keys` assertion belongs in a
   separate case rather than being folded into this one.

## 4. Source anchors

* **S082 — proc.rst (Linux v7.2)**, `Documentation/filesystems/proc.rst`,
  §3.5 `/proc/<pid>/mountinfo - Information about mounts`, lines 1965–1993;
  fetched bytes sha256 `e760f716f8278deefab17a63739033cadc7faee93663c49e76455afaaf40d126`
  (107560 bytes) from `https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/filesystems/proc.rst`.
  Anchors: line 1975 "(3) major:minor: value of st_dev for files on
  filesystem"; 1977 "(5) mount point: mount point relative to the process's
  root"; 1980 "(m+1) separator: marks the end of the optional fields"; 1981
  "(m+2) filesystem type: name of filesystem of the form type[.subtype]";
  1982 "(m+3) mount source"; 1983 "(m+4) super options: per super block
  options"; 1985 "Parsers should ignore all unrecognised optional fields";
  1989–1992 the optional-field tags `shared:X`, `master:X`,
  `propagate_from:X`, `unbindable`.
  Supports the contract's parse rule (fields 1–6, optional fields until `-`,
  then fstype/source/super options). It does not speak to quota
  classification, so the classification expectation rests on the contract
  table alone.
* S-id mapping note: the eight rows S077–S084 are drafted in the order
  (xfs.rst, xfs_super.c, btrfs sysfs.c, btrfs qgroup.c, btrfs inode.c,
  proc.rst, ext4.rst, tmpfs.rst). The contract itself cites **S081** for
  "per-subvolume anonymous st_dev", which is btrfs inode.c under that
  positional mapping — the fifth entry, and S081 is the fifth id. The
  mapping is therefore self-consistent and proc.rst is **S082**.

Only S082 is relied on; the case's `sources` array says exactly `["S082"]`.

## 5. Tooling

No tool was installed or updated for this seat; no packages, no channels.
Only the upstream kernel documentation was fetched over HTTPS (read-only
network read of a public source), plus the permitted read-only repository
reads. No host mountinfo, stat, sysfs or quota interface was probed — this
seat's item does not name those, and the case is synthetic by design.

## 6. Result

One case file written, valid JSON, exact key sets:
top level `schema, id, scenario, fixture, expected, rationale, sources`;
fixture `schema, mountinfo, paths, device_links, btrfs_sysfs`;
expected `exit, finding_id, paths` with each path object exactly
`path, fstype, mount_point, quota_state, enforcement, basis`. Expectation
derived from contract §C2 rows only; no implementation consulted.

---

# CORRECTION — round-23 pre-seal amendment (appended, not a rewrite)

Amendment: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/preseal-amendment.md`,
sha256 `4f3707ba2069a6da4d6455a29aea19d1809ae3eba76e25b166810a7e80f25cde`.
The amendment was written before L1 opened any ImplQuota candidate or ran
any C2 candidate; no C2 result was observed. Sections 1–6 above are the
original proposal record and stand unchanged.

**Corrected case:** `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/cases-corrected/CaseUnsupported.json`
(same `id` `CaseUnsupported`). The original proposal
`.ufo/waves/round-23/cases-proposed/CaseUnsupported.json` is **retained
untouched** — it was not edited, moved or re-`id`ed after the amendment.

## Delta versus the proposal (fixture only; expectations unchanged)

1. **`btrfs_sysfs` record gains the required member `qgroups_enabled`.**
   The amendment makes `qgroups_enabled` a required member of every
   `btrfs_sysfs` UUID record (true/false/null) and states that
   "qgroups false must pair with enabled=null/mode=null". My proposal's
   record had only `devices`, `qgroups`, `qgroups_mode` — under the
   amendment's "Missing/extra record keys setup" rule the proposal would
   now be a **setup error**, i.e. it could not even reach classification.
   The corrected record is
   `{"devices":["dm-0"],"qgroups":false,"qgroups_enabled":null,"qgroups_mode":null}`.
   This is the record for the **decoy** btrfs root mount; the amendment
   applies the member to decoys too, and it changes nothing observable
   because the decoy is never the chosen mount.
2. **UUID key restated in canonical RFC 4122 v4 form** —
   `6f1a2c3d-4e5f-6a7b-8c9d-0e1f2a3b4c5d` →
   `6f1a2c3d-4e5f-4a7b-8c9d-0e1f2a3b4c5d`. The amendment requires "UUID
   keys canonical UUIDs"; the proposal's third group began with the
   version nibble `6`, which is not a defined RFC 4122 version. The
   corrected value has version nibble `4` and variant nibble `8`.
3. **Unchanged:** the mountinfo text, the `paths` entry (`/mnt/nfs/data`,
   realpath `/mnt/nfs/data`, `st_dev` `0:61`), `device_links`, and every
   value under `expected`.

## Re-derivation under the amendment's superseding rules — expectations identical

* **Mount resolution.** The amendment keeps longest component-prefix
  selection, ignores empty trailing lines, decodes only the exact octal
  escapes `040/011/012/134` in root, mountpoint and source, and parses "the
  separator and the last THREE fields of EACH chosen line". My fixture has
  no backslash escape anywhere, and each line has exactly three fields
  after the `-` separator. Covering mountpoints for realpath
  `/mnt/nfs/data` are `/` (the decoy btrfs root) and `/mnt/nfs` (the nfs4
  export). The amendment refuses classification as
  `unknown/n/a/ambiguous_overmount` only when a covering mountpoint
  **occurs more than once**; here `/` occurs once and `/mnt/nfs` occurs
  once, so there is no ambiguity. Longest component-prefix selection then
  picks `/mnt/nfs` (8 characters) over `/` (1 character).
* **Device check.** The amendment makes a device mismatch *preempt* the
  filesystem table (`unknown/n/a/device_mismatch`, `device_check=mismatch`)
  and lets btrfs skip equality only when the stat major is `0`. The chosen
  fstype is nfs4 (not btrfs) and its `major:minor` `0:61` equals the path
  `st_dev` `0:61`, so no mismatch fires and classification proceeds with
  `device_check` `match`.
* **Classification.** The amendment's superseding rows cover ext2/3/4,
  btrfs, xfs and tmpfs. fstype `nfs4` falls to the retained `other` row
  (not xfs, not btrfs, not ext2/ext3/ext4, not tmpfs):
  `quota_state` `unknown`, `enforcement` `n/a`, `basis`
  `unsupported_fstype`. The amendment adds that for unsupported fstypes
  `quota_option_keys` is `[]` and that unknown nonquota super options are
  ignored and quota option **values** are never emitted — the nfs4 super
  options here contain no quota key (`hard` is the NFS hard-mount flag,
  `vers` is a protocol version), so the supplementary `quota_option_keys`
  for this path is the empty list.
* **Verdict precedence.** Unchanged: setup error, then any `enabled`, then
  any `unknown`, else disabled. No path enabled, one path unknown →
  **exit 2**, finding_id **`QUOTA_STATE_UNKNOWN`**, with each path object
  carrying exactly the six scored fields.

So the amendment's ext and duplicated-covering-point corrections do not
reach this case: the fixture has no ext path, and no covering mountpoint
is duplicated. The expected block is byte-identical to the proposal's.

## Supplementary sealed values (not part of the six scored fields)

For the single path: `device_check` `match`, `quota_option_keys` `[]`,
`btrfs_qgroups_mode` `null`. Recorded for the seal's supplementary checks;
no option value, mount source or UUID may appear in the tool output.

## Independence of this correction

No candidate implementation, oracle, or sibling case content was read
while producing the corrected case. The only sibling file opened in this
wave was `cases-corrected/CaseTmpfsUsrquota.json` (another seat's
corrected case), read after my corrected case was already written, and
only to confirm the wave's corrected-case file convention — the same
convention my corrected case already follows. No implementation, no test
and no run of any kind was performed: no candidate was opened, no probe
was executed, no build or gate was run.

## Final hashes

| artifact | sha256 |
|---|---|
| `cases-corrected/CaseUnsupported.json` | `28f3080b116cf3e09e3ee77f3e8b53daff826fdfb4387a21d3c58850878b22b7` |
| `cases-proposed/CaseUnsupported.json` (retained, unaltered) | `44c6f3a2d682e602a104ccb90a02cf1b23f06d878a13146518d16c25eb0a3018` |
| `build/CaseUnsupported.md` (this report) | self-referential; the final digest of this file is delivered to L1 with the case message |
| `preseal-amendment.md` (input) | `4f3707ba2069a6da4d6455a29aea19d1809ae3eba76e25b166810a7e80f25cde` |

No VCS mutation was performed in the lane: `git status --porcelain` shows
no tracked-file modification, and nothing was staged or committed.
