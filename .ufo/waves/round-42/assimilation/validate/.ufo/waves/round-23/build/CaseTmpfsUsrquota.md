# CaseTmpfsUsrquota — C2 fixture case (tmpfs `/dev/shm` with `usrquota`)

Seat: `MadoR22-2.CaseTmpfsUsrquota-8` (leaf fixture-case author, wave 1).
Case file written (one file, as assigned):
`/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/cases-proposed/CaseTmpfsUsrquota.json`
(4455 bytes; JSON parses; top-level keys exactly `schema, id, scenario, fixture, expected, rationale, sources`).

Contract read in full: `.ufo/waves/round-23/contract.md` (frozen at lane commit
`4dc80c1be48308075e83af17f15fbfe7e95e6cb8`). §C2 is the claim under test; the case is
derived **only** from that contract plus the named kernel sources (S082, S084).

## 1. Scenario and expectation

Fixture: a synthetic `/proc/self/mountinfo` of an ordinary host (ext4 root, btrfs
`/home` subvolume, xfs `/tmp`, tmpfs `/dev/shm`) in which the `/dev/shm` tmpfs carries the
bare `usrquota` flag in its **super options** column. One path is probed: `/dev/shm`
(`realpath` `/dev/shm`, `st_dev` `0:26`).

Expected (contract-derived, not implementation-derived):

| field | value | why |
|---|---|---|
| `exit` | `1` | verdict precedence: any path `enabled` → exit 1 |
| `finding_id` | `QUOTA_ENABLED` | same row (a runway-reporting finding, not a failure claim) |
| `path` | `/dev/shm` | the probed path, echoed |
| `fstype` | `tmpfs` | mountinfo field (m+2) of the chosen line |
| `mount_point` | `/dev/shm` | mountinfo field (5) of the chosen line |
| `quota_state` | `enabled` | tmpfs row 1: a quota key is present |
| `enforcement` | `enforced` | tmpfs row 1 (`usrquota` = accounting **and enforcement**) |
| `basis` | `tmpfs_quota_option` | tmpfs row 1 basis token |

## 2. Derivation, step by step (contract → sources only)

1. **Mount resolution.** Contract §C2 "Mount resolution": parse mountinfo per `proc.rst`
   §3.5 (fields 1–6, optional fields until `-`, then fstype, source, super options);
   candidate mounts are those whose mount point equals the realpath, is `/`, or is a
   prefix of the realpath; choose the **longest** mount point; among equal mount points
   the **last** line wins. For realpath `/dev/shm` the candidates are the ext4 line
   (mount point `/`) and the tmpfs line (mount point `/dev/shm`); `/dev/shm` is longer,
   so the tmpfs line is chosen. `fstype` = `tmpfs`, `mount_point` = `/dev/shm`.
   Field layout is fixed by **S082** = `Documentation/filesystems/proc.rst` §3.5 at v7.2,
   lines 1965–1990 (field table 1970–1983: major:minor = field 3 at 1975, separator at
   1980, filesystem type at 1981, mount source at 1982, super options at 1983).
2. **Option extraction.** Contract: "super options = last mountinfo field, comma-split,
   key = text before `=`". The tmpfs line's last field is
   `rw,nosuid,nodev,noexec,relatime,size=402653184k,usrquota`. Its keys are
   `rw, nosuid, nodev, noexec, relatime, size, usrquota`; `usrquota` carries no `=`, so
   its key is exactly `usrquota`.
3. **Classification.** Contract §C2 table, tmpfs row 1: "any of `quota`,`usrquota`,
   `grpquota` or a key ending `_hardlimit` → `enabled` / `enforced` /
   `tmpfs_quota_option`". `usrquota` is a member of that set, so
   `enabled`/`enforced`/`tmpfs_quota_option`. Row 2 ("none of them → `disabled`") does
   not apply. No `noquota` conflict row exists for tmpfs (the contract has no such row,
   and tmpfs has no `noquota` mount option — see §4 A4).
