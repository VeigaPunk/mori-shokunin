# Mo60Scribe74 — round-60 lesson skeleton (draft)

Seat: scribe, leaf. Round 60 (mori), wave w1, L1 MoriR60.
Posture: read-only on the lane; no commits, no VCS mutation, no fleet/sibling
writes. All commands below ran with cwd `/home/vgpnk/Projects/shokunin/mori-shokunin`
unless an absolute path is shown. Scratch: `/fast/scratch/hyaku/mori-r60/Mo60Scribe74`
(disk-guard status read first: `/fast/scratch/hyaku` 26% used, 596.6G free).

Deliverable: a complete markdown skeleton for `corpus/lessons/round-60.md`
(Gate / Round-59 absent-set correction / Mistakes / Wave w1 placeholder),
with every factual cell pinned to a command and a line pointer. The lesson was
already landed by the L1 in `398d3225`; this draft is the scribe's verified
version and it records three corrections to that landed text (F2, F3, F4).

---

## Findings

### F1 — The three Gate admissions are real and quoted verbatim; the S564 rejection is recorded with a re-open flip

- S561 `Mo59Critic22` (own-work A), pointer `.ufo/waves/round-59/w1/Mo59Critic22.md`:
  - `:8` `## Counterexample (verified, not inferred)`;
  - `:45-49` defects D1–D5; the D2 quote is `:46`
    `All 10 claims cite the same 6-byte span "lane" @offset 3 … | K1–K10 identical (…:offset:3; …)`.
  - SOURCES row: `corpus/SOURCES.md:341` (child count 337 S-rows at tip `b3c25613`).
- S562 `Mo59Sentinel57` (own-work A), pointer `.ufo/waves/round-59/w1/Mo59Sentinel57.md`:
  - `:20` `### F1 — HIGH — counters execute the repo tool blob even when its sha256 ≠ PIN …`;
  - `:29` `run printed \`selftest=ok\` while \`failed=tool_sha,…\` — the unpinned blob ran.`
  - SOURCES row: `corpus/SOURCES.md:342`.
- S563 `Mo59Critic25` (own-work B), pointer `.ufo/waves/round-59/w1/Mo59Critic25.md`:
  - `:33-36` `A nonzero exit on this file is attributable to any subset of these — the arm does not vary any factor.`;
  - `:37` `## Decisive mutants — both pass the frozen arms`; mutants M1 (filename
    heuristic) and M2 (note nullability) at `:44-45`.
  - SOURCES row: `corpus/SOURCES.md:343`.
- S564 `Mo59Sentinel58` rejected as same-scope duplicate of S562; the re-open flip
  names its distinct F2 construction, which exists at
  `.ufo/waves/round-59/w1/Mo59Sentinel58.md:77`
  (`## F2 — MEDIUM: the negative-control expectations are attacker-controlled committed bytes …`).
  SOURCES row: `corpus/SOURCES.md:344`, status cell `rejected`, lesson pointer
  `corpus/lessons/round-60.md`.

### F2 — The landed Gate dates the attack reports `2026-10-28`; the reports carry no internal date

`grep -c "2026-10-28"` over the four r59 attack reports prints `0` for each.
2026-10-28 is the SOURCES *mined* date (`corpus/SOURCES.md:341-344`), not a
report timestamp. Draft wording below says `(opened 2026-10-28)` so the date is
not read as an in-report date.

Command: `grep -c "2026-10-28" .ufo/waves/round-59/w1/Mo59Critic22.md .ufo/waves/round-59/w1/Mo59Sentinel57.md .ufo/waves/round-59/w1/Mo59Critic25.md .ufo/waves/round-59/w1/Mo59Sentinel58.md`
→ `0`/`0`/`0`/`0`.

### F3 — Mistakes row 1: the SCORECARD correction is complete and counter-enforced; the r59 *report* still carries both dead names

