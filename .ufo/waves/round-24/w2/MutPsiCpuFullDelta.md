# MutPsiCpuFullDelta — mutation probe of `tools/mori-pressure.py --selftest` (C2)

Seat: `MoriR24.MutPsiCpuFullDelta` (leaf; no subagents dispatched, no sibling lane touched).
Claim under test: **C2** — `MORI_PRESSURE_SELFTEST: PASS 12/12` over frozen
`tools/fixtures/mori-pressure/cases.json` (12 cases P01–P12, frozen at `f6a29702`
before the tool landed at `6ee62487`; contract Amendment A3 binds system cpu `full`
interval delta fields to null).
Date: 2026-10-22. Sandbox:
`/fast/scratch/hyaku/mori-r24-a2/w2/MutPsiCpuFullDelta/repo`
(`git clone --no-hardlinks /home/vgpnk/Projects/shokunin/mori-shokunin <dir>`;
checkout `a730ecfefbdb5c31b1db13aca2c40eecd5e97abc`, the measured lane tip for this wave).

**The lane repo was never written** except this report file. All mutation and
detection happened in the sandbox clone; no `git add`/`commit`/`stash`/`checkout`/
`reset`/`pull`/`push` and no mutating `jj` command ran in
`/home/vgpnk/Projects/shokunin/mori-shokunin` (the only `git checkout` was inside the
clone, to restore the mutated file's bytes).

---

## 1. Mutant

Smallest behavior-bearing point implementing **"system cpu full delta and ratio numeric
instead of null under `--interval`"**: delete the A3 guard block in
`_combine_interval` (`tools/mori-pressure.py:267-271` at tip), so system cpu `full`
falls through to the ordinary numeric delta/ratio computation instead of forcing
`total_delta_us: null` / `stall_ratio: null`. No other byte changed.

```diff
--- a/tools/mori-pressure.py
+++ b/tools/mori-pressure.py
@@ -264,11 +264,6 @@ def _combine_interval(
         if prev is None:
             # A kind present in one read only; leave delta fields absent.
             continue
-        if name in FULL_UNDEFINED and kind == "full":
-            # A3: system cpu full always carries null delta fields (never zero).
-            value["total_delta_us"] = None
-            value["stall_ratio"] = None
-            continue
         delta = value["total"] - prev["total"]
         value["total_delta_us"] = delta
         value["stall_ratio"] = round(delta / (interval_s * 1e6), 6)
```

Effect: in interval mode, system cpu `full` now reports computed
`total_delta_us`/`stall_ratio` (numeric) instead of null — e.g. in P11 0 / 0.0
(totals 0 → 0). This is the exact scenario A3 forbids ("System CPU `full` gets
`total_delta_us: null` and `stall_ratio: null` (never a numeric zero)").

## 2. Expected detector

`python3 -I tools/mori-pressure.py --selftest` (in the clone, same working dir
layout as the lane). The frozen interval case **P11** (`--interval 1`, two
snapshots) expects `cpu.full.total_delta_us == null` and
`cpu.full.stall_ratio == null` (verified: `cases.json` P11 `expect.resources.cpu.full`
= `{"total_delta_us": null, "stall_ratio": null}`). A numeric value there is a
contract violation and should fail the selftest.

## 3. Outputs

Pristine (tip `a730ecf`, no mutation), SHA256
`852d1ea7508004dc44690bb6e358625fbd07d89c26d4196793133559d8a773a5`:

```
$ python3 --version
Python 3.14.8
$ python3 -I tools/mori-pressure.py --selftest
MORI_PRESSURE_SELFTEST: PASS 12/12
exit=0
```

Mutated (guard deleted), SHA256
`c820ec98b83b0fc6add290528c8d6e9f18d55657f997f23d414f030806f1088a`:

```
$ python3 -I tools/mori-pressure.py --selftest
MORI_PRESSURE_SELFTEST: FAIL 11/12
P11: cpu.full.total_delta_us is 0, expected None; cpu.full.stall_ratio is 0.0, expected None
exit=1
```

## 4. Verdict: **KILLED**

The frozen case **P11** kills the mutant. P11's expectation block
(`_case_failures`, `tools/mori-pressure.py:466-486`) explicitly pins
`cpu.full.total_delta_us`/`stall_ratio` to null, and the mutated numeric values
(0 / 0.0) fail both pinned fields. The other 11 cases still pass (FAIL 11/12, only
P11 listed). Baseline was green before the mutation, so the red is a genuine kill,
not an inconclusive baseline. The selftest is sensitive to this A3 violation, and
the tool's own docstring/comment (`:83-85`, `:267-271`) is inconsistent with the
mutated behavior but the frozen cases are not — C2's selftest claim holds for this
mutant class (the null-forcing guard is load-bearing for P11).

## 5. Restoration evidence

Exact bytes restored in the clone with `git checkout -- tools/mori-pressure.py`
(clone-local only). After restore:

```
$ sha256sum tools/mori-pressure.py
852d1ea7508004dc44690bb6e358625fbd07d89c26d4196793133559d8a773a5  tools/mori-pressure.py
$ python3 -I tools/mori-pressure.py --selftest
MORI_PRESSURE_SELFTEST: PASS 12/12
exit=0
$ git status --porcelain
(clean)
$ git rev-parse HEAD
a730ecfefbdb5c31b1db13aca2c40eecd5e97abc
```

Restored hash equals the pristine pre-mutation hash; selftest back to PASS 12/12.

**Lane untouched:** the only file this seat created in the lane is this report
(`.ufo/waves/round-24/w2/MutPsiCpuFullDelta.md`). No tool installs were made
(no pacman/uv/npx/cargo action; `python3` 3.14.8 already present). No `/proc`,
`/sys`, cgroup, PSI trigger, or service interactions.
