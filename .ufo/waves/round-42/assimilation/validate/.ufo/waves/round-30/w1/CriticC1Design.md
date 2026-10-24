# CriticC1Design — round 30 wave 1: pre-data falsification of C1 (depth)

Seat: MoriR30.CriticC1Design (critic, leaf). Read-only in the lane. Scratch: `/fast/scratch/hyaku/mori-r30/CriticC1Design/`
(entering-tip tool copy from `git show 58b61681:tools/mori-oom-killers.py`, per-case input copies). Tool installs: none.
Inputs read: `.ufo/waves/round-30/contract.md` (at a66751b), the three eligible fixture files and `cases-a2-r29.json`,
`tools/mori-oom-killers.py`, `corpus/SOURCES.md`, `SKILL.md`, `corpus/lessons/round-29.md` `## Gate`,
`corpus/lessons/round-29-verifier-spotcheck.md:152-166`, `.ufo/waves/round-29/count-c1.sh:1-40`. No peer report was opened.
`count-c1.sh` does not exist yet (not in the working tree; `git ls-tree -r --name-only HEAD .ufo/waves/round-30/` lists only
`contract.md`, `evidence/census-start.txt`, `rule-text.md`), so every finding attacks the contract text that the counter must implement.

## Verdict

C1 as declared can print `C1=met` with **no invocation-scope content and no verified source** (F1, F2, F3), can print
`C1=unmet` on a correct, convention-following entry (F6, F7, F12, F16), and is **not causally separable from C2** as written
(F10, F11). Each of these can be fixed before data, by amending the contract before `count-c1.sh` lands; none is a tradeoff the judge must reject.

## Findings

| id | sev | contract line | class |
|---|---|---|---|
| F1 | high | :28-36 | met without substance |
| F2 | high | :28-31 | met without substance |
| F3 | high | :37-41, :52-53 | met without substance (sourcing) |
| F4 | medium | :20, :37 | met without substance (freshness of sources) |
| F5 | medium | :37-41 | universal clause not enumerated (25-word cap, word-count label) |
| F6 | medium | :39-41 | unmet on correct entry (quote escaping) |
| F7 | medium | :39 | unmet on correct entry (location syntax, multi-file ids) |
| F8 | medium | :38-40 | ambiguous line selection (admit and reject lines share an id) |
| F9 | medium | :37-40 | SOURCES row and Gate line not tied together |
| F10 | high | :15-19, :35-36 | not separable from C2 (tool at `<rev>`) |
| F11 | medium | :42, :111, :118 | not separable / hygiene counted (R6 rows) |
| F12 | medium | :32 | unmet on correct entry (duplicated case ids) |
| F13 | low | :33-36 | equality semantics unspecified |
| F14 | low | :29-31 | `fields` item syntax unspecified |
| F15 | low | :28 | "one Markdown table" ambiguous |
| F16 | medium | :42 | unmet on correct entry (SKILL tag convention) |
| F17 | medium | :47, :50 | provenance of counter and before-receipt |
| F18 | low | :27 | header lines unchecked for content |

### F1 (high): the 8 rows need not concern invocation scope at all
Contract :28-36 checks only that each row's verdict and `fields` agree with a case and with the tool. Nothing requires the
case to involve more than one invocation, a scope boundary, or a scope field.
Counterexample (run on the entering-tip tool, `python3 -I -B tool.py --inputs <copy>`): eight rows, each with
`fields` = `earlyoom.state="active"`, cases `c19-version-line-only`, `c24-nearmiss-kill-failed-without-colon`,
`c28-oomd-active-quiet`, `c33-differing-thresholds-mem-and-swap`, `a2-04-dryrun-sigterm-send-not-positive`,
`a2-04-dryrun-two-sigterm-sends-counted`, `a2-08-null-journal-active-earlyoom-readable-oomd`,
`a2-10-malformed-action-line-uncounted`. Output: verdict matched expect in 8/8 and `earlyoom.state` was `"active"` in 8/8. All
eight ids are unique to one eligible file. None of them has two earlyoom version lines. Conditions 2 and 3 are met, and conditions 4 and 5 are independent of these rows.
Impacted axes: depth (counted move with no depth), calibration.
Smallest safe correction: each row's `fields` must include `earlyoom.scope_complete` or
`earlyoom.earlier_invocation_send_lines`; and at least 4 rows' cases hold two or more version lines in `earlyoom_journal`
(MESSAGE, leading whitespace stripped, starting `earlyoom `, the C2 :70 rule). Eligible pool is measured below (F12).

