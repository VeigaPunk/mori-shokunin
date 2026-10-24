# HistR17 — C1 census-regression hunt: tools/mori-census.sh at 273aa74, 2be8294, fe9fa90

Seat `MoriR20.HistR17` (leaf, read-only, no subagents). Inputs: `.ufo/waves/round-20/contract.md` (C1), `.ufo/waves/round-20/evidence/c1-drift-entering.json` (measured_commit 2061780, census 87b8d680…ab28, rc 1, 50 tokens). HEAD at review: e4d9384. Scratch evidence: `.ufo/waves/round-20/build/HistR17/{273aa74,2be8294,fe9fa90}.diff` and `*.decl.diff` (git show output). Census and selftests were NOT run (not in this item). No installs or updates. No git/jj/repo mutation, no network.

## Verdict

- **The three commits explain 0 of the 50 drift tokens.** Their only new finding IDs (`HEAD_BRANCH_MISMATCH`, `LANE_AUTHOR_MISMATCH`) are absent from the drift. Read-only checks (§5), taken at 07:38–07:40 after the 07:18 measurement, show their trigger conditions and the `reason=ref-unresolved` path do not hold [INFERENCE: state unchanged since 07:18], so the r17 decision logic selects the same rows as r16 for every lane. Every token traces to r1–r15 emitters or to live state (§2).
- **Candidate census-regression from r17: none** (no token is attributable to 273aa74, 2be8294 or fe9fa90).
- **Undeclared default-output changes, flagged as candidate census-regressions: CR-1 … CR-5** (§3). All are latent at the measured state. CR-1 (`has_head`) is invisible to `--drift` by construction. CR-6 is a stale-text observation, not a value change.
- Every other default-output change is declared in SCORECARD / LOG / knowledge / SKILL (§1, cited path:line).

## 0. Identity chain

| Ref | Role | census sha256 (prefix) |
|---|---|---|
| 24526ea | round-16 end, entering r17 (`frozen/mori-census.sh`) | f1f8d1b6 |
| 273aa74 | r17 C2 initial (parent 24526ea) | 12e8e2d9 |
| 5c1dfb8 | evidence commit, no census change (parent 273aa74) | — |
| 2be8294 | r17 A2 closure (parent 5c1dfb8) | 14858cae |
| fe9fa90 | r17 selftest repair (parent 2be8294) = 2061780 = HEAD | 87b8d680 (measured) |

Census commits in (5be8943 = r10 pin, 2061780]: 1f07f1d (r12), 18d7d55 (r13), 8d22d18 (r14), 26f6589 (r15), 273aa74, 2be8294, fe9fa90. None in r11, r16, r18, r19, or 2061780..HEAD. The r10 pin header records census d7710981 (`corpus/evidence/baseline-r10-20261015T2231Z.json:2`).

## 1. Behavior-change ledger (census line numbers = HEAD tools/mori-census.sh)

Declared = SCORECARD/LOG/knowledge/SKILL/README/lessons text. "Code comment" alone is not a declaration.

