# CaseA2r04 — blind cases for rule A2-04 (dry-run send lines)

Seat `MoriR28.CaseA2r04` (case writer, blind to the tool). Rule **A2-04** — "after `dryrun mode enabled`, send lines go to
`earlyoom.dryrun_send_lines`, `sigterm`/`sigkill` stay 0, never positive evidence" (`.ufo/waves/round-27/contract.md:52`;
adopted form A6 at `.ufo/waves/round-26/contract.md:166-167`).

Deliverable: three cases for the L1 to paste into `tools/fixtures/mori-oom-killers/cases-a2.json` (the L1 owns that file; I
wrote nothing in the lane except this report). Each case names exactly one `rule` (`A2-04`), pins the rule's required field
`earlyoom.dryrun_send_lines` (integer), and pins a verdict and an integer exit. Each case has exactly one invocation (one
version line), so the A2-07 per-invocation split is not needed to decide any pinned value and the case rests on A2-04 alone.
State varies across the three: oomd `inactive` with 0 notices (C1, C2) against oomd `active` with 2 notices (C3); the
invocation boundary varies (version line at, above and at `ActiveEnterTimestampMonotonic`); the send-line count varies (1, 2, 1)
and the signalled process varies (SIGTERM, SIGTERM twice, SIGKILL). Files written by this seat: this report only.
Scratch (not in the lane): `/fast/scratch/hyaku/mori-r28/CaseA2r04/cases-a2r04.json`, sha256
`2cbcc5ef7057ab9df1d4587c2a6b4195485337fb246f44169bec66bde7f77ec1`. JSON validated with
`python3 -c 'import json,sys;json.load(sys.stdin)'` (exit 0), and the copy embedded below was re-parsed from this file.

## Cases (one fenced JSON array, paste-ready)

