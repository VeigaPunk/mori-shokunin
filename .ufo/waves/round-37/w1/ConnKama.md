# Round 37 connector scan — kama r29 writing-revision claim boundary

**Axes named:** adjacency (cross-lane claim ownership), calibration (kama's claimed axis; checked
only for claim-borrowing), discernment (frontier-overlap check). One bounded move: read kama r29's
report and knowledge entry, then scan every mori round-37 artifact for any sentence asserting
kama-owned writing-revision ground.

## What belongs to kama (r29)

Kama r29 C1 (measured, calibration), fleet report `.ufo/reports/round-29/kama.md`: "self-assessment
statements checked at their writing revision; the 11 base mismatches now carry correction rows with
the counter's observed values." The owned instrument and ground, from
`kama-shokunin/corpus/knowledge/self-assessment-at-writing.md`:

- statement forms (P pointer, H digest, N line-count, C commit, T time, Q quoted-output) extracted
  from lines of `SCORECARD.md`/`SHONEN.md`;
- for each line, the writing revision `W` comes from `git blame --line-porcelain` (S174), and the
  statement is evaluated against the committed tree/history **at `W`**, not the current tip
  (`git merge-base --is-ancestor` S175; `git grep` exclusions S176; `%ct` committer time S177);
- correction rows under `## Round 29 — self-assessment corrections` carry the counter's observed
  values; the entry claims this ground was previously uncovered ("no lane instrument checked
  SCORECARD/SHONEN statements at their writing revision").

A "writing-revision claim that belongs to kama" = any mori r37 sentence asserting that prose
self-assessment statements are extracted and checked at the revision each was written, or claiming
that instrument/ground as mori's own.

## Scan method and observed output

Round surface: `git diff --name-only 842a32074b5c7972e9728f3f629d83eb92f127c2 HEAD` → 42 files
(commits `e57c58b5`…`0a05f7e6`). Every prose-bearing file was read or term-grepped:

1. `git grep -inE 'writing revision|at its writing|self-assessment|statements at|writing-revision'
   HEAD -- corpus .ufo/waves/round-37 SCORECARD.md LOG.md SHONEN.md`
   → hits only in (a) wave JSON machinery quoting **this seat's own prompt**, (b) pre-round-37
   rows (QUALITY ≤ r35, lessons ≤ r35, SCORECARD r25/r29 rows). **Zero round-37 lane-prose hits.**
2. `git diff 842a320..HEAD | grep -inE 'blame|writing|statement|prose claim|self-assess'`
   (wave JSONs excluded) → only: a seat report quoting the fleet `AXES.md:15` calibration
   definition; LOG's held-scores line (below); fetched-source copy text (S222/RFC); code strings.
3. `grep -rinE 'kama|writing[- ]revision|self-assessment|blame|at the writing'
   .ufo/waves/round-37/w1/` → one hit: `CritC1Axis.md:11` quoting the fleet axis definition — a
   quotation, not an assertion, and a seat file in any case.
4. Full reads of the lane-authored r37 prose: `corpus/lessons/round-37.md` (Gate S221–S225, M1–M6,
   debts (a)–(h), misroot), `corpus/knowledge/source-drift-hardening-r37.md` (both policies, arms,
   five limits), fleet `.ufo/reports/round-37/mori.md` (C1/C2, work items, trend verdicts, SHONEN),
   SCORECARD Round-37 declaration/measured-outcome/capability rows (`SCORECARD.md:2035-2071`),
   `corpus/QUALITY.md` 106/107 (`:853-872`), `corpus/README.md` Round-37 rows (`:46`, `:585+`),
   `LOG.md` Round-37 entry (`:2139+`), `corpus/SOURCES.md` S221–S225 teaches cells,
   `.ufo/waves/round-37/contract.md`, and the evidence receipts.

## Closest candidates — ruled out

- **`QUALITY 106`** ("a measurement's discrimination claim is checked against an arm-detector, not
  only against a constant"): mori's counter rejects a memoizer via a run-time-drawn challenge
  **history**; no blame-at-writing-revision of prose statements is involved. Different mechanism,
  mori's own r36-routed lineage (w2/RevNgC2 N1).
- **`contract.md` P-C1/P-C2 "at revision R"**: predicates about a *tool's printed output* at a
  measured revision, not self-assessment prose at its writing revision.
- **`LOG.md:2179`** "Held (self-assessment carried in SCORECARD, not measured by any r37 counter)":
  the explicit opposite of claiming kama's ground — mori disclaims measuring its self-assessment
  statements this round.
- **Committed-bytes-at-named-revision practice**: mori's own QUALITY 78 (round 26) predates kama r29
  and cites mori's lineage, not kama's.
- **`CritC1Axis.md:11`** quotes the fleet `AXES.md` calibration definition ("SHONEN.md/SCORECARD
  entries match observed repo state"); a shared axis definition, not a mori claim to kama's
  instrument, and not lane-authored prose.

No mori r37 artifact mentions kama at all (hit set above is exhaustive for the round surface).

## Contested sentences

**None.** No mori round-37 lesson, knowledge entry, report prose, SCORECARD/QUALITY/README/LOG
row, contract sentence, receipt, or landed seat report asserts a writing-revision claim that
belongs to kama.

**Installs:** none (no tools installed or upgraded; python3 + git only).
**Tooling note:** pacman untouched per the orchestrator pause; no installs required.

VERDICT: PASS
