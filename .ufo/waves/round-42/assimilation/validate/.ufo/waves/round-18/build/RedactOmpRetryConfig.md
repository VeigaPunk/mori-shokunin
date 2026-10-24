# RedactOmpRetryConfig — round-18 C1 repair draft for the round-17 OmpRetryConfig report

Seat: `MoriR18Recovery.RedactOmpRetryConfig` (leaf scribe, round 18 wave 1). Read-only except this report.
Routed by: `corpus/lessons/round-17-verifier-spotcheck.md:339-346` (non-author closure) and `:390-397` (routed defect 1). Policy: `.ufo/waves/round-18/frozen/c1-policy.json` (must_redact_paths entry).
Original: `.ufo/waves/round-17/build/OmpRetryConfig.md` at 29b0dc7, blob `eee6fbaf3f3cb5297d2209fd0e3ce8a4eeaabe73`, SHA-256 `d6340be91155b713e327f310f6b1f82eefe8746d46c6455b61fa8fb7392b2ec7` (223 lines, 12726 bytes).

## Verdict

Draft complete. The replacement body below keeps the seat identity, task, verdict-level conclusions, public-source citations, non-private counts and the [INFERENCE] label with its falsifier. It carries zero hits under all nine classes R1–R9 of `frozen/c1-policy.json`. The L1 integrates: this draft is not written to the original path, and no allowlist entry is proposed for it.

## Scan results

Method: classes loaded from `frozen/c1-policy.json` with `json.load`; each class regex applied with python `re.finditer` to the draft text (121 lines, 11839 characters) and, as a counts-only control, `re.search` per line on the original blob. No text from the original is printed here.

| class | name | hits in replacement | lines with hit in original blob (counts only) |
|---|---|---|---|
| R1 | session_identity | 0 | 0 |
| R2 | session_store_path | 0 | 0 |
| R3 | tool_output_artifact | 0 | 0 |
| R4 | private_document | 0 | 0 |
| R5 | shell_history | 0 | 0 |
| R6 | privileged_config | 0 | 0 |
| R7 | operator_config_ref | 0 | 5 |
| R8 | routing_table_key | 0 | 8 |
| R9 | session_record_value | 0 | 4 |

The gate (`tools/mori-retention-gate.py`) is not run here; this is the class-regex check named in the wave brief. The original blob's non-zero counts are the before evidence for its routed status; the file has no allowlist entry and must scan to zero.

## What was removed (categories only, no values)

- Operator configuration: every line number, key-name list for routing and fallback tables, role/model identifiers and candidate-list entries replaced by a summary (values withheld).
- Transcript-derived values: per-file recovery-class and note names replaced by counts; the three named dying-class sessions and the walked-chain sessions are counted, not named; the session-store root is not named.
- Session-record field names with values: removed; only field presence and counts are kept.
- Operator model catalog: referenced as a store, not by path or table contents beyond the read-only access mode.
- Kept: the seat identity, the verdict logic, the omp public-schema defaults and byte offsets into the installed binary, the public z.ai documentation citation (docs.z.ai api-code.md:31, accessed 2026-10-20), the omp engine-path code excerpts, and the [INFERENCE] label on §6.4 with its falsifier.

## Commands and tooling

- `git -C /home/vgpnk/Projects/shokunin/mori-shokunin show 29b0dc7:.ufo/waves/round-17/build/OmpRetryConfig.md` (read) — exit 0.
- `git -C ... rev-parse 29b0dc7:<path>` → `eee6fbaf3f3cb5297d2209fd0e3ce8a4eeaabe73`; `git -C ... show ... | sha256sum` → `d6340be91155b713e327f310f6b1f82eefe8746d46c6455b61fa8fb7392b2ec7` — exit 0.
- Read of `.ufo/waves/round-18/frozen/c1-policy.json`, `.ufo/waves/round-18/contract.md`, `corpus/lessons/round-17-verifier-spotcheck.md:322-350` and `:388-397` — exit 0.
- Python 3 stdlib scan (json, re, subprocess) as above — exit 0. No files written by the scan; no temporary files; no /tmp use.
- No installs, no upgrades, no VCS mutation, no journal query, no package-manager transaction. Tooling directive: nothing needed; none installed.

## Notes for L1

- The replacement is a full body with a provenance line: blob id and SHA-256 are the record; history is not rewritten.
- The original file must be overwritten by L1 with the body below (or the file replaced in the repair commit); the gate must then show zero hits for it with no allowlist row.
- The round-17 spot-check cites `:339-346` and `:390-397`; the frozen policy cites `:339-346` for the must-redact source. Those lesson lines are non-author; not edited here.
- The privacy exposure of already-pushed history is operator/kagi-owned and is not assessed here.

## Replacement

Draft body removed from this report in round 18 (second pass): it is integrated, and further minimized, at `.ufo/waves/round-17/build/OmpRetryConfig.md`; the draft as delivered remains in commit `b8f5c6c` history only.
