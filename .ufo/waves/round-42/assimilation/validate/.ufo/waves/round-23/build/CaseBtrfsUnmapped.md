# CaseBtrfsUnmapped — C2 fixture case (mori round 23, wave 1)

Seat: `MadoR22-2.CaseBtrfsUnmapped-8` · role: reviewer (case author) · lane: leaf, no dispatch.

## Deliverable

- Case file (the only file this seat wrote besides this report):
  `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/cases-proposed/CaseBtrfsUnmapped.json`
  — schema `mori-quota-case-v1`, id `CaseBtrfsUnmapped`, one `mori-quota-fixture-v1`
  object, expected exit `2` / `QUOTA_STATE_UNKNOWN`, one expected path.
- No production file, no other case file, no `.scratch` write, no host probe, no
  privileged command, no VCS mutation. JSON well-formedness only was checked
  (parse + key-set inspection of my own file). No tool was installed or updated
  this seat, so there is no tool/version/channel record to report.

## Independence statement

The expectation was derived only from `.ufo/waves/round-23/contract.md` §C2 and
the named kernel sources opened read-only over HTTPS (no file written locally).
I did **not** read `.ufo/waves/round-23/build/ImplQuota/`, any
`.scratch/round23/ImplQuota` clone, `build/OracleQuota/`, or
`cases-proposed/` peers' files. I did not read the host's quota state.

## Scenario

A btrfs mount whose source resolves to a device basename that **no** uuid under
`/sys/fs/btrfs` lists. The device→filesystem mapping therefore fails, and the
quota state must be *unknown* (`btrfs_device_unmapped`), not enabled and not
disabled.

Fixture shape (all values are synthetic; nothing was observed on this host):

| element | value | why |
|---|---|---|
| mount source | `/dev/mapper/vault` | btrfs source naming a device that no uuid claims |
| `device_links` | `/dev/mapper/root`→`dm-0`, `/dev/mapper/vault`→`dm-9` | supplies the device basename for a source path (the real-mode `realpath(mount_source)` basename) |
| uuid `1d02a454-c549-4a35-b567-89d60902af8e` | `devices:["dm-0"]`, `qgroups:false`, mode `null` | a filesystem that exists but does not own `dm-9` |
| uuid `b3f1c7d2-5a08-4e93-9c64-7d2e1f0a8b55` | `devices:["dm-1"]`, `qgroups:true`, mode `"squota"` | a qgroup-capable filesystem on a *different* device — must not leak into the verdict |
| path | `/srv/data/store` (realpath identical), `st_dev` `0:57` | under the `/srv/data` btrfs mount (mount major:minor `0:44`) |
| other mountinfo lines | `/proc` (proc), `/` (btrfs `/dev/mapper/root`), `/tmp` (xfs, `noquota`) | realism + a `/` btrfs candidate that must lose to the longer mount point |

## Derivation (contract §C2, step by step)

1. **Mount resolution** — "Candidate mounts: mount point equals realpath, or is
   `/`, or realpath starts with mount point + `/`. Choose the **longest** mount
   point; among equal mount points the **last** line wins."
   For realpath `/srv/data/store` the candidates are `/` (line 2) and `/srv/data`
   (line 4, since `/srv/data/store` starts with `/srv/data/`). Longest wins →
   **mount_point `/srv/data`**, fstype `btrfs`, source `/dev/mapper/vault`.
   The `/` line is not selected. (`/proc` and `/tmp` are not prefixes.)
2. **Device check** — "If chosen fstype is not btrfs and its major:minor ≠ the
   path's st_dev → `unknown` basis `device_mismatch`. For btrfs a mismatch is
   expected (per-subvolume anonymous st_dev, S081) and is recorded as
   `device_check: "btrfs_subvolume_skipped"`; equal → `device_check: "match"`."
   Here fstype is btrfs and `0:44` ≠ `0:57`, so the mismatch branch is *not* a
   `device_mismatch` verdict; the path proceeds to quota classification. This
   reading is independently corroborated by the frozen real control
   `frozen/c2-expected-real.json`, whose btrfs fleet root (mount `0:30`, st_dev
   `0:57`) carries basis `btrfs_qgroups_dir_absent`, not `device_mismatch`.
