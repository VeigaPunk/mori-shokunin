# CaseSymlinkRealpath — C2 fixture case (symlinked path under `/home` whose realpath is on the xfs `/tmp` mount)

Seat: `MadoR22-2.CaseSymlinkRealpath-8` (reviewer, leaf member, no subagent dispatch).
Case file written (the only file written): `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/cases-proposed/CaseSymlinkRealpath.json` — sha256 `e7c4018a4044827873520dbcddc17508258122c97a23c2a3017a45020a772473`, 5042 bytes.
Contract read in full: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/contract.md` (frozen at lane commit `4dc80c1be48308075e83af17f15fbfe7e95e6cb8`).
Independence honoured: no candidate implementation was read (`.ufo/waves/round-23/build/ImplQuota/`, `.scratch/round23/ImplQuota/`), no oracle was read (`.ufo/waves/round-23/build/OracleQuota/`), no sibling case proposal in `cases-proposed/` was read. The expectation below is derived only from contract §C2 and the Linux v7.2 kernel sources named below.

Disclosure of what *was* read besides the contract and the kernel sources: the `DraftSourceRows` seat's draft `build/DraftSourceRows/rows.md` (the S077–S084 id→URL table, used only for the id attribution recorded in §3 and ambiguity A3), and excerpts of peer *reports* under `build/` (`CaseXfsConflict.md` in full for house style and its shape note, plus grep excerpts of `CaseUnsupported.md`, `CaseXfsDevMismatch.md`, `CaseBtrfsUnmapped.md`, `CaseBtrfsSquota.md`, `CaseXfsMixedEnforce.md`, `CaseXfsOptionsAbsent.md`, `CaseTmpfsUsrquota.md`, `ScoutPriorQuota.md`) obtained while locating the S-id mapping. No peer **case JSON** was opened; the `cases-proposed/` directory was only listed by name, never read. The expectation itself was re-derived from the contract and the kernel sources after the fixture was written, and the derivation in §2 stands on those alone.

## 1. What the case asserts

A path given as `/home/vgpnk/Projects/shokunin/link-to-tmp`, whose realpath is `/tmp/mori-quota-target`, must be classified against the **realpath's** covering mount — the xfs mount at `/tmp` with `noquota` in its super options — while the emitted `path` field echoes the **given** path.

| path (output) | fstype | mount_point | quota_state | enforcement | basis |
|---|---|---|---|---|---|
| `/home/vgpnk/Projects/shokunin/link-to-tmp` | xfs | /tmp | disabled | n/a | `xfs_noquota_option` |
| `/tmp/mori-quota-target` | xfs | /tmp | disabled | n/a | `xfs_noquota_option` |

Verdict: **exit 0, `finding_id` `QUOTA_DISABLED`**.

Row 2 is a control on the same mount (direct, unsymlinked). It pins that the mount-derived fields are identical for a path reached through a symlink and one reached directly, and that `path` in the output is the given path in both rows (for row 2 given path == realpath, so the two readings coincide there — that is why row 1 carries the discriminating weight).

The discriminating property of the case: the fixture contains a **btrfs mount at `/home`** (plus a btrfs root mount at `/`), so an implementation that resolved the covering mount from the *given* path rather than the realpath would select `/home` and report `btrfs` / `btrfs_qgroups_dir_absent`. An implementation that echoed the *realpath* in the output would report `path = /tmp/mori-quota-target` for row 1. Both are wrong under the contract, and both fail this case.

Fixture (`mori-quota-fixture-v1`, exact five keys `schema`, `mountinfo`, `paths`, `device_links`, `btrfs_sysfs`):

- `mountinfo` — seven realistic lines per proc.rst §3.5 (field (3) major:minor, (4) root, (5) mount point, (6) mount options, one optional `shared:N` tag, `-` separator, filesystem type, mount source, super options):

```
21 30 0:26 / /proc rw,nosuid,nodev,noexec,relatime shared:12 - proc proc rw
22 30 0:27 / /sys rw,nosuid,nodev,noexec,relatime shared:7 - sysfs sysfs rw
23 30 0:6 / /dev rw,nosuid,relatime shared:3 - devtmpfs devtmpfs rw,size=4023424k,nr_inodes=1005856,mode=755
25 30 0:30 / / rw,relatime shared:1 - btrfs /dev/mapper/root rw,compress=zstd:3,ssd,discard=async,space_cache=v2,subvolid=5,subvol=/
65 33 0:30 /@home /home rw,relatime shared:33 - btrfs /dev/mapper/root rw,compress=zstd:3,ssd,discard=async,space_cache=v2,subvolid=257,subvol=/@home
82 25 0:76 / /dev/shm rw,nosuid,nodev,noexec,relatime,size=16326424k shared:36 - tmpfs tmpfs rw,inode64
244 33 259:1 / /tmp rw,relatime shared:34 - xfs /dev/nvme0n1p1 rw,inode64,logbufs=8,logbsize=256k,noquota
```

  The two btrfs lines are deliberate decoys. `/` is a covering-mount candidate for every path, but the longest mount point wins, and `/home` is not a prefix of either probed realpath — it is only a prefix of the *given* path, which is the trap the case exists to close. The `/dev/shm` tmpfs line is a third decoy: it carries no quota option, so a resolver that picked it would report `tmpfs` / `tmpfs_quota_options_absent`.
- `paths` — two entries, each with exactly `path`, `realpath`, `st_dev`:
  - `path=/home/vgpnk/Projects/shokunin/link-to-tmp`, `realpath=/tmp/mori-quota-target`, `st_dev=259:1`
  - `path=/tmp/mori-quota-target`, `realpath=/tmp/mori-quota-target`, `st_dev=259:1`
- `device_links` — `{"/dev/mapper/root": "dm-0"}`.
- `btrfs_sysfs` — one synthetic uuid `3f6a1c02-9b4d-4e57-8a31-0d5e7c9b2a48` listing `dm-0`, `qgroups: false`, `qgroups_mode: null`. Present with the exact contract shape, inert for this case (no probed path resolves to a btrfs mount).

The `st_dev` value is the decisive one and it is stated by the contract, not guessed: real-mode inputs are `os.stat(path).st_dev` and `os.path.realpath(path)`, and `os.stat` follows symlinks, so a path under `/home` whose target is on the xfs `/tmp` filesystem reports the **xfs** device `259:1`, not the btrfs device of the directory holding the symlink. The fixture therefore carries `259:1` for row 1, and the chosen mount's field (3) is also `259:1`, so the non-btrfs device check passes.

## 2. Derivation, step by step

**(a) Which contract row applies.** Contract §C2 quota-classification table, xfs rows, against super options `rw,inode64,logbufs=8,logbsize=256k,noquota`:

1. `noquota` and no quota key → disabled / n/a / `xfs_noquota_option` — **MATCHES**.
2. any of `usrquota,uquota,quota,grpquota,gquota,prjquota,pquota` and no `noquota` → enabled / enforced / `xfs_quota_option` — fails: `noquota` is present and no quota key is.
3. only *noenforce keys, no `noquota` → enabled / accounting_only / `xfs_quota_option` — fails: `noquota` is present.
4. `noquota` together with any quota key → unknown / n/a / `xfs_conflicting_quota_options` — fails: no quota key is present.
5. neither `noquota` nor any quota key → unknown / n/a / `xfs_quota_options_absent` — fails: `noquota` is present.

Row 1 is the unique matching row, so the expectation does not depend on any unstated row-ordering convention.

**(b) Which field carries the tokens.** Contract: "super options = last mountinfo field, comma-split, key = text before `=`". The fixture places `noquota` only in the last field of the `/tmp` line; the mount-options field (6) is `rw,relatime` and carries no quota token, so the case is not sensitive to a field-6 vs field-m+4 misreading. Key extraction of the last field gives `rw`, `inode64`, `logbufs`, `logbsize`, `noquota` — `logbufs=8` and `logbsize=256k` yield keys `logbufs`/`logbsize`, which are not quota keys, and `noquota` is not one of the seven quota keys either, so it satisfies "no quota key" while satisfying the `noquota` condition.

**(c) Mount resolution.** Contract: candidate mounts are those whose mount point equals the realpath, is `/`, or is a prefix (realpath starts with mount point + `/`); the **longest** mount point wins, ties broken by the last line. For realpath `/tmp/mori-quota-target`: `/tmp` qualifies (prefix), `/` qualifies (root), `/home` does not, `/dev/shm` does not, `/proc`, `/sys`, `/dev` do not. `/tmp` (4 characters) beats `/` (1 character), so the chosen mount is the xfs line, and `mount_point` in the output is the mount's own mount point `/tmp` — not the path and not the realpath.

**(d) Device check.** Contract: for a non-btrfs chosen fstype, a major:minor ≠ the path's `st_dev` yields `unknown` / `device_mismatch`. The xfs line's field (3) is `259:1`; row 1's `st_dev` is `259:1` (see §1: `os.stat` follows the symlink) and row 2's is `259:1`. The check passes, so the `xfs_noquota_option` row — not `device_mismatch` — is the basis reached. Note the counterfactual: had the fixture carried the btrfs device `0:30` for row 1, the contract would have produced `unknown` / `device_mismatch` and exit 2, which is a different case (and is already covered by `CaseXfsDevMismatch`).

**(e) Verdict.** Contract §C2 verdict precedence: setup error → 2; else any `enabled` → 1 `QUOTA_ENABLED`; else any `unknown` → 2 `QUOTA_STATE_UNKNOWN`; else 0 `QUOTA_DISABLED`. Both reported paths are `disabled` — no `enabled`, no `unknown` — so **exit 0, `QUOTA_DISABLED`**.

**(f) The `path` field.** Contract §C2 output: `paths: [{path, fstype, mount_point, quota_state, enforcement, basis, device_check, quota_option_keys, btrfs_qgroups_mode}]`, where the input is the CLI `--path ABS`. The contract does not say the emitted `path` is the realpath, and the real-mode input list pairs `os.path.realpath(path)` (used for resolution) with the path itself (used for output and for `os.stat(path).st_dev`). The seat brief for this case states the intent explicitly: "classification uses realpath while output path echoes the given path". So row 1's emitted `path` is `/home/vgpnk/Projects/shokunin/link-to-tmp`. This is recorded as ambiguity **A1** below.

## 3. Source anchors actually relied on

| S-id | source | anchor used | what it fixes |
|---|---|---|---|
| **S077** | `Documentation/admin-guide/xfs.rst` (v7.2) | `noquota:171-173` — "noquota / Forcibly turns off all quota accounting and enforcement within the filesystem."; quota families `175-185` | the meaning of the `noquota` super option: quota off, hence `disabled` / `n/a`, and the fact that the enforcement column is `n/a` rather than `enforced` |
| **S078** | `fs/xfs/xfs_super.c` (v7.2) | `xfs_fs_show_options` quota emission `238-254`, in particular `253-254`: `if (!(mp->m_qflags & XFS_ALL_QUOTA_ACCT)) seq_puts(m, ",noquota");` | that the kernel emits `noquota` in the super-options string exactly when no quota accounting flag is set, i.e. `noquota` alone is the kernel's own "no quota" rendering, not a hand-made contradiction |
| **S081** | `fs/btrfs/inode.c` (v7.2) | `btrfs_getattr:8215-8218`, `stat->dev = BTRFS_I(inode)->root->anon_dev;` (`:8246`) | that the btrfs decoy mount's device number legitimately differs from a stat device (per-subvolume anonymous device), i.e. the btrfs branch would tolerate a device mismatch — used only to justify why the btrfs lines in the fixture are inert |
| **S082** | `Documentation/filesystems/proc.rst` (v7.2) | §3.5 `/proc/<pid>/mountinfo:1965-1990`; field table `1970-1983` (major:minor field 3 at `:1975`, separator m+1 at `:1980`, filesystem type m+2 at `:1981`, mount source m+3 at `:1982`, super options m+4 at `:1983`) | the mountinfo line shape used to author the fixture text, and the "scan to the separator, do not count fixed positions" requirement the `shared:N` optional fields exercise |

S-ids S079 (btrfs sysfs), S080 (btrfs qgroup) and S083/S084 (ext4, tmpfs docs) were **not** relied on: no probed path reaches a btrfs mount (so the `btrfs_qgroups_dir_present` / `btrfs_qgroups_dir_absent` rows are not reached and S079/S080 are unnecessary), and no ext or tmpfs mount covers a probed path (S083/S084 unnecessary). The `/dev/shm` tmpfs decoy is never chosen, so its classification row is not exercised either.

The S-id ↔ source mapping used here is the one drafted by the `DraftSourceRows` seat in `build/DraftSourceRows/rows.md` (S077 = xfs.rst, S078 = xfs_super.c, S079 = btrfs sysfs.c, S080 = btrfs qgroup.c, S081 = btrfs inode.c, S082 = proc.rst, S083 = ext4.rst, S084 = tmpfs.rst). It is corroborated independently by the contract's own text, which names **S081** as the source of the per-subvolume anonymous `st_dev` (`fs/btrfs/inode.c`) and cites **proc.rst §3.5** for the mountinfo layout. `corpus/SOURCES.md` still ends at S076; these rows are not yet written, so the mapping is a *derivation*, not a registry read — see ambiguity **A3**.

## 4. Contract ambiguities found

**A1 — the emitted `path` is the given path, but the contract never says so.** §C2 says only "Output (one JSON object): … `paths: [{path, fstype, …}]`" and lists `os.path.realpath(path)` among the real-mode inputs. It does not state whether `path` is the requested path or its resolved form. The seat brief for this case states the intended reading ("output path echoes the given path"), and it is the only reading under which `--path` and the output correspond one-to-one and under which a caller can correlate a report row with the path it asked about. I derived the case on that reading; an implementation that echoes the realpath would fail row 1. **L1 should make the wording explicit in the contract** ("`path` is the path as given on the command line / in the fixture `paths[]` entry"), because this is the single most likely divergence between an implementation and every case that involves a symlink or a non-identity realpath.

**A2 — `os.stat` vs `os.lstat` for the `st_dev` of a symlinked path is implied, not stated.** The contract lists `os.stat(path).st_dev` (follows symlinks) and `os.path.realpath(path)` as two separate inputs. `os.stat` following the symlink is what makes the device check coherent for a symlinked path: the given path's own directory is on a different filesystem than its target, and a `lstat`-style device would produce `device_mismatch` for a path whose realpath is legitimately on the chosen mount. My fixture encodes the `os.stat` reading (`st_dev = 259:1` for a path spelled under `/home`). **The contract should say explicitly that `st_dev` is `os.stat` (symlink-following) and not `os.lstat`**, because the two readings give different verdicts for exactly this case shape and nothing in §C2 disambiguates them for a reader who has not seen the CLI list.

**A3 — the S-id → source mapping is not yet in the registry, so "sources: S-ids among S077–S084" is only satisfiable by derivation.** `corpus/SOURCES.md` ends at S076; S077–S084 exist only as the `DraftSourceRows` draft in `build/DraftSourceRows/rows.md` and as the contract's own two hints (S081 = btrfs `anon_dev`; proc.rst §3.5 for mountinfo). The contract's C2 header says "sourced: S077–S084, opened this round, see lesson23 Gate" — a `lesson23` Gate that does not exist yet in `corpus/lessons/`. Until the rows are written and the Gate is sealed, every case author's `sources` list is a *provisional* attribution, and two seats could attribute the same kernel file to different S-ids. This is the same class of defect the round-22 lesson records as M1 (scalar/identity substitution): the id ↔ file binding must be frozen, not inferred per case. **Recommendation to L1: freeze the S077–S084 rows (or an explicit id→URL table) in a commit before the cases are sealed, and have the oracle validate each case's `sources` against that frozen table.**

**A4 — three different key vocabularies now exist for the same expectation shape.** The contract's output object uses `exit_code` and `finding_id`; the frozen control `frozen/c2-expected-real.json` uses `expected_exit`, `expected_finding_id`, `expected_paths` **and includes `device_check`** in each path row; the case-file instruction (and therefore my case) uses `exit`, `finding_id`, `paths` with the six compared fields `(path, fstype, mount_point, quota_state, enforcement, basis)`. A sibling case report (`CaseXfsConflict.md`) raises the same observation. The oracle must map the case-file shape onto the tool's output shape explicitly (and must decide whether `device_check`, `quota_option_keys` and `btrfs_qgroups_mode` are compared at all — the contract's "Measured" paragraph compares only the six). My case follows the case-file instruction exactly and includes no seventh field, so it is comparable under the six-field rule. **Recommendation: L1 states in the seal note which fields the oracle compares, and the oracle's mapping is written down before any implementation lands.**

**A5 — "the path's st_dev" in the device-check sentence is ambiguous about *which* path.** The sentence reads "If chosen fstype is not btrfs and its major:minor ≠ the path's st_dev", where "the path" could mean the requested path, the realpath, or the mount-relative path. All three coincide except for a symlinked path, where the requested path's *lexical* parent device differs from the resolved one. Given §C2 resolves the mount from the realpath, "the path's st_dev" must mean the realpath's (equivalently, `os.stat` of the requested path, which follows the link). My case is the one case in the set where this distinction is load-bearing, so it is worth stating in the contract rather than leaving to the reader.

**A6 — no tie-break case is specified for equal-length mount points in the fixture form.** The contract fixes "among equal mount points the last line wins", which my fixture exercises trivially (no duplicates). Not a defect in this case, recorded only because the fixture form allows duplicate mount points and a case author could construct a duplicate-point ambiguity that the contract's rule resolves but a *line-order-dependent* implementation might not. Flagged to L1 as a fixture-lint consideration, not a contract defect.

## 5. Verification performed

- The case file was re-read with a JSON parser and every structural constraint was checked programmatically: top-level keys exactly `schema, id, scenario, fixture, expected, rationale, sources`; fixture keys exactly `schema, mountinfo, paths, device_links, btrfs_sysfs`; each `paths[]` entry exactly `path, realpath, st_dev` with an absolute path and a well-formed `MAJ:MIN`; each `btrfs_sysfs` entry exactly `devices, qgroups, qgroups_mode` with a boolean `qgroups`; `expected` exactly `exit, finding_id, paths`; each expected row exactly the six compared fields; every `quota_state`, `enforcement` and `basis` value drawn from the contract's token vocabulary; `sources` ⊆ {S077…S084}.
- The fixture's seven mountinfo lines were parsed independently with the proc.rst §3.5 algorithm (scan to the `-` separator, then fstype, source, super options) and the contract's candidate/longest-mount-point rule was applied to each `realpath`; the resulting chosen mount, fstype, `mount_point`, device pair and quota-key set reproduce the expected rows exactly, and the resulting verdict is exit 0 / `QUOTA_DISABLED`.
- These are static checks of my own artifact only. **No build, test, lint, oracle or tool was executed** (per the wave's no-execution rule), and no implementation, oracle or peer case was read.

## 6. Files

- Case (original proposal, left byte-unchanged by both corrections): `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/cases-proposed/CaseSymlinkRealpath.json` (sha256 `e7c4018a4044827873520dbcddc17508258122c97a23c2a3017a45020a772473`)
- Corrected case, §7 (preserved as evidence of a self-inconsistent artifact): `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/cases-corrected/CaseSymlinkRealpath.json` (sha256 `ef8eeaa03fa2576d8c9e666acfa4b3c38f765d4cde0b6ff1cacda26a78e7eefb`)
- **Sealing candidate, §8:** `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/cases-corrected/CaseSymlinkRealpath-final.json` (sha256 `275c360585a93e2f1bc7e2ded0f4cd42b07d5b0eeb16b9790d1980f456b0d07e`)
- This report: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/build/CaseSymlinkRealpath.md`

