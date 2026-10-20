# JournalRegression — round-14 isolated journal regression gate

Seat: `MoriR14.JournalRegression` (executor, leaf). Date 2026-10-20.
Owned output: **new** `tools/mori-round14-regressions.py` and this report. No production,
frozen, fleet, sibling, MANIFEST or verifier file was edited. No commits.

## Delivered

| Path | SHA-256 (at report time) |
|---|---|
| `tools/mori-round14-regressions.py` (new, 2,470 lines, executable) | `7af94b4ce8651b8ee75b2a334098cb0a52909c2da2aec56d457e24f4a3ca58ac` |
| `tools/mori-census.sh` (production owner CensusRepair, read-only here) | `0e41cb83fce2e8c5c711171e1cde2e6fa2809dcfce630eccabe52bcbe41516d9` |
| `.ufo/waves/round-14/frozen/mori-census.sh` (pinned red input) | `39abda0a67028575d888d9157b8548dec0b4944c3d8c165691e88ab657fc3985` |

The gate pins `39abda0a…` as an **in-script constant** (`PINNED_SHA256`), not a manifest
read. `inputs.json` is cross-checked for contradiction only; a mismatch is `snapshot_tampered`
rc2. `expected.json` (`88d6c3d9…`) declares the same before/after gradient. Base commit
`dbe85009253c092fe50e4e93056fceeae273ec31`.

## Behaviour

`python3 tools/mori-round14-regressions.py --census PATH --output DIR` runs 43 case claims
against the census under test, and by default also runs the same fixtures against the pinned
frozen bytes. The frozen snapshot must fail the required red cases; the census under test must
pass every claim. The gate exits:

- `0` every claim passed and the frozen control reproduced every required red case;
- `1` any claim failed or the frozen control did not reproduce a required red case;
- `2` usage/setup/pin error (`snapshot_tampered`, unreadable target, unknown `--only` id).

`--census .ufo/waves/round-14/frozen/mori-census.sh --output DIR` is the red-before run: the
SUT digest equals the pinned frozen digest, the gate runs the suite once and exits `1` with the
stable failing case ids. `--no-frozen-control` measures the green snapshot alone.
`--only ID[,ID…]` is a focused real run (used by `--selftest`).

### Isolation and faithfulness

- Every census run is `bash <copy>` with a **complete explicit env** from `census_env()`
  (never `os.environ`). `HOME`, `TMPDIR`, every `MORI_*` path, `MORI_BOOT_ID` and
  `MORI_BOOT_ID_FILE` point into an opaque `case-NNN` fixture tree under `--output`.
- The target bytes are read once, hashed, copied into the fixture tree, read back, and
  executed from that copy. Every emitted `FINDING … script_sha256=` must equal the executed
  copy digest.
- `journalctl` resolves to a generated synthetic Python stub. It emulates `--user/--system`,
  `-o json`, exact `FIELD=value` filters, and **projects each record onto the requested
  `--output-fields` plus `__CURSOR`, `__REALTIME_TIMESTAMP`, `__MONOTONIC_TIMESTAMP`,
  `_BOOT_ID`**. A census that never requests `UNIT/USER_UNIT/UNIT_RESULT` cannot classify a
  subject and goes red. The gate additionally asserts exactly two unit-query calls (one per
  scope) and that each requests `_BOOT_ID,MESSAGE_ID,UNIT,USER_UNIT,UNIT_RESULT`.
- A PATH `journalctl` tripwire logs and refuses any bare call; a non-empty tripwire fails the
  case. No host journal is opened and no live probe fallback exists.
- Canaries (`MESSAGE`, malformed unit name, stderr text, and a **valid** canary unit name) are
  checked on the **raw** stdout/stderr before redaction; stored artifacts are redacted. The
  stub also forces `MESSAGE` into every record in leak mode and the gate asserts no `MESSAGE`
  field or match word was requested and no canary was emitted.
- Fixtures are removed unless `--keep-fixtures`; evidence remains under `--output`.

### Evidence retained

