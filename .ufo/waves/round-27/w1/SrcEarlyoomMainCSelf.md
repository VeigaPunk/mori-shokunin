# SrcEarlyoomMainCSelf — earlyoom 1.9.0 main.c: self-protection and option parsing

Seat: C1 source scout. Scope: `main.c` at tag `v1.9.0` (existing row **S119**; `main.c`
also appears in S117 for tag/message-grammar history). Result: **anchor on S119, not a
new row** — so this seat yields **no** S127+ row and does not by itself move C1's
`new_rows_cited` toward 3.

## Answer

### How earlyoom keeps itself off the victim list

1. **The unit does the heavy lifting, not the binary.** The upstream template sets
   `Nice=-20` and `OOMScoreAdjust=-100` on the service
   (`earlyoom.service.in:12,14`, already anchored by **S120**), plus
   `AmbientCapabilities=CAP_KILL CAP_IPC_LOCK` (`:9-10`), which is what lets the
   daemon's own `mlockall` succeed under `DynamicUser=true`.
2. **Inside `main.c` the same protection is opt-in via `-p`.** `case 'p'` only sets a
   local flag (`main.c:277-278`); after the option loop the flag triggers
   `setpriority(PRIO_PROCESS, 0, -20)` (`main.c:397`) and
   `set_oom_score_adj(-100)` (`main.c:401`). `set_oom_score_adj()` writes the decimal
   itself: `getpid()`, then `%s/%d/oom_score_adj` under `procdir_path`
   (`main.c:436-459`, path built at `:441`). Both steps are warn-and-continue:
   `Could not set priority: %s. Continuing anyway` (`:398`),
   `Could not set oom_score_adj: %s. Continuing anyway` (`:403`); success prints
   `Priority was raised successfully` (`:407`). Nothing else in `main.c` touches its
   own `oom_score_adj`.
3. **`mlockall` is best-effort and runs late.** It comes *after* the startup selftests
   (`main.c:419` then `:421`): `MCL_CURRENT | MCL_FUTURE | MCL_ONFAULT` (`:421`), with
   a retry without `MCL_ONFAULT` for kernels older than 4.4 (`:422-425`), and on total
   failure only `perror("Could not lock memory - continuing anyway")` (`:427`).
   `MCL_ONFAULT` is defined locally to 4 when glibc lacks it (`main.c:25-30`). `main.c`
   and `kill.c` contain no `setrlimit`/`RLIMIT_*`, so the daemon does not raise its own
   `RLIMIT_MEMLOCK`; it relies on `CAP_IPC_LOCK` from the unit.
   The dry-run kill in `startup_selftests()` is ordered first precisely so the stack has
   grown before the lock (`main.c:64-71`, comment at `:66`).
4. **Self is *not* hard-excluded from candidacy by `main.c`.** There is no
   `pid == getpid()` filter in the selection path of `main.c`; the only `getpid()` there
   is the `oom_score_adj` writer (`main.c:439`). The self-guard lives in `kill.c`:
   `if (victim.pid == getpid())` warns about `hidepid` and zeroes the victim struct
   (`kill.c:586-593`), i.e. it only catches the degenerate case where earlyoom selected
   itself. Separately `is_larger()` rejects any process whose `oom_score_adj` is exactly
   `-1000`, "like the kernel oom killer would" (`kill.c:467-476`). **`-100` is not a
   skip** — it only lowers `oom_score`, so protection is a score offset plus a small
   RSS, not an exclusion.

Live host corroboration (presence/value of the *unit* properties, not of the operator's
default file): `systemctl show earlyoom.service -p OOMScoreAdjust -p Nice
-p AmbientCapabilities -p ActiveState` →
`ActiveState=active`, `OOMScoreAdjust=-100`, `Nice=-20`,
`AmbientCapabilities=cap_kill cap_ipc_lock`; the installed
`/usr/lib/systemd/system/earlyoom.service` carries the template's directives at the same
line numbers (`:7 ExecStart=/usr/bin/earlyoom $EARLYOOM_ARGS`, `:9`, `:12`, `:14`, `:20`),
and its `ExecStart` passes no `-p` — the runtime flag set comes from the environment file,
which is the presence-only question owned by `MoriR27.HostUnitOomAdjust`, not answered
here. Either way the host's earlyoom itself runs at `oom_score_adj -100`. [INFERENCE] the
Arch sed edits recorded in S126 do not touch `OOMScoreAdjust=`, and the live property
confirms the value survived packaging.

