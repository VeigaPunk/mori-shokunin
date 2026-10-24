# HistR13: C1 census-regression hunt on commit 18d7d55 (`tools/mori-census.sh`)

Seat: MoriR20.HistR13 (leaf; no subagents). Read-only. I did not run the census, any selftest, fixture, build or linter. I installed or updated nothing. Journal reads were count-only and field-restricted (no `MESSAGE`).

Byte-exact extracts behind every census line citation are in `.ufo/waves/round-20/build/HistR13/` (all `git show` output):

| Abbrev | File | Content |
|---|---|---|
| C0 | `census-parent-of-18d7d55.sh` | `18d7d55^:tools/mori-census.sh`, sha256 3da5b098…, 3041 lines |
| C1 | `census-18d7d55.sh` | `18d7d55:tools/mori-census.sh`, sha256 39abda0a…, 3450 lines |
| CH | `census-2061780.sh` | HEAD (measured), sha256 87b8d680…, 4744 lines; equals `census_sha256` in RCPT |
| D1 | `18d7d55-census.diff` | the 18d7d55 diff, 748 lines |
| K | `git show 18d7d55:corpus/knowledge/structured-journal-scopes-r13.md` | round-13 knowledge |
| L, S | `LOG-2061780.md`; `SCORECARD-2e57647.md` (round-13 block at SCORECARD.md:658-718, same line numbers at HEAD) | round-13 LOG and SCORECARD |
| V | `corpus/lessons/round-13-verifier-spotcheck.md` (added dbe8500) | outside closure: `rejected-harmed` |
| R12 | `corpus/evidence/drift-r12-20261019T2204Z-classification.md` | r12 token receipt |
| REG | `.ufo/waves/round-13/evidence/drift-classification.json` (2e57647) | r13 register, 42 tokens |
| RCPT | `.ufo/waves/round-20/evidence/c1-drift-entering.json` | the 50 tokens to classify |
| SCR | `.ufo/waves/round-20/evidence/c1-pin-probe-scratch.json` | L1 canonical probe at 10:22 (later state; used for line form only) |
| B10 | `corpus/evidence/baseline-r10-20261015T2231Z.json` | r10 pin (text, misnamed `.json`) |

## 1. Verdict

1. **18d7d55 changes default output in two places only:** the journal probe (C1:879-1128) and the lane authorship test in `grade_lane` (C1:1721-1730). Function-body hashes show that probe_watchdog, probe_waves, probe_cgroup, probe_disk, probe_tmux, probe_silence, run_census, drift_report and run_pin are byte-identical to C0. The drift normalizer and its counter and volatile lists also changed (C1:1995-2023).
2. **10 of the 50 tokens are explained by 18d7d55** (group A, §3). The other 40 come from the r12 roster commit (21), lane-row field formats with live lane states (13), the r14 restoration (1), the pre-18d7d55 wave rule (2) and other live state (3). Set check: all 42 REG tokens are still in RCPT, and the 8 unclassified are the only additions.
3. **No 18d7d55 change is declared as a candidate census-regression** in round 13's SCORECARD, LOG or knowledge. The only regression wording there is the generic "not a regression-free proof" (L:754, S:694). Round 13 scored coverage "improved" and kept the SIGKILL WARN path (S:691). It described the unit-failure records as INFO or label-only (L:737; K:47; K:69-72).
4. **The outside closure rejected round 13 as harmed** for losing the critical OOM alarm and the fleet/non-fleet unit distinction (V:84-87, V:95, V:100, V:127, V:132-134). Round 14 restored both (L:758-768; CH:1486-1493, :1566-1576).
5. **Three 18d7d55 regressions are invisible in the HEAD token set on this host.** F1 (critical OOM alarm) and F3 (signal-result WARN) are invisible because both classes have zero records on both sides. F2 (fleet/non-fleet routing) is invisible because HEAD restored it; on C1 bytes it would have appeared as +FINDING:UNIT_FAILURE_JOURNAL. Findings are emitted only for positive counts (C1:1085), so `--drift` cannot see a severity or routing change on a zero-count class. "Zero census-regression tokens" in r20 does not clear them.
6. **One token pair is a live census-regression candidate that predates 18d7d55:** `-FINDING:WAVE_UNSETTLED_AGE` and its `obs` pairing (§5). R12 classed it as a "coverage/evidence-loss regression" (R12:33). REG classed it live-state. The rule behind it has been unchanged since the r10 pin.
7. **Still undeclared at HEAD:** the narrowed signal-11 count (F5; no observed effect on the current boot) and git-environment isolation (F7; inactive on this host). F1-F4, F6 and F8 were repaired or declared later (§4).

