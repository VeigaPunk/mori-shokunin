# Round 25 wave 2 — MutRoutedD2 (mutation probe of claim C1, item D2)

Seat: `MoriR25.MutRoutedD2` (mutation-tester, leaf). Target: `tools/mori-routed-r24.py`, item **D2**
("incomplete correction sweep in `corpus/knowledge/system-pressure-r24.md`").
Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin` (read-only; only this report was written there).
Private clone: `/fast/scratch/hyaku/mori-r25/w2-MutRoutedD2` (301 MB, `git clone --no-hardlinks`).
All code ran in the private clone; the lane checkout was never executed against, never written.

## Verdict — WEAKENED

The **tool** holds up: every D2 guard I removed flips the D2 verdict on at least one sandbox commit,
with one exception (the decision-table *heading* guard), which turns out to be verdict-redundant.

What is weakened is **the evidence behind C1**, not the tool. The C1 evidence wave 1 declared —
"mismatches 4 at `28b79d3d` → mismatches 0, held 4/4, hygiene held, exit 0 at the tip"
(`.ufo/waves/round-25/evidence/routed-r24-before-a5.txt`, `routed-r24-after-a5.txt`) — **cannot
discriminate the mutants at the verdict level**: all 14 mutants reproduce "mismatches 4, held 0, exit 1"
at the before revision, and 12 of 14 reproduce "mismatches 0, held 4/4, exit 0" at the tip. The two that
are discriminated at the tip are the ones that break the case fold, and they are discriminated in the
*strict* direction only (the mutant turns a held entry red).

So the declared C1 measurement demonstrates that the D2 predicates do not fire — it cannot show that
they would fire on a broken entry, because it only ever runs the checker on entries that satisfy D2.
Severity **medium**: at the verdict level the calibration claim is not falsifiable from its own evidence.

One mutant **survived** the whole corpus: **M3c** (the `decision_table_heading_missing` guard). Details
and the input that kills it are in §5.

---

## 1. Method

1. Copy the pristine tool (sha256 `cf5ef5815f1118ae3595171edde7f527176fde03480665eb6bbb46921c2969ef`,
   36313 bytes) and generate 14 mutants, each weakening exactly one D2 predicate. Every edit is asserted
   to apply exactly once, so a drifted source fails loudly instead of producing a silent no-op
   (`/fast/scratch/hyaku/mori-r25/mutants/make_mutants.py`).
2. Build a sandbox corpus of 20 commits in the private clone. Each commit edits **only**
   `corpus/knowledge/system-pressure-r24.md`, and each reverts exactly one round-25 fix (or is a green
   control). D1, D3, D5 and the D4 hygiene row keep holding on every case, so any verdict change is
   attributable to D2 alone.
3. Expected labels are written **by hand** from the contract's D2 predicate, not read back from the tool.
4. Run every tool variant (pristine + 14 mutants) over every case:
   `python3 -I -B <variant> --repo <clone> --rev <case-sha>`.
5. A mutant is **KILLED** when its D2 verdict differs from the pristine tool's D2 verdict on at least one
   case; otherwise it **SURVIVED** the corpus. A kill in the *lax* direction (pristine red, mutant
   green) is a false negative — the dangerous direction — and is reported separately from a kill in the
   *strict* direction (pristine green, mutant red = false positive).
6. Restore: clone checked out back at the tip, `refs/replace/` probe removed, file hashes identical
   (§7).

Scripts and raw results (kept, 708 KB): `/fast/scratch/hyaku/mori-r25/mutants/`
(`make_mutants.py`, `build_corpus.py`, `run_matrix.py`, `tip_only.py`, `identical_payloads.py`, `m3c_probe.py`,
`corpus.json`, `matrix.json`, `tip_only.json`, `identical_payloads.json`, `m3c_probe.json`).
Rebuild the corpus after deleting the clone:
`git clone --no-hardlinks /home/vgpnk/Projects/shokunin/mori-shokunin /fast/scratch/hyaku/mori-r25/w2-MutRoutedD2 && python3 /fast/scratch/hyaku/mori-r25/mutants/build_corpus.py && python3 /fast/scratch/hyaku/mori-r25/mutants/run_matrix.py`.

## 2. The mutants (all at `tools/mori-routed-r24.py`)

| Id | Mutant | Line in the pristine tool | What it weakens | sha256 (first 12) |
|---|---|---|---|---|
| M1a | `_normalize` → identity (no markers, no case fold, no whitespace fold) | `tools/mori-routed-r24.py:307-312` | all of D2's normalization | `0d3abbd3cbb0` |
| M1b | `_normalize` without `text.casefold()` | `:311` | case-insensitive matching | `65abd2516c3c` |
| M1c | `_normalize` without the `MARKER_CHARS` loop | `:309-310` | emphasis-marker stripping | `09d0e6c53070` |
| M1d | `_normalize` without the whitespace-run fold | `:312` | whitespace folding | `28b407a0fec4` |
| M2 | positive-anchor loop deleted (`D2_POSITIVE_PHRASES`) | `:600-602` | "only when the next", "not tracked" must appear | `3a6863714018` |
| M3a | corrections-heading-count guard deleted | `:558-559` | exactly one `## corrections` | `516b501d230d` |
| M3b | facts-heading guard deleted | `:560-561` | `## facts` present | `e8eed6bea55d` |
| M3c | decision-table-heading guard deleted | `:562-563` | `## decision table` present | `3b4a14be8821` |
| M3 | all three heading guards deleted | `:558-563` | as M3a+M3b+M3c | `71ba9c36a8a2` |
| M4 | decision-table row-count guard deleted | `:581-582` | table rows ≥ rows at `28b79d3d` | `4633da6ee8ff` |
| M5 | banner gate narrowed to `outside_text` (the pre-A3 form) | `:609` | "this section wins" absent from the **whole** entry | `ab7969442c56` |
| M6 | the `(k4)`+`total` line check deleted | `:613-617` | the K4 bullet must exist inside Corrections | `41a921e8e176` |
| M7 | whole-entry banner gate deleted outright | `:609-610` | as M5, plus the outside-only form | `1da8656a10b4` |
| M8 | *control*, not in the assigned list: negative-pattern loop deleted | `:597-599` | the three forbidden claims | `84fd877c0af7` |

