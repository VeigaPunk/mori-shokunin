# ImplQuota — round 23, claim C2: `tools/mori-quota-surface.py`

Seat: `MadoR22-2.ImplQuota-8` (writer executor, leaf; no subagent dispatch).
Lane: `mori-shokunin`, round 23 attempt 1, contract `.ufo/waves/round-23/contract.md`
(frozen at lane commit `4dc80c1be48308075e83af17f15fbfe7e95e6cb8`).
Scope: implement contract §C2 only. Detection and report only. No remediation,
no commit, no push, no config change, no host state change.

## Files

| path | role | bytes | sha256 |
|---|---|---|---|
| `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/build/ImplQuota/mori-quota-surface.py` | deliverable (integration source) | 45348 | `6b55315446e2e42288337b16ba57783fd3dfa73c07e929014c6f146e6c50926a` |
| `/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/round23/ImplQuota/tools/mori-quota-surface.py` | working copy in the seat's isolated clone | 45348 | identical sha256 |
| `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/build/ImplQuota.md` | this report | — | — |

The seat clone was created as the contract bounds require:
`git clone --no-hardlinks /home/vgpnk/Projects/shokunin/mori-shokunin
/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/round23/ImplQuota`.
No VCS mutation was performed in the lane (no `git add`/`commit`/`push`, no
mutating `jj`). The deliverable is byte-identical in both locations so the L1
can land it as `tools/mori-quota-surface.py` unchanged.

Language: Python 3, standard library only (`argparse`, `json`, `os`, `re`,
`subprocess`, `sys`, `tempfile`, `pathlib`). No third-party dependency, so no
install was required this wave — **no tool, version, channel or reason to
record** (tooling directive: nothing installed, nothing upgraded, no pacman
transaction attempted; the host-wide pacman pause was respected).

## What the probe does

