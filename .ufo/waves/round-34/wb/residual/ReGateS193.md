measured 2026-10-23T07:58:35Z

# ReGateS193 — residual review of revised S193 row (round 34, attempt 3)

Object: revised S193 row at /fast/scratch/hyaku/mori-r34/a3-L1/residual-snap/corpus_SOURCES.md:199.
Source copy: /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/evidence/sources-r34/S193.src (5434 lines, tag v7.2).
Prior rejection: .ufo/waves/round-34/wb/GateS193.md (defect: un-scoped "only when is not a partition" universal falsified by reparent path).

## 1. Anchor lines hold the cited code
- 3508-3510: `if (dev->parent && device_is_not_partition(dev)) {` / `error = sysfs_create_link(&dev->kobj, &dev->parent->kobj,` / `"device");` — guarded create inside device_add_class_symlinks (def 3487). HELD.
- 3542-3543: `if (dev->parent && device_is_not_partition(dev))` / `sysfs_remove_link(&dev->kobj, "device");` — guarded remove inside device_remove_class_symlinks (def 3532). HELD.
- 4653-4657: body of device_move_class_links (def 4647): `if (old_parent) sysfs_remove_link(&dev->kobj, "device");` (4653-4654), `if (new_parent) error = sysfs_create_link(&dev->kobj, &new_parent->kobj, "device");` (4655-4657). Called by exported device_move (def 4667) at 4706 and 4709. HELD.

## 2. Clause quote support (non-lane clauses, contiguous 3-25 word quotes)
- Clause 1: "On add and on delete, the `device` symlink is created and removed only when the device has a parent and is not a partition" — supported by S193.src:3508 `if (dev->parent && device_is_not_partition(dev))` (7w, contiguous) for add and S193.src:3542 same condition (4w) for delete. PASS.
- Clause 2: "on a reparent (`device_move`) the link follows the new parent with no partition check" — supported by S193.src:4655-4657 (create iff new_parent) and 4653-4654 (remove iff old_parent). `device_is_not_partition` appears nowhere in device_move_class_links (grep hits only 2430/2435 defs, 3508, 3542). After reparent the link exists iff new_parent is non-NULL, so "follows the new parent" also covers the NULL-new_parent case (link absent). PASS.
- Lane clause: "a `device` entry marks a whole disk with a parent device (tool rule R3)" — tool R3 (tools/mori-disk-rate.py:46-48, probed at :197) classifies a `device` entry as "disk"; the partition and slaves probes precede it (:192-196), so a classified "disk" is not a partition and has a parent (guard at 3508/3542). HELD.

## 3. Other create/remove paths of the `device` link
grep of S193.src for all sysfs create/remove/delete of the "device" link: creates at 3510 (guarded) and 4657 (move); removes at 3522 (add-error unwind `out_device:`, only reachable after the guarded create at 3508-3510 succeeded), 3543 (guarded delete), 4654 (move). No other sites. The revised scoping (add/delete guarded; reparent unguarded) covers all of them; 3522 is a benign cleanup of a link that only exists because the guard held, so it does not falsify clause 1.

## 4. Verdict
VERDICT: admit — the revised teaches cell is supported; no text change needed. Cell kept verbatim: "On add and on delete, the `device` symlink is created and removed only when the device has a parent and is not a partition; on a reparent (`device_move`) the link follows the new parent with no partition check."

## Residual risk / gaps
- Device_move callers not enumerated; the row claims behavior of the link helpers, not caller topology. device_move's own comment (S193.src:4663) confirms new_parent "can be NULL", covered by clause 2 wording.
- Tool docstring gloss (tools/mori-disk-rate.py:47-48) omits the parent half of the guard, but that is tool text, not the judged row; the lane clause matches the tool's code behavior.
- Tooling: nothing installed (pacman paused; no need); used read/grep only. /fast has 212G free; no scratch writes needed. No processes left running.
