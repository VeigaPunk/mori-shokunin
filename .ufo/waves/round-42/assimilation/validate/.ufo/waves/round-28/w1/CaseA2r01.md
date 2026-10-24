# Round 28 wave 1 — CaseA2r01: blind case writer for rule A2-01

Seat: MoriR28.CaseA2r01 (case writer, leaf, blind). Written 2026-10-22; upstream fetch access time
2026-10-22T18:00:13Z. Rule under test (round-27/contract.md:49; adopted round-26/contract.md:158-159): *a journald
`Suppressed N messages from earlyoom.service` line in scope sets `scope_complete` false.*

Three cases, all with `rule` = `A2-01`, ids `a2-01-<slug>` (printable ASCII, no newlines). The required pinned
field for A2-01 (`earlyoom.scope_complete`) is pinned in all three, and each pins a verdict and an exit code as
round-27/contract.md:64 requires. Distinctness: the suppressed line is inside the scope in two cases and one
microsecond before the scope start in the third; the suppressed counts differ (42, 17, 3); the oomd state differs
(inactive, inactive, active); the journal record counts differ (2, 2, 3); the timestamps differ from every frozen
round-26 case (19964362 / 19981126 / 19970000 / 19980000); the invented process name differs (`imaginary-burrower`
vs the frozen `imaginary-keeper` / `imaginary-indexer`).

## Blindness statement

I did **not** open, grep, cat or run `tools/mori-oom-killers.py` or any copy of it. I did **not** open
`.ufo/waves/round-26/evidence/`, `.ufo/waves/round-26/w1`, `.ufo/waves/round-26/w2`, `.ufo/waves/round-27/w1` or
`.ufo/waves/round-27/w2`. I ran no self-test and no counter.

Files I opened:

1. `.ufo/waves/round-27/contract.md` — read `:40-80`; a `grep` over the whole file for line numbers also returned
   lines 95-99, the C2-withdrawal paragraph. **Range overshoot, disclosed.** That paragraph says the round-27 C2
   claim was withdrawn before any case existed and that `count-c2.sh` stays committed; it discloses no tool
   behaviour.
2. `.ufo/waves/round-26/contract.md` — read whole (lines 1-190); permitted by the brief.
3. `tools/fixtures/mori-oom-killers/cases.json` — permitted file; read for the schema and the journal line shapes,
   and summarised the 32 frozen cases (id, verdict, exit, pinned fields, journal records) with a local `python3`
   script.
4. `/home/vgpnk/.omp/agent/RULES.md` — the operator tooling rules.
5. Upstream earlyoom v1.9.0 by `curl` (receipts below): `kill.c`, `main.c`, `msg.h`.

Directory listings (`ls -la`) of `.ufo/waves/round-28/` and `.ufo/waves/round-28/w1/` gave names and sizes only.

**Sibling round-28 report read, disclosed and assessed.** After the case file was finalised I ran `head -25` and
`tail -20` on `.ufo/waves/round-28/w1/CriticC2Design.md` to learn the report trailer convention, plus
`grep -n "Report:" *.md` over that directory and `tail -5 ConnSiblingOverlap.md`. `CriticC2Design.md` is a round-28
wave-1 report whose own head says it quotes the tool's behaviour and that writers who read it have tainted cases;
I disclose it rather than hide it. What I saw: the required-field map is right for 6 of 10 rules and wrong for
A2-07, A2-08, A2-09; a method note that the tool was loaded from git blobs and run on nine invented inputs; and
four recommendations to the L1 (corrected pins for the A2-07 / A2-08 / A2-09 / A2-10 writers, a freeze-batch audit,
a dated contract amendment, and the guard that no tool change may turn `KILLER_ACTED` into `KILLERS_QUIET`). None
of it concerns A2-01, and no expected value of mine changed afterwards: the case file was written and validated
before that read, and the only later edit was to this report. The L1 owns the taint judgement. The `grep -n
"Report:"` matched only the trailer line of `ReviewA2SpecVsTool.md`; I saw none of its content, and
`ConnSiblingOverlap.md`'s last five lines are about S150/S151 corpus rows, unrelated to the tool.

## Cases

