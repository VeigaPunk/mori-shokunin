# ReviewScopeClock: earlyoom scope rule against systemd v262 clocks

Seat: MoriR26.ReviewScopeClock (reviewer, leaf; no subagents, no background jobs). Access date for every source: 2026-10-22.
Lane: /home/vgpnk/Projects/shokunin/mori-shokunin. Scratch: /fast/scratch/hyaku/mori-r26/MoriR26.ReviewScopeClock/.
Tools installed or updated: none. Used curl, journalctl, systemctl, busctl and the python3 standard library, all already present.
Lane writes: this file only.

Lane state at review time (sha256, full):
- .ufo/waves/round-26/contract.md 74ec0661265b027888e337bb8473af90a12bb63752d3d6203500d609f3230569 (172 lines)
- tools/mori-oom-killers.py 2ca05bd4d434457e0be2a456d88c41a9f1f10f9420ebb64accb5e00ceec26c2e (mtime 10:30:19; the tool changed during this review and HEAD 93aa1b9 added zero-stamp handling; every probe below was re-run on this file)
- tools/fixtures/mori-oom-killers/cases.json 84d2343f1d672a4597a4ec5efe0fd048eb399e8b4f0f5b86cc483ff8f2e547af (32 cases)

## 1. Verdict

The scope rule is correct on the clock. It is also correct as the boundary for the current invocation's configuration (version, thresholds, dryrun). It is not a sound evidence window for "did the killer act". A restart or a stop turns real kills into KILLERS_QUIET with exit 0.

- Clocks: comparable within one boot, not across boots (section 3).
- Restart in the same boot (S1, disclosed, frozen): earlier invocations' action lines fall outside the scope. The reader returns KILLERS_QUIET, exit 0, scope_complete true, with a SIGTERM in the boot. The contract discloses this as A2a (contract.md:170-172), and frozen case c02 expects it (cases.json:46). Latent on this host: boots -2, -1 and 0 each had one earlyoom invocation. Reachable: the unit file sets Restart=always (/usr/lib/systemd/system/earlyoom.service).
- Stop without restart (S2, undisclosed): for any non-active unit the tool drops every journal record (tool:277). After an earlier kill, the reader returns KILLERS_QUIET, exit 0, actions null. Read literally, the contract gives KILLER_ACTED (contract.md:78-79, 97-98).
- Reload: no effect on the boundary (section 5).
- Never started (value 0): handled. Active with 0 gives KILLERS_UNKNOWN, exit 2. Inactive with 0 gives KILLERS_QUIET, exit 0, actions null, which c06 freezes (section 6).

Decision for the lead: Tier A (section 10) fits inside the current freeze. None of its changes alters a frozen expectation; I scanned all 32 cases. Tier B is the root fix for S1, but it changes frozen c02, so it needs an amendment and a new freeze. Without Tier B, S1 stays disclosed, and A-5 makes it visible in the output.

## 2. Method

- Read contract.md (current text), the tool's scope block (tool:272-298), the selftest loop (tool:654-672) and all 32 frozen cases.
- Fetched systemd v262 documents and sources, and earlyoom v1.9.0 main.c (section 12).
- Read-only live checks: systemctl show, busctl get-property on the unit object, journalctl for boots -2, -1 and 0, and journalctl --list-boots (commands in section 13). I did not start, stop, restart, reload or enable any unit.
- Ran the pure reader (python3 -I -B tools/mori-oom-killers.py --inputs FILE) on invented inputs written to scratch. I did not run live mode or --selftest; verification belongs to the main agent.

## 3. Clock check against the live host

