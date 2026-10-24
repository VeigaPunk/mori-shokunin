# SrcProcDocs — S168 candidate (Linux v7.2 Documentation/filesystems/proc.rst)

Seat: MoriR31.SrcProcDocs (leaf scout, wave 1, round 31). Assignment: open candidate source S168
for C1, draft its Gate and SOURCES rows. No lane commits, no edits outside this report file.

## 1. Fetch record

- URL: https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/filesystems/proc.rst
- Command: `timeout 120 curl -sSL --fail -m 60 -o S168.src -w 'http_code=%{http_code} size=%{size_download}\n' <url>`
  → `http_code=200 size=107560`; `date -u +%FT%TZ` run immediately after the fetch printed
  `2026-10-22T23:43:07Z`; file mtime `2026-10-22 20:43:07 -0300` (stat) = same instant.
- Saved UNCHANGED (curl wrote straight to the file; no post-processing) at
  `/fast/scratch/hyaku/mori-r31/SrcProcDocs/S168.src`.
- Byte size 107560; lines 2495.
- `sha256sum S168.src` → `e760f716f8278deefab17a63739033cadc7faee93663c49e76455afaaf40d126`
  (re-run after the quotes were read: identical).
- Genuine document, not a challenge page: bytes 1-6 are
  `.. SPDX-License-Identifier: GPL-2.0` and line 4 is `The /proc Filesystem` (S168.src:1,4).
- Exact-URL duplicate check: `grep -c 'raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/filesystems/proc.rst' corpus/SOURCES.md`
  → `1`, at `corpus/SOURCES.md:88` = row S082, whose recorded anchor already carries
  `sha256 e760f716f8278dee` — the same 16-hex prefix as the bytes fetched now, so the URL and the
  bytes are already admitted under another id.
- `grep -n -E 'start_time|proc_pid_stat|proc/<pid>/comm' corpus/SOURCES.md` → no output: no row
  currently covers the stat field table, start_time, or comm.

## 2. Decision: reject (duplicate URL)

Reject reason (one of the three binding criteria in the assignment): the exact URL is already a row
in `corpus/SOURCES.md` — S082 at `corpus/SOURCES.md:88`, same tag `v7.2`, same bytes
(sha256 prefix `e760f716f8278dee`). The bytes *do* carry the fact, so the rejection is about
identity, not content: a second id for the same bytes would duplicate evidence. The correct route
for these facts is to widen S082's scope/anchor/used-by (section 5), or to cite S082 in rows that
already name a S161+ id.

## 3. Located quotes (every one re-found in the saved bytes, never from memory)

Containment was proved with the counter's own normalisation (`' '.join(text.split())`,
`.ufo/waves/round-31/count-c1.py:42-43`) against the whole file: all 8 quotes below returned
`contained=True`, each `wc -w` ≤ 25.

| # | lines | words | verbatim quote | one-line fact it supports for a pid probe |
|---|---|---|---|---|
| Q1 | S168.src:347 | 8 | `start_time time the process started after system boot` | /proc/<pid>/stat carries start_time, a per-instance start stamp — the field a probe must compare, not the pid number, to tell the watchdog instance apart from a later process that reused the number |
| Q2 | S168.src:320 | 10 | `Table 1-4: Contents of the stat fields (as of 2.6.30-rc7)` | the stat field table this lane would cite is dated 2.6.30-rc7, so the table alone is not evidence of current field semantics and needs the man5 page (S171) beside it |
| Q3 | S168.src:135 | 4 | `cmdline Command line arguments` | proc.rst documents cmdline only as "Command line arguments" (Table 1-1) — no argv layout, no interpreter line, so the pgrep -f identity argument cannot be closed from this file |
| Q4 | S168.src:2008-2009 | 12 | `The comm value is limited in size compared to the cmdline value` | comm is a short name, not the full command line: matching a probe on comm cannot stand in for matching the watchdog's launch path |
| Q5 | S168.src:2009-2011 | 21 | `writing anything longer then the kernel's TASK_COMM_LEN (currently 16 chars, including the NUL terminator) will result in a truncated comm value.` | comm is capped at 16 chars including the NUL, so a long watchdog name reads back truncated and an exact-name pgrep against the untruncated name cannot match |
| Q6 | S168.src:2404-2405 | 12 | `Sensitive files like cmdline, sched*, status are now protected against other users.` | under hidepid=1/2 a probe running as another user cannot read cmdline at all: a failed cmdline read is an access result, not evidence the watchdog is dead |
| Q7 | S168.src:121-122 | 22 | `an open file descriptor to /proc/<pid> or to any of its contained files or subdirectories does not prevent <pid> from being reused` | holding /proc/<pid> open does not pin the pid, so an open fd is not proof the probed process is still the watchdog |
| Q8 | S168.src:126-127 | 9 | `Instead, operations on these FDs usually fail with ESRCH.` | operations on a stale /proc/<pid> fd "usually fail with ESRCH" — the documented outcome is ESRCH, not a silent read of whatever process holds the number now |

Line-number check (`sed -n`): 121-122 and 126-127 are the pid-reuse/ESRCH sentences; 135 is the
Table 1-1 cmdline row; 320 is the Table 1-4 header; 347 is the start_time row; 2005 is the section
3.6 header and 2008-2011 are its comm sentences; 2404-2405 are the hidepid=1 cmdline sentence.

