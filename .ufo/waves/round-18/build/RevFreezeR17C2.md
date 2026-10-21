# RevFreezeR17C2 — falsify frozen register row r17-C2

Seat: MoriR18Recovery.RevFreezeR17C2 (leaf, read-only derivation; no VCS mutation, no
installs — git was sufficient, so nothing was installed or upgraded per the 2026-10-19
tooling directive). Target: `.ufo/waves/round-18/frozen/c2-register.json` claim
`r17-C2` (frozen `tools/mori-round17-jj-regressions.py`, impl `tools/mori-census.sh`,
base `24526ea9617cd020fee16c28fe4d4a2789dc28cb`, tip `dcb2eea26d8dff0485b1cd0a9402fa63af82cb99`).

## Method

Independent re-derivation with the two read-only commands the frozen `verdict_rule.R/I/L`
names, run against the lane repo only:

```sh
git -C /home/vgpnk/Projects/shokunin/mori-shokunin rev-list --reverse --topo-order 24526ea..dcb2eea
git -C /home/vgpnk/Projects/shokunin/mori-shokunin diff-tree --no-commit-id --name-only -r <c>
```

Supporting read-only checks: `ls-tree` at base/tip, `show <rev>:<path> | sha256sum`,
`rev-list --parents` (merge check), pathspec-limited `diff-tree`/`log` for alternate
frozen-set candidates.

## Derived facts (all exit 0)

R (reverse topo, 6 commits, linear — no merges, so first-parent diffs are unambiguous):

```
273aa74ab73701f41fea38ec7bd1c47b4b2bfbc7   (parent = base 24526ea)
5c1dfb8d0530c74eb0e1630c2b522b735b486274
2be82940828424ef4a2d623173d7e603b8a18f93
fe9fa9083db998ead1554459d656568c4173f288
91940fa339e38006f8db5bd7d78bb6f037f4d016
dcb2eea26d8dff0485b1cd0a9402fa63af82cb99   (tip)
```

Touches of the register's two paths per commit (pathspec-limited `diff-tree`):

| commit | impl `tools/mori-census.sh` | frozen `tools/mori-round17-jj-regressions.py` | both |
|---|---|---|---|
| 273aa74 | yes | yes | co-commit |
| 5c1dfb8 | no | no | — |
| 2be8294 | yes | yes | co-commit |
| fe9fa90 | yes | no | — |
| 91940fa | no | no | — |
| dcb2eea | no | no | — |

- **I = 273aa74** — first commit of R touching the impl path (it is R's first commit;
  its parent is the base, so no earlier in-range impl touch can exist).
- **L = 2be8294** — last commit touching the frozen path; no harness touch in
  fe9fa90/91940fa/dcb2eea.
- **co_committed = true** — 273aa74 and 2be8294 each touch a frozen and an impl path.
- Existence: frozen harness **absent at base** (`ls-tree 24526ea` lists only the census,
  blob b280bd3), present at tip; census present at base and tip. Rule's `absent` branch
  (frozen missing at tip) does not fire.
- Byte identity: `show dcb2eea:tools/mori-round17-jj-regressions.py | sha256sum` =
  `da3e080a…fbcb89f0` = FINAL-PINNED_INPUTS.json's harness pin; census at tip =
  `87b8d680…b977ab28` = FINAL-PINNED pin; census at base = `f1f8d1b6…233c5501ff7` =
  byte-identical to `.ufo/waves/round-17/frozen/mori-census.sh` (the pinned entering
  baseline). The row describes real, pinned artifacts.

### Verdict per frozen `verdict_rule`

L = 2be8294 is not none, and L does **not** precede I (R positions: I=1, L=3; L after I)
→ **verdict = co-evolved**. Not pre-build, not absent, not no-implementation.
co_committed reported separately: true.

## Falsification attempts (none overturn the row)

