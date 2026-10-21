# ConnSoujiKama — sibling overlap scan (mori round 23, wave 1)

STATUS: complete. Read-only. No writes outside this report; no installs/upgrades; no live host
probe; no session transcript read; no sibling mutation or dispatch. Every sweep below excluded
`.git/`, `.ufo/interactive-sessions/` and `agent.db`.

## Axes

- **C1 calibration** (score 5): untouched by everything in this report.
- **C2 coverage / FR2 quota-EDQUOT observability** (score 6): the frozen real-control provenance
  and the verdict's scope are the only surfaces the sibling evidence can affect.

## 1. Exact sweep and counts

Roots (absolute, read-only):

- `/home/vgpnk/Projects/shokunin/souji-shokunin`
- `/home/vgpnk/Projects/shokunin/kama-shokunin`
- `/home/vgpnk/Projects/shokunin/kumitate-shokunin`

Tool: ripgrep 15.1.0. Canonical command (hit count; `-l` yields the file count):

```sh
rg -n -i --hidden --no-ignore --no-messages \
  -g '!.git/**' -g '!**/.ufo/interactive-sessions/**' -g '!**/agent.db' \
  -e '<PATTERN>' /home/vgpnk/Projects/shokunin/<repo> | wc -l
```

`--hidden` is mandatory: without it `.ufo/` is skipped and the counts are understated (kama's
union falls from 338 to 11). `--no-ignore` keeps gitignored wave artifacts in scope.

Union pattern:
`quota|tmpfs|\bdf\b|mount|runway|ENOSPC|EDQUOT|statvfs|f_bavail|free space|disk space|qgroup|noquota|mountinfo`

| repo | hits | files |
|---|---|---|
| souji-shokunin | 886 | 425 |
| kama-shokunin | 338 | 191 |
| kumitate-shokunin | 68 | 50 |

Per-token counts, same flags, `hits/files`:

| pattern | souji | kama | kumitate |
|---|---|---|---|
| `quota` | 320/160 | 68/51 | 31/17 |
| `tmpfs` | 83/33 | 5/5 | 0/0 |
| `\bdf\b` | 46/26 | 10/6 | 0/0 |
| `\bmount` | 393/237 | 121/107 | 33/30 |
| `runway` | 27/11 | 2/2 | 2/2 |
| `ENOSPC\|EDQUOT` | 9/6 | 9/7 | 3/3 |
| `Disk quota exceeded` | 64/40 | 0/0 | 0/0 |
| `statvfs\|f_bavail` | 0/0 | 49/2 | 0/0 |
| `qgroup` | 0/0 | 0/0 | 0/0 |
| `noquota` | 0/0 | 0/0 | 0/0 |
| `mountinfo` | 0/0 | 0/0 | 0/0 |
| `/proc/mounts` | 0/0 | 0/0 | 0/0 |
| `xfs` | 10/10 | 7/6 | 2/2 |
| `findmnt` | 5/3 | 2/1 | 2/2 |
| `usrquota\|grpquota\|prjquota\|qnoenforce\|hardlimit` | 0/0 | 0/0 | 0/0 |
| `df -h\|df -i\|df -T\|df -P` | 12/10 | 2/1 | 0/0 |
| `Filesystem` (noise control) | 1037/230 | 293/123 | 22/20 |

Tracked-only baseline for the same union (`git -C <repo> grep -I -n -i -E … -- .`):
souji 742/405, kama 323/184, kumitate 64/48. The working-tree numbers are quoted above because
untracked wave artifacts carry the same-day observations.

False positives to discount: kumitate's 3 `ENOSPC` hits are the substring in `fencedQuoteSpans`
(`/home/vgpnk/Projects/shokunin/kumitate-shokunin/scripts/cite-check.mjs:2247`, plus two selftest
dumps); kama's 49 `statvfs|f_bavail` hits are two captured CPython doc pages
(`/home/vgpnk/Projects/shokunin/kama-shokunin/.ufo/waves/round-22/residual/FinalSources/raw/os.html`,
`/home/vgpnk/Projects/shokunin/kama-shokunin/.ufo/waves/round-22/residual/FinalSources/raw/os.txt`)
in a round-22 source bundle, not a probe; souji's `xfs` hits are `/tmp/swarm-wave-xfSwGv` filenames
and a base64 blob; kumitate's `runway` hits are manifest-queue runway
(`/home/vgpnk/Projects/shokunin/kumitate-shokunin/corpus/knowledge/reconcile-and-cycle.md:219`,
`/home/vgpnk/Projects/shokunin/kumitate-shokunin/SKILL.md:190`), not disk; most kama/kumitate
`quota` hits are provider/model quota (kimi quota lanes, "weekly usage quota exhausted"), not disk.

