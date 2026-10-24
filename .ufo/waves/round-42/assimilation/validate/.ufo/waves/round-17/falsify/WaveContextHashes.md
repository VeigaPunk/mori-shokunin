# WaveContextHashes — recount of wave1/wave2 task, role, spec-SHA/CONTEXT_OK and registry dispatch artifacts

Scope: read-only recount of the retained round-17 dispatch artifacts and pre-dispatch receipts.
No dispatch, no gate/selftest execution, no VCS mutation (only `git cat-file`, `rev-parse`,
`merge-base --is-ancestor`, `ls-tree`, `log` under `--no-optional-locks`). All reads absolute.
Attacked claims only: task/role counts, spec-SHA ↔ CONTEXT_OK receipt match, absence of model
parameters, absence of ghost/replaced seats. Not attacked: claim admission, C1/C2/C3 truth.

## 1. Task and role census (observed, rc0 on every command)

| Artifact | wave1 | wave2 |
|---|---|---|
| `waveN-spec.json` `.items` | 70 | 64 |
| `waveN-dispatch.json` `.taskCall.tasks` | 70 | 64 |
| `.counts.spawn` / `.total` | 70 / 70 | 64 / 64 |
| `waveN-assignments.json` keys | 70 | 64 |
| `waveN-record.json` `.members` | 70 | 64 |
| live `swarm-registry.json` `.members` (build / falsify) | 70 | 64 |
| `waveN-task-response.json` unique `MoriR17.*` ids | 70 | 64 |
| seat reports present | 70/70 (`build/*.md`) | 19 md at read time (wave2 in flight) |

Role census, spec `.role` = registry `.role` = dispatch `.agent` (0 mismatches, 0 duplicates,
0 empty names/prompts):

- wave1: scout 23, scribe 13, reviewer 12, executor 7, connector 6, critic 4, revenger 3,
  sentinel 2 = 70.
- wave2: reviewer 27, scout 17, connector 4, critic 4, mutation-tester 4, executor 3,
  scribe 3, sentinel 2 = 64.

Cross-artifact identity: set(`assignments` keys) = set(`dispatch` task names) = set(`spec` item
names) = set(`record` members) = set(`registry` members) = set(`response_text` ids), both waves;
`comm -23`/`comm -13` returned empty in both directions. No `MoriR17.*` id occurs in both waves.

## 2. Spec SHA ↔ CONTEXT_OK receipt match (the assigned question: it matches)

| wave | spec sha256 | receipt `spec_sha256` | clauses | key shape |
|---|---|---|---|---|
| 1 | `6969eb19533ea65428c1e950271d91482a21a204f947e248c6db405b3907a416` | `6969eb19…` | 8 | 6 keys, **no `clause_ids`** |
| 2 | `6a2dc375e6131ac4c3b2fb342979ff920048e3ee0be9d295237b68ff6760cd2e` | `6a2dc375…` | 12 | 7 keys incl. ordered `clause_ids` |

Ordering (pre-dispatch both waves; `stat` ns mtimes):

- wave1: spec `15:38:00.944` < receipt `15:38:01.152` < dispatch `15:38:06.436` < first attempt
  `15:38:18.213` < successful spawn `15:52:53.313`.
- wave2: spec `16:24:46.856` < receipt `16:24:46.893` < dispatch `16:37:20.544` < first attempt
  `16:37:38.624` < successful spawn `16:46:38.956`.

Byte binding of what seats received: the receipt hashes the whole spec file
(`tools/mori-round17-context-check.py:389,398`), and the dispatched `.taskCall.context` is
byte-identical to the checked `context`: wave1 `532fd8bd…` = `sha256sum wave1-context.txt` (3505
bytes); wave2 `b726dd37…`. Every dispatched task also begins with its spec `.prompt`
(`startswith` true for 70/70 and 64/64); per-task tails are appended after the checked prompt
(see F4).

Pre-correction receipts (retained, expectedly not matching any current file): wave1
`1f588583…` failing `no_tmp_probe_outputs`; wave2 `a38b6b92…` failing `transcript_fields_only`.

Provenance of the retained bytes: both specs, both final receipts, both original receipts, and
wave1's dispatch/assignments/record/response are byte-clean against `HEAD 5c1dfb8d…` (commit
`16:37:09-03`). Wave2 dispatch/assignments/record/response are **untracked** at that HEAD
(commit precedes the `16:37:20` dispatch write). All 9 `PINNED_INPUTS.json` hashes match the
working tree; `fixture_files: 81` resolves as 78 regular + 3 symlinks = non-directory entries
under `fixtures/seat` excluding `expected.json`.

## 3. No model parameters (observed)

Key scans over spec, dispatch and record found no `model`, `temperature`, `top_p`, `top_k`,
`seed`, `max_tokens`, `provider`, `effort` or `thinking` keys. Exact key sets:

- item = `{name, prompt, role}`; task = `{agent, name, task}`;
- member = `{agentId, item, kind, role}`;
- `.compaction.applied == false`; `.resumeSends == []`; `.policy` carries lane counts only.