### F2 (high): no distinctness, so this need not be a decision table
Contract :28-31 says "at least 8 data rows" but never requires the rows to differ. Counterexample: eight copies of one row
citing `a2-06-active-earlier-invocation-sends-quiet` with `earlyoom.earlier_invocation_send_lines=2` and source `S156`.
That table meets conditions 2-4. The `shape` cell may also be empty, since no condition reads it.
Correction: case ids pairwise distinct; `shape` non-empty and pairwise distinct; rows span at least 2 verdicts.

### F3 (high): sha256, URL and excerpt are self-attested; nothing re-opens the source
Contract :37-41 compares the Gate line with the excerpt file, but both are authored in the lane. The sha256 is only required to be
"64-hex", and the excerpt's line labels are whatever the author writes. Counterexample: `S156.txt` with header
`sha256: 000…0` (64 zeros) and an invented line `120<TAB>earlyoom scopes its log to one invocation`, plus a Gate line quoting
`:120` → met. The uncounted residual at :52-53 covers only whether "shape text describes its case" and whether "each cited
quote supports it". It does not cover re-fetching the URL, recomputing the sha256, or diffing the excerpt against the fetched bytes.
The round-29 verifier did exactly that re-open (`round-29-verifier-spotcheck.md:117-128`), but this contract does not enumerate it.
Correction: add to the residual: "a wave-2 non-author re-fetches every S156+ URL, recomputes sha256 of the full bytes and
diffs each excerpt line against the fetched line of the same number; any mismatch fails C1."

### F4 (medium): "opened this round" is not counted
Contract :20 ("rows opened this round") and the assignment summary ("S156+ opened this round") are only checked as
"id ≥ 156" (:37). Nothing checks that the URL is new or that the access time falls inside round 30. The core invocation-scope sources
are already rowed: `corpus/SOURCES.md` carries earlyoom `v1.9.0/main.c`, `kill.c`, `msg.c`, `README.md`, `MANPAGE.md`,
systemd `v262/man/org.freedesktop.systemd1.xml`, `journalctl.xml`, `systemd.journal-fields.xml`, and
`cf8ebfc…/src/core/service.c` / `unit.c` (`rg -o 'https://raw.githubusercontent.com/(rfjakob/earlyoom|systemd/systemd)/…'`).
Counterexample: S156 re-rows `v1.9.0/main.c` and passes. Round 29's own Gate rejected exactly this case as "duplicate URL"
(`corpus/lessons/round-29.md:63-64`).
Correction: the counter fails any S156+ id whose URL appears in a SOURCES row below S156, and any whose `accessed:` is
earlier than the contract commit time.

### F5 (medium): the 25-word cap and the `(N words)` label are not checked
The bound "at most 25 words, verbatim, counted with `wc -w`" and the Gate format's `(N words)` are not in :37-41.
Round 29's routed R3 was exactly this defect, with labels one too high (`round-29-verifier-spotcheck.md:130,159`). A 60-word quote, or one
labelled "(9 words)" that has 10, is met. Separately, a single-word quote such as `"earlyoom"` is met.
Correction: the counter checks `wc -w` ≤ 25, the label equals the count, and the count is at least 3.

### F6 (medium): quote escaping makes a correct verbatim quote fail
Contract :39-41 requires "a double-quoted string" that is "verbatim" in the excerpt, but defines no escape grammar. The lane's own
admitted S155 Gate quote is `"if (args.dryrun && sig != 0) { warn(\"dryrun, not actually sending any signal\n\"); …"`
(`corpus/lessons/round-29.md:62`). There `\"` is a Markdown-side escape, while `\n` is literal C source. Lane tables also escape
pipes as `\|` (`SKILL.md:716`). An earlyoom version-line source quote (a C format string) carries both `"` and `\n`.
Three possible counter behaviours give three outcomes:
- No unescaping: `\"` is not found in the source, so a correct entry is unmet.
- JSON-style unescaping: `\n` becomes a newline and collapses to a space, so it mismatches the source's literal `\n` and a correct entry is unmet.
- Non-greedy `"…"` matching: the quote is truncated at the first inner `"`, which loosens the check.