| Quantity | Value (microseconds) | Read by |
|---|---|---|
| unit ActiveEnterTimestampMonotonic | 19964362 | systemctl show; busctl (same value) |
| unit ActiveEnterTimestamp (realtime) | 1792655744077607 | busctl Unit |
| unit ExecMainStartTimestampMonotonic | 19964246 (116 before ActiveEnter) | busctl Service |
| unit ExecMainStartTimestamp (realtime) | 1792655744077491 | busctl Service |
| boot 0, first journal record of the unit | 19964370 (+8); `_COMM=systemd`, PID 1 "Started" class, no `_SYSTEMD_INVOCATION_ID` | journalctl -b0 -u earlyoom.service |
| boot 0, first earlyoom record: the banner `earlyoom <version>` | 19981126 (**+16764**) | same command, `_COMM=earlyoom` |

Epoch check. Realtime minus monotonic, from the same read:
- unit ActiveEnter: 1792655744077607 - 19964362 = 1792655724113245
- unit ExecMainStart: 1792655744077491 - 19964246 = 1792655724113245
- journal PID 1 record: 1792655744077615 - 19964370 = 1792655724113245

All three give the same boot offset to the microsecond, so the unit's monotonic values and the journal's `__MONOTONIC_TIMESTAMP` share one clock origin within this boot.

Answers to the questions asked:
- Comparable within one boot: yes. Both are CLOCK_MONOTONIC. The journal doc says the field is the time "the entry was received by the journal in microseconds" (journal-fields v262, lines 659-660). The D-Bus doc says the Monotonic properties hold "CLOCK_MONOTONIC 64-bit microsecond timestamps" (org.freedesktop.systemd1.xml, lines 2783-2784). dual_timestamp_now sets the monotonic member from CLOCK_MONOTONIC (src/basic/time-util.c:79-80).
- Across boots: no. Boot -1's earlyoom records run from 14875281 to 154671911881 on boot -1's clock, about 43 hours, which matches `journalctl --list-boots` (2026-10-20 09:57:09 to 2026-10-22 04:54:50). Boot 0's ActiveEnter (19.96 s on its own clock) would wrongly admit boot -1 records stamped after 19.96 s if the `-b` filter were dropped. The journal doc says the monotonic value must be "combined with the boot ID" (lines 662-663).
- Suspend: both clocks exclude suspend time [INFERENCE: clock_gettime(2) lines 180-181 say so for CLOCK_MONOTONIC; no suspend occurred in the boots I read, so this was not tested].
- Invocation ID cross-check: all 12 earlyoom records in boot 0 carry `_SYSTEMD_INVOCATION_ID` equal to the unit's current InvocationID. The PID 1 record carries none. (Compared in-process; the ID is not copied here.)

## 4. Restart in the same boot

Mechanism (source, v262):
- Entering active sets ActiveEnter (src/core/unit.c:2773-2774), but only when `!MANAGER_IS_RELOADING(m)` holds (unit.c:2765).
- Restart=always passes through activating: src/core/service.c:103 maps SERVICE_AUTO_RESTART to UNIT_ACTIVATING (line 138 for Type=idle). Re-entering active sets a new ActiveEnter.
- So each start gets a new ActiveEnter, the scope moves forward, and earlier invocations' records fall below the bound. That part is correct behaviour.

Consequence (reproduced on invented inputs; no live restart; inputs in section 13):
- T5: a SIGTERM record at 19970000 from the old invocation; new ActiveEnter 20099990; banner at 20100000. Output: KILLERS_QUIET, exit 0, scope_complete true, sigterm 0.
- c02 freezes the same drop: a SIGTERM at 19964361 with ActiveEnter 19964362 expects KILLERS_QUIET, exit 0, sigterm 0 (cases.json:46). c02 is the lower-bound test, and its action line is the prior-invocation case.
- The disclosure at contract.md:170-172 is accurate. The output is still misleading: scope_complete says "true" and the verdict says "quiet" while the boot contains a SIGTERM. A-5 (section 10) makes the prior actions visible without changing the frozen verdict.

Frequency on this host:
- earlyoom: one banner in each of boots -2, -1 and 0. S1 is latent here.
- Other units restart within a boot: three units in boot 0 have two or more invocation IDs (two of them are snapper-cleanup.service and snapper-timeline.service). The most-invoked unit in boot -1 had 564 distinct invocation IDs.

