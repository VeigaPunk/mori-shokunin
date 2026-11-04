# Mo87E01C1Arms — C1 arm verification (mori r87, w1)

- seat: `Mo87E01C1Arms` (executor, leaf) · lane: `/home/vgpnk/Projects/shokunin/mori-shokunin` (read-only)
- round 87 attempt 1, wave w1 · date 2026-11-04
- frozen authority: `.ufo/waves/round-87/contract.md` §C1, at freeze `142542e0d853b4e8ec1aa1adb86708dc5786d9c0`
- after revision: `03b66a437e68d493ce0aacd1d80c321cc2e6bf7c` · entering revision: `6fc09d69edbb11e5070ff33258de49f062c0fb9b`
- tooling: **none installed** (`python3` 3.14.8, `git` 2.56.0 were already present; no uv/npx/pacman transaction)
- scratch: `/fast/scratch/hyaku/mori-r87/Mo87E01C1Arms` (removed before yield; no `/tmp` path is cited)

## Verdict

For all six frozen mutants, measured independently of `count-c1.py`'s aggregate:

1. the mutant anchor occurs **exactly once** in the subject loaded with `git show 03b66a4:<path>`;
2. the mutated copy's own `--selftest` exits **1** and prints **exactly one** `FAIL <arm>` line;
3. that arm is **the arm added by `03b66a4` whose name states the mutated clause**, and it did not exist at `6fc09d6`;
4. neutering *only that arm* in the same after subject and re-applying the same mutant returns the selftest to **rc 0, fail=0, frozen arm count** — so no other arm kills the mutant.

The arms added between entering and after are exactly the six killer arms (3 + 2 + 1), and the
same six mutant specs applied to the entering bytes are all survived (rc 0, fail=0). This
supports C1's operability sentence. Per seat scope I did **not** run the frozen
`count-c1.py <rev>` aggregate, so I do not certify the `C1=met … arms=54` line itself.

## 1. Pristine selftest tallies (three subjects, both revisions)

Each row is the subject's own `--selftest`, run as a byte copy inside scratch
(`python3 -I <copy> --selftest`, `TMPDIR` inside scratch, `GIT_CONFIG_GLOBAL=/dev/null`,
`GIT_CONFIG_SYSTEM=/dev/null`, cwd = a fresh scratch dir). `PASS`/`FAIL` columns are counted
`^PASS `/`^FAIL ` lines.

| revision | subject | rc | tally line | PASS | FAIL |
|---|---|---|---|---|---|
| 03b66a4 | count-c1.py | 0 | `C1_COUNTER_SELFTEST pass=18 fail=0` | 18 | 0 |
| 03b66a4 | count-c2.py | 0 | `C2_COUNTER_SELFTEST pass=13 fail=0` | 13 | 0 |
| 03b66a4 | count-c3.py | 0 | `C3_COUNTER_SELFTEST pass=23 fail=0` | 23 | 0 |
| 6fc09d6 | count-c1.py | 0 | `C1_COUNTER_SELFTEST pass=15 fail=0` | 15 | 0 |
| 6fc09d6 | count-c2.py | 0 | `C2_COUNTER_SELFTEST pass=11 fail=0` | 11 | 0 |
| 6fc09d6 | count-c3.py | 0 | `C3_COUNTER_SELFTEST pass=22 fail=0` | 22 | 0 |

Expectations in the seat brief (18/13/23 after, 15/11/22 entering) hold exactly; the frozen
per-file arm total is 18+13+23 = 54.

## 2. Anchors — exactly once at the after revision

Anchors are the `old` strings of the frozen r87 `MUTANTS` tuple. The r87 `count-c1.py` in the
worktree is byte-identical to the freeze commit (§5), so this population is the frozen one.

