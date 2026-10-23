measured 2026-10-23T09:15:36Z
# QUALITY 102 mutation probe

Axes: forbidden-cell sensitivity; permitted-recheck specificity; source-free supersession coverage; exact-byte restoration and containment.

Scope: `corpus/QUALITY.md:799-808` and `.ufo/waves/round-35/check-sources-appendonly.py` at `cedb0ec4f3a4f672804deac388b7191258f01fcd`. Pinned copies: `/fast/scratch/hyaku/mori-r35/MutQ102/QUALITY.md:799-808` and `/fast/scratch/hyaku/mori-r35/MutQ102/check-sources-appendonly.py:1-109`.

Below, `$S` means `/fast/scratch/hyaku/mori-r35/MutQ102`; all abbreviated scratch citations expand to that directory. The isolated clone is `$S/repo`.

## Detector and baseline qualification

Every receipt records this exact command shape, with its measured revision substituted:

```sh
timeout --signal=TERM --kill-after=2 120 python3 -I -B /fast/scratch/hyaku/mori-r35/MutQ102/check-sources-appendonly.py REV --repo /fast/scratch/hyaku/mori-r35/MutQ102/repo
```

Each process had a 1,073,741,824-byte address-space cap; command, cap, raw exit, stdout and stderr are retained (`$S/M1-pristine.txt:1-25`, corresponding mutant/restored receipts).

The raw pristine checker already exits 1. Therefore raw exit 1 alone is inconclusive, never a killed mutant. QUALITY 102 explicitly permits inherited debt while forbidding the round's own touched ids (`$S/QUALITY.md:799-807`). Before mutation, I fixed a scoped behavioral detector: require valid checker output and a consistent summary, then reject any CHANGED id outside the landed debt set. The fixed set is S041,S044,S051,S062,S064,S179,S180,S181,S183,S184,S185,S186,S188,S189,S190. Scoped exit 0 means no new flagged id; 1 means a new flagged id; invalid output is inconclusive. This interpretation and predictions were recorded before mutation (`$S/probe-plan.md:5-11`). It does not change the frozen checker or criterion.

Historical run: `dd76eb79ef4f6d39c9c26647a56d3fb607308f8f`, raw exit 1:

```text
appendonly_violations=17 ids=[S041,S044,S051,S062,S064,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193]
```

Evidence: `$S/dd76eb79.txt:1-25`; S182 and S193 are explicitly flagged at lines 14 and 22.

Landed run: `cedb0ec4f3a4f672804deac388b7191258f01fcd`, raw exit 1, scoped exit 0:

```text
appendonly_violations=15 ids=[S041,S044,S051,S062,S064,S179,S180,S181,S183,S184,S185,S186,S188,S189,S190]
```

Evidence: `$S/M1-pristine.txt:1-25`. Independent pristine receipts for M2 and M3 have the same result (`$S/M2-pristine.txt:23-25`, `$S/M3-pristine.txt:23-25`).

## M1 — edit S199 teaches in place

Mutation: replace the single word `demonstrates` with `mentions` in S199's teaches cell; all other cells remain the pinned bytes. The original word is at `$S/SOURCES.md:205`; mutation commit `b77146f2c47b225feddf79c4fa276d0f7f887a73` is a direct child of the landed tip (`$S/commits.json:2-7`).

Expected: flag S199, column teaches; 16 total violations; scoped exit 1. Observed: raw exit 1, `CHANGED id=S199 origin=cedb0ec4f3a4f672804deac388b7191258f01fcd changed_at=b77146f2c47b225feddf79c4fa276d0f7f887a73 cols=teaches`; `appendonly_violations=16`; `scoped_new_ids=[S199] scoped_exit=1` (`$S/M1-mutated.txt:3,23-26`).

VERDICT: killed — M1 by the new-S199 flag, not by the already-red raw exit status.

## M2 — change only S199 recheck

Mutation: S199 recheck changes from `on-release` to `180d`; teaches and all other cells remain pinned. Recheck is excluded by the checker (`$S/check-sources-appendonly.py:20`); original row: `$S/SOURCES.md:205`. Mutation commit `4eb61e32706a101651b2af584bc6090fef1fae74` directly follows the landed tip (`$S/commits.json:16-21`).

Expected: no S199 flag; unchanged 15 inherited violations; scoped exit 0. Observed exactly that, raw exit 1, `scoped_new_ids=[] scoped_exit=0` (`$S/M2-mutated.txt:3,23-25`).

VERDICT: survived — M2 is the intended permitted-change control, not a defect.

## M3 — append a source-free superseder

