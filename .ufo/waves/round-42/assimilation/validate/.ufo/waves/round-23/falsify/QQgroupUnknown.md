# QQgroupUnknown — round-23 falsification of sealed C2 case `SupplementQgroupUnknown`

**Seat:** `QQgroupUnknown` (agent `MadoR22-2.QQgroupUnknown`, reviewer)
**Lane:** `/home/vgpnk/Projects/shokunin/mori-shokunin`
**Scope:** exactly one sealed case, fixture mode only, one bounded invocation class.
**Verdict: PASS — the sealed case is satisfied by the pinned production tool; zero
mismatches; no expected byte was edited.** No severity-1/2 finding exists for this case.
One low-severity adjacent-path observation and one provenance nit are recorded below,
neither of which changes this case's result.

---

## 1. What was falsified

| item | value |
|---|---|
| Case | `frozen/quota-cases/SupplementQgroupUnknown.json` |
| Case id / schema | `SupplementQgroupUnknown` / `mori-quota-case-v1` |
| Case sha256 | `22f77b779845660b131dc0b19f3e02ddf203165734dfda040c52f08a06755f56` (5589 bytes) |
| Seal | `22772c10f6e3c1d8d3fe1b72083a6194e9f4e687` |
| Pinned production | `f3dc07c0bf423cc1947d0ffa91afa9ce236fbe3c` |
| Tool | `tools/mori-quota-surface.py` sha256 `e485741334d2e72a0f007481f1d2bc5b38658f54c04232965e4bbf552b8f7e92` |
| Tool bytes vs. pin | identical — `git show f3dc07c0…:tools/mori-quota-surface.py` hashes to the same `e4857413…` as the worktree file I executed |
| Case kind | non-primary source-review supplement (`frozen/case-decisions.json`: `"primary": false`; `frozen/seal-manifest.json`: `primary_c2 = 27`, `source_review_supplemental_c2 = 3`) |
| Source derivation | `preseal-amendment.md` §C2 "btrfs" bullet (present + `enabled=null` → unknown/n/a/`btrfs_qgroups_enabled_unavailable`), `frozen/case-decisions.json` entry `SupplementQgroupUnknown` (selected sha256 matches the frozen bytes byte-for-byte) |
| Sources cited by the case | `S079` = `fs/btrfs/sysfs.c` v7.2, `S080` = `fs/btrfs/qgroup.c` v7.2 |

The fixture exercises: btrfs subvolume mount at `/home` (`/@home`), a single listed
uuid whose `qgroups` directory is **present** (initialized) but whose `qgroups_enabled`
is **null** (unreadable/invalid) and `qgroups_mode` is null, path `st_dev 0:58`
(anonymous btrfs subvolume device), super options `rw,space_cache,subvolid=256,subvol=/@home`.

## 2. Source derivation re-checked against the registered kernel sources

Read from `evidence/sources/` (registered rows; `evidence/sources-manifest.json` maps
S079→`fs/btrfs/sysfs.c`, S080→`fs/btrfs/qgroup.c`, S081→`fs/btrfs/inode.c`,
S082→`Documentation/filesystems/proc.rst`, v7.2):

* `S079` `qgroup_enabled_show` (sysfs.c:2355–2368) emits the flag as an exact `0/1`
  (`sysfs_emit(buf, "%d\n", enabled)`) — supports "the enabled attribute is a witness".
* `S079` `qgroup_mode_show` (sysfs.c:2370–2395) contains `ASSERT(btrfs_qgroup_enabled(fs_info));`
  and emits only `qgroup`/`squota` under that guard — supports "mode is not consulted when
  enabled is not exactly 1" and "mode remains informational".
* `S080` call sites `btrfs_sysfs_add_qgroups` at qgroup.c:441 and :1032,
  `btrfs_sysfs_del_qgroups` at :620, :689, :1295 — supports "directory presence is the
  initialization artifact, distinct from the enabled state".
* `S081` inode.c:8246 `stat->dev = BTRFS_I(inode)->root->anon_dev;` — supports the btrfs
  equality skip for a zero stat major.

The rationale's derivation is therefore source-grounded, not asserted.

## 3. The execution (fixture mode only)

```
argv:    python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-quota-surface.py \
             --fixture /fast/scratch/hyaku/mori-r23/QQgroupUnknown/fixture.json
wrapper: timeout -k 2 15 prlimit --as=402653184 --      (384 MiB AS, 15 s)
TMPDIR:  /fast/scratch/hyaku/mori-r23/QQgroupUnknown     (never /tmp)
```

