# CriticSkillWrongTurn — round 27 wave 2: wrong turns in the `## Round27` decision table

Seat: MoriR27.CriticSkillWrongTurn (UFO-FSD critic, leaf). Attacks: the `## Round27 — OOM victim selection`
decision table in `SKILL.md` at the landed tip `5f00fd045c137b7e3835506d69946cfd9d010eb5`, rows at
`git show 5f00fd0:SKILL.md` lines 727-733. `SKILL.md` at `HEAD` `0becc42` is byte-identical to `5f00fd0`
(`diff <(git show 5f00fd0:SKILL.md) SKILL.md` printed nothing at 17:08Z). During this review the L1's uncommitted
working tree changed the `python` row, added an "unknown killer" row and fixed the kernel tie wording
(`git diff 5f00fd0 -- SKILL.md`, read 17:13Z). Each finding below says whether that working tree already covers it.

Tool installs: none. No pacman, no jj, no git writes. No subagents.

## Sources opened (curl on public raw URLs, 2026-10-22T17:09:03Z, bytes under the seat scratch dir)

| File (tag) | sha256 | Matches the entry's recorded hash |
|---|---|---|
| earlyoom `kill.c` (v1.9.0) | `b32e0fad65e298235102f98aff37e02c94400b544d454cb57192ae697b100bf3` | yes (S118) |
| earlyoom `main.c` (v1.9.0) | `08656b0bc90c85f23738661456b25c97af908bc5e2cfea78e0a69697b5f9d0e4` | not recorded in the entry |
| earlyoom `meminfo.c` (v1.9.0) | `526e512c89c58cb0b1db2ae98ea62d287cdc1516846be80c9173bdc4bf0edfeb` | not cited by the entry |
| earlyoom `MANPAGE.md` (v1.9.0) | `cc48b02e79255ae27bad9b2c49364fcae1b6b5eb20fe8e83ecef432f360dfeda` | not recorded |
| Linux `mm/oom_kill.c` (v7.2) | `452f1348e79c252ee89215d55fb104591412bbcea4a3ee965e873a401f756b4e` | yes (S003) |
| Linux `fs/proc/base.c` (v7.2) | `cef1a2cf3f34f683e69d623c4df563d5c0dc6bd71dcb3d42f40dadb0084915c6` | not recorded |
| Linux `mm/memcontrol.c` (v7.2) | `8a28e0bc010e0575fbf9d1739643686e271bcf5a76c0284081df537a4041fd5e` | not cited by the entry |
| Linux `Documentation/admin-guide/cgroup-v2.rst` (v7.2) | `a9433bb0e16a67f07a93424c7bf842f47616e9b0a27b51e17d7b34cff246b7ad` | not recorded |

All line numbers below were pinned with `grep -n` on these bytes. Verbatim quotes, each under 25 words:

- `kill.c:414` `cur->oom_score += OOM_SCORE_PREFER;` · `kill.c:411-412` `if (args->sort_by_rss) {` / `cur->VmRSSkiB += VMRSS_PREFER;`
  · `kill.c:30` `#define VMRSS_PREFER 3145728` · `kill.c:475` `if (cur->oom_score_adj == -1000) {` (after the comparison at `:430-465`)
- `kill.c:276-282` `if (args->kill_process_group) {` … `pid = -res;` … `killing whole process group %d (-g flag is active)`
  (no `oom_score_adj` check on that path)
- `kill.c:627` `sending %s to process %d uid %d "%s": oom_score %d, oom_score_adj %d, VmRSS %lld MiB, cmdline "%s"`
- `base.c:586` `unsigned long totalpages = totalram_pages() + total_swap_pages;` · `base.c:597`
  `points = (1000 + badness * 1000 / (long)totalpages) * 2 / 3;`
- `oom_kill.c:258` `oc->totalpages = mem_cgroup_get_max(oc->memcg) ?: 1;` · `oom_kill.c:340`
  `if (points == LONG_MIN || points < oc->chosen_points)` · `oom_kill.c:366-367` `if (is_memcg_oom(oc))` /
  `mem_cgroup_scan_tasks(oc->memcg, oom_evaluate_task, oc);` · `oom_kill.c:943` `do_send_sig_info(SIGKILL, SEND_SIG_PRIV, victim, PIDTYPE_TGID);`