Correction: the contract states the grammar. Inside the quoted string only `\"`, `\|` and `\\` are unescaped; everything else is literal.
The counter selftest includes the round-29 S155 admit line.

### F7 (medium): the location syntax excludes the lane's existing Gate shapes
Contract :39 accepts only `` `:L` `` or `` `:L-M` ``. Round 29's admitted S154 line writes `` `journal-def.h:120` "…" (2 words) ``,
with a file prefix inside the backticks and the word count after the quote (`corpus/lessons/round-29.md:57`). A counter anchored on
`` `: `` makes such an entry unmet. One id covering several files (S154 covered five) cannot fit the excerpt header's single
`url:` and `sha256:`, and line numbers from two files collide in one excerpt.
Correction: accept `` `[file]:L(-M)` `` and either position of `(N words)`, and state "one URL per S### id" in the contract.

### F8 (medium): one id can carry both admit and reject Gate lines
Round 29 used the same id for one admit line and several reject lines (S154 at `round-29.md:57-61`, S155 at `:62-65`).
Contract :38-40 says the lesson "holds a Gate line … with an `admit` decision" and the excerpt "names the same sha256 and URL",
but does not say the same as which line. Two outcomes follow:
- A counter that takes the first `| S### |` line fails on a correct entry whose first line is a reject.
- A counter that accepts any admit line but matches the excerpt to any line passes an excerpt of a rejected URL.

Gate lines are also not required to sit under `## Gate`.
Correction: the excerpt URL and sha256 must equal those of an `admit` line under `## Gate` for that id.

### F9 (medium): the SOURCES row is never tied to the Gate line or the excerpt
Contract :37-38 checks only that the row "exists". Counterexample: the SOURCES S156 row describes URL A, while the Gate line and
the excerpt use URL B → met. Correction: the Gate URL must appear in the SOURCES row for the same id.

### F10 (high): C1 reads C2's file, so the separability sentence is false
Contract :19 says "Neither counter reads the other claim's files". But :35-36 runs `tools/mori-oom-killers.py` **at
`<rev>`**, and :18 assigns that file to C2. Counterexample: a C2 residual fix (Judge11-13) that changes the output of
`a2-06-active-earlier-and-current-send-acted` makes C1 unmet even when the C1 entry is perfect.
The tool run is also redundant. C2 :62-63 already requires these three blobs to PASS at `<rev>`. And I measured that at
`58b61681` all 36 eligible cases reproduce verdict, exit, and every `expect.fields` value under typed equality: 0 mismatches,
0 missing paths. So pinning the tool loses nothing.
Correction: run the tool blob at `58b61681` (`git show 58b61681:tools/mori-oom-killers.py`), not at `<rev>`. Alternatively, keep `<rev>` and strike the
separability sentence, reporting C1 as conditional on C2 condition 2.

### F11 (medium): R6 hygiene feeds C1's count and its subject
Routed R6 (second half, :118) puts "the A2a limit for the disputed shape" in the C1 entry **and SKILL**. SKILL rows for it
would naturally contain `Round30` and the entry path, so they satisfy condition 5 (:42). Hygiene declared "never a counted
claim" (:111) then counts. The disputed shape is active, stamp absent or 0, a real send, then a plain restart. Its only frozen cases
will live in C2's `cases-a2-r30.json`, which C1 rows may not cite (:32-33). So the entry's most-disputed invocation-scope
statement goes unchecked and depends on C2's outcome. None of the eligible multi-invocation cases has that shape (F12 table).
Correction: condition 5 rows must each name a table-row case id. R6 text gets its own tag (for example `Round30-R6`) and is excluded.

