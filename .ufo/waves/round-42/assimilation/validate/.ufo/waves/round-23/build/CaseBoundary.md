# CaseBoundary — C2 fixture case (mori round 23, wave 1)

Seat: `MadoR22-2.CaseBoundary-8` · role: reviewer (case author) · lane: leaf, no subagent dispatch.

## Deliverable

- Case file (the only file this seat wrote besides this report):
  `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/cases-proposed/CaseBoundary.json`
  — schema `mori-quota-case-v1`, id `CaseBoundary`, one `mori-quota-fixture-v1` object,
  expected exit `0` / `QUOTA_DISABLED`, one expected path.
- No production file, no other case file, no host quota probe, no privileged command, no
  VCS mutation. The kernel sources were fetched over HTTPS into the lane's designated
  scratch root (`…/mori-shokunin/.scratch/r23case/`, per the wave's `TMPDIR` rule) only to
  compute their SHA-256 digests, and that scratch directory was deleted afterwards
  (`rm -rf …/.scratch/r23case`); nothing under `.scratch/` is committed. JSON
  well-formedness and key-set conformance of my own file were checked with a local parse
  (no tool installed or updated this seat, so there is no tool/version/channel record to
  report).

## Independence statement

The expectation was derived **only** from `.ufo/waves/round-23/contract.md` §C2 and the
named kernel sources S077–S084 opened read-only over HTTPS. I did **not** read
`.ufo/waves/round-23/build/ImplQuota/`, any `.scratch/round23/ImplQuota` clone, or
`build/OracleQuota/`. I did not read this host's quota state (no mountinfo/sysfs/quotactl
probe). The frozen control `frozen/c2-expected-real.json` was read for cross-checking only
(it is a contract artifact, not an implementation).

Full disclosure of peer reads: for **file-format conventions only** (the JSON key layout,
the trailing-newline convention in the fixture `mountinfo` text, and the S077–S084 id
mapping, which is not yet in `corpus/SOURCES.md`) I read the wave-1 seat report
`build/CaseBtrfsUnmapped.md`, the draft registry rows `build/DraftSourceRows/rows.md`, and
one peer case file `cases-proposed/CaseBtrfsUnmapped.json`. None of these contains an
implementation of `tools/mori-quota-surface.py` or of the probe's expected values, and
none of them covers my scenario (a *mapped* btrfs device with qgroups absent, versus that
seat's *unmapped* device). My expected values were computed from the contract's
mount-resolution rule and quota-classification table before and independently of those
reads; the case is deliberately **not** a near-duplicate of that seat's (different mount
prefixes, different basis token, different exit code).

## Scenario

Nested mounts whose *character* prefixes collide with a path: btrfs at `/a` (qgroups
absent) and xfs **with `usrquota`** at `/a/b`; the queried path `/a/bc` is a child of
`/a` but **not** of `/a/b`. The case pins that `/a/bc` must resolve to `/a` (btrfs, quota
disabled) and must **not** resolve to `/a/b` (xfs, quota enabled/enforced).

Fixture shape (all values synthetic; nothing was observed on this host):