- `memcontrol.c:1975-1979` `from the victim task's cgroup up to the OOMing cgroup (or root) to find the highest-level memory cgroup with oom.group set.`
- `cgroup-v2.rst:1464-1466` `If the OOM killer is invoked in a cgroup, it's not going to kill any tasks outside of this cgroup, regardless memory.oom.group values of ancestor cgroups.`
- `meminfo.c:116-119` `if (m.SwapTotalKiB > 0) {` … `m.SwapFreePercent = 0;`
- `MANPAGE.md:156-157` `#### -g` / `Kill all processes that have same process group id (PGID) as the process`

Host facts from the lane's own wave-1 record: the running earlyoom arms one `--prefer` and one `--avoid`
expression, `--sort-by-rss` is off, `-g` is off (`.ufo/waves/round-27/w1/HostUnitOomAdjust.md:49,51,55-56,64-65`).
The entry's ranking script reads the raw kernel file and applies no prefer/avoid adjustment
(`.ufo/waves/round-27/evidence/oom-score-classes.py:35`, `score = int(read("/proc/%s/oom_score" % d))`).

## Live host re-read (read-only, classes and counts only; inline `python3 -I -B` over `/proc`, 17:11:47Z-17:13Z)

- `omp`-comm processes: 3 at 17:11:47Z, 6 at 17:12:10Z, 3 again at the third read. At the third read two were
  top-level sessions, each with ancestry `bash <- alacritty <- hyprland <- other <- systemd`, each its own
  process-group leader. The third was a helper: a session leader whose parent is an `omp` process, with no children.
- Kernel-score rank (all `/proc` entries, 17:12:10Z): the highest `omp` process ranked **16th** (score 851,
  adjustment 200). The top 15 were chromium-class processes at adjustment 300 (scores 867-870). Their first ancestor
  not at 300 is also chromium-class, so the 300 was set inside that app's own tree [INFERENCE: who wrote it was not
  traced]. At 15:56Z the committed sample had 1 process at 300 (entry Fact 4 table).
- `oom_score_adj` by cgroup kind: 200 → 112 processes, all under `user@UID.service`; 300 → 16, all under
  `user@UID.service`; 0 → 3 under a `session-N.scope`, 18 under `system.slice`, 1 under `init.scope`.
- Python-class processes: 25 in total, 0 in an `omp` process group. Of the Python children of `omp` processes,
  6 were 1 hour old or more, 1 was under an hour, 6 under 10 minutes and 2 under a minute.
- `MemTotal` 31721800 kB, `SwapTotal` 31722876 kB (one swap file): the host has swap.
- This seat's own tool commands run as direct children of an `omp` process (ancestry read at 17:11:47Z).

## Findings (one per row; verdict, the situation that misleads, and the smallest fix as exact old → new text)

### F1 — row 727 ("earlyoom sent SIGTERM or SIGKILL …") — wrong, **high**
Counterexample (an `--avoid` match, a `--prefer` match, a second session): the "What to conclude" cell gives an
earlyoom ranking but grounds it in a kernel-only snapshot. On this host both regex options are armed
(HostUnitOomAdjust.md:64-65), so earlyoom's order is not the kernel's order. If `omp` matched `--avoid`, its
earlyoom score would be 851 − 300 = 551 (`kill.c:421`). Any `--prefer`-matched process with a kernel score of 552
or more would outrank it (`kill.c:414`). Either way, "ranked second" says nothing about earlyoom's choice. The
snapshot is also stale within the same day: at 17:12Z an `omp` process ranked 16th by kernel score alone, and more
than one `omp` process was live. A reader would conclude "omp is next in line after one process".
Fix: old `on 2026-10-22 the single `omp` process ranked second on the host` → new
`the 2026-10-22T15:56Z sample ranked the then single `omp` process second by the kernel's score alone — that order applies no `--prefer`/`--avoid` adjustment (this host arms one of each) and moves with memory use (at 17:12Z an `omp` process ranked 16th)`.
Working tree: not covered.

