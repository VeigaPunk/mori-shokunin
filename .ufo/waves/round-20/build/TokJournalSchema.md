# TokJournalSchema: round-20 C1 classification of 8 journal and header tokens

Seat: MoriR20.TokJournalSchema (leaf). Read-only. The census was not run, no baseline was pinned, no lane file was edited, no subagents were used.

Measured inputs:
- Census `tools/mori-census.sh` sha256 `87b8d680b9b2572e89977a10ff9b91630fbaf689f23f4892e06be427b977ab28`. This equals the worktree file, the blob at measured commit `2061780` and the blob at HEAD `e4d9384`. Census line numbers below refer to this blob.
- Baseline `corpus/evidence/baseline-r10-20261015T2231Z.json` (text file; header `census_sha256=d7710981…`). That hash equals `git show 5be8943:tools/mori-census.sh | sha256sum`. "baseline:N" below means line N of this file.
- Receipt `.ufo/waves/round-20/evidence/c1-drift-entering.json`. Launched 10:18:05Z.
- Host journal observations were made 10:32–10:37Z. Current boot `3e7084f4-7046-4957-a8a2-c00542a3b469` began 2026-10-20 09:57:09 -03 and is still running. `journalctl --list-boots` retains boots only from 2026-10-19 00:34 -03, so the r10 pin's boot is not retained.

## Verdict

- All 8 tokens get `census-schema-change`. Counts: census-schema-change 8, live-state 0, roster-change 0, census-regression 0. None of these tokens blocks the re-pin on journal grounds.
- Against the round-13 register: 7 agree, 1 disagrees. The disagreement is `-FINDING:KILL_SIGNAL_JOURNAL`. Round 13 filed it as an inferred live-state family (`LOG.md:754`). The measured cause is the retired text rule, not host activity.
- `-FINDING:KILL_SIGNAL_JOURNAL` is the only token where host state looks like the driver. It is not. The current boot does contain 2 lines that the r10 text rule matches, so the r10 rule would emit the warn on this host today. The r13+ rule does not emit it, by design and by selftest.

## Table (token | class | reason | evidence)

| token | class | reason | evidence |
|---|---|---|---|
| +FINDING:JOURNAL_CLASSES_UNMEASURED | census-schema-change | Round-13 addition, emitted unconditionally on every run (not positive-gated). r10 had no such id. Host state cannot add or remove it. | census:1377; intro 18d7d55 (r13), reasons rewritten 8d22d18 (r14); corpus/knowledge/structured-journal-scopes-r13.md:34-38, 106-114; LOG.md:725-726 |
| +SURFACE:journal.system | census-schema-change | Round-13 per-scope split of the single `journal` row. Emitted on every run, either in the main loop or in an unavailable branch. | census:1675, 1380, 1386, 1392; baseline:10 (single row); intro 18d7d55; corpus/knowledge/structured-journal-scopes-r13.md:36-37; LOG.md:725 |
| +SURFACE:journal.user | census-schema-change | Same round-13 per-scope split, user scope. | census:1675, 1380, 1386, 1392; baseline:10; intro 18d7d55; corpus/knowledge/structured-journal-scopes-r13.md:36-37; LOG.md:725 |
| -FINDING:SEGFAULT_JOURNAL | census-schema-change | r10 id (text grep plus JSON COREDUMP_SIGNAL=11 count, emitted only when >0) retired in r13. No emitter remains. The r10 rule would still emit it on this boot (count 1), so id retirement is the cause, not host state. | baseline:38; 5be8943:752-761, 777-779; census:262, 1327-1328, 1459, 1468; intro 7ca17b1 (r1), retired 18d7d55; corpus/knowledge/structured-journal-scopes-r13.md:45, 70-72 |
| -SURFACE:journal | census-schema-change | Single row replaced by journal.user and journal.system in r13. No emitter for the bare id remains. | baseline:10; 5be8943:737, 746, 787; census:1380, 1386, 1392, 1675; intro 7ca17b1 (r1), retired 18d7d55; corpus/knowledge/structured-journal-scopes-r13.md:36-37 |
| -FINDING:KILL_SIGNAL_JOURNAL | census-schema-change | r10 warn was a text count. r13+ warns only on structured records. The r10 rule would fire today on 2 `sudo` lines that mention SIGKILL. Structured killed/9 and UNIT_RESULT=signal counts are both 0. The census logic changed, so this is not live-state. No structured kill exists on this boot to miss. | baseline:37; 5be8943:751, 773-776; census:1342, 1454, 1587-1631, 3737-3738; text emit removed 18d7d55; warn restored 8d22d18; positives 26f6589; corpus/knowledge/structured-journal-scopes-r13.md:68-72, 78; corpus/knowledge/journal-alarm-routing-r14.md:17-21, 202-205; LOG.md:737; corpus/lessons/round-14.md:20 |
| HEADER | census-schema-change | Header label VERSION changed census-r5 to census-r6 in r13. The label is deliberately unmasked, so the bump surfaces as drift. | baseline:7; 5be8943:243, 1594; census:281, 2700; intro 18d7d55; corpus/knowledge/structured-journal-scopes-r13.md:34; corpus/knowledge/drift-pin-r10.md:4-6, 122-124 |
| volatile_fields | census-schema-change | The declared mask list changed in r13, r14 and r15: removed kill_signal, segfault, unit_failure; added boot and 37 journal and unit keys. run_drift compares list to list, so the token is host-independent. | baseline:4; census:2744-2772, 2981, 3001; 5be8943:1636-1648; diffs 18d7d55, 8d22d18, 26f6589; census:175-176, 183-185, 2765-2769; corpus/knowledge/drift-pin-r10.md:110-115, 241-247, 256-257 |

