# Round 25 — lesson (mori, L1 MoriR25)

author: MoriR25 (L1), from wave-1 seat reports under `.ufo/waves/round-25/w1/`.
Contract: `.ufo/waves/round-25/contract.md` (declared at `7634be75`; amendments A1–A4 each landed before the
code it governs).

## What the round learned

- **The harness job cap is 100, whatever the config says.** omp 18.12.6 builds one background-job manager per
  root session with `maxRunningJobs: () => Math.min(100, cfgAsyncMaxJobs.get(settings))` (S099, S102), floors it
  at 1 (S098), and counts every job that is running and not queued, of every type (bash, task, eval; S098).
  This host configures `async.maxJobs: 200`, so the effective cap is 100 (`tools/mori-job-runway.py` live run,
  `RUNWAY_CLAMPED`). The settings reference states a default and a floor but no maximum (S101); only the eval
  page says "default and maximum 100" (S103). The ceiling dates from the feature's first commit (S104).
- **A reached cap is not always an error.** Auto-backgrounded bash and eval calls check `atCapacity` and fall
  through to a foreground run (S112, S113); only registration paths (explicit async bash, task spawns) throw
  `Background job limit reached (100)`. Observed refusals are therefore a lower bound on cap pressure.
- **Refusals in this session's transcripts all name 100.** Wave-1 seat RefusalCensus counted 48 failed tool
  calls carrying the text in 24 transcript files from 2026-10-20T13:55Z to 2026-10-22T10:04Z, every one with
  `(100)` (`.ufo/waves/round-25/w1/RefusalCensus.md`; counts only, no content).
- **The seat gate and the harness count different things.** `wave-slot.sh` counts estimated live agents against
  a target (85 from its state file today, 200 by default); the harness counts running non-queued jobs against 100
  per root session. A grant is not a harness reservation (`.ufo/waves/round-25/w1/SeatGateRelation.md`).

## Mistakes

- **M1 — gate evidence written before the final tool (class: stale evidence).**
  Evidence: `.ufo/waves/round-24/evidence/c2-selftest-after.txt` (blob `4618daf9`) holds one line,
  `MORI_PRESSURE_SELFTEST: PASS 12/12`, the output of the tool at `6ee62487`; it landed in `89849a7`, the same commit
  that taught the tool to print `MATCHER: rejected 48/48`, which `SCORECARD.md:1514` claims. Wave-1 seat
  PatternStaleEvidence found the class recurring: 16 selftest-output files in rounds 18–24 name no revision, and
  of 15 re-run, 3 are stale, every one landed in a commit that also edited the tool it reports on.
  Captured-by: QUALITY 31 (`corpus/QUALITY.md:73`) already stated the bar; round 24 cited only QUALITY 19 and 70,
  and two round-24 wave-2 seats reported the file as prose without a gate.
  Fix: QUALITY 76, and `tools/mori-routed-r24.py` item D1, which reads `.ufo/waves/round-25/evidence/pressure-selftest.txt`
  (revision, command, tool blob, fixture tree, exit, exact body). Shown able to fail: red at `28b79d3d`
  (`evidence_file_missing`), green at `e54b644b`; the builder's 10 D1 mutants (wrong exit, wrong revision,
  `PASS 11/12`, `MATCHER 47/48`, extra line, wrong tool blob or fixture tree, wrong command, missing file,
  non-ancestor revision) each turn it red (`.ufo/waves/round-25/w1/BuildRoutedR24Tool.md`).
- **M2 — the L1's own D4 fix hid committed evidence (class: over-broad hygiene rule).**
  Evidence: commit `09f55b62` added `__pycache__/` to `.gitignore`; wave-1 seat ReviewPycacheRule showed it matches
  212 tracked `.pyc` files under `.ufo/waves/round-20/` and would hide new evidence caches from `git add -A`.
  Captured-by: none; the D4 predicate accepted every blanket form. Fix: `e43d8831` narrows the rule to
  `tools/__pycache__/`; `git ls-files -c -i --exclude-standard | wc -l` goes 212 → 0.
- **M3 — first-cut predicates passed on paraphrase (class: string-presence gates).**
  Evidence: the contract's original D2 and D3 predicates passed four edited copies that kept the false
  statements (`.ufo/waves/round-25/w1/CriticC1Predicates.md`). Captured-by: QUALITY 77 now names the
  whitespace-folded, emphasis-stripped sweep. Fix: amendments A1, A3 and A4 before the tool landed; the builder's
  13 D2 and 6 D3 mutants each turn the tool red.

## Gate (new SOURCES rows, opened 2026-10-22)

Quotes are located and at most 25 words. Upstream rows are pinned to tag `v18.12.6` = commit
`45c35e40c46166dc726ccc52f5d27f40f2449f99`.

