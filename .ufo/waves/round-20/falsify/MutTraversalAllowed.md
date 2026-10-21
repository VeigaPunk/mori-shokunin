BROKEN — C2 test strength for the assigned lexical-path-guard mutation: SURVIVED.

This is a scoped mutation-testing finding, not an overall C2 acceptance judgment or a claim of a defect in the pristine production tool. Both detectors passed on pristine, mutated, and exactly restored bytes. The mutant was not killed, and no baseline failure made the result inconclusive.

## Mutant and expected detector

Production source: `tools/mori-wave-settlement.py:152-170`. Contract: `.ufo/waves/round-20/contract.md:70-73` requires a relative path with no `..` component that resolves inside the lane root.

Exactly one conceptual mutant was applied, only to `.ufo/waves/round-20/falsify/MutTraversalAllowed/mori-wave-settlement.py`: delete the explicit POSIX/Windows absolute-path and `..`-component rejections in `_safe_report_path`. Empty/NUL checks and the separate resolved-containment check were left unchanged. Actual diff:

```diff
--- pristine
+++ mutant
@@ -151,14 +151,10 @@
 
 def _safe_report_path(lane_root: str, raw_path: str) -> tuple[bool, tuple[str, ...]]:
     """Validate the lexical path before performing any filesystem lookup."""
-    if (not raw_path or "\x00" in raw_path or os.path.isabs(raw_path)
-            or ntpath.isabs(raw_path)):
+    if not raw_path or "\x00" in raw_path:
         return False, ()
 
     components = raw_path.split(os.sep)
-    if ".." in components:
-        return False, ()
-
     candidate = os.path.abspath(os.path.join(lane_root, raw_path))
     try:
         if os.path.commonpath((lane_root, candidate)) != lane_root:
```

Expected kill signal: the mutated selftest exits nonzero, or the independent oracle exits nonzero with a mismatched case, while the pristine control passes. Neither signal occurred.

## Actual bounded detector runs

The same selftest command was run once in each phase (pristine, mutant, restored):

```sh
python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-20/falsify/MutTraversalAllowed/mori-wave-settlement.py --selftest
```

Exact stdout in ALL THREE phases:

```text
MORI_WAVE_SETTLEMENT_SELFTEST: PASS (21 cases, 21 passed, 0 failed)
```

Each run: stderr empty, exit code 0.

Independent-oracle commands, in phase order:

```sh
python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-20/build/OracleHarness/c2-oracle.py --tool /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-20/falsify/MutTraversalAllowed/mori-wave-settlement.py --out /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-20/falsify/MutTraversalAllowed/oracle-pristine.json
python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-20/build/OracleHarness/c2-oracle.py --tool /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-20/falsify/MutTraversalAllowed/mori-wave-settlement.py --out /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-20/falsify/MutTraversalAllowed/oracle.json
python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-20/build/OracleHarness/c2-oracle.py --tool /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-20/falsify/MutTraversalAllowed/mori-wave-settlement.py --out /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-20/falsify/MutTraversalAllowed/oracle-restored.json
```

Each oracle run: stdout empty, stderr empty, exit code 0.

Exact count commands:

```sh
/usr/bin/jq .counts /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-20/falsify/MutTraversalAllowed/oracle-pristine.json
/usr/bin/jq .counts /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-20/falsify/MutTraversalAllowed/oracle.json
/usr/bin/jq .counts /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-20/falsify/MutTraversalAllowed/oracle-restored.json
```

Exact stdout from EACH count command (each exit code 0):

```json
{
  "capability_absent": 0,
  "matched": 14,
  "mismatched": 0
}
```

In the mutant oracle evidence, both `traversal` and `absolute-path` remain `status: matched`; each observed scan exit is 1, state is `unavailable`, and `unsafe` is 1. These per-fixture scan exits are expected and are not detector failures.

The complete pristine, mutant, and restored oracle JSON files were also byte-identical. Exact comparison command:

```sh
cmp -- /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-20/falsify/MutTraversalAllowed/oracle-pristine.json /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-20/falsify/MutTraversalAllowed/oracle.json && cmp -- /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-20/falsify/MutTraversalAllowed/oracle-pristine.json /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-20/falsify/MutTraversalAllowed/oracle-restored.json
```

Output empty; exit code 0.

## Interpretation and scope

The independent harness constructs only an escaping traversal path (`../../outside.md`) and an absolute report outside the lane for these cases (`.ufo/waves/round-20/build/OracleHarness/c2-oracle.py:111-122`). The pristine tool separately retains a resolved-containment guard (`tools/mori-wave-settlement.py:162-167`).

[INFERENCE] That remaining guard masks deletion of the lexical guards for these frozen fixtures. The observed survivor identifies a gap in independent coverage of the contract's lexical restrictions, distinct from its containment restriction. Within-root paths containing `..` and absolute paths inside the lane are candidate discriminating fixtures; they were not run in this assignment. No contract, production code, oracle, or frozen expectation was changed.

## Before/after hashes and exact restoration

Observed SHA-256 values:

| Bytes | SHA-256 |
| --- | --- |
| Production source before copying | `c6e6091937e4bcb02775cea81ce33990924c6e27487a6ce255d2959d94f4e795` |
| Pristine scratch copy and preserved `pristine.py` | `c6e6091937e4bcb02775cea81ce33990924c6e27487a6ce255d2959d94f4e795` |
| Mutated scratch copy | `fc90c538a1a6e95af2f547c1922e20fe15a3ead2eada92c40d7bd96ba56ffb04` |
| Restored scratch copy | `c6e6091937e4bcb02775cea81ce33990924c6e27487a6ce255d2959d94f4e795` |
| Production source after restoration | `c6e6091937e4bcb02775cea81ce33990924c6e27487a6ce255d2959d94f4e795` |

Exact restoration and byte-comparison command:

```sh
cp -- /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-20/falsify/MutTraversalAllowed/pristine.py /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-20/falsify/MutTraversalAllowed/mori-wave-settlement.py && cmp -- /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-20/falsify/MutTraversalAllowed/pristine.py /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-20/falsify/MutTraversalAllowed/mori-wave-settlement.py && sha256sum /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-wave-settlement.py /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-20/falsify/MutTraversalAllowed/pristine.py /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-20/falsify/MutTraversalAllowed/mori-wave-settlement.py
```

Exact stdout (exit code 0):

```text
c6e6091937e4bcb02775cea81ce33990924c6e27487a6ce255d2959d94f4e795  /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-wave-settlement.py
c6e6091937e4bcb02775cea81ce33990924c6e27487a6ce255d2959d94f4e795  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-20/falsify/MutTraversalAllowed/pristine.py
c6e6091937e4bcb02775cea81ce33990924c6e27487a6ce255d2959d94f4e795  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-20/falsify/MutTraversalAllowed/mori-wave-settlement.py
```

The restored control runs above occurred after this restoration. Production files were read-only throughout. No installs/updates, subagents, census, host-service actions, Git/jj mutations, integration, or other mutation probes were performed.
