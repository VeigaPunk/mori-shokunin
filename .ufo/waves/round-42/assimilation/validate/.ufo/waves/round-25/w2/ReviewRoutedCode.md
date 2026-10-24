# ReviewRoutedCode: review of `tools/mori-routed-r24.py` (round 25, wave 2)

Seat: `MoriR25.ReviewRoutedCode` (leaf reviewer, read-only). Contract: `.ufo/waves/round-25/contract.md`, amendments A1–A5.
Reviewed file: `tools/mori-routed-r24.py`, blob `ddc7a43d`. Identical at `07a31ae`, `e06d4a0`, `098d1a5`, `90cc042` and `c4e4ff0`. `c4e4ff0` was the lane HEAD at the final run.
The lane HEAD moved three times while I worked (to `098d1a5`, `90cc042`, `c4e4ff0`), through other seats' commits. The only change to a tool input was an appended block at the end of `SCORECARD.md` (lines 1550–1586), which D5 does not read. The other tool-tree change, `tools/fixtures/mori-job-runway/supplementary-cases.json`, is C2's fixture, which no D-item reads.

## Verdict: WEAKENED

- The declared after-values reproduce. `python3 -I -B tools/mori-routed-r24.py --repo <clone> --rev HEAD` prints held 4 of 4, mismatches 0, hygiene held, exit 0 at `c4e4ff0`, `90cc042`, `098d1a5`, `07a31ae` and `e06d4a0`. At `28b79d3d` it prints mismatches 4, hygiene red, exit 1, which matches A5's "before".
- As a falsification instrument it is weaker than the contract states. Eight findings (F1, F2, F3, F6, F7, F8, F9, F13) let a stale or contradicting state read as held. Two (F4, F10) report unevaluable input as a mismatch (exit 1) or crash without JSON. One (F11) accepts a malformed `--rev`. None changes the verdict at the committed tip, because the tip's bytes are consistent. They change what "held" means for some inputs.
- Severity count: 6 Medium, 8 Low, 7 Info.

## Method

- Read the tool in full (951 lines) and contract A1–A5. Matched each predicate to its code.
- Re-derived verdicts from committed bytes with `git cat-file` and `ls-tree` reads only. The lane was not written: `--no-optional-locks` on every git call, and `hash-object` without `-w`.
- Ran the tool in private clones under `/fast/scratch/hyaku/mori-r25/w2-ReviewRoutedCode/`. Each probe is one commit that changes one file on top of `07a31ae`. Results are in `probe-summaries.json` and `tip-runs.json`.
- Caller and definition checks: the `lsp` device is not mounted (`xd://lsp` returned "Mounted devices: ast_edit, debug"). I used the literal grep fallback for call sites and checked the call list by reading the code. Grep output is not semantic proof.
- No omp run, no reads of `~/.omp` transcripts, no config edits, no subagents, no background jobs.

## Findings

Line numbers are for `tools/mori-routed-r24.py` unless another path is given.

### Medium

**F1. D5 reads Score and Last change by position; the header row is never read** (`659`, `660`, `666`, `740`)
- Row parsing takes Score as `cells[1]` and Last change as `cells[-1]`. It never reads the header and never requires the header's cell count. Line 660 only skips rows with fewer than three cells.
- Evidence: probe `pE` gives the operability row a fifth cell, so the real Last-change cell reads `round 1` while Score is 7. Result: held 4 of 4, exit 0. Probe `pF` reorders the header and every row to `Axis | Score | Last change | Evidence pointer`, with `round 1` in the third cell. Result: held 4 of 4, exit 0. Under A5 both must be red.
- Smallest fix: find the Score and Last change columns by header name. Fail closed when a data row's cell count differs from the header's.

**F2. D2 never scans headings for the stale phrases** (`587–593`, `595`)
- Only block bodies enter `outside_lines` and `inside_lines`, so `outside_text` has no heading text. `whole_text` (596) does include headings, but only the banner check uses it.
- Evidence: probe `pB` renames `## Scope` to `## Scope: averages refreshed on each read`, which sits outside the corrections section. Result: held 4 of 4, exit 0. A1 says the check runs "over the entry text".
- Smallest fix: add each non-corrections heading line to `outside_lines`.

