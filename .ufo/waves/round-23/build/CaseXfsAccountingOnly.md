# CaseXfsAccountingOnly — xfs accounting-only quota surface (round 23, C2)

Seat: `MadoR22-2.CaseXfsAccountingOnly-8` (leaf fixture-case author). Detection/report only.
Contract read in full at `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/contract.md`
(frozen at lane commit `4dc80c1be48308075e83af17f15fbfe7e95e6cb8`).

Deliverable: exactly one case file, `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/cases-proposed/CaseXfsAccountingOnly.json`
(5818 bytes, schema `mori-quota-case-v1`, id `CaseXfsAccountingOnly`).

Independence held: no candidate implementation was opened — neither
`/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/build/ImplQuota/` nor
`/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/round23/ImplQuota`. No oracle
(`/build/OracleQuota/`) was opened. No sibling case file's fixture, expectation or
rationale was read as a source for this expectation; sibling *case files* were read only
after this case's expectation was fixed, to confirm the on-disk key shape and the
mountinfo trailing-newline convention, and to check id/file-name uniqueness
(`CaseUnsupported.md` in this same wave discloses the same convention read). The
expectation below is derived from `contract.md` §C2 plus the three kernel sources named
in the case file.

## 1. Scenario and expectation

| Field | Value |
|---|---|
| scenario | xfs mount whose super options carry only `uqnoenforce` and `pqnoenforce` (user + project quota accounting without enforcement), no `noquota` |
| expected exit | `1` |
| expected finding_id | `QUOTA_ENABLED` |
| expected path | `path /srv/xfsacct/data`, `fstype xfs`, `mount_point /srv/xfsacct`, `quota_state enabled`, `enforcement accounting_only`, `basis xfs_quota_option` |
| sources cited | S077, S078, S082 |

## 2. Derivation, step by step

**Step 1 — mount resolution.** Contract §C2: "Candidate mounts: mount point equals
realpath, or is `/`, or realpath starts with mount point + `/`. Choose the longest mount
point; among equal mount points the **last** line wins."

Fixture realpath is `/srv/xfsacct/data`. Fixture mount points: `/` (btrfs), `/home`
(btrfs), `/run` (tmpfs), `/tmp` (xfs), `/srv/xfsacct` (xfs). Candidates for
`/srv/xfsacct/data`: `/` (explicitly a candidate) and `/srv/xfsacct` (prefix rule,
`/srv/xfsacct/data`.startswith(`/srv/xfsacct/`)). `/home`, `/run`, `/tmp` cover nothing.
Longest mount point wins → `/srv/xfsacct`, whose line's fstype is `xfs`, source
`/dev/nvme0n1p3`.

Anchor: **S082** = `Documentation/filesystems/proc.rst` at v7.2, §3.5 (lines 1965–1990;
field table 1970–1983: major:minor field 3 at 1975, mount point field 5 at 1977, mount
options field 6 at 1978, separator `m+1` at 1980, filesystem type `m+2` at 1981, mount
source `m+3` at 1982, super options `m+4` at 1983; optional tagged fields such as
`shared:N` before the separator). Every fixture line was re-parsed against that layout.

**Step 2 — device check.** Contract §C2: "If chosen fstype is not btrfs and its
major:minor ≠ the path's st_dev → `unknown` basis `device_mismatch`." The chosen line
carries `259:3`; the fixture path carries `st_dev "259:3"`. Equal → the mismatch branch
does not fire and the path reaches the quota table. (The btrfs per-subvolume anonymous
device rule, S081, is irrelevant to an xfs path and no btrfs path is queried.)

**Step 3 — option extraction.** Contract §C2: "super options = last mountinfo field,
comma-split, key = text before `=`". The chosen line's last field is
`rw,inode64,logbufs=8,logbsize=256k,uqnoenforce,pqnoenforce`. Keys: `rw`, `inode64`,
`logbufs`, `logbsize`, `uqnoenforce`, `pqnoenforce`. Quota-related keys present:
`uqnoenforce`, `pqnoenforce`. `noquota` is **absent**. The `logbufs=8` / `logbsize=256k`
values are irrelevant — the contract parses keys only and never echoes values.

