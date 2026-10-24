# R18 build — SrcOwaspLogging (C1 source screen)

Seat: MoriR18Recovery.SrcOwaspLogging. Leaf member; no dispatch. Read-only tooling (`read` only); no installs, no downloads written to disk, no lane VCS commands, no writes outside this report. Tooling installed: none.

## 1. Primary source opened

- URL opened: https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html
- Access date: 2026-10-21 (fetched via `read`, rendered HTML→markdown; 394 rendered lines).
- Document version/date: none displayed in the fetched page. Generator metadata only: mkdocs-1.6.1 / mkdocs-material-9.7.7. No revision date is exposed, so the version is recorded as *unknown*, identified by fetch date and the page's own text. [INFERENCE: none beyond this.]
- Section: "Data to exclude" (rendered-text heading at line 198; intro sentence line 204; bullet list lines 206–217). Line numbers are rendered-text line numbers of the fetched markdown, not source-file lines.
- Located quote (19 words, line 204, under "Data to exclude"): "should usually not be recorded directly in the logs, but instead should be removed, masked, sanitized, hashed, or encrypted"
- Adjacent teaching, same section (paraphrase, not quoted): session identifiers → hashed value if tracking is needed (line 207); access tokens, passwords, connection strings, keys, payment data, PII → excluded/transformed (lines 208–217); file paths, connection strings, internal network names and non-sensitive personal data → "special manner" before recording, not blanket exclusion (sub-list after the bullets, rendered text).
- Related guidance, same page: "Event collection" → when a field is malformed, "omit or safely replace that field … do not discard the entire security event" (first bullet under "Event collection"; cited by heading, no line number). "Sanitization can be undertaken post log collection, and prior to log display" (under "Data to exclude", by heading).

### What it teaches mori (C1 observability / log handoff)

1. Treatment vocabulary per data class: exclude, remove, mask, sanitize, hash, or encrypt. Map each C1 gate hit class to one of these treatments rather than to a single "delete" action.
2. Field-level, not record-level: replace or mask the offending field and keep the event (cheat sheet, "Event collection"). A C1 count reaching 0 by dropping whole records would contradict this; L1 should treat record-dropping as a finding, not a pass.
3. Hash, don't drop, when the value is needed for correlation: session identifiers are the explicit example.
4. Two-tier treatment for "special" data (paths, internal hostnames, non-sensitive PII): not blanket exclusion, but a documented handling step. This matters for committed reports where a path is evidence.
5. Redaction may happen at handoff/display rather than at write time (sanitization "post log collection, and prior to log display"). Useful when the committed artifact needs the raw field only in a restricted store.

Limits: the page is guidance, not normative; it uses "should usually"; it does not define the mori C1 policy classes, and it does not say how a committed repository should treat historic exposures (out of scope; operator/kagi-owned per contract).

## 2. Tier proposal (primary)

- Tier **B** (expert secondary). Scope: classification of data to exclude/mask/hash/encrypt for application log entries and log handoff. Reason: consolidated OWASP guidance that itself cites the normative ASVS (see §3) and NIST SP 800-92; not a requirement standard.

## 3. Alternative source screened

- URL opened: https://raw.githubusercontent.com/OWASP/ASVS/v5.0.0/5.0/en/0x25-V16-Security-Logging-and-Error-Handling.md (tag v5.0.0; fetched 2026-10-21 via github-raw). Note: the same path on `master` returned HTTP 404 (path under `5.0/en/0x15-…` did not exist); the tagged path is the one the OWASP Top 10 2025 A09 reference list points at (`…/v5.0.0/5.0/en/0x25-V16-Security-Logging-and-Error-Handling.md`).
- Located requirement V16.2.5 (verbatim, 20 words): "Other data, such as session tokens, may only be logged by being hashed or masked, either in full or partially."
- Same requirement, first sentence (paraphrase): when logging sensitive data, enforcement follows the data's protection level; certain data such as credentials or payment details may not be logged at all.
- V16.4.1 (log-injection encoding) cross-checks the cheat sheet's sanitization point.
- Decision: **ADMIT** as tier A (normative, versioned tag, requirement-level IDs). Reason it adds value beyond the cheat sheet: it distinguishes "may not be logged" (credentials, payment details) from "hashed or masked" (session tokens); the cheat sheet collapses these into one bullet with "removed … or encrypted". For C1 this means a credential class must be removed, while a session-token class may be kept as a hash. Disagreement on credentials vs tokens is none: both documents agree that tokens are not logged in plain form.

## 4. Registry rows (draft; L1 integrates; SOURCES.md NOT edited)

Column shape matches `corpus/SOURCES.md` header: id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by. Id left as S0xx per assignment.

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S0xx | OWASP Cheat Sheet Series: Logging — https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html | docs | B | application log data-class treatment (exclude, remove, mask, sanitize, hash, encrypt) before log handoff | "Data to exclude" heading:198; intro sentence:204 (quote: "should usually not be recorded directly in the logs, but instead should be removed, masked, sanitized, hashed, or encrypted"); bullets:206-217; no revision date shown, mkdocs-material 9.7.7 build; opened 2026-10-21 | Map each log data class to one treatment; hash session identifiers when correlation is needed; replace the malformed field rather than drop the whole event; paths and internal names get documented handling, not blanket exclusion. | queued | 2026-10-21 | 90d | — |
| S0xx | OWASP ASVS 5.0.0 V16 Security Logging and Error Handling — https://raw.githubusercontent.com/OWASP/ASVS/v5.0.0/5.0/en/0x25-V16-Security-Logging-and-Error-Handling.md | spec | A | requirement-level treatment of sensitive data in security logs (V16.2.5), with log-injection encoding (V16.4.1) | V16.2.5 (requirement ID, tag v5.0.0; "Other data, such as session tokens, may only be logged by being hashed or masked, either in full or partially."); V16.4.1; fetched 2026-10-21 | Credentials and payment details may not be logged; session tokens may be logged only hashed or masked, so the treatment depends on the data's protection level. | queued | 2026-10-21 | 365d | — |

Screened alternative verdict (in the row above): ADMIT, tier A.

## 5. Recheck commands (recorded; NOT run this wave — no downloads permitted)

- Cheat sheet: `curl -fsSL https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html | grep -c "should usually not be recorded directly in the logs"` — expect `1`. Line numbers (198/204/206–217) come from the `read` tool's markdown rendering and must be re-derived with the same tool, not from raw HTML.
- ASVS: `curl -fsSL https://raw.githubusercontent.com/OWASP/ASVS/v5.0.0/5.0/en/0x25-V16-Security-Logging-and-Error-Handling.md | grep -c "may only be logged by being hashed or masked"` — expect `1`.

## 6. Out of scope / not done

- SOURCES.md not edited (L1 integrates).
- No change to C1 policy, allowlist, or lane files; no reading of frozen C1 policy classes (not needed for this source question; L1 to map cheat-sheet treatments to the gate's classes).
- No version/date for the cheat sheet could be established from the page itself; the row's `recheck` 90d reflects that it is a rolling page.
- Publication-date claim for ASVS v5.0.0 not asserted (the fetched text carries none); [INFERENCE] none.