## 2. 18d7d55 behavior changes: declaration status and token effect

"Declared" means stated in round 13's SCORECARD, LOG or knowledge. "Label" means only a string in the output or census header.

| # | Change (C1 line; C0 line) | Default-output effect | Declared in round 13? | Tokens explained | Flag |
|---|---|---|---|---|---|
| B1 | VERSION census-r5 → census-r6 (C1:255) | header line | Yes: K:34 "Implemented query contract — census-r6" | HEADER | no |
| B2 | `SURFACE journal` → `journal.user` + `journal.system` rows (C1:1031-1128; C0:874-911) | per-scope rows; surface `st` is only ok/unavailable, never drift | Yes: L:746 ("0 → 2 explicitly scoped journal surfaces"); S:678; K:35-36 | -SURFACE:journal; +SURFACE:journal.user; +SURFACE:journal.system | split: no. Loss of drift status: F1 |
| B3 | Finding IDs (journal_finding_id C1:1014-1027; class queries C1:1058-1080) | new IDs; old IDs removed | Yes: K:40-47; C1 header:235-241, :909-916 | -FINDING:SEGFAULT_JOURNAL; +FINDING:SEGFAULT_SIGNAL11_JOURNAL_USER; +FINDING:COREDUMP_NOTICE_JOURNAL_USER | no (F5 for the narrowing) |
| B4 | KILL text class → structured unit_sigkill_record only; user WARN (C0:875, :898 → C1:1070, :1095; text retirement C1:909-916) | KILL warn only for `EXIT_CODE=killed EXIT_STATUS=9` unit exits | Yes: K:68-69; L:737; C1:909-916 | -FINDING:KILL_SIGNAL_JOURNAL (live count 0) | partly; signal-result WARN loss is F3 |
| B5 | OOM text class and critical DRIFT removed (C0:874, :893-894; mint-demand comment C0:853). Kernel and oomd notices INFO (C1:1094-1095) | no crit or DRIFT from any OOM record | Implicit only: K:69 "Other classes are INFO"; K:71-72 calls the removal "a correction" | none on this host (zero records) | **yes, F1** |
| B6 | Fleet split removed. One INFO UNIT_FAILURE_JOURNAL for all user and system unit-failure records; OUT_OF_SCOPE removed (C0:891, :904-908 → C1:1026-1027, :1101-1102) | one count covering all unit failures | Label only: K:47 "no fleet classification"; L:737 "remain INFO" | none at HEAD (restored by r14). On C1 bytes it would be +FINDING:UNIT_FAILURE_JOURNAL [INFERENCE] | **yes, F2** |
| B7 | GPF and segfault text count removed (C0:881); unmeasured list omits it (C1:1041) | no text-based segfault count | None. No "general protection" or GPF in L, S, K or round-13 lesson at 18d7d55 | none | **yes, F4** |
| B8 | Signal-11 count: unfiltered `COREDUMP_SIGNAL=11` JSON (C0:883) → `MESSAGE_ID=fc2e22bc` AND `COREDUMP_SIGNAL=11` (C1:1068) | narrower population | The read removal is declared (L:738). The narrowing is not | none (value masked) | **yes, F5** (low) |
| B9 | JOURNAL_CLASSES_UNMEASURED info, emitted on every run (C1:1041; header:241) | +1 finding on every run | Census header and REG only; not in L, S or K at round 13 | +FINDING:JOURNAL_CLASSES_UNMEASURED | **yes, F6** (low; declared at HEAD, SKILL.md:36) |
| B10 | Query bounds: 2 s + 1 s grace, 12 serial queries; jq, boot-id, stderr, malformed and multi-boot grade unavailable (C1:310-326, :935-1012, :1044-1056) | unavailable instead of zero on failure | Yes: K:55-66; SKILL-18d7d55:72-78; S:700-702 | none | no |
| B11 | Drift lists: counter keys (C1:1995-2006), volatile list gains `boot` (C1:2008), boot masking (C1:2023) | drift mode only | Pin contract in C1 header, "ROUND-10 DRIFT PIN" block (C1:146-190); L:754 | volatile_fields | no (not default output) |
| B12 | Authorship: `printf \| sed \| grep -Fxq` → awk plus bash whole-line match (C1:1721-1730; C0:1490-1498) | differs only where sibling output is large enough to break the pipe (§5) | Yes: L:725, L:744; QUALITY-18d7d55:65 (criterion 27); SKILL-18d7d55:125-133 | none (§5) | no |
| B13 | Git isolation: `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE` on four git calls; `-c core.fsmonitor=false` on `ls-files` (C1:1624, :1675, :1692, :1702; comment :1672-1674) | differs only when those variables are inherited | None in L, S, K, SKILL, PROVINCE or lessons (grep finds no GIT_DIR or fsmonitor) | none | **yes, F7** (low, conditional) |
| B14 | Selftest OOM-alone DRIFT arm deleted (C0:2475-2481; D1:573-575); replacement matrix (C1:2747-2790) | no default output; guard removed | None. L:740 reports 91/91 without mention | none | **yes, F8** |
| B15 | `boot=<id>` echoed in journal rows; `cmd=` is now a class template (C1:885-893, :1032, :1126-1128) | new fields | Yes: C1 header:885-893; K:49-56 | none (boot masked) | no |