**Step 4 — classification row.** Contract §C2 table, xfs rows:

| row | condition | matches here? |
|---|---|---|
| 1 | `noquota` and no quota key → `disabled`/`n/a`/`xfs_noquota_option` | no — `noquota` absent |
| 2 | any of `usrquota,uquota,quota,grpquota,gquota,prjquota,pquota` and no `noquota` → `enabled`/`enforced`/`xfs_quota_option` | no — none of these keys present |
| 3 | only `*noenforce` keys (`uqnoenforce,gqnoenforce,pqnoenforce,qnoenforce`), no `noquota` → `enabled`/`accounting_only`/`xfs_quota_option` | **yes** — the quota key set is exactly `{uqnoenforce, pqnoenforce}` and `noquota` is absent |
| 4 | `noquota` together with any quota key → `unknown`/`n/a`/`xfs_conflicting_quota_options` | no — no `noquota` |
| 5 | neither `noquota` nor any quota key → `unknown`/`n/a`/`xfs_quota_options_absent` | no — a quota key is present |

Row 3 is the unique match → `quota_state enabled`, `enforcement accounting_only`,
`basis xfs_quota_option`.

**Step 5 — verdict.** Contract §C2: "setup error → 2 `QUOTA_SETUP`; else any `enabled` →
1 `QUOTA_ENABLED` (positive evidence is never hidden by an unknown sibling); else any
`unknown` → 2 `QUOTA_STATE_UNKNOWN`; else 0 `QUOTA_DISABLED`." One path, `enabled` →
exit `1`, finding_id `QUOTA_ENABLED`. The contract also states that `QUOTA_ENABLED` is
"a runway-reporting finding (df percentages are insufficient there), not a failure
claim" — so exit 1 here is a positive-visibility verdict, not an error.

## 3. Source anchors

All three opened read-only from `raw.githubusercontent.com/torvalds/linux/v7.2` and cached
under `/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/round23/CaseXfsAccountingOnly/`
(read-only reference copies; no implementation, no build, no test).

| id | file | digest / bytes | anchors used |
|---|---|---|---|
| S077 | `Documentation/admin-guide/xfs.rst` | sha256 `53bda67b5612a3f2c02820604d05825c9d37addba9855e1d4fba330a516d051c`, 22719 B | `:171-173` `noquota` — "Forcibly turns off all quota accounting and enforcement within the filesystem."; `:175-177` `uquota/usrquota/uqnoenforce/quota` — "User disk quota accounting enabled, and limits (optionally) enforced."; `:179-181` `gquota/grpquota/gqnoenforce`; `:183-185` `pquota/prjquota/pqnoenforce` — the xfs quota-option vocabulary, including that the accounting-only spellings are exactly the `*noenforce` forms |
| S078 | `fs/xfs/xfs_super.c` | sha256 `0a95697dcfcdab8f7ab6ea26fdb941db952db4b73ed93c30d21e40861ed0450c`, 72773 B | `xfs_showargs` `:238-254`: `,usrquota` only under `XFS_UQUOTA_ENFD` (238–239), `,uqnoenforce` under `XFS_UQUOTA_ACCT` (240–241), `,prjquota` under `XFS_PQUOTA_ENFD` (243–244), `,pqnoenforce` under `XFS_PQUOTA_ACCT` (245–246), `,grpquota` (248–249), `,gqnoenforce` (250–251), `,noquota` only when `!(mp->m_qflags & XFS_ALL_QUOTA_ACCT)` (253–254). Parser arms `:1542-1576`: `Opt_noquota` clears both `XFS_ALL_QUOTA_ACCT` and `XFS_ALL_QUOTA_ENFD`; `Opt_uqnoenforce`/`Opt_qnoenforce` set `XFS_UQUOTA_ACCT` and clear `XFS_UQUOTA_ENFD`; `Opt_pqnoenforce` sets `XFS_PQUOTA_ACCT` and clears `XFS_PQUOTA_ENFD`; `Opt_usrquota`/`Opt_uquota`/`Opt_quota` set `XFS_UQUOTA_ENFD` |
| S082 | `Documentation/filesystems/proc.rst` | sha256 `e760f716f8278deefab17a63739033cadc7faee93663c49e76455afaaf40d126`, 107560 B | §3.5 `/proc/<pid>/mountinfo` lines 1965–1990; field table 1970–1983; optional-field list 1988–1993 ("Parsers should ignore all unrecognised optional fields") |

