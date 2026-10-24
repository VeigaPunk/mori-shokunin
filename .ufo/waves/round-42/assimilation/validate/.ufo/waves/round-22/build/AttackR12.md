# AttackR12 — R12 "non-author exclusions retained separately" (round-22, C1)

Seat MoriR22.AttackR12, critic. Static review only. No tests, builds, or SUT runs. No tool installs.
The only commands run were read-only: `git cat-file`/`ls-tree`/`merge-base`, plus in-memory Python
that counted receipt and blob identities (printing only paths, line numbers, classes and counts) and
compared `fnmatch` with `PurePath.match` on synthetic path strings. No matched text was emitted.

Inputs read: `contract.md`, `frozen/requirements.json`, `frozen/fixture-builder.py` and
`oracle-reconcile.py` (both committed at `e825c7f`), `tools/mori-retention-gate.py`, the r18 policy,
the r21 receipt `retention-floor.json`, and `LOG.md:1442-1457`. No SUT candidate exists yet
(`tools/mori-retention-reconcile.py` is absent).

## Verdict

R12 as frozen can pass superficially, and on the real receipt it is the requirement most likely to
be "calibrated" toward a wrong number. Four defects, ranked:

1. **The declared real-receipt denominator mixes up non-author with policy-source** (blocking for the claim narrative).
2. **The R12 oracle checks only a count** (`oracle-reconcile.py:52`). A tool that echoes the receipt's `non_author` field, or uses wrong glob semantics that happen to give the same count, passes.
3. **The fixture's allowlist rows violate the existing allowlist schema**, so a faithful SUT cannot pass R12 (or any exit-0 arm). Only an SUT that drifted from existing semantics can pass.
4. **Unspecified overlaps** (non-author with allowlisted, with the policy path, with must_redact) make "retained separately" ambiguous.

## 1. Counterexample from the real receipt: the declared 5/90 is the non-author partition

What the receipt contains (`retention-floor.json`, measured revision `9fb1f911…`):
- `hits` = 95, `allowlisted_hits` = 86, `unallowlisted_hits` = 4, `non_author` = 5.
- 86 + 4 + 5 = 95, with no non-author hit allowlisted. No duplicate identities.
- The 5 non-author hits are at `corpus/lessons/round-17-verifier-spotcheck.md` (3) and `corpus/lessons/round-18-verifier-spotcheck.md` (2).
- The hits on the supplied policy path `.ufo/waves/round-18/frozen/c1-policy.json` number **4** (lines 8, 11, 12, 14; classes R2, R5, R6, R8), and all 4 are allowlisted.
- I recounted this blob independently at both `9fb1f911` and `77a5bbe8`: 4 hits each, blob SHA-256 `db06e981…`, equal to the receipt's `policy_sha256`.
- The 4 unallowlisted hits are on a *different* path, the copy `.ufo/waves/round-20/falsify/NoHarmRun/rg/.ufo/waves/round-18/frozen/c1-policy.json`.

So 95 − 90 = 5 is the non-author exclusion (90 = `metric_before` = allowlisted + unallowlisted).
It is not a policy-source exclusion. `contract.md:23` ("raw incl5policy … 90(scanner)") and
`LOG.md:1447` ("policy-excluded5 / scanner90") contradict the contract's own definition at
`contract.md:13`, which says to remove exactly the supplied policy path. Peers EnteringPartition and
RawPartition reach the same arithmetic independently.

**Expected result for the real-receipt arm.** These values are derived from the receipt's identities, not measured. Command:

`check --repo <mori> --rev 77a5bbe8a0b41dfbfd2546d024d36e294b814bd0 --receipt .ufo/waves/round-21/evidence/final/retention-floor.json --policy .ufo/waves/round-18/frozen/c1-policy.json --allowlist corpus/evidence/retention-allowlist.json`

The receipt, policy and allowlist are all committed mode-100644 blobs at `77a5bbe8`, and `9fb1f911` is an ancestor. Expected:

- exit 0, `RETENTION_RECONCILED`
- `raw_total` 95, `non_author` 5, `policy_excluded` 4, `scanner_total` 91
- `raw_unallowlisted` 4, `scanner_unallowlisted` 4, `forbidden_allowlist` 0
- `retention_state` red, `privacy_clearance` false

