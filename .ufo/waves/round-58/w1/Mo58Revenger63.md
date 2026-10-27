# Mo58Revenger63 — C2 entry vs round-57 watchdog entry: duplication / overreach

Seat: revenger (leaf, no subagents). Scope: compare the proposed C2 depth entry
`corpus/knowledge/driver-events-r58.md` with `corpus/knowledge/watchdog-unclosed-r57.md`, with
line evidence; report duplicated claims or overreach, or an explicit no-counterexample result.
Detection only: no production, registry, SCORECARD, LOG, VCS or sibling-repo writes.

## Bytes analysed (pinned)

| Object | Value |
|---|---|
| Freeze rev | `fe8801120a67c1a6b8899d7d0423839caa09e7d0` (`git cat-file -e <rev>^{commit}` OK) |
| Entering rev | `b783d0b892637ce8d20f188cad20e4d8913ca635` (ancestor of freeze, verified) |
| `corpus/knowledge/driver-events-r58.md` (working tree, untracked) | sha256 `e7fc469cf4ffd86a6ba14e8b6e2f66ec6366e46f853b0733553ee414c81a9e55`, 19 lines, mtime 14:29:36 |
| `corpus/knowledge/watchdog-unclosed-r57.md` (committed) | sha256 `7d74c837c19c7be1fee72c9926403657c08865f1745b1c3ebe819bac29b98952`, 20 lines |
| `corpus/knowledge/driver-liveness-r56.md` (committed) | sha256 `ce438eeb42ac92b5ad9b4a2058d9256cb17b411db5d964c041e8c5caaa0866b2` |
| `tools/mori-driver-liveness.py` at `fe88011`, at `618562c7`, working tree, `corpus/evidence/sources-r57/`, `corpus/evidence/sources-r58/` | sha256 `6b3dba74c639190e7e96b6bed8e6ac8f285a51ce6d910fbe92e6dd39bf7be997` (all five agree) |

All measurements are read-only over `git show`/`git cat-file` of the lane plus throwaway fixtures
under `/fast/scratch/hyaku/mori-r58/Mo58Revenger63/` (each fixture `git init`-ed at that explicit
path; every git call `git -C <fixture>`; no commit outside the fixture). Receipt:
`.ufo/waves/round-58/w1/Mo58Revenger63-receipt.txt`.

## F1 — duplicate-claim finding is reachable only after a format blocker: with the entry's current bytes the frozen counter cannot count a single claim

- Frozen predicate: `count-c2.py:37` `KLINE = re.compile(r"^- \*\*K(\d+)\*\*.*\(tools/mori-driver-liveness\.py:(\d+)\)")`;
  `count-c2.py:11` states the shape as `'- **K<n>** ...'`; matching at `count-c2.py:80-89`; `claims < 8`
  → `failed=claims` (`:90-91`).
- The entry writes `- **K1 — unmatched timestamped prose is separate from a lane event.** …`
  (`driver-events-r58.md:10`; same shape at `:11-17`), i.e. bold closes after the title, not after `K<n>`.
- Reproduced on the entry's exact bytes (`e7fc469c…`) against the tool at the freeze rev in a scratch
  fixture whose SOURCES row is copied from `corpus/SOURCES.md:330`:

  ```
  [A verbatim-entry]        rc=1  C2=unmet claims=0 located=0 copy=ok tree=ok rows=ok sources=ok failed=claims
  [B format-only-fix]       rc=0  C2=met   claims=8 located=8 copy=ok tree=ok rows=ok sources=ok failed=none
  ```
  B changes only `- **K<n> — ` → `- **K<n>** — `; no prose, quote or line number changes.
- Consequence for this seat's question: as-is, the C2 "after" target (`contract.md:47`) is unreachable,
  so any duplicate-claim/overreach comparison is over a document whose own instrument scores it 0 claims.
  The frozen selftest never exercises this shape (`count-c2.py:127-135` `ENTRY_OK` uses `- **K{i}**`), and the
  contract's junk arms (`contract.md:49`) do not include a shape arm — so the selftest green does not
  cover the landed entry's format.
