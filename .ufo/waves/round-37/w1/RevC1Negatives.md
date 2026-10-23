# RevC1Negatives — each negative fixture re-run alone vs count-c1 (seed 11, rev e57c58b)

Scope: re-run each of the three frozen C1 negative fixtures in isolation (`--tool`) against
`.ufo/waves/round-37/count-c1.py e57c58b57c025364e79d130fbdf764d2674d83d6 --seed 11`, and verify the
rejection detail names the intended arm: memo-n1 → CHALLENGE (real+blind pass), summary-only →
per-id check on the blind arm, const → blind arm.

## Setup verification (before trusting the runs)

The counter loads negative fixtures from the working tree (`NEGATIVES_DIR`,
count-c1.py:890-896) and never re-verifies the freeze pins, so I verified them manually. Lane
working tree had no tracked modifications under `.ufo/waves/round-37/` (`git status --porcelain`
shows only untracked `w1/*.md` seat reports); `git hash-object` over the frozen paths:

```
19324701f23a225e5ded21c4785c491e7530ac7c  fixtures/memo-n1.py      == pin (evidence/freeze-r37.txt)
2f3993a04906ce33033ab207a284d9ca7d7ff57a  fixtures/const.py        == pin
2d62f742fbef39634a5ff04e25b399b87ce4c941  fixtures/summary-only.py == pin
7518fef8f54afff69ee38a99f2acbf518006f5ad  count-c1.py              == pin
```

Runs judged the frozen bytes. Lane repo untouched (read-only git only).

## Run 1 — memo-n1.py (must be rejected by the CHALLENGE arm)

Command: `python3 .ufo/waves/round-37/count-c1.py e57c58b57c025364e79d130fbdf764d2674d83d6 --tool .ufo/waves/round-37/fixtures/memo-n1.py --seed 11` → exit 1 (`C1=unmet`).

Observed (decisive lines):

```
tool: .ufo/waves/round-37/fixtures/memo-n1.py
blind arm: 24/24 sandbox histories matched the hidden truth (2.6s; coverage: deletions=17 changed-back=14 superseded=9)
real arm: pass (0.2s)
  tool:   appendonly_violations=18 ids=[S041,...,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]
  oracle: appendonly_violations=18 ids=[S041,...,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]
challenge arm (real-arm clothing): FAIL (0.1s)
  truth:  appendonly_violations=1 ids=[] deleted=[S109] superseded=[] round_changed=[S025]
  tool:   appendonly_violations=18 ids=[S041,...,S193] ...   (the published constant)
  reason: lists differ: want appendonly_violations=1 ... got appendonly_violations=18 ...
negative memo-n1.py     rejected (challenge: lists differ: want appendonly_violations=3 ids=[S116,S180] deleted=[S252] superseded=[S180] round_changed=[S116,S252] got appendonly_violations=18 ...)
```

Verification: blind 24/24 pass and real arm pass — the memoizer is honest everywhere it can key
on — and both the isolated arm run and the per-fixture detail name `challenge:`. The clothing
(lane path/identity/title under `CHALLENGE_PARENT`, count-c1.py:747-788) defeats it, and the
challenge truth comes from the counter's op log, not the receipt. Expected arm named: CHALLENGE. ✓

## Run 2 — const.py (must be rejected by the blind arm)

Command: `python3 .ufo/waves/round-37/count-c1.py e57c58b57c025364e79d130fbdf764d2674d83d6 --tool .ufo/waves/round-37/fixtures/const.py --seed 11` → exit 1 (`C1=unmet`).

Observed (decisive lines):

```
tool: .ufo/waves/round-37/fixtures/const.py
blind arm: 0/24 sandbox histories matched the hidden truth (1.1s; ...)
  repo00 FAIL: lists differ
      want: appendonly_violations=5 ids=[S098] deleted=[S047,S096,S101,S287] superseded=[S098] round_changed=[S047,S096,S098,S101,S287]
      got:  appendonly_violations=18 ids=[S041,...,S193] ...   (constant, all 24 repos identical)
real arm: FAIL (0.2s)   [summary lists match, but per-id lines differ]
  diff: per-id lines: want changed=[S041,...,S193] deleted=[] got changed=['S041'] deleted=['S069'] (malformed=0)
challenge arm (real-arm clothing): FAIL (0.1s)
negative const.py       rejected (blind 4/4 (repo200: lists differ))
```