## JSON (same content)

```json
[
  {"token":"+FINDING:JOURNAL_CLASSES_UNMEASURED","class":"census-schema-change","reason":"Round-13 addition, emitted unconditionally every run; not positive-gated, so not host state","evidence":"census:1377; baseline absent (baseline:1-39); intro 18d7d55, reasons rewritten 8d22d18; corpus/knowledge/structured-journal-scopes-r13.md:34-38,106-114; LOG.md:725-726"},
  {"token":"+SURFACE:journal.system","class":"census-schema-change","reason":"Round-13 per-scope split of the single journal row; emitted every run","evidence":"census:1675,1380,1386,1392; baseline:10 single row; intro 18d7d55; corpus/knowledge/structured-journal-scopes-r13.md:36-37; LOG.md:725"},
  {"token":"+SURFACE:journal.user","class":"census-schema-change","reason":"Round-13 per-scope split, user scope; emitted every run","evidence":"census:1675,1380,1386,1392; baseline:10; intro 18d7d55; corpus/knowledge/structured-journal-scopes-r13.md:36-37; LOG.md:725"},
  {"token":"-FINDING:SEGFAULT_JOURNAL","class":"census-schema-change","reason":"r10 text+JSON id retired in r13 with no emitter left; the r10 rule would still fire on this boot (count 1), so host state is not the cause","evidence":"baseline:38; 5be8943:752-761,777-779; census:262,1327-1328,1459,1468; intro 7ca17b1, retired 18d7d55; corpus/knowledge/structured-journal-scopes-r13.md:45,70-72"},
  {"token":"-SURFACE:journal","class":"census-schema-change","reason":"Single row replaced by journal.user and journal.system in r13; no emitter for the bare id","evidence":"baseline:10; 5be8943:737,746,787; census:1380,1386,1392,1675; retired 18d7d55; corpus/knowledge/structured-journal-scopes-r13.md:36-37"},
  {"token":"-FINDING:KILL_SIGNAL_JOURNAL","class":"census-schema-change","reason":"r10 text rule would fire today on 2 sudo lines that mention SIGKILL; structured killed/9 and UNIT_RESULT=signal counts are 0. Census logic changed (text to structured), so not live-state; no structured kill is missed","evidence":"baseline:37; 5be8943:751,773-776; census:1342,1454,1587-1631,3737-3738; text emit removed 18d7d55; warn restored 8d22d18; positives 26f6589; corpus/knowledge/structured-journal-scopes-r13.md:68-72,78; corpus/knowledge/journal-alarm-routing-r14.md:17-21,202-205; LOG.md:737; corpus/lessons/round-14.md:20"},
  {"token":"HEADER","class":"census-schema-change","reason":"VERSION changed census-r5 to census-r6 in r13; label deliberately unmasked","evidence":"baseline:7; 5be8943:243,1594; census:281,2700; intro 18d7d55; corpus/knowledge/structured-journal-scopes-r13.md:34; corpus/knowledge/drift-pin-r10.md:4-6,122-124"},
  {"token":"volatile_fields","class":"census-schema-change","reason":"Declared mask list changed in r13/r14/r15 (-kill_signal,-segfault,-unit_failure,+boot,+37 journal/unit keys); list-vs-list compare, host-independent","evidence":"baseline:4; census:2744-2772,2981,3001; 5be8943:1636-1648; diffs 18d7d55, 8d22d18, 26f6589; census:175-176,183-185,2765-2769; corpus/knowledge/drift-pin-r10.md:110-115,241-247,256-257"}
]
```