Race between the two live reads (S3):
- The live collection runs `systemctl show` and `journalctl` as separate commands (contract.md:73-76). A restart between them mixes invocations: the old bound with new banners in scope (T3 shape). The reader reports scope_complete true and takes thresholds from the last banner. A-2 and A-3 (section 10) address this.
- I traced no path where this race produces a false KILLERS_QUIET. It can mix invocations in the counts and thresholds.

## 5. Reload

- `systemctl reload earlyoom.service`: CanReload=no (live). Job applicability for JOB_RELOAD is unit_can_reload (src/core/unit.c:3060-3062). The service vtable sets `.can_reload = service_can_reload` (src/core/service.c:6713). The unit file has no ExecReload, so the reload is refused and nothing is signalled. I did not run it. The refusal message text is not verified [INFERENCE for the message; the mechanism is verified].
- `systemctl daemon-reload`: the reload sets `n_reloading` (src/core/manager.h:562, MANAGER_IS_RELOADING). Unit timestamps are not updated during the reload (unit.c:2765-2766). The unit state is serialized and restored, including active-enter-timestamp (src/core/unit-serialize.c:93 for the write, :242 for the read). ActiveEnter is unchanged, so the boundary holds.
- The running process keeps its arguments through daemon-reload. The reader reads no file; its thresholds come from the running process's banner and threshold records. Correct.
- Documentation: "Asks all units listed on the command line to reload their configuration" (man/systemctl.xml, lines 465-466).
- `reload-or-restart` and `try-restart` are restarts and fall under section 4.

## 6. Unit that never started (ActiveEnterTimestampMonotonic = 0)

- Documentation: "The fields are 0 in case such a transition has not yet been recorded on this boot." (org.freedesktop.systemd1.xml, lines 2789-2790). So 0 means "no transition on this boot", not a time.
- Live example: the systemd-oomd unit reads `t 0` over D-Bus (busctl), with ActiveState inactive and UnitFileState disabled.
- Literal reading of the contract with 0: the bound `>= 0` keeps every record in the boot. A unit that never started has no earlyoom records, so the literal reading gives the right answer by accident. Any stray record would be counted as current, which is not principled.
- Current code: tool:279 (`if aetm is None or aetm == 0`) makes the bound unknown. Active with 0 gives scope_complete false and KILLERS_UNKNOWN, exit 2 (T2). Inactive with 0 gives KILLERS_QUIET, exit 0, actions null (T2i; c06 at cases.json:145 freezes this).
- Wording risk (S5): exit 0 for a killer that never ran reads as reassurance. contract.md:102-104 says "quiet then means no positive evidence from the killers that are readable". That is disclosed. The fix is additive (A-6). Changing the verdict would change c06.

## 7. Stop without restart (S2, not disclosed)

- tool:274 comment: "Only an active unit has a current invocation." tool:277: `if earlyoom_state == "active" and journal is not None:`. For any other state the journal is never read.
- T1 (invented inputs): ActiveState inactive, ActiveEnter 19964362, one SIGTERM record at 19970000. Output: KILLERS_QUIET, exit 0, scope_complete false, actions null.
- The contract text does not say non-active units are excluded. Its scope sentence (contract.md:78-79) and rule 1 ("in scope", contract.md:97-98) would count that SIGTERM. The D-Bus doc says the timestamps hold "the last time a unit ... entered the active state" (lines 2784-2785). That is documented; I did not stop the unit, so it is not observed here.
- Result: a false quiet for a killer that acted, and undisclosed.
- No frozen case has ActiveState inactive or failed with ActiveEnter above 0 and journal records (scan of 32 cases; c27 has no ActiveState). So the fix fits inside the freeze (A-1).
- failed maps to state unavailable and KILLERS_UNKNOWN (contract.md:162-163, A2b). That is safe, but it still drops the evidence.

## 8. Corrections to my own first pass

