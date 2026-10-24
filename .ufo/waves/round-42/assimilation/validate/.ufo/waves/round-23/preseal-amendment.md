# Round23 pre-seal amendment — source/falsification corrections, not result-driven

Original contract.md, c1 requirements/oracle and real controls at4dc80c1 remain
immutable history. This amendment is written before L1 opens any ImplQuota candidate
or runs any C2 candidate. No C2 result has been observed. Original cases remain
unaltered proposals; corrected/additional cases are separately named and sealed.
Original source IDs S077–S084 were forward assignments, not existing registry rows;
registry and lesson Gate land before sourced knowledge admission.

## C1 bounded clean cutover

Same target: original26 requirements (R25 only red before), alias8→0, schema v2,
unchanged arithmetic/identities/exit/finding behavior. Correct original consequences:
r22's driver runs its checkout's tool, NOT a tool staged from --revision. Reproduce
r22 only in a checkout of da40bb2. Removing a key does NOT fail its subset-key
whitelist. R02/R11/R12, five refinement checks and expected-real's old-key comparison
are the actual breakages on the new API; historical r22 bytes stay immutable.

Freeze an additional code-bound guard before implementation: final production source
must equal the entering source SHA0795bac9… after EXACTLY these two transformations:
SCHEMA='mori-retention-reconciliation-v1' → …-v2, and deletion of the single
`'raw_unallowlisted':len(unallowed),` producer fragment. No other source byte may
change. This is a complete syntactic no-other-behavior-delta constraint for this
mechanical cutover, not a substitute for arbitrary future semantic changes. A source
mutant adding/removing/changing any other code must fail the guard. Output comparison
independently checks identical object key sets/values for every before/after arm,
except schema, removed key, tool_sha256 and argv (tool location differs), and verifies
selftest output schema/absence. Original26 plus these supplementary guards remain
separately reported, never silently redefining the original26 denominator.

## C2 final rules superseding only erroneous/ambiguous original clauses

- ext2/3/4: quota_state ALWAYS unknown, enforcement n/a. If any quota-related option
  key is present use basis `ext_quota_option_unverified`; otherwise retain
  `ext_quota_superblock_unobservable`. Mount option hints/replay settings do not prove
  runtime accounting enabled. S083 explicitly says plain quota flags are ignored.
- btrfs: qgroups directory presence means INITIALIZED, not enabled. Add required
  fixture member `qgroups_enabled` to each btrfs_sysfs UUID record: true/false/null.
  qgroups false must pair with enabled=null/mode=null. Present plus enabled=true →
  enabled/unknown/`btrfs_qgroups_enabled`; present plus enabled=false → disabled/n/a/
  `btrfs_qgroups_disabled`; present plus enabled=null (unreadable/invalid enabled)
  → unknown/n/a/`btrfs_qgroups_enabled_unavailable`. Absent dir retains disabled/n/a/
  `btrfs_qgroups_dir_absent` only on a successful parent inspection. Real mode reads
  qgroups/enabled first (exact0/1), never reads mode unless enabled is1. Mode remains
  informational, only qgroup/squota accepted; unavailable/other yields null, not raw
  text. A parent sysfs permission/listing error is unknown, NEVER absent/disabled.
- Mount resolution: ignore empty trailing lines. Parse separator and the last THREE
  fields of EACH chosen line, never file-wide. Octal-decode root, mountpoint and
  source with exactly040/011/012/134; reject other backslash escapes as QUOTA_SETUP.
  Longest component-prefix selection remains. However if ANY covering mountpoint
  occurs more than once, refuse classification as unknown/n/a/`ambiguous_overmount`,
  fstype=null,mount_point=null, device_check=not_checked. Do not guess stack order
  from line order or reusable IDs. This conservatively handles covering ancestor
  overmounts too. Parent-ID graph resolution is explicitly deferred, not fabricated.
- Device mismatch PREEMPTS the filesystem table: unknown/n/a/device_mismatch;
  device_check=mismatch. Btrfs skips equality only when stat major is0; nonzero
  btrfs stat major mismatching the mount → device_mismatch. Equal → match. No cover
  uses fstype=null,mountpoint=null, device_check=not_checked.
- Fixture source resolution: lookup RAW decoded source in device_links; use its
  mapped basename when present, otherwise basename(source). Compare that basename
  against UUID devices lists. Zero/multiple UUID matches remains unknown.
- Paths nonempty, unique, normalized absolute path/realpath (no dot/dotdot components);
  st_dev canonical decimal MAJ:MIN (no signs or leading zeros except0). Unknown case
  metadata never enters tool output. UUID keys canonical UUIDs, devices and mapped
  values plain nonempty basenames, no slashes/control chars. qgroups fields have exact
  bool/bool-or-null/mode-or-null types. Missing/extra record keys setup. Unknown
  nonquota super options ignored, quota option VALUES never emitted.