- At entering `ddfb12fb`, `SCORECARD.md` lines 2950–2951 held the dead names
  `c1-entering.txt` / `c2-entering.txt` (2 occurrences in those two lines).
  Command: `git show ddfb12fb:SCORECARD.md | sed -n '2950,2951p' | grep -c "c1-entering.txt\|c2-entering.txt"` → `2`.
- At tip `b3c25613` the same two lines carry the literal marker `r60-correction:`
  and name the real committed pointers (`control-c1-do-nothing.txt` /
  `control-c2-do-nothing.txt`). Commands:
  `grep -n "r60-correction:" SCORECARD.md` → `2950`, `2951`;
  `grep -n "c[12]-entering.txt" SCORECARD.md | grep -v "r60-correction:" | wc -l` → `0`;
  `grep -c "c1-entering.txt" SCORECARD.md` → `1` (only inside the markered line, likewise c2).
- No file was ever committed under the dead names:
  `git log --all --oneline -- .ufo/waves/round-59/evidence/c1-entering.txt .ufo/waves/round-59/evidence/c2-entering.txt` → empty.
- **Conflict with the landed lesson's "r59 report" half of the evidence cell:**
  the fleet report `/home/vgpnk/Projects/shokunin/.ufo/reports/round-59/mori.md:120`
  still reads `` `c1-entering.txt`, `c2-entering.txt` (do-nothing controls) ``.
  It was amended after the lane fix (`56a2beff`, 2026-10-28 07:43:54) without a
  pointer correction. The C1 DEAD-NAME ARM is scoped to `SCORECARD.md` only
  (contract C1; `count-c1.py:42-43` `DEAD_NAMES`/`CORRECTION_MARKER`, scanner
  `dead_uncorrected` `:77-87` reads `SCORECARD` bytes only), and QUALITY 156
  states the limit verbatim: "Not covered: pointers outside `.ufo/`/`corpus/`
  (fleet-repo report paths are resolved by the closure, not this sweep)"
  (`corpus/QUALITY.md:1590-1603`). Recorded below as a named limit, not as a met cell.
- Enforcer evidence, run first-hand:
  `python3 .ufo/waves/round-60/count-c1.py --selftest` → `C1_SELFTEST pass=6 fail=0`, rc 0;
  the arm's selftest cases are `dead_plain` / `dead_corrected` /
  `corrected_names_real` / `corrected_missing_real` at `count-c1.py:251-257`.
- `python3 .ufo/waves/round-60/count-c1.py ddfb12fb0838b4307c445194a844f0c4b1950195 --scratch "$S/enter"`
  → `C1=unmet dead-uncorrected=2 receipts=0/2 absent-set=0/5 lesson=absent rev=ddfb12fb…`,
  rc 1 (byte-equal to `evidence/control-c1-do-nothing.txt`).
- `python3 .ufo/waves/round-60/count-c1.py b3c256138f00c704d5aa56eb0332d74506502ef2 --scratch "$S/tip"`
  → `C1=met dead-uncorrected=0 receipts=2/2 absent-set=5/5 lesson=ok rev=b3c25613…`, rc 0
  (byte-equal to `evidence/c1-at-data.txt`; the receipts arm re-ran both r59
  counters at `7b86704d` in scratch, so `receipts=2/2` is first-hand here).

### F4 — Mistakes row 2: the landing class is real, but the landed "filed (07:41)" timestamp is not observable

Verified commit times (`git show -s --format='%H %ci %s' <rev>`):

| event | commit | time (-03) |
|---|---|---|
| r59 round integration (lesson/LOG/SCORECARD/62 reports) | `bf6c0ad3` | 2026-10-28 03:12:38 |
| fleet r59 report first committed (`.ufo/reports/round-59/mori.md`) | `9e9973ed` | 2026-10-28 03:13:02 |
| r59 data correction (C1/C2 receipts rev) | `7b86704d` | 2026-10-28 03:00:51 |
| **late landing**: `w1-results.json` + 3 seat reports | `f091bd77` | 2026-10-28 07:42:42 |
| fleet r59 report amendment (WAVE-DONE 64/64) | `56a2beff` | 2026-10-28 07:43:54 |