Beyond the three case files listed above, no other file was created or modified. No tool was installed or updated by this seat.

---

## 7. Correction — round-23 pre-seal amendment (appended after the amendment was issued, before any candidate was opened)

Amendment read in full: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/preseal-amendment.md`.
Corrected case authored: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/cases-corrected/CaseSymlinkRealpath.json` — sha256 `ef8eeaa03fa2576d8c9e666acfa4b3c38f765d4cde0b6ff1cacda26a78e7eefb`.
Original proposal left byte-unchanged: `cases-proposed/CaseSymlinkRealpath.json`, sha256 still `e7c4018a4044827873520dbcddc17508258122c97a23c2a3017a45020a772473` (verified after the correction was written).
No implementation was read and no test was run: this is a static re-derivation of my own case against the amended clauses.

### 7.1 Deltas — exactly two, and nothing else moved

| # | Where | Change | Mandated by |
|---|---|---|---|
| D1 | `fixture.btrfs_sysfs["3f6a1c02-…"].qgroups_enabled` | **added**, value `null` | amendment: "Add required fixture member `qgroups_enabled` to each btrfs_sysfs UUID record: true/false/null. qgroups false must pair with enabled=null/mode=null." The record's `qgroups` is `false` (the qgroups directory is absent), so `qgroups_enabled` is `null`, not `true` and not `false` |
| D2 | `fixture.paths[1].path` / `.realpath` | `/tmp/mori-quota-target` → `/tmp/mori-quota-target-dir` (a synthetic rename) | amendment: "Paths nonempty, unique, normalized absolute path/realpath". The original two rows shared one realpath, which fails the strict reading of "unique"; renaming the second synthetic directory makes the fixture valid under **both** readings (unique path entries, or unique path *and* realpath alike) at zero cost to the expectation, since row 2 is a direct path on the same xfs `/tmp` mount and its five mount-derived fields are unchanged |

