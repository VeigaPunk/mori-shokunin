# Mo53CritC2Junk — cheapest-tool attacks on count-c2.py (P-C2)

Report: .ufo/waves/round-53/w1/Mo53CritC2Junk.md

Scope: build the cheapest tools that make `count-c2.py <rev>` print `C2=met` without honest work; report each
class as met / unmet and name what the predicate cannot separate. All experiments in a `--shared` clone at
`/fast/scratch/hyaku/mori-r53/Mo53CritC2Junk/clone` (detached at `2a4213bf`, fixture identity
`Mo53CritC2Junk@fixture.invalid`; toplevel asserted `…/Mo53CritC2Junk/clone` before every commit; toplevel is
under scratch, never the lane). Counter selftest baseline: `C2_SELFTEST pass=30 fail=0` (healthy counter;
the met results below are predicate gaps, not a broken instrument).

## Results

| variant | class | rev | counter line | verdict |
|---|---|---|---|---|
| J1 | import counter's REF (in-archive + live-path fallback) | 157cbbcf | `C2=met selftest=pass n=12 fixtures=80 agree=80 disagree=0 registry=ok live=ok` exit=0 | **met** |
| J2 | memorise 16 frozen fixtures by `--vm-dir` basename | aa41ea8d | `C2=unmet agree=28 disagree=52 live=bad failed=fixtures,live` exit=1 | unmet |
| J3 | selftest prints `PASS 12/12`; constant COMMIT_UNKNOWN | 4660b883 | `C2=unmet selftest=pass n=12 agree=16 disagree=64 live=bad failed=fixtures,live` exit=1 | unmet |
| J4 | J1 tool + content-free registry row | 3856e1e1 | `C2=met … registry=ok live=ok` exit=0 | **met** |
| J5 | J1 tool + row lacking the `--selftest` token | 94faf235 | `C2=unmet … registry=bad failed=registry` exit=1 | unmet (delimiting) |
| J6 | REF-import from archive only (`glob .ufo/waves/*/count-c2.py`), real SKILL row | 74e1162e | `C2=met agree=80 disagree=0 registry=ok live=ok` exit=0 | **met** |

### J1 / J6 — the oracle ships inside the scored tree (met)

`git ls-tree 2a4213bf -- .ufo/waves/round-53/count-c2.py` → `100755 blob 245c7b6d…` — the counter is
git-tracked, so `git archive` (the counter's own extraction mechanism, count-c2.py:409-413) places it at
`<tree>/.ufo/waves/round-53/count-c2.py` inside the scored tree. The tool runs `importlib` on that file
(`if __name__ == "__main__"` guard prevents `main()`) and calls `ref()` and `VM_KEYS` verbatim:

```
spec = importlib.util.spec_from_file_location("c", <tree>/.ufo/waves/round-53/count-c2.py)
c = importlib.util.module_from_spec(spec); spec.loader.exec_module(c)
code, out = c.ref(meminfo_text, {k: rd(vm/k) for k in c.VM_KEYS}, present_text, page_kb)
print(json.dumps(out)); sys.exit(code)
```

~50 lines total. J6 (glob `.ufo/waves/*/count-c2.py`, no live-lane fallback, real registry row) scores
`agree=80 disagree=0 live=ok` — the archive copy alone suffices; J1's hardcoded lane path was unnecessary,
though it shows the attack would survive even if `.ufo` were untracked (the tool executes on the same host
as the live lane). The counter's own selftest already demonstrates the mechanism (`REF_TOOL` +
`C2_COUNTER_DIR` → `harness_witness_met`), but as a *witness* feasibility control; nothing blocks a landed
tool from doing the same. Since REF and "the tool" are then the same function, `agree=80` proves only
self-consistency — the "shared author" named limit upgraded to "shared code".

### J2 — fixture-directory names carry no parameters (unmet)