3. **btrfs device→uuid mapping** — "source basename maps to exactly one uuid
   whose `qgroups` is true → enabled"; "… exactly one uuid, `qgroups` false →
   disabled"; "**zero or several uuids list the device → unknown, n/a,
   `btrfs_device_unmapped`**."
   Source basename = `dm-9` (via `device_links`). Neither uuid lists `dm-9`
   (`dm-0`, `dm-1`), so **zero** uuids list the device →
   `quota_state=unknown`, `enforcement=n/a`, `basis=btrfs_device_unmapped`.
4. **Verdict precedence** — "setup error → 2 `QUOTA_SETUP`; else any `enabled` →
   1 `QUOTA_ENABLED`; else any `unknown` → 2 `QUOTA_STATE_UNKNOWN`; else 0
   `QUOTA_DISABLED`." The fixture is well formed (no setup error), no path is
   enabled, one path is unknown → **exit 2, `finding_id` `QUOTA_STATE_UNKNOWN`**.

Expected (sealed object, exactly the six contract fields, in the contract's
order): `path /srv/data/store`, `fstype btrfs`, `mount_point /srv/data`,
`quota_state unknown`, `enforcement n/a`, `basis btrfs_device_unmapped`.

## Source anchors used (S079, S080, S081, S082)

All opened read-only at `raw.githubusercontent.com/torvalds/linux/v7.2` (no local
copy written).

- **S082** — `Documentation/filesystems/proc.rst` §3.5 (lines 1939–1957):
  field list `(1)…(m+4)`; `:1949` "(3) major:minor: value of st_dev for files
  on filesystem"; `:1954` "(m+1) separator: marks the end of the optional
  fields"; `:1957` "(m+4) super options: per super block options"; `:1959`
  "Parsers should ignore all unrecognised optional fields." → grounds the
  mountinfo grammar and the `shared:N` optional-field handling used in the
  fixture.
- **S081** — `fs/btrfs/inode.c:8242`: `stat->dev = BTRFS_I(inode)->root->anon_dev;`
  → grounds the btrfs per-subvolume anonymous `st_dev` and hence the
  "mismatch is expected" branch that keeps the path on the btrfs quota row.
- **S079** — `fs/btrfs/sysfs.c`: `:2452-2456` "Path: /sys/fs/btrfs/<uuid>/qgroups/"
  with `qgroups_attrs` (`enabled`, `mode`); `:2586` `btrfs_sysfs_add_qgroups`;
  `:2266` `devices_kobj = kobject_create_and_add("devices", …)`; `:2155`
  `sysfs_create_link(devices_kobj, disk_kobj, disk_kobj->name)` → grounds that
  `<uuid>/devices/` entries are kernel disk names (e.g. `dm-0`) and that
  `<uuid>/qgroups/` is the visible qgroup surface.
- **S080** — `fs/btrfs/qgroup.c`: `:441` and `:1032` `btrfs_sysfs_add_qgroups(fs_info);`,
  `:620`, `:689`, `:1295` `btrfs_sysfs_del_qgroups(fs_info);` → grounds that the
  `qgroups` sysfs group exists only while qgroup support is on, so its presence
  is the enable signal and its absence the disable signal.

S-id binding caveat: `corpus/SOURCES.md` still ends at S076; the S077–S084 rows
are not yet written. I mapped S077–S084 by the order of the wave-1
`DraftSourceRows` item (xfs.rst, xfs_super.c, btrfs `sysfs.c`, btrfs
`qgroup.c`, btrfs `inode.c`, `proc.rst`, ext4.rst, tmpfs.rst) and cross-checked
the offset with the contract's own "per-subvolume anonymous st_dev, **S081**",
which lands exactly on `fs/btrfs/inode.c` `anon_dev`. If the sealed registry
rows differ, this case's `sources` array must be re-mapped; **the expectation
does not change** (it is derived from the contract table, not from the S-ids).

