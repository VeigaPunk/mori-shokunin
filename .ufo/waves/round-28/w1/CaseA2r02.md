# CaseA2r02 — blind case writer for rule A2-02

Seat: `MoriR28.CaseA2r02` (wave 1, lane `/home/vgpnk/Projects/shokunin/mori-shokunin`).
Rule claimed: **A2-02** — "an earlyoom `ActiveState` other than `active` or `inactive` maps to state
`unavailable` and `KILLERS_UNKNOWN`" (round-27/contract.md:50; adopted as **A2b** in round-26/contract.md:162-163).

## What I produced

Three cases for rule id `A2-02`, with distinct inputs (distinct `ActiveState`, distinct invocation
boundary, distinct journal length and content, distinct oomd side). Machine-readable copy:
`/fast/scratch/hyaku/mori-r28/MoriR28.CaseA2r02/cases-a2r02.json`
(sha256 `a39d623fcd8d723f0146ba009b0b3d9cc99a6129406383b6cc436b5c3c840077`, 98 lines,
validated with `python3 -c 'import json,sys;json.load(sys.stdin)'` → exit 0).

I did **not** write `tools/fixtures/mori-oom-killers/cases-a2.json`: my bounds allow writing only my
own report file and files under my own scratch dir, and the file is assembled from the ten rule
seats by the integration seat. Each case carries exactly one `rule` key (`"A2-02"`), the schema of
`tools/fixtures/mori-oom-killers/cases.json` plus that key, as the wave context requires.

Checks run on my own cases (no tool, no self-test): `python3 -c 'import json,sys;json.load(sys.stdin)'`
on the array → JSON_VALID; structural check (every case has exactly `{id, rule, why, inputs, expect}`;
`rule == "A2-02"`; `id` matches `a2-02-<slug>`, ASCII, no newline; `expect` has exactly
`{verdict, exit, fields}`; `earlyoom.state` pinned in every case; every journal record has exactly
`MESSAGE` and `__MONOTONIC_TIMESTAMP`, numeric string); distinctness (no `id` collides with the 32
frozen round-26 ids, no `inputs` object equals any frozen round-26 `inputs` compared as canonical
JSON, the three inputs pairwise distinct).

## The cases