## 2. Overlaps found

### O1 — `/tmp` is xfs on `/dev/nvme0n1p1` (corroborates the frozen C2 `/tmp` row)

- `/home/vgpnk/Projects/shokunin/kama-shokunin/corpus/lessons/round-19-verifier-spotcheck.md:121`
  (commit `37bd4c5`, 2026-10-21T04:05:09-03:00): "5.95 GiB on disk (`/tmp` is xfs, not tmpfs)."
- `/home/vgpnk/Projects/shokunin/kama-shokunin/.ufo/waves/round-21/falsify/advice/C2DigestSentinel.md:43`
  (commit `1027146`, 2026-10-21T09:32:52-03:00): "Tested on XFS /tmp with glibc 2.44".
- `/home/vgpnk/Projects/shokunin/kama-shokunin/.ufo/waves/round-23/falsify/advice/ExecLocaleArms.md:109`
  (commit `0df800e`, 2026-10-21T14:20:00-03:00): "`/tmp` (`/dev/nvme0n1p1`, xfs, 128G) was full".

This independently matches `frozen/c2-expected-real.json`'s `/tmp` row (fstype `xfs`,
mount_point `/tmp`, device `259:1` = `/dev/nvme0n1p1`). Kama observed it, not mori, at three
points on 2026-10-21.

### O2 — `/tmp` was tmpfs until 2026-10-20 (the frozen drift note is live, not theoretical)

- `/home/vgpnk/Projects/shokunin/souji-shokunin/census/round-12/scout-surfaces.md:92-103` (commit `d7266c5`,
  2026-10-19T19:24:49-03:00): `df -T /home /var/tmp /tmp` prints
  `/dev/mapper/root btrfs … /home`, `/dev/mapper/root btrfs … /`, `tmpfs tmpfs … 11% /tmp`;
  `stat -c '%d %m %n'` prints device 30 for the `/home` paths, 31 for `/var/tmp`, 57 for `/tmp`.
- `/home/vgpnk/Projects/shokunin/kama-shokunin/.ufo/waves/round-12/advice/ReviewSelftest.md:20` (commit `33f4668`,
  2026-10-20T01:35:52-03:00): "`/tmp` is tmpfs (writable, not inside any git worktree)."
- `/home/vgpnk/Projects/shokunin/souji-shokunin/.ufo/waves/round-13/w1/SafetyOperator.md:19` (commit `6ed10a7`,
  2026-10-20T02:34:39-03:00): "`/tmp` and `/dev/shm` are tmpfs".
- Same commit, `/home/vgpnk/Projects/shokunin/souji-shokunin/.ufo/waves/round-13/w1/ReviewSize.md:29`: "`/var/tmp` device 31, `/home` device 57 (`stat -c %d`) …
  Mount options for `/var/tmp` were not probed (`findmnt` printed nothing)".

Transition window: after 2026-10-20T02:34 and by 2026-10-21T04:05 (at most 25.5 h wide), ending
~10 h before the contract froze at 2026-10-21T13:59. The contract's note ("Host state may change
(remount, quota enable); a later differing run is a drift observation") is empirically justified.

### O3 — FR2 witness: EDQUOT with free space and a silent `quota -s`

The historical positive is in souji: 64 `Disk quota exceeded` hits in 40 files, 2026-10-18..20.

- `/home/vgpnk/Projects/shokunin/souji-shokunin/census/round-6/final-116.json:192` (commit `b5db5cf`, 2026-10-18T18:00:38-03:00):
  "tmpfs 16G size, 13G used, 3.1G avail, 80% — filesystem not full; git still reported Disk quota
  exceeded. quota -s printed nothing. Which quota rejected the write is uncertain."
- `/home/vgpnk/Projects/shokunin/souji-shokunin/census/round-6/final-94.json:125`: "df showed tmpfs 3.1G free; the write still failed."
- `/home/vgpnk/Projects/shokunin/souji-shokunin/census/round-10/seat-04.json:159`: "The host /tmp DISK QUOTA is active: a bare `--selftest`
  without TMPDIR=/var/tmp fails with 'Disk quota exceeded'".
- `/home/vgpnk/Projects/shokunin/souji-shokunin/census/round-8/final-21.json:77`: `/tmp` at 13G/16G (80%), dominated by other lanes' fixtures.

This is exactly C2's claim shape (df capacity does not see quota refusal) and it happened on this
host. But the mount options were never recorded (see §4.2), so the `enabled` basis of that incident
is not reconstructable from sibling bytes.

### O4 — same-day `/tmp` 100 % full *on the xfs/noquota mount* (capacity counterexample)

