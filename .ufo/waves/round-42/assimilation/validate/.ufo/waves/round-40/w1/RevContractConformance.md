# RevContractConformance — round-40 wave-1 seat report

Seat: `RevContractConformance` (reviewer, read-only). Lane root:
`/home/vgpnk/Projects/shokunin/mori-shokunin`. Report path:
`.ufo/waves/round-40/w1/RevContractConformance.md`.

Assignment: compare `.ufo/waves/round-40/contract.md` against the landed evidence
set; every evidence path the contract names must exist with the declared content
class (red = met on v2, after = unmet on v3, etc.); name missing or mismatched
files.

Measured objects: contract at the frozen bytes (sha `6514914885e6…`, matches
`evidence/freeze-r40.txt`); evidence as committed at `HEAD`
(`ede486b`, evidence commit `8d3badd`; instruments `265a955`). Three tracked
receipts are modified in the working tree by concurrent seats (see R1); all
content-class checks below read the **committed** bytes via
`git show HEAD:<path>`.

Tooling: none installed or upgraded.

## Verdict

- **All declared evidence paths exist.** No missing evidence file. Counts:
  11 `c10-red-*.txt`, 13 `c10-after*.txt`, 3 `c11-red-*.txt`,
  6 `c11-after*.txt`, `freeze-r40.txt`, `census-start.txt`, `census-end.txt`,
  `c10-parity.txt` (plus `.parity-c7/.parity-c8`), the two fixture builders,
  the three `fixtures/extracted/` v2 bytes, `corpus/knowledge/conform-scope-r40.md`
  and `corpus/lessons/round-39-erratum.md`.
- **C1 content classes all pass** (nine survivors met→unmet with the named new
  check, divzero exit 2→unmet, multicounter met→per-counter comm_violations,
  conjunct pass=8→selftest_conjunct failure, selftest pass=11).
- **C2 semantic verdicts pass, but the declared after-value fails** (H1), and two
  before-cell claims are not discriminated by the named receipts (M1, M2).
- Mechanical matrix: **87/92 assertions pass; 5 fail** (H1, M3, L1, L2, L3).

## Evidence-path existence

Every path the contract names resolves (glob `evidence/c10-red-*.txt` → 11 hits;
`evidence/c11-red-*.txt` → 3 hits; `c10-after*.txt` → 13; `c11-after*.txt` → 6).
The one contract-cited path that is absent, `fixtures/make-ancestry-dags.py`, is
the round-39 citation the contract itself records as "a path in no commit" and
corrects; the round-40 replacement `fixtures/run-c11-dags.py` exists (sha
`0cd7f1d23c88…`, pinned).

## Declared content-class matrix

