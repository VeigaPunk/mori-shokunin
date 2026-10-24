# ReopenS086 — independent re-open of source row S086 (Linux v7.2 `mm/shmem.c`)

Seat: `MadoR22-2.ReopenS086` · round 23 · read-only source re-opener.
Authority: `corpus/SOURCES.md` row S086, `corpus/lessons/round-23.md` Gate row S086,
`corpus/knowledge/quota-surface-r23.md` lines 47–48, `evidence/sources-manifest.json`,
`evidence/source-quotes.json`, `evidence/sources/S086-mm_shmem.c`.
No registry, source, expectation, oracle, implementation, case or Git object was edited.

## Verdict

The row's identity, scope, anchors, quote and teaches-cell core claims are **supported**
by the pinned v7.2 bytes. Two wording overreaches are located in the *new knowledge note*
(F1, F2) and one contract-scope limit is recorded (F3). None changes a frozen expectation,
the six-field C2 path-level classification for real v7.2 mountinfo, the C1 retention
cutover, or the separately corrected quota-selftest arm. Report-only; no remediation.

## 1. Exact source identity (observed)

| item | value |
|---|---|
| row | `| S086 | Linux tmpfs quota emission v7.2 — https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/shmem.c | code | A | active tmpfs quota token emission and default-limit initialization | shmem_show_options:4877-4894; enable initialization:5026-5038; tag v7.2; sha256 eb5d1e9107b287c8 | usrquota/grpquota tokens test active quota; only four named hardlimit keys are emitted, after quota initialization. | mined | 2026-10-21 | on-release | corpus/lessons/round-23.md, corpus/knowledge/quota-surface-r23.md |` |
| URL | `https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/shmem.c` |
| independent fetch | `/fast/scratch/hyaku/mori-r23/ReopenS086/shmem.c` |
| fetched sha256 | `eb5d1e9107b287c8d9d2c1dda83aa0e573917d5b0f88dc17b55162f22718cefb` |
| fetched bytes | `160068` |
| retained evidence | `.ufo/waves/round-23/evidence/sources/S086-mm_shmem.c`, same sha256 and byte count |
| comparison | `cmp` fetched vs retained → byte-identical |
| manifest | `sources-manifest.json` S086 `bytes` 160068, `sha256` full digest above |
| quotes file | `source-quotes.json` S086 `source_sha256` full digest above, `found_in_whitespace_normalized_source` true |
| row digest field | `eb5d1e9107b287c8` is the correct prefix of the full digest (row field is a prefix, not a different digest) |

Supporting kernel files fetched only to determine exported semantics referenced below
(not registry rows, not counted as S086 bytes):
`fs/quota/dquot.c` `951a0c8d0887f9c55d707818190ef4ce471a3d255ed7018f316c6625e997ed21` (84353 B);
`include/linux/quotaops.h` `2a316c7714d1e00c03361cdd46064637f523067dc9eef9abd5faa5ec437120da` (10287 B);
`include/linux/quota.h` `6acf78eaa04504881dff7f38fc4e85a4a76c0ec1054d123a778ee8e3c7980a5b` (19211 B).

## 2. Scope, anchors and quote (observed)

Scope cell: “active tmpfs quota token emission and default-limit initialization”.
Both halves are in the cited file and anchors:

- `shmem_show_options` starts at line 4827; the whole quota-emission block is
  4877 `#ifdef CONFIG_TMPFS_QUOTA` … 4894 `#endif`, exactly the row range.
- 4878 `if (sb_has_quota_active(root->d_sb, USRQUOTA))`
  4879 `seq_printf(seq, ",usrquota");`
  4880 `if (sb_has_quota_active(root->d_sb, GRPQUOTA))`
  4881 `seq_printf(seq, ",grpquota");`
  4882–4893: exactly four hardlimit names, each gated on a nonzero
  `sbinfo->qlimits.{usrquota,grpquota}_{b,i}hardlimit`:
  `usrquota_block_hardlimit`, `grpquota_block_hardlimit`,
  `usrquota_inode_hardlimit`, `grpquota_inode_hardlimit`.
- Enable/default-limit initialization: 5026 `#ifdef CONFIG_TMPFS_QUOTA`,
  5027 `if (ctx->seen & SHMEM_SEEN_QUOTA) {`,
  5032–5034 `/* Copy the default limits from ctx into sbinfo */` +
  `memcpy(&sbinfo->qlimits, &ctx->qlimits, sizeof(struct shmem_quota_limits));`,
  5036–5037 `if (shmem_enable_quotas(sb, ctx->quota_types)) goto failed;`, 5039 `#endif`.
  Range 5026–5038 is exact. `shmem_enable_quotas` loads each requested type with
  `DQUOT_USAGE_ENABLED | DQUOT_LIMITS_ENABLED` (lines 307–309).
