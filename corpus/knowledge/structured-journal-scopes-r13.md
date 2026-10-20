source: S013 — https://raw.githubusercontent.com/systemd/systemd/cf8ebfc6159cf0b3b99aa9a0164ccb07c4c9c5af/catalog/systemd.catalog.in — pinned commit cf8ebfc6159cf0b3b99aa9a0164ccb07c4c9c5af (2026-10-19), fetched 2026-10-20, sha256 e53707db7e6963b284e504dc17f36a4d5a2bdb4bd8a9611b2cf95c075ad86592: `e9bf28e6…` :58-64 loss notice, `fc2e22bc…` :66-75 coredump notice, `fe6faa94…` :604-616 kernel-OOM unit notice, `1f4e0a44…` :870-881 abnormal-termination notice, `d989611b…` :884-894 systemd-oomd notice; S035 — https://raw.githubusercontent.com/systemd/systemd/cf8ebfc6159cf0b3b99aa9a0164ccb07c4c9c5af/catalog/systemd.catalog.in — same pinned commit cf8ebfc6, catalog/systemd.catalog.in:561-575, scope “structured process-termination and unit-result identifiers”: `d9b373ed…` :561-566 unit-failure notice, `98e32220…` :568-575 unit-process-exit notice, opened 2026-10-20, sha256 e53707db7e6963b284e504dc17f36a4d5a2bdb4bd8a9611b2cf95c075ad86592; S036 — https://raw.githubusercontent.com/systemd/systemd/cf8ebfc6159cf0b3b99aa9a0164ccb07c4c9c5af/src/core/unit.c — src/core/unit.c:6333-6392, `unit_log_failure` :6333-6342 and `unit_log_process_exit` :6355-6392 emitter schemas (level policy, `LOG_MESSAGE_ID`, `UNIT_RESULT`, `EXIT_CODE`, `EXIT_STATUS`), opened 2026-10-20, sha256 4833056a6313b250ad6b53de3121a51e8dee602733e1aedf4a7d3d2687d547ed; same-commit supporting reads opened 2026-10-20: src/systemd/sd-messages.h :178-185 sha256 fb613f71807344eb29b9353cad8c09cb644fff4a18b1651fda9b49e0a23064fc, src/basic/process-util.c :2306-2315 sha256 a749f285bf168bdbb74bc7021055e8f121ec7a0bbbcb6a40e40283f5f699a4fe
verified-at: 2026-10-20 — source openings at base 6531ac6; L1 fixture and live measurements against c13df48 (census SHA-256 39abda0a67028575d888d9157b8548dec0b4944c3d8c165691e88ab657fc3985).
recheck: curl -fsSL https://raw.githubusercontent.com/systemd/systemd/cf8ebfc6159cf0b3b99aa9a0164ccb07c4c9c5af/catalog/systemd.catalog.in | grep -nE '^-- (e9bf28e6|fc2e22bc|fe6faa94|1f4e0a44|d989611b|d9b373ed|98e32220)'; curl -fsSL https://raw.githubusercontent.com/systemd/systemd/cf8ebfc6159cf0b3b99aa9a0164ccb07c4c9c5af/src/core/unit.c | grep -nF 'EXIT_CODE=%s'; curl -fsSL https://raw.githubusercontent.com/systemd/systemd/cf8ebfc6159cf0b3b99aa9a0164ccb07c4c9c5af/src/systemd/sd-messages.h | grep -nE 'UNIT_PROCESS_EXIT_STR|UNIT_FAILURE_RESULT_STR'; curl -fsSL https://www.freedesktop.org/software/systemd/man/latest/journalctl.html | grep -nF 'id="--output-fields="'; curl -fsSL https://www.freedesktop.org/software/systemd/man/latest/journalctl.html | grep -nF 'JSON array is used as field value'; curl -fsSL https://www.freedesktop.org/software/systemd/man/latest/systemd.journal-fields.html | grep -nF 'id="MESSAGE_ID="'; curl -fsSL https://www.freedesktop.org/software/systemd/man/latest/systemd.journal-fields.html | grep -nF 'cannot be altered by client code' → catalog 58,66,561,568,604,870,884; unit.c 6388; sd-messages 178,185; journalctl 230; journalctl 215; fields 40; fields 83

