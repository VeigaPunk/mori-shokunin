# Mori round 59 lesson

Round 59, attempt 2 (L1 MoriR59a2). Entering `2b9f03975bfb6e508f35074ac8181ec8bf54e805`;
freeze `ccfd554e` amended pre-data to `60b3a76ad0524c8978cc51922940be1c8c388915`;
data `be7372114ded3075e5f5a15227ffec977df22f7d` + correction `7b86704d7c0754a09958d131b64dbfa2a6d3eaed`.
Motivating route: `corpus/lessons/round-58-verifier-spotcheck.md` `## Routed defects for round 59`.
Attempt-1 leftovers (`.ufo/waves/round-59/count-c{1,2}.py`, selftest 21/24, never frozen or
dispatched) were discarded and replaced; not reused as evidence.

## Mistakes

| Class | Evidence pointer | Captured-by | Fix |
|---|---|---|---|
| instrument | `.ufo/waves/round-59/evidence/c1-at-freeze.txt` records a crash (scratch dir not created) and `fixtures=incomplete` (ls-tree returned full paths, not basenames) when the counters first ran at freeze `ccfd554e` — both corrected pre-data in the freeze amendment `60b3a76a` | QUALITY 154 (predicate/output identity) covers target-token drift; nothing required running the counter once at its own freeze revision before dispatch | freeze amendment before any seat scored; receipts re-captured (`c1-at-freeze.txt`, `c2-at-freeze.txt`) |
| scope | `be737211`: K11 quoted `corpus/evidence/sources-r59/w1-results-r53.json`, a file outside the counter's frozen `ARTIFACTS` map → `files:outside` | the frozen counter itself caught it at the data measure (`files:outside=…r53.json`); the intended pre-commit check (dry-run eval_entry on the drafted entry) was skipped | K11 demoted to a prose note naming S559 (data correction `7b86704d`); `C2=met` at `7b86704d` |
| stale-premise | attempt-1 `.ufo/waves/round-59/count-c2.py` selftest 21/24 (`honest_counts`, `blob_missing_unmet`, `repo_commit_inconsistent_unmet` failing) — the counter was drafted but never frozen, dispatched or self-verified green | none — attempt died before freeze; watchdog `lane-dead-no-report` | discarded; new counters frozen only after selftest + fixture/tree validation passed (`selftests.txt`) |
| taste (registry) | `corpus/lessons/round-58-verifier-spotcheck.md` routed defect 2: S552 re-admitted S478's paper/sha — the sibling-row sweep was never run | none before this round | QUALITY 155 (grep DOI/sha before a new row); reconciliation row S560 rejected-as-new-source; `## Gate` below records it |

## Gate

### Sources opened and gate decisions

- **Admit S553–S557 (tier A, own-work).** Re-opened `.ufo/waves/round-{54..58}/w1-results.json`
  from the lane tree on 2026-10-28; byte-identical copies under `corpus/evidence/sources-r59/`
  (shas on the rows). Located quote (S557, line 5): ` "seats": 64,` (3 words) — each artifact's
  seat total. Rows cite `corpus/knowledge/wave-settlement-artifacts-r59.md`, which binds the
  copies with sha-pinned claims.
- **Admit S558 (tier B, own-work).** Re-opened `.ufo/waves/round-58/evidence/w1-settlement.json`
  on 2026-10-28; copy sha `b259e73c…`. Located quote at byte 89: `mori-wave-settlement-v1`
  (1 token) — the lane-written summary schema token.
- **Admit S559 (tier B, own-work).** Re-opened `.ufo/waves/round-53/w1-results.json` on
  2026-10-28; copy sha `0d644e0f…`. Located quote (line 16):
  ` "report_file": ".ufo/waves/round-53/w1/Mo53Fr01.md"` (2 tokens) — the member key absent from
  r54–r58 members (writer-version drift, recorded not repaired).
- **Reject S560 (reconciliation row).** Round-58 routed defect 2: S552 duplicates S478 (same DOI
  `10.1109/TSC.2026.3698682`, same PDF sha256 `1603404d…`). Row opened 2026-10-28 as the
  append-only reconciliation: status `rejected`, teaches records it is already held as S478; no
  new-source credit. Sweep: `grep -n -e '10.1109/TSC.2026.3698682' -e '1603404d' corpus/SOURCES.md`
  → S262, S478, S552 (now also S560).
- **Non-author spot-check:** pending the independent round-59 closure; the lane's own seats are
  not non-authors.

### Considerthese curation

Opened `considerthese/2026-10-26.md` on 2026-10-28. One still-unimplemented proposal executed
this round — suggestion 2, *follow the unfixed critic flags forward*. Sweep:
`python3 .ufo/waves/round-49/flagged-fixed/count-flagged.py | awk '/verdict=UNFIXED/{print $1}'`
→ 9 ids (C1-F1, C1-F6, C1-F8, C2-F1, JC-D7, V3-J10, V3-J11, RA-F2, RH-F2); per-id
`git grep -F <id> HEAD -- corpus/lessons .ufo/waves ':(exclude).ufo/waves/round-49/' ':(exclude).ufo/waves/round-17/'`
for a `fixed|routed|dropped` disposition line. Dispositions: **C1-F1 routed to round 57**
(`.ufo/waves/round-56/w1/Mo56ScribeConsiderthese.md:112`); **RH-F2 closed by QUALITY 152**
(QUALITY 153 itself records it). The other 7 ids appear only as ledger lists (r56 scribe, r58
Mo58MutationTester39 `:88`) — no disposition yet; carried open to round 60. Suggestions 1
(env/stale pin split — implemented, `tools/mori-pin-check.py`), 3 (evidence-only closure re-runs
— still open, not taken this round) and 4 (status line — adopted by r58 lesson) unchanged.

