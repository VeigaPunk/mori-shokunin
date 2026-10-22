# Host capture — FR10 userspace OOM killers (round 26, wave 1)

Seat: MoriR26.HostCapture · 2026-10-22 · Leaf executor, read-only.
Sandbox clone: `/fast/scratch/hyaku/mori-r26/wt-capture` (branch `r26-wt-capture`, base `28b0494`).
Sandbox commits `e804d75` (script + first capture) and `b3a3f42` (class list aligned with the tool grammar, recaptured output).
Only this report was written in the lane: no lane commit, no push, no unit touched, no package changed.

## Deliverables

| File (in the sandbox clone) | sha256 |
|---|---|
| `.ufo/waves/round-26/capture/capture.sh` | `bea3b6cba7ea55e900662ce82abdf37731b28a8eadb866a0598555c860f5b9a6` |
| `.ufo/waves/round-26/capture/capture.txt` | `945a0a4e216a2284532e525329a940a8804c5d9df0a49070f06b84dba8e62955` |

`capture.sh` takes the output path as `$1` and writes exactly that one file. Run once:
`bash capture.sh .ufo/waves/round-26/capture/capture.txt` → exit 0, 72 records. The script source is
not pasted here (it is 315 lines); it is at the sandbox path above, sha256-pinned, and its design
decisions are below.

## Design decisions and why

**`set -u` only — no `set -e`, no `set -o pipefail`.** The brief asked for "no pipefail traps that
hide errors". `pipefail` + `errexit` aborts the whole capture on the first non-zero stage, so one
failing probe would silently truncate the file and the reader could not tell a truncated capture
from a quiet host. Instead every probe records its own exit status next to its value, and the one
pipeline whose two stages matter (journalctl → python reader) captures both stages' statuses via
`PIPESTATUS` and emits them as `earlyoom_journal_journalctl_rc` / `earlyoom_journal_reader_rc`.
Verified by fault injection: `sh -c 'echo "{}"; exit 7' | python3 …` yields `__capture_rc__ 7 0` —
the failure is recorded, not swallowed.

**Writes only `$1`.** The reader program lives in a shell variable (`PYCODE='…'`), not a heredoc,
because a bash heredoc materialises a temporary file. With `TMPDIR` pointed at an empty directory,
one full run left that directory empty.

**Journal bodies never reach the file.** `journalctl -q -b -u earlyoom.service -o json
--output-fields=MESSAGE` is piped straight into a python reader that emits only derived lines
(counts, threshold numbers, the three permitted fixed-format lines). No MESSAGE text is written to
disk at any point.

**ManagedOOM block attribution.** `systemctl show -p ManagedOOMSwap,ManagedOOMMemoryPressure -- user@1000.service user-1000.slice user.slice -.slice`
prints one blank-line-separated block per unit in argument order. The `--` separator is required:
without it systemctl reads the leading `-` of `-.slice` as an option and exits 1
(`systemctl: invalid option -- '.'`). The script splits on blank lines (not on every line), records
`managed_oom_show_units=` alongside, and records `managed_oom_blocks=4 managed_oom_units_listed=4`
so a block-count mismatch is visible. Order was confirmed against the same query with `Id` added
(`Id=user@1000.service`, `Id=user-1000.slice`, `Id=user.slice`, `Id=-.slice`).

**Counts, boot-wide and in-scope.** The contract's scope rule is
`__MONOTONIC_TIMESTAMP >= ActiveEnterTimestampMonotonic`. The script emits `journal_count_boot_*`
(whole current boot) and `journal_count_scope_*` (monotonic ≥ `earlyoom_scope_start_monotonic`), so
a reader can pick either and the two stay distinguishable. The anchor comes from the unit itself
(`systemctl show earlyoom.service -p ActiveEnterTimestampMonotonic --value` → `19964362`).