## Claim
Count journal OOM/crash/exit classes by catalog `MESSAGE_ID` in one explicitly labelled journal scope per query, with `-o json` and `--output-fields` restricted so no `MESSAGE` is emitted. The IDs are different units: `fe6faa94…` is a unit notice that the kernel OOM killer killed a process, `d989611b…` is a systemd-oomd notice for "one or more processes", and `fc2e22bc…` / `1f4e0a44…` are coredump notices; none is a per-victim kill counter. A systemd-observed signal-9 exit is countable only through the structured `98e32220…` record filtered `EXIT_CODE=killed` / `EXIT_STATUS=9`; it names no sender or cause. `d9b373ed…` is a unit-result record, not a kill count. User and system scopes are labelled separately and never summed. A zero `d989611b…` record count is a record count, not evidence that systemd-oomd is active or healthy; service activity stays `unmeasured` here. This is a partial FR1 advance: it measures notice and exit records, not kernel victims, a per-process roll-up, or fleet-caused kills.

Adjacent: `corpus/knowledge/kill-classes-by-message-id-r12.md` owns the measured 2026-10-19 scoped counts (5 kernel victim records, 7 user notices, 9 system notices, one boot) and the notice-versus-victim unit boundary. This note adds source mechanics for scope, boot, field and trust labelling; it does not re-measure and does not close kernel attribution or fleet correlation.

