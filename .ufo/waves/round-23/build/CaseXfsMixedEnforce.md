# CaseXfsMixedEnforce — C2 fixture case (xfs `prjquota` + `gqnoenforce`)

Seat: `MadoR22-2.CaseXfsMixedEnforce-8` (wave-23 build, C2 coverage capability).
Item: one independent fixture case, derived from `contract.md` §C2 plus the named kernel
sources only. Detection/report only; no production edits, no delegation, no installs,
no builds, no tests, no live host reads.

Artifacts produced:

| Path | Role |
|---|---|
| `.ufo/waves/round-23/cases-proposed/CaseXfsMixedEnforce.json` | the case file (schema `mori-quota-case-v1`) |
| `.ufo/waves/round-23/build/CaseXfsMixedEnforce.md` | this report |

## 1. Scenario under test

One path on one xfs mount whose super options carry **two quota types with different
enforcement**: `prjquota` (project quota, enforced) and `gqnoenforce` (group quota,
accounting only). The case therefore tests the contract's xfs rows against a *mixed*
option set, not against a single-key mount.

## 2. Sources opened (all at upstream tag `v7.2`, `raw.githubusercontent.com/torvalds/linux`)

| Anchor | File | What it backs |
|---|---|---|
| S078 (wave item `SrcXfsShowargs`) | `fs/xfs/xfs_super.c` | xfs mount-option table (`fsparam_flag("prjquota", Opt_prjquota)`, `fsparam_flag("gqnoenforce", Opt_gqnoenforce)`, `fsparam_flag("noquota", Opt_noquota)`, `fsparam_flag("quota", Opt_quota)`, …), the parse cases, and `xfs_fs_show_options()` |
| S077 (wave item `SrcXfsDoc`) | `Documentation/admin-guide/xfs.rst` | user-facing quota mount options and their "accounting enabled, limits (optionally) enforced" semantics |
| S082 (wave item `SrcProcMountinfo`) | `Documentation/filesystems/proc.rst` §3.5 | mountinfo field layout and optional tagged fields |

