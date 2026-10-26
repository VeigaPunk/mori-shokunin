# Mo50bRevC2Counter — line review of `.ufo/waves/round-50/count-c2.py` (wave a2w1)

Seat: Mo50bRevC2Counter, reviewer. Scope: round-50 `count-c2.py` against its docstring and round-49's
counter; the named areas (normalise by kind, `\|` unescape, words_beyond, unique-claim key, row
validation order, used-by split, opened-date rule, 31 selftest arms via mutation). No counters,
predicates or controls are proposed changed (frozen); everything below is a named limit or a defect
report for the L1.

## 0. Artifact identity and first-hand runs

Working tree `.ufo/waves/round-50/count-c2.py` is byte-identical to the freeze pin (line 17 of
`evidence/freeze-sha256.txt`):

```
533c8403b90e650c786381bbf1394cf327b331936a4111b9faba4abd068ee55d  .ufo/waves/round-50/count-c2.py   (freeze, line 17)
533c8403b90e650c786381bbf1394cf327b331936a4111b9faba4abd068ee55d  .ufo/waves/round-50/count-c2.py   (sha256sum, working tree)
```

All line numbers below refer to that file (391 lines). Runs performed first-hand, read-only:

- From the lane root: `python3 .ufo/waves/round-50/count-c2.py 487941b9395e89678af0053cc443cdb49cdee6e3`
  → `C2=met claims=22 located=22 quote_missing=0 bad_rows=0 sources=3 source_rows=ok pins=ok provenance=ok rev=487941b9395e89678af0053cc443cdb49cdee6e3`, rc=0. Matches the round prompt's claim.
- Selftest from a scratch mirror of the lane (`/fast/scratch/hyaku/mori-r50/Mo50bRevC2Counter/lane/…`;
  the selftest resolves the lane as `dirname`×3 of the script's own directory, lines 245-246, so a bare
  copy elsewhere aborts with FileNotFoundError) → 31 PASS lines, `C2_SELFTEST pass=31 fail=0`, rc=0 —
  matches the committed receipt `evidence/selftest-c2.txt` (last line `C2_SELFTEST pass=31 fail=0`).
- `main` exit codes: met→0 observed; unmet→1 matches the committed do-nothing receipt
  (`evidence/control-c2-donothing-git.txt`: `C2=unmet claims=0 … failed=entry_absent,pins` / `exit=1`);
  setup→2 (unresolvable rev, usage) NOT exercised first-hand — UNVERIFIED, code read only (lines 229-238).

## 1. Diff vs round 49 (`.ufo/waves/round-49/count-c2.py`, 355 lines)

Identical, unchanged from r49: `split_cells`, `normalise`, `parse_claims`, `sources_row`,
`git_reader`, `main`, the `evaluate` skeleton (pins → entry → table → per-row loop → floors →
provenance → output line), and the row_ok condition shape. Deltas, all predicate-driven:

| change | r49 | r50 |
|---|---|---|
| entry / copies / opened | journal-reach-r49, 4 systemd sources + own-work, 2026-10-25 | oom-memcg-stat-r50, 3 sources, 2026-10-26, `kind` tag (`html`/`text`) added (lines 39-46) |
| normalise dispatch | `normalise()` for every copy | `normalise()` for `html`, new `normalise_text()` (lines 61-62) for text copies (lines 116-120) |
| claim-cell rules | none (5-word floor only, line "len(cells[0].split()) < 5") | `MIN_CLAIM_WORDS = 6` (36), new `words_beyond()` + `MIN_BEYOND = 3` (35, 65-67), new case/whitespace-folded claim uniqueness via `seen_claims` (151, 154, 164) |
| `\|` unescape | none | `quotes[0].replace("\\|", "|")` (157) |
| floors | 8 rows | 10 rows (34), claims_floor arm uses 9 rows (329) |
| selftest | prose claims, no pipe escaping | `claim_text(i)` claims, `q.replace("|", "\\|")` in build(), new arms: breadcrumb_identical (364), claim_echoes (368), escaped_pipe_quote_located (376), words_beyond_counts (377), text_copy_keeps_angle_brackets (378); sources_floor arm now asserts the `sources_floor` token (336-338) |

