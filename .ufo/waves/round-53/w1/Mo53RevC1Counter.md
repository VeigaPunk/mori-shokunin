# Mo53RevC1Counter — line review of `.ufo/waves/round-53/count-c1.py`

Seat: reviewer, round 53 wave `w1`, lane `mori-shokunin`. Scope: the C1 counter only — docstring predicate vs
code, `scope()`, `final_votes()`, `evaluate()`, the selftest arms. All probes were run in memory against the real
landed bytes; nothing in the lane, the fleet repo, `tools/`, `corpus/` or any sibling report was written or
mutated. No subagents, no clones, no network, no installs. Scratch
`/fast/scratch/hyaku/mori-r53/Mo53RevC1Counter/` was created, used, and removed.

## Freeze integrity (checked first)

```
$ grep -n count-c1 .ufo/waves/round-53/evidence/freeze-sha256.txt
3:ebaff9158362b905961e9c23b2e91790df135e3b344327030c6f67a2db27005d  .ufo/waves/round-53/count-c1.py
$ sha256sum .ufo/waves/round-53/count-c1.py
ebaff9158362b905961e9c23b2e91790df135e3b344327030c6f67a2db27005d
$ git show f4da3fd4:.ufo/waves/round-53/count-c1.py | sha256sum
ebaff9158362b905961e9c23b2e91790df135e3b344327030c6f67a2db27005d
$ git diff --stat f4da3fd4 -- .ufo/waves/round-53/count-c1.py
(no output)
```

The working-tree counter, the freeze-commit bytes and the `freeze-sha256.txt` row agree; every reading below is
the frozen instrument (544 lines, `HEAD` = `95cf78ee`, data = `2a4213bf`).

## Readings reproduced

```
$ python3 .ufo/waves/round-53/count-c1.py 2a4213bf8da72f7cd78189baa5bb9be825dca1df
C1=unmet scope=46 rows=46 matched=46 status_ok=46 quote_ok=46 source_rows=ok pins=ok provenance=ok
held=44 absent=2 holds=46 changed=0 voted=0 dissent=0 rev=2a4213bf… failed=votes
exit=1

$ python3 .ufo/waves/round-53/count-c1.py --selftest
C1_SELFTEST pass=37 fail=0
exit=0
```

**End-to-end on the real landed ledger** (real ledger + real `corpus/SOURCES.md` + real nine v7.3 copies read at
`2a4213bf`, `d` from `scope()` at `20edafa5`, two synthetic voter files added in memory only to satisfy the vote
arm):

```
C1=met scope=46 rows=46 matched=46 status_ok=46 quote_ok=46 source_rows=ok pins=ok provenance=ok
held=44 absent=2 holds=46 changed=0 voted=46 dissent=0 rev=R
```

That is exactly the contract's target line. Conclusion: at the landed data commit the ledger, the SOURCES rows,
the pins and the derivations are internally consistent with the frozen counter; only the vote arm is open, as
`c1-at-data.txt` says. This is a feasibility reading with synthetic voters, not a verdict.

## Answer to the question about `scope()` and post-entering edits

`scope()` reads `corpus/SOURCES.md` and both entries through `read_entering`, i.e. `git_reader(repo, ENTERING)`
with `ENTERING = 20edafa5…` hard-coded (lines 45, 136-156, 325). It is therefore pinned: if an entry gains or
loses claim rows after the entering tip, D does **not** change, and the ledger must still carry exactly the
entering-tip set. `main()` derives `d` only from `scope(git_reader(repo, ENTERING))` (line 325) and never from the
argument revision, so the argument revision cannot widen or narrow D. Verified: `scope=46`, `rows=46`,
`matched=46`, and an independent recount of the two tables gives 21 + 28 = 49 rows with exactly 3 excluded
(their source row is the 2014 commit patch, no v7.2 raw URL) → 18 + 28 = 46. Scope composition reproduced:

```
== corpus/knowledge/memavailable-estimate-r51.md  found=True rows=21
   IN_SCOPE           18
   url_not_v72         3   (all S496, the 2014 commit patch)
== corpus/knowledge/overcommit-commit-limit-r52.md  found=True rows=28
   IN_SCOPE           28
distinct claim hashes total: 49   scope: 46
```

## Docstring predicate vs the code, clause by clause

`P-C1` is the docstring (lines 8-25). Each clause and its implementation:

