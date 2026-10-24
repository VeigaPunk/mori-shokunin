# CaseBtrfsTwoUuids — C2 fixture case (mori round 23, wave 1)

Seat: `MadoR22-2.CaseBtrfsTwoUuids-8` · role: reviewer (case author) · lane: leaf, no dispatch.

## Deliverable

- Case file (the only file this seat wrote besides this report):
  `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/cases-proposed/CaseBtrfsTwoUuids.json`
  — schema `mori-quota-case-v1`, id `CaseBtrfsTwoUuids`, one `mori-quota-fixture-v1`
  object, expected exit `2` / `QUOTA_STATE_UNKNOWN`, one expected path.
- No production file, no other case file, no `.scratch` write, no host probe, no
  privileged command, no VCS mutation. Only JSON well-formedness and key-set
  conformance of my own file were checked (parse + structural assertions; no
  tool was run against the candidate, because no candidate exists yet).
- No tool was installed or updated this seat, so there is no
  tool/version/channel record to report. `curl 8.23.0` and `python3 3.14.8`
  (pre-installed) were used for the read-only source fetches and the JSON check.

### File-name note (for L1)

The wave-1 item text says `cases-proposed/<YourSeatName>.json`. I used the
short seat name `CaseBtrfsTwoUuids` for both the file name and the `id` field,
which is the convention every other wave-1 case file in `cases-proposed/`
follows (`CaseBtrfsUnmapped.json` → `id: "CaseBtrfsUnmapped"`, etc.) and
matches the report path this seat was given
(`.ufo/waves/round-23/build/CaseBtrfsTwoUuids.md`). The roster id is
`MadoR22-2.CaseBtrfsTwoUuids-8`; if L1 prefers the roster id as the `id`
value, only the `id` string and the file name need renaming — the fixture and
the expectation are unaffected.

## Independence statement

The expectation was derived only from `.ufo/waves/round-23/contract.md` §C2 and
the named kernel sources opened read-only over HTTPS (no file written locally).
I did **not** read `.ufo/waves/round-23/build/ImplQuota/`, any
`.scratch/round23/ImplQuota` clone, `build/OracleQuota/`, or the `expected`
block of any peer file in `cases-proposed/`. I read only peer *structural*
keys (`id`, key sets, fixture path-entry key sets) to match the wave's file
format convention, and I did not read the host's quota state.

## Scenario

A btrfs mount whose device basename is listed under **two** different uuids
under `/sys/fs/btrfs`. The device→filesystem mapping is therefore ambiguous:
the probe cannot tell which filesystem the mount belongs to, so the quota state
must be *unknown* (`btrfs_device_unmapped`) — not enabled, not disabled.

Fixture shape (all values synthetic; nothing was observed on this host):

| element | value | why |
|---|---|---|
| mount source | `/dev/dm-3` | btrfs source for the mount under test |
| `device_links` | `/dev/dm-0`→`dm-0`, `/dev/dm-3`→`dm-3` | supplies the device basename for a source path (the real-mode `realpath(mount_source)` basename) |
| uuid `3e8a1c47-…-58c71b4d2093` | `devices:["dm-0"]`, `qgroups:false`, mode `null` | a real but unrelated filesystem on a different device — must not leak into the verdict |
| uuid `a7c3e9d1-…-5c7f0a3b6e11` | `devices:["dm-3"]`, `qgroups:true`, mode `"qgroup"` | **claimant 1** of the device under test |
| uuid `f2b5d804-…-91b0e5c7d2a4` | `devices:["dm-3"]`, `qgroups:true`, mode `"qgroup"` | **claimant 2** of the device under test |
| path | `/srv/data/store` (realpath identical), `st_dev` `0:57` | under the `/srv/data` btrfs mount (mount major:minor `0:44`) |
| other mountinfo lines | `/proc` (proc), `/` (btrfs `/dev/dm-0`), `/tmp` (xfs, `noquota`) | realism + a `/` btrfs candidate that must lose to the longer mount point |