- “After quota initialization” holds: `qlimits` is copied and quota load attempted in
  `shmem_fill_super`, before the root inode is created (5041–5042); `show_options`
  can only run on the mounted superblock.

Quote check for the lesson23 Gate cell:

```
| S086 | .../mm/shmem.c |4878–4879: `if (sb_has_quota_active(root->d_sb, USRQUOTA)) seq_printf(seq, ",usrquota");` | Admit A for actual tmpfs active-quota emission and four hardlimit names; no arbitrary suffix matching. |
```

- Located at 4878–4879 exactly; the source breaks the statement across those two lines.
- Exact raw-text occurrences of the one-line quote: 0 (expected due the newline).
- Occurrences after whitespace normalization: 1 (unique).
- Whitespace word count: 5, matching `source-quotes.json` `word_count: 5`; within the
  ≤25-word lesson Gate bound.
- Gate wording “actual tmpfs active-quota emission and four hardlimit names; no arbitrary
  suffix matching” is supported: the names are exactly the four in 4882–4893 and the
  `fsparam` table registers exactly those four names (4460–4467), so an arbitrary
  `_hardlimit` suffix is not a registered tmpfs option.

## 3. Row teaches-cell versus source (observed)

Supported verbatim by S086:

1. “usrquota/grpquota tokens test active quota” — 4878/4880 call
   `sb_has_quota_active`. Traced definition (`include/linux/quotaops.h:159-163`,
   `:139-157`): active = `DQUOT_USAGE_ENABLED` for the type and not
   `DQUOT_SUSPENDED`; mount-time load sets `DQUOT_USAGE_ENABLED` (shmem.c 307–309).
2. “only four named hardlimit keys are emitted” — exactly four names at 4882–4893, each
   printed only when its copied limit is nonzero (mount parser rejects a zero/`!size`
   value at 4640, 4649, 4658, 4667).
3. “after quota initialization” — copy/enable at 5026–5038 precedes any possible
   `show_options`; comment at 5032 itself calls them “default limits”.

One source fact sharpens the note's use of these lines: the four hardlimit **option
handlers do not set `SHMEM_SEEN_QUOTA`** — only `quota` (4623), `usrquota` (4629) and
`grpquota` (4635) do; the hardlimit handlers (4638–4673) only assign
`ctx->qlimits.*hardlimit`. Therefore a hardlimit-only mount never copies `qlimits`
(5027 guard false), never enables quota, and `show_options` prints no quota key at all.
This is observed, not inferred from docs: it follows directly from the guards. It
supports the preseal amendment's “hardlimit-only inputs are defensive synthetic cases”
and confirms the frozen `CaseTmpfsHardlimit` is a contract-rule case rather than a
real v7.2 mountinfo state.

## 4. New knowledge-note claims versus source

Note `corpus/knowledge/quota-surface-r23.md`:
line 47 `| tmpfs usrquota/grpquota flags or one of four documented hardlimit keys | enabled, enforced | S084/S086: actual emission tied to quota initialization; never arbitrary _hardlimit suffix matching |`
line 48 `| tmpfs no quota options | disabled at snapshot | S086 compiled-out or inactive quota prints no quota keys; no capacity implication |`

### F1 — line 48's “inactive quota prints no quota keys” is overbroad (observed)

The `usrquota`/`grpquota` tokens are gated on active state (4878/4880), but the four
hardlimit prints (4882–4893) are gated only on nonzero `sbinfo->qlimits`, **not** on
`sb_has_quota_active`. A reachable mixed configuration shows the literal universal is
false per quota type:

- mount options `usrquota,grpquota_block_hardlimit=1m`:
  `usrquota` sets `SHMEM_SEEN_QUOTA` (4629) and `QTYPE_MASK_USR` (4630);
  `grpquota_block_hardlimit` stores `ctx->qlimits.grpquota_bhardlimit` (4654) but does
  not add GRP to `quota_types`;
  `qlimits` is copied because the guard at 5027 is true;
  `show_options` then prints `,usrquota` (4878) **and**
  `,grpquota_block_hardlimit=…` (4885–4887) while GRP quota is inactive.
