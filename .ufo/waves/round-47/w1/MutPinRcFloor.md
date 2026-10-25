# MutPinRcFloor — mutation probe of `tools/mori-pin-check.py` (round 47, wave w1)

Seat: MutPinRcFloor (leaf, no subagents). Scratch: `.scratch/r47-MutPinRcFloor/`.
Detector: the tool's own `--selftest` (22 cases), run under `TMPDIR=<scratch>`.
Production file never written by this seat; all mutants were scratch copies.

## 0. Instrument identity

Contract freeze `63eecf2738db96f46b0bd02b1b2dfd66787493d0` pins
`tools/mori-pin-check.py` = `e3ef425abde30974faf53a894f96650af11570d2125a5bf621395f6ab0d903e1`.
`git show 63eecf27:tools/mori-pin-check.py | sha256sum` → `e3ef425a…` ✓.
Mutants were cut from the freeze blob (`frozen.py` in scratch), per the contract's
"claim is measured with `git show <freeze>:<path>`" rule.

Working-tree observation (not my edit; see §4): at seat start the working tree hashed
`104cf3dd8174933799de97ec0b11e6cdb1923bb2bda1130f0bb3afeff1e4f56d` (1-line deletion,
uncommitted `M`); by 16:46 it was back at `e3ef425a…` and `git status --porcelain
tools/mori-pin-check.py` is empty.

## 1. Baseline (pristine frozen bytes) — must pass or all verdicts inconclusive

```
$ TMPDIR=$S python3 $S/frozen.py --selftest      # $S = .scratch/r47-MutPinRcFloor
… all 22 case lines PASS …
PIN_CHECK_SELFTEST pass=22 fail=0
rc=0
```

## 2. Mutants and verdicts

Base for all: `check()` / `pin_commands()` in the freeze blob. Full per-case outputs
had every line PASS except the one(s) quoted.

### (a) delete the rc≠0-with-fail=0 check — KILLED

Removed from the tally arm:

```python
            if ok and re.search(r"\bfail=0\b", want) and rc != 0:
                ok = False
```

Expected detector arm: selftest case `nonzero_rc_with_fail0` (writes `foo.py.rc`=1 so the
tool prints the pinned tally but exits 1).

```
FAIL nonzero_rc_with_fail0  PIN_CHECK=met tally_pins=1 digest_pins=0 mismatches=0 unparsed=0 no_command=0 dropped=0 min_tally_pins=1 rev=deadbeef baseline=no
PIN_CHECK_SELFTEST pass=21 fail=1
rc=1
```

Verdict: **killed** (mutant flips the case to `met`).

### (b) drop `counts['dropped'] == 0` from met — KILLED

```python
    met = (counts["mismatches"] == 0 and counts["unparsed"] == 0
           and counts["no_command"] == 0
           and counts["tally_pins"] >= min_tally)
```

Expected detector arm: `baseline_row_deleted` (baseline has row `bar`, text does not;
`dropped=1` is the only unmet cause).

```
FAIL baseline_row_deleted  PIN_CHECK=met tally_pins=1 digest_pins=0 mismatches=0 unparsed=0 no_command=0 dropped=1 min_tally_pins=1 rev=deadbeef baseline=yes
PIN_CHECK_SELFTEST pass=21 fail=1
rc=1
```

Verdict: **killed**. Note the `dropped=1` line still prints — the mutant survives the
*reporting* but not the *predicate*; the selftest asserts met/unmet, not the line alone.

### (c) drop the unparsed condition — KILLED (both readings tested)

Tasking wording is ambiguous between the met-conjunct and the digitless-pin arm, so both
were probed.

(c-i) met-conjunct dropped:

```python
    met = (counts["mismatches"] == 0
           and counts["no_command"] == 0 and counts["dropped"] == 0
           and counts["tally_pins"] >= min_tally)
```

```
FAIL malformed_row  PIN_CHECK=met tally_pins=0 digest_pins=0 mismatches=0 unparsed=1 no_command=0 dropped=0 min_tally_pins=0 rev=deadbeef baseline=no
FAIL digitless_pin  PIN_CHECK=met tally_pins=1 digest_pins=0 mismatches=0 unparsed=1 no_command=0 dropped=0 min_tally_pins=1 rev=deadbeef baseline=no
PIN_CHECK_SELFTEST pass=20 fail=2
rc=1
```

