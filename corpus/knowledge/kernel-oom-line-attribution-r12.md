source: S003 — https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/oom_kill.c — v7.2 `dump_oom_victim` lines 447–453 and `__oom_kill_process` victim line 945; S004 — https://raw.githubusercontent.com/torvalds/linux/c03c1a14507dfaf8b856c2608f9ac216021fc222/mm/memcontrol.c — master commit c03c1a14 `mem_cgroup_print_oom_context` lines 1820–1826; S014 — https://www.freedesktop.org/software/systemd/man/latest/journalctl.html — systemd 262 `-k` lines 341–343 and `--output-fields=` lines 489–494; S015 — https://www.freedesktop.org/software/systemd/man/latest/systemd.journal-fields.html — systemd 262 `_TRANSPORT` lines 204–246
verified-at: 2026-10-19 (lane base 20e2255; host kernel 7.2.3-arch1-3, systemd 261 (261.2-1-arch))
recheck: curl -fsSL https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/oom_kill.c | grep -nF 'oom-kill:constraint='; curl -fsSL https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/oom_kill.c | grep -nF 'pr_cont(",task=%s,pid=%d,uid=%d'; curl -fsSL https://raw.githubusercontent.com/torvalds/linux/c03c1a14507dfaf8b856c2608f9ac216021fc222/mm/memcontrol.c | grep -nF 'pr_cont(",task_memcg='); journalctl -k -b all -q --grep='^oom-kill:constraint=' -o json --output-fields=_BOOT_ID | jq -r '._BOOT_ID' | sort | uniq -c; journalctl -k -b all -q --grep='(Out of memory|Memory cgroup out of memory): Killed process [0-9]+' -o json --output-fields=_BOOT_ID | jq -r '._BOOT_ID' | sort | uniq -c; journalctl -k -b 0 -q --grep='^oom-kill:constraint=' -o json --output-fields=_BOOT_ID | wc -l → anchors 447, 452, 1825; 5 7bd93aee71144017b870212161a3dabf; 5 7bd93aee71144017b870212161a3dabf; 0

## Claim
A kernel OOM summary and its `Killed process` victim record carry event-time attribution absent from aggregate counters: the summary includes task, PID, UID and (when available) `task_memcg`; journal record metadata carries timestamp and boot identity. They are system-journal kernel records (`_TRANSPORT=kernel`). A future probe may emit only strictly shape-validated tokens; it must never echo journal `MESSAGE` text.

Adjacent: `tsukuroi-shokunin/corpus/knowledge/oom-event-plane.md:23–42,359–367` distinguishes kernel OOM dumps from teardown/SIGKILL waves with no kernel record. This note adds source-backed event-time token fields only; it does not claim every fleet termination has a kernel OOM record.

## Evidence
- S003 `mm/oom_kill.c:447–453`: `dump_oom_victim()` writes the `oom-kill:constraint=` summary and the `task=%s,pid=%d,uid=%d` fields.
- S004 `memcontrol.c:1820–1826` appends `oom_memcg=` and `task_memcg=` cgroup paths to that summary. S003 `mm/oom_kill.c:945–947` emits the victim PID and UID on the `Killed process` line.
- Source line re-open (raw URL search, 2026-10-19): `oom-kill.c` matched `oom-kill:constraint=` at `447`, `task=%s,pid=%d,uid=%d` at `452`, and `Killed process` at `945`; `memcontrol.c` matched `task_memcg=` at `1825`. The copy-pastable source locators are the URLs/anchors above.
- S014 `journalctl -k:342` says `-k` adds `_TRANSPORT=kernel`. Its `--output-fields=:489–494` documents always-present `__REALTIME_TIMESTAMP` and `_BOOT_ID`; S015 `systemd.journal-fields:_TRANSPORT:204–246` defines `kernel` as records read from the kernel.
- Counts only, fields restricted: `journalctl -k -b all -q --grep='^oom-kill:constraint=' -o json --output-fields=_BOOT_ID | wc -l` → `5`; grouped with `jq -r '._BOOT_ID' | sort | uniq -c` → `5 7bd93aee71144017b870212161a3dabf`; the same count command with `-b 0` → `0`.
- Victim-record count: `journalctl -k -b all -q --grep='(Out of memory|Memory cgroup out of memory): Killed process [0-9]+' -o json --output-fields=_BOOT_ID | wc -l` → `5`; grouped with `jq -r '._BOOT_ID' | sort | uniq -c` → `5 7bd93aee71144017b870212161a3dabf`; with `-b 0` → `0`. No `MESSAGE` field is output.
- Timestamp context for the five kernel OOM summaries (L1's MESSAGE-free extraction): `journalctl -k -b all -q --grep='^oom-kill:constraint=' -o json --output-fields=_BOOT_ID | grep -oE '"__REALTIME_TIMESTAMP":"[0-9]+"'` → timestamps corresponding to `2026-10-18T17:46:17Z`, `18:06:07Z`, `19:07:45Z`, `22:53:10Z`, `23:57:18Z` (UTC-rendered from journal microseconds).

## Observed
The source defines the kernel summary and victim fields; the retained kernel journal has five matching summaries and five matching victim records, all grouped under the same boot ID. The current boot's summary count is zero. These are counts and source-format observations, not a new per-victim transcript.

## [INFERENCE]
A parser that reads an event for attribution must validate PID/UID as decimal tokens and the cgroup path against a strict path shape, otherwise emit `shape-refused`; it must not emit `task`/comm text or any `MESSAGE` value. The path is captured at event time: do not attempt attribution later by reopening a possibly deleted cgroup. The counters alone remain aggregate and cannot recover these fields.

## [UNKNOWN]
Whether every kernel OOM victim produces both retained records, and whether records were lost outside the retained journal, remain unknown. Fleet attribution of the five observed victims remains [UNKNOWN] unless a strictly shape-validated `task_memcg` token is read; these measurements did not expose or parse any journal `MESSAGE` payload.

## What it changes for mori
For the SKILL.md `CGROUP_OOM_KILL` error-pattern row (`:28`), counters are not the attribution source: the system-journal kernel records are. Any later probe must validate token shapes, preserve event-time fields only, refuse malformed records, and keep `MESSAGE` out of output.

## Delivery paths this cannot see
Kernel OOM records do not observe systemd-oomd's userspace cgroup kill, earlyoom's ordinary signals, or arbitrary SIGKILLs. Attribution is unavailable if the relevant system journal cannot be read, the event record was not retained, or journal loss occurred; a post-event cgroup lookup cannot restore a deleted victim path.

## Fills (coverage-map ground; Frontier row)
Coverage-map ground: event-time kernel OOM victim attribution from the system journal. Frontier F2: kernel OOM attribution, with token-only output and no `MESSAGE` echo.