## Derivation (contract §C2, step by step)

1. **Mount resolution** — "Candidate mounts: mount point equals realpath, or is
   `/`, or realpath starts with mount point + `/`. Choose the **longest** mount
   point; among equal mount points the **last** line wins."
   For realpath `/srv/data/store` the candidates are `/` (the `/@root` btrfs
   line) and `/srv/data` (the `/@data` btrfs line, since `/srv/data/store`
   starts with `/srv/data/`). Longest wins → **mount_point `/srv/data`**, fstype
   `btrfs`, mount source `/dev/dm-3`, mount major:minor `0:44`. The `/` line is
   not selected. (`/proc` and `/tmp` are not prefixes.)
2. **Device check** — "If chosen fstype is not btrfs and its major:minor ≠ the
   path's st_dev → `unknown` basis `device_mismatch`. For btrfs a mismatch is
   expected (per-subvolume anonymous st_dev, S081) and is recorded as
   `device_check: "btrfs_subvolume_skipped"`; equal → `device_check: "match"`."
   Here fstype is btrfs and `0:44` ≠ `0:57`, so the `device_mismatch` verdict
   does not apply; the path proceeds to quota classification. Corroborated
   independently by the frozen real control `frozen/c2-expected-real.json`,
   whose btrfs fleet root (mount `0:30`, st_dev `0:57`) carries basis
   `btrfs_qgroups_dir_absent`, not `device_mismatch`.
3. **btrfs device→uuid mapping** — the contract's btrfs rows are:
   (a) "source basename maps to exactly one uuid whose `qgroups` is true" →
   `enabled` / `unknown` / `btrfs_qgroups_dir_present`;
   (b) "… exactly one uuid, `qgroups` false" → `disabled` / `n/a` /
   `btrfs_qgroups_dir_absent`;
   (c) "**zero or several uuids list the device**" → `unknown` / `n/a` /
   `btrfs_device_unmapped`.
   The device basename is `dm-3` (via `device_links`), and **two** uuids list
   `dm-3` in their `devices` arrays → row (c) governs:
   `quota_state=unknown`, `enforcement=n/a`, `basis=btrfs_device_unmapped`.
4. **Verdict precedence** — "setup error → 2 `QUOTA_SETUP`; else any `enabled` →
   1 `QUOTA_ENABLED`; else any `unknown` → 2 `QUOTA_STATE_UNKNOWN`; else 0
   `QUOTA_DISABLED`." The fixture is well formed (no setup error), no path is
   enabled, the single path is unknown → **exit 2, `finding_id`
   `QUOTA_STATE_UNKNOWN`**.

Expected (sealed object, exactly the six contract fields, in the contract's
order): `path /srv/data/store`, `fstype btrfs`, `mount_point /srv/data`,
`quota_state unknown`, `enforcement n/a`, `basis btrfs_device_unmapped`.

### Why both claimants carry `qgroups: true` (deliberate design choice)

My first draft had claimant 1 at `qgroups: true` and claimant 2 at
`qgroups: false`. That fixture is *ambiguous under the contract text*: row (a)
reads "source basename maps to **exactly one uuid whose `qgroups` is true**",
which — read as a filter over the claimants rather than as a precondition on the
claimant count — would be satisfied by exactly one `qgroups: true` claimant even
though two uuids list the device. An implementation that filters claimants by
`qgroups` before counting would then report `enabled` /
`btrfs_qgroups_dir_present`, while an implementation that counts claimants
first would report `unknown` / `btrfs_device_unmapped`. A sealed case must not
depend on which of those two readings the implementer picks.

