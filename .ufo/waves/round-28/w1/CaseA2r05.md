# CaseA2r05 — blind case writer for round-28 C2, rule A2-05

Seat: `MoriR28.CaseA2r05` (executor, leaf). Wave: round-28, wave 1. L1 / integration owner: `MoriR28`.
Rule under test (round-27 `contract.md:53`): **A2-05** — "`ActiveEnterTimestampMonotonic` missing or `0` leaves the
invocation unbounded: `scope_complete` false". Required pinned field per the wave context: `earlyoom.scope_complete`.

Deliverable: 3 frozen blind cases for rule A2-05, contributed to `tools/fixtures/mori-oom-killers/cases-a2.json`
(the L1 assembles the file; I wrote only this report plus my scratch dir).

## Files changed

`.ufo/waves/round-28/w1/CaseA2r05.md` (this report — the only file written in the lane), plus scratch
`/fast/scratch/hyaku/mori-r28/MoriR28.CaseA2r05/cases-a2-05.json` (validated copy of the case array) and
`/fast/scratch/hyaku/mori-r28/MoriR28.CaseA2r05/upstream/{kill.c,main.c,msg.h}` (upstream v1.9.0 bytes fetched by
curl). No lane file was edited other than this report. No git/jj command was run in the lane; no commit, no ref update.

## The cases (JSON array, ready to append to `cases-a2.json`)

