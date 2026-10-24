# R23 static falsification

## Finding

**The frozen R23 predicate is path-sensitive and can fail on a clean, red run; the shipped success branch does not expose matched line contents for the supplied fixture.** Confidence: high for both code-path observations. This is a finite-oracle counterexample, not evidence that the current branch leaks matched source-line text.

## Branch-level evidence

- `frozen/requirements-v2.json:25-27` includes R23 but contains no per-requirement wording. The effective correction says other requirement meanings remain, and `contract.md:19` defines R23 as no matched-text leakage.
- `oracle-reconcile-v2.py:30-46,60` invokes the tool on `valid`; R23 requires exit 0, `RETENTION_RECONCILED`, empty stderr, absence of both frozen canaries in `json.dumps(v)`, and `privacy_clearance is False`.
- `fixture-builder-v2.py:11,40-43,47-53` places the canaries in source-line contents; `fixture-builder-v2.py:107-108` records hit identities, not line contents.
- In the shipped `scan` branch (`tools/mori-retention-reconcile.py:138-152`), matching lines are reduced to path, line number, class, and SHA-256. The success result (`:219-228`) returns those hit identities and digest-only input provenance, not line strings; `privacy_clearance` is hard-coded false. Setup failures (`:272-275`) return fixed reason codes, not exception/input bytes. Thus on the fixture with a neutral path, the success branch withholds the matched lines and satisfies the literal marker predicate.
- **Smallest counterexample to R23 as an executable finite predicate:** choose an oracle output filename whose stem contains either frozen canary. The oracle derives `fixture_root` from `out.stem` (`oracle-reconcile-v2.py:19,28`); the resulting `--repo` argument is included in the command and then returned verbatim as `argv` (`oracle-reconcile-v2.py:33-38`; shipped source `:227-228`). R23 searches all of `v`, including that `argv` (`oracle-reconcile-v2.py:60`), so this otherwise-valid red invocation fails the canary test solely because the workspace path contains the string. No fixture-source change is needed. The output is path metadata, not matched line text; this is a false failure for the stated semantic requirement and makes the finite predicate depend on the caller's output path.

## Red control

There is **no missing same-command red control** in the supplied oracle: R02 (`oracle-reconcile-v2.py:48`) and R23 use the same `invoke('valid')` cache key. `invoke` caches the subprocess and parsed result (`:30-39`), and R02 asserts `raw_unallowlisted == 1`, `retention_state == 'red'`, and clearance false on that exact result. R23 does not repeat the red assertion locally, and the result rows do not carry a run identifier; an independent R23-only record would therefore lack that link. But in this oracle's actual control flow the R02 red check is same-command and same-result, not a distinct run.

## Limits

Static source inspection only; no execution, build, test, or formatter run. No LSP device was available in the mounted tools, so the references above are file/line inspection rather than semantic-LSP proof. The counterexample falsifies path-invariance of R23's literal canary check; it does not demonstrate a matched-line disclosure by the shipped recomputation branch.