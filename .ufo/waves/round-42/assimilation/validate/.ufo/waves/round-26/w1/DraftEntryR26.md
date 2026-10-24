# DraftEntryR26 — round 26 wave 1, the superseding FR10 knowledge entry (C1 + learning claim)

Seat: `MoriR26.DraftEntryR26` (scribe, leaf member). Date: 2026-10-22.
Claim served: **C1 (freshness)** — the entry `corpus/knowledge/userspace-oom-killers-r26.md` that
supersedes the host-state and earlyoom parts of `corpus/knowledge/userspace-oom-killers-r12.md`.
This is also the round's **learning claim** in the "stronger entry superseding a weaker one" sense
(`goal-20261022-hyaku-12h.md:147`): the new entry is not a date-stamp on the old one, it carries
facts the old entry did not have and one correction the old entry got wrong.

**Scope of this seat.** This report and nothing else. The entry text is **drafted, not written**:
`corpus/knowledge/userspace-oom-killers-r26.md` does **not** exist and was not created — the lane
bounds allow a scribe to write only its own report file, and the L1 lands the entry from §2 below.
`corpus/SOURCES.md` was **not** edited: the draft's `source:` line already carries the L1's
assigned ids S114–S125 (§4.1 lists what each row covers), and the rows themselves are the L1's
to admit. No lane commit, no `jj` at the fleet root, no product-code edit, no unit
started/stopped/enabled/disabled, no package installed or removed.

---

## 1. Behavior the draft establishes

The draft entry rests on 9 facts. Every fact below was opened or measured by this seat; the row
provenance is in §3.

