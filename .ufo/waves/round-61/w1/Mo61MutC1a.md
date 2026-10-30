# Mo61MutC1a — mutation test of `.ufo/waves/round-61/count-c1.py` (round 61, C1)

Seat: mutation-tester (wave 1, 64 seats). Lane: mori-shokunin.
Lane repo: `/home/vgpnk/Projects/shokunin/mori-shokunin`
Under test: `.ufo/waves/round-61/count-c1.py` (frozen; sha256
`a6684e697583746e8b6318d6984f3ada5e619c45a0a3449ecf46d79193433e00`, git blob
`ed6f3c1338f894663e4b53e4b6b451ac2c2f2f51` at freeze rev `7370a731abcafc4c803111de7c22cd6264d63be1`).
Entering revision `325f7e639916fcbc77fa2ec7475951a1b86bb1cb`.
Scratch: `/fast/scratch/hyaku/mori-r61/Mo61MutC1a/` (TMPDIR set to
`…/Mo61MutC1a/scratch` for every counter invocation; `--scratch` passed explicitly).

**Scope:** detection and report only. No production file was modified; no VCS
state was mutated; no commit was made anywhere; no sibling/fleet path was
written. No counter/contract change is proposed — findings and a draft block
only, for the L1.

---

## 1. Verdict summary

| Mutant | Arm dropped | Committed witness that kills it | Verdict |
|---|---|---|---|
| `mut-dup` | dup arm (`count-c1.py:99-102`) | **none** | **SURVIVED → ROUTED DEFECT** |
| `mut-thin` | thin / empty-cell arm (`count-c1.py:104-108`) | committed selftest case `thin` | **KILLED** |
| `mut-noselftest` | `--selftest` arm (`count-c1.py:109-112`) | committed selftest case `noselftest` | **KILLED** |

**Headline finding (F1, routed defect): the C1 dup arm has no committed
witness.** The mutation that deletes the duplicate-row check
(`if len(live) > 1:` → `if False:`) survives *every* committed witness of the
counter — the frozen `--selftest` battery, the committed do-nothing control,
and the freeze-revision run — and reproduces the committed selftest receipt
**byte-for-byte**. It is killed only by a hostile fixture I had to construct
myself in scratch (two live rows for one path), i.e. by a witness that does
not exist in the committed evidence set. The contract's kill rule explicitly
names this condition ("two non-superseded rows", `contract.md:46-48`), so the
arm is load-bearing for the claim yet untested by the committed battery.

Two secondary findings from the same read: the `unres` arm
(`count-c1.py:113-116`) is also unreachable from its own committed selftest
case (the case named `unres` actually fails earlier at `missing`), and the
`noowner` counter has no increment site anywhere in the file, so the
`noowner=0` token in the frozen met line (`contract.md:42`) is a constant, not
a measurement. Both are coverage findings, not contract changes — reported
here, not fixed.

---

## 2. Method

1. Copied the frozen counter into scratch (`pristine-count-c1.py`) and made
   three one-line mutants (`mut/`). Each mutant differs from pristine by
   exactly one line (`diff | grep -c '^[<>]'` → 2 per mutant: one `-`, one `+`).
2. Built the mutant by editing **only the scratch copy**; the production file
   was never opened for writing. Verified before and after the whole run:
   `sha256sum .ufo/waves/round-61/count-c1.py` →
   `a6684e697583746e8b6318d6984f3ada5e619c45a0a3449ecf46d79193433e00`
   (unchanged), `git status --porcelain -- .ufo/waves/round-61/count-c1.py` →
   empty, `git diff --stat HEAD` → empty.
3. Drove each mutant through, in order:
   * **W1 — committed witness:** the counter's own `--selftest` battery
     (frozen receipt at `.ufo/waves/round-61/evidence/selftest-c1.txt`).
   * **W2 — committed witness:** the committed do-nothing control state
     (frozen receipt at `evidence/control-c1-do-nothing.txt`, entering rev).
   * **W2b — committed state:** the freeze revision `7370a731` (current
     committed tree, pre-data).
   * **W3 — my own scratch hostile fixtures** (NOT committed witnesses): one
     fixture per arm, each a throwaway `git init` repo at an explicit scratch
     path, to show the mutation is behaviour-bearing rather than a no-op.
4. Supplementary cross-counter probe: does C3's `livepins` sha arm catch a
   dup-arm mutant committed into the measured tree? (Section 5.)

