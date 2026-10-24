# RevC8Conjunct — C2 `selftest_conjunct` strip test + M19 selftest-gap receipt audit

Seat: `mori-r39.RevC8Conjunct` (leaf reviewer). Lane repo read-only; scratch under
`.ufo/waves/round-39/scratch/RevC8Conjunct/`. No installs, no tool upgrades.
Scored tip under test: `13bfba23b7ca063c76d3504a2ff6eb7b6a294932`.
Byte identity of the artifacts I ran (blob sha256 at the scored tip, git object read):

- `.ufo/waves/round-39/conform.py` → `fe0be179aba9df7150f0b6cdb50a5f9bbdb411efb1263b46ffa6b21d46ef7987`
  (= `evidence/freeze-r39.txt:3`; also identical at `f920eaf7`, the revision the c8
  receipts name).
- `.ufo/waves/round-39/count-c7.py` → `b92c65f224a6268a901aa6bc5ad66b499048eaca82b493356eb8e1f324ef0520`
  (= `evidence/freeze-r39.txt:2`).

## Verdict on the assignment

| Side | Result |
|---|---|
| Strip the first `proc.communicate(timeout=…)` in a scratch copy of `count-c7.py` | **Caught** — `CONFORM=unmet`, exit 1 |
| Which check catches it | `selftest_conjunct` FAIL — **not** `bounded_reads` (it prints PASS) |
| Honest counter passes | **Yes** — `CONFORM=met`, exit 0, all nine checks PASS |
| `evidence/m19-selftest-gap.txt` misquotes the r38 bytes | **No** — all 5 quoted fragments are byte-exact substrings of r38 `conform.py` at `13f3db7e`; central claim is true |

So neither acceptance FAIL trigger fires. Two concrete defects and one caption defect
remain, below.

## Findings

### F1 — MEDIUM: the contract's kill rule for `selftest_conjunct` is not implemented; the check passes on the exact M19-gapped bytes

`contract.md:116-117` states: *"a checker whose selftest never mutates the
communicate-timeout conjunct fails `selftest_conjunct`."* It does not.

`selftest_conjunct` (`conform.py:396-421`) reads only the **counter** source: it parses
`counters[0]`, asserts `comm_violations == []`, strips the first
`proc.communicate(timeout=…)` with a regex, and asserts the mutant produces a
`comm_violations` entry. It never inspects the checker's own mutation list
(`conform.py:427-455`), so "the shipped `--selftest` mutates the conjunct" is not what
the check measures — only "the static rule can flag a stripped copy".

Two executions prove the gap:

1. **The r38 counter bytes themselves** (the M19-gapped instrument,
   `13f3db7e:.ufo/waves/round-38/count-c1.py`, sha256
   `5aa51556946a3e5293ba069a12b9e816694ea406bd11f5cb22da5e5ba7c22ea3`, copied to
   scratch) evaluated by r39 `conform.py`:

   ```
   $ python3 .ufo/waves/round-39/conform.py 13bfba23 --counter \
       .ufo/waves/round-39/scratch/RevC8Conjunct/count-c1-r38.py
   check selftest_conjunct  PASS (honest_comm=[] mutant_comm=['communicate without timeout at line 116'])
   CONFORM=unmet      # (only predicate/timeout_state/scratch fail — r38 contract/scratch roots)
   ```

   The check that is supposed to close M19 passes on the bytes whose selftest never
   mutated the conjunct.

2. **A checker copy with the mutation gutted.** Removed the four-line
   `("selftest_conjunct", …)` entry (`conform.py:451-454`) from a scratch copy
   (`scratch/RevC8Conjunct/conform-no-strip-mut.py`; `grep -c 'communicate timeout
   keyword stripped'` = 0):

   ```
   $ python3 scratch/RevC8Conjunct/conform-no-strip-mut.py 13bfba23 --selftest
   … PASS scratch … 
   CONFORM_SELFTEST pass=8 fail=0      # exit 0
   $ python3 scratch/RevC8Conjunct/conform-no-strip-mut.py 13bfba23
   check selftest_conjunct  PASS (honest_comm=[] mutant_comm=['communicate without timeout at line 114'])
   CONFORM=met                          # exit 0
   ```

   Nothing asserts that the nine mutation names are present (`conform.py:495-513`
   counts whatever ran); a checker that silently drops the conjunct mutation is
   indistinguishable from the shipped one. The M19 regression is therefore prevented
   today only by the mutation entry existing in the committed bytes, not by any check.

