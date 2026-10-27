# Mo57Scribe51 — C1 field-mutation audit (round 57, w1)

Seat: Mo57Scribe51 (scribe/mutation). Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin`.
Entering revision `53e2b4768af93dd2472eb26ecc9b9fdca2e9daf2`; measured lane HEAD
`618562c72a03dc4d17386b715357f863fd327274` (freeze). No lane file was modified; `git status`
shows only pre-existing untracked round-57 plumbing (`build-w1-spec.py`, `w1-*.json`, `w1.ready*`,
`w1/`). Report only; no product edits, no commits, no remediation.

## 1. What I tested

Frozen C1 predicate — `.ufo/waves/round-57/contract.md:5`:

> the current SCORECARD capabilities table has two rows naming `driver-liveness` and `vote-binding`,
> each with a resolvable round-56 evidence pointer and first-working round 56.

Frozen counter — `.ufo/waves/round-57/count-c1.py`, sha256
`7156fb4bb29f27881091b22dfa7ef3d661b1e955a1ec9a4d13e48013f1b368ec`:

- `:7` the only read is `git -C repo show <R>:SCORECARD.md` (single `subprocess` call; no `open`,
  no `git cat-file`, no access to any evidence path);
- `:10` slice = text after the **first** `## Capabilities` up to the first `## Saturation`;
- `:11` row set = lines starting `|` containing the literal substring `driver-liveness` **or**
  `vote-binding`;
- `:12` pass = `len(rows) == 2` **and** every row contains `.ufo/waves/round-56/` **and** `| 56 |`
  somewhere on the line;
- `:13–14` prints `C1=met|unmet rows=N evidence=ok|bad rev=R`, exit 0/1.

Mutation method: each named field (name, evidence path, first-working round) was mutated in the
real SCORECARD byte image, one field at a time, and the frozen predicate was re-run over the
mutated commit. The predicate file was copied to scratch with **exactly one line changed** (its
hardcoded `repo =` path, `:6`) so the row/slice/lexeme logic is byte-identical; the diff is
recorded below. Base bytes are `618562c7:SCORECARD.md` (`sha256
c2c40693c30987e27e1ff9bcd92d50c430ff5fbd6ec46e7c655ceeaa1abe452f`, 280630 bytes, 2905 lines).

Equivalence gate: the patched counter on a fixture commit whose SCORECARD is **byte-identical** to
the lane's freeze SCORECARD prints `C1=unmet rows=0 evidence=bad` (rc 1), and the frozen counter on
lane rev `618562c7` prints the same tokens with `rev=` stripped (`tokens_equal=True`).

```
--- .ufo/waves/round-57/count-c1.py
+++ /fast/scratch/hyaku/mori-r57/Mo57Scribe51/count-c1-fixture.py
@@ -3,7 +3,7 @@
-repo = "/home/vgpnk/Projects/shokunin/mori-shokunin"
+repo = "/fast/scratch/hyaku/mori-r57/Mo57Scribe51/fixture-repo"
```

Baseline observation (lane, new): `python3 .ufo/waves/round-57/count-c1.py
618562c72a03dc4d17386b715357f863fd327274` → `C1=unmet rows=0 evidence=bad rev=618562c7…`, rc 1.
The frozen control at the entering tip reads the same tokens (`.ufo/waves/round-57/controls.txt:2-4`).
The lives slice is `SCORECARD.md:596-603` at HEAD: `## Capabilities` (596), header (598), separator
(599), `| — none yet — | | | |` (600), prose (602), `## Saturation` (604). A second `## Capabilities`
exists at `SCORECARD.md:1951` and `## Capabilities (round 12 demonstrations)` / `## Saturation
(declared round 12)` at 637/647 — all outside the slice.

## 2. Mutation matrix (measured)

Nine mutations of the three contract-named fields are **accepted** (`C1=met`, rc 0) although the
field no longer satisfies the contract sentence. Eleven mutations are rejected.

### 2.1 Accepted mutants (counterexamples)

| # | Field mutated | Mutant row(s) | Counter reading |
|---|---|---|---|
| A1 | name | `\| driver-liveness-probe \|`, `\| vote-binding-v2 \|` | `C1=met rows=2 evidence=ok`, rc 0, fixture `83d261e0` |
| A2 | name | `\| not-driver-liveness \|`, `\| no-vote-binding \|` | `C1=met rows=2 evidence=ok`, rc 0, `d49025eb` |
| A3 | name (cell) | names are `live census` and `silence oracle`; tokens appear only in the *description* cells | `C1=met rows=2 evidence=ok`, rc 0, `bf4b0553` |
| A4 | name (markup) | `\| **driver-liveness** \|`, `` \| `vote-binding` \| `` | `C1=met rows=2 evidence=ok`, rc 0, `412f1beb` |
| A5 | evidence path | `.ufo/waves/round-56/evidence/DOES-NOT-EXIST.txt`, `.ufo/waves/round-56/NOPE/absent.md` | `C1=met rows=2 evidence=ok`, rc 0, `9803594c` |
| A6 | evidence path | bare directory `` `.ufo/waves/round-56/` `` (no file named) | `C1=met rows=2 evidence=ok`, rc 0, `e173a278` |
| A7 | evidence path | r56 path in the *description* cell; Evidence cell = `` `corpus/knowledge/driver-liveness-r56.md` `` | `C1=met rows=2 evidence=ok`, rc 0, `b293f729` |
| A8 | first-working round | `\| 56 \|` placed in a description cell; First-working-round column = `57` | `C1=met rows=2 evidence=ok`, rc 0, `4c1f6d4f` |
| A9 | column count | five-column rows (extra cell appended) | `C1=met rows=2 evidence=ok`, rc 0, `8c2be5a5` |