Fixture note (my own harness bug, corrected): the first harness build omitted
the newline after the `|---|` separator, which merged row 1 into the separator
line; `parse_tables` (`count-c1.py:40-59`) then silently produced zero rows and
every scenario read `missing`. Corrected in `harness2.py`; all results below
come from the corrected run. The corrected fixture builder reproduces the
counter's own `table()` shape (`count-c1.py:133-136`).

---

## 3. The three mutants (exact diffs)

```
--- pristine-count-c1.py            +++ mut/mut-dup-count-c1.py
@@ -96,7 +96,7 @@
         live = [r for r in hits
                 if "supersed" not in r["name"].lower()
                 and "supersed" not in r["scope"].lower()]
-        if len(live) > 1:
+        if False:  # MUTANT mut-dup: dup arm dropped
             res["dup"] += 1
             res["failed"].append("dup:%s" % path)
             continue

--- pristine-count-c1.py            +++ mut/mut-thin-count-c1.py
@@ -102,7 +102,7 @@
         row = live[0] if live else hits[0]
         empty = [k for k in CELLS if not row[k]]
-        if empty:
+        if False:  # MUTANT mut-thin: empty-cell (thin) arm dropped
             res["thin"] += 1
             res["failed"].append("thin:%s:%s" % (path, ",".join(empty)))
             continue

--- pristine-count-c1.py            +++ mut/mut-noselftest-count-c1.py
@@ -106,7 +106,7 @@
             res["thin"] += 1
             res["failed"].append("thin:%s:%s" % (path, ",".join(empty)))
             continue
-        if "--selftest" not in row["selftest"]:
+        if False:  # MUTANT mut-noselftest: --selftest arm dropped
             res["noselftest"] += 1
             res["failed"].append("noselftest:%s" % path)
             continue
```

Mutant sha256 (scratch copies only):
`mut-dup` `d2f7b327439dd76fabd5fa2ae63726315ef5065c5095e994698885c6771613cf`;
`mut-thin` `278168f412738527f90f6ffa6a8aeaa0d8ad8df0bdb42e3bb51c0b5d133f7ba4`;
`mut-noselftest` `1b05510f89e078f69170add4f6bc5149a77dc792c468a726b4f6e9e5eb4421b7`.

---

## 4. Kill table (actual outputs)

### W1 — committed witness: `--selftest` battery

Baseline (pristine), identical to the frozen receipt
`.ufo/waves/round-61/evidence/selftest-c1.txt`:

```
case good: ok=True want=True pass failed=[]
case missing: ok=False want=False pass failed=['missing:tools/absent.py']
case thin: ok=False want=False pass failed=['thin:tools/h.py:owner']
case noselftest: ok=False want=False pass failed=['noselftest:tools/i.py']
case superseded-ok: ok=True want=True pass failed=[]
case unres: ok=False want=False pass failed=['missing:tools/nothere.py']
C1_SELFTEST pass=6 fail=0
rc=0
```

`mut-dup` — **SURVIVED** (rc=0, `pass=6 fail=0`):

```
case good: ok=True want=True pass failed=[]
case missing: ok=False want=False pass failed=['missing:tools/absent.py']
case thin: ok=False want=False pass failed=['thin:tools/h.py:owner']
case noselftest: ok=False want=False pass failed=['noselftest:tools/i.py']
case superseded-ok: ok=True want=True pass failed=[]
case unres: ok=False want=False pass failed=['missing:tools/nothere.py']
C1_SELFTEST pass=6 fail=0
rc=0
```

Proof of survival, not merely equal-looking output:

```
$ diff <(cat …/.ufo/waves/round-61/evidence/selftest-c1.txt) \
       <(python3 mut/mut-dup-count-c1.py --selftest --scratch $TMPDIR; echo "rc=$?")
IDENTICAL -> mut-dup reproduces the committed receipt byte-for-byte
```

`mut-thin` — **KILLED** (rc=1):

```
case thin: ok=True want=False FAIL failed=[]
C1_SELFTEST pass=5 fail=1
rc=1
```

`mut-noselftest` — **KILLED** (rc=1):

```
case noselftest: ok=True want=False FAIL failed=[]
C1_SELFTEST pass=5 fail=1
rc=1
```

### W2 — committed witness: do-nothing control state (entering rev `325f7e63`)

