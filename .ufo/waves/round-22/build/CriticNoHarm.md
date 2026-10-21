# CriticNoHarm — round 22 no-axis-harm review

Seat `MoriR22.CriticNoHarm` (critic, read-only, leaf). Scope: the C1 calibration capability in `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-22/contract.md` (contract blob sha256 `1658c390…321a1`, as pinned in `frozen/requirements.json`). I checked it against all six held scores: coverage 6, operability 7, depth 5, freshness 5, calibration 5, adjacency 6.

The ImplReconcile candidate had not landed when I reviewed. So this review covers the contract, the r21 receipts, the existing gate (`tools/mori-retention-gate.py`), and L1's frozen `frozen/fixture-builder.py` and `oracle-reconcile.py` from commit `e825c7f`.

**Nothing here clears existing debt.** The r21 admission is not privacy clearance. The original permission control stays RED 11/12. Both historical dispositions stay unknown, and baseline acceptance stays blocked.

## Method and what was actually run

- Read-only `git -C` plumbing only: `show`, `ls-tree`, `cat-file`, `rev-parse`, `merge-base`, `log`, plus `hash-object` on one retained file (no write). I ran no tests, builds, gates, oracle, fixture builder or candidate.
- I parsed both r21 receipts structurally with a short Python reader. It printed only counts, paths, classes, and partition letters. It printed no line text.
- **One measurement I did run:** a static regex count. I applied the real frozen policy classes (read as a blob at HEAD) to every committed blob under `.ufo/waves/round-22/` plus `LOG.md`, at both `77a5bbe` and HEAD `e825c7f`. I also applied them to the 30 pending working-tree files under `round-22/build/`. Result: **0 hits** at every revision checked (18 committed files at HEAD, 30 pending). This is not a run of the gate. It is a no-harm baseline for the integration check below.
- I did no installs or updates.

## Counterexamples (strongest first)

### CX1 — a supplied policy path with the same bytes erases the entire red set from the scanner view (calibration, depth)

**Evidence.** At measured revision `9fb1f911` (and at `77a5bbe`), two tracked paths share one blob, `8bf285bddce57f7fdefbbf514cb0b3bf97652742`:

- `.ufo/waves/round-18/frozen/c1-policy.json` has 4 hits, all allowlisted.
- `.ufo/waves/round-20/falsify/NoHarmRun/rg/.ufo/waves/round-18/frozen/c1-policy.json` has 4 hits, all unallowlisted. Last touched in `71abd41`.

All 4 retained unallowlisted hits are the copy's lines. The r21 lesson (L141) already calls them "inherited synthetic-policy copy lines".

**Attack.** Run `check … --policy .ufo/waves/round-20/falsify/NoHarmRun/rg/.ufo/waves/round-18/frozen/c1-policy.json`. Every contract-named guard passes:

- The path is safe and is not a symlink.
- Its bytes at the input revision equal its bytes at the target revision, so R15 does not trip.
- Its sha256 `db06e981…3128` equals the receipt's `policy_sha256`.
- Its classes are identical, so recomputation agrees and the tool exits 0 `RETENTION_RECONCILED`.

But "policy-excluded = exactly the supplied policy path" now removes the 4 red copy hits instead of the 4 allowlisted originals. The result is `policy_excluded=4`, `scanner_total=91`, and **`scanner_unallowlisted=0`**, under a successful reconciliation. `raw_unallowlisted` stays 4, so the raw authority survives. But the secondary denominator now reads clean. That is a calibration harm, and it is exactly the kind of count-only agreement the root lesson forbids.

The same trap fires without path substitution if the exclusion is keyed by blob OID, content digest, basename, or a path suffix. RawPartition and AttackR21 note the content-keyed variant. As far as I could find, no seat covers the path-substitution variant.

**Smallest safe correction (fixable defect, not a tradeoff).** Bind `--policy` and `--allowlist` to the receipt:

- Find the value after `--policy` (and after `--allowlist`) in the receipt `argv`. It must equal the receipt's argv `--repo` value + `/` + the supplied REPO_REL, as an exact string with no filesystem resolution. Resolve relative argv paths against the receipt `cwd` first.
- If either does not match, exit 2 with error `input_not_receipt_bound`.

This is compatible with the frozen fixture, whose argv already uses `str(root)` and `str(root/POLICY)`. Add one mutant arm: the valid fixture with a byte-identical second policy copy, passed as `--policy`, must exit 2.

### CX2 — the frozen fixture's allowlist conflicts with the gate semantics the contract requires (operability, depth)

**Evidence.**

