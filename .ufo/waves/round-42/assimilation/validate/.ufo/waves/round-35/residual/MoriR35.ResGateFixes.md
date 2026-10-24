measured 2026-10-23T09:33:12Z

# ResGateFixes — re-check of `corpus/lessons/round-35.md` `## Gate` at 6d3d94b3

Seat: MoriR35.ResGateFixes. Object: `corpus/lessons/round-35.md` at
`6d3d94b396698d67555a51c565eb6dc58d8cfa09` (tip under attack; previous tip `cedb0ec4`), read as committed
bytes via `git show` into `/fast/scratch/hyaku/mori-r35/MoriR35.ResGateFixes/` (tip-round35.md, tip-QUALITY.md,
tip-SKILL.md). LSP: no server answers these lane md files; all checks are literal text, not semantic proof.
Read-only lane access; no git writes, no installs, no subagents; every command `timeout 60` and exited.

## Item 1 — QUALITY 86 awk check over tip bytes

Ran the check verbatim from `corpus/QUALITY.md:441` (substituting lane and rev; `round-<N>` = `round-35`):

```
git -C /home/vgpnk/Projects/shokunin/mori-shokunin show 6d3d94b3...:corpus/lessons/round-35.md | awk -F'|' '/^## Gate/{s=1;next} ... END{...}'
gate_reject_rows=2 none_declared=0 malformed=0
exit=0
```

Matches the M5 fix cell's own receipt (`round-35.md:69`). The w2 defect (GateS200 finding 2:
`malformed=2`, exit 1 from `**reject**:` decision cells at `round-35.md:22-23@cedb0ec4`) is repaired:
S203/S204 now read `reject, C: …` / `reject, A for its scope: …` at `round-35.md:22-23` — `^reject, ` with a
non-empty reason, `https?://` source cell, non-empty quote cell.

VERDICT: holds — check prints `gate_reject_rows=2 none_declared=0 malformed=0`, exit 0.

## Item 2 — every quote word-label recounted (whitespace tokens)

Awk split each quote cell on ` — `, stripped the trailing location backtick, whitespace-token count vs `(N)`:

| row | labels | counts | result |
|---|---|---|---|
| S199 | (23), (9) | 23, 9 | OK |
| S200 | (5) | 5 | OK |
| S201 | (3), (3), (5) | 3, 3, 5 | OK |
| S202 | (5), (2), (5) | 5, 2, 5 | OK |
| S203 | (10) | 10 | OK |
| S204 | (16) | 16 | OK |

11/11 labels match. S201's old (4),(4),(6) → (3),(3),(5) fix (GateS201: "whitespace+1 vs whitespace")
is applied at `round-35.md:20`. Verbatim-at-line of each quote was already verified by w2 (GateS200:51,
GateS201:24-27); not re-fetched.

VERDICT: holds — all 11 whitespace-token counts equal their labels.

## Item 3 — sweep list and `Identified 14` vs `.ufo/waves/round-35/w1/SrcDmStack.md`

No-row list at `round-35.md:26-29` names 12 files. Cross-checked each is opened-and-non-stating in SrcDmStack
(this round, sha-pinned): `iostats.rst` (:15-24), `blk-core.c` (:35-44), `dm-linear.c` (:71), `statistics.rst`
(:73), `md.rst` (:72); sysstat `iostat.in` (:45-55), with `iostat.c`, `FAQ.md`, `man/sar.in` and `README.md`
all opened at :53; util-linux `lsblk.8.adoc` (:57-65) and `lsblk.c` (:63). All 12 named in SrcDmStack.

The two ReviewSkillCorr/ReviewLessonCorr omissions (`sysstat/README.md`, `md.rst`) are now named at
`round-35.md:28-29`. `Identified 14 named here (12 without a row, S203 and S204 with one)` (:30) is
arithmetically correct and internally consistent: 12 sweep-named + 2 row files (Disks.html, dm.c, named via
the table) = 14 "named". The three remaining SrcDmStack-opened files — collectl program `collectl`,
`man1/collectl.1`, `docs/WhySummary.html` (:87) — are explicitly acknowledged as also read ("the sweep
also read collectl's program and other collectl docs", :30-31), so the no-row enumeration is now complete
against the sweep's own record. SrcDmStack total opened this round: 17 files (14 named + collectl trio);
`sysfs-block` 404 (:74) and `md.c` prior-round (:75) correctly excluded.

VERDICT: holds — the no-row list covers all 12 non-row opened files; `Identified 14 named here` reconciles
exactly with SrcDmStack's record.

## Item 4 — SKILL.md `fourteen candidate files`

SKILL.md:852-853 at tip: `Round 35 opened fourteen candidate files and none states it; S203 and S204 are kept
as rejected rows`. SrcDmStack records **17** files opened this round, not 14. The L1's fix adopted the
lesson's "named here" count, but SKILL says "opened" without the `named here` scoping — the collectl program,
`man1/collectl.1`, and `docs/WhySummary.html` were fetched and searched as claim candidates at the collectl
site (ReviewSkillCorr:61-65 counts ≥16 opened; direct recount 17 incl. `lsblk.c`, ReviewSkillCorr overlooked
it). No reading of "candidate" yields 14: SrcDmStack's own `### Candidates` heading covers only five files.
Numeric-only defect; "none states it" stays true across all 17.

VERDICT: fails — residual undercount remains in SKILL.md:852-853 (14 claimed vs 17 opened); same numeric
defect repeated at `round-35.md:56` ("fourteen candidate files opened").

## Findings

1. defect (minor, numeric) — `SKILL.md:852-853` and `round-35.md:56`: "fourteen candidate files opened"
   undercounts SrcDmStack's 17 opened files by 3 (collectl `collectl`, `man1/collectl.1`,
   `docs/WhySummary.html`). Honest repair: "seventeen files opened" or the lesson's scoped
   "fourteen named here" phrasing. Substance ("none states it") unaffected.

## Residual risk / gaps

- Quotes' verbatim-at-line rests on w2's fetched-byte verification (GateS200/S201), not re-fetched this seat.
- Only `## Gate` and the named SKILL clause were in scope; the other wave-2 revisions (S182/S193 prose,
  checker/QUALITY-102 rewrite) were not re-judged here.
- Scratch: `/fast/scratch/hyaku/mori-r35/MoriR35.ResGateFixes/` (tip bytes only). No installs; no lane writes
  beyond this report; all supervised commands exited.

VERDICT: holds — QUALITY 86 awk over tip bytes: `gate_reject_rows=2 none_declared=0 malformed=0`, exit 0.
VERDICT: holds — all 11 quote word-labels equal whitespace-token counts.
VERDICT: holds — sweep list + `Identified 14 named here` reconciles with SrcDmStack (12 no-row + 2 rows + 3 collectl extras acknowledged).
VERDICT: fails — SKILL.md:852 `fourteen candidate files opened` (also `round-35.md:56`) still undercounts; 17 opened per SrcDmStack.
