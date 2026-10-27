# Mo54RevC2Counter — line-by-line review of `.ufo/waves/round-54/count-c2.py`

MACHINE_ID: plazir27
Seat: Mo54RevC2Counter (reviewer, leaf — no subagents, no questions). Scope: `count-c2.py` only — docstring
predicate vs code, `parse_claims` (table end, fences), the COPIES map (URLs as S521–S524 and S502/S507 carry
them), `entail_votes` (results binding, authorship by hash, fences), `evaluate` (every arm and failed name),
the selftest arms. Lane bounds respected: no subagents, no repo mutation, scratch under
`/fast/scratch/hyaku/mori-r54/Mo54RevC2Counter/` (removed at the end of this seat).

Reviewed bytes: working-tree `sha256sum` of `.ufo/waves/round-54/count-c2.py` =
`d6b42f893b304ca355c03a4e43ad431b268b39ecfe8163c6871bbc0d6550785e`, equal to line 3 of
`.ufo/waves/round-54/evidence/freeze-sha256.txt` — the reviewed bytes are the frozen bytes. Line numbers below
cite that file (570 lines). No tool was installed or upgraded (nothing to record under the 2026-10-19
authorization).

## Observed runs (command → output → exit)

- `scripts/hyaku/disk-guard.sh status` → exit 0; `/fast/scratch/hyaku` 26 % use, 596.8 G free.
- `python3 .ufo/waves/round-54/count-c2.py 78295c764093ff1f6cee08d7246679900bde7265` →
  `C2=unmet claims=21 located=21 quote_missing=0 bad_rows=0 sources=6 source_rows=ok pins=ok provenance=ok entailed=0 dissent=0 rev=78295c764093ff1f6cee08d7246679900bde7265 failed=entailment`, exit 1 —
  byte-identical to `evidence/c2-at-data.txt`.
- `python3 .ufo/waves/round-54/count-c2.py --selftest` → `C2_SELFTEST pass=54 fail=0`, exit 0; no FAIL line.
- `python3 .ufo/waves/round-54/count-c2.py --hashes 78295c7…` → 21 rows; every hash equals the `h=` in
  `evidence/c2-claims.txt` (row 1 `fcf9f378a818` … row 21 `257f4acfda4e`).
- Pins re-verified independently of the counter — `git show 78295c7…:<copy> | sha256sum` for all six copies:
  `94d24a605b61f94a…` (memory-failure.c.v7.3), `8011bb158129776b…` (hwpoison.rst.v7.3),
  `d852f950e42d92b8…` (sysfs-devices-node.v7.3), `a395e62b36ace3d1…` (memory-failure-trace.h.v7.3),
  `f81feb3dfca5f054…` (vm.rst.v7.3), `bc178ff511e05c1b…` (proc.rst.v7.3) — all six match the COPIES digests at
  lines 60–68.
- Lister format: `git -C <lane> ls-tree --name-only 78295c7… .ufo/waves/round-54/` prints full paths from the
  repo root (`…/contract.md`, `…/controls`, `…/count-c1.py`, `…/count-c2.py`, `…/evidence`); the same command on
  `.ufo/waves/round-54/w1/` and on a nonexistent `.ufo/waves/round-54/nonexistent/` both exit 0 with no output.
  So `entail_votes`' gate `path not in present` (line 151) compares like with like (full paths), and a missing
  or empty directory degrades to "no voter files present", not to an error.
- SOURCES rows at the data rev: S521 (SOURCES.md line 300), S502 (281), S507 (286) — each 11 cells, status
  `mined`, opened `2026-10-27` / `2026-10-26`, used-by cell contains
  `corpus/knowledge/memory-failure-kills-r54.md` as an exact comma-list member, and the URL cell carries the
  COPIES URL verbatim (`…/plain/mm/memory-failure.c?h=v7.3`, `…/plain/Documentation/filesystems/proc.rst?h=v7.3`,
  `…/plain/Documentation/admin-guide/sysctl/vm.rst?h=v7.3`). S522–S524 visible in the same grep with the same
  shape. `controls/c2data.py` writes these rows from `c2.COPIES` itself, so registry and counter cannot drift
  apart by construction.
- Data state: `.ufo/waves/round-54/w1-results.json` does not exist at 78295c7 (`git show` → `fatal: path … does
  not exist`) nor in the working tree; `w1/` is empty at the data rev. Consistent with the recorded no-votes
  reading (`entailed=0 … failed=entailment`).

## Docstring predicate (lines 7–23) vs code — clause walk

