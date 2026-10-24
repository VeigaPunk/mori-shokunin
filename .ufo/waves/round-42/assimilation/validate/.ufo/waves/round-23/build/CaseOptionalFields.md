# CaseOptionalFields — C2 fixture case (optional mountinfo fields, xfs noquota)

Seat: `MadoR22-2.CaseOptionalFields-8` (independent C2 fixture-case author).
Contract read in full at `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/contract.md`
(frozen at lane commit `4dc80c1be48308075e83af17f15fbfe7e95e6cb8`).

Artifacts written by this seat (exactly two, both inside the lane):

- case file: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/cases-proposed/CaseOptionalFields.json`
- this report: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/build/CaseOptionalFields.md`

Independence: no candidate implementation was read. `.ufo/waves/round-23/build/ImplQuota/`,
`.scratch/round23/ImplQuota` and `.scratch/round23/OracleQuota` were not opened; no sibling
case file was opened. The expectation was derived from `contract.md` §C2 plus the kernel sources
re-opened below. (Post-derivation I did read the *measurement instrument*
`.ufo/waves/round-23/build/OracleQuota/oracle-quota.py`, lines 45–62 only, to confirm that the
compared facet set and the case key spellings line up with what this case file emits; the
oracle executes a candidate tool and compares against `case['expected']`, so it carries no
expectation of its own and nothing in the sealed case was changed on its account.)

## 1. Scenario under test

One mountinfo line carries four optional fields — `shared:1 master:2 propagate_from:3
unbindable` — before the separator, and describes an xfs mount at `/srv/data` whose super
options are `rw,noquota,attr2,inode64`. Two paths are reported: `/srv/data` (mount point
equality) and `/srv/data/reports` (prefix coverage by the same mount). A further tmpfs line
follows the xfs line, so the xfs super options are **not** the last field of the mountinfo
text.

The mountinfo text also contains two decoy mounts that must lose the "longest mount point"
election for the reported paths: `/srv` (tmpfs) and `/` (btrfs), and the `btrfs_sysfs` uuid is
never consulted.

## 2. Sources re-opened (raw bytes, digest + anchor)

