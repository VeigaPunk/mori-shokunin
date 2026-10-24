# CaseEscapedSpace — C2 fixture case (mori round 23, wave 1)

Seat: `MadoR22-2.CaseEscapedSpace-8` · role: reviewer (case author) · lane: leaf, no dispatch.

## Deliverable

- Case file (the only file this seat wrote besides this report):
  `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/cases-proposed/CaseEscapedSpace.json`
  — schema `mori-quota-case-v1`, id `CaseEscapedSpace`, one `mori-quota-fixture-v1` object,
  expected exit `1` / `QUOTA_ENABLED`, two expected paths.
- No production file, no other case file, no `.scratch` write, no host probe beyond the
  permitted `/proc/self/mountinfo` read, no privileged or mutating command, no VCS mutation.
- No tool was installed or updated by this seat, so there is no tool/version/channel record
  to report.

## Independence statement

The expectation was derived only from `.ufo/waves/round-23/contract.md` §C2 (read in full)
and the named kernel sources S077–S084 as registered in
`.ufo/waves/round-23/build/DraftSourceRows/rows.md` and read from the wave's fetched
copies under `.scratch/round23/src/` (`Documentation_filesystems_proc.rst`,
`Documentation_admin-guide/xfs.rst`, `fs_xfs_xfs_super.c`).

I did **not** read `.ufo/waves/round-23/build/ImplQuota/`, any
`.scratch/round23/ImplQuota` clone, `build/OracleQuota/`, or peers' files in
`cases-proposed/`. No host quota state was read.

## Scenario

A mount point whose path contains a space. The kernel writes such a mount point into
`/proc/self/mountinfo` with the space octal-escaped as `\040`; the probe must decode it
before comparing it against the requested path's realpath. Two paths are probed:

- `/srv/my data/sub dir` — under the escaped-space mount (expected **enabled/enforced**)
- `/srv/plain` — under the shorter `/srv` mount (expected **disabled**)

The case is discriminating: if the octal escape is not decoded, the only covering mount
for the first path is `/srv` (`noquota` → disabled) and the run would exit `0`
`QUOTA_DISABLED` instead of `1` `QUOTA_ENABLED`.

## Fixture shape (all values synthetic; nothing was observed on this host)

| element | value | why |
|---|---|---|
| mountinfo line 1 | `26 33 0:24 / /proc rw,… shared:5 - proc proc rw` | realistic non-candidate line (proc.rst §3.5 field layout) |
| mountinfo line 2 | `33 2 0:30 /@ / rw,noatime shared:1 - btrfs /dev/mapper/root rw,…` | realistic `/` btrfs root; a candidate for every path but never the longest match here; gives `device_links`/`btrfs_sysfs` a purpose |
| mountinfo line 3 | `42 33 0:44 / /srv rw,relatime shared:12 - xfs /dev/mapper/srv rw,inode64,logbufs=8,logbsize=256k,noquota` | shorter xfs candidate with `noquota` |
| mountinfo line 4 | `43 33 0:45 / /srv/my\040data rw,relatime shared:13 - xfs /dev/mapper/data rw,inode64,usrquota,attr2` | the escaped-space mount; field 5 written `/srv/my\040data` |
| path 1 | `/srv/my data/sub dir` (realpath identical), `st_dev` `0:45` | under the decoded mount point; `st_dev` equals that mount's major:minor |
| path 2 | `/srv/plain` (realpath identical), `st_dev` `0:44` | contrast path; only `/` and `/srv` cover it |
| `device_links` | `/dev/mapper/root`→`dm-0`, `/dev/mapper/srv`→`dm-1`, `/dev/mapper/data`→`dm-2` | device basenames for the mount sources (contract fixture format) |
| `btrfs_sysfs` | uuid `8f3c1d2e-…` → `devices:["dm-0"]`, `qgroups:false`, `qgroups_mode:null` | the `/` btrfs filesystem; not the longest match for either path, so it cannot influence the verdict |

## Derivation (contract §C2, step by step)

1. **Mountinfo parsing** — contract: *"parse mountinfo per proc.rst §3.5 (fields 1–6,
   optional fields until `-`, then fstype, source, super options); decode octal escapes
   (`\040`, `\011`, `\012`, `\134`) in the mount point."*
   Each fixture line has the field layout of proc.rst §3.5 (S082, field table 1970–1983):
   field 3 `major:minor`, optional fields after field 6, the `-` separator, then
   filesystem type, mount source and super options. Field 5 of line 4 is
   `/srv/my\040data`, which decodes to `/srv/my data`.