Everything else is byte-identical to the original proposal: the `mountinfo` text, `device_links`, `paths[0]`, the whole `expected` object (exit, finding_id and both six-field rows), `scenario`, `sources`, and the top-level key set and `schema`/`id`. The `rationale` string was rewritten to state the deltas and the re-derivation; no other field changed.

### 7.2 Re-derivation under the amended clauses — the expectation is unchanged

- **btrfs rules (amended)** — the amended btrfs table adds `btrfs_qgroups_enabled` / `btrfs_qgroups_disabled` / `btrfs_qgroups_enabled_unavailable` and redefines dir-presence as *initialised*, not *enabled*. **Not reached**: the chosen mount for both probed paths is the xfs mount at `/tmp`. The btrfs lines in the fixture exist only as the foil for a resolver that wrongly used the given path; if such a resolver picked `/home` it would report the btrfs branch, and the case would fail — which is the intended discrimination, not an ambiguity.
- **ext rule (amended)** — "ext2/3/4: quota_state ALWAYS unknown … basis `ext_quota_option_unverified` when any quota-related option key is present". **Not reached**: the fixture contains no ext2/3/4 mount at all. (Note for the other seats: this amendment changes every ext-positive case's expected basis from `ext_quota_option` to `ext_quota_option_unverified` and its `quota_state` to `unknown` — my case is unaffected.)
- **`ambiguous_overmount` (amended)** — "if ANY covering mountpoint occurs more than once, refuse classification as unknown/n/a/`ambiguous_overmount`, fstype=null, mount_point=null, device_check=not_checked". **Not triggered**: the covering mount points for realpath `/tmp/mori-quota-target` are `/tmp` and `/`, and every mount point in my seven-line mountinfo occurs exactly once (`/proc`, `/sys`, `/dev`, `/`, `/home`, `/dev/shm`, `/tmp` — seven distinct strings). The duplicate-mountpoint rule therefore cannot change my expectation, and no `ambiguous_overmount` row is asserted.
- **Device mismatch preempts the filesystem table (amended)** — my chosen fstype is xfs and its field (3) `259:1` equals both rows' `st_dev` `259:1`, so there is no mismatch and the preemption never fires. (Had the fixture carried the btrfs device, the amended rule would preempt with `unknown`/`n/a`/`device_mismatch` — that is `CaseXfsDevMismatch`'s territory, not this case.)
- **XFS precedence (amended)** — "conflict(noquota with ANY quota/enforcement or noenforce key), then noquota, then any enforced key, then any accounting-only key, else absent". The `/tmp` super options are `rw,inode64,logbufs=8,logbsize=256k,noquota`; `noquota` is present and no quota/enforcement/noenforce key is, so the **noquota** row applies exactly as before: `disabled` / `n/a` / `xfs_noquota_option`. The amended ordering changes nothing here because only one of the branches is satisfied.
- **Per-line parsing of the last three fields (amended)** — "Parse separator and the last THREE fields of EACH chosen line, never file-wide". My fixture's `/tmp` line is `244 33 259:1 / /tmp rw,relatime shared:34 - xfs /dev/nvme0n1p1 rw,inode64,logbufs=8,logbsize=256k,noquota`; the three fields after the separator are `xfs`, `/dev/nvme0n1p1`, and the super options. The `shared:34` optional field sits *before* the separator and is skipped, so the case is sensitive to a parser that reads the wrong tail. `quota_option_keys` for this mount is `["noquota"]` (the amended rule admits `noquota` and recognized xfs keys only, sorted).
- **Trailing empty line (amended)** — "ignore empty trailing lines". My mountinfo text ends with `\n`, so it has one empty trailing line. Under the *original* clause "unparseable mountinfo line → exit 2 `QUOTA_SETUP`" that empty line was arguably an unparseable line, i.e. the original proposal carried a latent setup-error reading. The amendment removes that hazard, and the trailing newline is realistic (a real `/proc/self/mountinfo` ends with one). I kept it deliberately rather than trimming, because the amendment's rule is now explicit — and I flag the pre-amendment hazard here so the change is visible rather than silent.
- **Verdict** — both rows are `disabled`: no `enabled` and no `unknown` path, so **exit 0, `QUOTA_DISABLED`**, unchanged.

