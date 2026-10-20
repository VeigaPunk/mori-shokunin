# LessonAudit — falsification of `corpus/lessons/round-17.md` (round 17, wave 2)

Seat: `MoriR17.LessonAudit-4` (leaf, no dispatch). Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin`, measured commit `273aa74ab73701f41fea38ec7bd1c47b4b2bfbc7`. Date 2026-10-20. Lesson read at `corpus/lessons/round-17.md` (164 lines, `#02A2`).

Scope attacked: (1) the eight new source quotes S041–S048; (2) mutable-source change log; (3) Gate admits/rejects and outside-check status; (4) the five r16 routed items plus the jj migration disposition; (5) precision of the new procedural disclosures M1–M10. Not attacked: C1/C2/C3 algorithmic correctness, the SHONEN box, and the Gate's admit/reject decisions as judgments (no admit/reject decision is mine).

## Tooling and access record

- No install or update. Used pre-installed `curl`, `jq`, `grep`, `sha256sum`, `diff`, `wc`, `git show` (read-only, `24526ea`), `sed`.
- Outside fetches: one stdout-only `curl` per source URL (8 URLs, 2026-10-20). Nothing written to disk, nothing to `/tmp`.
- `/var/log/pacman.log` read with `grep -n` (read-only). No journal query, no pacman transaction, no VCS write, no selftest or gate run, no live probe.
- No transcript and no credential record was opened. `SentinelTranscripts.md:31` was read as report prose only.

## 1. Eight new source quotes

### 1a. Verbatim check (outside fetch + receipt cross-check)

| Row | Lesson quote | My word count | Outside check (2026-10-20) | Receipt | Result |
|---|---|---|---|---|---|
| S041 | "The 429 status code indicates that the user has sent too many requests in a given amount of time ("rate limiting")." | 21 | rfc6585.txt, whitespace-normalised: 1 hit, §4 at the plain-text line | `build/SrcRfc6585.md:16` | PASS (first grep missed on line wrap; normalised grep hit) |
| S042 | "Servers send the "Retry-After" header field to indicate how long the user agent ought to wait before making a follow-up request." | 21 | rfc9110 HTML, tags stripped: 2 hits | `build/SrcRfc9110.md:15` | PASS |
| S043 | "Rate limit reached for requests" | 5 | api-code.md: `:31 \| 1302 \| 429 \| Rate limit reached for requests` | `build/SrcZaiErrorCodes.md:25,17` | PASS for the quote. See D-03 for the inference drawn from it. |
| S044 | "jj commands will usually put the Git repo in a "detached HEAD" state, since in jj there is not concept of a "currently tracked branch"." | 25 | git-compatibility: `since in <code>jj</code> there is not concept` (markup only), and `there is not concept of a`: 1 hit each | `build/SrcJjGitCompat.md:16` | PASS (verbatim modulo `<code>` markup). 25 words is at the limit. |
| S045 | "This updates the author name and email. The author timestamp is not modified – use --update-author-timestamp to update the author timestamp." | 20 | cli-reference: `The author timestamp is not modified`: 1 hit (fragment only; full sentence not re-fetched) | `build/SrcJjMetaedit.md:30,32,34` | PASS (fragment); see D-04 for location and tier |
| S046 | "Errors are signaled by a non-zero status that is not 1." | 11 | git-merge-base: 1 hit | `build/SrcGitMergeBase.md:11` | PASS |
| S047 | "Do not issue an error message if the <name> is not a symbolic ref but a detached HEAD; instead exit with non-zero status silently." | 24 | git-symbolic-ref: `instead exit with non-zero status silently`: 1 hit (fragment) | `build/SrcGitSymbolicRef.md:17` | PASS (fragment) |
| S048 | "Overrides the default location of the pacman log file. The default is /var/log/pacman.log." | 13 | pacman.conf.5: 1 hit (fragment) | `build/SrcPacmanLog.md:13` | PASS (fragment) |

All eight are ≤25 words by my count. None exceeds the cap.

### 1b. Location, URL and date

- URLs match `corpus/SOURCES.md` S041–S048 (lines 47–54).
- Dates: the table has no per-row access-date cell. The date appears only in the prose sentence "All access dates are **2026-10-20**" (lesson line 42). Compliance is by blanket statement only.
- Locations: S041 §4 (ok), S042 §10.2.3 (ok), S043 api-code.md:31 (ok), S044 "Colocated workspaces" (ok), S046 OPERATION MODES (ok), S047 OPTIONS -q (ok), S048 LogFile (ok). **S045 gives only "metaedit --update-author".** The receipt and SOURCES row anchor `lines 2220–2238` (`build/SrcJjMetaedit.md:30`, `corpus/SOURCES.md:51`). The lesson omits the anchor.