```json
[
  {
    "id": "a2-05-monotonic-zero-active-quiet",
    "rule": "A2-05",
    "why": "A2-05 unbounded invocation, active unit, quiet boot. The show text carries ActiveEnterTimestampMonotonic=0, and round-26 contract.md:173-174 (Amendment A2, unbounded invocation, adopted) states that a missing or 0 ActiveEnterTimestampMonotonic leaves the invocation unbounded so scope_complete is false; round-27 contract.md:53 states the same rule id A2-05. earlyoom.scope_complete is therefore false here even though the journal holds a version line (main.c:161 form 'earlyoom 1.9.0', grammar rule contract.md:82), because A2-05 overrides the former 'a version line alone set it true' behaviour. earlyoom.state is 'active' because the show text has ActiveState=active and the state vocabulary is contract.md:90-91. No positive evidence exists: the journal carries no 'sending SIGTERM to process ' or 'sending SIGKILL to process ' line (contract.md:85) and no 'escalating to SIGKILL after ' line (contract.md:86), and oomd_notices is 0, so contract.md:97-98 finds no positive evidence. No read is null and the show text has ActiveState, but the earlyoom is active with scope_complete false, so contract.md:99-101 makes the verdict KILLERS_UNKNOWN with exit 2. oomd.state is 'inactive' (the oomd show text has ActiveState=inactive, output spec contract.md:95) and oomd.notices_this_boot is 0 (the input count). earlyoom.dryrun is false because the journal contains no 'dryrun mode enabled' line (contract.md:89). Not pinned, because contract.md:78-79 scopes lines by the ActiveEnterTimestampMonotonic lower bound that contract.md:173-174 leaves unknown here, so the contract does not decide earlyoom.version, earlyoom.grammar, earlyoom.thresholds.* or earlyoom.actions.* for this input (the frozen c05 pins none of them either).",
    "inputs": {
      "earlyoom_show": "LoadState=loaded\nActiveState=active\nUnitFileState=enabled\nActiveEnterTimestampMonotonic=0\n",
      "oomd_show": "LoadState=loaded\nActiveState=inactive\nUnitFileState=disabled\nActiveEnterTimestampMonotonic=0\n",
      "earlyoom_journal": [
        {
          "MESSAGE": "earlyoom 1.9.0",
          "__MONOTONIC_TIMESTAMP": "55821000"
        },
        {
          "MESSAGE": "sending SIGTERM when mem avail <=  8.00% and swap free <= 12.00%,",
          "__MONOTONIC_TIMESTAMP": "55821005"
        },
        {
          "MESSAGE": "        SIGKILL when mem avail <=  4.00% and swap free <=  6.00%",
          "__MONOTONIC_TIMESTAMP": "55821005"
        }
      ],
      "oomd_notices": 0
    },
    "expect": {
      "verdict": "KILLERS_UNKNOWN",
      "exit": 2,
      "fields": {
        "earlyoom.state": "active",
        "earlyoom.scope_complete": false,
        "earlyoom.dryrun": false,
        "oomd.state": "inactive",
        "oomd.notices_this_boot": 0
      }
    }
  },
  {
    "id": "a2-05-monotonic-missing-active-oomd-notices",
    "rule": "A2-05",
    "why": "A2-05 unbounded invocation caused by a missing property, with positive evidence that stands anyway. The show text has no ActiveEnterTimestampMonotonic line at all, which round-26 contract.md:173-174 puts under the same rule as the value 0 ('missing or 0 leaves the invocation unbounded'), so earlyoom.scope_complete is false (round-27 contract.md:53 names the same rule id A2-05). earlyoom.state is 'active' because the show text has ActiveState=active (contract.md:90-91). The oomd show text has ActiveState=active, so oomd.state is 'active', and oomd_notices is 3; contract.md:97-98 counts oomd_notices > 0 as positive evidence and states that positive evidence stands even when the scope is incomplete, so the verdict is KILLER_ACTED with exit 1. earlyoom.dryrun is false because the journal contains no 'dryrun mode enabled' line (contract.md:89). Not pinned: the journal's 'escalating to SIGKILL after 5.000 seconds' line (kill.c:318 form, grammar rule contract.md:86) would be counted as an action only if it lies in scope, and contract.md:78-79 with :173-174 do not fix the scope when the invocation start is unknown, so earlyoom.actions.escalations, earlyoom.actions.sigterm, earlyoom.actions.sigkill, earlyoom.version, earlyoom.grammar and earlyoom.thresholds.* are not decided for this input; the verdict above does not depend on that choice because the oomd notice count alone is positive evidence.",
    "inputs": {
      "earlyoom_show": "LoadState=loaded\nActiveState=active\nUnitFileState=enabled\n",
      "oomd_show": "LoadState=loaded\nActiveState=active\nUnitFileState=static\nActiveEnterTimestampMonotonic=12345678\n",
      "earlyoom_journal": [
        {
          "MESSAGE": "earlyoom 1.9.0",
          "__MONOTONIC_TIMESTAMP": "48200100"
        },
        {
          "MESSAGE": "escalating to SIGKILL after 5.000 seconds",
          "__MONOTONIC_TIMESTAMP": "48200900"
        }
      ],
      "oomd_notices": 3
    },
    "expect": {
      "verdict": "KILLER_ACTED",
      "exit": 1,
      "fields": {
        "earlyoom.state": "active",
        "earlyoom.scope_complete": false,
        "earlyoom.dryrun": false,
        "oomd.state": "active",
        "oomd.notices_this_boot": 3
      }
    }
  },
  {
    "id": "a2-05-monotonic-zero-inactive-quiet",
    "rule": "A2-05",
    "why": "A2-05 unbounded invocation on a unit that is not active. The show text carries ActiveEnterTimestampMonotonic=0, which round-26 contract.md:173-174 (Amendment A2, unbounded invocation) puts under the A2-05 rule (round-27 contract.md:53): the invocation has no known start, so scope_complete is false (contract.md:92-93 defines scope_complete as true only when the version line of the current invocation is inside the scope, and an inactive unit has no current invocation; AETM=0 also fails the rule outright). ActiveState=inactive makes earlyoom.state 'inactive' (contract.md:90-91), and contract.md:102-103 reserves actions null for an inactive or absent killer ('An inactive or absent killer reports actions: null'), so earlyoom.actions is null and no zero counts are printed. The journal holds only the version line of the boot's earlier run (main.c:161 form, contract.md:82) and no 'sending SIGTERM to process ' or 'sending SIGKILL to process ' line (contract.md:85) and no 'escalating to SIGKILL after ' line (contract.md:86), and oomd_notices is 0, so contract.md:97-98 finds no positive evidence. None of the contract.md:99-101 KILLERS_UNKNOWN triggers applies: no read is null, the show text has ActiveState, and the earlyoom is not active, so contract.md:102-104 gives KILLERS_QUIET with exit 0. oomd.state is 'inactive' (the oomd show text has ActiveState=inactive, contract.md:95) and oomd.notices_this_boot is 0 (the input count). Not pinned: contract.md:78-79 with :173-174 do not fix which boot lines lie in scope for an unbounded invocation, so earlyoom.version, earlyoom.grammar, earlyoom.thresholds.*, earlyoom.earlier_invocation_send_lines and earlyoom.dryrun are not decided for this input (the frozen c06 pins none of them either).",
    "inputs": {
      "earlyoom_show": "LoadState=loaded\nActiveState=inactive\nUnitFileState=disabled\nActiveEnterTimestampMonotonic=0\n",
      "oomd_show": "LoadState=loaded\nActiveState=inactive\nUnitFileState=disabled\nActiveEnterTimestampMonotonic=0\n",
      "earlyoom_journal": [
        {
          "MESSAGE": "earlyoom 1.9.0",
          "__MONOTONIC_TIMESTAMP": "31600400"
        }
      ],
      "oomd_notices": 0
    },
    "expect": {
      "verdict": "KILLERS_QUIET",
      "exit": 0,
      "fields": {
        "earlyoom.state": "inactive",
        "earlyoom.scope_complete": false,
        "earlyoom.actions": null,
        "oomd.state": "inactive",
        "oomd.notices_this_boot": 0
      }
    }
  }
]
```

