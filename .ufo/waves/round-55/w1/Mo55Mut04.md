# Mo55Mut04 — C2 source/quote mutation probe

## Result

**Verdict: inconclusive; no mutant was exercised.** The scratch copy contains only the detector and contract; the bounded counter's `main` reads a git revision through `git_reader`/`git_lister` and its C2 vote/data inputs are revision-backed. I did not run an equivalent detector against incomplete fixtures or mutate lane/source data, because either would not be the same bounded behavioral detector requested.

## Evidence

- Read-only disk guard: `/fast/scratch/hyaku` reported 594.6G free; no ENOSPC stop condition.
- Detector source: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-55/count-c2.py`, lines 184–197 and 205–218 show `evaluate` depends on the revision reader, pinned source copies, entry, and vote data. Lines 144–174 show output-bound voter inputs.
- Scratch setup command: `mkdir -p "$S"; cp .../count-c2.py "$S/count-c2.py"; cp .../contract.md "$S/contract.md"`, with `trap 'rm -rf -- "$S"' EXIT`. Exit 0. Scratch was removed by the trap.
- Scratch hashes before cleanup: counter `ccb2333a7e3d6744f00041b5bb95a95cb5191b6b5d5a8a963949db4891e12754`; contract `3050b1fd99763114fbbc6d39b5e782101d82e8881ac7b4d19ce4f91cfebd6c17`.
- Actual detector output: not run. No pristine/mutant/restored observations or input-byte hashes exist; consequently restoration cannot be claimed beyond the scratch cleanup above.

## Findings

- **Unverified / inconclusive — assigned mutants not tested.** Quote echo, wrong source URL, missing used-by, and malformed-row cases require a complete isolated git-backed fixture and C2 data/vote inputs. Evidence: detector source lines 184–218; scratch hashes and cleanup command above.
