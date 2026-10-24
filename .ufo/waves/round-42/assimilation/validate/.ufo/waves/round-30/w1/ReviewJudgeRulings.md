# ReviewJudgeRulings — pre-data harm screen for C2.1 (round 30, wave 1)

Seat: MoriR30.ReviewJudgeRulings (leaf reviewer). 2026-10-22. Findings only; no edits; a verdict here
is a recommendation, never a ruling. Lane: /home/vgpnk/Projects/shokunin/mori-shokunin, entering tip
58b61681a0e3f3b821a17d38a4e713ccd9921615.

Method and limits:

- Read: the three judged reports (.ufo/waves/round-29/w2/Judge11.md, Judge12.md, Judge13.md), the
  three case objects they judged (tools/fixtures/mori-oom-killers/cases-a2-r29.json:953-1066), the
  round-30 binding rule text (.ufo/waves/round-30/rule-text.md), both round-29 residual dissents
  (.ufo/waves/round-29/residual/ReviewLandedFix.md, CriticC2Verdict.md), and the round-30 claim
  contract (.ufo/waves/round-30/contract.md).
- No LSP device exists in this seat's toolset, so every check below is textual (rule text against
  case pins against judged reports); no language server stands behind any claim. Recorded as a
  verification gap in section 5.
- Tool-behavior facts are cited from the residual reports' own path:line citations, not re-run by
  this seat: sibling seats are mid-flight on the same tool file and a fresh run could race their
  edits. Every such use is marked "cited".
- No tools installed or updated. No subagents, no background jobs, no lane writes except this report.
- Wave-wide blindness respected: no tool source lines or tool output are pasted below. Case values
  quoted are the frozen fixtures' own invented values (timestamps only).

## 1. Ground truth: what Judge11-13 judged

All three reports end `case_ruling=tool error`; every mismatch they found is a tool error, none is a
case error or unclear text.

| case (cases-a2-r29.json) | judged tool-error fields | verdict/exit pin |
|---|---|---|
| r29-a2-10-inactive-lone-missing-stamp (:953-987) | version, grammar, earlier_invocation_send_lines (base 1, expect 0), dryrun_send_lines, process_group_lines | KILLERS_QUIET / 0 (:973-974) |
| r29-a2-10-failed-stamped-positive (:988-1026) | version, grammar, earlier_invocation_send_lines (base 2, fix 1, expect 0), dryrun_send_lines, process_group_lines | KILLER_ACTED / 1 (:1013-1014) |
| r29-a2-10-not-found-earlier-stamped-positive (:1027-1066) | version, grammar, dryrun_send_lines, process_group_lines (earlier fixed 2 -> 1 = expect) | KILLER_ACTED / 1 (:1052-1053) |

## 2. The assigned question, field by field

Does the rule text require the case value (tool error) or contradict it (case error)?

### 2.1 earlyoom.version = "1.9.0" (pins :977, :1017, :1056) — text requires it; tool error

Deciding lines (rule-text.md):

- :25-26 "Scope: earlyoom lines whose `__MONOTONIC_TIMESTAMP` ≥ `ActiveEnterTimestampMonotonic` of
  the current earlyoom invocation, in the current boot."
- :29 "`earlyoom <version>` → version (the first line of an invocation; `main.c:161`)"
- :39-40 "`scope_complete` (true only when the version line of the current invocation is inside the
  scope)"

Each case carries a version line exactly at the retained `ActiveEnterTimestampMonotonic`
(:963-964 @4100000 vs :959; :998-999 @5200000 vs :994; :1041-1042 @6300000 vs :1033), so each is
inside the scope (the boundary is inclusive: ≥), and :29 maps it to "1.9.0". The text conditions
version on nothing else — not on state. A null version contradicts :29 given :25-26. Tool error, as
all three judges ruled on exactly this pair.

Residual: ReviewLandedFix F1.3 grades these pins "at best unclear text" because the text never says a
non-active unit reports a version. That reading helps nobody: unclear text is itself a C2 miss
(contract.md:99-100), and the judges' tool-error rulings stand. Note :39-40 presupposes "the version
line of the current invocation" is well-defined for any unit with a retained boundary; it does not
restrict the invocation to active units.

### 2.2 earlyoom.grammar = "verified-1.9.0" (pins :978, :1018, :1057) — tool error, derivative of 2.1

Deciding line: rule-text.md:38 "`grammar` (`verified-1.9.0` or `unverified`)". The field's only two
values track whether the version line was parsed; with version = 1.9.0 (2.1) the value is
verified-1.9.0. No state condition appears anywhere in the text. Tool error (judged, all three cases).