**Class prefixes** follow the earlyoom v1.9.0 message grammar at tag `v1.9.0`: `sending SIGTERM to
process `, `sending SIGKILL to process `, `escalating to SIGKILL after `, `kill failed: `,
`low memory! at or below SIGTERM limits`, `low memory! at or below SIGKILL limits`, `mem avail: `,
`dryrun mode enabled`, `killing whole process group `, `Suppressed `. Prefix-anchored after
stripping leading whitespace, matching `/fast/scratch/hyaku/mori-r26/main.c:414,416,519,523`,
`kill.c:318,627,654` and `meminfo.c:279`. The `mem avail: ` class is the periodic report line, not
a kill. The last two classes were added after cross-reading the tool seat's grammar in
`tools/mori-oom-killers.py:111-121`, so the capture's class list is a superset-compatible mirror of
the tool's rather than a parallel list; the `Suppressed ` class additionally requires the
` messages from earlyoom.service` marker, so an unrelated line starting with the same word is not
counted. Both classes are 0 on this host (verified by a separate scan of the 13 journal lines).


**Byte-array MESSAGE.** The reader accepts a MESSAGE that is a JSON byte array and decodes it as
UTF-8 with replacement, matching the contract's input shape.

## Privacy verification

Required check, run against the produced `capture.txt`:

```
$ grep -inE 'avoid|prefer|cmdline|uid|EARLYOOM_ARGS' capture.txt
(no output; grep exit 1)
```

Per-token counts, all case-insensitive: `avoid` 0, `prefer` 0, `cmdline` 0, `uid` 0,
`EARLYOOM_ARGS` 0.

Stronger check — every one of the 13 journal MESSAGE lines in the current boot was tested for
verbatim appearance in `capture.txt`. Exactly 3 appear, all 3 permitted; the other 10 (both
selection-regex lines, the mem-total line, `Started Early OOM Daemon.`, 6 `mem avail:` reports) do
not: the version line `earlyoom 1.9.0`, the SIGTERM threshold line and the SIGKILL threshold line.
`ExecStart` is never queried (`systemctl show -p …` is limited to `Id,LoadState,ActiveState,
UnitFileState,ActiveEnterTimestampMonotonic` and `ManagedOOMSwap,ManagedOOMMemoryPressure`), and
`/etc/default/earlyoom` is never opened.

## Captured host facts (2026-10-22, this host)

Every value is quoted from the produced `capture.txt`; the command that produced each is named.

| Fact | Value | Source command |
|---|---|---|
| Kernel release | `7.2.11-arch1-1` | `uname -r` |
| systemd version | `systemd 262 (262-1-arch)` | `systemctl --version \| head -1` |
| earlyoom package | `earlyoom 1.9.0-1` | `pacman -Q earlyoom systemd` (query only) |
| systemd package | `systemd 262-1` | same |
| `earlyoom.service` is-active | `active` (rc 0) | `systemctl is-active earlyoom.service` |
| `earlyoom.service` is-enabled | `enabled` (rc 0) | `systemctl is-enabled earlyoom.service` |
| `systemd-oomd.service` is-active | `inactive` (rc 3) | `systemctl is-active systemd-oomd.service` |
| `systemd-oomd.service` is-enabled | `disabled` (rc 1) | `systemctl is-enabled systemd-oomd.service` |
| earlyoom unit show | `LoadState=loaded`, `ActiveState=active`, `UnitFileState=enabled`, `ActiveEnterTimestampMonotonic=19964362` | `systemctl show earlyoom.service …` |
| systemd-oomd unit show | `LoadState=loaded`, `ActiveState=inactive`, `UnitFileState=disabled`, `ActiveEnterTimestampMonotonic=0` | `systemctl show systemd-oomd.service …` |
| ManagedOOM, all four user scopes | `ManagedOOMSwap=auto`, `ManagedOOMMemoryPressure=auto` for `user@1000.service`, `user-1000.slice`, `user.slice`, `-.slice` | `systemctl show -p ManagedOOMSwap,ManagedOOMMemoryPressure -- …` |
| earlyoom version in scope | `1.9.0` (`journal_scope_complete=1`, source `scope`) | journal reader |
| earlyoom thresholds | SIGTERM `10.00%` mem / `10.00%` swap; SIGKILL `5.00%` mem / `5.00%` swap | journal reader |
| journal entries | 13 total, 13 in scope, 0 without timestamp | journal reader |
| kill activity this boot | `sending_sigterm_to_process=0`, `sending_sigkill_to_process=0`, `escalating=0`, `kill_failed=0` | journal reader (boot and scope) |
| low-memory warnings this boot | `low_memory_sigterm=0`, `low_memory_sigkill=0` | journal reader |
| periodic `mem avail:` reports | 6 | journal reader |
| dry-run mode | `dryrun_enabled=0` | journal reader |
| oomd notices (`d989611b15e44c9dbf31e3c81256e4ed`) | `0` in the current boot (rc 0); also `0` across all boots | `journalctl -q -b MESSAGE_ID=… -o json --output-fields=MESSAGE_ID` |