### 7.3 Supplementary sealed-check values (recorded, not asserted in the case file)

The amendment adds supplementary checks on `device_check`, `quota_option_keys` and `qgroups_mode` "where given", while the six scored fields remain the denominator. To keep the six-field denominator byte-identical to the original proposal I did **not** add those fields to `expected.paths[]`. Their values, for the record and for a supplementary check that wants them, are:

| row | path | device_check | quota_option_keys | btrfs_qgroups_mode |
|---|---|---|---|---|
| 1 | `/home/vgpnk/Projects/shokunin/link-to-tmp` | `match` | `["noquota"]` | `null` |
| 2 | `/tmp/mori-quota-target-dir` | `match` | `["noquota"]` | `null` |

### 7.4 New ambiguity surfaced by the amendment (A7)

**A7 — "Paths nonempty, unique" does not say whether *realpath* must be unique too.** Read one way it constrains the list (no duplicate entries); read another way it constrains both `path` and `realpath` (so two given paths may not share a target). The strict reading would forbid the most natural symlink case shape — probing a symlink and its target — so I judge the list-level reading the intended one, but I did not rely on that judgement: D2 makes the corrected case valid under both readings at no cost, and the original proposal's shape is preserved untouched for L1 to rule on. If L1 rules that unique realpaths are required, the corrected case is already conformant; if L1 rules the opposite, D2 remains harmless.

