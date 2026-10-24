# ConnTsukuroi — round 23 sibling-overlap scan (connector, read-only)

Scope: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin` at HEAD `a61db549c6c425e6a865885009b278f62ae6ef0f`
(working tree also carries mid-round changes to `corpus/lessons/round-23.md` and
`tools/check-path-reconciliation.py`; neither was used as quota evidence). Terms searched:
`quota`, `qgroup`, `EDQUOT`, `quotactl`, `xfs_quota`, `repquota`, `mountinfo`, `xfs`, `btrfs`,
`sys/fs/btrfs`, `noquota`, `usrquota`, `prjquota`, `_hardlimit`. No tsukuroi file was written;
no live host read, no build/test, no git mutation.

## Verdict

1. **No production overlap with C2.** tsukuroi has no filesystem-quota tool, probe, source row
   or test. `grep -rIlE 'qgroup|EDQUOT|quotactl|xfs_quota|repquota'` over the repo excluding
   `.ufo/` and `.git/` returns **0 files**; `sys/fs/btrfs` returns **0 files**;
   `tools/tsukuroi-census.sh` contains **0** `SURFACE disk` / `df -P` references. All 24
   `tools/` entries are host/contract gates (package, systemd, boot, freshness, citation and
   edit-contract checks); none probes filesystems or quota. C2's proposed
   `tools/mori-quota-surface.py` collides with nothing.
2. **Routing is clean but not co-owned.** tsukuroi `PROVINCE.md:8-14` owns the OS substrate
   (packages, systemd, journal/boot, drivers, update safety) and owns no resource-runway
   surface. Its pressure paragraph (`PROVINCE.md:30-33`) keeps OS triage here and routes fleet
   correlation to mori; `ADJ-04` (`PROVINCE.md:49`) routes "host pressure … liveness or progress
   correlation" to mori. mori `PROVINCE.md:10` already declares "resource runway (disk on the
   fleet root and `/tmp`, memory pressure)" and `:45` declares FR2 Quota/EDQUOT observability
   with the exact boundary C2 implements ("`df` capacity percentages cannot detect quota
   exhaustion"). C2 is an extension of mori's declared surface, not an absorption of tsukuroi's.
3. **One contested seam, resolvable by tsukuroi's own rule.** C2's *inputs* are OS mount/sysfs
   facts — the same family tsukuroi reads for OS diagnosis (`corpus/knowledge/root-dac-decision-r12.md:55`
   reads `/` fstype/options with `findmnt`; `corpus/knowledge/degraded-triage-r4.md:337` reads
   the btrfs subvolume inventory). tsukuroi `PROVINCE.md:59` settles it: select the owner by
   "**the question being asked**, not the binary or service name." Runway question → mori;
   OS filesystem/boot diagnosis → tsukuroi. A mori `QUOTA_ENABLED`/`QUOTA_STATE_UNKNOWN` is a
   runway precondition, not an OS-integrity finding, and is not a tsukuroi handoff trigger
   absent an actual `EDQUOT`/`ENOSPC` event. Conversely tsukuroi mount-option findings are not
   runway grades.
4. **Two explicit contradictions, not smoothed:**
   - **Source-id collision.** The contract cites C2 as "sourced: S077–S084". In tsukuroi's
     registry those eight ids are already occupied by unrelated rows: `corpus/SOURCES.md:84-91`
     = Git `rev-parse`/`gitrevisions` manuals and self-work scope evidence; S085/S086 continue
     that registry (86 rows total). The contract also uses bare "S081" for btrfs per-subvolume
     anonymous `st_dev`; tsukuroi's S081 is the Git typed-peeling manual
     (`corpus/SOURCES.md:88`). mori's registry currently ends at S076
     (`corpus/SOURCES.md`, last row `| S076`), so mori S077–S084 are new this round. S-ids are
     lane-local and must be written lane-qualified (`mori:S081`); a bare S-id in a cross-lane
     report resolves to the wrong document.
   - **Claim-label collision.** Both lanes are running a "round 23" with claims labelled C1/C2/C3
     and different axes (tsukuroi `.ufo/waves/round-23/preregister.json:26-55`: depth,
     operability, calibration — structured-edit audit/path reconciliation; no quota claim).
     A mori report that says "C1/C2" must be lane-qualified, and tsukuroi's
     `.ufo/waves/round-12/OverlapHost.md:55` ("Neither C1 nor C2 measures … `EDQUOT`")
     is a *tsukuroi round-12* non-claim, not a routing refusal or a mori statement.
5. **Lexical collision.** In tsukuroi, "quota" predominantly means a source-row allowance or an
   unauthenticated API allowance: `LOG.md:695` ("shared unauthenticated quota"), `LOG.md:783`
   ("S046–S048 … not a quota"), `corpus/SOURCES.md` row-metadata prose. No tsukuroi use of
   "quota" means filesystem quota. Counts and claims must not be merged across meanings.
6. **Shared substrate (second-order).** The frozen real control
   (`.ufo/waves/round-23/frozen/c2-expected-real.json:34-35`) puts the fleet root on the `/home`
   btrfs mount (major:minor `0:30`, subvol `/@home`, uuid
   `1d02a454-c549-4a35-b567-89d60902af8e`), and `tsukuroi-shokunin` is a strict descendant of
   that fleet root. tsukuroi's own knowledge records the host's btrfs layout with multiple
   subvolumes (`degraded-triage-r4.md:337`: `@` 256, `@home` 257, `@log`, `@pkg`); that this is
   the same UUID as the frozen `/home` mount follows from the shared mount path and the
   single-btrfs-filesystem layout, and is `[INFERENCE]`, not a frozen-field reading. Therefore the
   frozen btrfs verdict (`btrfs_qgroups_dir_absent`) is a **filesystem-wide** observation that
   covers every sibling checkout and snapshot, not a mori-private or per-subvolume fact. mori
   must not read it as evidence about tsukuroi's OS health; tsukuroi must not read mori's probe
   output as OS diagnosis.

## Axes

Declared axes: **calibration/depth/freshness** (C1, held 5) and **capability/coverage** (C2,
held 6). This report touches **capability** (what the btrfs arm actually observes), **depth**
(the unit of the observation is made explicit and falsifiable) and **freshness/provenance**
(lane-qualified source binding). It is **neutral on calibration**: no key, value, exit code,
finding id, schema, sealed case or frozen file changes.

## Evidence (all read-only, exact anchors)

- `tsukuroi-shokunin/tools/` — 24 entries; none named or containing quota/qgroup/EDQUOT logic.
- Zero-hit sweeps above (repo excluding `.ufo/`, `.git/`).
- `tsukuroi-shokunin/PROVINCE.md:8-14,23,30-33,49,59` — owned surfaces, Snapper/rollback row
  ("Diagnose filesystem mode and unit capability restrictions"), pressure routing, ADJ-04,
  question-first handoff rule.
- `tsukuroi-shokunin/.ufo/waves/round-12/OverlapHost.md:55` — round-12 C1/C2 explicitly did not
  measure `ENOSPC`/`EDQUOT`; a scoped non-claim, not a permanent refusal.
- `tsukuroi-shokunin/corpus/SOURCES.md:84-91` — S077–S084 are Git/self-work rows;
  `:92-93` S085/S086; 86 rows total.
- `tsukuroi-shokunin/.ufo/waves/round-19/l1-capture/siblings/mori/91940fa339e3/PROVINCE.md:45`
  — tsukuroi's own capture of mori FR2, with the "observe and report only" boundary.
- `tsukuroi-shokunin/.ufo/waves/round-23/preregister.json:26-55` — concurrent tsukuroi round 23
  claims (depth/operability/calibration) contain no quota surface.
- `mori-shokunin/PROVINCE.md:10,45` — owned runway surface and FR2 boundary.
- `mori-shokunin/.ufo/waves/round-23/frozen/c2-expected-real.json:24,29,34-40` — real control,
  `/home` btrfs mount + uuid, `/tmp` xfs `noquota`, `/dev/shm` tmpfs-usrquota note, drift caveat.
- `tsukuroi-shokunin/corpus/knowledge/root-dac-decision-r12.md:55`,
  `corpus/knowledge/degraded-triage-r4.md:337` — tsukuroi mount/subvolume evidence on the same
  btrfs filesystem.

## Proposed move (one, bounded)

**Bind C2's btrfs arm to filesystem-UUID granularity and verify it with a same-UUID paired-path
observation that uses the tsukuroi checkout as the second witness — no contract edit, no frozen
oracle edit, no output-schema/key/exit change, no sealed case addition.**

The btrfs classification is derived from `/sys/fs/btrfs/<uuid>/qgroups` and
`.../qgroups/mode`, which are per-filesystem, not per-subvolume. The output's per-path rows
therefore repeat identical filesystem-level tokens for every path on one UUID; `device_check`
(the `st_dev` match/skip token) is the only per-subvolume field. Concretely, after integration:

1. **Gate annotation (L1).** Record that the btrfs verdict for uuid
   `1d02a454-c549-4a35-b567-89d60902af8e` is filesystem-wide: it covers the fleet root, every
   sibling checkout under `/home/vgpnk/Projects/shokunin`, and all subvolumes/snapshots. It is
   not a per-subvolume or per-lane finding, and it says nothing about whether a limit is set.
2. **Paired-path check (L1, read-only, label as observation, not oracle).** Run the probe with
   `--path /home/vgpnk/Projects/shokunin --path /home/vgpnk/Projects/shokunin/tsukuroi-shokunin`.
   Both are descendants of the frozen `/home` mount point and the frozen evidence names no
   nested mount in that path, so both are expected to resolve to `/home` `[INFERENCE]`.
   Expected: both rows `fstype=btrfs`,
   `mount_point=/home`, `quota_state=disabled`, `enforcement=n/a`,
   `basis=btrfs_qgroups_dir_absent`, identical `btrfs_qgroups_mode` (null); exit 0
   `QUOTA_DISABLED`. `device_check` may differ only per `st_dev`.
3. **Do not** add the sibling path to the default paths, the frozen real control, or any sealed
   case; do not change verdict precedence.

Why this is the non-obvious synthesis: the contract's per-path output shape invites reading the
two btrfs rows as independent evidence, while the substrate behind them is one UUID. The
sibling checkout is a free, legitimate second path on that UUID — it proves the invariant
without inventing a fixture and without touching tsukuroi.

## Risks

- **Frozen contract.** The annotation belongs in the round-23 Gate/lesson, not in
  `contract.md`, `frozen/c2-expected-real.json` or any sealed case. If L1 wants the probe's
  `limits` text to carry the UUID caveat, that is a post-integration docs decision; sealed
  cases assert only exit, finding id and `(path, fstype, mount_point, quota_state, enforcement,
  basis)`, so such a text addition would not affect them — but it still changes tool output and
  should be stated, not assumed.
- **Drift.** The paired run is compared to itself, not to the frozen oracle; a remount or quota
  enable between the frozen observation and the run changes both rows together and does not
  falsify the invariant. The frozen note (`c2-expected-real.json:24`) already labels host drift
  as an observation, not an oracle rewrite.
- **Inapplicability.** If a later mountinfo read shows a nested mount under the tsukuroi path,
  the paired invariant is inapplicable; report `inapplicable`, not failure. The frozen control
  names no nested mount under `/home/vgpnk/Projects/shokunin`.
- **Citation hazard.** If the Gate mints mori S077–S084 without lane qualification, a reader
  resolving S081 lands on tsukuroi's Git manual. This is a verification defect independent of
  the move; the Gate should write `mori:S077…S084` and state the mapping explicitly.
- **Concurrent sibling.** tsukuroi is mid-round with a dirty working tree; its S-rows and tools
  may advance. Re-run the zero-hit sweeps at any later routing claim. This report binds to
  `a61db549`.
- **Carried debt untouched.** No privacy clearance, retention, permission-control or baseline
  status is implied or changed here.

## Verification

- **Move check (after integration):** the paired-path command above. Falsified if the two rows
  differ in any of `fstype`, `mount_point`, `quota_state`, `enforcement`, `basis`,
  `btrfs_qgroups_mode` while both resolve to the same uuid; or if the probe reports the second
  path on a different mount without mountinfo evidence of a nested mount.
- **Routing check:** confirm mori's S077–S084 rows exist and are the quota sources; confirm the
  contract's "S081" btrfs claim maps to the mori row, not to tsukuroi `SOURCES.md:88`; grep mori
  for bare cross-lane S-id citations and qualification.
- **Overlap re-check:** the zero-hit sweeps above at the tsukuroi revision in use; if a later
  tsukuroi round adds any quota/qgroup/`sys/fs/btrfs` surface, contested scope must be re-opened
  with L1.
- **No-harm:** C1's key set, schema, exit codes and finding ids are untouched by this move; no
  frozen file, case file, tsukuroi file or implementation is edited by this seat. The only write
  is this report.

## Bounds compliance

Read-only. No installs, no builds/tests/gates, no live host probes, no `/tmp` use, no git
mutation, no delegation, no background jobs. One procedural disclosure: the first lexical sweep
was launched with the whole tsukuroi tree in its path set before the `.ufo/interactive-sessions`
exclusion was applied; it returned only a filename match and no transcript content was opened
or used as evidence. Every later sweep excluded `.ufo/` or restricted to `.ufo/waves/round-12`
and `.ufo/waves/round-19` captures.
