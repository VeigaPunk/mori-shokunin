measured 2026-10-23T07:42:35Z

# GateS191 — wave-B attack on the attempt-2 S191 Gate row and registry row

Seat: MoriR34A3.GateS191. Lane read-only: mori-shokunin @ fd2521351c6cef47384aef30afbe1e4db7e6912e (master).
Scope: (a) re-fetch the S191 URL live, compare with the committed copy; (b) re-locate every Gate quote
in the copy (whitespace runs collapsed); (c) check the draft registry row cell by cell; (d) audit the
attempt-2 report `.ufo/waves/round-34/wa/ReopenS191.md` after reaching an independent verdict.

## 1. Live fetch vs committed copy

Command: `date -u +%FT%TZ; curl -fsSL --max-time 60 https://raw.githubusercontent.com/torvalds/linux/v7.2/block/partitions/core.c -o /tmp/s191-live.c; date -u +%FT%TZ; sha256sum /tmp/s191-live.c`

- Live fetch: 2026-10-23T07:40:51Z, sha256 `add355b5a35d09f77daa435e6f281ab6a3ba801d1b19980c8d5e471f05ed5d17`.
- Committed copy `git show fd2521351c:corpus/evidence/sources-r34/S191.src`: sha256
  `add355b5a35d09f77daa435e6f281ab6a3ba801d1b19980c8d5e471f05ed5d17`, 733 lines, blob `b5c59b79`.
- `cmp -l /tmp/s191-live.c /tmp/s191-committed.c` → no output (byte-identical).

Live == committed. sha256 in the draft Gate row matches.

## 2. Gate quotes re-located in the committed copy (whitespace runs collapsed)

Gate row claims (`drafts/corpus_lessons_round-34.md:16`):

1. `S191.src:208` (5 words): "static DEVICE_ATTR(partition, 0444, part_partition_show, NULL);"
   → line 208 is exactly that text. Contiguous, 5 words, no `"` or `|`. Verified.
2. `S191.src:221-222` (7 words): "static struct attribute *part_attrs[] = { &dev_attr_partition.attr,"
   → lines 221-222 collapse to `static struct attribute *part_attrs[] = { &dev_attr_partition.attr,` (222 is
   `\t&dev_attr_partition.attr,`). Contiguous, 7 words, no `"` or `|`. Verified.
3. `S191.src:266-268` (6 words): "const struct device_type part_type = {"
   → lines 266-268 collapse to `const struct device_type part_type = { .name = "partition", .groups = part_attr_groups,`;
   the quote is the contiguous leading run at line 266. 6 words, no `"` or `|` in the quote itself (the `"`
   in `.name = "partition"` is outside the quoted span). Verified.

All three quotes: contiguous at locator, 3-25 words, word count right, no forbidden characters.

## 3. Draft registry row cell-by-cell (`drafts/corpus_SOURCES.md:197`; added lines 131 in `attempt2-tracked.diff`)

| cell | value | check |
|---|---|---|
| id | S191 | consistent |
| source | Linux block/partitions/core.c at v7.2 … raw.githubusercontent.com/torvalds/linux/v7.2/block/partitions/core.c | URL is the one fetched; title matches file role (partition sysfs attribute) |
| kind | code | a .c source file — correct |
| tier | A | kernel source at a pinned tag — correct |
| scope | the v7.2 `partition` sysfs attribute and the attribute group of the partition device type | matches what the anchors cite |
| anchor | block/partitions/core.c:178-181,208,221-246,266-270; tag v7.2 | each range holds the cited code (see §4) |
| teaches | `partition` is declared with part_partition_show and listed in part_attrs; part_attr_group is in part_attr_groups, which the partition device type `part_type` carries as its groups. lane rule: a `partition` entry under /sys/class/block/<name> marks a partition (tool rule R3). | every non-`lane rule:` clause supported by a located quote (see §5) |
| status | mined | correct — row teaches, is used |
| opened | 2026-10-23 | consistent with fetch |
| recheck | on-release | consistent |
| used-by | tools/mori-disk-rate.py | `git ls-tree fd2521351c -- tools/mori-disk-rate.py` → `100755 blob c7ea8bdac9…` — path exists |

