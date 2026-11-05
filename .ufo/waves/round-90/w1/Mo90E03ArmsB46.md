# Mo90E03ArmsB46 — calibration

Entering revision verified by `git -C /home/vgpnk/Projects/shokunin/mori-shokunin rev-parse HEAD`:
`d1c8488986512a6a0475af88cc52779ce4703e00`.

## Delivered

Complete candidate: `.ufo/waves/round-90/w1/candidates/r88-count-c2.py`.
SHA256: `7f7c68e39a0d13d3581ea9a92d68d0a092c9e44b65157e530291467ce955edc6`.
Exactly two new arms; existing arms and production untouched.

- `met_line_call_site`: parses its own source with `ast`; requires a single bare `rev` argument call and forbids subscript arguments on met_line calls. Existing literal helper-test calls remain unchanged. Docstring explicitly says structural pin, not semantic proof.
- `clone_root_negative`: structural FunctionDef-body pin forbidding startswith/endswith/find/index attributes and In/NotIn comparisons. It deliberately does NOT make new behavioural root-negative assertions.

## L1 decisions superseding contradictory seat details

L1 MoriR90-3 directed both structural checks above. A behavioural B6 negative would also fail C2-clone-top (`return True`), violating isolation. Requiring every met_line call to use Name('rev') would reject the existing literal helper tests.
The entering file has 26 arms and NO EXPECTED_ARMS constant; SUBJECT_ARMS=26 grades the r87 gate and must remain unchanged. Two new arms give **28**, not the requested 27. L1 owns the integration merge of `arms_pinned` and `marker_literal` into `frozen_constants`, retaining both assertions, to reach frozen 27. This candidate does not perform that merge or falsify its tally.

## Exercised evidence

Scratch S=`/fast/scratch/hyaku/mori-r90/Mo90E03ArmsB46`.
Command for each row: `python3 -I $S/<file> --selftest --scratch $S/work-<label>` (cwd S, TMPDIR=S). Mutations extracted from the frozen r90 MUTANTS AST; each anchor occurred exactly once in candidate. Copies run concurrently using Python subprocesses; no repository mutations or clones.

| label / file | rc | complete FAIL label set | summary |
|---|---:|---|---|
| pristine / cand.py | 0 | {} | C2_COUNTER_SELFTEST pass=28 fail=0 |
| B4-met-line-call-site / B4-met-line-call-site.py | 1 | {met_line_call_site} | C2_COUNTER_SELFTEST pass=27 fail=1 |
| B6-clone-root-prefix / B6-clone-root-prefix.py | 1 | {clone_root_negative} | C2_COUNTER_SELFTEST pass=27 fail=1 |
| C2-clone-top / C2-clone-top.py | 1 | {clone_top_bound} | C2_COUNTER_SELFTEST pass=27 fail=1 |
| C2-printed-target / C2-printed-target.py | 1 | {met_line_derived} | C2_COUNTER_SELFTEST pass=27 fail=1 |

Exact FAIL lines:
```
FAIL met_line_call_site untruncated revision
FAIL clone_root_negative no prefix operation
FAIL clone_top_bound root
FAIL met_line_derived C2=met real=unmet fx=4 clean=1 refused=2 absent=1 arms=26 rev=abcdef123456
```

## Limits and handoff

No integrated revision counter run; parent must run frozen r90 C2 after its count reconciliation and B1 integration. Structural pins detect these syntactic mutation classes, not semantic correctness or real execution. LSP tools unavailable in this seat's exposed inventory; used AST/source inspection. No installs, upgrades, commits, external changes or subagents. Initial exploration used several shell listing/search calls despite available specialized tools (process defect; no production writes).

Self-evaluation: accuracy 4 (structural evidence only), completeness 4 (count reconciliation explicitly owned by L1), clarity 5 (full FAIL sets retained), actionability 4 (integration gate remains parent-owned), conciseness 4 (process caveats retained). Overall 4.2. Improvement: integrated frozen-counter measurement after parent merge. The assessment matches the scoped evidence, not a C2=met claim.

Scratch removed before return; only candidate and this report retained.