Grounding for A5/A6 ("resolvable" is never checked): `git -C <lane> cat-file -e
HEAD:.ufo/waves/round-56/evidence/DOES-NOT-EXIST.txt` → exit 1 (absent) at `618562c7`, `53e2b476`
and `HEAD`, while the mutant still reads `C1=met`. The real pointer
`.ufo/waves/round-56/evidence/driver-liveness-live.txt` exists at all three revisions (exit 0), so A5
isolates the *resolution* arm rather than the token that the real row would use.

Rejected-but-valid formatting (false negative): a correctly populated row written as `|56|` (valid
markdown, no padding spaces) fails — `C1=unmet rows=2 evidence=bad`, rc 1, `98732458`.

### 2.2 Rejected mutants (predicate is not vacuous)

| # | Mutation | Reading |
|---|---|---|
| R1 | canonical two rows (witness) | `C1=met rows=2 evidence=ok`, rc 0, `c77b2bbb` — feasibility only, built by me in scratch |
| R2 | names upper-cased `Driver-Liveness` / `Vote-Binding` | `C1=unmet rows=1 evidence=bad`, rc 1, `5ab0be42` |
| R3 | token split by a space (`driver liveness`) | `unmet rows=1`, rc 1, `51ab655c` |
| R4 | one row points at `.ufo/waves/round-55/evidence/c1-at-landed.txt` | `unmet rows=2 evidence=bad`, rc 1, `a180532d` |
| R5 | evidence cells empty; path only in the prose line under the table | `unmet rows=2 evidence=bad`, rc 1, `3885da23` |
| R6 | First-working-round = `57` on one row | `unmet rows=2 evidence=bad`, rc 1, `fa8276bd` |
| R7 | one row names both tokens (`\| driver-liveness / vote-binding \|`) | `unmet rows=1`, rc 1, `1c13b198` — the `len(rows)==2` arm holds |
| R8 | duplicate third row | `unmet rows=3 evidence=bad`, rc 1, `3097505d` |
| R9 | the two rows placed in the round-12 capabilities table (`## Capabilities (round 12 demonstrations)`) | `unmet rows=0`, rc 1, `a407dccc` |
| R10 | rows placed only in the round-53 capability table below `## Saturation` | `unmet rows=0`, rc 1, `ef7ccf48` |
| R11 | tokens on prose lines only, no `\|` row | `unmet rows=0`, rc 1, `56409691` |
| R12 | a `## Saturation` heading inserted between the two rows | `unmet rows=1`, rc 1, `2ed5a575` |

### 2.3 Slice-boundary mutants

| # | Mutation | Reading |
|---|---|---|
| B1 | first `## Saturation` line deleted (slice runs to the next one, 647) | `C1=met rows=2 evidence=ok`, rc 0, `06041a26` |
| B2 | that heading renamed `## Saturation note` | same, `C1=met`, rc 0, `c5ca2b7e` |
| B3 | every `## Saturation` heading removed → slice runs to EOF | `unmet rows=3 evidence=bad`, rc 1, `72c8149e`; third match is `SCORECARD.md:2903`, the round-56 claim row |
| B4 | first `## Capabilities` renamed → split lands on `## Capabilities (round 12 demonstrations)` (637) | `unmet rows=0 evidence=bad`, rc 1, `38660590` (no traceback) |

## 3. Findings

1. **The name column is not read.** Rows are selected by substring anywhere on the line
   (`count-c1.py:11`); a row whose first cell is `live census` passes when its description mentions
   `driver-liveness` (A3), a negated name passes (A2), and suffixes pass (A1).
2. **"Resolvable round-56 evidence pointer" is implemented as the literal substring
   `.ufo/waves/round-56/` on the row line** (`:12`). No path is opened or resolved; the counter makes
   exactly one `git show <R>:SCORECARD.md` call (`:7`). A pointer to a nonexistent file (A5) or to
   the bare directory (A6) satisfies it; a pointer in the wrong cell does too (A7). A pointer to a
   *different round* is rejected (R4) — so the arm discriminates on round, not on existence.
