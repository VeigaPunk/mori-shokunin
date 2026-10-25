# ScribeEntryA — C2 entry draft `corpus/knowledge/quota-observability-r48.md` (round 48, wave w1)

Seat: ScribeEntryA (leaf; no subagents dispatched). Lane root: `/home/vgpnk/Projects/shokunin/mori-shokunin`.
All paths in this report are relative to the lane root. Working tree is at the freeze commit
`4387cf94` (entering tip `e5dbac05`).

## Method

1. Read the frozen contract (`contract.md`), `v3-spec.md`, the counter `count-c2.py`
   (P-C2 predicate, COPIES digests, parse logic), and the operator `/home/vgpnk/.omp/agent/RULES.md`
   (no tool installs were needed; nothing was installed).
2. Opened all four committed copies myself:
   - `corpus/evidence/sources-r48/xfs_quota.8.html` (630 lines, man7 rendering of xfs_quota(8))
   - `corpus/evidence/sources-r48/quotactl.2.html` (351 lines, man7 rendering of quotactl(2))
   - `corpus/evidence/sources-r48/errno.h` (127 lines, Linux v7.2 asm-generic errno.h)
   - `corpus/evidence/sources-r48/aliyun-nas-quota.html` (269 lines, Aliyun NAS NFS volume quota guide)
3. Read the staged entry `knowledge/corpus/knowledge/quota-observability-r38.md` after the copies.
4. Ran a substring-test script (pasted below) that: hashes the four copies (binary read,
   matching `git show` bytes) against the frozen digests; normalises each copy exactly as
   `count-c2.py::normalise`; and verifies every quote of the draft at a substring of its
   committed copy with 6–25 whitespace-delimited words.
5. Ran the lane's quota-row sweep at the worktree, freeze, and entering refs; ran live page
   rechecks for the four URLs (read-only fetches).

## Pin evidence (committed copies match frozen sha256)

```
$ for f in xfs_quota.8.html quotactl.2.html errno.h aliyun-nas-quota.html; do sha256sum corpus/evidence/sources-r48/$f; done
6375e40e9c0e950d78b38edbe9b7e7fdf5868d55be07040d4a029c552c437d5f  corpus/evidence/sources-r48/xfs_quota.8.html
0d4ab273503d078ee0d9765c616b5082514e7d86e2c6a6b16c70cb7fba8b6ee8  corpus/evidence/sources-r48/quotactl.2.html
66a5ad60566fdd62e41701bcfc42bfeca5e5696ad1d47d78981575e0c51622be  corpus/evidence/sources-r48/errno.h
747fef1bcc8c6d6c18908f4534879922bebdaece1a476831d48be93c4e22719f  corpus/evidence/sources-r48/aliyun-nas-quota.html
```

All four equal the `COPIES` digests in `count-c2.py` → `pins=ok` will hold at R.
(Investigation note: `aliyun-nas-quota.html` contains two CRLF byte pairs; text-mode reads
alter bytes and produce a different hash — the counter reads via `git show`/binary, so this
is a non-issue, recorded for future tooling.)

## Quote substring verification

Script (`/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r48-ScribeEntryA/check_entry.py`)
mirrors `count-c2.py::evaluate` (same normalise, same cell parsing, same word bounds, same
source-row requirements with a mock SOURCES table of the exact shape the L1 must land for
S479–S482). Run:

```
$ TMPDIR=/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r48-ScribeEntryA \
  python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r48-ScribeEntryA/check_entry.py
pins_ok = True
head_n = 14 | has(source) = True | has(verified-at) = True | has(recheck) = True
header = ['claim', 'source', 'quote'] | rows = 15
claims = 15 | located = 15 | quote_missing = 0 | bad_rows = 0 | sources = 4
source_rows = ok | provenance = ok
ids_in_table = ['S479', 'S480', 'S481', 'S482'] | cited = ['S479', 'S480', 'S481', 'S482']
RESULT: C2=met
```

All 15 quotes occur verbatim in their committed normalised copy; every quote is 6–25 words
and unique; the table uses 4 distinct sources; source cells are bare S-ids; source lines cite
exactly the used ids; `verified-at`/`recheck` are present in the head. The only part I cannot
check myself is the bytes of the real `corpus/SOURCES.md` rows at R — those are the L1's
integration step (new ids S479–S482, opened 2026-10-25, mined, `used-by` listing
`corpus/knowledge/quota-observability-r48.md`). The mock rows used for validation are shown in
the tail of the script and have exactly that shape. UNVERIFIED: the counter's run at the
landed tip (entry and SOURCES rows do not exist at any revision yet).

## Lane sweep (`## What the lane held before`)

```
$ grep -cE 'xfs_quota|quotactl|EDQUOT|repquota' corpus/SOURCES.md
0
$ git show 4387cf94:corpus/SOURCES.md | grep -cE 'xfs_quota|quotactl|EDQUOT|repquota'
0
$ git show e5dbac05:corpus/SOURCES.md | grep -cE 'xfs_quota|quotactl|EDQUOT|repquota'
0
```

