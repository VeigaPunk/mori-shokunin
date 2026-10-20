# ScopedFixtures — minimal scoped journal fixtures for the r14 alarm/routing repair

Seat: `MoriR14.ScopedFixtures` (executor, leaf).
Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin`.
Milestone: restore the OOM alarm and structured fleet routing. Axis judged: **coverage**.

## Write scope and method

This report is my only write in the lane. I made no production edits and no commits. I did not run the census, its selftest, the gates or the oracle; those are the main verification, which L1 owns. What I did run were bounded empirical fixture probes, described next.

Every expected value below comes from one of two kinds of bounded empirical probe. Neither replaces the gates and selftests:

1. **Fixture filter probes.** I extracted the census's own filter strings (`JOURNAL_JQ_MSGID`, `_SIGKILL`, `_SIGSEGV`, `_UNITS`, `FLEET_UNIT_TOKENS`) from the working tree, and from `HEAD`, which equals the frozen r13 bytes. I evaluated them with `jq -s` over the synthetic records. The served stream was built with real journalctl semantics: AND across `FIELD=value` match words, then projection onto `--output-fields` plus the always-printed fields. These probes exercise the filter strings only. They do not run the census process, so its rows, findings, verdict and rc are not probed. Finding and verdict expectations (§4.5, §5) come from reading the emitter code and await the gates and selftests.
2. **Count-only host reads.** These were MESSAGE-free `journalctl` reads of this host's retained journals (§2). No host unit name is quoted.

### Snapshots

All files below were under concurrent sibling edits. Re-anchor at the delivered SHA.

| file | sha256 at last read | note |
|---|---|---|
| `tools/mori-census.sh` (working tree) | `0e41cb83fce2e8c5c711171e1cde2e6fa2809dcfce630eccabe52bcbe41516d9` | All five filter strings (`JOURNAL_JQ_MSGID`, `_SIGKILL`, `_SIGSEGV`, `_UNITS`, `FLEET_UNIT_TOKENS`) were byte-identical at `97b8d66f…`, `e8b6fd70…` and `0e41cb83…`. Every vector here was computed on that filter set and re-checked at `0e41cb83…`. |
| `HEAD:tools/mori-census.sh` | `39abda0a67028575d888d9157b8548dec0b4944c3d8c165691e88ab657fc3985` | The frozen r13 delivered census. Matches `.ufo/waves/round-14/frozen/expected.json`. |
| `tools/mori-round14-regressions.py` | `82010d1c…` / `26eeb412…` | JournalRegression's gate. |
| `tools/mori-round13-regressions.py` | `821ad74d…` | |

## 1. Result

**Fixture M** has 21 source records, all MESSAGE-free:

- 18 counted records and 3 near-miss records.
- Every one of the 12 scoped counters is nonzero.
- Every class has a different count in each scope (user/system):

  | class | user | system |
  |---|---|---|
  | kernel | 1 | 2 |
  | oomd | 2 | 1 |
  | coredump | 3 | 1 |
  | segfault | 2 | 1 |
  | sigkill | 1 | 2 |
  | failure | 2 | 4 |

- Fleet and non-fleet subjects appear in both scopes.
- The OOM alarm is fed from both sources in both scopes.
- Each subject field matches what this host actually records for that scope and class (§2).

**Fixture probe results** (bounded; L1's gates and selftests are the main verification).

- The current filters give exactly the 6 class tokens plus 12 unit tokens expected in each scope.
- The r13 `HEAD` filters give the **same six counts**, so the scoped-count gains are preserved.
- Stripping every non-requested field (projection) changes no vector.
- Embedding a canary in every subject name changes no vector.

**Discrimination.** I simulated six census selector mutations (§4.8):

- M detects all six.
- The gate's `R14_SCOPED_PARITY` as first read detected 1 of 6.
- After JournalRegression adopted my near-miss records, it detects 6 of 6.

**Other content.**

- 13 single-record arms, plus a three-record incident arm (I1) and an empty control (E0), each with r14 and frozen-r13 expectations (§5).
- 25 subject/result shape arms with exact unit-split vectors (§6).
- Helper realism findings (§7).
- A knowledge correction: slice units do emit `fe6faa94…` notices (§8).

**Coordination outcome** (each change was reported by its owning seat; I did not re-check the slot lines of the second CensusRepair edit):

- CensusRepair moved user arms to `USER_UNIT` and made its matrix fill all 12 cells. It then added a strict `coredump_notice > segfault_signal11` line.
- JournalRegression replaced the non-vocabulary `UNIT_RESULT="failed"` with `resources`. It also added the sig6, killed/15 and exited/9 near-misses and `USER_UNIT` user arms.
- KnowledgeRepair applied the slice correction to the knowledge note (reported by that seat).

## 2. Live grounding (count-only, MESSAGE-free)

### Command shape

For each scope S and catalog id I:

```sh
timeout -k 1 20 journalctl --S -b all -q --no-pager -o json \
  --output-fields=_BOOT_ID,MESSAGE_ID,UNIT,USER_UNIT,COREDUMP_UNIT,COREDUMP_USER_UNIT,UNIT_RESULT,EXIT_CODE,EXIT_STATUS,COREDUMP_SIGNAL \
  MESSAGE_ID=I | jq -s '<has()/type/equality counts only>'
