# CriticEntryOverclaim — round 26 wave 2 (falsify)

Target: `corpus/knowledge/userspace-oom-killers-r26.md` at lane tip `16935e24c93fa7e7567413d7ec091339a5df1474`.
I read it with `git show 16935e24:<path>`, not from the working tree. Line numbers are from that blob.
The task: find overclaims (universal words, `verified` resting on inference, decision-table rows the
tool does not implement, any wording implying earlyoom never acted, any "active since"). Each finding
names its target, the evidence, a verdict, and a narrower wording.

Summary: 15 findings. 4 are medium-severity defects, 9 are low-severity defects, and 2 hold. One check was not run.
No finding touches the counted values of C1 or C2. All of them are wording or provenance fixes in the entry.

## Medium-severity defects

**O1 — "implements exactly the reading this note describes" (lines 238-243).** Defect (medium).
Counterexample: the tool reads only the current boot (`tools/mori-oom-killers.py:493-505`, `journalctl -q -b -u
earlyoom.service`; the oomd count at `:528-539` is also `-b`). Its `earlier_invocation_send_lines` covers only
lines in that boot from before the current invocation (`:307-319`). The previous boot holds `send_sigterm=38 send_sigkill=1`
(`.ufo/waves/round-26/capture/capture-boots.txt:17`), and the tool cannot see those lines. It also reads none of
these: kernel journal records, `/proc/vmstat`, `memory.events`, `user.oomd_ooms`/`user.oomd_kill`. Those are
decision-table rows at entry lines 192, 197 and 198. It also has rules the note does not describe: the
`Suppressed … messages from earlyoom.service` rule (`:364-365,376-378`), process-group lines (`:362-363`), the
dry-run diversion (`:367-374`), and the zero/missing `ActiveEnterTimestampMonotonic` rule (`:278-286`).
Proposed: "The round-26 read tool implements the earlyoom-journal and oomd-notice parts of this reading, for
the **current boot only**: the grammar in F5 plus the A2 rules (process-group lines, journald suppression,
dry-run), the current-invocation scope, the thresholds and the oomd notice count. It does not read kernel
records, the kernel counters or oomd's cgroup attributes, and it cannot see earlier boots."

**O2 — the live-run sentence reads as "earlyoom has not acted" (lines 240-243).** Defect (medium).
The entry quotes `KILLERS_QUIET` with "all action counts `0`" and gives no horizon. The receipt
(`.ufo/waves/round-26/evidence/c2-live-run.txt:8-17,35`) is for the current invocation of the current boot.
The previous boot had 39 send lines (`capture-boots.txt:17`), the last at 2026-10-22T03:16:05-03:00
(`.ufo/waves/round-26/w1/DraftEntryR26.md`, §3.2 transcript). The sentence "not 'zero kills'" (line 243)
does not say *when*. Proposed: "…all action counts `0` **for the current invocation (since 2026-10-22
04:55:44 -03, this boot)**. In the previous boot, which the tool does not read, earlyoom logged 38 SIGTERM and
1 SIGKILL send lines (F9). A quiet verdict means no positive evidence in the current invocation from
the killers that are readable. It does not mean zero kills, and it says nothing about earlier boots."

**O3 — the decision-table row for an inactive, absent or unreadable earlyoom (line 200) contradicts the tool.** Defect (medium).
The row says "the killer's state is **unavailable**". The tool maps `inactive` to `inactive` and `not-found`
to `absent`. It uses `unavailable` only for a missing show, a missing `ActiveState`, or a transitional
state (`:191-212`). For an inactive or absent unit it reports `actions: null`, and the verdict can be
`KILLERS_QUIET` with exit 0 (contract rule 3, `contract.md:102-104`). The tool also counts this boot's lines
for an earlyoom that is not active: send lines found there give `KILLER_ACTED` (`:419-423`; contract A2
"Earlier invocations"), so that state is not merely "unavailable". The tool can also print
`earlier_invocation_send_lines: 0` for an inactive earlyoom (`:307-319`), which is a literal zero beside
"unavailable is never `0`". Proposed row: "earlyoom **inactive** or **absent** | no current invocation:
state `inactive`/`absent`, `actions: null` (unavailable, not zero). Send lines earlier in this boot are
still positive evidence | that zero kills happened. **Unreadable** (state `unavailable`) gives
`KILLERS_UNKNOWN`, never quiet."

