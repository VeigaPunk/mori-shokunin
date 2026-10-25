# CritC1Verdict — round 47 wave w2

**Target:** C1 / P-C1, calibration. **Verdict: unprovable as an admissible calibration claim** (the literal frozen-v1 run at T is met; that output alone is not sufficient evidence of honest pin binding). The landed SKILL change itself does **not** show use of a false-green path.

## Counterexample and landed-change assessment

The key positive finding is the exact E→T `SKILL.md` diff: `git diff 2d85e33d14198d388fd3cda9cc15ec07e57e7a53 68d66ca53d89be5c34a62f46af7c37449d9f9b63 -- SKILL.md` changes the r38 self-test tally from `pass=15 fail=0` to `pass=22 fail=0`, and adds registry rows. The entry command remains `python3 tools/mori-sources-appendonly.py <rev> --round-base REV`; the self-test command remains `python3 tools/mori-sources-appendonly.py --selftest`. No edit in this diff rebinds the command, injects an echo, weakens the pin, or hides/duplicates the row. `git diff --quiet af2250d8 68d66ca53d89be5c34a62f46af7c37449d9f9b63 -- SKILL.md` returned rc 0: the measured registry content did not change between receipt revision and T. Thus there is no observed false-green path used by the landing.

Nevertheless, the **frozen instrument** has a demonstrated false-green path. The committed receipt `evidence/v1-junk/skill-v2-oldcopy.txt` runs the frozen v1 checker against the freeze and a junk SKILL variant retaining stale `pass=15 fail=0`, but rebinding its command to `.scratch/MutGateFirstParent/gate-v3-pristine.py`. It reports that stale pin as `match`, then `PIN_CHECK=met tally_pins=26 ... mismatches=0 ... dropped=0`, rc 0. The same class (plus inline echo, entry rebind, hidden-row duplicate, and weakened pin) is recorded in `w1/CritC1Predicate.md` and `corpus/lessons/round-47.md` M2. This falsifies the inference that a green v1 score, by itself, proves all pin claims reproduce from the intended current instrument.

## Evidence (commands / outputs)

- `git diff --numstat E T -- SKILL.md` → `28 1 SKILL.md`; E→T diff inspection shows the sole replaced tally is `pass=15 fail=0` → `pass=22 fail=0`, with unchanged intended command. (Read-only git.)
- `git show T:tools/mori-pin-check.py | sha256sum` → `9832e38c3863ba82f7a740921e8c9d23d6cf2e702c2bb62ee2ad71fcc21bc2b6`; frozen `git show F:tools/mori-pin-check.py | sha256sum` → `e3ef425abde30974faf53a894f96650af11570d2125a5bf621395f6ab0d903e1`. This confirms T uses v2 bytes while P-C1 explicitly requires frozen v1 bytes.
- Reproduced at T with a scratch copy of F's checker: `TMPDIR=<lane>/.scratch/r47w2-CritC1Verdict python3 <scratch>/mori-pin-check-v1.py --repo <lane> --rev 68d66ca53d89be5c34a62f46af7c37449d9f9b63 --min-tally-pins 26 --baseline-rev 2d85e33d14198d388fd3cda9cc15ec07e57e7a53` → `PIN_CHECK=met tally_pins=28 digest_pins=5 mismatches=0 unparsed=0 no_command=0 dropped=0 min_tally_pins=26 rev=68d66ca53d89be5c34a62f46af7c37449d9f9b63 baseline=yes`; process completed successfully (rc 0).
- `evidence/v1-junk/skill-v2-oldcopy.txt` → false-green result `PIN_CHECK=met tally_pins=26 digest_pins=5 mismatches=0 ... dropped=0`, `rc=0`, while its target pin is still `pass=15 fail=0` and observed output is from the historical copy.
- `evidence/after-c1-v1-frozen.txt` and `after-c1-v2.txt` are receipts for `af2250d8`, not T. The direct frozen-v1 rerun above closes that specific receipt revision gap for the reported score. The recorded receipt output at T is therefore not treated as the basis for this verdict.
- Round-46 precedent: `corpus/lessons/round-46.md` says the frozen counter's false-green means admission is **unprovable**; `round-46-verifier-spotcheck.md` §2 separately distinguishes direct pin remeasurement (values happen to match) from admitting the predicate as proof. This round likewise distinguishes actual honest correction from predicate soundness.

## Verdict rationale, axes, correction

**Calibration:** unprovable, not verified. The exact landing diff and actual T result support that this particular tally was genuinely corrected and P-C1's command printed `met`. They do not overcome the frozen counter's established ability to accept arbitrary command rebinding, false output, hidden/duplicated rows, or weakened pin text while still green. The v2 tool and its seven junk receipts are useful remediation evidence but cannot retroactively replace the frozen P-C1 scorer; the v2 bytes at T are not the adjudicator for this contract.

**Impacted axis:** calibration (C1). No finding here scores another axis.

**Smallest safe correction:** report C1 as unprovable under frozen P-C1, while preserving the narrower factual statement that the landed SKILL row was honestly changed and frozen v1 prints met at T. A future contract must freeze and score a checker whose adversarial selftest makes these rebinding/echo/duplicate/weakening controls red before using green to admit the claim. Do not relabel the present result verified merely because v2 is hardened or because this observed diff is clean.
