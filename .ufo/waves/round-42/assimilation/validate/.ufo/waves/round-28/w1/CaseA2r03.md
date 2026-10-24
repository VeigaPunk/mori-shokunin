# Round 28 wave 1 — CaseA2r03: blind case writer for rule A2-03 (`killing whole process group ` lines)

Seat: MoriR28.CaseA2r03 (executor, leaf). Written 2026-10-22, last clock read `2026-10-22T18:12:18Z`.
Rule under test: **A2-03** — "`killing whole process group ` lines are counted in `earlyoom.process_group_lines`"
(round-27 contract.md:51; adopted as A5 in round-26 contract.md:164-165).

## What this seat delivers

Three A2-03 cases, each naming exactly one `rule` id, ready to append to `tools/fixtures/mori-oom-killers/cases-a2.json`.
Distinctness from the frozen round-26 file: invented group ids (5507, 6111, 6112, 6223, 6224, 6225), invented
timestamps (20500000 / 41000000 / 62000000), invented process name (`imaginary-lantern`, not a frozen name), invented
thresholds (20.00/10.00, not 10.00/5.00), an oomd-active shape, and a two-invocation journal. No frozen round-26 case
contains a `killing whole process group` line (grep over the frozen file returns none), so all three are new shapes.

Falsifiers, in order of strength: (1) **the count is of log lines, not of processes** — r26 :164-165 says so, and case 2
carries two group lines and no send line, so the group counter must read 2 while every action counter reads 0 and the
two counters cannot alias; (2) **the count is scoped** — case 3 puts a group line at exactly
`ActiveEnterTimestampMonotonic` (inside the scope by r26 :78, `>=`) plus an earlier invocation's version line outside
the scope, so the count must be 3, not 4 and not 0; (3) **the verdict does not come from the group lines** — case 2's
only positive evidence is `oomd_notices` (r26 :97) and cases 1 and 3 carry an in-scope send line, so all three
verdicts are decided by r26 :97 independently of whether a group line also counts as positive evidence, a question
the contract text does not decide and no case here bets on.

## Cases (one JSON array, ready to append)

