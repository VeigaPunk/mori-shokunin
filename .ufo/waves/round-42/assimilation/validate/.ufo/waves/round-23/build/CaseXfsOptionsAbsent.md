# CaseXfsOptionsAbsent — C2 fixture case for an xfs mount with neither `noquota` nor any quota key

Seat: `MadoR22-2.CaseXfsOptionsAbsent-8` (leaf case author, wave 1). Detection/report
only. Contract read in full at `.ufo/waves/round-23/contract.md` (frozen at lane commit
`4dc80c1be48308075e83af17f15fbfe7e95e6cb8`).

## Deliverable

Exactly one case file, as assigned:

| Item | Value |
|---|---|
| Path | `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/cases-proposed/CaseXfsOptionsAbsent.json` |
| Bytes | 4363 |
| SHA-256 | `7fd4c516706740a87aa2da76f00002f37999fae9ab7624bffd2eb4b764210645` |
| `schema` | `mori-quota-case-v1` |
| `id` | `CaseXfsOptionsAbsent` |
| Fixture schema | `mori-quota-fixture-v1` |

No other file was written by this seat except this report.

## The case in one line

An xfs mount whose super options contain neither `noquota` nor any quota key is
classified `unknown` with basis `xfs_quota_options_absent`; because no path is
`enabled`, the run exits 2 with finding id `QUOTA_STATE_UNKNOWN`.

Expected (the six contract tokens per path, ordered list of one object):

```json
{"exit": 2, "finding_id": "QUOTA_STATE_UNKNOWN",
 "paths": [{"path": "/srv/data", "fstype": "xfs", "mount_point": "/srv/data",
            "quota_state": "unknown", "enforcement": "n/a",
            "basis": "xfs_quota_options_absent"}]}
```

## Derivation (contract §C2 only, no implementation consulted)

1. **Quota key set.** Contract §C2, "Quota classification" table, xfs block:
   - row 1 `noquota` and no quota key → `disabled` / `n/a` / `xfs_noquota_option`
   - row 2 any of `usrquota,uquota,quota,grpquota,gquota,prjquota,pquota`, no `noquota`
     → `enabled` / `enforced` / `xfs_quota_option`
   - row 3 only *noenforce keys (`uqnoenforce,gqnoenforce,pqnoenforce,qnoenforce`), no
     `noquota` → `enabled` / `accounting_only` / `xfs_quota_option`
   - row 4 `noquota` together with any quota key → `unknown` / `n/a` /
     `xfs_conflicting_quota_options`
   - row 5 **neither `noquota` nor any quota key → `unknown` / `n/a` /
     `xfs_quota_options_absent`** ← the only row this fixture satisfies.
2. **Super options of the chosen mount.** Contract: "super options = last mountinfo
   field, comma-split, key = text before `=`". The fixture's `/srv/data` line ends with
   `rw,attr2,inode64,logbufs=8,logbsize=32k,noalign`; the keys are
   `rw, attr2, inode64, logbufs, logbsize, noalign`. No `noquota`, and none of
   `usrquota,uquota,quota,grpquota,gquota,prjquota,pquota` or of
   `uqnoenforce,gqnoenforce,pqnoenforce,qnoenforce`. Rows 1–4 are all excluded, so
   row 5 applies; `quota_state` `unknown`, `enforcement` the table's literal `n/a`,
   `basis` `xfs_quota_options_absent`.
3. **Mount resolution.** Contract: parse per proc.rst §3.5 (fields 1–6, optional fields
   until `-`, then fstype, source, super options); candidates are "mount point equals
   realpath, or is `/`, or realpath starts with mount point + `/`"; longest mount point
   wins; among equal mount points the **last** line wins. The fixture's path is
   `/srv/data` with `realpath` `/srv/data`. Candidates: `/srv/data` (exact match) and
   `/` (root). `/srv/data` is longer, so it wins → `fstype` `xfs`, `mount_point`
   `/srv/data`. No second line mounts on `/srv/data`, so the last-line tie-break is not
   reached. The other lines (`/`, `/proc`, `/sys`, `/home`) are not candidates for this
   realpath, so the presence of an ext4 root, a btrfs `/home`, proc and sysfs in the
   same mountinfo text cannot change the verdict.
