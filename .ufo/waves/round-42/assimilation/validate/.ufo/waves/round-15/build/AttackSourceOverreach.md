# AttackSourceOverreach — r15 C1: do the source fields support the alarm policy?

Seat: `MoriR15.AttackSourceOverreach` (critic, report only). Nothing was executed and no production
file was edited. Installs: none.

Axes: **coverage** (judged). I also checked whether any C1 wording overclaims **calibration** or
**provenance**.

Production at read time: `tools/mori-census.sh#DC7D`. It has no `positive_*` tokens yet, so the
attack targets the contract plus the current anchors.

Sources reopened this round (systemd commit `cf8ebfc6…`; man pages are systemd 262):

- S014 `journalctl.html`
- S015/S037 `systemd.journal-fields.html`
- S036 `src/core/unit.c`
- S038 `src/core/service.c`
- Supporting files, not cited in the S038 row:
  - `src/core/scope.c`
  - `src/core/unit.h`
  - `src/core/cgroup.c`
  - `systemd.service.html`

## Verdict

The C1 claim holds. The per-record predicate is a sound way to read these fields, and it adds no
new way to forge an alarm. A single forged scalar record already fires the alarm in r14, so r15
only removes suppression by injecting a bad neighbour record.

There are three source overreaches. All are fixable in docs or wording; none is a reason to reject:

- **CE1:** most of the edge cases the fixtures use to break the aggregate cannot come from a
  journalctl that follows its own filters. That is acceptable only if the positive predicate is
  self-contained.
- **CE2:** S038 anchors only the service result vocabulary. The one OOM actually seen on this host
  came through a scope unit.
- **CE3/CE4:** the source shows that "positive" counts record presence. It is not a count of
  events, failures or SIGKILL deliveries.

## CE1 — poison records a conforming journalctl cannot return (provenance; fixable)

**Counterexample.** These fixture records cannot be produced by a conforming journalctl:

- `ForeignBoot.json` `foreignboot_user_kernel_mixed`: a current-boot record next to a foreign
  `_BOOT_ID`.
- `KernelUser.json` `kernuser_wrong_oomd_id_retains_valid_oom`: a record with a different
  `MESSAGE_ID`.
- `kernuser_missing_message_id_*`: a record with no `MESSAGE_ID`.
- `UnitUser.json` `unituser_msgid_object_*`: `MESSAGE_ID` as a JSON object.
- `BootArray.json`: `_BOOT_ID` as an array or null.

Each one needs a producer that ignores its own match terms.

**Evidence.**

- S014 `-b`: "Show messages from a specific boot. This will add a match for `_BOOT_ID=`". An empty
  argument means the current boot. The probe always passes `-b` and `MESSAGE_ID=<id>`
  (`mori-census.sh:1072`, `:1194-1219`).
- S015 Trusted Journal Fields: underscore fields "cannot be altered by client code". So a
  `_BOOT_ID` array or null cannot come from a client.
- S014 JSON encoding rules give the only realistic shapes for a bad neighbour:
  1. A field over 4096 bytes is printed as `null`.
  2. A field that repeats in one entry becomes a JSON array.
  3. Non-printable or non-UTF-8 values become arrays of byte numbers.

  Real JSON output never prints a scalar field value as an object or a number.

So the realistic poison is a client-repeated field. Example: a same-uid process sends
`MESSAGE_ID=fe6faa94… MESSAGE_ID=d9b373ed…`. That single record matches both the kernel query and
the unit query, prints as an array, and makes both raw classes unavailable. The same applies to
`UNIT_RESULT`, `EXIT_CODE` and `EXIT_STATUS` arrays, and to arrays that contain a byte-array
element. That journalctl matches an entry when any value of a repeated field matches is
[INFERENCE], based on S014 rule 2 and the match semantics.

**Why it matters.** A positive is safe on a stream that broke its own filter only if the jq
predicate re-checks every match term itself. The terms are scalar `MESSAGE_ID == $id`, scalar
`_BOOT_ID == $boot`, and, for the process class, `EXIT_CODE == "killed"` and `EXIT_STATUS` = 9.
The predicate must not rely on journalctl having already filtered.

