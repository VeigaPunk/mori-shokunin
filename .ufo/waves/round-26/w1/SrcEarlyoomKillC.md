# SrcEarlyoomKillC — earlyoom v1.9.0 kill.c / msg.c source seat (round 26, wave 1)

Scope of this seat: the kill-path log literals of earlyoom v1.9.0 (`kill.c`) and the output route of
`warn()` (`msg.c`). `main.c` anchors quoted here are cross-checks only; they belong to the
`SrcEarlyoomMainC` row (cite, never absorb).

## Behavior (what the round can rest on)

1. The kill-action literal is a **format string**, not a fixed prefix — `kill.c:627`:
   `warn("sending %s to process %d uid %d \"%s\": oom_score %d, oom_score_adj %d, VmRSS %lld MiB, cmdline \"%s\"\n",`
   with `sig_name` chosen at `kill.c:617-624` (`"SIGTERM"`, `"SIGKILL"`, `"0 (no-op signal)"`).
   The rendered prefix is therefore `sending SIGTERM to process ` / `sending SIGKILL to process `,
   and the contract's prefix-anchored grammar matches the rendered text. The message body carries a
   **uid, process name and full command line** (`kill.c:627-629`), so any reader must count, never copy.
   The literal is emitted only when `sig != 0 || enable_debug` (`kill.c:626`); the `sig == 0`
   startup self-test (`main.c:72`) therefore produces no action line unless debug is on.
2. Escalation is a **second signal on the same pid**, not a new victim — `kill.c:317-322`: on
   `SIGKILL` limits reached while waiting, `sig` is set to `SIGKILL` and `kill_release()` is called
   directly. It prints `escalating to SIGKILL after %.3f seconds` (`kill.c:318`) and **no**
   `sending SIGKILL to process` line. So the `sigkill` count (from `kill.c:627`) and the `escalations`
   count (from `kill.c:318`) are different populations: an escalated kill yields one escalation line
   and zero SIGKILL action lines.
3. `kill failed: %s` (`kill.c:654`) is printed whenever `kill_wait()` returns non-zero, which covers
   two different causes: `kill(2)` failure (`kill.c:242-245`, `kill_release` returning non-zero) and
   the 10-second wait timeout (`kill.c:336-338`, `res = -1; errno = ETIME;`). A `kill failed` line
   therefore does not prove that no signal was delivered.
4. `process %d exited after %.3f seconds` (`kill.c:329`) is the success path of the wait loop;
   `process %d did not exit` (`kill.c:338`) is the timeout path. Both are per-attempt, not per-victim
   summaries, and neither is a kill action.
   **Counter semantics for the two counters the contract lists but does not rank** (raised by the
   mutation seat): both `kill failed:` (`kill.c:654`) and `low memory!` (`main.c:519`, `main.c:523`)
   are emitted *after* or *beside* an action, never instead of one, so neither can be the sole
   evidence of a kill.
   - `kill failed:` is printed at `kill.c:653-654`, inside `kill_process()`, which already printed
     the action line at `kill.c:627` before calling `kill_wait()` at `kill.c:640`. A journal can
     therefore contain `kill failed:` **only if** it also contains the matching
     `sending SIG… to process ` line for the same attempt. `kill failed` is a weaker duplicate of
     evidence the action line already carries, never independent evidence.
   - `low memory! at or below SIGKILL/SIGTERM limits` (`main.c:519`, `main.c:523`) is printed in
     `poll_loop()` **before** the victim is chosen and before the second memory check
     (`main.c:526-539`). That check can print `memory situation has recovered while selecting victim`
     (`main.c:537`) and skip `kill_process()` entirely, so a `low memory!` line can be present with
     **no** action line at all. It is a threshold-crossing notice, not a kill record.
   Consequence for the contract's verdict rule 1, which names action lines and escalation lines as
   positive evidence and leaves `kill failed:` / `low memory!` unranked: the source supports the
   contract's literal reading. A `low memory!` line alone is not evidence a killer acted, and a
   `kill failed:` line is always accompanied by the action line that is already positive evidence.
   Treating either as independent positive evidence would let a threshold crossing that recovered
   (`main.c:536-537`) be reported as a kill.