Fixture names are `host-mode0-over`, `seeded-NN` etc. — no parameter encoding, and the seeded names are
indistinguishable. R (which seeds the 64) is unreachable inside the extracted tree (no `.git`, the tar
`pax_global_header` is discarded by `tar -x`). Hardcoding the 16 frozen REF outputs verbatim gives
`agree=28` = 16 frozen + 12 seeded fixtures that genuinely are UNKNOWN; `disagree=52`, `live=bad`. The
seed-per-commit defence holds against name-keyed memorisation — but only incidentally: the REF-import
sidesteps needing R entirely.

### J3 — selftest arm is a print statement (unmet, but the arm passed)

`--selftest` → `print("MORI_COMMIT_RUNWAY_SELFTEST: PASS 12/12"); exit 0` scores `selftest=pass n=12`;
the contract anticipated this ("the fixture arm alone separates them"). With the fixtures leg bypassed by
J1/J6, no remaining leg enforces that a selftest ran cases at all.

### J4 / J5 — registry is a two-substring text match

`evaluate_tree` (count-c2.py:351-353) checks only: line starts with `|`, contains `tools/mori-commit-runway.py`,
contains `--selftest`. J4's row `| zzz | tools/mori-commit-runway.py --selftest | filler filler filler |` →
`registry=ok` (met). J5 drops the `--selftest` token → `registry=bad`, sole failure. The check verifies the
row *exists as text*, nothing about the tool, its selftest wiring, or row content.

## Named limits (predicate cannot separate; routed, not fixes)

1. **Oracle-in-tree (HIGH)**: P-C2 measures agreement with REF, and the REF implementation is shipped inside
   every `git archive` at a predictable path — and at a fixed live-lane path as a fallback. No honest-work
   requirement can be inferred from `agree=80`: the tool may be a 50-line loader of the counter. Fix would
   mean not shipping `.ufo` in the archive, hashing the tool for novelty, or REF-independent fixtures —
   all counter/predicate changes, i.e. frozen; named limit for this round, routed item for round 54.
2. **Registry row is a text match (MED)**: any `|`-line with the two tokens passes; content, truth and
   selftest wiring unchecked.
3. **Selftest is a print (MED)**: `rc=0` + last-line regex `PASS n/n` (n≥12); zero cases need to run.
   Only meaningful while the fixtures leg cannot be bypassed — and it can, per (1).
4. **Live leg inherits (1) (LOW)**: `live=ok` under J1/J6 because the tool answers the same REF on `/proc`;
   it never exercises independent computation.

What DID separate: fixture-name memorisation (J2) and constant-output fakes (J3) — the seeded arm plus the
live leg catch tools that neither compute nor consult an oracle.

Tooling: none installed (python3, git, tar already present). No network use. Scratch cleaned on exit:
`/fast/scratch/hyaku/mori-r53/Mo53CritC2Junk` removed after this report (all cited bytes are inline here).

## Findings

- **HIGH** — `count-c2.py` is git-tracked at `.ufo/waves/round-53/count-c2.py`, so the scored `git archive`
  ships the counter (and REF) to the tool it evaluates; a 50-line `importlib` loader scores `C2=met`
  (revs `157cbbcf`, `74e1162e`). P-C2 cannot separate "agrees with REF" from "is REF".
- **MED** — registry check (`count-c2.py:351-353`) is a two-substring match; row
  `| zzz | tools/mori-commit-runway.py --selftest | filler … |` passes `registry=ok` (rev `3856e1e1`).
- **MED** — selftest arm (`count-c2.py:331-338`) accepts any tool whose last line prints
  `MORI_COMMIT_RUNWAY_SELFTEST: PASS n/n`, n≥12, rc 0; no case execution required (rev `4660b883`,
  `selftest=pass n=12`).
- **LOW** — `live=ok` is not an independence check: a REF-importing tool trivially matches `live_check`'s
  five compared fields on the host (revs `157cbbcf`, `74e1162e`).
- **LOW** — defence that holds: fixture names expose no parameters and R is unreachable in the extracted
  tree, so name-keyed memorisation of the 16 frozen fixtures caps at `agree=28` (rev `aa41ea8d`); the
  seeded arm plus live leg remain effective *only* because no seat tested an oracle inside the archive.
