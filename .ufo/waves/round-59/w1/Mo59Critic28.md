# Mo59Critic28 — report-contract pre-check (receipt coverage)

Seat: critic, mori-r59-w1. Scope: verify the round-59 report can cite every receipt
this wave must produce; list evidence the frozen claims need that no arm writes.
Read-only; no production edits; no VCS mutation.

## Method (bounded)

1. Read frozen `contract.md`, `count-c1.py`, `count-c2.py` at the working tree
   (= freeze bytes; freeze `60b3a76a`, entering `2b9f0397`).
2. Enumerated all 64 seat items in `w1-spec.json`; extracted each prompt's task
   sentence and grepped all prompts for every receipt keyword
   (`SHONEN|S552|Mistakes|QUALITY|census|selftest|assimilation|quarantine|lesson|…`).
3. Verified artifact existence at freeze via `git cat-file -e`/`ls-tree`
   (read-only): both tools, 13 `fixtures-c1` dirs, 12 `trees-c2` dirs, all 7
   `.ufo` artifacts in `ARTIFACTS`/`DRIFT_SCAN`, fleet `MANIFEST.json` at
   `2807c6ab`.
4. Imported the frozen `count-c2.py` module and ran its own `eval_entry`
   against a scratch materialization of the in-flight landing (working-tree
   entry + `corpus/evidence/sources-r59/` copies + HEAD `corpus/SOURCES.md`).
5. Cross-checked every contract-required receipt against `w1-spec.json` arms
   and the committed `evidence/` receipts.

## What the wave must produce (receipt inventory) and coverage

| Receipt | Producer | Status |
|---|---|---|
| Both tools at frozen sha | pre-landed at freeze (`git cat-file -e` OK) | receipted (`evidence/c1-at-freeze.txt` C1=met; C2 tool arm ok) |
| Tool selftests (REGCHECK 12/0, SETSCAN 10/0) | Executor40 re-runs | receipted `evidence/selftests.txt` |
| Counter selftests (C1 6/0, C2 9/0) | — | receipted `evidence/selftests.txt` (committed); no seat re-runs `--selftest` standalone — minor |
| 13 C1 fixtures UNMET + expect prefixes | Reviewer01, Executor41 | covered |
| 12 C2 hostile trees UNMET | Executor42 (imports eval_entry), plus reviewer attacks | covered |
| C1 real arm (REGISTER_MET + bound map) | Reviewer05 replay | partial — see F3b |
| C2 scan/drift arms (5×OK, r53 FAIL) | Reviewer11, Executor43 | covered |
| C2 entry/rows/pins/tree arms | Scribe47 draft + landed bytes (working tree) | `eval_entry` on landing: `ok=True claims=13 files=6` (verified by me) |
| Do-nothing controls (entering rev) | Executor39 re-runs | receipted `evidence/control-c{1,2}-do-nothing.txt` |
| **Counter runs at the landing revision R** (`C1=met … rev=R`, `C2=met … rev=R`) | **no arm — cannot exist pre-commit** | F3 |
| Census start | — | receipted `evidence/census-start.txt` |
| **Census end (contract:102-105, exit 0 required)** | **no arm — post-commit by construction** | F3 |
| Round-59 lesson (Gate rows) | Scribe48 | brief covers S553–S558 only — F2 |
| SCORECARD round-59 section | Scribe49 | covered (claims+commands+receipt names) |
| LOG.md round-59 entry | Scribe50 | covered (claimed/frozen/controlled/waved) |
| **`## SHONEN` re-file vs `mori-shokunin/SHONEN.md`** | **no arm** | F1 |
| **`## Mistakes` row (S552 unchecked sibling-row sweep)** | **no arm** | F1 |
| **QUALITY criterion (grep registry for DOI/sha before new row)** | **no arm** | F1 |
| Quarantine verdicts → lesson (contract:96-98) | Scout51 hand-checks rows; no brief folds verdicts into a draft | F1-adjacent |
| `Assimilation: none` statement | no arm (contract:95-96 requires the line) | F1-adjacent |
| considerthese ≤1 nomination | Scout53 | covered |
| No-harm review (contract:26) | Reviewer19 | covered |
| w1 seat reports ×64 | all seats (`reportDir`) | covered |

## Findings

### F1 — Routed-defect receipts have no producing arm (report-body coverage gap)