## 3. The sandbox corpus (20 commits + 1 probe)

Every red case is a one-fix revert of the round-25 D2 patch (`.ufo/waves/round-25/w1/D2KnowledgeFix.md`).
Pristine tool, all cases (`python3 run_matrix.py`): the pristine verdicts match every hand-written
label, and D1/D3/D5/D4 hold on all 20 cases (`exit` is the process exit code).

| Case | What it does | Pristine D2 verdict | Pristine reasons |
|---|---|---|---|
| G0_tip | the landed tip, untouched | held | – |
| R1_duplicate_corrections_heading | a second `## Corrections …` heading | red | `corrections_heading_count_not_one` |
| R2_facts_heading_removed | `## Facts` → `## Factual record` | red | `facts_heading_missing` |
| R3_decision_table_heading_removed | `## Decision table` → `## Decision table of observable states` | red | `decision_table_heading_missing`, `decision_table_rows_fewer_than_base` |
| R4_one_decision_table_row_removed | one data row deleted from the table | red | `decision_table_rows_fewer_than_base` |
| R5_negative_refreshed_on_each_read | "The averages are refreshed on each read." appended (reverts the K5 body fix) | red | `phrase_present_outside_corrections: refreshed on (each\|every) read` |
| R6_negative_spike_invisible | "A shorter spike between two reads can be invisible." appended (reverts the K4 row fix) | red | `phrase_present_outside_corrections: spike[^\|.]{0,60}(is\|are\|can be\|may be) invisible` |
| R7_negative_null_means_undefined | "The \`null\` line means *undefined* …" appended (reverts the P3 row fix) | red | `phrase_present_outside_corrections: null[^\|.]{0,15}means[^\|.]{0,15}undefined` |
| R8_positive_only_when_the_next_missing | "only when the next" → "only once the next" (reverts the K5 body fix) | red | `phrase_missing_outside_corrections: only when the next` |
| R9_positive_not_tracked_missing | "*not tracked*" → "*not measured*" in the decision table (reverts the P3 row fix) | red | `phrase_missing_outside_corrections: not tracked` |
| R10_banner_inside_corrections_section | the "this section wins" banner re-inserted **inside** the Corrections section (reverts the banner deletion) | red | `banner_present_in_entry: this section wins` |
| R11_k4_total_line_removed | the K4 bullet deleted from the Corrections section (reverts the new K4 bullet) | red | `corrections_section_lacks_k4_total_line` |
| R12_negative_capitalised_refreshed | "Refreshed On Each Read." appended | red | `phrase_present_outside_corrections: refreshed on (each\|every) read` |
| R13_negative_double_spaced_refreshed | "refreshed  on  each  read" appended (double spaces) | red | same as R5 |
| R14_lowercase_headings_capitalised_forbidden | the three D2 headings lower-cased + a capitalised forbidden claim | red | same as R5 |
| R15_marker_boundary_null_means_undefined | `null` + 16 underscores + `means undefined` appended | red | same as R7 |
| R16_lowercase_entry_capitalised_forbidden | headings **and** the `(K4)` token lower-cased + a capitalised forbidden claim | red | same as R5 |
| G1_positive_capitalised_not_tracked | "not tracked" → "Not Tracked" (green control) | held | – |
| G2_positive_double_spaced_only_when_the_next | "only  when  the  next" (green control) | held | – |
| G3_facts_heading_marked_up | "## Facts" → "## \`Facts\`" (green control) | held | – |

