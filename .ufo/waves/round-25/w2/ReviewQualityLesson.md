# ReviewQualityLesson — round 25, wave 2 (falsify)

Seat: `MoriR25.ReviewQualityLesson` (reviewer, leaf: no subagents, no background jobs).
Scope: QUALITY.md criteria 76–77; `corpus/lessons/round-25.md` (header, learned facts, M1–M3, Gate, routed defects, round-26 bullets).
Measured at lane commit `07a31ae8e2` (lesson body unchanged there). The lane tip moved to `90cc042f22` during the review (wave-2 repairs, including an appended correction block in the lesson at `8aa9fa4`); I re-checked the key facts there. `corpus/QUALITY.md`, `tools/mori-routed-r24.py`, `tools/mori-pressure.py`, the pressure fixtures, `.gitignore`, `corpus/knowledge/system-pressure-r24.md` and `corpus/lessons/round-24.md` are byte-identical at both commits (`git diff --quiet`).
Recommendation only; this is not an admission.

## Verdict

1. **Lesson `corpus/lessons/round-25.md`: weakened.** Gate sourcing holds up (every admitted quote is located at its pinned line; statuses and most counts check). It still has three factual errors, two stale or shadowed statements, one scope error, and three mistake fixes that are not shown able to fail for the case each names (F1–F12 below).
2. **QUALITY 76: citation held; mechanism weakened.** The cited line is real (`corpus/lessons/round-24-verifier-spotcheck.md:137`). The gate that implements it (D1) compares the evidence body only to a hard-coded constant. The byte comparison with the shipping tool's own output happens only under `--rerun`, which never changes the verdict. A forged PASS body over a red tool reads **held** (F1).
3. **QUALITY 77: citation held; rule held for surface forms; defect present at the tip.** The cited lines are real (`:138–143`) and the whitespace/emphasis sweep works. Paraphrase is not covered (F3). Two lines the criterion names still state the contradicted range (F8), and the lesson shadows its own stale bullet instead of removing it (F7). QUALITY 77 says both are defects.
4. **C1 tool at the tip (context only):** `mismatches 0`, `held 4`, hygiene held at `8aa9fa4` and `90cc042f`; `28b79d3d` gives `mismatches 4`; `e54b644` holds D1. Not the calibration verdict; I only used these as checks on M1.

## Mistakes (class, evidence pointer, captured-by, fix shown able to fail)

| Mistake | Class | Evidence pointer | Captured-by | Fix shown able to fail | Verdict |
|---|---|---|---|---|---|
| M1 gate evidence before final tool | stale evidence: accurate | `.ufo/waves/round-24/evidence/c2-selftest-after.txt`, blob `4618daf9` = 35 bytes, one line. `6ee6248` and `13208d2a` print the same 35 bytes (`cmp` equal); `89849a7` prints a second MATCHER line; `SCORECARD.md:1514` (at `28b79d3d`) claims the MATCHER line | QUALITY 31 (text only, no gate); stated honestly | D1 is red for every one of 11 mutants I built (exit 1; revision `0`; non-hex revision; non-ancestor revision; `PASS 11/12`; `MATCHER 47/48`; extra line; wrong tool blob; wrong fixtures tree; wrong command; missing file). Red at `28b79d3d`, held at `e54b644`. **Not** red for a forged body over an unchanged tool (F1) | weakened (F1) |
| M2 over-broad hygiene rule | over-broad hygiene: accurate | `09f55b6` adds `__pycache__/` (diff checked). 212 tracked `.pyc` files, all under `.ufo/waves/round-20/`. Ignored-but-tracked count: 212 with the blanket rule, 0 at the tip | none; stated honestly | **Not shown.** D4 still accepts `__pycache__/`, `**/__pycache__/`, `*.pyc`, `*.py[cod]`, so the same regression reads hygiene held (F2) | not shown able to fail |
| M3 first-cut predicates passed paraphrase | string-presence gates: accurate | `.ufo/waves/round-25/w1/CriticC1Predicates.md:13` and `:39–47`: four edited copies (paraphrase, heading laundering, row deletion, whitespace reflow) | QUALITY 77 (text) and the D2 gate | Shown red for whitespace reflow, emphasis and re-added banner; D3 2 of 6 checked (red). Paraphrase "Averages are recomputed on each read" still held (F3). "A1, A3 and A4 before the tool landed" is **false for A4** (F6) | weakened (F3, F6) |
| M4 (new; appended at `8aa9fa4`, lesson after line 99) | claim reshaping (opinion) | none in the block. Timing checks out: `9b1a2f1` 07:44:17 vs `efaa157` 07:54:12 (−0300), 9 min 55 s; `contract.md:182` names "Main's calibration reminder" | none; stated honestly | "declare before any measurement" is an instruction, not a check | incomplete (F11) |