| Path(s) | Declared | Measured (committed bytes) | Verdict |
|---|---|---|---|
| `freeze-r40.txt` | sha256 over frozen paths; P-C10 == checker PREDICATE | 9/9 pins match; P-C10 1564/1564 EQUAL True; P-C11 1036/1036 EQUAL True; extracts == `git show bb1f2457:` bytes | PASS (scope gap M3) |
| `census-start.txt`, `census-end.txt` | census exit 0 | files exist, byte-identical, final line `mori ok <SOURCES.md>`; no command/EXIT line | PARTIAL (L3) |
| `c10-red-shadow-none/neg/cond/inf/decoy/underscore/second-popen/tuple` | v2 prints `CONFORM=met` exit 0 | each: `CONFORM=met`, `EXIT=0` | PASS |
| `c10-red-divzero.txt` | v2 exit 2, no FAIL line | `conformance setup error: division by zero`, `EXIT=2`, no `FAIL ` line | PASS |
| `c10-red-multicounter.txt` | v2 `CONFORM=met` | `CONFORM=met`, `EXIT=0` | PASS |
| `c10-red-conjunct.txt` | gutted r39 copy selftests green | `CONFORM_SELFTEST pass=8 fail=0`, `EXIT=0` | PASS |
| `c10-after.txt` | v3 `CONFORM=met` exit 0 | `CONFORM=met`, `EXIT=0` (all nine checks PASS) | PASS |
| `c10-after-selftest.txt` | `pass=11 fail=0` | `CONFORM_SELFTEST pass=11 fail=0`, `EXIT=0` | PASS |
| `c10-after-shadow-none/neg/cond/inf` | `unmet` + `timeout_scope` FAIL | `CONFORM=unmet`, `EXIT=1`, `check timeout_scope FAIL` | PASS |
| `c10-after-divzero.txt` | `unmet` + `timeout_scope` FAIL (violation, not setup error) | `check timeout_scope FAIL (… fold error: division by zero)`, `CONFORM=unmet`, `EXIT=1`; also `predicate/head_pin/tool_resolve/timeout_state` FAIL | PASS (L4 note) |
| `c10-after-decoy/underscore/second-popen/tuple` | `unmet` + `drain_bind` FAIL | each: `CONFORM=unmet`, `EXIT=1`, `check drain_bind FAIL` | PASS |
| `c10-after-conjunct.txt` | gutted v3 copy fails `selftest_conjunct` | `CONFORM_SELFTEST pass=0 fail=10`; all 10 failing lists contain `selftest_conjunct` | PASS |
| `c10-after-multicounter.txt` | `unmet`, per-counter comm_violations | `CONFORM=unmet`, `EXIT=1`; `check selftest_conjunct FAIL (count-c8.py: …; survivor-barecomm.py: …)` | PASS |
| `c11-before-lane.txt` | 18 as-of ids, S226 absent, stale empty | 18 entries; `S226` absent; `stale_supersede=[]` | PASS |
| `c11-red-neveredited.txt` | v2 omits the never-edited row | `superseded=[]`, `superseded_as_of=[]` | PASS |
| `c11-red-firstparent.txt` | v2 "fabricates a `changed` line plus a stale verdict" | `changed S001` + `stale_supersede=[S001]`; the same `changed S001` line also appears in the v3 after receipt | PARTIAL (M2) |
| `c11-red-readd.txt` | v2 "prints a `changed` event" | no `changed` line at all; only `round_changed=[S008]` | FAIL as written (M1) |
| `c11-after-selftest.txt` | `MORI_SOURCES_APPENDONLY_SELFTEST pass=15 fail=0` | exact match, `EXIT=0` | PASS |
| `c11-after-lane.txt` | `superseded_as_of=[19 ids incl. S226]`, stale empty | **35** entries, S226 at position 35, stale empty; summary `superseded` also 35 | FAIL (H1) |
| `c11-after-e37dcc6.txt` | `stale_supersede=[S069]` | 33 as-of + `stale_supersede=[S069]` | PASS |
| `c11-after-fixture-n.txt` | P-C11 never-edited verdict (as-of) | `superseded=[S001]`, `superseded_as_of=[S001]`, `EXIT=0` | PASS |
| `c11-after-fixture-p.txt` | P-C11 first-parent verdict (no fabricated edit) | `superseded_as_of=[S001]`, `stale_supersede=[]`, but `changed S001` and `appendonly_violations=1`, `EXIT=1` | PARTIAL (M2) |
| `c11-after-fixture-r.txt` | P-C11 re-add verdict (no changed event) | no `changed` line; `superseded_as_of=[S008]`, `round_changed=[S008]`, `EXIT=1` | PASS |

## Findings

### HIGH

**H1 — C2's declared after-value is false: contract says 19 as-of ids; the frozen
receipt has 35. The round's own correction (34) is also wrong.**

- Contract, C2 After: "on the lane at the landed tip the gate prints
  `supersede_timing superseded_as_of=[19 ids incl. S226] stale_supersede=[]`".
  The frozen P-C11 sentence — verbatim in both the contract and
  `tools/mori-sources-appendonly.py` (equality re-verified, 1036/1036 chars) —
  repeats "(19 ids) at the landed tip", and the receipt's own line 2 prints
  `S226 joins superseded_as_of (19 ids) at the landed tip` immediately above the
  35-id timing line.
- Evidence, `evidence/c11-after-lane.txt:22` (committed):
  `supersede_timing superseded_as_of=[S041,S044,S051,S062,S064,S067,S069,S070,S071,S083,S084,S090,S093,S096,S097,S101,S124,S127,S128,S129,S131,S140,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193,S226] stale_supersede=[]`
  → 35 entries, S226 last; the summary line's `superseded=[…]` is the same 35.
- Set difference against `c11-before-lane.txt`'s 18 ids: **+17**, not +1:
  `S067,S070,S071,S083,S084,S090,S093,S096,S097,S101,S124,S127,S128,S129,S131,S140`
  (16 never-edited rows) plus `S226`.
