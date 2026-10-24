# CensusRepair — r14 C1 coverage repair (owner: tools/mori-census.sh)

Milestone: restore OOM alarm and structured fleet routing.
Changed file: `tools/mori-census.sh` (only). No other production, frozen, MANIFEST,
SHONEN, verifier-harness or sibling file was written. No tool installs/upgrades.
No build/test/lint/smoke run was executed by this seat; L1 owns post-integration
verification (wave contract).

## Final interface (implemented; matches L1 ruling relayed during the wave)

SURFACE `journal.user` / `journal.system` keep the six r13 counts in order:
`kernel_oom_notice oomd_notice coredump_notice segfault_signal11 unit_sigkill_record
unit_failure_record`, then append validated integer splits:
`unit_fleet unit_nonfleet unit_unknown unit_missing unit_ambiguous unit_malformed
unit_oom unit_oom_fleet unit_oom_nonfleet unit_oom_subject_unknown unit_oom_result_unknown
unit_signal`.
Invariants: `fleet+nonfleet+unknown == unit_failure_record`; `unit_oom` and
`unit_signal` are subsets of it. When the unit query is unavailable every added
token reads `unavailable:<same status>` (never 0). Six-count predicates and their
argv match words are unchanged; no query asks for MESSAGE.

Findings:
- `OOM_KILL_JOURNAL` severity=crit — EXACTLY ONE global line per census when any of
  `user_notice`, `system_notice`, `user_unit_oom`, `system_unit_oom` is a positive
  integer. Fields appear once, are never summed, and each numeric field is
  byte-equal to that scope's SURFACE token (`kernel_oom_notice` / `unit_oom`); an
  unavailable source carries `unavailable:<reason>`. No `count=` token on this
  line. Drift counts this alarm line (emit_finding once), not records or kills.
  Sources: kernel-OOM unit notice `fe6faa94…` in either scope; `UNIT_RESULT=oom-kill`
  in either scope, independent of subject classification. Wording says kernel OOM
  or systemd-oomd (unit.c `unit_log_failure`; both callers).
- `UNIT_FAILURE_JOURNAL` (user) / `UNIT_FAILURE_JOURNAL_SYSTEM` (system), info:
  fleet-only, `subject=fleet owner=mori classification_rule=unit-name-token`.
- `UNIT_FAILURE_OUT_OF_SCOPE` / `_SYSTEM`, info: `subject=nonfleet owner=tsukuroi`;
  "no marker" is a routing hint, not proof of non-fleet ownership.
- `UNIT_FAILURE_UNATTRIBUTED_JOURNAL`, info: ONE literal id in BOTH scopes,
  `scope=user|system count=N missing/ambiguous/malformed owner=unresolved
  reason=subject-metadata-unknown`; raw `unit_failure_record` count retained.
- `KILL_SIGNAL_JOURNAL` warn (user only): fires when the user unit-process SIGKILL
  record count > 0 OR the user unit-failure `UNIT_RESULT=signal` count > 0;
  `count=`/`process_sigkill=` keep the process-record count and `user_unit_signal=`
  the result count, separate and never summed. System signal results stay info/no
  warn. SIGKILL note now says "cause unknown (a kernel OOM can also deliver SIGKILL)".
- Unchanged: `OOMD_NOTICE_JOURNAL_*`, `COREDUMP_NOTICE_JOURNAL_*`,
  `SEGFAULT_SIGNAL11_JOURNAL_*` (info), `KILL_SIGNAL_JOURNAL_SYSTEM` (info).
  Retired ids: `KERNEL_OOM_NOTICE_JOURNAL_USER`, `KERNEL_OOM_NOTICE_JOURNAL_SYSTEM`.