3. **"First-working round 56" is implemented as the lexeme `| 56 |` anywhere on the line** (A8: the
   round column can read 57 while a description cell carries `| 56 |`), while the legitimate
   unpadded form `|56|` is rejected (`98732458`). Same field has both a false-accept and a
   false-reject direction.
4. **Row count is exact (`== 2`)**, which correctly rejects one-row-both-names (R7) and duplicates
   (R8), but a stray third matching row anywhere in the slice flips the verdict to unmet (B3).
5. **Scope is heading-delimited**, not semantic: only text between the first `## Capabilities` and
   the first `## Saturation` is scanned. Rows added to any later capability table are invisible
   (R9, R10) — correct if "the capabilities table" means the top section only, and worth stating
   plainly because the SCORECARD has two `## Capabilities` headings (596, 1951) and two
   `## Saturation` headings (604, 647). Renaming or deleting the first `## Saturation` widens the
   slice (B1, B2) without changing the verdict for a clean data commit, but B3 shows the widened
   slice can import the round-56 claim row at `SCORECARD.md:2903`.
6. **The counter is non-vacuous on the shapes the contract's own example would take**: the canonical
   witness meets (R1); case, spacing, cross-round pointer, round 57, missing path on the row line,
   single-row-both, duplicate, and out-of-slice placements all stay unmet (R2–R12).
7. **C1 is currently unmet at the freeze** (`rows=0`, rc 1), consistent with the frozen entering
   control. Feasibility of the predicate — not C1 itself — is what R1 demonstrates; that witness was
   built by this seat in scratch and must not be read as the lane's claim.

## 4. Limits of this seat's evidence

- Mutations were run against a **copy** of the counter with only its hardcoded repo path changed;
  the predicate lines are byte-identical but the run is not literally the frozen file (the frozen
  file hardcodes the lane path and cannot read a fixture).
- The witness rows I wrote (R1) are mine; they are a feasibility fixture, not the round's data
  commit, and prove nothing about the lane's eventual rows.
- No mutation of `count-c2.py` was attempted; C2 is another seat's scope.
- `rev=` tokens in mutant readings are fixture commits, not lane revisions; only the baseline and
  the equivalence gate touch the lane.
- I did not fetch, re-open or judge any round-56 evidence file content; A5's "absent" claim rests on
  `git cat-file -e` at the three named lane revisions.
- Report-only seat: no remediation proposed in-lane, no counter rewritten (frozen bytes).

## 5. Gates and hygiene

- Lane repo untouched: no `git add/commit/jj`, no file writes outside this report; fixture work under
  `/fast/scratch/hyaku/mori-r57/Mo57Scribe51/fixture-repo`, with `git rev-parse --show-toplevel`
  asserted `== .../fixture-repo` at harness start (both harness scripts) before their commit runs.
- `scripts/hyaku/disk-guard.sh status` checked before work: `/fast` 27% used, 592 G free; no ENOSPC.
- `TMPDIR` set to the seat scratch; no tool installed or updated (so nothing to record); pacman not
  run; no subagents; no secrets or private URLs in this report.

## 6. Commands executed (verbatim, key ones)

```
python3 .ufo/waves/round-57/count-c1.py 618562c72a03dc4d17386b715357f863fd327274      # lane
python3 mutate_c1.py          # 19 field mutants, cwd = $HYAKU_SCRATCH/mori-r57/Mo57Scribe51
python3 mutate_c1_extra.py    # equivalence gate + 7 structural mutants
python3 -  <<'PY' …           # E8 (all Saturation headings removed) + cat-file pointer existence
python3 count-c1-fixture.py <fixture-rev>                                             # per case
```

## 7. Artifact paths

- Harness: `/fast/scratch/hyaku/mori-r57/Mo57Scribe51/mutate_c1.py`,
  `.../mutate_c1_extra.py`
- Patched predicate: `/fast/scratch/hyaku/mori-r57/Mo57Scribe51/count-c1-fixture.py`
  (sha256 `837359a7bfbb3671c359ea2ee52ce708885de0aadd6bef766423eb3c444717af`; one-line diff in §1)
- Fixture commits (28): `/fast/scratch/hyaku/mori-r57/Mo57Scribe51/fixture-repo` — case ids are the
  commit subjects (`git -C … log --oneline`) matched to the revs cited above.

## 8. Verdict

C1 at the freeze revision is **unmet** (`rows=0`, rc 1). The frozen counter rejects eleven
field-level mutations but accepts nine that break the contract sentence's three named fields —
name (`not-…`, suffixed, or tokens in a description cell with another name), evidence pointer
(nonexistent file, bare directory, wrong cell), and first-working round (`| 56 |` in a description
cell while the column says 57) — and rejects one legitimate formatting (`|56|`). Row-count, slice
placement and round-substring arms do discriminate.