### 2.3 earlyoom.earlier_invocation_send_lines — split by case

Deciding lines:

- rule-text.md:84-88 and :110 (A2-06): "send lines of this boot outside the current invocation go to
  `earlyoom.earlier_invocation_send_lines`; non-zero is positive evidence (`KILLER_ACTED`) for an
  earlyoom that is not active, reported without a verdict change for an active one"
- rule-text.md:114 and :95-96 (A2-10 / D1): a record without a numeric `__MONOTONIC_TIMESTAMP` "is
  left uncounted and makes the scope incomplete; positive evidence elsewhere still stands"
- rule-text.md:25-26 (scope, quoted in 2.1).

- Case 1 (:981 expect 0): the unit's only send record is stamp-less (:966-969, no
  `__MONOTONIC_TIMESTAMP` key), so A2-10 leaves it uncounted — it enters no bucket and earlier must
  be 0. Base 1 counted it: tool error, settled; the landed tool already reports 0 here (cited:
  ReviewLandedFix F5 inv3; Judge11 fix column).
- Case 3 (:1060 expect 1): the SIGTERM at 6299000 (:1037-1038) is < AETM 6300000 (:1033) — of this
  boot and outside the current invocation — so A2-06 routes it to earlier (1), and its non-zero value
  is positive evidence for a not-active unit, reinforced by A2-09 (:113). Settled; the landed tool
  gives 1 (Judge13 fix column).
- Case 2 (:1020 expect 0): the only genuinely two-readable field. The stamped SIGTERM at 5200001
  (:1002-1003) is ≥ AETM 5200000 (:994). Under :25-26 it is inside the current invocation, so A2-06
  does not route it to earlier and the pin 0 is required. The contrary reading (expect should be 1)
  needs the premise "a failed unit has no current invocation, so every timestamped line is earlier".
  That premise appears nowhere in the rule text: :25-26 and A2-06 speak of "the current earlyoom
  invocation" for every unit, and A2-06 itself measures "outside" lines for non-active units —
  measuring requires a reference invocation. CriticC2Verdict F1 traced the premise to a tool comment,
  not contract text. Judge12 ruled tool error; ReviewLandedFix F1.2 dissents (calls the case
  self-contradictory). Ruling: the text requires the case value; tool error stands; the dissent
  re-reads, it does not contradict.
  - Consistency check that decides it: the AETM-bounds-the-current-invocation reading makes Judge12
    (case 2 expect 0) and Judge13 (case 3 expect 1) jointly correct — sends ≥ the boundary are
    current, sends < it are earlier. The landed tool's behavior for non-active states (all timestamped
    lines to earlier; cited: ReviewLandedFix F1.2) satisfies Judge13 but not Judge12, so under two
    standing rulings of the same protocol it cannot be the text's meaning.
  - The verdict carrier for case 2 is independent of this counter: rule 1 keys on the line — "any
    earlyoom `sending SIG…to process` or escalation line in scope … Positive evidence stands even
    when the scope is incomplete" (:44-45). The send is in scope under :25-26, so KILLER_ACTED has
    its carrier even with `actions` null. ReviewLandedFix F1.2's "no in-scope carrier" holds only
    under its own no-current-invocation premise — circular.

### 2.4 dryrun_send_lines = 0 and process_group_lines = 0 (:982-983, :1021-1022, :1061-1062) — text requires 0; tool error; the sharpest contradiction theory lives here

Deciding lines:

- rule-text.md:49-51: "An inactive or absent killer reports `actions: null` (unavailable), never zero
  counts; quiet then means 'no positive evidence from the killers that are readable' …"
- rule-text.md:73-74 (A5): "`killing whole process group ` lines are counted in
  `earlyoom.process_group_lines`; every count is a count of earlyoom log lines, not of processes
  signalled or killed"
- rule-text.md:75-76 (A6) and :108 (A2-04): after `dryrun mode enabled`, send lines go to
  `earlyoom.dryrun_send_lines` …
- rule-text.md:107 (A2-03).

Neither message occurs in any of the three journals (:961-969, :996-1009, :1035-1048). A5/A6 define
both counters purely by line occurrence, and A5 adds "every count is a count of earlyoom log lines" —
zero matching lines can only mean 0. Nothing in the text conditions these counters on `actions`.

