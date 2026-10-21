# C1 population-hit adjudication — CriticC1

Axes: privacy minimization, provenance preservation, and fidelity to the frozen adjudication rule.

## Findings by severity

### High — redact both hits on line 50

The frozen population contains two hit rows for `.ufo/waves/round-17/build/CriticC1.md:50`: one `R1` and one `R2`. They share the same `line_sha256`, so this is two class hits on one line, not two distinct lines. Under the frozen policy, the line is not an instruction/boundary naming a surface, a lane field/key name, or a non-author file. It contains a concrete private session location/identity; therefore both rows are `redact`, not allowlisted.

Minimal replacement/provenance: replace the identifying source-location text with a neutral source-scope placeholder, retaining only any necessary aggregate corpus count. Preserve the adjudication record (redact verdict, one hit in each class, source path and line, and the original line SHA-256 below); compute and record a new digest for the replacement line when it is applied. Remove the complete concrete directory location and timestamped session identity. Do not retain session excerpts or a recoverable location. This is a report-only adjudication; no source file was changed.

### High — regex-missed session-derived context elsewhere in the file

The requested whole-file read found additional private context outside the frozen metric. These ranges contain summaries or observations derived from session records, including session outcomes, record-level event/error/resumption details, private seat/file identifiers, timestamps, provider/model identifiers, and counts. They are identified by kind only; no matched or private values are reproduced here.

- `.ufo/waves/round-17/build/CriticC1.md:3` — reviewer/seat provenance identifier and date; not matched by the frozen classes. [INFERENCE] The identifier is private seat metadata.
- `.ufo/waves/round-17/build/CriticC1.md:47-49,51` — transcript-field scope and processing provenance, plus corpus-size information; not direct transcript values, but source-derived scope/context outside the metric.
- `.ufo/waves/round-17/build/CriticC1.md:55-69` — historical session-outcome summaries, aggregate counts/distributions, provider/model pairings, and seat/root-file identities.
- `.ufo/waves/round-17/build/CriticC1.md:73-85` — event-level observations from other sessions, including session-file identity, time, record counts, error/resumption state, and additional seat/file identities.
- `.ufo/waves/round-17/build/CriticC1.md:89-93` — derived terminal/resumption classifications and aggregate counts from session records.
- `.ufo/waves/round-17/build/CriticC1.md:125-142` — measured session-derived classification results, counts, provider/model pairings, and error-signal details.
- `.ufo/waves/round-17/build/CriticC1.md:153-172` — incident-derived signal selection, session/seat outcomes, aggregate counts, and specific run observations.
- `.ufo/waves/round-17/build/CriticC1.md:186-199` — measured replay/double-scan outcomes, counts, and event/seat identity and timing details.

These are reading-sweep findings, not additional frozen C1 population rows. The file contains no other observed personal-document, shell-history, privileged-configuration, or operator-config values. The generic pseudocode and field names at lines 201-214 and the processing-limit statements at 228-233 do not disclose additional record values.

## Residual risk

The frozen policy explicitly treats its regex classes as a recall floor. Thus the two hits on line 50 do not measure the session-derived material above. A sanitized rewrite of the report should preserve only necessary anonymized conclusions and aggregate evidence, while removing record-level details, private model/provider identifiers, and session/seat/file identities. The `CriticC1.md` path is not one of the three `must_redact_paths`, but that does not make these copied private details allowlistable.

## Verification and scope

Read the round-18 contract and frozen C1-C3 inputs; selected the C1 rows with the requested `jq` filter; read line 50 with its immediate two-line context from the frozen base; read the whole report; and confirmed the worktree copy is byte-identical to the frozen-base copy by SHA-256. All checks were read-only. No tests/builds or tool installations were performed; none were needed for this adjudication. No external URLs were used.

Commands and outcomes:

- `jq '.hits[] | select(.path==".ufo/waves/round-17/build/CriticC1.md")' /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-18/frozen/c1-population.json` — exit 0; returned the two rows above.
- `git -C /home/vgpnk/Projects/shokunin/mori-shokunin show 29b0dc7:.ufo/waves/round-17/build/CriticC1.md | sed -n '49,51p'` — exit 0; read the matched line with surrounding context (not reproduced).
- `git -C /home/vgpnk/Projects/shokunin/mori-shokunin show 29b0dc7:.ufo/waves/round-17/build/CriticC1.md | sha256sum && sha256sum /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-17/build/CriticC1.md` — exit 0; the two whole-file digests were identical.

```json
[
  {
    "path": ".ufo/waves/round-17/build/CriticC1.md",
    "line": 50,
    "class": "R1",
    "line_sha256": "589f9d598e2700b141a9375ed176f53996440e5a593affad219f8d039c451914",
    "decision": "redact",
    "reason": "The line contains a concrete private session location and identity copied from a private source; it is not an allowed surface-only statement, lane field/key, or non-author file."
  },
  {
    "path": ".ufo/waves/round-17/build/CriticC1.md",
    "line": 50,
    "class": "R2",
    "line_sha256": "589f9d598e2700b141a9375ed176f53996440e5a593affad219f8d039c451914",
    "decision": "redact",
    "reason": "The line includes a path into the private session store rather than a surface name; remove the full location while retaining the original digest and adjudication metadata."
  }
]
```
