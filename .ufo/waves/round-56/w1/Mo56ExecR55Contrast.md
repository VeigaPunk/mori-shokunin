# Mo56ExecR55Contrast — round-56 C2 contrast arm: the frozen round-55 C1 counter at the freeze tip

Seat assignment (exec lane, wave w1): re-run the **frozen round-55**
`.ufo/waves/round-55/count-c1.py` at the round-56 freeze tip
`8be2717b0809281d07dffe83dad424a4859e0747` and confirm it still prints
`voted=0 ... failed=votes` with rc 1 (the C2 contrast arm); re-run the same
counter at the entering tip `5b295eeebd87ebd610d8d39bfe2035742f740cfa` and
diff the two outputs — only the `rev=` field may differ; paste both last
lines.

Tooling: no install, upgrade, or network fetch was needed. Everything ran on
the preinstalled `python3` (3.13, stdlib only) and `git` (read-only: `show`,
`rev-parse`, `ls-tree`, `cat-file`). No `pacman` was run (host-wide pacman
transactions are paused). Nothing was written to `~/.local/bin` or any PATH
directory. No lane file was mutated: the only file this seat wrote is this
report; all scratch lives under
`/fast/scratch/hyaku/mori-r56/Mo56ExecR55Contrast/` and was removed at the
end.

Wave carries NO vote items; nothing below is a vote line, and no line in this
report starts with a vote verb.

---

## 1. Command and outputs

The counter was invoked exactly as the assignment specifies, from a scratch
cwd with `TMPDIR` pointed at the seat scratch (the counter writes nothing, but
the cwd discipline is kept):

```
$ export TMPDIR=/fast/scratch/hyaku/mori-r56/Mo56ExecR55Contrast/tmp
$ python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-55/count-c1.py \
      8be2717b0809281d07dffe83dad424a4859e0747
```

**Last line at the freeze tip** (`8be2717b0809281d07dffe83dad424a4859e0747`),
exit code **1**:

```
C1=unmet scope=78 rows=78 matched=78 status_ok=78 line_ok=78 source_rows=ok pins=ok provenance=ok same=69 moved=7 changed=2 broken=0 holds=78 stale=0 voted=0 dissent=0 rev=8be2717b0809281d07dffe83dad424a4859e0747 failed=votes
```

**Last line at the entering tip** (`5b295eeebd87ebd610d8d39bfe2035742f740cfa`),
exit code **1**:

```
C1=unmet scope=78 rows=78 matched=78 status_ok=78 line_ok=78 source_rows=ok pins=ok provenance=ok same=69 moved=7 changed=2 broken=0 holds=78 stale=0 voted=0 dissent=0 rev=5b295eeebd87ebd610d8d39bfe2035742f740cfa failed=votes
```

stderr was empty for both runs.

**Confirmation of the C2 contrast arm: PASS.** `voted=0` and `failed=votes`
are present at the freeze tip, exit code 1, exactly as
`.ufo/waves/round-56/evidence/c2-old-counter-voted0.txt` records for the
entering tip. The frozen contrast receipt is reproduced byte-for-byte by my
entering-tip run:

```
$ diff <(sed '1d' .../evidence/c2-old-counter-voted0.txt) <(sed '1d' out-enter.txt)
# only the receipt's own trailing "exit=1" line differs (sed '1d' removed the
# payload line, so the receipt's "exit=1" remains) -> the payload line is
# byte-identical.
```

## 2. The diff: only the `rev=` field differs

```
$ diff out-freeze.txt out-enter.txt
1c1
< C1=unmet scope=78 ... voted=0 dissent=0 rev=8be2717b0809281d07dffe83dad424a4859e0747 failed=votes
---
> C1=unmet scope=78 ... voted=0 dissent=0 rev=5b295eeebd87ebd610d8d39bfe2035742f740cfa failed=votes
$ diff <(sed 's/rev=[0-9a-f]*/rev=REV/' out-freeze.txt) \
       <(sed 's/rev=[0-9a-f]*/rev=REV/' out-enter.txt) && echo IDENTICAL
IDENTICAL
```

**Confirmed: only the `rev=` field differs.** After normalising the `rev=`
token the two outputs are byte-identical, and the single-line diff touches
nothing but `rev=`.

### Why the difference is structural, not coincidental

The round-56 wave changed exactly two of the counter's inputs between the
entering tip and the freeze tip. Everything else the counter reads is the
same blob at both revs:

| Input the r55 C1 counter reads | entering tip `5b295eee` | freeze tip `8be2717b` | same? |
|---|---|---|---|
| `.ufo/waves/round-55/count-c1.py` (the counter itself) | `256aaab4f017…` | `256aaab4f017…` | yes (identical blob) |
| `.ufo/waves/round-55/w1/` (vote dir tree) | `24b5256df470…` | `24b5256df470…` | yes |
| `.ufo/waves/round-55/w1-results.json` (captured outputs) | `39562ece6706…` | `39562ece6706…` | yes |
| `corpus/knowledge/kernel-v7.3-recheck-r55.md` (ledger) | `06a458dadf7f…` | `06a458dadf7f…` | yes |
| `corpus/SOURCES.md` (registry) | `28d8b98d9c52…` | `50aab042f5d1…` | **no** — S544 + S545 rows appended |
| `ENTER` scope tip `ca52426e…` | (constant inside the counter) | (same) | yes |

The `corpus/SOURCES.md` drift is the only input change, and it does not reach
the vote arm: the counter's `registry()` lookup for the round-55 S-rows is
unaffected by the two appended rows, which is visible in the output itself
(`source_rows=ok provenance=ok` at both revs). The vote bytes that produce
`voted=0` are literally the same bytes at both revs.

Independent corroboration: the frozen blob of the counter at the freeze tip
and at the entering tip is byte-identical to the working-tree copy
(`sha256 e30658be34bfbf866860b20c9bde4117d467e351bb79e523131424cd5061e20b` for
all three), and the counter run from a materialised copy of that blob with
`--repo` reproduces the same lines and rc 1 at both revs. The working-tree
counter is therefore not a drifted artifact; the freeze-tip behavior is the
frozen behavior.

### Determinism

Each command was run twice at both revs; the outputs are byte-identical
run-to-run (`DETERMINISTIC`, `ENTER_DETERMINISTIC`), so the `voted=0` reading
is stable, not a transient.

## 3. Root cause isolated: the shape, not the data

The `failed=votes` cause is the counter's own binding predicate in
`.ufo/waves/round-55/count-c1.py` (`votes()` / `final_votes()`): a vote binds
only when the voter's **captured output** carries a line whose *stripped*
content is exactly `RECHECK <hash12> <word>` (or that prefix followed by a
space), and the counter binds votes read out of the seat's **report file**.

The committed round-55 captured outputs are JSON documents. In the raw bytes
the vote lines appear quoted and comma-suffixed, e.g. a line whose stripped
content is `"RECHECK 7b2d297eec60 holds",` — the leading quote makes it fail
the exact-line test. Measured over the 16-voter roster:

```
TOTAL raw lines containing RECHECK across roster: 151
TOTAL raw lines exactly matching the r55 predicate shape: 0
```

i.e. every one of the 151 vote mentions is present in the captured bytes and
**none** is in the shape the frozen counter recognises, so
`agree = [w for w, bound in v.values() if w == disp and bound]` is empty for
all 78 ledger rows and `voted` stays 0.

Two counterfactual arms run through the counter's **own** `evaluate()` (imported
from the frozen blob, no source edit), holding the votes constant and varying
only the *shape* of the captured outputs:

| arm | captured output shape | votes present | r55 counter reads |
|---|---|---|---|
| A | as committed (JSON) | 146 | `voted=0 dissent=0 … failed=votes` |
| B | same votes flattened to plain text lines | 146 | `voted=68 dissent=0 … failed=votes` |