| clause (docstring) | code | enforced? |
|---|---|---|
| ledger opens with `source:`, `verified-at:`, `recheck:` lines | 200-205 (`head` = first 20 non-blank lines, `has()`) | yes, but as a 20-line window, not "opens with"; `cited` collected only from `source:` lines |
| one table, header `h entry status source quote disposition` | 206, 99-119 | first matching table only; a second identically-headed table is invisible (F7) |
| exactly one row per hash of D, no other row | 212-221, 254-257 | yes within that first table (`rows`, `matched`, `bad_rows`) |
| each row's `entry` cell names the entry holding that hash | 224-225 | yes (`bad += 1`) |
| `status` equals the counter's derivation (`held` when the v7.2 quote occurs in the v7.3 copy) | 226-229 | yes |
| `source` cell is one S-id naming a SOURCES row at R: mined, opened 2026-10-26, frozen v7.3 URL of that path, used-by lists the ledger | 234-243 | yes, positionally (`len(srow)==11`, `srow[7]`, `srow[8]`, `srow[10]`) — brittle (F11) |
| `quote` is one backticked span, 6-25 words, `\|` reads as `\|`, occurs in the v7.3 copy, equals the v7.2 quote when `held` | 129-133, 230-233 | yes; bounds confirmed (5 words → `quote_ok` drops, 6-25 pass, 26 → drops) |
| `disposition` is `holds` or `changed` | 244-247 | yes |
| every committed v7.3 copy matches its frozen sha256 | 186-192 | yes |
| ≥2 distinct RECHECK voters' final unfenced line carries the disposition, none carries the other | 159-180, 248-253 | yes, last-wins per (hash, voter); but see F1/F2/F3 |
| a voter's line does not count for a row whose quote that voter proposed | 249 only | **partially** — applied to the agreement count, not to the dissent test (F1); text compare is not escape-normalised (F2) |
| the RECHECK voters are exactly the frozen VOTERS list | 50, 163 | yes; non-voter files are ignored entirely |

Two normalization asymmetries inside the quote arm: `one_quote` unescapes `\|`→`\|` (line 133) for the ledger
cell, while `proposed` stores the voter's QUOTE text raw (line 179), and `h`/`entry`/`sid` are backtick-stripped
(217, 224, 234) while `status` and `disp` are not (228, 244).

## Behaviour confirmed correct (do not report as defects)

- **Last-wins per (hash, voter)**: a later unfenced line overrides an earlier one; a fenced later line is ignored
  and the earlier unfenced word stands. Reproduced (`changed` then fenced `holds` → dissent stays 1).
- **Distinct voters**: `v` is a dict keyed by voter name, so `len(agree) >= 2` means two distinct seats; the same
  seat named twice in one file yields one vote.
- **Non-voters ignored**: a RECHECK line in `Mo53Exec08.md` contributes neither agreement nor dissent.
- **Fail-closed on absence**: at the data rev `.ufo/waves/round-53/w1/` does not exist, `git ls-tree` returns
  rc 0 with empty output, `present` is empty, `voted=0`, `failed=votes`, exit 1. A missing ledger, missing copy,
  missing SOURCES row or missing table all produce `unmet` with a named failure.
- **Word bounds**: 5 words fails, 6 and 25 pass, 26 fails — `MIN_WORDS`/`MAX_WORDS` are live.

## Findings

Severity is against the frozen instrument's effect on the C1 verdict. Nothing here proposes a counter change;
each item is a named limit for the round-53 report and a routed item for round 54.

### F1 — MED — author exclusion is applied to agreement only, not to dissent
`/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-53/count-c1.py:249-250`

`agree` drops the voter who proposed the row's quote (`q not in proposed…`, line 249), but the dissent test
`any(word != disp for word in v.values())` (line 250) iterates every voter including that proposer. The docstring
line 23-24 says "a voter's line does not count for a row whose quote that voter proposed", and the parenthetical
qualifies the line, not just the count. Reproduced: a voter that proposed the row's quote and then votes the other
word yields `dissent=1` and the row is never counted in `voted`, so the whole claim fails — while two other
voters carried the disposition. Live risk for the two `absent` rows, where a seat may well propose the v7.3
respelling and also hold an opinion about it: one such dissent kills C1 even though the docstring says that line
does not count. Direction: over-strict (false unmet), not permissive. Routed: either the docstring or the dissent
test has to name which side the exclusion applies to.

