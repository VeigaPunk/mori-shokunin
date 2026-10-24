source: S077 https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/admin-guide/xfs.rst (sha256 53bda67b5612a3f2c02820604d05825c9d37addba9855e1d4fba330a516d051c); S078 https://raw.githubusercontent.com/torvalds/linux/v7.2/fs/xfs/xfs_super.c (sha256 0a95697dcfcdab8f7ab6ea26fdb941db952db4b73ed93c30d21e40861ed0450c); S079 https://raw.githubusercontent.com/torvalds/linux/v7.2/fs/btrfs/sysfs.c (sha256 ce146120f29ac29c0bc1859f21e4b84da91a536df2ec9fd2fa5649144f731c43); S080 https://raw.githubusercontent.com/torvalds/linux/v7.2/fs/btrfs/qgroup.c (sha256 121a0af27f9553a9749c837536d618e2ea50d44ce54b30b032fa56e6f3df6ed5); S081 https://raw.githubusercontent.com/torvalds/linux/v7.2/fs/btrfs/inode.c (sha256 01a6ad07c09cd1a05fbccab640c15362c91b57b85faa94c2fd9b9c0128110fdf); S082 https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/filesystems/proc.rst (sha256 e760f716f8278deefab17a63739033cadc7faee93663c49e76455afaaf40d126); S083 https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/admin-guide/ext4.rst (sha256 7929550fa95ed7a0d56cd32c78e3c5f3a598827c4e55f1607097bff2e169dbbd); S084 https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/filesystems/tmpfs.rst (sha256 5ce3dffe9323912b9146a5f33744776ff623ef42cf8accd6b2dfbea0b9db5be6); contract `.ufo/waves/round-23/contract.md` §C2 (frozen at lane commit 4dc80c1be48308075e83af17f15fbfe7e95e6cb8); frozen real control `.ufo/waves/round-23/frozen/c2-expected-real.json`; FR2 boundary `PROVINCE.md:45` and `corpus/README.md:333`; df runway gap `corpus/knowledge/observability-surfaces-r2.md:253-261` and `tools/mori-census.sh:353-357`
verified-at: 2026-10-21 — kernel sources opened and digests recomputed by this seat (bytes streamed, no file written); the eight S-ids are the queued registry rows drafted at `.ufo/waves/round-23/build/DraftSourceRows/rows.md` and are **not yet committed rows** (corpus/SOURCES.md at 4dc80c1 ends at S076), so every S-id below is a forward reference until L1 commits them. The decision table is transcribed from contract §C2 unchanged. **No probe run, no oracle run, no host read was performed by this seat**: `tools/mori-quota-surface.py` does not exist at 4dc80c1, and this note is a DRAFT that L1 verifies after measurement.
recheck: `python3 tools/mori-quota-surface.py --selftest`; `python3 .ufo/waves/round-23/oracle-quota.py --tool tools/mori-quota-surface.py --cases .ufo/waves/round-23/frozen/quota-cases --output <absent-dir>/quota-cases.json --real-expected .ufo/waves/round-23/frozen/c2-expected-real.json`; real control `python3 tools/mori-quota-surface.py` compared against `frozen/c2-expected-real.json`; source recheck — refetch the eight S077–S084 URLs and compare sha256 against the values above.

---

# Quota surface: visible enablement is not exhaustion (DRAFT — round 23, C2)

**This is a draft.** The probe it describes does not exist in the lane yet, the eight source
rows it cites are not yet committed, and the wave-2 falsification has not run. L1 verifies
after measurement; nothing here may be cited as a measured result.

`df` reports **filesystem capacity**. A filesystem quota is a **per-user, per-group or
per-project ceiling**. Those are different quantities, so capacity percentages cannot see a
quota exhaustion (EDQUOT) event: a filesystem at 20 % used can still refuse a write because
one user's quota is full. The lane has already paid for this blind spot in a way it can
document — `tools/mori-census.sh:353-357` carries the standing note that the fleet's reported
disk failures are quota events (EDQUOT) which a capacity-% probe cannot see, and
`corpus/knowledge/audit-r11.md:95-99,168` retains the one first-hand instance the corpus
holds (`printf: write error: Disk quota exceeded`, exit 1, no tally). FR2's boundary
(`PROVINCE.md:45`) is therefore not a preference: `df` capacity percentages cannot detect
quota exhaustion; observe and report only, never change quota state.

