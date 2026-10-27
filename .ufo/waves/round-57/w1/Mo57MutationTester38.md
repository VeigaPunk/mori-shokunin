# C1 counter attack — Mo57MutationTester38

**Verdict: coverage finding; behavioral probe inconclusive.** The frozen counter has a junk-row acceptance path, but its hard-coded repository path prevents exercising a scratch fixture without changing the detector. No production bytes or frozen predicates were changed.

Evidence: `.ufo/waves/round-57/count-c1.py:7` runs `git -C /home/vgpnk/Projects/shokunin/mori-shokunin show {R}:SCORECARD.md`; line 10 splits the `## Capabilities` section; lines 11–12 accept exactly two lines if they contain either target token, `.ufo/waves/round-56/`, and `| 56 |`. There is no evidence-pointer resolution or evidence-content check. This is weaker than the frozen C1 predicate in `contract.md` (“resolvable round-56 evidence pointer”).

**Exact junk-row bytes** (insert in the capabilities section, replacing/adding the two rows):

```text
| junk | driver-liveness | `.ufo/waves/round-56/no-such-evidence-a` | 56 |
| junk | vote-binding | `.ufo/waves/round-56/no-such-evidence-b` | 56 |
```

For a revision `R` containing those rows and no other target-token rows, the counter's code predicts stdout `C1=met rows=2 evidence=ok rev=R` and exit 0, despite both pointers being nonexistent. The counter does not actually resolve either pointer.

**Mutation protocol / outputs:** Contract read first. Scratch directory explicitly created at `/fast/scratch/hyaku/mori-r57/Mo57MutationTester38`; pristine archive of frozen tip `618562c72a03dc4d17386b715357f863fd327274` extracted there. No detector was run: the script's fixed absolute `git -C` target cannot observe a scratch revision, and committing a mutation to the lane would violate the no-mutation boundary. Thus pristine/mutated/restored detector outputs and hash comparison are unavailable; do not count this as a killed mutant. Scratch archive is disposable and left only under the designated scratch path.
