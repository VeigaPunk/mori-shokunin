# QHostLike — falsification of sealed C2 case `CaseHostLike.json`

Seat: `QHostLike` (reviewer, wave 23 falsification) · lane `/home/vgpnk/Projects/shokunin/mori-shokunin`
Receipt: `.ufo/waves/round-23/falsify/QHostLike/scan.json` (sha256 `73b61453e08d2db69a0f081998530103bd4a3ae5d0109ea08d77313b6e86b98b`)
Scratch: `/fast/scratch/hyaku/mori-r23/QHostLike/` (no `/tmp` use)

## Verdict

**MATCH.** The sealed case `CaseHostLike` reproduces exactly against the production
quota-surface probe in fixture mode: exit `0`, `finding_id` `QUOTA_DISABLED`, and both
ordered six-field tuples identical to the sealed expectation. No mismatch, no excuse,
no expected-byte edit. This is a falsification seat for **one** case; it makes no claim
about the frozen `CaseEscapedSpace` strict red (another seat) and no claim about the
wave denominator.

## Bound identities (exact bytes)

| item | value |
|---|---|
| seal commit | `22772c10f6e3c1d8d3fe1b72083a6194e9f4e687` (`round-23: seal all oracle inputs before production implementation`, 2026-10-21T15:10:59-03:00) |
| production pin | `f3dc07c0bf423cc1947d0ffa91afa9ce236fbe3c` (`round-23: correct co-evolved selftest device input while preserving strict red`, 2026-10-21T15:25:42-03:00) |
| seal is ancestor of pin | yes (`git merge-base --is-ancestor` → 0) |
| tool path (canonical runtime) | `/home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-quota-surface.py` |
| tool sha256 | `e485741334d2e72a0f007481f1d2bc5b38658f54c04232965e4bbf552b8f7e92` |
| tool git blob at pin **and** at HEAD `6eb889c` | `439ff4c1a68fc4f98182c6b855b3b4c790286851` — identical; the working copy is byte-identical to the pinned production blob (no local drift) |
| case file | `.ufo/waves/round-23/frozen/quota-cases/CaseHostLike.json` |
| case sha256 (worktree) | `f4580093a6aa93eab53bef9c9f61667a2a0aa2224096b60568140904b148a63c` |
| case sha256 **at the seal commit** | `f4580093a6aa93eab53bef9c9f61667a2a0aa2224096b60568140904b148a63c` — unchanged |
| case sha256 (author lane `cases-corrected/`) | `f4580093a6aa93eab53bef9c9f61667a2a0aa2224096b60568140904b148a63c` — identical to the sealed copy |
| original proposal `cases-proposed/CaseHostLike.json` | `e83132fc329dc28dcd1e6ebdc51c645c78b9f8a15b5ffe701f7c75de793c9d93` — retained, untouched; its `expected` block is byte-equal to the frozen one (the amendment delta was fixture-shape only) |
| sealed oracle `oracle-quota.py` sha256 | `f1f4a027728180436fc5161171b0f6ad4ca4176229b5240aabb33e3f2af36bec` — identical to the blob at the seal commit |

The tool was **absent** at the seal commit (`git show <seal>:tools/mori-quota-surface.py`
→ "exists on disk, but not in <seal>"), so the seal-before-implementation ordering holds
for this claim. Canonical runtime is unique: exactly one production path
`tools/mori-quota-surface.py`; the wave-1 candidate copies live only under
`.ufo/waves/round-23/build/ImplQuota/` (`mori-quota-surface.py`, `-v2.py`, `-v3.py`) and
were not the measured runtime.

## Source derivation and rule basis read

* `.ufo/waves/round-23/contract.md` §C2 — original classification table, CLI, output
  shape, verdict precedence, limits vocabulary.
* `.ufo/waves/round-23/preseal-amendment.md` — the superseding clauses actually applied
  here: btrfs `qgroups` presence = *initialized*, not enabled (the `qgroups_enabled`
  fixture member is mandatory); device-mismatch preemption with the btrfs **stat major 0**
  equality skip; mount resolution by longest component-prefix covering mount, with
  duplicate-covering-point and parent-id refusal; `ambiguous_overmount` ⇒
  `fstype=null, mount_point=null, device_check=not_checked, quota_option_keys=[]`; XFS
  precedence conflict → noquota → enforced → accounting-only → absent; device source
  resolution by raw decoded source through `device_links`; fixture type/pairing rules.
