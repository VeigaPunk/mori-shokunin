PARTIAL — mutant KILLED by selftest; SURVIVED the independent 14-case oracle. This is a detector-strength finding, not an overall C2 admission verdict.

# MutStubCounted: one R2-removal probe

Probe dimensions: detector discrimination, scratch isolation, exact-byte restoration.

## Mutant and expected detector

Copied `tools/mori-wave-settlement.py` to `.ufo/waves/round-20/falsify/MutStubCounted/mori-wave-settlement.py`. Applied exactly one behavior mutation: deleted the following branch from `_member_status` (original `tools/mori-wave-settlement.py:226-228`), allowing the existing `return "present"` to classify a nonempty `STATUS: started` file as present:

```python
        if size <= max(len(stub) for stub in STUB_CONTENTS):
            if _read_regular_bytes(os.path.join(lane_root, *parts)) in STUB_CONTENTS:
                return "stub"
```

No expectations, fixtures, constants, or other behavior were edited. Expected detector: the refinement selftest `r2-stub` (`tools/mori-wave-settlement.py:42`, fixture at `:507-511`) expects exit 1, state partial, present 1, stub 1, missing_names ["A"]. The lesson explicitly claims selftest fail-capability for removing R2 (`corpus/lessons/round-20.md:24`). The observed selftest output below is aggregate; it does not name the failing case.

## Exact bounded commands

The same three commands were executed on pristine, mutated, and restored bytes, with an outer 180-second deadline for each Python command and 20 seconds for jq. No command timed out.

```sh
python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-20/falsify/MutStubCounted/mori-wave-settlement.py --selftest
python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-20/build/OracleHarness/c2-oracle.py --tool /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-20/falsify/MutStubCounted/mori-wave-settlement.py --out /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-20/falsify/MutStubCounted/oracle.json
/usr/bin/jq .counts /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-20/falsify/MutStubCounted/oracle.json
```

### Pristine control

Selftest stdout (exit 0):

```text
MORI_WAVE_SETTLEMENT_SELFTEST: PASS (21 cases, 21 passed, 0 failed)
```

Oracle stdout and stderr empty; exit 0. jq stdout (exit 0):

```json
{
  "capability_absent": 0,
  "matched": 14,
  "mismatched": 0
}
```

### Mutated

Selftest stdout (exit 1):

```text
MORI_WAVE_SETTLEMENT_SELFTEST: FAIL (21 cases, 20 passed, 1 failed)
```

Oracle stdout and stderr empty; exit 0. jq stdout (exit 0), exactly unchanged:

```json
{
  "capability_absent": 0,
  "matched": 14,
  "mismatched": 0
}
```

### Restored control

Selftest stdout (exit 0):

```text
MORI_WAVE_SETTLEMENT_SELFTEST: PASS (21 cases, 21 passed, 0 failed)
```

Oracle stdout and stderr empty; exit 0. jq stdout (exit 0), exactly unchanged:

```json
{
  "capability_absent": 0,
  "matched": 14,
  "mismatched": 0
}
```

All selftest and jq stderr were empty. All stdout shown ends with a newline. The successful pristine and restored controls make the mutant's selftest failure conclusive: **KILLED** under the assigned selftest-or-oracle criterion. Separately, **SURVIVED** the independent oracle: its 14/14 result does not detect this R2 removal. This coverage finding does not change the frozen contract or claim the combined detector missed the mutant.

## Before/after hashes and restoration

SHA-256 was captured immediately before and after each detector phase; hashes were stable within each phase:

| Bytes | SHA-256 |
|---|---|
| Production source, initial pristine copy, saved pristine copy, restored copy | `c6e6091937e4bcb02775cea81ce33990924c6e27487a6ce255d2959d94f4e795` |
| Mutated copy | `13eeb720e2273aeebe2a436a8b70704868b85b7edaa4776a7f1d5d2627bb1ecf` |
| Independent oracle, all phases | `2a0da4c8acf20f5960302e3850992fff7a164003501bf73ca912532a0f8e6914` |
| Frozen expected cases, all phases | `0984806922da727a02a7944c00154df7a5aaff356c91c6fb36f47467c4f7d2af` |

Restoration ran in a `finally` block before the restored-control detector runs:

```sh
cp -- /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-20/falsify/MutStubCounted/mori-wave-settlement.pristine.py /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-20/falsify/MutStubCounted/mori-wave-settlement.py
cmp -- /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-20/falsify/MutStubCounted/mori-wave-settlement.pristine.py /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-20/falsify/MutStubCounted/mori-wave-settlement.py
```

Both commands: stdout empty, stderr empty, exit 0. Restored before/after hashes equal the saved pristine bytes; production source retained its original hash throughout.

## Retained evidence and bounds

All following paths are under `.ufo/waves/round-20/falsify/MutStubCounted/`:

- `pristine-run.json`, `mutated-run.json`, `restored-run.json`: exact command strings, stdout, stderr, exit codes, deadlines, and before/after hashes.
- `pristine-oracle.json`, `mutated-oracle.json`, `restored-oracle.json`: per-phase oracle observations.
- `restoration.json`: restoration and byte-comparison command evidence.
- `oracle.json`: retained mutant oracle observation, copied from `mutated-oracle.json` after all detector phases; `oracle-artifact.json` records that copy (exit 0, empty stdout/stderr).
- `mori-wave-settlement.py`: restored exact pristine bytes; `mori-wave-settlement.pristine.py`: saved restoration authority.

No production code, corpus, baseline, fleet state, sibling source, Git index, jj state, or host service was modified. No census, git/jj command, subagent, alternate agent runtime, or tool install/update was invoked. The only mutation was the scratch-copy branch deletion documented above. Probe complete.
