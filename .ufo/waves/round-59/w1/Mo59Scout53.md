# Mo59Scout53 — considerthese recon: 2026-10-26 suggestion status

Seat: Mo59Scout53 (scout, leaf). Lane: mori-shokunin. Date: 2026-10-28.
Assignment: open `considerthese/2026-10-26.md` (and any newer file), list which
suggestions remain unimplemented, nominate at most one for this round, verified
against lane tools. Read-only; no commits, no VCS mutation, no fleet/sibling
writes. Frozen inputs read first: `.ufo/waves/round-59/contract.md`,
`.ufo/waves/round-59/count-c1.py`, `.ufo/waves/round-59/count-c2.py`
(freeze `60b3a76a…`, entering `2b9f0397…`). Scratch:
`/fast/scratch/hyaku/mori-r59/Mo59Scout53/` (created; nothing stored in it —
all evidence is read-only against committed bytes). `disk-guard.sh status`
green at start (27% on /fast/scratch/hyaku, 592.6 G free).

## File inventory

`considerthese/` on disk contains `2026-10-19.md` … `2026-10-26.md`; **2026-10-26
is the newest** (last commit `649e14cf`, 2026-10-26 08:43 -0300; `git log --all
-- considerthese/` shows nothing later). It proposes 4 suggestions
(`considerthese/2026-10-26.md:45-59`).

## Status of each suggestion (verified against lane bytes at HEAD `8ff344ff`)

| # | Suggestion (reflection line) | Status at entering tip | Evidence |
|---|---|---|---|
| 1 | Split pin-check mismatches into "can't run here" vs "stale" (`:47-50`) | **IMPLEMENTED** (r51) | `tools/mori-pin-check.py:140-144`: every mismatch line carries `class=env` or `class=stale`; summary ends `env=N stale=N` (`:884-892`); v5.1 rules at `:145-150`. Lesson `corpus/lessons/round-51.md:57-60`; QUALITY 139 cites `considerthese/2026-10-26.md` suggestion 1 (`QUALITY.md:1284-1286`). Round-58 contract confirms: "`suggestion 1 … is ALREADY implemented in tools/mori-pin-check.py:140-150`" (`.ufo/waves/round-58/contract.md:65`). |
| 2 | Follow unfixed critic flags forward — carry-over ledger (`:51-53`) | **STILL UNIMPLEMENTED as a ledger** | One-round snapshot exists: `.ufo/waves/round-49/flagged-fixed/count-flagged.py` + `defects.jsonl` (r48: `flagged=45 fixed=18 unfixed=9 na=18`; `corpus/lessons/round-49.md:211`). QUALITY **153** ("An unfixed critic flag is carried by round-qualified id into the next round's ledger") landed r56 (`corpus/lessons/round-56.md:76-78`) but self-reports the mechanism absent: the r49 tool "reads one `defects.jsonl`… the nine UNFIXED rows it prints for round 48 are named nowhere in rounds 49-56"; at `8be2717b` every unfixed id prints `later=0` (`QUALITY.md:1522-1544`). `corpus/lessons/round-57.md:49`: "suggestion 2's carry-over ledger remains planned." Only per-round exercises exist: r53 `Mo53ExecConsiderthese.md` inventory of r52 flags (13 fixed / 18 routed / 30 dropped; `corpus/lessons/round-53.md:225-235`). Round-58 lesson status line: "suggestion 2 … remain[s] unimplemented" (`corpus/lessons/round-58.md:26`). No `flagged-fixed/` dir exists under rounds 50–58 (`find .ufo/waves -name '*flagged*'` → round-49 only). |
| 3 | Re-execute what closures only evidence-verified (`:54-56`) | **IMPLEMENTED as recurring practice** (r50, r52, r54), though as a one-seat-per-round exercise, not a durable tool | r50: three executor seats re-ran r47/r48/r49 frozen counters at scored revisions — all AGREE (`corpus/lessons/round-50.md:137-144`; reports `a2w1/Mo50bExecReexecR47/R48/R49.md`). QUALITY **136** codifies it: "The round after a closure re-executes that closure's frozen counter at the revision the closure scored, and reports a divergence instead of smoothing it" (`QUALITY.md:1223-1250`). Recurred per contract: r52 (`round-52/contract.md:99`), r54 (`round-54/contract.md:110`; report `w1/Mo54ExecConsiderthese.md` — all 38+31 selftest lines and both verdict lines token-equal). Caveat: QUALITY 136's divergence arm is "`not yet shown`" and it is "once per round, not per seat" (`QUALITY.md:1241-1250`); the round-58 status line still lists suggestion 3 as unimplemented (`corpus/lessons/round-58.md:26`) — the recurring *mechanism* (a tool/ledger) does not exist. |
| 4 | Keep a suggestion-adoption status line (`:57-59`) | **ADOPTED** (r58) | `corpus/lessons/round-58.md` §Considerthese curation `:26`: "Suggestion 4 … is adopted here as this round's status record". One-time so far — the reflection asks for the line "each day", and no post-10-26 reflection exists; as a per-round lesson line it is now established practice. |

