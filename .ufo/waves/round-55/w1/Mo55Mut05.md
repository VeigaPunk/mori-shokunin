# Mo55Mut05 — C2 voter-settlement mutation probes (round-55 w1)

Seat: mutation tester, lane mori-shokunin. Scope: C2 entailment-arm settlement only.
Scratch: `/fast/scratch/hyaku/mori-r55/Mo55Mut05` (removed at yield; hashes below).
No production edits; lane source read-only throughout. Non-voter seat: this report carries no
vote lines.

## Method

Detector: the frozen counter's own `evaluate()` from
`.ufo/waves/round-55/count-c2.py` (docstring predicate P-C2), driven against the real
committed bytes at the frozen data revision `b8b7064c2b54c8b6b22c288232a96c43fae1af47`:
the 23-row claim table of `corpus/knowledge/disk-runway-enospc-r55.md`, the nine pinned
source copies (all sha256 re-verified against `COPIES` before scoring), and
`corpus/SOURCES.md` rows S535–S543. Only the settlement layer (voter reports under
`.ufo/waves/round-55/w1/` and `.ufo/waves/round-55/w1-results.json`) was synthesized,
exactly the artifacts the twelve `Mo55En*` seats and the orchestrator produce.

Baseline witness: two distinct roster voters (`Mo55En01`, `Mo55En02`), each report
carrying one unfenced `ENTAIL <h> entailed` line per claim hash, each output repeated
verbatim in the results.json entry of the same name. Result: `C2=met … entailed=23
dissent=0` — this is the settlement shape the wave must reproduce to admit C2.

Probe driver: `/fast/scratch/hyaku/mori-r55/Mo55Mut05/probe.py`
(sha256 `1fcb83d8e51a2f7539e1b7dae4174dcb2455448fb9e21a0b39d5c923892ba8f0`).
Claim hashes extracted with the counter's own `--hashes` mode:
`/fast/scratch/hyaku/mori-r55/Mo55Mut05/claim-hashes.txt`
(sha256 `2ef982ba1af86f29af8e35d99964d62aa4f237eca3203e0d3d71a5ad63aeb05b`).

## Probe results (detector = frozen counter)

Verdict column is the counter's own `met` boolean; `expected` is the behavior the frozen
predicate mandates. All 15 probes match.

