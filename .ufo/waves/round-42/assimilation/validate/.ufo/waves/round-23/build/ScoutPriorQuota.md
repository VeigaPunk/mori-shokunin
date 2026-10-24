# ScoutPriorQuota — prior quota evidence, C2 delta, bounded-Core wording

Authority: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/contract.md`
(frozen at lane commit `4dc80c1be48308075e83af17f15fbfe7e95e6cb8`), §C2 lines 65–150;
`PROVINCE.md:45`; `corpus/README.md:333`; `SCORECARD.md:1413-1425`; `LOG.md:1527-1535`.

Method: read-only source reading only. My item names none of the permitted live host
reads, so I ran none (`/proc/self/mountinfo`, `os.stat`, sysfs, `readlink` were **not**
touched). All host-state statements below are the frozen, L1-observed values in
`frozen/c2-expected-real.json` — not my observation. No fixtures, tests, builds,
formatters or VCS operations. This report is my only write.

Axes: (1) fidelity to prior evidence, (2) precision of the Frontier narrowing,
(3) provenance completeness at the frozen revision, (4) anti-overclaim.

---

## 1. Observed — what prior evidence actually states

| # | Location | What it says (paraphrase with quote fragments) | Provenance quality |
|---|---|---|---|
| P1 | `PROVINCE.md:45` | FR2 is a **named Frontier row**, state F2, first evidence `corpus/knowledge/audit-r11.md:218-222`; boundary: “`df` capacity percentages cannot detect quota exhaustion; observe and report only, never change quota state.” | Boundary statement only. No capability, no measurement. |
| P2 | `corpus/README.md:333` | Same row in the coverage map: “`df` capacity percentages cannot detect quota exhaustion; observe and report only, never change quota state.” | Duplicate of P1. |
| P3 | `corpus/knowledge/audit-r11.md:218-222` | “No closure is claimed for `/scratch/tmp` coverage …, operator-supplied live `MORI_*_BIN`…, **quota observability**, or universal resource thresholds. These are inherited observability/threat-model limits” (cited: `observability-census-r1.md:182-184,216-221`, `SKILL.md:147-175`). | A blanket no-closure sentence. Its three “inherited” citations do **not** themselves discuss quota (r1:182-184 = lane-silence/`/scratch` debt; r1:216-221 = `MORI_*_BIN`/environ threat model; SKILL:147-175 = Refuses/checklist/gates). So P3 is the lane’s *only* explicit “quota observability” limit statement, and it carries no measurement. |
| P4 | `corpus/knowledge/audit-r11.md:95-99`, `:168` (F13), `:216` (D21) | The **only first-hand quota event in the corpus**: flake-seat run 7 aborted with stderr `tools/mori-census.sh: line 1983: printf: write error: Disk quota exceeded`, exit 1, 44 PASS lines, no tally. Sibling runs: 9/10 green in that battery; the writer’s separate 20-run three-worker battery 20/20 green. It is “not a `grep`/SIGPIPE missing-match and is not silently discarded.” D21: “environmental failure retained… Selftest should eventually distinguish setup failure from a case result.” | Direct preserved stderr. **Which filesystem/quota caused it was never identified**, and D21 remains open. |
| P5 | `corpus/lessons/round-12.md:48` (M25) | “A setup abort never borrows a verdict code (exit 2) and is neither a case PASS nor FAIL.” Mined from F13/D21, captured-by 6. | Normative lesson, not implemented in the census harness. |
| P6 | `corpus/knowledge/observability-surfaces-r2.md:257-261`; `SKILL.md:411-413`; `tools/mori-census.sh:353-355` | “the fleet’s own reported disk failures were EDQUOT quota events that a capacity-% probe cannot see”; 85/95 are PROPOSALS; “the quota numbers are unreadable on this host”; never OR a byte floor against `df -P`. | Repeated assertion. **Origin unlocated**: the r2 pointer `(:88-94)` lands in the r2 live-receipt fence (lines 60–94 of that note) and `tools/mori-census.sh:88-94` is the `state_rounds` comment — neither contains EDQUOT text. No receipt path or count backs “the fleet’s reported disk failures.” [UNKNOWN] |
| P7 | `LOG.md:1527-1535`; `SCORECARD.md:1413-1425` | Round-23 routing: C2 adds “a read-only quota-surface probe because `df` percentages cannot see quota exhaustion (`audit-r11.md:218-222`)”, “sourced S077–S084”, target: sealed cases `capability_absent` → all match; real host exit 0 `QUOTA_DISABLED`. Targets, not results. | Declaration only. Note it cites P3 (a no-closure sentence) as the justification; the substantive blind-spot statement is P6. |
| P8 | `tools/mori-census.sh` (grep `quota`) | Quota appears **only in the comment at `:353-355`**. No quota probe, finding id, or code path exists in the census. | Observed by search. C2 is a new standalone probe, not a census change. |
| P9 | `considerthese/2026-10-19.md:19` (tracked in the lane tree) | Operator proposal: “Report the disk-quota (EDQUOT) blind spot every time; suggest a read-only journal-count signal.” | Proposal only; never acted on. C2 implements a mount/sysfs surface probe, **not** a journal-count signal; no claim should say it followed that suggestion. |

Net prior capability: **zero quota-aware measurement**. Prior evidence knows quota can
abort a write (P4) and asserts capacity-% cannot see it (P6); it never located which
filesystem, whether quota is enabled, or any limit/usage value.

## 2. Observed — what C2 adds (contract §C2, lines 65–150)

- A **new standalone read-only probe** `tools/mori-quota-surface.py` — not a census
  surface, not a cutover (line 65; CLI 73–76).
- Per-path classification **visible enabled / visible disabled / unknown**, with basis
  tokens and a mount-resolution procedure: mountinfo fields, octal escapes, longest
  mount point, last line on ties, `no_covering_mount`, `device_mismatch`, and the
  btrfs per-subvolume anonymous `st_dev` exception recorded as
  `btrfs_subvolume_skipped` (95–104).
- A fixed fstype×option decision table for xfs, btrfs (sysfs qgroups dir), ext, tmpfs,
  and `unsupported_fstype` (105–123).
- Output `mori-quota-surface-v1` with `finding_id`, `exit_code`, per-path
  `quota_state`/`enforcement`/`basis`/`device_check`/`quota_option_keys`/
  `btrfs_qgroups_mode`, `df_covers_quota: false`, fixed `limits` (124–131).
- Precedence: setup 2 `QUOTA_SETUP`; any enabled 1 `QUOTA_ENABLED`; else any unknown 2
  `QUOTA_STATE_UNKNOWN`; else 0 `QUOTA_DISABLED`; `QUOTA_ENABLED` is runway reporting,
  not failure (132–136).
- Fixed limits: no per-user/group/project limit or usage reading; no NFS/server-side or
  overlay/fuse; btrfs qgroup presence ≠ limit set; ext superblock feature unobservable;
  enable/disable/remount races not excluded (137–141).
- Measurement: sealed oracle cases (`capability_absent` before → exact match after) and
  a frozen real control (142–150). **Oracle match scope is exit, finding_id and the six
  per-path fields `(path, fstype, mount_point, quota_state, enforcement, basis)` only.**
  `device_check`, `quota_option_keys`, `btrfs_qgroups_mode`, `df_covers_quota` and
  `limits` are **not** case-oracle-asserted (only `device_check` appears in the real
  control).
- Real control (L1 observation, not mine): fleet root btrfs `/home`, disabled,
  `btrfs_qgroups_dir_absent`, `btrfs_subvolume_skipped`; `/tmp` xfs, disabled,
  `xfs_noquota_option`, `match`; exit 0 `QUOTA_DISABLED`. The frozen file also records
  that **`/dev/shm` is tmpfs `usrquota`, observed but outside the default paths**.

### What C2 does not add
No limit or usage values (P6’s “quota numbers are unreadable” remains true); no EDQUOT
detection, prediction, or attribution; no journal-count signal (P9); no NFS/overlay/fuse;
no ext superblock feature; no race exclusion; no census integration; no remediation; and
**no discharge of D21/M25** — the probe defines its own `QUOTA_SETUP`, but its exit 2 is
shared with `QUOTA_STATE_UNKNOWN`, and the census selftest harness is unchanged.

## 3. Provenance state at the frozen commit (integration blockers)

- `git show 4dc80c1:corpus/SOURCES.md` has **76 rows, S001–S076**; **S077–S084 do not
  exist**. `evidence/sources-start.txt` (measured at `1bfe708`) prints `rows 76` and six
  `W04` duplicate-URL warnings (S035, S037, S073–S076). `LOG.md:1534` records the
  round-23 start census as “rows 76”; the round-22 measured line `LOG.md:1515` also
  reads “Sources76→76”.
- `corpus/lessons/round-23.md` (the contract’s “lesson23 Gate”) does **not** exist at
  `4dc80c1`; lessons end at `round-22.md`.
- Consequence: the contract’s “sourced: S077–S084” and `SCORECARD.md:1423` are
  **forward references**. `DraftSourceRows` plans eight rows for `xfs.rst`,
  `xfs_super.c`, btrfs `sysfs.c`, btrfs `qgroup.c`, btrfs `inode.c`, `proc.rst`,
  `ext4.rst`, `tmpfs.rst` (status `queued`, used-by `—`). Until those rows are
  committed and the Gate is written, `DraftKnowledge`’s required `source:/verified-at:/
  recheck:` trio citing S077–S084 would cite nonexistent rows, and any Core text must
  not present them as admitted sources. The knowledge note should land **after** the
  rows, or cite the kernel URLs/anchor lines with an explicit `queued` status.
- `frozen/c2-expected-real.json` is dated 2026-10-21 and is L1’s host observation. It is
  the only authority for the `/dev/shm` nuance; my report repeats it as contract-frozen,
  not as my own measurement.

## 4. Exact wording — FR2 to bounded Core

Style follows existing Core precedents (“Core, bounded FR14 advance”; “Round-16 C1
advances FR11 only for the same-boot explicit window”). Append-only; do not rewrite
`FR2` history in place beyond the row text below, and never edit `audit-r11.md`.

### 4.1 Proposed PROVINCE.md Core bullet (after the **Resource runway** bullet, line 26)

```markdown
- **Quota-surface runway** — standalone read-only probe `tools/mori-quota-surface.py`
  (round-23 build; verification pending): per path, classify whether a filesystem quota
  mechanism is *visibly enabled*, *visibly disabled*, or *unknown*, from
  `/proc/self/mountinfo` super options plus `/sys/fs/btrfs/<uuid>/qgroups` presence and
  its optional `mode` text. Every verdict carries a basis token; rows record
  `device_check` where a covering mount is resolved, and a btrfs per-subvolume anonymous
  `st_dev` mismatch is recorded as `btrfs_subvolume_skipped`, not treated as failure.
  Output `mori-quota-surface-v1`; setup errors exit 2 `QUOTA_SETUP` with no partial
  verdict; `QUOTA_ENABLED` is a runway-reporting finding (`df` percentages are
  insufficient there), never a failure claim. It reads no limit or usage values,
  attributes no EDQUOT event, never calls quotactl, `btrfs qgroup`, `xfs_quota`,
  `repquota` or mount, and never changes quota state.
