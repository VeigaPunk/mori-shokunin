# FinalR24 — R24 "full provenance bindings retained" against the delivered tool

Seat: MoriR22.FinalR24 (critic, read-only, static). Scope: R24 only.

Sources read: `denominator-correction.md` (first), `contract.md`, `frozen/requirements-v2.json`, `oracle-reconcile-v2.py` (sha256 `dcd1c7c6…`, equal to its pin), `frozen/fixture-builder-v2.py` (`1b3e16f7…`, equal to its pin), `refinement-reconcile.py` (`06e104a3…`), `measure-round22.py` (`8205b15f…`), and the shipping `tools/mori-retention-reconcile.py` (`d6870fb6…`). The lane HEAD is `5888b56`. `git diff --stat 4f7cfce HEAD` over the tool, oracle, frozen directory, refinement and measure files is empty, so the retained `evidence/measure1` (measured at `4f7cfce`) applies to the current bytes.

No SUT, oracle, refinement, test, build or mutant was executed. The only commands run were read-only `git -C` plumbing (`rev-parse`, `log`, `status`, `merge-base`, `diff --stat`), `sha256sum`, and a field-limited Python read of retained `measure1` JSON for exit codes, booleans and digests. No hit text was printed. Static traces are marked [INFERENCE].

## Verdict

- **R24 holds for the delivered tool on the frozen valid branch.** Every bound field is derived from the objects the tool actually read.
- **The frozen R24 predicate is only partly fail-capable.** It cannot go red for argv content, for blob-versus-worktree digest source, or for input-revision resolution.
- **No retained run shows R24's provenance conjuncts going red.** The only retained R24 red, in the wrong-population mutant, comes from the exit/finding conjunct; every provenance field in that run is correct.
- **A same-command red control for R24 is missing.**

## 1. Branch-level reason the delivered tool satisfies R24 (valid variant)

The frozen R24 predicate is `oracle-reconcile-v2.py:61`, combined with the `record` gate at `:42`. It passes only if all of these hold:

- `exit == 0`
- `finding_id == RETENTION_RECONCILED`
- `stderr == ''`
- `input_revision == f['rev']`
- `measured_revision == f['measured_revision']`
- `tool_sha256 == sha256(tool bytes)`
- `inputs_sha256 == fixture digests`
- `argv` is a list

Trace through `check()` for `FIX.make(...,'valid')` with an absolute `--output`. The measure driver supplies one, and the retained after-run records an absolute fixture repo.

1. **Input revision:** `revision = resolve(repo, a.rev)` (`:156`), which runs `rev-parse --verify …^{commit}` once.
2. **Inputs:** `raw` comes from `committed()` (`:158`), so the bytes are Git blobs at `revision` via `ls-tree` and `cat-file`, with mode `100644/100755` and kind `blob`.
3. **Measured revision:**
   - It must be a full OID equal to its own `^{commit}` peel (`:161`).
   - It must be an ancestor of the input revision (`:163`).
   - Policy and allowlist bytes must be equal at the measured revision (`:164-165`).
4. **Receipt bindings:**
   - Recorded `--repo` is absolute (`:176`), and recorded `--policy` and `--allowlist` resolve to the supplied paths (`:177-182`).
   - argv `--rev` equals `measured` (`:184`).
   - Inner `commit` equals `measured` (`:186`).
   - `policy_sha256` equals the digest of the policy blob (`:187`).
5. **Reconciliation:** the valid fixture recomputes 5 raw, 1 non-author, 4 scanner, 3 allowlisted and 1 unallowlisted hits; `routed` is 0, `RETENTION_FINDINGS`, exit 1. That equals the receipt, so `differences == []`, giving exit 0 and `RETENTION_RECONCILED` (`:218`).
6. **Emitted fields** (`:225-228`):
   - `input_revision = revision`
   - `measured_revision = measured`
   - `inputs_sha256` is the digest of each loaded blob
   - `tool_sha256 = sha256(Path(__file__))`
   - `argv = sys.argv[1:]`

Retained observation: `after-observed.json` records R24 `pass:true` with tool `d6870fb6…`. In its valid run, `argv == cmd[2:]` exactly.

## 2. Branch-level reason R24 goes red — only one, and it is confounded

Across the retained mutants, R24 is red only in `mutant-wrong-population-observed.json` (tool `810277e4…`). Its valid run:

- exits 1 with `RETENTION_RECONCILIATION_MISMATCH` and `differences = [unallowlisted_hits, metric]`;
- has every provenance field correct: `input_revision`, `measured_revision`, `tool_sha256` and `inputs_sha256` all equal, and `argv == cmd[2:]`;
- still reports R03-shaped counts of 5/1/4.

So R24 went red only through the `cp.returncode == code` / `finding_id` conjunct, the same reason R01–R04 and R12 went red. The other mutants (count-only, false-clearance, setup-leak) leave R24 `pass:true`. The measure `killed` rule (`rc==1 and unmet>0`) does not record which requirement went red or why. The oracle `results` rows carry only `pass`, with no per-conjunct reason. **No retained artifact exercises R24's own provenance branch red.**

