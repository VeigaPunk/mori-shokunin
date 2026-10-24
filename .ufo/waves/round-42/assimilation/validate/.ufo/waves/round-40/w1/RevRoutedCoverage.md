# RevRoutedCoverage — r40 w1: do the contract's Routed inputs discharge r39 closure defects 1–4?

Seat: `RevRoutedCoverage` (reviewer, read-only). Round 40 wave 1, L1 mori-r40 attempt 1.
Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin`; scored tip `265a955cc67be4eae97d2dc5a9338a25f31eb29b`;
entering tip `bb1f2457bb8d3e8d5dfe98488b91e8c02e378ca3`; HEAD at read time `ede486b`
(two post-tip commits: evidence `8d3badd`, S229-placement repair `ede486b`).

Report path note: the delivered prompt carried no `Report:` trailer. I used the wave
`reportDir` + seat name (`.ufo/waves/round-40/w1/RevRoutedCoverage.md`), the convention
the other w1 reviewer reports use. Tool installs: none. No pacman, no production edits.
All git calls were read-only (`show`, `status`, `diff`, `merge-base` via the gate).
The fixture runner wrote its two receipt captures to `/tmp/` and built/removed its DAGs
under `.scratch/` (its own cleanup).

## Axes named

1. **Coverage** — every closure routed defect 1–4 is named in `contract.md` §Routed inputs.
2. **Discharge** — the named receipt/erratum exists, is consistent with the committed tip,
   and actually shows what the bullet says it shows.
3. **Single-source fidelity** — the prose/predicate fix for defect 3 agrees with the
   measured artifact (the exact class defect 3 was routed to close).
4. **Honesty of numbers/labels** — every count and word-count in the routed text matches
   measured bytes (the r39 S227 class).

## Verdict table — closure defects 1–4

| # | Closure defect | Contract bullet | Named discharge | Receipts checked | Verdict |
|---|---|---|---|---|---|
| 1 | drain-shape before-control not reproducible + "bypass-wait likewise" wording | `contract.md:17-23` | decoy fixture before/after + r39 erratum | `c10-red-decoy.txt` (r39 `CONFORM=met`, `drain_shape PASS`); `c10-after-decoy.txt` (v3 `CONFORM=unmet`, `drain_bind FAIL`); erratum:3-16; `SCORECARD.md:2199` carries "bypass-wait likewise" | **PASS** |
| 2 | name-not-value survivors + decoy drain + conjunct/multi-counter | `contract.md:24-28` → C1 | nine survivor fixtures, two-counter audit, gutted-conjunct copy | `c10-red-{shadow-none,shadow-neg,cond,inf,decoy,underscore,tuple,second-popen}.txt` (8 survivors) and `c10-red-multicounter.txt` all `CONFORM=met`; `c10-red-divzero.txt` exit 2; `c10-red-conjunct.txt` `pass=8 fail=0`; after: each survivor `CONFORM=unmet` with the named check, `c10-after-selftest.txt` `pass=11 fail=0`, `c10-after-conjunct.txt` `pass=0 fail=10` | **PASS** |
| 3 | first-parent prose vs second-parent fall-through; unreachable "18 ids" prose, one source of truth | `contract.md:29-31` → C2 | P-C11 frozen verbatim in gate + lane/DAG receipts | first-parent half **PASS** (my v2/v3 DAG re-runs below); count-prose half **FAIL** — contract/gate say 19, receipt says **35**, lesson/SCORECARD correction says 34 | **PARTIAL / FAIL** |
| 4 | S227 lesson Gate label 18 words vs 17 | `contract.md:40-41` | `corpus/lessons/round-39-erratum.md:18-22` | quote re-counted: **17** words; erratum states 18→17 | **PASS** (routed scope); residual in `SOURCES.md:292` |

Defects 5 (undispatched wave 2) and 6 (standing W04 census debt) are outside the list by
its own heading ("defects 1–4"); 6 is dispositioned in `corpus/lessons/round-40.md:8-10`
and the `ConnW04Routing` seat. That matches the assignment's defect scope.

## Findings

### F1 (HIGH) — defect 3's count-prose half is not discharged: the "one source of truth" is three numbers, none matching the receipt

The closure routed defect 3 asked for "fix prose or predicate, one source of truth" for the
unreachable "18 ids" prose. The round-40 discharge re-freezes the predicate and leaves a new
count inside it that its own receipt refutes.

- `contract.md:119` (P-C11, verbatim): "S226 joins superseded_as_of **(19 ids)** at the landed tip".
- `contract.md:137` (declared after-cell, citing `c11-after-lane.txt`):
  `supersede_timing superseded_as_of=[19 ids incl. S226] stale_supersede=[]`.
- `contract.md:145` (kill rule): "mismatches the **declared 19 ids**".
- `tools/mori-sources-appendonly.py:87` prints the same "(19 ids)" inside `PREDICATE` on every run.
- The cited receipt `evidence/c11-after-lane.txt` (last line) lists **35 unique ids**, S226 last,
  `stale_supersede=[]`.

My measurement (read-only):

```
$ python3 tools/mori-sources-appendonly.py 265a955cc67be4eae97d2dc5a9338a25f31eb29b --repo .
supersede_timing superseded_as_of=[S041,S044,S051,S062,S064,S067,S069,S070,S071,S083,S084,S090,S093,S096,S097,S101,S124,S127,S128,S129,S131,S140,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193,S226] stale_supersede=[]
```

35 ids. Same line at `8d3badd` and at `ede486b`. An independent parse of
`git show 265a955cc:corpus/SOURCES.md` finds exactly these 35 ids as superseded targets
present at R (set equality with the receipt; 229 registry rows).

The same-round correction is also wrong: `corpus/lessons/round-40.md:24` (M24) and
`SCORECARD.md:2232-2240` record **34 as-of ids** at T1. The 34 is the `e37dcc6` union
(as_of 33 + stale 1), not the tip's as_of set. So the record carries three conflicting
counts — contract/gate 19, lesson/SCORECARD 34, receipt/measurement 35.

Consequence: routed defect 3 is only half discharged. The semantic clause ("eligible set is
every superseded id present at R") is implemented correctly and receipt-true (my v2/v3 DAG
re-runs and the 18→35 lane extension confirm it), so this is claim-sizing/prose drift, not a
broken mechanism. But C2's declared after-cell is false at its own cited receipt, and the
frozen kill rule cannot be satisfied by the honest gate: applying "mismatches the declared 19
ids" literally rejects v3 (which prints 35). The freeze rule makes the predicate string
unfixable in place, so the repair must be erratum-class (name 35, mark the parenthetical
superseded, and correct 34→35 wherever the lesson/SCORECARD/LOG propagate it). Peers
`CritPredParenthetical`, `CritLaneLine`, and `RevFindingsCoverage` independently measured 35;
that is corroboration, not the basis of this finding.

### F2 (MEDIUM) — the routed input for lesson finding 1 claims an erratum paragraph that does not exist

`contract.md:32-35` says the P-C7 "narrowed reading [is] recorded in the r39 erratum". It is not.

```
$ grep -n 'P-C7\|drift_kill\|narrowed\|honest and mutated' corpus/lessons/round-39-erratum.md
(no output; exit 1)
$ git show 265a955cc:corpus/lessons/round-39-erratum.md | sha256sum
5cfea3774885697ecb4201de839c36dec7eb97292231199aefc17557709747f6  -
$ sha256sum corpus/lessons/round-39-erratum.md
5cfea3774885697ecb4201de839c36dec7eb97292231199aefc17557709747f6  corpus/lessons/round-39-erratum.md
```

The 28-line erratum contains four corrections: bypass-wait wording (:3-16), S227 18→17
(:18-22), and the r39 `pass=11` / `make-ancestry-dags.py` citations (:24-28). There is no
P-C7 paragraph. `corpus/lessons/round-40.md:42-43` repeats the false pointer ("narrowed
reading recorded in the same erratum"). The narrowed reading itself is stated in the contract
paragraph and appears accurate; the named discharge artifact does not exist, so this routed
input has **no discharging receipt**. (This is a lesson finding, not one of closure defects
1–4; I report it because the assignment asks for any routed input without a discharge.)

### F3 (LOW) — defect 3's before-cell overstates the printed divergence; the receipts discriminate on the timing line only

`contract.md:130-133` says v2 "fabricates a `changed` line plus a stale verdict" on the
first-parent merge and "prints a `changed` event" for the re-add. My re-runs show:

```
v2 dag-p: changed S001 superseded_by=S002 / ids=[S001] / as_of=[]  stale=[S001]
v3 dag-p: changed S001 superseded_by=S002 / ids=[S001] / as_of=[S001] stale=[]
v2 dag-r: superseded=[] round_changed=[S008] / as_of=[]  stale=[]
v3 dag-r: superseded=[S008] round_changed=[S008] / as_of=[S008] stale=[]
```

Both gates print the same `changed S001` line (the legitimate side-branch edit), and both
print `round_changed=[S008]` with no `changed S008` line. The observable discriminator is the
timing verdict, not a fabricated changed line. The r40 lesson's honest-stop paragraph
(`round-40.md:26-33`) already discloses that the re-add changed event is invisible at the
frozen bytes; the contract wording did not follow. The first-parent fix itself is genuinely
discharged (v2 `stale=[S001]` → v3 `as_of=[S001]`); this is a wording correction, no
predicate change.

### F4 (LOW) — defect 4 is discharged as scoped, but the same 18-word label survives in the registry search log

`corpus/lessons/round-39-erratum.md:18-22` states the lesson Gate label says 18, the quote is
17, and corrects it. I re-counted the quote: `printf '%s' '...' | wc -w` → **17**. That
discharges the routed scope (the lesson Gate row).

Residual: `corpus/SOURCES.md:292` (round-39 search log) still says
"(the two-dot range sentence, 18 words)", and the erratum does not name that occurrence.
The erratum's stated rationale — "the registry row's anchor cell is immutable" — does not
match the location: the S227 registry row's anchor cell (`SOURCES.md:233`) carries no word
count, and the mislabel lives in the lesson Gate row and the search log. The correction is
recorded; the rationale/location and the second occurrence are not.

## Checks that passed (evidence)

- **Freeze pins.** `sha256sum` over the six pinned paths and the three extracted v2 paths
  matches `evidence/freeze-r40.txt` exactly (contract `6514914…`, count-c8 `4e4d50e…`,
  conform `5025b96…`, gate `bde5a9a…`, fixture builders `8ff91db…`/`0cd7f1d…`, extracted
  `fe0be17…`/`b92c65f…`/`62cd413…`).
- **Predicate parity.** Extracted the blockquote from `contract.md:119` and the `PREDICATE`
  string from the gate (and P-C10 from `conform.py`): both compare equal after whitespace
  normalization — **P-C11 contract==gate True, P-C10 contract==conform True**.
- **Defect 1.** `c10-red-decoy.txt`: r39 checker `CONFORM=met`, `drain_shape PASS`. Same
  fixture under v3: `c10-after-decoy.txt` `CONFORM=unmet`, `drain_bind FAIL` ("Popen at line
  143 not drained by a bound, consumed communicate in its function"). The erratum names both
  receipts and supersedes the report/SCORECARD sentence; `SCORECARD.md:2199` contains the
  exact "bypass-wait likewise" wording the erratum corrects.
- **Defect 2.** Before/after receipt table (verdicts parsed from the committed files):
  - `c10-red-shadow-none/-neg`, `-cond`, `-inf`, `-decoy`, `-underscore`, `-tuple`,
    `-second-popen`, `-multicounter` → `CONFORM=met`, exit 0.
  - `c10-red-divzero` → exit 2 (no FAIL line); `c10-red-conjunct` → `CONFORM_SELFTEST pass=8 fail=0`.
  - After: `-shadow-none/-neg`, `-cond`, `-inf` → `CONFORM=unmet` with `timeout_scope FAIL`;
    `-decoy`, `-underscore`, `-tuple`, `-second-popen` → `unmet` with `drain_bind FAIL`;
    `-divzero` → `unmet`, `timeout_scope FAIL` ("fold error: division by zero"), exit 1;
    `-multicounter` → `drain_bind` + `selftest_conjunct` FAIL with per-counter messages;
    gutted v3 copy → `pass=0 fail=10`; v3 selftest → `pass=11 fail=0`.
- **Defect 3, first-parent/re-add halves.** Re-ran `fixtures/run-c11-dags.py` with the
  extracted v2 gate and with the landed v3 gate over dag-n/dag-p/dag-r; verdicts reproduced
  the committed `c11-red-*` and `c11-after-fixture-*` receipts byte-for-byte in their verdict
  lines (quoted under F3). Gate selftest: `MORI_SOURCES_APPENDONLY_SELFTEST pass=15 fail=0`,
  exit 0. Lane line: v2 18 ids (S226 absent) → v3 35 ids (S226 present), stale `[]`; at
  `e37dcc6` v3 prints as_of 33 + `stale=[S069]`, matching the declared corner.
- **Finding 7/10.** Erratum:24-28 contains both corrections (r39 `pass=11` stale; the
  `make-ancestry-dags.py` path exists in no commit; real builders named). Verified text.
- **Defect 4.** Quote word count 17; erratum:18-22 records the correction.

## Residual risk / verification gaps

- Three C1 receipts are modified in the worktree relative to HEAD — `c10-red-conjunct.txt`,
  `c10-after-conjunct.txt`, `c10-after-selftest.txt` (`git status --porcelain` → 3 M files).
  The diff is command-line/timing only (absolute path, `revision:`/`wall_seconds` lines);
  verdicts are identical to HEAD (`pass=8 fail=0`, `pass=0 fail=10`, `pass=11 fail=0`). I
  checked both versions; a later committed state may differ in bytes, not verdicts.
- `evidence/c10-parity.txt` proves the **counter** receipts byte-identical
  (count-c7 vs count-c8 at `bb1f2457`, one seed: `PARITY: receipts byte-identical`). The
  Routed inputs bullet for SimpCounters also claims checker behavior "including both
  selftests"; the r40 parity receipt does not cover `conform.py`. The r39 SimpCounters
  receipts (`w1/SimpCounters.md:52-57`) do cover the variant-vs-pristine conform selftest;
  I did not re-run that 57-second selftest (other seats own it).
- I did not re-run the conform selftest or the survivor sweep; my C1 checks are the
  committed/uncommitted receipts plus the contract==checker predicate extraction. The C2
  lane line, gate selftest, and both DAG fixture sets I did re-run.
- The wave context/assignment text says "34 as-of ids"; the receipt and three independent
  measurements (mine, `CritLaneLine`, `CritPredParenthetical`) say 35. Recorded here so the
  report/SCORECARD do not inherit 34.
- HEAD is `ede486b`, two commits past the scored tip; the gate line is unchanged at both
  (verified), so the receipt is not invalidated by the S229-placement repair.

## Commands run (exact; cwd `/home/vgpnk/Projects/shokunin/mori-shokunin` unless noted)

1. `ls corpus/lessons/ .ufo/waves/round-40/evidence/`; `git log --oneline -5`.
2. `sha256sum` over the nine pinned/extracted paths (outputs in "Freeze pins").
3. Python: extract `> P-C11:` / `> P-C10:` blockquotes from `contract.md` and `PREDICATE`
   from `tools/mori-sources-appendonly.py` / `.ufo/waves/round-40/conform.py`; compare
   normalized → `P-C11 contract==gate: True`, `P-C10 contract==conform: True`.
4. `python3 tools/mori-sources-appendonly.py 265a955cc67be4eae97d2dc5a9338a25f31eb29b --repo .`
   → the 35-id `supersede_timing` line, `stale_supersede=[]`. Same command with `8d3badd`,
   `ede486b` → same line.
5. Python: parse `git show 265a955cc:corpus/SOURCES.md` (229 rows, teaches-cell
   `supersedes S\d{3}` targets) → 35 superseded ids present, set-equal to the receipt line.
   Cross-rev: `for rev in 8d3badd ede486b; do timeout 200 python3 tools/mori-sources-appendonly.py $rev --repo . 2>&1 | grep -E '^supersede_timing'; done`
   → the same 35-id line at both revs.
6. Python: parse all `evidence/c10-*.txt` and `c11-*.txt` verdict lines (table quoted above):
   C11 as_of = 18 (before), 35 (tip), 33+stale 1 (`e37dcc6`), 0/0/0 (v2 DAGs), 1/1/1 (v3
   DAGs); C10 before met×9 + exit 2 + 8/0, after unmet×9 + 0/10 + 11/0.
7. `python3 .ufo/waves/round-40/fixtures/run-c11-dags.py tools/mori-sources-appendonly.py "$PWD" /tmp/rev-routed-v3.txt dag-n dag-p dag-r`
   and the same with `.ufo/waves/round-40/fixtures/extracted/gate-v2-bb1f2457.py`; verdict
   lines quoted under F3 (v3 EXIT 0/1/1; v2 EXIT 0/1/1).
8. `python3 tools/mori-sources-appendonly.py --selftest` →
   `MORI_SOURCES_APPENDONLY_SELFTEST pass=15 fail=0`, `EXIT=0`.
9. `grep -n "P-C7\|honest and mutated\|expected (want)\|want table" corpus/lessons/round-39-erratum.md`
   → no output, exit 1; `git show 265a955cc:corpus/lessons/round-39-erratum.md | sha256sum`
   equals the worktree sha `5cfea377…`.
10. `grep -n "19 ids" .ufo/waves/round-40/contract.md tools/mori-sources-appendonly.py`
    → contract:119, :137, :145; gate:87.
    `grep -n "34 as-of ids\|as-of ids" SCORECARD.md corpus/lessons/round-40.md`
    → `SCORECARD.md:2234` ("measured value is **34 as-of ids** at T1") and
    `corpus/lessons/round-40.md:24` (M24: "lists **34** as-of ids").
11. `printf '%s' 'you can ask for commits that are reachable from r2 excluding those that are reachable from r1' | wc -w`
    → `17`; `grep -n 'bypass-wait likewise' SCORECARD.md` → `2199`.
12. `git status --porcelain -- .ufo/waves/round-40/evidence ...` → 3 M files;
    `git diff HEAD -- <those files>` → command-line/timing-only changes.

## Bottom line

Closure defects **1, 2, and 4 are named with receipts that discharge them**. Closure defect
**3 is only half discharged**: its first-parent/re-add semantics are correct and
receipt-demonstrated, but its "unreachable count prose / one source of truth" half is not —
the frozen predicate and after-cell say 19, the lesson/SCORECARD correction says 34, and the
cited receipt plus three independent measurements say 35. Lesson finding **1** is claimed
discharged by an erratum paragraph that does not exist. Both are prose/record defects, not
gate-mechanism failures.