(grep exit 1, no matches.) Sweep `0` at freeze and at entering — matches the receipt
`evidence/sweep-quota-rows.txt`.

## Live rechecks (ran 2026-10-25)

```
$ curl -fsSL 'https://man7.org/linux/man-pages/man8/xfs_quota.8.html' | grep -c 'Quota exceeded'
1
$ curl -fsSL 'https://man7.org/linux/man-pages/man2/quotactl.2.html' | grep -c 'No disk quota is found for the indicated user'
1
$ curl -fsSL 'https://raw.githubusercontent.com/torvalds/linux/v7.2/include/uapi/asm-generic/errno.h' | grep -cE 'EDQUOT[[:space:]]+122'
1
$ curl -fsSL -A 'Mozilla/5.0' 'https://help.aliyun.com/zh/nas/user-guide/set-quotas-on-the-subdirectories-of-nas-nfs-volumes' | grep -c '目录配额功能'
9
```

All four fetch 200 and match the values recorded in the draft's `recheck:` lines.

## Corrections to the staged entry (where the copies disagree)

- **Staged S479 (aliyun) "Disk quota exceeded" error-string claim is not in the committed copy.**
  The staged entry claims the directory-scoped quota surfaces as the failing write's error
  string `Disk quota exceeded` citing the aliyun page. The committed aliyun copy contains no
  such English error string (page body is Chinese; the string "Disk quota exceeded" occurs
  nowhere in the copy). The draft instead supports the aliyun claims with what the copy
  actually shows: kubectl PV/PVC output with a quota-enabled StorageClass and a PVC patch for
  online expansion, The EDQUOT error-string fact is grounded in the xfs_quota copy instead
  (hard-limit paragraph), and the errno value in `errno.h`.
- **Staged S481 (RHEL 9 Japanese PDF) is not part of this claim.** The contract names the PDF
  as HTTP 403 and excluded. Its staged claims (soft-limit `+` marker replacing `-`, `grace`
  column units seconds/minutes/hours/days/weeks/months) are dropped from the draft.
- **Staged S482 (errno.h) quote confirmed.** `#define EDQUOT 122 /* Quota exceeded */` occurs
  verbatim at line 107 of the committed copy.
- **Staged S478 (quotactl) quotes confirmed with one transcription caveat.** `No disk quota is
  found for the indicated user. Quotas have not been turned on for this filesystem.` occurs
  verbatim (the staged prose lowercased the leading "No"); `quotactl_fd()` renders in the
  normalised copy as `quotactl_fd ()` (bold tag stripped), so the quote must include that space.
- **Staged shape.** The staged entry used narrative `### Claim` prose; P-C2 requires the
  `| claim | source | quote |` table. The draft replaces the prose with the table and keeps
  the boundary/probe/delivery sections that the seat assignment names.
- **Staged `verified-at: 2026-10-23` → `2026-10-25`** (P-C2 `OPENED`), and the four recheck
  lines now match the four frozen URLs with live values.

## Draft entry (full)