## 2. Mutable-source change log

Verified changes:

- `corpus/SOURCES.md` vs `24526ea`: `diff` shows **additions only**: rows S041–S048 (lines 47–54), one paths bullet (line 61), one search-log entry (lines 81–82). No existing row cell changed. The lesson's "no existing status, recheck or used-by cell changes" (lesson line 57–58) **PASSES**.
- Source counts reproduce: `evidence/source-count.json` gives `24526ea: rows 40, mined 19, queued 20, rejected 1, A37/B2/C1` and `273aa74: rows 48, mined 25, queued 22, rejected 1, A45/B2/C1`. Lesson line 161 **PASSES**.
- `corpus/PROVINCE.md` appended `Round-17 appended scope and closure notes` at line 96–98, superseding "verification pending" (line 25 left unrewritten). Logged as M4. **PASSES.**
- `corpus/knowledge/journal-cursor-window-r16.md` appended `Round-17 appended freshness correction` at lines 138–146. Logged as M4. **PASSES.**
- New knowledge notes `corpus/knowledge/seat-terminal-status-r17.md` and `corpus/knowledge/jj-branch-anchor-r17.md`: exist, cite S041/S043 and S044–S047 (matches "mined" status). The lesson never lists their creation.

Defects in the change log:

- **D-02 (unlogged mutable change).** `corpus/QUALITY.md` gained a `## Criteria added round 17` section with criteria 43–48 (lines 112–140). The draft receipt recorded the file as 110 lines with highest criterion 42 and "QUALITY.md not edited" (`build/QualityCriteriaDraft.md:1,3`). The file is now 140 lines. The lesson's mutable-change accounting never mentions it, and its Mistakes table cites Q43–Q48 as if they were settled criteria.
- **D-02b (unlogged contract amendment).** `contract.md` gained "Amendment A1" (L1, ~16:10), after wave-1 reviews, which changes the C1 classification order, the output keys (`finding_id`, `now_ms`, `settle_seconds`) and adds the settle-window class. File mtime is 16:08 (`.ufo/waves/round-17/contract.md`). The lesson mentions only the C3 addition (line 15–18). M7 names "A1 settle-window classes" without saying when A1 landed relative to dispatch.

## 3. Gate admits, rejects, and outside-check status

- Admit and reject lists (lesson lines 28–38) match `contract.md` A1 and the Gate candidate names. I did not re-adjudicate them.
- **Outside-check status: not performed.** The lesson says "Independent outside admit/reject spotcheck remains required" (line 38). `.ufo/waves/round-17/falsify/` contained only `swarm-registry.json` before this report. No independent admit/reject receipt exists in the round. The lesson's status is accurate. The Gate admits therefore have no independent closure. This report is a quote and evidence falsification, not the admit/reject spotcheck.
- **D-01 (broken evidence pointer).** Lesson header line 4 cites "fleet report `/home/vgpnk/Projects/shokunin/.ufo/reports/round-17/mori.md`". That file does not exist. `.ufo/reports/round-17/` holds kagi, kaidoku, kake, kama, kasegi, kotoba, kotodama, kumitate, mado, souji, tabi, tameshi, tsukuroi and no `mori.md`.
- **D-03 (overclaim from S043).** Lesson line 59: "S043 caused the A1 business-code/quota-before-generic429 fix ... These are sourced claims." The S043 receipt says the table "does not document the `(type=NNNN)` token form that the C1 parser reads ... Linking a transcript `(type=1302)` to this table is [INFERENCE], not observed here" (`build/SrcZaiErrorCodes.md:35`). `contract.md` A1 item 10 nonetheless states `(type=1113)`/`(type=1308)` ⇒ `dead_quota` and `(type=1302)` ⇒ rate limit, citing S043. The HTTP-table mapping is sourced. The transcript-token mapping is an inference. The lesson presents it as sourced.

## 4. r16 routed items (`corpus/lessons/round-16-verifier-spotcheck.md:202–223`) and jj migration