**O4 — the decision-table row for a send line (line 193) leaves out dry-run and process groups.** Defect (medium).
"earlyoom signalled a victim it selected" is false under `--dryrun`. In that mode the send line is still
printed (`kill.c:627` at v1.9.0) but the code logs "dryrun, not actually sending any signal" (`kill.c:271-273`).
The tool diverts those lines (A6, `:367-374`). With `-g`, one line signals a whole process group
(`kill.c:282`). Proposed: "**earlyoom** signalled the selected victim — unless the invocation logged
`dryrun mode enabled` (then nothing was sent). Under `-g`, a `killing whole process group ` line means the
signal went to a group, not one process."

## Low-severity defects

**O5 — F4 calls the priority claim `verified` when no warn() output was observed (lines 70-74).** Defect (low).
The text says "Every record in the unit's slice carries `PRIORITY 6`, including earlyoom's own `warn()` output". The only priority
read is `journalctl -q -b -u earlyoom.service … PRIORITY` (DraftEntryR26 §3.2), and `-b` means the current boot.
That boot's 13 records are: version, thresholds, mem total and filter echoes, all written by `fprintf(stderr)`
(`main.c:161,379-386,412-416`); periodic reports from `print_mem_stats(info, …)` (`main.c:542`); and one systemd record.
**None of them is `warn()` output.** The action lines (`kill.c:627`) and low-memory lines (`main.c:519,523`) are
`warn()`, and they exist only in boot -1, where no priority read was recorded. The conclusion does hold by
source: systemd sets one stream priority, `context->syslog_priority`, for any journal-connected fd
(systemd v262 `src/core/exec-invoke.c:249`, inside `connect_logger_as` at `:208`). earlyoom adds no level prefix unless it is in
syslog mode (`msg.c:66-69`). Proposed: "Every record observed in the current boot carries `PRIORITY 6`. That
boot holds no `warn()` line. By source, the unit's stream priority (`SyslogLevel=`, default info) applies to
stdout and stderr alike (systemd v262 `exec-invoke.c:249`), so action lines get the same priority
**`[INFERENCE]`** until a boot holding action lines is read."

**O6 — F4's limit sentence is contradicted by systemd source (lines 76-79).** Defect (low).
The sentence "a unit with `StandardError=journal` would give a different priority" is untagged and wrong
for v262: both streams use the same `context->syslog_priority` (`exec-invoke.c:249`). What really changes the priority is
`SyslogLevel=`, `SyslogLevelPrefix=` with a `<N>` prefix, or earlyoom's syslog mode (`msg.c:68-69`, `vsyslog`).
Proposed: "a unit with a different `SyslogLevel=`, or earlyoom run in its syslog mode, would give a
different priority."

**O7 — F7 says earlyoom "never enters the kernel's OOM-victim path, which is the only place…" (lines 124-126).** Defect (low).
earlyoom calls `process_mrelease` after the kill (`kill.c:251`). [INFERENCE] That syscall is defined in the
kernel's `mm/oom_kill.c` and runs the OOM reaper's teardown, so "never enters" is broader than what is true. The true
claim is that it never reaches the victim-*selection and kill* code where the counters increment. "The only place"
rests on `oom-kill-counter-kernel-only-r12.md`, not on any read made this round. The entry also calls the
mrelease "a `pidfd` release" (line 125) and "signal releases" (line 167); it is a memory release. **Not run:**
fetching upstream `mm/oom_kill.c` at v7.2 returned HTTP 429, so the location of `process_mrelease` was not
confirmed. Proposed: "…and never calls the kernel's OOM kill routine, which is where the kernel increments
`count_vm_event(OOM_KILL)` and `MEMCG_OOM_KILL` (per `oom-kill-counter-kernel-only-r12.md`). Its follow-up
`process_mrelease` only frees the dying victim's memory and does not touch those counters **`[INFERENCE]`**."
In F9, "39 signal releases" should become "39 `process_mrelease` success lines".

