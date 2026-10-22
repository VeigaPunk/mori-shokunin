# ReviewRuleTextAmbiguity — attacking the rule-text-ambiguity disclosure (round 30, wave 2)

Verdict: **agree** — the disclosure is accurate where it is stated (entry `## Facts` 4 closing bullet,
lesson first bullets, contract A2) and no counted artifact over-claims text-decidedness; two low defects:
the disclosure is absent from SKILL row 2 (prominence gap), and three sentences overstate writer
isolation ("read only the rule text") against committed gate evidence.

Seat: MoriR30.ReviewRuleTextAmbiguity (reviewer, leaf — no subagents, no background jobs). Date: 2026-10-22.

Method and compliance: every claim below was re-derived from committed bytes at the measured tip
`ad0f04745ced2194e58c22a0d6b38131bee3e230`; I first verified the working tree matches the tip blob for
every file cited (blob equality via `git rev-parse <rev>:<path>` vs `git hash-object`, 14/14 match), so
`path:line` cites are tip bytes. Git use was read-only (`rev-parse`, `log --diff-filter=A`, `log`) in the
lane; no jj commands; no writes in the lane except this report; no scratch needed. No host read, no unit,
journal, setting or signal touched; no tool installed or updated (operator directive 2026-10-19: none
needed). Receipts (`c1-after.txt`, `c2-after.txt`, `c2-freeze-selftest-*.txt`, `gate-a2-prefreeze.txt`)
are read as committed bytes, not re-run; counter re-runs belong to the C1/C2 re-check seats. The `lsp`
device was not applicable: the audited artifacts are prose/markdown/JSON, no language server answers
these paths; text reading is the only channel here.

## The disclosure, re-derived from committed bytes

Three sites state it, all at tip:

- Entry `## Facts` 4, closing bullet (`corpus/knowledge/earlyoom-invocation-scope-r30.md:70-71`):
  "Disclosed: the rule text alone does not decide the shape uniquely — a literal reading of the scope
  line gives `KILLER_ACTED` (wave-1 `ReviewRuleTextShape` F1); the writers and the tool agree on the
  split reading." Echoed in Limits (`:111-112`): "the disputed shape is `KILLERS_UNKNOWN` with the send
  reported, not `KILLER_ACTED`. Disclosed, not a gap to re-litigate."
- Lesson (`corpus/lessons/round-30.md:15-18`): "The disputed shape is now pinned blind. … The rule text
  alone does not force that reading (wave-1 ReviewRuleTextShape F1); the agreement is evidence, not
  proof."
- Contract A2 (`/.ufo/waves/round-30/contract.md:196-200`): "Disclosed, uncounted: the rule text does
  not decide the disputed shape uniquely (ReviewRuleTextShape F1–F2 …); the counted after-value is
  agreement of four blind writers and the tool, not a proof that the text decides the shape."

## Accuracy — verified against the rule text

The fork is real. With `ActiveEnterTimestampMonotonic` absent or `0`, the scope line
(`rule-text.md:25-26`) admits every boot line, so verdict 1's "any … send line in scope"
(`rule-text.md:44-45`) fires on the pre-restart sends — w1 reading A1, `KILLER_ACTED`. Under the other
reading, `rule-text.md:29` (a version line is "the first line of an invocation") plus A2-06
(`rule-text.md:84-88`, `:110`, report-only for an active unit) leaves no positive evidence and verdict
2's active-plus-incomplete-scope clause fires (`rule-text.md:46-48` with `:82-83`) — the split reading.
This matches w1 F1 exactly (`.ufo/waves/round-30/w1/ReviewRuleTextShape.md:46-48` and the result table
`:29-43`). The disclosure sentences are faithful compressions; two wording nits:

- The entry attributes the ACTED reading to "the scope line" alone; it also needs verdict 1's in-scope
  trigger (`rule-text.md:44-45`). Harmless compression, same conclusion.
- The entry cites w1 F1 only; the co-forking fields — `earlier_invocation_send_lines` delimiter (w1 F2,
  `ReviewRuleTextShape.md:100`) and `sigterm` (w1 F3, `:113`) — are cited only in the contract
  (`contract.md:197`, "F1–F2"). Under the literal reading the entry's own Answer pins
  (`actions.sigterm: 0`, `:63-64`) would read `sigterm: N` instead, so the entry's "shape" wording
  covers this only loosely. Info-level; the contract carries the precise citation.

