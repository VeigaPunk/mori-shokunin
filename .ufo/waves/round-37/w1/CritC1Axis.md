# CritC1Axis — C1 axis-choice attack

**Attacks:** classifying round-37 C1's counter-hardening as **calibration** rather than **operability**, at scored tip `e57c58b57c025364e79d130fbdf764d2674d83d6`.

Scope: advisory axis-fit review only; no admission, runtime judgment, remediation, or counter-completeness verdict.

## Axes and definitions

Fleet `../AXES.md:13` defines **operability** as “Runnable artifacts: checklists that are executable, commands that exist, scripts that run”; its signal is “A checklist item can be run and produces the stated outcome”.

Fleet `../AXES.md:15` defines **calibration** as “Self-assessment quality: gaps named honestly, confidence graded, overreach caught”; its signal is “SHONEN.md/SCORECARD entries match observed repo state”.

The lane's Axes table follows both meanings: `SCORECARD.md:11` assigns operability 7 and cites runnable census/selftest and blind-writer-gate evidence; `SCORECARD.md:14` assigns calibration 5 and records that round 12's self-assessed increase “was not re-derived by the outside reviewer and held at 5”. That calibration row now names the round-37 measurement-discrimination defect, without increasing the score.

## Strongest case for operability

The counter is itself an executable artifact. C1 adds a challenge history and output-interface checks, so its command rejects programs it previously accepted. That fits the operability signal's **stated outcome**, not merely script existence. `SCORECARD.md:2058` even registers the “real-arm challenge counter” as something the lane can now do.

There is a strong local precedent: `SCORECARD.md:200-226` selected **operability** for verdict-machine repairs including oracle matching and fixture-signal anti-sniff hardening. Calling every validator improvement calibration would contradict that precedent and ignore that measurement machinery can itself be operational infrastructure. The Axes table's blind-writer-gate example (`SCORECARD.md:11`) reinforces this objection.

## Strongest case for calibration

C1's declared object is specifically **what the lane's measurement establishes**, not a new append-only detection behavior. The frozen claim identifies two false-positive demonstrations of `C2=met` (`.ufo/waves/round-37/contract.md:10-26`); `SCORECARD.md:2044,2049-2052` calls the improvement measurement discrimination and distinguishes it from round 36's gate acquisition.

The operational append-only tool is byte-identical across entering and scored tips (measurement below). The changed surface is the assessment apparatus: a published real-arm answer and an incomplete interface check could previously support an unjustified success assessment. Requiring the named negative programs to fail catches that overreach. This is the canonical calibration definition directly, rather than calibration inferred merely from the author's chosen label.

The operability precedent is not decisive: round 4 also repaired a crashing production census and its close-tracking behavior (`SCORECARD.md:206-226`), while its receipt-backed attack scope and honest limitation were separately called calibration (`SCORECARD.md:230-239`). Nor does the capability row settle the axis: `../AXES.md:59-64` explicitly separates the repertoire table from the six quality axes. Finally, having a runnable counting command cannot alone select operability; every measured claim requires a verifiable measurement (`../AXES.md:27-31`).

## Evidence and commands

Commands below use the lane root as working directory. Only the Git inspection commands were executed for this review; counter results are existing receipts read as data, not independent reruns.

1. Executed:
   ```sh
   git rev-parse 842a32074b5c7972e9728f3f629d83eb92f127c2:tools/mori-sources-appendonly.py e57c58b57c025364e79d130fbdf764d2674d83d6:tools/mori-sources-appendonly.py
   ```
   Observed output, exit 0:
   ```text
   dfb5040b159f7a0b4afedc90a633d997352908f0
   dfb5040b159f7a0b4afedc90a633d997352908f0
   ```
2. Executed:
   ```sh
   git diff --name-status 842a32074b5c7972e9728f3f629d83eb92f127c2 e57c58b57c025364e79d130fbdf764d2674d83d6 -- tools/mori-sources-appendonly.py .ufo/waves/round-37/count-c1.py .ufo/waves/round-37/fixtures corpus/QUALITY.md SCORECARD.md
   ```
   Observed output, exit 0:
   ```text
   A	.ufo/waves/round-37/count-c1.py
   A	.ufo/waves/round-37/fixtures/const.py
   A	.ufo/waves/round-37/fixtures/memo-n1.py
   A	.ufo/waves/round-37/fixtures/summary-only.py
   M	SCORECARD.md
   ```
   This is a scoped path comparison, not an assertion that these are the round's only changed files.
3. Recorded producer commands (`contract.md:36-38`, paths resolved from its fixture directory):
   ```sh
   python3 .ufo/waves/round-36/count-c2.py bf0df77 --tool .ufo/waves/round-37/fixtures/memo-n1.py --seed 11
   python3 .ufo/waves/round-36/count-c2.py bf0df77 --tool .ufo/waves/round-37/fixtures/summary-only.py --seed 12
   ```
   Observed receipt output for each: `C2=met`, `EXIT=0` (`evidence/c1-before-memo.txt:8-10`, `evidence/c1-before-summary.txt:8-10`, under the round-37 wave). These are the false-confidence counterexamples, not failures newly executed here.
4. Recorded producer command:
   ```sh
   python3 .ufo/waves/round-37/count-c1.py e57c58b57c025364e79d130fbdf764d2674d83d6
   ```
   Observed receipt output (`.ufo/waves/round-37/evidence/c1-after.txt:3-16`): `blind arm: 24/24`, `real arm: pass`, `challenge arm (real-arm clothing): pass`; memoizer rejected on the challenge, constant rejected on blind histories, summary-only rejected for per-id lines; `C1=met`, `seed=13985344346805549517`, `EXIT=0`. These support the claimed assessment distinction; they are not a proof against every possible shortcut.

## Ruling and smallest safe correction

**Calibration is the right primary axis.** The strongest operability objection establishes overlap, but not a better classification of this claim: its causal improvement is the lane's ability to avoid overstating what its measurement proves. The existing operational subject did not change.

**Impacted axes:** calibration is primary; the new counter has an operability aspect, but that does not require relabeling C1 or imply a second credited axis move. Other axes and claim validity are outside this review.

**Smallest safe correction:** none to the axis. Retain the narrow measurement-discrimination wording; do not promote it into a claim that the production gate improved or that all memoizers are excluded. No axis defect or axis tradeoff was found for the canonical judge to resolve.

Tool installs/updates: none. No counters, builds, tests, or runtime were invoked; no lane source was edited.

Report: .ufo/waves/round-37/w1/CritC1Axis.md

VERDICT: PASS