5. Dry-run has **two** distinct literals: the flag `dryrun mode enabled, will not kill anything`
   (`main.c:295`, printed via `warn()`), and the per-attempt `dryrun, not actually sending any signal`
   (`kill.c:272`, also via `warn()`). The contract grammar lists only the first.
   **Reachability (settles the case seat's open question):** `args.dryrun` is assigned in exactly one
   place in the whole program — `main.c:296`, immediately after the `main.c:295` warn — and
   `kill.c:272` can only fire from `kill_wait()`, reached from `kill_process()` (`kill.c:640`) inside
   `poll_loop()` (`main.c:539`). Startup print order in `main()` is: version banner (`main.c:161`) →
   option parsing, where the dryrun warn fires (`main.c:195-341`, warn at `main.c:295`) → totals and
   thresholds (`main.c:412-417`) → `poll_loop()` (`main.c:431`). So on any real host, a journal that
   contains `kill.c:272` also contains `main.c:295` **earlier in the same invocation**, and both are
   inside the C2 scope window (the startup lines post-date `ActiveEnterTimestampMonotonic`; on this
   host the banner is at `__MONOTONIC_TIMESTAMP=19981126` vs an active timestamp of `19964362`).
   Consequence: the contract's dryrun sourcing from `main.c:295` alone loses no real-host capability,
   and the synthetic combination in the case seat's `c21` (a `kill.c:272` line with no `main.c:295`
   line) is not a physically reachable host state. No contract amendment is needed for the grammar
   list to be complete for the capability claimed.
6. Process-group mode (`-g`) prints `killing whole process group %d (-g flag is active)`
   (`kill.c:282`) before the group is signalled (`kill.c:276-283`); `pid` is negated to the pgid at
   `kill.c:281`.
7. `Could not find a process to kill. Sleeping 1 second.` (`kill.c:609`) is emitted when no victim
   exists (`kill.c:608`, `victim->pid <= 0`): **no process was signalled** on that path.
8. `warn()` writes to **stderr** by default — `msg.c:99-107` calls
   `logger(LOG_WARNING, stderr, yellow, fmt, vl)` (`msg.c:104`); `logger()` (`msg.c:66-73`) uses
   `vsyslog(priority, fmt, vl)` only when `use_syslog` is set (`msg.c:14`, default 0) and otherwise
   writes the stream it was handed, here `stderr` (`msg.c:71`).
   `use_syslog` is turned on only by `earlyoom_syslog_init()` (`msg.c:75-82`, `openlog("earlyoom",
   LOG_PID | LOG_NDELAY, LOG_DAEMON)` at `msg.c:79`), which `main.c:298-300` calls for the
   `--syslog` option (`main.c:187`). So: stderr unless `--syslog` was passed.
9. `fprintf(stderr, ...)` lines (`main.c:161`, `main.c:412-417`) bypass `logger()` entirely: they stay
   on stderr even under `--syslog`. The stream of a journal line therefore does not identify which
   earlyoom literal produced it.

## Gates and provenance

All bytes fetched by ordinary means (curl, no browser, no auth) on 2026-10-22 from
`raw.githubusercontent.com`. Re-fetched and hash-verified twice; the copy the L1 left at
`/fast/scratch/hyaku/mori-r26/kill.c` is byte-identical to my fetch (`cmp` clean, same sha256).
Tag resolution by read-only `git ls-remote --tags https://github.com/rfjakob/earlyoom.git`:
`refs/tags/v1.9.0` = `66d78843fd675859a09a52d3f17b1c408a827a34`, peeled
`refs/tags/v1.9.0^{}` = commit `202d4db0d308ca6478f68de68b46cae34896ddaf`.

```
Gate: https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/kill.c — HTTP 200, 21,169 B, sha256 b32e0fad65e298235102f98aff37e02c94400b544d454cb57192ae697b100bf3
      https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/msg.c  — HTTP 200,  6,864 B, sha256 a771c91529053341c290ede2a7df1d9fdf16e07fb9584db8a64604a45dea5197
      https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/msg.h  — HTTP 200,  1,027 B, sha256 e36604984a916fb00a624c27c73034bcd87d7d6facff9b290a6a561ee58de56c
      accessed 2026-10-22; tag v1.9.0 = commit 202d4db0d308ca6478f68de68b46cae34896ddaf
quotes (verbatim, <=25 words each):
  kill.c:627  "sending %s to process %d uid %d"
  kill.c:318  "escalating to SIGKILL after %.3f seconds"
  msg.c:104   "logger(LOG_WARNING, stderr, yellow, fmt, vl);"
```

## Ready-to-paste SOURCES.md row (id left as `S???`)

