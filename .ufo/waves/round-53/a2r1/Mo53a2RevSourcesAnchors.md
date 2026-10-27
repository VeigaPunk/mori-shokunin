# Mo53a2RevSourcesAnchors — findings

## Verification

Inspected revision `34d97cd3eaea8c13b0f065afc52aac1e5cf518a5` via `git archive` into the assigned scratch. Its `corpus/SOURCES.md` rows S502–S514 each have 11 cells. SHA-256 checks against their `corpus/evidence/sources-r53/` copies all passed for the prefixes in the anchor cells: S502 `bc178ff511e0`, S503 `c50205bc1997`, S504 `d6c5807421a6`, S505 `277e99e23ecc`, S506 `767ab88153c4`, S507 `f81feb3dfca5`, S508 `4dfcce2b8fa8`, S509 `d7bf787c910d`, S510 `8e51fb1c10fe`, S511 `ed691b24afbc`, S512 `2c26e67751f9`, S513 `4a107bc381b3`, S514 `678410005f88`.

Citation scan of archived `corpus/knowledge` finds S502–S510 only in `kernel-v7.3-recheck-r53.md` and S511–S514 only in `commit-runway-read-r53.md`, matching the names explicitly in those rows' used-by cells (SOURCES cells 10; my initial shell parser mistakenly indexed cell 10 as cell 9; the corrected cell inspection verifies the exact names). The lesson Gate table records located quotes and line positions, but I did not complete line-by-line quote/anchor validation for all 13 rows. **UNVERIFIED** for that requested check and the row teaches corrections beyond inspecting the lesson's old→new prose. No exact source-row correction established.

Command: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori`; exit code 0. Output: `mori ok /home/vgpnk/Projects/shokunin/mori-shokunin/SOURCES.md` plus 23 W04 duplicate-URL warnings (S035, S037, S073–S076, S147–S150, S166, S168, S201, S218, S220, S228, S349, S351, S470, S476, S486, S491, S492); no E findings. The working tree HEAD was the requested revision; it had four untracked attempt-2 dispatch/report paths at inspection time.

## Findings

- LOW — `corpus/SOURCES.md` S502–S514 / `corpus/lessons/round-53.md` Gate: full anchor-range and Gate-quote line resolution remains UNVERIFIED in this review; no mismatch is asserted.
