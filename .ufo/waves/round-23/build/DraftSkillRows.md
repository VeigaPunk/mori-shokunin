# DraftSkillRows — scoped findings report

Seat: `MadoR22-2.DraftSkillRows-8` (scribe)
Deliverable drafted: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/build/DraftSkillRows/skill-rows.md`
Authority: `.ufo/waves/round-23/contract.md` (frozen lane commit `4dc80c1be48308075e83af17f15fbfe7e95e6cb8`) §C2 lines 65–150;
schema authority `/home/vgpnk/Projects/shokunin/PROTOCOL.md` §Gate standard lines 375–423;
format authority `SKILL.md` lines 11–21 (decision table), 23–45 (error patterns), 156–182 (gates registry),
534–564 (round-22 section / `Field caveats` anchor), 3 (frontmatter triggers).
Tool installs: **none**. No tool, gate, selftest, probe or fixture was executed by this seat.
No live host read was made. No VCS mutation. No file outside my two assigned paths was written.

## What was produced

One draft file, `build/DraftSkillRows/skill-rows.md`, containing three SKILL.md-shaped blocks plus the
placement, scope and open-question notes:

1. **Registry row** — an 8-column gates-table row (`name | kind | entry | verdict map | self-test |
   pinned values | write scope | owner`) for `r23 quota surface (C2)`, plus a one-paragraph companion
   prose block, placed in a proposed new per-round section `## Round23 quota surface probe (r23)`.
2. **Decision-table row set** — two rows in the `Intent | Correct surface | Never | Expected output`
   shape, proposed for insertion after `SKILL.md:19` (the `Is there resource runway?` row, which the
   quota row corrects).
3. **Error-pattern row set** — eleven rows in the `Observation | Reading` shape, proposed for
   insertion into the `## Error patterns` table.

Markdown table shapes were checked programmatically: the registry block renders 10 pipe-delimited
cells per line (8 columns + 2 empty edges), the decision block 6 (4 columns + 2), the error block 4
(2 columns + 2). No `|` appears unescaped inside a cell.

## Findings that shaped the row

**Probe, not gate.** `PROTOCOL.md:377–380` defines a gate as a script that "compares them against
expected values persisted in its own repo"; a tool that cannot fail is a probe. `mori-quota-surface.py`
carries no in-repo expected-value comparison of its own — it classifies observed mountinfo/sysfs
state, and the sealed-case comparison lives in `oracle-quota.py` over the frozen cases
(`contract.md:142–146`). The row is therefore registered as `probe`, and the `kind` cell states the
reason inline so a later reader does not have to re-derive it. The contract itself calls the tool
"a new read-only probe" (`contract.md:67`).

**The 0/1/2 map cannot be the gate's clean/failed vocabulary.** `PROTOCOL.md:379` maps 0 to clean
and 1 to failed fleet-wide. Here rc1 is `QUOTA_ENABLED`, which `contract.md:134–135` calls "a
runway-reporting finding … not a failure claim" — a quota-enabled path is not a lane defect.
Registering rc1 as the gate's `failed` would convert a visibility observation into a fleet-failure
claim. The row therefore uses the lane's own vocabulary (the r17 misroot-sweep probe's rc1
`MORI_MISROOT_CANDIDATE`, "review lead, not ownership proof", `SKILL.md:176`) and says explicitly
that rc1 is not the gate's `failed`.

