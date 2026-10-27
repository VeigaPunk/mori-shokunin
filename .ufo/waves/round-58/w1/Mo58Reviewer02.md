# Mo58Reviewer02 — C1 pointer-path adversarial check

**Result: no counterexample found in the scoped path checks.** I read the frozen contract and both frozen counters; inspected C1 `measure()` lines 93–108. Its pointer check passes only backtick tokens beginning `.ufo/`, `tools/`, or `corpus/` to `git cat-file -e <rev>:<path>`.

Bounded scratch fixtures used freshly initialized, committed throwaway repositories under `/fast/scratch/hyaku/mori-r58/Mo58Reviewer02/` (never lane VCS). Two rows and pointer forms were varied; each run reports `binding=ok`. Results:

- Existing in-tree control path: `pointers=ok`.
- Malformed traversal `tools/../tools/mori-vote-bind.py`: `pointers=bad`, `failed=pointers`.
- Absolute `/etc/passwd` and parent/wrong-tree `../mori-shokunin/tools/mori-vote-bind.py`: these do not begin with an accepted prefix and are ignored by the pointer loop; fixture verdict `pointers=ok` for each.
- Missing accepted-prefix `tools/no-such-tool.py`: `pointers=bad`, `failed=pointers`.

The absolute and wrong-tree forms were tested in isolation with the other required pointers present. **Scope caveat:** those adversarial strings do not constitute a false-green full counter verdict because the frozen counter separately reports `manifest=bad`; the fixtures’ end-to-end exit remains 1. The experiment establishes the pointer sub-verdict omission, not a complete false-green. No claim is made about paths outside these forms.

No source, registry, SCORECARD, LOG, or lane VCS changes. Scratch was removed after preserving this report; disk guard status was available with 548.8G free on `/fast/scratch/hyaku`.