**Why the fixture's super-options string is kernel-realistic (not invented).** S078
lines 238–254 plus 253–254 together prove the emission is exhaustive and exclusive: the
kernel prints `,noquota` **iff** no accounting flag is set, and otherwise prints exactly
one name per active scope. A mount with user-quota accounting and project-quota
accounting, neither enforced, therefore reports exactly `uqnoenforce,pqnoenforce` and
never `noquota` — the fixture's last field. The mount-option *parser* arms (1553–1568)
show the same thing from the input side: `uqnoenforce` and `pqnoenforce` set their
scope's ACCT bit and clear that scope's ENFD bit, which is precisely "accounting
without enforcement" — the semantic the contract's row 3 encodes as
`quota_state enabled` / `enforcement accounting_only`.

**Why "accounting_only" is not a guess about enforcement.** S077 line 175–177 says user
quota "accounting enabled, and limits (optionally) enforced" — the *optional* part is
what the `*noenforce` spellings switch off, and S078's `ACCT`-vs-`ENFD` split shows the
kernel distinguishing exactly those two states. So the fixture's `uqnoenforce`+`pqnoenforce`
string is the observable trace of accounting that does not enforce, and `accounting_only`
is the only enforcement token the contract can attach to it. This is not a claim that
limits are unset — the contract's stated limits (no per-user/group/project limit or
usage reading) still hold.

## 4. Contract ambiguities found (for L1 / the oracle author)

