# MutC4KillAlt — alternative mutation of the `drifted` branch (`return "fresh"`)

Seat: `MoriR38.MutC4KillAlt` (mutation-tester, wave 2, round 38). Tip under attack:
`f725f3076972e6e70595b5ac8279be524a111ff8`. All work in
`.ufo/waves/round-38/scratch/MoriR38.MutC4KillAlt/`; lane files were never edited.

## Verdict

**PASS** — the alternative mutation is rejected on every path: `selftest row_states` FAILs and
names S103, and `count-c4.py` applied to a sandbox carrying the mutated tool prints `C4=unmet`
with `check drift_kill FAIL (mutation anchor absent)`. The kill criterion is also
mutation-agnostic on this branch: replayed with `to='return "fresh"'` against pristine bytes it
still prints `drift_kill PASS` with `row_states=('FAIL', got S103 fresh)`. The mutant does not
survive; two coverage caveats below are noted, not survivals.

## Mutant

- Pristine scratch bytes: `pristine.py`, sha256
  `453c5d8e260301df7a99daf62b4c16ea08e4a0b4f9e4f53821cdbce447011552` — identical to
  `sha256sum tools/mori-source-drift.py` in the lane and to
  `git show f725f30:tools/mori-source-drift.py | sha256sum`.
- Mutant: `alt.py`, one edit at `tools/mori-source-drift.py:208`
  (`def classify` at :202) — `    return "drifted"` → `    return "fresh"`;
  sha256 `e56e2f3255ad5acb028dc30abd8f14d755264137c3dce4705e695e3cec5605b5`.
  `diff -u pristine.py alt.py` shows exactly this one line.
- Shipped comparison mutant: `shipped.py`, same line → `return "excerpt"`;
  sha256 `c25ee3320016c04614e79eb22ebc71bdbe1269c2b16777f18898ac5d0468caf0`.

## Detector 1 — `python3 <copy> --selftest` (bounded, local 127.0.0.1 fixture)

| copy | exit | `row_states` | S103 named | other failing arms | last line |
|---|---|---|---|---|---|
| `pristine.py` | 0 | PASS | — | none | `MORI_SOURCE_DRIFT_SELFTEST: PASS (6 cases)` |
| `alt.py` | 1 | **FAIL** `got=[…('S103','fresh')…] want=[…('S103','drifted')…]` | **yes** (`('S103', 'fresh')`) | `exit_code` FAIL `rc=0 want 1`; `summary` FAIL `('10','3','1','0','4','2')` | `MORI_SOURCE_DRIFT_SELFTEST: FAIL (3/6)` |
| `shipped.py` | 1 | **FAIL** `got=[…('S103','excerpt')…]` | **yes** (`('S103', 'excerpt')`) | `exit_code` FAIL `rc=0 want 1`; `summary` FAIL `('10','2','2','0','4','2')` | `MORI_SOURCE_DRIFT_SELFTEST: FAIL (3/6)` |

Difference from the shipped mutation is only in the captured row state and the summary bucket
(`fresh=3` vs `excerpt=2`, `drifted=0` in both): both mutations collapse S103 out of `drifted`,
both leave `missing_sources_exit2` PASS. Saved: `pristine.selftest.txt`, `alt.selftest.txt`,
`shipped.selftest.txt`.

## Detector 2 — `count-c4.py` over a sandbox carrying the mutated tool

Two throwaway git repos built from the same rev's five measured files, differing only in the
tool bytes: `sandbox-pristine` (HEAD `63aed5b8a567c96df97a6873cf4d889a824ad63b`, tool sha
`453c5d8e…`) and `sandbox-alt` (HEAD `2f5fb1d555028e5d86c043f0ac1c201e9a482414`, tool sha
`e56e2f32…`). The lane counter was run unmodified with `--repo <sandbox>`.

- **Control, `sandbox-pristine`** → `C4=met`, rc=0; `check drift_kill PASS (exit=1
  row_states=('FAIL', got S103 excerpt))`. The sandbox plumbing itself is sound.
