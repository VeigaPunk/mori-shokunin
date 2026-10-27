# Mo52RevC2Counter — review of `.ufo/waves/round-52/count-c2.py` vs round 51 (w1, mori round 52)

Seat: Mo52RevC2Counter (leaf, reviewer). Scope: line-by-line review of the frozen round-52 C2 counter against
`.ufo/waves/round-51/count-c2.py`, focused on `entail_votes()` (VOTERS filter, fence handling, REPLACE parsing,
authorship set), the per-row MIN_VOTES rule, docstring predicate vs code, and the selftest arms guarding each new
rule. Limits, not edits — counters are frozen. Scratch `/fast/scratch/hyaku/mori-r52/Mo52RevC2Counter/` (removed
after the run; all cited output is copied below).

## Frozen-bytes check

- `sha256(.ufo/waves/round-52/count-c2.py)` = `0a9ec2ffdd85dd1a2be13f359ad82c0f45f99b781d73f9bcf3fa098d7f3bb74a`,
  equal to line 3 of `evidence/freeze-sha256.txt` and to the working-tree file. All line numbers below are the
  frozen bytes (515 lines; r51 = 475 lines).

## What changed r51 → r52 (unified diff, reviewed in full)

1. Docstring predicate (r52:5–22) rewritten for the new entry/sources; the entailment clause (r52:15–22) now
   states: ≥2 distinct ENTAILMENT voters, unfenced lines, own report `w1/<voter>.md`, no unfenced
   `ENTAIL <h> overclaim`, author's `entailed` not counted via `REPLACE <old> :: <text>` whose `<text>` hashes to
   `<h>`, voters exactly the frozen VOTERS list, "no other file, no L1 file, no other directory counts".
2. Constants: r51 `L1_PREFIX = "MoriR51"` (r51:38) **removed**; r52 adds `VOTERS = ["Mo52Ent%02d" % i …]`
   (r52:45) and `MIN_VOTES = 2` (r52:46). `ENTRY`/`SRC_DIR`/`ENTAIL_DIR` repointed (r52:42–44). COPIES swapped to
   the five v7.2 overcommit sources (r52:53–64).
3. `REPLACE_RE` added (r52:125): `^\s*REPLACE\s+([0-9a-f]{12})\s+::\s+(.+?)\s*$`. `ENTAIL_RE` unchanged
   (r52:124 = r51:118).