### 7.5 Files after the correction

- Corrected case: `.ufo/waves/round-23/cases-corrected/CaseSymlinkRealpath.json` — sha256 `ef8eeaa03fa2576d8c9e666acfa4b3c38f765d4cde0b6ff1cacda26a78e7eefb`
- Original proposal (untouched): `.ufo/waves/round-23/cases-proposed/CaseSymlinkRealpath.json` — sha256 `e7c4018a4044827873520dbcddc17508258122c97a23c2a3017a45020a772473`
- This report (appended): `.ufo/waves/round-23/build/CaseSymlinkRealpath.md`

Static validation of the corrected case was performed with a JSON parse plus a re-implementation of the amended resolution/classification rules: every structural key set, absolute/normalized path, canonical `MAJ:MIN`, UUID/basename shape, `qgroups_enabled` pairing, duplicate-mountpoint check, device preemption, XFS precedence, per-line last-three-field parsing and the verdict precedence all reproduce the asserted expectation. No build, test, lint, oracle or tool was executed, and no implementation or oracle was read.

---

## 8. Second correction — self-consistency defect in the §7 artifact (final artifact)

Detected by L1's static pre-seal check, not by me. Final artifact authored: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/cases-corrected/CaseSymlinkRealpath-final.json` — sha256 `275c360585a93e2f1bc7e2ded0f4cd42b07d5b0eeb16b9790d1980f456b0d07e` (8615 B).
The §7 artifact `cases-corrected/CaseSymlinkRealpath.json` (sha256 `ef8eeaa03fa2576d8c9e666acfa4b3c38f765d4cde0b6ff1cacda26a78e7eefb`) and the original proposal `cases-proposed/CaseSymlinkRealpath.json` (sha256 `e7c4018a4044827873520dbcddc17508258122c97a23c2a3017a45020a772473`) are both **preserved byte-unchanged as evidence**; the intermediate file is deliberately *not* repaired in place, so the defect and its correction both stay visible.

