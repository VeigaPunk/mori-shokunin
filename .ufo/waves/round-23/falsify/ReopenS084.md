# ReopenS084 — Linux tmpfs quota options v7.2

Seat: `MadoR22-2.ReopenS084` (leaf, read-only).
Pinned production: `f3dc07c0bf423cc1947d0ffa91afa9ce236fbe3c`.
Scratch: `/fast/scratch/hyaku/mori-r23/ReopenS084/` (fresh fetch only; TMPDIR set there).
No registry, lesson, note, frozen, expectation or production byte was edited; no selftest,
oracle, driver, quota tool or privileged interface was executed. No tool install/update.
No LSP server is exposed to this seat; documentary/code identity is established from exact
bytes and line numbers, production vocabulary from read-only `git show`, not grep-as-proof
of behavior.

## Inputs re-opened

| Input | Location |
|---|---|
| Registry row | `corpus/SOURCES.md:90` (path line `corpus/SOURCES.md:100`) |
| Lesson Gate row | `corpus/lessons/round-23.md:50` |
| Knowledge-note row | `corpus/knowledge/quota-surface-r23.md:47` |
| Retained source bytes | `.ufo/waves/round-23/evidence/sources/S084-Documentation_filesystems_tmpfs.rst` |
| Manifest entry | `.ufo/waves/round-23/evidence/sources-manifest.json` (S084: `bytes` 13078, `sha256` 5ce3dffe…) |
| Quote receipt | `.ufo/waves/round-23/evidence/source-quotes.json` (S084: 12 words, `found_in_whitespace_normalized_source: true`) |
| Fresh upstream fetch | `https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/filesystems/tmpfs.rst` → `tmpfs-v7.2.rst` |
| Production vocabulary (read-only) | `git -C … show f3dc07c0…:tools/mori-quota-surface.py` |

## Identity — MATCH (observed)

- Fresh fetch SHA256 = `5ce3dffe9323912b9146a5f33744776ff623ef42cf8accd6b2dfbea0b9db5be6`, 13078 bytes,
  276 lines.
- Retained evidence file SHA256 is the same value (`sha256sum`), and `cmp` fresh vs retained
  reports byte-identical.
- Registry prefix `5ce3dffe9323912b` is the first 16 hex digits of that digest; URL and `tag v7.2`
  match the fetched artifact. No checksum discrepancy.

## Anchor and quote — observed line map

Frozen section (`tmpfs.rst`, v7.2, 1-based lines):

| Line | Content |
|---|---|
| 129 | `tmpfs also supports quota with the following mount options` |
| 131 | table start delimiter |
| 132 | `quota` row: `quota                    User and group quota accounting and enforcement` |
| 133 | continuation: `is enabled on the mount. Tmpfs is using hidden` |
| 134 | continuation: `system quota files that are initialized on mount.` |
| 135–138 | `usrquota` / `grpquota` accounting+enforcement rows |
| 139–142 | four hardlimit rows (`usrquota_block_hardlimit`, `usrquota_inode_hardlimit`, `grpquota_block_hardlimit`, `grpquota_inode_hardlimit`) |
| 143 | table end delimiter |
| 145 | `None of the quota related mount options can be set or changed on remount.` |

Concrete discrepancies (both minor, neither changes scope or admission):

1. Registry anchor `quota table:129-145` brackets the quota section, but the literal table grid is
   131–143 (content 132–142); 129 is the introducing sentence and 145 is the remount sentence.
   The anchor still lands on the correct section.
2. Gate row `corpus/lessons/round-23.md:50` cites `132–134` for the quote. The quote
   `User and group quota accounting and enforcement is enabled on the mount.` is contained
   entirely in lines 132–133 after whitespace normalization; line 134 is the rest of the same
   table cell (`system quota files that are initialized on mount.`) and is not part of the quoted
   sentence. If 132–134 is meant as the whole cell, that is defensible; as a quote span it
   over-runs by one line.
3. Quote check itself passes: 12 words (≤25), word-for-word in the whitespace-normalized source,
   consistent with `source-quotes.json`.

## Scope and "teaches" — claim vs source

Observed, source-supported:

- Scope `tmpfs quota flags and four documented hardlimit names` is accurate: the table documents
  exactly `quota`, `usrquota`, `grpquota` plus four uniquely named hardlimit options (132–142).
- `quota, usrquota and grpquota enable accounting/enforcement` is supported literally: 132–134
  (`quota`: user and group accounting/enforcement enabled), 135–138 (`usrquota`/`grpquota`).
