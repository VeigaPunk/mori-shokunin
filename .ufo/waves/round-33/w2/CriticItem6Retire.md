# CriticItem6Retire — round 33, wave 2

Scope: the item-6 retirement at `corpus/lessons/round-33.md:114-128`, measured revision
`62db24c01d5b7c2247f43852ea2b28d0ae5e40c8`. Findings only; no closure or C1 verdict.
Axes: **operability, coverage, calibration** (`SCORECARD.md:3,10-14`).

## Ranked findings

### 1. Major — the frozen-run dependency used to retire all detector defects is false

**Attack:** `corpus/lessons/round-33.md:119-122`, especially “changing the tool would move the
digest-pinned round-32 frozen run ... which needs its own claim and re-pin.” The same mistaken
live-tool dependency appears in `SKILL.md:787-790`.

**Counterexample:** change only the live `tools/mori-blind-check.sh`, retaining the historical
bundle. The frozen verifier does not read that live path:

- `.ufo/waves/round-32/frozen/blind-check/verify.sh:24-26` selects
  `TOOL="$FC_DIR/tool/mori-blind-check.sh"`.
- Its digest comparison reads that selected copy (`:101-105`), and its execution uses that copy
  (`:137-139`). Its header explicitly says the lane is “never read for the run” (`:17-19`).
- `expected.json:11-17` distinguishes `path: tool/mori-blind-check.sh` from metadata
  `lane_path: tools/mori-blind-check.sh`; the recorded output is three files-opened findings,
  not these detector edge cases (`:63-70`).

Read-only identity check performed:

```text
timeout 30s prlimit --as=536870912 --cpu=20 -- env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /home/vgpnk/Projects/shokunin/mori-shokunin ls-tree 62db24c01d5b7c2247f43852ea2b28d0ae5e40c8 -- tools/mori-blind-check.sh .ufo/waves/round-32/frozen/blind-check/tool/mori-blind-check.sh .ufo/waves/round-32/frozen/blind-check/expected.json .ufo/waves/round-32/frozen/blind-check/verify.sh
100644 blob 80b8ba7fbe1ef616babda08f78f2d86db5dd7ac4 .ufo/waves/round-32/frozen/blind-check/expected.json
100755 blob 3c26ef69356c289866acf5d3d77e6f437ef73298 .ufo/waves/round-32/frozen/blind-check/tool/mori-blind-check.sh
100755 blob 2738c52629f6192ecdbc4e3bafd8a353616b4781 .ufo/waves/round-32/frozen/blind-check/verify.sh
100755 blob 3c26ef69356c289866acf5d3d77e6f437ef73298 tools/mori-blind-check.sh
```

Both tool paths are regular Git files, not a link to one mutable authority. [INFERENCE] A change
confined to the live path cannot alter the historical verifier's selected bytes or expected values.
A new current-tool baseline is distinct from rewriting/re-pinning the historical baseline.

The blanket rationale also discards the executor's distinction: F2/F3/F4/F6 have a measured scratch
candidate with unchanged selftest hits and `exact=16/16 C2=met`
(`.ufo/waves/round-33/w1/ExecItem6.md:104-121`); F1/F5 instead involve a documented detection-policy
tradeoff (`:123-134`). These are that seat's measurements, not checks rerun by this reviewer.

**Impacted axes:** operability, calibration. This is a fixable factual defect in the retirement
reason, not evidence that every proposed detector change is safe or that retirement is forbidden.

**Smallest safe correction:** preserve the round-32 frozen bundle; correct the live-versus-frozen
claim, including `SKILL.md:789-790`. Give F1–F6 explicit accepted-risk dispositions if retaining
retirement; do not use a nonexistent historical-bundle dependency to retire the four demonstrated
fixable cases. Any new current-tool evidence must remain distinct from historical evidence.

### 2. Major — “correct for its definition” omits the still-active alarm error and overstates absence

**Attack:** `corpus/lessons/round-33.md:123-128`, particularly “correct for its definition (no daemon)”
and the appeal to the round-31 table as sufficient reason to retire the probe defect.

**Strongest existing counterexample:** expected daemon absence under an operating inline driver
still produces a warning and a failed census, not merely a scoped informational observation.
The recorded run has `SURFACE watchdog: drift`, `WATCHDOG_ABSENT severity=warn`, and
`MORI_CENSUS: DRIFT` (`.ufo/waves/round-33/w1/ExecItem6.md:20-22`). This is expected driver shape:
fleet `AGENTS.md:13-19` identifies inline as current mode and prohibits running both drivers.
The cited round-31 entry explicitly says this observation is “not a dead fleet”
(`corpus/knowledge/watchdog-identity-r31.md:38-42`).

The code preserves the disputed consequence:

- `tools/mori-census.sh:829-834`: zero filtered matches emits **warn** and sets watchdog **drift**.
- `:418-429`: warn increments the drift count and sets the overall roll to **DRIFT**.
- `:2714-2719`: that roll produces exit **1**.

Thus documenting what a query means has not removed the expected-mode warning or its global
failure consequence. [INFERENCE] If every other surface were quiet, this warning alone would
still make the census fail; no additional run was performed.

There is a second mismatch with “no daemon”: `cap` saves command status (`tools/mori-census.sh:561-565`),
but `probe_watchdog` never checks that status after calling pgrep (`:710-716`). An unsuccessful
probe with no retained match follows the same absence/warning branch [INFERENCE from that code].
The cited table instead classifies pgrep exit 2/3 as **unavailable** (`watchdog-identity-r31.md:33`);
it also records a real watchdog match dropped by `grep -vF pgrep` (`:22`). Therefore even the
absence inference must stay scoped to the actual query/filter, not daemon identity.

The executor explicitly recommended acting on the inline-mode alarm. Its alternative retirement
included changing severity and surface grading, and disclosed the resulting dead-daemon blind
spot (`ExecItem6.md:138-153`). The lesson implements neither alternative; it retains the old policy.
That is not prohibited merely because the closure permits retirement, but its operational cost
must be the reasoned decision, not hidden behind a true-but-narrow observation.

**Impacted axes:** operability, coverage, calibration.

**Smallest safe correction:** if retiring without code changes, explicitly accept the expected-mode
WARN/DRIFT/exit-1 cost and the missing inline-progress coverage, and scope “absence” to the query.
Do not describe the decision table as having repaired grading. If those costs are not accepted,
this remains an action item; an unconditional demotion would trade away daemon-mode detection
(the executor's own caveat), not supply a no-harm correction.

### 3. Minor — the claimed frontier handoff is inaccurate and the active gate still calls it “Carried”

**Attack:** `corpus/lessons/round-33.md:121-128`: “Recorded as frontier debt” and inline liveness
“named in FR5's boundary.”

**Evidence:** the actual FR5 boundary names unavailable probes and argv-substring identity only;
it does not name inline-driver progress or its missing second liveness source
(`PROVINCE.md:48`; mirrored at `corpus/README.md:339`). Meanwhile the active gate instructions
still direct readers to the round-31 detector defects as **“Carried”** (`SKILL.md:781-782`), not
to the new retirement. The round-31 entry also explicitly says no row changes the probe and FR5
stays frontier (`corpus/knowledge/watchdog-identity-r31.md:60-63`).

**Counterexample:** a reader following the active gate and frontier records receives the old
carry status and no inline-specific frontier boundary, while the new lesson claims a completed
handoff. The defects themselves are not wholly silent: both groups are named in §6 and F1–F6
are linked (`round-33.md:116-128`). The defect is inconsistent disposition/provenance, not total omission.

**Impacted axes:** coverage, calibration.

**Smallest safe correction:** make the active gate point to the explicit accepted-risk disposition;
name the inline alarm/progress residual in FR5 if that is where it is handed off. Keep historical
round-31/32 records intact. Distinguish accepted limits from work merely deferred to a later claim.

## Closure-facing distinction, not a judgment

The closure expressly allows retirement (`corpus/lessons/round-32-verifier-spotcheck.md:197-198`);
the round-33 contract adds “with a reason” (`.ufo/waves/round-33/contract.md:100-101`). Therefore
unchanged tool bytes alone do **not** prove noncompliance, and no fix is mandatory just because
ExecItem6 recommended one. Both retirement labels are explicit (`round-33.md:119,125`).

[INFERENCE] As written, however, this is vulnerable to being called a fourth **documented carry**:
one reason depends on a false frozen-run coupling, the probe reason leaves the warning/failure
policy unacknowledged, and the text promises future work while active pointers still say carried.
A factually corrected, explicit acceptance of those residual costs could constitute retirement;
only the assigned closure/judge can decide that. No C1 outcome is inferred here.

## Checks and limits

- Statically traced the frozen verifier, its expected table, live detector branches/selftest
  expectations, census capture/absence/alarm/exit branches, round-31 table and current-mode
  fleet instruction. Reconciled round-31/32/33 routing and active gate/frontier pointers above.
- Ran only the bounded, memory-limited read-only `git ls-tree` command shown above; it completed.
  No test, selftest, census, counter, judge, mutation experiment, or other runtime was invoked.
- Existing wave-1 reproduction/candidate results are attributed to their committed report;
  neither their PASS results nor their timings are claimed as this seat's measurements.
- No tools installed or updated. No background process started. Wrote only this report; no lane
  source, Git/JJ state, fleet file, host setting, or sibling lane was changed.
