# SrcGdprArt5 — GDPR Art. 5(1)(c) as a retention test for C1

Seat: MoriR18Recovery.SrcGdprArt5 (scribe). Access date: 2026-10-21. Scope: source screening for C1 (`contract.md` :24-29, `frozen/c1-policy.json`). No files written except this report; no installs or updates; no subagent dispatch; no lane VCS mutation (one read-only `git log -1` on the lane); `corpus/SOURCES.md` not edited.

## 1. Admitted primary source

- **URL opened:** https://eur-lex.europa.eu/eli/reg/2016/679/oj (read tool, served via reader method `jina`, Content-Type text/html; 2503 lines; not byte-verified against the OJ PDF).
- **Document version/date:** Regulation (EU) 2016/679 "of 27 April 2016" (GDPR), original act at the `/oj` ELI; the served text is the act as published, with no consolidated amendment noted.
- **Located quote (Article 5(1)(c), Article 5 heading "Principles relating to processing of personal data"):** "adequate, relevant and limited to what is necessary in relation to the purposes for which they are processed" (18 words).
- **Located quote (Recital 39, sentence 6):** "Personal data should be processed only if the purpose of the processing could not reasonably be fulfilled by other means." (20 words)
- **Also located:** Recital 39 "...ensuring that the period for which the personal data are stored is limited to a strict minimum... time limits should be established by the controller for erasure or for a periodic review." Article 5(1)(e) storage limitation, "for no longer than is necessary for the purposes."
- **What it teaches mori (C1):** the test is purpose-relative. A retained item is in scope only relative to a stated purpose; the three words are a conjunction (adequate AND relevant AND limited), so each retained element is tested separately. Two halves matter for the gate:
  - "limited" is the over-retention half that C1 counts (unallowlisted hits = retained excess).
  - "adequate" is a floor: over-redaction that removes what the purpose needs fails the same test. C1 counts only retention, so it is one-sided [INFERENCE: nothing in `c1-policy.json` measures over-redaction].
  - Recital 39 "could not reasonably be fulfilled by other means" maps to redacted references (class id, path class, SHA-256, line count) used in place of content, which is the design already used by the report rules.
  - Recital 39 "time limits ... periodic review" maps to the `recheck` column, which C1 does not currently use.
- **Scope caveat (must carry):** GDPR governs personal data of natural persons processed in the EU. C1's classes (session paths, store paths, routing keys, shell history references) are not shown to be personal data in every case. This source is a principle analogy for the retention test, not a legal basis for C1 and not a compliance claim about mori. [INFERENCE]
- **Tier proposal: A** (primary, normative, EU law) with scope: "data-minimisation principle wording and recital guidance, used as a structural test analogy only."

## 2. Corroborating primary-adjacent source (not drafted as a row)

- **URL opened:** https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/data-protection-principles/a-guide-to-the-data-protection-principles/data-minimisation (read tool, native method; page metadata "meta-DC.Date: Tuesday, September 09, 2025").
- **Banner observed:** "Due to changes made by the Data (Use and Access) Act, this guidance is under review and may be subject to change." Tier and recheck must reflect this.
- **Located quote ("At a glance"):** "limited to what is necessary – you do not hold more than you need for that purpose." (17 words)
- **Located quote ("How do we decide"):** "The UK GDPR does not define these terms. Clearly, though, this will depend on your specified purpose..." (purpose-relative confirmation; the lane's adequacy test needs a stated purpose per class.)
- **Use:** confirms that "adequate, relevant and limited" has no fixed definition and is relative to purpose, and that periodic review is expected. Not drafted as a row: the L1 may add it if C1's teaching cites UK guidance. Tier if admitted: B (regulator guidance, under review).

## 3. Draft registry rows (for L1 integration; SOURCES.md not edited)

Column shape: `id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by`. Id left as S0xx for L1 numbering.

Admitted:

`| S0xx | GDPR Regulation (EU) 2016/679, Article 5(1)(c) data minimisation and Recital (39) — https://eur-lex.europa.eu/eli/reg/2016/679/oj | spec | A | data-minimisation retention test: adequate, relevant and limited to purpose; storage time limits and periodic review | Article 5(1)(c) and 5(1)(e); Recital (39) sentences on adequate/relevant/limited, "could not reasonably be fulfilled by other means", and time limits; served text of Regulation of 27 April 2016 read 2026-10-21 | The test is purpose-relative and a conjunction: keep what the stated purpose needs, no more, and not less; over-redaction fails adequacy as well. Scope: principle analogy only, not a legal basis for C1. | queued | 2026-10-21 | 365d | — |`

Rejected alternative (screened same question; a rejection is a row):

`| S0xx | Strac — GDPR Data Minimization: Article 5(1)(c) Explained — https://www.strac.io/blog/gdpr-data-minimization | community | C | vendor blog on GDPR data minimisation and retention enforcement | Article 5(1)(c) quote in body; page dated August 10, 2026; opened 2026-10-21 | REJECTED: vendor marketing for its own DLP product; it asserts "legally binding" framing and DPA fine ranges (for example "€50K–€900K range") with no cited decision, case number or date, so none of its enforcement claims are checkable. Its Art. 5(1)(c) quote matches the primary text, so no unique content is added. Flip: a cited DPA decision with case reference that supports a specific retention claim would make it admissible as a tier-B case note, not as a tier-A source. | rejected | 2026-10-21 | 90d | — |`

## 4. Alternative screened and why rejected (short form)

- strac.io blog: REJECTED (tier C). Vendor product page; unsourced fine ranges; no primary citation beyond the Art. 5 quote it reproduces. Opened 2026-10-21; read via native method.
- European Commission principles page (https://commission.europa.eu/law/law-topic/data-protection/information-business-and-organisations/principles-gdpr_en, opened 2026-10-21): official explainer that restates Art. 5(1)(c) and Recital 39 and adds "time limits to erase or review." Admissible as tier B corroboration; not drafted as a row this round because the primary text already carries those words.

## 5. Recheck command (read-only; not run beyond the reads above)

- Read tool: `read https://eur-lex.europa.eu/eli/reg/2016/679/oj`, then search the returned text for `adequate, relevant and limited to what is necessary`; expect the Article 5(1)(c) line to recur once. Recheck also for the Recital 39 phrase `could not reasonably be fulfilled by other means`.
- ICO: `read` the ICO data-minimisation URL; expect the "under review" banner to be checked each time; revise tier if the page is replaced.

## 6. Tooling and boundaries

- Tools installed or updated: none. No pacman, uv, npm or cargo action this seat.
- Writes: this report only.
- Lane reads: one `git -C /home/vgpnk/Projects/shokunin/mori-shokunin log --oneline -1` (returned `11db4df round-18: wave-1 spec...`). No other lane reads beyond `contract.md`, `frozen/c1-policy.json`, `corpus/SOURCES.md` (read-only).
- Privacy: no transcript, session, or private-config content read or quoted. The artifact spill footer for the EUR-Lex read contains a session-store path; it is not copied here.
- Subagents: none dispatched (leaf member).

## 7. Findings

- F1 (for C1 teaching): adopt the purpose-relative conjunction as the stated test for each retained element; record the purpose class beside each allowlist row, so the adjudication rule in `c1-policy.json` (classes a/b/c) maps to an explicit purpose. [INFERENCE on mapping, principle text observed]
- F2: the "adequate" half is unmeasured by C1; if C1 is to be used as a retention gate, L1 may want a separate over-redaction check. [INFERENCE]
- F3: GDPR scope caveat must travel with any citation of this row; do not cite it as a legal requirement on mori.
