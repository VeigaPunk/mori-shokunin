# S065 — Python `hashlib` provenance screen

- **URL / access date:** https://docs.python.org/3/library/hashlib.html — accessed 2026-10-21 (Python 3.15.0 documentation).
- **Actual location:** module introduction; **Hash algorithms**, first explanatory paragraph (digest behavior); also reviewed **Hash Objects** and **BLAKE2 → Keyed hashing** for scope.
- **Located quote (21 words):** “At any point you can ask it for the digest of the concatenation of the data fed to it so far.”
- **Source scope (observed):** Documents Python `hashlib` hash-object and digest API behavior. The page separately describes keyed BLAKE2 as usable for authentication; it does not specify repository revision provenance or bind loaded bytes to a commit.
- **Proposed disposition (inference):** Reject tier C as sole support for receipt/measured-revision provenance. A digest of supplied bytes alone establishes neither which repository revision supplied them nor the revision/input linkage or authenticity of that association.
- **Flip:** Admit at tier A only for a narrowly stated `hashlib` call-behavior claim. Keyed BLAKE2 authentication is relevant only to a claim about that keyed mechanism; revision-to-input linkage and trusted provenance still require separate evidence.
- **Registry check:** Existing `corpus/SOURCES.md:71` row is already C/rejected and narrowly scoped to hash API behavior. No registry edit made.