All four (pristine + three mutants) print the identical committed control line
and exit 1:

```
C1=unmet gates=25 registered=0 missing=25 thin=0 dup=0 unres=0 noselftest=0 noowner=0
failed=missing:.ufo/waves/round-52/count-c1.py,… rc=1
```

(The full line is byte-identical to
`.ufo/waves/round-61/evidence/control-c1-do-nothing.txt`.) No mutant changes
the control outcome — expected, since at the entering revision the registry
tables end at r51 and every gate is `missing` before any of the three arms is
reached. **The control therefore cannot discriminate between pristine and any
of the three mutants**; it is a red-before witness only.

### W2b — committed state at freeze rev `7370a731`

Same as W2 for all four (all 25 gates still `missing` pre-data):
`C1=unmet gates=25 registered=0 missing=25 … rc=1`. Also non-discriminating.

### W3 — my own scratch hostile fixtures (not committed witnesses)

Fixture: throwaway repo at an explicit scratch path, one commit, `SKILL.md`
carrying the eight-cell gate-registry header plus the rows below, manifest with
one path `tools/g.py`, `tools/g.py` committed.

**dup-two-live-rows** (two live rows naming the same path, neither containing
"supersed"):

```
pristine      : C1=unmet gates=1 registered=0 missing=0 thin=0 dup=1 unres=0 noselftest=0 noowner=0 failed=dup:tools/g.py   rc=1
mut-dup       : C1=met   gates=1 registered=1 missing=0 thin=0 dup=0 unres=0 noselftest=0 noowner=0 failed=none                rc=0
mut-thin      : C1=unmet … dup=1 … failed=dup:tools/g.py   rc=1
mut-noselftest: C1=unmet … dup=1 … failed=dup:tools/g.py   rc=1
```

→ the dup arm is real and load-bearing; only `mut-dup` changes its verdict.

**thin-empty-owner** (owner cell empty):

```
pristine      : C1=unmet … thin=1 … failed=thin:tools/g.py:owner   rc=1
mut-thin      : C1=met   … failed=none                              rc=0
mut-dup / mut-noselftest: unchanged (thin:1)
```

**noselftest-cell** (self-test cell reads "runs by hand"):

```
pristine      : C1=unmet … noselftest=1 … failed=noselftest:tools/g.py   rc=1
mut-noselftest: C1=met   … failed=none                                   rc=0
mut-dup / mut-thin: unchanged (noselftest:1)
```

**good** and **sup-plus-live** (superseded row + live row): all four print
`C1=met … registered=1 … rc=0` — no mutant disturbs the positive path.

---

## 5. Supplementary probe: does C3 catch a committed dup-arm mutant?

`count-c3.py:41` pins `PIN_C1 = "a6684e697583746e8b6318d6984f3ada5e619c45a0a3449ecf46d79193433e00"`,
i.e. the sha256 of the frozen `count-c1.py`. Running the frozen C3 over a
fixture repo that carries `count-c1.py` = pristine vs. `count-c1.py` = `mut-dup`:

```
--- C3 over fixture with pristine-c1 :: rc=1
  C3=unmet r60hole=FAIL r61repair=ok blobrefusal=ok expectpin=ok livepins=ok  cases=5 failed=r60 bytes lost or hole absent (red-before unfaithful)
--- C3 over fixture with mut-dup-c1 :: rc=1
  C3=unmet r60hole=FAIL r61repair=ok blobrefusal=ok expectpin=ok livepins=FAIL cases=5 failed=r60 bytes lost or hole absent (red-before unfaithful);r61 counters absent or sha pin mismatch at rev
```

(`r60hole=FAIL` in both rows is an artifact of my fixture lacking the r60
blob at rev `ac496c7c`; it is identical in both arms and irrelevant to the
comparison. Pristine C3 `--selftest` over the real lane tree is green:
`C3_SELFTEST pass=8 fail=0`, rc=0.)

**Reading:** C3's `livepins` arm *does* fail when the counter's bytes change —
but it is a **sha pin, not a behavioural witness**. It cannot distinguish
"the dup arm was removed" from "an unrelated byte moved"; it also means the
arm cannot be fixed in place without updating C3's pin (which the freeze
bans). C3 therefore does **not** close the coverage gap for the dup arm; it
only pins bytes. The behavioural gap in the C1 battery stands on its own.

---

