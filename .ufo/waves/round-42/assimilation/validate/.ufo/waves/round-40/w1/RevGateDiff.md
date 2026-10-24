# RevGateDiff — C2 gate-v3 diff review (P-C11), mori round 40 w1

Seat: reviewer (read-only; no production edits). Lane:
`/home/vgpnk/Projects/shokunin/mori-shokunin`.
Diff under review: `git diff bb1f2457 265a955cc -- tools/mori-sources-appendonly.py`
(1 file, +149/−48). Reviewed bytes: gate blob sha256
`bde5a9a34c7eb3bcbee39d669b8d187caeb51807ad1bdcd85a05c1bcd06777ec`, equal to the
worktree file, to `git show 265a955cc:tools/mori-sources-appendonly.py`, and to the
`freeze-r40.txt` pin.

No LSP server exists on this host (`pylsp`, `pyright` absent), so definition/reference
checks used reads plus `pyflakes` (clean, exit 0) and `ruff`; this is recorded as a
fallback, not semantic proof from a language server.

## Hunk-by-hunk classification

| # | Diff hunk | Final-file lines | Class | Notes |
|---|---|---|---|---|
| H1 | `@@ -69,27 +69,31 @@` | 76–96 | **(e) predicate text** | `P-C9`→`P-C11`; byte-equal to the contract's P-C11 blockquote (`EQUAL True`, both 1036 chars). Carries a false count — F1. |
| H2 | `@@ -154,28 +158,16 @@` | 158–165 | **(b) first-parent** | deletes `nearest_path_commit`. No remaining reference in `tools/` at the tip or HEAD (`git grep -c nearest_path_commit HEAD -- tools/` → exit 1); pyflakes clean. Leaves a dangling knowledge anchor — F4. |
| H3 | `@@ -239,22 +231,29 @@` | 234–252 | **(e) doc text** | version-3 docstring; accurately describes (a)/(b)/(c). |
| H4 | `@@ -279,16 +278,17 @@` | 286 | **(a) eligible set** | adds `first_commit` map. |
| H5 | `@@ -296,65 +296,78 @@` | 303–365 | **(b)+(c)+(a)** | first-parent-only `ref` (311–322, incl. `git_blob(head:path)` fallback), re-add branch removed (333–335), eligible set `tip`-bounded (348–354), `last_edit or first_commit` (363–365). Behavior verified below. Widens a second printed field — F2. |
| H6 | `@@ -541,37 +554,86 @@` | 560–600 | **(d) fixture/selftest** | dag-n/dag-p/dag-r bodies and hand-written expectations. Comment inaccuracy — F5. |
| H7 | `@@ -591,16 +653,55 @@` | 626–710 | **(d) fixture/selftest** | `_make_dag_repo` kinds N/P/R and body unpacking. No fixture exercises the not-in-walk first-parent fallback (the lane exercises it 43/55 times). |
| H8 | `@@ -784,17 +885,17 @@` | 891 | **(e) other** | argparse help string `P-C9`→`P-C11`. Cosmetic. |

No hunk is unclassifiable. No hunk changes behavior beyond P-C11's words except the
summary-field widening in F2 (and the stale documentation in F3/F4, which are omissions,
not behavior changes).

## Findings (by severity)

### F1 — HIGH (claim text vs measured bytes): the frozen count is wrong; the gate prints a predicate that contradicts its own output

- The frozen P-C11 says `S226 joins superseded_as_of (19 ids) at the landed tip`
  (`tools/mori-sources-appendonly.py:86`; `contract.md:137`). The assignment claim says
  the tip line "carries 34 as-of ids including S226". **Measured at the scored tip
  `265a955cc`: 35 as-of ids, `stale_supersede=[]`.**
- Evidence, all mutually identical:
  - `evidence/c11-after-lane.txt` line 22: `superseded_as_of` has **35** entries
    (S041,S044,S051,S062,S064,S067,S069,S070,S071,S083,S084,S090,S093,S096,S097,S101,
    S124,S127,S128,S129,S131,S140,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,
    S190,S193,S226).
  - My live run `python3 tools/mori-sources-appendonly.py 265a955cc --repo .` is
    **line-identical** to that receipt (`IDENTICAL True`, both 21 lines).
  - Independent re-derivation from `git show 265a955cc:corpus/SOURCES.md` (not using the
    gate): 229 rows; 35 distinct `supersedes S###` targets are present at the tip. Same
    35-id set.