- Independent corroboration (not my finding): `Mo58Scribe49.md:42,47,52` and `Mo58Scribe50.md:70-80`
  report the same bold-placement blocker. My reproduction agrees byte-for-byte.

## F2 — duplicated claims: no quote-level duplication, total branch/content duplication

Quote-level (clean): r58 cites tool lines `96, 101, 103, 123, 135, 145, 152, 159`
(`driver-events-r58.md:10-17`); r57 cites `133, 143, 118, 150, 157, 162, 172, 173`
(`watchdog-unclosed-r57.md:11-18`). **Intersection is empty; 8/8 quotes are distinct lines, and all 8 are
genuine substrings of the cited line at `fe88011`** (verified by direct line comparison; also arm B `located=8`).

Content-level (duplicated):

| r58 claim | r58 line | Already-recorded equivalent |
|---|---|---|
| K3 launch rest grammar (:123) | 12 | `driver-liveness-r56.md:33-36` (launch rest variants, incl. "no rest at all") + r57 `:11` K1 (:133 launch effect) |
| K4 complete rest grammar (:135) | 13 | `driver-liveness-r56.md:37-39` + r57 `:12` K2 (:143 close) |
| K5 wrap rest grammar (:145) | 14 | `driver-liveness-r56.md:45-46` + r57 `:14` K4 (:150 close) |
| K6 dead rest grammar (:152) | 15 | `driver-liveness-r56.md:40-43` ("inner text … never parsed beyond the wrapper") + r57 `:15` K5 (:157 clear) |
| K7 launch-fail rest grammar (:159) | 16 | `driver-liveness-r56.md:44` (` :: reason`) + r57 `:16` K6 (:162 count) |
| K1 other_line (:101) | 10 | `driver-liveness-r56.md:47-48` |
| K8 bad first token (:96) | 17 | `driver-liveness-r56.md:48-50` |
| K2 five-group split (:103) | 11 | **new** — `LINE_RE.groups == 5` (imported tool, measured); no prior entry names the split |

So 7 of 8 r58 claims restate grammar already recorded at S544/S547 boundary (`driver-liveness-r56.md:28-50`),
and 5 of 8 are the same five event branches r57/S548 already mined from the effect side
(r57 rows `:11,12,14,15,16` vs r58 rows `:12-16`). The depth delta is line-addressability plus K2, not new
semantics — consistent with the entry's own `coverage-map:` ("deepens existing FR5 surface, no frontier
advance claimed", `driver-events-r58.md:4`) and with `corpus/README.md:807`.

Registry-level duplication: `SOURCES.md:328` (S548) and `SOURCES.md:330` (S550) name the *same* sha256
`6b3dba74…`, and `corpus/evidence/sources-r58/mori-driver-liveness.py` is byte-identical to
`corpus/evidence/sources-r57/mori-driver-liveness.py` — a second row and a second copy of unchanged bytes.

Verdict on F2: **duplicated claims — established for content (7/8) and for the branch inventory (5/5); not
established for quote text (0/8)**. No written anti-duplication rule was found in `corpus/QUALITY.md` or
`corpus/README.md`, and the contract explicitly concedes "no frontier advance"; confidence: high on the
mapping, medium on calling it a defect.

## F3 — overreach: one claim stronger than its quote, one precision gap

1. **K7 overclaims** (`driver-events-r58.md:16`): "launch-fail validates the diagnostic separator **and reason
   shape**." The cited/underlying regex is `LAUNCHFAIL_RE = re.compile(r"^ :: (.*)$")` (`tools/mori-driver-liveness.py:61`).
   Measured on the imported module: `LAUNCHFAIL_RE.match(' :: ')` → `True` (empty reason accepted) and
   `LAUNCHFAIL_RE.match(' :: boom')` → `True`. Only the separator is validated; the reason is unconstrained
   `.*`, so "reason shape" is not in the bytes. The earlier entry states it correctly: `driver-liveness-r56.md:44`
   "` :: reason`" (no shape claim). Removal of the two words makes the claim exactly quote-carried.
