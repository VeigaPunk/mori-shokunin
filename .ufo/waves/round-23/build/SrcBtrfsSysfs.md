# SrcBtrfsSysfs — btrfs qgroups sysfs anchor re-open for round23 C2

Seat: `MadoR22-2.SrcBtrfsSysfs-8` (scout, read-only). Report-only; no registry, contract,
lesson, case, oracle or production edits. `corpus/SOURCES.md` was not modified.

Independence held: no candidate implementation was opened
(`.ufo/waves/round-23/build/ImplQuota/`, `.scratch/round23/ImplQuota`), no case file under
`cases-proposed/` or `build/Case*.md`, and no oracle file was opened. Disclosed reads outside
the anchor: sibling source report `.ufo/waves/round-23/build/SrcBtrfsGetattr.md` (format and
tier convention only) and frozen `.ufo/waves/round-23/frozen/c2-expected-real.json` (read after
the source analysis, for consistency of the device-name mapping only).

## Opened

| Item | Value |
|---|---|
| Primary URL | https://raw.githubusercontent.com/torvalds/linux/v7.2/fs/btrfs/sysfs.c |
| Access | 2026-10-21; one `curl -fsSL`; HTTP 200; 72,925 bytes; 2,702 lines; ASCII; LF only (0 CR) |
| Local copy | `.scratch/round23/SrcBtrfsSysfs/sysfs.c` (scratch copy, not a registry artifact) |
| **Fetched-bytes SHA-256** | **`ce146120f29ac29c0bc1859f21e4b84da91a536df2ec9fd2fa5649144f731c43`** |
| Git blob SHA-1 of fetched bytes | `0d14570c8bc2900bb41685a13cfbf2c4783789e8` |
| Tag resolution | `git ls-remote` 2026-10-21: `refs/tags/v7.2` = annotated tag object `237a1c39e8dfd3e1c6f1f023eea37a48ec04cc63`; peeled `refs/tags/v7.2^{}` = commit `8d3ae59288f1e7d58d76558a6ee96d533bc5019f` |
| Immutable pin | Same path fetched at commit `8d3ae59288f1e7d58d76558a6ee96d533bc5019f` → byte-identical (`cmp` IDENTICAL, same SHA-256). Saved as `.scratch/round23/SrcBtrfsSysfs/sysfs.commit.c` |
| Caller-trace annex | https://raw.githubusercontent.com/torvalds/linux/v7.2/fs/btrfs/qgroup.c — 139,049 bytes, 4,989 lines, SHA-256 `121a0af27f9553a9749c837536d618e2ea50d44ce54b30b032fa56e6f3df6ed5`, blob `502fb4a55cb2278946d104e85c13bb80bf575b01`; re-fetched at the same commit, byte-identical. Fetched only to trace `btrfs_sysfs_add_qgroups()` call sites (see below); the anchor itself is `sysfs.c` |

Provenance caveat: the tag→commit resolution and the commit-URL byte equality pin the bytes to
`8d3ae59:fs/btrfs/sysfs.c` as GitHub serves them; they do not authenticate GitHub or the tag.
The GitHub tree API for `v7.2:fs/btrfs` returned **HTTP 403** (unauthenticated rate limit), so
the blob SHA-1 could not be cross-checked against GitHub's own tree entry in this session. The
blob hash is recorded but is not used as identity.

## Anchor verification — confirmed, two range corrections

Prompt anchor: "qgroups attributes enabled/mode (~2353-2457) and `/sys/fs/btrfs/<uuid>/qgroups/`
path comment". Located exactly:

- `sysfs.c:2355-2367` `qgroup_enabled_show()`; flag read at **`:2363`**
  `enabled = fs_info->qgroup_flags & BTRFS_QGROUP_STATUS_FLAG_ON;`; emission at `:2366`
  `sysfs_emit(buf, "%d\n", enabled)`.
- `sysfs.c:2368` `BTRFS_ATTR(qgroups, enabled, qgroup_enabled_show);` → file name `enabled`.
- `sysfs.c:2370-2394` `qgroup_mode_show()`; `:2378` `ASSERT(btrfs_qgroup_enabled(fs_info));`
  `:2381` emits `"qgroup\n"` for `BTRFS_QGROUP_MODE_FULL`; `:2384` emits `"squota\n"` for
  `BTRFS_QGROUP_MODE_SIMPLE`; `:2386-2389` warns and emits zero bytes on any other mode.