`git show --stat --format='' f091bd77` → `w1-results.json | 392 +`,
`w1/Mo59Executor40.md | 556 +`, `w1/Mo59MutationTester31.md | 111 +`,
`w1/Mo59MutationTester32.md | 5 +-` (1062 insertions).
`git cat-file -e bf6c0ad3:.ufo/waves/round-59/w1-results.json` → absent, so the
results handoff landed only in `f091bd77`. No `07:41` artifact (commit, file
mtime, or log line) was observed; draft wording below uses the four verified
times instead. The substantive claim — the round committed ~4.5 h before the
wave's final handoff was swept, and the fleet report was amended 72 s after
`f091bd77` — holds.

### F5 — Absent-set truth matches the table and the lesson, by `git cat-file -e`

`for r in 7b86704d ddfb12fb b3c25613; do for n in Mo59Executor40 Mo59MutationTester31 Mo59MutationTester32 Mo59Critic29 Mo59Reviewer16; do git cat-file -e "$r:.ufo/waves/round-59/w1/$n.md"; done; done`

- at `7b86704d`: all five **absent**;
- at `ddfb12fb` and tip `b3c25613`: all five **present**.
- `git cat-file -e bf6c0ad3:.ufo/waves/round-59/w1/<name>.md` → present for
  `Mo59MutationTester32`, `Mo59Critic29`, `Mo59Reviewer16`; absent for
  `Mo59Executor40`, `Mo59MutationTester31`. This is exactly the pre-filing vs
  late split the lesson prose describes, and exactly the `late-committed`
  disposition rule of `count-c1.py:198-205` (absence at the r59 *data* rev wins).
- `evidence/r59-absent-set.md` carries the 5-row table; `evidence/r59-c1-met.txt`
  and `r59-c2-met.txt` contain the one-line `C1=met …` / `C2=met …` receipts at
  `rev=7b86704d…`, both `present` at tip.
- Predicate weakness worth knowing for the pending spot-check: `count-c1.py:222-233`
  checks the lesson per name with `name in lt and R59_LANDING[:8] in lt`, i.e.
  one `f091bd77` occurrence anywhere in the file satisfies all five names; it
  does not bind the pointer to each name. The draft below nevertheless states a
  landing pointer per name so the lesson satisfies the claim's intent, not just
  the token check.

### F6 — Gate candidates "considered" are sourced; the merge-package counts are exact

- `merge/mori`: `/home/vgpnk/Projects/shokuknow/merge/mori/MERGE-REPORT.md:5-8`
  — `proposed rows accepted: **136**`, `proposed knowledge entries: **80**`,
  `refused: 0`. Contract: "Assimilation: none (no merge/mori theme fits the
  instrument-hardening claims)" (`contract.md:139-141`). The match/no-match
  ruling is the r60 scout seat's (Mo60Scout83) judgment, not measured here.
- considerthese item exists: `considerthese/2026-10-26.md:1-12`, item 1 names
  the hardcoded `LANE = "/home/vgpnk/…/mori-shokunin"` in `conform.py:69` and
  r48 QUALITY 127. Contract records it as a lesson line, not a claim.
- Registry sweep (QUALITY 155, `corpus/QUALITY.md:1532-1540`):
  `grep -c 'Mo59Critic22\|Mo59Sentinel57\|Mo59Critic25\|Mo59Sentinel58' corpus/SOURCES.md`
  → `4`, and the 4 hits are rows `341-344` (their own rows), so the pre-append
  count was 0 by construction; the rows are fresh admissions, not reconciliations.
- Spot-check is **pending** as of this read: `.ufo/waves/round-60/w1/` contains
  only `Mo60Executor53.md`, `Mo60Executor56.md`, `swarm-registry.json`; no
  closure/spot-check artifact exists yet, and the landed lesson says pending.