```json
[
 {
  "id": "a2-02-earlyoom-activestate-failed",
  "rule": "A2-02",
  "why": "Rule A2-02 decides the earlyoom state and the verdict; the other pinned fields are decided by the base contract for this input. State: round-26/contract.md:162-163 (Amendment A2, rule A2b adopted) says 'an ActiveState other than active or inactive (failed, activating, deactivating, reloading, maintenance) maps to state unavailable and KILLERS_UNKNOWN', and the same rule is row A2-02 of the frozen table at round-27/contract.md:50. The show text here carries ActiveState=failed, so earlyoom.state is unavailable; 'unavailable' is one of the four legal states at round-26/contract.md:90. Verdict and exit: round-26/contract.md:99 gives 'KILLERS_UNKNOWN, exit 2'. No positive evidence exists, so the KILLER_ACTED clause of round-26/contract.md:97 (an in-scope 'sending SIG... to process' line, an escalation line, or oomd_notices > 0) cannot fire: the journal holds no such line and oomd_notices is 0. scope_complete: ActiveEnterTimestampMonotonic=0 leaves the invocation unbounded, so scope_complete is false (round-26/contract.md:173-174, the same rule as round-27/contract.md:53). The oomd side is readable and steady (ActiveState=inactive), so oomd.state is inactive and the notice count is 0 (round-26/contract.md:95 lists oomd.state and oomd.notices_this_boot; the frozen case c06 in tools/fixtures/mori-oom-killers/cases.json pins this exact mapping and count for this show shape). Journal shapes are upstream earlyoom v1.9.0: 'Started Early OOM Daemon.' is a systemd unit line outside the grammar (round-26/contract.md:80-89; the same line appears in the frozen case c01), the version line is main.c:161, the threshold line is main.c:414 with PRIPCT '%5.2lf%%' (msg.h:10) and the failed-kill line is kill.c:654 ('kill failed: ' plus strerror). The kill failed line is not positive evidence under round-26/contract.md:97, which counts only send and escalation lines, so the verdict stays KILLERS_UNKNOWN; the frozen case c16 pins the same shape as non-positive evidence. Not pinned because the contract does not decide them for a non-active earlyoom: earlyoom.version, earlyoom.grammar, earlyoom.thresholds, earlyoom.actions (round-26/contract.md:102 fixes actions null for an inactive or absent killer only, and the frozen unavailable-state case c25 pins none), earlyoom.dryrun.",
  "inputs": {
   "earlyoom_show": "LoadState=loaded\nActiveState=failed\nUnitFileState=enabled\nActiveEnterTimestampMonotonic=0\n",
   "oomd_show": "LoadState=loaded\nActiveState=inactive\nUnitFileState=disabled\nActiveEnterTimestampMonotonic=0\n",
   "earlyoom_journal": [
    {
     "MESSAGE": "Started Early OOM Daemon.",
     "__MONOTONIC_TIMESTAMP": "77000001"
    },
    {
     "MESSAGE": "earlyoom 1.9.0",
     "__MONOTONIC_TIMESTAMP": "77000002"
    },
    {
     "MESSAGE": "sending SIGTERM when mem avail <= 12.00% and swap free <= 12.00%,",
     "__MONOTONIC_TIMESTAMP": "77000003"
    },
    {
     "MESSAGE": "kill failed: Operation not permitted",
     "__MONOTONIC_TIMESTAMP": "77000004"
    }
   ],
   "oomd_notices": 0
  },
  "expect": {
   "verdict": "KILLERS_UNKNOWN",
   "exit": 2,
   "fields": {
    "earlyoom.state": "unavailable",
    "earlyoom.scope_complete": false,
    "oomd.state": "inactive",
    "oomd.notices_this_boot": 0
   }
  }
 },
 {
  "id": "a2-02-earlyoom-activestate-deactivating",
  "rule": "A2-02",
  "why": "A second non-steady state, this time with a bounded invocation and a readable active oomd. State: round-26/contract.md:162-163 maps every ActiveState other than active or inactive to state unavailable and KILLERS_UNKNOWN, and round-27/contract.md:50 is the same rule as A2-02; ActiveState=deactivating is one of the states it names. The show read succeeded, so the state comes from the mapping and not from a failed read (the null read path is the frozen case c25). Verdict and exit: round-26/contract.md:99 gives 'KILLERS_UNKNOWN, exit 2'; no positive evidence exists under round-26/contract.md:97, because the journal holds no send line, no escalation line and no other positive line, and oomd_notices is 0. The oomd unit is readable and active, so oomd.state is active and its notice count is 0 (round-26/contract.md:95; the frozen cases c28 and c29 pin the same oomd show shape, the same oomd.state and the same count). Journal shapes are upstream earlyoom v1.9.0: the version line is main.c:161, the term threshold line is main.c:414 and the kill threshold line is main.c:416 (eight leading spaces in the format string, PRIPCT '%5.2lf%%' at msg.h:10, so the one digit kill percent renders with its pad space); the mem avail line is outside the grammar (round-26/contract.md:80-89; the same line shape appears in the frozen cases c01 and c05). The version line sits exactly on ActiveEnterTimestampMonotonic, which the scope rule keeps (round-26/contract.md:78-79). Not pinned because the contract does not decide them for a non-active earlyoom: earlyoom.scope_complete (the only rules that fix it are the boundary rule of round-26/contract.md:92-93 and the unbounded rule of round-26/contract.md:173-174, and for a unit that is not active the contract never says which invocation the version line belongs to; the frozen boundary cases c02 and c03 pin scope_complete only for an active unit), earlyoom.version, earlyoom.grammar, earlyoom.thresholds, earlyoom.actions (round-26/contract.md:102 fixes actions null for an inactive or absent killer only) and earlyoom.dryrun.",
  "inputs": {
   "earlyoom_show": "LoadState=loaded\nActiveState=deactivating\nUnitFileState=enabled\nActiveEnterTimestampMonotonic=41880003\n",
   "oomd_show": "LoadState=loaded\nActiveState=active\nUnitFileState=static\nActiveEnterTimestampMonotonic=53716002\n",
   "earlyoom_journal": [
    {
     "MESSAGE": "earlyoom 1.9.0",
     "__MONOTONIC_TIMESTAMP": "41880003"
    },
    {
     "MESSAGE": "sending SIGTERM when mem avail <= 12.00% and swap free <= 12.00%,",
     "__MONOTONIC_TIMESTAMP": "41880004"
    },
    {
     "MESSAGE": "        SIGKILL when mem avail <=  6.00% and swap free <=  6.00%",
     "__MONOTONIC_TIMESTAMP": "41880005"
    },
    {
     "MESSAGE": "mem avail: 9000 of 19000 MiB (47.37%), swap free: 7000 of 8192 MiB (85.45%)",
     "__MONOTONIC_TIMESTAMP": "41880006"
    }
   ],
   "oomd_notices": 0
  },
  "expect": {
   "verdict": "KILLERS_UNKNOWN",
   "exit": 2,
   "fields": {
    "earlyoom.state": "unavailable",
    "oomd.state": "active",
    "oomd.notices_this_boot": 0
   }
  }
 },
 {
  "id": "a2-02-earlyoom-activestate-activating-empty-journal",
  "rule": "A2-02",
  "why": "The quietest shape of the same rule: a transitional earlyoom state with nothing logged this boot, so the state mapping alone decides the outcome. State: ActiveState=activating is named in the rule at round-26/contract.md:162-163 and round-27/contract.md:50, so earlyoom.state is unavailable even though the unit is loaded and enabled and the show read succeeded. The journal is an empty list, not null: null means the read failed (round-26/contract.md:73; the frozen null journal case c08), while an empty list is a successful read with no record, so this case is neither the null read path nor the frozen inactive case c06. Verdict and exit: no positive evidence exists under round-26/contract.md:97 (no send line, no escalation line, oomd_notices 0), so round-26/contract.md:99 gives KILLERS_UNKNOWN with exit 2. scope_complete: ActiveEnterTimestampMonotonic=0 leaves the invocation unbounded, so scope_complete is false (round-26/contract.md:173-174, the same rule as round-27/contract.md:53). The oomd unit is readable and inactive, so oomd.state is inactive and the notice count is 0 (round-26/contract.md:95; the frozen case c06 pins the same mapping and count for this shape). Not pinned because the contract does not decide them for a non-active earlyoom: earlyoom.version, earlyoom.grammar, earlyoom.thresholds, earlyoom.actions (round-26/contract.md:102 fixes actions null for an inactive or absent killer only), earlyoom.dryrun; and with an empty journal there is no version line to decide a version or a grammar from (round-26/contract.md:82).",
  "inputs": {
   "earlyoom_show": "LoadState=loaded\nActiveState=activating\nUnitFileState=enabled\nActiveEnterTimestampMonotonic=0\n",
   "oomd_show": "LoadState=loaded\nActiveState=inactive\nUnitFileState=disabled\nActiveEnterTimestampMonotonic=0\n",
   "earlyoom_journal": [],
   "oomd_notices": 0
  },
  "expect": {
   "verdict": "KILLERS_UNKNOWN",
   "exit": 2,
   "fields": {
    "earlyoom.state": "unavailable",
    "earlyoom.scope_complete": false,
    "oomd.state": "inactive",
    "oomd.notices_this_boot": 0
   }
  }
 }
]
```