4. `entail_votes()` (r52:128–147, was r51:120–129): iterates the 12 VOTERS instead of "every `.md` not starting
   with L1_PREFIX"; a `present` set from `ls(ENTAIL_DIR)` gates reads (r52:131,134); per-file fence toggle
   ```/~~~ (r52:136–142); votes stored as `(kind, voter)` sets (r52:143–145); REPLACE text hashed into
   `authored[voter]` (r52:146–147).
5. `evaluate()` vote block (r52:236–243): `ok_voters` = entailed voters with `h not in authored.get(who)`
   (r52:239); any overclaim in `v` → `dissent += 1` (r52:240–241, authorship does NOT excuse dissent);
   `elif len(ok_voters) >= MIN_VOTES` (r52:242). Failure condition unchanged from r51: `if dissent or
   entailed != claims` (r52:246–247).
6. Selftest: 12 quotes re-derived from the new copies (r52:339–351); the honest fixture now writes two voter
   files `Mo52Ent01.md` + `Mo52Ent07.md` (r52:379–382); entailment arms rebuilt (r52:462–504), 45 checks total.

## Verification performed (command + output + exit code)

- Reproduction, selftest (run with `TMPDIR=/fast/scratch/.../tmp`):
  `python3 .ufo/waves/round-52/count-c2.py --selftest` → `C2_SELFTEST pass=45 fail=0`, rc=0 — identical to
  `evidence/selftest-c2.txt` (all 45 PASS lines match name-for-name).
- At data rev: `python3 .ufo/waves/round-52/count-c2.py 8524904adb25e44f24d9f25aac7eae909625c18c` →
  `C2=unmet claims=28 located=28 quote_missing=0 bad_rows=0 sources=5 source_rows=ok pins=ok provenance=ok
  entailed=0 dissent=0 rev=8524904… failed=entailment`, exit=1 — byte-identical to `evidence/c2-at-data.txt`.
  `entailed=0` is the correct present-gate result: `git ls-tree --name-only 8524904… .ufo/waves/round-52/w1/`
  prints nothing, rc=0 (no voter reports exist at the data commit).
- At entering rev: same command on `4f266ef2…` → `… claims=0 … pins=bad provenance=bad …
  failed=entry_absent,pins`, exit=1 — byte-identical to `evidence/control-c2-do-nothing.txt`.
- Independent hash check: `printf '%s' "<row 1 claim text>" | sha256sum | cut -c1-12` → `9afaa81505da`, equal to
  `row=1 hash=9afaa81505da` in `evidence/c2-hashes-at-data.txt` (confirms `claim_hash`, r52:120–121, is
  case-sensitive sha256 of the whitespace-collapsed, end-stripped cell).
- Adversarial probes of `entail_votes` (imported the frozen module read-only; single voter file present):
  - 4-space-indented `ENTAIL <h> entailed` → **counted** as a vote.
  - 4-space-indented `REPLACE <h> :: text` → **registered authorship**.
  - `~~~`-fenced ENTAIL → skipped (fence logic works for tildes, r52:138).
  - ENTAIL after an unbalanced ``` fence → silently skipped (whole rest of that voter's file).
  - `ENTAIL <h> entailed-ish` → **counted** (`\b` matches before the hyphen); `entailedish` → not counted.
  - `REPLACE <h> ::text` (no space after `::`) → ignored (no authorship).
  - `REPLACE` with a >12-hex old-hash field → ignored (no authorship).
  - `REPLACE 0123456789ab :: SOME CLAIM TEXT` (row text differs only by case) → authorship registered for the
    **recased** hash (`9e738325235b`), NOT the row hash (`9afaa81505da`): the exclusion does not bind.
  - same voter casting both `entailed` and `overclaim` for h → both stored; `evaluate` takes the dissent branch.

## Docstring predicate vs code (clause-by-clause)

Every non-entailment clause maps 1:1 to code: provenance `has()` over the first 14 non-empty lines (r52:181–190);
header exactly `claim | source | quote` (r52:107); ≥12 rows (r52:190–192); claim ≥6 words (r52:203); uniqueness
case+whitespace folded (r52:204,214); ≥3 beyond-words via `[A-Za-z][A-Za-z0-9_]{2,}` (r52:87–89,216) — an
approximation of "words of 3+ letters" (tokens with digits count), carried unchanged from r51; source cell one
`S\d{3,}` (r52:205) mapped to a SOURCES row with `mined`/`2026-10-26`/URL/used-by (r52:229–233); one 6–25-word
backticked quote with `\|` unescaped (r52:206–211); whitespace-collapsed occurrence in the pinned copy (r52:236
`q in norm[url]`); all-5-sources floor (r52:250–252); sha256 pins (r52:166–171). The entailment clause matches
the code as analyzed above. No divergence found between the frozen predicate sentence and the implementation.
The docstring header (r52:10) says "same sentence in contract.md, this counter and the receipt label": the
receipts record the literal command and the counter's output line only, not the predicate sentence — satisfied in
the weaker sense that the output line is generated by this same counter (LOW wording nit, below).

## Selftest arms vs new rules

- VOTERS filter → `entail_l1_file_ignored_unmet` (MoriR52-notes.md), `entail_non_voter_seat_ignored_unmet`
  (Mo52CritC2.md), `entail_voter_outside_list_ignored_unmet` (Mo52Ent13.md), `entail_non_md_ignored_unmet`
  (Mo52Ent02.txt), `entail_other_dir_ignored_unmet` (round-52/other/), `voters_frozen` (r52:504). All present.
- MIN_VOTES=2 → `entail_no_votes_unmet`, `entail_one_voter_unmet`, `entail_same_voter_twice_unmet`,
  `entail_one_row_single_vote_unmet` (asserts `entailed=11`, proving the rule is per-row). All present.
- Fence handling → `entail_fenced_votes_ignored_unmet`, `entail_fenced_dissent_ignored_met`. Present, but only
  with ``` fences; `~~~` is implemented (r52:138) and untested.
- REPLACE parsing/authorship → `entail_author_vote_not_counted_unmet` (author's entailed drops out, 11 left),
  `entail_author_plus_two_others_met` (a third voter restores the row), `entail_fenced_replace_not_authorship_met`.
  Present and isolating.
- Dissent scope → `entail_dissent_unmet`, `entail_non_voter_dissent_ignored_met`. Present.
- All nine hardened-arm controls named in contract.md §C2 are present and reproduce green.

## Findings

- **MED (limit, docstring-vs-code, route to round 53)** — "no L1 file" is unenforceable. r51 skipped files whose
  name started with `MoriR51` (r51:38,124–126); r52 deleted `L1_PREFIX` and keys voter identity purely on
  filename membership in the frozen VOTERS list (r52:45,128–134). The docstring still claims "no L1 file …
  counts" (r52:21–22), but any seat — including the L1 planner — writing `.ufo/waves/round-52/w1/Mo52Ent01.md`
  would be counted as voter Mo52Ent01; the counter cannot detect it. The clause is true only by harness
  convention (each seat writes only its own report). A round-53 counter could bind voter identity to the commit
  author or a per-seat salt; not fixable in this round's frozen bytes.
- **MED (limit)** — "unfenced" is implemented only as a ```/~~~ toggle (r52:136–142), which diverges from a
  Markdown renderer in both directions: (a) 4-space-indented code blocks are not recognized — an ENTAIL or
  REPLACE line inside one **counts** (probe evidence above), so a voter quoting example syntax in an indented
  block can accidentally vote or self-declare authorship; (b) any line starting with 3+ backticks/tildes toggles
  regardless of CommonMark closer rules, so one unbalanced fence silently discards the rest of that voter's
  report (probe: all later votes lost). Fence state is correctly per-file, so the blast radius is one voter.
  Practical instruction for this wave: ENTAIL/REPLACE lines at column 0, never inside ```/~~~ and never indented.
- **LOW (limit)** — vote kind is a prefix match: `ENTAIL <h> entailed-ish` counts as `entailed` (r52:124 `\b`
  matches before a non-word char); only a joined token (`entailedish`) is rejected. Matches r51 and the seat
  instruction ("lines that start with"), but prose after the kind is not part of the vote.
- **LOW (limit)** — the REPLACE old-hash field is captured and never used (r52:125,146–147): authorship is
  defined solely by `<text>` hashing to the row hash, exactly as the docstring states, so a REPLACE with a wrong
  or foreign old hash still registers authorship of the new text. Conversely, because `claim_hash` is
  case-sensitive (r52:120–121) while table uniqueness is case-folded (r52:214), a voter who reprints the row text
  with different case in a REPLACE line is NOT excluded (probe: authorship lands on the recased hash) — the
  authorship exclusion is dodgeable by the very voter it targets. Self-defeating in practice (it is the voter's
  own report), but it bounds what the arm proves; already covered by the named limit "a REPLACE line is the only
  authorship signal the arm reads".
- **LOW (limit)** — REPLACE syntax is strict: `REPLACE <h> ::text` without the spaced `::`, or with an old-hash
  field longer/shorter than 12 hex, registers nothing (probes). Voters must emit the exact frozen line format.
- **LOW (limit)** — dissent binds only to the current row hash: an `ENTAIL <h> overclaim` against a stale hash
  (text later replaced, or a full 40-hex sha) is invisible, and the row can pass on two fresh entailed votes.
  This is the docstring's own `<h>` definition and the kill rule's intended REPLACE flow (new hash ⇒ old votes
  and old dissents stop binding; votes never deleted), not a bug — but dissent has no persistence across a
  replacement. Also note `dissent` counts only the 12 voters' overclaims (probe + `entail_non_voter_dissent_
  ignored_met`), per the frozen "voters are exactly the list" rule.
- **LOW (selftest gaps, evidence limits)** — no arm for `~~~` fences (implemented, r52:138); no arm for
  whitespace folding of REPLACE text (only ENTAIL hash folding is armed, r52:502–503); no arm for stray ENTAIL
  lines hashing to non-row text (ignored by construction, r52:237); no arm for case-differing claim/REPLACE text;
  no arm for indented code blocks (finding above). Each is a gap in what the selftest proves, not a counter
  defect; all contract-required arms are present and pass.
- **INFO (carried from r51, unchanged by this diff)** — `entailed != claims` (r52:246) uses the raw row count, so
  any malformed row double-fails (`bad_rows` + `entailment`); a blank line between table header and first row
  resets header parsing (r52:96–115); the source-cell URL is matched by substring (`u in srow[1]`, r52:231), so a
  longer URL containing a frozen URL would map to the frozen copy; the beyond-words token regex counts tokens
  containing digits as "words of 3+ letters" (r52:87–89). None are round-52 changes; listed for the record only.

No HIGH defect: the frozen code implements the frozen predicate sentence faithfully; all three frozen receipts
(selftest, at-data, do-nothing) reproduce byte-for-byte from the frozen bytes, and the row-hash receipt matches an
independent recomputation.

## Residual risk and verification gaps

- Voter identity rests on filenames (MED above); I could not verify how the wave harness prevents a non-voter
  seat from creating `w1/Mo52EntNN.md` — that is outside this counter's bytes. UNVERIFIED at counter level.
- I did not audit the five pinned source copies' contents against upstream v7.2 (the sha256 pins bind bytes to
  the freeze, and pins reproduced at the data rev; whether upstream says what the 28 claims say is the voters'
  entailment task, not this review).
- The `~~~`-fence and indented-code-block behaviors are probe-verified against the frozen module in scratch; the
  scratch copy (`src/c2-r52.py`, sha256 `0a9ec2ff…`) and probes were removed with the scratch directory after the
  report was written.

## Route for round 53 (named limits, no edits this round)

1. Voter identity: commit-author or salted per-voter token, replacing filename-only identity (MED).
2. Fence grammar: define "unfenced" precisely for voters (column 0, no ```/~~~ anywhere in a report that votes)
   or implement CommonMark closer rules (MED).
3. Authorship: fold case in `claim_hash` or state the case-sensitivity explicitly in the voter instruction (LOW).
