# SrcSlsaProvenance — C3 source screen (digest binding of an action to its inputs)

Seat: MoriR18Recovery.SrcSlsaProvenance (scribe, leaf). Access date: 2026-10-21. Read-only web reads only; no downloads, no files written outside this report. No tools installed or updated (none needed; reads used the built-in read tool).

## 1. Opened sources

| # | Exact URL opened | Document version / date as observed |
|---|---|---|
| P1 | https://slsa.dev/spec/v1.0/provenance | Page banner: "Version 1.2 is the current version." Predicate `https://slsa.dev/provenance/v1`. No publication date on page. |
| P2 | https://slsa.dev/spec/v1.0/verifying-artifacts | Same banner (v1.2 current). Steps 1–3 "Verifying artifacts". |
| P3 | https://slsa.dev/spec/v1.2/build-provenance | Current-version page; cross-check of P1 text (same BuildDefinition sentence and `externalParameters` bullet observed). |
| I1 | https://raw.githubusercontent.com/in-toto/attestation/main/spec/v1/resource_descriptor.md | Fetched from `main`; no version line in document. Commit not pinned. |
| I2 | https://raw.githubusercontent.com/in-toto/attestation/main/spec/v1/statement.md | Fetched from `main`; no version line in document. |
| I3 | https://raw.githubusercontent.com/in-toto/attestation/main/spec/v1/digest_set.md | Fetched from `main`; no version line in document. |
| I4 | https://raw.githubusercontent.com/in-toto/attestation/main/spec/v1/README.md | States `Version: v1.2`. |
| A1 (alternative, screened) | https://git-scm.com/book/en/v2/Git-Internals-Git-Objects | Pro Git 2nd edition, section 10.2 "Git Objects". |

Line numbers are not pinned: the rendered pages were read through the tool, so anchors are given as document headings and paragraphs. [INFERENCE] none of the located quotes below depends on a line number.

## 2. Located quotes (each ≤25 words; verbatim)

| Q | Source and location | Quote | Words |
|---|---|---|---|
| Q1 | P1, "### BuildDefinition", paragraph after the parameter example (same sentence present in P3, "### BuildDefinition") | "Metadata about those parameter values, particularly digests of artifacts referenced by those parameters, SHOULD instead go in `resolvedDependencies`." | 18 |
| Q2 | P1, "## Model", bullet on `externalParameters` | "In SLSA, these values are untrusted; they MUST be included in the provenance and MUST be verified downstream." | 18 |
| Q3 | P2, "### Step 1: Check SLSA Build level", numbered list "Given an artifact and its provenance", item 2 | "Verify that statement's subject matches the digest of the artifact in question." | 12 |
| Q4 | I1 resource_descriptor.md, "## Semantics", first bullet | "A descriptor that specifies a `digest` is assumed to refer to an immutable resource or artifact." | 16 |
| Q5 | I1, "## Semantics", first bullet (continuation) | "The field that consumers are expected to match the `digest` against is ultimately determined by the predicate type" | 18 |
| Q6 | I2 statement.md, "## Fields", `subject` entry | "Subject artifacts are matched purely by digest, regardless of content type." | 11 |
| Q7 | I3 digest_set.md, "### Guidelines" | "Two DigestSets SHOULD be considered matching if ANY acceptable field matches." | 13 |
| Q8 | I3, "### Guidelines" | "Consumers MUST only accept algorithms that they consider secure and MUST ignore unrecognized or unaccepted algorithms." | 16 |
| Q9 | I3, "## Fields" > "#### Supported algorithms" (first subsection, the standard-name list) | "for cases when the method of serialization is obvious or well known." | 12 |
| Q10 | I3, "#### `gitCommit`, `gitTree`, `gitBlob`, `gitTag`" | "The `gitTree` and `gitBlob` in particular can be used for arbitrary trees or files, even outside git." | 17 |
| Q11 (alt) | A1, section 10.2 "Git Objects", opening paragraph | "Git is a content-addressable filesystem." | 4 |

## 3. What it teaches mori (C3: bind a dispatch attempt to its exact inputs by digest)

