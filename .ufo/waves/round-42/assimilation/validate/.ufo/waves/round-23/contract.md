# mori round 23 — pre-registered contract (written before any implementation)

L1: MadoR22-2 (reused idle agent, acting as mori L1 for this round only). Entering
branch `1bfe708a170c877db3319060d0ab38771efe03ac` (r22 admitted, MANIFEST rounds[427]).
Claim held: mori=23 attempt1. Never start r24. Detection and report only.

## Routed items from the r22 closure (rounds[427])

1. `raw_unallowlisted` is a misleading frozen field name: its value is the in-scope
   (non-author-filtered) unallowlisted count, identical to `scanner_unallowlisted`;
   the true raw complement is `raw_not_allowlisted`. This contract pre-registers the
   rename/deprecation (C1) **before** any code change.
2. r22's `frozen/expected-real.json` landed with the implementation. Here every
   expected/oracle/requirements file lands in a commit **before** the implementation
   commit; the measure drivers check that ordering by commit ancestry and time.
3. Untracked `.scratch/` (646 MB at entry) stays out of every commit (only named
   paths are committed through jj-lane.sh).
4. Open debt carried, not cleared: 4 unallowlisted retention hits; original permission
   control RED 11/12; two historical dispositions unknown; baseline acceptance blocked;
   no privacy clearance.

## Claims (1–3; causally separable; distinct axes)

### C1 — calibration (lowest non-retired tie: calibration/depth/freshness = 5), score held 5

Remove the misleading output field. `tools/mori-retention-reconcile.py`:

- `SCHEMA` becomes `mori-retention-reconciliation-v2` in **every** output (check,
  setup error, selftest).
- The key `raw_unallowlisted` is **removed** from every output (clean cutover, no alias).
  Canonical names: `scanner_unallowlisted` = in-scope unallowlisted count (old
  `raw_unallowlisted` value, unchanged semantics); `raw_not_allowlisted` = raw
  identities not covered by a non-forbidden allowlist row (unchanged semantics).
- No other output key, value, exit code or finding id changes.

Frozen requirements (`frozen/c1-requirements.json`, oracle `oracle-rename.py`):

- R01–R24 = the r22 frozen v2 requirements, byte-for-byte predicates except that
  R02, R11, R12 read `scanner_unallowlisted` where they read `raw_unallowlisted`
  (pure field substitution; same expected values 1/3/1).
- R25 — every oracle run whose stdout parses as a JSON object has
  `schema == "mori-retention-reconciliation-v2"` and no key `raw_unallowlisted`.
- R26 — on the `valid` and `forbidden` builder arms,
  `raw_not_allowlisted` equals an independent count: raw hits (expected scanner hits
  + expected policy hits from the frozen r22 builder) whose (path,class,line_sha256)
  is in no allowlist row with a path outside `must_redact_paths`, read from the
  fixture's committed allowlist/policy bytes.
- Headline counter: `misleading_alias_runs` = number of oracle runs whose JSON output
  contains `raw_unallowlisted`. Before (tool at `1bfe708`) expected > 0; after 0.
  Requirement passes before expected 25/26 (R25 red), after 26/26.

Real control (`frozen/c1-expected-real.json`, frozen now): the r21 committed receipt
at `77a5bbe8a0b41dfbfd2546d024d36e294b814bd0` reconciles exit 0 `RETENTION_RECONCILED`,
`scanner_unallowlisted` 4, `raw_not_allowlisted` 9, `raw_total` 95, `allowlisted` 86,
`policy_excluded` 5, `scanner_total` 90, `retention_state` red, `privacy_clearance`
false, schema v2, key `raw_unallowlisted` absent.

Declared consequence (not hidden harm): r22's oracle-reconcile-v2 R02/R11/R12 and
measure-round22.py's output whitelist read the old key, so they no longer pass against
tool revisions after C1. The r22 claim stays reproducible at its bound revision
`da40bb20f81da125d798f73cd1653655be1255ca` (the r22 driver stages the tool from
`--revision`); the r23 oracle re-expresses all 24 r22 requirements against the new
schema. Before→after for C1 is measured by the r23 oracle only.

### C2 — coverage (FR2 quota/EDQUOT observability; frontier → bounded core), capability, score held 6

New read-only probe `tools/mori-quota-surface.py` (sourced: S077–S084, opened this
round, see lesson23 Gate). `df` capacity percentages cannot see quota exhaustion
(FR2); the probe reports, per path, whether a filesystem quota mechanism is visibly
enabled, visibly disabled, or unknown. It never calls quotactl, `btrfs qgroup`,
`xfs_quota`, `repquota`, mounts, writes, or any privileged interface.

