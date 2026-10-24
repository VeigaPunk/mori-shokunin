# JudgeC1Rows — row-by-row judgment of the watchdog-identity-r31 decision table

judged-revision: efcb73240e8f3765388aa670dd98aee47c82989b

Judged per the L1 note: row 14 was corrected at efcb7324 (verdict `alive` → `candidate`), rows 1–13 untouched.
Verified by `git diff a29f3e3f… efcb7324 -- corpus/knowledge/watchdog-identity-r31.md`: only the row-14 line and the
first Limits bullet differ, so rows 1–13 judgments are identical at both revisions.

Evidence opened at the cited lines (committed bytes, not just Gate quotes): sources-r31 S161, S162, S163, S164, S165,
S167, S169, S170, S171, S172, S173, S174 — anchors verified at S162:851/910/963, S163:325, S164:1096/1257,
S165:99/125/136, S167:136/584-586/588-592/610-611, S169:17-32, S170:13-47, S171:43/57/228-232, S172:26-36,
S173:1084-1086, S174:46-116; Gate table in `corpus/lessons/round-31.md`; wave-1 reports
`.ufo/waves/round-31/w1/{LiveCommProbe,LiveArgvProbe,ScoutCensusWatchdog}.md`; the residual report row 14 names,
`.ufo/waves/round-31/r1/CriticC1Tip.md`; committed `tools/mori-census.sh` (`probe_watchdog`, :703-733); fleet
`/home/vgpnk/Projects/shokunin/scripts/shokunin-watchdog.sh:1,376-409` (read-only). No tools installed (tooling
directive satisfied with zero changes).

row 1: supported — `-f` full-command-line matching verbatim S161:105-108; census counts lines not processes at mori-census.sh:715 (`pid_n=$(printf '%s\n' "$pids" | grep -c .)`); LiveArgvProbe (a) counted an `exec -a` decoy named `less shokunin-watchdog.sh` (3 lines with the watchdog absent); `candidate` (mention ≠ identity) follows.

row 2: supported — self-exclusion S161:318-324 (quote anchored :323, "will never report itself as a match") and S162:851-852 (`if (PIDS_GETINT(PID) == myself)` / `continue`); filter bytes at mori-census.sh:713; LiveArgvProbe (b) measured a watchdog-argv candidate carrying `--pgrep-mode` dropped at stage 3 (count 1→0), whose own framing covers "a real watchdog started with a pgrep-mentioning flag"; `false negative risk, not absence` follows.

row 3: supported — name-only matching S161:105-108 ("normally only matched against the process name"); zero-match warning verbatim S162:962-963; measured live: LiveCommProbe RL:54-57 (`shokunin-watchdog` = 17 chars > 15, exit=1 plus the warning) while six cmdline-matching processes were alive; `unavailable (probe blind)` follows.

row 4: supported — comm from basename of the executed filename S164:1257 (`__set_task_comm(me, kbasename(bprm->filename), true)`); `#!` splice S165:99-101; measured comm `bash`, cmdline `bash ./…`, exe `/usr/bin/bash` for the env-shebang launch (LiveCommProbe RL:32-35) and name-only pgrep exit=1 while it ran (R2:6-9); the watchdog shebang is `#!/usr/bin/env bash` (scripts/shokunin-watchdog.sh:1); `not-identity (name useless)` follows.

row 5: supported — TASK_COMM_LEN = 16 at S163:325; silent truncation S169:30-32; measured bin-shebang comm exactly `shokunin-watchd`, 15 bytes (`-x shokunin-watchd` exit=0 vs `-x shokunin-watch` exit=1, LiveCommProbe RL:40-43, 80-82); `not-identity (prefix only)` follows.

row 6: supported — PR_SET_NAME sets the calling thread's name (S172:26-29) with the 16-byte cap including the NUL (S172:32-36); comm is thread-writable (S169:21-23); LiveArgvProbe (c) measured a python process whose comm became `shokunin-watchd` via prctl rc 0 and was returned by `pgrep -x` (match count 1); `not-identity` follows.

row 7: supported — zombie rule S170:13-17 (complete command line "unless the process is a zombie"; a read "will return 0 characters"); the caution "not by itself proof that the process exited" is carried by S170:26-31 (processes "have the freedom to override the memory region and break assumptions about the contents or format") and S170:47 ("the command line that the process wants you to see"), so empty ⟹ exited is not established by the source; `unavailable` follows.

row 8: supported — interpreter name spliced as argv[0] with the script filename after it, S165:99-101; post-execve argv edits show in cmdline, S170:33-37; argv malleability measured in LiveArgvProbe (a)/(b), so a matching path is consistent but not proof; `candidate` follows.

