# ExecQuoteFinderMan — wave w1 (round 48, mori-shokunin)

Quote inventory for the two man-page sources of C2 (FR2 quota observability), verified by
substring test against the committed copies under
`corpus/evidence/sources-r48/`. 14 candidate quotes (7 per page), all 6–25 words.

## Method

- Normalisation is exactly `count-c2.py`'s `normalise()`: strip `<[^>]+>` tags, `html.unescape`,
  collapse all whitespace runs to a single space. The counter module is imported from
  `.ufo/waves/round-48/count-c2.py` via `importlib` (imported, never executed), so the script
  always normalises byte-for-byte like the counter.
- Each candidate is verified by substring test: `q in normalise(committed_copy)`, located at offset
  `norm.find(q)`, word count `len(q.split(" "))` in [6, 25].
- Run: `TMPDIR=/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r48-ExecQuoteFinderMan python3
  /home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r48-ExecQuoteFinderMan/verify_quotes.py`
  → exit 0, `PASS=14/14 FAIL=0` (full output below).
- Offsets are character offsets in the normalised text of the committed copy (one line per page).
- Scratch: `.scratch/r48-ExecQuoteFinderMan/` (script + normalised dumps). No lane tool was run
  from `/tmp`; `TMPDIR` was set for the run.
- Tooling: nothing installed or upgraded (stdlib `python3` 3.14.8 only) — no RULES.md/operator
  tooling record needed beyond this statement.

## Table

Offsets and word counts are the script's verified values. `claim` states only what the quote says.

| # | page | quote | words | offset | claim |
|---|------|-------|-------|--------|-------|
| 1 | xfs_quota.8 | `XFS filesystems with limit enforcement turned off can be used as an effective disk usage accounting system` | 17 | 3306 | XFS can act as a pure disk-usage accounting system when limit enforcement is turned off — accounting and enforcement are separable. |
| 2 | xfs_quota.8 | `use the state to monitor the XFS quota subsystem at various stages` | 12 | 8766 | The `state` command is the monitoring surface for the XFS quota subsystem (the page goes on to say it shows whether quotas are turned on and the space the quota system itself occupies). |
| 3 | xfs_quota.8 | `This command uses a special XFS "bulkstat" interface to quickly scan an entire filesystem and report usage information` | 18 | 14807 | The `quot` command scans an entire filesystem via the XFS bulkkstat interface and reports usage information. |
| 4 | xfs_quota.8 | `This command can be used even when filesystem quota are not enabled, as it is a full-filesystem scan` | 18 | 14927 | `quot` is a whole-filesystem scan and works even when filesystem quota are not enabled. |
| 5 | xfs_quota.8 | `Report filesystem quota information. This reports all quota usage for a filesystem` | 12 | 10215 | The `report` command reports all quota usage for a filesystem (per quota type and block/inode/realtime, per the rest of the command text). |
| 6 | xfs_quota.8 | `When a user exceeds the soft limit, the timer is enabled. Any time the quota drops below the soft limits, the timer is disabled` | 24 | 4219 | Exceeding the soft limit starts the grace timer; dropping back below the soft limits disables it. |
| 7 | xfs_quota.8 | `further requests for space (or attempts to create a file) fail with the "Quota exceeded" (EDQUOT) error` | 17 | 4114 | Once usage reaches the hard limit, further space/file requests fail with EDQUOT (`"Quota exceeded"`). |
| 8 | quotactl.2 | `quotactl, quotactl_fd - manipulate disk quotas` | 6 | 304 | `quotactl` and `quotactl_fd` are the syscalls that manipulate disk quotas. |
| 9 | quotactl.2 | `quotactl_fd () instead works on the mount point, which avoids this limitation and is simpler to use` | 17 | 4696 | `quotactl_fd()` addresses the filesystem by a descriptor open on its mount point, avoiding the block-device-lookup limitation of `quotactl()`. |
| 10 | quotactl.2 | `the special argument is a pointer to a null- terminated string containing the pathname of the (mounted) block special device` | 20 | 1991 | `quotactl()` addresses a filesystem by the pathname of its (mounted) block special device. |
| 11 | quotactl.2 | `The op argument indicates an operation to be applied to the user or group ID specified in id` | 18 | 1645 | Each `quotactl` operation applies to a specific user or group ID named by `id`. |
| 12 | quotactl.2 | `The subop value is one of the following operations: Q_QUOTAON(2const) Q_QUOTAOFF(2const) Q_GETQUOTA(2const) Q_GETNEXTQUOTA(2const)` | 13 | 2512 | `Q_GETQUOTA` and `Q_GETNEXTQUOTA` are among the subops `quotactl` supports, i.e. the per-id read style. |
| 13 | quotactl.2 | `No disk quota is found for the indicated user. Quotas have not been turned on for this filesystem` | 18 | 3524 | `quotactl` returns ESRCH when no disk quota is found for the user — quotas have not been turned on for the filesystem (the error entry’s text). |
| 14 | quotactl.2 | `The caller lacked the required privilege ( CAP_SYS_ADMIN ) for the specified operation` | 13 | 3430 | `quotactl` returns EPERM when the caller lacks `CAP_SYS_ADMIN` for the operation. |

