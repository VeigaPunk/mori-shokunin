# SrcBtrfsQgroup — btrfs qgroup sysfs call sites re-open (round 23, C2 source)

Seat: `MadoR22-2.SrcBtrfsQgroup-8` (leaf source re-opener). Contract read in full at
`.ufo/waves/round-23/contract.md`, frozen revision
`4dc80c1be48308075e83af17f15fbfe7e95e6cb8` (`git rev-parse` resolves; file sha256
`2bb35aefb08d3fafc467260f859453c0f096effe18b2446503f2b2ee87fe69e7`).

Detection/report only. `corpus/SOURCES.md` not edited. No candidate implementation
(`.ufo/waves/round-23/build/ImplQuota/`, `.scratch/round23/ImplQuota`), no
`cases-proposed/`, no `build/OracleQuota/` file was opened. No installs or upgrades. No
live host probes: the only network reads are the source fetches below; local copies live
under `.scratch/round23/SrcBtrfsQgroup/`.

## Fetch identity

| Fact | Value |
|---|---|
| URL | `https://raw.githubusercontent.com/torvalds/linux/v7.2/fs/btrfs/qgroup.c` |
| Method | `curl -sSfL` into `.scratch/round23/SrcBtrfsQgroup/qgroup.c` |
| Fetched | 2026-10-21 |
| Bytes / lines | 139049 / 4989 |
| **SHA-256 (fetched bytes)** | `121a0af27f9553a9749c837536d618e2ea50d44ce54b30b032fa56e6f3df6ed5` |
| Annotated tag object | `237a1c39e8dfd3e1c6f1f023eea37a48ec04cc63` (`refs/tags/v7.2`, GitHub API) |
| Tag target commit | `8d3ae59288f1e7d58d76558a6ee96d533bc5019f` (`object.type=commit`) |
| Fetch at target commit | `https://raw.githubusercontent.com/torvalds/linux/8d3ae59288f1e7d58d76558a6ee96d533bc5019f/fs/btrfs/qgroup.c` — `cmp` clean, same SHA-256 |

Raw URL bytes are bound to the tag target commit, not a mutable branch ref.