**O8 — F9 treats the two kernel lines as distinct events and calls them "one of each" (lines 169-171, 181-184, 267-268).** Defect (low).
Line 181 says "the two records are distinct events". Right after "1 kernel OOM summary and 1 kernel 'Killed process'
record", "the two records" reads as those two kernel lines. [INFERENCE] A kernel OOM kill prints the
`oom-kill:constraint=` summary and the `Killed process` line for the same kill, so they are one event. The
draft's transcript places a single kernel record in boot -1 (DraftEntryR26 §3.2). Proposed: "the two kernel
lines are the summary and the victim line of **one** kernel OOM kill **`[INFERENCE]`**. That kill and earlyoom's
last action are distinct events, about 39 minutes apart." At line 268, "one of each" should become "one kernel OOM kill".

**O9 — `verified` verdicts point to sections and counts that are not in the entry or the committed captures (lines 41-42, 107, 180, 246).** Defect (low; provenance).
`§3.1`, `§3.2`, `§3.3` and `§4.2` are sections of `.ufo/waves/round-26/w1/DraftEntryR26.md`, not of this entry. "This seat's own"
(lines 41, 180) names a seat that is not the entry's author (line 4: MoriR26). Several facts appear in neither
`capture.txt` nor `capture-boots.txt`: the install date (F1, line 31), the 8 µs and 17 ms offsets (F6), the kernel
counts and the 39-minute gap, and the 39 release and exit lines (F9). The capture keys are listed at `capture.txt:4-71` and
`capture-boots.txt:9-20`, where boot -1 shows only `other=87`. They rest on the draft's transcript. That transcript
records `journalctl -q -b -u …` (current boot) yet reports boot -1 and boot -2 figures, so the command shown cannot
produce the numbers shown. Proposed: replace each `§3.x` with
"`.ufo/waves/round-26/w1/DraftEntryR26.md` §3.x (wave-1 scribe transcript, not a committed capture)". Change
F1's and F9's verdicts to `verified` for the capture-backed keys and `scoped` (transcript-only) for the rest.

**O10 — "The journal is the only surface read … None of these surfaces sees the others" (lines 218-220).** Defect (low).
This is false on both counts. F1 reads `systemctl` and `pacman`, F7 reads the installed binary's bytes, F8 reads unit
properties (`capture.txt:25-34`), and the draft read `/proc/vmstat` and `user.slice/memory.events` (§3.2). The journal *does* hold the oomd
notice (`d989611b…`) and the kernel OOM records, as F8 and F9 count them. Proposed: "**earlyoom's evidence is its
journal only.** earlyoom does not write oomd's cgroup attributes, the D-Bus signal or the kernel counters. The
journal holds earlyoom lines, oomd notices and kernel OOM records side by side, but each counter surface sees only
its own killer."

**O11 — "eight classes" and "eight grammar literals" do not match F5's list or the tool (lines 3, 213, 239).** Defect (low).
F5 (lines 82-88) lists ten literals: version, two thresholds, two send lines, escalation, kill failed, two
low-memory lines, and dry-run. The tool has those ten classes (`:84-93`) plus process-group and suppression (`:118-121`).
Proposed: "the ten prefix-anchored literals of F5 (twelve with the A2 process-group and suppression rules)".

**O12 — "the completeness test is whether the version line is inside that window" (lines 114-115).** Defect (low).
The tool applies more conditions: `scope_complete = scope_known and version is not None and not suppressed`
(`:378`), and `scope_known` needs a non-zero `ActiveEnterTimestampMonotonic` (`:278-288`). Contract A2 also discloses head
truncation as undetected (`contract.md:170-172`, X8). Proposed: "a **necessary** condition is the version line inside
the window. The tool also requires a non-zero `ActiveEnterTimestampMonotonic` and no journald
`Suppressed … messages from earlyoom.service` line in scope. Loss of earlier lines by truncation or retention is
not detected."

