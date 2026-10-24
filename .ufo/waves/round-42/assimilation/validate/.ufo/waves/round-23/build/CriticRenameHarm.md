# CriticRenameHarm — r23 C1 (`raw_unallowlisted` removal, schema v2)

Seat `MadoR22-2.CriticRenameHarm-8`, critic, read-only. Lane HEAD `4dc80c1`.
Inputs read: `contract.md`, `oracle-rename.py`, `frozen/c1-requirements.json`,
`frozen/c1-expected-real.json`, r22 `oracle-reconcile-v2.py`,
`refinement-reconcile.py`, `measure-round22.py`, `frozen/fixture-builder-v2.py`,
`frozen/requirements-v2.json`, `frozen/expected-real.json`,
`evidence/measure3/summary.json`, `tools/mori-retention-reconcile.py`, `SKILL.md`
§retention reconciliation, `corpus/knowledge/retention-reconciliation-r22.md`.
Nothing was executed except read-only `git` plumbing, `sha256sum`, `diff`, and a
JSON read of the retained measure3 summary. No installs.

## Verified (not failures)

- R01–R24 are a pure field substitution. `diff` between r22 `oracle-reconcile-v2.py`
  and `oracle-rename.py` differs only in the docstring, the builder path
  (`HERE.parent/'round-22'/'frozen'/…`, same bytes), the observation schema and
  finding names, R02/R11/R12 `raw_unallowlisted`→`scanner_unallowlisted`, and the
  added R25/R26 and counter. Expected values 1/3/1 are unchanged. R02 now reads
  `scanner_unallowlisted==1` twice; this is harmless because the tool at
  `1bfe708` sets both keys from `len(unallowed)` (tool line 234).
- Pins match: contract `2bb35aef…`, oracle `a55b2b50…`, builder `1b3e16f7…`, r22
  requirements-v2 `48ea2369…`. The tool blob `414463bc…` is identical at `da40bb2`,
  `1bfe708` and `4dc80c1`.
- "Before 25/26 (R25 red)" is consistent with the source. Eight check-output runs
  (valid, forbidden, drop, inject, digest, line, class, metric) carry the old key
  and schema v1. R26 computes 2 and 4 under the current
  `raw_not_allowlisted` code (tool line 235, where `allowed_keys` excludes
  must-redact rows).
- "The r22 oracle is unusable on new revisions" is honest for R02/R11/R12: the
  `KeyError` is caught and the requirement records `pass: False`.
  `da40bb2` is the right bound revision: measure3 shows 24/24, refinement exit 0,
  and the real control matched.

## Concrete failures

### F1 — The declared reproduction mechanism is false (provenance)
The contract says: "r22 claim stays reproducible at `da40bb2` (the r22 driver
stages the tool from `--revision`)". `measure-round22.py` does not stage
anything. It executes the working-tree tool `LANE/'tools/mori-retention-reconcile.py'`
(line 58). It only checks that those bytes equal `git show <revision>:…`
(lines 60–70).
**Counterexample:** once C1 is in the lane working tree,
`measure-round22.py --revision da40bb2…` exits 2 with
`measurement_inputs_uncommitted` and produces no measurement. The claim can only
be reproduced from a checkout of `da40bb2`. Because the driver resolves
`LANE=HERE.parents[2]`, a clone checked out at that revision works.
**Axes:** provenance/honesty of the declared consequence.
**Smallest correction:** replace the parenthetical with "reproducible only from a
checkout of `da40bb2`; the driver runs the working-tree tool and refuses a
committed/loaded mismatch."

### F2 — The declared consequence names the wrong breakage and omits two consumers
- The output whitelist in `measure-round22.py` does not break. `safe_outputs`
  tests `set(value)<=allowed` (line 28), and removing a key preserves the
  subset relation.
- The real breakages at a post-C1 revision are:
  - `after.unmet==3` (R02/R11/R12).
  - `realmatch` turns false, because `frozen/expected-real.json` line 21 expects
    `raw_unallowlisted: 4`, and `type(None) is not int`.
  - The refinement suite exits non-zero. Five cases in `refinement-reconcile.py`
    read the key (lines 186–192): `clean-control`, `non-author-overlap`,
    `forged-clean`, `nested-policy-copy` and `forbidden-only`.
  - Because of that, `restored_red` is non-empty and `mutations_ok` is false.
- The contract names neither `refinement-reconcile.py` nor `frozen/expected-real.json`.

**Axes:** honesty of the declared consequence (calibration).
**Smallest correction:** in the contract, list exactly these four failure points
in place of "output whitelist".

### F3 — Hidden regression: the refinement suite and safety guard are dropped from C1 measurement (depth/no-harm)
The contract says "Before→after for C1 is measured by the r23 oracle only".
The r23 oracle re-expresses the 24 frozen requirements. It does not re-express
the 5 refinement cases, the rest of the r22 refinement suite, or `safe_outputs`.

Evidence from the retained r22 kill matrix (`evidence/measure3/summary.json`):
14 of 22 mutants turn **no** frozen row red. They were killed only by refinement
rows or by `safety:all-arm-output`:

- `setup-leak`
- `line-blind-raw`
- `metric-ignored`
- `non-author-unchecked`
- `no-dotdot`
- `no-ancestor`
- `symlink-accepted`
- `argv-empty`
- `exit-unchecked`
- `finding-unchecked`
- `routed-unchecked`
- `aux-unchecked`
- `forbidden-not-red`
- `repo-unbound`