4. **Device check.** Contract: "If chosen fstype is not btrfs and its major:minor ≠ the
   path's `st_dev` → `unknown` basis `device_mismatch`." tmpfs is not btrfs, so the
   tmpfs line's field 3 (`0:26`) must equal the path's `st_dev`; the fixture's `st_dev`
   is `0:26`, so the row is not degraded to `unknown`. (`device_check` is not among the
   compared per-path fields, but the fixture keeps it consistent so the row could not be
   flipped to `unknown` by a stricter reading.)
5. **Verdict.** Contract §C2 "Verdict precedence": setup error → 2; else any `enabled` →
   1 `QUOTA_ENABLED`; else any `unknown` → 2; else 0. The single path is `enabled`, so
   exit `1`, finding `QUOTA_ENABLED`.

### Source anchors

- **S084** = `Documentation/filesystems/tmpfs.rst` at v7.2 (digest recorded in
  `.ufo/waves/round-23/build/DraftSourceRows/rows.md`):
  - **129–143** quota mount-option table; **135–136** the `usrquota` row:
    "User quota accounting and enforcement is enabled on the mount." → supports both
    `quota_state=enabled` and `enforcement=enforced`.
  - **145** "None of the quota related mount options can be set or changed on remount." →
    supports reading the state from the mount's options rather than from any live
    interface, and is consistent with the contract's "visibly enabled" framing.
- **S082** = `Documentation/filesystems/proc.rst` §3.5 at v7.2, **1965–1990**
  (field table 1970–1983) → fixes how the fstype and the super-options column are
  located, and that optional tagged fields (`shared:9`) sit before the `-` separator.

### Out-of-band realism check (explicitly NOT part of the derivation)

To confirm that the fixture's option string is kernel-shaped rather than invented, I
re-read the upstream v7.2 tmpfs implementation (`mm/shmem.c` in this tree — note
`fs/tmpfs/shmem.c` does not exist at v7.2 here) **without using it to derive the
expectation**:
`fsparam_flag("usrquota", Opt_usrquota)` at 4462; `case Opt_usrquota:` at 4626–4631
setting `ctx->quota_types |= QTYPE_MASK_USR`; and the superblock `show_options` emitting
`seq_printf(seq, ",usrquota")` at 4878–4879 under
`sb_has_quota_active(root->d_sb, USRQUOTA)`. So the kernel prints the **bare key**
`usrquota` into the mountinfo **super-options** column — exactly where the contract
tells the probe to look. This source is **not** in S077–S084 and is **not** registered in
`corpus/SOURCES.md`; the case file's `sources` array therefore lists only S082 and S084.
Recommendation to L1: if the probe's tmpfs row is to be sourced from code rather than
docs, register this file (e.g. as a new S-row) — §3 below.

## 3. S-id mapping caveat (same caveat as the sibling cases)

`corpus/SOURCES.md` still ends at S076. The S077–S084 rows exist only as a draft in
`.ufo/waves/round-23/build/DraftSourceRows/rows.md` (status `queued`). I used the
mapping that draft states — **S082 = proc.rst §3.5**, **S084 = tmpfs.rst** — and it is
cross-checked by the contract's own citation of **S081** for "per-subvolume anonymous
st_dev" (the fifth row, `fs/btrfs/inode.c`), so the ordering is the draft's and is
consistent with the contract. **If L1 renumbers the rows, the `sources` array in
`CaseTmpfsUsrquota.json` must be renumbered**; the rationale's file:line anchors are
unaffected and remain the load-bearing evidence.

## 4. Contract ambiguities and gaps found (for L1)

- **A1 — tmpfs "disabled" arm is not literally sourced.** The contract's second tmpfs
  row ("none of them → `disabled` / `n/a` / `tmpfs_quota_options_absent`") has no
  explicit sentence in S084: the doc introduces quotas as activated by "the following
  mount options" (129) and makes them mount-time-only (145), so "absent ⇒ disabled" is a
  defensible implication, not a literal statement. This does **not** affect my case
  (the enabled arm is explicit), but it affects the sibling `CaseTmpfsNoQuota` arm and
  should be either sourced or the contract row narrowed.