Supporting code anchor **outside** the S077–S084 range (used only for fixture
realism, and reported as a source gap in §6.4): `fs/proc_namespace.c` — `show_mountinfo()`
prints `%i %i %u:%u ` (mount ID, parent ID, `MAJOR(sb->s_dev):MINOR(sb->s_dev)`), the
mount point via `seq_path_root(..., " \t\n\\")` (the `\040 \011 \012 \134` escape set),
the VFS mount-option field `" ro"/" rw"` + `show_vfsmnt_opts()`, the optional tagged
fields `shared:X` / `master:X` / `propagate_from:X` / `unbindable`, then `" - "`, the
fstype, the device name, and the **super options** as `" ro"/" rw"` + `show_sb_opts()` +
`sb->s_op->show_options()` (i.e. xfs's `xfs_fs_show_options()`).

**S-id mapping note (honesty):** `corpus/SOURCES.md` currently ends at S076; the
S077–S084 ids for this round are not yet written. The mapping I used is
S077=xfs doc, S078=xfs code/`show_options`, S079=btrfs sysfs, S080=btrfs qgroup,
S081=btrfs per-subvolume `st_dev`, S082=proc mountinfo, S083=ext4 doc, S084=tmpfs doc.
This is pinned by the contract's own citation "per-subvolume anonymous st_dev, **S081**"
combined with the wave-1 source-item list (`SrcXfsDoc`, `SrcXfsShowargs`,
`SrcBtrfsSysfs`, `SrcBtrfsQgroup`, `SrcBtrfsGetattr`, `SrcProcMountinfo`,
`SrcExt4Doc`, `SrcTmpfsDoc` — eight items for eight ids). The mapping is an
**[INFERENCE]** until L1/DraftSourceRows assigns the ids; the *content* of my
derivation does not depend on it, only the labels do.

## 3. Derivation (contract row by row)

**Fixture** (verbatim, `mori-quota-fixture-v1`):

```
mountinfo:
  1 0 259:1 / / rw,relatime shared:1 - ext4 /dev/nvme0n1p2 rw,data=ordered
  25 0 0:22 / /proc rw,nosuid,nodev,noexec,relatime shared:5 - proc proc rw
  36 1 253:2 / /data rw,relatime shared:1 - xfs /dev/mapper/data rw,inode64,prjquota,gqnoenforce
paths:      [{path:/data/projects, realpath:/data/projects, st_dev:253:2}]
device_links: {"/dev/mapper/data": "dm-1"}
btrfs_sysfs: {}
```

1. **Mount resolution.** Candidates for realpath `/data/projects`: `/` (root ext4
   line) and `/data` (xfs line). The **longest mount point** wins → `mount_point=/data`,
   `fstype=xfs`. The root ext4 line is present precisely so that an implementation
   that takes the first candidate, or the `/` candidate, or the wrong line fails.
2. **Device check.** fstype is xfs (not btrfs), and the mount line's major:minor
   `253:2` equals the path's `st_dev` `253:2` → no `device_mismatch`;
   `device_check` = `match`. (The contract's btrfs subvolume exemption is not
   involved here — this is the plain non-btrfs path.)
3. **Quota classification.** Super options = last mountinfo field =
   `rw,inode64,prjquota,gqnoenforce`; comma-split keys = `rw`, `inode64`,
   `prjquota`, `gqnoenforce`; `noquota` is **absent**.
   * Contract row *"xfs | any of usrquota,uquota,quota,grpquota,gquota,prjquota,pquota
     and no `noquota` | enabled | enforced | `xfs_quota_option`"* — **matches**
     (`prjquota` present, `noquota` absent).
   * Contract row *"xfs | only \*noenforce keys (uqnoenforce,gqnoenforce,pqnoenforce,
     qnoenforce), no `noquota` | enabled | accounting_only | `xfs_quota_option`"* — does
     **not** match: `prjquota` is a quota key and it is present, so the quota-key set
     is not "only \*noenforce keys".
   → `quota_state=enabled`, `enforcement=enforced`, `basis=xfs_quota_option`.
4. **Verdict precedence.** No setup error; one path is `enabled` → **exit 1**,
   `finding_id = QUOTA_ENABLED` (a runway-reporting finding, not a failure claim).

**Expected block (as written to the case file):**

```json
{"exit": 1, "finding_id": "QUOTA_ENABLED",
 "paths": [{"path": "/data/projects", "fstype": "xfs", "mount_point": "/data",
            "quota_state": "enabled", "enforcement": "enforced",
            "basis": "xfs_quota_option"}]}
```

**Derived auxiliary output fields** (outside the six compared fields, for L1's
oracle cross-check): `quota_option_keys = ["gqnoenforce","prjquota"]` (sorted,
quota-related keys only, no values), `device_check = "match"`,
`btrfs_qgroups_mode = null`, `df_covers_quota = false`.

**Kernel corroboration of the mixed semantics** (`fs/xfs/xfs_super.c`, v7.2):

* `Opt_pquota`/`Opt_prjquota` → `m_qflags |= (XFS_PQUOTA_ACCT | XFS_PQUOTA_ENFD)`
  — project quota **enforced**.
* `Opt_gqnoenforce` → `m_qflags |= XFS_GQUOTA_ACCT; m_qflags &= ~XFS_GQUOTA_ENFD`
  — group quota **accounting only**.
* `xfs_fs_show_options()` renders exactly this as `,prjquota` (when
  `XFS_PQUOTA_ENFD`) and `,gqnoenforce` (when only `XFS_GQUOTA_ACCT`), so the fixture
  string is what the kernel itself would print.
