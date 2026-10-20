# CensusFix — round 13 (C1 structured journal scopes + F01 long-history authorship)

Status: implementation complete, unverified by this seat (L1 owns integrated checks).
Owned file changed: `tools/mori-census.sh` only (VERSION `census-r5` -> `census-r6`).
No commits, no tool installs, no verification runs (per assignment: no tests/lint/build).

## 1. C1 design — what is counted, in which scope, with which unit

`probe_journal` (`tools/mori-census.sh:879-1120`) replaces the old single-surface
`journalctl --user -b --no-pager` text grep and the unfiltered `-o json
COREDUMP_SIGNAL=11` call. It now runs six structured queries per journal scope and
emits TWO surface rows, `SURFACE journal.user:` and `SURFACE journal.system:`,
each with its own state.

Per-query argv (no `-q`; scope is always explicit):

```
journalctl <--user|--system> -b --no-pager -o json \
  --output-fields=_BOOT_ID,MESSAGE_ID[,...] <one or more FIELD=value matches>
```

Classes (per scope), all count-only and never summed:

| class | structured key | unit |
|---|---|---|
| `kernel_oom_notice` | `MESSAGE_ID=fe6faa94e7774663a0da52717891d8ef` | notice record |
| `oomd_notice` | `MESSAGE_ID=d989611b15e44c9dbf31e3c81256e4ed` | notice record |
| `coredump_notice` | `MESSAGE_ID=fc2e22bc6ee647b6b90729ab34a250b1` | coredump notice |
| `segfault_signal11` | `MESSAGE_ID=fc2e22bc6ee647b6b90729ab34a250b1 COREDUMP_SIGNAL=11` | record (subset of coredump records) |
| `unit_sigkill_record` | `MESSAGE_ID=98e322203f7a4ed290d09fe03c09fe15 EXIT_CODE=killed EXIT_STATUS=9` | record (unit process, SIGKILL) |
| `unit_failure_record` | `MESSAGE_ID=d9b373ed55a64feb8242e02dbe79a49c` | record ("Unit failed") |

Class-concrete argv (replace `<scope>` with `--user` or `--system`):

```
# kernel_oom_notice / oomd_notice / coredump_notice / unit_failure_record
journalctl <scope> -b --no-pager -o json \
  --output-fields=_BOOT_ID,MESSAGE_ID MESSAGE_ID=<fe6faa94…|d989611b…|fc2e22bc…|d9b373ed…>
# segfault_signal11
journalctl <scope> -b --no-pager -o json \
  --output-fields=_BOOT_ID,MESSAGE_ID,COREDUMP_SIGNAL \
  MESSAGE_ID=fc2e22bc6ee647b6b90729ab34a250b1 COREDUMP_SIGNAL=11
# unit_sigkill_record
journalctl <scope> -b --no-pager -o json \
  --output-fields=_BOOT_ID,MESSAGE_ID,EXIT_CODE,EXIT_STATUS \
  MESSAGE_ID=98e322203f7a4ed290d09fe03c09fe15 EXIT_CODE=killed EXIT_STATUS=9
```

`cmd=` on the surface row is a shape (fields plus `<id>` placeholder), not a
replayable command, because one row aggregates six queries; the table above is the
replayable form.

Semantics and guards:

- **No MESSAGE.** Every query restricts output fields; the contract is count-only.
  `MESSAGE_ID`, `COREDUMP_SIGNAL`, `EXIT_CODE`, `EXIT_STATUS` are non-underscore
  (client-supplied) fields, so rows/findings carry `trust=client-supplied` and the
  probe calls them record matches, never authenticated events or victims.
- **Boot anchor.** `BOOT_ID_EXPECTED` (`:311-323`) is `MORI_BOOT_ID` or
  `/proc/sys/kernel/random/boot_id` normalized to 32 lowercase hex (proc emits a
  dashed UUID). Every parsed record's `_BOOT_ID` must equal it; a foreign boot is
  `boot-mismatch`, several boots are `multi-boot`. The one echoed journal-derived
  string is that 32-hex boot id. A class with zero records still prints the
  validated current boot in `boot=<32hex>`: the boot is known independently of
  whether the scope held records.