- `tools/mori-retention-gate.py:142-152` requires each allowlist row's field set to be exactly `{path, class, line_sha256, reason, rule}`, with `rule` in `{a,b,c}`. Otherwise it raises `invalid_allowlist_row`, which exits 2.
- `frozen/fixture-builder.py:56-60` writes rows containing only `path`, `class`, `line_sha256`, `reason`. There is no `rule`.

The contract says raw partitions "reproduce existing non_author_paths_glob and allowlist semantics".

**Consequence.** A reconciler that mirrors the gate's validation fails closed with exit 2 on every allowlist-dependent oracle arm: R01–R04, R11, R12, R22–R24. A reconciler lenient enough to pass the oracle accepts allowlists the production gate rejects. That makes it a second, looser authority on allowlist validity. Either outcome harms an axis.

The real retained allowlist (`corpus/evidence/retention-allowlist.json`: a dict with keys `note`, `rows`, `schema`; 86 rows; rules a×79, b×7) does carry `rule`. So only the synthetic fixture is wrong.

**Smallest safe correction.** Fix the frozen fixture before integration, under the contract's "expected values and fixture generator committed before implementation integration": add `'rule':'a'` to each synthetic row. The reconciler must then require the exact gate row shape. Commit the fixture fix as its own freeze commit, before the implementation lands, so the order stays honest. This is a defect, not a tradeoff.

### CX3 — the real retained receipt is never exercised by any frozen arm (calibration, freshness)

**Evidence.** `oracle-reconcile.py` calls only `FIX.make(...)` synthetic fixtures. The contract's load-bearing sentence is: "the real retained result must continue to show four unallowlisted hits, and privacy_clearance=false". It has no arm against `.ufo/waves/round-21/evidence/final/retention-floor.json`.

**Expected real-data values, by identity.** RawPartition, AttackR21 and EnteringPartition independently match these values:

- exit 0, `RETENTION_RECONCILED`
- `raw_total` 95, `policy_excluded` 4, `scanner_total` 91
- `raw_unallowlisted` 4, `scanner_unallowlisted` 4
- `non_author` 5, `forbidden_allowlist` 0
- `retention_state` red, `privacy_clearance` false

The open-debt phrasing "5 policy source hits / scanner 90" is the gate's non-author subtraction: 95 − 5 = 90, the population summary's `metric_before`. It is not a policy-file subtraction. Pinning 5/90 against the real receipt would force either a false mismatch or a conflated exclusion. A conflated exclusion would merge two authorities: R12 non-author and the policy path.

**Smallest safe correction.** L1 runs one real-data invocation after integration and retains it as evidence, with these expected values committed beforehand:

`check --repo /home/vgpnk/Projects/shokunin/mori-shokunin --rev <integration commit> --receipt .ufo/waves/round-21/evidence/final/retention-floor.json --policy .ufo/waves/round-18/frozen/c1-policy.json --allowlist corpus/evidence/retention-allowlist.json`

The receipt blob `5c81c3f9…` is committed unchanged at `77a5bbe` and at HEAD. Its measured revision `9fb1f911` is an ancestor of `77a5bbe`. Policy and allowlist bytes are equal at both revisions.

Also correct the lesson and quality narrative to 4/91. LessonDraft's brief asks for a "precise source of 5 policy exclusion", which the evidence contradicts.

### CX4 — the wrapper revision can be false provenance (freshness)

In `retention-floor-entering.json`, the wrapper `measured_revision` is `9fb1f911`, but argv `--rev` and stdout `commit` are `e9f340ce`. The hit multisets of the two receipts are identical. So a tool that recomputes only at the wrapper revision returns exit 0 and names `9fb1f911` as measured, which is false provenance that its output cannot reveal.

EnteringPartition, KnownGaps and AttackR21 already raise this. My no-harm framing:

- Require wrapper `measured_revision` == stdout `commit` == full-id resolution of argv `--rev`, else exit 2.
- The entering receipt then becomes a real-world exit-2 negative, not a defect. It must not be "fixed" by picking a revision.

## Gate-parity checks that protect depth (each is a concrete, falsifiable criterion)

