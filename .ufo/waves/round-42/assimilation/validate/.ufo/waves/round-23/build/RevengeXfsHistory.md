# RevengeXfsHistory — has xfs_showargs always printed noquota when no quota accounting is active?

Seat: `MadoR22-2.RevengeXfsHistory-8` (leaf, no subagent dispatch) · 2026-10-21 · lane r23, contract frozen at `4dc80c1be48308075e83af17f15fbfe7e95e6cb8`
Mission: reconstruct the history of the xfs mount-options display rule behind C2's xfs classification table (`tools/mori-quota-surface.py` probe, FR2), specifically the rows `xfs_noquota_option → disabled` and `xfs_quota_options_absent → unknown`. Detection and report only.

## Axes (godspeed)

1. Tag breadth — every 2.6.x git release tag (v2.6.12–v2.6.39, exhaustive) + sampled 3.x/4.x/5.x/6.x releases + master.
2. Guard fidelity — the exact guard condition on the `noquota` print vs. that kernel's full ACCT-bit universe.
3. Transition precision — the first release tag where the rule holds.
4. Rule verdict — is `xfs_quota_options_absent=unknown` right for older kernels.

## Method

Raw fetches from `https://raw.githubusercontent.com/torvalds/linux/<tag>/<path>` only (as assigned), stored under
`.scratch/round23/RevengeXfsHistory/` (114 retained copies — every quoted line below can be re-read there). Pre-git
history (SGI tree, 2.4/2.5) is not reachable in torvalds git (history starts at 2.6.12-rc2, 2005); no claim is made
below v2.6.12. Tools used: system `curl` 8.23.0, system Python 3.14.8 for fetch/re-extract scripting. **Installs: none.**
No live host reads, no /tmp, no lane VCS mutation, no reads of `.ufo/waves/round-23/build/ImplQuota/`,
`.scratch/round23/ImplQuota`, `cases-proposed/`, or `build/OracleQuota/`; no session-transcript reads.

Files per tag: `xfs_super.c` (path `fs/xfs/linux-2.6/` up to v3.0, `fs/xfs/` from v3.2), `xfs_vfsops.c` (2.6.x),
plus headers for the flag universe: `xfs_quota.h`, `libxfs/xfs_log_format.h`, `xfs_log_format.h`, `libxfs/xfs_quota_defs.h`.

## Reconstruction

Three eras. The display code's location moves, but the content rule is what matters.

### Era 1 — v2.6.12 through v2.6.23: NO quota options printed at all (rule does NOT hold)

For all twelve release tags v2.6.12–v2.6.23 (exhaustive, no gaps), `xfs_showargs` — in `fs/xfs/xfs_vfsops.c`,
reached via `linvfs_show_options` → `VFS_SHOWARGS` (v2.6.12, vfsops:1871; vector at :1951) or `xfs_fs_show_options`
(later tags) — contains **zero** quota output: no `noquota`, and no `usrquota/uqnoenforce/…` when quota IS active.
Full bodies re-read at v2.6.12 (vfsops:1870–1931), v2.6.15 (:1878–1948), v2.6.21 (:1896–1959): they print only
wsync/ino64/logdev/sunit/… style flags. `grep noquota` over all twelve fetched files: 0 hits.

Quota accounting nevertheless existed and could be active in these kernels: `Q_XQUOTAON` quotactl path at
v2.6.12 `fs/xfs/quota/xfs_qm_syscalls.c:142–148`, and on-disk `sb_qflags` quota checks at v2.6.12 vfsops:373–374.
So on era-1 kernels, an xfs mount with quota accounting active is **indistinguishable in mount options from one
without** — option absence carries no information.

### Transition: v2.6.23 → v2.6.24

v2.6.24 is the **first tag where the rule holds**. `fs/xfs/xfs_vfsops.c:2085–2107`:

```c
if (mp->m_qflags & XFS_UQUOTA_ACCT) {  …  usrquota / uqnoenforce }
if (mp->m_qflags & XFS_PQUOTA_ACCT) {  …  prjquota / pqnoenforce }
if (mp->m_qflags & XFS_GQUOTA_ACCT) {  …  grpquota / gqnoenforce }
if (!(mp->m_qflags & XFS_ALL_QUOTA_ACCT))
	seq_puts(m, "," MNTOPT_NOQUOTA);
```

