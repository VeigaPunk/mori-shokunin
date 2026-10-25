# RevAudit — attacking the C2 auditor (round 45, wave 1)

Scope: P-C2's auditor `tools/mori-gate-registry.py` (v2, built this wave). I built
fixture registries under `TMPDIR` and ran the delivered auditor against them, then ran
`--audit-all` at the entering tip and at the worktree. I wrote nothing outside this report
and my scratch dir; I did not edit the auditor, SKILL.md, the contract or another seat's
report.

**Artifact under test.** `tools/mori-gate-registry.py`, git blob
**`8feffe32793c3366d4886b9705c9a6cf22acb771`**, 743 lines, 31165 bytes,
`--selftest` → `GATE_REGISTRY_SELFTEST pass=15 fail=0` rc=0.

The file moved under me **four times** while this seat ran, and my verdicts bind only the
final blob:

| blob | lines | what changed |
|---|---|---|
| `d0aa10e3…` | 600 | first v2: whole-file tables, `entry_target`, duplicates, comment masking |
| `a61c42e2…` | 631 | `bad_row`→`wrong_row` folded into the counter line; empty population is SETUP |
| `f405eb38…` | 724 | `selftest-flag=` escape hardened (name must contain `test`); `--audit`+`--audit-all` together is SETUP; `mode=`/`population_digest=` |
| `8feffe32…` | 743 | `selftest_flag` replaced by an explicit branch test (`_flag_in_python_tests`; shell `case` pattern) instead of a 3-line argv proximity window |

**Two of my findings were closed mid-seat by revisions 3 and 4**: the `--help` escape vector
(F2) and the help-string mention (F1, which was MEDIUM and is now rejected). I re-ran the
entire fixture set against `8feffe32…`; every receipt below is from that blob. The entering-tip
and worktree counters are byte-identical between `f405eb38…` and `8feffe32…`, so the hardening
changed classification of deficient tools only, not the real registry's verdict.

Scratch: `.ufo/waves/round-45/tmp/RevAudit/` — harness `fixtures.py`, logs
`baseline-v1.txt`, `v2-full.txt`, `v2b-full.txt`, `v3-full.txt`,
`v2-bypass-probes.txt`, write-scope sandboxes `ws/`, `ws4/`.
Reproduce: `python3 .ufo/waves/round-45/tmp/RevAudit/fixtures.py tools/mori-gate-registry.py`.

## Headline

I could **not** earn `REGISTRY=met` with a deficient registry on items **1, 2, 3, 5, 6**, in
either direction. Item **4** rejects comment-only mentions, help-string mentions and
`--help`-style escapes; **one narrowed escape survives** (F2: a `test`-named flag that is
dispatched but self-tests nothing). Item **7 is not enforced by the auditor at all**, and the
separate arm's `writescope_mismatch=0` does not mean what item 6's sentence says (F3).

## Item-by-item

Commands are `python3 <auditor> --repo <fixture repo> --rev <sha> --audit <path>`, fixture
repos built fresh under `TMPDIR`.

| # | attack | outcome | rc | counter line |
|---|---|---|---|---|
| 1 | row exists only in a **second** standard 8-cell table | **met** — it counted (correct) | 0 | `registered=1 … tables=2` |
| 2 | **duplicate** row name | unmet (correct) | 1 | `duplicate=1` |
| 3 | row names a **different** tool / only passes the path as an argument | unmet (correct: not attributed) | 1 | `unregistered=1` |
| 4 | self-test cell fine, tool's only `--selftest` is a **comment** | unmet (correct) | 1 | `no_selftest=1` |
| 5 | **seven-cell** row / **empty** cell | unmet (correct) | 1 | `wrong_row=1` |
| 6 | entry path **does not resolve** at `--rev` | unmet (correct) | 1 | `wrong_row=2` |
| 7 | row whose **write-scope cell is false** | **met — the auditor cannot see it** | 0 | `registered=1 … wrong_row=0` |

### 1 — second-table-only row counts; a non-standard table does not

```
### S1 second-table-only row (must count)
audit tools/fixture-tool.sh   PASS row='second gate' (8 cells, entry resolves, --selftest argv branch)
tables=2
registered=1 unregistered=0 no_selftest=0 duplicate=0 wrong_row=0 tables=2
REGISTRY=met
rc=0
```

