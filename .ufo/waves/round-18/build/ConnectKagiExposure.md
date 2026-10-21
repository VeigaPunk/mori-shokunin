# C1 connector scan — Kagi/Mori privacy boundary

## Axes and bounded finding

- **Improves:** C1 adjacency/privacy retention and ownership clarity. The useful move is to reuse Kagi's credential-minimization precedents while making Mori's new criterion explicitly cover the broader class of private session/document/config context in Mori's own committed handoffs.
- **Unaffected:** C2 freeze/calibration and C3 dispatch-payload binding; this scan found no reason to change either contract.

## Evidence (read-only)

- Mori's round-18 contract makes C1 a gate over committed private-context retention, requires minimization of three routed build reports plus repeated mentions, and explicitly says history is not rewritten and exposure assessment remains operator/Kagi-owned (`.ufo/waves/round-18/contract.md:9-13,24-29`). The tool contract limits findings to path, line, class and SHA-256, without matched text (`.ufo/waves/round-18/contract.md:52-58`).
- Frozen C1 policy defines the classes, required-redaction paths, allowlist boundary and a known limit: regex hits are a recall floor, not a privacy proof (`.ufo/waves/round-18/frozen/c1-policy.json:1-29`). The frozen population stores per-hit `line_sha256` fields (`.ufo/waves/round-18/frozen/c1-population.json:12-17`); no matched source text is reproduced here.
- The non-author routing is explicit: the Mori repair is to minimize committed handoff material, and a scoped summary/hash can retain provenance without copying private context; exposure assessment of already-pushed history is operator/Kagi-owned, no real credential compromise is asserted, and the closure authorizes no rotation, deletion of another owner's session copy, or history rewriting (`corpus/lessons/round-17-verifier-spotcheck.md:390-397`).
- Kagi's province is secrets/vault operations and it refuses cross-domain work rather than absorbing it (`../kagi-shokunin/PROVINCE.md:3-6`). Its skill forbids putting secret values and secret-reference paths in durable artifacts (`../kagi-shokunin/SKILL.md:14-17`). Its QUALITY bar QA5 forbids credential material in admitted knowledge, including examples (`../kagi-shokunin/corpus/QUALITY.md:24`).
- Kagi already has a directly relevant reporting precedent: transcript findings are reported as hit lines/counts, never matched rows; any classification uses bounded metadata rather than copying text into an artifact (`../kagi-shokunin/SKILL.md:454-455,507-510`). Its hash policy also warns that a committed SHA-256 of a low-entropy private file can be an offline confirmation oracle (`../kagi-shokunin/SKILL.md:220-227`).

## Ownership split

- **Kagi:** assess whether already-pushed material is credential/secret material and advise on secret exposure and any source-side rotation/revocation. Kagi's domain and rotation guidance support that boundary (`../kagi-shokunin/PROVINCE.md:3-6`; `../kagi-shokunin/SKILL.md:406-420`).
- **Operator, informed by Kagi:** decide whether any already-pushed history should be rewritten. The routed lesson explicitly withholds authorization for rewriting; it does not make a Mori retention fix or a Kagi assessment itself a rewrite decision (`corpus/lessons/round-17-verifier-spotcheck.md:395-397`).
- **Mori:** reduce and measure retention in Mori-owned tracked evidence, perform the whole-tree repeat sweep, and define a minimization criterion for Mori's durable handoffs. The C1 metric and required-redaction/allowlist rules are local retention controls, not a credential-compromise assessment (`.ufo/waves/round-18/contract.md:24-29`; `.ufo/waves/round-18/frozen/c1-policy.json:17-29`).

## Exact handoff line for Mori's report

> Operator/kagi owns exposure assessment for already-pushed history; no real credential compromise is asserted and this closure does not authorize rotation, deletion of another owner's session copy, or history rewriting.

## Reuse versus new criterion

**Reuse Kagi's rules as precedent, but do not substitute them for the required Mori criterion.** Kagi has a rule/criterion for durable-artifact minimization of *credential material* (SKILL hard rule and QUALITY QA5), and a count/metadata-only precedent for sensitive transcript findings (SKILL reporting rule). These are narrower than C1's private-context classes, which include non-credential session, document and configuration references. No inspected Kagi rule/criterion states a general retention policy for all such private context in another lane's committed handoffs. Mori should therefore add the named lesson/QUALITY criterion required by C1 and cite Kagi QA5, the durable-artifact rule, and the transcript reporting precedent rather than re-deriving those narrower controls.

## One bounded move, risk, and verification

**Move:** In the new Mori criterion, distinguish retention of Mori-owned committed context from Kagi's secret-exposure assessment, and state that hashes are provenance aids—not a universal privacy guarantee. This composes Kagi's existing no-credential-in-artifacts/report-by-metadata rules with C1's wider class without changing the frozen C1 interface or taking on Kagi's domain.

**Risk/contradiction:** C1's frozen population and tool interface retain per-line SHA-256 identifiers (`frozen/c1-population.json:12-17`; `contract.md:52-58`), while Kagi warns that hashes of low-entropy private material may enable offline confirmation (`../kagi-shokunin/SKILL.md:220-227`). Thus “hash instead of text” reduces disclosure but cannot be claimed to eliminate it. Keep hashes within the already-declared C1 provenance/reporting boundary; do not treat them as proof that material is safe or as a substitute for operator/Kagi exposure assessment. The C1 policy itself also says its regex metric is not a privacy proof (`frozen/c1-policy.json:28-29`).

**Verification performed:** read-only reads/searches of the round-18 contract and frozen C1 inputs, Mori's routed lesson and province, Kagi's `PROVINCE.md`, `SKILL.md`, and `corpus/QUALITY.md`. No shell commands, tests, selftests, external URLs, or tool installs were used; command exit codes and URL access dates are therefore not applicable. No private source text or secret value is included in this report.