`contract.md:13-16` (round-58 spotcheck routed defects 1–2) obligates the
round-59 report/lesson to carry: (a) a `## SHONEN` assessment re-filed against
`mori-shokunin/SHONEN.md`; (b) an appended S552 reconciliation + a `## Mistakes`
row + a QUALITY criterion (`corpus/lessons/round-58-verifier-spotcheck.md:84-85`
explicit: "Re-file against `mori-shokunin/SHONEN.md` … Record an appended
reconciliation … add a `## Mistakes` row … and a QUALITY criterion to grep the
registry for the DOI/sha before opening a new row").

Grep over all 64 prompts: `SHONEN`=0 hits, `S552`=0, `Mistakes`=0,
`QUALITY`=0, `assimilation`=0, `quarantine`=0. Scribe briefs cover entry (47),
lesson Gate block (48), SCORECARD claims (49), LOG (50) — nothing else.
The reconciliation half-landed already: HEAD `corpus/SOURCES.md` line 340 holds
`| S560 | supersedes S552 — duplicate of S478 … | rejected | … | corpus/lessons/round-59.md |`,
but its `used-by` points at a lesson file whose `## Mistakes` row no seat drafts,
and no arm produces the QUALITY criterion text or the re-filed SHONEN lines.
The SHONEN checklist itself is already staged correctly (4 `[~]` boxes citing
mori `SKILL.md:1211/1178`, `LOG.md`, r59 `evidence/selftests.txt`, the r59
entry's Limits section — all pointers verified resolvable), so a correct
re-file is trivially possible; it is simply unassigned and unverified — the
same failure class that produced the wrong-lane assessment being fixed.

Impacted axes: honesty (unverified report lines), completeness (routed defect
closure unprovable from wave output).

Smallest safe correction: widen Scribe50's brief (report/LOG skeleton) to also
draft the `## SHONEN` re-file lines, the `## Mistakes` row for the S552 sweep,
the QUALITY criterion sentence, and the `Assimilation:`/`Quarantine:` lines
(fed by Scout51); or give one reviewer seat the four SHONEN box lines to verify.

### F2 — Scribe48 brief under-covers the entry's source rows by one

Scribe48: "Gate block for **the six** artifact S-rows (S553-S558)". The landed
entry cites **seven** source lines (S553–S559; frontmatter lines 1-7 include
S559 for the r53 artifact copy) and the registry carries **S560** (the S552
reconciliation, `used-by=corpus/lessons/round-59.md`). All seven rows verify
`mined`/`rejected` with exact `used-by` — the counter is fine — but the lesson
draft as briefed omits S559's Gate row and S560 entirely. The report's Gate
table will under-cite the entry unless the integrator writes outside the draft.

Impacted axes: completeness of the lesson receipt.

Smallest safe correction: re-scope Scribe48's row set to S553–S559 + note S560
already landed (or extend to 8 rows with the reject candidate it already owns).

### F3 — The decisive receipts cannot exist inside the wave; the report must cite pending paths

Frozen targets are `C1=met … rev=R` / `C2=met … rev=R` where R is the
post-landing commit. Executor39 runs counters at entering and freeze only
(correct — R is unknowable at dispatch). `c2-at-freeze.txt` already shows the
honest gap: `C2=unmet … failed=copy_absent:×6,entry_absent,tree` — the landing
(entry, 7 copies under `corpus/evidence/sources-r59/`, SOURCES rows) is
uncommitted working-tree material at dispatch time. Likewise `contract.md:102-105`
requires census "at round end (exit 0 required)" — Executor46's mid-wave
re-derivation cannot be the end receipt. Scribe49's "receipt names" draft must
therefore list named-but-pending closure receipts (e.g.
`evidence/c1-after.txt`, `evidence/c2-after.txt`, `evidence/census-end.txt`);
if it lists only existing files, the report cites nothing for the decisive arms.

**F3b (minor):** Reviewer05 is told to compare the real arm "to the committed
receipt" — no committed receipt holds the raw `verdict=REGISTER_MET`/`bound`
JSON; `evidence/c1-at-freeze.txt` records only counter tokens (`real=ok`). The
comparison is only against the token summary, not the bound map itself.

Impacted axes: honesty (a report that implies receipts exist at wave-close
would be false provenance), falsifiability (closure receipts must be named
before they are produced).

### F4 (minor) — Self-referential provenance inside the landed entry

Entry `verified-at` line asserts "copies sha256-verified equal to the committed
`.ufo` artifacts (counter arm `tree=ok`)" — at freeze that arm is `tree=bad`
(`evidence/c2-at-freeze.txt`); the sentence is true only after the landing
commit lands and the counter re-runs. The frozen predicate never parses it, so
it is cosmetic — but it is a truth claim whose witness does not yet exist.
Low-cost fix at integration: reword to "copies sha256-verified … (counter arm
`tree=ok` at the landing commit)" or produce the tree-equality receipt first.

## No-counterexample confirmations (checked, all clean)

- 13 `fixtures-c1` dirs + 12 `trees-c2` dirs committed at freeze (`git ls-tree`).
- All 7 `.ufo` artifacts (r53–r58 results + r58 settlement) exist at freeze.
- Both tools present at freeze; absent at entering `2b9f0397` (do-nothing honest).
- Fleet `MANIFEST.json` exists at `2807c6ab…`.
- Frozen `eval_entry` (module import, read-only) over the working-tree landing:
  `ok=True, claims=13, files=6` — grammar/frontmatter/rows/pins/spans all pass;
  S553–S559 `used-by` cells exactly `corpus/knowledge/wave-settlement-artifacts-r59.md`;
  no `files:outside` (r53 copy is cited in frontmatter only, never in a claim line).
- SHONEN.md: 4 `[~]` boxes; cited pointers `SKILL.md:1211`, `SKILL.md:1178`,
  `corpus/QUALITY.md:1479` all resolve.
- Every seat prompt in `w1-spec.json` is dispatched; all 64 report to
  `.ufo/waves/round-59/w1/` — report-file receipts producible.

## Verdict

Adversarial finding stands (F1 primary, F2–F4 supporting): the wave covers
every *counter-graded* receipt, but the *report-contract* receipts routed from
the round-58 spotcheck (SHONEN re-file, `## Mistakes` row, QUALITY criterion)
plus the lesson's full S-row set and the closure receipts are un-armed. The
frozen claims themselves are not endangered — the gap is in what the round-59
report can honestly cite without integrator improvisation.
