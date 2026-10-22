# ReopenS134: re-open of SOURCES row S134 at the landed tip

Seat: MoriR27.ReopenS134 (wave 2, leaf reviewer; no subagents, no background jobs).
Tip: 5f00fd045c137b7e3835506d69946cfd9d010eb5 (master). Working copies of corpus/SOURCES.md, corpus/lessons/round-27.md and SKILL.md are byte-identical to the tip (sha256 77f5ea37…, 44b40848…, 16b3e60c…).
Scratch: /fast/scratch/hyaku/mori-r27/MoriR27.ReopenS134/ (fetched bytes, tarball, tip copies). This file is the only lane write.

## 0. Summary

- Row S134 is accurate at the bytes. The URL, HTTP 200, 9,893 B, sha256, the :204-210 and :249-251 anchors, the tag mapping and "v18.12.6 only" all hold. No high-severity defect.
- Medium: M1, the scope cell claims a cap refusal that S134's own bytes do not contain. M2, SKILL.md:646 grounds the knowledge entry in S134–S136, which the entry does not cite. M3, ReviewR7Knowledge.md:63–64 gives four commits ids that now name other rows. M4, ReviewR7Knowledge.md:158 proposal row reuses the landed id S134.
- Low: L1, the anchor-cell quote is not verbatim. L2, the teaches cell's "degrades to foreground" clause is not in S134's bytes. L3, the gate's located-quote cell is a paraphrase. L4, the R7 review's ids and "next free S133" are stale (next free is S142).

## 1. Source record (the one URL the row names)

| Field | Record | Verdict |
|---|---|---|
| URL | https://raw.githubusercontent.com/can1357/oh-my-pi/45c35e40c46166dc726ccc52f5d27f40f2449f99/packages/coding-agent/src/eval/agent-bridge.ts (SOURCES.md:140) | the only URL in the row |
| Access, UTC | 2026-10-22T17:09:55Z; HTTP/2 200; content-length 9893; x-cache HIT (edge cache; the URL is commit-pinned, so the bytes are fixed) | holds |
| Size, lines | 9,893 B; 253 lines; ends with LF (grep -c '' gives 253) | holds (row: 9,893 B) |
| sha256 | 1c34c1ab4b4ec6d2119025be077e678cdf7074295cd796be6cbbd1d36a10f3bb | holds (row SOURCES.md:140 gives the same value) |
| Second route | codeload tarball of 45c35e40, 2026-10-22T17:15:47Z, 76,435,207 B, sha256 645df2d527de1b0ff62514ac14250230622439d5d5e84f781ffa06d38415b8d0; the file inside it has the same sha256; 1,441 .ts files under packages/coding-agent/src | holds; the tarball hash matches ReviewR3SkillRows.md:33–34 |
| Gate hash | round-27.md:68 table has no hash column; ReviewR3SkillRows.md:23 records 9,893 B and 1c34c1ab…f3bb | consistent; the gate records no hash of its own |
| Tag | api.github.com refs/tags/v18.12.6 gives sha 45c35e40c46166dc726ccc52f5d27f40f2449f99 (fetched 2026-10-22T17:13:25Z). The same commit's packages/coding-agent/package.json says "version": "18.12.6" (line 3; fetched 2026-10-22T17:17:55Z) | holds ("v18.12.6 only") |

## 2. Anchors and quotes (grep -n on the fetched bytes)

| Anchor or quote | Bytes (line: text) | Verdict |
|---|---|---|
| :204-210 | 204 `const manager = options.session.asyncJobManager;`; 205–207 null guard; 208 `const id = await reserveStructuredSubagentId(...)`; 209 `const ownerId = ...`; 210 `manager.register(` | holds |
| Quote `manager.register("task", id, …)` in the :204-210 cell | grep -n 'register("task", id' finds nothing. The call is split across lines: 210 `manager.register(`, 211 `"task",`, 212 `id,` | holds in substance; not verbatim (L1) |
| :249-251 (rethrow) | 249 `} catch (error) {`; 250 `if (error instanceof StructuredSubagentError) throw new ToolError(error.message);`; 251 `throw error;` | holds |
| Gate ":210" (round-27.md:77) | 210 `manager.register(` | holds |
| R3 §3 anchors (ReviewR3SkillRows.md:80–83): :204, :208-209, :210, :249-251 | 204, 208, 209, 210 and 249–251 match as above; the file has no atCapacity | holds |
| Capacity and degrade vocabulary (grep -n -i for capacity, cap, limit, max, degrad, fallback, foreground) | no hit; the only "background" word is the doc comment at 168 | holds ("registers without a capacity check"; no degrade path) |

