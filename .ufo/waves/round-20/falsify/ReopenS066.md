# ReopenS066 — falsify verdict: HOLDS (all five fields)

Independent re-open of source S066 on 2026-10-21. Fetched the pinned bytes myself from
`https://raw.githubusercontent.com/approvals/ApprovalTests.Python/5d98f0c166ad2dde7ff60effb12427db8183805e/README.md`
and checked the row in `corpus/SOURCES.md:72` and the Gate row in `corpus/lessons/round-20.md:41`.

## Per-field verdicts

**1. Quote present verbatim at stated location — HOLDS.**
- Byte identity: `curl -fsSL <url> -o README.md && sha256sum README.md` →
  `db6b2f6a1aa542dbb262dc655c6c40d3703d7c04b89b44adcd6c3e1d3e30de0b` (239 lines), exactly the
  raw sha256 recorded in the S066 row anchor (`corpus/SOURCES.md:72`) and the abbreviated hash
  in `corpus/lessons/round-20.md:49-50`. I verified the row's claims against these exact bytes.
- `grep -F -c 'Either you will update the master because you expected the changes and they are good' README.md` → `1`.
  The Gate quote (curly “ ” are delimiters) is an exact ASCII substring of fetched line 75:
  `examine the differences. Either you will update the master because you expected the changes and they are good,`
  (trailing comma of the sentence excluded from the quote — standard, not a deviation).
- Stated location "README.md line 75, Overview": `## Overview` is line 70, body lines 72-77;
  line 75 carries the quote. The SOURCES anchor "README.md lines 72-77 Overview" is also exact.

**2. ≤25 words — HOLDS.** Quote word count `wc -w` → **15**.

**3. Tier honest for scope — HOLDS.** Tier A with scope deliberately narrowed to "golden-master
approval flow only: a changed result is examined before the approved master is updated". For its
own approval flow, the project's own README at a pinned commit is a primary descriptive source;
consistent with peer README rows S016/S017/S025/S026 (all tier A, commit-pinned). The corpus
demonstrates tier discrimination around S066: Feathers' essay = B (S067), Wikipedia = C rejected
(S072). No explicit tier legend exists in SOURCES.md, SKILL.md, or PROVINCE.md — the A/B/C
semantics are [INFERENCE from observed registry convention]; the narrowing itself is observed.

**4. Teaches grounded — HOLDS.** Row teaches: "A differing result is a decision point: update the
master only when every difference is expected and good, otherwise restore behavior; grounds
classify-every-token-before-re-pin for the census drift baseline." Directly supported by fetched
lines 72-77 (results differ → reporter launches an external app to examine the differences →
update the master if expected and good, else update/roll back code). The re-pin application is
presented as grounding, not attributed to the README, and the scope cell restricts the row to
"approval flow only" — no overclaim. Downstream use is faithful: `corpus/knowledge/drift-repin-r20.md:70-71`
reads "MORI_DRIFT: none means 'unchanged since pin', never 'healthy' (S066's master is approved,
not proven correct)".

**5. Status/used-by consistent — HOLDS.** status=`mined`, recheck=`180d`, used-by=`corpus/knowledge/drift-repin-r20.md`.
- Path exists and cites S066 twice: line 7 "Sources: S066 (approval flow: examine every difference
  before updating the master)" and line 70 "(S066's master is approved, not proven correct)" —
  both faithful paraphrases of the pinned text.
- `corpus/lessons/round-20.md` additionally cites S066 (line 14 "Sourced: S066, S067"; Gate row line 41);
  used-by cells listing knowledge notes while lessons cite separately matches registry convention
  (e.g. S068/S071). status/recheck values match sibling r20 rows; lesson line 50 records
  "Status/recheck/used-by changes to existing rows: none" — consistent with what I observe.

## Verdict

**HOLDS** — every field. The row is pinned to exactly the bytes served at the recorded commit
(sha256 match), the Gate quote is byte-exact at the stated line, and no field overstates the
source's scope or authority.

## Provenance of this check

- Commands (exit 0): `curl -fsSL <pinned raw URL> -o README.md && sha256sum README.md && wc -l README.md`;
  `grep -F -c '<quote>' README.md` → 1; `printf '%s' '<quote>' | wc -w` → 15.
- Local copy retained at `.ufo/waves/round-20/falsify/ReopenS066/README.md`.
- Tools installed: none (curl/sha256sum/wc/grep already present); no pacman transactions.
- Bounds respected: read-only on the lane; no grep/glob outside the named corpus files and my
  scratch dir; no `.ufo/interactive-sessions/`, `.ufo/worktrees/`, `.jj/`, or `~/.omp` access;
  no subagents; no peer messaging needed.
