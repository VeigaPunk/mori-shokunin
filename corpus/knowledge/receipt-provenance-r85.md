source: S600 — https://reproducible-builds.org/docs/definition/, "Definitions", Reproducible Builds; pin `corpus/evidence/sources-r85/rb-definition-1.html:175-177` (the definition) and `:196-197` (the verification rule), sha256 `a558c89f5f27dffa69fd1dc49904179b60233bcfdfc64807abfe1acf37518ebb`.
verified-at: 2026-11-04
recheck: 365d

# Receipt provenance: a receipt is a claim a third party can re-derive (round 85)

Axes: calibration. The source grounds what "reproducible" and "verified by comparison" mean. The
receipt grammar in K3 is the lane's own frozen rule (`.ufo/waves/round-85/contract.md` P-C2), not a
claim attributed to the page: the page says nothing about receipts, counters, revisions as
provenance, or this lane. Measured on the pin, `receipt` and `attestation` occur 0 times each; the
word `revision` occurs once, and only as "a checkout from version control at a specific revision"
(a description of source code, not of a provenance binding).

## K1 — What the source defines

The definition sentence spans pinned raw lines 175-177. Its operative span (21 words) reads:

> given the same source code, build environment and build instructions, any party can recreate
> bit-by-bit identical copies of all specified artifacts

The property is a statement about **any party**, not about the producer. A build is reproducible
when someone who is not the author, given the same inputs, obtains identical output bytes. The page
adds that "the relevant attributes of the build environment, the build instructions and the source
code as well as the expected reproducible artifacts are defined by the authors or distributors", so
the claim's scope is exactly the artifact set those parties specified — an artifact outside that set
is outside the claim, and "reproducible" is not a whole-repository predicate.

Scope limit: the page defines build reproducibility. It defines no receipt, no revision-binding
scheme, no attestation format and no CI artifact, and names no tool or exit contract.

## K2 — Verification is byte comparison, realized as a digest

Pinned raw lines 196-197, 18 words:

> The reproducibility of artifacts is verified by bit-by-bit comparison. This is usually performed
> using cryptographically secure hash functions.

Three consequences, and one non-consequence:

- **A digest mismatch is decisive.** Two digests that differ are two byte strings that differ; the
  comparison has failed, and no prose about how a run went can restore it.
- **A digest match is decisive only up to the digest.** The source says the comparison "is usually
  performed using" a cryptographic hash. The hash is the customary *realization* of the byte
  comparison, not the definition of it. A matching digest may therefore be read as a byte match and
  as nothing stronger — not authenticity, not authorship, not absence of substitution at the source.
- **"Usually" is load-bearing.** The page does not make a hash the only admissible check; the lane
  chooses sha256 because a receipt must fit in text, and records that choice as the lane's, not the
  source's.
- **Not implied:** that the comparison ran here, that the producer is truthful, or that a receipt's
  other lines are true. Verification by hash binds **bytes**, not **execution**. This is the same
  standing "adaptive output forgery" limit the registry already names, unchanged by this entry.

## K3 — This lane's receipt grammar, and why each line exists

Frozen before data in `.ufo/waves/round-85/contract.md` P-C2 and graded by
`.ufo/waves/round-85/count-c2.py`:

```text
# cmd: <text>
# rev: <40-hex>
# limits: <text containing the word "limit">
# counter-sha256: <64-hex> <repo-relative path>       one line per bound path
# ---
<body: the frozen summary token, e.g. C1=met ...>
```

- `# cmd:` — what ran. Without it the body is an assertion with no subject.
- `# rev:` — the tree the bytes were read from; the counter requires it to resolve to the graded
  revision or an ancestor of it. A commit id alone is not enough (K2): it names a tree, not the
  bytes that were graded.
- `# counter-sha256:` — K2 applied. The digest of the named path **at that revision**, checked
  against `git show <rev>:<path>`. This is the line that closes the gap
  `.ufo/waves/round-84/w1/Mo84R03Record.md` §0 (b) names: a receipt that executes one copy of a
  counter while citing a revision holding different bytes asserts `met` about bytes nobody graded.
- `# limits:` — where the reading stops being a fact. A receipt with no limit line invites a reader
  to take its summary token as unconditional.
- `# ---` — one boundary between header and body, so a parser finds the summary token in the body
  without matching it in the header prose.

A receipt whose bound digest does not verify is a **mismatch**, not a weaker pass. The lane's frozen
defeat control is precisely a receipt naming the pre-arm counter bytes, and it must read
`C2=unmet ... bound=4 mismatch=1`; a receipt with no headers must read `C2=unmet headers=<receipt>`
rc 1. Neither is a soft reading, and neither is a pass.

What the grammar still does not do: it binds the bytes, not the run. A receipt whose hash verifies
still asserts that its `# cmd:` was executed against those bytes. A third party can re-derive the
byte comparison (K2) but must re-run the command to make the body a fact rather than a claim — which
is exactly what the round's own counters do when they grade a receipt.
