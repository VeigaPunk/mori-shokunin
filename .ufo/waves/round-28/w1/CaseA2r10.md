# CaseA2r10 — blind cases for rule A2-10 (mori round 28, wave 1)

Seat: `MoriR28.CaseA2r10` (case writer, blind). L1: agent MoriR28.

**Rule under test (A2-10).** round-27/contract.md:58 — "a journal record without a numeric
`__MONOTONIC_TIMESTAMP` is left uncounted and makes the scope incomplete; positive evidence
elsewhere still stands". Adopted by the wave-2 fix at round-26/contract.md:186-188, which
explicitly supersedes the earlier setup-error rule of round-26/contract.md:168-169.

**Files changed.** None in the lane repository except this report file. The case JSON lives in the
seat scratch dir at `/fast/scratch/hyaku/mori-r28/CaseA2r10/cases-a2-10.json` (canonical, validated)
and is reproduced verbatim below for the L1 to merge into `tools/fixtures/mori-oom-killers/cases-a2.json`.

## Blindness statement

**I did not open the tool.** I never opened, grepped, catted or ran `tools/mori-oom-killers.py` or
any copy of it; never opened `.ufo/waves/round-26/evidence/` or the round-26 `w1`/`w2` or round-27
`w1`/`w2` reports; ran no self-test and no counter script. Every expected value below is derived from
the two contracts, the frozen case file, and the upstream earlyoom sources.

**The list of files I opened:**
1. `.ufo/waves/round-27/contract.md` — lines 40-80 (rule table; A2-10 at :58).
2. `.ufo/waves/round-26/contract.md` — whole file (interface :58-109, output :90-95, verdicts
   :96-106, case-file spec :111-115, Amendment A2 :152-190).
3. `tools/fixtures/mori-oom-killers/cases.json` — schema, journal line shapes, frozen c01-c32 field sets.
4. `https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/kill.c` (curl).
5. `https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/main.c` (curl).
6. `https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/msg.h` (curl).

Upstream receipts (fetched 2026-10-22T17:59:08Z; sha256 of the bytes fetched):
kill.c `b32e0fad65e298235102f98aff37e02c94400b544d454cb57192ae697b100bf3` (21169 B);
main.c `08656b0bc90c85f23738661456b25c97af908bc5e2cfea78e0a69697b5f9d0e4` (21053 B);
msg.h `e36604984a916fb00a624c27c73034bcd87d7d6facff9b290a6a561ee58de56c` (1027 B).
Quotes used (verbatim, ≤25 words): kill.c:318 `warn("escalating to SIGKILL after %.3f seconds\n", secs);`;
kill.c:627 `warn("sending %s to process %d uid %d \"%s\": oom_score %d, oom_score_adj %d, VmRSS %lld MiB, cmdline \"%s\"\n",`;
kill.c:654 `warn("kill failed: %s\n", strerror(saved_errno));`; main.c:161 `fprintf(stderr, "earlyoom " VERSION "\n");`;
main.c:295 `warn("dryrun mode enabled, will not kill anything\n");`; main.c:414 `fprintf(stderr, "sending SIGTERM when mem avail <= " PRIPCT " and swap free <= " PRIPCT ",\n",`;
main.c:416 `fprintf(stderr, "        SIGKILL when mem avail <= " PRIPCT " and swap free <= " PRIPCT "\n",`;
main.c:519 `warn("low memory! at or below SIGKILL limits: mem " PRIPCT ", swap " PRIPCT "\n",`;
main.c:523 `warn("low memory! at or below SIGTERM limits: mem " PRIPCT ", swap " PRIPCT "\n",`;
msg.h:10 `#define PRIPCT "%5.2lf%%"`.

## Cases (one fenced JSON array, ready to merge into `cases-a2.json`)