Mutation: append S205 after S204. Its source cell is empty, kind and scope are `junk`, tier is C, anchor is an em dash, teaches is exactly `supersedes S041`, status is queued, opened is 2026-10-23, recheck is 365d, and used-by is an em dash. Existing rows are unchanged. Mutation commit `5a15d14d69a64226548e71bb4c1bf8148e49aaf7` directly follows the landed tip (`$S/commits.json:30-35`; the committed row is `corpus/SOURCES.md:211` at that commit in `$S/repo`).

Expected of source-integrity coverage: reject the empty-source junk row or retain S041's violation. Predicted weakness: the prefix alone discharges S041 (`$S/probe-plan.md:11`; checker `$S/check-sources-appendonly.py:46-49,80-90`).

Observed: raw exit 1, `SUPERSEDED id=S041 by=S205`, 205 parsed rows, only 14 violations, no S041 in the violation list, and `scoped_new_ids=[] scoped_exit=0` (`$S/M3-mutated.txt:3-5,23-25`). The checker reports no malformed/source-free-row error (`$S/M3-mutated.txt:24`).

VERDICT: survived — M3 exposes a source-free supersession hole.

Hole named plainly: an unsourced junk row launders an existing append-only violation. The checker validates row width and id, then trusts the teaches prefix without inspecting the superseder's source or supporting content (`$S/check-sources-appendonly.py:46-49,80-90`). The literal QUALITY 102 exception also requires only that prefix (`$S/QUALITY.md:800-801`), so this is a coverage gap in the criterion/check, not evidence that the implementation contradicts its stated syntactic exception. The raw whole-register result remains red because 14 other debts remain; this probe does not establish a green whole-register bypass.

## Exact restoration and hashes

Pristine SOURCES SHA-256, before every mutation: `cb6794c9e003448d5a68412d40d605668e0bc2b7193c964432cb8ee4fdbdd5c4` (hash of pinned `git show` bytes; `$S/probe-plan.md:5`). Mutated file hashes from bounded `sha256sum` (`$S/mutated-sha256.txt:1-3`):

- M1: `54070b5353daeb95e435fc8785ec1f2ffee4e49cf07c62b0da5db8371589a26b`.
- M2: `a314673ec35d03fe3f1297e0875845c17692f1be322939ca845a64109da170d5`.
- M3: `6a09f21f3502f4c8fde45adaf7fd7db7cb26db349e50a9fbf2f78cc5a4e0a61d`.

All three scratch files were restored in a finally block to the exact saved input bytes. Bounded `sha256sum` returned the pristine hash above for M1, M2 and M3 (`$S/restored-sha256.txt:1-3`). Checker hash remained `f56dbdafdc7e884f0598b46a21b0b440f3fbc09dc2d996077c9a7b5f1aa51f06` before/after restoration (`$S/mutated-sha256.txt:4`, `$S/restored-sha256.txt:4`).

The same detector then ran against explicit restoration commits whose parents are their mutant commits, not merely against the old tip:

- M1 restored `f3d76efb7f4cf2ba11f6709c07bd51c741a6f884`; raw exit 1, 15 violations, scoped exit 0 (`$S/commits.json:9-14`; `$S/M1-restored.txt:1-4,23-25`).
- M2 restored `bb03f40609e222691af6dcbb854201e6c02cc682`; raw exit 1, 15 violations, scoped exit 0 (`$S/commits.json:23-28`; `$S/M2-restored.txt:1-4,23-25`).
- M3 restored `a56b597faa20341f7870707fff662d4d3f1e5edb`; raw exit 1, 15 violations, scoped exit 0, with S041 back among the violations (`$S/commits.json:37-42`; `$S/M3-restored.txt:8,23-25`).

## Containment and disclosure

The clone was created with `timeout 120`, a 1 GiB address-space cap, and `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone --no-hardlinks --no-checkout /home/vgpnk/Projects/shokunin/mori-shokunin /fast/scratch/hyaku/mori-r35/MutQ102/repo`; output: clone done. All Git writes were isolated clone objects/trees/indexes, not lane/fleet Git or JJ state (`$S/commits.json:1-44`). Only this report was written in the lane. Scratch inputs, plan, receipts, hashes and clone commits remain under `$S`.

Host queries: bounded `df -h /fast` before cloning returned 167G available; bounded `date -u +%FT%TZ` returned the report timestamp. No source URLs were fetched. One read-only lane lookup of `<tip>:CORPUS.md` exited 128 because that path does not exist there; it contributes no finding. Two initial raw detector runs reproduced the 17/15 counts before the retained ten-run pristine/mutated/restored receipt set. No timeout occurred; all foreground child processes were awaited. No subagents, persistent background jobs, host changes, tool installations, tests beyond this assigned detector, integration or lane commits.
