# RevC9Ancestry — independent merge-base re-derivation of the C9 DAG fixtures (A, C; D as cross-check)

**Verdict on the assigned axis: PASS — no contradiction.** For both assigned fixtures the v2 gate's printed
`supersede_timing` line matches an independently derived `git merge-base --is-ancestor` verdict, and both
receipts reproduce byte-identically. Three findings (one MEDIUM: frozen contract text misstates the r38 fixture-A
output; two LOW: a header-docstring contradiction and an unwitnessed `--full-history` clause); none changes any
gate verdict.

Scope: read-only on the lane. Everything below ran against gate bytes identical to the scored tip
(`git diff --stat 13bfba2..HEAD -- tools/mori-sources-appendonly.py .ufo/waves/round-39/fixtures/` is empty;
HEAD is 20260b0). Scratch: `.ufo/waves/round-39/scratch/RevC9Ancestry/` (`rederive.py`, `rederive.json`,
`crosscheck.py`, `repro-after.txt`, `repro-red.txt`, mutant copies). No lane file was edited.

## Method

1. Imported the gate module's own machinery (`_selftest_dag_cases`, `_make_dag_repo`, `_selftest_env`) in
   `scratch/RevC9Ancestry/rederive.py` and built dag-a / dag-c / dag-d under scratch.
2. Derived edit commits **independently**: own markdown-table parser (immutable columns = all but
   `status`/`recheck`/`used-by`), compared against the commit's **true first parent**; cross-checked with plain
   `git diff <parent> <commit> -- corpus/SOURCES.md` for the `| S001 |` lines.
3. Derived the superseding row's landing commit independently: commits where a row whose `teaches` opens
   `supersedes S001` is newly present against **every** parent, filtered to non-descendants (minimal landings).
4. Ran `git merge-base --is-ancestor` directly for each derived edit/landing pair, in both directions.
5. Ran the gate on a fresh build of each fixture (`HEAD --repo <fixture> --round-base <base>`) and compared its
   `supersede_timing` line with step 4.
6. Re-ran the committed harness `.ufo/waves/round-39/fixtures/run-c9-dags.py` with (a) the v2 gate bytes and
   (b) the r38 bytes from `git show 13f3db7e:tools/mori-sources-appendonly.py`, then diffed the blocks against
   `evidence/c9-after-fixture-{a,c,d}.txt` and `evidence/c9-red-a.txt`.

Fixture SHAs are deterministic across builds (pinned dates): dag-a `b0=07be6c7f1765 e1=35fe5b450b0a
s1=e52b091f9e82 m=141a9c5a820e`; dag-c `b0=07be6c7f1765 c1=2053fccc3728 c2=d52c462a594a m=62130ad3fff2
t=971694077948`; dag-d `s1=2373145a52fe`.

## dag-a — "side-branch superseder is stale" (`--round-base b0`)

Raw diffs (`git diff`, S001 line): `b0→e1` changes `anchor a` → `anchor a v2`; `b0→s1` **no** S001 change;
`e1→m` **no** S001 change. So S001's only immutable-cell edit is `e1`; the merge does not fabricate one.
The `S002` row (`teaches` = `supersedes S001 — replacement`) is newly present at `s1` (also present at `m`,
but `m` descends from `s1`, so the landing is `s1`).

```
git -C dag-a merge-base --is-ancestor 35fe5b4(e1) e52b091(s1)  -> exit 1
git -C dag-a merge-base --is-ancestor e52b091(s1) 35fe5b4(e1)  -> exit 1   (incomparable)
```

P-C9 requires: as-of only if the landing descends from the last edit → **stale**.
Gate printed: `superseded_as_of=[] stale_supersede=[S001]`, summary `round_changed=[S001]`, `EXIT=1`
(byte-identical to `evidence/c9-after-fixture-a.txt`). **Match.**

## dag-c — "merge does not fabricate an edit" (`--round-base c1`)

