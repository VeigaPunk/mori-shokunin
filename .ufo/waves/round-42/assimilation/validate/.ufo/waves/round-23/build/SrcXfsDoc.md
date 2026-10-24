# SrcXfsDoc — independent verification of XFS quota mount options (S077)

Seat: `MadoR22-2.SrcXfsDoc-8`. Mode: read-only source verification. No implementation was
read, no fixture case or oracle was consulted, `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md`
was not edited, and no build/test/lint/smoke command was run.

Target: https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/admin-guide/xfs.rst
Fetched: 2026-10-21 into `/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/round23/SrcXfsDoc/xfs.rst`
(fetch directory is the only write outside this report). No installs or updates were performed.

## Identity of the fetched bytes

| property | value |
|---|---|
| bytes | 22719 |
| lines | 563 |
| SHA-256 of fetched bytes | `53bda67b5612a3f2c02820604d05825c9d37addba9855e1d4fba330a516d051c` |
| git blob SHA-1 of fetched bytes | `acdd4b65964c058647a7b383d8c2c778777a538e` |
| HTTP status / content-length | 200 / 22719 |
| GitHub contents API at `?ref=v7.2` | `sha=acdd4b65964c058647a7b383d8c2c778777a538e`, `size=22719`, decoded SHA-256 `53bda67b5612a3f2c02820604d05825c9d37addba9855e1d4fba330a516d051c` |

The API-reported tree blob SHA equals the locally computed `sha1("blob 22719\0" + bytes)`,
and the API-decoded content hash equals the fetched-byte hash; a second independent fetch was
byte-identical (`cmp`). The bytes therefore correspond to the `Documentation/admin-guide/xfs.rst`
tree entry at tag v7.2, not merely to whatever the URL served once. The response `ETag`
(`49931b6b...6aa63`) is not the body SHA-256; it is GitHub's representation tag, so it was not
used as a content digest.

Anchor slice (the exact cited block): byte offset `6903` (start of line 171), end offset `7455`
(end of line 185), 552 bytes, SHA-256 `3ea84f0d417486c8175335319a0019fe292956f6da9302dd523fe8354668d04f`.

## Anchor verification — lines 171-185

Verified: the block starts at line 171 and ends at line 185. It sits inside the
`Mount Options` section (heading at lines 19-20); the next major heading is
`Deprecation of V4 Format` (lines 226-227). Nothing precedes line 171 in this block except a
blank line (170); line 185 is the last line of the `pquota` entry.

```
171:  noquota
172:	Forcibly turns off all quota accounting and enforcement
173:	within the filesystem.
174:
175:  uquota/usrquota/uqnoenforce/quota
176:	User disk quota accounting enabled, and limits (optionally)
177:	enforced.  Refer to **xfs_quota(8)** for further details.
178:
179:  gquota/grpquota/gqnoenforce
180:	Group disk quota accounting enabled and limits (optionally)
181:	enforced.  Refer to **xfs_quota(8)** for further details.
182:
183:  pquota/prjquota/pqnoenforce
184:	Project disk quota accounting enabled and limits (optionally)
185:	enforced.  Refer to **xfs_quota(8)** for further details.
```

Option-key inventory in the whole file (whole-token occurrences): `noquota` 1 (`:171`),
`uquota` 1, `usrquota` 1, `uqnoenforce` 1, standalone `quota` 1 as an option (`:175`; the other
four `quota` tokens at `:172,176,180,184` are prose "quota accounting"), `gquota` 1,
`grpquota` 1, `gqnoenforce` 1, `pquota` 1, `prjquota` 1, `pqnoenforce` 1. Bare `qnoenforce`
has **0** occurrences in this file.

## Designated supporting quote (11 words)

> "Forcibly turns off all quota accounting and enforcement within the filesystem."

Location: `/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/round23/SrcXfsDoc/xfs.rst:172-173`
(option key `noquota` at `:171`).

Rule it backs — contract §C2 xfs row: `noquota` present and no quota key present →
`quota_state: disabled`, `enforcement: n/a`, `basis: xfs_noquota_option`.

Verdict for that rule: **supports**. The sentence states that `noquota` turns off both
quota accounting and enforcement for the filesystem, which is exactly the disabled state and
the `n/a` enforcement cell; the basis token names the documented option.

## Do the same lines support the rest of the xfs table?

The quote supports one row; the block does not fully determine the other four. Per-row verdicts:

| contract §C2 xfs row | source verdict | evidence and gap |
|---|---|---|
| `noquota`, no quota key → disabled / n/a / `xfs_noquota_option` | **supports** | `:171-173`; designated quote above. |
| any of `usrquota,uquota,quota,grpquota,gquota,prjquota,pquota`, no `noquota` → enabled / enforced / `xfs_quota_option` | **enabled supports; `enforced` under-determined** | All seven names are present at `:175`, `:179`, `:183`. The text says "accounting enabled, and limits (optionally) enforced" (`:176-177`, `:180-181`, `:184-185`): enforcement depends on limits being set, and this probe reads no limits. The doc establishes enforcement capability/availability, not that EDQUOT is currently armed. |
| only `uqnoenforce,gqnoenforce,pqnoenforce,qnoenforce`, no `noquota` → enabled / accounting_only / `xfs_quota_option` | **enabled supports; `accounting_only` under-determined; bare `qnoenforce` unsupported** | `uqnoenforce` `:175`, `gqnoenforce` `:179`, `pqnoenforce` `:183` are listed under headings whose text says accounting is enabled, so "not disabled" is supported. The block never says "accounting only" and groups each noenforce form with its enforced form; the accounting-only reading rests on the option name, not on a stated semantics. `qnoenforce` (no scope prefix) appears nowhere in the file, so that token is not covered by this source at all. |
| `noquota` with any quota key → unknown / n/a / `xfs_conflicting_quota_options` | **under-determines (weak lean toward disabled)** | The block never addresses simultaneous specification or precedence. "Forcibly turns off all quota accounting and enforcement" (`:172-173`) could be read as `noquota` winning, i.e. `disabled`, rather than `unknown`; "forcibly" is not an explicit precedence rule, so it neither supports nor cleanly contradicts the conservative `unknown`. Note this row is unreachable in real kernel-emitted mountinfo if S078 holds (`noquota` printed only when no accounting flag is set); it is a synthetic/adversarial-input row. |
| neither `noquota` nor any quota key → unknown / n/a / `xfs_quota_options_absent` | **under-determines** | The block documents option semantics only; it states no default state and no absence semantics. It also shows that mount options are not all reflected in `/proc/self/mounts` (`errortag` note, `:221-222`), so absence in a mount option string cannot be read as proof of disabled. That supports keeping `unknown` conservative, but the doc does not state the rule. |

Two scope limits apply to every row above. First, this file documents **mount options the kernel
accepts**, not the exact super-option string `/proc/self/mountinfo` re-emits (alias choice,
one-option-per-scope emission, and `noquota` emission belong to `fs/xfs/xfs_super.c`, S078).
Second, the doc is silent on superblock-resident quota state when no option is present and on any
per-user/group/project limit or usage value.

## Tier assignment

**Tier A**, scope narrowed to: *XFS quota mount-option vocabulary at tag v7.2 and the
`noquota` = accounting and enforcement off statement.* Upstream kernel documentation is the
primary, version-pinned reference for the option names and for the `noquota` rule; the bytes are
authenticated against the v7.2 tree.

Tier A does **not** extend to: `enforcement: enforced` being armed, `accounting_only` as a stated
semantics, bare `qnoenforce`, conflict precedence when `noquota` and a quota key coexist, the
mountinfo emission surface, or absence-of-option state. Those need S078 (xfs_super.c) or are
deliberately conservative probe policy, not documented facts. If L1 wants one row for both the
vocabulary and the mountinfo surface, this file alone cannot carry the second half.

This matches draft row S077 in
`/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/build/DraftSourceRows/rows.md`
(sha prefix `53bda67b5612a3f2`, anchors `:171-173,175-177,179-181,183-185`, tier A). The draft's
"teaches" cell says the noenforce suffix "names accounting without enforcement"; that is a
reasonable reading of the pairing and the name, but the literal text does not state it — record
it as inference if the row is admitted.

## Citation drift observed (no edit made)

`/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/build/CaseXfsDevMismatch.md:128`
cites "`Documentation/admin-guide/xfs.rst` — lines 170–184". The verified block is **171–185**;
line 170 is blank and line 184 is the first prose line of the `pquota` entry. The draft S077 row
and `CaseXfsMixedEnforce.md` cite the correct ranges. Flagged for L1 only.

## Remaining unknowns

- Whether bare `qnoenforce` is a real XFS mount alias: not observable in this file (0
  occurrences); would require `fs/xfs/xfs_super.c` or `xfs_quota(8)`, neither opened by this seat.
- Whether the kernel's mountinfo super-option string preserves these exact spellings: outside
  S077; S078 is the governing source.
- Whether `enforcement: enforced` should be weakened in the contract: frozen-contract question for
  L1, not changed here. This seat only records that S077 establishes availability, not arming.