- I first read the first journal record of boot 0 (19964370, +8 µs) as an earlyoom record. It is PID 1's record (`_COMM=systemd`). The earlyoom banner is +16764 µs. The contract's `-u` query includes PID 1 records (S4), so a future "first record in scope" rule would be wrong. A-4 fixes it.
- I first expected the zero bound to act as zero. The current code (tool:279) treats 0 as unknown, and T2 confirms it.

## 9. Findings by severity

- S1 (high; disclosed; frozen): a restart drops earlier kill records, and the reader reports QUIET with scope_complete true. Evidence: T5; c02 (cases.json:46); contract.md:170-172; tool:297. Root fix is Tier B.
- S2 (high; undisclosed; fixable inside the freeze): a stopped unit's journal is ignored, so an acting killer reads QUIET. Evidence: T1; tool:274-277; contract.md:78-79, 97-98. Fix A-1.
- S3 (medium-low; undisclosed): the two live reads are not atomic, so invocations can mix in scope. No false quiet traced. Evidence: contract.md:73-76; T3 (two banners in scope, scope_complete true). Fix A-2 and A-3.
- S4 (low): `-u` includes PID 1 records, and the contract's "earlyoom lines" is undefined. Evidence: boot 0 record 19964370 (`_COMM=systemd`); 12 records with the `_COMM` match, 13 without. Fix A-4.
- S5 (low; disclosed): a never-started killer reads KILLERS_QUIET, exit 0. Evidence: c06; contract.md:102-104. Fix A-6 (additive) and wording.
- S6 (nit): the tool's comment at tool:280-285 repeats one sentence twice.
- Verified, no defect: clocks comparable within a boot (section 3); reload has no boundary effect (section 5); zero is handled (section 6); transitional ActiveState values are handled by A2b (contract.md:162-163).

## 10. Rule changes

Tier A: inside the current freeze. Each was checked against the 32 frozen cases; none changes a frozen expectation. The selftest loop checks only the listed fields, the verdict and the exit (tool:654-672), so additive fields do not disturb frozen cases. I read only that loop, not all of run_selftest.

```text
A-1 Stopped or failed unit keeps its last invocation as evidence (fixes S2).
    Condition: raw ActiveState is "inactive" or "failed" AND ActiveEnterTimestampMonotonic > 0.
    Scope: records with __MONOTONIC_TIMESTAMP >= ActiveEnterTimestampMonotonic.
    Counts: positive evidence counts (rule 1); `actions` stays null; the verdict rules apply unchanged.
    Tool: widen the condition at tools/mori-oom-killers.py:277 (currently state == "active" only).
    Covers the last invocation only. Earlier invocations remain under A-5 and Tier B.

A-2 Exactly one banner in scope (S3).
    scope_complete = scope_known AND exactly one "earlyoom <version>" record in scope AND not suppressed.
    Tool: tools/mori-oom-killers.py:357. No frozen case has two banners in scope (scan).

A-3 Two reads around the journal read (S3; live collector only).
    Read systemctl show, then the journal, then systemctl show again.
    If ActiveState or ActiveEnterTimestampMonotonic differs, scope_complete = false.
    The pure reader takes the second show as an optional key; absent = no check, so frozen inputs are unchanged.

A-4 Source filter (S4; live collector only).
    journalctl -q -b -u earlyoom.service _COMM=earlyoom -o json --output-fields=MESSAGE
    Verified: 12 records in boot 0, against 13 without the match.
    Contract line 74 must change to match.

A-5 Visible prior-invocation evidence (additive; verdict unchanged) (S1 mitigation).
    earlyoom.actions_before_scope = {sigterm, sigkill, escalations, kill_failed}: action records with
    __MONOTONIC_TIMESTAMP < ActiveEnterTimestampMonotonic; null when the bound is unknown.
    On c02 this reads sigterm 1.
    Contract text to add after rule 3: "KILLERS_QUIET with actions_before_scope > 0 means earlyoom
    acted in an earlier invocation of this boot. It is not a clean boot."

A-6 Killer-ran flag (additive) (S5).
    earlyoom.started_this_boot = ActiveEnterTimestampMonotonic > 0 (null when unknown).
    Contract text to add: "KILLERS_QUIET with started_this_boot false means the killer did not run.
    It is not a clean report."
```