Raw diffs: `b0→c1` changes `anchor a` → `anchor a v2`; `b0→c2`, `c1→m`, `m→t` show **no** S001 line change.
So the only edit is `c1`, and the merge `m` changes nothing against its first parent `c1` (the "no fabricated
edit" claim holds at the level of the registry rows). `S003` (`supersedes S001`) is introduced only at `t`.

```
git -C dag-c merge-base --is-ancestor 2053fcc(c1) 9716940(t)  -> exit 0   (t descends from c1)
```

P-C9 requires as-of → gate printed `superseded_as_of=[S001] stale_supersede=[]`, `round_changed=[]` (round
base `c1`), `EXIT=0` (byte-identical to `evidence/c9-after-fixture-c.txt`). **Match.**

## dag-d — cross-check ("landing is the last edit commit")

Both `e1` and `s1` change S001 against their own first parent `b0` (verified by raw diff); landing `S002` is
`s1`; `git merge-base --is-ancestor s1 s1` exits 0 (a commit is its own ancestor). Gate printed
`superseded_as_of=[S001] stale_supersede=[]` — consistent with the equality reading (see Finding 2).

## Receipt reproduction

- v2 harness run: blocks for A, C, D are **byte-identical** to `evidence/c9-after-fixture-{a,c,d}.txt`.
- r38 bytes (`13f3db7e`) harness run: all three blocks are **byte-identical** to `evidence/c9-red-a.txt`:
  A `as-of=[] stale=[S001] EXIT=1`; C `as-of=[S001] stale=[] round_changed=[S001] EXIT=1`;
  D `as-of=[] stale=[S001] EXIT=1`.
- Instrumented r38 run (scratch copy): dag-a walk `b0,e1,s1,m` with `changed_at={1,2,3}`, `last_edit=3 (m)`,
  `landing=2 (s1)` → stale *via fabricated walk-record edits*; dag-d walk is simplified to `b0,s1`,
  `last_edit=landing=1` → stale via the strict `>` comparison.

## Findings

### F1 — MEDIUM: the frozen contract's r38-on-fixture-A claim is false (C3 Before and P-C9 parenthetical)

`contract.md:140-142` (C3 Before) asserts that "the round-38 gate bytes … print `superseded_as_of=[S001]` for a
superseder that never descends from the edit (fixture A)". Measured: r38 on fixture A prints
`superseded_as_of=[] stale_supersede=[S001]` — **identical to v2**. The same misstatement appears in the frozen
predicate: `contract.md:131` and the gate's `PREDICATE` (`tools/mori-sources-appendonly.py:84-87`) are verbatim
identical (832 bytes, compared programmatically). The parenthetical reads:

> "…committed fixtures for a side-branch superseder (stale, not as-of) and a merge that must not fabricate an
> edit (round-38 gate bytes print as-of and a fabricated edit there; the round-39 gate prints stale and no
> edit)."

On the merge fixture C both instruments print `superseded_as_of=[S001]`; only `round_changed` differs
(r38 `[S001]`/EXIT=1 vs v2 `[]`/EXIT=0). All r38 outputs below come from my byte-identical reproduction of the
`13f3db7e` bytes, which matches `evidence/c9-red-a.txt` block-for-block.

- Parallel reading ("r38 as-of [on A], v2 stale [on A]"): false — r38 is stale on A.
- Merge-fixture-only reading ("v2 prints stale [on C]"): false — v2 prints as-of on C
  (`evidence/c9-after-fixture-c.txt`).
- The only stale/as-of divergence in the fixture set is **dag-d**, and it runs r38=stale → v2=as-of, i.e. the
  opposite direction of the parenthetical; the lesson already records this
  (`corpus/lessons/round-39.md:20`, M21: "the r38 gate printed `stale=[S001]` on it") and so does
  `corpus/knowledge/gate-ancestry-r39.md` ("Fixture A … round-38 bytes print `stale=[S001]`"; "Fixture D …
  the round-38 bytes print stale").

Nuance — fixture A still earns its place: the C3 kill rule (`contract.md:151-152`: "a gate that keeps
index-order timing lists S001 as-of on fixture A") holds for an isolated timing regression. A mutant that keeps
v2's first-parent edits and `--full-history` but swaps the ancestry call for
`by_hash[edit_commit] < landing_index` prints `superseded_as_of=[S001]` on fixture A (scratch
`gate-mut-index.py`). What fails is the claim about the *r38 bytes as a whole*: their adjacent-record edit
detection makes `last_edit = m` (instrumented: `changed_at={1,2,3}`, `last_edit=3`, `landing=2`), so their own
index comparison lands on stale for A.

Impact: no gate verdict, selftest expectation, or receipt is wrong; a validator checking the frozen literals
against their own cited receipts hits a false clause. Corroborated independently by w1/RevScorecard F5 (same
fixture-A conclusion) and w1/RevFreeze F3 (the C3 Before cites `fixtures/make-ancestry-dags.py`, absent from
every commit; the committed harness is `fixtures/run-c9-dags.py`). The C3 After literal `pass=11` is likewise
stale — my `--selftest` run prints `pass=12 fail=0`. Wording fixes need no code change; I made no edits.

### F2 — LOW: the gate's header docstring contradicts its implemented/tested equality semantics

`tools/mori-sources-appendonly.py:28-33` says as-of requires a landing "descendant of (**strictly later
than**)" the last edit, and that stale covers a superseder that "landed **at or before** the edit". The code
(`:350-357`) uses `is_ancestor(edit_commit, commits[landing_index])`, and `git merge-base --is-ancestor s1 s1`
exits 0, so dag-d (landing == last edit) is printed as-of — which is exactly what the selftest expects
(`:558-561`, `superseded_as_of: ["S001"], stale_supersede: []`) and what P-C9's own words allow ("descendant,
by `git merge-base --is-ancestor`"). So the header's user-facing spec disagrees with the tool on the equality
case; a reader trusting the header would expect dag-d's S001 in `stale_supersede`.

### F3 — LOW (verification gap): the `--full-history` clause is not witnessed by any committed fixture

Removing `--full-history` from the v2 walk (scratch mutant `gate-mut-nofull.py`) yields byte-identical verdict
lines and exit codes on all three fixtures (A 1, C 0, D 1). The flag demonstrably matters on the lane history
(`corpus/knowledge/gate-ancestry-r39.md`: `6531ac60` appears only under `--full-history`), but the selftest
would not catch a regression that drops it. P-C9 names the flag; the fixture set does not discriminate it.

## Residual risk

- "The id's last immutable-cell edit" and "latest superseding row" are resolved by full-history **walk order**
  (commit-date order), not by ancestry (`:344-347`). dag-d is as-of only because `s1` sorts after `e1`; a DAG
  whose child/parent committer dates are non-monotone could change the selected "last edit" while the ancestry
  relation is unchanged. The knowledge file's Limits section discloses this; no fixture exercises it.
- Receipt shape: the harness header pins only the round-base SHA (`b0=07be6c7f1765` / `c1=2053fccc3728`); the
  edit/landing/merge SHAs are not recorded, so a receipt alone cannot prove which fixture bodies/dates produced
  it. My deterministic rebuild reproduced both receipts byte-for-byte, so current risk is low.
- Callers: no code parses `supersede_timing` outside the gate's own selftest regex (`:74`); grep over the lane
  (`*.py|*.md|*.sh`) finds the gate, the fixtures harness, documentation (QUALITY 104/909, README 606), and the
  round-38 wave-spec generators (`.ufo/waves/round-38/gen-wave{,-2}-spec.py`), which only emit the phrase in
  generated prompt text.
  `lsp` is unavailable in this runtime (`read xd://lsp` → "No such tool: xd://lsp"; mounted devices:
  ast_edit, debug), so caller/diagnostic checks used literal grep and direct execution — recorded as such, not
  as semantic proof.

## Checks actually run

- `python3 scratch/RevC9Ancestry/rederive.py` — builds + independent derivation + merge-base table (`rederive.json`).
- `git merge-base --is-ancestor` invocations quoted above (exit codes captured directly).
- `python3 .ufo/waves/round-39/fixtures/run-c9-dags.py {v2,r38} <lane> <scratch>/repro-{after,red}.txt` + block diff
  vs evidence: v2 IDENTICAL (A,C,D); r38 IDENTICAL (A,C,D).
- `python3 tools/mori-sources-appendonly.py --selftest` → `pass=12 fail=0` (exit 0).
- Mutants (scratch copies only): ancestry call → const-False flips C to stale; → const-True flips A to as-of;
  → walk-index (r38's comparison over v2 edits) yields as-of on A and C — the kill-rule mutant of F1;
  `--full-history` removal → no observable change (F3).
- Contract-vs-gate predicate equality check: verbatim, 832 bytes.

Tools installed: none.
