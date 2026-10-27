# Mo55Crit11 — C2 axis and no-harm review (mori round 55, wave w1)

Seat: Mo55Crit11 (leaf critic; no dispatch; non-voter — this report carries no C1/C2 vote lines).
Scope assigned: does C2 move depth rather than coverage/operability; is any axis harmed; is the healthy
host snapshot anywhere treated as a live ENOSPC event.
Measured revision: `b8b7064c2b54c8b6b22c288232a96c43fae1af47` (data commit per assignment). Worktree HEAD is
`b8a70adf` ("publish w1 ready marker"); `git diff b8b7064c..HEAD --stat` touches only
`.ufo/waves/round-55/{w1-dispatch.json,w1-input.json,w1-plan.json,w1.ready}` — the C2 entry and its sources
are byte-identical at both revisions, so worktree reads equal the frozen rev.

## Commands run (first-hand evidence)

1. `python3 .ufo/waves/round-55/count-c2.py b8b7064c2b54c8b6b22c288232a96c43fae1af47` →
   `C2=unmet claims=23 located=23 quote_missing=0 bad_rows=0 sources=9 source_rows=ok pins=ok provenance=ok entailed=0 dissent=0 rev=b8b7064c... failed=entailment` exit 1.
   Mechanical arm (header, 23 unique claims, quote location in committed copies, 9 sources, source rows,
   pins, provenance) fully passes at the measured rev; only the vote arm is outstanding, which is what w1
   seats supply.
2. `python3 .ufo/waves/round-55/count-c1.py b8b7064c2b54c8b6b22c288232a96c43fae1af47` →
   `C1=unmet scope=78 rows=78 matched=78 status_ok=78 line_ok=78 source_rows=ok pins=ok provenance=ok same=69 moved=7 changed=2 broken=0 holds=78 stale=0 voted=0 dissent=0 failed=votes` exit 1.
   Frozen counter distribution (69 same / 7 moved / 2 changed) reproduced exactly; only votes outstanding.
   C1 and C2 fail on disjoint arms with disjoint voter sets (Rc01–16 vs En01–12) and disjoint S-id ranges
   (S526–S534 vs S535–S543) — no structural interference between the two claims.
3. `sha256sum` of the nine pinned copies equals the hashes embedded in `corpus/SOURCES.md` rows S535–S543
   (lines 315–323) and the counter reports `pins=ok`: errno-base.h.v7.3 `2c148e92…`, statfs.c.v7.3
   `34e684be…`, xfs_super.c.v7.3 `0f806bf4…`, btrfs_super.c.v7.3 `6715b89d…`, btrfs_sysfs.c.v7.3
   `098cb522…`, tmpfs.rst.v7.3 `5ce3dffe…`, statfs.2 `3dc4ed70…`, statvfs.3 `5f65e9ce…`,
   coreutils.texi.v9.12 `e6521c9b…`.
4. Quote spot-checks against pinned copies (strongest claims first):
   - btrfs 4M threshold + "succeed even if the Avail is zero": `btrfs_super.c.v7.3:1788-1798`
     (`thresh = SZ_4M` at :1800) — claims "small metadata-consuming operations can still succeed" and the
     "4M threshold / ~2M observed" wording are faithful to the comment.
   - btrfs global reserve: `btrfs_super.c.v7.3` `f_bfree -= block_rsv->size >> bits` under
     "Account global block reserve as used" — faithful.
   - XFS: `xfs_super.c.v7.3:918-920` (`max(0LL, fdblocks - xfs_freecounter_unavailable(...))`),
     :949-961 (fakeinos, maxicount cap), :999-1002 (`st->f_bavail = st->f_bfree; return 0;`) — faithful.
   - VFS zero-fill ordering: `statfs.c.v7.3:58-69` (`statfs_by_dentry`: memset at :62 precedes the
     `s_op->statfs` call at :65; frsize backfill at :67) — the "before the filesystem's own statfs handler
     runs" claim is supported by the code order.
   - tmpfs: `tmpfs.rst.v7.3:83-101` (nr_inodes ceiling, default half of RAM pages; xattr consumption at
     :100-101), :92 (default size=50%), :94-98 (nr_inodes=0 unwise) — faithful.
   - statvfs(3): `statvfs.3.man-pages-6.19:227-234` — "f_favail is always the same as f_ffree … no way
     for a filesystem to report otherwise … no filesystems with an inode root reservation exist" — the two
     S542 claims attribute this to the manual and do not generalize beyond it.
   - statfs(2) fields :43-46, errno-base.h :32, coreutils.texi :11950/:12262, btrfs_sysfs.c :672-679 and
     :896-904 — all located as the counter reports (`located=23`).
5. `grep -c "f_files\|f_ffree" corpus/evidence/sources-r55/btrfs_super.c.v7.3` → 0 (grep exit 1, no refs):
   btrfs's statfs handler (`btrfs_statfs` at :1720) never assigns f_files/f_ffree, so with the VFS memset
   (:62) the host's zero btrfs inode counts follow. The entry's decision-table interpretation "btrfs does
   not supply a fixed inode capacity … zero is not evidence of inode exhaustion" — its one interpretation
   not backed by a dedicated sourced claim row — is derivable from two pinned claims (S536 zero-fill +
   S538 code).

## Axis analysis — C2 moves depth, not coverage/operability