1. **Allowlist container.** The gate accepts either a bare list or a dict's `rows` (`:318-319`). The real allowlist is a dict. Rejecting a dict fails the real-data run.
2. **Allowlisted is not disjoint from non-author.** The gate's `allowlisted_hits` does not filter non-author paths (`:261`), but `unallowlisted_hits` does (`:262-266`). In the retained data the sum 86 + 4 + 5 = 95 closes only because no allowlisted hit is non-author. The reconciler must compare each list by identity and must not assert `raw = allowlisted + unallowlisted + non_author`. Fixture: one allowlisted hit on a non-author path. Expect `allowlisted` to include it, `non_author` to include it, and `unallowlisted` to exclude it.
3. **One allowlist row allows every hit with the same `(path, class, line_sha256)`, across lines.** The frozen fixture's `allowed.txt` exercises this (2 hits, 1 row). Keep it.
4. **Finding precedence** is `allowlist_forbidden` > `RETENTION_FINDINGS` > `allowlist_stale` > `RETENTION_CLEAN` (`:280-287`). A forbidden row never allows. `routed` counts only unallowlisted hits on `must_redact_paths`.
5. **Symlink blobs are part of the scanned population.** The gate skips only non-blob entries and mode `160000` (`:199`). At `9fb1f911` there are 4 mode-`120000` entries, all under `round-17/fixtures/`. The contract's "committed symlink input is rejected" applies to the three input paths only. Real data cannot catch a reconciler that skips symlink blobs, because none of the 4 targets hits. Add a synthetic arm: a committed symlink whose target text matches the synthetic class must count as one raw hit.
6. **Path and line decoding.** Paths are decoded as UTF-8 with `errors=replace`. The line digest is the sha256 of the replaced text, split on `\n` only, so `\r` is kept.
7. **Receipt `policy_sha256` must equal the sha256 of the policy blob at the measured revision.** The gate hashed worktree bytes at run time (`:311-313`), so blob equality is the only binding the receipt offers. If they differ, exit 2.
8. **Unsupported receipt modes.** If the receipt argv contains `--expect-population` or lacks `--allowlist`, recomputation cannot reproduce it. Exit 2 (unsupported), never a guessed exit 0.
9. **Compare lists as multisets, not in order.** Gate order is `ls-tree` path order. The frozen fixture's stdout lists hits in dict-insertion order. An order-sensitive reconciler would falsely report MISMATCH on R01.

## Per-axis no-harm checks for L1 after integration

None of these were run by this seat. Each is falsifiable.

| Axis (held) | Check | Pass condition |
|---|---|---|
| coverage 6 | `git -C <repo> diff --stat 77a5bbe..<integ> -- tools/` | exactly one added file, `tools/mori-retention-reconcile.py`; no census/silence tool touched |
| operability 7 | sha256 of `tools/mori-retention-gate.py`, and the snapshot pin | `cf0896a2…829e` (blob `988c5484`) unchanged; `round-18/gate-snapshots/retention/retention.json` sha256 `55fcdd71…00e8` unchanged |
| operability 7 | oracle/impl field contract | the output carries every key the frozen oracle reads: `raw_hits`, `scanner_hits`, `policy_excluded_hits`, `input_revision`, `measured_revision`, `tool_sha256`, `inputs_sha256{receipt,policy,allowlist}`, `argv`, integer counters, `retention_state`, `privacy_clearance`; `stderr` empty on every arm |
| depth 5 | real-data run (CX3) | 95/4/91/4/4/5/0, red, false; plus the policy-excluded identities equal the 4 original-path digests, not the copy's |
| freshness 5 | r21 evidence byte-unchanged | sha256 `retention-floor.json` = `4001e2d9…c840`, `retention-floor-entering.json` = `87899139…6f72`; blobs `5c81c3f9…` / `df160d7c…` |
| calibration 5 | path-substitution mutant (CX1) and literal clearance | copy-path `--policy` exits 2; no code path can emit `privacy_clearance` other than JSON `false` |
| calibration 5 | real retention floor unchanged by round-22 | rerun the static count, or the gate itself at `<integ>`: unallowlisted multiset = the same 4 copy-path identities, and 0 new hits from round-22 files (baseline measured above: 0) |
| adjacency 6 | no clearance by cleanup or allowlisting | `<integ>` diff neither deletes nor modifies the round-20 nested policy copy, adds no allowlist rows, and leaves `c1-policy.json` and `retention-allowlist.json` bytes unchanged (`db06e981…3128`, `f46c78ec…c63b`) |

## Tradeoffs the canonical judge must reject (not fixable inside this claim)

- Deleting the round-20 nested copy, or allowlisting its 4 lines, would turn the retained floor green. That is history and policy actuation, outside this detection-only claim. It would also break "keep original evidence byte-unchanged". Under this contract it must be rejected, not admitted as a calibration gain.
- Making `scanner_total` equal 90 by any exclusion other than the exact bound policy path is the count-subtraction trap. Reject it.

## Residual unknowns

- I did not review the ImplReconcile candidate, because it had not landed.
- Why `71abd41` committed a byte-identical policy copy, and what that copy's disposition is, were not investigated. Both stay unknown.
- Whether the 4 symlink targets at the measured revision would hit under any class: I inferred no hit because their paths are absent from the receipt's hit list. I did not recompute.