2. **Mount resolution** — contract: *"Candidate mounts: mount point equals realpath, or is
   `/`, or realpath starts with mount point + `/`. Choose the longest mount point; among
   equal mount points the last line wins."*
   - realpath `/srv/my data/sub dir`: candidates `/` (line 2), `/srv` (line 3) and
     `/srv/my data` (line 4, since the realpath starts with `/srv/my data/`). Longest wins
     → **mount_point `/srv/my data`**, fstype `xfs`, source `/dev/mapper/data`, super
     options `rw,inode64,usrquota,attr2`.
   - realpath `/srv/plain`: candidates `/` and `/srv` only (`/srv/my data` is not a prefix
     of `/srv/plain`) → **mount_point `/srv`**, fstype `xfs`, super options
     `rw,inode64,logbufs=8,logbsize=256k,noquota`.
   - The "last line wins" tie-break is never needed: no two lines share a mount point.
3. **Device check** — contract: *"If chosen fstype is not btrfs and its major:minor ≠ the
   path's st_dev → `unknown` basis `device_mismatch` … equal → `device_check: "match`"*.
   Path 1: chosen fstype is xfs and mount major:minor `0:45` equals `st_dev` `0:45` →
   match. Path 2: `0:44` equals `0:44` → match. Neither path enters the mismatch branch,
   so no path is forced to `unknown`.
4. **Quota classification** — contract table rows for xfs:
   - path 1, super options contain `usrquota` and no `noquota` → quota_state `enabled`,
     enforcement `enforced`, basis `xfs_quota_option`.
   - path 2, super options contain `noquota` and no quota key → quota_state `disabled`,
     enforcement `n/a`, basis `xfs_noquota_option`.
   `usrquota` is a kernel-emitted super-option key (S078: `xfs_fs_show_options` prints
   `,usrquota` on `XFS_UQUOTA_ENFD`, `,uqnoenforce` on `XFS_UQUOTA_ACCT`, and `,noquota`
   only when no accounting flag is set), and `noquota` "forcibly turns off all quota
   accounting and enforcement" (S077). The two xfs lines are therefore internally
   consistent kernel output.
5. **Verdict precedence** — contract: *"else any `enabled` → 1 `QUOTA_ENABLED` (positive
   evidence is never hidden by an unknown sibling); else any `unknown` → 2
   `QUOTA_STATE_UNKNOWN`; else 0 `QUOTA_DISABLED`."*
   One path is `enabled` → **exit `1`, finding_id `QUOTA_ENABLED`**, even though the
   sibling path is `disabled`.

## Expected output (as written into the case file)

```
exit 1, finding_id QUOTA_ENABLED
paths[0] /srv/my data/sub dir  xfs  /srv/my data  enabled  enforced  xfs_quota_option
paths[1] /srv/plain            xfs  /srv          disabled n/a       xfs_noquota_option
```

The `expected.paths` objects carry exactly the six contracted keys (`path`, `fstype`,
`mount_point`, `quota_state`, `enforcement`, `basis`) and use only contract tokens
(`enabled`/`disabled`/`unknown`, `enforced`/`accounting_only`/`n/a`/`unknown`,
`xfs_quota_option`/`xfs_noquota_option`).

## Verification performed by this seat

JSON well-formedness and key-set conformance of my own file only: parsed the file, checked
the top-level key set (`schema`, `id`, `scenario`, `fixture`, `expected`, `rationale`,
`sources`), the fixture key set (`schema`, `mountinfo`, `paths`, `device_links`,
`btrfs_sysfs`), the expected key set (`exit`, `finding_id`, `paths`), and the six-key
shape of each expected path object. I additionally re-implemented the contract's stated
mount-resolution and device-check rules against my own fixture **in memory** (no file
written, no candidate implementation involved) and confirmed they select
`/srv/my data` (xfs, `0:45`) and `/srv` (xfs, `0:44`) respectively, matching the expected
values above. No build, test, linter, formatter or smoke run was executed (forbidden in
this wave); L1 measures after integration.

## Sources relied on

- **S082** — `Documentation/filesystems/proc.rst` §3.5 (field table 1970–1983): the
  mountinfo field layout used to locate mount point, filesystem type, mount source and
  super options.
- **S077** — `Documentation/admin-guide/xfs.rst` (`noquota` 171–173; `uquota/usrquota/
  uqnoenforce/quota` 175–177): `noquota` forcibly turns off quota accounting and
  enforcement; `usrquota` enables user quota accounting with limits optionally enforced.
- **S078** — `fs/xfs/xfs_super.c` (`xfs_fs_show_options`, quota emission 238–254): which
  quota option names the kernel actually prints into the super-option string, and that
  `noquota` is printed only when no accounting flag is set (so the two fixture xfs lines
  are mutually exclusive and kernel-consistent).

