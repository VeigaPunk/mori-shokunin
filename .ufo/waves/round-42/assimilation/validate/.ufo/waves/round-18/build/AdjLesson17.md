# C1 population adjudication — round-17 lesson

## Frozen hit and decision

The frozen C1 policy's adjudication rule is at `.ufo/waves/round-18/frozen/c1-policy.json:27-29`; the selected population record is from `.ufo/waves/round-18/frozen/c1-population.json`. There is one hit for `corpus/lessons/round-17.md`: line 241, class R6, SHA-256 `469c83039fa897c68dae0d9329873ce365e8f33c477841b3964731cac7b00948`.

Opened the specified requirement-commit context using the read-only command `git -C /home/vgpnk/Projects/shokunin/mori-shokunin show 29b0dc7:corpus/lessons/round-17.md | sed -n '238,244p'` (exit 0). The full 370-line lesson was then read. Its checked-out content matches the 29b0dc7 blob by SHA-256: `afc87fa66d138e6249df85339ebeec244974ad059a5b814e10f2027f299f77b3`.

**Decision: `allow-a`.** The hit is in a retrospective boundary statement that names restricted surfaces and states the narrow evidence boundary; it does not reproduce their contents or any private value. This fits frozen rule (a), not rule (c) (the lesson is an author file). No row for this hit is redacted, and no replacement/removal is prescribed for it by the frozen adjudication rule.

## Additional private context outside the frozen metric

The following are whole-file reading-sweep observations, not C1 population hits or adjustments to its count. Only line locations and kinds are recorded here; values and excerpts are omitted.

- `corpus/lessons/round-17.md:69,90-96` — host package-manager history and transaction-detail summaries; cross-session shell-log/UUID correlation and inferred actor attribution, including a session/document-themed label. These are summaries, not a verbatim other-session transcript excerpt.
- `corpus/lessons/round-17.md:74` — disclosure of a credential-record display/access event; no credential value is present in the lesson.
- `corpus/lessons/round-17.md:151-158` — live-session scan selectors, observation timestamp, and cohort/per-prefix outcome measurements; session-derived identifiers and data not matched by the frozen classes.
- `corpus/lessons/round-17.md:195` — provider-specific binding value in the OMP classification description; value omitted.
- `corpus/lessons/round-17.md:253-255` — cross-session package-event attribution and unresolved operator-scope context.
- `corpus/lessons/round-17.md:341-346` — provider/model answering labels and cohort counts, plus live directory-identifier redaction/retention history. Values and identifiers omitted.

These observations are outside the frozen regex metric and do not change the single-row adjudication above. No source files were changed.

## Population rows for this path

```json
[
  {
    "path": "corpus/lessons/round-17.md",
    "line": 241,
    "class": "R6",
    "line_sha256": "469c83039fa897c68dae0d9329873ce365e8f33c477841b3964731cac7b00948",
    "decision": "allow-a",
    "reason": "A boundary statement names restricted surfaces without reproducing their contents or private values; it satisfies frozen adjudication rule (a)."
  }
]
```
