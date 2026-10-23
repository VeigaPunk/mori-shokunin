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
| S201 | https://raw.githubusercontent.com/torvalds/linux/v7.2/block/genhd.c | `8c2faa15…d39a5` | (3) ddev->parent = parent; — `block/genhd.c:485`; (3) disk->slave_dir = kobject_create_and_add( — `:518`; (5) return add_disk_fwnode(parent, disk, groups, NULL); — `:623` | admit, A, `supersedes S182 —` (SrcS182Supersede) |
| S202 | https://raw.githubusercontent.com/torvalds/linux/v7.2/drivers/base/core.c | `fa223c8f…1c9fa` | (5) if (dev->parent && device_is_not_partition(dev)) { — `drivers/base/core.c:3508`; (2) if (new_parent) — `:4655`; (5) error = device_move_class_links(dev, old_parent, new_parent); — `:4706` | admit, A, `supersedes S193 —` (SrcS193Supersede) |
| S203 | https://raw.githubusercontent.com/sharkcz/collectl/4.3.20.3/docs/Disks.html | `c84b28a2…7681b8e` | (10) Device mapper disks, while listed in the detail data are — `docs/Disks.html:24` | reject, C: excludes device-mapper disks from a summary to avoid double counting, but never says the same I/O is on the backing device's line; omits md (SrcDmStack) |
| S204 | https://raw.githubusercontent.com/torvalds/linux/v7.2/drivers/md/dm.c | `b01ff2d6…bab8b02b` | (16) Account io->origin_bio to DM dev on behalf of target that took ownership of IO with DM_MAPIO_SUBMITTED. — `drivers/md/dm.c:1379-1380` | reject, A for its scope: accounts the original bio to the dm device and resubmits a clone (`:1386`), but does not show the backing device's diskstats line counting it (SrcDmStack) |

Also opened by SrcDmStack and rejected without a row (no stating sentence; sweep in `.ufo/waves/round-35/w1/SrcDmStack.md`):
Linux v7.2 `Documentation/admin-guide/iostats.rst`, `block/blk-core.c`, `drivers/md/dm-linear.c`,
`Documentation/admin-guide/device-mapper/statistics.rst`; sysstat v12.8.0 `man/iostat.in`, `iostat.c`, `FAQ.md`, `man/sar.in`;
util-linux v2.42.4 `misc-utils/lsblk.8.adoc`, `misc-utils/lsblk.c`; sysstat v12.8.0 `README.md`; Linux v7.2
`Documentation/admin-guide/md.rst` (logged by the sweep, counted after GateS200 and ReviewSkillCorr). Search question: does any primary source state that
I/O to a stacked block device is also accounted on its underlying devices in /proc/diskstats? Identified 14 named here (12 without a row, S203 and S204 with one), included 0; the sweep also read collectl's program and other collectl docs (`SrcDmStack.md`).
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
| 4 `SKILL.md:834` | marked observed, not sourced; seventeen files opened (fourteen named in the Gate), none states it; S203, S204 rejected | `SKILL.md` Round35 corrections |
| 5 QUALITY 98 worked example | append-only 98 correction (D1, D2, D4) | `corpus/QUALITY.md` 98 correction |
| 6 operator items | left alone: `LOG.md:1801`, `refs/jj/keep/…` `3b19cac`, SHONEN promotion | — |
| Axes table (found this round) | `Last change` for operability and depth said round 28 and round 12; the latest admitted closure grading each improved is round 31 (`MANIFEST rounds[495]`; `round-31-verifier-spotcheck.md:154-155`); cells corrected, each naming its old value | `SCORECARD.md:11-12`; `.ufo/waves/round-35/w1/AxesOracle.md` |

## Mistakes