A second standard table with **no heading** between the two (`S1b`) also gives `tables=2`
and `met`, so parsing does not depend on section boundaries. Independent cross-check of the
real file: the eight-cell header occurs at SKILL.md lines **162, 524, 588, 643, 718, 796,
881** = 7, and the auditor prints `tables=7`. v1 returned `unregistered` here
(`baseline-v1.txt`), which is exactly the `tables=1` defect P-C2 item 1 names.

The inverse boundary also holds — a table with a **non-standard header** is not a registry
table and its rows attribute nothing:

```
### E7 standard table + 3-cell-header table naming tools/b.sh
audit tools/a.sh   PASS row='std gate' (…)
audit tools/b.sh   FAIL (no row names tools/b.sh)
tables=1
registered=1 unregistered=1 … tables=1     REGISTRY=unmet   rc=1
```

### 2 — duplicate name is a finding, including across tables

```
duplicate name='dup gate' lines=7,8
registered=2 unregistered=0 no_selftest=0 duplicate=1 wrong_row=0 tables=1
REGISTRY=unmet   rc=1
```

Cross-table variant (same name in table 1 and table 2): `duplicate name='same name'
lines=7,13 … duplicate=1 rc=1`. Duplicates are scanned over rows from **all** tables, so
whole-file scope and duplicate detection compose.

### 3 — a row that does not name the audited path does not attribute

```
# entry cell: bash tools/runner.sh tools/fixture-tool.sh  (audited path is merely an argument)
audit tools/fixture-tool.sh   FAIL (no row names tools/fixture-tool.sh)
registered=0 unregistered=1 no_selftest=0 duplicate=0 wrong_row=0 tables=1
REGISTRY=unmet   rc=1
```

Same for a row naming `tools/decoy-tool.sh`. **v1 passed both** (`REGISTRY=met`) through its
substring fallback — the r44 defect, now closed. I expected the removal of the fallback to
break the registry's own cell shapes, because v1's strict `entry_names` fails on all three
shapes the real tables use:

- bare backticked cell — `\`bash tools/mori-silence-cases.sh\`` — the trailing backtick
  defeats `(?:\s|$)`;
- `python3 -I [-B] tools/…` — interpreter flags;
- `TMPDIR=… python3 tools/…` — env assignment.

Two of those rows (`mori-silence-cases.sh`, `mori-round19-regressions.py`) exist only in
that shape, so the concern was real. v2's `entry_target` normalises all three and I proved
it on each exact shape:

```
S8  TMPDIR=<dir> python3 tools/fixture-tool.py --mode after  → PASS row='env gate'         met rc=0
S9  bash -x tools/fixture-tool.sh                            → PASS row='flag gate'        met rc=0
S9b python3 -I -B tools/fixture-tool.py [--cases FILE]       → PASS row='real-shape gate'  met rc=0
```

So there is **no** attribution false-negative on the shapes the registry actually uses.

### 4 — comment-only `--selftest` is rejected

```
audit tools/fixture-tool.sh   FAIL row='fixture gate' (row 'fixture gate' tool has no real --selftest argv branch)
registered=0 unregistered=0 no_selftest=1 duplicate=0 wrong_row=0 tables=1
REGISTRY=unmet   rc=1
```

Correct too for `--selftest` only echoed in a usage string (`E1`). The r44 silence-oracle
false positive reproduces in v1 (`met`) and is gone. On the real registry the rule is
right — all four entering-tip `no_selftest` verdicts are true (see "4-vs-3" below). But the
requirement is still beatable: F1 and F2.

### 5 — seven-cell row and empty cell rejected

```
audit tools/fixture-tool.sh   FAIL row='fixture gate' (row has 7 cells, expected 8)      wrong_row=1  rc=1
audit tools/fixture-tool.sh   FAIL row='fixture gate' (row 'fixture gate' missing cells: owner)  wrong_row=1  rc=1
```

The reason string is now exact ("7 cells"), fixing r44's overstatement where the arm
rejected for "all eight cells missing".

### 6 — entry path that does not resolve at `--rev` (or escapes) is rejected

```
audit tools/ghost-tool.py   FAIL row='ghost gate' (row 'ghost gate' entry path tools/ghost-tool.py does not resolve at …)
wrong_row line=7 row='ghost gate' entry=tools/ghost-tool.py absent at …
wrong_row=2   REGISTRY=unmet   rc=1
```

Traversal variant (`../escape-outside.sh`): `FAIL (audited path is absolute or outside the
repo)` plus `wrong_row … absolute or outside the repo`, `rc=1`. The escape is not followed
(the file exists on disk outside the repo and is still refused).