```

No `MESSAGE` was requested and only integers were printed. `-b all` covers all retained boots, not the current boot.

### Results

| scope | id | records | `UNIT` only | `USER_UNIT` only | both | neither | non-string subject | `COREDUMP_*` subject | `UNIT_RESULT=oom-kill` | killed/9 | `COREDUMP_SIGNAL=11` |
|---|---|---|---|---|---|---|---|---|---|---|---|
| user | fe6faa94 | 7 | 0 | 7 | 0 | 0 | 0 | 0 | – | – | – |
| user | d989611b | 0 | | | | | | | | | |
| user | fc2e22bc | 1585 | 0 | 0 | 0 | 1585 | 0 | 1585 (all carry both `COREDUMP_UNIT` and `COREDUMP_USER_UNIT`) | – | – | 46 |
| user | 98e32220 | 4606 | 0 | 4606 | 0 | 0 | 0 | 0 | – | **0** | – |
| user | d9b373ed | 4609 | 0 | 4609 | 0 | 0 | 0 | 0 | **4** | – | – |
| system | fe6faa94 | 9 | 9 | 0 | 0 | 0 | 0 | 0 | – | – | – |
| system | d989611b | 0 | | | | | | | | | |
| system | fc2e22bc | 1 | 0 | 0 | 0 | 1 | 0 | 1 (`COREDUMP_UNIT` only) | – | – | 0 |
| system | 98e32220 | 0 | | | | | | | | | |
| system | d9b373ed | 1 | 1 | 0 | 0 | 0 | 0 | 0 | **1** | – | – |

### Supplementary counts

- **Invocation IDs.** User manager records carry `USER_INVOCATION_ID` (7/7, 4606/4606, 4609/4609). System manager records carry `INVOCATION_ID` (9/9, 1/1).
- **Transport.** Every counted record has `_TRANSPORT=journal`.
- **Coredump signal.** `COREDUMP_SIGNAL` is present as a string on 1585/1585 user and 1/1 system coredump records.
- **Subject unit types of `fe6faa94…` notices.**
  - user (7): slice 3, service 2, scope 2.
  - system (9): slice 4, service 5.
- **Always-printed fields.** A real JSON line on this host (systemd 261) also printed `__SEQNUM` and `__SEQNUM_ID`, besides the four fields S014 lists as always printed.

### Consequences for fixtures

1. **Realistic subject field per scope.** User scope uses `USER_UNIT`; system scope uses `UNIT`. Cross-scope shapes (`UNIT` in the user journal, `USER_UNIT` in the system journal) were observed 0 times out of 9,222 user and 10 system manager records. Keep them only as synthetic scope-independence arms.
   - `[INFERENCE]` A user manager running under a system UID could put `USER_UNIT` into the system journal. This was not observed here.
2. **Coredump records are not manager records.** Their subject fields are `COREDUMP_UNIT` and, in user scope, `COREDUMP_USER_UNIT`. In user scope `COREDUMP_UNIT` is the user manager `user@<uid>.service`.
   - S015 ("Fields to log on behalf of a different program") says of `COREDUMP_UNIT=` and `COREDUMP_USER_UNIT=`: "Used to annotate messages containing coredumps from system and session units."
   - Putting `UNIT`/`USER_UNIT` on `fc2e22bc…` records is an unrealistic shape.
3. **Real process-exit records are almost never SIGKILL.** None of 4606 user `98e32220…` records is killed/9. A SIGKILL fixture should include non-SIGKILL exits as near-misses.
4. **`UNIT_RESULT=oom-kill` occurs on this host.** Retained journals hold 4 user and 1 system record. I did not measure the current boot.
5. **Value types.** Every retained subject and selector value is a JSON string. Arrays (duplicate fields), byte arrays (non-UTF8) and null (fields over 4096 bytes) are possible per S014 but were not observed. They belong only in negative arms.

## 3. Record grammar (minimal, MESSAGE-free)

### Common fields

- `_BOOT_ID` is the fixture boot `0123456789abcdef0123456789abcdef`. This is `BOOT13` in the census selftest and `JOURNAL_BOOT` in the gates.
- `MESSAGE_ID` is the catalog id.
- All values are JSON strings.
- No `MESSAGE`, `COMMAND` or `_SYSTEMD_*` field is needed.

### Per class

| class token | `MESSAGE_ID` | selector fields (required) | subject at source (user / system) | fields the census requests |
|---|---|---|---|---|
| `kernel_oom_notice` | `fe6faa94e7774663a0da52717891d8ef` | – | `USER_UNIT` / `UNIT` | `_BOOT_ID,MESSAGE_ID` |
| `oomd_notice` | `d989611b15e44c9dbf31e3c81256e4ed` | – (optional `N_PROCESSES`, cgroup.c:3039-3043) | `USER_UNIT` / `UNIT` | `_BOOT_ID,MESSAGE_ID` |
| `coredump_notice` | `fc2e22bc6ee647b6b90729ab34a250b1` | `COREDUMP_SIGNAL` (any) | `COREDUMP_UNIT` + `COREDUMP_USER_UNIT` / `COREDUMP_UNIT` | `_BOOT_ID,MESSAGE_ID` |
| `segfault_signal11` | same coredump id | `COREDUMP_SIGNAL="11"` | same as coredump | `_BOOT_ID,MESSAGE_ID,COREDUMP_SIGNAL` |
| `unit_sigkill_record` | `98e322203f7a4ed290d09fe03c09fe15` | `EXIT_CODE="killed"`, `EXIT_STATUS="9"` | `USER_UNIT` / `UNIT` | `_BOOT_ID,MESSAGE_ID,EXIT_CODE,EXIT_STATUS` |
| `unit_failure_record` | `d9b373ed55a64feb8242e02dbe79a49c` | `UNIT_RESULT` from the vocabulary | `USER_UNIT` / `UNIT` | `_BOOT_ID,MESSAGE_ID,UNIT,USER_UNIT,UNIT_RESULT` |

### `UNIT_RESULT` vocabulary

From the pinned `cf8ebfc6…` sources. `unit_log_failure` is called with `*_result_to_string(s->result)`, e.g. service.c:2518 and socket.c:2118.

| unit type | table location | values |
|---|---|---|
| service | `service.c:6588` | success, resources, protocol, timeout, exit-code, signal, core-dump, watchdog, start-limit-hit, oom-kill, exec-condition |
| scope | `scope.c:721` | success, resources, timeout, oom-kill |
| timer | `timer.c:1079` | success, resources, start-limit-hit |
| socket | `socket.c:3660` | (socket's own table) |
| mount | `mount.c:2481` | (mount's own table) |
| automount | `automount.c:1164` | (automount's own table) |
| path | `path.c:1000` | (path's own table) |
| swap | `swap.c:1620` | (swap's own table) |

**No table contains `failed`.**

### Optional realism fields

These are never read by the census and are stripped by projection: `__CURSOR`, `__REALTIME_TIMESTAMP`, `__MONOTONIC_TIMESTAMP`, `__SEQNUM`, `__SEQNUM_ID`, `_TRANSPORT=journal`, and `USER_INVOCATION_ID` (user) or `INVOCATION_ID` (system).

### Projection rule

Real journalctl serves only:

- the requested `--output-fields`;
- plus `__CURSOR`, `__REALTIME_TIMESTAMP`, `__MONOTONIC_TIMESTAMP` and `_BOOT_ID` (S014: those fields "are always printed");
- plus `__SEQNUM` and `__SEQNUM_ID`, observed on systemd 261.

Consequences:

- Only the `unit_failure` query ever sees subject metadata.
- The other five classes carry subject metadata at the source, but the census cannot see it.
- So a correct fixture must give the same output with or without that metadata. This was verified for all 12 cells (§4.7).

## 4. Fixture M (12 nonzero scoped cells, realistic subjects)

### 4.1 Source records — what the journal holds

The **user** journal holds 10 records:

```jsonl
{"_BOOT_ID":"0123456789abcdef0123456789abcdef","MESSAGE_ID":"fe6faa94e7774663a0da52717891d8ef","USER_UNIT":"kagi-shokunin.service"}
{"_BOOT_ID":"0123456789abcdef0123456789abcdef","MESSAGE_ID":"d989611b15e44c9dbf31e3c81256e4ed","USER_UNIT":"app-browser-r14.scope"}
{"_BOOT_ID":"0123456789abcdef0123456789abcdef","MESSAGE_ID":"d989611b15e44c9dbf31e3c81256e4ed","USER_UNIT":"app-chat-r14.scope"}
{"_BOOT_ID":"0123456789abcdef0123456789abcdef","MESSAGE_ID":"fc2e22bc6ee647b6b90729ab34a250b1","COREDUMP_SIGNAL":"11","COREDUMP_UNIT":"user@1000.service","COREDUMP_USER_UNIT":"app-editor-r14.scope"}
{"_BOOT_ID":"0123456789abcdef0123456789abcdef","MESSAGE_ID":"fc2e22bc6ee647b6b90729ab34a250b1","COREDUMP_SIGNAL":"11","COREDUMP_UNIT":"user@1000.service","COREDUMP_USER_UNIT":"app-viewer-r14.scope"}
{"_BOOT_ID":"0123456789abcdef0123456789abcdef","MESSAGE_ID":"fc2e22bc6ee647b6b90729ab34a250b1","COREDUMP_SIGNAL":"6","COREDUMP_UNIT":"user@1000.service","COREDUMP_USER_UNIT":"app-term-r14.scope"}
{"_BOOT_ID":"0123456789abcdef0123456789abcdef","MESSAGE_ID":"98e322203f7a4ed290d09fe03c09fe15","EXIT_CODE":"killed","EXIT_STATUS":"9","USER_UNIT":"kagi-shokunin.service"}
{"_BOOT_ID":"0123456789abcdef0123456789abcdef","MESSAGE_ID":"d9b373ed55a64feb8242e02dbe79a49c","UNIT_RESULT":"oom-kill","USER_UNIT":"kagi-shokunin.service"}
{"_BOOT_ID":"0123456789abcdef0123456789abcdef","MESSAGE_ID":"d9b373ed55a64feb8242e02dbe79a49c","UNIT_RESULT":"signal","USER_UNIT":"pipewire-pulse.service"}
{"_BOOT_ID":"0123456789abcdef0123456789abcdef","MESSAGE_ID":"98e322203f7a4ed290d09fe03c09fe15","EXIT_CODE":"killed","EXIT_STATUS":"15","USER_UNIT":"app-term-r14.scope"}
```

The **system** journal holds 11 records:

```jsonl
{"_BOOT_ID":"0123456789abcdef0123456789abcdef","MESSAGE_ID":"fe6faa94e7774663a0da52717891d8ef","UNIT":"ufo-sighting.service"}
{"_BOOT_ID":"0123456789abcdef0123456789abcdef","MESSAGE_ID":"fe6faa94e7774663a0da52717891d8ef","UNIT":"user@1000.service"}
{"_BOOT_ID":"0123456789abcdef0123456789abcdef","MESSAGE_ID":"d989611b15e44c9dbf31e3c81256e4ed","UNIT":"NetworkManager.service"}
{"_BOOT_ID":"0123456789abcdef0123456789abcdef","MESSAGE_ID":"fc2e22bc6ee647b6b90729ab34a250b1","COREDUMP_SIGNAL":"11","COREDUMP_UNIT":"cups.service"}
{"_BOOT_ID":"0123456789abcdef0123456789abcdef","MESSAGE_ID":"98e322203f7a4ed290d09fe03c09fe15","EXIT_CODE":"killed","EXIT_STATUS":"9","UNIT":"ufo-sighting.service"}
{"_BOOT_ID":"0123456789abcdef0123456789abcdef","MESSAGE_ID":"98e322203f7a4ed290d09fe03c09fe15","EXIT_CODE":"killed","EXIT_STATUS":"9","UNIT":"NetworkManager.service"}
{"_BOOT_ID":"0123456789abcdef0123456789abcdef","MESSAGE_ID":"d9b373ed55a64feb8242e02dbe79a49c","UNIT_RESULT":"oom-kill","UNIT":"ufo-sighting.service"}
{"_BOOT_ID":"0123456789abcdef0123456789abcdef","MESSAGE_ID":"d9b373ed55a64feb8242e02dbe79a49c","UNIT_RESULT":"resources","UNIT":"the-tick.timer"}
{"_BOOT_ID":"0123456789abcdef0123456789abcdef","MESSAGE_ID":"d9b373ed55a64feb8242e02dbe79a49c","UNIT_RESULT":"oom-kill","UNIT":"NetworkManager.service"}
{"_BOOT_ID":"0123456789abcdef0123456789abcdef","MESSAGE_ID":"d9b373ed55a64feb8242e02dbe79a49c","UNIT_RESULT":"core-dump","UNIT":"cups.service"}
{"_BOOT_ID":"0123456789abcdef0123456789abcdef","MESSAGE_ID":"98e322203f7a4ed290d09fe03c09fe15","EXIT_CODE":"exited","EXIT_STATUS":"9","UNIT":"backup-r14.service"}
```

#### Near-miss records

The census queries exclude these three by design:

- user sig6 coredump (excluded from the segfault count);
- user `killed/15`;
- system `exited/9`.

#### Why the subjects look the way they do

- **User incident.** The `kagi-shokunin.service` trio is the realistic kernel-OOM sequence in a fleet service: a notice, a SIGKILL exit and an `oom-kill` failure. It must yield one OOM line, the KILL warn and a fleet route. It must never produce a "3 kills" total.
- **System notice fan-out.** The `user@1000.service` system notice is the ancestor fan-out of that same kill. r12 measured 4 such notices.
- **Vocabulary.** `the-tick.timer` uses a timer-legal result (`resources`). `cups.service core-dump` pairs with its sig11 coredump.
- **No closed causal history.** Other records are independent. The fixture is not meant as a complete causal history.

### 4.2 Census selftest form

The selftest dispatcher (`stub/journal-<scope>-<slot>`) serves static slots. Each slot gets the **served projection** of its query, as `jrec` lines (22 lines):

```sh
jrec "$FX/stub/journal-user-kernel_oom" fe6faa94e7774663a0da52717891d8ef
jrec "$FX/stub/journal-user-oomd" d989611b15e44c9dbf31e3c81256e4ed
jrec "$FX/stub/journal-user-oomd" d989611b15e44c9dbf31e3c81256e4ed
jrec "$FX/stub/journal-user-coredump" fc2e22bc6ee647b6b90729ab34a250b1
jrec "$FX/stub/journal-user-coredump" fc2e22bc6ee647b6b90729ab34a250b1
jrec "$FX/stub/journal-user-coredump" fc2e22bc6ee647b6b90729ab34a250b1
jrec "$FX/stub/journal-user-segfault" fc2e22bc6ee647b6b90729ab34a250b1 ',"COREDUMP_SIGNAL":"11"'
jrec "$FX/stub/journal-user-segfault" fc2e22bc6ee647b6b90729ab34a250b1 ',"COREDUMP_SIGNAL":"11"'
jrec "$FX/stub/journal-user-unit_sigkill" 98e322203f7a4ed290d09fe03c09fe15 ',"EXIT_CODE":"killed","EXIT_STATUS":"9"'
jrec "$FX/stub/journal-user-unit_failure" d9b373ed55a64feb8242e02dbe79a49c ',"UNIT_RESULT":"oom-kill","USER_UNIT":"kagi-shokunin.service"'
jrec "$FX/stub/journal-user-unit_failure" d9b373ed55a64feb8242e02dbe79a49c ',"UNIT_RESULT":"signal","USER_UNIT":"pipewire-pulse.service"'
jrec "$FX/stub/journal-system-kernel_oom" fe6faa94e7774663a0da52717891d8ef
jrec "$FX/stub/journal-system-kernel_oom" fe6faa94e7774663a0da52717891d8ef
jrec "$FX/stub/journal-system-oomd" d989611b15e44c9dbf31e3c81256e4ed
jrec "$FX/stub/journal-system-coredump" fc2e22bc6ee647b6b90729ab34a250b1
jrec "$FX/stub/journal-system-segfault" fc2e22bc6ee647b6b90729ab34a250b1 ',"COREDUMP_SIGNAL":"11"'
jrec "$FX/stub/journal-system-unit_sigkill" 98e322203f7a4ed290d09fe03c09fe15 ',"EXIT_CODE":"killed","EXIT_STATUS":"9"'
jrec "$FX/stub/journal-system-unit_sigkill" 98e322203f7a4ed290d09fe03c09fe15 ',"EXIT_CODE":"killed","EXIT_STATUS":"9"'
jrec "$FX/stub/journal-system-unit_failure" d9b373ed55a64feb8242e02dbe79a49c ',"UNIT_RESULT":"oom-kill","UNIT":"ufo-sighting.service"'
jrec "$FX/stub/journal-system-unit_failure" d9b373ed55a64feb8242e02dbe79a49c ',"UNIT_RESULT":"resources","UNIT":"the-tick.timer"'
jrec "$FX/stub/journal-system-unit_failure" d9b373ed55a64feb8242e02dbe79a49c ',"UNIT_RESULT":"oom-kill","UNIT":"NetworkManager.service"'
jrec "$FX/stub/journal-system-unit_failure" d9b373ed55a64feb8242e02dbe79a49c ',"UNIT_RESULT":"core-dump","UNIT":"cups.service"'
```

Notes on this form:

- `jrec` appends `"MESSAGE":"MORI_JOURNAL_CANARY"` to every line. That is a non-semantic leak probe; nothing is counted from it.
- The near-miss records do not appear in any slot. Real journalctl would not return them for these queries.
- The dispatcher ignores `EXIT_*` and `COREDUMP_SIGNAL` match words. So a selector-drop mutation can only be caught by the projecting/filtering gate (§4.8). The exception is a segfault argv drop: that routes to the coredump slot and grades `record-invalid`.

### 4.3 Gate form

Use the r14 gate helpers (`tools/mori-round14-regressions.py`: `jrec`, `kernel_oom`, `sigkill`, `unit_fail`). Records go to `<scope>.records`; the stub filters and projects.

```python
user=(
    kernel_oom(USER_UNIT="kagi-shokunin.service"),
    jrec(OOMD_ID, USER_UNIT="app-browser-r14.scope"),
    jrec(OOMD_ID, USER_UNIT="app-chat-r14.scope"),
    jrec(COREDUMP_ID, COREDUMP_SIGNAL="11", COREDUMP_UNIT="user@1000.service", COREDUMP_USER_UNIT="app-editor-r14.scope"),
    jrec(COREDUMP_ID, COREDUMP_SIGNAL="11", COREDUMP_UNIT="user@1000.service", COREDUMP_USER_UNIT="app-viewer-r14.scope"),
    jrec(COREDUMP_ID, COREDUMP_SIGNAL="6", COREDUMP_UNIT="user@1000.service", COREDUMP_USER_UNIT="app-term-r14.scope"),
    sigkill(USER_UNIT="kagi-shokunin.service"),
    unit_fail(UNIT_RESULT="oom-kill", USER_UNIT="kagi-shokunin.service"),
    unit_fail(UNIT_RESULT="signal", USER_UNIT="pipewire-pulse.service"),
    jrec(SIGKILL_ID, EXIT_CODE="killed", EXIT_STATUS="15", USER_UNIT="app-term-r14.scope"),
),
system=(
    kernel_oom(UNIT="ufo-sighting.service"),
    kernel_oom(UNIT="user@1000.service"),
    jrec(OOMD_ID, UNIT="NetworkManager.service"),
    jrec(COREDUMP_ID, COREDUMP_SIGNAL="11", COREDUMP_UNIT="cups.service"),
    sigkill(UNIT="ufo-sighting.service"),
    sigkill(UNIT="NetworkManager.service"),
    unit_fail(UNIT_RESULT="oom-kill", UNIT="ufo-sighting.service"),
    unit_fail(UNIT_RESULT="resources", UNIT="the-tick.timer"),
    unit_fail(UNIT_RESULT="oom-kill", UNIT="NetworkManager.service"),
    unit_fail(UNIT_RESULT="core-dump", UNIT="cups.service"),
    jrec(SIGKILL_ID, EXIT_CODE="exited", EXIT_STATUS="9", UNIT="backup-r14.service"),
),
```

### 4.4 Expected surface tokens (exact, in emitted order)

**User:**

```
kernel_oom_notice=1 oomd_notice=2 coredump_notice=3 segfault_signal11=2 unit_sigkill_record=1 unit_failure_record=2 unit_fleet=1 unit_nonfleet=1 unit_unknown=0 unit_missing=0 unit_ambiguous=0 unit_malformed=0 unit_oom=1 unit_oom_fleet=1 unit_oom_nonfleet=0 unit_oom_subject_unknown=0 unit_oom_result_unknown=0 unit_signal=1
```

**System:**

```
kernel_oom_notice=2 oomd_notice=1 coredump_notice=1 segfault_signal11=1 unit_sigkill_record=2 unit_failure_record=4 unit_fleet=2 unit_nonfleet=2 unit_unknown=0 unit_missing=0 unit_ambiguous=0 unit_malformed=0 unit_oom=2 unit_oom_fleet=1 unit_oom_nonfleet=1 unit_oom_subject_unknown=0 unit_oom_result_unknown=0 unit_signal=0
```

Both rows `ok`, with `boot=0123456789abcdef0123456789abcdef`.

### 4.5 Expected journal findings

Against the current census (emitters at `0e41cb83…`; anchors moved during the wave).

| id | severity | key tokens |
|---|---|---|
| `JOURNAL_CLASSES_UNMEASURED` | info | always present |
| `OOMD_NOTICE_JOURNAL_USER` | info | `count=2 scope=user` |
| `OOMD_NOTICE_JOURNAL_SYSTEM` | info | `count=1 scope=system` |
| `COREDUMP_NOTICE_JOURNAL_USER` | info | `count=3 scope=user` |
| `COREDUMP_NOTICE_JOURNAL_SYSTEM` | info | `count=1 scope=system` |
| `SEGFAULT_SIGNAL11_JOURNAL_USER` | info | `count=2 scope=user` |
| `SEGFAULT_SIGNAL11_JOURNAL_SYSTEM` | info | `count=1 scope=system` |
| `KILL_SIGNAL_JOURNAL_SYSTEM` | info | `count=2 scope=system` |
| `KILL_SIGNAL_JOURNAL` | **warn** | `paths=process_sigkill,unit_result_signal count=1 process_sigkill=1 user_unit_signal=1 scope=user` |
| `UNIT_FAILURE_JOURNAL` | info | `count=1 subject=fleet owner=mori classification_rule=unit-name-token scope=user` |
| `UNIT_FAILURE_OUT_OF_SCOPE` | info | `count=1 subject=nonfleet owner=tsukuroi scope=user` |
| `UNIT_FAILURE_JOURNAL_SYSTEM` | info | `count=2 subject=fleet scope=system` |
| `UNIT_FAILURE_OUT_OF_SCOPE_SYSTEM` | info | `count=2 owner=tsukuroi scope=system` |
| `OOM_KILL_JOURNAL` | **crit**, exactly 1 line | `paths=kernel_oom_notice,unit_result_oom_kill user_notice=1 user_unit_oom=1 user_unit_oom_result_unknown=0 system_notice=2 system_unit_oom=2 system_unit_oom_result_unknown=0`, with no `count=` |

**Absent:**

- `UNIT_FAILURE_UNATTRIBUTED_JOURNAL`;
- any `KERNEL_OOM_NOTICE_JOURNAL_*` (the per-class loop now skips `kernel_oom_notice`).

**Verdict.** DRIFT, rc 1. Journal-contributed drift lines = 2 (the crit and the warn).

**Frozen r13 (`39abda0a…`) on the same bytes.**

- **Same six counts per scope** (§4.7).
- Every finding is INFO except `KILL_SIGNAL_JOURNAL` warn: `KERNEL_OOM_NOTICE_JOURNAL_USER` count=1 and `_SYSTEM` count=2.
- `UNIT_FAILURE_JOURNAL` count=2: the non-fleet `pipewire-pulse` record is absorbed into the fleet id (the r13 harm).
- `UNIT_FAILURE_JOURNAL_SYSTEM` count=4.
- No `OOM_KILL_JOURNAL`; no `UNIT_FAILURE_OUT_OF_SCOPE*`.
- Verdict DRIFT, because of the warn.

**M therefore discriminates frozen from repaired by finding multiset, not by verdict.** Use the §5 single-record arms when a verdict-level red/green is needed.

### 4.6 Forbidden tokens: scope sums and swaps

No `kernel_oom_notice=3`, `oomd_notice=3`, `coredump_notice=4`, `segfault_signal11=3`, `unit_sigkill_record=3`, `unit_failure_record=6`, `unit_fleet=3`, `unit_nonfleet=3`, `unit_oom=3`. No `count=` on the OOM line. No OOM counter may appear twice.

Subject bytes must never appear in stdout or stderr. Do not grep raw names like `kagi-shokunin`: fixture trees contain that string in paths (`fx_quiet` creates `lanes/kagi-shokunin`, census `:2630`; gate `build_common` creates `root/kagi-shokunin`, gate `:591`). Use the canary variant in §4.10 instead.

### 4.7 Fixture probe evidence (bounded empirical `jq -s` probes of the filter strings)

Current filters (byte-identical at `97b8d66f…`, `e8b6fd70…` and `0e41cb83…`):

| cell | vector |
|---|---|
| user kernel / oomd / coredump / segfault / sigkill | `1 1 B`, `2 1 B`, `3 1 B`, `2 1 B`, `1 1 B` |
| user unit_failure | `2 1 1 0 0 0 0 1 1 0 0 0 1 1 B` |
| system kernel / oomd / coredump / segfault / sigkill | `2 1 B`, `1 1 B`, `1 1 B`, `1 1 B`, `2 1 B` |
| system unit_failure | `4 2 2 0 0 0 0 2 1 1 0 0 0 1 B` |

`B` is the fixture boot. Unit columns: total, fleet, nonfleet, unknown, missing, ambiguous, malformed, oom, oom_fleet, oom_nonfleet, oom_subject_unknown, oom_result_unknown, signal, boots, boot.

Cross-checks:

- **r13 `HEAD` filters.** `unit_failure_record` is a plain MSGID count. They give `1/2/3/2/1/2` user and `2/1/1/1/2/4` system, the same six counts.
- **Projection invariance.** Serving full source records instead of projected ones gives identical vectors in all 12 cells.

### 4.8 Selector-mutation discrimination

Probed with a filtering and projecting stub model, then the census filter. These are simulated mutations of the query shape, not mutated census bytes.

| simulated census mutation | M | gate `R14_SCOPED_PARITY` (first read) | `R14_SCOPED_PARITY` (after adoption, `82010d1c…`) |
|---|---|---|---|
| segfault argv drops `COREDUMP_SIGNAL=11` | detected (user → `record-invalid`) | missed | detected |
| segfault argv drop + jq signal check dropped | detected (user 2→3) | missed | detected |
| sigkill argv drops `EXIT_CODE`/`EXIT_STATUS` | detected (both scopes → `record-invalid`) | missed | detected |
| sigkill argv drops `EXIT_CODE` only, jq status-only | detected (system 2→3, via `exited/9`) | missed | detected |
| sigkill argv drop + jq exit checks dropped | detected (user 1→2, system 2→3) | missed | detected |
| unit query omits `UNIT,USER_UNIT,UNIT_RESULT` from `--output-fields` | detected | detected | detected |

The after-adoption parity vectors from the same probes (user `3/0/2/1/2/1`, system `2/1/4/3/0/2`) equal that case's own declared surfaces. That is an independent cross-check of the gate's expectations.

### 4.9 Minimality

Under the constraints below, M uses the fewest records. The constraints:

1. All 12 cells ≥ 1.
2. User ≠ system for every class, so swaps and sums are visible.
3. `segfault_signal11` ⊆ `coredump_notice`, strictly in at least one scope.
4. Fleet and non-fleet subjects in both scopes, with asymmetric counts.
5. Unit `oom-kill` in both scopes, with asymmetric counts.

The derivation:

| class | per-class floor | records |
|---|---|---|
| kernel, oomd, sigkill | 1/2 or 2/1 | 3 each |
| coredump/segfault | coredump 3/1, segfault 2/1 | 4 |
| unit_failure | user (1 fleet, 1 nonfleet), system (2, 2) | 6 |

That makes 19 slot-distinct records. The segfault records double as coredump records, so the count is 18. The three near-misses are the minimum to expose segfault, `EXIT_STATUS` and `EXIT_CODE` selector drops, giving 21.

**Smaller floor.** The absolute floor is 10 distinct records: one per cell, with segfault reusing coredump. It cannot see scope swaps or the segfault-superset bug.

### 4.10 Canary-embedded variant

Insert `-R14-UNIT-SUBJECT-CANARY` before the unit suffix of every subject value (`UNIT`, `USER_UNIT`, `COREDUMP_UNIT`, `COREDUMP_USER_UNIT`). For example, `kagi-shokunin-R14-UNIT-SUBJECT-CANARY.service` and `the-tick-R14-UNIT-SUBJECT-CANARY.timer`.

- The canary is the gate's `UNIT_CANARY` and contains no fleet token.
- All 12 vectors are unchanged (verified).
- Then assert the canary is absent from raw, pre-redaction stdout and stderr. This makes "no unit bytes" checkable for **valid** classified subjects.
- Today the gate's `R14_SEC_UNIT_CANARY` probes only an invalid, suffix-less name, which takes the malformed path.

## 5. Single-record discriminator arms

Each arm is one record in an otherwise quiet fixture: other slots are empty, i.e. a valid zero.

| arm | record (scope) | r14 expected | frozen r13 expected | proves |
|---|---|---|---|---|
| D1 | `fe6faa94` `USER_UNIT=kagi-shokunin.service` (user) | **DRIFT rc1**; `OOM_KILL_JOURNAL` crit `paths=kernel_oom_notice user_notice=1 … system_notice=0` | CLEAN rc0 (`KERNEL_OOM_NOTICE_JOURNAL_USER` info) | user notice alarm restored |
| D2 | `fe6faa94` `UNIT=user@1000.service` (system) | **DRIFT**; crit `system_notice=1` | CLEAN | system notice alarm; ancestor fan-out shape |
| D3 | `d9b373ed` `UNIT_RESULT=oom-kill USER_UNIT=pipewire-pulse.service` (user) | **DRIFT**; crit `paths=unit_result_oom_kill user_unit_oom=1`; `UNIT_FAILURE_OUT_OF_SCOPE` owner=tsukuroi; no `UNIT_FAILURE_JOURNAL` | CLEAN (`UNIT_FAILURE_JOURNAL`) | alarm independent of the fleet split; non-fleet route |
| D4 | `d9b373ed` `UNIT_RESULT=oom-kill UNIT=ufo-sighting.service` (system) | **DRIFT**; crit `system_unit_oom=1`; `UNIT_FAILURE_JOURNAL_SYSTEM` `subject=fleet` | CLEAN (`UNIT_FAILURE_JOURNAL_SYSTEM`) | system result path; fleet route |
| D5 | `d9b373ed` `UNIT_RESULT=exit-code USER_UNIT=kagi-shokunin.service` (user) | CLEAN; `UNIT_FAILURE_JOURNAL` `subject=fleet owner=mori classification_rule=unit-name-token` | CLEAN, same id, no subject tokens | no-harm control: fleet id kept |
| D6 | `d9b373ed` `UNIT_RESULT=exit-code USER_UNIT=pipewire-pulse.service` (user) | CLEAN; `UNIT_FAILURE_OUT_OF_SCOPE` owner=tsukuroi; **forbid** `UNIT_FAILURE_JOURNAL` | CLEAN; `UNIT_FAILURE_JOURNAL` (the harm) | user non-fleet route, by id |
| D7 | `d9b373ed` `UNIT_RESULT=exit-code UNIT=cups.service` (system) | CLEAN; `UNIT_FAILURE_OUT_OF_SCOPE_SYSTEM`; forbid `UNIT_FAILURE_JOURNAL_SYSTEM` | CLEAN; `UNIT_FAILURE_JOURNAL_SYSTEM` | system non-fleet route |
| D8 | `d9b373ed` `UNIT_RESULT=exit-code`, no subject (user) | CLEAN; `UNIT_FAILURE_UNATTRIBUTED_JOURNAL missing=1 owner=unresolved`; forbid `OUT_OF_SCOPE` and fleet | CLEAN; `UNIT_FAILURE_JOURNAL` | missing subject is unknown, never non-fleet |
| D9 | `98e32220` killed/9 `USER_UNIT=kagi-shokunin.service` (user) | DRIFT; `KILL_SIGNAL_JOURNAL` warn `paths=process_sigkill process_sigkill=1 user_unit_signal=0` | DRIFT (warn) | retained SIGKILL control |
| D10 | `d9b373ed` `UNIT_RESULT=signal USER_UNIT=kagi-shokunin.service` (user) | **DRIFT**; KILL warn `paths=unit_result_signal count=0 user_unit_signal=1`; fleet info | CLEAN | pre-r13 "result signal" warn restored. L1 ruling (F7): `count=0` is valid here because it is the process-SIGKILL count. |
| D11 | `d9b373ed` `UNIT_RESULT=signal UNIT=cups.service` (system) | CLEAN; `UNIT_FAILURE_OUT_OF_SCOPE_SYSTEM`; no KILL warn | CLEAN | system signal result does not warn |
| D12 | `d989611b` `USER_UNIT=app-browser-r14.scope` (user) | CLEAN; `OOMD_NOTICE_JOURNAL_USER` info; **no** `OOM_KILL_JOURNAL` | CLEAN | L1 ruling (F8): an oomd notice alone stays INFO |
| D13 | `fc2e22bc` `COREDUMP_SIGNAL=6 COREDUMP_UNIT=cups.service` (system; coredump slot only) | CLEAN; `coredump_notice=1 segfault_signal11=0`; no SEGFAULT finding | same | strict subset |
| I1 | user incident trio: the first `fe6faa94`, `98e32220` killed/9 and `d9b373ed` oom-kill records of M, all `kagi-shokunin.service` | DRIFT; exactly **one** `OOM_KILL_JOURNAL` (`paths=kernel_oom_notice,unit_result_oom_kill user_notice=1 user_unit_oom=1`), KILL warn, `UNIT_FAILURE_JOURNAL` fleet; no total of 2 or 3 | DRIFT (warn only) | one incident gives one alarm, never a summed kill count |
| E0 | all slots empty | CLEAN; six zeros and 12 unit zeros per scope | CLEAN | existing controls (`clean: empty journal`, gate `R14_BASELINE_EMPTY`) |

### Gate helper form for the arms

- D1 is `user=(kernel_oom(USER_UNIT=FLEET_UNIT),)`.
- D3 is `user=(unit_fail(UNIT_RESULT="oom-kill", USER_UNIT=NONFLEET_UNIT),)`.
- The rest follow the same pattern.

### Census selftest form for the arms

- D1 is `jrec "$FX/stub/journal-user-kernel_oom" fe6faa94e7774663a0da52717891d8ef`.
- D3 is `jrec "$FX/stub/journal-user-unit_failure" d9b373ed55a64feb8242e02dbe79a49c ',"UNIT_RESULT":"oom-kill","USER_UNIT":"pipewire-pulse.service"'`.

### Basis for D12

- **Pre-r13 text predicate.** It was `Out of memory|oom-kill|oom_reaper|Killed process` (frozen census `:874`).
- **oomd notice text.** The pinned text is "systemd-oomd killed … process(es) in this unit." (cgroup.c:3039-3048).
- `[INFERENCE]` The text predicate would not match that notice either, so D12 is no-harm-neutral.
- **The oomd kill still alarms through the unit result.** An oomd kill that fails the unit arrives as `UNIT_RESULT=oom-kill` (D3/D4). Local `/usr/share/doc/systemd/NEWS:8412-8413` says: "Units that were killed by systemd-oomd will now have a service result of 'oom-kill'."
- **L1 ruling (MoriR14).** An oomd notice alone stays INFO, and the unit-result `oom-kill` crit path is mandatory.

## 6. Subject/result shape arms

All are `unit_failure_record`, one record in the user slot unless noted. Each vector lists only the nonzero columns. Every arm has `boots=1` and is a raw count under r13 (`1 1 B`).

### Unknown subject

All of these give `UNIT_FAILURE_UNATTRIBUTED_JOURNAL` and are never fleet or non-fleet.

| arm | subject value | vector |
|---|---|---|
| N1 missing | (no `UNIT`/`USER_UNIT`) | total 1, unknown 1, missing 1 |
| N2 emitter only | `_SYSTEMD_UNIT=user@1000.service`, `_SYSTEMD_USER_UNIT=init.scope` | total 1, unknown 1, missing 1 |
| N3 both present, equal | `UNIT=USER_UNIT=kagi-shokunin.service` | total 1, unknown 1, ambiguous 1 |
| N4 both present, differ | `UNIT=kagi-shokunin.service`, `USER_UNIT=pipewire-pulse.service` | total 1, unknown 1, ambiguous 1 |
| N5 null (S014 oversize encoding) | `USER_UNIT=null` | total 1, unknown 1, malformed 1 |
| N6 duplicate-field array (S014) | `USER_UNIT=["kagi-shokunin.service","kagi-shokunin.service"]` | total 1, unknown 1, malformed 1 |
| N7 non-UTF8 byte array (S014) | `USER_UNIT=[107,97,…,255,46,…]` | total 1, unknown 1, malformed 1 |
| N8 no unit suffix | `kagi-shokunin` | total 1, unknown 1, malformed 1 (fleet token is not enough) |
| N9 space | `kagi shokunin.service` | total 1, unknown 1, malformed 1 |
| N10 256 chars | `"a"*248 + ".service"` | total 1, unknown 1, malformed 1 |
| N11 newline injection | `pipewire-pulse.service\nFINDING OOM_KILL_JOURNAL severity=crit obs=forged` | total 1, unknown 1, malformed 1 |
| N12 empty | `""` | total 1, unknown 1, malformed 1 |
| N14 illegal escape | `kagi-shokunin\q.service` | total 1, unknown 1, malformed 1 |
| N15 short escape | `app-x\x2.scope` | total 1, unknown 1, malformed 1 |

Notes:

- **N2 with a projecting stub.** It only bites if a census starts requesting and reading `_SYSTEMD_*`. With these realistic emitter values, such a census would misroute the record as non-fleet: the r13 harm direction.
- **The gate's own emitter arm.** It uses `EMITTER_UNIT=kagi-shokunin.service`, which tests the false-fleet direction. Keep both directions.
- **N11 and N14 checks.** Also assert that a `FINDING` line for `OOM_KILL_JOURNAL` appears only when expected, and that exactly one `MORI_CENSUS:` line is printed.

### Valid subject

| arm | subject value | vector |
|---|---|---|
| N13 255 chars | `"a"*247 + ".service"` | total 1, nonfleet 1 |
| X1 system scope | `USER_UNIT=ufo-sighting.service` | total 1, fleet 1 |
| X2 user scope | `UNIT=pipewire-pulse.service` | total 1, nonfleet 1 |
| X3 valid `\x2d` escapes, `oom-kill` | `app-Hyprland-xdg\x2dterminal\x2dexec-r14.scope` | total 1, nonfleet 1, oom 1, oom_nonfleet 1 |
| X4 template instance | `shokunin-lane@kagi.service` | total 1, fleet 1 |
| X5 canary fleet | `kagi-shokunin-R14-UNIT-SUBJECT-CANARY.service` | total 1, fleet 1 |
| X6 canary non-fleet | `pipewire-pulse-R14-UNIT-SUBJECT-CANARY.service` | total 1, nonfleet 1 |

X1 and X2 are synthetic cross-scope shapes; neither was observed on this host (§2).

### Result axis

Subject is a valid fleet unit (`kagi-shokunin.service`).

| arm | `UNIT_RESULT` | vector | consequence |
|---|---|---|---|
| R1 | missing | total 1, fleet 1, oom_result_unknown 1 | no alarm; fleet route kept |
| R2 | `["oom-kill"]` | total 1, fleet 1, oom_result_unknown 1 | **no alarm** |
| R3 | `OOM-KILL` | total 1, fleet 1 | exact vocabulary; not oom, not unknown |
| R4 | `null` | total 1, fleet 1, oom_result_unknown 1 | no alarm |

Boot, identity and producer-error arms (foreign boot, multi-boot, wrong `MESSAGE_ID`, rc1/rc2, stderr, malformed JSON, absent tools) already exist in both suites. They are not repeated here.

## 7. Findings on the existing fixture helpers

| id | severity | owner | finding | state at final read |
|---|---|---|---|---|
| F1 | MED | JournalRegression | Gate records used `UNIT_RESULT="failed"`, which is outside every pinned result table (§3). | **Adopted**: 0 occurrences; 15 `resources`, 6 `oom-kill`, 2 `signal` (`82010d1c…`). |
| F2 | MED | all suites | No near-miss records existed: every coredump was sig11 and every `98e32220` was killed/9. Five of six selector mutations were invisible (§4.8). The r13 harness also emits coredump records **without** `COREDUMP_SIGNAL` (`extra = {"COREDUMP_SIGNAL": "11"} if i < seg else {}`); real records always carry it (1586/1586). | Gate **adopted** (2× sig6, 2× killed/15, 1× exited/9). Census selftest **adopted** user coredump 2 > segfault 1 (CensusRepair report). The static selftest dispatcher cannot express EXIT near-misses; the gate owns that. |
| F3 | LOW | CensusRepair, JournalRegression | User-scope arms used `UNIT=`, the cross-scope shape. Host user records are 100% `USER_UNIT`. | **Adopted** in both. CensusRepair keeps one deliberate `UNIT`-in-user non-fleet arm, plus a system `USER_UNIT` arm. Its 12-cell matrix's only system unit failure uses `USER_UNIT` (cross-scope); a realistic `UNIT` system record would be the better default. |
| F4 | LOW | CensusRepair (at first read) | The selftest matrix had 5 zero cells: user oomd; system coredump, segfault, sigkill and failure. Its only unit record was subjectless. | **Adopted**: 12 nonzero cells. User 3/1/2/1/1/1; system 5/2/1/1/1/1 (`0e41cb83…`). Sigkill and failure are 1/1 in both scopes, so a swap there is invisible by count. M's asymmetric values cover it. |
| F5 | LOW | JournalRegression | The unit-byte canary probes only a malformed name. Valid fleet/non-fleet subject bytes are never canary-checked, and raw-name greps false-positive on fixture paths. | open. Use §4.10. |
| F6 | LOW | gates | The stub's `ALWAYS` lists the four S014 fields. Host 261 also prints `__SEQNUM`/`__SEQNUM_ID`. | harmless; the census ignores both |
| F7 | INFO | L1 | The signal-only KILL warn carries `count=0` (`count=$ps`). r13 CountDesign's invariant said no finding carries `count=0`. | **Resolved by L1 (MoriR14).** `count=` stays the process-SIGKILL count, so 0 is valid on the signal-only path. `user_unit_signal` carries the positive result count, under `class=kill_signal`. It is not a summed warning magnitude, and the final docs will say so explicitly. |
| F8 | INFO | L1 | An oomd notice alone is not the OOM alarm (D12). | **Resolved by L1 (MoriR14).** The oomd notice alone stays INFO; the unit-result `oom-kill` crit path is mandatory. No-harm-neutral vs pre-r13 `[INFERENCE]`. |

F1–F4 adoption states come from my grep and reads at the stated SHAs. CensusRepair's second coredump line is as that seat reported it.

## 8. Knowledge correction: slice units do emit kernel-OOM notices

`corpus/knowledge/journal-alarm-routing-r14.md` states that slice units emit no `fe6faa94…` notice, at three places: `:59-60`, `:136` and `:305`.

Counter-evidence:

- **Host.** Count-only, by subject suffix: 3 of 7 user and 4 of 9 system retained notices have `.slice` subjects. This agrees with r12 `corpus/evidence/drift-r12-20261019T2204Z-classification.md:60`, which lists `app.slice`, `-.slice`, `system.slice`, `user-1000.slice` and `user.slice`.
- **Pinned code** (`cf8ebfc6…` `src/core/cgroup.c`):
  - Only the inotify watch skips slices: `if (u->type == UNIT_SLICE) return 0;` at `:2075-2078`.
  - `on_cgroup_empty_event` (`:2936-2959`) calls `unit_check_oom(u)` with no slice exclusion.
- `[INFERENCE]` `unit_check_oom` reads the `memory.events` `oom_kill` counter (`:3082-3086`), which cgroup v2 reports hierarchically by default. So a slice's empty event can report a descendant kill.

**Suggested wording:** "slice units are not inotify-watched, but can still emit via the cgroup-empty path."

**Fixture consequence.** System notices with ancestor subjects (`user@1000.service`, slices) are real fan-out. Any future notice-level fleet routing would mislabel those as non-fleet. This is one more reason the OOM alarm stays global and is not routed by notice subject.

KnowledgeRepair confirmed the anchors and applied the wording to the note. That seat cites my host grouping as my observation; it did not rerun it.

## 9. Coordination

| peer | message | reply |
|---|---|---|
| `MoriR14.KnowledgeRepair` | §8 contradiction with evidence | applied: slices are now described as not inotify-watched but able to emit via the cgroup-empty path; "slice units" removed from the unseen paths |
| `MoriR14.JournalRegression` | F1, F3, F2 | none; adoption observed in the gate bytes |
| `MoriR14.CensusRepair` | F3/F4 | two replies: adopted `USER_UNIT` user arms and the 12-cell matrix; then adopted the strict coredump > segfault line |
| `MoriR14` (L1) | (decisions received) | F7 and F8 resolved as above. No further code edits needed. Report the filter executions as bounded empirical fixture probes; L1 names the gates and selftests, not seat jq, as the main verification. |

No other seat was contacted. `agent://all` was not used.

