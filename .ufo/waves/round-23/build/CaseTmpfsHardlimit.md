# CaseTmpfsHardlimit — C2 fixture case (tmpfs `grpquota_block_hardlimit` only)

Seat: `MadoR22-2.CaseTmpfsHardlimit-8` · wave: mori round 23 · claim: C2 (coverage / FR2 quota-surface)
Case file: `.ufo/waves/round-23/cases-proposed/CaseTmpfsHardlimit.json` (exactly one file written)
Independence: derived from `contract.md` + kernel v7.2 sources only. No candidate implementation read
(`.ufo/waves/round-23/build/ImplQuota/` and `.scratch/round23/ImplQuota/` were never opened), no oracle read,
no live host read, no test/build run.

## 1. Scenario and expectation

Mount a tmpfs at `/srv/quota-tmpfs` with **only** `grpquota_block_hardlimit=1m` (no `quota`, `usrquota`,
`grpquota` flag). The contract's tmpfs row keyed on "a key ending `_hardlimit`" must fire.

Expected (case file, `expected`):

| field | value |
|---|---|
| exit | 1 |
| finding_id | `QUOTA_ENABLED` |
| path | `/srv/quota-tmpfs` |
| fstype | `tmpfs` |
| mount_point | `/srv/quota-tmpfs` |
| quota_state | `enabled` |
| enforcement | `enforced` |
| basis | `tmpfs_quota_option` |

## 2. Derivation (contract → fixture → expectation)

**Contract §C2 quota-classification table, tmpfs rows**

> `tmpfs | any of quota,usrquota,grpquota or a key ending _hardlimit | enabled | enforced | tmpfs_quota_option`
> `tmpfs | none of them | disabled | n/a | tmpfs_quota_options_absent`

