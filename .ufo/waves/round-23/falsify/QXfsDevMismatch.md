# QXfsDevMismatch — round-23 C2 falsification of `CaseXfsDevMismatch.json`

**Verdict: MATCH (case not falsified).** The sealed case's expectation — exit `2`,
`finding_id` `QUOTA_STATE_UNKNOWN`, and the ordered six-field tuple
`(/mnt/xfsproj/work, xfs, /mnt/xfsproj, unknown, n/a, device_mismatch)` — is reproduced
exactly by the pinned production tool. No frozen case/rule/oracle byte was edited.

Seat: `QXfsDevMismatch` · mode: **fixture only** (one invocation, no real mode, no host quota read).

## 1. Identities (byte-exact)

| item | value |
|---|---|
| case file | `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/frozen/quota-cases/CaseXfsDevMismatch.json` |
| case sha256 (working tree) | `e5db2d1181e0b6ab2062447e2181307a9da4ba64760ce98a0d76f55ccb492097` |
| case sha256 at seal commit `22772c10f6e3c1d8d3fe1b72083a6194e9f4e687` | `e5db2d1181e0b6ab2062447e2181307a9da4ba64760ce98a0d76f55ccb492097` |
| frozen bytes unchanged vs seal | **True** |
| seal is ancestor of production pin | yes (`git merge-base --is-ancestor` → 0) |
| production pin | `f3dc07c0bf423cc1947d0ffa91afa9ce236fbe3c` |
| tool | `/home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-quota-surface.py` |
| tool sha256 | `e485741334d2e72a0f007481f1d2bc5b38658f54c04232965e4bbf552b8f7e92` |
| tool git blob at pin | `439ff4c1a68fc4f98182c6b855b3b4c790286851` (sha256 of the pinned blob equals the working-tree sha256: **True**) |
| fixture (own copy) | `/fast/scratch/hyaku/mori-r23/QXfsDevMismatch/fixture.json` sha256 `5e29840be5a7022c83ea6ae2025156370ac446b826bacbfd1f4cf868c7003c96` |
| fixture provenance | `case["fixture"] verbatim (json.dumps sort_keys, indent 2)` — no byte of the case was edited, the fixture is a serialization of `case["fixture"]` only |

`git status --untracked-files=no` on the lane is clean: this seat changed no tracked file
and no frozen byte.

## 2. Invocation (exactly one child)

```
argv given   : python3 -I TOOL --fixture ABS_FIXTURE
argv actual  : ['/usr/bin/timeout', '15', '/usr/bin/prlimit', '--as=402653184', '/usr/bin/python3', '-I', '/home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-quota-surface.py', '--fixture', '/fast/scratch/hyaku/mori-r23/QXfsDevMismatch/fixture.json']
cwd          : /fast/scratch/hyaku/mori-r23/QXfsDevMismatch
limits       : address_space_bytes=402653184 (384 MiB), timeout_seconds=15, one child at a time
invocations  : 1
TMPDIR       : <unset in invoking shell>
```

`python3 -I` (isolated) is on the command line, so `PYTHON*` environment overrides would
be ignored in any case; the tool's `tempfile` import is used by the `--selftest` arm only,
and in `--fixture` mode `load_fixture()` opens the fixture file and nothing else — no
`/proc/self/mountinfo`, no `os.stat`, no `/sys/fs/btrfs`. No `/tmp` fallback path was
exercised by this invocation.

## 3. Observed result

| channel | value |
|---|---|
| process exit | `2` |
| stdout sha256 | `97720fcd43e829df2b8adaa43e85a1d4af72f85ff3b40d5f3fc5bddd34382553` |
| stderr sha256 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (empty: `""`) |

Verbatim stdout (single line, preserved in the receipt):

```json
{"df_covers_quota":false,"exit_code":2,"finding_id":"QUOTA_STATE_UNKNOWN","limits":"no per-user, per-group or per-project limit or usage is read. no NFS or server-side quota and no overlay or fuse quota is covered. a visible btrfs qgroups directory does not imply that any limit is set. an ext2/ext3/ext4 quota feature in the superblock is unobservable without privileged tools. sysfs and mountinfo races during quota enable, disable or remount are not excluded. df capacity percentages never cover quota exhaustion (FR2 / EDQUOT). QUOTA_DISABLED is not a capacity or health verdict; ENOSPC can coexist. the btrfs qgroups mode attribute is never read, so btrfs_qgroups_mode is null in real mode.","paths":[{"basis":"device_mismatch","btrfs_qgroups_mode":null,"device_check":"mismatch","enforcement":"n/a","fstype":"xfs","mount_point":"/mnt/xfsproj","path":"/mnt/xfsproj/work","quota_option_keys":[],"quota_state":"unknown"}],"schema":"mori-quota-surface-v1"}
```

Pretty-printed for reading:

```json
{
  "df_covers_quota": false,
  "exit_code": 2,
  "finding_id": "QUOTA_STATE_UNKNOWN",
  "limits": "no per-user, per-group or per-project limit or usage is read. no NFS or server-side quota and no overlay or fuse quota is covered. a visible btrfs qgroups directory does not imply that any limit is set. an ext2/ext3/ext4 quota feature in the superblock is unobservable without privileged tools. sysfs and mountinfo races during quota enable, disable or remount are not excluded. df capacity percentages never cover quota exhaustion (FR2 / EDQUOT). QUOTA_DISABLED is not a capacity or health verdict; ENOSPC can coexist. the btrfs qgroups mode attribute is never read, so btrfs_qgroups_mode is null in real mode.",
  "paths": [
    {
      "basis": "device_mismatch",
      "btrfs_qgroups_mode": null,
      "device_check": "mismatch",
      "enforcement": "n/a",
      "fstype": "xfs",
      "mount_point": "/mnt/xfsproj",
      "path": "/mnt/xfsproj/work",
      "quota_option_keys": [],
      "quota_state": "unknown"
    }
  ],
  "schema": "mori-quota-surface-v1"
}
```

## 4. Primary comparison — the six scored fields only

Ordered tuples `(path, fstype, mount_point, quota_state, enforcement, basis)`:

| # | expected | actual | match |
|---|---|---|---|
| 0 | `("/mnt/xfsproj/work", "xfs", "/mnt/xfsproj", "unknown", "n/a", "device_mismatch")` | `("/mnt/xfsproj/work", "xfs", "/mnt/xfsproj", "unknown", "n/a", "device_mismatch")` | yes |

* `exit_match` = **True** (expected 2, output `exit_code` 2, process exit 2)
* `finding_id_match` = **True** (`QUOTA_STATE_UNKNOWN`)
* `primary_tuple_match` = **True**
* missing actual paths = 0, extra actual paths = 0
* row order preserved (single path row; ordering is not a free variable here)

## 5. Supplementary metadata — reported separately, NOT scored

The case declares **no** `supplementary_expected` block (`supplementary_expected declared in case:
False`), so these three fields carry no
pass/fail weight in the primary denominator. Observed values, checked against the
pre-seal amendment's device-mismatch preemption clause:

| field | observed | amendment expectation |
|---|---|---|
| `device_check` | `mismatch` | `mismatch` (amendment: "Device mismatch PREEMPTS the filesystem table: unknown/n/a/device_mismatch; device_check=mismatch") |
| `quota_option_keys` | `[]` | `[]` (amendment: on device-mismatch preemption `quota_option_keys=[]` and `btrfs_qgroups_mode=null`) |
| `btrfs_qgroups_mode` | `None` | `null` |

The final amendment explicitly pins the preemption metadata: `quota_option_keys=[]` and
`btrfs_qgroups_mode=null` on the device-mismatch preemption. The tool's observed values are
exactly those, so the preemption metadata is a satisfied pin (not one of two permitted readings).
The case still declares no `supplementary_expected` block, so these three fields remain outside
the scored six-field denominator.

Output-shape checks (supplementary, not part of the six-field denominator):
output keys = `['df_covers_quota', 'exit_code', 'finding_id', 'limits', 'paths', 'schema']` — exactly the six documented top-level keys for a standard (non-setup) quota output, no
`error` token; `schema` = `mori-quota-surface-v1`; `df_covers_quota` =
`False`; the `limits` text is the fixed boundary string.

## 6. Why this branch fires (contract trace, not result-fitting)

1. Mount resolution over the fixture's four mountinfo lines: covering mounts for
   `/mnt/xfsproj/work` are `/` (xfs 259:3) and `/mnt/xfsproj` (xfs 259:2); longest component
   prefix wins → `/mnt/xfsproj`, fstype `xfs`. No covering mount point occurs twice, so the
   amendment's `ambiguous_overmount` refusal does not fire; the parent-ID guard does not fire
   either because the selected mount's parent id `33` is absent from the snapshot (absent
   parent = unknown topology, no refusal), so the mount is chosen without fabricating a
   parent-ID graph.
2. Device identity: mount `259:2` vs path `st_dev` `8:16` → unequal. The btrfs anonymous-subvolume
   exemption does not apply (fstype is xfs, and the exemption is narrowed to a zero stat major).
3. Preemption therefore yields `unknown` / `n/a` / `device_mismatch` and suppresses the xfs table
   row that would otherwise have selected `xfs_noquota_option` for super options
   `rw,attr2,inode64,noquota`.
4. Verdict precedence: no setup error, no `enabled` row, one `unknown` row → exit `2`,
   `QUOTA_STATE_UNKNOWN`.

## 7. Leakage check (supplementary)

The tool's stdout contains no mount source (`/dev/nvme0n1p2`, `/dev/nvme0n1p3`,
`/dev/mapper/root`), no btrfs UUID, no device basename (`dm-0`), and no super-option value
(`compress=zstd:3`, `subvolid=257`, `subvol=/@home`). The only fixture-derived tokens present
are the fstype labels `xfs`/`btrfs` in the allowed `fstype` field and the ordinary option key
`noquota` in `quota_option_keys` — and for this branch `quota_option_keys` is `[]`, so not even
that key is emitted. Only `fstype: "xfs"` and the mount point `/mnt/xfsproj` (both required
scored fields) are echoed.