## Discriminating power (what a wrong implementation gets caught on)

1. Ignoring the longest-mount-point rule and taking the `/` btrfs mount →
   basis `btrfs_qgroups_dir_absent`, exit 0 `QUOTA_DISABLED` → **caught**.
2. Applying `device_mismatch` to a btrfs st_dev mismatch → basis
   `device_mismatch` → **caught** (contradicts the frozen real control).
3. Treating "some uuid has `qgroups: true`" as enabled → exit 1
   `QUOTA_ENABLED` → **caught** by the unrelated qgroup-capable uuid.
4. Defaulting an unmappable btrfs device to *disabled* → exit 0 → **caught**.

## Contract ambiguities found (for L1 / the contract owner)

A1. **`device_links` semantics are unspecified** (contract §C2, "Real-mode
   inputs only" vs the fixture object). The contract lists
   `os.path.realpath(mount_source)` basename as a real-mode input and the
   fixture supplies `device_links{"/dev/mapper/root":"dm-0"}`, but it never
   states the normative fixture rule: is the lookup keyed by the *raw* mount
   source, by its resolved path, is `basename(source)` a permitted fallback,
   and may a key be absent? My expectation is **invariant** under every reading
   (`dm-9` and `vault` are listed by no uuid), so the case is safe — but the
   case set cannot discriminate a `device_links`-ignoring implementation.
   *Recommendation:* the contract should fix one rule, e.g. "the device
   basename of a mount source is `device_links[source]` when the key is
   present, otherwise `basename(source)`".

A2. **A trailing newline in the mountinfo text is not addressed.** A real
   `/proc/self/mountinfo` ends with `\n`, so the fixture ends with `\n`; the
   contract says an "unparseable mountinfo line" is a setup error but does not
   say whether a trailing empty segment counts as a line. A parser using
   `text.split("\n")` without skipping empty strings would answer
   `QUOTA_SETUP` here. *Recommendation:* the contract should state that the
   mountinfo text is split into lines with empty segments ignored (or that a
   single trailing newline is not a line). Flagging it because it is the one
   place where this otherwise robust case could fail for an orthogonal reason.

A3. **`btrfs_qgroups_mode` token vocabulary is open.** The contract says "the
   mode text or null" without enumerating values. The kernel emits exactly two
   tokens: `qgroup` (BTRFS_QGROUP_MODE_FULL) and `squota`
   (BTRFS_QGROUP_MODE_SIMPLE) — `fs/btrfs/sysfs.c` `qgroup_mode_show`
   (~2370–2394). My fixture uses `"squota"` for the unrelated uuid; it is never
   read for this path (no uuid maps to `dm-9`, so this path's
   `btrfs_qgroups_mode` is `null`). *Recommendation:* the contract should
   declare the allowed token set so an implementation cannot invent one.

A4. **`btrfs_device_unmapped` is overloaded.** One basis token covers both
   "zero uuids list the device" and "several uuids list the device" (the latter
   is a *conflicting* mapping, this case is a *missing* one). The verdict is
   `unknown` in both, so the token is honest about the outcome but not about
   the cause. *Recommendation:* acceptable as-is, but the docs should say the
   basis does not distinguish "absent" from "ambiguous" mapping.

A5. **`device_check` is outside the sealed expected object.** The wave-1 item
   fixes the expected per-path fields to exactly `path, fstype, mount_point,
   quota_state, enforcement, basis`, so `device_check` (and `quota_option_keys`,
   `btrfs_qgroups_mode`) are unasserted by any case. This case deliberately
   pins the *btrfs-mismatch* branch (mount `0:44` vs st_dev `0:57`) but cannot
   assert `device_check == "btrfs_subvolume_skipped"`. *Recommendation:* the
   oracle may additionally compare `device_check` for the sealed cases, since
   the contract defines the token; the frozen real control already pins it
   (`btrfs_subvolume_skipped` for the fleet root, `match` for `/tmp`).

A6. **Super options vs mount options.** "super options = last mountinfo
   field" is unambiguous, and for this case field 6 (`rw,relatime`) and field 11
   both contain no quota key, so the case is insensitive to a mis-reading
   between them. No action needed; noted because a btrfs/xfs case with
   differing field 6/11 would be sensitive.

## Residual risk / verification gaps

- The S-id↔source binding is inferred, not yet observed in `corpus/SOURCES.md`
  (see caveat above). Only the `sources` array is at risk; the expectation is
  not.
- The sealed expected object cannot assert `device_check`, `quota_option_keys`,
  `btrfs_qgroups_mode`, or the "never echo mount sources / other options"
  rule; those remain verified only by the frozen real control and by reviewer
  inspection, not by this case.
- A2 (trailing newline) is the only identified way this case can fail for a
  reason unrelated to the unmapped-device behaviour. L1 may want to normalize
  it (e.g. accept both, or state the rule) before sealing.
- No host observation backs this fixture: the device names, uuids and mount
  lines are synthetic. It is a behavioural fixture, not a reproduction of this
  host's quota state.

---

# Correction — round-23 pre-seal amendment (appended after the amendment was read)

Authored on L1's instruction (MadoR22-2) after
`.ufo/waves/round-23/preseal-amendment.md` was issued and **before** any
ImplQuota candidate was opened or any C2 result was observed. No
implementation, oracle, or peer case file was read; no test or smoke run was
executed; only the corrected case's own JSON was parse-checked.

- Original proposal left **untouched**: `cases-proposed/CaseBtrfsUnmapped.json`,
  sha256 `c8796c446b4ab21dbc3a328ed309ceec855b17cf7318593c679ac13504244015`,
  3798 bytes, mtime 2026-10-21 14:27:14 -0300 (unchanged).
- Corrected case (new, same id): `cases-corrected/CaseBtrfsUnmapped.json`,
  sha256 `1986ade4a150637c62102316fcec8c55523919d35c377759a5908d1e682e59b1`,
  4980 bytes, mtime 2026-10-21 14:51:19 -0300.

## Delta (what changed, and what did not)

1. **Fixture** — the only fixture change is the amendment's new required
   fixture member `qgroups_enabled` in each `btrfs_sysfs` UUID record:
   - `1d02a454-c549-4a35-b567-89d60902af8e` (decoy, `qgroups:false`) →
     `qgroups_enabled: null`, `qgroups_mode: null` (the amendment's
     "qgroups false must pair with enabled=null/mode=null").
   - `b3f1c7d2-5a08-4e93-9c64-7d2e1f0a8b55` (decoy, `qgroups:true`) →
     `qgroups_enabled: true`, `qgroups_mode: "squota"`.
   - Record keys are now exactly `devices`, `qgroups`, `qgroups_enabled`,
     `qgroups_mode`; fixture top-level keys, `paths` shape, `device_links` and
     the mountinfo text are byte-identical to the original proposal.
2. **Expected (six scored fields)** — **unchanged**:
   `path /srv/data/store`, `fstype btrfs`, `mount_point /srv/data`,
   `quota_state unknown`, `enforcement n/a`, `basis btrfs_device_unmapped`;
   `exit 2`, `finding_id QUOTA_STATE_UNKNOWN`.
   The amendment's renamed bases (`btrfs_qgroups_enabled`,
   `btrfs_qgroups_disabled`, `btrfs_qgroups_enabled_unavailable`,
   `ext_quota_option_unverified`, `ambiguous_overmount`) belong to the
   enabled/disabled/unavailable, ext-positive and duplicated-covering-point
   cases — none of which this unmapped-device case exercises. The amendment
   keeps "zero or multiple UUID matches remains unknown", so
   `btrfs_device_unmapped` (contract token, not superseded) stands.