## 3. The 50 drift tokens (RCPT lines 13-62)

| Group | Tokens | Explaining change(s) | Class | Source |
|---|---|---|---|---|
| **A. 18d7d55 (10)** | HEADER; volatile_fields; -SURFACE:journal; +SURFACE:journal.user; +SURFACE:journal.system; -FINDING:SEGFAULT_JOURNAL; +FINDING:SEGFAULT_SIGNAL11_JOURNAL_USER; +FINDING:JOURNAL_CLASSES_UNMEASURED; +FINDING:COREDUMP_NOTICE_JOURNAL_USER; -FINDING:KILL_SIGNAL_JOURNAL | B1, B2, B3, B4, B9, B11. Live state also drives SEGFAULT_SIGNAL11, COREDUMP and KILL: current user boot shows 1 signal-11 record, 36 coredump notices and 0 unit SIGKILL records | census-schema-change; SEGFAULT_SIGNAL11, COREDUMP and KILL are schema plus live | C1; D1 |
| **B. r14 restore (1)** | +FINDING:UNIT_FAILURE_OUT_OF_SCOPE | Restored by 8d22d18 (CH:1493; 8d22d18 diff:410-412). C1 had removed the emission. Live non-fleet unit failures present | live-state | 8d22d18 |
| **C. r12 roster (21)** | +FINDING:ROSTER_SET_MISMATCH; +SURFACE:lane.{audio, chousa, game-dev-2d, game-dev-3d, kaidoku, kotodama, lore, mado, mori, revenger, souji, tabi, tameshi, tsukuroi} (14); +roster_n, +roster_source, +conf_n, +conf_dropped_n, +state_n, +state_dropped_n | 1f07f1d. It is the only census commit between the r10 pin (5be8943) and C0 | roster-change | L:661-662; S:605 |
| **D. lane rows (13)** | +gate_s, +reason, +path, +subject_commits, +window, -subject_commits, -window, -attribution, -example, -rowb_files, basis, age_s, round | Field formats from 1439c47 (r3) and 5b62c89 (r4). Values follow live lane states at measurement: aggregator row-B → row-A (§5); kumitate ledger-close row-4; kaidoku, kengaku, kake, kagi, chousa and revenger not-open committed-report; kama, tabi and mori young; kotodama not-open. Duplicate `round=` keys concatenate in drift_scan | live-state | SCR:14-35; git log -S |
| **E. WAVE (2)** | -FINDING:WAVE_UNSETTLED_AGE; obs | Pre-18d7d55 wave rule (unchanged, §5). Aged-unsettled IDs fell from 11 (B10:26-36) to 10 (SCR:53-62), so one baseline line goes unpaired and the rest pair with a different obs | candidate census-regression (R12:33); REG calls it live | R12:30, :33 |
| **F. other live (3)** | +FINDING:WATCHDOG_STATE_LAG; -FINDING:WATCHDOG_STALE; io_avg_unavailable | WATCHDOG_STATE_LAG from d30b4e4 (r7); 13 lanes lag at 10:22 (SCR:39-51). WATCHDOG_STALE from 7ca17b1 (r1); the probe flags only when log age exceeds 900 s, and the log was rewritten at 07:23, so it was likely fresh at 07:18 [INFERENCE]. io_avg_unavailable: /tmp is now `/dev/nvme0n1p1` xfs, while B10:12 shows tmpfs | live-state | git log -S; findmnt; stat |