Round 23 adds a **standalone read-only probe** that answers a strictly narrower question
than "is this filesystem exhausted?": **for a named path, is a filesystem quota mechanism
visibly enabled, visibly disabled, or unknown?** Visible enablement is a precondition for
exhaustion, not a prediction of it. The probe never calls `quotactl`, `btrfs qgroup`,
`xfs_quota`, `repquota`, `mount`, writes, or any privileged interface.

## 1. What the probe reads, and what it does not

Real-mode inputs are exactly: `/proc/self/mountinfo`; `os.stat(path).st_dev`;
`os.path.realpath(path)`; `os.path.realpath(mount_source)` basename; directory
listings/existence under `/sys/fs/btrfs/*/devices/` and `/sys/fs/btrfs/<uuid>/qgroups`; and
`/sys/fs/btrfs/<uuid>/qgroups/mode` when present. `--fixture FILE` is the synthetic arm and
performs **no host read**; `--path ABS` is repeatable and defaults to the fleet root
`/home/vgpnk/Projects/shokunin` then `/tmp`.

Mountinfo lines are parsed per **S082** (proc.rst §3.5): fields 1–6, then an arbitrary number
of optional `tag[:value]` fields, then the separator, then filesystem type, mount source and
super options (proc.rst:1973-1983; "Parsers should ignore all unrecognised optional fields",
1985). Field 3 (`major:minor`) is documented as "value of st_dev for files on filesystem"
(1975) — the comparison the `device_check` column performs.

Output is one JSON object, schema `mori-quota-surface-v1`: `finding_id`, `exit_code`, `paths`
(each with `path`, `fstype`, `mount_point`, `quota_state`, `enforcement`, `basis`,
`device_check`, `quota_option_keys`, `btrfs_qgroups_mode`), `df_covers_quota: false`, and a
fixed `limits` text. `fstype`/`mount_point` are null when no covering mount exists.
`quota_option_keys` carries sorted quota-related **keys only** — never option values, never
other options, and never mount sources or file names taken from an option value.

Verdict precedence: setup error → exit 2 `QUOTA_SETUP` (no partial verdict); else any path
`enabled` → exit 1 `QUOTA_ENABLED`; else any path `unknown` → exit 2 `QUOTA_STATE_UNKNOWN`;
else exit 0 `QUOTA_DISABLED`. **Positive evidence is never hidden by an unknown sibling**, and
`QUOTA_ENABLED` is a runway-reporting finding, not a failure claim.

## 2. Decision table (mirrors contract §C2 verbatim)

Super options are the last mountinfo field, comma-split; the key is the text before `=`.

| fstype | condition | quota_state | enforcement | basis |
|---|---|---|---|---|
| xfs | `noquota` and no quota key | disabled | n/a | `xfs_noquota_option` |
| xfs | any of usrquota,uquota,quota,grpquota,gquota,prjquota,pquota and no `noquota` | enabled | enforced | `xfs_quota_option` |
| xfs | only *noenforce keys (uqnoenforce,gqnoenforce,pqnoenforce,qnoenforce), no `noquota` | enabled | accounting_only | `xfs_quota_option` |
| xfs | `noquota` together with any quota key | unknown | n/a | `xfs_conflicting_quota_options` |
| xfs | neither `noquota` nor any quota key | unknown | n/a | `xfs_quota_options_absent` |
| btrfs | source basename maps to exactly one uuid whose `qgroups` is true | enabled | unknown | `btrfs_qgroups_dir_present` |
| btrfs | … exactly one uuid, `qgroups` false | disabled | n/a | `btrfs_qgroups_dir_absent` |
| btrfs | zero or several uuids list the device | unknown | n/a | `btrfs_device_unmapped` |
| ext2/ext3/ext4 | any of quota,usrquota,grpquota,prjquota,usrjquota,grpjquota | enabled | unknown | `ext_quota_option` |
| ext2/ext3/ext4 | none of them | unknown | n/a | `ext_quota_superblock_unobservable` |
| tmpfs | any of quota,usrquota,grpquota or a key ending `_hardlimit` | enabled | enforced | `tmpfs_quota_option` |
| tmpfs | none of them | disabled | n/a | `tmpfs_quota_options_absent` |
| other | — | unknown | n/a | `unsupported_fstype` |