CLI: `--path ABS` (repeatable; default the fleet root `/home/vgpnk/Projects/shokunin`
then `/tmp`), `--fixture FILE` (synthetic mode, no host reads), `--selftest`.
Unknown arguments, relative paths, both `--fixture` and `--path` → exit 2 `QUOTA_SETUP`.

Real-mode inputs only: `/proc/self/mountinfo`, `os.stat(path).st_dev`,
`os.path.realpath(path)`, `os.path.realpath(mount_source)` basename,
directory listings/existence under `/sys/fs/btrfs/*/devices/` and
`/sys/fs/btrfs/<uuid>/qgroups`, and reading `/sys/fs/btrfs/<uuid>/qgroups/mode` if present.

Fixture format `mori-quota-fixture-v1` (JSON object, exact keys):

```json
{"schema":"mori-quota-fixture-v1",
 "mountinfo":"<full /proc/self/mountinfo text>",
 "paths":[{"path":"/abs","realpath":"/abs","st_dev":"MAJ:MIN"}],
 "device_links":{"/dev/mapper/root":"dm-0"},
 "btrfs_sysfs":{"<uuid>":{"devices":["dm-0"],"qgroups":false,"qgroups_mode":null}}}
```

Missing/extra top-level keys, non-absolute paths, malformed st_dev, malformed JSON,
unparseable mountinfo line → exit 2 `QUOTA_SETUP` (no partial verdict).

Mount resolution (per path): parse mountinfo per proc.rst §3.5 (fields 1–6, optional
fields until `-`, then fstype, source, super options); decode octal escapes
(`\040`, `\011`, `\012`, `\134`) in the mount point. Candidate mounts: mount point
equals realpath, or is `/`, or realpath starts with mount point + `/`. Choose the
longest mount point; among equal mount points the **last** line wins. None → `unknown`
basis `no_covering_mount`. If chosen fstype is not btrfs and its major:minor ≠ the
path's st_dev → `unknown` basis `device_mismatch`. For btrfs a mismatch is expected
(per-subvolume anonymous st_dev, S081) and is recorded as `device_check:
"btrfs_subvolume_skipped"`; equal → `device_check: "match"`.

Quota classification (super options = last mountinfo field, comma-split, key = text
before `=`):

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

Output (one JSON object): `schema: "mori-quota-surface-v1"`, `finding_id`,
`exit_code`, `paths: [{path, fstype, mount_point, quota_state, enforcement, basis,
device_check, quota_option_keys, btrfs_qgroups_mode}]` (`fstype`/`mount_point` null when
no covering mount; `quota_option_keys` = sorted quota-related keys only, never values or
other options; `btrfs_qgroups_mode` the mode text or null), `df_covers_quota: false`,
`limits` (fixed boundary text). Never echo mount sources, other options or file names
from option values.

Verdict precedence: setup error → 2 `QUOTA_SETUP`; else any `enabled` → 1
`QUOTA_ENABLED` (positive evidence is never hidden by an unknown sibling); else any
`unknown` → 2 `QUOTA_STATE_UNKNOWN`; else 0 `QUOTA_DISABLED`. `QUOTA_ENABLED` is a
runway-reporting finding (df percentages are insufficient there), not a failure claim.

Limits stated in output and docs: no per-user/group/project limit or usage reading; no
NFS/server-side or overlay/fuse quota; btrfs qgroup presence ≠ any limit set; ext quota
feature in the superblock is unobservable without privileged tools; sysfs/mountinfo
races during enable/disable/remount are not excluded.

Measured (oracle `oracle-quota.py`, sealed cases under `frozen/quota-cases/`): before
(tool absent at entering revision) every sealed case `capability_absent`; after every
sealed case matches exit, finding_id and per-path
(path, fstype, mount_point, quota_state, enforcement, basis) exactly. Real control
(`frozen/c2-expected-real.json`, frozen now from independent host observation): exit 0
`QUOTA_DISABLED`; fleet root → btrfs, mount point `/home`, disabled,
`btrfs_qgroups_dir_absent`, device_check `btrfs_subvolume_skipped`; `/tmp` → xfs,
`/tmp`, disabled, `xfs_noquota_option`, device_check `match`.

## Sequencing and independence

1. This contract + `frozen/c1-*` + `frozen/c2-expected-real.json` land first.
2. Wave 1 (one validated batch): independent fixture-case authors (one case each,
   from this contract + sources, never reading any implementation), source re-openers,
   oracle authors (never reading implementation), a blind candidate implementation in
   an isolated clone, critics/connectors/sentinels/revengers/scribes.
3. L1 seals accepted cases + oracles in a commit; rejected proposals stay with reasons.
4. Only then does any implementation land. Drivers assert the seal commit is an
   ancestor of, and earlier than, the implementation commit.
5. Wave 2 falsifies the integrated revision.

No exploratory claim, no retirement, no stagnation waiver, no promotion, no privacy
clearance, no pin/baseline acceptance, no host remediation.
