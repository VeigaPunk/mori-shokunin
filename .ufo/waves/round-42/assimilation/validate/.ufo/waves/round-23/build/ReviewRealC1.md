# ReviewRealC1 — independent re-derivation of `frozen/c1-expected-real.json`

Seat: `MadoR22-2.ReviewRealC1-8` (reviewer). Detection and report only; no edits, no delegation,
no tool execution, no VCS mutation.

Task: independently re-derive `.ufo/waves/round-23/frozen/c1-expected-real.json` from committed
r21/r22 evidence (`round-22/frozen/expected-real.json`, `round-22/evidence/measure3/summary.json`,
the r21 receipt) **without running the tool**, and check whether `raw_not_allowlisted 9 = 95 − 86`
is the right complement given the allowlist / forbidden semantics.

## Verdict

**AGREE with the frozen values; one in-scope finding on population binding.**

All 14 pinned values in `frozen/c1-expected-real.json` re-derive exactly from committed bytes, and
`raw_not_allowlisted = 9` is the correct complement under the tool's stated allowlist/forbidden
semantics. The frozen file is a faithful transcription of a committed, measured observation, and its
value is independently reproducible from the r21 receipt identities plus the committed allowlist
without executing anything. The finding below concerns *evidence strength of the real arm*, not the
correctness of any pinned number.

## 1. Method (no tool execution)

Only read-only git plumbing (`cat-file`, `ls-tree`, `merge-base`, `rev-parse`) over the lane repo at
`4dc80c1be48308075e83af17f15fbfe7e95e6cb8`, plus byte-level JSON parsing of committed blobs in a
throwaway `python3 -c` (no repo mutation, no `tools/mori-retention-reconcile.py` invocation, no
oracle, no driver). `.scratch/` was not searched; the fleet tree was not walked.

Inputs read as committed blobs:

| Input | Revision used | SHA-256 | Matches frozen `inputs_sha256` |
|---|---|---|---|
| `.ufo/waves/round-21/evidence/final/retention-floor.json` | `77a5bbe8` | `4001e2d9…c840` | yes |
| `.ufo/waves/round-18/frozen/c1-policy.json` | `77a5bbe8` | `db06e981…3128` | yes |
| `corpus/evidence/retention-allowlist.json` | `77a5bbe8` | `f46c78ec…0c63b` | yes |

The same three blobs are byte-identical at `9fb1f911`, `77a5bbe8`, `1bfe708a`, `4dc80c1b`, so the
control does not depend on how far the branch advanced.

## 2. Re-derivation of the pinned `expected` block

### 2.1 Population from the committed r21 receipt (independent of the tool)

The r21 receipt's inner stdout is the r21 gate's own result. Parsing it directly:

* `hits` = 95 entries; all 95 are unique as 4-tuples `(path,line,class,line_sha256)` **and** unique
  as 3-tuples `(path,class,line_sha256)` — no 3-tuple aliasing, so hit-level coverage and key-level
  coverage coincide in this input.
* `allowlisted_hits` = 86; `unallowlisted_hits` = 4; `forbidden_allowlist` = 0; `warnings` = 0;
  `metric` = 4; `non_author` = 5; `finding_id` = `RETENTION_FINDINGS`; inner `commit` =
  `9fb1f911cfdd6061005c300795f44b1b45523897`.

The committed allowlist has exactly **86 rows**, and the set of row keys
`(path,class,line_sha256)` is **equal** to the set of the receipt's `allowlisted_hits` keys. Every
allowlist row key matches some raw hit (0 stale rows), and no row path is in
`must_redact_paths` (0 forbidden rows). Therefore coverage over raw hits is 86 and the uncovered
set is 95 − 86 = **9**.

The 9 uncovered identities, enumerated from the committed bytes:

| # | path | line | class | scope |
|---|---|---|---|---|
| 1 | `.ufo/waves/round-20/falsify/NoHarmRun/rg/.ufo/waves/round-18/frozen/c1-policy.json` | 8 | R2 | in-scope (scanner) |
| 2 | same | 11 | R5 | in-scope |
| 3 | same | 12 | R6 | in-scope |
| 4 | same | 14 | R8 | in-scope |
| 5 | `corpus/lessons/round-17-verifier-spotcheck.md` | 312 | R9 | non-author glob-excluded |
| 6 | `corpus/lessons/round-17-verifier-spotcheck.md` | 315 | R6 | non-author glob-excluded |
| 7 | `corpus/lessons/round-17-verifier-spotcheck.md` | 341 | R6 | non-author glob-excluded |
| 8 | `corpus/lessons/round-18-verifier-spotcheck.md` | 60 | R5 | non-author glob-excluded |
| 9 | `corpus/lessons/round-18-verifier-spotcheck.md` | 60 | R6 | non-author glob-excluded |

So **9 = 4 in-scope unallowlisted + 5 glob-excluded-and-unallowlisted**, and the 4 in-scope hits are
the 4 unallowlisted retention hits the contract carries as open debt (the nested round-20 NoHarmRun
copy of the r18 policy). The receipt's own `metric`/`unallowlisted_hits` (4) and `non_author` (5)
agree with this decomposition. This is the identity-based derivation the r22 lesson demands, and it
independently reproduces 4 / 9 / 95 / 86 / 5 without subtraction.

### 2.2 Partitions

Applying the committed policy's `non_author_paths_glob` (`corpus/lessons/round-*-verifier-spotcheck.md`,
`corpus/lessons/operator-*.md`) to the 95 committed hits: 5 identities are glob-excluded (the two
verifier-spotcheck lesson files, rows 5–9 above) → `policy_excluded` = 5, `scanner_total` = 90.
Of the 90 in-scope hits, 86 are allowlist-covered and 4 are not → `scanner_unallowlisted` = 4.
`forbidden_allowlist` = 0 (no allowlist row path is in `must_redact_paths`; the three `must_redact_paths`
entries are `.ufo/waves/round-17/build/{OmpRetryConfig,PacmanActorTrace,SessionExitCorrelation}.md`
and **no raw hit lies in them**), `stale`/`warnings` = 0.

`must_redact_paths` = `['.ufo/waves/round-17/build/OmpRetryConfig.md', '.ufo/waves/round-17/build/PacmanActorTrace.md', '.ufo/waves/round-17/build/SessionExitCorrelation.md']`;
`non_author_paths_glob` = `['corpus/lessons/round-*-verifier-spotcheck.md', 'corpus/lessons/operator-*.md']`.

### 2.3 Cross-check against the committed r22 measurement

`.ufo/waves/round-22/evidence/measure3/real-reconciliation.json` (committed at `4dc80c1b`) is a
committed observation of exactly the command the r23 driver will issue (`check --repo <lane> --rev
77a5bbe8… --receipt/--policy/--allowlist`): exit 0, `finding_id` `RETENTION_RECONCILED`,
`differences` `[]`, `receipt_match` true, `retention_state` `red`, `privacy_clearance` false,
`raw_total` 95, `allowlisted` 86, `raw_not_allowlisted` **9**, `scanner_total` 90,
`scanner_unallowlisted` 4, `raw_unallowlisted` 4, `policy_excluded` 5, `non_author` 5,
`forbidden_allowlist` 0, `exclusion_basis` `non_author_paths_glob`,
`input_revision` `77a5bbe8…`, `measured_revision` `9fb1f911…`, `inputs_sha256` identical to the
frozen file's. `measure3/summary.json` records `real_matches_frozen_expected: true` and
`retention_floor.unallowlisted: 4`.

### 2.4 Key-by-key agreement with `frozen/c1-expected-real.json`

