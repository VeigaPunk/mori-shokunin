# CaseA2r09 — blind case writer for rule A2-09 (round 28, wave 1)

Seat: `MoriR28.CaseA2r09` (leaf case writer). Rule written: **A2-09** only.
Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin`. Scratch: `/fast/scratch/hyaku/mori-r28/CaseA2r09/`.
Tooling installed or upgraded: **none** (no pacman, no uv, no npm, no cargo — the task needed only `curl`,
`python3` (stdlib) and the read/grep tools already present).

## Rule under test (verbatim)

- `.ufo/waves/round-27/contract.md:57` — `| A2-09 | send lines of a removed (`not-found`) earlyoom unit this boot are positive evidence |`
- Adopted at `.ufo/waves/round-26/contract.md:182` — "send lines of a removed (`not-found`) unit this boot are positive
  evidence" (wave-2 fix, CriticCapabilityRow Y8).

Scenario pinned by the cases: the earlyoom **unit file is gone** (`systemctl show` says `LoadState=not-found`), yet the
journal of the current boot still holds earlyoom.service lines from before the removal. Those send lines must be
**positive evidence** (`KILLER_ACTED`, exit 1), not silence.

## The cases (one fenced JSON array)

Each element carries exactly the five keys of the case schema plus the one added key `rule`:
`id`, `rule`, `why`, `inputs`, `expect{verdict, exit, fields}`.
Validated with `python3 -c 'import json,sys;json.load(sys.stdin)'` (exit 0, `JSON_VALID`) plus a structural check
(key sets, `rule == "A2-09"`, printable-ASCII ids, `__MONOTONIC_TIMESTAMP` decimal strings) — `ALL_OK 3`.

```json
[
  {
    "id": "a2-09-removed-unit-single-sigterm-send",
    "rule": "A2-09",
    "why": "Removed unit with one send line. The show text is what `systemctl show` prints for a unit whose unit file is gone: a read-only probe of a nonexistent unit on this host on 2026-10-22 returned LoadState=not-found, ActiveState=inactive, an empty UnitFileState and ActiveEnterTimestampMonotonic=0. A not-found unit is absent rather than inactive (round-26/contract.md:90 lists `absent` among the states; frozen case c07 pins this same show text to state `absent`). A2-09 (round-27/contract.md:57, adopted at round-26/contract.md:182) makes the send lines of a removed (not-found) unit this boot positive evidence, and the journal holds one `sending SIGTERM to process ` line (kill.c:627) whose pid and process name are invented, so the verdict is KILLER_ACTED exit 1 (round-26/contract.md:97-98). The scope is not complete: ActiveEnterTimestampMonotonic is 0, which leaves the invocation unbounded and scope_complete false (round-26/contract.md:173-174; A2-05 at round-27/contract.md:53), and positive evidence stands even when the scope is incomplete (round-26/contract.md:98). oomd_notices is 0, so no part of the evidence comes from oomd (round-26/contract.md:97); the oomd show text is the frozen inactive shape, so oomd.state is inactive and oomd.notices_this_boot is the 0 given in the inputs (round-26/contract.md:95). The action counts are deliberately not pinned: round-26/contract.md:102 puts actions null for an inactive or absent killer inside the quiet branch, while A2-09 puts this input in the acted branch, so the contract text does not say where the removed unit's send count is exposed.",
    "inputs": {
      "earlyoom_show": "LoadState=not-found\nActiveState=inactive\nUnitFileState=\nActiveEnterTimestampMonotonic=0\n",
      "oomd_show": "LoadState=loaded\nActiveState=inactive\nUnitFileState=disabled\nActiveEnterTimestampMonotonic=0\n",
      "earlyoom_journal": [
        {"MESSAGE": "sending SIGTERM to process 7311 \"fictional-compactor\"", "__MONOTONIC_TIMESTAMP": "19970000"}
      ],
      "oomd_notices": 0
    },
    "expect": {
      "verdict": "KILLER_ACTED",
      "exit": 1,
      "fields": {
        "earlyoom.state": "absent",
        "earlyoom.scope_complete": false,
        "oomd.state": "inactive",
        "oomd.notices_this_boot": 0
      }
    }
  },
  {
    "id": "a2-09-removed-unit-two-invocations-mixed-sends",
    "rule": "A2-09",
    "why": "Removed unit, two invocations this boot, sends in both. The unit file is gone, so the show text is the not-found shape (LoadState=not-found, ActiveState=inactive, empty UnitFileState, ActiveEnterTimestampMonotonic=0) and the state is absent (round-26/contract.md:90; frozen case c07). The journal holds two version lines (`earlyoom <version>`, main.c:161), so the boot is split into two invocations (round-26/contract.md:182, dry-run is applied per invocation split at each version line), and it holds one `sending SIGTERM to process ` line (kill.c:627), one `sending SIGKILL to process ` line (kill.c:627) and one `escalating to SIGKILL after ` line (kill.c:318). Every one of those three lines is a send or escalation line of the removed unit this boot, so A2-09 (round-27/contract.md:57) makes them positive evidence and the verdict is KILLER_ACTED exit 1 (round-26/contract.md:97-98). The scope is not complete because ActiveEnterTimestampMonotonic is 0, so the invocation is unbounded and scope_complete is false (round-26/contract.md:173-174; A2-05 at round-27/contract.md:53); the positive evidence still stands (round-26/contract.md:98). The counts of those three lines are not pinned, because round-26/contract.md:102 assigns actions null to an absent killer in the quiet branch and A2-09 moves this input to the acted branch, so the contract does not name the field that carries them. The two version lines do not make the state active, inactive or unavailable: only ActiveState decides that (round-26/contract.md:162-163 for the non-steady states). oomd_notices is 0 and the oomd show text is the frozen inactive shape, so oomd.state is inactive and oomd.notices_this_boot is 0 (round-26/contract.md:95, :97).",
    "inputs": {
      "earlyoom_show": "LoadState=not-found\nActiveState=inactive\nUnitFileState=\nActiveEnterTimestampMonotonic=0\n",
      "oomd_show": "LoadState=loaded\nActiveState=inactive\nUnitFileState=disabled\nActiveEnterTimestampMonotonic=0\n",
      "earlyoom_journal": [
        {"MESSAGE": "earlyoom 1.9.0", "__MONOTONIC_TIMESTAMP": "20481100"},
        {"MESSAGE": "sending SIGTERM to process 5120 \"fictional-archiver\"", "__MONOTONIC_TIMESTAMP": "20495000"},
        {"MESSAGE": "earlyoom 1.9.0", "__MONOTONIC_TIMESTAMP": "20610300"},
        {"MESSAGE": "sending SIGKILL to process 5121 \"fictional-archiver\"", "__MONOTONIC_TIMESTAMP": "20624500"},
        {"MESSAGE": "escalating to SIGKILL after 6.500 seconds", "__MONOTONIC_TIMESTAMP": "20624600"}
      ],
      "oomd_notices": 0
    },
    "expect": {
      "verdict": "KILLER_ACTED",
      "exit": 1,
      "fields": {
        "earlyoom.state": "absent",
        "earlyoom.scope_complete": false,
        "oomd.state": "inactive",
        "oomd.notices_this_boot": 0
      }
    }
  },
  {
    "id": "a2-09-removed-unit-three-sends-oomd-active",
    "rule": "A2-09",
    "why": "Removed unit, three send lines, oomd active but silent. The earlyoom show text is the not-found shape (LoadState=not-found, ActiveState=inactive, empty UnitFileState, ActiveEnterTimestampMonotonic=0), so the earlyoom state is absent (round-26/contract.md:90; frozen case c07). The journal holds one version line (`earlyoom <version>`, main.c:161) and three send lines: two `sending SIGTERM to process ` lines (kill.c:627) and one `sending SIGKILL to process ` line (kill.c:627), all with invented pids and process names. Those send lines belong to the removed unit this boot, so A2-09 (round-27/contract.md:57, round-26/contract.md:182) makes them positive evidence and the verdict is KILLER_ACTED exit 1 (round-26/contract.md:97-98). scope_complete is false because ActiveEnterTimestampMonotonic is 0, which leaves the invocation unbounded (round-26/contract.md:173-174; A2-05 at round-27/contract.md:53), and the positive evidence stands anyway (round-26/contract.md:98). The three send lines are not pinned as counts, because round-26/contract.md:102 gives an absent killer actions null in the quiet branch and A2-09 puts this input in the acted branch, so the contract does not name the field that would carry the counts. The oomd unit is active here, so oomd.state is active (round-26/contract.md:95; frozen case c10 pins this same oomd show text to state `active`), but oomd_notices is 0, so the oomd contributes no evidence of its own and oomd.notices_this_boot is 0 (round-26/contract.md:95, :97): the verdict comes from the removed earlyoom unit alone.",
    "inputs": {
      "earlyoom_show": "LoadState=not-found\nActiveState=inactive\nUnitFileState=\nActiveEnterTimestampMonotonic=0\n",
      "oomd_show": "LoadState=loaded\nActiveState=active\nUnitFileState=static\nActiveEnterTimestampMonotonic=12345678\n",
      "earlyoom_journal": [
        {"MESSAGE": "earlyoom 1.9.0", "__MONOTONIC_TIMESTAMP": "31880500"},
        {"MESSAGE": "sending SIGTERM to process 9042 \"fictional-ledger\"", "__MONOTONIC_TIMESTAMP": "31894000"},
        {"MESSAGE": "sending SIGTERM to process 9043 \"fictional-ledger\"", "__MONOTONIC_TIMESTAMP": "31894100"},
        {"MESSAGE": "sending SIGKILL to process 9044 \"fictional-ledger\"", "__MONOTONIC_TIMESTAMP": "31910500"}
      ],
      "oomd_notices": 0
    },
    "expect": {
      "verdict": "KILLER_ACTED",
      "exit": 1,
      "fields": {
        "earlyoom.state": "absent",
        "earlyoom.scope_complete": false,
        "oomd.state": "active",
        "oomd.notices_this_boot": 0
      }
    }
  }
]
```

## Per-case derivation table

Field values are derived from the contract text alone. "not pinned" lines below are fields the contract does **not**
decide for these inputs; they are deliberately absent from `expect.fields`.

### `a2-09-removed-unit-single-sigterm-send`

| Field | Value | Deciding contract line |
|---|---|---|
| `expect.verdict` | `KILLER_ACTED` | round-26 `contract.md:97` (positive evidence ⇒ KILLER_ACTED) + `:98` (evidence stands with an incomplete scope) + A2-09 at round-27 `contract.md:57` |
| `expect.exit` | `1` | round-26 `contract.md:97` ("`KILLER_ACTED`, exit 1") |
| `earlyoom.state` | `absent` | round-26 `contract.md:90` (state enum includes `absent`; `not-found` ⇒ absent as pinned by frozen `c07`) |
| `earlyoom.scope_complete` | `false` | round-26 `contract.md:173-174` (AETM missing/0 ⇒ unbounded ⇒ scope_complete false), rule A2-05 at round-27 `contract.md:53` |
| `oomd.state` | `inactive` | round-26 `contract.md:95` + `:162-163` (ActiveState `inactive` ⇒ `inactive`) |
| `oomd.notices_this_boot` | `0` | round-26 `contract.md:95` (field mirrors the input `oomd_notices`) |
| `earlyoom.actions*` | **not pinned** | round-26 `contract.md:102` reserves `actions: null` for an inactive/absent killer in the quiet branch; A2-09 moves this input to the acted branch and no line names the field that would carry the removed unit's send count |
| `earlyoom.grammar`, `earlyoom.version`, `earlyoom.thresholds`, `earlyoom.dryrun`, `earlyoom.earlier_invocation_send_lines` | **not pinned** | round-26 `contract.md:90-95` does not decide them for a not-found unit whose journal holds no version line / no threshold line |

### `a2-09-removed-unit-two-invocations-mixed-sends`

| Field | Value | Deciding contract line |
|---|---|---|
| `expect.verdict` | `KILLER_ACTED` | round-26 `contract.md:97-98` + A2-09 (round-27 `contract.md:57`, adopted round-26 `:182`) |
| `expect.exit` | `1` | round-26 `contract.md:97` |
| `earlyoom.state` | `absent` | round-26 `contract.md:90`; frozen `c07` (same show text) |
| `earlyoom.scope_complete` | `false` | round-26 `contract.md:173-174`; A2-05 (round-27 `:53`) |
| `oomd.state` | `inactive` | round-26 `contract.md:95`, `:162-163` |
| `oomd.notices_this_boot` | `0` | round-26 `contract.md:95` |
| `earlyoom.actions*`, `earlyoom.earlier_invocation_send_lines` | **not pinned** | the three send/escalation lines have no contract-decided home: `contract.md:102` gives an absent killer `actions: null` in the quiet branch, and A2-09 states only that such lines are positive evidence (round-27 `:57`) without naming a count field |
| `earlyoom.version`, `earlyoom.grammar` | **not pinned** | `contract.md:82` decides the version only for a version line of the *current* invocation; with a not-found unit there is no current invocation, so the contract does not decide the reported version/grammar |

### `a2-09-removed-unit-three-sends-oomd-active`

| Field | Value | Deciding contract line |
|---|---|---|
| `expect.verdict` | `KILLER_ACTED` | round-26 `contract.md:97-98` + A2-09 (round-27 `:57`) — oomd notices are 0, so the evidence is the removed unit's three send lines alone |
| `expect.exit` | `1` | round-26 `contract.md:97` |
| `earlyoom.state` | `absent` | round-26 `contract.md:90`; frozen `c07` |
| `earlyoom.scope_complete` | `false` | round-26 `contract.md:173-174`; A2-05 (round-27 `:53`) |
| `oomd.state` | `active` | round-26 `contract.md:95`; frozen `c10` pins this exact oomd show text to `active` |
| `oomd.notices_this_boot` | `0` | round-26 `contract.md:95` (input `oomd_notices` = 0) |
| `earlyoom.actions*` | **not pinned** | same reason as the other two cases (`contract.md:102` vs. A2-09) |
| `earlyoom.version`, `earlyoom.grammar`, `earlyoom.thresholds` | **not pinned** | `contract.md:90-95` does not decide them for a not-found unit |

### Distinctness (why these are not copies of the round-26 frozen cases)

- Show text: `LoadState=not-found` + empty `UnitFileState` + `ActiveEnterTimestampMonotonic=0` — frozen `c07` uses
  the same show text but an **empty** journal and expects `KILLERS_QUIET`/exit 0 (`cases.json:165-176`). All three of
  mine carry journal lines, so they exercise the A2-09 branch that `c07` cannot reach.
- Journal: new timestamps (19970000 / 20481100-20624600 / 31880500-31910500), new invented pids (7311, 5120-5121,
  9042-9044), new invented process names (`fictional-compactor`, `fictional-archiver`, `fictional-ledger`) — no
  `imaginary-keeper` / `imaginary-indexer` reuse. No uid, no cmdline, no real process names.
- Variation across the three: one send line vs. two invocations with three send/escalation lines vs. three sends in
  one invocation; oomd inactive vs. inactive vs. active; version line absent vs. two vs. one.

## Blindness statement

**I did not open, grep, cat or run the tool** `tools/mori-oom-killers.py` (nor any copy of it), did not open
`.ufo/waves/round-26/evidence/` or `.ufo/waves/round-26/w1`, `w2` or `.ufo/waves/round-27/w1`, `w2` reports, and did
not run any self-test. The three expected verdicts and every pinned field were derived from the contract text and
from the *frozen round-26 case file* only (read for schema and journal line shapes, as permitted).

### Files I opened (read-only)

| Path | Why |
|---|---|
| `skill://godspeed` | skill read |
| `.ufo/waves/round-27/contract.md:40-80` | A2 rule table and C2 statement (permitted) |
| `.ufo/waves/round-26/contract.md` (whole) | output spec, verdict rules, amendment A2 (permitted) |
| `tools/fixtures/mori-oom-killers/cases.json:1-403` (+ grep hits) | case schema and journal line shapes (permitted) |
| `https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/kill.c` | upstream log formats (permitted) |
| `https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/main.c` | upstream log formats (permitted) |
| `https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/msg.h` | upstream log formats (permitted) |
| `.ufo/waves/round-28/**` (directory listing only) | locate the w1 report path |