**F3. D3 holds on an appended note while the stale claim stays; the lane's text says the two now agree** (`786–799`; `corpus/lessons/round-24.md:79–80` and `:100`; `SCORECARD.md:1550–1586`)
- The predicate asks for a line containing `Correction`, `S07`, `PASS 7/7` and a hex token naming a 7-case commit. It does not ask for the uncorrected `PASS 6/6` to be gone.
- At the tip, lesson line 80 still reads "(`PASS 6/6`)". Line 100 says "lines 79–80 stay as written". The tool holds D3 on line 100 alone (`detail.matching_lines` has one entry).
- Impact: the same held verdict is produced if lines 79–80 were never touched. The appended SCORECARD sentence that the four self-assessments "now agree" (the lesson's `PASS 6/6` against SCORECARD:1521) is not what the bytes show.
- Smallest fix: this needs a contract change, because A1 defines the predicate. Either require that no line without `Correction` contains `PASS 6/6`, or correct lines 79–80 in place. Until then, describe D3 as "a correction line exists".

**F4. Pinned baselines that cannot be read give exit 1, not exit 2** (`570–573`, `698–701`, `761–765`; `main` `911–915`)
- The pinned commits `28b79d3d` and `4f05dd5a` are read through `_blob_bytes`. A missing object returns None and becomes a reason. Only REV is resolved up front.
- Evidence: probe `pN`, a `git clone --depth 1` of the lane tip, gives rc 1 with mismatches 4 and reasons `base_knowledge_entry_unreadable`, `base_scorecard_unreadable` and `supplementary_cases_unreadable`. The contract says exit 2 "when the repo or revision cannot be read". My reading is that a missing pinned baseline is that case.
- Smallest fix: in `main`, after line 915, resolve the three pinned commits with `_resolve_commit`. If any is None, return `_cannot_evaluate` (exit 2).

**F5. A read-only check can write objects into a partial clone** (`185–194`; `_git` `206–222`; `_batch_check` `225–249`)
- `_git_env` does not set `GIT_NO_LAZY_FETCH`. A missing object is fetched from a promisor remote and written into the repository.
- Evidence: a blobless clone of a filter-enabled private copy. One tool run moved missing objects from 524 to 520 and the pack count from 2 to 6. A patched copy with `"GIT_NO_LAZY_FETCH": "1"` added to `_git_env` kept missing objects at 524 (no writes). That patched run exits 1 for the F4 reason, so the two fixes must land together.
- Practical exposure is low, since the lane is not a partial clone. The breach of the "no git writes" rule is real.
- Smallest fix: add `"GIT_NO_LAZY_FETCH": "1"` to `_git_env()`. With F4, map a missing REV-side object to exit 2.

**F6. `--repo` below the repository top level changes results, and D4 fails open** (`259`, `275–277`, `404–406`; `main` `908–909`)
- `ls-tree rev -- path` and `ls-tree -r -z rev -- prefix` treat paths as relative to git's working directory. `-C repo` moves that into the subdirectory. The rerun archive call (`404–406`) uses the same pathspec form; I did not run it separately. `main` only checks `isdir`.
- Evidence at the tip: `--repo <clone>/tools`, and `--repo .` run from inside `tools/`, both give rc 1, with D1 red on `pressure_tool_missing` and `pressure_fixtures_missing`. From the repository root the result is held.
- D4 fails open in the same mode. (a) With a tracked `tools/__pycache__/probe.cpython-314.pyc`, the root run is hygiene-red (`tracked_bytecode_under_tools`) and the subdirectory run is hygiene-held. (b) With a root `.gitignore` line `!tools/__pycache__/`, the root run is red (`gitignore_negation_reinstates_bytecode`) and the subdirectory run is held, because `gitignore_files` is empty and the root file is never scanned.
- Smallest fix: require `git -C repo rev-parse --show-prefix` to print nothing, otherwise `_cannot_evaluate`. Alternatively, add `--full-tree` and `:(top)` pathspecs to those three calls.

### Low

**F7. D5 ignores extra axis rows and a second `## Axes` heading** (`622–637`, `717–742`)
- The first `## Axes` heading wins, with no duplicate check (`626–629`). Only the six axis names are checked; other rows are dropped (`717–722`). A5 says "each row's Score".
- Evidence: probe `pG` puts a second, correct `## Axes` table above the stale one. Result: held 4 of 4. Probe `pH` adds an extra row `coverage-old | 5 | … | round 1`. Result: held 4 of 4.
- Smallest fix: require exactly one `## Axes` heading and exactly six data rows, one per axis. Any other row is a reason.

**F8. D5 accepts Unicode digits and a hyphenated "round-1"** (`731`, `734`, `165`)
- `\d` matches any Unicode decimal digit and `int()` accepts them. `D5_ROUND1_RE` requires whitespace between "round" and "1".
- Evidence: probe `pI` writes operability's Score as `٧` (U+0667). Result: held 4 of 4. Probe `pJ` writes the Last change as `round-1 (6 → 7)`. Result: held 4 of 4.
- Smallest fix: use `[0-9]+` for Score. Match `round[\s-]*1(?![0-9])` for the Last-change phrase.

**F9. D2 folds whitespace line by line, so a stale phrase split by a blank line is missed** (`595–596`)
- Evidence: probe `pC` appends `- Averages are refreshed on each`, then a blank line, then `read by the tool.` Result: held 4 of 4. A1 folds all whitespace runs to one space, so this should be red.
- Smallest fix: use `_normalize("\n".join(lines))` for both `outside_text` and `whole_text`.

**F10. Uncaught exceptions end as a traceback with exit 1 and no JSON** (`411–416`, `734`, `747–749`, `917–924`)
- `main` catches only `GitUnavailable` and `GitError`. The rerun's `tar.extractall` catches only `TypeError`. `int()` at 734 raises `ValueError` on long digit strings. `_count_cases` at 748 catches only `ValueError`.
- Evidence, each with rc 1 and empty stdout. Probe `symlink_rerun`: a committed absolute symlink as R's tool raises `tarfile.AbsoluteLinkError`. Probe `long_score_cell`: a 5000-digit Score raises `ValueError: Exceeds the limit (4300 digits)`. Probe `deep_json_token_commit`: 200,000 `[` characters in a commit named by the lesson raise `RecursionError`.
- Smallest fix: catch `Exception` around the checks in `main` and return `_cannot_evaluate` (exit 2, with JSON).

**F11. A `--rev` containing a newline resolves to its first line** (`229`, `244–248`)
- `_batch_check` zips inputs with output lines and never checks that the counts match.
- Evidence: probe `pO` runs `--rev "HEAD\nzz-not-a-rev"`. Result: rc 0, status held, `rev_commit` equal to HEAD's commit.
- Smallest fix: reject `\n`, `\r` and NUL in `--rev`. Assert `len(out) == len(revs)`.

**F12. D1 adds two misleading reasons when the evidence's revision does not resolve** (`476–479`, `491–494`)
- Evidence: probe `pM` names an unknown 40-hex revision. Reasons: `revision_not_a_commit`, `pressure_tool_missing`, `pressure_fixtures_missing`.
- Smallest fix: skip the two comparisons when `revision is None`.

**F13. The corrections section can hold stale prose under a sub-heading** (`369–387`; contract-level)
- `_section_span` treats everything up to the next heading of level 2 or higher as corrections, sub-headings included.
- Evidence: probe `pK` puts a `### Stale body` block containing "Averages are refreshed on each read." inside `## Corrections`. Result: held 4 of 4.
- Smallest fix: inside the corrections section, allow only bullet and blank lines.

**F14. D5's "pinned observed" values are partly the lane's own declaration** (`tools/mori-routed-r24.py:44`, `140–143`; A5)
- The closure admits numbers only for calibration (5, `corpus/lessons/round-24-verifier-spotcheck.md:68`) and coverage (6, `:88`). For operability, depth, freshness and adjacency it says "unchanged" with no number (`:106–109`). Those four values come from the lane's own round-24 declaration (`SCORECARD.md:1504` at `28b79d3d`, in a section headed "Targets, not results").
- A5's phrase "closure-admitted" overstates this for four of six axes. The appended SCORECARD note at line 1582 discloses it.
- Not a tool defect. For four axes, D5 is a consistency check between two lane records. Smallest fix: say so in the docstring and the output ("consistency with the round-24 declaration"), or get an independent observation.

### Info

- **I1. Dead code and lint.** `GitError` is never raised, because every `_git` call passes `allow_failure=True` (`259`, `278`, `292`, `299`, `404–407`). It is still caught at `912` and `923`. `body_lines` is unused (`449`, reported by pyflakes). ruff 0.17.1 reports E501 at `206` and B905 (zip without `strict=`) at `246`.
- **I2. A4 says the banner gate "reports both counts".** The tool reports two booleans (`607–608`).
- **I3. K4 substring match.** `total` matches as a substring (`614`), so "subtotal" would pass. Established by code reading only.
- **I4. D1 `held` is a text predicate.** `--rerun` (`511–524`) is outside `held`, as A1 says. At the tip the rerun gives `body_byte_equal: true` and exit 0 (verified). Without `--rerun`, a hand-written body with the right header and text passes.
- **I5. D2 phrase lists are literal** (`109–113`). "The averages are recomputed at every read." outside the corrections section gives held 4 of 4 (probe `pD`).
- **I6. The pinned-line parse is correct.** From `SCORECARD.md` lines 1499–1506 at `28b79d3d`, the parse yields exactly coverage 6, operability 7, depth 5, freshness 5, calibration 5 and adjacency 6 (`160–163`, `670–688`). The window also holds the claim table's before-values (lines 1501–1502). They agree with the observed line (1504). Any disagreement fails closed (`683–684`). The round-1 constants (`151–158`) equal the base table's scores (`SCORECARD.md:10–15` at `28b79d3d`).
- **I7. A lane self-record is inaccurate.** The appended SCORECARD text (line 1584) says "D5 checks scores only, not evidence pointers or Last change text". The tool does check the Last-change round-1 phrase (`739–741`). The real weakness is F1. The sentence should be corrected.

## Checked and held

- Tip reproduction at `c4e4ff0`, `90cc042`, `098d1a5`, `07a31ae` and `e06d4a0`: held 4 of 4, mismatches 0, hygiene held, rc 0.
- Base `28b79d3d`: mismatches 4, rc 1. D5 is red on coverage 5≠6, operability 6≠7 and depth 4≠5. Hygiene is red (no `.gitignore` line). D1 is red (no evidence file). D2 has seven reasons. D3 is red.
- The committed before-A5 evidence (`revision: 28b79d3d`, `exit: 1`, mismatches 4) matches a fresh base run.
- Exit codes: held 0; mismatch 1; path is not a directory 2; unresolvable rev 2; path is not a repository 2; missing argument 2 (argparse).
- Fail-closed, by reading and by probes: missing evidence, knowledge entry, lesson, SCORECARD or Axes table; unparseable or conflicting pinned lines; an unparseable pinned JSON; unresolvable tokens; a missing `.gitignore`. Each one is recorded as a reason, not a hold. F4, F10, F11 and F12 are the exceptions.
- D1: header order, exact command, exact `exit`, and body byte-equal (`98–101`, `508`). Tool and fixtures blob and tree equal at R and REV (`476–498`). The rerun at the tip matches.
- D2: one corrections heading; facts and decision-table headings present; 11 rows against a base of 11; K4 and `total` on one line (`612–617`); banner gated on the whole entry (`607–610`). That is stricter than A3, as A4 records.
- D3: n = 7 from `4f05dd5a` (`supplementary_case_count: 7`).
- D4: exact-line rule (`129–136`, `834`), negation scan (`848–853`) and tracked bytecode (`855–863`). All correct when run from the repository root.
- Git discipline: only `cat-file --batch-check`, `cat-file blob`, `ls-tree`, `merge-base --is-ancestor` and `archive` (rerun only). The environment is whitelisted (`185–203`). No index or working-tree read. The only write is the rerun's `TemporaryDirectory` (`411`), removed on exit. Every check receives `rev_commit` (`919–922`), so an option-like rev never reaches argv.

## Residual risk

- D1, D2 and D3 "held" are predicates over text the lane wrote (I4, I5, F3, F13).
- D5 is a consistency check for four axes (F14).
- The round-1 constants (`151–158`) must be kept in step with the base table by hand. The tool does not check them.

## Verification gaps

- No language server. Caller and definition checks used the literal grep fallback, so there is no semantic reference proof.
- Probes were built on `07a31ae`. The tool blob and every input D1–D5 read are unchanged at `c4e4ff0` (diffed by path). The probes were not rebuilt on the newer tip.
- Not run: the other seats' mutation sets; `--rerun` with an invalid `TMPDIR` (the fallback to `/tmp` worked, so there was no failure to report); `git archive` pathspecs under a subdirectory; the promisor fix on git versions other than 2.56.0; a real remote in place of the local filter-enabled copy.
- The exit-2 mapping in F4 is my reading of "cannot be read". The contract does not say that in those words.
- SCORECARD prose beyond the Axes table and lines 1499–1506 was not reviewed.

## Tools and installs

- No installs, upgrades or pacman transactions. Existing tools used: `python3` 3.14.8 (`/usr/bin/python3`), `git` 2.56.0 (`/usr/bin/git`), `ruff` 0.17.1 and `pyflakes` 4.0.3 (`~/.local/bin`, already present). They ran on private copies only.
- Scratch: `/fast/scratch/hyaku/mori-r25/w2-ReviewRoutedCode/` keeps four small JSON summaries (`probe-summaries.json`, `tip-runs.json`, `run-base.json`, `run-tip.json`). The clones are removed.

## Reproduction

```
git clone --no-hardlinks <lane> <scratch>/repo          # private copy only
python3 -I -B tools/mori-routed-r24.py --repo <clone> --rev HEAD
# each probe: clone, change one file, git add -A, git commit, run the tool at that commit
```
