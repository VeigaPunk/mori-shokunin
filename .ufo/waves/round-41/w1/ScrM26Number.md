# ScrM26Number — M26 draft: frozen r40 35/17 baseline vs r41 36-as-of tip after S231

- Seat: `L1-mori-r41-attempt2.ScrM26Number` (scribe, leaf — no subagent dispatch)
- Date: 2026-10-24 · Lane: mori-shokunin round 41, attempt 2 · Policy: prepared v2 wave (64 seats, 31 attack), not dispatched from this seat
- Ticket (verbatim): "Draft M26 distinguishing the frozen r40 35/17 baseline from the r41 36-as-of tip after S231."
- Bounds honored: read-only except this file; no production edits; no lane Git/jj/index mutation; no sibling-repo opens; **no tool installs or updates performed** (tooling directive: none needed; pacman pause not tested, not attempted).

## Axes (named)

Lane axes this round (contract + SCORECARD "Held" line): coverage 6, operability 7, depth 5, calibration 5, freshness 5, adjacency 6; lowest live tie is depth/calibration/freshness at 5. This seat works the **calibration** axis (C3 correction records) against the **depth** axis's landed-tip semantics (C2 P-C12 timing line), with freshness served by grounding in 2026-10-24 receipts. Moves kept: report-only drafting — improves calibration clarity, harms none (zero surface mutation).

## The distinction, stated once, precisely

Three revision universes carry three different supersede-set counts. They are not competing measurements of one state; each count is bound to its revision.

| revision | as-of ids | stale | extension rows | where observed (this seat read) |
|---|---|---|---|---|
| `e37dcc6` (r40 mid-history guard) | 33 (S041…S193; no S226, no S229) | `[S069]` | not derived | `.ufo/waves/round-41/evidence/control-after.txt` §"C2 after e37dcc6", timing line verbatim |
| `62a207f7521fa2e2fcd2e8b0260f047ccfce8862` — r40 closure tip, T1, **the frozen r40 v3 gate reference** | **35** (incl. S069, S226) | `[]` | **17** (S226 plus 16 earlier, never-edited) | `control-before.txt` §C2 before lane line; §C3 `observed_as_of=35 observed_extension=17`; `calibration-after.txt` |
| `aa161e998eb22282e3d96ed2710bb0b39e5163de` — r41 measured tip (C1/C2 after-receipts) | **36** (35 + S229) | `[]` | not derived anywhere | `control-after.txt` §"C2 after lane line", timing line verbatim: `superseded_as_of=[…,S226,S229] stale_supersede=[]` |

Why the tip is 36 while the calibrated baseline stays 35/17:

1. S231 (r41 correction row, `corpus/SOURCES.md:237`, "supersedes S229") makes the pair (S229 → S231) present at R. S229 is never-edited: it appears in **no** `changed` event in either before or after receipt (both list the same 18 changed ids; S229 absent from each).
2. Under P-C12's eligible-set rule, "a never-edited superseded id's last immutable-cell edit is its first-sighting commit, so it reaches the as-of/stale test" — S229 therefore joins `superseded_as_of` at the landing tip: 35 + 1 = 36, `stale_supersede=[]`.
3. The C3 counter is revision-pinned, not tip-pinned: `tools/mori-round41-calibration.py <measured-tip> --repo <repo> --reference-rev 62a207f…` "loads the reference gate bytes from the reference commit, derives observed as-of and extension counts" (contract C3). Hence `calibration-after.txt` reports `MORI_R41_CALIBRATION mismatches=0 observed_as_of=35 extension_rows=17` even at a tip whose own timing line counts 36. The 36 belongs to C2's universe; the 35/17 belongs to the reference universe. Neither supersedes the other.
4. Extension-row hazard: by P-C12's never-edited rule, S229 would join the extension set at the tip (S226 plus 17 earlier → 18). **No receipt derives a tip-side extension count** — the only extension figures printed anywhere are the reference-derived 17 (before: mismatched 16/MISSING records; after: 17/17/17). [INFERENCE] The 18-at-tip figure follows definitionally but is unmeasured; asserting it in any record without its own derivation would itself be an instance of the M26 class below.

## Draft M26 (lesson-table row, sibling M25's shape)

