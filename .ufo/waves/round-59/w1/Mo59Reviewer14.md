# Mo59Reviewer14 — frozen-byte integrity + adversarial counter review

Seat scope: sha256 the frozen contract, both counters, both tools at the freeze
revision and the working tree; report equality or divergence; return one
adversarial finding or an explicit no-counterexample with bounded method.
Read-only; no production edits. Scratch:
`/fast/scratch/hyaku/mori-r59/Mo59Reviewer14` (cleaned before yield).

## 1. Frozen-byte integrity — VERDICT: EQUAL, PINs verified end-to-end

Freeze revision `60b3a76ad0524c8978cc51922940be1c8c388915` (amended freeze;
initial `ccfd554e64084a0b4370806dd12a850e0a7bd7db`, entering
`2b9f03975bfb6e508f35074ac8181ec8bf54e805`, observed HEAD
`7b86704d7c0754a09958d131b64dbfa2a6d3eaed`).

Method: `sha256sum` on the working-tree file vs
`git -C $L show <rev>:<path> | sha256sum`, two passes bracketing this session.

| path | working tree == freeze `60b3a76` | == initial `ccfd554e` | sha256 (wt) |
|---|---|---|---|
| `.ufo/waves/round-59/contract.md` | **EQUAL** | diverge (amendment) | `427fca0b…107e` |
| `.ufo/waves/round-59/count-c1.py` | **EQUAL** | diverge (amendment) | `2be6fda8…9dfd` |
| `.ufo/waves/round-59/count-c2.py` | **EQUAL** | diverge (amendment) | `2df3ae84…77be` |
| `tools/mori-register-check.py` | **EQUAL** | diverge (amendment) | `38b733d896f880f5b7ecb464848b80798810ab052fcf0a8afb320918151472b8` |
| `tools/mori-settlement-scan.py` | **EQUAL** | **EQUAL** | `4c04bf2170b0484192dd157ee04851e8243e030c54046c5e8806d46eea5ac9a9` |

- Both tool hashes equal the contract's abbreviated PINs **and** the counters'
  `PIN` constants (`count-c1.py:34` / `count-c2.py:56`). Contract ↔ counter ↔
  tool-bytes all agree.
- The four divergences vs `ccfd554e` are exactly the documented amendment:
  `git diff --stat ccfd554e..60b3a76` touches only `contract.md` (±1 line),
  `count-c1.py` (+3/−2), `count-c2.py` (±2 lines), `tools/mori-register-check.py`
  (+4/−2) — matching commit message "counter scratch-mkdir + ls-tree rev:path +
  register name boundary". C2 tool untouched.
- All five paths ABSENT at entering `2b9f0397` (`git cat-file -e`), present at
  both freeze commits. `2b9f0397` is ancestor of `60b3a76`; `60b3a76` is
  ancestor of HEAD.
- Re-hash at session end: all five still EQUAL — no drift under concurrent
  seat work. No stray `count-*` leftovers in the frozen dir
  (only `contract.md count-c1.py count-c2.py evidence fixtures-c1 trees-c2`).

## 2. Counter behavior at boundary revisions — controls reproduce exactly

All runs read-only (`git show`/`cat-file`/`ls-tree` at explicit revisions),
materialization under `--scratch`, `TMPDIR` under my scratch:

```
python3 count-c1.py 2b9f0397…  --scratch c1-entering
→ C1=unmet selftest=bad fixtures=bad real=bad pointers=bad rev=2b9f0397…
  failed=tool_absent,selftest,fixtures_absent,real,pointers        exit=1   ✓ frozen before-state
python3 count-c1.py 60b3a76…  --scratch c1-freeze
→ C1=met selftest=ok fixtures=ok real=ok pointers=ok rev=60b3a76…  exit=0   ✓ frozen target verbatim
python3 count-c1.py 7b86704d… --scratch c1-head
→ C1=met selftest=ok fixtures=ok real=ok pointers=ok rev=7b86704d… exit=0
python3 count-c2.py 2b9f0397…  --scratch c2-entering
→ C2=unmet … claims=0 files=0 failed=tool_absent,copy_absent:*,…,trees_absent exit=1  ✓
python3 count-c2.py 60b3a76…  --scratch c2-freeze
→ C2=unmet selftest=ok scan=ok drift=ok trees=ok entry=bad rows=bad pins=bad
  tree=bad claims=0 files=0  exit=1   ✓ instrument pre-satisfied, depth pending
python3 count-c2.py 7b86704d… --scratch c2-head
→ C2=met selftest=ok scan=ok drift=ok trees=ok entry=ok rows=ok pins=ok
  tree=ok claims=13 files=6  exit=0   ✓ frozen target verbatim (N=13≥10, F=6≥3)
count-c1.py --selftest → C1_SELFTEST pass=6 fail=0  exit=0  ✓
count-c2.py --selftest → C2_SELFTEST pass=9 fail=0  exit=0  ✓
```

## 3. Adversarial probes — no counterexample found

