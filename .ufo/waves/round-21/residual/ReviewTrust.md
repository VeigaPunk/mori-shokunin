# ReviewTrust — round21 residual integration review (trust refinement)

Seat: MoriR21.ReviewTrust (critic). Scope: whether a submitted disposed declaration can ever
authenticate itself, whether the real after rows stay as two unresolved, and whether
"mandatory baseline acceptance" is kept separate from intercepting the raw `--pin` command.
Review only: no edits, no tests, no census and no pin. No tools installed.

## Verdict summary

| Attack | Result |
|---|---|
| A1: does a disposed declaration produce `pin_allowed`/rc0 automatically? | **Holds (counterexample failed).** rc0 cannot be reached. |
| A2: are the real after rows two unresolved with null dispositions? | **Holds for the data**; **not measured** by the independent oracle (defect T1). |
| A3: do the independent harnesses exercise the external-review-required path? | **No** (defect T2). Only the author's selftest exercises it. |
| A4: acceptance gate versus `--pin` interception | Prose is mostly honest; the registry `kind` labels are inverted (defect T3). |
| A5: provenance wording | One overclaiming phrase (T4) and one ambiguous freeze citation (T5). |

## A1 — automatic authentication: the counterexample failed

Strongest available counterexample: a self-authored disposed row that passes every structural
check. The fields are `independent:true`, an actor distinct from cleanup, a valid wave id and
`settlement`, plus a committed record whose five keys match exactly.

- `tools/mori-evidence-loss.py:580-595`: when a disposed row has no issues, it is appended to
  `disposed` with `status:"structural_only"`. In the same branch it is also appended to
  `unresolved` with `reason:"external_review_required"`, and a non-invalid issue is added.
- `tools/mori-evidence-loss.py:596-601`: a disposed row with issues goes to `unresolved` with
  `reason:"disposition_invalid"`.
- `tools/mori-evidence-loss.py:612-619`: `pin_allowed` requires `not unresolved` **and**
  `len(disposed) == len(required_rows)`. Every disposed append comes with an unresolved
  append, and `_load_required` rejects an empty population (`:346`). So for every valid input
  `pin_allowed` is always `False`, and rc0 (`:636`) cannot be reached.
- `tools/mori-evidence-loss.py:1138-1148`: the selftest `declared_disposition` case pins this
  behaviour. It expects rc1, disposed1, unresolved1, invalid0, `pin_allowed:false`, finding
  `…:aggregator-r10:external_review_required`, and `trust_basis:"declared-record-not-authenticated"`.
  If someone removed `:590-595`, this case would fail. The guard has a discriminating
  author-side test.
- The actor check is a comparison of two declared strings (`:574-576`). The cleanup actor is
  never verified against the cleanup file's content (`:539-540`). In the real accounting, the
  cleanup actor `souji-shokunin <souji@shokunin.local>` is declared on a copy committed by
  `mori-shokunin` at `a8442a0` (`git log` on `cleanup-receipts.tsv`). Because A1 holds, this
  cannot lead to a pin. It does confirm that actor fields are declarations only.

Tradeoff, not a defect: the `pin_allowed` conjuncts for disposed and retained are dead code.
The contract's rc0 meaning ("complete valid accounting, zero unresolved") is kept only as a
reserved meaning, and `SKILL.md:521` says "not currently produced". Leave the code as is.
Removing the external-review append is exactly the regression that A1 guards against.

## A2 — real after rows

- `corpus/evidence/loss-accounting-r21.json`: both `aggregator-r10` and `aggregator-r10-resume`
  have `state:"unresolved"` and `independent_disposition:null`.
- I re-derived the hashes read-only:
  - The baseline is `0993b235…0478` both in the worktree and at `e9f340c`.
  - `removal-metadata.txt` is `4276625b…263e` both in the worktree and at `a8442a0`.
  - `cleanup-receipts.tsv` is `46f84c3a…70a7` both in the worktree and at `a8442a0`.
  - The required baseline identities equal the accounting baseline identities.