4. **Device check precedes classification.** Contract: "If chosen fstype is not btrfs
   and its major:minor ≠ the path's st_dev → `unknown` basis `device_mismatch`." The
   chosen mount is xfs (not btrfs), so the fixture sets the path `st_dev` to the mount's
   own field 3 (`253:2`), making `device_check` `match` and keeping the expected basis
   `xfs_quota_options_absent` rather than `device_mismatch`. This is deliberate: the
   case targets the options-absent row, not the device row.
5. **Verdict precedence.** Contract: setup error → 2 `QUOTA_SETUP`; else any `enabled` →
   1 `QUOTA_ENABLED`; else any `unknown` → 2 `QUOTA_STATE_UNKNOWN`; else 0
   `QUOTA_DISABLED`. There is exactly one path and it is `unknown`, so exit 2 and
   `QUOTA_STATE_UNKNOWN`. `QUOTA_ENABLED` is not reachable here, and the contract's
   "positive evidence is never hidden by an unknown sibling" rule is not exercised.
6. **Fixture shape.** Top-level keys are exactly `schema`, `mountinfo`, `paths`,
   `device_links`, `btrfs_sysfs`; each path object is exactly `path`, `realpath`,
   `st_dev`; `st_dev` is decimal `MAJ:MIN` in the same form as mountinfo field 3;
   all fixture paths are absolute; `device_links` maps `/dev/mapper/*` to `dm-*` names;
   `btrfs_sysfs` maps a uuid to `devices`/`qgroups`/`qgroups_mode`. No malformed line,
   no extra key, no relative path, so the `QUOTA_SETUP` arms are not triggered.

## Fixture text (mountinfo)

```
1 0 259:1 / / rw,relatime shared:1 - ext4 /dev/nvme0n1p2 rw,errors=remount-ro
17 1 0:25 / /proc rw,nosuid,nodev,noexec,relatime shared:5 - proc proc rw
20 1 0:6 / /sys rw,nosuid,nodev,noexec,relatime shared:7 - sysfs sysfs rw
30 1 0:44 / /home rw,relatime shared:14 - btrfs /dev/mapper/root rw,ssd,space_cache,subvolid=5,subvol=/
40 1 253:2 / /srv/data rw,relatime shared:20 - xfs /dev/mapper/data rw,attr2,inode64,logbufs=8,logbsize=32k,noalign
```

Field layout follows proc.rst §3.5 (S082): (1) mount ID, (2) parent ID, (3) major:minor,
(4) root, (5) mount point, (6) mount options, optional `shared:N` fields, `-` separator,
then filesystem type, mount source and super options. Every line is a legal
mountinfo line; the xfs super options carry no quota key and no `noquota`.

## Source anchors relied on

All three were opened by this seat from the pinned upstream raw URLs at tag `v7.2`
(fetched over the network and streamed to stdout; **no file was written to disk** by
this seat). The digests below match the drafted registry rows.

| S-id | Source | Anchor verified by this seat | Digest of fetched bytes |
|---|---|---|---|
| S077 | `Documentation/admin-guide/xfs.rst` (v7.2) | lines 171–185: `noquota` (171–173), `uquota/usrquota/uqnoenforce/quota` (175–177), `gquota/grpquota/gqnoenforce` (179–181), `pquota/prjquota/pqnoenforce` (183–185) — the xfs quota option vocabulary used as the key set | `53bda67b5612a3f2c02820604d05825c9d37addba9855e1d4fba330a516d051c` (22719 B) |
| S078 | `fs/xfs/xfs_super.c` (v7.2) | lines 238–254 in `xfs_showargs`: `,usrquota`/`,uqnoenforce` (238–241), `,prjquota`/`,pqnoenforce` (243–246), `,grpquota`/`,gqnoenforce` (248–251), `,noquota` (253–254) — which option names the kernel can emit, and the reachability finding below | `0a95697dcfcdab8f7ab6ea26fdb941db952db4b73ed93c30d21e40861ed0450c` (72773 B) |
| S082 | `Documentation/filesystems/proc.rst` (v7.2) | section 3.5, lines 1965–1990: field table 1970–1983 (3 major:minor at 1975, 5 mount point at 1977, 6 mount options at 1978, separator `m+1` at 1980, filesystem type `m+2` at 1981, mount source `m+3` at 1982, super options `m+4` at 1983); optional-field list 1988–1993 | `e760f716f8278deefab17a63739033cadc7faee93663c49e76455afaaf40d126` (107560 B) |

`sources` in the case file is exactly `["S077", "S078", "S082"]`.

## Findings and contract ambiguities

