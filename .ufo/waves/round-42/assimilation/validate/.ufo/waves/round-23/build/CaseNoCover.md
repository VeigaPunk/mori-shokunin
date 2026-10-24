# CaseNoCover — C2 fixture case: no `/` mount and no mount covering the path

Seat: `MadoR22-2.CaseNoCover-8` (leaf case author, wave 23 build wave).
Contract: `.ufo/waves/round-23/contract.md` (frozen at lane commit
`4dc80c1be48308075e83af17f15fbfe7e95e6cb8`), read in full.
Case file written: `.ufo/waves/round-23/cases-proposed/CaseNoCover.json` (one file, one
case; 5365 bytes).

## Independence

- Derivation sources: `contract.md` §C2 only, plus the pinned kernel doc
  `Documentation/filesystems/proc.rst` at tag `v7.2` §3.5 (the S082 row), fetched
  read-only over HTTPS.
- **Not** opened: `.ufo/waves/round-23/build/ImplQuota/`,
  `.scratch/round23/ImplQuota`, `.ufo/waves/round-23/build/OracleQuota/` (and
  `OracleQuota.md`), `.ufo/waves/round-23/cases-proposed/*` (sibling case files), and
  no candidate implementation of `tools/mori-quota-surface.py` (which does not exist at
  this revision). No sibling case's *expectation* was read.
- Disclosed incidental exposure: one repository-wide `grep` over
  `.ufo/waves/round-23/build/` (run to locate the S-id → source mapping) printed short
  fragments of sibling reports (`CaseBtrfsUnmapped.md`, `CaseUnsupported.md`,
  `CaseXfsMixedEnforce.md`, `CaseBtrfsSquota.md`, `CaseTmpfsHardlimit.md`). Those
  fragments were S-id citations and source-anchor lines for *other* scenarios (btrfs
  device unmapped, unsupported fstype, xfs mixed enforcement, tmpfs hardlimit); none
  covered the no-cover branch, and the expectation below was fixed against the
  contract text before those fragments were inspected. The S-id mapping used here
  (`S082` = proc.rst) was independently confirmed from
  `.ufo/waves/round-23/build/DraftSourceRows/rows.md` and from the contract's own
  `S081` = per-subvolume anonymous `st_dev` (i.e. `fs/btrfs/inode.c`) citation.
- No tool install or upgrade was needed or performed (no new tooling; the only network
  fetch was the pinned kernel doc). No live host probe, no privileged command, no
  `quotactl`/`btrfs`/`xfs_quota`/`repquota`/`mount` call, no `/tmp` write, no fleet-root
  write, no VCS mutation. Writes: this report and the one assigned case file.

## The case in one line

`mountinfo` carries no root `/` mount line and no mount point that covers the queried
path, so mount resolution finds no candidate mount.

Fixture (`mori-quota-fixture-v1`, exact five top-level keys per contract lines 82–90):
six parseable mountinfo lines with mount points `/proc`, `/dev`, `/sys`, `/tmp`,
`/srv/quota`, `/home` — **no line with mount point `/`** — one path
`/srv/quota-probe/data` (realpath identical, `st_dev` `259:2`), `device_links`
`{"/dev/mapper/root": "dm-0"}`, and one btrfs sysfs uuid listing `dm-0` with
`qgroups: false`, `qgroups_mode: null`.

Expected: exit **2**, finding_id **`QUOTA_STATE_UNKNOWN`**, one path
`{path: "/srv/quota-probe/data", fstype: null, mount_point: null, quota_state: "unknown",
enforcement: "n/a", basis: "no_covering_mount"}`.

## Derivation (contract line references are from `contract.md` as frozen)

**1. Fixture well-formedness (lines 82–93).** The fixture has exactly the five
top-level keys `schema`, `mountinfo`, `paths`, `device_links`, `btrfs_sysfs`; the one
path is absolute; `st_dev` is `259:2`, a well-formed `MAJ:MIN`; the JSON parses. Each
mountinfo line carries fields 1–6, zero or more optional tagged fields (`shared:N`),
the `-` separator, then fstype, source and super options — the layout of proc.rst §3.5
(field table, lines 1973–1983: `major:minor` at 1975, separator at 1980, filesystem
type at 1981, mount source at 1982, super options at 1983; example line 1970
`36 35 98:0 /mnt1 /mnt2 rw,noatime master:1 - ext3 /dev/root rw,errors=continue`).
Therefore none of the setup-error conditions on line 92–93 fires: this is a verdict
case, not a `QUOTA_SETUP` case.

**2. Mount resolution (lines 95–103).** Candidates are mounts whose mount point equals
the realpath, is `/`, or is a prefix of the realpath followed by `/`. Against the
fixture's mount points:

| mount point | equals realpath? | is `/`? | realpath starts with `mp + "/"`? |
|---|---|---|---|
| `/proc` | no | no | no |
| `/dev` | no | no | no |
| `/sys` | no | no | no |
| `/tmp` | no | no | no |
| `/srv/quota` | no | no | no (`/srv/quota-probe/data` starts with `/srv/quota-`, not `/srv/quota/`) |
| `/home` | no | no | no |

No candidate ⇒ contract line 99–100: **`unknown`, basis `no_covering_mount`**.
Contract lines 126–127: `fstype`/`mount_point` are **null** when there is no covering
mount. No device comparison is reached (lines 100–103 apply only to a *chosen* mount),
so no `device_check` value is asserted.

**3. `enforcement`.** The classification table (lines 108–122) has no row for the
no-cover branch, so `enforcement` is derived by the table's own uniform convention:
every row whose `quota_state` is `unknown` carries `enforcement` `n/a` (xfs conflicting
options, xfs options absent, btrfs device unmapped, ext superblock unobservable,
unsupported fstype). The only non-`n/a` enforcement values in the table are `enforced`,
`accounting_only` and `unknown`, all on `enabled` rows. ⇒ **`n/a`**.

**4. Run verdict (lines 132–135).** Not a setup error; no path is `enabled`; the one
path is `unknown` ⇒ exit **2**, finding_id **`QUOTA_STATE_UNKNOWN`**. Note exit 2 is
shared with `QUOTA_SETUP`; the finding_id is what distinguishes them, so the sealed
oracle must compare the finding_id (as contract lines 142–145 require).

**5. Compared tuple.** The contract compares only
`path, fstype, mount_point, quota_state, enforcement, basis` (lines 144–145), so
`device_check`, `quota_option_keys` and `btrfs_qgroups_mode` are deliberately **not**
asserted in `expected` — the contract does not specify their values when no mount was
chosen.

## Discriminating power (why this case earns its slot)

