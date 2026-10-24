# ReopenS136 — re-open of SOURCES row S136 (oh-my-pi task/index.ts at 45c35e40)

Seat: MoriR27.ReopenS136 (leaf reviewer, wave 2, round 27). Lane: /home/vgpnk/Projects/shokunin/mori-shokunin. Tip: 5f00fd045c137b7e3835506d69946cfd9d010eb5 (master). Read-only: no lane edits, no git writes, no subagents, no background jobs. Upstream bytes sit in scratch at /fast/scratch/hyaku/mori-r27/ReopenS136/.

## 0. Bottom line

- The bytes hold. The row's URL, HTTP status, byte count, sha256 and tag all match. Every anchor lands on the code it names.
- The teaches cell has one false clause (H1, high): "results: [] belongs to the all-refused shape only." It also has one over-general clause (M1, medium): "A wave's spawns are separate registrations."
- The scope holds in substance. The "all-refused" label omits one condition (L1, low).
- Not a duplicate. S136 is the only registry row that names `task/index.ts`. The row entered at commit 79ecf58 and no earlier row names that file.
- Of the 9 lane lines that cite S136 at the tip: 2 are wrong (ReviewR7Knowledge.md:64 and :160); 3 are superseded history (ReviewR7Knowledge.md:25, :74, :75); 2 hold (round-27.md:79 and :114); SKILL.md:646 holds for its anchors, but its vibe clause (SKILL.md:660) is unsupported (M4); and the S136 row itself (SOURCES.md:142) is split (section 4).
- The false "only" clause has an origin. It was proposed in round 25 (`.ufo/waves/round-25/w2/ReviewSkillPattern.md:45`), carried into the round-26 draft (`.ufo/waves/round-26/w1/DraftHygieneKnowledge.md:223`), and landed as SOURCES.md:142. The round-27 R3 review took the teaches text "as proposed" (`.ufo/waves/round-27/w1/ReviewR3SkillRows.md:173`) after checking anchors, byte sizes and hashes only (lines 172-173).

## 1. Method and commands (all read-only)

1. `date -u` gave 2026-10-22T17:10:12Z. `curl -sS -L -w` on the row URL (`https://raw.githubusercontent.com/can1357/oh-my-pi/45c35e40c46166dc726ccc52f5d27f40f2449f99/packages/coding-agent/src/task/index.ts`) gave http=200, size_download=72824. A second fetch gave the same.
2. `sha256sum` on the fetched bytes: cd1df9be9086ae151a8053688b99c869179413a221a9a0e519a5c8af9cc82b06. `file`: "JavaScript source, Unicode text, UTF-8 text". `wc -l`: 1852.
3. Tag URL `https://raw.githubusercontent.com/can1357/oh-my-pi/v18.12.6/packages/coding-agent/src/task/index.ts`: http=200, size 72824, `cmp` identical to the commit-pinned copy.
4. GitHub API (unauthenticated, GET only): `repos/can1357/oh-my-pi/git/refs/tags/v18.12.6` gave object.type "commit", sha 45c35e40c46166dc726ccc52f5d27f40f2449f99 (lightweight tag). `repos/can1357/oh-my-pi/commits/45c35e40…` gave committer date 2026-10-21T20:49:59Z, message "chore: bump version to 18.12.6". `repos/can1357/oh-my-pi/contents/packages/coding-agent/src/task/index.ts?ref=45c35e40…` gave blob sha 745ef98c7721edaafe204df35510f3cf4945cfe8, size 72824. `git hash-object` on the fetched file gave the same 745ef98c7721edaafe204df35510f3cf4945cfe8.
5. Lane: `git grep -n S136 5f00fd04…` gave 9 lines in 4 files (`git grep -c`: ReviewR7Knowledge.md 5, SKILL.md 1, corpus/SOURCES.md 1, corpus/lessons/round-27.md 2). `git grep -n 'task/index' 5f00fd04… -- corpus/SOURCES.md` gave only line 142. `git log -S'| S136 | oh-my-pi task/index.ts' -- corpus/SOURCES.md` gave only 79ecf58. `git grep -c -i vibe 5f00fd04… -- corpus/SOURCES.md` gave 0.
6. Anchors and quotes: `grep -n` and direct reads on the fetched bytes. Pinned line numbers are in section 3.
7. No `lsp` device was used. The cited code is an upstream blob outside any workspace, and the citing statements are Markdown text. Text grep and direct reads were the method.