Tier B: needs an amendment and a new freeze, because it changes counted expectations.

```text
B-1 Action evidence spans the whole boot (root fix for S1).
    Action evidence: every earlyoom action record in journalctl -b, any invocation.
    Configuration (version, thresholds, dryrun, scope_complete): current invocation only.
    Frozen c02 would change from KILLERS_QUIET / exit 0 / sigterm 0 to KILLER_ACTED / exit 1 / sigterm 1.
    count-c2.sh would fail cases_changed_since_freeze, by design. This needs amendment A3 and a new
    case-file version.

B-2 Invocation key (removes the clock race).
    Match InvocationID (systemctl show) against _SYSTEMD_INVOCATION_ID (journal-fields v262, lines 309-317;
    12 of 12 records match live). Needs new fixture fields.
```

Ready-to-paste scope paragraph, replacing contract.md:78-79 once Tier A is adopted:

```text
- Clock: `__MONOTONIC_TIMESTAMP` is the journal's receipt time on CLOCK_MONOTONIC (systemd.journal-fields v262,
  lines 656-664). `ActiveEnterTimestampMonotonic` is the manager's CLOCK_MONOTONIC stamp of the last entry into
  `active` (org.freedesktop.systemd1 v262, lines 2780-2790). Both are per boot: compare only records of `journalctl -b`.
- Records: earlyoom records only (`_COMM=earlyoom`; PID 1 lifecycle records are excluded).
- Current invocation (version, thresholds, dryrun, scope_complete): records with __MONOTONIC_TIMESTAMP >=
  ActiveEnterTimestampMonotonic, when the bound is non-zero. scope_complete requires exactly one banner record in
  that scope, no journald "Suppressed" notice, and the same ActiveState and ActiveEnterTimestampMonotonic in both
  systemctl show reads around the journal read.
- Stopped or failed unit with a non-zero bound: the same scope, used as evidence; actions stay null.
- Bound 0 or missing: no current invocation; scope_complete false.
- Action evidence: positive evidence in the current scope counts (rule 1). actions_before_scope reports action
  records stamped before the bound. Earlier invocations stay outside the scope until the Tier B amendment.
- reload: `systemctl reload` is refused (CanReload=no); daemon-reload keeps the bound (unit-serialize.c:93, :242;
  manager.h:562). Neither changes the scope.
```

## 11. Verification gaps and residual risk

- Restart, stop and reload were not run live (unit actions are forbidden to me). S1 and S2 come from source reading and invented inputs. The live host had one invocation per boot.
- The refusal text for `systemctl reload` is not verified. The mechanism is.
- The order between the manager's ActiveEnter stamp and the child's first write is not analysed (src/core/service.c and execute.c not traced). Observed margin: the banner is +16764 µs after ActiveEnter, from one invocation. A-1 to A-4 do not depend on this order. scope_complete fails closed if the banner falls outside the scope.
- ExecMainStart (19964246, 116 µs before ActiveEnter) would give the same result here. I did not analyse it as a replacement bound.
- Journal receipt lag: __MONOTONIC_TIMESTAMP is the receipt time, not the write time, so a late-received record can land on the wrong side of a bound. Not measured. [INFERENCE: negligible at this scale; journald "Suppressed" notices are handled by A1b.]
- I did not run --selftest. The probes in section 13 are behaviour checks, not a pass.

## 12. Sources

All fetched by curl on 2026-10-22 from the URLs below. sha256 is of the bytes fetched to scratch. Quotes are verbatim except XML tags and line wraps.

