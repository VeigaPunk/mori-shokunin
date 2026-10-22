# mori round 26 — claim contract (attempt 1, L1 MoriR26)

Entering tip `248408f5b6610a85bcbdebe7ac0b4fa7ed51422a` (round 25 admitted, `MANIFEST.json` rounds[455]).
Written before any round-26 implementation. Targets, not results.

## Frontier area and why

Rounds 23–25 each counted a routed repair on calibration (the drift sentinel in the round-25
spot-check). This round works a different frontier area: **FR10, userspace OOM killers**
(`PROVINCE.md:53`). The admitted entry `corpus/knowledge/userspace-oom-killers-r12.md` says, in the
present tense, that both userspace killers are inactive on this host. On 2026-10-22 a read-only
check shows `earlyoom.service` active and enabled (earlyoom 1.9.0, Arch package `earlyoom 1.9.0-1`)
and `systemd-oomd.service` inactive and disabled (systemd 262). The admitted knowledge is stale, and
mori has no tool that reads what earlyoom is set to do or whether it has acted.

Routed round-25 defects R1–R8 (`corpus/lessons/round-25-verifier-spotcheck.md:172-202`) are hygiene
or named debt this round, never a counted claim.

## C1 — freshness (score 5, tied lowest active axis): supersede the stale FR10 host-state entry

Statement: four enumerated present-tense statements that this host's userspace killers are inactive
(list below) contradict the committed round-26 capture; at the landed tip none of the four phrases
remains, and a superseding entry `corpus/knowledge/userspace-oom-killers-r26.md` exists whose
`source:` line cites at least one `corpus/SOURCES.md` row opened in round 26.

Frozen list (file → exact phrase, fixed-string match):

| Id | File | Phrase |
|---|---|---|
| F1 | `corpus/knowledge/userspace-oom-killers-r12.md` | `On this host both services are inactive` |
| F2 | `corpus/knowledge/userspace-oom-killers-r12.md` | `` `systemctl is-active earlyoom.service` → `inactive` `` |
| F3 | `corpus/knowledge/userspace-oom-killers-r12.md` | `Both service units are inactive` |
| F4 | `corpus/README.md` | `inactive on this host` |

Counting command (one command over committed bytes; `R` is a revision):

```sh
R=<rev>; n=0; while IFS='|' read -r f p; do git -C /home/vgpnk/Projects/shokunin/mori-shokunin grep -q -F "$p" "$R" -- "$f" && n=$((n+1)); done < .ufo/waves/round-26/c1-phrases.txt; echo "stale_present=$n"; git -C /home/vgpnk/Projects/shokunin/mori-shokunin cat-file -e "$R:corpus/knowledge/userspace-oom-killers-r26.md" && echo r26_entry=present || echo r26_entry=absent
```

`c1-phrases.txt` holds the four `file|phrase` lines above and is frozen with this contract.
Before (at `248408f5`): `stale_present=4`, `r26_entry=absent`. Declared after (at the landed tip):
`stale_present=0`, `r26_entry=present`. The stale lines are rewritten as dated past-tense records that
name the superseding entry; they are not shadowed by a banner (QUALITY 77).

Not claimed by C1: any statement about other entries, any host-wide unit census, any kill history.

## C2 — coverage (score 6): userspace OOM killer read capability (FR10 → Core, bounded)

New read-only tool `tools/mori-oom-killers.py`, Python 3 standard library only, runs under
`python3 -I -B`. Statement: the tool passes N/N frozen cases, where the cases file
`tools/fixtures/mori-oom-killers/cases.json` is written by a seat other than the tool seat and is
committed before the tool's first commit, and N = `jq '.cases|length'` of that file at its freeze
commit (N ≥ 20). Before: `git cat-file -e 248408f5:tools/mori-oom-killers.py` exits 128. Declared
after: `python3 -I -B tools/mori-oom-killers.py --selftest` prints
`MORI_OOM_KILLERS_SELFTEST: PASS N/N` and exits 0 at the landed tip.

### Interface (binding on the tool seat and the case seat)

- `--inputs FILE`: run the pure reader on one JSON inputs object (shape below), print one JSON result
  object, exit with the verdict code. `--selftest [--cases FILE]`: run every case through the same pure
  function; default cases path resolved from the script location; an empty or missing cases file is a
  setup error (exit 2), never a silent fall-back. No arguments: collect the inputs object live
  (commands below), then run the same pure function. `--dump-inputs`: print the live inputs object
  (for receipts) without the reader.
- Inputs object:
  ```json
  {"earlyoom_show": "<text of systemctl show earlyoom.service -p LoadState,ActiveState,UnitFileState,ActiveEnterTimestampMonotonic>" | null,
   "oomd_show": "<same four properties for systemd-oomd.service>" | null,
   "earlyoom_journal": [{"MESSAGE": "...", "__MONOTONIC_TIMESTAMP": "<usec>"}] | null,
   "oomd_notices": <int> | null}
  ```
  `null` means the read failed. Live collection: `systemctl show <unit> -p ...`;
  `journalctl -q -b -u earlyoom.service -o json --output-fields=MESSAGE` (keep `MESSAGE` and
  `__MONOTONIC_TIMESTAMP` only, in memory); `journalctl -q -b MESSAGE_ID=d989611b15e44c9dbf31e3c81256e4ed -o json --output-fields=MESSAGE_ID`
  line count for `oomd_notices`. A `MESSAGE` that is a byte array in journal JSON is decoded as UTF-8
  with replacement.