**F1 — the xfs "options absent" arm is unreachable in real mode (highest value for L1).**
S078 (`xfs_showargs`, lines 238–254) shows the kernel emits `,noquota` exactly when no
accounting flag is set (`if (!(mp->m_qflags & XFS_ALL_QUOTA_ACCT)) seq_puts(m,
",noquota");`), and otherwise emits one quota key per scope. A kernel-emitted xfs
super-option string therefore always contains either `noquota` or at least one quota
key; "neither" cannot occur on a live mount. Consequences:
- The contract's real control (`/tmp` → xfs, `disabled`, `xfs_noquota_option`) is
  consistent with S078 — a real xfs mount without quota options reports `noquota`.
- The row `xfs_quota_options_absent` is satisfiable only through the synthetic
  `--fixture` mode. The contract does not say so: it lists the row in the same table
  as the real-mode-reachable rows, and the CLI section describes `--fixture` as
  "synthetic mode, no host reads" without marking which table rows are synthetic-only.
  L1 should either annotate the row as fixture-reachable-only or accept that the row
  is a defensive branch.
- This case therefore is a fixture-mode case by construction, and I state that in its
  rationale rather than implying a real mount could look like this.

**F2 — `qnoenforce` in the contract's xfs noenforce key list is never emitted by xfs.**
Contract row 3 lists `uqnoenforce,gqnoenforce,pqnoenforce,qnoenforce`. S078 shows the
kernel emits `uqnoenforce`, `gqnoenforce` and `pqnoenforce` only; there is no
`qnoenforce` in xfs (S077's option list has the same three accounting-only forms). The
superset is harmless for classification (an extra key can only add a match), but it
means row 3 would also classify a super-option string containing the non-existent
`qnoenforce` as `enabled`/`accounting_only`. Non-blocking; noted for exactness.

**F3 — the contract's xfs quota-key list and the kernel's emitted names differ.**
Contract row 2 keys are `usrquota,uquota,quota,grpquota,gquota,prjquota,pquota`;
kernel-emitted names (S078) are `usrquota`, `grpquota`, `prjquota` plus the
`*noenforce` forms. The mount-option spellings in S077 (`uquota`, `gquota`, `pquota`,
`quota`) are *mount inputs*, while S078 shows what is *reported back* in super
options. A probe that reads only mountinfo sees the S078 vocabulary. The union
behaves correctly here because row 3 covers the emitted `*noenforce` forms, but the
split between "input spellings" and "reported spellings" is not stated in the contract
and should be, since the probe reads the reported spelling only.

**F4 — `quota_option_keys` for a path with no quota key is unspecified.** Contract:
"`quota_option_keys` = sorted quota-related keys only". For this fixture the quota-key
set is empty, so the value is `[]` by the obvious reading, but `null` is not excluded.
This does not affect the case's `expected` object (it carries exactly the six
contract-named fields), but the oracle must not compare that field strictly for this
case, or must pin `[]`.

**F5 — `st_dev` comparison form is unspecified.** The fixture format writes
`"st_dev":"MAJ:MIN"` without stating whether the comparison against mountinfo field 3
is numeric or string, nor whether the fixture may use a different numeric radix. I
wrote the fixture's `st_dev` byte-identically to the mount's field 3 (`253:2`,
decimal as the kernel writes it), so string and numeric comparison agree and the
`device_mismatch` arm is not reached. L1 may want the contract to say "decimal
`major:minor`, compared as the exact string".

**F6 — `no_covering_mount` requires a mountinfo without a `/` line.** Contract lists
basis `no_covering_mount` for "no covering mount", but "/" is always a candidate when
present, so the basis is only reachable with a synthetic mountinfo lacking a root
line. Not used by this case (my mountinfo has a root line and the longest match is
`/srv/data`); recorded because it is the same class of issue as F1 — the table mixes
real-mode-reachable and fixture-only arms without marking them.

**F7 — output field name vs case field name.** The probe's output object uses
`exit_code`, while the case format uses `exit` under `expected`. The mapping is
implicit; the oracle owns it. Recorded for L1's seal checklist.

## Bounds, independence and tooling

- **Independence held.** I never opened `.ufo/waves/round-23/build/ImplQuota/`,
  `.scratch/round23/ImplQuota`, `.ufo/waves/round-23/cases-proposed/` peer files, or
  `.ufo/waves/round-23/build/OracleQuota/`. The peer artifacts I did read are
  source-side only: `build/SrcExt4Doc.md`, `build/SrcTmpfsDoc.md` and the scribe's
  `build/DraftSourceRows/rows.md` (the S077–S084 id mapping). The expectation was
  derived from `contract.md` plus the kernel sources named in those rows, re-fetched
  and re-read by this seat.
