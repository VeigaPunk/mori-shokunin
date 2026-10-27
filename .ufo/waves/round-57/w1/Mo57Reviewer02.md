# C1 counter attack — Mo57Reviewer02

## Finding — High: C1 reports `met` for junk rows that violate both row coverage and evidence resolution

The frozen predicate requires two rows, one for each named capability, with a **resolvable** round-56 evidence pointer and first-working round 56 (`.ufo/waves/round-57/contract.md:5`). But `count-c1.py:10-12` only selects pipe-prefixed lines containing either capability substring, requires exactly two such lines, and searches each line for the literal substrings `.ufo/waves/round-56/` and `| 56 |`. It neither opens a pointer nor checks that one row names each capability; table syntax is not parsed.

Scratch fixture A used these exact SCORECARD row bytes:

```text
| driver-liveness | junk row: no run, no demo, nothing measured; vote-binding deliberately absent | .ufo/waves/round-56/does-not-exist.md | 56 |
| driver-liveness | second junk row: duplicate capability name, equally empty, no run | .ufo/waves/round-56/also-missing.md | 56 |
```

The counter copy differed from the frozen counter only at `repo = ...` (redirected to the scratch fixture repo; the parsing/counting code remained unchanged). Command and observed result:

```text
python3 /fast/scratch/hyaku/mori-r57/Mo57Reviewer02/count-c1.fixture.py ec2749030370e9d35891b2de011be9311c760648
C1=met rows=2 evidence=ok rev=ec2749030370e9d35891b2de011be9311c760648
exit=0
```

The evidence pointer check against that fixture revision failed as expected: `git -C <fixture1> show ec2749030370e9d35891b2de011be9311c760648:.ufo/waves/round-56/does-not-exist.md` returned `fatal: path ... does not exist` (exit 128). The second missing pointer likewise did not exist. Thus the counter reaches its target despite no `vote-binding` row and no resolvable evidence.

Additional parser falsifier: two pipe-prefixed junk rows inside a fenced code block, with the first row naming both capabilities, also produced `C1=met rows=2 evidence=ok` (fixture revision `c664384b073b36b35cc21854c6cccef13760b95b`, exit 0). This confirms fence contents are counted as rows and per-capability row coverage is not enforced.

Control: the real counter against the frozen entering revision printed `C1=unmet rows=0 evidence=bad rev=53e2b4768af93dd2472eb26ecc9b9fdca2e9daf2` (exit 1), consistent with `.ufo/waves/round-57/controls.txt`.

## Verdict

**C1 counter is unsound for its frozen predicate.** A `met` result does not establish that both capabilities are represented or that either evidence pointer resolves. No production code, counters, frozen predicates, or lane history were changed; scratch fixtures and counter copy were removed after execution.

## Residual risk / verification gap

The counter hardcodes the lane repository path (`count-c1.py:6-7`), so the attack used a scratch copy with only that repository constant redirected; the actual counter was not run against a junk revision in the lane repo, avoiding prohibited lane mutations. No LSP device was mounted (`xd://lsp` returned “No such tool”); counter and predicate evidence is from direct source reads. No other checks were run.
