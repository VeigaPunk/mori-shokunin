# ScoutPriorRound — r36 routed defects vs r37 dispositions

Attacks: whether every defect routed in `corpus/lessons/round-36-verifier-spotcheck.md` and `corpus/lessons/round-36.md` has an r37 disposition claimed in `.ufo/waves/round-37/contract.md` and `corpus/lessons/round-37.md`.

Axes: (1) completeness of the routed set, (2) a named disposition in those two r37 texts, (3) an artifact the disposition names. A move that only restates (a)–(h) fails (1).

No tools installed. Lane files not edited. Text reads only; no language server (markdown/prose, not a symbol contract).

## Routed set

Spotcheck § "Routed defects and notes for the lane (fix next round)" (`round-36-verifier-spotcheck.md:50-59`) plus the two r37-routed notes in `round-36.md` (M4 residual `:56`; collateral `:72-79`; null-agent registry note `:63-65`). Operator item 6 and SHONEN item 7 are notes, not lane defects. Interloper `c081375` (`:11`) is recorded, not routed to r37.

## Table

| defect | source | r37 disposition (contract / lesson) | artifact | has disposition |
|---|---|---|---|---|
| r17-jj `jj_config_redirected` side-effect red | `round-36.md:72-79` (options: pin scratch in a jj workspace, or scope the assertion) | **(d)** scoped to the redirect property; jj-file required only when a sandbox has a jj workspace. Lesson M4, "re-run green" (`contract.md:87`, `round-37.md:35,48-49`) | `tools/mori-round17-jj-regressions.py:1040-1069`; `evidence/r17-jj-selftest-r37.txt:2` `EXIT=0` (the ok-line is `expect()` ids, so the string `jj_config_redirected` is absent by construction) | yes |
| absolute operator paths in r36 evidence (SentData) | spotcheck `:59` | **(e)** counters print repo-relative lane paths (`display_path`); "no new evidence file carries an absolute operator path" (`contract.md:88`, `round-37.md:49-50`) | `count-c1.py:831-833` `display_path` exists. Claim about new evidence is false — see below | yes (claimed; artifact contradicts the sentence) |
| count-c2 SIGKILL of its own sandbox child on timeout | spotcheck `:55`; `round-36.md:56` | **(f)** disclosed: 120 s, SIGTERM then SIGKILL after 5 s, state `tool_timeout`, not a list mismatch (`contract.md:44-47,89`, `round-37.md:50-51`). Not the SCORECARD "avoid SIGKILL" plan | `count-c1.py:27-29` | yes (disclosure, not removal) |
| 9-vs-7 drifted prose | `round-36.md` M2 `:54` (fixed in r36); spotcheck quality `:37` | **(h)** re-verified: nine, S210/S211 named (`contract.md:91`, `round-37.md:52-54`) | `corpus/knowledge/source-drift-r36.md:24-33`; `corpus/README.md:568-574` | yes |
| count-c1 "docstring still says v1" | spotcheck `:55` | only the class sentence: "Frozen-byte residuals from round 36 remain frozen evidence and are not edited" (`round-37.md:54`). Not named | module docstring `count-c1.py:2-34` does **not** say v1. Only `v1` token is `:570` ("the v1 root"), inside `real_root` | class-only |
| counters miss SOURCES.md delete+restore inside a round | spotcheck `:55` | class sentence only (`round-37.md:54`). **(c)** is a different defect (per-id `deleted <id>` lines, `contract.md:86`) | no successor check in `contract.md` P-C1 | class-only |
| no 429/4xx path (`oracle_excluded=0`) | spotcheck `:55` | class sentence only. Not a C2 check | `contract.md` P-C2 names cap + redirect, not 429 | class-only |
| freeze-pointer slip: report ties sha `c7edaacf…` to `freeze-v3.txt`; sha256 pins live in `freeze-v2.txt:4` | spotcheck `:52`. Quote is real: fleet `.ufo/reports/round-36/mori.md:72`. v3 pins are git blobs (`freeze-v3.txt:8-11`) | **none.** Contract debt table and lesson do not mention the pointer, `c7edaacf`, or `freeze-v2` | correction asked for "the next round's report or a lesson addendum". Neither file corrects it. Fleet `.ufo/reports/round-37/mori.md` also has no match | **no** |
| partial wave: keep the never-returned w2 seats on the r37 verification list until superseded | spotcheck `:54` (says 62/66, 4 seats). Later report text says 65/66, one unnamed seat (`.ufo/reports/round-36/mori.md:157-160`) | **none.** No verification list in contract, lesson, or `dispatch-log.txt` | observed now: `w2-spec.json` 66 items, `w2/*.md` 65, missing **`ExecGateRound`** only. Not named in r37 | **no** |
| w2 registry null agent ids; record real seat ids in the r37 dispatch log if inline dispatch is used again | spotcheck `:56`; `round-36.md:63-65` | **none.** Lesson says the wave was returned for orchestrator-inline dispatch (`round-37.md:42-44`) and does not mention seat ids | `dispatch-log.txt` (16 lines) records no seat id. `w1-plan.json` spawn rows still have `"agentId": null` | **no** |

## Not lane defects (disposition is the r36 classification)

| note | source | r37 contract/lesson | elsewhere |
|---|---|---|---|
| untracked `.scratch/` | spotcheck `:53`, restated as operator-owned `:57` | silent | fleet report `.ufo/reports/round-37/mori.md:154` "untouched" |
| LOG.md:1801, `refs/jj/keep 3b19cac`, `.scratch/`, SHONEN promotion | spotcheck `:57` "not lane debt" | silent | same report `:162-163` "carried unchanged" |
| SHONEN boxes look checkable | spotcheck `:58` observation | silent | not a defect |

## Letters claimed in r37 that these two files do not route

`(a)` drift-hardening verify, `(b)` memoization N1, `(c)` per-id `deleted` lines, `(g)` seed-collision scratch are in `contract.md:84-86,90` and `round-37.md:47-52`. They are not routed defects in the two lesson files. `(g)` is named in the r36 report (`ExecReC2B`) and in `dispatch-log.txt:16`, not in `round-36.md`.

## (e) artifact vs sentence

Command: search `/home/vgpnk` under `.ufo/waves/round-37/evidence/`.

Hits in new evidence:

- `c1-before-memo.txt:2` `tool: /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-37/fixtures/memo-n1.py` (r36 counter output)
- `c1-before-summary.txt:2` same shape for `summary-only.py`
- `census-start.txt:16` and `census-end.txt:16` `mori ok /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md`

No hit in `c1-after.txt`, `c2-after.txt`, or `drift-live-r37.txt`. The new counters' own scored receipts match `display_path`. The disposition sentence "no new evidence file carries an absolute operator path" does not.

## Missing-seat command

```
python3: w2-spec.json items=66; w2/*.md=65; missing=['ExecGateRound']
```

## VERDICT: FAIL

Three routed lane defects have no disposition in the r37 contract or lesson: the freeze-pointer slip, the never-returned w2 seat(s) (disk: `ExecGateRound`), and null agent ids under a repeated inline dispatch. Class-only carry (`round-37.md:54`) covers the docstring / delete+restore / `oracle_excluded=0` residuals but does not name them. Debt (e) is claimed and its "no absolute path in new evidence" sentence is false on the four files above.

Confidence: high on the text comparison; high on the 65/66 count and the `/home/vgpnk` hits (observed this session).
