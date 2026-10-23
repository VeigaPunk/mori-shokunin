measured 2026-10-23T05:39:44Z

# Reopen S193 — verification report (seat MoriR34A2.ReopenS193)

Row: corpus/SOURCES.md line 199 at 8d56809afccefe0ab80c8e73ac3e1ea57c25f5f3
(blob ef1207c8261aea42c3a52e92e901ccb319dc99ff, identical at tip fd2521351c6cef47384aef30afbe1e4db7e6912e).
Source: https://raw.githubusercontent.com/torvalds/linux/v7.2/drivers/base/core.c
Committed copy: corpus/evidence/sources-r34/S193.src (5434 lines, 151293 bytes).

## 1. Live re-check (two fetches)
- `curl -sSL --fail -m 60 -o S193.live1 <url>`: OK, `date -u +%FT%TZ` = 2026-10-23T05:38:54Z,
  sha256 = fa223c8f9f1bb40ca52c73f156439d311065e9be04efa2c6cf57039940e1c9fa.
- second identical fetch (S193.live2): same date, same sha256 (matches).
- Committed copy: sha256 of corpus/evidence/sources-r34/S193.src (working tree) =
  fa223c8f9f1bb40ca52c73f156439d311065e9be04efa2c6cf57039940e1c9fa; blob at
  8d56809 = 4d026682944f218445a232b23d8ccd607bc693fe (rev-parse) and blob at tip =
  same 4d026682…; `cmp` of extracted S193.src@8d56809 vs live1 and vs working tree:
  both byte-identical (exit 0). `git status --porcelain` clean for both SOURCES.md
  and S193.src.
- Note: lane tip is fd2521351 (round-34 wave-A dispatch, pre-judgment), not 8d56809;
  both SOURCES.md and S193.src blobs are identical at the two revs, so judgment unaffected.

## 2. Anchor cell clauses ("drivers/base/core.c:3508-3510,3542-3543; tag v7.2")
- A1: lines 3508-3510 hold the cited creation block. Verbatim (S193.src@8d56809:3508-3510):
  `if (dev->parent && device_is_not_partition(dev)) {` /
  `error = sysfs_create_link(&dev->kobj, &dev->parent->kobj,` / `"device");`. Held.
- A2: lines 3542-3543 hold the cited removal block. Verbatim (:3542-3543):
  `if (dev->parent && device_is_not_partition(dev))` / `sysfs_remove_link(&dev->kobj, "device");`. Held.
- A3: tag v7.2 resolves and serves the URL (two successful fetches) and the served bytes
  equal the committed copy (see §1). Held.

## 3. Teaches cell clauses (teaches cell of the row)
Clause T1 — `device` symlink is created only when the device has a parent:
- S193.src:3508 (5 words): "if (dev->parent && device_is_not_partition(dev)) {"
- S193.src:3509 (4 words): "error = sysfs_create_link(&dev->kobj, &dev->parent->kobj,"
Clause T2 — created only when the device is not a partition:
- S193.src:3508 (5 words): "if (dev->parent && device_is_not_partition(dev)) {"
- S193.src:2432 (4 words): "return !(dev->type == &part_type);" (device_is_not_partition
  body, defined at 2430-2433 under CONFIG_BLOCK).
Clause T3 — removed only when the device has a parent:
- S193.src:3542 (4 words): "if (dev->parent && device_is_not_partition(dev))"
- the immediately following line 3543 executes `sysfs_remove_link(&dev->kobj, "device");`
  (quote omitted because it contains `"`).
Clause T4 — removed only when the device is not a partition:
- S193.src:3542 (4 words): "if (dev->parent && device_is_not_partition(dev))"
- predicate defined at S193.src:2432 (4 words): "return !(dev->type == &part_type);"
Clause T5 — `lane rule: a `device` entry marks a whole disk with a parent device
(tool rule R3).` — lane-rule clause, exempt per instructions.
All clauses supported; none unsupported.

## 4. Cross-checks (whole file, grep enumeration)
- The only create/remove sites for a symlink named "device" are 3510 (create, guarded),
  3522 (error-path cleanup), 3543 (remove, guarded) — all inside
  device_add_class_symlinks/device_remove_class_symlinks (defs at 3487, 3532) — and
  4653-4657 in device_move_class_links (helper of device_move, def at 4651), which
  reparents a device without the partition guard. The reparent path is outside the
  cited anchor lines and outside the row's "creates and removes" claim; noted as residual.
- device_add_class_symlinks is invoked from device_add (S193.src:3708,
  "error = device_add_class_symlinks(dev);" — 3 words); device_remove_class_symlinks
  from device_del (S193.src:3947) and from device_add error path (3814). This supports
  the row's scope phrase "driver core creates and removes a class device's `device` symlink".

## 5. Proposed Gate row
| S193 | https://raw.githubusercontent.com/torvalds/linux/v7.2/drivers/base/core.c | 2026-10-23T05:38:54Z | fa223c8f9f1bb40ca52c73f156439d311065e9be04efa2c6cf57039940e1c9fa | 3508 "if (dev->parent && device_is_not_partition(dev)) {" (5w); 3509 "error = sysfs_create_link(&dev->kobj, &dev->parent->kobj," (4w); 3542 "if (dev->parent && device_is_not_partition(dev))" (4w); 2432 "return !(dev->type == &part_type);" (4w); 3708 "error = device_add_class_symlinks(dev);" (3w) | admit, A, mined |

VERDICT: admit

## 6. Residual risk / verification gaps
- device_move_class_links (S193.src:4651-4658) maintains the "device" symlink on
  reparent without the not-a-partition guard; it is not exercised by the row's cited
  add/del code and is outside the claim scope, but it is the only adjacent exception.
- Live match is a point-in-time byte equality of the tag URL (05:38:54Z); tag
  mutability is not asserted.
- Tooling: nothing installed (no installs needed; RULES.md read at
  /home/vgpnk/.omp/agent/RULES.md). Fetches used system curl; hashes used sha256sum;
  git reads used only read-only rev-parse/show/status.