* `Documentation/admin-guide/xfs.rst` v7.2: `pquota/prjquota/pqnoenforce` — "Project
  disk quota accounting enabled and limits (optionally) enforced";
  `gquota/grpquota/gqnoenforce` — "Group disk quota accounting enabled and limits
  (optionally) enforced".

**Cross-check performed.** I re-implemented the contract's mount-resolution and
classification text (my own transcription of §C2 — *not* any candidate
implementation, not the oracle) and ran it over my own fixture: derived
`{exit:1, finding_id:QUOTA_ENABLED, paths:[{…quota_state:enabled,
enforcement:enforced, basis:xfs_quota_option}]}` — identical to the `expected` block.
This confirms internal consistency of the case; it is not evidence about any
implementation.

## 4. Independence statement

* Did **not** read `.ufo/waves/round-23/build/ImplQuota/`, `.scratch/round23/ImplQuota/`,
  or `.ufo/waves/round-23/build/OracleQuota/` (the oracle directory appeared in
  `build/` while I worked; I deliberately left it unread).
* Did **not** read sibling case proposals in `cases-proposed/` (it was empty when I
  wrote; I did not re-read it afterwards).
* Read only: `contract.md`, `corpus/SOURCES.md`, the kernel sources listed above, and
  two sibling *source* reports (`build/SrcExt4Doc.md`, `build/SrcTmpfsDoc.md`) for the
  house convention on how a source row is proposed.
* No live host reads of any kind were performed (this item names none, and the wave
  permits host reads only to seats whose item names them). No installs, no builds,
  no tests, no linters, no background jobs.

## 5. Contract ambiguities found (for L1)

**5.1 — Row precedence is not stated (medium).** The xfs block of the §C2 table is
written as five condition→verdict rows with no "first matching row wins, in listed
order" clause. For a mount carrying *both* a quota key and a noenforce key, rows 2
and 3 overlap semantically: row 2 matches literally (`prjquota` ∈ the quota-key set,
`noquota` absent) and yields `enforced`; a reader that treats row 3 as "a noenforce
key is present" yields `accounting_only`. Both readings are defensible from the text
as written. I chose `enforced` because (a) row 3's word "**only**" restricts the
quota-key set to noenforce keys, which is false here, and (b) the kernel really does
enforce project quota on this mount, so `accounting_only` would understate
enforcement — the FR2-dangerous direction, and contrary to the contract's own
posture that positive evidence is never hidden. **Recommendation:** the contract
should state the matching order explicitly ("first matching row in listed order
wins") before the implementation lands, otherwise `CaseXfsMixedEnforce` and any
`CaseXfsAccountingOnly` case are decided by an unstated precedence.

**5.2 — `enforcement` is per path, but xfs enforcement is per quota type (medium).**
The token set (`enforced` / `accounting_only` / `unknown` / `n/a`) cannot express
"project quota enforced, group quota accounting-only". Reporting `enforced` is
truthful for at least one quota type but a consumer may read it as "all quota types
on this mount are enforced". **Recommendation:** state that `enforced` means "at
least one quota type on this mount is enforced", or add an explicit mixed token;
otherwise the output invites an over-claim that the limits section does not cover.

**5.3 — The `xfs_conflicting_quota_options` row is unreachable for kernel-generated
super options (low, but it changes what the sibling case can prove).**
`xfs_fs_show_options()` emits `,noquota` only when `!(m_qflags & XFS_ALL_QUOTA_ACCT)`,
and every quota key sets at least one ACCT bit. A real xfs mount therefore never
shows `noquota` next to a quota key in the super-options field; that combination can
only appear in a hand-written super-options string. **Recommendation:** the sibling
`CaseXfsConflict` should be labelled explicitly as a synthetic-super-options case,
and the contract should say so, so that "no real host can produce this row" is not
read as a probe defect.

**5.4 — The escape set is not documented in S082 (medium, source-coverage gap).**
The contract requires decoding `\040`, `\011`, `\012`, `\134` in the mount point.
`Documentation/filesystems/proc.rst` §3.5 (v7.2) documents the field layout and the
optional tagged fields but says **nothing** about octal escaping. The escape set is
established by `fs/proc_namespace.c` (`seq_path_root(m, &mnt_path, &p->root, " \t\n\\")`),
which is outside the S077–S084 range named by the contract. **Recommendation:** add
the procfs code source to the round's source set (or narrow the contract's escape
claim to "as produced by procfs"), otherwise S082 cannot back the decode requirement.

