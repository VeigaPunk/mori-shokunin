# S079 source re-open — Linux btrfs sysfs interface v7.2

**Seat:** MadoR22-2.ReopenS079 (read-only leaf scout; no executions, no edits, no delegation, no installs).
**Target row:** `S079` in `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md` (line 85), URL `https://raw.githubusercontent.com/torvalds/linux/v7.2/fs/btrfs/sysfs.c`.
**Pinned bytes:** `/fast/scratch/hyaku/mori-r23/ReopenS079/sysfs.c`, 2702 lines, 72925 bytes.
**Method note:** no `lsp` device is mounted in this environment; definition tracing used literal primary-source bytes (the upstream fetch plus the retained `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/evidence/sources/S080-fs_btrfs_qgroup.c`), not lane-wide text grep. No semantic-reference proof is claimed.

## Verdict

Row S079 is accurate against its pinned revision: URL/tag, full rawSHA, all three anchors, the lesson23 Gate quote, and every clause of the new note are supported. **No registry correction is required.** Two precision/ordering observations (F1, F2) are reported for the parent; neither changes the row's admission decision, any frozen byte, or the C2 safety rule.

## 1. Byte identity

- Fetched `sysfs.c` sha256 = `ce146120f29ac29c0bc1859f21e4b84da91a536df2ec9fd2fa5649144f731c43` — exactly the assignment rawSHA.
- `bytes` 72925 matches `evidence/sources-manifest.json` entry `{id: S079, bytes: 72925, sha256: ce146120…c43}`.
- `cmp` against `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/evidence/sources/S079-fs_btrfs_sysfs.c` → **byte-identical**. The row's 16-hex prefix `ce146120f29ac29c` is a correct prefix of the full hash.
- URL is the v7.2 tag path; content hash is stable between the fresh fetch and the retained evidence copy.

## 2. Anchor verification (pinned file line numbers)

| Row anchor | Observed |
|---|---|
| `qgroup_enabled_show:2355-2368` | Declaration at 2355; body 2355–2367; `BTRFS_ATTR(qgroups, enabled, qgroup_enabled_show);` at 2368. The flag read is line 2363. No drift. |
| `qgroup_mode_show:2370-2395` | Declaration at 2370; `ASSERT(btrfs_qgroup_enabled(fs_info));` at 2378; `FULL → "qgroup"` at 2380–2381; `SIMPLE → "squota"` at 2383–2384; default emits nothing and warns at 2386–2389; `BTRFS_ATTR(qgroups, mode, qgroup_mode_show);` at 2395. No drift. |
| `devices links:2155` | `ret = sysfs_create_link(devices_kobj, disk_kobj, disk_kobj->name);` at 2155 inside `btrfs_sysfs_add_device` (declared 2134). The only other `sysfs_create_link` in the file is the `"bdi"` link at 2334, so 2155 is unambiguous. |
| `separate qgroups enabled and mode attributes` | `qgroups_attrs[]` at 2455–2461 registers `enabled` and `mode` as distinct attributes; the path comment at 2449–2452 states `/sys/fs/btrfs/<uuid>/qgroups/`. |

Both range anchors include the attribute-registration line immediately after the show function; that is scope-consistent, not an off-by-one.

**Bounded note on "device link names":** 2155 establishes only that the link name is the block-device kobject's name (`disk_kobj->name`). The concrete string form (`dm-0` etc.) is produced by the block layer (`bdev_kobj`), outside this file; the row does not claim that string convention, and none is inferred here.

## 3. lesson23 Gate quote

`corpus/lessons/round-23.md:45` cites:

```
2363: enabled = fs_info->qgroup_flags & BTRFS_QGROUP_STATUS_FLAG_ON;
```

- Located verbatim at line 2363 (only the leading tab is omitted in the Gate cell).
- 5 whitespace-delimited tokens, well under the ≤25-word bound.
- Truthful: the `enabled` attribute takes `qgroup_lock`, tests `BTRFS_QGROUP_STATUS_FLAG_ON`, and emits `"%d\n"` (0/1) at 2366.

## 4. New note: claim vs source

Registry note: *"Read the explicit enabled flag; directory existence is separate, and mode asserts that qgroups are enabled."*

| Clause | Source evidence | Result |
|---|---|---|
| explicit enabled flag | S079:2362–2366 (`spin_lock`, `enabled = …FLAG_ON`, `spin_unlock`, `sysfs_emit(buf, "%d\n", enabled)`) | Supported (value is exactly 0/1). |
| directory existence is separate | S079 `btrfs_sysfs_add_qgroups` (2586–2617) gates only on `btrfs_is_testing()` and on the kobject not already existing (2595–2600); it never tests `STATUS_FLAG_ON`. Corroborated by retained S080 bytes (sha256 `121a0af27f9553a9749c837536d618e2ea50d44ce54b30b032fa56e6f3df6ed5`): `btrfs_read_qgroup_config` calls `btrfs_sysfs_add_qgroups` at 441 and only then sets `qgroup_flags = 0` at 445; teardown removes the directory at 689 (config free) and failed-enable cleanup at 620/1295; `btrfs_quota_disable` clears `STATUS_FLAG_ON` at 1406 without removing the directory. | Supported: presence = initialized, not enabled; absence is only usable after successful parent inspection. |
| mode asserts that qgroups are enabled | S079:2378 `ASSERT(btrfs_qgroup_enabled(fs_info));` inside the `qgroup_lock` region. | Literally supported; precision finding F1. |