| element | value | why |
|---|---|---|
| mountinfo line 1 | `28 28 8:2 / / rw,relatime shared:1 - ext4 /dev/sda2 rw,errors=remount-ro` | the root filesystem: a candidate (`mount point is /`) that must lose to the longer `/a` |
| mountinfo line 2 | `30 28 0:30 /@a /a rw,relatime shared:2 - btrfs /dev/sdb1 rw,compress=zstd:3,ssd,discard=async,space_cache=v2,subvolid=256,subvol=/@a` | the **correct** covering mount for `/a/bc` |
| mountinfo line 3 | `31 30 259:1 / /a/b rw,relatime shared:3 - xfs /dev/nvme0n1p1 rw,attr2,inode64,usrquota` | the **trap**: nested mount whose name shares the prefix `/a/b` with the path prefix |
| path | `/a/bc` (realpath identical), `st_dev` `0:57` | the queried path; `st_dev` is a btrfs anonymous device, deliberately ≠ the mount's `0:30` |
| `device_links` | `/dev/sda2`→`sda2`, `/dev/sdb1`→`sdb1`, `/dev/nvme0n1p1`→`nvme0n1p1` | supplies the device basename of each mount source (the real-mode `realpath(mount_source)` basename) |
| uuid `7c3f2a1e-9b4d-4c8a-8f61-2e5d0a7b9c33` | `devices:["sdb1"]`, `qgroups:false`, mode `null` | the btrfs filesystem behind `/a` — qgroups **not** enabled |
| uuid `d41a9f60-3c72-4e15-9b8a-6f0c2e7d4a81` | `devices:["dm-0"]`, `qgroups:true`, mode `"squota"` | a qgroup-capable filesystem on a *different* device — must not leak into the verdict |

## Derivation (contract §C2, step by step)

1. **Mount resolution.** Contract: *"Candidate mounts: mount point equals realpath, or is
   `/`, or realpath starts with mount point + `/`. Choose the **longest** mount point; among
   equal mount points the **last** line wins."*
   For realpath `/a/bc`:
   - `/a` qualifies — `"/a/bc".startswith("/a" + "/")` is true.
   - `/a/b` does **not** qualify — `"/a/bc".startswith("/a/b/")` is **false**; `/a/bc` is a
     *sibling* of `/a/b`, not a descendant. (A plain `startswith("/a/b")` prefix test would
     wrongly admit it — that is exactly the bug this case is built to catch.)
   - `/` qualifies (special case), but `/a` is longer.
   → chosen mount point **`/a`**, fstype **btrfs**, source `/dev/sdb1`, major:minor `0:30`.
   The nested xfs mount at `/a/b` is **not** chosen.
2. **Device check.** *"If chosen fstype is not btrfs and its major:minor ≠ the path's st_dev
   → unknown basis `device_mismatch`. For btrfs a mismatch is expected (per-subvolume
   anonymous st_dev, S081) and is recorded as `device_check: "btrfs_subvolume_skipped"`;
   equal → `device_check: "match"`."* fstype is btrfs, so the `0:30` ≠ `0:57` mismatch is
   expected and the path proceeds to quota classification (this is corroborated by the
   frozen real control, where the btrfs fleet root has mount `0:30` and st_dev `0:57` yet
   basis `btrfs_qgroups_dir_absent`, not `device_mismatch`).
3. **btrfs device→uuid mapping.** *"source basename maps to exactly one uuid whose
   `qgroups` is true"* → enabled; *"… exactly one uuid, `qgroups` false"* → disabled / n/a /
   `btrfs_qgroups_dir_absent`; *"zero or several uuids list the device"* → unknown / n/a /
   `btrfs_device_unmapped`. Source basename = `sdb1`; **exactly one** uuid lists `sdb1`
   (`7c3f2a1e-…`, `qgroups:false`) → **disabled**, enforcement **n/a**, basis
   **`btrfs_qgroups_dir_absent`**. The `dm-0` uuid (`qgroups:true`) is a different device and
   contributes nothing.
4. **Verdict precedence.** *"setup error → 2 `QUOTA_SETUP`; else any enabled → 1
   `QUOTA_ENABLED`; else any unknown → 2 `QUOTA_STATE_UNKNOWN`; else 0 `QUOTA_DISABLED`."*
   The fixture is well formed; the single path is disabled; nothing is enabled or unknown →
   **exit 0, `finding_id` `QUOTA_DISABLED`**.

Sealed expected object (exactly the six contract fields): `path /a/bc`, `fstype btrfs`,
`mount_point /a`, `quota_state disabled`, `enforcement n/a`, `basis
btrfs_qgroups_dir_absent`.

## Source anchors used (S077, S078, S079, S080, S081, S082)

