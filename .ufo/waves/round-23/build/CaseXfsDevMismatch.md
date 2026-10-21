# CaseXfsDevMismatch — C2 fixture case for the xfs device-identity mismatch

## Result

One independent C2 fixture case authored and written to
`.ufo/waves/round-23/cases-proposed/CaseXfsDevMismatch.json` (schema
`mori-quota-case-v1`). Scenario: an xfs mount whose mountinfo `major:minor`
differs from the probed path's `st_dev`.

Expected verdict (derived from `contract.md` §C2 only): exit `2`,
`finding_id` `QUOTA_STATE_UNKNOWN`, one path
`/mnt/xfsproj/work` → `fstype` `xfs`, `mount_point` `/mnt/xfsproj`,
`quota_state` `unknown`, `enforcement` `n/a`, `basis` `device_mismatch`.

No implementation was read: neither
`.ufo/waves/round-23/build/ImplQuota/` nor
`.ufo/waves/round-23/cases-proposed/` (other than confirming my own file name
was unused) nor `.scratch/round23/ImplQuota`. The expectation is derived from
`contract.md` (frozen at `4dc80c1be48308075e83af17f15fbfe7e95e6cb8`) and the
four named kernel sources only.

## Derivation

1. **Mount resolution.** Probed path `/mnt/xfsproj/work`, `realpath`
   `/mnt/xfsproj/work`, `st_dev` `8:16`. The contract's candidate rule
   (mount point equals realpath, or is `/`, or realpath starts with mount point
   + `/`) admits the fixture's root line `/` and its xfs line `/mnt/xfsproj`;
   the longest mount point wins, so the chosen mount is `/mnt/xfsproj`
   (`fstype` `xfs`, mountinfo `major:minor` `259:2`).
   Anchor: `proc.rst` §3.5 lines 1947–1957 (fields (1)–(6), optional fields
   (n…m), separator, filesystem type, mount source, super options) and line
   1949, field (3) *major:minor: value of st_dev for files on filesystem*.
2. **Device check.** Contract §C2: *"If chosen fstype is not btrfs and its
   major:minor ≠ the path's st_dev → `unknown` basis `device_mismatch`."*
   fstype is xfs (not btrfs) and `259:2 ≠ 8:16` → `quota_state` `unknown`,
   `basis` `device_mismatch`, `enforcement` `n/a` (the contract table's
   convention for every unknown-state row).
3. **The xfs rows are not reached.** The fixture's xfs super options are
   `rw,attr2,inode64,noquota`; without the device check that would select
   `xfs_noquota_option`. Anchors for those (unreached) rows: `xfs.rst` lines
   170–184 (`noquota`; `uquota/usrquota/uqnoenforce/quota`;
   `gquota/grpquota/gqnoenforce`; `pquota/prjquota/pqnoenforce`) and
   `xfs_super.c` `xfs_showargs` lines 238–254 (`usrquota`/`uqnoenforce`,
   `prjquota`/`pqnoenforce`, `grpquota`/`gqnoenforce`, `noquota`).
4. **btrfs contrast (why the rule is fstype-scoped).** `btrfs/inode.c` line
   8242 `stat->dev = BTRFS_I(inode)->root->anon_dev;` — a btrfs subvolume
   reports a per-subvolume anonymous `st_dev` that legitimately differs from
   the mountinfo `major:minor`, which is exactly why the contract exempts
   btrfs (`device_check` `btrfs_subvolume_skipped`). For a non-btrfs
   filesystem the mountinfo `major:minor` *is* the filesystem's `st_dev`
   (`proc.rst` line 1949), so a difference means the probed path is not on the
   chosen filesystem and no quota verdict about that filesystem may be
   asserted.
5. **Verdict precedence.** Contract §C2: *else any `unknown` → 2
   `QUOTA_STATE_UNKNOWN`*. The single path is unknown, none is enabled →
   exit `2`, finding id `QUOTA_STATE_UNKNOWN`.

## Fixture shape

`mountinfo` holds four lines, all parsed per §3.5 (6 fields, optional fields,
`-`, fstype, source, super options):

| line | major:minor | mount point | fstype | purpose |
|---|---|---|---|---|
| 1 | `259:3` | `/` | xfs | root line; always a candidate, never the longest for this path |
| 2 | `0:22` | `/proc` | proc | non-candidate; shows optional-field parsing (`shared:12`) |
| 3 | `0:30` | `/home` | btrfs | non-candidate btrfs line, mirrors the frozen real control |
| 4 | `259:2` | `/mnt/xfsproj` | xfs | the chosen mount; `major:minor` ≠ the path's `st_dev` |

`paths` carries one entry (`/mnt/xfsproj/work`, realpath identical,
`st_dev` `8:16`). `device_links` maps `/dev/mapper/root` → `dm-0`;
`btrfs_sysfs` carries the single uuid from `frozen/c2-expected-real.json`
with `devices` `["dm-0"]`, `qgroups` `false`, `qgroups_mode` `null` — inert for
this case, present so the fixture stays a realistic host view rather than a
one-line toy. `st_dev` `8:16` (SCSI-style) versus the mountinfo `259:2`
(NVMe-style) models a stale mountinfo device record after a device
renumber: the numbers disagree, so the probe must not attribute the mount's
quota options to the probed path.