Concrete mutant: the process predicate checks only id and boot "because the query already matched
`EXIT_CODE=killed EXIT_STATUS=9`". It would then count `{"EXIT_CODE":"killed","EXIT_STATUS":["15","9"]}`.
The NegativeStatus and ProcessUser array cases catch this mutant. Keep them.

**Defect, if present:** any r15 claim, knowledge or SKILL text that says journalctl returns
foreign-boot or mismatched-id records as a measured frequency. AttackFixtureOracle makes the same
realism point about the stub.

**Smallest correction.**

1. In `corpus/knowledge/journal-positive-evidence-r15.md`, label the foreign-boot, wrong-id,
   missing-id, object-id and boot-array cases as defense against a non-conforming producer.
   Name multi-valued client fields (S014 rules 1–3) as the only source-realistic poison.
2. In production, compute the positive vector with
   `select(type=="object" and (.MESSAGE_ID|type)=="string" and .MESSAGE_ID==$id and (._BOOT_ID|type)=="string" and ._BOOT_ID==$boot and <class terms>)`.
   It must run in the same jq pass, in both the valid and the invalid branch.
   - Today the invalid branch (`:973`, `:1037`) emits only a reason string.
   - `journal_query` returns early on that string (`:1103-1105`).
   - The positive must survive that early return without changing `JQ_STATUS`.

## CE2 — S038 anchors only `service.c`, but the real OOM path was a scope (coverage; fixable)

**Counterexample.** The one OOM recorded on this host was
`app-Hyprland-xdg-terminal-exec-dd9e67bd.scope: Failed with result 'oom-kill'`
(`corpus/knowledge/observability-census-r1.md:94`). That is a **scope** unit.

Desktop apps run in `app-*.scope`, so the realistic `positive_unit_oom` path goes through scopes.
The S038 row (`corpus/SOURCES.md:44`) cites only `src/core/service.c:6588-6602`
(`[SERVICE_FAILURE_OOM_KILL] = "oom-kill"`).

**Evidence that the predicate is still right.** Scopes write the same structured record:

- `scope.c:725` has `[SCOPE_FAILURE_OOM_KILL] = "oom-kill"`.
- `scope_enter_dead` calls `unit_log_result(...)` at `scope.c:273`.
- `unit_log_result` (`unit.h:1058-1062`) calls `unit_log_failure`.
- `unit_log_failure` (`unit.c:6333-6341`) logs `MESSAGE_ID` `d9b373ed…` with
  `UNIT_RESULT=%s`.

So the exact-string `oom-kill` predicate covers scopes. Only the citation is missing.
ReconResultEmitter (`build/ReconResultEmitter.md:170-184`) found `scope.c` but did not get it into
SOURCES.

Second gap from the same file: a scope with `OOMPolicy=continue` never fails
(`scope.c:585-586` returns before the result is set). There `positive_unit_oom=0` is expected even
when a kernel OOM notice (`fe6faa94`) exists. A zero is not evidence of absence.

**Smallest correction.**

- The knowledge doc should cite `scope.c:725`, `scope.c:273`, `unit.h:1058-1062` and
  `unit.c:6333-6341` next to S038, and state: "exact string `oom-kill`, independent of unit type".
- The IndexPositive seat may extend the S038 anchor cell; this is not a new row.
- The production predicate does not change.

## CE3 — one kernel OOM produces several positives (calibration; already fenced; keep it so)

**Evidence.**

- `cgroup.c:3075-3103`: the kernel OOM notice is logged once each time the cgroup's `oom_kill`
  counter grows (`c > crt->oom_kill_last`). One notice can therefore cover more than one kill.
- Right after the notice, `unit_notify_cgroup_oom(u, false)` runs. With the default stop policy it
  sets the result to `oom-kill`: services at `service.c:4722-4752`, scopes at `scope.c:589-599`.
  A later `unit_log_failure` then writes that result.

**Counterexample.** One kernel kill in a user scope gives `user_positive_kernel_oom=1` and
`user_positive_unit_oom=1`. It also gives hierarchy fan-out across user and system (the 5 kills
vs 7 user notices vs 9 system notices measured in r13).

`OOM_KILL_JOURNAL` fires once (`:1330-1331`), so the alarm is correct. The risk is that a reader
adds the positive tokens together or reads `positive_kernel_oom` as a count of kernel kills.

**Smallest correction.** Name the tokens and notes as counts of records or notices. Never put a
summed or `total` field next to them. Keep the `:1331` "not a unique-victim" note as it is.