**5.5 — `qnoenforce` is user-type only in the kernel (low).** `Opt_qnoenforce` and
`Opt_uqnoenforce` share one case arm (`m_qflags |= XFS_UQUOTA_ACCT`), i.e. the
unprefixed `qnoenforce` sets *user* quota accounting only, not "all types"; and
`Opt_quota` likewise sets `XFS_UQUOTA_ACCT | XFS_UQUOTA_ENFD` (user type), matching
the xfs doc listing `quota` inside the user family (`uquota/usrquota/uqnoenforce/quota`).
The contract's xfs rows treat `quota` and `qnoenforce` as flat tokens, which is fine
for the `enabled`/`accounting_only` verdicts, but a reader could infer that `quota`
means "all quota types". This case does not depend on the distinction (`prjquota`
and `gqnoenforce` are type-explicit), but the contract's wording could be tightened.

**5.6 — Nothing in the contract binds `quota_option_keys` membership (low).**
"quota-related keys only" is not enumerated. For this fixture the natural set is
`{prjquota, gqnoenforce}` (both listed in the contract's own xfs rows); a
strict-literal reading could also include `noquota` when present. Not load-bearing
for the sealed comparison (six fields), but worth pinning before an oracle asserts
on it.

## 6. Residual risk and verification gaps

1. **The `enforced` vs `accounting_only` fork is the whole point of this case.** If
   L1 concludes that row 3 should win whenever any noenforce key is present, this
   case's expected value flips to `{"quota_state":"enabled","enforcement":"accounting_only",
   "basis":"xfs_quota_option"}` (exit and finding_id stay 1 / `QUOTA_ENABLED`). I
   recommend against that reading (see §5.1) but the decision is L1's, and it must be
   made before the case is sealed and before any implementation lands.
2. **S-id labels are provisional** (§2). If DraftSourceRows assigns the eight ids in
   a different order, the `sources` array must be relabelled; the anchors in the
   rationale should survive unchanged (file paths + line-level facts).
3. **The fixture is synthetic.** No host was probed, so `253:2`, `/dev/mapper/data`
   and `/data/projects` are plausible but not observed. That is the intended mode
   (`--fixture`, "no host reads"), but it means this case says nothing about the real
   host's xfs mounts.
4. **Not covered here (sibling items):** `noquota`/disabled, options-absent, device
   mismatch, ext4/tmpfs/btrfs rows, no-covering-mount, escape decoding, optional
   fields, stacked mounts, setup errors. This case deliberately covers exactly one
   contract row pair (xfs row 2 + row 3 boundary).
5. **No implementation was run** (wave rule: no builds/tests in this wave; L1
   measures after integration). The §3 cross-check is a self-consistency check of my
   own transcription of the contract, not a measurement of any candidate.

## 7. Tooling

No tools were installed or updated in this seat: the task needed only file reads,
kernel-source fetches over HTTPS, and one local JSON validation — all covered by the
existing environment (`read`, `bash` with `curl`/`python3` already present). Nothing
to record under the operator tooling directive.

---

# Correction (pre-seal amendment) — appended 2026-10-21

Amendment read in full: `.ufo/waves/round-23/preseal-amendment.md` (C2 final rules
superseding only erroneous/ambiguous original clauses; written before any candidate
was opened). Corrected case authored at
`.ufo/waves/round-23/cases-corrected/CaseXfsMixedEnforce.json` (same id
`CaseXfsMixedEnforce`); the original proposal at
`.ufo/waves/round-23/cases-proposed/CaseXfsMixedEnforce.json` is **byte-unchanged**
(sha256 `6d6bb2a6a15b762cb0d8b326a0346d5bcca90c2362153428a684dabc6a6b0d70` before
and after this correction). No implementation read, no candidate executed, no
delegation.

## C.1 Delta summary: fixture and expected values are unchanged; the derivation is superseded

| Amendment delta | Applies to this case? | Effect |
|---|---|---|
| btrfs: every `btrfs_sysfs` UUID record (including decoys) needs `qgroups_enabled=true` when `qgroups=true`, `null` when `qgroups=false`; enabled basis becomes `btrfs_qgroups_enabled` | **No** | this fixture has no btrfs mount and `btrfs_sysfs` is `{}` — zero UUID records, so no decoy needs the new member and no basis token changes |
| ext2/3/4: always `unknown` / `n/a`; basis `ext_quota_option_unverified` when any quota-related key is present | **No** | this fixture has no ext mount; the ext4 line is the root mount and is not a candidate for `/data/projects` |
| duplicated covering mount point → `unknown` / `n/a` / `ambiguous_overmount`, `fstype=null`, `mount_point=null`, `device_check=not_checked` | **No** | covering mount points for `/data/projects` are `/` (once) and `/data` (once); no covering mount point occurs more than once, so classification proceeds |
| mount resolution / device-check / fixture-hygiene refinements | **Yes, checked** | no behavioural change to this case (see C.2) |

The `expected` block is therefore **identical** to the original proposal:

```json
{"exit": 1, "finding_id": "QUOTA_ENABLED",
 "paths": [{"path": "/data/projects", "fstype": "xfs", "mount_point": "/data",
            "quota_state": "enabled", "enforcement": "enforced",
            "basis": "xfs_quota_option"}]}
