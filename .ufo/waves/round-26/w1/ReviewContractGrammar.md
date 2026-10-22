# Review — contract message grammar vs earlyoom v1.9.0 (MoriR26.ReviewContractGrammar, 2026-10-22)

Scope: the "Message grammar" block of `.ufo/waves/round-26/contract.md` (section C2, Interface).
For every grammar line: (a) byte-exactness of the anchor after the prefix anchor, (b) cited line
number, (c) whether the line can be emitted with a prefix under `warn()` (msg.c), (d) whether a
message can split across two journal entries. Then: action-relevant messages the contract misses.

Method: re-fetched the tag-pinned upstream files this round (URLs and sha256 below), read the
emission sites, and did one read-only host-journal observation (`journalctl -q -b -u
earlyoom.service`) restricted to the version line and the two threshold lines — the only MESSAGE
text reproduced here contains version and threshold values, no process names, uids or command
lines (privacy bounds honored). No tools installed this round; no pacman transactions; no unit
started, stopped or restarted; lane untouched (this Report file is the only lane write).

## Sources (fetched 2026-10-22, sha256 of exact bytes quoted)

| File | URL | sha256 |
|---|---|---|
| main.c | https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/main.c | 08656b0bc90c85f23738661456b25c97af908bc5e2cfea78e0a69697b5f9d0e4 |
| kill.c | https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/kill.c | b32e0fad65e298235102f98aff37e02c94400b544d454cb57192ae697b100bf3 |
| msg.c | https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/msg.c | a771c91529053341c290ede2a7df1d9fdf16e07fb9584db8a64604a45dea5197 |
| msg.h | https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/msg.h | e36604984a916fb00a624c27c73034bcd87d7d6facff9b290a6a561ee58de56c |
| meminfo.c | https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/meminfo.c | 526e512c89c58cb0b1db2ae98ea62d287cdc1516846be80c9173bdc4bf0edfeb |
| Makefile | https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/Makefile | b852cb9b832729f37f2b19fe93956720a5a58017aa8f76a6036cc928d96127ae |
| journald-stream.c | https://raw.githubusercontent.com/systemd/systemd/v262/src/journal/journald-stream.c | e919ebe8c8d8fb435082d01bfd951ff0626196ae514dec4509a8c7a3d8617175 |

## Question (c): can a grammar line be emitted with a prefix? — No, in the journal capture path

- `warn()` adds **no text prefix**: msg.c:98 — "No "warning" prefix is added."; msg.c:99-107 passes
  the caller's fmt unchanged to `logger(LOG_WARNING, stderr, yellow, ...)` (msg.c:104).
- The only thing prepended is an ANSI color, and only when the target fd **is a tty**: msg.c:16 —
  "color_log writes to `f`, prefixing the `color` code if `f` is a tty." The gate is msg.c:32-44
  (`isatty` on stdout/stderr, `NO_COLOR` check msg.c:25-31); when not a tty, msg.c:48-52 sets
  `color = ""` and `reset = ""`, so the writes at msg.c:54 and :56 emit nothing. Under a systemd
  unit, stderr is the journal stream socket, never a tty → every `warn()` line lands in the journal
  byte-for-byte, no prefix, no suffix.
- `--syslog` mode: `logger` switches to `vsyslog(priority, fmt, vl)` (msg.c:68-72) — still no text
  prefix; the raw message text is unchanged (syslog priority/identifier travel in separate fields).
- The only textual prefixer in earlyoom is `fatal()` (`"fatal: "`, msg.c:84-90) — startup failures
  only; no grammar line goes through it.
- Host evidence: the three startup entries observed this round carried no `\x1b` byte
  (`ansi=False` for all three; values shown in "Host observations" below).

## Question (d): can a message split over two journal entries? — Each line is one entry; the threshold message IS two entries

- journald treats each newline-terminated line of a service's stdout/stderr stream as its own
  record: journald-stream.c:49-50 — "The different types of log record terminators: a real \n was
  read, a NUL character was read, the maximum line length"; dispatch is per line
  (journald-stream.c:325, `stdout_stream_line`); a plain newline adds no extra field
  (journald-stream.c:287 — "Do not add field if traditional newline").