### F2 — MED — the author-exclusion text compare is not escape-normalised
`count-c1.py:133` (row quote: `ws(spans[0].replace("\\|", "|"))`) vs `count-c1.py:179`
(`ws(q.group(2).strip("`"))`)

The row's quote has `\|` unescaped to `\|`; the voter's QUOTE line is stored raw. A voter who reproduces the
ledger cell verbatim (escaped form) is therefore **not** recognised as the author, the exclusion silently fails,
and the author's vote counts toward `MIN_VOTES`. Reproduced on a two-voter fixture: escaped proposal →
`voted=1` for that row with one independent voter; unescaped proposal → `voted=0`. Latent for the current 46
rows: no ledger quote cell contains a pipe (the only `\|` in the entry is on the "Reading rules" line, not a
ledger row), so this round cannot be flipped by it. Live for any future ledger whose quote contains `|`.

### F3 — MED — fence tracking is marker-agnostic and length-blind
`count-c1.py:169-173` (and the same idiom at 102-105 in `parse_table`)

`if line.lstrip()[:3] in ("```", "~~~"): fence = not fence` toggles on the first three characters of any line,
regardless of fence length or marker type. Consequences, both reproduced:

- A 4-backtick fence containing a 3-backtick line closes on the inner line, so text that is inside a fenced block
  **is counted as a vote**. Fixture: a report holding a fenced example (4-backtick fence around a 3-backtick
  block) with a line whose first token is `RECHECK` produced `met` on the strength of the example line alone.
- An unbalanced fence (one marker only) silently drops every later vote, because the rest of the file stays
  fenced.

The selftest's `fenced_votes_unmet` covers only a balanced single 3-backtick pair. Wave seats are told to put
drafts inside fenced blocks, so the first mode is reachable by ordinary, non-adversarial authoring.

### F4 — MED — `scope()` silently narrows D with filters the docstring does not state
`count-c1.py:144-155`

The docstring defines D as the claim rows of the two entries whose source row's URL names tag v7.2. The code adds
four drop conditions, each a silent `continue` with no failure label: `len(cells) != 3` (144), no resolvable
SOURCES row (147), no `re.escape(V72) + (path)` match (150), and `one_quote(...) is None` i.e. the quote cell does
not hold exactly one backticked span (153). Reproduced: a claim row with two backticked spans → `scope=0`; a row
with a bare (unbackticked) quote → dropped; a row with an unescaped pipe splitting the cell → dropped. Separately,
`d[claim_hash(cells[0])]` (155) overwrites on a duplicate claim text: two identical claim rows → `scope=1`. All of
this shrinks the number of ledger rows the counter demands, and `met` only requires `len(d) > 0` (269) — the
`scope=46` floor lives in the contract and the receipt, not in the counter. Direction: permissive. Not reachable
at the frozen entering tip (verified 46), but it is a soundness hole in the instrument and in any re-scoping.

### F5 — MED — selftest arms do not cover the arms they claim to
`count-c1.py:396-533` (37 checks) vs `183-277`, `136-156`, `99-119`

All 37 checks pass (`C1_SELFTEST pass=37 fail=0`, exit 0), and the docstring at line 335 claims it "asserts
verdict and the named failure for each arm". Branches with **no** arm:

1. the author-proposer dissent interaction of F1 (249-250);
2. the escaped-pipe proposal of F2;
3. `ids <= cited` at 264 in isolation — `prov=False` removes `source:` and `recheck:` together, so the subset
   clause is untested (a probe confirms it works: a row citing an S-id absent from the header → `provenance=bad`);
4. `len(srow) == 11` and the positional columns at 238-239;
5. `MAX_WORDS` at 231 (only the too-short side is tested);
6. every `scope()` narrowing filter of F4 (`scope_reader` exercises only the fenced-table skip and the non-v7.2
   URL) and the hash-collision overwrite;
7. `parse_table` absorbing a later table when the first matching table is empty (108-109);
8. a second identically-headed table (F7);
9. the `norm[path]` KeyError (F6);
10. a 4-backtick fence (F3);
11. `has("verified-at")` independent of `source`/`recheck`;
12. semicolon-separated used-by;
13. a backticked `status` or `disp` (F13).

Also: `selftest()` reads the v7.3 copies from the **working tree** (`open(os.path.join(lane, copy))`, line 339),
not from a frozen revision and without re-checking their sha256, so the selftest is not hermetic w.r.t. the freeze
discipline of `contract.md` ("measured with `git show <freeze>:<path>`"). The working tree matched the commit when
I checked (`git status --porcelain` showed only untracked `w1/`, `w1.ready*`, `evidence/selftests/`), so this is
not a live divergence.

### F6 — LOW — `norm[path]` / `V73[path][2]` are unguarded dictionary lookups
`count-c1.py:226`, `238`

`path` comes from `scope()` (the v7.2 URL of the SOURCES row); `norm` and `V73` are keyed by the nine pinned
paths. A scope path outside those nine raises `KeyError` — reproduced: `KeyError: 'mm/some_other_file.c'`, traceback
on stderr, **no `C1=` line**, exit 1 (indistinguishable from a clean unmet by exit code alone). Not reachable this
round because D is frozen at `20edafa5` and its 46 rows map onto exactly the nine copies (verified). A clean
`C1=unmet failed=<label>` or exit 2 would be the correct shape.

### F7 — LOW — "and no other row" is enforced only inside the first identically-headed table
`count-c1.py:108-118`, `206`

`parse_table` stops at the first non-`|` line after rows start, so a second table carrying the same header and
extra rows is never read. Reproduced: appending an appendix table with one extra row left `met=True`,
`rows=46 matched=46`. A stray or decoy row can therefore sit in the ledger unmeasured. (The converse — an empty
first table whose rows live in a later one — does fail, but with `bad_rows,rows` because the later header row is
absorbed as a data row, i.e. the diagnosis is wrong even though the verdict is right.)

### F8 — LOW — `source_rows=ok|bad` conflates every bad-row cause with a source-row defect
`count-c1.py:268` (`srows = "ok" if ids and not bad else "bad"`)

`bad` is incremented for malformed cell counts (214), unknown/duplicate hash (219), entry mismatch (225), missing
or wrong source row (241), and invalid disposition (245). Reproduced: a wrong `entry` cell alone prints
`source_rows=bad`. The output field therefore cannot be used to tell a SOURCES defect from a ledger typo.

Two related diagnostics: (a) `met = not failed and len(d) > 0` (269) can print `C1=unmet` with **no** `failed=`
list when `d` is empty — `main()` guards that case with exit 2 (326-328), but `evaluate()` called directly does
not, so the line is not self-explanatory; (b) `holds=`/`changed=` are incremented only after the disposition check
passes (244-247), so a ledger with one invalid disposition prints `rows=46` but `holds+changed=45` with no field
saying which row was skipped.

### F9 — LOW — `main()` crashes when `--repo` is the last argument
`count-c1.py:305-308`

`repo = args[i + 1]` with no bounds check. `count-c1.py abc --repo` → `IndexError: list index out of range`,
traceback, no `C1_SETUP` line. The documented usage is `<rev> [--repo DIR]`, so a trailing `--repo` is a usage
error that should exit 2 with the usage line.

### F10 — LOW — positional SOURCES parsing and a 20-line front-matter window
`count-c1.py:238-239`, `200`

The source-row arm assumes an 11-column SOURCES table and reads `srow[7]` (status), `srow[8]` (opened),
`srow[10]` (used-by) by index, and splits used-by on `[,;]`. Any schema change (an added column) turns every row
into `bad_rows` with no column-level diagnosis. Likewise `head` is the first 20 non-blank ledger lines, and
`cited` (203-205) only collects S-ids from lines matching `^[-* ]*source\s*:`, so a ledger with a longer preamble
loses `provenance` for a reason the output does not name. Both are currently satisfied (9 `source:` lines,
`verified-at` on the 11th non-blank line, `recheck:` on the 12th, 11 columns).

### F11 — LOW — `status` and `disp` are not backtick-stripped while `h`, `entry`, `sid` are
`count-c1.py:217`, `224`, `228`, `234`, `244`

Reproduced: a backticked status cell → `failed=status`; a backticked disposition → `failed=bad_rows,votes`. The
landed ledger writes all six cells bare, so this is latent, but the normalization is inconsistent within one row.

### F12 — LOW — the contract's `P-C1` summary is not the docstring verbatim, as the contract asserts
`contract.md` §C1 "**P-C1.** The predicate is the docstring of `count-c1.py` verbatim (same sentence)"

The contract asserts verbatim identity, then gives a compressed sentence that omits the front-matter keys, the
header cells, the S-id `mined`/`opened`/`used-by` conditions, the 6-25 word span, the escaped-pipe reading and the
sha256 pins — all of which the docstring and the code enforce. A reader who checks the contract sentence against
the data will miss clauses the counter applies. The docstring is the operative text; the contract's rendering
should be a pointer, not a paraphrase.

### F13 — LOW — indented code blocks are not fences
`count-c1.py:169`

`line.lstrip()[:3]` never matches a 4-space-indented line, so a line whose first token is `RECHECK` inside an
indented code block counts as a vote. That is consistent with the wave rule ("starts (after spaces) with
`RECHECK …`") but not with a plain reading of "unfenced"; only the fenced case is skipped.

## Residual risk

- The vote arm is the only arm still open at the data commit (`voted=0`, `failed=votes`); the verdict of C1
  depends entirely on 12 seat reports that did not exist at `2a4213bf`. I could not observe them (UNVERIFIED by
  design at my read time). Under F1/F3 a single authored example line or a single author-proposer dissent is
  enough to move the verdict, in opposite directions.
- `held` still only proves the v7.2 words occur somewhere in the v7.3 file (the docstring's own named limit); the
  counter cannot see placement or meaning, and the disposition plus two votes are the only carriers.
- The pins prove the committed copies hash to the frozen digests; they do not prove cgit served tag v7.3. I did
  not re-fetch (no network use this seat), so that leg is UNVERIFIED here.
- F2 and F4 are latent against today's bytes but are properties of the frozen instrument, so they will apply
  unchanged to any round-54 ledger that reuses it.

## Verification gaps

- I did not run the counter at a revision carrying real vote reports (none exist at the data rev); the vote-arm
  readings are in-memory fixtures over the real copies and the real ledger.
- I did not modify or re-freeze the counter, so every finding is a recommendation only.
- I did not check `count-c2.py`.
- The claim-level source re-fetch (cgit v7.3) was out of scope for this seat and was not performed.

## Findings (summary)

| # | severity | concern (file:line) |
|---|---|---|
| F1 | MED | `count-c1.py:249-250` — author exclusion applied to agreement only; an author-proposer's dissent still vetoes the row against the docstring's "line does not count" |
| F2 | MED | `count-c1.py:133` vs `179` — row quote unescapes `\|`, the voter's QUOTE text does not, so the author exclusion silently fails and the author's vote counts |
| F3 | MED | `count-c1.py:169-173` — fence toggle is marker-agnostic and length-blind; a 4-backtick fence containing a 3-backtick line lets fenced text count as a vote; an unbalanced fence loses all later votes |
| F4 | MED | `count-c1.py:144-155` — `scope()` silently drops rows (`cells!=3`, no SOURCES row, non-raw-v7.2 URL, quote cell without exactly one backtick span) and overwrites duplicate claim hashes; D can shrink below the 46 the contract fixes |
| F5 | MED | `count-c1.py:396-533` — 13 `evaluate`/`scope`/`parse_table` branches have no selftest arm; `selftest()` also reads the v7.3 copies from the working tree (line 339), not from the frozen revision |
| F6 | LOW | `count-c1.py:226,238` — unguarded `norm[path]` / `V73[path][2]`; a scope path outside the nine pinned copies raises `KeyError`, no `C1=` line, exit 1 |
| F7 | LOW | `count-c1.py:108-118,206` — "no other row" is enforced only inside the first identically-headed table; a second such table with extra rows is unmeasured |
| F8 | LOW | `count-c1.py:268` — `source_rows=bad` fires for entry mismatches, bad dispositions, duplicate/unknown hashes and malformed cells, not only source-row defects |
| F9 | LOW | `count-c1.py:305-308` — `--repo` as the last argument raises `IndexError` instead of the usage/exit-2 path |
| F10 | LOW | `count-c1.py:200,238-239` — positional 11-column SOURCES parse and a 20-non-blank-line front-matter window; failures surface as `bad_rows`/`provenance` without a column/line diagnosis |
| F11 | LOW | `count-c1.py:217,224,228,234,244` — `status` and `disp` are not backtick-stripped while `h`/`entry`/`sid` are |
| F12 | LOW | `contract.md` §C1 P-C1 — the compressed sentence is presented as the docstring "verbatim" but omits six clauses the code enforces |
| F13 | LOW | `count-c1.py:169` — 4-space-indented code blocks are not fences, so a line inside one counts as a vote |
