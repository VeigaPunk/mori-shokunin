# ReviewSkillPattern — SKILL.md round-25 addition (job-cap refusal pattern and decision rows)

Seat: MoriR25.ReviewSkillPattern (reviewer, leaf: no subagents, no background jobs).
Pinned to: lane HEAD `098d1a5` (2026-10-22 08:52 -0300); the target blobs (SKILL.md `2b7edd2b`, knowledge `20eef3ef`, tool `239dd8eb`, SOURCES) are unchanged at HEAD `98fd5b0` (08:55 -0300). Target: `SKILL.md` lines 643–673.
Source checked against: `corpus/knowledge/harness-job-capacity-r25.md` (blob `20eef3ef`; line numbers below are for that blob) and `corpus/SOURCES.md` rows S098–S113.
Read-only. This report is the only lane file I wrote.

## Verdict

**BROKEN.**

- **Held:** the rule "no instruction may tell an agent to edit settings, kill jobs or split waves". I read all 31 added lines. The only imperative is "mori must state the cap" (a read-only tool run). Every other sentence describes or forbids those acts.
- **Broken:** decision row 2 (SKILL.md:659) says a bash or eval call made while the cap is full is silent. Its own cited source S103 says eval `agent()` fails at that cap. Upstream code agrees: eval `agent()` and `workpool()` register without a capacity check and raise the refusal.
- **Weakened:** the refusal trigger counts quoted prose as a refusal (F4). The wrapper text misses partial-batch refusals (F3). The refusal-path list is too short and its partial-start claim is not in the entry (F2). Row 4 omits a tool false-number caveat that the entry now records, and I reproduced it (F5). Some sentences have no source (F6).
- **Round-25 addition present:** yes, landed in `8ef481e`. The fallback (use the entry's Decision table as the source) was not needed. I still compared each row with the entry's Decision table (lines 216–219).
- **Lane moved during review:** HEAD went `07a31ae` → `e0e33c1` → `098d1a5`. `86477e8` (retention repair) changed SKILL.md in two places (row 1 and the "never acts" line). `51dc820`, `d3b7af2` and `98d1a5` changed the entry. Rows 2–4 and the upstream pointers are the same bytes as the landed block. F9 is pinned to the post-repair text.

## Findings (severity order; evidence, then smallest fix)

### F1 — High — Row 2 says a bash or eval call at the cap is silent. That is false for eval `agent()`, and the entry says "auto-backgrounded".

- SKILL.md:659: "a bash or eval call was made while the cap was full | nothing — the auto-background branch checks `atCapacity` first and runs in the foreground instead".
- The entry carries the qualifier. F9 (line 156): "an auto-backgrounded bash or eval call degrades to a foreground run and raises nothing". Decision row (line 217): "An auto-backgrounded bash or eval call at the cap".
- Counter-evidence at upstream tag v18.12.6 (commit `45c35e40`, fetched as the GitHub tarball, sha256 `645df2d5…`):
  - `docs/tools/eval.md:258` (S103's own quoted line): "`agent()` fails with `Background job limit reached` once that cap is full."
  - `packages/coding-agent/src/eval/agent-bridge.ts:210` calls `manager.register("task", id, …)` with no capacity check. The error is rethrown at `:249–251`.
  - `packages/coding-agent/src/task/workpool.ts:175` and `:363` register with no capacity check.
  - `atCapacity` has exactly three hits: the getter (`async/job-manager.ts:338`), `tools/bash.ts:1228`, and `tools/eval.ts:536`.
- Row 2 also contradicts row 3 for an explicit `async: true` bash call. Row 2 says silent; row 3 says refused. The explicit path (`tools/bash.ts:1188–1209`) has no check.
- **Smallest fix:** row 2 trigger → "an auto-backgrounded bash call, or the eval tool's auto-background branch, at the cap". Report → "runs in the foreground, no error (`tools/bash.ts:1227–1229`, `tools/eval.ts:536`)". Add one sentence: "`agent()` and `workpool()` inside an eval cell, and explicit `async: true` bash, register without the check and do raise (`docs/tools/eval.md:258`; `eval/agent-bridge.ts:210`; `task/workpool.ts:175,363`; `tools/bash.ts:1188–1209`)." Add the same qualifier and paths to entry F9 (lines 142–156).

### F2 — Medium — Row 3 lists too few refusing paths. Its "partial start" claim is true upstream but not in the entry. No SOURCES row covers the task code it cites.

- Upstream has 12 `register` call sites in `packages/coding-agent/src`. Ten take no check at their own call site: `eval/agent-bridge.ts:210`; `eval/judgment-batch-bridge.ts:223` (inside a `try` at 222); `modes/controllers/tan-command-controller.ts:144`; `security/coordinator.ts:499`; `task/executor.ts:3272` (inside a `try` at 3271); `task/index.ts:1407`; `task/restore.ts:85`; `task/workpool.ts:175` and `:363`; `vibe/runtime.ts:1370`. The other two are reached only after a check or with one: `tools/eval.ts:563` (after the check at `:536`, no `await` between), and `tools/bash.ts:882` (reached both through the auto-background check at `:1228` and directly through explicit async bash). Row 3 names two of the ten.
- Partial start is real. `task/index.ts:1191–1219` catches per spawn and keeps going. Successes are pushed at `:1208–1209`, failures at `:1214`. Row 3's "a batch can partially start, so refusals and starts coexist" is therefore correct upstream.
- The entry does not say this. F8 (lines 129–138) describes only the all-refused report (`results: []`, `:1229`). U5 says how many registrations succeed was not measured. The SKILL sentence has no source in the entry or SOURCES.
- SOURCES has no row for any task file. `grep "task/index|task/workpool|eval/agent-bridge|workpool\.ts" corpus/SOURCES.md` returns no match. The entry cites `task/index.ts` in F5, F7, F8 and F10, and SKILL.md cites it in rows 1 and 3, all without a row.
- **Smallest fix:** row 3 → "a task spawn (including eval `agent()` and `workpool()` batches), a vibe subagent, or an explicit `async: true` bash". Entry F8 → add the partial branch with `task/index.ts:1191–1219` and `:1233–1236`. SOURCES → add rows for `task/index.ts`, `task/workpool.ts` and `eval/agent-bridge.ts` at v18.12.6, or stop citing those lines as sourced.

### F3 — Medium — The wrapper text the block tells mori to look for misses refusals in a partial batch.

- SKILL.md:654 gives only "`Failed to start background task job{s}: <agentId>: <message>`".
- Upstream, when no spawn starts, that text is returned with `details.results: []` (`task/index.ts:1221–1231`). When some spawns start, the result is the success text plus a suffix: " Failed to schedule N spawn(s): <agentId>: <message>." (`task/index.ts:1233–1236`, used at `:1249`).
- Effect: a search for "Failed to start background task job" misses partial refusals.
- **Smallest fix:** give both forms on line 654, and say that `results: []` belongs to the all-refused form only.

### F4 — Medium — Row 1 counts any appearance in a transcript as a harness refusal. Quoted prose is not a refusal.

- SKILL.md:658: "the fixed sentence appears in a transcript or tool result". Entry row 216 has the same trigger ("A refusal observed in a transcript").
- The sentence is quoted in prose throughout this lane. Wave-1 `.ufo/waves/round-25/w1/SkillErrorPattern.md` §2 and F6 found literal `(1)` and `(15)` strings in seat transcripts that quote the refusal. I relied on that report and did not re-run its census. This report also quotes the sentence.
- **Smallest fix:** trigger → "the sentence appears as an emitted error or tool result; text quoted in prose (a seat's transcript, a report) is not a refusal". Make the same change to entry row 216, and move the self-quoting limit into the entry (it is now only in the wave-1 report).

### F5 — Medium — Row 4 tells mori to state the cap from the tool, with no caveat for a known false number. I reproduced it.

- SKILL.md:661 lists the verdicts (`RUNWAY_DEFAULT`, exit 0) and a "never infer" list. It omits entry line 211 (H1): a file omp reads as `async.maxJobs: 50` in some shapes is reported as `RUNWAY_DEFAULT`, effective 100.
- Scratch run of the lane tool. Blob `239dd8eb`, unchanged since `8ef481e`. Run from a `git archive` copy under scratch, with five throwaway config files:

| Config shape (scratch file) | Exit | configured | effective | verdict |
|---|---|---|---|---|
| `async:` then `  maxJobs: 50` | 0 | set 50 | 50 | RUNWAY_AS_CONFIGURED |
| `async: {maxJobs: 50}` (one line) | 2 | malformed | null | RUNWAY_UNKNOWN |
| `{async: {maxJobs: 50}}` (root flow) | 0 | absent | 100 | RUNWAY_DEFAULT |
| `{"async": {"maxJobs": 50}}` (JSON) | 0 | absent | 100 | RUNWAY_DEFAULT |
| `async:` then `  {maxJobs: 50}` (flow child) | 0 | absent | 100 | RUNWAY_DEFAULT |

- Cause: rule 1 of the contract reads "no column-0 `async:` line" as `absent`, so these shapes read as the default. Contract amendment A2 asks the tool to abstain on forms it cannot read as omp does, and does not name these shapes.
- I did not run omp, so I did not confirm that omp reads them as 50. The entry says it does.
- **Smallest fix now:** row 4 "never infer" → add "that the file sets no `maxJobs`: `RUNWAY_DEFAULT` also reads a root flow mapping, a JSON file or a flow-mapped `maxJobs` child as absent (entry line 211)". The real repair is a tool change in round 26.

### F6 — Low–Medium — Some sentences have no source in the entry or SOURCES.

- SKILL.md:673 "Only the operator can change the installed binary or the harness build." No source anywhere. The entry's routing paragraph (lines 28–34) says only "Changing the cap is the operator's." → delete, or mark [INFERENCE].
- SKILL.md:666–667 "writes under `~/.omp` are the operator's (`kama-shokunin/PROVINCE.md:45–47`)". The cited text is verified. It is kama's own write boundary, and the entry does not carry it. → cite the entry, or drop.
- SKILL.md:665–666 "Dispatch and wave shape are kumitate's (`PROVINCE.md:65`)". Verified. The entry now states the same routing (lines 28–34, added after the block landed) → cite that paragraph.
- SKILL.md:664–665 "it does not split, shrink or re-dispatch a wave". The entry's Limits say "detection and report only; no settings write; no job cancelled". They do not name split, shrink or re-dispatch. → add the words to Limits, or keep the claim generic.

### F7 — Low — The byte pointer is the `throw` keyword, not the fixed sentence.

- SKILL.md:653 "installed `omp` byte 160033342". Entry F6 (lines 102–103) gives 160033359 for the template.
- Binary read as bytes (mmap, no execution): byte 160033342 begins `throw new Error(\`Background job limit reached (${o})`. Byte 160033359 begins `Background job limit reached (${o})`. The difference is 17, the length of "throw new Error(`".
- **Smallest fix:** "installed `omp` byte 160033359 (the `throw` is at 160033342)".

### F8 — Low — "Fixed text" carries a number that varies. "(100) is the clamp" overstates.

- SKILL.md:651 "The fixed text `Background job limit reached (100). …`". The number is the effective cap at that instant. Entry F6 (lines 106–110) and row 216 say it is a snapshot.
- SKILL.md:658 "so `(100)` is the clamp, not the operator's configured value". (100) equals `min(100, configured)`. It is 100 whenever the configured value is 100 or more, or unset. A configured 100 also prints (100). Row 216 says the configured value being 100 is not proved.
- **Smallest fix:** line 651 → "The fixed sentence template `Background job limit reached (N). Wait for running jobs to finish or cancel one.`, N the effective cap at that instant". Line 658 → "(100) is the effective cap, `min(100, configured)`; it shows 100 whenever the configured value is 100 or more, or unset, so it cannot show the configured value".

### F9 — Low — A host value sits in a durable skill, and the retention repair left a garbled sentence.

- SKILL.md:658 now reads "(this host's the operator's OMP settings file says 200 and the clamp reduces it to 100)". Commit `86477e8` (retention repair) replaced the file path and left the sentence ungrammatical.
- The value 200 is host- and day-specific. Entry F12 (lines 184–188) says "one host on one day, not a fleet fact". Before the repair, the pointer the settings file matched the file on the day I checked (line 244 `async:`, line 245 `maxJobs: 200`).
- SKILL.md:661 still cites "(`contract.md:83-84`)". That path is unqualified; the file is `.ufo/waves/round-25/contract.md`. Its lines 83–85 do say the live count is not readable.
- **Smallest fix:** row 1 → "that the operator configured 100 (this host's OMP settings file, read 2026-10-22, sets 200; entry F12)", or drop the host sentence. Line 661 → cite the entry's Limits ("A cap, not a count") instead of `contract.md`.

### F10 — Low — The header overstates source coverage.

- SKILL.md:646–647: "Grounded in `corpus/knowledge/harness-job-capacity-r25.md` (sources S098–S104, S112–S113)." The block also cites `task/index.ts` lines (1210–1230, 1229, 1490, 1565) that no SOURCES row covers (F2).
- **Smallest fix:** fixed together with F2.

### F11 — Info — Index gap (optional).

- The "## Error patterns" table (SKILL.md:23–45) does not point to the new subsection. One pointer row would fix discoverability.

## Statement ledger (SKILL.md 643–673, blob 2b7edd2b)

| Line | Statement (short) | Grounding | Verdict |
|---|---|---|---|
| 646–647 | Sources S098–S104, S112–S113; anchors at tag v18.12.6 | Entry header; admitted SOURCES rows; tag = `45c35e40` (checked with `git ls-remote`) | Held (F10 for task pointers) |
| 651–652 | Fixed sentence is upstream's `register()` message | S098:372; entry F6 (106–110); `job-manager.ts:371–373` checked | Held (F8 wording) |
| 653 | Byte 160033342 | Entry F6 says 160033359; binary read | Pointer wrong (F7) |
| 654 | Wrapper "Failed to start background task job{s}…" (`task/index.ts:1220–1230`) | Entry F8 (134–136), all-refused only | Partial (F3) |
| 658, row 1 trigger | Sentence "in a transcript or tool result" | Entry row 216 (same trigger) | Over-broad (F4) |
| 658, row 1 report | Registration refusal; effective cap `max(1, floor(min(100, async.maxJobs)))` | Entry F3, F6; `job-manager.ts:334`; `sdk.ts:2284` checked | Held |
| 658, row 1 report | "(100) is the clamp, not the operator's configured value" | Entry F2, F3; row 216 (configured 100 not proved) | Overstated (F8) |
| 658, row 1 never-infer | Operator configured 100; host sets 200 | Entry F12 (184–188) | Host-specific, garbled (F9) |
| 658, row 1 never-infer | Cap still 100 now (`job-manager.ts:331–335`) | Entry F6 (re-read at every check) | Held |
| 658, row 1 never-infer | Refused work did not run; `results: []` at `:1229` | Entry F8 (129–138), row 218; `task/index.ts:1210–1219`, `:1229` | Held for all-refused; silent on partial (F3) |
| 659, row 2 | "A bash or eval call while full → nothing" | Entry F9 (156) and row 217 say auto-backgrounded; S103:258; `agent-bridge.ts:210` | **Contradicted (F1)** |
| 659, row 2 never-infer | Cap not reached; call was backgrounded | Entry row 217 | Held |
| 660, row 3 trigger | Task spawn or explicit async bash refused | Entry F5, F8, F9 | Incomplete (F2) |
| 660, row 3 report | Batch can partially start; refusals and starts coexist | Upstream `task/index.ts:1191–1235` (checked); entry silent (F8 all-refused; U5 "not measured") | True upstream, ungrounded in entry (F2) |
| 660, row 3 never-infer | Wave dead; refusal creates no job | Entry F8 (129–138), row 218 | Held |
| 660, row 3 never-infer | Population is every running, non-queued job, bash/task/eval (`job-manager.ts:343,367,:48`; `bash.ts:882`) | Entry F4, F7; lines checked | Held |
| 660, row 3 never-infer | Queued task counts only after `markRunning()` (`task/index.ts:1565,1490`) | Entry F5 (98–101); lines checked | Held |
| 661, row 4 | Tool command; JSON keys; four verdicts; exit codes | Contract C2 rules 5–6; `tools/mori-job-runway.py:98–108`; entry tool section | Held |
| 661, row 4 | Cap, not a running count; not readable from outside (`contract.md:83–84`) | Entry Limits; contract lines 83–85 checked | Held (F9 pointer) |
| 661, row 4 | Absent or unreadable clamp means RUNWAY_UNKNOWN | Entry rows 213–214 | Held |
| 661, row 4 | File's `maxJobs` is the value the session resolved | Entry F13 (190); U4 | Partial: H1 missing (F5) |
| 663–665 | mori never edits settings, cancels or kills, splits/shrinks/re-dispatches | Entry Limits ("detection and report only", "no settings write", "no job cancelled"); SKILL.md:9, 139–147; PROVINCE.md:12–16 checked | Edit and cancel held; split/shrink/re-dispatch not named in entry (F6) |
| 665–666 | Dispatch and wave shape are kumitate's | `PROVINCE.md:65` checked; entry lines 28–34 (added after block) | Held via entry; SKILL does not cite it (F6) |
| 666–667 | Writes under `~/.omp` are the operator's | `kama-shokunin/PROVINCE.md:45–47` checked; not in entry or SOURCES | Ungrounded (F6) |
| 667–669 | Remedy "finish or cancel one" is the operator's; mori reports, not work order | Remedy text S098:372; entry line 34 covers the cap only | Partial (F6) |
| 671–672 | Refusal not repairable by raising the setting; above 100 cannot lift the cap | Entry F2, F3; S099 (`sdk.ts:2284`) checked | Held |
| 673 | Only the operator can change the installed binary or the harness build | None | Ungrounded (F6) |

Decision rows against the entry's Decision table: row 1 ↔ row 216, row 2 ↔ row 217, row 3 ↔ rows 218–219, row 4 ↔ rows 203–214 (line 211 is the missing H1 caveat).

## Entry defects the block depends on (fix the entry first)

- **K1** (entry lines 142–156; rows 218–219): list `agent()`, `workpool()` and the other non-checking registrations. Cite `docs/tools/eval.md:258` and `eval/agent-bridge.ts:210`. Say which two call sites do check.
- **K2** (entry lines 129–138): add the partial-start branch (`task/index.ts:1191–1219`, `:1233–1236`).
- **K3** (SOURCES): add rows for `task/index.ts`, `task/workpool.ts` and `eval/agent-bridge.ts` at v18.12.6. None exists.
- **K4** (entry row 216): make the trigger "emitted, not quoted", as in F4.
- **K5** (entry line 211; row 4): keep H1. The tool needs a round-26 fix.

## What held

- The edit/kill/split rule (verdict above).
- Upstream anchors at tag `v18.12.6` = `45c35e40c46166dc726ccc52f5d27f40f2449f99` (`git ls-remote --tags`; tarball sha256 `645df2d5…`):
  - `job-manager.ts`: `:331–335` getter; `:338–346` `atCapacity`; `:343` and `:367` count lines; `:348` `register`; `:371–373` the throw; `:48` `AsyncJobType`.
  - `sdk.ts:2282–2286` construction; clamp at `:2284`.
  - `task/index.ts:1210–1219` catch (discard at `:1213`); `:1221–1231` all-refused report (`results: []` at `:1229`); `:1490` `markRunning()`; `:1565` `queued: true`.
  - `tools/bash.ts:882` register; `:1227–1228` check. `tools/eval.ts:536` check.
  - `docs/tools/eval.md:258`.
- Binary `~/.local/bin/omp` (sha256 `85d9daf3…`, 256,702,432 bytes): one clamp site at byte 164406766; `async.maxJobs` setting at 155231590; fixed sentence at 160033359.
- Tool contract (schema, four verdicts, exit codes, output keys) matches row 4 (`tools/mori-job-runway.py` lines 98–108).
- Cross-lane pointers say what the block says: `SKILL.md:9` ("Detection and report only. This lane never remediates."), `SKILL.md:139–147`, `PROVINCE.md:12–16`, `PROVINCE.md:65`, `kama-shokunin/PROVINCE.md:45–47`.
- Admitted rows S098–S104 and S112–S113 exist. S105–S111 are rejected and not cited.
- The landed text equals the wave-1 draft's §3 text. The wave-1 routing question (no tsukuroi on the path) is respected.

## Verification gaps and residual risk

- omp was not run (out of bounds). Not verified: whether omp reads the H1 shapes as 50; any live refusal; the partial-start, `agent()` and `workpool()` refusals at runtime (read from code only).
- Not traced: the body of `#startManagedBashJob`; error handling at `judgment-batch-bridge.ts:222–223` and `task/executor.ts:3271–3272` (both inside `try`); how `workpool()` and the eval cell surface their refusals.
- Not checked: S102's "byte-identical to release asset" claim (not in the block); the round-20 quotations (entry F10); the wave-1 self-quote counts (relied on, not re-run).
- Residual risk: the H1 false number stays until the tool changes. Row 2 keeps misclassifying `agent()` refusals until the entry and block are fixed. The host value will drift.
- The lane is still moving. Findings are pinned to `098d1a5`.

## Commands and tooling record

- Installed or upgraded: nothing. No pacman, uv, cargo or npm transaction.
- Used, all read-only: system `git` 2.56.0 (`diff`, `show`, `log`, `ls-tree`, `rev-parse`, `ls-remote`, `archive`, `status --no-optional-locks`); `curl` (one GET of the pinned tarball, 76,435,207 bytes, HTTP 200); `tar`; python3 stdlib (`mmap`, `hashlib`) reading the omp binary as bytes; the lane's `tools/mori-job-runway.py` from a `git archive` copy under scratch, on five throwaway configs.
- Removed afterwards: `/fast/scratch/hyaku/mori-r25/w2-ReviewSkillPattern` (tarball, extracted tree, copies, diffs).
- Lane: nothing written except this report. Other seats' uncommitted w2 files were left alone.

## Smallest fix set (ordered)

1. Row 2 (SKILL.md:659) and entry F9 (lines 142–156): restore "auto-backgrounded"; add `agent()`, `workpool()` and explicit async bash as raising paths. [F1, K1]
2. Row 3 (SKILL.md:660) and entry F8 (lines 129–138): list the raising paths; add the partial branch; add the task, workpool and agent-bridge SOURCES rows. [F2, K2, K3]
3. Line 654: both wrapper forms. [F3]
4. Row 1 trigger (SKILL.md:658) and entry row 216: "emitted, not quoted". [F4, K4]
5. Row 4 (SKILL.md:661): add the H1 caveat. [F5, K5]
6. Delete or source SKILL.md:673 and :666–667; cite entry lines 28–34 for the kumitate routing. [F6]
7. Line 653: byte 160033359. [F7]
8. Lines 651 and 658: wording on the number. [F8]
9. Line 658: repair the garbled host sentence or drop it; line 661: cite the entry, not `contract.md`. [F9]
10. Line 646: header. [F10]
