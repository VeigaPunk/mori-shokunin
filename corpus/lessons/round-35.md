author: mori-shokunin L1 MoriR35 (round 35, attempt 1)

# mori round 35 — lesson

Entering tip `dd76eb79` (round 34 closed `rejected-honest-stop`, MANIFEST `rounds[524]`). One measured claim, C1
(calibration): the SCORECARD capabilities register agrees with the fleet closure record (contract
`.ufo/waves/round-35/contract.md`, counter `count-c1.py`, frozen at `f2d28711`; control wave C0 receipts at `913df22e`;
register landed at `721040a9`).

## Gate (rows opened 2026-10-23 in round 35)

Six rows appended after S198 (S199–S204); no existing row's cell changed in place this round. Four are admitted (tier A,
`mined`), two are rejected. Copies: `corpus/evidence/sources-r35/S199.src`, `S203.src`, `S204.src`; S201 and S202 re-fetched
bytes are identical to the committed `corpus/evidence/sources-r33/S182.src` and `sources-r34/S193.src`, so no new copy.

| row | URL (accessed 2026-10-23) | sha256 | quote (≤25 words, location) | decision |
|---|---|---|---|---|
| S199 | https://raw.githubusercontent.com/VeigaPunk/kimi-shokunin/b47dfbe2cd185e33f9aa42a66a9e6c63c9591d5b/skills/shokunin/protocol/AXES.md | `04ea5c9e…7d993` | (23 words) Rows enter only through a round that demonstrates the capability running; a capability without a passing demonstration in the round report is pre-claiming — `AXES.md:62-64`; (9 words) Self-assessment quality: gaps named honestly, confidence graded, overreach caught — `:15` | admit, A (SrcAxes; byte-identical to the fleet `AXES.md`) |
| S200 | `git -C /home/vgpnk/Projects/shokunin show 37b51a243302e8009c7067431e8a47f9a722fd14:MANIFEST.json` (own-work dataset; a repo command, CORPUS rule for `own-work`) | `0b414b8a…ae9952` | (5 words) sources-registry (34 rows; census clean) — `rounds[313].capabilities_added[0]` | admit, A (SrcManifest: 13 admitted mori entries carry 18 capabilities) |
| S201 | https://raw.githubusercontent.com/torvalds/linux/v7.2/block/genhd.c | `8c2faa15…d39a5` | (4) ddev->parent = parent; — `block/genhd.c:485`; (4) disk->slave_dir = kobject_create_and_add( — `:518`; (6) return add_disk_fwnode(parent, disk, groups, NULL); — `:623` | admit, A, `supersedes S182 —` (SrcS182Supersede) |
| S202 | https://raw.githubusercontent.com/torvalds/linux/v7.2/drivers/base/core.c | `fa223c8f…1c9fa` | (5) if (dev->parent && device_is_not_partition(dev)) { — `drivers/base/core.c:3508`; (2) if (new_parent) — `:4655`; (5) error = device_move_class_links(dev, old_parent, new_parent); — `:4706` | admit, A, `supersedes S193 —` (SrcS193Supersede) |
| S203 | https://raw.githubusercontent.com/sharkcz/collectl/4.3.20.3/docs/Disks.html | `c84b28a2…7681b8e` | (10) Device mapper disks, while listed in the detail data are — `docs/Disks.html:24` | **reject**: excludes device-mapper disks from a summary to avoid double counting, but never says the same I/O is on the backing device's line; omits md (SrcDmStack) |
| S204 | https://raw.githubusercontent.com/torvalds/linux/v7.2/drivers/md/dm.c | `b01ff2d6…bab8b02b` | (16) Account io->origin_bio to DM dev on behalf of target that took ownership of IO with DM_MAPIO_SUBMITTED. — `drivers/md/dm.c:1379-1380` | **reject**: accounts the original bio to the dm device and resubmits a clone (`:1386`), but does not show the backing device's diskstats line counting it (SrcDmStack) |

Also opened by SrcDmStack and rejected without a row (no stating sentence; sweep in `.ufo/waves/round-35/w1/SrcDmStack.md`):
Linux v7.2 `Documentation/admin-guide/iostats.rst`, `block/blk-core.c`, `drivers/md/dm-linear.c`,
`Documentation/admin-guide/device-mapper/statistics.rst`; sysstat v12.8.0 `man/iostat.in`, `iostat.c`, `FAQ.md`, `man/sar.in`;
util-linux v2.42.4 `misc-utils/lsblk.8.adoc`, `misc-utils/lsblk.c`. Search question: does any primary source state that
I/O to a stacked block device is also accounted on its underlying devices in /proc/diskstats? Identified 12, included 0.
Result: `SKILL.md`'s stacked-device clause is marked observed, not sourced (SKILL Round35 corrections).