`/home/vgpnk/Projects/shokunin/kama-shokunin/.ufo/waves/round-23/falsify/advice/ExecLocaleArms.md:109-112` and its artifacts
(`/home/vgpnk/Projects/shokunin/kama-shokunin/.ufo/waves/round-23/falsify/out/ExecLocaleArms/tmp-enospc-observed.txt`, `/home/vgpnk/Projects/shokunin/kama-shokunin/.ufo/waves/round-23/falsify/out/ExecLocaleArms/tmp-df-at-rerun.txt`, mtime 2026-10-21 12:58:51):

```
df -h /tmp:  /dev/nvme0n1p1  128G  128G  3.3M  100%  /tmp
df -i /tmp:  /dev/nvme0n1p1  Inodes 9401856  IUsed 9388926  IFree 12930  IUse% 100%
12 of 37 fixtures failed with "No space left on device"
later:       /dev/nvme0n1p1  128G  111G   18G   87%  /tmp (36,468,346 inodes free)
```

The frozen real control was observed ~1 h later on the same xfs/noquota mount. So on this host
`QUOTA_DISABLED` and a 100 %-full `/tmp` coexist; the probe's green is a quota-mechanism verdict,
not a capacity verdict. The same report attributes the peak to other lanes' scratch:
`/tmp/f14-var` 16G, `/tmp/tsukuroi-r17-boot` 2.9G, `/tmp/kama-r23` 1.7G, `/tmp/kama-r23w2` 5.4G
(left untouched). That is a live runway observation on the exact path C2 classifies `disabled`.

### O5 — btrfs `/home` mount and unstable anonymous `st_dev`

- `/home/vgpnk/Projects/shokunin/souji-shokunin/.ufo/waves/round-13/w1/AttackBounds.md:171`: "`/home` is btrfs `@home` and `/var/tmp` is btrfs `@` (findmnt),
  so they are separate subvolumes." This corroborates the frozen `mount_point: /home` row and the
  `btrfs_subvolume_skipped` design.
- `/home/vgpnk/Projects/shokunin/souji-shokunin/.ufo/waves/round-14/w1/SafetyCache.md:45` (commit `48f8945`, 2026-10-20T04:54:42-03:00): "The lane and
  `tools/` are btrfs `@home` with st_dev 57 throughout."
- But `/home/vgpnk/Projects/shokunin/souji-shokunin/census/round-12/scout-surfaces.md` (19:24 the previous evening) recorded device 30 for the same `/home`
  paths. Anonymous btrfs `st_dev` moved 30 → 57 within ~7 h without a visible mount change.

### O6 — kumitate adjacencies (no disk-quota overlap)

- `/home/vgpnk/Projects/shokunin/kumitate-shokunin/.ufo/waves/round-35/evidence/ExecS8Fidelity.patch:290` (commit `4c9e407`,
  2026-10-20T23:35:06-03:00): test roots are drawn outside the repo "because the fleet TMPDIR can
  be in-repo when the system temp mount is quota-dead." The rationale is proposed wave-35 prose:
  `/home/vgpnk/Projects/shokunin/kumitate-shokunin/tests/helpers/tmp-roots.mjs` and `/home/vgpnk/Projects/shokunin/kumitate-shokunin/scripts/ufo-swarm-wave.test.mjs` are absent at HEAD and the
  falsify note (`/home/vgpnk/Projects/shokunin/kumitate-shokunin/.ufo/waves/round-35/falsify/SecUfoSwarmWaveTest.md:94`) records the sentence as not retained at master/pin.
- `/home/vgpnk/Projects/shokunin/kumitate-shokunin/.ufo/waves/round-36/build/CriticPinSemantics.md:68` (commit `3d5760a`,
  2026-10-21T02:42:21-03:00): "findmnt /fast → xfs (persistent; no tmpfiles rule for /fast)".
  `/fast` is outside C2's paths; it is a mount observation, not a quota probe.

## 3. Capability overlap: none

- Zero hits in all three repos for `mountinfo`, `/proc/mounts`, `qgroup`, `noquota`, and every
  quota mount-option token (`usrquota`, `grpquota`, `prjquota`, `*qnoenforce`, `*hardlimit`).
- Zero tracked filenames matching `quota|mount|df` in any of the three.
- No sibling imports or shells a quota/statvfs API; kama's only `statvfs` text is captured CPython
  documentation.
- Provenance is consistent: souji refuses host-OS/process surfaces and routes runway to mori;
  kumitate owns dispatch/worktree locking. `tools/mori-quota-surface.py` has no competing
  implementation and no sibling authority to reconcile.

## 4. Contradictions, stated rather than smoothed

