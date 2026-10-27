# Mo58Reviewer06 — C2 registry binding

## Finding (actionable): malformed extra-column S550 row scores met

The frozen C2 counter accepts a malformed registry row with an extra column. At `count-c2.py` lines 102–105 it splits the row and only rejects `len(cells) < 12`; it checks the expected status and used-by values at fixed positions, but never requires the exact schema width. An otherwise conformant fixture row with ` | EXTRA |` appended therefore scored `C2=met ... rows=ok`, exit 0.

Evidence: freeze revision `fe8801120a67c1a6b8899d7d0423839caa09e7d0`; scratch receipt `/fast/scratch/hyaku/mori-r58/Mo58Reviewer06/receipt.txt`. Probe constructed isolated throwaway git fixtures using the counter's `_mkrepo` and `measure`; no production or lane VCS writes. Other attacks were rejected: duplicate S550 rows, wrong status, dangling used-by path, short column count, and lookalike S5500 ID all returned exit 1 with `rows=bad`.

## Method / scope

Read the frozen contract and counter at the named freeze revision, then exercised six targeted registry mutations against the frozen counter with conformant entry/copy content. No LSP device was available (`xd://lsp` returned “No such tool”). The finding concerns structural row parsing only; the dangling-path rejection is textual substring validation and does not establish that a referenced knowledge file exists. No production edit, VCS mutation, or external tool installation.

Scratch was created explicitly and cleared before yield; receipt retained in the assigned report directory above.
