# Mo55Crit09 — C2 claim attack C: rows 17–23 vs btrfs sysfs/tmpfs sources

Seat: Mo55Crit09 (critic, leaf). Scope: attack rows 17–23 of `corpus/knowledge/disk-runway-enospc-r55.md`
against the pinned sources S538 (btrfs_super.c.v7.3), S539 (btrfs_sysfs.c.v7.3), S540 (tmpfs.rst.v7.3);
assess filesystem-specific boundaries. Non-voter: no RECHECK/ENTAIL/REPLACE/QUOTE lines emitted.

Date: 2026-10-27. Scratch: `/fast/scratch/hyaku/mori-r55/Mo55Crit09` (removed at exit; no evidence kept there per policy — all evidence is in-repo).

## Method and evidence

1. Pin verification (all match `evidence/freeze-sha256.txt`):
   - command: `cd /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/evidence/sources-r55 && sha256sum btrfs_super.c.v7.3 btrfs_sysfs.c.v7.3 tmpfs.rst.v7.3`
   - output: `6715b89d… btrfs_super.c.v7.3`, `098cb522… btrfs_sysfs.c.v7.3`, `5ce3dffe… tmpfs.rst.v7.3` — exit 0. All three equal the frozen pins.
2. Quote location: each row 17–23 quote located verbatim in its pinned source (grep + read of surrounding lines).
3. Code/doc context read in full for each claim: btrfs_super.c.v7.3:1740–1843 (statfs body), btrfs_sysfs.c.v7.3:660–679, 690–703, 741–749, 896–908, 1883–1948; tmpfs.rst.v7.3:39–108.
4. Counter state: `.ufo/waves/round-55/evidence/c2-at-data.txt` → `C2=unmet claims=23 located=23 quote_missing=0 bad_rows=0 sources=9 source_rows=ok pins=ok provenance=ok entailed=0 dissent=0 rev=f70051dd… exit=1` (0 votes at freeze; voting is En seats' job, not this critic seat).
5. Host snapshot corroboration: `.ufo/waves/round-55/evidence/host-disk-snapshot.txt` shows btrfs `metadata/total_bytes`, `metadata/bytes_used`, `system/*`, `global_rsv_size=536870912` readable under `/sys/fs/btrfs/1d02a454-c549-4a35-b567-89d60902af8e/allocation/…` — consistent with rows 18–19's published-attribute claims. Snapshot is read-only observation, not an ENOSPC reproduction (matches doc's own boundary note).

## Row-by-row attack

### Row 17 (S538, btrfs_super.c.v7.3:1797) — zero-Avail does not guarantee universal write failure
Claim: btrfs Avail of zero does not guarantee every write fails; small metadata-consuming operations can still succeed.
Strongest counterexample: the quote is a mid-comment fragment; is "Avail" here actually the statfs `f_bavail` userspace sees?
Result: counterexample fails. The comment sits inside `btrfs_statfs()` immediately above `thresh = SZ_4M` and the rule `if (!mixed && block_rsv->space_info->full && (total_free_meta < thresh || total_free_meta - thresh < block_rsv->size)) buf->f_bavail = 0;` (btrfs_super.c.v7.3:1800–1818). "Avail" = the `f_bavail` this same function reports; df's Avail column. The comment text "some operations that consume a few metadata will succeed even if the Avail is zero" (lines 1796–1798) supports the claim verbatim. Quote word count 13 (predicate 6–25). Verdict: sound; boundary correctly btrfs-specific.

### Row 18 (S539, btrfs_sysfs.c.v7.3:897–902) — per-space-type sysfs counters
Claim: btrfs exports each space type's allocated chunk total and bytes-used as separate sysfs counters, alongside pinned/reserved/may-use.
Strongest counterexample: does a "space type" sysfs node actually exist per type, and is `total_bytes` the allocated-chunk total?
Result: counterexample fails. `SPACE_INFO_ATTR(field)` (lines 741–749) generates show fns reading `sinfo->field` under `sinfo->lock`; instances at 896–908 include total_bytes, bytes_used, bytes_pinned, bytes_reserved, bytes_may_use, bytes_readonly. `btrfs_sysfs_add_space_info_type()` (1944–1956) creates per-type kobjects named by `alloc_name()` (1902–1936: data, data-reloc, metadata, metadata-treelog, metadata-remap, system, mixed) under `/sys/fs/btrfs/UUID/allocation/TYPE` (comment at 1942–1943). `total_bytes`/`bytes_used` are the space_info allocated/used figures for that type. Quote is the 6-token contiguous run at 897–902; located. Verdict: sound.

### Row 19 (S539, btrfs_sysfs.c.v7.3:678–679) — global_rsv_size published attribute
Claim: global block reserve size published as an attribute of the allocation directory, read from the reserve under its own lock.
Strongest counterexample: is the read actually under the reserve's lock, and is the attribute really under `allocation/`?
Result: counterexample fails. `global_rsv_size_show` (672–679) calls `btrfs_show_u64(&block_rsv->size, &block_rsv->lock, buf)`; `btrfs_show_u64` (660–669) takes the spinlock around `val = *value_ptr`. `BTRFS_ATTR(allocation, global_rsv_size, …)` exports it under the allocation group (registered at line 1068). Host snapshot shows `allocation/global_rsv_size=536870912` readable. Quote 8 whitespace tokens (6–25). Verdict: sound.