Upstream fetches: `2026-10-22T17:59:59Z`, `curl` — sha256 `b32e0fad65e298235102f98aff37e02c94400b544d454cb57192ae697b100bf3`
(kill.c), `08656b0bc90c85f23738661456b25c97af908bc5e2cfea78e0a69697b5f9d0e4` (main.c),
`e36604984a916fb00a624c27c73034bcd87d7d6facff9b290a6a561ee58de56c` (msg.h); saved under my scratch dir.
Quoted upstream lines: kill.c:282, kill.c:318, kill.c:627, kill.c:654, main.c:161, main.c:295, main.c:412-417,
main.c:519-523, msg.h:10.

### Host read that produced the not-found show shape (read-only, no unit touched)

`systemctl show mori-fixture-nonexistent-earlyoom.service -p LoadState,ActiveState,UnitFileState,ActiveEnterTimestampMonotonic`
→ `LoadState=not-found`, `ActiveState=inactive`, `UnitFileState=`, `ActiveEnterTimestampMonotonic=0` (exit 0).
The unit name is invented and does not exist; no unit was started, stopped or restarted.

## Risks and blockers

1. **Not-pinned count fields (by design).** The contract does not decide whether the removed unit's send lines are
   exposed in `earlyoom.actions`, in `earlyoom.earlier_invocation_send_lines`, or in neither, so no count is pinned.
   If the L1 wants a count assertion, that needs a contract decision (which field carries a not-found unit's sends),
   not a case-writer guess.
2. **`earlyoom.state` = `absent` for a not-found unit** is pinned from frozen `c07` plus `contract.md:90`. Residual
   risk: if the tool were to report `unavailable` for a not-found unit *only* when journal lines exist, all three
   cases would need re-derivation. The contract's state list has `absent` for exactly this shape, so `absent` is the
   contract-faithful value.
3. **`earlyoom.scope_complete` = `false`** rests on the A2-05 unbounded-invocation rule (`contract.md:173-174`),
   which applies because a not-found unit reports `ActiveEnterTimestampMonotonic=0`. If the tool suppressed
   `scope_complete` for an absent killer instead of reporting false, the pin would fail; the output spec at
   `contract.md:92-93` lists `scope_complete` as a plain boolean, not nullable.
4. **No blocker.** Three cases for A2-09 are ready; the L1 assembles `tools/fixtures/mori-oom-killers/cases-a2.json`
   from the ten rule-writing seats and runs the tool once at the freeze commit.

## Handoff to the L1

- File to merge: the fenced JSON array above (3 elements, each with `rule: "A2-09"`).
- Rule coverage claimed by this seat: A2-09 only. Required pinned field for A2-09 per the wave context
  (`earlyoom.state`) is present in all three cases, together with `verdict` and `exit`.
- Scratch copies kept at `/fast/scratch/hyaku/mori-r28/CaseA2r09/` (`cases-a2-r09.json`, `upstream/`).
