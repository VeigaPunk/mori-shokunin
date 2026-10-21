# CaseExt4Journaled — C2 fixture case for an ext4 journal-quota mount

## Result

One independent C2 fixture case authored and written to
`.ufo/waves/round-23/cases-proposed/CaseExt4Journaled.json` (schema
`mori-quota-case-v1`, id `CaseExt4Journaled`).

Scenario: an ext4 mount at `/srv/journal` whose super options carry
`jqfmt=vfsv0` and `usrjquota=aquota.user` — journal quota with a quota file
name in the option value.

Expected verdict (derived from `contract.md` §C2 only): exit `1`,
`finding_id` `QUOTA_ENABLED`, one path `/srv/journal/data` → `fstype`
`ext4`, `mount_point` `/srv/journal`, `quota_state` `enabled`, `enforcement`
`unknown`, `basis` `ext_quota_option`.

Independence: no implementation was read — neither
`.ufo/waves/round-23/build/ImplQuota/` nor `.scratch/round23/ImplQuota`. The
expectation is derived from `contract.md` (frozen at lane commit
`4dc80c1be48308075e83af17f15fbfe7e95e6cb8`) and the named kernel sources
(S082 `Documentation/filesystems/proc.rst`, S083
`Documentation/admin-guide/ext4.rst`). No sibling case file was used to derive
the expectation; sibling files were read only to confirm the on-disk case
schema/shape already in use in `cases-proposed/`.

## Derivation

1. **Mount resolution.** Probed path `/srv/journal/data`, realpath
   `/srv/journal/data`, `st_dev` `8:2`. The contract's candidate rule
   (contract.md:95–104: mount point equals realpath, or is `/`, or realpath
   starts with mount point + `/`) admits the fixture's root line `/` and its
   ext4 line `/srv/journal`; the longest mount point wins, so the chosen
   mount is `/srv/journal`, `fstype` `ext4`, mountinfo `major:minor` `8:2`.
   The other four lines (`/proc`, `/sys`, `/dev`, `/tmp`) are not candidates
   for this realpath.
   Anchors: `proc.rst` §3.5 (S082) lines 1970–1983 give the field order —
   (1) mount ID, (2) parent ID, (3) major:minor, (4) root, (5) mount point,
   (6) mount options, (n…m) optional fields, (m+1) separator, (m+2)
   filesystem type, (m+3) mount source, (m+4) super options — and line 1985
   "Parsers should ignore all unrecognised optional fields". My ext4 line
   carries the optional field `shared:7`, so the parser must scan to the
   `-` separator rather than count fixed positions; the super options are
   then the last field, `rw,user_xattr,acl,jqfmt=vfsv0,usrjquota=aquota.user`.
2. **Device check.** Chosen fstype is ext4, not btrfs, and the mountinfo
   `major:minor` `8:2` equals the path's `st_dev` `8:2`, so the contract's
   `unknown` / `device_mismatch` branch is not reached. `proc.rst:1975`
   defines field (3) as the "value of st_dev for files on filesystem", so
   equality is the ordinary case for ext4; the btrfs per-subvolume anonymous
   `st_dev` exemption (S081, `fs/btrfs/inode.c` `btrfs_getattr`) does not
   apply to an ext4 mount.