With **both** claimants at `qgroups: true` the expectation `unknown` /
`btrfs_device_unmapped` holds under every reading of rows (a) and (b): no
reading of "exactly one uuid whose `qgroups` is true" is satisfied by two
claimants, and no reading of "exactly one uuid, `qgroups` false" is satisfied
either. The case therefore isolates the row (c) condition alone, which is
exactly the condition the scenario is about. The trade-off is that the case no
longer discriminates "filter-then-count" from "count-then-filter"; the
disagreeing-claimant variant belongs in a *separate* case, where the
expectation is deliberately a function of the contract's chosen reading. I
recommend L1 commission that variant explicitly with its reading pinned.

## Source anchors used (S079, S080, S081, S082)

All opened read-only at `raw.githubusercontent.com/torvalds/linux/v7.2` (no local
copy written). Digests re-verified by this seat on 2026-10-21 (prefix of the
SHA-256 of the fetched bytes): `fs/btrfs/sysfs.c` `ce146120f29ac29c`,
`fs/btrfs/qgroup.c` `121a0af27f9553a9`, `fs/btrfs/inode.c` `01a6ad07c09cd1a0`,
`Documentation/filesystems/proc.rst` `e760f716f8278dee` — all four match the
prefixes recorded in the wave-1 `DraftSourceRows` draft.

- **S082** — `Documentation/filesystems/proc.rst` §3.5, lines 1965–1990:
  `:1975` "(3) major:minor: value of st_dev for files on filesystem";
  `:1980` "(m+1) separator: marks the end of the optional fields";
  `:1981` "(m+2) filesystem type"; `:1982` "(m+3) mount source";
  `:1983` "(m+4) super options"; `:1985` "Parsers should ignore all
  unrecognised optional fields." → grounds the mountinfo grammar the fixture
  lines are written in, and the `shared:12` optional field used on the `/proc`
  line.
- **S081** — `fs/btrfs/inode.c:8215` `btrfs_getattr(…)`; `:8246`
  `stat->dev = BTRFS_I(inode)->root->anon_dev;` → grounds the btrfs
  per-subvolume anonymous `st_dev`, hence the "mismatch is expected" branch
  that keeps this path on the btrfs quota rows instead of `device_mismatch`.
- **S079** — `fs/btrfs/sysfs.c`: `:2266`
  `fs_devs->devices_kobj = kobject_create_and_add("devices", &fs_devs->fsid_kobj);`
  and `:2155` `ret = sysfs_create_link(devices_kobj, disk_kobj, disk_kobj->name);`
  → grounds that `/sys/fs/btrfs/<uuid>/devices/` entries are the block
  device's own kernel name (e.g. `dm-3`), i.e. the "device basename" the
  contract maps; `:2355` `qgroup_enabled_show` / `:2368`
  `BTRFS_ATTR(qgroups, enabled, …)`; `:2370` `qgroup_mode_show` / `:2395`
  `BTRFS_ATTR(qgroups, mode, …)`; `:2450-2451` the "Path:
  /sys/fs/btrfs/<uuid>/qgroups/" comment and `:2453-2459` `qgroups_attrs` →
  grounds the fixture's `qgroups` / `qgroups_mode` fields and the legality of
  the mode text: `qgroup_mode_show` emits exactly `qgroup`
  (BTRFS_QGROUP_MODE_FULL) or `squota` (BTRFS_QGROUP_MODE_SIMPLE), so the
  fixture's `"qgroup"` is a real kernel token.
- **S080** — `fs/btrfs/qgroup.c`: `:441` and `:1032`
  `btrfs_sysfs_add_qgroups(fs_info);`; `:620`, `:689`, `:1295`
  `btrfs_sysfs_del_qgroups(fs_info);` → grounds that the `qgroups` sysfs group
  exists only while qgroup support is on, so `qgroups: true` ⇔ the group is
  present, and the mode attribute is readable.

