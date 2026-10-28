# Mo59Reviewer13 — C1+C2 counter cross-check (frozen target tokens vs counter-emitted tokens)

**Seat:** Mo59Reviewer13 (reviewer) · **Scope:** verify the frozen target output
tokens in `contract.md` are exactly the tokens `count-c1.py` and `count-c2.py`
emit; report any token not emitted. **Result: NO COUNTEREXAMPLE** — every
frozen target token is emitted; token sets are identical modulo two
contract-licensed exceptions detailed below.

## Verdict

| Claim | Contract target (frozen) | Emitted at freeze `60b3a76a` | Token-set verdict |
|---|---|---|---|
| C1 | `C1=met selftest=ok fixtures=ok real=ok pointers=ok rev=R` | `C1=met selftest=ok fixtures=ok real=ok pointers=ok rev=60b3a76a…` | **exact equality** (6/6 tokens, same order) |
| C2 | `C2=met selftest=ok scan=ok drift=ok trees=ok entry=ok rows=ok pins=ok tree=ok claims=N files=F rev=R` | `C2=unmet selftest=ok scan=ok drift=ok trees=ok entry=bad rows=bad pins=bad tree=bad claims=0 files=0 rev=60b3a76a… failed=…` | **all 12 target tokens emitted**; sole extra token is `failed=`, contract-licensed on the unmet line only |

**No target token is missing from either counter's emit path. No adversarial
finding on the token-equivalence axis.**

## Method (bounded)

Freeze revision `60b3a76ad0524c8978cc51922940be1c8c388915`, entering
`2b9f03975bfb6e508f35074ac8181ec8bf54e805`, HEAD `8ff344ff18924c…`. All reads
read-only (`git show`/`ls-tree`/`cat-file`); counters executed from
byte-extracted freeze copies under `$HYAKU_SCRATCH/mori-r59/Mo59Reviewer13/`
with `--scratch` + `TMPDIR` confined there. No lane/VCS mutation.

1. **Freeze integrity.** `git diff 60b3a76a -- contract.md count-c1.py
   count-c2.py` → empty; `git log 60b3a76a..HEAD -- <those paths>` → empty.
   Extracted copies SHA-256 identical to worktree:
   count-c1 `2be6fda8…0c9dfd`, count-c2 `2df3ae84…75e7be`, contract
   `427fca0b…17e`. Frozen bytes are the bytes reviewed.
2. **Static emit-format extraction.** Each counter has exactly one result-line
   print site (verified by grep for `print(`): count-c1.py:262–272,
   count-c2.py:452–459. Token names lifted from the format strings.
3. **Dynamic runs at freeze and at entering** (freeze copies,
   `--scratch` under seat scratch). Outputs below.
4. **Token-set diff** (script: split each side on whitespace, compare key sets
   bidirectionally) — contract target vs emitted@freeze vs static emit order.
5. **Adversarial checks** — see §4.

## 1. C1

Contract target (contract.md:41): `` `C1=met selftest=ok fixtures=ok real=ok
pointers=ok rev=R`, exit 0 ``.

Emit site (count-c1.py:262–272):
```python
line = ("C1=%s selftest=%s fixtures=%s real=%s pointers=%s rev=%s"
        % ("met" if met else "unmet", "ok" if detail.get("selftest") else "bad",
           "ok" if "fixtures_absent" not in failed
               and not any(f.startswith("fixture") for f in failed) else "bad",
           "ok" if detail.get("real") else "bad",
           "ok" if detail.get("pointers") else "bad", rev))
if not met:
    line += " failed=" + ",".join(failed) if failed else " failed=unknown"
```
Static token set `{C1, selftest, fixtures, real, pointers, rev}` ≡ contract
target token set; `failed=`/`failed=unknown` only when `not met`
(contract.md:43 licenses `C1=unmet … failed=…`; the `…` covers additional
reason tokens).

Observed:
```
$ python3 count-c1.py --selftest          → C1_SELFTEST pass=6 fail=0, exit 0   (contract.md:54 ✓)
$ python3 count-c1.py 60b3a76a --scratch … → C1=met selftest=ok fixtures=ok real=ok pointers=ok rev=60b3a76ad0524c8978cc51922940be1c8c388915, exit 0
$ python3 count-c1.py 2b9f0397 --scratch … → C1=unmet selftest=bad fixtures=bad real=bad pointers=bad rev=2b9f0397… failed=tool_absent,selftest,fixtures_absent,real,pointers, exit 1
```
The freeze run **dynamically emits the exact met target line** (the tool at
frozen PIN `38b733d8…472b8` is already committed pre-data, 13 fixtures under
`fixtures-c1/` — ls-tree count verified — and SCORECARD/pinned fleet
`MANIFEST.json@2807c6ab` all resolve). Token diff at freeze: `[]` both
directions.

## 2. C2

Contract target (contract.md:69): `` `C2=met selftest=ok scan=ok drift=ok
trees=ok entry=ok rows=ok pins=ok tree=ok claims=N files=F rev=R` (N ≥ 10,
F ≥ 3), exit 0 ``.