- XFS precedence: conflict(noquota with ANY quota/enforcement or noenforce key),
  then noquota, then any enforced key, then any accounting-only key, else absent.
  Mixed enforced/noenforce means SOME quota-type enforcement flag is set, not all.
  quota_option_keys includes noquota and recognized xfs keys only, sorted.
- tmpfs: preserve quota/usrquota/grpquota and the FOUR documented
  usrquota_block_hardlimit/usrquota_inode_hardlimit/grpquota_block_hardlimit/
  grpquota_inode_hardlimit keys only. Arbitrary suffix `_hardlimit` is NOT sufficient.
  Hardlimit-only inputs are defensive synthetic cases; kernel normally also emits an
  active quota flag. `enforced` describes mechanism flags, never a nonzero limit.
- ext quota-related vocabulary adds noquota and jqfmt to the original keys, but
  classification remains unknown. For unsupported/btrfs fstype quota_option_keys=[]
  (btrfs mechanism is sysfs, not options). An unstatable real path/setup read error
  produces code2 QUOTA_SETUP, error a fixed token only, paths=[], no input text echoed.
- Output tuples remain the original six scored fields; supplementary sealed checks
  additionally verify device_check, quota_option_keys and qgroups_mode where given,
  exact allowed keys, no option-value/source/uuid leakage, and schema/exit consistency.
  Preserve original six-field denominator separately from supplementary assertions.

## Boundary and scope

Input fence excludes fstab, mount units, Snapper/config, superblocks, quotactl,
quota commands and remediation. Default root+/tmp only; other explicit paths are
operator-pinned runway targets. realpath/stat can trigger automount or block on remote
filesystems; no guarantee of effect-free resolution on arbitrary paths. Snapshot
races, btrfs-on-btrfs association, per-ID limits/usage, causes and EDQUOT attribution
remain unknown. QUOTA_DISABLED is not a capacity/health verdict: ENOSPC can coexist.
All quota configuration/diagnosis belongs to tsukuroi/operator.

## Seal proof

Require SEAL != REV and strict SEAL ancestor of REV; entering reconciler unchanged
and quota production path ABSENT at SEAL. Seal all oracles, driver, original proposals,
accepted/changed case files and decisions, dependencies (r22 builder/requirements)
and manifests. Run only committed seal copies of harnesses; compare measured working
copies to their committed bytes. Hash every frozen dependency. Git timestamps are
corroboration, not proof of no private earlier measurement. L1 did not open the blind
candidate before seal; preserve proposals/rejections, do not claim outside authorship.

## Final pre-seal clarifications (same source-review stage, no candidate/result read)

The C1 guard is a byte-exact SOURCE constraint, not a semantic proof. Its fixed
target hash/mode/transforms are frozen in `frozen/c1-source-delta.json`. Replay
before/after tools against the SAME fixture instances so argv, receipt digests
and revisions match; compare schema and removed alias specially, pin tool_sha256
to each fixed source hash. Do not normalize argv or other provenance away.
The docs cutover is mandatory in SKILL and the r22 knowledge note.

C2 additionally refuses when the chosen mount's parent ID is present in the
snapshot but is not the ID of the longest strictly-shorter covering mount.
Use unknown/n/a/ambiguous_overmount with null fstype/mountpoint and not_checked
device_check. This catches a new mount on a plain ancestor directory hiding an
older nested mount without any repeated mountpoint; a missing parent ID remains
unknown topology but does not trigger this extra refusal. Root has no shorter
cover. No existing case expectation changes beyond the already-corrected stack.

On no-cover/ambiguous/device-mismatch preemption, quota_option_keys=[] and
btrfs_qgroups_mode=null. `btrfs_qgroups_mode` is the canonical OUTPUT spelling;
fixture input keeps `qgroups_mode`. `enforcement` uses literal string n/a.
For initialized-but-disabled/unreadable qgroups, fixture qgroups_mode must be null.
The amended fixture schema remains v1 within this not-yet-shipped round; ORIGINAL
proposals are preserved rejected old-shape evidence, not valid final inputs.
Supplementary checks use separately frozen metadata, never insert keys into the
independent six-field primary expectations. No unscored claim for metadata.

## Real-mode safety correction before seal

S079's mode reader ASSERTs enabled. Reading enabled1 and then mode can race a
concurrent quota disable, so enabled-first alone does not make that read safe.
SentinelProbe's source review agrees. Real mode therefore NEVER reads qgroups/mode
and emits btrfs_qgroups_mode=null as intentionally unobserved, not mode-absent.
Fixture mode still projects validated qgroup/squota metadata; all independent
primary/supplementary fixture targets and the frozen default real control remain
unchanged. The visible enabled claim reads only the non-asserting enabled attribute.
Original v1/v2 candidate sources remain unexecuted rejected evidence.