`<output>/evidence.json` contains: harness path+sha256, both target paths/executed copies/sha256,
the pinned constants and cross-checked manifest path, all 43 claims with observed reasons, the
required-red list, a per-case red/green `pairs` block (status, rc, reasons, stdout/stderr
sha256), every run record (argv, explicit env subset, rc, timeout, duration, stdout/stderr
paths and hashes), and the full green/frozen case observations. `MORI_R14_REGRESSIONS:
claims=N pass=N fail=N exit=E` plus `EVIDENCE <path>` close stdout.

## Claims pinned (43)

OOM (one global crit line, six fields, each equal to its scope SURFACE token; no `count=`):
`R14_OOM_ALARM_USER`, `R14_OOM_ALARM_SYSTEM`, `R14_UNIT_OOM_KILL`, `R14_UNIT_OOM_NONFLEET`,
`R14_UNIT_OOM_SYSTEM`, `R14_UNIT_OOM_BOTH_SCOPES` (two non-summed counters), `R14_UNIT_OOM_MISSING_SUBJECT`, `R14_UNIT_OOM_SUBJECT_ARRAY`,
`R14_FANOUT_ONE_SIGNAL_PER_KIND` (one OOM line, one SIGKILL line, drift=2),
`R14_PARTIAL_ERROR_SYSTEM_ALARMS` (user rc1 + system notice still crit),
`R14_UNIT_QUERY_ERROR_KERNEL_ALARM` (unit query rc1 + user notice still crit),
`R14_SCOPE_NOT_SUMMED` (user 3 / system 5, never 8), `R14_SCOPED_PARITY` (six raw counts per
scope, both scopes, near-miss selector records: sig6 coredump and killed/15 + exited/9 exit
records do not move the segfault/sigkill counts), `R14_OOMD_ONLY_INFO` (oomd notices INFO only).

Routing (INFO, roll unaffected): `R14_UNIT_FAILED_FLEET` (fleet, owner=mori, CLEAN),
`R14_UNIT_FAILED_NONFLEET` (owner=tsukuroi, CLEAN), `R14_UNIT_FAILED_UNKNOWN` (emitter-only
`_SYSTEMD_UNIT` -> unattributed), `R14_USER_UNIT_IN_SYSTEM` (USER_UNIT is a valid subject in
the system journal), `R14_SUBJECT_AMBIGUOUS` (both fields, even equal -> unattributed),
`R14_UNIT_SUBJECT_NULL_UNKNOWN` (null -> unattributed), `R14_UNIT_VALID_ESCAPE_KNOWN`
(`\xHH` valid), `R14_UNIT_INVALID_ESCAPE_UNKNOWN` (`\q` invalid, never fleet),
`R14_UNIT_RESULT_MISSING` and `R14_UNIT_RESULT_ARRAY_UNKNOWN` (`unit_oom_result_unknown`, not
oom), `R14_UNIT_RESULT_NOT_OOM_STRINGS` (uppercase `OOM-KILL` and empty string are non-oom,
non-unknown strings), `R14_UNIT_PARTITION` (fleet+nonfleet+unknown == raw total; sub- and
oom-partitions are also checked on every row).

Retained warnings/controls: `R14_SIGKILL_WARN` (user process SIGKILL warn, DRIFT),
`R14_UNIT_SIGNAL_WARN` (user `UNIT_RESULT=signal` warn, `count=0` /
`process_sigkill=0` / `user_unit_signal=1`, no sum, DRIFT), `R14_UNIT_SIGNAL_SYSTEM_INFO`
(system signal stays INFO), `R14_BASELINE_EMPTY` (CLEAN rc0, six+unit zeros),
`R14_QUERY_ERROR_UNAVAILABLE` (rc5 -> `unavailable:rc-5`), `R14_STDERR_UNAVAILABLE`,
`R14_MALFORMED_UNAVAILABLE`, `R14_WRONG_BOOT_UNAVAILABLE`, `R14_MULTI_BOOT_UNAVAILABLE`,
`R14_IGNORE_FILTERS_INVALID` (wrong class for the kernel query -> `record-invalid`),
`R14_TIMEOUT_UNAVAILABLE`, `R14_TEXT_ONLY_NOT_ADMITTED` (Q15), `R14_MESSAGE_CANARY`,
`R14_SEC_UNIT_CANARY` (malformed/newline name), `R14_SEC_VALID_UNIT_CANARY` (valid nonfleet
canary name is classified but never emitted; canary exists only in the record, not a path),
`R14_SEC_DUP_MSGID_MIXED` (retained control, see risk 1).

