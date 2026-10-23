# CritClaimSizing — C1 half-controls

## Scope and axes

Attacks **C1 claim sizing/nonredundancy**, on the **calibration** axis: can per-id checking alone, or a challenge arm alone, replace the combined measurement? C2/freshness is not exercised. This is a scoped adversarial review, not an admission judgment.

Scored revision: `e57c58b57c025364e79d130fbdf764d2674d83d6`.

**Result:** neither shortcut suffices. Each half-control prints `C1=unmet` and exits 1, because it accepts a different required negative fixture. No defect found within the assigned attack.

## Construction and bounds

Copied the frozen counter into `/fast/scratch/hyaku/mori-r37/CritClaimSizing/` twice:

- `count-per-id-only.py`: deleted the challenge implementation and its calls from both the positive and negative paths, and removed challenge gating from the final conjunction. Kept summary, per-id, real-history, blind-coverage, and all-three-negative requirements. It cannot fail merely because a removed challenge result was left false.
- `count-challenge-only.py`: deleted per-id parsing/comparison, including every blind, real, and challenge callsite. Kept the challenge and the other original requirements. It cannot reject the summary-only fixture through a leftover per-id check.

Both retain the frozen PREDICATE string and the original negative fixture directory. The tested honest tool is extracted from the scored revision; fixture delegation uses the lane tool whose blob matches that revision (provenance below).

To obey the read-only lane bound, both scratch roots and `TMPDIR` were placed under this seat's scratch. The retained challenge's storage parent was likewise relocated there, **not** under the lane. Its original git identity, title, random history generator, and forced deletion witness remain unchanged. This does not exercise lane-path camouflage. For these specific controls that limitation is non-discriminating: `fixtures/memo-n1.py:29-37` branches only on local git `user.name`, while `fixtures/summary-only.py:16-20` filters `deleted ` lines regardless of path.

No lane source or fixture was changed. The only lane write is this report. No tools installed or updated.

## Provenance measurement

Working directory for every command below: `/home/vgpnk/Projects/shokunin/mori-shokunin`.

Command:

```sh
git hash-object .ufo/waves/round-37/count-c1.py .ufo/waves/round-37/fixtures/memo-n1.py .ufo/waves/round-37/fixtures/const.py .ufo/waves/round-37/fixtures/summary-only.py tools/mori-sources-appendonly.py && git rev-parse e57c58b57c025364e79d130fbdf764d2674d83d6:.ufo/waves/round-37/count-c1.py e57c58b57c025364e79d130fbdf764d2674d83d6:tools/mori-sources-appendonly.py
```

Observed output, exit 0:

```text
7518fef8f54afff69ee38a99f2acbf518006f5ad
19324701f23a225e5ded21c4785c491e7530ac7c
2f3993a04906ce33033ab207a284d9ca7d7ff57a
2d62f742fbef39634a5ff04e25b399b87ce4c941
dfb5040b159f7a0b4afedc90a633d997352908f0
7518fef8f54afff69ee38a99f2acbf518006f5ad
dfb5040b159f7a0b4afedc90a633d997352908f0
```

The first five values also match the pins in `.ufo/waves/round-37/evidence/freeze-r37.txt:4,6-8,10`.

## Control A — per-id check, no challenge

Command:

```sh
env TMPDIR=/fast/scratch/hyaku/mori-r37/CritClaimSizing/tmp PYTHONDONTWRITEBYTECODE=1 python3 /fast/scratch/hyaku/mori-r37/CritClaimSizing/count-per-id-only.py e57c58b57c025364e79d130fbdf764d2674d83d6 --seed 37
```

Observed stdout (predicate and temporary tool-path header omitted), exit **1**:

```text
blind arm: 24/24 sandbox histories matched the hidden truth (2.3s; coverage: deletions=23 changed-back=13 superseded=8)
real arm: pass (0.3s)
  tool:   appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]
  oracle: appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]
  tool exit=1
negative memo-n1.py     ACCEPTED (both remaining arms pass)
negative const.py       rejected (blind 4/4 (repo200: lists differ))
negative summary-only.py rejected (blind 4/4 (repo200: per-id lines differ (malformed=0)))
C1=unmet
seed=37
```

**Counterexample to the shortcut:** `memo-n1.py` performs honest work on the blind repositories but emits the published real summary plus its expected changed-id lines elsewhere (`fixtures/memo-n1.py:16-19,29-37`). Per-id checking does not distinguish that memoized real answer. The missing challenge is the necessary discriminator, as specified by `contract.md:40-42`.

## Control B — challenge, no per-id check

Command:

```sh
env TMPDIR=/fast/scratch/hyaku/mori-r37/CritClaimSizing/tmp PYTHONDONTWRITEBYTECODE=1 python3 /fast/scratch/hyaku/mori-r37/CritClaimSizing/count-challenge-only.py e57c58b57c025364e79d130fbdf764d2674d83d6 --seed 37
```

Observed stdout (predicate and temporary tool-path header omitted), exit **1**:

```text
blind arm: 24/24 sandbox histories matched the hidden truth (2.3s; coverage: deletions=23 changed-back=13 superseded=8)
real arm: pass (0.3s)
  tool:   appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]
  oracle: appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]
  tool exit=1
challenge arm (real-arm clothing): pass (0.1s)
  truth:  appendonly_violations=3 ids=[S072] deleted=[S097,S180] superseded=[S072] round_changed=[S097]
  tool:   appendonly_violations=3 ids=[S072] deleted=[S097,S180] superseded=[S072] round_changed=[S097]
negative memo-n1.py     rejected (challenge: lists differ: want appendonly_violations=6 ids=[S131,S191] deleted=[S069,S169,S238,S260] superseded=[S191] round_changed=[S131,S238] got appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193])
negative const.py       rejected (blind 4/4 (repo200: lists differ))
negative summary-only.py ACCEPTED (all three arms pass)
C1=unmet
seed=37
```

**Counterexample to the shortcut:** `summary-only.py` delegates to the honest gate, preserves the summaries and exit status, and removes only the per-id deletion lines (`fixtures/summary-only.py:16-20`). A new challenge history cannot expose output that the counter never checks.

## Evidence, impact, smallest safe correction

| Half-control | Escaping required negative | Control verdict |
|---|---|---|
| Per-id only | `memo-n1.py` | `C1=unmet`, exit 1 |
| Challenge only | `summary-only.py` | `C1=unmet`, exit 1 |

The positive tool passed every retained arm; failure came from accepting a required negative, not a setup error or honest-tool mismatch. The two proposed shortcuts therefore harm calibration in independent ways. The scored counter's final `all(rejected)` conjunction (`count-c1.py:949`) prevents either half from claiming success.

**Smallest safe correction:** none to the scored proposal for this attack. Do not substitute either half-control. Restoring the deleted half is necessary: the challenge and negative challenge check (`count-c1.py:754-810`) for control A; per-id checks in every arm (`count-c1.py:703-707,733-750,782-785`) for control B. No separate correctness claim is made about other mutations or untested paths.

VERDICT: PASS
