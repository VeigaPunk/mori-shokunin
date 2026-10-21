# QExt4Journaled — round-23 C2 falsification report (fixture mode, sealed case CaseExt4Journaled)

Seat: `QExt4Journaled` · Wave: round-23 · Claim: **C2** (coverage / quota observability) · Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin`
Receipt: `.ufo/waves/round-23/falsify/QExt4Journaled/scan.json`
Scratch (all deliberate artifacts): `/fast/scratch/hyaku/mori-r23/QExt4Journaled/`

## 0. Axes named (godspeed)

| axis | measured by | result |
|---|---|---|
| A1 exit-code fidelity | measured `exit` vs sealed `expected.exit` | **match** (2) |
| A2 finding-id fidelity | measured `finding_id` vs sealed `expected.finding_id` | **match** (`QUOTA_STATE_UNKNOWN`) |
| A3 ordered six-field tuple | per-path `(path, fstype, mount_point, quota_state, enforcement, basis)` in order | **match** (1/1 primary) |
| A4 non-disclosure (supplementary) | option values / mount sources / device basenames / UUIDs absent from stdout | **clean** |
| A5 byte identity of inputs | case sha256, tool sha256, pinned-revision equality | **clean** |
| A6 scope discipline | fixture mode only, one child, 384 MiB AS, 15 s, scratch-only | **clean** |

No axis was traded off against another; nothing was edited to make an axis green.

## 1. Exact execution (the only invocation performed)

```
cd /fast/scratch/hyaku/mori-r23/QExt4Journaled
export TMPDIR=/fast/scratch/hyaku/mori-r23/QExt4Journaled
timeout --signal=KILL 15 prlimit --as=402653184 -- \
  python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-quota-surface.py \
  --fixture /fast/scratch/hyaku/mori-r23/QExt4Journaled/fixture.json \
  >stdout.txt 2>stderr.txt
```

* argv (preserved verbatim in the receipt): `["python3","-I","/home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-quota-surface.py","--fixture","/fast/scratch/hyaku/mori-r23/QExt4Journaled/fixture.json"]`
* address-space limit `402653184` bytes (384 MiB), timeout `15` s, signal `KILL`, children `1`.
* **Fixture mode only.** `--path` was never passed; no real-mode run was performed; no host quota interface was touched (no `quotactl`, `btrfs qgroup`, `xfs_quota`, `repquota`, mount, qgroup or mode read, no `/sys/fs/btrfs` inspection).
* `stdout` 988 bytes, `stderr` empty (`""`), process exit status `2`.

## 2. Input byte identities

| item | path | sha256 |
|---|---|---|
| sealed case | `.ufo/waves/round-23/frozen/quota-cases/CaseExt4Journaled.json` | `d317ccb1141271ed0cda2d2b2209fcfb965b57016e6dfc4e0efcf34560c9fb40` |
| seal decision cross-check | `frozen/case-decisions.json` → `selected_sha256` for `CaseExt4Journaled` | `d317ccb1141271ed0cda2d2b2209fcfb965b57016e6dfc4e0efcf34560c9fb40` — **identical** |
| copied fixture | `/fast/scratch/hyaku/mori-r23/QExt4Journaled/fixture.json` | `8b59b774f8c0147d360d7230596a5f92c96653a5ccb9547515686af04311ff11` |
| tool (worktree) | `tools/mori-quota-surface.py` | `e485741334d2e72a0f007481f1d2bc5b38658f54c04232965e4bbf552b8f7e92` |
| tool at pinned production `f3dc07c0bf423cc1947d0ffa91afa9ce236fbe3c` | `git show f3dc07c0…:tools/mori-quota-surface.py` | `e485741334d2e72a0f007481f1d2bc5b38658f54c04232965e4bbf552b8f7e92` — **identical** |
| tool at lane HEAD `6eb889c037163e4886eaa61501258910d6a529b9` | `git show HEAD:tools/mori-quota-surface.py` | `e485741334d2e72a0f007481f1d2bc5b38658f54c04232965e4bbf552b8f7e92` — **identical** |

The fixture was produced by copying `case["fixture"]` verbatim out of the sealed case (no key added, removed or reordered). The sealed case file was **not** modified; expected bytes untouched.

Fixture conformance re-checked by hand against the amendment: top-level keys exactly `{schema, mountinfo, paths, device_links, btrfs_sysfs}`; one unique, normalized, absolute path `/srv/journal/data`; `st_dev` canonical decimal `8:2`; btrfs UUID key canonical, record keys exactly `{devices, qgroups, qgroups_enabled, qgroups_mode}` with `qgroups=false` paired to `qgroups_enabled=null` and `qgroups_mode=null`.

## 3. Given vs actual

**Given (sealed expectation, primary six fields only)**

```
exit 2
finding_id QUOTA_STATE_UNKNOWN
/srv/journal/data | ext4 | /srv/journal | unknown | n/a | ext_quota_option_unverified
```

**Actual (measured stdout)**

```json
{"df_covers_quota":false,"exit_code":2,"finding_id":"QUOTA_STATE_UNKNOWN",
 "limits":"…","paths":[{"basis":"ext_quota_option_unverified","btrfs_qgroups_mode":null,
 "device_check":"match","enforcement":"n/a","fstype":"ext4","mount_point":"/srv/journal",
 "path":"/srv/journal/data","quota_option_keys":["jqfmt","usrjquota"],
 "quota_state":"unknown"}],"schema":"mori-quota-surface-v1"}
