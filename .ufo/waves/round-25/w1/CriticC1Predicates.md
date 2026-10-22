# CriticC1Predicates — attack on the C1 predicates (round 25, wave 1)

Seat: MoriR25.CriticC1Predicates (critic, leaf). Contract `.ufo/waves/round-25/contract.md` at lane tip
`0099a391eccaf3b6b9910d8d71d4d48ca4ea539f`; base `28b79d3d1b76824f0c825aabe6cb6c5dc49961bf`. I read only git
objects, plus throwaway `/tmp` extracts and sandbox repos, which I removed. I made no lane writes except this file. Tool installs: none.

**Amendment window is open:** `git cat-file -e 0099a391:tools/mori-routed-r24.py` exits 128 (the C1 tool has not landed).

## Summary

| # | Item | Severity | Kind | Can held be true while the defect is not fixed? |
|---|---|---|---|---|
| F1 | D2 | high | fixable defect | yes, four ways demonstrated (paraphrase, heading laundering, deletion, whitespace reflow) |
| F2 | D1 | high | fixable defect | yes: round 25's own gate evidence can repeat D1 exactly and D1 still holds |
| F3 | D1 | medium | fixable (re-derivability) | the closure cannot re-derive D1 without executing a registered gate |
| F4 | D1 | low | tradeoff to declare | holds while the recorded selftest is red |
| F5 | D3 | medium | fixable defect | yes: the correction line can be wrong in its ids, name no revision, or go stale this round |
| F6 | D4 | medium | fixable defect | yes, two demonstrated (negation, nested override); a third (tracked bytecode) follows from git semantics |
| F7 | claim sizing | medium | tradeoff for the judge (fixable now) | C1 reads neither SCORECARD nor SHONEN; D4 is not a mismatch of any statement |
| F8 | wording | low | fixable | "reads git objects only" contradicts D1's execution step |

I could not break D1 with a different tool. The predicate pins the `tools/mori-pressure.py` blob and the
`tools/fixtures/mori-pressure` tree at R and at REV. `_cases_path()` resolves only `script_dir/fixtures/mori-pressure/cases.json`
or `script_dir/../tools/fixtures/mori-pressure/cases.json` (`git show 28b79d3d:tools/mori-pressure.py`, lines 404–413).
Both paths are inside the pinned tree. The tool imports only the standard library (lines 54–65). The selftest output is deterministic:
two runs from a `git archive 28b79d3d tools` extract were byte-identical (`cmp` → `IDENTICAL`). The output was
`MORI_PRESSURE_SELFTEST: PASS 12/12` / `MATCHER: rejected 48/48 corrupted expectations`, exit 0, under Python 3.14.8.

---

## F1 — D2: the absence of three literal phrases is not a correction (high)

**Counterexample (run).** I implemented D2 as the contract states it (`contract.md:20`):
- body = lines outside every section whose heading starts `## Corrections`, with sections ending at the next `## ` heading;
- `\n` → ` `;
- substring search for the three phrases;
- `(K4)` must appear in a Corrections section.

I ran it over `git show 28b79d3d:corpus/knowledge/system-pressure-r24.md` and four mutants (script `d2sim.py`, run with `python3 -I -B`):

```
base (False, ['refreshed on each read', 'a shorter spike between two reads can be invisible', '`null` means *undefined*'])
paraphrase (True, [])
launder_heading (True, [])
delete_rows (True, [])
indent_reflow (True, [])
```

- **paraphrase:** "refreshed on *every* read", "a brief spike between two reads may be invisible", "`null` means undefined"
  (no asterisks), plus `- (K4) see below.` in the corrections section. All three statements are still false, and D2 holds.
- **launder_heading:** rename `## Facts` (line 56) to `## Corrections-era facts` and `## Decision table` (line 162) to
  `## Corrections and decision table`. Every false line is now "inside a Corrections section", so the original text is exempt
  and unchanged. `(K4)` is satisfied by `- (K4) pending.`
- **delete_rows:** delete decision-table rows 1 and 2 (lines 170–171) and the clause at lines 94–95. D2 holds, and the
  table loses its two "does NOT prove" rows. That harms depth while D2 reports a repair.
- **indent_reflow:** `refreshed\n  on each read` folds to `refreshed   on each read` (folding line breaks only does not collapse
  runs of spaces). A double space or a trailing space inside the other two phrases also evades the check.