The six textual `model` occurrences are field names or analysis questions
(`message.model`, `provider/model of terminal errors`, the zai-retry question, and this
assignment's own text), not overrides.

## 4. No ghost / replaced seats (artifact-internal, observed)

- All member kinds are `spawn`; no `resume` anywhere (`.counts.resume == 0`).
- `agentId` is `null` in the pre-spawn dispatch registry (70/70, 64/64) and non-null in the
  post-spawn records (0 nulls); every record id equals its assignment value.
- Suffix convention is uniform: wave1 all `MoriR17.<Name>-5`, wave2 all `MoriR17.<Name>-4`;
  0 deviations. Agent ids are unique within each wave and disjoint across waves.
- No duplicate item names, task names, ids or response lines.
- Response lines pair `MoriR17.X` with job `MoriR17.X` (no re-paired job).
- Assignment files were written after the successful spawn (`15:54:14` wave1; `16:46:38.969`
  wave2, 4 ms after the response) and the registry records after them; refusal history is
  wholesale (70/70 or 64/64 refused four times, then 0 refused), never a partial spawn.
- wave1 has exactly 70 seat reports with names equal to the 70 assignments, no extras; the four
  `mutation-tester` seats own exactly the four clones under `.ufo/worktrees/round-17/`, each at
  base `273aa74…` = `PINNED_INPUTS.measured_commit`.

Boundary: the harness-level live seat roster was not exhaustively enumerated; the no-ghost result
is over the retained artifacts plus the visible roster subset (all visible `MoriR17.*-4` ids are
registry members).

## 5. Findings

**F1 — wave1 pre-dispatch receipt is the 8-clause r16 checker, not the 12-clause r17 checker
(confidence high; low severity; already disclosed).** The wave1 receipt's 6-key payload has no
`clause_ids`, matching `tools/mori-round16-context-check.py:274-280`; the r17 checker always
emits `clause_ids` (`tools/mori-round17-context-check.py:420`), and it could not have produced
that receipt: the receipt is `15:38:01`, while the seat that wrote the r17 checker was not
spawned until `15:52:53` and the lane copy has mtime `16:13:00` (its own report is `16:00:48`). A 12-clause `CONTEXT_OK` run against the
same `6969eb19…` SHA does exist, but only inside the seat report
`build/ContextCheck17.md:92` (report mtime `16:00:48`), i.e. post-dispatch and seat-advisory
under QUALITY39, not a retained pre-dispatch evidence receipt. `build/SkillRegistry.md:374` and
`corpus/lessons/round-17.md:68` already record the 8-clause fact and label the wave1 run "r16
checker", so no retained prose overstates it. The wave1 context text carries all four r17 clause
families (`wave1-context.txt:3` fleet-root/misroot, `:5` VCS-mutation ban, `:7`
background/long-lived/host-service ban, `:9` field-limited transcript reads + no print), which is
consistent with — but does not re-execute — the advisory rc0.

**F2 — the context receipts have no argv/cwd/rc/tool-hash/timestamp (confidence high; low).**
Only `spec_sha256` binds them to evidence; checker-version provenance is inferred from payload
shape, and pre-dispatch ordering from mtimes. This is exactly why F1 must be inferred rather than
read from a receipt. No contradicting receipt exists (`grep -rl spec_sha256` under `.ufo` finds
only these four round-17 files plus reports).

**F3 — wave2's dispatch artifacts are unlanded (observed state, not a defect).**
`wave2-dispatch.json`, `wave2-assignments.json`, `wave2-record.json`,
`wave2-task-response.json` and `falsify/swarm-registry.json` are untracked at `HEAD 5c1dfb8d…`
(`git cat-file -e` rc128). Their ids/roles still agree with the committed wave2 spec and the
committed wave2 receipt; landing is pending with the in-flight wave.

**F4 — the gate covers `context` only; prompts and per-task tails are unchecked (boundary).**
Appended tails are uniform and benign: 70/70 and 64/64 end in the correct
`Report: …/build|falsify/<Name>.md`, with lane-bounds variants 63 leaf-only + 7 labrat for wave1
and 61 + 3 for wave2, matching executor counts 7 and 3 exactly; 0 report-path mismatches. A
manual scan of all 134 prompts for `/tmp`, `agent://all`, `journalctl`, `git add|commit|…`,
`jj metaedit|commit|…` produced 5 wave1 hits (`JjGate`, `ContextCheck17`, `PacmanActorTrace`,
`SrcJjMetaedit`, `ReviewSeatBreachDetect`) and 1 wave2 hit (`ConformanceAudit`); each is a
prohibition or read-only analysis, none authorizes a clause violation. This is a manual scan,
not a gate result, and contradiction detection is outside the gate by its own doc.

## 6. Remaining unknowns

- The pre-correction spec bytes are not retained (only hashes `1f5885…` / `a38b6b92…`), so the
  correction delta that flipped rc1→rc0 is not byte-auditable.
- The wave2 receipt cannot be proven to have been produced by the pinned r17 bytes from the
  receipt alone; its `clause_ids` order matches the tool table.
- No gate, checker or selftest was executed (prohibited for this seat); no harness-level
  exhaustive roster was queried.
- wave2 reports were incomplete at read time; ghost/replacement coverage for wave2 rests on
  dispatch, response and registry artifacts.

## 7. Tooling

No tool installs or upgrades were performed or needed (distribution `python3`, `jq`,
`coreutils`, read-only `git`).

Command anchors: `sha256sum <pinned paths>` rc0 (9/9 match);
`jq -r '.items|length'` rc0 (70/64); `jq -r '.taskCall.tasks|length'` rc0 (70/64);
`comm` set comparisons rc0 (empty diffs); `stat -c '%y %n'` rc0 (ordering above);
`git --no-optional-locks cat-file -p HEAD:<path> | sha256sum` rc0 (clean/untracked table).
Two read-only jq probes failed on operator scoping/quote errors (rc5, rc2) and were redone with
corrected filters; they produced no artifact and are not evidence.