### Quarantine slice

Re-derived per contract (`.ufo/waves/round-59/assimilation/quarantine-slice`): S244, S262, S268 —
same three rows as round 58, no new mori rows. Verdicts (w1 Mo59Scout51 fresh fetch 2026-10-28,
matching round-58): **S244 unverifiable** — ACM DOI 403 here, arXiv carrier reachable, but the row
carries no locator so no quarantine quote exists to check (staged counterpart S483 grounds the
abstract); **S262 present** — live OpenAlex response byte-equal in title/DOI/inverted-index to the
committed copy `corpus/evidence/sources-r42/S262.oa.json`, quote located at abstract pos 27–39;
**S268 present** — fresh IEEE VOR PDF fetch sha256 `1603404dd25b3a0dff93f2dcb23c75b671d4e2d78da3cce8f461e87ebde6add2`
byte-identical to the S478/S552 pin, eBPF-tracepoint quote located at printed p.3016.

### Assimilation

`merge/mori/` package exists; adoption not in this round's shape — `Assimilation: none`
(quarantine re-check done instead, per the assimilation contract's allowance).

## Wave w1 — integrated findings

64 seats dispatched via `w1.ready` (orchestrator marker 2026-10-28T02:53:55). Mix: reviewer 20,
critic 10, mutation-tester 8, executor 8, scribe 4, scout 4, connector 2, sentinel 2, revenger 4,
simplifier 2 — attack share 40/64 = 62.5%; L1 held the planner seat. **All 64 reports landed
after WAVE-DONE** (`w1-results.json` 64/64 members); the three late seats (Mo59Executor40,
Mo59MutationTester31/32) added no verdict change — MT31's sole survivor (m3) mutates the
counter's own MANIFEST_REV pin (detector-redundancy note, not a committed-bytes attack) and
MT32 killed every C2 counter mutant fail-closed.

**Claim verdicts.** C1 `met` — no met-flip found by any attack seat (Mo59Critic24 pure-function
MANIFEST arm; Mo59Reviewer05/06 replay; Mo59Executor41 13/13 fixtures killed; Mo59Reviewer14
frozen-byte integrity equal end-to-end). C2 `met` at data but **unverified** — verified met-flip
counterexamples: Mo59Critic22 (semantically-empty entry, orphaned `grammar:` reasons, one-row
binding), Mo59Reviewer08 (`grammar:` unrouted in `measure()`), Mo59Critic23 (`line:`≡`offset:`
aliasing, vacuous claim sets), Mo59Critic25 (drift arm accepts any nonzero exit — M1/M2 mutants),
Mo59MutationTester37 (committed-symlink copy survives `eval_entry`, latent).

**Routed instrument-robustness defects (no verdict flip).**
- HIGH: sha pin is advisory at execution — unpinned tool bytes run as the operator with inherited
  env; `root / rel` materialization follows symlinks out of scratch (Mo59Sentinel57/58, both
  demonstrated with throwaway repos). Fix: gate every execution on `tool_ok`, containment-assert
  write targets, minimal subprocess env.
- Fixture `expect.txt` files are attacker-controlled committed bytes; an empty expect neutralizes
  a frozen control (Mo59Sentinel58 F2). Reason-prefix coverage: one emitted reason can satisfy a
  multi-prefix expect (Mo59MutationTester36).
- C1 semantic arms delegate to the same-author tool's own JSON — self-graded (Mo59Critic27).
- C1 was `met` at the freeze revision itself; the real do-nothing control is the *entering*
  revision (Mo59Critic26 provenance class; also Mo59Reviewer18 F-class).
- Selftest-consistency blind spot: mutants survive `--selftest`, killed by `measure`
  (Mo59MutationTester38) — audit tokens attest "whatever executed", not the pinned tool.
- Kill rule under-pins the hostile corpus and registry-row binding is first-hit-wins positional
  (Mo59Reviewer18 F1/F5); census `E03` double-gates the row escape.

**Domain findings.**
- Mo59Reviewer12 (10-artifact survey): r50-a2w1 members carry non-null `note` and null `output`
  64/64, and r53 members carry `report_file` — a second drift class beyond the recorded one.
- Mo59Revenger62: committed r55 member `output` is a non-JSON truncated blob naming a report file
  that was never written (`Mo55Rc14.md` absent) — artifacts record *partial* settlement honestly
  but carry no status/verdict field.
- Mo59Executor46: S552↔S478 duplicate confirmed against committed bytes; S560 reconciliation
  shape correct; census surfaces the overlap as W04 only.
- Mo59Executor43: confirmed the K11 `files:outside` defect and its `7b86704d` fix.
- Mo59Connector55/56: settlement-vocabulary boundary with kumitate held — entry states
  artifact-shape facts only, no orchestration verdict (PROVINCE:119-120, 150/153).
- Mo59Revenger59/60/61: handoff/settlement reverse-engineering; `seats == len(results)` grading
  independent of settlement lifecycle; four channels carry partial-state information.
- Mo59Scout52: tsukuroi P55 mismatch routed to mori as dispatch-mechanism defect — cross-lane
  settlement-schema delta recorded (not adopted into mori's pinned artifact set).

**Lane-side landings.** SHONEN pointers refreshed; QUALITY 155 (registry DOI/sha sweep) added;
flag-ledger executed above; LOG round-59 section; SCORECARD round-59 section.