**A1 — row 3's "only `*noenforce` keys" is not stated as "and no other quota key",
and it must not be read as "and no other option at all".** The contract writes the row
as "only *noenforce keys (uqnoenforce,gqnoenforce,pqnoenforce,qnoenforce), no `noquota`".
Two readings are possible from the text alone:
(a) the *quota-related* key set is a non-empty subset of the `*noenforce` set and
contains no `noquota` — the reading used here; (b) the *entire* super-options string
contains nothing but `*noenforce` keys — which no real mount could ever satisfy, since
S078 shows the kernel always emits `rw`, `inode64`, `logbufs=…`, `logbsize=…` alongside.
Reading (b) would make row 3 unreachable in real mode and reduce the contract's
`accounting_only` enforcement token to fixture-only dead code. The contract's own
`quota_option_keys` output field ("sorted quota-related keys only, never values or
other options") shows the contract already distinguishes quota-related keys from other
options, which supports (a). **Recommendation:** state the row as "the quota-related
keys are exactly a non-empty subset of {uqnoenforce,gqnoenforce,pqnoenforce,qnoenforce},
and `noquota` is absent", and define "quota-related key" once for the whole table. This
case's expectation depends on (a): under (b) the fixture would fall through to
`xfs_quota_options_absent` / `unknown` / `QUOTA_STATE_UNKNOWN`.

**A2 — "quota key" is used in rows 1, 2, 4 and 5 without a definition, and the two
xfs rows use different key sets.** Row 2 enumerates `usrquota,uquota,quota,grpquota,
gquota,prjquota,pquota`; row 3 enumerates the four `*noenforce` names; rows 1 and 4 say
"any quota key" and row 5 says "any quota key" again, without saying which set they
mean. If "quota key" in rows 1/4/5 meant only the row-2 set, then a mount carrying
`uqnoenforce` and `noquota` would fall to row 1 (`noquota` and no quota key → `disabled`)
rather than row 4 (`unknown`/`xfs_conflicting_quota_options`) — the two answers disagree
about whether a visibly contradictory super-options string is "disabled" or "unknown".
**Recommendation:** define one set `Q` = union of row 2 and row 3 keys plus `noquota`,
then state rows 1/4/5 against `Q`. Under the natural reading (a `noenforce` key *is* a
quota key) this case is unaffected — my fixture has no `noquota` at all — but the
`noquota`+`*noenforce` combination is currently under-determined and is a plausible
sibling case.

**A3 — `qnoenforce` in row 3's list is a mount-input spelling the kernel never
reports.** S078's `xfs_showargs` emits only `uqnoenforce`, `gqnoenforce` and
`pqnoenforce`; there is no `qnoenforce` in the reported vocabulary (it exists as an
*input* option, `Opt_qnoenforce`, `xfs_super.c:116`, sharing the `Opt_uqnoenforce`
parser arm at 1553–1556). A probe that reads mountinfo can therefore never see
`qnoenforce`; keeping it in row 3 only widens the set. Harmless for this case, but the
row's list mixes input spellings with reported spellings and should say which.

**A4 — row 2's key list is likewise a mix.** `uquota`, `gquota`, `pquota` and `quota`
are accepted *mount inputs* (S077 175–185; S078 parser arms 1547–1572); what the kernel
*reports back* in the super-options column is `usrquota`, `grpquota`, `prjquota`
(S078 239/244/249). A probe reading mountinfo sees only the reported spellings. The
union is harmless here, but the contract should note that the reported vocabulary is
the one a mountinfo-only probe can observe, since it is what `quota_option_keys` will
actually contain.

**A5 — the `device_check` value is not in the compared key set, so a btrfs-shaped
`device_mismatch` cannot be pinned by this case.** The contract compares per-path
`(path, fstype, mount_point, quota_state, enforcement, basis)`; `device_check` is
output but not compared. My fixture deliberately makes the xfs device check *equal*
(`259:3` = `259:3`), so a wrong implementation that mis-mapped the device branch would
produce `unknown`/`device_mismatch` and fail the case — but a case whose device check
*should* be `btrfs_subvolume_skipped` cannot express that difference in `expected`.
Not a defect in this case; a note for whoever authors the btrfs device cases.

**A6 — the S-id binding is provisional.** `corpus/SOURCES.md` ends at S076 at the
entering revision; S077–S084 exist only as the draft in
`.ufo/waves/round-23/build/DraftSourceRows/rows.md` (status `queued`). I used that
draft's mapping — S077 = xfs.rst, S078 = xfs_super.c, S082 = proc.rst — which is
self-consistent with the contract's own pointer "per-subvolume anonymous st_dev,
**S081**" (the fifth row, `fs/btrfs/inode.c`). **If L1 renumbers the rows, the
`sources` array in this case file must be renumbered**; the rationale's file:line
anchors are unaffected and remain the load-bearing evidence.

## 5. Verification performed in this seat

- **Contract-table re-derivation, independent implementation.** I re-implemented the
  contract's §C2 rules (mountinfo parsing per S082, longest-mount-point selection,
  device check, key extraction, the five xfs rows, verdict precedence) in a throwaway
  script under `.scratch/round23/CaseXfsAccountingOnly/check.py` and ran it against my
  own fixture. It produces `exit 1`, `QUOTA_ENABLED`, and the single path
  `{path /srv/xfsacct/data, fstype xfs, mount_point /srv/xfsacct, quota_state enabled,
  enforcement accounting_only, basis xfs_quota_option}` — byte-identical to the
  `expected` object in the case file. The script is a *derivation check of my own
  reading*, not an implementation of the probe and not a substitute for the sealed
  oracle; it lives in scratch and is not part of the deliverable.