All opened read-only at `raw.githubusercontent.com/torvalds/linux/v7.2`; digests of the
fetched bytes (sha256, first 16 hex) confirmed as `xfs_super.c 0a95697dcfcdab8f`,
`btrfs/sysfs.c ce146120f29ac29c`, `btrfs/inode.c 01a6ad07c09cd1a05`.

- **S082** — `Documentation/filesystems/proc.rst` §3.5 (field table `(1)…(m+4)`): `(3)
  major:minor`, `(5) mount point`, `(6) mount options`, `(n…m)` optional fields,
  `(m+1)` separator, `(m+2)` filesystem type, `(m+3)` mount source, `(m+4)` super options;
  *"Parsers should ignore all unrecognised optional fields."* → grounds the fixture's
  mountinfo grammar, the `shared:N` optional fields, and the reading of super options as
  the last field (which is where `usrquota` lives).
- **S081** — `fs/btrfs/inode.c` `btrfs_getattr`: `stat->dev = BTRFS_I(inode)->root->anon_dev;`
  → grounds that a btrfs path reports the subvolume's anonymous device, so mount
  major:minor and path `st_dev` differ by design and the mismatch branch must not be read
  as `device_mismatch`.
- **S079** — `fs/btrfs/sysfs.c`: the `qgroups` attribute group under
  `/sys/fs/btrfs/<uuid>/qgroups/` (`enabled`, `mode`, `inconsistent`,
  `drop_subtree_threshold`) and `<uuid>/devices/` links named after the kernel disk name
  (`sdb1`, `dm-0`) → grounds both the `devices` list used for the device→uuid mapping and
  the `qgroups` presence/absence surface.
- **S080** — `fs/btrfs/qgroup.c`: `btrfs_sysfs_add_qgroups(fs_info)` / 
  `btrfs_sysfs_del_qgroups(fs_info)` → grounds that the `qgroups` surface exists only while
  qgroup support is on, so its absence is the disable signal and its presence the enable
  signal.
- **S077** — `Documentation/admin-guide/xfs.rst` Mount Options: `noquota`; 
  `uquota/usrquota/uqnoenforce/quota`; `gquota/grpquota/gqnoenforce`;
  `pquota/prjquota/pqnoenforce` → grounds the trap mount's `usrquota` key as a genuine
  XFS quota option.
- **S078** — `fs/xfs/xfs_super.c` `xfs_fs_show_options`: `",usrquota"` on
  `XFS_UQUOTA_ENFD`, `",uqnoenforce"` on `XFS_UQUOTA_ACCT`, `",noquota"` only when no
  accounting flag is set → grounds that `rw,attr2,inode64,usrquota` is a kernel-emittable
  super-option string (enforced user quota), i.e. the trap is realistic, not synthetic
  nonsense, and that `noquota` and `usrquota` cannot co-occur in an emitted string.

S-id binding caveat: `corpus/SOURCES.md` still ends at S076; the S077–S084 rows are not yet
in the registry (drafted this round by the `DraftSourceRows` seat, not written to
`corpus/SOURCES.md`). I mapped S077–S084 by that draft's order (xfs.rst, xfs_super.c,
btrfs sysfs.c, btrfs qgroup.c, btrfs inode.c, proc.rst, ext4.rst, tmpfs.rst) and
cross-checked with the contract's own pointer — *"per-subvolume anonymous st_dev, **S081**"*
— which lands exactly on `fs/btrfs/inode.c` `anon_dev`, matching the draft row for S081.
If the sealed registry rows differ, this case's `sources` array must be re-mapped; **the
expectation does not change** (it is derived from the contract's mount-resolution and
quota-classification rules, not from the S-ids).

## Discriminating power (what a wrong implementation gets caught on)

1. **Prefix test without a path-component boundary** (`realpath.startswith(mount_point)`):
   `/a/bc` would match `/a/b` → xfs, `usrquota` → **enabled / enforced /
   `xfs_quota_option`**, exit 1 `QUOTA_ENABLED` → **caught** (wrong fstype, wrong
   mount_point, wrong quota_state, wrong enforcement, wrong basis, wrong exit).
