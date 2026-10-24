# CriticPrivacyPlan — privacy attack on the round-27 wave-1 host captures

Seat `MoriR27.CriticPrivacyPlan` (critic, leaf). Read-only. Date 2026-10-22. Lane tip read: `5fa0a00`.
Targets: the HostOomScoreClasses, HostBootSendClasses and HostUnitOomAdjust prompts
(`.ufo/waves/round-27/wave1-spec.json` items of those names), the two drafted capture scripts found at
`/fast/scratch/hyaku/mori-r27/oom-score-classes.py` and `/fast/scratch/hyaku/mori-r27/boot-send-classes.py`,
the already-landed `w1/HostUnitOomAdjust.md`, the frozen policy `.ufo/waves/round-18/frozen/c1-policy.json` and
`corpus/evidence/retention-allowlist.json`. Retention classes are named here by id only (R1..R9).

## Verdict in one paragraph

The drafted capture scripts are sound: run read-only here, their outputs (11 + 10 lines) contain no uid, pid,
command line, journal identifier, non-fleet name or R-class hit (lint below, `flagged=0` both). The danger is
elsewhere: (1) the frozen retention scan cannot see any of the forbidden values these captures could carry, so
"metric stays 4" is not a privacy pass; (2) the landed `HostUnitOomAdjust.md` already carries the operator's
uid number on four lines while scanning to zero hits; (3) a capture script that embeds the policy regexes as a
self-check adds exactly 4 hits (4 → 8), the same mechanism that produced today's 4.

## Counterexamples (strongest first)

### X1. The retention scan is blind to every forbidden value of these captures

- Evidence: count-only probe (`/fast/scratch/hyaku/mori-r27/CriticPrivacyPlan/probe.py`, loads the class regexes
  from the policy file at run time): boot -1 `sends=39 ... lines_with_any_rclass_hit=0`; boots -2 and 0 `0`;
  live `/proc`: `procs=1285 ... procs_cmdline_with_rclass_hit=0`. So pasting all 39 raw send lines (pid, uid
  number, comm, full command line) into a committed file would leave the metric at 4.
- Policy agrees: `c1-policy.json:28` "Regex classes are a recall floor, not a privacy proof".
- Second proof, on landed text: `w1/HostUnitOomAdjust.md` scans to `rclass_hits= []` yet carries the
  operator's uid number (X2).
- Axes: calibration (false privacy pass), provenance of the no-harm claim (`contract.md:82-85`).
- Correction: keep the scan as the no-harm counter, and add a second, non-metric leak lint over every new
  capture output and report before commit (pattern list in "Leak lint" below). Require `flagged=0`.

### X2. Landed leak: operator uid number in `w1/HostUnitOomAdjust.md`