- **Case-file schema self-check.** The file parses as JSON; top-level keys are exactly
  `schema,id,scenario,fixture,expected,rationale,sources`; `fixture` keys are exactly
  `schema,mountinfo,paths,device_links,btrfs_sysfs` with `schema` =
  `mori-quota-fixture-v1`; `expected` keys are exactly `exit,finding_id,paths`; each
  expected path object has exactly `path,fstype,mount_point,quota_state,enforcement,basis`;
  every token in `quota_state`/`enforcement`/`basis` is a contract token; `sources` ⊆
  S077–S084.
- **Fixture field-layout re-parse.** Each of the 5 mountinfo lines was re-split against
  the S082 field table; all have the required shape (ID, parent ID, major:minor, root,
  mount point, mount options, optional tagged fields, `-`, fstype, source, super
  options) and the `-` separator is present in every line. The text ends with a
  trailing newline, as a real `/proc/self/mountinfo` does, matching the convention used
  by the other cases in this wave.

## 6. Tooling

No installs and no upgrades were needed or performed: `curl`, `python3`, `sha256sum`
and `stat` from the base system sufficed, and the operator's tooling directive was
therefore not triggered. Nothing was installed from any channel.

## 7. Limits of this seat's claim

- The case asserts the probe's classification of a synthetic super-options string, not
  any observed host state. The fixture's btrfs `/`, btrfs `/home`, tmpfs `/run` and xfs
  `/tmp` (`noquota`) lines are structural decoys that make the mount resolution
  non-trivial; they are **not** claimed to reproduce any observed host mount, and the
  real control remains `frozen/c2-expected-real.json`.
- No live host read was performed by this seat (my item names none), no `quotactl`,
  `btrfs`, `xfs_quota`, `repquota`, `mount` or other privileged/mutating interface was
  invoked, and no build, test, lint or gate was run.
- No statement is made about quota limits, usage, or per-user/group/project state; the
  contract's stated limits stand. `QUOTA_ENABLED` here is a runway-reporting finding,
  not a failure claim and not a claim that any limit is currently exceeded.
- The S-id→file mapping is an inference from the queued draft rows plus the contract's
  single S081 pointer (A6); the file:line anchors, not the S-ids, carry the evidence.

---

# Correction — pre-seal amendment applied (2026-10-21)

Instruction source: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/preseal-amendment.md`
(read in full before authoring) and the IRC instruction from L1 (`agent://MadoR22-2`),
which states the amendment was written **before** L1 opened any ImplQuota candidate or
ran any C2 candidate, and that no C2 result has been observed. This correction is
therefore source/falsification-driven, not result-driven; no candidate implementation,
oracle, or C2 output was read to produce it.

**Corrected case file written:** `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/cases-corrected/CaseXfsAccountingOnly.json`
(same id `CaseXfsAccountingOnly`, schema `mori-quota-case-v1`, 8035 bytes,
sha256 `e03c414b1625518c5bb88171e53e5584c72ea1d5f7e54e2bed5873600f3ba135`).

**Original proposal left untouched:** `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/cases-proposed/CaseXfsAccountingOnly.json`
(5818 bytes, sha256 `84844aac55a9507d880191bfe05747a5c0570feec24221cb2e29c7f3bb09463f`).
Its `btrfs_sysfs` record still reads `{devices, qgroups:false, qgroups_mode:null}` and
its `expected` object is unchanged; both were re-read after the correction was written to
confirm the proposal was not mutated.

## C1. Delta from the original proposal

**One fixture change, one unchanged expectation.**