## 4. Results — every mutant except M3c is killed

| Mutant | Verdict | Killing case(s) | Direction |
|---|---|---|---|
| M1a normalize_identity | KILLED | G0_tip, G1, G2, G3 (strict) and **R16** (lax) | both |
| M1b no casefold | KILLED | G0_tip, G1, G2, G3 (strict) and **R16** (lax) | both |
| M1c no marker removal | KILLED | G3 (strict), **R15** (lax) | both |
| M1d no whitespace fold | KILLED | **R13** (lax), G2 (strict) | both |
| M2 drop positive anchors | KILLED | **R8**, **R9** (both lax) | lax |
| M3 drop all heading guards | KILLED | **R1**, **R2** (lax) | lax |
| M3a drop corrections-count guard | KILLED | **R1** (lax) | lax |
| M3b drop facts guard | KILLED | **R2** (lax) | lax |
| **M3c drop decision-table-heading guard** | **SURVIVED (20/20)** | – | – |
| M4 drop row-count guard | KILLED | **R4** (lax) | lax |
| M5 banner gate → outside-only | KILLED | **R10** (lax) | lax |
| M6 drop (k4)+total check | KILLED | **R11** (lax) | lax |
| M7 drop banner gate | KILLED | **R10** (lax) | lax |
| M8 control: drop negative patterns | KILLED | R5, R6, R7, R12, R13, R14, R15, R16 (all lax) | lax |

Bold = a kill in the **lax** direction: the mutant reports the entry as clean while the pristine tool
reports it red. That is the direction that matters for C1 — a weakened tool would have certified a
broken entry.

Two results worth spelling out:

* **M5 (banner gate narrowed to `outside_text`) is killed only by R10.** The banner sits *inside* the
  Corrections section, so an outside-only gate cannot see it; the wave-1 A3 amendment to gate on the
  whole entry is load-bearing and is now covered by a case.
* **M1b's lax kill needs R16.** With the entry as it stands, the three D2 headings are capitalised, so
  a tool without the case fold fails the *heading* guards first and never reaches the case-sensitive
  forbidden-claim check. R16 lower-cases the headings **and** the `(K4)` token, after which the mutant
  reports the entry clean while the pristine tool reports
  `phrase_present_outside_corrections: refreshed on (each|every) read`. In other words, the case fold
  and the `(k4)` token check are coupled: `D2_CORRECTIONS_TOKEN = "(k4)"` is compared against a
  case-folded line, so the token only matches because of the fold.

## 5. The survivor: M3c (`decision_table_heading_missing`)

**Why it survives.** When the `## decision table` heading is absent, `table_indices` is empty, so
`table_rows` stays 0 (`tools/mori-routed-r24.py:566-570`), and the row-count guard at `:581-582`
(`table_rows < base_rows`, with `base_rows` = 11 at the pinned base `28b79d3d`) fires anyway. The
missing heading is therefore reported twice, and the verdict is red whether or not the heading guard
exists. On R3 the pristine tool prints both reasons and M3c prints only
`decision_table_rows_fewer_than_base` — the *reason* differs, the *verdict* does not, so C1's declared
verdict (`held`/`mismatches`/exit) cannot tell them apart.

**The input that kills it.** The heading guard becomes load-bearing as soon as the pinned base's
decision table has zero data rows, because then the row-count guard cannot fire
(`table_rows < base_rows` is `0 < 0` = false). Probe (`/fast/scratch/hyaku/mori-r25/mutants/m3c_probe.py`,
private clone only, base revision shadowed with a `refs/replace/` ref, removed afterwards):

