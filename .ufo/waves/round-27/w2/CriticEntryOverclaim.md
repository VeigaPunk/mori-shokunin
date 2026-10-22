# CriticEntryOverclaim — round 27, wave 2 (falsify)

Seat `MoriR27.CriticEntryOverclaim`. Attacks: `corpus/knowledge/oom-victim-selection-r27.md` at lane tip
`5f00fd045c137b7e3835506d69946cfd9d010eb5` (the working-tree file matches the tip: `git diff --stat 5f00fd04 -- <entry>`
printed nothing). What I hunted: universal words, unmarked inference, numbers without a date or command, conclusions
wider than their source, and advice to change a setting. Line numbers below are entry lines unless a file is named.

Method: upstream bytes re-fetched with curl into `/fast/scratch/hyaku/mori-r27/CriticEntryOverclaim/` at
2026-10-22T17:11:22Z. The sha256 of each file matches the entry or the lesson: `kill.c` `b32e0fad…0bf3`, `main.c`
`08656b0b…d0e4`, `MANPAGE.md` `cc48b02e…dfeda`, `mm/oom_kill.c` `452f1348…6b4e`, `proc.rst` `e760f716…d126`, systemd
`main.c` `5ecdca43…aae3`. Two more were fetched: `fs/proc/base.c` (`cef1a2cf…15c6`) and the man7 page
`proc_pid_oom_score_adj.5.html` (`769edf3b…80a9`, tags stripped to text before line numbers were taken). The host checks
were read-only and printed counts only. Tools installed: none.

## Verdict summary

| # | Entry line(s) | What is attacked | Verdict | Severity |
|---|---|---|---|---|
| 1 | 119-121, 158 | "ranks second" in earlyoom's order; "the single `omp` process" | wrong | high |
| 2 | 120-121, 162, 180 | "every in-session seat of every lane ends at once"; "a fleet-wide event" | unsupported | high |
| 3 | 64 | kernel tie "keeps the first task scanned" | wrong | medium |
| 4 | 151-152, 162 | "Only the system journal…"; "it names a process class" | wrong | medium |
| 5 | 68-73 | "disagree in three places" | wrong (one place) | medium |
| 6 | 60-62, 160 | adj 200 "worth 20% of RAM plus swap" | wrong as a universal | medium |
| 7 | 77, 161 | earlyoom "signals one process" | wrong as a universal | medium |
| 8 | 160 | adj 200 means "it descends from a user unit" | wider than its source | medium |
| 9 | 104-105, 167 | earlier run "1213 … with the same ranking" | unsupported | medium |
| 10 | 145 | "left no fleet line within 3 h 16 min" | wrong direction | medium |
| 11 | 17 | "share of those 39 sends hit the fleet's own runtimes" | wider than its source | medium |
| 12 | 179, 180-181 | "tell a prefer-adjusted victim from a plain one"; "a `python` send kills one tool process" | wider than its source | medium |
| 13 | 127-128 | "Boots -5 to -2 and boot 0 hold no send lines" | holds; evidence left unexplained | low |
| 14 | 136, 159 | "Only earlyoom's +300 … can produce that" | conditional on the stated inference | low |
| 15 | 55 | "protects itself through its unit, not its scan" | wording | low |
| 16 | 2, 76, 143, 149 | header "read-only"; "every level measured"; "No fleet record"; "none falls within 60 s" | wording | low |
| 17 | 51, 67 | "the shipped `earlyoom.default`"; "no memory reads … 800" | wording | low |

No sentence advises changing a setting. "only -1000 would exclude it" (`:56`) describes the code. "Read scores from the
code, not the pages" (`:73`) is advice about reading, and item 5 narrows it. `:194` "No setting is recommended or
changed" holds.

## Findings

**1. High: earlyoom's ranking is stated from kernel scores, while the host arms both a prefer and an avoid expression.**
Counterexample: the host's earlyoom argument list holds `--prefer` and `--avoid`, and neither expression is read
(`.ufo/waves/round-27/w1/HostUnitOomAdjust.md:47-49,64` "two regex policies are armed (one prefer, one avoid)").
Fact 1 itself says each match moves earlyoom's key by 300 (`kill.c:410-421`, re-read). Fact 4 ranks the kernel's
`/proc/<pid>/oom_score` only (`evidence/oom-score-classes.py:35`). An avoid match on `omp` drops it from 847 to 547. A
prefer match on any 800-point `python` raises it to 1100. So earlyoom's order is unknown. The entry never mentions the
armed `--avoid`. "Single" is also one sample, not a property of the host. At 2026-10-22T17:13:38Z a `/proc` walk
counted `omp_processes=3 parent_is_omp=0 parent_other=3` (three top-level `omp` processes; count-only script, this
seat). The wave-1 seat saw 1 to 3 at about 15:50Z (`w1/ConnFleetSeatKillPath.md:55-56`).
- `:119` old "The single `omp` process held the second-highest score on the host" → new "The one `omp` process in this
  sample held the second-highest kernel `oom_score` of the 792 processes read".