## Per-token evidence

### 1. +FINDING:JOURNAL_CLASSES_UNMEASURED
- Now: `census:1377` emits it as `emit_finding JOURNAL_CLASSES_UNMEASURED info ...`. The guards start at `:1378`, so it runs on every probe. Comments at `:267` and `:1070-1073`.
- Baseline: absent. `git log -S` returns 18d7d55 (round 13) and 8d22d18 (round 14). The reasons were rewritten in r14 (`8d22d18` diff, hunk `+  emit_finding JOURNAL_CLASSES_UNMEASURED info "classes=kernel_victim_text,...`).
- Intent: `corpus/knowledge/structured-journal-scopes-r13.md:34-38` (census-r6 contract). `:106-114` (round-14 correction: "the unmeasured reason overstated the absence of structured fields"). `LOG.md:725-726` (round-13 claim).
- Class: census-schema-change.

### 2–3. +SURFACE:journal.system, +SURFACE:journal.user
- Now: `census:1675` `emit_surface "journal.$scope" "$st" "$d"`, inside the per-scope loop `:1633-1676`. Unavailable branches at `:1380`, `:1386`, `:1392`.
- Baseline: absent. The single row is `baseline:10` (`SURFACE journal: drift ...`).
- Introduced: 18d7d55 (`git log -S'journal.$scope'`). The diff hunks are `-emit_surface journal ...` and `+    emit_surface "journal.$scope"`.
- Intent: `corpus/knowledge/structured-journal-scopes-r13.md:36-37` ("two independent surfaces, journal.user and journal.system"). `LOG.md:725`, `:746` (0 to 2 scoped surfaces). `SCORECARD.md:708` (round-13 capability row).
- Class: census-schema-change (both rows).

### 4. -FINDING:SEGFAULT_JOURNAL
- Now: no emitter. The segfault class is `SEGFAULT_SIGNAL11_JOURNAL_{USER,SYSTEM}` (`census:262`, `:1327-1328`). It is emitted only when positive (`:1459`, `:1468`).
- Baseline: `baseline:38` (`FINDING SEGFAULT_JOURNAL severity=info obs=class=segfault count=<V> ...`). The r10 emitter is `5be8943:752-761` (text grep plus JSON COREDUMP_SIGNAL=11 count) and `:777-779` (emit when >0).
- Introduced: 7ca17b1 (round 1, `git log -S`). Retired 18d7d55 (round 13: the text count line and the emit are both removed, and the header lists the new ids).
- Intent: `corpus/knowledge/structured-journal-scopes-r13.md:45` (`segfault_signal11` row). `:70-72` ("Removing the unreliable text count is a correction"). `LOG.md:38-42` (round-1 count of 656 from the text and JSON form).
- Not host state: the r10 rule on this boot would still fire. COREDUMP_SIGNAL=11 user records = 1, and the text regex gives 0. The receipt itself lists `+FINDING:SEGFAULT_SIGNAL11_JOURNAL_USER`, so the structured count was positive at receipt time.
- Class: census-schema-change.

### 5. -SURFACE:journal
- Now: only `emit_surface "journal.$scope"` exists (`census:1380`, `:1386`, `:1392`, `:1675`).
- Baseline: `baseline:10`. The r10 emitters are `5be8943:737` (journalctl missing), `:746` (rc>1), and `:787` (main row).
- Introduced 7ca17b1; retired 18d7d55. Intent: `corpus/knowledge/structured-journal-scopes-r13.md:36-37`.
- Class: census-schema-change. The r12 reading "baseline aging across the boot" (`corpus/evidence/drift-r12-20261019T2204Z-classification.md:37`) was correct for census-r5 logic and is superseded here.

