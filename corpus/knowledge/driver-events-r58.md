source: S550
verified-at: 2026-10-27
recheck: `python3 .ufo/waves/round-58/count-c2.py R`
coverage-map: Core — driver-liveness event-class parsing semantics; deepens existing FR5 surface, no frontier advance claimed

# Driver-liveness event classes are parsed log facts, not lane health verdicts

This entry adds implementation-level lexical and rest-parser constraints beyond the round-56 writer-grammar inventory and round-57 pairing interpretation. It describes the accepted tokens, per-event regular expressions, timestamp conversion, and sample bounds; it does not infer lane health, authoritative settlement, provider death, or exhaustive tracepoint coverage.

- **K1** — The outer event token is one of five lowercase strings, not an arbitrary label. Quote: `(launch|complete|lane-dead-no-report|launch-fail|wrap)` (tools/mori-driver-liveness.py:55).
- **K2** — The lane token permits ASCII letters, digits, underscore, and hyphen only; a dotted name is outside this lexical class. Quote: `([A-Za-z0-9_-]+)` (tools/mori-driver-liveness.py:55).
- **K3** — The outer grammar requires a numeric round token followed by a separate rest capture. Quote: `round=(\d+)(.*)$` (tools/mori-driver-liveness.py:55).
- **K4** — Timestamp conversion delegates to Python's fromisoformat parser and returns epoch seconds. Quote: `datetime.datetime.fromisoformat(tok).timestamp()` (tools/mori-driver-liveness.py:72).
- **K5** — In the pgid launch form, optional driver, slot, attempt, and mission fields appear in fixed order, not an unordered key/value bag. Quote: `pgid=(\d+)(?: driver=(\S+))?(?: slot=(\d+))?(?: attempt=(\d+))?(?: mission=(\S+))?` (tools/mori-driver-liveness.py:57).
- **K6** — Complete accepts only three suffix alternatives; attempt and advancing-round values must be numeric. Quote: `r"^; (?:hyaku-inline attempt=(\d+)|advancing to round=(\d+)|respawning)$"` (tools/mori-driver-liveness.py:59).
- **K7** — A dead-no-report suffix requires the exact retry-same-round wrapper and permits only optional parenthesized payload text. Quote: `r"^; retry same round(?: \((.*)\))?$"` (tools/mori-driver-liveness.py:60).
- **K8** — Wrap accepts only landed or complete, with an optional exact fleet-wrap suffix. Quote: `r"^ (?:landed|complete)(?:; NOT respawning \(fleet-wrap\))?$"` (tools/mori-driver-liveness.py:62).
- **K9** — The launch-fail capture accepts an empty reason, so a counted launch-fail does not guarantee nonempty diagnostic text. Quote: `r"^ :: (.*)$"` (tools/mori-driver-liveness.py:61).
- **K10** — The source constant sets the malformed-example sample cap to three. Quote: `MAX_MALFORMED_EXAMPLES = 3` (tools/mori-driver-liveness.py:63).
- **K11** — The malformed-example helper appends raw examples only while the sample count is below that cap. Quote: `if len(examples) < MAX_MALFORMED_EXAMPLES:` (tools/mori-driver-liveness.py:88).

These are log-shape parser facts only; the tool states that it emits no wellness or failure verdict and never remediates (`tools/mori-driver-liveness.py:8-10,31-36`). No event causality or authoritative settlement follows.