Supporting files fetched for this report (not part of row S080's citation set unless
noted): `fs/btrfs/sysfs.c` sha256 `ce146120f29ac29c0bc1859f21e4b84da91a536df2ec9fd2fa5649144f731c43`
(this is S079's file), `fs/btrfs/disk-io.c` sha256
`aa40ed0700e8de5a9fa7f7c5651994e5eb8b4f5ade84b8010cd5220664d7b292`, `fs/btrfs/messages.h`
sha256 `92ac58d6052272ef9567a8b03901945c041da51f48777f465bef408ec402c75c`,
`fs/btrfs/Kconfig` sha256
`dfc4add66fcde8c4cf3864df26f257def66e33f6a2db5c69b0c237f20b252236` (the last two from
`git.kernel.org/.../plain/...?h=v7.2` after a GitHub 429).

## Anchor verification — CONFIRMED, exact

Declared anchor: `btrfs_sysfs_add_qgroups`/`btrfs_sysfs_del_qgroups` call sites at
~441, ~1032, ~1295. All exact; `qgroup.c` contains exactly five direct call sites.

| Line | Enclosing function (extent) | Role |
|---|---|---|
| 441 | `btrfs_read_qgroup_config` (420–624) | add, mount-time status read; guarded by `if (!fs_info->quota_root) return 0;` at 432 |
| 620 | same, `out:` error branch | del on status-read error; caller `disk-io.c:3726` treats the negative return as fatal mount failure |
| 689 | `btrfs_free_qgroup_config` (667–690) | del on close/teardown and `btrfs_quota_disable()` (comment 663–666 names all three callers) |
| 1032 | `btrfs_quota_enable` | add, before the enable transaction; skipped if `fs_info->quota_root` already set (1029–1030) |
| 1295 | same, `out:` error branch | del on enable failure |

The repeated-add comment anchor is exact at 1045–1047: a second
`btrfs_sysfs_add_qgroups()` "returns 0 (success) when the sysfs entries already exist".
`sysfs.c` defines del at 2567–2583 and add at 2586–2620; the kobject is named `qgroups`
under `&fs_info->fs_devices->fsid_kobj` (2588, 2604–2605), matching the contract's
`/sys/fs/btrfs/<uuid>/qgroups` path comment at 2453.

Enable/disable ordering around those call sites (all observed, same file):

- 444–445: `qgroup_flags` defaulted to 0 "in case no status key is found".
- 453–482: status item parsed; 470–474 `old qgroup version, quota disabled` → `goto out`
  with `ret == 0`; 476 loads `qgroup_flags`; 613–615 sets `BTRFS_FS_QUOTA_ENABLED` only
  when `BTRFS_QGROUP_STATUS_FLAG_ON` is set.
- 1104: `fs_info->qgroup_flags = BTRFS_QGROUP_STATUS_FLAG_ON` set inside the enable
  transaction, before commit; 1256: `set_bit(BTRFS_FS_QUOTA_ENABLED, ...)` after commit.
- 1367: `clear_bit(BTRFS_FS_QUOTA_ENABLED, ...)` at the start of quota disable;
  1403–1409 clears `quota_root`, `FLAG_ON`, `FLAG_SIMPLE_MODE`; 1411
  `btrfs_free_qgroup_config()` → 689 del; 1413–1419 quota tree cleaned and root deleted.

`sysfs.c` state attributes (S079's file, cited here only as needed): `enabled` (2355–2368)
emits `0`/`1` from `qgroup_flags & BTRFS_QGROUP_STATUS_FLAG_ON`; `mode` (2370–2395)
begins with `ASSERT(btrfs_qgroup_enabled(fs_info))` at 2378 and emits `qgroup\n` (2381) or
`squota\n` (2384). The attribute group at 2455–2461 makes both files exist as soon as the
`qgroups` kobject exists.

## Located quote supporting the §C2 rule it backs

> "Called when qgroups get initialized, thus there is no need for locking"
> — `fs/btrfs/sysfs.c:2585`, immediately above `btrfs_sysfs_add_qgroups` at 2586; 12 words.

This is what backs the contract's `btrfs_qgroups_dir_present` basis: the directory is the
`qgroups` kobject, created when qgroup configuration is initialized. It supports the
premise ("presence means qgroup sysfs was initialized"), not the inferred quota state.

For the other direction, the teardown comment is equally exact:

> "This is called from close_ctree() or open_ctree() or btrfs_quota_disable()"
> — `fs/btrfs/qgroup.c:664`, on `btrfs_free_qgroup_config`; 15 words; the del is at 689.

## Verdict on the contract §C2 row

Rule under test, contract lines 115–116:

> `| btrfs | source basename maps to exactly one uuid whose qgroups is true | enabled | unknown | btrfs_qgroups_dir_present |`
> `| btrfs | … exactly one uuid, qgroups false | disabled | n/a | btrfs_qgroups_dir_absent |`

and the real-mode input rule at line 80 ("reading `/sys/fs/btrfs/<uuid>/qgroups/mode` if
present"), plus line 128 (`btrfs_qgroups_mode` = the mode text or null) and line 138
("btrfs qgroup presence ≠ any limit set").

**Verdict: under-determines the row as written. It supports `dir absent → disabled`; it
does not support `dir present → enabled`, and the same source exhibits reachable states
that contradict that direction. It also contradicts the unconditional `mode` read.**

| Clause | Source verdict | Basis |
|---|---|---|
| exactly one uuid, `qgroups` false → `disabled` | SUPPORTED at steady state | add is called at mount whenever `quota_root` exists (441, 432); del runs only on status-read error (620, and then the mount fails), qgroup-config free/teardown or quota disable (689, 664, 1411), and enable failure (1295). A successfully mounted fs with no directory therefore has `BTRFS_FS_QUOTA_ENABLED` clear |
| exactly one uuid, `qgroups` true → `enabled` | NOT SUPPORTED; contradicted as a general rule | 441 adds before the status item is parsed; 444–445 and 470–474 leave the directory present with quota off and the mount succeeding; 1032 adds before 1104/1256 in the enable path; 1367 clears the bit before 1406/1411/689 in the disable path |
| `enforcement: unknown` for btrfs | CONSISTENT | presence of the `qgroups` kobject and its attributes carries no limit information; nothing in these paths reads or implies per-qgroup limits |
| line 80: read `qgroups/mode` "if present" | CONTRADICTED as an unconditional rule | `qgroup_mode_show` asserts `btrfs_qgroup_enabled` (sysfs.c:2378); `ASSERT` expands to `BUG()` when `CONFIG_BTRFS_ASSERT=y` (`messages.h:142–155`; option at `Kconfig:74–83`, default N). With asserts off the read returns 0 bytes after `unexpected qgroup mode` warning (2386–2389) |
| line 128: mode text | PARTIALLY SPECIFIED | real reads yield `qgroup\n` or `squota\n`, newline included; the fixture schema's `qgroups_mode` examples (`"qgroup"`, `"squota"`) carry none |
| line 138: presence ≠ any limit set | SUPPORTED | the directory and attributes exist with no limit items; limit state is per-qgroup files, not this kobject |

Findings, in order of consequence:

1. **Presence is not equivalent to enabled; the mount path can leave the directory with
   quota off.** `btrfs_read_qgroup_config` adds the sysfs group at 441 immediately after
   confirming `quota_root` exists, then defaults `qgroup_flags` to quota-off (444–445) and
   sets the enabled bit only if the on-disk status item carries `FLAG_ON` (613–615). Two
   normal-return paths never set the bit and never del the directory: no status key found
   (loop ends positive, `return ret < 0 ? ret : 0` at 623 yields 0) and
   `old qgroup version, quota disabled` (470–474, `ret` still 0). Mount then succeeds
   (`disk-io.c:3726` only fails on a negative return), so a mounted btrfs path can see
   `qgroups` present while quota is disabled. [INFERENCE] these branches are defensive and
   need damaged or old metadata; I did not reproduce one. The code path is observed, the
   frequency is not.

2. **Two runtime windows have the same shape, independent of metadata damage.** During
   enable, the directory exists from 1032 but the enabled bit is set only at 1256 after
   the transaction commits (with `FLAG_ON` written at 1104 before commit). During disable,
   the bit is cleared at 1367 while the directory survives until 1411 → 689, and the
   `enabled` attribute keeps reporting 1 until `FLAG_ON` is cleared at 1406. The contract's
   `limits` already exclude enable/disable/remount races, so these windows do not by
   themselves invalidate the classification on a quiescent fs; they do mean presence is
   evidence of initialization, not of state.

3. **Reading `mode` is not a read-only-safe operation under the frozen input list.** The
   mode show function asserts that quota is enabled (2378). Since the contract authorizes
   only directory listings under `qgroups` and the `mode` content (line 79–80), a probe
   cannot first read `qgroups/enabled` to gate the read, and even gating on `enabled` would
   not close the window because `enabled` tracks `FLAG_ON` (2363) while the assert tracks
   `BTRFS_FS_QUOTA_ENABLED` (qgroup.c:33–41), and the two are set/cleared at different
   points (1104 vs 1256; 1367 vs 1406). On a `CONFIG_BTRFS_ASSERT=y` kernel the probe can
   therefore panic the host while merely reading an attribute; on a default kernel it gets
   an empty value with a warning. This is the one item I would treat as blocking for the
   probe design rather than as a wording issue.

4. **Mode value domain.** `mode` emits only `qgroup` (full) or `squota` (simple), each with
   a trailing newline (2381, 2384); there is no `disabled`/`full`/`simple` spelling. Any
   sealed case that supplies `qgroups_mode` other than those two strings is encoding a
   value the kernel cannot produce. The fixture schema cannot exercise the newline
   difference, so a real-mode probe that does not normalize trailing whitespace will emit
   `"qgroup\n"` where fixture cases expect `"qgroup"`; the sealed suite would not catch it
   [INFERENCE from the schema at contract line 89 and the emit at 2381/2384].

5. **Basis names are accurate; the state word is not.** `btrfs_qgroups_dir_present` /
   `btrfs_qgroups_dir_absent` describe exactly what is observed (the kobject's existence).
   Attaching `quota_state: enabled` to presence reads a stronger fact than this source
   establishes. The `enabled` attribute (2355–2368) is the source's own, non-asserting
   state surface, and it is not in the contract's authorized input list.

6. **The real control in the contract is compatible with this source.** Fleet root → btrfs
   with `btrfs_qgroups_dir_absent` → `disabled` is the direction the source supports. The
   `enforcement: unknown` and "presence ≠ limit" declarations also match.

## Tier and scope I would assign

**Tier A, narrow scope — qgroups sysfs kobject lifecycle only.**

Proposed scope text: "the btrfs code paths that create and destroy
`/sys/fs/btrfs/<uuid>/qgroups` at tag v7.2: the kobject is added when the quota-root
status is read at mount (`qgroup.c:441`) and when quota is enabled (`:1032`), and is
removed on status-read error (`:620`), on qgroup-config free including quota disable
(`:689`, caller comment `:663–666`), and on enable failure (`:1295`); therefore absence of
the directory on a successfully mounted filesystem means quota is not enabled, while
presence means the qgroup sysfs group is initialized and does not by itself prove that
quota is enabled; the `enabled` attribute reports the on-disk ON flag and the `mode`
attribute asserts quota enabled before emitting `qgroup` or `squota`."

Rationale for A: primary upstream kernel source, byte-bound to annotated tag `v7.2` and
its target commit, no secondary mediation. Rationale for the narrowing: at this scope the
file is authoritative about the lifecycle and ordering it implements; it is not evidence
for `quota_state: enabled` from directory presence alone.

If L1 tiers by strength of support for the *contract row as written*, the row's
present→enabled arm is **C at best** (not supported, with counterexamples in the same
file) while the absent→disabled arm is **A**. A single letter for the row should be **A
with the narrowed scope above**, and the contract should not cite S080 for `enabled`.

Recommendation for L1 (no action taken here): either (a) keep the probe's btrfs state
derived from `qgroups/enabled` (authorize reading that one file) and only then read
`mode`, accepting that the enable/disable windows remain; or (b) classify btrfs from
directory presence as `quota_state: unknown` when present, reserving `disabled` for
absence; or (c) drop the `mode` read entirely and report `btrfs_qgroups_mode: null` in
real mode. The sealed cases and the real control would need to be re-derived under
whichever option is chosen; the current combination (presence → enabled, unconditional
mode read) is the one combination the source does not support.

Cross-row note: draft row S079 (`fs/btrfs/sysfs.c`) says its presence "is evidence that
quota accounting is on". The `enabled` attribute in that same file is the ON-flag surface,
and presence is not wired to it; I record the tension, I did not edit that row.

## Residual gaps (not resolved here)

1. Reachability rate of the old-version / missing-status-key paths on real v7.2
   filesystems: code paths observed, frequency not measured (marker: [INFERENCE]).
2. Whether the host kernel in use compiles `CONFIG_BTRFS_ASSERT`: not checked; live kernel
   config probes are outside this seat's permitted reads. The BUG risk is conditional on
   that option (Kconfig default N), not universal.
3. `btrfs_sysfs_add_qgroups`'s `btrfs_is_testing()` early return (sysfs.c:2593–2594) is
   test-only; I did not trace what creates the kobject in kernel selftests.
4. I did not open `fs/btrfs/ioctl.c` to enumerate the ioctl entry points that reach
   `btrfs_quota_enable`/`btrfs_quota_disable`; qgroup.c shows the sequencing, not the
   command surface.
5. The device→uuid mapping (`/sys/fs/btrfs/<uuid>/devices/`) is S081/S079 scope; this
   report confirms only that the `qgroups` kobject is per-`fs_devices` (sysfs.c:2588,
   2604–2605), so the contract's uuid→qgroups lookup has the right level.