- **A2 — only the super-options column is read.** The contract defines the quota key
  source as "super options = last mountinfo field". For tmpfs this is correct (the
  kernel emits `usrquota` there — §2 out-of-band check), but the contract is silent
  about mountinfo field (6) "mount options". Any filesystem that reflected a quota key
  only in field (6) would be classified `disabled` under the contract as written. The
  contract's own wording is the tie-breaker here, so I did not deviate; but L1 may want
  to state explicitly that field (6) is deliberately not consulted, since a case that
  places `usrquota` in field (6) only would be classified `disabled`/`n/a`.
- **A3 — the `_hardlimit` disjunct is under-determined in the sources.** S084
  (129–143) only says the `*_hardlimit` options "Set global user/group quota block/inode
  hard limit"; it never states that supplying one alone enables accounting or
  enforcement. The contract nevertheless folds it into the same
  `enabled`/`enforced`/`tmpfs_quota_option` row. My case deliberately avoids that
  disjunct (only `usrquota` is present), so my expectation does not inherit the gap —
  but the sibling `_hardlimit` case does, and the contract row should either cite a
  kernel-code anchor (e.g. `mm/shmem.c`, where the limits are stored in
  `ctx->qlimits` and printed back at 4882–4893) or split the two disjuncts into
  separate rows with separate bases.
- **A4 — tmpfs has no `noquota` and no conflict row.** The contract has an
  `xfs_conflicting_quota_options` row but no tmpfs analogue. That is consistent with the
  kernel: tmpfs's option table (out-of-band check of `mm/shmem.c`) has `quota`,
  `usrquota`, `grpquota` and the four `*_hardlimit` string options, and **no `noquota`**,
  so a tmpfs mount cannot carry "noquota together with a quota key". The absence of the
  row is therefore correct, but the contract does not say so; a note would prevent a
  future author from inventing a tmpfs conflict case.
- **A5 — tmpfs has no `unknown` row.** Every tmpfs mount therefore resolves to
  `enabled` or `disabled` and never to `unknown`/`n/a`. This is a deliberate-looking
  consequence of the mount-time-only nature of the options, but it is worth recording
  that the tmpfs row set has no "cannot tell" outcome, unlike xfs/btrfs/ext4.
- **A6 — `quota_option_keys` semantics are not pinned for tmpfs.** The contract says the
  output field holds "sorted quota-related keys only"; it does not enumerate which
  tmpfs keys count as "quota-related" (the flag set {quota,usrquota,grpquota} plus any
  `*_hardlimit` key?). My expected path object asserts only the six compared fields, so
  it does not depend on this; the oracle should not compare it either.

## 5. Independence, scope and hygiene

- **Independence held.** No candidate implementation was opened:
  `.ufo/waves/round-23/build/ImplQuota/` and `.scratch/round23/ImplQuota` were never
  read, nor `.ufo/waves/round-23/build/OracleQuota/`. The expectation comes from the
  contract's own table plus S082/S084 only.
- **Disclosure (peer files read).** Before authoring I read the sibling case file
  `.ufo/waves/round-23/cases-proposed/CaseTmpfsHardlimit.json` to learn the on-disk
  case-file shape (top-level keys, fixture key set, expected-field set) and read the
  source-scout report `.ufo/waves/round-23/build/SrcTmpfsDoc.md` (a source re-opener's
  report, not an implementation). Neither supplies my expectation: my row uses the
  `usrquota` disjunct (explicit in `tmpfs.rst:135-136`), whereas the sibling case uses
  the `_hardlimit` disjunct, which `tmpfs.rst` does **not** support (see A3). Peer build
  reports for other seats (btrfs/xfs cases) were seen only as grep snippets while
  locating the S-id registry; they are not tmpfs/quota-option sources for this case.
- **No live host reads.** I performed no `/proc/self/mountinfo` read, no `os.stat` of the
  fleet root or `/tmp`, no `/dev/mapper` readlink, no `/sys/fs/btrfs` listing, and no
  privileged or mutating command of any kind. The fixture is synthetic and lives only in
  the case file; no scratch file, clone, fixture directory or git object was created.
- **No VCS mutation.** Nothing was staged, committed, or branched; no `jj` command was
  run. The only writes were the two assigned files: the case JSON and this report.
- **No tool install or upgrade** was needed or performed (no new tool was required for
  derivation; the only network access was read-only HTTPS fetches of upstream Linux v7.2
  source text to stdout, for the anchors above).