- A resolver that uses `realpath.startswith(mount_point)` **without** the contract's
  trailing `/` would select `/srv/quota` (xfs, `noquota` present, `st_dev` `259:2`
  matching the mount's `major:minor` `259:2`) and report
  `disabled` / `xfs_noquota_option` / exit 0 `QUOTA_DISABLED`. The expected
  `no_covering_mount` / exit 2 fails such an implementation. The `st_dev` was chosen to
  match that non-covering mount precisely so the wrong branch is *observable* rather
  than masked by a coincidental `device_mismatch`.
- A resolver that reads **field 4** (`root`) instead of **field 5** (`mount point) —
  both are `/` on several fixture lines — would find a `/` mount and report a
  `xfs_noquota_option` verdict; also fails.
- A resolver that treats a mountinfo without a `/` line as malformed would exit 2
  `QUOTA_SETUP` instead of `QUOTA_STATE_UNKNOWN`; also fails (same exit, different
  finding_id).
- The fixture also carries a btrfs `/home` line plus `device_links`/`btrfs_sysfs`
  entries, so an implementation that reaches for btrfs sysfs state on a path with no
  covering mount has an opportunity to mis-attribute; the expected `basis` catches it.

## Contract ambiguities found (for L1; none blocks this case)

- **A-1 — "or is `/`" has an ambiguous subject.** Line 98: "mount point equals
  realpath, or is `/`, or realpath starts with mount point + `/`". Reading (a) the
  *mount point* is `/` (so a root mount covers every path) or (b) the *realpath* is
  `/`. Reading (a) is the natural one — otherwise a root mount could never be selected
  for a non-root path and the clause would be dead — and (b) would make
  `realpath.startswith(mp + "/")` the only prefix rule, so the clause would be
  redundant with "equals realpath". **This case's expectation is identical under both
  readings**, because the fixture contains no mount point `/` and the realpath is not
  `/`: no candidate either way. Recommend L1 state the subject explicitly, and
  recommend other case authors with a root-mount fixture pin the reading.
- **A-2 — `enforcement` for the no-cover branch is unspecified.** Line 99–100 gives
  `unknown` + `no_covering_mount` but no `enforcement` token, and the table has no such
  row. This case asserts `n/a` by the table's uniform convention for `unknown` rows;
  L1 should either add a table row or state the rule, since the oracle compares
  `enforcement` exactly (line 145).
- **A-3 — non-compared output fields are undefined for the no-cover branch.**
  `device_check`, `quota_option_keys` and `btrfs_qgroups_mode` (lines 125–128) have no
  stated value when no mount was chosen (`null`? empty list? `[]`/`null` vs
  `"not_applicable"`?). The compared tuple (144–145) excludes them, so the oracle is
  unaffected — but a sentinel that checks "no extra/absent fields" could trip.
- **A-4 — `no_covering_mount` is unreachable in real mode.** Every live
  `/proc/self/mountinfo` contains a `/` mount line, so under reading (a) a real path
  always has at least the root candidate and the `no_covering_mount` branch is
  fixture-only. That is consistent with the contract framing this as a synthetic-mode
  edge, but the limits text (lines 137–140) does not say so. Worth one clause so the
  branch is not mistaken for a host-reachable condition.

## Residual risk / verification gaps

- The case is derived by hand from contract prose; no implementation existed to run it
  against (by design: the case lands before the implementation, per the contract's
  sequencing step 4). L1's oracle run is the verification.
- `expected` does not assert `device_check` / `quota_option_keys` /
  `btrfs_qgroups_mode` (contract's compared tuple omits them). If L1 later widens the
  compared tuple, this case's expected object must be extended with an agreed
  convention for the no-cover branch — see A-3.
- Fixture realism was checked by hand against proc.rst §3.5 field layout (S082) and
  against the host-observed line shapes recorded in `frozen/c2-expected-real.json`
  (`0:30 /@home /home ... - btrfs /dev/mapper/root rw,compress=zstd:3,…` and
  `259:1 / /tmp ... - xfs /dev/nvme0n1p1 rw,…,noquota`). The `/srv/quota` xfs line is
  synthetic but structurally identical to the `/tmp` line, so a parser that special-cases
  the real host's lines still sees the same shape.
- No tooling installed or updated this wave; nothing to report on the install ledger.

---

# CORRECTION (appended after `.ufo/waves/round-23/preseal-amendment.md`)

Authored by the same seat (`MadoR22-2.CaseNoCover-8`) on L1's instruction. The
amendment is written before any ImplQuota candidate was opened and before any C2
result was observed; no candidate implementation, oracle, or candidate run was read
while producing this correction. The original proposal
`.ufo/waves/round-23/cases-proposed/CaseNoCover.json` is retained byte-unchanged
(sha256 `27fd2e5f12fe0db0767f72649457a6cac4ed048109c6d660e7ac5e723a3d49d6`).

## New artifact

`.ufo/waves/round-23/cases-corrected/CaseNoCover.json` — same id `CaseNoCover`, same
schema `mori-quota-case-v1`, same scenario, same expected tuple.

## Delta applied to my case (and why the other two amendment deltas do not touch it)

1. **`qgroups_enabled` member added to the btrfs_sysfs UUID record.** The amendment
   makes `qgroups_enabled` a *required* member of every btrfs_sysfs UUID record
   (true/false/null), and requires `qgroups` false to pair with `enabled=null` /
   `mode=null`. My fixture's single record (`1d02a454-c549-4a35-b567-89d60902af8e`,
   `devices:["dm-0"]`, `qgroups:false`, `qgroups_mode:null`) therefore becomes
   `qgroups_enabled: null`. The record is a decoy for this scenario (the queried path
   has no covering mount, so no btrfs resolution happens), but the amendment says
   "every btrfs_sysfs UUID record, including decoys" — so the member is added rather
   than the decoy removed. Record keys are now exactly
   `devices, qgroups, qgroups_enabled, qgroups_mode`.
2. **ext2/3/4 → `unknown` / `n/a` / `ext_quota_option_unverified`** — does not apply:
   my case has no ext path and no ext mount line.
3. **Duplicated covering point → `unknown` / `null` fstype+mount_point /
   `ambiguous_overmount`** — does not apply: my fixture's six mount points
   (`/proc`, `/dev`, `/sys`, `/tmp`, `/srv/quota`, `/home`) are all distinct, and none
   of them covers the queried path, so there is neither a duplicate covering point nor
   any covering point at all.

Everything else is preserved byte-for-byte: `mountinfo` text, `paths`,
`device_links`, `exit`, `finding_id`, the whole expected path tuple, `scenario`,
`id`, `schema` and `sources` (`["S082"]`). Machine-verified diff against the original
proposal: the only differing fixture key is `btrfs_sysfs`; `expected`, `scenario` and
`sources` compare equal.

## Derivation under the amendment (unchanged verdict, tightened reasoning)

- **Fixture validity.** Member types now satisfy the amendment's exact-type rule:
  `qgroups` bool, `qgroups_enabled` bool-or-null (null), `qgroups_mode` mode-or-null
  (null). UUID key is canonical; `devices` and the `device_links` mapped value `dm-0`
  are plain nonempty basenames without slashes or control characters. The one path is
  nonempty, unique, a normalized absolute path/realpath with no dot or dotdot
  component, and `st_dev` `259:2` is a canonical decimal `MAJ:MIN` with no sign and no
  leading zeros. Top-level fixture keys are exactly the five of contract lines 82–90.
- **Octal escapes.** The fixture contains no backslash at all, so the amendment's
  "only 040/011/012/134 are decodable, any other backslash escape is a setup error"
  rule cannot fire.
- **Per-line parsing.** Every mountinfo line carries fields 1–6, optional tagged fields
  (`shared:N`), the `-` separator, and exactly three trailing fields (fstype, source,
  super options) — the amendment's "last THREE fields of EACH chosen line, never
  file-wide" rule, matching proc.rst §3.5 (S082, lines 1965–1990).
- **Empty trailing lines.** The mountinfo text ends with a newline, so the last element
  after splitting is empty; the amendment requires empty trailing lines to be ignored,
  so this stays a verdict case rather than a setup error. (Recorded here because it is
  the one place where the original proposal's outcome depends on an amendment clause
  rather than on the original contract text.)
- **Mount resolution.** No `/` mount point exists; no mount point equals the realpath
  `/srv/quota-probe/data`; no mount point is a component prefix of it (`/srv/quota` +
  `/` = `/srv/quota/` is not a prefix — the next character is `-`, not `/`). No
  candidate ⇒ `unknown` / `no_covering_mount`, `fstype=null`, `mount_point=null`, and
  `device_check=not_checked` per the amendment's no-cover clause. The new
  duplicate-covering-point refusal does not fire.
- **Enforcement** `n/a` (uniform contract convention for an `unknown` state; the
  amendment states the same for the ext rows).
- **Run verdict** — setup error → 2 `QUOTA_SETUP`; any enabled → 1 `QUOTA_ENABLED`;
  any unknown → 2 `QUOTA_STATE_UNKNOWN`; else 0 `QUOTA_DISABLED` (contract lines
  132–135): exit **2**, finding_id **`QUOTA_STATE_UNKNOWN`**. Exit 2 is shared with
  `QUOTA_SETUP`, so the finding_id must be compared.
- **Scored tuple.** The amendment keeps the original six scored fields and adds
  supplementary sealed checks over `device_check`, `quota_option_keys` and
  `ggroups_mode` *where given*. `expected.paths` therefore carries exactly the six
  scored fields. Values this case would support if L1 wants them as supplementary
  checks: `device_check="not_checked"`, `quota_option_keys=[]` (no covering mount, so
  no super options), `btrfs_qgroups_mode=null` (no btrfs mount chosen). They are not
  asserted in `expected` because the case format's expected path objects carry the six
  scored fields only.

## Ambiguities under the amendment (for L1)

- **B-1 — `no_covering_mount` vs. the new vocabulary.** The amendment introduces
  `ambiguous_overmount` for the duplicated-covering-point case and `not_checked` /
  `mismatch` for `device_check`, but does not restate the no-cover basis token. This
  case keeps `no_covering_mount` from contract lines 99–100, on the reading that the
  amendment supersedes only the clauses it names. If L1 intends `no_covering_mount` to
  be renamed (or merged with `ambiguous_overmount`), the expected tuple changes and
  the case must be re-issued — the amendment text does not say so.
- **B-2 — "covering mountpoint occurs more than once" vs. ancestor overmounts.** The
  amendment says the refusal "conservatively handles covering ancestor overmounts too",
  but "covering" is undefined for mount points that are ancestors of, rather than
  equal to, the queried path (e.g. two lines with mount point `/home` and a queried
  path `/home/x`; or a `/` line plus a `/home` line). My case has no covering point at
  all, so the reading does not affect it; L1 should state whether the duplicate test
  applies to the *selected* longest mount point only or to every candidate ancestor,
  because the two readings differ for nested-mount fixtures.
- **B-3 — `device_check` vocabulary for the no-cover case.** The original contract
  named `match` / `btrfs_subvolume_skipped` (and left mismatch unnamed); the amendment
  names `mismatch` and `not_checked`. `not_checked` is new, so a tool written to the
  original contract would emit something else there. Since `device_check` is outside the
  six scored fields, the six-field denominator is unaffected — but if L1 seals
  `device_check` as a supplementary check, the no-cover value `not_checked` must be
  applied consistently across all no-cover cases.
- **B-4 — `enforcement` for the no-cover branch is still unspecified.** Carried
  forward from A-2: the amendment fixes `enforcement` for the ext rows (always `n/a`)
  but leaves the no-cover branch without an explicit token; this case asserts `n/a`
  by the uniform `unknown` convention.

## Hashes (sha256)

- `cases-corrected/CaseNoCover.json` (new, corrected case):
  `334c7cfdddbf9b9f650e62dab94aeba656047044402de166d5b094ed1d210215` (7814 bytes).
- `cases-proposed/CaseNoCover.json` (original, retained untouched):
  `27fd2e5f12fe0db0767f72649457a6cac4ed048109c6d660e7ac5e723a3d49d6`.
- `contract.md` (immutable history): `2bb35aefb08d3fafc467260f859453c0f096effe18b2446503f2b2ee87fe69e7`.
- `preseal-amendment.md`: `4f3707ba2069a6da4d6455a29aea19d1809ae3eba76e25b166810a7e80f25cde`.