```

### 4.2 Proposed replacement for `PROVINCE.md:45`

```markdown
- **FR2 — Quota/EDQUOT observability** (state F2). First evidence:
  `corpus/knowledge/audit-r11.md:218-222`; quota write abort
  `corpus/knowledge/audit-r11.md:95-99,168,216`. Round 23 advances only visible
  filesystem quota enablement state to Core (bullet above); the remainder stays
  Frontier. Remainder: per-user/group/project limit and usage values,
  NFS/server-side and overlay/fuse quota, ext superblock quota-feature detection, and
  enable/disable/remount races. Boundary: visible enablement is not exhaustion — the
  probe cannot predict or attribute an EDQUOT event; `QUOTA_DISABLED` describes only
  the named paths' visible options and sysfs, not every mount on the host; quota
  configuration remains tsukuroi/operator-owned; observe and report only, never change
  quota state.
```

### 4.3 Proposed replacement for `corpus/README.md:333`

```markdown
| FR2 | Quota/EDQUOT observability | `knowledge/audit-r11.md:218-222`; `knowledge/quota-surface-r23.md` (round 23) | Round 23: per-path visible quota enablement (enabled/disabled/unknown with basis; btrfs subvolume `st_dev` skipped) is bounded Core. Limit/usage values, NFS/overlay/fuse, ext superblock feature and enable/disable/remount races stay Frontier. `df` capacity percentages cannot detect quota exhaustion; visible enablement is not exhaustion; observe and report only, never change quota state. |
```

The `knowledge/quota-surface-r23.md` link is valid only once that note lands; land the
row and note together.

### 4.4 Optional SKILL consistency sentence (`SKILL.md:411-413`)

The existing bullet remains true; append one sentence rather than editing its claims:

```markdown
  A separate read-only probe reports only visible enablement
  (`tools/mori-quota-surface.py`, round 23); it reads no numbers and detects no
  exhaustion.