| predicate clause (docstring line) | code | verdict |
|---|---|---|
| opens with `source:` lines, `verified-at:` and `recheck:` (8–9) | `head` = first 14 non-blank lines, `has()` regex (200–204) | matched, but looser than "opens with" — see Finding 5 |
| table header cells claim, source, quote, ≥14 rows (9) | `parse_claims` header match (114–117), `claims < MIN_CLAIMS` (207–209) | matched (exact lowercase triple; `MIN_CLAIMS=14` line 48) |
| claim cell ≥6 words, unique (case+whitespace folded), ≥3 words of 3+ letters absent from its quote (10–11) | 216, 219+222, 225–229 (`words_beyond`, 91–94) | matched; "3+ letters" is implemented as "3+ chars starting with a letter" (tokens like `S521` count) — pedantic, noted |
| source cell one S-id; SOURCES row mined, opened 2026-10-26/27, URL among the six, entry in used-by (11–13) | 220–222 (`fullmatch S[0-9]{3,}` on the stripped cell), 243–245 | matched; observed against the real rows |
| quote cell one backticked span, 6–25 words, escaped `\|` reads as `\|`, unique, occurs whitespace-collapsed in the committed copy (13–15) | 221 (`SPAN`), 225–226, 227–231, 249 | matched; the real row 9 exercises the `\|\|` escape and locates |
| table draws on ≥4 of the 6 sources (15) | 249–252, 267–268 | matched with a wrinkle — see Finding 6 |
| every committed copy matches its frozen sha256 (15–16) | 185–191 | matched; independently re-verified above |
| ≥2 distinct ENTAILMENT voters, unfenced line in their own report at R (16–18) | `entail_votes` 137–167, gate 253–260 | matched (distinct voters via a set; same voter twice counts once — selftest arm) |
| no ENTAILMENT voter carries an unfenced overclaim line (18) | 257–258 | matched; flat prohibition, no last-line-wins — consistent with the frozen C2 kill rule (overclaim is resolved only by rewording + two fresh votes), deliberately unlike the C1 dissent rule |
| voter counts only when w1-results.json at R lists a result of that name (18–20) | 141–148, 151 | matched in code; shape coupling is the top residual risk — see Finding 1 |
| voter's entailed line does not count for a row whose text that voter wrote (REPLACE text hashes to h) (20–21) | 163–165, 256 | matched; REPLACE text is trimmed and hashed with the same `claim_hash` (probe) |
| h = first 12 hex of sha256 of the claim cell, whitespace collapsed, ends stripped (21–22) | `claim_hash` 129–130 | matched |
| voters are exactly the frozen VOTERS list — no other file, no L1 file, no other directory (22–23) | 45, 149–152 | matched; selftest arms cover L1-file, non-voter seat, out-of-list, round-52 name, `.txt`, other-directory cases |
| Output line + `failed=` list (26–27) | 280–286 | matched field-for-field |
| Exit 0 met / 1 unmet / 2 setup; read-only git show / ls-tree / rev-parse (28) | 313, 326, 332, 335; subprocess calls at 291, 299, 328 | matched (observed exit 1 unmet, exit 0 selftest); exactly those three git commands |

## `parse_claims` (104–127)

- Fence model: any line whose first three characters (after lstrip) are ``` or `~~~` toggles one boolean
  (102–104); content inside is skipped (105–106). Marker type is not tracked (a `~~~` line inside a ``` block
  toggles off) and a 4-space-indented code block is not a fence — see Finding 8. The real entry wraps nothing in
  fences before the table; the selftest arm `table_inside_fence_unseen_unmet` covers the fenced-table case.
