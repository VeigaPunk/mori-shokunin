# MutAliasReturn — C1 alias-restoration mutation

## Result

**KILLED by the isolated frozen C21 source-byte guard.** Pristine and restored controls passed; the applicable one-fragment mutant was rejected. This is one mutation probe, not a full-driver, original26, or reconciler-output rerun.

Axes: mutation applicability; frozen-detector sensitivity with identical controls; source isolation and exact restoration.

## Pin and mutation

- Production base observed: `f3dc07c0bf423cc1947d0ffa91afa9ce236fbe3c`; expectation seal: `22772c10f6e3c1d8d3fe1b72083a6194e9f4e687`.
- Actual separate, shallow, no-local-hardlink clone: `/fast/scratch/hyaku/mori-r23/MutAliasReturn/repo`, branch `round23/MutAliasReturn`, observed HEAD equal to the production base. Only the named source/guard inputs were materialized; the lane index and refs were not changed.
- Mutated candidate: `/fast/scratch/hyaku/mori-r23/MutAliasReturn/repo/tools/mori-retention-reconcile.py`, line234.
- Smallest behavior-bearing change: reinsert the original **35-byte** producer fragment `'raw_unallowlisted':len(unallowed),` between `scanner_total` and `scanner_unallowlisted`. The original staged entering blob confirms that exact location. No schema, arithmetic, other producer, frozen rule, oracle or expected byte was edited.
- Mutant source archive: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/falsify/MutAliasReturn/mutant-source.py`.

## Expected detector and execution

Expected: reject a candidate with the removed alias producer restored while accepting the frozen transformed target.

Executed the **unchanged C21 predicate AST**, lines610–694, from `/fast/scratch/hyaku/mori-r23/MutAliasReturn/repo/.ufo/waves/round-23/build/MeasureDriver/measure-round23-v2.py`. The entire driver and source-delta document were checked against their sealed SHA256 identities; read-only Git observations confirmed identical driver/document bytes at the seal and production revision. The detector imports driver definitions but never calls its CLI or `Driver.run`.

The only input adapter supplies `git_mode` from actual stat modes of the staged entering file and temporary candidate, both100755; the original committed entering mode was independently observed as100755. The original byte transform, alias/literal counts, expected/observed hashes and frozen-document comparisons execute unchanged. Candidate bytes are provided directly rather than committed or executed. This measures the preregistered source constraint, not general semantic equivalence.

- Detector: `/fast/scratch/hyaku/mori-r23/MutAliasReturn/detect-source-guard.py`
- Detector SHA256: `9b70558c42c28c60a196df90482f8844d3c29c145f183951c69b42bbd4b4bf1d`
- Sealed driver SHA256: `5c12fdc056309966d3e716d25e3427a7908056595383f0353655b42282fdfbcd`
- Frozen source-delta SHA256: `df425412405c9358caec31c2fd7c6cc303d1f395b648a169b19c982bd3567318`
- Exact argv, environment, paths, versions and hashes: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/falsify/MutAliasReturn/argv-hashes.json`
- Raw bounded stdout/stderr, exits, elapsed times and restoration receipt: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/falsify/MutAliasReturn/bounded-result.json`

All three invocations used the same argv/interpreter and candidate path, sequentially, with384MiB address-space,15s wall-time and15s CPU limits. TMPDIR was `/fast/scratch/hyaku/mori-r23/MutAliasReturn`. No live quota reads, privileged operation, mount, process/session inspection, delegation, full-driver invocation or additional runtime was used.

## Actual output

| Bytes | Exit | C21 pass | Alias fragment count | v2 literal count | Frozen delta matches | Elapsed seconds |
|---|---:|---|---:|---:|---|---:|
| Pristine | 0 | true | 0 | 1 | true | 0.070966 |
| Mutated | 1 | false | 1 | 1 | true | 0.056113 |
| Restored | 0 | true | 0 | 1 | true | 0.047739 |

Every stderr was empty; no invocation timed out. The computed/frozen target remained `4599ee1aff95f21714e320a87fd31260f0435aa9c7a9884ac60ab952fe099a36` in every arm. The mutant's observed bytes differed from that target and contained exactly one alias producer; it was neither inapplicable nor a baseline-failure kill. No additional failure occurred in this scoped detector.

## Restoration evidence

| Identity | SHA256 |
|---|---|
| Authentic entering source | `0795bac9367c33e534b79599114c1635d83c4b0e4a57fbbe235644858a59de32` |
| Candidate before | `4599ee1aff95f21714e320a87fd31260f0435aa9c7a9884ac60ab952fe099a36` |
| Mutant / archived mutant | `e7248958afdf6899886416e89eae43fde4fad717a01394e3bb45e681b4b8af42` |
| Candidate after | `4599ee1aff95f21714e320a87fd31260f0435aa9c7a9884ac60ab952fe099a36` |
| Production before and after | `4599ee1aff95f21714e320a87fd31260f0435aa9c7a9884ac60ab952fe099a36` |

Restoration ran in a `finally` block, replacing the temporary candidate with exact pinned pristine bytes even if the detector failed. The restored invocation accepted those bytes, their hash matched the before hash, and mode remained100755. The intentionally preserved mutant archive is separate from the restored candidate. Production was never mutated.

Post-probe lane oracle hashes still match the frozen seal manifest:

- `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/oracle-rename.py`: `a55b2b50d3e7447a1d5312c8b066a13137a6a6895f0343b3240ebf081d97c5f2`
- `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/oracle-quota.py`: `f1f4a027728180436fc5161171b0f6ad4ca4176229b5240aabb33e3f2af36bec`

## Scope and retained boundaries

Read the contract, preseal amendment, frozen source-delta, original case-decision records, S077–S086 source decisions and lesson23. The stable receipt `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/evidence/measure4/summary.json` separately records original C1 pass25/26→26/26 and misleading_alias_runs8→0; those counters were **not rerun or redefined here**. This probe exercises supplementary C21 only and does not claim a new observed alias-output count.

C2 remains strictly UNPROVABLE at the existing29/30: frozen CaseEscapedSpace selected43/parent33 conflicts with shorter covering42. No exclusion, special case, relabel, frozen rewrite, quota-selftest execution or full-driver rerun was performed. The separately corrected co-evolved quota selftest is not this case.

Four inherited unallowlisted hits, original permission RED11/12, two unknown dispositions, blocked baseline acceptance and privacy_clearance=false remain unchanged. A source-guard kill is not clearance, health, closure, admission or promotion authority.

Tool installs/updates: none. Existing Git2.56.0 and Python3.14.8 were used.
