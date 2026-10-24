# S078 source re-open — XFS option emission at tag v7.2

**Seat:** MadoR22-2.ReopenS078 (read-only leaf; no subagents, no edits to source/registry/frozen/oracle bytes, no driver/quota executions, no live-host reads).
**Row under check:** `corpus/SOURCES.md:84` — S078, `https://raw.githubusercontent.com/torvalds/linux/v7.2/fs/xfs/xfs_super.c`, kind `code`, tier `A`, scope `emitted XFS accounting/enforcement flags only`, anchor `xfs_fs_show_options:238-254; tag v7.2; sha256 0a95697dcfcdab8f`, status `mined`, opened `2026-10-21`, recheck `on-release`.
**Fresh copy:** `/fast/scratch/hyaku/mori-r23/ReopenS078/S078-fs_xfs_xfs_super.c` (HTTPS fetch from the row URL, 2026-10-21). Retained bytes compared at `.ufo/waves/round-23/evidence/sources/S078-fs_xfs_xfs_super.c`.
**Verdict:** the row's URL, tag, byte identity, anchor, Gate quote and the note's S078 claims are source-correct. **No contradiction found.** Four wording/scope observations and two residual unknowns below; none changes the row, its expected bytes, or any case expectation.

## 1. Byte identity and tag (observed)

| Check | Observed | Result |
|---|---|---|
| Fresh fetch size | 72773 bytes | matches manifest `bytes` |
| Fresh fetch sha256 | `0a95697dcfcdab8f7ab6ea26fdb941db952db4b73ed93c30d21e40861ed0450c` | exact match to assignment rawSHA and `evidence/sources-manifest.json` S078 |
| Retained evidence file sha256 | same full digest | match |
| `cmp` retained vs fresh | no difference | `BYTES_IDENTICAL` |
| Git blob id of fresh bytes | `63c4bcbe6c2bc427a7d21623e688833922693ae1` | equals GitHub API `contents/fs/xfs/xfs_super.c?ref=v7.2` `sha` and `size` 72773 |
| Tag claim `v7.2` | `refs/tags/v7.2` exists, annotated tag object `237a1c39e8dfd3e1c6f1f023eea37a48ec04cc63` → commit `8d3ae59288f1e7d58d76558a6ee96d533bc5019f` | tag verified, not a mutable branch |

The registry cell carries the 16-hex prefix `0a95697dcfcdab8f`, not the full 64 hex; that is exactly the first 16 characters of the verified digest and matches the stated convention for S077–S086 in `build/DraftSourceRows.md:41-42` ("Digests are full-length; the row cells carry the 16-hex prefix"). Full digest is retained in `sources-manifest.json` and `build/DraftSourceRows.md:48`. Older registry rows use full 64-hex sha fields, so the two conventions coexist; the S078 cell is internally consistent with its eight sibling rows. No duplicate occurrence of the S078 URL exists in `SOURCES.md` (`grep -n xfs_super.c` → line 84 only).

## 2. Anchor and located quote (observed)

File: `fs/xfs/xfs_super.c`, fetched bytes as above. Line numbers are exact for that digest.

- `xfs_fs_show_options` definition: `static int` at 186, name at 187, parameters/body 188–190; function closes at 263.
- Quota emission block: 238–254, exactly the cited anchor:
  - 238–241 `XFS_UQUOTA_ENFD` → `,usrquota`, else `XFS_UQUOTA_ACCT` → `,uqnoenforce`
  - 243–246 `XFS_PQUOTA_ENFD` → `,prjquota`, else `XFS_PQUOTA_ACCT` → `,pqnoenforce`
  - 248–251 `XFS_GQUOTA_ENFD` → `,grpquota`, else `XFS_GQUOTA_ACCT` → `,gqnoenforce`
  - 253–254 `if (!(mp->m_qflags & XFS_ALL_QUOTA_ACCT))` / `seq_puts(m, ",noquota");`
- Gate row (`corpus/lessons/round-23.md:44`) quotes 253–254 verbatim. Whitespace-normalized containment check: `True`; whitespace word count `6` (≤25). Located, not paraphrased.
- Gate decision "emitted XFS accounting/enforcement tokens, not synthetic conflicts/absence as host states" is consistent with the row's scope cell ("emitted XFS accounting/enforcement flags only") and with the file's single quota-emission site (grep over the whole file finds quota token strings only in the option table 114–116/157–168, the emission block 238–254, and the parse switch 1542–1578).

The anchor is a line range inside the function rather than the function's declaration range (186–190); `DraftSourceRows.md:62-67` records both and the registry's compact form is unambiguous. Not a defect.

## 3. Registry `teaches` claim vs source (observed)

| Claim (`SOURCES.md:84`) | Source evidence | Verdict |
|---|---|---|
| "noquota is printed only with no accounting flags" | 253–254: emission is guarded by `!(mp->m_qflags & XFS_ALL_QUOTA_ACCT)`; no other `noquota` emission exists in the file | true |
| "usrquota and uqnoenforce distinguish enforcement from accounting-only" | 238–241: ENFD→`usrquota`, else ACCT→`uqnoenforce`; same pattern for P/G at 243–251 | true |
| "Synthetic conflicting strings are probe policy, not kernel observations." | Parse path 1542–1578: `Opt_noquota` clears **both** `XFS_ALL_QUOTA_ACCT` and `XFS_ALL_QUOTA_ENFD` (1543–1544); every quota-implying option sets its ACCT bit (1550, 1555, 1561, 1565, 1571, 1575). Hence no mount-option order leaves a quota token set while ACCT is empty: `usrquota,noquota` ends with both cleared (prints only `,noquota`), `noquota,usrquota` ends with ACCT set (prints only `,usrquota`). Likewise "no quota token at all" cannot occur, because `,noquota` is emitted unconditionally whenever ACCT is empty | true for the in-file mount-option parse+emission path |