### 7 — a false write-scope cell still prints met

```
# the tool's --selftest writes ./STRAY-WRITE inside the repo; the row says "stdout only, never writes the repo"
audit tools/fixture-tool.sh   PASS row='fixture gate' (8 cells, entry resolves, --selftest argv branch)
registered=1 unregistered=0 no_selftest=0 duplicate=0 wrong_row=0 tables=1
REGISTRY=met   rc=0
```

The auditor has no write-scope logic (the cell is only checked for non-emptiness). Item 6
therefore rests entirely on the separate arm — and that arm's zero does not establish the
clause. See F3.

## `--audit-all` receipts

Population rule, verified by importing the tool's own `population()`: at `WORK` **n=39**
(tools=33, round-44 `count-c*=3`, round-45 `count-c*=3`); at the entering tip **n=36** (the
round-45 counters did not exist). In both receipts below
`registered+unregistered+no_selftest` equals the population.

**Entering tip `554ff416`** — `python3 tools/mori-gate-registry.py --rev 554ff416 --audit-all`, **`rc=1`**:

```
registered=29 unregistered=3 no_selftest=4 duplicate=0 wrong_row=0 tables=7
mode=population
population_digest=4dbf0ca9823d2af1d6de352b54138bbc261c68a10c9a81e6ef77eb88576292f1
REGISTRY=unmet
```

- **unregistered (3)** — the three orphans: `tools/mori-disk-rate.py`,
  `tools/mori-round41-calibration.py`, `tools/mori-wave-settlement.py`. Each is named only
  in a *section heading* (e.g. `## Round34 — two-sample disk write rate tool (FR6;
  tools/mori-disk-rate.py)`), never in a table row.
- **no_selftest (4)** — `tools/mori-round19-regressions.py` (0 occurrences),
  `tools/mori-routed-check.py` (0), `tools/mori-silence-cases.sh` (comment only),
  `tools/mori-routed-r24.py` (4 occurrences, none a branch — table below).

**Worktree `WORK` at 2026-10-25T07:53:35-03:00** (after the residual seat landed), **`rc=1`**:

```
registered=33 unregistered=6 no_selftest=0 duplicate=0 wrong_row=0 tables=7
mode=population
population_digest=2d1e9096f7622639f3bb45624ffee594caa81c05ee200c9a22323f86d4a9c056
REGISTRY=unmet
```

- **unregistered (6)** — `.ufo/waves/round-45/count-c1.py`, `count-c2.py`, `count-c3.py`
  (their rows are still being drafted) plus the same three orphans (`mori-disk-rate.py`,
  `mori-round41-calibration.py`, `mori-wave-settlement.py`). All six are the drafted-row
  integration item, not an auditor defect.
- **no_selftest (0)** — reached. `mori-routed-r24.py` gained a real branch
  (`if "--selftest" in raw: return _selftest_dispatch(raw)`, L1469) that runs before argparse
  and prints `ROUTED_R24_SELFTEST pass=26 fail=0` rc=0. I watched this counter fall **4 → 2 →
  1 → 0** across four runs as `mori-round19-regressions.py`, `mori-routed-check.py`,
  `mori-silence-cases.sh` and finally `mori-routed-r24.py` landed.
- The worktree is live, not frozen: `count-c3.py` and the three selftest edits landed between
  my runs, and `registered` moved 30 → 31 → 32 → 33.

**Status against the C2 target.** `no_selftest=0` is achieved and `duplicate=0`,
`wrong_row=0` hold. The only remaining counter is `unregistered=6`, which needs the six
drafted SKILL.md rows to be integrated. A fully green run must read **`registered=39`** (the
population) — 33 + 0 + 0 with `unregistered=0`; if a run reports `registered=32` with
`unregistered=0 no_selftest=0`, seven population members were dropped from the audit, which
is the undercount class this claim exists to catch.

## The 4-vs-3 `no_selftest` class (witness for the round's lesson)

The wave-1 item set named **three** tools lacking a real self-test; the v2 auditor found
**four**. I checked all four against the bytes and **every verdict is true**:

| tool | occurrences | why it is not a branch |
|---|---|---|
| `mori-round19-regressions.py` | 0 | — |
| `mori-routed-check.py` | 0 | — |
| `mori-silence-cases.sh` | 1 | L20 comment: `#  Each case runs the actual census CLI (bash "$CENSUS", no --selftest)` |
| `mori-routed-r24.py` | 4 | L19 docstring; L96 `EVIDENCE_COMMAND` constant; L399 docstring; L422 a subprocess argv list that runs ***mori-pressure.py*** `--selftest`. Its own argparse is `--repo/--rev/(--rerun)` (L892-903) |