Totals: 10 + 1 + 21 + 13 + 2 + 3 = 50. The `volatile_fields` token is attributed to B11 as far as 18d7d55 goes. The HEAD list also has keys added by later commits (r14-r17, e.g. `unit_*`, `positive_*`), so that token is partly later-commit drift too.

The 8 tokens that REG does not cover (RCPT:64-74): COREDUMP and SEGFAULT_SIGNAL11 (A), UNIT_FAILURE_OUT_OF_SCOPE (B), `path` (D), `age_s` (D), `round` (D), -WATCHDOG_STALE (F) and io_avg_unavailable (F).

REG labels that should change: `-FINDING:KILL_SIGNAL_JOURNAL` is "[INFERENCE] live". It is a B4 class redefinition (C1:1070, :1095) plus a zero live count, so it should be schema plus live. `-FINDING:WAVE_UNSETTLED_AGE` is "[INFERENCE] live" against R12:33.

## 4. Flags: undeclared default-output changes (candidate census-regression)

No item below is declared as a candidate census-regression in round 13. "HEAD" is 2061780.

**F1 [HIGH]. Critical OOM alarm demoted to INFO; the OOM DRIFT path is gone.**
- Before: C0:874 text class; C0:893-894 `OOM_KILL_JOURNAL crit` (DRIFT, contract at C0:853); selftest C0:2475-2481 `drift: OOM_KILL_JOURNAL` (expects DRIFT). After: C1:1094-1095 `sev=info`, with warn only for user `unit_sigkill_record`. C1 has no `crit` in its journal region (grep). The surface `st` cannot become drift (C1:1126-1128).
- Declared? Only implicitly, by K:69 "Other classes are INFO". The pre-r13 contract is documented in corpus/knowledge/audit-r11.md:204 and corpus/knowledge/observability-surfaces-r2.md:179. It is absent from L:722-756 and S:658-718.
- Outside verdict: V:84 (OOM alarm regression), V:95 (coverage harmed).
- HEAD: restored. `OOM_KILL_JOURNAL crit` with `paths=kernel_oom_notice` or `unit_result_oom_kill` (CH:1566-1576). Restoration selftests at 8d22d18 diff:609, :616. L:766-768 and L:794 record the restoration.
- Drift visibility: none on this host (no kernel OOM notice on the current boot; no OOM token at HEAD).