```
replacement commit c11fe61664c0b447803c882ebd47c1f535b588d6 dropped base table rows: 13
case commit c8f6f766d361d3578d5b6b9f61277b32b3cab0b5
pristine  {"base_rows": 0, "d2_held": false, "d2_reasons": ["decision_table_heading_missing"], "exit": 1, "rows": 0, "status": "failed"}
M3c       {"base_rows": 0, "d2_held": true,  "d2_reasons": [],                          "exit": 0, "rows": 0, "status": "held"}
M3_all    {"base_rows": 0, "d2_held": true,  "d2_reasons": [],                          "exit": 0, "rows": 0, "status": "held"}
M3c verdict-level killed on this input: True
```

So M3c is killed by: *a repository whose pinned base revision `28b79d3d` carries a decision table with
zero data rows, plus an entry at the revision under test whose `## Decision table` heading is missing.*
In every other repository the guard is dead weight — its red verdict is always produced by the
row-count guard instead.

**Smallest fix** (one line, `tools/mori-routed-r24.py:581`): make the row-count guard fire only when
the table heading is present, so the two checks are independent and the heading guard is not
subsumed:

```python
    if table_indices and base_rows is not None and table_rows < base_rows:
        reasons.append("decision_table_rows_fewer_than_base")
```

With that change R3 is caught by `decision_table_heading_missing` alone and R4 is still caught by the
row-count guard. (The alternative — deleting the heading guard at `:562-563` — loses a real signal
when the base table is empty, so it is the worse of the two.)

## 6. Coverage findings

### F1 — the C1 evidence cannot falsify any D2 predicate (severity: medium)

The declared C1 measurement runs the checker on one good entry (the tip) and one bad one
(`28b79d3d`), and its evidence files embed the tool's **entire** JSON payload
(`.ufo/waves/round-25/evidence/routed-r24-before-a5.txt:5`, `routed-r24-after-a5.txt:5`). Both levels
were measured (`/fast/scratch/hyaku/mori-r25/mutants/identical_payloads.json`,
`python3 identical_payloads.py`):

| Declared revision | Claim C1 states | Mutants with the **same verdict** (`held`/`mismatches`/exit) | Mutants with a **byte-identical JSON payload** |
|---|---|---|---|
| `28b79d3d` ("before") | `mismatches 4, held 0, exit 1` | **14 of 14** | **7 of 14** (M1c, M1d, M3, M3a, M3b, M3c, M4) |
| `07a31ae` ("after", the tip) | `mismatches 0, held 4/4, exit 0` | **12 of 14** (all but M1a, M1b) | **12 of 14** (the same 12) |

Reading: the *verdict* C1 claims cannot tell any mutant from the pristine tool at the "before"
revision, and cannot tell 12 of 14 from it at the tip — the two it does catch (M1a, M1b, the case-fold
mutants) are caught in the **strict** direction only (mutant red on a good entry, pristine green). At
the reason level the "before" payload does separate 7 mutants (M1a, M1b, M2, M5, M6, M7, M8 change the
D2 reason list — e.g. pristine lists both `phrase_missing_outside_corrections` reasons and M2 lists
neither), so the evidence is not wholly blind; but the *claim* C1 makes is a verdict claim, and a
verdict-level diff of the two evidence files cannot falsify it.

Concretely: removing the positive anchors, the corrections/facts heading guards, the row-count guard,
the whole-entry banner gate, the `(k4)`+`total` check or the three forbidden-claim patterns changes
**nothing** in the verdict that the declared evidence certifies. A future round that breaks any of
those gates would still certify "mismatches 0, held 4/4, exit 0" on the tip, and "mismatches 4, held 0"
at the base.

*Smallest fix:* give the routed checker a committed case corpus in the same shape C2 already has
(`tools/fixtures/mori-job-runway/cases.json`), i.e. one red case per D2 predicate and one green case,
and make the C1 evidence include a run over that corpus — not only a run at the tip. Until that
exists, "held 4/4 at the tip" is a statement about the entry, not about the checker.

### F2 — the `## decision table` heading guard is verdict-redundant (severity: low)

M3c survived 20/20 corpus cases (§5). *Smallest fix:* the one-line change at `:581` given in §5.

### F3 — two halves of the normalization are pinned by one case each (severity: low, informational)