**Counterexample [INFERENCE: from these red-row sets, plus the R01–R24 predicates
being identical modulo the substitution; not executed]:** take a C1
implementation that also carries, for example, `forbidden-not-red`
(`retention_code=int(bool(unallowed))`) or `argv-empty` (`'argv':[]`). It would
score 26/26 with `misleading_alias_runs` 0:
- R11's forbidden arm stays red through `unallowed==3`.
- R24 only checks `isinstance(argv,list)`.
- R25 and R26 do not touch these paths.

**Axes:** depth/rigor and no-harm for properties admitted in r22.
**Smallest correction:** do two things in a sealed commit before the
implementation lands:
1. Re-express `refinement-reconcile.py` with the same five-case substitution
   `raw_unallowlisted`→`scanner_unallowlisted`. The values 0/1/1/2/0 are the
   same, because both keys come from `len(unallowed)`.
2. Have the r23 driver run that suite, `safe_outputs` with `raw_unallowlisted`
   removed from the allowed set, and the 22-mutant matrix against the post-C1
   tool.

### F4 — The "no other key changes / no alias" invariant is pre-registered but unmeasured
R25 matches only the literal key `raw_unallowlisted`. No requirement and no real
control compares the output key set.

**Counterexamples that score 26/26 and also match `c1-expected-real.json`:**
- A renamed alias such as `raw_unallowlisted_v1` or `legacy_unallowlisted`. This
  violates "clean cutover, no alias".
- Dropping `receipt_authenticity: 'unattested'`. No predicate or expected field
  reads it, so a provenance-honesty marker can vanish unnoticed.
- Dropping `differences`. R05–R10 check only exit and finding.

**Axes:** calibration and provenance.
**Smallest correction:** in R25, also require exact key sets:
- For exit 0/1 runs, `set(obj)` must equal the 24-key set: the `1bfe708` check
  keys minus `raw_unallowlisted`. Those are `schema`, `finding_id`,
  `receipt_match`, `differences`, `raw_total`, `policy_excluded`,
  `exclusion_basis`, `scanner_total`, `scanner_unallowlisted`,
  `raw_not_allowlisted`, `non_author`, `allowlisted`, `forbidden_allowlist`,
  `retention_state`, `privacy_clearance`, `input_revision`, `measured_revision`,
  `receipt_authenticity`, `inputs_sha256`, `tool_sha256`, `argv`, `raw_hits`,
  `scanner_hits` and `policy_excluded_hits`.
- For exit 2 runs, it must equal
  `{schema, finding_id, error, privacy_clearance, receipt_match}`.

### F5 — R25 never exercises the selftest output
The contract requires schema v2 "in every output (check, setup error, selftest)".
The oracle never invokes `--selftest`, so a selftest that still emits v1, or the
old key, goes unobserved. Today the risk is low because all three paths share
`SCHEMA` (lines 231, 274, 287), but the requirement is unmeasured.
**Smallest correction:** add one `--selftest` run to `runs`, so R25 counts it.

### F6 — R26 does not discriminate the "raw" half of `raw_not_allowlisted`
On both builder arms and on the real control,
`raw_not_allowlisted == scanner_unallowlisted + policy_excluded`:
- valid: 2 = 1 + 1
- forbidden: 4 = 3 + 1
- real: 9 = 4 + 5

So a tool computing `len(unallowed)+len(excluded)` passes R26 and
`c1-expected-real.json`. That count ignores allowlist coverage of non-author
hits. R26 does kill the scanner-alias confusion (1≠2, 3≠4) and a tool that
treats forbidden rows as covering (2≠4).

The only discriminating shape is an allowlisted non-author hit. r22 refinement
`non-author-overlap` builds it: the true value is 1, the mutant gives 2. But that
case checks `raw_unallowlisted`, not `raw_not_allowlisted`.

**Axes:** calibration (guard strength). This is not harm caused by C1, since C1
does not touch line 235.
**Smallest correction:** add a R26 conjunct on the `non-author-overlap` shape
with expected `raw_not_allowlisted == 1`, counted independently from committed
bytes.

### F7 — Docs cutover not registered
After C1, these live-guidance texts are false for the tool:
- `SKILL.md:556–558` presents `raw_unallowlisted` as a current output field.
- The `SKILL.md:538` registry row pins r22 `requirements-v2.json` and
  `oracle-reconcile-v2.py` as the tool's frozen values.
- `corpus/knowledge/retention-reconciliation-r22.md:27–36` says "`raw_unallowlisted`
  keeps its frozen alias meaning". This file is the SKILL row's stated Ground.

The contract registers no doc change and no check covers one.
**Axes:** freshness.
**Smallest correction:** in the C1 implementation commit, update the SKILL field
caveats and the pinned values to `frozen/c1-requirements.json` and
`oracle-rename.py`, and add a dated r23 note to the knowledge doc.
`corpus/lessons/round-22.md` stays historical and unchanged.

## Judge-facing split
- F1, F2, F7: fixable wording or cutover gaps.
- F4, F5, F6: fixable oracle weaknesses, if re-sealed before the implementation commit.
- F3: the one that should block admission of "after 26/26" as no-harm evidence.
  Without the re-expressed refinement suite and mutant matrix, 14 of the r22
  mutants are invisible to C1 measurement.