| Frozen key | Frozen value | Independent derivation | Agree |
|---|---|---|---|
| `allowlisted` | 86 | 86 allowlist rows, all hit-matching, all non-forbidden | ✓ |
| `exclusion_basis` | `non_author_paths_glob` | policy `non_author_paths_glob` applied | ✓ |
| `finding_id` | `RETENTION_RECONCILED` | r22 committed real run | ✓ |
| `forbidden_allowlist` | 0 | 0 rows under `must_redact_paths` | ✓ |
| `non_author` | 5 | receipt `non_author` = 5; glob match = 5 | ✓ |
| `policy_excluded` | 5 | glob-excluded identities = 5 | ✓ |
| `privacy_clearance` | false | hard-coded false | ✓ |
| `raw_not_allowlisted` | 9 | uncovered identity set = 9 (§2.1) | ✓ |
| `raw_total` | 95 | committed receipt `hits` = 95 | ✓ |
| `receipt_match` | true | r22 committed real run, `differences` `[]` | ✓ |
| `retention_state` | `red` | 4 unallowlisted in-scope identities | ✓ |
| `scanner_total` | 90 | 95 − 5 glob-excluded | ✓ |
| `scanner_unallowlisted` | 4 | in-scope uncovered = 4 | ✓ |
| `schema` | `mori-retention-reconciliation-v2` | contract C1 schema cutover (post-change) | ✓ (target value) |

Also checked: `expected_exit` 0 (r22 committed run exit 0); `input_revision` `77a5bbe8…`;
`measured_revision` `9fb1f911…`; `forbidden_keys` `["raw_unallowlisted"]`.

### 2.5 Relationship to the r22 frozen file

`round-22/frozen/expected-real.json` `expected` block (13 keys) vs the r23 file (14 keys):
**13 values identical, no value changed.** The r23 file drops `raw_unallowlisted` and adds
`raw_not_allowlisted` + `schema` — exactly the pre-registered C1 rename and schema cutover, with no
other drift. The r22 file's `measured_revision` is `9fb1f911…` and `input_revision` `77a5bbe8…`, the
same pair the r23 file carries.

## 3. Is `9 = 95 − 86` the right complement under allowlist/forbidden semantics?

**Yes — and the subtraction is a partition identity, not a coincidence.** In the committed tool
(`tools/mori-retention-reconcile.py` at `4dc80c1b`, blob `0795bac9…`, byte-identical at
`1bfe708a`, `da40bb20`, `4dc80c1b`):

* `allowed_keys` = the set of allowlist row keys `(path,class,line_sha256)` whose path is **not** in
  `must_redact_paths` **and** whose key matches an actual hit (stale rows are demoted to `warnings`);
* `allowed` = hits whose 3-tuple is in `allowed_keys` → `allowlisted` = 86;
* `raw_not_allowlisted` = hits whose 3-tuple is **not** in `allowed_keys` → 9.

`allowed` and the `raw_not_allowlisted` set therefore partition the raw hit multiset exactly, so
`raw_total = allowlisted + raw_not_allowlisted` holds structurally, not numerically. Under the
forbidden semantics the two partition members are the *right* ones: a hit whose only covering row is
forbidden (path inside `must_redact_paths`) is counted as not-allowlisted, because a forbidden row
is not a licence. The frozen R26 wording — "in no allowlist row with a path outside
`must_redact_paths`" — matches the implementation's semantics exactly.

Cross-check of the two definitions against the r23 oracle's independent count: the oracle's helper
uses *all* non-forbidden rows, the tool uses non-forbidden **and** hit-matching rows. These agree
for hit-level membership testing, because a row that matches no hit has a key no hit carries, so
including or excluding it cannot change which hits are covered.

**Numerical caveat the frozen file does not state (low severity).** 9 is not the retention-debt
count. It is 4 in-scope unallowlisted identities plus 5 identities that are *simultaneously*
glob-excluded (`corpus/lessons/round-1[78]-verifier-spotcheck.md`) and unallowlisted. The open debt
carried by the contract is 4, not 9. The frozen file pins `scanner_unallowlisted` 4 next to
`raw_not_allowlisted` 9, so the pair is unambiguous in the file itself; but its `derived_from`
sentence expresses the value only as the subtraction "9 = raw_total 95 − allowlisted 86" and does not
record the 4 + 5 decomposition. The committed r22 lesson
(`.ufo/waves/round-22/denominator-correction.md`) states: "never infer unallowlisted=raw−allowlisted−non-author
without identity-based exclusion." The subtraction phrasing in `derived_from` is therefore a weaker
statement of the derivation than the lesson permits, even though the value it names is correct and
independently identity-derived (§2.1). Recommended, no key or value change: cite the identity
recomputation over the r21 receipt's 95 identities minus the committed allowlist's 86 covering keys,
and record the 4 + 5 split.

