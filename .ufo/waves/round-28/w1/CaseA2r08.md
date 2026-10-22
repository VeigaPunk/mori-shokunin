# CaseA2r08 — blind case writer for rule A2-08 (round 28, wave 1)

Seat: `MoriR28.CaseA2r08`. Rule: **A2-08** — "a `null` earlyoom journal reads `KILLERS_UNKNOWN` for any
earlyoom state" (round-27/contract.md:56; adopted at round-26/contract.md:181-182).

Deliverable: 3 cases for `tools/fixtures/mori-oom-killers/cases-a2.json`. All three pin
`earlyoom.state` with a value other than `active` in two of them (`inactive`, `absent`), which is the
field the round-28 counter requires for A2-08, and every case pins both a verdict and an exit code.

## 1. The cases

Ready to paste as a JSON array. Validated with
`python3 -c 'import json,sys;json.load(sys.stdin)'` in
`/fast/scratch/hyaku/mori-r28/CaseA2r08/a2-08-cases.json` (sha256
`fe6f0a9e9f1f0325918f1fa35eb38106037ba537d595a9afd278b006239005f5` before the last two `why` edits; the
array is unchanged in shape, ids, inputs and expectations).

```json
[
  {
   "id": "a2-08-null-journal-inactive-earlyoom",
   "rule": "A2-08",
   "why": "Null earlyoom journal with an inactive earlyoom. The journal read failed, so `earlyoom_journal` is null (round-26/contract.md:73, '`null` means the read failed'). Rule A2-08 (round-27/contract.md:56, adopted at round-26/contract.md:181-182) reads a null earlyoom journal as `KILLERS_UNKNOWN` for any earlyoom state, so the inactive state does not excuse the failed read. The verdict is `KILLERS_UNKNOWN` exit 2 (round-26/contract.md:99-101: a needed read that is null). No positive evidence overrides it: the journal holds no line at all and `oomd_notices` is 0, so round-26/contract.md:97 (an in scope send or escalation line, or oomd notices above zero) is not met. The state is `inactive` because the show text reads LoadState=loaded with ActiveState=inactive, one of the four states of round-26/contract.md:90-91; the frozen round-26 case c06 pins that same show text to `inactive` at tools/fixtures/mori-oom-killers/cases.json:157. The actions block is null because an inactive killer reports actions null and never zero counts (round-26/contract.md:102). The oomd state is `inactive` from its own show text and the notice count is the input value 0 (round-26/contract.md:95). Not pinned: earlyoom.version, earlyoom.grammar, earlyoom.thresholds, earlyoom.scope_complete, earlyoom.dryrun. With a null journal no MESSAGE line exists (the grammar of round-26/contract.md:80-89), so the contract fixes no value for them.",
   "inputs": {
    "earlyoom_show": "LoadState=loaded\nActiveState=inactive\nUnitFileState=disabled\nActiveEnterTimestampMonotonic=0\n",
    "oomd_show": "LoadState=loaded\nActiveState=inactive\nUnitFileState=disabled\nActiveEnterTimestampMonotonic=28741905\n",
    "earlyoom_journal": null,
    "oomd_notices": 0
   },
   "expect": {
    "verdict": "KILLERS_UNKNOWN",
    "exit": 2,
    "fields": {
     "earlyoom.state": "inactive",
     "earlyoom.actions": null,
     "oomd.state": "inactive",
     "oomd.notices_this_boot": 0
    }
   }
  },
  {
   "id": "a2-08-null-journal-absent-earlyoom",
   "rule": "A2-08",
   "why": "Null earlyoom journal with an absent earlyoom. `earlyoom_journal` is null because the read failed (round-26/contract.md:73). Rule A2-08 (round-27/contract.md:56, adopted at round-26/contract.md:181-182) reads a null earlyoom journal as `KILLERS_UNKNOWN` for any earlyoom state, and `absent` is one of the states of round-26/contract.md:90-91. The verdict is `KILLERS_UNKNOWN` exit 2 (round-26/contract.md:99-101). No positive evidence stands: the journal is null, so there is no in scope send or escalation line, and `oomd_notices` is 0, so round-26/contract.md:97 is not met. The state is `absent` because the show text of a unit that does not exist reads LoadState=not-found, the removed unit that round-26/contract.md:182 (rule A2-09) and round-27/contract.md:57 treat apart from an inactive unit; the frozen round-26 case c07 pins that same show text to `absent` at tools/fixtures/mori-oom-killers/cases.json:177. The actions block is null because an absent killer reports actions null and never zero counts (round-26/contract.md:102). The oomd side is readable and quiet: its show text gives ActiveState=active and `oomd_notices` is 0, which is not positive evidence (round-26/contract.md:97), so the oomd state is `active` and the notice count is 0 (round-26/contract.md:95). Not pinned: earlyoom.version, earlyoom.grammar, earlyoom.thresholds, earlyoom.scope_complete, earlyoom.dryrun, because a null journal yields no MESSAGE line for the grammar of round-26/contract.md:80-89 to decide.",
   "inputs": {
    "earlyoom_show": "LoadState=not-found\nActiveState=inactive\nUnitFileState=\nActiveEnterTimestampMonotonic=0\n",
    "oomd_show": "LoadState=loaded\nActiveState=active\nUnitFileState=static\nActiveEnterTimestampMonotonic=44120983\n",
    "earlyoom_journal": null,
    "oomd_notices": 0
   },
   "expect": {
    "verdict": "KILLERS_UNKNOWN",
    "exit": 2,
    "fields": {
     "earlyoom.state": "absent",
     "earlyoom.actions": null,
     "oomd.state": "active",
     "oomd.notices_this_boot": 0
    }
   }
  },
  {
   "id": "a2-08-null-journal-active-earlyoom-readable-oomd",
   "rule": "A2-08",
   "why": "Null earlyoom journal with an active earlyoom and a readable, active oomd. `earlyoom_journal` is null because the read failed (round-26/contract.md:73). Rule A2-08 (round-27/contract.md:56, adopted at round-26/contract.md:181-182) reads a null earlyoom journal as `KILLERS_UNKNOWN` for any earlyoom state, so the active state does not change the outcome: the verdict is `KILLERS_UNKNOWN` exit 2 (round-26/contract.md:99-101, a needed read that is null). A readable and active oomd with `oomd_notices` 0 carries no positive evidence (round-26/contract.md:97), so it cannot pull the verdict to quiet. The earlyoom state is `active` because the show text reads LoadState=loaded with ActiveState=active (round-26/contract.md:90-91); the frozen round-26 case c08 pins that same show text to `active` with a null journal at tools/fixtures/mori-oom-killers/cases.json:197. This case differs from c08 in the oomd side: c08 has an inactive oomd with notices 0, this one has a readable active oomd, which still carries no positive evidence at `oomd_notices` 0 (round-26/contract.md:97). The actions block is null, not zero counts: the journal read failed, so no count of send, escalation, failed kill or low memory line exists (round-26/contract.md:93-94 lists actions as a count block or null), and the frozen round-26 case c08 pins `earlyoom.actions` null for an active earlyoom with a null journal at tools/fixtures/mori-oom-killers/cases.json:198. The oomd state is `active` from its show text and the notice count is the input value 0 (round-26/contract.md:95). Not pinned: earlyoom.version, earlyoom.grammar, earlyoom.thresholds, earlyoom.scope_complete, earlyoom.dryrun, because a null journal yields no MESSAGE line for the grammar of round-26/contract.md:80-89 to decide.",
   "inputs": {
    "earlyoom_show": "LoadState=loaded\nActiveState=active\nUnitFileState=enabled\nActiveEnterTimestampMonotonic=33002571\n",
    "oomd_show": "LoadState=loaded\nActiveState=active\nUnitFileState=static\nActiveEnterTimestampMonotonic=55211476\n",
    "earlyoom_journal": null,
    "oomd_notices": 0
   },
   "expect": {
    "verdict": "KILLERS_UNKNOWN",
    "exit": 2,
    "fields": {
     "earlyoom.state": "active",
     "earlyoom.actions": null,
     "oomd.state": "active",
     "oomd.notices_this_boot": 0
    }
   }
  }
]
```

