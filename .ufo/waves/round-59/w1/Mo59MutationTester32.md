# Mo59MutationTester32 — C2 counter mutation probe (round 59, w1)

Assignment: mutate a scratch copy of `.ufo/waves/round-59/count-c2.py` — (M1)
remove the grammar arm, (M2) accept `len(cells)>=11`, (M3) drop the pin check,
(M4) all three — and construct entries that false-green under the mutants.
Mode: read-only on the lane. All mutants, roots, fixture repos and run state
lived under `/fast/scratch/hyaku/mori-r59/Mo59MutationTester32/` (cleaned after
this report; receipts inlined below). No lane/fleet VCS mutation; no subagents.
Disk guard green at start (27% use, 593G free). No tools installed.

Baseline bytes (never modified, verified unchanged at end):
- `count-c2.py` sha256 `2df3ae84f6d66f9ee46cd46cf2cb199ca85e7400301c5a0e9dd94b7b375877be`
- `contract.md` sha256 `427fca0bf2a928133c09b37746e58a2d98c6c551651046f31320531a43de107e`
- freeze rev `60b3a76ad0524c8978cc51922940be1c8c388915`; lane HEAD during runs
  `7b86704d7c0754a09958d131b64dbfa2a6d3eaed` (mid-wave; tool+entry landed, tool
  sha equals frozen PIN `4c04bf21…ac9a9`).

## Mutants (smallest behavior-bearing points, pristine line numbers)

| id | site | change |
|----|------|--------|
| M1 | count-c2.py:121-122 | delete grammar-arm append (heuristic `if "**K" in ln …`) |
| M2 | count-c2.py:183 | `if len(cells) != 11:` → `if len(cells) < 11:` |
| M3 | count-c2.py:148-149 | delete `if sha256(fb) != pin: reasons.append("pin:%s")` |
| M4 | all three | combined, as assigned |

Diffs (11/11/11/29 lines, saved as runs/diff-M{1,2,3,4}.patch before cleanup):

```diff
--- M1/M4 hunk 1 (@@ -118,8)
     m = CLAIM.match(ln)
     if not m:
-        if "**K" in ln or (ln.lstrip().startswith("-") and "Quote:" in ln):
-            reasons.append("grammar:%.40s" % ln.strip()[:40])
         continue
--- M2/M4 hunk 3 (@@ -180,7)
-            if len(cells) != 11:
+            if len(cells) < 11:
--- M3/M4 hunk 2 (@@ -145,8)
         except OSError:
             reasons.append("pin:copy_absent=%s" % cfile)
             continue
-        if sha256(fb) != pin:
-            reasons.append("pin:%s" % kid)
```

Mutant identity at run time: each mutant was verified against the pristine copy
by the unified diffs above (exact hunk content) and by behavior (R2-R4); no
mutant byte was ever written to the lane.

## Detector protocol (bounded)

Same detector on pristine / mutated / restored bytes, three layers:
1. `eval_entry` harness (probe.py, importlib; no subprocess) on 5 synthetic
   roots (R-good control, R-pin-wrong, R-row-extra [t08-style trailing 12th
   cell], R-grammar [extra malformed K-line], R-all) + the 12 frozen hostile
   trees materialized from the freeze rev (`git archive 60b3a76:.ufo/waves/round-59/trees-c2`).
2. Full counter CLI at freeze rev and at HEAD (read-only `git show` only).
3. End-to-end: sandbox fixture repo at an explicit scratch path
   (`mktemp -d -p <seat-scratch>` + `git -C "$F" init -q`; all runs
   `git -C "$F"`), containing the HEAD blobs for TOOL, 6×REAL_SCAN+DRIFT, 6
   copies, SOURCES, entry, and the 12 hostile trees; counter driven with
   `--repo "$F"`.

Restoration cycle: `work/count-c2.py` was M4 bytes → probed → restored from
pristine → sha256 re-verified `2df3ae84…877be` → probed again (results
identical to pristine variant). Lane counter/contract sha256 re-checked after
all runs: unchanged (values above).

## Results

### R1 — counter selftest is blind to all four mutants
`python3 <variant> --selftest` → `C2_SELFTEST pass=9 fail=0`, rc=0 for
pristine, M1, M2, M3, M4 alike. The 9 selftest checks exercise the CLAIM regex,
constants and a synthetic good/frontmatter-less tree; none exercises the
grammar arm, row width, or pin equality. Contract line 84 expects `pass=9
fail=0` — the mutant passes the frozen selftest unchanged.

### R2 — full counter: every mutant is killed, fail-closed (no C2-level false green)
At HEAD `7b86704d` (identical inputs, only counter bytes differ):

```
pristine  : C2=met   selftest=ok scan=ok drift=ok trees=ok  entry=ok rows=ok pins=ok tree=ok claims=13 files=6 rc=0
M1        : C2=unmet … trees=bad … failed=tree:t12-malformed-claim:reasons,trees            rc=1
M2        : C2=unmet … trees=bad … failed=tree:t08-extra-cell-row:verdict,trees             rc=1
M3        : C2=unmet … trees=bad … failed=tree:t04-stale-pin:verdict,trees                  rc=1
M4        : C2=unmet … trees=bad … failed=tree:t04-stale-pin:verdict,tree:t08-extra-cell-row:verdict,tree:t12-malformed-claim:reasons,trees rc=1
```