### 6. -FINDING:KILL_SIGNAL_JOURNAL
- Now: emitted only at `census:1630` (user `KILL_SIGNAL_JOURNAL` warn). It is gated by `kill_fire` (`:1342` init, `:1620-1622` set). It fires on structured user records only: `MESSAGE_ID=98e32220…` with `EXIT_CODE=killed` and `EXIT_STATUS=9`, or `MESSAGE_ID=d9b373ed…` with `UNIT_RESULT=signal`, or the positive arms. The per-class loop skips user unit_sigkill records (`:1454`).
- Baseline: `baseline:37`. The r10 emitter is `5be8943:773-776`: `if [ "$c_kill" -gt 0 ]`, where `c_kill` is `grep -ciE 'status=9/KILL|Failed with result .signal|SIGKILL'` over `journalctl --user -b --no-pager` (`5be8943:751`).
- Introduced/retired: text rule 7ca17b1 (r1). Text emit removed in 18d7d55 (r13). Structured warn restored in 8d22d18 (r14, hunk `+    emit_finding KILL_SIGNAL_JOURNAL warn ...`). Positive arms added in 26f6589 (r15, hunk `+    emit_finding KILL_SIGNAL_JOURNAL warn ... user_positive_process_sigkill=$pps`).
- Counterfactual on the current boot (observed, read-only, see section "Live counterfactual"):
  1. The r10 regex matches **2** lines.
  2. Both are `SYSLOG_IDENTIFIER=sudo`. MESSAGE contains `SIGKILL`. It does not contain `status=9/KILL` or `Failed with result 'signal'`. MESSAGE_ID, EXIT_CODE, EXIT_STATUS and UNIT_RESULT are absent. Timestamps are 2026-10-20T20:52:59Z and 20:53:15Z, before the receipt launch. So the r10 rule would have counted 2 at receipt time. [INFERENCE] These are sudo command logs whose command text contains `SIGKILL`; the MESSAGE text was not read or printed.
  3. The structured predicates give 0. `98e32220…` with killed/9: 0 (there are 2 `exited`/9 records, which the predicate correctly excludes). `d9b373ed…` with `UNIT_RESULT=signal`: 0 (270 records, none signal).
- Conclusion: the warn is absent because the census rule changed from text to structured records. The r10 rule would fire on this host. Live-state needs unchanged census logic, so it does not apply. Not a regression: no structured kill exists on this boot, and the two text lines are not unit process-exit or unit-result records. The round-13 design lists that path as unmeasured (`census:1377` reasons `other_signals:...`; `structured-journal-scopes-r13.md:78`: "a SIGKILL the manager did not observe").
- Intent: `corpus/knowledge/structured-journal-scopes-r13.md:68-72, 78`. `corpus/knowledge/journal-alarm-routing-r14.md:17-21` ("restores the historical KILL_SIGNAL_JOURNAL warning from two structured arms") and `:202-205`. `LOG.md:737` (round 13: "a structured process-exit SIGKILL replacement so the existing user warning path need not be lost"). `corpus/lessons/round-14.md:20` (M7: "never infer signal9 or sender from generic signal result"). `corpus/lessons/round-13-verifier-spotcheck.md:84` (accepts "generic unreliable-text retirement"). Selftest `census:3737-3738` asserts that a legacy text stream must not produce KILL_SIGNAL_JOURNAL. Its fixture (18d7d55 selftest hunk) uses `status=9/KILL` and `Failed with result signal SIGKILL`.
- Class: census-schema-change.
- Versus older readings: round 13 `drift-classification.json:35` gave "[INFERENCE] current watchdog/wave/lane activity or finding context", and `LOG.md:754` calls it an inferred live-state family. That reason is wrong; the cause is the rule change. Round 12 (`drift-r12-20261019T2204Z-classification.md:31`) called it a boot-scope change; correct for census-r5 logic, not for r20.

### 7. HEADER
- Now: `census:281` `VERSION=census-r6`. Header line `census:2700` `printf 'mori-census %s — ts=%s — mode=%s — read-only\n'`.
- Baseline: `baseline:7` (`mori-census census-r5 — ts=<V> — mode=live — read-only`). r10 emitters are `5be8943:243` (`VERSION=census-r5`) and `:1594` (same printf).
- Introduced: census-r5 in 9738f1a (r8, `git log -S'VERSION=census-r5'`). census-r6 in 18d7d55 (r13 hunk `-VERSION=census-r5` / `+VERSION=census-r6`).
- Why the token has no sign: the label is not key=value, so `drift_field_report` falls back to the line id (`census:2866`).
- Intent: `corpus/knowledge/structured-journal-scopes-r13.md:34` ("## Implemented query contract — census-r6"). `corpus/knowledge/drift-pin-r10.md:4-6` (r10 kept census-r5; revision identified by SHA). `:122-124` (VERSION deliberately unmasked).
- Class: census-schema-change.

