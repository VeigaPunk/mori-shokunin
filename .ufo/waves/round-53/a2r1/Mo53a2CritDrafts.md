# Mo53a2CritDrafts — residual integration draft review

Reviewed revision `34d97cd3eaea8c13b0f065afc52aac1e5cf518a5` (and frozen contract `f4da3fd400fa88a6db8ea544a4f7045c15d2410e`). Axes attacked: freshness, coverage, calibration, adjacency, operability (pointer/evidence integrity).

## Findings

- **HIGH — LOG.md:2860:** both cited after-receipts `evidence/c1-at-landed.txt` and `evidence/c2-at-landed.txt` are absent at the reviewed revision. `git ls-tree -r --name-only 34d97cd... .ufo/waves/round-53/evidence` lists at-data and at-salvage receipts, not landed receipts. The text also claims a `census-end.txt`, absent at this revision (only `census-start.txt` exists), despite contract §Separability requiring end census exit 0. Do not present these as existing evidence. Smallest correction: replace LOG's sentence beginning `After: the landed receipts` with `At salvage (0df803033fba2386b10f5dcc6aa96bdef65cba15): C1=met ... (evidence/c1-at-salvage.txt); C2=met ... (evidence/c2-at-salvage.txt). No landed receipts or census-end receipt are present in this revision; round-end census is UNVERIFIED.` If they are produced later, cite them only after they land and quote their actual output. This is a data/evidence gap, not a counter change.

- **HIGH — LOG.md:2866:** `end in evidence/census-end.txt` is dangling, and the contract explicitly requires an end census rc 0. Replace `end in evidence/census-end.txt` with `end census receipt not present at reviewed revision; round-end census UNVERIFIED` unless a verified receipt is added. Do not infer success from census-start.

- **MED — SHONEN.md:8 / corpus/QUALITY.md:1381-1477:** SHONEN points to `corpus/QUALITY.md:1381-1477`, which does in fact contain criteria 144–147 and supports the checklist claim. But the cited line span is not self-verifying for the word “criteria”: criterion 144 states recheck ledger/two votes; 145 the mode/band rule; 146 receipt-number fidelity; 147 own-commit command. No criterion defines the SHONEN checklist itself. Marking `[~]` is appropriate; do not present these as completed independent verification.

- **MED — corpus/README.md:754-755:** freshness paragraph correctly describes the at-data receipt (`C1=unmet`, no votes), but there is no after/landed receipt at this revision; do not imply C1 was admitted. Resource-runway paragraph cites `c2-at-landed.txt` (in the truncated continuation; the file is absent). Replace its after-counter citation/value with the at-salvage evidence, explicitly labeling the revision, or omit the post-wave counter result pending a landed receipt. Do not use C2-at-data as proof of post-wave state.

- **MED — PROVINCE.md:422-429, 444-455:** the appendix is careful to disclaim remediation and notes that choosing mode/ratio/reserve belongs to operator and tsukuroi. The potential bleed is the blanket phrase at 453 that deciding whether a commit refusal is a host fault belongs to “the operator and tsukuroi”: evidence here establishes only that this is outside mori's detection/report scope; it does not establish that tsukuroi owns commit-accounting fault attribution. `kumitate` is not named in this appendix. Smallest safe replacement for lines 451-453: `Boundaries: choosing vm.overcommit_memory, overcommit_ratio, overcommit_kbytes, admin_reserve_kbytes or user_reserve_kbytes, and deciding whether a commit refusal is a host fault, are outside this lane's detection/report remit; no ownership assignment is made here. This note claims no admission...` If the intended ownership is operator-only, cite an authoritative ownership source; do not assign it to tsukuroi from this evidence.

- **LOW — SHONEN.md:6:** `LOG.md:2841` resolves to the correct Round 53 heading, but its claim is actually supported by the body at 2848-2855, and it does not establish that the section's claimed end receipts exist. Minimal pointer correction: cite `LOG.md:2848-2860` and retain `[~]`; the heading line alone only identifies the round.

- **LOW — PROVINCE.md:428 and corpus/README.md:755:** the listed rows/coverage evidence is internally plausible and agrees with frozen contract scope: S502–S510 for C1, S511–S514 for C2. No count discrepancy found in the quoted 46/44/2/46 values. The title “Round-53 coverage additions” appropriately distinguishes new runway ground from freshness recheck.

## Evidence checked

- `git -C /home/vgpnk/Projects/shokunin/mori-shokunin ls-tree -r --name-only 34d97cd3eaea8c13b0f065afc52aac1e5cf518a5 .ufo/waves/round-53/evidence` — exit 0; enumerated receipts, including `c1-at-salvage.txt`, `c2-at-salvage.txt`, `census-start.txt`; no `c1-at-landed.txt`, `c2-at-landed.txt`, or `census-end.txt`.
- `git show 34d97cd...:corpus/QUALITY.md` lines 1381–1477 — criteria 144–147 present.
- `git show 34d97cd...:SKILL.md` lines 1178 onward — commit-runway decision table and error patterns present.
- `git show 34d97cd...:PROVINCE.md` lines 402–455 — appended notes and boundaries as reviewed.

No checks or counters were run; no tool or counter change proposed.
