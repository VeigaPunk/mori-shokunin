# Round 13 — structured journal scopes and trustworthy verdicts

date: 2026-10-20 · lane: mori-shokunin · entering commit: `6531ac6029e200a6392bb76673b6a17d3c895c96`.
Round record: LOG.md round-13 entry; fleet report `.ufo/reports/round-13/mori.md`.

## Declared claims

1. **C1 coverage** — acquire independently labeled, MESSAGE-free journal class counts in user and system scopes. Before: the census has only user-journal coverage; after: the system scope reports typed notice classes or explicit unavailable. Counts are records/notices, not unique kills or fleet causation. This is a partial FR1 advance; kernel victim attribution and fleet correlation remain frontier.
2. **C2 operability** — close audit-r11 F01/F02: an exact lane author followed by a large sibling history remains progressing, and the oracle rejects invalid/duplicated/exit-inconsistent final census verdicts while retaining its honest 28-case suite.

Both owned axes enter at 6; either meets the lowest-owned-axis obligation. The planned freshness re-pin is not claimed: the old baseline remains available and red drift is disclosed rather than erased. The round-13 plan is a starting point, not an assertion that a new pin has been earned.

## Mistakes

| id | class | evidence pointer | captured-by | fix |
|---|---|---|---|---|
| M1 | A producer SIGPIPE was interpreted as absence of exact lane authorship | `corpus/knowledge/audit-r11.md:156,308-374`; round-12 lesson M2/M3 left the production path open | Q6/Q7; strengthened Q27 | Consume captured history without an early-exiting reader; large-history behavioral regression and its negative witness recorded in the measurement evidence. |
| M2 | Oracle accepted the prefix of a verdict rather than the verdict contract | `corpus/knowledge/audit-r11.md:157,376-396` (BANANA wrapper 28/28) | Q8; new Q26 | Validate full vocabulary, cardinality and rc agreement; reject malformed wrappers while preserving the actual lane-behavior suite. |
| M3 | “Regenerated from canonical seed” was asserted without a correctly normalized byte comparison; L1 then copied presentation indentation before ReviewPromotion caught it | `corpus/lessons/round-12-verifier-spotcheck.md`; round-13 `.ufo/waves/round-13/build/ReviewPromotion.md`; canonical `kimi-shokunin/templates/mint/SHONEN.md:7-14` | none; new Q28 | Compare with the unindented canonical template content after name substitution, not the raw Markdown code block; restore ordinary checklist bytes and keep every box unchecked. |
| M4 | Scalar calibration/adjacency were over-credited beyond re-derivable evidence | `SCORECARD.md:651-655`; non-author `round-12-verifier-spotcheck.md` | Q20/Q21/Q25 | Keep calibration at 5 and adjacency at 6; no scalar credit for unclaimed repairs. Round-12 corrections are honored, not silently rewritten. |
| M5 | Routed override-token validation remains outside the selected cutovers | `LOG.md` round-12 entry: sentinel LOW `MORI_ROSTER_LANES` tokens; `.ufo/waves/round-13/build/PriorReview.md` | Q3/Q9/Q25 | Not represented as fixed: roster override validation is retained as a named residual, because this round's production edits are journal classes and exact-author membership. No token-safety capability is claimed. |
| M6 | Field-restricted output was mistaken for structured selection | `kill-classes-by-message-id-r12.md:3,14,17`; `kernel-oom-line-attribution-r12.md:3,15-17`; `.ufo/waves/round-13/build/ReviewSources.md` | Q15/Q25 | Append errata distinguishing `--grep` MESSAGE matching from MESSAGE-free output; retain old samples as historical text-selected records, not as a structured victim gate. |
| M7 | New harness parsed an invented FINDING schema and rejected correct census evidence | `.ufo/waves/round-13/evidence/regressions-after/evidence.json` (2 C1 failures); `runs/c1.primary.stdout:11-15` has `severity=info obs=` | Q2/Q20 | Repair only the FINDING regex and add a pure test using the actual emitted syntax; retain the red run and remeasure the same suite. |
| M8 | Static expected selftest total omitted four assertions | `.ufo/waves/round-13/build/CensusFix.md` predicts 87; `.ufo/waves/round-13/evidence/census-selftest.json` observes 91/91 | Q20 | Active SKILL/score/report totals use the observed tally; preserve the seat's prediction as a prediction, not rewrite it into an observation. |

## Gate

Admission bar: `corpus/QUALITY.md` criteria 1–28. Lane-dispatched seats are advisory, never the independent non-author verifier. A fresh outside reviewer must still sample at least one admit and one reject after landing; no outside round-13 result is pre-claimed.