## 2. Per-case derivation

### a2-08-null-journal-inactive-earlyoom

| field | value | contract line |
|---|---|---|
| `expect.verdict` | `KILLERS_UNKNOWN` | round-26/contract.md:99-101 (rule 2, a needed read that is null); A2-08 round-27/contract.md:56 |
| `expect.exit` | `2` | round-26/contract.md:99 (rule 2 exit 2) |
| `earlyoom.state` | `inactive` | round-26/contract.md:90-91 (state vocabulary); LoadState=loaded + ActiveState=inactive → inactive, frozen c06 at cases.json:157 |
| `earlyoom.actions` | `null` | round-26/contract.md:102 (an inactive killer reports actions null, never zero counts) |
| `oomd.state` | `inactive` | round-26/contract.md:95 (oomd state); own show text ActiveState=inactive; frozen c06 at cases.json:159 |
| `oomd.notices_this_boot` | `0` | round-26/contract.md:95; input `oomd_notices` 0; frozen c06 at cases.json:160 |

Not pinned, with reason: `earlyoom.version`, `earlyoom.grammar`, `earlyoom.thresholds`,
`earlyoom.scope_complete`, `earlyoom.dryrun` — a null journal yields no MESSAGE line, so the grammar of
round-26/contract.md:80-89 has nothing to decide them from. The contract fixes no value for them.

