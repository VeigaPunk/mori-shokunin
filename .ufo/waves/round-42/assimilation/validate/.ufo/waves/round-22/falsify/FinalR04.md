# FinalR04 — falsification of R04 (scanner identities = raw minus non-author-glob identities)

Seat `MoriR22.FinalR04`, critic, leaf. Static analysis only. Nothing was executed: no tool, oracle, fixture, mutant, test or build run. The only commands were read-only `git -C` plumbing (`rev-parse`, `status`, `log`, `diff --stat`), `sha256sum`, and `jq` field extraction over already-retained measure1 evidence JSON. No matched text is reproduced; the synthetic token is called "the token". No tools were installed or updated.

## Verdict

- **R04 holds on the delivered source at the branch level.** Fixture and oracle agree on the expected sets, and the gate parity is exact.
- **R04's identity predicate has never been shown to be fail-capable.** No retained run, mutant or refinement case ever evaluated the R04 predicate to `False`. The only population mutant was killed by the exit-code conjunct that R04 shares with R01, before the identity predicate was reached.
- **The same-command red control is missing.** That control is a run with the same `check` argv on the `valid` arm that exits 0 with `RETENTION_RECONCILED` and the correct 5/1/4 counts, but carries wrong scanner identities.

Lesson M1 says scalar count agreement cannot establish population agreement. That criterion is therefore asserted but not evidenced as fail-capable.

## Inputs bound (verified, not inherited)

- Lane HEAD is `5888b565`. `git status` is clean for `tools/mori-retention-reconcile.py` and the round-22 sources. The last tool commit is `3985b3d`.
- Hashes match the pins in `requirements-v2.json`:

  | File | sha256 |
  |---|---|
  | Shipping tool | `d6870fb6…0ce7` |
  | `oracle-reconcile-v2.py` | `dcd1c7c6…adb` |
  | `frozen/fixture-builder-v2.py` | `1b3e16f7…15d1` |
  | `contract.md` | `1658c390…21a1` |
  | `denominator-correction.md` | `968945b2…f9` |

- In measure1 (`measured_revision 4f7cfce`), `summary.tool_sha256`, `after-observed.tool_sha256` and the executing-input binding all equal `d6870fb6…`. The retained evidence was therefore produced by the current shipping source.
- The prior `build/AttackR04.md` cites line numbers that no longer match (`:199-201` is now `:203-205`). Its claims were re-derived below against current source rather than repeated.

## Branch-level reason R04 holds

**Shipping tool (`tools/mori-retention-reconcile.py`)**

- `:203` defines `is_non_author = any(fnmatch.fnmatch(h['path'], pattern) for pattern in patterns)`. The patterns are the policy blob's `non_author_paths_glob`, read from the input revision and byte-equal to the measured revision (`:164-166`).
- `:204` builds `excluded` and `:205` builds `scanner` as complementary identity filters over the same `hits` list. There is no count subtraction.
- `:228` emits `raw_hits=hits`, `scanner_hits=scanner` and `policy_excluded_hits=excluded`.
- The supplied policy path is never excluded by path or content. In the `valid` run, `policy.json` stays in `scanner_hits`.

**Gate parity (`tools/mori-retention-gate.py`)**

- The gate's non-author matcher at `:121-122` is the same `fnmatch.fnmatch`.
- Its partition at `:260-266` is identical: allowlisted is drawn from all hits, including non-author overlap, and unallowlisted is drawn from non-author-excluded hits only.
- Tree listing is identical: `ls-tree -r -z --full-tree` (`:189` versus `:69`).
- Line splitting is identical: `decode(errors='replace').split('\n')` and sha256 of the utf8 line (`:92-101` versus `:146-147`).
- The only divergence is path decoding. The tool uses `strict` and the gate uses `replace`, so a non-UTF-8 path makes the tool exit 2 (fail closed). That cannot cause a false R04 pass.

**Fixture (`frozen/fixture-builder-v2.py`)**

- The measured tree holds `policy.json` (one token hit, on the `synthetic` key line), `allowed.txt` (2 hits), `unallowed.txt` (1), `non-author.txt` (1), `binary.bin` (NUL, skipped) and `allowlist.json` (no token).
- `receipt.json` is only in the second commit, so it is outside the scan.
- The expected sets at `:107-108` come from the builder's own regex scan, and the builder does not import the SUT.
  - Expected excluded set: `{non-author.txt:1}`.
  - Expected scanner set: `{allowed.txt:1, allowed.txt:2, policy.json:k, unallowed.txt:1}`.

**Oracle (`oracle-reconcile-v2.py:40-46, 50`)**

The R04 pass condition is `rc==0`, `finding==RETENTION_RECONCILED`, empty stderr, sorted equality of `scanner_hits` with the expected scanner set, and list equality of `policy_excluded_hits` with the expected excluded set. Retained `after-observed` confirms this:

- The `valid` run exits 0 with empty `differences`.
- `scanner_hits` paths are `[allowed.txt, allowed.txt, policy.json, unallowed.txt]`.
- `policy_excluded_hits` paths are `[non-author.txt]`.
- Results are 24/24 in both `after` and `restored`.

**Comparator soundness.** Full-dict list equality implies multiset equality, so the comparator cannot produce a false pass. Its sort key `(path, line)` is not a total order, and `policy_excluded_hits` is compared in order. Both are latent false-fail risks only. They stay latent while the fixture has one class and one excluded hit.

## Counterexample 1 (primary): the missing same-command red control

**Evidence that the gap is real (retained, via jq):**