3. **Supplementary (scored separately from the six-field denominator, per the
   amendment)** — for `/srv/data/store`:
   `device_check = btrfs_subvolume_skipped`, `quota_option_keys = []`,
   `btrfs_qgroups_mode = null`.

## Amended derivation (re-run, same conclusion)

1. *Mount resolution* — covering mountpoints for realpath `/srv/data/store`
   are `/` (line 2) and `/srv/data` (line 4). Neither occurs more than once,
   so the amendment's `ambiguous_overmount` refusal does **not** fire; longest
   component-prefix wins → mount point `/srv/data`, fstype `btrfs`.
2. *Line parsing* — separator and the last three fields of the **chosen** line
   only → fstype `btrfs`, source `/dev/mapper/vault`, super options
   `rw,compress=zstd:3,ssd,discard=async,space_cache=v2,subvolid=256,subvol=/@vault`;
   no backslash escapes present, so the octal-decode/reject rule is not
   triggered; the trailing empty segment after the final newline is ignored
   (amendment: "ignore empty trailing lines").
3. *Device check* — path `st_dev` `0:57` has **major 0**, so for btrfs the
   equality check is skipped and the path is **not** preempted into
   `device_mismatch` (a nonzero stat major mismatching the mount would
   preempt). The frozen real control uses the same skip for its btrfs fleet
   root (mount `0:30`, st_dev `0:57`).
