# RevengeTmpfsQuota — tmpfs quota `show_options` reconstruction (v7.2)

Seat: MadoR22-2.RevengeTmpfsQuota-8 (leaf, read-only; no implementation, tests, or host probes).
Question: which quota options does tmpfs print into mountinfo super options (incl. hardlimit
keys), and do the contract's two tmpfs classification rows match what the kernel prints?

## Sources (fetched to `.scratch/round23/RevengeTmpfsQuota/`, kernel tag `v7.2`)

| file | integrity |
|---|---|
| `mm/shmem.c` | kernel.org plain + raw.githubusercontent `v7.2`, sha256 identical `eb5d1e9107b287c8d9d2c1dda83aa0e573917d5b0f88dc17b55162f22718cefb` |
| `mm/shmem_quota.c` | kernel.org plain, 351 lines |
| `fs/proc_namespace.c` | kernel.org plain |
| `fs/quota/dquot.c` | kernel.org plain |
| `include/linux/shmem_fs.h`, `include/linux/quota.h`, `include/linux/quotaops.h`, `include/uapi/linux/quota.h`, `fs/Kconfig` | kernel.org plain |
| `Documentation/filesystems/tmpfs.rst` | kernel.org plain |
| Arch official kernel config | gitlab.archlinux.org packaging/linux `main` `config.x86_64`, header `# Linux/x86 7.2.11-arch1` (sourced web fact, not a host read) |

No tools installed this wave (curl/python3 pre-existing). No live host reads performed.

## 1. Reconstructed contract of tmpfs mountinfo super options

Field assembly — `show_mountinfo` (`fs/proc_namespace.c:135-188`): super options field =
`sb_rdonly(sb) ? " ro" : " rw"` + `show_sb_opts` (`:45-62`: `,sync`/`,dirsync`/`,mand`/`,lazytime`
by sb flags) + `security_sb_show_options` (LSM) + `sb->s_op->show_options(...)` output, verbatim.

tmpfs `s_op->show_options = shmem_show_options` (`mm/shmem.c:5218`, inside `CONFIG_TMPFS`).
Body `mm/shmem.c:4827-4896`. Complete emission list (each prefixed `,`, conditional):

| token | condition |
|---|---|
| `size=%luk` | `max_blocks != shmem_default_max_blocks()` |
| `nr_inodes=%lu` | `max_inodes != shmem_default_max_inodes()` |
| `mode=%03ho` | mode != `0777\|S_ISVTX` |
| `uid=%u` / `gid=%u` | non-root uid/gid |
| `inode32` / `inode64` | per inode64/inums truth table (`:4855-4861`) |
| `huge=%s` | `CONFIG_TRANSPARENT_HUGEPAGE && sbinfo->huge` |
| `mpol=…` | via `shmem_show_mpol` |
| `noswap` | `sbinfo->noswap` |
| **quota block** (`:4877-4894`, whole block `#ifdef CONFIG_TMPFS_QUOTA`) | |

Quota tokens, exact conditions:

| token | condition |
|---|---|
| `usrquota` | `sb_has_quota_active(sb, USRQUOTA)` |
| `grpquota` | `sb_has_quota_active(sb, GRPQUOTA)` |
| `usrquota_block_hardlimit=%lld` | `sbinfo->qlimits.usrquota_bhardlimit != 0` |
| `grpquota_block_hardlimit=%lld` | `sbinfo->qlimits.grpquota_bhardlimit != 0` |
| `usrquota_inode_hardlimit=%lld` | `sbinfo->qlimits.usrquota_ihardlimit != 0` |
| `grpquota_inode_hardlimit=%lld` | `sbinfo->qlimits.grpquota_ihardlimit != 0` |

`sb_has_quota_active` = loaded && not suspended (`include/linux/quotaops.h:159-162`; `!CONFIG_QUOTA`
stub `:204-207`). Values are decimal (`%lld`); no escaping involved. **Complete** quota-related
key set printable in mountinfo = `{usrquota, grpquota, usrquota_block_hardlimit,
usrquota_inode_hardlimit, grpquota_block_hardlimit, grpquota_inode_hardlimit}`.

Bare `quota` is **never** printed: parse-only alias (`:4461`, case `:4620-4625`). No
`prjquota`/`noquota`/`*noenforce` keys exist for tmpfs.

## 2. Parse ↔ show mapping (why the conditions are what they are)

- Parse table `shmem.c:4460-4468`: flags `quota`, `usrquota`, `grpquota`; strings
  `usrquota_block_hardlimit`, `usrquota_inode_hardlimit`, `grpquota_block_hardlimit`,
  `grpquota_inode_hardlimit` (all `#ifdef CONFIG_TMPFS_QUOTA`).
- Flag cases (`:4620-4637`) set `SHMEM_SEEN_QUOTA` and OR into `quota_types`
  (`quota` ⇒ USR|GRP; `usrquota` ⇒ USR; `grpquota` ⇒ GRP). Hardlimit cases (`:4638-4673`) only
  set `ctx->qlimits.*` — they never set `SHMEM_SEEN_QUOTA` nor `quota_types`.