**F2 [HIGH]. Fleet/non-fleet unit-failure split and tsukuroi owner routing removed.**
- Before: C0:891 fleet regex; C0:905 fleet-only UNIT_FAILURE_JOURNAL; C0:908 OUT_OF_SCOPE, owner tsukuroi. After: C1:1026-1027 maps all user and system unit-failure records to one ID; C1:1101-1102 counts all of them with "no fleet classification".
- Declared? Label only (K:47; L:737 "remain INFO"). The loss is not declared.
- Outside verdict: V:86, V:100 (adjacency harmed), V:133.
- HEAD: restored (CH:1486 fleet, CH:1493 non-fleet, CH:1500 unattributed).
- Drift: on C1 bytes the current host state would have produced +FINDING:UNIT_FAILURE_JOURNAL, because RCPT's non-fleet finding implies a total above zero [INFERENCE]. The current boot has 270 user unit-failure records, all `UNIT_RESULT=exit-code` (checked at about 07:45).

**F3 [MED]. Signal-result unit failures lost their WARN.**
- Before: C0:875 text includes `Failed with result .signal`, feeding the KILL warn (C0:898, DRIFT). After: the KILL warn fires only for `EXIT_CODE=killed EXIT_STATUS=9` (C1:1070, :1095). Signal-result failures become INFO unit-failure records (C1:1101-1102).
- Declared? No. K:68-72 names SIGKILL preservation and unmeasured "other signals", not this downgrade. Outside verdict: V:132 ("signal paths").
- HEAD: restored (CH:1621 `paths=unit_result_signal`; CH:1630 warn).

**F4 [MED]. GPF and segfault text dropped; not named as unmeasured at round 13.**
- Before: C0:881 `segfault|general protection fault` count. After: C1:1041 unmeasured list is `oom_kill_text,other_signals,other_unit_failure_text` and names neither.
- Declared at round 13? No (grep finds "general protection" only in corpus/knowledge/observability-census-r1.md:68,151). Outside: V:134 (route 3).
- HEAD: named as retired (CH:1377 `gpf_text:text-heuristic-retired`; SKILL-HEAD:36; corpus/knowledge/journal-alarm-routing-r14.md:162). Repaired by r14.

**F5 [LOW]. Signal-11 count narrowed from any `MESSAGE_ID` to `fc2e22bc` only.**
- Before: C0:883 unfiltered JSON count. After: C1:1068 (unchanged at CH:1406).
- Declared? The removal of the unfiltered read is declared (L:738). The narrowing is not. K:36-38 and K:45 name only the row.
- Observed now: `COREDUMP_SIGNAL=11` records in the current user boot: 1, all `fc2e22bc`. `1f4e0a44` records: 0 in user and system. [INFERENCE] another boot could hold a `1f4e0a44` record with `COREDUMP_SIGNAL=11`.
- HEAD: still open, not declared as a narrowing.

**F6 [LOW]. Always-on info finding not declared in LOG, SCORECARD or knowledge at round 13.**
- C1:1041 emits it before any availability check, so +1 finding on every run. Declared in the census header (C1:241) and REG only. HEAD declares it at SKILL-HEAD:36, so this is repaired.

**F7 [LOW, conditional]. Git isolation and `core.fsmonitor=false`.**
- Output differs only when GIT_DIR, GIT_WORK_TREE or GIT_INDEX_FILE is inherited. The old census could then query the wrong repository for every lane. The comment cites "audit-r11 r13 advisory" (C1:1672), but audit-r11.md at 6531ac6 has no fsmonitor or GIT_DIR text.
- Undeclared in L, S, K, SKILL or PROVINCE. V:57 mentions "environment hardening" only in passing.
- Measurement host: all three variables are unset (checked). HEAD: unchanged and still undeclared.