## Still-unimplemented set and nomination

Strictly unimplemented: **suggestion 2** (the durable, id-keyed carry-over flag
ledger across rounds). Suggestion 3 is a weaker candidate — the practice recurs
but has no permanent instrument, and QUALITY 136's check is already written.

**Nomination: suggestion 2** — land the carry-over ledger QUALITY 153 specifies:
the nine UNFIXED round-48 ids (`python3 .ufo/waves/round-49/flagged-fixed/count-flagged.py`
prints them) plus each subsequent round's unfixed set, keyed by round-qualified
id (QUALITY 153 shows bare `C2-F1` collides with a different round-17 defect in
134 lines — the round qualifier is required), each with a committed
fixed/routed/dropped disposition checked against the next round's landing diff.
Cheap falsification arm already written in `QUALITY.md:1533-1548`.

Not nominated: suggestion 1 (done); suggestion 3 (substantially done as
practice; a permanent instrument is a real but thinner gap); suggestion 4
(adopted r58 — keep emitting the line per round rather than re-adopting it).

## Files opened / commands run (all read-only)

- `considerthese/2026-10-26.md` (full); `ls considerthese/`; `git log --all -- considerthese/`
- `.ufo/waves/round-59/contract.md` (full); `count-c1.py`, `count-c2.py` (frozen, headers + key lines)
- `tools/mori-pin-check.py` (docstring :127-150, summary :884-892, selftest arms :1473-1527)
- `tools/mori-routed-check.py` docstring :1-63 (checked as possible ledger home — it is r23-specific)
- `corpus/QUALITY.md` rows 136 (:1223-1250), 139 (:1284-1286), 153 (:1522-1548)
- `corpus/lessons/round-49.md:148-152,210-212`; `round-50.md:136-145`; `round-51.md:56-60`;
  `round-53.md:222-235`; `round-55.md:105-108`; `round-56.md:76-90`; `round-57.md:48-50`; `round-58.md:20-30`
- `find .ufo/waves -name 'count-flagged*' -o -name '*flagged*'`; `ls .ufo/waves/round-5{0..8}/`
- `grep -rn 'considerthese' .ufo/waves/round-5*/contract.md`
- `.ufo/waves/round-54/w1/Mo54ExecConsiderthese.md` (head :1-60)
- `/home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status` → green

## Limits / unknowns

- I did not re-run `count-flagged.py` (it is read-only per its docstring claim,
  but running it was unnecessary — QUALITY 153's quoted output and the r57/r58
  lesson lines already fix the status).
- "Unimplemented" is judged against committed lane bytes at `8ff344ff`; a seat
  report drafted-but-unmerged inside the current wave is not visible.
- Whether suggestion 4's status line should recur in the round-59 lesson is the
  L1's call, not a gap.