## 3. Row cells (column order at SOURCES.md:5)

Order: id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by.

| Cell | Claim | Check on the bytes | Verdict |
|---|---|---|---|
| source | "oh-my-pi eval/agent-bridge.ts at v18.12.6" | §1 | holds |
| kind, tier | code, A | TypeScript source; gate row says "admit, A" (round-27.md:77) | holds |
| scope, clause 1 | "it registers without a capacity check" | No capacity check in the file (§2). Tarball grep: atCapacity appears only at async/job-manager.ts:338, tools/bash.ts:1228 and tools/eval.ts:536. maxRunningJobs is read only in job-manager.ts (331–372) and set at sdk.ts:2284; no reader on the agent() path | holds |
| scope, clause 2 | "so it raises the cap refusal rather than degrading" | The refusal is not in S134's bytes. register() throws it at job-manager.ts:369–374 (sha256 0f37afaaa822ef1de845b8eb21473a70210176ff61e2dcff5925f85ec0e544e7, 49,665 B, fetched before 17:12:29Z): 370 `if (activeCount >= maxRunningJobs) {`; 371–373 `throw new Error(` with the message `Background job limit reached (${maxRunningJobs}). Wait for running jobs to finish or cancel one.`. The S098 row cites this range (SOURCES.md:104); S134 does not. "Rather than degrading" holds in S134's bytes: there is no fallback branch, and both catch blocks rethrow (241–243, 249–251) | unsupported by S134's own anchors; true at this commit through S098 (M1) |
| scope, "v18.12.6 only" | pinned tag | §1 | holds |
| anchor | pointers and sha | §2 | holds; wording only (L1) |
| teaches, clause 1 | "A cell that spawns agents can still be refused at the cap" | The agent() path registers with no pre-check (210). The register() refusal leaves through the try that starts at 193, and the rethrow at 249–251 passes it on | holds by composition with S098; S134 cites neither the refusal nor S098 (M1) |
| teaches, clause 2 | "even when the eval tool's own backgrounding degrades to foreground" | Not in S134's bytes. tools/eval.ts (fetched 2026-10-22T17:17:55Z, 41,679 B, sha256 01e9c5c56af15d3e04cdeaf99d959afa90129f8cbb015d6908e02795351920e3, equal to S113's recorded hash): the if at 536 ends with `autoBgManager.atCapacity) {`, and 537 is `return await run(signal, emitToolUpdate);` | unsupported by S134's bytes; holds through S113 (L2) |
| status, opened, recheck | mined; 2026-10-22; on-release | format | holds |
| used-by | SKILL.md | SKILL.md:646 is the only id citation (§5); the knowledge entry does not cite S134 | holds |

## 4. Identity and duplicate checks

- Registry: only SOURCES.md:140 names agent-bridge.ts (git grep -n agent-bridge on corpus/SOURCES.md). Other rows name other files: S098 job-manager.ts, S099 sdk.ts, S112 bash.ts, S113 eval.ts, S135 workpool.ts, S136 task/index.ts. Verdict: not a duplicate of an older row's file.
- git log --first-parent -S'agent-bridge' -- corpus/SOURCES.md lists one commit, 79ecf58 (round-27 R3 rows). The sha256 prefix 1c34c1ab also appears in SOURCES.md only in that commit.
- check-row-identity.py at the tip (read-only; run with -I -B) prints rows=141 changed=5 and flags S090, S093, S096, S097 and S101 only. S134 is not flagged, so its tip cells equal its first-published cells.
- Origin: DraftHygieneKnowledge.md:218 (heading "4.5 Registry rows…") and :221 (the same row, as S118). The landed row differs in two cells only: id (S118 to S134) and used-by (draft: corpus/knowledge/harness-job-capacity-r25.md, SKILL.md; landed: SKILL.md). The narrowing matches the entry's bytes, which carry no S134 citation. Informational: S118 now names an earlyoom row (SOURCES.md:124), so the draft ids are stale, and the landing renumbered them correctly.
- The e398f83 commit never sat under the S134 id: git log -S with its full sha shows only 5f00fd0, where it is S139 (SOURCES.md:145).

## 5. Citing statements

Sweeps at the tip: git grep -n S134 gives 8 lines. Range citations that span S134: ReviewR7Knowledge.md:25, :74, :75 (S133–S136). Anchor-level citations of agent-bridge.ts in live files: SKILL.md:659; corpus/lessons/round-25.md:127–128; corpus/lessons/round-25-verifier-spotcheck.md:151 and :184; plus the wave-1 gate source ReviewR3SkillRows.md:23 and :80–83.

