measured 2026-10-23T12:06:57Z
# CritAxisFit — round 36, wave 1

Scope: claim-to-axis and admission-design review, not native judgment, admission, or a landed-tool execution. The frozen predicates remain untouched. References below are lane-relative unless prefixed `fleet:`; `fleet:` means `/home/vgpnk/Projects/shokunin/`. Counter and control references mean `.ufo/waves/round-36/`.

## Axes and review verdicts

Freshness means re-verifying skill claims against live surfaces and flagging or fixing stale items; operability means runnable artifacts producing their stated outcome (`fleet:AXES.md:13-14`). Distinct axes and causal separability are required even for capability acquisitions (`fleet:AXES.md:27-41`). Freshness, depth and calibration are tied at 5 in the current table (`SCORECARD.md:12-14`).

VERDICT: C1 fails

This is a counter-to-freshness inference defect, not a finding that an implementation following the frozen byte rules is incorrect. The named fetch/comparison operation is freshness-directed, but its positive receipt can certify representation differences rather than changed sources or stale skill claims (counterexample below; `contract.md:13,21,35-47`).

VERDICT: C2 holds

The proposed surface is genuinely operability: a runnable append-only check gains deleted-row detection. This exceeds merely registering the old script, although registration/self-test delivery still requires separate evidence (`contract.md:14,62-83`; `corpus/lessons/round-35-verifier-spotcheck.md:172-178`). This review does not assert that the proposed gate has already landed or passed.

## C1 — strongest local counterexample: unchanged S156 becomes drifted

1. The selected copy is an annotated, noncontiguous excerpt, not a saved response body. It starts with provenance fields, adds source line numbers, and jumps from source line 28 to 106 (`corpus/evidence/sources-r30/S156.txt:1-20`). The original lesson explicitly calls these committed excerpts (`corpus/lessons/round-30.md:104-110`).
2. Its stored original-response digest is `b56aa781be9c29b610156925030d3c4ab720c0ad73d57907d230ca3047302f2a` (`corpus/evidence/sources-r30/S156.txt:3`; `corpus/lessons/round-30.md:114`).
3. I opened the ordinary pinned URL once. Command, run from the lane:

   `timeout 45s curl --fail --location --silent --show-error --max-time 30 https://raw.githubusercontent.com/systemd/systemd/v262/src/shared/bus-print-properties.c | timeout 45s sha256sum`

   Output: `b56aa781be9c29b610156925030d3c4ab720c0ad73d57907d230ca3047302f2a  -`

   Thus the fetched source bytes equal the recorded round-30 source bytes; there is no response-body change relative to that recorded digest.
4. The annotated copy has a different digest. Commands:

   `timeout 10s sha256sum corpus/evidence/sources-r30/S156.txt`

   Output: `4c02999410622d782979d025a9a61314104873cba9c19e4857feba4bd0473b5e  corpus/evidence/sources-r30/S156.txt`

   `timeout 10s git show 6bd57097:corpus/evidence/sources-r30/S156.txt | timeout 10s sha256sum`

   Output: `4c02999410622d782979d025a9a61314104873cba9c19e4857feba4bd0473b5e  -`

   The representation mismatch therefore predates this round's data work; it is not hypothetical worktree interference.
5. The existing v2 receipt actually labels S156 oracle-drifted (`evidence/c0-rescore-v2.txt:1141-1142`). Its correct reference classifier meets P-C1 with 35 fresh and 7 drifted real rows (`evidence/c0-rescore-v2.txt:1153-1159`). Those are existing receipts, not runs I performed.

Why it matters: the frozen rule compares the whole annotated copy against the fetched body; ASCII trimming does not remove headers or source line numbers (`contract.md:38-45`; `count-c1.py:109-124`). A false staleness witness therefore helps satisfy the required oracle-drifted floor (`count-c1.py:630-637`). The counter's registry parser retains id, URL and source text, not teaches or used-by; the classifier consumes response/copy bytes, not the skill's claims (`count-c1.py:129-144,235-268`).

[INFERENCE] An unchanged source can consequently remain drifted indefinitely solely because its saved representation is annotated. Conversely, leaving an incorrect teaches/skill assertion uncorrected need not change any C1 decision. This is not a semantic freshness check, even when the byte classifier is perfect. Existing lane guidance already distinguishes passage presence from source support and locator drift from fact drift (`SKILL.md:804-809`).

Impacted axes: freshness is not established by P-C1 alone; describing these results as verified stale facts would also overstate calibration (`fleet:AXES.md:14-15`). No harm to either axis is asserted merely from creating an honestly labelled byte-comparison probe.

Smallest safe correction now: preserve the frozen claim and receipts, disclose that drifted means a byte/representation discrepancy, and do not infer freshness admission solely from C1=met. Do not relabel the claim, rewrite the counter, or silently replace historical evidence after data (`fleet:.ufo/prompts/mori-round-36.md:351,357-361`). For a future freeze, compare like representations and connect the real witness to the source/skill assertion being re-verified; the present claim's missing evidence must remain visible rather than be amended away.

