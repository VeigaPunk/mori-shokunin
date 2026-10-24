# ScrLandedChanges — mori round 40, wave 1 (scribe: landed changes)

Role: scribe. Read-only seat. This report is the only artifact written; no
instrument, receipt, product, judge, LOG/SCORECARD or git/jj state was touched.
Lane root: `/home/vgpnk/Projects/shokunin/mori-shokunin` (paths below are
lane-relative unless absolute).

## Behavior

Drafted the round-40 "Landed changes" bullets from the committed receipts, the
three round-40 commits, and the LOG/SCORECARD/lesson records. Every number below
was read from a committed file or computed by a command named in *Gates*; nothing
was re-run from the instruments themselves. Two prose-vs-receipt count conflicts
were found and are reported verbatim (F1, plus F2/F3 on the C2 before-cells).

## Landed changes (receipt set → commit)

Commit chain (verified: `git rev-list --parents -4 HEAD`):
`bb1f2457` (entering tip) → `265a955cc67be4eae97d2dc5a9338a25f31eb29b` (T1) →
`8d3badd0647c5dbfaf5f5a1443c5d4d5109a8d21` (T2) → `ede486b7a09afbacfb380d5871c46a8051a6dc2e`
(HEAD, T3 repair). All three are linear single-parent commits.

### T1 — `265a955cc` "round-40: instruments — conform v3 (P-C10), gate v3 (P-C11), S229, r39 erratum"

`git show --stat 265a955cc`: 29 files, +10980/−49. Instrument bytes and their
freeze pins (`evidence/freeze-r40.txt`, sha256 re-checked by me, all match):

- `.ufo/waves/round-40/conform.py` — conformance checker v3, 805 lines, sha256
  `5025b9664632d01063c11b4f5dadd4f9a063db66d73315d7ed25db8d90b83aaf`.
- `.ufo/waves/round-40/count-c8.py` — counter of record, sha256
  `4e4d50eb1e96d947f0e9d2ab25a13b2b8c33963f216f3be43060a3348702f6da`.
- `tools/mori-sources-appendonly.py` — tracked gate v3 (P-C11), sha256
  `bde5a9a34c7eb3bcbee39d669b8d187caeb51807ad1bdcd85a05c1bcd06777ec`.
- `.ufo/waves/round-40/contract.md` — frozen contract, sha256
  `6514914885e6a1249ed7903931b9734a55e828275121353c2727348eae504a8d`.
- Before-instrument bytes extracted via `git show bb1f2457:<path>` into
  `fixtures/extracted/`: `conform-v2-r39.py` (`fe0be179…`), `count-c7-r39.py`
  (`b92c65f2…`), `gate-v2-bb1f2457.py` (`62cd4132…`); the extracted shas match
  the freeze receipt.
- Fixtures landed here: `fixtures/make-survivor-fixtures.py`
  (`8ff91db7…`), ten generated survivors (`survivor-{barecomm,cond,decoy,divzero,inf,second-popen,shadow-neg,shadow-none,tuple,underscore}.py`;
  `barecomm` is the second counter of the two-counter audit, the other nine are
  the survivor set), `fixtures/generated/conform-r39-conjunct-gutted.py`,
  `fixtures/run-c11-dags.py` (`0cd7f1d2…`), and the four witness files.
