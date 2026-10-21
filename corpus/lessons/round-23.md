author: mori-shokunin (L1 MadoR22-2, reused coordinator)
round: 23

# Round23 — distinguish a mechanism flag from an interface's presence

## Claims and authority

C1 calibration, held5: remove misleading raw_unallowlisted with schema-v2 clean
cutover; canonical scanner_unallowlisted retains its in-scope meaning and
raw_not_allowlisted its raw-complement meaning. C2 coverage capability, held6:
FR2 visible quota-mechanism state, not limits/usage, exhaustion, privacy clearance
or remediation. Original preregistration4dc80c1; source-derived amendments in
`.ufo/waves/round-23/preseal-amendment.md` precede opening/measuring the blind C2
candidate. Original proposals, oracles, failed drafts and all expected bytes remain
visible; revisions have new names. No observed C2 result selected an expectation.

MANIFEST rounds[427] admits r22's bounded retention accounting, not privacy/history
clearance. Four unallowlisted hits, original permission control RED11/12, two unknown
dispositions and blocked baseline acceptance remain debt. No r24.

## Mistakes

| ID | Class | Evidence pointer | Captured-by | Fix / fail-capability |
|---|---|---|---|---|
| M1 | chronology | r22 expected-real.json first landed with production8cb4afb; outside rounds[427] | existing freeze-order/expected-before-code requirements | Seal every executable oracle/driver/expected/dependency before implementation; strict ancestor, production absent/unchanged at seal. Actual guard red/green follows exercise; timestamps alone do not prove private chronology. |
| M2 | misleading population name | r22 raw_unallowlisted4 actually in-scope; raw_not_allowlisted9 | QUALITY70 population identity | Preregistered schema-v2 removal before build; keep scanner_unallowlisted4/raw_not_allowlisted9 and all historical artifacts. Exact two-source-transformation + object-equality guard prevents unintended code changes. |
| M3 | source contradiction | original contract ext enabled row versus S083262–263 | primary-source claim-vs-source check | Before seal/candidate inspection, change ext hints to unknown, preserve original proposals and separately derive corrected cases. A quota option hint is not quotaon state. |
| M4 | presence mistaken for active state | original btrfs qgroups-dir-present→enabled; source reviewers SrcBtrfsQgroup/Sysfs | primary lifecycle and enabled-flag source | Read qgroups/enabled first; do not read ASSERT-guarded mode unless on. Directory absence only follows successful parent inspection. Frozen present-but-disabled/unknown cases must distinguish this. |
| M5 | unsafe mount-order assumption | CriticContractC2 D1/D2; original last-line-wins | no-false-disabled reporting | Refuse duplicate covering mountpoints/ancestor-overmount ambiguity rather than infer topology from line order. Original stacked proposal retained; corrected case reports unknown. |
| M6 | incorrect reproduction mechanism | contract claims r22 stages tool from revision; CriticRenameHarm | instrument source review | r22 reproduces only in a checkout of its bound revision; subset output whitelist does not break when a key is removed. Real/refinement old-key checks are the actual API breakages. Append correction, never rewrite frozen original. |
| M7 | fixture invocation | first L1 before oracle used relative output, yielding relative synthetic repo path, then retried absolute | absolute tool/input paths | First uncommitted setup-only run was discarded before any freeze change; second absolute invocation gives expected25/26 (R25red, eight alias-bearing runs). Disclosure is not fabricated red-before evidence. No expected bytes changed. |
| M8 | procedure | early L1 used shell sed/grep/ls and Python edits rather than specialized tools; W1 CaseOptionalFields/DraftSourceRows used transient /tmp; sibling-case exposures disclosed by TmpfsUsrquota/SetupMalformed/NoCover/SymlinkRealpath | host tool policy and wave scope | Preserve deviations and limits, use surgical edits/targeted tools from correction onward. No retroactive independence or compliance claim; source-based expectations retained. |

## Gate

All source rows S077–S086 opened2026-10-21; raw bytes and SHA256 retained under
`.ufo/waves/round-23/evidence/sources/` and `sources-manifest.json`. Primary scoped
A is documentary authority, not proof of final implementation or runtime health.
S077–S084 were planned forward IDs at4dc80c1, not rows already present then.