## Per-case derivation

Every expected value below is derived from the two contracts only. The rule-bearing line is
round-26/contract.md:162-163 (A2b adopted) = round-27/contract.md:50 (row A2-02). `round-26:N`
means `.ufo/waves/round-26/contract.md:N`.

### Case 1 — `a2-02-earlyoom-activestate-failed`

| field | value | contract line |
|---|---|---|
| `earlyoom.state` | `unavailable` | round-26:162-163 — ActiveState other than active/inactive → `unavailable`; state enum round-26:90 |
| `earlyoom.scope_complete` | `false` | round-26:173-174 — AETM `0` leaves the invocation unbounded → scope_complete false (= round-27:53) |
| `oomd.state` | `inactive` | round-26:95 (`oomd.state`); frozen c06 pins `inactive` for this show shape |
| `oomd.notices_this_boot` | `0` | round-26:95; frozen c06 pins `0` for `oomd_notices: 0` |
| verdict | `KILLERS_UNKNOWN` | round-26:162-163 (rule A2-02 fixes the verdict); round-26:99 for the exit code 2 |
| exit | `2` | round-26:99 — `KILLERS_UNKNOWN`, exit 2 |

KILLER_ACTED cannot fire: round-26:97 needs an in-scope send line, an escalation line, or
`oomd_notices > 0`; the journal holds none of those and `oomd_notices` is 0. The `kill failed:` line
is not positive evidence under round-26:97 (only send and escalation lines are) — frozen c16 pins
the same shape as non-positive evidence.