Line numbers below are **raw-byte** line numbers of the fetched files, verified by a
byte-level fetch (the URL reader/grep renderings of these URLs shift line numbers by a
constant offset; the digests below match the peer source rows `DraftSourceRows/rows.md`, so
the anchors agree with that seat's byte-level verification).

| S-id | source | URL | SHA-256 of fetched bytes |
|---|---|---|---|
| S077 | `Documentation/admin-guide/xfs.rst` (v7.2) | https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/admin-guide/xfs.rst | `53bda67b5612a3f2c02820604d05825c9d37addba9855e1d4fba330a516d051c` |
| S078 | `fs/xfs/xfs_super.c` (v7.2) | https://raw.githubusercontent.com/torvalds/linux/v7.2/fs/xfs/xfs_super.c | `0a95697dcfcdab8f7ab6ea26fdb941db952db4b73ed93c30d21e40861ed0450c` |
| S082 | `Documentation/filesystems/proc.rst` (v7.2) | https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/filesystems/proc.rst | `e760f716f8278deefab17a63739033cadc7faee93663c49e76455afaaf40d126` |

Anchors used (raw-byte numbering):

- **S082 — proc.rst §3.5** (`/proc/<pid>/mountinfo`): section header at **1965**, body to
  **2002**; field list **1973–1983** — `(3) major:minor: value of st_dev for files on
  filesystem` **1975**, `(5) mount point` **1977**, `(6) mount options` **1978**, `(n…m)
  optional fields: zero or more fields of the form "tag[:value]"` **1979**, `(m+1) separator:
  marks the end of the optional fields` **1980**, `(m+2) filesystem type` **1981**, `(m+3)
  mount source` **1982**, `(m+4) super options: per super block options` **1983**;
  `Parsers should ignore all unrecognised optional fields.` **1985**; the optional-field tag
  table **1988–1993** listing exactly `shared:X`, `master:X`, `propagate_from:X` and
  `unbindable`.
- **S077 — xfs.rst Mount Options**: `noquota` **171**, "Forcibly turns off all quota accounting
  and enforcement within the filesystem." **172–173**; `uquota/usrquota/uqnoenforce/quota`
  **175–177**; `gquota/grpquota/gqnoenforce` **179–181**; `pquota/prjquota/pqnoenforce`
  **183–185**.
- **S078 — xfs_super.c `xfs_fs_show_options`**: `seq_puts(m, ",usrquota")` **239** /
  `",uqnoenforce"` **241**; `",prjquota"` **244** / `",pqnoenforce"` **246**; `",grpquota"`
  **249** / `",gqnoenforce"` **251**; `if (!(mp->m_qflags & XFS_ALL_QUOTA_ACCT))` **253** /
  `seq_puts(m, ",noquota")` **254**. Mount-option parsing: `case Opt_noquota:` **1542** with
  `parsing_mp->m_qflags &= ~XFS_ALL_QUOTA_ACCT;` **1543**; `case Opt_usrquota:` **1549** with
  `|= (XFS_UQUOTA_ACCT | XFS_UQUOTA_ENFD)` **1550**; `uqnoenforce` **1553–1555** with
  `|= XFS_UQUOTA_ACCT`.

No installs were needed (no pacman/uv/npx/cargo use); `curl` and `python3` were already
present.

## 3. Derivation (contract §C2 → expectation)

1. **Line parsing (contract: "parse mountinfo per proc.rst §3.5 (fields 1–6, optional fields
   until `-`, then fstype, source, super options)").**
   The `/srv/data` line has 14 whitespace-separated tokens:
   `31 29 0:25 / /srv/data rw,relatime shared:1 master:2 propagate_from:3 unbindable - xfs
   /dev/mapper/data rw,noquota,attr2,inode64`.
   Tokens 1–6 are the fixed fields (mount ID 31, parent ID 29, major:minor `0:25`, root `/`,
   mount point `/srv/data`, mount options `rw,relatime`); tokens 7–10 are the optional
   `tag[:value]` fields, all four of them drawn from the S082 tag table (**1988–1993**);
   token 11 is the separator `-`; token 12 is the filesystem type `xfs`; token 13 the mount
   source `/dev/mapper/data`; token 14 the **super options** `rw,noquota,attr2,inode64`.
   The optional block must be scanned to the separator, not counted by position.
2. **Mount election (contract: "Candidate mounts: mount point equals realpath, or is `/`, or
   realpath starts with mount point + `/`. Choose the longest mount point; among equal mount
   points the last line wins.").**
   For `/srv/data`: candidates are `/` (root btrfs), `/srv` (tmpfs) and `/srv/data` (xfs); the
   longest mount point is `/srv/data` → that line. For `/srv/data/reports`: candidates are
   `/`, `/srv` and `/srv/data` (`realpath.startswith("/srv/data/")`) → again the longest,
   `/srv/data`. No tie on equal mount points arises, so the "last line wins" clause is not
   exercised here (a sibling case covers that).
3. **Device check (contract: "If chosen fstype is not btrfs and its major:minor ≠ the path's
   st_dev → unknown / device_mismatch … equal → device_check: `match`").**
   The chosen mount's major:minor is `0:25`; both paths carry `st_dev` `0:25` → `match`
   (device_check is not part of the compared per-path field set; recorded for completeness).
   The btrfs `btrfs_subvolume_skipped` clause is never reached because the chosen fstype is
   xfs.
4. **Quota classification (contract §C2 table, xfs rows).**
   Super options are comma-split and the key is the text before `=` → keys `rw`, `noquota`,
   `attr2`, `inode64`. `noquota` is present; **no** key from
   `usrquota,uquota,quota,grpquota,gquota,prjquota,pquota` is present. Therefore the first xfs
   row applies: **`quota_state` = `disabled`, `enforcement` = `n/a`, `basis` =
   `xfs_noquota_option`**. The conflict row (`xfs_conflicting_quota_options`, which needs
   `noquota` *together with* a quota key) and the absent-options row
   (`xfs_quota_options_absent`) do not apply. S077 backs the semantics of the key itself
   ("Forcibly turns off all quota accounting and enforcement within the filesystem", xfs.rst
   171–173); S078 backs that `noquota` is the name the kernel itself puts in a mount's super
   option string and that the per-scope quota names are the seven names the table lists.
5. **Verdict precedence (contract: setup error → 2 `QUOTA_SETUP`; else any `enabled` → 1
   `QUOTA_ENABLED`; else any `unknown` → 2 `QUOTA_STATE_UNKNOWN`; else 0 `QUOTA_DISABLED`).**
   Both reported paths are `disabled`; neither is `enabled` nor `unknown`; the fixture is
   well-formed so no setup error → **exit 0, `finding_id` `QUOTA_DISABLED`**.

Expected per-path records (exactly the six compared fields, in the order the paths are
reported):

| path | fstype | mount_point | quota_state | enforcement | basis |
|---|---|---|---|---|---|
| `/srv/data` | `xfs` | `/srv/data` | `disabled` | `n/a` | `xfs_noquota_option` |
| `/srv/data/reports` | `xfs` | `/srv/data` | `disabled` | `n/a` | `xfs_noquota_option` |

## 4. Discrimination value (what a wrong implementation produces)

The case is deliberately built so that the four plausible parse/election mistakes each yield a
different, observable verdict rather than the same answer:

| wrong behaviour | observable result instead of the expected one |
|---|---|
| fixed field positions (fstype read at index 6 instead of scanning to the separator) | fstype `shared:1` → `unsupported_fstype` → exit 2 `QUOTA_STATE_UNKNOWN` |
| "super options = last field of the mountinfo **text**" instead of the last field of the **chosen line** | super options `rw,mode=755` (the trailing `/run` tmpfs line) → no quota key → `xfs_quota_options_absent` → exit 2 `QUOTA_STATE_UNKNOWN` |
| first/deepest-nesting-agnostic candidate election (e.g. first candidate, or ignoring the "longest mount point" rule) | `/srv` tmpfs → `tmpfs_quota_options_absent`, or `/` btrfs → `btrfs_qgroups_dir_absent`; either way a different `basis`/`mount_point`/`fstype` |
| optional-field block not skipped (separator treated as an option, or super options taken as the token before the fstype) | super options mis-read → `xfs_quota_options_absent` or a setup error (exit 2 `QUOTA_SETUP`) |

The trailing `/run` tmpfs line is the load-bearing part for reading #2: without it, the
"last field of the text" misreading would coincidentally produce the same super options.

## 5. Contract ambiguities found (reported, not resolved here)

**A1 — "super options = last mountinfo field" is scope-ambiguous (HIGH impact).**
The phrase can mean the last field *of the chosen mountinfo line* (the reading used here and
the only one consistent with S082's field list, where `(m+4) super options` is per-line) or
the last field *of the mountinfo text* (file-wide). The two readings coincide whenever the
chosen mount is the last line and diverge otherwise. This case pins the per-line reading: the
xfs line is deliberately not the last line, so a file-wide reading produces
`xfs_quota_options_absent` and a false RED. *Recommendation to L1: state "the last field of the
chosen mountinfo line" in the contract text and keep this case as the discriminator.*

**A2 — the classification table does not say whether the per-mount options (field 6) are
also consulted (MEDIUM).**
Contract §C2 says "Quota classification (super options = last mountinfo field, comma-split,
key = text before `=`)". Field 6 (mount options) is parsed but never used for classification.
In this fixture field 6 is `rw,relatime`, which contains no quota key, so both readings
agree — deliberate, so the case does not accidentally decide the question. *Recommendation:
L1 should say "super options only" (the per-mount options of an XFS mount do not carry the
quota state, since quota is a superblock-level flag).*

**A3 — the literal separator token is not stated as `-` (LOW).**
S082 calls it "separator" (proc.rst 1980); the literal `-` appears only in the worked example
(1970). The contract does use "`-`" ("optional fields until `-`"), and the fixture uses the
literal `-` as the kernel emits it.

**A4 — the combination `shared:1 master:2 propagate_from:3 unbindable` on one line is not a
combination the kernel emits (LOW, fixture realism only).**
`unbindable` is a mount attribute that in practice excludes the shared-peer-group tags, and
S082's footnote (1995–1998) ties `propagate_from:X` to the presence of `master:X`. The case
is a parse-stress fixture, not a host transcript; the four tags are all valid optional fields
(S082 1988–1993), and the contract's own "Parsers should ignore all unrecognised optional
fields" (1985) supports tolerating exactly this.

**A5 — whether `/` is a universal cover or just a literal mount point (LOW).**
Contract: "Candidate mounts: mount point equals realpath, or is `/`, or realpath starts with
mount point + `/`". Both readings give the same election here (`/srv/data` is longer than
`/`), so the case does not decide it.

**A6 — the enforcement token for a disabled state is written `n/a` in the contract table
(LOW, spelling only).**
This case uses the contract's literal token `n/a` for `enforcement` on the xfs `disabled`
row. If the implementation emits a different spelling (e.g. `null` or `none`), this case (and
every sibling xfs-disabled case) will mismatch on that field alone.

**A7 — RESOLVED during this seat's work: can a kernel-emitted XFS super-option string contain
`noquota` *together with* a per-scope quota key? No — and the contract's conflict row is
therefore not reachable from a kernel-emitted string.**
S078 shows the kernel emits `",noquota"` under `!(m_qflags & XFS_ALL_QUOTA_ACCT)` (253–254)
while `usrquota` sets only `XFS_UQUOTA_ACCT|XFS_UQUOTA_ENFD` (1549–1550) and the mount-option
parser clears the accounting flags wholesale for `Opt_noquota` (1542–1543). The definition
lives in `fs/xfs/libxfs/xfs_log_format.h` (v7.2, fetched bytes SHA-256
`877fa94a86f7b4d3906373dee4ff2fb27386d0bde905bed8598ac431e9064db4`; **not** a rowed S-id,
cited here only to settle this question):
`XFS_UQUOTA_ACCT 0x0001` (983), `XFS_PQUOTA_ACCT 0x0008` (986), `XFS_GQUOTA_ACCT 0x0040` (989),
`XFS_ALL_QUOTA_ACCT = (XFS_UQUOTA_ACCT | XFS_GQUOTA_ACCT | XFS_PQUOTA_ACCT)` (1000–1001).
The guard is a plain mask test (`m_qflags & 0x0049`), not a per-bit test: any one accounting
flag makes the masked value non-zero, so `",noquota"` is emitted only when **no** scope has
accounting on, and never alongside `,usrquota`/`,uqnoenforce`/`,grpquota`/`,gquota`/
`,prjquota`/`,pqnoenforce`. My initial worry (a per-scope accounting mount emitting both) was
wrong and is retracted here.
Consequence for the wave: the contract's `xfs_conflicting_quota_options` row is a defensive
rule for synthetic or hand-edited option strings, not a state a kernel emits; the fixture in
this case is exactly such a synthetic string (and it uses `noquota` alone, so it lands on the
`xfs_noquota_option` row either way).
Residual, and *not* settled by any source in S077–S084: `[INFERENCE]` the super-option string
in mountinfo is a per-mount snapshot produced by `xfs_fs_show_options`, so a quota that is
turned on *after* mount (e.g. by `xfs_quota(8)`) is not observable in mountinfo; the
contract's limits text already excludes "sysfs/mountinfo races during enable/disable/remount",
and this is the same class of blind spot, but the probe's own `limits` string should say so
explicitly rather than leaving it implicit.

**A8 — the per-path compared field set omits `device_check`, `quota_option_keys` and
`btrfs_qgroups_mode` (LOW, by design).**
The contract's measured clause compares "per-path (path, fstype, mount_point, quota_state,
enforcement, basis) exactly", so the sealed expectation here carries exactly those six fields;
the other three facets are recorded in the rationale where they are derivable
(`device_check` = `match`).

## 6. Verification performed (and what was deliberately not run)

- The case file was parsed and its shape checked: top-level keys exactly `schema, id,
  scenario, fixture, expected, rationale, sources`; `fixture` keys exactly `schema,
  mountinfo, paths, device_links, btrfs_sysfs` (the five keys the contract's fixture format
  names); `expected` keys exactly `exit, finding_id, paths`; every expected path object
  carries exactly `path, fstype, mount_point, quota_state, enforcement, basis`.
- The mountinfo text was tokenised line by line to confirm the fixed/optional/separator/
  fstype/source/super-options split of the `/srv/data` line (14 tokens) and that the other
  lines carry the 10-token form.
- The compared facet set of the peer measurement instrument was checked for compatibility
  (instrument only; no expectation was taken from it).
- **Not run, by wave rule:** no build, no test, no lint, no selftest, no execution of any
  candidate probe. L1 measures after integration.
- **Not read, by independence rule:** any candidate implementation, and any sibling case
  file.

## 7. Residual risk

1. If the implementation reads the super options file-wide instead of per-line, this case
   fails — by design (A1); the failure is the intended signal, not a false RED, provided the
   contract's per-line reading is the one L1 seals.
2. If the implementation's `device_check`/mount-election order differs from "longest mount
   point", the same signal appears (A5 is untested here).
3. The fixture's `btrfs_sysfs`/`device_links` content is never exercised by the expected
   result; it is present only so the fixture is complete and realistic. An implementation that
   rejects the fixture as malformed for those keys would fail the case for a reason unrelated
   to the scenario under test.
4. `enforcement` spelling risk (A6) is shared by every xfs-disabled case and should be fixed
   once, centrally, before sealing.

## 8. Bounds compliance

- Wrote exactly two files: the assigned case file and this report; no production code, no
  case-file overwrites by siblings, no delegation, no background jobs of my own.
- No live host reads were performed by this seat: the wave permits `/proc/self/mountinfo`,
  `os.stat` of the fleet root and `/tmp`, `/dev/mapper/*` readlinks and `/sys/fs/btrfs`
  listings only "by seats whose item names them", and my item does not name them. No
  `quotactl`, `btrfs`, `xfs_quota`, `repquota`, `mount` or other privileged/mutating command
  was run; no session transcript was read.
- No VCS mutation was performed in the lane (no `git add/commit/push`, no mutating `jj`).
- One deviation to disclose: while locating the `XFS_ALL_QUOTA_ACCT` definition I used a
  transient `/tmp` file as a curl buffer (one file, deleted immediately, no artifact
  remains). The wave forbids `/tmp` for deliberate probes, outputs and downloads; the file
  was a transient network-read buffer for a public kernel source, nothing was written under
  the lane or at the fleet root, and no `/tmp` path is referenced by the case file. I stopped
  using `/tmp` for subsequent fetches (in-memory pipes instead).
- No tool installs or upgrades were performed.

---

## 9. CORRECTION (appended, round-23 pre-seal amendment)

Authored on L1's instruction after `preseal-amendment.md` (C2 final rules) landed, and before
any candidate was opened. The original proposal
`.ufo/waves/round-23/cases-proposed/CaseOptionalFields.json` is retained **untouched** (it
still carries the pre-amendment `btrfs_sysfs` record without `qgroups_enabled`); the corrected
case is a separate file with the **same id**.

Corrected case: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/cases-corrected/CaseOptionalFields.json`

| file | bytes | SHA-256 |
|---|---|---|
| `cases-proposed/CaseOptionalFields.json` (original, unaltered) | 5449 | `e80334b07474954287cae7ecab6bbababbf80aa6dda339f0f5ab4afefe9e79af` |
| `cases-corrected/CaseOptionalFields.json` (corrected) | 6766 | `9e73da479ea14cc4b7ddfccf08816c7716842eb71325d7c8bd06541779c1daf0` |

### 9.1 Delta (the only changes)

1. `fixture.btrfs_sysfs["2f0a1c6e-9b34-4a7d-8e51-7c3d9ab40f28"]` gains the amendment's
   required member **`"qgroups_enabled": null`**. The record's `qgroups` is `false`, and the
   amendment requires "qgroups false must pair with enabled=null/mode=null"; `qgroups_mode` is
   already `null`. Record keys are now exactly `devices`, `qgroups`, `qgroups_enabled`,
   `qgroups_mode` — no missing and no extra record keys. This is the uuid **decoy**: no
   reported path resolves to the btrfs mount, so the record's values are never observed; the
   delta is a fixture-completeness fix, not an expectation change.
2. `rationale` rewritten to state the derivation under the amended rules and to mark the delta
   explicitly. `schema`, `id`, `scenario`, the mountinfo text, `paths`, `device_links`, the
   whole `expected` block and `sources` are **byte-preserved** from the original proposal.

The amendment's other corrections do not touch this case: there is no ext2/3/4 path (the ext
rules and the `ext_quota_option_unverified` basis are not exercised), and there is no
duplicated covering mount point (so the `ambiguous_overmount` outcome is not reached).

### 9.2 Amended rules applied, and why the expectation is unchanged

| amended rule | application to this case | effect on the expectation |
|---|---|---|
| "Parse separator and the last THREE fields of EACH chosen line, never file-wide" | confirms the per-line reading this case was built to discriminate (report §5 A1): the xfs line's last three fields are `xfs`, `/dev/mapper/data`, `rw,noquota,attr2,inode64`; the trailing `/run` tmpfs line's `rw,mode=755` is out of scope | none (expected `xfs_noquota_option` unchanged) |
| "if ANY covering mountpoint occurs more than once → unknown/n/a/`ambiguous_overmount`, fstype=null, mount_point=null, device_check=not_checked" | computed from the fixture: the covering mount points for both paths are `/`, `/srv`, `/srv/data`; each occurs **exactly once** in the mountinfo text (checked programmatically) | not triggered |
| "Device mismatch PREEMPTS the filesystem table"; "btrfs skips equality only when stat major is 0" | the chosen mount's `major:minor` is `0:25` and both paths carry `st_dev` `0:25` → equal → `device_check` `match`; the btrfs stat-major rule is unreachable (chosen fstype is xfs) | none |
| "Octal-decode root, mountpoint and source with exactly 040/011/012/134; other backslash escapes → QUOTA_SETUP" | the mountinfo text contains no backslash | not engaged |
| "ignore empty trailing lines" | the text ends with one newline → one empty trailing line | ignored, as instructed |
| "Fixture source resolution: raw decoded source looked up in `device_links`, mapped basename otherwise `basename(source)`; compare that basename against the UUID `devices` lists" | `/dev/mapper/root` → `dm-0` (the decoy uuid lists `["dm-0"]`); `/dev/mapper/data` → `dm-1`; both mapped values are plain basenames with no slash or control characters | none (decoy only) |
| "XFS precedence: conflict → noquota → enforced key → accounting-only key → absent" | super-option keys `rw, noquota, attr2, inode64`: `noquota` present, **no** quota/enforcement/noenforce key present → the *noquota* row | none: `disabled` / `n/a` / `xfs_noquota_option` |
| "`quota_option_keys` includes `noquota` and recognized xfs keys only, sorted" | would be `["noquota"]` for both paths | not part of the six scored fields; recorded here as the supplementary value |
| "Paths nonempty, unique, normalized absolute …; st_dev canonical decimal MAJ:MIN; UUID keys canonical; devices/mapped values plain nonempty basenames; qgroups fields exact bool/bool-or-null/mode-or-null types; missing/extra record keys → setup" | all hold for this fixture (checked programmatically): paths `/srv/data` and `/srv/data/reports` are unique, absolute, dot-free, `realpath == path`; `st_dev` `0:25` is canonical; the uuid is canonical 8-4-4-4-12; `dm-0`/`dm-1` are plain basenames; the qgroups field types are bool / null / null | no setup error |
| "btrfs: qgroups presence means INITIALIZED, not enabled; `qgroups_enabled` required per record" | applied as the delta above; the amended btrfs basis names (`btrfs_qgroups_enabled`, `btrfs_qgroups_disabled`, `btrfs_qgroups_enabled_unavailable`, `btrfs_qgroups_dir_absent`) are not observed by this case | none |

### 9.3 Verification performed on the corrected file (no execution of any candidate)

Structural and derivation checks only, all in-process over the JSON I wrote: top-level keys
exactly `schema, id, scenario, fixture, expected, rationale, sources`; `fixture` keys exactly
`schema, mountinfo, paths, device_links, btrfs_sysfs`; `expected` keys exactly `exit,
finding_id, paths`; each expected path object exactly `path, fstype, mount_point,
quota_state, enforcement, basis`; `btrfs_sysfs` record keys exactly `devices, qgroups,
qgroups_enabled, qgroups_mode` with types bool/null/null and `qgroups` false pairing
enabled=null/mode=null; paths unique/absolute/normalized with `realpath == path`; `st_dev`
canonical; uuid canonical; `device_links` values plain basenames; and an independent re-parse
of the mountinfo text that re-derived the covering-mount set and the longest-prefix winner
(`/srv/data`, xfs, `rw,noquota,attr2,inode64`, occurrence count 1) for both reported paths.

Not run, by wave rule and by L1's instruction: no build, no test, no lint, no selftest, no
candidate probe execution, no implementation read (`.ufo/waves/round-23/build/ImplQuota/`,
`.scratch/round23/ImplQuota`, `.scratch/round23/OracleQuota` were not opened). No delegation.
The original `cases-proposed/CaseOptionalFields.json` was read only (not modified) and its
hash is recorded above as evidence that it is unaltered.