- The two threshold lines are two separate `fprintf` calls, each ending in `\n`
  (main.c:414-415 and main.c:416-417) → **two journal entries**. The contract already models them
  as two grammar lines, which is correct; a case writer must treat them as independent entries.
- Host evidence: two distinct entries were observed (both with `__MONOTONIC_TIMESTAMP=19981234` —
  equal microsecond values are possible, so scope-boundary cases must not assume strict ordering
  *between* these two entries; both fall on the same side of any single boundary value).
- No grammar format string contains an interior `\n`, so no grammar line splits; and no single
  entry ever contains two grammar lines. The contract's per-entry scope rule
  (`__MONOTONIC_TIMESTAMP ≥ ActiveEnterTimestampMonotonic`) is entry-safe.

## Host observations (read-only journalctl, this boot's earlyoom invocation)

```
'earlyoom 1.9.0'                                                     ts=19981126  ansi=False
'sending SIGTERM when mem avail <= 10.00% and swap free <= 10.00%,'  ts=19981234  ansi=False
'        SIGKILL when mem avail <=  5.00% and swap free <=  5.00%'   ts=19981234  ansi=False
```

- Version on this host is `1.9.0` without a leading `v`, although Makefile:3 derives VERSION from
  `git describe --tags` (tag `v1.9.0`). The grammar rule `earlyoom <version>` is shape-agnostic —
  correct — but the tool should parse the remainder generically, not hardcode either shape.
- The SIGKILL row shows the `%5.2lf%%` padding (msg.h:10, `#define PRIPCT "%5.2lf%%"`): a value
  below 10 renders with a leading space inside the number, so `<= ` is followed by two spaces.
  Threshold parsing must tolerate that whitespace; the contract's host-shaped quiet case
  (10.00/10.00/5.00/5.00) exercises exactly this.

## Verdict per grammar line

| Contract line (anchor) | Cited | Byte-exact? | Verdict |
|---|---|---|---|
| `earlyoom <version>` (first line of invocation) | main.c:161 | yes (`"earlyoom " VERSION "\n"`) | **correct** |
| `sending SIGTERM when mem avail <= <a>% and swap free <= <b>%,` | main.c:414 | yes, incl. trailing comma (host-observed) | **correct** |
| `SIGKILL when mem avail <= <c>% and swap free <= <d>%` | main.c:416 | yes after whitespace strip; source line has 8 leading spaces, no trailing comma | **correct** (see padding note below) |
| `sending SIGTERM to process ` / `sending SIGKILL to process ` | kill.c:627 | yes at runtime — format is `sending %s to process %d uid %d "%s": oom_score %d, oom_score_adj %d, VmRSS %lld MiB, cmdline "%s"` with `%s` ∈ {SIGTERM, SIGKILL, "0 (no-op signal)"} (kill.c:617-629) | **correct** |
| `escalating to SIGKILL after ` | kill.c:318 | yes (`"escalating to SIGKILL after %.3f seconds\n"`) | **correct** |
| `kill failed: ` | kill.c:654 | yes (`"kill failed: %s\n"`) | **correct** |
| `low memory! at or below SIGTERM limits` / `... SIGKILL limits` | main.c:519-523 | yes; full strings `low memory! at or below SIGKILL limits: mem ` (main.c:519) and `... SIGTERM limits: mem ` (main.c:523) | **correct** (fix the range: cite main.c:519 and main.c:523; the statements span 519-520 and 523-524) |
| `dryrun mode enabled` | main.c:295 | yes (`"dryrun mode enabled, will not kill anything\n"`) | **correct** |

Line-number detail: every cited number matches the statement that emits the anchor. Only the
low-memory range is imprecise — `main.c:519-523` covers both warn statements' first lines but
truncates the SIGTERM statement's argument line (524). Fix: `main.c:519,523`.

Emission-condition notes a case writer needs:

- The `sending %s to process` line is emitted when `sig != 0 || enable_debug` (kill.c:626). With
  `-d` and the startup signal-0 self-test it reads `sending 0 (no-op signal) to process ...`
  (kill.c:623) — it matches neither action anchor, so no false positive; the contract's two
  prefixes stay safe.
- Each `low memory!` warning is immediately preceded by a stats line at warn level:
  `print_mem_stats(warn, m)` (main.c:518/522) printing `` `mem avail: %5lld of %5lld MiB (…), swap
  free: …` `` (meminfo.c:279). It is not a grammar line and must stay unmatched — prefix anchoring
  already excludes it.