### F12 (medium): "exactly one of" silently excludes the scope-boundary cases
Contract :32. `cases.json` and `cases-supplementary.json` share 29 ids: 28 have identical content, and
`c21-nearmiss-midline-sigkill` differs in `why` and `inputs`. Only 36 ids are eligible: 3 in `cases.json`, 3 in supplementary
and 30 in `cases-a2.json`. The excluded ids include `c02-scope-boundary-one-microsecond-before`, `c03-scope-boundary-exactly-at`,
`c04-incomplete-scope-with-action` and `c05-incomplete-scope-without-action`. These are the most natural invocation-scope rows, so a correct entry citing them is unmet.
The eligible pool with two or more version lines is **exactly 8**, all in `cases-a2.json`:
`a2-03-group-kill-three-after-earlier-invocation`, the three `a2-06-*`, the three `a2-07-*`, and
`a2-09-removed-unit-two-invocations-mixed-sends`. Of these, only `a2-06-inactive-…` and `a2-09-…` are inactive; none is active with stamp 0 or absent.
Further eligible single-invocation scope cases are `a2-01-*` (3), `a2-05-*` (3) and `c34-escalation-only-incomplete-scope`.
Correction: either allow `<file>#<id>` in the `case` cell when the copies are identical, or state the exclusion in the contract so
DraftEntryC1 does not cite c02-c05.

### F13 (low): equality is unspecified
Contract :33-36 says "equals" without defining it. Python `==` on `json.loads` values gives `true == 1`, `false == 0` and `5 == 5.0`
(I ran it: `True True True`). The tool's own comparator also accepts a numeric string for a number
(`tools/mori-oom-killers.py:654-668`). So `earlyoom.scope_complete=1` passes. Correction: typed comparison, in which a bool equals only a
bool, numbers compare numerically, and strings compare exactly. This costs nothing: 0 typed mismatches at the entering tip (F10 run).

### F14 (low): `fields` item syntax is unspecified
Contract :30 leaves open whether items are backticked, what separates them (comma, `;` or `<br>`), and whether string values
must be quoted. `earlyoom.state=active` is not JSON. Contract :29 also leaves open whether the verdict cell may be backticked. Whichever reading
the counter picks, a reasonable author can miss it. Correction: one example row in the contract, plus a counter selftest on it.

### F15 (low): "one Markdown table" is ambiguous
Contract :28 can be read as exactly one table or at least one. The R6 A2a-limit text, or a sources table, adds a second table, and an
exactly-one counter then goes unmet. Correction: "the first table whose header contains …".

### F16 (medium): condition 5 contradicts SKILL's tag convention
`RoundNN` appears in SKILL.md only in section headings, never in table rows (`SKILL.md:611,644,676,712,720`). `rg -c Round26` gives 2, both
headings. A convention-following `## Round30 — …` section whose rows cite the entry has 0 rows containing `Round30`, so it is
unmet. "The entry's path" is also open to three readings: the full path, the basename (SKILL :720 uses the basename), or a Markdown link. A bare substring
match on `Round30` also hits `Round300`.
Correction: count table rows under a heading starting `## Round30` that contain the entry basename.

### F17 (medium): provenance of the counter and of the before-receipt
Contract :47 runs the counter from a working-tree path, so an uncommitted edit changes the result. "Committed before the entry,
the rows or any excerpt" (:50) is not something the counter checks. At the contract commit `a66751b`, neither `count-c1.sh` nor
`evidence/c1-before.txt` exists, yet :50 cites the receipt. The working-tree `evidence/` holds only `census-start.txt`.
If the counter copies the round-29 pattern, the environment variable `MORI_C1_LANE_REPO` (`.ufo/waves/round-29/count-c1.sh:4`)
silently points `<rev>` at another repository.
Correction: the verifier runs `git show <counter-commit>:.ufo/waves/round-30/count-c1.sh` and checks that the counter commit is an ancestor of the
first commit that adds the entry or any S156+ excerpt. The counter prints the repository it read and ignores the environment override, or refuses it.

### F18 (low): the header lines are checked for presence only
`source:`, `verified-at:` and `recheck:` (:27) may hold anything. In particular, `source:` need not name any S156+ id.
Condition 3 also compares verdict and fields but never the exit code. That is harmless only while the blobs are pinned.
Correction: `source:` names at least one S156+ id cited by the table.

