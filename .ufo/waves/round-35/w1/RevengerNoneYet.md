measured 2026-10-23T08:52:02Z

# RevengerNoneYet — why SCORECARD.md:586-592 still says `— none yet —` while 18 capabilities were admitted

Seat: MoriR35.RevengerNoneYet (leaf, wave 1). Reconstructed from executable evidence: lane git
history (read-only), frozen counter `count-c1.py`, fleet MANIFEST at `37b51a24` (read-only `git show`),
frozen round-35 contract, pre-data receipts, lessons/closures.

LSP note (role rule): the `lsp` device (`xd://lsp`) is not mounted in this leaf (no `/xd/lsp`, no
device dir; `/home/vgpnk/.omp/agent/agents/revenger.md:10` prescribes it "whenever a server answers the
file" — none answers here; sibling seats record the same absence, e.g. `.ufo/waves/shokunin12h-20261014-p2-kumitate/members/NoteVerifyNativeJudgePipeline.md`). All findings below are therefore literal
text/`git show` evidence, not semantic LSP proof. Recorded per role.

## The three registers and what each says

1. Contract-field table (the thing the task asks about): `SCORECARD.md:586-592` — `## Capabilities`
   with one row `| — none yet — | | | |`, introduced by **d677cf3** ("protocol conformance: adopt
   SCORECARD.md contract fields (2026-10-16 operator amendment rollout) — additive scaffolds only, no
   axis claims", 2026-10-16 22:40:54 -03). It also added `## Saturation` (594) and a LOG block
   (`LOG.md:533-543`): "Added by this rollout, purely additively at the end of SCORECARD.md: `##
   Capabilities` (empty repertoire scaffold) … no axis claim … none enter through this rollout."
2. Fleet MANIFEST (the closure record the round-35 contract uses as oracle): at
   `37b51a243302e8009c7067431e8a47f9a722fd14:MANIFEST.json`, mori lane `capabilities_added` across
   admitted closures = **18**: r12×1, r14×1, r15×1, r16×1, r18×3, r19×1, r22×1, r24×2, r25×2,
   r26×1, r28×2, r31×2 (r17×3 present but `admitted=false`, excluded — matches the contract's "18"
   list at `.ufo/waves/round-35/contract.md:22-26`).
3. Per-round SCORECARD capability tables (the actual record-keeping): the file contains one h2
   `## Capabilities` **empty** table (line 586), a second h2 `## Capabilities (round 12 demonstrations)`
   (line 627, 5 rows), and then h3 sections `### Capabilities demonstrated round 13` (708), `###
   capabilities: round18 table-shape repair` (1175), `### capabilities: first demonstrated round19`
   (1224), `round 20` (1265), `round 24` (1530), `round 25` (1564), `round 26` (1616) — plus
   heading-less inline tables for r14 (799-803), r15 (886-888), r21 (1339-1341), r22 (1405-1407),
   and r16 (990-992).

## Timeline (commit → what happened to the register)

- `d677cf3` (2026-10-16): adds empty `## Capabilities` contract scaffold; explicitly defers any row.
- `1f07f1d` (2026-10-19, round 12): adds `## Capabilities (round 12 demonstrations)` at 627 **below**
  the contract scaffold, with 5 rows (source registry, live census, census self-test, silence oracle,
  drift pin). Line 625: "Capability rows (below) enter through this round's demonstrations." The
  scaffold at 586 is left untouched. `git log -S '— none yet —' -- SCORECARD.md` → **only d677cf3**
  ever touched that cell; it is byte-identical at the tip.
- Rounds 13-31: each admitted capability is recorded in the round's own section (h3 or inline table),
  or not at all — MANIFEST admits capabilities for r14/r15/r22/r28/r31 that have **no** dedicated
  SCORECARD capability table (r14/r15 use prose heading-less tables at 801/886; r22 only inside the
  claim table 1386/1407; r28/r31 have no capability row at all). No commit ever merges a row into the
  standing table at 586-592.
- `7d949b4` (2026-10-21, round 19 commit): the only "capability table" correction in history: the
  round-18 closure defect #6 (`corpus/lessons/round-18-verifier-spotcheck.md:179-181`: "put the three
  tools in the SCORECARD.md capabilities table format required by AXES.md, with evidence pointer and
  first-working round") and lesson M4 (`corpus/lessons/round-19.md:32`) land the r18 table-shape
  repair at 1175. That fix interpreted the AXES requirement as a **per-round formatting** rule, not as
  maintenance of one canonical contract register.
- Round 35 (frozen): `count-c1.py` `register_rows()` takes `cap[-1]` — the **last** h2 section whose
  heading starts `## Capabilities`, i.e. the round-12 demos table at 627, not the contract scaffold at
  586. Before receipt (`evidence/c1-before.txt`, at `dd76eb79`): `register='## Capabilities (round 12
  demonstrations)' oracle=18 rows=5 matched=0 missing=18 bad=0 extra=5 mismatches=23 C1=unmet`, exit 1
  — also confirmed in `evidence/c1-controls.txt` row 1.

## Mechanism (why it drifted)

- The 2026-10-16 amendment defined **one** repertoire table (`AXES.md:57-64` "SCORECARD.md therefore
  carries a separate `capabilities:` table … Rows enter only through a round that demonstrates the
  capability running"; field table at `AXES.md:80`). d677cf3 created it empty and deferred entry.
- Round 12 then created a **second, parallel** h2 section instead of filling the scaffold; subsequent
  rounds appended per-round h3 sections. The file accumulated many capability sections; the standing
  contract table was never the place rows were written.
- No gate or QUALITY criterion ever enforced the standing table. The QUALITY criteria on capabilities
  (Q60 first-working-round actuality, Q62 missing-capability red from the measured before boundary —
  `corpus/QUALITY.md:202-221`) govern *evidence honesty per row*, not *register maintenance*. The
  stagnation nudge (`SCORECARD.md:639-641`, N=3) references "a capability entering the table", but
  rounds pointed at their own per-round tables, so it never fired.
- The same class of drift — standing table stale while rounds append — was noticed and repaired **for
  the Axes table**: r25 (`e68855d` "SCORECARD Axes table brought to the closure-admitted scores with a
  correction note (C1 item D5)"; r25 capability row `round-24 routed-defect and Axes-table check` at
  1569; r29 `420d05a` "C1 fix — standing Axes table rows cite the latest admitted closure per axis";
  r31 contract notes the Axes `Last change` still stale at 116-117). Closures that reviewed SCORECARD
  (r34 spot-check §3: `git diff f10a320d 3a7a89ea -- SCORECARD.md` → `+22 −0` "appends … rewrites no
  row") checked append-only-ness and the Axes table, never the capabilities register. The stale
  `— none yet —` cell was never noticed by any round or closure before round-35's own frozen counter
  named it (contract `:24-26`). `grep 'none yet'` over `corpus/` and `.ufo/reports/` → no matches.

## captured-by

None. No QUALITY criterion, closure gate, or prior counter covered the standing contract-field table's
sync with fleet closure records; the only mechanism that finally caught it is the round-35 frozen
counter (P-C1) itself, which was built for exactly this. The closest historical gates (round-18 R6 /
Q60 formatting rule; Axes-table counters r25/r29) covered format and the *Axes* table, not the
capabilities register.

## Verdicts

VERDICT: rows unsupported — the `| — none yet — |` row at SCORECARD.md:590 is unsupported: 18
capabilities are recorded as admitted in fleet MANIFEST 37b51a24 and appear in per-round SCORECARD
sections (627, 708, 801, 886, 990, 1175, 1224, 1265, 1341, 1407, 1530, 1564, 1616), none of which
populated the contract-field table.
VERDICT: sources admit — fleet MANIFEST 37b51a24, lane SCORECARD.md (lines above), lessons
round-18/19, and the frozen round-35 contract/counter are mutually consistent about the count and the
drift; they are reliable primary records.
VERDICT: claims holds — the mechanism claim holds: d677cf3 created an empty scaffold with deferred
entry; round 12 (1f07f1d) started a parallel per-round recording convention; rounds appended instead of
updating; no gate/QC enforced the standing table; the mismatch surfaced only via the round-35 counter.
VERDICT: audits agree — the round-18 outside closure's capability-table defect (#6) and round-19 M4
agree on the AXES table requirement; they covered per-round shape, not register sync, so they did not
catch the drift but support the reconstructed intent.
VERDICT: code no defect found — `count-c1.py` behaves correctly; its choice of the *last*
`## Capabilities` h2 section (the round-12 demos table) is the frozen contract's definition
(contract `:35`), and before-receipt `C1=unmet` is the true state, not a counter bug.
VERDICT: supported — the stale contract-field table at SCORECARD.md:586-592 while 18 capabilities were
admitted is a real, verifiable, mined mistake usable for this round: introduced by d677cf3, first
diverged at 1f07f1d, never repaired or noticed until round 35's frozen counter, and captured by no
existing QUALITY criterion or gate.

DRAFT mined-mistake (for L1): class = scorecard-contract drift; evidence = SCORECARD.md:586-592
vs 627/708/801/886/990/1175/1224/1265/1341/1407/1530/1564/1616 vs MANIFEST 37b51a24 (18 caps);
commit trail d677cf3 → 1f07f1d → … → tip; captured-by = none (new QC criterion: the SCORECARD
`capabilities:` contract field must be reconciled against the fleet MANIFEST closure record each
admitted round or when the register section changes).