- `fill_super` (`:5027-5038`): only under `SHMEM_SEEN_QUOTA` ⇒ wire `dq_op`/`s_qcop`
  (`dquot_quotactl_sysfile_ops`), `memcpy` limits into `sbinfo->qlimits`,
  `shmem_enable_quotas(sb, quota_types)` loading each type with
  `DQUOT_USAGE_ENABLED | DQUOT_LIMITS_ENABLED` (`:298-321`); any load failure aborts the mount.
- Remount (`:4778-4793`): enabling quota forbidden; changing any global hardlimit forbidden.
  Docs agree: `tmpfs.rst:129-158` (same seven options; "None of the quota related mount options
  can be set or changed on remount"; defaults seed dquots on first access).
- Enforcement is real: `mm/shmem_quota.c` `shmem_acquire_dquot` seeds new per-id rb-tree entries
  from `sbinfo->qlimits` (USRQUOTA/GRPQUOTA branches); format registered as
  `QFMT_SHMEM = 5` (`shmem_quota.c:324-329`, `include/uapi/linux/quota.h:80`).

### Meta-proofs for observability

- **No false negative** (an enabled mount always shows ≥1 key): any active type ⇒ `SHMEM_SEEN_QUOTA`
  at mount ⇒ `shmem_enable_quotas` succeeded ⇒ `sb_has_quota_active` true ⇒ its flag token printed.
  Accounting cannot be turned off post-mount: `s_qcop = dquot_quotactl_sysfile_ops` (`:5029`);
  `dquot_quota_disable` (`fs/quota/dquot.c:2641-2689`) refuses accounting flags (`-EOPNOTSUPP`,
  `:2652-2656`) and only clears `DQUOT_LIMITS_ENABLED`; `dquot_quota_off` (`:2371-2375`) runs only
  in the mount-failure unwind and `put_super`.
- **No false positive** (no non-quota token can trigger): generic tokens (`ro|rw,sync,dirsync,
  mand,lazytime`, LSM opts) and all other shmem tokens (`size,nr_inodes,mode,uid,gid,inode32/64,
  huge,mpol,noswap,casefold,strict_encoding`) are never `quota`/`usrquota`/`grpquota` and never
  end in `_hardlimit`.
- **Cross-type asymmetry** (the one real subtlety): hardlimit tokens print from `sbinfo->qlimits`
  regardless of that type's active state. E.g. `mount -o usrquota,grpquota_inode_hardlimit=N`
  prints `usrquota,grpquota_inode_hardlimit=N` with **no** `grpquota` (GRP type never loaded; the
  stored GRP default is inert because GRP dquots are only acquired for loaded types). A
  `_hardlimit` token can never appear alone: nonzero `qlimits` requires `SHMEM_SEEN_QUOTA`
  requires a flag ⇒ ≥1 flag token always co-present.

## 3. Verdict vs contract tmpfs rows

**Row 1 — "any of `quota`,`usrquota`,`grpquota` or a key ending `_hardlimit` ⇒ enabled /
enforced / `tmpfs_quota_option`": MATCH.**
Every printable quota key is covered by the condition, and any hit implies at least one loaded
quota type with usage+limits enabled, so mount-level `enforced` is sound. Two flagged nuances:

1. `quota` is a **dead key**: parse-only, never appears in mountinfo super options. Harmless to
   the verdict (pure disjunction; a `quota`-mounted fs also always emits `usrquota` AND
   `grpquota`), but fixtures/oracles must not expect `quota` inside `quota_option_keys`.
2. `_hardlimit` keys can appear without their matching type flag (see asymmetry above). Verdict
   unaffected; per-type limit enforcement is NOT implied by a hardlimit token — the contract
   claims mount-level enforcement only, which holds.

**Row 2 — "none of them ⇒ disabled / `tmpfs_quota_options_absent`": SOUND as an inference**
(proof: no-false-negative direction inverted — zero quota tokens ⇒ no type ever loaded on a
visible mounted tmpfs). One-way caveat: with `CONFIG_TMPFS_QUOTA=n` tmpfs prints zero quota keys
ever, so the probe must read `disabled` even though the mechanism is not compiled in ("absent"
conflates with "off"; can never yield a false `enabled`). Gate is open on this host series:
Arch official `7.2.11-arch1` config has `CONFIG_TMPFS_QUOTA=y` (`arch-config.x86_64:11443`,
`CONFIG_QUOTA=y:11360`, `CONFIG_TMPFS=y:11439`).

Value note: hardlimit tokens carry numeric values in mountinfo
(`usrquota_block_hardlimit=1073741824`); the contract's `quota_option_keys` = "keys only, never
values" correctly handles this.

## 4. Confidence and residual unknowns

- High: every claim above is sourced from fetched `v7.2` text with line cites; `shmem.c`
  digest-cross-checked against two independent mirrors; tag existence confirmed by HTTP 200 on
  `h=v7.2` from kernel.org.
- Not read (non-quota context, verdict-irrelevant): `shmem_show_mpol` NULL behavior, exact
  `shmem_default_max_blocks/inodes` values; unimportant for the tmpfs rows.
- [INFERENCE, marked]: whether every deployed kernel in scope is ≥6.6-series with the same
  layout was not verified beyond Arch's current config; older kernels without tmpfs quota fall
  under the `CONFIG_TMPFS_QUOTA=n` caveat.
