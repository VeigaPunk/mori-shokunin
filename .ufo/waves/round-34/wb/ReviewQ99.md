measured 2026-10-23T07:05:00Z

# ReviewQ99 — QUALITY criterion 99 (attempt-2 draft, uncommitted)

Object: last section of `/fast/scratch/hyaku/mori-r34/a3-L1/drafts/corpus_QUALITY.md` (lines 733-746; identical to lane
working-tree `corpus/QUALITY.md`, `git diff` vs `fd2521351c6cef47384aef30afbe1e4db7e6912e` shows only this +15-line
append). Judged against the lane's QUALITY conventions (criteria 95-98 at :683-731) and the draft lesson.

## Backing (lesson mistake + evidence)

- Backed by a lesson mistake: draft lesson M2 at `drafts/corpus_lessons_round-34.md:79-87` — "round 34's own pre-data
  battery (16 controls, QUALITY 98-shaped) missed a label-keyed, harness-keyed shortcut, which met P-C1-A1 after
  data." Criterion 99 carries `Lesson: corpus/lessons/round-34.md M2` (:742). Same pattern as 95-98 (each cites its
  lesson + a shown-fail). Supported.
- Evidence resolves: `.ufo/waves/round-34/evidence/ctl-postdata-shortcut/receipt.txt:9` prints `C1=met` for probe
  `ef936fb4` under `count-c1-a1.py` (:4-5 command+seed); :3 names exactly what it skips (one real read, rate 0 for
  every device; class from name patterns, never opens partition/slaves/device).
- M2's counter cites verified: `count-c1-a1.py` `def scenario` (:145-166) draws each class from its own name family
  (`DISKS` sample, `part_name` partitions, `dm-i`/`md127-i` stacked, `VIRT` virtual, `xyz9` unknown); the live arm
  rejects only `r * 300 > (s3-s0)*512*1000` (:~277) — an upper bound, so `write_Bps=0` always passes. M2's ":277-278
  (upper bound only)" and ":150-166 (each class drawn from its own name family)" are accurate.

## "Shown able to fail" — true

Check: "the contract's control table names both controls and the receipt scores each `unmet` under the frozen counter
before the first data commit" (:741-742). At `b9fb029e` the contract's Pre-data-controls table has no harness-keyed
control (grep of `b9fb029e:.ufo/waves/round-34/contract.md` for harness-keyed rows: C-emptylive is empty live output
everywhere — it does not detect the harness; C-echo/C-echo-ppid are oracle-import shapes, not harness-keyed). So the
Check fails on that table regardless of how the label-keyed clause is read. TRUE.

Converse: a table naming a control of each kind (i) and (ii), each receipted `unmet` pre-data, passes the Check as
written [INFERENCE: the Check names no other conditions].

## Defects found in 99's wording

D1 (minor, real): clause (i) is ambiguous about input-byte keying. C-labelkey "answers the 12 fixed-seed scenarios from
a table keyed on input bytes" — literally it derives output from the inputs, so a strict reader could call round 34's
table compliant with (i) while missing the generator-label shape ef936fb4 used. The shown-fail sentence takes the
stricter reading but the criterion text doesn't.
Fix: append to (i): "a table keyed only on the fixed input bytes is criterion 98's label-keyed shape and does not
satisfy this clause; the key must be a label the generator emits per scenario".

D2 (minor): the two-sided-bound sentence has no grammatical subject and is not in the mechanical Check — the same
gap MutQ98 showed inside 98 (draft lesson :68-70 records the prose/check split). As written a contract could satisfy
Check (a)-(b) while its counter keeps an upper-only live bound, re-admitting ef936fb4's exact hole.
Fix: give it a subject and put it in the Check: "...only there, doing nothing or returning a constant on the real
input. The frozen counter checks each arm the claim names on the real input with a bound in both directions, so a
constant such as zero cannot meet it. Check: ... (c) the frozen counter's real-input arm rejects a constant output;
(d) `git merge-base --is-ancestor <receipt commit> <first data commit>` holds."

D3 (optional, consistency): 98's Check names the ancestor test explicitly at (c); 99's "before the first data commit"
could do the same — covered by the (d) line above if adopted.

## Adjacent defect (not in 99, reported for L1)

Committed 98's last line (:731) cites "round-34 Mistakes M1" for the rule-order defect; the draft lesson numbers that
mistake **M3** (`drafts/corpus_lessons_round-34.md:88-94`; the draft M1 is the round-33 glossary mistake, :74-78).
Either the lesson keeps M3 and 98's parenthetical must read M3, or the lesson renumbers. Flagged, not counted against
99.

## Overclaim / contradiction vs 98

- 99 does not contradict 98: 98 enumerates eight shapes; 99 adds two controls on top and refines (does not redefine)
  the label-keyed shape. 99's scope qualifier "whose counter runs the deliverable in a harness" is honest narrowing.
- No overclaim: the shown-fail sentence is true (above); the probe description in :745-746 matches receipt.txt:3
  exactly; no unattested numbers.
- Header duplicate: two `## Criteria added round 34` headers now exist (:713 routed-defect-1, :733 mistake-M2). The
  parentheticals differ; consistent with the file's per-mistake section convention (round 32, 33, 34 each add a
  section). Acceptable; optionally merge into one round-34 header with two criteria — cosmetic only.

## Tooling

No installs; pacman untouched per the pause. All checks used git read-only commands and grep.

VERDICT: admit with listed fixes — D1 (i) ambiguity sentence, D2 subject + Check (c)/(d) for the two-sided bound; D3
folds into D2's (d). Adjacent 98→M3 cite reconciliation is for the L1, not a condition on 99.