`mori-routed-r24.py` was assigned to no wave-1 item (`grep -c mori-routed-r24` = 0 over
`w1-spec.json`, `w1-dispatch.json`, `contract.md`), so `no_selftest=0` was unreachable until
the residual seat was created. That is the round's instrument-undercount lesson, **not** a
reason to widen the predicate: the auditor was right and the inventory was wrong. Worth
keeping: the classifier refuses a tool that merely *invokes another tool's* `--selftest` — a
sharper property than "the string occurs".

## Findings

### F1 — CLOSED mid-seat (was MEDIUM on `d0aa10e3…`/`a61c42e2…`/`f405eb38…`) — `--selftest` in another argument's help string

Against `d0aa10e3…`–`f405eb38…` this earned `met` for a tool with no branch:

```
audit tools/fixture-tool.py   PASS row='fixture gate' (8 cells, entry resolves, --selftest argv branch)
registered=1 unregistered=0 no_selftest=0 duplicate=0 wrong_row=0 tables=1
REGISTRY=met        rc=0
```

Tool body — the flag is never parsed:

```python
ap.add_argument("--verbose", action="store_true",
                help="see --selftest for the test suite")
```

`selftest_flag()`'s `PY_ARGV` marker matched `add_argument` inside a three-line window. On
`8feffe32…` the same fixture is **rejected**:

```
audit tools/fixture-tool.py   FAIL row='fixture gate' (row 'fixture gate' tool has no real --selftest argv branch)
no_selftest=1   REGISTRY=unmet   rc=1
```

The fix is the right one: `_flag_in_python_tests` requires the flag literal to sit in a
parser key, a comparison, or a membership test against an argv-like name, instead of being
merely near an argv-ish token. Kept here as the record that the class existed and that the
replacement closes it.

### F2 — LOW — the `selftest-flag=` escape still certifies a tool that self-tests nothing

The `--help` vector I first found is closed in `f405eb38…` (`escape_branch` requires `test`
in the flag name). But the guard is a **name substring**, not evidence that the branch tests
anything:

```
$ python3 tools/mori-gate-registry.py --repo <tmp>/e5b/repo --rev <sha> --audit tools/fixture-tool.sh
audit tools/fixture-tool.sh   PASS row='fixture gate' (8 cells, entry resolves, --test-fixtures argv branch)
registered=1 unregistered=0 no_selftest=0 duplicate=0 wrong_row=0 tables=1
REGISTRY=met
rc=0
```

with

```sh
#!/bin/sh
case "${1-}" in
  --test-fixtures) echo "no fixtures"; exit 0 ;;
esac
exit 0
```

and row self-test cell ``bash tools/fixture-tool.sh --test-fixtures`` (selftest-flag=--test-fixtures).
`met` for a tool whose only branch prints a sentence. **Do not close
`mori-routed-r24.py` this way**: it had no self-test branch under any flag, so a
`selftest-flag=` row would have been precisely the false claim C2 exists to stop. The round
did not rely on the escape — the residual seat added a real 26-arm branch, and the auditor
recognises it.

### F2a — LOW — the escape's rejection reason names the wrong failed condition

For `selftest-flag=--help` on a tool that *does* have `--help) echo "usage: fixture"; exit 0 ;;`:

```
FAIL row='fixture gate' (row 'fixture gate' declares selftest-flag --help, but
tools/fixture-tool.sh has no --help parser key or case pattern (a self-test flag name
must also contain 'test'))
```

The case pattern exists. `escape_branch` returns at the name gate (L333-334) before it ever
looks for the pattern, so the message asserts a measurement it did not make. A row author
would hunt a pattern that is present. Report the failing clause only.

### F3 — MEDIUM — item 7's receipt does not measure the claim the cells make

The separate arm at the entering tip:

```
TRUE: r44-figure-ledger-c1, r44-gate-conformance-c2, r44-corpus-coverage-c3, r44-gate-registry-c2
FALSE: -   UNEXERCISED: -   UNAVAILABLE: r45-count-c1, r45-count-c2, r45-count-c3
WRITESCOPE instruments=7 true=4 false=0 unexercised=0 unavailable=3 writescope_mismatch=0 \
  rev=554ff416459c92f0dea9762f834a556df2990187
WRITESCOPE=met   rc=0
```