## Contract ambiguities found (not asserted by the case)

1. **The `device_mismatch` clause is not explicitly stated to preempt the
   fstype classification table.** The clause gives a complete verdict
   (`unknown` + `device_mismatch`) and the sealed comparison is on a single
   `basis` per path, so the only self-consistent reading is that the device
   check replaces the table row. Under the alternative reading (classify by
   options *and* report the mismatch) the case would expect
   `basis` `xfs_noquota_option` with `device_check` `mismatch` — a materially
   different expectation. **Medium severity:** an implementation could
   plausibly choose either. Recommendation to L1: state the precedence
   explicitly in the sealed contract text.
2. **`device_check` has no named token for a non-btrfs mismatch.** The
   contract names only `match` and `btrfs_subvolume_skipped`. The natural
   third token is `mismatch`, but it is not in the contract's token list. The
   case's `expected.paths` uses exactly the six contract-comparison fields
   (path, fstype, mount_point, quota_state, enforcement, basis) and therefore
   does not depend on this gap; the oracle must likewise not compare
   `device_check` for this case.
3. **`enforcement` for a `device_mismatch` verdict is derived by convention,
   not stated.** Every `unknown`-state row in the contract table carries
   `enforcement` `n/a`, while `enforcement` `unknown` appears only in the
   btrfs-enabled row ("qgroup presence ≠ any limit set"). The case asserts
   `n/a`; a contract that intends `unknown` would make this expectation
   wrong. **Low–medium severity**, but it is a free-text-free token
   comparison and would flip a pass/fail.
4. **The rule's scope for `other`/tmpfs/ext fstypes is unstated.** The
   clause is written for "not btrfs", so it also governs tmpfs (`enforcement`
   `enforced` in the table) and unsupported fstypes (`unsupported_fstype`).
   This case does not exercise those, but the oracle author should know the
   clause is fstype-general, not xfs-specific.
5. **S-id assignment for the source rows is not yet in the registry.**
   `corpus/SOURCES.md` currently ends at S076; S077–S084 are the eight
   round-23 source scribes. The S-ids used in this case are inferred from the
   wave-1 source-scribe order (`SrcXfsDoc`, `SrcXfsShowargs`, `SrcBtrfsSysfs`,
   `SrcBtrfsQgroup`, `SrcBtrfsGetattr`, `SrcProcMountinfo`, `SrcExt4Doc`,
   `SrcTmpfsDoc` → S077…S084), which is confirmed by the contract's own
   pointer "per-subvolume anonymous st_dev, **S081**" matching
   `SrcBtrfsGetattr` (the fifth scribe). The rationale therefore also carries
   the upstream URL + line anchors so the case survives renumbering.
6. **Minor anchor drift.** The `SrcBtrfsGetattr` task text cites
   `btrfs_getattr` at ~8246; the assignment is at `btrfs/inode.c` line **8242**
   in tag v7.2. The scout should record 8242.

## Sources opened (upstream, tag v7.2)

- `Documentation/filesystems/proc.rst` — §3.5 mountinfo field list, lines
  1944 (sample), 1947–1957 (fields), 1949 (major:minor = st_dev).
- `Documentation/admin-guide/xfs.rst` — lines 170–184: `noquota`,
  `uquota/usrquota/uqnoenforce/quota`, `gquota/grpquota/gqnoenforce`,
  `pquota/prjquota/pqnoenforce`.
- `fs/xfs/xfs_super.c` — lines 114–168 (option table), 238–254
  (`xfs_showargs` printing `usrquota`/`uqnoenforce`/`prjquota`/`pqnoenforce`/
  `grpquota`/`gqnoenforce`/`noquota`).
- `fs/btrfs/inode.c` — line 8242: `stat->dev = BTRFS_I(inode)->root->anon_dev;`.

Fetched read-only over HTTPS; no bytes were written outside my assigned case
file and this report (no scratch fixture, no host probe).

## Bounds honored

- No live host read of any kind was performed for this case: no
  `/proc/self/mountinfo`, no `os.stat`, no `/sys/fs/btrfs` listing, no
  `/dev/mapper` readlink. All host-shaped values in the fixture are synthetic
  or copied from the frozen `frozen/c2-expected-real.json`.
- No `quotactl`, `btrfs`, `xfs_quota`, `repquota`, `mount`, or any privileged or
  mutating command was invoked; nothing was remediated, pinned, dispatched or
  configured.
- No test, build, lint, formatter or self-test was run. The only executed
  command was a JSON parse of my own case file (structure + mountinfo field
  split), which is a fact about my artifact, not a gate.
- No tool was installed or updated by this seat (no install needed); the
  operator tooling directive is recorded as a no-op.

## Residual risk / verification gaps