- **JSON validation.** One `jq` pass (host parser is `jaq 3.1.1`, jq-compatible;
  `MORI_JQ_BIN`) slurps the stream, type-guards every record, validates the class
  field (`MESSAGE_ID`/`COREDUMP_SIGNAL`/`EXIT_CODE`+`EXIT_STATUS`) and the boot,
  and emits `<records>\t<boots>\t<boot>`. `jq` stderr is discarded; empty input is
  `0\t0\tnone` at rc 0 (valid zero).
- **stderr separated.** `journal_query` (`:935-1010`) captures stdout via command
  substitution and pipes stderr to a `wc -c` coprocess that drains it continuously
  and emits only a byte count; the bytes themselves are never stored or printed.
  The coproc descriptors are duplicated into ordinary persistent dynamic FDs
  before the capture (coproc FDs are unavailable inside a command-substitution
  subshell) and the originals are closed, so `wc` sees EOF from the ordinary write
  FD. Nonempty stderr grades the class `unavailable:stderr-nonempty` even at rc 0,
  because journalctl can warn on a partial/corrupt or permission-limited store
  while exiting 0. `-q` is not used.
- **rc discipline.** Nonzero producer rc is never parsed (partial bytes are
  discarded): `unavailable:rc-N`, with 124/137 named `timeout`. An absent
  `journalctl`, absent parser, or missing timeout binary makes the scopes
  unavailable; no count is fabricated.
- **Bounded runtime.** Each query runs under `timeout -k 1 2` via
  `MORI_JOURNAL_TIMEOUT_S` (local default 2 s, `:305-310`), documented as a local
  bound, not a measured scan cost.
- **Independent scopes.** No total, no sum, no victim inference. A zero in the
  system row is "0 matching records in the queried scope", not service health;
  rows carry `oomd_activity=unmeasured`.
- **Severity.** All notice/coredump/unit-failure counts are INFO. The sole warn is
  `KILL_SIGNAL_JOURNAL` for **user-scope** `unit_sigkill_record`, preserving the
  DRIFT path the old text class had; its observation says `unit=record signal=9
  attribution=none`. The system analogue is INFO (`KILL_SIGNAL_JOURNAL_SYSTEM`).
- **Finding ids (INFO unless stated):** `KERNEL_OOM_NOTICE_JOURNAL_{USER,SYSTEM}`,
  `OOMD_NOTICE_JOURNAL_{USER,SYSTEM}`, `COREDUMP_NOTICE_JOURNAL_{USER,SYSTEM}`,
  `SEGFAULT_SIGNAL11_JOURNAL_{USER,SYSTEM}`, `KILL_SIGNAL_JOURNAL` (user, warn) /
  `KILL_SIGNAL_JOURNAL_SYSTEM`, `UNIT_FAILURE_JOURNAL` (user) /
  `UNIT_FAILURE_JOURNAL_SYSTEM`, plus one unconditional INFO
  `JOURNAL_CLASSES_UNMEASURED` (`classes=oom_kill_text,other_signals,other_unit_failure_text`,
  `reason=no-anchored-structured-field`; emitted even when journalctl/jq is absent).

## 2. Removed / changed public schema (no compatibility aliases)

