# FinalR14 — falsification of R14 "target not ancestor returns 2"

Seat: MoriR22.FinalR14 (critic, read-only, leaf). Static analysis only: no tool, oracle, fixture, selftest, refinement, mutant or measurement was executed. Git use: read-only `log`/`show`/`status`/`diff --stat`/`rev-parse`/`merge-base --is-ancestor` against the lane repo. Retained measurement evidence was read field-limited (`id`, `pass`, `variant`, `exit_code`, `error`, `tool_sha256`, mutation `id/killed/unmet`); no stdout bodies or matched text copied. Nothing installed.

Effective correction read first (`denominator-correction.md`); it does not touch R14 meaning.

## Inputs verified against current shipping source

| Input | sha256 | Binding |
|---|---|---|
| `tools/mori-retention-reconcile.py` (HEAD 5888b56, clean) | `d6870fb6…0ce7` | equals `tool_sha256` in `evidence/measure1/after-observed.json` and `refinement-observed.json` (measured at 4f7cfce; `git diff 4f7cfce HEAD` empty for tool/oracle/refinement/measure/frozen) |
| `oracle-reconcile-v2.py` | `dcd1c7c6…adb` | equals `requirements-v2.json.oracle_sha256` |
| `frozen/fixture-builder-v2.py` | `1b3e16f7…15d1` | equals `requirements-v2.json.fixture_builder_sha256`; frozen in e2f549b, ancestor of SUT commit 8cb4afb |

## Verdict

- **Exit-level R14 holds** on the shipping SUT, by static path walk and by the retained observation (`R14 pass=true`, `exit_code=2`).
- **Branch-level reason requirement fails.** The frozen R14 arm doesn't isolate the ancestry branch: an SUT with the ancestry check deleted still passes R14 (and all 24 frozen arms). The shipping SUT's R14 reason (`git_read_failed`) is the same generic code that R13 and every git failure produce, so the reason can't attest that the ancestry branch fired.
- **The same-command red control is missing.** No mutant targets ancestry. The refinement arms that *would* discriminate (`diverged-consistent`, `cousin`, `head-cousin`) have only ever run against the green SUT, never against a red one under the same command.

## Branch walk on the shipping tool (frozen `diverged` arm)

Fixture (`fixture-builder-v2.py:89-92`): `other = commit-tree <M1 tree>` (parentless, unreferenced). It sets `wrapper.measured_revision=other` and `result.commit=other`. It does **not** set `wrapper.argv[--rev]`: that argv list was built at line 77 with the original `measured` (M1).

`check()` order in `tools/mori-retention-reconcile.py`:
1. `:155-158` resolve `--rev`, read the three blobs at input revision, `receipt_schema`: all pass.
2. `:160-161` `measured` is 40-hex and `resolve(other)==other`: passes.
3. `:163` `git merge-base --is-ancestor other R`. The return code is nonzero, and `git()` `:59` raises `Invalid('git_read_failed')`, so the tool exits 2 with `RETENTION_RECONCILIATION_SETUP`. **This is the first failing branch on the shipping SUT.**

Observed: the `diverged` run gives `exit_code=2`, `error=git_read_failed`. The `invalid-revision` (R13) run gives `exit_code=2` with the **identical** `error=git_read_failed`, because `resolve()` `:64` fails through the same `git()` `:59`. The two branches can't be told apart from their output.

## Smallest counterexample (frozen arm not fail-capable for its own defect)

Mutant **M-noanc**: delete the single line `tools/mori-retention-reconcile.py:163` (`git(repo,'merge-base','--is-ancestor',measured,revision)`).

Static walk of M-noanc on the frozen `diverged` arm:
- `:164-165` compares policy and allowlist bytes at `other` with those at R. They are equal, because `other`'s tree is M1's tree and the diverged variant changes neither file.
- `:166-171` policy, allowlist, exit, stderr, stdout and argv types all pass.
- `:174-182` the `--repo` and absolute `--policy`/`--allowlist` bindings resolve to `policy.json`/`allowlist.json`, so they pass.
- `:184` `argv[--rev]` is M1 but `measured` is `other`, so it raises `Invalid('receipt_revision_conflict')` and exits 2 with `RETENTION_RECONCILIATION_SETUP`.
- The oracle (`oracle-reconcile-v2.py:42,54`) checks only exit 2, `finding_id`, `stderr==''` and parseable JSON, so **R14 passes**. No other frozen arm exercises ancestry: R01 is a true ancestor, and R13 fails earlier at `:161`. So the frozen result is 24/24 with `unmet=0`.