**Evidence.**
- The false lines at base are `system-pressure-r24.md:94-95`, `:170` and `:171`.
- The corrections section is `:8-42`. It already carries `(K5)` and `(P3)` but no `(K4)` (token census of lines 8–42: K3, K5, K6, P2, P3, P4).
- The corrected wording exists in the round-24 critic's text:
  - `.ufo/waves/round-24/w2/CriticKnowledgeOverclaim.md:94-96`: K4 "counted in `total` and decayed into the averages … may leave `avg10` under the threshold", and row 1 "can stay under the threshold";
  - `:185`: P3 "`null` means not tracked".
  - The K5 correction is already in the entry at `:17`: "recomputed on a read only when the next …".
- The routed text asks to "Fix the body lines in place, with a correction note, and stop relying on a 'this section wins' banner" (`corpus/lessons/round-24-verifier-spotcheck.md:143`).

**Impacted axes:** calibration (a false held), depth (the deletion variant).

**Smallest safe correction (D2 "Held at REV when"):**
1. Normalize the text: fold every whitespace run to one space, remove `*`, `_` and backticks, and lowercase it.
2. Exactly one heading starts `## Corrections`. Its section ends at the next `## ` heading. `## Facts` and `## Decision table` still exist under those exact names.
3. Negatives outside that section, 0 matches each:
   - `(refresh|recomput|updat)\w* (on|at) (each|every) read`
   - `can be invisible`
   - `null means undefined`
4. Positives:
   - the paragraph starting `**F4` contains `only when the next`;
   - the table row starting `| All four files present` exists and contains `under the threshold`;
   - the row starting `| IRQ file carries only` exists and contains `not tracked`;
   - the line in the Corrections section carrying `(K4)` also contains `total`.

## F2 — D1 checks a re-made round-24 run, not the routed practice (high)

**Counterexample.** Suppose round 25 commits its C2 gate evidence for `tools/mori-job-runway.py` as
`MORI_JOB_RUNWAY_SELFTEST: PASS 21/21` alone: no revision line, measured before a later edit of the tool. That is
D1's defect, repeated byte for byte in kind. D1 still holds, because it inspects only
`.ufo/waves/round-25/evidence/pressure-selftest.txt`. The same applies to the supplementary run that SCORECARD cites
(`SCORECARD.md:1521`, "`PASS 7/7`"). Its output (`PASS 7/7` / `MATCHER: rejected 28/28`, observed by me from the base
extract with `--cases tools/fixtures/mori-pressure/supplementary-cases.json`) has no revision-named evidence in the
lane, and D1 does not ask for it.

**Evidence.**
- The routed fix is about future outputs: "Commit future selftest outputs with the measured revision and the full stdout" (`round-24-verifier-spotcheck.md:137`).
- The contract re-creates one past output (`contract.md:19`).
- Round 25 ships a new gate with a selftest after-value (`contract.md:86-88`). At `0099a391` the round-25 tree has no evidence directory yet (`git ls-tree -r --name-only 0099a391 .ufo/waves/round-25/` → contract, wave1-run.json, wave1-spec.json).

**Impacted axes:** calibration (a repaired-defect count while the defect recurs in the same round).

**Smallest safe correction:** generalize D1 to every file under `.ufo/waves/round-25/evidence/` at REV whose bytes contain `_SELFTEST:`. Each such file must:
- begin with three lines: `revision: <40 hex>` (an ancestor R of REV), `tool: <repo path>`, `exit: <n>`;
- have the named tool's blob, and its `tools/fixtures/<stem>` tree when present, identical at R and REV.

Keep `pressure-selftest.txt` as one required member of that set. The set is enumerated by the counting command, so the clause is not universal.

## F3 — D1 is not closure-re-derivable as written (medium)

**Evidence.**
- D1's held condition is defined by executing R's `tools/mori-pressure.py --selftest` (`contract.md:19`).
- `tools/mori-pressure.py` is a registered lane gate (`round-24-verifier-spotcheck.md:15-16`, citing `SKILL.md:641`).
- PROTOCOL says "The integrator verifies a gate's *committed evidence* … it does not execute a sibling's gate" (`/home/vgpnk/Projects/shokunin/PROTOCOL.md:412-417`).
- The round-24 closure accordingly re-measured C1 "independently of `tools/mori-routed-check.py`, which was not executed" (`round-24-verifier-spotcheck.md:42`).

So a closure re-measuring D1 with plain git cannot re-derive the "remaining bytes equal the stdout" clause. The rule requires an after-state "the closure can re-derive with one command over committed bytes" (`.ufo/prompts/mori-round-25.md:343-344`). For D1 that degrades to evidence-verified.

