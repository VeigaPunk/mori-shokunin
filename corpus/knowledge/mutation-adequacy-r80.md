source: S595 — https://arxiv.org/abs/2102.11378v2, Practical Mutation Testing at Scale, abstract; pin `corpus/evidence/sources-r80/arXiv-2102.11378v2-abs.html:121`, sha256 `28ea1f163860348979a3aa9e9ef8e00fc8eb3ecec2762782d639783003f1b884`.
verified-at: 2026-11-04
recheck: 365d

# Mutation adequacy: a selftest must discriminate (round 80)

Axes: calibration, operability, coverage. The source grounds the test-adequacy concept; the named selftest repair and grading rule below are the lane's application, not claims attributed to the paper.

## K1 — What mutation analysis measures

The abstract describes assessing a suite's adequacy through its ability to detect small artificial faults deliberately seeded into the program. Its visible body is line 121 of the pin; the contiguous 16-word span is `Mutation analysis assesses a test suite&#39;s adequacy by measuring its ability to detect small artificial faults`. The entity `&#39;` is the pinned spelling of the rendered apostrophe. Metadata repeats the sentence at lines 28, 32 and 39; the anchor here is the abstract body, not those copies. The source scout's located-quote receipt is `.ufo/waves/round-80/w1/Mo80Sc02Source.md` §3–4.

## K2 — Consequence for a selftest

An arm that no named mutant can turn red is not execution evidence that the asserted discriminating arm exists. A green summary alone does not establish the distinction the arm claims to test. For the lane's repair, add one discriminating arm per named surviving mutation, demonstrate that it fails on that mutant and passes on the real bytes, and grade the selftest's own verdict. This is the round-80 contract's declared rule, not a new predicate inferred from the abstract: `.ufo/waves/round-80/contract.md` P-C2 and `.ufo/waves/round-80/mutate-c2.py` define the frozen six-mutant experiment. A survivor directs investigation; it does not by itself establish a missing arm.

## K3 — Direction and cost of the inference

A killed mutant demonstrates discrimination of that particular edit in that run; it proves neither broad test completeness nor that every arm contributed. A survivor shows only that no current arm discriminated that edit under the selftest verdict. Human judgement must decide what that observation means. Each mutant costs one selftest run in this harness, so its set is bounded and named: `drop_admitted`, `raise_ceiling`, `count_other_verdicts`, `cut_clause_boundary`, `any_round_in_cell`, and `met_ignores_mismatch`. Neither increasing the count nor killing this entire set licenses a universal adequacy claim.

## K4 — The lane's instance and the zero-arm trap

The entering round-79 counter at `d58889220d3c6a18d461f2d31b5ab162ffef1e4e` has four selftest arms. The historical receipt `.ufo/waves/round-80/evidence/controls-r80.txt` records `python3 -I .ufo/waves/round-80/mutate-c2.py --rev d5888922` producing `MUTATION_C2 survivors=2 killed=4 total=6 rev=d58889220d3c`, rc 1. `drop_admitted` and `cut_clause_boundary` survive with `C2_COUNTER_SELFTEST pass=4 fail=0`. This is receipt evidence, not a harness re-execution by this entry's author. The r79 spotcheck D79-2 named three survivors from its earlier mutation seat; the frozen r80 six-mutant harness, not that descriptive tally, grades this round.

Zero successful arms must never be interpreted as a pass merely because the summary contains `fail=0`. On 2026-11-04 this seat ran both `tools/mori-disk-rate.py --selftest` and `tools/mori-round41-calibration.py --selftest` with `TMPDIR=/nonexistent-mo80-tmp`. Each printed a `SELFTEST SETUP [Errno 2] No such file or directory` diagnostic followed respectively by `MORI_DISK_RATE_SELFTEST pass=0 fail=0` and `MORI_R41_CALIBRATION_SELFTEST pass=0 fail=0`; both exited **2**, not 0. A superficially green zero-failure summary is a setup failure here, not a green process verdict or a passing selftest. Commands and observed outputs are recorded in `.ufo/waves/round-80/w1/Mo80S02Entry.md`; no instrument change is implied.

## Limits

The abstract does not discuss equivalent mutants, name any Python tool, or support a completeness claim. The lane's selftest-verdict criterion, six names and one-run-per-mutant cost are local experiment choices, not assertions from the abstract. A surviving mutant is a lead for human judgement, never proof that a test is missing. The historical receipt establishes the entering measurement only; this entry does not claim that the repair landed, that any new arm passed, or that the final harness killed all six.

## Boundaries

This is the lane's own gate-quality craft, not a claim about another lane's tests. Detection and report only: no remediation, OS or unit state changes, credentials, foreign test audit, or instrument predicate change. The source registry, pin and counter implementation have separate owners; their execution and integration are not established by this prose.