- Contract routing is explicit and frozen: `contract.md:8` (depth/freshness/calibration tied at 5 are the
  lowest axes; two claims on distinct lowest axes) and `contract.md:29` ("## C2 — depth: ENOSPC runway is
  not just the filesystem's block column"). Attribution is not seat-disputable this round.
- Content matches the depth pattern fixed in this lane's scorecard: depth moves are "source-linked knowledge
  entries with `source:`/`verified-at:`/`recheck:` lines" (`SCORECARD.md:12`), and the last three rounds of
  this exact claim family were graded depth: r49 (C2 re-measured 21/21), r50 (22/22), and r54's
  "new ground, knowledge only" memory-failure entry — `corpus/lessons/round-54-verifier-spotcheck.md:159`
  grades "depth | improved" while `:160-161` grade "coverage | unchanged | not claimed; no tool or
  capability row" and "operability | unchanged". The r55 entry is the same shape one row larger (23 claims).
- It is not a coverage move: coverage in this lane is breadth of *measured surfaces* (silence roster,
  census probes, watch receipts — `SCORECARD.md:10`); C2 adds no surface and no tool; the corpus README
  registers it under "Round-55 knowledge additions" (`corpus/README.md:792`) with the bounded advance
  "no live ENOSPC reproduction or tool", and the registry's section header is not an axis verdict (r54's
  identically-shaped "coverage additions"-registered entry graded coverage unchanged, spot-check :160).
- It is not an operability move: no harness, probe, or automation is landed; the decision table's third
  column gives read-only "next observation" guidance (interpretive), consistent with the lane's
  detection/report-only province. `SCORECARD.md` convention credits moves only to their declared axes
  (e.g. `:1230`).
- The claim is non-exploratory per the contract's requirement: it is falsifiable by the frozen counter
  (mechanical arm already green at the measured rev) plus the bound vote arm, and it carries a recheck
  contract for future releases.

## No-harm, per axis

- Coverage (6): unchanged — no new measured surface; registry row is a note, not a capability.
- Operability (7): unchanged — no tool bytes; disk-guard/census untouched (verified: worktree diff vs the
  measured rev contains only wave dispatch files).
- Freshness (5, the C1 axis): unchanged and unblocked — counters verified disjoint above; C2 consumes no
  C1 S-ids and the two ledgers are separate files. My report emits no vote lines for either arm.
- Calibration (5): claims track their sources — I sampled 12 of 23 rows directly including every
  strong/counterexample-prone claim (btrfs zero-Avail semantics, XFS f_bavail=f_bfree, VFS ordering,
  tmpfs xattr/inode ceiling, statvfs f_favail equality, df --inodes column replacement) and found no
  overclaim; the two S542 rows attribute the equality to the manual rather than asserting it as kernel
  fact. The one unsourced decision-table interpretation (btrfs zero inodes) verifies against pinned
  sources per command 5.
- Adjacency (6): clean — "Boundaries" forbids writes/mounts/cache drops/repair/quota ops; EDQUOT is
  explicitly deferred to the existing `knowledge/quota-observability-r48.md`; tmpfs gets "no sizing
  recommendation"; nothing remedial is proposed.

## Host snapshot vs live event

- Contract rule (`contract.md:35`): the snapshot is "a read-only observation, not an ENOSPC reproduction
  or a counted subclaim." Entry compliance: the 23 counted rows all cite S535–S543; host numbers appear
  only under "## On this host" and "### Captured host snapshot"; `:50` ends "These are point-in-time
  observations, not an ENOSPC reproduction"; `:58` ends "both are point-in-time readings and neither
  reproduces ENOSPC"; the counter itself names the limit (`count-c2.py:35-36`: v7.3 bytes say nothing about
  this host's 7.2.11 kernel "and no ENOSPC was observed firing (every filesystem read here had free blocks
  and inodes)").
- Every snapshot figure is healthy (3%/26-30%/34% block use, 1% inode use, global_rsv_size ==
  global_rsv_reserved); no decision-table row asserts the host is in any runway-limiting state — the table
  rows are generic conditionals, and the btrfs zero-inode row is used to *correct* a misreading
  ("zero is not evidence of inode exhaustion"), the opposite of alarmism. A healthy snapshot is nowhere
  dressed up as a live ENOSPC event.
- Kernel versions are kept distinct (sources pinned at tag v7.3; host labeled 7.2.11-arch1-1), so no
  freshness confusion is introduced.

## Counterexample tested (strongest local challenge)

Challenge: "a new entry on ground the coverage map did not hold is a coverage/expansion move" (the corpus
README row could be read that way). Refuted by the lane's own admitted precedent: r54's identical-shaped
entry (new ground, knowledge only, README-registered) closed as depth improved with coverage and
operability explicitly "unchanged / not claimed" (`corpus/lessons/round-54-verifier-spotcheck.md:159-161`),
and the axis semantics in `SCORECARD.md:10-12` tie coverage to measured surfaces, not to knowledge rows.
The frozen contract is the only instruction source and it routes C2 to depth. No competing authority found.

## Unverified / out of scope

- Per-row entailment judgments are the En seats' arm (votes outstanding at yield time); my calibration
  sampling is 12/23 rows by direct source comparison, the rest counter-verified for location only
  (`located=23` is the counter's, not my re-derivation, for those 11).
- Vote settlement (`w1-results.json` binding) was not inspected; not required for the axis question.

## Findings

- None blocking; no axis harmed; C2 is a depth move consistent with contract routing and r49/r50/r54
  precedent. Evidence: this report §Axis analysis; `contract.md:8,29,35`; `SCORECARD.md:10-12`;
  `corpus/lessons/round-54-verifier-spotcheck.md:159-161`.
- Info — dual same-day host samples with differing numbers (`corpus/knowledge/disk-runway-enospc-r55.md:48-58`,
  /fast 30% vs 26%): honestly labeled and governed by the supersede sentence at :58; calibration-neutral.
- Info — the two S542 quote cells carry raw roff markup (`.I`/`.IR`): faithful to the pinned copy and
  counter-located, cosmetically rough for human readers; not a defect.