Insert in the registry table of `corpus/SOURCES.md` (next free id is `S114`; the L1 owns the number):

```
| S??? | earlyoom kill.c and msg.c at v1.9.0 — https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/kill.c ; https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/msg.c | code | A | earlyoom 1.9.0 kill-path log literals and the warn() output route: the action, escalation, kill-failure, dryrun, process-group and victim-selection texts, and whether warn() reaches stderr or syslog; not the poll-loop decision logic, not the meminfo threshold parsing, not this host's unit configuration | kill.c:272,282,318,329,338,609,617-627,654; msg.c:14,66-73,75-82,99-107; msg.h:10; tag v1.9.0 = commit 202d4db0d308ca6478f68de68b46cae34896ddaf; kill.c 21,169 B sha256 b32e0fad65e298235102f98aff37e02c94400b544d454cb57192ae697b100bf3; msg.c 6,864 B sha256 a771c91529053341c290ede2a7df1d9fdf16e07fb9584db8a64604a45dea5197; opened 2026-10-22 | The action line is a format string whose body names uid, process name and cmdline, so a reader counts and never copies; an escalated kill prints the escalation text but no SIGKILL action text, so the two counters are distinct populations; warn() writes to stderr unless --syslog switches logger() to syslog. | mined | 2026-10-22 | on-release | corpus/knowledge/userspace-oom-killers-r26.md |
```

Tier **A**: primary upstream project source at the exact release tag the C2 contract names
(`v1.9.0`); the C2 message grammar is defined by these literals, and the file was read in full at
that tag. Status **mined**: the row is cited by the new FR10 entry (`corpus/knowledge/userspace-oom-killers-r26.md`,
required by C1) and by the C2 tool's grammar. Used-by is written for the planned r26 entry; if the
L1 lands that entry under another name, adjust that one cell. Recheck **on-release** (a new earlyoom
tag can move these literals).

## Facts with line numbers (all from the v1.9.0 bytes above)

| Fact | Location |
|---|---|
| action literal is `sending %s to process %d uid %d "%s": ... cmdline "%s"` | `kill.c:627-629` |
| `sig_name` values `SIGTERM` / `SIGKILL` / `0 (no-op signal)` | `kill.c:617-624` |
| action literal printed only when `sig != 0 \|\| enable_debug` | `kill.c:625-626` |
| escalation text `escalating to SIGKILL after %.3f seconds` | `kill.c:318` |
| escalation sends SIGKILL via `kill_release()` directly (no action line) | `kill.c:317-322` |
| `kill failed: %s` | `kill.c:654` |
| `kill failed` also fires on the wait timeout (errno ETIME) | `kill.c:336-338`, `kill.c:653-654` |
| action line precedes `kill_wait()`, so `kill failed:` never appears without an action line | `kill.c:627`, `kill.c:640`, `kill.c:653-654` |
| `low memory!` printed before victim selection; the recheck can recover and skip the kill | `main.c:517-524`, `main.c:526-539` |
| recovery message `memory situation has recovered while selecting victim` | `main.c:537` |
| `process %d exited after %.3f seconds` | `kill.c:329` |
| `process %d did not exit` | `kill.c:338` |
| wait loop: 100 iterations of 100 ms (about 10 s) | `kill.c:268`, `kill.c:306` |
| dryrun per-attempt text `dryrun, not actually sending any signal` | `kill.c:272` |
| dryrun flag text `dryrun mode enabled, will not kill anything` | `main.c:295` |
| `args.dryrun` is assigned in exactly one place, right after that warn | `main.c:296` |
| `kill.c:272` is reachable only from `kill_wait()` inside `poll_loop()` | `kill.c:640`, `main.c:539` |
| startup print order: banner → options → totals/thresholds → poll loop | `main.c:161`, `195-341`, `412-417`, `431` |
| process-group text `killing whole process group %d (-g flag is active)` | `kill.c:282` |
| `pid` negated to the process group id before signalling | `kill.c:276-282` |
| `Could not find a process to kill. Sleeping 1 second.` | `kill.c:609` |
| that path signals nothing (returns before any `kill()`) | `kill.c:608-615` |
| `warn()` calls `logger(LOG_WARNING, stderr, ...)` | `msg.c:99-107` (call at `msg.c:104`) |
| `logger()` picks syslog vs the handed stream | `msg.c:66-73` |
| `use_syslog` default 0, set only by `earlyoom_syslog_init()` | `msg.c:14`, `msg.c:75-82` |
| `openlog("earlyoom", LOG_PID \| LOG_NDELAY, LOG_DAEMON)` | `msg.c:79` |
| `--syslog` option enables it | `main.c:187`, `main.c:298-300` |
| threshold format `PRIPCT "%5.2lf%%"` (width 5, 2 decimals) | `msg.h:10` |
| version banner `earlyoom " VERSION` | `main.c:161` |
| threshold lines printed with `fprintf(stderr, ...)`, not `warn()` | `main.c:412-417` |
| low-memory texts `low memory! at or below SIGKILL/SIGTERM limits` | `main.c:519`, `main.c:523` |

