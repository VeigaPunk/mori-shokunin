# JournalFixtureDesign — delivered C1 journal fixtures: audit + gap matrix

Seat: `MoriR13.JournalFixtureDesign` (executor, leaf). Axes: **coverage**, **operability**.
Scope: fixture design and read-only contract audit. No production edit, no commit, no build/
test/lint/format/smoke run, no census/oracle invocation, no tool install. The only write is this
file. Main agent owns integrated verification.

**Snapshots.** `tools/mori-census.sh` is a live editing target owned by `MoriR13.CensusFix`.
Implementation observations are against sha256
`958515111674daa86ce62d224cb1f653cbbcb33b8c14d50641f2810830b9adcf` (3440 lines, journal block
starts at `:887`, `probe_journal` at `:997`); the §5 D-A defect found there was repaired by
CensusFix before this report was finalized at sha256
`ce2752abde2747e63bce19ec18683aa2a0d1386c1312c7d9ea1db433cc2f3250` (3441 lines, tail at `:926`,
drift keys at `:1986-1998`, boot mask at `:2014`). Further edits continued while this report was
written; the last read was
`0f2faa2cb519fbdb6ecc86086a5cba5b8b107a016632b88dc1bd3bb7796ac872`, where D-A and D-D are closed
and the row `cmd=` is per-scope literal (`:1106`). CensusFix confirmed the repair independently and
re-evaluated the same filter under **jaq 3.1.1** with identical outputs (valid `2\t1\tboot`,
same-boot wrong-id `record-invalid`, foreign boot `boot-mismatch`, two foreign boots
`multi-boot`, non-object `record-invalid`, empty `0\t0\tnone`), so the classifier does not depend
on a jq-only construct. The shipped default remains `jq` (`JQ_BIN`, `:291`). CensusFix then
closed the open findings in `.ufo/waves/round-13/build/CensusFix.md` and froze the wave: severity
policy recorded, class-concrete argv published in that report, untested arms recorded as named
residuals for the carrying commit, stale pointers named (§7). No further census change follows
from this report. The two states are named where they differ.
The frozen pre-change baseline `.ufo/waves/round-13/frozen/mori-census.sh` (`probe_journal`
`:854`) is used only for before-state anchors. Line numbers will move; the tokens and semantics
below are the durable contract. Direct `jq` evaluations of the classifier were run (§5 D-A); no
census or oracle was executed.

---

## 1. Axes named

- **Coverage:** six class queries per scope replace four text classes; two previously text-only
  classes (`KILL_SIGNAL_JOURNAL`, `UNIT_FAILURE_JOURNAL`) keep their ids on catalog bases; a
  separate signal-11 record class remains; text-only surfaces are named `unmeasured=`, never 0.
- **Operability:** valid-empty vs denied vs producer-failure vs malformed are distinct states; a
  nonzero rc, stderr byte, missing parser/binary/timeout, or wrong boot is `unavailable`, never a
  count; every query is bounded; no `MESSAGE` is parsed or echoed.

---

## 2. Measured facts the fixtures must encode (observation, not inference)

Host kernel `7.2.3-arch1-3`, systemd `261 (261.2-1-arch)`, 2026-10-20. All probes are
`--output-fields`-restricted; no `MESSAGE` was read or quoted.

| # | Observation | Value |
|---|---|---|
| O1 | valid empty query (`--user`/`--system`, `-q -b`, real or all-zero ID) | `rc=0`, 0 lines, 0 stderr bytes |
| O2 | current boot `430d3038…`, all three original catalog IDs, both scopes | 0 records each |
| O3 | all-boot retained journals, user | `fe6faa94…` 7, `d989611b…` 0, `fc2e22bc…` 1585 |
| O4 | all-boot retained journals, system | `fe6faa94…` 9, `d989611b…` 0, `fc2e22bc…` 1 |
| O5 | denied journal (`sudo -u nobody journalctl --system\|--user -q -b -n1 …`) | `rc=1`, stdout empty, stderr exactly `No journal files were opened due to insufficient permissions.`; phrase survives `-q` |
| O6 | bad option (`journalctl --bogus-option`) | `rc=1` (rc=1 is not unique to denial) |
| O7 | `--output-fields=_BOOT_ID` still prints `__SEQNUM`, `__CURSOR`, `__REALTIME_TIMESTAMP`, `_BOOT_ID`, `__SEQNUM_ID`, … and no `MESSAGE` | confirmed on one user record |
| O8 | `COREDUMP_SIGNAL=11` record | `"COREDUMP_SIGNAL":"11"` (string), one JSON object per line; 5 records → 5 lines |
| O9 | repeated match args are OR | `fe6faa94 + fc2e22bc` → 1592 = 7 + 1585; `fe6faa94 + d989611b` → 7 |
| O10 | boot id forms | `/proc/sys/kernel/random/boot_id` = `430d3038-1859-49e6-82cf-5fc475d1b3d0`; journal `_BOOT_ID` = `430d3038185949e682cf5fc475d1b3d0` (dashes stripped) |
| O11 | catalog additions used by the delivered code | `d9b373ed55a64feb8242e02dbe79a49c` = "Unit failed" (local catalog `:561-566`); `98e322203f7a4ed290d09fe03c09fe15` = "Unit process exited" (local `:568-573`) |

