measured 2026-10-23T05:41:24Z

# ReopenS191 — live re-fetch and clause-by-clause verdict (round 34, wave A)

Seat: MoriR34A2.ReopenS191. Lane: mori-shokunin @ 8d56809afccefe0ab80c8e73ac3e1ea57c25f5f3 (master).
Scope: re-open S191 (Linux block/partitions/core.c @ v7.2) live; judge anchor + teaches against the
committed copy corpus/evidence/sources-r34/S191.src; propose Gate row or reject.

## 1. Live re-fetch (twice, into scratch)

Command (each): `timeout 60 curl -sSL --fail -m 60 https://raw.githubusercontent.com/torvalds/linux/v7.2/block/partitions/core.c -o S191_fetch{N}.c`

- Fetch 1: sha256 `add355b5a35d09f77daa435e6f281ab6a3ba801d1b19980c8d5e471f05ed5d17` at 2026-10-23T05:38:41Z
- Fetch 2: sha256 `add355b5a35d09f77daa435e6f281ab6a3ba801d1b19980c8d5e471f05ed5d17` at 2026-10-23T05:38:43Z
- `cmp S191_fetch1.c S191_fetch2.c` → identical (FETCHES_IDENTICAL).
- `cmp S191_fetch1.c corpus/evidence/sources-r34/S191.src` → identical (MATCHES_COMMITTED).
- Committed copy sha256: `add355b5a35d09f77daa435e6f281ab6a3ba801d1b19980c8d5e471f05ed5d17` (733 lines).
- `--fail` guarantees the raw URL resolved (no 404 proxy page); tag v7.2 served the file.

## 2. Anchor verification (block/partitions/core.c:178-181,208,221-246,266-270; tag v7.2)

All ranges read from the committed copy S191.src (line numbers are file line numbers):

- 178-181 — `part_partition_show` definition.
  - 178: `static ssize_t part_partition_show(struct device *dev,`
  - 179: `				   struct device_attribute *attr, char *buf)`
  - 180: `{`
  - 181: `	return sysfs_emit(buf, "%d\n", bdev_partno(dev_to_bdev(dev)));`
  Holds.
- 208 — `static DEVICE_ATTR(partition, 0444, part_partition_show, NULL);` — `partition`
  attribute declared with `part_partition_show`. Holds.
- 221-246 — 221 `static struct attribute *part_attrs[] = {`; 222 `	&dev_attr_partition.attr,`
  (listed in part_attrs); 236-238 `static const struct attribute_group part_attr_group = { .attrs = part_attrs, };`;
  240-246 `static const struct attribute_group *part_attr_groups[] = { &part_attr_group, ... NULL };`.
  Holds (222, 236-238, 240-246 all inside the cited span).
- 266-270 — `const struct device_type part_type = { .name = "partition", .groups = part_attr_groups,
  .release = part_release, .uevent = part_uevent, };` (266-271; 268 `.groups = part_attr_groups`).
  Holds.

No anchor line mismatch found.

## 3. Teaches clause-by-clause (quotes from S191.src; all quotes free of `"`/`|`)

Teaches cell: "`partition` is declared with part_partition_show and listed in part_attrs; part_attr_group
is in part_attr_groups, which the partition device type `part_type` carries as its groups. lane rule: a
`partition` entry under /sys/class/block/<name> marks a partition (tool rule R3)."

Non-lane-rule clauses:

1. "`partition` is declared with part_partition_show"
   S191.src:208 (5 words): "static DEVICE_ATTR(partition, 0444, part_partition_show, NULL);"
   Supported.
2. "and listed in part_attrs"
   S191.src:221-222 (7 words): "static struct attribute *part_attrs[] = { &dev_attr_partition.attr,"
   Supported.
3. "part_attr_group is in part_attr_groups"
   S191.src:240-241 (8 words): "static const struct attribute_group *part_attr_groups[] = { &part_attr_group,"
   Supported (part_attr_group at 236-238, element of part_attr_groups at 241).
4. "which the partition device type `part_type` carries as its groups"
   S191.src:266 (6 words): "const struct device_type part_type = {"
   S191.src:268 (3 words): ".groups		= part_attr_groups,"
   Supported (part_type at 266, .groups = part_attr_groups at 268; also used at 344 `pdev->type = &part_type;`).

Lane-rule clause (excluded from quote requirement, per assignment): "a `partition` entry under
/sys/class/block/<name> marks a partition (tool rule R3)" — lane rule, not source-fact; no quote required.

## 4. Proposed Gate row

| S191 | https://raw.githubusercontent.com/torvalds/linux/v7.2/block/partitions/core.c | 2026-10-23T05:38:41Z | add355b5a35d09f77daa435e6f281ab6a3ba801d1b19980c8d5e471f05ed5d17 | S191.src:208 "static DEVICE_ATTR(partition, 0444, part_partition_show, NULL);"; S191.src:221-222 "static struct attribute *part_attrs[] = { &dev_attr_partition.attr,"; S191.src:240-241 "static const struct attribute_group *part_attr_groups[] = { &part_attr_group,"; S191.src:266 "const struct device_type part_type = {"; S191.src:268 ".groups		= part_attr_groups," | admit, A, mined |

## 5. Residual risk / verification gaps

- Fetches used the same day/tag; remote content is time-stamped by sha256 match to the committed copy
  (recorded opened date 2026-10-23; recheck policy on-release). A future upstream rewrite of v7.2 would
  only affect recheck, not this admission.
- No tool installs performed this run (curl, sha256sum, date, cmp all already present); per operator
  directive, nothing to record.

VERDICT: admit
