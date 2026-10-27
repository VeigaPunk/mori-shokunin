# Mo56MutC1Counter — mutation probe on the frozen C1 counter

Seat: Mo56MutC1Counter (w1). Scope: mutation-test
`/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-56/count-c1.py`
with six single-point mutants; each mutant run at freeze tip
`8be2717b0809281d07dffe83dad424a4859e0747` AND at a scratch fixture revision
carrying a matching mutant tree; report every `C1=met` printed on a
non-compliant tree (BYPASSED).

The honest finding the freeze pins cannot catch: the counter sha is pinned in
the freeze commit, but nothing re-verifies the counter's bytes at runtime — a
verifier executes whatever file it is handed. Six of six mutants behaved
exactly as designed; four printed `C1=met` on trees the frozen predicate
rejects.

Lane repo never mutated (no index/tree writes; `git status --porcelain` on the
watched paths empty before and after). All mutants and the fixture repo live
under `/fast/scratch/hyaku/mori-r56/Mo56MutC1Counter/` (removed at seat end).

## Setup and baselines (pristine counter)

Counter bytes identical at freeze tip and working tree:
`sha256 = c4e58eedadda2f7069bb8f31c5b1b6ae527a54aecaa7490308a55f127047f71d`.
Tool sha256 at `6ced9da9` and `8be2717b` both equal PIN
`6b3dba74c639190e7e96b6bed8e6ac8f285a51ce6d910fbe92e6dd39bf7be997` — pin arm
verified to bind the data-commit bytes, not just the freeze-commit copy.

Scratch fixture repo `fixrepo` = `git archive 8be2717b` tree copied into
`git init` at `$S/fixrepo`, freeze-tree commit `f8450c89fe0b560c8812cbc791a1193e8ec78ae8`
(asserted `rev-parse --show-toplevel` == fixrepo dir before first commit; all
commits carry throwaway identity inside the fixture repo only). Each mutant
tree = one branch off `f8450c89` with a single intended diff.

Pristine-counter baselines reproduced both frozen receipts exactly:

```
$ python3 count-c1-pristine.py 8be2717b0809281d07dffe83dad424a4859e0747
C1=met selftest=ok fixtures=ok entry=ok row=ok norem=ok rev=8be2717b0809281d07dffe83dad424a4859e0747   exit=0
$ python3 count-c1-pristine.py 3f494b49cde612d929e82887a48e1660c022c359
C1=met selftest=ok fixtures=ok entry=ok row=ok norem=ok rev=3f494b49cde612d929e82887a48e1660c022c359   exit=0   (matches evidence/c1-at-freeze.txt)
$ python3 count-c1-pristine.py 5b295eeebd87ebd610d8d39bfe2035742f740cfa
C1=unmet selftest=bad fixtures=bad entry=bad row=bad norem=bad failed=tool_absent rev=5b295eeebd87ebd610d8d39bfe2035742f740cfa   exit=1   (matches controls.txt do-nothing-c1)
$ python3 count-c1-pristine.py --selftest
C1_COUNTER_SELFTEST pass=1 fail=0   exit=0
```

## Mutants and matching trees

| # | counter mutation (single point) | mutant sha256 | tree pairing (branch `f8450c89`+1 commit) |
|---|--------------------------------|---------------|--------------------------------------------|
| M1 | `EXPECT_FIX["two-lanes"]: 0→1` (value softened) | `20b81e5a…c048` | `drift1` `9f74f4bb`: two-lanes log +1 malformed line |
| M2 | `HEALTH_WORDS` minus `"healthy"` | `dd053aab…91eb` | `healthword` `4ed2486d`: tool gains `# healthy` before `# selftest` marker |
| M3 | entry check → file existence only | `b97ceddf…4237` | `entryshape` `bbf1c41b`: placeholder entry, no S544/tool name |
| M4 | fixture arm loop deleted | `012e562b…5d84` | `drift4` `5e70be5e`: in-flight log +1 malformed line |
| M5 | `if PIN and` → `if False and` (pin gate dead) | `5427f492…b26a` | `tooldrift` `afe7fa78`: tool +2 inert EOF comment lines (sha `45a0d445…12ab` ≠ PIN) |
| M6 | rev-parse failure → accept raw rev; `rev=` label hardcoded to `8be2717b` | `da6849ed…6fd9` | `tooldrift2` `221da240`: same inert drift; plus compliant-tree rev `f8450c89` |