**Impacted axes:** calibration (the strength of the closure's ruling).

**Smallest safe correction:** make held byte-only:
- the remaining bytes equal exactly `MORI_PRESSURE_SELFTEST: PASS 12/12\nMATCHER: rejected 48/48 corrupted expectations\n`, which is the stdout SCORECARD states at `SCORECARD.md:1514`;
- `exit: 0`;
- the tool blob and fixtures tree are identical at R and REV;
- `jq '.cases|length'` of R's `cases.json` is 12.

The tool MAY still re-execute R's gate and add a reason when the run disagrees, but held must be decidable without execution.

## F4 — D1 holds over a red gate (low; declare or forbid)

As written, `exit: 1` followed by `FAIL n/N` lines satisfies D1 whenever the record is honest (`contract.md:19`: "`<n>` equals that run's exit code"). That is defensible: the defect concerns stale evidence, not gate health. But C1 would then count D1 "repaired" while the round-24 C2 gate is red at REV. **Correction:** F3's byte-only form forces `exit: 0`. Otherwise, add one sentence to the contract saying that a held D1 over a red run is reported as such, not as a repair.

## F5 — D3: one matching line, true or not (medium)

**Counterexamples:**
- `Correction: the supplementary file is S01–S06, PASS 7/7`. The ids stay wrong, and the drifted text at `corpus/lessons/round-24.md:79-80` ("(S01–S06)" … "(`PASS 6/6`)") stays in place, while D3 holds.
- `Correction note: SCORECARD says PASS 7/7; the lesson's 6/6 stands` also holds.
- `PASS 7/7` is a substring of `PASS 7/70`.

**Same-round staleness.** The contract has the six round-24 survivors "killed by new supplementary cases" (`contract.md:34-36`). So at REV `supplementary-cases.json` will likely hold more than 7 cases [INFERENCE from that sentence]. A correction reading "the supplementary file holds 7 cases, `PASS 7/7`" with no revision then disagrees with the bytes at REV. That is D3's own defect class, and D3 holds.

**Evidence.**
- n = 7 at `4f05dd5a` (ids S01–S07, from a JSON read of the blob).
- `PASS 7/7` is true there: my run from the `28b79d3d` extract printed `PASS 7/7`, exit 0, and `git diff --stat 4f05dd5a 28b79d3d -- tools` is empty.
- Base: `grep -n -E 'Correction|PASS 7/7'` over the lesson at `28b79d3d` → no lines (exit 1). The only corrections heading is lowercase (`:87`).

**Impacted axes:** calibration.

**Smallest safe correction:** the line must match all of:
- `Correction`;
- `\bS07\b` (or `S01–S07`);
- `PASS 7/7(?!\d)`;
- a 7–40 hex token that resolves (`git rev-parse --verify <tok>^{commit}`) to a commit where `supplementary-cases.json` has 7 cases.

## F6 — D4: a matching line is not "ignored" (medium)

**Counterexamples.** The first three rows are sandbox git repos in `/tmp`; the tracked-bytecode case is reasoned from git semantics, not run.

| Setup | `.gitignore` line D4 accepts | `git status --porcelain --untracked-files=all` |
|---|---|---|
| root `__pycache__/` then `!tools/__pycache__/` | yes | `?? tools/__pycache__/m.cpython-314.pyc` (not ignored) |
| root `__pycache__/`, `tools/.gitignore` = `!__pycache__/` | yes | `?? tools/__pycache__/m.cpython-314.pyc` (not ignored) |
| root `__pycache__/` only (control) | yes | `.gitignore` only (ignored) |

The tracked-bytecode case: if a round-25 commit adds `tools/__pycache__/*.pyc` before the rule, the rule never untracks it. D4 holds with bytecode in the tree. That is worse than the routed state. I did not run this one; the sandbox for it was not built.

**Evidence.**
- D4 is satisfied by line membership alone (`contract.md:22`).
- Today's state: `git status --porcelain --ignored -- tools` → `!! tools/__pycache__/`. That shows the untracked cache is ignored locally, by a rule outside `.gitignore`, which at base has only `.ufo/interactive-sessions/` and `.ufo/worktrees/`.
- `.gitignore` is the only ignore file in the tree at base.
- 212 bytecode paths are already tracked, all under `.ufo/waves/round-20/falsify/SelftestC2/…`. None are under `tools/` (`git ls-tree -r --name-only 28b79d3d | grep -c -E '__pycache__|\.py[cod]$'` → 212; restricted to `^tools/` → 0). A repo-wide "no tracked bytecode" condition would therefore be red forever; scope it to `tools/`.

**Impacted axes:** operability (hygiene), calibration (a false held).

**Smallest safe correction:** keep the line rule, and add both:
- no `.gitignore` blob at REV, at any depth, has a line starting `!` that contains `pycache` or `.py`;
- `git ls-tree -r --name-only REV -- tools` has 0 paths matching `(^|/)__pycache__/|\.py[cod]$`.

## F7 — claim sizing: is this calibration? (medium; tradeoff the judge rules on, fixable now)

**Rule.** "A calibration claim must count mismatches between the lane's self-assessment (SCORECARD/SHONEN) and observed repo state. It cannot be an assertion" (`.ufo/prompts/mori-round-25.md:346-347`).

**What passes.**
- C1 is counted by a command, not asserted (`contract.md:26-31`).
- C1 has one after-value (`mismatches: 0`).
- No universal clause carries the result once F2's enumeration is used.

**What does not.**
- **C1 reads neither SCORECARD nor SHONEN.** Its items are four lane artifacts: an evidence file, a knowledge entry, a lesson and `.gitignore`. `mismatches = 4 − held` measures how much of a repair checklist is done, with before = 4 by construction. The round-24 closure flagged the same gap and admitted it only as a boundary: "That record is the ledger, not SCORECARD or SHONEN … noted here as a boundary" (`round-24-verifier-spotcheck.md:98`). Repeating it makes this a known, not a new, boundary.
- **D4 is not a mismatch of any statement.** The contract frames each item as "a place where a lane-written statement or record disagrees with the committed bytes" (`contract.md:13`). For D4 the lane's statement was true: the round-24 report says "`.scratch/` … and `tools/__pycache__/` are untracked and were left untouched" (fleet `.ufo/reports/round-24/mori.md:130`). An untracked cache is not committed bytes. D4 is hygiene (operability). Counting it inflates the calibration denominator.
- **D1–D3 can be tied to real self-assessments:**
  - **D1:** SCORECARD says the selftest "prints `PASS 12/12`, exit 0, then `MATCHER: rejected 48/48`" (`SCORECARD.md:1514`). The committed evidence it rests on reads only `MORI_PRESSURE_SELFTEST: PASS 12/12` (`git show 28b79d3d:.ufo/waves/round-24/evidence/c2-selftest-after.txt`). That is a SCORECARD-vs-bytes mismatch.
  - **D3:** SCORECARD says `PASS 7/7` (`SCORECARD.md:1521`), while the lesson says `PASS 6/6` (`round-24.md:80`).
  - **D2:** the report's self-assessment is "six knowledge statements, which were corrected before this report" (fleet `.ufo/reports/round-24/mori.md:96`). That is the report, not SCORECARD.

**Smallest safe correction (before the C1 tool lands):**
1. Add a "contradicted self-assessment" column naming `SCORECARD.md:1514` (D1), report `:96` (D2) and `SCORECARD.md:1521` versus the lesson (D3).
2. Have the tool read the SCORECARD rows for D1 and D3 and fail the item when the cited row text changes.
3. Move D4 out of the counted set into an uncounted hygiene guard reported beside C1. That gives `items: 3`, before `mismatches: 3`, after 0.

If the L1 keeps four counted items, the judge may rule C1 a bounded repair checklist rather than a calibration measurement. That is a tradeoff to disclose, not a defect the tool can fix.

## F8 — "reads git objects only" contradicts D1 (low)

`contract.md:14-15` says the tool "reads git objects only (no working tree, no git writes)". D1 writes a temporary extract and executes R's code under the host `python3`; the run here used 3.14.8, and its output depends on that interpreter. **Correction:** "reads git objects, writes only a temporary extract outside the repo, executes R's `tools/mori-pressure.py` under `python3 -I -B`, and records `sys.version` in `reasons[]`". This becomes moot if F3's byte-only form is adopted.

## Commands run (all read-only on the lane)

- `git show 28b79d3d:{.gitignore,corpus/lessons/round-24.md,corpus/knowledge/system-pressure-r24.md,SCORECARD.md,SHONEN.md,tools/mori-pressure.py}`; `git ls-tree` over base and tip; `git diff --stat 4f05dd5a 28b79d3d -- tools corpus/knowledge .gitignore` → empty.
- `git archive 28b79d3d tools | tar -x -C /tmp/critc1.*`. Then, in that extract:
  - `python3 -I -B tools/mori-pressure.py --selftest`, twice → identical, exit 0;
  - `… --selftest --cases tools/fixtures/mori-pressure/supplementary-cases.json` → `PASS 7/7`, `MATCHER: rejected 28/28`, exit 0.
- D2 simulation `d2sim.py` (in that extract) over the base entry and four mutants → output quoted in F1.
- D4 sandbox repos under `/tmp/critc1-d4.*` → output quoted in F6.
- Both `/tmp` directories were removed after this report was written.
