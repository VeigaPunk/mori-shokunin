# HistoryScope — tip-only own-evidence vs pushed-history ownership (round 22)

Seat `MoriR22.HistoryScope` (scout, read-only). Scope: `PROVINCE.md` and the public evidence it
directly cites for own-evidence retention, checked against the round-22 contract. No
tests, builds, selftests, journal/session/config reads, installs or edits outside this file.

## Verdict

**No authority widening is required by the round-22 C1 contract.** Reading blobs at an
ancestor `measured_revision` for accounting is measurement of mori's own committed tree,
which mori already owns. It is not an exposure assessment of pushed history and gives no
authority to rewrite it. Four boundary risks need wording or implementation guards
(see "Boundary risks" below). Confidence: high on the ownership text; medium on the
risks, which concern code not yet written (`[INFERENCE]` where marked).

## Observed facts

- **Ownership text.** `PROVINCE.md:125-131` says mori owns the retention gate over its *own*
  committed evidence and redacts lane-authored copies at the tip only. Pushed history,
  exposure assessment, credential rotation and any history rewrite are **kagi/operator**-owned.
  The same split appears in:
  - `.ufo/waves/round-18/build/ConnectKagiExposure.md:17-20`: Kagi assesses pushed material;
    the operator decides any rewrite; Mori reduces and measures retention in Mori-owned
    tracked evidence.
  - `corpus/lessons/round-17-verifier-spotcheck.md:394-397`: a non-author closure that
    authorizes no rotation, deletion or rewrite.
  - `corpus/knowledge/evidence-minimization-r18.md:44-45`.
- **Measuring at historical revisions is already in scope.**
  - The existing gate resolves any `--rev` to a commit and scans `ls-tree -r` at that commit
    (`tools/mori-retention-gate.py:177-204`).
  - The frozen metric is measured "Before … at base; after at the measured round-18 commit"
    (`.ufo/waves/round-18/frozen/c1-policy.json:27`).
  - So "tip-only" limits *redaction* (mutation), not *measurement*.
- **Digests are already emitted.** The gate's result already emits per-hit
  `path/line/class/line_sha256` lists (`hits`, `unallowlisted_hits`, `allowlisted_hits`;
  `tools/mori-retention-gate.py:289-300`). The r21 receipt's stdout therefore already carries
  digest identities. A reconciliation that re-emits only recomputed identities adds no new
  disclosure class.
- **Hashes are not secrecy.** Line digests are provenance, not secrecy. A digest of a short,
  low-entropy line can be confirmed by guessing (`evidence-minimization-r18.md:41-43`;
  `ConnectKagiExposure.md:34`).
- **Inputs are byte-unchanged since the entering branch.** Read-only plumbing showed:
  - `77a5bbe8…` is an ancestor of HEAD `306e06ec…`.
  - `git diff 77a5bbe8 HEAD` is empty for `PROVINCE.md`, `tools/mori-retention-gate.py`,
    `c1-policy.json`, `evidence-minimization-r18.md`, `ConnectKagiExposure.md` and
    `corpus/evidence/retention-allowlist.json`.
  - The only changes are 7 added `.ufo/waves/round-22/` files plus `LOG.md`.
  - `tools/mori-retention-reconcile.py` is absent at HEAD, which is consistent with
    `before_kind: capability_absent`.
- **Digest bindings match.**
  - The contract blob's SHA-256 is `1658c390…321a1`, equal to `contract_sha256` in
    `.ufo/waves/round-22/frozen/requirements.json`.
  - The `c1-policy.json` blob's SHA-256 is `db06e981…3128`, equal to the policy SHA-256
    cited in the minimization knowledge.
  - `requirements.json` holds requirement IDs only. It has no ownership, history or
    clearance text.
- **Push status is not observable.** HEAD is detached with no resolvable `@{upstream}`
  (rc 128). Push status of any revision is not observable from the lane checkout.

## Boundary risks (no widening if held)

1. **Ancestry is not push status.** R13/R14 check that `measured_revision` is an ancestor of
   `--rev`. That is branch lineage only. The tool must not label any revision or hit as
   pushed, exposed or unexposed. Doing so would enter kagi/operator exposure assessment.
2. **"RECONCILED" is not clearance.** Exit 0 `RETENTION_RECONCILED` with
   `retention_state=red` must coexist with `privacy_clearance` as a **constant literal
   `false`**, never computed. The tool should also have no field implying history
   disposition (for example `history_clean`, `exposure`, `rewrite_needed`). The contract
   already requires `privacy_clearance=false`. `[INFERENCE]` A computed field could later be
   flipped by a refactor.
3. **Retroactive allowlisting.** R15/R16 forbid applying current policy or allowlist bytes to
   a historical revision, which is correct. Policy-source exclusion must remain exactly the
   supplied `--policy` path. It must never be applied as an allowlist row or a redaction, so
   the raw denominator stays authoritative. Otherwise a reconciliation could silently
   "dispose of" historical hits, which is a history-ownership claim.
4. **`--repo` is unrestricted.** Like the existing gate (`tools/mori-retention-gate.py:715`),
   `--repo DIR` accepts any repository. It cannot authenticate the repository's identity.
   Running it on a sibling lane would assess another owner's retention: out of province, so
   report it and do not absorb it. Selftest synthetic fixtures are fine. This is not new in
   round 22, but the round-22 knowledge or PROVINCE note should restate it.

Also: committing reconciliation output at the tip re-propagates per-hit digests of lines that
may already be redacted at the tip. This stays inside the declared C1 provenance boundary,
but committed summaries should prefer counts plus a multiset digest over per-hit lists. The
exception is the policy-path excluded identities, which are lane-authored regex text and
which the contract mandates.

## Suggested PROVINCE append (draft for L1; not applied)

> Round22: read-only receipt reconciliation recomputes retention accounting at an ancestor
> measured revision of mori's own repository. Reading committed history for accounting is
> measurement, not exposure assessment. Ancestry is not push status, and
> `privacy_clearance` is always false. Pushed-history exposure, rotation and rewrite stay
> kagi/operator-owned. Sibling repositories are out of province.

## Unresolved

- Whether the r21 receipt's 95/5/90/4 accounting reproduces is unmeasured here, pending L1
  integration.
- Remote or pushed state of `77a5bbe8`/`306e06ec` is unobserved.
- The reconcile implementation is unwritten, so risks 1–4 are requirements to check, not
  observed defects.

## Verification exercised

Read-only `git -C` plumbing only: `rev-parse`, `diff --stat`/`--name-status`, `ls-tree`,
`log`, `merge-base --is-ancestor`, `cat-file blob | sha256sum`. No tool installs or updates.
No tests, selftests or measurements were run.