## 4. New note claim-vs-source (`corpus/knowledge/quota-surface-r23.md`)

All S078 citations are lines 37–40 of that note.

| Note row | Source check | Verdict |
|---|---|---|
| "XFS noquota, no other quota flag / disabled / S077/S078: no accounting flags" | 253–254; parse confirms noquota clears ACCT and ENFD (1542–1546) | true; note wording ("no accounting flags") is the correct reading of the emitted token |
| "XFS usrquota/grpquota/prjquota or accepted enforcing alias / enabled, enforced / S078: at least one enforcement flag, not a nonzero limit or every quota type" | 238–251 emit one token per quota type on ENFD; show_options reads flags only, never a limit or usage; P/G/U are independent | true; "not every quota type" is correct (U/P/G are separate conditions) |
| "XFS only uqnoenforce/gqnoenforce/pqnoenforce accounting flags / enabled, accounting_only / S078: accounting is not enforcement" | 240–241, 245–246, 250–251 select the `*noenforce` token exactly when ACCT is set and ENFD is clear | true |
| "XFS conflicting noquota plus quota flag, or no quota token at all / unknown / defensive parser rules, not claimed normal v7.2 kernel output" | conflict and total absence are unreachable from the mount-option parse (see §3 row 3) | true, with the residual in §6.1 |

No S078-backed sentence in the note asserts a limit, usage, capacity, health, or EDQUOT state; the note's boundary text matches the row's scope.

## 5. Observations (no claim-of-fact is false)

- **O1 — format, not error:** the registry cell stores a 16-hex prefix, not the full rawSHA the assignment names. Full digest independently verified twice (sha256 of fresh bytes; git blob `63c4bcbe…` against GitHub's `v7.2` contents API). No action requested; the registry was not edited.
- **O2 — scope boundary:** the note's enforcing row adds "or accepted enforcing alias". Source does register `quota`→`Opt_quota`, `uquota`, `gquota`, `pquota` (157, 162–164) and maps them to ENFD (1547–1551, 1559–1562, 1569–1572), so the claim is true of this file; however those spellings are **parse inputs only** and are never emitted by `xfs_fs_show_options`, and the alias table lies outside the anchored 238–254 range. The note qualifies conflicts as defensive parser policy but does not attach the same qualifier to the alias clause. This is a wording asymmetry, not a source contradiction.
- **O3 — completeness asymmetry:** the accounting-only row names the three emitted `*noenforce` tokens and omits `qnoenforce`, which the same file registers (168) and maps to user ACCT-without-ENFD (1553–1557); the contract's classification table does include `qnoenforce`. Accurate as emitted-token vocabulary, incomplete as accepted-key vocabulary.
- **O4 — basis-name caveat:** emitted `,noquota` is *not* evidence that the `noquota` mount option was supplied; it is emitted whenever no accounting bits are set, including a filesystem that never enabled quota (253–254). The note says "no accounting flags", which is correct; the contract's basis string `xfs_noquota_option` could be misread as option-presence evidence. No note change required from this re-open.

## 6. Residual unknowns / limits

1. **Runtime `m_qflags` transitions:** §3 row 3 proves conflict/absence impossible for the in-file mount-option parse. `show_options` reflects live `m_qflags`, which can also be changed by quotactl paths in other files (`xfs_qm_syscalls.c`), not opened here. The note already frames conflicts as defensive and "not claimed normal v7.2 kernel output", so this is a proof boundary of the row, not a contradiction. Settling it would require a different source row.
2. **`XFS_ALL_QUOTA_ACCT` bit composition** is defined outside this file (not in S078); its name and the parser's own set/clear use (1543, 1550, 1555, 1561, 1565, 1571, 1575) support the reading, but the macro definition itself was not re-opened in this row-scoped check.
3. Chronology: `opened 2026-10-21` is corroborated only by evidence mtimes (`sources/S078…c` 14:50, `SOURCES.md` 14:59, note 15:05, Gate 15:25 local) and by the draft receipt; timestamps are not proof of ordering, consistent with lesson M1. Chronology was not part of this check.

## 7. Method and compliance

Read-only: HTTPS GET of the row URL into `/fast/scratch/hyaku/mori-r23/ReopenS078/`; `sha256sum`, `cmp`, `git hash-object`, GitHub contents/tag API metadata; targeted `awk`/`sed`/`grep` line reads of the fetched and retained files; a Python whitespace-normalized quote check. No builds, tests, linters, selftests, pinned driver, quota tool, mount/quotactl/btrfs/xfs_qma/repquota call, journal/process/credential read, subagent, or lane/ref/index write. No production, frozen, oracle, case, or registry byte was changed.

**Bottom line:** S078 remains a valid tier-A, in-scope source for emitted XFS quota accounting/enforcement tokens (`usrquota`/`grpquota`/`prjquota`, their `*noenforce` accounting-only tokens, and the accounting-absence token `noquota`). The assignment's rawSHA is exactly reproduced (prefix in the row cell, full digest in evidence), the Gate quote is located at 253–254 and within the 25-word limit, and every S078-cited note sentence is supported by the fetched bytes. No red for this row; no change to the frozen CaseEscapedSpace/C1/C2 expectations is implied by this report.