| Element | Original proposal | Corrected case | Why |
|---|---|---|---|
| `fixture.btrfs_sysfs["1d02a454-…"].qgroups_enabled` | *absent* | `null` | Amendment: "Add required fixture member `qgroups_enabled` to each btrfs_sysfs UUID record: true/false/null"; "qgroups false must pair with enabled=null/mode=null". The record's `qgroups` is `false`, so `qgroups_enabled` must be `null` and `qgroups_mode` stays `null`. |
| `fixture.mountinfo` | 5 lines + trailing newline | **unchanged** | The amendment's mount-resolution and field-parse clauses change how lines are read, not what the fixture must contain. |
| `fixture.paths`, `fixture.device_links` | as proposed | **unchanged** | The amendment adds validation rules (nonempty, unique, normalized absolute; canonical `MAJ:MIN`; canonical UUID keys; plain basenames). The original fixture already satisfies all of them; verified, not altered. |
| `expected` | exit 1, `QUOTA_ENABLED`, one path (`enabled` / `accounting_only` / `xfs_quota_option`) | **unchanged** | The amendment's XFS precedence clause resolves this fixture identically to the original contract's row 3. See C2 below. |

The `btrfs_sysfs` record is a **structural decoy** in this case: no btrfs path is queried,
so its `qgroups_enabled` value cannot influence this expectation. It is corrected anyway
because the amendment makes the member required on *every* record, decoys included, and
because a record missing a required key would be a `QUOTA_SETUP` failure under the
amendment's "Missing/extra record keys setup" rule.

## C2. Re-derivation under the amendment's final C2 rules

Step-by-step against `preseal-amendment.md` §"C2 final rules superseding only
erroneous/ambiguous original clauses":

1. **Empty trailing lines ignored** — the fixture's mountinfo ends with a newline, so its
   final split element is empty and is dropped. The five remaining lines are the ones
   analysed. *(Amendment: "ignore empty trailing lines".)*