S-id binding caveat: `corpus/SOURCES.md` still ends at S076; the S077–S084 rows
are not yet written. I mapped S077–S084 by the order of the wave-1
`DraftSourceRows` item (xfs.rst, xfs_super.c, btrfs `sysfs.c`, btrfs `qgroup.c`,
btrfs `inode.c`, `proc.rst`, ext4.rst, tmpfs.rst) and cross-checked the offset
against the contract's own "per-subvolume anonymous st_dev, **S081**", which
lands exactly on `fs/btrfs/inode.c` `anon_dev`; the fetched digests of all four
files I used match the prefixes that draft records. If the sealed registry rows
differ, this case's `sources` array must be re-mapped; **the expectation does
not change** (it is derived from the contract table, not from the S-ids).

## Discriminating power (what a wrong implementation gets caught on)

1. Taking the **first** claimant uuid (`a7c3e9d1-…`, `qgroups: true`) → basis
   `btrfs_qgroups_dir_present`, exit 1 `QUOTA_ENABLED` → **caught**.
2. Taking the **last** claimant uuid → same as (1) here (both claimants agree),
   but caught in the disagreeing-claimant variant → **caught** (see design note).
3. Ignoring the longest-mount-point rule and taking the `/` btrfs mount
   (`/dev/dm-0`, claimed by exactly one uuid with `qgroups: false`) → basis
   `btrfs_qgroups_dir_absent`, exit 0 `QUOTA_DISABLED` → **caught**. This is
   the strongest trap in the fixture: the `/` mount is a *clean* single-claimant
   btrfs filesystem, so a resolver that takes the wrong mount still produces a
   well-formed btrfs verdict.
4. Applying `device_mismatch` to a btrfs st_dev mismatch → basis
   `device_mismatch` → **caught** (contradicts the frozen real control).
5. Resolving the device by the raw mount-source basename (`dm-3`) *without*
   consulting `device_links` → still `dm-3` here, so it is **not** caught by
   this case; the `device_links` semantics ambiguity (below) is therefore
   *not* exercised by this fixture — deliberately, since the contract's
   `device_links` semantics are not yet pinned.
6. Defaulting an ambiguous btrfs device to *disabled* (a plausible "qgroups
   dir not found" shortcut) → exit 0 `QUOTA_DISABLED` → **caught**.

## Contract ambiguities found (for L1 / the contract owner)

A1. **Row (c) of the btrfs table overloads one basis token for two different
   causes.** "zero or several uuids list the device → unknown / n/a /
   `btrfs_device_unmapped`" covers both a *missing* mapping (no uuid claims the
   device) and an *ambiguous* mapping (several uuids claim it). The verdict is
   `unknown` in both, so the token is honest about the outcome but not about the
   cause — and the two causes are operationally different (one is a
   configuration gap, the other a probe that must refuse to guess). The sealed
   expected object for this case therefore cannot distinguish "refused to guess
   between two claimants" from "found no claimant", and neither can a passing
   implementation. *Recommendation:* the contract should either add a distinct
   basis token for the ambiguous case (e.g. `btrfs_device_ambiguous`) or state
   explicitly that `btrfs_device_unmapped` is the single token for both, so a
   future implementer is not tempted to invent a second one.

A2. **"exactly one uuid whose `qgroups` is true" is grammatically ambiguous.**
   Row (a) can be read as (i) exactly one uuid lists the device, and that uuid
   has `qgroups: true` — a precondition on the claimant *count*; or (ii) among
   the uuids listing the device, exactly one has `qgroups: true` — a filter
   applied *before* the count. The two readings disagree exactly when two
   uuids list the device and only one of them has `qgroups: true`. My first
   draft sat on that fault line and was rewritten so the expectation holds
   under both readings. *Recommendation:* the contract should say "exactly one
   uuid lists the device, and its `qgroups` is true", and should add a
   sentence for the several-claimants case saying the claimant count is
   evaluated **before** any `qgroups` filtering.