### Case 2 — `a2-02-earlyoom-activestate-deactivating`

| field | value | contract line |
|---|---|---|
| `earlyoom.state` | `unavailable` | round-26:162-163 (`deactivating` is named); round-26:90 |
| `oomd.state` | `active` | round-26:95; frozen c28 pins `active` for this oomd show shape |
| `oomd.notices_this_boot` | `0` | round-26:95; frozen c28 pins `0` for `oomd_notices: 0` |
| verdict | `KILLERS_UNKNOWN` | round-26:162-163; no positive evidence under round-26:97 |
| exit | `2` | round-26:99 |

`earlyoom.scope_complete` is deliberately **not** pinned here: the only rules that fix it are
round-26:92-93 (version line of the *current invocation* inside the scope) and round-26:173-174
(AETM missing or 0 → unbounded), and for a unit that is not active the contract never says which
invocation is current. The frozen boundary cases c02/c03 pin `scope_complete` only for an active unit.

### Case 3 — `a2-02-earlyoom-activestate-activating-empty-journal`

| field | value | contract line |
|---|---|---|
| `earlyoom.state` | `unavailable` | round-26:162-163 (`activating` is named); round-26:90 |
| `earlyoom.scope_complete` | `false` | round-26:173-174 — AETM `0` → unbounded → false |
| `oomd.state` | `inactive` | round-26:95; frozen c06 |
| `oomd.notices_this_boot` | `0` | round-26:95; frozen c06 |
| verdict | `KILLERS_UNKNOWN` | round-26:162-163; no positive evidence under round-26:97 |
| exit | `2` | round-26:99 |

Empty list ≠ null: round-26:73 — `null` means the read failed (frozen c08); `[]` is a successful
read with no record, so this is not the A2-08 null-journal path.

### Fields I did not pin, and why

`earlyoom.version`, `earlyoom.grammar`, `earlyoom.thresholds`, `earlyoom.actions`,
`earlyoom.dryrun` are unpinned in all three cases: the contract fixes `actions: null` only for an
**inactive or absent** killer (round-26:102) and says nothing about the `unavailable` state that
A2-02 introduces; the frozen unavailable-state case c25 likewise pins no such field. For
`scope_complete` in case 2 see above. `earlyoom.earlier_invocation_send_lines` is unpinned because
the contract does not say whether it is emitted for a non-active unit (round-26:175-179).

## Blindness statement

I did **not** open, grep, cat, or run `tools/mori-oom-killers.py` or any copy of it; I did not open
`.ufo/waves/round-26/evidence/`, nor the round-26 `w1`/`w2` or round-27 `w1`/`w2` reports; I ran no
self-test and no tool command of any kind. Every expected value above was derived from the two
contract files and the frozen case file only.

