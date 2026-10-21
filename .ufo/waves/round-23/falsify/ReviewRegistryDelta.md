# ReviewRegistryDelta — round-23 source-registry delta review

Seat: `MadoR22-2.ReviewRegistryDelta` (reviewer, read-only).
Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin`
Wave: `.ufo/waves/round-23` (contract `4dc80c1`, amendment `c1e8b81`, seal `22772c1`).
Scope: `corpus/SOURCES.md` registry delta only — older immutable cells, the ten new
rows S077–S086, the `used-by` old→new change, and the located-quote grounding of
those ten rows against retained and upstream source bytes.
No code, no source row, no frozen/expected/oracle byte was edited by this seat.
No host quota read, no probe/fixture/pinned-driver execution (not authorized for this item).
No installs performed (no pacman / uv / cargo / npm transaction in this seat).

Tools used: `read`, `grep`, `bash` (read-only git `show/log/status/diff/cat-file`,
`curl` for upstream re-fetch, `sha256sum`), `write` (this report only).
Scratch (helpers + upstream byte copies): `/fast/scratch/hyaku/mori-r23/ReviewRegistryDelta/`
(`TMPDIR` pointed there; no `/tmp` use).

---

## Verdict

**Conformant for the assigned registry scope**, with two LOW documentation-completeness
observations and no registry-integrity defect found. No source row edit, no older-cell
mutation, no unlogged mutable-field change, no over-long or ungrounded quote.

Every named check was executed against bytes, not narrative:

| check | result | primary evidence |
|---|---|---|
| older immutable cells untouched | PASS (0 of 76 rows changed or missing) | `git show 1bfe708:corpus/SOURCES.md` vs HEAD row-by-row byte compare |
| ten new rows scoped A | PASS (10/10 tier `A`, 11 cells each) | `corpus/SOURCES.md:83-92` |
| `used-by` old→new logged | PASS (all ten, two places) | `corpus/lessons/round-23.md:74-76`; `.ufo/waves/round-23/build/DraftSourceRows.md:233-244` |
| `used-by` resolvable | PASS (both target paths exist; each row cited by both) | file existence + literal ID counts |
| ten located quotes ≤25 words | PASS (max 12 words) | `.ufo/waves/round-23/evidence/source-quotes.json`; lesson Gate table `corpus/lessons/round-23.md:41-51` |
| quotes located in source bytes | PASS (10/10 at the stated line numbers) | `evidence/sources/S0xx-*` |
| source bytes authentic | PASS (10/10 upstream digests reproduced) | fresh `raw.githubusercontent.com/torvalds/linux/v7.2/...` fetch, 2026-10-21 |

---

## 1. Older immutable cells untouched — PASS

- `corpus/SOURCES.md` rows S001–S076 at HEAD are **byte-identical** to
  `1bfe708:corpus/SOURCES.md` (76 rows compared cell-string by cell-string;
  changed = 0, missing = 0).
- `git diff --stat 1bfe708..HEAD -- corpus/SOURCES.md` = `13 insertions(+)`, **0 deletions**.
  The 13 added lines are exactly: 10 registry rows (S077–S086), 1 `## Paths` bullet
  (`corpus/SOURCES.md:100`), 1 `Bounded search14` search-log paragraph
  (`corpus/SOURCES.md:132`), 1 blank line. No pre-existing line was rewritten.
- Contract-v1 rule 2 ("Append-only. Only `status`, `recheck` and `used-by` change in
  place, and each change is logged old→new in the round lesson",
  `/home/vgpnk/Projects/shokunin/CORPUS.md`) is respected: the only in-place field
  mutation is `used-by`, and it is logged old→new (see §3).
- No `supersedes S0NN —` prefix was required: no pre-round row (S001–S076) covers the
  quota / btrfs / xfs / mountinfo / tmpfs scope, so the ten rows are additions, not
  corrections of an existing row (checked by grepping the pre-round table).

## 2. Ten new rows scoped A — PASS

`corpus/SOURCES.md:83-92`:

