# C1 population adjudication — adjacent round-17 reports

## Axes and scope

Axes: reduce retention of copied private context while preserving audit provenance. This is a document-retention review of the two frozen C1 population rows, not a runtime/code change review; no runtime behavior or saturation claim is made.

Read the round-18 contract (`.ufo/waves/round-18/contract.md:24-30`) and frozen C1 policy (`.ufo/waves/round-18/frozen/c1-policy.json:17-29`), including its adjudication rule and explicit warning that the regex is only a recall floor. Also read the frozen C2 register and C3 ledger format named by the contract. The path-filtered C1 population results contained one R4 row for each requested path.

## Frozen-row decisions

Both hits are **redact**. Neither is merely a surface name or a lane field/key, and neither is a non-author path under the frozen policy's `non_author_paths_glob`. Each hit records a private-document location in authored report text; the surrounding passage also carries operator attribution. Retaining the path/value is not eligible for allow-a, allow-b, or allow-c.

| Path and line | Class | Decision | Reason |
|---|---|---|---|
| `.ufo/waves/round-17/build/OverlapTsukuroi.md:96` | R4 (`private_document`) | redact | Personal-document location embedded in an actor-attribution passage; not a boundary-only reference. |
| `.ufo/waves/round-17/build/PacmanTxnToday.md:119` | R4 (`private_document`) | redact | Personal-document location embedded in a passage attributing host activity and directory usage. |

Minimal replacement for each hit is a sanitized provenance record, preserving the frozen original hash and one-hit count, for example:

- `Redacted; verdict=redact; count=1; class=R4; line_sha256=9e0a71be8e562c0ebe64f376879b594b85339627d97f226d35679ca33e497d65.`
- `Redacted; verdict=redact; count=1; class=R4; line_sha256=76e720e340da8863f68bb23618f8e9449e3a8cd374d123c6d68b8bf460920b91.`

For the first hit, remove the personal location and the associated actor-attribution/session-note detail in `.ufo/waves/round-17/build/OverlapTsukuroi.md:95-97`; retain no copied location or note-derived intent. For the second, remove the personal location and the linked account/directory-attribution detail in `.ufo/waves/round-17/build/PacmanTxnToday.md:117-121`; retain no identifying or directory-breakdown values. A generic source pointer is sufficient if separately retained evidence has passed privacy review. Keep only the sanitized verdict/count/class/hash record above.

## Whole-file sweep: additional context outside the frozen metric

These are human-read findings beyond the frozen C1 regex count; they are not additional population rows. No private value or excerpt is reproduced here.

- `.ufo/waves/round-17/build/OverlapTsukuroi.md:34` — user-specific home cache/artifact location not covered by the `Documents`-specific R4 expression.
- `.ufo/waves/round-17/build/OverlapTsukuroi.md:95-97` — actor attribution and an operator-session-note-derived intent fact; the latter is not detected by the frozen session-identity, session-store, or tool-output-artifact classes. The R4 location at line 96 is the population hit above.
- `.ufo/waves/round-17/build/PacmanTxnToday.md:119-120` — account attribution and a per-directory working-location breakdown; the non-Documents home locations on line 120 and the account attribution are not caught by R4. The R4 location on line 119 is the population hit above.
- `.ufo/waves/round-17/build/OverlapTsukuroi.md:25-39, 82-100, 106-124, 128-149` and `.ufo/waves/round-17/build/PacmanTxnToday.md:12-24, 28-67, 71-88, 92-113, 122-132` — detailed host transaction, package/version, boot-chain, and post-event operational history. These details are outside the frozen regex metric; treat them as potentially sensitive host-context material, not as allowlisted merely because the scan did not match them.
- No OMP routing/model values, OMP configuration-line references, shell-history path, sudoers reference, timestamped OMP session identity, or numbered tool-output artifact was observed in these two full-file reads. The package-transaction history above is distinct from shell history.

## Evidence and verification record

- Read the frozen population rows using path-filtered JSON queries and applied the frozen policy rule (`c1-policy.json:27`). Read both requested report texts in full. The exact requested base-commit context commands returned exit 0:
  - `git -C /home/vgpnk/Projects/shokunin/mori-shokunin show 29b0dc7:.ufo/waves/round-17/build/OverlapTsukuroi.md | sed -n '93,99p'` — exit 0.
  - `git -C /home/vgpnk/Projects/shokunin/mori-shokunin show 29b0dc7:.ufo/waves/round-17/build/PacmanTxnToday.md | sed -n '116,122p'` — exit 0.
- No files other than this report were written; no tools were installed. No URL access. No caller/definition/diagnostics or runtime checks were applicable to these document-only population rows; canonical-runtime, same-identity rerouting, saturation, and resume-preflight behavior remain unassessed rather than inferred.

```json
[
  {
    "path": ".ufo/waves/round-17/build/OverlapTsukuroi.md",
    "line": 96,
    "class": "R4",
    "line_sha256": "9e0a71be8e562c0ebe64f376879b594b85339627d97f226d35679ca33e497d65",
    "decision": "redact",
    "reason": "A private-document location is copied into an authored actor-attribution passage; preserve only sanitized hit provenance and remove the linked identifying/session-note details."
  },
  {
    "path": ".ufo/waves/round-17/build/PacmanTxnToday.md",
    "line": 119,
    "class": "R4",
    "line_sha256": "76e720e340da8863f68bb23618f8e9449e3a8cd374d123c6d68b8bf460920b91",
    "decision": "redact",
    "reason": "A private-document location is copied into an authored activity-attribution passage; remove linked account and directory details while retaining only sanitized hit provenance."
  }
]
```