- `sysfs.c:2395` `BTRFS_ATTR(qgroups, mode, qgroup_mode_show);` → file name `mode`.
- `sysfs.c:2451-2454` comment block "Qgroups global info"; **`:2453`
  `* Path: /sys/fs/btrfs/<uuid>/qgroups/`**.
- `sysfs.c:2455-2461` `qgroups_attrs[]` = `enabled` (2456), `inconsistent` (2457),
  `drop_subtree_threshold` (2458), `mode` (2459), `NULL` (2460); `ATTRIBUTE_GROUPS(qgroups)`
  at `:2462`.
- Directory creation: `btrfs_sysfs_add_qgroups()` `sysfs.c:2586-2620`; `kobject_init_and_add(...,
  fsid_kobj, "qgroups")` at `:2604-2605`; `fsid_kobj` is named `%pU` at `:2259-2260`, i.e.
  `/sys/fs/btrfs/<uuid>`. Deletion: `btrfs_sysfs_del_qgroups()` `:2567-2583`.
- Header table `sysfs.c:38` documents `qgroup_attrs` →
  `/sys/fs/btrfs/<uuid>/qgroups/<level>_<qgroupid>` (the **per-qgroup** set, `:2517-2528`).
  The global `qgroups_attrs` directory has no row in that header table; it is documented only
  at `:2453`.

Corrections to the prompt range (no material effect):
- Lower bound: `2353` is two lines before the first anchor (`:2355` starts `qgroup_enabled_show`).
- Upper bound: `2457` falls **inside** `qgroups_attrs[]`; the array ends at `:2461` (`mode` is
  `:2459`), and the creation function is far below at `:2586-2620`.

## Located quotes (each ≤25 words)

Primary, `sysfs.c:2453` (verbatim, 2 whitespace tokens):

> Path: /sys/fs/btrfs/<uuid>/qgroups/

Secondary, `sysfs.c:2363` (verbatim code, 5 whitespace tokens):

> enabled = fs_info->qgroup_flags & BTRFS_QGROUP_STATUS_FLAG_ON;

Secondary, `qgroup.c:444` (verbatim comment, 12 words) — the caller-trace qualifier:

> /* default this to quota off, in case no status key is found */

## Contract rule backed

`contract.md:80` — real-mode inputs: "directory listings/existence under
`/sys/fs/btrfs/*/devices/` and `/sys/fs/btrfs/<uuid>/qgroups`, and reading
`/sys/fs/btrfs/<uuid>/qgroups/mode` if present."

`contract.md:115-117` — btrfs classification rows: "source basename maps to exactly one uuid
whose `qgroups` is true" → `enabled` / `btrfs_qgroups_dir_present`; "… `qgroups` false" →
`disabled` / `btrfs_qgroups_dir_absent`; "zero or several uuids list the device" → `unknown` /
`btrfs_device_unmapped`.

The primary quote backs the **path** part of `contract.md:80` exactly. The secondary quote
backs a *different, stronger* witness than the contract uses: the directory's own `enabled`
file reports the ON flag as 0/1, and `contract.md:80` does not list that file as an input.

## Assessment

### Supports (A-grade narrow facts)

1. **Path and attribute surface.** The global qgroups directory is `/sys/fs/btrfs/<uuid>/qgroups/`
   (`:2453`, `:2586-2605`) and contains exactly `enabled`, `inconsistent`,
   `drop_subtree_threshold`, `mode` (`:2455-2461`). The contract's read path and its nullable
   `btrfs_qgroups_mode` field are real.
2. **`enabled` is the flag witness.** `:2363` reads `BTRFS_QGROUP_STATUS_FLAG_ON` under
   `qgroup_lock`; `:2366` prints `0`/`1`. This is the kernel's precise enabled/disabled
   indicator, strictly better than directory presence.
3. **`mode` values.** `:2379-2390` yields `qgroup` (full) or `squota` (simple quota), and zero
   bytes for an unexpected mode. `mode` is created with the kobject itself
   (`default_groups`, `:2469-2473`), so "mode present" carries no state information beyond
   "the directory exists".
4. **`enforcement: unknown` is right.** Qgroup presence tracks accounting/tracking structures;
   limits are distinct per-qgroup files `max_referenced`, `max_exclusive`, `limit_flags` under
   `/sys/fs/btrfs/<uuid>/qgroups/<level>_<qgroupid>/` (`:2517-2528`), which the probe never
   enumerates. This supports the contract's own limit "btrfs qgroup presence ≠ any limit set".
