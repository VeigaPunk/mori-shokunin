# Mo85E03C3Fixture — round 85 w1 seat report (C3 load-bearing controls)

Seat: prove that the round-85 C3 counter's own census observation is load-bearing,
using only fixture git repos under the seat scratch dir. Authority:
`.ufo/waves/round-85/contract.md` P-C3 and `.ufo/waves/round-85/count-c3.py`.

## 0. Result

Both assigned controls landed and both falsify their frozen clause; neither read
`met`. An extra single-difference anchor makes the second falsification airtight.

| control | fixture | output | rc | clause falsified |
|---|---|---|---|---|
| 1 census-stub | `786aab607daf` | `C3=unmet observed=3 aa=unstable own_tokens=0 rcs=1,1,1` | 1 | own observation: three stable non-empty `MORI_DRIFT:` lines |
| 2a subject-live-stale (spec-letter fleet-root variant, disclosed) | `409de5e807b0` | `C3=unmet observed=3 aa=stable subject=unmet rc=1` + subject tail `C2=unmet ... live_tokens=51` | 1 | none — MASKED (see §3) |
| 2b subject-live-stale (real fleet root, control of record) | `409de5e807b0` | `C3=unmet observed=3 aa=stable own_tokens=64 subject_tokens=63 subject_deltas=0 unmatched=0 unnamed=0 detector=green` | 1 | `own_tokens` equals the subject's `live_tokens` |
| 3 anchor (pristine subject) | `f2efbfcbffd0` | `C3=met observed=3 aa=stable own_tokens=64 subject_tokens=64 subject_deltas=0 unmatched=0 unnamed=0 detector=green` | 0 | — (single-difference proof for 2b) |

Full commands, byte hashes and verbatim outputs:
`.ufo/waves/round-85/evidence/c3-controls.txt`.

## 1. Fixture construction

All fixture bytes were `git show`-extracted byte-exact from the entering revision
`2cc4b1ae35a83e4fd3fc48bae842bdf38df2e80e`; hashes are in the evidence receipt.
Each fixture: `mktemp -d` under `/fast/scratch/hyaku/mori-r85/Mo85E03C3Fixture/`,
`git init -q`, asserted `rev-parse --show-toplevel` equals the fixture dir,
committed with `-c user.name=t -c user.email=t@t -c commit.gpgsign=false`.

- **census-stub** (`786aab607daf`): the five counter-read paths with
  `tools/mori-census.sh` replaced by exactly `#!/bin/sh` + `exit 1` (no
  `MORI_DRIFT:` line); subject pristine.
- **subject-live-stale** (`409de5e807b0`): real census bytes at the entering
  revision (no stub), subject edited at exactly one anchor (occurrence count
  asserted = 1): the tail argument `len(live_tokens)` → `len(live_tokens) - 1`,
  so the subject prints `live_tokens=63` while everything it derives and grades
  internally is unchanged. Plus `SCORECARD.md` byte-exact (note N1 below).
- **anchor** (`f2efbfcbffd0`): identical to subject-live-stale except the
  pristine subject bytes.

Counter selftest precondition: `C3_COUNTER_SELFTEST pass=20 fail=0`, rc 0.

## 2. Commands (shape; full literal lines in the evidence receipt)

```
HYAKU_SCRATCH=<seat scratch> python3 -I <lane>/.ufo/waves/round-85/count-c3.py \
    HEAD --repo <fixture dir> --fleet-root <fixture dir | /home/vgpnk/Projects/shokunin>
```

## 3. Disclosures

- **N1 — sixth fixture path.** Fixtures 2/3 carry `SCORECARD.md` (byte-exact,
  entering revision) in addition to the five counter-read paths: the r83 subject
  loads it (`CARDS`) and exits `C2_SETUP census/baseline/SCORECARD absent` rc 2
  without it, so a five-path fixture cannot exercise the subject path of the
  counter at all.
- **N2 — fleet root of record for control 2b.** The seat spec's fixture-1
  command template passes `--fleet-root "$D"`; with the fixture dir as fleet
  root the subject's own live census sees a different token set (52 tokens:
  19 snapshot tokens absent, 7 added) than the r82 snapshot, its C2 verdict is
  unmet (rc 1), and the counter short-circuits at `subject=unmet` — control 2a
  records this honestly. The clause control of record (2b) therefore points
  `--fleet-root` at the real fleet root `/home/vgpnk/Projects/shokunin`, the
  same read-only arrangement as the frozen retroactive control in
  `evidence/controls-r85.txt` (census `--drift` writes nothing; all writes stay
  under the seat scratch). 2b changes exactly one thing versus anchor 3: the
  decremented `live_tokens` print — that is what makes the attribution clean.
- **N3 — counter bytes moved during the round.** Between the freeze commit
  `ab260865` and the measurement, pre-data amendments A1–A4 landed (HEAD
  `91f657f6`); the counter gained the A3 subject-verdict gate
  (`fields.get("verdict") != "met"` → `subject=unmet`). The measured bytes are
  HEAD's clean worktree bytes
  `43ad71d8104df29f1be8e3e0cef20d485e35a5f3f70d4994d70adc67b88a2724` (freeze
  blob `c035e32f...47b44`). The 2b subject passes the A3 gate (its own verdict
  is still `C2=met`; only the printed number changed), so 2b isolates the
  `own_tokens == subject_tokens` term of the `met` conjunction.
- **N4 — host-state dependence.** Controls 2b/3 observe the live fleet; their
  64-token reading is today's measurement and matches the frozen retroactive
  control (`own_tokens=64 subject_tokens=64`). A host-state change mid-run could
  in principle destabilize the observation; it did not in this run (aa=stable,
  unmatched=0, unnamed=0).
- **Negative result:** none of the controls read `met`; the one masked variant
  (2a) is disclosed above rather than presented as a clause falsification.

## 4. Scope compliance

- Writes: `.ufo/waves/round-85/evidence/c3-controls.txt` and this report only.
- Lane operations read-only (`git show`/`log`/`diff`/`status`/`rev-parse`); no
  lane commit/push/mutation; fixture commits only, inside the seat scratch.
- Scratch `/fast/scratch/hyaku/mori-r85/Mo85E03C3Fixture/` deleted on exit
  (verified absent). Nothing written under /tmp, fleet root, `.ufo/state/`,
  watchdog log, MANIFEST or any PATH directory.
- No tools installed (python3/git/bash already present); pacman untouched.
- No subagents dispatched; no `agent://all` traffic.

## 5. Suggested checks for the L1

- `python3 -I .ufo/waves/round-85/count-c3.py --selftest` → `pass=20 fail=0`.
- Re-run control 2b against any fixture rebuilt per §1 (hashes in the evidence
  receipt) and confirm the `subject_tokens=63` shape at rc 1.