Consequences: rc=1 is never "empty" (O1 vs O5/O6); a current-boot zero is not a retained-boot
count (O2 vs O3/O4); boot ids must be dash-normalized before comparison (O10).

Sources: S014 local systemd 261 man page `:572` (JSON objects separated by newline), `:598`
(non-unique field → JSON array), `:680` (`__CURSOR`,`__REALTIME_TIMESTAMP`,
`__MONOTONIC_TIMESTAMP`,`_BOOT_ID` always printed), `:797` (`-q`), `:1107` (exit status 0/nonzero);
pinned S014 (systemd 262) same anchors. S015: underscore fields trusted; `MESSAGE` not metadata;
`MESSAGE_ID` is client-set. S013 pinned `cf8ebfc6…`: `fc2e22bc…` `:66`, `fe6faa94…` `:604`,
`d989611b…` `:884`; the two unit IDs verified in the local 261 catalog (O11).

---

## 3. Delivered class contract (snapshot)

Six class queries per scope (`journal.user`, `journal.system`), independent, never summed.

| class token | match | unit | id (finding prefix) | user sev | system sev |
|---|---|---|---|---|---|
| `kernel_oom_notice` | `MESSAGE_ID=fe6faa94e7774663a0da52717891d8ef` | unit notice | `KERNEL_OOM_NOTICE_JOURNAL_USER/_SYSTEM` | info | info |
| `oomd_notice` | `MESSAGE_ID=d989611b15e44c9dbf31e3c81256e4ed` | unit notice | `OOMD_NOTICE_JOURNAL_USER/_SYSTEM` | info | info |
| `coredump_notice` | `MESSAGE_ID=fc2e22bc6ee647b6b90729ab34a250b1` | coredump notice | `COREDUMP_NOTICE_JOURNAL_USER/_SYSTEM` | info | info |
| `segfault_signal11` | `MESSAGE_ID=fc2e22bc…` **and** `COREDUMP_SIGNAL=11` | record | `SEGFAULT_SIGNAL11_JOURNAL_USER/_SYSTEM` | info | info |
| `unit_sigkill_record` | `MESSAGE_ID=98e322203f7a4ed290d09fe03c09fe15` **and** `EXIT_CODE=killed` **and** `EXIT_STATUS=9` | record | `KILL_SIGNAL_JOURNAL` (user), `KILL_SIGNAL_JOURNAL_SYSTEM` | **warn** | info |
| `unit_failure_record` | `MESSAGE_ID=d9b373ed55a64feb8242e02dbe79a49c` | record | `UNIT_FAILURE_JOURNAL` (user), `UNIT_FAILURE_JOURNAL_SYSTEM` | info | info |

Notes that must not be lost:
- `98e32220…` alone means "Unit process exited" (any exit); the class is the field-qualified
  **SIGKILL subset**. `EXIT_CODE`/`EXIT_STATUS` are non-underscore client-set fields, hence no
  stronger trust claim than the rest.
- `segfault_signal11` is a strict subset of the `fc2e22bc…` coredump notices (the jq filter also
  requires the coredump `MESSAGE_ID`).
- Only `user:unit_sigkill_record` flips the roll (warn). All notice classes, including
  `kernel_oom_notice`, are info. See §5 D-E: this drops the old `OOM_KILL_JOURNAL crit` DRIFT
  path; `CGROUP_OOM_KILL` remains crit (`tools/mori-census.sh:1290`), so the fleet keeps a crit
  kernel-kill counter, and a journal notice is context rather than kill evidence. L1 should
  ratify this in the header/PROVINCE rather than leave it implicit.
- `JOURNAL_CLASSES_UNMEASURED` (info, once) plus `unmeasured=oom_kill_text,other_signals,
  other_unit_failure_text` on both rows disclose classes with no anchored structured field. This
  is the correct "kept, not silently dropped" treatment (QUALITY 5/17).

