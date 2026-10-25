author: mori-shokunin (L1 MoriR18Recovery, round 18 recovery attempt 2)

# Round 18 — repair the round-17 privacy harm, then freeze-order and dispatch binding

Entering tip `d005cdde0e009dea6c0cc29b37163de536528658` (round-17 non-author spot-check,
verdict rejected-harmed: adjacency harmed by committed private context). Attempt 1
(launch 2026-10-20T18:52:38-03:00) left no lane files, waves, worktrees or seats; nothing was
reused or discarded. Requirement freeze commit `29b0dc79e193b9d67845e39850a091a84bad66bd`
precedes every implementation commit (first: `b8f5c6c`).

## Claims

- **C1 adjacency (sourced S049–S052):** committed private-context retention, frozen classes
  R1–R9; before 116 unallowlisted hits (routed 40) at d005cdd.
- **C2 calibration (lowest, tie at 5):** freeze-order verdicts; before 1 uncorrected
  pre-build overclaim (r17-C3); r18 claims verified pre-build at the measured tip.
- **C3 operability:** per-attempt dispatch payload binding; round-17 legacy receipts 9/9
  unbound versus round-18 ledgers.

## Gate

Sources opened 2026-10-21 by round-18 scribes (`.ufo/waves/round-18/build/Src*.md`), decided
by the L1. Every row below is new (status none → listed).

| Row | URL | Decision | Located quote (≤25 words) and location |
|---|---|---|---|
| S049 | https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html | admit B, mined | "should usually not be recorded directly in the logs, but instead should be removed, masked, sanitized, hashed, or encrypted" — "Data to exclude", rendered line 204 |
| S050 | https://raw.githubusercontent.com/OWASP/ASVS/v5.0.0/5.0/en/0x25-V16-Security-Logging-and-Error-Handling.md | admit A, mined | "Other data, such as session tokens, may only be logged by being hashed or masked, either in full or partially." — V16.2.5 |
| S051 | https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-122.pdf | admit A, mined | "PII collections should only be made where such collections are essential to meet the authorized business purpose and mission of the organization." — §4.2.1, p. 4-3 |
| S052 | https://opentelemetry.io/docs/security/handling-sensitive-data/ | admit A, mined | "hashes are reversible in practice if the input space is small and predictable" — "Replacing user.id with user.hash" callout |
| S053 | https://opentelemetry.io/docs/security/config-best-practices/ | admit A, queued | "Attributes that aren't on the allowed list are removed before any value checks are done." — "Scrub sensitive data", ¶2 |
| S054 | https://eur-lex.europa.eu/eli/reg/2016/679/oj | **reject** (scope) | "adequate, relevant and limited to what is necessary in relation to the purposes for which they are processed" — Art. 5(1)(c) |
| S055 | https://www.strac.io/blog/gdpr-data-minimization | reject C (vendor blog) | screened alternative; restates S054 without primary authority |
| S056 | https://www.pnas.org/doi/10.1073/pnas.1708274114 (PMC5856500) | admit A, mined | "define the research questions and analysis plan before observing the research outcomes" — Abstract |
| S057 | https://doi.org/10.1177/1745691612463078 | reject C | label-level confirmatory/exploratory agenda; adds no ordering test |
| S058 | https://git-scm.com/docs/git-rev-list ; https://git-scm.com/docs/git-diff-tree | admit A, mined | "Output the commits chosen to be shown (see Commit Limiting section above) in reverse order." — git-rev-list `--reverse` |
| S059 | https://git-scm.com/docs/git-log | reject C | porcelain ordering/merge-diff defaults; plumbing S058 governs |
| S060 | https://slsa.dev/spec/v1.0/provenance (+ in-toto ResourceDescriptor) | admit A, mined | "A descriptor that specifies a `digest` is assumed to refer to an immutable resource or artifact." — ResourceDescriptor, Semantics |
| S061 | https://git-scm.com/book/en/v2/Git-Internals-Git-Objects | reject C (tutorial) | "Git is a content-addressable filesystem." — §10.2 |
| S062 | https://www.rfc-editor.org/rfc/rfc8785 | admit A, mined | "Whitespace between JSON tokens MUST NOT be emitted." — §3.2.1 (used to bound, not to claim, canonicality) |
| S063 | https://docs.python.org/3/library/json.html | reject C for this question | parameter docs cannot establish a canonical form |