2. **Shortest/root mount chosen** (e.g. resolving via the `/` line): ext4 root →
   **unknown** (`device_mismatch`, or `ext_quota_superblock_unobservable` if the device
   check is skipped) → exit 2 `QUOTA_STATE_UNKNOWN` → **caught**.
3. **Prefix scan picking the first match in file order** (`/` before `/a`): ext4 root →
   unknown → exit 2 → **caught**.
4. **Device check applied to btrfs** (treating `0:30` ≠ `0:57` as `device_mismatch`):
   basis `device_mismatch`, exit 2 → **caught** (contradicts the frozen real control).
5. **Leaking the unrelated qgroup-capable uuid**: any implementation that asks "does *any*
   uuid have `qgroups: true`" instead of "does the uuid that owns *this* device" →
   **enabled**, exit 1 → **caught**.
6. **Defaulting an unmappable/absent qgroups surface to enabled** → exit 1 → **caught**.

## Contract ambiguities found (for L1 / the contract owner)

A1. **The mount-boundary rule is stated only in prose and is the whole point of this
   case.** "Candidate mounts: mount point equals realpath, or is `/`, or realpath starts
   with mount point + `/`" implies a *path-component* boundary (the trailing `/` is
   essential), but the contract never says this in so many words, and a reader could
   reasonably implement it as a bare string-prefix test. My case is the one that fails
   loudly under that misreading. *Recommendation:* state the boundary explicitly — e.g.
   "the prefix test must be `realpath == mount_point + '/'` or `realpath.startswith(
   mount_point + '/')`; a bare `startswith(mount_point)` is not sufficient" — and note that
   a trailing slash in the mount point would need normalizing.

A2. **`/` is a candidate for *every* path, unconditionally.** The rule lists "is `/`" as an
   alternative to the prefix test, so a path that is not under `/` at all (in principle
   impossible) would still get the root mount; more practically, the root mount always
   enters the candidate set and the "longest mount point" tie-break is what excludes it.
   The contract's own wording is "mount point equals realpath, **or is `/`**, or realpath
   starts with mount point + `/`" — the middle clause is redundant with the third for the
   root (since `"/x".startswith("//")` is false, it is *not* redundant: it is the only way
   `/` becomes a candidate). *Recommendation:* say explicitly that the root mount point
   `/` is a candidate for every path, so implementers do not special-case it away.

A3. **`device_links` semantics are unspecified** (inherited from the contract; flagged
   again by the `CaseBtrfsUnmapped` seat). The contract lists
   `os.path.realpath(mount_source)` basename as a real-mode input and supplies
   `device_links` in the fixture, but never states the normative lookup (keyed by raw
   source? by resolved path? is `basename(source)` a permitted fallback? may a key be
   absent?). *This case is invariant under every reading I can construct*: the mount source
   is `/dev/sdb1`, whose raw basename is `sdb1` and whose `device_links` value is also
   `sdb1`, and no other device name appears in the fixture — so both readings select the
   same uuid. *Recommendation:* the contract should fix one rule, e.g. "the device basename
   of a mount source is `device_links[source]` when the key is present, otherwise
   `basename(source)`". (Concretely for this fixture: the mount source is `/dev/sdb1`, whose
   raw basename is `sdb1` and whose `device_links` value is also `sdb1`, and no other device
   name occurs anywhere in the fixture — so a raw-`basename(source)` implementation, a
   `device_links`-lookup implementation, and a resolved-path implementation all select the
   same uuid `7c3f2a1e-…`.)

A4. **The sealed expected field set cannot assert `device_check`.** The wave-1 item fixes
   the expected per-path fields to exactly `path, fstype, mount_point, quota_state,
   enforcement, basis`, so `device_check` (and `quota_option_keys`, `btrfs_qgroups_mode`)
   are unasserted by any case — even though this case deliberately pins the
   *btrfs-mismatch* branch. *Recommendation:* the oracle may additionally compare
   `device_check` for the sealed cases; the frozen real control already pins it
   (`btrfs_subvolume_skipped` for the fleet root, `match` for `/tmp`).

A5. **A trailing newline in the mountinfo text is not addressed** (also raised by
   `CaseBtrfsUnmapped`). A real `/proc/self/mountinfo` ends with `\n`, so the fixture text
   does too; the contract says an "unparseable mountinfo line" is a setup error but does
   not say whether the trailing empty segment counts as a line. A parser that splits on
   `\n` without skipping empty strings would answer `QUOTA_SETUP` here — an orthogonal
   failure that would mask this case's real signal. *Recommendation:* the contract should
   state that the mountinfo text is split into lines with empty segments ignored. As of
   this report every peer case file in `cases-proposed/` that I could see except one ends
   with `\n`, so the case set currently disagrees with itself on this point, which
   strengthens the case for a normative sentence.)

A6. **`device_check` ordering versus quota classification is only implicit.** The contract
   states the device check inside the mount-resolution paragraph and the quota
   classification as a separate table; it does not say explicitly that a `device_mismatch`
   verdict pre-empts the quota table. My case is insensitive to the order (both readings
   of the `/`-trap yield *unknown*, exit 2), so nothing is at risk, but the contract should
   say "the device check is applied first; on mismatch the path is `unknown` with basis
   `device_mismatch` and the quota table is not consulted".

## Residual risk / verification gaps

- The S-id↔source binding is inferred (registry rows not yet in `corpus/SOURCES.md`); only
  the `sources` array is at risk, not the expectation.
- The sealed expected object cannot assert `device_check`, `quota_option_keys`,
  `btrfs_qgroups_mode`, or the "never echo mount sources / other options" rule; those stay
  verified only by the frozen real control and reviewer inspection.
- A5 (trailing newline) is the one way this case can fail for a reason unrelated to the
  boundary behaviour; L1 may want to normalize it before sealing.
- No host observation backs this fixture: the mount lines, device names and uuids are
  synthetic. It is a behavioural fixture, not a reproduction of this host's quota state.
- The case pins the *combination* (btrfs chosen ⇒ disabled ⇒ exit 0) rather than the
  xfs `usrquota` classification per se; the xfs rows are exercised only as the trap.
  `CaseXfsUsrquota` (peer seat) covers the xfs row on its own terms.

---

# Correction — pre-seal amendment (`preseal-amendment.md`), applied before any candidate inspection

Appended by the same seat (`MadoR22-2.CaseBoundary-8`) after L1's amendment notice. **No
candidate implementation was opened, read, executed or tested** — the corrected case was
authored from the amendment text and the contract alone.

## Corrected artifact

- New file: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/cases-corrected/CaseBoundary.json`
  — same `schema` (`mori-quota-case-v1`), same `id` (`CaseBoundary`), same scenario intent,
  same fixture values except the mandated fixture-member addition, same expected object.
