# CaseA2r06 — blind case writer for round-28 C2, rule A2-06

Seat: `MoriR28.CaseA2r06` (executor, leaf). Wave: round-28, wave 1. L1 / integration owner: `MoriR28`.
Rule under test (round-27 `contract.md:54`): **A2-06** — "send lines of this boot outside the current invocation go to
`earlyoom.earlier_invocation_send_lines`; non-zero is positive evidence (`KILLER_ACTED`) for an earlyoom that is not
active, reported without a verdict change for an active one". Required pinned field per the wave context:
`earlyoom.earlier_invocation_send_lines`. Deliverable: 3 frozen blind cases for A2-06, contributed to
`tools/fixtures/mori-oom-killers/cases-a2.json` (the L1 assembles the file; I wrote only this report plus my scratch dir).

## Files changed

`.ufo/waves/round-28/w1/CaseA2r06.md` (this report — the only file written in the lane), plus scratch
`/fast/scratch/hyaku/mori-r28/CaseA2r06/cases-a2-06.json` (validated copy of the case array) and
`/fast/scratch/hyaku/mori-r28/CaseA2r06/{kill.c,main.c,msg.h,unit.c,dbus-unit.c}` (upstream bytes fetched by curl).
No lane file was edited other than this report. No git/jj command was run in the lane; no commit, no ref update.

Tooling: **no install and no upgrade were made.** `python3` (3.14.8) and `curl` were already present; only `curl`,
`python3`, `sha256sum`, `date`, `grep`, `sed` were used, all pre-installed. No pacman transaction was attempted (the
wave context pauses pacman host-wide).

## The cases (JSON array, ready to append to `cases-a2.json`)

