# Round 26 wave 1 — CriticC2Width (critic, leaf)

Seat `MoriR26.CriticC2Width`, 2026-10-22. Target: C2 as declared in `.ufo/waves/round-26/contract.md:48-118` and
`SCORECARD.md:1598` (HEAD `5b10649`). Tools installed or upgraded: none (curl, jq, python3, git, systemctl and
journalctl were already present). Scratch: `/fast/scratch/hyaku/mori-r26/MoriR26.CriticC2Width/`.

## Verdict

PASS N/N on cases frozen by another seat before the tool is a sound **counter**, but it is not enough by itself
for a capability row. It measures agreement between the tool and the contract's rules, not between the tool and
earlyoom. The case seat writes expected values from the contract (`contract.md:111-118`), so a contract rule
that turns an unknowable state into a number is frozen in as the right answer. This has already happened:
the cases were frozen at `5b10649` (blob `5b4dcee7`, 32 cases), and `c02`, `c04`, `c06` and `c19` expect
outputs that the counterexamples below show are wrong about the host. Nine counterexamples reproduce on the
tool seat's draft (`wt-tool` HEAD `74df6f5`, tool blob `0df359bc`, sha256 `7dfc65af…`). Six are contract
defects that the case file cannot catch. This is the same width gap the round-25 ruling describes
(`corpus/lessons/round-25-verifier-spotcheck.md:84-88`: the counter "measures agreement with 21 L1-written
examples" while the row said "never"). Writing the cases in a different seat makes the counter independent of
the tool author. It does not narrow the statement to what the counter can show.

## Why PASS N/N alone is too wide (four structural gaps)

1. **The contract is the case seat's oracle.** All 32 `why` fields cite `contract.md` or earlyoom source lines.
   When the two disagree (dry-run, restart), the cases follow the contract (`c02`, `c18`, `c19`; jq output below).
2. **The self-test only covers the pure reader.** Live collection is never exercised by `--selftest`
   (`contract.md:60-64`). That includes the journalctl flags, the exit-code and stderr handling, and the
   field filter. The draft discards stderr and treats any exit 0 as success (`wt-tool/tools/mori-oom-killers.py:410-424`).
3. **Nothing ties the tip's cases to the freeze.** C2 defines N at the freeze commit (`contract.md:53-54`), but the
   self-test runs over whatever `cases.json` is at the landed tip. No rule says the cases blob at the tip must
   equal blob `5b4dcee7`. Right now the HEAD blob equals the freeze blob (`git rev-parse 5b10649:… HEAD:…` →
   both `5b4dcee7…`).
4. **There is no committed receipt.** The round-25 closure ran no lane tool and verified the PASS line from
   committed evidence that carried the revision and the tool blob (`round-25-verifier-spotcheck.md:11-12,70`).
   C2 asks only that the command "prints" PASS (`contract.md:55-56`), and the declaration cites no evidence file
   (`SCORECARD.md:1598`).

Also: cases may pin zero fields (`jq '[.cases[]|.expect.fields|keys|length]|min'` → `0`), and only 23 of 32 pin
any `actions` field. An unpinned count is untested.

## Counterexamples run on the draft (inputs in scratch, invented process names)

Command: `python3 -I -B counterexamples.py`. It writes `in-X*.json` and runs
`python3 -I -B wt-tool/tools/mori-oom-killers.py --inputs <file>` on each.

| Id | Input shape | Draft output |
|---|---|---|
| X1 | `dryrun mode enabled`, then twice: low-memory line, `sending SIGTERM to process …`, `dryrun, not actually sending any signal` | `exit=1 KILLER_ACTED dryrun=True sigterm=2` |
| X2 | one `sending SIGTERM to process …`, then `killing whole process group … (-g flag is active)` | `exit=1 KILLER_ACTED sigterm=1` |
| X3 | complete startup, then `Suppressed 4321 messages from earlyoom.service` | `exit=0 KILLERS_QUIET scope_complete=True sigterm=0` |
| X4 | earlier invocation (version line, a SIGTERM line and a SIGKILL line before `ActiveEnterTimestampMonotonic`), then a clean current invocation | `exit=0 KILLERS_QUIET sigterm=0 sigkill=0` |
| X5 | `ActiveState=activating` (auto-restart window), journal holds a SIGTERM line | `exit=0 KILLERS_QUIET state=inactive actions=None` |
| X6 | `ActiveState=failed`, journal holds a SIGTERM line | `exit=0 KILLERS_QUIET state=inactive actions=None` |
| X7 | version and threshold lines only, no `mem avail:` line (the logger channel is not shown to reach the journal) | `exit=0 KILLERS_QUIET sigterm=0` |
| X8 | head-truncated: one SIGTERM line, no version line | `exit=1 KILLER_ACTED scope_complete=False sigterm=1` (an exact count, though the true value is at least 1) |
| X9 | earlyoom inactive, journal `[]`, `oomd_notices: 0` (what `-q` returns when the system journal is not readable) | `exit=0 KILLERS_QUIET` |

## The six named attacks: does the contract already abstain, and the rule to add

**A1 — journal truncation.**
- Head loss: **abstains** for quiet. A missing version line makes `scope_complete` false and the verdict
  `KILLERS_UNKNOWN` (`contract.md:92-93,99-100`; case `c05`).
- Head loss with an action: **does not abstain on the number.** Rule 1 keeps positive evidence
  (`contract.md:97-98`), and `c04` freezes `"earlyoom.actions.sigterm":1` with `scope_complete:false`. That is
  a lower bound printed as an exact count (X8).
- Middle loss: **does not abstain.** journald writes "Suppressed %i messages from %s" when it rate-limits a
  unit (systemd v262 `src/journal/journald-manager.c:1294`). The notice carries `OBJECT_SYSTEMD_UNIT`
  (`journald-manager.c:1146`), and `journalctl -u` matches `_UID=0` plus `OBJECT_SYSTEMD_UNIT`
  (`src/shared/logs-show.c:1748-1749`). So the notice is in the tool's input, but the grammar has no line
  for it (X3).
- Unreadable system journal: **does not abstain for oomd.** `-q` "Suppresses … any warning messages
  regarding inaccessible system journals when run as a normal user" (`man/journalctl.xml:797-799`). A user
  whose own user journal opens then gets empty stdout and `oomd_notices: 0` (X9). [INFERENCE] I only
  exercised the no-journal-at-all case, where `sudo -n -u nobody journalctl -q -b MESSAGE_ID=… -o json`
  exits 1 with 62 stderr bytes ("No journal files were opened due to insufficient permissions."), which the
  draft does catch. Dropping `-q` is not a fix: without it journalctl prints `-- No entries --` to stdout even
  in JSON mode (`src/journal/journalctl-show.c:605-606`).

```text
Rule A1a: When scope_complete is false or grammar is unverified, earlyoom.actions is null and KILLER_ACTED rests on a boolean positive_evidence field, never on counts.
Rule A1b: A journal line that starts with "Suppressed " and contains " messages from earlyoom.service" inside the scope sets scope_complete false.
Rule A1c: A journal read is null unless journalctl exits 0 and a same-run probe `journalctl -q -b -n 1 _PID=1 -o json` returns one entry (system journal readable).
```

**A2 — earlyoom restarted mid-boot.** **Does not abstain; the cases freeze the error.**
- The scope is the current invocation only (`contract.md:78-79`). Rule 3 still says `KILLERS_QUIET`.
- Upstream ships `Restart=always` with `MemoryMax=50M` (`earlyoom.service.in:17,20`), so a restart after an
  in-cgroup out-of-memory kill is a designed path.
- Case `c02` (action line 1 µs before `ActiveEnterTimestampMonotonic`) expects `KILLERS_QUIET` with
  `sigterm:0`. That is exactly X4.
- An inactive or failed earlyoom is reported as `actions: null` and the verdict is quiet (`contract.md:102-104`;
  cases `c06`, `c07`).
- The state enum has no value for `failed`, `activating`, `deactivating` or `reloading` (`contract.md:90-91`).
  The draft maps all of them to `inactive` (`mori-oom-killers.py:199-201`; X5, X6).
- oomd is scoped "this boot" while earlyoom is scoped "this invocation". One verdict word spans two
  different scopes.

On this host there has been no restart so far: `NRestarts=0`, 0 lines before activation, 13 in scope
(probe below).

```text
Rule A2a: A grammar-matching line before ActiveEnterTimestampMonotonic (or any boot line when earlyoom is not active) marks an earlier invocation: its send lines are positive evidence, and otherwise the verdict is KILLERS_UNKNOWN with earlier_invocation true, never KILLERS_QUIET.
Rule A2b: Any ActiveState other than active, inactive or a not-found LoadState maps to state unavailable and KILLERS_UNKNOWN.
```

**A3 — `--syslog` instead of stderr.** **Does not abstain; the cases freeze the error** (`c19`, "version line
only" → `KILLERS_QUIET`).
- `--syslog` switches only `logger()` output (`warn`/`info`/`fatal`) to `vsyslog` (`msg.c:66-72,76-79`).
- The version and threshold lines are plain `fprintf(stderr, …)` calls (`main.c:161,414-416`), so they stay
  on stderr. A run where syslog does not reach the unit's journal still shows a complete scope with zero sends.
- [INFERENCE] On a stock systemd host `/dev/log` is journald's socket and the lines arrive with
  `_SYSTEMD_UNIT`, so this is a guard, not an observed failure.
- There is a heartbeat: the first `mem avail:` report is printed immediately ("We start at zero so we print
  the first report immediately", `main.c:510-511`) through `info()` (`main.c:541-542`, `msg.c:124-128`).
  The upstream default keeps it on with `-r 3600` (`earlyoom.default:5`). This host shows 6 `mem avail:`
  lines in scope, on transport `stdout`.

```text
Rule A3: earlyoom counts are non-null only when the scope holds at least one "mem avail: " or "low memory! " line (proof the logger channel reaches the journal); otherwise actions is null and an active earlyoom is KILLERS_UNKNOWN.
```

Tradeoff to disclose: under A3, a host running `-r 0` with no low-memory event reads `KILLERS_UNKNOWN`.

**A4 — a version other than 1.9.0.** **Abstains for quiet** (`contract.md:100`; `c09` with `1.4.2` →
`KILLERS_UNKNOWN`). **Does not abstain for counts**: rule 1 runs before rule 2, and `c04` freezes `sigterm:1`
under `grammar:"unverified"`. The match string is not defined either:
- The upstream Makefile sets `VERSION` from `git describe --tags --dirty`, with the fallback
  `"(unknown version)"` (`Makefile:3-6`). Source builds therefore print `v1.9.0`, `v1.9.0-dirty` or
  `v1.9.0-N-g<hash>`.
- This host prints `1.9.0` (probe), and the draft tests `== "1.9.0"` (`mori-oom-killers.py:64,321`).
- A4 is covered by rule A1a for counts, plus:

```text
Rule A4: grammar is verified-1.9.0 only when the version string equals "1.9.0" exactly; "v1.9.0", any suffix and "(unknown version)" are unverified.
```

**A5 — `-g`.** **Does not abstain on meaning.** `-g` prints nothing at startup (`main.c:255-257`). At kill time
the same single `sending SIGTERM to process …` line (`kill.c:627`) is followed by a signal to the whole
process group (`kill.c:276-282`). `sigterm:1` then means one send event that hit an unknown number of
processes (X2).

```text
Rule A5: Add grammar "killing whole process group " → actions.process_group_sends; the schema states that every action count is a count of earlyoom log lines, not of processes signalled or killed.
```

**A6 — `--dryrun` lines counted as kills.** **Does not abstain.**
- In dry-run mode `kill_process` still prints `sending %s to process …` (`kill.c:626-629`). It then calls
  `kill_wait`, which returns at once after "dryrun, not actually sending any signal" (`kill.c:271-273`).
- The loop repeats on every poll while memory stays low (`main.c:514-540`).
- Contract rule 1 makes each such line `KILLER_ACTED` (`contract.md:97`). The only dry-run case, `c18`, has
  no send line, so the conflict is untested, and the draft returns `KILLER_ACTED sigterm=2` (X1).
- `args.dryrun` is set once per invocation (`main.c:294-296`), so a per-invocation rule is exact.

```text
Rule A6: When dryrun is true for the invocation, "sending SIG… to process" lines count as actions.dryrun_would_send, sigterm/sigkill stay 0, and they are never positive evidence.
```

## Other holes (smaller)

- Child processes run by `-N`, `-P` or the `-n` dbus-send helper write into the unit's journal. Their lines
  cannot be told apart, because only `MESSAGE` and the timestamp are kept (`contract.md:73-75`).
  Fix: keep `_TRANSPORT` and drop lines that are not `stdout`/`stderr`/`syslog`, or disclose the gap.
- Rate-limit loss at the very end leaves no marker until earlyoom's next accepted line, because the notice
  is written on the next accepted message (`journald-manager.c:1280-1295`). Rule A1b cannot close this; it
  is a residual to disclose.
- `--output-fields` always prints `__MONOTONIC_TIMESTAMP` (`man/journalctl.xml:673-675`). The scope clock is
  sound, and the host probe returned that key on all 13 lines.

## Freeze state and the smallest safe correction

The cases are already frozen (`5b10649`, "written by case seat WriteOomKillersCases, sandbox eaa13ef9"). The
tool is not yet in the lane: `git ls-tree -r --name-only HEAD -- tools/mori-oom-killers.py` returns nothing.
The freeze-order predicate is therefore still satisfiable. Two options:

1. **Preferred.** Land a contract amendment with rules A1a–A6 before the tool's first lane commit. Have the
   case seat (not the tool seat, not the L1) add cases X1–X9 and re-pin `c02` and `c04` to the new rules,
   re-frozen at a named commit. State N and that commit in the amendment. Add three lines to C2:

```text
C2-a: The cases blob at the landed tip equals the blob at the named freeze commit (git rev-parse <freeze>:<path> = git rev-parse <tip>:<path>).
C2-b: A committed receipt .ufo/waves/round-26/evidence/oom-killers-selftest.txt records revision, tool blob, cases blob, exit code and the PASS line.
C2-c: Every case pins earlyoom.actions (whole object or null), earlyoom.scope_complete and verdict.
```

2. **If no amendment lands.** Keep `PASS 32/32` as the counted value. Use the bounded capability row (variant B
   below), and carry X1–X9 as disclosed known false numbers in the r26 entry's Limits section. This is the
   round-25 R1/R2 posture, and it would be routed again.

The draft must not be shaped to pass X1–X9 before they are frozen. Doing so would invert the order rule.

## Draft SCORECARD capability row (no "never", no "kills")

Variant A, if rules A1a–A6 and C2-a–C2-c land before the tool:

```markdown
| userspace OOM killer read (earlyoom 1.9.0, systemd-oomd) | from `systemctl show` and this boot's journal, report each killer's unit state, the earlyoom version string and its four startup thresholds, counts of earlyoom signal-send, process-group, escalation, failed-kill and low-memory log lines for the current invocation, and the number of systemd-oomd kill notices this boot; verdict `KILLER_ACTED` on a logged real signal send (not dry-run) or an oomd notice, `KILLERS_UNKNOWN` when a read fails, the invocation start or logger heartbeat is missing, journald reports suppressed lines, an earlier invocation exists, or the version is not exactly 1.9.0, and `KILLERS_QUIET` otherwise. Counts are log lines, not processes killed; quiet means no such line in the journal the tool could read | `tools/mori-oom-killers.py --selftest` PASS N/N over cases frozen at `<freeze>` (blob `<blob>`, case seat ≠ tool seat ≠ L1); `.ufo/waves/round-26/evidence/oom-killers-selftest.txt`; `.ufo/waves/round-26/evidence/<live-run>.txt`; `corpus/knowledge/userspace-oom-killers-r26.md` | 26 |
```

Variant B, if the contract stays as frozen at `28b04940` with cases at `5b10649`:

```markdown
| userspace OOM killer read (earlyoom 1.9.0, systemd-oomd), bounded | from `systemctl show` and this boot's journal, report each killer's unit state, the earlyoom version string and four startup thresholds, counts of earlyoom signal-send, escalation, failed-kill and low-memory log lines since the current invocation started, and the number of systemd-oomd kill notices this boot, with a `KILLER_ACTED` / `KILLERS_UNKNOWN` / `KILLERS_QUIET` verdict as specified in contract C2. Known limits: dry-run send lines are counted as sends; one send under `-g` can hit a whole process group; journald rate-limit gaps and earlier invocations in the same boot are not seen; states other than active read as inactive; counts with an incomplete scope are lower bounds | `tools/mori-oom-killers.py --selftest` PASS 32/32 over cases frozen at `5b10649` (blob `5b4dcee7`) before the tool; `.ufo/waves/round-26/evidence/<live-run>.txt`; `corpus/knowledge/userspace-oom-killers-r26.md` (Limits) | 26 |
```

Words to keep out of either row: "never", "has not killed", "no OOM kill", "kills N processes", "complete".

## Host probe (counts, states, thresholds and version strings only)

`python3 -I -B /fast/scratch/hyaku/mori-r26/MoriR26.CriticC2Width/probe.py` reads `systemctl show
earlyoom.service` and `journalctl -q -b -u earlyoom.service -o json --output-fields=MESSAGE,_TRANSPORT`.
It printed:

```text
show.Type=simple show.Restart=always show.NRestarts=0 show.ActiveState=active show.UnitFileState=enabled
show.ActiveEnterTimestampMonotonic=19964362 show.ExecMainStartTimestampMonotonic=19964246
show.StandardOutput=journal show.StandardError=inherit show.LogRateLimitBurst=0 show.LogRateLimitIntervalUSec=0
journal.exit=0 stderr_bytes=0 journal.lines_boot=13 before_enter=0 in_scope=13
in_scope.counts={kill_line:1, mem_report:6, term_line:1, version:1} transports={journal:1, stdout:12}
version_strings=['1.9.0'] threshold_numbers=[['10.00','10.00'],['5.00','5.00']]
```

The host-shaped quiet case `c01` matches these values. This host shows 0 send lines, 0 dry-run lines,
0 suppression lines and 0 process-group lines this boot.

## Sources opened (2026-10-22, curl, HTTP 200)

URLs are `https://raw.githubusercontent.com/<path>`; sha256 values are in the block below the table.

| Path | Quote (verbatim, ≤25 words), line |
|---|---|
| rfjakob/earlyoom/v1.9.0/kill.c | `warn("dryrun, not actually sending any signal\n");` — 272 |
| rfjakob/earlyoom/v1.9.0/kill.c | `warn("killing whole process group %d (-g flag is active)\n", res);` — 282 |
| rfjakob/earlyoom/v1.9.0/main.c | `// Print a a memory report when this reaches zero. We start at zero so` — 510 |
| rfjakob/earlyoom/v1.9.0/msg.c | `vsyslog(priority, fmt, vl);` — 69 |
| rfjakob/earlyoom/v1.9.0/earlyoom.service.in | `Restart=always` — 17; `MemoryMax=50M` — 20 |
| rfjakob/earlyoom/v1.9.0/earlyoom.default | `EARLYOOM_ARGS="-r 3600"` — 5 |
| rfjakob/earlyoom/v1.9.0/Makefile | `VERSION ?= $(shell GIT_DIR=$(shell pwd)/.git git describe --tags --dirty)` — 3 |
| systemd/systemd/v262/man/journalctl.xml | `any warning messages regarding inaccessible system journals when run as a normal` — 798 |
| systemd/systemd/v262/src/journal/journald-manager.c | `LOG_MESSAGE("Suppressed %i messages from %s", rl - 1, c->unit),` — 1294 |
| systemd/systemd/v262/src/shared/logs-show.c | `(r = journal_add_match_pair(j, "OBJECT_SYSTEMD_UNIT", unit))` — 1749 |
| systemd/systemd/v262/src/journal/journalctl-show.c | `printf("-- No entries --\n");` — 606 |

sha256 of the fetched bytes (`sha256sum` in scratch). The earlyoom `main.c`, `kill.c`, `meminfo.c` and
`MANPAGE.md` re-fetches are byte-equal to the L1 copies in `/fast/scratch/hyaku/mori-r26/`:

```text
08656b0bc90c85f23738661456b25c97af908bc5e2cfea78e0a69697b5f9d0e4  earlyoom main.c
b32e0fad65e298235102f98aff37e02c94400b544d454cb57192ae697b100bf3  earlyoom kill.c
a771c91529053341c290ede2a7df1d9fdf16e07fb9584db8a64604a45dea5197  earlyoom msg.c
d4019b66d87539a006fc2d178d972dcf1b46e70343627b8bf66d1a08dcdda0bd  earlyoom earlyoom.service.in
c0770413a180e0731583f643fc4e84f4a0dac57efb8f575b74ee9a971df984a2  earlyoom earlyoom.default
b852cb9b832729f37f2b19fe93956720a5a58017aa8f76a6036cc928d96127ae  earlyoom Makefile
d54bbede45d5b1e3dc856da9624649ef8cb0829731597c212be303a76a1edbdd  systemd man/journalctl.xml
428dc8308d5caf70faee074e87888264c3708aa8e24c6069854790b952a7ffa2  systemd src/journal/journald-manager.c
abc2fc1f3d6f10d0f01b4d1ff18689eb5561a98fd71fde911117ce16c50ed72f  systemd src/shared/logs-show.c
c61d8534e11f2b212372ae70dac593f0b8f33879ebf1034d470d9dc41da75f65  systemd src/journal/journalctl-show.c
```

## Addendum — cross-check with SrcEarlyoomTagHistory (received 13:23Z)

That seat's report (`w1/SrcEarlyoomTagHistory.md:111,164-165,218-220`) agrees with this one and changes no rule.
- The `sending SIGTERM when mem avail` threshold line first appears in v1.8 (`v1.8/main.c:382`). The send and
  escalation prefixes are stable from v1.7 to v1.9.0. So the version line is the only thing that tells v1.8 from
  1.9.0, and rule A4 (an exact `1.9.0` match on the version line, never inferred from a threshold line) stands.
- Because the send prefix is stable, nulling counts under an unverified grammar (rule A1a) costs little true
  signal for v1.7–v1.8. The rule is still needed for the incomplete-scope lower bound and for untested versions.
- `sending 0 (no-op signal) to process …` (`kill.c:620-629`) is printed only when debug mode is on (`-d`,
  `kill.c:626`), at the startup self-test. The exact prefixes in `contract.md:85` already exclude it. The cases
  have no near-miss case for it.

## Impacted axes

- coverage: C2's capability statement is wider than its counter.
- calibration: a SCORECARD row that overclaims repeats round-25 R2.
- operability: the verdict exit codes are what callers branch on.

Fixable defects: A1a, A1b, A1c, A2a, A2b, A5, A6, C2-a, C2-b and C2-c.
Tradeoffs the judge must weigh:
- Rule A3 makes `-r 0` hosts read `KILLERS_UNKNOWN`.
- Rule A2a makes any host with a restart this boot read `KILLERS_UNKNOWN` unless a send is logged.
- Residual: rate-limit loss at the end of the journal stays invisible.
