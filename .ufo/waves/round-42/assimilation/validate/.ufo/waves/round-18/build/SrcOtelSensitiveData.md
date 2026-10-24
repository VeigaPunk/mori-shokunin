# R18 source scribe — OpenTelemetry sensitive-data guidance (C1 telemetry minimization / redaction / hashing)

Seat: MoriR18Recovery.SrcOtelSensitiveData. Access date for all opens: 2026-10-21.
No file written except this report. No downloads, no installs, no VCS, no lane edits. `corpus/SOURCES.md` NOT edited (L1 integrates).
Tooling: none installed or updated this seat (read tool only).

## 1. Primary source opened

- URL: https://opentelemetry.io/docs/security/handling-sensitive-data/ (markdown alternate `index.md` read at the same URL family)
- Opened: 2026-10-21 via read tool, markdown alternate; raw HTML read for metadata.
- Version/date: no version number on the page. Page metadata (raw HTML `<meta property="article:modified_time">` and `dateModified`): **2026-01-14T14:37:39-05:00**. Page word count metadata: 574.
- Section headings in order: Your responsibility; Sensitive data considerations; Data minimization; Protecting sensitive data; Deleting and hashing user information; Replacing `user.id` with `user.hash`; Truncating IP addresses; Delete attributes with redaction processor.
- Line numbers: the read tool output for the markdown alternate does not carry line numbers; locations below are given by heading and bullet ordinal. [INFERENCE] none of the located quotes depend on a numeric line.

### Located quotes (each ≤25 words)

- Q1 (13 words): "hashes are reversible in practice if the input space is small and predictable" — section "Replacing `user.id` with `user.hash`", callout "Risk and limitations of hashing for anonymization".
- Q2 (9 words): "Only collect data that serves an observability purpose." — section "Data minimization", bullet 1.
- Q3 (11 words): "Consider whether aggregated or anonymized data could serve the same purpose." — section "Data minimization", bullet 3.

### What it teaches mori

1. Minimization first: the page's own priority is not to collect a sensitive attribute at all; redaction/hashing are fallbacks ("the best way to prevent the collection of sensitive data is not to collect data that might be sensitive", section "Protecting sensitive data").
2. Hashing is not anonymization for small or predictable input spaces (Q1). A mori redaction rule must not claim that a hashed numeric identifier is protected.
3. Truncation / coarsening is named as the alternative to hashing: drop the last IPv4 octet or last 80 bits of IPv6; keep only domain of email; keep only year/month of dates (section "Truncating IP addresses").
4. Allow-list deletion is the collector-level mechanism (`redaction` processor, see Section 3).
5. The page makes the implementer responsible for instrumentation library output too (section "Your responsibility") — mori must review any instrumentation it consumes, not assume it is clean.

### Tier proposal

- Tier **A** (primary/normative for OpenTelemetry project behaviour and recommended configuration). Scope: OTel-project guidance on what minimization, attribute deletion, hashing and truncation mean in OTel processors. It is **not** a legal standard, not a proof that any given attribute is non-sensitive, and not evidence that a specific mori deployment is compliant.
- Row proposed below as `queued` (not yet mined by any lesson).

### SOURCES.md registry row (draft; not written to SOURCES.md)

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S0xx | OpenTelemetry Handling sensitive data — https://opentelemetry.io/docs/security/handling-sensitive-data/ | docs | A | telemetry data minimization, attribute deletion, hashing and truncation guidance for OTel pipelines, scope limited to OTel-project recommendations rather than legal compliance | Data minimization bullets 1-4; Protecting sensitive data; Deleting and hashing user information; Replacing user.id with user.hash callout "Risk and limitations of hashing for anonymization"; Truncating IP addresses; page metadata article:modified_time 2026-01-14T14:37:39-05:00; opened 2026-10-21 | Collect the attribute only when an observability purpose needs it; hashing a small or predictable identifier is reversible in practice, so prefer drop or truncation and do not claim anonymization. | queued | 2026-10-21 | on-release | — |