```

**Comparison**

* exit: `2` vs `2` → match.
* finding_id: `QUOTA_STATE_UNKNOWN` vs `QUOTA_STATE_UNKNOWN` → match.
* ordered six-field tuple, path 0:
  `["/srv/journal/data","ext4","/srv/journal","unknown","n/a","ext_quota_option_unverified"]`
  vs the same six values → **match**. Path count 1 vs 1.
* Primary denominator for this seat: **1/1**, reported separately from supplementary metadata.

## 4. Supplementary metadata (asserted apart, never folded into the six-field denominator)

| field | actual | assessment |
|---|---|---|
| `device_check` | `match` | correct: mountinfo field 3 `8:2` equals the probed path `st_dev` `8:2`, so the device-mismatch preemption must not fire; the btrfs stat-major-zero exemption is irrelevant to an ext4 mount |
| `quota_option_keys` | `["jqfmt","usrjquota"]` | keys only, sorted, drawn from the amended ext vocabulary; the `usrjquota`/`jqfmt` presence selects `ext_quota_option_unverified` over `ext_quota_superblock_unobservable` |
| `btrfs_qgroups_mode` | `null` | correct: the chosen mount is ext4 and no mode text is ever projected for it; in real mode the tool never reads the mode attribute (safety correction) |

No supplementary field exists in the sealed expectation for this case, so these are reported as observations, not as scored assertions.

## 5. Non-disclosure checks (supplementary, all negative)

Tokens searched in the measured stdout: `aquota.user` **absent**, `vfsv0` **absent**, `/dev/sda2` **absent**, `/dev/mapper/root` **absent**, `dm-0` **absent**, UUID `1d02a454-c549-4a35-b567-89d60902af8e` **absent**. Only the mount point `/srv/journal` appears, which is a required scored field. The quota file name carried by `usrjquota=aquota.user` is not echoed anywhere in stdout or stderr — this closes the non-disclosure property the case rationale recorded as a gap (the six-field tuple has no slot for it).

## 6. Derivation cross-check (case ↔ amendment ↔ sources ↔ implementation)

1. **Mount resolution.** Path `/srv/journal/data` (realpath identical). Covering mounts in the fixture mountinfo: the btrfs root line (mount point `/`) and the ext4 line (mount point `/srv/journal`). Longest component-prefix wins → `/srv/journal`, fstype `ext4`, mountinfo `8:2`. The amendment's *ambiguous-overmount* refusal does **not** fire here: each covering mount point occurs exactly once, and the chosen mount's `parent_id` is `1`, which is precisely the `mount_id` of the longest strictly-shorter cover (`/`), so no parent-id conflict exists. (The tool implements this in `resolve_mount`.)
2. **Field layout.** Six fixed fields, optional fields up to the `-` separator, then fstype/source/super-options as the last three fields of that line — per `S082` = `Documentation/filesystems/proc.rst:1985` ("Parsers should ignore all unrecognised optional fields."), locally verified at `evidence/sources/S082-Documentation_filesystems_proc.rst:1985`, with `(m+4) super options` at `:1983`. The ext4 line carries the optional field `shared:7` and no octal escapes, so root/mountpoint/source decode unchanged.
3. **Device check.** fstype `ext4` (not btrfs) and `8:2 == 8:2` → `match`; the mismatch preemption must not fire.
4. **Classification.** The pre-seal amendment supersedes the original ext rows: for ext2/3/4 `quota_state` is **always** `unknown` with enforcement `n/a`; a present quota-related option key selects basis `ext_quota_option_unverified`, otherwise `ext_quota_superblock_unobservable`. The super options are `rw,user_xattr,acl,jqfmt=vfsv0,usrjquota=aquota.user` → two quota-related keys present → `ext_quota_option_unverified`. This is anchored in `S083` = `Documentation/admin-guide/ext4.rst:262` ("These options are ignored by the filesystem."), locally verified at `evidence/sources/S083-Documentation_admin-guide_ext4.rst:262`, with `jqfmt=<quota type>, usrjquota=<file>, grpjquota=<file>` at `:267`.
5. **Verdict.** No path is `enabled`; the single path is `unknown` → exit `2` / `QUOTA_STATE_UNKNOWN`. The original contract's ext→`enabled` rows (which would have produced `QUOTA_ENABLED`, exit 1) are exactly what the amendment removed; the sealed case reflects the amended rule.
6. **Implementation correspondence.** `tools/mori-quota-surface.py` (sha `e4857413…`) implements the amended rows: `EXT_QUOTA_KEYS` includes `noquota` and `jqfmt`; the ext branch returns `("unknown","n/a","ext_quota_option_unverified")` whenever any ext quota key is present, else `("unknown","n/a","ext_quota_superblock_unobservable")` — and never returns `enabled` for ext.

The sealed expectation is therefore derivable from the amendment plus the two named kernel sources, and the implementation reproduces it exactly.

## 7. Frozen contradiction and what this seat does *not* excuse

`evidence/frozen-contradiction.json` records the round's strict red in **a different** sealed case, `CaseEscapedSpace` (selected mount id 43, parent id 33 vs longest strictly-shorter cover `/srv` id 42; the sealed rule requires `unknown / n/a / ambiguous_overmount`, while the frozen expectation row says `enabled / enforced / xfs_quota_option`). That case was **not** executed by this seat and is **not** excused by this report; its red remains a mismatch, and the global C2 strict target stays **UNPROVABLE at 29/30** (`measure4/summary.json`: `c2.pass 29 / total 30`). This seat's green arm changes nothing about that total and is not offered as a substitute for it.

Also not confused with the quota selftest arm: the `49/49` selftest arm (`evidence/quota-selftest-corrected.json`, after the separate co-evolved fixture-input correction) is a different fixture family and carries no weight for or against this sealed case.

## 8. Scope discipline observed

* Fixture mode only; real mode never invoked; no live host quota read of any kind.
* No frozen case, expectation, oracle or production byte was edited; no commit, add, push or jj mutation in the lane.
* All deliberate scratch lives under `/fast/scratch/hyaku/mori-r23/QExt4Journaled/`; `TMPDIR` pointed there; nothing was written to `/tmp`.
* Exactly one child process was spawned; 384 MiB address-space cap and 15 s timeout applied via `prlimit`/`timeout`.
* No builds, linters, formatters, full suites or gates were run; no subagent dispatch.
* No quota tooling (`quotactl`, `xfs_quota`, `repquota`, `btrfs qgroup`), no mount operations, no remediation.
* The only files written by this seat: the assigned receipt `.ufo/waves/round-23/falsify/QExt4Journaled/scan.json` and this report `.ufo/waves/round-23/falsify/QExt4Journaled.md`.

## 9. Tooling

No installs or updates were required or performed. Existing tools used: `python3` 3.14.8 (`/usr/bin/python3`), `prlimit` util-linux 2.42.4 (`/usr/bin/prlimit`), coreutils `timeout` (`/usr/bin/timeout`), `git` read-only (`show`/`rev-parse`/`status`/`log`).

## 10. Verdict and residual risk

**Seat verdict: PASS.** The sealed case `CaseExt4Journaled` reproduces exactly under the pinned production tool in fixture mode: exit `2`, `finding_id QUOTA_STATE_UNKNOWN`, and the ordered six-field tuple `(/srv/journal/data, ext4, /srv/journal, unknown, n/a, ext_quota_option_unverified)` — 1/1 primary for this seat, with supplementary metadata (`device_check=match`, `quota_option_keys=["jqfmt","usrjquota"]`, `btrfs_qgroups_mode=null`) reported apart and no option value, mount source, device basename or UUID leaked.

Residual risk / verification gaps (bounded, non-blocking for this seat):

1. This is a single-case, single-run observation: no repetition, so any nondeterminism in the tool would not be exposed by this arm.
2. The `device_check` and `quota_option_keys` values are not sealed expectations for this case; they are reviewed observations and are not scored.
3. Fixture mode never exercises the real-mode input path (mountinfo from `/proc/self/mountinfo`, `os.stat`, sysfs listing, `qgroups/enabled`); real-mode behaviour for an ext4 mount is covered by the frozen real control and by other seats, not here.
4. The seat verifies the case's *implementation correspondence*, not the case's *authorship independence*; the independence claim belongs to the seal and the case-decision record, both of which are consistent here (`selected_sha256` matches the sealed file byte-for-byte, decision reason: "Independent source-derived pre-measurement correction; exact author bytes, no L1 expectation edits").
5. The global C2 strict red in `CaseEscapedSpace` is untouched by this seat and remains an open, reported mismatch; the C2 coverage claim must stay UNPROVABLE at 29/30 on the strength of that case alone.
