# C1 population-hit adjudication: ConformanceAudit.md

## Scope and basis

Adjudicated the frozen population rows for `.ufo/waves/round-17/falsify/ConformanceAudit.md` at base `d005cdde0e009dea6c0cc29b37163de536528658`. The controlling policy is `.ufo/waves/round-18/frozen/c1-policy.json` (adjudication rule at line 27; non-author path globs at lines 23–25); the population is `.ufo/waves/round-18/frozen/c1-population.json` (commit and totals at lines 3–10). The report file was read in full; each hit line was separately opened at `29b0dc7` with up to two adjacent lines for context. No matched text is reproduced here.

There are eight population rows on five source lines: line 43 (one), line 44 (two classes), line 46 (three classes), line 74 (one), and line 75 (one). All eight are **redact**. None qualifies for allow-a, allow-b, or allow-c: these are historical audit-report statements, not merely instruction/boundary/contract surface names; the matches are not field/key names occurring in lane tool code, a contract, or a synthetic fixture; and this path is not in the frozen non-author globs. It is also not one of the three must-redact paths, but that does not create an allowlist category.

## Row decisions and minimal provenance-preserving replacement

For every redacted row, the minimal replacement is a neutral private-context finding marker that retains the original audit verdict/status, a count of one for that class occurrence, the class ID, and the original line SHA-256 as a **pre-redaction** digest. Remove the identified private content and any supporting detail that would reproduce it. The SHA-256 is provenance for the original line, not a digest of replacement text. This is replacement guidance only; no source file was edited.

- `ConformanceAudit.md:43`, R9 — **redact**. Remove the session-record field/value disclosure and supporting examples; retain only finding metadata and the provenance fields above.
- `ConformanceAudit.md:44`, R7 — **redact**. Remove the operator-configuration file reference and its line-range detail; retain only finding metadata and provenance.
- `ConformanceAudit.md:44`, R9 — **redact**. Remove the private record-field references and the report of their contents; retain only finding metadata and provenance.
- `ConformanceAudit.md:46`, R3 — **redact**. Remove numbered session tool-output artifact identifiers and associated artifact-location detail; retain only finding metadata and provenance.
- `ConformanceAudit.md:46`, R5 — **redact**. Remove the shell-history file reference and any history-specific detail; retain only finding metadata and provenance.
- `ConformanceAudit.md:46`, R6 — **redact**. Remove privileged-configuration path/reference detail; retain only finding metadata and provenance.
- `ConformanceAudit.md:74`, R9 — **redact**. Remove the session-record field/value report and examples; retain the audit finding result, count, class, and original digest only.
- `ConformanceAudit.md:75`, R9 — **redact**. Remove the private retry/model-record field references and value-reporting detail; retain the audit finding result, count, class, and original digest only.

## Additional private context not represented by the frozen regex metric

These are reading-sweep observations, not additional C1 hits or metric adjustments. They are cited by lane path and line only; no private values or excerpts are repeated.

- `.ufo/waves/round-17/falsify/ConformanceAudit.md:39` — partial other-session identity containing a personal-document-derived label, plus a session-to-host-event attribution/correlation using an invocation identifier. R1 and R4 do not match this form. The same line also reports host package-operation chronology and actor attribution. This is not an OMP transcript excerpt, but it is private session/host correlation context.
- `.ufo/waves/round-17/falsify/ConformanceAudit.md:46` — login-history (`wtmp`) access is mentioned in addition to the R3/R5/R6 hits. The line reports access, not login-record contents; the access fact has no dedicated class in the frozen policy.
- `.ufo/waves/round-17/falsify/ConformanceAudit.md:53-54` — host package-transaction history, including event chronology, package/actor attribution, and a temporary-path reference. These host-history facts are outside the frozen classes.
- `.ufo/waves/round-17/falsify/ConformanceAudit.md:61-63` — historical cross-round activity details, including run/job identifiers, temporary-path details, journal activity, and a fleet-root write. These are not matched by the C1 classes and are outside the frozen metric.

No private-document contents or concrete OMP routing/model values are visible in this file. The generic category reference at line 81 is not itself a routing value. Line 44 refers to operator configuration but does not reproduce configuration values. No other-session transcript excerpt is reproduced in this audit file; it contains references and summaries of prior activity.

## Frozen population rows

```json
[
  {"path":".ufo/waves/round-17/falsify/ConformanceAudit.md","line":43,"class":"R9","line_sha256":"f41f1d13d0350d0b30336118bdf7b3189fdd52b8a6664a34a9ba316eed7b48a8","decision":"redact","reason":"Session-record value disclosure outside the permitted contexts; replace with neutral finding metadata retaining verdict, count, class, and original line digest."},
  {"path":".ufo/waves/round-17/falsify/ConformanceAudit.md","line":44,"class":"R7","line_sha256":"8de187ab2fabfdb923a1dde890dc46e0b6dcd772f46eb2c7c0ccda3e9af2a319","decision":"redact","reason":"Operator-configuration reference and line-range detail are not an allowed surface-only contract statement; retain only verdict, count, class, and original line digest."},
  {"path":".ufo/waves/round-17/falsify/ConformanceAudit.md","line":44,"class":"R9","line_sha256":"8de187ab2fabfdb923a1dde890dc46e0b6dcd772f46eb2c7c0ccda3e9af2a319","decision":"redact","reason":"Private record-field/value reporting outside the permitted contexts; retain only verdict, count, class, and original line digest."},
  {"path":".ufo/waves/round-17/falsify/ConformanceAudit.md","line":46,"class":"R3","line_sha256":"22465d90379d23601814115ba9250f4f5308d1066e212c9410b0a1f7b275af4a","decision":"redact","reason":"Numbered session tool-output artifact identifiers are not allowlisted; retain only verdict, count, class, and original line digest."},
  {"path":".ufo/waves/round-17/falsify/ConformanceAudit.md","line":46,"class":"R5","line_sha256":"22465d90379d23601814115ba9250f4f5308d1066e212c9410b0a1f7b275af4a","decision":"redact","reason":"Shell-history reference is not allowlisted; retain only verdict, count, class, and original line digest."},
  {"path":".ufo/waves/round-17/falsify/ConformanceAudit.md","line":46,"class":"R6","line_sha256":"22465d90379d23601814115ba9250f4f5308d1066e212c9410b0a1f7b275af4a","decision":"redact","reason":"Privileged-configuration reference is not allowlisted; retain only verdict, count, class, and original line digest."},
  {"path":".ufo/waves/round-17/falsify/ConformanceAudit.md","line":74,"class":"R9","line_sha256":"615eb07331c47fe324e42354d643ab63ef95d0410cb5495c9baf1ed7ee5abd17","decision":"redact","reason":"Session-record field/value report outside the permitted contexts; retain finding result, count, class, and original line digest."},
  {"path":".ufo/waves/round-17/falsify/ConformanceAudit.md","line":75,"class":"R9","line_sha256":"9634076935132e1cdbcf3d06aef5e5e93ba0536e7c10c1167b02e54c0ae40e02","decision":"redact","reason":"Private retry/model-record reference and value-reporting detail outside the permitted contexts; retain finding result, count, class, and original line digest."}
]
```
