# DRAFT — round-23 province text: bounded FR2 advance (visible quota-mechanism state) to Core

**Seat:** `MadoR22-2.DraftProvince-8` (scribe, leaf — no subagent dispatch).
**Status:** **DRAFT for L1 integration. Not applied.** No file under the lane was edited by this
seat; the only writes are this file and `.ufo/waves/round-23/build/DraftProvince.md`.
**Base revision:** lane commit `4dc80c1be48308075e83af17f15fbfe7e95e6cb8` (the contract freeze
commit). Every line number below is from that revision.
**Authority:** `.ufo/waves/round-23/contract.md` §C2 (frozen before any implementation);
`.ufo/waves/round-23/build/CriticScopeProvince.md` (the scope ruling this draft implements);
`corpus/knowledge/audit-r11.md:216-220` (D21); `corpus/knowledge/observability-surfaces-r2.md:255-260`;
`SKILL.md:411-413`.
**Tool installs:** none. **Live host reads:** none (my item does not name them; the host facts below
are L1's frozen observation from `.ufo/waves/round-23/frozen/c2-expected-real.json`, not mine).
**VCS:** read-only plumbing only (`git log`/`show`/`status`/`rev-parse`); no add/commit/push.

---

## 1. The boundary this draft encodes

**Moves to Core (bounded subset).** The *kernel-visible* state of a filesystem quota mechanism on
mori's runway targets: visibly enabled / visibly disabled / unknown, per path, read only from
`/proc/self/mountinfo` super options, `stat` device ids, `/dev/mapper` link basenames and
`/sys/fs/btrfs` device/qgroups presence and mode.

**Stays in Frontier (the FR2 remainder — this is the part that must not be lost).**

| # | Remainder item | Why it cannot be in Core |
|---|---|---|
| R1 | per-user/group/project **limits and usage**, and therefore any **exhaustion / EDQUOT verdict** | the probe reads no limit or usage value; the quota numbers are unreadable on this host (`SKILL.md:411-413`) |
| R2 | **NFS/server-side** quota and **overlay/fuse** quota surfaces | not observable from the mount-option/sysfs inputs at all |
| R3 | **enable/disable/remount races** between mountinfo and sysfs | a snapshot of two sources read at two moments; no consistency claim is possible |
| R4 | the **ext2/ext3/ext4 superblock quota feature** | unobservable without privileged tools; the mount option alone is not the superblock feature |
| R5 | btrfs **qgroup presence ≠ any limit set** | a `qgroups` directory is an accounting capability, not an entitlement or an exhaustion verdict |

`df` capacity percentages still cannot detect quota exhaustion: that sentence is unchanged by this
advance and stays in both the Core row and the Frontier row.

**Adjacency ruling implemented (from `CriticScopeProvince.md`).** Filesystem quota *configuration* —
mount units, fstab, Snapper/qgroup setup, superblock quota features, and *why* a mechanism is on or
off — is host OS state owned by **tsukuroi/operator**. Mori observes the kernel-visible effect on
runway targets only, never sets, tunes or diagnoses it. This is the load-bearing fence; the probe's
input list is a *province* fence, not merely an implementation detail.

---

## 2. Placement map (base revision `4dc80c1`)

| Block | File | Location | Kind |
|---|---|---|---|
| A | `PROVINCE.md` | after line 209 (EOF) | **pure append** |
| B1 | `PROVINCE.md` | line 10 (`Owns` clause) | in-place line replacement |
| B2 | `PROVINCE.md` | insert after line 26 (`Core` list) | in-place insertion |
| B3 | `PROVINCE.md` | line 45 (`Frontier` FR2 row) | in-place line replacement |
| B4 | `PROVINCE.md` | lines 12-15 (`Refuses` paragraph) | in-place line replacement |
| B5 | `PROVINCE.md` | `## Adjacent` table (after the tsukuroi row) | in-place row insertion |
| C | `corpus/README.md` | line 333 (`Frontier` table FR2 row) | in-place line replacement |
| D | `corpus/README.md` | coverage map + EOF section | optional, see §6 |

If L1 accepts only appends, use **Block A alone** (§7 gives the fallback wording); B2/B3 are what
make the move visible in the Core list and the Frontier row, so they are the load-bearing edits.

---

## 3. Block A — `PROVINCE.md`, pure append at EOF (after line 209)

Append exactly this text at the end of `PROVINCE.md`:

```markdown

## Round-23 appended scope notes (2026-10-21)

- **Core, bounded FR2 advance (quota-mechanism visibility only):** the read-only probe
  `tools/mori-quota-surface.py` reports, per runway target, whether a filesystem quota mechanism
  is *visibly* enabled, visibly disabled or unknown. Default targets are the fleet root and
  `/tmp`; any other absolute path is an operator-pinned runway target, like `MORI_DISK_TARGETS`.
  `QUOTA_ENABLED` is runway evidence that `df` percentages are insufficient there; it is not a
  fault, a limit, a usage reading or a configuration claim, and `unknown` is never read as
  disabled.
- **Input fence (a province fence, not only a tool detail):** the probe reads only kernel-exported
  inputs — `/proc/self/mountinfo` super options, `stat` device ids, `/dev/mapper` link basenames,
  `/sys/fs/btrfs` device/qgroups presence and mode. It never reads `/etc/fstab`, systemd `.mount`
  units or `systemctl`, Snapper or any other quota-tool configuration, nor a filesystem
  superblock or its feature flags; it calls no `quotactl`, `btrfs qgroup`, `xfs_quota`,
  `repquota` or `mount` interface, mounts nothing, writes nothing and changes no quota state.
- **No cause, attribution or remediation:** mori states what is visible and stops. Why a
  mechanism is on or off, whether it should be, and any limit or usage figure are tsukuroi /
  operator questions; an `enabled` or `unknown` result is a report, not a diagnosis.
- **Still FR2 frontier:** per-user/group/project limits and usage and therefore any exhaustion or
  EDQUOT verdict; NFS/server-side and overlay/fuse quota surfaces; enable/disable/remount races
  between mountinfo and sysfs; the ext2/ext3/ext4 superblock quota feature, unobservable without
  privileged tools. A qgroups directory is not a limit. `df` capacity percentages still cannot
  detect quota exhaustion.
- **Adjacent tsukuroi, mori-side only:** tsukuroi owns the host mount/unit configuration and the
  Snapper/rollback net that can enable a quota mechanism; mori reports only kernel-visible quota
  state on runway targets and routes cause or configuration questions to tsukuroi/operator.
- **No census cutover, no baseline change:** the probe is standalone; the `SURFACE disk` runway
  row, its thresholds and the round-21 correction (r20 baseline invalid, acceptance blocked) are
  untouched, and no baseline is re-pinned.
- **Measurement pending:** `tools/mori-quota-surface.py` lands in the round-23 implementation
  commit; L1 owns the measurement and the wording above is provisional until then. No privacy
  clearance, no baseline acceptance and no frontier closure is claimed.
```

---

## 4. Block B — `PROVINCE.md`, minimal in-place replacements

### B1 — `PROVINCE.md:10` (the `Owns (read-only probes)` clause)

**Old (exact):**

```markdown
resource runway (disk on the fleet root and `/tmp`, memory pressure); lane silence grading (silent / progressing / progressing-weak).
```

**New (exact):**

```markdown
resource runway (disk on the fleet root and `/tmp`, memory pressure) and the kernel-visible quota-mechanism state on those targets; lane silence grading (silent / progressing / progressing-weak).
```

### B2 — `PROVINCE.md`, new `Core` bullet, insert after line 26 (after `Resource runway`)

```markdown
- **Quota-mechanism visibility (FR2 bounded advance)** — read-only
  `tools/mori-quota-surface.py` reports, per runway target (default the fleet root and `/tmp`;
  other absolute paths only when operator-pinned), whether a filesystem quota mechanism is
  *visibly* enabled, visibly disabled or unknown. It reads only kernel-exported
  `/proc/self/mountinfo` super options, `stat` device ids, `/dev/mapper` link basenames and
  `/sys/fs/btrfs` device/qgroups presence and mode. `QUOTA_ENABLED` is runway evidence that `df`
  percentages are insufficient there; it is not a fault, a limit, usage or a configuration claim.
  It calls no `quotactl`, `btrfs qgroup`, `xfs_quota`, `repquota` or `mount` interface, mounts
  nothing, writes nothing and changes no quota state; quota configuration and any remediation
  stay tsukuroi/operator-owned. Per-id limits and usage, EDQUOT attribution, ext superblock
  quota features, NFS/server-side and overlay/fuse quota, and enable/disable/remount races stay
  Frontier (FR2).
```

### B3 — `PROVINCE.md:45`, the `Frontier` FR2 row

**Old (exact):**

```markdown
- **FR2 — Quota/EDQUOT observability** (state F2). First evidence: `corpus/knowledge/audit-r11.md:218-222`. Boundary: `df` capacity percentages cannot detect quota exhaustion; observe and report only, never change quota state.
```

**New (exact):**

```markdown
- **FR2 — Quota/EDQUOT observability** (state F2). First evidence: `corpus/knowledge/audit-r11.md:218-222`; `corpus/knowledge/quota-surface-r23.md`. Round 23 advances only the kernel-visible quota-mechanism state to Core (`tools/mori-quota-surface.py`: per-runway-target enabled/disabled/unknown from mount super options and btrfs qgroups sysfs presence). Remainder: per-user/group/project limits and usage, EDQUOT event attribution, ext superblock quota features, NFS/server-side/overlay/fuse quota, and enable/disable/remount races. Boundary unchanged: observe and report only, never change quota state; a qgroups directory is not a limit, and `df` capacity percentages still cannot detect quota exhaustion. Cause and configuration of a quota mechanism stay tsukuroi/operator-owned.
```

### B4 — `PROVINCE.md:12-15`, the `Refuses` paragraph

**Old (exact):**

```markdown
**Refuses:** dispatch and orchestration mechanism (→ kumitate); OS package,
systemd unit, driver/firmware and boot state (→ tsukuroi) — mori reads journal
and cgroup events as fleet evidence and reports them, never owning OS state;
endpoint and model-serving health (→ kama); credential material (→ kagi).
```

**New (exact):**

```markdown
**Refuses:** dispatch and orchestration mechanism (→ kumitate); OS package,
systemd unit, driver/firmware and boot state (→ tsukuroi) — mori reads journal
and cgroup events as fleet evidence and reports them, never owning OS state;
filesystem quota *configuration* — mount units, fstab, Snapper/qgroup setup,
superblock quota features, and why a quota mechanism is on or off or whether it
should be (→ tsukuroi/operator); mori observes its kernel-visible effect on
runway targets only, never sets, tunes or diagnoses it;
endpoint and model-serving health (→ kama); credential material (→ kagi).
```

### B5 — `PROVINCE.md`, `## Adjacent` table: one new tsukuroi row (insert after the existing tsukuroi row, before `kama`)

```markdown
| tsukuroi (quota configuration) | Owns the host mount/unit configuration and the Snapper/rollback net that can enable a quota mechanism; mori reports only kernel-visible quota state on runway targets and routes cause or configuration questions to tsukuroi/operator as a report, never a diagnosis. Shared `findmnt` input is not shared ownership. | `../tsukuroi-shokunin/PROVINCE.md:3-4,23,41-42,59-60`; `../tsukuroi-shokunin/corpus/knowledge/snapper-eacces-mechanism.md:127`; `corpus/knowledge/audit-r11.md:216` |
```

---

## 5. Block C — `corpus/README.md:333`, the `Frontier` table FR2 row

**Old (exact):**

```markdown
| FR2 | Quota/EDQUOT observability | `knowledge/audit-r11.md:218-222` | `df` capacity percentages cannot detect quota exhaustion; observe and report only, never change quota state. |
```

**New (exact):**

```markdown
| FR2 | Quota/EDQUOT observability | `knowledge/audit-r11.md:218-222`; `knowledge/quota-surface-r23.md` | `df` capacity percentages cannot detect quota exhaustion; observe and report only, never change quota state. Round 23 advances only the kernel-visible quota-mechanism state to Core (`tools/mori-quota-surface.py`: per-runway-target enabled/disabled/unknown from mount super options and btrfs qgroups sysfs presence; `QUOTA_ENABLED` is runway evidence that `df` percentages are insufficient there, not a fault, limit, usage or configuration claim). Remainder: per-user/group/project limits and usage and any exhaustion/EDQUOT verdict; ext superblock quota features; NFS/server-side and overlay/fuse quota; enable/disable/remount races; a qgroups directory is not a limit. Cause and configuration of a quota mechanism stay tsukuroi/operator-owned. |
```

---

## 6. Block D — `corpus/README.md` (optional; L1's call, not in my seat scope)

The README `## Coverage map` table has no row for the round-23 note, and the README has no
round-23 section. No sibling seat owns either, so L1 may want them. Both are **optional** for the
FR2 move itself.

**D1 — coverage-map row** (insert into the `## Coverage map` table, after the
`knowledge/journal-cursor-window-r16.md` row):

```markdown
| `knowledge/quota-surface-r23.md` | the round-23 quota-surface note: the kernel-visible quota-mechanism decision table transcribed from contract §C2 (xfs/btrfs/ext/tmpfs arms, the btrfs anonymous-`st_dev` skip, `device_mismatch` kept distinct), the per-path visibility surface and its limits — no limits/usage read, no exhaustion verdict, ext superblock feature unobservable — and what `df` cannot see; source ids S077–S084 are forward references until the rows are admitted | round-23 wave, 2026-10-21; contract §C2; frozen real control `frozen/c2-expected-real.json` |
```

**D2 — appended section at EOF of `corpus/README.md`** (mirrors the round-20 idiom):

```markdown
## Round-23 coverage additions (bounded FR2 advance)

| Ground | Entry | Bounded advance |
|---|---|---|
| FR2 quota/EDQUOT observability | `knowledge/quota-surface-r23.md` | Kernel-visible quota-mechanism state per runway target (enabled/disabled/unknown) via `tools/mori-quota-surface.py`; a probe, not a census surface. Limits and usage, exhaustion verdicts, ext superblock features, NFS/overlay/fuse and enable/disable races stay frontier. |
```

---

## 7. Append-only fallback (if L1 accepts no in-place edits)

If L1 refuses every in-place edit (B1–B5, C), append this one paragraph to `PROVINCE.md` at EOF,
immediately after Block A. It carries the same meaning: the Core entry, the Frontier remainder and
the two fences, so nothing about the advance is lost by the move.

```markdown
- **FR2 row, superseded reading (round 23):** the `FR2 — Quota/EDQUOT observability` Frontier row
  above is read with this advance: the kernel-visible quota-mechanism state (per runway target:
  enabled / disabled / unknown) is Core via `tools/mori-quota-surface.py`; the remainder stays
  Frontier — per-user/group/project limits and usage and any exhaustion/EDQUOT verdict, ext
  superblock quota features, NFS/server-side and overlay/fuse quota, enable/disable/remount races
  — and the row's boundary is unchanged (observe and report only, never change quota state; a
  qgroups directory is not a limit; `df` capacity percentages still cannot detect quota
  exhaustion). Cause and configuration of a quota mechanism stay tsukuroi/operator-owned, and
  non-default `--path` values are operator-pinned runway targets only.
```

---

## 8. Wording decisions and their grounds

1. **"Visibility", never "quota state" as an absolute.** The row says *kernel-visible* /
   *visibly*, because the probe reports what the kernel exports, not what is configured. The
   critic's ruling requires exactly this (`CriticScopeProvince.md` CX2/CX3, corrections 2–4).
2. **The input list is repeated as a province fence.** `CriticScopeProvince.md` correction 2
   states the fence must be in the *docs*, not only in the tool. The named exclusions are
   `/etc/fstab`, systemd `.mount` units, `systemctl`, Snapper or any other quota-tool
   configuration, and filesystem superblocks or feature flags — the surfaces tsukuroi owns.
3. **No agent is named as a cause.** No `Snapper`, `systemd` unit, `fstab` or installer is named
   as the reason a mechanism is on or off, and nothing suggests enabling or disabling quota
   (correction 4). `enabled`/`unknown` route cause and configuration to tsukuroi/operator.
4. **Non-default paths are operator-pinned.** Correction 3: `--path` values other than the fleet
   root and `/tmp` are operator-pinned runway targets, the `MORI_DISK_TARGETS` precedent
   (`corpus/knowledge/observability-surfaces-r2.md:249,262-264`); the probe states visibility for
   them and interpreting them is the operator's call.
5. **`QUOTA_ENABLED` keeps the contract's own calibration sentence** (contract §C2: "a
   runway-reporting finding …, not a failure claim"). The Core row repeats it, so a later reader
   cannot promote it into a fleet-failure claim.
6. **`unknown` is never `disabled`** — the standing lane rule (`SKILL.md:151`, "a missing surface
   is reported as `unavailable`, never as unhealthy").
7. **The FR2 row is replaced, not deleted** — the `first evidence` cell keeps
   `audit-r11.md:218-222` and adds the round-23 note, so the original first evidence stays
   visible. The row stays *in* the Frontier section; only its tail is re-scoped, exactly as the
   FR1 (round 13/15) and FR11 (round 16) rows were re-scoped in place.
8. **D21 is not discharged.** `corpus/knowledge/audit-r11.md:216` routes quota *diagnosis* to
   operator/tsukuroi. The new capability reads visibility only, so the audit-time quota abort
   remains an environmental failure with an undiagnosed cause.
9. **`/dev/shm` coexistence is not claimed away.** The frozen real control's own note records
   `/dev/shm` (tmpfs `usrquota`) as observed on this host but outside the default paths; the
   frozen control is exit 0 `QUOTA_DISABLED` for the two default paths only. The Core row
   therefore claims no host-wide "no quota" state.
10. **No census cutover.** The probe is standalone (no `SURFACE` id), so the `SURFACE disk` row,
    its thresholds and the blocked r20 baseline are untouched and no baseline is re-pinned.
11. **One citation corrected against the tree.** The ruling's proposed adjacency row cited
    `../tsukuroi-shokunin/PROVINCE.md:…24…` for the Snapper/rollback-net surface. In tsukuroi's
    tree that row is line **23** and line 24 is blank — verified both at the ruling's pinned
    commit `a61db549c6c425e6a865885009b278f62ae6ef0f` and at the current tsukuroi HEAD
    `6ecb8d2ed6f553fea0f374b4258939c707517547`. B5 cites `:3-4,23,41-42,59-60`; each of those was
    read and confirmed. (tsukuroi HEAD has moved since the ruling's pin; the cited lines are
    identical in both revisions.)

---

## 9. Open questions routed to L1

1. **Note filename.** This draft cites `corpus/knowledge/quota-surface-r23.md` (the knowledge
   seat's draft name). If L1 lands it under another name, substitute it in B3 and C; if it does
   not land, drop that citation and keep `audit-r11.md:218-222` alone.
2. **S077–S084 are forward references.** At `4dc80c1`, `corpus/SOURCES.md` ends at S076, so the
   round-23 note's source trio is not yet admitted. Land the source rows (the source-row seat's
   draft) before the note is cited as an admitted knowledge entry, or the citation is a
   false-provenance risk.
3. **Contested classification rows** (the knowledge seat's §5): the ext `enabled` row against
   S083 ("ignored by the filesystem"), the tmpfs `*_hardlimit`-only arm under-determined by S084,
   and mount selection/overmount ordering not documented by S082. If L1 rules any of them
   differently, the *classification* changes but **this province text does not** — the Core row
   claims visibility, not a per-fstype table.
4. **Blocks B4 and B5 exceed my literal seat scope** ("FR2 → Core plus the README frontier
   row"). They implement the critic's corrections 1–4, which the ruling marks as required
   wording for the province. L1 may drop them; if dropped, the "quota configuration is host OS
   state" fence lives only in the Frontier row (B3) and the appended note (Block A).
5. **Placement of the `Owns` clause (B1).** Round 16 amended the same paragraph for the
   same-boot journal window; this follows that precedent. If L1 prefers a smaller `Owns` edit,
   the alternative is to leave line 10 unchanged — the Core row and the Frontier row already
   carry the surface.
6. **Whether the probe should ever join the census.** Not claimed here; a census surface would
   change the `SURFACE disk` row and the pinned baseline, which this wave does not touch.

---

## 10. Verification actually performed

Read-only: `read` of `PROVINCE.md` (lines 6-15, 20-28, 42-57, 59-70, 196-209), `corpus/README.md`
(lines 1-60, 299-363, 379-426), `corpus/knowledge/audit-r11.md:209-233`,
`corpus/knowledge/observability-surfaces-r2.md:247-271`, `corpus/knowledge/quota-surface-r23.md`'s
sibling draft report, `.ufo/waves/round-23/contract.md` (full),
`.ufo/waves/round-23/frozen/c2-expected-real.json`, `.ufo/waves/round-23/wave1-spec.json` and
`wave1-assignments.json` (seat scopes), and the sibling reports
`build/CriticScopeProvince.md` and `build/DraftSkillRows.md`.
`git log`/`git show`/`git status`/`git rev-parse` on `/home/vgpnk/Projects/shokunin/mori-shokunin`
(read-only plumbing; the round-16 commit `114ebe5` was used as the in-place-amendment template).
`ls` of `tools/` (confirms `tools/mori-quota-surface.py` is **absent** at the base revision, which
is why the Core row is marked *measurement pending*).
**No** build, test, lint, formatter, selftest, gate or probe run — none is permitted in this wave.
**No** live host read. **No** VCS mutation. **No** tool install.
