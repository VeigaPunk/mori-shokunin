# AuditHash — C1 raw-byte digest boundary

## Finding — Important acceptance gap: the proposed digest mutant does not isolate byte hashing

This is a pre-implementation test-design finding, not a confirmed defect in the auditor: `tools/mori-evidence-loss.py` was absent at the specified path, and no lane-local copy was found. No runtime verdict is available.

The contract requires SHA-256 of evidence **bytes** and says stale evidence must not resolve a row (`.ufo/waves/round-21/contract.md:14`). The proposed `digest-mismatch` probe starts with committed evidence and records its revision and hash (`.ufo/waves/round-21/build/MutDigestTrust/proposed-probe.py:99-145`), then appends one legal whitespace byte to the evidence file after that revision was captured, without updating the provenance revision or digest (`:204-214`). That mutation is changed raw content with the original declared digest, but the reference also still names the pre-mutation commit. A detector can reject based on revision/current-file disagreement, so this probe can pass without demonstrating that the digest check hashes the evidence bytes rather than a normalized projection.

Concrete counterexample: use the fixture's canonical disposition JSON bytes `B`, with recorded digest `SHA256(B)`. Commit `B + b" "` as the disposition file in a new evidence revision and point the provenance `revision` at that commit, but leave `sha256` equal to `SHA256(B)`. JSON parsing yields the same object; serializing that object with the fixture's `json_bytes` normalization recreates `B`, so a verifier hashing the normalized projection sees the recorded digest and can accept/count the disposition as disposed. A raw-byte verifier sees `SHA256(B + b" ") != SHA256(B)` and must mark the evidence invalid, leave the row not disposed, and keep `pin_allowed=false`.

Smallest safe change: in the auditor, read each evidence file once, compare the declared digest with SHA-256 of those exact raw bytes, and only then parse those same bytes; never hash a parsed/canonicalized projection. In the probe, keep the trailing-whitespace mutation but make it a committed evidence revision and update the provenance revision to that revision while deliberately retaining the old digest. Preserve a separate valid pristine control. This removes stale-revision disagreement as an alternate reason for rejection and makes the test discriminate raw-byte hashing from normalized-projection hashing.

## Residual risk and verification gaps

- The canonical auditor and a lane-local implementation candidate were not available, so implementation behavior is unknown; this report does not claim the counterexample was accepted by running code.
- `.ufo/waves/round-21/build/MutDigestTrust.md:3,48-49` records the proposal as unexecuted. I did not run it, tests, builds, linters, a census, or a pin.
- No LSP device is mounted (`xd://lsp` lookup returned “No such tool”), so status/references/definition/diagnostics could not be queried; no text-search output is offered as semantic proof.
- No tools were installed or updated. No production files were changed.