## CE4 — a process-SIGKILL record is not a failure (calibration; residual tradeoff)

**Evidence.**

- `unit_log_process_exit` (`unit.c:6365-6390`) writes `EXIT_CODE` and `EXIT_STATUS` even when
  `success` is true; it then logs at `LOG_DEBUG`.
- No structured field records success. Only `PRIORITY` and the `MESSAGE` suffix " (success)" show
  it.
- systemd.service(5) documents `SuccessExitStatus=… SIGKILL`: "the termination signal SIGKILL [is]
  considered clean".

**Counterexample.** A user unit with `SuccessExitStatus=SIGKILL`, under a manager at debug log
level, writes a `98e32220…` record with `killed` and `9`. That record makes
`positive_process_sigkill=1` and fires the user WARN, but the manager counted the exit as a
success.

Assumption [INFERENCE]: the user manager's default level is `info`, so the debug line is normally
not emitted. Any same-uid process could forge the same record anyway (CE6).

**Classification.** A tradeoff, not a defect. The current note, "unit process exited on SIGKILL"
(`:1353`), is accurate.

**Smallest correction.** Do not describe `positive_process_sigkill` as a failure or an unexpected
kill. Requesting `PRIORITY` in the same query is future work, because it changes the query.

## CE5 — the `signal` result is not SIGKILL (calibration; wording guard)

**Evidence.** `service.c:4781-4782`: any main-process `CLD_KILLED` that is not a clean exit maps to
`SERVICE_FAILURE_SIGNAL`, which is the string `signal`. Clean exits are SIGHUP, SIGINT, SIGTERM,
SIGPIPE and the `SuccessExitStatus=` list (systemd.service(5)). Socket, mount and swap units also
use `signal` for control-process deaths, and those tables are not cited. The scope table has no
`signal` entry (`scope.c:721-726`).

**Smallest correction.** `positive_unit_signal` must never be labelled or summed as SIGKILL. Keep
`process_sigkill` and `user_unit_signal` as separate counters, as `:1353` already does.

## CE6 — authentication: no new forgery path; KILL line lacks the trust marker (concur)

**Evidence.** S015: "the journal service does not validate the values of any structured journal
fields whose name is not prefixed with an underscore". In the user scope, any same-uid process
writes into the same journal file as the user manager.

r14 already lets one valid forged scalar record fire the alarm, through the all-valid aggregate. r15
adds no forgery path; it removes the injection-suppression path. `KILL_SIGNAL_JOURNAL` (`:1353`) has
no `trust=client-supplied` marker, but `OOM_KILL_JOURNAL` (`:1331`) does. SecurityTrust F4 and
SecurityPrivacy P6 found the same gap; I agree with both.

**Smallest correction.** Add `trust=client-supplied` to the KILL line. Describe positives as
shape-and-boot checked only. Do not use "validated", "verified" or "authenticated" without that
qualifier.

Binding system-scope records to their emitter (`_PID=1`) is future work and is not claimed.

## Residual (S014; not an r15 defect)

S014: "`--user` only works if persistent logging is enabled". With `Storage=volatile`, the user
scope returns a valid empty stream: rc 0 and `positive_*=0`. The user manager's notices then sit in
the system journal. The existing `absent_records=possible:no-retained-record-is-not-no-event`
covers this, and it must stay on both rows.

## Required behavior (smallest, ordered)

1. The positive predicate re-checks every journalctl match term per record, with scalar types. It
   runs in the same jq pass as the raw check and survives the `record-invalid` early return at
   `:1103-1105` without changing raw `JQ_STATUS` (CE1).
2. The knowledge doc separates realistic poison (multi-valued, byte-array and null-encoded client
   fields) from producer-non-conformance cases (CE1).
3. Cite the `oom-kill` path for scope units (`scope.c:725`, `scope.c:273`, `unit.h:1058-1062`,
   `unit.c:6333-6341`) next to S038 (CE2).
4. Positive tokens count record presence. No summing, no `total`, no failure or SIGKILL relabelling
   (CE3–CE5).
5. Put `trust=client-supplied` on every line that carries a positive, including `:1353` (CE6).

The canonical judge should not reject on any of these. Items 1 and 5 are fixable production
details. Items 2–4 are documentation and wording.