## 8. Residual risks and verification gaps (honest, bounded)

* **Single observation.** One invocation of one case. Determinism is not exercised across
  repeated runs; the receipt is the only measurement.
* **Case-level coverage.** This seat says nothing about the other 29 sealed C2 cases, the C1
  calibration claim, the real-mode control, or the driver-level strict red. Those are other
  seats' scope; nothing here promotes them.
* **Fixture fidelity.** The mountinfo snapshot, the `8:16` st_dev and the decoy btrfs sysfs
  record are synthetic. The tool's *real-mode* device-identity path (where `os.stat` supplies
  `st_dev`) was not exercised here — no host quota read was authorized for this seat.
* **Preemption metadata is pinned, not open** (corrected, see NC-2 below): the final amendment
  fixes `quota_option_keys=[]` and `btrfs_qgroups_mode=null` for the device-mismatch
  preemption; the tool's observed values match that pin. The case itself scores only the six
  primary fields, so the pin is checked here as supplementary metadata.
* **Parent-ID guard is inert here.** The extra `ambiguous_overmount` refusal depends on a
  mount id being present in the snapshot; this fixture's snapshot lacks the parent, so the
  branch is untested by this case.

## 9. Wave-level note — the `CaseEscapedSpace` red is not excused

`CaseEscapedSpace` is outside this seat's assignment and was **not** executed here. Its strict
red (selected mount `43`/parent `33` against the shorter `/srv` `42` cover conflicting with its
expected *enabled* row) is a genuine, reportable **mismatch** under the amended rules and must
stay reported as such: the actual rule for that topology is `unknown`/`ambiguous_overmount`, not
`enabled`. It is not to be special-cased, excluded, relabelled or rewritten, and nothing in this
report excuses it. The corrected quota selftest arm (`49/49`, separately labelled, after the
co-evolved fixture input correction) is a different arm from the frozen `CaseEscapedSpace` case
and must never be conflated with it.

## 10. Tooling

No installs, upgrades or service restarts were performed. Only pre-existing host tools were
used: `/usr/bin/python3` (3.14.8, system), `/usr/bin/timeout`, `/usr/bin/prlimit`, `git`
(read-only subcommands: `show`, `status`, `rev-parse`, `merge-base`, `cat-file`). No builds,
linters, formatters, gates or test suites were run; the single fixture invocation above is the
only execution authorized and performed.

## 11. Artifacts written by this seat

* Receipt: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/falsify/QXfsDevMismatch/scan.json`
  (schema `mori-r23-falsification-receipt-v1`, sha256 `2f94248c0a101286a30f93dad46d1f7ff491f6aabff03108f37959c06340e26b`)
* This report: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/falsify/QXfsDevMismatch.md`
* Scratch (probe material, outside the lane): `/fast/scratch/hyaku/mori-r23/QXfsDevMismatch/`
  (`fixture.json`, `stdout.txt`, `stderr.txt`) — no `/tmp` use.

## 12. Named corrections (appended after L1 review; no rerun, no new measurement)

These are reporting-arithmetic corrections only. **No re-execution occurred**: the invocation
count stays 1, the exit code stays `2`, and the stdout/stderr byte identities below are the
originals. The measured evidence and the MATCH verdict are unchanged.

* **NC-1 — output top-level key count corrected.** Section 5 said "exactly the seven documented
  keys". That was wrong. A standard (non-setup) quota output carries **SIX** top-level keys:
  `schema`, `finding_id`, `exit_code`, `paths`, `df_covers_quota`, `limits`. The observed key set
  is exactly those six — `['df_covers_quota', 'exit_code', 'finding_id', 'limits', 'paths',
  'schema']` — with **no** `error` token (an `error` token is only permitted, and only then, on a
  setup-error output, which this run is not). The receipt already recorded the correct six-element
  list under `actual.output_keys`; only the prose count was wrong. Corrected in §5.
* **NC-2 — preemption metadata is pinned, not ambiguous.** Section 5 and the §8 residual-risk
  list previously described the `quota_option_keys` behaviour as "one of two permitted readings"
  and as an open question. That was wrong. The **final amendment explicitly pins** the
  device-mismatch preemption metadata: `quota_option_keys=[]` and `btrfs_qgroups_mode=null`.
  The observed values are `quota_option_keys=[]` and `btrfs_qgroups_mode=null`, i.e. the pin is
  **satisfied**. The case still declares no `supplementary_expected` block, so this remains
  supplementary metadata outside the scored six-field denominator. Corrected in §5 and §8.

Neither correction changes the verdict: exit `2`, `finding_id` `QUOTA_STATE_UNKNOWN` and the
ordered six-field tuple `("/mnt/xfsproj/work", "xfs", "/mnt/xfsproj", "unknown", "n/a",
"device_mismatch")` still match the frozen expectation exactly; stdout sha256
`97720fcd43e829df2b8adaa43e85a1d4af72f85ff3b40d5f3fc5bddd34382553`, stderr empty. The receipt
`falsify/QXfsDevMismatch/scan.json` is unchanged and remains accurate (it contains no
seven-key or two-readings claim).
