# CaseXfsConflict — C2 fixture case (xfs super options carrying both `noquota` and `usrquota`)

Seat: `MadoR22-2.CaseXfsConflict-8` (reviewer, leaf member, no dispatch).
Case file written: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/cases-proposed/CaseXfsConflict.json`
Contract read in full: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/contract.md` (frozen at lane commit `4dc80c1be48308075e83af17f15fbfe7e95e6cb8`).
Independence honoured: no candidate implementation was read (`.ufo/waves/round-23/build/ImplQuota/`, `.scratch/round23/ImplQuota/`), no oracle was read. The expectation below is derived only from contract §C2 and the kernel v7.2 sources named below.

## 1. What the case asserts

A single xfs mount whose **super options** (last mountinfo field) contain `noquota` **and** `usrquota` must be reported as

`quota_state = unknown`, `enforcement = n/a`, `basis = xfs_conflicting_quota_options`,

for every path resolving to that mount, and the run verdict is `exit 2`, `finding_id = QUOTA_STATE_UNKNOWN`.

Two probed paths, both on the same xfs mount, so the case also pins that the mount is chosen once and applies to a nested path:

| path | fstype | mount_point | quota_state | enforcement | basis |
|---|---|---|---|---|---|
| `/srv/quota-lab` | xfs | /srv/quota-lab | unknown | n/a | xfs_conflicting_quota_options |
| `/srv/quota-lab/data` | xfs | /srv/quota-lab | unknown | n/a | xfs_conflicting_quota_options |

Fixture (`mori-quota-fixture-v1`, exact five keys `schema`, `mountinfo`, `paths`, `device_links`, `btrfs_sysfs`):

- `mountinfo` — three realistic lines per proc.rst §3.5 (field (3) major:minor, (4) root, (5) mount point, (6) mount options, one optional `shared:N` tag, `-` separator, filesystem type, mount source, super options):

```
33 2 0:30 /@ / rw,noatime shared:1 - btrfs /dev/mapper/root rw,compress=zstd:3,ssd,discard=async,space_cache=v2,subvolid=256,subvol=/@
65 33 0:30 /@home /home rw,noatime shared:183 - btrfs /dev/mapper/root rw,compress=zstd:3,ssd,discard=async,space_cache=v2,subvolid=257,subvol=/@home
244 33 259:1 / /srv/quota-lab rw,nosuid,nodev,noatime shared:207 - xfs /dev/nvme0n1p1 rw,inode64,logbufs=8,logbsize=256k,noquota,usrquota
```

  The two btrfs lines are deliberate decoys: `/` is a covering-mount candidate for every path, but the longest mount point wins, and `/home` is not a prefix of either probed realpath.
- `paths` — `/srv/quota-lab` (realpath identical) and `/srv/quota-lab/data` (realpath identical), both `st_dev` `259:1`.
- `device_links` — `{"/dev/mapper/root": "dm-0"}`; `btrfs_sysfs` — one synthetic uuid listing `dm-0`, `qgroups: false`, `qgroups_mode: null`. Present with the exact contract shape, inert for this case.

## 2. Derivation, step by step

**(a) Which contract row applies.** Contract §C2 quota-classification table, xfs rows:

1. `noquota` and no quota key → disabled / n/a / `xfs_noquota_option` — **fails**: `usrquota` is a quota key.
2. any of `usrquota,uquota,quota,grpquota,gquota,prjquota,pquota` and no `noquota` → enabled / enforced / `xfs_quota_option` — **fails**: `noquota` is present.
3. only `*noenforce` keys (`uqnoenforce,gqnoenforce,pqnoenforce,qnoenforce`), no `noquota` → enabled / accounting_only / `xfs_quota_option` — **fails**: no `*noenforce` key is present *and* `noquota` is present.
4. **`noquota` together with any quota key → unknown / n/a / `xfs_conflicting_quota_options` — MATCHES.**
5. neither `noquota` nor any quota key → unknown / n/a / `xfs_quota_options_absent` — **fails**: both are present.

