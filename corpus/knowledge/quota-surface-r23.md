source: S077–S086 in corpus/SOURCES.md; Linux v7.2 scoped primary docs/code; .ufo/waves/round-23/contract.md and preseal-amendment.md; corpus/knowledge/audit-r11.md:95-99,168,218-222
verified-at: 2026-10-21 source opening and independently re-opened initial eight sources; primary-source digests/quotes in .ufo/waves/round-23/evidence/sources-manifest.json and source-quotes.json; implementation observations are separate revision-bound receipts
recheck: open S077–S086 at pinned v7.2, compare raw hashes; run the sealed round23 oracles against the explicitly selected committed tools, never infer a current host state from the documentary table

# Filesystem quota visibility is not a capacity or exhaustion verdict

FR2 asks what fleet runway reporting misses when it reads only df. A filesystem can
impose user/group/project or subvolume limits that df percentages do not measure.
The historical census selftest's `Disk quota exceeded` abort is evidence of a failed
write, not an identified filesystem/mechanism/cause (audit-r11 anchors above).
No source-only table or new probe retrospectively diagnoses that failure.

## Sources change the question before implementation

The original round23 contract contained two unsound implications. Independent
source re-openers and critics caught both before L1 opened/measured the blind quota
candidate. Original drafts/cases remain under the round23 wave directory; corrected
cases have separate paths and are sealed before implementation.

1. **An initialized btrfs qgroups directory is not an enabled flag.** S079 exposes
   enabled from BTRFS_QGROUP_STATUS_FLAG_ON. S080 creates the directory before parsing
   that flag and can leave it initialized while quota is off. Read enabled first;
   read mode only when enabled is1, since qgroup_mode_show asserts enabled. Directory
   absence is usable only after successful parent inspection, never an access error.
2. **ext quota options are not proof of runtime quota enablement.** S083 documents
   plain quota hints as ignored by the filesystem and journal options as replay
   configuration. Without privileged/runtime state inspection, report unknown both
   when a hint exists and when it does not. Do not convert a hint to an enabled fact.

## Decision table for the separate runway probe

`tools/mori-quota-surface.py` is separate from the census. It reads kernel-visible
state, reports only, and never configures quotas or changes the drift baseline.

| Surface evidence | Reporting state | Source / interpretation boundary |
|---|---|---|
| XFS noquota, no other quota flag | disabled | S077/S078: no accounting flags; no capacity/health implication |
| XFS usrquota/grpquota/prjquota or accepted enforcing alias | enabled, enforced | S078: at least one enforcement flag, not a nonzero limit or every quota type |
| XFS only uqnoenforce/gqnoenforce/pqnoenforce accounting flags | enabled, accounting_only | S078: accounting is not enforcement |
| XFS conflicting noquota plus quota flag, or no quota token at all | unknown | defensive parser rules, not claimed normal v7.2 kernel output |
| btrfs directory present, enabled1 | enabled, enforcement unknown | S079/S080: flag read, not a limit/usage read |
| btrfs directory present, enabled0 | disabled | initialized-but-disabled is distinct from absent |
| btrfs directory present, enabled unreadable/invalid | unknown | never read ASSERT-guarded mode or silently substitute disabled |
| btrfs directory absent after successful UUID/device parent inspection | disabled at snapshot | no promise across concurrent enable/disable or remount |
| btrfs device unassociated/ambiguous, or sysfs access error | unknown | do not borrow a different UUID or conflate access failure with absence |
| ext2/3/4 quota hints/replay settings present or absent | unknown | S083 does not authenticate active quota state; superblock/runtime inspection is out of scope |
| tmpfs usrquota/grpquota flags or one of four documented hardlimit keys | enabled, enforced | S084/S086: actual emission tied to quota initialization; never arbitrary `_hardlimit` suffix matching |
| tmpfs no quota options | disabled at snapshot | S086 compiled-out or inactive quota prints no quota keys; no capacity implication |
| NFS/server quota, overlay/fuse, other unsupported filesystem | unknown | no extrapolated enabled/disabled claim |

The probe's explicit `--path` accepts operator-pinned runway targets; defaults are
fleet root and /tmp, matching the census's canonical default pair at this round.
This does not survey every host filesystem. The independent host observation frozen
before implementation found btrfs /home without qgroups and XFS /tmp with noquota;
/dev/shm simultaneously had tmpfs usrquota outside the defaults. The frozen default
control is a dated expected observation, not a permanent disabled assertion.

## Resolve the mount before interpreting its mechanism

S082 describes mountinfo fields, not a safe last-line-wins stack algorithm. S085
shows per-mount emission and escaped path fields. Compare the resolved given path
to component boundaries, never a bare prefix (`/a/b` does not cover `/a/bc`).
Refuse ambiguous duplicate covering points or inconsistent chosen-parent topology
instead of claiming disabled for a hidden nested mount. Missing topology, unsupported
fstypes and snapshot races remain limits, not inferred absence.

S081 assigns a btrfs path's stat device from its subvolume root's anonymous device,
which can differ from mountinfo's superblock device. A major0 btrfs mismatch is a
recorded skipped check, not verified identity. Ordinary non-btrfs device mismatch
preempts quota classification. The probe does not resolve arbitrary mount topology
or authenticate filesystem associations.

## Exit and evidence vocabulary

- 0 QUOTA_DISABLED: all requested paths have a disabled-mechanism observation.
- 1 QUOTA_ENABLED: at least one requested path has positive mechanism evidence;
  retain unknown siblings. This is not a fleet failure, limit breach or health alarm.
- 2 QUOTA_STATE_UNKNOWN: mechanism state could not be determined for at least one
  path and no enabled evidence exists. Read finding_id, not exit code alone.
- 2 QUOTA_SETUP: invalid/unreadable inputs; no partial verdict, no input text echoed.

QUOTA_DISABLED can coexist with ENOSPC or a full filesystem. df remains a capacity
signal. QUOTA_ENABLED does not show that a limit is set or exhausted. Fixed per-path
basis tokens explain evidence class without exposing mount sources, UUIDs, quota-file
names or option values. Only recognized quota option keys are emitted.

## Ownership fence

Mori reads /proc/self/mountinfo, target stat/realpath and the named btrfs sysfs fields.
No fstab, mount unit, Snapper/config or superblock reads; no quotactl/ioctl, btrfs,
xfs_quota, repquota, mount, writes, quota enable/disable or cleanup. Configuration,
why a mechanism is on/off, and remediation route to tsukuroi/operator. realpath/stat
on arbitrary remote or automount paths can block or trigger resolution; the probe
makes no universal effect-free claim there. Per-ID limits/usage, EDQUOT attribution,
NFS/overlay/fuse state, btrfs-on-btrfs ambiguity, snapshot races and census integration
remain frontier. Privacy/history clearance and baseline acceptance remain blocked
by the existing independent debt, not changed by quota visibility.
