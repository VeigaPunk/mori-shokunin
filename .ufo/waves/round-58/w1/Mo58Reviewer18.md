# Mo58Reviewer18 — C1 do-nothing review

## Finding — high: C1 already scores met at the entering revision without a round-58 change

The frozen C1 counting command, run against entering revision `b783d0b892637ce8d20f188cad20e4d8913ca635`, exited 0 and returned the exact target state:

```text
$ python3 .ufo/waves/round-58/count-c1.py b783d0b892637ce8d20f188cad20e4d8913ca635
C1=met rows=2 pointers=ok manifest=ok binding=ok failed=none rev=b783d0b892637ce8d20f188cad20e4d8913ca635
exit 0
```

This is the cheapest no-work state: no changes to the lane or fixtures, merely running the supplied counter at the specified entering revision. The report contradicts contract.md lines 29–34, particularly its specified before/control unmet result and statement that the counter does not exist at entering revision. The active register and both keyed rows are present in entering SCORECARD.md; the counter implementation at the current working tree reads that historical scorecard with `git show` and validates pointers at that revision, but obtains `MANIFEST.json` from the current fleet filesystem (`count-c1.py` lines 109–119). Thus the command's all-green output is not evidence that the frozen counter itself existed at entering revision, yet it disproves the stated counter's C1 unmet-before behavior.

For comparison, the exact same command shape at freeze revision also returned `C1=met rows=2 pointers=ok manifest=ok binding=ok failed=none`, exit 0. No counter bytes, lane files, or VCS state were changed.

Bounded method: read the frozen contract and counter; checked disk guard (green, 550.1G free on `/fast/scratch/hyaku`); ran the frozen counter once at each contract-named revision; checked entering SCORECARD for active-register phrase and the two R56 keys. No fixtures or additional repository inspection. Scratch directory was created at `/fast/scratch/hyaku/mori-r58/Mo58Reviewer18` and set as TMPDIR; it contained no evidence artifacts and was removed before handoff.
