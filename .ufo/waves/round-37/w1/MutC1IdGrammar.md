# MutC1IdGrammar — per-id grammar check (`same_id_lines`) mutation probe

Attacks: C1's summary-only discrimination, i.e. the per-id `changed`/`deleted`
equality check `same_id_lines` in `.ufo/waves/round-37/count-c1.py:566` (r36 debt
(c), "per-id `deleted <id>` line checks"). One plausible defect: disable that
check and see whether summary-only is accepted.

## Mutant

Scratch copy only; the lane file was never edited.

- pristine copy: `/fast/scratch/hyaku/mori-r37/MutC1IdGrammar/count-c1-pristine.py`
- mutant copy: `/fast/scratch/hyaku/mori-r37/MutC1IdGrammar/count-c1-mutant.py`

Single-point mutation (`mutation.diff`):

```diff
 def same_id_lines(got, want):
     changed, deleted, malformed = got
-    return (malformed == 0
-            and sorted(changed) == sorted(want["ids"])
-            and sorted(deleted) == sorted(want["deleted"])
-            and len(changed) == len(set(changed))
-            and len(deleted) == len(set(deleted)))
+    return True
```

`python3 -m py_compile` on the mutant: rc 0.

## Detector (same bounded run on pristine / mutant / restored)

```
cd /home/vgpnk/Projects/shokunin/mori-shokunin
python3 <scratch>/count-c1-{pristine|mutant}.py \
  e57c58b57c025364e79d130fbdf764d2674d83d6 \
  --tool /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-37/fixtures/summary-only.py \
  --seed 7777
```

Pass/fail signal: the summary-only fixture must be rejected — its negative line
must say `rejected` and the primary blind arm must fail on `per-id lines differ`.
The mutation's expected flip is `ACCEPTED` / blind 24/24 on exactly those arms.
Fixed seed 7777 for replayability; outputs: `baseline.txt`, `mutant.txt`,
`restored.txt`, `baseline2.txt` (repeat run, identical).

## Observed outputs

### 1. Pristine bytes (baseline)

```
blind arm: 2/24 sandbox histories matched the hidden truth (2.8s; coverage: deletions=22 changed-back=17 superseded=10)
  repo00 FAIL: per-id lines differ (malformed=0)
      want: changed=['S034'] deleted=['S072']
      got:  changed=['S034'] deleted=[]
  ... (20 more blind FAILs, all "per-id lines differ", each with want deleted=[...] / got deleted=[])
real arm: pass (0.3s)
challenge arm (real-arm clothing): FAIL (0.1s)
  reason: per-id lines differ: want changed=['S258', 'S285'] deleted=['S119', 'S176'] got changed=['S258', 'S285'] deleted=[]
negative memo-n1.py     rejected (challenge: lists differ: ...)
negative const.py       rejected (blind 4/4 (repo200: lists differ))
negative summary-only.py rejected (blind 4/4 (repo200: per-id lines differ (malformed=0)))
C1=unmet
seed=7777
EXIT=1
```

Baseline is conclusive: summary-only is rejected on the blind arm (22/24 draws
carry `deleted` witnesses; the 2 passes are the draws with no deletion, coverage
`deletions=22`) and on the negative fixture. The real arm passes even on
pristine because the lane truth has `deleted=[]`, so the real arm alone cannot
discriminate this fixture — the blind/challenge arms carry the kill.

### 2. Mutated bytes (`same_id_lines` → `True`)

```
tool: .ufo/waves/round-37/fixtures/summary-only.py
blind arm: 24/24 sandbox histories matched the hidden truth (2.4s; coverage: deletions=22 changed-back=17 superseded=10)
real arm: pass (0.3s)
challenge arm (real-arm clothing): pass (0.1s)
negative memo-n1.py     rejected (challenge: lists differ: ...)
negative const.py       rejected (blind 4/4 (repo200: lists differ))
negative summary-only.py ACCEPTED (all three arms pass)
C1=unmet
seed=7777
EXIT=1
```

Flip confirmed: summary-only goes from rejected (2/24 blind, challenge FAIL,
negative `rejected`) to accepted (24/24 blind, challenge pass, negative
`ACCEPTED`). All 22 blind histories that carry `deleted` witnesses flipped to
pass; the two deletion-free draws are unchanged. `C1=unmet` here is the
consequence of the counter now accepting a negative (`all(rejected)` is False),
not the honest gate failing.

### 3. Restored bytes (pristine copied back)

```
blind arm: 2/24 sandbox histories matched the hidden truth (2.7s; coverage: deletions=22 changed-back=17 superseded=10)
real arm: pass (0.3s)
challenge arm (real-arm clothing): FAIL (0.1s)
  reason: per-id lines differ: want changed=['S258', 'S285'] deleted=['S119', 'S176'] got changed=['S258', 'S285'] deleted=[]
negative memo-n1.py     rejected (challenge: lists differ: ...)
negative const.py       rejected (blind 4/4 (repo200: lists differ))
negative summary-only.py rejected (blind 4/4 (repo200: per-id lines differ (malformed=0)))
C1=unmet
seed=7777
EXIT=1
```

Byte-identical to the baseline run (same seed): summary-only is rejected again.

## Verdict against the assignment

The mutation flips summary-only to accepted on the primary blind arm (2/24 →
24/24), on the challenge arm (FAIL → pass), and on the negative fixture
(`rejected` → `ACCEPTED`). The per-id grammar check is therefore load-bearing
for C1's summary-only discrimination. No surviving mutant.

## Restoration evidence

```
86699627c7627cc3eea3ba9ea952079d081db390f9ba2be1e1d4d685dd98cdae  count-c1-pristine.py
86699627c7627cc3eea3ba9ea952079d081db390f9ba2be1e1d4d685dd98cdae  count-c1-mutant.py   (restored)
86699627c7627cc3eea3ba9ea952079d081db390f9ba2be1e1d4d685dd98cdae  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-37/count-c1.py  (lane, unchanged)
cmp -s pristine mutant -> RESTORED_BYTES_IDENTICAL=yes
```

Mutant hash while mutated: `a48c9e9dd7ef4adb3ea9ad84aedd5fd8a9675e74c1def8dc5cc3c20375050818`.
Fixture hash (never modified): `d88c9eb648df24548520716682f8b5b68702a46dafdd7a645b270d81ee80f9c9`.
Lane `count-c1.py` was never written; the counter's own challenge/scratch dirs
under `.ufo/waves/round-37/scratch/` were removed by its `finally` (directory
observed empty after every run). All scratch artifacts live under
`/fast/scratch/hyaku/mori-r37/MutC1IdGrammar/`.

Note: a first baseline attempt passed `--tool .ufo/...` repo-relative; the
counter runs the tool with the sandbox repo as cwd, so the relative path failed
to open (`can't open file '//.ufo/...'`) and produced exit 2 per draw. Re-run
with the absolute fixture path; all measurements above use absolute paths.

Installs/updates: none.

VERDICT: PASS