- In `mutant-wrong-population-observed.json`, the failed IDs are `R01, R02, R03, R04, R11, R12, R22, R23, R24`.
- Its `valid` run had exit 1 with `RETENTION_RECONCILIATION_MISMATCH` and `differences = [unallowlisted_hits, metric]`, while `raw_total/policy_excluded/scanner_total` stayed 5/1/4.
- In `record()`, the expression `ok = cp.returncode==code and …` is already False, and `ok = ok and predicate(v, f)` short-circuits. **The R04 predicate was never called.**
- R04 "failed" for the same reason as R01. The receipt's `metric` disagreed, which is a receipt-accounting kill and not an identity kill.
- No other mutant (`count-only`, `false-clearance`, `setup-leak`) reaches R04. The refinement cases in `refinement-reconcile.py:16-21, 95-101` contain no `scanner_hits` or `policy_excluded_hits` predicate. Even `non-author-overlap` checks counters only.
- The `--selftest` fixture has `non_author_paths_glob: []` (`:243`), so it never exercises a partition at all.

**Smallest counterexample:** a one-substring output-only mutant of the shipping source (unique substring at `:228`):

- Replace: `'scanner_hits':scanner,'policy_excluded_hits':excluded`
- With: `'scanner_hits':[h for h in hits if h['path']!=paths['policy']],'policy_excluded_hits':[h for h in hits if h['path']==paths['policy']]`

**Static trace on the `valid` arm with the identical `check` argv:**

- Accounting still uses the unmodified `excluded`, `scanner` and `unallowed`, so `differences=[]`. The run exits 0 with `RETENTION_RECONCILED`.
- `raw_total`, `policy_excluded` and `scanner_total` are still 5/1/4, so R01, R02, R03, R12, R22, R23 and R24 pass.
- The emitted identities are the v1 (policy-path) population: scanner `{allowed×2, non-author, unallowed}` and excluded `{policy.json}`. **Only R04 fails**, giving 23/24.
- On real input, `realmatch` in `measure-round22.py:104-105` compares scalars only, so it would still pass.
- The real-input identity digests in `evidence/measure1-identity-check.json` would diverge. That file states it is "not part of measure-round22.py all_claim_checks_pass".

**Consequence.** Today, the synthetic R04 predicate is the sole in-claim identity discriminator. Its false branch has zero observed executions.

**Smallest safe correction (append-only, frozen files untouched).**

1. Add this mutant as `identity-output-swap` to the `mutations` list in `measure-round22.py`.
2. Require it to be killed with `unmet == 1` and `R04` as the sole failing ID. Counts must still be 5/1/4, and its `valid` run must exit 0 with `RETENTION_RECONCILED`. That proves R04's predicate, not the exit conjunct, decided the kill.
3. Optionally, fold the three real-input multiset digests from `frozen/expected-real-identities.json` into `realmatch`. That would make the identity claim in-claim on real input as well.

`measure-round22.py` is not covered by the pins in `requirements-v2.json`, but it is bound per-run through `executing-input-bindings`. Editing it changes the measurement driver, not the frozen oracle.

## Counterexample 2 (adjacent): emitted `raw_hits` is unconstrained by identity

- **Mutant:** at `:228`, change `'raw_hits':hits` to `'raw_hits':scanner+scanner[:1]`.
- **Effect on the `valid` arm:**
  - Five entries, none of them `binary.bin`.
  - `raw_total` is still `len(hits)` = 5.
  - Accounting is unchanged.
- **Result:**
  - R22 (`raw_total==5`, no `binary.bin`) passes.
  - R04 passes, because it compares against fixture truth and not against `v['raw_hits']`.
  - All 24 pass, and `realmatch` passes.
- **The violated relation:** emitted scanner and excluded identities must partition the emitted authoritative raw list (`Counter(scanner) + Counter(excluded) == Counter(raw_hits)`, with the two disjoint). Nothing in the claim enforces it.
- **Smallest correction:** in the same measurement-driver addition, assert `Counter(raw_hits) == Counter(expected all hits)` and the partition sum/disjointness on the `valid` arm. Alternatively, cover it with the in-claim real-input digest above.
- **Impact:** preservation of the raw authoritative list (correction ¶ "Preserve raw authoritative lists"). This does not change the current R04 verdict.

## Re-verified, not counterexamples to current R04

- **Literal glob.** The fixture glob `['non-author.txt']` contains no metacharacters, so the fixture cannot tell `fnmatch` from literal membership or `PurePath.match`. Against the current source this is not a false pass, because the tool and the gate use the same `fnmatch.fnmatch` over the same `-z` path strings. It is a regression-detection gap: an engine swap would only be caught on real input, and only if the engine produced different matches there.
- **Exclusion is by policy, not of the policy source.** `policy.json` remains in scanner in the retained `valid` run, as the correction requires.
- **`raw_unallowlisted == scanner_unallowlisted == len(unallowed)` (`:222`).** The two fields are the same scanner-side set by construction. That is consistent with the real expected 4/4, and outside R04.

## Impacted axes

- **Calibration** is the claim axis. M1's fail-capable criterion is unevidenced: R04's false branch was never exercised, and the identity claim is outside `all_claim_checks_pass` on real input.
- **Depth.** The identity relation to the emitted raw list is unenforced.
- **No impact on privacy.** `privacy_clearance` is hard-coded False (`:225`, `:273`). R04 satisfaction is accounting agreement only. The open debts are unchanged: RED11/12, two unknown dispositions, and a blocked baseline.

## Not done (per bounds)

- No executions of the tool, oracle, fixture builder or mutants. Both mutant traces above are static.
- No production or frozen-file edits.
- No delegation.
- No session, journal or config reads.