## Universal clauses not enumerated by the counter

- "verifiable technical depth on invocation scope" (assignment summary; contract :23): no scope test on any row (F1).
- "decision table": no distinctness or coverage test (F2).
- "opened this round": no novelty or time-window test (F4).
- "sha256 of the full bytes fetched" and "excerpt verbatim from the source": never re-fetched (F3).
- "at most 25 words, counted with `wc -w`": unchecked (F5).
- "Committed before the entry, the rows or any excerpt" (:50): unchecked by the counter (F17).
- "rows tagged `Round30`" (:15): has no defined tag convention in SKILL (F16).
- Privacy bound on entry content (invented values only): no C1-specific scan. Only the global retention metric is held (:106-109).

## Causal separability from C2

Not separable as written: F10 (C1 runs C2's tool at `<rev>`) and F11 (R6 hygiene puts C2's disputed shape into C1's entry and SKILL count).
With the F10 and F11 corrections, the remaining shared surfaces are `corpus/lessons/round-30.md` and `corpus/SOURCES.md`. Those are append-only and
carry disjoint ids, provided C2 rows no S156+ sources of its own. Otherwise C1 could count C2's rows, so the contract should state that C2 adds no SOURCES rows.

## Ready-to-paste contract amendment (pre-data; L1's decision)

```text
C1 amendments (pre-data, from w1/CriticC1Design.md):
2a. Case ids pairwise distinct; `shape` non-empty and pairwise distinct; rows span >= 2 verdicts.
2b. Each row's `fields` includes `earlyoom.scope_complete` or `earlyoom.earlier_invocation_send_lines`; >= 4 rows cite a
    case whose earlyoom_journal holds >= 2 version lines (MESSAGE, leading whitespace stripped, starting `earlyoom `).
2c. `fields` items are backticked `path=<json>`, separated by `, `; values compared typed (bool only equals bool,
    numbers numerically, strings exactly). The table is the first one whose header contains the five cells.
3a. The tool run uses `git show 58b61681:tools/mori-oom-killers.py`, not the tool at <rev>; exit code compared to expect.exit.
4a. Each S156+ URL appears in no SOURCES row below S156; `accessed:` >= the contract commit time.
4b. The excerpt URL and sha256 equal those of an `admit` line for that id under `## Gate`; the SOURCES row for the id contains that URL.
4c. Quote grammar: located as `` `[file]:L` `` or `` `[file]:L-M` ``, `(N words)` before or after; inside "...", only \" \| \\
    are unescaped; wc -w <= 25 and equal to N.
5a. Count table rows under a heading starting `## Round30` that contain `earlyoom-invocation-scope-r30.md` and name a
    table-row case id; R6 rows are tagged `Round30-R6` and excluded.
Residual (wave-2 non-author): re-fetch every S156+ URL, recompute sha256, diff each excerpt line against the fetched line.
Provenance: run the counter from its commit blob; the counter commit is an ancestor of the first commit adding the entry
or any S156+ excerpt; the counter ignores any repo-path environment override.
Separability: C2 adds no SOURCES rows.
```

## Evidence commands (all run by this seat)

- `git ls-tree -r --name-only HEAD .ufo/waves/round-30/` lists only `contract.md`, `evidence/census-start.txt` and `rule-text.md`.
- Duplicate ids: a Python scan of the four fixture files found 29 ids shared by `cases.json` and `cases-supplementary.json`. Of these, 28 are identical and `c21-…` differs.
  The ids unique to one file number 3, 3, 30 and 24 (r29).
- Multi-invocation pool: a Python scan for at least two `earlyoom ` MESSAGE lines found 8 cases, all in `cases-a2.json`. The ActiveState and stamp values are listed under F12.
- F1 run: the eight trivial rows were run through the entering-tip tool copy with `--inputs`. The verdict matched in 8/8 and `earlyoom.state` was `"active"` in 8/8.
- F10 run: all 36 eligible cases were run through the entering-tip tool copy with `--inputs`. Verdict and exit mismatches: `[]`; missing paths: `[]`; typed-unequal: `0`.
- `python3 -c 'print(True==1, 1==1.0, 0==False)'` printed `True True True`.
