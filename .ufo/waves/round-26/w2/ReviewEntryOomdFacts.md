# ReviewEntryOomdFacts — wave-2 falsification of userspace-oom-killers-r26.md

Seat: MoriR26.ReviewEntryOomdFacts (leaf; no subagents; no lane writes).
Target: `corpus/knowledge/userspace-oom-killers-r26.md` at tip 16935e24c93fa7e7567413d7ec091339a5df1474 (271 lines; blob sha256 prefix 73593455). Line numbers below are tip line numbers.
Scope: the systemd-oomd, ManagedOOM, d989611b, journal JSON, `--output-fields`, `-u` and monotonic-clock statements. The earlyoom statements (F2, F3, F5, F7, F9 counts) are not in this seat's scope and are not run here.
Time box: exceeded by a few minutes to pin the tip blobs. Every check below is either run or marked not run.

## 1. Method and bounds

- **Tip, not working tree.** Entry, contract and tool read with `git show 16935e24:<path>`. The working-tree copy is modified (`git status` shows ` M`); its 26-line diff touches only earlyoom and tool text (tip lines 193, 200, 213-216, 238-243). No statement below is in that diff. Lane HEAD is now f1efb46, which this review does not cover.
- **systemd v262 sources** fetched by ordinary curl from the public raw URL (curl 8.23.0) into `/fast/scratch/hyaku/mori-r26/ReviewEntryOomdFacts/v262/`. sha256 prefixes: resource-control.xml d57641df; systemd-oomd.service.xml 4b29be2e; oomd-util.c 2e94450a; systemd.catalog.in e53707db; journalctl.xml d54bbede; JOURNAL_EXPORT_FORMATS.md 207a646c; org.freedesktop.systemd1.xml 59cfeea5; sd-messages.h fb613f71; logs-show.c abc2fc1f; journald-stream.c e919ebe8; oomd.c d6749807; oomd-util.h 79f3daac. Adjacent files also fetched: job.c, unit.c, time-util.h, systemd.journal-fields.xml, org.freedesktop.oom1.xml, oomd-manager.c, src/basic/utf8.c, four units/ drop-ins, and the v262 tree listing (GitHub API, public).
- **Host reads, all read-only.** `systemctl show -p ManagedOOMSwap -p ManagedOOMMemoryPressure` on the four units; `journalctl -q -b -u earlyoom.service -o json --output-fields=MESSAGE -n 1` with key names printed and no values; `journalctl --list-boots` plus a per-boot count of `MESSAGE_ID=d989611b…` records (counts only). Nothing was started, stopped, enabled or restarted. No MESSAGE text, process name, settings value or session id was written to any output.
- **Tooling.** No install or upgrade was needed. curl 8.23.0 and python3 (stdlib) were already present; systemctl and journalctl are the host's (systemd 262). RULES.md was read first.

## 2. Verdicts

Columns: ID | entry line | statement | source (v262 unless noted) | verdict.

