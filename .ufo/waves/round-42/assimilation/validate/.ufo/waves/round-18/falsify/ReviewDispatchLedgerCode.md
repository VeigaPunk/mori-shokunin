# Dispatch-ledger review at `e2bfbd6`

## Finding

### Medium — invalid nonterminal `result` values can be accepted in a clean ledger

The frozen row format limits `result` to `refused | started | partial` (`.ufo/waves/round-18/frozen/c3-ledger-format.json:14-19`). The verifier renders any other value as `null` at `tools/mori-dispatch-ledger.py:248-260`, but it does not add a finding for that value. Its started-row scan at `:279-296` only selects `started` and `partial`, and `clean` at `:313-338` depends on row binding plus the accumulated findings. [INFERENCE] A ledger with otherwise valid bindings, contiguous attempts/times, an invalid result on a nonterminal row, and one valid `started` row last can therefore be reported `clean`, despite violating the frozen result enum. This was not present in the four ledgers verified below and was not exercised with a synthetic fixture.

## Requested behavior checks

- **Payload recomputation uses the requested commit.** `_read_committed_json` reads `git cat-file blob <rev>:<path>` (`tools/mori-dispatch-ledger.py:102-114`). `_verify` loads the ledger through that helper at the given `rev` (`:200-204`) and loads each row's dispatch file through the same helper with that `rev` (`:226-233`). It recomputes identity from the parsed dispatch object (`:120-164`) and compares the digest, byte length, and task count (`:234-239`). This uses committed objects, not filesystem paths.
- **The ordinary-call wrapper is accepted.** `_payload_identity` searches nested objects for a `{context: string, tasks: list}` call and prefers the unique object whose last path key is `run` or `taskCall` (`:124-148`). At the requested revision, every row in the residual-drafting ledger bound successfully, which confirms acceptance of its `taskCall` wrapper in practice.
- **The ledger itself is also read at the requested revision.** The current worktree copy of `residual-drafting-attempts.json` read as seven rows (`.ufo/waves/round-18/residual-drafting-attempts.json:1-93`), while `verify --rev e2bf…` returned five committed rows. The measured result is therefore for the revision's ledger and dispatch content, not the current worktree copy.

## Verification results at `e2bfbd6f8dccc51fc06455efc41f720301112dd4`

| Ledger | Rows | Bound | Unbound | Ledger findings | Status / exit |
|---|---:|---:|---:|---|---|
| `.ufo/waves/round-18/wave1-attempts.json` | 1 | 1 | 0 | none | clean / 0 |
| `.ufo/waves/round-18/residual-drafting-attempts.json` | 5 | 5 | 0 | `STARTED_MISSING` | failed / 1 |
| `.ufo/waves/round-17/wave1-dispatch-attempts.json` | 5 | 0 | 5 | `ATTEMPTS_NONCONTIGUOUS`, `STARTED_MISSING`; five `LEGACY_ROW_UNBOUND` row findings | failed / 1 |
| `.ufo/waves/round-17/wave2-dispatch-attempts.json` | 4 | 0 | 4 | `ATTEMPTS_NONCONTIGUOUS`, `STARTED_MISSING`; four `LEGACY_ROW_UNBOUND` row findings | failed / 1 |

Thus the measured round-18 population is 6/6 bound, 0 unbound, with one ledger-level failure (`STARTED_MISSING` on the five refused residual rows). The round-17 legacy population is 0/9 bound and 9/9 unbound, as expected for legacy rows without payload digests. The C3 unbound-row count at this revision is 0; that does not mean the residual ledger is clean. The round-17 and round-18 populations differ, so this is not a same-population comparison.

The L1 draft's `5/5 bound` plus `STARTED_MISSING` statement matches the committed revision (`.ufo/waves/round-18/draft-verdicts.md:10`). The triage's seven-refusal count (`.ufo/waves/round-18/out-of-metric-triage.md:30`) matches the present worktree's seven rows, not the five-row ledger at `e2bf…`; [INFERENCE] the extra rows may be later worktree additions. Do not include them in the metric for `e2bf…` without a revision-scoped measurement.

## Commands and verification gaps

Read-only verify commands run (all against the same full revision):

```text
python3 /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-dispatch-ledger.py verify --repo /home/vgpnk/Projects/shokunin/mori-shokunin --rev e2bfbd6f8dccc51fc06455efc41f720301112dd4 --ledger .ufo/waves/round-18/wave1-attempts.json  # exit 0
python3 /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-dispatch-ledger.py verify --repo /home/vgpnk/Projects/shokunin/mori-shokunin --rev e2bfbd6f8dccc51fc06455efc41f720301112dd4 --ledger .ufo/waves/round-18/residual-drafting-attempts.json  # exit 1
python3 /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-dispatch-ledger.py verify --repo /home/vgpnk/Projects/shokunin/mori-shokunin --rev e2bfbd6f8dccc51fc06455efc41f720301112dd4 --ledger .ufo/waves/round-17/wave1-dispatch-attempts.json  # exit 1
python3 /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-dispatch-ledger.py verify --repo /home/vgpnk/Projects/shokunin/mori-shokunin --rev e2bfbd6f8dccc51fc06455efc41f720301112dd4 --ledger .ufo/waves/round-17/wave2-dispatch-attempts.json  # exit 1
```

The committed tool blob and the worktree source had the same SHA-256 (`4d8c7bf55b142569750f909ab3e9f7ef261d6d99672c55413027746c02c427b4`). The LSP device is unavailable in this session (`read xd://lsp` returned “No such tool”; no LSP status, references, definition, or diagnostics were possible). No grep fallback was used. No selftest or other non-requested execution was run.

The tool proves equality between the committed dispatch payload and the digest recorded in the committed ledger; per the frozen known limit (`.ufo/waves/round-18/frozen/c3-ledger-format.json:21`), that alone does not prove what bytes the external task tool received. The `STARTED_MISSING` finding records the committed result population, not independent evidence of the refusal cause or saturation event.