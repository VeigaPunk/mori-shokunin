# CaseXfsUsrquota — C2 fixture case for an xfs mount with the `usrquota` super option

Seat: `MadoR22-2.CaseXfsUsrquota-8` (fixture-case author). Detection and report only.

Authority: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/contract.md`
(frozen at lane commit `4dc80c1be48308075e83af17f15fbfe7e95e6cb8`), §C2. Sources: S077–S084
row set (`.ufo/waves/round-23/build/DraftSourceRows/rows.md`); the three relied on here are
**S077** (`Documentation/admin-guide/xfs.rst` v7.2), **S078** (`fs/xfs/xfs_super.c` v7.2) and
**S082** (`Documentation/filesystems/proc.rst` v7.2).

## Result

One independent C2 fixture case written to
`/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/cases-proposed/CaseXfsUsrquota.json`
(schema `mori-quota-case-v1`, id `CaseXfsUsrquota`).

Scenario: an xfs mount whose mountinfo super options carry the kernel-emitted token
`usrquota` (user-quota accounting **plus enforcement** on) and no `noquota`, probed at the
mount point itself and at a nested directory beneath it.

Expected verdict, derived from contract §C2 only:

| path | fstype | mount_point | quota_state | enforcement | basis |
|---|---|---|---|---|---|
| `/srv/xfsquota` | `xfs` | `/srv/xfsquota` | `enabled` | `enforced` | `xfs_quota_option` |
| `/srv/xfsquota/projects/data` | `xfs` | `/srv/xfsquota` | `enabled` | `enforced` | `xfs_quota_option` |

Run-level: exit **1**, finding id **`QUOTA_ENABLED`**.

No implementation was read: neither `.ufo/waves/round-23/build/ImplQuota/` nor
`.scratch/round23/ImplQuota`. No host quota probe, no `quotactl`/`xfs_quota`/`repquota`/`mount`,
no privileged command, no build/test/lint run. No tool install or update was performed
(`curl`/`python3` already present; no pacman/uv/npx/cargo transaction).

## Derivation

1. **Fixture shape.** `mori-quota-fixture-v1` with exactly the five contract keys
   `schema`, `mountinfo`, `paths`, `device_links`, `btrfs_sysfs`; each `paths` entry carries
   exactly `path`, `realpath`, `st_dev` in `MAJ:MIN` form; all probed paths absolute.
2. **Mountinfo parse (S082).** `proc.rst` §3.5 (field table lines 1973–1983) fixes the line
   layout: fields 1–6, then zero or more optional `tag[:value]` fields, then the separator,
   then filesystem type, mount source, super options. The fixture's xfs line is
   `31 29 259:2 / /srv/xfsquota rw,relatime shared:7 - xfs /dev/nvme0n1p2 rw,attr2,inode64,logbufs=8,logbsize=32k,usrquota`,
   so mount point `/srv/xfsquota`, fstype `xfs`, mount `major:minor` `259:2`, super options
   `rw,attr2,inode64,logbufs=8,logbsize=32k,usrquota`.
3. **Mount resolution.** Contract §C2: candidates are "mount point equals realpath, or is `/`,
   or realpath starts with mount point + `/`"; the **longest** mount point wins.
   For `/srv/xfsquota` the `/srv/xfsquota` line qualifies by equality and the btrfs root line
   (mount point `/`) qualifies as `/`; longest wins → the xfs line. For
   `/srv/xfsquota/projects/data` the `/srv/xfsquota` line qualifies by the prefix rule and
   again beats `/` → the same xfs line. The btrfs root line is a decoy only; it is never
   selected, so the btrfs rows are unreachable for either probed path.
4. **Device check.** fstype is `xfs`, i.e. not btrfs, and the chosen mount's `major:minor`
   `259:2` equals the paths' `st_dev` `259:2` (S082 line 1975: *major:minor: value of st_dev
   for files on filesystem*). The `device_mismatch` precondition does not fire, so the xfs
   classification table is reached. The btrfs per-subvolume anonymous-`st_dev` exemption
   (contract §C2, citing S081 `fs/btrfs/inode.c` line 8246) is irrelevant to this case.
5. **Quota classification.** Super options are comma-split with the key taken as the text
   before `=`: keys `rw`, `attr2`, `inode64`, `logbufs`, `logbsize`, `usrquota`. The quota key
   `usrquota` is present and `noquota` is absent, which is contract §C2 xfs row 2 →
   `quota_state` `enabled`, `enforcement` `enforced`, `basis` `xfs_quota_option`. No other xfs
   row can pre-empt it: the accounting-only row requires *only* `*noenforce` keys, the
   conflict row requires `noquota` together with a quota key, the absent row requires neither.
   Row 2 is the single matching row.
6. **Why the token means "enforced" (S078).** `fs/xfs/xfs_super.c` v7.2
   `xfs_fs_show_options` lines 238–241 print `,usrquota` exactly when
   `mp->m_qflags & XFS_UQUOTA_ENFD` is set and `,uqnoenforce` when only `XFS_UQUOTA_ACCT` is
   set; lines 253–254 print `,noquota` only when no quota accounting flag is set. The kernel
   therefore emits `usrquota` precisely in the enforced state, and never emits `noquota`
   alongside a quota key — which is why the fixture's string contains `usrquota` and not
   `noquota`. The option vocabulary itself is anchored in S077 (`xfs.rst` lines 171–185:
   `noquota` 171–173, `uquota/usrquota/uqnoenforce/quota` 175–177, `gquota/grpquota/gqnoenforce`
   179–181, `pquota/prjquota/pqnoenforce` 183–185).
7. **Verdict precedence.** Contract §C2: no setup error, and at least one path is `enabled` →
   exit `1`, finding id `QUOTA_ENABLED`. Positive evidence is never hidden by a sibling path,
   and here both paths are enabled. The expected per-path tuples are listed in the fixture's
   path order, matching the ordered `paths` array of the output schema.

## Ambiguities and gaps found (recorded, not resolved here)

1. **`enforced` is a filesystem-level flag, not "a limit exists".** S078 shows the emitted
   `usrquota` token means `XFS_UQUOTA_ENFD` is set at the time the super-option string is
   rendered (the string reflects current `m_qflags`, i.e. state at read time, not the original
   command line). S077's wording is "User disk quota accounting enabled, and limits
   (optionally) enforced" — the option names do not assert that any per-user limit is set or
   that EDQUOT would fire. The contract's own limits paragraph concedes that no per-user/group/
   project limit or usage is read. The contract's token `enforced` is therefore the only
   available cell for "accounting on with enforcement enabled"; a reader wanting "a limit
   exists" has no token and the probe has no data source. Flagged for L1: the token is
   enforcement-*capability/state*, not enforcement-*armed*.
2. **The contract's xfs key set is wider than what the kernel emits.** S078 shows
   `quota`, `uquota`, `gquota`, `pquota` (and bare `qnoenforce`) are accepted only as
   mount-time aliases and are never printed by `xfs_fs_show_options`; the emitted tokens are
   `usrquota`/`grpquota`/`prjquota`, their `*noenforce` counterparts, and `noquota`. This case
   therefore exercises only the observable token `usrquota`; the alias spellings in contract row
   2 remain untested by it, and the bare `qnoenforce` key in the contract's noenforce list has
   no documentation anchor in S077 (0 occurrences there) and is user-scope in S078.
3. **Row-order dependence is untested by this case.** Contract rows 3 (accounting-only) and 5
   (options absent) overlap in their English for a no-quota-key option set; only the
   "only *noenforce keys" wording of row 3 separates them, i.e. the table needs first-match
   semantics. This case has a quota key, so it cannot distinguish the two orderings — the
   `uqnoenforce`-only and options-absent cases own that axis.
4. **`device_check` is deliberately outside the expected tuple.** Contract §C2 output includes
   `device_check` and `quota_option_keys`, but the case schema's expected per-path object is
   exactly `path`, `fstype`, `mount_point`, `quota_state`, `enforcement`, `basis`. This case
   therefore pins the six-token tuple only (device equality is still a precondition: with a
   mismatching `st_dev` the expectation would be `device_mismatch` instead). Recorded so the
   oracle's comparison scope is unambiguous.
5. **Non-quota super options are carried in the fixture** (`attr2`, `inode64`, `logbufs=8`,
   `logbsize=32k`) to keep the option string realistic and to exercise "quota-related keys
   only" extraction. Since `quota_option_keys` is not part of the expected tuple, a leak of
   non-quota keys into that field would not be caught by this case; the sentinel output-leak
   seat owns that axis.

## Independence disclosure

The expectation was derived from contract §C2 plus S077/S078/S082 and was written before any
sibling case file was opened. For JSON key conventions only — no expectation content — I read
the peer case files `CaseXfsOptionsAbsent.json`, `CaseXfsMixedEnforce.json`,
`CaseXfsConflict.json` and the peer report `CaseXfsDevMismatch.md`; none of them covers the
`usrquota`-enforced scenario (their super options are `noquota`, `prjquota,gqnoenforce` and
`noquota,usrquota` respectively). No implementation, oracle or fixture-lint source was read.

## Files

- Case: `.ufo/waves/round-23/cases-proposed/CaseXfsUsrquota.json`
- This report: `.ufo/waves/round-23/build/CaseXfsUsrquota.md`

Report: `.ufo/waves/round-23/build/CaseXfsUsrquota.md`

---

# Correction — round-23 pre-seal amendment (appended 2026-10-21)

Amendment: `.ufo/waves/round-23/preseal-amendment.md`, written before L1 opened any
`ImplQuota` candidate or ran any C2 candidate; no C2 result was observed when the corrected
case was authored. No implementation, oracle or candidate source was read for this correction;
no test was run.

## Corrected case authored

`.ufo/waves/round-23/cases-corrected/CaseXfsUsrquota.json` — same id `CaseXfsUsrquota`, same
scenario text, same expected values. The proposal
`.ufo/waves/round-23/cases-proposed/CaseXfsUsrquota.json` is **retained unaltered**.

## Delta (exactly one fixture member)

The amendment's C2 btrfs rule adds a required fixture member `qgroups_enabled` to every
`btrfs_sysfs` UUID record and states the pairing "qgroups false must pair with
enabled=null/mode=null". This case carries one `btrfs_sysfs` record — the decoy for the btrfs
root line — whose `qgroups` is `false`; it therefore gains `qgroups_enabled: null` (its
`qgroups_mode` was already `null`). Record key set is now exactly
`devices`, `qgroups`, `qgroups_enabled`, `qgroups_mode`, matching the amendment's
"missing/extra record keys setup" rule and its exact bool/bool-or-null/mode-or-null typing.

Everything else is byte-identical to the proposal: the `mountinfo` text, both `paths` entries,
`device_links`, and the entire `expected` object (exit 1, `QUOTA_ENABLED`, and the two
six-field per-path tuples `enabled` / `enforced` / `xfs_quota_option`). The `rationale` was
rewritten to state the amendment and to re-derive against the superseding rules.

## Re-derivation under the amendment's superseding C2 rules

The expectation is unchanged, because no amended rule alters the outcome of an XFS mount
carrying the enforced `usrquota` token.

1. **Mount resolution.** The amendment keeps longest component-prefix selection and adds a
   refusal rule: "if ANY covering mountpoint occurs more than once, refuse classification as
   unknown/n/a/`ambiguous_overmount`, fstype=null, mount_point=null, device_check=not_checked".
   The fixture's mount points are `/` (btrfs root line) and `/srv/xfsquota` (xfs line), each
   occurring exactly once, so the ambiguity rule cannot fire. Longest prefix selects
   `/srv/xfsquota` for both probed realpaths. The amendment's "parse the separator and the last
   THREE fields of EACH chosen line, never file-wide" yields the same fstype `xfs`, source
   `/dev/nvme0n1p2` and super options for the chosen line; no backslash escape occurs, so the
   `040/011/012/134`-only octal rule is not engaged.
2. **Device check.** The amendment makes device mismatch preempt the filesystem table
   (unknown/n/a/`device_mismatch`, `device_check=mismatch`) and limits the btrfs equality skip
   to a zero stat major. Here fstype is `xfs` (not btrfs) and the mount `major:minor` `259:2`
   equals the paths' `st_dev` `259:2`, so no mismatch is declared and the XFS table is reached.
3. **XFS precedence.** The amendment's order is conflict (`noquota` with any quota/enforcement
   or noenforce key) → `noquota` → any enforced key → any accounting-only key → absent. The
   fixture's option keys are `rw`, `attr2`, `inode64`, `logbufs`, `logbsize`, `usrquota`: no
   `noquota`, so branches 1–2 do not apply; `usrquota` is an enforced key, so branch 3 applies
   → `enabled` / `enforced` / `xfs_quota_option`. The "mixed enforced/noenforce means SOME
   quota-type enforcement flag is set" clarification does not apply (one quota key only).
   `quota_option_keys` content is a supplementary check outside this case's six-field tuple.
4. **btrfs decoy.** The btrfs root line is never the chosen mount for either probed path, so
   the amended btrfs bases (`btrfs_qgroups_enabled`, `btrfs_qgroups_disabled`,
   `btrfs_qgroups_enabled_unavailable`) remain unreachable here. The decoy record's own
   `qgroups:false` / `qgroups_enabled:null` / `qgroups_mode:null` shape is the
   amendment-mandated pairing for an absent qgroups directory.
5. **Verdict precedence.** Unchanged by the amendment: no setup error, paths enabled →
   exit 1, `QUOTA_ENABLED`; positive evidence is never hidden by a sibling path.
6. **Fixture hygiene** under the amendment's new fixture rules: paths nonempty, unique,
   normalized absolute with no dot/dotdot components; `st_dev` `259:2` is a canonical decimal
   `MAJ:MIN` with no sign and no leading zero; the UUID key
   `8f3c1a2e-5b47-4d19-9c08-7e6b2a4d9f13` is canonical; the `devices` entry and the
   `device_links` mapped value are plain nonempty basenames without slashes or control
   characters.

The `ext`-rule change (`unknown` / `n/a` / `ext_quota_option_unverified`) and the
duplicated-covering-mountpoint change (`ambiguous_overmount`) do not touch this case: it is an
XFS case with a single occurrence of each covering mount point.

## Final hashes (SHA-256 of file bytes)

| file | SHA-256 |
|---|---|
| `.ufo/waves/round-23/cases-proposed/CaseXfsUsrquota.json` (original, retained unaltered) | `a8dc0a29e9c59256a861ede854e1907ec79b5a513d1d31768b72a37792afab19` |
| `.ufo/waves/round-23/cases-corrected/CaseXfsUsrquota.json` (corrected) | `3e1620f745d7a1cc6fa497b1f61f991539809cd1bde67f86b73860baaaa4244b` |

Report: `.ufo/waves/round-23/build/CaseXfsUsrquota.md`