```json
[
 {
  "id": "a2-10-malformed-action-line-uncounted",
  "rule": "A2-10",
  "why": "Malformed timestamp: the record is left uncounted and the scope is incomplete. The journal holds the version line at 20441000 (in scope: 20441000 is not below ActiveEnterTimestampMonotonic 20441000, contract.md:78) and one record whose __MONOTONIC_TIMESTAMP is the non numeric string 'not-a-number'; that record carries an action line in the kill.c:627 shape 'sending SIGTERM to process 7301 \"imaginary-harvester\"' (invented pid and invented process name only; the uid and cmdline parts are dropped, as the frozen cases do at cases.json c02, c03, c13). round-27/contract.md:58 (rule A2-10, adopted by the wave-2 fix at round-26/contract.md:186-188, which supersedes the setup-error rule of round-26/contract.md:168-169) says such a record is left uncounted and makes the scope incomplete, so earlyoom.scope_complete is false even though the version line is inside the scope (contract.md:78, :92-93). Left uncounted, the record is not a line in scope (contract.md:78 needs a numeric timestamp to compare with ActiveEnterTimestampMonotonic) and therefore not positive evidence (contract.md:97): earlyoom.actions.sigterm is 0, not 1, and the other counts are 0 because no other counted line exists (contract.md:85-88; the frozen host shaped case pins the same five counts at 0, cases.json c01). Counts with an incomplete scope are printed as counts (round-26/contract.md:170, A1a, frozen c04), so the zero counts are pinned here. With no positive evidence and an active earlyoom whose scope is incomplete, the verdict is KILLERS_UNKNOWN exit 2 (contract.md:99-100). The version line 'earlyoom 1.9.0' (main.c:161) is in scope, so earlyoom.version is 1.9.0 (contract.md:82; cases.json c19). No threshold line (main.c:414, main.c:416) is present, so earlyoom.thresholds is null (contract.md:91-92; cases.json c19). No 'dryrun mode enabled' line (main.c:295) is present, so earlyoom.dryrun is false (contract.md:89, :94). The show text says ActiveState=active, so earlyoom.state is active (contract.md:90). The oomd show text says ActiveState=inactive and the notice count is 0, so oomd.state is inactive and oomd.notices_this_boot is 0 (contract.md:95). earlyoom.grammar is not pinned: the contract fixes the two grammar values (contract.md:91) but not whether an in scope version line still verifies the grammar when the scope is incomplete for another reason; the frozen cases pin 'verified-1.9.0' only for a complete scope (cases.json c19) and 'unverified' only when no version line is in scope (cases.json c04, c05).",
  "inputs": {
   "earlyoom_show": "LoadState=loaded\nActiveState=active\nUnitFileState=enabled\nActiveEnterTimestampMonotonic=20441000\n",
   "oomd_show": "LoadState=loaded\nActiveState=inactive\nUnitFileState=disabled\nActiveEnterTimestampMonotonic=0\n",
   "earlyoom_journal": [
    {"MESSAGE": "earlyoom 1.9.0", "__MONOTONIC_TIMESTAMP": "20441000"},
    {"MESSAGE": "sending SIGTERM to process 7301 \"imaginary-harvester\"", "__MONOTONIC_TIMESTAMP": "not-a-number"}
   ],
   "oomd_notices": 0
  },
  "expect": {
   "verdict": "KILLERS_UNKNOWN", "exit": 2,
   "fields": {
    "earlyoom.state": "active", "earlyoom.version": "1.9.0",
    "earlyoom.thresholds": null, "earlyoom.scope_complete": false,
    "earlyoom.actions.sigterm": 0, "earlyoom.actions.sigkill": 0,
    "earlyoom.actions.escalations": 0, "earlyoom.actions.kill_failed": 0,
    "earlyoom.actions.low_memory_warnings": 0, "earlyoom.dryrun": false,
    "oomd.state": "inactive", "oomd.notices_this_boot": 0
   }
  }
 },
 {
  "id": "a2-10-positive-evidence-elsewhere-stands",
  "rule": "A2-10",
  "why": "Malformed timestamp with positive evidence elsewhere: the record is left uncounted, the scope is incomplete, and the positive evidence still stands. The journal holds the version line at 31007000 (in scope: 31007000 is not below ActiveEnterTimestampMonotonic 31007000, contract.md:78), one record whose __MONOTONIC_TIMESTAMP is the non numeric string 'not-a-timestamp' carrying an escalation line, and one well formed escalation line at 31007500. The malformed record is left uncounted and makes the scope incomplete (round-27/contract.md:58; round-26/contract.md:186-188), so earlyoom.scope_complete is false and only the well formed line is counted: earlyoom.actions.escalations is 1, not 2 (contract.md:86; the escalation shape is kill.c:318 'escalating to SIGKILL after %.3f seconds', cases.json c15). The counted escalation line is in scope and is positive evidence, and positive evidence stands even when the scope is incomplete (contract.md:97-98), so the verdict is KILLER_ACTED exit 1 and not KILLERS_UNKNOWN. This case discriminates the rule from the superseded setup-error rule (round-26/contract.md:168-169, a setup error gives KILLERS_UNKNOWN exit 2 under contract.md:105), which the same inputs would meet. The earlyoom side holds no action line, so the sigterm and sigkill counts stay 0 (contract.md:85; cases.json c04 pins zero counts next to a nonzero one). The version line 'earlyoom 1.9.0' (main.c:161) is in scope, so earlyoom.version is 1.9.0 (contract.md:82; cases.json c19). No threshold line (main.c:414, main.c:416) is present, so earlyoom.thresholds is null (contract.md:91-92; cases.json c19). No 'dryrun mode enabled' line (main.c:295) is present, so earlyoom.dryrun is false (contract.md:89, :94). The show text says ActiveState=active, so earlyoom.state is active (contract.md:90). The oomd show text says ActiveState=inactive and the notice count is 0, so oomd.state is inactive and oomd.notices_this_boot is 0 (contract.md:95). earlyoom.grammar is not pinned: the contract fixes the two grammar values (contract.md:91) but not whether an in scope version line still verifies the grammar when the scope is incomplete for another reason.",
  "inputs": {
   "earlyoom_show": "LoadState=loaded\nActiveState=active\nUnitFileState=enabled\nActiveEnterTimestampMonotonic=31007000\n",
   "oomd_show": "LoadState=loaded\nActiveState=inactive\nUnitFileState=disabled\nActiveEnterTimestampMonotonic=0\n",
   "earlyoom_journal": [
    {"MESSAGE": "earlyoom 1.9.0", "__MONOTONIC_TIMESTAMP": "31007000"},
    {"MESSAGE": "escalating to SIGKILL after 5.000 seconds", "__MONOTONIC_TIMESTAMP": "not-a-timestamp"},
    {"MESSAGE": "escalating to SIGKILL after 9.500 seconds", "__MONOTONIC_TIMESTAMP": "31007500"}
   ],
   "oomd_notices": 0
  },
  "expect": {
   "verdict": "KILLER_ACTED", "exit": 1,
   "fields": {
    "earlyoom.state": "active", "earlyoom.version": "1.9.0",
    "earlyoom.thresholds": null, "earlyoom.scope_complete": false,
    "earlyoom.actions.sigterm": 0, "earlyoom.actions.sigkill": 0,
    "earlyoom.actions.escalations": 1, "earlyoom.actions.kill_failed": 0,
    "earlyoom.actions.low_memory_warnings": 0, "earlyoom.dryrun": false,
    "oomd.state": "inactive", "oomd.notices_this_boot": 0
   }
  }
 },
 {
  "id": "a2-10-oomd-notices-positive-malformed-records",
  "rule": "A2-10",
  "why": "Malformed timestamps with positive evidence from the other killer: the records are left uncounted, the scope is incomplete, and the positive evidence still stands. Two journal records carry non numeric timestamps ('not-a-number' and 'abc') and both carry an escalation line in the kill.c:318 shape 'escalating to SIGKILL after %.3f seconds'; the well formed version line at 41852500 is in scope (it is above ActiveEnterTimestampMonotonic 41852000, contract.md:78). round-27/contract.md:58 (round-26/contract.md:186-188) leaves such records uncounted and makes the scope incomplete, so earlyoom.scope_complete is false and earlyoom.actions.escalations is 0, not 2: both escalation shaped records are left uncounted and only counted lines reach the counts (contract.md:86; cases.json c15 pins one escalation for one counted line). Counts with an incomplete scope are printed as counts (round-26/contract.md:170, A1a, frozen c04). The earlyoom side therefore holds no positive evidence (contract.md:97), but oomd_notices is 2, a notice count greater than zero, which is positive evidence on its own; positive evidence stands even when the scope is incomplete (contract.md:97-98), so the verdict is KILLER_ACTED exit 1 and not KILLERS_UNKNOWN (cases.json c30 pins the same precedence for the oomd side). The version line 'earlyoom 1.9.0' (main.c:161) is in scope, so earlyoom.version is 1.9.0 (contract.md:82; cases.json c19). No threshold line (main.c:414, main.c:416) is present, so earlyoom.thresholds is null (contract.md:91-92; cases.json c19). No 'dryrun mode enabled' line (main.c:295) is present, so earlyoom.dryrun is false (contract.md:89, :94). The earlyoom show text says ActiveState=active, so earlyoom.state is active (contract.md:90). The oomd show text says ActiveState=active, so oomd.state is active, and the notice count is 2, so oomd.notices_this_boot is 2 (contract.md:95). earlyoom.grammar is not pinned: the contract fixes the two grammar values (contract.md:91) but not whether an in scope version line still verifies the grammar when the scope is incomplete for another reason.",
  "inputs": {
   "earlyoom_show": "LoadState=loaded\nActiveState=active\nUnitFileState=enabled\nActiveEnterTimestampMonotonic=41852000\n",
   "oomd_show": "LoadState=loaded\nActiveState=active\nUnitFileState=static\nActiveEnterTimestampMonotonic=13000000\n",
   "earlyoom_journal": [
    {"MESSAGE": "earlyoom 1.9.0", "__MONOTONIC_TIMESTAMP": "41852500"},
    {"MESSAGE": "escalating to SIGKILL after 2.500 seconds", "__MONOTONIC_TIMESTAMP": "not-a-number"},
    {"MESSAGE": "escalating to SIGKILL after 7.250 seconds", "__MONOTONIC_TIMESTAMP": "abc"}
   ],
   "oomd_notices": 2
  },
  "expect": {
   "verdict": "KILLER_ACTED", "exit": 1,
   "fields": {
    "earlyoom.state": "active", "earlyoom.version": "1.9.0",
    "earlyoom.thresholds": null, "earlyoom.scope_complete": false,
    "earlyoom.actions.sigterm": 0, "earlyoom.actions.sigkill": 0,
    "earlyoom.actions.escalations": 0, "earlyoom.actions.kill_failed": 0,
    "earlyoom.actions.low_memory_warnings": 0, "earlyoom.dryrun": false,
    "oomd.state": "active", "oomd.notices_this_boot": 2
   }
  }
 }
]
```