Query shapes (delivered, `probe_journal` `:998`, `journal_query` `:942-996`):

```sh
timeout -k 1 "$JOURNAL_TIMEOUT_S" journalctl <--user|--system> -b --no-pager -o json \
  --output-fields=_BOOT_ID,MESSAGE_ID[,…] MESSAGE_ID=<id> [EXIT_CODE=killed EXIT_STATUS=9]
  [COREDUMP_SIGNAL=11]
```

Validation: stdout and stderr captured **separately** via a coprocess; any stderr byte →
`unavailable` (`stderr-nonempty`, bytes discarded); `rc != 0` → `rc-<n>` / `timeout` (124/137);
missing `timeout` → `no-timeout-bin`; `jq -s` over the whole stream; one boot id per stream;
only a 32-lowercase-hex boot id is echoed.

Reason vocabulary (closed): `rc-<n>`, `timeout`, `no-timeout-bin`, `stderr-nonempty`,
`malformed-json`, `record-invalid`, `multi-boot`, `boot-mismatch`, `boot-conflict` (currently
unreachable, §5 D-D). Row-level early returns: `journalctl=missing`, `parser=missing`,
`boot_id=unavailable`.

Surface row grammar (delivered):

```
SURFACE journal.user: ok (cmd=<template>; scope=user kernel_oom_notice=3 oomd_notice=0 coredump_notice=1 segfault_signal11=1 unit_sigkill_record=1 unit_failure_record=1; boot=0123456789abcdef0123456789abcdef; unit=notice notice_classes=… record_classes=… trust=client-supplied field=user:MESSAGE_ID rc=0; unmeasured=… reason=no-anchored-structured-field; ts=…)
SURFACE journal.system: unavailable (cmd=…; scope=system kernel_oom_notice=0 … oomd_notice=unavailable:rc-2 …; boot=…|unavailable:no-records; …; rc=2; …)
```

Finding observations (delivered): notice classes carry
`class=<cls> unit=notice message_id=<id> count=<n> scope=<scope> trust=client-supplied
basis=scoped-record-count boot=<id>`; signal-11 carries `class=segfault_signal11 unit=record
source_field=COREDUMP_SIGNAL value=11 …`; unit SIGKILL carries `class=unit_sigkill_record
unit=record message_id=98e32220… signal=9 … attribution=none`; unit failure carries
`class=unit_failure_record unit=record message_id=d9b373ed… … attribution=none`.

---

## 4. Delivered selftest inventory (14 journal checks at the snapshot)

`tools/mori-census.sh:2700-2860` area at the `9585151` snapshot (the structured block plus the
replaced `clean: empty journal` case). What each currently pins:

| check | pins | status vs code |
|---|---|---|
| `journal: per-scope catalog counts; user unit SIGKILL is the only warn` | all six classes, both scopes, 3/5/2 counts, `boot=BOOT13`, six finding ids, `unit=record` for record classes, `MORI_CENSUS: DRIFT`, `MORI_JOURNAL_CANARY` absent | passes; add the scope-sum forbids (§6 G11) |
| `journal: legacy text ids are not counted (Q15)` | class slots empty + text only in global `journal`; zeros; no legacy finding | passes (catches a leftover text query; does not feed text to a structured query) |
| `journal: user producer rc1 -> user unavailable, system still counted` | per-class `unavailable:rc-1`, scope independence | passes |
| `journal: system producer rc2 -> system unavailable, user ok` | `rc-2`, independence | passes |
| `journal: system producer rc1 -> system unavailable, user still counted` | `rc-1`, independence | passes |
| `journal: nonempty stderr -> unavailable, never counted` | split capture, `stderr-nonempty`, stderr canary absent | passes |
| `journal: malformed JSON -> unavailable, never 0` | `{not json` → `malformed-json` | passes |
| `journal: record identity mismatch -> unavailable` | `jrec` (correct BOOT13) + wrong `MESSAGE_ID` → expected `record-invalid` | passes at `ce2752a`; failed at `9585151` (§5 D-A) |
| `clean: empty journal` (replaced) | both rows `ok`, three class zeros each, `boot=unavailable:no-records` | passes; extend to all six class tokens and the no-finding forbids (G1) |
| `journal: record from another boot -> unavailable` | foreign `_BOOT_ID` + correct id → `boot-mismatch` | passes |
| `journal: records from several boots -> unavailable:multi-boot` | two foreign boot ids → `multi-boot` | passes |
| `journal: absent JSON parser -> both scopes unavailable` | `parser=missing` | passes |
| `journal: absent journalctl -> both scopes unavailable` | `journalctl=missing` | passes |
| `journal: invalid boot anchor -> both scopes unavailable` | `boot_id=unavailable` | passes |

