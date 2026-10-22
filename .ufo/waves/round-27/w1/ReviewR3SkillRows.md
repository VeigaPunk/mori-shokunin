# ReviewR3SkillRows — re-verification of DraftHygieneKnowledge part (c) (mori round 27, wave 1)

Seat: MoriR27.ReviewR3SkillRows (reviewer, leaf; no subagents, no background jobs). Date: 2026-10-22.
Scope: routed R3 (`corpus/lessons/round-25-verifier-spotcheck.md:182-185`) as drafted for the SKILL.md
round-25 block in `.ufo/waves/round-26/w1/DraftHygieneKnowledge.md` §4 (part (c), rows 1-4 at
`SKILL.md:658-661`), each drafted sentence re-verified against its cited source opened by curl at the
pinned commit. Parts (a)/(b) of the draft are another seat's slice; not reviewed here except where a
part-(c) sentence points into the entry.

**Verdict up front.** Every drafted sentence in part (c) holds at the pinned commit. Four old → new
pairs are ready to apply as **in-place row fixes** (what QUALITY calls for; §5 below). One drafted
accessory is stale and must be renumbered before applying (§2 F2). No drafted sentence fails.

## 1. Method and fetch record (all ordinary fetches, 2026-10-22)

Pinned commit: oh-my-pi `45c35e40c46166dc726ccc52f5d27f40f2449f99` (tag `v18.12.6`), the commit named
in the draft §1 and in SOURCES rows S098-S104/S112-S113. Raw files fetched over
`raw.githubusercontent.com`, sha256 verified against the pins:

| file | bytes | sha256 (prefix) | matches |
|---|---|---|---|
| docs/tools/eval.md | 28,027 | `fb2fc4a1…495c` | S103 pin (SOURCES.md:109) |
| src/eval/agent-bridge.ts | 9,893 | `1c34c1ab…f3bb` | draft §4.5 |
| src/task/workpool.ts | 22,838 | `8cc4b17d…6dc6` | draft §4.5 |
| src/tools/bash.ts | 67,415 | `d985ef25…3ea2` | draft §1 |
| src/tools/eval.ts | 41,679 | `01e9c5c5…20e3` | S113 (SOURCES.md:119) |
| src/async/job-manager.ts | 49,665 | `0f37afaa…544e7` | draft §1 |
| src/task/index.ts | 72,824 | `cd1df9be…82b06` | draft §4.5 |
| src/sdk.ts | — | `c0228add…e6957` | draft §1 |

Plus six files named only as register sites: `eval/judgment-batch-bridge.ts` (`4a174f71…`), `modes/controllers/tan-command-controller.ts` (`efd0130c…`), `security/coordinator.ts` (`61e610c4…`), `task/executor.ts` (`756a1f07…`), `task/restore.ts` (`2d3a06c3…`), `vibe/runtime.ts` (`bbaa9c23…`).

Whole-source enumeration re-run, as the draft did: tarball `codeload.github.com/can1357/oh-my-pi/tar.gz/45c35e40…`,
76,435,207 B, sha256 `645df2d527de1b0ff62514ac14250230622439d5d5e84f781ffa06d38415b8d0` — byte-identical
to the draft's §1 record; `packages/coding-agent/src` extracted, 1,441 `.ts` files. `grep -rn atCapacity`
returns **exactly three** hits: `async/job-manager.ts:338` (the getter), `tools/bash.ts:1228`,
`tools/eval.ts:536`. `grep -rn '\.register(' | grep -v unregister` returns, among other registries,
**exactly twelve** async-job-manager sites, all twelve named by the draft §4 intro:
`eval/agent-bridge.ts:210`, `eval/judgment-batch-bridge.ts:223`, `modes/controllers/tan-command-controller.ts:144`,
`security/coordinator.ts:499`, `task/executor.ts:3272`, `task/index.ts:1407`, `task/restore.ts:85`,
`task/workpool.ts:175`, `task/workpool.ts:363`, `vibe/runtime.ts:1370`, `tools/bash.ts:882`,
`tools/eval.ts:563`. Every other `.register(` hit is a different registry (postmortem, AgentRegistry,
protocol router, writer/history/claims/callbacks/trace registries). The lane file was not modified;
fetched bytes are in `/fast/scratch/hyaku/mori-r27/ReviewR3SkillRows/` (outside the lane).

