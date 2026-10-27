# Mo57Reviewer20 — SOURCES registry review

## Axis / verdict

**C2 depth: source-grounded interpretation of `unclosed` pairing counts.** The registry has an admissible, newly opened source row that supports a meaningful but bounded claim about the log grammar: **S547**, opened 2026-10-27, identifies the writer-source shapes and specifically adds the `launch-fail` and `wrap` forms omitted by S544's earlier extract. It is appropriate provenance for interpreting which logged events can close a launch; it does not establish that an unclosed launch represents a currently running process.

## Evidence

- `corpus/SOURCES.md:327` (S547): corrected-anchor row specifies writer source, fleet revision `f564b1b5906a8a0e55d7e0acb7951915828c365b`, the v2 extract and SHA-256 `1ea4524c…`, status `mined`, opened `2026-10-27`, and use by `corpus/knowledge/driver-liveness-r56.md` and `tools/mori-driver-liveness.py`. It states explicitly that S544 omitted two of the five parsed event shapes and that S547 adds launch-fail and wrap anchors.
- `corpus/evidence/sources-r56/watchdog-log-grammar-v2.txt:7-11` is an opened source copy. It shows writer-form examples for launch-fail (line 7), launch (8), wrap (9), complete (10), and lane-dead-no-report (11). The copy is source material, not itself a formal proof of current process state.
- `corpus/knowledge/driver-liveness-r56.md:20-26` defines `unclosed` as launches without a same-round close and says fields are shape facts, not health verdicts. Lines 62-68 explicitly limit the interpretation to pairing facts over log lines, not a health verdict, and note that driver-authored log lines are not authenticated events.

## Counterexamples / limits

- The v2 extract contains only eleven writer-form examples (`watchdog-log-grammar-v2.txt:1-11`); it is not a live process table or a comprehensive transcript. Its examples support event-shape parsing, not whether a process still exists.
- The knowledge entry itself identifies out-of-grammar kimi-port `lane-round-failed` lines and says the probe reports those as `other_lines` (`driver-liveness-r56.md:69-75`). Thus an unclosed count is conditional on recognized same-round close shapes; it is not equivalent to a count of live workers or failed drivers.
- S544 (`SOURCES.md:324`) is insufficient alone as complete grammar provenance because it omits launch-fail and wrap; S547 explicitly supersedes that anchor gap. S547 nevertheless remains own-work writer-source evidence, not independent/authenticated execution evidence.

## Finding

No actionable registry defect found in scope: S547 is present, mined, opened this round, resolvable to the v2 source copy, and specifically supports the bounded grammar/pairing interpretation. The correct claim boundary is that `unclosed` is a pairing count, **not** a present-running count; neither S547 nor the extract licenses a process-liveness conclusion.

## Verification gaps

No LSP device/status was available in the mounted tools, so no semantic references/definition/diagnostics checks were performed. Registry/source assessment used the literal file evidence above. No production files or registry rows were changed; no tools installed.