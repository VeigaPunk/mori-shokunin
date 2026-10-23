measured 2026-10-23T09:16:21Z

# GateS202 — re-open S202 live (round 35 wave 2)

Scope: row `corpus/SOURCES.md:208` at `cedb0ec4f3a4f672804deac388b7191258f01fcd` and its Gate line
`corpus/lessons/round-35.md:21` at the same rev. Source:
`https://raw.githubusercontent.com/torvalds/linux/v7.2/drivers/base/core.c`; committed copy
`corpus/evidence/sources-r34/S193.src`. Gate decision under attack: `admit, A, supersedes S193 —`
(round-35.md:21).

## Byte fidelity

- `timeout 100 curl -fsSL -o /fast/scratch/hyaku/mori-r35/MoriR35.GateS202/core.c <URL>` →
  `sha256sum` = `fa223c8f9f1bb40ca52c73f156439d311065e9be04efa2c6cf57039940e1c9fa`, 5434 lines,
  151293 bytes. Matches the Gate's truncated `fa223c8f…1c9fa` (round-35.md:21).
- `git show cedb0ec…:corpus/evidence/sources-r34/S193.src | sha256sum` → same
  `fa223c8f…e1c9fa`, 5434 lines, 151293 bytes; `cmp -s` live-vs-copy printed `CMP_IDENTICAL`.
  Confirms round-35.md:13 ("S201 and S202 re-fetched bytes are identical to the committed …
  sources-r34/S193.src, so no new copy").

## Quote checks (Gate line, round-35.md:21)

All quotes contiguous at stated lines in the live file; word counts match the `(n)` markers;
none contains `"` or `|`:

- `(5) if (dev->parent && device_is_not_partition(dev)) {` — live `core.c:3508`, exact line, 5 words.
- `(2) if (new_parent)` — live `core.c:4655`, exact line, 2 words.
- `(5) error = device_move_class_links(dev, old_parent, new_parent);` — live `core.c:4706`, exact
  line, 5 words.

The row itself (SOURCES.md:208) contains no source quotes; its code cells (`device`,
`device_is_not_partition(dev)` naming in teaches) match identifiers at the anchors.

## Anchor ranges (row cell `drivers/base/core.c:2430-2433,3508-3510,3542-3543,4653-4657,4704-4706; tag v7.2`)

- `2430-2433`: `static inline int device_is_not_partition` under `#ifdef CONFIG_BLOCK`, body
  `return !(dev->type == &part_type);` — live `core.c:2429-2439`.
- `3508-3510`: `if (dev->parent && device_is_not_partition(dev)) { error = sysfs_create_link(&dev->kobj,
  &dev->parent->kobj, "device")` — live `core.c:3508-3510` inside `device_add_class_symlinks`.
- `3542-3543`: `if (dev->parent && device_is_not_partition(dev)) sysfs_remove_link(&dev->kobj,
  "device");` — live `core.c:3542-3543` inside `device_remove_class_symlinks` (`:3532`).
- `4653-4657`: `device_move_class_links` (`:4647`) body: `if (old_parent) sysfs_remove_link(...,
  "device"); if (new_parent) error = sysfs_create_link(..., "device")` — no partition check present.
- `4704-4706`: `device_move` (`:4667`) calls it under `if (dev->class)` at `:4705-4706`.
- Tag `v7.2` is part of the fetched URL; bytes verified above.

## teaches entailment (SOURCES.md:208)

Teaches opens verbatim `supersedes S193 —` as required. Source-derived content: "on add and on
delete the `device` symlink is created and removed only when the device has a parent and is not a
partition" = the guards at `:3508` and `:3542`; "device_move_class_links, called by device_move,
removes it under the old parent and creates it under the new parent with no partition check" =
`:4653-4657` plus call site `:4706`. No claim beyond the anchors. The `when` cell ("when the v7.2
driver core creates and removes a class device's `device` symlink") covers the same three paths.
Status `mined`, date 2026-10-23, recheck `on-release`, used-by `SKILL.md` — consistent with the
admitted-row shape of S199–S201 in the same hunk.

## Supersession bookkeeping

- teaches opens `supersedes S193 —` — confirmed at SOURCES.md:208.
- `timeout 60 git -C …/mori-shokunin diff dd76eb79 cedb0ec4f3a4f672804deac388b7191258f01fcd --
  corpus/SOURCES.md` → `6 insertions(+), 0 deletions`, single hunk `@@ -202,6 +202,12 @@` appending
  S199–S204. Neither S182 nor S193 (SOURCES.md:199 at rev, still carrying the round-34 in-place
  anchor `3508-3510,3542-3543,4653-4657`) appears in the diff — both left as they stand, matching
  round-35.md:11 ("no existing row's cell changed in place this round") and the round-35.md:36-40
  edit-history bullets.

## Verdict

VERDICT: admit — agree with the Gate's `admit, A, supersedes S193` decision; live bytes, sha256,
quotes, anchors, teaches and supersession bookkeeping all check out.

## Residual risk / gaps

- Teaches says "is not a partition" without noting the predicate is meaningful only under
  `CONFIG_BLOCK` (`core.c:2429-2439`); the anchor range `2430-2433` does cite the `#ifdef` body, and
  the admitted S193 teaches used the same phrasing, so this is residual fidelity, not a defect.
- `3508-3510` shows only the create call's first two lines; the `"device"` link name is on `:3510`
  (in range) — covered.
- Not re-run: `count-c1.py` (out of scope for a source row), S201's own checks (another seat),
  lanes' build/test suite.
- No tools installed or updated; no writes outside this report and scratch
  `/fast/scratch/hyaku/mori-r35/MoriR35.GateS202/core.c`; all lane git was read-only
  (show/diff).