| id | kind | tier | scope (cell 5) | anchor | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|
| S077 | docs | A | XFS noquota and per-scope option vocabulary, not limit values | Mount Options:171-185; tag v7.2; sha256 53bda67b5612a3f2 | mined | 2026-10-21 | on-release | lesson + knowledge |
| S078 | code | A | emitted XFS accounting/enforcement flags only | xfs_fs_show_options:238-254; … 0a95697dcfcdab8f | mined | 2026-10-21 | on-release | lesson + knowledge |
| S079 | code | A | separate qgroups enabled and mode attributes; device link names | qgroup_enabled_show:2355-2368; qgroup_mode_show:2370-2395; devices links:2155; … ce146120f29ac29c | mined | 2026-10-21 | on-release | lesson + knowledge |
| S080 | code | A | qgroups sysfs creation versus actual status flags | btrfs_read_qgroup_config:432-445,470-474,612-615; add:1032; del:620,689,1295; … 121a0af27f9553a9 | mined | 2026-10-21 | on-release | lesson + knowledge |
| S081 | code | A | btrfs per-subvolume anonymous stat device | btrfs_getattr:8245-8246; … 01a6ad07c09cd1a0 | mined | 2026-10-21 | on-release | lesson + knowledge |
| S082 | docs | A | textual mountinfo field layout only | section3.5:1965-2002, field table:1973-1983; … e760f716f8278dee | mined | 2026-10-21 | on-release | lesson + knowledge |
| S083 | docs | A | documented quota hint/replay settings, not active quota state | quota options:261-271; … 7929550fa95ed7a0 | mined | 2026-10-21 | on-release | lesson + knowledge |
| S084 | docs | A | tmpfs quota flags and four documented hardlimit names | quota table:129-145; … 5ce3dffe9323912b | mined | 2026-10-21 | on-release | lesson + knowledge |
| S085 | code | A | per-mount field assembly and path escaping | show_mountinfo:135-193, seq_path_root:151, separator:172; … fd82c0db52055ae8 | mined | 2026-10-21 | on-release | lesson + knowledge |
| S086 | code | A | active tmpfs quota token emission and default-limit initialization | shmem_show_options:4877-4894; enable initialization:5026-5038; … eb5d1e9107b287c8 | mined | 2026-10-21 | on-release | lesson + knowledge |