## Per-case derivation

### `a2-05-monotonic-zero-active-quiet` — verdict `KILLERS_UNKNOWN`, exit 2

| Field | Value | Contract line that decides it |
|---|---|---|
| `earlyoom.state` | `active` | r26 `contract.md:90-91` (state vocabulary) + input `ActiveState=active` |
| `earlyoom.scope_complete` | `false` | r26 `contract.md:173-174` (A2, unbounded invocation: missing or 0 ⇒ false); r27 `contract.md:53` (rule id A2-05); r26 `contract.md:92-93` (true only when the version line of the current invocation is in scope) |
| `earlyoom.dryrun` | `false` | r26 `contract.md:89` (dry-run flag only from `dryrun mode enabled`; no such line in the journal) |
| `oomd.state` | `inactive` | r26 `contract.md:95` (output spec) + input oomd `ActiveState=inactive` |
| `oomd.notices_this_boot` | `0` | input count; r26 `contract.md:95` |
| verdict / exit | `KILLERS_UNKNOWN` / 2 | r26 `contract.md:99-101` (no positive evidence, but earlyoom active with `scope_complete` false) with `:97-98` (no send/escalation line, `oomd_notices` 0 ⇒ no positive evidence) |

### `a2-05-monotonic-missing-active-oomd-notices` — verdict `KILLER_ACTED`, exit 1

| Field | Value | Contract line that decides it |
|---|---|---|
| `earlyoom.state` | `active` | r26 `contract.md:90-91` + input `ActiveState=active` |
| `earlyoom.scope_complete` | `false` | r26 `contract.md:173-174` ("missing or 0"); r27 `contract.md:53` |
| `earlyoom.dryrun` | `false` | r26 `contract.md:89` (no `dryrun mode enabled` line) |
| `oomd.state` | `active` | r26 `contract.md:95` + input oomd `ActiveState=active` |
| `oomd.notices_this_boot` | `3` | input count; r26 `contract.md:95` |
| verdict / exit | `KILLER_ACTED` / 1 | r26 `contract.md:97-98` (`oomd_notices` > 0 is positive evidence; "positive evidence stands even when the scope is incomplete") |

### `a2-05-monotonic-zero-inactive-quiet` — verdict `KILLERS_QUIET`, exit 0

| Field | Value | Contract line that decides it |
|---|---|---|
| `earlyoom.state` | `inactive` | r26 `contract.md:90-91` + input `ActiveState=inactive` |
| `earlyoom.scope_complete` | `false` | r26 `contract.md:92-93` (true only when the version line of the *current* invocation is in scope; an inactive unit has none) plus `:173-174` (AETM 0 ⇒ unbounded ⇒ false) |
| `earlyoom.actions` | `null` | r26 `contract.md:102-103` ("An inactive or absent killer reports `actions: null`") |
| `oomd.state` | `inactive` | r26 `contract.md:95` + input oomd `ActiveState=inactive` |
| `oomd.notices_this_boot` | `0` | input count; r26 `contract.md:95` |
| verdict / exit | `KILLERS_QUIET` / 0 | r26 `contract.md:102-104` ("otherwise"); the `:99-101` unknown trigger is scoped to an *active* earlyoom, and `:97-98` finds no positive evidence (no send/escalation line, `oomd_notices` 0) |

### Fields deliberately not pinned, and why