* Fixture input: `case["fixture"]` copied verbatim into
  `/fast/scratch/hyaku/mori-r23/QQgroupUnknown/fixture.json`
  (sha256 `482e9eebf1b8fee82e6f5fb5050c3c502e9c6c8ecd152ae01c2184863696c3b9`, 919 bytes).
  The frozen case file was opened read-only and is byte-unchanged.
* `--path` was never passed, so the tool took the `probe_fixture` branch
  (`tools/mori-quota-surface.py:1900-1902` → `probe_fixture` → `load_fixture`): no
  `/proc/self/mountinfo`, no `/sys/fs/btrfs`, no `stat`/`realpath` of host paths.
* Exit code **2**; stdout 989 bytes, sha256 `79c2dc8c352ecfe10829b2814e952191924c8045f5d9c2f35863bd8252a2d302`;
  stderr empty (0 bytes, sha256 `e3b0c442…` = empty).
* Invoked 3 times (2 plain + 1 `strace` run for the host-read trace), **all three the
  same single case**: exit 2 and byte-identical stdout each time. No other case, no
  `--selftest`, no driver, no real mode, no build/lint.
* Host-read trace (`strace -f -e trace=openat,open,getdents64,readlink,statx,newfstatat`):
  marker hits `mountinfo` 0, `/sys/fs/btrfs` 0, `quotactl` 0, `qgroups` 0, `xfs_quota` 0,
  `repquota` 0. The only non-stdlib opens are the fixture file, the tool file,
  `/etc/ld.so.cache`, `/etc/localtime` and CPython's own `/proc/self/maps` (interpreter
  startup). All `getdents64` calls target CPython stdlib directories.

## 4. Result versus the sealed expectation

**Primary (scored, six-field denominator — kept separate from supplementary metadata):**

| field | expected | observed | match |
|---|---|---|---|
| exit | 2 | 2 | yes |
| finding_id | `QUOTA_STATE_UNKNOWN` | `QUOTA_STATE_UNKNOWN` | yes |
| tuple 1 | (`/home/quota/unknown`, `btrfs`, `/home`, `unknown`, `n/a`, `btrfs_qgroups_enabled_unavailable`) | identical | yes |

Ordered six-field tuple list (expected == observed, one row):
`["/home/quota/unknown","btrfs","/home","unknown","n/a","btrfs_qgroups_enabled_unavailable"]`

**Supplementary metadata (observed only — this case carries no `supplementary_expected`
block, so none of it is scored and none of it widens the denominator):**

* `device_check` = `btrfs_subvolume_skipped` (stat major 0 ⇒ btrfs equality skip, per
  `evaluate()` at `tools/mori-quota-surface.py:513-559`)
* `quota_option_keys` = `[]` (btrfs carries its mechanism in sysfs, not in mount options)
* `btrfs_qgroups_mode` = `null` (mode is not consulted when enabled is not exactly 1)

These three observations agree with the case rationale, but they are **not** sealed
expectations for this case and are reported as such.

**Output shape / safety checks (all pass):** schema `mori-quota-surface-v1`; top-level key
set exactly `{df_covers_quota, exit_code, finding_id, limits, paths, schema}`; path-row key
set exactly the nine allowed keys; `df_covers_quota` false; `limits` non-empty; no `error`
token (not a setup error); no partial verdict; leakage canary scan over the fixture
(uuid, mount sources, `key=value` option tokens, distinctive option values, device
basename `dm-0`) → **0 hits**.

**Mismatch list: empty.** The case's decisive property — a *present* qgroups directory
with an *unreadable/invalid* enabled attribute must be reported `unknown`, never
`disabled` — holds: observed `quota_state = unknown`,
`basis = btrfs_qgroups_enabled_unavailable`, which is the discriminating branch
(`classify_btrfs`, `tools/mori-quota-surface.py:465-485`; the null-enabled fall-through
at line 484 is the branch that makes this case falsifiable at all).

## 5. Findings by severity

**Severity 1–2 (blocking): none.** No defect found in this case, its expectation, its
derivation, or the code path it exercises.