Any of the following on this arm is an R12 failure:
- `policy_excluded` = 5 or `scanner_total` = 90. This means the non-author set was folded into the policy exclusion.
- `policy_excluded` = 8, `scanner_total` = 87, `scanner_unallowlisted` = 0. This means suffix or basename matching also excluded the round-20 copy. It is a false-clean scanner denominator, and the worst outcome.

Impacted axes: calibration (the claim's numbers) and depth.

**Smallest safe correction.** L1 appends a correction to the r22 declaration and lesson: "the 95 vs 90 gap equals non_author = 5; policy_excluded = 4; scanner = 91". The tool must not be tuned to reproduce 5/90. If L1 keeps "95/5/90" as a target, the canonical judge must reject the claim, because no contract-conforming implementation can produce it.

## 2. Counterexample: R12 passes on a count-only or echoing SUT

The oracle's R12 predicate is `non_author==1 and raw_unallowlisted==1 and raw_total==5` on the `valid` variant. Three SUTs that would wrongly pass:

- **Echo SUT.** It copies `non_author` from the receipt. It passes R12, and no frozen mutant alters `non_author`; R10 mutates only `metric`.
- **Wrong-glob SUT.** It uses `PurePath.match`, which is right-anchored and per segment. It passes R12 because the fixture glob is the literal `non-author.txt` at the repo root, where every glob engine agrees.
- **Identity-free SUT.** It never emits or checks which hits are non-author. "Retained separately" goes unverified, and R03 only implies the non-author hit stays in `scanner_total` by arithmetic.

### Concrete fixture R12-X

It extends the builder's `valid` tree: same class `R22`, regex `[R]22_SAMPLE`, one token per line.

Policy: `non_author_paths_glob = ["non-author.txt", "notes/*-na.md", "na-*.txt"]`, `must_redact_paths = []`.

| path | hits | allowlisted | `fnmatch` non-author | `PurePath.match` non-author |
|---|---|---|---|---|
| policy.json (`synthetic` line) | 1 | yes | no | no |
| allowed.txt | 2 (identical lines, one row) | yes | no | no |
| unallowed.txt | 1 | no | no | no |
| non-author.txt | 1 | no | yes | yes |
| notes/deep/x-na.md | 1 | no | **yes** (`*` crosses `/`) | **no** |
| nested/non-author.txt | 1 | no | **no** (anchored) | **yes** (right-anchored) |
| na-allowed.txt | 1 | **yes** (rule `c`) | yes | yes |
| binary.bin (NUL) | skipped | — | — | — |

I checked the four glob outcomes in the last two columns with `fnmatch.fnmatch` and `PurePath.match` on the path strings.

Receipt (existing gate semantics, `tools/mori-retention-gate.py:260-288`):
- `hits` 8, `non_author` 3, `metric` 2, `routed` 0, `warnings` [], `forbidden_allowlist` []
- `finding_id` `RETENTION_FINDINGS`, wrapper `exit_code` 1
- `unallowlisted_hits` = {unallowed.txt:1, nested/non-author.txt:1}
- `allowlisted_hits` = 4: policy.json, allowed.txt ×2, and na-allowed.txt. The gate computes allowlisted over all hits, so a hit can be both allowlisted and non-author.

Expected reconcile result:
- exit 0, `RETENTION_RECONCILED`
- `raw_total` 8, `non_author` 3, `policy_excluded` 1, `scanner_total` 7
- `raw_unallowlisted` 2, `scanner_unallowlisted` 2, `forbidden_allowlist` 0
- `retention_state` red, `privacy_clearance` false
- Non-author identities = exactly {non-author.txt:1, notes/deep/x-na.md:1, na-allowed.txt:1}, as digest-only tuples (path, line, class, line_sha256).

How it discriminates:
- **`PurePath.match` SUT.** Its non-author count is also 3 and its metric is also 2. That is the deliberate count coincidence. Its identities differ, though, so its recomputed `unallowlisted_hits` disagree with the receipt and it exits **1**. It is caught only if the SUT compares lists. Under a count-only oracle it passes, which is the point of the fixture.
- **`PurePath.full_match` or `glob`-style SUT** (`*` does not cross `/`). `non_author` 2 and metric 3, so it fails.
- **Count-subtraction SUT** (`unallowlisted = raw − allowlisted − non_author`). It gets 8 − 4 − 3 = 1 instead of 2, so it fails. This also kills "partition sums to raw" assumptions: 3 + 4 + 2 = 9 ≠ 8.

### Mutant arms on the R12-X receipt

Each changes only the stated fields and rewraps `stdout`. Each must exit 1 with `RETENTION_RECONCILIATION_MISMATCH`.

- **M1 non-author lie:** `non_author` 3 → 2, lists unchanged. Kills the echo SUT.
- **M2 glob relabel:** move notes/deep/x-na.md into `unallowlisted_hits`, `metric` 3, `non_author` 2. This is the receipt a no-cross-`/` gate would emit.
- **M3 identity swap:** in `unallowlisted_hits`, replace nested/non-author.txt with notes/deep/x-na.md, counts unchanged. This is the receipt a `PurePath.match` gate would emit. It kills count-only validators.
- **M4 overlap drop:** remove na-allowed.txt from `allowlisted_hits`. This is the receipt a gate that excluded non-author before the allowlist would emit.

### Exact actionable criterion for R12

R12 passes only if all of the following hold:
- On the `valid` arm, the R12-X arm and the real-receipt arm, the result has exit 0 and `RETENTION_RECONCILED`.
- `non_author` equals the length of a separately emitted non-author identity list.
- That list equals the fnmatch-derived set above, compared as an exact multiset.
- That list is a subset of the raw hits and disjoint from `raw_unallowlisted`.
- Policy-path hits are excluded only via `policy_excluded`.
- M1 through M4 each exit 1 with `RETENTION_RECONCILIATION_MISMATCH`.

Today's oracle checks one count. Treat it as necessary but not sufficient, and record R12 as weak until an amendment adds these checks.

## 3. Fixture blocker: allowlist rows lack `rule`

`fixture-builder.py:55-60` emits allowlist rows with only `{path, class, line_sha256, reason}`. The existing `_validate_allowlist` (`tools/mori-retention-gate.py:142-152`) requires exactly `{path, class, line_sha256, reason, rule}` with `rule ∈ {a, b, c}`, and otherwise raises `invalid_allowlist_row`, which is a setup error. The production allowlist has `rule` on all 86 rows.

The contract requires reproducing the existing allowlist semantics (`contract.md:13`), and says schema inconsistencies fail closed. A faithful SUT therefore returns exit 2 `RETENTION_RECONCILIATION_SETUP` on the `valid` fixture. R12, and every exit-0 arm (R01–R04, R11, R12, R22–R24), cannot pass. An SUT that passes them has relaxed the allowlist schema. That is a superficial pass and an identity change from the gate it claims to mirror.

**Smallest safe correction:** add `row['rule']='b'` (rule `c` for a non-author row) in a new append-only, committed fixture-builder revision before integration. Do not relax the SUT.

This is a fixable defect, not a tradeoff.

## 4. Semantic ambiguities to pin before integration

- **Partition overlap.** The gate's `allowlisted_hits` and `non_author` sets can overlap. The reconciler should emit a disjoint partition that sums to `raw_total`:
  - `non_author`
  - `allowlisted_author` (allowlisted minus non-author)
  - `raw_unallowlisted`
  - an explicit `non_author_allowlisted` overlap count

  On R12-X these are 3 / 3 / 2 / 1. On the real receipt they are 5 / 86 / 4 / 0.
- **Non-author ∩ policy path.** If the supplied policy path matches a non-author glob, report `non_author` on the raw (authoritative) population, so the hit is counted in both `non_author` and `policy_excluded`. Also report the overlap explicitly, for example `policy_excluded_non_author`, and never subtract it twice. The scanner-side `non_author`, if emitted, is a separate field. Not reachable with the r18 policy.
- **Non-author ∩ must_redact.** The existing gate drops such hits from `metric` and `routed` silently (`:262-268`), and `validate_policy` does not reject the overlap. The reconciler must reproduce this, not fix it: same exit and `finding_id`. It should surface a report-only counter, for example `non_author_must_redact`, so the overlap is never invisible. Not reachable with the r18 policy (peer GateAllow checked this with `fnmatch`). This is a tradeoff to disclose, not a reason to reject.
- **Glob engine.** "Existing semantics" means `fnmatch.fnmatch` on the decoded repo-relative path: on POSIX it is case-sensitive, `*` crosses `/`, matching is anchored at both ends, and `[` starts a character class. Any reimplementation must match it. The independence rule bars importing the gate, not `fnmatch`.

## Not claimed

No SUT, oracle or fixture was executed. All values for R12-X and the real-receipt arm are derived by reading the gate code and the receipt, not observed outputs. No privacy clearance is implied: the 4 unallowlisted hits remain red under every reading above.
