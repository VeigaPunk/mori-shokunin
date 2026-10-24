# DraftSkillRows — SKILL.md rows for the r23 quota-surface probe

Seat: `MadoR22-2.DraftSkillRows-8` (scribe)
Authority: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/contract.md`
(frozen lane commit `4dc80c1be48308075e83af17f15fbfe7e95e6cb8`), §C2 lines 65–150.
Schema authority: `/home/vgpnk/Projects/shokunin/PROTOCOL.md` §Gate standard lines 375–423.
Format authority: `SKILL.md` §Gates table lines 156–182 (8-column row shape),
§Decision table lines 11–21 (`Intent | Correct surface | Never | Expected output`),
§Error patterns lines 23–45 (`Observation | Reading`).
Tool installs: none. No tool, gate, selftest or probe was executed; no live host read
was made by this seat. Read-only: `SKILL.md`, `PROTOCOL.md`, `contract.md`,
`frozen/c2-expected-real.json`, `corpus/SOURCES.md`, `corpus/knowledge/audit-r11.md`,
`PROVINCE.md`, `.ufo/waves/round-22/build/GateRegistry.md`.

Status: **DRAFT for L1.** `tools/mori-quota-surface.py` does not exist at the entering
revision, so no row below is a measured claim. The text is written to be true of the
contract-specified tool; L1 verifies it against the landed implementation and the
sealed cases before any of it is committed to `SKILL.md`.

---

## 1. Placement and shape

`SKILL.md` ends at line 564 (the round-22 `Field caveats` paragraph). Two idioms exist
for a new registry row: the main `## Gates` table (`SKILL.md:164–182`) and a per-round
section with its own header copy (`## Round21 retained-loss observation and policy-test
registry`, `SKILL.md:517–532`; `## Round22 retention receipt reconciliation …`,
`SKILL.md:534–564`). The per-round section is the newest idiom and is what this draft
proposes.

**Ordering constraint (needs L1 + the `DraftRenameDocs` seat):** the round-22
`Field caveats` paragraph (`SKILL.md:556–564`) is the anchor for the C1 schema-v2
correction paragraph drafted by `MadoR22-2.DraftRenameDocs-8`. That correction must
stay immediately after its anchor. This section therefore goes **after** the
correction paragraph, last in the file:

```
SKILL.md:534–564   ## Round22 retention receipt reconciliation … (unchanged)
                   <DraftRenameDocs correction paragraph>   ← keeps :556–564 adjacency
                   ## Round23 quota surface probe (r23)      ← this draft, new
```

Nothing here edits `SKILL.md:556–564`, the round-22 registry row (`SKILL.md:538`), or
any other existing row.

---

## 2. Registry row (gates table)

New section header + the 8-column header copy from `SKILL.md:162`:

```markdown
## Round23 quota surface probe (r23)

| name | kind | entry | verdict map | self-test | pinned values | write scope | owner |
|---|---|---|---|---|---|---|---|
| r23 quota surface (C2) | probe (FR2 quota-visibility observation; not a gate verdict and not a quota-limit reading) — a probe under `PROTOCOL.md` §Gate standard because the tool carries no in-repo expected-value comparison of its own: it classifies observed mount/sysfs state, and the sealed-case comparison lives in `oracle-quota.py` over the frozen cases | `python3 tools/mori-quota-surface.py [--path ABS ...] [--fixture FILE] [--selftest]`; `--path` is repeatable and must be absolute; the default set is the fleet root `/home/vgpnk/Projects/shokunin` then `/tmp`; `--fixture FILE` is synthetic mode and reads no host surface; `--fixture` together with `--path` is refused | probe, not a gate: rc0 `QUOTA_DISABLED` — no probed path shows a visibly enabled quota mechanism, so `df` capacity percentages remain a sufficient runway signal there · rc1 `QUOTA_ENABLED` — at least one path shows a visibly enabled quota mechanism; a runway-reporting finding (df percentages cannot see quota exhaustion), **not** a failure claim, no severity, no DRIFT · rc2 `QUOTA_SETUP` — usage or fixture error (unknown argument, relative path, `--fixture` with `--path`, missing/extra fixture key, non-absolute fixture path, malformed `st_dev`, malformed JSON, unparseable mountinfo line): no partial verdict · rc2 `QUOTA_STATE_UNKNOWN` — at least one path's quota state could not be determined: unknown, never disabled and never zero · exit 2 carries two finding ids (`QUOTA_SETUP`, `QUOTA_STATE_UNKNOWN`), distinguished by `finding_id`, never by exit code alone; an undeclared nonzero code reads as could-not-evaluate · lane vocabulary, not the gate clean/failed classes: rc1 `QUOTA_ENABLED` is a positive visibility finding and is **not** the gate's `failed` — a quota-enabled path is not a lane defect (precedent: the r17 misroot-sweep probe's rc1 `MORI_MISROOT_CANDIDATE`, "review lead, not ownership proof"); rc2 is could-not-evaluate | `python3 tools/mori-quota-surface.py --selftest` — the actual CLI over isolated synthetic fixtures (`mori-quota-fixture-v1`), asserting the exit code and the stable finding id per case; no host reads, no network, no privileged interface; the observed tally is measured at L1 integration, not predicted here | fixture format `mori-quota-fixture-v1` (schema, `mountinfo`, `paths`, `device_links`, `btrfs_sysfs`); sealed case table `.ufo/waves/round-23/frozen/quota-cases/` (to be sealed by L1 before the implementation commit — not yet committed at draft time); real control `.ufo/waves/round-23/frozen/c2-expected-real.json` (exit 0 `QUOTA_DISABLED`; fleet root → btrfs, mount `/home`, disabled, `btrfs_qgroups_dir_absent`, `device_check btrfs_subvolume_skipped`; `/tmp` → xfs, mount `/tmp`, disabled, `xfs_noquota_option`, `device_check match`); the digests of these inputs are pinned and checked by `oracle-quota.py`, not by the probe itself | none live: read-only over `/proc/self/mountinfo`, `os.stat(path).st_dev`, `os.path.realpath(path)`, `os.path.realpath(mount_source)` basename, `/sys/fs/btrfs/*/devices/` listings, `/sys/fs/btrfs/<uuid>/qgroups` existence and its `mode` file; stdout only, one JSON object; it never calls `quotactl`, `btrfs qgroup`, `xfs_quota`, `repquota`, `mount`, writes, or any privileged or mutating interface; selftest uses isolated fixtures and no `/tmp` write | mori |
```

Companion prose (required by the precedents; one paragraph, immediately after the row):

```markdown
The probe reports whether a filesystem quota mechanism is **visibly** enabled,
visibly disabled, or unknown, per path. It is not a quota-limit reader: no
per-user, group or project limit and no usage is read, NFS/server-side and
overlay/fuse quota are outside the surface, btrfs qgroup presence is not any
limit set, and the ext superblock quota feature is unobservable without
privileged tools. `df` capacity percentages still cannot see quota exhaustion —
that is the reason this surface exists — and `df_covers_quota` is always `false`.
`QUOTA_ENABLED` at rc1 is a runway-reporting finding, never a failure claim, and
an `unknown` sibling is never hidden by an `enabled` path (positive evidence
first). sysfs/mountinfo races during enable, disable or remount are not excluded,
so a later differing run is a drift observation, not an oracle rewrite. Output
echoes only quota-related option **keys** (sorted), never option values, mount
sources, other options or file names from option values.
```

---

## 3. Decision-table row set

Insert into the `## Decision table` table (`SKILL.md:11–21`), after the existing
`Is there resource runway?` row (`SKILL.md:19`), because both rows answer a runway
question and the quota row is the correction to that row's blind spot.

```markdown
| Is a filesystem quota mechanism enabled on a path? (r23 probe) | `python3 tools/mori-quota-surface.py --path <ABS>` — read-only mountinfo super-options plus btrfs sysfs `qgroups` presence, per `contract.md` §C2; see "Round23 quota surface probe (r23)" below | calling `quotactl`, `btrfs qgroup`, `xfs_quota`, `repquota`, mounting, writing, or any privileged or mutating interface; reading per-user/group/project limits or usage; treating a btrfs `qgroups` directory as a limit set; treating `df` capacity percent as quota headroom; treating an `unknown` state as disabled | one JSON object on stdout: `schema mori-quota-surface-v1`, `finding_id`, `exit_code`, per-path `quota_state`/`enforcement`/`basis`/`device_check`/`quota_option_keys`/`btrfs_qgroups_mode`, `df_covers_quota: false`, and a fixed `limits` text |
| Did a quota limit get exhausted on a fleet path? (r23) | the r23 quota-surface probe answers only **mechanism visibility**; exhaustion itself is unmeasured because no limit or usage is read | inferring exhaustion from `df` used percent, from a btrfs chunk percent, or from the `enabled` state; reporting the `enabled` state as a failure or severity | `quota_state=enabled` says a quota mechanism is visibly enabled on that path and nothing more; the run verdict is `QUOTA_ENABLED` at rc1 — a runway-reporting finding, not a failure claim, no DRIFT, no remediation |
```

Row-shape note: the two rows keep the table's four columns and the existing
conventions — the `Never` column carries the refusal, the `Expected output` column
carries the vocabulary, and a semicolon-separated "and nothing more" clause carries
the calibration limit rather than a second table.

---

## 4. Error-pattern row set

Insert into the `## Error patterns` table (`SKILL.md:23–45`). The table's
`Observation | Reading` shape is kept; each reading names the observable, the
correct inference, and the limit it does not support.

```markdown
| `df -P` capacity percent is low on a path whose quota mechanism is enabled | capacity percentage cannot see quota exhaustion (FR2): `df` measures the filesystem's fill, not a per-id limit; the quota-surface probe reports mechanism visibility only, and no limit or usage is read — `corpus/knowledge/audit-r11.md:218-222`, `PROVINCE.md:45` |
| `quota_state=enabled` | a quota mechanism is **visibly** enabled on that path (mount option or btrfs `qgroups` directory). It is not a claim that a limit exists, that usage is near it, or that enforcement is active — enforcement is `enforced` only where the fstype makes it observable, and reads `unknown` for btrfs and ext |
| `enforcement=accounting_only` (xfs `*noenforce` keys only) | quota accounting is on without enforcement: the mechanism is enabled, but it does not block writes. Never read as "quota enforced", and never as "no quota" |
| `quota_state=unknown` (`xfs_quota_options_absent`, `ext_quota_superblock_unobservable`, `btrfs_device_unmapped`, `no_covering_mount`, `device_mismatch`, `unsupported_fstype`) | unknown, never disabled and never zero: the surface does not expose the answer. The ext superblock quota feature is unobservable without privileged tools, an NFS/overlay/fuse fstype is outside the surface, and a `btrfs_device_unmapped` case means zero or several uuids list the device — never pick one |
| `device_check=btrfs_subvolume_skipped` | expected on btrfs: a subvolume carries its own anonymous `st_dev`, so the path's major:minor differs from the mount's. This is a recorded skip, not a mismatch defect |
| `device_check` on a non-btrfs path differs from the mount's major:minor | `basis=device_mismatch`: the chosen mount does not carry this path, so the path's quota state is `unknown` — never the neighbouring mount's state |
| `basis=xfs_conflicting_quota_options` | `noquota` together with a quota key is contradictory mount state; the correct reading is `unknown`, not a guess about which option wins |
| `btrfs_qgroups_mode` present | the mode text is reported as observed; the presence of the `qgroups` directory is not any limit set, and the mode value is not a limit, a usage or an enforcement claim |
| run verdict `QUOTA_ENABLED` at rc1 | a runway-reporting finding, not a failure claim: `df` percentages are insufficient where a quota mechanism is enabled. No severity, no DRIFT, no remediation, and the positive evidence is never hidden by an `unknown` sibling path |
| rc2 with `finding_id=QUOTA_SETUP` | a setup error — usage, an unreadable or malformed fixture, or an unparseable mountinfo line. No partial verdict is emitted, and it is never read as a quota observation |
| rc2 with `finding_id=QUOTA_STATE_UNKNOWN` | could-not-evaluate for at least one path: the state is unknown, not disabled and not clean. The two rc2 finding ids share an exit code and are told apart by `finding_id`, never by the exit code alone |
```

---

## 5. Claims this draft does not make

- It does not claim the tool exists, that any case passes, or that the real control
  reproduces — `tools/mori-quota-surface.py` is absent at the entering revision and
  no sealed case has been sealed yet.
- It does not claim quota **limits**, quota **usage**, quota **exhaustion**, EDQUOT
  occurrence, or enforcement beyond what an fstype makes observable.
- It does not claim the btrfs `st_dev` anomaly is a defect — it is expected for
  subvolumes and is recorded as a skip.
- It does not close FR2: the bounded core subset is visible enablement state only;
  per-id limits/usage, NFS/overlay/fuse, races and the ext superblock feature stay
  in Frontier (the `DraftProvince` seat owns that PROVINCE edit).
- It changes no existing `SKILL.md` row, and it changes no other lane's file.

## 6. Open questions for L1

1. **Sealed case path.** The row names `.ufo/waves/round-23/frozen/quota-cases/`; the
   contract names `frozen/quota-cases/` for the oracle. If L1 seals under a different
   name, the row's pinned-values cell must be corrected before commit.
2. **Digest ownership.** The row says the input digests are pinned and checked by
   `oracle-quota.py`, not by the probe. If the landed probe also verifies digests,
   that cell must be updated rather than left overstated in either direction.
3. **Section placement.** Per-round section (proposed) vs a row appended to the main
   `## Gates` table (`SKILL.md:164–182`). Both are schema-conformant; this draft
   recommends the per-round section, matching the r21/r22 idiom.
4. **Ordering with the C1 correction paragraph.** Confirm the correction paragraph
   keeps immediate adjacency to `SKILL.md:556–564` and this section lands last.
5. **Frontmatter trigger.** `SKILL.md:3` lists trigger strings ("fleet health", "did a
   wave die", …) and carries no quota trigger. Whether a quota trigger string is added
   is a routing decision beyond this row; if L1 adds one, the same anti-trigger
   (not OS-package state, not remediation) must be preserved.
6. **Where the selftest's expected values live.** `PROTOCOL.md` §Gate standard requires
   a self-test's expected values to be committed in the owning repo and independent of
   the recomputation. The contract fixes neither the location nor the case count for
   `mori-quota-surface.py --selftest`. Two shapes fit the precedents: an in-script
   expected case table (the r13–r19 idiom, `SKILL.md:167–182`) or the frozen
   `quota-cases/` table (the r16/r17 idiom, `SKILL.md:170`, `:174`). This draft names
   neither in the self-test cell, because naming one that L1 does not land would be an
   unverifiable pointer. L1 must pick one and the row must name it.
7. **Probe vs gate, once more, in the other direction.** If L1 lands the sealed-case
   comparison *inside* the tool (the tool grading itself against committed expected
   cases rather than `oracle-quota.py` doing it), the row's `kind` cell must flip from
   `probe` to `gate`, and the verdict map must be restated in the gate's clean/failed
   vocabulary. The row as drafted is correct only while the comparison stays in the
   oracle.