- Corpus surface: `corpus/SOURCES.md` +1 row (S229, appended at line 292 in this
  commit's blob — outside `## Registry`; see T3), `corpus/evidence/sources-r40/S229.src`,
  `corpus/knowledge/conform-scope-r40.md`, `corpus/lessons/round-39-erratum.md`.
- `SKILL.md`: the v3 conformance row added and the SOURCES-append-only row
  updated to `MORI_SOURCES_APPENDONLY_SELFTEST pass=15 fail=0` (+2/−1).

Receipt set tied to T1: `evidence/c10-parity.txt` (count-c7 vs count-c8 receipts
byte-identical at `bb1f2457`, seed 20261024, `c7_exit=0 c8_exit=0`) and every
`c10-after-*` / `c11-after-*` receipt, which names T1 on its `command:` line and,
where the check prints it, `check head_pin PASS (pin=265a955cc… tip=265a955cc…)`.
Freeze gate: `freeze-r40.txt` also carries `P-C10 contract==checker PREDICATE: True`.

### T2 — `8d3badd` "round-40: evidence receipts, wave spec (66-seat v2, validated), SCORECARD/LOG/lesson"

`git show --stat 8d3badd`: 48 files, +1943. Receipt sets landed here:

- **C1 before set (11 files)** — `evidence/c10-red-*.txt`, measured with the
  extracted r39/v2 checker bytes at `bb1f2457`: nine survivor fixtures → eight
  print `CONFORM=met` `EXIT=0` and `c10-red-divzero.txt` prints
  `conformance setup error: division by zero` `EXIT=2`;
  `c10-red-multicounter.txt` → `CONFORM=met` `EXIT=0`;
  `c10-red-conjunct.txt` → `CONFORM_SELFTEST pass=8 fail=0` `EXIT=0`.
- **C1 after set (13 files)** — `evidence/c10-after-*.txt`, measured at T1:
  `c10-after.txt` → nine checks PASS, `CONFORM=met` `EXIT=0`;
  `c10-after-selftest.txt` → `CONFORM_SELFTEST pass=11 fail=0` `EXIT=0`;
  nine survivor receipts → `CONFORM=unmet` `EXIT=1` with the named check:
  cond/inf/shadow-neg/shadow-none → `timeout_scope`; decoy/second-popen/tuple/
  underscore → `drain_bind`; divzero → `timeout_scope` (plus four collateral
  FAILs, F6); `c10-after-multicounter.txt` → `drain_bind` + `selftest_conjunct`
  FAIL, `CONFORM=unmet` `EXIT=1`; `c10-after-conjunct.txt` →
  `CONFORM_SELFTEST pass=0 fail=10` `EXIT=1`, `selftest_conjunct` in every
  failing list (the gutted copy cannot run that arm, hence ten, not eleven).
  The command in `c10-after-conjunct.txt` names
  `fixtures/generated/conform-v3-conjunct-gutted.py`, which was **not tracked at
  this commit** (see T3).
- **C2 before set (4 files)** — `evidence/c11-before-lane.txt` (extracted v2
  bytes at `bb1f2457`: `superseded_as_of=[18 ids]`, S226 absent,
  `stale_supersede=[]`, `EXIT=1`) and `c11-red-{neveredited,firstparent,readd}.txt`
  (v2 bytes on dag-n/dag-p/dag-r).
- **C2 after set (6 files)** — `evidence/c11-after-selftest.txt` →
  `MORI_SOURCES_APPENDONLY_SELFTEST pass=15 fail=0` `EXIT=0`;
  `c11-after-lane.txt` → as-of list of 35 ids including S226, `stale_supersede=[]`,
  `EXIT=1` (F1); `c11-after-e37dcc6.txt` → 33 as-of ids,
  `stale_supersede=[S069]`, `EXIT=1`; `c11-after-fixture-n/p/r.txt` → dag-n
  `as_of=[S001] stale=[] EXIT=0`, dag-p `as_of=[S001] stale=[] EXIT=1`,
  dag-r `as_of=[S008] stale=[] EXIT=1`.
- **Provenance/plan set** — `evidence/freeze-r40.txt`, `census-start.txt`,
  `census-end.txt` (byte-identical to each other, 17 lines each, F4),
  `evidence/wave-plan.txt` (`spawn=66`), `gen-wave-spec.py`, `w1-spec.json`,
  `scratch/selftest-v3-draft{1,2}.txt`.
- **Records** — `LOG.md` entry
  `## Round 40 (L1 mori-r40, attempt 1 resumed after the 01:32 launch died)`
  (LOG.md:2276; its closing line "Instruments at `265a955…`; evidence at this
  commit" therefore names `8d3badd`); `SCORECARD.md` entry
  `## Round 40 declaration (attempt 1 resumed, L1 mori-r40) — conformance v3
  scope-aware timeouts + per-Popen drains (C1, operability), gate v3 P-C11
  eligible set + first-parent reference (C2, depth)` (SCORECARD.md:2216);
  `corpus/lessons/round-40.md` (`## Gate`, `## Mistakes` M23/M24,
  `## Round shape and debts`). Entering-tip context is the LOG entry
  `## Round 39 (L1 mori-r39)` (LOG.md:2240).

### T3 — `ede486b` (HEAD) "round-40: repair S229 registry placement (E12: row inside ## Registry) + commit referenced gutted-conjunct fixture"

`git show --stat ede486b`: 2 files, +805/−1.

- `.ufo/waves/round-40/fixtures/generated/conform-v3-conjunct-gutted.py`
  committed (804 lines, sha256 `20e324228735d39ad6bb293aac9dfd4b3a27a009a0f2ecf222731771bd2aaabf`);
  `git ls-tree 8d3badd` returns nothing for this path. Byte check by difflib:
  it equals the frozen `conform.py` with exactly one hunk, removal of the
  `CONJUNCT_MUTATION,` entry from the mutation table (conform.py:734). This
  makes the `c10-after-conjunct.txt` command's target a committed path.
- `corpus/SOURCES.md`: the S229 row moves from line 292 (outside `## Registry`)
  to line 235 (inside `## Registry`, which spans lines 3–236 at HEAD);
  +1/−1. Registry row count is 229 at `265a955` and at HEAD.
- No receipt was regenerated for this commit; no LOG/SCORECARD/lesson text
  records it (F5).

### Pending (uncommitted at HEAD)

- `git status --short` at HEAD: `?? .scratch/` and `?? .ufo/waves/round-40/w1/`.
  The wave-1 seat report set — `.ufo/waves/round-40/w1/{ExeCensus,ExeExtractPins,ExeGateE37,ScrLandedChanges}.md`
  at the time of writing — is untracked; no wave-1 report commit exists yet.
  This is the only still-pending evidence commit.
- The assignment's "pending evidence commit" for the receipts is therefore
  resolved: it landed as T2 (`8d3badd`), with the T3 repair at HEAD.

## Gates

Run by me (all read-only; no instrument run):

1. `git log --oneline -20`, `git show --stat --oneline {265a955cc,8d3badd,ede486b}`,
   `git rev-list --parents -4 HEAD` → linear chain and file lists above.
2. `git diff --stat 265a955cc HEAD -- .ufo/waves/round-40/conform.py
   .ufo/waves/round-40/count-c8.py tools/mori-sources-appendonly.py
   .ufo/waves/round-40/contract.md` → **empty output**: instrument bytes did not
   move between T1 and HEAD, so the T1-measured after-receipts are still the
   bytes at HEAD.
3. `sha256sum` on those four paths plus `fixtures/make-survivor-fixtures.py`,
   `fixtures/run-c11-dags.py` → six of six equal the `freeze-r40.txt` pins.
4. `git ls-tree 8d3badd|HEAD -- ...conform-v3-conjunct-gutted.py` → absent at
   T2, blob `7176704b…` at HEAD.
5. `python3` difflib `conform.py` vs the gutted fixture → one hunk
   (`-        CONJUNCT_MUTATION,`), 805 vs 804 lines, shas above.
6. `python3` parse of `c11-after-lane.txt` → `superseded_as_of` 35 items
   (34 commas, 35 distinct) = `superseded` 35; `ids` 18; set difference 17
   never-edited ids: `S067,S070,S071,S083,S084,S090,S093,S096,S097,S101,S124,
   S127,S128,S129,S131,S140,S226`.
7. `python3` registry scan of `corpus/SOURCES.md` at HEAD and of the
   `git show 265a955:corpus/SOURCES.md` blob → 229 rows; every one of those 17
   ids has a row containing `supersedes S<id>`; no missing id.
8. `diff evidence/census-start.txt evidence/census-end.txt` → byte-identical;
   `wc -l` → 17 each. Neither file has a `command:` line or an `EXIT=` line.
9. `git show 265a955 -- SKILL.md`, `git show ede486b -- corpus/SOURCES.md` →
   the SKILL row edit and the S229 placement move as described.
10. Text reads of LOG.md, SCORECARD.md, `corpus/lessons/round-40.md`,
    `corpus/lessons/round-39-erratum.md`, and every `evidence/c10-*`/`c11-*`
    receipt (command line + verdict lines).

Not run by me: `conform.py` (either version), `tools/mori-sources-appendonly.py`
(any mode), the census script, and `run-c11-dags.py`. Their outcomes above are
quoted from committed receipts; an unrun check has not passed here. I did not
rerun anything to "confirm" a receipt.

Note on exit codes (read from the gate source, not inferred): without
`--round-base` the gate exits 1 when `ids` or `deleted` is non-empty; with
`--round-base` it exits 1 when `round_changed` is non-empty. That explains
`c11-after-lane.txt EXIT=1` (18 standing ids), `c11-after-fixture-p EXIT=1`
(`ids=[S001]`), and `c11-after-fixture-r EXIT=1` (`round_changed=[S008]`).

## Touched surfaces

- Wrote only `.ufo/waves/round-40/w1/ScrLandedChanges.md`.
- Read-only everywhere else. No writes to the fleet repo, sibling lanes, lane jj
  state, lane Git index, `.ufo/state/` or `.ufo/watchdog.log`; no git/jj
  mutation; no tool installation.

## Out of scope

- Re-running instruments, census, or the fixture DAG builders.
- Judging whether C1/C2 are admitted, and resolving the conflicts below.
- Committing, pushing or publishing anything (including the pending wave-1
  report set).

## Findings

**F1 (count conflict; highest-value item for the judge).** The committed
receipt says **35** as-of ids; the prose derived from it says **34**, and the
never-edited count differs the same way (**17** vs **16**).

- Receipt `evidence/c11-after-lane.txt`, timing line (verbatim, 35 items /
  34 commas): `supersede_timing superseded_as_of=[S041,S044,S051,S062,S064,S067,
  S069,S070,S071,S083,S084,S090,S093,S096,S097,S101,S124,S127,S128,S129,S131,
  S140,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193,S226]
  stale_supersede=[]`; the same file's summary line has `superseded=` with the
  same 35 ids and `ids=` with 18.
- Prose 34: assignment context ("Lane line at the tip carries 34 as-of ids
  including S226"), `LOG.md:2295-2296` ("lane line at T1 lists 34 as-of ids
  incl. S226, none stale"), `SCORECARD.md:2234` ("the measured value is **34
  as-of ids** at T1"), lesson M24 ("the measured lane line at T1 lists **34**
  as-of ids"), and the committed seat prompts in `w1-spec.json` /
  `wave-plan.txt` ("verify the supersede_timing line lists 34 as-of ids").
- Prose 16: `SCORECARD.md:2232-2233` and lesson M24 ("16 never-edited superseded
  rows (S226 plus 15 earlier)"). The receipt's set difference is 17
  (`S226` plus 16 earlier, listed in Gates #6), and all 17 are genuinely
  superseded in the registry at `265a955` (Gates #7).
- The frozen predicate itself carries a third number, "(19 ids)"
  (`contract.md:119`, `contract.md:137,145`), already recorded as the M24
  mis-prediction.
  Conflict: 19 (frozen parenthetical) vs 34 (correction prose) vs 35 (receipt).
  I did not resolve which prose number is intended.

**F2 (C2 before-cell vs receipt, dag-p).** `contract.md` C2 before-cell says the
v2 gate "fabricates a `changed` line plus a stale verdict on the
first-parent-lacks-path merge (`c11-red-firstparent.txt`)". The committed v2
receipt prints `changed S001 superseded_by=S002`, `appendonly_violations=1
ids=[S001] deleted=[] superseded=[S001] round_changed=[S001]`,
`supersede_timing superseded_as_of=[] stale_supersede=[S001]`, `EXIT=1`; the v3
receipt (`c11-after-fixture-p.txt`) prints the same `changed` line and the same
summary fields, differing only in the timing verdict
(`superseded_as_of=[S001] stale_supersede=[]`). On the committed bytes the
observable v2→v3 difference on dag-p is the timing verdict alone, not a
fabricated changed line. The gate's own selftest pins this v3 output
(`("first-parent-lacks-path merge contributes no edits", "dag-p", 1, {…"ids":
["S001"]…})`), so the receipt matches the frozen expectation.

**F3 (C2 before-cell vs receipt, dag-r).** `contract.md` C2 before-cell says v2
"prints a `changed` event for the linear delete-then-re-add
(`c11-red-readd.txt`)". The committed receipt has **no** `changed` line:
`appendonly_violations=0 ids=[] deleted=[] superseded=[] round_changed=[S008]`,
`supersede_timing superseded_as_of=[] stale_supersede=[]`, `EXIT=1`. The lesson's
honest-stop paragraph (corpus/lessons/round-40.md, after M24) records exactly
this: "the v2 red for the re-add *changed event itself* is invisible at the
frozen bytes … The fixture was redesigned so the re-added row is superseded".
The frozen contract before-cell was not amended to match.

**F4 (census receipts carry no command or exit).** `evidence/census-start.txt`
and `census-end.txt` are byte-identical, 17 lines each, ending
`mori	ok	/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md`. Neither
names the command that produced it nor an exit code, so "census exit 0"
(LOG/SCORECARD/lesson) is prose-only with respect to the receipt set.

**F5 (record gap for T3).** The LOG round-40 entry ends "Instruments at
`265a955cc…`; evidence at this commit" (the entry landed at `8d3badd`), and no
LOG/SCORECARD/lesson line records the HEAD repair `ede486b` (S229 placement +
committed gutted-conjunct fixture). The repair exists only in its commit message
and diff.

**F6 (divzero after-receipt collateral, unadjudicated).**
`c10-after-divzero.txt` reaches `CONFORM=unmet EXIT=1` with the declared
`timeout_scope` FAIL (`line 114 (communicate): fold error: division by zero`),
but also FAILs `predicate` (`exit=1 equal=False`), `head_pin` (`pin=None`),
`tool_resolve` (`exit=1 resolved=`) and `timeout_state`
(`exit=1 timeout_reason=False`). The other eight survivor fixtures fail exactly
one named check. I record the difference without classifying it.

**F7 (declared wave size).** `contract.md:171` says "ONE v2 wave of 64 seats";
`evidence/wave-plan.txt` has `counts: {"spawn": 66}` and LOG says "66 seats
(32 attack)". 66 is inside the declared band (64–128) and 32/66 = 48.5% ≥ 25%,
but the contract's number and the dispatched plan's number differ.

## Artifact paths

- This report: `.ufo/waves/round-40/w1/ScrLandedChanges.md`.
- Receipts: `.ufo/waves/round-40/evidence/c10-*.txt` (11 red, 13 after,
  `c10-parity.txt`), `.ufo/waves/round-40/evidence/c11-*.txt` (4 before/red,
  6 after), `census-start.txt`, `census-end.txt`, `freeze-r40.txt`,
  `wave-plan.txt`.
- Instruments: `.ufo/waves/round-40/{conform.py,count-c8.py,contract.md}`,
  `tools/mori-sources-appendonly.py`, `fixtures/` (extracted, generated,
  generators), `w1-spec.json`, `gen-wave-spec.py`.
- Records: `LOG.md` (round-40 entry at 2276; round-39 at 2240), `SCORECARD.md`
  (round-40 at 2216), `corpus/lessons/round-40.md`,
  `corpus/lessons/round-39-erratum.md`, `corpus/SOURCES.md`,
  `corpus/evidence/sources-r40/S229.src`,
  `corpus/knowledge/conform-scope-r40.md`, `SKILL.md`.
- Commits: T1 `265a955cc67be4eae97d2dc5a9338a25f31eb29b`,
  T2 `8d3badd0647c5dbfaf5f5a1443c5d4d5109a8d21`, T3/HEAD
  `ede486b7a09afbacfb380d5871c46a8051a6dc2e`.
