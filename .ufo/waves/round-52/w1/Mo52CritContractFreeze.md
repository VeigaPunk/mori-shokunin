# Mo52CritContractFreeze — attack on the frozen contract, counters, receipts and separability

Seat: Mo52CritContractFreeze. Lane: mori-shokunin. Round 52 wave w1.
Scratch: `/fast/scratch/hyaku/mori-r52/Mo52CritContractFreeze/` (removed after this report).
Nothing was installed or upgraded during this seat (no toolchain change; all checks used git/python3 -B).

Attack surface (assignment): `contract.md` vs `count-c1.py`, `count-c2.py` and the receipts in `evidence/`:
predicate sentence == counter code == receipt label; before-values == receipts; controls skip exactly the claimed
work; causal separability (each counter with the other claim's data reverted); honesty of named limits;
`freeze-sha256.txt` against the bytes at freeze commit `d3a8ea5957b73bddbde750a8c0af2fba8da8b7c2`.

## 1. Freeze bytes (contract lines 6-9)

All 24 paths in `evidence/freeze-sha256.txt` were re-hashed at `d3a8ea…` via
`git show d3a8ea…:<path> | sha256sum` — 24/24 equal (contract.md, count-c1.py, count-c2.py, controls/c1-data.py,
controls/c1-controls.py, build-w1-spec.py, census-start.txt, the eight control receipts, selftest-c1/c2,
sweep-overcommit.txt, and the five `corpus/evidence/sources-r52/` copies). The lane's index/working tree still
matches the freeze bytes for every frozen path (no in-place edit; contract line 8-9's fallback is not triggered).
Topology: `d3a8ea` (freeze) is the parent of the data commit `8524904…`; `4f266ef2…` is the round-51 closure tip.

## 2. Predicate sentence == counter code == receipt label

Contract P-C1 (line 30-31) and P-C2 (line 65-66) both state the predicate is the counter docstring verbatim.
I compared docstrings (`count-c1.py:6-35`, `count-c2.py:6-22`) clause by clause against the implementations:

- C1 (A) axes: `manifest_targets` (`count-c1.py:96-110`) uses lane==mori, verdict==admitted, round<=51,
  axis improved|harmed, highest round; `check_axes` (`:173-214`) enforces one `## Axes` heading outside fences,
  one row per axis, 4 cells, first `round N` match, verdict as a whole word in the segment up to `;`, Evidence cell
  must contain the round-N* spot-check path when it exists at R else `MANIFEST.json`, Score cell equals the newest
  closure's per-axis stated score (second cell, or the `Score N → M` target). All clauses match the docstring.
- C1 (B) shonen: `check_pins`/`parse_shonen` (`:217-288`) enforce >=4 boxes, >=2 pins, backticked
  `python3 <relative> --selftest` + `(N/M)` or `→ PREFIX pass=N fail=K`, regular file mode 100644/100755 (never
  symlink), run in a `git archive` of R under scratch with TMPDIR in scratch, receipt row present under
  `evidence/selftests/<stem>.txt` at R, no other tally token (`hidden`), floors.
- C1 (C) living pins: `check_living` (`:322-365`) enumerates single-line pins in `corpus/QUALITY.md` and
  `corpus/README.md` only, checks every pin present at entering tip E survives byte-for-byte at R (appended, never
  rewritten), and marks a pin good (shlex-parses as python3|bash, regular path, rc=0, matching tally) or superseded
  (QUALITY later numbered criterion `supersedes N's check`, or a later line carrying the stale span verbatim with
  `supersedes`). The one-line "quotation next to its replacement" rule is implemented at `:337-341` and is exactly
  what the pre-freeze note (contract lines 135-137) describes.
- C1 (D) locators: `check_locators` (`:368-413`) — see Finding F1 for the one scope gap.
- C2 entry/table/rows/quotes/pins/provenance: `evaluate` (`count-c2.py:159-269`) mirrors the docstring: header
  cells claim|source|quote, >=12 rows, claim >=6 words/unique/>=3 words beyond the quote, S-id row mined/opened
  2026-10-26/URL among the five frozen copies/used-by lists the entry, quote = one backticked span of 6-25 words,
  unique, whitespace-collapsed occurrence in the committed copy, all 5 sources drawn, committed copies match frozen
  sha256, provenance requires source:/verified-at:/recheck: and cites the table ids.
- C2 entailment arm: `entail_votes` (`:128-149`) reads only `w1/Mo52Ent01..12.md`, only unfenced lines, only
  `ENTAIL <12hex> entailed|overclaim` / `REPLACE <12hex> :: <text>`; author exclusion by hash of the REPLACE text;
  >=2 distinct non-author voters per row; any overclaim => dissent. Exactly the docstring's hardened arm.
- Receipt labels: the output line format (`C1=met|unmet items=…`, `C2=met|unmet claims=…`) is identical in the
  docstrings, the code and every receipt; exit 0/1 mapping matches (`count-c1.py:579`, `count-c2.py:319`).

Selftests re-ran and reproduced the frozen receipts exactly: `C1_SELFTEST pass=42 fail=0` and
`C2_SELFTEST pass=45 fail=0` (byte-identical PASS lists; only the `$ python3 …` header line differs).

## 3. Before-values == receipts

- C1 before (contract lines 35-39) vs `evidence/control-c1-do-nothing.txt`: re-ran
  `count-c1.py 4f266ef2… --repo <scratch clone> --fleet-repo /home/vgpnk/Projects/shokunin --scratch …` and
  reproduced every `item` line and `C1=unmet items=37 axes=6 pins=2 boxes=4 living=4 superseded=1 locators=25
  mismatches=8 errors=0 hidden=0 lane_writes=0 … failed=mismatch` byte-for-byte. The eight mismatches in the
  receipt are exactly the eight the contract lists: operability `round=47,evidence_missing:…round-51…` (should be
  51), depth `round=50,evidence_missing:…round-51…`, two SHONEN pins `receipt_missing`, `QUALITY.md:909` and
  `README.md:608` `expect=pass=12_fail=0 … got=…pass=22_…`, `README.md:607` `unrunnable` (bare `--selftest`),
  `SCORECARD.md:1771` `expect=pair:5_→_6 got=absent`.
- C2 before (contract line 72-73) vs `evidence/control-c2-do-nothing.txt`: reproduced
  `C2=unmet claims=0 … pins=bad … failed=entry_absent,pins` exactly.
- Entering scores (contract line 11): extracted the `## Axes` table at `4f266ef2…` — coverage 6, operability 7,
  depth 5, freshness 5, calibration 5, adjacency 6. Exactly the contract's list. The newest closure (round 51,
  `corpus/lessons/round-51-verifier-spotcheck.md:130-135`) states the same scores (6/7/5/5/5/6), which is what the
  Score arm trusts.
- Manifest targets: replicated `manifest_targets` against `MANIFEST.json` at the pinned fleet rev
  `f0b61b4…` — {coverage:(47,improved), operability:(51,improved), depth:(51,improved), freshness:(28,improved),
  calibration:(50,improved), adjacency:(19,improved)}, and `sha256(MANIFEST.json)[:12]=6209bdb8e400`, matching
  every receipt's `manifest=6209bdb8e400`.

## 4. Target-after == receipts

- `evidence/c1-at-data.txt` reproduced at `8524904…` from a scratch clone: identical item lines,
  `C1=met items=42 axes=6 pins=2 boxes=4 living=7 superseded=4 locators=27 mismatches=0 errors=0 hidden=0
  lane_writes=0 …`, exit 0. So the C1 kill rule is not triggered.
- `evidence/c2-at-data.txt` reproduced: `C2=unmet claims=28 located=28 quote_missing=0 bad_rows=0 sources=5
  source_rows=ok pins=ok provenance=ok entailed=0 dissent=0 … failed=entailment`, exit 1 — exactly the "data
  commit before any vote reads failed=entailment" gate (contract lines 76-77).
- `evidence/c2-hashes-at-data.txt` reproduced: all 28 `row=N hash=… claim=…` lines identical.

## 5. Controls really skip the claimed work

I re-ran all eight controls with the frozen `controls/c1-data.py` (parts exactly as in
`controls/c1-controls.py:17-25`) in fresh `--no-local` scratch clones at E, committing each control, and running
the frozen counter against each control commit. Every control re-run reproduced the frozen receipt's item lines
and C1= line exactly (the only difference anywhere is the control-commit rev hash, which is timestamp-dependent):
do-nothing items=37 mm=8; axes-only items=39 mm=5 (receipts+living still open); receipts-only items=37 mm=6
(axes+living+locator open); living-only items=40 living=7 superseded=4 mm=5; rewrite-in-place items=42 mm=3 with
`pin_removed_or_rewritten` x3; delete-stale-pins items=39 living=1 mm=3; repeat-stale-tally items=42 mm=3
(`pass=12 fail=0` superseding lines run and fail); witness items=42 mm=0. The contract table (lines 124-137)
therefore matches the receipts, which match reproduction. No control alone reaches met; only the all-parts witness
does — precisely the claimed arm isolation.

## 6. Causal separability

Two scratch clones at `8524904…`:
- sepA: reverted the whole C2 surface (entry, `corpus/SOURCES.md` restored to E, `corpus/evidence/sources-r52/`
  removed) and committed. `count-c1.py` at that commit: `C1=met items=42 … mismatches=0 …` — identical to
  `c1-at-data.txt`. C1 is unaffected by C2's data.
- sepB: reverted the whole C1 surface (`SCORECARD.md`, `SHONEN.md`, `corpus/QUALITY.md`, `corpus/README.md`
  restored to E, `evidence/selftests/` receipts removed) and committed. `count-c2.py` at that commit:
  `C2=unmet claims=28 located=28 … failed=entailment` — identical to `c2-at-data.txt`. C2 is unaffected by C1's
  data.
Code-level cross-reads are absent (`count-c1.py` reads no knowledge entry/SOURCES/copy bytes; `count-c2.py` reads
no SCORECARD/SHONEN/QUALITY/README byte). The contract's separability section (lines 87-92) holds.

## 7. Named limits are honest

- "a pin split across lines is not enumerated" — LPIN/PIN regexes cannot match across `\n`; selftest
  `multiline_span_not_enumerated` covers it.
- "a matching tally proves the instrument prints it today, not that its arms are good" — the counter actually runs
  the pinned command at R.
- "locator arm checks quoted strings and proposed A → B pairs only" — code `:400-412`.
- "Score arm trusts the newest closure's per-axis table" — `closure_scores` `:147-170`.
- "lane_writes sees only paths git status --ignored lists (not .git/)" — `status()` uses
  `--porcelain --ignored --untracked-files=all`; a `.git/` write is indeed invisible.
- "pinned commands run unsandboxed in an archive of R" — `run()` `:534-560` executes in the extracted archive
  with TMPDIR under scratch.
- C2 limits (contract lines 82-85): located quote proves occurrence; two entailed votes prove two ENTAILMENT seats
  recorded it for that exact text (seats are the lane, LEARNING.md — committed reviewer step, not outside
  verification); REPLACE is the only authorship signal; v7.2 bytes say nothing about other kernels/host sysctls.
  All match the code and docstring.

## Findings

F1 (LOW) — locator arm scope is narrower than the P-C1 docstring.
Contract line 30 references the docstring verbatim; docstring (D) (`count-c1.py:32-33`) says "every backticked
`path:N[-M]` in the six Axes rows and the SHONEN boxes…". Implementation `check_locators` (`count-c1.py:370-377`)
collects only cells `r[2:]` (Evidence and Last-change) of the Axes rows:
`if r and r[0].strip("* ").lower() in AXES: texts.extend(r[2:])`. A `path:N` in an axis-name or Score cell would
not be checked. No current row has one (axis names are bare words; scores are integers), so no receipt is
affected; the named limits do not list this scope reduction. Smallest safe correction: extend the scan to all four
cells (or amend the docstring), for round 53.

F2 (LOW) — the landed data is not byte-identical to the frozen `controls/c1-data.py` all-parts output, but the
difference touches nothing the counter reads. I reproduced the witness in a scratch clone at E (`axes,locator,
receipts,living`) and diffed against `8524904…`: `corpus/QUALITY.md` and `corpus/README.md` are byte-identical;
`evidence/selftests/*` differ only in the embedded `$ cd <lane checkout at …>` rev line (data records the freeze
commit `d3a8ea…`, the clone records the control/E rev — both are the rev of the checkout the tools ran in,
contract line 133's reading is unaffected); `SCORECARD.md` differs in exactly three places outside the `## Axes`
table where the frozen `axes()` prefix match (`controls/c1-data.py:73-84`, `l.startswith("| operability | 7 |")`)
also fires: the "Active score/Round17 role" table (~line 1080), the round-50 correction table (~line 1227) and the
"Old/New" corrected-text block (~line 1674). The landed data edits only the `## Axes` rows (plus the freshness
locator 1771→1781). Both the data and the reproduced witness yield `C1=met items=42`, so the claim, the control
readings and the data landing all stand; this is a reproducibility nuance, not a predicate violation (contract line
44 labels the witness feasibility-only, disclosed). For round 53: make `axes()` target the `## Axes` table only,
or document that data is a subset of the applier.

F3 (LOW) — the sweep receipt does not record a literal `$` command line. Contract items 7 (lines 21-22) says
"every receipt records its literal command line"; `evidence/sweep-overcommit.txt` opens with a prose description
(`# sweep at 4f266ef2 over … (git grep -l -F, files per term)`) and no verbatim shell invocation. All other round-
52 receipts (controls, at-data, hashes, selftests, census) do record their literal command. The count output
itself is reproduced by the contract (§3) and the freeze bytes are verified, so this is a documentation-form gap.

No HIGH or MED findings: the predicates, counters, receipts, before/after values, control isolations, kill-rule
exits and separability all check out against the frozen bytes at `d3a8ea…` and the landed data at `8524904…`.
