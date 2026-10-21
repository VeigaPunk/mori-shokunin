# DraftProvince — scoped findings report (round 23, C2 province text)

**Seat:** `MadoR22-2.DraftProvince-8` (scribe, leaf — no subagent dispatch).
**Deliverable drafted:** `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/build/DraftProvince/province.md`
**Authority:** `.ufo/waves/round-23/contract.md` §C2, frozen at lane commit
`4dc80c1be48308075e83af17f15fbfe7e95e6cb8`; scope ruling `.ufo/waves/round-23/build/CriticScopeProvince.md`;
`corpus/knowledge/audit-r11.md:216-220`; `corpus/knowledge/observability-surfaces-r2.md:255-260`;
`SKILL.md:411-413`.
**Tool installs:** none — no pacman/uv/npx/cargo transaction was run; the host-wide pacman pause was
untouched. Reason: nothing was needed (markdown drafting and read-only file reads only).
**Live host reads:** none. **Builds/tests/linters/selftests/gates:** none (not permitted in this
wave). **VCS:** read-only plumbing only; no `git add`/`commit`/`push`, no mutating `jj` command.

## Files written (this seat's only writes)

| Path | Role |
|---|---|
| `.ufo/waves/round-23/build/DraftProvince/province.md` | the draft province text (the deliverable) |
| `.ufo/waves/round-23/build/DraftProvince.md` | this report |

`PROVINCE.md`, `corpus/README.md`, `corpus/SOURCES.md`, `corpus/knowledge/**`, `SKILL.md` and
`tools/**` are byte-unchanged. No candidate implementation was read (`build/ImplQuota/`,
`.scratch/round23/ImplQuota` — neither was opened), no oracle was read, no proposed case content was
read, and no session transcript was read (this wave permits none).

## What the draft contains

Nine labelled blocks with exact, copy-pasteable text, a placement map keyed to base-revision line
numbers, an append-only fallback, wording decisions with their grounds, and open questions for L1.

| Block | Target | Kind | Content |
|---|---|---|---|
| A | `PROVINCE.md` EOF | **pure append** | `## Round-23 appended scope notes (2026-10-21)` — seven bullets: the bounded Core advance, the input fence, the no-cause/no-remediation fence, the FR2 remainder, the tsukuroi adjacency, no census cutover, measurement pending. |
| B1 | `PROVINCE.md:10` | in-place | `Owns (read-only probes)`: add "and the kernel-visible quota-mechanism state on those targets". |
| B2 | `PROVINCE.md` after line 26 | in-place insert | new `Core` bullet `**Quota-mechanism visibility (FR2 bounded advance)**`. |
| B3 | `PROVINCE.md:45` | in-place | `Frontier` FR2 row: advance sentence + `Remainder:` list + unchanged boundary + tsukuroi ownership clause. |
| B4 | `PROVINCE.md:12-15` | in-place | `Refuses` paragraph: add filesystem-quota *configuration* (mount units, fstab, Snapper/qgroup setup, superblock quota features, why on/off) as tsukuroi/operator OS state. |
| B5 | `PROVINCE.md` `## Adjacent` table | in-place insert | one mori-side `tsukuroi (quota configuration)` row. |
| C | `corpus/README.md:333` | in-place | the matching `Frontier` table FR2 row, in the README's own path convention. |
| D | `corpus/README.md` coverage map + EOF | **optional** | coverage-map row for the round-23 note and a `## Round-23 coverage additions` table (round-20 idiom). |
| — | `PROVINCE.md` EOF | **fallback** | one paragraph restating the advanced/remainder split, for a strictly append-only landing. |

## The boundary the draft encodes (what moves, what stays)

**To Core (bounded):** the *kernel-visible* quota-mechanism state per runway target — visibly
enabled / visibly disabled / unknown — read only from `/proc/self/mountinfo` super options, `stat`
device ids, `/dev/mapper` link basenames and `/sys/fs/btrfs` device/qgroups presence and mode.

**Remaining in Frontier (FR2), named explicitly in the Core row, the Frontier row, the README row
and the appended note:** per-user/group/project limits and usage and therefore any exhaustion or
EDQUOT verdict; EDQUOT event attribution; ext2/ext3/ext4 superblock quota features;
NFS/server-side and overlay/fuse quota; enable/disable/remount races between mountinfo and sysfs;
and "a qgroups directory is not a limit". `df` capacity percentages still cannot detect quota
exhaustion — that sentence is unchanged and appears in every block that touches FR2.

## Findings

1. **The scope ruling (already in wave 1) governs this text, and the draft implements its four
   corrections**: pre-registered province wording; the input list restated as a *province* fence
   (never read `/etc/fstab`, systemd `.mount` units or `systemctl`, Snapper or any quota-tool
   configuration, nor a superblock or its feature flags); non-default `--path` values declared
   operator-pinned runway targets (the `MORI_DISK_TARGETS` precedent); and no cause, attribution
   or remediation text — no configuring agent is ever named, and `enabled`/`unknown` route cause
   and configuration to tsukuroi/operator.
2. **A citation conflict between two sibling reports (verbatim).** `CriticScopeProvince.md:33`
   cites the FR2 row as `` `mori-shokunin/PROVINCE.md:46` ``; at lane HEAD `4dc80c1` the FR2 row is
   line **45** and line 46 is FR3. `build/DraftKnowledge.md` cites `PROVINCE.md:45`, agreeing with
   the tree. My draft uses 45. No wording difference — a citation offset in the critic's report.