**F8 [MED, guard]. OOM-alone DRIFT selftest arm deleted.**
- C0:2475-2481 (`drift: OOM_KILL_JOURNAL`, expects DRIFT) is removed in D1:573-575. C1:2747-2755 gets its DRIFT from the user SIGKILL warn. C1:2785-2790 only asserts that legacy OOM text yields no finding.
- Undeclared. L:740 reports 91/91 with no mention.
- HEAD: OOM crit arms restored (8d22d18 diff:609, :616; CH:3593, :3618).

## 5. Outside 18d7d55: items for the L1 to rule on

- **WAVE candidate.** `probe_waves` has the same body hash (f7c82218…) at the r10 pin (5be8943), in C1 and at HEAD. C1:864-873 counts a wave directory with no registry, dispatch or run marker as `empty`, not unsettled. R12:30 records the operator sweep e20f4fa removing the aggregator wave markers. R12:33 classes the lost finding as a coverage or evidence-loss regression with settlement [UNKNOWN]. PROVINCE-18d7d55:33 (FR3) declares the limit as frontier, not as a regression. REG's live-state label does not answer R12:33. The frozen contract says a census-regression token blocks re-pin, so the L1 should either class these two tokens that way or record a rebuttal.
- **F01 does not explain any lane token.** The F01 failure needs sibling output large enough to block sed on the pipe. The measured case is 12,001 siblings (C1:1716-1717). The aggregator's window (epoch 1792039857 = 2026-10-15T04:50:57Z, the launch at watchdog.log:390; repo is the root) held 137 records at R12:23. At my check it held 305 records (14,376 bytes), one of them the aggregator's own. The window only grows, so r10 held at most 137. The pipe-size threshold is general Linux behavior and was not measured here [INFERENCE].
- **Watchdog and disk tokens** are live state, as §3-F shows.

## 6. Blind spot and recommendations

- Findings are emitted only for positive counts (C1:1085), and drift compares tokens. A severity or routing change for a class with zero records on both sides produces no token. F1 and F3 are of this kind on this host. F2 shows up only as a changed finding ID, and HEAD restored it. Zero census-regression tokens therefore does not establish absence of census-regression. The only evidence against F1-F3 is the restored code (CH) and the selftest arms (F8).
- Record in the r20 register that severity and routing regressions on zero-count classes are not drift-detectable. Keep the OOM, UNIT and SIGKILL selftest arms as the gate, and do not claim completeness in any re-pin reason.
- Reclassify the 8 unregistered tokens (§3), the two WAVE tokens (§5) and `-FINDING:KILL_SIGNAL_JOURNAL` in the r20 register. Correct the REG label for the KILL token.
- Round-13 scoring contradicts the outside verdict (L:752 "coverage improved 6→7" against V:95 "harmed"). L:758-764 supersedes it. Any citation of the round-13 scores should cite that supersession.

## 7. Checks and gaps

- **Not run (bounds):** census, selftests, fixtures, builds. Evidence is static: diffs, function-body hashes, `git log -S`, `git show`, `grep`.
- **Live checks (count-only or field-restricted, about 07:40-07:45 -03; boot started 2026-10-20 09:57:08 per `uptime -s`):** kernel OOM notices (fe6faa94) user 0 and system 0; unit SIGKILL records (98e32220 with EXIT_STATUS=9) user 0 and system 0; unit-failure records (d9b373ed) user 270 (all `UNIT_RESULT=exit-code`) and system 0; coredump notices (fc2e22bc) user 36; `COREDUMP_SIGNAL=11` user 1; `1f4e0a44` 0 and 0. `findmnt -T /tmp` gives /dev/nvme0n1p1 xfs. The GIT_DIR, GIT_WORK_TREE and GIT_INDEX_FILE variables are unset. The watchdog log mtime is 07:23:21.
- **Boot change:** the r13 run (drift-retained-baseline.json, started_utc 2026-10-20T04:33:14Z) predates the current boot, so journal-count tokens are boot-scoped live state.
- **Lane states at 07:18** are inferred from the RCPT tokens. SCR is the later 10:22 state.
- **Installs and updates:** none.