### 8. volatile_fields
- Now: `run_drift` compares the baseline's `# volatile_fields=` list (`baseline:4`) with `DRIFT_VOLATILE_LIST` (`census:2772`, built from `:2771` and `DRIFT_COUNTER_KEYS` `:2744-2764`). The comparison is `census:2981`; the print is `:3001`.
- Changes since r10 (LC_ALL=C set difference, 69 to 103 tokens):
  - Removed: `kill_signal`, `segfault`, `unit_failure` (18d7d55 hunk `-  kill_signal ...`, `-  ... segfault ...`, `-  unit_failure unavailable ...`).
  - Added: `boot` (18d7d55 hunk `DRIFT_VOLATILE_SPECIAL` `+ ... boot ...`), `kernel_oom_notice oomd_notice coredump_notice segfault_signal11 unit_sigkill_record unit_failure_record` (18d7d55).
  - Added in r14: `unit_*`, `user_*`, `system_*` routing keys (8d22d18; `git log -S'user_unit_oom_result_unknown'`).
  - Added in r15: `positive_*` and `*_positive_*` keys (26f6589; `git log -S'positive_kernel_oom'`).
- Origin of the token: 5be8943 (round 10, `git log -S'volatile_fields'`).
- Intent: census header `:175-176` (volatile = "values that legitimately change run-to-run"), `:183-185` (journal counts incl. positive_*), `:2765-2769` (r15 comment). `corpus/knowledge/drift-pin-r10.md:110-115` (class-based list), `:241-247` (a red result is a named finding; re-pin only as a recorded act with a reason), `:256-257` (drift against a rewritten list reports `volatile_fields`, which is an expected result).
- [INFERENCE] `boot` is masked as a run-to-run value; the new journal rows print the validated boot id (`census:1671`). The header does not name it.
- Class: census-schema-change.

## Live counterfactual (observed, read-only; MESSAGE text not printed)

| check | command (abridged) | result |
|---|---|---|
| C1 r10 rule, current boot | `journalctl --user -b --no-pager \| grep -ciE 'status=9/KILL\|Failed with result .signal\|SIGKILL'` | 2 (≈10:32Z) |
| C2 the 2 matches, metadata only | jq predicate over `-o json --output-fields=MESSAGE,SYSLOG_IDENTIFIER`; prints flags, identifier, MESSAGE_ID presence, timestamps | both `sudo`; MESSAGE_ID, EXIT_*, UNIT_RESULT absent; `__REALTIME_TIMESTAMP` 2026-10-20T20:52:59.413287Z and 2026-10-20T20:53:15.098599Z (≈10:35Z) |
| C3 structured kill | `-o json --output-fields=_BOOT_ID,MESSAGE_ID,EXIT_CODE,EXIT_STATUS MESSAGE_ID=98e322203f7a4ed290d09fe03c09fe15 EXIT_CODE=killed EXIT_STATUS=9 \| wc -l` | 0 |
| C4 structured unit signal | MESSAGE_ID=d9b373ed55a64feb8242e02dbe79a49c, grouped by UNIT_RESULT | 270 records, none `signal` |
| C5 segfault counterpart | `COREDUMP_SIGNAL=11 \| wc -l`; text `segfault\|general protection fault` count | 1; 0 |
| C6 boots | `journalctl --list-boots --no-pager` | boot 0 `3e7084f4…` from 2026-10-20 09:57:09 -03, still running; retained list starts 2026-10-19 00:34 -03 |
| C7 census identity | `sha256sum tools/mori-census.sh`; `git show <rev>:tools/mori-census.sh \| sha256sum` | 2061780, e4d9384 and worktree = 87b8d680…; 5be8943 = d7710981… |
| C8 volatile lists | LC_ALL=C `comm` of baseline:4 against the current list | only in r10: kill_signal, segfault, unit_failure; only in current: 37 tokens incl. boot |
| C9 adjacent (not in item) | MESSAGE_ID=fc2e22bc6ee647b6b90729ab34a250b1 user scope \| wc -l | 36 |

## Agreement with the round-13 register (`.ufo/waves/round-13/evidence/drift-classification.json`)

