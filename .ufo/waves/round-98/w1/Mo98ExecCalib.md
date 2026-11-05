# Mo98ExecCalib — independent C2 calibration check (mori r98 wave w1)

Role: executor. Scope: independent verification of C2 **without** the lane gate as the expectation source; plus gate `--selftest` and gate-bytes-unchanged corroboration. C1 untouched. No file outside this report and my scratch was written; no git/jj mutation; no sudo, no sysctl or host-state change; no tools installed.

## Method

Own checker (scratch `check_c2.py`, removed on finish): expectation from `/home/vgpnk/Projects/shokunin/MANIFEST.json` — rows with `lane=='mori'`, `type=='closure'`, `admitted==true`; per axis the highest `round` with `verdicts[axis] in ('improved','harmed')`. Observed: leading `round N (verdict` of the last cell (Last change) of each axis row in `## Axes` of `SCORECARD.md` extracted read-only via `git -C /home/vgpnk/Projects/shokunin/mori-shokunin show <rev>:SCORECARD.md` into scratch, for entering `b2a67ce562bbf2f0cc73f47d8e79f792badf5e63` and landing `600deb7ed2695f54b289cf5b6c3931e0fa9c8bb3`.

## Result table (axis | expected | entering lead | landing lead | ent match | lnd match)

```
axis | expected | entering lead | landing lead | ent match | lnd match
coverage | 80 | r80 (improved | round 80 (improved, score held); … | True | True
operability | 97 | r93 (improved | round 97 (improved, score held); round 93 … | False | True
depth | 86 | r86 (improved | round 86 (improved, score held); … | True | True
freshness | 97 | r82 (improved | round 97 (improved, score held); round 82 … | False | True
calibration | 93 | r93 (improved | round 93 (improved, score held); … | True | True
adjacency | 19 | r19 (improved | round 19 (improved, score held) | True | True

entering mismatches=2 landing mismatches=0
```

Score and Evidence-pointer cells, entering vs landing, all six rows: identical (`score_evidence_columns_unchanged=yes`; scores 6/7/5/5/5/6; pointer lengths 567/1304/990/646/604/363 bytes, byte-equal).

## Command outputs behind each verdict

- `python3 /fast/scratch/.../check_c2.py` → `entering mismatches=2 landing mismatches=0`; `rounds[1384]: lane=mori type=closure admitted=True round=97 verdicts={'operability': 'improved', 'freshness': 'improved', 'depth': 'unchanged', 'coverage': 'unchanged', 'calibration': 'unchanged', 'adjacency': 'unchanged'}`; EXIT=0.
- `python3 /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-scorecard-calibration.py --selftest` → last line `CALIB_SELFTEST pass=11 fail=0`, EXIT=0.
- `git -C /home/vgpnk/Projects/shokunin/mori-shokunin diff --stat b2a67ce5..600deb7e -- tools/mori-scorecard-calibration.py` → empty output (bytes unchanged since entering).
- Frozen receipts (copied verbatim):
  - `evidence/before-c2.txt`: `C2=unmet mismatches=2 columns_unchanged=yes tool=ok tool_rc=1 mismatched_axes=operability,freshness rev=b2a67ce562bbf2f0cc73f47d8e79f792badf5e63` + `exit=1`.
  - `evidence/landing-c2.txt`: `rev=600deb7ed2695f54b289cf5b6c3931e0fa9c8bb3 count-c2.py sha256=d6fe755fff2e2805c6550ff9bfe0b53c369d5dd8c9799fe4e02bd1e5e73c01fd` / `C2=met mismatches=0 columns_unchanged=yes tool=ok tool_rc=0 mismatched_axes=- rev=600deb7ed2695f54b289cf5b6c3931e0fa9c8bb3` + `exit=0`.

My independent expectation source (fleet MANIFEST) reproduces exactly the gate's mismatched axis pair at entering (operability, freshness) and zero mismatches at landing, with only the two Last-change cells changed.

## Unrun checks

- Did not run `count-c2.py` myself (task was an independent check without the lane tool; receipts + selftest cover the gate side).
- C1 not checked (out of my scope).
- No scratch residue: scratch dir removed before finishing; no cited evidence lived only in scratch (checker logic summarized above; table pasted in full).