## 4. Anchor line numbers hold the cited code (committed copy)

- 178-181: `static ssize_t part_partition_show(struct device *dev, struct device_attribute *attr, char *buf) { return sysfs_emit(buf, "%d\n", bdev_partno(dev_to_bdev(dev))); }` — the show function. Holds.
- 208: `static DEVICE_ATTR(partition, 0444, part_partition_show, NULL);` — `partition` declared with `part_partition_show`. Holds.
- 221-246: 221 `static struct attribute *part_attrs[] = {`; 222 `&dev_attr_partition.attr,`; 236-238 `static const struct attribute_group part_attr_group = { .attrs = part_attrs, };`; 240-246 `static const struct attribute_group *part_attr_groups[] = { &part_attr_group, … NULL };`. Holds (all inside span).
- 266-270: `const struct device_type part_type = { .name = "partition", .groups = part_attr_groups, .release = part_release, .uevent = part_uevent, };` — `.groups = part_attr_groups` at 268 inside span. Holds.

## 5. Teaches clauses — each supported by a located quote in the copy

1. "`partition` is declared with part_partition_show" — S191.src:208 (see §2.1). Supported.
2. "and listed in part_attrs" — S191.src:221-222 (see §2.2). Supported.
3. "part_attr_group is in part_attr_groups" — S191.src:240-241 collapses to
   `static const struct attribute_group *part_attr_groups[] = { &part_attr_group,` (8 words). Supported
   (part_attr_group defined 236-238, made a member of part_attr_groups at 241).
4. "which the partition device type `part_type` carries as its groups" — S191.src:266
   `const struct device_type part_type = {` (6 words) + S191.src:268 `.groups = part_attr_groups,` (3 words).
   Supported (cross-use at S191.src:344 `pdev->type = &part_type;`).

The remaining clause is labelled `lane rule:` and is excluded from the source-fact requirement.

## 6. Independent verdict (reached before opening the attempt-2 report)

VERDICT: admit — no row cells I would change.

## Audit of /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-34/wa/ReopenS191.md

Factual claims the round would cite, checked against my own evidence:

- §1 Fetch 1 sha256 `add355b5…` at 2026-10-23T05:38:41Z — matches my live sha256. agree
- §1 Fetch 2 sha256 `add355b5…` at 2026-10-23T05:38:43Z — same hash; I could not re-observe its timestamp but the hash matches. agree
- §1 `cmp S191_fetch1.c corpus/evidence/sources-r34/S191.src` identical — my `cmp -l` on the same bytes agrees. agree
- §1 committed copy sha256 `add355b5…` (733 lines) — matches (`git show … | sha256sum`, `wc -l` → 733). agree
- §2 anchor 178-181 = part_partition_show definition — matches copy. agree
- §2 anchor 208 = `static DEVICE_ATTR(partition, 0444, part_partition_show, NULL);` — matches. agree
- §2 anchor 221-246 covers part_attrs, part_attr_group, part_attr_groups — matches. agree
- §2 anchor 266-270 = part_type with `.groups = part_attr_groups` — matches. agree
- §3 clause 1 quote S191.src:208 (5 words) — matches my count. agree
- §3 clause 2 quote S191.src:221-222 (7 words) — matches my count. agree
- §3 clause 3 quote S191.src:240-241 (8 words) `static const struct attribute_group *part_attr_groups[] = { &part_attr_group,` — matches copy. agree
- §3 clause 4 quotes S191.src:266 (6 words) and :268 (3 words) — match copy (268 collapses tabs to `.groups = part_attr_groups,`). agree
- §3 cross-use `pdev->type = &part_type;` at S191.src:344 — present in copy. agree
- §4 proposed Gate row quotes — all consistent with copy; note it proposes two extra quotes (240-241, 268) that the landed draft row does not carry — not a defect, only a narrower final row. agree
- §5 "No tool installs performed this run" — [INFERENCE] not checkable from bytes; plausible. agree

No factual claim in the report that the round would cite is contradicted by the bytes.

AUDIT: agree 15 / disagree 0