Against that, ReviewLandedFix F1.1 reads :49-51's "never zero counts" as governing every count field
of an inactive or absent killer, making the six pins (cases 1 and 3) contradict the text — case
error. The plain grammar is against that reading: the sentence's subject is `actions: null`; "never
zero counts" explains why an unavailable killer's action counts are null rather than zero (unknown,
not measured zero). Three further textual facts cap it:

1. The same output reports `earlier_invocation_send_lines` — a count — for non-active units, and a
   frozen older-file case pins it non-zero for an inactive unit (frozen `a2-06` pins 3; cited:
   CriticC2Verdict F1). Counts-for-non-active is already the operative contract behavior.
2. Case 2's unit is `failed` → state `unavailable` (rule-text.md:71-72; pin :1016). :49-51 names
   "inactive or absent" only, so even the broad reading cannot decide case 2's zeros.
3. The landed tool itself already reports earlier_invocation_send_lines = 0 for the case-1 unit
   (settled field, 2.3) without anyone reading :49-51 against it — the broad reading would condemn
   the landed tool's own settled output.

Ruling: the text requires 0; tool error (judged). Residual: this is the one field class where "the
rule text contradicts the case" is colorable, so it is the fix's main harm exposure (3.1).

### 2.5 verdict and exit — settled, with one disclosed tension

- Case 1 QUIET/0 (:973-974): after A2-10 removes the lone record, no positive evidence exists
  anywhere (oomd_notices 0 at :970; earlier 0) → rule 3 (:49-51). Base KILLER_ACTED was the tool
  error; the landed tool reads QUIET/0 here (cited: ReviewLandedFix F5 inv3).
- Cases 2-3 ACTED/1 (:1013-1014, :1052-1053): positive evidence stands despite the incomplete scope
  (:44-45) — case 2's in-scope send (2.3), case 3's earlier count for a not-found unit (:110, :113).
- Tension to disclose, not a dispute: A2b / A2-02 maps a `failed` ActiveState to "state `unavailable`
  and `KILLERS_UNKNOWN`" (:71-72, :106) without a no-positive-evidence qualifier, while case 2 pins
  KILLER_ACTED. The reconciliation is precedence: rule 2 begins "no positive evidence, and any of:"
  (:46), so its triggers govern only the evidence-free case, and A2-06/A2-09 explicitly create ACTED
  for not-active units. A closure reading A2b literally would condemn the base tool the same judges
  passed on verdict and contradict A2-06/A2-09 — not a live harm theory, but the amendment should
  state the precedence (section 4).

## 3. Harm screen: could a judged tool fix to pass these three cases be judged a harm?

Frame from the claim contract: the fix follows the Judge11-13 tool-error rulings, changes the tool
never a case file, must keep conditions 1-2 (residual PASS 24/24 and older pins held), and "may not
turn any `KILLER_ACTED` of an older file into another verdict" (contract.md:98-102); the retention
scan must not rise (contract.md, "Held, not claimed").

Procedurally, no harm is possible: all mismatches are judged tool error by non-author judges, the
protocol authorizes exactly this fix, and the case file stays frozen (contract.md:98-100).

Substantive harm theories an outside closure could raise, ranked:

**3.1 (medium) The "never zero counts" broad reading.** If the closure adopts ReviewLandedFix F1.1,
reporting the two counters as 0 for the inactive (case 1) and absent (case 3) units violates
rule-text.md:49-51, so the L1 "changed the tool where a rule does contradict a frozen case" — outside
its authority, hence a harm. Why it should fail: the sentence's grammatical subject is `actions`
(which stays null in any correct fix); A5's "every count is a count of earlyoom log lines" forces 0
when no line occurs; the same output already reports a count field for non-active units and a frozen
case pins 3 for an inactive one; and :49-51 does not name `unavailable`, so it cannot decide case 2
at all. Exposure is real because the reading exists in a lane report a closure may weigh. Mitigation:
a counted rule-text amendment settling "counters 0 or null when actions is null" before or with the
fix, so the closure judges the fix against settled text (CriticC2Verdict F1 item (b)).

