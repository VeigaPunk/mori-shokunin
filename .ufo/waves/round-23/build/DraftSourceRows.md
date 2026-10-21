# DraftSourceRows — round-23 SOURCES row draft (S077–S084)

Seat: `MadoR22-2.DraftSourceRows-8` (scribe, leaf member — no subagent dispatch).
Scope: draft the eight `corpus/SOURCES.md` registry rows S077–S084 for the kernel v7.2
sources named in the wave-1 scout items, in the exact 11-column contract-v1 shape.

## Behavior (what I produced)

- **Rows file (deliverable):** `.ufo/waves/round-23/build/DraftSourceRows/rows.md` —
  eight rows S077–S084, header copied verbatim from `corpus/SOURCES.md:5`, one row per
  line, `status=queued`, `used-by=—`, `opened=2026-10-21`, `recheck=on-release`.
- **Registry NOT edited.** `corpus/SOURCES.md` is unchanged; registry writes are L1's
  (`MadoR22-2`). Confirmed by reading only.
- **No `|` inside any cell** — enforced programmatically, not by eye.
- No ids S077–S086 exist in `corpus/SOURCES.md` today (grep over the registry table
  returned no match), so S077 is the next unused id and the block is contiguous.

## Gates

No build, test, lint, formatter, selftest, oracle or gate was run, and none is
requested by this seat. The only executable check is a private shape check over the
rows file (column count, id pattern, kind/tier/status enums, date/recheck/used-by
cells, pipe absence) — reported as "ALL OK" for 8 rows; it is a draft-shape check, not
a lane gate, and it is not part of the corpus census.

## Touched surfaces

| path | write | note |
|---|---|---|
| `.ufo/waves/round-23/build/DraftSourceRows/rows.md` | created | the deliverable |
| `.ufo/waves/round-23/build/DraftSourceRows.md` | created | this report |
| `.scratch/round23/DraftSourceRows/` | created | fetched upstream bytes + two helper scripts (untracked; out of every commit) |
| `corpus/SOURCES.md` | **not written** | L1 owns the registry |

No VCS mutation: no `git add/commit/push`, no mutating `jj` command, no branch or
worktree change, no lane index touch.

## Sources opened, and how each anchor was established

Every file was fetched over HTTPS from the pinned tag
`https://raw.githubusercontent.com/torvalds/linux/v7.2/<path>`, hashed with
`sha256sum` over the fetched bytes, and then read at the line ranges below. Digests
are full-length; the row cells carry the 16-hex prefix.

| id | path | full sha256 of fetched bytes |
|---|---|---|
| S077 | `Documentation/admin-guide/xfs.rst` | `53bda67b5612a3f2c02820604d05825c9d37addba9855e1d4fba330a516d051c` |
| S078 | `fs/xfs/xfs_super.c` | `0a95697dcfcdab8f7ab6ea26fdb941db952db4b73ed93c30d21e40861ed0450c` |
| S079 | `fs/btrfs/sysfs.c` | `ce146120f29ac29c0bc1859f21e4b84da91a536df2ec9fd2fa5649144f731c43` |
| S080 | `fs/btrfs/qgroup.c` | `121a0af27f9553a9749c837536d618e2ea50d44ce54b30b032fa56e6f3df6ed5` |
| S081 | `fs/btrfs/inode.c` | `01a6ad07c09cd1a05fbccab640c15362c91b57b85faa94c2fd9b9c0128110fdf` |
| S082 | `Documentation/filesystems/proc.rst` | `e760f716f8278deefab17a63739033cadc7faee93663c49e76455afaaf40d126` |
| S083 | `Documentation/admin-guide/ext4.rst` | `7929550fa95ed7a0d56cd32c78e3c5f3a598827c4e55f1607097bff2e169dbbd` |
| S084 | `Documentation/filesystems/tmpfs.rst` | `5ce3dffe9323912b9146a5f33744776ff623ef42cf8accd6b2dfbea0b9db5be6` |

Located anchors (all re-read at the cited lines, not paraphrased from memory):

- **S077** `xfs.rst` — `noquota` at 171–173; `uquota/usrquota/uqnoenforce/quota` at
  175–177; `gquota/grpquota/gqnoenforce` at 179–181; `pquota/prjquota/pqnoenforce` at
  183–185. Quote (≤25 words): "Forcibly turns off all quota accounting and enforcement
  within the filesystem." (`xfs.rst:172-173`).
