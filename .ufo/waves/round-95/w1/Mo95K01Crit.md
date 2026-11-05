# Mo95K01Crit — round 95 attempt 1, w1

Review only: calibration, operability, depth, freshness, coverage, adjacency. No admission decision, integration, predicate edit, or score change performed.

## Scope and authorities

Entering revision: `754f4991198c16ddd1d4a3ea9206cfb7d74d6827`. Frozen artifacts: `2dc476d7fdb68bf916685a9f217a92047662baeb`.

The assignment's lane-local `AXES.md` and `LEARNING.md` do not exist; I read their fleet authorities at `/home/vgpnk/Projects/shokunin/AXES.md` and `/home/vgpnk/Projects/shokunin/LEARNING.md`. References below use `../AXES.md`, `../LEARNING.md`, and `../PROTOCOL.md` for those files. Other paths are lane-relative.

## K1 — C1 is coverage growth, not the claimed self-assessment mismatch

**C1: NOT-ADMIT as calibration.**

Strongest counterexample: the purportedly inaccurate self-assessment already explicitly states the exact observed gap. `corpus/lessons/round-94.md:15-17` names m2/m3/m4/m6 as survivors and says the score is not moved; its Mistakes row at :37 names the missing fixtures and routes the amendment. Thus the honest before self-assessment and observed repository state agree: four known survivors.

The round-95 contract :16-20 instead calls `met` the battery's kill claim and interprets survival as a disagreement with self-assessment. That changes the meaning of the earlier result. Round-94's result concerned embedded-token discrimination, not certification that census, trio and patched12 clauses had mutation coverage. The non-author closure explicitly scopes the observed discrimination at `corpus/lessons/round-94-verifier-spotcheck.md:56-68`; the mutation report distinguishes a control-battery gap from a counter defect at `.ufo/waves/round-94/w1/Mo94M01Mut.md:78-82`.

`../AXES.md:15` defines calibration by honest gaps, confidence and caught overreach, with SHONEN/SCORECARD matching state. Its :20-23 and `../LEARNING.md:84-88` map discernment to calibration, not to a test count. `../LEARNING.md:35,42-48` additionally requires outside gate comparison for discernment. `count-c1.py:210-223` counts differing counter outcomes over fixtures, not false self-assessment statements or corrections to them. No inaccurate recorded self-assessment is enumerated by the count.

Smallest safe correction: preserve the frozen evidence and predicates; record the result as strengthening the named mutation battery, without claiming this count establishes a calibration move. A different calibration claim would require a separately declared measurable mismatch and its correction, not retroactive reinterpretation of the already-honest round-94 lesson. Whether a different axis or capability can be credited is for the canonical judge; this review does not reclassify the frozen claim.

## K2 — R94-only do-nothing baseline

Confirmed by the frozen counter's before field: `before_r94_survivors=4 r94_survivor_ids=m2,m3,m4,m6` at entering. This is precisely the assigned way to measure R94-only fixtures; I did not edit the fixture list. The same run also executes R95 fixtures and therefore has an overall exit 0 and after survivors=0; that overall result must not be mislabeled as the old battery passing.

Executed from the seat scratch directory:

```sh
S=${HYAKU_SCRATCH:-/fast/scratch/hyaku}/mori-r95/Mo95K01Crit
L=/home/vgpnk/Projects/shokunin/mori-shokunin
# Previously extracted with:
git -C "$L" show 2dc476d7:.ufo/waves/round-95/count-c1.py > "$S/count-c1.py"
trap 'rm -rf -- "$S"' EXIT
TMPDIR="$S" python3 -I "$S/count-c1.py" 754f4991198c16ddd1d4a3ea9206cfb7d74d6827 --lane /home/vgpnk/Projects/shokunin/mori-shokunin --census /home/vgpnk/Projects/shokunin/scripts/sources-census.sh
rc=$?; printf 'exit=%s\n' "$rc"
```

Observed output, exit 0 (157.65 seconds):