| mutant | subject (at 03b66a4) | anchor line | occurrences at 03b66a4 | occurrences at 6fc09d6 |
|---|---|---|---|---|
| M1-unanchored-conjunct | count-c1.py | 170 | 1 | 1 |
| M2-total-floor | count-c1.py | 169 | 1 | 1 |
| M3-arms-tally | count-c1.py | 141 | 1 | 1 |
| M4-receipt-summary | count-c2.py | 193 | 1 | 1 |
| M5-binding-digest | count-c2.py | 205 | 1 | 1 |
| M6-keyshape | count-c3.py | 73 | 1 | 1 |

No mutant was `unanchored` or `empty-mutation` at either revision.

## 3. Kills at `03b66a4` — one arm per mutant, and it is the new arm

`tally` is the mutated copy's own `COUNTER_SELFTEST pass/fail`; the `FAIL` line is verbatim.

| mutant | file | rc | tally | FAIL line (verbatim) | killer arm | arm present at 6fc09d6? |
|---|---|---|---|---|---|---|
| M1-unanchored-conjunct | count-c1.py | 1 | 17/1 | `FAIL unanchored_plus_killed_unmet mutants=1 killed=1 survivors=0 total=1 arms=-1` | `unanchored_plus_killed_unmet` | **no** |
| M2-total-floor | count-c1.py | 1 | 17/1 | `FAIL zero_mutants_unmet mutants=0 killed=0 survivors=0 total=0 arms=-1` | `zero_mutants_unmet` | **no** |
| M3-arms-tally | count-c1.py | 1 | 17/1 | `FAIL arms_tally_from_subject mutants=0 killed=0 survivors=0 total=0 arms=26` | `arms_tally_from_subject` | **no** |
| M4-receipt-summary | count-c2.py | 1 | 12/1 | `FAIL summary_required RECEIPT fixture-a.txt expect=met met problems=-` | `summary_required` | **no** |
| M5-binding-digest | count-c2.py | 1 | 12/1 | `FAIL binding_required RECEIPT fixture-b.txt expect=met met problems=-` | `binding_required` | **no** |
| M6-keyshape | count-c3.py | 1 | 22/1 | `FAIL derive_keyshape keyshape` | `derive_keyshape` | **no** |

For every mutant the mutated run's `PASS ∪ FAIL` label set equals the pristine label set, and
`PASS` equals the pristine `PASS` minus the killer arm exactly (no arm disappeared, no crash —
the tally line is printed after all arms ran). Pass counts 17/17/17/12/12/22 + 1 fail reproduce
18/18/18/13/13/23.

## 4. Arm-set delta entering → after

| subject | arms at 6fc09d6 | arms at 03b66a4 | added | removed |
|---|---|---|---|---|
| count-c1.py | 15 | 18 | `unanchored_plus_killed_unmet`, `zero_mutants_unmet`, `arms_tally_from_subject` | — |
| count-c2.py | 11 | 13 | `summary_required`, `binding_required` | — |
| count-c3.py | 22 | 23 | `derive_keyshape` | — |

The three added columns are exactly the six killer arms of §3 — no killer arm pre-existed, and
no killer arm is unrelated to the mutant (each name states the mutated clause).

Arm sources at `03b66a4` (each assertion directly reads the mutated clause):