```

## C.2 Amendment clauses checked against this fixture

* **XFS precedence (new, explicit):** *"conflict(noquota with ANY quota/enforcement or
  noenforce key), then noquota, then any enforced key, then any accounting-only key,
  else absent."* Super options `rw,inode64,prjquota,gqnoenforce` → step 1 does not fire
  (`noquota` absent), step 2 does not fire, **step 3 fires on `prjquota`** (an enforced
  xfs quota key), step 4 (`gqnoenforce`, accounting-only) is never reached →
  `enabled` / `enforced` / `xfs_quota_option`.
* **"Mixed enforced/noenforce means SOME quota-type enforcement flag is set, not
  all."** This is the explicit statement my §5.1/§5.2 flagged as missing: for this
  mount, project quota is enforced and group quota is accounting-only, and the
  path-level token is `enforced`. **§5.1 (unstated row precedence) and §5.2 (per-path
  vs per-quota-type enforcement) are now resolved by the amendment**, in the direction
  my original derivation took (`enforced`); the residual consumer-facing caution in
  §5.2 stands as a documentation note, not an open contract defect.
* **Empty trailing lines ignored:** the fixture's mountinfo text ends with a newline
  (as real mountinfo does); the trailing empty segment is ignored.
* **Separator and last three fields parsed per chosen line, never file-wide:** this
  line yields fstype `xfs`, source `/dev/mapper/data`, super options
  `rw,inode64,prjquota,gqnoenforce`; the other two lines are parsed independently and
  neither is a candidate for `/data/projects`.
* **Octal decoding of root/mountpoint/source with exactly 040/011/012/134; other
  backslash escapes rejected as QUOTA_SETUP:** this fixture contains no backslash
  escapes, so the rule is not exercised here.
* **Longest component-prefix selection; duplicate covering mount point →
  `ambiguous_overmount`:** longest prefix is `/data` (the root `/` also covers but is
  shorter); no covering mount point repeats, so `fstype`/`mount_point` are not nulled.
* **Device mismatch preempts the filesystem table:** fstype xfs is not btrfs and the
  mount's `253:2` equals the path's canonical `st_dev` `253:2`, so no preemption and
  the path is classified rather than left unknown.
* **Fixture hygiene:** paths nonempty/unique/normalized absolute (`/data/projects`,
  no dot components), `st_dev` canonical decimal `MAJ:MIN`, `device_links` values are
  plain nonempty basenames (`dm-1`), `btrfs_sysfs` is an empty object (no records,
  hence no `qgroups_enabled` members required).
* **Supplementary sealed values for this case:** `device_check` = `match`;
  `quota_option_keys` = `["gqnoenforce","prjquota"]` (sorted, recognized xfs
  quota/noenforce keys only; `inode64` and `rw` are non-quota options and are ignored;
  option values never emitted); qgroups mode = `null` (no btrfs mount).
* **Output tuples:** the original six scored fields are preserved as the denominator;
  the amendment's supplementary assertions (device_check, quota_option_keys,
  qgroups mode, exact allowed keys, no source/uuid/value leakage) are recorded above
  for L1's oracle.

## C.3 Re-derivation under the amendment

I re-transcribed the amendment's mount-resolution, duplicate-covering, device-check and
XFS-precedence clauses (my own transcription; no candidate implementation, no oracle,
no sealed harness) and ran them over the corrected fixture: derived
`{exit:1, finding_id:QUOTA_ENABLED, paths:[{path:/data/projects, fstype:xfs,
mount_point:/data, quota_state:enabled, enforcement:enforced, basis:xfs_quota_option}]}`
— identical to the case's `expected` block. Self-consistency of the case only; no
measurement of any candidate.

## C.4 Items still open after the amendment (for L1)

1. **Escape-set source gap (unchanged).** The amendment mandates decoding
   040/011/012/134 and rejecting other backslash escapes, but S082
   (`Documentation/filesystems/proc.rst` §3.5) documents no escaping at all; the
   behaviour is in `fs/proc_namespace.c` (`seq_path_root(..., " \t\n\\")`), outside the
   S077–S084 range named by the contract. Not resolvable by this seat, and it does not
   affect this case (no escapes in the fixture).
2. **Output-key naming ambiguity.** The contract names the field
   `btrfs_qgroups_mode`; the amendment's supplementary-check wording says
   `qgroups_mode`. The exact-allowed-keys check depends on which name is canonical.
   This case emits `null` under either name, so it does not discriminate, but other
   btrfs cases do.
3. **S-id labels remain provisional** (§2): the amendment states S077–S084 were
   "forward assignments, not existing registry rows", so the `sources` array
   `["S077","S078","S082"]` labels the anchors (xfs doc, `fs/xfs/xfs_super.c`,
   `proc.rst` §3.5) and must be re-checked against the registry rows when they land.
4. **Unchanged from §5.3:** the `xfs_conflicting_quota_options` branch is unreachable
   from kernel-generated xfs super options (`noquota` is printed only when no quota
   ACCT bit is set), so the sibling conflict case remains a synthetic-super-options
   case.

## C.5 Final hashes (sha256)

| File | sha256 |
|---|---|
| `.ufo/waves/round-23/cases-corrected/CaseXfsMixedEnforce.json` (corrected, this correction) | `ed13abb0eabfbbb8dd8c3391d6cc665a939d8b30b60338f08a9b840e14cd44da` |
| `.ufo/waves/round-23/cases-proposed/CaseXfsMixedEnforce.json` (original proposal, untouched) | `6d6bb2a6a15b762cb0d8b326a0346d5bcca90c2362153428a684dabc6a6b0d70` |
| `.ufo/waves/round-23/build/CaseXfsMixedEnforce.md` (this report, before the appended correction section) | `513da2de37efc9169f3b90be79d68b4a634069a3b03763211e5cb9c359cc025d` |

(The report hash above is the pre-append value; the file now also contains §C. Re-run
`sha256sum` after this append for the final report digest.)