Empirical sentences inside the disclosure context check out against committed receipts: fixture frozen
at `db1ec469` (first-adding commit, no later touch, blob `a05863cc` at freeze and tip — verified by
read-only `git log --diff-filter=A` / `rev-parse`); entering-tip tool `58b61681:tools/mori-oom-killers.py`
and the changed tool both print `PASS 8/8` on the frozen file
(`evidence/c2-freeze-selftest-base.txt:3-4`, `evidence/c2-freeze-selftest-fixed.txt:2-4`); all eight
writer expects pin `KILLERS_UNKNOWN`/exit 2 (derivation tables `w1/CaseR30a.md:84,89`,
`CaseR30b.md:105,112`, `CaseR30c.md:63,69`, `CaseR30d.md:102,107`; counter `shape_verdicts=8/8`,
`authors=4`, `evidence/c2-after.txt`). So entry `:68-69` "all eight expect this answer and both the
entering-tip and the changed tool print it" is receipt-backed. The same receipt records
`blind_violations=1`, `C2=unmet` (`evidence/c2-after.txt`) — the author's conceded C2 miss; not my item.

## Prominence

- Entry: adequate. The disclosure is the closing bullet of the same Fact block that states the Answer
  (`:63-64` Answer, `:70-71` Disclosed), plus the Limits echo (`:111-112`).
- SKILL row 2 (`SKILL.md:753`): **the disclosure is absent.** The row states the A2a limit and the
  reader's abstention ("reported but is not a verdict input, so the reader abstains"), names the shape
  as "the disputed shape round 29 moved from `KILLER_ACTED` to `KILLERS_UNKNOWN`", and its not-to-conclude
  cell guards the two w1 failure modes ("that the earlier send proves the current invocation acted;
  … that the same shape reads `KILLERS_QUIET`") — but nothing tells a reader that the rule text does not
  force the pinned reading. Mitigations: the row's grounding cell points at the entry (which carries the
  disclosure) and at tool lines, not at a claim of text-derivation; and no file claims the disclosure
  lives in SKILL — lesson R6 (`round-30.md:194`) claims only the "A2a limit" is stated in the entry and
  SKILL, which is true. So this is a prominence gap, not a false claim anywhere.

## Over-claim inventory — does any round-30 file claim the text decides?

Sweep covered the entry, SKILL `## Round30` rows (`SKILL.md:752-755`), the lesson, contract, the fixture,
counters, receipts, and the w1 wave files. Files that claim more than the disclosure:

1. **The four blind writer reports (frozen data, disclosed as such).** Each asserts, with line cites and
   no `unclear` flag, that rule-text lines decide the disputed verdict: `w1/CaseR30a.md:7` ("Lines 46-48
   make an active earlyoom with incomplete scope KILLERS_UNKNOWN"), `CaseR30b.md:7`, `CaseR30c.md:7`
   ("lines 46-48 therefore yield KILLERS_UNKNOWN"), `CaseR30d.md:7`, plus their derivation tables
   (`CaseR30a.md:84,89`; `CaseR30b.md:105,112`; `CaseR30c.md:63,69`; `CaseR30d.md:102,107`). These are
   exactly the derivations w1 F1/F2 show are non-unique. They are blind-run artifacts — data, not lane
   claims — and the contract pre-committed to counting their agreement as evidence, not proof
   (`contract.md:196-200`); post-freeze edits are forbidden (`contract.md:171-173`, freeze
   identification). Listed because the assignment asks for files that claim more; none is a counted
   artifact.
2. **The writer briefs presume decidability of the forked fields.** `wave1-spec.json:10,15,20,25` and
   `wave1-dispatch.json:7,13,19,25`: "Derive every expected value from rule-text.md alone; where the text
   does not decide a value, do not pin it and say so" — next to mandatory pins of `verdict`, `exit`,
   `actions.sigterm`, `earlier_invocation_send_lines`, precisely the forked fields. The contradiction was
   caught pre-data (`w1/CriticSizing.md:59-62`, `w1/CriticC2Design.md:23-24`) and answered in the
   contract: an honest `unclear text` flag counts as a C2 miss (`contract.md:183-186`), and the
   disclosed-uncounted bullet neutralizes the epistemics. Residual tension stands: the design only
   avoids a miss because all four writers guessed the split reading without flagging — which is what
   happened, and what the disclosure now honestly labels agreement, not proof.
3. **Superseded draft (historical only).** `w1/DraftEntryC1.md:122-124` states the disputed answer
   grounded in a tool probe ("probe: invented inputs, `--inputs`, exit 2, those values") with no
   non-uniqueness disclosure; the landed entry replaced that grounding with the blind-writer sentence
   and the disclosure. Superseded by the entry header's binding note; no action possible or needed.

Checked and **not** over-claims: entry `:43-44` (conditional restatement of verdict 2, not a
decidability claim); SKILL.md:752 (row 1 states both branches of the split reading, entry-grounded);
SKILL.md:753 (A2a framing grounded in entry + tool lines); the decision table (entry `:93-107`) — it
deliberately contains **no** disputed-shape row, and its header says rows are "the case's frozen `expect`
values … printed by the entering-tip tool", i.e. frozen-expect framing, not text-derivation
(`c1-after.txt`: `rows=13`, `C1=met`); `w1/CriticHarmScreen.md:170-171` (D4 requires the SKILL row to say
UNKNOWN — a requirement, not a derivation claim); lesson R6 (`round-30.md:194`) — claims only the A2a
limit is in entry+SKILL, which is accurate; SOURCES rows S156-S160 (`corpus/SOURCES.md:162-166`) carry
no disputed-shape claim.

## Findings by severity

- **F1 (low) — SKILL row 2 lacks the non-uniqueness disclosure** (`SKILL.md:753`). A future reader
  re-deriving from `.ufo/waves/round-30/rule-text.md` — the same extract the writers used, still
  committed — finds the F1 fork with no warning at the SKILL layer; the guard exists one hop away in the
  cited entry (`earlyoom-invocation-scope-r30.md:70-71`). No file claims otherwise, so nothing is false;
  the fix, if the round wants it, is one grounding-cell clause naming the entry's disclosure, which
  would keep the counted SKILL-row shape (`c1-after.txt`: `skill_rows=4`). Recommendation, not a miss.
- **F2 (low) — writer isolation overstated in three sentences.** Entry `:68-69` and lesson `:15` say the
  writers "read only the rule text"; the fixture note (`tools/fixtures/mori-oom-killers/cases-a2-r30.json:4`)
  says "read only rule-text.md and public upstream sources". Committed gate evidence contradicts the
  strict reading: the A2 gate flagged one forbidden-opened path in **each** of the four reports, every
  one the host-injected godspeed skill (`evidence/gate-a2-prefreeze.txt:3-9`; `w1/CaseR30d.md:110`), and
  CaseR30a also lists `/home/vgpnk/.omp/agent/RULES.md` (same receipt, closing note). The reads are
  disclosed and allowlisted by A3 (`contract.md:207-221`) and lesson M5 (`round-30.md:94-98`), so the
  record self-corrects — but the three sentences as written claim more isolation than happened. The
  blindness conclusion (no writer saw the tool, a fixture or another report) survives: the gate's
  allowlist plus `provenance=8/8` (`evidence/c2-after.txt`) cover the case-relevant inputs.
- **F3 (info) — entry disclosure cites F1 only; field forks (w1 F2/F3) ride on the word "shape".**
  `earlyoom-invocation-scope-r30.md:70-71` vs `contract.md:197` (F1–F2) and
  `w1/ReviewRuleTextShape.md:100,113`.
- **F4 (info) — over-claim inventory** as listed above: writer reports (data, neutralized by
  `contract.md:196-200`), writer briefs (presumption, caught pre-data), superseded draft. No counted
  artifact — entry, SKILL rows, lesson, decision table, counters, receipts — claims the text decides
  `KILLERS_UNKNOWN`.

## Residual risk and verification gaps

- I did not re-run `count-c1.sh`/`count-c2.sh` or the gates; the receipts are committed bytes and C1/C2
  re-verification belongs to the dedicated seats. My accuracy claims about tool behavior rest on those
  receipts plus w1's static review, not on my own tool execution. [INFERENCE] I did not open
  `tools/mori-oom-killers.py`; SKILL row 2's tool-line grounding (`58b61681:…:293-302, :465-469,
  :487-489`) is unverified by me.
- I verified the eight expects' verdicts/exit via writer derivation tables and receipts, not field-by-field
  against the fixture's elided case bodies; the counter's `pins_ok=… fields=8/8` covers the rest.
- Scope: files at tip under `.ufo/waves/round-30/`, the entry, SKILL `## Round30`, the lesson, the
  fixture and receipts. Older SKILL sections (e.g. `SKILL.md:695-702`) and round-29 files are outside
  "round-30 files" and were not swept.

No tool installs or updates (directive of 2026-10-19 recorded: none needed).