1. An input is bound only by a digest computed over the exact bytes the verifier later re-hashes (Q3, Q6). For C3 that is the committed `dispatch_path` bytes, or the payload recomputation in `frozen/c3-ledger-format.json`, compared by digest rather than by path or wording.
2. Input digests belong in a separate, digest-bearing record, not in the parameter values themselves (Q1). The ledger's `payload_sha256`/`payload_bytes` fields are that record; the dispatch JSON stays the parameter object.
3. The payload is untrusted until verified against its digest (Q2). A binding proves the committed payload equals what the ledger hashed; it does not prove the task tool received those bytes. The frozen `known_limit` already says this. The spec supports keeping that limit explicit.
4. Digest matching is only as strong as the algorithm set a consumer accepts (Q7, Q8). Q7 ("ANY acceptable field matches") is a weakening: a verifier comparing a multi-entry digest set should require the named algorithm (`sha256`) it was built to check, not any single matching entry.
5. The serialization must be pinned for a digest to mean anything (Q9). The standard algorithm names are defined for cases where "the method of serialization is obvious or well known". C3's `payload_sha256` hashes `json.dumps(..., sort_keys=True, separators=(',', ':'), ensure_ascii=False)` bytes. That recipe is project-private and not a well-known serialization, so the spec does not endorse it. It is pinned by the frozen format file, which is what makes it verifiable [INFERENCE: stability across Python versions for this input class is not tested here].
6. Option for L1 to weigh (not a judgment): the spec defines `gitBlob` as the git object hash over `blob <size>\0<content>` (Q10). A `gitBlob` digest of the committed dispatch JSON would bind bytes without any custom serialization. It would be a cross-check beside `payload_sha256`, not a replacement, because the payload-identity recipe is what the ledger hashes today.

Caveat on P1: the page is the v1.0 document and carries a banner that v1.2 is current. Q1 and Q2 are confirmed in P3 (v1.2 build-provenance) for the BuildDefinition sentence and `externalParameters` bullet. Step 1 of P2 was not cross-checked on the v1.2 verifying-artifacts page (not opened) [INFERENCE: text unchanged].

## 4. Tier proposal

- Primary row (SLSA Provenance v1 + in-toto resource descriptor / statement / digest set): tier **A** (normative specification; RFC 2119 keywords; in-toto README states v1.2). Scope: digest-based identity of build inputs and subjects.
- Alternative (Pro Git, Git Objects): tier **C** for this question (tutorial; explicitly not a normative definition of object hashing; see §5).

## 5. Draft `corpus/SOURCES.md` registry rows (id left as S0xx; not edited into SOURCES.md)

Primary (admit):

`| S0xx | SLSA Provenance v1.0 — https://slsa.dev/spec/v1.0/provenance (with in-toto ResourceDescriptor, Statement and DigestSet: https://github.com/in-toto/attestation/blob/main/spec/v1/resource_descriptor.md, .../statement.md, .../digest_set.md) | spec | A | digest-based binding of build inputs and subjects to exact bytes | Provenance > BuildDefinition paragraph "Metadata about those parameter values…" (P1, cross-checked P3); Verifying artifacts > Step 1 item 2 (P2); in-toto ResourceDescriptor > Semantics; in-toto Statement > subject; in-toto DigestSet > Guidelines; in-toto README Version v1.2; P1 banner names v1.2 current; access 2026-10-21, no commit pin for in-toto main-branch files | Digests of artifacts referenced by parameters belong in resolvedDependencies, and a subject matches only by digest of the exact bytes; a DigestSet with ANY-field matching is weaker than a pinned algorithm check, and the serialization of hashed bytes must be pinned. | queued | 2026-10-21 | on-release | — |`

Alternative 1 (reject):

`| S0xx | Pro Git, Git Objects (2nd ed.) — https://git-scm.com/book/en/v2/Git-Internals-Git-Objects | book | C | content-addressable object storage as explanation of git hashing | section 10.2 "Git Objects", "Git is a content-addressable filesystem." | REJECTED for C3: tutorial-grade explanation, not a normative definition; its examples are SHA-1-only 2nd-edition material; the normative git-object digest (`gitBlob`/`gitTree`) is already defined by the primary row's in-toto DigestSet text, which itself notes git has no official internal-format document. Flip: a source giving the normative git object-format specification for SHA-256 repositories (not opened this round) would be admitted. | rejected | 2026-10-21 | 365d | — |`

## 6. Recheck commands (proposed; read-only, print nothing to disk; not run this round)

- `curl -fsSL https://slsa.dev/spec/v1.0/provenance | grep -c 'particularly digests of artifacts'` — expect `1`.
- `curl -fsSL https://raw.githubusercontent.com/in-toto/attestation/main/spec/v1/resource_descriptor.md | grep -c 'immutable resource or artifact'` — expect `1`. Main-branch fetch is unpinned; pin to a commit when the row is integrated.
- `curl -fsSL https://raw.githubusercontent.com/in-toto/attestation/main/spec/v1/digest_set.md | grep -c 'method of serialization is obvious'` — expect `1`.

## 7. Limits

- Only the quotes in §2 were located; no line numbers were observed for the rendered pages.
- The verifying-artifacts v1.2 page and the in-toto spec at a pinned commit were not opened.
- The alternative screen covered one candidate only; no broader search was run.
- No claim is made about whether the frozen C3 tool or ledger matches the cited text; that is a judgment for L1.
- Tools: none installed, updated or removed. The `read` tool was the only access path.