| # | Commit | Change (HEAD lines) | Default-output effect | Declared where | Tokens | Status |
|---|---|---|---|---|---|---|
| 1 | 273aa74 | Rows 6/9 and has_head read refs/heads/branch: ps_report_closed takes rev (2274); child-lane root branch (2402–2406); row-9 rev (2421–2422); rev-parse/log on rev (2425–2439) | Changes grading only if HEAD differs from branch tip; none today | knowledge/jj-branch-anchor-r17.md:15–19; LOG.md:1129; SCORECARD.md:1012 | 0 | DECLARED |
| 2 | 273aa74 | HEAD_BRANCH_MISMATCH warn: probe call (2337), emit (2537–2538) | New FINDING, +1 drift, verdict DRIFT rc1 (426–427, 2719) | knowledge/jj-branch-anchor-r17.md:23–24; SKILL.md:164; LOG.md:1129 | 0 (no +FINDING:HEAD_BRANCH_MISMATCH) | DECLARED (ID, severity) |
| 3 | 273aa74 | Same probe hoisted above rows 2–8 (2337 precedes 2350), so it fires for young, not-open and report-closed lanes | Same finding in any state | none (code comment 2331–2336 only; no selftest covers it: falsify/CensusNewBranches.md:193–209) | 0 | UNDECLARED → CR-2 |
| 4 | 273aa74 → 2be8294 | LANE_AUTHOR_MISMATCH warn: first in row 9 (falsifier F1); moved before early returns (call 2346–2347, emit 2540–2541) | New FINDING, state-independent after 2be8294 | knowledge/jj-branch-anchor-r17.md:26; SKILL.md:164, 199; LOG.md:1195–1196; corpus/lessons/round-17.md:71 (M6) | 0 | DECLARED (at HEAD) |
| 5 | 273aa74 | has_head = resolution of the row-9 rev (2423–2427); row-D emit (2504–2506) | Value differs only when branch and HEAD resolve differently (rare); meaning changed | none: git grep has_head over LOG, SCORECARD, SKILL, README, corpus/** has no hit; code comment 2504–2505 only | 0 (masked, §2) | UNDECLARED → CR-1 |
| 6 | 273aa74 | Child-lane row 6 checks the fleet root's branch (2402–2406) | Same commit today (ROOT attached to master) | knowledge/jj-branch-anchor-r17.md:17 | 0 | DECLARED |
| 7 | 2be8294 | Mirror-first resolver: valid lane.branch naming an existing ref wins (2158–2166) | Plain-git lane with mirror ≠ attached branch graded on mirror; none today | knowledge/jj-branch-anchor-r17.md:80–86; LOG.md:1195–1196; SKILL.md:197–198 | 0 | DECLARED |
| 8 | 2be8294 | .jj repo without authoritative mirror → unavailable reason=ref-unresolved (2331–2335) | Row-1 unavailable; none today (14 of 14 .jj lanes resolve) | knowledge/jj-branch-anchor-r17.md:82–84; LOG.md:1195–1196; SKILL.md:197–198 (literal token only in code, P1) | 0 (+reason not from this, §2) | DECLARED (rule) |
| 9 | 2be8294 | Committer-author pass runs before young/closed returns (2346–2347) | Can add LANE_AUTHOR lines for young or closed lanes | LOG.md:1195–1196 ("early young-window authorship diagnostics"); SKILL.md:199 | 0 | DECLARED |
| 10 | 2be8294 | GIT_SCRUB + git_cap() for every Git child (568–596; all git_cap sites) | None unless the census environment sets GIT_TRACE* or GIT_CONFIG* (§5) | LOG.md:1195 ("Git trace/config child isolation") | 0 | DECLARED (env sensitivity not stated, P3) |
| 11 | 2be8294 | .jj fleet root without mirror → row-6 closure skipped (2402–2409) | Row-6 not-open detection lost for child lanes if ROOT were .jj | none (knowledge:83–84 covers the lane grade only) | 0 | UNDECLARED → CR-4 |
| 12 | 273aa74, 2be8294 | valid_branch regex ^[a-zA-Z0-9][a-zA-Z0-9._/-]*$ (2156; used 2165, 2180, 2189) | Attached branch with other characters replaced by origin/HEAD or master/main | none (falsify/CensusNewBranches.md:143–162 only) | 0 | UNDECLARED → CR-5 |
| 13 | 273aa74, 2be8294 | protocol and aggregator both map to $ROOT (2011); per-lane emit (2537–2538) | One root divergence → two warns and drift +2 | none (falsify/CensusNewBranches.md:181–191 only) | 0 | UNDECLARED → CR-3 |
| 14 | 273aa74, 2be8294 | SURFACE cmd= text (2510) still says cat-file -e HEAD:; code runs "$rev:$rpath" (2278) | No value change (byte-identical by amendment A1) | code comments 2206, 2535; build/CriticHarm.md:62 (K7); not in SCORECARD/LOG/knowledge | 0 | UNDECLARED text staleness → CR-6 (observation) |
| 15 | 273aa74, 2be8294 | Warn finding → drift count → verdict DRIFT, exit 1 (426–427, 2719) | Clean verdict flips when a C2 finding fires | SKILL.md:164 ("warn findings"; "1 failed (DRIFT)"); selftests census:4078, 4093 | 0 | DECLARED BY COMPOSITION (P2) |
| 16 | 273aa74 | Header, usage and selftest TMPDIR text (34–47, 212, 407) | --help text only | n/a | 0 | NON-DEFAULT |
| 17 | 273aa74, 2be8294, fe9fa90 | Selftest fixtures, stub dispatcher, trace canary (3034–3042, 3103–3147, 3221–3231, 4058–4309) | None | LOG.md:1184 (2be8294 landing), LOG.md:1210 (fe9fa90), corpus/lessons/round-17.md:264–282 (M19) | 0 | NON-DEFAULT, DECLARED |
| 18 | all | Drift normalizer, pin and drift functions (2776–2940) | Untouched (hunk ranges in §4) | — | — | NO CHANGE |

## 2. Drift-token attribution (all 50 tokens of c1-drift-entering.json)

Method: each token's emitting string was located with `git log -S` on tools/mori-census.sh, its emitter at HEAD was read, and each r17 hunk was tested against it. The drift run compares per-line key=value fields (census:2826–2918); unsigned tokens are changed field values, signed tokens are added or removed keys or lines.

| Group | Tokens | Emitter (HEAD) | Introduced or changed by | From r17? | Driver at the measured run |
|---|---|---|---|---|---|
| A roster (21) | +SURFACE:lane.{audio, chousa, game-dev-2d, game-dev-3d, kaidoku, kotodama, lore, mado, mori, revenger, souji, tabi, tameshi, tsukuroi}; +roster_source +roster_n +conf_n +conf_dropped_n +state_n +state_dropped_n; +FINDING:ROSTER_SET_MISMATCH | silence line 2552; lane lines 2545 | 1f07f1d (r12): "census roster = declared lanes ∪ driver counters (9 -> 23)" | No | Roster 9 → 23. LOG.md:701–704 says audio, game-dev-2d and game-dev-3d were removed from shokunin.conf LANES on 2026-10-15 (roster-truth question for TokRosterFields) |
| B journal (9) | +FINDING:COREDUMP_NOTICE_JOURNAL_USER; +FINDING:SEGFAULT_SIGNAL11_JOURNAL_USER; +FINDING:JOURNAL_CLASSES_UNMEASURED; +FINDING:UNIT_FAILURE_OUT_OF_SCOPE; +SURFACE:journal.system; +SURFACE:journal.user; -FINDING:KILL_SIGNAL_JOURNAL; -FINDING:SEGFAULT_JOURNAL; -SURFACE:journal | journal emitters | 18d7d55 (r13), 8d22d18 (r14) | No | Schema change: scoped journal IDs replaced the r1 IDs |
| C watchdog (1) | +FINDING:WATCHDOG_STATE_LAG | watchdog state emitter | d30b4e4 (r7) | No | Dormant at r10; firing at measure [INFERENCE] |
| D r1 IDs (2) | -FINDING:WATCHDOG_STALE; -FINDING:WAVE_UNSETTLED_AGE | r1 emitters (7ca17b1, 486a4e3) | r1 | No | Not firing at measure [INFERENCE] |
| E young/reason (2) | +gate_s; +reason | row-8 GL_EXTRA reason=age_le_gate gate_s= (2377) | gate_s added by 1439c47 (r3); reason= key present since r4–r8 (git log -S) | No | Young at 07:18: mori (launch 07:18:05), kama (07:17:03), tabi (06:47:50), from .ufo/watchdog.log launch lines (age ≤ 7200 s) [INFERENCE on the lane-age source] |
| F row-6 path (1) | +path | row-6 GL_EXTRA reason=committed-report … path= (2411) | 1439c47 (r3) | No (no r17 string carries path=) | A lane in row 6 at measure [INFERENCE] |
| G row transitions and value changes (10) | +subject_commits; +window; -subject_commits; -window; -attribution; -example; -rowb_files; basis; age_s; round | row-A GL_EXTRA (2473), row-B GL_EXTRA (2494) | Strings from 1439c47 (r3). window=launch..NOW also appears in the r17 LANE_AUTHOR text (2541), which is not emitted | No: r17 leaves row-A/B strings unchanged and changes no row at the measured state (§5) | Lane row transitions, commit- and time-driven [INFERENCE] |
| H header and counters (4) | HEADER; volatile_fields; obs; io_avg_unavailable | VERSION census:281; DRIFT_COUNTER_KEYS 2744–2770; DRIFT_VOLATILE_SPECIAL 2771 | VERSION: 18d7d55, 8d22d18, 26f6589. Counter growth (kernel_oom_notice…): 18d7d55 | No: no r17 hunk touches 281 or 2744–2771 (§4); counter block identical in 24526ea and HEAD | Live values of obs and io_avg_unavailable [INFERENCE] |
| J r17 IDs (0 tokens) | +FINDING:HEAD_BRANCH_MISMATCH and +FINDING:LANE_AUTHOR_MISMATCH are NOT in the drift | 273aa74/2be8294 emitters | — | — | Not firing at measure (§5) |

Totals: 21 + 9 + 1 + 2 + 1 + 2 + 10 + 4 = 50. Tokens explained by the three r17 commits: **0**.

The c1 register's 8 unclassified tokens (`unclassified_vs_prior_register`) fall as follows: +FINDING:COREDUMP_NOTICE_JOURNAL_USER, +FINDING:SEGFAULT_SIGNAL11_JOURNAL_USER, +FINDING:UNIT_FAILURE_OUT_OF_SCOPE → group B; +path → F; -FINDING:WATCHDOG_STALE → D; age_s, round → G; io_avg_unavailable → H. None is an r17 token.

## 3. Flagged: undeclared default-output changes (candidate census-regression)

Each is latent at the measured state (§5). None blocks the C1 re-pin on the present tokens, because none of them appears in the drift; but each is a default-output behavior without a declaration in SCORECARD, LOG or knowledge.

- **CR-1 has_head semantics.** tools/mori-census.sh:2423–2427 and 2504–2506 (introduced 273aa74). Undeclared: no hit for has_head in LOG.md, SCORECARD.md, SKILL.md, README.md, corpus/**. Drift-invisible by design: has_head is a counter key (census:2746) and its values are masked to `<V>` by drift_normalize (census:2791); the baseline header lists it as volatile (corpus/evidence/baseline-r10-20261015T2231Z.json:4). Live effect: none. Action: declare the new meaning in LOG/knowledge, or restore HEAD-anchored semantics for this token.

- **CR-2 HEAD-branch probe scope.** tools/mori-census.sh:2337 (before row 2 at 2350) and emit at 2537–2538 (state-independent). The finding and warn severity are declared (knowledge/jj-branch-anchor-r17.md:23–24; SKILL.md:164). The scope is not: it fires for young, not-open and report-closed lanes. The falsifier records that no selftest puts a HEAD drift on those states (falsify/CensusNewBranches.md:193–209, "untested"). Action: declare the scope and add a young/not-open selftest, or limit the probe to graded states.

- **CR-3 duplicate HEAD warn for the root.** tools/mori-census.sh:2011 maps protocol and aggregator to $ROOT; the per-lane emit (2537–2538) therefore fires twice for one root divergence, and each adds to the drift count (426–427). Undeclared (falsify/CensusNewBranches.md:181–191, F5). The drift cannot see the duplicate: drift_line_id (census:2812) keys FINDING lines by id, so both lines collapse to one token. Live effect: none (ROOT HEAD equals master). Action: emit once per repository.

- **CR-4 .jj fleet root skips the row-6 closure.** tools/mori-census.sh:2402–2409 (introduced 2be8294): when ROOT is .jj and its mirror does not resolve, root_rev stays empty and ps_report_closed is skipped, so row 9 still grades. Declared only as "not silently graded from HEAD" (knowledge/jj-branch-anchor-r17.md:83–84), not as a skipped closure check. Live effect: none (ROOT has no .jj directory). Action: declare, or make root-unresolved fail closed with reason=ref-unresolved as for lanes.

- **CR-5 branch-name rule narrower than git.** tools/mori-census.sh:2156 (used at 2165, 2180, 2189). Attached branches containing characters outside [A-Za-z0-9._/-] are replaced by origin/HEAD or master/main. Undeclared in prose (falsify/CensusNewBranches.md:143–162, F3, low). The rule matches scripts/hyaku/jj-lane.sh:85 per that falsifier, so it is a disclosed narrowing, not a helper mismatch. Live effect: none (every attached or mirror branch is master or main, §5). Action: declare the narrowing in knowledge/jj-branch-anchor-r17.md.

- **CR-6 (observation, not a change) stale command text.** The SURFACE silence line still says `git -C <root> cat-file -e HEAD:…` (census:2510), but the code runs `cat-file -e "$rev:$rpath"` (census:2278). Output is byte-identical by design (amendment A1, census:2206 and 2535); the decision is recorded only in code comments and in build/CriticHarm.md:62 (K7). Action: change the cmd text or record the A1 text freeze in SKILL.md.

## 4. Non-default changes and precision notes (not flagged)

- P1 `reason=ref-unresolved` literal is only in code (2146, 2328, 2334); the rule is declared (knowledge/…:82–84; SKILL.md:197–198; LOG.md:1195–1196).
- P2 The verdict flip (warn → DRIFT, rc 1) is declared by composition (SKILL.md:164) and asserted by selftests (census:4078, 4093, 4272); no prose states the flip directly.
- P3 GIT_SCRUB (census:580–593) makes output depend on GIT_TRACE* and GIT_CONFIG* in the caller environment. Declared in LOG.md:1195, sensitivity not stated. Current shell has only GIT_EDITOR, GIT_PAGER and GIT_TERMINAL_PROMPT. The watchdog and driver environments were not inspected [INFERENCE: no effect].
- P4 Falsifier F1 (LANE_AUTHOR only in row 9) was real for 273aa74 and is fixed in 2be8294. knowledge/…:26 is accurate at HEAD.
- P5 Residual race (falsify/CensusNewBranches.md:164–179, F4): row 9 reads the moving branch in three calls. Needs a concurrent commit; not flagged.
- Hunk ranges 24526ea..HEAD (new side): 34–47, 212, 407, 568–596, 2134–2275, 2277–2281, 2296, 2309, 2322–2348, 2382–2389, 2397–2439, 2504–2505, 2533–2542, 3012, 3034–3042, 3103–3147, 3221–3231, 4047–4309. Nothing in 2776–2940 (drift normalizer, pin, drift) and nothing in the DRIFT_COUNTER_KEYS block (2744–2770) or DRIFT_VOLATILE_SPECIAL (2771).

## 5. Live-state checks (read-only, taken 07:38–07:40; supports §2 and §3)

- Fleet root (serves protocol and aggregator): attached to refs/heads/master; no .jj directory; no lane.branch; HEAD equals master.
- 14 .jj lanes (chousa, kagi, kaidoku, kake, kama, kasegi, kengaku, kumitate, mado, mori, souji, tabi, tameshi, tsukuroi): lane.branch = master (kaidoku: main); HEAD detached; refs/heads/<lane.branch> exists; HEAD equals the branch tip; merge-base --is-ancestor HEAD rc 0 for all.
- 7 plain-git lanes (audio, game-dev-2d, game-dev-3d, kotoba, kotodama, lore, revenger): attached to main or master; HEAD equals the branch tip; rc 0 for all.
- No commit in any lane's branch history, nor in the fleet root's master history, has a committer `<lane>-shokunin <<lane>@shokunin.local>` with an author email outside @shokunin.local (protocol: 326 committer-identity commits, 0 foreign; aggregator: 11, 0 foreign).
- Young at 07:18 (age ≤ 7200 s): mori, kama, tabi, per the launch lines of /home/vgpnk/Projects/shokunin/.ufo/watchdog.log [INFERENCE that the census LA_EPOCH source is these lines]. Explains +gate_s and +reason (group E).
- falsify/CensusNewBranches.md:245–247 recorded 8 jj lanes on 2026-10-20; today 14 .jj directories exist. The six additional lanes (chousa, kagi, kake, kasegi, kengaku, kumitate) are included in the checks above.

## 6. Reproduce

```
cd /home/vgpnk/Projects/shokunin/mori-shokunin
git show <c> -- tools/mori-census.sh                      # per-commit diff
git show <c>:tools/mori-census.sh | sha256sum             # census identity
git log -S'<token string>' --oneline -- tools/mori-census.sh   # emitter introduction
git diff -U0 24526ea HEAD -- tools/mori-census.sh | grep '^@@'  # hunk ranges
git grep -n -e has_head -e valid_branch -- LOG.md SCORECARD.md SKILL.md README.md corpus
git -C <repo> config --get lane.branch; git -C <repo> merge-base --is-ancestor HEAD refs/heads/<branch>
```

## 7. Gaps and handoff

- The census was not executed, so "no r17 token" rests on the drift token list plus the decision logic applied to read-only live inputs [INFERENCE]. One `--drift` run by the L1 would confirm it; not in this item.
- Groups E, F, G and H attribute live-state tokens without a captured census output. Only the token list exists in the evidence file.
- CR-3 and CR-5 cite falsifier text; the falsifier claims were not re-executed.
- For the roster seat: audio, game-dev-2d and game-dev-3d are still roster lanes after LOG.md:701–704 says they were removed.
- For the drift-normalizer seat: value-level changes in masked fields (has_head) cannot appear as tokens. The C1 register should say so before a re-pin is read as "no regression".
- Tooling: nothing installed or updated.
