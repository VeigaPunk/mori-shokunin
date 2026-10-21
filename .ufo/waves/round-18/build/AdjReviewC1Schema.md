# C1 frozen population adjudication — schema review files

## Scope and evidence

Adjudicated only the frozen C1 rows for `.ufo/waves/round-17/build/ReviewC1Contract.md` and `.ufo/waves/round-17/build/ReviewSchemaDrift.md`, under `frozen/c1-policy.json`'s `adjudication_rule`. The population contains **3 rows total**: two class rows on line 13 of `ReviewC1Contract.md` (one unique line) and one on line 9 of `ReviewSchemaDrift.md`.

Read the specified base-commit context only: `git -C /home/vgpnk/Projects/shokunin/mori-shokunin show 29b0dc7:.ufo/waves/round-17/build/ReviewC1Contract.md | sed -n '12,14p'` (exit 0) and `git -C /home/vgpnk/Projects/shokunin/mori-shokunin show 29b0dc7:.ufo/waves/round-17/build/ReviewSchemaDrift.md | sed -n '8,10p'` (exit 0). The corresponding `jq '.hits[] | select(.path==...)'` population queries both exited 0. The two files were also read in full for the separate private-context sweep below. No matched text or source values are reproduced here.

No LSP device was available: `read xd://lsp` returned “No such tool.” No grep was used as semantic evidence. No builds, tests, or code changes were made; no tools were installed.

## Adjudications

| Path:line | Class | Decision | Basis and minimal redaction |
|---|---|---|---|
| `.ufo/waves/round-17/build/ReviewC1Contract.md:13` | R1 | **redact** | The line contains a concrete session identity and source-derived scan observations. It is not a surface-only instruction/contract, a permitted tool/fixture field-name occurrence, or a non-author file. Replace the entire line with a neutral marker such as `[redacted: source-specific observation removed]`. Preserve in this audit record the verdict, the two C1 hit rows on this one line, classes R1 and R2, and the original line SHA-256. Remove the session-store location/identity and all scan-derived field facts and distributions. |
| `.ufo/waves/round-17/build/ReviewC1Contract.md:13` | R2 | **redact** | Same line and hash as the R1 row; the path is a source-specific session-store reference, not an allowed surface-only mention, and the line also carries copied session observations. Use the same neutral replacement and preserve the same two-row/one-line provenance externally. |
| `.ufo/waves/round-17/build/ReviewSchemaDrift.md:9` | R2 | **redact** | Although the transcript filename is abstracted, the line associates a session-store location with a copied session-header value. It is not a contract/boundary naming only a surface. Replace the line with the same neutral marker; preserve externally the verdict, one C1 hit row, class R2, and original line SHA-256. Remove the source-derived header value and session-location reference. |

The redaction-marker text is not a substitute for the immutable C1 audit row: retain the row-level decision, hit counts, class identifiers, and original SHA-256 in the audit record. Do not retain the private-source values or the session-derived distribution counts as a replacement for them.

## Private context missed by the frozen regex classes

These observations are outside the frozen metric. The lines are cited without copying any private values:

- `.ufo/waves/round-17/build/ReviewC1Contract.md:9` — session-derived provider/model routing values and per-model/class distributions; the regexes do not capture these values.
- `.ufo/waves/round-17/build/ReviewC1Contract.md:13` — in addition to the matched path/identity, the line exposes session-scan field inventory and aggregate observation counts not covered by the matching classes.
- `.ufo/waves/round-17/build/ReviewC1Contract.md:15` — session-record error-status value and error-message tokens; R9's narrow field-name alternatives do not cover these values.
- `.ufo/waves/round-17/build/ReviewSchemaDrift.md:9` — session-header version value; R2 catches the location, but R9 does not cover that field/value.
- `.ufo/waves/round-17/build/ReviewSchemaDrift.md:13` — repeats the session-derived header-version fact, likewise outside the regex classes.

No other private document, configuration, shell-history, privileged-configuration, or operator routing-setting values were identified in the two files during the full-file read. These findings are a reading sweep, not additions to the frozen C1 count.

## Residual risk and verification gaps

This is an adjudication of the frozen population rows for the two assigned files, not a review of the later integration diff or a full-tree privacy certification. LSP caller/definition/diagnostic checks could not be performed because no LSP device was mounted. No runtime or automated checks were requested or run.

```json
[
  {
    "path": ".ufo/waves/round-17/build/ReviewC1Contract.md",
    "line": 13,
    "class": "R1",
    "line_sha256": "275cba91ef8c87c9772347107c662ed553aab1d345fd4c8733384782b6902c1b",
    "decision": "redact",
    "reason": "The line contains a concrete session identity and copied session-derived observations, so it does not meet any allow rule. Preserve only the audit verdict/counts/class/hash; redact the source-specific material."
  },
  {
    "path": ".ufo/waves/round-17/build/ReviewC1Contract.md",
    "line": 13,
    "class": "R2",
    "line_sha256": "275cba91ef8c87c9772347107c662ed553aab1d345fd4c8733384782b6902c1b",
    "decision": "redact",
    "reason": "The session-store reference is source-specific and the same line contains copied session observations; it is not an allowed surface-only mention. Preserve only the audit verdict/counts/class/hash."
  },
  {
    "path": ".ufo/waves/round-17/build/ReviewSchemaDrift.md",
    "line": 9,
    "class": "R2",
    "line_sha256": "13fd6b8fb4b3fc89df6f0bdca663b9082dff063c8d62d3a19fb944248496911d",
    "decision": "redact",
    "reason": "The session-store location is tied to a copied session-header value, so this is not a surface-only contract reference. Preserve only the audit verdict/counts/class/hash."
  }
]
```