- **No execution of any candidate implementation, oracle, selftest or gate** — the wave
  forbids it, and this case is therefore **unexecuted by construction**. L1 measures it
  after integration.
- **C1 untouched.** This seat made no change to `tools/mori-retention-reconcile.py`, to
  any frozen file, or to any production path.

## 6. Residual risk / verification gaps

1. The case is **unverified against any implementation** by design (wave rule). If the
   sealed oracle compares only the six per-path fields named in the contract, this case
   pins: mount selection (longest mount point, `/dev/shm` over `/`), tmpfs
   classification from the super-options column, the `usrquota` key match, and the
   `enabled` → exit 1 `QUOTA_ENABLED` precedence.
2. If the oracle also compares `device_check` or `quota_option_keys`, this case pins
   `device_check` implicitly (`match`, since `0:26` == `0:26`) and `quota_option_keys`
   only as the sorted quota-related keys of the chosen mount (`usrquota`) — the latter
   depends on the unpinned A6 semantics; the expected object deliberately omits it.
3. The S-id binding is provisional (see §3); renumbering S077–S084 requires editing the
   `sources` array of the case file.
4. The kernel-side realism check in §2 used a source outside S077–S084; if L1 prefers the
   case to rest on registered sources only, the fixture's super-options string can be
   justified by S084's option table alone (the doc lists `usrquota` as a tmpfs mount
   option, and `proc.rst` §3.5 fixes where the last field comes from) — the expectation
   is unchanged either way.

---

## 7. Correction appended 2026-10-21 — round-23 pre-seal amendment (authored before any candidate was opened)

Source of the correction: `.ufo/waves/round-23/preseal-amendment.md` (amendment written
before L1 opened any ImplQuota candidate or ran any C2 candidate; no C2 result observed
by this seat, and none inspected).

**Corrected case authored:**
`/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/cases-corrected/CaseTmpfsUsrquota.json`
(same `id` `CaseTmpfsUsrquota`). The original proposal
`cases-proposed/CaseTmpfsUsrquota.json` is **retained unaltered** (byte-identical to
what §1–§6 of this report describes).

### Delta (the whole delta)

| item | proposal | corrected |
|---|---|---|
| fixture `btrfs_sysfs["1d02a454-…"].qgroups_enabled` | *absent* | **`null`** (amendment: “Add required fixture member `qgroups_enabled` … true/false/null”; “qgroups false must pair with enabled=null/mode=null”) |
| every other fixture byte | — | unchanged (`mountinfo`, `paths`, `device_links`, `qgroups:false`, `qgroups_mode:null`) |
| `expected` | — | unchanged: exit `1`, `QUOTA_ENABLED`, `/dev/shm` → `tmpfs`, `/dev/shm`, `enabled`, `enforced`, `tmpfs_quota_option` |
| `sources` | — | unchanged: `S082`, `S084` |

The corrected file’s `rationale` was rewritten to state that it is the corrected case,
to record the delta, and to re-derive the (unchanged) expectation against the
amendment’s superseding C2 rules. The six scored output fields are preserved exactly.

### Re-derivation against the amendment’s superseding C2 rules (expectation unchanged)

1. **Mount resolution** — the amendment keeps longest component-prefix selection and
   adds: if any covering mountpoint occurs more than once → `unknown`/`n/a`/
   `ambiguous_overmount`, `fstype=null`, `mount_point=null`, `device_check=not_checked`.
   Covering mountpoints for realpath `/dev/shm` in this fixture are `/` (the ext4 line)
   and `/dev/shm` (the tmpfs line); **each occurs exactly once**, so no ambiguity arises
   and the tmpfs line is still selected. Per-line parsing of separator + last three
   fields holds for all four lines; no backslash escapes appear (so neither the
   `040/011/012/134` decode nor the “reject other backslash escapes” rule is
   exercised); the single trailing newline yields no non-empty trailing line.
