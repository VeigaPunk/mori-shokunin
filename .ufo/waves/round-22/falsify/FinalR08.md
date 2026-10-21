# FinalR08 — falsification of R08 ("altered line returns 1")

Seat `MoriR22.FinalR08`, critic, static only. Nothing executed (no SUT, oracle, selftest, refinements, measurement driver), nothing installed, no production edits, no delegation. Read in full: `denominator-correction.md` (first), `contract.md`, `frozen/requirements-v2.json`, `frozen/fixture-builder-v2.py`, `oracle-reconcile-v2.py`, `tools/mori-retention-reconcile.py`, `refinement-reconcile.py`, `measure-round22.py`, `build/AttackR08.md`; `tools/mori-retention-gate.py:84-113,180-204` for line semantics. Read-only plumbing: `sha256sum` of the pinned files, `git log`/`git show`/`git status`/`git diff` on the lane.

## Bindings observed

- Lane HEAD `5888b565…`; tool last changed in `3985b3d` (selftest gained the `wrong.json` MISMATCH arm); `git status` clean for tool, frozen/ and oracle. Tool sha256 `d6870fb6…0ce7`.
- Fixture builder `1b3e16f7…15d1`, oracle `dcd1c7c6…8adb`, contract `1658c390…21a1`, correction `968945b2…24f9`. All four equal the pins in `requirements-v2.json`, so the v2 artifacts are frozen. Any correction has to be a new versioned artifact, not an edit.
- The gate's and the tool's line semantics are identical: NUL blobs are skipped, decoding uses `utf-8 errors=replace`, lines come from `split('\n')` and are numbered from 1 (gate `:90-101`, tool `:145-148`).

## Verdict

**At exit-code level, R08 holds on the shipping tool. At branch level, the requirement fails as a verified property.** The tool does reach MISMATCH because of the line change. But no committed artifact (frozen oracle, refinements, selftest or measurement mutants) can tell the line comparison on the raw `hits` field apart from one on `allowlisted_hits`. One mutant tool that compares `hits` without `line` passes every frozen requirement and every refinement case [INFERENCE, static trace; not executed].

## Static trace of the frozen arm on the shipping tool

1. Fixture `line` variant (`fixture-builder-v2.py:82`): `result['hits'][0]['line'] += 1`. `hits[0]` is the single `policy.json` hit. It sits at line 13 of the sorted, indented policy JSON, on the `synthetic` key. The `regex` value line does not self-match, because its text has `]` between `R` and `22`. The mutation sets line 14, which is `}`: a valid int ≥ 1 that collides with no other hit.
2. **Aliasing (new finding).** `fixture-builder-v2.py:55` builds `allowed=[h for h in hits if …]` from the same dict objects. `:68` and `:72-75` then set `allowlisted_hits = allowed_effective = allowed` (same objects again), and `unallowlisted_hits` is built the same way. Because the edit at `:82` happens in place and `:93` re-serializes afterwards, the stdout receipt carries line 14 in both `hits` and `allowlisted_hits`. R07 (`digest`) and R09 (`class`) mutate `hits[0]` the same way, so they are aliased too.
3. Tool `check()` with that receipt:
   - Every validation passes. Path binding holds because the argv paths are absolute under `str(root)`. The revision binds, the policy digest matches, the counters are ints, and `normalize_hits` accepts line 14 without a duplicate.
   - `tool:212-213` gives `differences = ['hits', 'allowlisted_hits']`.
   - `metric`, `routed`, `non_author`, `finding_id`, `forbidden_allowlist`, `warnings` and `exit_code` all equal the recomputation (1, 0, 1, `RETENTION_FINDINGS`, empty, empty, 1). The allowlist has two rows (the `allowed.txt` duplicate row is removed at `:60`) and neither is stale.
   - Result: exit 1, MISMATCH, `receipt_match` false, `privacy_clearance` false, stderr empty.
   - The oracle (`oracle-reconcile-v2.py:51`) records R08 with **no predicate**, so only exit, finding and empty stderr are checked.

## Counterexample (smallest)

**Mutant tool M-hits-line-blind** is a one-line change at `tool:213` that drops `line` from the `hits` key only:

```python
        if (Counter(k[:1]+k[2:] for k in claimed[field].elements())!=Counter(hit_key(h)[:1]+hit_key(h)[2:] for h in actual)) if field=='hits' else claimed[field]!=Counter(hit_key(h) for h in actual): differences.append(field)
```

How M survives each layer:

- **Frozen R08:** `allowlisted_hits` still differs through the alias, so M gives exit 1 and MISMATCH. The arm stays green.
- **Rest of the frozen 24:**
  - R05 (drop): the count changes, so it is killed by count.
  - R06 (inject): a new path appears.
  - R07 and R09: aliased into `allowlisted_hits`.
  - R18 (bool line) and R19 (duplicate): `normalize_hits` still validates the full 4-tuple.
  - Result: all 24 green.