3. **Classification.** Contract.md:105 parses the super options as a
   comma-split list whose key is the text before `=`, giving keys `rw`,
   `user_xattr`, `acl`, `jqfmt`, `usrjquota`. `usrjquota` is a member of the
   contract's ext4 quota-key set (`quota`, `usrquota`, `grpquota`,
   `prjquota`, `usrjquota`, `grpjquota` — contract.md:118), so the enabled
   row applies: `quota_state` `enabled`, `enforcement` `unknown`, `basis`
   `ext_quota_option`. `jqfmt` is *not* in that set, but the row is an "any
   of" test, so `jqfmt` neither adds nor removes the verdict.
   Anchor for the option names and their meaning: `ext4.rst` lines 261–265
   (`quota, noquota, grpquota, usrquota` — "These options are ignored by the
   filesystem. They are used only by quota tools to recognize volumes where
   quota should be turned on.") and lines 267–271 (`jqfmt=<quota type>,
   usrjquota=<file>, grpjquota=<file>` — journal-replay quota details,
   which "replace the above quota options") — S083.
   The contract's ext4 row is the *only* ext row that can fire here: the
   "none of them" row (`unknown` / `ext_quota_superblock_unobservable`)
   cannot apply because a quota key is present.
4. **Verdict precedence.** Exactly one path is probed; it is `enabled` and
   nothing is `unknown`, so exit `1` with finding id `QUOTA_ENABLED`
   (contract.md:132–135). Per the contract, `QUOTA_ENABLED` is a
   runway-reporting finding (df percentages are insufficient there), not a
   failure claim.
5. **File-name non-disclosure.** `usrjquota=aquota.user` puts a quota file
   name in an option *value*. The contract requires the probe to expose
   option **keys** only and to "never echo mount sources, other options or
   file names from option values" (contract.md:124–130), and
   `quota_option_keys` is defined as "sorted quota-related keys only, never
   values or other options". So the correct output names the key
   `usrjquota` and never the string `aquota.user`. The fixture deliberately
   carries a value-shaped token (`aquota.user`, `vfsv0`) so a whole-stdout
   canary scan has something to catch.

## Fixture shape

`mountinfo` holds six lines, all parsed per §3.5 (six fixed fields, optional
fields, `-`, fstype, source, super options):

| line | major:minor | mount point | fstype | purpose |
|---|---|---|---|---|
| 1 | `0:31` | `/` | btrfs | root line; always a candidate, never the longest for this path |
| 2 | `0:22` | `/proc` | proc | non-candidate; optional-field parsing (`shared:2`) |
| 3 | `0:23` | `/sys` | sysfs | non-candidate |
| 4 | `0:5` | `/dev` | devtmpfs | non-candidate |
| 5 | `259:1` | `/tmp` | xfs | non-candidate; also mirrors the frozen real control's xfs line |
| 6 | `8:2` | `/srv/journal` | ext4 | the chosen mount; `major:minor` = path `st_dev` |

`paths` carries one entry (`/srv/journal/data`, realpath identical,
`st_dev` `8:2`). `device_links` maps `/dev/mapper/root` → `dm-0` (the only
link the contract's real-mode inputs can produce is a `readlink` of
`/dev/mapper/*`); `btrfs_sysfs` carries the single uuid from
`frozen/c2-expected-real.json` with `devices` `["dm-0"]`, `qgroups`
`false`, `qgroups_mode` `null` — inert for this case (the chosen mount is
ext4), present so the fixture stays a realistic host view rather than a
one-line toy, and so the top-level fixture keys match
`mori-quota-fixture-v1` exactly.

**Fixture realism (kernel-emitted option order).** The super-options string
`rw,user_xattr,acl,jqfmt=vfsv0,usrjquota=aquota.user` is not invented: in
`fs/ext4/super.c` the fsparam table registers `jqfmt` as an enum whose
constant table accepts `vfsold`/`vfsv0`/`vfsv1`, and `ext4_show_quota_options`
prints `,jqfmt=%s` followed by `seq_show_option(seq, "usrjquota", usr_qf_name)`
— i.e. the kernel prints the format first and then the quota file name, and
the file name is exactly the kind of token the contract forbids echoing.
That kernel file is corroboration beyond the registered S077–S084 rows
(it has no S-id this wave), so it is described here rather than listed in
the case's `sources`.

## Contract ambiguities found (not asserted by the case)

1. **`jqfmt` is absent from the contract's ext4 quota-key set.** The ext4
   documentation (S083, `ext4.rst:267`) lists `jqfmt=<quota type>` as one of
   the three journal-quota options, and `fs/ext4/super.c` treats it as a
   quota-format selector, yet contract.md:118 admits only
   `quota,usrquota,grpquota,prjquota,usrjquota,grpjquota`. An ext4 mount
   carrying **only** `jqfmt=vfsv0` would therefore be classified
   `unknown` / `ext_quota_superblock_unobservable` even though a journal
   quota format is visibly configured. **Medium severity** — this case is
   deliberately insensitive to it (it also carries `usrjquota`, so the
   verdict is `enabled` either way), but a sibling `jqfmt`-only case would
   pin the gap shut one way or the other. Recommendation to L1: state
   whether `jqfmt` is a quota key for the ext4 row.
2. **`noquota` is documented for ext4 but has no ext4 row in the contract.**
   `ext4.rst:261` documents `quota, noquota, grpquota, usrquota`, and the
   contract's xfs rows give `noquota` its own treatment (disabled /
   `xfs_noquota_option`), but the ext4 rows say "none of them" for an ext4
   mount whose only quota-ish key is `noquota`. So an ext4 mount with
   `noquota` reads as `unknown` rather than `disabled`. **Medium severity,
   same family as ambiguity 1.** My case does not use `noquota`.
3. **`prjquota` is in the contract's ext4 key set but not in the ext4
   documentation.** S083's option groups (`quota, noquota, grpquota,
   usrquota` and `jqfmt, usrjquota, grpjquota`) never mention `prjquota`.
   The kernel's fsparam table does register `prjquota` as a flag, so the
   contract's set is kernel-backed, but the documented ext4 option surface
   and the contract's set do not match exactly. **Low severity** — a
   superset of real option names is the safe direction. This case does not
   use `prjquota`.
4. **"enabled" for ext4 means "quota intent visible in mount options", not
   "quota is enforced or the superblock feature is on".** S083 says the
   options are "ignored by the filesystem" and used only by quota tools,
   and the contract's own limits line says "ext quota feature in the
   superblock is unobservable without privileged tools". The contract's
   `enabled` row is therefore consistent with "a quota mechanism is visibly
   configured", and `enforcement` `unknown` carries the honesty. Recorded
   so a reviewer does not read `quota_state: enabled` as a claim that
   quotas are enforced on that ext4 filesystem. **Low severity** (the
   contract's basis token `ext_quota_option` already carries the nuance).
5. **`quota_option_keys` membership is under-defined, and the sealed
   comparison cannot see it.** The contract says `quota_option_keys` is
   "sorted quota-related keys only" without saying, per fstype, which keys
   count as quota-related — for ext4 that plausibly includes `usrjquota` and
   possibly `jqfmt`, but the contract does not say. More importantly, the
   scenario's second half — "output must expose option keys only, never the
   file name" — is **not observable in the sealed per-path tuple**: the
   oracle compares `(path, fstype, mount_point, quota_state, enforcement,
   basis)` for fixture cases (`build/OracleQuota.md`), which excludes
   `quota_option_keys` entirely, and `quota_option_keys` is not in the
   contract's list of fields the sealed case must match either. **Medium
   severity as a coverage gap, not a rule defect.** Recommendation to L1:
   add a whole-stdout negative assertion over the sealed cases (the
   fixture already carries the canary string `aquota.user`, and
   `build/SentinelOutput.md` proposes exactly this shape of canary check),
   or record explicitly that the no-file-name rule is out of scope for the
   sealed-case comparison. Without one of those, a probe that echoed
   `usrjquota=aquota.user` verbatim into `quota_option_keys` would still
   pass this case.
6. **`device_check` for a matching non-btrfs mount is outside the sealed
   tuple as well.** The contract's output lists `device_check` per path,
   but the oracle compares six fields for fixture cases and adds
   `device_check` only for the `--real-expected` control. So this case
   asserts that the device check *passes* (by the fact that the verdict is
   the ext4 option row and not `device_mismatch`), without asserting the
   token `match` itself. **Low severity**, consistent with the
   contract's own comparison list ("per-path (path, fstype, mount_point,
   quota_state, enforcement, basis)").
7. **`major:minor` vs `st_dev` comparison type is unstated.** The contract
   writes "its major:minor ≠ the path's st_dev"; the fixture carries both
   as `MAJ:MIN` strings (`"8:2"`). Numeric comparison and string comparison
   agree here, but a tool comparing numerically would need to parse
   `"8:2"`; a tool comparing as raw strings is fine. **Low severity.**
   Recorded because the fixture format's `st_dev` example
   (`"MAJ:MIN"`) is a string and the real-mode input is
   `os.stat(path).st_dev`, whose `st_dev` is an int — the two are different
   Python types, so the tool must normalize. This case does not assert the
   normalization either way (see ambiguity 6).

## Sources opened (upstream, tag v7.2)

- `Documentation/filesystems/proc.rst` — §3.5 mountinfo field list: sample
  line 1970, field table 1970–1983 (major:minor field (3) at 1975, mount
  options (6) at 1978, optional fields at 1979, separator (m+1) at 1980,
  filesystem type (m+2) at 1981, mount source (m+3) at 1982, super options
  (m+4) at 1983), "Parsers should ignore all unrecognised optional fields"
  at 1985.
- `Documentation/admin-guide/ext4.rst` — lines 261–265 (quota option group,
  "ignored by the filesystem"), lines 267–271 (`jqfmt=<quota type>,
  usrjquota=<file>, grpjquota=<file>`, journal-replay options that "replace
  the above quota options").
- `fs/ext4/super.c` (corroboration, no S-id this wave) — fsparam table:
  `fsparam_string_empty("usrjquota", …)`, `fsparam_string_empty
  ("grpjquota", …)`, `fsparam_enum("jqfmt", …, ext4_param_jqfmt)` with
  `{"vfsold",…},{"vfsv0",…},{"vfsv1",…}`; `ext4_show_quota_options` prints
  `,jqfmt=%s` then `seq_show_option(seq, "usrjquota", usr_qf_name)`;
  `note_qf_name` rejects a quota file name containing `/` ("quotafile must
  be on filesystem root"), which is why `aquota.user` is a legal value.

Read-only; no bytes were written outside my assigned case file and this
report.

## Bounds honored

- Exactly one case file written:
  `.ufo/waves/round-23/cases-proposed/CaseExt4Journaled.json`. No
  production edit, no delegation, no background job.
- No implementation read: neither
  `.ufo/waves/round-23/build/ImplQuota/` nor `.scratch/round23/ImplQuota`;
  no oracle source read either.
- No live host read of any kind: no `/proc/self/mountinfo`, no `os.stat`,
  no `/sys/fs/btrfs` listing, no `/dev/mapper` readlink, no `quotactl`, no
  `btrfs`, no `xfs_quota`, no `repquota`, no `mount`, no privileged or
  mutating command. All host-shaped values in the fixture are synthetic or
  copied from `frozen/c2-expected-real.json` (the uuid `1d02a454-…`, the
  `dm-0` device link, the xfs `/tmp` line).
- No test, build, lint, formatter or self-test was run. The only executed
  commands were JSON parses of my own case file (structure, mountinfo field
  split, and a re-derivation of the expected verdict from my own fixture) —
  facts about my artifact, not gates.
- No tool was installed or updated by this seat (none needed); the operator
  tooling directive is recorded as a no-op. No `pacman` transaction was
  attempted (all pacman transactions are paused host-wide this wave).

## Residual risk / verification gaps

- The expected `quota_state` `enabled` depends on reading `usrjquota` as one
  of the contract's ext4 quota keys (contract.md:118) — that is explicit in
  the contract, so the risk is low; but if L1's sealing text narrows the
  ext4 key set (ambiguity 1/2/3), this case must be re-derived, not edited
  to match an implementation.
- The expectation rests on the device check *passing*. If an implementation
  compared `major:minor` and `st_dev` in a way that fails on this fixture,
  the observed result would be `device_mismatch` — the fixture's `8:2`/`8:2`
  equality is the only defence, and `device_check` itself is outside the
  sealed tuple (ambiguity 6).
- The scenario's "never the file name" half is not asserted by the sealed
  comparison (ambiguity 5). The fixture carries the canary
  `aquota.user`; whether it is actually scanned is L1's call.
- The mountinfo text is a plausible host view, not an observed one: the
  ext4 line (`/dev/sda2`, `8:2`) is synthetic. The case asserts a *rule*,
  not a host fact. `frozen/c2-expected-real.json` remains the only host
  control for C2 and contains no ext4 path.
- Fixture-format conformance was checked by hand against contract.md:84–93
  (exact top-level keys; absolute paths; `MAJ:MIN` `st_dev`; parseable
  mountinfo lines). If L1's `frozen/quota-cases/` linter applies a stricter
  shape than the contract text, this fixture may need a mechanical rewrite.

---

## Correction (appended after the round-23 pre-seal amendment)

L1 issued `.ufo/waves/round-23/preseal-amendment.md` (written before any
candidate was opened). Its "C2 final rules superseding only
erroneous/ambiguous original clauses" section changes two rules that this
case exercised. The original proposal
`.ufo/waves/round-23/cases-proposed/CaseExt4Journaled.json` is left
**untouched** as an unaltered proposal; the corrected, sealable case is a
new file:

`.ufo/waves/round-23/cases-corrected/CaseExt4Journaled.json` (same id
`CaseExt4Journaled`).

### Delta from the original proposal

| field | original proposal | corrected case | why |
|---|---|---|---|
| `expected.exit` | `1` | `2` | ext4 is now always `unknown`, so no path is `enabled`; verdict precedence gives `2` |
| `expected.finding_id` | `QUOTA_ENABLED` | `QUOTA_STATE_UNKNOWN` | same |
| `quota_state` | `enabled` | `unknown` | amendment: "ext2/3/4: quota_state ALWAYS unknown, enforcement n/a … Mount option hints/replay settings do not prove runtime accounting enabled" |
| `enforcement` | `unknown` | `n/a` | same clause |
| `basis` | `ext_quota_option` | `ext_quota_option_unverified` | amendment's renamed basis for "a quota-related option key is present"; `ext_quota_superblock_unobservable` is retained only when no quota-related key is present |
| `fixture.btrfs_sysfs[…].qgroups_enabled` | absent | `null` | amendment: required member on every btrfs_sysfs UUID record; `qgroups false` must pair with `qgroups_enabled=null` and `qgroups_mode=null` |
| `rationale` | cites the original ext rows | cites the amendment as the superseding rule | — |

### Corrected derivation

1. **Mount resolution** — unchanged by the amendment's new rules. Longest
   component-prefix selection still picks `/srv/journal` (fstype `ext4`,
   `major:minor` `8:2`) over the root `/`. The amendment's new
   `ambiguous_overmount` refusal does not fire: in this mountinfo `/`
   occurs once and `/srv/journal` occurs once, so no covering mount point
   is duplicated (verified by counting covering mount points over the
   fixture). The amendment's "parse the separator and the last THREE
   fields of EACH chosen line, never file-wide" is satisfied: the ext4
   line's last three fields are `ext4`, `/dev/sda2`,
   `rw,user_xattr,acl,jqfmt=vfsv0,usrjquota=aquota.user`; the optional
   field `shared:7` sits before the separator and no octal escapes occur
   in root/mount point/source.
2. **Device check** — unchanged: fstype is not btrfs, `8:2` == `st_dev`
   `8:2`, so the mismatch preemption (`unknown/n/a/device_mismatch`) does
   not fire. The btrfs stat-major-zero exemption does not apply to ext4.
3. **Classification** — the amendment's ext rule fires: quota_state is
   ALWAYS `unknown` with enforcement `n/a` for ext2/3/4, because a mount
   option (or a journal-replay setting such as `usrjquota`/`jqfmt`) does
   not prove runtime accounting is enabled — S083 states the plain quota
   flags "are ignored by the filesystem". The amendment's ext
   quota-related vocabulary (original keys plus `noquota` and `jqfmt`)
   matches two keys here, `usrjquota` and `jqfmt`, so the basis is
   `ext_quota_option_unverified`; `ext_quota_superblock_unobservable`
   would apply only if no quota-related key were present.
4. **Verdict precedence** — one path, `unknown`, nothing `enabled` →
   exit `2`, `QUOTA_STATE_UNKNOWN`.
5. **Fixture conformance to the new rules** — `btrfs_sysfs` record
   `1d02a454-c549-4a35-b567-89d60902af8e` now has exactly the keys
   `devices`, `qgroups`, `qgroups_enabled`, `qgroups_mode`, with the
   mandated pairing `qgroups:false → qgroups_enabled:null,
   qgroups_mode:null`; the uuid is canonical; `dm-0` is a plain
   basename; the single path is unique, normalized and absolute with no
   dot/dotdot components; `st_dev` `8:2` is a canonical decimal
   `MAJ:MIN`. The btrfs record remains inert for this case (the chosen
   mount is ext4) and exists to keep the fixture a realistic host view
   with exactly the mandated top-level keys.

### Amendments that do not change this case

- btrfs `qgroups_enabled` / `btrfs_qgroups_enabled` rename — inert here
  (chosen fstype is ext4); the btrfs record in the fixture is carried in
  the new required shape anyway.
- `ambiguous_overmount` (duplicated covering mount point) — this case has
  no duplicated covering mount point, so it keeps a real fstype and mount
  point rather than `null`/`null`.
- xfs precedence and tmpfs four-key rule — other fstypes, not exercised.
- source resolution via `device_links` — the chosen mount is ext4 and
  needs no device mapping.

### Verification gap that survives the amendment

The scored per-path tuple is still the six contract fields, so the
scenario's "never the file name" half (`usrjquota=aquota.user` must not
be echoed) remains **not asserted by the tuple**. The amendment says
"supplementary sealed checks additionally verify device_check,
quota_option_keys and qgroups_mode **where given**" — the expected tuple
has no slot for `quota_option_keys`, so unless the oracle derives it
from the contract's vocabulary, a probe echoing
`usrjquota=aquota.user` into `quota_option_keys` would still pass this
case. The fixture retains the canary string `aquota.user` for such a
whole-stdout check. (See the "Contract ambiguities found" item 5 above.)

### Bounds

No implementation read (`build/ImplQuota/`, `.scratch/round23/ImplQuota`
untouched), no test or tool run — only JSON parses and format checks of
my own two case files. The original proposal file was not edited. One new
file written under the explicitly authorized `cases-corrected/` path.
