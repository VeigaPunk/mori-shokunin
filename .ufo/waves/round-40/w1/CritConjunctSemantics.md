# CritConjunctSemantics — attack on `selftest_conjunct` / `entry_live` (C1, P-C10)

**Review recommendation: FAIL (weaker-proxy finding).** P-C10's words claim "the
checker's own textual-mutation table carries a **live** `selftest_conjunct` entry";
the code's `entry_live` conjunct tests **textual presence and reference, never
application**. A checker whose table still carries the entry but whose `selftest`
never applies that arm is *not* caught by v3; a checker whose wiring is faithful but
spelled `str(source)` *is* rejected. This is an advisory falsification report, not a
canonical runtime judgment. No admission, integration, remediation, or alternate
runtime was performed.

**Axes:** calibration (does the code enforce the predicate's words), depth
(does `selftest_conjunct` measure what P-C10 says), operability (receipt
correspondence). The findings below concern the `entry_live` sub-clause of C1's
third made-sound check only; they do not falsify the counter-side conjuncts
(`comm_violations`, per-one-at-a-time strip detection, anchor presence — all
behavioral and verified green) or any C2 claim.

## Evidence identity

All relative paths are under `/home/vgpnk/Projects/shokunin/mori-shokunin`.

- **V** = `.ufo/waves/round-40/conform.py`, sha256
  `5025b9664632d01063c11b4f5dadd4f9a063db66d73315d7ed25db8d90b83aaf` — matches
  `evidence/freeze-r40.txt:9`.
- **C8** = `.ufo/waves/round-40/count-c8.py`, sha256
  `4e4d50eb1e96d947f0e9d2ab25a13b2b8c33963f216f3be43060a3348702f6da` — matches
  `evidence/freeze-r40.txt:8`.
- **S** = `.scratch/CritConjunctSemantics/` (this seat's only write area besides
  this report).

## Mechanism — what `entry_live` actually tests

`evaluate()` at **V:617–620**:

```python
entry_live = ("selftest_conjunct" in SELFTEST_MUTATION_NAMES
              and "CONJUNCT_MUTATION" in mutations_src
              and "selftest_mutations(source)" in selftest_src
              and CONJUNCT_MUTATION in selftest_mutations(src))
```

Four sub-clauses, three lexical (name in a module tuple; a substring of
`inspect.getsource(selftest_mutations)`; a substring of
`inspect.getsource(selftest)`), and one behavioral: conjunct 4 *calls*
`selftest_mutations(src)` on the audited counter's source and checks the returned
list still contains `CONJUNCT_MUTATION`. Conjunct 4 is real — it catches the r39
table-gutting (`evidence/c10-after-conjunct.txt` shows it flips every arm to
`failing=[…,'selftest_conjunct']`). **But all four conjuncts test the table and
its textual references; none tests that `selftest`'s loop applies the arm.** The
`"selftest_mutations(source)"` substring is a syntactic literal — the exact call
spelling — so the proxy is simultaneously too weak (application unverified) and too
strong (call-spelling overconstrained).

## Counterexample 1 — the assigned construction: entry live, arm unwired, v3 does not catch it

**Mutant** `S/conform-v3-unwired.py` (sha256
`e8dd33548d051c93044915ec82283e82536e12b675682b8ee03b58006b832e72`): identical to V
except (a) `SCRATCH_ROOT` repointed to `S/scratch` (seat write bounds; the checker
path is never itself audited) and (b) an 8-line early-`continue` inside the
`selftest` loop that, for `name == "selftest_conjunct"`, prints the same
`PASS %-18s %s -> only %s failed` line and increments `passed` **without writing or
evaluating any mutant counter**. The table keeps `CONJUNCT_MUTATION`; the real call
`mutations = selftest_mutations(source)` is kept verbatim. A diagnostic
`print("ARM_EVALUATED %s", file=sys.stderr)` precedes each real `evaluate()`.

**Commands and outputs:**

```
$ python3 S/conform-v3-unwired.py 265a955cc67be4eae97d2dc5a9338a25f31eb29b
check selftest_conjunct  PASS (count-c8.py: honest_comm=[] strips=6 detected=6 anchor=True entry_live=True)
CONFORM=met
EXIT=0
```

```
$ python3 S/conform-v3-unwired.py 265a955cc67be4eae97d2dc5a9338a25f31eb29b --selftest
PASS predicate          predicate token changed -> only predicate failed
PASS head_pin           pin label renamed -> only head_pin failed
PASS tool_resolve       relative resolution removed -> only tool_resolve failed
PASS bounded_reads      git helper run timeout removed -> only bounded_reads failed
PASS timeout_scope      timeout value replaced with None -> only timeout_scope failed
PASS timeout_scope_shadow function-local None shadow inserted -> only timeout_scope failed
PASS drain_bind         communicate drains replaced by wait+read -> only drain_bind failed
PASS drain_bind_decoy   decoy used communicate beside a wait+read drain -> only drain_bind failed
PASS timeout_state      budget flag ignored -> only timeout_state failed
PASS scratch            scratch parent moved off-lane -> only scratch failed
PASS selftest_conjunct  communicate timeout keyword stripped -> only selftest_conjunct failed
CONFORM_SELFTEST pass=11 fail=0
EXIT=0
```

`diff` of that stdout against `evidence/c10-after-selftest.txt:3–14` (the frozen
receipt): **byte-identical** — "IDENTICAL: unwired selftest stdout == frozen
receipt lines 3-14". Yet stderr (`S/unwired-selftest.err`) shows exactly ten
`ARM_EVALUATED` lines; **`ARM_EVALUATED selftest_conjunct` never appears**. The
eleventh PASS is fabricated; the conjunct arm was never exercised.

**Caught?** No. Normal audit: `entry_live=True`, `CONFORM=met` exit 0. Selftest:
`pass=11 fail=0` exit 0, receipt-identical. The kill rule's two prongs bracket and
miss this mutant: the table is *not* gutted (c10-after-conjunct's trigger) and the
`pass=` count is still eleven (the count guard). Between them sits "present,
referenced, counted — never applied".

## Counterexample 2 — spelling, not wiring: faithful wiring rejected (false negative)

**Mutant** `S/conform-v3-renamed.py` (sha256
`2e0eb9cd0bb03228e850c3fbc6435d1bdd0c4da83eb274616d5c5e4cad8350ee`): one-line
delta, `mutations = selftest_mutations(source)` → `selftest_mutations(str(source))`
(`str` on `str` is identity — behavior byte-identical).

```
$ python3 S/conform-v3-renamed.py 265a955cc67be4eae97d2dc5a9338a25f31eb29b
check selftest_conjunct  FAIL (count-c8.py: honest_comm=[] strips=6 detected=6 anchor=True entry_live=False)
CONFORM=unmet
EXIT=1
```

Its own `--selftest` (same command with `--selftest`, exit 1):
`PASS selftest_conjunct … only selftest_conjunct failed` — the conjunct arm
**works and detects the stripped counter** — while every other arm reports
`failing=[…,'selftest_conjunct']`, i.e. mutant B's self-audit convicts itself of
unliveness for a call spelling (`CONFORM_SELFTEST pass=1 fail=10`). A checker whose
conjunct is genuinely exercised prints `CONFORM=unmet`.

## Counterexample 3 — dead text counts as "live"

**Mutant** `S/conform-v3-commentonly.py` (sha256
`3e09d929114b72599a18c7b0ce19cabd0c6ebaebed360435e89a00b01a1c48dd`): the literal
string `selftest_mutations(source)` moved into a **comment**; the real call spelled
`list(selftest_mutations(str(source)))` (still genuinely applied).

```
$ python3 S/conform-v3-commentonly.py 265a955cc67be4eae97d2dc5a9338a25f31eb29b
check selftest_conjunct  PASS (count-c8.py: honest_comm=[] strips=6 detected=6 anchor=True entry_live=True)
CONFORM=met
EXIT=0
```

`entry_live=True` while the wiring the clause claims to verify exists only in a
comment. Conversely the live call is spelled `str(source)` — the same spelling
mutant B was convicted for. The two mutants swap true wiring and true text and the
verdicts follow the *text*, not the wiring.

## Assessment

- **Is "live entry" the claimed property?** Partially. The fix for r39 finding 12
  genuinely catches a *gutted* table (all three lexical clauses plus conjunct 4's
  real evaluation — `c10-after-conjunct.txt`). But "live" in P-C10's sense requires
  the arm to be *applied* by `selftest`; the code proves only *referenced*. Mutant A
  demonstrates the residual: present + referenced + counted + never applied →
  `entry_live=True`, `pass=11`, receipt-identical.
- **Weakest form:** the weakest verifier satisfying all four conjuncts is dead text
  (mutant C). The strongest counterexample available is mutant A: it preserves every
  observable contract line (`CONFORM=met`, `pass=11 fail=0`, eleven PASS rows) while
  the conjunct is unwired.
- **Structural root:** `--selftest` evidence is self-reported by the file under
  test; `entry_live` is the only audit-time attempt to pin that report, and it pins
  syntax, not execution. The `pass=11` count guard is a *receipt-shape* control —
  fabricable in the same edit that unwires the arm.
- **Fixable defect vs tradeoff:** fixable. No stronger machine check is required to
  restore honesty — bound the words, or make application verifiable (below).
  Treating counterexample 1 as canonical-judge-rejectable would require reading
  "live" as "present in the table and textually referenced", which is precisely the
  weaker-proxy reading this report falsifies.
- **Residual noting (outside probe scope):** `head_pin` compares the counter's
  `--pin-only` output to `git rev-parse HEAD` (live tip), not to the audited `rev`;
  at run time lane `HEAD` was `ede486b7…`, ahead of scored tip `265a955cc…`, so the
  passing run certified the *current* tip. Harmless here; worth one sentence if the
  check is ever rerun on stale checkouts.

## Smallest safe correction

Ordered by size:

1. **Wording bound (minimal, honest):** amend the clause to what the code enforces —
   "the checker's table *contains* a `selftest_conjunct` entry whose anchor occurs in
   the counter, referenced from `selftest` by exact spelling; arm application is
   self-reported". Predicate change → new counter version per the freeze rule
   (contract.md:9–10), not an in-place edit.
2. **Verifiable application (v4 candidate):** have `--selftest` emit, per arm, the
   sha256 of the mutant counter bytes it wrote (e.g. `arm=<name> mutant_sha=<h>`);
   then `pass=11` plus digests makes a never-applied arm visible in the receipt
   itself. Fabricating a digest is possible only by also lying about a checkable
   artifact — one order harder than fabricating a PASS line.
3. **Drop the literal-spelling clause:** replace `"selftest_mutations(source)" in
   selftest_src` with an AST check for any call to `selftest_mutations` in
   `selftest`'s body — kills counterexamples 2/3's asymmetry without pretending to
   verify application.

(1) is the smallest safe correction; (2)+(3) together close both directions if a v4
is cut anyway.

## Exercised checks and boundaries

- Ran: the three mutant audits and two mutant selftests above (system `python3`
  only; receipts in `S/*.out`, `S/*.err`); `diff` mutant-vs-V and
  mutant-selftest-vs-frozen-receipt; `sha256sum` identity checks; read V, C8, the
  contract, and the c10 evidence receipts listed.
- No tools installed or upgraded (system python3 sufficed).
- No tracked lane files, fleet state, sibling lanes, lane jj state, or the lane Git
  index touched. Writes: this report plus `S/` scratch; mutant selftests wrote only
  under `S/scratch` (cleaned by the instrument itself). `git` used read-only
  (`rev-parse`).

**Bottom line:** `selftest_conjunct`'s `entry_live` is a reference checker, not a
liveness checker. The r39 finding-12 defect (gutted table selftests green) is really
fixed; the neighboring defect class — entry present, arm unapplied — passes the
same green. Fixable by wording bound or verifiable per-arm evidence; not a reason
to restore v2.