- The original proposal `cases-proposed/CaseBoundary.json` is **retained untouched**
  (sha256 `9a40c67f4c557e296582f07f9bdd0771b4fec6f84113f51c80c3cefce733c048`).

## Delta applied (fixture member `qgroups_enabled`)

The amendment makes `qgroups_enabled` a **required member of every `btrfs_sysfs` UUID
record** (true/false/null) and separates *initialisation* (directory present) from
*enabled* (the `enabled` attribute). Every record — including decoys — now carries it:

| uuid | devices | qgroups | qgroups_enabled | qgroups_mode | why |
|---|---|---|---|---|---|
| `7c3f2a1e-9b4d-4c8a-8f61-2e5d0a7b9c33` | `["sdb1"]` | `false` | **`null`** | `null` | the device behind the chosen `/a` mount: the qgroups **directory is absent**, and the amendment requires `qgroups false` to pair with `enabled=null`/`mode=null` |
| `d41a9f60-3c72-4e15-9b8a-6f0c2e7d4a81` | `["dm-0"]` | `true` | **`true`** | `"squota"` | the decoy: directory **present** and `enabled` true → for *its* device the verdict would be enabled / unknown / `btrfs_qgroups_enabled`; it is a different device and must not contribute |

Nothing else in the fixture changed: `mountinfo`, `paths`, `device_links` are byte-identical
to the original proposal (verified by comparison), and the expected object is unchanged.