* `corpus/knowledge/quota-surface-r23.md` — the recorded decision table and the
  "resolve the mount before interpreting its mechanism" rule (S082/S085), plus the final
  pre-seal mode-safety qualification (real mode never reads `qgroups/mode`).
* `corpus/SOURCES.md` rows S077–S082 — the six sources the case cites
  (XFS options / XFS emission / btrfs sysfs / btrfs qgroup lifecycle / btrfs anon st_dev /
  proc mountinfo layout), all present with `on-release` verification.
* `tools/mori-quota-surface.py` — `resolve_mount` (421), `covering_mounts` (407),
  `classify_btrfs` (465), `classify` (487), `evaluate` (513), `verdict` (561),
  `probe_fixture` (681), `load_fixture` (695), `payload` (774), `option_keys` (347),
  `quota_option_keys` (360).

## The one bounded fixture-mode execution

Fixture copied **verbatim** from `case["fixture"]` into the seat scratch
(`json.dumps(fixture, indent=2, sort_keys=True) + "\n"`), fixture sha256
`b07ec77d0b40dae50f2f1ece1359e695e23a1a7c8b2b4a696c61f58c3aa0caee`, content-equal to
the case fixture (verified structurally, not by digest alone).

```
/usr/bin/timeout 15 /usr/bin/prlimit --as=402653184 \
  /usr/bin/python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-quota-surface.py \
  --fixture /fast/scratch/hyaku/mori-r23/QHostLike/fixture.json
```