## 6. Secondary findings (coverage, not contract)

**F2 — the `unres` arm is unreachable from its own selftest case.** The
committed case `("unres", [GOOD], ["tools/nothere.py"], False)`
(`count-c1.py:157`) supplies table row `GOOD`, whose entry cell names
`tools/g.py`, while the manifest path is `tools/nothere.py`. `row_hits`
(`count-c1.py:62-70`) therefore finds no hit, `missing` fires at
`count-c1.py:92-95` and `continue`s **before** the `unres` arm at
`count-c1.py:113-116`. The frozen receipt proves it:
`case unres: ok=False want=False pass failed=['missing:tools/nothere.py']` —
the arm never ran. A counter with the `unres` arm deleted entirely would
still pass the committed battery unchanged. No witness in the committed
evidence set exercises `unres`.

**F3 — `noowner` is a dead counter.** `res["noowner"]` is initialised at
`count-c1.py:75` and `:214` and printed at `:127`, and there is **no
`res["noowner"] += 1` anywhere in the file** (grep: only those three
occurrences). The frozen met line `… noselftest=0 noowner=0 rev=<rev>`
(`contract.md:42`) therefore prints a constant `0` for a dimension the counter
does not measure. The owner-cell dimension is in fact covered by the `thin`
arm (an empty owner cell yields `thin:<path>:owner`), so the token is
redundant rather than wrong — but it is not a measured boolean, the same
shape of defect C3's `r60hole` arm audits in the r60 counter. (The empty-owner
path *is* killed by the committed `thin` case, so F3 is a reporting/calibration
finding, not an uncovered arm.)

**F4 — the "superseded" filter is a two-cell substring grep, and an
all-superseded path falls back to a superseded row.** `live`
(`count-c1.py:96-98`) filters on `"supersed" in name.lower()` **or**
`"supersed" in scope.lower()` only; `row = live[0] if live else hits[0]`
(`:103`). Probe: two rows for the same path, both with
`superseded: see next row` in the **scope** cell → `hits=2`, `live=0` →
the fallback picks `hits[0]` (a superseded row) and the counter reports
`registered=1 … ok=True`. Meanwhile the natural spelling of "superseded" in
this registry's own idiom (the **verdict** cell, per
`.ufo/waves/round-61/w1/Mo61RevC1.md:62-71`) is not recognised at all, so such
a row counts as *live* and a genuinely duplicated gate is reported as `dup`.
Not part of my assigned mutation set; recorded because it bears on how much
the `dup`/`superseded` arms can be trusted, and because Mo61RevC1 already
filed the same observation in the same round.

---

## 7. Draft block for the L1 (no amendment proposed — text only, for routing)

The freeze bars amendments to the contract and the counters; the following is
recorded as a routed finding for the lesson, not as a proposed change:

> **Round-61 routed defect (C1, dup arm unwitnessed).** The C1 counter's
> duplicate-row arm (`count-c1.py:99-102`) has no committed witness: deleting
> it (`if len(live) > 1:` → `if False:`) leaves the frozen `--selftest`
> battery byte-identical to `evidence/selftest-c1.txt` (`pass=6 fail=0`,
> rc=0), and leaves the committed do-nothing control and the freeze-revision
> run unchanged. The mutation is killed only by a hostile fixture
> (two live rows for one path) that the committed evidence set does not
> contain. The contract's kill rule names this exact condition ("two
> non-superseded rows", `contract.md:46-48`). Same-shape coverage gaps found
> in the same read: the `unres` arm is unreachable from its own selftest case
> (the case fails earlier at `missing`), and the `noowner` counter has no
> increment site, so `noowner=0` in the met line is a constant rather than a
> measurement. Next round's C1 counter should carry, at minimum, a
> two-live-rows fixture and a matching-row-with-unresolvable-entry fixture,
> and should either increment `noowner` or drop the token from the met line.

No counter, contract, registry, or production file was changed by this seat.

---

## 8. Reproduction (exact commands)