## 2. Hash, size, tag and identity

| Check | Result | Verdict |
|---|---|---|
| Row URL, commit-pinned raw | http=200, final URL unchanged | holds |
| sha256 | cd1df9be…82b06, equal to SOURCES.md:142 | holds |
| Byte count | 72,824 B, equal to the row | holds |
| Tag "v18.12.6" | commit 45c35e40…; tag URL bytes equal | holds |
| Blob sha1 cross-check | 745ef98c…, equal to the GitHub contents API | holds (extra check) |
| Hash in Gate (round-27.md:79) | none recorded; the R3 review records the abbreviated `cd1df9be…82b06` at `.ufo/waves/round-27/w1/ReviewR3SkillRows.md:28` | holds (consistent) |
| Duplicate of an older row | none. S136 is the only row naming `task/index.ts`. Older rows cover other files at the same commit: S098 job-manager.ts, S099 sdk.ts, S100 settings.ts, S101 docs/settings.md, S134 agent-bridge.ts, S135 workpool.ts | holds (not a duplicate) |

## 3. Anchor verdicts (bytes at 45c35e40, `grep -n` and reads)

| Row anchor | What the bytes show (line numbers in the fetched file) | Verdict |
|---|---|---|
| :1191-1219 per-spawn register and catch | 1191 `for (const spawn of asyncSpawns) {`; 1192 `try {`; 1193 `this.#registerSpawnJob({`; 1208-1209 successes pushed; 1210 `} catch (error) {`; 1214 failure pushed; 1219 loop closes | holds |
| discard at :1213 | 1213 `spawn.run?.discard(\`background job registration failed: ${message}\`);` | holds |
| :1221-1231 all-refused report | 1221 `if (started.length === 0 && syncSpawns.length === 0) {`; return 1222-1230; 1231 closes the block | holds; label incomplete (L1) |
| results: [] at :1229 | 1229 `details: { projectAgentsDir: null, results: [], totalDurationMs: 0 },` | holds as a literal; the claim about it is wrong (H1) |
| :1233-1236 partial-batch suffix | 1233 `const scheduleFailureSummary =`; 1235 ` Failed to schedule N spawn(s): …`; used at 1249 and 1345 | holds |
| :1407 register | 1407 `return manager.register(` inside `#registerSpawnJob` (1362-1579) | holds |
| :1490 markRunning | 1490 `markRunning();` inside the try at 1489 | holds |
| :1565 queued: true | 1565 `queued: true,` in the register options (1562-1577) | holds |
| Gate range `:1191-1236` (round-27.md:79) | covers the anchors above | holds as a range; no verbatim quote (L4) |

Quoted text in the row: the only quotation is `"results: []"`. It appears literally at 1229. The statement about it is what fails.

## 4. Teaches and scope verdicts (SOURCES.md:142)

Teaches clause 1, "A wave's spawns are separate registrations": holds for non-blocking spawns on the async path (1157 `asyncSpawns = spawns.filter(spawn => !spawn.blocking)`; 1191-1193; 1407). Over-general (M1): blocking spawns never register. They are classified at 1017 `itemBlocking`, split at 1158 `syncSpawns`, and run inline at 1285-1346. A host with no job manager falls back to sync at 1041-1047.

Teaches clause 2, "so one batch can start and refuse at once": holds (1208-1209 starts; 1210-1218 refusals; 1233-1236 suffix).