The `kind` dispatch is not cosmetic: the two `.c` copies are full of `<`/`>` comparison operators that
`normalise()`'s tag stripper eats. Mutation M16 below (swapping the dispatch) breaks
`escaped_pipe_quote_located` — the C quote `if (points == LONG_MIN || points < …` is destroyed by
tag-stripping (`< 8)` starts a pseudo-tag that runs to the next `>` in the file). The dispatch is
correct and load-bearing.

## 2. The named areas

**normalise() vs normalise_text() by kind (lines 61-62, 70-75, 116-120).** HTML copies get
script/style-block drop (71), comment drop (72), tag strip (73), entity decode (74), whitespace
collapse (75); text copies get whitespace collapse only (62). This matches the docstring sentence
exactly ("HTML copy: script, style and comment blocks dropped, tags stripped, entities decoded; every
copy: whitespace collapsed"). Arms 378-382 pin each normalise() sub independently; arm 378 pins that
text copies keep `<`. Correct. Residual: D7 below on the script regex.

**`\|` unescape — do split_cells() and SPAN agree?** Yes, in the normal direction. `split_cells`
(51-58) splits only on `(?<!\)\|` (53), so an escaped pipe never splits a cell and the backtick span
keeps `\|`; SPAN (48) then extracts it and line 157 unescapes once, for locating. The selftest proves
the round trip: build() escapes every pipe (line 299 area) and `escaped_pipe_quote_located` (376)
asserts an 8-word quote containing `||` (from `if (points == LONG_MIN || points <`) locates; M03
removing the unescape fails exactly that arm. Two residual corners, both LOW: (a) the unescape is
applied only to the quote — a `\|` in a claim cell keeps its backslash, harmless because the
words_beyond regex ignores `\`; (b) a quote whose LAST character is `\|` immediately followed by the
closing pipe with no space collapses the row — see D2.

**words_beyond() (65-67).** `[A-Za-z][A-Za-z0-9_]{2,}` on both sides, lower-cased, set difference,
`>= 3`. Implements "at least 3 words of 3+ letters that are absent from its quote" case-folded; a
first char must be a letter (so digit-led tokens never count — conservative direction). `words = q.split(" ")` (158) after `\s+` collapse is the 6-25 word count. Arms: 368 (echo floor), 377 (== 4). Correct as a floor; interpretive limit: "words" is read as distinct words (set), and the fold is only case — the frozen predicate says no more.

**Unique-claim key (151, 154, 164).** `re.sub(r"\s+", " ", cells[0]).strip().lower()` — case and
whitespace folded, exactly the predicate's fold. Punctuation is not folded, so "Foo bar." and "Foo
bar" are distinct keys; that is what the frozen sentence says. Defect D1 below on registration order.

**Row validation order (147-183).** Order is: 3-cells + claim ≥ 6 words (148) → fold key, strip sid
(151-152) → sid format + exactly one span + claim dup (154) → unescape, 6-25 words, quote dup,
words_beyond (157-162) → register quote/claim/sid (163-165) → SOURCES row (166-177) → locate (181).
Registration (163-165) happens before the SOURCES-row and locate checks — good: a row that fails those
later checks still poisons its claim/quote for later rows. The only non-registering exits are checks
before line 163 — which is exactly what creates D1. `bad_rows` counts every failure; `claims` (139)
counts raw rows regardless of health, so the claims floor cannot be met by junk rows that then fail
validation (fails closed).

**Used-by split (177).** `re.split(r"[,;]", srow[10])`, strip each element, exact membership of
`entry_path`. Matches the real convention: at 487941b, rows S490/S491 (SOURCES.md lines 269-270) carry
used-by `corpus/knowledge/oom-memcg-stat-r50.md` and the landed run passes with all rows ok. `;` is a
legal separator per the code but no selftest arm uses it (G2). Exactness: element match, not substring
— correct; unpinned by any arm (G6).

**Opened-date rule (176).** Exact string equality `srow[8] == OPENED` (`2026-10-26`, line 33). Any
format deviation → bad row, fails closed. Real rows S489-S491 all carry `| mined | 2026-10-26 |`.
Arm 340 pins it (M04 inverted → 6 arms fail, including this one). Correct.

**The 11-cell SOURCES layout (170, 175-177).** `srow[1]` = "Title — URL" (substring URL match),
`srow[7]` = status, `srow[8]` = opened, `srow[10]` = used-by. Verified against real rows at
487941b (S489 line 268, S490 269, S491 270): 11 cells, indices agree. `sources_row` (103-107) takes
the FIRST row whose first cell is the id, at 0-3 space indent — see D6.

**Provenance (132-134, 193-198).** `has()` requires `source:`/`verified-at:`/`recheck:` among the
first 14 NON-BLANK lines; every S-id used in the table must appear in a `source:` line. Loose reading
of "opens with" (D8/INFO); ids ⊆ cited is real and pinned by arm 352. `recheck:` content is unchecked
by design (the predicate only says the line exists).

**Pins (114-120).** sha256 of the committed copy (bytes recovered via `utf-8/surrogateescape`, which
round-trips the `git show` decode at 213-215) must equal the frozen digest for all three copies,
regardless of rows; failure appends `pins` before the entry branch — matching the committed do-nothing
receipt (`failed=entry_absent,pins` because the copies are absent at the entering tip). Correct.

## 3. Mutation battery — the 31 arms under attack

Method: pristine scratch copy, 21 exact-string mutations (one line each unless noted), selftest per
mutant, FAIL lines recorded. Baseline pass=31 fail=0. "SURVIVED" = no arm failed = arm gap.

| mut | guarded line mutated | outcome |
|---|---|---|
| M01 | 151: `.lower()` dropped from claim key | SURVIVED — no arm has case-differing duplicate claims (G1) |
| M02 | 37: `MIN_BEYOND = 0` | FAILS claim_echoes_quote_unmet |
| M03 | 157: `\|` unescape removed | FAILS escaped_pipe_quote_located |
| M04 | 176: `== OPENED` → `!=` | FAILS honest_met, altered_quote, row_opened_other_day, indented_row_ok, breadcrumb, escaped_pipe (6) |
| M05 | 175: `"mined"` → `!=` | FAILS row_not_mined + 5 met-arms |
| M06 | 177: `[,;]` → `[,]` | SURVIVED — no `;` used-by arm (G2) |
| M07 | 170+175: `len(srow) == 12` | FAILS honest_met + 4 |
| M08 | 154: claim-dup check removed | FAILS breadcrumb_identical_claims_unmet |
| M09 | 159: quote-dup check removed | FAILS duplicate_quote_unmet |
| M10 | 36: `MIN_CLAIM_WORDS = 7` | SURVIVED — no 5/6-word boundary arm (G3) |
| M11 | 181: `if q in norm[url]` → `if True:` | FAILS altered_quote_unmet, quote_from_wrong_copy_unmet |
| M12 | 118: digest `!=` → `==` | FAILS honest_met, indented_row_ok, escaped_pipe — but NOT pin_mismatch_unmet itself: under the inversion the *pristine* copies are the flagged ones, so the arm still sees `pins=bad`; the inversion is caught, by the met-arms (INFO) |
| M13 | 66-67: `{2,}` → `{1,}` (2 sites) | SURVIVED — words_beyond_counts has no 2-letter word (G4) |
| M14 | 72: comment-sub line removed | SURVIVED — the arm's comment contains no `>`, so tag-strip (73) already swallows it; comment-sub is only load-bearing for comments containing `>` (0 in the pinned copy) (G7) |
| M15b | 71: script/style sub → `t = text` | FAILS normalise_drops_script_text, normalise_drops_style_text (a first attempt that deleted the line crashed with UnboundLocalError — harness artifact, redone) |
| M16 | 120: html/text kinds swapped | FAILS escaped_pipe_quote_located — by-kind dispatch is load-bearing |
| M17 | 132: `[:14]` → `[:2]` | FAILS honest_met, indented_row_ok, escaped_pipe — window is load-bearing |
| M18 | 154: `S[0-9]{3,}` → `S[0-9]+` | SURVIVED — no malformed-sid arm (G5) |
| M19 | 81-85: fence toggle removed | FAILS table_inside_fence_unseen_unmet |
| M20 | 177: used-by element match → substring | SURVIVED — no exactness arm (G6) |

20 of 21 mutations caught (M15 crashed for a harness reason; its correct rerun M15b is caught). Six
survive: G1, G2, G3, G4, G5, G6, plus the M14 arm weakness G7. All six are *selftest* gaps — in every
case the production logic itself behaved correctly when exercised directly (e.g. my demo2 feeds sid
`901` and it is counted bad, so M18's rule works, it is just untested).

## 4. Targeted demonstrations against the real `evaluate()`

Demo 1 — trailing escaped pipe (D2): `split_cells('| a | S901 | `ends with pipe \|` |')` (no space
before the closing pipe) → `['a', 'S901']` — the quote cell is silently dropped, the row becomes
2 cells → bad (fails closed). With the usual space (`…\|` |`) the cell survives (3 cells). The landed
entry contains 0 `\|` occurrences and both `.c` copies contain 0 lines matching `\|`, so this is
latent only.