Not present: rc0 + denied phrase, rc>0 with records (partial stream), rc141, truncated JSON,
array `_BOOT_ID`, array `MESSAGE_ID`, duplicate cursor, partial class failure with a positive
sibling count, denied system + positive user, scope-sum absence, `no-timeout-bin`,
`JOURNAL_CLASSES_UNMEASURED`. The rebuilt empty-journal case covers the routine zero arm but only
three of the six class tokens.

---

## 5. Defects and gaps found (ordered by severity)

### D-A — found and repaired during the wave: the classifier mislabelled same-boot field failures

At snapshot `9585151`, `JOURNAL_JQ_TAIL`’s `else` branch (`:924` then) checked only that every
element was an object with a nonempty string `_BOOT_ID`, then returned
`if $b > 1 then "multi-boot" else "boot-mismatch" end`. It never compared to `$boot`, so a
**correct-boot** record failing an identity/field condition was labelled `boot-mismatch`.
Evaluated directly with that filter (`jq -s -r --arg boot BOOT13 --arg id fe6faa94…`):

| input | 9585151 output | required |
|---|---|---|
| correct BOOT13 + `MESSAGE_ID=d989611b…` | `boot-mismatch` | `record-invalid` |
| foreign boot + correct `MESSAGE_ID` | `boot-mismatch` | `boot-mismatch` |
| `_BOOT_ID` as array | `record-invalid` | `record-invalid` |

The delivered `journal: record identity mismatch` case expects `record-invalid`, so at `9585151`
that case failed, and a correct-boot wrong `EXIT_STATUS`/`COREDUMP_SIGNAL` was also mislabelled.

**Repaired at `ce2752a`** (`:926`) with the equivalent condition

```sh
... unique) as $b | if $b > 1 then "multi-boot"
  elif all(.[]; ._BOOT_ID == $boot) then "record-invalid"
  else "boot-mismatch" end ...
```

Re-tested by direct jq evaluation: correct-boot/wrong-id → `record-invalid`; foreign boot →
`boot-mismatch`; array `_BOOT_ID` → `record-invalid`; valid stream → `N<TAB>N<TAB>boot`; empty →
`0<TAB>0<TAB>none`; two foreign boots → `multi-boot`. Keep the identity case permanently: it is
the regression for this exact misclassification. The lesson for the fixture matrix is that the
reason vocabulary is only useful if a same-boot field failure and a boot failure are separated;
otherwise `boot-mismatch` becomes a catch-all and an operator cannot tell a spoofed/foreign
stream from a malformed record.

### D-B — cursor identity is a named residual (L1 decision); fixture fidelity is still improvable

The delivered fixtures (`jrec`, `:2732-2736` at the earlier snapshot) omit `__CURSOR`,
`__REALTIME_TIMESTAMP` and `__MONOTONIC_TIMESTAMP`, all of which journalctl always prints
(O7/S014 `:680`). Consequences:
1. **L1 has decided** there is no cursor identity abstraction this round: records are counted as
   parsed, and a duplicated/replayed line would be counted twice. This is a named residual, not a
   defect to fix here; do not add a cursor-uniqueness condition without an L1 decision (it would
   also force every fixture record to carry a unique cursor). Record it in the residual list (§9)
   and in the knowledge note’s "delivery paths this cannot see" so the count is not presented as
   deduplicated.
2. **Optional fixture fidelity:** making `jrec` emit the mandatory address fields would make the
   positive fixtures shape-faithful to real journalctl (and would prove the parser tolerates
   them), but it changes every expected count only if `__CURSOR` values collide. If adopted,
   generate `"__CURSOR":"s=jf;i=<n>;b=<boot>"` per record and keep the counts unchanged. Not
   required for the round.

### D-C — `cmd=` shape is a stated limitation; class-concrete argv is in CensusFix’s report

At `0f2faa2` the row publishes
`journalctl --$scope -b --no-pager -o json --output-fields=_BOOT_ID,MESSAGE_ID[,...] MESSAGE_ID=<id>`
(`:1106`). CensusFix’s report now carries three class-concrete replayable argv forms (four
MESSAGE_ID-only classes; `segfault_signal11` with `MESSAGE_ID`+`COREDUMP_SIGNAL`; `unit_sigkill`
with `MESSAGE_ID`+`EXIT_CODE`+`EXIT_STATUS`). The row keeps a shape because one row aggregates six
queries; that limitation is stated rather than fixed. Residual clarity points: `MESSAGE_ID=<id>`
requires the reader to take the class ID from the finding, and `--no-pager` remains while
ReviewEvidence B8 expects it absent. Nothing here is unsafe; it is a provenance-clarity gap
(criterion 9), recorded for the carrying commit.