**Severity 3 (low, adjacent path, NOT this case, no change requested here):**
`classify_btrfs` returns the basis token `btrfs_device_unmapped` for the *inspection
failure* case (`record["qgroups"] is None`, `tools/mori-quota-surface.py:474-477`).
In real mode a `stat`/listing error on `/sys/fs/btrfs/<uuid>/qgroups` leaves `qgroups`
as `None` (`scan_btrfs_sysfs`, lines 571-627), so the tool would say "device unmapped"
although the device *was* mapped and only the state was unobservable. The verdict
(unknown / n/a) is still conservative and never claims disabled, so the amendment's
"A parent sysfs permission/listing error is unknown, NEVER absent/disabled" holds; the
defect is the *basis label* only. It is **unreachable in fixture mode** (the fixture
loader enforces `type(qgroups) is bool`, `tools/mori-quota-surface.py:753`), so it does
not affect this case, `SupplementQgroupDisabled`, or any other sealed fixture case.
Reported for the parent to route; no byte of the frozen case, the tool, or the expectation
was touched by this seat.

**Severity 4 (nit, provenance only):** the case's `rationale` text relies on S081
(`inode.c:8246`) and S082 (`proc.rst` §3.5 field layout), but the case's `sources` array
lists only `["S079","S080"]`. Both cited sources are registered and resolvable in
`evidence/sources/`, so the derivation is sound; only the machine-readable source list is
narrower than the prose. No expectation change is implied, and none is made.

## 6. Honest scope statements

* This seat verified **one** case, in **fixture mode**, against the **pinned** production
  tool bytes. It did not run the C2 driver, the oracle over the suite, the selftest, or
  any real-mode probe; it did not read qgroups, mode, mountinfo or any live quota state.
* The strict C2 target remains **UNPROVABLE at 29/30** for the unrelated frozen
  contradiction in `CaseEscapedSpace` (see `evidence/frozen-contradiction.json`: the
  sealed rule requires `unknown`/`ambiguous_overmount` for the selected mount 43 whose
  parent id 33 is not the id of the longest strictly-shorter cover `/srv` (42), while the
  frozen expected row still says `enabled`). That red is **not** excused, **not**
  special-cased, **not** excluded, **not** relabelled and **not** rewritten here, and this
  case is not the red. The driver receipt `evidence/measure4/c2-oracle-after.json` shows
  `pass 29 / total 30`, `unmet 1`, `supplementary pass 274 / total 274` at the same pin.
* Cross-check (not a substitute for the independent run above): the driver's own per-case
  entry for `SupplementQgroupUnknown.json` at pin `f3dc07c0…` used
  `fixture_sha256 = 482e9eeb…` — the same fixture bytes I built — with
  `headline = {exit_match: true, finding_match: true, paths_match: true}` and
  `reason: null`, and its staged tool copy hashes to the same `e4857413…` I executed.
* No privacy clearance, no baseline acceptance, no promotion, no health claim is implied.
  `QUOTA_DISABLED`/`QUOTA_STATE_UNKNOWN` remain surface observations, not capacity or
  health verdicts.

## 7. Residual risk and verification gaps

1. **Real mode untested by this seat** (forbidden for me): the `qgroups_enabled` read
   path in `scan_btrfs_sysfs` and the "never read `qgroups/mode`" safety rule are
   unexercised by this seat; they are covered only by the driver's real control.
2. **Fixture-only discrimination**: my evidence shows the null-enabled branch produces
   the expected row; it does not show what a *host* would return for the same topology
   (racy enable/disable windows are explicitly out of scope).
3. **The `btrfs_device_unmapped` basis-label defect (severity 3)** remains unexercised and
   unfixed; if the parent wants it addressed it needs a real-mode (or a dedicated
   source-review supplement) arm, not this fixture.
4. **Case-seal bookkeeping**: the sealed bytes, the `case-decisions.json` `selected_sha256`
   and the driver's recorded case sha256 all agree (`22f77b77…`); the frozen file was
   opened read-only only (mtime unchanged, hash unchanged after the run).
5. **Denominator discipline**: this case contributes 1 to the 30-case C2 population and
   0 to the 27-case primary denominator; it is reported on its own and does not change
   the 29/30 strict position.

## 8. Artifacts

* Receipt (synthetic, this seat): `.ufo/waves/round-23/falsify/QQgroupUnknown/scan.json`
* This report: `.ufo/waves/round-23/falsify/QQgroupUnknown.md`
* Scratch (this seat only): `/fast/scratch/hyaku/mori-r23/QQgroupUnknown/`
  (`fixture.json`, `stdout.txt`, `stderr.txt`, `exit_code.txt`, `argv.txt`,
  `wrapper.txt`, `stdout_rerun.txt`, `stdout_trace.txt`, `trace.txt`,
  `compare_case.py`, `comparison.json`, `build_receipt.py`)

**Tooling:** no package was installed, updated or removed in this seat; only pre-existing
`python3` (3.14.8), `prlimit` and `timeout` (util-linux 2.42.4) and `strace` were used.