## Findings (severity order)

### F1 — High — D1 passes a forged body over a red tool (M1 fix; QUALITY 76)

- Evidence: `tools/mori-routed-r24.py:98–101` (`EXPECTED_BODY`); `:506–509` compares the body only to that constant; `:511–525`: `--rerun` is "reported only; it never decides whether D1 holds".
- Reproduction (private clone at `07a31ae`; scratch commits, not in the lane):
  - `R_broken`: change only `tools/fixtures/mori-pressure/cases.json`, case P01 `expect.exit` 0→1. `python3 -I -B tools/mori-pressure.py --selftest` at `R_broken` prints `MORI_PRESSURE_SELFTEST: FAIL 11/12` and `P01: exit 0 != 1`, rc 1. The tool blob is unchanged (`5785c5b2…`).
  - Forged evidence committed on top of `R_broken`: `revision: R_broken`, `tool_blob: 5785c5b2…`, `fixtures_tree` = `R_broken`'s tree, `exit: 0`, and the PASS body.
  - Tool, default: **D1 held, mismatches 0, rc 0.** Tool with `--rerun`: `body_byte_equal: false`, `exit: 1`, and D1 is still held with mismatches 0.
- Context: the committed file at `ec840f9` is truthful (rerun body byte-equal, sha `d767d1b6…`). The gap is in the gate, not the file.
- Why it matters: QUALITY 76 says bytes that differ from what the shipping tool prints at that revision "read red" and "a tally is never a pass because its number looks right". The counted check passes exactly that. Realistic routes: a hand-written body, or output that depends on host or interpreter [INFERENCE, not tested].
- Smallest fix, pick one: (a) make the rerun held-determining (run R's tool from `git archive`; require body byte-equal and exit equal to the header). This needs an amendment, because A1 kept the run optional to keep "git object reads only". (b) If the bound stays, reword M1 and QUALITY 76: the default check pins tool and fixture bytes and a constant body, and stdout equality with R's run is proven only by a recorded `--rerun` receipt. Either way, add the forged-over-red case to the battery and commit its generator (QUALITY 23).

### F2 — Medium — M2's fix is not shown able to fail (D4 accepts blanket rules)

- Evidence: `tools/mori-routed-r24.py:129–136` accepts `__pycache__/`, `__pycache__`, `**/__pycache__/`, `*.pyc`, `*.py[cod]`; `:834` is an exact-line match.
- Reproduction: `.gitignore` as at `09f55b6` (blanket `__pycache__/`): hygiene held, mismatches 0, and `git ls-files -c -i --exclude-standard` gives 212. A `*.pyc` line alone also holds.
- Hygiene is reported, not counted, so no red result fires for this regression.
- Smallest fix: make D4 red when any path tracked at REV matches the ignore rules (the `git ls-files -c -i --exclude-standard` count over a temp extract at REV must be 0), or remove the blanket forms from the accepted set by amendment. Add the `09f55b6` `.gitignore` as a mutant.

### F3 — Medium — M3's paraphrase class still passes D2; the landed regex is narrower than the critic's

- Evidence: `tools/mori-routed-r24.py:109–113` (negatives: `refreshed on (each|every) read`, `spike…invisible`, `null…undefined`). `CriticC1Predicates.md:73–74` recommended `(refresh|recomput|updat)\w* (on|at) (each|every) read`. The landed tool did not adopt it.
- Reproduction: append "- Averages are recomputed on each read (psi.c:1268)." outside the corrections section. D2 held, mismatches 0. Controls that do go red: a line split as "refreshed on / each read"; `**refreshed on each read**`; "this section wins" re-added.
- Smallest fix: adopt the critic's regex, add "recomputed on each read" as a mutant, and state in M3 that the gate is still string-presence.

### F4 — Medium — the headline cap claim is false below 100

- Evidence: lesson line 9, "The harness job cap is 100, whatever the config says." Upstream at `45c35e40`: `packages/coding-agent/src/sdk.ts:2284` is `maxRunningJobs: () => Math.min(100, cfgAsyncMaxJobs.get(settings))`, and `async/job-manager.ts:331–334` floors at 1. A configured value below 100 is honoured (the knowledge entry's table says so: a value of 50 gives `RUNWAY_AS_CONFIGURED`).
- Smallest fix: "The cap is `min(100, async.maxJobs)`, floored at 1. The host's configured value is above 100, so its effective cap is 100."

### F5 — Medium — "only registration paths throw" is an incomplete list (QUALITY 71)

- Evidence: lesson line 16 names explicit async bash and task spawns. `async/job-manager.ts:370–373` throws inside `register()` for every caller. Another caller is `packages/coding-agent/src/eval/agent-bridge.ts:210` (`manager.register("task", …)` for `agent()`, with no capacity check at the call). The lesson's own admitted S103 row quotes `docs/tools/eval.md:258`: "`agent()` fails with `Background job limit reached` once that cap is full."
- Smallest fix: "Every `register()` call throws at capacity (`job-manager.ts:370–373`): explicit async bash, task spawns, eval `agent()` and `workpool()`. Only auto-background bash and eval fall through (S112, S113)."

### F6 — Medium — header and M3 ordering claims are wrong

- Evidence: lesson line 4, "amendments A1–A4 each landed before the code it governs."
  - Commits (−0300): A1 `51ddd01` 07:05:20 and A3 `042d75b` 07:20:37 precede the tool `e54b644` 07:44:02. OK.
  - A4 is recorded in `9b1a2f1` at 07:44:17, 15 seconds after the tool. Its own text (`contract.md:174–180`) describes `e54b644` as "the landed tool". **False for A4.**
  - A5 (`efaa157`, 07:54:12) is missing from the header. It does precede the D5 code (`e68855d` 07:54:52, `e06d4a0` 08:07:03), so it is correct on order.
  - M3 (lesson line 48) says "amendments A1, A3 and A4 before the tool landed". False for A4.
- Smallest fix: "A1 and A3 landed before `e54b644`. A4 landed 15 s after it (`9b1a2f1`) and records the deviation. A5 landed before the D5 code."

### F7 — Medium — the round-26 Axes bullet is stale and shadowed; M1's SCORECARD pointer has moved

- Evidence: lesson lines 97–99 still say the Axes table "still shows round-1 scores (coverage 5, operability 6, depth 4)". At `07a31ae` and `90cc042f` the table shows 6, 7, 5 (`e68855d` fixed it). The appended "Corrections appended before the report" block (lines after 99, added at `8aa9fa4`) says the bullet is false, but the stale bullet is still in place. QUALITY 77: "the superseded wording is removed, not shadowed."
- The routed list (lines 79–90) still omits D5, which C1 counts (`contract.md:190`).
- M1's pointer `SCORECARD.md:1514` resolved at `b5b126f`. At `8aa9fa4` and the tip the MATCHER claim is at line 1518; line 1514 is a different row.
- Smallest fix: delete lines 97–99 (or rewrite them as "fixed at `e68855d`, counted as D5 in `e06d4a0`"); add D5 to the routed list; repoint the M1 pointer to 1518 or to the section heading.

### F8 — Medium — D2 is labelled fixed while two lines the criterion names still contradict the corrections

- Evidence: knowledge entry line 42 (corrections): F3 readers at `psi.c:1540,1545,1550` plus `psi.c:1686`. Body lines 89 and 148 still say the readers are at `psi.c:1538-1550`, a range that excludes 1686.
- Verified fixed at the tip: K4 row (line 19), K5 (lines 20–21), P3 (lines 30–31), K3 rows (lines 178, 182), P4 rows (lines 179, 183). The lesson's "K3 and P4 rows were corrected in the same edit" is true.
- The D2 predicate tests no ranges (D2 held at the tip).
- QUALITY 77: "a contradicted line left standing is a defect whether or not a corrections section exists." The lesson's "fix or explain" heading accepts "not fixed" without an owner or a route.
- Smallest fix: correct lines 89 and 148 to match line 42, or name an owner and a round. Say "D2 partly fixed". Add the range to the D2 predicate as an outside-corrections check.

### F9 — Low — "Refusals in this session's transcripts all name 100" has the wrong scope

- Evidence: `.ufo/waves/round-25/w1/RefusalCensus.md:4` (scope: omp session transcripts under `~/.omp/agent/sessions`) and `:70–73` (window by mtime 2026-10-19..22; 3,424 transcripts in window; 45 workspaces, 2 with hits). The "only 100" result holds for the harness_error tier: 48 occurrences, `100=48` (`:101–102`).
- Smallest fix: "Every harness_error refusal in omp session transcripts under `~/.omp/agent/sessions` with mtime 2026-10-19..22 names 100."

### F10 — Low — "round 24 cited only QUALITY 19 and 70" holds for one column only

- Evidence: `corpus/lessons/round-24.md:60` (M1 captured-by: QUALITY 19) and `:64` (M5: QUALITY 70). Other round-24 artifacts cite QUALITY 9, 11, 23, 54, 72 and 75 (`git grep` over `.ufo/waves/round-24` and the round-24 lesson files). No round-24 artifact cites QUALITY 31.
- Smallest fix: "The round-24 lesson's captured-by column cites only QUALITY 19 and 70; no round-24 artifact cites QUALITY 31."

### F11 — Low — the new M4 (appended at `8aa9fa4`) lacks an evidence pointer and a shown fix

- Evidence: the block after lesson line 99. Its timing is right (see table). No pointer is given (`contract.md:182` and the two commit IDs would do). "Declare the self-assessment rows … before any measurement" is an instruction, not a check. M4 also sits outside the Mistakes section, which lists M1–M3 only.
- Smallest fix: cite `contract.md:182` and the two commits; move M4 into the Mistakes section; name a check, or mark it a process note with no fix claim.

### F12 — Low — operator configuration value in committed material (QUALITY 51 decision)

- Evidence: lesson line 12 states the host's configured value (I did not repeat it here). At `90cc042f` the same value appears in 33 committed files, 5 of them outside `.ufo/`. The knowledge entry's F12 now names "the operator's OMP settings file" but still states the value. The retention scan in `90cc042` reports no new unallowlisted round-25 hits (commit message; not re-run).
- QUALITY 51 excludes "operator configuration values" from committed handoff material. The lane applies that inconsistently (path redacted, value kept).
- Smallest fix: decide whether lessons count as handoff material. If yes, write "the configured value, above 100" in line 12 and in F12. If no, record the ruling in QUALITY 51.

### F13 — Low — the three-round sentinel is stated under one reading only

- Evidence: `.ufo/waves/round-25/w1/CriticSizing.md:122–126` gives a class reading (trips) and a strict same-files reading (does not trip). Lines 134–135 ask the round report to state both. The appended block states only the class reading.
- Smallest fix: add the strict reading.

### F14 — Low — rejected Gate rows lack the located quote QUALITY 60 asks for

- Evidence: `corpus/SOURCES.md` rows S105–S108, S110 and S111, and the lesson's Gate cells, say "none: …" (0 hits). QUALITY 60 requires a located quote, or an explicit screening-only limitation with the access attempts. The bodies were read, so there is no quote; the Gate header still says "Quotes are located."
- Smallest fix: relabel these cells "screening result: body read, 0 hits for X", and state the access attempt (S109 already does).

### F15 — Low — QUALITY 77 cites no line for its whitespace/emphasis clause

- Evidence: QUALITY 77 says the sweep is "whitespace-folded, emphasis-stripped". Its citation `round-24-verifier-spotcheck.md:138–143` does not say that. The wording comes from `contract.md:97–109` (A1, D2 row) and `CriticC1Predicates.md:71`.
- Smallest fix: add those two citations to QUALITY 77.

### F16 — Note — the wave-1 residual list is stale

- Evidence: `BuildRoutedR24Tool.md:327–330` (§7.11) still lists K3, P4 and the `[INFERENCE]` label as residuals. At the tip they are fixed (knowledge lines 178, 182, 183). Only the F3 range remains. The lesson is right on K3/P4.

### F17 — Note — evidence sits outside the lane (QUALITY 23)

- The 41-case battery is `/tmp/morifals/falsify.py` (`BuildRoutedR24Tool.md:342`). The survivor replay is in `/fast/scratch/hyaku/mori-r25/wt-survivors` (`SurvivorReplay.md:4–7`). The refusal counter is in scratch (`RefusalCensus.md:5–7`). The sandbox commits cited by the builder (`5117b5f8…`, `666257c…`) do not resolve in the lane. None is committed with a generator and a digest.
- Smallest fix: commit the generators and digests, or cite these results as unrun.

### F18 — Note — D1 hard-codes the tallies

- Evidence: `tools/mori-routed-r24.py:98–101` pins `PASS 12/12` and `rejected 48/48` as literals. The next legitimate pressure-tool change (for example, more main cases) turns D1 red until the literal is edited. `PatternStaleEvidence.md` §5 says so.
- Smallest fix: derive the expected body from R's run (the `--rerun` path; see F1).

### F19 — Note — the depth claim is not exhaustive

- Evidence: lesson line 98 says "every later round holds coverage 6, operability 7, depth 5". `SCORECARD.md` shows depth 5 in several later rounds (lines 1019, 1056, 1161, 1237, 1300, 1339, 1357, 1405 at `28b79d3d`). Coverage 6 is traced by `ReviewLessonR24Counts.md`. I did not check every round.

## Number check (every number in the lesson, against its cited report or command)

| Lesson line | Number or claim | Checked against | Result |
|---|---|---|---|
| 4 | "amendments A1–A4" | `contract.md` (A1–A5), commit order | ✗ omits A5; A4 after tool (F6) |
| 9 | "cap is 100, whatever the config says" | `sdk.ts:2284`; `job-manager.ts:331–334` | ✗ below 100 (F4) |
| 9 | `Math.min(100, cfgAsyncMaxJobs.get(settings))`; omp 18.12.6 | `sdk.ts:2284` at `45c35e40`; `packages/coding-agent/package.json` = 18.12.6; binary byte 164406766 | ✓ |
| 10 | floors at 1 (S098) | `job-manager.ts:331–334` | ✓ |
| 10 | counts running, non-queued jobs of every type | `job-manager.ts:342–343, 365–368`; `AsyncJobType` at `:48` | ✓ |
| 11 | configured value → effective cap 100; `RUNWAY_CLAMPED` | `python3 -I -B tools/mori-job-runway.py`: configured `set` equal to the lesson's value, clamp `found` 100 (1 site), default 100 (1 site), effective 100, verdict `RUNWAY_CLAMPED`, rc 1. Value compared, not repeated | ✓ |
| 12 | settings reference: default and floor, no maximum (S101) | `docs/settings.md:623` | ✓ |
| 13 | "default and maximum 100" only on the eval page (S103) | grep of `docs/`, `packages/coding-agent/README.md`, `CHANGELOG.md` at `45c35e40` | ✓ (within those paths) |
| 13 | ceiling dates from the feature's first commit (S104) | `476b858b` diff: `sdk.ts` `Math.min(100, Math.max(1, …) ?? 15)` | ✓ |
| 15 | atCapacity fall-through (S112, S113) | `bash.ts:1221–1228`; `eval.ts:533–536` at `v18.12.6` | ✓ |
| 16 | only registration paths throw | `job-manager.ts:370–373`; `agent-bridge.ts:210`; S103 quote | ✗ (F5) |
| 18 | refusals all name 100 | census harness_error: 48 occurrences, `100=48` (`RefusalCensus.md:101–102`) | ✓ numbers; ✗ scope (F9) |
| 19 | 48 failed calls; 24 transcript files | `RefusalCensus.md:101` (`occurrences=48 files_with_hits=24`) | ✓ |
| 19 | 2026-10-20T13:55Z to 2026-10-22T10:04Z | `RefusalCensus.md:103, :105` (13:55:38.259Z; 10:04:50.044Z) | ✓ |
| 22 | 85 from state file; 200 by default | `SeatGateRelation.md:16–19` | ✓ |
| 27–28 | blob `4618daf9`; one line `PASS 12/12` | `git cat-file`: 35 bytes, one line | ✓ |
| 28 | output of the tool at `6ee62487` | `6ee6248` prints the same 35 bytes; `13208d2a` equals the committed blob | ✓ |
| 29 | landed in `89849a7`, which adds MATCHER | `89849a7` prints PASS and MATCHER (82 bytes) | ✓ |
| 30 | `SCORECARD.md:1514` claims MATCHER | `28b79d3d:1514` ✓; `8aa9fa4` and tip: line 1518 | ✓ at `28b79d3d`; ✗ at tip (F7) |
| 30 | 16 unbound files; 15 re-run; 3 stale | `PatternStaleEvidence.md` §1, §2 and class table (3 stale of 15 re-run). Its totals line sums to 15 without the mutant control | ✓ with a note |
| 33 | QUALITY 31 at `corpus/QUALITY.md:73` | `corpus/QUALITY.md:73` | ✓ |
| 33–34 | round 24 cited only QUALITY 19 and 70 | `round-24.md:60, :64` | ✓ scoped to captured-by column (F10) |
| 34 | two round-24 wave-2 seats reported the file as prose | `LiveBracketCheck.md:330–333`; `RerunC2Count.md:199–201`; `ReviewKnowledgeFacts.md:222–225` | ✓ |
| 36–39 | D1 red at `28b79d3d` (evidence_file_missing); green at `e54b644b`; 10 D1 mutants red | sandbox runs: 11 of 11 mutants red with the expected reasons; `28b79d3d` red; `e54b644` held (D1 code unchanged from `e54b644` to tip: no hunk in `_check_d1`) | ✓ |
| 42–44 | `09f55b62` adds `__pycache__/`; 212 tracked `.pyc`, all under round-20; 212 → 0 | `git show 09f55b6 -- .gitignore`; `git ls-files` (212, all `.ufo/waves/round-20`); blanket = 212; tip = 0 | ✓ |
| 45 | `e43d8831` narrows to `tools/__pycache__/` | `.gitignore` at tip | ✓ |
| 48 | four edited copies | `CriticC1Predicates.md:13, :39–47` | ✓ |
| 48 | "A1, A3 and A4 before the tool landed" | commit ancestry: `51ddd01`, `042d75b` precede `e54b644`; `9b1a2f1` (A4) follows it | ✗ A4 (F6) |
| 49 | builder's 13 D2 and 6 D3 mutants red | `BuildRoutedR24Tool.md` §6 (report); my runs: 2 of 6 D3 red, 3 of 13 D2 probes as expected, paraphrase held | partly reproduced; rest unrun |
| 53–73 | Gate: quotes located, ≤ 25 words, pinned tag | 9 admitted quotes located at pinned lines; longest 18 words; tag `v18.12.6` = `45c35e40` | ✓ (S100 cites 941–946; quote is 942–945, immaterial) |
| 56–73 | S102 offset 164406766; sha `85d9daf3…` | byte search; `sha256sum ~/.local/bin/omp` | ✓ |
| 56–73 | statuses: S098–S104, S112–S113 mined; S105–S111 rejected | `corpus/SOURCES.md:104–119`, status column | ✓ |
| 56–73 | access times precede carrying commits | 10:06–10:10Z vs `90ed9b7` 10:20Z, `cb51e84` 10:24Z | ✓ |
| 76–77 | 18 candidates; 1 admitted (S103); 17 rejected; seven recorded as rows | `SrcRejections.md` §2, §5 coverage; registry holds seven | ✓ |
| 81 | D1 fixed at `7bb0fe61` | `git log` | ✓ |
| 82–84 | D2 fixed at `02084f27`; K4 row; banner removed; K3, P4 corrected; two F3 ranges open | knowledge lines 13, 19, 178–183 (corrected); 89, 148 (open) | ✓ facts; ✗ "fixed" wording (F8) |
| 85 | D3 correction at `round-24.md` | `round-24.md:98–100`; D3 mutant red | ✓ |
| 86 | D4 `tools/__pycache__/` | `.gitignore` | ✓ |
| 87–90 | six survivors; all killed at tip; five only by supplementary; nine neighbours; S08–S16; `ec840f9d`; opt-in via `--cases` | `SurvivorReplay.md` §3–§5, §7 (report only); file has 16 cases; `PASS 12/12` frozen and `PASS 16/16` with `--cases` (run); no committed runner | ✓ run parts; survivor kills unrun (F17) |
| 94–96 | sentinel trips (rounds 23–25) | `CriticSizing.md:122–124` (class reading) | ✓ one reading (F13) |
| 97 | Axes round-1 scores 5, 6, 4 | `28b79d3d` top table | ✓ at `28b79d3d`; ✗ at tip (F7) |
| 98 | every later round: coverage 6, operability 7, depth 5 | tip top table (6, 7, 5); SCORECARD round lines | partly (F19) |
| appended | ~ten minutes; 3-of-3; D5 at `e68855d` | `9b1a2f1` to `efaa157` = 9 min 55 s; `routed-r24-after` held 3 of 3; `e68855d` | ✓ |

## Criteria 76–77

- **76.** Cites `corpus/lessons/round-24-verifier-spotcheck.md:137` (real; says "Commit future selftest outputs with the measured revision and the full stdout") and `PatternStaleEvidence.md`.
  - Implemented: the header fields in order; the tool blob and fixtures tree equal at R and REV; `exit` present.
  - Not enforced by default: `exit` equal to R's real exit, and the body equal to R's real stdout (F1).
  - Mechanism sentence ("every stale file … landed in a commit that also edited the tool"): supported by `PatternStaleEvidence.md` (3 of 3).
  - Verdict: citation held; mechanism weakened.
- **77.** Cites `:138–143` (real). Line 140 supports "a statement a critic named explicitly gets its own named correction row" (knowledge line 19 has the K4 row).
  - Implemented and verified: whitespace-fold, emphasis-strip, banner (red when re-added).
  - Not covered: paraphrase (F3). Two named lines still stand at the tip (F8). The lesson shadows its stale bullet (F7). The whitespace/emphasis clause has no cited line (F15).
  - Verdict: citation held; rule held for surface forms; defect present at the tip.

## Verified as held

- C1 tool: `mismatches 0`, `held 4`, hygiene held at `07a31ae`, `8aa9fa4` and `90cc042f`; `28b79d3d` gives `mismatches 4`; `e54b644` holds D1.
- The D1 evidence file at `ec840f9` reruns byte-equal (sha `d767d1b6…`).
- Pressure selftest: `PASS 12/12` (frozen) and `PASS 16/16` with `--cases` (supplementary, 16 cases).
- Runway live run: `RUNWAY_CLAMPED`; selftest `PASS 21/21`.
- Gate quotes, S102 byte offset and sha, the S104 first-commit ceiling, the S101 "no maximum", the S103 "default and maximum 100" (docs only).
- Knowledge corrections K3, K4, K5, P3, P4 at the tip; banner removed.
- Lesson pointers `corpus/QUALITY.md:73` (still criterion 31 at the tip).

## Verification gaps (unrun checks are not passes)

- Builder's 13 D2 and 6 D3 mutants: I ran 3 D2 probes and 2 D3 mutants.
- Survivor replay (six survivors; "five only by the supplementary file"): report-level only; harness outside the lane.
- Refusal census counts: report-level only; the transcripts are private and I did not re-scan them.
- Rejected-row "0 occurrences" claims: checked against `SrcRejections.md`; the pages were not re-fetched.
- "Every later round" claims (F19): not exhaustive.
- `ReviewPycacheRule` claim that the rule "would hide evidence caches from `git add -A`": not re-checked.
- Retention gate result (`90cc042`): commit message only; not re-run.
- Lane tip moved during review; the last check was at `90cc042f22`. The `wave-2` seat reports added at `90cc042` (other seats) were not cross-read.

## How the checks were run (reproducible from committed lane bytes)

- Private clone of the lane (read only); tool runs as `python3 -I -B tools/mori-routed-r24.py --repo <clone> --rev <rev>`.
- F1: scratch commit changing `cases.json` P01 `expect.exit` 0→1; `git archive <R> tools/mori-pressure.py tools/fixtures/mori-pressure | tar -x`, then `python3 -I -B tools/mori-pressure.py --selftest` (FAIL 11/12, rc 1). Forged evidence committed on top with `revision`, `tool_blob`, `fixtures_tree`, `exit: 0` and the PASS body; tool run with and without `--rerun`.
- F2: scratch commit with `.gitignore` = the `09f55b6` content; `git ls-files -c -i --exclude-standard | wc -l` gives 212.
- F3: scratch commit appending the paraphrase outside the corrections section; tool run.
- M1 history: `git archive` at `6ee6248`, `13208d2a`, `89849a7`, each followed by the pressure selftest.
- Runway: `python3 -I -B tools/mori-job-runway.py` (reads the config and the binary's bytes; never runs omp).
- Scratch clones and sandbox trees removed afterwards (upstream clone 302 MB; mutation sandbox; private clone). Other seats' scratch directories were not touched.

## Tooling record and bounds

- Installs and upgrades: none. Tools used: `git`, `python3 -I -B`, `sha256sum`, `curl`, `gh api` (read only), and the lane's read tools.
- Upstream fetched by ordinary means: 7 raw files at `45c35e40` / `v18.12.6` (raw.githubusercontent.com); the commit `476b858b` and the tag ref (api.github.com); a depth-1 `git clone` of `can1357/oh-my-pi` at `v18.12.6`. No bot challenge or captcha was met, and I left no source unopened.
- `~/.local/bin/omp`: read as bytes only (`sha256sum` and a byte search). omp was not executed.
- Lane: read only (`git --no-optional-locks`; `git fetch` from the lane into the private clone). No `git add`, `commit`, `stash`, `checkout`, `reset`, `pull` or `push` in the lane; no jj commands. The only lane write is this report.
- No secrets, transcripts or session identifiers are quoted here. The configured value is referred to by line, not repeated.