```json
[
{"id": "a2-03-group-kill-one-with-sigterm-action",
 "rule": "A2-03",
 "why": "Rule A2-03 (round-27 contract.md:51; round-26 contract.md:164-165): `killing whole process group ` lines are counted in earlyoom.process_group_lines, and every count is a count of earlyoom log lines, not of processes signalled or killed. The group line here is the upstream rendering of kill.c:282, `warn(\"killing whole process group %d (-g flag is active)\\n\", res)`, with the invented group id 5507; the group id is invented and no uid, name or command line is carried. The line sits one microsecond after the SIGTERM send line of kill.c:627 and both are inside the scope, because round-26 contract.md:78 scopes earlyoom lines to a timestamp at or after ActiveEnterTimestampMonotonic=20500000, so process_group_lines is 1. The send line is an action line and the group line is not, so the action counts follow only the two action prefixes of round-26 contract.md:85: sigterm 1, sigkill 0; no escalation, kill failed or low memory line is present either (round-26 contract.md:86-88). The version line of main.c:161 is at exactly 20500000, inside the scope, so scope_complete is true and the version parses to 1.9.0, so grammar is verified-1.9.0 (round-26 contract.md:90, :82). The threshold lines of main.c:414 and main.c:416 are inside the scope and PRIPCT (msg.h:10) renders 20.00 and 10.00 without a pad space, so the thresholds are 20.0, 20.0, 10.0 and 10.0 (round-26 contract.md:83-84). No `dryrun mode enabled` line (main.c:295) is present, so dryrun is false (round-26 contract.md:89). The in scope send line is positive evidence, so the verdict is KILLER_ACTED exit 1 (round-26 contract.md:97). The oomd side is inactive with 0 notices, so it contributes no evidence (round-26 contract.md:95, :97).",
 "inputs": {
  "earlyoom_show": "LoadState=loaded\nActiveState=active\nUnitFileState=enabled\nActiveEnterTimestampMonotonic=20500000\n",
  "oomd_show": "LoadState=loaded\nActiveState=inactive\nUnitFileState=disabled\nActiveEnterTimestampMonotonic=0\n",
  "earlyoom_journal": [
   {"MESSAGE": "earlyoom 1.9.0", "__MONOTONIC_TIMESTAMP": "20500000"},
   {"MESSAGE": "sending SIGTERM when mem avail <= 20.00% and swap free <= 20.00%,", "__MONOTONIC_TIMESTAMP": "20500000"},
   {"MESSAGE": "        SIGKILL when mem avail <= 10.00% and swap free <= 10.00%", "__MONOTONIC_TIMESTAMP": "20500000"},
   {"MESSAGE": "sending SIGTERM to process 5507 \"imaginary-lantern\"", "__MONOTONIC_TIMESTAMP": "20510000"},
   {"MESSAGE": "killing whole process group 5507 (-g flag is active)", "__MONOTONIC_TIMESTAMP": "20510001"}],
  "oomd_notices": 0},
 "expect": {"verdict": "KILLER_ACTED", "exit": 1, "fields": {
  "earlyoom.state": "active", "earlyoom.version": "1.9.0", "earlyoom.grammar": "verified-1.9.0",
  "earlyoom.thresholds.term_mem_pct": 20.0, "earlyoom.thresholds.term_swap_pct": 20.0,
  "earlyoom.thresholds.kill_mem_pct": 10.0, "earlyoom.thresholds.kill_swap_pct": 10.0,
  "earlyoom.scope_complete": true,
  "earlyoom.actions.sigterm": 1, "earlyoom.actions.sigkill": 0, "earlyoom.actions.escalations": 0,
  "earlyoom.actions.kill_failed": 0, "earlyoom.actions.low_memory_warnings": 0,
  "earlyoom.process_group_lines": 1, "earlyoom.dryrun": false,
  "oomd.state": "inactive", "oomd.notices_this_boot": 0}}},
{"id": "a2-03-group-kill-two-no-action-oomd-notices",
 "rule": "A2-03",
 "why": "Rule A2-03 (round-27 contract.md:51; round-26 contract.md:164-165) against the action counters. Two `killing whole process group ` lines are in scope, rendered as upstream kill.c:282 does it, `warn(\"killing whole process group %d (-g flag is active)\\n\", res)`, with the invented group ids 6111 and 6112; no uid, name or command line is carried. The fixture deliberately omits a `sending SIG... to process ` line so that the two counters cannot alias: the group lines are counted in earlyoom.process_group_lines, whose value is 2, a count of two earlyoom log lines and not of the processes in those groups (round-26 contract.md:164-165), while the action counts stay at 0 because round-26 contract.md:85 makes only the two send prefixes action lines; a group line names no signal, so it cannot be counted as a sigterm or a sigkill. No escalation, kill failed or low memory line is present either (round-26 contract.md:86-88). All three journal lines are at or after ActiveEnterTimestampMonotonic=41000000 and the version line of main.c:161 is at exactly 41000000, so the scope is complete and the version parses to 1.9.0, so grammar is verified-1.9.0 (round-26 contract.md:78, :90, :82). No threshold line of main.c:414 or main.c:416 is present, so the thresholds are unknown and the thresholds block is null (round-26 contract.md:92). No `dryrun mode enabled` line (main.c:295), so dryrun is false (round-26 contract.md:89). The verdict does not come from the earlyoom side: the only positive evidence is the oomd notice count of 4, which round-26 contract.md:97 makes positive evidence on its own, so the verdict is KILLER_ACTED exit 1; the oomd state is active because the show text carries ActiveState=active, and the notice count is the one given in the inputs (round-26 contract.md:95).",
 "inputs": {
  "earlyoom_show": "LoadState=loaded\nActiveState=active\nUnitFileState=enabled\nActiveEnterTimestampMonotonic=41000000\n",
  "oomd_show": "LoadState=loaded\nActiveState=active\nUnitFileState=static\nActiveEnterTimestampMonotonic=30000000\n",
  "earlyoom_journal": [
   {"MESSAGE": "earlyoom 1.9.0", "__MONOTONIC_TIMESTAMP": "41000000"},
   {"MESSAGE": "killing whole process group 6111 (-g flag is active)", "__MONOTONIC_TIMESTAMP": "41000050"},
   {"MESSAGE": "killing whole process group 6112 (-g flag is active)", "__MONOTONIC_TIMESTAMP": "41000100"}],
  "oomd_notices": 4},
 "expect": {"verdict": "KILLER_ACTED", "exit": 1, "fields": {
  "earlyoom.state": "active", "earlyoom.version": "1.9.0", "earlyoom.grammar": "verified-1.9.0",
  "earlyoom.thresholds": null, "earlyoom.scope_complete": true,
  "earlyoom.actions.sigterm": 0, "earlyoom.actions.sigkill": 0, "earlyoom.actions.escalations": 0,
  "earlyoom.actions.kill_failed": 0, "earlyoom.actions.low_memory_warnings": 0,
  "earlyoom.process_group_lines": 2, "earlyoom.dryrun": false,
  "oomd.state": "active", "oomd.notices_this_boot": 4}}},
{"id": "a2-03-group-kill-three-after-earlier-invocation",
 "rule": "A2-03",
 "why": "Rule A2-03 (round-27 contract.md:51; round-26 contract.md:164-165) across an invocation boundary, with a higher count. The journal holds two version lines: an earlier invocation's version line of main.c:161 at 19960000, which is before ActiveEnterTimestampMonotonic=62000000 and therefore outside the current invocation (round-26 contract.md:78), and the current invocation's version line at exactly 62000000, which is inside the scope, so scope_complete is true and the version parses to 1.9.0, so grammar is verified-1.9.0 (round-26 contract.md:90, :82). Three `killing whole process group ` lines follow the current version line, at 62000000, 62000051 and 62000052, all rendered as upstream kill.c:282 does it, `warn(\"killing whole process group %d (-g flag is active)\\n\", res)`, with the invented group ids 6223, 6224 and 6225; no uid, name or command line is carried. The first of them is stamped exactly at ActiveEnterTimestampMonotonic, and round-26 contract.md:78 scopes earlyoom lines to a timestamp at or after that value, so the boundary line is inside the scope by the same rule the frozen case c03 pins for an action line; it also follows the current invocation's version line in the journal, so it belongs to that invocation. The other two group lines are plainly inside the scope, so process_group_lines is 3, a count of three earlyoom log lines and not of the processes in those groups (round-26 contract.md:164-165). The out of scope version line at 19960000 is the version line of an earlier invocation and not of the current one, so it neither sets the version nor makes the scope incomplete (round-26 contract.md:93). The only send line is the SIGKILL form of kill.c:627, so the sigkill count is 1 and the sigterm count is 0 (round-26 contract.md:85); there is no escalation, kill failed or low memory line (round-26 contract.md:86-88). No threshold line of main.c:414 or main.c:416 is present, so the thresholds block is null (round-26 contract.md:92), and no `dryrun mode enabled` line (main.c:295) is present, so dryrun is false (round-26 contract.md:89). The in scope SIGKILL send line is positive evidence, so the verdict is KILLER_ACTED exit 1 (round-26 contract.md:97). The oomd side is inactive with 0 notices and contributes no evidence (round-26 contract.md:95, :97).",
 "inputs": {
  "earlyoom_show": "LoadState=loaded\nActiveState=active\nUnitFileState=enabled\nActiveEnterTimestampMonotonic=62000000\n",
  "oomd_show": "LoadState=loaded\nActiveState=inactive\nUnitFileState=disabled\nActiveEnterTimestampMonotonic=0\n",
  "earlyoom_journal": [
   {"MESSAGE": "earlyoom 1.9.0", "__MONOTONIC_TIMESTAMP": "19960000"},
   {"MESSAGE": "earlyoom 1.9.0", "__MONOTONIC_TIMESTAMP": "62000000"},
   {"MESSAGE": "killing whole process group 6223 (-g flag is active)", "__MONOTONIC_TIMESTAMP": "62000000"},
   {"MESSAGE": "sending SIGKILL to process 6224 \"imaginary-lantern\"", "__MONOTONIC_TIMESTAMP": "62000050"},
   {"MESSAGE": "killing whole process group 6224 (-g flag is active)", "__MONOTONIC_TIMESTAMP": "62000051"},
   {"MESSAGE": "killing whole process group 6225 (-g flag is active)", "__MONOTONIC_TIMESTAMP": "62000052"}],
  "oomd_notices": 0},
 "expect": {"verdict": "KILLER_ACTED", "exit": 1, "fields": {
  "earlyoom.state": "active", "earlyoom.version": "1.9.0", "earlyoom.grammar": "verified-1.9.0",
  "earlyoom.thresholds": null, "earlyoom.scope_complete": true,
  "earlyoom.actions.sigterm": 0, "earlyoom.actions.sigkill": 1, "earlyoom.actions.escalations": 0,
  "earlyoom.actions.kill_failed": 0, "earlyoom.actions.low_memory_warnings": 0,
  "earlyoom.process_group_lines": 3, "earlyoom.dryrun": false,
  "oomd.state": "inactive", "oomd.notices_this_boot": 0}}}
]
```

## Derivation tables

Legend: `r26` = `.ufo/waves/round-26/contract.md`, `r27` = `.ufo/waves/round-27/contract.md`; line numbers are 1-based.
`fx` = the frozen round-26 file `tools/fixtures/mori-oom-killers/cases.json` (precedent for a pinned path).

### Case 1 — `a2-03-group-kill-one-with-sigterm-action`

| field | expected value | deciding line |
|---|---|---|
| `earlyoom.state` | `active` | r26 :90 (state enum) + show text `ActiveState=active` (same shape as fx `c01`) |
| `earlyoom.version` | `1.9.0` | r26 :82 (`earlyoom <version>`), main.c:161 |
| `earlyoom.grammar` | `verified-1.9.0` | r26 :90, :82 — version parses to 1.9.0 (fx `c19`) |
| `earlyoom.thresholds.term_mem_pct` | `20.0` | r26 :83, main.c:414, PRIPCT `msg.h:10` |
| `earlyoom.thresholds.term_swap_pct` | `20.0` | r26 :83, main.c:414, PRIPCT `msg.h:10` |
| `earlyoom.thresholds.kill_mem_pct` | `10.0` | r26 :84, main.c:416, PRIPCT `msg.h:10` |
| `earlyoom.thresholds.kill_swap_pct` | `10.0` | r26 :84, main.c:416, PRIPCT `msg.h:10` |
| `earlyoom.scope_complete` | `true` | r26 :93 + :78 — version line at `ActiveEnterTimestampMonotonic` is in scope (fx `c03`) |
| `earlyoom.actions.sigterm` | `1` | r26 :85 — one `sending SIGTERM to process ` line in scope |
| `earlyoom.actions.sigkill` | `0` | r26 :85 — no SIGKILL send line |
| `earlyoom.actions.escalations` / `.kill_failed` / `.low_memory_warnings` | `0` / `0` / `0` | r26 :86 / :87 / :88 — no escalation, `kill failed: ` or low-memory line |
| `earlyoom.process_group_lines` | `1` | r27 :51, r26 :164-165 — exactly one `killing whole process group ` line in scope |
| `earlyoom.dryrun` | `false` | r26 :89 — no `dryrun mode enabled` line (fx `c19`) |
| `oomd.state` | `inactive` | r26 :95 — oomd show text `ActiveState=inactive` |
| `oomd.notices_this_boot` | `0` | r26 :95 — the input value |
| verdict | `KILLER_ACTED` | r26 :97 — in-scope send line is positive evidence |
| exit | `1` | r26 :97 |

### Case 2 — `a2-03-group-kill-two-no-action-oomd-notices`

| field | expected value | deciding line |
|---|---|---|
| `earlyoom.state` | `active` | r26 :90 + show text `ActiveState=active` |
| `earlyoom.version` | `1.9.0` | r26 :82, main.c:161 |
| `earlyoom.grammar` | `verified-1.9.0` | r26 :90, :82 |
| `earlyoom.thresholds` | `null` | r26 :92 — no threshold line in scope (fx `c19` pins the same null) |
| `earlyoom.scope_complete` | `true` | r26 :93 + :78 |
| `earlyoom.actions.sigterm` | `0` | r26 :85 — group line is not a `sending SIGTERM to process ` prefix |
| `earlyoom.actions.sigkill` | `0` | r26 :85 — group line names no signal |
| `earlyoom.actions.escalations` / `.kill_failed` / `.low_memory_warnings` | `0` / `0` / `0` | r26 :86 / :87 / :88 — none of those lines present |
| `earlyoom.process_group_lines` | `2` | r27 :51, r26 :164-165 — two in-scope group lines |
| `earlyoom.dryrun` | `false` | r26 :89 |
| `oomd.state` | `active` | r26 :95 — oomd show text `ActiveState=active` (fx `c10` same shape) |
| `oomd.notices_this_boot` | `4` | r26 :95 — the input value |
| verdict | `KILLER_ACTED` | r26 :97 — `oomd_notices` > 0 is positive evidence on its own |
| exit | `1` | r26 :97 |

### Case 3 — `a2-03-group-kill-three-after-earlier-invocation`

| field | expected value | deciding line |
|---|---|---|
| `earlyoom.state` | `active` | r26 :90 + show text `ActiveState=active` |
| `earlyoom.version` | `1.9.0` | r26 :82, main.c:161 — both version lines read `1.9.0`, so the value is independent of which invocation is read |
| `earlyoom.grammar` | `verified-1.9.0` | r26 :90, :82 |
| `earlyoom.thresholds` | `null` | r26 :92 — no threshold line (fx `c19`) |
| `earlyoom.scope_complete` | `true` | r26 :93 + :78 — the current invocation's version line at `ActiveEnterTimestampMonotonic` is in scope; the 19960000 line is an earlier invocation's |
| `earlyoom.actions.sigterm` | `0` | r26 :85 |
| `earlyoom.actions.sigkill` | `1` | r26 :85 — one `sending SIGKILL to process ` line in scope |
| `earlyoom.actions.escalations` | `0` | r26 :86 |
| `earlyoom.actions.kill_failed` | `0` | r26 :87 |
| `earlyoom.actions.low_memory_warnings` | `0` | r26 :88 |
| `earlyoom.process_group_lines` | `3` | r27 :51, r26 :164-165 — three in-scope group lines; the one at exactly `ActiveEnterTimestampMonotonic` is in scope by r26 :78 (`>=`, fx `c03`) |
| `earlyoom.dryrun` | `false` | r26 :89 |
| `oomd.state` | `inactive` | r26 :95 |
| `oomd.notices_this_boot` | `0` | r26 :95 |
| verdict | `KILLER_ACTED` | r26 :97 — in-scope SIGKILL send line |
| exit | `1` | r26 :97 |

## Fields deliberately not pinned, and why

- `earlyoom.earlier_invocation_send_lines` — not pinned in any case. r26 :175-177 decides its *count* for case 3 (0:
  no send line lies outside the current invocation) but not whether the key is emitted when the count is 0, and it
  belongs to rule A2-06, not A2-03.
- `earlyoom.actions` as a whole object — not pinned; the individual counters are pinned (same style as the frozen
  file, which pins `earlyoom.actions` only when it is `null`).
- `earlyoom.thresholds.*` in cases 2 and 3 — not pinned; the block is `null` there (r26 :92), so the sub-paths do
  not exist. `earlyoom.error` — not pinned (r26 :105: the error text is implementation defined).
- An inactive/absent earlyoom with group lines — deliberately **not** written as a case. r26 :102 reserves `null`
  counts for an inactive or absent killer, and the contract text does not decide whether a group-line count is
  reported at all in that state; a case there would have to invent the value, and it could not pin the rule's
  required field honestly. State variation is therefore carried on the oomd side (inactive in cases 1 and 3, active
  in case 2) and by the invocation boundary in case 3.

## Blinding: what I did and did not open

**The tool was never opened, grepped, catted or run.** `tools/mori-oom-killers.py` (and any copy of it) was not
read, searched or executed; no self-test was run; `.ufo/waves/round-26/evidence/`, `.ufo/waves/round-26/w1`,
`.ufo/waves/round-26/w2`, `.ufo/waves/round-27/w1` and `.ufo/waves/round-27/w2` were never opened. Every expected
value above is derived from r26/r27 contract text plus upstream earlyoom v1.9.0 sources.

Files I opened (complete list):
- `.ufo/waves/round-27/contract.md` — the rule table, lines 40-80 only, plus one `grep` for the `A2-0` ids
  (returned lines 49-57, inside that range).
- `.ufo/waves/round-26/contract.md` — whole file (interface, output spec, verdicts, Amendment A2 at 152-200).
- `tools/fixtures/mori-oom-killers/cases.json` — schema and journal-line shapes (read ranges 6-120, 119-263, 390-483,
  599-758; one `grep` for `process group|oomd.state|oomd_notices|escalating|kill failed`).
- `.ufo/waves/round-28/w1/CriticC2Design.md` — **taint disclosure, self-reported.** This file is outside the read
  list I was given (round-28 wave reports were neither named as readable nor as forbidden), and it opens with its own
  blind-seat warning that the `CaseA2r*` writers must not read it before the freeze commit. I opened lines 1-45 of
  it while checking report house style, before I had seen the case file schema and before I wrote any case. It is a
  non-blind report: it describes the tool's internals (`read_inputs`, `_lookup`, output column names) and other rules
  (A2-07, A2-08, A2-09, A2-10). It says nothing about A2-03, about `earlyoom.process_group_lines`, or about any
  value I pin, and every expected value in this report is traceable to r26/r27 contract lines plus upstream v1.9.0
  sources (the per-field tables above cite those). My seat's blinding claim is nevertheless qualified by this read;
  the L1 should weigh that before freezing the file, and may prefer to re-derive the three A2-03 cases from this
  report's derivations alone.
- `/home/vgpnk/.omp/agent/RULES.md` — the operator tooling directive.
- Upstream earlyoom v1.9.0 via `curl` (see receipts below).

## Upstream source receipts

Fetched with `curl -fsSL` from `https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/<file>`; access time
`2026-10-22T18:00:13Z` for all three; sha256 of the fetched bytes:

| file | sha256 |
|---|---|
| `kill.c` | `b32e0fad65e298235102f98aff37e02c94400b544d454cb57192ae697b100bf3` |
| `main.c` | `08656b0bc90c85f23738661456b25c97af908bc5e2cfea78e0a69697b5f9d0e4` |
| `msg.h` | `e36604984a916fb00a624c27c73034bcd87d7d6facff9b290a6a561ee58de56c` |

Quotes cited by the three cases (verbatim, ≤25 words each, with line numbers):

- `kill.c:282` — `warn("killing whole process group %d (-g flag is active)\n", res);`
- `kill.c:627` — `warn("sending %s to process %d uid %d \"%s\": oom_score %d, oom_score_adj %d, VmRSS %lld MiB, cmdline \"%s\"\n",`
- `main.c:161` — `fprintf(stderr, "earlyoom " VERSION "\n");`
- `main.c:295` — `warn("dryrun mode enabled, will not kill anything\n");`
- `main.c:414` — `fprintf(stderr, "sending SIGTERM when mem avail <= " PRIPCT " and swap free <= " PRIPCT ",\n",`
- `main.c:416` — `fprintf(stderr, "        SIGKILL when mem avail <= " PRIPCT " and swap free <= " PRIPCT "\n",`
- `msg.h:10` — `#define PRIPCT "%5.2lf%%"`

(The r26 :86-88 grammar lines — escalation, kill failed, low memory — are named by the contract itself; no expected
value in these three cases depends on their upstream rendering, so they are not quoted here.)

## Files written, verification, tooling

- Written: `.ufo/waves/round-28/w1/CaseA2r03.md` (this report), plus scratch only, under the seat's own directory
  `/fast/scratch/hyaku/mori-r28/CaseA2r03/`: `cases-a2-r03.json` (the three cases, 115 lines, sha256
  `132f275c714947cd16b6ba76f3b7ee656369f80bd9ddbf073bda600dd5fa1e96`), `upstream/kill.c`, `upstream/main.c`,
  `upstream/msg.h`. Nothing else was written to the lane; no case file was edited or created in the lane; no jj, git
  or index operation was run.
- Verification actually run: `python3 -c 'import json,sys;json.load(sys.stdin)' < cases-a2-r03.json` → exit 0
  (`JSON_VALID`); the same check on the JSON block embedded above passes and that block parses equal to the scratch
  file (`IDENTICAL_TO_SCRATCH: True`). A structural check confirmed: 3 cases; keys exactly
  `{id, rule, why, inputs, expect}`; `rule == "A2-03"` for all; ids match `a2-03-<slug>`, ASCII, single line;
  `inputs` keys exactly `{earlyoom_show, oomd_show, earlyoom_journal, oomd_notices}`; `expect` keys exactly
  `{verdict, exit, fields}`; every journal record has exactly `MESSAGE` and a string `__MONOTONIC_TIMESTAMP`; every
  case pins `earlyoom.process_group_lines` (the required field for A2-03). No tool, no self-test and no counter was
  run — those belong to the L1 after the freeze commit.
- Tooling: no install or update was performed by this seat, so nothing is recorded under the operator's tooling
  directive. Pre-existing tools used: `curl 8.23.0` (upstream fetch) and `python3 3.14.8` (JSON validation). No pacman
  transaction was run; host-wide pacman transactions are paused for this wave.

## Risks and blockers

- **Interpretation risk (small, disclosed):** case 2 pins every action counter at 0 while two group lines are in
  scope. The contract's action grammar (r26 :85) admits only the two `sending SIG… to process ` prefixes, and A5
  (r26 :164-165) assigns group lines to their own field, so 0 is the contract-derived value. If the tool instead
  double-counts a group line into `actions.sigterm`/`sigkill`, case 2 fails and the L1 must choose: the case file is
  frozen and the tool is not, so the tool is what moves. Flagged so the L1 is not surprised by that failure mode.
- **Undecided question avoided:** whether a `killing whole process group` line is itself positive evidence (r26 :97
  lists only send lines, escalation lines and oomd notices) is not decided by the contract text. No case here depends
  on it: cases 1 and 3 have an in-scope send line, case 2 has `oomd_notices` > 0.
- **Scope-boundary reading:** case 3 assumes the count follows the same scope rule as the action counts (r26 :78,
  `>=`), which the frozen file pins for actions at `c03`. The out-of-scope line in case 3 is a version line, not a
  group line, so a reading in which the tool counts group lines over the whole boot rather than the current
  invocation's scope is *not* distinguished by these three cases; only `scope_complete`/`version` are.
- **No blocker.** The assignment is complete: 3 cases, derived from the contract, JSON-validated, with the required
  field pinned in each.
