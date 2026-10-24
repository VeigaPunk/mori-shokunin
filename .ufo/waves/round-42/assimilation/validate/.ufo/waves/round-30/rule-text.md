# Round-30 rule text for blind case writers (verbatim extract at lane 58b61681a0e3f3b821a17d38a4e713ccd9921615)

Extract of `.ufo/waves/round-26/contract.md:58-110` (interface, grammar, output, verdicts):

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


Extract of `.ufo/waves/round-26/contract.md:152-190` (amendment A2):

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
- **Wave-2 fix (CriticA2Amendment D1):** a journal record without a numeric `__MONOTONIC_TIMESTAMP` is now left
  uncounted and makes the scope incomplete, instead of a setup error; positive evidence elsewhere still stands. The
  earlier setup-error rule (commit `278f02e4`, recorded in A2 at `825f988f`) is superseded. Commit order of the A2
  bullets: suppressed, non-steady, process-group, dry-run, readability `825f988f`; unbounded invocation `93aa1b93`;
  earlier invocations `738eec13`; wave-2 fixes `f1efb465` and this commit.

Extract of `.ufo/waves/round-27/contract.md:47-58` (rule table):

| Id | Rule (as adopted in round-26 amendment A2) |
|---|---|
| A2-01 | a journald `Suppressed N messages from earlyoom.service` line in scope sets `scope_complete` false |
| A2-02 | an earlyoom `ActiveState` other than `active` or `inactive` maps to state `unavailable` and `KILLERS_UNKNOWN` |
| A2-03 | `killing whole process group ` lines are counted in `earlyoom.process_group_lines` |
| A2-04 | after `dryrun mode enabled`, send lines go to `earlyoom.dryrun_send_lines`, `sigterm`/`sigkill` stay 0, never positive evidence |
| A2-05 | `ActiveEnterTimestampMonotonic` missing or `0` leaves the invocation unbounded: `scope_complete` false |
| A2-06 | send lines of this boot outside the current invocation go to `earlyoom.earlier_invocation_send_lines`; non-zero is positive evidence (`KILLER_ACTED`) for an earlyoom that is not active, reported without a verdict change for an active one |
| A2-07 | dry-run applies per invocation (split at each version line): one dry-run invocation does not zero another invocation's real sends |
| A2-08 | a `null` earlyoom journal reads `KILLERS_UNKNOWN` for any earlyoom state |
| A2-09 | send lines of a removed (`not-found`) earlyoom unit this boot are positive evidence |
| A2-10 | a journal record without a numeric `__MONOTONIC_TIMESTAMP` is left uncounted and makes the scope incomplete; positive evidence elsewhere still stands |