### D-D — `boot-conflict` (closed at `0f2faa2`)

The earlier probe compared per-scope boot ids across classes, but every filter already required
`_BOOT_ID == $boot`, so two classes could not disagree unless the anchor was empty (then no
counting happened). The branch was dead. It is removed at `0f2faa2`; the per-scope boot is now
simply the validated `JQ_BOOT`. Keep it out unless a filter is added that does not enforce the
anchor — otherwise the reason token becomes a false vocabulary entry.

### D-E — severity policy recorded; L1 ratifies at integration

All notice classes are info; only `user:unit_sigkill_record` is warn. The retired text
`OOM_KILL_JOURNAL` was crit, so a user-scope kernel-OOM unit notice alone now leaves the roll
CLEAN. CensusFix recorded the rationale: the old crit was text-asserted and is not carried onto a
per-unit notice (round-12 M19); `CGROUP_OOM_KILL` stays crit as the trusted local cgroup counter in
its own scope; a per-unit SIGKILL record keeps the old text class’s warn roll behavior. That is
defensible and now stated in `CensusFix.md`; L1 should confirm it in the round record. If the old
DRIFT path is wanted anyway, set `user:kernel_oom_notice` to crit; fixture P1’s expected verdict
flips to DRIFT.

### D-F — two delivered disclosures have no assertion (recorded residual)

`JOURNAL_CLASSES_UNMEASURED` (info, `:1032`) and the row’s `unmeasured=` token (`:1120`) are not
checked anywhere. A refactor could delete the coverage-loss disclosure silently. Recorded as a
named residual for the carrying commit; G13 is the case to add there.

### D-G — `no-timeout-bin` branch untested (recorded residual)

`:943-947` returns `no-timeout-bin` when `timeout` is absent; no case drives it (the tmux suite has
the analogous case). Recorded for the carrying commit; G12.

### D-H — valid-empty zeros are only partly asserted (recorded residual)

The rebuilt `clean: empty journal` now pins both `ok` rows, three class zeros each, and
`boot=unavailable:no-records`. It does not assert `segfault_signal11=0`,
`unit_sigkill_record=0`, `unit_failure_record=0`, or the absence of class findings. Extend it
(G1) at the carrying commit rather than add another case.

### D-I — scope summation is not asserted (recorded residual)

The matrix case has user 3 + system 5; nothing forbids `count=8` or a `total=`. Extension G11 at
the carrying commit.

### D-J — `MESSAGE` keys are tolerated (deliberate) — residual, not a blocker

Every matrix record carries `"MESSAGE":"MORI_JOURNAL_CANARY"`, and the record is counted; the
canary assertion proves nothing is echoed. The gate therefore relies on `--output-fields` as the
primary control and on never printing capture bytes, not on a `MESSAGE`-key refusal. This is
acceptable for safety (no leak), but it means a contract-violating producer is still counted.
If fail-closed is preferred, add `(has("MESSAGE") | not)` to each filter’s outer condition and
expect `record-invalid`; that flips the matrix case’s canary records to unavailable, so the
fixtures must then use a separate canary case. Pick one and document it.

### D-K — presentation

`field=user:MESSAGE_ID` reads like a scope-prefixed field name; `identity_field=MESSAGE_ID` or
`identity_fields=MESSAGE_ID` is clearer. The row-level `unit=notice` is qualified by
`notice_classes=`/`record_classes=`, so it is not false, but a reader skimming `unit=notice` next
to `unit_sigkill_record=1` can misread it; the finding’s `unit=record` is the authoritative label.

---

## 6. Gap matrix — 11 new cases + 2 extensions (deferred to the carrying commit)

These are the cases to add at integration, not edits to the frozen wave: CensusFix recorded them
as named residuals and L1 owns the integrated run. The expectations below are written against the
delivered grammar so the carrying commit can add them mechanically and recompute the tally.

All cases build on `fx_quiet` + `mkdir -p "$FX/root"`; `BOOT13=0123456789abcdef0123456789abcdef`
is already in `sut_env` (`MORI_BOOT_ID`). Slot names at the snapshot: `kernel_oom`, `oomd`,
`coredump`, `unit_sigkill`, `unit_failure`, `segfault`. `jrec` = the delivered helper (BOOT13,
MESSAGE canary). Assertions use `check` plus a backward-compatible `--forbid` separator (one PASS
per case; absence patterns are checked against the same `$OUT_FILE`).