| # | Routed item | Lesson disposition | Verdict |
|---|---|---|---|
| 1 | Undisclosed fleet-root write (`MoriR16.Lesson`) | M1 row; C3 no-pathspec sweep; frozen `frozen/MoriR16.Lesson` 847 bytes, sha256 `15f9f82d…5510e` (`sha256sum` matches the fleet archive `/home/vgpnk/Projects/shokunin/.ufo/waves/hyaku/misroots/MoriR16.Lesson` and `PINNED_INPUTS.json`) | PASS. The M1 row does not call it an "outside-lane write" explicitly. Minor. |
| 2 | M7 under-describes BootContinuity probes; append precision | M2 row. Line refs verified against `build/…` source: `.ufo/waves/round-16/build/BootContinuity.md:23` (`-b -n 2`), `:24` (`--cursor`), `:25` (bogus cursor rc1), `:26` (`--user -n 1`), `:28` (`id -nG`), `:42` (reasons from rc1), `:31–32` (`/tmp`, bg_2667) | **D-05 (partial).** The r16 item asked for an *appended* precision correction. No round-17 append exists in `corpus/lessons/round-16-verifier-spotcheck.md` (237 lines) or `corpus/lessons/round-16.md` (251 lines). `QUALITY.md:123–126` says "Correct it by appended precision" and cites those files. The correction lives only in the r17 lesson. |
| 3 | Pre-dispatch context gate | M3 row. Receipts: `evidence/context-check-wave1-original.json` (rc1, `no_tmp_probe_outputs` missing) → `context-check-wave1.json` (`CONTEXT_OK`, spec sha `6969eb19…` = `wave1-spec.json`); `context-check-wave2-original.json` (rc1, `transcript_fields_only` missing) → `context-check-wave2.json` (`CONTEXT_OK`, spec sha `6a2dc375…` = `wave2-spec.json`) | **D-06 (precision).** The wave-1 receipt was produced by the r16 checker (`clauses_checked: 8`, no `clause_ids`). Whether `no_live_journal_queries` was checked for wave 1 is therefore not shown by any receipt. M3 also merges two distinct facts in one row: the r16 original lacked the live-journal ban, and the r17 wave-1 original lacked `no_tmp_probe_outputs`. Wave 2 used the 12-clause r17 checker. |
| 4 | Stale wording after closure | M4 row. PROVINCE line 96–98 and knowledge note 138–146 appended. `pacman.log:2531` `upgraded systemd (261.2-1 -> 262-1)` at 09:16:28 | PASS |
| 5 | Carry-forward (r10 pin, alias false-unavailable, vacuum/cross-boot UNKNOWN, anchor-only, no census cutover) | Lesson "Carry-forward / migration dispositions" lines 79–86 | PASS |

**jj migration disposition.** Routed inputs (`contract.md` C2, line 18–19): `JjAuditMori.md` F3, F4, rows 1/2/5/6, and `JjTrialMori.md`. Source: `/home/vgpnk/Projects/shokunin/.ufo/waves/hyaku/jj-w1/reports/`.

- M6 covers F3/F4 and the C2 branch anchor. PASS.
- **D-07 (routed source undispositioned).** `JjTrialMori.md` is named nowhere in the lesson (grep: no hit). Its hazards are not dispositioned:
  - **H2**: repo-scoped jj config lives in `~/.config/jj/repos/<id>/`; copying `.jj` silently drops `snapshot.auto-track="none()"` (`JjTrialMori.md:49–60, 179–183`).
  - **H3**: `auto-track=all()` writes intent-to-add entries into the git index (`:86–90, 184–187`).
  - **H4**: `@{u}` breaks after the first jj mutation (`:108–111, 188–191`).
  - **H5**: every jj mutation resets the git index (`:192–194`).
  - H1 (cite only the `pushed` hash) is only loosely covered by "final `landed` citation retained" (lesson line 85).
  - Recommendations 2–5 are not dispositioned. Recommendation 4 is a real-remote `origin/HEAD` caveat.
- **D-08 (routing rows not mapped).** Audit rows 1/2/5/6 are `JjAuditMori.md` call-site numbers (`:211–218`). The contract and `build/CensusGitSites.md:33–38` name the same call sites as census "row 6" (2100/2102) and "row 9" (2197/2207). The lesson never maps one to the other. The mapping exists only in build receipts.
- **D-09 (silent narrowing).** `JjAuditMori.md` rows 10, 12, 15, 17 (gate-side `git rev-parse HEAD`), F10 (r15/r16 gate environment unhardened), F12 (`.jj` absent from output guards), and recommendations 4, 5, 7 are not dispositioned. The lesson's line 82 "JjAuditMori census HEAD hazard is fixed by C2" is correctly scoped to the census. It does not say the gate-side HEAD probes remain open.

