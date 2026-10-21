# S063 — Python `json` documentation

- **URL:** https://docs.python.org/3/library/json.html
- **Access date:** 2026-10-21
- **Actual location:** Python 3.15.0 documentation, **Basic Usage**, note following the `json.dump` parameter descriptions (the note about `sort_keys`).
- **Verbatim quote (22 words):** “`sort_keys` sorts the keys before they are converted to strings, so numeric keys are sorted by value, not by their string representation.”
- **Source scope:** This documents CPython `json` API behavior. In particular, it documents sorting before string conversion and numeric-key sorting by value. It does not establish RFC 8785/JCS key ordering or ECMAScript number serialization, prove that a `json.dumps` call is JCS-equivalent, or verify which arguments a specific frozen invocation passed.
- **Disposition:** Reject as a JCS conformance gate. Admit only as a narrowly scoped tool-behavior / frozen-call-parameter citation (tier A, call-contract scope), as the existing S063 row proposes; the located quote supports the `sort_keys` behavior but not JCS equivalence. The disposition flips only if the claim is narrowed to that documented CPython behavior, not if the source is offered as proof of JCS conformance.
- **Existing row:** `corpus/SOURCES.md:69` (S063); no registry edit made.
