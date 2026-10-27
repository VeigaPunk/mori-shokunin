# Mo56CritC2Claim — falsification review of the C2 vote-binding claim

Seat: Mo56CritC2Claim (mori-shokunin, leaf critic). Freeze tip analyzed:
`8be2717b0809281d07dffe83dad424a4859e0747` (all reads via read-only
`git show`/`grep` at that rev; the frozen counter was executed against git
objects, not the working tree). Scratch:
`/fast/scratch/hyaku/mori-r56/Mo56CritC2Claim/` (removed at exit; candidate
tools and arm harness were scratch-only and are quoted below by command +
output). No fleet or lane files mutated; no votes carried; no tools installed
or upgraded (none needed). Counter rerun, evidence:
`TMPDIR=<scratch>/tmp python3 .ufo/waves/round-56/count-c2.py 8be2717b0809281d07dffe83dad424a4859e0747`
→ `C2=met selftest=ok tally=ok control=ok contrast=voted0 entry=ok row=ok rev=8be2717b0809281d07dffe83dad424a4859e0747`, rc=0 (reproduces
`evidence/c2-at-freeze.txt`).

## (a) Re-binding round-55 bytes: operability capability, or re-scoring history?

The standing fleet rule (`.ufo/prompts/kasegi-round-23.md:372`, same text in
the sibling lane prompts): "Re-scoring a rule the lane already holds on new
inputs, or counting rows a sourceless fixture also counts, is quality work,
never coverage or depth."

Case for "just re-scoring history":

- The tally arm's inputs are bytes the lane already holds — the round-55
  ledger `corpus/knowledge/kernel-v7.3-recheck-r55.md` and the orchestrator's
  `.ufo/waves/round-55/w1-results.json`. The produced
  `TALLY rows=78 agree=78 double=68 single=10 zero=0 dissent=0 voters=16
  bound_voters=15` re-counts votes already emitted by the round-55 voters and
  ledger rows whose verification content was already closed; no new
  verification ground is created and the underlying kernel claims gain
  nothing.
- Had this claim been typed on coverage or depth, the standing rule would bar
  it: the counting command demonstrably re-scores an existing ledger on
  inputs the lane already held at freeze time.

Case for "operability capability acquisition":

- The rule names coverage and depth only. AXES.md provides a distinct claim
  type for exactly this shape: "A claim may instead be a **capability
  acquisition** … it still lands a per-axis verdict." The capabilities
  repertoire table measures "what the shokunin can now *do*", and rows "enter
  only through a round that demonstrates the capability running". C2 is typed
  and recorded (SCORECARD round-56 claim table, axis `operability 7`) as a
  capability acquisition, not a coverage/depth move.
- The capability is the runnable artifact `tools/mori-vote-bind.py` — pinned
  sha256, 16-case selftest, `tally`/`extract` CLI. That is the operability
  axis signal verbatim ("commands that exist, scripts that run"). The
  re-bound tally is the *demonstration that the capability runs over real
  committed bytes* — the evidence pointer the capabilities-table rule
  requires — not the capability itself.