| # | fixture | rc/verdict | must contain | forbid |
|---|---|---|---|---|
| G1 (extend `clean: empty journal`) | all 12 class slots present, empty, rc0 | 0 CLEAN | both `^SURFACE journal\.(user\|system): ok`, all six class zeros, `boot=unavailable:no-records` | the six class finding ids, `KILL_SIGNAL_JOURNAL`, `UNIT_FAILURE_JOURNAL`, `unavailable:` |
| G2 | `journal-user-kernel_oom` empty rc0, `.err` = `No journal files were opened due to insufficient permissions.` | 0 CLEAN | `journal.user: unavailable`, `kernel_oom_notice=unavailable:stderr-nonempty` | `kernel_oom_notice=0`, `KERNEL_OOM_NOTICE_JOURNAL_USER` |
| G3 | 2 `jrec` kernel_oom records, `.rc`=1 | 0 CLEAN | `journal.user: unavailable`, `kernel_oom_notice=unavailable:rc-1`, `rc=1` | `KERNEL_OOM_NOTICE_JOURNAL_USER`, `kernel_oom_notice=2` |
| G4 | 1 `jrec` kernel_oom record, `.rc`=141 | 0 CLEAN | `kernel_oom_notice=unavailable:rc-141` | `KERNEL_OOM_NOTICE_JOURNAL_USER`, `count=1` |
| G5 | one unterminated `{"_BOOT_ID":"BOOT13","MESSAGE_ID":"fe6faa94…","MESSAGE":"MORI_TRUNC_CANARY` in `journal-user-coredump`, rc0 | 0 CLEAN | `coredump_notice=unavailable:malformed-json` | `COREDUMP_NOTICE_JOURNAL_USER`, `count=1`, `MORI_TRUNC_CANARY` |
| G6 | `{"_BOOT_ID":["BOOT13"],"MESSAGE_ID":"fe6faa94…"}` in `journal-user-kernel_oom`, rc0 | 0 CLEAN | `kernel_oom_notice=unavailable:record-invalid` | `kernel_oom_notice=1`, `KERNEL_OOM_NOTICE_JOURNAL_USER` |
| G7 | `{"_BOOT_ID":"BOOT13","MESSAGE_ID":["fe6faa94…","d989611b…"]}`, rc0 | 0 CLEAN | `kernel_oom_notice=unavailable:record-invalid` (after D-A patch) | `kernel_oom_notice=1` |
| G8 (not a case — named residual) | two identical records with the same `__CURSOR` in `journal-user-kernel_oom`, rc0 | — | current behavior: `kernel_oom_notice=2`, finding `count=2`; this is **accepted** per L1 (no cursor identity abstraction this round) | do not assert unavailable; record the residual in the knowledge note and report |
| G9 | 2 `jrec` kernel_oom records; `journal-user-coredump` empty rc3; rest empty | 0 CLEAN | `journal.user: unavailable`, `kernel_oom_notice=2`, `coredump_notice=unavailable:rc-3`, `rc=3`, `FINDING KERNEL_OOM_NOTICE_JOURNAL_USER .*count=2` | `COREDUMP_NOTICE_JOURNAL_USER` |
| G10 | 5 `jrec` kernel_oom records; all six system slots empty rc1 | 0 CLEAN | `FINDING KERNEL_OOM_NOTICE_JOURNAL_USER .*count=5`, `journal.system: unavailable`, each system class `unavailable:rc-1` | any `_SYSTEM` finding, `count=10` |
| G11 (extend existing matrix) | user kernel_oom=3, system kernel_oom=5 | 1 DRIFT | existing assertions unchanged | `count=8`, `total=`, `sum=` |
| G12 | quiet fixture; `EXTRA_ENV=(MORI_TIMEOUT_BIN=/nonexistent/timeout)` | 0 CLEAN | both rows `unavailable`, `kernel_oom_notice=unavailable:no-timeout-bin` | the six class findings |
| G13 | quiet fixture | 0 CLEAN | `FINDING JOURNAL_CLASSES_UNMEASURED severity=info`, `classes=oom_kill_text,other_signals,other_unit_failure_text`, row `unmeasured=oom_kill_text,other_signals,other_unit_failure_text` | any class finding |
| G14 | `journal-user-kernel_oom` = `kernel: Out of memory: Killed process 4242 status=9/KILL` rc0 | 0 CLEAN | `kernel_oom_notice=unavailable:malformed-json` | `KERNEL_OOM_NOTICE_JOURNAL_USER`, `KILL_SIGNAL_JOURNAL`, `count=0` |