- Scope: earlyoom lines whose `__MONOTONIC_TIMESTAMP` ≥ `ActiveEnterTimestampMonotonic` of the
  current earlyoom invocation, in the current boot.
- Message grammar (earlyoom 1.9.0, `main.c`/`kill.c` at tag `v1.9.0`), matched after stripping
  leading whitespace, prefix-anchored:
  - `earlyoom <version>` → version (the first line of an invocation; `main.c:161`)
  - `sending SIGTERM when mem avail <= <a>% and swap free <= <b>%,` → term thresholds (`main.c:414`)
  - `SIGKILL when mem avail <= <c>% and swap free <= <d>%` → kill thresholds (`main.c:416`)
  - `sending SIGTERM to process ` / `sending SIGKILL to process ` → one action each (`kill.c:627`)
  - `escalating to SIGKILL after ` → escalation (`kill.c:318`)
  - `kill failed: ` → failed kill (`kill.c:654`)
  - `low memory! at or below SIGTERM limits` / `... SIGKILL limits` → low-memory warning (`main.c:519-523`)
  - `dryrun mode enabled` → dry-run flag (`main.c:295`)
- Output (`schema: mori-oom-killers-v1`): `earlyoom` {`state` (`active`, `inactive`, `absent`,
  `unavailable`), `version`, `grammar` (`verified-1.9.0` or `unverified`), `thresholds`
  {`term_mem_pct`, `term_swap_pct`, `kill_mem_pct`, `kill_swap_pct`} or null, `scope_complete` (true
  only when the version line of the current invocation is inside the scope), `actions`
  {`sigterm`, `sigkill`, `escalations`, `kill_failed`, `low_memory_warnings`} or null, `dryrun`},
  `oomd` {`state`, `notices_this_boot` or null}, `verdict`.
- Verdicts and exits:
  1. `KILLER_ACTED`, exit 1: any earlyoom `sending SIG…to process` or escalation line in scope, or
     `oomd_notices` > 0. Positive evidence stands even when the scope is incomplete.
  2. `KILLERS_UNKNOWN`, exit 2: no positive evidence, and any of: a needed read is `null`; earlyoom
     active but `scope_complete` false; earlyoom active and `grammar` `unverified`; a show text that
     lacks `ActiveState`.
  3. `KILLERS_QUIET`, exit 0: otherwise. An inactive or absent killer reports `actions: null`
     (unavailable), never zero counts; quiet then means "no positive evidence from the killers that are
     readable", and the output names which killers were unavailable.
  4. Setup or internal error: exit 2 with `verdict: KILLERS_UNKNOWN` and an `error` field; an
     uncaught exception never exits 1.
- Privacy: the tool never prints `MESSAGE` text, process names, command lines, uids or the
  `--avoid`/`--prefer` expressions; output holds states, numbers, the version string and counts.
- Read-only: no writes outside stdout/stderr, no unit or journal changes, no network.

### Case file (written by the case seat, frozen before the tool)

`tools/fixtures/mori-oom-killers/cases.json`: `{"schema": "mori-oom-killers-cases-v1", "cases":
[{"id", "why", "inputs", "expect": {"verdict", "exit", "fields": {<dotted path>: <value>}}}]}`.
The cases cover each verdict rule, each grammar line, the scope boundary (a line one microsecond
before and at `ActiveEnterTimestampMonotonic`), an incomplete scope with and without actions, an
inactive and an absent earlyoom, a `null` journal, an unverified version, oomd notices, a byte-array
`MESSAGE`, and the host-shaped quiet case (thresholds 10.00/10.00/5.00/5.00). Case `MESSAGE` text uses
invented process names only.

## Held, not claimed

operability 7, depth 5, calibration 5, adjacency 6. No retirement, waiver, exploratory claim or
promotion. No-harm check: the lane retention scan (R8) is run at the entering tip and at every
candidate tip; its value at the landed tip must not exceed the entering value.

## Amendment A1 (2026-10-22, before any C1 after-measurement; after the C2 tool's first selftest result)

Reason: wave-1 seat CriticLearningRules (`.ufo/waves/round-26/w1/CriticLearningRules.md`) showed the C1 command
above reads the phrase list from the working tree (run from the fleet root it prints `stale_present=0` at the
entering tip), counts a bad revision or a deleted file as fixed, does not fold whitespace (QUALITY 77), and cannot
see the sourced-claim clause. The counters are now committed scripts that read committed bytes only.