4. *Source resolution* — the raw decoded source `/dev/mapper/vault` is a
   `device_links` key → mapped basename `dm-9`; the two UUID device lists are
   `['dm-0']` and `['dm-1']` → **zero** UUIDs list `dm-9` → `unknown` /
   `n/a` / `btrfs_device_unmapped`. (The amendment's `basename(source)`
   fallback would yield `vault`, also unlisted — the expectation is invariant
   under both readings, and A1 from the original report is now closed: the rule
   is "lookup RAW decoded source in device_links".)
5. *qgroup state* — the decoy uuid with `qgroups:true`/`qgroups_enabled:true`/
   `mode:"squota"` is a **different** device: qgroup presence is an
   INITIALIZED state, not proof that this path's device is qgroup-enabled, and
   its mode must not leak. No uuid maps to `dm-9`, so no uuid is consulted and
   this path's mode is `null` ("never reads mode unless enabled is 1").
6. *Verdict precedence* — no path enabled, one path unknown → exit 2,
   `QUOTA_STATE_UNKNOWN`.

## Amendment-driven ambiguities that remain open

- **N1** — the amendment does not name the device_check token for "btrfs, stat
  major 0 → equality skipped". I kept the original contract token
  `btrfs_subvolume_skipped`, corroborated by the frozen real control. If the
  sealed implementation renamed it, the supplementary assertion must be
  re-mapped (the six scored fields are unaffected).
- **N2** — the fixture still declares `"schema":"mori-quota-fixture-v1"` while
  its UUID records now carry a member absent from the contract's v1 example.
  The amendment mandates the member but does not bump the fixture schema
  string, and the contract makes "extra keys" a setup error, so a strict
  v1-shape validator would reject this fixture. *Recommendation:* the contract
  should state that the amended fixture is still `mori-quota-fixture-v1` with
  the extended UUID record, or bump it explicitly.
- **N3** — the amendment says "supplementary sealed checks additionally verify
  device_check, quota_option_keys and qgroups_mode where given", but the case
  file's `expected` key set was enumerated by the wave-1 item as exactly
  `exit`/`finding_id`/`paths` with exactly six fields per path. To keep the
  original six-field denominator intact and the case schema unaltered, the
  supplementary values are stated in the case's `rationale` (prefixed
  `SUPPLEMENTARY`) and here, not as extra JSON keys. L1 may want a structured
  field before sealing; the oracle can equally derive them from the contract.
- **N4** — the amendment's `btrfs_qgroups_mode` spelling differs from the
  contract's output key `btrfs_qgroups_mode`; I treat them as the same value
  and keep the contract's output key.

## Residual risk after the correction

- The six scored fields are unchanged from the original proposal, so no
  amendment clause can have invalidated the derivation; the only movement is
  the added `qgroups_enabled` member, which this case never consults.
- N1–N4 are naming/shape questions, not behavioural ones; none can change the
  exit code or the `QUOTA_STATE_UNKNOWN` finding for this case.
- The supplementary assertions are stated in prose only (N3), so an oracle
  that reads the case file programmatically will not see them unless L1
  normalizes the format.