```json
[
 {
  "id": "a2-06-active-earlier-invocation-sends-quiet",
  "rule": "A2-06",
  "why": "A2-06 (round-27 contract.md:54; adopted form round-26 contract.md:175-179) on an active earlyoom: send lines of this boot outside the current invocation go to earlyoom.earlier_invocation_send_lines and are reported without a verdict change. The scope of the current invocation is __MONOTONIC_TIMESTAMP >= ActiveEnterTimestampMonotonic = 64000000 (round-26 contract.md:78-79), so the SIGTERM send at 12100000 and the SIGKILL send at 12200000, both belonging to the earlier invocation that opened with its version line at 12000000, are outside it and the count is 2. Being out of scope they are not positive evidence under the enumeration of round-26 contract.md:97, so the verdict stays KILLERS_QUIET exit 0, which is the shape frozen by c02 and named as the disclosed limit at round-26 contract.md:171-172 and round-26 contract.md:178-179. The current invocation opens with its version line at 64000000, exactly at ActiveEnterTimestampMonotonic, which is inside the scope (round-26 contract.md:78, and the boundary frozen by c03), so scope_complete is true (round-26 contract.md:92-93). Both version lines read earlyoom 1.9.0 (main.c:161), so earlyoom.version is 1.9.0 and earlyoom.grammar is verified-1.9.0 whichever version line the reader takes. The threshold lines are the main.c:414 and main.c:416 forms with PRIPCT \"%5.2lf%%\" (msg.h:10), so 12.50 renders as 12.50% and 6.25 as \" 6.25%\"; both invocations print the same pair, so the four thresholds of round-26 contract.md:91-92 are 12.5/12.5/6.25/6.25 whichever invocation is read. No send, escalation, kill-failed or low-memory line is in scope, so the five action counts of round-26 contract.md:94 are 0, and no dryrun line (round-26 contract.md:89) leaves earlyoom.dryrun false.",
  "inputs": {
   "earlyoom_show": "LoadState=loaded\nActiveState=active\nUnitFileState=enabled\nActiveEnterTimestampMonotonic=64000000\n",
   "oomd_show": "LoadState=loaded\nActiveState=inactive\nUnitFileState=disabled\nActiveEnterTimestampMonotonic=0\n",
   "earlyoom_journal": [
    {"MESSAGE": "earlyoom 1.9.0", "__MONOTONIC_TIMESTAMP": "12000000"}, {"MESSAGE": "sending SIGTERM when mem avail <= 12.50% and swap free <= 12.50%,", "__MONOTONIC_TIMESTAMP": "12000100"},
    {"MESSAGE": "        SIGKILL when mem avail <=  6.25% and swap free <=  6.25%", "__MONOTONIC_TIMESTAMP": "12000100"}, {"MESSAGE": "sending SIGTERM to process 90001 \"imaginary-bellows\"", "__MONOTONIC_TIMESTAMP": "12100000"},
    {"MESSAGE": "sending SIGKILL to process 90002 \"imaginary-lathe\"", "__MONOTONIC_TIMESTAMP": "12200000"}, {"MESSAGE": "earlyoom 1.9.0", "__MONOTONIC_TIMESTAMP": "64000000"},
    {"MESSAGE": "sending SIGTERM when mem avail <= 12.50% and swap free <= 12.50%,", "__MONOTONIC_TIMESTAMP": "64000000"}, {"MESSAGE": "        SIGKILL when mem avail <=  6.25% and swap free <=  6.25%", "__MONOTONIC_TIMESTAMP": "64000000"}
   ],
   "oomd_notices": 0
  },
  "expect": {
   "verdict": "KILLERS_QUIET",
   "exit": 0,
   "fields": {
    "earlyoom.state": "active", "earlyoom.version": "1.9.0",
    "earlyoom.grammar": "verified-1.9.0", "earlyoom.thresholds.term_mem_pct": 12.5,
    "earlyoom.thresholds.term_swap_pct": 12.5, "earlyoom.thresholds.kill_mem_pct": 6.25,
    "earlyoom.thresholds.kill_swap_pct": 6.25, "earlyoom.scope_complete": true,
    "earlyoom.actions.sigterm": 0, "earlyoom.actions.sigkill": 0,
    "earlyoom.actions.escalations": 0, "earlyoom.actions.kill_failed": 0,
    "earlyoom.actions.low_memory_warnings": 0, "earlyoom.dryrun": false,
    "earlyoom.earlier_invocation_send_lines": 2, "oomd.state": "inactive",
    "oomd.notices_this_boot": 0
   }
  }
 },
 {
  "id": "a2-06-inactive-earlier-invocation-sends-acted",
  "rule": "A2-06",
  "why": "A2-06 (round-27 contract.md:54; adopted form round-26 contract.md:175-179) on an earlyoom that is not active: a non-zero earlyoom.earlier_invocation_send_lines is positive evidence, so the verdict is KILLER_ACTED exit 1, and round-26 contract.md:177-178 names this shape as the case where a stop without restart no longer reads quiet. The unit is loaded but not running (ActiveState=inactive), so earlyoom.state is inactive (round-26 contract.md:90-91) and the actions block is null, never zero counts (round-26 contract.md:102-103, the shape frozen by c06). The three send lines of this boot are stamped 40100000, 40200000 and 40300000, all before ActiveEnterTimestampMonotonic = 70000000 and all in the invocation that opened with the version line at 40000000, so they are outside the current invocation and the count is 3; the version line at 70000000 opens the current invocation, at exactly ActiveEnterTimestampMonotonic as in frozen c02 and c03. oomd is inactive with zero notices, so the oomd fields are the ones round-26 contract.md:95 and round-26 contract.md:102 decide. Not pinned: earlyoom.version, earlyoom.grammar, earlyoom.thresholds, earlyoom.scope_complete and earlyoom.dryrun, because with an inactive unit the contract text does not decide them (round-26 contract.md:90-95 fixes only the field names, and the frozen inactive case c06 pins none of them).",
  "inputs": {
   "earlyoom_show": "LoadState=loaded\nActiveState=inactive\nUnitFileState=enabled\nActiveEnterTimestampMonotonic=70000000\n",
   "oomd_show": "LoadState=loaded\nActiveState=inactive\nUnitFileState=disabled\nActiveEnterTimestampMonotonic=0\n",
   "earlyoom_journal": [
    {"MESSAGE": "earlyoom 1.9.0", "__MONOTONIC_TIMESTAMP": "40000000"}, {"MESSAGE": "sending SIGTERM when mem avail <=  9.00% and swap free <=  9.00%,", "__MONOTONIC_TIMESTAMP": "40000000"},
    {"MESSAGE": "        SIGKILL when mem avail <=  4.50% and swap free <=  4.50%", "__MONOTONIC_TIMESTAMP": "40000000"}, {"MESSAGE": "sending SIGTERM to process 90003 \"imaginary-sifter\"", "__MONOTONIC_TIMESTAMP": "40100000"},
    {"MESSAGE": "sending SIGTERM to process 90004 \"imaginary-ploughman\"", "__MONOTONIC_TIMESTAMP": "40200000"}, {"MESSAGE": "sending SIGKILL to process 90005 \"imaginary-mason\"", "__MONOTONIC_TIMESTAMP": "40300000"},
    {"MESSAGE": "earlyoom 1.9.0", "__MONOTONIC_TIMESTAMP": "70000000"}
   ],
   "oomd_notices": 0
  },
  "expect": {
   "verdict": "KILLER_ACTED",
   "exit": 1,
   "fields": {
    "earlyoom.state": "inactive", "earlyoom.actions": null,
    "earlyoom.earlier_invocation_send_lines": 3, "oomd.state": "inactive",
    "oomd.notices_this_boot": 0
   }
  }
 },
 {
  "id": "a2-06-active-earlier-and-current-send-acted",
  "rule": "A2-06",
  "why": "A2-06 with an in-scope action as well, so the two counters are separated. The earlier invocation opened with its version line at 3000000 and sent SIGTERM at 3050000, which is outside the current invocation because the scope starts at ActiveEnterTimestampMonotonic = 8000000 (round-26 contract.md:78-79), so earlyoom.earlier_invocation_send_lines is 1. The SIGKILL at 8100000 is inside the scope and is one action of the kind `sending SIGKILL to process ` (round-26 contract.md:85, kill.c:627), so it is the in-scope positive evidence of round-26 contract.md:97 and the verdict is KILLER_ACTED exit 1; the earlier count is reported alongside it without changing the verdict, as A2-06 requires for an active earlyoom (round-26 contract.md:178-179). The out-of-scope send line is not counted into the actions block, so earlyoom.actions.sigterm is 0 while earlyoom.actions.sigkill is 1 (round-26 contract.md:94, the boundary frozen by c02). The current invocation opens with its version line at 8000000, exactly at ActiveEnterTimestampMonotonic, which is inside the scope (round-26 contract.md:78, the boundary frozen by c03), so scope_complete is true (round-26 contract.md:92-93), and both version lines read earlyoom 1.9.0 (main.c:161), so earlyoom.version is 1.9.0 and earlyoom.grammar is verified-1.9.0. The threshold lines are the main.c:414 and main.c:416 forms with PRIPCT \"%5.2lf%%\" (msg.h:10), so 20.00 and 15.00 render unpadded and 9.00 as \" 9.00%\"; both invocations print the same pair, so the four thresholds of round-26 contract.md:91-92 are 20.0/15.0/9.0/9.0 whichever invocation is read. No escalation, kill-failed or low-memory line is in scope, so those counts are 0 (round-26 contract.md:86-88, round-26 contract.md:94), and no dryrun line (round-26 contract.md:89) leaves earlyoom.dryrun false.",
  "inputs": {
   "earlyoom_show": "LoadState=loaded\nActiveState=active\nUnitFileState=enabled\nActiveEnterTimestampMonotonic=8000000\n",
   "oomd_show": "LoadState=loaded\nActiveState=inactive\nUnitFileState=disabled\nActiveEnterTimestampMonotonic=0\n",
   "earlyoom_journal": [
    {"MESSAGE": "earlyoom 1.9.0", "__MONOTONIC_TIMESTAMP": "3000000"}, {"MESSAGE": "sending SIGTERM when mem avail <= 20.00% and swap free <= 15.00%,", "__MONOTONIC_TIMESTAMP": "3000000"},
    {"MESSAGE": "        SIGKILL when mem avail <=  9.00% and swap free <=  9.00%", "__MONOTONIC_TIMESTAMP": "3000000"}, {"MESSAGE": "sending SIGTERM to process 90006 \"imaginary-baker\"", "__MONOTONIC_TIMESTAMP": "3050000"},
    {"MESSAGE": "earlyoom 1.9.0", "__MONOTONIC_TIMESTAMP": "8000000"}, {"MESSAGE": "sending SIGTERM when mem avail <= 20.00% and swap free <= 15.00%,", "__MONOTONIC_TIMESTAMP": "8000000"},
    {"MESSAGE": "        SIGKILL when mem avail <=  9.00% and swap free <=  9.00%", "__MONOTONIC_TIMESTAMP": "8000000"}, {"MESSAGE": "sending SIGKILL to process 90007 \"imaginary-compost\"", "__MONOTONIC_TIMESTAMP": "8100000"}
   ],
   "oomd_notices": 0
  },
  "expect": {
   "verdict": "KILLER_ACTED",
   "exit": 1,
   "fields": {
    "earlyoom.state": "active", "earlyoom.version": "1.9.0",
    "earlyoom.grammar": "verified-1.9.0", "earlyoom.thresholds.term_mem_pct": 20.0,
    "earlyoom.thresholds.term_swap_pct": 15.0, "earlyoom.thresholds.kill_mem_pct": 9.0,
    "earlyoom.thresholds.kill_swap_pct": 9.0, "earlyoom.scope_complete": true,
    "earlyoom.actions.sigterm": 0, "earlyoom.actions.sigkill": 1,
    "earlyoom.actions.escalations": 0, "earlyoom.actions.kill_failed": 0,
    "earlyoom.actions.low_memory_warnings": 0, "earlyoom.dryrun": false,
    "earlyoom.earlier_invocation_send_lines": 1, "oomd.state": "inactive",
    "oomd.notices_this_boot": 0
   }
  }
 }
]
```