**3.2 (medium) The "non-active units have no current invocation" premise.** Under ReviewLandedFix
F1.2, case 2's earlier pin (0) is self-contradictory → case error → the fix would be "repairing" a
case the protocol calls a miss → harm. Why it should fail: the premise is absent from the rule text
(a tool comment, per CriticC2Verdict F1); the scope line and A2-06 presuppose a current invocation
for every unit; and the premise cannot be held consistently with Judge13 standing — its case needs a
current invocation to call the 6299000 send "outside" it. A closure adopting it re-rules the
non-author judges: the second-authority problem CriticC2Verdict F1 named. Mitigation: the amendment
should state the reading explicitly ("a non-zero retained ActiveEnterTimestampMonotonic bounds the
current invocation for any state") as a counted decision (CriticC2Verdict F1 item (a)).

**3.3 (low-medium, concrete trap) Collateral regressions.** CriticC2Verdict's probe proves
feasibility — across 134 inputs (four case files plus a2-detectors) verdict_flips=[] and the older
tallies hold (32/32, 32/32, 30/30) — but the same probe turns `null` into `0` for unreadable-show
states (c25, c32). A real fix must not: reporting counts or a version for a unit whose show read
failed invents facts about an unreadable killer — the exact protection :49-51 encodes — and a closure
could judge that a harm even with no frozen pin on it. Related absolute bound: any ACTED→QUIET flip
anywhere is evidence dropped; it would breach contract.md:101-102 and A2-06's stated purpose ("a stop
without restart no longer reads quiet", :86-87). By construction the fix must keep version, grammar
and the counters null when the boundary is missing/0 or the show read failed, and keep every
positive-evidence carrier intact.

**3.4 (low) Coupling with the C2.3 blind shape.** The needed fix touches non-active-state behavior at
a non-zero AETM; the blind file pins active units with AETM absent or 0 — different branches of the
same tool file. The risk is a fix that reworks the shared split/scope logic and moves the
unbounded-active outcome after writers froze their pins. Related disclosure: the landed tool's
unbounded-active demotion (sends before the last version line reported as earlier, verdict UNKNOWN)
implements a rule the extract does not state (cited: CriticC2Verdict F4 H1); writers reading only
rule-text.md may pin the plain-text outcome for that shape instead. That dispute is C2.3's to settle
in the same amendment (CriticC2Verdict item (d)); flagged here only as a same-file coupling hazard.

**3.5 (low) A2b literalism vs case 2's ACTED** (2.5 tension). Live only if a closure reads :71-72 as
an unconditional verdict override; that reading contradicts :46 and A2-06/A2-09 and condemns the base
tool. Mitigation: one amendment sentence stating that positive-evidence rules (rule 1, A2-06, A2-09)
take precedence over A2-02's KILLERS_UNKNOWN.

Bottom line: under the rule text read plainly, every disputed case value is required by the text —
tool error on all counts, no case error, no unclear text. A fix is therefore authorized and, per the
probe, feasible with zero verdict flips. It could be judged a harm only through theory 3.1 or 3.2
(both ReviewLandedFix F1 re-readings) or by committing the 3.3 trap. The re-readings fail on grammar,
on the frozen-files precedent, and on judge authority; the trap is avoidable by construction.

## 4. Recommendation to the integration owner (MoriR30)

Land one counted, numbered rule-text amendment before or with the fix, settling:

- (a) a non-zero retained ActiveEnterTimestampMonotonic bounds the current invocation for any state;
  sends ≥ it are current-invocation (positive evidence per rule 1), sends < it are earlier (A2-06);
- (b) dryrun_send_lines and process_group_lines are counts keyed to line occurrence (0 when no
  matching line), independent of `actions: null`, which stays null for inactive/absent per :49-51;
- (c) A2-02's KILLERS_UNKNOWN applies only when rule 1's positive evidence is absent;
- (d) the unbounded (AETM absent/0) shape's scope and verdict, so the C2.3 blind pins and the tool
  agree by construction.

Never touch the frozen case files; the fix stays tool-only and keeps conditions 1-2.

## 5. Residual risk and verification gaps

- No LSP device in this seat's toolset: all checks are textual; no semantic server stands behind any
  claim above.
- Tool-state facts (landed behavior on the three cases, the c25/c32 null→0 probe effect,
  verdict_flips=[]) are cited from the residual reports' citations, not re-run here:
  ReviewLandedFix.md F1/F5, CriticC2Verdict.md F1/F4. Sibling seats are mid-flight on the same tool
  file; a fresh run could have raced their edits.
- Not run by this seat: the tool, selftest, counters, blind gate. Round-26 contract original line
  numbers are used only as the judges and residual seats cite them; all quoted rule text above is
  quoted from the round-30 binding extract (.ufo/waves/round-30/rule-text.md) with its own line
  numbers.
- Out of scope, noted: Judge02 vs Judge04's conflicting `dryrun` rulings (cited: CriticC2Verdict F2)
  — same field, different cases; amendment items (b)/(d) must not disturb the frozen r29 a2-07 cases
  that pass at the entering tip.
- No tools installed or updated; no subagents or background jobs; lane writes: this report only.