- **C1 counter:** `bash .ufo/waves/round-26/count-c1.sh <rev>` (phrase list read from `28b04940`; bad revision,
  missing file or short list exit 2; whitespace folded, emphasis removed). Before at `248408f5`:
  `stale_present=4`, `r26_entry=absent`, `r26_new_source_ids=0`, `r12_names_r26=0`. Declared after at the
  landed tip: `stale_present=0`, `r26_entry=present`, `r26_new_source_ids` ≥ 1 (S ids above S113, the last row
  at the entering tip, are rows opened in round 26), `r12_names_r26` ≥ 1.
- **C2 counter:** `bash .ufo/waves/round-26/count-c2.sh <rev>` (runs the tool from a `git archive` of the
  revision; checks the case file's first commit is a strict ancestor of the tool's first commit and that the case
  file is unchanged since). Declared after: `freeze_order=ok`, `cases_changed_since_freeze=0`, `N=32`,
  `MORI_OOM_KILLERS_SELFTEST: PASS 32/32`, `exit=0`. Before at `248408f5`: `absent`, exit 2. Also added to C2's
  after-state: a `### capabilities: first demonstrated round 26` row in SCORECARD and the committed live-run
  receipt `.ufo/waves/round-26/evidence/c2-live-run.txt`. Timing disclosed: the case count (32) and the tool's
  PASS 32/32 were known when this amendment was written; the amendment fixes N to the frozen count and tightens,
  never widens, the after-state.
- Seat independence (cases by WriteOomKillersCases, tool by BuildOomKillersTool, built blind) is a process fact
  with pointers to their wave-1 reports, not part of the counted value.
- Uncounted correction rows (QUALITY 77 sweep, not on the frozen list): r12 line 14 `not-found` and line 18
  "earlyoom's service unit is not found" are rewritten as dated records in the same change.

## Amendment A2 (2026-10-22, after the tool landed; tool rules only, counted value unchanged)

Reason: wave-1 seat CriticC2Width (`.ufo/waves/round-26/w1/CriticC2Width.md:40-155`) ran nine counterexamples
X1–X9 against the tool. The frozen cases stay frozen; the L1 changed the tool where a rule does not contradict a
frozen case, and discloses the rest as limits. The counted value stays `PASS 32/32` on the frozen file.

- **A1b (adopted):** a journald `Suppressed N messages from earlyoom.service` line in scope sets
  `scope_complete` false (X3 now `KILLERS_UNKNOWN`).
- **A1c (adopted, live mode only):** journal reads count as `null` unless `journalctl -q -b -n 1 _PID=1` returns
  a record (X9's unreadable-journal path in live mode).
- **A2b (adopted):** an `ActiveState` other than `active` or `inactive` (failed, activating, deactivating,
  reloading, maintenance) maps to state `unavailable` and `KILLERS_UNKNOWN` (X5, X6).
- **A5 (adopted):** `killing whole process group ` lines are counted in `earlyoom.process_group_lines`; every count
  is a count of earlyoom log lines, not of processes signalled or killed (X2).
- **A6 (adopted):** when the invocation logged `dryrun mode enabled`, send lines go to
  `earlyoom.dryrun_send_lines`, `sigterm`/`sigkill` stay 0 and they are never positive evidence (X1).
- **Malformed timestamp (adopted, from the case seat's supplementary c35):** a journal record without a numeric
  `__MONOTONIC_TIMESTAMP` is a setup error: `KILLERS_UNKNOWN`, exit 2.
- **Not adopted (each contradicts a frozen case), disclosed as limits:** A1a (counts with an incomplete scope are
  lower bounds printed as counts; frozen `c04`), A2a (lines of an earlier invocation in the same boot are not seen;
  frozen `c02`, X4), A3 (no logger-heartbeat check; frozen `c19`, X7), X8 (head-truncated count is a lower bound).
- **Unbounded invocation (adopted, from wave-1 SrcJournalJson F2):** `ActiveEnterTimestampMonotonic` missing or `0`
  leaves the invocation unbounded, so `scope_complete` is false (before this, a version line alone set it true).
- **Earlier invocations (partly adopted, from wave-1 ReviewScopeClock S1/S2):** a new field
  `earlyoom.earlier_invocation_send_lines` counts send and escalation lines of this boot outside the current
  invocation. For an earlyoom that is not active, a non-zero count is positive evidence (`KILLER_ACTED`; a stop
  without restart no longer reads quiet). For an active earlyoom it is reported but does not change the verdict,
  because frozen `c02` pins `KILLERS_QUIET` for that shape; that limit stays disclosed (A2a above).
- **Wave-2 fixes (CriticCapabilityRow Y1, Y3, Y8):** dry-run is now applied per earlier invocation (split at each
  version line), so one dry-run invocation no longer zeroes the real sends of another; a `null` journal reads
  `KILLERS_UNKNOWN` for any earlyoom state; send lines of a removed (`not-found`) unit this boot are positive
  evidence. Detector inputs and their outputs: `.ufo/waves/round-26/evidence/a2-detectors/` and
  `a2-detectors.txt` (invented inputs from wave-2 MutPostFreezeRules and CriticCapabilityRow). No committed case
  file pins these rules; the counted value stays `PASS 32/32` on the frozen file.