Note: the row shape matches the 11-column header of corpus/SOURCES.md; the `S0xx` id is left for the L1 to assign. Cell text contains no `|` character.

## 2. Alternative screened (one)

- URL: https://opentelemetry.io/docs/security/config-best-practices/ (markdown alternate `index.md` at same family), opened 2026-10-21.
- Version/date: page modified date not observed in the fetched markdown; [INFERENCE] current docs. Recheck command below records this as a gap.
- Located quote (15 words): "deletes span, log, and metric datapoint attributes that don't match a list of allowed attributes" — section "Scrub sensitive data" (under "Manage specific security risks" → "Configure your Collector to block these security threats"), first paragraph.
- Second located quote (15 words): "Attributes that aren't on the allowed list are removed before any value checks are done." — section "Scrub sensitive data", second paragraph.
- Content: concrete `redaction` processor config with `allow_all_keys: false`, `allowed_keys`, `ignored_keys`, and `blocked_values` regexes for card numbers, plus a `summary: debug` setting.

### Decision: ADMIT (tier A, narrow scope)

Reason: it supplies the only concrete, primary-source example in this family of the allow-list deletion and value masking mechanism that the primary source's "Delete attributes with redaction processor" section defers to. Scope is strictly the Collector `redaction` processor's semantics and example configuration. It does not establish hashing, truncation, or sensitive-data classification, and it does not establish which attributes mori emits are sensitive.

Flip condition (to reject): if the current page is found to have been superseded or its redaction section moved to a page with different semantics, the row becomes `rejected` with that reason.

Registry row draft (not written):

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S0xx | OpenTelemetry Collector configuration best practices, Scrub sensitive data — https://opentelemetry.io/docs/security/config-best-practices/ | docs | A | Collector redaction processor allow-list deletion and blocked-value masking semantics and example config; not hashing, truncation or sensitive-data classification | Scrub sensitive data section, paragraphs 1-2 and example YAML; page modified date not observed in fetched markdown | Attributes outside an allow-list are deleted before value checks; blocked-value regexes mask allowed attributes. Allow-list is a deletion mechanism, not an anonymization claim. | queued | 2026-10-21 | on-release | — |

## 3. Not admitted as a row (read for context only)

- Wikipedia "Data minimization" (https://en.wikipedia.org/wiki/Data_minimization) was read only to confirm the term the primary source links to. It is an encyclopedia, not a registry-tier source; no row proposed. The regulatory texts it cites (e.g. GDPR second principle) would be the primary source if mori later needs a legal anchor; not screened this round.

## 4. Recheck commands (not executed; for the L1 or a future scribe)

- Primary modified date: `curl -s https://opentelemetry.io/docs/security/handling-sensitive-data/ | grep -o 'article:modified_time[^>]*'` (expect 2026-01-14T14:37:39-05:00 unless updated; stdout only, nothing saved).
- Primary quote presence: `curl -s https://opentelemetry.io/docs/security/handling-sensitive-data/index.md | grep -n -F 'predictable (e.g. numeric user IDs)'`.
- Alternative quote presence: `curl -s https://opentelemetry.io/docs/security/config-best-practices/index.md | grep -n -F "don't match a list of allowed attributes"`.
- Alternative date (gap): `curl -s https://opentelemetry.io/docs/security/config-best-practices/ | grep -o 'article:modified_time[^>]*'`.
- Recheck cadence: on-release, matching the OTel docs release rhythm; the L1 may set 180d.

## 5. Findings summary

- Primary: admitted, tier A, scoped to OTel-project recommendations; located quotes recorded; modified date 2026-01-14.
- Alternative: admitted, tier A, narrow scope (Collector redaction allow-list semantics); modified date not observed.
- Wikipedia: not a row.
- Gaps: no line numbers for the markdown alternates; alternative page date unobserved; neither source establishes that any mori attribute is sensitive or that any mori output is compliant.
- Touched surfaces: this report only. No SOURCES.md edit, no lane edit, no VCS, no install.