Files I opened (all read-only):

1. `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-27/contract.md:40-80` (plus its
   rule-table lines 49-58 via a line-numbered grep for citation).
2. `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-26/contract.md` (whole file; lines
   60-110 and 150-200 re-read with line numbers for citation).
3. `/home/vgpnk/Projects/shokunin/mori-shokunin/tools/fixtures/mori-oom-killers/cases.json` (schema
   and journal line shapes; ids c01, c02, c03, c05, c06, c16, c19, c25, c27, c28, c29, c30 read).
4. Upstream earlyoom v1.9.0 sources fetched by `curl` (public raw URLs, ordinary means):

| URL | fetched (UTC) | sha256 of bytes |
|---|---|---|
| `https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/kill.c` | 2026-10-22T17:59:33Z | `b32e0fad65e298235102f98aff37e02c94400b544d454cb57192ae697b100bf3` |
| `https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/main.c` | 2026-10-22T17:59:33Z | `08656b0bc90c85f23738661456b25c97af908bc5e2cfea78e0a69697b5f9d0e4` |
| `https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/msg.h` | 2026-10-22T17:59:33Z | `e36604984a916fb00a624c27c73034bcd87d7d6facff9b290a6a561ee58de56c` |

Verbatim quotes used (each ≤ 25 words, with its line number in the fetched file):

- `kill.c:654` — `warn("kill failed: %s\n", strerror(saved_errno));`
- `kill.c:627` — `warn("sending %s to process %d uid %d \"%s\": oom_score %d, oom_score_adj %d, VmRSS %lld MiB, cmdline \"%s\"\n",`
- `main.c:161` — `fprintf(stderr, "earlyoom " VERSION "\n");`
- `main.c:414` — `fprintf(stderr, "sending SIGTERM when mem avail <= " PRIPCT " and swap free <= " PRIPCT ",\n",`
- `main.c:416` — `fprintf(stderr, "        SIGKILL when mem avail <= " PRIPCT " and swap free <= " PRIPCT "\n",`
- `msg.h:10` — `#define PRIPCT "%5.2lf%%"`

(The `mem avail:` line in case 2 is out of grammar per round-26:80-89; its shape is taken from the
frozen cases c01/c05, since `meminfo.c` is outside my allowed fetch list.)

## Risks and notes for the integration seat

- **The tool's verdict for a non-steady earlyoom with positive evidence is not pinned by my cases.**
  A2-02 as written maps the state and the verdict together, so my cases keep the journal free of
  send/escalation lines and `oomd_notices` at 0. A case with a send line in scope under
  `ActiveState=failed` would need the L1 to decide whether round-26:97 (positive evidence stands)
  outranks the A2-02 verdict; the contract does not settle that order, so I did not invent it.
- **`actions` for the `unavailable` state is unpinned on purpose** (see above). If the tool emits
  `actions: null` for a non-steady state, my cases still pass because they assert nothing about it.
- **`scope_complete: false` in cases 1 and 3** rests on the unbounded-invocation rule
  (round-26:173-174) with `ActiveEnterTimestampMonotonic=0`; three independent readings agree on
  `false` there (unbounded invocation; the "true only when" wording of round-26:92-93; no in-scope
  version line of a current invocation for a unit that is not active).
- My `id` slugs use the `a2-02-` prefix as the wave context requires, unique against the 32
  frozen round-26 ids.

## Tooling and files changed

No package was installed or upgraded for this seat; the work needed only `python3` (standard
library), `curl` and `sha256sum`, all already present on this host. No host service was touched.
Files changed: `.ufo/waves/round-28/w1/CaseA2r02.md` (this report, in the lane);
`/fast/scratch/hyaku/mori-r28/MoriR28.CaseA2r02/cases-a2r02.json` (scratch, machine-readable cases);
`/fast/scratch/hyaku/mori-r28/MoriR28.CaseA2r02/src/{kill.c,main.c,msg.h}` (scratch, upstream sources).