### a2-08-null-journal-absent-earlyoom

| field | value | contract line |
|---|---|---|
| `expect.verdict` | `KILLERS_UNKNOWN` | round-26/contract.md:99-101; A2-08 round-27/contract.md:56 ("for any earlyoom state") |
| `expect.exit` | `2` | round-26/contract.md:99 |
| `earlyoom.state` | `absent` | round-26/contract.md:90-91 (state vocabulary); LoadState=not-found → absent, frozen c07 at cases.json:177; the removed-unit notion of A2-09, round-26/contract.md:182 |
| `earlyoom.actions` | `null` | round-26/contract.md:102 (an absent killer reports actions null) |
| `oomd.state` | `active` | round-26/contract.md:95; own show text ActiveState=active; frozen c10 at cases.json:247 |
| `oomd.notices_this_boot` | `0` | round-26/contract.md:95; input `oomd_notices` 0 |

Not pinned: same five fields as above, same reason.

### a2-08-null-journal-active-earlyoom-readable-oomd

| field | value | contract line |
|---|---|---|
| `expect.verdict` | `KILLERS_UNKNOWN` | round-26/contract.md:99-101; A2-08 round-27/contract.md:56 |
| `expect.exit` | `2` | round-26/contract.md:99 |
| `earlyoom.state` | `active` | round-26/contract.md:90-91; LoadState=loaded + ActiveState=active → active, frozen c08 at cases.json:197 |
| `earlyoom.actions` | `null` | round-26/contract.md:93-94 (actions is a count block or null); no journal means no counts to make; frozen c08 at cases.json:198 |
| `oomd.state` | `active` | round-26/contract.md:95; own show text ActiveState=active; frozen c28 at cases.json:683 |
| `oomd.notices_this_boot` | `0` | round-26/contract.md:95; input `oomd_notices` 0 |

Not pinned: same five fields as above, same reason.

### Why `oomd_notices` is 0 in all three

Round-26/contract.md:97 makes `oomd_notices > 0` positive evidence on its own, and rule 1 (exit 1) is
checked before rule 2 (exit 2). A non-zero notice count would make these cases `KILLER_ACTED` instead of
the A2-08 `KILLERS_UNKNOWN`, so the notice count stays at 0 in every case and the A2-08 branch is the one
under test.

### Distinctness from the frozen round-26 file