### Era 2 — v2.6.24 through master: rule holds everywhere checked

Per-type options, then exactly `noquota ⟺ (m_qflags & XFS_ALL_QUOTA_ACCT) == 0`. The flag universe is constant
across the whole history: `XFS_ALL_QUOTA_ACCT ≡ XFS_UQUOTA_ACCT | XFS_GQUOTA_ACCT | XFS_PQUOTA_ACCT` — confirmed by
expansion at v2.6.15/v2.6.24/v2.6.27/v3.0/v3.4/v3.10 (`fs/xfs/xfs_quota.h`) and v3.13/v4.19/v6.12/master
(`xfs_log_format.h`; `libxfs/` from the libxfs move). `XFS_PQUOTA_ACCT` exists from the first git tag (v2.6.12
quota.h:152), so the U|G|P universe never grew after v2.6.24 — the guard always covered the complete universe.
The define's *home* moved `xfs_quota.h` → `xfs_log_format.h` (between v3.10 and v3.13) → `libxfs/xfs_log_format.h`;
semantics unchanged.

Structural notes: display moved `xfs_vfsops.c` → `xfs_super.c` between v2.6.24 and v2.6.25; unified path
`fs/xfs/xfs_super.c` by v3.2; function renamed `xfs_fs_show_options` at v5.9 (fs_context API). From v6.12/master the
enforced/non-enforced branch order is flipped (ENFD tested first) but the emitted strings and the noquota rule are
identical (ENFD is set only together with ACCT — mount-translation code, e.g. v2.6.24 vfsops:402–415). [INFERENCE:
ENFD ⊆ ACCT at all eras; directly shown only for v2.6.24's translation code.]

**Per-tag guard table** (guard = the `XFS_ALL_QUOTA_ACCT` if-line; print = following `noquota` seq_puts):

| Tags | Result |
|---|---|
| v2.6.12–v2.6.23 (all 12) | no quota display at all (neither per-type keys nor noquota) |
| v2.6.24 | xfs_vfsops.c guard:2106, print:2107 |
| v2.6.25, v2.6.26 | xfs_super.c guard:517, print:518 |
| v2.6.27, v2.6.28 | guard:545/:545, print:546 |
| v2.6.29 | guard/print 598/599 |
| v2.6.30 | 585/586 |
| v2.6.31 | 592/593 |
| v2.6.32 | 596/597 |
| v2.6.33 | 597/598 |
| v2.6.34 | 598/599 |
| v2.6.35 | 608/609 |
| v2.6.36 | 566/567 |
| v2.6.37, v2.6.38 | 562/563 (both) |
| v2.6.39 | 551/552 |
| v3.0, v3.2, v3.4, v3.7, v3.10 | guard/print 565/566, 566/567, 556/557, 568/569, 577/578 |
| v3.13, v3.15, v3.17, v3.19 | 561/562, 561/562, 554/555, 556/557 |
| v4.1, v4.4, v4.7, v4.10, v4.13, v4.16, v4.19 | 536/537, 535/536, 544/545, 553/554, 554/555, 556/557, 526/527 |
| v5.0, v5.4, v5.9, v5.13, v5.16 | 528/529, 511/512, 220/221, 223/224, 241/242 |
| v6.0, v6.3, v6.6, v6.9, v6.12, v6.15, v6.17, v6.18, master | 244/245, 245/246, 225/226, 227/228, 229/230, 239/240, 240/241, 248/249, 253/254 |

Modern master (`xfs_fs_show_options`, xfs_super.c:238–254) is byte-shape identical to v2.6.24's rule.

**Emitted-token set for real kernels in era 2:** exactly `usrquota, uqnoenforce, prjquota, pqnoenforce, grpquota,
gqnoenforce, noquota`. The plain aliases `uquota/gquota/pquota/quota/qnoenforce` are accepted at *parse*
(v2.6.24 vfsops:1910–1932; v4.7+ `Opt_*` tables) but never emitted by showargs — real /proc/mounts can only contain
the seven tokens above. The display branches are disjoint, so no kernel can emit `noquota` together with any
per-type key.

## Answers

**Q1 — Has xfs_showargs always printed noquota when no quota accounting is active?** No. The claim is false for
v2.6.12–v2.6.23, which print no quota tokens at all (neither when quota is active nor when inactive). The rule
("noquota printed iff zero accounting of any of user/group/project") holds from **v2.6.24** to master — first
holding tag: **v2.6.24**; every later release tag checked (18 remaining 2.6.x exhaustively + 20 modern samples
through master) satisfies it, with no counterexample.

**Q2 — Is `xfs_quota_options_absent=unknown` right for older kernels?** Yes, for every era, for era-specific
reasons:

- Era 2 (≥ v2.6.24): absence is anomalous — such kernels always emit a quota key (`noquota` or a per-type token),
  so absence cannot mean "disabled"; `unknown` is the only sound verdict.
- Era 1 (v2.6.12–v2.6.23): absence is exactly what an *active-quota* mount also looks like (no display existed),
  so mapping absence to disabled would produce false "QUOTA_DISABLED" verdicts; `unknown` is required.

Adjacent contract rows also check out against this history: `xfs_noquota_option → disabled` is sound for era-2
kernels and unreachable from era-1 real mountinfo (era-1 kernels never emit `noquota`, so no false-disabled hazard;
a fixture could still exercise the row safely). `xfs_conflicting_quota_options → unknown` describes a combination no
kernel can emit (disjoint display branches), i.e. it only fires on synthetic/corrupted mountinfo — `unknown` is
right there too. FYI only: the contract's enabled-key list includes parse aliases (`uquota`, `gquota`, `pquota`,
`quota`) that real kernels never print; harmless over-approximation, no contract change implied.

