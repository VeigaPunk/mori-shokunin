# SrcRejectHash — S065 re-screen for round 22 (C1 retention reconciliation)

**Verdict: re-reject S065 as sole support** for any C1 claim about receipt provenance, measured-revision linkage, input authenticity, or privacy clearance. Retain S065 only for narrow `hashlib` call-behavior claims. No registry edits were made.

## Observed

- **Source opened:** https://docs.python.org/3/library/hashlib.html, fetched 2026-10-21. The page title now reads "Python 3.15.1 documentation". Existing S065 row (`corpus/SOURCES.md:71`) records "Python 3.15.0". This is version drift in the anchor cell, not a change in scope. Not edited.
- **Primary located quote (21 words):** "At any point you can ask it for the digest of the concatenation of the data fed to it so far" — section **Hash algorithms**, first paragraph (`#hash-algorithms`).
- **Supplementary located quotes (each ≤25 words, used for the privacy and authentication boundary):**
  - "Naive algorithms such as `sha1(password)` are not resistant against brute-force attacks." (12 words) — section **Key derivation** (`#key-derivation`).
  - "Keyed hashing can be used for authentication as a faster and simpler replacement for Hash-based message authentication code (HMAC)." (19 words) — section **BLAKE2 → Keyed hashing** (`#keyed-hashing`).
- **Existing S065 state (observed in the repo at HEAD `306e06ecd02e0ea8e544fbd30d1ff7e7359c581e`; last commit touching `corpus/SOURCES.md` is `a8442a018aa9c51b21b92c3ce3b17736317375b1`):**
  - `corpus/SOURCES.md:71` has tier C, status `rejected`, and the claim "authoritative only for hash API behavior". Its flip is "admit A for a narrow hashlib call-behavior question, never for revision linkage or authenticity without separate evidence."
  - `corpus/lessons/round-19.md:43` records the Gate quote from the module introduction and the reject-C disposition. Lines 131–133 record Main's independent agree-reject-C spot-check.
  - Prior screens `.ufo/waves/round-19/build/SrcHashlibReject.md` and `.ufo/waves/round-19/falsify/SourceS065.md` reached the same rejection. The latter notes that the keyed-hashing section is not listed in the row's anchor cell.

## Why the digest API cannot independently establish provenance

The digest API cannot prove where bytes came from. This follows from the documented API semantics; it is an inference, not a hashlib statement about Git.

1. **The digest depends only on the bytes passed in.** The primary quote defines the digest as a function of "the data fed to it" and nothing else. A SHA-256 over receipt, policy, or allowlist bytes does not record which repository, path, blob, or commit those bytes came from. The C1 contract requires that `measured_revision` be a full commit, be an ancestor of `--rev`, and be the source of the blobs read through `git -C` plumbing. That linkage comes from Git object resolution (S064 scope), not from a hash.
2. **An unkeyed digest authenticates nothing.** The page says authentication requires keyed hashing or HMAC. The contract's receipt digests (loaded input SHA256, executing tool SHA256, `line_sha256`) are unkeyed. Anyone who can write the receipt can recompute them for substituted bytes. A matching digest shows that the bytes are consistent with each other; it does not show who produced the receipt or when. This matches the contract's open-debt note: "a source hash is not secrecy/authentication."
3. **Recomputation agreement is not origin.** The C1 tool recomputes the hit multiset and checks it against the receipt. Exit 0 (`RETENTION_RECONCILED`) means the accounting agrees for the bytes that were read. It does not establish that those bytes were the ones originally measured beyond what the Git ancestry and blob-equality checks show.

## Why the digest API cannot establish privacy clearance

This section is also inference, grounded in the supplementary Key derivation quote and the contract.

1. **A digest-only identity can still reveal content.** The page warns that a naive digest of a low-entropy secret can be brute-forced. Hit identities `(path, line, class, line_sha256)` hash matched lines without a salt. When a line matched a narrow R-class regex, an attacker can enumerate candidate lines and test them against `line_sha256`. Emitting digests instead of matched text reduces direct exposure, but it is not a guarantee that the content stays secret.
2. **Hashing says nothing about whether private data is absent.** A digest neither detects nor removes private data. The hit population is determined by the frozen policy regexes and the tracked-blob walk. Hashing only labels hits that were already found, so nothing about the digest can bound the hits that were missed. A zero delta or zero new-hit count is therefore not clearance (the contract states this explicitly). The retained real result must still show four unallowlisted hits with `privacy_clearance=false`.
3. **Equal digests across two populations don't certify either one.** The contract's root lesson is that population equality is checked by identities and explicit exclusions, not by count subtraction. Digest equality compares identities only. Correct classification, allowlist semantics, and the policy-source exclusion (raw 95, including 5 policy-source hits, against scanner 90) are separate questions.

## Disposition

- **S065 must not be cited as the sole support** for any C1 claim about receipt provenance, `measured_revision` linkage, input-tree equality, authenticity, or `privacy_clearance`. Such claims require separate evidence: Git revision semantics (S064, which this round reopened) and the tool's own ancestry and blob-equality checks. Even with that evidence, no source authenticates the absence of private data.
- **Permitted narrow use, tier A only, as the existing flip states:** documenting `hashlib.sha256` and `hexdigest()` call behavior, for example the deterministic digest of fed bytes used to compute `line_sha256` and the loaded-input SHA256 fields.
- **Registry:** unchanged. Row 71 already carries C/rejected with the correct narrow scope. These are candidate notes for L1 only, and no edit has been made:
  - The anchor cell's "3.15.0" now differs from the live page (3.15.1).
  - The anchor does not list `#keyed-hashing` or `#key-derivation`, which are the sections relevant to the authentication and privacy boundary.

## Remaining unknowns

- Whether any r21 receipt used keyed hashing: not observed. The contract describes only unkeyed SHA256 fields.
- The entropy of the actual retained hit lines, and so how practical brute-forcing `line_sha256` would be: not assessed. No matched text was read.
- Whether "outside closure" admits this round's re-screen: not decided here.

## Exercised actions

- Fetched the hashlib page once.
- Ran read-only `git rev-parse` and `git log` on the mori-shokunin repo.
- Read `corpus/SOURCES.md:71`, `corpus/lessons/round-19.md`, the two round-19 S065 reports, and the round-22 contract.
- No tests, builds, installs, registry edits, or draft artifacts. No tools were installed.