- https://raw.githubusercontent.com/systemd/systemd/v262/man/org.freedesktop.systemd1.xml, sha256 59cfeea5144e169369ee81f2b797fe9eb63ec18cb6aa918c2e66a7d5218117ca.
  - Line 2244: `readonly t ActiveEnterTimestampMonotonic = ...;`
  - Lines 2783-2784, quote (10 words): "contain CLOCK_REALTIME and CLOCK_MONOTONIC 64-bit microsecond timestamps"
  - Lines 2789-2790, quote (16 words): "The fields are 0 in case such a transition has not yet been recorded on this boot."
  - Line 2433: "property InvocationID is not documented!"
- https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd.journal-fields.xml, sha256 ff1c00abcc8b60f3bc8243edc241f8c72da2c9249ff0e69a0286d356aad93335.
  - Lines 659-660, quote (10 words): "the entry was received by the journal in microseconds"
  - Lines 662-663: "combined with the boot ID in _BOOT_ID="
  - Lines 309-317 (`_SYSTEMD_INVOCATION_ID=`), quote (10 words) at 311-312: "The invocation ID for the runtime cycle of the unit"
- https://raw.githubusercontent.com/systemd/systemd/v262/man/journalctl.xml, sha256 d54bbede45d5b1e3dc856da9624649ef8cb0829731597c212be303a76a1edbdd. Lines 673-675: `__CURSOR`, `__REALTIME_TIMESTAMP`, `__MONOTONIC_TIMESTAMP` and `_BOOT_ID` are always printed in JSON output.
- https://raw.githubusercontent.com/systemd/systemd/v262/man/systemctl.xml, sha256 caca7b87ae3bc8730b070a38d814c698acf82c596df9cb47a58fc7510c7b765c. Lines 465-466, quote (13 words): "Asks all units listed on the command line to reload their configuration."
- https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd.unit.xml, sha256 eb9479bea50ccb0e7643836ec083e8ef68bdf9ef2b26f31839939168f82714c6. No match for ActiveEnterTimestamp, InvocationID or auto-restart (grep, empty). The D-Bus XML is the authority for these properties.
- https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd.service.xml, sha256 12770f86a26dcdf32873225669f5aa9421283c303bbc72bddb04530850f66d44. Fetched, not quoted.
- https://raw.githubusercontent.com/systemd/systemd/v262/src/... (sha256):
  - src/basic/time-util.c 373dac1568e2bfc8e295e05e86e577f5444f6048a53d91c04b1fad68eb257f52 (lines 79-80)
  - src/core/unit.c 47e98d394462e05bf4bc0be2d1105fa8c21044cc9f5ebf00464f1742a92efcb7 (lines 2765, 2773-2774, 3060-3062)
  - src/core/unit-serialize.c e2fd3ff3c188aaad8b51a867abb4541d0341a3fa16aab9832909b8747678a2cd (lines 93, 242)
  - src/core/manager.h 9e10913d4b864e66945c580b2977f71fbd09f095385982b0d9c77ceace3677d8 (line 562)
  - src/core/service.c 9bf8a80bc29ef733648c688e4f40c3d01d6a4f67a877b2b5e23fbf8284c03d9c (lines 103, 138, 6713)
  - src/core/dbus-unit.c 47f461aeb70722ae7fb02f9b89ffd12db1639b7750a02e218dc27747f4cd9d0d (line 974)
  - src/core/job.c 024a1accfd833223f2913d72e1f106fd40175429d31fcaca2321370fb5a10897 (read for JOB_RELOAD only)
  - src/core/execute.c 30f8c6b60858f0722637f99f55e86f3babe9c933dce67a6023c06fc8a863dc8d (fetched, not analysed)
  - src/journal/journald-stream.c e919ebe8c8d8fb435082d01bfd951ff0626196ae514dec4509a8c7a3d8617175 (fetched; no invocation-ID handling found)
  - src/shared/bus-util.h 145076586e534df103db9e73d70f65e0ec4b98642607a3c96e23d6088e9b508f and src/core/dbus-util.h 7dac128023d62dd73ab4e0825c177eb8fc0b3175df3dcd91f798710b713a98fe (BUS_PROPERTY_DUAL_TIMESTAMP not located in either; the live values cover the mapping)