Emit site (count-c2.py:452–459):
```python
line = ("C2=%s selftest=%s scan=%s drift=%s trees=%s entry=%s rows=%s "
        "pins=%s tree=%s claims=%d files=%d rev=%s"
        % ("met" if met else "unmet", tok("selftest"), tok("scan"),
           tok("drift"), tok("trees"), tok("entry"), tok("rows"),
           tok("pins"), tok("tree"), detail["claims"], detail["files"], rev))
if not met:
    line += " failed=" + ",".join(failed)
```
Static token set `{C2, selftest, scan, drift, trees, entry, rows, pins, tree,
claims, files, rev}` ≡ contract target token set; `failed=` only when
`not met` (contract.md:71 + docstring "+ ` failed=`" license it).

Observed:
```
$ python3 count-c2.py --selftest          → C2_SELFTEST pass=9 fail=0, exit 0   (contract.md:84 ✓)
$ python3 count-c2.py 60b3a76a --scratch … → C2=unmet selftest=ok scan=ok drift=ok trees=ok entry=bad rows=bad pins=bad tree=bad claims=0 files=0 rev=60b3a76a… failed=copy_absent:…×6,entry_absent,tree, exit 1
$ python3 count-c2.py 2b9f0397 --scratch … → C2=unmet selftest=bad scan=bad drift=bad trees=bad entry=bad rows=bad pins=bad tree=bad claims=0 files=0 rev=2b9f0397… failed=copy_absent:…×6,drift,entry_absent,scan,selftest,tool_absent,tree,trees,trees_absent, exit 1
```
At freeze the C2 claim-time data (entry `wave-settlement-artifacts-r59.md` +
6 `corpus/evidence/sources-r59/` copies) does not yet exist — expected: those
are the C2 axis's round-59 payload — so the line is unmet, but every one of
the 12 frozen tokens is still emitted with its correct name (`bad`/`0`
values), proving name-level emission. The met-branch token set is determined
solely by the same literal format string: `claims`/`files` are `%d` and on a
met line are forced ≥10/≥3 by `MIN_CLAIMS`/`MIN_FILES` via `claims_min`/
`files_min` reasons gating `entry_ok` (count-c2.py:130–135, 303–305).
Token diff at freeze: contract−emitted `[]`; emitted−contract `['failed']`
(licensed, unmet-only).

## 3. Token-set diff summary

```
C1: contract {C1 selftest fixtures real pointers rev}
    emitted  {C1 selftest fixtures real pointers rev}          → identical
C2: contract {C2 selftest scan drift trees entry rows pins tree claims files rev}
    emitted  {…same 12…} (+ failed on unmet line only)          → contract ⊆ emitted
Statically missing tokens: none (C1, C2). Extra tokens on met line: none.
```

## 4. Adversarial checks (all pass)

- **Hidden/duplicate tokens:** single print site per counter (grep-verified);
  format literals contain exactly the listed `%s`/`%d` slots; no token can be
  dropped or added by data.
- **`failed=` scope:** emitted iff `not met` (c1:270–271, c2:457–458); contract
  unmet forms carry the `…` ellipsis licensing additional reason tokens.
  C1's `failed=unknown` fallback is unreachable (unmet ⇒ at least one arm
  appends to `failed`).
- **`claims`/`files`:** emitted as `%d` unconditionally; on met, `entry_ok`
  requires ≥10 claims and ≥3 distinct cited files — the format can emit any
  int, but met forces the contract's `N ≥ 10, F ≥ 3`.
- **`rev=R`:** echoes argv verbatim (c1:269 `rev`, c2:456 `rev`) — always
  present, placeholder matches.
- **Fixture/tree arm shapes:** 13 entries under `fixtures-c1/`, 12 under
  `trees-c2/` at freeze (ls-tree counts) — match contract §9 counts.
- **Before arms:** both counters at entering `2b9f0397` emit
  `…=unmet … failed=…tool_absent…` exit 1 — matching contract.md:43,71
  (C2's longer reason list is inside the `…` license).
- **Selftests at freeze:** `C1_SELFTEST pass=6 fail=0`,
  `C2_SELFTEST pass=9 fail=0`, exit 0 each (contract.md:54,84).
- **Tool pins:** `git show 60b3a76a:tools/mori-register-check.py | sha256sum`
  = `38b733d8…472b8` = PIN (count-c1.py:46);
  `tools/mori-settlement-scan.py` = `4c04bf21…5ac9a9` = PIN (count-c2.py:53).
- **Read-only discipline:** both tools are subprocess/git-free (grep: no
  `subprocess`, `git` calls; writes confined to `TMPDIR`-confined selftest
  roots), so the counters' real-arm `python3` invocations cannot mutate repos.

## 5. Residual risk / verification gaps

- **Met C2 line not dynamically witnessed** — impossible at freeze by design
  (entry+copies land later this round). Statically airtight: one literal
  format string determines the token set, and each arm-token name was
  exercised dynamically on the unmet line.
- **Cosmetic:** when ENTRY exists but any copy is absent, `entry_ok` goes
  `bad` without appending a bare `entry` reason (the `have_all` branch,
  count-c2.py:295–298 appends only `entry_absent` when ENTRY itself is
  missing). `met` is still correctly false via `copy_absent`/`tree` — a
  diagnostics-loudness nit, not a token or verdict defect.
- **Scope bound:** this seat checked token-name equality only; whether each
  arm's `ok`/`bad` is *computed* correctly (fixtures, quotes, pins, rows) is
  other seats' scope.

**Bottom line:** routed defect #3's requirement — "frozen C1 whose every
required output token is emitted by the counting command" (and the same for
C2) — holds for the frozen byte stream at `60b3a76a`. No token in either
frozen target is absent from its counter's emit path; no unexpected token
appears on a met line.