So the frozen R14 "pass" can't be cited as evidence of the ancestry capability. The defect is the stale `argv --rev` confound that AttackR14 F1 reported against v1. I re-verified it here against v2: `fixture-builder-v2.py` froze it unfixed.

A second escaping class: mutant **M-exists** replaces `:163` with `git(repo,'merge-base',measured,revision)`, a merge-base-existence check. On the frozen `diverged` arm the orphan has no merge base, so it fails with `git_read_failed` and R14 passes. This mutant also passes all 24 frozen arms [INFERENCE: static; not executed].

## Where discrimination actually lives, and why it is unproven

`refinement-reconcile.py:20,26-32,81` adds three arms that fix the confound by binding `argv --rev` to `other`:
- `diverged-consistent`: parentless.
- `cousin`: `-p M1`, sibling of R.
- `head-cousin`: cousin with HEAD moved onto it via `update-ref`.

Each expects exit 2 with `error=='git_read_failed'`. Static walk against M-noanc: every check through `:194` passes and the scan at `other` equals M1's 5 hits. The partitions, counters, `finding_id`, and exit 1 versus retention code 1 all agree, so M-noanc returns **exit 0 `RETENTION_RECONCILED`** and all three arms go red. Against M-exists, `cousin` and `head-cousin` go red because the merge base is M1.

This evidence is unproven for three reasons:
- **Provenance.** These arms aren't in SUT commit 8cb4afb or 3985b3d. They first appear in `b095ecc` ("wip: mid-round checkpoint"), after implementation. `refinement-reconcile.py` is not pinned in `requirements-v2.json`. They are co-evolved controls authored by the SUT owner, not frozen independent requirements.
- **No red control under the same command.** `measure-round22.py:77-96` defines exactly four mutants: count-only, false-clearance, wrong-population and setup-leak. None touches `:163`. Every mutant runs only the frozen oracle command (`args`, kill basis `frozen24-oracle`). The refinements command (`:74`) runs once, against the real tool only. Retained summary: all four mutants killed, `all_killed_and_restored=true`. No observation shows any R14-relevant arm, frozen or refinement, going red.
- **The asserted reason is not branch-specific.** `error=='git_read_failed'` is also emitted by `:64` (R13), `:72` `ls-tree`, `:86` `cat-file`, and `:145` scan `cat-file`. The arms discriminate only through the valid-versus-variant differential, not through the reason.

## Lower-severity SUT-side counterexample [INFERENCE, not executed]

`git()` `:54-55` strips `GIT_*` and passes `--no-replace-objects`, but nothing disables `$GIT_DIR/info/grafts` or a `shallow` file. Ancestry at `:163` is therefore computed partly from uncommitted local metadata. A graft that gives `other` the parent M1 would make `--is-ancestor` succeed, and the tool would return exit 0 for a truly non-ancestral measured commit.

Contrast with the inputs: the contract has the receipt, policy and allowlist read as Git blobs rather than worktree files, but it doesn't bind the history used for ancestry. This is a tradeoff about trusting the operator-supplied repo, not a frozen-arm failure. Record it as a residual unknown rather than a fix demand.

## Impacted axes

- **calibration** (primary): R14's frozen pass overstates capability, and the mutation evidence reports "all killed" with no ancestry mutant.
- **depth**: the frozen oracle has a confounded arm.
- **freshness**: the v1 finding F1 was carried into v2 unfixed.
- Coverage, operability and adjacency are unchanged.

## Smallest safe correction (no frozen-input rewrite)

1. **Same-command red control.** In `measure-round22.py`, add mutant `no-ancestry`, replacing the `:163` line with `pass` (and optionally `exists-only`). Run it through **the refinements command** (`refinement-reconcile.py --tool <mutant>`) with kill basis `refinements`. Require `diverged-consistent`, `cousin` and `head-cousin` to be `pass=false` (exit 0, not 2), and require `exists-only` to fail `cousin`.
   - Separately, record that under the frozen24 command `no-ancestry` survives (`unmet=0`). That survival is itself the retained proof of the frozen R14 confound, so report it as a finding rather than calling it a kill.
2. **Branch-specific reason.** In the SUT, run `merge-base --is-ancestor` directly. Map rc 1 to `measured_not_ancestor` and any other nonzero rc to `git_read_failed`, then update the three refinement expectations. This makes R13 (`git_read_failed` at resolve) and R14 distinguishable by output.
3. **Report honesty.** Until steps 1 and 2 land, cite R14 as "exit-level only; ancestry capability evidenced by unpinned co-evolved refinements without a red control." Do not edit `fixture-builder-v2.py`, which is frozen and pinned. Any `argv --rev` fix belongs in a v3 freeze with a correction note.