- `unanchored_plus_killed_unmet` — `(not met) and "unanchored" in " ".join(extras)` on a fixture that pairs one unanchored mutant with one killed mutant (so `total=1`; the mutant makes `met` true).
- `zero_mutants_unmet` — `(not met) and "total=0" in tail` on an empty mutant list.
- `arms_tally_from_subject` — `tail.endswith("arms=20")` where the synthetic subject prints `pass=20` (the mutated constant yields `arms=26`, the r86 counter's `TARGET_ARMS`).
- `summary_required` — `(not ok_a) and any("summary" in line for line in lines_a)` on a `met`-expecting receipt missing the summary token.
- `binding_required` — `(not ok_b) and any("sha:payload.txt" in line for line in lines_b)` on an unbound `met`-expecting receipt.
- `derive_keyshape` — `derive("foo*bar", (set(), set(), set())) == "value-changed"`.

## 5. Sole-killer exclusion (the arm does the killing)

Two runs per mutant on the same after subject: (A) the killer-arm assertion replaced by `True`,
no mutant; (B) same arm neutered **plus** the mutant re-applied.

| mutant | arm neutered | A: rc / tally / FAILs | B: rc / tally / FAILs | conclusion |
|---|---|---|---|---|
| M1 | `unanchored_plus_killed_unmet` | 0 / 18-0 / none | 0 / 18-0 / none | arm is the sole killer |
| M2 | `zero_mutants_unmet` | 0 / 18-0 / none | 0 / 18-0 / none | arm is the sole killer |
| M3 | `arms_tally_from_subject` | 0 / 18-0 / none | 0 / 18-0 / none | arm is the sole killer |
| M4 | `summary_required` | 0 / 13-0 / none | 0 / 13-0 / none | arm is the sole killer |
| M5 | `binding_required` | 0 / 13-0 / none | 0 / 13-0 / none | arm is the sole killer |
| M6 | `derive_keyshape` | 0 / 23-0 / none | 0 / 23-0 / none | arm is the sole killer |

(A) shows neutering does not perturb the frozen arm count; (B) shows that with that one arm
disabled the mutant is no longer detected — the kill is attributable to that arm alone.

## 6. Controls

| control | result |
|---|---|
| same six mutant specs on the entering bytes (`6fc09d6`), anchors 1× | all **survived**, rc 0, no `FAIL`; tallies 15 (M1–M3), 11 (M4–M5), 22 (M6) |
| neutral mutation per subject (append `# neutral control comment`) at `03b66a4` | green, rc 0; 18/13/23, no `FAIL` — file change alone does not trip any arm |
| mutated label set vs pristine | identical except the killer arm flips `PASS`→`FAIL`, for all six |

The entering control here uses the frozen mutant specs (not the probe's differently-specified
mutants), so "the six survive before and die after" is measured for the exact population.

## 7. Freeze identity actually read

| file | freeze `142542e0…` vs worktree | note |
|---|---|---|
| `.ufo/waves/round-87/count-c1.py` | SAME (`e2ff968721678cc6…`) | C1 detector is the frozen bytes |
| `.ufo/waves/round-87/evidence/controls-r87.txt` | SAME (`53d65a426632acdb…`) | |
| `.ufo/waves/round-87/evidence/probe-r87.txt` | SAME (`530e35e6058edfa5…`) | |
| `.ufo/waves/round-87/contract.md` | DIFF (`f28d75a7…` → `bf208a44…`) | only the appended `## Amendments (pre-data, disclosed)` + A1 block |
| `.ufo/waves/round-87/count-c2.py` | DIFF (`e1dfd45a…` → `264a43f0…`) | exactly A1: `SUBJECT_ARMS` 11→13, `SUBJECT_LABELS` gains `summary_required`+`binding_required`, `subject_arms` arm 11→13; no other hunk |

Both DIFFs are the disclosed pre-data A1 amendment; the C1 detector and both evidence files are
byte-identical to the freeze.

Subject identity (git blob at each revision, and sha256 of the extracted copy, first 16 hex):

| subject | blob @03b66a4 | blob @6fc09d6 | sha256 @03b66a4 | sha256 @6fc09d6 |
|---|---|---|---|---|
| count-c1.py | `91eecabadc…` | `3c2b873983…` | `bcd66561093aa304` | `1912e87d767aabfa` |
| count-c2.py | `71829635cd…` | `14299ca083…` | `28d667338674402f` | `94a645b562ef2917` |
| count-c3.py | `3ecc5c89fd…` | `a2ac2e6930…` | `2e618dce42b38418` | `e5f7214163968d4a` |

Mutated copies (sha256 first 16): M1 `9c36c78aff3dfa7a`, M2 `1887d42fc2d57d08`,
M3 `d3628a3485866438`, M4 `f875d54759b36da2`, M5 `66484e7a9cc7c390`,
M6 `376f02ec3597949a`. Lane HEAD read at start of work: `b9e6f68d887c570909c7bacc8bac86579d850d1d`.

## 8. Commands run (exact)

Setup (scratch; no lane write):

```
S=/fast/scratch/hyaku/mori-r87/Mo87E01C1Arms; mkdir -p "$S"; cd /home/vgpnk/Projects/shokunin/mori-shokunin
git rev-parse --verify '03b66a437e68d493ce0aacd1d80c321cc2e6bf7c^{commit}'
git rev-parse --verify '6fc09d69edbb11e5070ff33258de49f062c0fb9b^{commit}'
git show <rev>:.ufo/waves/round-86/count-c{1,2,3}.py > "$S/<rev>/count-cX.py"
git ls-tree <rev> .ufo/waves/round-86/count-c1.py .ufo/waves/round-86/count-c2.py .ufo/waves/round-86/count-c3.py
```

Every selftest (pristine, mutated, arm-neutered, neutral, entering) used exactly:

```
d=$(mktemp -d -p "$S/tmp"); cd "$d"
TMPDIR="$d" GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null \
  python3 -I <absolute path to copy> --selftest
```

Mutation was applied in Python: `body.count(old)` asserted `== 1`, then `body.replace(old, new)`
written to `$S/mut/<label>/<file>`. Anchors/replacements are the frozen `MUTANTS` tuple:

```
M1 (count-c1.py)  'and not any(e.startswith(("empty-mutation", "unanchored")) for e in extras)' -> 'and True'
M2 (count-c1.py)  'met = (pristine_ok and total > 0' -> 'met = (pristine_ok and total >= 0'
M3 (count-c1.py)  'arms = arms_of(out)[0]' -> 'arms = TARGET_ARMS'
M4 (count-c2.py)  'if token in body:' -> 'if True:'
M5 (count-c2.py)  'if measured == sha:' -> 'if True:'
M6 (count-c3.py)  'if not KEYSHAPE.match(body):' -> 'if False:'
```

Freeze identity:

```
git show 142542e0d853b4e8ec1aa1adb86708dc5786d9c0:<path> | sha256sum   # vs sha256sum <worktree path>
diff -u <(git show 142542e0…:.ufo/waves/round-87/contract.md) .ufo/waves/round-87/contract.md
diff -u <(git show 142542e0…:.ufo/waves/round-87/count-c2.py) .ufo/waves/round-87/count-c2.py
```

## 9. Notes, limits, dead ends

- **M1 shares its assertion text with `unanchored_excluded`** (subject line 230). Neutering by raw
  assertion text would have hit two arms, so the exclusion experiment replaced the whole
  label-scoped `cases.append(("unanchored_plus_killed_unmet", …))` block. `unanchored_excluded`
  stays green under the M1 mutant because its fixture has `total=0`, so `met` remains false via the
  `total > 0` conjunct; the isolating arm is the one whose fixture keeps `total=1`. This is a
  property of the arm design, not a hole: the mutant's conjunct is only observable where a killed
  mutant coexists with an unanchored one, and that arm is exactly that case.
- The M3 kill tail `arms=26` is the r86 counter's `TARGET_ARMS` constant, confirming the mutated
  `arms = TARGET_ARMS` overrode the subject's own `pass=20` reading.
- I did **not** run the frozen `python3 -I .ufo/waves/round-87/count-c1.py <rev>` aggregate; the
  `C1=met mutants=6 killed=6 survivors=0 total=6 arms=54` line is outside this seat's assignment.
  What is established here: six anchors unique, six mutated copies red with exactly the named
  new arm, six arm-only neuters green, tallies 18/13/23 vs 15/11/22, entering survivors 6/6.
- C2 was not touched by this seat.
- No lane file was created, edited or deleted; all lane access was `git show`/`git rev-parse`/
  `git ls-tree`. No commit, checkout, reset, stash or mutating `jj` was run. Scratch under
  `/fast/scratch/hyaku/mori-r87/Mo87E01C1Arms` was deleted with `rm -rf` before this report.