2. **Separator and last THREE fields of each chosen line** — the chosen line
   `251 33 259:3 / /srv/xfsacct rw,nosuid,nodev,noatime shared:214 - xfs /dev/nvme0n1p3 rw,inode64,logbufs=8,logbsize=256k,uqnoenforce,pqnoenforce`
   yields fstype `xfs`, source `/dev/nvme0n1p3`, super options
   `rw,inode64,logbufs=8,logbsize=256k,uqnoenforce,pqnoenforce`. *(Amendment: "Parse
   separator and the last THREE fields of EACH chosen line, never file-wide".)*
3. **Octal decode** — root `/`, mount point `/srv/xfsacct` and source `/dev/nvme0n1p3`
   contain no backslash at all, so the `040/011/012/134` decode is a no-op and no other
   escape needs rejecting. *(Amendment: "Octal-decode root, mountpoint and source with
   exactly 040/011/012/134; reject other backslash escapes as QUOTA_SETUP".)*
4. **Longest component-prefix selection** — for realpath `/srv/xfsacct/data` the covering
   mount points are `/` (explicitly a candidate) and `/srv/xfsacct` (component-prefix
   candidate); the longest wins → `mount_point /srv/xfsacct`, `fstype xfs`. The btrfs `/`
   and `/home`, tmpfs `/run` and xfs `/tmp` (`noquota`) lines cover nothing.
5. **No duplicated covering mount point** — the fixture's mount points (`/`, `/home`,
   `/run`, `/tmp`, `/srv/xfsacct`) each occur **exactly once**, so the amendment's
   `ambiguous_overmount` refusal does **not** fire. This is the point of the amendment's
   new rule, and this fixture is on the safe side of it. *(Amendment: "if ANY covering
   mountpoint occurs more than once, refuse classification as unknown/n/a/ambiguous_overmount,
   fstype=null,mount_point=null, device_check=not_checked".)*
6. **Device check preempts the filesystem table** — the chosen fstype is `xfs`, not btrfs,
   and the mount's `major:minor` `259:3` **equals** the path's `st_dev` `259:3`, so
   `device_check` is `match` and the filesystem table is reached. The btrfs
   "stat major is 0" exemption is irrelevant to an xfs path. *(Amendment: "Device mismatch
   PREEMPTS the filesystem table … Equal -> match".)*
7. **XFS precedence** — comma-splitting the super options and taking the text before `=`
   gives keys `rw, inode64, logbufs, logbsize, uqnoenforce, pqnoenforce`. Step 1
   (conflict: `noquota` with any quota/enforcement or noenforce key) does not fire,
   `noquota` is absent; step 2 (`noquota`) does not fire; step 3 (any enforced key:
   `usrquota,uquota,quota,grpquota,gquota,prjquota,pquota`) does not fire — the only
   quota-related keys present are the accounting-only spellings; step 4 (any
   accounting-only key: `uqnoenforce,gqnoenforce,pqnoenforce,qnoenforce`) **fires** →
   `quota_state enabled`, `enforcement accounting_only`, `basis xfs_quota_option`; step 5
   (absent) is not reached. The amendment's "Mixed enforced/noenforce means SOME
   quota-type enforcement flag is set" clarification does not apply — this fixture has no
   enforced key at all. *(Amendment: "XFS precedence: conflict(…), then noquota, then any
   enforced key, then any accounting-only key, else absent".)*
8. **Verdict** — one path, `enabled` → exit `1`, finding_id `QUOTA_ENABLED`.

**Result: the corrected case's expectation is byte-identical to the original proposal's**
(`exit 1`, `QUOTA_ENABLED`, path `/srv/xfsacct/data` with `fstype xfs`,
`mount_point /srv/xfsacct`, `quota_state enabled`, `enforcement accounting_only`,
`basis xfs_quota_option`). The amendment changes the *route* to that answer (its explicit
precedence list replaces the contract's table reading) but not the answer for this
fixture, which is the expected outcome: the amendment exists to fix cases whose original
expectation was wrong (ext positive arms, duplicated covering points, btrfs "present ⇒
enabled"), and this case was none of those.

## C3. Verification performed for the correction

- **Amendment-rule re-derivation.** I re-implemented the amendment's final rules
  (empty-trailing-line skip, last-three-fields per line, octal decode with escape
  rejection, longest component-prefix selection, duplicated-covering-point refusal,
  device-check preemption, the five-step XFS precedence, and the verdict precedence) in a
  throwaway script at `.scratch/round23/CaseXfsAccountingOnly/check_amended.py` and ran
  it against the corrected fixture. Output is byte-identical to the corrected `expected`
  object. The script is a derivation check of my own reading, not an implementation of
  the probe and not a substitute for the sealed oracle; it stays in scratch and is not
  part of the deliverable.
- **Fixture validation under the amendment's new input rules.** Checked in the same
  script: every `btrfs_sysfs` record has exactly `{devices, qgroups, qgroups_enabled,
  qgroups_mode}` with the required types and the `qgroups=false ⇒ enabled=null,
  mode=null` pairing; UUID keys are canonical lowercase 8-4-4-4-12; device names and
  `device_links` values are plain nonempty basenames with no slash or control char;
  `paths` is nonempty and unique with normalized absolute `path`/`realpath` (no `.` or
  `..` components); `st_dev` is canonical decimal `MAJ:MIN` with no sign and no leading
  zeros.
- **No implementation, oracle, or candidate result was read**, and no build, test, lint
  or gate was run. The only live host read in this seat remains the one already
  disclosed (§7 of the original report): none for the correction itself.

## C4. Effect of the amendment on this seat's §4 ambiguities

- **A1 (row 3's "only `*noenforce` keys") — RESOLVED, in the direction this case assumed.**
  The amendment's XFS precedence clause "then any enforced key, then any accounting-only
  key" makes the classification key-set-based rather than string-based: a mount whose
  quota-related keys are exactly a non-empty subset of the accounting-only spellings is
  `enabled`/`accounting_only` regardless of the other (non-quota) options present
  (`rw`, `inode64`, `logbufs`, `logbsize` in this fixture). This is reading (a) of A1,
  and it confirms the original expectation was the intended one. The A1
  recommendation is therefore satisfied by the amendment; the ambiguity is closed.
- **A2 ("quota key" undefined across rows 1/4/5) — RESOLVED for the xfs rows.** The
  amendment's step 1 says the conflict test is "`noquota` with **ANY** quota/enforcement
  **or** noenforce key", which fixes the previously under-determined `noquota` +
  `*noenforce` combination as a conflict (`xfs_conflicting_quota_options`), not as
  `disabled`. It also fixes the precedence order relative to the original table's row
  order. The A2 recommendation (one set `Q`) is now realised in the amendment's wording.
  No change to this case, which contains no `noquota`.
- **A3 (`qnoenforce` is an input-only spelling) — still open, still harmless.** The
  amendment's XFS clause keeps the four `*noenforce` names (via "any accounting-only
  key") without restating which the kernel can report. S078 shows the kernel reports
  only `uqnoenforce`, `gqnoenforce`, `pqnoenforce`; `qnoenforce` remains an input-only
  spelling (`Opt_qnoenforce`, `xfs_super.c:116`, sharing the `Opt_uqnoenforce` parser
  arm at 1553–1556). This case uses only the two reported spellings, so it is
  unaffected; the note stands for the rows' precision.
- **A4 (input-vs-reported spelling split) — still open, still harmless.** The amendment
  likewise keeps both vocabularies in the row-2 key set (`uquota`, `gquota`, `pquota`,
  `quota` are inputs; `usrquota`, `grpquota`, `prjquota` are what the kernel reports).
  This fixture uses only reported spellings, so it is unaffected.
- **A5 (`device_check` outside the six scored fields) — extended by the amendment.**
  The amendment adds a supplementary clause ("Output tuples remain the original six
  scored fields; supplementary sealed checks additionally verify device_check,
  quota_option_keys and qgroups_mode where given"). For this path the supplementary
  values would be `device_check "match"` and `quota_option_keys ["pqnoenforce",
  "uqnoenforce"]` (sorted, no values, no other options) — but the scored `expected`
  object deliberately carries only the six original fields, so the original six-field
  denominator stays separable from the supplementary assertions, exactly as the
  amendment requires. The corrected file keeps the six-field `expected` shape; the
  supplementary values are recorded here rather than injected into `expected`, because
  the case-file schema for `expected.paths` objects fixes the six keys.
- **A6 (S-id binding provisional) — unchanged and still load-bearing only for
  provenance.** S077 = `xfs.rst`, S078 = `xfs_super.c`, S082 = `proc.rst`, per the queued
  `DraftSourceRows/rows.md` draft, cross-checked against the contract's own S081
  pointer. The amendment adds that "registry and lesson Gate land before sourced
  knowledge admission", which confirms the ids are still forward assignments at this
  point. If L1 renumbers the rows, the `sources` array in **both** the original proposal
  and the corrected case must be renumbered; the file:line anchors are unaffected.

## C5. Final hashes

| File | Bytes | sha256 |
|---|---|---|
| `.ufo/waves/round-23/cases-proposed/CaseXfsAccountingOnly.json` (original, untouched) | 5818 | `84844aac55a9507d880191bfe05747a5c0570feec24221cb2e29c7f3bb09463f` |
| `.ufo/waves/round-23/cases-corrected/CaseXfsAccountingOnly.json` (new, corrected) | 8035 | `e03c414b1625518c5bb88171e53e5584c72ea1d5f7e54e2bed5873600f3ba135` |

(This report's own sha256 is reported to L1 in the reply rather than written here, so
that the recorded value is the hash of the final bytes of this file.)