### F7 — No lane VCS or production file was touched

Only this file was written (`/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-60/w1/Mo60Scribe74.md`).
`git status --porcelain` at entry showed untracked round-60 wave material only
(`w1/`, `w1.ready*`, `evidence/c1-at-data.txt`). The lane tip at measurement was
`b3c25613`; C1 was re-derived at both `ddfb12fb` and `b3c25613` with named pins.

---

## Draft: `corpus/lessons/round-60.md` (full markdown skeleton)

~~~markdown
author: mori L1 MoriR60 (round 60, hyaku run-11, in-session)
date: 2026-10-28
round: 60
entering: ddfb12fb0838b4307c445194a844f0c4b1950195
freeze: ac496c7cde8cad965079858accae3bedfe4a73f2 (amendments 1-2 pre-data, recorded in contract.md)

# Round 60 — instrument hardening (C1 calibration, C2 depth, C3 operability)

Fresh-start round: the rejected closures of rounds 57–59 and their verifier
spot-checks were read before declaring claims; every claim names a surface a
do-nothing control cannot reach, with control receipts committed pre-data
(`.ufo/waves/round-60/evidence/control-c{1,2,3}-do-nothing.txt`, scored at
the entering revision `ddfb12fb…`).

## Gate

- Candidates considered: the three declared claims (C1 record-receipt
  integrity, C2 hardened entry-claims verifier, C3 counter execution
  boundary); the shokuknow `merge/mori` package (136 rows / 80 entries —
  no theme matches instrument hardening this round; scout ruling on
  `/home/vgpnk/Projects/shokuknow/merge/mori/MERGE-REPORT.md`); the
  considerthese 2026-10-26 absolute-host-path item
  (`considerthese/2026-10-26.md`, item 1 — honored by construction: no r60
  instrument carries an absolute host path; recorded as a lesson line, not a
  claim).
- Admitted (sources opened this round; the r59 attack reports carry no
  internal date, so 2026-10-28 is the SOURCES opening date):
  - S561 — Mo59Critic22 report (own-work A): the four met-flip defect
    classes D1–D5; opened at `.ufo/waves/round-59/w1/Mo59Critic22.md`
    §Counterexample `:8`, defect table `:45-49`, quote `:46` (opened
    2026-10-28): "K1–K10 identical (…:offset:3; …)" — the identical-span
    construction the old grammar scored `met`. Row `corpus/SOURCES.md:341`.
  - S562 — Mo59Sentinel57 report (own-work A): execution/write boundary;
    opened §F1 `:20` (opened 2026-10-28): "the unpinned blob ran" while
    `failed=tool_sha` — pin-as-bookkeeping, not as an execution gate. Row
    `corpus/SOURCES.md:342`.
  - S563 — Mo59Critic25 report (own-work B): drift-arm attribution; opened
    §Decisive mutants `:37`, quote `:33-36` (opened 2026-10-28): "A nonzero
    exit on this file is attributable to any subset of these — the arm does
    not vary any factor." — the confound the H5 control kills. Row
    `corpus/SOURCES.md:343`.
- Rejected:
  - S564 — Mo59Sentinel58 report: REJECTED as a same-scope duplicate of
    S562 (same F1 execution-gate finding; this round used none of its
    constructions); flip: a future round needing its distinct F2
    expect-tamper construction (`.ufo/waves/round-59/w1/Mo59Sentinel58.md:77`)
    re-opens the row. Kept as the taste record. Row `corpus/SOURCES.md:344`
    (status `rejected`), lesson pointer `corpus/lessons/round-60.md`.
- Registry sweep (QUALITY 155): `grep -c 'Mo59Critic22\|Mo59Sentinel57\|Mo59Critic25\|Mo59Sentinel58' corpus/SOURCES.md`
  → 4 at the tip, all four inside their own rows `corpus/SOURCES.md:341-344`;
  the pre-append count was 0, so S561–S564 are fresh own-work rows, not
  reconciliations.