| token | round-13 label (line) | round-20 class | verdict | reason |
|---|---|---|---|---|
| +FINDING:JOURNAL_CLASSES_UNMEASURED | intentional journal schema/version/mask change (:6) | census-schema-change | AGREE | Id is an r13 addition; the label maps to schema |
| +SURFACE:journal.system | same (:9) | census-schema-change | AGREE | Per-scope split |
| +SURFACE:journal.user | same (:10) | census-schema-change | AGREE | Per-scope split |
| -FINDING:SEGFAULT_JOURNAL | same (:36) | census-schema-change | AGREE | Stronger: the r10 rule would still fire on this boot, so id retirement is the whole cause |
| -SURFACE:journal | same (:38) | census-schema-change | AGREE | Row replaced |
| -FINDING:KILL_SIGNAL_JOURNAL | [INFERENCE] current watchdog/wave/lane activity or finding context (:35) | census-schema-change | DISAGREE | The cause is the retired text rule, shown by the counterfactual. No watchdog, wave or lane activity is involved. |
| HEADER | same (:44) | census-schema-change | AGREE | VERSION bump |
| volatile_fields | same (:47) | census-schema-change | AGREE | Mask list change |

Score: 7 agree, 1 disagree. The round-12 readings (`drift-r12-20261019T2204Z-classification.md:31-32, 37`) called KILL, SEGFAULT and SURFACE:journal boot-scope changes. That reading was correct under census-r5 logic and does not carry into r20.

## Caveats and judgment calls for the L1

1. KILL is the only judgment call. If the L1 reads loss of text-only, non-manager SIGKILL visibility as an unintended regression, the class becomes census-regression and blocks the re-pin. I read it as a documented, selftest-asserted blind spot (`structured-journal-scopes-r13.md:70-72, 78`; `census:1377`; `census:3737-3738`), so not a regression. The counterfactual numbers above are the evidence.
2. The reason text `other_signals:structured-field-unimplemented` (`census:1377`) is categorical wording that the round-13 verifier rejected (`corpus/lessons/round-13-verifier-spotcheck.md:87`); round 14 kept it. It is info-line text, not a drift token, so no class change follows.
3. VERSION is still `census-r6` at HEAD (`git log -S'VERSION=census-r6'` returns only 18d7d55), although r14 and r15 changed behavior. HEADER is therefore not a behavior marker. The new baseline should record the census SHA (`drift-pin-r10.md:5-6`).
4. The r20 register should replace the round-13 `[INFERENCE]` label on KILL with census-schema-change and cite the counterfactual.
5. Adjacent, not classified here: `+FINDING:COREDUMP_NOTICE_JOURNAL_USER` and `+FINDING:SEGFAULT_SIGNAL11_JOURNAL_USER` (in the receipt's `unclassified_vs_prior_register`). The current boot has 36 user coredump notices (C9) and 1 COREDUMP_SIGNAL=11 record (C5). Their emitters are positive-only (`census:1459`). [INFERENCE] The id part fits the r13 schema family and the presence reflects a live positive. The L1 should assign the class.

## Commands, tooling, not done

- Read-only git: `git show <rev>:tools/mori-census.sh | sha256sum` for 2061780, e4d9384 and 5be8943. `git log -S'<id>' --oneline -- tools/mori-census.sh` for `JOURNAL_CLASSES_UNMEASURED`, `SEGFAULT_JOURNAL`, `KILL_SIGNAL_JOURNAL`, `emit_surface journal`, `journal.$scope`, `VERSION=census-r6`, `VERSION=census-r5`, `volatile_fields`, `positive_kernel_oom`, `user_unit_oom_result_unknown`, `state_val_unread_reasons boot script_sha256`. Diff hunks were read with `git show 18d7d55|8d22d18|26f6589 -- tools/mori-census.sh`, cited by hunk content.
- Read-only journal and host queries: the C1–C9 commands above, plus `cat /proc/sys/kernel/random/boot_id`.
- Scratch copies of the r10 census and the three diffs were made under this seat's build directory for reading and then removed. Nothing is left behind except this file.
- Tooling: no installs or updates. Used pre-existing git, journalctl, jq, sha256sum, comm and timeout.
- Not done: census not run (`--drift`, `--pin`, live or selftest); no baseline pinned; no register written (the r20 register belongs to the L1); no lane or census file edited; no subagents.