- `escalating to SIGKILL after ` fires only inside the 10 s wait loop after a SIGTERM
  (kill.c:313-321); the SIGKILL-stats branch there is debug-only (kill.c:324-327, stdout).

## Action-relevant messages the contract misses

Ordered by relevance to the tool's action counters and verdicts. All are `warn()` (no prefix in
journal, per above); anchors proposed after the same leading-whitespace strip. Pid-bearing lines
need a regex rather than a fixed string.

1. `process %d exited after %.3f seconds` — kill.c:329. Termination confirmation inside the wait
   loop. Proposed anchor: `^process [0-9]+ exited after `.
2. `process %d did not exit` — kill.c:338. Victim survived the 10 s wait; `kill_wait` then returns
   -1, so a `kill failed: …` entry follows (kill.c:653-654). Direct corroboration of a failed
   kill. Anchor: `^process [0-9]+ did not exit`.
3. `killing whole process group %d (-g flag is active)` — kill.c:282 (the -g line). Signals that
   the pid passed to `kill()` is a negated pgid; action-mode context. Anchor:
   `^killing whole process group [0-9]+ \(-g flag is active\)`.
4. `Could not find a process to kill. Sleeping 1 second.` — kill.c:609. Low-memory episode with no
   victim: explains a nonzero `low_memory_warnings` count with zero actions. Fixed prefix works.
5. `memory situation has recovered while selecting victim` — main.c:537. Warning-without-action
   transition; distinguishes "warned, then recovered" from "warned, then killed". Fixed prefix.
6. `dryrun, not actually sending any signal` — kill.c:272. In dryrun mode the counted
   `sending SIG…to process` actions sent nothing. The contract captures the startup dryrun flag
   (main.c:295) but not this per-action qualifier; with it, the case seat can pin "actions
   counted but no signal sent" behavior.
7. Minor: `sleeping 1 second` — kill.c:662, EPERM throttle right after a failed kill;
   `…process_mrelease pidfd=… failed: …` — kill.c:253 (success variant is `info()`, stdout,
   kill.c:255); `selected myself (pid %d)` — kill.c:588; zombie `rss=0 but oom_score=%d` —
   kill.c:446. None required by the contract's output fields; list for completeness.

Adjacent lines the tool must keep unmatched (several are privacy-bearing): the prefer/avoid/ignore
regex echoes (main.c:379, 386, 393 — these contain the user's `--prefer`/`--avoid`/`--ignore`
expressions and must never be matched into any output), the victim detail tail of kill.c:627
(uid, name, cmdline — count the line, never print its fields), the `mem total:` line (main.c:412),
periodic/report `mem avail:` lines (meminfo.c:279 via main.c:542), option echoes (main.c:246, 249,
253, 282, 286, 407) and priority warnings (main.c:398, 403). The contract's prefix-anchored
grammar already excludes all of them; no defect, recorded as a must-not-match list.

## Residual risk and verification gaps

- v1.8-vs-v1.9.0 discrimination: I verified every v1.9.0 anchor myself but did not re-fetch v1.7 /
  v1.8. MoriR26.SrcEarlyoomTagHistory (same wave) reports the only grammar difference across those
  tags is the threshold wording, making the version line the sole discriminator; consequence:
  `grammar: verified-1.9.0` must be gated on the version line only — finding thresholds must not
  by itself mark the grammar verified. Corroborated, not independently re-verified.
- `--syslog` mode: I verified earlyoom sends the unchanged format text via `vsyslog` (msg.c:68-72)
  and [INFERENCE] that journald's syslog ingestion stores the unchanged text in `MESSAGE`; the
  host path exercised this round is the stderr stream path (no ANSI observed).
- I did not observe an action line, escalation, kill failure or dryrun line in the host journal —
  those verdicts rest on the source reading; the fixture cases are what will exercise them.
- The two equal `__MONOTONIC_TIMESTAMP` values on the threshold entries are one observation on one
  boot; journald timestamp granularity is not documented here. Cases must not depend on strict
  ordering between those two entries.

No tool installs or upgrades were needed this round (curl, journalctl, python3, git already
present); nothing to record under the tooling directive.