**Reading for C1.** The four frozen stale phrases in `.ufo/waves/round-26/c1-phrases.txt` claim this
host's userspace killers are inactive. This capture contradicts that on the earlyoom side: earlyoom
is `active` and `enabled` since monotonic `19964362` in the current boot, while the systemd-oomd
side is `inactive` and `disabled`. "Both inactive" is therefore false; "systemd-oomd inactive" is
true. The capture is the committed artifact the r26 entry can cite.

**Reading for C2.** This host is the *quiet* case: earlyoom is active with `scope_complete=1` and a
verified `1.9.0` version line inside scope, thresholds parsed (10.00/10.00/5.00/5.00 — exactly the
host-shaped quiet case the contract names), and no action line of any class. `oomd_notices=0`. A
live read of this host today should be `KILLERS_QUIET` (exit 0) — but only because the reads
succeeded. The capture also pins two facts the tool must get right here:
`ActiveEnterTimestampMonotonic` is non-zero (scope is computable, not unavailable), and
`systemd-oomd.service` is `inactive`, so its `actions` must be `null` (unavailable), never zero
counts.

## Verification performed

| Check | Result |
|---|---|
| `bash -n capture.sh` | syntax OK |
| Full run, exit status | `0`, 72 records |
| Forbidden-token grep on `capture.txt` | 0 hits for all five tokens |
| All 13 journal MESSAGE lines tested for verbatim presence | 3 present, all permitted; 10 absent |
| Run with `TMPDIR` pointed at an empty dir | that dir stayed empty — no temp files |
| Two consecutive runs, content diff | identical except the `ts=` timestamps |
| Fault injection: pipeline stage exits 7 | recorded as `__capture_rc__ 7 0`, not swallowed |
| Empty journal input to the reader | emits zero-valued counts, exit 0, no crash |
| Missing `$1` | usage message on stderr, exit 2 |
| `managed_oom` attribution | 4 blocks ↔ 4 units; order confirmed against an `Id`-bearing query |

## Tooling record

No install or upgrade was needed. The script uses only tools already present: `bash` 5.3.20,
`systemctl`/`journalctl` (systemd 262), `pacman` (query mode only), `python3`, `awk`, `head`, `date`,
`grep`, `sha256sum`. No pacman transaction was run — the round pacman freeze is untouched, and no
host service was started, stopped, enabled or restarted.

## Risks and open items for the L1

1. **The capture lives in the sandbox clone, not the lane.** Per the wave bounds I did not commit to
   the lane. The L1 must decide whether `capture.sh` / `capture.txt` land in the lane tree and under
   which path — the C2 tool seat may prefer the capture to stay a receipt under
   `.ufo/waves/round-26/capture/` rather than under `tools/`.
2. **The capture is a point-in-time snapshot** taken 2026-10-22. It is evidence for the r26 entry's
   dated past-tense rewrite, not a live probe the tool depends on. The tool
   (`tools/mori-oom-killers.py`) must collect its own inputs live; the capture is the receipt that
   the host was in this state.
3. **`systemd-oomd.service` is `inactive` with `ActiveEnterTimestampMonotonic=0`.** If the tool
   derives an oomd scope from that field it sees zero; the capture shows oomd never started this
   boot, so oomd's state and `notices_this_boot` must come from the unit state and the journal
   query, not from a monotonic comparison.
4. **`journal_count_scope_*` and `journal_count_boot_*` are equal here** (13 entries, all in scope),
   so this host cannot discriminate between the two. The distinction is implemented but only
   exercised on a host with an earlyoom restart inside one boot; the tool seat's frozen cases carry
   that boundary case, mine does not.