- `hardlimit settings are separate`: supported. Rows 139–142 say only "Set global … hard limit";
  145 and 147–155 add remount/limit-initialization semantics with no accounting-enable claim.
- Gate decision `hardlimit-only activation is not taught by this sentence` is correct.

Inference, not literal source text (`[INFERENCE]`):

- `do not justify arbitrary suffix matching` follows from the closed enumeration of four names,
  not from an explicit prohibition in S084. It is corroborated by S086's closed
  `fsparam_string` table (`fs/shmem.c:4464–4467`), which accepts exactly those four names and has
  no generic `_hardlimit` parser. Admission is sound; the sentence should not be quoted as a
  source statement.

## Knowledge-note claim vs source — concrete problems

Target: `corpus/knowledge/quota-surface-r23.md:47`

> `tmpfs usrquota/grpquota flags or one of four documented hardlimit keys | enabled, enforced |
> S084/S086: actual emission tied to quota initialization; never arbitrary `_hardlimit` suffix matching`

1. **Omitted documented enabling token.** The row lists only `usrquota`/`grpquota`, but S084
   132–134 documents the distinct `quota` option that enables *both* user and group accounting
   and enforcement, and the pinned production set `TMPFS_QUOTA_KEYS`
   (`tools/mori-quota-surface.py:217–227`, `quota` at 219) already treats it as an enabling
   token. The note under-describes its own decision row (registry `teaches` and the amended
   contract both include `quota`).
2. **Hardlimit key presented as active-state evidence.** S084's four hardlimit rows only set
   global limits. S086 shows the mechanism: `Opt_*hardlimit` parse cases
   (`mm/shmem.c:4638–4672`) assign `ctx->qlimits.*` and never set `SHMEM_SEEN_QUOTA`; that flag
   is set only by `quota`/`usrquota`/`grpquota` (`:4623`, `:4629`, `:4635`). `sbinfo->qlimits` is
   copied only inside `if (ctx->seen & SHMEM_SEEN_QUOTA)` (`:5027`, `:5033`), yet
   `shmem_show_options` emits hardlimit keys solely on nonzero `sbinfo->qlimits`
   (`:4882–4893`), while `usrquota`/`grpquota` emission is gated on `sb_has_quota_active`
   (`:4878–4881`). Consequence: a hardlimit token proves the mount was *initialized* with quota,
   not that accounting/enforcement is active now; after a runtime quota-off the hardlimit token
   can remain the only quota-related token visible. Therefore the note's flat
   `hardlimit key → enabled, enforced` is not source-supported. It is at most the pre-registered
   defensive synthetic rule, which `preseal-amendment.md:73–77` states explicitly
   ("Hardlimit-only inputs are defensive synthetic cases"), and which the Gate correctly declines
   to derive from S084. The note drops that qualification and cites S084/S086 as if they taught
   the state.
3. **"inactive quota prints no quota keys"** (note, exit/evidence section) is false for the
   four hardlimit keys by the same `:4882–4893` gating: they persist while the active flags are
   suppressed at `:4878–4881`. It is true that compiled-out `CONFIG_TMPFS_QUOTA` prints none
   (`:4876` `#ifdef`).
4. The phrase `actual emission tied to quota initialization` is literally true for hardlimits
   (`qlimits` is copied only under the mount-time seen-gate at `:5027/:5033`) but is stated next
   to an active-state conclusion; "initialized" and "currently enabled" are exactly the
   distinction this round exists to keep (M4 class), so the row should not use it as support for
   `enabled, enforced`.

## Sealed-case context (not changed, not executed)

`frozen/quota-cases/CaseTmpfsHardlimit.json` expects
`enabled`/`enforced`/`tmpfs_quota_option` for a mountinfo whose only quota-related key is
`grpquota_block_hardlimit=1m`, with rationale citing the contract table and the pre-seal
amendment, not S084. That expectation is a pre-registered defensive contract decision inside the
sealed denominator; whether it should remain, or the note should carry the synthetic qualifier,
is the parent's ruling. I did not execute the case, oracle or driver, and did not edit it.

## Remaining unknowns

- Whether a live tmpfs can present a hardlimit-only mountinfo snapshot at all is a kernel
  dynamic path (`Q_QUOTAOFF` after a mount that initialized limits); I verified the code paths
  cited above but did not exercise any host or fixture.
- No host quota state, mount topology or health is inferred here. No privileged reads or
  quota commands were performed.
- The frozen `CaseEscapedSpace`, C1/C2 counts, quota selftest 49/49 and the pinned-driver red are
  outside this seat's question and were not touched.