- **Refinements:**
  - `path-only` changes the path, which is still part of the key.
  - `allowed-list-only` and `unallowed-list-only` reparse stdout (no aliasing) and mutate only the partition lists, which M still compares in full.
  - `forged-clean` changes the count.
  - Result: all cases green.
- **Selftest:** `wrong.json` sets `hits: []`, a count change, so green.
- **Real reconciliation:** unchanged.
- **Measurement driver:** its mutant list is `count-only`, `false-clearance`, `wrong-population` and `setup-leak` (`measure-round22.py:77-82`). None of them is line-identity-specific.

**Distinguishing receipt (smallest).** Take the valid synthetic receipt and change the `non-author.txt` hit in `hits` from line 1 to line 2. Line 2 is the empty trailing line. Leave everything else unchanged.

- A non-author hit appears in no partition list, so `hits` is its only carrier, and the receipt stays internally consistent.
- Shipping tool: `differences == ['hits']`, exit 1, MISMATCH. The requirement holds here.
- M: no differences, exit 0, RECONCILED. This is a false pass.
- This is the raw-population line identity that C1 claims to reconcile. No current artifact exercises it.

## Missing same-command red control

1. **No red run of R08 against a tool that ignores line, using the same oracle command.**
   - `measure-round22.py:91` runs the identical `oracle-reconcile-v2.py --tool <mutant>` command, but its kill criterion (`:93`) is the aggregate `unmet>0`. It never requires R08 itself to go red.
   - No mutant there targets line identity. Under `count-only`, R08 would go red [INFERENCE], but R07 and R09 would too, so that kill does not show R08 is fail-capable.
   - Under M, R08 stays green.
2. **No paired valid/mutated receipt inside the same repo and revision.**
   - R08's green baseline is R01, which runs in a separate `valid` fixture repo with a different `--repo`, `--rev` and receipt bytes (the receipt argv embeds `str(root)`).
   - The measured commit is plausibly identical across variants, because commit dates are fixed and the tree bytes are identical [INFERENCE], but the command is not.
   - The selftest's same-command pattern (`base` versus `bad` with only `--receipt` swapped, `tool:253-256`) exists only for the drop-all-hits arm. It has no line arm and asserts no `differences`.

## Prior build-wave note checked against current source (`build/AttackR08.md`)

- It says the "mutation lands in `hits` only" and `differences == ['hits']`. **False:** aliasing makes it `['hits','allowlisted_hits']`.
- It says the frozen R05–R10 mutations are all internally inconsistent, so a checker that never recomputes would pass them. **False for R07/R08/R09:** their aliased mutations are internally consistent, because the allowlist join ignores `line`. Under consistency-only checking, R08 actually kills such a checker.
- It says the selftest has 3 arms and no MISMATCH arm. **Stale:** `3985b3d` made it 4 arms, including the `wrong.json` MISMATCH arm.
- Its remaining ambiguities (precedence of duplicate rejection, multiset versus order) are consistent with the shipping tool. The fixture's choice of `hits[0]` avoids the duplicate trap: with `allowed.txt` line 1 → 2, the arm would become an R19 duplicate with exit 2. The frozen arm holds only because of the dict insertion order in `files`.

## Impacted axes

- **Calibration (primary):** the R08 pass is cited as proof that line participates in raw identity, but the frozen arm proves that only for `allowlisted_hits`.
- **Depth:** the mutant coverage is missing a line-identity mutant.
- **No regression in the shipping tool's behavior.**

## Smallest safe correction (for L1; v2 stays frozen, the new artifacts are versioned)

1. **Fixture v3.** Add a `line-raw` variant that edits a copy, not the shared dict, of the `non-author.txt` hit in `hits` only:
   ```python
   result['hits'][-1]=dict(result['hits'][-1],line=result['hits'][-1]['line']+1)
   ```
   Keep the current aliased `line` arm as the consistent-partition case.
2. **Oracle v3.** Give R08 the predicate `v['differences']==['hits'] and v['receipt_match'] is False and v['privacy_clearance'] is False and (v['raw_total'],v['policy_excluded'],v['scanner_total'])==(5,1,4)` on `line-raw`. Pin `['hits','allowlisted_hits']` on the aliased arm.
3. **Same-command pair.** Commit the valid receipt and the `line-raw` receipt in one revision. Run the identical argv with only `--receipt` swapped, and require exit 0/RECONCILED and exit 1/MISMATCH respectively. Mirror this in the selftest with `inner|{'hits':[h|{'line':2}]}`, asserting exit 1 and `'hits'` in `differences`.
4. **Mutant control.** Add M (the text replacement above, which is constructible against `tool:213`) to `measure-round22.py`, with a kill basis that requires R08 itself to be unmet, not just aggregate `unmet>0`.

Checks for L1 after integration: the oracle-v3 finite run, refinements, `--selftest`, and the M mutant run through the same oracle command, plus a restored control.

No production, policy, allowlist, evidence or history bytes changed. No installs. No matched text emitted.