A3. **`btrfs_qgroups_mode` token vocabulary is open.** The contract says "the
   mode text or null" without enumerating values. The kernel emits exactly two
   tokens: `qgroup` (BTRFS_QGROUP_MODE_FULL) and `squota`
   (BTRFS_QGROUP_MODE_SIMPLE) — `fs/btrfs/sysfs.c` `qgroup_mode_show`
   (2370–2395). This fixture uses `"qgroup"`, a real kernel token.
   *Recommendation:* the contract should declare the allowed token set so an
   implementation cannot invent one.

A4. **`device_check` and the other two output fields are outside the sealed
   expected object.** The wave-1 item fixes the expected per-path fields to
   exactly `path, fstype, mount_point, quota_state, enforcement, basis`, so
   `device_check` (and `quota_option_keys`, `btrfs_qgroups_mode`) are
   unasserted by any case. This case deliberately pins the *btrfs-mismatch*
   branch (mount `0:44` vs st_dev `0:57`) but cannot assert
   `device_check == "btrfs_subvolume_skipped"`. *Recommendation:* the oracle
   may additionally compare `device_check` for the sealed cases, since the
   contract defines the token; the frozen real control already pins it
   (`btrfs_subvolume_skipped` for the fleet root, `match` for `/tmp`).

A5. **`device_links` semantics are still unspecified** (shared with the
   `CaseBtrfsUnmapped` finding): the contract's real-mode inputs name
   "os.path.realpath(mount_source) basename" while the fixture supplies a
   `device_links` map from a device path to a device name. My fixture makes
   the two readings coincide (source `/dev/dm-3` → basename `dm-3` →
   `device_links["/dev/dm-3"] == "dm-3"`), so this case passes under either
   reading and therefore does not discriminate them. *Recommendation:* L1
   should pin the semantics once, in the contract, rather than leaving it to
   each fixture.

A6. **Trailing newline in the fixture's `mountinfo`.** The contract does not
   say whether the fixture's `mountinfo` string ends with `\n`. This fixture
   ends with a newline (as the real file does). An implementation that
   `split("\n")` without dropping a trailing empty string would see one
   unparseable "line" and — per "unparseable mountinfo line → exit 2
   `QUOTA_SETUP`" — would fail the case for a reason unrelated to the
   behaviour under test. *Recommendation:* the contract should state that
   blank lines are skipped, and/or the oracle should accept either form.

A7. **"the last line wins" among equal mount points.** Not exercised by this
   case (no two lines share a mount point), but it is the other half of the
   mount-resolution sentence and worth an explicit case.

## Residual risk / verification gaps

- The S-id↔source binding is inferred from the wave-1 `DraftSourceRows` draft,
  not yet observed in `corpus/SOURCES.md` (see caveat above). Only the
  `sources` array is at risk; the expectation is not.
- The sealed expected object cannot assert `device_check`, `quota_option_keys`,
  `btrfs_qgroups_mode`, or the "never echo mount sources / other options" rule;
  those remain verified only by the frozen real control and by reviewer
  inspection, not by this case.
- A6 (trailing newline) and A2 (the filter-vs-count reading) are the two
  identified ways this case can fail for a reason unrelated to the ambiguous
  mapping. A2 is mitigated by design (both claimants agree); A6 is not, and
  L1 may want to normalize it before sealing.
- The fixture's `/` btrfs mount and its unrelated single-claimant uuid are
  load-bearing for discriminating power (trap 3 above): if a future edit drops
  the `/` mount line, the case loses that trap. Both are present in the
  sealed file as written.
- No host observation backs this fixture: the device names, uuids and mount
  lines are synthetic. It is a behavioural fixture, not a reproduction of this
  host's quota state.

## Correction — round-23 pre-seal amendment (appended after the amendment was read)

Amended by parent instruction after `.ufo/waves/round-23/preseal-amendment.md`
was read. The amendment states it was written before L1 opened any ImplQuota
candidate and that no C2 result was observed; this correction is therefore
source/falsification-driven, not result-driven. **No implementation, candidate or
oracle was read, and no test was run.** The original proposal
`cases-proposed/CaseBtrfsTwoUuids.json` is retained **byte-unchanged**; the
corrected case is a new file in the explicitly authorized
`cases-corrected/` directory with the **same id**.

