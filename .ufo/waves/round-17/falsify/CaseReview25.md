# C1 case review — CaseReview25

**Verdict: specific falsifiers in both targeted regression oracles.** The retained after-run observations match every declared `want` assertion, and the fixture bytes/expectations are source-supported; however, those green results do not establish retry metadata or the required main-session count. These are gate/oracle coverage gaps, not evidence that the current tool output is wrong.

## Scope and evidence

Axes attacked: C1 coverage, oracle sensitivity, input/expectation independence, and retained-case consistency. `git -C /home/vgpnk/Projects/shokunin/mori-shokunin diff --unified=2 24526ea9617cd020fee16c28fe4d4a2789dc28cb -- tools/mori-seat-terminal.py tools/mori-round17-seat-regressions.py .ufo/waves/round-17/fixtures/seat/expected.json` completed successfully (rc 0): these three target files are additions from the entering tip.

The LSP device is unavailable here: `read xd://lsp` returned “No such tool” and listed mounted tools without LSP. Literal grep was used only to locate case identifiers; findings below are grounded in the cited source and contract reads.

The fixture hashes match the pins in `fixtures/seat/expected.json:25-26,67` (and the expected-table digest matches `PINNED_INPUTS.json:13`): `RetrySingle/retry-one.jsonl` `e9a4436e…d276d49`; main-session fixture `187e2d13…d1f69`; nested control `76e28a1b…b722`; `expected.json` `b684c63b…7cb01f`. The complete `sha256sum` command returned rc 0.

- `RetrySingle/retry-one.jsonl:1-2` is synthetic schema-v3 input; its terminal error is at 1760998000000, has `errorStatus:429`, `(type=1302)`, and the singular text `after 1 retry`. The case pins `--now-ms 1761000000000`, so the error is 2,000 seconds old, beyond the default 900-second settle window. Contract A1 says old errors past that window are dead (`contract.md:113`), type 1302 means rate limit (`contract.md:123`), and the singular/plural retry pattern is specified at `contract.md:118`. Thus the declared `dead_rate_limit` result is supported independently by the contract; the fixture is hash-pinned.
- `MainSessionExclusion/2026-10-20T15-00-00Z_0123abcd.jsonl:1-2` is a direct child whose stem matches the main-session pattern and contains an aged 429 rate-limit error. `MainSessionExclusion/nested-ok.jsonl:1-2` is a nested completed control. Contract A1 explicitly makes only matching direct children `kind: main`, excludes them from totals, and counts them in `main_sessions` (`contract.md:114`). The expected completed=1/dead=0/rc=0 is therefore supported: the nested seat must count, while counting the direct main transcript as an ordinary seat would produce a dead result.

The `want` entries are explicit and separate from tool output (`expected.json:1311-1332,1335-1357`); no circular output-derived expectation was observed. Retained L1 evidence is in `evidence/seat-before/run-manifest.json:1` and `evidence/seat-after/run-manifest.json:1` (case objects selected by their `id`). Both before cases are `capability_absent`, `ok:false`; both after cases are `match`, `ok:true`, with empty reasons. Retry after-observation: rc=1, `MORI_SEAT_TERMINAL_DEAD`, one `dead_rate_limit`, `now_ms=1761000000000`. Main after-observation: rc=0, `MORI_SEAT_TERMINAL_OK`, files_scanned=2, seat_count=2, main_sessions=1, `now_ms=1761000000000`, and one counted `completed` with no dead totals. These match the fields present in each `want`.

Read-only count rerun (jq rc 0):

```sh
jq -s 'map([.cases[] | select(.id == "retry_after_1_retry" or .id == "main_session_excluded_from_totals")]) | map({count: length, cases: map({id, status, ok})})' \
  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-17/evidence/seat-before/run-manifest.json \
  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-17/evidence/seat-after/run-manifest.json
```

Output:

```json
[
  {"count":2,"cases":[{"id":"retry_after_1_retry","status":"capability_absent","ok":false},{"id":"main_session_excluded_from_totals","status":"capability_absent","ok":false}]},
  {"count":2,"cases":[{"id":"retry_after_1_retry","status":"match","ok":true},{"id":"main_session_excluded_from_totals","status":"match","ok":true}]}
]
```

No tool or selftest was run. The cases have valid pinned packs and pin `--now-ms`; their expected rc values are 1 and 0, respectively. The before-side `capability_absent` outcomes are recorded as failures, not accepted setup/clean outcomes. Both expected totals declare all eight classes, and the real nested completed control makes the main-exclusion totals non-vacuous. Neither case is a setup-path test.

## Findings (severity order)

### P2 — `retry_after_1_retry` does not assert either retry-specific output

`fixtures/seat/expected.json:1311-1332` expects only rc, finding, class totals, and `retry-one: dead_rate_limit`; it has no expected `retries: 1` or `retry_exhausted: true`. The tool's parser does implement the singular form (`tools/mori-seat-terminal.py:89-93,222-243`), but the gate cannot pin those fields: `WANT_KEYS` admits only rc/finding/totals/seats (`tools/mori-round17-seat-regressions.py:214-216`), and `compare_want` compares totals and seat classes only (`:1215-1259`). Gate checks at `:1394-1412` merely require a permitted retry flag type and consistency between the aggregate and per-seat flags; `retries` may be null (`:1061-1063`).

**Static per-case counterexample [INFERENCE]:** remove the singular alternative from `_RETRIES_RE`, or stop setting `retry_exhausted`, while keeping error classification unchanged. This fixture still yields the wanted dead-rate-limit class and totals; null retries and a false per-seat flag with aggregate 0 satisfy the gate's type/consistency checks. The case remains green while both retry-specific behaviors required by A1 (`contract.md:118`, original per-seat output contract `:60-63`) are broken. The retained `observed` summary does not include these fields, so its `match` cannot close this gap.

### P2 — `main_session_excluded_from_totals` does not require `main_sessions`

`fixtures/seat/expected.json:1335-1357` asserts the nested completed seat and totals but has no `main_sessions` expectation. The gate's `WANT_KEYS` also cannot express it (`tools/mori-round17-seat-regressions.py:214-216`); its strict required output tuple omits `main_sessions` (`:1364-1371`), and it validates the count only when the field is present (`:1355-1358,1437-1439`). This falls short of A1's explicit requirement to count direct main sessions in that output field (`contract.md:114,119`).

**Static per-case counterexample [INFERENCE]:** preserve the main row as `kind: main`, preserve the exclusion from totals and the nested seat's completed result, but omit top-level `main_sessions`. The expected totals/finding/seats still match; the gate does not reject the missing field. The current after manifest records `main_sessions:1`, but does not show the gate asserting that value against an oracle. The real negative control does prove exclusion from totals; it does not prove the required count field is emitted.

## Residual risk / verification gaps

The current after-run observations support the explicit rc/finding/totals/seat-class assertions; these findings are about what those assertions fail to falsify. No live probes, executable, or selftests were run. No other class or setup false-green was found within these two cases; this review does not establish completeness of other C1 cases or the entire gate.

Report: .ufo/waves/round-17/falsify/CaseReview25.md