```json
[
 {"id": "a2-04-dryrun-sigterm-send-not-positive", "rule": "A2-04",
  "why": "Rule A2-04 (.ufo/waves/round-27/contract.md:52) in its adopted form A6 (.ufo/waves/round-26/contract.md:166-167): when the invocation logged `dryrun mode enabled`, send lines go to earlyoom.dryrun_send_lines, earlyoom.actions.sigterm and earlyoom.actions.sigkill stay 0, and they are never positive evidence. Shape: one invocation, one send line. The version line `earlyoom 1.9.0` (main.c:161, .ufo/waves/round-26/contract.md:82) is stamped 20000100, exactly ActiveEnterTimestampMonotonic, so it is inside the scope (.ufo/waves/round-26/contract.md:78-79) and scope_complete is true (.ufo/waves/round-26/contract.md:92-93); earlyoom.version is 1.9.0 and earlyoom.grammar is verified-1.9.0 (.ufo/waves/round-26/contract.md:82, 91). The flag line `dryrun mode enabled, will not kill anything` (main.c:295, .ufo/waves/round-26/contract.md:89) at 20000120 sets earlyoom.dryrun true (.ufo/waves/round-26/contract.md:94). The only send line of this invocation, `sending SIGTERM to process 7301 \"imaginary-lantern\"` (kill.c:627 form, .ufo/waves/round-26/contract.md:85), is stamped 20000300, after the flag, so it is counted in earlyoom.dryrun_send_lines (1) and not in earlyoom.actions.sigterm (0) or earlyoom.actions.sigkill (0) (.ufo/waves/round-26/contract.md:166-167); the pid and the invented process name are placeholders and no uid or cmdline is carried into the fixture (.ufo/waves/round-26/contract.md:107). Because a dry-run send line is never positive evidence and no other positive evidence exists (.ufo/waves/round-26/contract.md:97 lists only in-scope send or escalation lines and oomd notices above zero), the verdict is KILLERS_QUIET exit 0 (.ufo/waves/round-26/contract.md:102-104). No escalation, kill failed or low memory line is in scope, so those counts are 0 (.ufo/waves/round-26/contract.md:86-88, 94). No threshold line (main.c:414, main.c:416) is present, so earlyoom.thresholds is null (.ufo/waves/round-26/contract.md:91-92). `mem total: ...` (main.c:412) and `dryrun, not actually sending any signal` (kill.c:272) are outside the closed message grammar (.ufo/waves/round-26/contract.md:80-89), so they change no count. earlyoom.state is active, oomd.state is inactive and oomd.notices_this_boot is 0 (.ufo/waves/round-26/contract.md:90-95).",
  "inputs": {
   "earlyoom_show": "LoadState=loaded\nActiveState=active\nUnitFileState=enabled\nActiveEnterTimestampMonotonic=20000100\n",
   "oomd_show": "LoadState=loaded\nActiveState=inactive\nUnitFileState=disabled\nActiveEnterTimestampMonotonic=0\n",
   "earlyoom_journal": [
    {"MESSAGE": "earlyoom 1.9.0", "__MONOTONIC_TIMESTAMP": "20000100"},
    {"MESSAGE": "dryrun mode enabled, will not kill anything", "__MONOTONIC_TIMESTAMP": "20000120"},
    {"MESSAGE": "mem total: 16384 MiB, user mem total: 15000 MiB, swap total: 8192 MiB", "__MONOTONIC_TIMESTAMP": "20000140"},
    {"MESSAGE": "sending SIGTERM to process 7301 \"imaginary-lantern\"", "__MONOTONIC_TIMESTAMP": "20000300"},
    {"MESSAGE": "dryrun, not actually sending any signal", "__MONOTONIC_TIMESTAMP": "20000310"}],
   "oomd_notices": 0},
  "expect": {"verdict": "KILLERS_QUIET", "exit": 0, "fields": {
   "earlyoom.state": "active", "earlyoom.version": "1.9.0", "earlyoom.grammar": "verified-1.9.0",
   "earlyoom.thresholds": null, "earlyoom.scope_complete": true, "earlyoom.dryrun": true,
   "earlyoom.dryrun_send_lines": 1, "earlyoom.actions.sigterm": 0, "earlyoom.actions.sigkill": 0,
   "earlyoom.actions.escalations": 0, "earlyoom.actions.kill_failed": 0, "earlyoom.actions.low_memory_warnings": 0,
   "oomd.state": "inactive", "oomd.notices_this_boot": 0}}},
 {"id": "a2-04-dryrun-two-sigterm-sends-counted", "rule": "A2-04",
  "why": "Rule A2-04 (.ufo/waves/round-27/contract.md:52, adopted as A6 at .ufo/waves/round-26/contract.md:166-167) with a different count, a different invocation boundary and threshold lines in scope. The version line `earlyoom 1.9.0` (main.c:161) is stamped 30015100, after ActiveEnterTimestampMonotonic 30015000, so it is inside the scope (.ufo/waves/round-26/contract.md:78-79) and scope_complete is true (.ufo/waves/round-26/contract.md:92-93), with earlyoom.version 1.9.0 and earlyoom.grammar verified-1.9.0 (.ufo/waves/round-26/contract.md:82, 91). The flag line `dryrun mode enabled, will not kill anything` (main.c:295) at 30015200 sets earlyoom.dryrun true (.ufo/waves/round-26/contract.md:89, 94). Two send lines of that same dry-run invocation follow, `sending SIGTERM to process 7302 \"imaginary-marmot\"` at 30016000 and `sending SIGTERM to process 7303 \"imaginary-quill\"` at 30016500 (kill.c:627 form, .ufo/waves/round-26/contract.md:85), so earlyoom.dryrun_send_lines is 2 while earlyoom.actions.sigterm and earlyoom.actions.sigkill stay 0 (.ufo/waves/round-26/contract.md:166-167); the pids and the invented process names are placeholders and no uid or cmdline is carried into the fixture (.ufo/waves/round-26/contract.md:107). The threshold lines of main.c:414 and main.c:416 are in scope and are not send lines, so they set earlyoom.thresholds to 20.00/20.00/12.00/12.00 percent (.ufo/waves/round-26/contract.md:83-84, 91-92; PRIPCT at msg.h:10 is a five character field, and both values here are five characters wide, so no pad space is rendered) and they add no action count (.ufo/waves/round-26/contract.md:85). No escalation, kill failed or low memory line is in scope, so those counts are 0 (.ufo/waves/round-26/contract.md:86-88, 94). The dry-run send lines are never positive evidence and oomd notices are 0, so no positive evidence exists (.ufo/waves/round-26/contract.md:97) and the verdict is KILLERS_QUIET exit 0 (.ufo/waves/round-26/contract.md:102-104). earlyoom.state is active, oomd.state is inactive and oomd.notices_this_boot is 0 (.ufo/waves/round-26/contract.md:90-95).",
  "inputs": {
   "earlyoom_show": "LoadState=loaded\nActiveState=active\nUnitFileState=enabled\nActiveEnterTimestampMonotonic=30015000\n",
   "oomd_show": "LoadState=loaded\nActiveState=inactive\nUnitFileState=disabled\nActiveEnterTimestampMonotonic=0\n",
   "earlyoom_journal": [
    {"MESSAGE": "earlyoom 1.9.0", "__MONOTONIC_TIMESTAMP": "30015100"},
    {"MESSAGE": "dryrun mode enabled, will not kill anything", "__MONOTONIC_TIMESTAMP": "30015200"},
    {"MESSAGE": "sending SIGTERM when mem avail <= 20.00% and swap free <= 20.00%,", "__MONOTONIC_TIMESTAMP": "30015300"},
    {"MESSAGE": "        SIGKILL when mem avail <= 12.00% and swap free <= 12.00%", "__MONOTONIC_TIMESTAMP": "30015300"},
    {"MESSAGE": "sending SIGTERM to process 7302 \"imaginary-marmot\"", "__MONOTONIC_TIMESTAMP": "30016000"},
    {"MESSAGE": "sending SIGTERM to process 7303 \"imaginary-quill\"", "__MONOTONIC_TIMESTAMP": "30016500"}],
   "oomd_notices": 0},
  "expect": {"verdict": "KILLERS_QUIET", "exit": 0, "fields": {
   "earlyoom.state": "active", "earlyoom.version": "1.9.0", "earlyoom.grammar": "verified-1.9.0",
   "earlyoom.thresholds.term_mem_pct": 20.0, "earlyoom.thresholds.term_swap_pct": 20.0,
   "earlyoom.thresholds.kill_mem_pct": 12.0, "earlyoom.thresholds.kill_swap_pct": 12.0,
   "earlyoom.scope_complete": true, "earlyoom.dryrun": true,
   "earlyoom.dryrun_send_lines": 2, "earlyoom.actions.sigterm": 0, "earlyoom.actions.sigkill": 0,
   "earlyoom.actions.escalations": 0, "earlyoom.actions.kill_failed": 0, "earlyoom.actions.low_memory_warnings": 0,
   "oomd.state": "inactive", "oomd.notices_this_boot": 0}}},
 {"id": "a2-04-dryrun-send-with-oomd-notices", "rule": "A2-04",
  "why": "Rule A2-04 (.ufo/waves/round-27/contract.md:52, adopted as A6 at .ufo/waves/round-26/contract.md:166-167) with a SIGKILL send line and a non-zero oomd notice count, so the verdict is carried by a different killer and the dry-run send line is shown not to be its source. The version line `earlyoom 1.9.0` (main.c:161) at 40020000 equals ActiveEnterTimestampMonotonic 40020000, so it is inside the scope (.ufo/waves/round-26/contract.md:78-79), scope_complete is true, earlyoom.version is 1.9.0 and earlyoom.grammar is verified-1.9.0 (.ufo/waves/round-26/contract.md:82, 91-93). The flag line `dryrun mode enabled, will not kill anything` (main.c:295) at 40020100 sets earlyoom.dryrun true (.ufo/waves/round-26/contract.md:89, 94). The send line `sending SIGKILL to process 7304 \"imaginary-sable\"` (kill.c:627 form with sig_name set to SIGKILL, .ufo/waves/round-26/contract.md:85) at 40020200 belongs to that dry-run invocation, so it is counted in earlyoom.dryrun_send_lines (1) and never in earlyoom.actions.sigterm or earlyoom.actions.sigkill, which stay 0 (.ufo/waves/round-26/contract.md:166-167); the pid and the invented process name are placeholders and no uid or cmdline is carried into the fixture (.ufo/waves/round-26/contract.md:107). oomd_notices is 2, which is positive evidence on its own, so the verdict is KILLER_ACTED exit 1 (.ufo/waves/round-26/contract.md:97-98), and oomd.state is active with oomd.notices_this_boot 2 (.ufo/waves/round-26/contract.md:90-95). No escalation, kill failed or low memory line is in scope, so those counts are 0 (.ufo/waves/round-26/contract.md:86-88, 94); no threshold line is present, so earlyoom.thresholds is null (.ufo/waves/round-26/contract.md:91-92). earlyoom.state is active (.ufo/waves/round-26/contract.md:90). The contract does not say what a dry-run invocation does to the warning and escalation counters, so no value for earlyoom.actions.low_memory_warnings is pinned here beyond the absence of such a line, which fixes it at 0 (.ufo/waves/round-26/contract.md:88, 94).",
  "inputs": {
   "earlyoom_show": "LoadState=loaded\nActiveState=active\nUnitFileState=enabled\nActiveEnterTimestampMonotonic=40020000\n",
   "oomd_show": "LoadState=loaded\nActiveState=active\nUnitFileState=static\nActiveEnterTimestampMonotonic=40015000\n",
   "earlyoom_journal": [
    {"MESSAGE": "earlyoom 1.9.0", "__MONOTONIC_TIMESTAMP": "40020000"},
    {"MESSAGE": "dryrun mode enabled, will not kill anything", "__MONOTONIC_TIMESTAMP": "40020100"},
    {"MESSAGE": "sending SIGKILL to process 7304 \"imaginary-sable\"", "__MONOTONIC_TIMESTAMP": "40020200"}],
   "oomd_notices": 2},
  "expect": {"verdict": "KILLER_ACTED", "exit": 1, "fields": {
   "earlyoom.state": "active", "earlyoom.version": "1.9.0", "earlyoom.grammar": "verified-1.9.0",
   "earlyoom.thresholds": null, "earlyoom.scope_complete": true, "earlyoom.dryrun": true,
   "earlyoom.dryrun_send_lines": 1, "earlyoom.actions.sigterm": 0, "earlyoom.actions.sigkill": 0,
   "earlyoom.actions.escalations": 0, "earlyoom.actions.kill_failed": 0, "earlyoom.actions.low_memory_warnings": 0,
   "oomd.state": "active", "oomd.notices_this_boot": 2}}}
]
```

## Derivation per case (field, value, contract line)

"r26" = `.ufo/waves/round-26/contract.md`, "r27" = `.ufo/waves/round-27/contract.md`.
Case tags: **C1** = `a2-04-dryrun-sigterm-send-not-positive`, **C2** = `a2-04-dryrun-two-sigterm-sends-counted`,
**C3** = `a2-04-dryrun-send-with-oomd-notices`.

| Case | Field | Value | Contract line / reason |
|---|---|---|---|
| C1 | earlyoom.state | active | r26:90 (state enum); show text `ActiveState=active` |
| C1 | earlyoom.version | 1.9.0 | r26:82, :90; version line at 20000100 |
| C1 | earlyoom.grammar | verified-1.9.0 | r26:90-91; version 1.9.0 in scope |
| C1 | earlyoom.thresholds | null | r26:91-92; no main.c:414/:416 line in scope |
| C1 | earlyoom.scope_complete | true | r26:92-93, scope :78-79; version line == ActiveEnterTimestampMonotonic, so in scope |
| C1 | earlyoom.dryrun | true | r26:89, :94; flag line at 20000120 |
| C1 | earlyoom.dryrun_send_lines | 1 | **rule** r27:52, r26:166-167; one send line after the flag |
| C1 | earlyoom.actions.sigterm | 0 | rule r26:166-167; the send line is diverted |
| C1 | earlyoom.actions.sigkill | 0 | rule r26:166-167; no sigkill send line |
| C1 | earlyoom.actions.escalations | 0 | r26:86, :94; no escalation line in scope |
| C1 | earlyoom.actions.kill_failed | 0 | r26:87, :94; no kill-failed line in scope |
| C1 | earlyoom.actions.low_memory_warnings | 0 | r26:88, :94; no low-memory line in scope |
| C1 | oomd.state | inactive | r26:95; show text `ActiveState=inactive` |
| C1 | oomd.notices_this_boot | 0 | r26:95; `oomd_notices` input 0 |
| C1 | verdict / exit | KILLERS_QUIET / 0 | r26:97 (no positive evidence), :102-104; a dry-run send is never positive evidence |
| C2 | earlyoom.state | active | r26:90 |
| C2 | earlyoom.version | 1.9.0 | r26:82, :90 |
| C2 | earlyoom.grammar | verified-1.9.0 | r26:90-91 |
| C2 | earlyoom.thresholds.term_mem_pct / term_swap_pct | 20.0 / 20.0 | r26:83, :91-92; main.c:414 line; PRIPCT msg.h:10 is 5 wide, 20.00 needs no pad |
| C2 | earlyoom.thresholds.kill_mem_pct / kill_swap_pct | 12.0 / 12.0 | r26:84, :91-92; main.c:416 line; PRIPCT msg.h:10 |
| C2 | earlyoom.scope_complete | true | r26:92-93, :78-79; version line 30015100 > ActiveEnterTimestampMonotonic 30015000 |
| C2 | earlyoom.dryrun | true | r26:89, :94 |
| C2 | earlyoom.dryrun_send_lines | 2 | **rule** r27:52, r26:166-167; two send lines after the flag, same invocation |
| C2 | earlyoom.actions.sigterm | 0 | rule r26:166-167; both sends diverted |
| C2 | earlyoom.actions.sigkill | 0 | rule r26:166-167; no sigkill send line |
| C2 | earlyoom.actions.escalations / kill_failed / low_memory_warnings | 0 / 0 / 0 | r26:86-88, :94; no such line in scope |
| C2 | oomd.state / notices_this_boot | inactive / 0 | r26:95 |
| C2 | verdict / exit | KILLERS_QUIET / 0 | r26:97, :102-104; threshold lines are not sends (r26:85), so no positive evidence |
| C3 | earlyoom.state | active | r26:90 |
| C3 | earlyoom.version | 1.9.0 | r26:82, :90 |
| C3 | earlyoom.grammar | verified-1.9.0 | r26:90-91 |
| C3 | earlyoom.thresholds | null | r26:91-92; no threshold line |
| C3 | earlyoom.scope_complete | true | r26:92-93, :78-79; version line 40020000 == ActiveEnterTimestampMonotonic 40020000 |
| C3 | earlyoom.dryrun | true | r26:89, :94 |
| C3 | earlyoom.dryrun_send_lines | 1 | **rule** r27:52, r26:166-167; one SIGKILL send line after the flag |
| C3 | earlyoom.actions.sigterm | 0 | rule r26:166-167 |
| C3 | earlyoom.actions.sigkill | 0 | rule r26:166-167; the SIGKILL send is diverted, not counted |
| C3 | earlyoom.actions.escalations / kill_failed / low_memory_warnings | 0 / 0 / 0 | r26:86-88, :94; no such line in scope |
| C3 | oomd.state | active | r26:95; show text `ActiveState=active` |
| C3 | oomd.notices_this_boot | 2 | r26:95; `oomd_notices` input 2 |
| C3 | verdict / exit | KILLER_ACTED / 1 | r26:97-98; oomd notices > 0 is positive evidence on its own, the dry-run send contributes none |

Not pinned, because the contract text does not decide them for these inputs: `earlyoom.process_group_lines` and
`earlyoom.earlier_invocation_send_lines` (no `killing whole process group` line, no earlier invocation, in any of the three
journals), and `earlyoom.actions` as a whole object (its members are pinned individually instead).
`earlyoom.dryrun_send_lines` is pinned as an **integer count** of send lines, by analogy with the sibling counter
`earlyoom.earlier_invocation_send_lines`, which round-28 amendment A1 fixes as "an integer value above 0", and with
`earlyoom.process_group_lines`, which r26:164-165 describes as a count of log lines.

## Blindness statement — the tool was not opened

I did **not** open, grep, cat or run `tools/mori-oom-killers.py` or any copy of it; I did not open
`.ufo/waves/round-26/evidence/`, `.ufo/waves/round-26/w1`, `.ufo/waves/round-26/w2`, `.ufo/waves/round-27/w1` or
`.ufo/waves/round-27/w2`; I ran no self-test.

Files I opened:

1. `.ufo/waves/round-27/contract.md` — lines 40-80 only (the A2 rule table, :49-58).
2. `.ufo/waves/round-26/contract.md` — whole file (output spec :60-115, case schema :110-115, amendment A2 :152-200).
3. `tools/fixtures/mori-oom-killers/cases.json` — the frozen round-26 case file: schema, id style, journal record shape, `why`
   style, and the `earlyoom.thresholds` / `earlyoom.thresholds.*` pinning forms.
4. `.ufo/waves/round-28/contract.md` — the round-28 claim contract, which the wave context told me to read first; it carries
   the rule table by reference and amendment A2 (the case/tool mismatch judging rules), no tool internals.
5. `/home/vgpnk/.omp/agent/RULES.md` — the operator tooling rules the wave context told me to read first.
6. `tools/mori-retention-gate.py` (first 80 lines), `corpus/evidence/retention-allowlist.json` and
   `.ufo/waves/round-18/frozen/c1-policy.json` — to check that this report's text cannot raise the lane retention scan. The
   nine policy classes are OMP-settings / session / bash-log / document patterns; none matches this report's text.
7. Directory listings only, no file contents: `tools/`, `.ufo/waves/round-26/`, `.ufo/waves/round-28/`, `.ufo/waves/round-28/w1/`.
8. One repo-wide literal search for `retention-policy-v1` with `--include='*.json' --include='*.sh'` (to locate the policy
   file); it printed only `c1-policy.json` paths. No `.md` and no `.py` file was read by it, so no forbidden report body and no
   tool source was displayed.

## Sources (upstream earlyoom v1.9.0, fetched by curl)

Fetched 2026-10-22T17:59:35Z with `curl -sSfL` from `https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/<file>`:

| File | sha256 | Quote (verbatim, with line) |
|---|---|---|
| kill.c | `b32e0fad65e298235102f98aff37e02c94400b544d454cb57192ae697b100bf3` | kill.c:627 `warn("sending %s to process %d uid %d \"%s\": oom_score %d, oom_score_adj %d, VmRSS %lld MiB, cmdline \"%s\"\n",` |
| kill.c | same | kill.c:272 `warn("dryrun, not actually sending any signal\n");` |
| kill.c | same | kill.c:318 `warn("escalating to SIGKILL after %.3f seconds\n", secs);` |
| kill.c | same | kill.c:654 `warn("kill failed: %s\n", strerror(saved_errno));` |
| main.c | `08656b0bc90c85f23738661456b25c97af908bc5e2cfea78e0a69697b5f9d0e4` | main.c:161 `fprintf(stderr, "earlyoom " VERSION "\n");` |
| main.c | same | main.c:295 `warn("dryrun mode enabled, will not kill anything\n");` |
| main.c | same | main.c:412 `fprintf(stderr, "mem total: %4lld MiB, user mem total: %4lld MiB, swap total: %4lld MiB\n",` |
| main.c | same | main.c:414 `fprintf(stderr, "sending SIGTERM when mem avail <= " PRIPCT " and swap free <= " PRIPCT ",\n",` |
| main.c | same | main.c:416 `fprintf(stderr, "        SIGKILL when mem avail <= " PRIPCT " and swap free <= " PRIPCT "\n",` |
| main.c | same | main.c:519 `warn("low memory! at or below SIGKILL limits: mem " PRIPCT ", swap " PRIPCT "\n",` |
| msg.h | `e36604984a916fb00a624c27c73034bcd87d7d6facff9b290a6a561ee58de56c` | msg.h:10 `#define PRIPCT "%5.2lf%%"` |

Upstream fact the cases rely on: with `--dryrun`, earlyoom still logs `sending %s to process ...` (kill.c:627) and only then
skips the signal inside `kill_wait` (kill.c:271-273), so a dry-run journal really does contain a send line. That is the
situation A2-04 exists for, and it is why case C1 carries both lines in upstream order.

## Risks, limits and blockers

1. **Type of `earlyoom.dryrun_send_lines`.** The rule text says "send lines go to `earlyoom.dryrun_send_lines`" without saying
   count or list. I pinned an integer count, by analogy with `earlyoom.earlier_invocation_send_lines` (r27:54; round-28
   amendment A1 fixes it as an integer) and `earlyoom.process_group_lines` (r26:164-165). If the tool emits a list there, that
   is a "tool error" ruling under round-28 amendment A2 and the L1 changes the tool, never the case file.
2. **Tool matcher shape.** The contract grammar is prefix-anchored (r26:80-81), so `sending SIGTERM to process 7301 ...` matches
   on the prefix alone; if the tool's matcher additionally wants a pid-shaped token or a quoted name, each line carries both.
   I kept the frozen round-26 convention exactly: pid plus quoted invented name, no uid, no cmdline (r26:107; frozen `c11`/`c13`).
3. **Pids in the fixtures.** The pids 7301-7304 are invented placeholders, never read from this host, following the frozen
   round-26 file's own convention (`4242`, `5150` in `c11`-`c14`). No uid, no cmdline, no host unit name and no host
   configuration value appears in any case.
4. **Not decided, therefore not pinned.** What a dry-run invocation does to the escalation, kill-failed and low-memory-warning
   counters is not stated by r26:166-167. I therefore used journals without escalation, kill-failed or low-memory lines, so those
   counters are 0 for the plain reason that no such line exists, and I did not pin `earlyoom.process_group_lines` or
   `earlyoom.earlier_invocation_send_lines`.
5. **No counter run here.** `count-c2.sh` does not exist yet under `.ufo/waves/round-28/` (the directory holds `count-c1.sh`
   and `misroot-hash-check.sh`, no `count-c2.sh`), so the "≥2 cases per rule, ≥1 pinning the rule's field" requirement is
   satisfied by construction (3 cases, all pinning `earlyoom.dryrun_send_lines`) but not yet measured. The L1 assembles the
   ten seats' cases into `tools/fixtures/mori-oom-killers/cases-a2.json`.
6. **Tooling.** No package was installed or updated: `python3` 3.14.8 and `curl`, both already present, were enough, and all
   pacman transactions are paused host-wide, so no channel was used.

## What the L1 needs from this seat

Paste the fenced JSON array above into `tools/fixtures/mori-oom-killers/cases-a2.json` (schema `mori-oom-killers-cases-v1`
as in the frozen file, with one added key `rule` per case). No other change to the lane is needed from this seat.