- https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/main.c, sha256 08656b0bc90c85f23738661456b25c97af908bc5e2cfea78e0a69697b5f9d0e4. Line 161: `fprintf(stderr, "earlyoom " VERSION "\n");`, inside main() with no guard (lines 150-166 read).
- https://man7.org/linux/man-pages/man2/clock_gettime.2.html, sha256 7d7948bcf8400a786c2795b24e8da979d6e01610f7b8ea6bf1ab97f06205fb69. Lines 180-181, quote (12 words): "This clock does not count time that the system is suspended." Attribution to CLOCK_MONOTONIC is inferred from the adjacent "All CLOCK_MONOTONIC variants" sentence [INFERENCE].

## 13. Reproduction and probes

Live reads (read-only):
- `systemctl show earlyoom.service -p LoadState,ActiveState,UnitFileState,ActiveEnterTimestampMonotonic` gives ActiveEnterTimestampMonotonic=19964362, ActiveState=active, UnitFileState=enabled.
- `busctl --system get-property org.freedesktop.systemd1 /org/freedesktop/systemd1/unit/earlyoom_2eservice org.freedesktop.systemd1.Unit ActiveEnterTimestamp` gives `t 1792655744077607`.
- `journalctl -q -b0 -u earlyoom.service _COMM=earlyoom -o json --output-fields=MESSAGE | wc -l` gives 12. Without `_COMM=earlyoom` it gives 13.
- `journalctl --list-boots` gives boots -2, -1 and 0.
- Record classes per boot (labels only, no text): boot 0 has banner 1, threshold 2, `mem avail:` report 6, other report 3, PID 1 record 1, action 0. Boot -1 has banner 1, action 39 (sigterm 38, sigkill 1), low-memory 40. Boot -2 has banner 1, action 0.

Pure-reader probes (invented inputs in scratch; base = cases.json c01 inputs with the changes shown):
- T0 control: c01 unchanged. KILLERS_QUIET, exit 0, scope_complete true.
- T1 stop: earlyoom_show = `LoadState=loaded\nActiveState=inactive\nUnitFileState=enabled\nActiveEnterTimestampMonotonic=19964362`; add `{"MESSAGE": "sending SIGTERM to process 4242 (invented-proc) and the rest", "__MONOTONIC_TIMESTAMP": "19970000"}`. Output: KILLERS_QUIET, exit 0, scope_complete false, actions null.
- T2 zero, active: ActiveState=active, ActiveEnterTimestampMonotonic=0. Output: KILLERS_UNKNOWN, exit 2, scope_complete false.
- T2i zero, inactive: ActiveState=inactive, ActiveEnterTimestampMonotonic=0. Output: KILLERS_QUIET, exit 0, actions null.
- T3 two banners: active, ActiveEnterTimestampMonotonic=19964362; add `{"MESSAGE": "earlyoom 1.9.0", "__MONOTONIC_TIMESTAMP": "20050000"}`. Output: KILLERS_QUIET, exit 0, scope_complete true.
- T5 restart: active, ActiveEnterTimestampMonotonic=20099990; journal = [SIGTERM at 19970000 (invented-proc), banner `earlyoom 1.9.0` at 20100000, term-threshold line at 20100100, kill-threshold line at 20100100 (c01 text)]. Output: KILLERS_QUIET, exit 0, scope_complete true, sigterm 0.
- Frozen-case scan (cases.json, read-only, 32 cases): one case has an action record before ActiveEnter (c02); no case has two banners in scope; no case has ActiveState inactive or failed with ActiveEnter above 0 and journal records.

Privacy: no MESSAGE text, process name, command line, uid, /etc/default/earlyoom value or OMP value is copied here. Invocation IDs and boot IDs were compared or read, not copied. Invented names only (invented-proc).
