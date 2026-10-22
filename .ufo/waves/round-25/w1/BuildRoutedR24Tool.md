# BuildRoutedR24Tool — C1 read-only check of the round-24 routed defect items

Seat: `MoriR25.BuildRoutedR24Tool` (executor, wave `mori-r25-w1`).
Surface: `tools/mori-routed-r24.py`.
Sandbox clone: `/fast/scratch/hyaku/mori-r25/wt-routed` (origin = the lane repo, read-only fetch only).
Branches (updated for amendment A5, which added the counted item D5):

* `r25-wt-routed-a5` — **deliverable**: the tool alone on the lane tip `e68855d`, commit
  `5117b5f8529362e0c30fabd39217f93439a4af6f` (one file, +167/-4). **The L1 landed this in the lane at
  `e06d4a0`, byte-identical.**
* `r25-wt-routed-proof-d5` — the tool plus one sandbox-only D5 fix-shape commit `666257c`.
* `r25-wt-routed-final` / `r25-wt-routed-proof` — the A1/A3-only tool (D1..D3) and its three
  sandbox-only fix-shape commits, kept for the record.

No lane commit was made by this seat; nothing in the lane repo was written except this report.

Tooling: no install, no upgrade, no pacman/uv/cargo transaction was needed or run. The tool is Python 3
standard library only (`python3 -V` -> `Python 3.14.8`), so the operator tooling directive was not
triggered.

---

## 1. What was implemented

`tools/mori-routed-r24.py` re-derives the round-24 routed defect items D1..D5 at a committed
revision, per claim contract C1 **as amended by A1, A3 and A5**. One command, one JSON object on stdout:

```
python3 -I -B tools/mori-routed-r24.py --repo <lane> --rev <landed tip>
```

Output schema `mori-routed-r24-v1`: `items: 4`, `held`, `mismatches`, one row per counted item
`{id, held, reasons[], detail}` (D1, D2, D3, D5), plus `hygiene: {id: D4, held, reasons[], detail}`.
Exit `0` only when `mismatches == 0` **and** the hygiene row holds; `1` otherwise; `2` when the repo or
the revision cannot be read.

Read-only discipline, verified by inspection of every git call site in the file:

| call | use |
|---|---|
| `git cat-file blob <rev>:<path>` | read a committed blob (never the working tree) |
| `git cat-file --batch-check` | resolve a rev to a commit id (`<rev>^{commit}`) |
| `git ls-tree <rev> -- <path>` | blob id of `tools/mori-pressure.py`, tree id of `tools/fixtures/mori-pressure` |
| `git ls-tree -r -z <rev>` | list tracked paths (hygiene: `.gitignore` files, bytecode under `tools/`) |
| `git archive --format=tar <rev> -- <paths>` | temporary extract of R's tool + fixtures (only under `--rerun`) |
| `git merge-base --is-ancestor R REV` | R is REV or an ancestor of REV |

No `rev-parse`, no `diff`, no `log`, no `show`, no working-tree read, no git write. The environment is
cleaned (`GIT_CONFIG_GLOBAL=/dev/null`, `GIT_CONFIG_NOSYSTEM=1`, `GIT_OPTIONAL_LOCKS=0`,
`--no-optional-locks`) exactly as in `tools/mori-routed-check.py`. Helper style (`_git_env`, `_git`,
`_git_status`, `_rev_parse`-equivalent, `_blob_bytes`, `_list_paths`, `_emit`, `_cannot_evaluate`,
`GitUnavailable`/`GitError`, `RC_HELD/RC_FAILED/RC_UNAVAILABLE`) is reused from
`/home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-routed-check.py`, which was **read only, never
modified** (its blob at `1888bc6` is unchanged).

The tool writes nothing outside a temporary directory it creates and removes; that directory is used
only by the optional `--rerun` flag.

## 2. The four counted items and the hygiene row (A1 + A3 + A5)