- **No host probes.** No `/proc` read, no `os.stat`, no `readlink`, no mount or quota
  command, no privileged call, nothing under `/tmp`, no write outside the one assigned
  case file and this report. The only reads outside the lane were the three pinned
  upstream raw file fetches over the network, streamed to stdout; the fetched bytes
  were not written to disk.
- **No VCS mutation**, no `git add`/`commit`, no branch or worktree change; no clone
  was needed because this seat writes no fixture bytes.
- **No tool installs or upgrades** were needed or performed; no pacman/uv/npm/cargo
  transaction, so nothing to record in the tooling channel. The host's pacman pause
  was respected.
- **No tests/builds/linters** were run. The only self-check was an in-memory re-read
  of my own case file (JSON parse, key-set equality against the contract's fixture
  and case formats, and an independent re-implementation of the contract's mount
  resolution and key extraction over my own fixture), which confirmed the chosen
  mount `/srv/data` (xfs, `253:2`), the key set
  `rw,attr2,inode64,logbufs,logbsize,noalign`, and the derived verdict
  `unknown / n/a / xfs_quota_options_absent`, exit 2 `QUOTA_STATE_UNKNOWN`.
- **Carried debt untouched:** the 4 unallowlisted retention hits, original permission
  control RED 11/12, the two unknown historical dispositions, and the blocked baseline
  acceptance are not addressed here; no privacy clearance, no promotion, no baseline
  acceptance, no host remediation is claimed.

---

# Correction (pre-seal amendment) — appended after the original report

Trigger: L1's instruction to read `.ufo/waves/round-23/preseal-amendment.md` and author a
NEW corrected case under `cases-corrected/` **before any candidate inspection or
result**. No candidate was inspected by this seat at any point: the blind
implementation directory and the C2 oracle were never opened, and no candidate output
was seen. The original proposal stays untouched as an unaltered proposal.

## Corrected artifact

| Item | Value |
|---|---|
| Path | `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/cases-corrected/CaseXfsOptionsAbsent.json` |
| Bytes | 5194 |
| SHA-256 | `d54cba9914cf85c4c4036b250b2e8c6dd3401f770e3929f5072c980797e16a58` |
| `schema` / `id` | `mori-quota-case-v1` / `CaseXfsOptionsAbsent` (same id as the proposal) |
| Original proposal digest (re-checked after the correction) | `7fd4c516706740a87aa2da76f00002f37999fae9ab7624bffd2eb4b764210645` — unchanged, 4363 B |

## Delta against the original proposal (exactly one substantive change)

1. **New mandatory fixture member `qgroups_enabled` on the btrfs_sysfs UUID record.**
   The amendment makes `qgroups_enabled` a required member of every btrfs_sysfs UUID
   record (true / false / null) and requires `qgroups` false to pair with
   `enabled=null` and `mode=null`. This fixture's single record is a decoy (its uuid is
   not the queried path's filesystem), so it is the `qgroups` false case: the record is
   now exactly
   `{"devices": ["dm-0"], "qgroups": false, "qgroups_enabled": null, "qgroups_mode": null}`
   — four record keys, none missing, none extra.
2. **Rationale sentence** documenting that the amendment's C2 rules leave this case's
   expectation unchanged and that the only fixture-level requirement touching this file
   is the new `qgroups_enabled` member.

Everything else is byte-identical to the proposal: the `mountinfo` text (5 lines), the
single `paths` entry (`/srv/data`, realpath `/srv/data`, `st_dev` `253:2`), the
`device_links` map, the `expected` block, `scenario`, `id`, `schema` and
`sources` (`["S077", "S078", "S082"]`).

## Amendment clauses checked against this case — effect on the expectation