Mount resolution precedes the table. Candidate mounts are those whose mount point equals the
path's realpath, is `/`, or is a prefix of the realpath followed by `/`; the longest mount
point wins, and among equal mount points the **last** line wins. No candidate → `unknown`,
basis `no_covering_mount`. If the chosen fstype is not btrfs and its major:minor differs from
the path's `st_dev` → `unknown`, basis `device_mismatch`. For btrfs a mismatch is expected
(§3) and is recorded as `device_check: "btrfs_subvolume_skipped"`; equality is
`device_check: "match"`.

### 2.1 What each row rests on

| row | source anchor | what the source actually says |
|---|---|---|
| xfs `noquota` → disabled | **S077** xfs.rst:171-173 | "Forcibly turns off all quota accounting and enforcement within the filesystem." |
| xfs quota families → enabled/enforced | **S077** xfs.rst:175-185 | `uquota/usrquota/uqnoenforce/quota`, `gquota/grpquota/gqnoenforce`, `pquota/prjquota/pqnoenforce` — "accounting enabled, and limits (optionally) enforced" |
| xfs `*noenforce` → accounting_only | **S077** xfs.rst:175,179,183 pairs each enforced name with a noenforce name; **S078** xfs_super.c:238-251 prints `,usrquota` when `XFS_UQUOTA_ENFD` else `,uqnoenforce` when only `XFS_UQUOTA_ACCT` (same pattern for project/group) | the noenforce suffix names accounting **without** enforcement — it is not a disabled quota |
| xfs conflicting options → unknown | **S078** xfs_super.c:253-254 prints `,noquota` only when `!(m_qflags & XFS_ALL_QUOTA_ACCT)`, and 1542-1545 shows `Opt_noquota` clears both the accounting and enforcement flags | a kernel-emitted option string never pairs `noquota` with a quota key; a conflict is therefore a synthetic or remounted state, and the honest reading is `unknown` |
| btrfs qgroups present/absent | **S079** btrfs/sysfs.c:2450-2461 (attribute group, path comment `/sys/fs/btrfs/<uuid>/qgroups/`), 2567-2583 (`btrfs_sysfs_del_qgroups` removes the directory), 2586-2620 (`btrfs_sysfs_add_qgroups` creates it); **S080** btrfs/qgroup.c:441 and 1032 (add call sites), 620, 689 and 1295 (del call sites) | the directory exists while qgroups are initialised and is torn down with them; presence is evidence that quota accounting is on, and its absence does **not** prove quota was never possible |
| btrfs enforcement = unknown | **S079** sysfs.c:2370-2395 (`qgroup_mode_show` prints `qgroup` or `squota`) | the mode attribute reports which accounting mode is active; it does not report that any limit is set or enforced |
| btrfs device mapping | **S079** sysfs.c:2266 (`devices` kobject) and 2155 (device link per device) | `/sys/fs/btrfs/<uuid>/devices/` lists the device names a uuid spans, which is what the source-basename → uuid mapping reads |
| ext option → enabled (contested, see §5) | **S083** ext4.rst:261-265 and 267-271 | `quota, noquota, grpquota, usrquota` and `jqfmt=, usrjquota=, grpjquota=` are the documented names; the page also states the plain options "are ignored by the filesystem" and are used only by quota tools to recognize volumes where quota should be turned on |
| ext no option → unknown | **S083** ext4.rst (absence only) | the ext superblock quota feature is not observable from the mount options, so absence proves nothing |
| tmpfs quota → enabled/enforced | **S084** tmpfs.rst:129-143 | `quota`, `usrquota`, `grpquota` are "User and group quota accounting and enforcement is enabled on the mount"; `usrquota_block_hardlimit`, `usrquota_inode_hardlimit`, `grpquota_block_hardlimit`, `grpquota_inode_hardlimit` set global limits — hence a key-suffix test, not a fixed key list |
| tmpfs no option → disabled | **S084** tmpfs.rst:129-145 | quotas are features "with the following mount options"; 145 states quota options cannot be set or changed on remount, so the mount-time option set is the state surface |

### 2.2 The `*_hardlimit` and `noenforce` distinctions are the point

Two rows above turn on a distinction a fixed key list would erase:

- **XFS `uqnoenforce` is not "quota off".** S077 pairs `usrquota` with `uqnoenforce` in one
  option name, and S078 prints `,uqnoenforce` when only the accounting flag is set. The
  filesystem is accounting; it is not enforcing. Calling that `disabled` would be a false
  green about a mechanism that is running.
- **tmpfs `*_hardlimit` is not one of three fixed keys.** S084 documents four hardlimit keys
  with per-scope names. A key-suffix test (`endswith("_hardlimit")`) is what catches them.

## 3. The btrfs `st_dev` quirk — a mismatch that is not a mismatch

A btrfs path reports a **different device number** from the one its mount advertises, by
design.

- **S082** (proc.rst:1975) documents mountinfo field 3 (`major:minor`) as "value of st_dev for
  files on filesystem". The kernel fills it from the **superblock** device
  (`fs/proc_namespace.c:143-144`, `MAJOR(sb->s_dev)`, an auxiliary read outside the S077–S084
  set and therefore cited here only as corroboration of the mechanism), and `sb->s_dev` is the
  block device.
- **S081** (btrfs/inode.c:8246) sets the per-inode stat device to
  `BTRFS_I(inode)->root->anon_dev` — the subvolume's **anonymous** device. Each btrfs
  subvolume root has its own anonymous device.

So for the same filesystem, mountinfo advertises the block device's major:minor while
`os.stat()` on a path inside a subvolume reports an anonymous major-0 device. A literal
equality test would report `device_mismatch` on every btrfs path — a false alarm that would
turn a healthy, quota-disabled filesystem into `unknown`.

The contract's resolution: for btrfs a mismatch is **expected** and is recorded as
`device_check: "btrfs_subvolume_skipped"`; the classification proceeds on the btrfs rows.
For any non-btrfs fstype the same mismatch is real evidence and yields `unknown` with basis
`device_mismatch`. Equality on btrfs is `device_check: "match"`.

The frozen real control shows both branches at once: the fleet root (`/home`, btrfs subvolume)
is `btrfs_subvolume_skipped`, while `/tmp` (xfs) is `match`
(`.ufo/waves/round-23/frozen/c2-expected-real.json`). Read the quirk as *the btrfs check is
skipped because the comparison is meaningless there*, never as *the btrfs device was
verified*.

## 4. Limits — what this probe cannot see

These bounds are part of the output (`limits`) and of this note, not hedges:

1. **No limits and no usage.** No per-user, per-group or per-project limit or usage value is
   read. The probe reports whether a mechanism is visibly on; it never answers "how full is
   this user's quota". Quota numbers remain unreadable on this host.
2. **No exhaustion, no EDQUOT attribution.** Visible enablement is a precondition for
   exhaustion, not a prediction or an attribution of it. The probe does not detect, date or
   attribute a quota-abort event, and `QUOTA_DISABLED` does not mean "no quota event will
   happen".
3. **No NFS or server-side quota; no overlay/fuse quota.** A server-enforced quota is invisible
   from the client's mount options, and overlay/fuse filesystems are not in the table at all.
4. **btrfs qgroup presence ≠ a limit set.** The directory's presence says accounting is on
   (S079/S080); it says nothing about whether any limit was ever configured, and btrfs
   enforcement stays `unknown` even when the directory is present.
5. **ext superblock quota state is unobservable** without privileged tools; absence of the
   mount options is not evidence of absence of quota.
6. **Races are not excluded.** sysfs and mountinfo are read at one instant; an
   enable/disable/remount between the reads is not excluded. S084 narrows one sub-case
   (tmpfs quota options cannot change on remount), but a fresh mount/umount can still race.
7. **Named paths only.** A verdict covers the paths the run named. The frozen real control's
   own note records that `/dev/shm` (tmpfs `usrquota`) was observed on this host but is
   outside the default paths — a default `QUOTA_DISABLED` run is compatible with an enabled
   quota mount elsewhere on the host. **Never read a default run as "the host has no
   quota".**
8. **Exit 2 is overloaded.** `QUOTA_SETUP` and `QUOTA_STATE_UNKNOWN` share exit code 2;
   consumers must read `finding_id`. The enabled-over-unknown precedence means an unknown
   sibling does not change the exit code, though it stays visible per path.
9. **No privileged interface, ever.** No `quotactl`, `btrfs qgroup`, `xfs_quota`, `repquota`,
   `mount`, or write. Quota state is tsukuroi/operator-owned; mori observes and reports.