Not relied on: S079, S080, S081 (btrfs sysfs/qgroup/anonymous-st_dev — the btrfs mount in
this fixture is never selected), S083 (ext4), S084 (tmpfs).

## Contract ambiguities found (reported, not resolved by fiat)

1. **Output form of `mount_point` is not stated.** The contract mandates decoding the
   octal escapes "in the mount point" for parsing and comparison, and the comparison is
   against a realpath containing a literal space, so only the *decoded* form can ever
   match. The contract never says whether the `mount_point` field in the **output**
   carries the decoded (`/srv/my data`) or the raw (`/srv/my\040data`) text. I chose
   decoded, as it is the only form consistent with the mandated matching rule and with the
   contract's own rule that the output `path` echoes the given path (the given path here
   contains a literal space). L1 should confirm this in the frozen case/oracle so the
   expectation is not an implementation-private choice.
2. **The escape-decoding rule is under-sourced by S077–S084.** The contract attributes the
   parse to "proc.rst §3.5", but that section documents only the field layout; it contains
   no statement about octal escaping of the mount point (no occurrence of `\040` in the
   section — the file's only `\040` occurrence is in the unrelated smaps example at line
   705). The escape behaviour is a kernel seq_file/mangle property (outside S077–S084).
   The rule is nonetheless fully determinate because the contract states the escape set
   (`\040`, `\011`, `\012`, `\134`) explicitly, so my expectation does not depend on the
   missing anchor; only the *provenance* of the rule is thinner than the contract's
   phrasing implies. Recommended L1 action: register the seq_file escape source alongside
   S082, or state in the contract that the escape set is contract-fixed rather than
   source-derived.
3. **Root field (field 4) escaping is unspecified.** The contract scopes decoding to the
   mount point only, while the kernel escapes the `root` field as well (S082 shows
   btrfs roots such as `/@`). My fixture keeps every root field escape-free (`/`, `/@`),
   deliberately, so the case does not depend on an unstated rule.
4. **`enforcement` for a disabled filesystem is `n/a`**, per the contract table's
   `disabled | n/a | …` rows. This is read literally; note that the table's `unknown`
   rows also use `n/a` while btrfs-`enabled` uses `unknown` as an enforcement token, so
   the `enforcement` and `quota_state` token spaces overlap by design.

## Residual risk / verification gaps

- If the oracle compares the output `mount_point` as the raw escaped text, this case's
  `paths[0].mount_point` expectation would need to be `/srv/my\040data` instead of
  `/srv/my data`. This is the single ambiguity with a plausible divergent expectation; it
  is item 1 above and is L1's call at seal time.
- The case exercises only the xfs rows of the classification table; it is one of several
  xfs cases in this wave, so overlap with `CaseXfsUsrquota`-style seats is expected and
  intentional — this case's distinctive contribution is the `\040` decoding path and the
  longest-match interaction with it.
- No test, build or oracle execution was performed by this seat (forbidden in this wave);
  L1 measures after integration.

---

# Correction appended under `.ufo/waves/round-23/preseal-amendment.md` (round 23, pre-seal)

Seat: `MadoR22-2.CaseEscapedSpace-8` · same seat, no delegation · no implementation read,
no test run, no candidate opened.

## What changed

A **new** corrected case was authored at
`/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/cases-corrected/CaseEscapedSpace.json`
(same `id` = `CaseEscapedSpace`, same `schema` = `mori-quota-case-v1`).
The original proposal
`.ufo/waves/round-23/cases-proposed/CaseEscapedSpace.json` is **untouched and unaltered**
(sha256 `dccf734c088e5f2d2bae8d22ac0f3c89af21e40a888b21710c0c1a1e0d7bc409`, still without
the `qgroups_enabled` member).

### Delta 1 — `btrfs_sysfs` record gains `qgroups_enabled` (the only fixture edit)

Amendment: *"Add required fixture member `qgroups_enabled` to each btrfs_sysfs UUID
record: true/false/null. qgroups false must pair with enabled=null/mode=null."*

The single UUID record in this fixture is a **decoy** (the btrfs `/` mount never wins the
longest match for either probed path):

```json
"8f3c1d2e-5b6a-4c7d-9e0f-1a2b3c4d5e6f": {
  "devices": ["dm-0"], "qgroups": false, "qgroups_enabled": null, "qgroups_mode": null
}
```

`qgroups=false` → `qgroups_enabled=null` and `qgroups_mode=null`, exactly the pairing the
amendment mandates. Record keys are now exactly `devices`, `qgroups`, `qgroups_enabled`,
`qgroups_mode` (no extra keys).

### Delta 2 — btrfs enabled-basis rename: **not applicable to this case**

