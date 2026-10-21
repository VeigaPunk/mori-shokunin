# Absolute evidence-path check (preimplementation)

## Scope / axes
- **C1 freshness:** directly in scope—the audit must only read committed evidence beneath `--root` and must reject absolute provenance paths.
- **C2 calibration:** not exercised; this check does not assess rule classification.

## Finding
**No implementation defect can be confirmed yet.** The specified candidate `tools/mori-evidence-loss.py` was absent from the lane repository (`glob` on `/home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-evidence-loss.py` returned “Path not found”) and from the named isolated implementation clone (`glob` on `/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/round21/**/mori-evidence-loss.py` returned “No files found matching pattern”; direct read of the clone candidate also returned “not found”). Thus there is no implementation diff or runtime behavior to attribute a confirmed finding to.

**Concrete preimplementation counterexample:** with `--root /tmp/audit-root`, put `"/tmp/outside.json"` in a provenance `path` field. A naïve resolver that evaluates `Path(root) / raw_path` and then calls `read_bytes()` follows the absolute right-hand operand, not `/tmp/audit-root/tmp/outside.json`; the evidence read escapes the declared root. This is a counterexample to that resolver pattern, **not a claim that the absent candidate currently uses it**. Contract: `.ufo/waves/round-21/contract.md:14` requires relative provenance and rejection of absolute paths; lines 14–16 specify audit input/output and unsafe-evidence behavior.

## Smallest safe change
At the provenance boundary, validate the unmodified path value as a string and reject `Path(raw_path).is_absolute()` **before** joining it to `--root` and before any `resolve`, existence/stat, hash, open/read, or subprocess operation. Keep the existing relative-path containment/symlink validation after that check. A focused future fixture should assert that an absolute path is rejected without opening the target; do not treat it as a normal missing/hash-mismatch row.

## Residual risk / verification gaps
- The implementation and its tests are not available in the scoped checkout/clone, so the counterexample is advisory and no implementation pass/fail is claimed.
- No tests or runtime probes were run (per assignment).
- `xd://lsp` is not mounted in this session; semantic LSP checks were unavailable. No text search is used as semantic proof.
- No tools were installed or updated.