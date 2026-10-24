HOLDS — scoped detector result: KILLED by selftest. The independent frozen oracle SURVIVED this mutant (14/14 matched). This is a mutation-probe result, not a round-admission judgment.

# MutTrailerLastLine — C2 R1 mutation probe

## Scope and mutant

Axes: defect isolation, behavioral detection, exact-byte restoration.

Production source: `/home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-wave-settlement.py`.
Scratch target: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-20/falsify/MutTrailerLastLine/mori-wave-settlement.py`.

Exactly one behavior-bearing mutation was applied, confined to `_trailer`: replace the reverse search for the last matching report line (production `tools/mori-wave-settlement.py:207-211`) with only the task's final split line:

```python
    lines = task["task"].splitlines()
    match = REPORT_RE.fullmatch(lines[-1].rstrip()) if lines else None
```

Trailing-whitespace stripping, empty-task handling, path safety, status classification, and every fixture/check were unchanged. No production file was edited. The scratch target was subsequently restored.

## Expected detector

`tools/mori-wave-settlement.py:40` requires `r1-godspeed-trailer` to be settled with one present member and zero unparsed members. Its fixture at lines 496-500 appends `\n\n| godspeed` after a valid report trailer. R1 is disclosed at `corpus/lessons/round-20.md:31-35`; the frozen contract requires the last matching line at `.ufo/waves/round-20/contract.md:70-73`.

[INFERENCE] The expected failing selftest case is `r1-godspeed-trailer`: the mutant examines `| godspeed` instead of the earlier report trailer. The CLI emits only aggregate results, so the individual failing case ID was not directly observed.

The independent oracle's `_task` helper appends the report as the final line (`.ufo/waves/round-20/build/OracleHarness/c2-oracle.py:20-24`); its main loads only the frozen cases (lines 393-405). The actual oracle result below establishes that its 14 cases did not kill this R1 regression.

## Commands and actual outputs

The following identical bounded commands were run on the same scratch target in order: pristine control, mutated bytes, restored bytes. Selftest timeout was 60 seconds; oracle timeout was 120 seconds. Each phase completed within its bound.

Selftest command:

```sh
python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-20/falsify/MutTrailerLastLine/mori-wave-settlement.py --selftest
```

Pristine control — exit 0:

```text
MORI_WAVE_SETTLEMENT_SELFTEST: PASS (21 cases, 21 passed, 0 failed)
```

Mutant — exit 1:

```text
MORI_WAVE_SETTLEMENT_SELFTEST: FAIL (21 cases, 20 passed, 1 failed)
```

Restored — exit 0:

```text
MORI_WAVE_SETTLEMENT_SELFTEST: PASS (21 cases, 21 passed, 0 failed)
```

Oracle command:

```sh
python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-20/build/OracleHarness/c2-oracle.py --tool /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-20/falsify/MutTrailerLastLine/mori-wave-settlement.py --out /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-20/falsify/MutTrailerLastLine/oracle.json
```

Pristine, mutant, and restored: exit 0 each; no command output each.

After each oracle run, this exact command returned exit 0:

```sh
/usr/bin/jq .counts /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-20/falsify/MutTrailerLastLine/oracle.json
```

Exact output, identical in all three phases:

```json
{
  "capability_absent": 0,
  "matched": 14,
  "mismatched": 0
}
```

Phase-specific full oracle results were preserved under `.ufo/waves/round-20/falsify/MutTrailerLastLine/` as `oracle-pristine.json`, `oracle-mutant.json`, and `oracle-restored.json`. `oracle.json` contains the restored run.

## Hashes and restoration evidence

SHA-256 values were obtained with `sha256sum` (exit 0):

| Object / phase | SHA-256 |
| --- | --- |
| Production source before and after probe | `c6e6091937e4bcb02775cea81ce33990924c6e27487a6ce255d2959d94f4e795` |
| Scratch target, pristine | `c6e6091937e4bcb02775cea81ce33990924c6e27487a6ce255d2959d94f4e795` |
| Scratch target, mutated | `d4bd6e4ce027f9ed4bafd075a60e30b6c1ac864bab9ad3e1c634df9abde67358` |
| Scratch target, restored | `c6e6091937e4bcb02775cea81ce33990924c6e27487a6ce255d2959d94f4e795` |
| Pristine backup, before and after probe | `c6e6091937e4bcb02775cea81ce33990924c6e27487a6ce255d2959d94f4e795` |
| Independent oracle, before and after probe | `2a0da4c8acf20f5960302e3850992fff7a164003501bf73ca912532a0f8e6914` |
| Frozen `c2-expected.json`, before and after probe | `0984806922da727a02a7944c00154df7a5aaff356c91c6fb36f47467c4f7d2af` |

The mutation was reversed with an exact surgical restoration. This byte comparison then returned exit 0 and no output:

```sh
cmp -- /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-20/falsify/MutTrailerLastLine/mori-wave-settlement.pristine.py /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-20/falsify/MutTrailerLastLine/mori-wave-settlement.py
```

Both detectors were rerun after that restoration, with the passing outputs recorded above.

## Finding

**Combined detector: KILLED**, because the passing pristine selftest became exit 1 under exactly the assigned R1 mutant, then passed again on byte-identical restored code. **Independent frozen oracle alone: SURVIVED**, a specific R1 coverage gap; its 14/14 result is not evidence that this regression is absent. No contract change or production fix was made.

No tools were installed or updated. No census, fleet scan, subagent, other agent runtime, git/jj mutation, sibling edit, or host-service action was invoked. Writes were restricted to this scoped report and the assigned scratch directory (detector fixtures used temporary directories under `/tmp`).