- `:158` old "on this host the single `omp` process ranks second (Fact 4)" → new "in the 15:56:35Z sample one `omp`
  process held the second-highest kernel `oom_score` (Fact 4); its place in earlyoom's order is unknown, because the
  host arms a `--prefer` and an `--avoid` expression whose text is not read (wave-1 HostUnitOomAdjust)".
- Add to Fact 5 (after `:137`): "The host also arms an `--avoid` expression (wave-1 HostUnitOomAdjust); an avoid match
  lowers a send-line score and cannot raise it above the ceiling."

**2. High: the fleet-wide-kill conclusion rests on a premise the evidence contradicts.** The entry says "no other
`omp` process was visible" (`:120-121`). The wave-1 source counted 3 with `ps` (`ConnFleetSeatKillPath.md:55-56`), and
this seat counted 3 top-level `omp` processes at 17:13:38Z. The same source says the killed `omp` cannot be told apart
from an interactive one (`ConnFleetSeatKillPath.md:120-122`). So "when earlyoom picks it" does not mean "when earlyoom
picks an `omp`-class process". A SIGTERM also ends the seats only if the process exits on it, and the entry does not
say whether it does. Impacted axes: depth, calibration.
- `:119-121` old "The fleet's in-session seats run as subagents inside that one process [INFERENCE: …, and no other
  `omp` process was visible], so when earlyoom picks it, every in-session seat of every lane ends at once." → new "The
  fleet's in-session seats run as subagents of one session `omp` process [INFERENCE: they are `task` jobs of one
  session]. The host runs more than one `omp` process (1 to 3 at about 15:50Z, wave-1 ConnFleetSeatKillPath; 3
  top-level at 17:13Z, wave-2 CriticEntryOverclaim), and which one holds the fleet session was not read. If earlyoom
  signals that process and the process exits, every in-session seat ends with it."
- `:162` old "the session process may have been the victim, which ends every in-session seat" → new "an `omp`-class
  process was the victim; it may or may not have been the fleet's session process. If it was, every in-session seat
  ended [INFERENCE]".
- `:180-181` old "say why one earlyoom send to `omp` is a fleet-wide event while a `python` send kills one tool
  process" → new "say why an earlyoom send to the fleet's session `omp` process would end every in-session seat
  [INFERENCE], while a send to a `python`-class process ends one process that may not belong to the fleet".
- `:171` add "; the host runs more than one `omp` process, so an `omp`-class victim is not shown to be the fleet's".

**3. Medium: the kernel tie rule is reversed.** `mm/oom_kill.c:340` reads `if (points == LONG_MIN || points <
oc->chosen_points) goto next;`. An equal score falls through to `select:` (`:343-348`) and replaces the earlier
choice, so the last task scanned wins.
- `:64` old "a tie keeps the first task scanned (`:340`)" → new "a tie goes to the task scanned later: `:340` skips a
  task only when its points are lower (`points < oc->chosen_points`)".

**4. Medium: two claims about attribution are too wide.** (a) Mori's own entry says `/proc/vmstat` and cgroup
`memory.events` `oom_kill` move only for kernel kills (`corpus/knowledge/oom-kill-counter-kernel-only-r12.md:6,21` at
`fc09f96c`), so the journal is not the only source that separates the two. (b) The send line carries the pid, uid,
process name and `cmdline` (`kill.c:627-629`). The class label is mori's privacy reduction, not what the journal
holds (`ConnFleetSeatKillPath.md:125-126` "the class label is all mori may keep").
- `:151-152` old "Only the system journal tells earlyoom kills from kernel kills, and it names a process class, never
  a seat or a lane. Joining a send to a lane is a time-window inference, never an attribution." → new "Per event, only
  the system journal tells earlyoom kills from kernel kills; the kernel-only `oom_kill` counters
  (`oom-kill-counter-kernel-only-r12.md`) tell them apart per scope and window. A send line names a pid, uid, process
  name and command line (S118 `kill.c:627`). Mori keeps only the class, so joining a send to a lane is a time-window
  inference here; whether a command line names a lane was not read."
- `:162` old "the journal names a class, not a seat" → new "mori keeps only the class; the command line was not read".