| artifact | bytes | sha256 |
|---|---|---|
| `cases-proposed/CaseBtrfsTwoUuids.json` (original, unchanged) | 5952 | `178ff8aec3d2257c8eb59eae9cffab440b36258fce5e66ce8b04b3fbc25ced19` |
| `cases-corrected/CaseBtrfsTwoUuids.json` (corrected) | 6839 | `6bdcea63cf12d1d63e82e6cbaca827c3e00729dfd016f28331d260d6f0e7328c` |

### Delta applied to the fixture

1. **New required fixture member `qgroups_enabled` in every `btrfs_sysfs` UUID
   record** (amendment, C2 btrfs rules: "Add required fixture member
   `qgroups_enabled` to each btrfs_sysfs UUID record: true/false/null").
   - claimant `a7c3e9d1-4f62-4b8e-9d21-5c7f0a3b6e11`: `qgroups: true`,
     `qgroups_enabled: true`, `qgroups_mode: "qgroup"`.
   - claimant `f2b5d804-7c19-4e62-8a3d-91b0e5c7d2a4`: `qgroups: true`,
     `qgroups_enabled: true`, `qgroups_mode: "qgroup"`.
   - decoy `3e8a1c47-9b25-4d0e-a6f3-58c71b4d2093` (other device `dm-0`):
     `qgroups: false`, `qgroups_enabled: null`, `qgroups_mode: null` — the
     pairing the amendment mandates ("qgroups false must pair with
     enabled=null/mode=null").
   Each record now has exactly the four keys `devices`, `qgroups`,
   `qgroups_enabled`, `qgroups_mode`.
2. **Fixture source resolution re-stated to the amendment's rule** — "lookup RAW
   decoded source in `device_links`; use its mapped basename when present,
   otherwise `basename(source)`". The raw source is `/dev/dm-3`;
   `device_links["/dev/dm-3"] == "dm-3"`. The fixture is unchanged here and
   satisfies both the amendment's raw-source rule and the original contract's
   `realpath(mount_source)`-basename rule, because `/dev/dm-3` is its own
   realpath.
3. **Device-check rule re-stated to the amendment's** — "Btrfs skips equality
   only when stat major is 0; nonzero btrfs stat major mismatching the mount →
   `device_mismatch`". This path's `st_dev` is `0:57`, i.e. stat major `0`, so
   the equality check is skipped and the btrfs subvolume `st_dev` difference
   (mount `0:44`) is not a `device_mismatch` verdict. The fixture is unchanged
   here; the original `0:57` already sat in the stat-major-0 regime.
4. **Mount-resolution wording re-stated** — the trailing empty line is ignored
   per "ignore empty trailing lines", and the case records explicitly that no
   covering mount point occurs twice, so the amendment's `ambiguous_overmount`
   refusal does **not** apply. The four mountinfo lines are unchanged.
5. **Basis vocabulary** — the original table's `btrfs_qgroups_dir_present` /
   `btrfs_qgroups_dir_absent` are superseded by the amendment's
   `btrfs_qgroups_enabled` / `btrfs_qgroups_disabled` /
   `btrfs_qgroups_enabled_unavailable` / `btrfs_qgroups_dir_absent`. **This
   case's expected basis is `btrfs_device_unmapped`, which the amendment leaves
   untouched** ("Zero/multiple UUID matches remains unknown"), so the six-field
   expected object is unchanged:
   `exit 2`, `QUOTA_STATE_UNKNOWN`, one path
   `{path /srv/data/store, fstype btrfs, mount_point /srv/data, quota_state
   unknown, enforcement n/a, basis btrfs_device_unmapped}`.
   The rationale no longer cites the two superseded basis tokens as live rows.

### The other three amendment retokens, and why they do not touch this case

- "update enabled btrfs basis to `btrfs_qgroups_enabled`" — this case's btrfs
  path is **not** enabled; the device→uuid mapping is ambiguous, so the
  claimant rows are never reached. The token is quoted in the rationale only
  to explain which row *would* have applied had the mapping been unambiguous.
- "ext positive cases become unknown/n/a/`ext_quota_option_unverified`" — this
  case has no ext2/3/4 path. No ext fixture is touched by this seat.
- "duplicated-covering-point case becomes unknown/null fstype+mountpoint/
  `ambiguous_overmount`" — this case has **no duplicated covering mount
  point** (each of `/proc`, `/`, `/tmp`, `/srv/data` occurs exactly once), so
  `ambiguous_overmount` does not apply. Verified programmatically over the
  mountinfo text; the assertion is recorded in the rationale so a reviewer can
  see the case is not silently in that class.

### Corrected derivation (short)

Realpath `/srv/data/store` → candidate mount points `/` (the `/@root` btrfs
line) and `/srv/data` (the `/@data` btrfs line); longest wins → **mount_point
`/srv/data`**, fstype `btrfs`, source `/dev/dm-3`, mount major:minor `0:44`.
Device check: fstype btrfs and stat major `0` → equality skipped, not
`device_mismatch` (S081: `fs/btrfs/inode.c:8246`
`stat->dev = BTRFS_I(inode)->root->anon_dev;`). Source resolution: raw source
`/dev/dm-3` → `device_links` → basename `dm-3`; **two** uuids list `dm-3` in
their `devices` arrays (both with `qgroups: true`, `qgroups_enabled: true`) →
the several-claimants row → `quota_state unknown`, `enforcement n/a`,
`basis btrfs_device_unmapped`. Verdict precedence: no setup error, no enabled
path, one unknown path → **exit 2, `QUOTA_STATE_UNKNOWN`**.

### Why both claimants still agree on qgroups

The amendment adds an `enabled` dimension but does not change the
several-claimants condition, and the filter-vs-count ambiguity I raised as A2
in the original report is still not resolved by the amendment text. Keeping
both claimants at `qgroups: true` / `qgroups_enabled: true` therefore remains
the choice that makes the expectation `unknown` hold under **every** reading
of the exactly-one rows: with two claimants, neither "exactly one uuid whose
qgroups is true" nor "exactly one uuid, qgroups false" can be satisfied, and
the ambiguity preempts any per-claimant `enabled` classification. A
disagreeing-claimant variant (one `qgroups_enabled: true`, one `false`) would
be sensitive to A2 and needs the contract owner's reading pinned before it can
be sealed; I have not authored it.

### Re-verification of the corrected file (observed)

Structural assertions re-run on `cases-corrected/CaseBtrfsTwoUuids.json`:
JSON parses; case keys exactly `schema, id, scenario, fixture, expected,
rationale, sources`; fixture keys exactly `schema, mountinfo, paths,
device_links, btrfs_sysfs`; every `btrfs_sysfs` record has exactly
`devices, qgroups, qgroups_enabled, qgroups_mode` with `qgroups` a bool,
`qgroups_enabled` bool-or-null, `qgroups_mode` str-or-null; every
`qgroups: false` record pairs with `qgroups_enabled: null` and
`qgroups_mode: null`; UUID keys canonical; `devices` and `device_links` values
plain nonempty basenames with no slash or control characters; paths nonempty,
unique, absolute and normalized (no `.`/`..` components); `st_dev` canonical
decimal `MAJ:MIN` with no sign and no leading zeros; every mountinfo line has
≥10 fields and a `-` separator and contains no backslash escape outside
`\040 \011 \012 \134`; no covering mount point is duplicated; mount resolution
selects `/srv/data`; device resolution yields exactly two claimants; the
expected path object has exactly the six contract fields with the contract's
tokens; and the expected object contains no superseded basis token. All
assertions passed.

Report: `.ufo/waves/round-23/build/CaseBtrfsTwoUuids.md`
