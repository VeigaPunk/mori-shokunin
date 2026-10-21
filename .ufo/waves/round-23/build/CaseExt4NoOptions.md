# CaseExt4NoOptions — ext4 mount with no quota option (superblock quota unobservable)

Seat: `MadoR22-2.CaseExt4NoOptions-8` (leaf fixture-case author). Contract read in full at
`.ufo/waves/round-23/contract.md` (frozen revision `4dc80c1be48308075e83af17f15fbfe7e95e6cb8`).

Independence held: no candidate implementation was opened (`.ufo/waves/round-23/build/ImplQuota/`
and `.scratch/round23/ImplQuota` were not read), and no oracle or sibling case was used as a
derivation source — every expectation below is derived from `contract.md` plus the named kernel
sources only. No tests, builds, linters, live host probes, or VCS mutation were performed.

Case file written (exactly one):
`.ufo/waves/round-23/cases-proposed/CaseExt4NoOptions.json`

## Source anchors used (S077–S084 subset actually relied on)

| S-id | source | bytes / SHA-256 | anchor used |
|---|---|---|---|
| S082 | `Documentation/filesystems/proc.rst` (linux v7.2) | sha256 `e760f716f8278deefab17a63739033cadc7faee93663c49e76455afaaf40d126` | §3.5 lines 1965–1983: field list (1)–(6), optional fields, separator, fstype, source, **(m+4) super options**; (3) `major:minor` is "value of st_dev for files on filesystem" |
| S083 | `Documentation/admin-guide/ext4.rst` (linux v7.2) | sha256 `7929550fa95ed7a0d56cd32c78e3c5f3a598827c4e55f1607097bff2e169dbbd` | lines 261–265 (`quota, noquota, grpquota, usrquota` — "These options are ignored by the filesystem. They are used only by quota tools…"); lines 267–271 (`jqfmt`, `usrjquota`, `grpjquota`) |

The two byte-identical copies under `.scratch/round23/src/` and the per-seat
`.scratch/round23/Src{ProcMountinfo,Ext4Doc}/` fetch directories hash equal, so the anchors I
read are the anchors the wave's source re-openers are documenting.

## Derivation, step by step

1. **Fixture shape.** Exactly the five top-level keys of `mori-quota-fixture-v1` per contract
   lines 82–90: `schema`, `mountinfo`, `paths`, `device_links`, `btrfs_sysfs`. `paths` entries use
   the contract's own three-field shape `{path, realpath, st_dev}` with `st_dev` in `MAJ:MIN`.

2. **mountinfo text.** Three lines built to the proc.rst §3.5 grammar (S082 lines 1965–1983):
   fields 1–6 (`mount ID`, `parent ID`, `major:minor`, `root`, `mount point`, `mount options`),
   an optional field (`shared:N`), the `-` separator, then `fstype`, `mount source`, `super options`
   (the **last** field — contract line 105 makes super options the last mountinfo field, so the
   quota keys are read from there and not from field 6).

   ```
   29 1 8:1 / / rw,relatime shared:1 - ext4 /dev/sda1 rw,errors=remount-ro
   30 29 0:31 / /home rw,relatime shared:2 - btrfs /dev/mapper/root rw,space_cache=v2,subvolid=5,subvol=/
   31 29 8:2 / /srv rw,relatime shared:3 - ext4 /dev/sdb1 rw,errors=remount-ro
   ```

   The btrfs line at `/home` is present but **never selected** by either probed path; it exists so
   the case also demonstrates that a non-covering mount is ignored, and so the fixture's
   `device_links`/`btrfs_sysfs` maps are non-empty and internally consistent
   (`/dev/mapper/root → dm-0`, and the uuid lists `dm-0`).

3. **Mount resolution** (contract lines 95–99). Candidates are mounts whose mount point equals the
   realpath, is `/`, or is a prefix of the realpath; the **longest** mount point wins.
   - `/srv/data` → candidates `/` (len 1) and `/srv` (len 4) → `/srv`, fstype `ext4`.
   - `/var/log` → candidates `/` only (`/home` is neither equal nor a prefix) → `/`, fstype `ext4`.
   Both chosen fstypes are `ext4`, so the ext2/ext3/ext4 rows of the classification table apply.

4. **Device check** (contract lines 100–103). The chosen fstype is not btrfs, so a major:minor that
   differs from the path `st_dev` would force `unknown` / basis `device_mismatch`. To keep the
   expectation on the quota-classification axis rather than the device axis, each path's `st_dev`
   equals its chosen mount's major:minor: `/srv/data → 8:2`, `/var/log → 8:1`. Both therefore take
   `device_check: "match"`, and neither path can fall into `device_mismatch`.