**5. Medium: the documentation and the code disagree in one place, not three.** First, `proc.rst` states the exported
range itself: "the exported value includes oom_score_adj so it is effectively in range [0,2000]" (`proc.rst:1811-1812`).
Second, both documents define badness in units of "a proportion along that range of allowed memory" (`proc.rst:1763`;
man page text `:79-80`). In those units, "added" (`proc.rst:1777`; man `:102`) is what the code does with `adj *=
totalpages / 1000` (`oom_kill.c:233-234`). Only the "3% extra memory" for root (man `:86-88`) has no v7.2
implementation (`oom_kill.c:199-237`).
- `:69-73` old "The documentation and the code disagree in three places. … Read scores from the code, not the pages."
  → new "The documentation and the code disagree in one place: the man page's "root processes are given 3% extra
  memory" (S128 adj page `:86-88`) has no implementation in v7.2 `oom_badness` (S003 `mm/oom_kill.c:226-235`). Both
  documents define the badness as 0–1000 in proportion-of-allowed-memory units, in which "added" matches the code's
  scaling, and `proc.rst` gives the exported 0–2000 range (S082 `proc.rst:1811-1812`)."

**6. Medium: "20% of RAM plus swap" holds only for a system-wide OOM and for the exported file.** In a memory-cgroup
OOM, `totalpages` is the cgroup's limit (`oom_kill.c:257-258`). Under a mempolicy or cpuset constraint, it is the
allowed nodes plus swap (`:283-301`). The man page says the same (man `:90-100`).
- `:62` old "An `oom_score_adj` of 200 is therefore worth 20% of RAM plus swap, not 200 points." → new "An
  `oom_score_adj` of 200 is therefore worth 20% of the memory the OOM may allocate from: RAM plus swap in a system-wide
  OOM and in `/proc/<pid>/oom_score`, the cgroup's limit in a memory-cgroup OOM (`:257-263`)."
- `:160` old "weighted as if it held 20% more of RAM plus swap" → new "weighted as if it held 20% more of RAM plus swap
  (of the cgroup limit in a memory-cgroup OOM)".

**7. Medium: earlyoom 1.9.0 can signal a whole process group.** `kill.c:276-282` replaces the pid with the negated
process group id under `-g` ("killing whole process group %d (-g flag is active)"); see `MANPAGE.md:156-157`. On this
host the `-g` flag is not in the argument list (`HostUnitOomAdjust.md:55`). A count-only journal pass at
2026-10-22T17:13:12Z found `process_group_lines=0` in each of boots -5 to 0.
- `:77` old "It does not affect earlyoom, which signals one process." → new "It does not affect earlyoom, which
  signals one process, or its process group under `-g` (S118 `kill.c:276-282`); `-g` is not in this host's argument
  list (wave-1 HostUnitOomAdjust)."
- `:161` old "that earlyoom does the same; it signals one process" → new "that earlyoom does the same; it signals one
  process (its process group only under `-g`, absent here)".

**8. Medium: an adjustment of 200 does not prove descent from a user unit.** Any process may raise its own value
(`base.c` floor rule, entry `:96-101`; the probe raised 200 to 500). The committed sample holds other-class processes
at 300 and 100 (`evidence/oom-score-classes.txt:7`). The sibling lane recorded Chromium helpers at +300
(`tsukuroi-shokunin/corpus/knowledge/oom-event-plane.md:115-116`).
- `:160` old "it descends from a user unit of an unprivileged user manager (100 + 100)" → new "most likely it inherits
  the user manager's default for its units (100 + 100, Fact 3); the value alone does not prove it, because any process
  may raise its own value".

**9. Medium: the earlier-run numbers have no committed source.** `rg '1213|15:46:40|same ranking'` over the lane
(excluding `w2/`) matches only the entry. `evidence/oom-score-classes.txt` has a single committed version, the 15:56:35Z
run (`git log -p` shows one commit, `126e192`). `:167` "one sample" also contradicts the claim of two runs.
- `:104-105` old "(an earlier run at 15:46:40Z read 1213, most of the difference kernel threads, with the same
  ranking)" → new: delete, or commit that run's output and cite it.

**10. Medium: the 3 h 16 min gap runs the other way.** The source says the last boot -1 watchdog line came at
02:59:43Z, "3 h 16 min before the `omp` SIGTERM" (`ConnFleetSeatKillPath.md:95-96`). The entry reads as a window after
the send.
- `:145` old "The boot -1 `omp` send left no fleet line within 3 h 16 min;" → new "The last boot -1 fleet line came 3 h
  16 min before the `omp` send, and no fleet line followed it in boot -1;".

**11. Medium: the scope promises fleet attribution that the facts withhold.** Fact 5 says a class name "does not prove
the process belonged to the fleet" (`:129-130`).
- `:17` old "what share of those 39 sends hit the fleet's own runtimes" → new "what share of those 39 sends went to
  processes whose names fall in a fleet runtime's class".