### F2 — row 727, the `--sort-by-rss` case — wrong as stated, **medium**
Counterexample (`--sort-by-rss` set): the "conclude" cell states the `oom_score` key without a condition. Under
`--sort-by-rss` the key is the resident set (`kill.c:430-440`), and prefer/avoid move it by ±3145728 KiB, not
±300 (`kill.c:411-412,418-419`). The "not conclude" cell mentions the flag, but the conclusion a reader acts on does
not. On this host the row holds, because the flag is off (HostUnitOomAdjust.md:51). That is also consistent with the
8 above-ceiling send lines, which only a score-side +300 can produce.
Fix: old `earlyoom takes the highest `oom_score` it computes:` → new `with `--sort-by-rss` off (as on this host), earlyoom takes the highest `oom_score` it computes:`.
Working tree: not covered.

### F3 — row 727, a process at `oom_score_adj` -1000 — holds
earlyoom rejects -1000 only after the comparison (`kill.c:467-478`). A rejected candidate never replaces the current
victim, so the result is still the highest score among the rest. The kernel exports 0 for such a process
(`base.c:596-597`), so even a `--prefer` match gives it only 300. No fix needed.

### F4 — row 728 ("a send line's `oom_score` exceeds …") — holds one way, misleads the other way, **medium**
The positive direction holds: above the ceiling, only the score-side +300 explains it (`kill.c:414`, `base.c:597`).
Counterexample: a line at or under the ceiling is read as "no prefer match". An idle process at adjustment 200
exports 800 (entry Fact 2), and with a match it prints 1100, under 1466. The entry's Limits section says the count
is a lower bound, but the row does not. Under `--sort-by-rss` a match never shows in the score. Instead it adds
3072 MiB to the printed `VmRSS` (`kill.c:30,412,627`), so the RSS a reader quotes from a send line is inflated.
Fix: old `what the prefer expression says; it is never read or copied` → new
`what the prefer expression says (it is never read or copied), or that a line at or under the ceiling had no prefer match — an idle process at 200 with a match reads 1100; under `--sort-by-rss` a match moves the printed VmRSS by 3072 MiB instead of the score`.
Working tree: not covered.

### F5 — row 729 ("a fleet process shows `oom_score_adj` 200") — partly wrong, **medium**
Counterexamples: (a) A kernel OOM limited to one cgroup sets `totalpages` to that cgroup's limit
(`oom_kill.c:258`), so 200 is worth 20% of the limit, not of RAM plus swap. (b) Under `--sort-by-rss`, the
adjustment only breaks ties (`kill.c:437,449-453`). (c) The inference runs one way only. On this host 16 processes
under the same user manager carry 300, set inside their own app tree. A seat started from such a tree would not show
200 and would outrank `omp`. "The harness did not set it" holds for omp and Bun (entry Fact 3, S132).
Swapless host: holds. `totalpages` is then RAM alone (`base.c:586`), and "RAM plus swap" still reads correctly with
swap 0.
Fix: old `it weighs as if the process held 20% more of RAM plus swap` → new
`in a host-wide kernel OOM and in earlyoom's default ranking it weighs as if the process held 20% more of RAM plus swap (20% of the cgroup's limit in a cgroup-limited OOM; only a tie-break under `--sort-by-rss`)`.
Working tree: not covered.

### F6 — row 730 ("an in-session seat died … `omp`-class process") — wrong, **high**
Counterexamples (a seat run outside the omp process, and a kernel kill):
(a) "ends every in-session seat of every lane at once" assumes one `omp` process. At 17:11Z two terminal-launched
top-level `omp` sessions and one `omp` helper were live. A send to an `omp`-class process can hit a helper, which
ends no session, or one of two sessions, which ends only that session's seats. Entry Limits already calls the
single-process model an inference (`oom-victim-selection-r27.md:171` at the tip). The row states it as a conclusion.
(b) The row keys on an earlyoom send only. A kernel kill of `omp` leaves no earlyoom send. Its victim is the
highest kernel score inside the OOM's cgroup (`oom_kill.c:366-367`), with no prefer/avoid, sent SIGKILL
(`oom_kill.c:943`). That kernel-only order is where F1's "second" ranking would actually apply.
Fix: old `an in-session seat died and the journal shows an earlyoom send to an `omp`-class process in that window`
→ new `an in-session seat died and an earlyoom send or a kernel killed-process record names an `omp`-class process in that window`;
old `the session process may have been the victim, which ends every in-session seat of every lane at once` → new
`an `omp` process may have been the victim; if it was a session process, every seat inside that session ended at once — more than one `omp` process can be live (at 17:11Z two terminal-launched sessions and one helper), so it need not be every lane`.
Working tree: (b) is partly covered by the new "unknown killer" row; (a) is not covered.