| id | class | evidence | captured-by | fix (shown able to fail) |
|---|---|---|---|---|
| M1 | a control that met the frozen counter before data was ruled a residual instead of forcing a re-design | `.ufo/waves/round-35/evidence/c1-controls.txt` (10c CtlSkipDesign B: empty capability and what cells, `C1=met`; 9d: unbackticked dangling prose, `C1=met`); the contract's control list maps none of QUALITY 98's server-echo, observed-column-copy, no-decision or rule-changed shapes and has no denial control, which the sibling closure kaidoku round 32 (`kaidoku-shokunin/corpus/lessons/round-32-verifier-spotcheck.md:76,116`) requires of a calibration counter | QUALITY 98 (content-free shape; "a control the counter scores as met means the counter or the target is wrong") — it should have caught it, and the L1 did not apply it | QUALITY 101 and the 98 correction's last sentence; shown able to fail on this round's receipt (10c) |
| M2 | SOURCES cells edited in place, and a lesson sentence that hid it | round 34: S182 at `8d56809a`, S193 at `406d91a4`; `round-34.md:46`; the revised check lists 16 ids edited in place before round 34 (15 not superseded, plus S069) | CORPUS §SOURCES.md rule 2 and QUALITY 81 state the rule, but no check enforced it | QUALITY 102 with `.ufo/waves/round-35/check-sources-appendonly.py` (revised after wave 2): `dd76eb79 --round-base f10a320d` → `round_changed=[S182,S193]`, exit 1; at the tip with `--round-base dd76eb79` → `round_changed=[]`, exit 0; 18 ids stay listed (S069, S182, S193 superseded; 15 routed debt) |
| M3 | the SCORECARD capabilities field stayed `— none yet —` from `d677cf3` while closures admitted 18 capabilities; each round wrote its own per-round table instead | `SCORECARD.md:586-592`; `.ufo/waves/round-35/w1/RevengerNoneYet.md` | none | the round-35 register and P-C1: `count-c1.py dd76eb79` → `mismatches=23 C1=unmet` |
| M4 | the L1 ran `git add -N .` in the lane at 09:06Z, putting intent-to-add entries for every untracked file (`.scratch/`, `w2/`) in the lane git index; no commit used them | `.ufo/waves/round-35/dispatch-log.txt` (09:06Z) | the round prompt §6.4 (never `git add` in the lane) — it states the rule; nothing enforced it | none shown able to fail this round; the next helper commit's jj mutation resets the index, checked with `git status --porcelain --untracked-files=no` after it (Round mechanics below) |
| M5 | the first `## Gate` table landed at `cedb0ec4` failed QUALITY 86's own check (`malformed=2`: S203/S204 decision cells read `**reject**:`), and three counts or words were wrong (S201 quote word counts 4/4/6 for 3/3/5; "twelve" candidate files; SKILL's partition clause bound to the parent) | `.ufo/waves/round-35/w2/GateS200.md`, `GateS201.md`, `ReviewSkillCorr.md`, `CritNoHarm.md` N1 | QUALITY 86 and 90 (the L1 did not run them before landing) | revised below; QUALITY 86's awk now prints `gate_reject_rows=2 none_declared=0 malformed=0`, exit 0 |

## Revisions after wave 2 (this round's own text, old → new)

- Gate S203/S204 decision cells `**reject**: …` → `reject, C: …` / `reject, A for its scope: …` (QUALITY 86).
- Gate S201 quote word counts (4), (4), (6) → (3), (3), (5) (GateS201, GateS200).
- Sweep: the no-row list gained sysstat `README.md` and Linux `md.rst`; "Identified 12" → "Identified 14 named here";
  SKILL "twelve candidate files" → "fourteen" (ReviewSkillCorr, ReviewLessonCorr).
- SKILL Round35 correction: "a device with a parent that is not a partition" → "the device has a parent and the device
  itself is not a partition" (CritNoHarm N1).
- `check-sources-appendonly.py`: operational errors exit 2, not 1; a supersede row is reported as `superseded_by=`, no
  longer discharges the id; new `--round-base` (CritNoHarm N2, N3; MutQ102 mutant iii). QUALITY 102 rewritten to match.
- QUALITY 101/102 notes appended (MutQ101: 9d survives 101; MutQ102).

## Judges (wave 2, non-author; decision rule quoted from `.ufo/waves/round-35/evidence/c1-controls.txt`)

| item | seat | verdict |
|---|---|---|
| register rows, 18 | JudgeRowsR12, R14, R15, R16, R18, R19, R22, R24, R25, R26, R28, R31 | 18/18 `supported`; pointer relevance 18/18 `holds` |
| rule canary | JudgeCanary | the rule flags 5/5 altered rows (empty, two denials, other-round, word bag) and 0/13 unaltered; P-C1 scores the same bytes `C1=met` |
| post-data controls | CtlDenial, CtlWordBag, CtlOffTopic | each `C1=met`, exit 0: P-C1 alone does not discriminate denial, word-bag or off-topic prose |
| counter | ExecTipRerun, ExecOracleIndep | `C1=met` reproduced at `cedb0ec4` in fresh clones; an independent oracle agrees row for row |
| C1 verdict | CritC1Verdict | `fails — C1 verifies`: 10c met before data against QUALITY 98; honest stop |
| no harm | CritNoHarm | coverage, freshness, adjacency hold; depth (N1), operability (N2), calibration (N3) failed at `cedb0ec4` and were revised above |
| sources | GateS199–S203 | admit S199–S202, reject S203 (agree); GateS204 returned without a report (no verdict) |
| repairs | ReviewSkillCorr, ReviewDwrCorr, ReviewQ98Corr, ReviewAxesFix, ReviewLessonCorr | supported, with the count defects revised above |
| criteria | MutQ100, MutQ101, MutQ102 | 100: 3 killed, positive passes; 101: 10c and denial killed, 9d survives; 102: in-place edit killed, junk superseder survived the first text |
| append-only debt | ScoutAppendDebt | all 15 pre-round-34 ids are real immutable-cell changes; 5 were logged old→new in round 33 |

Residual call (3 seats) after `6d3d94b3`: ResQ102Check confirmed every number QUALITY 102 states and found the M2
count stale (15 → 16, revised above); ResNoHarmFixes found that `--round-base` missed an id changed back to its
first cells inside the round (endpoint-only `round_changed`); the checker now takes `round_changed` from every
recorded change and QUALITY 102 says so. That last fix was made after the residual seats read the tip and is not
re-judged.
- ResGateFixes: SKILL's and the outcome table's count said fourteen files opened; the sweep opened 17 (14 named in the Gate) — revised.