## Derivation, case by case

### `a2-06-active-earlier-invocation-sends-quiet` — active earlyoom, earlier invocation acted, verdict unchanged

| field | expected | contract line that decides it |
|---|---|---|
| `earlyoom.earlier_invocation_send_lines` | 2 | A2-06 row round-27 `contract.md:54` + scope round-26 `contract.md:78-79`: both send lines (12100000, 12200000) are `< 64000000` = AETM, so both are outside the current invocation and both count |
| verdict / exit | `KILLERS_QUIET` / 0 | round-26 `contract.md:97` (positive evidence is an **in-scope** send/escalation line; none here), `:99-101` (not `KILLERS_UNKNOWN`: scope_complete true, grammar verified, no null read), `:102-103`; A2-06 for an active earlyoom changes no verdict, round-26 `contract.md:178-179`, the limit disclosed at `:171-172` and frozen by c02 (`cases.json:45-70`) |
| `earlyoom.state` | `active` | round-26 `contract.md:90-91` (state vocabulary) + show text `ActiveState=active`; c01 (`cases.json:8`) |
| `earlyoom.version`, `earlyoom.grammar` | `1.9.0`, `verified-1.9.0` | round-26 `contract.md:82`, `:91-92`; `main.c:161`; both version lines read `1.9.0`, so the value is independent of which invocation is read |
| `earlyoom.thresholds.*` | 12.5 / 12.5 / 6.25 / 6.25 | round-26 `contract.md:83-84` + `msg.h:10` (`PRIPCT "%5.2lf%%"`), `main.c:414`, `main.c:416`; both invocations print the same pair |
| `earlyoom.scope_complete` | true | round-26 `contract.md:92-93` (true only when the current invocation's version line is inside the scope) + `:78` (version line at 64000000 equals AETM, so inside), boundary frozen by c03 (`cases.json:72`) |
| `earlyoom.actions.*` (5 counts) | 0 / 0 / 0 / 0 / 0 | round-26 `contract.md:94` (in-scope action counts) + `:85-88`; no send, escalation, kill-failed or low-memory line is in scope |
| `earlyoom.dryrun` | false | round-26 `contract.md:89` (flag set only by `dryrun mode enabled`); no such line |
| `oomd.state`, `oomd.notices_this_boot` | `inactive`, 0 | round-26 `contract.md:95`, `:102-103`; oomd show text `ActiveState=inactive`, `oomd_notices` 0 |

### `a2-06-inactive-earlier-invocation-sends-acted` — not-active earlyoom, non-zero count is positive evidence

| field | expected | contract line that decides it |
|---|---|---|
| `earlyoom.earlier_invocation_send_lines` | 3 | A2-06 row round-27 `contract.md:54` + round-26 `contract.md:176-177` ("send and escalation lines of this boot outside the current invocation"); all three send lines (40100000, 40200000, 40300000) are `< 70000000` = AETM (`:78-79`) and belong to the invocation opened at 40000000 |
| verdict / exit | `KILLER_ACTED` / 1 | A2-06 non-active branch, round-26 `contract.md:177-178` ("a non-zero count is positive evidence (`KILLER_ACTED`; a stop without restart no longer reads quiet)"); exit code from `:96-98` |
| `earlyoom.state` | `inactive` | round-26 `contract.md:90-91`; `ActiveState=inactive`; frozen by c06 (`cases.json:145`) |
| `earlyoom.actions` | `null` | round-26 `contract.md:102-103` ("An inactive or absent killer reports `actions: null` (unavailable), never zero counts"); frozen by c06 |
| `oomd.state`, `oomd.notices_this_boot` | `inactive`, 0 | round-26 `contract.md:95`, `:102-103` |
| **not pinned** | — | `earlyoom.version`, `earlyoom.grammar`, `earlyoom.thresholds.*`, `earlyoom.scope_complete`, `earlyoom.dryrun`: with an inactive unit the contract fixes only the field names (`contract.md:90-95`), and the frozen inactive case c06 pins none of them, so the text does not decide their values here |

### `a2-06-active-earlier-and-current-send-acted` — active earlyoom, both counters exercised

| field | expected | contract line that decides it |
|---|---|---|
| `earlyoom.earlier_invocation_send_lines` | 1 | A2-06 row round-27 `contract.md:54` + scope round-26 `contract.md:78-79`: only the send line at 3050000 is `< 8000000` = AETM; the send line at 8100000 is in scope and does not count here |
| `earlyoom.actions.sigterm` | 0 | round-26 `contract.md:94` (in-scope counts only) + `:78-79`; the SIGTERM at 3050000 is out of scope, exactly the boundary frozen by c02 (`cases.json:45-70`, sigterm 0 for a line one microsecond before AETM) |
| `earlyoom.actions.sigkill` | 1 | round-26 `contract.md:85` (`sending SIGKILL to process `), `kill.c:627`; the line at 8100000 is in scope |
| `earlyoom.actions.escalations`, `.kill_failed`, `.low_memory_warnings` | 0, 0, 0 | round-26 `contract.md:86-88`, `:94`; no such line exists in the journal |
| verdict / exit | `KILLER_ACTED` / 1 | round-26 `contract.md:96-98` (in-scope send line is positive evidence; exit 1). The earlier count does not alter it: A2-06 for an active earlyoom, round-26 `contract.md:178-179` |
| `earlyoom.state` | `active` | round-26 `contract.md:90-91` |
| `earlyoom.version`, `earlyoom.grammar` | `1.9.0`, `verified-1.9.0` | round-26 `contract.md:82`, `:91-92`; `main.c:161`; both version lines read `1.9.0` |
| `earlyoom.thresholds.*` | 20.0 / 15.0 / 9.0 / 9.0 | round-26 `contract.md:83-84` + `msg.h:10`, `main.c:414`, `main.c:416`; both invocations print the same pair |
| `earlyoom.scope_complete` | true | round-26 `contract.md:92-93` + `:78`; the current invocation's version line at 8000000 equals AETM, boundary frozen by c03 (`cases.json:72`) |
| `earlyoom.dryrun` | false | round-26 `contract.md:89`; no dryrun line |
| `oomd.state`, `oomd.notices_this_boot` | `inactive`, 0 | round-26 `contract.md:95`, `:102-103` |

## Deliberate design choices (so the L1 can audit them)

1. **The current invocation's version line is stamped exactly at `ActiveEnterTimestampMonotonic`** in all three cases
   (64000000, 70000000, 8000000). The contract fixes the scope by timestamp (`contract.md:78-79`) but does not fix how
   "the current invocation" is delimited when the journal holds several invocations, and A2-07 (`round-27
   contract.md:55`) shows the tool splits invocations at version lines. Aligning the two readings makes every plausible
   delimitation agree on the same count, so no pinned value depends on that gap.
2. **Both invocations in cases 1 and 3 print the same threshold pair and the same version string.** The contract decides
   `earlyoom.version`, `earlyoom.grammar` and the thresholds from whichever invocation the reader takes; making the two
   invocations agree removes the ambiguity instead of betting on one reading.
3. **No escalation line and no `dryrun mode enabled` line appears in any case.** round-27 `contract.md:54` says the
   out-of-invocation field counts "send lines", while round-26 `contract.md:176-177` says "send and escalation lines";
   the two texts differ, so a case pinning an escalation-inclusive count would be decided by wording, not by rule. The
   same holds for the A2-07 per-invocation dry-run split (`round-27 contract.md:55`), so dry-run is left out.
4. **Process names and pid-like numbers are invented** (`imaginary-bellows`, `imaginary-lathe`, `imaginary-sifter`,
   `imaginary-ploughman`, `imaginary-mason`, `imaginary-baker`, `imaginary-compost`; numbers 90001-90007), following the
   frozen file's convention of dropping the uid and cmdline parts of the kill.c:627 format (c02, `cases.json:45-70`).
   No uid, pid, slice, unit name or `earlyoom` configuration value of this host appears anywhere.
5. **Case 2 keeps `earlyoom_show` at `ActiveState=inactive` with a non-zero `ActiveEnterTimestampMonotonic`**, which is
   what `systemctl show` reports for a unit that was active earlier in the boot and is now stopped, keeping the count
   decided by the same scope rule as the active cases.

## Blindness statement and the files I opened

**I did not open, grep, cat or run `tools/mori-oom-killers.py`, nor any copy of it. I did not open
`.ufo/waves/round-26/evidence/`, nor `.ufo/waves/round-26/w1`, `.ufo/waves/round-26/w2`, `.ufo/waves/round-27/w1` or
`.ufo/waves/round-27/w2`. I ran no self-test and no counter.** Every expected value above is derived from the rule text
(round-27 `contract.md:54`, round-26 `contract.md:152-200`), the round-26 output/verdict spec (`:66-119`), the frozen
round-26 case file (schema and precedent), and the upstream earlyoom v1.9.0 format strings.

Files opened, all read-only:

- `.ufo/waves/round-27/contract.md` lines 40-80 (rule table).
- `.ufo/waves/round-26/contract.md`, whole file (spec + amendment A2).
- `tools/fixtures/mori-oom-killers/cases.json` (schema, journal line shapes, and the frozen cases c01-c08, c15-c17, c29
  used as precedent).
- `.ufo/waves/round-28/contract.md` lines 29-113 and `.ufo/waves/round-28/wave1-spec.json` (my own seat entry and the
  C2 counter's stated requirements).
- `/home/vgpnk/.omp/agent/RULES.md` (tooling directive).
- Upstream, fetched by curl to my scratch dir (URL, access time UTC, sha256 of the bytes):
  - `https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/kill.c` — 2026-10-22T17:59:25Z,
    sha256 `b32e0fad65e298235102f98aff37e02c94400b544d454cb57192ae697b100bf3`.
    Quote, kill.c:627 — `warn("sending %s to process %d uid %d \"%s\": oom_score %d, oom_score_adj %d, VmRSS %lld MiB, cmdline \"%s\"\n",`
    Quote, kill.c:318 — `warn("escalating to SIGKILL after %.3f seconds\n", secs);`
    Quote, kill.c:282 — `warn("killing whole process group %d (-g flag is active)\n", res);`
  - `https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/main.c` — 2026-10-22T17:59:25Z,
    sha256 `08656b0bc90c85f23738661456b25c97af908bc5e2cfea78e0a69697b5f9d0e4`.
    Quote, main.c:161 — `fprintf(stderr, "earlyoom " VERSION "\n");`
    Quote, main.c:414 — `fprintf(stderr, "sending SIGTERM when mem avail <= " PRIPCT " and swap free <= " PRIPCT ",\n",`
    Quote, main.c:416 — `fprintf(stderr, "        SIGKILL when mem avail <= " PRIPCT " and swap free <= " PRIPCT "\n",`
    Quote, main.c:295 — `warn("dryrun mode enabled, will not kill anything\n");`
  - `https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/msg.h` — 2026-10-22T17:59:25Z,
    sha256 `e36604984a916fb00a624c27c73034bcd87d7d6facff9b290a6a561ee58de56c`.
    Quote, msg.h:10 — `#define PRIPCT "%5.2lf%%"`
  - `https://raw.githubusercontent.com/systemd/systemd/v262/src/core/unit.c` — 2026-10-22T18:04:02Z, sha256
    `47e98d394462e05bf4bc0be2d1105fa8c21044cc9f5ebf00464f1742a92efcb7`, and
    `https://raw.githubusercontent.com/systemd/systemd/v262/src/core/dbus-unit.c` — 2026-10-22T18:12:15Z, sha256
    `47f461aeb70722ae7fb02f9b89ffd12db1639b7750a02e218dc27747f4cd9d0d`. These two are outside the task's read list: I
    opened them only to check how systemd maintains `ActiveEnterTimestampMonotonic` for a unit no longer active, and
    **no expected value in the cases above depends on them**. Disclosed for completeness.
  - No bot challenge was encountered or passed; these are plain raw file downloads.

## Checks actually run (all on my own scratch files; none on the lane, no self-test)

- `python3 -c 'import json,sys;json.load(sys.stdin)' < cases-a2-06.json` → exit 0 (`JSON_OK`).
- Structural assertions over the parsed array: exactly the keys `id, rule, why, inputs, expect`; `rule == "A2-06"`; ids
  match `a2-06-<slug>` and are printable ASCII; `expect.exit` is an integer and not a bool; every journal record has
  exactly `MESSAGE` and `__MONOTONIC_TIMESTAMP`, the latter all-digit; the three `inputs` objects are pairwise distinct;
  every case pins `earlyoom.earlier_invocation_send_lines`.
- Scope re-derivation from the contract's own rule (`ts >= AETM`): out-of-scope send counts 2, 3, 1 — equal to the pinned
  `earlyoom.earlier_invocation_send_lines` in all three cases; in-scope send counts 0, 0, 1.
- Byte-exact re-rendering of every threshold line from `PRIPCT "%5.2lf%%"` matched all eight threshold records; every
  `MESSAGE` matched one of the upstream prefixes, and no message carries a uid, cmdline or oom_score.
- The JSON block embedded in this report parses and is identical to the scratch array (verified by extracting the fenced
  block and comparing to `cases-a2-06.json`). Journal timestamps are chronological in all three cases.

## Risks for the L1

- The two rule texts disagree on whether an out-of-invocation **escalation** line counts toward
  `earlyoom.earlier_invocation_send_lines` (round-27 `contract.md:54` "send lines" vs round-26 `contract.md:176-177`
  "send and escalation lines"). My cases contain no escalation line, so the pinned counts hold under either reading; if
  the tool counts escalations too, none of my cases distinguishes it and a further case would be needed to pin it.
- The contract does not say how "the current invocation" is delimited when the journal holds several invocations (A2-07,
  round-27 `contract.md:55`, shows a version-line split). My cases align the version line with
  `ActiveEnterTimestampMonotonic` so the count is the same under a timestamp reading and a version-line reading.
- For an inactive earlyoom the contract does not decide `earlyoom.version`, `earlyoom.grammar`,
  `earlyoom.thresholds`, `earlyoom.scope_complete` or `earlyoom.dryrun`; I left those five unpinned in case 2, as the
  frozen inactive case c06 does.
- If the tool reports a different value for `earlyoom.actions` on an inactive unit than `null`, case 2 would fail on
  that one field; the count and the verdict are the parts A2-06 decides.