```text
C1=met survivors=0 killed=7/7 before_r94_survivors=4 r94_survivor_ids=m2,m3,m4,m6 after_survivor_ids=- pristine=green equiv=m5(declared) crash_ids=-
KILL m1 by=R94-L,R94-R,R94-M
KILL m1b by=R94-L,R94-R,R94-M
KILL m2 by=R95-LEN
KILL m3 by=R95-CEN
KILL m4 by=R95-TRIO
KILL m6 by=R95-PAT
KILL m7 by=R94-L,R94-R,R94-M
PRISTINE R94-L C1=unmet 1 admission
PRISTINE R94-R C1=unmet 1 admission
PRISTINE R94-M C1=unmet 1 admission
PRISTINE R95-LEN C1=unmet 1 admission
PRISTINE R95-CEN C1=unmet 1 census
PRISTINE R95-TRIO C1=unmet 1 trio
PRISTINE R95-PAT C1=unmet 1 patched12
exit=0
```

Pins observed with `sha256sum` / `git show ... | sha256sum`:

- Frozen r95 C1 script: `6c288d70c39a5736b6aba0b4a0525159010124c0b5494f047a10aab6dfeaa450`.
- Frozen r95 C2 script: `014980bc82b71b7a48764b45e7e550050e928956a32cd6e4ef3b4208aa844b9f`.
- Entering r94 pristine: `6eb7fa4cf0ecf86064bb2714a5b93b52bf3356dc6e38e5dc7ee51f7255a7b384`.
- Entering r93 C1: `98ed3e3ea9a1478957884dc1352fbab6b129913f941bfac7f739f63c8a6152d2`.

## K3 — C2 is honestly a capability demonstration, not a new round-95 operability move

**C2: ADMIT-CANDIDATE only as the explicitly bounded namespace capability demonstration; NOT-ADMIT as a new round-95 change to counter behaviour.**

The existing defective artifact is `.ufo/waves/round-93/count-c1.py`, whose :39 hardcodes CENSUS and whose :150 executes it. It remains unchanged. The working successor is the already-existing `.ufo/waves/round-94/count-c1v2.py` (:126-144 resolves an explicit census and diagnoses absence). The operational contrast is real, but the successor behaviour was not created in round 95.

The new deliverable is a real runnable namespace comparison, `.ufo/waves/round-95/count-c2.sh:35-56`, demonstrating the old and successor counters against a hidden home with an outside positive control. The capability identity must be that harness/demonstration, not retroactive invention of r94 host-independent behaviour. `../AXES.md:57-64,80` requires name, ability, evidence pointer, first-working round, and a passing demonstration in the round report. The evidence pointer may be a path or command (a literal command column is not mandatory), but the capability must actually run. The lane uses that same four-column table at `SCORECARD.md:4777-4781`. Round 95 can be first-working for this namespace harness; it must not be claimed as first-working for the older successor counter.

The prior closure expressly offered the capability route at `corpus/lessons/round-94-verifier-spotcheck.md:124-126`, and held operability unchanged at :80-86. No numeric operability improvement follows merely from running the new probe.

## K4 — C2's before is admissible, not absence

Yes, for the limited comparison requested by K01. `.ufo/waves/round-94/w1/Mo94K01Crit.md:98` explicitly accepts an old host-bound counter failing without the host path and an append-only successor working, or a capability row. The round-93 file is present, not missing: its entering blob was read and hashed above. The frozen before receipt `.ufo/waves/round-95/evidence/before-c2-r95.txt:1,6` records hidden=1, old unmet rc1, successor met rc0, outside old met rc0, exit0. That is not the r94 `files=0` absence baseline.

Fresh reproduction (20.01 seconds):

```sh
S=${HYAKU_SCRATCH:-/fast/scratch/hyaku}/mori-r95/Mo95K01Crit/c2-probe
mkdir -p "$S"
trap 'rm -rf -- "$S"' EXIT
TMPDIR="$S" bash /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-95/count-c2.sh 754f4991198c16ddd1d4a3ea9206cfb7d74d6827 /home/vgpnk/Projects/shokunin/mori-shokunin /home/vgpnk/Projects/shokunin
rc=$?; printf 'exit=%s\n' "$rc"
```