**D1 — stale gate evidence.** `.ufo/waves/round-25/evidence/pressure-selftest.txt` must exist at REV
with five header lines **in this order**: `revision: <40 hex>` (a commit R that is REV or an ancestor of
REV), `command: python3 -I -B tools/mori-pressure.py --selftest`, `tool_blob: <oid>` equal to the blob of
`tools/mori-pressure.py` at R *and* at REV, `fixtures_tree: <oid>` equal to the tree
`tools/fixtures/mori-pressure` at R *and* at REV, `exit: 0`. **A3: the body after the five header lines
must be byte-equal to** `MORI_PRESSURE_SELFTEST: PASS 12/12\nMATCHER: rejected 48/48 corrupted
expectations\n` — not merely contain it; any extra line (a FAIL, a traceback) leaves D1 unheld.
The optional `--rerun` re-executes **R's** tool from a `git archive` extract in a
`tempfile.TemporaryDirectory` and reports `body_byte_equal` in the row detail; it is reported, never
needed for `held`.

**D2 — incomplete correction sweep.** Over `corpus/knowledge/system-pressure-r24.md` with `*`, `_` and
backticks removed, case folded and whitespace runs folded to one space: exactly one heading starting
`## corrections`; headings `## facts` and `## decision table` both present (exact, after normalization);
the decision table has at least as many data rows as at `28b79d3d` (11 there); outside the corrections
section, 0 matches of `refreshed on (each|every) read`, of
`spike[^|.]{0,60}(is|are|can be|may be) invisible` and of `null[^|.]{0,15}means[^|.]{0,15}undefined`;
outside it, both `only when the next` (K5) and `not tracked` (P3) occur; inside it, **one physical line**
contains both `(k4)` and `total`.

**A3 banner clause.** A3 says "D2 also requires the banner gone. Outside the corrections section, 0
matches of `this section wins`". The banner sentence ("Where this section and a later line disagree, this
section wins.") sits at `system-pressure-r24.md:11`, i.e. **inside** the `## Corrections` block (heading
line 8, next heading `## Scope` line 43), so the outside-only form is already satisfied before any fix
and cannot distinguish a fixed entry from an unfixed one on this clause. Seat `MoriR25.D2KnowledgeFix`
confirmed in writing that the sentence is **deleted** from the entry and asked for the strict gate. The
tool therefore gates on the phrase being **absent from the whole normalized entry**, and reports both
`banner_outside_corrections` and `banner_in_whole_entry` in the row detail. This gate is strictly
stronger than the A3 literal text and accepts the sibling's real patch (proved in §5).

**D3 — lesson count drift.** With n = the number of cases in
`tools/fixtures/mori-pressure/supplementary-cases.json` at `4f05dd5a32055e85a9297eb8fc8dfec7dfc4625e`
(7): `corpus/lessons/round-24.md` at REV has **one line** containing `Correction`, `S07`, `PASS 7/7`
**not followed by a digit**, and a 7-40 hex token naming a commit at which that file has n cases. The
token is resolved with `cat-file --batch-check` and the case count at that commit is re-derived, so a
token that names no commit (or a commit with a different count) fails.

**D5 — the SCORECARD `## Axes` table (added by A5).** Held at REV when

* the `## Axes` table at REV has **exactly one row per axis** (coverage, operability, depth,
  freshness, calibration, adjacency) — a missing row and a duplicated row are both red;
* each row's `Score` equals the score **parsed from `SCORECARD.md` lines 1499-1506 at
  `28b79d3d`** (the pinned closure-admitted observed state). The parse is a regex over that line
  range, and it **fails closed**: if it does not yield all six axes (or yields an axis twice with
  different scores), D5 is unheld with a reason rather than silently passing;
* no row whose score differs from its **round-1 value** (coverage 5, operability 6, depth 4,
  freshness 5, calibration 5, adjacency 6) says `round 1` in `Last change`.

The `round 1` test is `round\s+1\b`, so `round 12` and `round 13` — the cells the landed fix
actually writes — do **not** match. A row whose score equals its round-1 value may still say
`round 1`; that is the control case.

**D4 — hygiene row (reported, not counted).** Held when `.gitignore` at REV has a line that is exactly
one of `__pycache__/`, `__pycache__`, `**/__pycache__/`, `tools/__pycache__/`, `*.pyc`, `*.py[cod]`; no
`.gitignore` in the REV tree has a `!` line mentioning `pycache` or `.py`; and no tracked path under
`tools/` contains `__pycache__` or ends `.pyc`.

## 3. Before-state re-derivation

At the round-24 tip `28b79d3d1b76824f0c825aabe6cb6c5dc49961bf` (exit 1):