row 9: unsupported — the state-letter position is carried (S167:588-592: pid, "(", task name, ") ", then state) and the label too (S167:136 `"Z (zombie)"`, S171:57 `Zombie`), but the reading's load-bearing gloss — "the process has exited but is not yet reaped: the pid is still occupied, the watchdog loop is not running" — is carried by no cited line and no cited measurement: grep of the committed copies finds no reap/exit semantics for Z in S167 or S171 (single hit each, the label itself), and no wave-1 report observed a zombie; the verdict `absent (exited, unreaped)` rests entirely on that unsourced definitional gloss.

row 10: supported — starttime defined S171:228-232 ("time the process started after system boot … expressed in clock ticks"); tick conversion S167:584-586 (`nsec_to_clock_t(timens_add_boottime_ns(task->start_boottime))`, printed at :610-611); LiveArgvProbe (d) measured two incarnations of one command line with different field-22 values (5741473 vs 5741569); "different value under the same pid is a different process" follows from the definition; `not-identity (pid reused)` follows.

row 11: supported — wrap-to-minimum verbatim S173:1084-1086; boot-relative start_time S167:584-586 (`start_boottime` → clock ticks); pid recurrence plus the (pid, start_time) pairing within one boot follows; `not-identity` follows.

row 12: supported — exit-1 semantics S161:305 ("No processes matched or none of them could be signalled." — the signalling disjunct belongs to pkill/pidwait, and exit=1 on zero matches was measured live, LiveCommProbe RL:57/67); the census query is the `-af shokunin-watchdog` pipeline (mori-census.sh:711-715); `absent (that query only)` follows.

row 13: supported — exit 2 syntax / exit 3 fatal verbatim S161:308 and S161:311; the census missing-binary arm mori-census.sh:716-720 (surface `unavailable`, finding "daemon liveness UNKNOWN, not absent", then `return 0`) verified in committed bytes; `unavailable` follows.

row 14: supported — /proc/locks line format S174:46-48 (FLOCK = BSD lock created using flock(2)), :76-77 (WRITE = BSD exclusive lock) and :80 (field 5 = "The PID of the process that owns the lock"), :91-93 (device + inode subfields); the watchdog opens the file and flocks via the helper at scripts/shokunin-watchdog.sh:381-382 (`exec {LOCKFD}>"$UFO/.watchdog.lock"` then `flock -n "$LOCKFD"` — flock(1) is a separate process, no bash builtin), so the owner pid shown is the short-lived helper, and a descriptor-inheriting child keeps the lock past a watchdog death; both measured in the cited reproduction committed at .ufo/waves/round-31/r1/CriticC1Tip.md (`lock pid == watchdog bash pid: no`, `lock pid alive: no`; after SIGKILL of the bash: `lock lines after kill=1`, `flock -n exit=1` = still held); reading /proc/locks is passive and the census contains no flock at all (grep of committed tools/mori-census.sh: zero hits), so "without contending / never run" holds; `candidate (the watchdog or an orphaned child holds the lock)` follows and is the correct downgrade from the first committed version's `alive`.

## Residual risk and verification gaps

- Gate anchor drift, no row impact: S172's gate anchor `:34-35` sits at :35-36 of the committed copy and S173's `:1092-1093` at :1091-1092 (quote text verified present in both). S027 (cited in Limits only) is not present under `corpus/evidence/sources-r31/` at either revision — a prior-lane row, outside this table.
- The row 14 helper/orphan mechanism is measured (committed reproduction) but the kernel side (fs/locks.c) is intentionally unsourced this round; the entry's Limits bullet discloses this, so the row does not overstate — but a kernel change to flock owner-pid reporting would not be caught by the recheck line.
- Wave-1 reports are working-tree files, not committed at either revision; they are the assignment's designated measurement evidence and were judged as given (their scratch logs were not re-opened, and I ran no measurements or counters myself — non-author judge, committed bytes and committed reports only).
- The row 9 gap is fixable without new mining: extend the already-carried proc.rst scope (S082's state list defines zombie as terminated-but-unreaped) or mark the gloss [INFERENCE]. As committed at efcb7324, that row should not be counted as supported.

## Summary

13 of 14 rows supported; row 9 unsupported on one narrow, precisely scoped ground (zombie semantics carried by no cited line or measurement; the state-letter position and the Z label are carried). The efcb7324 correction of row 14 (`alive` → `candidate`, helper-PID reading, orphan-child caveat) is faithful to S174, to the fleet script bytes at :380-382, and to the committed CriticC1Tip reproduction; rows 1–13 are byte-identical to a29f3e3f and all supported, each on cited source lines plus the named wave-1 measurements.