2. **K3 precision gap, not overreach** (`:12`): "Launch processing … `LAUNCH_REST_RE` … a rejected rest is sent
   through the malformed path" — true, but `LAUNCH_REST_RE.match('')` → `True` (`:56-58`, trailing `)?$`), so
   "has its own suffix grammar" coexists with an accepted empty rest. `driver-liveness-r56.md:34-35` names that
   ("or no rest at all"); the r58 claim does not. Not false, incomplete.
3. **Entry prose overreaches its own provenance** (`:8`): "the exact round-56 lane tool copy opened this round
   **and committed at** `corpus/evidence/sources-r58/mori-driver-liveness.py`; the copy and
   `tools/mori-driver-liveness.py` are byte-identical **at the measured revision**." Measured:
   `git log --all -- corpus/evidence/sources-r58/` prints nothing; `git cat-file -e fe88011:corpus/evidence/sources-r58/mori-driver-liveness.py`
   and the same for `corpus/knowledge/driver-events-r58.md` both fail; `git status --porcelain` shows both as
   `??` untracked. No revision carries the pair yet, so "committed"/"at the measured revision" is unsupported
   at `b783d0b8` and `fe88011` (at `fe88011` the frozen counter prints `C2=unmet entry=absent`, matching
   `.ufo/waves/round-58/evidence/controls.txt`). This is the practice `corpus/QUALITY.md` criterion 9 forbids
   ("Every path, line or commit pointer resolves at the carrying commit"); note the same pattern already exists
   at S548: `SOURCES.md:328` pins `618562c7…`, where `corpus/evidence/sources-r57/mori-driver-liveness.py` also
   does not resolve (it first exists at `fe88011`; `git cat-file -e` fail/OK measured). So r58 repeats the r57
   imprecision rather than fixing it — observation, not a new class of defect.
4. Minor: `recheck:` is the literal placeholder `python3 .ufo/waves/round-58/count-c2.py R` (`:3`) against r57's
   runnable `cmp tools/… corpus/evidence/sources-r57/…` (`watchdog-unclosed-r57.md:3`). The counter accepts any
   `recheck:` string (`count-c2.py:61`), so this passes mechanically while naming no reproducible command.

## F4 — the frozen instrument cannot see F2 or F3 (mutation arms, scratch fixtures)

Fixtures: tool bytes = freeze-rev tool, copy = same bytes, SOURCES row = `corpus/SOURCES.md:330`, frozen
`measure()` invoked from the delivered `count-c2.py` with `LANE` pointed at the fixture.

| Arm | Mutation | Output | Reading |
|---|---|---|---|
| C | K7 claim text replaced by "launch-fail proves the lane died and the provider is gone" (quote unchanged) | `C2=met claims=8 located=8 …` | claim prose is never read; an overclaim scores met |
| D | K7 quote replaced by fabricated text plus a separate genuine span `` `LAUNCHFAIL_RE` `` | `C2=met claims=8 located=8 …` | `count-c2.py:86-88` accepts **any** span ≥ 12 chars; the full quoted sentence need not match |
| E | r58 K3 quote replaced by r57 K1's genuine-but-wrong-line quote `` `row["open_launches"].append(key)` `` | `C2=met claims=8 located=8 …` | cross-entry quote transplant undetected (same token loophole: `LAUNCH_REST_RE` is 14 chars) |
| H | entry body replaced by the r57 restatement only (8 bullets, r57's own quotes/lines) | `C2=met claims=8 located=8 …` | pure duplication of r57 content scores met |
| G | `source:`/`verified-at:`/`recheck:` lines removed from frontmatter and mentioned in the body | `C2=met … sources=ok` | `count-c2.py:61-65` is a whole-text substring test, not a frontmatter test |
| F | eight claim-free bullets with fabricated spans | `C2=unmet claims=8 located=0 … failed=quotes` | the contract's junk arm (a) does fire |

Lane rule this collides with: `corpus/QUALITY.md` criterion 128 ("the counter proves location, not
entailment"; the round-47/48 reproductions), criterion 140 (a depth claim carries a committed entailment vote
per row; "location proves the quoted words exist, not that the claim follows"), criterion 143 (two non-author
`entailed` votes; an `overclaim` blocks the row until its text is replaced). The frozen r58 counter has **no**
entailment/hash arm (no `--hashes`, no `ENTAIL` scan), and `contract.md:47-52` names none, so under the lane's
own bar C2 can be `met` while K7's overclaim stands — the round-50 failure mode (counter met, six claims not
carried by their quotes) is reproducible on this instrument (arm C).