- Whole-mount “no quota options” is still true: no options → `qlimits` zero and no
  active type → no keys, and `CONFIG_TMPFS_QUOTA` off removes the whole block
  (4877–4894) and the parser names (4460–4467).

Impact: none on the probe's per-path six-field verdict for real output, because in any
kernel-emitted line carrying a hardlimit key at least one active token (`usrquota` or
`grpquota`) is also emitted, so the path is already `enabled`. The sentence should not be
reused as a per-type rule.

### F2 — line 47's “actual emission tied to quota initialization” conflates two gates (observed)

- Active tokens: gated at dump time on `sb_has_quota_active` (accounting enabled and not
  suspended), not merely “initialized”.
- Hardlimit keys: gated on `qlimits` having been copied at initialization. That copy is
  type-agnostic (`memcpy` of the whole struct at 5032–5034), so a hardlimit key can be
  emitted for a type that is not active (F1's mixed case).
- Consequently “one of four hardlimit keys → enabled, enforced” is source-consistent at
  **path level** only because any real kernel-emitted hardlimit key co-occurs with an
  active flag at mount; the hardlimit line itself supplies no active-state or enforcement
  evidence. For a synthetic hardlimit-only fixture, `enabled/enforced` is the contract's
  defensive convention (amendment), not a source-derived fact; S086 shows the kernel
  drops such limits silently and emits nothing.
- “never arbitrary `_hardlimit` suffix matching” is exactly supported (4460–4467); that
  part needs no qualification.

### F3 — “enforced” is a mount-time mechanism flag, not a runtime enforcement guarantee (inference from traced definition)

`sb_has_quota_active` reads `DQUOT_USAGE_ENABLED` and non-suspension only
(`include/linux/quotaops.h:139-163`). Enforcement enablement is a separate
`DQUOT_LIMITS_ENABLED` flag. `fs/quota/dquot.c` `dquot_quota_disable`
(lines 2641–2672) refuses to turn off accounting flags but does allow clearing
enforcement flags; `show_options` would still print `usrquota` because usage remains
enabled. Thus the token proves accounting visibility, not that limits are currently
enforced. The preseal amendment already defines `enforced` as “mechanism flags, never a
nonzero limit”, which is the correct reading; the note's `enabled, enforced` should be
read as mount-time mechanism evidence only. This facet comes from the traced helper/dquot
definition, not from the S086 bytes alone, and is recorded as inference.

## 5. Consequence for this round

- No contradiction with the row's own `teaches` cell, which does not claim hardlimit
  emission tests active state, and no correction to the S086 registry bytes is warranted.
- No change to any frozen case, oracle, driver, expectation, `CaseEscapedSpace` handling,
  C1 alias counts, or the separately co-evolved quota-selftest arm. F1/F2 are wording
  precision in the knowledge note; F3 is an existing contract boundary, not a defect.
- If the note owner later revises prose (not this seat, not frozen), the source-faithful
  wording would be: “compiled-out or quota-uninitialized tmpfs prints no quota keys; a
  hardlimit key is initialization-gated and can accompany a type whose active token is
  absent, but every kernel-emitted hardlimit key co-occurs with at least one active
  `usrquota`/`grpquota` token.” No expectation or implementation implication.

## 6. Side observation outside the assigned row (noted, no action)

`build/CaseTmpfsHardlimit.md` cites S086 line ranges that do not match the retained
bytes: it says `quota` 4626–4631, `usrquota` 4632–4637, `grpquota` 4638–4643,
hardlimits 4644–4679, `shmem_show_options` 4833–4902, fill-super 5033–5044. Retained
bytes show `Opt_quota` at 4620, `Opt_usrquota` at 4626, `Opt_grpquota` at 4632,
hardlimits 4638–4673, `shmem_show_options` 4827–4896 with the emission block
4877–4894, and the fill-super quota block 5026–5038. The registry row, lesson Gate,
`source-quotes.json` and `sources-manifest.json` all use the retained, correct ranges;
only that derived report's local line numbering is offset. Flagged for the owning seat;
not edited here.

## 7. Bounds honoured

Read-only: no live journal/process/service/session probe, no `/proc` host read, no
quotactl/`btrfs`/`xfs_quota`/`repquota`/`mount`/qgroup call, no build/test/lint/oracle/
selftest/pinned-driver run, no Git mutation, no sibling or lane-index write. Network use
was limited to fetching the pinned raw kernel files into
`/fast/scratch/hyaku/mori-r23/ReopenS086/`; no `/tmp` fallback. No tool install or
update was performed. The only lane write is this report.