Global invariants on every case: no `total=`/`sum=` token; no retired
`KERNEL_OOM_NOTICE_JOURNAL_*`; exactly two scoped journal rows; all six raw counts and all 12
`unit_*` tokens present on ok/unavailable rows; fleet+nonfleet+unknown == raw failure count;
missing+ambiguous+malformed == unknown; oom fleet+nonfleet+subject_unknown == unit_oom;
unit_oom <= unit_failure_record; OOM field == SURFACE token; no MESSAGE key/field; no canary;
no tripwire call; finding `script_sha256` equals the executed target.

## Red-before / green-after procedure (for L1; not executed here)

```sh
R=/home/vgpnk/Projects/shokunin/mori-shokunin
python3 "$R/tools/mori-round14-regressions.py" \
  --census "$R/.ufo/waves/round-14/frozen/mori-census.sh" \
  --output /tmp/r14-red
# expected exit 1; FINDING R14_OOM_ALARM_USER status=fail,
# R14_UNIT_OOM_KILL status=fail, R14_UNIT_FAILED_NONFLEET status=fail, ... (29 required)

python3 "$R/tools/mori-round14-regressions.py" \
  --census "$R/tools/mori-census.sh" \
  --frozen "$R/.ufo/waves/round-14/frozen/mori-census.sh" \
  --output /tmp/r14-green
# expected exit 0; R14_FROZEN_CONTROL status=pass; 43/43 claims pass

python3 "$R/tools/mori-round14-regressions.py" --selftest
# expected exit 0: parser checks + a real focused gate subprocess over the pinned
# frozen bytes (exit 1, FINDING R14_OOM_ALARM_USER/R14_UNIT_OOM_KILL status=fail)
# + a tampered-copy subprocess (exit 2, R14_SNAPSHOT_TAMPERED)
```

Required red set: 29 ids in `FROZEN_RED_REQUIRED`, including every OOM/unit-oom arm, every
routing/unknown arm, both signal arms, parity/scope separation, partial error, valid-unit
canary and MESSAGE canary. The gate's `pairs` block records each case's red and green reasons
and stdout/stderr hashes for the before→after receipt.

## Risks, limits, blockers

1. **Mixed `MESSAGE_ID` stream remains all-or-nothing (not waived).** `R14_SEC_DUP_MSGID_MIXED`
   is a retained control, not a green requirement: one valid `fe6faa94` record plus a
   `MESSAGE_ID` array still grades the class `record-invalid` (honest, never a fake zero) and
   therefore emits no OOM alarm. JournalSentinel flagged this as an alarm-silencing path; the
   landed r14 census did not change the r13 `all(…)` validation. L1 should route this as a
   residual limitation. A future fix that counts the valid record must update this control
   deliberately (it will otherwise fail on the pinned unavailable expectation), so the gate
   cannot silently bless either behavior.
2. **Query-shape pin.** The gate asserts exactly two unit queries (one per scope) with
   `_BOOT_ID,MESSAGE_ID,UNIT,USER_UNIT,UNIT_RESULT`. A legitimate redesign with a different
   call shape must update this invariant deliberately; it cannot pass by never requesting the
   fields.
3. **Runtime.** 43 cases × 2 targets ≈ 86 census invocations; normal runs are sub-second and
   `R14_TIMEOUT_UNAVAILABLE` costs ~1 s per query (bounded by `MORI_JOURNAL_TIMEOUT_S=1`).
   Expect roughly one to two minutes for the full green run. `--only` exists for focused runs.
4. **Selftest green path.** `--selftest` proves the real red path (exit 1 + stable ids) and the
   tamper path (exit 2 + `R14_SNAPSHOT_TAMPERED`) in subprocesses; it does not execute the
   repaired census. The green proof is the L1 run above.
5. **Schema ownership.** Expected values are persisted from L1's final ruling and the landed
   bytes at report time. If CensusRepair changes ids/severity/fields again, the gate fails
   loudly rather than silently accepting the change.

## Tooling / verification

No tools installed or upgraded. No build, lint, test, formatter, smoke, census or gate run was
executed by this seat (lane rule: L1 runs verification once after all changes land). The
digests and line counts above come from `sha256sum`/`grep` reads only.