```
{"held":0,"items":4,"mismatches":4,"schema":"mori-routed-r24-v1","status":"failed"}
D1 False ['evidence_file_missing']
D2 False ['phrase_present_outside_corrections: refreshed on (each|every) read',
          'phrase_present_outside_corrections: spike[^|.]{0,60}(is|are|can be|may be) invisible',
          'phrase_present_outside_corrections: null[^|.]{0,15}means[^|.]{0,15}undefined',
          'phrase_missing_outside_corrections: only when the next',
          'phrase_missing_outside_corrections: not tracked',
          'banner_present_in_entry: this section wins',
          'corrections_section_lacks_k4_total_line']
D3 False ['no_line_with_correction_s07_and_pass_marker']
D5 False ['axis_score_mismatch: coverage 5!=6', 'axis_score_mismatch: operability 6!=7', 'axis_score_mismatch: depth 4!=5']
hygiene False ['no_pycache_ignore_rule']
```

This matches A5's declared before-value exactly: **mismatches 4 of items 4**, D1-D3 and D5 all red,
and D5 red with the three predicted reasons `coverage 5!=6`, `operability 6!=7`, `depth 4!=5` (the
`## Axes` table at `28b79d3d` still carried the round-1 scores 5, 6 and 4 while the closure-admitted
scores are 6, 7 and 5). The hygiene row is red at `28b79d3d` because `.gitignore` there has no
pycache rule; the lane's own `09f55b6` added `tools/__pycache__/`, so hygiene is green from that
commit onward — reported, not counted, exactly as A1/A5 say.

## 4. Each item can flip: the sandbox proof

### 4a. D1-D3 (A1/A3) — sandbox-only fix-shape commits

One commit per fix-shape on `r25-wt-routed-proof` (fake fixes, sandbox only — **never** in the lane):

| sandbox rev | commit | mismatches | held | D1 | D2 | D3 | hygiene |
|---|---|---|---|---|---|---|---|
| `042d75b` | base (A3) | 3 | 0 | red | red | red | green |
| `838c561` | D2 fix shape in the knowledge entry | 2 | 1 | red | **green** | red | green |
| `0b1bad9` | D3 correction line in the lesson | 1 | 2 | red | green | **green** | green |
| `78f2840` | D1 evidence file with revision header | **0** | **3** | **green** | green | green | green |
| `d1096d1` | final A1/A3 tool | 0 | 3 | green | green | green | green |

Revs (full): `042d75bd2be1aa0deeafc282a22ef01de1b0ed39`, `838c561`,
`0b1bad9b78c62aa6b3c5d162704c2c8aa2ae9ef5`, `78f2840`,
`d1096d1df50a6efc6dc199d5f271e03ea5afd3a3`.

