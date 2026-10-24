# FreezeMetadata scoped report

Changed files:
- `.ufo/worktrees/round-19/FreezeMetadataSparse/tools/mori-freeze-order.py`
- `.ufo/waves/round-19/build/FreezeMetadata.md` (this report)

Implemented C2 in the assigned checker. `--rev` is optional for backward compatibility; without it, evaluation remains available and the receipt explicitly marks provenance `unbound`. With it, the checker resolves a full commit OID, requires the register and any supplied corrections file to resolve inside the repository and match the exact Git blob bytes at that commit, and returns exit 2 with a safe `input-revision-mismatch` error when that cannot be established. The input bytes are read once, hashed before parsing, and the same bytes are parsed. The executing script receives its own byte digest; that digest does not claim the script is present at the measured revision.

Receipts carry the measured revision, register/corrections/script SHA-256 digests, command argv, and original tip-override strings; claim rows carry resolved base/tip OIDs when resolvable. Existing verdict labels, topology rules, and exit classifications were retained. Invalid or unknown `--rev` returns exit 2 without echoing its value.

Source evidence (path:line + class):
- `tools/mori-freeze-order.py:61-85` — revision resolution and repository root.
- `tools/mori-freeze-order.py:125-159` — one-read hashing, measured-revision blob match, then parsing.
- `tools/mori-freeze-order.py:170-233` — register/corrections loading and digest propagation.
- `tools/mori-freeze-order.py:249-342` — resolved claim OIDs, verdict evaluation, and receipt metadata.
- `tools/mori-freeze-order.py:361-412` — bound/unbound handling and safe exit-2 errors.
- `tools/mori-freeze-order.py:675-703` — optional `--rev` and exact command argv capture.

Checks: no tests, builds, lint, formatting, smoke runs, or verification runs were performed; the parent owns those gates. LSP was unavailable in the exposed toolset. No additional blocker identified.