Amendment: *"Present plus enabled=true → enabled/unknown/`btrfs_qgroups_enabled`."*
No btrfs mount is selected for either path in this case, so no expected basis here is a
btrfs basis and the rename changes nothing. The corrected file keeps
`btrfs_qgroups_dir_absent` **out** of the expectations entirely.

### Delta 3 — ext → `ext_quota_option_unverified`: **not applicable**

No ext2/ext3/ext4 mount is in this fixture; both expected paths are xfs.

### Delta 4 — duplicated covering mountpoint → `ambiguous_overmount`: **not applicable**

Amendment: *"if ANY covering mountpoint occurs more than once, refuse classification as
unknown/n/a/`ambiguous_overmount`, fstype=null, mount_point=null, device_check=not_checked."*
Covering mountpoints here are `/` (line 2), `/srv` (line 3) and `/srv/my data` (line 4,
decoded) for path 1, and `/` plus `/srv` for path 2 — **each occurs exactly once** in the
mountinfo, so no overmount refusal is triggered and the classification stands.

### Delta 5 — explicit re-derivation under the amendment's other changed clauses

- *"Parse separator and the last THREE fields of EACH chosen line, never file-wide."* Each
  fixture line ends `… - <fstype> <source> <super options>`; fstype/source/super options
  are therefore read per line.
- *"Octal-decode root, mountpoint and source with exactly 040/011/012/134; reject other
  backslash escapes as QUOTA_SETUP."* The only escape present is `\040` in the mount point
  of line 4 → `/srv/my data`; the root fields (`/`, `/@`) and the sources contain no
  backslash, so no line is rejected as `QUOTA_SETUP`.
- *"ignore empty trailing lines"* — the fixture's mountinfo ends with a newline; the
  resulting empty tail line is ignored, not parsed.
- *"Device mismatch PREEMPTS the filesystem table … Equal → match."* Both chosen fstypes are
  xfs with `major:minor == st_dev` (`0:45`/`0:45`, `0:44`/`0:44`), so the filesystem table
  applies and no path becomes `unknown`.
- *"XFS precedence: conflict(noquota with ANY quota/enforcement or noenforce key), then
  noquota, then any enforced key, then any accounting-only key, else absent."* Path 1's
  super options `rw,inode64,usrquota,attr2` contain the enforced key `usrquota` and no
  `noquota` → enabled/enforced/`xfs_quota_option`. Path 2's super options
  `rw,inode64,logbufs=8,logbsize=256k,noquota` contain `noquota` and no quota key →
  disabled/n/a/`xfs_noquota_option`. No conflict and no mixed enforced/noenforce case
  arises.
- Fixture metadata rules: both paths are nonempty, unique, normalized absolute paths with
  no dot/dotdot components; both `st_dev` values are canonical decimal `MAJ:MIN`; the
  single UUID key is canonical; `devices` and the `device_links` values are plain nonempty
  basenames without slashes or control characters.
- Verdict precedence is unchanged by the amendment: one path is `enabled` → exit `1`,
  `finding_id` `QUOTA_ENABLED`.

### Unchanged expectation

```
exit 1, finding_id QUOTA_ENABLED
paths[0] /srv/my data/sub dir  xfs  /srv/my data  enabled  enforced  xfs_quota_option
paths[1] /srv/plain            xfs  /srv          disabled n/a       xfs_noquota_option
```

The original six scored fields per path are unchanged; the corrected file adds no
supplementary keys to the expected path objects.

## Residual ambiguity after the amendment

Ambiguity 1 of the original report (raw vs decoded form of the output `mount_point`) is
**narrowed but not closed**: the amendment now scopes octal decoding explicitly to
*"root, mountpoint and source"* and mandates component-prefix selection, so the decoded
form is the value the matcher works with, but the amendment still does not state whether
the emitted `mount_point` string is the decoded text. The corrected case keeps
`/srv/my data` (decoded) for the same reason as before. This remains L1's seal-time call.

Ambiguity 2 of the original report (the escape rule being under-sourced by S077–S084) is
unchanged: the amendment states the escape set explicitly, so the expectation stays
determinate, but no S-id in S077–S084 documents the kernel's escaping behaviour.

## Hashes (sha256)

- `cases-proposed/CaseEscapedSpace.json` (original, **unaltered**):
  `dccf734c088e5f2d2bae8d22ac0f3c89af21e40a888b21710c0c1a1e0d7bc409`
- `cases-corrected/CaseEscapedSpace.json` (new corrected case):
  `8340738a509e474a94a815637e66b407dfb60c6449511e52db55296d844abeea`

Both computed over the exact bytes on disk at the time of writing.
