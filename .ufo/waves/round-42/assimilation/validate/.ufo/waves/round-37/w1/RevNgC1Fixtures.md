# w1/RevNgC1Fixtures — realism attack on the three C1 negative fixtures

Attacks: `fixtures/memo-n1.py`, `fixtures/const.py`, `fixtures/summary-only.py`
(frozen `freeze-r37.txt`; unchanged in `freeze-r37-v3.txt`) and the judging they
stand in for — `.ufo/waves/round-37/count-c1.py:842-858` (`run_negative`).

## Fixture audit

| fixture | key / trick | kills it | realistic? |
|---|---|---|---|
| `memo-n1.py` | honest iff `git config --local user.name == "mori counter"` (memo-n1.py:30-32); published constant elsewhere | challenge arm's lane identity (`count-c1.py:815-816`) | **weak** — keys on environment, never on the measured input. A submitter who can read the counter source (it is in-tree) keys on the one thing the real arm cannot vary: the history itself |
| `const.py` | unconditional constant | blind draw | control; fine |
| `summary-only.py` | honest delegate minus `deleted` lines | per-id check | adequate for the narrow per-id grammar claim |

The memoizer exemplar is the weak one. The claim says "a real-arm memoizer" as a
class; the battery only exercises the class member that classifies by
*environment*. The realistic member classifies by *content*.

## Attack fixtures (built in `/fast/scratch/hyaku/mori-r37/RevNgC1Fixtures/`)

- **`memo-sha.py`** — sha256 of `git log --format=%H --reverse <rev> --
  corpus/SOURCES.md` == memorized lane-chain digest
  (`58179d63…`, the 47-commit chain at 6bd57097) ⇒ print the published constant
  + 18 `changed` lines, `return 1`, never reading a registry row. Every other
  history delegates to the honest gate. Content key: survives path checks,
  identity clothing, rev renaming, and the drawn arm.
- **`memo-len.py`** — the assignment's example: recompute only when the history
  is short (<20 commits ⇒ delegate; ≥20 ⇒ constant). Expected to die on long
  lane-history probes.
- **`memo-table.py` + `table.json` (built by `build_table.py`)** — precomputes
  the counter's own `oracle()` answer for **every rev `draw_real_rev` can
  choose** (the 29 of last-40 `rev-list HEAD` revs carrying the tool with a
  parent, `count-c1.py:762-775`) plus the real arm — 30 `(chain_sha, base_sha)`
  keys. On any lane-history input it replays a stored answer; only fresh
  (challenge/blind) histories delegate. No appendonly analysis is ever run for
  a measured lane input.

## Measurements (counter = working-tree `count-c1.py`, blob `3e15f9fd`, sha256
`5279ed9d` — the v2 counter pinned by `freeze-r37-v3.txt`; "v1" runs replay the
frozen blob `7518fef8` extracted to scratch, never editing the lane)

**Subject runs** (`count-c1.py e57c58b… --tool <fixture>`):