5. **Device mapping rule.** `sysfs_create_link(devices_kobj, disk_kobj, disk_kobj->name)` at
   `:2155` (removal keyed the same way at `:1971`) creates `/sys/fs/btrfs/<uuid>/devices/<name>`
   where `<name>` is the backing block-device kobject name. A source of `/dev/mapper/root`
   realpaths to `/dev/dm-0`, basename `dm-0`, matching the contract's `device_links` fixture
   key (`contract.md:88-89`) and its "exactly one uuid lists the device" test (`:117`).

### Under-determines the rule as written (`contract.md:115-116` maps presence directly to state)

`sysfs.c` alone cannot establish when the directory exists: `btrfs_sysfs_add_qgroups()` has no
call site in the file, and `btrfs_sysfs_add_mounted()` (`:2287-2352`) creates `devices`,
`features`, `debug`, `discard` and `allocation` but **not** `qgroups`. Tracing the callers in
`qgroup.c` (annex above):

- **Mount:** `btrfs_read_qgroup_config()` returns early when there is no quota root
  (`qgroup.c:432-433`), then creates the directory (`:441`) and **only afterwards** sets
  `fs_info->qgroup_flags = 0` (`:445`) and applies the on-disk status flags. `BTRFS_FS_QUOTA_ENABLED`
  is set only if `BTRFS_QGROUP_STATUS_FLAG_ON` is present (`:612-615`). On the `ret >= 0` path the
  directory is retained even when no ON flag was found; only the error path deletes it
  (`:618-620`).
- **Enable ioctl:** directory created at `:1032`, transaction runs, ON flag and
  `BTRFS_FS_QUOTA_ENABLED` set at `:1254-1256`; failure unwinds with `btrfs_sysfs_del_qgroups()`
  at `:1295`.
- **Disable:** clears `BTRFS_FS_QUOTA_ENABLED` (`:1367`), then clears `quota_root` and the ON flag
  (`:1404-1407`) before `btrfs_free_qgroup_config()` (`:1411`) → `btrfs_sysfs_del_qgroups()`
  (`:689`).

Consequences:

- In steady state, presence tracks *an initialized quota root*, which normally means quota
  enabled: the contract's mapping is correct for the ordinary mounted filesystem.
- **Present-but-disabled windows exist.** (a) The enable/disable transitions above: these are
  exactly the races the contract already disclaims. (b) A mounted filesystem whose quota tree
  exists but whose status item lacks the ON flag keeps the directory with `enabled` reading `0`
  (`:445` default + success path). That is a persistent, non-race false `enabled` under
  `contract.md:115`. The source cannot exclude it.
- **Absent-but-enabled is possible but bounded.** `btrfs_is_testing()` returns before creating
  the directory (`:2593-2594`), and a sysfs creation failure (`:2601-2602`) or a mount-time
  qgroup-config read error (`qgroup.c:618-620`) removes/never creates it. These yield
  `btrfs_qgroups_dir_absent` → `disabled` while quotas may be on (`contract.md:116`). Rare and
  failure-mode only, but not excluded by the contract.
- **No contradiction of the path, of `mode`, or of `enforcement: unknown`.** The only
  contradiction is against an *unqualified biconditional* "dir present ⇔ enabled".

### Side-effect note on reading `mode` (detection only, no remediation)

Because `mode` exists whenever the directory exists, and its show function asserts
`btrfs_qgroup_enabled(fs_info)` (`:2378`), reading `qgroups/mode` inside a present-but-disabled
window exercises a btrfs `ASSERT` and then emits zero bytes. [INFERENCE: `ASSERT` expands to a
warning plus stack dump when `CONFIG_BTRFS_ASSERT` is enabled; `fs/btrfs/assert.h` was not
opened.] Read-only, but not silent. `contract.md:80` permits the read "if present"; this is a
real, if narrow, interaction with the anomalous state above.

## Tier and scope

**Tier B** for the row as it would back `contract.md:115-116` (directory presence used as the
enabled/disabled verdict). The source is primary upstream kernel code at immutable tag `v7.2`
(A-grade authority), but it does not by itself establish the presence→enabled equivalence it is
cited for; that equivalence needs the `qgroup.c` call-site trace and still leaves the bounded
present-but-disabled class. 

A-grade sub-claims, admissible today if L1 splits the row:

- `/sys/fs/btrfs/<uuid>/qgroups/` exists with attributes `enabled`, `inconsistent`,
  `drop_subtree_threshold`, `mode`; `enabled` prints the ON flag as 0/1; `mode` prints
  `qgroup` or `squota` (`sysfs.c:2355-2395`, `2451-2462`, `2586-2620`).
- `/sys/fs/btrfs/<uuid>/devices/` entries are symlinks named after the backing block-device
  kobject (`sysfs.c:2155`, `:1971`), which is what makes the `readlink -f` basename join in the
  contract and fixture legitimate.

Scope excludes: xfs/ext/tmpfs rows; any statement that a quota limit is set; any claim that
`st_dev` matches or mismatches (S081 territory); the `enabled` file as a contract input (the
contract does not list it); per-qgroup limit semantics; btrfs send/receive or subvolume qgroup
inheritance.

Proposed registry row (SOURCES.md untouched by this seat; L1 owns insertion, id assignment and
final status):

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| (S077–S084 unassigned) | Linux fs/btrfs/sysfs.c at v7.2 — https://raw.githubusercontent.com/torvalds/linux/v7.2/fs/btrfs/sysfs.c | code | B | btrfs qgroups sysfs surface: exact `/sys/fs/btrfs/<uuid>/qgroups/` path, `enabled`/`mode` file semantics, and `/sys/fs/btrfs/<uuid>/devices/` link naming; does **not** establish dir-presence ⇔ quota enabled | `fs/btrfs/sysfs.c:2355-2395`, `2451-2462`, `2567-2620`, `2155`, `1971`; tag v7.2 (commit `8d3ae59288f1e7d58d76558a6ee96d533bc5019f`), bytes SHA-256 `ce146120…c43`; caller trace `fs/btrfs/qgroup.c:432-445`, `612-620`, `1032`, `1254-1256`, `1295`, `1367-1411`, `689` | The global qgroups directory exists and exposes `enabled` (ON flag, 0/1) and `mode` (`qgroup`/`squota`); the directory is created when a quota root is initialized, before the ON flag is read, so presence is strong but not conclusive evidence of enabled; devices are symlinked by block-device kobject name (`dm-0`). | queued | 2026-10-21 | on-release | — |

If L1 prefers a single A row, restrict it to the path/attribute/device-naming cells and drop the
presence→enabled claim from the row's `teaches` cell; the current C2 wording would then need a
separate anchor or an amendment to read `qgroups/enabled`.

## Remaining unknowns

- Whether L1's sealed cases model the persistent present-but-disabled state (quota tree without
  the ON status item). No case file was read.
- Whether the probe is permitted to read `qgroups/enabled`; `contract.md:80` omits it, and that
  file would collapse the anomaly without any privileged call.
- Host `CONFIG_BTRFS_ASSERT` value, which decides whether the `mode` read can warn in that
  window. Kernel config is outside this seat's permitted live reads.
- GitHub tree-entry blob cross-check (HTTP 403 rate limit); bytes are pinned by tag→commit and
  commit-URL equality instead.
- S-id for this row: the census receipt `.ufo/waves/round-23/evidence/sources-start.txt` lists
  only duplicate-URL findings and ends at S076, and `corpus/SOURCES.md` holds 76 rows with
  maximum id S076 (no S077–S084 row) at this revision. The id above is therefore a placeholder,
  as in the sibling `SrcBtrfsGetattr` report.

## Run log

- Commands: `curl -fsSL` of `sysfs.c` (tag and commit URLs), `qgroup.c` (tag and commit URLs),
  and one GitHub tree API call (403, no file written); `wc -l`, `stat`, `file`, `git hash-object`,
  `sha256sum`, `cmp`, `git ls-remote`, `grep -n`, `nl -ba`, `sed -n`.
- Reads: `contract.md`, `corpus/SOURCES.md` (grep for btrfs/quota rows and count),
  `.ufo/waves/round-23/evidence/sources-start.txt`, `.ufo/waves/round-23/frozen/c2-expected-real.json`,
  `.ufo/waves/round-22/build/SrcRejectHash.md`, `.ufo/waves/round-23/build/SrcBtrfsGetattr.md`,
  `.ufo/waves/round-23/wave1-spec.json` (own item).
- Tools installed or updated: none.
- Tests, builds, linters, formatters, smoke runs: none. No `/tmp` use. No VCS mutation, no lane
  index/worktree access. No live host probe (no `/proc`, `/sys`, `stat` of host paths).
