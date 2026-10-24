# ProvenanceCapture — r15 revision-scope provenance + r14 migration pin

Seat: `MoriR15.ProvenanceCapture` (executor, leaf). Date 2026-10-20.
Axes: provenance fidelity, moving-input detection, zero behavioral drift, safe paths-only capture.

## Scope and authorization

- Primary: `tools/mori-round14-regressions.py` (r14 outside dirty-scope debt).
- L1-authorized extension: `tools/mori-round13-regressions.py` `record_revision` metadata, because the routed `dirty=true` debt originated there.
- No other production file, runner, gate, fixture, verifier, MANIFEST or sibling report was edited. No commits. No verification/build/test/formatter ran (parent owns the post-integration gate).

## Files changed

| File | Change |
|---|---|
| `tools/mori-round14-regressions.py` | exact start/end revision scope, canonical per-facet change evidence, load/end content hashes, harness start/end digest; one L1-authorized expectation migration (below). |
| `tools/mori-round13-regressions.py` | `record_revision` widened minimally: exact porcelain + parsed status paths + parsed entries, real observed HEAD separate from the asserted pin, sanitized git env, start/end scope and driving-script hash. Historical `(head, dirty)` contract preserved. |
| `.ufo/waves/round-15/build/ProvenanceCapture.md` | this report. |

## Behavior

r14 gate behavior is unchanged except the exact L1-authorized semantic migration:

- `R14_SEC_DUP_MSGID_MIXED` (`tools/mori-round14-regressions.py:1776`) now expects the r15 partial-positive outcome: `rc=1`, `DRIFT`, `drift=1`, exactly one `OOM_KILL_JOURNAL crit`, raw `kernel_oom_notice=unavailable:record-invalid` retained, `positive_kernel_oom=1`, `positive_unit_oom=0`, unit counters valid zero (`user_unit_oom=0`, `user_unit_oom_result_unknown=0`), no `count=` total. `FORBID_OOM` was removed for this case only; `OUT_ID` forbids and retired-prefix forbids stay. On the pinned frozen census it remains red (historical residual control), so r14 still shows the old suppression as red-before, not a no-harm waiver.
- Every other r14 case, expectation, exit code (0/1/2), CLI flag, query count, fixture, stdout grammar and `FROZEN_RED_REQUIRED` list is untouched. Aggregate-unavailability checks for foreign-boot, multi-boot, wrong-class, whole-stream-malformed, stderr, rc and timeout cases remain exactly as before; none of those fixtures contains a valid current-boot positive, so none migrates.
- r13 verdicts, exit map, claims, CLI and frozen pins are untouched. `record_revision()` still raises `SetupError` when no revision exists and still honors `MORI_EVIDENCE_DIRTY` for the boolean.

## Retained evidence

r14 `evidence.json` (additive keys only):

- `harness`: `sha256` (end), `executed_sha256` (import-time digest of the bytes Python loaded), `start_sha256` (same import boundary), `end_sha256`, `changed`.
- `revision.asserted_revision`: `MORI_EVIDENCE_REVISION` if set, annotation only; never compared.
- `revision.start` / `revision.end`: real `git rev-parse HEAD` plus the exact `git status --porcelain --untracked-files=all` lines (status codes and paths only, no bytes), parsed state, entries, `dirty`, capture timestamp.
- `revision.inputs.<target>`: source path, `start_sha256` (digest used at load), `end_sha256` (re-hash after last run), `changed`, `end_state`.
- Per-facet change fields: `head_changed` (real HEAD), `status_changed` (porcelain minus harness-written paths), `inputs_changed`, `harness_changed`, `porcelain_added`/`porcelain_removed` (paths only), `dirty_excluding_harness_output.start/end`, `output_scope.excluded_prefixes` and `excluded_entries`, and `not_measured`.
- No universal `moving:false`: status equality cannot prove stationary bytes, so each facet is reported separately and null when unmeasurable. `status_changed=false` means only that the porcelain text is equal; `not_measured` names the content gap.
- The start driver digest is captured at module import (`HARNESS_SHA_IMPORT`), not in `prepare()`, so an edit landing after import but before arg parsing is still detected as `harness_changed=true`; the end digest is taken after the last run, before evidence is written. r13 applies the same import-time start digest to its driving script.

r13 `evidence.json` (and setup/tamper evidence): `revision.head`/`dirty`/`source` preserved, plus `dirty_source` (`env:MORI_EVIDENCE_DIRTY` or `porcelain`), `dirty_captured` (the observed porcelain boolean), `asserted_revision`, `observed_head`, `start`/`end` (exact porcelain, parsed `paths`, dirty), `head_changed`, `status_changed`, `dirty_excluding_harness_output`, `output_scope`, `not_measured`, and a `harness` block with `executed_sha256`, start/end SHA-256 and `changed`.

Exclusion is tight, never the whole `--output` tree: only `runs/`, `wrappers/`, `mutants/`, `targets/`, `evidence.json`, `evidence.json.tmp` and the random fixture root. A candidate is dropped if any resolved census, oracle, frozen, shonen or target path lives at or below it, so an input placed under `--output` is still compared. Git probing uses `GIT_OPTIONAL_LOCKS=0`, `core.fsmonitor=false`, `--no-optional-locks`, and `GIT_CONFIG_GLOBAL/SYSTEM=/dev/null`; no index or fsmonitor state is written or consulted.

## Historical reconstruction impossibility

A historical r13 receipt that carries only `dirty=true` cannot be expanded into paths: the boolean was never accompanied by the porcelain lines, the worktree state of that run is gone, and re-running the gate now measures today's tree. The new scope is therefore prospective only. The same applies to any r14 receipt produced before this change, which had no revision block at all. No claim is made that past receipts can be repaired or re-attributed.

## Note on the routed "imported r13 repo_revision" claim

Inspected: r13's `record_revision` is a `Harness` staticmethod, not an imported helper, and `tools/mori-round14-regressions.py` imports nothing from r13 (it is deliberately self-contained). r14 had no revision metadata of any kind. The r13 helper itself retained only `dirty` (bool); it now retains the exact scope as authorized.

## Risks / open points

- No execution here by lane rule; the parent must run the two gates once after integration.
- `CensusPositive` had landed the r15 positive-token contract as comments only at read time; it has since confirmed (peer message, static inspection, not executed) that the migrated fixture shape matches: one crit OOM/DRIFT, `SURFACE journal.user` carries bare `positive_kernel_oom=1`/`positive_unit_oom=0` (plus zero signal/process positives), and the alarm line uses scope-prefixed integer fields `user_positive_kernel_oom=1`, `user_positive_unit_oom=0` (also `system_positive_*`), with no combined value and no duplicate bare key. The r14 case pins the surface literals and the crit/DRIFT outcome; it deliberately does not assert the alarm positive-field syntax, which `HarnessBuild` owns.
- r13's historical `revision.head` may remain the asserted pin; `observed_head` and the start/end scope always carry real `git rev-parse HEAD`. Consumers that compare `head` to a worktree revision should use `observed_head`.
- `MORI_EVIDENCE_DIRTY` still overrides the historical r13 `dirty` boolean (behavior preserved, not silently changed); `dirty_source` names the assertion and `dirty_captured` retains what porcelain actually showed, so the override is visible rather than laundered. CE7 is closed as a label, not as a changed contract.
- Evidence consumers see additive keys only; `harness.sha256` still means the end-state digest, as before.
- `r13` and `r14` hash their own script at import and end, and r14 hashes resolved targets at load and end; files are small and read once per boundary, not per case.

## Tooling

No install or upgrade was performed.