## C2 — repair overlap and admission boundary

The old script already detects immutable edits and changed-back ids, but computes endpoint violations only over ids still present at the tip (`.ufo/waves/round-35/check-sources-appendonly.py:84-100,119-124`). The outside review separately routes deleted rows as an acknowledged gap in item 2, while item 3 asks for registration, self-test and final-fix receipts (`corpus/lessons/round-35-verifier-spotcheck.md:172-178`). C2 therefore adds an operation beyond item 3; its origin in routed debt does not make that operation disappear.

The strongest deletion skip is already exercised: J5 omits deletion reporting, matches the real historical arm, but fails the blind arm 0/24 and finishes C2=unmet (`evidence/c0-rescore-v2.txt:476-482,552-558`). The real arm's deleted list is empty, so the forced sandbox deletions are essential evidence, not redundant decoration (same receipt).

Fixable admission gap: P-C2 checks executable output, not the promised registration or self-invocation self-test. The counter extracts only the tool blob, runs histories, and compares summaries (`count-c2.py:590-621,624-643,677-686,722-725`). Its own positive reference is a scratch program and meets P-C2 (`evidence/c0-rescore-v2.txt:1161-1171`). That demonstrates algorithm reachability, not a registered, conformant lane gate.

Smallest safe correction: keep P-C2 frozen; separately land and cite the SKILL registry row, fixture self-invocation asserting exit plus stable finding-id, and revision-bound committed evidence required by the gate standard (`/home/vgpnk/Projects/kimi-shokunin/skills/shokunin/protocol/PROTOCOL.md:398-419,428-435`). Since QUALITY 102 still names the old wave command, append an explicit current-authority pointer rather than leave the promoted tool and historical checker as competing enforcement instructions (`corpus/QUALITY.md:802-810`; `contract.md:14`). This is fixable delivery work, not grounds to deny the deleted-row operation's operability fit.

## Independence, controls and anti-loop

- Causal separation holds by design: C1 reads the registry/copies and live HTTP; C2 reads Git history and never needs the C1 program or its output. C2's real input is fixed at the entering historical revision, not C1's new artifact (`contract.md:21-23,35-47,62-83`). Sharing SOURCES and the frontier source row is sharing input, not requiring either tool to land first (`contract.md:16-17`). C1's clean-corpus requirement constrains measurement scheduling, not causal independence (`count-c1.py:567-580`).
- Neither literal do-nothing control meets the frozen target. K1 produces no classifications: 40 blind mismatches, C1=unmet (`evidence/c0-rescore-v2.txt:858-884`). J1's empty summary fails both arms and gives C2=unmet (`evidence/c0-rescore-v2.txt:2-8,75-85`). The v2 record reports 25 negative controls unmet and two positive references met (`evidence/freeze-v2.txt:3-5`). This does not cure the C1 axis-inference defect above.
- These are not calibration claims in disguise: they measure executable behavior, not SCORECARD/SHONEN mismatch counts; that distinction matches the prompt's calibration rule (`contract.md:13-23`; `fleet:.ufo/prompts/mori-round-36.md:348-349`).
- They do not repeat the r35 empty-prose register mechanism: r35 never read the capability/what cells and credited denial/off-topic registers; the present blind arms compare enumerated states or exact id lists (`corpus/lessons/round-35-verifier-spotcheck.md:60-74`; `count-c1.py:298-312,539-562`; `count-c2.py:517-522,590-621`).
- But the randomized-fixture plus real-oracle architecture is not new: r34 C1 already declared that structure (`.ufo/waves/round-34/contract.md:52-63`). It failed when a harness-keyed program could skip real classification and live sampling (`corpus/lessons/round-34-verifier-spotcheck.md:65-76`). Current K9/J11 v2 controls fail their real arms, addressing those particular path shortcuts rather than proving all shortcuts impossible (`evidence/c0-rescore-v2.txt:176-190,1138-1151`).
- Historical wording defect, not a new authority: round-36 contract lines 4-5 call r32-r35 four calibration counters. The actual claims were r32 freshness, r33 depth, r34 coverage plus exploratory calibration, and r35 calibration (`.ufo/waves/round-32/contract.md:15-34`; `.ufo/waves/round-33/contract.md:24-42`; `.ufo/waves/round-34/contract.md:7-18,90-97`; `.ufo/waves/round-35/contract.md:14-20`). Preserve the frozen bytes and record the correction outside them.

## Exercised evidence and limits

Only the single ordinary S156 GET and the three digest commands recorded above were executed. Existing counter receipts were read, not re-run. No lane tool, counter, self-test, build, formatter, native judge, alternate runtime or background job was invoked; no code was authored and no tools were installed or updated. The landed-tip counters and gate delivery checks remain the integration owner's verification, not passes claimed by this review.