### Row 20 (S540, tmpfs.rst.v7.3:88–90) — tmpfs inode ceiling via mount option
Claim: a tmpfs instance carries an inode ceiling of its own, set through a mount option separate from the size limit.
Strongest counterexample: row 22 of the same table says `nr_inodes=0` removes the ceiling — so the unqualified claim "carries an inode ceiling" is falsified for `nr_inodes=0` mounts.
Result: real but non-blocking. The claim's quote ends at "The default", and the doc table (lines 85–91) lists `nr_inodes` as a distinct sizing mount option whose default is half of physical RAM pages (or lowmem pages, whichever lower). The claim is scoped to the default/mechanism reading; the same source and table carry the exception, which row 22 states explicitly. The pair (rows 20 + 22) presents the boundary completely. Severity: low wording risk, not an unsupported clause — an ENTAIL voter can hold it as the default behavior. No correction required; if the L1 wants zero ambiguity, append "by default" — cosmetic only.

### Row 21 (S540, tmpfs.rst.v7.3:100–101) — xattrs draw on the inode allowance
Claim: on a tmpfs with an inode limit, extended attributes draw on that same allowance, so inode usage can grow without any new file being created.
Strongest counterexample: does setting an xattr actually consume an inode in tmpfs, or does the doc only say "space for inodes is used up"?
Result: counterexample fails. The doc states: "If nr_inodes is not 0, that limited space for inodes is also used up by extended attributes: 'df -i''s IUsed and IUse% increase, IFree decreases." (lines 100–101). The doc's own df -i observation (IUsed increases when xattrs are added) is the direct support for "inode usage can grow without any new file being created". Claim condition "On a tmpfs with an inode limit" matches "If nr_inodes is not 0". Quote located mid-line at 100–101, 10 words. Verdict: sound.

### Row 22 (S540, tmpfs.rst.v7.3:95–97) — nr_inodes=0 removes the ceiling
Claim: setting the tmpfs inode option to zero removes the inode ceiling entirely; documentation calls it generally unwise.
Result: verbatim support at lines 95–97: "if nr_inodes=0, inodes will not be limited. It is generally unwise to mount with such options, …". Quote 15 words, located. Verdict: sound.

### Row 23 (S540, tmpfs.rst.v7.3:92–93) — default size = 50% of RAM
Claim: a tmpfs mounted without any size option may grow to half of physical memory; block runway is bounded by RAM, not a disk device.
Strongest counterexample: the doc table says the default is "half of your physical RAM without swap"; the claim omits the swap qualifier, and tmpfs blocks may be swapped out — so "bounded by RAM" is strictly incomplete.
Result: non-blocking nuance. The claim quotes the correct sizing sentence ("the default, when neither size nor nr_blocks is specified, is size=50%"). The ceiling is a size limit derived from RAM; swap affects backing store, not the default cap. The doc's Boundaries section already states "tmpfs is memory-backed and can induce memory pressure" — the entry does not claim tmpfs cannot swap. Severity: info-level wording note; no unsupported clause in the quoted claim. No correction required.

## Filesystem-specific boundary assessment (rows 17–23)

- btrfs claims (17–19) stay inside btrfs's own statfs heuristic and sysfs interface. No generalization to XFS/tmpfs. The doc's decision-table row for btrfs repeats the boundary: "do not treat zero Avail as proof every operation fails". Consistent.
- tmpfs claims (20–23) stay inside tmpfs mount-option semantics; the inode ceiling is separate from the size limit, and the xattr-inode coupling is tmpfs-specific. The doc's tmpfs decision-table row restates both. Consistent.
- No cross-filesystem contamination: XFS claims (rows 9–12) do not leak into these rows; btrfs's zero-Avail heuristic is not presented as a generic statfs behavior; tmpfs RAM-backing is not attributed to btrfs/XFS.
- No duplicate-authority problem inside rows 17–23: S538→17, S539→18–19, S540→20–23; the table overall uses 9 sources against a ≥6 floor.
- No identity/false-provenance problem: source pins verified against the freeze file; the counter's own provenance/source_rows read `ok` at data rev b8b7064c.

## Findings

- **Low** — Row 20 unqualified phrasing "carries an inode ceiling of its own" vs the `nr_inodes=0` exception (stated in row 22). Holdable as default-behavior claim; cosmetic fix only if desired. Evidence: `corpus/evidence/sources-r55/tmpfs.rst.v7.3:88-97`; `corpus/knowledge/disk-runway-enospc-r55.md` claim rows 20 and 22.
- **Info** — Row 23 omits the doc's "without swap" qualifier ("bounded by RAM rather than by a disk device"). The quoted claim itself is supported; the entry's Boundaries section already covers memory pressure/swap context. Evidence: `corpus/evidence/sources-r55/tmpfs.rst.v7.3:87-93,103`; Boundaries section of the knowledge entry.
- **None** — Rows 17, 18, 19, 21, 22: no counterexample survived local evidence; quotes located, pins correct, boundaries clean.

No kill-class defect found in rows 17–23. This seat emits no C2 vote; the ENTAIL pass/fail decision belongs to the En voters per the frozen contract.