3. **A second, corrected citation in the ruling's proposed adjacency row (verbatim).** The ruling
   proposed `../tsukuroi-shokunin/PROVINCE.md:3-4,24,41-42,59-60` for the Snapper/rollback-net
   surface. In tsukuroi's tree the Snapper row is line **23** and line 24 is blank — verified at the
   ruling's pinned commit `a61db549c6c425e6a865885009b278f62ae6ef0f` and at the current tsukuroi
   HEAD `6ecb8d2ed6f553fea0f374b4258939c707517547` (tsukuroi HEAD has moved since the pin; the
   cited lines are identical in both). B5 cites `:3-4,23,41-42,59-60`; every cited line was read.
4. **The tool does not exist at the base revision.** `tools/` at `4dc80c1` has no
   `mori-quota-surface.py`. The Core row is therefore marked *(measurement pending)* and the
   appended note states that the probe lands in the round-23 implementation commit and that L1 owns
   the measurement; the wording is provisional until then.
5. **The `QUOTA_ENABLED` verdict must not become a failure claim.** The Core row repeats the
   contract's own calibration sentence ("runway evidence that `df` percentages are insufficient
   there; it is not a fault, a limit, usage or a configuration claim"), matching the sibling
   SKILL-row draft's reasoning that rc1 is not the gate's `failed`.
6. **D21 is not discharged by this advance.** `corpus/knowledge/audit-r11.md:216` routes quota
   *diagnosis* to operator/tsukuroi; the new capability reads visibility only, so the retained
   audit-time quota abort stays an environmental failure with an undiagnosed cause. The draft says so.
7. **`/dev/shm` coexistence is not claimed away.** The frozen real control's own note records
   `/dev/shm` (tmpfs `usrquota`) as observed on this host but outside the default paths, and the
   frozen control is exit 0 `QUOTA_DISABLED` for the two default paths only. No host-wide "no
   quota" claim appears in any block.
8. **Nothing in the `Frontier` section is closed.** FR2 stays a Frontier row, re-scoped, exactly as
   FR1 (round 13/15) and FR11 (round 16) were re-scoped in place; the original first evidence
   `corpus/knowledge/audit-r11.md:218-222` is kept and the round-23 note is added beside it.
9. **Forward-reference risk in the citations.** `corpus/SOURCES.md` at `4dc80c1` ends at S076, so
   the round-23 note's S077–S084 trio is not yet admitted. The draft cites the note by name only;
   if the note does not land, the citation must be dropped rather than left dangling. L1 should
   land the source rows before the note is cited as admitted.
10. **Contested classification rows do not change this text.** The knowledge seat's §5 records
    three contested contract rows (ext `enabled` vs S083 "ignored by the filesystem"; the tmpfs
    `*_hardlimit`-only arm under-determined by S084; mount selection/overmount ordering not
    documented by S082). The province text claims *visibility*, not a per-fstype table, so a ruling
    on any of them leaves it intact.
11. **No census cutover and no baseline change.** The probe is standalone (no `SURFACE` id), so the
    `SURFACE disk` row, its thresholds and the round-21 correction (r20 baseline invalid,
    acceptance blocked) are untouched and no baseline is re-pinned.

## Out of scope / not done

- No production edit: `PROVINCE.md` and `corpus/README.md` are byte-unchanged; this seat's whole
  contribution is text for L1 to land.
- Blocks B4 and B5 exceed the literal seat wording ("FR2 → Core plus the README frontier row").
  They implement the ruling's corrections, which mark the fence wording as required. L1 may drop
  them; the same fence then lives only in B3 and Block A. Flagged in the draft's open questions.
- Not owned by this seat and therefore not drafted here: `corpus/SOURCES.md` rows S077–S084 (the
  source-row seat), `corpus/knowledge/quota-surface-r23.md` (the knowledge seat), the `SKILL.md`
  registry/decision/error rows (the skill-row seat), the round-23 lesson, the oracle, the sealed
  cases and the implementation. Block D is offered as optional because no sibling seat owns the
  README coverage-map row or a round-23 README section.
- No live host read, no host probe, no privileged command, no `quotactl`/`btrfs`/`xfs_quota`/
  `repquota`/`mount` call, no remount, no configuration change, no remediation.
- No build, test, lint, formatter, selftest, gate, oracle or probe execution — none is permitted
  in this wave, and none was attempted. The draft's wording was checked by reading, not by running.
- No session-transcript read of any kind.
- No delegation (leaf seat) and no tool install.

## Verification actually performed

`read` of `PROVINCE.md` (lines 6-15, 20-28, 42-57, 59-70, 196-209), `corpus/README.md` (1-60,
299-363, 379-426), `corpus/knowledge/audit-r11.md:209-233`,
`corpus/knowledge/observability-surfaces-r2.md:247-271`, `.ufo/waves/round-23/contract.md` (full),
`.ufo/waves/round-23/frozen/c2-expected-real.json`, `.ufo/waves/round-23/wave1-spec.json` and
`wave1-assignments.json` (seat scopes only), and the sibling reports `build/CriticScopeProvince.md`
and `build/DraftSkillRows.md`.
`git log`/`git show`/`git status`/`git rev-parse` on `mori-shokunin` and `tsukuroi-shokunin`
(read-only plumbing); the round-16 commit `114ebe5` was used as the in-place-amendment template
for a frontier→core advance, and `git show 114ebe5 -- PROVINCE.md` confirmed the precedent (an
`Owns` clause edit, a new `Core` bullet, a round note, and a re-scoped frontier row in place).
`ls tools/` confirmed the probe's absence at the base revision; `awk`/`grep` confirmed every cited
line number in both lanes' `PROVINCE.md` files.
No build, test, lint, formatter, selftest, gate or probe run.

Report: .ufo/waves/round-23/build/DraftProvince.md