| Field | Why not decided by the contract |
|---|---|
| `earlyoom.version`, `earlyoom.grammar` | r26 `contract.md:78-79` scopes lines by the `ActiveEnterTimestampMonotonic` lower bound; with the bound missing or 0 (`:173-174`) the contract does not say whether a boot version line counts as the current invocation's line, so it does not decide `verified-1.9.0` vs `unverified`. Frozen `c05` (same situation) pins neither. |
| `earlyoom.thresholds.*` | Same scope question: the two threshold lines are in scope only under one reading of the unbounded scope. |
| `earlyoom.actions.sigterm` / `.sigkill` / `.escalations` / `.kill_failed` / `.low_memory_warnings` | Counts are counts of in-scope lines; in scope depends on the unbounded scope. Frozen `c04` pins action counts only where an in-scope action exists under a *known* bound. |
| `earlyoom.earlier_invocation_send_lines` | Only the A2-06 rule (`r27 contract.md:54`) introduces it, and its count needs a decided scope; the two send-less journals here make any count 0, but the field's presence for a non-active unit is not decided by `:95`. |
| `earlyoom.dryrun` in case 3 | The rule at r26 `contract.md:89` decides the flag from a `dryrun mode enabled` line; with an unbounded scope it is not decided whether the flag is reported for a non-active unit (frozen `c06` pins no `dryrun` either). |

## Distinctness from the frozen round-26 cases

- Timestamps are invented and new: `55821000`/`55821005`, `48200100`/`48200900`, `31600400` — none of the frozen
  `19964362`/`19964361`/`19970000`/`19981126`/`19981234`/`19983943` values.
- Thresholds are invented and non-host: `8.00/12.00/4.00/6.00` (host case `c01` uses `10.00/10.00/5.00/5.00`); the
  `PRIPCT` rendering (`"%5.2lf%%"`, `msg.h:10`) is reproduced exactly, pad space (` 8.00%`, ` 4.00%`) and the
  eight-space SIGKILL indent (`main.c:416`) included.
- Trigger variants: AETM present-and-`0` (cases 1, 3), AETM property absent (case 2). State variants: earlyoom
  `active` (1, 2) / `inactive` (3); oomd `inactive` (1, 3) / `active` (2); `oomd_notices` 0 vs 3.
- Verdict variants: `KILLERS_UNKNOWN` (2), `KILLER_ACTED` (1), `KILLERS_QUIET` (0) — all three exit codes appear. No
  case copies a round-26 shape (`c01`/`c19` bounded scope, `c02`/`c03` boundary at `19964362`, `c04`/`c05` version
  line one microsecond before a known bound, `c06`/`c07` empty journal).
- Privacy: the journal texts carry no pid, uid, command line or process name — only the upstream `earlyoom 1.9.0`
  version line, the two threshold lines and the upstream escalation line.

## Evidence actually observed

- JSON validated with `python3 -c 'import json,sys;json.load(sys.stdin)' < cases-a2-05.json` → exit 0 (`JSON_OK`) in
  `/fast/scratch/hyaku/mori-r28/MoriR28.CaseA2r05/`; a structural check confirmed unique printable ASCII ids, the
  keys `id/why/inputs/expect/rule`, `rule == "A2-05"` on every case, the four input keys, journal records with only
  `MESSAGE` and a string `__MONOTONIC_TIMESTAMP`, `expect` with `verdict/exit/fields`, and `earlyoom.scope_complete`
  pinned in all three cases.
- Upstream bytes fetched by `curl` at `2026-10-22T17:59:56Z` (sha256 of the fetched bytes):
  - `https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/kill.c` — `b32e0fad65e298235102f98aff37e02c94400b544d454cb57192ae697b100bf3`
  - `https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/main.c` — `08656b0bc90c85f23738661456b25c97af908bc5e2cfea78e0a69697b5f9d0e4`
  - `https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/msg.h` — `e36604984a916fb00a624c27c73034bcd87d7d6facff9b290a6a561ee58de56c`
  Quotes used (verbatim, ≤25 words each):
  - `kill.c:318` — `warn("escalating to SIGKILL after %.3f seconds\n", secs);`
  - `kill.c:627` — `sending %s to process %d`
  - `main.c:161` — `fprintf(stderr, "earlyoom " VERSION "\n");`
  - `main.c:414` — `fprintf(stderr, "sending SIGTERM when mem avail <= " PRIPCT " and swap free <= " PRIPCT ",\n",`
  - `main.c:416` — `fprintf(stderr, "        SIGKILL when mem avail <= " PRIPCT " and swap free <= " PRIPCT "\n",`
  - `main.c:295` — `warn("dryrun mode enabled, will not kill anything\n");`
  - `msg.h:10` — `#define PRIPCT "%5.2lf%%"`