**12. Medium: "What it changes" claims more than the facts give.** The Limits say the prefer count is a lower bound
(`:172-173`): a prefer-matched victim under the ceiling reads as plain.
- `:179` old "tell a prefer-adjusted victim from a plain one" → new "flag a send line whose score only a prefer match
  explains (a lower bound)". The `:180-181` sentence is covered by item 2.

**13. Low: the evidence file shows one unparsed send line per boot, and the entry does not explain it.**
`evidence/boot-send-classes.txt:5,6,11` print `unparsed_send_lines=1` for boots -2, -1 and 0. They are earlyoom's startup
banner, `main.c:414` "sending SIGTERM when mem avail <= …". The count-only pass at 17:13:12Z printed `banner=1` and no
other unparsed line in each of those three boots. The statement holds.
- `:128` append "(the one unparsed `sending SIG` line in boots -2, -1 and 0 is earlyoom's startup threshold banner,
  S119 `main.c:414`)".

**14. Low: "Only" ignores the inference it rests on.** `:135-136` marks the ceiling as [INFERENCE], and then `:136`
states "Only … can produce that" without the condition.
- `:136` old "Only earlyoom's +300 `--prefer` adjustment can produce that" → new "Under that assumption, only
  earlyoom's +300 `--prefer` adjustment can produce that". Make the same change in row 2 of the decision table (`:159`).

**15. Low: the scan does stop earlyoom from signalling itself.** `kill.c:587-592` zeroes the victim when earlyoom picks
itself, and `:608-614` then sleeps one second.
- `:55` old "earlyoom protects itself through its unit, not its scan:" → new "earlyoom lowers its own kernel score
  through its unit; its scan does not exclude it, but it never signals itself (above):".

**16. Low: four wordings are wider than their sources.**
- Header `:2` "host read-only on 2026-10-22" also lists an `oom_score_adj` probe, which is a write. New: "host read-only
  on 2026-10-22, except an `oom_score_adj` probe on processes the probe started".
- `:76` "0 at every level measured": the root cgroup has no such file (`HostUnitOomAdjust.md:127`). New: "0 at every
  level measured where the file exists (the root has none; wave-1 HostUnitOomAdjust, 2026-10-22)".
- `:143` "No fleet record names a kill cause." New: "None of the fleet records searched (watchdog log, hyaku events log,
  wave-slot ledger, dead-seat files) names a kill cause."
- `:149` "none falls within 60 s": the entries are timed by their file's write time, and the source warns that a true
  60 s match could be hidden (`ScoutDeadSeatCorrelation.md:52,151-152`). New: "none was written within 60 s".

**17. Low: two smaller wording points.**
- `:51` "the shipped `earlyoom.default`" means upstream's file. Arch's packaged default was not opened
  (`HostUnitOomAdjust.md:162` [INFERENCE]). New: "upstream's `earlyoom.default` at v1.9.0".
- `:67` "A process with no memory reads … 800 at adjustment 200". `adj *= totalpages / 1000` truncates, so a process
  with no memory reads 799 unless `totalpages` is a multiple of 1000 (`oom_kill.c:233`; `base.c:597`) [INFERENCE:
  arithmetic]. New: "about 800".

## Universal words that hold (checked)

- `:12` "held no victim-selection rule": `git grep -c -i -E 'oom_score|OOMScoreAdjust' fc09f96c -- corpus/knowledge
  SKILL.md PROVINCE.md` printed nothing. The lessons hold only `round-26.md:67`.
- `:32` "never the command line": matching is by `get_comm` only (`kill.c:404-427`).
- `:130-131` "Every victim ran under the operator's account and at `oom_score_adj` 200":
  `evidence/boot-send-classes.txt:7,9` (`uid_class={'operator': 39}`, `victim_oom_score_adj={'200': 39}`).
- `:87-88` "no `oom_score_adj` or `OOMScoreAdjust` anywhere in their source trees": whole-tree grep at 0 hits
  (`w1/SrcOmpBunOomAdj.md:52-54`).
- `:38-40` the +450 [INFERENCE] arithmetic holds: the exported score carries adj × 2/3 (`base.c:597`).
- `:186-188` the sibling's "+200 band first" model exists (`oom-event-plane.md:116,349`), and the band date
  2026-10-14 (`:15`) holds (`oom-event-plane.md:8`).
- `:96-101` the floor rule matches `proc.rst:1799-1801`.

## Smallest safe correction

Apply items 1-4 before admission. Items 1 and 2 change what a reader would act on: the `omp` ranking and the
fleet-wide kill. Items 3 and 4 are false as written. Items 5-12 are exact text swaps. Items 13-17 are wording. None of
them touches the counter: `count-c1.sh` reads only the `source:` line, the SOURCES rows and the SKILL rows
(`w1/CriticC1Counter.md`).
