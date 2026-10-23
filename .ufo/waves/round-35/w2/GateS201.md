measured 2026-10-23T09:15:39Z

# GateS201 — re-open S201 (block/genhd.c v7.2) and judge Gate line

Scope: SOURCES.md row S201 and its Gate row in `corpus/lessons/round-35.md`, both at
`cedb0ec4f3a4f672804deac388b7191258f01fcd`. Source URL:
https://raw.githubusercontent.com/torvalds/linux/v7.2/block/genhd.c

VERDICT: admit — agree with the gate's decision.

## Evidence

1. Fetch + sha256. `timeout 60 curl -fsSL https://raw.githubusercontent.com/torvalds/linux/v7.2/block/genhd.c`
   saved to `/fast/scratch/hyaku/mori-r35/GateS201/genhd.c`; `sha256sum` gives
   `8c2faa1564190e9a8e4cf3ebac5e2561b96818e38560cdcf44fea1761c8d39a5`, matching the Gate's
   `8c2faa15…d39a5` (round-35.md:20 @cedb0ec4).

2. Committed copy. `git show cedb0ec4:corpus/evidence/sources-r33/S182.src | sha256sum` gives the same
   `8c2faa15…d39a5`; `cmp` reports byte-identical. Gate's claim that S201 re-fetch equals the
   committed r33 copy (round-35.md:14) is true.

3. Quotes — all contiguous at stated lines, no `"` or `|` (verified against the fetched bytes
   and the raw `od -c` of round-35.md:20):
   - `ddev->parent = parent;` — genhd.c:485 verbatim.
   - `disk->slave_dir = kobject_create_and_add(` — genhd.c:518 verbatim (line-initial prefix;
     stopping before `"slaves"` keeps the `"` out of the quote).
   - `return add_disk_fwnode(parent, disk, groups, NULL);` — genhd.c:623 verbatim.
   All are ≤25 words by any counting; the parenthesized labels (4,4,6) are each 1 above a
   whitespace-token count (3,3,5). Other Gate rows (S199, S200, S202–S204) label by
   whitespace-token count exactly, so the S201 labels are inconsistent with the table's own
   convention — cosmetic, does not touch the ≤25 cap or the decision.

4. Anchor `block/genhd.c:485-486,512-518,620-623 (__add_disk, device_add_disk); tag v7.2`.
   Lines 485-486 (`ddev->parent = parent; ddev->groups = groups;`) and 512-518 (part0
   `bd_holder_dir` "holders" at 512-513, `slave_dir` "slaves" at 518) sit inside
   `static int __add_disk` (genhd.c:427). `device_add_disk` at 620-623 calls
   `return add_disk_fwnode(parent, disk, groups, NULL);` — parent passed through. Line 518
   content confirmed: `disk->slave_dir = kobject_create_and_add("slaves", &ddev->kobj);`.

5. Teaches (SOURCES.md:207 @cedb0ec4): opens `supersedes S182 —` as required by contract
   item 2 (`.ufo/waves/round-35/contract.md:111`). Claim "carries the anchor lines that
   round 34 added to S182 in place" is true: `git show 8d56809a -- corpus/SOURCES.md` adds
   exactly `485-486,512-518,620-623 (__add_disk parent, holders and slaves directories,
   device_add_disk)` to S182's anchor cell — the same line ranges S201 now anchors. The rest
   of teaches only restates what those lines do (parent/groups set, holders dir for part0,
   slaves dir for disk, parent passed through device_add_disk) — verified at the lines above.

6. S182 untouched this round: `git diff dd76eb79 cedb0ec4 -- corpus/SOURCES.md` contains only
   `+` rows S201 and S202 (and other additions); zero `-`/`+` lines touching `| S182 ` or
   `| S193 ` (`grep -c "^[+-]| S18[23]"` → 0). The round-35 Gate claim "no existing row's
   cell changed in place" (round-35.md:12) holds for S182.

7. Gate decision `admit, A` (round-35.md:20) matches the row's `A` tier, `mined` state, and
   the 2026-10-23 open date.

## Notes

- Not-blocking cosmetic defect: the three quote-count labels (4,4,6) are whitespace+1 while
  sibling rows count whitespace exactly; all quotes remain ≤25 words so the gate's stated
  rule is satisfied either way.
- No installs this seat; all checks used pre-existing tools (curl, sha256sum, git, cmp, sed, od).