## 4. Findings

### F1 — the C1 real arm pins scalars only; it cannot falsify a mis-populated tool (Medium)

`frozen/c1-expected-real.json` pins counter values only: `raw_total` 95, `allowlisted` 86,
`raw_not_allowlisted` 9, `scanner_total` 90, `scanner_unallowlisted` 4. Inside the tool these
quantities are algebraically dependent — `allowlisted + raw_not_allowlisted = raw_total` and
`scanner_total + policy_excluded = raw_total` are partition identities — so the pinned set carries
roughly two independent constraints, not five.

Consequence: a tool that keeps every counter correct while placing the *wrong identities* in each
bucket (e.g. swapping the `raw_hits` / `scanner_hits` / `policy_excluded_hits` lists while keeping
their lengths) satisfies the frozen real control exactly. r22 already solved this for the same tree
and the same receipt: `round-22/frozen/expected-real-identities.json` pins SHA-256 digests of the
three identity lists, and `measure-round22.py:143-151` checks `identity_match` **and**
`identity_twin_rejected` (a same-command run with `scanner_hits` and `policy_excluded_hits`
swapped must *not* match) as part of `realmatch`, and records both in
`measure3/summary.json` (`real_identity.swapped_twin_rejected: true`).

The r23 driver as authored (`.ufo/waves/round-23/build/MeasureDriver/measure-round23.py`) contains
**no** identity or twin check: a search for `identity|identit|twin|swapped|raw_hits` in that file
returns zero hits, and its `C13.c1_real_control_matches_frozen` compares only the `expected` keys
plus `inputs_sha256`, `input_revision`, `measured_revision`, `tool_sha256`, `argv`,
`privacy_clearance is False` and the absence of `raw_unallowlisted`.