Teaches clause 3, `"results: []" belongs to the all-refused shape only`: WRONG (H1). Evidence:
- 1169 `const syncResults: SingleResult[] = [];`, and 1177 `results: [...syncResults],` inside `buildAsyncDetails` (1175-1187).
- Both returns on the no-blocking path use `details: buildAsyncDetails()`: 1267 (single spawn) and 1281 (several spawns), inside 1253-1283. No blocking spawn means nothing is pushed to syncResults, so `results` is `[]` on full success and on partial start.
- The mixed return (1349-1353, `details: buildAsyncDetails()` at 1352) carries sync results when they exist.
- Within the batch path (1175-1352), only the all-refused return (1229) lacks the `async` and `progress` keys that `buildAsyncDetails` sets (1181-1186).
- Other `results: []` sites in index.ts: 220 (`createTaskModeError`), 1618 (progress emit), 1720 (per-item failure), 1790 (progress emit), 1818 (`results: salvaged ? [salvaged] : []`, catch-all failure), and a comment at 1500.

Scope, "how a task spawn batch registers": holds, and it is narrower than the bytes (it omits the blocking split at 1017-1025 and the sync fallback at 1041-1047). Not a false statement.

Scope, "how a refusal inside one batch is caught per spawn": holds (1191-1218).

Scope, "the two report shapes": holds as two text forms: "Failed to start background task job…" (1226) and "Failed to schedule N spawn(s)…" (1235). The second form also appears alone at 1345, where a mixed call has every async spawn refused. That is a wording point (L1), not a count error.

Scope, "v18.12.6 only": holds (tag check, section 2).

## 5. Findings by severity

**H1 (high). SOURCES.md:142, teaches clause 3, is false.** Evidence in section 4. Exact correction:
- old: `"results: []" belongs to the all-refused shape only.`
- new: `"results: []" is the literal of the all-refused report (:1229), but every return of the batch path with no blocking spawn carries it too (:1267, :1281 via buildAsyncDetails at :1177), so it does not separate refusal from success.`

Reach: the registry cell is what a reader takes as the teaching. A reader who treats `results: []` as a refusal marker would misclassify every fully async batch. The lane's uses that are correctly scoped: harness-job-capacity-r25.md:135 (all-refused report) and SKILL.md:658 (cites :1229 literally). The loose framing at harness-job-capacity-r25.md:223 is L3.

**M1 (medium). Teaches clause 1 is unscoped.** Blocking spawns never reach `register`.
- old: `A wave's spawns are separate registrations,`
- new: `A batch's non-blocking spawns are separate registrations when a job manager is present (:1157, :1191-1193, :1407); blocking spawns run inline and register nothing (:1017-1025, :1158).`

Reach: a seat count for the job cap would count blocking seats that never occupy a slot. The lane's own [INFERENCE] "each refused seat is a separate registration attempt" (harness-job-capacity-r25.md:164; ReviewR7Knowledge.md:83, :91) still holds, because only non-blocking seats reach `register()`.

**M2 (medium). Traceability gap for the entry that relies on these lines.** S136's used-by is `SKILL.md` only (SOURCES.md:142). The harness entry (corpus/knowledge/harness-job-capacity-r25.md) cites `task/index.ts` at :99 (1565), :100 (1490), :133 (1213), :136 and :249 (1220-1230), and :127 (1046). It never names S136. Its line 1 names S138-S141 and the S098-S113 family, and no S136. Four of the five ranges fall inside S136's anchors. 1046 falls inside no row's anchors. R3 flagged these citations as rowless before landing (ReviewR3SkillRows.md:66-69). QUALITY.md:373 (criterion 81) allows `used-by` to change after landing. The on-release recheck of S136 would not reach the entry today. Options (owner's choice): (a) add `corpus/knowledge/harness-job-capacity-r25.md` to S136's used-by and have the entry name S136 at those lines; (b) give 1046 its own row or an explicit "unsourced" mark.