### 8.1 The defect

My §7 delta D2 renamed the second fixture path to `/tmp/mori-quota-target-dir` but I did **not** update the corresponding expected row, whose `path` member still read `/tmp/mori-quota-target`. The artifact therefore asserted two contradictory paths: `fixture.paths[1].path != expected.paths[1].path`. The oracle compares the *ordered per-path tuples* `(path, fstype, mount_point, quota_state, enforcement, basis)`, so this artifact would have failed on the `path` member alone, in every run, regardless of the implementation's correctness.

**Why my own validation missed it.** My static checker compared `fstype`, `mount_point`, `quota_state`, `enforcement` and `basis` against a re-derivation, and separately checked structural key sets — but it never asserted the *equality of the `path` member between a fixture entry and its expected row*. I validated the five derived fields and assumed the sixth was trivially the same string I had typed on both sides. It was not. The defect was in the artifact, not in the reasoning: the rename was gratuitous, and the rule that would have caught it (`fixture.paths[i].path == expected.paths[i].path` for every `i`, in order) is exactly the oracle's own comparison rule, so it should have been the first assertion in my checker rather than an omission. L1's pre-seal check found it before any candidate was opened, which is the process working as intended; recorded here as my miss, not as a process failure.

### 8.2 The fix, and the ruling it rests on

