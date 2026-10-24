# S065 re-rejection review — round22 lesson Gate (fresh falsification, static only)

**Seat:** MoriR22.SourceReject. **Scope:** review the round22 re-reject-C-as-sole-support decision and its ≤25-word located quote; source re-open performed. **Bounds honored:** read-only, no executions, no production edits, no delegation; shipping source re-verified directly rather than repeating build-wave notes.

## Verdict

**Agree — the round22 re-rejection of S065 as sole provenance/privacy authority is correct, and the located quote is verbatim, within the ≤25-word gate, and accurately located.** No finding overturns the decision. Details by check below.

## Quote verification (re-opened source)

- Round22 lesson claim (`corpus/lessons/round-22.md:27`): quote from "Hash algorithms, first paragraph" — *"At any point you can ask it for the digest of the concatenation of the data fed to it so far."*
- **Word count: 21 ≤ 25.** (At/any/point/you/can/ask/it/for/the/digest/of/the/concatenation/of/the/data/fed/to/it/so/far.)
- **Verbatim:** yes, in both the live page and the pre-update snapshot; the live page renders "digest" with emphasis markup (`*digest*`), which is formatting, not word content. The surrounding sentence continues "using the `digest()` or `hexdigest()` methods" — the ≤25-word excerpt cuts cleanly inside it.
- **Location accurate:** the sentence is the last sentence of the first paragraph of the `## Hash algorithms` section (`#hash-algorithms`), exactly as the lesson records.
- **Version drift handled correctly:** live page is now Python **3.15.1** documentation (last updated Oct 21, 2026 13:02 UTC); the immutable anchor cell (`corpus/SOURCES.md:71`) pins **Python 3.15.0, opened 2026-10-21**. A Wayback capture of 2026-10-20 12:06 UTC (`web.archive.org/web/20261020120616/...`) identifies as **Python 3.15.0** and contains the identical paragraph — so the original anchor was accurate at open time, and `corpus/lessons/round-22.md:29` ("Immutable original version/anchor cells are not rewritten because a live page version changed") is the right handling. The quote survives verbatim across both versions, so the re-rejection is grounded on the current page, not only the archived anchor.

## Decision review against adverse in-page evidence

The decision "Re-reject C as sole provenance/privacy authority" survives the strongest material the page offers:

1. **BLAKE2 "Keyed hashing"** (`#keyed-hashing`): "Keyed hashing can be used for authentication as a faster and simpler replacement for HMAC... securely used in prefix-MAC mode", plus a sign/verify cookie example. This supports at most a keyed-message-authentication mechanism claim for shared-key holders. It does not associate supplied bytes with a repository revision, identify the repository supplying bytes, or establish that loaded inputs match a committed tree. The round22 lesson separately rejects "a digest as secrecy/authentication" (`corpus/lessons/round-22.md:31`), so even keyed mode cannot upgrade S065 to authority here.
2. **Collision warning** (module Warning box): MD5/SHA1 "have known hash collision weaknesses" — digests are not injective, so digest equality is weaker still as input-identity proof. Reinforces the rejection.
3. **`usedforsecurity`** (Changed in 3.9): `False` "indicates that the hashing algorithm is not used in a security context" — the docs themselves treat hashing as usable outside security contexts.
4. **Tree hashing / `file_digest` / SHAKE**: file- and tree-organization hashing helpers; no revision, ancestry, or committed-tree semantics anywhere on the page.

The r19 falsification's conclusion (`.ufo/waves/round-19/falsify/SourceS065.md`) is unchanged by the fresh re-open: keyed authentication remains a narrow mechanism claim, never revision linkage. The registry disposition (`corpus/SOURCES.md:71`, status `rejected`, scope "authoritative only for hash API behavior", flip = tier A only for narrow hash-call behavior) and the bounded-search records (`corpus/SOURCES.md:113,119`) are internally consistent: S065 status/recheck/used-by unchanged in round22; only S064's used-by changed (`corpus/lessons/round-22.md:29`).

## Shipping-source consistency (verified against current `tools/mori-retention-reconcile.py`)

The rejection's rationale is embodied, not contradicted, by the current shipping source:

- **Digests as identity only.** `digest()` = sha256 hexdigest (line 31). Uses: per-line `line_sha256` in scan (line 151), `policy_sha256` cross-check (line 192), and evidence metadata `inputs_sha256`/`tool_sha256` (line 232). No code path treats a digest as establishing revision linkage, authenticity, secrecy, or clearance.
- **Provenance comes from git plumbing, not hashing:** `resolve()` via `rev-parse --verify --end-of-options <rev>^{commit}`, wrapper re-peel, `merge-base --is-ancestor` (R14), byte equality of policy/allowlist at measured vs input revision (R15/R16), and independent recount over the measured tree.
- **The one digest-equality gate** (`receipt_policy_digest`, line 192) compares the receipt's claimed policy digest against bytes the tool itself loaded from a resolved git blob; a disagreement yields a mismatch difference (exit 1), never a pass or clearance. That is byte-identity validation within the retained A-flip scope ("hash API behavior"), not provenance-by-hash.
- **Explicit non-claims:** `receipt_authenticity: 'unattested'` (line 232) and hard-coded `privacy_clearance: False` (both `check()` line 233 and `selftest()`), matching the module docstring "Agreement never grants clearance" and the S065 rationale that a hash API does not authenticate provenance.
- **Population comparison is identity-based** (M1 fix): claimed vs actual multisets keyed on `(path, line, class, line_sha256)` (lines 129, 218–219) — receipt-side digest lies are caught by multiset inequality, consistent with the lesson's "compares exact path/line/class/digest multisets".

## Findings

**Blocking:** none.

**Minor/informational:**

1. *(info)* Live page moved 3.15.0 → 3.15.1 on the re-open date, adding/expanding the "File hashing" (`file_digest`) section and a "Deprecated since version 3.15" note. Correctly not folded into immutable cells per `corpus/lessons/round-22.md:29`; the quoted paragraph is unchanged in both versions (verified against the 2026-10-20 snapshot).
2. *(info)* The strongest adverse candidate (BLAKE2 keyed authentication) supports only a narrow keyed-MAC mechanism claim and is already outside the retained C scope; rejecting S065 as *sole* provenance/privacy authority remains exactly right even admitting that mechanism claim for other purposes.
3. *(info)* Any future S065 use must cite a fresh quote from the then-live page, since upstream can reword or remove the paragraph; the pinned anchor preserves only the original evidence, not the live page's persistence.

## Residual risk

- Upstream page churn is the only live risk to quote reproducibility; it is mitigated by the immutable anchor convention plus this round's snapshot confirmation.
- The Wayback capture used here is a public third-party archive retained as a verification aid in this report only; it is not lane evidence and does not modify any lane record.

## Verification gaps

- Static analysis only per bounds: the tool and its selftest were not executed; all shipping-source statements are from reading the current file at the cited lines.
- The exact 3.15.0-era read from round19 was not independently retrievable beyond the immutable anchor cell plus this round's archived snapshot; no discrepancy was found between them.

## Tooling directive record

No installs or updates were needed or performed (read-only web fetches and repo reads only). No pacman/uv/npm/cargo activity.

— MoriR22.SourceReject, 2026-10-21. Report path: `.ufo/waves/round-22/falsify/SourceReject.md` (this file; only write performed).