The D2 fix shape rewrote the three routed body lines (F4 "refreshed on each read" -> "only when the
next 2-second update is due"; decision-table row 1 "can be invisible" -> "is not represented in the
reported average"; IRQ row "`null` means *undefined*" -> "*not tracked by the kernel*"), deleted the
precedence banner, and added a one-line `(K4)` corrections bullet containing `total`. The D3 fix shape
appended one lesson line carrying `Correction`, `S07`, `PASS 7/7` and the hex token
`4f05dd5a32055e85a9297eb8fc8dfec7dfc4625e`. The D1 fix shape wrote the evidence file with the five
header lines and the exact A3 body.

### 4b. D5 (A5) — sandbox-only fix-shape commit

Branch `r25-wt-routed-proof-d5`, base `efaa157` (the lane tip before the D5-shaped SCORECARD commit
`e68855d`), tool at `fbd5cb6`, fix-shape commit `666257cd3ee962538eb3c3830cfb1878885bd36d`:

```
$ python3 -I -B tools/mori-routed-r24.py --repo . --rev efaa157
items 4 held 3 mismatches 1
  D1 True []   D2 True []   D3 True []
  D5 False ['axis_score_mismatch: coverage 5!=6', 'axis_score_mismatch: operability 6!=7',
            'axis_score_mismatch: depth 4!=5']
 hygiene True

$ python3 -I -B tools/mori-routed-r24.py --repo . --rev 666257cd3ee962538eb3c3830cfb1878885bd36d
items 4 held 4 mismatches 0
  D1 True []   D2 True []   D3 True []   D5 True []
 hygiene True
exit 0
```

The D5 fix shape brought the three stale `## Axes` rows to the closure-admitted scores (coverage
5 -> 6, operability 6 -> 7, depth 4 -> 5) and stamped their `Last change` with the round that moved
them (`round 25 (5 -> 6)` and so on) instead of `round 1`. It is a **sandbox-only** commit; the lane's
own D5 fix is `e68855d`, which the tool also accepts (§5).

## 5. The real lane tip already passes

The sibling seats landed the real fixes while the sandbox proof ran. The lane tip
`e68855d555341fa291eb482343a741bdd9db7100` ("SCORECARD Axes table brought to the closure-admitted
scores with a correction note (C1 item D5)") already satisfies the checker with D5 included, and so does
the current lane tip `26c8485927c4f12f75ce5981fcba091ad4f9b3e2` (which carries the landed tool):

```
$ python3 -I -B tools/mori-routed-r24.py --repo . --rev e68855d
{"held":4,"hygiene":{...,"held":true,"id":"D4","reasons":[]},"items":4,"mismatches":0,
 "rev_commit":"e68855d555341fa291eb482343a741bdd9db7100","rows":[
   {"id":"D1","held":true,"reasons":[],"detail":{...}},
   {"id":"D2","held":true,"reasons":[],"detail":{...}},
   {"id":"D3","held":true,"reasons":[],"detail":{...}},
   {"id":"D5","held":true,"reasons":[],"detail":{"axes_rows":{"adjacency":["6"],"calibration":["5"],
      "coverage":["6"],"depth":["5"],"freshness":["5"],"operability":["7"]},
      "pinned_scores":{"adjacency":6,"calibration":5,"coverage":6,"depth":5,"freshness":5,"operability":7},
      "scorecard_base_rev":"28b79d3d1b76824f0c825aabe6cb6c5dc49961bf","scorecard_path":"SCORECARD.md"}}],
 "schema":"mori-routed-r24-v1","status":"held", ...}
exit 0
```

**`"mismatches": 0` with `"held": 4` of `"items": 4` and the hygiene row held** — the A5 declared
after-value, re-derived by this tool over the lane's own committed bytes. With `--rerun`, the D1 body
is byte-equal to a fresh run of R's own tool:

```
"rerun": {"body_byte_equal": true, "exit": 0, "ran": true,
          "body_sha256": "d767d1b6fd53e45caae8ca430f54f91badc08f89676a4d606bd1e2ac0be16f",
          "stdout_sha256": "d767d1b6fd53e45caae8ca430f54f91badc08f89676a4d606bd1e2ac0be16f"}
```

The lane's evidence file at that tip (committed by `7bb0fe6`) names
`revision: ec840f9df9999bb6f5796c07128db0fec26e7c7e` (an ancestor of the tip — confirmed with
`git merge-base --is-ancestor`), `tool_blob: 5785c5b2…`, `fixtures_tree: c28ccfdf…`, `exit: 0`, and the
exact two-line body.

**Compatibility with the sibling's real patches.** The D2 knowledge patch drafted by
`MoriR25.D2KnowledgeFix` (`/tmp/mori-r25-d2/d2verify.py`, applied to a copy of the pristine lane blob in
a scratch clone, never written to the lane) was run through this tool: `mismatches 0`, D2 green. Their
banner deletion satisfies the strict whole-file gate; their one-line `(K4)` bullet satisfies the
same-physical-line requirement for `(k4)` + `total`. The lane's own D5 SCORECARD commit `e68855d`
satisfies the D5 predicate as implemented.

## 6. Falsification battery (41 cases, all as expected)

A throwaway battery (`/tmp/morifals/falsify.py`, outside the lane) clones the sandbox per case, mutates
one thing, commits, and re-runs the tool against the lane tip `e68855d` (all items green, the
control). **41 OK, 0 FAIL.** Mutants that must stay red, each with the reason the tool gave:

* D1 (10): `exit: 1` -> `exit_line_not_zero`; `revision: 0` -> `revision_line_malformed`; `PASS 12/12` ->
  `PASS 11/12` -> `body_not_byte_equal`; `MATCHER: rejected 47/48` -> `body_not_byte_equal`; an extra body
  line -> `body_not_byte_equal`; a wrong `tool_blob` -> `tool_blob_mismatch_at_revision`; a wrong
  `fixtures_tree` -> `fixtures_tree_mismatch_at_revision`; `python3` without `-I -B` ->
  `command_line_malformed`; the evidence file removed -> `evidence_file_missing`; a `revision:` naming a
  non-ancestor -> `revision_not_rev_or_ancestor`.
* D2 (13): the K5 phrase put back -> `phrase_present_outside_corrections: refreshed on (each|every) read`;
  the K4 phrase put back -> `phrase_present_outside_corrections: spike[^|.]{0,60}(is|are|can be|may be)
  invisible`; the P3 phrase put back -> `phrase_present_outside_corrections:
  null[^|.]{0,15}means[^|.]{0,15}undefined`; the banner put back -> `banner_present_in_entry: this section
  wins`; `## Facts` renamed -> `facts_heading_missing`; `## Decision table` renamed ->
  `decision_table_heading_missing` + `decision_table_rows_fewer_than_base`; a second `## Corrections`
  heading -> `corrections_heading_count_not_one`; `(K4)` renamed -> `corrections_section_lacks_k4_total_line`;
  `total` dropped from the K4 line -> `corrections_section_lacks_k4_total_line`; `only when the next`
  dropped -> `phrase_missing_outside_corrections: only when the next`; `not tracked` dropped ->
  `phrase_missing_outside_corrections: not tracked`; a decision-table row deleted ->
  `decision_table_rows_fewer_than_base`.
* D3 (6): `Correction` dropped -> `no_line_with_correction_s07_and_pass_marker`; `PASS 7/70` (digit after
  the marker) -> `no_line_with_correction_s07_and_pass_marker`; `S07` dropped ->
  `no_line_with_correction_s07_and_pass_marker`; every hex token replaced by a non-existent one ->
  `no_hex_token_naming_a_commit_with_n_cases`; the four elements split across two physical lines ->
  `no_line_with_correction_s07_and_pass_marker`.
* D4 (4): the ignore rule commented out -> `no_pycache_ignore_rule`; a `!tools/*.pyc` negation added ->
  `gitignore_negation_reinstates_bytecode: .gitignore`; a tracked `.pyc` under `tools/` (forced past the
  ignore rule) -> `tracked_bytecode_under_tools`.
* D5 (7, added for A5): a score off by one (`coverage 7`) -> `axis_score_mismatch: coverage 7!=6`; a
  duplicated axis row -> `axis_row_duplicated: depth`; a missing axis row -> `axis_row_missing: freshness`;
  a stale `round 1` on an axis whose score moved (`coverage`, `round 12 (...)` -> `round 1`) ->
  `axis_stale_round_1: coverage`; the `## Axes` section renamed -> `axes_section_missing`; a non-numeric
  score -> `axis_score_not_numeric: adjacency`.

Positive controls that must stay green: the control commit (`mismatches 0`, exit 0), a full-length 40-hex
D3 token, a D5 row whose score equals its round-1 value still saying `round 1`, and the `--rerun` path.

The D5 stale-`round 1` mutant is the reason the `round 1` test is a word-boundary regex: the lane's
landed rows say `round 12 (5 -> 6; ...)` and `round 13 (6 -> 7)`, both of which contain the substring
"round 1" but are not the round-1 marker.

Exit-code behaviour was checked separately: exit 0 when `mismatches == 0` and hygiene holds; exit 1 for a
red item; exit 2 with `"status":"could-not-evaluate"` and `"error":"revision does not resolve to a commit"`
for an unresolvable rev; exit 2 for a non-existent repo directory.

## 7. Deviations, risks and open points

1. **The D2 banner gate is stricter than A3's literal wording** (whole file, not "outside the
   corrections section"), for the reason in §2 and on the sibling's written confirmation. This is the one
   place where the tool is deliberately stricter than the letter of the contract; it accepts the
   sibling's real patch, so it does not block the after-value. If the L1 prefers the literal clause, the
   change is one line (`whole_text` -> `outside_text` in `_check_d2`) and the literal clause is already
   satisfied by the landed fix.
2. **`## facts` / `## decision table` are matched exactly** after normalization, not by prefix. A
   renamed heading is red. The landed fix keeps both headings verbatim, so this holds at the tip.
3. **D2's decision-table row floor is 11**, the count at `28b79d3d`. The landed fix keeps 11 rows
   (verified: `decision_table_data_rows: 11`, `decision_table_data_rows_at_base: 11`). The lane's own
   `02084f2` also swept the K3/P4 rows; this checker does not test those (A3 says so explicitly) and I
   did not add a test for them.
4. **D1's expected body is the literal A3 string** (`PASS 12/12`, `MATCHER: rejected 48/48`), pinned to
   the current frozen case count. If the frozen cases change, the expected body must change with them;
   the `--rerun` flag is the self-checking path for that (it compares the recorded body to a fresh run
   of R's tool rather than to a constant).
5. **`--rerun` re-executes R's tool**, not REV's, and only from the named revision R. That is what A1
   asks for ("re-executes R's tool from a temporary extract"); no code from REV is ever run. The default
   path (no `--rerun`) runs nothing at all.
6. **The tool has no `--selftest`.** A1/A3/A5 do not ask for one; the falsification battery in §6 is
   the equivalent evidence and it lives outside the lane.
7. **D5's `round 1` reading.** A row is stale only when its score differs from its round-1 value
   **and** its `Last change` cell names round 1. `round 12` / `round 13` are not round 1 (word-boundary
   regex), and a row that still carries its round-1 score may say `round 1`. This is the reading A5's
   table describes; the landed `e68855d` fix satisfies it.
8. **D5's pinned scores are parsed, not hardcoded.** The expected per-axis score comes from a regex
   over `SCORECARD.md` lines 1499-1506 at `28b79d3d`; only the round-1 values are the contract's
   literals. The parse fails closed (`pinned_scores_unparseable`) when the line range does not yield all
   six axes, or yields one axis twice with different scores. The row-count guard for the decision table
   (D2) uses the same fail-closed pattern against its base revision.
9. **D5 does not read the round-25 score claim from the lane's own prose.** It reads the `## Axes`
   table and the pinned base lines only, so a self-assessment cannot widen its own target.
10. **Landed by the L1, not by me.** The L1 landed the D1..D5 tool in the lane at `e06d4a0`
    ("routed-r24 check gains counted item D5 (contract A5)"), byte-identical to my sandbox deliverable
    `5117b5f8529362e0c30fabd39217f93439a4af6f` (sha256 of both:
    `cf5ef5815f1118ae3595171edde7f527176fde03480665eb6bbb46921c2969ef`). This seat made no lane
    commit; the only lane write by me is this report. The lane's own D1..D3-only version is
    `e54b644b` (landed earlier in the round).
11. **Residual D2 defects reported, not counted.** The sibling `MoriR25.D2KnowledgeFix` lists four
   remaining body-vs-corrections disagreements (K3 version scope, P4 ENOENT causes, the F3 reader range,
   a missing `[INFERENCE]` on the counter_regressed row). My checker does not test them, per A3, and
   they do not affect the after-value.

## 8. Files and commands

* Delivered: `/fast/scratch/hyaku/mori-r25/wt-routed/tools/mori-routed-r24.py`
  — branch `r25-wt-routed-a5`, commit `5117b5f8529362e0c30fabd39217f93439a4af6f`
  (the D1..D5 tool alone on the lane tip `e68855d`; one file, +167/-4). **The L1 landed it in the
  lane at `e06d4a0`, byte-identical** (sha256 `cf5ef5815f1118ae3595171edde7f527176fde03480665eb6bbb46921c2969ef`).
  The A1/A3-only sandbox version (D1..D3) is `r25-wt-routed-proof` at `d1096d1`; the lane took it at
  `e54b644b`.
* Sandbox proof: `r25-wt-routed-proof-d5` (tool `fbd5cb6` + D5 fix-shape commit
  `666257cd3ee962538eb3c3830cfb1878885bd36d`) and `r25-wt-routed-proof` (A1/A3 proof, §4a).
* Scratch (outside the lane, disposable): `/tmp/morifals/falsify.py` (41-case battery),
  `/tmp/mori-r25-d2/` (the D2 sibling's patch, read only), `/tmp/d2test`, `/tmp/d2lane`, `/tmp/d2lane2`
  (scratch clones used to run the sibling's patch through this tool).
* Report (this file): `.ufo/waves/round-25/w1/BuildRoutedR24Tool.md`.
