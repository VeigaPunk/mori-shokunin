# ExecHostTracefs2 — host tracefs re-read (round 47 w2)

Seat: ExecHostTracefs2. Attack: S477's anchor claims (own-work host tracefs reading) as
recorded in `corpus/lessons/round-47.md` and `corpus/knowledge/oom-tracepoints-r47.md`
(source row S477), comparing a fresh read-only re-read against the receipt
`.ufo/waves/round-47/evidence/host-tracefs.txt` (timestamp line ignored).

## Verdict: holds

All eleven read commands in the receipt reproduce byte-identically (stdout and rc) on
2026-10-25 re-read, ignoring the timestamp line. Kernel version, directory listing, every
event `format` (including the S477 located quote and all event IDs), and the `enable` flag
are unchanged.

## Method

Read-only only: `ls` and `sudo -n cat` under `/sys/kernel/tracing/events/oom`. No write
to tracefs, no tracing enabled, no `sudo` beyond read-only `cat`/`ls`. Outputs captured to
`/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r47w2-ExecHostTracefs2/` and
diffed programmatically against the receipt, command block by command block.

## Observed evidence

```
$ uname -r
7.2.11-arch1-1
rc=0

$ ls /sys/kernel/tracing/events/oom
ls: cannot open file '/sys/kernel/tracing/events/oom': Permission denied
rc=2

$ sudo -n ls /sys/kernel/tracing/events/oom
compact_retry
enable
filter
finish_task_reaping
mark_victim
oom_score_adj_update
reclaim_retry_zone
skip_task_reaping
start_task_reaping
wake_reaper
rc=0

$ sudo -n cat /sys/kernel/tracing/events/oom/mark_victim/format
name: mark_victim
ID: 582
...
	field:uid_t uid;	offset:48;	size:4;	signed:0;
...
rc=0

$ sudo -n cat /sys/kernel/tracing/events/oom/enable
0
rc=0
```

Full capture: `.scratch/r47w2-ExecHostTracefs2/{ls-user,ls-sudo,enable,uname,fmt-*}.txt`.

## Diff against receipt `host-tracefs.txt`

Parsed the receipt into its 11 command blocks (`$ ls (as user)`, `$ sudo -n ls`,
8 × `$ sudo -n cat <event>/format`, `$ sudo -n cat enable`) and compared each block's
stdout + rc line against the matching fresh capture. Result: **11/11 MATCH, 0
mismatches** (outputs byte-equal; rc lines equal: `ls` user rc=2, everything else rc=0).
Only the receipt's header line (date/timestamp) differs by design and was ignored.

## S477 anchor claims — each still holds

1. Reading requires root; unprivileged `ls /sys/kernel/tracing/events/oom` →
   `Permission denied`, rc=2. ✓ (reproduced)
2. Kernel `7.2.11-arch1-1` (receipt header claim) matches `uname -r`. ✓
3. `sudo -n ls` listing identical: exactly the 8 event directories
   (`compact_retry`, `finish_task_reaping`, `mark_victim`, `oom_score_adj_update`,
   `reclaim_retry_zone`, `skip_task_reaping`, `start_task_reaping`, `wake_reaper`)
   plus `enable` and `filter`. ✓
4. Located quote `"field:uid_t uid;	offset:48;	size:4;	signed:0;"` present verbatim on
   one line of `mark_victim/format` (tab-separated, offset 48/size 4/signed 0). ✓
5. `events/oom/enable` reads `0` (all events disabled; no tracing active). ✓
6. Every event `format` body — event names, IDs (577–584) and field layouts — identical to
   the receipt, so the entry's field-schema claims (S475-anchored through S477's own-work
   receipt) rest on an unchanged kernel ABI. ✓

## Boundaries honored

- No tracefs writes; `events/oom/enable` confirmed `0` before and during the read.
- No mutation of the lane repo, fleet root, jj state, or git index; scratch only under
  `.scratch/r47w2-ExecHostTracefs2/`.
- No tool installations (none needed); no pacman.

## Risks / limits

- The re-read confirms the live kernel still matches the receipt; it does not prove the
  receipt was itself captured honestly at round-47 time (that is the seat's assumption).
- Event IDs are kernel-build specific; 577–584 unchanged now, but a kernel update would
  invalidate them (already noted in the entry's Boundaries).
- UNVERIFIED: sha256 pin of the receipt file itself (no committed pin exists for it); the
  receipt's byte content matches the live host regardless.