Row 4 is the unique matching row, so the expectation does not depend on any unstated row-ordering convention: rows 1–3 and 5 are each mutually exclusive with row 4 by their own stated conditions.

**(b) Verdict.** Contract §C2 verdict precedence: setup error → 2; else any `enabled` → 1 `QUOTA_ENABLED`; else any `unknown` → 2 `QUOTA_STATE_UNKNOWN`; else 0 `QUOTA_DISABLED`. No path is `enabled`, both are `unknown` → **exit 2, `QUOTA_STATE_UNKNOWN`**.

**(c) Mount resolution.** Contract: candidate mounts are those whose mount point equals the realpath, is `/`, or is a prefix (`mount point + "/"`); the **longest** mount point wins, ties broken by the last line. `/srv/quota-lab` (14 chars) beats `/` (1 char) and is not shadowed by `/home`. Both probed paths therefore resolve to the same xfs mount, and `mount_point` in the output is the *mount's* mount point (`/srv/quota-lab`), not the path.

**(d) Device check.** Contract: for a non-btrfs chosen fstype, a major:minor ≠ the path's `st_dev` yields `unknown` / `device_mismatch`. The xfs line's field (3) is `259:1` and both paths' `st_dev` is `259:1`, so the check passes and the conflict row — not `device_mismatch` — is the basis reached.

**(e) Which field carries the tokens.** Contract: "super options = last mountinfo field, comma-split, key = text before `=`". The fixture places `noquota` and `usrquota` only in the last field; the mount-options field (6) is `rw,nosuid,nodev,noatime` and carries no quota token, so the case is not sensitive to a field-6 vs field-m+4 misreading.

## 3. Source anchors actually relied on

| S-id | source | anchor used | what it fixes |
|---|---|---|---|
| S077 | `Documentation/admin-guide/xfs.rst` (v7.2) | `:171-172` "noquota / Forcibly turns off all quota accounting and enforcement within the filesystem."; `:175-177` "uquota/usrquota/uqnoenforce/quota / User disk quota accounting enabled, and limits (optionally) enforced." | the two tokens are mutually opposed in meaning, so a string carrying both cannot be resolved to a single state |
| S078 | `fs/xfs/xfs_super.c` (v7.2) | `:187` `xfs_fs_show_options`; `:1344` `.show_options = xfs_fs_show_options`; `:238-254` the quota printing; `:1542-1552` the option parser | the super-options string that reaches mountinfo is `xfs_fs_show_options` output; `,usrquota` is printed only under `XFS_UQUOTA_ENFD` (`:238-239`) and `,noquota` only when `!(mp->m_qflags & XFS_ALL_QUOTA_ACCT)` (`:253-254`), so the two are mutually exclusive in real output; the parser agrees (`Opt_noquota` clears `XFS_ALL_QUOTA_ACCT`/`XFS_ALL_QUOTA_ENFD` at `:1542-1546`, `Opt_quota/Opt_uquota/Opt_usrquota` set them at `:1547-1552`) |
| S082 | `Documentation/filesystems/proc.rst` (v7.2) | `:1965-1983` §3.5 mountinfo field layout | the exact field layout the fixture reproduces |

Fetched bytes (into `.scratch/round23/CaseXfsConflict/`, read-only):

- `xfs.rst` sha256 `53bda67b5612a3f2c02820604d05825c9d37addba9855e1d4fba330a516d051c`
- `xfs_super.c` sha256 `0a95697dcfcdab8f7ab6ea26fdb941db952db4b73ed93c30d21e40861ed0450c`
- `proc.rst` sha256 `e760f716f8278deefab17a63739033cadc7faee93663c49e76455afaaf40d126`

No tool was installed or updated for this seat (no install needed: `curl` and `python3` were already present, and no build/test/lint was run, per wave bounds).

Scratch artifacts (untracked, outside every commit, per contract item 3): the three fetched source files remain at `.scratch/round23/CaseXfsConflict/{xfs.rst,xfs_super.c,proc.rst}` with the SHA-256 values above, so the anchors can be re-verified without a re-fetch. No file outside my two assigned paths (the case file and this report) was created or modified in the lane; no fixture, clone, or implementation was produced by this seat.