Tier-`A` eligibility holds under contract v1 ("A: primary or authoritative for that
scope (spec, official docs, source code …)"): all ten are kernel v7.2 primary documents
or primary source files, and each tier is scoped to its own `scope` cell. No
`community` row carries tier A, no tier inflation.

**Anchor resolution (each anchor label found in the corresponding source bytes; every
range in bounds; every embedded `sha256` prefix equals the manifest digest):**

- S077 `xfs.rst:171` = `  noquota`, `185` = "…enforced. Refer to **xfs_quota(8)**…" ✓
- S078 `xfs_super.c:238` = `if (mp->m_qflags & XFS_UQUOTA_ENFD)`, `254` = `seq_puts(m, ",noquota");` ✓
- S079 `sysfs.c:2355` = `static ssize_t qgroup_enabled_show(…)`, `2368` = `BTRFS_ATTR(qgroups, enabled, …)`, `2370` = `qgroup_mode_show`, `2395` = `BTRFS_ATTR(qgroups, mode, …)` ✓
- S080 `qgroup.c:432` = `if (!fs_info->quota_root)`, `441` = `btrfs_sysfs_add_qgroups(fs_info)`, `444` = "default this to quota off…", `470-474` status-version parse, `612-615` flag set + `BTRFS_FS_QUOTA_ENABLED`; `add:1032` and `del:620,689,1295` resolve to `btrfs_sysfs_add_qgroups` / `btrfs_sysfs_del_qgroups` call sites ✓
- S081 `inode.c:8245` = `generic_fillattr(…)`, `8246` = `stat->dev = BTRFS_I(inode)->root->anon_dev;` ✓
- S082 `proc.rst:1965` = `3.5  /proc/<pid>/mountinfo - Information about mounts`, `2002` = "Documentation/filesystems/sharedsubtree.rst" ✓
- S083 `ext4.rst:261` = `quota, noquota, grpquota, usrquota`, `271` = "…for more details (http://sourceforge.net/projects/linuxquota)." ✓
- S084 `tmpfs.rst:129` = "tmpfs also supports quota with the following mount options", `145` = "None of the quota related mount options can be set or changed on remount…" ✓
- S085 `proc_namespace.c:135` = `static int show_mountinfo(…)`, `151` = `seq_path_root(m, &mnt_path, &p->root, " \t\n\\")`, `172` = `seq_puts(m, " - ")` ✓
- S086 `shmem.c:4877` = `#ifdef CONFIG_TMPFS_QUOTA`, `4894` = `#endif`, `5026-5038` = `SHMEM_SEEN_QUOTA` block with `shmem_enable_quotas(sb, ctx->quota_types)` ✓

**`teaches` grounding spot-verified against the bytes** (contract v1 rule 1: the located
quote must ground `teaches`): S078 — `usrquota` on `XFS_UQUOTA_ENFD`, else `uqnoenforce`
on `XFS_UQUOTA_ACCT`, `noquota` only when no accounting flag (`xfs_super.c:239-254`) ✓;
S079 — `qgroup_mode_show` contains `ASSERT(btrfs_qgroup_enabled(fs_info))`, so "mode
asserts that qgroups are enabled" is literally true ✓; S080 — sysfs directory is added
at 441 while the flag is defaulted off at 444 ✓; S081 — `anon_dev` assignment ✓;
S084/S086 — exactly four documented hardlimit names (`usrquota_block_hardlimit`,
`usrquota_inode_hardlimit`, `grpquota_block_hardlimit`, `grpquota_inode_hardlimit` in
`tmpfs.rst:139-142` and `shmem.c:4464-4467`) ✓, supporting "never arbitrary suffix
matching".

## 3. `used-by` old→new logged and resolvable — PASS

- **Logged (round lesson, contract v1 rule 2), `corpus/lessons/round-23.md:74-76`:**
  "Source used-by changes (all ten S077–S086): `corpus/lessons/round-23.md` →
  `corpus/lessons/round-23.md, corpus/knowledge/quota-surface-r23.md`; mined→mined and
  on-release→on-release unchanged. The note exists and cites every source. Delta receipt
  is `build/DraftSourceRows.md` under the round23 wave directory."
- **Logged per row** in the wave receipt
  `.ufo/waves/round-23/build/DraftSourceRows.md:233-244` (before/after for S077…S086).
- **Byte-proof that only the ten `used-by` cells moved.** Current
  `corpus/SOURCES.md` sha256 = `1f49a4d8338a48f7a85c0614ab24261b5b113d858259e41c30f0f0930ff6ad09`
  = the receipt's "after". Replacing the ten appended substrings
  (` | mined | 2026-10-21 | on-release | corpus/lessons/round-23.md, corpus/knowledge/quota-surface-r23.md |`
  → `… | corpus/lessons/round-23.md |`) reproduces sha256
  `2aa5cbf1fa999cd888b81bc34dd48967e15994a9558f17e47d9793d72e2f526d` = the receipt's
  "before"; byte delta = **390 = 10 × 39**, matching the receipt. File line count 136
  before and after (no row added or removed by that edit).
- **Resolvable.** Both referenced paths exist relative to the lane root
  (`corpus/lessons/round-23.md`, `corpus/knowledge/quota-surface-r23.md`, the latter
  8142 bytes at HEAD — it grew after the 7371-byte size quoted in the receipt, when
  later rounds of the lesson were folded in). Each of S077–S086 is literally cited in
  the knowledge note (S077×3, S078×3, S079×3, S080×2, S081×1, S082×1, S083×2, S084×1,
  S085×1, S086×4) and in the lesson (S077×4, S078×1, S079×2, S080×2, S081×1, S082×1,
  S083×2, S084×2, S085×1, S086×3). The one-count citations were read in context and are
  substantive, not incidental: `quota-surface-r23.md:47` (S084/S086 tmpfs row), `:60`
  (S082/S085 mount-resolution paragraph), `:67` (S081 anonymous-device paragraph).
- **Status honesty.** `status=mined` requires being cited by ≥1 path in `used-by`
  (contract v1); both paths cite all ten rows, so `mined` is earned.
- **Whole-registry resolution sweep.** For every one of the 86 rows with
  `status=mined`, every `used-by` path exists on disk → **0 missing paths** (this is
  the check the wave receipt claims; independently reproduced).
- Knowledge note and lesson both landed in commit `c1e8b81` together with the rows, so
  no revision in this lane's history points at a not-yet-existing `used-by` target.

## 4. Ten located quotes, ≤25 words, with source bytes — PASS

`evidence/source-quotes.json` (10 records) cross-checked against
`evidence/sources-manifest.json` and the retained bytes in `evidence/sources/`:

| id | words (recomputed / recorded) | found in source bytes | quote sha256 == manifest == file | byte size == manifest |
|---|---|---|---|---|
| S077 | 11 / 11 | yes | yes | yes |
| S078 | 6 / 6 | yes | yes | yes |
| S079 | 5 / 5 | yes | yes | yes |
| S080 | 12 / 12 | yes | yes | yes |
| S081 | 3 / 3 | yes | yes | yes |
| S082 | 7 / 7 | yes | yes | yes |
| S083 | 7 / 7 | yes | yes | yes |
| S084 | 12 / 12 | yes | yes | yes |
| S085 | 4 / 4 | yes | yes | yes |
| S086 | 5 / 5 | yes | yes | yes |

Maximum quote length 12 words — under the ≤25-word limit of contract v1 rule 1, with
margin. Every quote is present in the whitespace-normalized source bytes.

**Line locations in the lesson Gate table (`corpus/lessons/round-23.md:41-51`) re-verified
against the source bytes — 10/10 quotes occur at exactly the stated lines:**

- S077 171–173 "Forcibly turns off all quota accounting and enforcement within the filesystem." ✓
- S078 253–254 `if (!(mp->m_qflags & XFS_ALL_QUOTA_ACCT)) seq_puts(m, ",noquota");` ✓
- S079 2363 `enabled = fs_info->qgroup_flags & BTRFS_QGROUP_STATUS_FLAG_ON;` ✓
- S080 444 "default this to quota off, in case no status key is found" ✓
- S081 8246 `stat->dev = BTRFS_I(inode)->root->anon_dev;` ✓
- S082 1985 "Parsers should ignore all unrecognised optional fields." ✓
- S083 262 "These options are ignored by the filesystem." ✓
- S084 132–134 "User and group quota accounting and enforcement is enabled on the mount." ✓
- S085 172 `seq_puts(m, " - ");` ✓
- S086 4878–4879 `if (sb_has_quota_active(root->d_sb, USRQUOTA)) seq_printf(seq, ",usrquota");` ✓

**Independent upstream re-open (this seat, 2026-10-21).** All ten v7.2 raw files were
re-fetched from `https://raw.githubusercontent.com/torvalds/linux/v7.2/...` and digested;
the sha256 prefixes are identical to the manifest and to the `sha256` fragment inside
each registry row's anchor cell:

`53bda67b5612a3f2` (xfs.rst) · `0a95697dcfcdab8f` (xfs_super.c) · `ce146120f29ac29c`
(sysfs.c) · `121a0af27f9553a9` (qgroup.c) · `01a6ad07c09cd1a0` (inode.c) ·
`e760f716f8278dee` (proc.rst) · `7929550fa95ed7a0` (ext4.rst) · `5ce3dffe9323912b`
(tmpfs.rst) · `fd82c0db52055ae8` (proc_namespace.c) · `eb5d1e9107b287c8` (shmem.c).

This is a non-author re-open of 10/10 rows (contract v1 rule 1 asks for a *sample*; the
wave assigned eight re-openers for the initial eight — `build/SrcXfsDoc.md`,
`SrcXfsShowargs.md`, `SrcBtrfsSysfs.md`, `SrcBtrfsQgroup.md`, `SrcBtrfsGetattr.md`,
`SrcProcMountinfo.md`, `SrcExt4Doc.md`, `SrcTmpfsDoc.md` — and this seat additionally
covers S085/S086).

## 5. Registry census invariants reproduced locally — PASS

Reproduced in Python (equivalent to the frozen census in `/home/vgpnk/Projects/shokunin/CORPUS.md`):

- rows = **86** (= 76 pre-round + 10 new; matches `evidence/source-accounting.json`
  `before_rows 76`, `after_rows 86`, `new_ids [S077…S086]`)
- malformed rows (NF ≠ 13) = **0** (all 86 rows carry exactly 11 cells)
- duplicate ids = **none**; ids contiguous S001…S086
- tier/status/kind enum violations = **none**; tier-A + `community` inflation = **none**
- mined rows with non-existent `used-by` paths = **none**
- the ten new URLs are mutually distinct and collide with no older row's URL
- the six duplicated URLs in the registry are exactly the pre-round W04 set recorded in
  `evidence/sources-start.txt` (S035/S037, S073/S076 pairs) — pre-existing debt, not
  introduced by this delta

---

## Findings by severity

### LOW-1 — Gate table carries the access date once, not per row (contract v1 rule 1, wording)
`corpus/lessons/round-23.md:41-51` — the Gate table columns are
`Row | URL | Located quote (≤25 words) | Decision / scope`. The access date appears only
in the Gate preamble ("All source rows S077–S086 opened2026-10-21", line 34-40) and in
each row's `opened` cell (`corpus/SOURCES.md`, all ten = `2026-10-21`). Rule 1 asks the
Gate to record, *for every new row*, the URL, the access date and a ≤25-word located
quote. Substance is satisfied (per-row date is in the registry itself, and this seat
re-fetched all ten on 2026-10-21), but the Gate table does not itself carry a
per-row date column. Documentation-completeness observation only; no factual defect and
no change is required to any source row.

### LOW-2 — Search-log entry compresses the PRISMA-style counts (contract v1 rule 5, wording)
`corpus/SOURCES.md:132` ("Bounded search14 — Round23 opened ten Linux v7.2 primary files
on2026-10-21, identified/screened10 and included10 scoped rows S077–S086 …") states
identified/screened/included but gives no explicit **excluded** count (it is 0 — all ten
identified rows were included) and no explicit query string / searched-location
enumeration beyond the URLs listed in the Gate; the "where searched" is the ten upstream
v7.2 raw URLs and the rejected interpretations are named as exclusion reasons, with a
stop rationale. The compressed phrasing `identified/screened10` reads as one combined
number where the prior entries (`search13`: "identified2, screened2, re-admitted1 …")
read as separate counts. Same compressed house style as the pre-existing entries, so
this is consistency-level polish, not a new deviation.

### INFO-1 — Two anchor ranges name functions whose definition starts earlier
`S078` anchor `xfs_fs_show_options:238-254` names a function defined at
`xfs_super.c:187`; `S080` anchor `btrfs_read_qgroup_config:432-445,470-474,612-615`
names a function defined at `qgroup.c:420`. The ranges are *content windows inside* those
functions (they do contain the quoted lines), not function spans; `add:1032` /
`del:620,689,1295` resolve only via `btrfs_sysfs_add_qgroups` / `btrfs_sysfs_del_qgroups`
call sites. No claim is false, but a re-checker must not read these ranges as function
boundaries (contract v1: "Never a bare homepage" — a line anchor is acceptable; the
naming is the only soft spot).

### INFO-2 — S085/S086 were added beyond the eight assigned independent re-openers
Disclosed in the search log ("Two extra code sources close escaping/tmpfs-emission
gaps"). Contract v1 rule 1 requires a non-author re-open *sample*, which the eight
re-opener reports satisfy; this seat's own 10/10 upstream re-fetch closes the digest
and quote-location gap for the two extra rows, but it is this seat's receipt, not an
independent seat's report.

### INFO-3 — Pre-existing duplicate-URL debt unchanged
Six duplicated URLs remain (W04 set in `evidence/sources-start.txt`). Out of scope for
this delta, unchanged by it, and no new row adds a duplicate.

---

## Residual risk and verification gaps

1. **The pre-append registry state is not a commit.** `used-by` old→new is provable
   only by hash reversal (verified here) plus the non-versioned wave receipt
   `build/DraftSourceRows.md`; `corpus/SOURCES.md` was committed once in this round
   (`c1e8b81`) already carrying the final ten `used-by` values. A reviewer relying on
   git history alone cannot see the "before" value.
2. **The census validator was not executed.** `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`
   is a gate and my item did not authorize running it; its checks (row count, NF,
   duplicate ids, enum/tier inflation, mined used-by existence) were reproduced
   locally in Python instead. The pre-round census receipt
   (`evidence/sources-start.txt`, exit=0) was read, not re-run.
3. **Upstream authenticity is v7.2-as-fetched-today.** The digests match the manifest,
   the retained evidence bytes and the registry anchor cells, but a future upstream tag
   mutation would change them; that is what `recheck=on-release` covers. Only
   `raw.githubusercontent.com` was consulted; no second mirror was cross-checked.
4. **Other seats' reports were not adjudicated.** The eight source re-openers'
   internal claims were checked for existence and ID mapping only; their contents were
   not re-verified line by line.
5. **No runtime side was exercised.** No quota probe, fixture, selftest or pinned
   driver was run, no quota/`quotactl`/mount/qgroup read was performed, and no
   frozen/expected/oracle byte was touched. The strict C2 red and the frozen
   `CaseEscapedSpace` contradiction (`evidence/frozen-contradiction.json`) are outside
   this seat and remain exactly as sealed.
6. **Scope of the tier judgement.** Tier `A` was checked for eligibility
   (primary kernel doc/source, scoped, non-community) and for internal consistency with
   each row's `scope`/`teaches`; it is a curation label, and this seat makes no truth
   claim about the kernel behaviour the rows teach — that claim belongs to the C2
   measure and its own falsification seats.

## Tooling record

No package was installed or updated by this seat: the task needed only read-only git,
`sha256sum`, `curl` and Python (all pre-existing). Channel/reason record: n/a.
Scratch root used: `/fast/scratch/hyaku/mori-r23/ReviewRegistryDelta/`
(`check.py`, `quotes.py`, `lesson.py`, `anchors.py`, `receipt.py`, `up/` upstream byte
copies). `TMPDIR` was set to that path for every invocation; no `/tmp` write, no
background job, no subagent dispatch (leaf seat).