`TMPDIR=/fast/scratch/hyaku/mori-r23/QHostLike`, one child at a time, 384 MiB address
space, 15 s wall timeout. Exit **0**; stdout 1193 bytes sha256
`e8ad07bf9a873b43e1663ba392a83c394c3fa3cf025865a8a707579b2f6b0a17`; stderr empty
sha256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`. A repeat
invocation produced the identical stdout digest (deterministic). **Real mode was never
invoked**; no host quota read was performed by this seat.

### Primary comparison — six scored fields, ordered

| # | path | field | expected (sealed) | actual | match |
|---|---|---|---|---|---|
| 0 | `/home/vgpnk/Projects/shokunin` | fstype | `btrfs` | `btrfs` | ✅ |
| | | mount_point | `/home` | `/home` | ✅ |
| | | quota_state | `disabled` | `disabled` | ✅ |
| | | enforcement | `n/a` | `n/a` | ✅ |
| | | basis | `btrfs_qgroups_dir_absent` | `btrfs_qgroups_dir_absent` | ✅ |
| 1 | `/tmp` | fstype | `xfs` | `xfs` | ✅ |
| | | mount_point | `/tmp` | `/tmp` | ✅ |
| | | quota_state | `disabled` | `disabled` | ✅ |
| | | enforcement | `n/a` | `n/a` | ✅ |
| | | basis | `xfs_noquota_option` | `xfs_noquota_option` | ✅ |

`exit` expected `0` = actual `0`; `finding_id` expected `QUOTA_DISABLED` = actual
`QUOTA_DISABLED`; ordered tuple lists equal; 0 extra and 0 missing paths.

### Supplementary metadata — kept separate from the primary denominator

`CaseHostLike` declares **no** `supplementary_expected` block (only `CaseBtrfsDevMatch`
does, across the 30 sealed cases), so these three fields are not part of the scored
expectation. Observed, and checked against the values the case rationale states in prose:

| path | `device_check` | `quota_option_keys` | `btrfs_qgroups_mode` | rationale agrees |
|---|---|---|---|---|
| `/home/vgpnk/Projects/shokunin` | `btrfs_subvolume_skipped` | `[]` | `null` | ✅ |
| `/tmp` | `match` | `["noquota"]` | `null` | ✅ |

Schema `mori-quota-surface-v1`; output key set exactly
`{schema, finding_id, exit_code, paths, df_covers_quota, limits}`; `df_covers_quota`
`false`; `limits` a non-empty string. Per-path key set exactly the nine fields. No
`error` token (not a setup error).

### Leakage

Independent canary scan (oracle's own `canaries`/`leakage_hits` applied to this stdout):
uuid `b3f1c2d4-…`, mount sources `/dev/mapper/root` and `/dev/sda2`, option tokens
`subvolid=256`, `subvol=/@`, `subvol=/@home`, `logbufs=8`, `logbsize=32k`, device
basename `dm-0` — **0 hits**. No option value, mount source or UUID appears in the
output.

## Independent corroboration (not the wave driver)

* **Sealed oracle v3 re-run, single case.** The committed `oracle-quota.py`
  (`f1f4a027…`, byte-identical to the seal-commit blob) was re-run against a
  one-case directory holding a byte-identical copy of the sealed case:
  `counts {total 1, pass 1, unmet 0, capability_absent 0}`,
  `supplementary_counts {total 9, pass 9, unmet 0}`, finding
  `R23_C2_QUOTA_CASES_MATCH`, oracle exit `0`, headline `{exit_match true,
  finding_match true, paths_match true}`. This is a single-case rerun of the sealed
  harness — the wave denominator is untouched by it.
* **Wave measure4 cross-check.** `.ufo/waves/round-23/evidence/measure4/c2-after-observed.json`
  row for `CaseHostLike.json` is `status: pass` with
  `{exit_match true, finding_match true, paths_match true}`; wave counts
  `{total 30, pass 29, unmet 1}` — the single unmet row is the frozen `CaseEscapedSpace`
  strict red, owned by another seat. The before-arm in the same directory is
  `capability_absent 30/30` (tool absent at the entering revision), so the C2
  before→after contrast is intact.

## Discriminating probes (all synthetic, fixture-mode, seat scratch only)

The case is only meaningful if the tool actually discriminates the branches it claims.
24 mutated fixtures (each one child, same 384 MiB / 15 s bound, no production, frozen or
oracle byte touched) confirm the branches are live rather than hard-coded:

| probe | mutation | result |
|---|---|---|
| P1 | `/tmp` st_dev `8:2`→`8:3` | `QUOTA_STATE_UNKNOWN` exit 2, `/tmp` → `unknown/n/a/device_mismatch` (mismatch preempts the table) |
| P2 | qgroups present + `enabled=true` | `QUOTA_ENABLED` exit 1, btrfs → `enabled/unknown/btrfs_qgroups_enabled` |
| P3 | qgroups present + `enabled=null` | `QUOTA_STATE_UNKNOWN` exit 2, btrfs → `unknown/n/a/btrfs_qgroups_enabled_unavailable` (never silently disabled) |
| P4 | drop `noquota` from the xfs super options | `/tmp` → `unknown/n/a/xfs_quota_options_absent`, exit 2 |
| P5 | duplicate `/home` covering mount point | `unknown/n/a/ambiguous_overmount`, `fstype=null`, `mount_point=null`, `device_check=not_checked`, `quota_option_keys=[]` |
| P6 | btrfs st_dev major ≠ 0 (`259:57`) | `unknown/n/a/device_mismatch` (the major-0 equality skip does **not** generalise) |
| P7 | remove the `device_links` entry | btrfs → `unknown/n/a/btrfs_device_unmapped` |
| P8 | `qgroups: null` | `QUOTA_SETUP` `fixture_btrfs_qgroups` (null is not a valid qgroups type) |
| P9 | qgroups present + `enabled=false` | `disabled/n/a/btrfs_qgroups_disabled` (initialized-but-disabled ≠ absent) |
| P10 | `/home` line parent id `25`→`99` (id absent from snapshot) | no refusal — absent parent id is unknown topology, per the amendment |
| P11 | `/home` line parent id `25`→`77` (absent) | no refusal (same rule) |
| P12 | `/home` line parent id `25`→`29` (present in snapshot, ≠ ancestor id) | `unknown/n/a/ambiguous_overmount` — the parent-id refusal fires |
| N1 | `qgroups=false` + `enabled=true` | `QUOTA_SETUP` `fixture_btrfs_qgroups_pairing` |
| N2 | `enabled=false` + `qgroups_mode="qgroup"` | `QUOTA_SETUP` `fixture_btrfs_mode_pairing` |
| N3 | `enabled=true`, mode `squota` | `enabled/unknown/btrfs_qgroups_enabled`, mode projected `squota`, exit 1 |
| N4 | a second uuid also lists `dm-0` | `unknown/n/a/btrfs_device_unmapped` (zero-or-several uuid rule) |
| G1 | `paths: []` | `QUOTA_SETUP` `fixture_paths` (production rejects an empty path list) |
| G2 | extra key in a path entry | `QUOTA_SETUP` `fixture_path_entry` |
| G3 | missing `realpath` in a path entry | `QUOTA_SETUP` `fixture_path_entry` |
| G4 | unparseable mountinfo line | `QUOTA_SETUP` `mountinfo_line_unparseable` |
| O1 | reverse the mountinfo line order | same verdict — the longest covering mount still wins, no line-order dependence |
| O2 | mount point `/srv\040data` | decoded to `/srv data`, matching path, verdict preserved |
| O3 | invalid backslash escape `\051` | `QUOTA_SETUP` `mountinfo_escape_invalid` (only 040/011/012/134 accepted) |
| O4 | trailing blank lines | ignored, verdict unchanged |

## Fixture-mode isolation (syscall evidence)

`strace -f -e trace=openat,open,stat,statx,newfstatat,readlink,getdents64,ioctl` over the
canonical invocation: the only file the tool opens is the fixture itself. **No**
`/proc/self/mountinfo`, **no** `/sys/fs/btrfs/**`, **no** `quotactl`/`ioctl`/BTRFS
ioctl, no `getdents64` on a quota directory. The only other opens are CPython startup
(`/proc/self/maps`, `/proc/sys/vm/overcommit_memory`, `/etc/localtime`) and the tool
source file itself. Fixture mode is a synthetic projection: it cannot and does not
observe host quota state.

## Findings

1. **No defect found in the production tool for this case.** Exit, `finding_id` and both
   ordered six-field tuples match the sealed expectation exactly; the supplementary
   metadata matches the case rationale prose; no leakage; no input-guard bypass; the
   discriminating branches (device mismatch, ambiguous overmount, parent-id refusal,
   btrfs enabled/disabled/unavailable, xfs option precedence) all fire as the amendment
   requires.
2. **Low-severity, non-blocking observation — case coverage gap, not a tool defect.**
   `CaseHostLike` carries no `supplementary_expected` block, so the sealed oracle scores
   no per-path `device_check` / `quota_option_keys` / `btrfs_qgroups_mode` assertions for
   it (only 1 of the 30 sealed cases declares that block). Those three values for this
   case are therefore only checkable against the case's prose rationale. They agree here,
   but the machine-checked supplementary coverage for this case is thinner than the
   amendment's "supplementary sealed checks" wording implies. This is a *sealed-input*
   observation; it does not license editing the frozen bytes and I did not edit them.
3. **Informational — candidate/production divergence.** The wave-1 candidate
   `tools/mori-quota-surface.py` under `.ufo/waves/round-23/build/ImplQuota/` differs from
   production in the fixture input guards (`require(isinstance(paths, list) and paths, …)`
   vs `isinstance(paths, list)`, exact path-entry key set vs subset check, and two extra
   selftest arms). Production is the stricter measured runtime. The wave-1 candidate
   passes this same case under the sealed oracle (1/1, 9/9), so this case alone does not
   discriminate those two revisions — but the divergence is in the *stricter* direction and
   is not a defect.
4. **Informational — fixture is a synthetic analogue, not a host capture.** The frozen
   real control (`frozen/c2-expected-real.json`) observed the live pair as btrfs `0:30`
   vs st_dev `0:57` and xfs `259:1`; the fixture's xfs line uses `8:2`/`8:2`. The
   expectation (`disabled`, `btrfs_qgroups_dir_absent`, `xfs_noquota_option`) is the same
   shape as the real control's `expected_paths`, which is the intended correspondence.
   No claim of live-host equivalence is made.

## Residual risk and verification gaps

* Scope is one fixture-mode case. The frozen `CaseEscapedSpace` strict red is another
  seat's item; this report makes no claim about it, and nothing here excuses it.
* Real mode was not exercised by this seat (fixture mode only, per the assignment). The
  frozen real control is covered by the driver's real arm, not here.
* `btrfs_qgroups_mode` is `null` in this fixture because the case's uuid has `qgroups`
  absent; the projection of `qgroup`/`squota` is exercised only by probe N3, not by the
  sealed case.
* The tool's real-mode `qgroups/mode` never-read guarantee is a static property here; the
  fixture-mode path reads the fixture's declared `qgroups_mode`, which is by design.
* `QUOTA_DISABLED` is a mechanism observation only. It is not a capacity, health or
  admission verdict, and it carries no baseline acceptance, privacy clearance or
  promotion.

## Tools / installs

None. No package was installed or upgraded; the seat used only pre-existing
`/usr/bin/python3` (3.14.8), `/usr/bin/timeout` and `/usr/bin/prlimit` (util-linux
2.42.4), plus `strace` for the isolation trace. Nothing was written outside the seat's
assigned paths: `.ufo/waves/round-23/falsify/QHostLike.md`, `.ufo/waves/round-23/falsify/QHostLike/scan.json`,
and the scratch tree `/fast/scratch/hyaku/mori-r23/QHostLike/`. No production, frozen,
oracle or sibling file was modified; no lane index, jj state or ref was touched; no
background job was left running; no subagent was dispatched.