What proc.rst does NOT carry, for the entry's benefit: the unit of start_time (clock ticks since
boot) and the boot-time arithmetic are not stated here — line 347 gives only "time ... after system
boot"; the argv/interpreter composition of cmdline is not stated here (Q3). Those remain S171
(man5 proc_pid_stat.5) and S170 (man5 proc_pid_cmdline.5) territory.

## 4. Ready-to-paste Gate row (reject shape, binding format)

```markdown
| S168 | https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/filesystems/proc.rst | 2026-10-22T23:43:07Z | `e760f716f8278deefab17a63739033cadc7faee93663c49e76455afaaf40d126` | `proc.rst:347` (8 words): "start_time time the process started after system boot"; `proc.rst:2009-2011` (21 words): "writing anything longer then the kernel's TASK_COMM_LEN (currently 16 chars, including the NUL terminator) will result in a truncated comm value."; `proc.rst:135` (4 words): "cmdline Command line arguments" | reject, exact URL already a row: S082 at corpus/SOURCES.md:88 carries this same URL at tag v7.2 with the same sha256 prefix e760f716f8278dee, so the bytes are already admitted; extend S082's scope and anchor instead of opening a second id for them |
```

If the L1 overrides the duplicate rule and admits it, the same row admits verbatim with the five
strongest quotes and decision `admit, A, mined`:

```markdown
| S168 | https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/filesystems/proc.rst | 2026-10-22T23:43:07Z | `e760f716f8278deefab17a63739033cadc7faee93663c49e76455afaaf40d126` | `proc.rst:347` (8 words): "start_time time the process started after system boot"; `proc.rst:320` (10 words): "Table 1-4: Contents of the stat fields (as of 2.6.30-rc7)"; `proc.rst:2009-2011` (21 words): "writing anything longer then the kernel's TASK_COMM_LEN (currently 16 chars, including the NUL terminator) will result in a truncated comm value."; `proc.rst:135` (4 words): "cmdline Command line arguments"; `proc.rst:121-122` (22 words): "an open file descriptor to /proc/<pid> or to any of its contained files or subdirectories does not prevent <pid> from being reused"; `proc.rst:126-127` (9 words): "Instead, operations on these FDs usually fail with ESRCH." | admit, A, mined |
```

## 5. Draft SOURCES row, and the recommended S082 extension

Column order copied from `corpus/SOURCES.md:5` (`id | source | kind | tier | scope | anchor |
teaches | status | opened | recheck | used-by`). Use this row only if the L1 admits S168 despite
the duplicate URL; every S161+ id needs exactly one row of this shape (`count-c1.py:141-145`).

```markdown
| S168 | Linux proc filesystem docs v7.2 — /proc/<pid> stat field table, comm and cmdline descriptions, pid-reuse and hidepid access rules — https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/filesystems/proc.rst | docs | A | /proc/<pid>/stat field table (start_time), comm truncation, cmdline description, open-fd pid reuse, hidepid access rules | Table 1-4:320,347; 3.6:2005-2011; Table 1-1:135; pid reuse:121-127; hidepid:2404-2410; tag v7.2; sha256 e760f716f8278dee | The stat field table is dated 2.6.30-rc7 and gives start_time only as time since boot; comm is capped at TASK_COMM_LEN (16 chars with the NUL); an open /proc/<pid> fd does not prevent pid reuse and stale-fd operations usually fail with ESRCH; hidepid=1/2 protects cmdline from other users. | mined | 2026-10-22 | on-release | corpus/knowledge/watchdog-identity-r31.md |
```

Recommended instead (L1 edit to the existing S082 row at `corpus/SOURCES.md:88`, keeping one row
per URL): append to `scope` "; /proc/<pid> stat field table, comm and cmdline descriptions,
pid-reuse note, hidepid access rules"; append to `anchor` "; stat table:320,347; comm:2005-2011;
cmdline:135; pid reuse:121-127; hidepid:2404-2410"; append to `teaches` "start_time is documented
only as time since boot, comm is capped at TASK_COMM_LEN, an open /proc/<pid> fd does not stop pid
reuse, and hidepid=1/2 protects cmdline from other users."; append `, corpus/knowledge/watchdog-identity-r31.md`
to `used-by`. The L1 decides whether `opened` moves from 2026-10-21 to 2026-10-22.

## 6. Notes and remaining unknowns

- Counter consequence: `count-c1.py:81-87,130-133` counts "exactly one SOURCES.md row" per cited
  S161+ id; a S168 row would pass that check even with a duplicate URL, so the duplicate is a
  contract-level call, not a counter failure. Rows citing S082 do NOT count toward the predicate's
  "at least 6 rows cite an id S161 or higher" and "at least 4 such ids" (`contract.md:32-33`), so
  the entry may cite S082 in rows only as an extra source beside a S161+ id.
- No tool was installed or updated (nothing was needed; no pacman transaction was run).
- Unverified by me: whether the L1 wants `opened` refreshed on an extended S082, and whether the
  C1 counter's measurement-time re-fetch of the S082 URL is already exercised by any other seat
  (its sha256 here is stable across my two reads).
- Nothing outside this file and `/fast/scratch/hyaku/mori-r31/SrcProcDocs/` was written; the lane
  Git index and jj state were not touched (read-only git/grep only).
