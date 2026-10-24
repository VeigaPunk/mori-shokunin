# MutC2Knowledge — C2 knowledge-binding mutant (round 37, wave 1)

Attacks: the knowledge-binding clause of P-C2 — "the committed corpus binds the hardening
(knowledge entry citing this round's source rows and commit 8ff9bba …)" — as implemented at
`.ufo/waves/round-37/count-c2.py:188-193`:

```
rows = re.findall(r"\bS2\d\d\b", knowledge or "")
check("knowledge", knowledge is not None
      and "huge_cap" in knowledge and "redirect_private_refused" in knowledge
      and HARDENING_COMMIT in knowledge and bool(rows), ...)
```

## Setup

Throwaway clone (not the lane), based on the scored tip e57c58b:

```
mkdir -p /fast/scratch/hyaku/mori-r37/MutC2Knowledge
git clone --no-local -q /home/vgpnk/Projects/shokunin/mori-shokunin clone
git -C clone switch -c mut-knowledge e57c58b57c025364e79d130fbdf764d2674d83d6
```

Clone path: `/fast/scratch/hyaku/mori-r37/MutC2Knowledge/clone`
Base rev: `e57c58b57c025364e79d130fbdf764d2674d83d6` (ancestor of `master`, so the clone carries it).

## Mutant

In the clone only, `corpus/knowledge/source-drift-hardening-r37.md` was rewritten byte-wise:

- all 15 `\bS2\d\d\b` citation tokens (`S205`, `S221`–`S225`) → `S2XX`;
- both `8ff9bba` occurrences → `<removed>`.

Nothing else changed; `huge_cap` and `redirect_private_refused` remain (the mutation isolates the
citation + commit binding, not the arm names). Committed as:

```
mutant_rev = a1ae241749b44675267dea3e1f14692b12333871
corpus/knowledge/source-drift-hardening-r37.md | 11 insertions(+), 11 deletions(-)
```

File hashes (sha256):

- pristine (also identical to the lane file): `364c3152de22378d162decb2c8a0c36589d1382171f41e8d450234524d9d4525`
- mutant: `e2c58608181d07e012f3a5895b6829d7a7bf6e8cce2d20c36a28e3d1e9f19021`
- mutant bytes match the citation/commit pattern 0 times (`grep -cE '\bS2[0-9]{2}\b|8ff9bba'` → `0`).

## Detector runs (same bounded counter on all three states)

Command shape:

```
python3 .ufo/waves/round-37/count-c2.py <rev> --repo /fast/scratch/hyaku/mori-r37/MutC2Knowledge/clone
```

Observed, in order:

1. Pristine `e57c58b` (baseline, run before any mutation):
   `check knowledge PASS (present=True rows=['S205', 'S221', 'S222', 'S223', 'S224', 'S225'] cited_commit=True)` / `C2=met` / `EXIT=0`
2. Mutant `a1ae241`:
   `check knowledge FAIL (present=True rows=[] cited_commit=False)` / `C2=unmet` / `EXIT=1`
   (all six other checks still PASS: tool_present, selftest, cap_kill, redirect_kill, capability, readme, live)
3. Restored `e57c58b` (after `git reset --hard`):
   `check knowledge PASS (present=True rows=['S205','S221','S222','S223','S224','S225'] cited_commit=True)` / `C2=met` / `EXIT=0`

Raw outputs: `/fast/scratch/hyaku/mori-r37/MutC2Knowledge/{baseline.txt,mutant.txt,restored.txt}`.

## Verdict

Expected: `knowledge FAIL` and `C2=unmet` at the mutant rev — observed exactly. The citation and
commit binding in the knowledge check is load-bearing: **mutant killed**.

VERDICT: PASS

## Restoration evidence

```
git -C clone reset --hard -q e57c58b57c025364e79d130fbdf764d2674d83d6
restored_rev=e57c58b57c025364e79d130fbdf764d2674d83d6
sha256(corpus/knowledge/source-drift-hardening-r37.md) = 364c3152…d4525   (== pristine)
git status --porcelain = (empty)
```

The mutant commit object `a1ae241` still exists in the disposable clone (deliberately, as probe
evidence); the working tree and the measured rev are the pristine tip and the counter is green
again. The lane repo was not written: `count-c2.py` and the probe selftest run from copies, and
`sha256(corpus/knowledge/source-drift-hardening-r37.md)` in the lane is still
`364c3152…d4525`. Lane HEAD moved `c31076e → 0a05f7e` during the wave from peer commits, not from
this seat (only `git cat-file`/`git show`/`rev-parse`/`merge-base`/`log` reads were issued against
the lane).

## Coverage note (reading-based, not executed — not part of the verdict)

`rows` accepts any single `\bS2\d\d\b` token anywhere in the entry, so the check verifies "some
S2xx is cited", not P-C2's "this round's source rows" (S221–S225) and not that all five are
present; the commit binding is likewise a bare substring test. A variant that replaced S221–S225
with unrelated S2xx ids while keeping `8ff9bba` would pass this check. [INFERENCE] — this was not
run, per the one-mutant bound; the assigned mutant (remove citations **and** the commit string) is
the one measured above and it is killed.

## Installs / updates

None.