That contradicts round-44 F8 for the same cells, and **the bytes say F8 was right**. The
cell `r44 gate registry (C2)` claims "the selftest writes only under the caller TMPDIR". Run
the *revision's own* auditor with an inherited `GIT_DIR` — the exact condition F8 named:

```
victim files: before=28 after=46 created=18
./HEAD ./config ./description ./hooks/applypatch-msg.sample …
# the same invocation with the current auditor: rc=0, created=0
```

18 files written outside `TMPDIR`, at the revision the arm audited, by the instrument whose
cell forbids it — and the arm returned TRUE for that row. Two structural reasons:

1. `fixtures/write-scope.json` carries a `claim` per entry that is **narrower** than the
   cell it prints as `declared=`: "the instrument writes no file inside the repo; its
   selftest writes only under the caller TMPDIR". That drops the cell's "reads the repo at
   `--rev`" clause — the clause under which count-c1 executes committed git pipelines.
2. Every entry's `command` is the instrument's `--selftest`, so no production path is ever
   exercised and no sentence about production behaviour can be falsified.

Net: `writescope_mismatch=0` is true, `WRITESCOPE=met` prints, and item 6's English clause
("the audited write-scope cells make no false claim") is false at the revision audited. At
the *worktree* this particular cell is now true (the current auditor scrubs `GIT_*`), so the
damage is to the evidence rather than to today's cells — but the arm cannot tell the two
apart, and the frozen predicate reads only the zero.

### F4 — LOW — a genuine `--selftest` branch can be rejected (false negative)

```
$ python3 tools/mori-gate-registry.py --repo <tmp>/repos/e6-true-branch-narrow --rev <sha> \
      --audit tools/fixture-tool.py
audit tools/fixture-tool.py   FAIL row='fixture gate' (… no real --selftest argv branch)
no_selftest=1   REGISTRY=unmet   rc=1
```

Tool: `def main(a): if "--selftest" in a: … ; sys.exit(main(sys.argv[1:]))` — a real branch,
rejected because `_flag_in_python_tests` allows a membership test only against a fixed
argv-name allowlist (`raw|argv|args|sys.argv|arguments|options|opts|tokens|words`) and the
parameter here is `a`. No real tool is affected today (all four true verdicts are genuine),
but a false `no_selftest` is the mirror image of the false `registered` the claim exists to
prevent — and this allowlist is a new, narrower surface than the proximity window it
replaced.

### F5 — LOW — `wrong_row` double-counts one row

In the item-6 fixture a *single* malformed row yields `wrong_row=2`: once from
`stats["wrong_row"]` for the attributed target failing resolution, once from the
`wrong_rows` registry scan. Met/unmet is unaffected, but a counter consumer cannot tell one
bad row from two.

## Residual risk / not verified

- I did not audit `.ufo/waves/round-45/count-c2.py`'s composition of these counters (another
  seat owns it); if it gates on the counter line it inherits F3's blind spot and F5's
  arithmetic.
- The auditor moved four times during this seat. Verdicts bind `8feffe32…`; any later edit
  needs `fixtures.py` re-run.
- The worktree receipt is a live snapshot (07:53:35), not a landed tip: `unregistered=6` is
  state, not a final verdict. `no_selftest=0` is real and measured.
- Not exercised: `--registry` pointing outside `SKILL.md`, an unresolvable `--rev`, a git
  timeout, CRLF registries, and a registry whose header differs only in spacing.
- No tool was installed or upgraded for this seat (none needed); no network call was made;
  no pacman transaction was run.

## Verdict on the attack

Items **1, 2, 3, 5, 6** are enforced — I could not earn `met` on any of them, in either
direction (no bypass, and no false finding on the registry's real cell shapes). Item **4**
now holds against comments, against help-string mentions (F1, closed mid-seat) and against
the `--help` escape; it still yields `met` for a tool with no self-test branch through a
`test`-named flag that is dispatched but tests nothing (F2). Item **7** is outside the
auditor entirely, and the arm's zero does not establish the clause it is cited for (F3).

Net: the claim's auditor is honest about items 1–6 as written, with one narrow escape on
item 4 and one arm-scoping gap on item 6. Nothing in this report argues C2 is met — at the
last measurement it reads `registered=33 unregistered=6 no_selftest=0`, and `unregistered=0`
is an integration step the L1 still owes.