## Fixture cross-check (read-only over both frozen case files)

Both files were read, not written. Hit lists below are the **decoded** ones (a byte-array `MESSAGE`
decoded as UTF-8 with replacement, contract.md:66). Counted `cases.json` sha256 `84d2343f…`
(32 cases); supplementary `cases-supplementary.json` sha256 `277684eb…` (32 cases); 29 shared ids,
counted-only `c19`/`c24`/`c28`, supplementary-only `c33`/`c34`/`c35`.

| keyword | counted `cases.json` | supplementary `cases-supplementary.json` |
|---|---|---|
| `kill` (lowercase) | c16, c18, c23, c24 | c16, c18, c21, c23 |
| `sending` | c01, c02, c03, c04, **c11**, **c12**, c13, c14, c20, c21, c28 | c01, c02, c03, c04, **c11**, **c12**, c13, c14, c20, c21, c33, c35 |
| `process` | c02, c03, c04, **c11**, **c12**, c13, c14, c21 | c02, c03, c04, **c11**, **c12**, c13, c14, c21, c35 |

`c11` and `c12` carry a byte-array `MESSAGE` decoding to the `kill.c:627` form
`sending SIGTERM to process 4242 "imaginary-keeper"` (c12 with a U+FFFD inside the invented name);
both expect `sigterm` 1 and `KILLER_ACTED`/1. A scan over string-typed values only misses them.
The `kill` lists differ structurally: the counted file has `c24` ("kill failed Operation not
permitted", no colon), the supplementary has `c21` carrying the five real `kill.c` lines, whose
`Could not find a process to kill. Sleeping 1 second.` (`kill.c:609`) supplies a lowercase `kill`.

## Host-side corroboration (read-only, this host)

Read-only commands only: `systemctl show earlyoom.service -p ...`, `systemctl cat earlyoom.service`,
`journalctl -q -b -u earlyoom.service -o json --output-fields=MESSAGE`, `git ls-remote`.

- `earlyoom.service` on this host: `ExecStart=/usr/bin/earlyoom $EARLYOOM_ARGS`,
  `StandardOutput=journal`, `StandardError=inherit`, `ActiveEnterTimestampMonotonic=19964362`.
- The unit file `/usr/lib/systemd/system/earlyoom.service` carries no `--syslog`; a read-only
  `grep -c -- '--syslog' /etc/default/earlyoom` returned `0` (count only; the file's contents were
  not copied). So `use_syslog == 0` here and `warn()` writes to **stderr**.
- Journal evidence for the route: 13 lines match `-u earlyoom.service`; 12 carry
  `SYSLOG_IDENTIFIER=earlyoom`, `_TRANSPORT=stdout`, `PRIORITY=6`, `_SYSTEMD_UNIT=earlyoom.service`,
  and 1 is systemd's own `Started Early OOM Daemon.` (`_SYSTEMD_UNIT=init.scope`). stderr lines of a
  service with `StandardError=inherit` therefore surface in the journal as **stdout transport,
  priority 6**, not as syslog transport.
- Scope boundary holds on this host: the `earlyoom 1.9.0` version line has
  `__MONOTONIC_TIMESTAMP=19981126`, which is greater than `ActiveEnterTimestampMonotonic=19964362`,
  so the invocation's version line is inside the C2 scope and `scope_complete` can be true.
- Grammar observed this boot: version 1, term-threshold 1, kill-threshold 1, action 0, escalation 0,
  kill-failed 0, dryrun 0. No earlyoom line this boot names a process, uid or command line.
- Padding trap, host-visible: the kill-threshold line renders as
  `        SIGKILL when mem avail <=  5.00% and swap free <=  5.00%` — `%5.2lf` pads `5.00` to
  width 5, so there are **two** spaces after `<=`, while the term line renders
  `sending SIGTERM when mem avail <= 10.00% and swap free <= 10.00%,` with one space.
- `journalctl -q -b -u earlyoom.service -o json --output-fields=MESSAGE` keeps exactly
  `MESSAGE`, `_BOOT_ID`, `__CURSOR`, `__MONOTONIC_TIMESTAMP`, `__REALTIME_TIMESTAMP`, `__SEQNUM`,
  `__SEQNUM_ID`; it drops `_SYSTEMD_UNIT`, `SYSLOG_IDENTIFIER` and `_PID`, so the tool cannot
  attribute a line to the unit by field from that query.

## Contradictions and risks to flag (verbatim for the L1 / canonical judge)

1. **Dry-run versus verdict rule 1 (real conflict).** `kill_process()` prints the action line at
   `kill.c:627` *before* it calls `kill_wait()` (`kill.c:640`), and `kill_wait()` returns early in
   dry-run mode with `dryrun, not actually sending any signal` (`kill.c:271-274`). So a dry-run
   invocation still emits `sending SIGTERM to process ...` while killing nothing. C2 verdict rule 1
   says "any earlyoom `sending SIG…to process` ... line in scope" is `KILLER_ACTED` (exit 1). As
   written, a dry-run host reports a kill that never happened. The contract's output schema does
   carry a `dryrun` field, so the rule can be reconciled, but the rule text itself does not exempt
   dry-run scope. Flagged, not fixed here.
   — Status after peer check: the tool seat confirms it follows the rule literally (an in-scope
   action line yields `KILLER_ACTED`, exit 1) and surfaces `"dryrun": true` in the result so the
   consumer can reconcile it; it reports no change and no re-commit. The open point is therefore
   the **rule text**, owned by the L1: either the contract states that dry-run scope is exempt, or
   the schema's `dryrun` field is named as the reconciliation. Not a tool defect; no further input
   requested from this seat.
   — **Resolved by the L1.** Contract amendment A2 (`contract.md:152-167`), A6 adopted: "when the
   invocation logged `dryrun mode enabled`, send lines go to `earlyoom.dryrun_send_lines`,
   `sigterm`/`sigkill` stay 0 and they are never positive evidence (X1)". The tool implements it at
   `tools/mori-oom-killers.py:369-374` (the dryrun send lines are moved out of `sigterm`/`sigkill`
   and never reach the positive-evidence test), and the dryrun flag itself is taken from
   `PREFIX_DRYRUN = "dryrun mode enabled"` (`tools/mori-oom-killers.py:115`), i.e. from the
   `main.c:295` line — the same sourcing this seat's reachability argument showed is the only
   source on a real host. The tool's own comment at `tools/mori-oom-killers.py:366-368` cites
   `kill.c:626-629` and `kill.c:271-273` for the behaviour. This contradiction is closed; no further
   action is required from this seat.
   — The tool's prefix constants match the upstream literals exactly: `PREFIX_KILL_FAILED =
   "kill failed: "` (`kill.c:654`), `PREFIX_ESCALATION = "escalating to SIGKILL after "`
   (`kill.c:318`), `PREFIX_LOW_MEMORY_TERM`/`_KILL` (`main.c:523`/`main.c:519`),
   `PREFIX_PROCESS_GROUP = "killing whole process group "` (`kill.c:282`), `RE_SIGTERM_ACTION`/
   `RE_SIGKILL_ACTION` (`kill.c:627`). The threshold regexes use `<=\s*` before the number
   (`tools/mori-oom-killers.py:102-107`), which is the padding tolerance this seat flagged in
   contradiction 2 — already in place.
2. **Threshold padding versus the fixed threshold grammar.** `PRIPCT` is `"%5.2lf%%"` (`msg.h:10`),
   so `5.00` renders as ` 5.00%` (leading pad) and `10.00` renders as `10.00%`. The contract's
   threshold grammar is written with a single space (`mem avail <= <a>%`), and the frozen case file
   is said to use thresholds `10.00/10.00/5.00/5.00`. A strict `mem avail <= (\d+\.\d+)%` match
   fails on the kill-threshold line of the host-shaped case. The tool and case seats should allow
   whitespace before the number. — Status after peer check: the tool seat reports its threshold
   patterns already accept whitespace between `<=` and the number, and its case
   `thresholds-with-width-padding` covers it, so no change is needed there; the case seat was sent
   the same note (`.ufo/waves/round-26/w1/WriteOomKillersCases.md` is that seat's report).
3. **The `-g` and dry-run-per-attempt texts are outside the contract grammar.** `kill.c:282`,
   `kill.c:272`, `kill.c:329`, `kill.c:338`, `kill.c:609` exist at v1.9.0 but are not in the C2
   grammar list. None of them is a kill action; the case seat should assert they are **not** counted
   as actions, so the fixtures pin that boundary.
4. **`kill failed` is not a "no kill happened" signal.** It also covers the 10-second wait timeout
   (`kill.c:336-338` → `kill.c:653-654`). The contract calls the `kill_failed` counter "failed kill";
   that name is fine but the semantics should not be read as "no signal was sent".
   — Counter ranking, settled from source for the mutation seat's open question: `kill failed:` is
   always accompanied by the action line for the same attempt (the action is printed at `kill.c:627`,
   `kill_wait()` is called at `kill.c:640`, and only then can `kill.c:653-654` fire), so it is never
   independent evidence; and `low memory!` (`main.c:519`, `main.c:523`) is printed **before** victim
   selection, so the recheck at `main.c:526-539` can print
   `memory situation has recovered while selecting victim` (`main.c:537`) and skip the kill
   altogether — a `low memory!` line can exist with no action line at all. The contract's literal
   rule 1 (action lines and escalation lines are positive evidence; `kill failed:` and `low memory!`
   are counted but unranked) matches the source. Treating either counter as independent positive
   evidence would report a threshold crossing that recovered as a kill.
   — Status: the L1's amendments A1 and A2 (`contract.md:127-179`) do **not** rule on whether
   `kill failed:` or `low memory!` are positive evidence; the frozen cases pin the counters
   (`c16` pins `kill_failed` 1 with `sigkill` 0, `c17` pins `low_memory_warnings` 2) and the
   tool counts them without treating them as positive evidence
   (`tools/mori-oom-killers.py:358-361`). The source reading above is the source-supported one and
   the mutation seat has recorded it as the settled reading in its battery rather than an open
   choice. Reachability note for the L1, should the question be taken up: the `c17` shape (two
   `low memory!` lines, no action) is reachable on a live host, whereas the `c16` shape (a
   `kill failed:` line with no action line) is not — it is synthetic, because `kill.c:627` always
   precedes `kill.c:653-654`.
5. **Stream cannot be inferred per line.** `fprintf(stderr, ...)` literals (`main.c:161`,
   `main.c:412-417`) bypass `logger()`, so under `--syslog` a host would put version/threshold lines
   on stderr and `warn()` lines on syslog. [INFERENCE] journald records a syslog-transported line
   with `PRIORITY=4` and `_TRANSPORT=syslog`, so a tool that assumes one transport per unit will
   misread a `--syslog` host. This host does not use `--syslog`.
6. **Scope query includes non-earlyoom lines.** `journalctl -b -u earlyoom.service` also returns
   systemd's unit lifecycle message (`Started Early OOM Daemon.`, `_SYSTEMD_UNIT=init.scope`),
   which sits inside the `ActiveEnterTimestampMonotonic` window. It matches no grammar line, so the
   grammar filter removes it; the tool must rely on the grammar, not on the `-u` filter alone.
7. `main.c` anchors (`main.c:161`, `295`, `414`, `416`, `519`, `523`) were verified here only as
   cross-checks of the contract text; they belong to the `SrcEarlyoomMainC` row and were not
   absorbed into this seat's row.

## Touched surfaces

- Wrote only this report: `.ufo/waves/round-26/w1/SrcEarlyoomKillC.md`.
- Scratch (read-only source copies): `/fast/scratch/hyaku/mori-r26/SrcEarlyoomKillC/{kill.c,msg.c,msg.h,main.c,meminfo.c,globals.h,kill.h,proc_pid.c,proc_pid.h}`.
- No lane file other than this report was created or edited; no git/jj command was run in the lane;
  no unit was started, stopped, enabled or restarted; no product code, judge or corpus file changed.

## Out of scope (not done here)

- No SOURCES.md edit (row supplied above for the L1 to paste); no entry text for
  `corpus/knowledge/userspace-oom-killers-r26.md`; no tool or case code (other seats); `main.c` line
  anchors were not sourced into a row (another seat).

## Tooling

No tool was installed, upgraded or downgraded this run; no pacman transaction was attempted (host-wide
pacman pause). Reads used the preinstalled `curl 8.23.0` and `python3 3.14.8` (standard library only).