### F7 — row 731 (`python`-class send) at the landed tip — wrong, **medium**
Landed text: `at most one tool process ended; the seat's session survived unless it was also signalled`.
Counterexamples: (a) Under `-g`, earlyoom signals the victim's whole process group (`kill.c:276-282`). This holds
on this host: `-g` is off, and 0 of 25 Python processes share an `omp` process group. (b) A kernel kill of the
session in the same window leaves no earlyoom send, so "unless it was also signalled" invites a reader to check
only earlyoom. (c) 6 Python children of `omp` were 1 hour old or more. A long-lived child is not a one-seat tool
process [INFERENCE: role not read, no command line opened].
Working tree: the rewritten row (`it establishes signalling of that selected process, not the session's survival or
death; check separately for kernel OOM events …`) fixes (b) and (c). Remaining smallest fix for (a): append
`; under `-g` (off here) earlyoom signals the victim's whole process group` to its "conclude" cell.

### F8 — row 732 (`memory.oom.group` is 1) — wrong in two ways, **medium**
Counterexamples: (a) The kernel uses the **highest** cgroup with `oom.group` set, between the victim's cgroup and
the OOM's own cgroup (`memcontrol.c:1975-1979`). A 1 on an ancestor widens the kill beyond "the subtree" of the
cgroup where it was read. An OOM confined to a cgroup below it ignores it entirely (`cgroup-v2.rst:1464-1466`).
(b) "earlyoom … signals one process" is false under `-g`. That path also has no -1000 exemption (`kill.c:276-282`,
the -1000 check at `:475` is in the selection code only). So a -1000 group member is signalled by earlyoom but
spared by the kernel's group kill (`cgroup-v2.rst:1461-1462`). Host: every measured `memory.oom.group` is 0 and
`-g` is off, so neither case is live today.
Fix: old `a kernel OOM kill there takes the whole subtree (tasks at -1000 spared)` → new
`a kernel OOM kill whose victim lies below it takes every task of the highest cgroup with `memory.oom.group` 1 between the victim and the OOM's own cgroup (tasks at -1000 spared); an OOM confined to a cgroup below it ignores it`;
old `that earlyoom does the same; it signals one process` → new
`that earlyoom does the same; it signals one process, or under `-g` (off here) the victim's whole process group with no -1000 exemption`.
Working tree: not covered.

### F9 — row 733 ("a lane is marked dead minutes into a new boot") — holds, **low** wording
Counterexample: a lane started at boot can die within minutes in the *new* boot. "Detected after a reboot" is
literally true, and "not conclude: the time of death" protects the reader, but "after a reboot" invites placing the
death in the previous boot. Fix: old `the death was detected after a reboot` → new
`the death was detected after a reboot; it may lie in either boot`. Working tree: not covered.

### F10 — swapless host, all rows — holds
The row-728 ceiling `(2000 + adj) * 2 / 3` does not depend on `totalpages` (`base.c:597`). With no swap, earlyoom
sets `SwapFreePercent = 0` (`meminfo.c:116-119`), so its swap condition is always met and it acts on memory alone.
The table needs no swapless caveat. This host has swap equal to RAM (`/proc/meminfo`, 17:11Z).

### Side finding (entry, outside the table) — already fixed in the working tree
Tip entry Fact 2: `a tie keeps the first task scanned (`:340`)` (`git show 5f00fd0:corpus/knowledge/oom-victim-selection-r27.md`, line 64).
`oom_kill.c:340` skips only a strictly lower score, so on a tie the later task wins. The working tree now reads
`a tie goes to the last task scanned`. Severity was low, because no table row uses the tie rule.

## Impact

- Axes: depth (substance of C1's table), calibration (a snapshot stated as a standing conclusion: F1, F6), and
  freshness (the ranking aged within 76 minutes).
- C1's counter is unaffected: every row still cites the entry. But F1 and F6 are false statements a reader would
  act on in the counted section. The L1 should land the F1 and F6 text before admission. F2, F4, F5, F7(a) and F8
  are fixable defects, not tradeoffs.
- Checks the L1 should run after editing: `bash .ufo/waves/round-27/count-c1.sh <rev>` (rows must still cite the
  entry), and the lane retention scan from the contract (must stay at or below 4). This report adds no settings
  path, pid, uid, command line, `MESSAGE` text or expression value.
