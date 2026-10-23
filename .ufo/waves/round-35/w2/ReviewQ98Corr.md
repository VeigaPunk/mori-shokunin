measured 2026-10-23T09:17:10Z

Attacked text: `corpus/QUALITY.md:769-778` at cedb0ec4f3a4f672804deac388b7191258f01fcd (the paragraph beginning

"98 correction (round 35, append-only; round-34 spot-check §6 item 5)"). Sources attacked against:
QUALITY.md:715-731 (criterion 98), `.ufo/waves/round-34/contract.md`, `.ufo/waves/round-34/evidence/c1-controls.txt`,
`.ufo/waves/round-35/contract.md`. `git diff 8d56809 cedb0ec` on both round-34 cited files is empty, so every
cited line is identical at the revision the correction cites and at the landed tip.

Origin check (context, not a counted defect): the paragraph carries defects D1, D2, D4 named by reviewer
ReviewC2Judge3 (`.ufo/waves/round-34/wb/ReviewC2Judge3.md:22-25`) and routed by the spot-check
(`corpus/lessons/round-34-verifier-spotcheck.md:209-213`, order "D2, D1, D4"). The skipped label D3 is the
lesson-citation defect that round 34 already fixed at QUALITY.md:763 ("round-34 Mistakes M3"), so the D1/D2/D4
selection is complete for the routed scope.

VERDICT: supported — D1 ("98 lists 'a rule changed, or rows deleted, after data' as a shape, but round 34's
control table … has no row for a rule changed after data; its inapplicability entry covers only rows deleted
after judgment"). 98's shape list reads "a rule changed, or rows deleted, after data" (QUALITY.md:717-718).
The round-34 table (contract.md:69-81) holds 10 data rows; the only post-judgment row is :81
"rows deleted after judgment … inapplicable to C1: no judge; the judged object is the tool bytes at the landed
tip" — it names the deletion half only; no row names a changed rule or states inapplicability for it. A defender
can argue :81's reason (tool-bytes-only judging) or the kill rule (contract.md:62-63 freezes counter/rules)
covers rule changes, but 98(a) tests whether the table names every shape, and neither is stated in the table —
the correction's stated fact is accurate. ReviewC2Judge3 itself graded D1 "minor, wording … defensible
purposively" (wb/ReviewC2Judge3.md:23), so the correction's "breaks its own rules" phrasing is stronger than
the source audit but the underlying observation is the same. Cited range contract.md:65-81 covers the table
(the table proper is :69-81); slightly wide, includes heading/prose — a pin looseness, not an error.

VERDICT: supported — D2 ("server-echo row reads `unmet (guard)` … and the C-echo-v1 receipt shows the guard
trip … by 98's own sentence a guard trip discharges only the skip-work and content-free shapes, so server echo
was not discharged"). contract.md:78 reads "| server echo (kama r26) | C-echo: imports this counter's oracle
by path | unmet (guard) |"; c1-controls.txt:26-28 shows control 09 with `guard=['.ufo', 'count-c1']` on both
runs (also row 16, controls.txt:47-49). 98's discharge sentence: "a control that fails by generic absence
(deliverable absent, guard tripped) discharges only the skip-work and content-free shapes" (QUALITY.md:719-721).
The cleanest case is the P-C1 line: v1 scores 12/12 + 300/300 + live=ok — the guard trip is the sole rejection
cause, a pure generic-absence failure, which under 98 discharges nothing but skip-work/content-free. Residual
contestability [INFERENCE]: the P-C1-A1 run also fails substantively (fixed 0/12, live-rc=1, line 28) because
the A1 namespace blocks the oracle read — one could argue the shape was substantively discharged under A1.
But the contract's own annotation is `unmet (guard)`, so the correction's claim that the worked example
advertises a guard-based discharge it does not license stands. Pin: contract.md:77-78 contains the row but the
row itself is :78 (off-by-one looseness, matches the source review's own cite at ReviewC2Judge3.md:22).

VERDICT: supported — D4 ("the contract says three of its 16 negative controls met P-C1 (contract.md:142-143);
four runs met … in three shape groups"). contract.md:142-143 reads "all 16 negative controls `C1=unmet` under
P-C1-A1 (three of / them met P-C1)" — "them" = the 16 negative controls, i.e. control runs. The receipt shows
exactly four negative-control P-C1 `C1=met` lines: control 10 C-echo-v2-base64 (controls.txt:29-30),
11 C-echo-v3-umount (:32-33), 13 C-emptylive (:38-39), 14 C-zero-singleread (:41-42) — the correction's cited
ranges :29-34 and :38-43 pin all four and name them correctly. Three is defensible only as a shape-group count
(contract.md:115 "Three shapes met P-C1", whose bullets group C-emptylive with its rate-0 variant and echo v2/v3
as one shape each — three groups), which is exactly the reading the correction reports ("in three shape
groups"). Under the contract's own "of the 16 negative controls" wording the sentence is misstated; the
correction describes the discrepancy accurately and fairly. Row count confirmed: controls 01-16 negative,
17-18 positive; no other P-C1 `C1=met` among negatives.

VERDICT: supported — last sentence ("Round 35's own contract … also fails 98(a): it names no server-echo,
observed-column-copy, no-decision or rule-changed control"). 98(a): "the contract's control table names every
shape above once" (QUALITY.md:724); shapes include generic rows, observed-column copy, server echo,
label/id-keyed, skip-work, content-free, no-decision, rule-changed/rows-deleted (QUALITY.md:715-718).
Round-35's Controls list (.ufo/waves/round-35/contract.md, "### Controls"): items 1-10 name do-nothing,
no-reader/delete, junk, label-keyed, all-false/wrong-round, shotgun, rejected-round, stale pointers, dangling,
and catch-all #10 "any further skip program". Server echo, observed-column copy, no-decision and rule-changed
are neither named nor given a stated inapplicability, and #10 is an open net, not a per-shape mapping; several
listed items (wrong-round, shotgun, rejected-round, stale, dangling) are also not among 98's seven shapes.
The lane's own lesson records the same four omissions plus a missing denial control
(`corpus/lessons/round-35.md:64`, mistake M1), matching the correction's "(round-35 lesson M1)" cite.
Minor wording point: the R35 controls are a numbered list, not a literal table, and item 2 (delete the
Capabilities sections / empty heading) arguably gestures at the rows-deleted shape — but nothing names the
rule-changed half or states inapplicability, so 98(a) fails as the correction says.

Framing claim ("98's worked example breaks its own rules three ways"): accurate for the routed scope — D1/D2
break rules internal to 98 (shape table completeness, discharge semantics); D4 is a misstatement in the
contract the example endorses (ReviewC2Judge3.md:25 grades it "minor, C1-side"), so "its own rules" is loose
there but consistent with the spot-check's grouping (spotcheck :209 groups all three as worked-example
defects). The "round-34 spot-check §6 item 5" provenance cite is exact (spotcheck :209-213).

Residual risk: none of the four statements is refuted. Pin looseness (D1 range includes the section heading;
D2 range is one line wide) does not change any verdict. The strongest counter-readings — :81's reason covers
rule changes (D1), A1's run fails substantively (D2), "three" = shapes (D4), r35 controls are precedents that
don't apply to a registry claim (last sentence) — are all arguable defences that the correction itself or the
source audit already anticipates; none makes a stated fact false.

Verification gaps: I did not re-run count-c1.py on the control revisions (deadline-bounded; the receipt is the
committed record and its lines are quoted verbatim). No installs made.