10. **Coverage of the oracle is narrower than the output.** The sealed-case oracle asserts
    exit, `finding_id` and the per-path `(path, fstype, mount_point, quota_state, enforcement,
    basis)` tuple only. `device_check`, `quota_option_keys`, `btrfs_qgroups_mode`,
    `df_covers_quota` and `limits` are **not** case-asserted; only the real control names
    `device_check`.

## 5. Contested rows — open objections L1 must settle before this note is admitted

The table above transcribes the frozen contract. Three source-derived objections against it
are recorded here rather than silently resolved, because they bear on whether the probe can
produce a false "enabled":

- **ext `enabled` is contradicted as written.** **S083** (ext4.rst:261-265) states the plain
  quota options "are ignored by the filesystem" and exist so quota tools can "recognize
  volumes where quota should be turned on" — i.e. documented intent, not proof that
  accounting or enforcement is active. The journaled trio (`jqfmt`, `usrjquota`, `grpjquota`)
  is stronger evidence (the filesystem does act on it) but still does not establish
  enablement. `prjquota` is not documented for ext4 at v7.2, and `jqfmt` is documented but
  absent from the contract's trigger list. The critic seat proposes both ext rows return
  `unknown` (basis `ext_quota_option_activation_unobservable` for the option-present arm).
  Until L1 rules, this note records the ext `enabled` row as **contested**; it does not
  defend it.
- **The tmpfs `*_hardlimit`-only arm is under-determined.** **S084** says the hardlimit keys
  "Set global user quota block hard limit" and never says that supplying one alone enables
  accounting or enforcement. A `*_hardlimit`-only mount expecting `enabled`/`enforced` rests
  on kernel implementation behaviour, not on this documentation.
- **Mount selection can hide a positive finding.** The contract's "longest mount point; among
  equal mount points the last line wins" is the probe's own choice — S082 documents no
  selection algorithm or ordering guarantee — and line order is not stack order. An overmount
  can therefore mask an enabled quota on the covering path. A proposed fix uses the mountinfo
  parent chain to identify blocked mounts and a new basis `ambiguous_overmount`. This is
  flagged for L1's seal decision; the note does not adopt it.

## 6. What `df` cannot see — the one-line summary

`df` sees **capacity**; a quota is **entitlement**. Capacity percentages cannot detect
quota exhaustion (FR2), cannot show that accounting is on without enforcement, cannot
distinguish an XFS accounting-only mount from an enforcing one, cannot show a btrfs
subvolume's own anonymous device, and cannot see any per-user limit or usage value at all.
The probe adds exactly one thing `df` does not have: a **named, sourced, per-path statement
of whether a filesystem quota mechanism is visibly enabled, visibly disabled, or unknown** —
with every verdict carrying the basis that produced it.

## 7. Provenance limits of this note

- The decision table is transcribed from contract §C2, which is frozen at lane commit
  `4dc80c1`. It is not an independent re-derivation of the rules.
- S077–S084 are **queued** rows drafted at `.ufo/waves/round-23/build/DraftSourceRows/rows.md`;
  `corpus/SOURCES.md` at `4dc80c1` ends at S076. Until L1 commits them, every S-id here is a
  forward reference and this note's `source:` line names URLs and digests, not admitted
  registry rows.
- The eight source digests in the `source:` line were recomputed by this seat on 2026-10-21
  from the `v7.2` raw URLs (bytes streamed in memory, nothing written to disk). `v7.2` is a
  branch name, not an immutable tag commit; the digest is what pins the bytes.
- The host facts in §3 and §4.7 are **L1's frozen observation** from
  `frozen/c2-expected-real.json`, not a measurement by this seat. This seat performed no
  mountinfo read, no `os.stat`, no sysfs listing, no `/dev/mapper` readlink, no tool
  execution, no oracle run, and no build/test/lint/formatter run.
- No probe result exists yet. `tools/mori-quota-surface.py` is absent at `4dc80c1`; the
  pre-registered "before" state for every sealed case is `capability_absent`.
- Carried debt is unchanged by this note: 4 unallowlisted retention hits, original permission
  control RED 11/12, two historical wave dispositions unknown, baseline acceptance blocked,
  and **no privacy clearance**. Quota configuration remains operator/tsukuroi-owned; this
  probe observes and reports only.
