# CritC2Axis — C2 axis choice and sizing

Attacks: C2's attribution as a **measured freshness move**, not the usefulness of its hardening verification. Scored revision: `e57c58b57c025364e79d130fbdf764d2674d83d6`; entering revision: `842a32074b5c7972e9728f3f629d83eb92f127c2`. This is a scoped critic finding, not round admission or a canonical-runtime judgment.

## Axes and what actually changes

The canonical definitions distinguish **operability** (runnable artifacts producing stated outcomes) from **freshness** (skill claims re-verified against live surfaces; stale items flagged or fixed): `../../kimi-shokunin/skills/shokunin/protocol/AXES.md:13-15`.

C2 verifies a drift instrument's **4 MiB bounded-read policy** and **post-redirect public-destination policy**, already landed in round 36. Round 37 adds named selftest assertions, requires each policy's removal to kill its own assertion, and binds the results into a knowledge entry, capability row and coverage-map rows. That is useful, bounded **operability/verification of a freshness instrument**. It does not itself establish that a taught source claim was re-verified or became less stale.

**Freshness is the application surface here, not the measured number.** The measured change is unmet→met for policy-test discrimination and artifact binding. `SCORECARD.md:2045,2066` nevertheless assigns that measurement to freshness. The score is explicitly held at 5 (`SCORECARD.md:2068-2069`): no numeric score inflation or premature saturation is alleged. Holding the number does not supply the missing freshness-axis evidence.

## Strongest local counterexample and evidence

1. **The entering instrument already performs the same fetch/classification work.** Research command, run from the lane root:

   ```text
   git diff 842a32074b5c7972e9728f3f629d83eb92f127c2 e57c58b57c025364e79d130fbdf764d2674d83d6 -- tools/mori-source-drift.py
   ```

   Observed output: `1 file changed, 20 insertions(+), 0 deletions(-)`, with the sole hunk `@@ -394,6 +394,26 @@ def _selftest():`. The additions are the two named policy assertions (`tools/mori-source-drift.py:398-416`), not changes to `fetch`, its policies, or source-claim evaluation. The policies are expressly attributed to `8ff9bba` in `contract.md:54-56` and `corpus/knowledge/source-drift-hardening-r37.md:25-40`.

2. **P-C2 can improve while actual knowledge freshness remains unestablished.** The counter runs fixture selftests and mutations (`.ufo/waves/round-37/count-c2.py:151-180`), checks knowledge-entry tokens and index/capability strings (`:187-206`), then checks only that a committed receipt contains a fixed summary sentence (`:208-211`). It does not require a live recheck of an identified taught claim against its anchor, or a disposition of such a claim.

   [INFERENCE] A source's taught claim could become stale while all those tested artifacts remain unchanged; P-C2 would still return met. That is a counterexample to interpreting P-C2 as a measured freshness improvement, not a claim that the hardening tests fail. No adversarial tree was created or executed.

3. **The proposal itself preserves this distinction.** `SCORECARD.md:2066` calls C2 measured freshness but also states that the live sweep is a demonstration, **not a freshness verdict**. `corpus/knowledge/source-drift-hardening-r37.md:18-23` limits classification to byte behavior. The prior non-author ruling admitted the instrument as an exploratory freshness technique, explicitly not a freshness verdict (`corpus/lessons/round-36-verifier-spotcheck.md:27-32`); that ruling is not a new measured freshness delta in round 37.

### Recorded measurements inspected, not rerun

Commands below are the commands associated with the committed receipts; their outputs were read, not independently re-executed in this review.

- `python3 .ufo/waves/round-37/count-c2.py 842a320` → selftest check FAIL despite tool exit 0; named mutation-arm checks FAIL; knowledge/capability/readme/live FAIL; `C2=unmet`, `EXIT=1` (`.ufo/waves/round-37/evidence/c2-before.txt:2-11`).
- `python3 .ufo/waves/round-37/count-c2.py e57c58b57c025364e79d130fbdf764d2674d83d6` → all checks PASS; `cap_kill` reports `exit=1 huge_cap=FAIL`; `redirect_kill` reports `exit=1 redirect_private_refused=FAIL`; `C2=met`, `EXIT=0` (`.ufo/waves/round-37/evidence/c2-after-tip.txt:2-11`; command/revision specified by this assignment).
- `python3 tools/mori-source-drift.py --root .` → `MORI_SOURCE_DRIFT rows=220 fresh=49 excerpt=0 drifted=9 unavailable=0 no-copy=162`, `EXIT=1` (`.ufo/waves/round-37/evidence/drift-live-r37.txt:221-222`). The same summary is recorded for round 36 with that command (`corpus/knowledge/source-drift-r36.md:26-28`; `.ufo/waves/round-36/evidence/drift-live-r36.txt:221`). An unchanged result can be valid freshness work when an actual taught claim is rechecked; equality alone is not the defect. P-C2 does not require that recheck.

## Impact and smallest safe correction

- **Freshness:** the declared measured improvement is unsupported; freshness should remain unchanged on this evidence.
- **Operability:** the bounded, mutation-backed policy verification and corpus binding are the demonstrated surface.
- **Calibration:** calling this a measured freshness move overstates what the otherwise honestly scoped evidence establishes. C1 is outside this review.

This is a **fixable axis-attribution defect**, not a demonstrated new safety-versus-freshness tradeoff. Preserve the useful tests, corpus binding and receipts; declare their scope as operability verification of the existing drift instrument, keep freshness unchanged and its score held. Any corrected declaration must be explicit/versioned, not a silent rewrite of the frozen contract. Keeping a measured freshness claim instead requires separately frozen, claim-bound live re-verification evidence; renaming policy checks is insufficient.

No lane remediation, runtime judgment, tool installation or upgrade was performed. The only file written is this report.

VERDICT: FAIL