Verification: the negative-section detail names the blind arm first (`run_negative` orders
blind → real → challenge, count-c1.py:809-829), on 4 pre-drawn sandboxes repo200–203 shared by all
fixtures (count-c1.py:924-926). Expected arm named: blind. ✓

## Run 3 — summary-only.py (must be rejected by the per-id check on the blind arm)

Command: `python3 .ufo/waves/round-37/count-c1.py e57c58b57c025364e79d130fbdf764d2674d83d6 --tool .ufo/waves/round-37/fixtures/summary-only.py --seed 11` → exit 1 (`C1=unmet`).

Observed (decisive lines; blind printed 7/24 with 17 repo failures, all per-id):

```
tool: .ufo/waves/round-37/fixtures/summary-only.py
blind arm: 7/24 sandbox histories matched the hidden truth (2.6s; ...)
  repo00 FAIL: per-id lines differ (malformed=0)
      want: changed=['S098'] deleted=['S047', 'S096', 'S101', 'S287']
      got:  changed=['S098'] deleted=[]
  ... repo01,02,03,04,06,07,08,10,12,13,14,16,18,20,21,22 all: per-id lines differ (malformed=0)
real arm: pass (0.3s)
challenge arm (real-arm clothing): FAIL (0.1s)
  reason: per-id lines differ: want changed=[] deleted=['S109'] got changed=[] deleted=[]
negative summary-only.py rejected (blind 4/4 (repo200: per-id lines differ (malformed=0)))
```

Verification: the fixture's summary lists are correct (real arm passes, lists match) but the
omitted `deleted <id>` lines are caught by `same_id_lines` inside `check_blind`
(count-c1.py:658-668); every blind failure reason is `per-id lines differ`, and the per-fixture
detail names `blind ... per-id lines differ`. Expected arm named: per-id check on the blind arm. ✓

## Cross-run integrity

The three invocations executed concurrently. The negative-section lines (`negative memo-n1.py …`,
`negative const.py …`, `negative summary-only.py …`) are byte-identical across all three outputs,
and const/summary blind truths per repo index are identical — deterministic under seed 11 and no
scratch collision (mkdtemp per arm, count-c1.py:832-845; r36 debt g holds). Note `--tool` runs the
named fixture through the three arms *in addition to* the counter's unconditional re-judgment of
all three frozen fixtures (count-c1.py:889-896, 923-933); the acceptance criteria are satisfied by
both the isolated arm sections and the per-fixture detail lines.

## Findings by severity

No defect found. All three rejections name the arm the acceptance expects, with the exact
arm-ordering logic at count-c1.py:809-829 (`blind %d/%d (repo%02d: …)` → `real arm fails` →
`challenge: %s` → `all three arms pass`).

## Residual risk / observations (no verdict impact)

1. `real_arm` (count-c1.py:723-745) does not check the child's exit code, while `check_blind`
   (count-c1.py:677-680) and `challenge_arm` (count-c1.py:781-782) enforce
   `expected_exit = 1 if round_changed else 0`. For memo-n1 this is moot — the lane real-arm truth
   has nonempty `round_changed=[S182,S193]` so the expected exit is 1 and memo-n1 exits 1 — and any
   wrong-exit tool is still caught by the blind arm, which always runs. Observed, not attacked
   further (out of this seat's scope).
2. The counter trusts the working-tree fixtures/counters (no pin re-verification at run time);
   mitigated here by the manual hash match above, but a dirty tree would silently re-judge
   unfrozen bytes.

## Verification gaps

None within scope. Each fixture was run once per the assigned command (three concurrent
invocations, seed 11); determinism across those three independent processes is the only replay
evidence. No tool installs were made.

VERDICT: PASS