The frozen file already has `c08-null-journal` (cases.json:185-202): an active earlyoom, a null journal,
an inactive oomd, notices 0. My third case keeps the null journal and the active earlyoom but changes the
oomd side to a readable, active oomd, so the "any earlyoom state" clause is exercised with a second
readable killer present. The first two cases use states the frozen file never pairs with a null journal:
`inactive` (frozen c06 has an empty list, cases.json:170) and `absent` (frozen c07 has an empty list,
cases.json:170). Input-level check: the three input objects are distinct from each other and from all 32
frozen input objects (comparison on the canonical JSON of `inputs`, overlap 0).

## 3. Blindness statement

**I did not open, grep, cat or run** `tools/mori-oom-killers.py` or any copy of it; I did not open
`.ufo/waves/round-26/evidence/`, `.ufo/waves/round-26/w1`, `.ufo/waves/round-26/w2`,
`.ufo/waves/round-27/w1` or `.ufo/waves/round-27/w2`; and I ran no self-test and no `--inputs` or
`--selftest` invocation of the tool. Every expected value above is derived from the round-26 and
round-27 contract text plus the permitted read of the frozen case file's schema and journal line shapes.

### Files I opened (all reads)

Lane files (read-only):

1. `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-26/contract.md` — whole spec, including
   the amendment at :152-200. Lines read: 60-80, 88-96, 100-205, plus targeted greps that returned line
   numbers for :66-78, :89-96, :158-185.
2. `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-27/contract.md` — lines 40-80 (the
   permitted window), which covers the frozen rule table at :47-58.
3. `/home/vgpnk/Projects/shokunin/mori-shokunin/tools/fixtures/mori-oom-killers/cases.json` — schema and
   journal line shapes, plus the `expect` blocks of the frozen cases I cite (c06, c07, c08, c10, c25,
   c28, c30) at :144-204, :228-252, :599-626, :708-730.
4. `/home/vgpnk/.agents/skills/godspeed/SKILL.md` — the skill named in the assignment.

Upstream sources, fetched by ordinary `curl` into my scratch dir (not into the lane), for real log line
formats:

5. `https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/main.c` — accessed 2026-10-22T18:08:08Z,
   sha256 `08656b0bc90c85f23738661456b25c97af908bc5e2cfea78e0a69697b5f9d0e4`. Quote (main.c:161, 6 words):
   `fprintf(stderr, "earlyoom " VERSION "\n");`
6. `https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/kill.c` — accessed 2026-10-22T18:08:08Z,
   sha256 `b32e0fad65e298235102f98aff37e02c94400b544d454cb57192ae697b100bf3`.
7. `https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/msg.h` — accessed 2026-10-22T18:08:08Z,
   sha256 `e36604984a916fb00a624c27c73034bcd87d7d6facff9b290a6a561ee58de56c`.

Files I wrote (both inside my own bounds):

8. `/fast/scratch/hyaku/mori-r28/CaseA2r08/a2-08-cases.json` — the validated case array.
9. `.ufo/waves/round-28/w1/CaseA2r08.md` — this report.

## 4. Risks and blockers

- **The upstream fetch was unnecessary for these three cases.** All three have a null journal, so no
  MESSAGE line is parsed and no grammar value is pinned. The fetch is recorded above because it was run,
  not because any expected value depends on it.
- **`earlyoom.actions` for the active case is the one value I pinned on a frozen-case precedent rather
  than on an explicit contract sentence.** Contract line 102 states the null-actions rule for an inactive
  or absent killer; for an active killer with a null journal the contract says only that `actions` is a
  count block or null (round-26/contract.md:93-94). I pinned `null` because frozen c08 pins
  `earlyoom.actions: null` for exactly that shape (cases.json:198) and the frozen file must keep passing
  at the landed tip. If the L1 prefers a strictly contract-text-only reading, drop that one field from
  case 3; the case still pins verdict, exit and `earlyoom.state`.
- **No blocker.** The rule text, the counter requirement (A2-08 → `earlyoom.state` with a value other
  than `active` in at least one case) and the case schema are all satisfied by the array above.
- **No tool was installed or upgraded**, so there is no tool/version/channel/reason entry to report. The
  host's `python3` is 3.14.8 and `jq` was not needed; all pacman transactions stayed paused as instructed.
