# SrcNosekPrereg — scoped source findings for round-18 C2 (freeze-order)

Scribe seat: MoriR18Recovery.SrcNosekPrereg. Access date: 2026-10-21. Scope: one primary source plus one alternative screened. No file other than this report was written; `corpus/SOURCES.md` was not edited (the L1 integrates).

## 1. Access record

| item | value |
|---|---|
| requested URL | https://www.pnas.org/doi/10.1073/pnas.1708274114 |
| result for requested URL | HTTP 403 on 2026-10-21 (read tool, `Method: failed`); re-check with curl also HTTP 403 |
| metadata + abstract obtained via | https://doi.org/10.1073/pnas.1708274114 (CrossRef API, read tool, 2026-10-21) |
| full text obtained via | https://pmc.ncbi.nlm.nih.gov/articles/PMC5856500/ (PubMed Central mirror of the same DOI; PMCID PMC5856500; PMID 29531091; read tool, 2026-10-21) |
| document | Nosek BA, Ebersole CR, DeHaven AC, Mellor DT. "The preregistration revolution." Proc Natl Acad Sci U S A 115(11):2600–2606 |
| version/date | CrossRef "Published: 2018-03-12"; PMC "Issue date 2018 Mar 13"; PNAS licence; PMC states it is the PNAS article (Sackler Colloquium series). Accepted for review 2017-06-15 (received), approved 2017-08-28 per PMC front matter |
| Europe PMC cross-check | https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=DOI:10.1073/pnas.1708274114&format=json (read tool, 2026-10-21): hitCount 1, pmcid PMC5856500, pageInfo 2600-2606 |

Gap: the PNAS publisher page itself was not readable (403). Content was taken from the CrossRef abstract and the PMC full text, which match each other on the abstract sentences quoted below. The PDF on PMC (`pdf/pnas.201708274.pdf`) was not opened; page-level pin cites are therefore not given. Locations are section headings.

## 2. Located quotes (each ≤25 words)

| # | quote (verbatim) | words | location | verified |
|---|---|---|---|---|
| Q1 | "define the research questions and analysis plan before observing the research outcomes" | 14 | Abstract (PMC and CrossRef agree) | grep on PMC text: 1 match |
| Q2 | "In prediction, the problem of forking paths is avoided because the analytic pipeline is specified before observing the data." | 19 | section "Standard Tools of Statistical Inference Assume Prediction" | grep: "the analytic pipeline is specified before observing the data" 1 match |
| Q3 | "If the outcomes have not yet been observed, Jolene can document the changes to her preregistration without undermining diagnosticity." | 19 | section "Challenge 1: Changes to Procedure During Study Administration" | grep: 1 match |
| Q4 | "there is not yet sufficient experimental evidence establishing its superiority for reproducibility" | 13 | section "Preregistration Distinguishes Prediction and Postdiction" | grep: 1 match |

Word counts were counted by hand; each is ≤25.

## 3. What it teaches mori (C2)

1. The distinction is the one C2 needs: prediction is a test whose analysis plan was fixed before observing outcomes; postdiction is analysis chosen after seeing data (Q1, Q2). A freeze commit can only support "pre-build" when it precedes the outcome-bearing implementation; a freeze taken after implementation output is a postdiction. This matches the register's verdict rule (`frozen/c2-register.json`, `verdict_rule`: `co-evolved` when L equals or follows I).
2. Post-hoc edits are not automatically disqualifying, but the rule is timing plus disclosure: changes before outcomes are observed keep diagnosticity (Q3); changes after must be reported as deviations, not silently absorbed. Mori's correction-row approach (appending a row to `corpus/evidence/freeze-register.json` rather than rewriting the declared row) is consistent with this disclosure norm.
3. Limit: the paper does not establish that preregistration improves reproducibility empirically (Q4). Mori must not cite it as proof that freezing improves outcomes; it supports the definitional and labelling rule only.
4. [INFERENCE] Git commit order is a proxy for "before observation", not proof of it. A frozen commit can precede an implementation while the author already knew the outcome. The register's `pre-build` label therefore certifies commit ordering only; it does not certify absence of prior knowledge. This caveat should appear wherever C2 is reported.

## 4. Tier proposal

- Tier **A** (primary/normative), scope: definitions of prediction versus postdiction, the timing rule for committed plans, and the disclosure rule for deviations. Not scoped as empirical evidence of reproducibility gains (Q4).

## 5. Registry row (draft, for L1 integration; id left as S0xx)

Column shape matches `corpus/SOURCES.md` line 5: `id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by`.

