# Review — `corpus/knowledge/dispatch-ledger-r18.md` at `e2bfbd6`

Reviewed against `corpus/QUALITY.md`, `corpus/SOURCES.md`, the frozen C3 format, and committed round-18 evidence. Findings are scoped to the knowledge note and its claims/recheck instructions.

## Findings (severity order)

### High — The note overstates what the ledger binds

**Location:** `corpus/knowledge/dispatch-ledger-r18.md:7-12,29-32`.

The phrase “exactly what was sent” at lines 8-9 is contradicted by the note's own limitation at lines 29-32 and by the frozen rule. The frozen identity hashes a Python serialization of only `taskCall.context` and `taskCall.tasks` parsed from the committed dispatch JSON (`.ufo/waves/round-18/frozen/c3-ledger-format.json:4`); it is not a digest of the original dispatch-file bytes or the entire task-tool invocation. The committed critic further records that this projection does not observe the task-tool boundary, omits the `i` argument, and cannot detect an omitted refusal or an omitted ledger (`.ufo/waves/round-18/build/CriticC3Operability.md:15-19`). The RFC source note also distinguishes the parsed in-memory projection from the original file bytes (`.ufo/waves/round-18/build/SrcRfc8785.md:64`).

**Fix:** Replace “exactly what was sent” with a statement limited to row/self-consistency with the committed `{context, tasks}` projection. State explicitly that this is not proof of original dispatch-file bytes, all invocation arguments, actual task-tool receipt, or complete attempt inventory. Keep the existing task-tool and unlogged-attempt caveats, and add the omitted-`i`/projection limitation. Cite the frozen format and critic report at exact line ranges.

### Medium — The rules table omits verifier conditions and blurs recording requirements with enforced checks

**Location:** `corpus/knowledge/dispatch-ledger-r18.md:10-21`.

The “Bound when” cell at line 18 lists only digest and byte-length equality, but the frozen predicate and implementation also require `tasks_count` to match (`frozen/c3-ledger-format.json:19`; `tools/mori-dispatch-ledger.py:234-239`). The ledger-shape failure list omits an invalid/missing timestamp, which the implementation rejects as `AT_INVALID` (`tools/mori-dispatch-ledger.py:269-276`). Conversely, the introduction says rows complete with a result and exact refusal text (lines 10-12), but the verifier does not validate the `refused_text` semantics or require every non-started result to be `refused`; the critic flags this gap (`build/CriticC3Operability.md:18`; see verifier result handling at `tools/mori-dispatch-ledger.py:248-249,313-315`). A malformed refusal row can therefore be presented as if validated when it is not.

**Fix:** Add `tasks_count` equality and invalid/missing timestamps to the table. Label the table as the verifier's checked predicate, not the full record-schema requirement; explicitly identify `result`, `refused_text`, and returned-ID-set semantics that are recorded but not validated, or narrow the prose so it does not imply those fields are verified.

### Medium — The recheck command is not runnable literally and its scope is ambiguous

**Location:** `corpus/knowledge/dispatch-ledger-r18.md:3`.

`--rev <rev>` and `TMPDIR=<empty dir>` are shell syntax, not executable values as written: angle brackets are redirection operators, and the second placeholder also contains a space. The selftest requires `TMPDIR` to name an existing real directory and rejects paths beneath `/tmp` or `/var/tmp` (`tools/mori-dispatch-ledger.py:413-426`); the parser's accepted `verify` arguments are `--repo`, `--rev`, and `--ledger` (`:522-529`). Separately, the command checks only `wave1-attempts.json`. The lane also retains `residual-drafting-attempts.json` as C3 evidence (`out-of-metric-triage.md:30`; committed rows `[1-7]`), while the frozen metric describes round-level dispatch ledgers (`frozen/c3-ledger-format.json:20`). The note does not say whether this is a one-ledger example or a complete C3 recheck.

**Fix:** Give a syntactically valid invocation using a concrete revision (or define a shell-safe `REV` variable and quote `"$REV"`), state that it must run from the repository root, and provide an existing authorized scratch-directory value for `TMPDIR` without angle brackets or whitespace. Either add a separate verify invocation for every included ledger (including the residual-drafting receipt) or explicitly label this as a wave-1-only example and state what it does not recheck.

### Medium — Several evidence claims lack QUALITY-grade anchors

**Location:** `corpus/knowledge/dispatch-ledger-r18.md:29-35`.

The parenthetical `(round-18 CriticC3Operability)` at line 31 is not a path-and-line citation or evidence ID. Lines 33-35 state the different-population conclusion and “failure-capable selftests” without a measured anchor. These statements are supported by committed evidence—the critic's scoring guidance and population analysis (`.ufo/waves/round-18/build/CriticC3Operability.md:7-18,32`), and the executor's commands/selftest record (`.ufo/waves/round-18/build/DispatchLedger.md:19-22`)—but the knowledge note does not point readers to it. `corpus/QUALITY.md:3-5` requires a source anchor per claim and separation of observation, inference, and unknown.

**Fix:** Replace the shorthand with exact lane-relative path:line references. Cite the actual receipt for selftest execution and identify its tested arms; also say that the critic's call-boundary-divergence and omitted-refusal falsifiers were proposed but not run (`CriticC3Operability.md:21-28`). Cite the receipt(s) supporting the before/after population statement, and label it as a capability/schema contrast rather than a measured same-population improvement.

## Residual risk and non-findings

- The note correctly says the identity is **not** RFC 8785/JCS canonical (`corpus/knowledge/dispatch-ledger-r18.md:25-28`); RFC 8785 §3.1, §3.2.2.3, and §3.2.3 support the named duplicate-name, number, and key-order differences. It does not claim privacy proof or independent evidence. No finding on those examples.
- The remaining concern is the boundary between the narrow committed projection and actual invocation/receipt completeness. The frozen limitation is candid, but the opening wording and the omitted-argument limitation must be brought into agreement before the note can be relied on without qualification.
- S060 and S062 resolve to the registry entries (`corpus/SOURCES.md:66,68`) and committed opening notes (`.ufo/waves/round-18/build/SrcSlsaProvenance.md:5-43`; `SrcRfc8785.md:7-23,49-68`). I opened the cited SLSA page, in-toto ResourceDescriptor and DigestSet pages, RFC 8785, and the Python JSON documentation on 2026-10-21. The SLSA page identifies v1.2 as current while the URL is v1.0; this is disclosed in the source note and registry. The Python docs row S063 is rejected in `SOURCES.md`; I do not rely on it as a JCS-conformance source.

## Verification and gaps

- Confirmed committed target, QUALITY, and SOURCES content with `git show` at `e2bfbd6f8dccc51fc06455efc41f720301112dd4` (each exit 0). `git ls-tree -r --name-only ... -- .ufo/waves/round-18` exited 0. A `git grep` invocation exited 0 and was used only to locate exact report paths; its output is not semantic evidence.
- One attempted listing command had an accidental trailing pipe and exited 2 at shell/tool parsing; it produced no evidence and changed nothing.
- I did **not** run `mori-dispatch-ledger.py verify`, `--selftest`, or any build, lint, test, or formatter. The command's runnability was assessed statically against its parser/selftest requirements and the committed receipts. No tool was installed or updated; no VCS mutation was performed.
- No LSP device/status route is exposed in the mounted tools for this document-only review; no references/definition/diagnostics request was available. No grep output was used as semantic proof.