| # | Location | Statement (verbatim, at most 25 words) | Verdict | Sev | Exact correction |
|---|---|---|---|---|---|
| 1 | SOURCES.md:140 | the row itself | see §2–§3 | M1, L1, L2 | §6 |
| 2 | round-27.md:77 | "`:210` (agent() registers with the job manager without a capacity check; quote in …§3)" | holds on anchor and clause; the "quote" is a pointer and a paraphrase, not a located quote | L3 | put `manager.register(` (agent-bridge.ts:210) in the located-quote cell |
| 3 | round-27.md:78–79 | "admit, A, mined (as S134)" for S135 and S136 | holds (same status cells at SOURCES.md:141–142) | none | none |
| 4 | round-27.md:114 | "three source rows S134–S136" | holds (SOURCES.md:140–142; ReviewR3SkillRows.md:171–172) | none | none |
| 5 | SKILL.md:646 | "Grounded in corpus/knowledge/harness-job-capacity-r25.md (sources S098–S104, S112–S113; rows 2–3 also S134, S135, S136, added round 27 for routed R3)" | wrong as worded. "rows 2–3" holds for the SKILL table (SKILL.md:659 cites agent-bridge.ts:210 and workpool.ts:175,363; SKILL.md:660 cites task/index.ts:1191-1219), but the sentence sits in the entry's grounding clause. The entry has no S134–S136 (git grep: zero hits), no "row 2" or "row 3" numbering, and its own source line also names S138–S141 (harness-job-capacity-r25.md:1), which this sentence omits | M2 | "Grounded in corpus/knowledge/harness-job-capacity-r25.md (sources S098–S104, S112–S113, S138–S141). The SKILL table rows 2–3 of this section also cite S134–S136, added round 27 for routed R3." |
| 6 | ReviewR7Knowledge.md:63–64 | "the "(1-100)" description was removed on 2026-05-03 (S134)" | wrong. S134 is agent-bridge.ts (SOURCES.md:140). The e398f83 commit is S139 (SOURCES.md:145) | M3 | line 64: "(S134)" to "(S139)"; "(S135, S136)" to "(S140, S141)" (SOURCES.md:146–147); line 63: "(S133)" to "(S138)" (SOURCES.md:144) |
| 7 | ReviewR7Knowledge.md:158 | proposal row labelled S134 for e398f83, inside a code fence; the section heading at :151 says "owner owns ids" | wrong as an id. Its cells equal the landed S139 row (diff: the id is the only difference) | M4 | relabel as S139, or mark "superseded by S139" |
| 8 | ReviewR7Knowledge.md:25, :55, :74–75 | "next free id is **S133**"; "ids are proposals, next free S133"; "adds S133–S136"; "gains S133–S136" | wrong at tip. S133 is the systemd row (SOURCES.md:139); the R7 rows landed as S138–S141 (SOURCES.md:144–147; harness-job-capacity-r25.md:1). Next free id is S142 (141 rows, max S141) | L4 | mark superseded; next free id is S142 |
| 9 | SKILL.md:659 | "eval/agent-bridge.ts:210" in the Never-infer column | holds: line 210 is manager.register(, the file has no atCapacity, and the refusal comes from job-manager.ts:369–374 | none | none |
| 10 | corpus/lessons/round-25.md:127–128 | "`eval/agent-bridge.ts:210` calls `manager.register("task", …)` with no capacity pre-check" | holds (bytes 210–211; the quoted call is condensed as in L1). The cited async/job-manager.ts:370-373 holds | none | none |
| 11 | corpus/lessons/round-25-verifier-spotcheck.md:151 and :184 | "`eval/agent-bridge.ts:210`, `task/workpool.ts:175,363` register without a capacity check" | holds | none | none |
| 12 | .ufo/waves/round-27/w1/ReviewR3SkillRows.md:23 and :80–83 | the §1 hash row and the §3 fact base | holds: 9,893 B and 1c34c1ab…f3bb; lines 204, 208–209, 210 and 249–251 match the bytes | none | none |
| 13 | .ufo/waves/round-26/w1/DraftHygieneKnowledge.md:221 | the S118 draft row | holds except its id (S118 is an earlyoom row at SOURCES.md:124); historical draft | none | none |
| 14 | other historical anchor mentions in round-25 and round-26 wave reports | agent-bridge.ts:210 in various reports | not each re-verified; they name the :210 line verified in §2. BinaryLocateFacts.md uses binary byte offsets, not source lines | none | none |

## 6. Findings by severity

High: none.

Medium

- M1 (SOURCES.md:140, scope cell). "so it raises the cap refusal rather than degrading" is true at this commit, through job-manager.ts:369–374 (S098). The row's own anchors do not carry it. "Without a capacity check" also reads as "uncapped" unless the row says the check sits inside register(). Exact correction for the anchor cell: append "; the cap check and throw sit inside register() at job-manager.ts:369-374 (S098)". Alternative: narrow the scope to what the bytes show: "it registers without a capacity check, and any register() refusal propagates (:249-251)".
- M2 (SKILL.md:646). Wrong as worded (row 5 above). Exact correction: "Grounded in `corpus/knowledge/harness-job-capacity-r25.md` (sources S098–S104, S112–S113, S138–S141). The SKILL table rows 2–3 of this section also cite S134–S136, added round 27 for routed R3."
- M3 (ReviewR7Knowledge.md:63–64). Wrong at tip (row 6 above). The e398f83 commit is S139, S134 is agent-bridge.ts, and the 2026-09-24 clamp rewrites are S140 and S141 (SOURCES.md:146–147). The 944d7f8d commit is S138 (SOURCES.md:144), not S133.
- M4 (ReviewR7Knowledge.md:158). The proposal row labelled S134 has the same cells as the landed S139 row, so the id is the only difference. Its id now names the agent-bridge row, so a copy would duplicate S134. Exact correction: relabel as S139, or add "superseded by S139".

Low

- L1 (SOURCES.md:140, anchor cell). "manager.register("task", id, …)" is not a verbatim quote. Exact correction: "`:204-210` (`manager.register(` at :210; `"task",` at :211; `id,` at :212)".
- L2 (SOURCES.md:140, teaches cell). "degrades to foreground" is not in S134's bytes. It holds through tools/eval.ts:536–537 (S113). Exact correction: add "tools/eval.ts:536-537 (S113)" to the anchor cell, or add a "see S113" pointer.
- L3 (round-27.md:77). The located-quote cell is an anchor plus a paraphrase, while the gate header says quotes are located (round-27.md:65). Exact correction: put the verbatim line "manager.register(" (agent-bridge.ts:210) in that cell.
- L4 (ReviewR7Knowledge.md:25, :55, :74–75). "next free id is S133", "adds S133–S136" and "gains S133–S136" are stale. S133 is the systemd row (SOURCES.md:139), and the R7 rows landed as S138–S141. Exact correction: mark these superseded; the next free id is S142.

## 7. Residual risk and verification gaps

- The row names one URL. The other fetches (tag API, package.json, job-manager.ts, tools/eval.ts, tarball) test composition and the tag; they are not the row's own URL. The raw-URL response came from an edge cache (x-cache HIT); the commit-pinned URL and the independent codeload tarball gave the same sha256.
- "atCapacity appears only in three places" comes from one tarball extraction in scratch. It covers the shipped source at 45c35e40, not the installed binary.
- I did not re-verify the S098, S112 or S113 rows' own cells, only the lines they point to.
- Historical anchor mentions in other round-25 and round-26 wave reports were not checked one by one (§5 row 14).
- count-c1.sh was not run (out of this assignment). check-row-identity.py was run, read-only.

## 8. Tooling and compliance

- Operator tooling rules were read first. No install or update was needed for this check, and none was made. pacman was not used (paused host-wide).
- Tools and versions used: curl 8.23.0 (ordinary HTTPS fetches; no headless browser); sha256sum 0.8.0 (as reported by the binary); git 2.56.0 (read-only subcommands: show, grep, log, rev-parse, plus one status call disclosed below); Python 3.14.8 (the lane's read-only checker, run with -I -B); GNU tar 1.35 (extraction into scratch only); grep, diff, tr, cut and date.
- Writes: scratch under /fast/scratch/hyaku/mori-r27/MoriR27.ReopenS134/, and this report. No jj command. No lane edit. No unit, service or process action; no oom_score_adj change; no signal sent; omp not run.
- Disclosure: I ran `git status --porcelain --untracked-files=all` once in the lane. My bounds list only show, grep, log, diff, cat-file and ls-tree as read-only git, so this call was outside them. Status may write an opportunistic refresh of the lane index, which I did not check. No content changed, and I ran no add, commit, stash, checkout, switch, reset, pull or push. The owner may want to check the lane index.
- Privacy and retention: this report carries no uid, pid, host command line, journal text, OMP settings value, session identifier, session-store path, or path to the operator's harness settings file.

## 9. Out of scope, observed, not verified

- corpus/knowledge/harness-job-capacity-r25.md:2 gives a value read from the operator's OMP settings file under the key async.maxJobs. The value is withheld here. The lane's privacy rule is key-name only, so the owner should review that line.
