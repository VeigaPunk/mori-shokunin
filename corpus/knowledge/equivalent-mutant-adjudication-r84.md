source: S599 — https://arxiv.org/abs/2408.01760v1, Large Language Models for Equivalent Mutant Detection: How Far Are We?, abstract; pin `corpus/evidence/sources-r84/arXiv-2408.01760-abs.html:121`, sha256 `688224106999973f3b5c318af871b77923df2c36d0e3e2d799424e2c697cff49`.
verified-at: 2026-11-04
recheck: 365d

# Equivalent-mutant adjudication: an unkillable edit is a cost, not a missing test (round 84)

Axes: operability, calibration, depth. The source grounds the concept only — that equivalent
mutants exist, that they cost and bias mutation testing. The exemption discipline below is the
lane's own rule, not a claim attributed to the paper.

## K1 — What the source states

The abstract's second sentence (pinned body line 121, 14 words) reads: "the presence of equivalent
mutants is known to introduce redundant cost and bias issues". The same sentence is repeated in
page metadata at lines 28, 32 and 39; the anchor is the abstract body, not those copies. The page
is an empirical study of LLM-based equivalent-mutant detection on Java method-level mutants; it
does not define an adjudication procedure, name any tool this lane uses, or state anything about a
gate's exit contract.

## K2 — Why a survivor can be a non-finding

A mutation that no arm can observe is either (a) a missing discriminating arm, or (b) a mutant
whose edit cannot change observable behaviour. Only (a) is a test gap. Treating (b) as (a) inflates
the survivor count and makes a mutation gate unclosable: the gate keeps demanding an arm that no
assertion could ever make fail. The source grounds the cost side of that claim; the distinction is
the lane's decision rule, frozen in `.ufo/waves/round-84/contract.md` P-C1.

## K3 — The exemption is proven, not asserted

An adjudicated equivalent mutant is exempt from the survivor count only while the graded bytes
carry its **coupling marker** exactly once: the marker is the structural reason the dropped clause
cannot be observed. For the two r84 exemptions the markers are `agreed == len(snapshot_tokens)`
(M24c: an unclassified token is absent from `stated`, so it can never be counted agreed) and
`agreed == len(snapshot_tokens)` plus `residual += duplicates` plus `duplicates == 0` (M24d: an
`unexplainable` class never equals `derive(...)`, and duplicate classes are absorbed by
`residual += duplicates` while `met` separately requires `duplicates == 0`). If a marker disappears
or duplicates, the same mutant reads `survived` and the claim is unmet — the exemption cannot
outlive its proof. `tools/mori-record-sweep.py`-style record discipline applies to the exemption
too: the marker is a claim about bytes.

## K4 — The lane's instance

The r83 C1 reviewer measured four extra mutants beyond the frozen 23 at `c4845c83`
(`.ufo/waves/round-83/w1/Mo83R01C1.md` §6): `M24a` (`killed_n = total - survivors` →
`killed_n = total`) and `M24b` (green() dropping the `"fail=0"` token) survived as real blind
spots, while `M24c`/`M24d` (dropping `not unclassified` / `residual == 0` from the r83 drift
counter's `met`) survived as provably equivalent edits. Round 84 carries the two real survivors as
arms and the two equivalent ones as adjudicated exemptions. The adjudication is revision-scoped:
the markers are read from the graded revision's bytes, so a later edit that removes the coupling
re-opens the mutant.

## Limits

The abstract does not discuss this lane, its counters, exit statuses, coupling markers or any
adjudication procedure; it reports a study on Java method-level mutants with an LLM detector. An
exemption is never evidence that a suite is adequate, and an equivalent mutant is never a reason to
skip an arm that *could* observe a different edit. The equivalence proofs above are structural
arguments about the counter's own code, not a general theory of program equivalence (which is
undecidable in general — a limit this entry records rather than proves from the source).

## Boundaries

This is the lane's own gate-quality craft. Detection and report only: no remediation, no OS or unit
state change, no credential material, no foreign test audit, no change to a frozen predicate. The
source registry row, pin and counter implementation have separate owners; their execution is not
established by this prose.