The shipped r39 selftest *does* contain the mutation and does flip its own check
(`--selftest` run below), so the C2 factual claim (`pass=9 fail=0`) holds; the kill
rule and the check's discriminating power do not.

### F2 — LOW (latent bypass): `bounded_reads` does not audit `communicate` on any counter, and never on a non-first `--counter`; the documented rule is broader than the code

`conform.py:17-19` documents `bounded_reads` as "every `subprocess.run(` **and every
`communicate(`** in every counter carries a `timeout=` keyword". The code contradicts
this: `bounded_violations` is filled only for `run/check_output/check_call`
(`conform.py:211-214`); `communicate` presence violations go to `comm_violations`
(`conform.py:268-278`), which is consumed only by `selftest_conjunct`, and only for
`counters[0]` (`conform.py:407`). Evidence:

- Stripped single counter: `bounded_reads PASS (count-c7-stripped-regex.py: bounded=[] value=[])`,
  while the same stripped counter fails only `selftest_conjunct`.
- Two-counter invocation, honest first + stripped second:

  ```
  $ python3 .ufo/waves/round-39/conform.py 13bfba23 \
      --counter …/count-c7.py --counter …/count-c7-stripped-regex.py
  check bounded_reads      PASS (count-c7.py: bounded=[] value=[]; count-c7-stripped-regex.py: bounded=[] value=[])
  check selftest_conjunct  PASS (honest_comm=[] mutant_comm=['communicate without timeout at line 114'])
  CONFORM=met              # exit 0
  ```

  A counter with a stripped communicate timeout supplied as a later `--counter` is
  accepted. The docstring advertises "every `--counter` is audited statically"
  (`conform.py:9-10`). No declared receipt or contract claim uses more than one
  `--counter` (`c8-after*.txt` each carry one), so this is latent, not exercised.

### F3 — LOW (caption, not misquote): `m19-selftest-gap.txt` quotes exact bytes but mislabels a docstring line as a call site

Byte check against `13f3db7e:.ufo/waves/round-38/conform.py` (scripted substring test):
all five quoted lines are **EXACT**:

```
CHECK_NAMES = ("predicate", "head_pin", "tool_resolve", "bounded_reads",     # r38:44
results["bounded_reads"] = (source_ok, "; ".join(detail))                     # r38:189
("bounded_reads", "proc = run([\"git\", \"-C\", repo] + list(args), timeout=timeout, env=clean_env())",   # r38:229
"git helper run timeout removed"),                                            # r38:231
`Popen(` is followed by `communicate(timeout=`, and the first counter         # r38:16 (docstring)
```

The central claims are **true**: the r38 mutation list is exactly
`predicate, head_pin, tool_resolve, bounded_reads, timeout_state, scratch` (AST/regex
over `r38-conform.py:220-236`) — none touches `communicate`; and r38's static rule did
enforce it (`r38-conform.py:114-124`: every `communicate` call must have `timeout` in
its keywords and `saw_communicate` must be set). Independent proof that the rule
existed while the selftest never mutated it — r38 `conform.py` on a stripped r38
counter:

```
$ python3 scratch/RevC8Conjunct/conform-r38.py 13f3db7e --counter …/count-c1-r38-stripped.py
check bounded_reads    FAIL (count-c1-r38-stripped.py: run=True popen=False cap=True mkdtemp=True scratch=True)
check timeout_state    FAIL (exit=None timeout_reason=False pass=False)
CONFORM=unmet
```

The caption defect: *"first communicate(timeout=…) call sites in the r38 checker
body (for contrast)"* is false — an AST walk of r38 `conform.py` finds **zero**
`communicate(` and **zero** `Popen(` call sites; the quoted text is the module
docstring (r38:16), truncated mid-sentence ("and the first counter"). The receipt also
quotes the mutation tuple selectively (old string at :229 and the `why` string at
:231, omitting the replacement at :230) without claiming adjacency. Byte quotes are
verbatim; only the framing is wrong.

## Evidence: commands and observed outputs

Honest counter (scratch copy, sha256 `b92c65f2…`, byte-identical to the scored tip):

```
$ python3 .ufo/waves/round-39/conform.py 13bfba23 --counter \
    .ufo/waves/round-39/scratch/RevC8Conjunct/count-c7.py
check predicate          PASS (exit=0 equal=True)
check head_pin           PASS (pin=20260b0c… tip=20260b0c…)
check tool_resolve       PASS (exit=0 resolved=…/witness-summary-only-live.txt)
check bounded_reads      PASS (count-c7.py: bounded=[] value=[])
check timeout_value      PASS (count-c7.py: bounded=[] value=[])
check drain_shape        PASS (violations=[])
check timeout_state      PASS (exit=1 timeout_reason=True pass=False)
check scratch            PASS (count-c7.py: mkdtemp_dir=True root=True)
check selftest_conjunct  PASS (honest_comm=[] mutant_comm=['communicate without timeout at line 114'])
CONFORM=met              # exit 0
```

Strip construction (mirrors the checker's own mutation, `conform.py:411-412`):
first match of `proc\.communicate\(timeout=[^)]+\)` is at `count-c7.py:114`
(`out, err = proc.communicate(timeout=timeout)` inside `run()`, 6 occurrences total);
`re.subn(..., count=1)` → `n_sub=1`; the regex mutant and the literal anchor used by
the shipped `--selftest` (`conform.py:452-453`) produce **identical bytes**.

Stripped counter:

```
$ python3 .ufo/waves/round-39/conform.py 13bfba23 --counter \
    .ufo/waves/round-39/scratch/RevC8Conjunct/count-c7-stripped-regex.py
check bounded_reads      PASS (count-c7-stripped-regex.py: bounded=[] value=[])
check timeout_value      PASS (count-c7-stripped-regex.py: bounded=[] value=[])
check drain_shape        PASS (violations=[])
check timeout_state      PASS (exit=1 timeout_reason=True pass=False)
check scratch            PASS (count-c7-stripped-regex.py: mkdtemp_dir=True root=True)
check selftest_conjunct  FAIL (honest_comm=['communicate without timeout at line 114'] mutant_comm=['communicate without timeout at line 114', 'communicate without timeout at line 121'])
CONFORM=unmet            # exit 1
```

Shipped selftest and shipped default run (independent re-run at the scored tip;
`scratch/RevC8Conjunct/selftest-run.txt`):

```
$ python3 .ufo/waves/round-39/conform.py 13bfba23 --selftest
PASS bounded_reads      git helper run timeout removed -> only bounded_reads failed
PASS selftest_conjunct  communicate timeout keyword stripped -> only selftest_conjunct failed
CONFORM_SELFTEST pass=9 fail=0     # exit 0 (~51s)
$ python3 .ufo/waves/round-39/conform.py 13bfba23
CONFORM=met                        # exit 0, all nine PASS
```

This output is itself the direct contradiction of `conform.py:34-37` (phrase at :36), which says the
strip "flips exactly `bounded_reads`"; it flips `selftest_conjunct` and `bounded_reads`
stays PASS. (The parenthetical in P-C8, `contract.md:95`, calls it "the shipped
`--selftest`'s bounded_reads mutation" — the mutation is named `selftest_conjunct`,
`conform.py:451`.)

## Residual risk and verification gaps

- Lane HEAD advanced during this review (`20260b0c…` at first run → `ebc61f47…` on a
  later run), so `head_pin` receipts are only valid against the tip each run measured.
  I pinned every byte-level claim by blob sha256, not by HEAD.
- I did not execute r38's `conform.py --selftest` end-to-end at `13f3db7e` (no receipt
  exists in `round-39/evidence/`); the "no communicate mutation" claim is established
  from the committed mutation list plus the stripped-counter experiment above.
- F1's gutted-checker probe mutates a scratch copy, not the lane bytes; it measures
  check semantics, not the shipped artifact.
- F2's two-counter bypass is demonstrated on a synthetic stripped counter; no declared
  receipt invokes `conform.py` with more than one `--counter`.
- The `selftest_conjunct` regex is receiver-name-bound (`proc\.communicate`); a counter
  using another receiver would fail the check for the wrong reason (brittleness, not
  exploitable in the shipped counter — all six communicate calls use `proc`).
