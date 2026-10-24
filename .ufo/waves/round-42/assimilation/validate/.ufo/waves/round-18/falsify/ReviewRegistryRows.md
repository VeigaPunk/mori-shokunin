# Review: round-18 registry rows

**Recommendation:** not conformant as written; revise the C1/C2 entry recipes and pins before treating the rows as runnable. Axes checked: registry fields, CLI behavior, verdict mapping, frozen evidence, and write scope. No source changes made.

## Findings (severity order)

### High — C1's registered scan cannot produce the intended clean post-repair verdict

`SKILL.md:178` makes `--expect-population .ufo/waves/round-18/frozen/c1-population.json` part of the ordinary scan command. With that option, `mori-retention-gate.py:272-288` compares the complete current hit multiset against the frozen d005 population and returns exit 1 whenever it differs, irrespective of the unallowlisted-hit metric. The contract's after target is zero unallowlisted hits (`.ufo/waves/round-18/contract.md:24-29`), which requires the hit population to change as the routed files are redacted; the registered command therefore cannot return 0 for the intended result. The C1 row's code-1 explanation also omits `population_match=false`. The executor receipt records this path at `build/RetentionGate.md:22-24` (code 1 with population mismatch), rather than a clean after result.

Separate the d005 population-reproduction check from the measured after scan: keep `--expect-population` for the baseline check, but omit it from the ordinary after command (or make the two modes explicit). Update the code-1 description if population mismatch remains a normal failure.

The optional allowlist path named in this row, `corpus/evidence/retention-allowlist.json`, is absent from the current tree. Supplying it as written cannot work; omitting it leaves hits unallowlisted. This also leaves the stated C1 zero target unsupported by the current registry recipe (see `draft-verdicts.md:8`).

### High — C2 presents required revision overrides as optional

The r18 claims in `frozen/c2-register.json:30-41` have literal placeholder tips. `mori-freeze-order.py:200-214` returns `could-not-evaluate` for a placeholder tip without an override, and its row parser accepts repeated `--tip-for` overrides (`:568-593`). Yet `SKILL.md:179` places them in an optional bracket group. A run without an override for each of r18-C1, r18-C2, and r18-C3 returns code 2 instead of evaluating the current tree. The correction file is also bracketed optional even though the C2 after claim depends on the appended r17-C3 correction (`contract.md:31-37`; correction row exists in `corpus/evidence/freeze-register.json:4-12`). Make the required overrides explicit for a measured revision and include the corrections file in the command that is meant to reproduce the claimed after count.

The existing `build/FreezeOrder.md:25` self-test receipt is stale for the reviewed tool: its recorded SHA-256 differs from the current `tools/mori-freeze-order.py` hash returned by `sha256sum`. Consequently its 11/11 result and measured run do not verify the current bytes. No current-code self-test was run by this reviewer.

### Medium — C1's frozen-run mode is not the command shown, and its baseline pin is omitted

The C1 entry combines `scan ... [--frozen-run]` (`SKILL.md:178`), but the parser defines `--frozen-run` as a top-level mode, not a `scan` option, and `main` rejects a frozen-run invocation with a subcommand (`tools/mori-retention-gate.py:673-686, 689-714`). The frozen run must be a separate invocation. A successful standalone frozen run and a 19/19 self-test are recorded in `build/RetentionGate.md:26-36`; the current tool hash matches that report, and the snapshot digest check returned exit 0. Thus the operational two-evidence artifacts are present, but the registry entry does not expose a runnable frozen-run command.

The C1 pinned-values cell omits `.ufo/waves/round-18/gate-snapshots/retention/retention.json`, although that is the frozen-run input (`tools/mori-retention-gate.py:331-345`) and contains the expected verdict (`.../retention.json:21-34`). The snapshot directory currently contains only `retention.json`; the digest is embedded as `SNAPSHOT_PINS` in the tool (`:27-30`), not in the protocol-prescribed `expected.json`. This gives operational tamper detection, but does not meet PROTOCOL §Gate's literal `expected.json` pin requirement (`PROTOCOL.md:401-406`). List the snapshot in the registry and provide the required expected manifest, or explicitly resolve this format deviation with the protocol owner.

### Low — Entry and self-test cells are recipes, not self-contained commands

All three entry cells contain unresolved `<repo>` / `<REV>` placeholders (and C3 uses `PATH`), so none is directly runnable verbatim. C1 additionally has the invalid frozen-run placement above; C2 needs all three tip overrides. The C3 tool accepts one ledger path per invocation (`mori-dispatch-ledger.py:513-537`), while its pinned values name multiple wave ledgers; the row should say that the command must be run once per ledger if the intended metric is round-wide.

Each registered self-test command omits the required scratch environment. C1 requires `TMPDIR` to resolve to an existing repo-local `.scratch` (`mori-retention-gate.py:457-468`); C2 requires a non-system temp path inside the checkout (`mori-freeze-order.py:401-418`); C3 requires an existing real directory outside system temp roots (`mori-dispatch-ledger.py:413-426`). The write-scope notes mention `$TMPDIR` but do not make the runnable command/precondition explicit. Also qualify the `JSON stdout` scope text for C1 and C2: both self-tests print text rather than JSON (`mori-retention-gate.py:702-704`; `mori-freeze-order.py:564`).

## Fields and remaining risk

- All three rows have the required name, `gate` kind, verdict field, self-test spelling, pinned-value field, write-scope field, and `mori` owner (`SKILL.md:162,178-180`). The explicit process exit classes 0/1/2 are mapped in all rows, and source paths inspected expose no additional explicit gate return code. C1's code-1 *reason* list is incomplete as noted above.
- The write boundaries are otherwise truthful: normal scans use read-only Git object/history commands; the self-tests create isolated fixtures/commits under caller-provided scratch, not in the measured repo. The scratch path constraints and self-test output format need the clarifications above.
- No canonical-runtime, identity-rerouting, or saturation behavior is changed by these registry/gate files; no runtime was invoked. C3's round-wide tally remains a manual multi-ledger aggregation unless the invocation procedure says to run each ledger.

## Verification record and gaps

- Read the round-18 contract, frozen C1/C2/C3 inputs, L1 draft verdicts and out-of-metric triage, the three rows, gate source, and executor reports. No gate, self-test, build, lint, formatter, or runtime was run by this reviewer; executor-reported results are cited as reports, not re-executed observations.
- Read-only commands run: three lane `git diff-tree` inspections (each exit 0); `wc -l` over the three gate scripts (exit 0); `sha256sum` over the retention snapshot and the three current tools (each exit 0). Snapshot digest matched its in-tool pin; current retention and dispatch tool hashes match their receipts; current freeze-order hash does not match `build/FreezeOrder.md:25`.
- LSP was unavailable: `read xd://lsp` returned “No such tool”; no LSP status/references/definition/diagnostics could be obtained. One initial shell `grep -n` was used only to locate registry rows before discovering that unavailability; it is not semantic evidence. Conclusions above rest on direct source reads and the reported hash checks.
- No tools installed or updated; no VCS mutations; no URLs accessed.