Disagreement inside the lane: SrcGdprArt5 proposed admitting S054 as tier A; SrcNist800122
screened it and rejected it for scope. The L1 rejected it: GDPR binds EU personal-data
processing (Art. 3), mori's committed host/agent evidence is not that, so minimization is
grounded in S049–S052 and GDPR is cited only as an analogy.

Spot-check: pending the non-author closure (a lane-dispatched seat is still the lane).
Wave-2 re-opening seats are author-side falsifiers, not the outside check.

## Mistakes

| ID | Class | Evidence | Captured-by | Fix (shown able to fail) |
|---|---|---|---|---|
| M1 | adjacency / retention | round-17 committed other-session output, session identities, operator config values and session-record values (`round-17-verifier-spotcheck.md:322-350`); frozen population 116 hits in 28 files (`.ufo/waves/round-18/frozen/c1-population.json`) | none — Q44/Q45 bind instruction text and disclosure, Q50 a display cap; nothing minimized committed handoffs | QUALITY 51 + `tools/mori-retention-gate.py`: exits 1 at d005cdd (metric 116, population_match true) and on 9 planted class fixtures (selftest 19/19 arms) |
| M2 | calibration / freeze label | r17-C3 labelled "precommitted" at five locations; ruled co-evolved (`round-17-verifier-spotcheck.md:207-213,398-402`) | none | QUALITY 52 + `tools/mori-freeze-order.py`: r17-C3 `co-evolved`, overclaim 1, exit 1 before the appended correction; co-commit selftest arm exits 1 |
| M3 | provenance | round-17 attempt receipts carry no payload digest (9 rows) (`round-17-verifier-spotcheck.md:291-297`) | partial (Q44 binds the spec only) | QUALITY 53 + `tools/mori-dispatch-ledger.py`: legacy files 5 and 4 unbound, exit 1; tamper selftest arms exit 1 |
| M4 | scope | carried V1–V3, V5–V14 and L1 authorization (`round-17-verifier-spotcheck.md:303-320,403-407`) | partial (Q37–Q39, Q44) | QUALITY 54; wave-2 context adds the V12 jj-config prohibition and the not-runtime/clean-state caveat (`build/SentinelContextAudit.md`); context check rc0 both waves |
| M5 | reference-drift (round 18) | contract acceptance examples contradicted the frozen rules: C2 example kept r18 `no-implementation` rows out of the overclaim count, C1 example expected zero new hits at the freeze commit although the frozen inputs self-match (`build/FreezeOrder.md` discrepancy; `build/RetentionGate.md` blocker) | none | QUALITY 55; the L1 fixed the tool to the literal rule (`no-implementation` + pre-build label = overclaim) and updated its selftest arm; at the freeze commit the check now exits 1 with 4 overclaims |
| M6 | scope (round 18) | seat ScribeLessonDraft redirected committed lesson text to a /tmp file and removed it (disclosed, `build/ScribeLessonDraft.md` §5) | Q38 (caught by disclosure, not prevented) | carried as a V-class deviation; no private value involved |

## Carried, not closed

- Out-of-metric private context in six session-derived and two host-config round-17 reports:
  minimization drafting was refused by the process job cap (`.ufo/waves/round-18/residual-drafting-attempts.json`); disposition in `.ufo/waves/round-18/out-of-metric-triage.md`.
- Pushed history still holds the original bytes; exposure assessment is operator/kagi-owned.
- Old r10 drift red and r13–r16 HEAD/env/output qualifications remain open; no repin.
- Package/boot-chain events of 2026-10-20 remain a detection-only tsukuroi/operator handoff.