**O13 — "nothing in that chain would be monitored even if the service were started" (lines 143-146).** Defect (low).
The capture lists four units only (`capture.txt:25,34`). Units below `user@1000.service` and the `system.slice`
units were not read, and the sentence also depends on unit drop-ins staying as captured. Proposed: "none of the
four captured units would be monitored with the properties as captured. Units outside those four were not read."

**O14 — "No claim … about upstream master" (line 266) contradicts lines 139 and 210-211.** Defect (low; self-contradiction).
Both lines make claims about master (a kernel-OOM option "since 2026-02-02", README message shapes). Proposed:
"No claim about upstream master beyond the dated pointer in F7 and Limits (the option's addition commit, per S016)."

**O15 — the tag definitions and output rules overstate the note (lines 22-24, 215-217).** Defect (low).
Line 22 says "Every fact below is tagged", but the decision-table rows and "What it changes" carry no tag. The
`verified` definition, "holds on this host on the counted evidence", does not fit F2, F3, F5 and F7, which are
upstream-source facts. Lines 216-217 say "Only counts, states, thresholds and version strings leave this note",
but the note also carries timestamps, dates, durations and checksums. Proposed definition: "`verified` — read
directly from the cited upstream bytes or the committed capture". Proposed output rule: "…counts, states, thresholds,
version strings and timestamps".

## Holds

- **H1 — "active since" (line 208; also lines 2, 32-33).** Holds. The only occurrence names the wording it rejects
  ("never 'active since'"). The stamp is called "the current invocation's start". Supporting data:
  `capture-boots.txt:15` shows boot -2 with `lines=8 version=1`. Its first record is 2026-10-20 08:58 -03
  (`date -d @1792497480`). Boot -1 runs 2026-10-20 09:57 to 2026-10-22 04:54 -03 (`:6-7`). This matches
  "installed 2026-10-20" and "not new to this host". One residual risk: the install date itself is transcript-only (O9).
- **H2 — F9's previous-boot counts (lines 161-168).** Holds against `capture-boots.txt:17` (38, 1, 0, 0, 39, 1). The
  273 total equals 8 + 252 + 13 (`:15,17,19`). Line 15, "true on 2026-10-19", is consistent with boots -5 and -4 having
  `lines=0` (`:9,11`), the first of which starts 2026-10-19 18:55 -03.

## Not run

- Upstream kernel `mm/oom_kill.c` at v7.2 (O7, O8): `curl` returned HTTP 429. The `process_mrelease` location and the
  pairing of the summary line with the victim line stay `[INFERENCE]`.

## Evidence fetched (ordinary curl, scratch `/fast/scratch/hyaku/mori-r26/CriticEntryOverclaim/`)

| file | URL | sha256 |
|---|---|---|
| msg.c | https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/msg.c | a771c91529053341c290ede2a7df1d9fdf16e07fb9584db8a64604a45dea5197 |
| kill.c | …/earlyoom/v1.9.0/kill.c | b32e0fad65e298235102f98aff37e02c94400b544d454cb57192ae697b100bf3 |
| main.c | …/earlyoom/v1.9.0/main.c | 08656b0bc90c85f23738661456b25c97af908bc5e2cfea78e0a69697b5f9d0e4 |
| exec-invoke.c | https://raw.githubusercontent.com/systemd/systemd/v262/src/core/exec-invoke.c | 3be6c5a98ff29d3c7e929759f0d6c2f2ff8cc66bb146fdf836fbd2fe8fbebfed |

## Smallest safe correction

Make O1-O4 first. They are the overclaims a reader acts on: the tool's scope, a quiet verdict read as "never
acted", the inactive-earlyoom row, and the dry-run send line. O5-O15 are wording and provenance
fixes within the same entry. No change to the C1 phrase list, the C2 case file or the tool is needed for any finding.

## Tooling

No tool was installed or upgraded. I used only curl, git (read-only) and coreutils already on the host.
No journal, unit or settings data was read beyond the committed lane files.