- **S078** `xfs_super.c` — `xfs_fs_show_options` at 186–190; emitted quota options
  `usrquota`:239, `uqnoenforce`:241, `prjquota`:244, `pqnoenforce`:246,
  `grpquota`:249, `gqnoenforce`:251, `noquota`:254 (all inside 238–254); accepted
  option names and their flag effects at 1542–1578, including `qnoenforce` registered
  at 168. Quote: `if (!(mp->m_qflags & XFS_ALL_QUOTA_ACCT))` / `seq_puts(m, ",noquota");`
  (253–254).
- **S079** `btrfs/sysfs.c` — `qgroup_enabled_show` 2355–2368, `qgroup_mode_show`
  2370–2395 (mode text `qgroup`/`squota` at 2381–2384), path comment
  `* Path: /sys/fs/btrfs/<uuid>/qgroups/` at 2453, `qgroups_attrs` 2455–2462,
  `btrfs_sysfs_del_qgroups` 2567–2583, `btrfs_sysfs_add_qgroups` 2586–2620.
  Quote: `enabled = fs_info->qgroup_flags & BTRFS_QGROUP_STATUS_FLAG_ON;` (2363).
- **S080** `btrfs/qgroup.c` — `btrfs_read_qgroup_config` 420, `btrfs_sysfs_add_qgroups`
  call 441, `fs_info->qgroup_flags = 0;` 445 (comment 444: "default this to quota off,
  in case no status key is found"), `btrfs_quota_enable` 997, `btrfs_sysfs_add_qgroups`
  call 1032, `BTRFS_QGROUP_STATUS_FLAG_ON` set 1104, `btrfs_sysfs_del_qgroups` calls
  620, 689, 1295. Quote: `/* default this to quota off, in case no status key is found */`
  (444).
- **S081** `btrfs/inode.c` — `btrfs_getattr` 8215–8218, `stat->dev = BTRFS_I(inode)->root->anon_dev;`
  8246. Quote: that assignment line, verbatim.
- **S082** `proc.rst` — section 3.5 heading at 1965; example line 1970; field table
  1973–1983 (`major:minor` 1975, mount point 1977, separator 1980, filesystem type
  1981, mount source 1982, super options 1983); "Parsers should ignore all
  unrecognised optional fields." 1985. Quote: `(m+4) super options: per super block options`
  (1983).
- **S083** `ext4.rst` — `quota, noquota, grpquota, usrquota` at 261–265;
  `jqfmt=<quota type>, usrjquota=<file>, grpjquota=<file>` at 267–271. Quote: "These
  options are ignored by the filesystem. They are used only by quota tools to recognize
  volumes where quota should be turned on." (262–263).
- **S084** `tmpfs.rst` — table header 129, rows `quota` 132, `usrquota` 135,
  `grpquota` 137, `usrquota_block_hardlimit` 139, `usrquota_inode_hardlimit` 140,
  `grpquota_block_hardlimit` 141, `grpquota_inode_hardlimit` 142; table end 143;
  remount sentence 145. Quote: "None of the quota related mount options can be set or
  changed on remount." (145).

## Out of scope (deliberately not done)

- `corpus/SOURCES.md` was not edited; the search-log entry, the `used-by` appends and
  the `mined`/`queued` flips are L1's.
- No `corpus/lessons/round-23.md` Gate text was written — the contract's `## Gate`
  requirement (URL + access date + ≤25-word located quote per new row) is the round
  lesson's; the quotes and locations above are handed over ready to paste.
- No probe implementation, no oracle, no case, no fixture, no selftest.
- No live host reads beyond fetching upstream source files over HTTPS; no
  `quotactl`, `btrfs`, `xfs_quota`, `repquota`, `mount`, or any privileged/mutating
  command; no `/proc/self/mountinfo`, `/sys/fs/btrfs` or `/dev/mapper` inspection
  (those belong to the probe's own runtime and to the frozen C2 real control).
- No tool install was needed or performed. No pacman/`uv`/`npm`/`cargo` action this
  wave; nothing to record in the tooling directive.

## Findings (verbatim source evidence; contract not edited)

These are observations for the L1/judge. They do not modify the frozen contract; the
contract's own wording is quoted so the conflict can be judged against it.

**F-1 — btrfs: directory presence is not "quota enabled".**
Contract §C2: *"btrfs | source basename maps to exactly one uuid whose `qgroups` is
true | enabled | unknown | `btrfs_qgroups_dir_present`"* and the probe reads
`/sys/fs/btrfs/<uuid>/qgroups/mode` "if present". The kernel separates the two facts:
`btrfs_sysfs_add_qgroups()` creates the `qgroups` kobject when a quota root is
scanned (`sysfs.c:2586-2620`, called from `qgroup.c:441` and `qgroup.c:1032`), while
the enabled state is the separate flag `BTRFS_QGROUP_STATUS_FLAG_ON`
(`sysfs.c:2363`) which `qgroup.c:445` explicitly leaves **off** when no status key is
found — comment at `qgroup.c:444`: *"default this to quota off, in case no status key
is found"*. The directory can therefore exist with `enabled` = 0. The authoritative
read is `qgroups/enabled`, not the presence of `qgroups/`. S079/S080 as drafted teach
exactly this separation.

**F-2 — btrfs: `mode` is only meaningful when enabled.**
`qgroup_mode_show()` asserts `btrfs_qgroup_enabled(fs_info)` (`sysfs.c:2378`) and
emits `qgroup` or `squota` (2381–2384). Reading `mode` on a filesystem whose
qgroup status is off is an assert-guarded path, so the contract's "read
`qgroups/mode` if present" is safe only when `enabled` was read first.

**F-3 — xfs: a kernel-emitted super-options string never contains `noquota` together
with a quota key.** `xfs_fs_show_options` prints `noquota` only when
`!(mp->m_qflags & XFS_ALL_QUOTA_ACCT)` (`xfs_super.c:253-254`), and the per-scope
options are printed only from the accounting/enforcement flags (238–251). So the
contract's conflicting-options row — *"xfs | `noquota` together with any quota key |
unknown | n/a | `xfs_conflicting_quota_options`"* — cannot be produced by a real XFS
mount's mountinfo super options; it is reachable only from a synthetic fixture. Case
authors should not derive it from an observed host.

**F-4 — xfs: the kernel emits `usrquota`/`grpquota`/`prjquota`, never `uquota`,
`quota`, `gquota` or `pquota`.** Contract §C2 lists the xfs quota-key set as
"usrquota,uquota,quota,grpquota,gquota,prjquota,pquota". `xfs_super.c:238-254` emits
only `usrquota`, `uqnoenforce`, `prjquota`, `pqnoenforce`, `grpquota`, `gqnoenforce`,
`noquota`; `uquota`/`quota`/`gquota`/`pquota` exist only as *accepted* mount-option
spellings (1547–1573) that map onto the same flags. The contract's list is a superset,
so it is safe for key matching, but a fixture that asserts `quota` as an emitted key
would not match a real mount.

**F-5 — ext4: the option names the contract keys on are, per the doc, ignored by the
filesystem.** Contract §C2: *"ext2/ext3/ext4 | any of quota,usrquota,grpquota,
prjquota,usrjquota,grpjquota | enabled | unknown | `ext_quota_option`"*.
`ext4.rst:261-265` says the opposite about their meaning: *"These options are ignored
by the filesystem. They are used only by quota tools to recognize volumes where quota
should be turned on."* The doc also never mentions `prjquota` (zero hits in
`ext4.rst`; `prjquota` exists only in `fs/ext4/super.c:1804`). The contract's own
limits section already says "ext quota feature in the superblock is unobservable
without privileged tools"; the doc strengthens that: the *option* is not filesystem
state either, so `quota_state: enabled` derived from an ext4 option key is a
statement about intent, not about the filesystem. S083 is drafted to say so.

**F-6 — tmpfs: the kernel prints `usrquota`/`grpquota` and the hardlimit keys, never a
bare `quota`.** `mm/shmem.c:4878-4893` (`shmem_show_options`) prints `,usrquota`,
`,grpquota` only when `sb_has_quota_active(...)`, and prints the four hardlimit
options with values (`usrquota_block_hardlimit=…`). The contract's tmpfs key set
("quota,usrquota,grpquota or a key ending `_hardlimit`") is again a superset; keys are
text before `=`, so `usrquota_block_hardlimit` matches the `_hardlimit` suffix rule
while its value is not echoed.

**F-7 — mountinfo octal-escape decoding is not covered by S082.**
Contract §C2 requires decoding `\040`, `\011`, `\012`, `\134` in the mount point.
`proc.rst` §3.5 (1965–1990) documents the field layout but says nothing about
escaping. The escaping is in `fs/proc_namespace.c:151` (`seq_path_root(m, &mnt_path,
&p->root, " \t\n\\")`) and `fs/seq_file.c:441-459` (`mangle_path`, "replacing each
occurrence of character from @esc with usual octal escape"). Neither file is among the
eight scout sources, so **no row in S077–S084 backs the octal-decode rule**; the
escape set the kernel applies is exactly `" \t\n\\"` → `\040 \011 \012 \134`, matching
the contract's list. If the rule is to be source-backed, a ninth row for
`fs/proc_namespace.c` (or `fs/seq_file.c`) is the gap. Flagged, not fixed.

**F-8 — device→uuid mapping is consistent with the fixture.** `sysfs.c:2266` creates
the `devices` kobject under `<uuid>` and `sysfs.c:2155` links each device by its
disk-kobject name (`sysfs_create_link(devices_kobj, disk_kobj, disk_kobj->name)`),
i.e. entries look like `dm-0`. The frozen C2 fixture's `"devices":["dm-0"]` and
`/dev/mapper/root → dm-0` shape match this.

**F-9 — `st_dev` vs mountinfo `major:minor` for btrfs.** `inode.c:8246` sets
`stat->dev = BTRFS_I(inode)->root->anon_dev` — the per-subvolume root's anonymous
device, allocated per root in `fs/btrfs/disk-io.c:1093-1101` (`get_anon_bdev(&root->anon_dev)`),
not the superblock device. So the contract's btrfs "mismatch is expected" rule is
correctly grounded in S081; note the allocation site lives in `disk-io.c`, which is not
among the eight rows, so S081 as scoped covers the *read* side (inode.c) only.

## Contract-id alignment

The eight sources, in scout-item order, map to the contract's own S-id hints: the
contract names *"S077–S084"* as the probe's source set and cites *"S081"* for the
per-subvolume anonymous `st_dev` — which is `fs/btrfs/inode.c` in this ordering
(S077 xfs.rst, S078 xfs_super.c, S079 btrfs/sysfs.c, S080 btrfs/qgroup.c, S081
btrfs/inode.c, S082 proc.rst, S083 ext4.rst, S084 tmpfs.rst). That ordering is
therefore the one the contract already assumes, and it is preserved here.

## Known limits of this seat's work

- The rows are **drafts**. Nothing was admitted to the registry, no `mined` status was
  claimed, and `used-by` is `—` for all eight; the round lesson's `## Gate` still has
  to record URL, access date and a ≤25-word located quote per row (the quotes and
  locations are in this report).
- Anchor line numbers are line numbers **in the fetched v7.2 files as fetched on
  2026-10-21** (digests above). A v7.2 tag is immutable, but a re-fetch must be
  digest-checked before the anchors are trusted again.
- Tier assignments are scoped proposals (`tier` is scoped to `scope` per
  `CORPUS.md`, not global truth): all eight are tier A *for their stated scope*
  (official kernel documentation or kernel source at a pinned tag). F-5 argues that
  the ext4 row's scope must stay narrow, which the drafted scope already does.
- The `## Findings` section is source reading only. It is not a verdict on the
  contract's rules, which are frozen; F-1 through F-7 are inputs for the L1 and for
  the wave-2 falsification, not changes.

## Registry change receipt — used-by append (continuation seat, 2026-10-21)

L1 (`MadoR22-2`) assigned this seat one permitted registry change: append
`corpus/knowledge/quota-surface-r23.md` to the `used-by` cell of rows S077–S086,
preserving every other byte and cell of every row (older rows included). The parent
confirmed it would not touch `corpus/SOURCES.md` until this finished.

**Change made — one `edit` call per row, 10 edits total, each anchored on a unique
per-row `teaches` cell tail plus the `mined | 2026-10-21 | on-release |` cells.**

| row | `used-by` before | `used-by` after |
|---|---|---|
| S077 | `corpus/lessons/round-23.md` | `corpus/lessons/round-23.md, corpus/knowledge/quota-surface-r23.md` |
| S078 | `corpus/lessons/round-23.md` | `corpus/lessons/round-23.md, corpus/knowledge/quota-surface-r23.md` |
| S079 | `corpus/lessons/round-23.md` | `corpus/lessons/round-23.md, corpus/knowledge/quota-surface-r23.md` |
| S080 | `corpus/lessons/round-23.md` | `corpus/lessons/round-23.md, corpus/knowledge/quota-surface-r23.md` |
| S081 | `corpus/lessons/round-23.md` | `corpus/lessons/round-23.md, corpus/knowledge/quota-surface-r23.md` |
| S082 | `corpus/lessons/round-23.md` | `corpus/lessons/round-23.md, corpus/knowledge/quota-surface-r23.md` |
| S083 | `corpus/lessons/round-23.md` | `corpus/lessons/round-23.md, corpus/knowledge/quota-surface-r23.md` |
| S084 | `corpus/lessons/round-23.md` | `corpus/lessons/round-23.md, corpus/knowledge/quota-surface-r23.md` |
| S085 | `corpus/lessons/round-23.md` | `corpus/lessons/round-23.md, corpus/knowledge/quota-surface-r23.md` |
| S086 | `corpus/lessons/round-23.md` | `corpus/lessons/round-23.md, corpus/knowledge/quota-surface-r23.md` |

Ordering: the existing entry is kept first and the knowledge path is appended after
it, matching the registry's prevailing `, `-separated convention (21 pre-existing
multi-path cells use `", "`; e.g. `S002`, `S013`).

**Hash receipt** (`corpus/SOURCES.md`, sha256 over file bytes):

- before: `2aa5cbf1fa999cd888b81bc34dd48967e15994a9558f17e47d9793d72e2f526d`
- after: `1f49a4d8338a48f7a85c0614ab24261b5b113d858259e41c30f0f0930ff6ad09`
- line count before 136, after 136 (unchanged; no row added or removed)

**Scope proof.** Reversing only the ten appended substrings
(` | mined | 2026-10-21 | on-release | corpus/lessons/round-23.md, corpus/knowledge/quota-surface-r23.md |`
→ ` | mined | 2026-10-21 | on-release | corpus/lessons/round-23.md |`) reproduces the
pre-edit sha256 exactly, and the byte delta is exactly `10 × 39 = 390` bytes — so no
byte outside the ten `used-by` cells changed. `git diff --stat` shows
`13 insertions(+)` on this file: the ten appended cells plus L1's own three
uncommitted additions (a `## Paths` study-sequence line, the `Bounded search14`
search-log paragraph, and one blank line), none of which this seat wrote.

**Invariants checked after the edit (read-only, from `CORPUS.md:112-149`):**

- rows: 86 (`grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'`)
- malformed rows (NF != 13): 0
- duplicate ids: none
- enum violations / tier inflation: none
- mined rows whose `used-by` paths do not exist: none — the appended path
  `corpus/knowledge/quota-surface-r23.md` exists (7371 bytes) and each of S077–S086
  is literally cited in it (S077×3, S078×3, S079×2, S080×2, S081×1, S082×1, S083×2,
  S084×1, S085×1, S086×4).

**Not done here (L1's):** no `status` cell was changed (all ten rows were already
`mined`), no `recheck` change, no search-log or `## Paths` edit, no lesson edit, no
commit. The parent records the old→new `used-by` change in the round-23 lesson.

No tests, builds, gates, installs or new seats were involved in this continuation.

## Deviations from the stated lane bounds

- One helper script was written to `/tmp` (`/tmp/rows_gen.py`) and deleted
  immediately after use, while the lane rule names
  `TMPDIR=/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch`. No probe output,
  download or artifact was stored under `/tmp`; the second helper script and all
  fetched bytes live under `.scratch/round23/DraftSourceRows/`. Disclosed for the
  record; no other lane or fleet-root write occurred.

## Artifact paths

- Rows draft: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/build/DraftSourceRows/rows.md`
- This report: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/build/DraftSourceRows.md`
- Scratch (fetched bytes, helper scripts): `/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/round23/DraftSourceRows/`
  (`btrfs/`, `xfs_super.c`, `ext4_super.c`, `shmem.c`, `seq_file.c`, `proc_namespace.c`,
  `namespace.c`, `proc.rst`, `gen_rows.py`, `check_rows.py`)
- Registry: `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md` — read-only
  for the row draft; in the continuation seat it received the ten S077–S086 `used-by`
  appends recorded in the receipt section above (no other cell touched).
- Contract read: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/contract.md`
- Contract-v1 authority read: `/home/vgpnk/Projects/shokunin/CORPUS.md:64-149`
