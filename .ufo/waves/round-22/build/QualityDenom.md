# QualityDenom — Q51/Q57/Q63 count and binding, Q69 acceptance, one new criterion

Seat: MoriR22.QualityDenom (scout, leaf). Read-only. Repository HEAD observed at `306e06ecd02e0ea8e544fbd30d1ff7e7359c581e`.
Inputs read: `corpus/QUALITY.md`, round-22 `contract.md`, `frozen/fixture-builder.py`, `frozen/requirements.json`, `oracle-reconcile.py`,
`corpus/lessons/round-18.md`, `round-19.md`, `round-21.md`, and round-21 `evidence/final/retention-floor{,-entering}.json`
(field projections only: counts, paths, classes, revisions; no matched text was printed or copied).
I ran no tests, builds, linters, retention gate or reconcile tool. Every figure below comes from `jq` projections of committed receipts
or read-only `git -C` plumbing (`rev-parse`, `ls-tree`, `merge-base --is-ancestor`, `cat-file -p | sha256sum`, `log -1`).
I installed or updated nothing; `jq`, `git` and `sha256sum` were already present.

## Headline (observed)

The contract's frontier statement, "raw95 incl5 policy versus 90 scanner", does not match the committed receipt's identities.

| Population at `9fb1f911` (r21 `retention-floor.json`, wrapper exit 1) | Count | How determined |
|---|---|---|
| `hits` (raw) | 95 (95 unique identities) | array length |
| `allowlisted_hits` | 86 | array length |
| `unallowlisted_hits` (`metric`) | 4 | array length; `metric`=4 |
| hits − (allowlisted ∪ unallowlisted), by identity `(path,line,class,line_sha256)` | 5 | set difference; 0 partition identities absent from `hits` |
| …of which in `corpus/lessons/round-17-verifier-spotcheck.md` / `round-18-verifier-spotcheck.md` | 3 / 2 | classes R9,R6,R6 / R5,R6 |
| `non_author` field | 5 | scalar |
| hits at the exact policy path `.ufo/waves/round-18/frozen/c1-policy.json` | 4, all allowlisted, 0 unallowlisted | path filter |
| hits at the copy `.ufo/waves/round-20/falsify/NoHarmRun/rg/.ufo/waves/round-18/frozen/c1-policy.json` | 4, = all 4 unallowlisted (R2,R5,R6,R8) | path filter |

- The 90 is `allowlisted + unallowlisted`, which is raw minus the 5 **non-author** identities. The policy glob `non_author_paths_glob` = `corpus/lessons/round-*-verifier-spotcheck.md`, `corpus/lessons/operator-*.md` (policy blob at `9fb1f911`) explains that exclusion.
- The exact policy source contributes **4** hits, not 5, and none of them is unallowlisted.
- [INFERENCE] The "5 policy" figure is the `non_author`=5 count attributed to the wrong exclusion. That is exactly the count-subtraction error the round-22 root lesson names. I cannot see the source of the contract's "scanner90" label. Neither round-21 waves nor round-22 frozen files contain it (bounded grep of `.ufo/waves/round-21`; frozen files inspected).
- [INFERENCE, not measured] Applied to this real receipt, the contract's own rule (exclude exactly the supplied policy path, keep everything else) would yield: `raw_total`=95, `policy_excluded`=4, `scanner_total`=91, `raw_unallowlisted`=4, `scanner_unallowlisted`=4 (the unallowlisted hits sit in the round-20 copy, which the policy-path rule does not exclude), `non_author`=5. Under QUALITY #55 the frozen rule wins over the "95/5/90" narrative. The synthetic R03 fixture (5/1/4) is unaffected.
- Retention remains **red** (4 unallowlisted), and `privacy_clearance` must stay false. Nothing here is clearance.