2. **Quota classification (tmpfs)** — the amendment preserves `quota`, `usrquota`,
   `grpquota` and the **four documented** hardlimit keys and states that an arbitrary
   `_hardlimit` suffix is **not** sufficient. This case uses the plain flag `usrquota`,
   a member of the preserved set, so contract row
   `tmpfs | any of quota,usrquota,grpquota or a key ending _hardlimit | enabled |
   enforced | tmpfs_quota_option` applies unchanged → `enabled`/`enforced`/
   `tmpfs_quota_option`. The amendment’s clarifications (“`enforced` describes mechanism
   flags, never a nonzero limit”; “the kernel normally also emits an active quota flag”
   alongside hardlimit options) are both satisfied by this shape: a mechanism flag only,
   no limit value, and the kernel-faithful flag-only option string.
3. **Device check** — the amendment makes device mismatch **preempt** the filesystem
   table (`unknown`/`n/a`/`device_mismatch`, `device_check=mismatch`) and skips the
   equality test for btrfs only when the stat major is `0`. tmpfs is not btrfs, so the
   equality test applies: the tmpfs line’s major:minor `0:26` equals the path’s
   `st_dev` `0:26` → `device_check=match`, no preemption.
4. **Fixture shape** — paths nonempty/unique/normalized absolute with no dot/dotdot
   components (`/dev/shm`); `st_dev` canonical decimal `MAJ:MIN` with no signs and no
   leading zeros except `0` (`0:26`); UUID key canonical; `device_links` values plain
   nonempty basenames without slashes or control characters (`dm-0`, `nvme0n1p3`);
   `qgroups`/`qgroups_enabled`/`qgroups_mode` have exact bool / bool-or-null /
   mode-or-null types (`false` / `null` / `null`).
5. **Verdict** — no setup error; one path `enabled` → exit `1`, finding `QUOTA_ENABLED`;
   the amendment preserves the six scored output fields and the original verdict
   precedence.

### Amendment clauses that do NOT apply to this case (stated for the seal record)

- **btrfs `qgroups_enabled` semantics** (`btrfs_qgroups_enabled` / `btrfs_qgroups_disabled`
  / `btrfs_qgroups_enabled_unavailable`) — no btrfs path is probed; the only btrfs_sysfs
  record is an inert decoy (its `qgroups:false` pairs with `enabled=null`, `mode=null`),
  and no expectation depends on it.
- **ext2/3/4 → always `unknown`/`n/a`** (`ext_quota_option_unverified`) — no ext path is
  probed.
- **duplicate covering mountpoint → `ambiguous_overmount`** — each covering mountpoint
  occurs once (§7.1 above).
- **XFS precedence rework** — no xfs path is probed (the fixture keeps a realistic xfs
  `/tmp` line for realism only; it is not in `paths`).

### Hygiene for this correction

No implementation, oracle or candidate result was read or executed; no test was run.
The only writes are the authorized corrected case file and this appended section.
Original proposal untouched; no other file modified. No tool install or upgrade.

### Final hashes (SHA-256)

- corrected case `cases-corrected/CaseTmpfsUsrquota.json`: see §7 hash table appended
  below by the final hash step.
- original proposal `cases-proposed/CaseTmpfsUsrquota.json`: unchanged (hash below).
- this report `build/CaseTmpfsUsrquota.md`: hash after this append (below).

| artifact | SHA-256 | bytes |
|---|---|---|
| `.ufo/waves/round-23/cases-corrected/CaseTmpfsUsrquota.json` | `7ecc3503a5fd3aa4b6a1bb635ae34965f7a6f97466c4ff273e9bb836517ac800` | 5608 |
| `.ufo/waves/round-23/cases-proposed/CaseTmpfsUsrquota.json` (unaltered proposal) | `6152062f45080ace9a1ca4b3121f15ebcb6ddc544f011a2a4e0c4e53959adc3f` | 4455 |
| `.ufo/waves/round-23/preseal-amendment.md` (input, read-only) | `4f3707ba2069a6da4d6455a29aea19d1809ae3eba76e25b166810a7e80f25cde` | — |
| `.ufo/waves/round-23/contract.md` (input, read-only, immutable history) | `2bb35aefb08d3fafc467260f859453c0f096effe18b2446503f2b2ee87fe69e7` | — |

The hash of this report cannot be embedded in itself; it is delivered in this seat's
reply to L1 (`agent://MadoR22-2`) as the sha256 of
`.ufo/waves/round-23/build/CaseTmpfsUsrquota.md` after this final append.