- [INFERENCE] I did not run the tool. From reading the code, the real audit should report
  omitted0, retained2, unresolved2 (both with reason `unresolved`), disposed0, invalid0,
  `pin_allowed:false`, rc1. This matches `SKILL.md:525-526`. There is no committed real audit
  receipt yet; `trust-refinement.md:9` requires one, and it is pending L1 acceptance.

### T1 (defect) — the oracle cannot tell "2 unresolved" apart from "2 garbage" or "2 declared-disposed"

`oracle-loss.py:79-88` checks only five things: the schema, rc==1, empty stderr,
`pin_allowed is False`, and `omitted == expected_omitted`. It never checks `unresolved`,
`invalid`, `disposed`, `unresolved_ids[].reason`, or the states of the source rows.

Counterexample (static, using `_load_accounting` at `:366-383`): an after accounting whose two
rows carry the right ids, `state:"x"` and null provenance would be accepted by the loader. It
would yield omitted0, retained2, invalid2, rc1 and pin false, and the oracle would report the
same after row as the real data ("0 omitted").

Two other inputs reach the oracle's after row in the same way:
- two self-authored disposed rows (unresolved2 with reason `external_review_required`);
- two tampered rows.

So the C1 after claim "0 omitted, 2 unresolved remain visible" (`contract.md:7`) is only half
measured by the independent instrument. The retained/unresolved half rests on the author's
selftest and on prose.

- Impacted claims: C1 freshness (measurement validity) and the trust boundary (a declared
  disposition is indistinguishable from a retained unknown).
- Smallest correction: L1 owns the oracle, so this is an instrument fix, not a production
  change. For each phase, derive the expected values from the source accounting rows and assert:
  - `unresolved == count(state=="unresolved")`;
  - every `unresolved_ids[].reason == "unresolved"`;
  - `disposed == 0` and `invalid == 0`.

  For the before phase, assert `retained == 0`. If the oracle's bytes must stay as historical
  record, add this as a separate post-integration check and disclose it.

## A3 — independent exercise of external-review-required

### T2 (defect) — the fixture runner's disposed cases are all masked by a record-shape mismatch

`fixture-loss.py:144-152` writes the disposition record with seven keys: `actor`,
`disposition`, `id`, `independent`, `fixture`, `kind`, `wave_id`. The tool requires the key set
to equal exactly `{id, actor, wave_id, disposition, independent}` (`tools/mori-evidence-loss.py:462`).
A literal set-equality check on those key names returns `False`.

Consequences, statically:
- Every fixture case with state disposed hits `disposition_record_mismatch` (`:577-579`).
  Such a row is never `structural_only`; it lands in `unresolved/disposition_invalid` with
  invalid≥1.
- `valid-independently-disposed` (`fixture-loss.py:266-269`) still expects rc0, unresolved0,
  disposed1 and `pin_allowed:true`. It fails, but because the record keys don't match, not
  because of external review. `FixtureLoss.md:40` predicted a trust-refinement mismatch; the
  observed failure has a different cause.
- `false-independent-boolean` and `same-actor-cleanup-only` (`:300-309`) would pass even if
  `independent_flag_invalid` (`:554-556`) or `independent_actor_not_distinct` (`:575-576`)
  were deleted. `FixtureLoss.md:27` says these cases test "the intended rejection condition
  rather than a digest/metadata mismatch"; that is false in practice.
- No independent harness ever produces disposed1/unresolved1 with reason
  `external_review_required`. Only the author's selftest (`:1138-1148`) does. That selftest has
  no case for `independent:false`, which is guarded twice anyway: once by `:554-556` and again
  by the record check at `:473`.
- Not on this seat's axis, noted for L1: `duplicate-accounting-id` expects rc1
  (`fixture-loss.py:280-284`), but duplicate ids are a setup error at rc2 (`tools/:377-378`).
  The runner's `fail` status will therefore have several causes, and L1 must read it per case.

