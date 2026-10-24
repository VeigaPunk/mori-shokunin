measured 2026-10-23T09:14:34Z

# ReviewSkillCorr — attack on the two `Round35 correction` bullets in SKILL.md

Seat: MoriR35.ReviewSkillCorr. Lane: mori-shokunin. Object under attack:
`SKILL.md` at `cedb0ec4f3a4f672804deac388b7191258f01fcd`, the two bullets appended under
"Round35 corrections to the Round34 section above" (blob lines 844–858; bullets start :846 and :849).
Read-only: no lane writes, no counter run as module, no git writes. Scratch under
`/fast/scratch/hyaku/mori-r35/ReviewSkillCorr/` (two fetched kernel files only).

## Bullet 1 — S201/S202 attributions (SKILL.md@cedb0ec4:846-848)

Claims: (a) the class rule's `device` entry (S193) now rests on S202, which supersedes S193
append-only — on add and on delete the link exists only for a device with a parent that is not a
partition, and a reparent moves it with no partition check; (b) the `__add_disk` lines round 34 added
to S182 in place now rest on S201, which supersedes S182.

Checked:
- S201 and S202 exist as their own rows, `corpus/SOURCES.md:207-208`, each `mined`, tier A, teaches
  cell begins `supersedes S182 —` / `supersedes S193 —`. S182 and S193 still stand unmodified
  (`SOURCES.md:188,199`), so "append-only" is accurate.
- The prior in-place edits the supersession repairs are real: `corpus/lessons/round-35.md:34-40`
  logs S182's anchor change at `8d56809a` and S193's anchor+teaches rewrite at `406d91a4`.
- Independent code check (fetched `v7.2` files; sha256 `8c2faa15…d39a5` genhd.c and
  `fa223c8f…1c9fa` core.c, both matching the Gate table `round-35.md:21-22`):
  - `drivers/base/core.c:3508` `if (dev->parent && device_is_not_partition(dev))` guards
    `sysfs_create_link(..., "device")`; `:3542` same guard for `sysfs_remove_link` — add/delete
    clause true.
  - `core.c:4653-4657` `device_move_class_links` removes under `old_parent` and creates under
    `new_parent` with `if (old_parent)` / `if (new_parent)` — no partition check; `core.c:2430-2433`
    defines `device_is_not_partition` and it is not used there. Called from `device_move` at
    `:4704-4706`. "Reparent moves it with no partition check" is literal.
  - `block/genhd.c:485` `ddev->parent = parent;`, `:512-518` creates `holders` for part0 and
    `slave_dir`, `:620-623` `device_add_disk` returns `add_disk_fwnode(parent, disk, groups, NULL)`
    — every anchor line S201 carries is in `__add_disk`/`device_add_disk` as claimed.

VERDICT: supported — every attribution resolves to a committed row and every quoted line verifies
against the fetched v7.2 bytes.

## Bullet 2 — miscited S192, observed-not-sourced, "twelve candidate files" (SKILL.md@cedb0ec4:849-858)

Sub-claims:

1. "a stacked device maps onto devices already counted (S192)" is miscited; S192 supplies only the
   `slaves` classification. Supported: the Round34 rule does say that (`SKILL.md@cedb0ec4` last
   Round34 bullet), and `SOURCES.md:198` (S192) covers only `bd_link_disk_holder` symlinks and the
   lane rule "a non-empty `slaves` directory marks a stacked device" — nothing about write
   accounting on the backing device.
2. "a dm-0 write-sector delta equalled its slave partition's and its disk's (219728 sectors over
   30 s, `.ufo/waves/round-34/wb/ExecStackedRemeasure.md`)". Supported exactly: the report's 30 s
   measurement table shows Δ write-sectors **219728** for dm-0, nvme0n1p2 and nvme0n1 (§2 table and
   the bullet "Δ(dm-0) == Δ(nvme0n1p2) == Δ(nvme0n1) == 219728 sectors, bit-exact"); window is
   "midpoint interval exactly 30000 ms". Numbers and topology match verbatim.
3. "S203 and S204 are kept as rejected rows". Supported: `SOURCES.md:209-210`, both status
   `rejected`, REJECTED rationale matching the sweep reasons in `round-35.md` Gate table.
4. "none states it". Supported for every opened candidate — each per-file section of
   `.ufo/waves/round-35/w1/SrcDmStack.md` records a non-stating result (iostats.rst:39-40 only tells
   the reader to sum all devices; dm.c:1379-1386 accounts the original bio only; blk-core.c:812-813
   is the resubmit rule; collectl Disks.html:24-25 excludes dm from its summary without stating the
   underlying-device accounting).
5. "twelve candidate files". **Unsupported.** SrcDmStack.md's own record enumerates more than
   twelve files opened this round: five `### Candidates` files + `iostat.c`, `FAQ.md`, `README.md`,
   `man/sar.in` (opened inline, `:53`) + `dm-linear.c`, `md.rst`, `statistics.rst` (`:71-73`) +
   collectl `Disks.html`, `collectl`, `man1/collectl.1`, `docs/WhySummary.html` = at least 16
   distinct files fetched and searched (17 counting the never-fetched `md.c` carry-over excluded).
   The lesson's own accounting at `round-35.md:25-29` ("Identified 12, included 0") reaches 12 only
   by omitting `sysstat/README.md` and `md.rst` from its file list while the sweep log records both
   as opened. The count is off; the "none states it" conclusion is not affected — every additional
   opened file also fails to state the claim.
6. Closing directives "Do not sum a stacked device with its slaves; why the backing line also moves
   stays FR6 frontier." Supported as honest scoping: ExecStackedRemeasure.md confirms the summing
   hazard empirically (dm-0 bytes appear three times in a naive sum) and no admitted source explains
   the mechanism.

VERDICT: supported — miscited-S192, observed-not-sourced, 219728, and S203/S204-rejected clauses all
verify; but the numeral "twelve" undercounts the files SrcDmStack.md records as opened (≥16,
including sysstat `README.md`, `iostat.c`, `FAQ.md`, `man/sar.in`, kernel `md.rst`, `dm-linear.c`,
`statistics.rst`, and three collectl files). Defect is numeric-only; no claim's substance flips.

## Summary

VERDICT: supported — bullet 1 (S201 supersedes S182; S202 supersedes S193, append-only, add/delete
parent-not-partition, reparent with no partition check): all attributions and code lines verified.
VERDICT: supported — bullet 2 substance (S192 miscited; clause observed-not-sourced; 219728 sectors
over 30 s matches ExecStackedRemeasure.md; S203/S204 rejected rows; sweep conclusion "none states
it" holds for every file opened).
VERDICT: unsupported — bullet 2 numeral "twelve candidate files": SrcDmStack.md records ≥16 opened
files; lesson `round-35.md:29` "Identified 12" omits opened files (sysstat `README.md`, `md.rst`)
from its own sweep list.

## Residual risk / gaps

- I did not re-fetch the non-kernel candidates (iostats.rst, sysstat, util-linux, collectl);
  "none states it" rests on SrcDmStack.md's logged line-level checks, all reproducible from its
  recorded sha256s.
- The "twelve" count is a reporting defect, not a correctness defect in the rule text.
- No tool installed or updated (pacman paused host-wide; `curl` was already present). Scratch:
  2 files under `/fast/scratch/hyaku/mori-r35/ReviewSkillCorr/`. No processes left running.