- The eligible-set extension is therefore **17 ids, not 1 and not 16**:
  `S067,S070,S071,S083,S084,S090,S093,S096,S097,S101,S124,S127,S128,S129,S131,S140,S226`
  (18 → 35; `lost as-of: []`). The only "19" in the receipts is v2's 18 + S226; the only
  "34" is `e37dcc6`'s total eligible set (33 as-of + `stale=[S069]`), which the
  assignment appears to have carried to the tip.
- Consequence for admission: C2's acceptance sentence is not met as written, and the
  kill rule — "a gate keeping the edit-bounded eligible set still omits S226 → the lane
  line mismatches the declared 19 ids" — would reject the **honest** gate, because the
  honest gate prints 35. The wave plan repeats the bad number and will make sibling
  seats report FAIL: `evidence/wave-plan.txt:468` ("lists 34 as-of ids including S226"),
  `:543` ("measured 34-id lane line"), `:703`/`:708` ("34 as-of ids", "measured value is
  34", "the 16 never-edited superseded ids"), also `w1-spec.json:5,35,270,275`.
- The **code is faithful to P-C11's rule sentence** ("every superseded id present at R")
  and to the receipt; do not change the code to print 19/34. The defect is the frozen
  claim's arithmetic. Fix by a new claim version / erratum declaring 35 (17 joins), or
  remove the parenthetical count from the predicate; either way the wave-plan prompts
  that assert 34 must be corrected, or every seat attacking them fails on a false
  premise.

### F2 — MEDIUM (behavior beyond P-C11's words): the `appendonly_violations` summary's `superseded=[...]` field also widens

- P-C11 assigns the enlarged eligible set to the **timing line** only. But
  `superseded` (line 354) feeds both the timing line and the summary line
  (`report()` at 410). Measured: summary `superseded=` is 18 ids before and **35** at
  the tip (and 34 at `e37dcc6` in v3 vs 18 in v2).
- The contract's After declaration names only `supersede_timing ...`; the claim never
  states that the summary field changes, and the module docstring still defines
  `superseded` as a subset of `ids` (F3). The receipts show the widening honestly, so
  this is an undeclared observable, not a hidden one. Either name it in the claim or
  keep the summary list edit-bounded and use the wide set only for the timing test.

### F3 — MEDIUM (stale in-file contract): module docstring still says `superseded` ⊆ `ids`

- `tools/mori-sources-appendonly.py:21-22`: "superseded — ids in `ids` for which a row
  present at `<rev>` has a `teaches` cell opening `supersedes S###`." False for v3: at
  the tip, 35 ids are superseded and only 18 are in `ids`.
- Line 28-30 similarly defines `superseded_as_of` only via "last immutable-cell edit
  commit", omitting the new first-sighting fallback for never-edited ids.
- This file is the tool's own usage contract; the (a) hunk changed the semantics without
  updating it.

### F4 — MEDIUM (in-repo binding broken): `corpus/knowledge/gate-ancestry-r39.md` is left stale and its anchor no longer resolves

- The page's recheck clause (lines 12–13) fires on exactly this diff: "recheck: on the
  next change to tools/mori-sources-appendonly.py's walk, edit detection or timing code,
  and with the S227 cadence." The diff changes edit detection and timing and deletes the
  helper the page documents.
- Lines 41–53 still present "The round-39 semantics (gate P-C9)" and the resolution
  "through `nearest_path_commit` for parents that do not touch the registry".
- The page's `anchor:` line 44 (`nearest_path_commit(repo, parent, path)`) now has **zero
  occurrences** in the named tool at `265a955cc` and at HEAD (only round-39/40 history
  and the extracted v2 fixture still contain the string), so a QUALITY-108-style
  resolvability check over this knowledge entry fails at R. The page was not touched in
  the 29-file tip commit (SKILL.md was updated; this page was not).
- `corpus/README.md:606` and `corpus/QUALITY.md:909/112` also still cite P-C9/`pass=12`;
  those are append-only historical criterion rows, so they are lower priority than the
  recheckable knowledge page, but a reader of the row now sees a false live description.

### F5 — LOW (comment/receipt accuracy): the dag-r comment's v2 before-picture is not what the frozen v2 bytes print

- `tools/mori-sources-appendonly.py:586` says of dag-r: "The round-39 gate re-flags the
  re-add as the last edit and prints stale." The frozen v2 receipt
  (`evidence/c11-red-readd.txt`) prints `superseded_as_of=[] stale_supersede=[]` (no
  stale), because v2's edit-bounded eligible set excludes S008; the re-add edit is only
  internal. Contract C2's Before likewise says v2 "prints a `changed` event for the
  linear delete-then-re-add"; the receipt has no `changed S008` line — its
  `round_changed=[S008]` comes from the **deletion** and is identical under v3.
- The fixture and kill rule are nonetheless sound: my probe of v3's eligible set with
  the v2 re-add branch reinstated prints `stale_supersede=[S008]` on dag-r (fixture
  fails), while dag-n/dag-p stay green. So the fixture isolates (c) only in combination
  with (a) — the comment should say that, not attribute a `stale` verdict to the v2
  bytes.

### F6 — LOW (contract wording): dag-p's "fabricated changed line"

- Contract C2 Before says v2 "fabricates a `changed` line plus a stale verdict" on the
  first-parent-lacks-path merge. The receipt prints `changed S001 superseded_by=S002`
  under **both** v2 and v3, because S001 genuinely differs from its first-sighting cells
  at the side-branch edit. The fabricated part is the merge-commit edit, observable only
  as `stale_supersede=[S001]` (v2) vs `superseded_as_of=[S001]` (v3). The verdict-level
  description is right; the "changed line" phrasing is not.

## Verification performed (commands and outputs)

All commands from `/home/vgpnk/Projects/shokunin/mori-shokunin` unless noted.

1. `git diff --stat bb1f2457 265a955cc -- tools/mori-sources-appendonly.py`
   → `1 file changed, 149 insertions(+), 48 deletions(-)`.
2. `sha256sum tools/mori-sources-appendonly.py` and
   `git show 265a955cc:tools/mori-sources-appendonly.py | sha256sum`
   → both `bde5a9a3…06777ec`; `freeze-r40.txt` pins the same.
3. `python3 tools/mori-sources-appendonly.py --print-predicate`, compared
   programmatically to the contract's P-C11 blockquote → `EQUAL True` (1036 chars).
4. `python3 tools/mori-sources-appendonly.py --selftest`
   → `MORI_SOURCES_APPENDONLY_SELFTEST pass=15 fail=0`, `EXIT=0`.
5. `python3 tools/mori-sources-appendonly.py 265a955cc --repo .`
   → 18 `changed` lines, exit 1; summary `ids=[18]`, `superseded=[35]`,
   `round_changed=[]`; timing `superseded_as_of=[35]`, `stale_supersede=[]`.
   Compared to `evidence/c11-after-lane.txt` → `IDENTICAL True`.
6. `python3 tools/mori-sources-appendonly.py e37dcc6 --repo .`
   → timing as-of 33 + `stale_supersede=[S069]` (total 34); identical to
   `evidence/c11-after-e37dcc6.txt` (`IDENTICAL True`).
7. `python3 .ufo/waves/round-40/fixtures/extracted/gate-v2-bb1f2457.py e37dcc6 --repo .`
   → as-of 18 + `stale_supersede=[S069]` (v2's eligible set keeps its verdicts; no flip).
8. `python3 tools/mori-sources-appendonly.py bb1f2457 --repo .`
   → as-of 35, stale `[]`; the `ids`/`deleted`/`round_changed` groups are byte-identical
   to the v2 receipt (18 ids, `[]`, `[]`). The delta is exactly the eligible set.
9. Fixture runner, v3 bytes:
   `python3 .ufo/waves/round-40/fixtures/run-c11-dags.py tools/mori-sources-appendonly.py <lane> /tmp/dags-v3.txt dag-n dag-p dag-r`
   → dag-n `superseded_as_of=[S001]` exit 0; dag-p `superseded_as_of=[S001]` exit 1;
   dag-r `superseded_as_of=[S008]` exit 1. Verdict blocks compared to
   `c11-after-fixture-{n,p,r}.txt` → `IDENTICAL True` ×3.
10. Fixture runner, v2 extracted bytes
    (`…/fixtures/extracted/gate-v2-bb1f2457.py`; sha256 `62cd4132…` equals
    `git show bb1f2457:tools/mori-sources-appendonly.py`)
    → dag-n `[]`; dag-p `stale_supersede=[S001]`; dag-r `[]`. Compared to
    `c11-red-{neveredited,firstparent,readd}.txt` → `IDENTICAL True` ×3.
11. Mutant probes (temp copies under `/tmp`, never in the lane):
    - v3 eligible set + v2 re-add branch → dag-r `stale_supersede=[S008]` (fixture
      fails), dag-n/dag-p unchanged. Confirms the dag-r kill rule.
    - v3 with the v2 edit-bounded eligible set → dag-n and dag-r print an empty timing
      line (fixture fails); dag-p still passes. So dag-p exercises only (b); dag-n/dag-r
      exercise (a); (c) is caught only in combination with (a).
12. Independent registry count (no gate code):
    `git show 265a955cc:corpus/SOURCES.md` → 229 rows, 35 distinct supersede targets
    present, `S226` present and superseded by `S228`, `S229` present.
13. Walk probe: `git log --format=%H%x09%P --reverse --full-history 265a955cc -- corpus/SOURCES.md`
    → 55 commits, **0** parent-after-child pairs (date order is topological here);
    **43/55** commits have their first parent outside the walk, so the new
    `git_blob(head:path)` fallback is exercised heavily on the lane.
14. `ruff check --no-cache --isolated tools/mori-sources-appendonly.py` → 49 diagnostics
    (UP031 ×40, PLW1510 ×8, RUF059 ×1) vs 48 on v2 (UP031 ×39, PLW1510 ×7, RUF059 ×1,
    EXE001 ×1); delta is style-only (`UP031` at the new fallback, `PLW1510` at the new
    dag-p `subprocess.run`). `pyflakes` → exit 0. `ast.parse` → OK.

## Residual risk and verification gaps

- **Walk order (pre-existing, now more load-bearing).** `git log --reverse` is commit-date
  order, not `--topo-order`; the new "first-sighting commit" fallback depends on it. The
  lane walk is topologically ordered (0 inversions over 55 path commits), so no lane
  verdict is at risk, but a date-skewed DAG can define "first sighting" on a child. No
  fixture covers date skew.
- **Fallback coverage.** The first-parent-not-in-walk branch (317–322) is exercised 43
  times on the lane but by no selftest DAG; its equivalence to v2's
  `nearest_path_commit` state is verified only through the byte-identical lane receipts
  at `bb1f2457`, `e37dcc6`, and the tip.
- **`supersede_landing`** is still max-walk-index over the full-history walk (pre-existing
  r38 residual 2); two different superseding rows on incomparable branches remain
  order-defined.
- **`superseded` membership** uses any supersede row seen in the walk, even if that
  superseding row is absent at R. No lane case: all 35 timing-line ids have a superseding
  row present at the tip (checked independently).
- **Admission math.** The `19`/`34` counts cannot be reconciled with any committed
  receipt; the receipts, an independent registry parse, and the live gate all say 35 at
  the tip. Anything that scores C2 against the literal count will fail the honest
  instrument.
- **Environment note (not a finding):** lane HEAD is `ede486b` (a post-tip S229 placement
  repair plus the gutted-conjunct fixture), not the scored tip; the gate file is
  byte-identical, and the gate at HEAD also prints 35 as-of ids. The worktree has three
  modified C1 receipts (`c10-after-conjunct.txt`, `c10-after-selftest.txt`,
  `c10-red-conjunct.txt`) and untracked scratch/w1 paths; none of the C2 receipts I used
  are dirty.