## Per-case derivation

Contract line references are to `.ufo/waves/round-26/contract.md` unless another file is named.
`r27` = `.ufo/waves/round-27/contract.md`.

### Case 1 — `a2-10-malformed-action-line-uncounted` (KILLERS_UNKNOWN, exit 2)

| Field | Value | Deciding line |
|---|---|---|
| verdict / exit | KILLERS_UNKNOWN / 2 | :99-100 (active earlyoom, `scope_complete` false, no positive evidence) |
| earlyoom.state | `active` | :90 (`ActiveState=active`; c01) |
| earlyoom.version | `1.9.0` | :82 (version grammar, main.c:161); in scope per :78; c19 |
| earlyoom.thresholds | `null` | :91-92 (`or null`; no threshold line, main.c:414/:416); c19 |
| earlyoom.scope_complete | `false` | r27:58 + :186-188 (malformed record ⇒ scope incomplete); :93 |
| earlyoom.actions.sigterm | `0` | :85 grammar; the action line is in the malformed record, which A2-10 leaves uncounted; :97; zero-count precedent c01, c04 |
| earlyoom.actions.sigkill | `0` | :85; no counted SIGKILL line; c01 |
| earlyoom.actions.escalations | `0` | :86; no counted escalation line; c01 |
| earlyoom.actions.kill_failed | `0` | :87; no counted `kill failed:` line (kill.c:654); c01 |
| earlyoom.actions.low_memory_warnings | `0` | :88; no counted low-memory line (main.c:519/:523); c01 |
| earlyoom.dryrun | `false` | :89 (no `dryrun mode enabled` line, main.c:295); :94; c19 |
| oomd.state | `inactive` | :95 (`ActiveState=inactive`); c01 |
| oomd.notices_this_boot | `0` | :95 (input `oomd_notices`); c01 |
| earlyoom.grammar | **not pinned** | :91 fixes the two values; the contract does not decide the value for "version line in scope, scope incomplete for another reason"; c04/c05 pin `unverified` only when no version line is in scope, c19 pins `verified-1.9.0` only with a complete scope |

