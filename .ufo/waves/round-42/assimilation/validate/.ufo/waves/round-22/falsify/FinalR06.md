# FinalR06 — falsifying R06 "injected receipt hit returns1"

Seat MoriR22.FinalR06 (critic). Static review of the current shipping source. I executed nothing. No SUT, oracle, fixture, test or build was run. My only actions were reading files, running `sha256sum`, read-only `git log`/`status`, and running Python to read JSON fields out of the retained L1 evidence under `evidence/measure1` (I printed metadata fields only, no line text). I read the correction document first. Installs: none.

## Verdict
- **The shipping tool satisfies R06 (holds).** On the frozen `inject` fixture the result is exit 1, `RETENTION_RECONCILIATION_MISMATCH`, `differences == ['hits']`. Exactly one comparison triggers it: the multiset comparison of the `hits` field.
- **R06 has never been shown to fail.** No retained run demonstrates that R06 can go red. Every mutant L1 measured leaves R06 green. The one mutant that only R06 can kill is not in the mutation set.
- **The oracle does not check the reason.** The frozen oracle checks only exit code, `finding_id` and empty stderr. It does not check `differences`, `receipt_match` or the denominators.

## Inputs (hashes match the requirements-v2 pins)
| Artifact | sha256 |
|---|---|
| `tools/mori-retention-reconcile.py` | d6870fb6…0ce7, which equals the `tool_sha256` in measure1 |
| `oracle-reconcile-v2.py` | dcd1c7c6…8adb, which equals the pin |
| `frozen/fixture-builder-v2.py` | 1b3e16f7…15d1, which equals the pin |

The last commits touching these files are 3985b3d, 8cb4afb and e2f549b.

## Trace of the `inject` variant through the shipping tool
1. **Fixture (builder lines 79 and 93).** The builder appends one hit, `{path:'injected.txt', line:1, class:'R22', line_sha256:'0'*64}`, to `result['hits']`, then re-serializes stdout. Nothing else changes: the partitions, `metric`, `non_author`, `finding_id` and `exit_code` stay at their valid values. `result['hits']` is the same list object as `hits`, so the injected hit appears only in `hits`. `allowed` and `unallowed` were built before the append and do not contain it.
2. **Setup checks pass (SUT lines 155–194).**
   - The revisions resolve, and `measured` is the parent of `rev`, so `merge-base --is-ancestor` returns 0.
   - The policy and allowlist bytes are identical at both revisions.
   - The policy schema is valid; the extra `synthetic` key is ignored.
   - The allowlist rows have exactly the 5 required keys with `rule='b'`.
   - `exit_code` is the integer 1 and `stderr` is empty.
   - In argv, `--repo` is absolute (the measurement driver passes an absolute scratch path). The absolute `--policy` and `--allowlist` paths strip back to the repo-relative inputs, and `--rev` equals `measured`.
   - `commit` and `policy_sha256` bind correctly, and the counters are ints.
   - `normalize_hits` accepts the injected hit: the path is a non-empty string, the line is an int > 0, the class is a non-empty string, the digest is 64 hex characters, and it is not a duplicate. It does no path-existence or known-class check, so the case reaches comparison instead of exiting 2.
3. **Recomputation (lines 195–210).** The rescan finds 5 hits: one in the policy file, two in `allowed.txt`, one in `unallowed.txt`, and one in `non-author.txt`. The NUL-containing blob is skipped. Of these, 3 are allowlisted, 1 is excluded as non-author, the scanner population is 4, 1 is unallowlisted, `routed` is 0, and `retention_code` is 1 (`RETENTION_FINDINGS`).
4. **Comparison (lines 212–218).**
   - `hits`: the receipt claims 6 identities against 5 recomputed, so `'hits'` is added to the differences.
   - `allowlisted_hits`, `unallowlisted_hits`, `metric`, `routed`, `non_author`, `finding_id`, `forbidden_allowlist`, `warnings` and `exit_code` all agree.
   - Result: exit 1 with MISMATCH.
5. **Retained observation.** `measure1/after-observed.json` records the inject run as exit 1, stderr empty, `differences:['hits']`, `receipt_match:false`, raw/excluded/scanner = 5/1/4, `privacy_clearance:false`. This matches the trace.

## Counterexample: one-sided comparison (the missing red control)
Change SUT line 213 by one expression:

```python
if bool(Counter(hit_key(h) for h in actual)-claimed[field]): differences.append(field)
```

This mutant flags only identities that are missing from the receipt and ignores extra ones.

| Check | Arm | Result against the mutant |
|---|---|---|
| Frozen R05 | `drop` | caught (missing identity) |
| Frozen R07, R08, R09 | in-place alteration | caught (the original identity goes missing) |
| Frozen R10 | `metric` | caught (counter) |
| **Frozen R06** | `inject` | **passes the mutant: there is no missing identity and the partitions are unchanged, so it exits 0. This is the only frozen requirement that goes red.** |
| `--selftest` | its only mismatch arm, `wrong.json`, sets `hits:[]` (a drop) | the mutant still reports `RECONCILE_SELFTEST_PASS` 4/4 |
| `refinement-reconcile.py` | `path-only`, `allowed-list-only`, `unallowed-list-only` and `forged-clean` all create missing identities; `non-author-counter` changes a counter | the mutant passes all of them |

The `measure-round22.py` mutation set contains `count-only`, `false-clearance`, `wrong-population` and `setup-leak`; none of them is one-sided. In the retained evidence, R06 is `pass:True` under every mutant:
- `count-only` turned R07, R08 and R09 red;
- `false-clearance` turned R02, R11 and R23 red;
- `wrong-population` turned 9 requirements red, R06 not among them;
- `setup-leak` turned nothing red.

R06's only red observation is the before-run, whose reason is `capability_absent`. That shows the tool was missing, not that R06's check can fail.

**So nothing has shown R06 can fail.** The aggregate kill criterion in the measurement driver (line 93, `unmet>0`) cannot tell R06 apart from the other requirements.

## Second counterexample (impact on the M1 lesson): count-only on `hits` alone survives frozen24
- **The mutant.** It compares only `hits` by count (`sum(claimed['hits'].values())!=len(actual)`) and keeps identity comparison for both partitions.
- **Why the frozen suite misses it.**
  - R05 and R06 change the count, so a count check catches them.
  - R07, R08 and R09 mutate `result['hits'][0]` in place. That dict is the same object as `allowlisted_hits[0]` (builder line 55: `allowed=[h for h in hits …]`), and the hit is the policy-file hit, which is allowlisted. The alteration therefore also shows up in `allowlisted_hits`, which is still compared by identity.
  - The mutant therefore passes all 24 frozen requirements.
- **Where it is caught.** Only the co-evolved refinement `path-only`, whose hits are parsed from JSON and so not shared with the partitions.
- **Consequence.** The retained `count-only` kill (`kill_basis: frozen24-oracle`) happens only because that mutant counts all three fields. It does not show that the frozen suite checks the identities in raw `hits` itself, which is the population lesson M1 is about.

## Axes affected
- **Fail-capability of R06 (main defect).** It is not witnessed.
- **Calibration.** The mutation-kill evidence overstates how much the frozen requirements discriminate, as shown by the two counterexamples above.
- **Reason attribution.** The oracle does not bind `differences`.
- No effect on privacy clearance (`privacy_clearance` is false on every arm I inspected) or on line-text leakage.

## Smallest safe correction (for L1 to decide; this seat makes no edits)
1. In `measure-round22.py`, add a one-sided mutant: replace `claimed[field]!=Counter(hit_key(h) for h in actual)` with `bool(Counter(hit_key(h) for h in actual)-claimed[field])`. Run it through the same oracle command, and require the observed `R06` row to be `pass:false` and the `restored-control` R06 row to be `pass:true`. That is, judge the kill per requirement, not only by `unmet>0`.
2. The frozen oracle is pinned, so put the reason check in the co-evolved refinements instead. Add an `inject` case that checks `differences==['hits']`, `receipt_match is False` and 5/1/4. Also add a count-preserving swap that drops one real hit and injects one fabricated hit in `hits` only. The swap kills the second counterexample through a hits-only arm.
3. Optionally, add an extra-identity arm to `--selftest`. Today its only mismatch arm is a drop.

## Precondition note (not a defect in the current measurement)
The fixture records `str(root)` as argv `--repo`, and the SUT requires that value to be absolute (line 176). If the oracle were invoked with a relative `--output`, R06 and every other non-setup arm would exit 2 with `receipt_repo_binding`. `measure-round22.py` passes an absolute path, so this does not affect the recorded runs.