## 10. Checks for L1 after all changes land (run once)

L1's main verification is the census selftest and the gates below. The seat's jq probes (§4.7, §4.8, §6) are supporting fixture evidence only.

1. `bash tools/mori-census.sh --selftest`. The journal-matrix case (12 cells) and every `journal:` label pass. No `MORI_JOURNAL_CANARY` appears.
2. Run the r14 gate. Confirm:
   - `R14_SCOPED_PARITY` passes on repaired bytes;
   - the frozen `39abda0a…` bytes fail its OOM and routing expectations;
   - the argv log shows the six class argv shapes.
3. Optional: add M (§4.3) and D1–D13/I1 as gate cases.
   - Expected values are in §4.4–4.6 and §5.
   - Frozen bytes must fail D1–D4, D6–D8 and D10.
   - Frozen bytes must stay green on D9, D11–D13 and E0.
4. To reproduce any probe vector here, take the assignment block from `JOURNAL_ID_KERNEL_OOM=` to the line before `# journal_query <scope-flag>` in the census. Evaluate it in a subshell. Then run:

   ```sh
   jq -s -r --arg boot 0123456789abcdef0123456789abcdef --arg id <ID> [--arg fleet "$FLEET_UNIT_TOKENS"] "$JOURNAL_JQ_<X>"
   ```

   over the projected slot lines.

## 11. Tooling and scratch

- **Installs and updates:** none.
- **Tools used:** existing `jq`, `journalctl` (read-only, count-only), `curl`, `git show`, `python3`.
- **Scratch:** `/tmp/r14-fixture-vectors/` and the fetched pinned-source copies under `/tmp` are removed at the end of this seat.
