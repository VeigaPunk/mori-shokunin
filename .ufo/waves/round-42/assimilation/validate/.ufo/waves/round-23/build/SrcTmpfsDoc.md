# SrcTmpfsDoc — tmpfs quota mount options re-open (round 23, C2)

Seat: `MadoR22-2.SrcTmpfsDoc-8` (leaf source re-opener). Contract read in full at
`.ufo/waves/round-23/contract.md` (frozen revision `4dc80c1be48308075e83af17f15fbfe7e95e6cb8`).
Independence held: no candidate implementation (`.ufo/waves/round-23/build/ImplQuota/`,
`.scratch/round23/ImplQuota`) and no proposed cases (`cases-proposed/`,
`build/OracleQuota/`) were opened. No edit to `corpus/SOURCES.md`.

## Fetch identity

- URL: `https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/filesystems/tmpfs.rst`
- Method: `curl -sSL` into `/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/round23/SrcTmpfsDoc/tmpfs.rst`
- Fetched: 2026-10-21; HTTP/2 200; `etag: "8a144d1c0b6ed02286911002361760fa897cdb16c9fc5777db8336ab192aa771"`
- Bytes: 13078; lines: 276
- **SHA-256: `5ce3dffe9323912b9146a5f33744776ff623ef42cf8accd6b2dfbea0b9db5be6`**

## Anchor verification — CONFIRMED, exact extent 129–145

The task's anchor "quota mount options (~129–145)" is exact:

- 129: heading `tmpfs also supports quota with the following mount options`
- 131: table rule; 132–134: `quota` row; 135–136: `usrquota` row; 137–138: `grpquota` row
- 139–142: `usrquota_block_hardlimit`, `usrquota_inode_hardlimit`,
  `grpquota_block_hardlimit`, `grpquota_inode_hardlimit` rows
- 143: table rule; 144: blank
- 145: `None of the quota related mount options can be set or changed on remount.`

The only other quota mentions in the file are 147–158 (limit suffixes/defaults and
user-namespace note) and none adds enabling semantics.

## Located quote (12 words, lines 132–134)

> User and group quota accounting and enforcement is enabled on the mount.

Exact byte location: line 132 `quota                    User and group quota accounting and enforcement`,
line 133 `                         is enabled on the mount. Tmpfs is using hidden`, line 134
`                         system quota files that are initialized on mount.` The quoted sentence
spans 132–134; the `quota` key itself is line 132. Parallel sentences exist at 135–136
(`usrquota`) and 137–138 (`grpquota`).

## Rule coverage vs contract §C2 (contract lines 120–121)

The rule under test (contract line 120):
`tmpfs | any of quota,usrquota,grpquota or a key ending _hardlimit | enabled | enforced | tmpfs_quota_option`,
and line 121: `tmpfs | none of them | disabled | tmpfs_quota_options_absent`.

| Clause of the rule | Source verdict | Basis |
|---|---|---|
| `quota` present → accounting **and enforcement** | SUPPORTED | 132–134 states accounting and enforcement are enabled; hidden quota files initialized on mount |
| `usrquota` / `grpquota` present → accounting and enforcement | SUPPORTED | 135–136 and 137–138 use the same "accounting and enforcement" wording |
| "a key ending `_hardlimit`" alone → enabled **and enforced** | **UNDER-DETERMINED** | 139–142 only say "Set global user/group quota block/inode hard limit." The file never states that supplying a `_hardlimit` option by itself enables quota accounting or enforcement, nor whether it implies the corresponding `usrquota`/`grpquota` mode. This arm needs a kernel-code source, not this doc |
| none of the keys → `disabled` | SUPPORTED BY IMPLICATION, not literally stated | 129 introduces quotas as features activated by "the following mount options"; 145 makes them mount-time-only; absence from super options therefore means not enabled on that mount. The doc never writes an explicit default-disabled sentence |
| Mount-time-only / super-options are the right state surface | SUPPORTED | 145: quota-related options cannot be set or changed on remount; 147–148 repeats this for limit parameters |

**Overall: supports (does not contradict), with one material gap.** Nothing in 129–158
contradicts the contract table. The single unsupported disjunct is `_hardlimit`-only
enabling/enforcement; the "absent → disabled" direction is a defensible reading of the
same text rather than an explicit statement.

Consequence for C2: the contract's `tmpfs_quota_option` row is only partially
documented by this source. Any sealed tmpfs case that expects `enabled`/`enforced` from a
`*_hardlimit`-only mount (wave-1 scenario `CaseTmpfsHardlimit`, `grpquota_block_hardlimit=1m`
only) rests on kernel implementation behavior, not on this documentation; L1 should not
cite this file as support for that arm and should require a code anchor (e.g. the tmpfs
option parser) if the arm is to be sourced at all.

Nuance on the contract's stated limits: contract line ~137 says "sysfs/mountinfo races
during enable/disable/remount are not excluded", while line 145 documents that quota
options cannot be set or changed on remount. The doc thus narrows the remount part of
that race caveat for quota keys (a fresh mount/umount can still race), without
contradicting the general no-race-exclusion boundary.

## Tier assignment

**Tier A**, scope: *tmpfs quota mount-option vocabulary and documented semantics only —
`quota`/`usrquota`/`grpquota` enable quota accounting and enforcement on that mount;
`*_block_hardlimit`/`*_inode_hardlimit` set global limits and, like all quota options,
are mount-time-only (not changeable on remount).*

Rationale: pinned upstream kernel documentation at tag `v7.2`, primary for the named
options. Scope deliberately excludes (a) whether a `_hardlimit`-only mount enables
quota, (b) the default-disabled direction as an explicit statement, (c) any per-user/
group/project limit or usage observability, and (d) runtime enforcement beyond the
documented mount-option claim. Within that scope it is the authoritative reference; for
the excluded `_hardlimit` arm it cannot be the sole support.

If L1 prefers tiering by evidential strength for the *whole* tmpfs row as written, this
row would be **B for the `_hardlimit` arm / A for the named-option arm**; a single tier
letter should be **A with the narrowed scope above**, not A for the full row.

## Residual unknowns / gaps

- No statement in this file resolves whether `usrquota_block_hardlimit=...` alone turns
  accounting/enforcement on; the doc's wording is consistent with "limit value is
  stored, quota still off", so the contract's enabled+enforced expectation for that arm
  is unproven here.
- The file does not define what kernel emits in mountinfo super options after a failed or
  partial quota mount; the probe's option-key reading remains a documentation-level
  inference.
- `Note that tmpfs quotas do not support user namespaces` (157–158) is out of scope for
  the C2 rows but bounds enforcement observability in user-namespaced mounts.
- No tool installs or upgrades were performed; no live host probes were made beyond the
  network fetch above. `SOURCES.md` untouched.