## 4. Contract ambiguities found

1. **Row 4's "any quota key" is narrower than the table's key vocabulary, leaving `noquota` + a `*noenforce`-only string under-determined.** Row 2 defines the quota-key set as `{usrquota,uquota,quota,grpquota,gquota,prjquota,pquota}`; row 3 treats `uqnoenforce,gqnoenforce,pqnoenforce,qnoenforce` as a separate family. If the super options were `noquota,uqnoenforce`, row 4 ("`noquota` together with any quota key") arguably does not apply (a `*noenforce` key is not in row 2's set), while row 1 fails (`usrquota`-style key present) and rows 2/3 fail (`noquota` present) — leaving no row and no defined basis. My case deliberately uses `usrquota`, which is unambiguously in row 2's set, so it is immune. **Recommendation to L1:** state explicitly that row 4's "any quota key" includes the `*noenforce` family, or add a row for `noquota` + `*noenforce`.
2. **Table row order is not declared as evaluation order.** Rows 1–5 as written are mutually exclusive for the case I built, but the contract never says the table is evaluated top-down, so a second xfs case that (say) pairs `usrquota` with `uqnoenforce` would be ambiguous under an unordered reading. **Recommendation:** add "rows are evaluated top-down; first match wins" to §C2.
3. **`quota_option_keys` membership is undefined.** The output field is specified as "sorted quota-related keys only", but no set of "quota-related" keys is enumerated (does `noquota` count? `uqnoenforce`? `qnoenforce`?). This is not part of the compared per-path tuple, so it does not affect this case, but it is an unbounded field for the implementation.
4. **The per-path compared tuple omits `device_check` and `quota_option_keys`.** The contract's output object carries nine per-path fields (`:{path, fstype, mount_point, quota_state, enforcement, basis, device_check, quota_option_keys, btrfs_qgroups_mode}`), while the case-file instruction and the oracle's compared tuple are the six fields `(path, fstype, mount_point, quota_state, enforcement, basis)`. My case file therefore carries exactly the six, matching the sibling cases already in `cases-proposed/`. Note the frozen `frozen/c2-expected-real.json` uses a *different* shape again (`expected_exit` / `expected_finding_id` / `expected_paths` with `device_check` included), so three different key vocabularies now exist for the same data. **Recommendation to L1:** pick one shape and say so before sealing.
5. **Enforcement token for unknown rows.** The contract writes `n/a` in the table; the case file emits the literal string `"n/a"`, consistent with the frozen real expectation's `enforcement: "n/a"`. Worth confirming the oracle compares it as a string, not as null.

## 5. Boundary of this case (what it does not claim)

- It does not claim any live xfs mount can produce `noquota` + `usrquota`; S078 shows the opposite. The case is an adversarial/synthetic input, which is exactly the requested scenario, and it pins the *probe's* refusal to guess.
- It does not assert anything about quota limits, usage, or per-project/group state; the contract's stated limits (no limit/usage reading, `df` cannot see exhaustion) remain untouched.
- It makes no claim about the two decoy btrfs lines, which are present only to make the mount resolution non-trivial.
- No host read, build, test, lint, or privileged interface was used; the only live host read in this seat was `/proc/self/mountinfo` (permitted, and used only to shape a realistic fixture line, never as the expectation's source).

## 6. Verdict

One case file written at the uniquely assigned path, schema `mori-quota-case-v1`, id `CaseXfsConflict`, expected `exit 2` / `QUOTA_STATE_UNKNOWN` with two per-path records `unknown` / `n/a` / `xfs_conflicting_quota_options`. The derivation rests on a uniquely matching contract row plus three kernel anchors (S077, S078, S082) that make the input adversarial and fix the mountinfo field layout. Five contract ambiguities are recorded in §4; none of them changes this case's expectation, but items 1, 2 and 4 are worth a contract amendment before sealing so that sibling cases cannot diverge.

---

# CORRECTION (appended after the round-23 pre-seal amendment, before any candidate inspection or result)

Trigger: L1 instruction (agent://MadoR22-2) to author a NEW corrected case at
`.ufo/waves/round-23/cases-corrected/CaseXfsConflict.json` (same id), leaving the original
proposal untouched. No candidate implementation was opened, no result was observed, no
test/build/lint was run. The original `cases-proposed/CaseXfsConflict.json` is byte-unchanged.

## C1 — corrected case file

`/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/cases-corrected/CaseXfsConflict.json`
sha256 `84dfae8db5f4803e58e82be92d2ac07d321c98214f1a29fee9f844e9d3c56680` (6143 bytes).

Original proposal (retained, untouched): `cases-proposed/CaseXfsConflict.json`
sha256 `197388a69be4e3c483d853c4a400fed7adc57f5ae972dff9047758f33bb4dab1` (4861 bytes).

### Delta against the original proposal

| element | original | corrected | reason |
|---|---|---|---|
| `btrfs_sysfs` record members | `devices`, `qgroups`, `qgroups_mode` | `devices`, `qgroups`, **`qgroups_enabled`**, `qgroups_mode` | amendment: `qgroups_enabled` (true/false/null) is a required member of every btrfs_sysfs UUID record; "Missing/extra record keys setup" |
| `qgroups_enabled` value | absent | `null` | the record is a decoy with `qgroups: false`; the amendment requires `qgroups false` to pair with `enabled=null`/`mode=null` |
| `btrfs_sysfs` uuid key | `11111111-2222-3333-4444-555555555555` | `6b1f4a2c-8d3e-4c5b-9f70-1a2b3c4d5e6f` | the amendment requires canonical UUID keys; the original placeholder was already canonical in shape, so this is a cosmetic tightening to a realistic RFC 4122 v4 value, not a semantic change |
| `mountinfo`, `paths`, `device_links` | — | **byte-identical** | the xfs scenario and its two probed paths are unaffected by the amendment |
| `expected` (exit, finding_id, six-field per-path tuples) | — | **byte-identical** | see "expectation preserved" below |
| `rationale` | original text | extended | cites the amendment's explicit xfs precedence sentence, the per-line last-three-fields rule, the duplicate-covering-mountpoint rule, the device-mismatch preemption rule, the raw-source `device_links` lookup rule, and the supplementary unscored fields |

### Expectation preserved, and why

The amendment's xfs rule is explicit: "XFS precedence: conflict(noquota with ANY quota/enforcement
or noenforce key), then noquota, then any enforced key, then any accounting-only key, else absent."
The fixture's super options are `rw,inode64,logbufs=8,logbsize=256k,noquota,usrquota` — `noquota`
together with `usrquota` (a quota/enforcement key) — so the **conflict** branch is taken first and
yields `unknown` / `n/a` / `xfs_conflicting_quota_options`. This is the same row the original
proposal cited (original contract §C2 xfs row 4), and the amendment explicitly restates it as the
highest-precedence xfs branch, so the scored six-field denominator is unchanged:

- `exit` = 2, `finding_id` = `QUOTA_STATE_UNKNOWN`
- `/srv/quota-lab` → xfs, /srv/quota-lab, unknown, n/a, xfs_conflicting_quota_options
- `/srv/quota-lab/data` → xfs, /srv/quota-lab, unknown, n/a, xfs_conflicting_quota_options

Amendment clauses checked against this case (all pass, none forces a change):

- **Duplicate covering mountpoint** (unknown / n/a / `ambiguous_overmount`, fstype=null, mount_point=null, device_check=not_checked): not triggered. Covering mountpoints for `/srv/quota-lab` are `/` and `/srv/quota-lab`; for `/srv/quota-lab/data` the same two; each occurs **exactly once** in the fixture (`/home` covers neither). Verified by counting mountpoint occurrences per path.
- **Longest component-prefix selection**: `/srv/quota-lab` (14 chars) beats the decoy root `/` (1 char) for both paths; `mount_point` in the output is the mount's mount point, not the path.
- **Per-line last-three-fields parsing** and **octal decoding of root/mountpoint/source with exactly `\040`/`\011`/`\012`/`\134`**: the fixture has no backslashes at all, so no escape is decoded and none is rejected; the quota tokens sit only in the last field (super options), while field (6) carries no quota token, so the case is insensitive to a field-6 vs field-(m+4) misreading.
- **Device mismatch preempts the filesystem table**: the xfs line's field (3) is `259:1` and both paths' `st_dev` is `259:1`, so the equality test passes and the conflict row — not `device_mismatch` — is the basis reached.
- **Raw-source `device_links` lookup**: `device_links["/dev/mapper/root"] = "dm-0"` is keyed by the raw decoded source as it appears in the mountinfo line, and the btrfs UUID's `devices` list holds the plain basename `dm-0`. Inert for this case (the btrfs lines are decoys the longest-prefix rule never selects), but now consistent with the amendment's lookup rule.
- **Fixture hygiene**: paths nonempty, unique, normalized absolute with no `.`/`..` components; `st_dev` canonical decimal `MAJ:MIN` with no leading zeros; `btrfs_sysfs` uuid canonical; `devices` and mapped values plain nonempty basenames with no slashes; `qgroups` exact bool, `qgroups_enabled` bool-or-null, `qgroups_mode` mode-or-null.
- **Supplementary (unscored) fields** the amendment allows a seal to check where given: `device_check` = `match` for both paths; `quota_option_keys` = `["noquota","usrquota"]` (noquota and recognized xfs keys only, sorted); `btrfs_qgroups_mode` = null. Recorded in the corrected rationale; the six scored fields are untouched.
- **Amendment clauses that do not apply to this case**: ext2/3/4 always-unknown with `ext_quota_option_unverified` (no ext path here); the btrfs `btrfs_qgroups_enabled` basis rename and the `btrfs_qgroups_disabled` / `btrfs_qgroups_enabled_unavailable` bases (no btrfs path is selected; the decoy's `qgroups` is false with `enabled=null`, and its mount is never chosen); the tmpfs four-key `_hardlimit` vocabulary (no tmpfs path); the `ambiguous_overmount` refusal (no duplicated covering mountpoint, as shown above).

### Amended-contract ambiguities still open after this correction (unchanged from §4, plus one new)

- §4 items 1 and 2 stand: the amendment *does* now settle row-4 precedence for xfs (conflict first, and conflict covers "ANY quota/enforcement or noenforce key"), which closes my §4 item 1 for xfs and confirms my §4 item 2 concern is resolved for xfs by the explicit precedence sentence. The `quota_option_keys` membership (item 3) is now pinned for xfs by the amendment ("noquota and recognized xfs keys only, sorted") and is closed for this case. Item 4 (three key vocabularies for the same data) and item 5 (`enforcement` "n/a" as a string) remain open and are not mine to decide.
- **New, minor:** the amendment requires `qgroups_enabled` as a fixture member but does not say whether a fixture written before the amendment (i.e. every original proposal in `cases-proposed/`) is rejected as a setup error ("Missing/extra record keys setup") or is simply superseded by the corrected file. If the seal still runs the original proposals, those fixtures will exit 2 `QUOTA_SETUP` and must not be counted as capability failures. My corrected file is written to be valid under the amended rules; the original is left byte-unchanged as the proposal of record.

## Corrected-case verification performed

Structural validation only (no tool run, no candidate, no test): case top-level keys exactly
`{schema, id, scenario, fixture, expected, rationale, sources}`; fixture keys exactly
`{schema, mountinfo, paths, device_links, btrfs_sysfs}`; `expected` keys exactly
`{exit, finding_id, paths}` with per-path keys exactly the six scored fields; per-line mountinfo
separator and last-three-field layout; every covering mountpoint counted exactly once per path;
longest-prefix resolution re-derived by hand and by script; path/`st_dev`/UUID/basename hygiene;
`qgroups_enabled` type and pairing; `expected` block compared field-by-field against the original
proposal and found identical.

Report hash after this append is recorded to L1 separately (the report file's own hash changes
with this append, so the number quoted for `build/CaseXfsConflict.md` above is the pre-append
value `5e96465afe884fbe459911b087a6b686e48feb1fb100f51e3ae764c9d0e1db2a`).