- Impacted: the trust boundary (no non-author evidence for the declared-disposed→blocked
  property) and C1 mutation sensitivity.
- Smallest correction: keep the fixture bytes. In the acceptance record, label
  `valid-independently-disposed` as superseded by `trust-refinement.md:5`, with expected values
  rc1, disposed1, unresolved1, invalid0, pin false. Any later independent fixture must emit the
  exact five-key record so that the external-review path and the individual rejection checks
  are actually reached. Do not change the tool to satisfy the stale rc0 expectation.

## A4 — mandatory acceptance versus `--pin` interception

Honest statements found:
- `trust-refinement.md:9`: the raw `--pin` "still writes if directly invoked; it is not wrapped
  or changed".
- `SKILL.md:528-531`: "not interception of the existing raw `mori-census.sh --pin` write path".
- `corpus/lessons/round-21.md:48-52`.
- `corpus/knowledge/drift-repin-r20.md:102-107`: the r20 `recheck:` recipe is superseded.
- `SKILL.md:501-503`: QUALITY69 is applied before any pin.

Nothing claims OS-level prevention. Two softer phrases are both qualified later in the same
file, so I make no correction for them:
- "operational pin blocker" (`lessons/round-21.md:5`);
- "operationally blocking" (`contract.md:7`).

### T3 (defect, low) — the registry `kind` labels are inverted against the refinement

- The audit is labelled `probe (negative baseline-acceptance evidence…)` (`SKILL.md:521`).
- The classifier is labelled `gate` (`SKILL.md:522`).
- Mori's own convention is that a probe is "not a gate" (`SKILL.md:172`).
- `trust-refinement.md:9` and `lessons/round-21.md:49` call the audit "the mandatory …
  baseline-acceptance gate".
- `trust-refinement.md:7` denies that the classifier is a pin authority.

So the registry and the refinement are two sources that disagree on exactly which tool is
mandatory. A steward reading only the registry sees the classifier as the gate.

- Impacted: calibration (the "not authority" boundary of the C2 classifier) and the C1
  acceptance procedure.
- Smallest correction: an appended erratum below `SKILL.md:532` (do not rewrite the row). The
  audit is the mandatory baseline-acceptance gate, which only ever blocks: rc0 cannot be reached
  and it does not intercept `--pin`. The classifier is a synthetic-expectation gate only and
  never acceptance.

## A5 — provenance wording

### T4 (low)

`PROVINCE.md:177-178` calls a disposed row one that "cites a structurally validated, hash-bound
**independent** record". The tool asserts only `declared-record-not-authenticated`
(`tools/:588,634`). `:180-181` qualifies the phrase, but the noun still claims independence.

Correction: an appended erratum changing it to "a declared-independent record".

### T5 (low, ambiguity)

`SCORECARD.md:1295` lists `frozen/required.json` next to "requirements3b792db". In fact
`required.json` was first committed at `8fed329`, in the same commit as the after accounting
`loss-accounting-r21.json` (`git log`). It is not among the five files frozen at `3b792db`,
which are unchanged (`git diff --stat 3b792db HEAD` is empty).

The impact is limited: the two-id population is frozen in the contract prose
(`contract.md:7`) and hardcoded in the oracle (`oracle-loss.py:50`). The baseline triples are
hash-verified against `e9f340c`.

Correction: an erratum stating that the required file was authored at `8fed329`, after the
freeze, with only its id set frozen by the contract.

## Unknowns

- No real audit receipt is committed; the expected values above are [INFERENCE] from code.
- `oracle-loss.py:4` claims the oracle was written before reading target source. The oracle and
  the tool first appear in the same commit, `ce413b9`, so Git cannot verify the order.

## Commands run (all read-only)

- `wc`, `ls`, `sha256sum` on the three provenance files.
- `git -C <lane> log/show --stat/diff --stat/cat-file blob` for the hashes and the freeze check.
- One `python3` literal check that the fixture's key set ≠ the tool's five-key set. It does not
  import or execute the tool.