```json
[
  {
    "id": "a2-01-suppressed-in-scope-active-quiet",
    "rule": "A2-01",
    "why": "Core A2-01 firing: an in-scope suppressed line makes the scope incomplete and, with no positive evidence, an active earlyoom then reads KILLERS_UNKNOWN exit 2. Rule A2-01 (round-27/contract.md:49) says a journald `Suppressed N messages from earlyoom.service` line in scope sets scope_complete false; the rule was adopted as A1b in round-26/contract.md:158-159. Journal record 1 is the invocation's version line `earlyoom 1.9.0` at 42000000, exactly ActiveEnterTimestampMonotonic=42000000, so it is inside the scope (round-26/contract.md:78-79: scope is the current invocation's lines in the current boot whose __MONOTONIC_TIMESTAMP is >= ActiveEnterTimestampMonotonic; the version line is main.c:161 `fprintf(stderr, \"earlyoom \" VERSION \"\\n\")` at earlyoom v1.9.0). Journal record 2, `Suppressed 42 messages from earlyoom.service` at 42001234, is also inside the scope, so scope_complete is false (round-26/contract.md:92-93 defines scope_complete as true only when the version line of the current invocation is inside the scope; A2-01 adds the in-scope suppressed line as a second disqualifier). No `sending SIG... to process` line and no escalation line is in scope and oomd_notices is 0, so there is no positive evidence (round-26/contract.md:97-98); an active earlyoom with scope_complete false is KILLERS_UNKNOWN exit 2 (round-26/contract.md:99-101). earlyoom.state is active because the show text carries ActiveState=active (round-26/contract.md:91; the same mapping frozen in cases.json c01/c04/c13). earlyoom.version is 1.9.0 because the version line is in scope (round-26/contract.md:82 with :78-79). earlyoom.dryrun is false because no `dryrun mode enabled` line is in scope and the output spec gives dryrun no null alternative (round-26/contract.md:89 and :94; frozen cases.json c01/c19). oomd.state inactive and oomd.notices_this_boot 0 follow the oomd show text and the oomd_notices input (round-26/contract.md:95; frozen cases.json c01/c06). Deliberately not pinned: earlyoom.grammar, because round-26/contract.md:91 lists the two grammar values but states no condition for choosing between them, and the two readings that fit the frozen set (verified when the in-scope version line reads 1.9.0, versus verified only for a complete scope) disagree exactly for this input; earlyoom.actions, because frozen case c05 declines to pin the counts of an active reader whose scope is incomplete; earlyoom.thresholds, because round-26/contract.md:92 gives thresholds a null alternative and frozen case c04, also an incomplete scope, leaves thresholds unpinned; earlyoom.earlier_invocation_send_lines, because the contract does not decide its value for a boot with no earlier invocation.",
    "inputs": {
      "earlyoom_show": "LoadState=loaded\nActiveState=active\nUnitFileState=enabled\nActiveEnterTimestampMonotonic=42000000\n",
      "oomd_show": "LoadState=loaded\nActiveState=inactive\nUnitFileState=disabled\nActiveEnterTimestampMonotonic=0\n",
      "earlyoom_journal": [
        {"MESSAGE": "earlyoom 1.9.0", "__MONOTONIC_TIMESTAMP": "42000000"},
        {"MESSAGE": "Suppressed 42 messages from earlyoom.service", "__MONOTONIC_TIMESTAMP": "42001234"}
      ],
      "oomd_notices": 0
    },
    "expect": {
      "verdict": "KILLERS_UNKNOWN",
      "exit": 2,
      "fields": {
        "earlyoom.state": "active", "earlyoom.version": "1.9.0", "earlyoom.scope_complete": false, "earlyoom.dryrun": false, "oomd.state": "inactive", "oomd.notices_this_boot": 0
      }
    }
  },
  {
    "id": "a2-01-suppressed-before-scope-start",
    "rule": "A2-01",
    "why": "A2-01 carries the qualifier 'in scope', so a suppressed line from before the current invocation starts must not fire the rule. The journal holds `Suppressed 17 messages from earlyoom.service` at 73499999, one microsecond before ActiveEnterTimestampMonotonic=73500000, and the version line `earlyoom 1.9.0` at 73500000 (main.c:161 at earlyoom v1.9.0). Scope is the current invocation's lines in the current boot whose __MONOTONIC_TIMESTAMP is >= ActiveEnterTimestampMonotonic (round-26/contract.md:78-79), so the suppressed line at 73499999 is outside the scope; rule A2-01 (round-27/contract.md:49; round-26/contract.md:158-159) fires only on a suppressed line in scope, so the version line of the current invocation, which is inside the scope, leaves scope_complete true (round-26/contract.md:92-93). Every other field pinned here is the same pairing that frozen case c19 pins for a version-line-only journal: version 1.9.0 and the verified 1.9.0 grammar (round-26/contract.md:82 and :91), thresholds null and the dry-run flag unset because no threshold line and no `dryrun mode enabled` line is in scope (round-26/contract.md:89 and :92). With no action line in scope and oomd_notices 0 there is no positive evidence (round-26/contract.md:97-98) and nothing forces the unknown verdict (round-26/contract.md:99-101), so the verdict is KILLERS_QUIET exit 0 (round-26/contract.md:102-104). oomd.state inactive and oomd.notices_this_boot 0 follow the oomd show text and the oomd_notices input (round-26/contract.md:95; frozen cases.json c19). Deliberately not pinned: earlyoom.actions, because round-26/contract.md:102 reserves actions null for an inactive or absent killer and frozen case c19 also leaves the counts of an action-free journal unpinned; earlyoom.earlier_invocation_send_lines, because the contract does not decide its value for a boot with no earlier invocation, and a suppressed line is neither a send line nor an escalation line (round-26/contract.md:176).",
    "inputs": {
      "earlyoom_show": "LoadState=loaded\nActiveState=active\nUnitFileState=enabled\nActiveEnterTimestampMonotonic=73500000\n",
      "oomd_show": "LoadState=loaded\nActiveState=inactive\nUnitFileState=disabled\nActiveEnterTimestampMonotonic=0\n",
      "earlyoom_journal": [
        {"MESSAGE": "Suppressed 17 messages from earlyoom.service", "__MONOTONIC_TIMESTAMP": "73499999"},
        {"MESSAGE": "earlyoom 1.9.0", "__MONOTONIC_TIMESTAMP": "73500000"}
      ],
      "oomd_notices": 0
    },
    "expect": {
      "verdict": "KILLERS_QUIET",
      "exit": 0,
      "fields": {
        "earlyoom.state": "active", "earlyoom.version": "1.9.0", "earlyoom.grammar": "verified-1.9.0", "earlyoom.thresholds": null, "earlyoom.scope_complete": true, "earlyoom.dryrun": false, "oomd.state": "inactive", "oomd.notices_this_boot": 0
      }
    }
  },
  {
    "id": "a2-01-suppressed-in-scope-with-action",
    "rule": "A2-01",
    "why": "A2-01 next to positive evidence: the in-scope suppressed line still makes the scope incomplete, but the positive evidence stands and the verdict does not fall back to unknown. The version line `earlyoom 1.9.0` is at 88000000, exactly ActiveEnterTimestampMonotonic=88000000, and `Suppressed 3 messages from earlyoom.service` at 88000050 is later, so both are inside the scope (round-26/contract.md:78-79); rule A2-01 (round-27/contract.md:49; round-26/contract.md:158-159) then sets scope_complete false (round-26/contract.md:92-93). The third record, `sending SIGTERM to process 5151 \"imaginary-burrower\"` at 88000100, is the kill.c:627 form `sending %s to process %d ...` with only the invented process name kept and no uid and no command line, so it is one in-scope SIGTERM action (round-26/contract.md:85) and it is positive evidence that stands even when the scope is incomplete (round-26/contract.md:97-98); hence KILLER_ACTED exit 1 and not the unknown verdict of round-26/contract.md:99-101. The action counts are printed as counts even for an incomplete scope (round-26/contract.md:93-94; the same pairing frozen in cases.json c04, which pins actions.sigterm 1 and actions.sigkill 0 with scope_complete false), so sigterm is 1 and sigkill is 0. earlyoom.state is active because the show text carries ActiveState=active (round-26/contract.md:91). earlyoom.version is 1.9.0 because the version line is in scope (round-26/contract.md:82 with :78-79). earlyoom.dryrun is false because no `dryrun mode enabled` line is in scope and the output spec gives dryrun no null alternative (round-26/contract.md:89 and :94). oomd is active but reports no notice this boot, so oomd.state is active and oomd.notices_this_boot is 0 (round-26/contract.md:95; frozen cases.json c10/c28), and oomd contributes no positive evidence, so the verdict rests on the earlyoom action line alone. Deliberately not pinned: earlyoom.grammar, because round-26/contract.md:91 states no condition for choosing between verified-1.9.0 and unverified and the readings that fit the frozen set disagree for an incomplete scope; earlyoom.thresholds, because round-26/contract.md:92 gives thresholds a null alternative and frozen case c04 leaves thresholds unpinned; earlyoom.earlier_invocation_send_lines, because the contract does not decide its value for a boot with no earlier invocation.",
    "inputs": {
      "earlyoom_show": "LoadState=loaded\nActiveState=active\nUnitFileState=enabled\nActiveEnterTimestampMonotonic=88000000\n",
      "oomd_show": "LoadState=loaded\nActiveState=active\nUnitFileState=static\nActiveEnterTimestampMonotonic=12345678\n",
      "earlyoom_journal": [
        {"MESSAGE": "earlyoom 1.9.0", "__MONOTONIC_TIMESTAMP": "88000000"},
        {"MESSAGE": "Suppressed 3 messages from earlyoom.service", "__MONOTONIC_TIMESTAMP": "88000050"},
        {"MESSAGE": "sending SIGTERM to process 5151 \"imaginary-burrower\"", "__MONOTONIC_TIMESTAMP": "88000100"}
      ],
      "oomd_notices": 0
    },
    "expect": {
      "verdict": "KILLER_ACTED",
      "exit": 1,
      "fields": {
        "earlyoom.state": "active", "earlyoom.version": "1.9.0", "earlyoom.scope_complete": false, "earlyoom.actions.sigterm": 1, "earlyoom.actions.sigkill": 0, "earlyoom.dryrun": false, "oomd.state": "active", "oomd.notices_this_boot": 0
      }
    }
  }
]
```

## Derivation tables

Contract paths are relative to `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/`. "frozen cNN" cites
`round-26/tools/fixtures/mori-oom-killers/cases.json`, read for schema and line shapes only. Case 1 is
`a2-01-suppressed-in-scope-active-quiet`, case 2 `a2-01-suppressed-before-scope-start`, case 3
`a2-01-suppressed-in-scope-with-action`.

| Case | Field | Expected | Deciding line |
|---|---|---|---|
| 1 | verdict | KILLERS_UNKNOWN | round-26/contract.md:99-101 (active, scope_complete false, no positive evidence) |
| 1 | exit | 2 | round-26/contract.md:99 (KILLERS_UNKNOWN, exit 2) |
| 1 | earlyoom.scope_complete | false | round-27/contract.md:49 + round-26/contract.md:158-159, on the in-scope line at 42001234 |
| 1 | earlyoom.state | active | round-26/contract.md:91 (ActiveState=active); frozen c01/c04/c13 |
| 1 | earlyoom.version | 1.9.0 | round-26/contract.md:82 with :78-79 (version line in scope) |
| 1 | earlyoom.dryrun | false | round-26/contract.md:89 + :94 (no dryrun line; no null alternative); frozen c01/c19 |
| 1 | oomd.state | inactive | round-26/contract.md:95 (ActiveState=inactive); frozen c01/c06 |
| 1 | oomd.notices_this_boot | 0 | round-26/contract.md:95 + input oomd_notices=0; frozen c01/c06 |
| 2 | verdict | KILLERS_QUIET | round-26/contract.md:102-104 (no positive evidence, scope complete) |
| 2 | exit | 0 | round-26/contract.md:102 (KILLERS_QUIET, exit 0) |
| 2 | earlyoom.scope_complete | true | round-26/contract.md:92-93 (version line at 73500000 in scope) + :78-79 (suppressed line at 73499999 out of scope, so A2-01 does not fire) |
| 2 | earlyoom.state | active | round-26/contract.md:91; frozen c19 |
| 2 | earlyoom.version | 1.9.0 | round-26/contract.md:82 with :78-79; frozen c19 |
| 2 | earlyoom.grammar | verified-1.9.0 | round-26/contract.md:91 + :82 (version line in scope reads 1.9.0); frozen c19 |
| 2 | earlyoom.thresholds | null | round-26/contract.md:92 (thresholds or null; no threshold line in scope); frozen c19 |
| 2 | earlyoom.dryrun | false | round-26/contract.md:89 + :94; frozen c19 |
| 2 | oomd.state | inactive | round-26/contract.md:95; frozen c19 |
| 2 | oomd.notices_this_boot | 0 | round-26/contract.md:95 + input oomd_notices=0; frozen c19 |
| 3 | verdict | KILLER_ACTED | round-26/contract.md:97-98 (in-scope `sending SIGTERM to process` line; positive evidence stands even when the scope is incomplete) |
| 3 | exit | 1 | round-26/contract.md:97 (KILLER_ACTED, exit 1) |
| 3 | earlyoom.scope_complete | false | round-27/contract.md:49 + round-26/contract.md:158-159, on the in-scope line at 88000050 |
| 3 | earlyoom.state | active | round-26/contract.md:91 |
| 3 | earlyoom.version | 1.9.0 | round-26/contract.md:82 with :78-79 |
| 3 | earlyoom.actions.sigterm | 1 | round-26/contract.md:85 (one action each) + :93-94 (counts printed even for an incomplete scope); frozen c04 |
| 3 | earlyoom.actions.sigkill | 0 | round-26/contract.md:85 (no SIGKILL send line); frozen c04 |
| 3 | earlyoom.dryrun | false | round-26/contract.md:89 + :94 |
| 3 | oomd.state | active | round-26/contract.md:95 (ActiveState=active); frozen c10/c28 |
| 3 | oomd.notices_this_boot | 0 | round-26/contract.md:95 + input oomd_notices=0; frozen c28 |

### Fields deliberately not pinned, and why

- `earlyoom.grammar` in cases 1 and 3 (incomplete scope): round-26/contract.md:91 lists the two values but states no
  condition for choosing between them; "verified when the in-scope version line reads 1.9.0" and "verified only for a
  complete scope" both fit the frozen set (c04: incomplete scope, grammar unverified; c09: complete scope, grammar
  unverified) and they disagree exactly here. Both cases' verdict and exit are the same under either reading, so the
  ambiguity does not weaken the rule test.
- `earlyoom.actions` in cases 1 and 2: round-26/contract.md:102 reserves `actions` null for an inactive or absent
  killer; frozen c05 declines to pin the counts of an active reader with an incomplete scope, and frozen c19 leaves
  the counts of an action-free journal unpinned.
- `earlyoom.thresholds` in cases 1 and 3: round-26/contract.md:92 allows null; frozen c04, an incomplete scope,
  leaves thresholds unpinned.
- `earlyoom.earlier_invocation_send_lines` in all three: round-26/contract.md:175-179 introduces the field but does
  not decide its value for a boot with no earlier invocation, and a suppressed line is neither a send line nor an
  escalation line, so it does not feed that counter.
- `earlyoom.process_group_lines`, `earlyoom.dryrun_send_lines`: other rules' fields; round-26/contract.md:93-95
  gives no value for them on these inputs.

All three keep earlyoom active on purpose: a non-active earlyoom would need `ActiveEnterTimestampMonotonic` = 0 or
missing, which round-26/contract.md:173-174 makes an unbounded invocation with `scope_complete` false for a
different reason (rule A2-05), contaminating an A2-01 case. The varied state is the oomd unit's.

## Source receipts

Fetched with `curl -fsSL` on 2026-10-22, access time 2026-10-22T18:00:13Z, into
`/fast/scratch/hyaku/mori-r28/MoriR28.CaseA2r01/src/`. Quotes are verbatim, at most 25 words, with line numbers.

| File | URL | sha256 | bytes |
|---|---|---|---|
| kill.c | https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/kill.c | b32e0fad65e298235102f98aff37e02c94400b544d454cb57192ae697b100bf3 | 21169 |
| main.c | https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/main.c | 08656b0bc90c85f23738661456b25c97af908bc5e2cfea78e0a69697b5f9d0e4 | 21053 |
| msg.h | https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/msg.h | e36604984a916fb00a624c27c73034bcd87d7d6facff9b290a6a561ee58de56c | 1027 |

- `main.c:161` — `fprintf(stderr, "earlyoom " VERSION "\n");`
- `main.c:295` — `warn("dryrun mode enabled, will not kill anything\n");`
- `main.c:414` — `fprintf(stderr, "sending SIGTERM when mem avail <= " PRIPCT " and swap free <= " PRIPCT ",\n",`
- `main.c:416` — `fprintf(stderr, "        SIGKILL when mem avail <= " PRIPCT " and swap free <= " PRIPCT "\n",`
- `kill.c:318` — `warn("escalating to SIGKILL after %.3f seconds\n", secs);`
- `kill.c:627` — `sending %s to process %d uid %d "%s":`
- `kill.c:654` — `warn("kill failed: %s\n", strerror(saved_errno));`
- `msg.h:10` — `#define PRIPCT "%5.2lf%%"`

These confirm the shapes round-26/contract.md:82-89 cites (version line, dryrun line, both threshold lines,
escalation, kill failed, the `sending %s to process %d uid %d "%s"` send line) and that the version line is
`earlyoom <version>` with no leading whitespace. The journald `Suppressed N messages from earlyoom.service` line is
not an earlyoom upstream string; its shape is fixed by the rule text (round-27/contract.md:49), used verbatim with
three different counts.

## Validation

In the scratch dir `/fast/scratch/hyaku/mori-r28/MoriR28.CaseA2r01/`, `cases-a2-01.json` (the exact bytes of the
fenced array above) passes `python3 -c 'import json,sys;json.load(sys.stdin)'` → no output, exit 0. A local
`python3` assertion pass checked for each case: keys exactly `{id, rule, why, inputs, expect}`; `rule` == "A2-01";
input keys exactly `{earlyoom_show, oomd_show, earlyoom_journal, oomd_notices}`; expect keys exactly
`{verdict, exit, fields}`; `earlyoom.scope_complete` present in `fields`; id ASCII, newline-free, prefixed
`a2-01-`; every journal record keys exactly `{MESSAGE, __MONOTONIC_TIMESTAMP}` with a numeric timestamp. All
assertions passed. The fenced block was re-extracted from this report and compared canonically with the scratch
file: equal. I did not run the tool, so I cannot report a tool pass.

## Risks and blockers

1. **Taint disclosure.** I read part of the sibling round-28 report `CriticC2Design.md` after finalising my case
   file; see above. The L1 owns the taint judgement.
2. **`earlyoom.version` in the two incomplete-scope cases** rests on the reading that an in-scope version line
   yields the version string whatever the scope completeness (round-26/contract.md:82 + :78-79). If the tool
   instead withholds the version when the scope is incomplete, these two pins would fail and the L1 would have to
   drop them or change the tool; the contract does not decide that case. The required field, the verdict and the
   exit are unaffected.
3. **Case 2 depends on the rule's `in scope` qualifier being implemented as a scope filter** rather than a scan of
   the whole boot journal. The rule text says "in scope" twice (round-27/contract.md:49, round-26/contract.md:158),
   so this is the contract-derived reading, but it is the one case that could force a tool change if the tool scans
   the whole journal.
4. No blocker on scope: the three cases are complete, distinct, and each pins the required field plus a verdict and
   an exit code.

## Files changed

- `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-28/w1/CaseA2r01.md` (this report).
- Scratch only, outside the lane: `/fast/scratch/hyaku/mori-r28/MoriR28.CaseA2r01/cases-a2-01.json` (the case
  bytes) and `/fast/scratch/hyaku/mori-r28/MoriR28.CaseA2r01/src/{kill.c,main.c,msg.h}` (upstream fetch).

## Tooling

No tool installed or updated; no pacman transaction (all pacman transactions are paused host-wide). Tools used:
`curl 8.23.0` (upstream fetch, official GitHub raw URL), `python3 3.14.8` (JSON validation and local assertions),
`sha256sum 0.8.0` (source hashes), `grep` (contract line numbers, via the harness search tool). No subagent, no
background job, no `jj` command, no `git` write command; the only repo write was this report. No host unit, no
journal read on this host, no `systemctl` call, no OMP settings value, session id or session-store path read or
copied; every value in the cases is invented.

Report: `.ufo/waves/round-28/w1/CaseA2r01.md`