## Evidence
- S013 `fe6faa94e7774663a0da52717891d8ef` `:604-616`: subject “A process of @UNIT@ unit has been killed by the OOM killer.”; body “killed by the Linux kernel out-of-memory (OOM) killer logic”. The entry is unit-scoped and does not identify a process count. The same body says “the memory pressure might or might not have been caused by @UNIT@”, so the notice does not establish cause. The catalog names only `Defined-By: systemd`; it does not name the emitting component.
- S013 `d989611b15e44c9dbf31e3c81256e4ed` `:884-894`: subject “systemd-oomd killed one or more processes in unit @UNIT@”; body “One or more processes in the @UNIT@ unit have been killed by systemd-oomd”. One record can stand for several processes; it is a userspace-oomd notice, not a kernel record and not a process count.
- S035 (same pinned catalog bytes as S013, separate scope) `d9b373ed55a64feb8242e02dbe79a49c` `:561-566`: subject “Unit failed”; body “The unit @UNIT@ has entered the 'failed' state with result '@UNIT_RESULT@'.” A unit-result record, not a kill count; `@UNIT_RESULT@` may encode a non-signal failure. `98e322203f7a4ed290d09fe03c09fe15` `:568-575`: subject “Unit process exited”; body “An @COMMAND@= process belonging to unit @UNIT@ has exited.” and “The process' exit code is '@EXIT_CODE@' and its exit status is @EXIT_STATUS@.” This is the structured signal path: filter `EXIT_CODE=killed` and `EXIT_STATUS=9`; the class also fires for ordinary exits, so the filter is mandatory.
- S036 `src/core/unit.c:6333-6392`: `unit_log_failure` `:6333-6342` logs at `LOG_WARNING` with `LOG_MESSAGE_ID(SD_MESSAGE_UNIT_FAILURE_RESULT_STR)` and `UNIT_RESULT=%s`; `unit_log_process_exit` `:6355-6392` sets the level at `:6372-6377` to DEBUG on success, NOTICE for `code == CLD_EXITED`, and WARNING otherwise, and `:6379-6391` emits `LOG_MESSAGE_ID(SD_MESSAGE_UNIT_PROCESS_EXIT_STR)` with `EXIT_CODE=%s` from `sigchld_code_to_string(code)`, `EXIT_STATUS=%i`, `COMMAND=%s` and the unit invocation ID. Same-commit supporting reads: `sd-messages.h:185` maps `SD_MESSAGE_UNIT_PROCESS_EXIT_STR` to `98e32220…`, `:178-179` maps `SD_MESSAGE_UNIT_FAILURE_RESULT` to `d9b373ed…`, and `process-util.c:2306-2309` maps `CLD_KILLED` to “killed”. Limit: neither record names a signal sender or OOM cause; both exist only for processes under a systemd manager that observes the event.
- S013 `fc2e22bc6ee647b6b90729ab34a250b1` `:66-75`: subject “Process @COREDUMP_PID@ (@COREDUMP_COMM@) dumped core”; body “crashed and dumped core”. S013 `1f4e0a44a88649939aaea34fc6da8c95` `:870-881`: subject “Process @COREDUMP_PID@ (@COREDUMP_COMM@) terminated abnormally”. Both are crash/coredump notices, not OOM-kill classes; neither may be added to a kill-class count.
- S013 `e9bf28e6e834481bb6f48f548ad13606` `:58-64`: subject “Journal messages have been missed”; body “Kernel messages have been lost as the journal system has been unable to process them quickly enough.” A notification class exists for loss, so the journal is not a complete event history.
- S015 User Journal Fields `:33`: “User fields are fields that are directly passed from clients and stored in the journal.” `MESSAGE=` `:34-36`: the field “is not supposed to be parsed for metadata”. `MESSAGE_ID=` `:40-42`: “A 128-bit message identifier ID for recognizing certain message types”; it is “recommended to be a UUID-compatible ID, but this is not enforced”. Therefore a `MESSAGE_ID` match is a client-supplied type label, not authenticated producer identity and not trusted origin evidence.
- S015 Trusted Journal Fields `:83-84`: “Fields prefixed with an underscore are trusted fields, i.e. fields that are implicitly added by the journal and cannot be altered by client code.” `_BOOT_ID=` `:100` is the kernel boot ID; `_TRANSPORT=` `:106` lists valid transports, with `kernel` “for those read from the kernel” (`:128`). These are the fields that can carry trusted scope/origin context when a query requests them.
- S014 Source Options `:71`: `--system` shows system services and the kernel; `--user` shows the current user's service messages; with neither, journalctl shows “all messages that the user can see”, interleaving accessible journals. The access paragraph (`:57-58`) says “only root and users who are members of a few special groups are granted access to the system journal”, and Source Options says `--user` “only works if persistent logging is enabled, via the Storage= setting in journald.conf(5)” (`:75-76`).
- S014 `-k` `:192`: “This adds the match _TRANSPORT=kernel.” and “This implies --boot=0 unless explicitly specified otherwise.” S014 `--boot` adds a `_BOOT_ID=` match. A kernel-record class therefore has an implicit current-boot default that must be stated or overridden.
- S014 `--after-cursor=` `:121`: “Start showing entries from the location in the journal after the location specified by the passed cursor.” S015 `__CURSOR=` `:196`: an “opaque text string that uniquely describes the position of an entry”, portable across machines, platforms and journal files.
- S014 `json` `:209`: “formats entries as JSON objects, separated by newline characters”. `:215`: “if a non-unique field is encountered a JSON array is used as field value”. S014 `--output-fields=` `:230`: the option affects only full-field modes and `cat`; for those, the `__CURSOR`, `__REALTIME_TIMESTAMP`, `__MONOTONIC_TIMESTAMP` and `_BOOT_ID` fields are always printed. A count-only query can therefore request `_BOOT_ID` and still never receive `MESSAGE`.
- S014 `-q` `:257`: suppresses “any warning messages regarding inaccessible system journals when run as a normal user”. S014 `Exit status` `:352`: “On success, 0 is returned; otherwise, a non-zero failure code is returned.” The page enumerates no permission-specific code, and suppressed warnings mean stderr silence is not an access proof.

