# JournalRegression — round-14 isolated journal regression gate

Seat: `MoriR14.JournalRegression` (executor, leaf). Date 2026-10-20.
Owned output: **new** `tools/mori-round14-regressions.py` and this report. No production,
frozen, fleet, sibling, MANIFEST or verifier file was edited. No commits.

## Delivered

| Path | SHA-256 (at report time) |
|---|---|
| `tools/mori-round14-regressions.py` (new, 2,476 lines, executable; Main applied the `%%s` fix at line 632) | `c39e5a7352666d09dc662293e1ea7be47ee3523b53247a5a6ae02e7dda19288d` |
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

### Measured receipts (Main, commit 5601d12; this seat ran none)

- `r14-selftest-accepted.json`: exit 0, `SELFTEST: pass checks=20`, harness `c39e5a…`.
- `red-before-accepted.json` + `red-before-accepted/evidence.json`: exit 1, mode `red-before`,
  43 claims / 43 fail, harness `c39e5a…`, 20.8 s.
- `green-after-accepted.json` + `green-after-accepted/evidence.json`: exit 0, mode
  `strict-with-frozen-control`, 44 claims / 44 pass (43 cases + `R14_FROZEN_CONTROL`),
  harness `c39e5a…`, 41.8 s.
- `c1-measurement.json` counts the six named acceptance arms (user/system kernel OOM,
  unit oom-kill, fleet, nonfleet, user signal) as 6 fail on the frozen bytes and 0 on the
  repaired census, and independently reports all 12 raw scope counts identical between the
  two receipts. It states the red limit explicitly: **43/43 failing is not 43 production
  defects**—the frozen schema also lacks the added unit tokens/query fields, including on
  retained controls. The receipts contain observed results, not fixture specifications; both
  runs share the case ids and harness bytes, temporary fixture paths differ, and byte-identical
  full fixture trees are not claimed.
- The earlier `r14-selftest.json` / `red-before.json` (harness `7af94b…`) are **setup
  failures**, not a valid red-before: `build_common` formatted a literal shell `printf '%s'`
  through Python `%`, raising `TypeError`. Main fixed it to `%%s` and added a generic
  `except Exception` that returns rc2 (`R14_INTERNAL`) instead of a false behavioral rc1.

### Source-only formatting audit (post-fix)

The only unsafe literal-`%` inside a `%`-formatted string was the PATH tripwire body
(`printf '%s'` at line 632); it is now `printf '%%s'`. Every other `%` call site was audited:
`git`/`pgrep`/`tmux` bodies are static; the `df` stub's `1%%` is not `%`-formatted (it is
passed as a literal body, so the shell prints `%`); the journal stub template is assembled by
`.replace`, and its inner `%` formats are `scope=%s rc=%d` with 2/2 arguments. No similar
hazard remains.

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
# measured at 5601d12: exit 1; all 43 cases fail (coarse red, see risk 2);
# the named acceptance arms and 12-cell raw parity are counted in c1-measurement.json

python3 "$R/tools/mori-round14-regressions.py" \
  --census "$R/tools/mori-census.sh" \
  --frozen "$R/.ufo/waves/round-14/frozen/mori-census.sh" \
  --output /tmp/r14-green
# measured at 5601d12: exit 0; 44/44 pass (43 cases + R14_FROZEN_CONTROL)

python3 "$R/tools/mori-round14-regressions.py" --selftest
# measured at 5601d12: exit 0, checks=20: parser checks + a real focused gate
# subprocess over the pinned frozen bytes (exit 1, FINDING R14_OOM_ALARM_USER/
# R14_UNIT_OOM_KILL status=fail) + a tampered-copy subprocess (exit 2,
# R14_SNAPSHOT_TAMPERED)
```

Required red set: 29 ids in `FROZEN_RED_REQUIRED`; this is the gate's red-control contract.
It is not a defect count. The reported before→after differential is the six named acceptance
arms (6 fail on frozen, 0 on the repaired census) plus independent 12-cell raw-counter parity,
as recorded in `c1-measurement.json`; L1 explicitly ruled that the 43/43 coarse red is not 43
production defects. The gate's `pairs` block records each case's red and green reasons and
stdout/stderr hashes for the receipt.

## Risks, limits, blockers

1. **Mixed `MESSAGE_ID` stream remains all-or-nothing (not waived).** `R14_SEC_DUP_MSGID_MIXED`
   is a retained control, not a green requirement: one valid `fe6faa94` record plus a
   `MESSAGE_ID` array still grades the class `record-invalid` (honest, never a fake zero) and
   therefore emits no OOM alarm. JournalSentinel flagged this as an alarm-silencing path; the
   landed r14 census did not change the r13 `all(…)` validation. L1 should route this as a
   residual limitation. A future fix that counts the valid record must update this control
   deliberately (it will otherwise fail on the pinned unavailable expectation), so the gate
   cannot silently bless either behavior.
2. **Coarse red-before differential (acknowledged; no code change).** The accepted red-before
   fails all 43 frozen cases, including controls (empty, notice-only-info, query-error,
   SIGKILL warn), because the r13 rows lack the 12 `unit_*` tokens and the unit query lacks
   `UNIT/USER_UNIT/UNIT_RESULT`; the token-completeness and unit-argv invariants alone fail
   every frozen case. Per L1's ruling this is **not 43 production defects**: the report counts
   six named acceptance arms (user/system kernel OOM, unit oom-kill, fleet, nonfleet, user
   signal) as 6 fail on frozen and 0 on the repaired census, with the alarm/severity/routing
   reasons inspected, plus independent 12-cell raw-counter parity from
   `c1-measurement.json`. `c1-measurement.json` also records the provenance limit: receipts
   are observed results, not fixture specifications; case ids and harness bytes are shared,
   temporary fixture paths differ, and byte-identical full fixture trees are not claimed.
   A cleaner per-case differential would apply completeness/argv checks to the SUT or add a
   frozen-specific expectation mode; that is an L1 design decision and was not changed here.
3. **Query-shape pin.** The gate asserts exactly two unit queries (one per scope) with
   `_BOOT_ID,MESSAGE_ID,UNIT,USER_UNIT,UNIT_RESULT`. A legitimate redesign with a different
   call shape must update this invariant deliberately; it cannot pass by never requesting the
   fields.
4. **Runtime.** 43 cases × 2 targets ≈ 86 census invocations; normal runs are sub-second and
   `R14_TIMEOUT_UNAVAILABLE` costs ~1 s per query (bounded by `MORI_JOURNAL_TIMEOUT_S=1`).
   Accepted green elapsed 41.8 s; `--only` exists for focused runs.
5. **Selftest green path.** `--selftest` proves the real red path (exit 1 + stable ids) and the
   tamper path (exit 2 + `R14_SNAPSHOT_TAMPERED`) in subprocesses; it does not execute the
   repaired census. The green proof is the accepted strict run above.
6. **Schema ownership.** Expected values are persisted from L1's final ruling and the landed
   bytes at report time. If CensusRepair changes ids/severity/fields again, the gate fails
   loudly rather than silently accepting the change.

## Tooling / verification

No tools installed or upgraded. This seat ran no build, lint, test, formatter, smoke, census or
gate; all measured receipts under `.ufo/waves/round-14/evidence/` were produced by Main at
commit `5601d12` against harness `c39e5a…`. The seat's post-fix work was the source-only
`%`-format audit (line 632 was the sole unsafe literal-`%` locus; it is now `%%s`, and no
similar hazard remains) and this report update. The digests and line counts above come from
`sha256sum`/`grep` reads only.