Coverage cross-check against the seat brief, all satisfied by the table: XFS separates quota
accounting from limit enforcement (#1); the `state` command (#2); `quot` is a whole-filesystem scan
(#3, #4); report / soft-limit markers and the grace column (#5 + #6); ESRCH when quotas are not on
(#13); `quotactl_fd` addressing a filesystem by mount point (#9); `Q_GETQUOTA`/`Q_GETNEXTQUOTA`
style per-id reads (#12, #11); EDQUOT/EPERM-style errors (#7, #14).

## Findings beyond the quotes

- The committed xfs_quota.8 copy has no literal "grace column" or asterisk/marker text for report
  output; soft-limit/grace semantics are described by the `timer` command text (#6). The `report`
  command text (#5) reports all quota usage; I found no marker-character description to quote.
- The committed quotactl.2 copy lists `Q_GETQUOTA`/`Q_GETNEXTQUOTA` (and the XFS `Q_XGETQUOTA`/
  `Q_XGETNEXTQUOTA` variants) among the subops but gives no per-operation prose: after the operation
  list it goes straight to `RETURN VALUE`/`ERRORS`. The per-id-read claim (#12) is therefore exactly
  the enumeration, not a behavioural description.

## Script

`verify_quotes.py` (scratch; reproduced verbatim):

```python
#!/usr/bin/env python3
"""ExecQuoteFinderMan — verify 14 candidate quotes (7 per man page) by substring test.

Normalisation is exactly count-c2.py's normalise(): tags stripped, html.unescape,
whitespace collapsed. The module is imported (not executed) so its main() never runs.
"""
import importlib.util
import pathlib
import sys

ROOT = pathlib.Path("/home/vgpnk/Projects/shokunin/mori-shokunin")
COUNTER = ROOT / ".ufo/waves/round-48/count-c2.py"
SRC = ROOT / "corpus/evidence/sources-r48"

XFS = SRC / "xfs_quota.8.html"
QUOTACTL = SRC / "quotactl.2.html"

# (quote, source, claim)
CANDIDATES = [
    # ---- xfs_quota.8.html ----
    ("XFS filesystems with limit enforcement turned off can be used as an effective disk usage accounting system",
     XFS, "XFS can act as a pure disk-usage accounting system when limit enforcement is turned off."),
    ("use the state to monitor the XFS quota subsystem at various stages",
     XFS, "The state command is the monitoring surface: it shows whether quotas are on and the space the quota system itself occupies."),
    ("This command uses a special XFS \"bulkstat\" interface to quickly scan an entire filesystem and report usage information",
     XFS, "quot scans an entire filesystem via the XFS bulkkstat interface and reports usage."),
    ("This command can be used even when filesystem quota are not enabled, as it is a full-filesystem scan",
     XFS, "quot is a whole-filesystem scan that works even when quota are not enabled."),
    ("Report filesystem quota information. This reports all quota usage for a filesystem",
     XFS, "The report command reports all quota usage for a filesystem (per type and block/inode/realtime)."),
    ("When a user exceeds the soft limit, the timer is enabled. Any time the quota drops below the soft limits, the timer is disabled",
     XFS, "Exceeding the soft limit starts the grace timer; dropping below the soft limits disables it."),
    ("further requests for space (or attempts to create a file) fail with the \"Quota exceeded\" (EDQUOT) error",
     XFS, "Once usage reaches the hard limit, further space/file requests fail with EDQUOT (\"Quota exceeded\")."),
    # ---- quotactl.2.html ----
    ("quotactl, quotactl_fd - manipulate disk quotas",
     QUOTACTL, "quotactl and quotactl_fd are the syscalls that manipulate disk quotas."),
    ("quotactl_fd () instead works on the mount point, which avoids this limitation and is simpler to use",
     QUOTACTL, "quotactl_fd addresses the filesystem by a descriptor open on its mount point, avoiding the block-device-lookup limitation."),
    ("the special argument is a pointer to a null- terminated string containing the pathname of the (mounted) block special device",
     QUOTACTL, "quotactl() addresses a filesystem by the pathname of its (mounted) block special device."),
    ("The op argument indicates an operation to be applied to the user or group ID specified in id",
     QUOTACTL, "Each quotactl operation applies to a specific user or group ID named by id."),
    ("The subop value is one of the following operations: Q_QUOTAON(2const) Q_QUOTAOFF(2const) Q_GETQUOTA(2const) Q_GETNEXTQUOTA(2const)",
     QUOTACTL, "Q_GETQUOTA and Q_GETNEXTQUOTA are among the subops quotactl supports for per-id reads."),
    ("No disk quota is found for the indicated user. Quotas have not been turned on for this filesystem",
     QUOTACTL, "quotactl returns ESRCH when no quota exists for the user, i.e. quotas are not turned on for the filesystem."),
    ("The caller lacked the required privilege ( CAP_SYS_ADMIN ) for the specified operation",
     QUOTACTL, "quotactl returns EPERM when the caller lacks CAP_SYS_ADMIN for the operation."),
]


def main() -> int:
    spec = importlib.util.spec_from_file_location("count_c2", COUNTER)
    cc = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cc)

    norm = {name: cc.normalise((SRC / name).read_text(encoding="utf-8", errors="surrogateescape"))
            for name in ("xfs_quota.8.html", "quotactl.2.html")}

    fail = 0
    print(f"{'#':>2} {'words':>5} {'offset':>6}  {'src':<20} quote")
    for i, (q, src, claim) in enumerate(CANDIDATES, 1):
        n = norm[src.name]
        words = len(q.split(" "))
        off = n.find(q)
        ok = off >= 0 and 6 <= words <= 25
        if not ok:
            fail += 1
        print(f"{i:>2} {words:>5} {off:>6}  {src.name:<20} {ok!s:>5}  {q}")
    print(f"\nPASS={len(CANDIDATES)-fail}/{len(CANDIDATES)} FAIL={fail}")
    return 1 if fail else 0


if __name__ == "__main__":
    sys.exit(main())
```

## Evidence (command + output + exit code)

Command (run with `TMPDIR` = scratch, not `/tmp`):

```
python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r48-ExecQuoteFinderMan/verify_quotes.py
```

Output: exit code **0**:

```
 # words offset  src                  quote
 1    17   3306  xfs_quota.8.html      True  XFS filesystems with limit enforcement turned off can be used as an effective disk usage accounting system
 2    12   8766  xfs_quota.8.html      True  use the state to monitor the XFS quota subsystem at various stages
 3    18  14807  xfs_quota.8.html      True  This command uses a special XFS "bulkstat" interface to quickly scan an entire filesystem and report usage information
 4    18  14927  xfs_quota.8.html      True  This command can be used even when filesystem quota are not enabled, as it is a full-filesystem scan
 5    12  10215  xfs_quota.8.html      True  Report filesystem quota information. This reports all quota usage for a filesystem
 6    24   4219  xfs_quota.8.html      True  When a user exceeds the soft limit, the timer is enabled. Any time the quota drops below the soft limits, the timer is disabled
 7    17   4114  xfs_quota.8.html      True  further requests for space (or attempts to create a file) fail with the "Quota exceeded" (EDQUOT) error
 8     6    304  quotactl.2.html       True  quotactl, quotactl_fd - manipulate disk quotas
 9    17   4696  quotactl.2.html       True  quotactl_fd () instead works on the mount point, which avoids this limitation and is simpler to use
10    20   1991  quotactl.2.html       True  the special argument is a pointer to a null- terminated string containing the pathname of the (mounted) block special device
11    18   1645  quotactl.2.html       True  The op argument indicates an operation to be applied to the user or group ID specified in id
12    13   2512  quotactl.2.html       True  The subop value is one of the following operations: Q_QUOTAON(2const) Q_QUOTAOFF(2const) Q_GETQUOTA(2const) Q_GETNEXTQUOTA(2const)
13    18   3524  quotactl.2.html       True  No disk quota is found for the indicated user. Quotas have not been turned on for this filesystem
14    13   3430  quotactl.2.html       True  The caller lacked the required privilege ( CAP_SYS_ADMIN ) for the specified operation

PASS=14/14 FAIL=0
```

## Risks / notes

- Quotes were verified against the committed copies at the current working tree (the frozen sha256s
  in `count-c2.py` pin these files; no file bytes were altered).
- Per the counter's `normalise()`, the hyphens and parentheses inside quotes are literal characters of
  the (rendered) HTML text; a copy with different markup would shift offsets.
- No limitations beyond the two "Findings" above; nothing was UNVERIFIED for the pages I was
  assigned (the other two frozen sources — `errno.h`, `aliyun-nas-quota.html` — are outside this
  seat's scope).