Query/partition: the existing `MESSAGE_ID=d9b373ed…` query now requests
`_BOOT_ID,MESSAGE_ID,UNIT,USER_UNIT,UNIT_RESULT` and splits ONE record set in ONE
jq pass (no second scan, no new stub slot; the fixture dispatcher still routes by
MESSAGE_ID). Subject = exactly one of `UNIT`/`USER_UNIT` present (`has()` presence,
scope-independent; USER_UNIT may legitimately appear in the system journal); both
present (even equal), neither, non-string, >255 chars, wrong charset or missing
unit suffix -> unknown, never non-fleet. Valid names are 1..255 over the ASCII
safe set `[A-Za-z0-9_.:@-]` plus ONLY literal `\xHH` escape sequences — a bare
backslash or an illegal escape (`\q`) is malformed, not a subject.
`_SYSTEMD_*` are the emitter and are never read. Fleet marker set is the frozen
r12 literal
`shokunin|ufo-sighting|tmux-spawn|the-tick|fleet`, case-insensitive substring on the
subject name only, passed as a fixed `--arg` (no env/roster interpolation). Only
integer aggregates and the validated 32-hex boot id are printed; unit/result bytes
never reach a row or finding.

`journal_query` now checks the exact column count and `is_int` on every count
column before accepting a row (legacy 3-column filters unchanged; unit vector is
15 columns). New integer keys were added to `DRIFT_COUNTER_KEYS`
(`user_notice system_notice user_unit_oom* system_unit_oom* unit_fleet … unit_signal
user_unit_signal process_sigkill`).

Unmeasured reasons corrected: `JOURNAL_CLASSES_UNMEASURED` and the SURFACE row now
separate `kernel_victim_text/text-heuristic-retired`, `gpf_text/text-heuristic-retired`,
`other_signals/structured-field-unimplemented` (EXIT_CODE/EXIT_STATUS exist per
S036; only EXIT_STATUS=9 implemented) and `uncataloged_unit_failure/text-heuristic-retired`,
plus `absent_records=possible:no-retained-record-is-not-no-event`. No categorical
"no anchored structured field" claim remains. Comment corrections from Main's
source review: the historical 5-vs-7/9 figure is labeled a MESSAGE-selected text
sample (round-12 M19 / r13 errata), not a victim census; the OOM alarm and user
KILL_SIGNAL warn are documented as single global lines while routing is per
scope; and `oom`/`signal` are documented as mutually exclusive result subsets
that overlap the fleet/non-fleet/unknown subject buckets.

## Evidence retained

- `corpus/lessons/round-13-verifier-spotcheck.md` (read in full): :72–89 OOM alarm
  loss and :86–88 fleet/non-fleet/owner loss + overbroad unmeasured reason;
  :130–137 routed defects.
- Frozen r12 journal probe `.ufo/waves/round-13/frozen/mori-census.sh:861-911`:
  crit OOM on positive text, UNIT_FAILURE_JOURNAL info fleet-only (:904-905),
  UNIT_FAILURE_OUT_OF_SCOPE info owner tsukuroi (:908), marker set (:891).
- Pinned systemd `cf8ebfc6`: `src/core/unit.c:6333-6342` `unit_log_failure` emits
  `UNIT_RESULT`; `src/basic/log.c:1613-1614` `UNIT=` only for PID 1 / `USER_UNIT=`
  otherwise; current `systemd.journal-fields` “UNIT=, USER_UNIT=” names the unit a
  manager logs about, `_SYSTEMD_UNIT` describes the emitter (S015).
- Standalone jaq filter simulation (not a census run) over 8 synthetic d9b373ed
  records: `8 2 1 5 1 2 2 2 1 0 1 1 1 <boot>` = total 8, fleet 2, nonfleet 1,
  unknown 5 (missing 1, ambiguous 2, malformed 2), oom 2 (fleet 1, unknown 1),
  result-unknown 1. Covered: either valid field, both fields equal, null+valid,
  escaped `\x2d` name, no suffix, space-bearing name, array UNIT_RESULT.
- Charset tightening (Main source-review follow-up): standalone jaq check of
  `^([A-Za-z0-9_.:@-]|\\x[0-9A-Fa-f]{2})+$`: `kagi-shokunin.service`,
  `app-Hyprland-xdg\x2dterminal\x2dexec-dd9e67bd.scope`, `x\x2d.service`,
  `a@b.service`, `a:b.slice` valid; `x\qy.service`, `x\xZZ.service`, `bad name.service`,
  `shokunin` (no suffix) invalid. The filter therefore no longer accepts an
  arbitrary backslash.