```
| S0xx | Nosek, Ebersole, DeHaven & Mellor (2018), "The preregistration revolution" — https://www.pnas.org/doi/10.1073/pnas.1708274114 (full text via https://pmc.ncbi.nlm.nih.gov/articles/PMC5856500/; pnas.org HTTP 403 on 2026-10-21) | paper | A | prediction versus postdiction distinction; preregistration as a plan committed before outcomes are observed; disclosure of deviations; definitional scope only, not empirical proof of reproducibility gains | Abstract; "Standard Tools of Statistical Inference Assume Prediction" (quote: "In prediction, the problem of forking paths is avoided because the analytic pipeline is specified before observing the data"); "Preregistration Distinguishes Prediction and Postdiction" ("there is not yet sufficient experimental evidence establishing its superiority for reproducibility"); "Challenge 1: Changes to Procedure During Study Administration"; PNAS 115(11):2600-2606, issue 2018 Mar 13; PMC5856500 full text; PDF not opened | Freezing the analysis plan before observing outcomes is what makes a claim a prediction; a freeze taken after observation is postdiction, and later changes must be disclosed as deviations. Mori's C2 pre-build label certifies commit order before the outcome-bearing implementation, not absence of prior knowledge. | queued | 2026-10-21 | 365d | — (proposed: round-18 C2 freeze-order register, `.ufo/waves/round-18/frozen/c2-register.json`; not yet cited by any note) |
```

Note for L1: `kind` value `paper` is not among the existing kinds in the registry (docs, code, spec, book, community, tool, own-work). Use `docs` or `spec` if the L1 wants to keep the existing vocabulary; this report does not decide it.

## 6. Alternative screened and rejected

Candidate: Wagenmakers, Wetzels, Borsboom, van der Maas & Kievit (2012), "An Agenda for Purely Confirmatory Research," Perspectives on Psychological Science, DOI 10.1177/1745691612463078 (CrossRef, read 2026-10-21). Abstract: only analyses committed in advance "deserve the label 'confirmatory'", and only for these are common tests valid.

Decision: **rejected** (tier C). Reasons: (a) same normative question as Nosek, so it adds no independent claim for C2 with the A-tier row in place; (b) its stronger claim (common tests valid only for preregistered analyses) rests on the body, which was not opened (only the CrossRef abstract was read), so it cannot be cited as verified; (c) the Sage full text was not attempted in this round, to avoid an unplanned second access path. Flip condition: a located body quote supporting a claim that Nosek does not already cover, verified in a later round.

Registry row (draft, rejection kept as a row):

```
| S0xx | Wagenmakers, Wetzels, Borsboom, van der Maas & Kievit (2012), "An Agenda for Purely Confirmatory Research" — https://doi.org/10.1177/1745691612463078 | paper | C | REJECTED: confirmatory versus exploratory labelling; second normative article on the same question | Abstract only (CrossRef, Perspectives on Psychological Science, 2012-11); body not opened | REJECTED: same normative claim as the A-tier Nosek row; its stronger validity claim is unverified because the body was not opened; flip: a located body quote supporting a claim Nosek does not already cover. | rejected | 2026-10-21 | 365d | — |
```

Considered but not screened: Kerr (1998), "HARKing," Personality and Social Psychology Review, DOI 10.1207/s15327957pspr0203_4 (CrossRef abstract read). It is a possible later lead on post-hoc presentation as a priori; not screened here, so no row is drafted.

## 7. Recheck command

Run with read-only stdout piping; writes nothing (verified 2026-10-21, all four quotes matched once each):

```
curl -sL --max-time 60 https://pmc.ncbi.nlm.nih.gov/articles/PMC5856500/ | grep -o -e "the analytic pipeline is specified before observing the data" -e "If the outcomes have not yet been observed, Jolene can document the changes to her preregistration without undermining diagnosticity" -e "there is not yet sufficient experimental evidence establishing its superiority for reproducibility" -e "define the research questions and analysis plan before observing the research outcomes" | sort | uniq -c
curl -sI --max-time 30 https://doi.org/10.1073/pnas.1708274114 | head -n 1   # expect HTTP 302
curl -s -o /dev/null -w "pnas.org HTTP %{http_code}\n" --max-time 30 https://www.pnas.org/doi/10.1073/pnas.1708274114   # observed 403 on 2026-10-21
```

Observed results 2026-10-21: four quote matches (count 1 each); `HTTP/2 302` from doi.org; `pnas.org HTTP 403`.

## 8. Tooling and privacy

- Tools installed or updated: none. Used the existing read tool and `curl` (already on the host); no package install, no pacman.
- No files were written except this report. No downloads were saved. No probe output was written to `/tmp`.
- No transcripts, session records, credentials, operator configuration or private documents were opened or quoted. Only the public article text and the public Wagenmakers/Kerr abstracts were read.

## 9. Out of scope / not done

- `corpus/SOURCES.md` not edited (L1 integrates the draft rows above).
- No judgment of C2 or the freeze register (advisory only).
- Pin-level page numbers for the PNAS print version were not verified (PDF not opened); locations are headings.