5. **Quota classification** (contract lines 105–120). Super options are the last mountinfo field,
   comma-split, key = text before `=`:
   - `/srv` mount: `rw,errors=remount-ro` → keys `rw`, `errors`.
   - `/` mount: `rw,errors=remount-ro` → keys `rw`, `errors`.
   Neither contains any of `quota, usrquota, grpquota, prjquota, usrjquota, grpjquota`, so the
   ext "none of them" row fires (contract line 119): **quota_state `unknown`, enforcement `n/a`,
   basis `ext_quota_superblock_unobservable`** for both paths. The ext "any of them" row (line 118)
   cannot fire.

6. **Why `unknown` and not `disabled`.** S083 lines 261–265 state that the quota-family mount
   options are *ignored by the filesystem* and are used only by quota tools to recognise volumes
   where quota should be turned on. A mount that carries none of those keys therefore proves
   nothing about the on-disk superblock quota feature: the feature may still be set in the
   superblock and simply not advertised through the mount options. The contract's own limits text
   says the same thing in its own words — "ext quota feature in the superblock is unobservable
   without privileged tools" (contract §C2 limits, lines 137–140) — and forbids `quotactl`/`repquota`/
   `btrfs qgroup`/`xfs_quota`, so no privileged read is available to narrow this. Absence of
   evidence is `unknown`, not `disabled`; `disabled` would be an unevidenced claim.

7. **Verdict precedence** (contract lines 132–135). Setup error → 2 `QUOTA_SETUP` (not applicable:
   the fixture is well-formed, so no setup error). Any `enabled` → 1 `QUOTA_ENABLED` (none). Any
   `unknown` → 2 `QUOTA_STATE_UNKNOWN` (both paths are `unknown`). So the case expects
   **exit 2, `finding_id` `QUOTA_STATE_UNKNOWN`**. Note that `QUOTA_ENABLED` is a runway-reporting
   finding, not a failure claim, so `QUOTA_STATE_UNKNOWN` is likewise an honest "not established"
   verdict rather than a fault finding.

8. **Expected-path key set.** Exactly the six contract tokens `path`, `fstype`, `mount_point`,
   `quota_state`, `enforcement`, `basis`, per the seat brief; `device_check`,
   `quota_option_keys` and `btrfs_qgroups_mode` are deliberately *not* asserted here (the brief
   fixes the expected-path key set, and `quota_option_keys` for these mounts would be an empty
   list, whose exact rendering is not fixed by the contract). Order of `expected.paths` matches the
   order of `fixture.paths`.

## Contract ambiguities found (reported, not silently resolved)

1. **The ext `enabled` arm contradicts S083, and my case is built to avoid depending on it.**
   Contract line 118 makes any of `quota,usrquota,grpquota,prjquota,usrjquota,grpjquota` yield
   `enabled`. S083 lines 261–265 says those very options "are ignored by the filesystem" and serve
   only as quota-tools recognition hints — i.e. their presence is a *request*, not an observation of
   an enabled quota, exactly parallel to the contract's own "positive evidence" framing for xfs.
   The `unknown` enforcement the contract attaches to that row is the defensible half; `enabled`
   is the half the opened source does not support. My case deliberately sits on the **none-of-them**
   arm (line 119), whose outcome (`unknown` / `n/a` / `ext_quota_superblock_unobservable`) is
   uncontroversial and matches both the contract and S083. A sibling case that asserts the ext
   `enabled` arm would be asserting something S083 does not back, and should be flagged to L1.

2. **`prjquota` is in the contract's ext trigger list but appears nowhere in S083.** The ext4
   document names only `quota, noquota, grpquota, usrquota` (261–265) and `jqfmt, usrjquota,
   grpjquota` (267–271). `prjquota` is not documented there; the contract appears to have carried
   it over from the xfs key set. Not load-bearing for this case (none of these keys are present),
   but the ext trigger list is not fully evidenced by the ext4 source row.