```

(Leave the gate-registry row and decision table to `DraftSkillRows`.)

### 4.5 Handling of `audit-r11.md`

Keep `:218-222` byte-unchanged (it is retained historical evidence). The new Core
bullet and FR2 row supersede its *scope* by explicitly narrowing quota observability to
visible enablement; they do not claim the audit was wrong about limits/usage, NFS,
overlay/fuse, ext superblock, or races.

## 5. Wording that must not appear (overclaim fence)

| Forbidden phrasing | Why |
|---|---|
| “quota observability”, “EDQUOT observability is now implemented”, “quota exhaustion is detected/visible” | The probe classifies **visible enablement** only; limits, usage and exhaustion are unread. |
| “quota numbers/limits/usage are readable” | Contradicts `SKILL.md:413` and §C2 limits; the probe reads no numbers. |
| “no quotas on the host” / “quotas are disabled” from `QUOTA_DISABLED` | Only the named paths are classified; `/dev/shm` tmpfs `usrquota` exists outside the defaults per the frozen real control. |
| “btrfs qgroups present ⇒ quota enforced” / “⇒ a limit exists” | §C2: qgroups presence ≠ any limit set; btrfs enforcement is `unknown`. |
| “measured on every output field” | Oracle asserts exit, `finding_id`, and six per-path fields only. |
| “distinguishes setup failure from a case result” (as done) | D21/M25 target the census harness; here `QUOTA_SETUP` and `QUOTA_STATE_UNKNOWN` share exit 2 — only `finding_id` separates them. |
| “census surface”, “census cutover”, “adds a finding to the census” | The probe is standalone; census has only a comment (P8). |
| “NFS/overlay/fuse covered”, “races excluded”, “authenticated host-wide state” | Explicitly excluded by §C2 limits; mountinfo/sysfs snapshots race remount/enable/disable. |
| “the fleet's reported disk failures were EDQUOT events” as a verified count | The origin is unlocated (P6); cite it as the lane's prior narrative, not a receipt. |

## 6. Residual unknowns / spec holes handed to L1

1. **`device_check` token for non-btrfs mismatch and no-cover rows is undefined.** §C2
   names only `match` and `btrfs_subvolume_skipped`; the output schema requires the
   field. Core wording above therefore names only the two defined tokens and says
   “where a covering mount is resolved”. [INFERENCE: implementation will need a
   `mismatch`/null token — for the implementer, not for provincial text.]
2. **Nonexistent/unreadable absolute `--path` is unstated.** Only unknown args, relative
   paths, and `--fixture`+`--path` are defined as `QUOTA_SETUP` (73–75). A missing
   absolute path or an `os.stat`/`realpath` permission failure has no contract outcome;
   the real control does not exercise it.
3. **Per-path fixture validation is underspecified.** Exact top-level keys are required;
   missing `realpath`/`st_dev` per entry is not listed among setup errors.
4. **Oracle scope ≠ full output.** Cases do not assert `device_check`,
   `quota_option_keys`, `btrfs_qgroups_mode`, `df_covers_quota` or `limits`; only the
   real control names `device_check`.
5. **S077–S084 and `corpus/lessons/round-23.md` do not exist at `4dc80c1`.** Any text
   citing them is a forward reference until the Gate lands; the knowledge note must not
   open with an admitted-source trio before the rows are committed.
6. **Source-dependent table rows** (xfs `*noenforce` echo via `xfs_showargs`; tmpfs
   `_hardlimit` keys; btrfs qgroups sysfs path/mode) are contract-frozen but not yet
   re-opened in this report; `SrcXfsShowargs`, `SrcTmpfsDoc`, `SrcBtrfsSysfs`,
   `SrcBtrfsQgroup`, `SrcBtrfsGetattr`, `SrcProcMountinfo` own that verification.
   The knowledge note should cite their verdicts, not restate kernel behavior as
   self-verified.
7. **`/dev/shm` coexistence** must survive into the note and the Core wording: a default
   `QUOTA_DISABLED` run is compatible with an enabled quota mount elsewhere on the host.
8. **D21 stays open**; C2 neither reruns the r11 abort nor makes the census selftest
   classify setup aborts. No wording may imply otherwise.
