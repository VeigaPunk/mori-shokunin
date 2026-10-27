# Mo54RevenD2 — how the round-53 SCORECARD C1/C2 rows came to cite the at-salvage receipts

Lane `mori-shokunin`, round 54 wave w1, reconstruction seat (leaf; no subagents). Everything below is read-only
`git show` / `git log` / `git diff` / file reads plus the round-54 check run against the lane as a read-only repo;
the only repository I wrote to is a throwaway fixture under `/fast/scratch/hyaku/mori-r54/Mo54RevenD2/fixture`
(removed at the end). No counter, predicate, control or kill rule is proposed for change.

Question: reconstruct how the round-53 `SCORECARD.md` C1/C2 rows came to cite the at-salvage receipts
(R = `0df80303`) while the round-53 report measures `0b36d23e`; the order of the salvage, SCORECARD and receipts
commits; the check that would have caught it; and whether the same pattern exists in an earlier round's rows.

## 1. The invariant, reconstructed

Three rules bear on a claim row's After cell; at round-53 time only two of them existed, and none of them named the
stage the cell must cite:

1. `.ufo/waves/round-53/contract.md:43,49,85,90` — the *counter* must read `C1=met` / `C2=met` **at the landed tip**
   (the kill rules: "`C1=unmet` (or exit 2) at the landed tip → C1 not verified", "`C2=unmet` at the landed tip →
   C2 not verified"). This binds the measurement, not the citation.
2. `corpus/QUALITY.md:1434-1460` (QUALITY 146, added round 53) — "A SCORECARD row's numbers are the numbers of the
   receipt it cites", with a check that compares each primer key of the row against the `^C1=`/`^C2=` line of the
   receipt the cell names. It constrains row-vs-receipt, and is silent about *which* receipt.
3. `corpus/QUALITY.md:1479-1493` (QUALITY 148, **round 54**, working tree only) — "A SCORECARD claim row cites the
   receipt measured at the landed revision, never an intermediate one". This is the rule the round-53 rows break; it
   did not exist when they were written.

So the invariant that was broken is rule 3; the two rules in force at round 53 do not imply it, and rule 2 in fact
*certifies* the broken rows (§4).

## 2. Timeline (topology is authoritative; both dates are shown because they differ)

Author date ≠ committer date for every commit in the chain, and the committer date of each commit equals the author
date of the next one — the landing order below is the parent chain, read from `git log --first-parent`.

| rev | author date | committer date | parent | what landed |
|---|---|---|---|---|
| `2a4213bf` | 2026-10-26 22:31:29 | 22:37:16 | (freeze `f4da3fd4`) | data: v7.3 ledger, tool + fixtures, S502–S513 |
| `95cf78ee` | 22:37:16 | 22:41:08 | `2a4213bf` | w1 spec + dispatch + **at-data receipts** (`c1-at-data.txt`, `c2-at-data.txt`) |
| `fd86307a` | 22:41:08 | 23:28:22 | `95cf78ee` | post-wave data corrections |
| `0df80303` | 2026-10-26 23:28:22 | 2026-10-27 00:15:36 | `fd86307a` | **orchestrator salvage** of unlanded attempt-1 w1 state (66 seat reports, `w1-results.json`, drafts), incl. `w1/Mo53ScribeScorecard.md` and `w1/Mo53ScribeQuality.md` |
| `34d97cd3` | 2026-10-27 00:15:36 | 00:22:20 | `0df80303` | attempt 2: **SCORECARD round-53 section** (and round-52 correction) + **at-salvage receipts** (`c1-at-salvage.txt`, `c2-at-salvage.txt`, file mtime/header `00:20:50`) |
| `7b90a3c6` | 00:22:20 | 00:41:20 | `34d97cd3` | a2r1 dispatch + 7 reports; LOG/PROVINCE/SKILL/lesson corrections |
| `0b36d23e` | 00:41:20 | 00:55:26 | `7b90a3c6` | **a2r1 settled** — the round's measured revision; at-landed receipts do **not** exist here |
| `28401324` | 00:55:26 | 00:57:23 | `0b36d23e` | **receipts at `0b36d23e`**: `c1-at-landed.txt`, `c2-at-landed.txt`, `census-end.txt`, `pin-check-at-landed.txt` (receipt headers `00:55:37`) |
| `39dcf4d7` | 00:57:23 | 01:10:36 | `28401324` | round-53 verifier spot-check; finds the mismatch as D2 |

Order asked for: **salvage (`0df80303`) → SCORECARD section + at-salvage receipts (`34d97cd3`) → residual wave
(`7b90a3c6`) → measured tip (`0b36d23e`) → at-landed receipts (`28401324`) → spot-check (`39dcf4d7`)**. The
SCORECARD cells were written *three commits before* the receipt stage they are judged against existed.

Round-50 analogue, same shape one wave earlier:
`487941b9` (data, 09:05:32) → `4548a34d` (at-data receipts `a2-c1-at-data.txt`/`a2-c2-at-data.txt`, 09:27:40) →
`bae8656e` (**SCORECARD round-50 section**, 09:31:37) → `756d5b1a` (**at-landed receipts** `a2-c1-at-landed.txt`/
`a2-c2-at-landed.txt` at `bae8656e`, 10:52:00).

## 3. Mechanism — how the cells came to cite at-salvage (evidence chain)

1. **The wave draft asked for the landed receipt.** `.ufo/waves/round-53/w1/Mo53ScribeScorecard.md:94` (landed in the
   salvage `0df80303`): the C1 After cell is the placeholder
   `[L1 fills — paste evidence/c1-at-landed.txt verbatim; target tokens C1=met scope=46 ro…]`; `:95` likewise for C2
   with `evidence/c2-at-landed.txt` and target tokens `C2=met tool=present selftest=pass n≥12 …`. The intended stage
   was the landed one.
2. **Attempt 1 died before that receipt existed** (session exit 2026-10-26 23:57:36 -03; `LOG.md:2880`,
   `corpus/lessons/round-53.md:265-267`). The salvage carried the votes (`w1-results.json`, 66 recovered reports) and
   the draft, no at-landed receipt.
3. **Attempt 2 re-measured at the only available tip** — the salvage — at `00:20:50`
   (`.ufo/waves/round-53/evidence/c1-at-salvage.txt:1-3`, `c2-at-salvage.txt:1-3`), and filled the draft's
   placeholders with **those** numbers. `corpus/lessons/round-53.md:282-283` states the choice and its rule:
   "After cells from the at-salvage receipts so that each row's numbers are those of the receipt it cites
   — QUALITY 146". The C1 cell's tail (`SCORECARD.md:2796`) is `(R = \`0df80303\`; the at-landed re-run is named in
   the round-53 report)`; the C2 cell (`:2797`) is the same plus the draft's data-commit aside `n=23` →
   `evidence/c2-at-data.txt`.
4. **The tip then moved.** The a2r1 residual call landed (`7b90a3c6`, `0b36d23e`), so the round's measured revision
   became `0b36d23e` — the fleet report says so verbatim: `.ufo/reports/round-53/mori.md:6-8` "measured revision
   (final integration tip) `0b36d23e596276c70725873621fe15a28c87189f`; final lane tip `28401324 …`", and its After
   measurements cite `evidence/c1-at-landed.txt` / `c2-at-landed.txt` (report `:79-86`).
5. **The at-landed receipts landed after the cells**, in `28401324` (verified: `git ls-tree` at `0b36d23e` lists only
   the at-salvage receipts; `28401324` adds the at-landed pair). Nobody re-pointed the cells; only the LOG was
   reworded (`LOG.md:2860-2861`, at `34d97cd3` it read "the landed receipts `evidence/c1-at-landed.txt`,
   `evidence/c2-at-landed.txt`", reworded at `7b90a3c6` to name the at-salvage receipts *and* the at-landed re-run).
6. **Nothing re-read the cells afterwards.** The residual reviewer that looked exactly at these cells,
   `.ufo/waves/round-53/a2r1/Mo53a2RevScorecard.md`, wrote: "Round-53 after cells match the salvage receipts: C1
   `held=44 … voted=46 dissent=0` (`evidence/c1-at-salvage.txt`); C2 `n=31 …` (`evidence/c2-at-salvage.txt`)" and
   returned "No MED/HIGH findings". It verified cell-vs-cited-receipt (QUALITY 146's arm) at `34d97cd3` — where the
   at-landed receipt did not exist, so there was nothing to compare against.

**Consequence of the mechanism:** the fix for round-52's mistake (row carried at-data digits while citing the landed
receipt — `corpus/lessons/round-53.md:80-86`, QUALITY 146) was to move the *citation to the receipt whose digits were
transcribed*. That fix silently traded one stage error for its mirror image: the row now cites the receipt it
measured, but a receipt measured at a revision the round does not report. Because the two receipts' verdict lines
are token-identical except `rev=` (§5), every number in the cells stayed true, so nothing downstream reacted.

## 4. Why the rules in force certified the row

`QUALITY 146`'s check takes the receipt named last in the cell and compares keys: for `SCORECARD.md:2796` the cited
receipt is `c1-at-salvage.txt`, whose line prints `held=44 absent=2 holds=46 changed=0 voted=46 dissent=0` — the row's
own numbers. The check reads **ok**; it cannot read "wrong stage" because it has no notion of stage. QUALITY 148's
own text records this: "QUALITY 146 did not fire because the numbers matched" (`corpus/QUALITY.md:1483`).

## 5. The verdicts are stage-invariant (verified, not assumed)

Stripping `rev=` from the `C1=`/`C2=` lines makes the at-salvage and at-landed receipts identical:

```
$ diff <(sed 's/ rev=[0-9a-f]*//' .ufo/waves/round-53/evidence/c1-at-salvage.txt) \
       <(sed 's/ rev=[0-9a-f]*//' .ufo/waves/round-53/evidence/c1-at-landed.txt)