Malformed lines use a non-ISO first token (`banana split <lane> round=<n>`) —
parse-log `_bad`, no lane-row effect. Chosen fixture targets
(`two-lanes`, `in-flight`) have tool-selftest cases that do NOT assert a
malformed count, isolating the counter arm (see Finding F2).

## Results (every executed combination)

M1 — `@8be2717b` (real repo):
`C1=unmet selftest=ok fixtures=bad … rev=8be2717b… failed=fixtures` exit=1
(mutant also wrong on the honest tree — false negative).
`mut1 --selftest` → `C1_COUNTER_SELFTEST pass=1 fail=0` exit=0
(counter selftest does not catch table-value drift).
`pristine @drift1` → `C1=unmet … failed=fixtures` exit=1 (detector fires).
`mut1 @drift1` → `C1=met selftest=ok fixtures=ok entry=ok row=ok norem=ok rev=9f74f4bb…` exit=0 — **BYPASSED**.

M2 — `@8be2717b` → `C1=met …` exit=0 (identical to pristine on compliant tree).
`pristine @healthword` → `C1=unmet … norem=bad failed=pins,norem` exit=1.
`mut2 @healthword` → `C1=unmet … norem=ok failed=pins` exit=1 — **KILLED**
(the pin arm independently catches the same tool bytes that carry the
health word; a single-point counter mutant cannot bypass both).

M3 — `@8be2717b` → `C1=met` exit=0.
`pristine @entryshape-v2` → `C1=unmet … entry=bad failed=entry` exit=1.
`mut3 @entryshape-v2` → `C1=met … entry=ok rev=bbf1c41b…` exit=0 — **BYPASSED**.

M4 — `@8be2717b` → `C1=met` exit=0.
`pristine @drift4` → `C1=unmet … fixtures=bad` exit=1.
`mut4 @drift4` → `C1=met … fixtures=ok rev=5e70be5e…` exit=0 — **BYPASSED**.

M5 — `@8be2717b` → `C1=met` exit=0; `@5b295eee` →
`C1=unmet … failed=tool_absent rev=5b295eee…` exit=1 (do-nothing control intact).
`pristine @tooldrift` → `C1=unmet … failed=pins` exit=1.
`mut5 @tooldrift` → `C1=met … rev=afe7fa78…` exit=0 — **BYPASSED**
(the only arm binding tool bytes is gone; any rewritten tool passes).

M6 — `@8be2717b` → `C1=met … rev=8be2717b…` exit=0 (identical to pristine).
`mut6 @5b295eee` → `C1=unmet … failed=tool_absent rev=8be2717b…` exit=1 —
note the label already lies on the UNMET line (real evaluated rev was `5b295eee`).
`pristine @tooldrift2` → `C1=unmet … failed=pins` exit=1.
`mut6 @tooldrift2` → `C1=unmet … failed=pins rev=8be2717b…` exit=1 — verdict
**KILLED** by the intact pin arm.
`mut6 @f8450c89 (compliant tree, non-frozen rev)` →
`C1=met selftest=ok fixtures=ok entry=ok row=ok norem=ok rev=8be2717b…` exit=0 —
byte-identical output line to the honest freeze receipt while evaluating a
different revision: **SURVIVED** as receipt-label forgery (the verdict itself
stayed honest only because the tree was compliant; a consumer that greps
`C1=met rev=8be2717b` is defeated).

Summary: BYPASSED 4/6 (M1, M3, M4, M5); KILLED 2/6 (M2, M6-verdict); M6
survives as label forgery. Every bypass required executing mutated counter
bytes — the frozen predicate itself always caught the non-compliant trees
when the pristine counter ran.

## Accidental observation (M3 first pairing)

