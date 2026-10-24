# DraftKnowledge — scoped findings (round 23, C2 knowledge note)

Seat: `MadoR22-2.DraftKnowledge-8` (scribe, leaf — no subagent dispatch).
Authority: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/contract.md`
§C2, frozen at lane commit `4dc80c1be48308075e83af17f15fbfe7e95e6cb8`.

## Files written (this seat's only writes)

| Path | Role |
|---|---|
| `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/build/DraftKnowledge/quota-surface-r23.md` | the deliverable draft knowledge note (20 889 B) |
| `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/build/DraftKnowledge.md` | this report |

No production file was edited: `corpus/SOURCES.md`, `corpus/knowledge/**`, `SKILL.md`,
`PROVINCE.md`, `corpus/README.md` and `tools/**` are byte-unchanged. No candidate
implementation was read (`build/ImplQuota/`, `.scratch/round23/ImplQuota` — the latter does not
exist yet); no proposed case content was read (`cases-proposed/` was listed but not opened).

## What the draft contains

The note opens with the required `source:` / `verified-at:` / `recheck:` trio, then carries:

1. **The provenance trio** naming all eight sources S077–S084 with their full URLs and
   recomputed SHA-256 digests, the contract, the frozen real control, the FR2 boundary
   (`PROVINCE.md:45`, `corpus/README.md:333`), and the df-runway gap
   (`corpus/knowledge/observability-surfaces-r2.md:253-261`, `tools/mori-census.sh:353-357`).
   The `verified-at:` line states that the eight S-ids are **queued rows not yet committed**
   (`corpus/SOURCES.md` at `4dc80c1` ends at S076) and are therefore forward references.
   The `recheck:` line gives the four commands L1 runs after measurement (selftest, sealed
   oracle with `--real-expected`, real control, and a source re-fetch/digest comparison).
2. **The decision table**, transcribed verbatim from contract §C2 (all 13 rows, plus the
   mount-resolution preamble and the `device_check` rules), followed by a **per-row source
   anchor** table naming the S-id and line range behind each row, and a subsection on the two
   distinctions that a naive key list would erase (`*noenforce` ≠ disabled; `*_hardlimit`
   needs a suffix test).
3. **The btrfs `st_dev` quirk** as its own section: mountinfo field 3 is the superblock
   device (`proc.rst:1975`; kernel fills it from `MAJOR(sb->s_dev)`), while a btrfs path's
   stat device is the subvolume's anonymous device (`inode.c:8246`,
   `stat->dev = BTRFS_I(inode)->root->anon_dev`). A literal equality test would fire a false
   `device_mismatch` on every btrfs path; the contract's resolution is
   `device_check: "btrfs_subvolume_skipped"`. The note states explicitly that this means the
   btrfs comparison was **skipped as meaningless**, never that the device was verified.
4. **Ten limits**, including the two that matter most for honest use: no limits/usage values
   are read, and visible enablement is a precondition for exhaustion, not a prediction or
   attribution of one; plus `QUOTA_DISABLED` covering only the named paths (the frozen control's
   own note records `/dev/shm` tmpfs `usrquota` outside the defaults), the overloaded exit 2,
   and the fact that the sealed oracle asserts only exit + `finding_id` + six per-path fields.
5. **A contested-rows section** naming three source-derived objections that L1 must settle
   before the note is admitted — the ext `enabled` row (contradicted by S083's "ignored by the
   filesystem"), the tmpfs `*_hardlimit`-only arm (under-determined by S084), and mount
   selection/overmount ordering (S082 documents no selection algorithm) — each recorded as
   contested rather than silently resolved or silently adopted.
6. **A "what `df` cannot see" section**: capacity versus entitlement; `df` cannot detect
   exhaustion, cannot separate accounting-only from enforcing, cannot show a btrfs
   subvolume's anonymous device, and cannot read any per-user limit or usage value.
7. **A provenance-limits section**: the table is transcribed from the frozen contract, not
   re-derived; the S-ids are forward references; the host facts are L1's frozen observation,
   not a measurement by this seat; no probe result exists yet.

The note is **marked a draft** in three places (header, first paragraph, and the `verified-at:`
line), and states that L1 verifies after measurement.

## Grounding performed (observed by this seat)

The eight kernel sources were opened and their digests recomputed on 2026-10-21. Bytes were
streamed in memory over HTTPS; **nothing was written to disk**, so no scratch path was used.

| id | file | sha256 (full) | key line(s) located |
|---|---|---|---|
| S077 | `Documentation/admin-guide/xfs.rst` | `53bda67b5612a3f2c02820604d05825c9d37addba9855e1d4fba330a516d051c` | 171-173 noquota; 175-177, 179-181, 183-185 the three quota families |
| S078 | `fs/xfs/xfs_super.c` | `0a95697dcfcdab8f7ab6ea26fdb941db952db4b73ed93c30d21e40861ed0450c` | 238-251 enforcement vs accounting emission; 253-254 `noquota`; 1542-1578 option parsing |
| S079 | `fs/btrfs/sysfs.c` | `ce146120f29ac29c0bc1859f21e4b84da91a536df2ec9fd2fa5649144f731c43` | 2355-2368 `qgroup_enabled_show`; 2370-2395 `qgroup_mode_show`; 2450-2461 qgroups attribute group + path comment; 2567-2620 add/del qgroups; 2266 + 2155 `devices` kobject and links |
| S080 | `fs/btrfs/qgroup.c` | `121a0af27f9553a9749c837536d618e2ea50d44ce54b30b032fa56e6f3df6ed5` | 441 and 1032 add call sites; 620, 689, 1295 del call sites |
| S081 | `fs/btrfs/inode.c` | `01a6ad07c09cd1a05fbccab640c15362c91b57b85faa94c2fd9b9c0128110fdf` | 8246 `stat->dev = BTRFS_I(inode)->root->anon_dev;` |
| S082 | `Documentation/filesystems/proc.rst` | `e760f716f8278deefab17a63739033cadc7faee93663c49e76455afaaf40d126` | 1965 §3.5 header; 1973-1983 field table; 1975 major:minor; 1979-1980 optional fields + separator; 1981-1983 fstype/source/super options; 1985 ignore unrecognised optional fields |
| S083 | `Documentation/admin-guide/ext4.rst` | `7929550fa95ed7a0d56cd32c78e3c5f3a598827c4e55f1607097bff2e169dbbd` | 260-265 plain quota group ("ignored by the filesystem"); 266-271 journaled group |
| S084 | `Documentation/filesystems/tmpfs.rst` | `5ce3dffe9323912b9146a5f33744776ff623ef42cf8accd6b2dfbea0b9db5be6` | 129-143 quota options table; 145 mount-time-only note |

All eight digests **match the sibling draft** at
`.ufo/waves/round-23/build/DraftSourceRows/rows.md` byte for byte (same 16-hex prefixes), so
the id→file mapping this note cites is the same mapping the source-row draft uses. The
contract's own citation "per-subvolume anonymous st_dev, S081" is consistent with it.

One auxiliary read outside the S077–S084 set, cited in the draft only as mechanism
corroboration and explicitly labelled as such: `fs/proc_namespace.c:143-144`
(`MAJOR(sb->s_dev)`, `MINOR(sb->s_dev)` — mountinfo field 3 comes from the superblock device)
and `:151` (`seq_path_root(m, &mnt_path, &p->root, " \\t\\n\\\\")` — the escape set the
contract's `\040 \011 \012 \134` rule refers to). S082's own §3.5 text does **not** document
escaping or mount selection; the note therefore does not cite S082 for either.

## Findings

1. **The eight S-ids are not yet admitted rows.** `git show 4dc80c1:corpus/SOURCES.md` has
   76 rows, S001–S076; `corpus/lessons/round-23.md` (the contract's "lesson23 Gate") does not
   exist either. The contract's "sourced: S077–S084" and the note's `source:` trio are forward
   references until L1 commits the rows. The draft handles this by naming URLs + digests and
   stating the status, rather than presenting the rows as admitted. **L1 must land the source
   rows (or amend the trio) before this note can be cited as an admitted knowledge entry.**
2. **The ext `enabled` row is contradicted by its own source.** S083 states the plain ext4
   quota options "are ignored by the filesystem" and exist only so quota tools can recognize
   volumes where quota should be turned on. The contract reads that same option name as
   `enabled`. `prjquota` is not documented for ext4 at v7.2, and the documented `jqfmt` is
   absent from the contract's trigger list. Recorded as contested; L1 rules.
3. **The tmpfs `*_hardlimit`-only arm is under-determined by S084**, which says the keys "Set
   global user quota block hard limit" and never states that supplying one alone enables
   accounting or enforcement. Recorded as contested; L1 rules.
4. **Mount selection is the probe's own choice, not a procfs contract.** S082 documents no
   selection algorithm and no line-order guarantee; "longest mount point, last line wins" is
   the contract's rule, and line order is not stack order, so an overmount can mask an
   enabled quota. Recorded as contested; L1 rules.
5. **`df` blind spot is well attested in-lane, not merely asserted.** `tools/mori-census.sh:
   353-357` carries the standing note that the fleet's disk failures were EDQUOT events a
   capacity-% probe cannot see, and `corpus/knowledge/audit-r11.md:95-99,168` retains one
   first-hand instance (stderr `printf: write error: Disk quota exceeded`, exit 1, no tally).
   The note cites both, so the new capability rests on retained lane evidence rather than on a
   fresh external claim.
6. **`/dev/shm` coexistence must survive into the admitted note.** The frozen real control's
   own note records `/dev/shm` (tmpfs `usrquota`) as observed on this host but outside the
   default paths. A default `QUOTA_DISABLED` run is therefore compatible with an enabled quota
   mount elsewhere; the draft states this explicitly so no later reader can upgrade "disabled
   on the two default paths" into "the host has no quota".
7. **Oracle coverage is narrower than the output.** The sealed oracle asserts exit,
   `finding_id` and `(path, fstype, mount_point, quota_state, enforcement, basis)` only;
   `device_check`, `quota_option_keys`, `btrfs_qgroups_mode`, `df_covers_quota` and `limits`
   are not case-asserted (only the real control names `device_check`). The note records this
   so a later writer cannot claim the whole output is oracle-verified.
8. **Exit 2 is overloaded** (`QUOTA_SETUP` vs `QUOTA_STATE_UNKNOWN`), consistent with the
   lane's existing probe convention; consumers must read `finding_id`.

## Out of scope / not done (by instruction and by lane bounds)

- No probe implementation was written or read; no oracle was run; no case was opened; no
  build, test, lint, formatter or smoke run was performed.
- No live host read was performed: no `/proc/self/mountinfo`, no `os.stat` of the fleet root
  or `/tmp`, no `/dev/mapper/*` readlink, no `/sys/fs/btrfs` listing. My item does not name
  those reads, so I ran none; the host facts in the draft are L1's frozen observation from
  `frozen/c2-expected-real.json`, attributed as such.
- No `corpus/SOURCES.md`, `SKILL.md`, `PROVINCE.md`, `corpus/README.md` or `tools/**` edit.
  The S077–S084 rows, the SKILL registry row, the PROVINCE/Core wording and the README
  frontier row are sibling seats' drafts and L1's to land.
- No VCS mutation in the lane: no `git add`/`commit`/`push`, no mutating `jj` command. Only
  read-only plumbing (`rev-parse`, `show`, `cat-file`) was used.
- No session-transcript read of any kind (this wave permits none).
- No tool install or update: nothing was needed. Python 3 standard library only, plus the
  host's existing HTTPS stack. Channel/reason record: none — no install occurred, so no
  pacman/uv/npx/cargo transaction was run and the host-wide pacman pause was untouched.

## Confidence

- **High**: the decision table's transcription of contract §C2; the source digests and line
  anchors (all eight re-verified here); the btrfs `st_dev` mechanism; the `df` blind-spot
  citations; the "queued, not admitted" status of S077–S084.
- **Medium**: the per-row source-anchor table's mapping of each contract row onto its
  backing S-id — it is my reading of which source backs which row, and L1 may prefer a
  different anchoring for the ext rows given finding 2.
- **Deliberately unresolved**: the three contested rows (§5 of the draft). They are L1's seal
  decisions, not mine; the draft presents the contract table and flags the objections without
  adjudicating them.

Report: .ufo/waves/round-23/build/DraftKnowledge.md