## Observed
The source inventory contains seven relevant catalog IDs: loss, ordinary/abnormal coredump, OOM-unit, oomd, unit-failure and unit-process-exit records. S014/S015 specify scope, field output and trust; S035/S036 specify process-result metadata. This source-opening section does not re-measure the round-12 5/7/9 sample. That sample is historical, text-selected where `--grep` was used, not a current-boot or authenticated unique-kill count (see the round-13 errata in the two round-12 notes).

## [INFERENCE]
Catalog and process-result field matches can classify retained records without matching MESSAGE. `_BOOT_ID` anchors the query to a boot, not to a unique victim or trusted emitter. All non-underscore classification fields remain client-supplied. Therefore a zero match count means only no retained matches in that scope/boot; `oomd_activity=unmeasured` explicitly prevents turning zero notices into a service-health or zero-kill claim.

## [UNKNOWN]
Cross-scope duplicate identity, retention completeness, silent partial access, record/victim cardinality, signal senders and fleet causation are not established by these counts. Some legitimate multi-valued journal fields serialize as arrays; the implementation refuses the whole class rather than offering a misleading partial count. Duplicate identical records are counted twice. Cursor rotation/vacuum behavior and cross-boot ordering remain FR11. A boot-scoped zero does not assert that a killer was active, disabled or inactive.

## Implemented query contract — census-r6

The census emits two independent surfaces, `journal.user` and `journal.system`,
with six per-scope class counters. The source inventory's abnormal-coredump and
journal-loss IDs are knowledge-only; they are not extra implemented counters.

| counter | exact match | unit / interpretation |
|---|---|---|
| `kernel_oom_notice` | MESSAGE_ID=fe6faa94e7774663a0da52717891d8ef | record carrying a kernel-OOM unit-notice ID, not a kernel victim |
| `oomd_notice` | MESSAGE_ID=d989611b15e44c9dbf31e3c81256e4ed | notice record; `oomd_activity=unmeasured` |
| `coredump_notice` | MESSAGE_ID=fc2e22bc6ee647b6b90729ab34a250b1 | coredump notice, not an OOM kill |
| `segfault_signal11` | same coredump ID and COREDUMP_SIGNAL=11 | signal-specific coredump record |
| `unit_sigkill_record` | MESSAGE_ID=98e322203f7a4ed290d09fe03c09fe15 EXIT_CODE=killed EXIT_STATUS=9 | systemd-observed process-result record; sender/cause unknown |
| `unit_failure_record` | MESSAGE_ID=d9b373ed55a64feb8242e02dbe79a49c | failed-unit result record, no fleet classification |

Every query uses `journalctl <--user|--system> -b --no-pager -o json
--output-fields=_BOOT_ID,MESSAGE_ID[,...] <field matches>`. Signal classes add
only their numeric field metadata to output. MESSAGE and COMMAND are never
requested. The actual argv is constructed by `probe_journal`/`journal_query`;
the row's `cmd=` is a class-template description, not a copy/paste command.

Every counted record must match the normalized current boot from
`/proc/sys/kernel/random/boot_id` (`MORI_BOOT_ID` fixture override). Queries
are bounded by local `MORI_JOURNAL_TIMEOUT_S=2` plus the one-second timeout
kill grace. Twelve serial queries therefore have a 36-second producer-bound
ceiling, excluding parsing and the other census surfaces; this is not a
whole-census wall-time guarantee. Missing timeout refuses the query.

Stdout and stderr are captured separately; any nonzero rc, stderr bytes,
malformed JSON, wrong boot or class identity makes that class unavailable.
Parser diagnostics and record payloads are never echoed. A successful empty
stream is a zero record count. A readable subset with no diagnostics can still
look like a complete query: full journal readability is not claimed.