* The case fold is only observable in the lax direction on an all-lowercase entry (R16); on the entry
  as it stands it is masked by the capitalised headings. If a future edit lower-cases the headings,
  the case fold becomes the only thing standing between a capitalised forbidden claim and a green
  verdict. *Smallest fix:* keep R14/R16 in the corpus (no tool change needed).
* The marker-removal half is observable in the strict direction on natural input only (G3,
  "## \`Facts\`"); a lax kill needs the adversarial distance-boundary case R15 (16 underscores between
  `null` and `means`, i.e. one character over the `[^|.]{0,15}` bound). *Smallest fix:* keep R15 in
  the corpus.

Neither F3 item is a defect of the tool; both are corpus requirements, and neither is met by the
declared C1 evidence.

## 7. Restoration evidence

The lane was never executed against and never written. Its tracked bytes are unchanged:

```
$ git -C /home/vgpnk/Projects/shokunin/mori-shokunin status --porcelain
 M .ufo/waves/round-25/w2/MutRunwayA2Forms.md          <- another seat's edit, not mine
 M .ufo/waves/round-25/w2/MutRunwayFloor.md             <- another seat's edit, not mine
?? .scratch/
?? .ufo/waves/round-25/w2/CriticHarmAxes.md             <- another seat's report
?? .ufo/waves/round-25/w2/MutRoutedD2.md                <- this report (mine)
?? .ufo/waves/round-25/w2/MutRoutedD3D5.md              <- sibling seat's report
?? .ufo/waves/round-25/w2/ReopenBinaryRow.md            <- another seat's report
   -- the only file this seat wrote in the lane is .ufo/waves/round-25/w2/MutRoutedD2.md.

$ sha256sum tools/mori-routed-r24.py corpus/knowledge/system-pressure-r24.md   # lane
cf5ef5815f1118ae3595171edde7f527176fde03480665eb6bbb46921c2969ef  tools/mori-routed-r24.py
03940cbf6e6bba9c592ebc549cbceda351108c37ccd7b7bc47093d32c837b833  corpus/knowledge/system-pressure-r24.md
```

The private clone is back at the tip with identical bytes and no probe residue:

```
$ git -C /fast/scratch/hyaku/mori-r25/w2-MutRoutedD2 status --porcelain   # (empty)
$ git -C … rev-parse HEAD
07a31ae8e22514bbc603afa13f2de7c8b2424cca
$ git -C … replace -l                                                    # (empty)
$ sha256sum tools/mori-routed-r24.py corpus/knowledge/system-pressure-r24.md   # clone
cf5ef5815f1118ae3595171edde7f527176fde03480665eb6bbb46921c2969ef  tools/mori-routed-r24.py
03940cbf6e6bba9c592ebc549cbceda351108c37ccd7b7bc47093d32c837b833  corpus/knowledge/system-pressure-r24.md
```

Before/after hashes: the tool file is byte-identical to the pristine copy
(`cf5ef581…` before and after; `pristine.py` in the mutants directory is the same hash), and the
knowledge entry is byte-identical to the tip's blob (`03940cbf…`). The corpus commits live only on
`case/*` branches in the private clone; they are not in the lane and are not proposed for it.

## 8. Tooling

No tool was installed or upgraded: `python3` 3.14.8 and `git` 2.56.0 were already present and
sufficient (stdlib only, `python3 -I -B`). No `pacman` transaction was attempted (host-wide pacman
pause). No `jj` command was run at the fleet root or in the lane. No `git` write was performed in the
lane; all writes were in `/fast/scratch/hyaku/mori-r25/`.

## 9. Limits / not done

* Only D2 was attacked. D1, D3, D5 and the D4 hygiene row were used as invariants (they held on every
  case) and were not mutated; a sibling seat covers D3/D5.
* The mutants are code changes to the checker, not to the entry. The corpus commits change the entry
  only, so the results say nothing about whether the round-25 entry text is correct — only about
  whether the checker can tell a correct entry from an unfixed one.
* The corpus is a set of hand-built cases, not a random sample: "survived" means "no case I built
  distinguishes it", not "undetectable".
* M3c's kill requires a repository whose pinned base table is empty; that state is contrived and does
  not occur in this repo (base rows = 11), which is exactly why the guard is currently redundant.
* Scratch left in place: `/fast/scratch/hyaku/mori-r25/mutants` (716 KB, the scripts and the raw
  result JSON). The 301 MB private clone was **removed** after the last run
  (`rm -rf /fast/scratch/hyaku/mori-r25/w2-MutRoutedD2`); the rebuild command is in §1.