- The expected `basis`/`enforcement` depend on reading the `device_mismatch`
  clause as preempting the fstype table and on the table's `n/a` convention
  (ambiguities 1 and 3). If L1's sealing text resolves either differently,
  this case must be re-derived, not edited to match an implementation.
- The `st_dev`/`major:minor` mismatch is synthetic. It is a faithful exercise
  of the contract rule, but the real-host equivalent (a stale mountinfo device
  record) was not observed, so the case asserts a *rule*, not a *host fact*.
  `frozen/c2-expected-real.json` remains the only host control, and it does
  not contain a mismatch (its `/tmp` xfs path is `match`).
- Because the case asserts only six per-path fields, it does not constrain
  `device_check`, `quota_option_keys` or `btrfs_qgroups_mode`; those remain
  unverified for the mismatch branch until the oracle author decides whether
  the contract's `device_check` vocabulary is closed.

---

## Correction — pre-seal amendment (appended after `preseal-amendment.md`)

A corrected case was authored at
`.ufo/waves/round-23/cases-corrected/CaseXfsDevMismatch.json` (same `id`
`CaseXfsDevMismatch`). The original proposal
`.ufo/waves/round-23/cases-proposed/CaseXfsDevMismatch.json` is **untouched**
(unchanged bytes, SHA-256 `f6d4f5fd3dae0eb55532665e9daaea2610875b0a30dafa88be478c16e4fee377`).
Corrected case SHA-256:
`e5db2d1181e0b6ab2062447e2181307a9da4ba64760ce98a0d76f55ccb492097`.

### Delta

| element | original proposal | corrected case | driver |
|---|---|---|---|
| `fixture.btrfs_sysfs[uuid].qgroups_enabled` | absent | `null` | amendment: "Add required fixture member `qgroups_enabled` to each btrfs_sysfs UUID record"; `qgroups` false pairs with `enabled` null and `mode` null, and this record is a **decoy** for the probed path but must still carry the member |
| `fixture.btrfs_sysfs[uuid].qgroups_mode` | `null` | `null` (unchanged) | amendment: mode null when `qgroups` false |
| `expected.paths[0]` | `unknown` / `n/a` / `device_mismatch` | unchanged | amendment device clause confirms the original reading: "Device mismatch PREEMPTS the filesystem table: unknown/n/a/device_mismatch" |
| `expected.paths[0].device_check` | not asserted (six scored fields only) | not asserted (six scored fields only) | amendment names the token `mismatch`; it is stated in the rationale prose, not added as a scored field, so the original six-field denominator is preserved |
| `mountinfo`, `paths`, `device_links`, `exit`, `finding_id`, `sources` | — | unchanged | no amendment clause touches them |

The btrfs `enabled` basis rename (`btrfs_qgroups_enabled`), the ext
`unknown`/`n/a`/`ext_quota_option_unverified` change and the duplicated
covering-mount-point `ambiguous_overmount` change apply to other seats' cases
(btrfs-enabled, ext-positive and stacked/duplicate cases) and to **no** part of
this case: this fixture's only btrfs record is a decoy with `qgroups` false
(no qgroups directory → `btrfs_qgroups_dir_absent`, never reached because the
path is not on the btrfs mount), there is no ext path, and the covering
mount points of `/mnt/xfsproj/work` are `/` (once) and `/mnt/xfsproj` (once) —
no covering mount point occurs more than once, so the amendment's
`ambiguous_overmount` refusal does not apply (verified mechanically over the
fixture's non-empty lines).

### Amendment clauses that close the ambiguities I reported

1. *Preemption* — resolved: the device mismatch clause now states
   "PREEMPTS the filesystem table: unknown/n/a/device_mismatch".
2. *`device_check` token* — resolved: `mismatch` is now named for this branch
   (only `match` and `btrfs_subvolume_skipped` were named before).
3. *`enforcement` for a mismatch* — resolved: the clause states `n/a`
   explicitly, matching the table convention I had derived.
4. *btrfs exemption scope* — the amendment narrows it to a **zero stat major**;
   this case's stat major is 8 and its fstype is xfs, so it is unaffected.
   The sibling btrfs case `CaseBtrfsDevMatch` carries the zero-major branch.

### One residual gap (not asserted by the case)

The amendment fixes `device_check` for the mismatch branch but does not say
whether the preemption also suppresses the supplementary `quota_option_keys`
for the xfs super options `rw,attr2,inode64,noquota` (`["noquota"]` if the
option extraction still runs on the chosen line, `[]` if it is suppressed
together with the classification table). The case asserts only the six scored
fields, so neither reading can fail it; the oracle author may want to pin the
choice in prose.

### Bounds for this correction

No candidate implementation was read and no test, build, lint, formatter or
self-test was run; the only executed command was a JSON parse plus a mechanical
covering-mount-point count over my own corrected fixture, and SHA-256 hashing
of my own two case files. No live host read of any kind was performed. Only
the explicitly authorized new output path (`cases-corrected/`) and this report
were written; the original proposal file was not modified.