- Spot-check: pending — filed for the round-60 non-author closure
  (≥1 admit: S561; ≥1 reject: S564). No closure artifact exists under
  `.ufo/waves/round-60/w1/` at this filing.

## Round-59 absent-set correction (supersedes round-59)

This section supersedes round-59's absent-at-filing record (routed defect 3
of `corpus/lessons/round-59-verifier-spotcheck.md`). Truth by
`git cat-file -e` at the r59 data revision `7b86704d` and at the round-60
tip (full table: `.ufo/waves/round-60/evidence/r59-absent-set.md`):

- Mo59Critic29 — absent at `7b86704d`; supersedes the round-59 lesson claim
  of absent-at-filing: committed pre-filing in `bf6c0ad3` (2026-10-28
  03:12:38 -03); the lesson's set was wrong, the report's missing set did
  not name it — consistent. Late-committed by the data-rev rule; landing
  pointer `bf6c0ad3` (and `f091bd77` for the round's late sweep).
- Mo59Reviewer16 — absent at `7b86704d`; supersedes the round-59 lesson
  claim of absent-at-filing: committed pre-filing in `bf6c0ad3`.
- Mo59MutationTester32 — absent at `7b86704d`; added `bf6c0ad3`
  (pre-filing), modified post-filing in `f091bd77`; the report's "missing"
  listed it because its modified bytes were uncommitted at filing.
- Mo59Executor40 — absent at `7b86704d`; late: landed post-filing in
  `f091bd77` (07:42:42 -03).
- Mo59MutationTester31 — absent at `7b86704d`; late: landed post-filing in
  `f091bd77`.
- `.ufo/waves/round-59/w1-results.json` — absent at `bf6c0ad3`; landed
  post-filing in `f091bd77` (the WAVE-DONE handoff arrived after the round
  commit; see Mistakes row 2).

## Mistakes

1. class reference-drift · evidence: the r59 report
   (`/home/vgpnk/Projects/shokunin/.ufo/reports/round-59/mori.md:120`,
   amended `56a2beff` 07:43:54) and `SCORECARD.md` (r59 section, lines
   2950–2951 at entering `ddfb12fb…`) cited
   `.ufo/waves/round-59/evidence/c1-entering.txt` and `c2-entering.txt`;
   no file was ever committed under those names
   (`git log --all -- <both paths>` is empty) — the receipts live at
   `control-c1-do-nothing.txt` / `control-c2-do-nothing.txt` (commit
   archaeology: Mo60Revenger96, this round's wave) · captured-by: none —
   no pointer-existence check ran before filing (QUALITY 156 is added this
   round as the retro criterion) · fix: the `r60-correction:` re-pointing in
   `SCORECARD.md:2950-2951`, the count-c1 DEAD-NAME ARM (a committed counter
   that scores uncorrected dead names unmet: `count-c1.py:42-43,77-100`,
   selftest `:251-257`), and QUALITY 156 (`corpus/QUALITY.md:1590`). Named
   limit: the counter scans `SCORECARD.md` only, so the fleet report cell
   above remains uncorrected and is closure work (QUALITY 156 "Not covered"
   sentence), not evidence for `C1=met`.

2. class landing · evidence: `f091bd77` (2026-10-28 07:42:42 -03) committed
   `.ufo/waves/round-59/w1-results.json` and the three late seat files
   (`Mo59Executor40.md`, `Mo59MutationTester31.md`,
   `Mo59MutationTester32.md` diff) after the r59 round commit `bf6c0ad3`
   (03:12:38) and the first fleet report commit `9e9973ed` (03:13:02); the
   round committed before the wave's final handoff was swept (the fleet
   report was amended at `56a2beff`, 07:43:54) · captured-by: none — no
   post-WAVE-DONE tree sweep before the report commit · fix: the round-60
   procedure commits the round only after WAVE-DONE plus one explicit
   `git status --porcelain` sweep of the wave dir, and the Wave w1 settlement
   below records the final post-WAVE-DONE sweep receipt; recorded here so the
   non-author closure can check it (this round's own commits obey it).

## Wave w1

(placeholder — filled after WAVE-DONE integration and the final
post-WAVE-DONE `git status --porcelain` sweep: seat count, role mix, attack
share, dead seats, results handoff, and the sweep receipt.)
~~~

---

## Evidence log (exact commands)

All from `/home/vgpnk/Projects/shokunin/mori-shokunin`, lane tip `b3c25613`;
`S=/fast/scratch/hyaku/mori-r60/Mo60Scribe74`.

```
grep -n "r60-correction:" SCORECARD.md                          → 2950, 2951
grep -n "c[12]-entering.txt" SCORECARD.md | grep -v r60-correction: | wc -l → 0
git show ddfb12fb:SCORECARD.md | sed -n '2950,2951p' | grep -c "c[12]-entering.txt" → 2
git log --all --oneline -- .ufo/waves/round-59/evidence/c1-entering.txt ...  → (empty)
grep -c "c1-entering.txt\|c2-entering.txt" /home/vgpnk/Projects/shokunin/.ufo/reports/round-59/mori.md → c1:1 c2:1 (line 120)
git show -s --format='%H %ci %s' f091bd77 bf6c0ad3 9e9973ed 7b86704d ddfb12fb  (lane + fleet)
git show --stat --format='' f091bd77                            → 4 files, 1062 insertions
git cat-file -e bf6c0ad3:.ufo/waves/round-59/w1-results.json    → absent
*git cat-file -e <rev>:.ufo/waves/round-59/w1/<5 names>.md      → 7b86704d absent ×5; bf6c0ad3 present×3
python3 .ufo/waves/round-60/count-c1.py --selftest              → C1_SELFTEST pass=6 fail=0, rc 0
python3 .ufo/waves/round-60/count-c1.py ddfb12fb… --scratch $S/enter → C1=unmet dead-uncorrected=2 …, rc 1
python3 .ufo/waves/round-60/count-c1.py b3c25613… --scratch $S/tip   → C1=met dead-uncorrected=0 receipts=2/2 absent-set=5/5 lesson=ok, rc 0
grep -c 'Mo59Critic22\|Mo59Sentinel57\|Mo59Critic25\|Mo59Sentinel58' corpus/SOURCES.md → 4 (rows 341-344)
grep -n "^156\.\|^157\." corpus/QUALITY.md                      → 1590, 1605
grep -n "136\|80 entries" /home/vgpnk/Projects/shokuknow/merge/mori/MERGE-REPORT.md → :5,:7
grep -c "2026-10-28" .ufo/waves/round-59/w1/Mo59{Critic22,Sentinel57,Critic25,Sentinel58}.md → 0 ×4
```

## Out of scope / known limits

- The lesson's Gate "no merge/mori theme matches" ruling is the scout seat's
  judgment (Mo60Scout83); I verified the package counts only.
- The fleet report `.ufo/reports/round-59/mori.md:120` still carries both dead
  names; the lane counter does not scan fleet paths (QUALITY 156 says so). I
  did not edit it (fleet write prohibition).
- The landed lesson (`398d3225`) differs from this draft at: Gate date
  parentheticals (F2), Mistakes row 1's report-cell wording (F3), and Mistakes
  row 2's "(07:41)" (F4). The substantive claims are unchanged.
- No claim of C1/C2/C3 met is made by this seat; C1 was re-derived here, C2/C3
  were not re-run.

## Cleanup

Scratch `$S` removed after the runs; nothing under `/tmp` was used as evidence.

Report: .ufo/waves/round-60/w1/Mo60Scribe74.md