**M3 (medium). ReviewR7Knowledge.md has stale S-ids that are wrong at the tip.** The review's proposed ids were renumbered at landing; the landed entry already uses the right ids (harness-job-capacity-r25.md:1, :3, :276-277). Corrections for the review file:
- :64 `(S135, S136)` becomes `(S140, S141)`. At the tip S140 is 6962d5cd, the clamp rewrite, and S141 is c4a2441d, the removal (SOURCES.md:146-147).
- :160 row id `S136` becomes `S141` (commit c4a2441d). At the tip S136 is task/index.ts (SOURCES.md:142).
- :63 `(S133)` becomes `(S138)`; :64 `(S134)` becomes `(S139)`; the table at :157-:159 `S133`, `S134`, `S135` become `S138`, `S139`, `S140`.
- Recommended form: a dated correction block, as the lane logs its other in-place corrections (round-27.md:109 and :116).

**M4 (medium). The vibe clause in SKILL.md:660 is unsourced.** Row 3's condition cell reads "a `task` spawn, an eval `agent()` or `workpool()` batch, a vibe subagent, or an explicit `async: true` bash." No SOURCES row mentions vibe (section 1, step 5). The row cell cites no vibe anchor. The clause came from the R3 NEW text (ReviewR3SkillRows.md:156). Upstream, `packages/coding-agent/src/vibe/runtime.ts:1370` does call `manager.register(` at 45c35e40 (http=200, 59,019 B, sha256 bbaa9c238342c7b0e29af6fb5fd54d48fcccdcc37796db2af0be9f0762ce14ed). That file is not in the lane, and I did not trace how its refusal surfaces. SKILL.md:646's "rows 2–3 also S134, S135, S136" holds for every other clause. Correction (owner's choice): add a row with an anchor for vibe/runtime.ts, or change the clause to "a `task` spawn, an eval `agent()` or `workpool()` batch, or an explicit `async: true` bash."

**L1 (low). The all-refused label omits a condition.** :1221 requires `syncSpawns.length === 0`. A call with a blocking spawn and every async spawn refused gets the suffix alone (:1345). Anchor cell, new: `:1221-1231 (all-refused report: no async spawn started and no blocking spawn in the call)`.

**L2 (low, optional). The scope cell is narrower than the bytes.** It omits the blocking split (1017-1025) and the sync fallback (1041-1047). This is not a false statement.

**L3 (low). harness-job-capacity-r25.md:223** gives "the tool returns `results: []`" as part of why a refused seat did not run. The `register()` throw is the valid reason. `results: []` alone does not show refusal (H1). New wording: "`register()` throws before the job exists; `results: []` alone does not show refusal."

**L4 (low). The Gate row for S136 (round-27.md:79) records a line range, not a verbatim quote.** The Gate rule at round-27.md:65 says "Quotes are located and at most 25 words." S134 and S135 (:77-78) follow the same pattern and point to ReviewR3SkillRows §3, which paraphrases (ReviewR3SkillRows.md:99-100). A verbatim quote would be `details: { projectAgentsDir: null, results: [], totalDurationMs: 0 },` (:1229). The Gate row also has no fetch time, unlike the S127-S132 rows.

**L5 (low). Off-by-one range.** harness-job-capacity-r25.md:136 and :249, and SKILL.md:654, cite `task/index.ts:1220-1230`. S136 cites 1221-1231. Line 1220 is blank (length 0). Align both to 1221-1230.

**L6 (low, history only). ReviewR7Knowledge.md:25, :55, :74, :75** ("next free id is S133"; "S133–S136"). These were correct proposals when written. Landing superseded them: the entry uses S138-S141 (harness-job-capacity-r25.md:1, :3). No action beyond M3.

## 6. Citing statements (the 9 lines at the tip)

| # | Location | Statement | Verdict |
|---|---|---|---|
| 1 | corpus/SOURCES.md:142 | the S136 row | split: URL, hash, size, tag, anchors hold; clause 1 over-general (M1); clause 3 wrong (H1); used-by incomplete (M2) |
| 2 | corpus/lessons/round-27.md:79 | Gate: `:1191-1236`, "admit, A, mined (as S134)" | holds; no verbatim quote (L4) |
| 3 | corpus/lessons/round-27.md:114 | "three source rows S134–S136" | holds (the rows exist; 79ecf58) |
| 4 | SKILL.md:646 | "rows 2–3 also S134, S135, S136" | holds for anchors: row 2 cites agent-bridge.ts:210 (S134) and workpool.ts:175,363 (S135); row 3 cites task/index.ts:1191-1219 and :1233-1236 (S136). Row 3's vibe clause unsupported (M4) |
| 5 | .ufo/waves/round-27/w1/ReviewR7Knowledge.md:25 | "next free id is S133"; "S133–S136 as proposals" | holds as written; superseded (L6) |
| 6 | ReviewR7Knowledge.md:64 | "rewritten on 2026-09-24 (S135, S136)" | WRONG at the tip; S140, S141 (M3) |
| 7 | ReviewR7Knowledge.md:74 | "adds S133–S136" to the entry source line | superseded; the landed entry line 1 carries S138–S141 |
| 8 | ReviewR7Knowledge.md:75 | "gains S133–S136" to the recheck line | superseded; the landed entry line 3 carries S138–S141 |
| 9 | ReviewR7Knowledge.md:160 | table row "S136 = oh-my-pi commit c4a2441d…" | WRONG at the tip; S141 (M3) |

Related statements that repeat the false clause or lean on the same framing, without the S136 id:
- .ufo/waves/round-25/w2/ReviewSkillPattern.md:45, "say that `results: []` belongs to the all-refused form only". Origin of H1; wrong for the same reason.
- .ufo/waves/round-26/w1/DraftHygieneKnowledge.md:223, the S120 draft row with the same teaches text. Wrong; carried into SOURCES.md:142.
- .ufo/waves/round-27/w1/ReviewR3SkillRows.md:172-173, the R3 verification scope. Anchors, byte sizes and hashes were verified; the teaches text was taken "as proposed."
- harness-job-capacity-r25.md:164 and ReviewR7Knowledge.md:83, :91, "each refused seat is a separate registration attempt." Holds: refused seats are non-blocking.
- harness-job-capacity-r25.md:135 and SKILL.md:658, `results: []` in the all-refused context. Holds.

## 7. Residual risk and verification gaps

- No runtime test. Every behaviour claim is a reading of the bytes at 45c35e40.
- `policy.effectiveAgent.blocking` (line 1017) is defined outside index.ts. I did not trace it. M1 depends only on the branch structure inside index.ts.
- M4: I checked only that `vibe/runtime.ts:1370` contains a `manager.register(` call. I did not check whether a refusal there surfaces the same way.
- S134 and S135 rows and their anchors were not re-verified (outside my assignment). I used their rows only to confirm they exist and what SKILL.md:659 cites.
- The "v18.12.6" label rests on a lightweight tag that upstream could move. The commit-pinned URL is immutable, so the byte check does not depend on the tag.
- `check-row-identity.py` was not run. S136 is a new row, not an in-place edit, so the check does not apply to it.
- The lane counters (count-c1.sh and similar) were not run. They are not in my assignment.

## 8. Tooling record

- No installs or updates. The operator tooling rules file was read first; nothing needed installing.
- Used, all already present: curl 8.23.0 (fetches); sha256sum (`--version` reports 0.8.0); `jq` on PATH resolves to jaq 3.1.1 at /home/vgpnk/.local/bin/jq (JSON reads only); git 2.56.0, read-only subcommands only (grep, show, log, ls-tree, hash-object without -w); rg 15.1.0 present, not used.
- No pacman transactions. No subagents or background jobs. Writes: this report, and the scratch directory /fast/scratch/hyaku/mori-r27/ReopenS136/.