Positive user `unit_sigkill_record` retains `KILL_SIGNAL_JOURNAL` WARN and the
DRIFT path; the same system class is INFO. Other classes are INFO. Scopes are
never summed. Unsupported text-only arbitrary signal/unit-failure paths are
explicitly unmeasured. Removing the unreliable text count is a correction,
not proof that cgroup counters cover the removed journal paths.

## What it changes for mori
SKILL.md decision/error rows and PROVINCE.md Core now describe the delivered scoped-record contract rather than the entering user-only text probe. FR1 advances only the structured system-journal notice/result plane; kernel victim-token attribution and fleet correlation remain frontier. The round-13 behavioral and live receipts named below measure this implementation; the historical base is `6531ac6`, not an after-state claim.

## Delivery paths this cannot see
Catalog `MESSAGE_ID` counts cannot see: processes outside a systemd manager, or a SIGKILL the manager did not observe; a signal-9 exit's sender or cause (the `98e32220…` record carries `EXIT_CODE`/`EXIT_STATUS` only); signals other than those producing a retained exit record; unit failures outside these IDs; kernel OOM victims whose notice was not emitted or not retained; journal records lost to rate limiting or loss (`e9bf28e6…`, and the rate-limit text at catalog `:54-56`); records outside the queried boot, retention window or vacuumed files; an inaccessible system journal (permission) or an unavailable user journal (`Storage=`); cursor invalidation after rotation. `fc2e22bc…`/`1f4e0a44…` observe crashes, not kills. `d989611b…` observes oomd actions, not other userspace killers, and a zero is not service health. `d9b373ed…` observes a unit result, not a kill. `fe6faa94…` observes a unit notice, not a unique victim, and explicitly not the cause of memory pressure. `MESSAGE_ID` itself is client-settable, so no count proves producer identity, and none proves a fleet lane caused a host event.

## Fills (coverage-map ground; Frontier row)
Coverage-map ground: MESSAGE-free structured journal notice-class counts with independent user/system scope labels and exact boot context, plus the systemd-observed signal-9 exit class and its cause blindness. Frontier FR1: partial advance only — notice and exit records are countable per scope, but kernel victim attribution, per-process roll-up, signal-sender identity and fleet correlation remain frontier. FR11: cursor mechanics documented (`--after-cursor=`, opaque `__CURSOR`), with rotation/vacuum behavior still unknown.

## Measured round-13 receipt

L1 ran `python3 tools/mori-round13-regressions.py --mutation both --jobs 1
--output .ufo/waves/round-13/evidence/regressions-accepted`: 19 contract checks
passed, 2 exact-locus mutations reproduced the old defects, exit 0. C1's five
checks cover system positives 2/1/3/3, user zeros, independent user positives
3/0/1/1, MESSAGE-canary exclusion, and the full scoped-row/CLEAN contract.
The census selftest observed 91/91, including scope-error and positive user
SIGKILL-warning cases (`evidence/census-selftest.json` under the same wave).

Live source-counter comparison: execute the `python` member retained in
`.ufo/waves/round-13/evidence/live-measurement.json` (its `reproduce` command
is executable). Twelve independently queried class/scope cells bracketed the
census and matched 12/12; all were zero in the named current boot. Explicit
scoped journal surfaces increased 0 → 2 versus frozen r12 bytes. This proves
live query and label operation, not observation of a new real kill.
One interleaved full-census pair took 3.025310 s old / 2.960516 s new; one pair
is not a latency distribution or a speedup claim.

Counting command, from the lane root:
`jq '[.result.baseline.stdout,.result.delivered.stdout] | map(split("\n") | map(select(startswith("SURFACE journal."))) | length)' .ufo/waves/round-13/evidence/live-measurement.json`
→ `[0,2]`, measured against c13df48 and frozen base 6531ac6.