```bash
# scratch layout
S=/fast/scratch/hyaku/mori-r61/Mo61MutC1a
mkdir -p "$S"/{mut,scratch,out}
cp /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-61/count-c1.py "$S/pristine-count-c1.py"

# the three one-line mutations (applied to the SCRATCH copies only)
# mut/mut-dup-count-c1.py        :99   `if len(live) > 1:`            -> `if False:`
# mut/mut-thin-count-c1.py       :105  `if empty:`                    -> `if False:`
# mut/mut-noselftest-count-c1.py :109  `if "--selftest" not in …:`    -> `if False:`

export TMPDIR="$S/scratch"

# W1 committed witness
python3 "$S/mut/mut-dup-count-c1.py"       --selftest --scratch "$TMPDIR"; echo "rc=$?"
python3 "$S/mut/mut-thin-count-c1.py"      --selftest --scratch "$TMPDIR"; echo "rc=$?"
python3 "$S/mut/mut-noselftest-count-c1.py" --selftest --scratch "$TMPDIR"; echo "rc=$?"

# W2 committed control state (entering revision)
python3 "$S/mut/mut-dup-count-c1.py" 325f7e639916fcbc77fa2ec7475951a1b86bb1cb \
  --repo /home/vgpnk/Projects/shokunin/mori-shokunin \
  --manifest /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-61/gate-manifest.json \
  --scratch "$TMPDIR"; echo "rc=$?"

# W2b freeze revision
#   same command with 7370a731abcafc4c803111de7c22cd6264d63be1

# W3 hostile fixtures + C3 pin probe: harness2.py, probe_c3_pin.py
python3 "$S/harness2.py"; python3 "$S/probe_c3_pin.py"
```

Receipts (small, copied into this report above; raw copies kept in scratch
until cleanup): `out/harness2-run.txt`, `out/probe_c3_pin.txt`,
`out/final-receipt.txt`.

### Restoration / non-mutation evidence

```
$ sha256sum …/.ufo/waves/round-61/count-c1.py
a6684e697583746e8b6318d6984f3ada5e619c45a0a3449ecf46d79193433e00   (pre-run and post-run, identical)

$ git -C …/mori-shokunin status --porcelain -- .ufo/waves/round-61/count-c1.py
(empty — tracked file byte-identical to HEAD)

$ git -C …/mori-shokunin diff --stat HEAD -- .
(empty — no tracked file modified)

$ git -C …/mori-shokunin status --porcelain
?? .ufo/waves/round-61/build-w1-spec.py      (pre-existing, not mine)
?? .ufo/waves/round-61/w1-dispatch.json       (pre-existing, not mine)
?? .ufo/waves/round-61/w1-dispatch.stderr      (pre-existing, not mine)
?? .ufo/waves/round-61/w1-spec.json           (pre-existing, not mine)
?? .ufo/waves/round-61/w1.ready               (pre-existing, not mine)
?? .ufo/waves/round-61/w1.ready.dispatched    (pre-existing, not mine)
?? .ufo/waves/round-61/w1/                    (wave reports; this file is mine)
```

All mutants, fixtures and receipts live only under
`/fast/scratch/hyaku/mori-r61/Mo61MutC1a/` and were removed on cleanup.
Every fixture repo was created at an explicit scratch path with
`git -C "$D" init -q`; every later git call named `git -C "$D"`; the throwaway
identity `t <t@t>` was used only inside those scratch repos. No `task` call,
no `agent://all` broadcast, no writes to the fleet root or any sibling repo.

**Tools installed/updated:** none. No pacman, no `uv tool`, no binary
download. Python 3.14.8 and git 2.56.0 were already present and sufficient.

**Disk guard:** `scripts/hyaku/disk-guard.sh status` run before the work —
`/fast/scratch/hyaku` 54% used, 370.9G free (green); no ENOSPC encountered.

---

## 9. Kill table, condensed

| Mutant | W1 committed selftest | W2 committed control | W2b freeze rev | W3 own hostile fixture | Verdict |
|---|---|---|---|---|---|
| `mut-dup` | **survives** (rc=0, `pass=6 fail=0`, receipt byte-identical) | survives (identical) | survives (identical) | **killed** (`dup=1`→`C1=met`) | **ROUTED DEFECT — no committed witness** |
| `mut-thin` | **killed** (case `thin` FAIL, rc=1) | survives (identical) | survives (identical) | killed (`thin=1`→`C1=met`) | killed |
| `mut-noselftest` | **killed** (case `noselftest` FAIL, rc=1) | survives (identical) | survives (identical) | killed (`noselftest=1`→`C1=met`) | killed |

Baseline was green throughout (pristine: `pass=6 fail=0` rc=0; pristine
control: rc=1 with the committed unmet line), so no result above is
inconclusive.