G1/G2 pin the empty-vs-denied boundary (O1/O5). G3/G4 pin producer-failure/partial-stream refusal
(O6; QUALITY 6/7). G5-G7 pin malformed/truncated/array handling; G8 records the accepted cursor
residual rather than an action. G9/G10 pin per-class and
per-scope independence with a positive count. G13 pins the coverage-loss disclosure. G14 proves
legacy text served to a structured query cannot become a count.

Expected journal-check count: 14 delivered + 11 new = 25 (G1 and G11 are assertion extensions;
G8 is a named residual, not a case). The total selftest tally must be recomputed from the printed
`MORI_CENSUS_SELFTEST: … (N cases, …)` at the carrying commit (QUALITY 20); this file does not
claim a measured total.

---

## 7. Reconciliation with the round plan and the knowledge note

- **Six classes vs three + signal-11.** The delivered set is broader than the item prompt and
  keeps `KILL_SIGNAL_JOURNAL` (warn, user) and `UNIT_FAILURE_JOURNAL` (info) on catalog bases
  (`98e32220…`, `d9b373ed…`), which is the strongest answer to the prompt’s "preserve existing
  user finding ids where meaningful" and to ReviewCensus B6’s coverage-loss objection. The two
  new IDs are catalog-verified (O11); the SIGKILL class is field-qualified, not the bare ID.
- **`-b` current boot.** Delivered code uses `-b` (equivalent to `-b 0`), matching `SKILL.md:17`
  "current-boot anchor". This resolves the `-b all` line in
  `corpus/knowledge/structured-journal-scopes-r13.md:54` in favor of the claim; the knowledge note
  should be corrected (its own `[UNKNOWN]` admits the live count was not measured).
- **Knowledge-note class table vs code.** The note (`:41-45`) lists `coredump_abnormal_notice`
  (`1f4e0a44…`) and `journal_loss_notice` (`e9bf28e6…`); the code instead implements
  `unit_sigkill_record` and `unit_failure_record` and the signal-11 class. Both sets are
  defensible; they are not the same claim. `JournalKnowledge`/L1 must reconcile the note with the
  delivered class set (either add the two note classes or remove them from the expected table).
- **Kernel victims remain out.** `SCORECARD.md:644-649` still describes a "system-journal
  kernel-OOM count probe … 5 retained records"; `PROVINCE.md:31` narrows FR1 to notice records and
  keeps kernel attribution frontier. Kernel records carry no `MESSAGE_ID` (EvidenceScribe E10:
  0 hits in 48,173 records), and text matching them is barred by criterion 15. The delivered
  `unmeasured=oom_kill_text` disclosure is the correct treatment. The scorecard line needs a
  sweep by its owner; do not call `fe6faa94…` a kernel record.
- **Severity.** See D-E. Record the policy explicitly: notices are context (info); the crit
  kernel-kill path is `CGROUP_OOM_KILL`; the warn user-SIGKILL record preserves the old text
  class’s roll behavior.

---

## 8. Drift / volatile contract

Delivered counter keys: `kernel_oom_notice`, `oomd_notice`, `coredump_notice`,
`segfault_signal11`, `unit_sigkill_record`, `unit_failure_record` (plus the pre-existing list).
Observed at `ce2752a` (`:1986-1998`): all six are present in `DRIFT_COUNTER_KEYS`. No prefix
collision: `oom`/`count` do not match `oomd_notice=`/`kernel_oom_notice=`/`count`-prefixed
tokens. The boot id is echoed as `boot=<32hex>` and `boot=unavailable:no-records`; the normalizer
has the mask `s/\bboot=[^ ;)]*/boot=<V>/g` (`:2014`) and `boot` is in `DRIFT_VOLATILE_SPECIAL`
(`:2000`), so reboots are masked and a missing/changed boot token still surfaces structurally.
`rc`, `scope`, `unit`, class tokens, reason tokens and `unmeasured=` must **not** be masked: a
class turning unavailable must surface as drift. Verify that the mask is not so broad that it
hides a *changed* reason on a `boot=` token; it masks the whole value, which is the intended
volatile behavior.

