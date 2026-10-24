# D4 — earlyoom entry correction findings

## Behavior and finding

- The case-insensitive `grep` for `version` in `corpus/knowledge/earlyoom-invocation-scope-r30.md` and the follow-up search for “reports … version” isolate the unconditional reader-output claim to the Round-30 C2.1 sentence at lines 53–54. Other body mentions describe the startup version line, invocation boundaries, or shapes; they do not make that unconditional output claim (`corpus/knowledge/earlyoom-invocation-scope-r30.md:21-22,41-42,64-65,84,103,120`).
- The Round-30 wave-2 finding calls out this exact conditional: the reader reports a version only if a version line is at or after the retained stamp; it records a pre-stamp example with `version: null` and equal/post-stamp examples with a version (`.ufo/waves/round-30/w2/ReviewEntryProse.md:27-43`). The Round-30 lesson records the finding verbatim as “reports its version” holding only for a version line at or after the retained stamp (`corpus/lessons/round-30.md:231-232`).
- Static inspection of `tools/mori-oom-killers.py` confirms the condition: the retained nonzero stamp filters records inclusively (`stamp >= aetm`, lines 305–322); `version` starts as `None` (line 360) and is set only while iterating scoped version lines (lines 389–396); the result exposes it as `earlyoom.version` (line 518). Thus if the retained scope has no version line, the output remains null; if it has multiple version lines, the last parsed one is returned (`tools/mori-oom-killers.py:305-322,360,389-396,518`).
- The review's scratch observations are reported evidence, not a run performed for this report (`.ufo/waves/round-30/w2/ReviewEntryProse.md:34-39`). I did not rerun them or run tests.
- QUALITY 77 requires corrected wording at every statement site and removal of superseded wording; an appendix alone does not close it (`corpus/QUALITY.md:349-355`). The original C2.1 sentence at entry lines 52–55 therefore needs an in-place correction as well as any requested appended note. The cited Restart sentence at lines 23–25 should also be corrected in place to carry the source split below (`corpus/knowledge/earlyoom-invocation-scope-r30.md:23-25`).

## Restart=always source split

- The entry currently cites S159 alone for the killed/crashed restart claim (`corpus/knowledge/earlyoom-invocation-scope-r30.md:23-25`). The Round-30 lesson records ReviewEntryProse LOW-1 that S120 also carries `Restart=always` (`corpus/lessons/round-30.md:231-232`).
- S159 is the commit that introduced `Restart=always` and carries the adjacent comment/commit rationale; its SOURCES scope explicitly excludes the v1.9.0 file bytes (`corpus/SOURCES.md:165`). S120 is the upstream `earlyoom.service.in` file at v1.9.0 and records `Restart=always` at line 17 (`corpus/SOURCES.md:126`). The startup version line is separately sourced to S119 `main.c:161` in the entry (`corpus/knowledge/earlyoom-invocation-scope-r30.md:21`).

## Paste-ready draft

The following is the requested appended text. To satisfy QUALITY 77, also replace the active body statements at entry lines 23–25 and 52–55 with their corrected wording in the same integration; do not leave the old assertions standing as active prose (`corpus/QUALITY.md:349-355`).

````markdown
## Round-31 correction (D4)

### Facts §3, C2.1 — version reporting is conditional

Old entry text, line 52: “- Round-30 change (C2.1, the round-29 Judge11–13 `tool error` rulings): for a non-active unit with a readable show text”
Old entry text, line 53: “  and a retained non-zero stamp (S157), the reader scopes the last invocation from that stamp, reports its version and”
Old entry text, line 54: “  its zero line counters, keeps `actions: null`, and treats a send inside that last invocation as positive evidence too”
Old entry text, line 55: “  (`.ufo/waves/round-30/evidence/fix-tool.diff`; differential `.ufo/waves/round-30/evidence/c2-differential.txt`).”

Corrected version statement for the entry body: For a non-active unit with readable show text and a retained non-zero stamp, the reader scopes the last invocation from that stamp and reports the latest version line in that retained scope only if one exists; if no version line is at or after the stamp, `earlyoom.version` is `null` (`tools/mori-oom-killers.py:305-322,360,389-396,518`; `.ufo/waves/round-30/w2/ReviewEntryProse.md:27-43`). This D4 statement corrects version availability only; it does not independently reassess the other C2.1 clauses.

### Facts §1 — S159/S120 Restart=always overlap

Old entry text, line 23: “- The shipped unit restarts earlyoom whenever it is killed or crashes (S159: \"Have systemd restart us should we get”
Old entry text, line 24: “  killed or crash for some reason\", `Restart=always`), so one boot can hold several invocations, and a restart writes a”
Old entry text, line 25: “  new version line: \"send, restart\" and \"send, no restart\" are different shapes.”

Source split and corrected statement for the entry body: S159 is the commit that introduced `Restart=always` into earlyoom's unit template and carries the killed-or-crash restart rationale. S120 is the upstream `earlyoom.service.in` file at v1.9.0 and records `Restart=always` at line 17. With the startup version line at S119 `main.c:161`, a restarted earlyoom process begins another invocation and prints a new version line; “send, restart” and “send, no restart” are different shapes (`corpus/SOURCES.md:126,165`; `corpus/knowledge/earlyoom-invocation-scope-r30.md:21`).
````

## Gates, surfaces, and limits

- Gates reviewed: the version condition against the current tool source and the correction rule in QUALITY 77. No self-test, build, fixture, runtime probe, or source download was run; the draft's code citations are static-source evidence, not execution evidence (`tools/mori-oom-killers.py:305-322,360,389-396,518`; `corpus/QUALITY.md:349-355`).
- Read-only surfaces: the entry, Round-30 wave-2 finding, Round-30 lesson, QUALITY, tool source, and SOURCES rows cited above. Product files were not edited. No tools were installed or updated.
- Out of scope: changing the entry or SOURCES registry, validating the review's scratch probes, host state, and any test execution.
- Artifact written: `.ufo/waves/round-31/w1/FixEntryVersionD4.md`.