## Clean sub-results (falsification attempts that found nothing)

- All 8 r58 quotes are exact substrings of the cited line at `fe88011` (lines 96, 101, 103, 123, 135, 145, 152,
  159); no off-by-one, no wrong-line citation, no normalized hyphenation (contrast the r57 S549 observation).
- `copy` identity holds three ways: copy-at-`R` == tool-at-`R` == tool-at-`fe88011` == tool-at-`618562c7`
  (sha256 `6b3dba74…`), so the `copy=ok tree=ok` arms are honest, not merely equal by accident of two wrong bytes.
- K2's "five parsed fields" is literally true: `LINE_RE.groups == 5` (imported module, measured).
- K5 (`WRAP_REST_RE`), K6 (`DEAD_REST_RE` = `^; retry same round(?: \((.*)\))?$`), K8 (`:96` then `_bad`) are
  statement-supported by the bytes; no overreach beyond wording found in rows K1, K2, K5, K6, K8.
- The contract's per-row registry requirements hold on the bytes: `SOURCES.md:330` has `status` cell `mined`
  and `used-by` cell exactly `corpus/knowledge/driver-events-r58.md` (cells 8 and 11 of the split), and the
  §2b Gate quote exists and is byte-faithful in the search log (`SOURCES.md:388`).
- No textual reuse of r57's table rows: r57 is a `| K<n> |` table, r58 is a bullet list; the borrowed content is
  the branch set and r56's grammar, not r57's sentence text.

## Findings summary (for the wave)

1. **Blocker (corroborates two scribe seats):** entry bytes as written → `C2=unmet claims=0 failed=claims`;
   the C2 target requires `- **K<n>** …`. Independent of any duplication question.
2. **Duplication:** 7/8 claims restate `driver-liveness-r56.md:28-50`; 5/8 are r57's five branches from the
   grammar side; only K2 (:103) is new; S550 is a second registry ID and second copy of unchanged bytes
   already under S548. Not a rule violation found — the contract concedes no frontier advance.
3. **Overreach:** K7 "reason shape" is not carried by `LAUNCHFAIL_RE = ^ :: (.*)$` (empty reason accepted);
   entry:8's "committed … at the measured revision" does not resolve at `b783d0b8`/`fe88011` (no ref carries
   the pair), repeating the S548-style revision pin; `recheck:` is a placeholder.
4. **Instrument gap:** location-only predicate passes fabricated quote text (D), transplanted quotes (E),
   pure r57 restatement (H), body-only frontmatter (G) and overclaiming prose (C) — the lane's own criteria
   128/140/143 put that burden on entailment votes, which this counter does not collect.

No production edit, no registry/SCORECARD/LOG change, no lane VCS mutation, no fleet/sibling write. Scratch
`/fast/scratch/hyaku/mori-r58/Mo58Revenger63/` (fixtures only, <1 MB) cleaned after the receipt was copied.
Tool installs: none (no pacman, no remote scripts).
