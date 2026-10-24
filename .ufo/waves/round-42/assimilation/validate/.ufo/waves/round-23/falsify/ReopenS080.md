# ReopenS080 — S080 btrfs qgroup lifecycle re-open (round 23, wave 2)

Seat: `MadoR22-2.ReopenS080` (leaf, read-only). Question: re-open source row
S080 in `corpus/SOURCES.md`, verify scope/anchor, raw SHA-256, the ≤25-word
Gate quote, and the knowledge note's S080 claim against the source.
No registry/lesson/note edit. No code edit. No candidate, driver, case, oracle
or count measured — outside this seat's question.

Inputs read: `corpus/SOURCES.md` (row 86), `corpus/lessons/round-23.md` (Gate +
M4/M8 and strict-red sections), `corpus/knowledge/quota-surface-r23.md`,
`.ufo/waves/round-23/preseal-amendment.md`, `contract.md`,
`evidence/sources-manifest.json`, `evidence/source-quotes.json`,
`evidence/source-accounting.json`, `evidence/frozen-contradiction.json` not
opened (not needed), `build/SrcBtrfsQgroup.md` (prior re-opener),
`build/DraftSourceRows/rows.md`, `build/DraftKnowledge/quota-surface-r23.md`
(draft only). Pin `f3dc07c0bf423cc1947d0ffa91afa9ce236fbe3c`; HEAD
`6eb889c037163e4886eaa61501258910d6a529b9` (payload commit, pin is ancestor,
docs identical). Working tree `corpus/SOURCES.md` =
`1f49a4d8338a48f7a85c0614ab24261b5b113d858259e41c30f0f0930ff6ad09`,
`corpus/lessons/round-23.md` =
`93cfe32de5d36731fa266478120ff1565d1bdd7822868598624025e185e1339b`, both
byte-identical at the pin.

## Fetch identity — CONFIRMED

| Fact | Value |
|---|---|
| URL | `https://raw.githubusercontent.com/torvalds/linux/v7.2/fs/btrfs/qgroup.c` |
| Fetch | `curl -fsSL` to `/fast/scratch/hyaku/mori-r23/ReopenS080/qgroup.c` |
| Bytes / lines | 139049 / 4989 |
| **SHA-256 (fresh fetch)** | `121a0af27f9553a9749c837536d618e2ea50d44ce54b30b032fa56e6f3df6ed5` |
| Retained bytes `evidence/sources/S080-fs_btrfs_qgroup.c` | same SHA-256, `cmp` clean against the fresh fetch |
| `sources-manifest.json` S080 | same URL, `bytes` 139049, full SHA as above |
| Tracked blob at pin | `502fb4a55cb2278946d104e85c13bb80bf575b01`, `git cat-file` body SHA-256 as above, size 139049 |