| old (r5) | r13 status | reason / replacement |
|---|---|---|
| `SURFACE journal:` single user row | removed | two rows `journal.user`, `journal.system` |
| `oom_kill=N` (text grep) | removed | text is not metadata (QUALITY #15/M13); kernel victim lines have no stable MESSAGE_ID and are named `oom_kill_text` in `unmeasured=` |
| `kill_signal=N` (text grep: `status=9/KILL`, `SIGKILL`, `Failed with result 'signal'`) | removed as text | user `KILL_SIGNAL_JOURNAL` warns only on the catalog SIGKILL record (`98e32220…`, EXIT_CODE=killed/EXIT_STATUS=9); other signals are `other_signals` in `unmeasured=` |
| `segfault=N` (text grep + unfiltered JSON `COREDUMP_SIGNAL=11`) | replaced | `segfault_signal11` = field-validated `MESSAGE_ID=fc2e22bc… AND COREDUMP_SIGNAL=11`, in its own per-scope query; coredump notices are NOT relabelled segfaults |
| `unit_failure=N`, `UNIT_FAILURE_OUT_OF_SCOPE`, `UNIT_FAILURE_JOURNAL` text | retired as text | `unit_failure_record` counts catalog `d9b373ed…` "Unit failed" records; no fleet classification; `UNIT_FAILURE_JOURNAL` id retained for the user record count |
| `OOM_KILL_JOURNAL` crit | removed | the record is a per-unit notice, not a kill (M19); counting it as a kill was the defect |
| `rc` semantics (`>1` unavailable, 1 tolerated) | removed | nonzero rc is unconditionally unavailable |
| `MORI_FIXTURE` live-only JSON branch | removed | structured queries run identically live and in fixtures |

The removed text classes were not reliable kill counters: 5 kernel `Killed
process` records coexisted with 7 user + 9 system `fe6faa94…` notices in one boot
(`corpus/knowledge/kill-classes-by-message-id-r12.md:6,15-21`;
`corpus/lessons/round-12.md:42` M19). The cgroup surface (`CGROUP_OOM_KILL`, trusted
`memory.events.local`) is NOT asserted to replace every path the text classes could
see; its scope is named on its own row.

## 3. F01 — exact-author membership without a producer pipe

Old pipeline (`audit-r11.md:156`, Appendix B `:308-375`):
`printf … | sed … | grep -Fxq …` under `pipefail`. On a long history grep exits at
the first match, sed takes SIGPIPE (141), the pipeline rc becomes 141, and an exact
subject commit grades `progressing-weak` (`other_authored_commits=12001`, rc 0).

New code (`tools/mori-census.sh:1703-1720`): one `awk` pass filters the window and
prints the author list into `$authors` via a here-string; whole-line membership is a
bash `case` pattern (`*$'\n'"$expected"$'\n'*`). There is no writer process feeding a
reader, so no writer can be killed early; `sibn` is a second here-string awk pass.
Also in `grade_lane`, the git calls now clear inherited
`GIT_DIR/GIT_WORK_TREE/GIT_INDEX_FILE` and `ls-files` runs with
`-c core.fsmonitor=false` (`:1665-1668`, `:1685`, `:1695`), removing repo-hook and
env-redirection channels from the same inputs.

## 4. Drift mask

`DRIFT_COUNTER_KEYS` (`:1987-1997`) drops the dead text keys
`kill_signal`/`segfault`/`unit_failure`, keeps `oom_kill` (cgroup), and adds the six
new class counters (`kernel_oom_notice`, `oomd_notice`, `coredump_notice`,
`segfault_signal11`, `unit_sigkill_record`, `unit_failure_record`). `boot` joins
`DRIFT_VOLATILE_SPECIAL` and gets the mask rule `\bboot=[^ ;)]*` -> `boot=<V>`. The
`VERSION` bump to `census-r6` and the volatile-list change mean an r5 pin reports
drift/`volatile_fields`; re-pinning is an L1 recorded act, not part of this seat.

## 5. Selftest coverage added (hermetic; stubs only, MORI_BOOT_ID pinned)

Dispatcher (`:2268-2291`): journalctl is arg-aware by scope + MESSAGE_ID/class and
honors `journal-<scope>-<class>[.rc|.err]`, falling back to the legacy global
`journal`. New cases (labels as they print):

1. `journal: per-scope catalog counts; user unit SIGKILL is the only warn` — user
   3/0/1/1/1/1, system 5/2/0/0/0/0, INFO ids asserted, `boot=<hex>`, DRIFT; also
   asserts a `MORI_JOURNAL_CANARY` MESSAGE value never reaches output.
2. `journal: legacy text ids are not counted (Q15)` — legacy text in the global
   file, empty class slots; all counts 0, no OOM_KILL/KILL_SIGNAL/SEGFAULT/
   UNIT_FAILURE text finding.
3. `clean: empty journal` — rc0 empty stream => both rows ok, all counts 0,
   `boot=0123456789abcdef0123456789abcdef` (the known current boot, even with no
   records), CLEAN.
4. `journal: user producer rc1 -> user unavailable, system still counted`.
5. `journal: system producer rc2 -> system unavailable, user ok`.
6. `journal: system producer rc1 -> system unavailable, user still counted`.
7. `journal: nonempty stderr -> unavailable, never counted` (stderr canary absent
   from output).
8. `journal: malformed JSON -> unavailable, never 0`.
9. `journal: record identity mismatch -> unavailable` (`record-invalid`).
10. `journal: record from another boot -> unavailable` (`boot-mismatch`).
11. `journal: records from several boots -> unavailable:multi-boot`.
12. `journal: absent journalctl -> both scopes unavailable`.
13. `journal: absent JSON parser -> both scopes unavailable, no counts`.
14. `journal: invalid boot anchor -> both scopes unavailable`.
15. `silence: 12k-history exact subject -> progressing (F01)` — one exact subject
    record + 12,000 siblings.
16. `silence: 12k-history siblings only -> progressing-weak, exact count`
    (`other_authored_commits=12000`).

Fixture boot id is `0123456789abcdef0123456789abcdef` via `sut_env`'s `MORI_BOOT_ID`.

## 6. Measured evidence (read-only inspection, 2026-10-20)

- `journalctl --user -b --no-pager -o json --output-fields=_BOOT_ID,MESSAGE_ID
  MESSAGE_ID=000…0` -> rc 0, 0 stdout bytes, 0 stderr bytes; same with `--system`
  (uid 1000). So a valid empty query is a 0-byte rc-0 stream; rc 1 is not empty.
- `/proc/sys/kernel/random/boot_id` -> `430d3038-1859-49e6-82cf-5fc475d1b3d0`;
  normalized (dashes removed) = 32 lowercase hex.
- The delivered jq tail evaluated against five inputs: empty -> `0 0 none`;
  two valid -> `2 1 <boot>`; same-boot wrong MESSAGE_ID -> `record-invalid`;
  foreign boot -> `boot-mismatch`; two foreign boots -> `multi-boot`; non-object ->
  `record-invalid`. (Host parser: `jaq 3.1.1`.)
- Catalog S013 at commit `cf8ebfc6` (`catalog/systemd.catalog.in`): `:561`
  `d9b373ed55a64feb8242e02dbe79a49c` "Unit failed"; `:568`
  `98e322203f7a4ed290d09fe03c09fe15` "Unit process exited" with EXIT_CODE/
  EXIT_STATUS; `:66`/`:604`/`:884` the three assigned ids.

## 7. Expected integrated selftest (static count; not run by this seat)

- Invocations: 75 `check()` + 4 `check_cli()` + 8 `pd_check()` = **87 assertion
  cases**. Expected green summary:
  `MORI_CENSUS_SELFTEST: PASS (87 cases, 87 passed, 0 failed)`,
  `run_selftest` exit 0. Three additional negative guards (`bad()`) do not add a
  PASS: MESSAGE canary leakage, a legacy text finding, and stderr canary leakage
  each fail the run if present.
- Journal matrix: 14 case labels (13 new `journal:` arms above plus the updated
  `clean: empty journal`), both scope rows, six class tokens, INFO severities with
  the single user `KILL_SIGNAL_JOURNAL` warn. `CountDesign` found no gap except a
  named residual for the `timeout`/`no-timeout-bin` arms (not exercised by a case).
- Fixture costs: no wall-time price; the 12k-history cases hash a ~1.2 MB stub
  git log twice per case (`fx_hash` before/after) and run one census each; no
  network, no host journal access, no files outside the `/tmp` selftest tree.
- Known integration blocker (not a census failure): RegressionHarness still parses
  one `SURFACE journal:` row / four classes / the older unmeasured list and will
  red until it re-anchors to the two-row grammar; corrected grammar was sent.

## 8. Probe prices for the new journal surface (QUALITY #11)

- **Found-ness:** 6 classes x 2 scopes = 12 cells; each cell is an integer or a
  named `unavailable:<reason>` on its scope row. No cell can be silently absent;
  a whole-scope absence (missing journalctl/parser/boot anchor) is a row reason.
- **Marginal wall time:** [UNMEASURED]. This seat only measured the empty-match
  rc/bytes above, not a timed live scan; the assumed cost is not priced.
- **Enforced bound / vocabulary:** 2 s per `journalctl` query
  (`MORI_JOURNAL_TIMEOUT_S`, labeled local), 12 queries -> <=24 s added worst
  case; rc 124/137 -> `unavailable:timeout`; missing `timeout` -> `no-timeout-bin`
  with no query run.
- **Filter drop set:** `MESSAGE` is never requested; stderr bytes are dropped
  (presence alone fails the class); records from another boot are
  `boot-mismatch`/`multi-boot`; records missing/wrong class fields are
  `record-invalid`; all stdout from a nonzero-rc/timeout query is dropped; records
  outside `-b` never arrive. Duplicate identical records are NOT dropped (counted
  twice, no cursor identity). Records arriving after the 2 s bound are not
  dropped as a count: the class becomes unavailable.

## 9. Risks, boundaries, and contested points

- **Prior text classes retired as a measurement correction (Q15/Q16).** The old
  counts were MESSAGE-text matches; they were not reliable kill counters. The
  structured replacements cover the three assigned catalog notices, signal-11
  records and two unit records. Still unmeasured and named on the row:
  `oom_kill_text` (kernel victim lines have no stable MESSAGE_ID), `other_signals`
  (only signal 9 has the assigned anchor), `other_unit_failure_text`. Cgroup
  counters are not claimed to cover these paths.
- **Forgeable fields.** Any local writer can set `MESSAGE_ID`/`COREDUMP_SIGNAL`/
  `EXIT_*`; counts are client-supplied record matches and carry that label.
  No trusted-field (`_PID=1`/`_EXE`) cross-check was added.
- **No partial-count abstraction.** One non-object or field-invalid record makes
  that class `record-invalid` (fail-closed) rather than a partial count with a
  rejected counter; duplicate identical records count twice (no `__CURSOR`
  dedup — L1 decision: count parsed records, not authenticated unique events).
- **Current boot only.** Queries use `-b` (= `-b 0`), not `-b all`; retained-boot
  samples (the 7/9 notice observation) are not presented as current-boot counts.
  This diverges from the `-b all` suggestion in the JournalKnowledge note; the
  D2 boot-id anchor requires the current boot.
- **Runtime bound.** 2 s per query is a local placeholder; a slow store yields
  `unavailable:timeout`, never an unbounded scan. stderr is drained by a
  `wc -c` coprocess that emits only a byte count (the producer can never block on
  a full stderr pipe), bounded by the same query timeout.
- **Drift/baseline.** New surface names and finding ids change the normalized
  output; existing pins will report `volatile_fields`/line drift.
- **Integration.** OracleFix (`tools/mori-silence-cases.sh`) confirmed its stub
  returns empty rc-0 JSON for every journalctl argv, so its 28 cases see zero
  counts and both rows `ok`; the `MORI_CENSUS:` emitter grammar is unchanged.
  RegressionHarness and CountDesign were sent the final two-row/6-class grammar;
  my first harness message was stale and was corrected.
- **Severity policy (L1-ratified, recorded here).** Notice/record counts are INFO:
  the `fe6faa94…` kernel-OOM record is a per-unit notice, and carrying the old
  text-derived `OOM_KILL_JOURNAL` crit onto it would re-assert a kill the record
  does not prove (M19). `CGROUP_OOM_KILL` remains crit because it reads a trusted
  cgroup local kill counter with its scope named. The only journal warn is the
  user `unit_sigkill_record` record (signal 9, `attribution=none`).
- **Unasserted branch arms (named residuals, not added — scope frozen).** The
  selftest does not exercise: rc 141 with records on stdout; truncated
  multi-record JSON (the `malformed-json` path is exercised by `{not json`);
  array-valued `_BOOT_ID` (`record-invalid` via the non-string-boot branch);
  array-valued `MESSAGE_ID` (`record-invalid` via scalar equality); a failed class
  alongside a positive sibling (code emits the sibling INFO with the row
  `unavailable`); denied system scope with a positive user count; absence of a
  summed token (no total field exists); `no-timeout-bin` (fixture PATH always has
  `timeout`); legacy text served directly into a structured slot
  (`malformed-json`; the delivered text-only case keeps text out of every slot).
  JournalFixtureDesign's 11-case gap matrix is the recommended place to add them
  at the carrying commit; L1 recomputes the tally there.
- **Stale doc pointers (outside this seat's files).** `PROVINCE.md:24`,
  `corpus/knowledge/structured-journal-scopes-r13.md` (five-class table; delivered
  is six), and `SCORECARD.md:644-649` (kernel-OOM line) still describe the old
  classes. `LOG.md` append per AGENTS.md is owed by L1.