- **`sandbox-alt`** → `C4=unmet`, rc=1:
  - `check anchors FAIL (anchors=3 missing=['return "drifted"'])` — the entry pins the literal
    branch text as its third anchor (`corpus/knowledge/source-drift-content-anchor-r38.md:28`),
    so the mutation also breaks the byte-exact anchor check.
  - `check capability PASS (paths=[tools/mori-source-drift.py, …/c2-after-v3.txt, …/drift-live-r37.txt] missing=[])`
  - `check live_rows PASS (named=10 summary_drifted=10 unknown=[])`
  - `check named_row_drift FAIL (exit=1 row_states=('FAIL', got=[…('S103','fresh')…] want=[…('S103','drifted')…]))`
  - **`check drift_kill FAIL (mutation anchor absent)`** — `count-c4.py:275` finds no
    `DRIFT_MUTANT_FROM` (`'return "drifted"'`, :47) in the tool text and takes the else branch
    at :285; no mutant is constructed.
  - All three fabricated witnesses still rejected. Saved: `counter-sandbox-alt.txt`,
    `counter-sandbox-pristine.txt`.

## Detector 2b — the kill criterion itself, anchor present

`driftkill.py` imports `count-c4.py`'s own `selftest_arms` and replays the exact check at
`:275-282` (`kill_rc == 1 and row_states == FAIL and "S103" in detail`):

| label | tool bytes | from → to | result |
|---|---|---|---|
| A | `alt.py` (already mutated) | `drifted`→`excerpt` | `drift_kill FAIL (mutation anchor absent)` |
| B | `pristine.py` | `drifted`→`excerpt` (shipped) | `drift_kill PASS (exit=1 row_states=FAIL, S103 excerpt)` |
| C | `pristine.py` | `drifted`→`fresh` (alternative) | **`drift_kill PASS (exit=1 row_states=FAIL, got ('S103','fresh'))`** |
| D | `shipped.py` (already mutated) | `drifted`→`excerpt` | `drift_kill FAIL (mutation anchor absent)` |

C shows the kill predicate is behavioural, not `excerpt`-specific; A/D show the literal check
cannot operate on an already-mutated tool (symmetric for both mutations). Saved:
`B_pristine_shipped_excerpt.driftkill.txt`, `C_pristine_alt_fresh.driftkill.txt`.

## Acceptance answers

1. `selftest row_states` **fails** under `return "fresh"`: exit 1, `got ('S103','fresh')` vs
   `want ('S103','drifted')`.
2. **S103 is named** in the failure detail (and in the sandbox's `named_row_drift` detail).
3. The counter's `drift_kill` detail over the alt-carrying sandbox:
   **`FAIL (mutation anchor absent)`** (`count-c4.py:285`).
4. The kill check rejects a different mutation of the same branch: the alt mutant never yields
   `drift_kill PASS` in place, `C4=unmet` rc=1, and the same predicate independently kills it
   when the anchor is present (C). **PASS.**

## Coverage caveats (not survivals)

- `drift_kill`'s rejection here is structural (anchor absent), not a constructed kill: the
  counter can only exercise its criterion on its one hardcoded `return "drifted"` →
  `return "excerpt"` pair. A behavior-preserving rewording of that branch would also fail the
  check closed (never a false pass), and the literal is independently pinned by the entry
  anchor at `corpus/knowledge/source-drift-content-anchor-r38.md:28`.
- `"S103" in state[1]` (`count-c4.py:282`) is nearly vacuous: `row_states` echoes the full
  `got=`/`want=` lists, so any `row_states` FAIL satisfies the S103 clause. All four observed
  FAIL details (alt, shipped, sandbox-alt, A) contain S103 in `want`. The clause does not prove
  S103 itself diverged; the state comparison does.

## Restoration evidence

- Lane tool untouched: `sha256sum tools/mori-source-drift.py` =
  `453c5d8e…1552` before and after every run; tip blob hash identical;
  `git status --porcelain -- tools/mori-source-drift.py` empty. No mutating git/jj command was
  run in the lane; only `git show`/`cat-file`/`status` reads and read-only counter runs.
- Scratch copies are disposable; `pristine.py` hash unchanged after all probes. Keep-set
  retained for the record; no `mori-c4-*` temp dirs left under the lane scratch root
  (`ls -d .ufo/waves/round-38/scratch/mori-c4-*` → none).
- Tool installs/upgrades: none (no pacman/uv/npm transaction attempted).

## Evidence map (all under `.ufo/waves/round-38/scratch/MoriR38.MutC4KillAlt/`)

`pristine.py`, `alt.py`, `shipped.py`, `probe.py`, `pristine.selftest.txt`, `alt.selftest.txt`,
`shipped.selftest.txt`, `driftkill.py`, `B_pristine_shipped_excerpt.driftkill.txt`,
`C_pristine_alt_fresh.driftkill.txt`, `counterrun.py`, `counter-sandbox-alt.txt`,
`counter-sandbox-pristine.txt`, `sandbox-pristine/`, `sandbox-alt/`.