| probe | expected | counter verdict | evidence line |
|---|---|---|---|
| baseline 2v bound | met | met | `entailed=23 dissent=0` |
| A unbound entailed | unmet | unmet | report lines present, captured outputs say "no vote" → `entailed=0 failed=entailment` |
| A2 report-only binding | unmet | unmet | outputs echo lines but reports have none → `entailed=0 failed=entailment` |
| B overclaim unechoed | unmet | unmet | one `… overclaim` line in a report, not in output → `dissent=1`, `entailed=22`, `failed=entailment` |
| B2 overclaim echoed | unmet | unmet | overclaim also echoed in captured output → identical `dissent=1` |
| C dup result entries | unmet | unmet | one distinct voter, results.json lists that name twice → still one voter, `entailed=0 failed=entailment` |
| C2 dup lines one report | met | met | same `… entailed` line twice inside one report: set-dedup is harmless; two distinct bound voters still carry every row → `entailed=23` |
| C3 dup+valid mix | met | met | duplicated entry for V1 plus genuine V2 → two distinct voters, `entailed=23` |
| D result-name drift | unmet | unmet | report at `Mo55En01.md`, output under `Mo55En01-report` / `Mo55En01␣` → binding fails, `entailed=0 failed=entailment` |
| D2 missing report | unmet | unmet | results.json echoes lines but the report file is absent from the wave dir → `entailed=0 failed=entailment` |
| E self-authored excluded | unmet | unmet | V1 votes on a row whose text it also authored via `REPLACE <h> :: <text>` → its vote for that row excluded, `entailed=22 failed=entailment` |
| E2 author-vote excluded | unmet | unmet | same exclusion with roles swapped → row left with one valid voter, `entailed=22` |
| F fenced ignored | unmet | unmet | all vote lines inside a ```` ``` ```` fence → `entailed=0 failed=entailment` |
| G unknown hash | unmet | unmet | 23 bound lines naming hash `000000000000` → counts for zero rows, `entailed=0 failed=entailment` |
| H non-roster ignored | met | met | same lines plus an overclaim in `Mo55Conn01.md` (not in frozen VOTERS) → no settlement effect at all, `entailed=23 dissent=0` |

Full driver output: `/fast/scratch/hyaku/mori-r55/Mo55Mut05/probe-run-2.txt`
(sha256 `457ddd9a5d5294cf3abae1bb7c673060c1a195b4e53d584d482f1e2322045c0c`;
first run before two expectation-label fixes: `probe-run-1.txt`, sha256
`251a33fae32cde39399591e3b4fc1b782c90b743f43b8d8d7ae4845345388369`).
Driver exit: `MUT05_PROBE pass=15 fail=0`, shell exit 0.

## Reading of the four assigned cases

1. **Unbound entail** — the arm requires the exact `ENTAIL <h> entailed` string to appear
   in the results.json output of the same voter name. Report-only votes, output-only
   votes, fenced votes and wrong-hash votes all settle to zero (A, A2, F, G). A plausible
   defect here would have let unbound lines count; none observed.
2. **Overclaim** — asymmetric by design: a single unfenced overclaim line in a roster
   voter's report blocks the row from the entailment tally (`dissent += 1`) whether or
   not the orchestrator echoed it (B, B2). No bypass via results.json filtering exists.
3. **Duplicate voter** — settlement counts distinct voter names per hash, not vote
   lines and not result entries. Duplicated results.json entries for one name do not
   inflate (C); duplicated lines inside one report are deduped without penalizing the
   voter (C2); a mix of duplicate and genuine entries settles at the true distinct count
   (C3). The inflation mutant is killed.
4. **Result-name** — binding is exact-name: report filename `<voter>.md` must exist in
   `.ufo/waves/round-55/w1/` and results.json must carry a result whose `name` equals
   that voter exactly, whose `output` repeats the line. Trailing-space or suffixed names
   break the binding (D); a missing report file breaks it (D2); non-roster names are
   outside settlement entirely, including for overclaim (H).

Cross-check against live lane state at the frozen rev:

```
$ python3 .ufo/waves/round-55/count-c2.py b8b7064c2b54c8b6b22c288232a96c43fae1af47
C2=unmet claims=23 located=23 quote_missing=0 bad_rows=0 sources=9 source_rows=ok
  pins=ok provenance=ok entailed=0 dissent=0 rev=b8b7064c…fae1af47 failed=entailment
exit 1
```

matches the assignment's data read (23 located, 0 votes, exit 1). My baseline witness is
therefore the exact settlement shape the twelve `Mo55En*` reports plus results.json must
reproduce: per claim hash, ≥2 distinct frozen-roster voters with unfenced
`… entailed` lines, each line repeated verbatim under the same voter name in
results.json, zero overclaim lines anywhere in roster reports, and no voter voting
`entailed` on text it authored via `REPLACE`.

## Restoration / integrity

All mutations were applied to in-memory fixture dicts only; no lane file was written.
`git status --porcelain` in the lane shows only other seats' wave artifacts
(`SCORECARD.md`, `corpus/QUALITY.md`, lesson files, `.ufo/waves/round-55/w1/`) — none
touched by this seat. Scratch removed after report write per seat spec.

## Findings

- info — C2 settlement arm matches the frozen predicate on all four assigned cases
  (unbound entail, overclaim, duplicate voter, result-name) plus authored-exclusion,
  fence, unknown-hash and roster-scope probes; witness shape for admittance recorded.
  Evidence: this report §Probe results; driver `probe.py` sha256
  `1fcb83d8e51a2f7539e1b7dae4174dcb2455448fb9e21a0b39d5c923892ba8f0`;
  output `probe-run-2.txt` sha256
  `457ddd9a5d5294cf3abae1bb7c673060c1a195b4e53d584d482f1e2322045c0c`.
- info — No coverage gap found in the entailment arm for the assigned mutations; every
  mutant was killed or (C2/C3/H) correctly survived as contract-compliant behavior.