## 3. Smallest counterexample: frozen R24 passes a provenance violation

The mutant is one token at tool line 228: `'argv':sys.argv[1:]` → `'argv':[]`. The anchor occurs once.

- **Frozen 24 [INFERENCE]:** R24 still passes, because `isinstance([], list)` is true. Nothing else reads `argv`, so the suite scores 24/24. This violates the contract clause that argv appears in the output receipt (`contract.md:10`).
- **Caught elsewhere [INFERENCE]:** the mutant would be killed only by `refinement-reconcile.py:101` (`argv == cmd[2:]` on exit-0/1 cases) and by `measure-round22.py:106` (`real['argv'] == realcmd[2:]`). Measure never runs refinements against mutants, so that kill is asserted but not demonstrated.

Other mutants that survive frozen R24, re-verified against current sources [INFERENCE]:

| Mutant | Why frozen R24 misses it | Current refinement arm that would kill it |
|---|---|---|
| `'input_revision':a.rev` | The oracle passes a full OID | `symbolic-input` (`--rev HEAD`, expects full OID) |
| Read inputs from the worktree, not blobs | The valid worktree equals HEAD blobs | `dirty-worktree` |
| Drop `:187`, the policy digest check | No frozen arm changes `policy_sha256` | `wrong-policy-digest` |
| Drop `:186`, the inner commit check | R13/R14 fail earlier at the git read | `inner-commit-split` |
| Peel check at `:161` reduced to a regex | R13 still exits 2 via the git read | `measured-tag` |
| Policy dropped from the `:177` path loop | No frozen path arm | `policy-path-substitution` |

These refinement arms did not exist when `build/AttackR24.md` was written. That note's claim that refinements leave M1–M7 unverified is now **stale for the refinement suite** but **still true for the frozen 24 and for retained mutant evidence**.

## 4. Missing same-command red control

The missing control is a run of the exact `finite-after` command (`oracle-reconcile-v2.py --requirements frozen/requirements-v2.json --tool <T> --output <abs>`), with `<T>` a provenance-only mutant, expecting **R24 to be the sole unmet ID**.

The smallest fail-capable choice is `'tool_sha256':digest(Path(__file__).read_bytes())` → `'tool_sha256':digest(b'')`. The anchor occurs once, and no other frozen requirement reads `tool_sha256`. The expected result is `unmet == 1`, with the R24 row `pass:false` and the other 23 passing [INFERENCE].

For argv and blob-source mutants, the frozen predicate cannot go red. Their same-command red control must be the refinement command (`refinement-reconcile.py --tool <mutant>`), expecting exit 1 with the named cases failing. Today the refinement suite runs only against the shipping tool, which is green-only.

## 5. Latent hazard (not triggered by the measure driver)

`fixture-builder-v2.py:77` records `--repo str(root)`, and the oracle derives `root` from `--output` without resolving it. If `--output` is relative, the tool fails closed with `receipt_repo_binding` (`:176`) on every valid-based arm, and R24 fails at the exit conjunct. `measure-round22.py` resolves `HERE`, so its paths are absolute. This is an oracle-portability hazard, not a tool defect.

## Impacted axes

- **Calibration:** R24's 24/24 credit is not backed by a demonstrated fail-capable provenance arm. The only R24 red is collateral damage from the exit conjunct.
- **Depth:** the binding lines exist and are exercised green, but they are not distinguished by retained red evidence.
- **No regression, duplicate authority or false provenance in the shipping tool for R24.** At the claim level, `realmatch` (argv, tool digest, revisions) and the refinement checks compensate for the frozen predicate's weakness, so `all_claim_checks_pass` would catch an argv drop on the real run.

## Fixable defect versus tradeoff

- **Frozen oracle:** the vacuous argv conjunct, and the absence of blob-versus-worktree and symbolic-revision discrimination, are frozen defects pinned by `oracle_sha256`. The judge must not count R24's argv/blob/resolution conjuncts as evidence. They cannot be fixed without re-freezing, which would be a contract change.
- **Measure driver:** it is unpinned and can be fixed.

## Smallest safe correction (frozen bytes unchanged)

In `measure-round22.py`, add these entries to `mutations`:

1. `('provenance-tool-digest', [("'tool_sha256':digest(Path(__file__).read_bytes())","'tool_sha256':digest(b'')")])`. Judge it by the frozen 24, with the kill condition that the unmet IDs are exactly `{'R24'}`, not just `unmet > 0`.
2. `('provenance-argv-drop', [("'argv':sys.argv[1:]","'argv':[]")])`. Judge it by `refinement-reconcile.py --tool <mutant>` with `rr == 1`, and record `frozen24_unmet == 0` explicitly as an expected survivor.

Also record the unmet ID set for every mutant, so a kill can be attributed at the requirement level. Leave R24's stated pass unchanged, but cite its provenance strength from the refinements and `realmatch`, not from the frozen predicate.

## Tooling

No installs or updates.