## Re-derivation under the amendment (expected object is identical)

1. **Covering-mountpoint multiplicity.** Amendment: *"if ANY covering mountpoint occurs more
   than once, refuse classification as unknown/n/a/`ambiguous_overmount`"*. Covering
   mountpoints for realpath `/a/bc` are `/` and `/a`; each occurs exactly **once** in the
   mountinfo text, so the refusal does not apply. (`/a/b` is not a covering mountpoint for
   `/a/bc`: `/a/bc` does not start with `/a/b/`.)
2. **Mount resolution.** *"Longest component-prefix selection remains"*; *"parse separator
   and the last THREE fields of EACH chosen line"*, *"ignore empty trailing lines"*. Chosen
   mount point **`/a`** (longest covering prefix), fstype `btrfs`, source `/dev/sdb1`,
   major:minor `0:30`. The trailing empty segment of the mountinfo text is ignored, and the
   last three fields of the chosen line are `btrfs /dev/sdb1 rw,compress=zstd:3,ssd,…`.
3. **Device check.** Amendment: *"Device mismatch PREEMPTS the filesystem table"*;
   *"Btrfs skips equality only when stat major is 0"*. The path `st_dev` is `0:57` — stat
   major **0** — so the btrfs equality skip applies and the `0:30` vs `0:57` difference is
   **not** a `device_mismatch`; the path proceeds to the btrfs table. (Had the stat major
   been nonzero, the preemption would have produced unknown/`device_mismatch` and my
   expectation would have been wrong — the fixture is deliberately chosen with a zero stat
   major, matching the frozen real control's fleet-root pattern.)
4. **btrfs row.** Amendment: *"Absent dir retains disabled/n/a/`btrfs_qgroups_dir_absent`
   only on a successful parent inspection"*; present+enabled=true → enabled/unknown/
   `btrfs_qgroups_enabled`; present+enabled=false → disabled/n/a/`btrfs_qgroups_disabled`;
   present+enabled=null → unknown/n/a/`btrfs_qgroups_enabled_unavailable`. The selected
   device's uuid has the directory **absent** (`qgroups:false`, `qgroups_enabled:null`) →
   **disabled / n/a / `btrfs_qgroups_dir_absent`** — the same basis token as the original
   proposal, because the absent-directory branch is explicitly retained by the amendment.
5. **Source resolution.** Amendment: *"lookup RAW decoded source in `device_links`; use its
   mapped basename when present, otherwise `basename(source)`"*. The raw decoded source
   `/dev/sdb1` **is** a `device_links` key, mapping to `sdb1` — identical to
   `basename("/dev/sdb1")`, so the lookup is invariant. Exactly **one** uuid lists `sdb1`
   → mapped, not zero/multiple.
6. **Verdict precedence.** Well-formed fixture; the single path is disabled; nothing enabled
   or unknown → **exit 0, `QUOTA_DISABLED`**.

**Expected object (unchanged):** exit `0`, finding_id `QUOTA_DISABLED`, path `/a/bc` →
fstype `btrfs`, mount_point `/a`, quota_state `disabled`, enforcement `n/a`, basis
`btrfs_qgroups_dir_absent`.

## Amendment clauses that do NOT apply to this case (and why)

- **ext2/3/4 → always unknown** / `ext_quota_option_unverified`: the ext4 root mount is
  never the chosen mount for this path (it is not a covering mountpoint of `/a/bc` beyond
  the shorter `/`), and it carries no quota option key, so it would retain
  `ext_quota_superblock_unobservable` in any case. No ext expectation exists in this case.
- **Duplicated covering mountpoint → `ambiguous_overmount`** (fstype null, mount_point null,
  device_check `not_checked`): no covering mountpoint repeats here, so this case keeps a
  concrete fstype/mount_point. The decoy uuid is a *device* decoy, not a mountpoint decoy.
- **`btrfs_qgroups_enabled` (present+enabled=true)** applies only to the `dm-0` decoy
  device; the selected device's directory is absent.
- **XFS precedence, tmpfs key list, `quota_option_keys` vocabulary, octal escapes,
  `noquota`/`jqfmt` extension**: not exercised — the fixture's xfs line carries `usrquota`
  only, the mountinfo contains no backslash escapes, and `quota_option_keys` for a btrfs
  path is `[]` per the amendment (btrfs mechanism is sysfs, not options), which is outside
  the six scored fields.

## Discriminating power after the amendment

1. Bare-prefix mount matching (no component boundary) → `/a/bc` matches `/a/b` → the xfs
   mount. Under the amendment's preemption this lands on **device mismatch** first
   (`259:1` vs stat `0:57`, fstype not btrfs) → unknown / `device_mismatch` / exit 2
   `QUOTA_STATE_UNKNOWN`; if the device check were skipped, on the xfs quota row →
   enabled / enforced / `xfs_quota_option` / exit 1 `QUOTA_ENABLED`. **Both differ from the
   expected exit 0 and from the expected fstype, mount_point and basis → caught either way.**
2. Root `/` chosen instead of the longer `/a` → ext4, `8:2` vs stat `0:57` → unknown /
   `device_mismatch`, exit 2 → **caught**.
3. Device check applied to btrfs as a non-btrfs (i.e. ignoring the "stat major 0" skip) →
   unknown / `device_mismatch`, exit 2 → **caught**.
4. Ignoring the device→uuid mapping and asking "does *any* uuid have qgroups enabled?" → the
   decoy (`dm-0`, present+enabled=true) yields enabled → exit 1 → **caught**.
5. Treating a btrfs *present* directory as enabled without reading `enabled` (the error the
   amendment corrects) → for the selected device the directory is **absent**, so this error
   is invisible here; that error class is what the amendment's `qgroups_enabled` member
   exposes and it is exercised by the decoy record, whose directory is present.

## Residual risk / verification gaps (correction)

- The corrected case was validated by a **local parse and rule re-derivation only**
  (key sets, types, canonical-UUID / canonical-`MAJ:MIN` / basename shapes, covering-
  mountpoint multiplicity, longest-prefix choice, device→uuid mapping, stat-major-0 skip,
  verdict precedence). No tool was installed or updated; no candidate was read or run.
- The expected object still cannot assert `device_check`, `quota_option_keys` or
  `qgroups_mode` (the amendment keeps the six scored fields as the denominator and adds
  supplementary checks "where given"). For this path the amendment's own rules imply
  `device_check` = the btrfs-skip value and `quota_option_keys` = `[]`.
- The S077–S084 id mapping remains inferred from the wave's `DraftSourceRows` draft (rows
  still not in `corpus/SOURCES.md`); only the `sources` array is at risk, not the
  expectation.

## Final hashes (sha256)

| file | sha256 |
|---|---|
| `.ufo/waves/round-23/cases-proposed/CaseBoundary.json` (original, untouched) | `9a40c67f4c557e296582f07f9bdd0771b4fec6f84113f51c80c3cefce733c048` |
| `.ufo/waves/round-23/cases-corrected/CaseBoundary.json` (new) | `2e2ef692060105f054f2561091cb7603e77b1328b7954f63046ff57e7bea5d52` |
| `.ufo/waves/round-23/build/CaseBoundary.md` (this report) | self-referential — the digest of this file is computed after the last edit and reported to L1 directly; it cannot be embedded here without invalidating itself |

(The two case-file hashes above are final. The report's own digest is sent to L1 in the
seat message.)