The registry's truncated prefix `sha256 121a0af27f9553a9` matches the full
digest. Registry row text is byte-identical at pin and worktree. This fetch
does not by itself resolve the annotated tag object; the prior re-opener
(`build/SrcBtrfsQgroup.md`) bound the same SHA-256 to tag target commit
`8d3ae59288f1e7d58d76558a6ee96d533bc5019f`. I independently confirmed only the
URL bytes and the retained/pinned identities. No `lsp` device is exposed in
this seat's toolset, so anchors were verified by literal reads of the
digest-bound bytes (no language server answers for an upstream kernel file
outside the lane's indexed sources).

## Scope — CONFIRMED

Row scope: "qgroups sysfs creation versus actual status flags", tier A, code,
v7.2. `qgroup.c` contains exactly five direct call sites of the pair: adds at
441 and 1032, dels at 620, 689 and 1295 (one additional name mention is a
comment at 1046). The scope does **not** claim directory presence means
enabled; its teaches column explicitly denies that equivalence. This is the
narrowed scope recommended by `SrcBtrfsQgroup`, not the superseded original
contract's `dir present → enabled` arm (amended in `preseal-amendment.md`).

## Anchor verification — CONFIRMED, exact

Line numbers in the digest-bound retained file.

| Anchor | Verified content | Role |
|---|---|---|
| 432-433 | `if (!fs_info->quota_root) return 0;` | add only when a quota root exists |
| 441-443 | `ret = btrfs_sysfs_add_qgroups(fs_info); if (ret < 0) goto out;` | directory created at mount-time scan start |
| 444 | `/* default this to quota off, in case no status key is found */` | Gate quote |
| 445 | `fs_info->qgroup_flags = 0;` | enabled flag defaults off |
| 453-455, 464-476 | search; status key branch; 470-474 `old qgroup version, quota disabled` → `goto out` with `ret` still 0; 476 loads `qgroup_flags` from the status item | flag only turns on when a valid status key says ON |
| 612-615 | `out:` `qgroup_flags |= flags;` (local `flags` = 0 throughout) and `if (ret >= 0) { if (qgroup_flags & FLAG_ON) set_bit(BTRFS_FS_QUOTA_ENABLED) }` | off-flag path does not set quota-enabled |
| 616-623 | rescan handling; `return ret < 0 ? ret : 0;` | normal-return paths succeed with directory still present |
| 1032 | `btrfs_sysfs_add_qgroups` in `btrfs_quota_enable` (997), before `FLAG_ON` at 1104 and `set_bit` at 1256 | second add site |
| 620 | del inside `out:` when `ret < 0` (status-read error) | del |
| 689 | `btrfs_sysfs_del_qgroups` in `btrfs_free_qgroup_config` (667-690; caller comment 663-666 names close/open/quota-disable) | del |
| 1295 | del in `btrfs_quota_enable` error exit when `ret` | del |

All anchors resolve to the labeled constructs. The row's teaches sentence —
"A quota root can initialize its sysfs directory while the enabled flag
remains off; initialized does not mean enabled" — follows directly:

- no status key: pass 1 ends with `ret = 1` at 554-558 (or already at 453-455
  for an empty quota tree); at 612-615 the flag stays 0, the `ret < 0` del at
  618-620 is not taken, and 623 returns 0;
- old status version: 470-474 jumps to `out` with `ret == 0`; same result;
- enable/disable windows: add at 1032 precedes ON at 1104 and
  `BTRFS_FS_QUOTA_ENABLED` at 1256; disable clears the bit at 1367 and FLAG_ON
  at 1406 before `btrfs_free_qgroup_config` → 689 removes the directory.

## Gate quote — CONFIRMED

`corpus/lessons/round-23.md` Gate, S080 row:

> `|444: “default this to quota off, in case no status key is found” |`

- verbatim line 444 (comment markers excluded), exactly one occurrence in the
  file, **12 words ≤ 25**;
- `evidence/source-quotes.json` S080 records the same quote, `word_count` 12,
  `found_in_whitespace_normalized_source` true, and the matching full SHA-256;
- Gate decision "Admit A for lifecycle/flag separation; initialized directory
  can persist with quota off" matches the code paths above.

## Note claim-vs-source — CONFIRMED

Note bytes `corpus/knowledge/quota-surface-r23.md` =
`2614a8f133072b27a3d5e07a7ad5d70455f509ef4052c01a9ad7e112879b8c84`, identical
at pin.

| Note claim | Source verdict |
|---|---|
| 20-22: "S080 creates the directory before parsing that flag and can leave it initialized while quota is off." | TRUE. Add 441 precedes status parse 453-476; flags default 445; the two normal-return paths above leave the directory present with FLAG_ON clear and return 0. "Can" is exactly right; no frequency is claimed. |
| 41: "S079/S080: flag read, not a limit/usage read" | TRUE. The `enabled` attribute reads FLAG_ON (S079 sysfs.c:2363); S080 defines and maintains that flag; no limit is read. |
| 42: directory present + enabled0 → disabled | TRUE relative to the attribute's own semantics: enabled0 means FLAG_ON clear, and mount sets `BTRFS_FS_QUOTA_ENABLED` only when FLAG_ON (614-615). |
| 99-109: enabled-first is insufficient; real mode NEVER reads mode | CONSISTENT and strictly safer. `qgroup_mode_show` asserts `btrfs_qgroup_enabled` (S079:2378), which resolves to `BTRFS_FS_QUOTA_ENABLED` (qgroup.c:33-45), cleared at 1367; the `enabled` attribute reports FLAG_ON, cleared later at 1406. So a read of enabled=1 followed by mode can assert inside the wider 1367→1406 window as well as across 1406. The note's conclusion holds; its "ON flag between two reads" wording describes one window, not the only one. |
| No alternative S080 attribution found in the final note | The note cites S080 only at lines 21 and 41; no S080 claim about limits, capacity, ext/tmpfs/xfs, or remediation. |

The note's final text does not repeat the draft's error. The historical draft
`build/DraftKnowledge/quota-surface-r23.md:93` says "presence is evidence that
quota accounting is on", which S080 contradicts; the final note (lines 20-24,
41-43) replaces that with the enabled-flag rule. Draft is retained proposal
evidence, not shipped knowledge.

