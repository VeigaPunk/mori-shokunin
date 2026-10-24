# CritS262Scope — attack on oom-victim-context-r41.md (abstract-scope audit)

Round: 42 · wave: w1 · role: critic · tip under attack: 34b926730c30e0251e1aec531863d8355dc491f1
Target: `corpus/knowledge/oom-victim-context-r41.md` (admitted, S262/ROMA)
Located evidence: `corpus/evidence/sources-r42/S262.oa.json` (OpenAlex record, abstract_inverted_index reconstructed in full, 1,456 chars)

## Counterexample tested (the strongest posed by the assignment)

**Posed:** "the 6.9 s / 92.6 % figures trace to S268's full text, not the abstract."
**Result: FAILS.** The planted counterexample is refuted by the located bytes:

- `6.94 % throughput overhead across eight workloads` — verbatim in the abstract ("ROMA incurs only a 6.94% throughput overhead across eight workloads").
- `recovery within 6.9 s under up to eight concurrent attackers` — verbatim ("Under up to eight concurrent attackers … keeps recovery time within 6.9 seconds").
- `24-hour runs with up to 64 containers` — verbatim ("In 24-hour runs with up to 64 containers, ROMA remains stable …").
- `92.6 %` appears **nowhere** in the entry, the abstract, or the corpus. S268 is the *refused* tracepoints entry (lesson `round-42.md:16`, `refused-oom-tracing.md`), a different paper — the posed provenance is fabricated.
- No claim sentence relies on S268 or on the full text.

## Sentence audit — citation basis vs the located abstract

Load-bearing claim sentences all ground in the abstract:

| Lines | Sentence | Basis |
|---|---|---|
| 12–13 | "cgroup-scoped but not container-scoped" | PARTIAL — "not container-scoped" ✓ (located quote); "cgroup-scoped" is an inference — the abstract never says selection *is* cgroup-scoped |
| 15–17 | verbatim 「lack sufficient container context…」 quote | ABSTRACT — exact match to inverted-index reconstruction |
| 17–20 | co-located kill / unreclaimed shared resources → DoS | ABSTRACT — supported; drops the abstract's "malicious" qualifier (minor adversary→any widening); "kill" vs "disrupt" is redeemed by "avoids collateral kills" |
| 22–26 | eBPF monitoring + two lightweight LSM hooks; confine victim selection; proactive reclaim | ABSTRACT — near-verbatim |
| 26–28 | 6.94 % / eight workloads / 6.9 s / eight attackers / 24 h / 64 containers | ABSTRACT — verbatim (counterexample refuted above) |
| 30–40, 59–79 | lane analysis, probe shape, delivery paths | No S262 citation asserted — analysis sections, in-bounds |
| 44–50 | boundary bullets | Mostly accurate; see F3 below |
| 87–92 | adoption provenance (re-located 2026-10-24, paywalled) | ACCURATE — matches lesson M3 and `any_repository_has_fulltext: False` in the record |

## Findings — sentences whose citation basis is NOT the located abstract

- **F1 (provenance, real defect) — line 4 `source:` header.** Claims scope "Abstract and TLDR, as recorded by the publisher's Semantic Scholar record and by OpenAlex". Three faults in one line: (a) no TLDR exists in the deposited record — `S262.oa.json` has zero TLDR/summary fields; (b) "the publisher's Semantic Scholar record" is doubly false — Semantic Scholar is not the publisher (IEEE is), and the entry's own boundary records "Semantic Scholar lacks the DOI" (L46), i.e. the cited record does not exist; (c) duplicate authority — it contradicts the accurate L1 header ("Abstract, as carried by the publisher-deposited OpenAlex record"), leaving two live source claims.
- **F2 (same defect, scope line) — line 50.** "…scope of this entry is therefore the paper's own abstract and TLDR, as recorded by the publisher's metadata." Same phantom TLDR; OpenAlex is an index, not "the publisher's metadata".
- **F3 (minor, unanchored detail) — line 45.** `ieeexplore.ieee.org/document/11540439` — the document number 11540439 is not in the located record (`ids` = openalex + doi only). Harmless inside a fetch-failure remark, but unevidenced by the cited copy.
- **F4 (borderline) — headline "cgroup-scoped".** Inference presented inside the finding sentence; the abstract supports only the negative (lacks container context), not the positive cgroup-scoping claim.

Root cause is visible in `lessons/round-42.md` M3: the staged package was grounded on a Semantic Scholar recheck that stopped resolving ("DOI not in Semantic Scholar"); the lane re-grounded on OpenAlex — and line 1 is the corrected header while line 4 is the stale package-era header retained unmarked. False provenance, not false content: no knowledge claim traces to the phantom TLDR.

## Impacted axes

Provenance/authority (F1–F3), claim-vs-evidence scoping (QUALITY #2 anchored claim, #3 observation/inference separation, #46 stale-statement supersession). Claim substance axis: clean — every figure and every finding sentence resolves to the located abstract quote.

## Verdict under QUALITY — ADMIT, with a mandatory bounded erratum

Refusal is disproportionate. The refused sibling (S268 tracepoints) was refused because its *only* source was unreachable — nothing to locate. Here the source is located, the committed evidence copy verifies, the gate quote matches byte-for-byte, the recheck command reruns green (`grep -c 'lack sufficient container context'` → 1), and zero claim sentences depend on the phantom TLDR. The defects sit in provenance scaffolding, which QUALITY #4/#46 handle by append-only erratum, not rejection. The critic's posed counterexample fails on the evidence.

## Smallest safe correction (single erratum block)

1. Mark L4 `source:` line superseded by L1 (abstract only, publisher-deposited OpenAlex record) — removes the duplicate authority and the Semantic Scholar/TLDR claim.
2. L50 "abstract and TLDR … publisher's metadata" → "abstract, as carried by the OpenAlex record".
3. Re-word or annotate headline "cgroup-scoped" as lane inference (abstract supports only "lacks container context").
4. Drop or mark `document/11540439` unverified-by-record.

## Tools / methods

`read`, `grep` (registry row, decoy-figure sweep), Python json (inverted-index abstract reconstruction, TLDR/fulltext/location field probes). No installs; no writes outside this report. No secrets touched.

Report: .ufo/waves/round-42/w1/CritS262Scope.md