1. **Alternate frozen sets.** Every defensible additional requirement input for r17-C2 was
   created in-range: `.ufo/waves/round-17/` is entirely absent at base (`ls-tree 24526ea --
   .ufo/waves/round-17` empty). Contract text (`.ufo/waves/round-17/contract.md` §"C2 census
   contract"), `wave1-context.txt`, `wave2-spec.json`, the C1-style expectation table
   (`fixtures/seat/expected.json` is C1's), and the pinned baseline copy
   (`frozen/mori-census.sh`) are all first touched in **273aa74** — the same commit as I —
   and contract.md/expected.json are touched again in 2be8294. So for any frozen set drawn
   from these, L ≥ 273aa74 = I → co-evolved (L == I is explicitly co-evolved under the rule).
   The routed jj-audit evidence lives in the fleet repo, not the lane, so it can never be a
   lane frozen path. LOG.md/SCORECARD.md exist at base but are ledgers, not C2 requirement
   inputs, and LOG.md is itself touched in 273aa74 → co-evolved again. **No defensible
   path-set choice yields pre-build**; only a pre-base freeze could, and none exists.
2. **Hidden earlier impl touch / ordering tricks.** 273aa74 is R's first commit with
   parent = base; `rev-list --parents` shows a strictly linear chain; no merge ambiguity.
3. **Byte-level decoys.** Tip bytes match the FINAL-PINNED hashes; the frozen baseline copy
   matches base census bytes exactly, so "frozen vs impl" is not confounded by the baseline
   snapshot drifting.
4. **Declared-label undercount (would the row hide an overclaim?).** The row declares
   `unlabeled` citing LOG.md:1197. Verified by reading LOG.md:1184-1213: line 1197 reads
   "constant C2 assertion universe; precommitted C3 witness/control/recipe pins." — a
   before/after measurement-constancy statement from the A2 correction list, not a freeze-
   order claim. The non-author spot-check (round-17-verifier-spotcheck.md:169-172) reads it
   the same way ("the 204-assertion universe was not proven frozen before initial
   implementation") and repair item 2 names C3 as the only round-17 item labelled pre-build.
   If one insisted LOG.md:1197 were an implicit pre-build declaration, an overclaim would
   appear (verdict co-evolved ≠ pre-build) — but that reading is contradicted by both the
   line's own text and the outside ruling; `unlabeled` is correct. Since effective label is
   unlabeled, overclaim = false regardless of verdict.

## Is the register's path-set choice right?

Yes, and it is the strongest defensible choice, not merely an adequate one:

- r17-C2's claim is census jj-colocation behavior (round-17 contract §"C2 census contract");
  impl = `tools/mori-census.sh` is the actual deliverable (changed 273aa74, 2be8294, fe9fa90).
  Swapping the sets (harness as impl) would reframe the claim away from what round-17
  declared — not defensible.
- The C2 scenario/assertion universe (17 scenarios, 204 assertions) lives inside the harness
  file itself (the gate builds its jj sandboxes from internal definitions; there is no
  separate expected.json for C2). Freezing exactly the harness is therefore the *minimal*
  set that could ever have demonstrated pre-build — and it demonstrably does not, because
  the harness was created in the same commit as the first impl change. This is exactly the
  defect the outside ruling names, so the register's frozen set is what makes the oracle
  comparison meaningful.
- A stricter registrar could add contract.md / wave1-context.txt / the pinned baseline copy
  to `frozen`; per falsification attempt 1, that changes neither the verdict nor the
  outside-ruling comparison (still co-evolved, still agreeing). The C2 count contribution
  (0 overclaims, 0 oracle_disagreements) is invariant across all defensible sets.

## Verdict

**AGREE with register row r17-C2.** Derived I=273aa74, L=2be8294, co_committed=true,
verdict=co-evolved; declared `unlabeled` is correct (LOG.md:1197 is a constancy statement);
outside ruling at corpus/lessons/round-17-verifier-spotcheck.md:169-172 is co-evolved and
matches the derivation → oracle agreement holds for this row (contributes 0 to the C2
overclaim count, 0 disagreements). The frozen/impl sets are correct and minimal-strongest;
no defensible alternate set changes the verdict or the comparison. Falsification attempt
failed; the row survives.

Minor note (no action): the register could have listed `.ufo/waves/round-17/frozen/mori-census.sh`
as an additional frozen path for symmetry with C3's witness pinning; verdict unchanged
(L = 273aa74 = I → still co-evolved).