## Confidence and limits

- Tag-level claims: high confidence; direct primary-source evidence, exhaustive over all 2.6.x git tags.
- [INFERENCE] ENFD ⊆ ACCT at all eras (shown directly only for v2.6.24 translation code); does not affect the
  noquota rule, only the enforcement-string commentary.
- Pre-2.6.12 (SGI heritage in 2.4/2.5 pre-git trees) is unreachable via torvalds GitHub raw; not covered by any
  claim above. Minor-series tags between the sampled 3.x–6.x releases were not individually fetched; every sampled
  release across all series holds the era-2 rule, so an unsampled minor-series break is considered unlikely but not
  excluded by direct evidence.
- No candidate implementations, case files, or oracle material were read; independence preserved.

## Evidence index (retained under `.scratch/round23/RevengeXfsHistory/`)

- Era-1 bodies: `v2.6.12__xfs_vfsops.c:1870-1931`, `v2.6.15__xfs_vfsops.c:1878-1948`, `v2.6.21__xfs_vfsops.c:1896-1959`; 0 noquota hits in all 12 era-1 vfsops copies.
- First-holder block: `v2.6.24__xfs_vfsops.c:2085-2107` (display), `:1716-1727` (MNTOPT strings), `:1910-1932` (parse aliases), `:402-415` (ACCT/ENFD translation).
- Era-2 guards: `v2.6.25__xfs_super.c:517-518`, `v3.10__xfs_super.c:577-578`, `v4.19__xfs_super.c:526-527`, `v5.9__xfs_super.c:220-221`, `v6.12__xfs_super.c:229-230`, `master__xfs_super.c:253-254` (and the full table above).
- Flag universe: `v2.6.15__xfs_quota.h:151-152`, `v3.10__xfs_quota.h:166-167`, `v3.13__xfs_log_format.h`, `v4.19__xfs_log_format.h`, `v6.12__xfs_log_format.h` (libxfs), `master__xfs_log_format.h` — all `XFS_ALL_QUOTA_ACCT = (U | G | P)`.
- Era-1 quota activatability: `v2.6.12__xfs_qm_syscalls.c:142-148` (Q_XQUOTAON), `v2.6.12__xfs_vfsops.c:373-374` (on-disk sb_qflags).