| ID | Line | Statement | Source | Verdict |
|---|---|---|---|---|
| O1 | 146 | `auto` is the upstream default | resource-control.xml:1529 "Defaults to auto." | holds |
| O2 | 146-147 | `auto` means the cgroup's data is not used for monitoring and detection | resource-control.xml:1545-1546 (holds); :1546-1548 say an `auto` unit "can still be a candidate for systemd-oomd to terminate" when an ancestor is `kill` | defect (low): the termination clause is omitted |
| O3 | 144-146 | the four named units carry `auto` on both properties, so nothing in the chain is monitored | host, my read: `auto`/`auto` on the user@ unit, user-UID.slice, user.slice and -.slice. Upstream v262 sets no ManagedOOM* in units/user@.service.in, units/user-.slice.d/10-defaults.conf, units/user@.service.d/10-login-barrier.conf or units/user@0.service.d/10-login-barrier.conf. Only `kill` cgroups are monitored: systemd-oomd.service.xml:43-44 | holds |
| O4 | 147-148 | systemd-oomd's kill accounting is the `user.oomd_ooms` and `user.oomd_kill` cgroup attributes | oomd-util.c:269 (+1 per kill attempt); :305-308 (+ processes killed, only when above 0); :50-78 (decimal counters) | holds |
| O5 | 148 | "plus a `Killed` D-Bus signal" | oomd-util.c:311-319: `Killed` ("ss"), path /org/freedesktop/oom1, interface org.freedesktop.oom1.Manager; org.freedesktop.oom1.xml:37-44, :69 ("sent when any cgroup is killed by oomd"), :103 (since 252) | holds; gap (low): the interface is not named, and org.freedesktop.systemd1.xml has no `Killed` (grep count 0). Nuance: the signal fires after any kill call with no hard error, even when zero processes were killed (oomd-util.c:298-321), so it is not proof that a process died |
| O6 | 149-151 | catalog id d989611b15e44c9dbf31e3c81256e4ed reads "systemd-oomd killed one or more processes in unit @UNIT@" | systemd.catalog.in:884-885 (exact text); sd-messages.h:195-196 (SD_MESSAGE_UNIT_OOMD_KILL) | holds |
| O7 | 149, 195 | systemd-oomd is the writer of the d989611b notice | not located: the macro is not used in oomd-util.c, oomd.c, oomd-util.h, oomd-manager.c, unit.c, job.c or the other fetched files | not run (emitter unverified; no contrary source found) |
| O8 | 151 | 0 notices in every retained boot | host counts: boot indices -5 to 0 (the six boots journalctl lists), 0 each | holds (counts) |
| O9 | 195 | row: the notice means "one or more processes in a unit"; it is not a count | systemd.catalog.in:885 "one or more processes" | holds (subject to O7) |
| O10 | 198 | row: `user.oomd_ooms` / `user.oomd_kill` are "its accounting of its kill attempts and killed pids" | oomd-util.c:50-78 and :269, :306: both attributes hold decimal counters; no pid is written to either | defect (low): "killed pids" is wrong. Use "a running count of kill attempts and a running count of processes killed" |
| O11 | 198-199 | the attributes "live and die with the cgroup path" | written on ctx->path (oomd-util.c:269, :306); cgroup xattr lifetime was not read | [INFERENCE] holds in direction |
| O12 | 69-72 | earlyoom records carry no MESSAGE_ID; all carry PRIORITY 6 | journald-stream.c:641-642 (`.priority = LOG_INFO`, the default of the stream object used for stdout and stderr); :241-242 (only a `<N>` prefix changes it); no MESSAGE_ID is set anywhere in journald-stream.c (grep) | holds. The [INFERENCE] at lines 77-79 is now source-backed for the stream default. Not checked: the unit's StandardError setting |
| O13 | 69-71 | the one record with a MESSAGE_ID is systemd's unit-lifecycle line | sd-messages.h:155 (SD_MESSAGE_UNIT_STARTED = 39f53479…); job.c:742 maps the start job to SD_MESSAGE_UNIT_STARTED_STR (enclosing function not read) | holds |
| O14 | 3 (recheck), 113 | `-u earlyoom.service` returns earlyoom's records | journalctl.xml:321-323 and :1164-1171: `-u` also matches `UNIT=… _PID=1` (PID 1's records), `OBJECT_SYSTEMD_UNIT=… _UID=0`, and `COREDUMP_UNIT=… MESSAGE_ID=fc2e22bc…` | holds for the PID 1 lifecycle line the 13-record count depends on. defect (low): the set is labelled "earlyoom's records" (113, 162) but is wider. The prefix grammar keeps other lines out of the counts [INFERENCE: no such line was seen] |
| O15 | 2, 3 | `--output-fields=MESSAGE,__MONOTONIC_TIMESTAMP` yields the timestamp | journalctl.xml:669-675: for json, __CURSOR, __REALTIME_TIMESTAMP, __MONOTONIC_TIMESTAMP and _BOOT_ID are always printed; logs-show.c:1266-1267 (unconditional); logs-show.c:1193 and :1298 (user fields filtered by the set). Host, keys only, `-u earlyoom.service -o json --output-fields=MESSAGE -n 1`: MESSAGE, _BOOT_ID, __CURSOR, __MONOTONIC_TIMESTAMP, __REALTIME_TIMESTAMP, __SEQNUM, __SEQNUM_ID | holds (the extra field in the entry is redundant and harmless) |
| O16 | 3 | `journalctl -q -b MESSAGE_ID=d989611b… -o json --output-fields=MESSAGE_ID \| wc -l` counts records | host: 0 in the current boot; one JSON object per line was observed | holds |
| O17 | 113-115 | F6 scope: `__MONOTONIC_TIMESTAMP` at or above ActiveEnterTimestampMonotonic | systemd.journal-fields.xml:656-660: `__MONOTONIC_TIMESTAMP` is CLOCK_MONOTONIC "at the point in time the entry was received by the journal". unit.c:2766-2774: active_enter_timestamp comes from dual_timestamp_now at the state change (declaration time-util.h:91; body not read). job.c:742: the Started record follows the state change, so its receipt stamp lands just inside the bound, as the entry reports | holds on a shared clock. defect (low, precision): receipt time is not stated, so a line written before the bound but received after it counts as current [INFERENCE: negligible for a Type=simple unit] |
| O18 | 113 | both stamps are monotonic microseconds since boot | systemd.journal-fields.xml:656-660 (CLOCK_MONOTONIC); unit.c:2774 | holds [INFERENCE for the dual_timestamp_now body] |
| O19 | 2; contract tip line 76 | "A MESSAGE that is a byte array in journal JSON is decoded as UTF-8 with replacement" (C2 interface) | tool-tip.py:162-168 (list to bytes to decode "utf-8","replace"); JOURNAL_EXPORT_FORMATS.md:145-147 ("non-printable or non-UTF8" becomes a number array); logs-show.c:1126-1131; src/basic/utf8.c:105-122 (control characters and newline fail the printable check; wrapper utf8_is_printable not read) | holds as a decoding policy. gap (low, contract wording): the array trigger is wider than invalid UTF-8. No tool defect was found, because the tool decodes any list |
| O20 | 113 | timestamps arrive as numeric strings | JOURNAL_EXPORT_FORMATS.md:154-156 (numeric string of usec); logs-show.c:1266-1267 (USEC_FMT string) | holds; the tool's string-to-int parse was not run |
| O21 | 144-145 | systemd-oomd inactive and disabled | host state, outside source scope | not run |