**Exit 2 carries two finding ids.** `QUOTA_SETUP` (setup error, no partial verdict) and
`QUOTA_STATE_UNKNOWN` (a path's state is undeterminable) share exit code 2 under
`contract.md:132–134`. The verdict-map cell says they are told apart by `finding_id`, never by the
exit code alone, and that an undeclared nonzero code reads as could-not-evaluate
(`PROTOCOL.md:380`).

**Write scope is none, and the refusals are named in the cell.** The contract's real-mode input
list (`contract.md:77–80`) is reproduced as the read set, and the row states that the tool never
calls `quotactl`, `btrfs qgroup`, `xfs_quota`, `repquota`, `mount`, writes, or any privileged or
mutating interface (`contract.md:70–71`). The write-scope cell says "none live" and stdout-only,
matching the `journal window (r16)` probe's write-scope idiom (`SKILL.md:172`).

**The btrfs `st_dev` anomaly is a recorded skip, not a defect.** `contract.md:100–103` and S081
(`btrfs_getattr` sets `stat->dev = root->anon_dev`) mean a btrfs subvolume's `st_dev` differs from
the mount's major:minor by design. The error-pattern set says so in its own row
(`device_check=btrfs_subvolume_skipped`), and separately keeps the non-btrfs `device_mismatch` case
distinct, so the two are never conflated.

**`unknown` is never `disabled`.** Every basis that yields `unknown`
(`xfs_quota_options_absent`, `ext_quota_superblock_unobservable`, `btrfs_device_unmapped`,
`no_covering_mount`, `device_mismatch`, `unsupported_fstype`) has its own error-pattern row stating
that unknown is never disabled and never zero — the lane's standing calibration rule
(`SKILL.md:151`, "A missing surface is reported as `unavailable`, never as unhealthy").

**`df` blindness is the reason the surface exists, and the row says so.** `SKILL.md:411–413` records
that the fleet's actually-reported disk failures are quota events that a capacity-percent probe
cannot see. The decision-table row set carries the correction as a second row (exhaustion itself is
unmeasured because no limit or usage is read), and the companion prose fixes `df_covers_quota` at
`false`.

## Placement and ordering (needs L1)

`SKILL.md` ends at line 564. Two placement idioms exist — the main `## Gates` table
(`SKILL.md:164–182`) and a per-round section with its own header copy
(`SKILL.md:517–532`, `SKILL.md:534–564`). The per-round section is the newest idiom and is what the
draft proposes; it is also the only placement that leaves the existing 8-column header intact.

Ordering constraint with the C1 correction: `MadoR22-2.DraftRenameDocs-8` has drafted an
append-only correction paragraph whose anchor is the round-22 `Field caveats` paragraph
(`SKILL.md:556–564`). That paragraph must stay immediately adjacent to its anchor, so the new
round-23 section goes **last** — after the correction paragraph, at EOF. The two blocks do not
overlap: the correction is a plain paragraph, the round-23 block is a heading plus a registry table.
No existing row is edited by either block.

## Scope boundary — what this draft does not claim

- It does not claim the tool exists or that any case passes: `tools/mori-quota-surface.py` is absent
  at the entering revision, and the sealed case table is not yet committed.
- It does not claim quota **limits**, **usage**, **exhaustion**, EDQUOT occurrence, or enforcement
  beyond what an fstype makes observable. The error-pattern set says so per row.
- It does not close FR2. The bounded core subset is visible enablement state only; per-id
  limits/usage, NFS/overlay/fuse, enable/disable/remount races and the ext superblock feature stay
  in Frontier (the `DraftProvince` seat owns that PROVINCE edit).
- It changes no existing `SKILL.md` row and no other lane's file.

## Open questions routed to L1

1. Sealed-case path: the row names `.ufo/waves/round-23/frozen/quota-cases/`; the contract writes
   `frozen/quota-cases/` for the oracle. If L1 seals under another name, the pinned-values cell must
   be corrected before commit.
2. Digest ownership: the row says the input digests are pinned and checked by `oracle-quota.py`, not
   by the probe. If the landed probe also verifies digests, that cell must change rather than stay
   overstated in either direction.
3. Placement: per-round section (proposed) vs a row appended to the main `## Gates` table. Both are
   schema-conformant.
4. Ordering with the C1 correction paragraph (above).
5. Frontmatter trigger: `SKILL.md:3` carries no quota trigger string. Whether one is added is a
   routing decision beyond this row; if added, the anti-trigger (not OS-package state, not
   remediation) must be preserved.
6. Where the selftest's expected values live. `PROTOCOL.md:391–394` requires them to be committed
   in the owning repo and independent of the recomputation; the contract fixes neither the location
   nor the case count for `--selftest`. The self-test cell therefore names neither the in-script
   expected-case-table idiom (r13–r19, `SKILL.md:167–182`) nor the frozen `quota-cases/` idiom
   (r16/r17, `SKILL.md:170`, `:174`) — naming one L1 does not land would be an unverifiable
   pointer. L1 must pick and the row must name it.
7. Probe vs gate, the other direction: if the sealed-case comparison lands **inside** the tool
   rather than in `oracle-quota.py`, the `kind` cell must flip to `gate` and the verdict map must be
   restated in the gate's clean/failed vocabulary. The row as drafted is correct only while the
   comparison stays in the oracle.

## Coordination

- `MadoR22-2.DraftRenameDocs-8` notified this seat that its correction paragraph is destined for
  EOF and does not touch the round-22 registry row. Placement here is chosen to stay disjoint
  (correction paragraph first, new section last); no reply was needed.
- `MadoR22-2.SimplifyRules.md` (same wave, same contract §C2 table) was read for the classification
  row order and its XFS R3-before-R5 precedence note; the error-pattern rows here were written to
  agree with it (no row asserts an outcome the simplification shows is order-dependent).

## Verification actually performed

Read-only file reads and text processing only:
`read` of `SKILL.md` (sections 1–24, 129–182, 380–460, 461–564), `PROTOCOL.md:375–430`,
`contract.md` (full, with line numbers for §C2), `frozen/c2-expected-real.json`,
`corpus/SOURCES.md` (header + S059–S076 rows), `corpus/knowledge/audit-r11.md:216–224`,
`PROVINCE.md:44–46`, `corpus/README.md:333`, `.ufo/waves/round-23/build/SimplifyRules.md`,
`.ufo/waves/round-23/build/swarm-registry.json`, `.ufo/waves/round-23/wave1-assignments.json`,
`.ufo/waves/round-23/wave1-spec.json` (the DraftSkillRows / DraftKnowledge / DraftProvince item
prompts), `.ufo/waves/round-22/build/GateRegistry.md` (registry conventions).
A pipe-count check over the three markdown blocks in the draft (result in the deliverable above).
No build, test, lint, selftest, gate or probe run — none is permitted in this wave, and none was
attempted.