The final artifact restores the original second path and realpath (`/tmp/mori-quota-target` for both) and leaves the expected object **unchanged** from the original proposal. The §7 D2 rename is dropped entirely. Consequence: the final artifact differs from the original proposal in exactly one place — the mandated `qgroups_enabled: null` member on the single `btrfs_sysfs` UUID record. `mountinfo`, `paths` (both entries), `device_links`, the whole `expected` object, `scenario`, `sources`, the top-level key set and `schema`/`id` are byte-identical to the original proposal.

L1's ruling settles **A7** from §7.4: "Unique means given path only, sharing realpath is allowed (normal symlink scenario)." So the amended "Paths nonempty, unique" clause constrains the *given* path entries, not the realpaths. Row 1 (a symlink given under `/home`) and row 2 (its target, given directly) legitimately share the realpath `/tmp/mori-quota-target` — that is the ordinary symlink case shape, not a fixture defect. My earlier reading (list-level uniqueness) is confirmed, but the final artifact no longer depends on the reading at all: it satisfies both readings, because the shared realpath is now restored and the given paths are distinct.

### 8.3 Re-derivation — unchanged, and now with the missing assertion

Everything re-derived in §7.2 still holds: the chosen mount is the xfs mount at `/tmp` (longest covering mount point for realpath `/tmp/mori-quota-target`), the device check does not preempt (259:1 = 259:1), the amended XFS precedence selects the `noquota` row (`disabled` / `n/a` / `xfs_noquota_option`), the btrfs, ext and `ambiguous_overmount` clauses are not reached, and the verdict is **exit 0 `QUOTA_DISABLED`**. The final static check now asserts, in addition to everything checked before, that `fixture.paths[i].path == expected.paths[i].path` for every `i` in order — it passes for both rows.

### 8.4 Which artifact to seal

**`cases-corrected/CaseSymlinkRealpath-final.json`** (sha256 `275c360585a93e2f1bc7e2ded0f4cd42b07d5b0eeb16b9790d1980f456b0d07e`) is the sealing candidate for id `CaseSymlinkRealpath`. The two other files with the same id are evidence, not candidates: `cases-proposed/CaseSymlinkRealpath.json` (the original proposal, superseded) and `cases-corrected/CaseSymlinkRealpath.json` (the §7 artifact, self-inconsistent, retained to show the defect and its correction). If the sealer keys on filename rather than id, note that three files in the tree now carry id `CaseSymlinkRealpath`; only the `-final` one is consistent.