**C1 fixture battery (13/13 dirs at freeze, matching contract).** Per-fixture
tool runs at the freeze revision, full `reasons` captured vs each frozen
`expect.txt` prefix: every fixture scored `REGISTER_UNMET`, exit 1, every
expect token covered by a defect-specific reason, **zero vacuous tokens**
(token never satisfied by the no-input baseline `scorecard_unreadable`).
Defect specificity confirmed, e.g. `f03` → `keys:duplicate=…`, `f06` →
`pointers:bad=/etc/passwd`, `f07` → `pointers:bad=../../etc/passwd`,
`f10` → `manifest:lane='kotoba'`, `f13` → `pointers:none=…`.

**C2 hostile-tree battery (12/12 dirs at freeze, matching contract).**
`eval_entry` per tree at the freeze revision: every tree evaluated UNMET
(`ok=False`), every expect prefix covered, **zero vacuous tokens** vs the
empty-dir baseline (`entry_absent`). t05 `claims_min` fires at 7 claims;
t12 `grammar` fires on malformed claim lines.

**Amendment scope.** `ccfd554e..60b3a76` diff is surgical — exactly the four
named files; nothing else touched. Freeze-integrity kill rule intact.

**Schema consistency.** `corpus/SOURCES.md` rows are 11 cells; real `mined`
rows show cell[7]=`mined`, cell[10]=used-by — the counter's `cells[7]=="mined"`
/ `cells[10]==ENTRY` gates are correct-column (`eval_entry`, `count-c2.py`).

## 4. Findings (severity-ordered)

### F1 — MEDIUM (disclosed design, reported for the record): C1 met-arm fully pre-satisfied at the freeze commit; C2 instrument arms likewise
`count-c1.py 60b3a76…` prints the byte-exact frozen target `C1=met …` exit 0 —
the tool, 13 fixtures, register rows, pointers and MANIFEST binding all
satisfied **at the freeze commit itself**, 105 s after the entering revision.
`count-c2.py` at freeze likewise passes tool/selftest/scan/drift/trees; only
the depth-data arms (entry/copies/rows) were pending and are now met at HEAD.
Consequence: no wave activity can change `C1=met`, and C2's met reduces to
landing the entry + copies (which seats did: claims=13 files=6). The contract
discloses this ("pre-data" in the amendment message; before-control defined at
entering), so it is not a kill-rule violation — but calibration value rests
wholly on hostile-fixture discrimination, which §3 verified non-vacuous.

### F2 — LOW: `count-c2.py` real-arm `entry_ok` gate drops the `grammar` reason family — production arm looser than hostile arm
- `eval_entry` appends `grammar:` for malformed claim-like lines
  (`count-c2.py:121-122`) and returns strict `ok=False`.
- In `measure()` the strict result `entry_ok_all` (`:300`) is computed then
  **discarded**; the gate list (`:303-304`) excludes only
  `frontmatter|distinct|claims_min|files|span|entry_absent` — `grammar` escapes.
- The hostile arm (`:347-351`) uses strict `ok != want_ok`, so tree t12
  (malformed claim) is correctly UNMET there.
- Empirical proof (synthetic tree under scratch): 10 valid claims + line
  `- **K99** — typo line. Quote: \`x\` (no-pin-here)` →
  `eval_entry ok=False reasons=['grammar:…']` yet real-arm gates
  `entry_ok=True rows_ok=True pins_ok=True`. Same bytes → UNMET under the
  t12 arm. Effect: a shipped entry can carry malformed claim-like padding
  without the counter noticing. Frozen; report-only.

### F3 — LOW/cosmetic cluster
- Dead `got` comprehension `count-c1.py:155-157` (computed, never used) —
  suggests an abandoned normalization; actual matching is raw `startswith` (`:158`).
- `count-c2.py:295-298` `have_all` failure path drops reason detail: a missing
  `SOURCES.md`/copy flattens entry/rows/pins to `bad` with only
  `entry_absent`/`copy_absent` tokens (no dedicated `sources_absent` reason in
  the counter output for that path).
- C1 bound-name check is prefix-only `bmap[k].startswith(v)` (`count-c1.py:200`)
  rather than equality — inert because the tool already enforces exact
  name binding (f08 altered / f09 substring-only both fail `manifest:name`).

## 5. Residual risk / bounded method

No counterexample to frozen-byte integrity or counter soundness within this
method: (a) sha256 over 5 files × {wt, freeze, initial-freeze} + presence at
entering; (b) counter runs at entering/freeze/HEAD both claims; (c) per-fixture
reason capture across all 13+12 hostile inputs with baseline-vacuity test;
(d) one synthetic grammar-gate construction; (e) amendment diff-scope; (f) two
bracketing hash passes against concurrent drift.

Not exercised: exhaustive fuzz of `eval_entry` grammar (beyond one constructed
case), C1 tool against fixture-subset combinations, counter-level mutation
battery (mutation-tester seats' scope), any `R` beyond the three tested
revisions. F1/F2/F3 are the complete finding set.

No production files, corpus, registry, SCORECARD, LOG, or lane VCS touched.
Receipts (counter outputs above) copied into this report; scratch removed.