- Table end: the first non-pipe line after the header and at least one row ends the scan (`break`, 108–109) —
  later tables are never read. A blank line mid-body therefore ends the table, and a second table with the same
  header sits unchecked (probe P1b: two same-header tables → only the first table's rows parsed). See Finding 2.
- Blank line before the separator: `header = header if rows else None` (116) resets the header while `rows` is
  still empty, so a blank line between the header row and the separator makes the whole table invisible
  (probe P1: header=None, rows=0 → `failed=table`). False-negative direction. Part of Finding 2.
- Header detection requires the exact folded triple (114–117); a data row before any header is silently skipped
  (117) — correct direction (the predicate requires the header).
- Separator rows are skipped by the `:?-{3,}:?` all-cells test (123–124); a data row cannot collide (a single
  `-` cell fails the 3-dash minimum).

## COPIES map (53–68)

- The six URLs are byte-identical to the URL cells of S521–S524 (sources-r54) and S502/S507 (sources-r53) at the
  data rev — observed, and `c2data.py` generates those rows from `c2.COPIES`, so the registry cannot name a
  different URL than the counter pins.
- Copy paths match `SRC_DIR`/`R53_DIR` (41–42) and the real layout; digests match independent sha256 of the six
  committed copies at 78295c7 (observed above). All six kinds are `"text"`, so `normalise()` (96–101) never runs
  — Finding 9.
- `?h=v7.3` query form matches the contract's cgit form; no raw.githubusercontent or jsdelivr URL is pinned for
  C2 (those answered 429/403 on 2026-10-27 per the seat brief — the counter avoids them entirely).

## `entail_votes` (137–167)

- Results binding (141–148): `settled` is built only from a top-level JSON object's `results` array, entries
  that are objects with a string `name`. Malformed JSON, a top-level array, a missing file, or a non-dict entry
  all degrade to an empty `settled` (votes then count nothing — safe direction; selftest arms
  `entail_results_absent_unmet`, `entail_results_malformed_unmet`, `entail_voter_not_in_results_unmet`). The
  shape is pinned only by this frozen code and by `controls.py:78–80` (same shape) — Finding 1.
- Presence + settlement gate (149–152): the file must be listed by `ls(ENTAIL_DIR)` at R and the voter name must
  be in `settled`. `git ls-tree --name-only` prints full paths from the repo root (observed), matching
  `ENTAIL_DIR + voter + ".md"`. An empty or nonexistent `w1/` yields an empty `present` (observed rc 0, no
  output).
- Fences (153–159): one boolean toggled by ```/`~~~` prefixes, same model as `parse_claims`; selftest arms cover
  fenced votes ignored and a fenced dissent ignored.
- Vote capture (160–162): `^\s*ENTAIL\s+<12 hex>\s+(entailed|overclaim)\b` — leading whitespace allowed, a
  blockquote `>` prefix is not (probe), trailing prose after the word is allowed (`entailed — note`, `entailed.`
  both count; `overclaimer` does not match — probe). Distinct voters are deduplicated by the set of
  (kind, voter) pairs.
- Authorship (163–165, 256): every unfenced `REPLACE <old> :: <text>` line adds `claim_hash(<text>)` to that
  voter's authored set; the bar in 256 removes that voter's `entailed` vote only for the hash it wrote
  (selftest arms: author's vote not counted; author + two others met; a fenced REPLACE is not authorship; a
  REPLACE for a different hash does not bar other rows). The `<old>` hash group is ignored — per predicate, only
  the text matters.
- The counter reads only the twelve `Mo54En01–Mo54En12.md` files (45, 149) — RECHECK voters' files in the same
  directory are never opened, so the C1/C2 separability claim holds for this counter (no ledger, no C1 row, no
  RECHECK vote is read; the only paths are the constants at 40–44 plus `corpus/SOURCES.md` at 210).

## `evaluate` (176–287)

- Pins (183–191): every COPIES entry must be present at R with the exact sha256 (bytes recovered via
  surrogateescape round-trip); absent or altered copy → `pins` failed. A missing copy also empties `norm[url]`,
  so its rows go to `quote_missing` as well.
- Entry (192–209): absent → `entry_absent`; no header-matching table → `table` (+ `claims_floor`,
  `source_rows`); `claims = len(rows)` counts malformed rows too, so any bad row also breaks
  `entailed != claims`.
- Row loop (215–260): 3 cells and ≥6 claim words (216); folded claim uniqueness (219, 222); exactly one S-id
  after stripping backticks/spaces (220–222); exactly one backticked span in the quote cell (221–222);
  6–25 words, quote uniqueness, ≥3 beyond-words (225–230); SOURCES row must exist with 11 cells, contain a
  COPIES URL in cell 1, be `mined`, opened 2026-10-26/27, and list the entry path as an exact comma-list member
  of cell 10 (238–245); location is a whitespace-collapsed substring of that row's URL copy (249). Every
  short-circuit increments `bad` → `bad_rows` + `source_rows` + `entailment` all trip together — no partial
  credit.
- Entailment (253–260): `ok_voters` = settled voters with an `entailed` line who did not author the hash; any
  overclaim from a settled, present voter → `dissent` for that row and the row cannot be entailed (257–259);
  `dissent or entailed != claims` → `entailment` failed (263–264). Matches the frozen kill rule.
- Provenance (269–275): every S-id used in the table must appear in the entry's `source:` line(s) within the
  14-line head window (selftest arm `table_id_uncited_in_source_unmet`); `verified-at:` and `recheck:` must be
  present (selftest arm for a removed `verified-at`). See Findings 5 for the window's looseness.
- Failed names and the output line (279–286): `pins, entry_absent, table, claims_floor, bad_rows, entailment,
  quote_missing, sources_floor, provenance, source_rows` — exactly the docstring's contract; `failed=` is
  sorted and deduplicated; `met = not failed`.

## `main` / `selftest` (305–337, 339–567)

- `main`: `--selftest` exact-match; `--hashes <rev>` reads ENTRY from the lane root derived from `__file__`
  (four dirnames up — correct for the frozen location) and prints row/hash/claim for every parsed row; the
  scoring path resolves `<rev>^{commit}` (exit 2 on failure) and always evaluates the resolved commit. Malformed
  `--repo`/`--entry` (missing value) raises IndexError — Finding 7.
- `selftest`: 54 checks, all passing (observed). Coverage is broad: honest met line; entry absent; no table;
  altered quote; quote from the wrong copy; quote located only in another copy (per-row URL binding); short and
  26-word quotes; duplicate quote; claims floor; sources floor with 3 sources; exactly 4 sources met; status
  not mined; opened 2026-10-25 rejected / 2026-10-26 accepted (boundary); used-by missing; 3-space indented
  SOURCES row ok / 4-space rejected; pin mismatch; table id uncited; `verified-at` removed; wrong header;
  2-word claim; 13 duplicate claims; claim echoing its quote; table inside a fence; foreign entry path; and 20
  entailment arms (no votes, one voter, same voter twice, one row single vote → `entailed=13`, dissent,
  unsettled voter, results absent/malformed, settled subset met, unsettled dissent ignored, L1 file, non-voter
  seat, out-of-list voter, round-52 name, `.txt` file, other directory, fenced votes, fenced dissent, non-voter
  dissent ignored, authorship bar, author + two others, fenced REPLACE not authorship, hash of other text,
  whitespace-folded hash met) plus `voters_frozen`, `words_beyond_counts`, `text_copy_keeps_angle_brackets`.
- Gaps in the selftest (none blocking): no arm for a blank line between header and separator (Finding 2a), none
  for a second same-header table (2b), none for the trailing-cell escaped pipe (3), none for case-variant quote
  uniqueness (4), none for a >14-line preamble (5), none for `kind="html"` (9), none for the `--repo`-last-arg
  IndexError (7). The `drop` parameter of `build()` (386) is never used by any check — dead parameter.

## Probes (frozen module imported read-only in scratch; synthetic strings only)

- P1 `parse_claims` with a blank line between header row and separator → `header=None rows=0` (table invisible).
- P1b two same-header tables separated by a blank line → `rows=1`, first table's row only; the second table's
  row is never parsed.
- P2 `split_cells("| a | b | c \\|")` → `['a', 'b']` (last cell dropped); `split_cells("| a | b \\| |")` →
  `['a', 'b \\|']` (mid-cell escaped pipe kept — the row-9 shape works).
- P3 `ENTAIL_RE`: `entailed — note` and `entailed.` match as `entailed`; `overclaimer` does not match;
  `  ENTAIL …` and tab-indented match; `> ENTAIL …` does not.
- P4 a 4-space-indented vote line matches `ENTAIL_RE` (counts as unfenced).
- P5 `REPLACE_RE` trims the text both ends; `claim_hash` of the captured text equals `claim_hash` of the
  trimmed text.
- P6 exact duplicate quote → `bad_rows=1`; P6b quotes differing only in case → both located, `bad_rows=0`
  (case-sensitive quote uniqueness); P7 claims differing only in case → second row `bad_rows=1` (case-folded
  claim uniqueness).
- P8 15 filler lines before `source:` → `provenance=bad` (14-non-blank-line window).
- P9 a row whose quote is missing contributes nothing to `sources=` (`sources=1` with two cited copies, one
  located row).
- CLI: `count-c2.py <rev> --repo` (missing value) → `IndexError: list index out of range`, exit 1, no `C2=` line.

## Findings

1. MED — `.ufo/waves/round-54/count-c2.py:141–148` (results binding): the settlement record
   `.ufo/waves/round-54/w1-results.json` is read as a top-level JSON object with a `results` array of objects
   carrying a string `name`; any other shape (top-level array, different key, annotated names) silently settles
   zero voters, so every vote is ignored and C2 reads `entailed=0 … failed=entailment` after votes land — a
   false kill (safe direction, immediately visible). The file does not exist yet at the data rev or in the
   working tree (observed), and nothing outside the frozen code pins the shape (`controls.py:78–80` uses the
   same shape; `scripts/hyaku/ufo-wave-policy-v2.json` does not mention it). Named limit / coordination item for
   the L1 before votes settle; routed item for round 55 if the shape should be documented outside frozen code.
2. LOW — `count-c2.py:107–116` (`parse_claims` blank-line semantics), probes P1/P1b: (a) a blank line between
   the header row and the separator resets the header and makes the whole table invisible (`failed=table`,
   false negative); (b) a blank line mid-body ends the table and the scan breaks, so a second table with the
   same header is never parsed — its rows sit unchecked in a file the counter can call met (they also do not
   count toward the floor, so this cannot inflate the claim). Not exercised by the real entry (single claims
   table; the decision tables have different headers and fall after the break). Routed item.
3. LOW — `count-c2.py:74–83` (`split_cells`), probe P2: a row whose last cell ends with an escaped pipe loses
   that cell (`| a | b | c \|` → two cells → `bad_rows`). Unreachable for well-formed C2 rows (the quote cell
   ends with a backtick; the real row 9's mid-cell `\|\|` locates fine). Latent parser bug; routed item.
4. LOW — `count-c2.py:219` vs `227/231` (uniqueness asymmetry), probes P6b/P7: claim uniqueness is case-folded,
   quote uniqueness is case-sensitive; the docstring says "unique in the table" for both without qualification,
   so two quotes differing only in case both count. Lenient direction; named limit.
5. LOW — `count-c2.py:200–204` (provenance window), probe P8: "opens with source: lines, verified-at: and
   recheck:" is implemented as "each key occurs somewhere in the first 14 non-blank lines", and `has()` also
   matches list-item/bold forms (`- source:`, `**source:**`). Looser than the verbatim predicate inside the
   window; keys placed deeper fail provenance (false negative). The real entry carries all three keys in its
   first 8 non-blank lines (observed). Named limit.
6. LOW — `count-c2.py:249–252` with `267–268`, probe P9: `used_sources` accumulates only on located rows, so a
   source whose rows all fail location does not count toward the ≥4 floor and the reported `sources=N`
   undercounts "the table draws on". Harmless (the run already fails `quote_missing`); named limit.
7. LOW — `count-c2.py:321,323` (argument parsing), observed: `--repo` or `--entry` as the last argument raises
   `IndexError` → traceback, exit 1 — outside the documented 0/1/2 taxonomy (docstring line 28). No `C2=` line
   is printed, so it cannot fake a met reading. Routed item.
8. LOW — `count-c2.py:102,155` (fence model), probe P4: fences are only ```/`~~~` prefixes; a 4-space-indented
   code block counts as unfenced (an indented vote line counts, an indented table row counts), and a `~~~` line
   inside a ``` block toggles the state because the marker type is not tracked. Consistent across both parsers
   and with "unfenced line" read literally; lenient direction. Named limit.
9. INFO — `count-c2.py:96–101`: `normalise()` (the HTML path) is dead code — all six COPIES kinds are `"text"`
   and no selftest arm covers `kind="html"`; a future HTML copy would run an untested path.
10. INFO — `count-c2.py:343–345`: the selftest loads the six copies from the working tree, not from a rev, so
    it validates against drifting bytes; the freeze-sha256 receipt and git-show measurement are the actual
    guards (the working tree currently matches the freeze for the counter itself — observed).
11. INFO — `count-c2.py:308–316`: `--hashes` ignores `--repo`/`--entry` and derives the lane root from
    `__file__`; correct for the frozen location, wrong if the script is copied elsewhere.
12. INFO — `count-c2.py:133`: the trailing `\b` admits a prose suffix (`entailed — note` counts as entailed)
    and rejects `overclaimer`; blockquote-prefixed lines never count. Matches "unfenced line starting (after
    spaces)".
13. INFO — `count-c2.py:238–242` with `169–173`: the URL binding is substring first-match in COPIES dict order,
    and `sources_row` takes the first sid-matching line of SOURCES.md without skipping fenced lines; the real
    registry rows carry exactly one URL each and no fenced rows (observed), so neither is exercised today.
14. INFO — `count-c2.py:386`: the `drop` parameter of the selftest's `build()` is never passed by any check —
    dead parameter.

## Verification gaps

- The orchestrator's future `w1-results.json` bytes are UNVERIFIED (file absent at the data rev and in the
  working tree) — Finding 1 is a shape-coupling risk, not an observed failure.
- Voter reports landing in `w1/` while this seat ran (Mo54En03/04/05/07/09 visible) were not judged — out of
  scope for this seat; the counter itself will judge them at the settled rev.
- Everything else cited above was executed and observed; no step was skipped for cost.