No `lsp` device exists in this seat's tool inventory, so caller/definition checks were done as byte-level
reads of the pinned sources, not as server-backed references — recorded here rather than passed off as
semantic lookups.

## 2. Findings by severity

- **F1 (confirmation, no defect).** All four drafted row fixes hold; see §3 for the per-sentence fact
  base and §4 for the final pairs. The SKILL.md rows still carry the old text today, so the pairs apply
  cleanly (byte-verified reads of `SKILL.md:658-661`).
- **F2 (defect in the draft's accessory, not in the lane; must fix before applying).** Draft §4.5
  proposes registry ids S114-S120; the registry has since grown past them — `corpus/SOURCES.md` now
  carries S114 (earlyoom README, SOURCES.md:120), S115 (MANPAGE, :121), S116 (meminfo, :122) and
  further rows to at least S131 (32 rows matching `^| S1` today). The three proposed rows are still
  needed (§2 F4), but their ids must be assigned fresh by the integration owner (S132+ is free as of
  this read; the owner owns final numbering). The draft's §2a.2 proposals S114-S117 collide the same way.
- **F3 (wording, optional; the drafted sentence holds as written).** Row 2's new condition cell reads
  "an **auto-backgrounded** bash call … was made while the cap was full" — at the cap the call is
  precisely *not* backgrounded, which is the row's own point and is stated in its report-as cell
  ("runs in the foreground instead"). If the owner wants the condition cell airtight, use the verified
  alternative in §4 pair 2 (variant W); otherwise the drafted wording stands.
- **F4 (confirmation of the draft's "no row today" claim).** `corpus/SOURCES.md` has no row whose
  source is `eval/agent-bridge.ts`, `task/workpool.ts` or `task/index.ts` — the only grep hit for those
  tokens is S103's prose ("…workpool() pools…", SOURCES.md:109), not a row for a file. The three new
  rows remain required; the entry's `task/index.ts` citations (:99-100, :127, :133, :136, :244) are
  likewise rowless today.
- **F5 (confirmation, correction style).** The lane's QUALITY rules call for **in-place row fixes**
  here, not appended corrections; §5 gives the rule citations and the sweep result.

## 3. Fact base behind each drafted sentence (all verified today at `45c35e40`)

- **S103, eval.md:258** — verbatim: "`agent()` fails with `Background job limit reached` once that cap
  is full." Same line: the cap is "default and maximum 100", session-wide, "shared by every other
  background job in the session, including async `bash`, async `task` spawns, `workpool()` pools and
  nested subagents' jobs". Supports row 2's added never-infer clause.
- **eval `agent()` registers with no pre-check** — `eval/agent-bridge.ts:204` takes
  `options.session.asyncJobManager`, `:208-209` reserve id and owner, `:210` `manager.register(` — no
  `atCapacity` anywhere on the path (whole-tree grep: none in this file); `:249-251` is the
  catch/rethrow the draft cites.
- **`workpool()` registers twice, no pre-check** — `task/workpool.ts:169-175` `#ensurePoolJob()` (only
  a duplicate-id check at `:173`) then `manager.register(` at `:175`; `:355-363` `#startTurn` then
  `manager.register(` at `:363`.
- **Explicit `async: true` bash registers with no pre-check** — `tools/bash.ts:1188-1210`
  `if (asyncRequested)` → `#startManagedBashJob` → `manager.register(` at `:882`; no `atCapacity` in
  the branch. The **auto-background** branch is `tools/bash.ts:1220-1229` with the
  `!autoBgManager.atCapacity` conjunct at `:1228` (fall-through to foreground at the cap, comment
  `:1221-1222`).
- **eval auto-background branch** — `tools/eval.ts:533-538`: at `:536`
  `… || !autoBgManager || autoBgManager.atCapacity` → `return await run(signal, emitToolUpdate)` (foreground,
  no refusal) at `:537`; the eval tool's own registration site is `tools/eval.ts:563`.
- **Job-manager core** — `async/job-manager.ts:331-335` the cap getter re-reads a function option at
  check time (row 1's "re-read at every check" citation holds); `:338` `get atCapacity()`; `:343` and
  `:367` both count `status === "running" && !queued` (row 3's population claim and the `:48` type
  union `"bash" | "task" | "eval"` hold); `:371-373` the fixed `Background job limit reached (${maxRunningJobs})…` throw.
- **Task spawn batch** — `task/index.ts:1191-1219` per-spawn try/catch around `#registerSpawnJob`
  (discard at `:1213`), so refusals and starts coexist; `:1221-1231` the all-refused wrapper with
  `results: []` at `:1229`; `:1233-1236` the partial-batch suffix `Failed to schedule N spawn(s)…`;
  `:1407` `return manager.register(`; `:1490` `markRunning()`; `:1565` `queued: true`.
- **Vibe subagent** — `vibe/runtime.ts:1370` `manager.register(` of a `"task"` job labelled
  `` `vibe ${record.cli} ${record.id}…` `` — no `atCapacity` on its path; supports row 3's "a vibe
  subagent" condition.
- **Clamp** — `sdk.ts:2282-2284` `maxRunningJobs: () => Math.min(100, cfgAsyncMaxJobs.get(settings))`
  (sha `c0228add…e6957`), backing row 1 variant B's "value above the clamp … reduces it to 100".
- **Entry cross-references** — `corpus/knowledge/harness-job-capacity-r25.md:184-188` is F12, the dated
  host observation ("read 2026-10-22"), closing with "This is one host on one day, not a fleet fact."
  → row 1 variant B's new clause resolves and is accurate. `:211` is the decision-table `RUNWAY_DEFAULT`
  row recording the false number ("…still reads `RUNWAY_DEFAULT`, effective 100 (a false number;
  round-25 correction, wave-2 CriticHarnessOverclaim H1…)"), naming exactly the three forms the row 4
  caveat lists: a flow-style root mapping (`{async: {maxJobs: …}}`), a JSON-form file, and a
  flow-mapped `maxJobs` child under `async:` → the caveat's mapping, "also"-scoping, and citation all hold.
- **Twelve-ten tally** — the two `atCapacity` pre-checks sit only on the bash and eval auto-background
  branches (`bash.ts:1228`, `eval.ts:536`), so exactly ten of the twelve register sites have no
  pre-check on any of their paths, matching the draft's ten-site list. Precision note, no change
  needed: `bash.ts:882` also serves the explicit-async caller (`bash.ts:1188-1210`) which does *not*
  pre-check — that unchecked path is separately and correctly carried by row 2's never-infer cell and
  row 3's condition cell, so the row-3 tally sentence is consistent as drafted.

## 4. Final old → new pairs, ready to apply (in place; see §5)

Lines are the current working-tree bytes of `SKILL.md`. Pair 1 uses the privacy placeholder
`«OMP-SETTINGS-VALUE»`, which stands for the exact bytes already between `says ` and ` and the clamp`
in `SKILL.md:658`; the applier must paste those bytes unchanged (variant A) or drop them entirely
(variant B). No settings value is reproduced in this report.

**Pair 1 — SKILL.md:658, row 1 host clause (variant B recommended; A is the grammar-only fallback).**

```
OLD: that the operator configured 100 (this host's the operator's OMP settings file says «OMP-SETTINGS-VALUE» and the clamp reduces it to 100);
NEW: that the operator configured 100 (the operator's OMP settings file sets a value above the clamp, and the clamp reduces it to 100; that file is one host's configuration, not a fleet fact — `corpus/knowledge/harness-job-capacity-r25.md` F12);
```

Variant A (if the owner prefers keeping the dated value in place; the entry's F12 already carries the
dated observation, so B loses no recorded fact):

```
NEW: that the operator configured 100 (the operator's OMP settings file says «OMP-SETTINGS-VALUE» and the clamp reduces it to 100);
```

**Pair 2 — SKILL.md:659, full row 2.** NEW is the draft's §4.2 row, verified verbatim; the optional
variant W tightens only the condition cell (F3).

```
OLD: | a bash or eval call was made while the cap was full | nothing — the auto-background branch checks `atCapacity` first and runs in the foreground instead (`tools/bash.ts:1220-1229`, `tools/eval.ts:536`) | that the cap was not reached; that the call was backgrounded |
NEW: | an **auto-backgrounded** bash call, or the eval tool's auto-background branch, was made while the cap was full | nothing from that call — the auto-background branch checks `atCapacity` first and runs in the foreground instead (`tools/bash.ts:1220-1229`, `tools/eval.ts:536`) | that the cap was not reached; that the call was backgrounded; that every call at the cap is silent — eval `agent()`, `workpool()` and an explicit `async: true` bash reach `register()` with no `atCapacity` check and do raise the refusal (`docs/tools/eval.md:258`; `eval/agent-bridge.ts:210`; `task/workpool.ts:175,363`; `tools/bash.ts:1188-1209`) |
NEW (variant W, optional): same row with the condition cell replaced by: | a bash call eligible for auto-backgrounding, or the eval tool's auto-background branch, was made while the cap was full |
```

**Pair 3 — SKILL.md:660, full row 3.** NEW is the draft's §4.3 row (draft line 201), verified verbatim.

```
OLD: | a `task` spawn or an explicit `async: true` bash was refused | one refused registration; a batch can partially start, so refusals and starts coexist in one result | that the wave is dead — a refusal creates no job; that the count was this wave's own seats: the population is every **running, non-queued** job in the session tree — bash, task and eval alike (`job-manager.ts:343,367`, `:48`; `tools/bash.ts:882`) — and a parked (queued) task job counts only after `markRunning()` (`task/index.ts:1565,1490`) |
NEW: | a registration was refused — a `task` spawn, an eval `agent()` or `workpool()` batch, a vibe subagent, or an explicit `async: true` bash | one refused registration; a batch can partially start, so refusals and starts coexist in one result (`task/index.ts:1191-1219`, `:1233-1236`) | that the wave is dead — a refusal creates no job; that the count was this wave's own seats: the population is every **running, non-queued** job in the session tree — bash, task and eval alike (`job-manager.ts:343,367`, `:48`; `tools/bash.ts:882`) — and a parked (queued) task job counts only after `markRunning()` (`task/index.ts:1565,1490`); that the paths named here are the only ones that can refuse — of the twelve `register()` call sites in the shipped source only the bash and eval auto-background branches pre-check `atCapacity`, so ten sites refuse with no check of their own (`eval/agent-bridge.ts:210`; `eval/judgment-batch-bridge.ts:223`; `modes/controllers/tan-command-controller.ts:144`; `security/coordinator.ts:499`; `task/executor.ts:3272`; `task/index.ts:1407`; `task/restore.ts:85`; `task/workpool.ts:175,363`; `vibe/runtime.ts:1370`) |
```

**Pair 4 — SKILL.md:661, row 4 third cell only** (first two cells unchanged). NEW is the draft's §4.4
cell, verified verbatim; the inserted caveat sits between the `RUNWAY_UNKNOWN` clause and the F13 clause.

```
OLD: that the session was at capacity — the tool reports the **cap**, never a running-job count, and the live count is not readable from outside the session (`contract.md:83-84`); that an absent or unreadable clamp means "no clamp" (it is `RUNWAY_UNKNOWN`); that the file's `async.maxJobs` is the value the session resolved — the runtime settings stack has project and overlay layers the tool does not read (`corpus/knowledge/harness-job-capacity-r25.md` F13)
NEW: that the session was at capacity — the tool reports the **cap**, never a running-job count, and the live count is not readable from outside the session (`contract.md:83-84`); that an absent or unreadable clamp means "no clamp" (it is `RUNWAY_UNKNOWN`); that the file sets no `maxJobs` — `RUNWAY_DEFAULT` also reads a root flow mapping, a JSON file or a flow-mapped `maxJobs` child as absent, so the effective 100 is the schema default rather than a value read from the file (`corpus/knowledge/harness-job-capacity-r25.md` decision row `RUNWAY_DEFAULT`); that the file's `async.maxJobs` is the value the session resolved — the runtime settings stack has project and overlay layers the tool does not read (`corpus/knowledge/harness-job-capacity-r25.md` F13)
```

**Companion edits the pairs require (from draft §4.5, id renumbering per F2):**

1. `SKILL.md:646` block header — after the rows land, add the three new source ids to "(sources
   S098–S104, S112–S113)".
2. Three new `corpus/SOURCES.md` rows for `eval/agent-bridge.ts`, `task/workpool.ts`,
   `task/index.ts` at `45c35e40` — the draft §4.5 row bodies (anchors, byte sizes, sha256s) all
   verified today (§1, §3); take their text as proposed but replace the proposed S118/S119/S120 ids
   with fresh ids from the owner (S114-S120 are taken; the registry reaches at least S131 today).

## 5. In place or appended — what the lane's QUALITY rules call for

**In-place row fixes.** QUALITY #77 (`corpus/QUALITY.md:349-355`): "A correction sweeps every mention
in place … every place that states it (body prose, decision-table rows, sibling files) carries the
corrected wording at the commit that carries the correction; the superseded wording is removed, not
shadowed … a statement a critic named explicitly gets its own named correction row." The SKILL.md
block is a decision table, named explicitly by #77, and R3 is the critic-named statement
(`corpus/lessons/round-25-verifier-spotcheck.md:182-185`). Appending a correction block beside the
still-wrong rows is exactly what #77 forbids. QUALITY #4 ("Errata are append-only blocks",
`corpus/QUALITY.md:6`) governs errata *records*, not live decision-table rows; the lane's own round-25
precedent corrected the round-24 entry's statements "corrected in place" and removed the banner
(`corpus/lessons/round-25-verifier-spotcheck.md:165`). So: apply pairs 1-4 in place at the commit that
carries them; the routed-defects ledger row for R3 is the named correction record. Sweep check done:
inside SKILL.md the corrected facts are stated only in the rows themselves (grep for `atCapacity`,
"while the cap was full", `auto-background`, `agent-bridge`, `workpool` → only `SKILL.md:659`), so
pairs 1-4 are the complete SKILL.md surface.

## 6. Drafted sentences that do not hold

None in part (c). One accessory does not hold as proposed (F2): the §4.5 id block (S118-S120, and the
same collision in §2a.2's S114-S117) — content verified, numbering stale. One optional wording
tightening is offered (F3, pair 2 variant W); the drafted wording itself is not false.

## 7. Residual risk and verification gaps

- Unchanged cells were not re-verified: the installed-binary byte offsets in row 1 (`sdk.ts:2284`,
  byte 164406766; `job-manager.ts:371-373`, byte 160033342) and `contract.md:83-84` are pre-existing
  pins outside this item's drafted sentences; the sdk.ts *source* anchor (`:2284`) was verified today.
- The row-4 caveat is deliberately non-exhaustive ("also reads…"); the quoted/escaped/anchored-header
  and indented-root forms live in the entry's `malformed` row and routed R1, not in this caveat.
- The underlying tool defect behind row 4 is routed R1, not fixed by these pairs; until R1 lands the
  caveat stays true of the tool.
- Sibling-file sweep beyond SKILL.md: the entry's F9 and its refusal-observation decision rows keep
  the shorter refusing-path list (draft §5); R3 names the SKILL block, and the entry-side mentions are
  the owner's call when part (a) lands — flagged, not judged here.
- The upstream tree was enumerated over `packages/coding-agent/src` of the `45c35e40` tarball, same
  scope as the draft; a `.register(` call built dynamically (never a literal in source) would not be
  counted by either pass.

## 8. Tooling record

Nothing installed or upgraded: no pacman, uv, cargo or npm transaction (pacman paused host-wide this
round; `~/.omp/agent/RULES.md` read first). Existing read-only tools used: curl, tar, awk, grep,
sha256sum, wc. Lane writes: this report only. Scratch: `/fast/scratch/hyaku/mori-r27/ReviewR3SkillRows/`.
Privacy: no OMP settings value, no harness-settings-file path or line reference, and no journal text
appears in this report; the one value-bearing clause is carried as «OMP-SETTINGS-VALUE» per pair 1.