## 5. Precision of the new procedural disclosures

Verified:

- M2 line refs (section 4 above): PASS.
- M4 PROVINCE and knowledge appends: PASS.
- M5 C3 addition timing: contract mtime 16:08 precedes L1 measurement receipts (16:34–16:35). PASS, with D-02b.
- M9: `SentinelTranscripts.md:31` discloses one `credential_pin` display. The lesson's description matches. The count "one" was not independently re-verified beyond that line.
- M10: the L1 selftests were run; the disclosure matches. PASS.
- Selftest counts (from receipts, not re-run): census `125/125` (`evidence/census-selftest.json` stdout, 125 PASS lines); terminal 33 (`seat-selftest.json` arms 33); seat gate 14 (`seat-gate-selftest.json`, 14 named checks); jj gate 13 (`jj-gate-selftest.json`, 13 named checks); misroot 11 (`misroot-selftest.json` arms 11); context 29 (`context-selftest.json` arms 29); silence 28/28 (`silence-oracle.json`, 28 PASS, 0 FAIL). All PASS.
- Preservation: `evidence/preservation.json` `unchanged: true` for 7/7 files. PASS.
- Live C1 counts: `evidence/seat-live.json` `.stdout` = `completed 368, dead_rate_limit 94, aborted 6, incomplete 1, unavailable 0, retry_exhausted 90, now_ms 1792524914623, settle 900, finding MORI_SEAT_TERMINAL_DEAD, rc 1`. Per-prefix dead_rate_limit: Tabi 22, Tsukuroi 44, Souji 28. PASS.
- C1 gate exit 1→0 and 54→0: `seat-before/run-manifest.json` `exit_code 1, verdict capability_absent`; `seat-after` `exit_code 0, verdict ok`. PASS.
- C2 assertions 124→134, failed 21→0, cases 7/12→12/12 (`jj-before/after/run-manifest.json`). PASS.
- C3 `c3-before` rc0 (0 candidates), `c3-after` rc1 (candidate found); frozen `c3-expected.json` pins `15f9f82d…5510e`. PASS.
- Pacman anchors: `pacman.log:2462` (`-Syu`, 09:15:30), `:3161` (`-U … zcode`, 13:23:08), `PacmanTxnToday.md:100` "448 actions". PASS.

Defects:

- **D-04 (S045 tier and location).** The receipt says the jj CLI page "self-labels 'This CLI reference is experimental. It is automatically generated'" and asks the main agent to decide whether tier A is appropriate (`build/SrcJjMetaedit.md:7,46–48`). SOURCES keeps tier A. The lesson's Gate says nothing about it. Location is incomplete (D-01 section 1b).
- **D-05 (partial r16 item 2)**: see section 4.
- **D-06 (M3 precision)**: see section 4.
- **D-10 (M8 under-disclosure and unsupported specifics).** Lesson M8 (line 73) records one command, `jj -R …/mori-shokunin diff --stat`, at "op45a25744584d", snapshotted "@ at 15:55:07", and states "It did not move the branch." `build/ReviewSkillRows.md:37–38` lists **three** jj invocations without `--ignore-working-copy`: `jj -R … status` (rc0), `jj -R … diff --stat` (rc0), and `jj -R … diff --git` (rc0). The op id and the 15:55:07 time do not appear in `ReviewSkillRows.md`. They appear only in lesson copies under `.ufo/worktrees/round-17/*/corpus/lessons/round-17.md:73`. "It did not move the branch" is not evidenced in the cited receipt.
- **D-11 (JjGate /tmp breach outside the Mistakes table).** `build/JjGate.md:16,325–327` discloses an accidental `/tmp/does-not-exist` created and removed. The lesson mentions it only in the C2 measurement paragraph (lesson line 131–133) and calls it "a procedural violation", but no Mistakes row exists.
- **D-12 (resumed-after-error stated as measured).** Lesson line 157 says "Resumed-after-error remains a measured counterexample to permanent death", with no receipt pointer. The live tool classifies only the terminal record (`contract.md` line 47–59, A1 item 2), so the live receipt cannot measure it. The support is in critic receipts, `build/CriticHarm.md:41` (H3: 71 error records followed by later messages) and `build/DeadSeatCrossCheck.md:197`. Those are manual analyses, not committed gate output. Lesson line 157 should cite them.
- **D-13 (gate exit codes unverifiable for C2).** Lesson line 113 says "gate exits1→0" for C2. `jj-before/run-manifest.json` and `jj-after/run-manifest.json` have keys `cases,census,environment,failed,gate,generated_at,schema,scratch_run,tools,totals` and no `exit_code`. Only `failed` 21→0 is recorded.
- **D-14 (typographic glue in the lesson).** Glued number/word joins make the lesson's own pins ambiguous. Instances: line 66 `sha25615f9f82d…5510e`; line 68 `SHA6969eb19…`; line 69 `host261.2-1` and `records262-1`; line 91 `and448 actions`; line 102 `tip273aa…`; line 104 `landed273aa…`; line 126 `totals124→134`; line 143 `census125/125`; line 153 `settle900seconds`, `reports469`; line 154 `completed368`; also `HTTP429`, `generic429`, `chmod000`. The hash fragments read as `sha256` + pin or as a single token. Full pins are in `PINNED_INPUTS.json`.

