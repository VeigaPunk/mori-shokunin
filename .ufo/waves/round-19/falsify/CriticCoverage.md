# C1 bounded coverage falsification

## Blocking counterexample (static; not executed)

[INFERENCE] A caller can provide an empty population and empty review rows, then pass the digest of that population as `--expected-sha256`. The check compares the supplied population only with that caller-selected digest, accepts an empty path list, and checks for missing rows only among paths in that supplied list. With no findings, `finish` emits `CLEAN`. The same bypass works for any strict subset with matching rows and a co-selected digest. This does not show that the production invocation used a reduced population; it shows the gate does not itself enforce the contract’s frozen 194-path denominator.

## Evidence and classes

- `.ufo/waves/round-19/contract.md:6` — **scope / no-denominator-cuts requirement**.
- `.ufo/waves/round-19/contract.md:10` — **caller-supplied population-pin interface**.
- `tools/mori-content-review.py:237-240` — **pin trust anchor**: input digest is checked against the supplied argument, not an enforced frozen-population identity.
- `tools/mori-content-review.py:255-270` — **empty-population acceptance**: no non-empty or frozen-membership condition.
- `tools/mori-content-review.py:332-337` — **bounded missing-row accounting**: only supplied paths are checked.
- `tools/mori-content-review.py:176-199` — **clean-on-no-findings outcome**.
- `.ufo/waves/round-19/frozen/content-population.json:4-199` — **frozen 194-path scope**.
- `.ufo/waves/round-19/frozen/expected.json:3-20` — **oracle coverage gap**: pin mismatch is specified, but not a changed subset paired with its matching pin.
- `.ufo/waves/round-19/content-reviews-before.json:3-5` — **partial delivery / fail-closed note**: 26 delivered rows for the 194-path population; absent rows are not a safety assertion.
- `.ufo/waves/round-19/build/ContentGate.md:22-24` — **self-attested review basis**: the gate validates declarations, not whether the content was actually assessed.
- `.ufo/waves/round-19/build/swarm-registry.json:8-12` — **same-wave implementation provenance only**.
- `corpus/lessons/round-19.md:21` — **same-wave provenance is not a content-safety predicate**.
- `.ufo/waves/round-19/build/CriticScope.md:5-20` — **bounded result, not whole-tree proof**; keep the R1–R9 policy and exact allowlist unchanged.

## Impacted axis

**Adjacency (C1).** A clean result can certify a caller-selected subset rather than the required frozen population. Independently, `content-reviewed` remains a reviewer declaration; same-wave origin alone cannot establish that content was reviewed. The gate’s clean status must never be presented as whole-tree privacy clearance.

## Smallest safe correction

Bind the population to an authoritative identity fixed by the pre-implementation freeze (for example, compare the supplied bytes to that frozen artifact at its trusted revision); do not treat a population and digest selected together by the invoking caller as the trust anchor. Keep missing, stale, unresolved, and provenance-only rows non-clean. Treat the result as bounded coverage of the exact frozen population only, and require actual content-based review evidence rather than same-wave provenance before claiming review completion. Preserve the existing R1–R9 all-blob policy and allowlist unchanged.

No command, test, smoke, or verification was run. The 194/26 observation is a count of the retained population and delivered rows, not a gate result.