At freeze rev `60b3a76a` pristine is unmet (`failed=copy_absent×6,entry_absent,tree`;
the tool+scans pre-exist there, so `selftest=ok scan=ok drift=ok`) and M4 adds
`tree:t04-stale-pin:verdict,tree:t08-extra-cell-row:verdict,tree:t12-malformed-claim:reasons,trees`.
The three mutated checks are each load-bearing and non-redundant: removing any
of them flips the corresponding frozen hostile tree (count-c2.py:347-352 verdict
+ expect-prefix check), so the counter detects its own mutation and fails
closed. **Verdict per mutant: killed.**

### R3 — frozen-tree verdict flips under M4 (eval_entry level)
9/12 trees byte-identical behavior, expect-prefix covered under both variants.
Flips exactly where predicted:

| tree | expect | pristine | M4 |
|------|--------|----------|----|
| t04-stale-pin | pin | ok=false `pin:1` | **ok=true** (verdict flip) |
| t08-extra-cell-row | rows:bad_row | ok=false `rows:bad_row=S901` | **ok=true** (verdict flip; extra cell is trailing so cells[7]/cells[10] stay valid) |
| t12-malformed-claim | grammar | ok=false `grammar:…,claims_min:9` | ok=false but `claims_min:9` only — **expect prefix `grammar` no longer producible** |

### R4 — arm-level false greens: constructed entries the mutants accept
`eval_entry` flags recomputed exactly as measure() does (count-c2.py:303-307,
`met` at 360-361):

| root | pristine | best mutant |
|------|----------|-------------|
| R-good (control) | ok=true, [] | unchanged (no false alarms introduced) |
| R-pin-wrong (10 claims, pin=b×64) | ok=false, `pin:1…pin:10`, pins=false | M3/M4: **ok=true, pins=true** → counter would print `pins=ok` |
| R-row-extra (trailing `| extra |` 12-cell row) | ok=false, `rows:bad_row=S901`, rows=false | M2/M4: **ok=true, rows=true** |
| R-grammar (10 valid + malformed K11, no `; pin`) | ok=false, `grammar:…` | M1/M4: **ok=true, zero trace** |
| R-all (all three defects) | ok=false, 12 reasons (rows=false, pins=false) | M4: **ok=true, 0 reasons** — complete arm-level false green |

Mutated-then-restored work copy: mutated pass reproduced M4 (R-all ok=true);
restored pass (sha256 `2df3ae84…877be` re-verified) reproduced pristine (R-all
ok=false, `grammar:…,pin:1…,rows:bad_row`).

## F1 — adversarial finding on PRISTINE bytes: malformed claim lines are invisible at met level

Discovered while attributing M1: the grammar arm feeds only the internal
`ok` flag. The met-level filter at count-c2.py:303-305 accepts reasons with
prefixes `frontmatter|distinct|claims_min|files|span|entry_absent` — `grammar`
is **not** in the list, and `met` (360-361) never consults the raw `ok`. So a
real entry may carry any number of malformed `**K…` lines; they are silently
not counted as claims, and C2 still evaluates met as long as ≥10 valid claims
remain. The grammar check is enforced only inside the hostile-trees arm
(t12), never on the scored entry itself.

End-to-end proof (scratch fixture repo, pristine counter, HEAD blobs):

```
A  entry verbatim (lane HEAD):        C2=met  … trees=ok entry=ok rows=ok pins=ok tree=ok claims=13 files=6  rc=0
B  entry + appended malformed line
   `- **K99** — malformed trailing claim. Quote: ` "seats": 64,`
     (corpus/evidence/sources-r59/w1-results-r56.json:line:5)`  (no `; pin …`):
                                       C2=met  … trees=ok entry=ok rows=ok pins=ok tree=ok claims=13 files=6  rc=0
C  same rev, M4 counter:              C2=unmet failed=tree:t04-stale-pin:verdict,tree:t08-extra-cell-row:verdict,trees rc=1
```

B is the false green: a hostile edit to the scored entry leaves C2=met on
pristine bytes. Impact bounded — the malformed line contributes no claim
(claims stays 13, span/pin checks still apply to valid claims), so this
weakens entry hygiene enforcement, not the ≥10-byte-exact-claims predicate
itself. Coverage finding only; per role I do not propose contract changes.

## Verdicts

- M1, M2, M3, M4: **killed** — each flips frozen hostile trees t12/t08/t04
  respectively (count-c2.py:348 verdict / :352 prefix check); counter fails
  closed, exit 1, at both freeze rev and HEAD. No C2-level false green exists
  for these mutations.
- Arm-level false greens demonstrated for each removed check (R4) — the
  `entry/rows/pins=ok` tokens in the frozen target output are exactly the
  arms the mutants defeat on constructed inputs.
- Surviving coverage findings: (F1) grammar reasons never fail the scored
  entry at met level (count-c2.py:303-305 vs :360-361); (R1) frozen selftest
  (`pass=9 fail=0`) passes identically on all four mutants.
- Inconclusive: none. Baseline detector on pristine bytes behaved as frozen
  contract expects (12/12 hostile trees unmet with their expect prefixes).

## Restoration evidence

- Lane `.ufo/waves/round-59/count-c2.py` before and after all runs:
  `2df3ae84f6d66f9ee46cd46cf2cb199ca85e7400301c5a0e9dd94b7b375877be` (equal).
- Lane `.ufo/waves/round-59/contract.md` before and after:
  `427fca0bf2a928133c09b37746e58a2d98c6c551651046f31320531a43de107e` (equal).
- Work copy mutated (M4 bytes) → probed → restored → sha256 equal to lane
  original → probe reproduced pristine results.
- Scratch root `/fast/scratch/hyaku/mori-r59/Mo59MutationTester32/` (mutants,
  roots, fixture repo `tmp.PbNNwBMi43`, run state) removed after this report.