- No tool was run, so no PASS/FAIL line for these cases exists yet. The L1 must run
  `python3 -I -B tools/mori-oom-killers.py --selftest --cases tools/fixtures/mori-oom-killers/cases-a2.json`
  (and the round-28 C2 counter) after the freeze commit. I did not run either.

## Blind-rule compliance

I did **not** open, grep, cat, or run `tools/mori-oom-killers.py` or any copy of it. I did **not** open
`.ufo/waves/round-26/evidence/`, `.ufo/waves/round-26/w1`, `.ufo/waves/round-26/w2`,
`.ufo/waves/round-27/w1` or `.ufo/waves/round-27/w2`. I ran **no** self-test, and no `jj`/`git` command in the lane.

Files I opened (all read-only):

1. `.ufo/waves/round-26/contract.md` — whole file, plus targeted raw ranges 76-80, 80-89, 90-106, 172-176 (the only
   contract text I derived from).
2. `.ufo/waves/round-27/contract.md` — lines 40-80 only (rule table; the A2-05 row is line 53).
3. `tools/fixtures/mori-oom-killers/cases.json` — schema and journal line shapes (the 32 frozen cases).
4. `.ufo/waves/round-28/contract.md` — the round-28 claim contract named in my seat context; no tool source, no
   round-26/27 evidence.
5. `.ufo/waves/round-28/wave1-dispatch.json` — my own seat spec only.
6. Directory listing of `tools/fixtures/mori-oom-killers/` (names and sizes only). I did **not** open
   `cases-supplementary.json`; it is outside the allowed read list.
7. Upstream `kill.c`, `main.c`, `msg.h` at tag `v1.9.0` via `curl` into my scratch dir (URLs, access time and
   sha256 above).

All paths above are relative to `/home/vgpnk/Projects/shokunin/mori-shokunin/`.

## Risks

- **R1 (only real risk).** Case 3 pins `earlyoom.scope_complete` for a *non-active* earlyoom. The contract lists
  `scope_complete` unconditionally inside the `earlyoom` object (`r26 contract.md:90-94`, no "or null", unlike
  `thresholds`/`actions`) and A2-05 is unconditional (`r26 :173-174`), so `false` is the contract-derived value; but
  the frozen `c06` (same show shape, `ActiveState=inactive`, AETM `0`) does not pin it. If the tool omits the field
  for a non-active unit, this one pin fails. The counter's rule requirement (≥1 case pinning `earlyoom.scope_complete`)
  is met by cases 1 and 2 regardless, so a failure here would cost one case, not the rule.
- **R2.** Whether an unbounded invocation admits whole-boot lines into the scope is not decided by the contract.
  That is exactly why `version`, `grammar`, `thresholds.*` and the action counts are unpinned in cases 1-2. The
  verdict/exit pairs are robust under both readings: case 1 is `KILLERS_UNKNOWN`/2 whether the version line counts as
  in scope (grammar verified) or not (grammar unverified, `:99-101` also fires); case 2 is `KILLER_ACTED`/1 either way
  because `oomd_notices` 3 alone is positive evidence (`:97-98`).
- **R3.** Case 2's `earlyoom_show` omits the `ActiveEnterTimestampMonotonic` line entirely — a shape no frozen
  round-26 case uses (every frozen show text carries the property). If the tool treats a missing property differently
  from `0` despite A2-05 naming both, case 2 fails; cases 1 and 3 use the explicit `0` form.
- **R4.** Ids use the `a2-05-` prefix from my seat brief; the counter requires printable unique ids and exactly one
  listed rule id, which all three satisfy. The invented threshold percentages `8.00/12.00/4.00/6.00` are pinned by no
  expectation, so a parsing difference cannot fail a case; they exist only to make the journal realistic.

## Blockers

None. No dependency on another seat, no decision needed from the L1 beyond merging the array above into
`tools/fixtures/mori-oom-killers/cases-a2.json` before the freeze commit.

## Tooling

No install or upgrade was performed in this wave. Tools already present and used: `python3` 3.14.8 (JSON validation),
`curl` 8.23.0 (upstream fetch), `jaq` 3.1.1 (JSON inspection), `git`/`bash` (read-only listing only). No pacman
transaction was run (host pacman transactions are paused).