The first `entryshape` commit (`90626cee`, file literally stating "deliberately
omits the required source-row identifier and the tool filename") printed
`C1=met` under the PRISTINE counter: the entry arm matches substrings, and the
placeholder's prose contained both needles. Tree rebuilt needle-free at
`bbf1c41b` for the M3 pairing above; the substring weakness itself is recorded
as Finding F3.

## Restoration evidence

- Lane counter `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-56/count-c1.py`
  sha256 `c4e58eed…f71d` before AND after all runs (never written).
- Lane tool `tools/mori-driver-liveness.py` sha256 `6b3dba74…e997` (= PIN)
  unchanged.
- All counter mutations exist only under
  `/fast/scratch/hyaku/mori-r56/Mo56MutC1Counter/` — declared scratch,
  deleted at seat end (`rm -rf`).
- `git -C mori-shokunin status --porcelain` on `count-c1.py`,
  `tools/mori-driver-liveness.py`, `fixtures`, `corpus/knowledge/driver-liveness-r56.md`:
  empty, exit=0.
- No tool installs; python3/git/tar only. TMPDIR = scratch `tmp/` throughout;
  the counter's `mori-r56-c1-*` materializations stayed inside it.

## Findings

- HIGH — `count-c1.py` pin arm (line ~122): M5 (`if PIN and` → `if False and`)
  lets a tool bearing arbitrary rewritten bytes print `C1=met` on
  `tooldrift` (`afe7fa78`). The frozen PIN is the sole arm binding tool
  bytes; a runtime-counter mutation silently unfreezes the whole C1 claim.
  Named limit, not a fix proposal: nothing in the round-56 flow re-verifies
  executed counter bytes against the freeze (candidate round-57 item:
  verifier-side `git show <freeze>:count-c1.py | sha256sum` gate, or counters
  that self-hash their own argv[0] source).
- HIGH — `count-c1.py` rev arm (lines ~181-203): M6 hardcodes `rev=8be2717b`
  while evaluating any rev, and the same line prints the pinned tip even on
  `C1=unmet` output. Receipt trust depends entirely on counter integrity —
  the `rev=` field is self-attested, never cross-checked by a consumer.
- MED — `count-c1.py` fixture table vs. tool selftest: M1 and M4 both bypass
  on fixture-byte drift that escapes the tool's own selftest (selftest
  asserts malformed counts only on 3 of 9 fixtures — `malformed`×2,
  `hyaku-pairing`, `legacy-grammar`, `variants` partially; `two-lanes`,
  `in-flight`, `fails-and-dead`, `attempt-rollover` carry no count
  assertion). The counter's EXPECT_FIX table is thus single-arm coverage for
  those fixtures; a table value softened to match drifted bytes (M1) or the
  arm's deletion (M4) prints `C1=met`. Also: M1 wrongly printed `unmet` on
  the honest `8be2717b` tip, and the counter's own `--selftest` only checks
  `len(EXPECT_FIX)==9` (pass=1 on the drifted table).
- MED — `count-c1.py` entry arm (line ~151): M3 (existence-only check)
  bypasses on a placeholder entry; and even the PRISTINE arm is substring
  matching — a file that verbatim contains "S544" and
  "mori-driver-liveness.py" while claiming to omit them still prints
  `entry=ok` (observed on `90626cee`, first pairing). "Names" is lexical,
  not semantic.
- LOW — `count-c1.py` norem arm (line ~165): scan scope is
  `tool_src.split("# selftest",1)[0]` — text after the first `# selftest`
  marker is never health-word-checked. Not exploitable under the pristine
  pin arm (any tool byte change trips `pins`), but a second-order gap if
  that arm is ever bypassed.
- LOW — `count-c1.py` HEALTH_WORDS vs docstring: the tuple has 5 words but
  the frozen predicate sentence names only 3 (healthy, unhealthy,
  failed lane); `"is stuck"`, `"wedged"` are counter-enforced beyond the
  written contract. M2 was KILLED by the pin arm — positive defense-in-depth
  evidence for the freeze as written.
- INFO — controls integrity under mutants: M5 at `5b295eee` still prints
  `failed=tool_absent` exit=1 — mutating an arm does not blanket-flip the
  counter; killed mutants failed specifically, never silently.

Report: .ufo/waves/round-56/w1/Mo56MutC1Counter.md