So the shape accounts for the entire `0 → 68` movement: the votes were always
in the bytes. (The residual `68 → 78` gap is the 10 rows that only one voter
covered — the dispatch-coverage validator item the contract already carries as
planned — so the residual is a *coverage* limit, not a binding limit. This is
consistent with the frozen C2 docstring's parenthetical and with the
contract's routed-item note; it is not evidence against C2.)

## 4. The new binder reproduces the frozen tally receipt

For completeness I re-derived the other side of the contrast with the frozen
binder at the freeze tip (`tools/mori-vote-bind.py`, blob sha256
`8be1acdbb36cd68deba005e21a4a8679534ab5a5099a787aa9335d288dfa6bca`, equal to
the PIN in `.ufo/waves/round-56/evidence/freeze-sha256.txt`):

```
$ python3 vb.py tally --ledger ledger.md --results r55-results.json --verb RECHECK \
      --voter Mo55Rc01 … --voter Mo55Rc16
TALLY rows=78 agree=78 double=68 single=10 zero=0 dissent=0 voters=16 bound_voters=15
```

byte-identical to the frozen receipt `.ufo/waves/round-56/evidence/tally-r55.txt`
(the receipt carries one extra `exit=0` line of its own). The binder sees
**78/78 rows agreeing, 68 double-voted, 10 single-voted, 0 zero, 0 dissent**
over exactly the same committed bytes on which the frozen counter reads
`voted=0`. The two readings are the contrast the C2 claim rests on, and both
are reproducible.

Also confirmed the same contrast arm end-to-end through the frozen round-56
C2 counter at the freeze tip:

```
$ python3 .ufo/waves/round-56/count-c2.py 8be2717b0809281d07dffe83dad424a4859e0747
C2=met selftest=ok tally=ok control=ok contrast=voted0 entry=ok row=ok rev=8be2717b0809281d07dffe83dad424a4859e0747
rc=0
```

and the round-56 C1 counter at the same rev (context, not my claim):
`C1=met selftest=ok fixtures=ok entry=ok row=ok norem=ok rev=8be2717b…`, rc 0.

## 5. Limits of this verification (named, not fixed)

- The r55 counter's `git_reader` resolves `ENTER` (`ca52426e…`) from the
  repo; both revs can read it, verified via `git cat-file -e`.
- The `contrast` arm inside the frozen `count-c2.py` accepts the substring
  `voted=0` in stdout with rc 0 or 1. I confirmed this is **shape-insensitive
  in the empty-vote-dir direction**: forcing `ls()` to return an empty vote
  directory still yields the same `voted=0 … failed=votes` line and rc 1. The
  arm therefore discriminates exactly what it is meant to discriminate — "the
  frozen counter does not bind these votes" — but it does not by itself prove
  *why*; the why is established in §3 above by the A/B counterfactual. The
  counter is frozen, so this is a limit of the arm's specificity, not a
  defect I may repair.
- `count-c2.py`'s `--min` equivalent (`min_votes` in
  `tools/mori-vote-bind.py`) is accepted but **does not affect the tally
  classification**: `tally()` derives `double`/`single`/`zero` from the vote
  count per row and never compares against `min_votes`; the value is only
  echoed into the returned dict's `"min"` key, which the `TALLY` line does not
  print. Measured: `--min 1` and `--min 99` both print the identical
  `TALLY rows=78 agree=78 double=68 single=10 zero=0 dissent=0 voters=16
  bound_voters=15`. The frozen expected line is therefore reproduced, but the
  flag is inert. LOW severity; routed to round 57, not fixed here (the tool is
  frozen).

## Findings

- **HIGH — none.** The C2 contrast arm is confirmed at the freeze tip:
  `voted=0 … failed=votes`, rc 1, at
  `.ufo/waves/round-55/count-c1.py` (run against
  `8be2717b0809281d07dffe83dad424a4859e0747`). The entering-tip run differs
  **only** in the `rev=` field (diff normalised to `rev=REV` is byte-identical).
  Both last lines are pasted verbatim in §1.
- **MED (limit, not a defect to fix here) — `tools/mori-vote-bind.py`
  `tally(..., min_votes=…)` / CLI `--min` is inert.** The threshold never
  enters the `agree`/`double`/`single`/`zero`/`dissent` classification
  (`tools/mori-vote-bind.py:161,202`; `--min 1` and `--min 99` print the same
  `TALLY` line). The frozen expected value is still reproduced exactly, so the
  C2 predicate is unaffected. Routed to round 57.
- **MED (limit of the frozen contrast arm's specificity) —
  `.ufo/waves/round-56/count-c2.py:110-120`** accepts the substring `voted=0`
  at rc 0/1, and an empty vote directory yields the same line; the arm
  demonstrates *that* the frozen counter does not bind, not *why*. The *why* is
  supplied by the A/B shape counterfactual in §3 of this report. Counter is
  frozen — routed to round 57 if the L1 wants a sharper arm.
- **LOW (no-change confirmation) — the round-56 wave did not perturb the
  contrast inputs.** The vote-dir tree (`24b5256d…`), the captured outputs
  (`39562ece…`), the ledger (`06a458da…`) and the counter itself
  (`256aaab4…`) are identical blobs at both revs; only `corpus/SOURCES.md`
  drifted (S544/S545 appended), and that drift does not reach the vote arm
  (`source_rows=ok provenance=ok` at both revs). No re-pin consequence arises
  from this seat's checks.
- **LOW (residual, already routed) — 10 of 78 rows are single-voted**
  (covered by `Mo55Rc13` only); `Mo55Rc14` has no report file and no bound
  vote, so `bound_voters=15` of `voters=16`. The contract already carries the
  dispatch-coverage validator (≥2 voters per scoped row) as a planned item and
  the binder surfaces these rows honestly as `single=10`. No action here.