| Row | URL | Located quote (≤25 words) | Decision / scope |
|---|---|---|---|
| S077 | https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/admin-guide/xfs.rst |171–173: “Forcibly turns off all quota accounting and enforcement within the filesystem.” | Admit A for XFS noquota vocabulary only, not limits or all enforcement states. |
| S078 | https://raw.githubusercontent.com/torvalds/linux/v7.2/fs/xfs/xfs_super.c |253–254: `if (!(mp->m_qflags & XFS_ALL_QUOTA_ACCT)) seq_puts(m, ",noquota");` | Admit A for emitted XFS accounting/enforcement tokens, not synthetic conflicts/absence as host states. |
| S079 | https://raw.githubusercontent.com/torvalds/linux/v7.2/fs/btrfs/sysfs.c |2363: `enabled = fs_info->qgroup_flags & BTRFS_QGROUP_STATUS_FLAG_ON;` | Admit A for explicit enabled flag; reject directory-presence alone as active-state authority. |
| S080 | https://raw.githubusercontent.com/torvalds/linux/v7.2/fs/btrfs/qgroup.c |444: “default this to quota off, in case no status key is found” | Admit A for lifecycle/flag separation; initialized directory can persist with quota off. |
| S081 | https://raw.githubusercontent.com/torvalds/linux/v7.2/fs/btrfs/inode.c |8246: `stat->dev = BTRFS_I(inode)->root->anon_dev;` | Admit A for btrfs per-subvolume anonymous st_dev, not other filesystems or quota enablement. |
| S082 | https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/filesystems/proc.rst |1985: “Parsers should ignore all unrecognised optional fields.” | Admit A for mountinfo field layout only; no last-line ordering or escape guarantee inferred. |
| S083 | https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/admin-guide/ext4.rst |262: “These options are ignored by the filesystem.” | Admit A for documented option limitations; reject option-present as proof of enabled quotas. |
| S084 | https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/filesystems/tmpfs.rst |132–134: “User and group quota accounting and enforcement is enabled on the mount.” | Admit A for tmpfs quota flags; hardlimit-only activation is not taught by this sentence. |
| S085 | https://raw.githubusercontent.com/torvalds/linux/v7.2/fs/proc_namespace.c |172: `seq_puts(m, " - ");` | Admit A for per-mount namespace field emission/escaping, not topology inferred from ordering. |
| S086 | https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/shmem.c |4878–4879: `if (sb_has_quota_active(root->d_sb, USRQUOTA)) seq_printf(seq, ",usrquota");` | Admit A for actual tmpfs active-quota emission and four hardlimit names; no arbitrary suffix matching. |

New rows enter mined with used-by this lesson. They gain the final knowledge note
only after that note exists and cites them; mutable-field changes are logged below.
No existing immutable registry row is edited. Additional source rows085/086 close
original source coverage gaps, not implementation-result-selected evidence.

Reject: `QUOTA_DISABLED` means capacity/health/exhaustion clear; directory presence
means enabled; checksum means authenticated repository; author advisers are a fresh
non-author spot-check. Flip requires the actual missing authority, not a green
selftest. Current outside-lane admit/reject check remains pending parent closure.

## Scope and remaining debt

Mori observes kernel-visible state on runway targets, never fstab/mount units,
Snapper/config or superblock configuration and never quota commands/ioctls. Causes,
configuration/remediation route to tsukuroi/operator. No census integration or baseline
re-pin. Named default paths only; /dev/shm's tmpfs usrquota is outside the default pair.
QUOTA_DISABLED can coexist with ENOSPC. Parent now requires heavy scratch under
`/fast/scratch/hyaku/mori-r23/`; new work uses that root, and only this round's scratch
is removed at landing. Entering .scratch/round22 is operator/prior evidence, untouched.

Source used-by changes (all ten S077–S086): `corpus/lessons/round-23.md` →
`corpus/lessons/round-23.md, corpus/knowledge/quota-surface-r23.md`; mined→mined and
on-release→on-release unchanged. The note exists and cites every source. Delta receipt
is `build/DraftSourceRows.md` under the round23 wave directory.