A read-only quota-surface probe. `df` capacity percentages cannot see quota
exhaustion (FR2: the fleet's reported disk failures are EDQUOT events), so the
probe reports, per path, whether a filesystem quota mechanism is *visibly*
enabled, visibly disabled, or unknown. It never calls `quotactl`,
`btrfs qgroup`, `xfs_quota`, `repquota`, mounts, writes, or any privileged or
mutating interface, and it reads no credential, token or session material.

Real-mode inputs are exactly the contract's set: `/proc/self/mountinfo`,
`os.stat(path).st_dev`, `os.path.realpath(path)`,
`os.path.realpath(mount_source)` basename, directory listings/existence under
`/sys/fs/btrfs/*/devices/` and `/sys/fs/btrfs/<uuid>/qgroups`, and the text of
`/sys/fs/btrfs/<uuid>/qgroups/mode` when that file exists. Fixture mode opens
the fixture file and nothing else on the host.

## Contract clause → implementation map

| contract clause | implementation (deliverable line numbers) |
|---|---|
| CLI `--path ABS` repeatable, default fleet root then `/tmp` | `parse_args` (591–599), `main` default list (1363–1368); `DEFAULT_PATHS` (100–101) |
| CLI `--fixture FILE` synthetic mode, no host reads | `probe_fixture` (465–474) → `load_fixture` (476–548); fixture mode calls neither `real_inputs` nor `scan_btrfs_sysfs` |
| CLI `--selftest` | `selftest` (636–1348) |
| unknown arguments / relative path / `--fixture` with `--path` → exit 2 `QUOTA_SETUP` | `Parser.error`/`Parser.exit` → `Invalid("usage")` (583–589), `main` guards (1351–1374) |
| fixture format `mori-quota-fixture-v1`, exact top-level keys | `FIXTURE_KEYS` (115–117), key-set check (485) |
| setup triggers: missing/extra top-level keys, non-absolute paths, malformed `st_dev`, malformed JSON, unparseable mountinfo line | (485), (497–508), (512), (477–483), (202–231) |
| mountinfo parsing per proc.rst §3.5 (fields 1–6, optional fields to `-`, fstype, source, super options) | `parse_mountinfo` (202–231) |
| octal escapes `\040 \011 \012 \134` in the mount point | `unescape_mount_point` (184–199), `OCTAL_ESCAPES` (132) |
| candidate mounts: equal to realpath, `/`, or realpath under mount point + `/` | `select_mount` (303–321) |
| longest mount point wins; equal mount points → last line | `select_mount` (313–319) |
| no covering mount → `unknown` / `no_covering_mount` | `evaluate` (330–340) |
| non-btrfs major:minor ≠ `st_dev` → `unknown` / `device_mismatch` | `evaluate` (347–355) |
| btrfs mismatch → `device_check: "btrfs_subvolume_skipped"`; equal → `"match"` | `evaluate` (344–346) |
| quota classification table (xfs 5 rows, btrfs 3 rows, ext 2 rows, tmpfs 2 rows, other) | `classify` (272–301), key sets (119–129) |
| super options = last mountinfo field, comma-split, key = text before `=` | `option_keys` (233–244) |
| output: `mori-quota-surface-v1`, `finding_id`, `exit_code`, `paths[…]`, `df_covers_quota: false`, `limits` | `payload` (550–559) |
| path row keys: path, fstype, mount_point, quota_state, enforcement, basis, device_check, quota_option_keys, btrfs_qgroups_mode | `evaluate` (324–368) |
| `fstype`/`mount_point` null when no covering mount | `evaluate` (326–329) |
| `quota_option_keys` = sorted quota-related keys only, never values or other options | `quota_option_keys` (246–258) |
| `btrfs_qgroups_mode` = mode text or null | `evaluate` (357–361) |
| verdict precedence: setup → 2; any enabled → 1 `QUOTA_ENABLED`; else any unknown → 2 `QUOTA_STATE_UNKNOWN`; else 0 `QUOTA_DISABLED` | `verdict` (370–377), `main` (1351–1376) |
| never echo mount sources, other options or option values | no output field carries a source or a non-quota option; `option_keys` keeps keys only |

### Selftest arms (33 arms, all fixture mode, no host state)

Every arm builds a synthetic fixture under a fresh `mkdtemp` tree, runs this
CLI as a real subprocess, and asserts exit code, `finding_id`, `schema`,
`df_covers_quota`, stderr emptiness and the per-path identity
(`path`, `fstype`, `mount_point`, `quota_state`, `enforcement`, `basis`).

* Verdict-class arms — `QUOTA_ENABLED`: `xfs-usrquota`, `xfs-accounting-only`,
  `ext4-usrquota`, `tmpfs-usrquota`, `tmpfs-hardlimit`,
  `btrfs-qgroups-present`, `btrfs-device-match`, `enabled-plus-unknown`
  (precedence: enabled over an unknown sibling), `escaped-mount-point`,
  `optional-mountinfo-fields`, `symlink-resolved-path`,
  `longest-mount-point-wins`, `last-line-wins-on-tie`.
* `QUOTA_STATE_UNKNOWN`: `xfs-options-absent`, `xfs-conflicting-options`,
  `ext4-options-absent`, `btrfs-device-unmapped`, `btrfs-two-uuids`,
  `unsupported-fstype`, `no-covering-mount`, `xfs-device-mismatch`.
* `QUOTA_DISABLED`: `xfs-noquota`, `btrfs-qgroups-absent`,
  `tmpfs-options-absent`, `last-line-wins-on-tie`.
* Setup arms (`QUOTA_SETUP`, empty `paths`, no partial verdict):
  `setup-malformed-st-dev`, `setup-relative-path`,
  `setup-extra-top-level-key`, `setup-missing-top-level-key`,
  `setup-unparseable-mountinfo`, `setup-malformed-json`,
  `setup-unknown-argument`, `setup-relative-path-argument`,
  `setup-fixture-with-path`, `setup-selftest-with-path`.

No arm invokes real mode, so no arm reads `/proc/self/mountinfo`,
`/sys/fs/btrfs` or any probed path: fixture mode opens the fixture file only.

## Contract ambiguities found, and the resolution used

These are the places where the contract text admits more than one reading.
Each is resolved literally where the contract is explicit and, otherwise, in
the reading that keeps every contract row reachable and mutually exclusive.
Wave-2 falsification and the oracle author should treat these as the places
where a divergence is most likely to appear.

1. **"quota key" in the xfs rows 1 and 4.** The table names the enabling set
   explicitly in row 2 (`usrquota,uquota,quota,grpquota,gquota,prjquota,pquota`)
   and separates the `*noenforce` keys in row 3. I read "quota key" as the
   row-2 set. Consequence: `noquota` + `uqnoenforce` → `disabled` /
   `xfs_noquota_option` (row 1); `noquota` + any row-2 key → `unknown` /
   `xfs_conflicting_quota_options` (row 4). The alternative reading (noenforce
   keys count as quota keys) would move `noquota`+noenforce to the conflict
   row. Only a fixture carrying `noquota` together with a noenforce key can
   distinguish the two readings.
2. **Enforcement precedence for xfs.** Row 2 (a quota key present, no
   `noquota`) → `enforced`; row 3 (only noenforce keys) → `accounting_only`.
   A fixture with both `usrquota` and `uqnoenforce` therefore reports
   `enforced` (row 2), not `accounting_only`.
3. **`device_check` token for a non-btrfs device mismatch** — the contract
   names `match` and `btrfs_subvolume_skipped` only. I emit `mismatch`.
   The compared per-path field set (path, fstype, mount_point, quota_state,
   enforcement, basis) does not include `device_check`, so this is a
   documentation-only token.
4. **`device_check` token when no covering mount** — not named by the
   contract. I emit `not_checked`. Same field-set note as (3).
5. **`limits` shape.** The contract says "fixed boundary text". I emit a
   JSON array of six fixed strings, identical in every output (normal and
   setup), covering: no per-user/group/project limit or usage reading; no
   NFS/server-side and no overlay/fuse quota; btrfs qgroup presence ≠ a limit
   being set; ext quota feature in the superblock unobservable without
   privileged tools; sysfs/mountinfo races during enable/disable/remount not
   excluded; `df` percentages never cover quota exhaustion.
6. **Setup output shape.** A setup error emits the same six top-level keys
   with `paths: []` (no partial verdict) plus one extra key `error` carrying a
   stable reason token (`usage`, `fixture_key_set`, `fixture_schema`,
   `fixture_invalid_json`, `fixture_path_not_absolute`,
   `fixture_st_dev_malformed`, `mountinfo_line_unparseable`,
   `mountinfo_unreadable`, `path_stat_failed`, `path_not_absolute`,
   `input_unavailable`). The normal output carries exactly the contract's six
   keys and no `error` key.
7. **Which option field is classified.** The contract says "super options =
   last mountinfo field". Classification and `quota_option_keys` therefore use
   only the super-options field; the mount-options field (field 6) is not
   consulted. This matters for any fixture that places a quota key in field 6
   instead of the last field: such a fixture is classified as if the key were
   absent.
8. **`--selftest` combined with another flag** → usage / `QUOTA_SETUP`
   (exit 2). The contract lists the three modes but does not state the
   combination rule.
9. **Relative `--fixture FILE`** is accepted; only `--path` must be absolute
   (the contract annotates `--path ABS` and not `--fixture FILE`). A relative
   fixture path is not a "relative path" in the usage-error sense.
10. **Nested fixture key sets.** The exact-key rule is stated for top-level
    keys only. A path entry must carry `path`, `realpath` and `st_dev`; a
    `btrfs_sysfs` entry must carry `devices`, `qgroups` and `qgroups_mode`.
    Extra *nested* keys are ignored; a missing nested key is a setup error
    (the data cannot be classified).
11. **`btrfs_qgroups_mode` attribution.** The mode is reported only when
    exactly one uuid lists the mount's device; with zero or several uuids the
    mode is `null` (the device is not attributable to one uuid).
12. **tmpfs `*_hardlimit` keys** are quota-related and therefore appear in
    `quota_option_keys` (key only, never the value).
13. **Real mode, unreadable probed path** → `path_stat_failed` setup error,
    no partial verdict. The contract does not name this case.
14. **Empty fixture `paths` list** → no enabled and no unknown path → exit 0
    `QUOTA_DISABLED`. The contract does not name this case.

## Relationship to the frozen real control (`frozen/c2-expected-real.json`)

Static derivation from the frozen observation, **not a measurement** — the
tool was not executed against the host in this wave:

* fleet root `/home/vgpnk/Projects/shokunin` → mount `/home`, fstype `btrfs`,
  source `/dev/mapper/root` → resolved basename `dm-0`, which is the single
  uuid's device; that uuid has no `qgroups` directory → `disabled`,
  `btrfs_qgroups_dir_absent`; the mount's `0:30` differs from the path's
  `st_dev` `0:57` → `device_check: "btrfs_subvolume_skipped"`; the path is
  reported as given, not resolved.
* `/tmp` → mount `/tmp`, fstype `xfs`, super options carry `noquota` and no
  quota key → `disabled`, `xfs_noquota_option`; `259:1` equals the path's
  `st_dev` → `device_check: "match"`.
* Both paths disabled → exit 0, `finding_id` `QUOTA_DISABLED`, matching the
  frozen real control. This is a derivation from the contract's rules against
  the frozen observation; the L1's post-integration measurement is the
  authority, and a later differing run is a drift observation.

## Evidence and verification actually performed

* Static parse of the deliverable: `ast.parse` of
  `tools/mori-quota-surface.py` → `PARSE_OK` (1376 lines). This parses the
  file; it does not execute the module.
* Static name-resolution sweep over the AST (module-level definitions,
  imports, assignments, arguments, comprehension targets) → no unresolved
  names other than the `__file__` module global; no duplicate top-level
  definitions (30 top-level defs/constants).
* Byte-identity of the two copies of the deliverable (same sha256, shown
  above).

**Not performed, by wave rule and by the assignment's "do not run anything":**
the tool was not executed, `--selftest` was not executed, no real-mode probe
was run, no fixture arm was run, and no mountinfo/sysfs/stat of a probed path
was read. The selftest arms are therefore *unexecuted* in this wave: they are
delivered as written code and are L1-measured after integration. The single
exception disclosed above is the AST parse of my own file, which executes no
project code and touches no host state.

## Independence

I did not open `.ufo/waves/round-23/cases-proposed/` or
`.ufo/waves/round-23/build/OracleQuota/`, and did not read the fixture-case
proposals, the oracle or the case-author reports in `build/`. The
implementation was derived from `contract.md` §C2 and the frozen
`c2-expected-real.json` only. (A repository-wide search for source anchors
printed file names from `.scratch/` and the contract; no case or oracle
content was returned or read.)

## Risks

* The ten ambiguities above are the divergence surface against a sealed
  oracle; items 1, 2, 7 and 9 can change a per-path verdict rather than only
  a documentation token.
* The selftest is unexecuted here. If any arm's expectation is wrong, the
  selftest will report `QUOTA_SELFTEST_FAIL` with the exact arm label rather
  than a wrong verdict, but that failure has not been observed by this seat.
* Real-mode device resolution for btrfs relies on `os.path.realpath` of the
  mount source (which covers the `/dev/mapper/*` → `dm-N` indirection through
  the symlink) and on the sysfs `devices/` listing matching that basename. A
  host where the mount source is not a symlink path would need the same
  basename to appear in `devices/`.
* btrfs subvolume `st_dev` is anonymous by design, so the fleet root's
  `device_check` is `btrfs_subvolume_skipped` rather than `match`; this is
  the contract's stated expectation, not a defect.

## Blockers

None for the assigned scope. The only pending item is the L1's
post-integration measurement (execution of the probe and its selftest), which
this wave forbids.

## Tooling record

No install, no update, no upgrade, no service restart was performed or needed
this wave (standard-library-only implementation; the host-wide pacman pause
was left untouched).

Report: write your scoped findings to .ufo/waves/round-23/build/ImplQuota.md

---

# §2 — v2 candidate (pre-seal amendment), authored after the original v1

Status: v2 authored against `.ufo/waves/round-23/preseal-amendment.md` in full,
including its "Final pre-seal clarifications" section (parent-ID consistency
refusal, preemption output clearing, canonical `btrfs_qgroups_mode` output
spelling with `qgroups_mode` as the fixture input spelling, literal `n/a`
enforcement, amended fixture schema still named v1). The original v1 candidate
is **not altered** and remains the original-rules candidate.

## Files (v2)

| path | role | bytes | sha256 |
|---|---|---|---|
| `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/build/ImplQuota/mori-quota-surface-v2.py` | v2 deliverable | 64833 | `5c8b251d69dd5cb0cd86757179a70bcf7e7ca0f4c1c465d37b1190e66d3728b6` |
| `/fast/scratch/hyaku/mori-r23/ImplQuota/tools/mori-quota-surface-v2.py` | fresh scratch clone working copy | 64833 | identical sha256 |
| `/fast/scratch/hyaku/mori-r23/ImplQuota/archive/mori-quota-surface.v1.py` | byte archive of the v1 candidate | 45348 | `6b55315446e2e42288337b16ba57783fd3dfa73c07e929014c6f146e6c50926a` |
| `/fast/scratch/hyaku/mori-r23/ImplQuota/archive/SHA256SUMS.txt` | archive manifest | — | — |

Scratch handling: the fresh scratch is `/fast/scratch/hyaku/mori-r23/ImplQuota`,
an actual separate `git clone --no-hardlinks` of the lane repository on its own
branch `round23/implquota-v2`, commit `59b043b` ("round23 C2: amended
quota-surface candidate v2 (pre-seal amendment)"), base commit `4dc80c1be48308075e83af17f15fbfe7e95e6cb8`.
The v1 candidate bytes were archived (paths above) before this seat's own old
scratch `/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/round23/ImplQuota`
was removed. No other scratch was touched: sibling round-23 scratch directories
and the r22 scratch (`measure1`, `measure2`, `measure3`, `trial1-fixtures`,
`trial1.json`) are intact. The lane repository's v1 deliverable file is byte
unchanged (same sha256 as §1).

## Every delta v1 → v2

| # | area | v1 | v2 | amendment clause |
|---|---|---|---|---|
| 1 | ext2/ext3/ext4 | `usrquota` → enabled/unknown/`ext_quota_option` | **always** unknown / n/a; a quota-vocabulary key → `ext_quota_option_unverified`, otherwise `ext_quota_superblock_unobservable` | "ext2/3/4: quota_state ALWAYS unknown" (S083) |
| 2 | ext vocabulary | 6 keys | `quota, noquota, usrquota, grpquota, prjquota, usrjquota, grpjquota, jqfmt` | "adds noquota and jqfmt" |
| 3 | btrfs witness | qgroups **directory presence** = enabled | the `qgroups/enabled` attribute (exact 0/1) is the witness; presence alone means initialized | "qgroups directory presence means INITIALIZED, not enabled" (S079, S080) |
| 4 | btrfs bases | `btrfs_qgroups_dir_present` / `btrfs_qgroups_dir_absent` | present+enabled=1 → enabled/unknown/`btrfs_qgroups_enabled`; present+enabled=0 → disabled/n/a/`btrfs_qgroups_disabled`; present+enabled=null → unknown/n/a/`btrfs_qgroups_enabled_unavailable`; absent (successful parent inspection) → disabled/n/a/`btrfs_qgroups_dir_absent` | "Add required fixture member qgroups_enabled" |
| 5 | btrfs mode read | always read `qgroups/mode` | read `enabled` first; read `mode` **only** when enabled is 1; only `qgroup`/`squota` accepted, anything else → null | "never reads mode unless enabled is 1" (S079: mode asserts enabled) |
| 6 | btrfs parent error | n/a | a parent listing error or an uninspectable uuid is **unknown**, never absent/disabled | "A parent sysfs permission/listing error is unknown, NEVER absent/disabled" |
| 7 | duplicate mount point | last mountinfo line wins | a covering mount point occurring more than once is refused: unknown/n/a/`ambiguous_overmount`, fstype null, mount_point null, device_check not_checked | "conservatively handles covering ancestor overmounts" (S082, S085) |
| 8 | parent-ID consistency | not checked | the selected mount must hang under the longest strictly shorter covering mount when its parent id is present in the snapshot; otherwise refused as `ambiguous_overmount`. A parent id absent from the snapshot refuses nothing | "Final pre-seal clarifications" |
| 9 | device mismatch | btrfs mismatch always skipped | mismatch **preempts** the table for every fstype: unknown/n/a/`device_mismatch`, device_check `mismatch`; the btrfs skip applies only when the path's `st_dev` major is 0 | "Device mismatch PREEMPTS the filesystem table" |
| 10 | preempted row contents | quota_option_keys were reported before the device check | every preempted row (no cover, ambiguous mount, device mismatch) carries `quota_option_keys: []` and `btrfs_qgroups_mode: null` | "On no-cover/ambiguous/device-mismatch preemption, quota_option_keys=[] and btrfs_qgroups_mode=null" |
| 11 | xfs conflict | `noquota` + a quota key | `noquota` + **any** quota key **or** any noenforce key → `xfs_conflicting_quota_options` | "conflict(noquota with ANY quota/enforcement or noenforce key)" (S077, S078) |
| 12 | tmpfs keys | any key ending `_hardlimit` | only `quota, usrquota, grpquota` and the four documented hardlimit names; an arbitrary `_hardlimit` suffix is not a quota option | "Arbitrary suffix `_hardlimit` is NOT sufficient" (S084, S086) |
| 13 | quota_option_keys | btrfs/other → [] already | btrfs and unsupported fstype → `[]`; xfs → `noquota` + recognized xfs keys; ext → the ext vocabulary; tmpfs → the seven documented keys; values never emitted | "For unsupported/btrfs fstype quota_option_keys=[]" |
| 14 | mountinfo parsing | separator + the three fields after it; only the mount point decoded | the separator and the **last three fields of each line**, per line, never file-wide; the root, the mount point and the source are octal-decoded; **any other backslash escape is a setup error**; empty trailing lines ignored | "Parse separator and the last THREE fields of EACH chosen line" |
| 15 | fixture paths | absolute only | nonempty, unique, normalized absolute (no empty, `.` or `..` component, no trailing slash) for both `path` and `realpath` | "Paths nonempty, unique, normalized absolute" |
| 16 | fixture st_dev | `MAJ:MIN` | canonical decimal `MAJ:MIN`: no sign, no leading zeros except `0` | "canonical decimal MAJ:MIN" |
| 17 | fixture UUIDs | any string key | canonical hyphenated UUID keys only | "UUID keys canonical UUIDs" |
| 18 | fixture device names | any string | plain nonempty basenames: no slash, no control character, not `.`/`..`, for both the `devices` lists and the `device_links` values | "devices and mapped values plain nonempty basenames" |
| 19 | fixture records | extra keys tolerated | exact record key set `{devices, qgroups, qgroups_enabled, qgroups_mode}`; missing or extra → setup error | "Missing/extra record keys setup" |
| 20 | fixture pairing | n/a | `qgroups` false requires `qgroups_enabled` null and `qgroups_mode` null; any `qgroups_enabled` other than true requires `qgroups_mode` null | "For initialized-but-disabled/unreadable qgroups, fixture qgroups_mode must be null" |
| 21 | fixture source resolution | `device_links[source]` only | the raw decoded source is looked up in `device_links`; the mapped value's basename is used when present, otherwise the basename of the source | "Fixture source resolution" |
| 22 | output spelling | `btrfs_qgroups_mode` | unchanged output spelling `btrfs_qgroups_mode`; the fixture input keeps `qgroups_mode` | "canonical OUTPUT spelling" |
| 23 | enforcement literal | `n/a` | unchanged literal `n/a` | "enforcement uses literal string n/a" |
| 24 | fixture schema name | `mori-quota-fixture-v1` | unchanged name `mori-quota-fixture-v1` with the amended member set (the round is not yet shipped) | "The amended fixture schema remains v1 within this not-yet-shipped round" |
| 25 | output schema token | `mori-quota-surface-v1` | unchanged: the amendment renames no schema token, and the sealed checks verify "schema/exit consistency" | — |
| 26 | selftest | 33 arms | 47 arms (43 fixture arms + 4 CLI arms), including the amended rules: ext always unknown, btrfs enabled/disabled/unavailable, duplicate mount point, parent-ID refusal, parent-ID consistent, parent-ID absent, arbitrary `_hardlimit` ignored, invalid octal escape, non-canonical st_dev, dotdot path, duplicate path, non-canonical UUID, device name with a slash, qgroups pairing, extra/missing record key | — |

## New source rows (S077–S086) and what each backs in v2

| row | backs |
|---|---|
| S077 (XFS options v7.2) | the xfs option vocabulary and that `noquota` turns accounting and enforcement off |
| S078 (xfs_super.c emission) | that `noquota` is printed only with no accounting flags and that `usrquota`/`uqnoenforce` distinguish enforcement from accounting-only; a conflicting synthetic string is probe policy, not a kernel observation |
| S079 (btrfs sysfs.c) | separate `enabled` and `mode` attributes, `enabled` printing 0/1, `mode` printing `qgroup`/`squota`, and that reading `mode` asserts qgroups are enabled |
| S080 (btrfs qgroup.c) | that a quota root can initialize its sysfs directory while the enabled flag stays off: initialized ≠ enabled |
| S081 (btrfs inode.c) | the per-subvolume anonymous `st_dev`, so the btrfs equality skip is required on that path |
| S082 (proc.rst §3.5) | the mountinfo field layout, and that no last-line topology guarantee is taught |
| S083 (ext4.rst) | that plain quota hints are ignored by the filesystem and that neither hints nor journal-replay settings prove runtime accounting enabled |
| S084 (tmpfs.rst) | the tmpfs quota flags and the four documented hardlimit names; hardlimit settings do not justify arbitrary suffix matching |
| S085 (proc_namespace.c) | that mountinfo emits escaped namespace paths and that the field layout is not a safe mount stack ordering rule |
| S086 (shmem.c) | that the tmpfs `usrquota`/`grpquota` tokens test active quota and that only the four named hardlimit keys are emitted |

## Frozen real control under the v2 rules (derivation, not a measurement)

The tool was not executed. Against `frozen/c2-expected-real.json` and the
amendment's note that `/home` is id 65 with parent 33 and `/tmp` is id 244 with
parent 33, root id 33:

* fleet root `/home/vgpnk/Projects/shokunin` → covering mounts `/` (33) and
  `/home` (65), no duplicate point; the parent check compares 33 against the
  longest shorter cover's id 33 → **no refusal**; device 0:30 vs path 0:57 with
  `st_dev` major 0 → `device_check: btrfs_subvolume_skipped`; source
  `/dev/mapper/root` resolves to `dm-0`, the single uuid's device; that uuid has
  no qgroups directory → disabled / n/a / `btrfs_qgroups_dir_absent`; mode null.
* `/tmp` → covering `/` (33) and `/tmp` (244) → parent 33 == 33 → no refusal;
  `259:1` equals the path's `st_dev` → `device_check: match`; super options
  carry `noquota` and no quota key → disabled / n/a / `xfs_noquota_option`.
* Both disabled → exit 0, `QUOTA_DISABLED`.

The frozen real control's expected rows are therefore unchanged by v2.

## v2 ambiguities still open (for the sealed oracle and wave 2)

1. **btrfs equality versus skip.** The amendment says "Btrfs skips equality
   only when stat major is 0" and separately "Equal → match". v2 checks
   equality first: an exactly equal btrfs device reports `match`, and only a
   btrfs *mismatch* with `st_dev` major 0 reports `btrfs_subvolume_skipped`. The
   opposite order would report `btrfs_subvolume_skipped` for an exactly equal
   major-0 device. The frozen real control (0:30 vs 0:57) is unaffected.
2. **Uninspectable btrfs uuid.** A uuid whose qgroups state cannot be read is
   excluded from the device match, so the path reports
   `btrfs_device_unmapped` (unknown). The amendment requires "unknown, never
   absent/disabled" but names no token for this case; no new token was invented.
3. **Mode normalization.** Only `qgroup` and `squota` are accepted, in fixture
   mode as well as real mode; any other text yields null. The kernel prints
   exactly those two values (S079).
4. **UUID case.** Canonical hyphenated layout is required; hexadecimal case is
   accepted in either case because the kernel prints lowercase and no case is
   named by the amendment.
5. **`device_links` key set.** The lookup key is the decoded mount source; the
   mapped value must be a plain basename. A fixture that maps a source to a
   value with a path separator is a setup error.
6. **Fixture `paths` extra keys.** Extra keys inside a path entry are ignored
   (unknown case metadata never enters the output); the three required keys
   must be present.
7. **Enforcement `enforced` semantics** stay the contract's: the flag says a
   quota mechanism flag is set, never that a nonzero limit exists (S077,
   S084, S086).

## Evidence for v2

* Static parse of the v2 candidate: `ast.parse` → `PARSE_OK` (1882 lines),
  plus an AST name-resolution sweep: no unresolved names, no duplicate
  top-level definitions, and no remaining references to the removed v1 helpers
  `select_mount`/`ambiguous_mount`. This parses the file; it does not execute
  the module.
* The v2 candidate is committed on the scratch branch `round23/implquota-v2`
  (commit `59b043b`); the lane tree carries no commit from this seat.

**Not performed, by wave rule and by the assignment:** the v2 tool was not
executed, `--selftest` was not executed, no real-mode probe was run, no host
mountinfo/sysfs/stat of a probed path was read, and neither
`.ufo/waves/round-23/cases-proposed/` nor `.ufo/waves/round-23/build/OracleQuota/`
was opened. The single disclosed execution is the AST parse of this seat's own
file.

## Tooling record (v2)

No install, no update, no upgrade, no service restart; the implementation is
standard-library only. The host-wide pacman pause was left untouched.

---

# §3 — v3 candidate (pre-seal source safety correction), final

Decision applied: the btrfs `qgroups/mode` attribute is **never read in real
mode**. Its show function asserts that qgroups are enabled, so a read inside a
present-but-disabled window can trip a kernel assert on an assert-enabled
kernel, and a quota disable racing the read makes the read unsafe. The
real-mode readset is the `qgroups/enabled` attribute only; `btrfs_qgroups_mode`
is therefore null in real mode. Fixture mode is unchanged: a fixture's
`qgroups_mode` is still projected as `qgroup` or `squota` (anything else null),
so the primary and supplementary fixture targets are unchanged and the default
real control is unchanged.

## Files (v3)

| path | role | bytes | sha256 |
|---|---|---|---|
| `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/build/ImplQuota/mori-quota-surface-v3.py` | **v3 deliverable (final)** | 66279 | `5199e97b5ac89a39b3f047586a6e624d7e95041415390750a93f91bf15d55129` |
| `/fast/scratch/hyaku/mori-r23/ImplQuota/tools/mori-quota-surface-v3.py` | fresh scratch working copy | 66279 | identical sha256 |
| `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/build/ImplQuota/mori-quota-surface-v2.py` | **v2 preserved byte-unchanged as the rejected unsafe-read source evidence** | 64833 | `5c8b251d69dd5cb0cd86757179a70bcf7e7ca0f4c1c465d37b1190e66d3728b6` |
| `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/build/ImplQuota/mori-quota-surface.py` | v1 original, byte-unchanged | 45348 | `6b55315446e2e42288337b16ba57783fd3dfa73c07e929014c6f146e6c50926a` |
| `/fast/scratch/hyaku/mori-r23/ImplQuota/archive/mori-quota-surface.v1.py` | byte archive of v1 | 45348 | as above |
| `/fast/scratch/hyaku/mori-r23/ImplQuota/archive/mori-quota-surface.v2.py` | byte archive of v2 (rejected unsafe-read evidence) | 64833 | as above |
| `/fast/scratch/hyaku/mori-r23/ImplQuota/archive/SHA256SUMS.txt` | archive manifest for v1, v2 and v3 | — | — |

Scratch: the fresh scratch `/fast/scratch/hyaku/mori-r23/ImplQuota` holds two
candidate branches of the same separate clone, base `4dc80c1`:
`round23/implquota-v2` (commit `59b043b`, v2) and `round23/implquota-v3`
(commit `0180a16`, "round23 C2: final quota-surface candidate v3 (no real-mode
qgroups/mode read)", which also commits the v1 and v2 archive bytes). Nothing
else in the lane was touched; this seat's own old scratch was already removed
in §2 after archiving, and sibling and r22 scratch remain intact.

## Delta v2 → v3 (complete)

| # | area | v2 | v3 |
|---|---|---|---|
| 1 | real-mode readset | `qgroups/enabled`, and `qgroups/mode` when enabled reads 1 | `qgroups/enabled` only; the mode attribute is never opened |
| 2 | real-mode `btrfs_qgroups_mode` | `qgroup`/`squota` when enabled read 1 | always null |
| 3 | `scan_btrfs_sysfs` | read `enabled`, then `mode` | read `enabled` only; the record's mode field stays None, with the reason inline |
| 4 | limits | 7 fixed sentences | 8 fixed sentences: the appended sentence is "the btrfs qgroups mode attribute is never read, so btrfs_qgroups_mode is null in real mode" |
| 5 | fixture mode | fixture `qgroups_mode` projected as `qgroup`/`squota` | **unchanged**; the fixture pairing rule (mode null unless `qgroups_enabled` is true) still applies |
| 6 | every other rule | as §2 | **unchanged** (ext always unknown, btrfs enabled gate, duplicate mount point refusal, parent-ID refusal, device-mismatch preemption, preempted-row clearing, xfs precedence, tmpfs key set, strict fixture validation, output minimization) |
| 7 | selftest | 47 arms | 47 arms, unchanged (all fixture mode; the fixture mode projection arm still expects `squota`) |

## Why the change is safe and complete

* The removed read is the only read v2 made of a file whose kernel show
  function can assert. The remaining btrfs reads are directory listings, one
  `os.stat` for the qgroups directory and one read of the `enabled` attribute,
  none of which has an assert path.
* The classification does not lose information: `btrfs_qgroups_enabled`,
  `btrfs_qgroups_disabled`, `btrfs_qgroups_enabled_unavailable` and
  `btrfs_qgroups_dir_absent` are all decided by the `enabled` attribute and
  the directory's existence, never by the mode text.
* The frozen real control is unchanged: the fleet root's uuid has no qgroups
  directory, so the mode is null in any case; `/tmp` is not btrfs.
* The change is confined to the real-mode readset. Fixture projection, the
  six primary fields, the supplementary metadata fields, the exit map and the
  finding ids are untouched, so the sealed primary and supplementary fixture
  targets are unchanged.

## Evidence for v3

* Static parse of the v3 candidate: `ast.parse` → `PARSE_OK` (1907 lines,
  66279 bytes), plus an AST name-resolution sweep: no unresolved names, no
  duplicate top-level definitions.
* Static readset audit: the only string literal `"mode"` in the file is at
  three places — the sysfs record key (always None in real mode), the fixture
  projection (`btrfs_modes(mode)` on the fixture's `qgroups_mode`) and the
  record lookup in `classify_btrfs`. No code path joins `"mode"` into a
  filesystem path, so the attribute cannot be opened.
* No execution: the v3 tool was not executed, `--selftest` was not executed,
  no real-mode probe was run, and neither `cases-proposed/` nor
  `build/OracleQuota/` was opened. The single disclosed execution is the AST
  parse of this seat's own file.

## Candidate selection summary for the L1

| candidate | rules | status |
|---|---|---|
| `mori-quota-surface.py` (v1) | original contract §C2 table, original fixture shape | preserved byte-unchanged; superseded by the pre-seal amendment |
| `mori-quota-surface-v2.py` (v2) | amended rules, but reads `qgroups/mode` in real mode | preserved byte-unchanged as the **rejected unsafe-read source evidence** |
| `mori-quota-surface-v3.py` (v3) | amended rules, real-mode readset = `enabled` only | **final candidate** |

## Tooling record (v3)

No install, no update, no upgrade, no service restart; standard-library only.
The host-wide pacman pause was left untouched.