1. **tmpfs vs xfs is time-separated, not a live conflict.** Sibling records agree with the frozen
   row once dated (O1/O2). No sibling contradicts the frozen `/tmp` tuple at its observation time.
2. **The historical positive is unreconstructable.** No sibling recorded `/proc/self/mountinfo` or
   super options (0 hits; souji states mount options "were not probed"). The EDQUOT-when-free
   incident cannot be replayed to decide whether a mount-option reader would have said
   `enabled`; only sealed synthetic cases can exercise that branch.
3. **Both frozen default paths are `disabled`.** The only live `enabled` surface the contract
   itself observed is `/dev/shm` (tmpfs `usrquota`), explicitly outside the default paths. At
   freeze time C2's positive `QUOTA_ENABLED` verdict has no live witness, only synthetic cases.
4. **btrfs mismatch is not uniquely S081.** The `/home` anonymous `st_dev` changed 30 → 57 across
   two sibling observations of the same subvolume set. A mount-dev/st_dev mismatch can be
   per-subvolume numbering *or* anon-number reassignment across remounts. The contract's
   `btrfs_subvolume_skipped` handling is safe (it claims no match); the causal narrative should
   not attribute the frozen mismatch solely to per-subvolume nesting.
5. **`QUOTA_DISABLED` ≠ capacity OK.** On the same xfs/noquota `/tmp`, a sibling recorded 100 %
   bytes, 100 % inodes and 12/37 ENOSPC fixture failures before 2026-10-21T12:58 (at least ~1 h
   before the freeze). A green `QUOTA_DISABLED` read as runway clearance would be false.

## 5. Proposed move (one, bounded)

**Make C2's real control a dated witness ledger, not a lone snapshot: keep the frozen two-path
tuple as the sole predicate, add two non-scoring witnesses, and bound the verdict in the fixed
`limits` text.**

- **W1 (coverage, live positive branch).** At measure time, run the tool once more with
  `--path /dev/shm` and record it as a `supplement`, not a requirement. The frozen note already
  records `/dev/shm` as tmpfs `usrquota`; under the contract table that is
  `enabled`/`enforced`/`tmpfs_quota_option`, exit 1 `QUOTA_ENABLED`. This is the only live surface
  where the positive verdict can be shown; the default paths can only show `disabled`.
- **W2 (calibration, scope).** Record O4 as the counterexample in the C2 evidence/lesson and add
  one sentence to the fixed `limits` text: "QUOTA_DISABLED is a quota-mechanism observation, not a
  capacity verdict; df/ENOSPC remains the capacity signal."
- Nothing else changes: `c1-*` untouched, `c2-expected-real.json` bytes untouched, no schema/key/
  exit/finding-id change, no sealed predicate change, no privileged call, no new live read in this
  wave.

Why non-obvious: the contract frames `QUOTA_ENABLED` as the runway finding and makes the real
control a two-path `QUOTA_DISABLED`. On this host that green is the *only* thing the real control
can produce, while the same mount was full an hour earlier and the fleet's historical EDQUOT
witness belongs to a `/tmp` that no longer exists. The sibling corpus supplies both the missing
negative control and the only live positive surface.

Affected axes: **C2 coverage** improves (positive branch has a live witness; the verdict's scope is
bounded by same-host evidence). **C1 calibration is untouched.** Verification and substrate: no
predicate or schema change; W1 is non-scoring by construction.

## 6. Risks

- A sealed case might pin the `limits` bytes (the contract defines "fixed boundary text", not its
  bytes). Check `frozen/quota-cases/` first; if pinned, put the sentence in docs only.
- Promoting W1 to a requirement would be an unregistered contract change. If `/dev/shm` differs at
  measure time, record drift; do not rewrite the oracle.
- W2 must not be read as the tool measuring capacity; the sentence says the opposite, and no `df`
  field is added.
- `/dev/shm` can be remounted; a changed supplement is drift, not a probe failure.
- The kama `/tmp` event is a capacity/inode event, not EDQUOT. It supports the scope caveat, not
  C2's quota claim; do not cite it as quota evidence.

## 7. Verification (for L1; this seat ran none)

- Before integrating W2: `rg -n 'limits' .ufo/waves/round-23/frozen/quota-cases/` (directory not
  yet populated at scan time) and confirm no case pins the text.
- After integration: default-pair output vs `frozen/c2-expected-real.json` (exit 0,
  `QUOTA_DISABLED`, per-path tuple); run `--path /dev/shm` separately and record the tuple; confirm
  schema `mori-quota-surface-v1` and key set unchanged.
- Re-run the canonical sweep; expected union counts 886/425, 338/191, 68/50, or record the delta
  with its cause.

## Installs and updates

None. No pacman, uv, npm, cargo, or release-binary activity.