| run | fixture | counter | result |
|---|---|---|---|
| A (seed 7316774888929676074, 5736150416745720704) | memo-sha | v2 | blind 24/24, real pass, **drawn pass**, challenge pass → `C1=met`, exit 0 |
| B (seed 7381930386425195158) | memo-len | v2 | **drawn FAIL** (ancestor rev's constant differs), rest pass → `C1=unmet` |
| E (seed 9603065918689219940) | memo-len | **v1** | all pass → `C1=met` |
| F (seed 16755777699435452218) | memo-sha | **v1** | all pass → `C1=met` |
| G (seed 2488844468156318482) | memo-table | v2 | all pass; drawn arm `rev=9ca8f2eb4f` answered **from the table** → `C1=met` |

**Negative-slot runs** (`--negatives <dir>` where `memo-n1.py` is my fixture;
subject = the honest gate at e57c58b):

| run | slot occupant | counter | line |
|---|---|---|---|
| C | memo-sha | v2 | `negative memo-n1.py ACCEPTED (all three arms pass)` → `C1=unmet`, exit 1 |
| D | memo-len | v2 | `negative memo-n1.py ACCEPTED` → `C1=unmet` |
| H | memo-table | v2 | `negative memo-n1.py ACCEPTED`; drawn arm `rev=4890c2d571` replayed from table → `C1=unmet`, exit 1 |
Full transcripts: `/fast/scratch/hyaku/mori-r37/RevNgC1Fixtures/runs/`.

## Findings

- **F1 (HIGH) — the memoizer negative does not represent its class.** The
  counter ACCEPTS a chain-hash-keyed memoizer in the negative slot (runs C, H)
  and scores it `C1=met` as subject (runs A×2, G). On the real arm it prints a
  stored answer *without reading a row* — a true memoizer, strictly stronger
  than the exemplar. P-C1's "rejects … a real-arm memoizer" holds only for
  environment-keyed members.
- **F2 (MED) — the negative judge is weaker than the subject judge.**
  `run_negative` (count-c1.py:842-858) runs blind(4)/real/challenge only; the
  subject path additionally runs `real_draw_arm` (main flow, count-c1.py:973).
  memo-len is `ACCEPTED` as a negative (run D) yet `FAIL` as a subject (run B)
  — the battery admits fixtures the counter itself would catch.
- **F3 (named bypass, class-level) — content-keyed memoization + honest
  delegation is undetectable by this counter.** Partition the probes: lane-history
  inputs (real arm fixed; drawn arm enumerable — 29 candidates, all
  precomputable, run G proves it by table lookup) are keyable; fresh histories
  (blind, challenge) are unkeyable but are delegated and answered honestly.
  No arm can distinguish replay from compute when the answer is identical —
  the counter's own docstring concedes the narrower rev-literal case
  (`count-c1.py:758-761`: "defeats every such key except the arm's own rev
  literal … (disclosed residual)"); the chain digest exceeds that residual
  (survives `HEAD` vs full-sha spelling, rev rotation, worktree moves). The
  only remaining lever is white-box (forbidding delegation/vendored compute),
  which the counter does not check.
- **F4 (corroborating) — the drawn arm's actual coverage is "constant property
  of the history", not "memorization".** It kills exactly the keys that fire on
  *other* lane revs (memo-len, run B) and nothing else (memo-sha run A,
  memo-table run G). The corpus itself draws shallow: `build_sandbox` produces
  5–9 commits (count-c1.py:430,434 — `rng.randint(6,12)` rows +
  `rng.randint(4,8)` op commits), so length gating was never at risk there.

## Fixture verdicts

`memo-n1.py`: **weak stand-in** — defeated by the challenge arm only because its
key is environmental; the class survives. `const.py`: adequate control.
`summary-only.py`: adequate for its narrow claim.

## Environment / provenance

Lane counter measured = v2 (`3e15f9fd`, `freeze-r37-v3.txt`), landed at
`4bfa0490` mid-wave (contract A1 amendment, contract.md:127-136); v1
(`7518fef8`, `freeze-r37.txt`) measurements replayed from the extracted blob
for completeness. Scratch only: `/fast/scratch/hyaku/mori-r37/RevNgC1Fixtures/`
(no lane files touched; counter writes its own challenge repos under
`.ufo/waves/round-37/scratch/` by design and removes them). Installs: none.

VERDICT: FAIL — the three negative fixtures are weak stand-ins; a stronger
real-arm memoizer (chain-hash key, honest delegation off-key, or a
precomputed per-rev table covering the drawn arm's enumerable space) passes all
four subject arms (`C1=met`, exit 0) and is ACCEPTED in the negative slot.
Bypass: content-keyed memoization on the lane's commit-chain digest;
`count-c1.py:755-799` (drawn arm residual), `count-c1.py:842-858`
(no drawn arm in `run_negative`), `fixtures/memo-n1.py:30-32` (environment key).