5. **The `mem avail:` class counts the periodic report line** (`meminfo.c:279`), 6 of them this
   boot. It is a report, not an action — the tool's `low_memory_warnings` must not derive from it.
6. **The `d989611b…` oomd notice id matched nothing this boot** (0 in the current boot and 0 across
   all boots). The query itself is correct — the same matcher returns 1 line for a known-present
   `MESSAGE_ID` (`7c8a41f37b764941a0e1780b1be2f037`) and 5 across all boots — so `0` here means "no
   oomd notice", not "the filter is broken". Worth stating in the r26 entry so the count is not
   misread as an unavailable read.

## Ready-to-paste: the capture text

```text
ts=2026-10-22T10:27:17-03:00 # mori round-26 FR10 host capture (userspace OOM killers)
ts=2026-10-22T10:27:17-03:00 capture_script=.ufo/waves/round-26/capture/capture.sh
ts=2026-10-22T10:27:17-03:00 capture_started=2026-10-22T10:27:17-03:00
ts=2026-10-22T10:27:17-03:00 capture_scope=current boot; earlyoom.service and systemd-oomd.service
ts=2026-10-22T10:27:17-03:00 uname_release=7.2.11-arch1-1 uname_rc=0
ts=2026-10-22T10:27:17-03:00 systemd_version_line=systemd 262 (262-1-arch) systemd_version_rc=0
ts=2026-10-22T10:27:18-03:00 pacman_query_rc=0
ts=2026-10-22T10:27:18-03:00 package_earlyoom=1.9.0-1
ts=2026-10-22T10:27:18-03:00 package_systemd=262-1
ts=2026-10-22T10:27:18-03:00 unit_earlyoom.service_is_active=active unit_earlyoom.service_is_active_rc=0
ts=2026-10-22T10:27:18-03:00 unit_earlyoom.service_is_enabled=enabled unit_earlyoom.service_is_enabled_rc=0
ts=2026-10-22T10:27:18-03:00 unit_systemd-oomd.service_is_active=inactive unit_systemd-oomd.service_is_active_rc=3
ts=2026-10-22T10:27:18-03:00 unit_systemd-oomd.service_is_enabled=disabled unit_systemd-oomd.service_is_enabled_rc=1
ts=2026-10-22T10:27:18-03:00 unit_show_rc=0
ts=2026-10-22T10:27:18-03:00 unit_show_Id=earlyoom.service
ts=2026-10-22T10:27:18-03:00 unit_show_LoadState=loaded
ts=2026-10-22T10:27:18-03:00 unit_show_ActiveState=active
ts=2026-10-22T10:27:18-03:00 unit_show_UnitFileState=enabled
ts=2026-10-22T10:27:18-03:00 unit_show_ActiveEnterTimestampMonotonic=19964362
ts=2026-10-22T10:27:18-03:00 unit_show_Id=systemd-oomd.service
ts=2026-10-22T10:27:18-03:00 unit_show_LoadState=loaded
ts=2026-10-22T10:27:18-03:00 unit_show_ActiveState=inactive
ts=2026-10-22T10:27:18-03:00 unit_show_UnitFileState=disabled
ts=2026-10-22T10:27:18-03:00 unit_show_ActiveEnterTimestampMonotonic=0
ts=2026-10-22T10:27:18-03:00 managed_oom_show_rc=0 managed_oom_show_units=user@1000.service,user-1000.slice,user.slice,-.slice
ts=2026-10-22T10:27:18-03:00 managed_oom_user@1000.service_ManagedOOMSwap=auto
ts=2026-10-22T10:27:18-03:00 managed_oom_user@1000.service_ManagedOOMMemoryPressure=auto
ts=2026-10-22T10:27:18-03:00 managed_oom_user-1000.slice_ManagedOOMSwap=auto
ts=2026-10-22T10:27:18-03:00 managed_oom_user-1000.slice_ManagedOOMMemoryPressure=auto
ts=2026-10-22T10:27:18-03:00 managed_oom_user.slice_ManagedOOMSwap=auto
ts=2026-10-22T10:27:18-03:00 managed_oom_user.slice_ManagedOOMMemoryPressure=auto
ts=2026-10-22T10:27:18-03:00 managed_oom_-.slice_ManagedOOMSwap=auto
ts=2026-10-22T10:27:18-03:00 managed_oom_-.slice_ManagedOOMMemoryPressure=auto
ts=2026-10-22T10:27:18-03:00 managed_oom_blocks=4 managed_oom_units_listed=4
ts=2026-10-22T10:27:18-03:00 earlyoom_scope_start_monotonic=19964362 earlyoom_scope_start_rc=0
ts=2026-10-22T10:27:18-03:00 journal_entries_total=13
ts=2026-10-22T10:27:18-03:00 journal_entries_without_timestamp=0
ts=2026-10-22T10:27:18-03:00 journal_entries_in_scope=13
ts=2026-10-22T10:27:18-03:00 journal_scope_start_monotonic=19964362
ts=2026-10-22T10:27:18-03:00 journal_count_boot_sending_sigterm_to_process=0
ts=2026-10-22T10:27:18-03:00 journal_count_scope_sending_sigterm_to_process=0
ts=2026-10-22T10:27:18-03:00 journal_count_boot_sending_sigkill_to_process=0
ts=2026-10-22T10:27:18-03:00 journal_count_scope_sending_sigkill_to_process=0
ts=2026-10-22T10:27:18-03:00 journal_count_boot_escalating=0
ts=2026-10-22T10:27:18-03:00 journal_count_scope_escalating=0
ts=2026-10-22T10:27:18-03:00 journal_count_boot_kill_failed=0
ts=2026-10-22T10:27:18-03:00 journal_count_scope_kill_failed=0
ts=2026-10-22T10:27:18-03:00 journal_count_boot_low_memory_sigterm=0
ts=2026-10-22T10:27:18-03:00 journal_count_scope_low_memory_sigterm=0
ts=2026-10-22T10:27:18-03:00 journal_count_boot_low_memory_sigkill=0
ts=2026-10-22T10:27:18-03:00 journal_count_scope_low_memory_sigkill=0
ts=2026-10-22T10:27:18-03:00 journal_count_boot_mem_avail_report=6
ts=2026-10-22T10:27:18-03:00 journal_count_scope_mem_avail_report=6
ts=2026-10-22T10:27:18-03:00 journal_count_boot_dryrun_enabled=0
ts=2026-10-22T10:27:18-03:00 journal_count_scope_dryrun_enabled=0
ts=2026-10-22T10:27:18-03:00 journal_count_boot_process_group_lines=0
ts=2026-10-22T10:27:18-03:00 journal_count_scope_process_group_lines=0
ts=2026-10-22T10:27:18-03:00 journal_count_boot_suppressed_messages=0
ts=2026-10-22T10:27:18-03:00 journal_count_scope_suppressed_messages=0
ts=2026-10-22T10:27:18-03:00 journal_version_line_source=scope
ts=2026-10-22T10:27:18-03:00 journal_scope_complete=1
ts=2026-10-22T10:27:18-03:00 journal_version_line_text=earlyoom 1.9.0
ts=2026-10-22T10:27:18-03:00 journal_version=1.9.0
ts=2026-10-22T10:27:18-03:00 journal_threshold_term_line_text=sending SIGTERM when mem avail <= 10.00% and swap free <= 10.00%,
ts=2026-10-22T10:27:18-03:00 journal_threshold_term_mem_pct=10.00
ts=2026-10-22T10:27:18-03:00 journal_threshold_term_swap_pct=10.00
ts=2026-10-22T10:27:18-03:00 journal_threshold_kill_line_text=SIGKILL when mem avail <=  5.00% and swap free <=  5.00%
ts=2026-10-22T10:27:18-03:00 journal_threshold_kill_mem_pct=5.00
ts=2026-10-22T10:27:18-03:00 journal_threshold_kill_swap_pct=5.00
ts=2026-10-22T10:27:18-03:00 earlyoom_journal_journalctl_rc=0 earlyoom_journal_reader_rc=0
ts=2026-10-22T10:27:18-03:00 oomd_notice_message_id=d989611b15e44c9dbf31e3c81256e4ed oomd_notice_count=0 oomd_notice_rc=0
ts=2026-10-22T10:27:18-03:00 capture_finished=2026-10-22T10:27:18-03:00
```