| id | class | evidence pointer | captured-by | fix |
|---|---|---|---|---|
| M26 | count-universe conflation (a supersede-set extension at the r41 tip read as re-opening the calibrated r40 baseline counts) | `evidence/control-after.txt` §"C2 after lane line" (36 as-of incl. S229, stale `[]`, measured tip `aa161e99…`) vs `evidence/calibration-after.txt` (`mismatches=0 observed_as_of=35 extension_rows=17`, reference-derived) and §"C2 after e37dcc6" (`stale_supersede=[S069]`); correction records at `SCORECARD.md:2271`, `LOG.md:2363`, `corpus/lessons/round-40.md:70`; r40 closure `corpus/lessons/round-40-verifier-spotcheck.md:107-112` §"Number-drift in the correction layer" | none today — the frozen counter is `--reference-rev 62a207f…`-pinned and reads only the three single-line records (`corpus/lessons/round-40.md:72-73` notes the counter's one-line regex), so no committed check fails a document that cites 36 as the corrected as-of count or asserts a tip-side extension total; nearest rule is QUALITY 20 "tally cites the counted universe recomputed from delivered artifacts" — wording only, no mechanism | state the two-universe sentence in the correction layer (append-only; exact draft below). Shown able to fail: the same counter's failure mode on drifted recorded counts is observed — before-run prints `mismatches=6` on 34/16 records (`evidence/control-before.txt` §"C3 before calibration": `SCORECARD.md recorded_as_of=34 observed_as_of=35 … LOG.md recorded_extension=MISSING … MORI_R41_CALIBRATION mismatches=6`); the specific 36-record mutant was **not** executed by this seat (scribe bounds) — executor recipe below |

Draft sentence for the correction layer (candidate, append-only):

> The 35/17 calibration values are the frozen r40 gate's derivation at reference `62a207f7521fa2e2fcd2e8b0260f047ccfce8862` (T1); the landed r41 tip's timing line counts 36 as-of ids because S231's supersede of S229 extends the eligible set by one never-edited id. The two numbers are counts over different revisions of one append-only ledger, not competing measurements of one state; neither supersedes the other, and any extension-row figure for the tip requires its own derivation at its own revision.

Executor recipe to demonstrate the fix able to fail (not run by this seat): in a disposable clone, replace one single-line record with `Round-41 calibration correction: observed_as_of=36; extension_rows=17.` and run `python3 tools/mori-round41-calibration.py <tip> --repo <clone> --reference-rev 62a207f7521fa2e2fcd2e8b0260f047ccfce8862`; expected nonzero mismatches (recorded_as_of=36 vs observed_as_of=35). Unexecuted here; marked as such.

## Landed-state conflict (reported verbatim for the canonical judge)

The committed round-41 lesson (HEAD `7450722e`) already fills the M26 slot with a different class — `corpus/lessons/round-41.md:34`:

> | M26 | landing (registry rows committed without their opened-source copies) | attempt-1 commit `d72ac16` added S230/S231 rows + `corpus/knowledge/conform-bindings-r41.md` citing them, but no `corpus/evidence/sources-r41/` copies existed; QUALITY 9 (every path/citation resolves at the carrying commit) | none — the census checks row shape, not copy presence; the locator claims were unverifiable until the copies landed | fetched and committed `corpus/evidence/sources-r41/{S230,S231}.src` this round; located quotes re-derived from the committed bytes. Shown able to fail: `test -f corpus/evidence/sources-r41/S230.src` exits 1 at `d72ac16` |

This ticket scopes M26 to the 35/17-vs-36 count-universe distinction. Both rows are recorded; renumbering, merging, or discard is the judge's/orchestrator's call, not this seat's. Note the landed M25 row already owns the 34/16→35/17 recurrence; this draft is the successor hazard (don't let the tip's 36 re-open the calibrated 35/17), not a duplicate of M25.

## Provenance (exact, this seat)

Read-only commands/facts run:
- `git -C /home/vgpnk/Projects/shokunin/mori-shokunin log --oneline -6` → `7450722e` (after-measurement receipts, SCORECARD r41 declaration, lesson fix), `c5326c61` (single-line calibration records), `aa161e99` (C3 records 35/17, r41 lesson, S230/S231 copies, freeze verify, attempt-1 receipt), `e4293ad9`, `d72ac167` (freeze C1–C3 contracts and controls), `62a207f7` (r40 closure). HEAD = `7450722e`.
- `git status --porcelain` → untracked only: `.ufo/waves/round-41/evidence/wave-run.json`, `wave-run.stderr`, `w1/` (this wave's outputs; expected mid-wave).
- `ls corpus/evidence/sources-r41/` → `S230.src` (113,070 B), `S231.src` (63,374 B, 868 lines) — the landed M26-landing fix's copies exist at HEAD.
- Byte-read receipts/files: `skill://godspeed`; `.ufo/waves/round-41/contract.md`; `evidence/control-before.txt` (§C2 before lane line, §C3: `MORI_R41_CALIBRATION mismatches=6 observed_as_of=35 extension_rows=17`); `evidence/control-after.txt` raw:106-151 (after lane line 36 as-of incl. S229; e37dcc6 stale `[S069]`); `evidence/calibration-after.txt` (all rows 35/35/17/17, `mismatches=0`); `corpus/SOURCES.md:234-237` (S228–S231 rows; S231 "supersedes S229", 17 words at `S229.src:294-296`); `corpus/lessons/round-41.md` (Gate table S230/S231 admitted 2026-10-24; M25/M26 rows raw:30-34); `corpus/lessons/round-40.md:49-73` (appended correction + single-line record); `corpus/lessons/round-40-verifier-spotcheck.md:106-130` (number-drift section: SCORECARD.md:2234, LOG.md:2296, M24 "16 rows: S226 plus 15 earlier"); `LOG.md:2350-2366`; `SCORECARD.md:2262-2273, 2292-2303` (C2 row "lane-history verdicts preserved (36 as-of; S069 stale at e37dcc6)", C3 row, Held axes); `evidence/freeze-r41.txt:6-10` (contract sha256 `6427bbbe…`, conform.py sha256 `e1f2e11e…`; "SOURCES.md S230/S231 rows are round data").

Known limits:
- Some display reads truncated long lines (>768 chars); every load-bearing quote above is from a raw read or a fully displayed line. The contract's P-C10/P-C12 verbatim bodies were taken from the receipts' printed predicate lines, not re-derived from truncated contract display.
- Not executed: the 36-record counter mutant (see recipe); the tip-side extension derivation; census bookends read only via contract attribution (229 rows, exit 0, 16 W04) — census files themselves not opened by this seat.
- No dispatch surface: the prepared 64-member wave remains undispatched; this seat wrote only `.ufo/waves/round-41/w1/ScrM26Number.md`.

## Suggested main-agent checks

- `git -C /home/vgpnk/Projects/shokunin/mori-shokunin status --porcelain` — only wave-run/w1 entries besides siblings' reports.
- Confirm the M26 adjudication decision lands wherever the canonical judge records it; the landed lesson row and this draft must not silently coexist under one id.