| Amendment clause (C2 final rules) | Applies to this case? | Effect |
|---|---|---|
| btrfs: qgroups presence = initialized, not enabled; add required `qgroups_enabled`; qgroups false pairs enabled=null/mode=null | Fixture shape only (decoy record) | record updated as above; no expectation change — the queried path is xfs, and the decoy uuid is never classified |
| btrfs bases `btrfs_qgroups_enabled` / `btrfs_qgroups_disabled` / `btrfs_qgroups_enabled_unavailable` replacing the enabled-row basis | No (no queried btrfs path) | n/a |
| ext2/3/4 always unknown/n/a, `ext_quota_option_unverified` when a quota-related key is present | No (no ext path) | n/a |
| Duplicated covering mount point → unknown/n/a/`ambiguous_overmount`, fstype=null, mount_point=null, device_check=not_checked | No — verified the covering mount points for `/srv/data` are exactly `/` and `/srv/data`, each appearing once in the fixture, so the refusal is not triggered | no change |
| Device mismatch preempts the filesystem table; `device_check` mismatch | No — the fixture's `st_dev` is byte-identical to the mount's field 3 (`253:2`), fstype is xfs (not btrfs), so the check yields `match` | no change |
| Mount resolution: ignore empty trailing lines; parse separator and the last three fields per line; octal-decode root/mountpoint/source with exactly 040/011/012/134, reject other escapes | Checked — every fixture line has exactly three fields after the `-` separator, no backslash appears in any root/mountpoint/source, so no `QUOTA_SETUP` and no escape rejection | no change |
| Fixture path rules: nonempty, unique, normalized absolute path/realpath, no dot/dotdot; `st_dev` canonical decimal MAJ:MIN | Checked — `/srv/data` is absolute, normalized, dot-free, unique; `253:2` is canonical decimal with no leading zeros | no change |
| Fixture source resolution via raw decoded source → `device_links` basename → UUID devices list | Checked — `/dev/mapper/root` → `dm-0` matches the decoy uuid's `devices` list (exactly one match), so even if the btrfs path were queried it would be one clean uuid match, not zero/multiple | no change |
| XFS precedence: conflict → noquota → any enforced key → any accounting-only key → else absent | Checked — the super options hold no `noquota` and no quota/enforcement/noenforce key, so the chain still lands on the absent arm: `unknown` / `n/a` / `xfs_quota_options_absent` | **expectation unchanged** |
| tmpfs hardlimit-only keys restricted to the four documented names | No (no tmpfs path) | n/a |
| Output tuples remain the original six scored fields; supplementary checks cover device_check / quota_option_keys / qgroups_mode "where given" | The case's `expected.paths` objects keep exactly the six scored fields (path, fstype, mount_point, quota_state, enforcement, basis), as the case format requires | no change |

For the record, the supplementary values a sealed check would compute for this fixture's
path, if it asks for them: `device_check` `match` (st_dev `253:2` equals the mount's
field 3); `quota_option_keys` `[]` (under the amended rule the list holds `noquota` and
recognized xfs keys only — this super-option string contains none); `btrfs_qgroups_mode`
null (not a btrfs path). None of them is asserted by this case's `expected` object, so
no comparison surface changes.

## Findings carried forward (unchanged, still for L1's attention)

F1 (the `xfs_quota_options_absent` arm is unreachable in real mode, per S078
`xfs_showargs` printing `,noquota` whenever no accounting flag is set), F2
(`qnoenforce` in the contract's noenforce list is never emitted by xfs), F3 (mount-input
versus reported option spellings), F4 (`quota_option_keys` empty-list form), F5
(`st_dev` comparison form), F6 (`no_covering_mount` needs a rootless mountinfo) and F7
(`exit_code` versus `exit` naming) all remain open and unmitigated by this seat; the
amendment resolves none of them, and F1 in particular still argues that the xfs
options-absent row should be annotated as fixture-reachable-only.

## Bounds for the correction

- **No implementation read, no result seen.** `.ufo/waves/round-23/build/ImplQuota/`,
  `.scratch/round23/ImplQuota` and `build/OracleQuota/` were never opened; the
  amendment was applied to the contract text alone, before any candidate existed in my
  view.
- **Writes:** exactly two paths — the authorized `cases-corrected/CaseXfsOptionsAbsent.json`
  and this appended report. The original `cases-proposed/CaseXfsOptionsAbsent.json` was
  not edited (digest re-verified after the correction: unchanged).
- **No tests/builds/linters**; the only self-check was an in-memory re-read of the
  corrected file (JSON parse, key sets against the case and fixture formats, the
  amendment's field-type and normalization rules, the covering-mount-point uniqueness
  check, and an independent re-implementation of the amended mount resolution and key
  extraction) which reproduced the chosen mount `/srv/data` (xfs, `253:2`), the key set
  `rw,attr2,inode64,logbufs,logbsize,noalign`, and the verdict
  `unknown / n/a / xfs_quota_options_absent`, exit 2 `QUOTA_STATE_UNKNOWN`.
- **No host probes, no installs, no VCS mutation, no delegation.**