Row changes logged old→new this round: none (status, recheck and used-by of existing rows unchanged).
Round-34 in-place changes now superseded (routed defect 2):
- S182 anchor, changed in place at `8d56809a`: `block/genhd.c:1353,1371-1374,1395,1403,1418-1425 (diskstats_show,
  diskstats_op, proc_create_seq); tag v7.2` → the same plus `; 485-486,512-518,620-623 (__add_disk parent, holders and
  slaves directories, device_add_disk)`. The added lines now rest on S201. S182 itself is left as it stands.
- S193 anchor and teaches, rewritten in place at `406d91a4`: anchor `drivers/base/core.c:3508-3510,3542-3543; tag v7.2`
  → `…,4653-4657; tag v7.2`; teaches `The device symlink is created, and removed, only when the device has a parent and
  is not a partition.` → `On add and on delete, … ; on a reparent (device_move) the link follows the new parent with no
  partition check.` The rescoped content now rests on S202. S193 itself is left as it stands.

## Corrections (append-only) to `corpus/lessons/round-34.md`

- `round-34.md:46` says "No status or recheck cell of an existing row changed." It is literally true and misleading: at
  `8d56809a` S182's anchor cell changed in place, and at `406d91a4` S193's anchor and teaches cells were rewritten in
  place (CORPUS §SOURCES.md rule 2 allows only status, recheck and used-by). Both are now superseded by S201 and S202.

## Round-34 routed defects (closure §6) — outcome

| item | outcome | pointer |
|---|---|---|
| 1 counter discrimination | clause 2 of round-33 §8 item 1 answered by QUALITY 100; P-C1-A1's live arm is not re-claimed (C1 of round 34 stays an honest stop); this round's counter has two-sided bounds per arm, but see M1 | `corpus/QUALITY.md` 100 |
| 2 SOURCES append-only | supersede rows S201, S202; `round-34.md:46` corrected above; check script and QUALITY 102 | `corpus/SOURCES.md`; `.ufo/waves/round-35/check-sources-appendonly.py` |
| 3 dangling `w1/` pointer | append-only correction naming the committed wave-A and wave-B judges | `corpus/knowledge/disk-write-rate-r33.md` § Round-35 correction |
| 4 `SKILL.md:834` | marked observed, not sourced; twelve candidate files opened, none states it; S203, S204 rejected | `SKILL.md` Round35 corrections |
| 5 QUALITY 98 worked example | append-only 98 correction (D1, D2, D4) | `corpus/QUALITY.md` 98 correction |
| 6 operator items | left alone: `LOG.md:1801`, `refs/jj/keep/…` `3b19cac`, SHONEN promotion | — |
| Axes table (found this round) | `Last change` for operability and depth said round 28 and round 12; the latest admitted closure grading each improved is round 31 (`MANIFEST rounds[495]`; `round-31-verifier-spotcheck.md:154-155`); cells corrected, each naming its old value | `SCORECARD.md:11-12`; `.ufo/waves/round-35/w1/AxesOracle.md` |

## Mistakes

| id | class | evidence | captured-by | fix (shown able to fail) |
|---|---|---|---|---|
| M1 | a control that met the frozen counter before data was ruled a residual instead of forcing a re-design | `.ufo/waves/round-35/evidence/c1-controls.txt` (10c CtlSkipDesign B: empty capability and what cells, `C1=met`; 9d: unbackticked dangling prose, `C1=met`); the contract's control list maps none of QUALITY 98's server-echo, observed-column-copy, no-decision or rule-changed shapes and has no denial control, which the sibling closure kaidoku round 32 (`kaidoku-shokunin/corpus/lessons/round-32-verifier-spotcheck.md:76,116`) requires of a calibration counter | QUALITY 98 (content-free shape; "a control the counter scores as met means the counter or the target is wrong") — it should have caught it, and the L1 did not apply it | QUALITY 101 and the 98 correction's last sentence; shown able to fail on this round's receipt (10c) |
| M2 | SOURCES cells edited in place, and a lesson sentence that hid it | round 34: S182 at `8d56809a`, S193 at `406d91a4`; `round-34.md:46`; the check also finds 15 ids edited in place before round 34 | CORPUS §SOURCES.md rule 2 and QUALITY 81 state the rule, but no check enforced it | QUALITY 102 with `.ufo/waves/round-35/check-sources-appendonly.py`: exit 1 with 17 ids at `dd76eb79`; S182 and S193 discharged by S201/S202 (15 remain, routed) |
| M3 | the SCORECARD capabilities field stayed `— none yet —` from `d677cf3` while closures admitted 18 capabilities; each round wrote its own per-round table instead | `SCORECARD.md:586-592`; `.ufo/waves/round-35/w1/RevengerNoneYet.md` | none | the round-35 register and P-C1: `count-c1.py dd76eb79` → `mismatches=23 C1=unmet` |