The gap is closable without new artifacts: the tree at the measured revision `9fb1f911` is unchanged,
so `round-22/frozen/expected-real-identities.json` (digests `c275d2c2…` / `9690b3a9…` /
`17c348f0…`) is directly reusable as the r23 real-arm population pin, and the swapped-twin
rejection can be carried over from `measure-round22.py:145-148`. Without it, C1's real arm measures
count agreement only — the exact scalar-agreement failure mode the r22 lesson records as M1 — and
that arm is the only place in the wave where the r21 receipt's actual identities are exercised at
all (the r23 oracle's R26 runs on synthetic fixtures).

Severity rationale: the pinned numbers are correct and independently reproducible, so no claim is
false as written; the defect is that the *evidence* the real arm provides is narrower than the
evidence r22 established for the identical population, at the exact point where the wave's own
lesson says count agreement is insufficient.

### F2 — the real arm does not exercise forbidden-row handling at all (Low, residual risk)

In this receipt `forbidden_allowlist` = 0 and **no raw hit lies under `must_redact_paths`**
(verified from the committed policy and the 95 committed hits). Therefore a mutant that mishandles
forbidden rows — e.g. admitting a `must_redact_paths` row into `allowed_keys` — would leave
`raw_not_allowlisted` at 9 and pass the frozen real control unchanged. The forbidden semantics is
exercised only by the synthetic arms (R11 `forbidden_allowlist == 1`, and R26's forbidden arm
expecting `raw_not_allowlisted == 4`). This is a coverage property of the real control, not an
error in it, and it should not be read as evidence that the real receipt validates the forbidden
branch.

### F3 — cross-reference, not a new finding: the C1 declared consequence overstates r22 reproducibility

`.ufo/waves/round-23/contract.md` §C1 "Declared consequence" states the r22 claim "stays
reproducible at its bound revision `da40bb20` (the r22 driver stages the tool from `--revision`)".
In the committed driver, `measure-round22.py:58` sets `tool = LANE/'tools/mori-retention-reconcile.py'`
— the **working-tree** tool — while line 59 fetches the revision's bytes only for the digest
comparison; the binding check at lines 60-66 aborts with `measurement_inputs_uncommitted` (exit 2)
whenever the working-tree bytes differ from `--revision`. So after C1 lands in the working tree the
r22 driver exits 2 rather than re-verifying the r22 claim, and the r22 claim is reproducible only
from a checkout pinned at `da40bb20`. This is already captured by another seat as lesson candidate
M6 (`build/DraftLesson/mistakes.md`), so it is recorded here only for completeness of the C1
provenance chain; it does not affect any value in `frozen/c1-expected-real.json`.

## 5. Verification gaps / what was not checked

* **Not executed.** No tool, oracle, driver or selftest was run (contract §Bounds: no
  tests/builds/linters/formatters/smoke runs this wave; L1 measures after integration). Every number
  above is a byte-level derivation from committed blobs, not an observation of a running program.
* **Field-level equivalence to the r22 driver** was not re-derived from the r22 driver source; the
  r22 values were cross-read from the committed `measure3/real-reconciliation.json` receipt and
  `measure3/summary.json`.
* **`raw_not_allowlisted` under multiplicity** was verified for *this* input only (95 unique
  3-tuples, so no 3-tuple aliasing). For a hypothetical input where two hits share a
  `(path,class,line_sha256)`, `allowlisted` and `raw_not_allowlisted` would still partition the hit
  multiset, but `allowlisted` would count hits rather than distinct keys. This does not affect the
  frozen real control; it is noted so the count is not read as "86 distinct allowlist rows".
* The **C2** frozen file and the C2 real arm were out of scope and were not reviewed.
* `SCHEMA` was not exercised: the pinned `mori-retention-reconciliation-v2` is the contract's
  declared post-change target, not an observed value.

## 6. Conclusion

`frozen/c1-expected-real.json` is a correct and independently reproducible frozen real control.
`raw_not_allowlisted = 9` is the right complement: it is the exact complement of the 86 non-forbidden
allowlist-covered identities within the 95 committed raw identities, and it decomposes as 4
in-scope unallowlisted + 5 glob-excluded-and-unallowlisted (open debt remains 4). The single
in-scope finding is F1: the real arm pins counters without a population binding, so it is weaker
than the r22 real control it supersedes; F2 is a residual coverage limit of the real arm, and F3 is
a cross-reference already owned by another seat.

**Recommendation to L1:** accept the frozen values; optionally (a) add the 4 + 5 decomposition and
an identity-based citation to `derived_from`, and (b) bind the C1 real arm to the existing
`round-22/frozen/expected-real-identities.json` digests plus a swapped-twin rejection, as r22 did.

## 7. Provenance of the cited `rounds[427]` reference

`frozen/c1-expected-real.json`'s `derived_from` attributes the value to "the r22 closure rechecks
(rounds[427])". Verified against the fleet `MANIFEST.json` `rounds[427]`: it is the **mori** round-22
closure (`round` 22, `lane` `mori`, `admitted` true, `verdict` `admitted`), and its
`verification.rechecks` records, verbatim: "check on r21 receipt at 77a5bbe → rc0
RETENTION_RECONCILED raw95/policy_excluded5/scanner90/raw_unallowlisted4/raw_not_allowlisted9/
allowlisted86/forbidden0, red, privacy_clearance=false, measured 9fb1f91; receipt's own committed
stdout: hits95, unallowlisted4, allowlisted86, non_author5, metric4", and its `notes` record "the
true raw complement (95−86=9)". The provenance attribution is accurate. The round-23 contract's
"MANIFEST rounds[427]" pointer is to the same entry.

## 8. Run log

* **Commands:** read-only `git -C <lane> cat-file / ls-tree / merge-base --is-ancestor / rev-parse
  / status --porcelain`; `sha256sum` over committed blob streams; `python3 -c` JSON/CSV-style
  parsing of committed blob bytes in a temporary shell; file reads via the read tool. One `grep -rn`
  over the lane tree was issued and hit the 300 s timeout on `.scratch/`; it was not repeated and no
  `.scratch/` content was read.
* **Tools installed or updated:** none. No package-manager transaction was needed or run.
* **Measurements/tests/builds:** none run. No candidate tool was executed.
* **Files written:** this report only, at `.ufo/waves/round-23/build/ReviewRealC1.md`. No production,
  frozen, oracle, case or driver file was touched; no git/jj mutation was performed in the lane.

Report: .ufo/waves/round-23/build/ReviewRealC1.md
