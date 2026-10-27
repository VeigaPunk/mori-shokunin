# Mo58Reviewer22 — C2 source grounding

## Finding — low severity: K3 and K4 are overclaimed by their located quotes

Reviewed `tools/mori-driver-liveness.py` at frozen revision `fe8801120a67c1a6b8899d7d0423839caa09e7d0` against the eight current located statements in `corpus/knowledge/driver-events-r58.md`.

- K3 claims both that launch uses `LAUNCH_REST_RE` and that rejected suffixes go through the malformed path, but quotes only `m2 = LAUNCH_REST_RE.match(rest)` at line 123. The latter inference is evidenced by the subsequent `if not m2: _bad(raw); continue` at lines 124–126, not by the cited quote itself.
- K4 claims completion uses `COMPLETE_REST_RE` and additionally contrasts attempt keys with a generic suffix parser, but quotes only the match at line 135. The source-specific distinction is at lines 136–139 (attempt-key extraction and malformed rejection) and the named grammar at line 21.

The described behavior is present in the source, so this is a located-evidence/quote sufficiency defect, not a falsified event-class behavior. K1, K2, K5–K8 statements and their line-numbered quotations match the frozen source on inspection. No other counterexample found within the eight claims.

## Bounded method / gaps

Read frozen contract and frozen C1/C2 counters; inspected the complete frozen target source with `git show <freeze>:tools/mori-driver-liveness.py` and compared each K1–K8 quote and claim against it. The `lsp` device was not mounted (`xd://lsp` returned “No such tool”), so no semantic LSP references/definition/diagnostics were available; this is direct source inspection, not semantic tooling evidence. Disk-guard status returned running (exit 0). No production files changed.