Killed twice over (`malformed_row` is kept unmet *only* by the unparsed conjunct at
floor 0; `digitless_pin` likewise at floor 1).

(c-ii) digitless-pin arm deleted (`if not re.search(r"\d", pinned): … continue`):

```
FAIL digitless_pin  PIN_CHECK=unmet tally_pins=1 digest_pins=0 mismatches=1 unparsed=0 no_command=0 dropped=0 min_tally_pins=1 rev=deadbeef baseline=no
PIN_CHECK_SELFTEST pass=21 fail=1
rc=1
```

Killed, but note *how*: the case still ends `PIN_CHECK=unmet` (the pinned `: PASS` no
longer matches the observed `pass=3 fail=0`, so `mismatches=1`) — the assertion fails only
because the case also demands a `state=unparsed` line, which the mutant no longer emits.
A future case that pinned the observed mismatch text instead of the digitless shape would
let this mutant survive silently. No action taken; recorded as detector nuance.

### (d) make the digest check always hit — KILLED

Replaced the compare loop:

```python
            hit = paths[0] if paths else None
```

Expected detector arm: `digest_stale` (row pins `0`×64 as digest of `tools/foo.py`).

```
FAIL digest_stale  PIN_CHECK=met tally_pins=1 digest_pins=1 mismatches=0 unparsed=0 no_command=0 dropped=0 min_tally_pins=1 rev=deadbeef baseline=no
PIN_CHECK_SELFTEST pass=21 fail=1
rc=1
```

Verdict: **killed** (mutant reports the stale digest as a `match` → met).

## 3. Survivor analysis

No survivor among (a), (b), (c-i), (c-ii), (d): every mutant dropped the selftest to
`fail≥1` and exit 1. **No selftest gap to name.** Weakest detection observed is (c-ii),
killed on a state assertion rather than the met predicate (see §2c).

## 4. Out-of-scope observation (detection only, not mutated by this seat)

At seat start `tools/mori-pin-check.py` in the working tree hashed
`104cf3dd…` vs freeze `e3ef425a…`; `git diff 63eecf27 -- tools/mori-pin-check.py`
showed exactly one deleted line, `bound = []` in `pin_commands()`. A copy of those bytes
(`pristine.py`) run under the same detector:

```
NameError: name 'bound' is not defined. Did you mean: 'round'?
  (selftest → check → pin_commands, line 132)
rc=1
```

By the end of the seat the working tree was back at `e3ef425a…` and
`git status --porcelain tools/mori-pin-check.py` prints nothing (clean). This seat made
no write to any production path; whoever made/repaired the transient edit, it was outside
this scratch. C1 measurements taken meanwhile from working-tree bytes would have crashed;
freeze-blob measurements are unaffected.

## 5. Restoration evidence

- Production `tools/mori-pin-check.py`: never written by this seat (reads and `cp` out
  only); hash `e3ef425abde30974faf53a894f96650af11570d2125a5bf621395f6ab0d903e1` after all
  runs; `git status --porcelain` clean at 2026-10-25T16:46:56-03:00.
- Scratch mutants restored to frozen bytes after probing; final scratch state:

```
e3ef425abde30974faf53a894f96650af11570d2125a5bf621395f6ab0d903e1  frozen.py
e3ef425abde30974faf53a894f96650af11570d2125a5bf621395f6ab0d903e1  mut-a.py
e3ef425abde30974faf53a894f96650af11570d2125a5bf621395f6ab0d903e1  mut-b.py
e3ef425abde30974faf53a894f96650af11570d2125a5bf621395f6ab0d903e1  mut-c.py
e3ef425abde30974faf53a894f96650af11570d2125a5bf621395f6ab0d903e1  mut-c2.py
e3ef425abde30974faf53a894f96650af11570d2125a5bf621395f6ab0d903e1  mut-d.py
e3ef425abde30974faf53a894f96650af11570d2125a5bf621395f6ab0d903e1  pristine.py
```

## 6. Tooling

No tools installed or upgraded (none needed; `python3` and `git` preexisting). No pacman
use. All runs had `TMPDIR=/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r47-MutPinRcFloor`.