## Concrete discrepancies and residual limits

1. **Anchor completeness (minor, not a false claim).** The range `612-615`
   stops before the success condition at 616-623. The "directory persists with
   quota off on a successful mount" outcome also depends on `ret >= 0` at 613,
   del only when `ret < 0` at 618-620, and `return ret < 0 ? ret : 0` at 623,
   plus the loop-exit `ret == 1` at 554-558 and the `ret == 0` old-version exit
   at 470-474. Citing 612-615 alone shows flag arithmetic but not the
   successful-return branch. No edit made; if the registry is ever revised,
   extending to 612-623 is the accurate range.
2. **Reachability not established.** On healthy v7.2 metadata the persistent
   directory-present/quota-off state comes from defensive branches (old qgroup
   version, missing status key) and from concurrent enable/disable windows.
   Code paths observed; frequency not measured. `[INFERENCE]` The row says
   "can" and the note says "can"; neither asserts a normal steady state.
3. **Transient enabled=1 during disable.** The probe's `enabled` read reflects
   FLAG_ON (S080), while `btrfs_qgroup_enabled` reflects
   `BTRFS_FS_QUOTA_ENABLED`; the two are cleared at 1406 and 1367
   respectively. The note's final section forbids the mode read and already
   lists snapshot races as limits; no contradiction, but the distinction is
   load-bearing for any future mode-read proposal.
4. **Historical draft only.** `build/DraftKnowledge/quota-surface-r23.md:93`
   contains the contradicted presence→on sentence; it is superseded in the
   final note and is not part of the shipped knowledge bytes. Flagged so it is
   never cited as current.
5. No registry, lesson, note, frozen, oracle or production file was edited.
   HEAD is one commit past the pin with identical docs; that is the expected
   payload commit, not drift.

## Verdict

S080 row, its scope/anchor, the Gate quote and the final note's S080 sentence
are **CONFIRMED against digest-bound v7.2 bytes**. Zero claim-vs-source
contradictions in the registry/lesson/final note. Two low-severity
anchor-completeness/transient-state refinements and one already-corrected
historical draft observation are recorded above; none requires a registry
edit, and none changes the C2 rule that directory presence is initialization,
not enabled state.

## Non-actions

- No C1 original26/26, alias count, C2 29/30, selftest, quota, driver or
  mutation invocation; those belong to other seats and the parent.
- No live host reads, quota commands, service/process probes or `/tmp` use.
  Only network read: the single v7.2 source URL, into
  `/fast/scratch/hyaku/mori-r23/ReopenS080/`. No installs or upgrades.
- No writes outside this report; no lane index/jj/refs touched.