1,2c1,2
< # attempt 2 (L1 MoriR53a2), at the salvage tip 0df80303…, 2026-10-27T00:20:50-03:00
< $ python3 .ufo/waves/round-53/count-c1.py 0df80303…
> # attempt 2 (L1 MoriR53a2), at the final integration tip 0b36d23e…, 2026-10-27T00:55:37-03:00
> $ python3 .ufo/waves/round-53/count-c1.py 0b36d23e…
c1 diff rc=1   # the only differing lines are the header/time and the command line
```

Per-verdict comparison (`C1=`/`C2=` lines only, `rev=` stripped): **c1 identical, c2 identical**. Same for round 50
(`a2-c1-at-data` vs `a2-c1-at-landed`: `C1=met items=8 axes=6 pins=2 boxes=4 mismatches=0 errors=0 hidden=0
manifest=a94551c5bc8d` both; `a2-c2` likewise). C2 numbers by stage: at-data `n=23`, at-salvage `n=31`, at-landed
`n=31`. So the correction's claim "the verdict lines are token-identical apart from `rev=` … no number in the cells
changes" (`SCORECARD.md:2854-2856`, working tree) holds.

Note for a reader: the After cells carry **no `rev=` token** — the only stage marker in the committed row is the
receipt filename, so a reader who does not open `.ufo/waves/round-53/evidence/` cannot see that the row is measured
at `0df80303`.

## 6. The check that would have caught it

The round-54 instrument `.ufo/waves/round-54/checks/receipt-stage.py` (2891 bytes, untracked in the working tree;
QUALITY 148) is exactly this arm. Run read-only against the lane (`--repo …`, `git show`/`cat-file` only), with
`TMPDIR` in my scratch:

| rev | output tail | exit | what it means |
|---|---|---|---|
| `bae8656e` | `RECEIPT_STAGE rev=bae8656e cited_intermediate=2 flagged=0` | 0 | round-50 section exists, at-landed receipt does not yet — cannot fire |
| `34d97cd3` | 2 FLAGs (round 50 only) | 1 | round-53 cells already wrong, but `c1/c2-at-landed.txt` absent → silent on round 53 |
| `7b90a3c6` | 2 FLAGs (round 50) | 1 | same |
| `0b36d23e` | `cited_intermediate=5 flagged=2` | 1 | same — the measured tip itself does not trip it for round 53 |
| `28401324` | 5 FLAGs: 2668 r50 `a2-c1-at-data`, 2669 r50 `a2-c2-at-data`, 2796 r53 `c1-at-salvage`, 2797 r53 `c2-at-salvage`, 2797 r53 `c2-at-data` | 1 | **first revision that flags round 53** — the commit that lands the at-landed receipts |
| `39dcf4d7` | `cited_intermediate=5 flagged=5` | 1 | (the spot-check revision; the L1's own `evidence/receipt-stage-before.txt` records the same five lines) |
| `756d5b1a` | 2 FLAGs (round 50) | 1 | **first revision that flags round 50** — the commit that lands its at-landed receipts |
| working tree (fixture repo `d1d3c9cd`, SCORECARD + both rounds' receipts copied) | `RECEIPT_STAGE rev=HEAD cited_intermediate=5 flagged=0` | 0 | the two correction paragraphs in the working-tree SCORECARD suppress all five |

Three arms would have caught it, at three different times, and only one of them needs the landed file to exist:

1. **Rev arm (earliest possible, not built):** compare the `rev=` of the receipt the cell names with the
   "measured revision" line of the round's fleet report. At `34d97cd3` the cells name `c1-at-salvage.txt`
   (`rev=0df80303`) and `c2-at-salvage.txt` (`rev=0df80303`); the report (written later) states `0b36d23e`. The arm
   fires at report time, i.e. before the receipts commit, and needs no landed receipt — this is the arm QUALITY 148
   does not have.
2. **Stage arm (what now exists):** QUALITY 148 / `receipt-stage.py`. Fires at `28401324` for round 53 (2 commits
   after the cells landed) and at `756d5b1a` for round 50 (7 rounds before round 54).
3. **Path-existence arm (was available and did run, on the wrong file):** the a2r1 critic `Mo53a2CritDrafts`
   (HIGH×2, `corpus/lessons/round-53.md:294-297`) checked that receipt paths named in the report exist —
   `c1-at-landed.txt`, `c2-at-landed.txt`, `census-end.txt` were all absent at `34d97cd3` (verified:
   `git cat-file -e 34d97cd3:.ufo/waves/round-53/evidence/{c1-at-landed,c2-at-landed,census-end}.txt` → ABSENT ×3).
   It reworded the LOG. The same arm applied to the SCORECARD cells would have passed them, because by then the
   cells had been re-pointed to the at-salvage files, which existed. Existence is not stage.

The non-author closure did catch it by reading, one commit after the receipts landed:
`corpus/lessons/round-53-verifier-spotcheck.md:48-52` D2 — "the round-53 C1 and C2 After cells (`SCORECARD.md:2796-2797`)
cite the at-salvage receipts (R = `0df80303`), not the final integration tip `0b36d23e` that the report measures; the
cells defer to the report for the at-landed re-run. The numbers match the receipt cited (QUALITY 146 holds) … Route:
an appended note naming the at-landed receipts." Captured-by: reading, not an instrument — the same "Captured-by:
none" the round-52 M1 entry records for the mirror-image defect (`corpus/lessons/round-53.md:85`).

## 7. The same pattern in earlier rounds

Direct answer from the requested grep: **exactly one earlier round — round 50, both claim rows.** Enumerating every
claim row's After cell in `SCORECARD.md` at `HEAD` for `evidence/<name>-at-<stage>.txt` gives nine citations over
four rounds; nothing before round 50 uses an `-at-<stage>` name at all:

```
round 50 rows: 2   line 2668  a2-c1-at-data      line 2669  a2-c2-at-data
round 51 rows: 2   line 2716  c1-at-landed       line 2717  c2-at-landed
round 52 rows: 2   line 2746  c1-at-landed       line 2747  c2-at-landed
round 53 rows: 3   line 2796  c1-at-salvage      line 2797  c2-at-salvage, c2-at-data
total rows with -at-<stage> in the After cell: 9
```

Round 50 in full (`SCORECARD.md:2668-2669`, both cells, verbatim tails): "`C1=met items=8 axes=6 pins=2 boxes=4
mismatches=0 errors=0 hidden=0 manifest=a94551c5bc8d rev=487941b9…`, rc 0 — `evidence/a2-c1-at-data.txt`" and
"`C2=met claims=22 … rev=487941b9…`, rc 0 — `evidence/a2-c2-at-data.txt`", while
`.ufo/waves/round-50/evidence/a2-c1-at-landed.txt` and `a2-c2-at-landed.txt` (R = `bae8656e`, the round-50 measured
tip) sit beside them. Same shape: section written at `bae8656e`, landed receipt added at `756d5b1a`, cells never
re-pointed; it stayed live for seven rounds (`756d5b1a` → `2d0347a3`) with no flag. Rounds 51 and 52 cite the landed
stage and are clean.

Adjacent naming that the stage check does not classify (from the scan of all After cells; these are **not** the same
class, stated as checked rather than assumed):

- Round 36 (`SCORECARD.md:2021-2022`) cites `evidence/c1-after.txt`/`c2-after.txt` (added `9ca8f2eb`) while
  `evidence/c1-after-final.txt` exists (added `5a2fe05d`, "close-out receipts — census-end, C1/C2 final-tip
  re-scores"). Different command, not a later stage of the cited one: `c1-after-final.txt` is the `P-C1` receipt of
  `tools/mori-source-drift.py` (`blind_rows=40 … real_rows=220 … seed=15951461284190234552`), while the row cites
  `count-c1.py bf0df77` (`seed=7388485190103051243`). No stage swap.
- Round 37 (`SCORECARD.md` round-37 section) cites both stages openly: rows at the section's first table cite
  `c1-after.txt`/`c2-after.txt` (`bcf65505`, counter v1 at `e57c58b5`) and appended rows cite
  `evidence/c1-after-v2.txt` / `c2-after-v3.txt` (`4bfa0490`, counter v2/v3, amended counters A1–A3). Both citations
  and both counter versions are present in the row set, so this is an append-only re-score, not a silent swap.
- Round 42 cites `c1-after.txt`/`c2-after.txt`/`c3-after.txt`; no second stage exists in
  `.ufo/waves/round-42/evidence/`.

## 8. Divergences and confidence

- The round-53 SCORECARD section was authored in attempt 2, not attempt 1: the message of `34d97cd3` and
  `git show 0df80303:SCORECARD.md` (the salvage tree carries the round-52 section only in its pre-correction form)
  agree; the *draft* for it came out of the salvage (`w1/Mo53ScribeScorecard.md`). [OBSERVED]
- Sub-minute ordering inside `34d97cd3` cannot be recovered: the commit's author date (`00:15:36`) precedes the
  at-salvage receipts' header/mtime (`00:20:50`), which precedes its committer date (`00:22:20`). Whether an earlier
  at-salvage receipt existed when the cell text was typed is **[INFERENCE]** — unresolved, and immaterial to the
  finding, because the landed commit content is what the cells cite and what the check reads.
- The claim that the cells' digits are the at-salvage receipts' digits is [OBSERVED] (C1 `held=44 absent=2 holds=46
  changed=0 voted=46 dissent=0`, C2 `n=31 fixtures=80 agree=80 disagree=0`), not [INFERENCE].
- I did not run either frozen counter (not my seat, and no change to adjudicate); every verdict string above is read
  from the committed receipts.

## 9. Named limits of the check that now exists (routed material, not a fix request)

From `receipt-stage.py` itself plus the run table in §6:

1. **Existence-gated** — it can only fire once the `<x>-at-landed.txt` file exists in that round's evidence dir
   (`cat-file -e` guard, `receipt-stage.py:58-64`). It was silent on round 53 at `34d97cd3`, `7b90a3c6` and the
   measured tip `0b36d23e`; a rev arm (§6.1) would not be.
2. **Over-flags deliberate comparison citations** — the round-53 C2 cell's `evidence/c2-at-data.txt` mention is an
   explicit attribution of `n=23` to the data commit, not a citation of the row's measurement, yet it is flagged
   (line 2797, third of the five). The FLAG text cannot distinguish the two.
3. **Naming-bound** — `evidence/<name>-at-(data|salvage).txt` only; `-after`/`-after-tip`/`-after-v2` naming
   (rounds 36/37) and any future style are invisible (its own "Not covered" clause says so).
4. **Correction matched by name, not content** — any later paragraph opening `**Round-N correction:**` that mentions
   `<x>-at-landed` suppresses the flag (`receipt-stage.py:65-68`); the working-tree run (§6, last row) shows all five
   flags cleared by two paragraphs, with no check that the paragraphs are true.
5. **No cell/rev linkage** — the check never compares the cited receipt's `rev=` with the report's measured revision,
   which is the invariant the rows actually break.

## Findings

- **MED — `SCORECARD.md:2796-2797` (committed at `HEAD`/`2d0347a3`; corrected only in the working tree at
  `SCORECARD.md:2850-2856`)**: the round-53 C1 and C2 After cells cite `evidence/c1-at-salvage.txt` /
  `evidence/c2-at-salvage.txt` (R = `0df80303`) while the round reports and measures `0b36d23e`; the committed row
  names a revision the round does not report. Verdict unaffected (verdict lines token-identical apart from `rev=`,
  §5).
- **MED — `SCORECARD.md:2796-2797` + `corpus/QUALITY.md:1434-1460`**: the mechanism is the round-53 QUALITY 146 fix —
  pointing each cell at the receipt whose digits were transcribed. QUALITY 146's own check therefore reads `ok` on
  the wrong-stage row, and the residual reviewer `Mo53a2RevScorecard` certified it ("no MED/HIGH findings"). A
  number-fidelity rule is not a stage rule; the stage rule arrived one round later (QUALITY 148) and no rule required
  re-pointing the cell when the measured tip moved.
- **MED — `SCORECARD.md:2668-2669` (round 50)**: the identical pattern, seven rounds earlier (`a2-c1-at-data` /
  `a2-c2-at-data` cited beside existing `a2-c1-at-landed.txt` / `a2-c2-at-landed.txt`, R = `bae8656e`); first
  detectable by the round-54 instrument at `756d5b1a` and undetected from then until round 54. It is the only earlier
  round with the pattern; rounds 51/52 cite the landed stage, and no round before 50 uses an `-at-<stage>` citation
  at all.
- **LOW — `.ufo/waves/round-54/checks/receipt-stage.py:58-64`**: existence-gated, so on the round that produced the
  defect it is silent at the section commit, the residual commit and the measured tip; it first fires at the receipts
  commit (`flagged=5` at `28401324`). The missing arm is a `rev=` comparison against the report's measured revision,
  which has no existence precondition.
- **LOW — `.ufo/waves/round-54/checks/receipt-stage.py:57`**: flags the round-53 C2 cell's `c2-at-data` mention,
  which the cell explicitly attributes to the data commit (`n=23`); the flag text cannot separate a comparison
  citation from a measurement citation.
- **LOW — `LOG.md:2860-2862` at `34d97cd3`**: the round-53 report carried forward pointers to
  `c1-at-landed.txt`, `c2-at-landed.txt` and `census-end.txt`, none of which existed at that commit (verified absent by
  `git cat-file -e`). The a2r1 critic caught this (HIGH×2) and reworded the LOG, but the same forward-pointer class in
  the SCORECARD cells was not re-examined after `28401324` landed the files — that is the gap between "the pointer
  resolves" and "the pointer names the right stage".
- **LOW — `SCORECARD.md:2850-2863` (working tree, uncommitted)**: both correction paragraphs cite
  `corpus/lessons/round-54.md`, which does not exist in the tree (`ls corpus/lessons/` ends at
  `round-53-verifier-spotcheck.md`). Draft-state dangling pointer for the L1's integration, not a shipped defect.

Scratch `/fast/scratch/hyaku/mori-r54/Mo54RevenD2/` (including the fixture repo `d1d3c9cd`, whose
`git rev-parse --show-toplevel` printed `/fast/scratch/hyaku/mori-r54/Mo54RevenD2/fixture` before its single commit)
was removed at the end of this seat. No tool was installed or upgraded (none needed); no pacman transaction was run;
no kernel log line was counted. Nothing was written outside this report file and that scratch dir.