- Bash semantics checks: prefixed assignment is visible inside a function
  (`in=15` then `in=3`); a 15-column tab vector parses to 15 fields including
  `boots=0 boot=none`.
- Selftest added/updated (code only; not executed here): the matrix now fills all
  TWELVE scoped cells (6 classes × user/system nonzero) and expects the single OOM
  crit line with `user_notice=3 system_notice=5`, no `count=`, each OOM field
  exactly once, both OOMD/COREDUMP/SEGFAULT/SIGKILL findings per scope, the user
  SIGKILL warn, the system fleet route, and `UNIT_FAILURE_UNATTRIBUTED_JOURNAL`.
  Per ScopedFixtures' live observation (user manager records carry USER_UNIT,
  system records UNIT), user-scope fixtures now use USER_UNIT; one user-slot UNIT
  arm and one system-slot USER_UNIT arm remain deliberately to prove the subject
  is read scope-independently. The user matrix serves coredump=2 against
  segfault=1 (one plain + one signal-11 record in separate slots), so a dropped
  `COREDUMP_SIGNAL=11` argv match or a dropped jq signal check changes the
  expected counts.
  New cases: system-only OOM crit; unit-query rc1 with kernel OOM still crit and
  split tokens unavailable; fleet (info/CLEAN, via USER_UNIT); non-fleet
  (info/CLEAN, owner tsukuroi); both-subject-fields-equal unknown; legal `\xHH`
  name non-fleet; illegal `\q` escape malformed/non-fleet-negative; user
  `UNIT_RESULT=signal` warn+DRIFT; fleet oom-kill crit +
  fleet route; subjectless oom-kill crit + unattributed; array UNIT_RESULT unknown
  (no alarm); UNIT newline injection canary (no forged FINDING line, no unit bytes
  in output); system-journal USER_UNIT fleet; text-only legacy classes produce no
  OOM/KILL/UNIT finding.

## Risks / residuals (explicit)

- No behavioral verification by this seat (wave contract). The selftest additions
  and the live census still need the L1 gate run; the sibling regression harness
  (`tools/mori-round14-regressions.py`) pins the final interface.
- `UNIT_FAILURE_UNATTRIBUTED_JOURNAL` is emitted with the same id in both scopes per
  L1 ruling; two same-id FINDING lines can make `--drift` line pairing ambiguous.
- Malformed/array `MESSAGE_ID` still grades the class unavailable (fail-closed
  raw total, per L1: do not broaden to counting malformed records). It is
  disclosed as unavailable, never a silent 0, and the other scope/source can
  still alarm.
- Fixture dispatcher still ignores `--output-fields` (no projection added): the
  selftest proves the request via the SURFACE `unit_query_output_fields` token,
  not by stripping unrequested fields. Adding projection would also weaken the
  MESSAGE-canary leak proof; recorded as a residual.
- Kernel-OOM notices are client-supplied (`trust=client-supplied`); restoring the
  alarm reintroduces the user-journal forgery/DoS surface noted in r13 Security.
  This is the required alarm restoration, not a claim of unique-victim counting.
- `UNIT_RESULT=signal` warn is a result ordinal, not proof of SIGKILL; the SIGKILL
  record path remains the count= basis.
- No drift re-pin: the r10 baseline was already red and is untouched.

## Interface coordination

Sent the exact schema to `MoriR14.JournalRegression` and
`MoriR14.HarnessMigration` (including the L1 final-ruling correction: one global
OOM line, no per-scope OOM ids, `UNIT_FAILURE_UNATTRIBUTED_JOURNAL` same id in both
scopes). Also answered `MoriR14.JournalSentinel`, `MoriR14.RoutingAttack`,
`MoriR14.OomAttack` and `MoriR14.CounterAttack` with the settled dispositions.

## Parent verification commands

- `bash tools/mori-census.sh --selftest` (hermetic; expect PASS, 0 failed)
- `bash tools/mori-census.sh` (live; read-only)
- sibling gate: `python3 tools/mori-round14-regressions.py --selftest` and its
  frozen-vs-repaired run (red before / green after)