## 3. Findings by severity

1. **Defect, low — O10 (line 198).** "killed pids" is wrong. The attributes are decimal counters (oomd-util.c:50-78, :306). No pid list is kept.
2. **Defect, low — O2 (lines 146-147).** The `auto` paraphrase omits the ancestor-kill clause (resource-control.xml:1546-1548). No unit in the chain is `kill`, so O3 still holds.
3. **Defect, low — O14 (line 113 and the 13-record count).** The `-u` set is called "earlyoom's records", but journalctl.xml:1164-1171 shows it also matches PID 1 records, OBJECT_SYSTEMD_UNIT root records and COREDUMP records.
4. **Defect, low — O17 (lines 113-115).** `__MONOTONIC_TIMESTAMP` is journal receipt time (systemd.journal-fields.xml:656-660), and the entry does not say so.
5. **Gap, low — O5 (line 148).** The `Killed` signal's interface is `org.freedesktop.oom1.Manager`, not systemd1. It can fire with zero processes killed (oomd-util.c:303-319).
6. **Gap, low — O19 (contract tip line 76).** The byte-array trigger is non-printable or non-UTF-8 (JOURNAL_EXPORT_FORMATS.md:145-147). The contract's wording is trigger-neutral, so no tool defect follows.
7. **Unverified — O7 (lines 149, 195).** The emitter of the d989611b notice was not located. The catalog text and the ID name support the entry's reading.

No finding overturns a systemd-side claim. Every defect is a wording or omission problem. My own host reads agree with the entry on the four `auto` units (O3) and on zero d989611b records (O8, O16).

Suggested wording, if the note is revised: line 198 "a running count of kill attempts (`user.oomd_ooms`) and a running count of processes killed (`user.oomd_kill`)"; line 146 add "and an `auto` unit can still be a kill candidate if an ancestor is `kill`"; line 113 add "the timestamp is journal receipt time"; line 113 label the set "the `-u` set (earlyoom's own records plus PID 1 lifecycle lines and related records)".

## 4. Residual risk and verification gaps

- **Not run:** the d989611b emitter (O7); the dual_timestamp_now body (time-util.c); the wrapper utf8_is_printable (utf8.h); the tool's JSON string parse (O20); host unit state (O21); the Type=notify inference at lines 120-121; the earlyoom statements (out of this seat's scope).
- **Not checked for other boots:** the d989611b count was run for six boots. The sibling capture's previous-boot earlyoom counts were not re-run.
- **Tip scope:** this review covers 16935e24 only. Lane HEAD is f1efb46 and the working tree has an uncommitted 26-line diff. Neither was reviewed.
- **Runtime not observed:** no kill was observed, so the Killed-signal nuance (O5) and the array trigger (O19) are source readings, not runtime behaviour.

## 5. Tooling record

- Used, not installed: curl 8.23.0 (fetches), python3 stdlib (parsing), systemctl and journalctl 262 (host, read-only).
- Installed or upgraded: none.
- Writes: this report, and scratch files under /fast/scratch/hyaku/mori-r26/ReviewEntryOomdFacts/ only.