| candidate | decision | reason |
|---|---|---|
| Explicit structured journal class counts with independent source scopes | admitted subject to the committed behavioral measurements below | S013/S014/S015; units and error states remain explicit; Q2/Q3/Q15/Q16. |
| Capture-safe author membership and full oracle final-verdict checking | admitted subject to the committed behavioral measurements below | S031 and audit F01/F02; Q6/Q7/Q8/Q26/Q27. |
| `fe6faa94…` count means unique kernel kills or fleet-caused kills | rejected | It counts unit notices, not kernel victim records; host scope does not prove fleet membership (Q16/Q18). |
| Re-pin old drift baseline merely to make a red run green | rejected | Classification and explicit reason are required (Q10); no freshness claim this round. |
| Lane's own swarm reviews certify promotion or outside discernment | rejected | `LEARNING.md` outside-author rule; SHONEN remains unchecked. |

### Source registry changes

Two new rows S035/S036 are added for the opened process-exit/unit-result catalog scope and its primary emitter. Existing rows change only permitted mutable cells:

- S013 used-by: `corpus/knowledge/kill-classes-by-message-id-r12.md, corpus/knowledge/userspace-oom-killers-r12.md` → the same two paths plus `corpus/knowledge/structured-journal-scopes-r13.md`.
- S014 and S015 used-by: `corpus/knowledge/kill-classes-by-message-id-r12.md, corpus/knowledge/kernel-oom-line-attribution-r12.md` → the same two paths plus `corpus/knowledge/structured-journal-scopes-r13.md`.
- S031 status: queued → mined; used-by: `—` → `corpus/knowledge/verdict-contract-r13.md`.
- S035 is new: code/A/mined, opened 2026-10-20, recheck on-release, used-by `corpus/knowledge/structured-journal-scopes-r13.md`; it does not rewrite S013's immutable scope/anchor.
- S036 is new: code/A/mined, opened 2026-10-20, recheck on-release, used-by `corpus/knowledge/structured-journal-scopes-r13.md`; its primary emitter confirms EXIT_CODE plus decimal EXIT_STATUS rather than relying on message wording.
- No recheck cell changes. Original opened dates remain source-row provenance; this round's reopening records live with the source seats under `.ufo/waves/round-13/build/` and the appended access table.

Initial census and validation: `.ufo/waves/round-13/sources-before.json`. Row count 34; A31/B2/C1; mined12/queued21/rejected1; validation exit 0. Final counts and measured verdicts are appended after integration rather than invented here.

### Round-12 outside review learned

The outside admit/reject sample agreed (`round-12-verifier-spotcheck.md:8-17`; `round-12.md:180-184`). Its score and SHONEN corrections are retained. Q28 turns the untested SHONEN equality assertion into a falsifiable check; the source hierarchy and no-causal-overclaim rules remain intact. The prior runtime cost is a disclosed cost, not a reason to shrink the declared lane universe.

### Reopened authorities (2026-10-20)

| row | URL | accessed | located quote (≤25 words) | location / opening evidence |
|---|---|---|---|---|
| S013 | https://raw.githubusercontent.com/systemd/systemd/cf8ebfc6159cf0b3b99aa9a0164ccb07c4c9c5af/catalog/systemd.catalog.in | 2026-10-20 | “Subject: A process of @UNIT@ unit has been killed by the OOM killer.” | pinned catalog:604–605; `.ufo/waves/round-13/build/CatalogSource.md` |
| S014 | https://www.freedesktop.org/software/systemd/man/latest/journalctl.html | 2026-10-20 | “A comma separated list of the fields which should be included in the output.” | Output Options → `--output-fields=`; `.ufo/waves/round-13/build/JournalSource.md` |
| S015 | https://www.freedesktop.org/software/systemd/man/latest/systemd.journal-fields.html | 2026-10-20 | “not supposed to be parsed for metadata.” | User Journal Fields → `MESSAGE=`; `.ufo/waves/round-13/build/FieldsSource.md` |
| S031 | https://man7.org/linux/man-pages/man7/pipe.7.html | 2026-10-20 | “a write(2) will cause a SIGPIPE signal to be generated for the calling process.” | I/O on pipes and FIFOs; `.ufo/waves/round-13/build/PipeSource.md` |
| S035 | https://raw.githubusercontent.com/systemd/systemd/cf8ebfc6159cf0b3b99aa9a0164ccb07c4c9c5af/catalog/systemd.catalog.in | 2026-10-20 | “The process' exit code is '@EXIT_CODE@' and its exit status is @EXIT_STATUS@.” | pinned catalog:575; process-exit entry :568–575, unit-result entry :561–566; `.ufo/waves/round-13/build/ClaimAttack.md` |
| S036 | https://raw.githubusercontent.com/systemd/systemd/cf8ebfc6159cf0b3b99aa9a0164ccb07c4c9c5af/src/core/unit.c | 2026-10-20 | `LOG_ITEM("EXIT_STATUS=%i", status),` | `unit_log_process_exit`, pinned source :6355–6392; L1 primary-source opening, class source dossier `ClaimAttack.md` |

Tooling: PipeSource installed `core/man-pages` version `6.19-1`, official pacman channel (`sudo pacman -S --needed --noconfirm man-pages`), to inspect the local authoritative pipe manual. No full-system or partial upgrade is claimed. Source content is evidence, not instructions to enable services or change host state.
