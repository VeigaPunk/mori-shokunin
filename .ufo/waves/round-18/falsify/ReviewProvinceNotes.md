# Round-18 Mori province boundary review

## Finding

No clear substantive absorption of Kagi's credential-custody ground, Kumitate's dispatch/orchestration, or Tsukuroi's package/boot diagnosis appears in the appended section. There are two wording defects and one handoff gap: (1) `kagi/operator-owned` does not distinguish analysis from action; (2) the C3 sentence's “one ledger row per whole-wave task call” is less precise than the frozen per-attempt contract; and (3) the package clause assigns diagnosis/interpretation but leaves recovery/remediation ownership unstated.

## Evidence and contradictions

- Mori limits the retention gate to its own committed evidence and says it redacts lane-authored copies at tip; its exposure/rotation/history clause groups Kagi and the operator together (`PROVINCE.md:125-131`). Kagi declares secrets, vault ops, and credential-hygiene evidence as its domain (`../kagi-shokunin/PROVINCE.md:3-6`), documents custody and rotation knowledge (`../kagi-shokunin/PROVINCE.md:62`), and states Kagi owns runtime auth and credential custody (`../kagi-shokunin/PROVINCE.md:64`). **Contradiction/ambiguity:** those sources support Kagi as the credential analysis/custody owner, but do not make Kagi the operator of a history rewrite or credential-state change. The slash formulation obscures that boundary; it does not establish that Mori has taken the work.
- Mori correctly says dispatch planning, slot acquisition, retrying, and adjudication are Kumitate/operator-owned, with slot-grant lines treated as evidence (`PROVINCE.md:134-138`). Kumitate declares orchestration and tooling, including OMP task/hub scope, and routes dispatch/routing semantics into its domain (`../kumitate-shokunin/PROVINCE.md:3-6,19-28`). However, the C3 sentence says “one ledger row per whole-wave task call” (`PROVINCE.md:134-136`), while the frozen schema requires one row per **task-call attempt**, including ordered attempts (`.ufo/waves/round-18/frozen/c3-ledger-format.json:5-19`). This is a contract/province wording mismatch, not evidence that Mori owns dispatch.
- The package correction says package/boot-chain interpretation stays Tsukuroi's (`PROVINCE.md:139-141`). Tsukuroi owns package state and boot diagnosis, but explicitly does not install, upgrade, remove packages, restart services, rebuild or boot; the operator remediates (`../tsukuroi-shokunin/PROVINCE.md:8-14,20-28`). **Gap:** the Mori sentence does not say who owns recovery/remediation. It does not explicitly assign recovery to Tsukuroi, so there is no direct contradiction in the active sentence.
- The L1 draft verdicts and triage are framed around claim metrics and privacy dispositions (`.ufo/waves/round-18/draft-verdicts.md:6-13`; `.ufo/waves/round-18/out-of-metric-triage.md:3-6,18-35`); they do not resolve these sibling ownership distinctions.

## Affected axes

- **Adjacency (primary):** clarify the Kagi/operator and Tsukuroi/operator handoff; no cross-lane ownership expansion is warranted.
- **Operability (secondary):** align the C3 description with the frozen attempt-row cardinality.
- **No observed effect:** calibration, depth, coverage, and freshness. This is a wording-only proposal, not a claim that any tool or runtime behavior changed.

## One bounded proposal: clarify the three ownership clauses in the round-18 section

Use wording along these lines:

1. Replace the end of the retention bullet with: “Mori's gate covers its own committed lane evidence only. Kagi owns credential-specific exposure, custody, and rotation **analysis**; the operator owns credential-state changes, exposure response, and any rewrite of pushed history. Mori neither assesses credential exposure nor performs those actions. Line digests are provenance, not a secrecy claim.”
2. Replace the C3 cardinality phrase with: “one ledger row per task-call attempt binds the committed payload digest to the observed result.” Retain the existing sentence that leaves planning, slot acquisition, retries, and dispatch adjudication with Kumitate/operator.
3. Replace the package sentence with: “Package and boot-chain diagnosis stays Tsukuroi-owned; package, service, or boot recovery/remediation remains operator-owned.”

These clauses preserve Mori's passive evidence role, Kagi's credential-analysis/custody boundary, Kumitate's dispatch authority, and Tsukuroi's read-only OS diagnosis while making the operator handoffs explicit.

## Risks and verification

- **Risk:** calling Kagi the owner of credential “rotation” without qualifying it could imply that it performs rotation. Keep the word tied to analysis/advice and reserve state-changing action for the operator. Likewise, do not let “boot recovery” imply that Tsukuroi performs the recovery.
- **Verification performed:** read-only comparison of the named province sections, the round-18 contract, frozen C1/C2/C3 inputs, and the L1 draft/triage. The C3 attempt-row wording was checked directly against the frozen schema. No commands, tests, or builds were run; no repository files other than this report were written. No tools were installed or updated.