I sent this finding to `agent://MoriR22` (decision affecting R02's real-run expectations) and `agent://MoriR22.LessonDraft` (lesson row accuracy).

## Binding defect in the entering receipt (observed)

`retention-floor-entering.json` (sha256 `878991395ec4f0e89364377009748b25ec55993934e016fbf049955228696f72`, landed at `77a5bbe8`):
- wrapper `measured_revision` = `9fb1f911cfdd6061005c300795f44b1b45523897`;
- argv `--rev` = `e9f340ce986f82a60baad1b8e5ead655ab818a1c`;
- stdout `commit` = `e9f340ce…`.

The wrapper claims a revision it did not scan. Its `hits`/`allowlisted_hits`/`unallowlisted_hits` arrays are byte-identical to the final receipt's, and the policy and allowlist blob ids are equal at `e9f340ce`, `9fb1f911`, `77a5bbe8` and `306e06ec` (`8bf285bd…` and `f8be55b1…`). So a recomputation keyed on the wrapper `measured_revision` would likely **reconcile (exit 0) while masking the mis-binding** [INFERENCE: hit equality at both revisions observed; recomputation not run].

Requirements gap: every `fixture-builder.py` variant sets wrapper `measured_revision`, `result['commit']` and argv `--rev` together (`invalid-revision`, `diverged` at :86-91; valid path :72-76). No R01–R24 arm tests a disagreement among those three fields. R24 (`oracle-reconcile.py:61`) checks only the tool's echoed `measured_revision` against the fixture's wrapper value. The contract text binds "Receipt target measured_revision" alone. Under Q57 ("binds… exact measured revision") and Q58 ("carries the measured full commit… and argv"), a three-way disagreement should be setup/unevaluable (exit 2), not reconciled against any one of the three fields. Route: L1 integration decision. I am not proposing a new requirement ID, because the frozen requirements are frozen.

Other bindings at `9fb1f911`: the receipt's `policy_sha256` `db06e981…` equals sha256 of the policy blob bytes. `9fb1f911` is an ancestor of HEAD (rc0). `e9f340ce` is an ancestor of `9fb1f911` (rc0). `stderr` is empty.

## Q51 — count and binding

- **Status at r21 tip: not satisfied.** Q51 requires "zero unallowlisted hits" at the measured revision. Observed `metric`=4 and exit 1 at both `e9f340ce` and `9fb1f911`. `round-21.md:141-142` records "red4→4… no privacy/history clearance". This is carried debt, not a pass.
- **Count gap:** Q51's "zero unallowlisted" is computed over 90 identities, after the 5 non-author exclusions. Q51 never names that exclusion. A Q51 zero would therefore be silent about out-of-author hits. R12 reports `non_author` separately for the reconcile tool. Q51 itself carries no such requirement.
- Must-redact clause: `forbidden_allowlist`=0 at `9fb1f911`; the policy declares 3 `must_redact_paths`. Consistent with Q51; no claim beyond that.
- `line_sha256` identities are short-line digests. Per Q51's last sentence and S052 (round-18 Gate), they are provenance, not redaction. The reconcile tool's digest-only identity output inherits that limit.

## Q57 — count and binding

- Q57: "an additional bounded review never replaces the all-blob retention gate or narrows its allowlist denominator." The contract's `scanner_total` is a narrowed denominator. It is compatible with Q57 only as a secondary, labelled figure while `raw_total` stays authoritative, as the contract states. Any report citing 90 or 91 as "the" denominator would breach Q57.
- Q57's "exact measured revision" binding is not met by the entering receipt above. A reconciliation must require three-way revision agreement to honour Q57.
- Q57's population clause ("covers every path in its frozen population") maps to recomputing over every tracked blob at the measured revision. `git ls-tree -r` at `9fb1f911` lists 7715 paths (count only; not a hit population).

## Q63 — before/after counting

- `oracle-reconcile.py:24-25` assigns `capability_absent` when `--tool` is not a working-tree file. That is an actual filesystem observation, not a phase label, so it complies with Q63's letter. However, the before result records neither the stat outcome nor any revision.
  - Observed independently: `tools/mori-retention-reconcile.py` is absent in the tree at `e9f340ce`, `9fb1f911`, `77a5bbe8` (entering) and `306e06ec` (`ls-tree`, count 0).
  - Recommendation: L1's before receipt should bind the absence to the entering revision's tree, not to a working-tree path. A path absent from the worktree is not the same as a path absent from the measured tree.
- Same instrument and unchanged expectations: both modes run one `oracle-reconcile.py`. Its output records `requirements_sha256`, `fixture_builder_sha256` and `oracle_sha256` (:23). The expected values live in the oracle predicates and the fixture builder, both digested, while `requirements.json` holds IDs only. Consistent with Q63.
- Q62 distinction holds: when the tool is present, a crash or non-JSON output is recorded as `pass:false` without `capability_absent` (:36-45).
- R02 in the oracle (:48) is synthetic (`raw_unallowlisted==1`). The contract's real-retained "four unallowlisted" claim is **not** a finite-oracle requirement. Per Q63, it needs its own L1 receipt derived from the tool's returned fields. Per the identity table above, its policy-excluded and scanner values would be 4 and 91, not 5 and 90.

## Q69 — acceptance

- Q69 blocks baseline acceptance on unaccounted evidence loss. Round-21 refines the audit to a "negative-only observation prerequisite, not a positive authorization gate" (`round-21.md:101-104`), superseding the ":48-50 mandatory acceptance gate" shorthand. Q69's QUALITY.md text does not carry that refinement, though it states a blocker and therefore is not contradicted.
- Round 22 changes nothing for Q69. Both historical disappearance dispositions remain unknown (`round-21.md:19,35`). The original permission control remains RED 11/12 (`round-21.md:137-138`). Baseline acceptance stays blocked.
- Analogy rule, already implied by Q69's "same-identity posthoc pushed receipts prove cleanup, never independent lifecycle closure": a reconciled retention receipt proves accounting agreement, never clearance or acceptance.
- Unverified: whether outside closure admitted Q69. I did not open the fleet MANIFEST, which is outside the named files. "r21 admitted" is taken from the contract only and is not privacy clearance.

## One new criterion (draft; admission is the outside closure's decision)

> 70. A denominator reconciliation is an identity partition, not arithmetic. State every population (raw, each exclusion, each derived denominator) as an identity multiset `(path, line, class, line digest)` with the rule that selects it. Attribute a count difference to an exclusion only when the removed identities are exactly that rule's members. The raw denominator stays authoritative; a narrower compatible denominator is secondary and labelled. Exact agreement, zero delta or zero new hits never clears privacy: unallowlisted > 0 stays retention red and `privacy_clearance` stays false.
> ← lessons/round-22.md#M&lt;n&gt; (root lesson per round-22 `contract.md:22`; **citation pending that row's landing**); r21 `evidence/final/retention-floor.json` at `9fb1f911`: the 95→90 gap is the 5 non-author identities, the exact policy path holds 4 allowlisted hits.

Lesson backing: the contract names this root lesson ("population equality is checked by identities and explicit exclusions, never count subtraction alone; an agreement gate is distinct from privacy clearance"). The receipt analysis above is a concrete instance where count subtraction mislabelled the exclusion. No `corpus/lessons/round-22.md` exists yet (only round-18 to round-21 were found), so the criterion must not be admitted until that row lands with this evidence pointer. No new source rows were opened or proposed.

## Remaining unknowns

- The origin of the "scanner90 / 5 policy-source hits" figures, if they come from some instrument other than `mori-retention-gate.py`.
- The tool's actual output on the real receipts (not run; L1 measures after integration).
- Whether L1 treats wrapper/argv/commit disagreement as setup (exit 2) or reconciles against one of the fields.
- Outside-closure admission status of Q69 and of the drafted Q70.

Checks for L1 after integration: run `oracle-reconcile.py` before and after. Run the reconcile tool on both round-21 receipts and confirm 95/4/91/4/4/5 by identity, and confirm the entering receipt is rejected or flagged for revision disagreement. Confirm `privacy_clearance` is false on every arm.