**Super options of the chosen mount** — contract §C2: "super options = last mountinfo field, comma-split,
key = text before `=`". Per **S082** (proc.rst §3.5) the last field is `(m+4) super options: per super block
options`; per **S084** (tmpfs.rst) the tmpfs quota options are mount options of that filesystem, and the
kernel prints them through the superblock `show_options` callback, so they land in that last field.

The fixture's tmpfs line ends with `rw,inode64,grpquota_block_hardlimit=1048576`:

* key `grpquota_block_hardlimit` ∉ {`quota`,`usrquota`,`grpquota`} → the first tmpfs row does **not** match
  on the flag branch;
* key `grpquota_block_hardlimit` **ends with `_hardlimit`** → the first tmpfs row **does** match →
  `quota_state=enabled`, `enforcement=enforced`, `basis=tmpfs_quota_option`;
* `inode64` is not quota-related and is ignored by the classification (it is a real key the kernel prints;
  S084 documents `inode64`/`inode32`).

**Mount resolution** — contract §C2: candidates are mount points equal to the realpath, `/`, or a prefix of
the realpath; longest mount point wins. realpath `/srv/quota-tmpfs` equals the tmpfs line's mount point
(longest, 16 chars) — `/`, `/home`, `/tmp`, `/dev/shm` do not cover it → `fstype=tmpfs`,
`mount_point=/srv/quota-tmpfs`.

**Device check** — contract §C2: "If chosen fstype is not btrfs and its major:minor ≠ the path's st_dev →
`unknown` basis `device_mismatch`". The fixture sets the path `st_dev` to `0:27`, equal to the line's
major:minor, so the mismatch branch does not apply and the tmpfs classification is reached. (The btrfs
per-subvolume anon-dev skip, S081, is irrelevant to a tmpfs path.)

**Verdict precedence** — contract §C2: setup error → 2 `QUOTA_SETUP`; else any `enabled` → 1
`QUOTA_ENABLED`; else any `unknown` → 2 `QUOTA_STATE_UNKNOWN`; else 0 `QUOTA_DISABLED`. One enabled path,
no unknown sibling → `exit=1`, `finding_id=QUOTA_ENABLED`.

**Value spelling** — the scenario says `=1m`; the fixture writes `=1048576`. S084: "Quota limit parameters
accept a suffix k, m or g for kilo, mega and giga" (so `1m` = 1 MiB = 1048576 bytes at mount time), and the
kernel prints the *parsed* limit, not the mount-time spelling. The contract's key-only parsing (key = text
before `=`) makes the value immaterial to the classification, but the fixture is written in the form the
kernel actually emits.

## 3. Source anchors relied on

| S-id | source (kernel v7.2) | anchor used |
|---|---|---|
| S084 | `Documentation/filesystems/tmpfs.rst` | quota mount-option table: `quota` = "User and group quota accounting and enforcement is enabled on the mount"; `usrquota`; `grpquota` = "Group quota accounting and enforcement is enabled on the mount"; `usrquota_block_hardlimit`, `usrquota_inode_hardlimit`, `grpquota_block_hardlimit`, `grpquota_inode_hardlimit` = global limit setters; "Quota limit parameters accept a suffix k, m or g"; "None of the quota related mount options can be set or changed on remount." |
| S082 | `Documentation/filesystems/proc.rst` §3.5 | field list: (1) mount ID, (2) parent ID, (3) major:minor, (4) root, (5) mount point, (6) mount options, optional fields `tag[:value]` until the `-` separator, then filesystem type, mount source, (m+4) super options; "Parsers should ignore all unrecognised optional fields." |

Corroborating kernel files (opened read-only, **not** S-numbered in this round, so not cited in the case
file's `sources`): `mm/shmem.c` v7.2 and `fs/proc_namespace.c` v7.2 (see §4).

## 4. Contract ambiguities and defects found

**A1 — the `_hardlimit` branch of the tmpfs row is unreachable against real v7.2 output (highest impact).**
`mm/shmem.c` v7.2:

* `shmem_parse_opt` sets `ctx->seen |= SHMEM_SEEN_QUOTA` **only** for the `quota` (4626–4631), `usrquota`
  (4632–4637) and `grpquota` (4638–4643) flags; the four hardlimit options (4644–4679) only set
  `ctx->qlimits.*hardlimit` and never touch `seen`/`quota_types`.
* `shmem_fill_super` copies the parsed limits into the superblock **only** inside
  `if (ctx->seen & SHMEM_SEEN_QUOTA)` (5033–5044, `memcpy(&sbinfo->qlimits, &ctx->qlimits, …)`), and sets
  `sb->dq_op`/`sb->s_qcop` only there.
* `shmem_show_options` (4833–4902) prints `,usrquota` / `,grpquota` when `sb_has_quota_active(...)` and
  prints `,grpquota_block_hardlimit=%lld` only when `sbinfo->qlimits.grpquota_bhardlimit != 0`.

Consequence: a mount with **only** `grpquota_block_hardlimit=1m` never enables quota accounting and never
stores the limit — `sbinfo->qlimits` stays zero, so the kernel prints **no** quota key at all and the
mount is indistinguishable in mountinfo from a plain tmpfs. Conversely, whenever a hardlimit key *is*
printed, quota was enabled on that mount, so `,usrquota` and/or `,grpquota` are printed as well. The
contract's tmpfs row therefore has a branch that no real mountinfo can exercise on its own, and the
premise of this case (a lone hardlimit key) is a state a v7.2 kernel cannot produce. The expectation in the
case file is the **contract's rule applied to the contract's premise** — the rule is what the oracle and the
implementation must implement, and the rule is unambiguous — but any real-host claim of the form "the probe
detects a tmpfs hardlimit" would be unsupported, and a real host mount of exactly this scenario would be
reported as `disabled` / `tmpfs_quota_options_absent` (a true statement about what mountinfo shows, and a
false negative against the operator's intent, since the limit was silently dropped by the kernel).
Disclose as a limit, or amend the row to state that a hardlimit key implies quota was enabled on the mount.

**A2 — the bare `quota` token is not observable either.** `mount -o quota` enables both USR and GRP types
(4626–4631), and `shmem_show_options` prints `,usrquota,grpquota`; the literal key `quota` never appears in
the super options. Harmless for the contract (the check is a superset), but a case author should not build
a fixture whose discriminating key is `quota` — it is not producible.

**A3 — value form.** S084/kernel: the limit is parsed with `memparse` and printed as a byte count
(`%lld`), so the mount-time suffix form (`1m`) never appears in mountinfo. A fixture author must use the
byte form; the contract's key-only parsing makes this cosmetic, but an implementation that echoed values
would leak nothing here — it must not echo values at all (contract: "Never echo mount sources, other options
or file names from option values").

**A4 — no defect found in the field the contract reads.** Contract §C2's "super options = last mountinfo
field" is correct for tmpfs: `fs/proc_namespace.c` v7.2 `show_mountinfo()` composes the last field as
`" ro"/" rw"` + `show_sb_opts()` + `sb->s_op->show_options(...)`, and `shmem_fs_type.show_options =
shmem_show_options` (`mm/shmem.c:5224`). The tmpfs quota keys therefore are visible in the field the
contract reads. The *mount options* field (6) carries only the per-mount flags (`rw,nosuid,nodev,noexec,
relatime`); the fixture keeps both fields in that shape.

**A5 — device_check for tmpfs is a strict equality test.** A tmpfs path's `st_dev` is the anonymous
`0:<n>` dev of the mount, and the mountinfo major:minor is the same `sb->s_dev`; the contract's
non-btrfs equality rule therefore holds (unlike btrfs subvolumes, S081). Fixtures must keep the fixture
`st_dev` string exactly equal to the line's major:minor, in `MAJ:MIN` form, or the classification collapses
to `unknown` / `device_mismatch` before the tmpfs row is reached.

**A6 — informational: enforcement semantics.** S084 attributes "accounting **and enforcement**" to the
`quota`/`usrquota`/`grpquota` flags, but describes the four hardlimit options only as global limit setters.
The contract maps a lone `_hardlimit` key to `enforcement=enforced`; the sources support that reading for
the flags, not for a hardlimit standing alone (A1). No change to the expectation is warranted, but the
row's wording conflates "limit configured" with "enforcement active".

## 5. Residual risk / verification gaps

* The case cannot be validated against a real mount of the scenario, because such a mount does not exist
  (A1); it is a contract-rule case, and the seal should record it as such.
* The fixture's surrounding mounts (`/`, `/home` btrfs, `/tmp` xfs, `/dev/shm` tmpfs) are inert for the
  verdict but are there to make the mountinfo text structurally realistic per S082; they are not claimed to
  reproduce this host.
* The value `1048576` is derived from S084's suffix rule (`1m` = 1 MiB) and the kernel's `memparse`; I did
  not observe a live mountinfo line to confirm the byte rendering, because the wave's lane bounds restrict
  live host reads to the seats whose item names them and my item names none.
* No implementation, oracle, or sibling case was consulted; the expectation is falsifiable only against the
  contract table, which is the intended oracle basis for this wave.

## 6. Bounds honoured

One case file written (`.ufo/waves/round-23/cases-proposed/CaseTmpfsHardlimit.json`) plus this report
(`.ufo/waves/round-23/build/CaseTmpfsHardlimit.md`); no production edit, no delegation, no background job, no
VCS mutation, no live host read, no privileged or mutating command, no test/build run.

## 7. Correction (round-23 pre-seal amendment, 2026-10-21) — appended

Authoritative input: `.ufo/waves/round-23/preseal-amendment.md` (written before L1 opened any ImplQuota
candidate; no C2 result observed). Original proposal
`.ufo/waves/round-23/cases-proposed/CaseTmpfsHardlimit.json` is **retained untouched**
(sha256 `6f469ff5ebffb1487b0943f147acebce16d9588cdf39942f9904077d8cc83b58`).

**Corrected case file (new, same id):** `.ufo/waves/round-23/cases-corrected/CaseTmpfsHardlimit.json`
sha256 `b3226093395d0753138f4761dcd91881e56ff350de213ae4b12f03a57ceb5771`.

### 7.1 Delta applied

| amendment clause | applied to this case? | change made |
|---|---|---|
| btrfs_sysfs UUID record requires `qgroups_enabled` (true / null-with-false / null-with-unknown), `qgroups false` pairs with `enabled=null` and `mode=null` | **yes** (decoy record) | added `"qgroups_enabled": null` to the single UUID record `1d02a454-…` (which has `qgroups:false`, `qgroups_mode:null`) |
| btrfs "present + enabled=true" → basis `btrfs_qgroups_enabled` | no | case is tmpfs; no btrfs path is queried, record is inert |
| ext2/3/4 positive cases → `unknown` / `n/a` / `ext_quota_option_unverified` | no | case is tmpfs; the fixture's `/` line is ext4 but is not a queried path |
| duplicated covering mountpoint → `unknown` / `null` fstype+mount_point / `ambiguous_overmount` | no | covering mountpoints for `/srv/quota-tmpfs` are `/` and `/srv/quota-tmpfs`, each occurring exactly once in the fixture; the rule does not fire |
| mount resolution: ignore empty trailing lines; parse separator + last three fields per line; octal-decode exactly 040/011/012/134 and reject other escapes | verified, no change needed | fixture ends with a newline (one empty trailing line — now explicitly ignored); each line has `-` plus fstype/source/super options as its last three fields; no backslash escapes present |
| device mismatch preempts the filesystem table; equal → `match` | verified, no change needed | path `st_dev` `0:27` equals the line's major:minor `0:27`; fstype is not btrfs |
| fixture source resolution via raw decoded source → `device_links` basename → UUID devices | verified, no change needed | the decoy btrfs line's source `/dev/mapper/root` maps to `dm-0`, which matches the UUID's devices list `["dm-0"]`; the tmpfs path is unaffected |
| path/realpath normalized absolute, unique, no dot/dotdot; `st_dev` canonical decimal MAJ:MIN | verified, no change needed | `/srv/quota-tmpfs` and its realpath are identical, absolute and normalized; `0:27` has no signs and no leading zeros |
| tmpfs: keep quota/usrquota/grpquota and the **four documented** hardlimit keys only; arbitrary `_hardlimit` suffix insufficient | verified, no change to outcome | the fixture's key `grpquota_block_hardlimit` is one of the four documented keys, so the tmpfs row still fires |
| output tuples remain the original six scored fields | preserved | `expected.paths[0]` still carries exactly `path, fstype, mount_point, quota_state, enforcement, basis` |

### 7.2 Unchanged expectation, and why

`exit 1`, `finding_id QUOTA_ENABLED`, path `/srv/quota-tmpfs` → `tmpfs` / `/srv/quota-tmpfs` / `enabled` /
`enforced` / `tmpfs_quota_option`. The amendment states its tmpfs change as a *key-vocabulary* narrowing
("Arbitrary suffix `_hardlimit` is NOT sufficient") and restates no different outcome for the tmpfs row;
where the amendment did intend different outcomes it said so explicitly (ext → `ext_quota_option_unverified`,
btrfs → `btrfs_qgroups_enabled`/`disabled`/`enabled_unavailable`, duplicate cover → `ambiguous_overmount`).
The original §C2 tmpfs row for a recognized quota key remains `enabled / enforced / tmpfs_quota_option`.

The amendment also adjudicates my §4 A1 finding: "Hardlimit-only inputs are defensive synthetic cases; kernel
normally also emits an active quota flag." This case is exactly that declared class, so the fixture is kept
as the contract-rule case, and the kernel-impossibility of the state stays recorded in the case rationale as
a case-class note rather than a defect.

### 7.3 One residual ambiguity for L1 to pin before sealing (token-level)

The amendment's tmpfs bullet ends: "`enforced` describes mechanism flags, never a nonzero limit." Two
readings are possible for a **hardlimit-only** input, which is this case:

* (R1, applied) the row's outcome is unchanged → `quota_state=enabled`, `enforcement=enforced`,
  `basis=tmpfs_quota_option`; the sentence forbids inferring enforcement from a limit *value* (or from an
  unrecognized key), not from a recognized quota key;
* (R2, alternative) enforcement may only be claimed from an actual mechanism flag (`quota`/`usrquota`/
  `grpquota`), so a hardlimit-only input would be `enabled` with a non-`enforced` enforcement token — a
  combination the original table does not define (the table's `enabled` row for tmpfs is always `enforced`).

I applied R1 because the amendment narrows the key set without restating outcomes, and because inventing a
new outcome combination would be an invention beyond the amendment. If L1's intent was R2, the delta is a
single token in one object (`enforcement` in `expected.paths[0]`, plus the matching `expected` in the oracle
and the implementation's tmpfs row); the fixture needs no change, since it already carries no mechanism flag.

### 7.4 Supplementary cross-check values (not part of the six scored fields)

For the seal's supplementary assertions, this case's path would report `device_check: "match"` (st_dev equal
to major:minor, fstype not btrfs), `quota_option_keys: ["grpquota_block_hardlimit"]` (recognized tmpfs quota
keys only, sorted; `inode64` excluded), `btrfs_qgroups_mode: null`.

### 7.5 Bounds honoured for this correction

One new case file in the explicitly authorized `cases-corrected/` directory plus this appended report
section; the original `cases-proposed/` case is byte-unchanged; no implementation, oracle or sibling case
read; no live host read; no test/build run; no delegation. The report file's own sha256 (self-referential,
so not embedded here) is reported to L1 with this correction.