- Lines 121, 129, 130 and 139 write the cgroup unit names with the real uid digits (`user-N.slice`,
  `user@N.service`, N = the operator's uid). Command (prints line numbers only):
  `re.search(r"user[@-][0-9]+", line)` over the file → `uid_in_unit: [121, 129, 130, 139]`.
- The contract forbids it: `contract.md:37-38` "never a command line, a uid, a pid list".
- The prompt invited it: "give the unit names, not session ids". On this host every unit name on that
  path except the slices above it embeds the uid (masked: `N::/user.slice/user-N.slice/user@N.service/app.slice/
  app-graphical.slice/app-Hyprland-…-exec-<instance>.scope`, from `sed -E 's/[0-9]+/N/g' /proc/self/cgroup`).
- Correction (smallest): before commit, replace those four digit runs with the literal placeholder `UID`
  (`user-UID.slice`, `user@UID.service`); the final scope suffix is already elided at line 121-122.
  Message routed to the L1 below.

### X3. Policy-literal self-match adds exactly 4 hits

- Test: each class regex applied to its own text, raw and JSON-escaped:
  `R2 ['R2']`, `R5 ['R5']`, `R6 ['R6']`, `R8 ['R8']`; R1, R3, R4, R7, R9 do not self-match.
- Precedent: today's 4 unallowlisted hits are one committed copy of the policy file at
  `.ufo/waves/round-20/falsify/NoHarmRun/rg/.ufo/waves/round-18/frozen/c1-policy.json`, lines 8, 11, 12, 14
  (gate output at `5fa0a00`: `metric 4`, `unallowlisted_hits 4`, classes R2, R5, R6, R8).
- Attack: an executor that adds a "privacy self-check" to its committed script by pasting the class regexes
  (or vendors a copy of the policy next to it) moves the metric 4 → 8.
- Correction: scripts that self-check load the policy at run time by path (as `probe.py` here does); never
  paste a class regex or a forbidden surface's literal path or key name into a script, comment, docstring or
  report. Name classes by id.

### X4. The prompt's send-line grammar matches 0 of 39 real lines

- Prompt (HostBootSendClasses): `... "<name>": oom_score <n>, VmRSS <n> MiB, cmdline "..."`.
- Upstream, earlyoom v1.9.0 `kill.c:627`: `"sending %s to process %d uid %d \"%s\": oom_score %d, oom_score_adj %d, VmRSS %lld MiB, cmdline \"%s\"\n"`.
- Probe on boot -1: `match_1_9_0_grammar=39 match_prompt_grammar=0`.
- Privacy impact: an executor following the prompt literally sees 39 "unparsed" send lines and the natural
  debug step is to print one. The drafted `boot-send-classes.py:16` already uses the 1.9.0 grammar and stops the
  match at `MiB`, so the command line is never captured into a group (good).
- Correction: pin the grammar to `kill.c:627`; unparsed lines are counted (`unparsed_send_lines=N`), never shown.

### X5. Non-send earlyoom lines carry the forbidden settings values

- `main.c:379` `"Preferring to kill process names that match regex '%s'\n"`, `main.c:386` `"Will avoid killing
  process names that match regex '%s'\n"`, `main.c:393` `"Will ignore process names that match regex '%s'\n"`:
  every earlyoom start writes the configured expressions into the journal. `main.c:76,84` print the notify
  and pre-hook script paths. `kill.c:446` prints a pid and a process name (zombie warning); `kill.c:282`,
  `:329`, `:338` print pids.
- Round 26 counted 87 lines of class `other` in boot -1 (`.ufo/waves/round-26/capture/capture-boots.txt:15`),
  so these lines exist in the retained window. [INFERENCE] some of them are the startup regex lines.
- Attack: any "sample of other lines", `journalctl --grep` paste, or `-o cat` excerpt copies the host's
  `/etc/default/earlyoom` expressions verbatim.
- Correction: classify by fixed prefix as `capture-boots.sh` does; a line of class `other` contributes a count
  only; no seat runs `journalctl -u earlyoom` without `-o json` piped straight into the counting script.

### X6. Journal JSON always carries host identifiers

- Probe: with `--output-fields=MESSAGE,__MONOTONIC_TIMESTAMP,__REALTIME_TIMESTAMP` every record still has the keys
  `_BOOT_ID`, `__CURSOR`, `__SEQNUM`, `__SEQNUM_ID` (all three retained boots). `journalctl --list-boots`
  (text) prints a 32-hex boot ID per row.
- Drafted script prints none of them (good). Attack: a raw `-o json` dump kept "for audit" and committed.
- Correction: boot offsets only, as in `capture-boots.txt:3-8` (`boot index=-1 first_utc_s=… last_utc_s=…`);
  never commit raw journal JSON or `--list-boots` text.

### X7. Exception text echoes the input

- `int("bun /x/y --flag")` → `ValueError: invalid literal for int() with base 10: 'bun /x/y --flag'`;
  `open("/proc/999999999/oom_score")` → `FileNotFoundError [Errno 2] No such file or directory: '/proc/999999999/oom_score'`
  (invented inputs, run here). A traceback captured with `2>&1` into a committed output carries a pid or a
  fragment of a name or command line. Naive `/proc/<pid>/stat` splitting is the classic trigger: a comm with a
  space or `)` shifts fields into `int()`.
- Drafted `oom-score-classes.py:39` catches `(OSError, ValueError)`, which covers ESRCH (`ProcessLookupError`
  is an `OSError`) and vanished pids (good). Drafted `boot-send-classes.py:57` can raise `KeyError` naming only
  the field name (harmless).
- Correction: per-record `try`, count failures (`read_errors=N`), never print the exception; record stderr as
  a return code only (`2>/dev/null` plus `rc=`, the round-26 pattern `capture-boots.sh`).

### X8. `ExecStart` cannot answer the flag question and carries a pid

- `systemctl show earlyoom.service -p ExecStart` (masked): `argv[]=<masked>; … ; pid=N ; …`; unit
  `/usr/lib/systemd/system/earlyoom.service:8` `ExecStart=/usr/bin/earlyoom $VAR`, `:7` `EnvironmentFile=-/etc/default/earlyoom`.
  So the prompt's "flags present in ExecStart" design reads "absent" for every flag (false provenance), and
  the raw output carries earlyoom's pid in `pid=` (and `MainPID=`).
- The scout saw this and switched to masked live argv (`HostUnitOomAdjust.md:21-22, 40-56`), publishing
  presence only. Residual risk: raw `systemctl show` output pasted anywhere carries the pid.
- Digest attack: `/etc/default/earlyoom` is small (`HostUnitOomAdjust.md:157` gives the byte count) and its
  structure is now public (three option pairs, `-r`, one prefer, one avoid: lines 44, 64). A published host
  sha256 would let anyone confirm guessed expressions offline. The scout withheld it (lines 155-156): keep it
  that way. [low] the byte count also narrows guesses; drop it unless a claim needs it.

### X9. Lesser defects in the drafts (privacy-neutral, calibration)

- `boot-send-classes.py:41-43` skips a non-string `MESSAGE` (journald emits a byte array for non-UTF-8 text,
  e.g. a victim with a non-UTF-8 comm) without counting it as a send or as unparsed. Probe: 0 byte-array
  records in all retained boots, so no present miscount. Fix: decode as `capture-boots.sh:20-21`.
- `oom-score-classes.py:60-61` reports every `systemd` comm with a non-zero adjustment, not "the" user manager;
  `:38` marks zombies (no `VmSize:`) as kernel threads. Values only, no leak.
- `HostUnitOomAdjust.md:80` copies an operator drop-in's setting value from a non-earlyoom `/etc` file. Not on
  the contract's forbidden list; advisory only.

## Field inventory (every output field that could carry a forbidden value)

| Capture | Field / surface | Could carry | Draft status | Safe form |
|---|---|---|---|---|
| OomScoreClasses | `/proc/<pid>/comm` | non-fleet name | classified, never printed | fixed label enum |
| OomScoreClasses | `/proc/<pid>` directory name | pid | not printed | never printed, not even counted per pid |
| OomScoreClasses | `/proc/<pid>/cmdline` (if used to tell omp from bun) | command line, R1/R2/R3/R4/R7 paths | not read | do not read; comm suffices (live: comm `omp` 1, `bun` 0, `node` 0) |
| OomScoreClasses | exception text | pid in path, name fragment | caught | count only |
| OomScoreClasses | user-manager lookup via unit name or `MainPID` | uid in `user@N.service`, pid | not used | label `user_manager_adj=` |
| BootSendClasses | `MESSAGE` | pid, uid, comm, command line | in memory only | never printed |
| BootSendClasses | regex group for comm | non-fleet name | classified | label enum |
| BootSendClasses | uid group | uid number | mapped to `operator`/`root`/`other` | labels only |
| BootSendClasses | pid group | pid list | `len(set)` only | count only |
| BootSendClasses | `_BOOT_ID`, `__CURSOR`, `__SEQNUM*` | host identifiers | not printed | boot offset only |
| BootSendClasses | non-send lines (`main.c:379,386,393,76,84`; `kill.c:282,329,338,446`) | settings values, script paths, pid, name | not printed | count by class |
| BootSendClasses | `__REALTIME_TIMESTAMP` | nothing forbidden | hour keys `YYYY-MM-DDTHHZ` | fine (cannot form R1) |
| UnitOomAdjust | `systemctl show -p ExecStart` raw | `pid=`, start time | not pasted | binary path plus "uses environment file" |
| UnitOomAdjust | live earlyoom argv | prefer/avoid/ignore values | masked | flag presence booleans |
| UnitOomAdjust | `/proc/self/cgroup`, cgroup dir names | uid (twice), scope instance id, logind session id (`session-N.scope` on a tty login) | **uid leaked, lines 121, 129, 130, 139** | `user-UID.slice`, `user@UID.service`, `<scope>` |
| UnitOomAdjust | `systemctl show user@$(id -u).service` | uid once expanded (`Id=`, shell trace) | command kept unexpanded (lines 67, 69) | never `set -x`, never print `Id=` |
| UnitOomAdjust | `sha256sum /etc/default/earlyoom` | low-entropy digest of a settings file | withheld | `differs=yes/no` only |
| All | report prose, script comments, citations | R7 path or any `config.yml` path:line citation, R2/R5/R6/R8 literals | none found (w1 reports scan 0 R-class hits) | class ids only |

## Exact output shape that keeps the retention scan at 4

Commit set per capture: the script, its aggregate output file, the seat report. Never commit raw journal
JSON, `--list-boots` text, `/proc` snapshots, stderr transcripts, `systemctl show` raw output, or any copy of the
policy file. Hits found in capture output are redacted, never allowlisted: `c1-policy.json:26` admits allowlist
rows only for lines that carry "no value copied from a private source", and capture output is exactly such a
copy. No new allowlist row is needed if the shape below is kept (row shape for reference:
`{path, class, line_sha256, reason, rule ∈ a|b|c}`, keyed by the exact line hash, forbidden for must-redact paths).

Output grammar (ready to paste into the executor prompts):

```text
Every output line is: key=value [key=value ...], single spaces, nothing else.
key   := [a-z0-9_]+ from the fixed vocabulary below (no other keys)
value := -?[0-9]+(\.[0-9]+)? | label | label:count(,label:count)* | YYYY-MM-DDTHHZ:count(,...)*
label := omp | bun | node | python | earlyoom | systemd | kthread | other
       | operator | root | other_uid | SIGTERM | SIGKILL | yes | no | absent | unavailable
OomScoreClasses keys: run ts_utc processes_read read_errors class count oom_score_min oom_score_median
  oom_score_max adj top10 user_manager_adj earlyoom_adj
BootSendClasses keys: boot first_utc_s last_utc_s sends sigterm sigkill unparsed_send_lines undecodable
  victim_class uid_class distinct_victim_pids oom_score_min oom_score_median oom_score_max
  rss_mib_min rss_mib_median rss_mib_max victim_adj hours_utc rc
UnitOomAdjust keys: earlyoom_adj_unit earlyoom_execstart_binary earlyoom_uses_envfile flag_prefer flag_avoid
  flag_ignore flag_sort_by_rss flag_r flag_p user_manager_adj_unit oom_kill_allocating_task panic_on_oom
  overcommit_memory oom_group_depth_<n> envfile_differs_from_package
Cgroup levels are reported by depth and role label (root, user_slice, user_uid_slice, user_manager,
app_slice, app_graphical_slice, terminal_scope), never by unit name.
Commands are recorded unexpanded (`$(id -u)` stays literal); no `set -x`; boot selection by offset only.
```

Why this cannot raise the metric: R1 needs a `T..-..-..-...Z_<hex8>-` stamp (the only stamp allowed is
`YYYY-MM-DDTHHZ`); R2, R4, R5, R6, R7 need path or file-name tokens and R8, R9 need specific identifiers, none of
which is in the vocabulary or the label set; R3 needs `<digits>.<tool>.log`, and every value is numeric or a
label. Prose in reports follows the same rule: class ids, never a literal.

Leak lint (non-metric, run on each new output and report before commit; print line numbers only):

```text
uid_in_unit        user[@-][0-9]+
pid_kv             \b(pid|PID|MainPID)[= :][0-9]+
uid_kv             \buid[= :][0-9]+
process_n          \bprocess [0-9]+
cmdline            cmdline            (outputs only; reports may cite the literal from kill.c)
logind_session     session-[0-9]+\.scope
hex32_id           (?<![0-9a-f])[0-9a-f]{32}(?![0-9a-f])
journal_ids        __CURSOR|_BOOT_ID|__SEQNUM
regex_option_value --(prefer|avoid|ignore)[ =]['"(^]
plus the nine class regexes loaded at run time from c1-policy.json
```

Gate at the candidate commit: `python3 -I -B tools/mori-retention-gate.py scan --repo . --rev <candidate>
--policy .ufo/waves/round-18/frozen/c1-policy.json --allowlist corpus/evidence/retention-allowlist.json` must
read `metric 4` with the unallowlisted set still exactly the four round-20 policy-copy rows (path lines 8, 11,
12, 14), and the leak lint must read `flagged=0` on every new file. Expected false positives in reports, all
checked here and harmless: `PID 1` / `uid 0` constants (`CriticInheritProbe.md:122-123,157`,
`SrcKillCSelection.md:38,81,120,129,140`) and the upstream README example options (`SrcEarlyoomManpageOptions.md:70,154`).

## Commands run and outputs (values masked or count-only)

- `python3 -I -B tools/mori-retention-gate.py scan --repo . --rev 5fa0a00 …` → `metric 4, hits 113, allowlisted 104,
  non_author 5, unallowlisted 4` (R2, R5, R6, R8 in the round-20 policy copy). Same `metric 4` at `fc09f96`.
- `python3 -I probe.py` → per boot: `records_keys=['MESSAGE', '_BOOT_ID', '__CURSOR', '__MONOTONIC_TIMESTAMP',
  '__REALTIME_TIMESTAMP', '__SEQNUM', '__SEQNUM_ID']`; boot -1 `sends=39 match_1_9_0_grammar=39
  match_prompt_grammar=0 byte_array_messages=0 lines_with_any_rclass_hit=0`; live `procs=1285
  comm_classes={'other': 1258, 'python': 26, 'omp': 1} procs_cmdline_with_rclass_hit=0`.
- `python3 -I ../oom-score-classes.py | python3 -I lint.py` → `lines=11 flagged=0`;
  `python3 -I ../boot-send-classes.py | python3 -I lint.py` → `lines=10 flagged=0` (lint = alphabet + leak list +
  R-classes; outputs themselves not copied here).
- Self-match test of the nine class regexes (raw and JSON form) → R2, R5, R6, R8 self-match; others do not.
- `systemctl show earlyoom.service -p ExecStart … | sed -E 's/[0-9]+/N/g; s/(argv\[\]=)[^;]*/\1<masked>/'` → `pid=N`
  present; `systemctl cat earlyoom.service` → `:7 EnvironmentFile=-/etc/default/earlyoom`, `:8 ExecStart=/usr/bin/earlyoom $VAR`.
- `pacman -Qkk earlyoom` (read-only query) → three `backup file: … (… mismatch)` lines, `N total files, N altered files`.
- Leak-pattern scan of `w1/*.md` → only `HostUnitOomAdjust.md uid_in_unit [121, 129, 130, 139]` is a real leak.
- `w1/swarm-registry.json` (tracked in earlier rounds' wave dirs) → `rclass []`.

## Sources opened (curl, 2026-10-22, public raw URLs)

| URL | sha256 | SOURCES |
|---|---|---|
| https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/kill.c | `b32e0fad65e298235102f98aff37e02c94400b544d454cb57192ae697b100bf3` | anchor on S118: `:282,329,338,446,627` |
| https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/main.c | `08656b0bc90c85f23738661456b25c97af908bc5e2cfea78e0a69697b5f9d0e4` | anchor on S119: `:76,84,379,386,393` |
| https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/proc_pid.c | `e5b654466cd92fb49cc1dcd905922dab56a1d156f10f4108d8af262a70b212d5` | fetched, not used; no row proposed |

Quotes (verbatim, under 25 words): `kill.c:627` as in X4; `main.c:379` "Preferring to kill process names that match
regex '%s'\n"; `main.c:386` "Will avoid killing process names that match regex '%s'\n"; `main.c:393` "Will ignore
process names that match regex '%s'\n"; `kill.c:446` "%s: pid %d \"%s\": rss=0 but oom_score=%d. Zombie main
thread?"; `c1-policy.json:28` "Regex classes are a recall floor, not a privacy proof".

## Impacted axes and tradeoffs

- Calibration and the no-harm claim: X1, X3 (fixable defects; the gate needs the leak lint beside it).
- Privacy contract C1 (`contract.md:37-39`): X2 (fixable; four-token redaction), X5, X6, X7, X8 (shape rules).
- Depth / provenance of C1 facts: X4, X8 (prompt grammar and flag source were wrong; drafts and scout corrected).
- No tradeoff here needs the judge to reject: every finding has a redaction or shape fix that keeps the facts.

Tooling: nothing installed or upgraded. Writes: this report, and scratch files under
`/fast/scratch/hyaku/mori-r27/CriticPrivacyPlan/` (fetched sources, `probe.py`, `lint.py`, a scan JSON).
