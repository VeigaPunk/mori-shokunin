# Round 18 — SrcNist800122 (C1 minimization source)

Author seat: MoriR18Recovery.SrcNist800122 (leaf, source reader). Access date: 2026-10-21 (UTC).
Scope: source for C1 minimization of use, collection and retention of PII. No file written outside this report. No package installed or upgraded. No excluded path, transcript, credential or operator configuration opened.

## 1. Primary source opened

- Exact URL opened: https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-122.pdf (read tool, converted text; 1391 converted lines).
- Landing page opened: https://csrc.nist.gov/pubs/sp/800/122/final (read tool, HTML). The page carries an anti-framing banner in its markup; the bibliographic metadata and PDF link were read normally.
- Document: NIST Special Publication 800-122, *Guide to Protecting the Confidentiality of Personally Identifiable Information (PII)*, McCallister, Grance, Scarfone; April 2010. Landing page document history: "04/06/10: SP 800-122 (Final)". No later revision listed at access.
- Located quote 1 (≤25 words), §4.2.1 "Minimizing the Use, Collection, and Retention of PII", printed page 4-3 (converted text line 627):
  "PII collections should only be made where such collections are essential to meet the authorized business purpose and mission of the organization." (22 words)
- Located quote 2, Executive Summary heading, printed page ES-2 (converted text line ~157):
  "Organizations should minimize the use, collection, and retention of PII to what is strictly necessary" (15 words)
- Located quote 3, §4.2.1, printed page 4-3 (converted text line 627):
  "If the PII serves no current business purpose, then the PII should no longer be used or collected." (18 words)
- Also in §4.2.1 (printed page 4-3/4-4): regular review of holdings; PII no longer relevant and necessary "should be properly destroyed", subject to litigation holds and NARA schedules. Footnote 48 defers review frequency to applicable laws and policies.

### What it teaches mori (C1)

1. Retention is decided by a necessity test per item (current business purpose), not only by whether an item matches a pattern class. A gate that counts class hits cannot by itself establish that a committed item is unnecessary; the necessity test is a separate judgment that must be recorded.
2. Minimization is also a periodic-review duty over existing holdings (§4.2.1), which supports measuring the before/after population at a fixed revision rather than assuming removal from the current tree is complete.
3. Disposal is governed by the organization's own schedules and holds. Mori's C1 target (0 hits in tracked blobs) is a repository-hygiene measure; the source does not establish that removal from history is required or sufficient. [INFERENCE: history rewrite is out of scope per the contract, consistent with this.]

### Applicability caveat

SP 800-122 is written for Federal agencies; §1.1 states it "may be used by nongovernmental organizations on a voluntary basis". It does not define mori's private-context classes. Applying its principle to the lane is [INFERENCE] and must be cited as guidance, not as a legal obligation.

### Proposed tier

Tier **A** (primary, normative guidance from a standards body) with scope: "federal-agency PII confidentiality guidance; minimum-necessary collection, use and retention principle; voluntary non-federal use per §1.1; not a legal obligation for mori."

## 2. Alternative source screened

- Candidate: Regulation (EU) 2016/679 (GDPR), Article 5(1)(c) "data minimisation".
- URL: https://eur-lex.europa.eu/eli/reg/2016/679/oj/eng — opened 2026-10-21 through the read tool (returned the full OJ text converted from the EUR-Lex page). A direct curl GET to the same URL returned HTTP 202 (no body) in both attempts; the read tool was the only content path, so the text is not independently checksummed.
- Located quote (Art. 5(1)(c), converted text line 507): "adequate, relevant and limited to what is necessary in relation to the purposes for which they are processed ('data minimisation')" (20 words). Recital (39) also states the storage period must be "limited to a strict minimum".
- Decision: **REJECTED** for the C1 registry as a citation. Reason: the Regulation is binding only where its Article 3 territorial scope applies; no lane fact establishes processing of EU data subjects' personal data. [INFERENCE: the lane is not an EU controller.] The same principle is already grounded in S0xx (SP 800-122), so the GDPR text adds no load-bearing claim for C1. Flip condition: admit as a scoped tier-A row if the operator establishes EU-data-subject processing for the lane.

## 3. Registry rows (for L1 integration; SOURCES.md not edited)

Column shape: id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S0xx | NIST SP 800-122, Guide to Protecting the Confidentiality of Personally Identifiable Information (PII) — https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-122.pdf | docs | A | PII minimum-necessary collection, use and retention; federal-agency guidance with voluntary non-federal use (§1.1) | ES-2 heading "Organizations should minimize the use, collection, and retention of PII"; §4.2.1 printed pp. 4-3 to 4-4; April 2010 final, document history 04/06/10; landing page https://csrc.nist.gov/pubs/sp/800/122/final opened 2026-10-21 | Retention needs a current-business-purpose test per item: PII with no current purpose "should no longer be used or collected"; holdings need periodic review and disposal under schedules. A class-hit gate does not by itself establish necessity. | queued | 2026-10-21 | 365d | — |
| S0xx | GDPR Regulation (EU) 2016/679 Art. 5(1)(c) — https://eur-lex.europa.eu/eli/reg/2016/679/oj/eng | spec | A | EU-jurisdiction personal-data processing only (Art. 3 scope); not applicable to the lane on present facts | Art. 5(1)(c), converted text line 507; recital (39) "limited to a strict minimum"; opened 2026-10-21 via read tool, direct GET returned 202 | REJECTED: binding only where Art. 3 territorial scope applies, and no lane fact establishes EU-data-subject processing; the principle is already grounded by the NIST row above, so no load-bearing claim is added. Flip: admit as scoped tier-A if EU-data-subject processing is established. | rejected | 2026-10-21 | 365d | — |

Note for L1: the NIST row's `used-by` is "—" because no committed lesson or policy file cites it yet; C1 policy citations are for L1 to place. The NIST `id` is left as S0xx per instruction (next free numeric id after S048 is for L1 to assign).

## 4. Recheck commands (no file written; byte-range GET fetches 1 byte per check)

- `curl -s -r 0-63 -A 'Mozilla/5.0' -o /dev/null -w '%{http_code} %{content_type}\n' https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-122.pdf` — observed 2026-10-21: `206 application/pdf` (the full-GET HEAD attempt `curl -sIL` returned 404 for the same URL, so HEAD is not a valid recheck method for this host).
- `curl -sIL --max-time 30 -o /dev/null -w '%{http_code}\n' https://csrc.nist.gov/pubs/sp/800/122/final` — observed 2026-10-21: `200`.
- `curl -s -r 0-0 -A 'Mozilla/5.0' -o /dev/null -w '%{http_code}\n' https://eur-lex.europa.eu/eli/reg/2016/679/oj/eng` — observed 2026-10-21: `202` (no body; the read tool is the content path).

## 5. Tooling and VCS

- Tools installed or upgraded: none.
- Lane read: `git -C /home/vgpnk/Projects/shokunin/mori-shokunin log -1 --format=%H` returned `11db4df00bca48f49fada47a2a19b371e86f8778`. [INFERENCE: this differs from the contract's entering tip d005cdde; L1 should confirm the lane tip before integrating.] No mutating VCS command was run.
- Scratch: none written; no `/tmp` use; no downloads saved.

## 6. Out of scope / not done

- No edit to `corpus/SOURCES.md`, the lane checkout, or any sibling file.
- No verification of the C1 gate itself; no judgment on the C1 claim.
- Converted-text line numbers (markit for the PDF; jina for EUR-Lex) are reading aids; printed page numbers are the citation anchors.