### How `--prefer` / `--avoid` / `--ignore` / `--sort-by-rss` reach the config

- Long-option ids are an enum starting at 513 (`main.c:38-46`); the table declares
  `required_argument` for the three regex options and `no_argument` for
  `--sort-by-rss`, `--dryrun`, `--ignore-root-user`, `--syslog` (`main.c:180-191`).
- The case handlers store **one** `optarg` per class into a local `char*`
  (`prefer_cmds` `:289`, `avoid_cmds` `:292`, `ignore_cmds` `:302`), so a repeated flag
  **overwrites** the earlier one — last occurrence wins; there is no list and no comma
  splitting. `--sort-by-rss` sets a single `bool` and prints one line
  (`main.c:284-286`).
- Compilation is deferred until after the `getopt_long` loop, once per class:
  pointer from the local `regex_t`, `regcomp(..., REG_EXTENDED | REG_NOSUB)`, and
  `fatal(6, "could not compile regexp '%s'\n", ...)` on a bad pattern
  (`main.c:374-395`; flags visible at `:376,383,390`). The struct is zero-initialised
  (`main.c:139-146`), so an unset option leaves a `NULL` pointer, which the header
  documents as "NULL = no-op" (`kill.h:26-38`, fields `:30-33`).
- Semantics are not in `main.c`: `is_larger()` matches the regexes against the **comm**
  name and adds `OOM_SCORE_PREFER` `+300` / `OOM_SCORE_AVOID` `-300` to `oom_score`
  (`kill.c:24-27,404-427`); with `--sort-by-rss` it instead adds
  `VMRSS_PREFER` `+3145728` / `VMRSS_AVOID` `-3145728` KiB to `VmRSSkiB`
  (`kill.c:29-32,411-420`) and the victim becomes the largest `VmRSS` rather than the
  largest `oom_score` (`kill.c:430-462`). `--ignore` is the only hard rule: a match
  returns `false` and the process is never a candidate (`kill.c:424-427`). `-M`/`-S`
  and the thresholds are out of scope here (S115/S119 already cover them).

## Gate

- URL: https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/main.c
- Access: 2026-10-22T15:46:35Z, HTTP 200, 21,053 bytes, 552 lines
- sha256: `08656b0bc90c85f23738661456b25c97af908bc5e2cfea78e0a69697b5f9d0e4`
  — identical to the hash already recorded in row S119, so these are the same bytes.
- Verbatim, each ≤25 words:

1. `main.c:397` — `if (setpriority(PRIO_PROCESS, 0, -20) != 0) {`
2. `main.c:401` — `int ret = set_oom_score_adj(-100);`
3. `main.c:421` — `int err = mlockall(MCL_CURRENT | MCL_FUTURE | MCL_ONFAULT);`
4. `main.c:441` — `snprintf(buf, sizeof(buf), "%s/%d/oom_score_adj", procdir_path, pid);`
5. `main.c:376` — `if (regcomp(args.prefer_regex, prefer_cmds, REG_EXTENDED | REG_NOSUB) != 0) {`

Supporting reads in the same fetch: `main.c:66`
`// (2) the stack grows to maximum size before calling mlockall()`;
`main.c:427` `perror("Could not lock memory - continuing anyway");`.

## Paste-ready SOURCES change (S119)

Append to the **anchor** column of the existing S119 row, immediately before its closing
` |` (the column currently ends with `... opened 2026-10-22`). Insert with a leading
`; `:

```
; re-opened 2026-10-22 for self-protection and option parsing: enum of long-option ids main.c:38-46; long-option table with required_argument for prefer/avoid/ignore and no_argument for sort-by-rss main.c:180-191; case handlers main.c:277-303 (a repeated --prefer/--avoid/--ignore overwrites the single optarg, so the last occurrence wins); -p applies setpriority(-20) main.c:397 and writes -100 to its own /proc/<pid>/oom_score_adj main.c:401,436-459, both warn-and-continue main.c:398,403; mlockall(MCL_CURRENT|MCL_FUTURE|MCL_ONFAULT) after the startup dry-run kill main.c:419-421, MCL_ONFAULT retry for pre-4.4 kernels main.c:422-425, non-fatal perror main.c:427, local MCL_ONFAULT fallback main.c:25-30, no setrlimit anywhere in main.c or kill.c; --prefer/--avoid/--ignore compiled once after getopt with regcomp(REG_EXTENDED|REG_NOSUB) and fatal(6) main.c:374-395, NULL pointer meaning no rule kill.h:26-38; sha256 still 08656b0bc90c85f23738661456b25c97af908bc5e2cfea78e0a69697b5f9d0e4
```

Also append to the same row's **used-by** column:
`, corpus/knowledge/oom-victim-selection-r27.md`.

That row's `scope` and `teaches` say "startup and poll-loop emission only", which the
anchor above would contradict. Minimal keeping-in-scope edit (proposed, L1's call):

- scope, replace `earlyoom v1.9.0 startup and poll-loop emission only: the version line,`
  with `earlyoom v1.9.0 startup, option parsing, self-protection and poll-loop emission: the version line, the long-option table and the regcomp of --prefer/--avoid/--ignore, the -p niceness and oom_score_adj path, mlockall and the startup dry-run kill,`
- teaches, after the existing sentence add: `The -p path and mlockall are best-effort and warn-and-continue, and earlyoom never hard-excludes itself from the candidate list, so its own safety comes from an oom_score_adj of -100 rather than from a skip rule.`

## Not mine to land — two facts that belong to other rows

`kill.c` selection semantics (the `±300` / `±3145728` constants, the `--ignore`
rejection, the `-1000` skip, the self-selection guard) are **outside S118's declared
scope**, which says "not the poll-loop decision logic". Either S118's scope is widened
and anchored, or these get a new row; only the latter would count toward C1's S127+
requirement. Anchors for that decision:

```
; victim-selection scoring kill.c:24-32 (OOM_SCORE_PREFER 300, OOM_SCORE_AVOID -300, VMRSS_PREFER 3145728, VMRSS_AVOID -3145728), applied by is_larger kill.c:404-427 against the comm name, --ignore returns false kill.c:424-426, oom_score_adj -1000 processes skipped kill.c:467-476, self-selected victim zeroed with a hidepid warning kill.c:586-593, sort-by-rss compares VmRSS else oom_score kill.c:430-462; kill.c sha256 b32e0fad65e298235102f98aff37e02c94400b544d454cb57192ae697b100bf3 (same bytes as S118)
```

`earlyoom.service.in:9-10,12,14` are already in S120's anchor; no edit needed there. The
host's live unit properties match them (see above).

## Unknowns / limits

- Whether the host's effective `EARLYOOM_ARGS` includes `-p` is presence-only host
  config and is `MoriR27.HostUnitOomAdjust`'s question; not inspected here. It does not
  change the outcome, because the unit already sets `OOMScoreAdjust=-100`.
- `oom_score` itself is computed by the kernel; how `oom_score_adj` scales into
  `oom_badness()` is `MoriR27.SrcKernelOomBadness`'s question, not `main.c`'s.
- `meminfo.c`/`procinfo` decide which processes are even read (e.g. `hidepid` effects);
  not traced here.

## Tooling

No installs, no upgrades, no pacman. Only `curl` (system) and the read/grep tools;
scratch at `/fast/scratch/hyaku/mori-r27/SrcEarlyoomMainCSelf/` (`main.c`, `kill.c`,
`kill.h`, `msg.h`, `globals.h`). No unit or service was started, stopped or signalled.