Expected drift families against `corpus/evidence/baseline-r10-20261015T2231Z.json` (not a measured
list): `volatile_fields`, `-SURFACE:journal +SURFACE:journal.user +SURFACE:journal.system`,
`-FINDING:OOM_KILL_JOURNAL` (old text line gone), the old `KILL_SIGNAL_JOURNAL`/`SEGFAULT_JOURNAL`/
`UNIT_FAILURE_*` lines changed in place (ids kept, observations changed), `+FINDING:
JOURNAL_CLASSES_UNMEASURED`, plus new field keys. No re-pin this round without a recorded reason.

---

## 9. Residuals / delivery paths this design cannot see

1. Kernel victim records (`Killed process`, `oom-kill:constraint=`) are not counted (no stable
   `MESSAGE_ID`; text barred). `unmeasured=oom_kill_text` discloses it; FR1 remains partial.
2. `MESSAGE_ID`, `EXIT_CODE`, `EXIT_STATUS`, `COREDUMP_SIGNAL` are client-set (S015). A spoofed
   record can raise a finding; it cannot hide a real one. `trust=client-supplied` is printed.
3. Journal loss/rate limiting (`e9bf28e6…`) and retention/vacuum bound every count; a count is
   records in a readable scope, not complete event history.
4. **No cursor identity abstraction (L1 decision):** records are counted as parsed, so a
   duplicated or replayed stream would count twice. This is a named residual, not this round’s
   fix; the count must not be described as deduplicated.
5. One event can produce notices in both scopes; scopes are never summed, and a notice is not a
   unique victim (`kill-classes-by-message-id-r12.md:16-18`).
6. oomd service state is not read: a zero `oomd_notice` is "no matching record in this readable
   scope, this boot", not "no oomd kills" and not "oomd inactive" (ReviewCensus M2; `SKILL.md:29`
   requires inactive ≠ healthy zero in prose). A `service=` token would need a systemctl read the
   fixture environment does not stub; out of scope, named here.
7. The `-b` + `_BOOT_ID == anchor` check trusts journalctl’s boot filter; a producer that forges
   the anchor would pass. This is a contract check, not authentication.
8. The 2 s per-query bound is a LOCAL placeholder (like the tmux bound); a very large store can
   grade `timeout`, which is unavailable, not zero. Re-measure before reusing elsewhere.
9. Fixture counts are synthetic; live current-boot counts today are 0 (O2). The 7/9/1585/1 values
   (O3/O4) are retained-boot history, not current state and not fixture expectations.

---

## 10. Proposed L1 checks (not run by this seat)

1. `bash tools/mori-census.sh --selftest` → PASS; recompute the tally; zero shell diagnostics.
2. `bash tools/mori-census.sh` live → both rows, six class tokens each, `boot=` equal to
   `/proc/sys/kernel/random/boot_id` dash-stripped, no `MESSAGE` text, rc 0 today.
3. Direct jq check of the D-A patch (three single-record inputs above) before the integrated run;
   then the identity-mismatch case must pass.
4. Stub mutations: rc1+records, rc141+records, rc0+denied `.err`, truncated JSON, array
   `_BOOT_ID` → each grades unavailable and the census output contains no sentinel/`MESSAGE` text.
   Do not expect a duplicate-cursor refusal: cursor identity is a named residual (§9).
5. `bash tools/mori-census.sh --drift corpus/evidence/baseline-r10-20261015T2231Z.json` → exit 1
   with the §8 token families (not 2, not 0); old baseline kept.
6. `bash tools/mori-silence-cases.sh` → `matched=28 total=28`, exit 0.
7. Record `sha256sum tools/mori-census.sh tools/mori-silence-cases.sh` and the logs as the round
   receipt (QUALITY 20/23).

---

## 11. Bottom line for CensusFix

- The delivered architecture matches the measured contract: six structured classes per scope,
  split stderr, bounded queries, normalized boot anchor, no `MESSAGE` echo, per-class
  independence, never summed.
- D-A is closed at `ce2752a`: the classifier now separates a same-boot field/identity failure
  (`record-invalid`) from a stream that is on another boot (`boot-mismatch`). Keep the delivered
  `journal: record identity mismatch` case as its permanent regression.
- D-C, D-F/G/H/I and the G1-G14 matrix are **deferred to the carrying commit** per CensusFix’s
  frozen-wave decision; CensusFix’s report records them as named residuals, and this report is the
  mechanical case list. They are cheap, deterministic, and each closes a named channel rather
  than adding breadth theater.
- L1 ratifies D-E’s recorded severity policy in the round record, and reconciles the knowledge
  note’s class table with the delivered six classes (§7).

Tool installs/updates this seat: none. Commits: none. Builds/tests/lint/format/smoke runs: none.
Production files untouched; this report is the only write.