Demo 2 — duplicate registration gap (D1). Four rows: row1 claim C with a 30-word quote (fails length,
NOT registered), row2 same claim C with a valid 6-word quote that locates, row3 sid `901` (bad) with
quote Q3, row4 valid sid with the same quote Q3:

```
C2=unmet claims=4 located=2 quote_missing=0 bad_rows=2 sources=1 source_rows=bad pins=ok provenance=ok rev=R failed=bad_rows,claims_floor,source_rows,sources_floor
```

Rows 2 and 4 duplicate row 1's claim and row 3's quote yet are counted good and located
(bad_rows=2, not 4; located=2 includes the duplicate rows). The predicate's "unique in the table" is
violated for those rows without any corresponding bad row. Met/unmet stays conservative here (the
defective first instances still force unmet), but the printed counts — which receipts cite — overstate
compliance whenever a duplicate's first instance is itself defective.

## 5. Defects

- **D1 — MED — count-c2.py:154,159-164.** Claim and quote uniqueness are enforced only against rows
  that already passed checks at 148-162; a duplicate whose first instance fails any of those checks is
  never flagged and counts as a good, located row (demo 2: bad_rows=2 for a 4-row table where 2 rows
  violate uniqueness; located=2 includes them). Verdict direction stays conservative; counts and
  per-row goodness are wrong. Fix shape (for the L1's consideration only — counter is frozen): register
  `ckey`/`q` in `seen_*` at first sight, before the checks that can fail.
- **D2 — LOW — count-c2.py:51-58.** A cell whose last character is `\|` followed immediately by the
  closing pipe (`` `…\|`| ``) is dropped by `parts[1:-1]` (55) — the row mis-parses to 2 cells → bad.
  Fails closed; latent (0 occurrences in the landed entry and copies).
- **D3 — LOW — count-c2.py:170-174.** URL match `u in srow[1]` is substring-based: any source cell
  containing a frozen URL as a substring (superset URL, suffix, or two URLs at once — first dict
  winner) pins that copy. Latent with the current three URLs; a wrong pin would test the quote against
  the wrong copy.
- **D4 — LOW — count-c2.py:195-201.** `source_rows` reports bad whenever ANY row is bad (`not bad`),
  and `provenance` fails whenever `ids_in_table` is empty — unrelated failures (a bad quote) leak into
  both fields (demo 2 shows `source_rows=bad` caused by quote-length/sid failures). Diagnostic
  over-reporting; inherited unchanged from r49.
- **D5 — LOW — count-c2.py:78-100.** parse_claims absorbs every pipe row after the header until the
  first non-pipe line — a second table adjacent with no prose between contributes its rows/header to
  `rows` (fails closed as bad rows); and a blank line between the header row and the separator row
  resets `header` (87-88 `header = header if rows else None`), silently discarding the entire table
  (fails closed as claims=0). Inherited from r49.
- **D6 — LOW — count-c2.py:103-107.** sources_row is fence-blind and accepts 0-3 space indent in
  SOURCES.md; a fenced or ≤3-space-indented `| S489 |…` decoy line would be picked up (first match
  wins). ≥4-space lines are correctly ignored. Low because SOURCES.md is fleet-pinned at R.
- **D7 — LOW — count-c2.py:71.** The script/style regex ends at the first `</script`: a literal
  `"</script>"` inside JS leaks the remainder of that block into the normalised copy (could make a
  fabricated quote locatable); self-closing `<script …/>` is not dropped. On the pinned copy:
  8 `<script` vs 8 `</script>`, balanced — theoretical today. Inherited from r49 (where all copies
  were HTML and the risk was the same).
- **D8 — INFO/limit — count-c2.py:132-134.** "Opens with source:/verified-at:/recheck:" is enforced
  as presence within the first 14 non-blank lines, in any order and position; `recheck:` content is
  unchecked. This matches r49 and the predicate's loose wording; recorded as a named limit, not a
  proposal.
- **D9 — INFO — count-c2.py:225-228.** `--repo`/`--entry` given as the last argument raises an
  uncaught IndexError (traceback, exit 1) instead of the usage exit 2. Cosmetic robustness; does not
  affect scoring invocations.

Selftest arm gaps (each survives its mutation — the listed production lines are correct but unpinned):
**G1** line 151 case/whitespace fold (M01); **G2** line 177 `;` separator (M06); **G3** line 36 the
6-word boundary (M10 — claim_cell_short uses a 2-word claim, so 5, 6 or 7 all pass every arm);
**G4** lines 66-67 the 3+letters rule (M13); **G5** line 154 malformed S-id (M18); **G6** line 177
element-vs-substring exactness (M20); **G7** line 381 the comment arm needs a comment containing `>`
to be load-bearing (M14).

## 6. What checks out (no defect found)

By-kind normalise dispatch (correct and load-bearing, M16); `\|` unescape round trip (M03, arm 376);
words_beyond semantics and its arm (M02); opened-date exact equality (M04); status `mined` (M05);
11-cell row width (M07); claim and quote duplicate detection among registered rows (M08, M09); locate
semantics (M11); pins (M12, via met-arms); fence skipping (M19); script/style/comment drops and tag
strip for HTML vs raw text for the `.c` copies (arms 378-382, M15b); provenance ids ⊆ source: lines
(arm 352); the real SOURCES layout (S489-S491 at 487941b); the landed result (22 claims, all located,
3 sources, pins ok) reproduces first-hand, rc=0.

## Residual risk and verification gaps

- Exit code 2 paths and `--repo`-overridden runs were not executed (read-only review); receipts cover
  the scoring invocation.
- I did not re-verify the three sha256 pins against the live upstream (out of scope and offline rule);
  the counter's pin check itself ran pins=ok at the landed rev first-hand.
- The predicate's semantic floors (10 rows, 3 sources, quote locality) are floors by design; my
  findings are about the counter's mechanics, per the frozen-contract rule.

No tool was installed or upgraded for this seat (RULES.md channels unused; pacman untouched).

## Findings

- MED — `.ufo/waves/round-50/count-c2.py:154,159-164` — uniqueness registration gap: a duplicate
  claim/quote whose first instance fails an earlier check is counted good and located (demonstrated;
  counts overstate predicate compliance; verdict stays unmet where a defect exists).
- LOW — `.ufo/waves/round-50/count-c2.py:51-58` — `\|` as the last cell character before a
  space-less closing pipe drops the cell (fails closed; latent, 0 occurrences in landed data).
- LOW — `.ufo/waves/round-50/count-c2.py:170-174` — substring URL match can pin the wrong copy
  (latent with the current three URLs).
- LOW — `.ufo/waves/round-50/count-c2.py:195-201` — `source_rows`/`provenance` conflate unrelated
  row failures (diagnostic over-report).
- LOW — `.ufo/waves/round-50/count-c2.py:78-100` — adjacent second table absorbed; blank line
  between header and separator discards the table (both fail closed; inherited from r49).
- LOW — `.ufo/waves/round-50/count-c2.py:103-107` — sources_row fence-blind, matches ≤3-space
  indented id lines in SOURCES.md.
- LOW — `.ufo/waves/round-50/count-c2.py:71` — script regex first-`</script` termination /
  self-closing script tag unhandled (balanced 8/8 on the pinned copy; inherited from r49).
- LOW — selftest arm gaps: case/whitespace fold (151), `;` used-by split (177), 6-word claim floor
  boundary (36), 3+letters rule (66-67), malformed S-id (154), used-by exactness (177), comment arm
  weakness (381 vs 72) — each demonstrated by a surviving mutation (M01, M06, M10, M13, M18, M20, M14).
- INFO — `.ufo/waves/round-50/count-c2.py:132-134` — "opens with" = presence in first 14 non-blank
  lines; recheck: content unchecked (named limit).
- INFO — `.ufo/waves/round-50/count-c2.py:225-228` — trailing `--repo`/`--entry` arg raises
  IndexError instead of usage exit 2.
- INFO — mutation M12: the pin-inversion is caught by honest_met/indented_row_ok/escaped_pipe, not by
  pin_mismatch_unmet (the arm's pristine-pins-ok premise breaks under that mutation); guard still live.