### Case 2 — `a2-10-positive-evidence-elsewhere-stands` (KILLER_ACTED, exit 1)

| Field | Value | Deciding line |
|---|---|---|
| verdict / exit | KILLER_ACTED / 1 | :97-98 (in-scope escalation line is positive evidence; positive evidence stands even when the scope is incomplete) |
| earlyoom.state | `active` | :90; c01 |
| earlyoom.version | `1.9.0` | :82; in scope per :78; c19 |
| earlyoom.thresholds | `null` | :91-92; no threshold line; c19 |
| earlyoom.scope_complete | `false` | r27:58 + :186-188; :93 |
| earlyoom.actions.sigterm | `0` | :85; no counted action line (the malformed record's action line would be the only one, and A2-10 leaves it uncounted); c04 |
| earlyoom.actions.sigkill | `0` | :85; no counted SIGKILL line; c04 |
| earlyoom.actions.escalations | `1` | :86 (kill.c:318 shape) — one well-formed in-scope escalation at 31007500; the malformed one is uncounted (r27:58), so 1 not 2; c15 |
| earlyoom.actions.kill_failed | `0` | :87; no counted `kill failed:` line; c04 |
| earlyoom.actions.low_memory_warnings | `0` | :88; no counted low-memory line; c04 |
| earlyoom.dryrun | `false` | :89, :94; c19 |
| oomd.state | `inactive` | :95; c01 |
| oomd.notices_this_boot | `0` | :95; c01 |
| earlyoom.grammar | **not pinned** | same reason as case 1 |

### Case 3 — `a2-10-oomd-notices-positive-malformed-records` (KILLER_ACTED, exit 1)

| Field | Value | Deciding line |
|---|---|---|
| verdict / exit | KILLER_ACTED / 1 | :97-98 (`oomd_notices` > 0 is positive evidence on its own; stands even with an incomplete scope); c30 |
| earlyoom.state | `active` | :90; c01 |
| earlyoom.version | `1.9.0` | :82; in scope per :78 (41852500 ≥ 41852000); c19 |
| earlyoom.thresholds | `null` | :91-92; no threshold line; c19 |
| earlyoom.scope_complete | `false` | r27:58 + :186-188; :93 |
| earlyoom.actions.sigterm | `0` | :85; no counted action line; c04 |
| earlyoom.actions.sigkill | `0` | :85; no counted SIGKILL line; c04 |
| earlyoom.actions.escalations | `0` | :86 — both escalation-shaped records carry non-numeric timestamps and are left uncounted (r27:58), so 0 not 2; c15 |
| earlyoom.actions.kill_failed | `0` | :87; no counted `kill failed:` line; c04 |
| earlyoom.actions.low_memory_warnings | `0` | :88; no counted low-memory line; c04 |
| earlyoom.dryrun | `false` | :89, :94; c19 |
| oomd.state | `active` | :95 (`ActiveState=active`); c10 |
| oomd.notices_this_boot | `2` | :95 (input `oomd_notices`); c10 |
| earlyoom.grammar | **not pinned** | same reason as case 1 |

## Distinctness from the frozen round-26 cases

No input here repeats a frozen case. The frozen file's 32 cases contain no record with a non-numeric
`__MONOTONIC_TIMESTAMP` (grep `"__MONOTONIC_TIMESTAMP": "[^0-9]` over
`tools/fixtures/mori-oom-killers/cases.json` → no matches), so A2-10 is uncovered by the frozen file.
The three cases vary: oomd state (inactive/active), invocation boundary (version line exactly at the
boundary in cases 1-2, 500 µs above it in case 3), malformed-record count (1, 1, 2), malformed value
shapes (`not-a-number`, `not-a-timestamp`, `abc`), malformed message shape (action line in case 1,
escalation lines in cases 2-3), and the positive-evidence source (earlyoom escalation in case 2,
oomd notices in case 3). Pids and process names are invented (`7301`, `imaginary-harvester`); no uid,
cmdline, unit name or host value appears.

## Fields deliberately not pinned

- `earlyoom.grammar` in all three cases — the contract fixes the two legal values (:91) but not which
  applies when the version line is in scope while the scope is incomplete for a different reason; the
  frozen file pins `verified-1.9.0` only with a complete scope (c19) and `unverified` only when no
  version line is in scope (c04, c05).
- `earlyoom.actions` as a whole — all three cases have an active earlyoom, where the frozen
  c01/c04/c10/c15 pin the per-count members, so per-count members are pinned and the container is not.
- `earlyoom.process_group_lines`, `earlyoom.dryrun_send_lines`, `earlyoom.earlier_invocation_send_lines`
  — these belong to A2-03/A2-04/A2-06, not A2-10, and their value is not decided for these inputs.

## Validation performed

`python3 -c 'import json,sys;json.load(sys.stdin)'` on the scratch file → exit 0 (`JSON_VALID`).
A structural pass confirmed: 3 cases; keys exactly `{id, rule, why, inputs, expect}`; `rule` ==
`A2-10` on every case; ids match `a2-10-[a-z0-9-]+`; `inputs` keys exactly
`{earlyoom_show, oomd_show, earlyoom_journal, oomd_notices}`; every journal record has exactly
`{MESSAGE, __MONOTONIC_TIMESTAMP}`; `expect` keys exactly `{verdict, exit, fields}`;
`earlyoom.scope_complete` present in every `expect.fields`; and the pinned `sigterm`/`escalations`
counts equal a recomputation over the in-scope, numerically stamped records only. No self-test, counter
or tool invocation was run. This report is 100 % no-line-count-safe only if kept under 250 lines; the
figures at the end are within that budget.

## Risks and blockers

- None blocking. Residual risk: `earlyoom.grammar` is unpinned by design (see above); if the tool
  reports `unverified` for these shapes, the unpinned field absorbs the difference.
- Case 1 pins `earlyoom.actions.*` at zero on an incomplete scope. The frozen corpus prints counts
  under an incomplete scope (c04: `sigterm` 1, `sigkill` 0), and A1a (round-26/contract.md:170)
  records that counts under an incomplete scope are lower bounds printed as counts — so zeros are the
  printed value, and the null alternative would contradict c04's shape.
- The contract's privacy rule (:107) forbids printing message text, names, uids and cmdlines; my
  fixtures carry only invented names and pids, and the expected output fields contain no message text,
  matching c11/c12's treatment.
