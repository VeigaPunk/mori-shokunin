measured 2026-10-23T08:51:58Z

# S193 supersede finding

## Behavior and evidence

- Re-fetched `https://raw.githubusercontent.com/torvalds/linux/v7.2/drivers/base/core.c` with `timeout 90 curl --fail --location --silent --show-error ... --output /fast/scratch/hyaku/mori-r35/SrcS193Supersede/core.c`. Output: SHA-256 `fa223c8f9f1bb40ca52c73f156439d311065e9be04efa2c6cf57039940e1c9fa`, 151293 bytes. The saved file and `corpus/evidence/sources-r34/S193.src` have the same SHA-256 and byte count; `cmp -s` returned `cmp_exit=0`.
- Add path: v7.2 `core.c:3508-3510` gates `sysfs_create_link(..., "device")` on `dev->parent && device_is_not_partition(dev)`. Delete path: `:3542-3543` uses the same guard for `sysfs_remove_link`.
- Under `CONFIG_BLOCK`, `device_is_not_partition` returns `!(dev->type == &part_type)` (`core.c:2430-2433`).
- Reparent path: `device_move_class_links` at `:4647-4658` removes the link under `if (old_parent)` (`:4653-4654`) and creates it under `if (new_parent)` (`:4655-4657`); these conditions contain no partition check. `device_move` calls the helper at `:4705-4706`.
- Thus the add/delete condition is not a universal condition for reparenting. The requested S202 scope is supported by the reopened v7.2 bytes. The full file reopened this round is at `/fast/scratch/hyaku/mori-r35/SrcS193Supersede/core.c`.

## First-landed S193 cells versus the round-34 tip

The read-only `git show 406d91a4 -- corpus/SOURCES.md` output shows the in-place change; the round-34 lesson logs the exact old and new cells at `corpus/lessons/round-34.md:51-55`.

| Cell | First landed at `8d56809a` | Tip `3a7a89ea` after `406d91a4` |
|---|---|---|
| anchor | `drivers/base/core.c:3508-3510,3542-3543; tag v7.2` | `drivers/base/core.c:3508-3510,3542-3543,4653-4657; tag v7.2` |
| teaches, source-derived clause | `The device symlink is created, and removed, only when the device has a parent and is not a partition.` | `On add and on delete, the device symlink is created and removed only when the device has a parent and is not a partition; on a reparent (device_move) the link follows the new parent with no partition check.` |

`git log --format='%h %H %s' --follow -- corpus/SOURCES.md` identifies `406d91a4b891766e36272415df3bdaca87548d96` as the round-34 rewrite. The verifier spot-check calls the supported content plus in-place anchor/teaches rewrite a form defect (`corpus/lessons/round-34-verifier-spotcheck.md:117-119`). S202 should therefore append the correction rather than alter S193.

## Drafts

```DRAFT SOURCES S202
| S202 | Linux drivers/base/core.c at v7.2 (device class symlink add/delete and move) — https://raw.githubusercontent.com/torvalds/linux/v7.2/drivers/base/core.c | code | A | v7.2 add/delete guards and device_move_class_links behavior for the class device `device` symlink | drivers/base/core.c:3508-3510,3542-3543,2430-2433 (device_is_not_partition under CONFIG_BLOCK),4653-4657,4704-4706; tag v7.2 | supersedes S193 — On add and delete, the class `device` symlink is created or removed only when `dev->parent` exists and `device_is_not_partition(dev)` passes. Under CONFIG_BLOCK that predicate excludes `part_type`. `device_move_class_links` instead removes under `old_parent` and creates under `new_parent`, with no partition check; `device_move` calls this helper. | mined | 2026-10-23 | on-release | tools/mori-disk-rate.py |
```

```DRAFT Gate S202
| S202 | https://raw.githubusercontent.com/torvalds/linux/v7.2/drivers/base/core.c | 2026-10-23 (fetch time not separately captured) | `fa223c8f9f1bb40ca52c73f156439d311065e9be04efa2c6cf57039940e1c9fa` | `core.c:3508` (5 words): "if (dev->parent && device_is_not_partition(dev)) {"; `:3509` (4): "error = sysfs_create_link(&dev->kobj, &dev->parent->kobj,"; `:3542` (4): "if (dev->parent && device_is_not_partition(dev))"; `:3543`: `sysfs_remove_link(&dev->kobj,`; `:2432` (4): "return !(dev->type == &part_type);"; `:4653` (2): "if (old_parent)"; `:4654`: `sysfs_remove_link(&dev->kobj,`; `:4655` (2): "if (new_parent)"; `:4656` (4): "error = sysfs_create_link(&dev->kobj, &new_parent->kobj,"; `:4706` (5): "error = device_move_class_links(dev, old_parent, new_parent);" | admit, A, mined |
```

```DRAFT corpus/lessons/round-35.md
- S193 at `406d91a4`, in-place old → new: anchor `drivers/base/core.c:3508-3510,3542-3543; tag v7.2` → `drivers/base/core.c:3508-3510,3542-3543,4653-4657; tag v7.2`; teaches `The device symlink is created, and removed, only when the device has a parent and is not a partition.` → `On add and on delete, the device symlink is created and removed only when the device has a parent and is not a partition; on a reparent (device_move) the link follows the new parent with no partition check.` The correction is append-only as S202, whose teaches begins `supersedes S193 — `.
```

VERDICT: reject — the first-landed S193 universal “only” claim does not cover the reparent path; the round-34 in-place rewrite also has the form defect cited above.

VERDICT: admit — proposed S202 is supported by the re-opened v7.2 source at the scoped add/delete and move paths; it preserves the correction as a new row.

## Gates and limits

- Fetch/comparison commands completed as recorded above; no counter, gate executable, tests, build, or census was run. The Gate S202 table is a draft from the inspected source, not an executed admission gate.
- Commands used for history: `timeout 120 git -C /home/vgpnk/Projects/shokunin/mori-shokunin diff --no-ext-diff --unified=8 8d56809a:corpus/SOURCES.md 3a7a89ea:corpus/SOURCES.md` and `timeout 30 git -C /home/vgpnk/Projects/shokunin/mori-shokunin show --format=fuller --no-ext-diff --unified=1 406d91a4 -- corpus/SOURCES.md`; both read-only. The second output shows the old/new S193 row. Timestamp command `date -u +%FT%TZ` returned `2026-10-23T08:51:58Z`.
- Touched surfaces: this report and the scratch source copy at `/fast/scratch/hyaku/mori-r35/SrcS193Supersede/core.c`. No product file, Git index, or commit was changed; no tool was installed or updated.
- Out of scope: integrating S202, editing the lesson or SOURCES registry, running lane validation, and making any source-policy or tool changes.