## 5. Findings (precision / documentation ordering, no registry contradiction)

### F1 — Low: the ASSERT predicate is a different state variable from the exported flag

- S079:2363 exports `fs_info->qgroup_flags & BTRFS_QGROUP_STATUS_FLAG_ON`.
- S080:42–45 defines `btrfs_qgroup_enabled()` as `btrfs_qgroup_mode() != BTRFS_QGROUP_MODE_DISABLED`, and S080:33–39 makes `btrfs_qgroup_mode()` depend on `test_bit(BTRFS_FS_QUOTA_ENABLED, &fs_info->flags)`, not on the status flag.
- Ordering in S080: enable sets `qgroup_flags = STATUS_FLAG_ON` at 1104 (under `qgroup_ioctl_lock`, **outside** `qgroup_lock`) and sets the `FS_QUOTA_ENABLED` bit later at 1256 under `qgroup_lock`; disable clears the bit at 1367 and clears `STATUS_FLAG_ON` later at 1406 under `qgroup_lock`.
- Consequence: `enabled`-attribute = 1 with ASSERT-bit = 0 exists in both transitions (enable window 1104→1256; disable window 1367→1406). A mode read after observing `enabled=1` is therefore unsafe in both directions, not only when a disable "clears the ON flag between two reads" (`corpus/knowledge/quota-surface-r23.md:102`). The note's wording is true; the causal sentence in the knowledge note is looser than the source.
- Also observed: 1104 writes `qgroup_flags` outside `qgroup_lock` while the sysfs reader takes that lock, so even the `enabled` read is a snapshot rather than a lock-partitioned state. No broader kernel-race claim is made.
- **Impact:** none on the decision. The preseal rule (real mode NEVER reads `qgroups/mode`) is required, and is stronger than the wording it replaced. Frozen fixture expectations already emit `btrfs_qgroups_mode` as intentionally unobserved.

### F2 — Low: stale operational instruction inside the knowledge note

- `corpus/knowledge/quota-surface-r23.md:22–23` still says "read mode only when enabled is1, since qgroup_mode_show asserts enabled".
- The same file at 99–103 ("This supersedes any operational instruction above to read mode when enabled1. Final real-mode design NEVER reads qgroups/mode") and `preseal-amendment.md:132–141` say real mode never reads mode at all.
- The later text wins and no frozen byte is affected, but a future implementer who stops at line 23 would implement the rejected read. Recommendation for a future note revision: drop the stale sentence or mark it inline as superseded. No edit made here.

## 6. Frozen-expectation cross-check (source consistency)

Read-only check of `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/frozen/quota-cases/`:

- `CaseBtrfsQgroup.json`: fixture `qgroups: true`, `qgroups_enabled: true`, `qgroups_mode: "qgroup"`; expected `enabled / unknown / btrfs_qgroups_enabled`. Its rationale explicitly identifies `btrfs_qgroups_dir_present` as the superseded original token (present = initialized, not enabled).
- `SupplementQgroupDisabled.json`: expected `disabled / n/a / btrfs_qgroups_disabled`.
- `SupplementQgroupUnknown.json`: expected `unknown / n/a / btrfs_qgroups_enabled_unavailable`.
- Expected path objects carry the six compared fields (`path, fstype, mount_point, quota_state, enforcement, basis`) and omit `btrfs_qgroups_mode`, consistent with "mode intentionally unobserved, not mode-absent".

These frozen rows agree with the pinned source. **No source-vs-frozen contradiction found in S079's scope.**

## 7. Explicit limits and non-findings

- Only S079 was re-opened as a row. S080 (and the `qgroup.h` declarations, sha256 `ddb85c4e5501e7bb094a08ff3d63c3c12d03920bf10f187fb5290d17e31b4930`) were consulted solely to trace the helper/ordering that S079's note depends on; S080's registry row was not edited or re-scored here.
- No runtime or host reads, no executions, no builds/tests/linters, no quota tools, no installs. Scratch is confined to `/fast/scratch/hyaku/mori-r23/ReopenS079/`; the only lane write is this report.
- No implementation token was audited; C2 integration and driver conclusions belong to the assigned implementation/falsification seats.
- Registry, frozen cases, oracle, lesson and knowledge files were not modified.