- The corrective prose is off by one in the same direction: lesson M24
  (`corpus/lessons/round-40.md`), `SCORECARD.md` round-40 correction, `LOG.md`
  round-40, the wave context in `w1-spec.json`/`wave-plan.txt`, and
  `gen-wave-spec.py:30,59,128` all say **34 as-of ids / 16 never-edited rows
  (S226 plus 15 earlier)**. The measured values are **35 / 17 (S226 plus 16
  earlier)**. [INFERENCE] the 34 matches the eligible count at `e37dcc6`
  (33 as-of + 1 stale); it is not the tip value either way.
- Consequence: the C2 kill rule ("a gate keeping the edit-bounded eligible set
  … the lane line mismatches the declared 19 ids") would reject the correct v3
  gate; the seat prompt `ExeGateLane` instructs a seat to "verify … lists 34
  as-of ids", a target no correct gate prints. Under the contract's own freeze
  rule ("a change to a predicate after this freeze is a new counter version"),
  fixing the parenthetical is a new predicate/counter version, not an edit.

### MEDIUM

**M1 — `c11-red-readd.txt` does not show the before-behaviour the contract
declares.**

Contract: "the v2 gate … prints a `changed` event for the linear
delete-then-re-add (`c11-red-readd.txt`)". Committed receipt verdict lines:

```
appendonly_violations=0 ids=[] deleted=[] superseded=[] round_changed=[S008]
supersede_timing superseded_as_of=[] stale_supersede=[]
EXIT=1
```

There is no `changed S008` line. The v3 after receipt differs only in the timing
line and the summary's `superseded` field:

```
appendonly_violations=0 ids=[] deleted=[] superseded=[S008] round_changed=[S008]
supersede_timing superseded_as_of=[S008] stale_supersede=[]
EXIT=1
```

`round_changed=[S008]` appears in **both**. The lesson's honest-stop paragraph
admits this ("the v2 red for the re-add changed event itself is invisible at the
frozen bytes") and says the fixture was redesigned so the visible discriminator
is the empty timing line — but the contract was not updated. As written, the
before-cell is not satisfied by the named receipt, and the "no changed event"
after-cell is true only in the `changed`-line sense while `round_changed=[S008]`
persists in v3.

**M2 — the dag-p receipt pair cannot discriminate the declared fabricated
`changed` line; the after fixture still reports a violation.**

Contract before: v2 "fabricates a `changed` line plus a stale verdict on the
first-parent-lacks-path merge". Committed lines, red vs after:

```
red   : changed S001 superseded_by=S002
        appendonly_violations=1 ids=[S001] … round_changed=[S001]
        supersede_timing superseded_as_of=[] stale_supersede=[S001]
after : changed S001 superseded_by=S002
        appendonly_violations=1 ids=[S001] … round_changed=[S001]
        supersede_timing superseded_as_of=[S001] stale_supersede=[]
```

Both print the identical `changed S001` and `appendonly_violations=1`; the only
observable red→after delta is the timing verdict. The v3 gate's own selftest
expects `ids=["S001"]` for dag-p (`tools/mori-sources-appendonly.py:612-615`), so
the changed line is intended in v3 and the fabricated merge edit is invisible in
the per-id output. The contract's wording ("fabricates a `changed` line",
"no fabricated edit") is not demonstrated by these receipts; a reader judging
the after cell by the changed/violation lines sees the same content as the
control.

**M3 — the freeze receipt does not pin the fixture payloads the receipts
execute, contrary to the contract's freeze declaration.**

Contract: frozen before receipts are "the fixture builders and the
survivor-fixture payloads". `evidence/freeze-r40.txt` pins 9 paths: the
contract, `count-c8.py`, `conform.py`, the tracked gate, the two builders, and
the three extracted v2 bytes. It pins **none** of the 12 executed payloads under
`.ufo/waves/round-40/fixtures/generated/`:
`survivor-{barecomm,cond,decoy,divzero,inf,second-popen,shadow-neg,shadow-none,tuple,underscore}.py`
and `conform-{r39,v3}-conjunct-gutted.py`. The receipts invoke those files by
path. The builder pins make regeneration plausible but do not prove the executed
bytes equal the builder output at freeze time; `conform-v3-conjunct-gutted.py`
was not committed at the scored tip at all (added at `ede486b`, after the
receipts and after `265a955`). The red conjunct control's bytes are likewise
unpinned; whether it was tracked when `c10-red-conjunct.txt` was produced is not
recorded (no hash in the receipt, and a concurrent seat overwrote that receipt's
mtime at 03:01:55).

**M4 — the declared "frozen before any data receipt" ordering is not met
(disclosed).**

Exact mtimes: before receipts `c11-before-lane.txt`/`c11-red-neveredited.txt`
02:41:05, `c10-red-shadow-none.txt` 02:41:19; `freeze-r40.txt` 02:46:06; after
receipts `c10-after.txt` 02:47:46, `c11-after-lane.txt` 02:49:31,
`c11-after-selftest.txt` 02:49:55. The contract says "Frozen before any data
seat or data receipt"; the freeze receipt's own note says the prior launch died
before persisting it, and the resuming L1 re-verified the inherited bytes.
Mitigation: I independently confirmed all 9 pins match the current bytes and the
three extracts hash-match `git show bb1f2457:` — so the before-control
instruments are the claimed v2 bytes. The declared invariant is still false as
an ordering claim, and the receipt set's integrity rests on the resumed L1's
re-verification rather than on a pre-existing pin.

### LOW

**L1 — count-c8 is not "count-c7 minus the sixteen dead lines".**
`diff -u <(git show bb1f2457:.ufo/waves/round-39/count-c7.py) .ufo/waves/round-40/count-c8.py`
→ **5 removed, 0 added** (SimpCounters D1 + D2). The other 11 lines (D3/D4) are
removed from `conform.py`; SimpCounters' report itself says "1 + 4 + 5 + 6 = 16
lines removed across two files". The parity claim is unaffected: `.parity-c7.txt`
and `.parity-c8.txt` are byte-identical (sha `c03e05ce…` both), and the extracted
c7 matches the `bb1f2457` blob (sha `b92c65f2…`).

**L2 — round shape: contract says 64 seats; the landed spec has 66.**
`w1-spec.json` has `items` length **66** (`counts.spawn=66`,
`policy.maxLanes=66`, `reportDir=.ufo/waves/round-40/w1`); `SCORECARD.md` and
`LOG.md` say 66 seats / 32 attack (48.5%). The contract's "ONE v2 wave of 64
seats" is stale.

**L3 — "census exit 0" is not recorded in the named receipts.**
`census-start.txt` and `census-end.txt` are byte-identical and contain no
command line and no `EXIT=`/`exit=` line; the only success signal is the final
`mori ok /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md` line
(16 W04 duplicate-URL rows above it). The lesson asserts exit 0, but the named
evidence does not carry the exit status.

**L4 — observation, not a contract mismatch: the divzero after-cell is not a
clean single-check flip.**
`c10-after-divzero.txt` also fails `predicate` (`exit=1 equal=False`),
`head_pin` (`pin=None`), `tool_resolve` (`exit=1 resolved=`), and
`timeout_state` (`timeout_reason=False`), unlike the other eight survivors.
This is consistent with running a crashing counter copy through the checker's
counter-invoking checks; the declared named check (`timeout_scope`) is present
and the declared class is satisfied.

## Residual risk and verification gaps

- **R1 — working-tree drift.** Three tracked receipts are modified relative to
  `HEAD` by concurrent seats at review time:
  `.ufo/waves/round-40/evidence/c10-after-conjunct.txt`,
  `c10-after-selftest.txt`, `c10-red-conjunct.txt`. The edits replace relative
  command paths with absolute paths and add `wall_seconds: 57.371` /
  `revision:` lines (the seat reports `ExeConjunctAfter.md` / `ExeSelftestTiming`
  show these re-runs). The committed versions and the working-tree versions
  carry the same verdict lines, so no content-class verdict changes; but the
  evidence set is mutable post-commit and the freeze does not pin evidence
  files. Main should decide whether to commit, revert, or leave those edits.
- **No live re-execution of the instruments.** This is a read-only seat, and
  `HEAD` has moved to `ede486b`; the c10 receipts pin `head_pin=265a955` and
  `tip=265a955`, so a live re-run at `HEAD` would fail `head_pin` by
  construction. All content-class checks are against committed receipt bytes;
  the pin hashes and the `git show bb1f2457:` extracts were recomputed.
- The dag-p "no fabricated edit" and dag-r "no changed event" semantics are
  verified only through the timing line and the gate's own selftest
  expectations; this seat ran no independent mutation probe of those corners.
- H1 is mechanical and reproducible from the committed line; I did not attempt
  to regenerate the predicate or a new counter version (out of scope for a
  read-only seat).

## Exact commands run (outputs as observed)

1. `sha256sum .ufo/waves/round-40/{contract.md,count-c8.py,conform.py} tools/mori-sources-appendonly.py .ufo/waves/round-40/fixtures/{make-survivor-fixtures.py,run-c11-dags.py} .ufo/waves/round-40/fixtures/extracted/{conform-v2-r39.py,count-c7-r39.py,gate-v2-bb1f2457.py}`
   → all 9 hashes equal the `freeze-r40.txt` pins
   (`6514914885e6…`, `4e4d50eb1e96…`, `5025b9664632…`, `bde5a9a34c7e…`,
   `8ff91db744c6…`, `0cd7f1d23c88…`, `fe0be179aba9…`, `b92c65f224a6…`,
   `62cd4132dbe1…`).
2. `git show bb1f2457:{.ufo/waves/round-39/conform.py,.ufo/waves/round-39/count-c7.py,tools/mori-sources-appendonly.py} | sha256sum`
   → `fe0be179…`, `b92c65f2…`, `62cd4132…` — equal to the extracts.
3. `diff -u <(git show bb1f2457:.ufo/waves/round-39/count-c7.py) .ufo/waves/round-40/count-c8.py`
   → one hunk at 95 (D1) and one at 438 (D2); removed=5 added=0.
4. `cmp .ufo/waves/round-40/evidence/.parity-c7.txt .ufo/waves/round-40/evidence/.parity-c8.txt`
   → identical; `sha256sum` both `c03e05ce2bf0…`.
5. Python (AST) extraction of the `PREDICATE` constants vs the contract
   blockquotes → `P-C10 contract_len 1564 instrument_len 1564 EQUAL True`;
   `P-C11 contract_len 1036 instrument_len 1036 EQUAL True`.
6. Python count over committed `c11-after-lane.txt` →
   `entries=35`, `S226 at position 35`; set difference vs the before line →
   `added = ['S067','S070','S071','S083','S084','S090','S093','S096','S097','S101','S124','S127','S128','S129','S131','S140','S226'] n=17`;
   `before asof n=18`; `e37 asof=33 stale=['S069']`.
7. 92-assertion conformance matrix over committed receipts (`git show HEAD:`)
   → `87/92 checks pass`; failures:
   `after-lane as-of count (contract declares 19) | DECLARED=19 MEASURED=35`;
   `count-c8 = c7 minus sixteen dead lines | removed=5 added=0`;
   `wave seats = contract 64 | DECLARED=64 MEASURED=66`;
   `census exit code recorded | no EXIT/exit line; only final "mori ok"`;
   `freeze pins every executed fixture payload | unpinned: 12 files under fixtures/generated/`.
8. `git show HEAD:.ufo/waves/round-40/evidence/{c11-red-firstparent,c11-after-fixture-p,c11-red-readd,c11-after-fixture-r}.txt | grep -E '^(changed|appendonly_violations|supersede_timing|EXIT)'`
   → quoted verbatim in M1/M2 above.
9. `git status --porcelain -- .ufo/waves/round-40/evidence`
   → three ` M` entries (R1).
10. `git ls-tree -r --name-only 265a955 -- .ufo/waves/round-40/fixtures/generated`
    vs `HEAD` → the v3 gutted copy is absent at `265a955`, present at `HEAD`.
11. `stat -c '%y %n'` on freeze and representative receipts → mtimes quoted in M4.
12. `python3` on `w1-spec.json` → `reportDir=.ufo/waves/round-40/w1`,
    `maxLanes=66`, `items=66`, roles include reviewer 16 / executor 18 /
    critic 9 / scout 6 / scribe 6 / mutation-tester 4.
13. `grep -n 'S229' corpus/SOURCES.md` → line 235 (registry row, mined
    2026-10-24, used-by `corpus/knowledge/conform-scope-r40.md`);
    `corpus/lessons/round-40.md` contains M23 and M24; the erratum contains the
    bypass-wait wording fix and the S227 18→17-word correction.