```markdown
source: S479 — https://man7.org/linux/man-pages/man8/xfs_quota.8.html — §QUOTA OVERVIEW hard limit; §QUOTA ADMINISTRATION items 3, 5, 9; xfsprogs-dev.git 2026-08-04, HTML 2026-09-09
source: S480 — https://man7.org/linux/man-pages/man2/quotactl.2.html — §ERRORS ESRCH; §NOTES quotactl_fd; man-pages 6.19 (2026-06-05), tarball 2026-09-09
source: S481 — https://raw.githubusercontent.com/torvalds/linux/v7.2/include/uapi/asm-generic/errno.h — line 107; tag v7.2
source: S482 — https://help.aliyun.com/zh/nas/user-guide/set-quotas-on-the-subdirectories-of-nas-nfs-volumes — 步骤三：验证目录配额功能; PV/PVC output rows; last-modified 2026-10-13
verified-at: 2026-10-25
recheck: 180d — `curl -fsSL 'https://man7.org/linux/man-pages/man8/xfs_quota.8.html' | grep -c 'Quota exceeded'` -> 1 (ran 2026-10-25)
recheck: 180d — `curl -fsSL 'https://man7.org/linux/man-pages/man2/quotactl.2.html' | grep -c 'No disk quota is found for the indicated user'` -> 1 (ran 2026-10-25)
recheck: 180d — `curl -fsSL 'https://raw.githubusercontent.com/torvalds/linux/v7.2/include/uapi/asm-generic/errno.h' | grep -cE 'EDQUOT[[:space:]]+122'` -> 1 (ran 2026-10-25)
recheck: 180d — `curl -fsSL -A 'Mozilla/5.0' 'https://help.aliyun.com/zh/nas/user-guide/set-quotas-on-the-subdirectories-of-nas-nfs-volumes' | grep -c '目录配额功能'` -> 9 (ran 2026-10-25)
coverage-map: FR2

# Quota exhaustion is a per-id state; `df` cannot see it

## Claims

| claim | source | quote |
|---|---|---|
| XFS keeps quota accounting separate from limit enforcement. | S479 | `XFS distinguishes between quota accounting and limit enforcement.` |
| A user whose usage reaches the hard limit fails space requests with the EDQUOT error. | S479 | `If a user's usage reaches the hard limit, further requests for space (or attempts to create a file) fail with the "Quota exceeded" (EDQUOT) error.` |
| The hard limit cannot be exceeded. | S479 | `The hard limit cannot be exceeded.` |
| Quota accounting is enabled at mount time of the XFS filesystem. | S479 | `Quota accounting must be turned on at the time of mounting the XFS filesystem.` |
| XFS accounts quota even for users who have no quota limits. | S479 | `XFS filesystems perform quota accounting whether the user has quota limits or not.` |
| Limits are never enforced on the superuser or on group and project ID zero. | S479 | `limits are never enforced on the superuser (nor are they enforced for group and project ID zero)` |
| The only way to reset an over-quota condition is to reduce usage below the quota. | S479 | `The only way to reset this condition, short of turning off limit enforcement or increasing the limit, is to reduce usage below quota.` |
| The command scans the entire filesystem and may take a long time. | S479 | `This command can be used even when filesystem quota are not enabled, as it is a full-filesystem scan (it may also take a long time...).` |
| ESRCH means no disk quota exists for the user because quotas are not turned on. | S480 | `No disk quota is found for the indicated user. Quotas have not been turned on for this filesystem.` |
| quotactl_fd() addresses the filesystem by mount point, avoiding the block-device lookup. | S480 | `quotactl_fd () instead works on the mount point, which avoids this limitation and is simpler to use` |
| Exceeding the soft limit is allowed but produces warnings. | S480 | `The soft limit can be exceeded, but warnings will ensue.` |
| A kernel without CONFIG_QUOTA returns the ENOSYS error for these calls. | S480 | `ENOSYS The kernel has not been compiled with the CONFIG_QUOTA option.` |
| Linux defines EDQUOT as errno 122 with the comment "Quota exceeded". | S481 | `#define EDQUOT 122 /* Quota exceeded */` |
| The provider's example output shows a 20Gi dynamic PV bound through the quota-enabled StorageClass. | S482 | `nas-****-c72c-497f-ab13-****** 20Gi RWX Delete Bound default/nas-pvc-nas-sts-0 alicloud-nas-quota-sc <unset> 15m` |
| Expanding a quota-based NAS volume is done by patching the PVC's requested storage. | S482 | `kubectl patch pvc nas-pvc-nas-sts-0 -p '{"spec":{"resources":{"requests":{"storage":"30Gi"}}}}'` |

## What the lane held before

`grep -cE 'xfs_quota|quotactl|EDQUOT|repquota' corpus/SOURCES.md` -> 0 (run at freeze `4387cf94`, identical at entering `e5dbac05`): the lane held kernel quota flags (S078, S084, S088, S089) and mount option vocabulary (S077, S082, S085) but no user-space reporting or error surface.

## Boundaries

- **Read-only.** mori observes and reports quota state; it never changes a quota, a limit or a grace timer. Quota administration is not mori's act.
- **Linux-specific.** `EDQUOT = 122` is a Linux fact (S481). A document quoting a different number for the same symbolic name (for example Solaris `errno=49`) describes a different platform and stays rejected.
- **Filesystem-specific.** `xfs_quota(8)` is XFS; the `quotactl(2)` syscall surface is common to quota-supporting Linux filesystems, but the reporting tools are not (ext4 uses `quota(1)` / `repquota(1)`).
- **Not a threshold authority.** S482 documents a vendor product's quota semantics; it does not set mori's own alert thresholds, which remain locally calibrated and labelled (FR8).

## Probe shape

A quota probe reads per-id quota state, never filesystem capacity:

- read the enforcement/accounting state (`xfs_quota -x -c state` on XFS) so that "quota off" is distinguishable from "usage zero";
- read per-id usage and limits, and treat `ESRCH` as "not turned on", never as a zero;
- match the platform's own EDQUOT number when reading the workload's error string — 122 on Linux (S481);
- price the probe: `quotactl()` is a cheap syscall, while `xfs_quota`'s `quot` subcommand is a full-filesystem scan that may take a long time (S479) — a resident scan, not a one-shot census probe.

## Delivery paths this cannot see

A filesystem with quota accounting disabled and no way to turn it on; a quota managed by a remote file system whose counters are eventually consistent rather than point-in-time; any exhaustion that is bounded by a capacity limit rather than a quota limit; the live page state between rechecks (the copies are dated).
```

## Notes

- All reads/writes were confined to the report path `.ufo/waves/round-48/w1/ScribeEntryA.md`
  and scratch `/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r48-ScribeEntryA/`; no
  production file was modified, and no network write or credential material was involved.
- No tools were installed or upgraded (operator tooling rule: record installs — none).
- The RHEL 9 PDF (staged S481) was not fetched; the contract already records its HTTP 403 and
  exclusion. The Solaris `errno=49` rejection is restated in the entry's Boundaries.