3. **`jqfmt` is documented but is not a contract trigger key.** S083 lines 267–271 document
   `jqfmt=<quota type>` as part of the journaled-quota option family ("They replace the above quota
   options"). The contract's ext trigger list contains `usrjquota`/`grpjquota` but not `jqfmt`, so
   a mount carrying only `jqfmt=...` would classify as `unknown`/`ext_quota_superblock_unobservable`
   under the contract, even though `jqfmt` is documented as a quota-family option. `noquota` is the
   mirror-image case: it *is* documented (line 261) and is *not* a trigger key, which is
   consistent (it means "no quota") but is nowhere stated for ext in the table, where xfs gets an
   explicit `noquota` row. Both gaps are outside my scenario and left untouched by this case.

4. **Ordering of the device check versus the quota classification is not spelled out as a
   precedence**, only as separate paragraphs (contract lines 100–103 before the table at 105–120).
   My fixture sets `st_dev` equal to each chosen mount's major:minor, so both orderings yield the
   same expectation and the case is insensitive to that gap.

5. **`enforcement` for the unknown ext row is `n/a`,** which is consistent with every other unknown
   row in the table, but the table uses `n/a` and never spells out whether the emitted value is the
   literal string `n/a` or JSON `null`. I emit the literal string `n/a`, matching the table's
   own token; the expected-path key set for this seat admits only the contract's tokens, so `n/a`
   is the only contract-derived choice.

6. **The `mount_point` for the `/` case is `/`.** The contract says `fstype`/`mount_point` are null
   only "when no covering mount" (contract lines 124–127); a covering root mount is a real mount
   point, so `/var/log` reports `mount_point: "/"`, not null and not `""`.

## What this case does and does not establish

- Establishes: the ext "no quota key anywhere in super options" path is `unknown`, not
  `disabled`, and that a device-matching ext4 mount is what lets the case reach the quota table at
  all (`device_mismatch` would otherwise pre-empt it).
- Does not establish: that quota is off on any ext4 filesystem (it cannot be established without
  privileged reads, which this probe forbids); that `prjquota` or `jqfmt` behave as the contract
  lists; anything about ext2/ext3 (the contract extrapolates the row; S083 is ext4-specific).
- No claim of privacy clearance, baseline acceptance, or remediation follows from this case.

---

# Correction (appended 2026-10-21) — pre-seal amendment applied

Authored after `.ufo/waves/round-23/preseal-amendment.md` was read, and **before** any
ImplQuota candidate was opened or any C2 candidate result was observed. No implementation
(`build/ImplQuota/`, `.scratch/round23/ImplQuota`) was read; no oracle was read; no test,
build or live host probe was run. No delegation.

The original proposal `.ufo/waves/round-23/cases-proposed/CaseExt4NoOptions.json` is retained
byte-unchanged as history. The corrected case is a **new** file:

- corrected case: `.ufo/waves/round-23/cases-corrected/CaseExt4NoOptions.json` (same `id`)

## Delta from the original proposal

| element | original proposal | corrected case | reason |
|---|---|---|---|
| `fixture.btrfs_sysfs.<uuid>.qgroups_enabled` | **absent** | `null` | amendment: "Add required fixture member `qgroups_enabled` to each btrfs_sysfs UUID record: true/false/null"; the record has `qgroups: false`, which "must pair with enabled=null/mode=null" |
| `expected.paths[*].basis` | `ext_quota_superblock_unobservable` | `ext_quota_superblock_unobservable` (**unchanged**) | the amendment's ext clause keeps this basis for mounts with **no** quota-related option key; the `ext_quota_option_unverified` basis applies only when such a key is present, which is the sibling `CaseExt4Usrquota` scenario, not this one |
| `expected.paths[*].quota_state` / `enforcement` | `unknown` / `n/a` | `unknown` / `n/a` (**unchanged**) | the amendment's ext clause fixes ext quota_state to ALWAYS unknown with enforcement n/a — this case already expected exactly that |
| `expected.exit` / `finding_id` | `2` / `QUOTA_STATE_UNKNOWN` | `2` / `QUOTA_STATE_UNKNOWN` (**unchanged**) | no path is `enabled`; at least one path is `unknown` → verdict precedence gives exit 2 `QUOTA_STATE_UNKNOWN` |
| fixture mountinfo, paths, device_links | unchanged | unchanged | no clause of the amendment changes a fixture whose covering mount points are unique, whose st_dev values match their chosen mounts, and whose super options carry no quota key |
| `rationale` | original derivation | rewritten to cite the amendment's clauses as the governing rules and the original contract lines as the retained ones | the amendment supersedes only the erroneous/ambiguous original clauses, so the derivation must name which text now governs |

**The expectation itself did not move.** That is the substantive finding of this correction:
the original proposal already sat on the arm that the amendment preserves (ext, no quota-related
key → `unknown` / `n/a` / `ext_quota_superblock_unobservable`), so the amendment's ext clause
confirms rather than revises it. The only fixture-level defect the amendment exposes in this
case is the missing required `qgroups_enabled` member on the btrfs_sysfs record.

## Corrected derivation under the amendment

1. **ext classification** (amendment, ext2/3/4 clause). ext quota_state is ALWAYS `unknown`,
   enforcement ALWAYS `n/a`. The ext quota-related vocabulary now also contains `noquota` and
   `jqfmt`, but classification stays `unknown` either way. Both mounts here carry super options
   `rw,errors=remount-ro` only — keys `rw` and `errors`, no quota-related key at all — so the
   retained basis `ext_quota_superblock_unobservable` applies to both paths. S083
   (`ext4.rst:261-265`) is the anchor for why a plain quota flag is only a hint and why absence
   proves nothing about the superblock feature; the original contract's limits text (lines
   137-140) records that the ext superblock quota feature is unobservable without privileged
   tools, which the probe forbids.