| Row | URL | Accessed | Located quote | Decision |
|---|---|---|---|---|
| S098 | https://raw.githubusercontent.com/can1357/oh-my-pi/45c35e40c46166dc726ccc52f5d27f40f2449f99/packages/coding-agent/src/async/job-manager.ts | 2026-10-22T10:10:54Z | :372 "Background job limit reached (${maxRunningJobs}). Wait for running jobs to finish or cancel one." | admit, A, mined |
| S099 | https://raw.githubusercontent.com/can1357/oh-my-pi/45c35e40c46166dc726ccc52f5d27f40f2449f99/packages/coding-agent/src/sdk.ts | 2026-10-22 | :2284 "maxRunningJobs: () => Math.min(100, cfgAsyncMaxJobs.get(settings))," | admit, A, mined |
| S100 | https://raw.githubusercontent.com/can1357/oh-my-pi/45c35e40c46166dc726ccc52f5d27f40f2449f99/packages/coding-agent/src/tools/settings.ts | 2026-10-22 | :941-946 `id: "async.maxJobs", protocolDefault: ["rpc"], type: "number", default: 100,` | admit, A, mined |
| S101 | https://raw.githubusercontent.com/can1357/oh-my-pi/45c35e40c46166dc726ccc52f5d27f40f2449f99/docs/settings.md | 2026-10-22 | :623 "`async.maxJobs` \| number \| `100` \| Running background-job cap, floored to at least 1" | admit, A, mined (the missing maximum is the finding) |
| S102 | own-work: `~/.local/bin/omp`, sha256 `85d9daf3a05fc76e8cd425ae1904eb576af8d21cc85fcf4690742626e07ccfa4` | 2026-10-22 | byte 164406766 "maxRunningJobs: () => Math.min(100, XPe.get(R))" | admit, A, mined |
| S103 | https://raw.githubusercontent.com/can1357/oh-my-pi/45c35e40c46166dc726ccc52f5d27f40f2449f99/docs/tools/eval.md | 2026-10-22 | :258 "counted against the session-wide `async.maxJobs` cap (default and maximum 100)" | admit, A, mined |
| S104 | https://github.com/can1357/oh-my-pi/commit/476b858b3a4abe6f6c8a06c252c23961be41e912 | 2026-10-22 | "feat(coding-agent): added async background job execution with configurable concurrency limits" | admit, A, mined |
| S105 | https://github.com/Daxiongmao87/oh-my-pi-termux | 2026-10-22T10:06:29Z | none: 0 occurrences of `maxJobs` or `Background job` | reject, C |
| S106 | https://gist.github.com/sonsu-lee/4d76307bc70d6696c8336855ac292d3e | 2026-10-22T10:06:30Z | none: the config has no `async:` block | reject, C |
| S107 | https://omp.sh/docs/subagents (and settings, tools, slash pages) | 2026-10-22T10:06:31Z | none: 0 occurrences of `maxJobs` on all four pages | reject, C |
| S108 | https://api-docs.deepseek.com/quick_start/agent_integrations/oh_my_pi/ | 2026-10-22T10:06:31Z | none: 0 occurrences of `maxJobs`; a search summary claimed otherwise | reject, C |
| S109 | https://blog.csdn.net/gitblog_01054/article/details/164872117 | 2026-10-22T10:06:33Z | none: HTTP 521 on four attempts, no body | reject, C (unopened) |
| S110 | https://github.com/can1357/oh-my-pi/issues/14636 | 2026-10-22T10:06:34Z | issue prose pairs 15 with 100; the 15 is the undefined-option fallback | reject, C |
| S111 | https://www.gradually.ai/en/changelogs/omp/ | 2026-10-22T10:06:36Z | none: 0 occurrences of `maxJobs` | reject, C |
| S112 | https://raw.githubusercontent.com/can1357/oh-my-pi/v18.12.6/packages/coding-agent/src/tools/bash.ts | 2026-10-22 | :1221-1222 "At the running-job cap, fall through to direct foreground execution instead of failing every bash call" | admit, A, mined |
| S113 | https://raw.githubusercontent.com/can1357/oh-my-pi/v18.12.6/packages/coding-agent/src/tools/eval.ts | 2026-10-22 | :534-535 "At the running-job cap, fall through to direct foreground execution instead of failing every eval call" | admit, A, mined |

Status changes: none to existing rows. New rows enter as listed (S098–S104, S112–S113 `mined`, used by
`corpus/knowledge/harness-job-capacity-r25.md`; S105–S111 `rejected`). Search log: wave-1 SrcRejections screened 18
candidates (1 admitted as S103, 17 rejected; seven of the rejections are recorded as rows).

## Routed round-24 defects (fix or explain)

- D1 fixed: `.ufo/waves/round-25/evidence/pressure-selftest.txt` at `7bb0fe61`.
- D2 fixed in place at `02084f27`: K5, K4 and P3 body lines rewritten, a `(K4)` corrections row added, the
  "this section wins" banner removed; the K3 and P4 rows were corrected in the same edit. Not fixed: two F3
  citation ranges (`psi.c:1538-1550` where the corrections give `1540,1545,1550` plus `1686`).
- D3 fixed: correction line appended to `corpus/lessons/round-24.md`.
- D4 fixed: `.gitignore` line `tools/__pycache__/` (after M2).
- Six surviving pressure mutants: all six are killed at the tip, five only by the supplementary file
  (`.ufo/waves/round-25/w1/SurvivorReplay.md`). The replay found nine more surviving neighbours and added
  supplementary cases S08–S16 that kill them (`ec840f9d`). Open: no committed script runs the supplementary file;
  it is opt-in through `--cases`.

## For round 26

- The three-round sentinel reading: calibration has been claimed through repairs of the previous closure's
  routed defects in rounds 23, 24 and 25 (`.ufo/waves/round-25/w1/CriticSizing.md`). Round 26 should fix routed
  defects as uncounted work and aim its counted claim at a different frontier.
- The SCORECARD Axes table at its top still shows round-1 scores (coverage 5, operability 6, depth 4), while
  every later round holds coverage 6, operability 7, depth 5 (`.ufo/waves/round-25/w1/ReviewLessonR24Counts.md`).
  That is a self-assessment mismatch a calibration claim could count.