## Findings summary

| ID | Area | Severity | Count | Evidence |
|---|---|---|---|---|
| D-01 | Broken fleet-report pointer (header) | high | 1 | lesson:4; `.ufo/reports/round-17/` lacks `mori.md` |
| D-02 | Unlogged `QUALITY.md` +criteria 43–48; unlogged knowledge-note creation; A1 amendment timing | medium | 3 | `QUALITY.md:112–140`; `QualityCriteriaDraft.md:1,3`; `contract.md` A1 |
| D-03 | S043 overclaim for `(type=NNNN)` transcript mapping | medium | 1 | `SrcZaiErrorCodes.md:35–37`; `contract.md` A1 item 10 |
| D-04 | S045 tier-A caveat undisclosed; location incomplete | low | 2 | `SrcJjMetaedit.md:7,30,46–48` |
| D-05 | r16 item 2 not appended to source; `QUALITY.md:123–126` points at nothing | medium | 1 | r16 closure `:210–215`; r16 lesson 237/251 lines |
| D-06 | M3 wave-1 receipt clause coverage unshown; merged facts | low | 1 | `evidence/context-check-wave1*.json` |
| D-07 | `JjTrialMori.md` undispositioned; H2–H5 undispositioned; recs 2–5 | high | 1 (5 items) | `JjTrialMori.md:49–60, 86–111, 179–194` |
| D-08 | Routed audit rows 1/2/5/6 vs census row 6/9 unmapped | low | 1 | `JjAuditMori.md:211–218`; `CensusGitSites.md:33–38` |
| D-09 | Gate-side HEAD probes (rows 10/12/15/17), F10, F12 silently out of scope | medium | 1 | `JjAuditMori.md:222–230, 180–204` |
| D-10 | M8 lists 1 of 3 jj commands; op id/time/"did not move" unsupported | medium-high | 1 | `ReviewSkillRows.md:37–38` |
| D-11 | JjGate `/tmp` breach absent from Mistakes table | medium | 1 | `JjGate.md:16,325–327` |
| D-12 | "measured" resumed-after-error without pointer; live tool cannot measure it | low-medium | 1 | lesson:157; `CriticHarm.md:41` |
| D-13 | C2 "gate exits1→0" unverifiable (no exit_code field) | low | 1 | `jj-before/run-manifest.json` keys |
| D-14 | Glued number/word tokens in pins and counts | low | ~12 instances | lesson lines 66–154 |

Total defects: 14 IDs (D-01…D-14). Excluding D-14's ~12 glued-token instances, 20 countable instances (D-02 and D-07 counted per item). Open: outside admit/reject spotcheck not performed (status recorded correctly, lesson line 38).

## Not verified

- r13 24/24, r14 44/44, r15 63/63 and frozen red 34/34 (`evidence/r1{3,4,5}-preserved.json`): not re-read.
- `build/CriticC1.md` and `build/TranscriptShapes.md` rejected interpretations: not re-adjudicated.
- Gate admit/reject judgments: not re-adjudicated; no SHONEN box or rank reviewed.
- Quote checks S045, S047, S048 and S044 were fragment-level, not full-sentence re-fetches.

## Corrections this seat did not make

Per scope, nothing was rewritten. No file under `corpus/`, `tools/`, `.ufo/state`, or any lane file was edited. Only this report was written.