2. **Mount resolution** (amendment, mount resolution clause). The separator and the **last three
   fields of each line** are parsed, never file-wide; the trailing empty line is ignored; root,
   mount point and source are octal-decoded with exactly `\040 \011 \012 \134` (this mountinfo
   contains no backslash escapes, so the reject-other-escapes rule is not exercised).
   Candidate mounts: mount point equals the realpath, is `/`, or is a component-prefix of the
   realpath; the longest wins. `/srv/data` → `/srv` (len 4) beats `/` (len 1); `/var/log` → `/`.
   The amendment's new refusal rule — if ANY covering mount point occurs more than once, refuse
   classification as `unknown`/`n/a`/`ambiguous_overmount` with `fstype=null`, `mount_point=null`
   — does **not** fire here: the three mount points are `/`, `/home` and `/srv`, each occurring
   exactly once, and no probed path has two covering mount points that repeat.
3. **Device check** (amendment, device mismatch clause). Device mismatch now **preempts** the
   filesystem table (`unknown`/`n/a`/`device_mismatch`, `device_check=mismatch`), and btrfs skips
   equality only when the stat major is `0`. Both probed paths are ext4 with matching
   major:minor (`8:2` for `/srv`, `8:1` for the root mount), so `device_check=match` and the
   filesystem table is reached. The btrfs mount at `/home` covers neither path and is never
   selected, so neither the btrfs equality-skip rule nor its `btrfs_subvolume_skipped` path
   applies.
4. **Fixture source resolution** (amendment). The raw decoded source `/dev/mapper/root` is looked
   up in `device_links` and maps to the basename `dm-0`, which is the device listed by the single
   `btrfs_sysfs` uuid — exactly one uuid match. That uuid is `qgroups: false` paired with
   `qgroups_enabled: null` and `qgroups_mode: null`, as the amendment requires; it is a decoy for
   this case because no probed path resolves to the btrfs mount.
5. **Fixture shape** (amendment, fixture rules). Paths are nonempty, unique and normalized
   absolute with no dot/dot-dot components; `st_dev` values are canonical decimal `MAJ:MIN`
   (`8:2`, `8:1`) with no signs and no leading zeros; the uuid key is a canonical UUID; `devices`
   entries and the mapped `device_links` value are plain nonempty basenames without slashes or
   control characters; the `qgroups` fields have the exact bool / bool-or-null / mode-or-null
   types; the uuid record carries exactly `devices`, `qgroups`, `qgroups_enabled`, `qgroups_mode`
   with no missing or extra keys. Unknown non-quota super options are ignored and no option
   value, mount source or uuid is emitted in any expected field.
6. **Verdict** (amendment and original contract lines 132-135). No path is `enabled`; both paths
   are `unknown` → exit 2, `finding_id` `QUOTA_STATE_UNKNOWN`. The six scored output fields
   (`path`, `fstype`, `mount_point`, `quota_state`, `enforcement`, `basis`) are the only fields
   asserted here; supplementary `device_check`, `quota_option_keys` and `qgroups_mode` checks are
   left to the sealer's supplementary assertions, and the original six-field denominator is
   preserved unchanged.

## Ambiguities still outstanding after the amendment (unchanged in substance)

- The amendment fixes the ext **outcome** (`unknown`/`n/a`) but the ext *basis* wording still
  differs from the xfs treatment: ext has no `noquota`-specific row, so an ext mount carrying
  only `noquota` lands on `ext_quota_option_unverified` (a quota-related key present) rather than
  on any "noquota ⇒ disabled" row. The amendment's ext clause does not say whether `noquota`
  alone is a quota-related key for basis purposes. It does not affect this case (neither mount
  carries `noquota`), but a sibling ext case with `noquota` would need that reading fixed.
- The amendment says a btrfs uuid's `qgroups` false must pair with `enabled=null/mode=null`, and
  that a *present* directory with `enabled=null` yields `btrfs_qgroups_enabled_unavailable`. The
  boundary between "directory absent" (`btrfs_qgroups_dir_absent`, only on a successful parent
  inspection) and "directory present but unreadable" is now explicit for btrfs; the equivalent
  distinction for ext — an unreadable superblock versus a superblock with no quota feature —
  remains unobservable by construction, which is precisely why ext stays `unknown`.
- `enforcement` for the ext unknown arm is the literal string `n/a` (the contract's table token),
  not JSON `null`; the amendment keeps the table's token vocabulary and does not restate this.

## Scope note

This correction adds no claim of privacy clearance, baseline acceptance, remediation or
quota-configuration authority; quota configuration and diagnosis remain tsukuroi/operator work.