- The claim's surface is new: the entry records `coverage-map: new
  capability — seat-output vote binding (no prior lane note)`. The frozen
  old instrument demonstrably cannot do it (contrast arm: the frozen r55 C1
  counter reads `voted=0` on the same bytes — reproduced locally, see (b)
  experiment 3), and the do-nothing control shows the new run is not
  vacuous.

Verdict: the classification as an operability capability acquisition is
correct and survives the re-scoring rule. The rule governs coverage and depth
claims; a new runnable operation demonstrated on real bytes, with a named
contrast instrument that cannot perform it, is the canonical capability
pattern. The strongest counterargument — that the demonstration input is
historical — is a real but named limit, not a misclassification: fixable by a
live use (e.g. the planned dispatch validator consuming the binder), route to
round 57; it does not convert the claim into re-scoring, because the
capability claimed is the operation, not the number it prints.

## (b) Can a do-nothing control meet count-c2.py?

The counter's executable arms (selftest banner, exact tally on committed
bytes, junk control → `zero=78` and `double=0`) plus the pin and the
contrast arm were replicated in scratch
(`exp/run_arms.py`, candidates `exp/cand_*.py`, inputs = committed bytes
extracted with `git show 8be2717b:...`). Command + output:

1. Real tool baseline (materialized from `git show 8be2717b:tools/mori-vote-bind.py`):
   `python3 run_arms.py real_tool.py` → `failed=none`,
   `real-tally: TALLY rows=78 agree=78 double=68 single=10 zero=0 dissent=0 voters=16 bound_voters=15`.
2. Constant-print stub (`cand_constant.py`, prints the expected selftest and
   tally banners, ignores inputs): `failed=control` — on the junk results
   file it prints `double=68`, so the control arm's `zero=78`/`double=0`
   requirement kills it. A pure echo do-nothing cannot reach the target.
3. Plain-line binder (`cand_plainline.py`, the frozen r55 C1 binding
   semantics — a vote binds only as a stripped *text* line): `failed=tally`,
   `real-tally: TALLY rows=78 agree=0 double=0 single=0 zero=78 ...` — it
   reproduces the round-55 `voted=0` cause on the committed bytes. No
   preexisting plain-text tally tool can meet the target.
4. Substring binder (`cand_substring.py`, the frozen r55 C2 ENTAIL-arm
   semantics — `.ufo/waves/round-55/count-c2.py:19` "whose output contains
   that same line"): `failed=none`; its tally line on the committed bytes is
   byte-identical to the real tool's. This cheaper control *skips the claimed
   work entirely* — no JSON channel, no scalar anchoring, no fence or
   overclaim discipline — yet meets every executable arm.
5. Divergence probe (synthetic results.json: voter A's JSON output mentions
   ``RECHECK a6e5226259c9 holds`` inside a prose string, voter B carries a
   proper `vote_lines` array): real tool → `single=1 ... bound_voters=1`;
   substring binder → `double=1 ... bound_voters=2`. The two tools are
   behaviorally distinguishable, but no committed round-55 byte triggers the
   difference, so the frozen counter's executable arms cannot tell them
   apart; only the frozen PIN (identity of bytes authored with the claim)
   excludes the weaker tool.

Preexisting-tool angle: `grep -l "TALLY rows=" tools/*.py
.ufo/waves/round-5*/count-*.py` → only `tools/mori-vote-bind.py` and
`.ufo/waves/round-56/count-c2.py`; at the entering tip the tool is absent
(`evidence/controls.txt` do-nothing-c2 → `failed=tool_absent`), and the pin
checks the sha256 of `tools/mori-vote-bind.py` at R. A preexisting tool
therefore cannot meet the counter on two independent grounds (pin, selftest
banner).

Verdict: no *preexisting* or *constant-print* do-nothing control meets
count-c2.py — but the executable arms alone are met by a strictly weaker
substring binder that skips the claimed dual-shape parsing. Under the
fleet's own standing rule ("a target must be one a do-nothing control cannot
reach … build the cheapest control that skips the claimed work"), the arms
are under-discriminating: the claimed work is enforced by identity (PIN),
not by behavior. This is a fixable defect in the frozen counter, reported as
a named limit with a routed item for round 57 (add one arm the substring
binder fails, e.g. a results fixture with a vote sentence inside a prose
string, which experiment 5 shows separates the tools). It is not grounds to
reject C2 this round: the pin binds the shipped bytes, the shipped bytes
genuinely implement the dual-shape parser (16-case selftest; the authors'
own frozen mutation receipts kill exactly this weakness class —
`mut:substring-scalar-binding KILLED arm=t_json_prose_substring_rejected`,
`controls.txt`), and the honest demonstration receipt stands.

## (c) Is the capability-table row warranted, and was the capability demonstrated running?

AXES.md: "Rows enter only through a round that demonstrates the capability
running; a capability without a passing demonstration in the round report is
pre-claiming and does not enter the table."

Demonstrated running: yes. The frozen counter at R is itself the
demonstration — it executes the pinned tool from git objects: 16-case
selftest (rc 0, `pass=16 fail=0`), the real-byte tally (exact frozen line),
the junk control (`zero=78`), and the contrast run of the frozen r55 C1
counter (`voted=0`). Receipt `evidence/c2-at-freeze.txt` rc 0; my independent
rerun at the freeze tip (header above) reproduces `C2=met`, rc 0.

Warranted: yes, with two register-wording qualifications for the L1's
closure write: (i) the capability's delta over history is the *standalone,
tested* dual-shape parser with overclaim/fence/hash discipline — substring
binding per se already existed inside the frozen r55 C2 counter (acknowledged
in the entry itself), so the row must not phrase the capability as "vote
binding" simpliciter or it overclaims novelty; (ii) the demonstration's
real-data arm is the historical re-bind (limit from (a)).

SCORECARD state: the round-56 section currently carries the claim table only
(the file ends at line 2905); the capabilities row enters at closure via
MANIFEST `capabilities_added` per the round-35 register convention. That is
process-normal, not pre-claiming, because the demonstration receipt exists
this round.

Verdict: the row is warranted; the capability was demonstrated running at the
freeze revision by a frozen, independently re-runnable receipt.

## Supplementary evidence

- Roster shape on committed bytes: 16/16 roster voters present in
  `.ufo/waves/round-55/w1-results.json`; 15 outputs contain the vote verb
  only inside JSON string scalars; 0 carry a stripped plain vote line —
  independently confirms the round-55 failure cause (1) on the bytes C2
  re-binds.
- S545 registry row and entry at 8be2717b match the contract (`mined`,
  `2026-10-27`, used-by naming the entry and the tool; entry names S545 and
  `tools/mori-vote-bind.py`).
- Before-receipt asymmetry: `evidence/controls.txt` shows count-c1.py marks
  unevaluated arms `bad` on `tool_absent` while count-c2.py prints them
  `ok` (its `evaluate()` returns before any arm runs; `main()` labels arms
  not in the failed list `ok`). The before labels on the C2 line are vacuous
  defaults, not measurements.

## Findings

- MED — `.ufo/waves/round-56/count-c2.py` executable arms: a substring
  binder implementing the frozen r55 C2 "output contains" semantics (30
  lines, no JSON parsing, no overclaim/fence discipline) passes selftest,
  tally, and control arms byte-identically on the committed round-55 bytes
  (experiment 4 above); the two tools diverge only on inputs no committed
  byte exercises (experiment 5). The claimed dual-shape work is enforced by
  the PIN, not behaviorally falsified by the counter. Route to round 57 as a
  counter-arm addition (a prose-mention or fenced-scalar results fixture the
  substring binder fails); do not change the frozen counter this round.
- LOW — `.ufo/waves/round-56/count-c2.py:67-70,157-165`: at the entering tip
  the counter returns `failed=tool_absent` before evaluating any arm, and
  `main()` prints the unevaluated arms `selftest=ok tally=ok control=ok
  contrast=voted0 entry=ok row=ok` (see `evidence/controls.txt`), while
  count-c1.py marks the same situation `bad` for every arm. Cosmetic
  asymmetry; before-cell arm labels on the C2 line must not be cited as
  measured. Wording/limit note for round 57.
- LOW — `tools/mori-vote-bind.py` demonstration scope: the capability's only
  real-data run is a historical re-bind of round-55 bytes; no live wave has
  consumed the binder. Route to round 57: exercise the binder in a live
  settlement (the planned dispatch validator is the natural consumer). This
  is the same limit named in (a); it caps how strongly the closure may word
  the register row.
- INFO — round-55 committed bytes: 15 of 16 roster voters carried the vote
  verb only as JSON string scalars, 0 as stripped text lines; the contrast
  arm's `voted=0` cause (1) independently re-verified on committed bytes.
- INFO — no preexisting lane tool prints a `TALLY` banner or could satisfy
  the pin/selftest pair; the preexisting-tool do-nothing threat is excluded.