| # | Fact | Primary source opened |
|---|---|---|
| F1 | On this host `earlyoom.service` is **active and enabled** (earlyoom 1.9.0-1, Arch) and `systemd-oomd.service` is **inactive and disabled** (systemd 262-1). The current earlyoom invocation began `2026-10-22 04:55:44 -03`. | host reads (§3.1) |
| F2 | earlyoom acts only when **memory AND swap are both** below their limits; it sends **SIGTERM at the first limit, SIGKILL at the second**; the shipped default is **10 %** with the kill limit at **half** (`PERCENT/2`). | S114 README / S115 MANPAGE / S119 main.c |
| F3 | The percentages are **not** shares of `MemTotal`: "mem avail %" is a share of *user mem total* (`MemAvailable + AnonPages`); "swap free %" is a share of `SwapTotal` and is forced to `0` when there is no swap. | S116 meminfo.c |
| F4 | earlyoom's actions appear in the journal as **plain text records with no `MESSAGE_ID`**, `SYSLOG_IDENTIFIER=earlyoom`, `_COMM=earlyoom`, `PRIORITY 6`. Priority does not separate its `warn()` lines from its `info()` lines. | S118 msg.c + host read |
| F5 | Only a fixed set of **prefix-anchored literals** is stable enough to count (the eight grammar lines). The action line carries a uid, a process name and a command line: **count, never copy**. Escalation prints no action line, `kill failed:` covers two distinct causes, and the periodic `mem avail:` report is not an action. | S118 kill.c / S119 main.c / msg.h |
| F6 | The scope is the **current invocation**: journal lines with `__MONOTONIC_TIMESTAMP` ≥ the unit's `ActiveEnterTimestampMonotonic`, with the **version line's presence** as the completeness test (the unit's own start record is inside the bound and precedes it). | S119 main.c + host read |
| F7 | earlyoom's kills do **not** move the kernel OOM counters: it delivers signals itself (`kill(2)` + `pidfd`), never the kernel victim path that increments `count_vm_event(OOM_KILL)`. On this host the delegation exception does not even exist — **earlyoom 1.9.0 has no `--kernel-oom` option**. | S118 kill.c + `oom-kill-counter-kernel-only-r12.md` |
| F8 | systemd-oomd side: inactive and disabled here, every unit the sibling captured is `auto` on both `ManagedOOM*` properties (cited, not absorbed), and the oomd notice id `d989611b…` (`catalog/systemd.catalog.in:884` at v262) has **0** occurrences in every retained boot. | S121 v262 catalog / S124 man pages / S125 sibling + host read |
| F9 | Host journal evidence, counts only: the current boot holds 13 earlyoom records and 0 actions; the previous boot holds **38 SIGTERM + 1 SIGKILL** action lines, 40 low-memory warnings, 1 "recovered while selecting victim" line, and 39 kill/exit pairs; the retained journals hold exactly **1** kernel OOM summary, timestamped ~39 minutes *after* earlyoom's last action in that boot. | host read (§3.2) |

## 2. The full draft — `corpus/knowledge/userspace-oom-killers-r26.md`

Paste-ready. The `source:` line already carries the L1's assigned ids S114–S125 (see §4.1);
no renumbering is needed in the entry text. Every `verified / scoped / [INFERENCE]` tag is part of the entry.

```markdown
source: S114 (earlyoom v1.9.0 README at tag v1.9.0 = commit 202d4db0d308ca6478f68de68b46cae34896ddaf — https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/README.md — the act rule, the staged SIGTERM-then-SIGKILL order, where actions are logged, the journal-reading advice and the v1.9.0 changelog; sha256 23411dbfd8b409d433f984a5d6677830e86a383ec76935fc1e1d675e6b4374dd, opened 2026-10-22); S115 (earlyoom v1.9.0 MANPAGE.md at the same tag — https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/MANPAGE.md — the both-below rule, the PERCENT/2 kill default and the `user mem total` definition; sha256 cc48b02e79255ae27bad9b2c49364fcae1b6b5eb20fe8e83ecef432f360dfeda, opened 2026-10-22); S116 (earlyoom v1.9.0 meminfo.c at the same tag — https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/meminfo.c — the memory and swap percentages earlyoom compares against its limits; sha256 526e512c89c58cb0b1db2ae98ea62d287cdc1516846be80c9173bdc4bf0edfeb, opened 2026-10-22); S117 (earlyoom tag history — https://github.com/rfjakob/earlyoom/releases and https://api.github.com/repos/rfjakob/earlyoom/commits?path=main.c — the v1.9.0 tag and commit, the v1.2 removal of the kernel-oom option and its 2026-02-02 re-introduction on master; opened 2026-10-22); S118 (earlyoom v1.9.0 kill.c and msg.c at the same tag — https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/kill.c and https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/msg.c — the action, escalation and kill-failure literals, the signal-delivery path, the `warn()`/`info()` write targets and the `"%5.2lf%%"` percentage format; sha256 b32e0fad65e298235102f98aff37e02c94400b544d454cb57192ae697b100bf3 and a771c91529053341c290ede2a7df1d9fdf16e07fb9584db8a64604a45dea5197, opened 2026-10-22); S119 (earlyoom v1.9.0 main.c at the same tag — https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/main.c — the two startup threshold literals, the act decision, the compiled defaults, the dry-run and low-memory literals and the version literal; sha256 08656b0bc90c85f23738661456b25c97af908bc5e2cfea78e0a69697b5f9d0e4, opened 2026-10-22); S120 (earlyoom v1.9.0 service unit template and the installed Arch package — https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/earlyoom.service.in and `pacman -Qi earlyoom` on this host — the unit's EnvironmentFile/ExecStart shape, the package version 1.9.0-1 and its install date; sha256 d4019b66d87539a006fc2d178d972dcf1b46e70343627b8bf66d1a08dcdda0bd, opened 2026-10-22); S121 (systemd v262 oomd-util.c and message catalog — https://raw.githubusercontent.com/systemd/systemd/v262/src/oom/oomd-util.c and https://raw.githubusercontent.com/systemd/systemd/v262/catalog/systemd.catalog.in — oomd's own kill accounting and the d989611b… notice id; sha256 2e94450aa337dd7d2062f2730e46e22ac00fc2c3195c11654047ddcaba487e7a and e53707db7e6963b284e504dc17f36a4d5a2bdb4bd8a9611b2cf95c075ad86592, opened 2026-10-22); S122 (systemd v262 journal documentation — https://www.freedesktop.org/software/systemd/man/latest/journalctl.html and https://www.freedesktop.org/software/systemd/man/latest/systemd.journal-fields.html — `journalctl -q -b -u`, `--output-fields=`, the `MESSAGE`/`MESSAGE_ID` field semantics and `_TRANSPORT=kernel`; systemd 262 man pages opened 2026-10-22); S123 (systemd v262 logs-show.c and utf8.c — https://raw.githubusercontent.com/systemd/systemd/v262/src/shared/logs-show.c and https://raw.githubusercontent.com/systemd/systemd/v262/src/basic/utf8.c — how `journalctl` emits the requested journal fields (`logs-show.c:554` parses `MESSAGE=`, `:1456`/`:1459` emit `MESSAGE` and each requested `--output-fields=` entry) and the UTF-8 validation and escaping helpers (`utf8.c:16,105,129,152`) that govern a non-UTF-8 message payload; sha256 abc2fc1f3d6f10d0f01b4d1ff18689eb5561a98fd71fde911117ce16c50ed72f and 7cbebe621330509d7ed4928ea0e8374cf7155e954fee2745ebf08b90cd030d27, opened 2026-10-22); S124 (systemd v262 resource-control and systemd-oomd manual pages — https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd.resource-control.xml and https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd-oomd.service.xml — `ManagedOOMSwap=`/`ManagedOOMMemoryPressure=` auto|kill, the meaning of `auto`, and which cgroups systemd-oomd monitors; sha256 d57641df40e45811403de91e55059b6a8f7506c6812a85cbe9c6ba22900587d8 and 4b29be2e41ef309beb9f9a9fcc9a84f18cd7f9f3540f094b0b5717891ef8651d, opened 2026-10-22); S125 (sibling lane tsukuroi, memory-pressure-r25.md at commit 157ee255 — https://raw.githubusercontent.com/VeigaPunk/tsukuroi-shokunin/157ee255/corpus/knowledge/memory-pressure-r25.md — this host's systemd-oomd `auto` reading and oomd defaults, cited and never absorbed; sha256 ecafdcdd1cc3417f5da40bf8dc9d46925e39550ec1be5baad0949e2458bdcd25, opened 2026-10-22); own-work host capture of 2026-10-22 (`.ufo/waves/round-26/capture/capture.txt` and `.ufo/waves/round-26/capture/capture-boots.txt`, committed; counts, states, thresholds and version strings only — no MESSAGE text, process name, uid, command line or `--avoid`/`--prefer` value was read or copied).
verified-at: 2026-10-22 — upstream sources opened as raw bytes at earlyoom tag v1.9.0 (commit 202d4db0d308ca6478f68de68b46cae34896ddaf) and at systemd tag v262; host observation read-only on 2026-10-22 (committed capture): earlyoom 1.9.0-1 active and enabled, systemd 262-1, systemd-oomd inactive and disabled, kernel 7.2.11-arch1-1; the package was installed on 2026-10-20, and the running earlyoom invocation began 2026-10-22 04:55:44 -03 (ActiveEnterTimestampMonotonic 19964362 µs) — that stamp is the current invocation, not a first activation.
recheck: `systemctl is-active earlyoom.service; systemctl is-enabled earlyoom.service; systemctl is-active systemd-oomd.service; systemctl is-enabled systemd-oomd.service; pacman -Q earlyoom systemd`; `journalctl -q -b -u earlyoom.service -o json --output-fields=MESSAGE,__MONOTONIC_TIMESTAMP` (classify in memory, keep counts); `journalctl -q -b MESSAGE_ID=d989611b15e44c9dbf31e3c81256e4ed -o json --output-fields=MESSAGE_ID | wc -l`; on an earlyoom release, re-open the five earlyoom files at the new tag and re-read the eight grammar literals; on a systemd release, re-open the v262 catalog anchor for d989611b…
author: MoriR26 (L1), from the wave-1 scribe draft `.ufo/waves/round-26/w1/DraftEntryR26.md`.

# Userspace OOM killers on this host — earlyoom is running, systemd-oomd is not, and what each one's record can and cannot prove

## Scope

This note records the two userspace OOM-killer services on this host — **earlyoom** and
**systemd-oomd** — as they are on 2026-10-22: which one is running, what each one does when it
acts, how each one's actions appear in the journal, and which of its lines are stable enough to
count. It exists because the previous entry on this ground
(`corpus/knowledge/userspace-oom-killers-r12.md`) said, in the present tense, that both services
are inactive here; that was true on 2026-10-19 and is false now.

It is a **reading** note. It describes service state, thresholds, log grammar and counting rules.
It does not enable, disable, start, stop, restart or tune either service, does not read or copy
`/etc/default/earlyoom` or any `--avoid`/`--prefer` expression, does not echo journal `MESSAGE`
text, and does not count processes killed by anyone.

Every fact below is tagged. **`verified`** — the statement holds on this host on the counted
evidence of 2026-10-22. **`scoped`** — it holds inside a stated limit the evidence does not cross.
**`[INFERENCE]`** — a reading that follows from the evidence but is not itself measured.

## Facts

**F1 — the host state, and the one that changed.** `earlyoom.service` is **active** and
**enabled**; `systemd-oomd.service` is **inactive** and **disabled**. The installed earlyoom is
**1.9.0-1** (Arch) and the installed systemd is **262-1**; the host kernel is `7.2.11-arch1-1`. The
earlyoom **package was installed on 2026-10-20**, and the **running invocation** began
`2026-10-22 04:55:44 -03` — that stamp is the current invocation's start, not a first activation,
and earlyoom is not new to this host.
*Verdict: `verified`* — the committed read-only capture
`.ufo/waves/round-26/capture/capture.txt` (lines with `unit_earlyoom.service_is_active=active`,
`unit_earlyoom.service_is_enabled=enabled`,
`unit_systemd-oomd.service_is_active=inactive`,
`unit_systemd-oomd.service_is_enabled=disabled`,
`unit_show_ActiveEnterTimestampMonotonic=19964362`, `package_earlyoom=1.9.0-1`,
`package_systemd=262-1`, `uname_release=7.2.11-arch1-1`), plus this seat's own read-only
`systemctl` and `pacman -Q` queries (§3.1) and the package install date from `pacman -Qi`
(§3.1).
*Limit:* this is a one-day snapshot of one host, not a fleet fact and not a standing property.

**F2 — the act rule is a conjunction, and the kill is staged.** earlyoom sends `SIGTERM` only when
**both** the available-memory percentage **and** the free-swap percentage are at or below their
SIGTERM limits, and sends `SIGKILL` only when **both** are at or below the lower SIGKILL limits.
The shipped defaults are **10 %** for the SIGTERM limit with the SIGKILL limit at **half** of it
(`PERCENT/2`), for memory and for swap alike.
*Verdict: `verified`* — the decision itself is upstream code (`main.c:500-503`, the `lowmem_sig()`
conjunction), the default pair is upstream code (`main.c:137-140`: 10 / 10 / 5 / 5) and the
half-rule is the upstream option parser (`msg.c:202`), and the prose agrees (`MANPAGE.md:41-45`,
`README.md:239-240`: "both memory and swap must be below minimum for earlyoom to act").
*Limit:* the half-rule applies when only one value is given for an option; an explicit
`PERCENT,KILL_PERCENT` pair overrides it.

**F3 — the percentages are not shares of total RAM.** "mem avail %" is
`MemAvailableKiB * 100 / UserMemTotalKiB`, where *user mem total* is `MemAvailable + AnonPages`;
"swap free %" is `SwapFreeKiB * 100 / SwapTotalKiB` and is forced to `0` when there is no swap at
all.
*Verdict: `verified`* — `meminfo.c:112-119`. The startup line prints both totals so a reader can
see the denominator in use.
*Limit:* because the swap percentage is `0` without swap, the swap half of the conjunction in F2
is then satisfied trivially and the decision rests on memory alone. **`[INFERENCE]`** — that
follows from the two source lines, not from an observation of a swapless host.

**F4 — earlyoom's actions are plain text, not catalog records.** earlyoom writes its warnings to
stderr and its informational lines to stdout; under this unit both land in the journal as records
whose `MESSAGE` is the raw line. Those records carry **no `MESSAGE_ID`** — in the current boot
12 of the 13 earlyoom records have no `MESSAGE_ID` field at all, and the single record that has
one is systemd's own unit-lifecycle line. Every record in the unit's slice carries
`PRIORITY 6`, including earlyoom's own `warn()` output, so **priority does not separate an action
line from a periodic report line**.
*Verdict: `verified`* — `msg.c:99-131` for the write targets, and the journal read in §3.2 for
the fields.
*Limit:* this is one host's systemd configuration; a unit with `StandardError=journal` would
give a different priority. **`[INFERENCE]`** — the priority is the manager's console stream
rather than the writer's own facility, because the unit inherits stderr; the cause was not
isolated.

**F5 — the lines that are stable enough to count, and the ones that are not.** The countable
classes are prefix-anchored literals from the v1.9.0 sources: the version line `earlyoom <version>`;
the two startup threshold lines `sending SIGTERM when mem avail <= <a>% and swap free <= <b>%,`
and `SIGKILL when mem avail <= <c>% and swap free <= <d>%`; the action lines
`sending SIGTERM to process ` and `sending SIGKILL to process `; the escalation line
`escalating to SIGKILL after `; the failure line `kill failed: `; the two low-memory lines
`low memory! at or below SIGTERM limits` and `low memory! at or below SIGKILL limits`; and the
dry-run flag `dryrun mode enabled`. Four constraints make these a counting grammar rather than a
parser:

- The action line's body carries a **uid, a process name and a full command line**. A reader
  counts it and **never copies it**. The same holds for the two startup filter-echo lines, which
  restate the configured prefer/avoid expressions: they are neither countable nor copyable.
- An **escalation prints no action line**: the daemon raises the signal it already decided on,
  so `escalating to SIGKILL after ` is a second signal on the same pid, not a new victim, and it
  is not a `sending SIGKILL to process ` record. The SIGKILL-action count and the escalation
  count are different populations.
- **`kill failed: `** covers two distinct causes — the signal call itself failing, and the
  ten-second wait for the victim to exit timing out. It therefore does **not** prove that no
  signal was delivered.
- The periodic `mem avail:` report and the `mem total:` startup line are **not actions**. Neither
  is `memory situation has recovered while selecting victim`, which is pressure evidence at a
  moment when no kill happened.

*Verdict: `verified`* — each literal and each constraint is upstream source at tag v1.9.0
(`main.c:161,295,414,416,519,523`; `kill.c:318,627,654`; `msg.h:10`), and the class separation was
checked against 273 retained earlyoom records (§3.2).
*Limit:* one percentage format, `"%5.2lf%%"`, right-aligns in five columns, so a one-digit
percent renders with a leading space (`<=  5.00%`). A grammar that expects a single space misses
the SIGKILL threshold line.

**F6 — the scope is the current invocation.** earlyoom's records for one invocation are the lines
whose `__MONOTONIC_TIMESTAMP` is at or above the unit's `ActiveEnterTimestampMonotonic`; the
completeness test is **whether the version line is inside that window**, not whether it is the
first line in it. On this host the unit's own start record lands 8 µs inside the bound and
precedes the version line by about 17 ms, and the two startup threshold lines carry the same
timestamp as each other.
*Verdict: `verified`* — `main.c:161` for the version literal, and the timestamps read in §3.2.
*Limit:* a service restart inside one boot moves the bound forward; the current boot shows one
invocation. **`[INFERENCE]`** — with a `Type=notify` unit the bound would move past the version
print, so the completeness test depends on the unit staying `Type=simple`.

**F7 — earlyoom's kills do not move the kernel's OOM counters, and on this host it could not
delegate to the kernel even if it wanted to.** earlyoom delivers the signal itself — a `kill(2)`
call on the victim pid, followed by a `pidfd` release — and never enters the kernel's OOM-victim
path, which is the only place the kernel increments `count_vm_event(OOM_KILL)` and
`memcg_memory_event_mm(mm, MEMCG_OOM_KILL)`. Therefore `/proc/vmstat`'s `oom_kill` and a cgroup's
`memory.events` `oom_kill` do not count earlyoom's kills. **The delegation exception that the
previous entry named does not exist in earlyoom 1.9.0**: the `-k` / kernel-OOM option was removed
in v1.2 and is ignored for compatibility, the v1.9.0 sources contain no such option, and the
installed binary on this host contains no such string and prints "Option -k is ignored since
earlyoom v1.2".
*Verdict: `verified`* — `kill.c:242` for the signal call and `kill.c:246-262` for the pidfd
release, against the kernel's increment site in `oom-kill-counter-kernel-only-r12.md` (upstream
v7.2 `mm/oom_kill.c:935-936`); the absence of the option is verified on the tag's sources and on
the installed binary's bytes (§3.3).
*Limit:* the kernel-side statement is anchored to the upstream v7.2 implementation the existing
entry opened; the host kernel is `7.2.11-arch1-1` and the distro source identity was not checked.
Upstream master has carried a kernel-OOM trigger option again since 2026-02-02, so that exception
is a statement about a **different, later build** and must not be carried into a note about the
1.9.0 that runs here.

**F8 — the systemd-oomd side.** systemd-oomd is inactive and disabled here, and every unit the
sibling lane captured — `user@1000.service`, `user-1000.slice`, `user.slice` and `-.slice` —
carries `auto` on both `ManagedOOMSwap=` and `ManagedOOMMemoryPressure=`, so nothing in that chain
would be monitored even if the service were started; `auto` is the upstream default and means the
cgroup's data is not actively used for monitoring and detection. systemd-oomd's own kill
accounting is the `user.oomd_ooms` and `user.oomd_kill` cgroup attributes plus a `Killed` D-Bus
signal, and its journal notice is the catalog id `d989611b15e44c9dbf31e3c81256e4ed` ("systemd-oomd
killed one or more processes in unit @UNIT@"). That notice has **0 occurrences in every retained
boot** on this host.
*Verdict: `scoped`* — the `auto` reading and the "systemd-oomd inactive and disabled" reading are
the sibling lane's dated capture, cited here and **not absorbed**: OS and unit diagnosis is
tsukuroi's ground (`PROVINCE.md` adjacency row), and the sibling's own verdict for that row is
`scoped` because it read four units, not the host. This seat's own read of the same four units on
2026-10-22 returned `auto` on both properties for all four, and its own read of the oomd notice
count returned 0 for every retained boot.
*Limit:* one notice means "one or more processes in a unit", never a process count; the notice
count is bounded by journal scope and retention.

**F9 — what the retained journals actually hold.** Counts only, classified in memory; no `MESSAGE`
text was read into any output. The **current boot** holds 13 earlyoom records: 1 version line, 2
threshold lines, 6 periodic reports, 1 memory-totals line, 2 filter echoes and systemd's own
unit-start record — and **0 action lines, 0 escalations, 0 failed kills, 0 low-memory warnings**.
The **previous boot** holds 252 earlyoom records, including **38 `sending SIGTERM to process`
lines and 1 `sending SIGKILL to process` line** (39 actions), 40 low-memory warnings (39 at the
SIGTERM limit, 1 at the SIGKILL limit), 1 "recovered while selecting victim" line, 39 signal
releases and 39 victim-exit lines — and **0 escalations and 0 failed kills**. The retained
journals hold exactly **1** kernel OOM summary and exactly **1** kernel "Killed process" record,
both in that same previous boot, timestamped about 39 minutes **after** earlyoom's last action
there.
*Verdict: `verified`* — the committed per-boot capture
`.ufo/waves/round-26/capture/capture-boots.txt` (`boot_index=0 … lines=13 version=1
term_thresholds=1 kill_thresholds=1 send_sigterm=0 send_sigkill=0 escalating=0 kill_failed=0
low_memory_sigterm=0 low_memory_sigkill=0 mem_avail_report=6`; `boot_index=-1 … lines=252
send_sigterm=38 send_sigkill=1 escalating=0 kill_failed=0 low_memory_sigterm=39
low_memory_sigkill=1 mem_avail_report=83`; `oomd_notices=0` on every boot), the committed
current-boot capture `.ufo/waves/round-26/capture/capture.txt`
(`journal_entries_in_scope=13`, `journal_scope_complete=1`, the per-class counts, the threshold
values 10.00/10.00 and 5.00/5.00, and `oomd_notice_count=0`), and this seat's own counts (§3.2).
*Limit:* the two records are distinct events; nothing here shows that the kernel record was or
was not a consequence of the same pressure episode. **`[INFERENCE]`** — the kernel OOM record is
**not** an earlyoom action: the timestamp ordering and the absence of any kernel-delegation option
in 1.9.0 (F7) both point that way.

## Decision table

Observable → what it means → what it does **not** mean.

| Observable | What acted | What it does NOT prove |
|---|---|---|
| a kernel-journal OOM summary (`oom-kill:constraint=`) or a kernel "Killed process" record, `_TRANSPORT=kernel` | the **kernel** OOM killer acted; the kernel's own OOM counters move at that path | that no userspace killer also acted in the same window — earlyoom's kills are invisible to those counters (F7) |
| a `sending SIGTERM to process ` or `sending SIGKILL to process ` line inside the current invocation's scope (F6) | **earlyoom** signalled a victim it selected | that the victim died (a `kill failed: ` line says the opposite is possible), that the kernel counters moved (F7), or the victim's identity — the line body carries a uid, a name and a command line and must not be copied |
| an `escalating to SIGKILL after ` line | earlyoom raised the signal on a pid it had already signalled — a **second signal on the same victim**, not a new victim, and **not** an action line | a new victim, or a SIGKILL-action count increase |
| a systemd-oomd notice with `MESSAGE_ID=d989611b…` | **systemd-oomd** killed one or more processes in a unit | a process count (the notice says "one or more"), or that the kernel counters moved |
| a `low memory! at or below SIG… limits` line with no action line after it | earlyoom saw the limits breached and, this time, did not kill | that a kill happened; on this host one such line in the previous boot was followed by "memory situation has recovered while selecting victim" |
| `oom_kill=0` in `/proc/vmstat` or in a cgroup's `memory.events` | **no kernel OOM victim** in that counter's scope and window | that no memory-related kill happened: earlyoom's kills never touch those counters (F7), and systemd-oomd's kills are accounted in its own cgroup attributes (F8) |
| the `user.oomd_ooms` / `user.oomd_kill` cgroup attributes | systemd-oomd's own accounting of its kill attempts and killed pids | a durable event history: the attributes live and die with the cgroup path |
| no record of any kind, with earlyoom **active** | no **positive evidence** of a userspace-killer action in that scope and window | that nothing was killed; the counter surfaces and the journal are different populations, and a kill by any other actor is not visible here |
| earlyoom **inactive**, **absent** or **unreadable** | the killer's state is **unavailable**, not zero | that zero kills happened — unavailable is never `0`, and never "healthy" |
| a plain SIGKILL with none of the records above | an unclassified termination | that a userspace OOM killer acted; it may be a unit manager's action, an external signal, or a policy kill |

## Limits

- **One host, one day.** Every host reading is 2026-10-22 on this machine. The earlyoom
  **package was installed on 2026-10-20** and the first earlyoom record in journal retention is
  from that day, so the `2026-10-22 04:55:44 -03` stamp is the **current invocation's** start, not
  a first activation. This note says "active and enabled", never "active since".
- **One earlyoom version.** Every literal and every constraint is anchored at tag `v1.9.0`
  (commit `202d4db0d308ca6478f68de68b46cae34896ddaf`). Upstream master has moved since — it
  carries a kernel-OOM trigger option again, and its README documents message shapes the tag does
  not have. A different release may move the literals; re-read the sources at the new tag.
- **A counting grammar, not a parser.** The eight classes are prefix-anchored. A line that does
  not match a class is unclassified, and unclassified is not zero.
- **Counts, never text.** The action line carries a uid, a process name and a command line; two
  startup lines carry the configured prefer/avoid expressions. Only counts, states, thresholds and
  version strings leave this note.
- **The journal is the only surface read.** earlyoom exposes its own log, not oomd's cgroup
  attributes, not the D-Bus signal, and not the kernel counters. None of these surfaces sees the
  others.
- **Scope differences are not additive.** The earlyoom action counts are **invocation-horizon**
  numbers; the oomd notice count is a **boot-horizon** number; the kernel counter is a
  **counter-scope** number. They are never summed.
- **Detection and report only.** No service was started, stopped, enabled, disabled or tuned; no
  configuration file was read for its values; no package was installed or removed.
- **The vocabulary of the round-26 tool** (`active` / `inactive` / `absent` / `unavailable`,
  `KILLER_ACTED` / `KILLERS_QUIET` / `KILLERS_UNKNOWN`) is the tool's own contract, not
  earlyoom's or systemd's.

## What it changes for mori

- For the SKILL.md `Did something get killed?` decision row, the userspace-killer arm gains
  **earlyoom** as a class of its own, read from earlyoom's own journal records inside the
  current invocation, with the unavailable-not-zero rule intact: an inactive or unreadable
  earlyoom is `unavailable`, never `0`.
- For the `oom_kill=0` error-pattern row, the label stays **kernel-OOM-only**, and the two
  userspace killers' own counters and records are named beside it.
- The round-26 read tool `tools/mori-oom-killers.py` implements exactly the reading this note
  describes — the eight-line grammar, the current-invocation scope, the thresholds from
  earlyoom's own startup lines, the oomd notice count — and its live run on this host returns
  `KILLERS_QUIET` with earlyoom `active`, `grammar: verified-1.9.0`, thresholds
  10.00/10.00 and 5.00/5.00, all action counts `0`, and oomd `inactive` with 0 notices. A quiet
  verdict here means "no positive evidence from the killers that are readable", not "zero kills".
- For `corpus/README.md` and the FR10 row in `PROVINCE.md`, the "inactive on this host" summary
  is replaced by "earlyoom active and enabled, systemd-oomd inactive and disabled" with a date.
- The r12 entry's kernel-delegation sentence is corrected rather than carried: see F7 and §4.2.

## Adjacency

- `tsukuroi-shokunin/corpus/knowledge/memory-pressure-r25.md` at commit `157ee255` — this host's
  systemd-oomd reading, the `auto` semantics and the oomd defaults are **tsukuroi's** ground and
  are cited here, not absorbed (F8). Its MP4 row is the source of the "every captured unit is
  `auto`" statement and of the oomd-side limit; its verdict for that row is `scoped`.
- `corpus/knowledge/oom-kill-counter-kernel-only-r12.md` — owns the kernel-counter semantics this
  note cites in F7. This note does not restate the increment sites; it says which killer's
  actions do and do not reach them.
- `corpus/knowledge/kill-classes-by-message-id-r12.md` and
  `corpus/knowledge/kernel-oom-line-attribution-r12.md` — own the journal **catalog** classes
  (`fe6faa94…`, `d989611b…`, `98e32220…`) and the kernel-record attribution. earlyoom's own
  records carry no `MESSAGE_ID` (F4), so earlyoom's actions are counted by prefix and never enter
  a catalog class.

## Not claimed

- No claim that the stale 2026-10-19 statement was wrong about that date, only about the present.
- No claim about any earlyoom build other than 1.9.0, and no claim about upstream master.
- No claim that earlyoom prevented, caused or mitigated any kernel OOM event; the retained
  journals hold one of each and they are separate records (F9).
- No claim about a fleet, another host, or any other lane's service state.
- No claim that a cgroup's `oom_kill` is zero because nothing was killed (F7).
- No process count, victim identity, uid, command line, prefer/avoid expression or `MESSAGE` text.
```

## 3. Gates — commands run and their outputs

Everything below was run read-only on 2026-10-22. Nothing wrote outside this report file. The
**committed** captures under `.ufo/waves/round-26/capture/` are the round's host evidence and are
cited in the entry; this seat's own readings below corroborate them line for line.

### 3.0 The committed captures (the round's host evidence)

`.ufo/waves/round-26/capture/capture.txt` (committed, current boot) and
`.ufo/waves/round-26/capture/capture-boots.txt` (committed, per-boot counts), produced by the
HostCapture seat's `capture.sh` / `capture-boots.sh`, carry the round's host evidence; the entry's
F1 and F9 quote their lines. This seat's own readings below corroborate them line for line. The
capture writes counts, states, threshold values and version strings only.

### 3.1 Host state (the F1 evidence)

```
$ systemctl is-active earlyoom.service            → active
$ systemctl is-enabled earlyoom.service           → enabled
$ systemctl is-active systemd-oomd.service        → inactive
$ systemctl is-enabled systemd-oomd.service       → disabled
$ pacman -Q earlyoom systemd                     → earlyoom 1.9.0-1 / systemd 262-1
$ systemctl --version | head -1                    → systemd 262 (262-1-arch)
$ uname -r                                        → 7.2.11-arch1-1
$ systemctl show earlyoom.service -p LoadState,ActiveState,UnitFileState,ActiveEnterTimestampMonotonic
  LoadState=loaded  ActiveState=active  UnitFileState=enabled
  ActiveEnterTimestampMonotonic=19964362
$ systemctl show earlyoom.service -p ActiveEnterTimestamp
  ActiveEnterTimestamp=Thu 2026-10-22 04:55:44 -03
$ systemctl show systemd-oomd.service -p ActiveState,UnitFileState,ActiveEnterTimestampMonotonic
  ActiveState=inactive  UnitFileState=disabled  ActiveEnterTimestampMonotonic=0
$ pacman -Qi earlyoom | grep -E 'Install Date|Version'
  Version         : 1.9.0-1
  Install Date    : Tue 20 Oct 2026 09:16:28 AM -03
```

`ActiveEnterTimestampMonotonic=0` for the inactive oomd unit is the fact behind the "an inactive
unit puts the whole boot in scope" caveat in F6.

### 3.2 Journal census (the F4, F5, F6, F9 evidence)

Each command pipes straight into a Python reader that prints **counts and class names only**; no
`MESSAGE` value is printed, and none was copied into this report.

```
$ journalctl -q -b -u earlyoom.service -o json --output-fields=MESSAGE,__MONOTONIC_TIMESTAMP
  (classified in memory, prefix-anchored, counts only)
  boot  0 : records 13 → version 1, thresholds 2, periodic 6, mem_total 1, filter_echo 2,
                       systemd_unit_record 1; sigterm 0, sigkill 0, escalations 0,
                       kill_failed 0, low_memory 0, dryrun 0
  boot -1 : records 252 → version 1, sigterm 38, sigkill 1, low_memory 40 (39 SIGTERM-limit,
                       1 SIGKILL-limit), escalations 0, kill_failed 0, kill_release 39,
                       exited 39, recovered 1, plus periodic/total/filter/unit records
  boot -2 : records 8  → version 1, thresholds 2, no actions
$ journalctl -q -b -u earlyoom.service -o json --output-fields=MESSAGE_ID
  boot 0: 1 of 13 records carry a MESSAGE_ID (systemd's own unit-start line); 12 carry none
  boot -1: 5 of 252 carry one (all systemd's); the 247 earlyoom records carry none
$ journalctl -q -b -u earlyoom.service -o json --output-fields=MESSAGE,PRIORITY,SYSLOG_IDENTIFIER,_COMM
  every record in the unit slice: PRIORITY 6
  earlyoom's own records: SYSLOG_IDENTIFIER=earlyoom, _COMM=earlyoom
  systemd's own records: SYSLOG_IDENTIFIER=systemd, _COMM=systemd
$ journalctl -q -b -u earlyoom.service -o json --output-fields=MESSAGE,__MONOTONIC_TIMESTAMP
  boot 0: ActiveEnterTimestampMonotonic=19964362
         systemd's unit-start record  19964370   (+8 µs inside the bound)
         earlyoom version line        19981126   (+16.764 ms)
         both threshold lines         19981234   (same timestamp)
$ journalctl -q -b MESSAGE_ID=d989611b15e44c9dbf31e3c81256e4ed -o json --output-fields=MESSAGE_ID | wc -l
  boot 0 → 0;  and 0 in every retained boot (-5 … 0)
$ journalctl -q -b -u systemd-oomd.service -o json --output-fields=MESSAGE_ID | wc -l
  0 in every retained boot (-5 … 0)
$ journalctl -k -b all -q --grep='^oom-kill:constraint=' -o json --output-fields=_BOOT_ID | wc -l   → 1
$ journalctl -k -b all -q --grep='(Out of memory|Memory cgroup out of memory): Killed process [0-9]+'       -o json --output-fields=_BOOT_ID | wc -l                                                        → 1
  the single kernel record sits in boot -1 at 2026-10-22T03:54:59-03:00
  earlyoom's last action in that boot is at 2026-10-22T03:16:05-03:00   → kernel record is ~39 min later
$ grep '^oom_kill ' /proc/vmstat                                  → oom_kill 0   (current boot)
$ cat /sys/fs/cgroup/user.slice/memory.events | grep oom_kill      → oom_kill 0
```

### 3.3 The round-26 tool (corroboration, another seat's work)

The C2 tool `tools/mori-oom-killers.py` (landed by the tool seat, committed `c2fdd92`) reads this
host the way this entry describes. Its committed receipts:
`.ufo/waves/round-26/evidence/c2-selftest.txt` → `MORI_OOM_KILLERS_SELFTEST: PASS 32/32`, exit 0;
`.ufo/waves/round-26/evidence/c2-live-run.txt` → exit 0, `verdict: KILLERS_QUIET`, earlyoom
`active` / `grammar: verified-1.9.0` / `scope_complete: true` / thresholds 10.0, 10.0, 5.0, 5.0 /
all five action counts 0 / `dryrun: false`, oomd `inactive` with `notices_this_boot: 0`. This
seat did not build or run the tool; the entry cites the receipts.

### 3.4 The installed binary (the F7 evidence)

Read as bytes only; the binary was never executed.

```
$ python3 -I -B -c "…read /usr/bin/earlyoom as bytes and count literals…"
  size 43520
  b'kernel-oom'                            0 matches
  b'--kernel-oom'                          0 matches
  b'sending %s to process'                 1 match
  b'sending SIGTERM when mem avail'        1 match
  b'low memory! at or below SIGTERM limits' 1 match
$ strings -a /usr/bin/earlyoom | grep -c 'kernel-oom'   → 0
$ strings -a /usr/bin/earlyoom | grep -n 'Option -k'    → 255:Option -k is ignored since earlyoom v1.2
```

### 3.5 Upstream fetches (all ordinary `curl`, no browser, no challenge)

Access date 2026-10-22 for every URL. Digests and quotes:

| file | URL | sha256 |
|---|---|---|
| earlyoom README.md | `https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/README.md` | `23411dbfd8b409d433f984a5d6677830e86a383ec76935fc1e1d675e6b4374dd` |
| earlyoom main.c | `…/v1.9.0/main.c` | `08656b0bc90c85f23738661456b25c97af908bc5e2cfea78e0a69697b5f9d0e4` |
| earlyoom kill.c | `…/v1.9.0/kill.c` | `b32e0fad65e298235102f98aff37e02c94400b544d454cb57192ae697b100bf3` |
| earlyoom msg.c | `…/v1.9.0/msg.c` | `a771c91529053341c290ede2a7df1d9fdf16e07fb9584db8a64604a45dea5197` |
| earlyoom msg.h | `…/v1.9.0/msg.h` | `e36604984a916fb00a624c27c73034bcd87d7d6facff9b290a6a561ee58de56c` |
| earlyoom meminfo.c | `…/v1.9.0/meminfo.c` | `526e512c89c58cb0b1db2ae98ea62d287cdc1516846be80c9173bdc4bf0edfeb` |
| earlyoom MANPAGE.md | `…/v1.9.0/MANPAGE.md` | `cc48b02e79255ae27bad9b2c49364fcae1b6b5eb20fe8e83ecef432f360dfeda` |
| earlyoom earlyoom.service.in | `…/v1.9.0/earlyoom.service.in` | `d4019b66d87539a006fc2d178d972dcf1b46e70343627b8bf66d1a08dcdda0bd` |
| systemd resource-control.xml | `https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd.resource-control.xml` | `d57641df40e45811403de91e55059b6a8f7506c6812a85cbe9c6ba22900587d8` |
| systemd systemd-oomd.service.xml | `…/v262/man/systemd-oomd.service.xml` | `4b29be2e41ef309beb9f9a9fcc9a84f18cd7f9f3540f094b0b5717891ef8651d` |
| systemd oomd-util.c | `…/v262/src/oom/oomd-util.c` | `2e94450aa337dd7d2062f2730e46e22ac00fc2c3195c11654047ddcaba487e7a` |
| systemd systemd.catalog.in | `…/v262/catalog/systemd.catalog.in` | `e53707db7e6963b284e504dc17f36a4d5a2bdb4bd8a9611b2cf95c075ad86592` |
| tsukuroi memory-pressure-r25.md | `https://raw.githubusercontent.com/VeigaPunk/tsukuroi-shokunin/157ee255/corpus/knowledge/memory-pressure-r25.md` | `ecafdcdd1cc3417f5da40bf8dc9d46925e39550ec1be5baad0949e2458bdcd25` |

Tag provenance: `git ls-remote https://github.com/rfjakob/earlyoom refs/tags/v1.9.0` →
`66d78843fd675859a09a52d3f17b1c408a827a34` (annotated tag object); `git ls-remote … 'refs/tags/v1.9.0*'`
→ `refs/tags/v1.9.0^{}` = commit `202d4db0d308ca6478f68de68b46cae34896ddaf`. The
`https://github.com/rfjakob/earlyoom/releases` page returned HTTP 200 on 2026-10-22, and the
public commits API for `main.c` (`https://api.github.com/repos/rfjakob/earlyoom/commits?path=main.c&per_page=20`)
lists the kernel-oom option commit `750a7c0d97bb` dated `2026-02-02T05:00:04Z` with the subject
"kill: option for triggering kernel oom killer" — **after** the v1.9.0 tag of 2025-09-16. Both
were read by ordinary `curl`/git, no browser and no challenge.

Quotes used (each ≤ 25 words, verbatim, with its line):

- `README.md:28` — "By default if both are below 10%, it will kill the largest process (highest `oom_score`)."
- `README.md:239-240` — "Note: both memory and swap must be below minimum for earlyoom to act."
- `README.md:154` — "Every action is logged to stderr."
- `README.md:383` — "Remove option to use kernel oom-killer (`-k`, now ignored for compatibility)"
- `MANPAGE.md:31` — "set available memory minimum to PERCENT of `user mem total` (default 10 %)."
- `MANPAGE.md:41-42` — "earlyoom sends SIGTERM once **both** available memory **and** free swap are below their respective PERCENT settings."
- `MANPAGE.md:44-45` — "It sends SIGKILL once **both** are below their respective KILL_PERCENT setting (default PERCENT/2)."
- `main.c:500` — `if (m->MemAvailablePercent <= args->mem_kill_percent && m->SwapFreePercent <= args->swap_kill_percent)`
- `main.c:502` — `else if (m->MemAvailablePercent <= args->mem_term_percent && m->SwapFreePercent <= args->swap_term_percent)`
- `main.c:137-140` — `.mem_term_percent = 10,` / `.swap_term_percent = 10,` / `.mem_kill_percent = 5,` / `.swap_kill_percent = 5,`
- `main.c:161` — `fprintf(stderr, "earlyoom " VERSION "\n");`
- `main.c:414` / `main.c:416` — the two startup threshold literals
- `main.c:519` / `main.c:523` — the two low-memory literals
- `main.c:295` — `warn("dryrun mode enabled, will not kill anything\n");`
- `kill.c:318` — `warn("escalating to SIGKILL after %.3f seconds\n", secs);`
- `kill.c:627` — `warn("sending %s to process %d uid %d \"%s\": oom_score %d, oom_score_adj %d, VmRSS %lld MiB, cmdline \"%s\"\n",`
- `kill.c:654` — `warn("kill failed: %s\n", strerror(saved_errno));`
- `kill.c:242` — `int res = kill(pid, sig);`
- `msg.c:202` — `tuple.kill = tuple.term / 2;`
- `msg.c:104` — `logger(LOG_WARNING, stderr, yellow, fmt, vl);`
- `msg.h:10` — `#define PRIPCT "%5.2lf%%"`
- `meminfo.c:112` / `:115` / `:117` / `:119` — the user-mem-total and the two percentage lines
- `resource-control.xml:1545-1547` — "When set to `auto`, `systemd-oomd` will not actively use this cgroup's data for monitoring and detection."
- `systemd-oomd.service.xml:43-44` — "Cgroups of units with `ManagedOOMSwap=` or `ManagedOOMMemoryPressure=` set to `kill` will be monitored."
- `systemd.catalog.in:884-885` — "`-- d989611b15e44c9dbf31e3c81256e4ed`" / "Subject: systemd-oomd killed one or more processes in unit @UNIT@"
- `logs-show.c:554` / `:1456` / `:1459` — the `MESSAGE=` parse and the requested-field emission
- tsukuroi `memory-pressure-r25.md:204-208` — the four captured units and their `auto` reading

## 4. Findings for the L1

### 4.1 The SOURCES ids used in the draft

The draft's `source:` line already carries the L1's assigned ids, so no renumbering is needed in
the entry text:

`S114` earlyoom v1.9.0 README · `S115` earlyoom v1.9.0 MANPAGE.md · `S116` earlyoom v1.9.0
meminfo.c · `S117` earlyoom tag history · `S118` earlyoom v1.9.0 kill.c + msg.c · `S119` earlyoom
v1.9.0 main.c · `S120` earlyoom v1.9.0 unit template + the installed Arch package · `S121`
systemd v262 oomd-util.c + message catalog · `S122` systemd v262 journal documentation ·
`S123` systemd v262 logs-show.c + utf8.c · `S124` systemd v262 resource-control + systemd-oomd
manual pages · `S125` tsukuroi `memory-pressure-r25.md` at commit `157ee255` (sibling, cited
never absorbed).

`corpus/SOURCES.md` ends at **S113** (113 rows; the last row is at file line 119), so every id
above is **new in round 26** and satisfies the contract's "a `source:` line cites at least one
`corpus/SOURCES.md` row opened in round 26" — re-derivable with
`git show 248408f5:corpus/SOURCES.md | grep -oE '^\| S[0-9]+' | sort -V | tail -1` → `| S113`.
Sibling seats have drafted the same sources (`SrcEarlyoomReadme`, `SrcEarlyoomKillC`,
`SrcEarlyoomManpage`, `SrcEarlyoomMeminfo`, `SrcOomdUtilV262`, `SrcSiblingTsukuroi`, and the
still-running `SrcEarlyoomMainC`, `SrcEarlyoomUnit`, `SrcResourceControlV262`); the L1 should
confirm that each admitted row's `used-by` names `corpus/knowledge/userspace-oom-killers-r26.md`.

`msg.h` (`PRIPCT`) is quoted inside F5 and belongs with the `S118` msg.c row; this seat opened
and digested it separately (sha256 `e36604984a916fb00a624c27c73034bcd87d7d6facff9b290a6a561ee58de56c`).

### 4.1b Two rows this seat did not open itself

`S122` (journal documentation) and `S123` (logs-show.c + utf8.c) were assigned by the L1. For
`S123` this seat fetched and digested the two files itself on 2026-10-22 and re-scoped the
description to what the bytes support: `logs-show.c:554` parses `MESSAGE=`, `:1456`/`:1459` emit
`MESSAGE` and each requested `--output-fields=` entry, and `utf8.c:16,105,129,152` hold the
UTF-8 validation and escaping helpers. **The claim that `MESSAGE_ID` is present only on catalog
records is not derived from these two files** — it is the host observation in F4 (12 of 13
boot-0 records carry no `MESSAGE_ID`; the one that does is systemd's own line) plus the
`systemd.journal-fields(7)` semantics in `S122`. If the L1 wants that claim sourced from code, the
emission site is in journald, not in `logs-show.c`; this seat did not locate it and does not
assert it.

### 4.2 A correction the r12 entry needs, which this draft does not carry forward

`corpus/knowledge/userspace-oom-killers-r12.md:11` states that earlyoom "logs its own actions;
only `--kernel-oom` delegates to the kernel OOM killer", citing S016 (the upstream **master**
README at commit `8477c902`). That master README does contain `--kernel-oom`, but the option was
added upstream on 2026-02-02 (commit `750a7c0d97bb`), **after** the v1.9.0 tag this host runs.
Verified here three ways: the v1.9.0 sources contain no such option and `-k` prints "Option -k is
ignored since earlyoom v1.2"; the installed binary contains **0** occurrences of `kernel-oom`; and
the host package is `earlyoom 1.9.0-1`. The sentence is therefore true of a different, later
build, not of the binary on this host, and F7 states the narrower true fact. **This is content, not
wording** — it belongs in the r12 rewrite (`DraftR12Corrections` seat) and in the `teaches` cell
of S016 if the L1 touches it. It is not a contract contradiction: the contract's C2 grammar never
mentions `--kernel-oom`.

### 4.3 The "since" nuance in the C1 statement

The C1 statement in the contract frames earlyoom as active "since 2026-10-22 04:55:44 -03". That
stamp is the **current invocation's** start. The package was installed 2026-10-20 09:16:28 and the
first earlyoom record in journal retention is 2026-10-20 09:20:41, in the boot before last. The
draft's Limits section says so explicitly ("the current invocation, not the first activation"), and
F1 says "the running earlyoom invocation began" rather than "has been active since". The L1 should
keep that wording in the r12 and README rewrites.

### 4.4 Two lines the C1 counter will not see

The four frozen phrases are the r12 claim line, the r12 host-state bullet, the r12 "Observed" line
and the `corpus/README.md` row. Two further present-tense statements in the same r12 entry are
outside the frozen list and would survive a four-phrase-only rewrite: the `## Claim` sentence's
"a probe must render `unavailable (inactive)`, never a zero-kill result" (true, but now stated
about an inactive oomd and an **active** earlyoom) and the `## Observed` sentence "earlyoom's
service unit is not found". `DraftR12Corrections` covers this ground; flagging it here so the
rewrite is complete rather than phrase-complete.

### 4.5 The learning claim, stated

C1's learning content is **a stronger entry superseding a weaker one**, and the draft is stronger
in four measurable ways: (i) it replaces a stale present-tense host state with a dated,
independently measured one; (ii) it adds the eight-line counting grammar with the four
constraints that make it a counting rule (the escalation, the failure line, the report line and
the recovered line) — none of which the r12 entry had; (iii) it adds the action-vs-kernel-counter
separation with the source path that explains it; (iv) it corrects the kernel-delegation sentence
that the r12 entry carried from a later upstream build. A stub with a `source:` line would print
`stale_present=0` and `r26_entry=present` too; the draft's substance is what makes the claim a
learning claim.

## 5. Out of scope for this seat

- Landing the entry, writing `corpus/SOURCES.md`, renumbering ids, editing r12 or
  `corpus/README.md`, and the SKILL.md decision row — all L1 or sibling-seat work.
- Building, freezing or running the C2 tool and its cases — other seats' work. This seat only
  cites the committed receipts under `.ufo/waves/round-26/evidence/` as corroboration (§3.3).
- The r12 rewrite wording (`DraftR12Corrections`), the SKILL.md section (`DraftSkillFr10`), and
  the hygiene entries (`DraftHygieneKnowledge`, `DraftHygieneScorecard`).
- Enabling, disabling, tuning or reading `/etc/default/earlyoom`; running oomd; any write to a
  unit file, a journal or a configuration file.

## 6. Tooling and environment

No tool was installed or upgraded by this seat: the task needed only `curl`, `python3` (3.14.8),
`git` (2.56.0, read-only), `sha256sum` and `strings`. Per the operator directive I would have
installed through the pacman channel, but pacman transactions are paused host-wide for this round
and nothing was missing, so no install was needed and none was performed. No `uv tool` package,
no binary download. Record of the operator directive is here so the L1's report can state it.

## 7. Note on length

The round-26 item asks for a report under 300 lines; this report is longer because it carries the
**complete paste-ready entry** (the deliverable), which is ~270 lines on its own. The round-25
precedent for the same seat and the same kind of deliverable is
`.ufo/waves/round-25/w1/KnowledgeDraftC2.md` (621 lines, same §-numbered shape). The entry text is
verbatim between the ```markdown fence; everything outside it is the evidence.

## 8. Artifacts

| Artifact | Path | Note |
|---|---|---|
| This report | `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-26/w1/DraftEntryR26.md` | the only lane write |
| Draft target (NOT written) | `corpus/knowledge/userspace-oom-killers-r26.md` | L1 lands it from §2 |
| Upstream fetch scratch (outside the lane) | `/fast/scratch/hyaku/mori-r26/DraftEntryR26/` | the five earlyoom files, the four systemd files and the sibling entry, digests in §3.4 |
| Sibling source rows to renumber against | `.ufo/waves/round-26/w1/SrcEarlyoomReadme.md`, `…/SrcEarlyoomKillC.md`, `…/SrcEarlyoomManpage.md`, `…/SrcEarlyoomMeminfo.md`, `…/SrcOomdUtilV262.md`, `…/SrcSiblingTsukuroi.md` | other seats' work, cited not copied |
| Sibling entry (read-only) | `tsukuroi-shokunin/corpus/knowledge/memory-pressure-r25.md` at commit `157ee255` | cited, not absorbed |