```text
HOSTINDEP hidden=1 before=C1=unmet(rc=1) after=C1=met(rc=0) control_outside=C1=met(rc=0) census_sha=3fb7261569f4 rev=754f4991198c
exit=0
```

This verifies the frozen predicate, not universal host independence or a detailed diagnosis of every old-counter failure mode.

## K5 — would they pass without the work?

- **C1, without adding the R95 fixtures:** no; the R94-only projection leaves four survivors. **But the complete frozen r95 counter already passes at entering**, since it supplies the fixtures itself. Its :163-180 reads only the pinned pristine at the supplied revision and constructs new fixtures; it does not require candidate-revision changes. Distinguish real battery construction in the freeze from any later landing edits.
- **C2, with only r93 as the implementation:** no; old-counter in-namespace result is unmet rc1. **C2, with the actual unchanged entering repository:** yes; the fresh command above already returns exit0 at `754f4991`, as does the frozen before receipt. The successor already exists there. Contract :53 says do-nothing fails `(b)`, but `(b)` explicitly requires old-counter failure, so that failure actually satisfies `(b)`; the same execution also satisfies `(c)`. This sentence confuses an old implementation contrast with a temporal entering→landing contrast.

Smallest safe correction: append a precise correction in the round report explaining these two meanings of before. Leave frozen bytes intact. Credit C2 only as the newly demonstrated namespace comparison; do not use its entering pass as evidence of new counter behaviour or an operability score increase.

## K6 — universal language and enumeration

- C1's “every pristine fixture”, “every one of the seven mutants” and “all seven non-equivalent mutants” are acceptable **only over the explicitly named set**, not all possible mutations. Enumeration exists in `count-c1.py:44-64,197-216,224-227` and the K2 output. No unenumerated universal proof follows.
- The m5 statement “on every input” / “every reachable pair” (`contract.md:32-33`) is a mathematical invariant, not an empirical input sweep: `count-c1v2.py:157-165` increments exactly one of two counters per NINETEEN item on completed evaluations. It does not assert every input terminates successfully. No exhaustive execution command exists, nor is one needed for that scoped algebraic claim.
- “the lane's counting surface” (`contract.md:39`) is broader than the enumerated two counter files (`count-c2.sh:31-32`). There is **no lane-wide enumerating command** in P-C2r95. Scope the report to those two named counters.
- “has no host path” (`contract.md:43`) is broader than the namespace experiment, which hides one home directory; the limit at :57-59 correctly disclaims general host freedom. Do not promote this to “host-independent everywhere”, “every counter”, or “no harm”. The namespace check supplies no all-path scan.
- No universal “complete” or blanket “no harm” claim appears in the two claim predicates. This review did not run a six-axis no-harm battery and does not certify one.

## Impact and smallest safe disposition

Calibration is the primary blocker: a disclosed test gap is not a counted false self-assessment. Coverage/depth can describe stronger testing, but a post-data axis replacement is not this seat's authority. Operability/capability evidence is real but temporally overdescribed; preserve the narrower capability identity and the entering pass. Freshness and adjacency acquire no improvement from these counters; no sibling or host configuration change was made. No depth or all-axis no-harm judgment is inferred.

No tools installed or updated. No tracked input edited, no lane/fleet git mutation, no sibling write. Scratch was removed by the EXIT traps; retained evidence is the exact commands and outputs above, not pointers into deleted scratch. No independent expanded mutation sweep was run or claimed.

Self-evaluation: accuracy 4 (axis classification remains a recommendation to the canonical judge); completeness 4 (required replay and K1–K6 addressed, no wider mutant sweep); clarity 4 (temporal versus implementation before is explicitly separated); actionability 4 (append-only correction and capability identity are named); conciseness 3 (full replay output retained for auditability). Improvement applied: scope C2 to its concrete harness, not general host independence. Overall 3.8; user agreement is not presumed.

SEAT Mo95K01Crit PASS
